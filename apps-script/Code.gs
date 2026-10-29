/** Marketing Eraa: approved prospects -> GitHub -> Hostinger -> verified Google Sheet links.
 *  Use as a BOUND script (Extensions > Apps Script) in the MASTER spreadsheet.
 *  Needs Script Property GITHUB_TOKEN (fine-grained token: Contents read/write on one repo).
 *  No lead email, phone, private notes, or outreach drafts are transmitted to GitHub.
 */
const ME = Object.freeze({
  owner: 'k6658489-a11y',
  repo: 'marketing-eraa-demo',
  branch: 'main',
  csv: 'data/prospects.csv',
  host: 'https://demo.marketingeraa.com',
  countries: ['UAE', 'UK', 'USA'],
  header: ['country','business_name','slug','industry','city','services','business_email','business_phone','headline','approved_for_demo'],
  required: ['Business Name','City / Region','Industry','Services / Observations','Demo Approval','Demo Slug','Demo Status','Demo Preview URL'],
  // Existing master Sheet column names, not A1 positions. Do not rename headers.
});

function onOpen() {
  SpreadsheetApp.getUi().createMenu('Marketing Eraa Demos')
    .addItem('1. Test Sheet & GitHub', 'testConnections')
    .addItem('2. Preview approved leads (no publishing)', 'previewApprovedDemos')
    .addItem('3. Sync approved demos to GitHub', 'syncApprovedDemos')
    .addItem('4. Verify published demo URLs', 'verifyPublishedDemos')
    .addSeparator()
    .addItem('Enable 15-minute automatic sync & checks', 'installAutomation')
    .addItem('Disable automatic sync & checks', 'removeAutomation')
    .addToUi();
}

function testConnections() {
  const book = SpreadsheetApp.getActiveSpreadsheet();
  ME.countries.forEach(name => {
    const sheet = book.getSheetByName(name);
    if (!sheet) throw new Error('Missing sheet ' + name);
    getColumns_(sheet);
    Logger.log(name + ': header OK; ' + Math.max(0, sheet.getLastRow()-1) + ' data rows');
  });
  const response = github_('get', repositoryUrl_(), null);
  if (response.status !== 200) throw new Error('GitHub connection failed HTTP ' + response.status);
  const details = JSON.parse(response.body);
  if (details.full_name !== ME.owner + '/' + ME.repo) throw new Error('Wrong GitHub repository');
  Logger.log('GitHub OK: ' + details.full_name + ', branch=' + details.default_branch + ', private=' + details.private);
  Logger.log('Connection test passed. No files have been changed.');
}

function getColumns_(sheet) {
  const row = sheet.getRange(1, 1, 1, sheet.getLastColumn()).getDisplayValues()[0].map(s => String(s).trim());
  const result = {};
  row.forEach((name, i) => { if (name) result[name] = i; });
  ME.required.forEach(name => { if (!(name in result)) throw new Error(sheet.getName() + ': missing header ' + name); });
  return result;
}

function cell_(row, columns, name) {
  return String(row[columns[name]] == null ? '' : row[columns[name]]).trim();
}

function key_(item) { return item.country + '/' + item.slug; }
function validSlug_(slug) { return /^[a-z0-9]+(?:-[a-z0-9]+)*$/.test(slug) && slug.length <= 80; }
function textOnly_(value, max) { return String(value || '').replace(/[\u0000-\u001f\u007f]/g, ' ').trim().slice(0,max); }

function fingerprint_(item) {
  const content = [item.country, item.name, item.slug, item.industry,
    item.city, item.services, item.headline].join('\x1f');
  const bytes = Utilities.computeDigest(Utilities.DigestAlgorithm.SHA_256, content, Utilities.Charset.UTF_8);
  return bytes.map(byte => ('0' + (byte & 0xff).toString(16)).slice(-2)).join('').slice(0,12);
}

function gatherApproved_() {
  const book = SpreadsheetApp.getActiveSpreadsheet();
  const entries = [], seen = new Set();
  for (const country of ME.countries) {
    const sheet = book.getSheetByName(country);
    if (!sheet) throw new Error('Missing tab ' + country);
    const columns = getColumns_(sheet);
    const numRows = sheet.getLastRow();
    if (numRows <= 1) continue;
    // Display values ensure consistency for business-name and custom text columns.
    const rows = sheet.getRange(2, 1, numRows-1, sheet.getLastColumn()).getDisplayValues();
    rows.forEach((row, i) => {
      const approval = cell_(row, columns, 'Demo Approval').toLowerCase();
      if (approval !== 'yes' && approval !== 'approved') return;
      const name = textOnly_(cell_(row, columns, 'Business Name'),120);
      const city = textOnly_(cell_(row, columns, 'City / Region'),160);
      const industry = textOnly_(cell_(row, columns, 'Industry'),90);
      const services = textOnly_(cell_(row, columns, 'Services / Observations'),300);
      const slug = cell_(row, columns, 'Demo Slug').toLowerCase();
      if (!name || !city || !industry || !services || !validSlug_(slug)) {
        throw new Error('Incomplete approved lead: ' + country + ' row ' + (i + 2) + '. Add business, city, industry, services and valid demo slug.');
      }
      const item = {country:country.toLowerCase(), name, slug, industry, city, services,
        headline:'', sheet, columns, rowNumber:i+2};
      if (seen.has(key_(item))) throw new Error('Duplicate demo slug: ' + key_(item));
      seen.add(key_(item));
      item.version = fingerprint_(item);
      entries.push(item);
    });
  }
  return entries.sort((a,b) => key_(a).localeCompare(key_(b)));
}

function previewApprovedDemos() {
  const entries = gatherApproved_();
  Logger.log('Approved demo concepts: ' + entries.length + '. NO website files were changed.');
  entries.forEach(item => Logger.log(key_(item) + ' (' + item.version + ')'));
}

function csvCell_(text) { return '"' + String(text == null ? '' : text).replace(/"/g, '""') + '"'; }
function createCsv_(entries) {
  const rows = [ME.header];
  entries.forEach(e => rows.push([e.country,e.name,e.slug,e.industry,e.city,e.services,'','',e.headline,'yes']));
  return rows.map(row => row.map(csvCell_).join(',')).join('\n') + '\n';
}
function repositoryUrl_() { return 'https://api.github.com/repos/' + ME.owner + '/' + ME.repo; }
function contentsUrl_() { return repositoryUrl_() + '/contents/' + ME.csv; }

function github_(method, url, payload) {
  const token = PropertiesService.getScriptProperties().getProperty('GITHUB_TOKEN');
  if (!token) throw new Error('Missing GITHUB_TOKEN in Apps Script Project Settings > Script Properties');
  const options = {
    method:method,
    headers:{'Authorization':'Bearer ' + token,
      'Accept':'application/vnd.github+json','X-GitHub-Api-Version':'2022-11-28'},
    muteHttpExceptions:true,
    followRedirects:true
  };
  if (payload !== null) { options.contentType='application/json'; options.payload=JSON.stringify(payload); }
  const response=UrlFetchApp.fetch(url, options);
  return {status:response.getResponseCode(), body:response.getContentText()};
}

function readGitHubCsv_() {
  const r=github_('get', contentsUrl_() + '?ref=' + encodeURIComponent(ME.branch), null);
  if (r.status === 404) return {sha:null, content:null};
  if (r.status !== 200) throw new Error('Cannot read GitHub CSV. HTTP ' + r.status + ' ' + r.body.slice(0,200));
  const file=JSON.parse(r.body);
  if (!file.content || !file.sha || file.encoding !== 'base64') throw new Error('GitHub CSV contents could not be decoded');
  const content=Utilities.newBlob(Utilities.base64Decode(file.content.replace(/\s/g,''))).getDataAsString('UTF-8');
  return {sha:file.sha,content};
}

function writeStatus_(item, status, url) {
  const cols=item.columns, sh=item.sheet;
  sh.getRange(item.rowNumber, cols['Demo Status']+1).setValue(status);
  if (url !== undefined) sh.getRange(item.rowNumber, cols['Demo Preview URL']+1).setValue(url);
}

function syncApprovedDemos() {
  const lock=LockService.getScriptLock();
  if (!lock.tryLock(15000)) { Logger.log('Another sync is active; skipping'); return; }
  try {
    const entries=gatherApproved_();
    if (!entries.length) { Logger.log('No approved leads. Skipping CSV replacement; existing previews unchanged.'); return; }
    const csv=createCsv_(entries);
    const current=readGitHubCsv_();
    if (current.content === csv) { Logger.log('GitHub CSV already up to date ('+entries.length+' demos)'); return; }
    const payload={message:'Sync approved Marketing Eraa website demos from Sheet',
      content:Utilities.base64Encode(csv,Utilities.Charset.UTF_8),branch:ME.branch};
    if (current.sha) payload.sha=current.sha;
    const out=github_('put',contentsUrl_(),payload);
    if (![200,201].includes(out.status)) throw new Error('GitHub upload HTTP '+out.status+' '+out.body.slice(0,260));
    entries.forEach(item => {
      // The URL is not exposed to the spreadsheet before a live page passes verification.
      writeStatus_(item,'Queued — GitHub build and Hostinger deployment pending','');
    });
    Logger.log('Synced '+entries.length+' approved previews to GitHub. Hostinger URL not yet verified.');
  } finally {lock.releaseLock();}
}

function verifyPublishedDemos() {
  const lock=LockService.getScriptLock();
  if (!lock.tryLock(15000)) { Logger.log('Another verification is active; skipping'); return; }
  try {
    const entries=gatherApproved_();
    let verified=0, pending=0;
    entries.forEach(item => {
      const url=ME.host+'/'+item.country+'/'+item.slug+'/';
      const statusCell=item.sheet.getRange(item.rowNumber,item.columns['Demo Status']+1);
      const linkCell=item.sheet.getRange(item.rowNumber,item.columns['Demo Preview URL']+1);
      try {
        // Only a page containing the unique key AND matching current source fingerprint counts as published.
        const response=UrlFetchApp.fetch(url+'?me_verify='+item.version,{
          method:'get',muteHttpExceptions:true,followRedirects:true,
          headers:{'Cache-Control':'no-cache'}
        });
        const body=response.getContentText();
        const matchKey='data-demo-key="'+key_(item)+'"';
        const matchVersion='data-demo-version="'+item.version+'"';
        if (response.getResponseCode() === 200 && body.includes(matchKey) && body.includes(matchVersion)) {
          statusCell.setValue('Published & verified');
          linkCell.setValue(url);
          verified++;
        } else {
          pending++;
          // Leave a previously verified URL alone if unrelated fetch/transient error; otherwise keep it blank.
          if (linkCell.getDisplayValue().trim() !== url) {
            statusCell.setValue('Pending deployment / version mismatch (HTTP '+response.getResponseCode()+')');
          }
        }
      } catch(err) {
        pending++;
        Logger.log('Pending '+key_(item)+': '+err.message);
      }
    });
    Logger.log('Published and current: '+verified+' | Not yet verified: '+pending);
  } finally {lock.releaseLock();}
}

function installAutomation() {
  removeAutomation();
  ScriptApp.newTrigger('syncApprovedDemos').timeBased().everyMinutes(15).create();
  ScriptApp.newTrigger('verifyPublishedDemos').timeBased().everyMinutes(15).create();
  Logger.log('Installed background sync + site verification roughly every 15 minutes.');
}

function removeAutomation() {
  const names=new Set(['syncApprovedDemos','verifyPublishedDemos']);
  ScriptApp.getProjectTriggers().forEach(t => {
    if (names.has(t.getHandlerFunction())) ScriptApp.deleteTrigger(t);
  });
  Logger.log('Old Marketing Eraa automation triggers removed (if any).');
}
