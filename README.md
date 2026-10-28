# Marketing Eraa demo website generator

Generate static, unofficial homepage previews for prospect businesses from a CSV of independently verified information. No API keys or paid services needed. Industry themes: cleaning, plumbing, landscaping, beauty, automotive, consulting, general.

## Install into your existing repository

Download this package and **extract it**. Upload the `tools` folder, `data` folder, `.htaccess`, and `.github/workflows/generate-demos.yml` into the root of your existing `marketing-eraa-demo` GitHub repository on the `main` branch. **Do not overwrite the existing `index.html` or `uae/test-business/index.html`.** Keep directory paths, especially the hidden `.github` folder.

## Use

Edit `data/prospects.csv`. Add a row for a real prospect only after independent verification. CSV headings:

`country,business_name,slug,industry,city,services,business_email,business_phone,headline,approved_for_demo`

- `country` must be `uae`, `uk`, or `usa`.
- `slug` should contain only lowercase letters, numbers and hyphens; use a distinct value for each prospect.
- `industry` supports cleaning/plumbing/landscaping/beauty/automotive/consulting/general.
- `services` is a pipe-delimited list, like `Home Cleaning|Office Cleaning`.
- Set `approved_for_demo` to `yes` only after checking facts, content and source usage. Otherwise the row is skipped.
- Leave unknown contact information blank. Don't invent reviews, awards, guarantees, services or contact details.
- Quotes/commas in fields must be CSV-escaped by the editor; Google Sheets CSV export handles this.

### Illustrative row — DO NOT publish as a real prospect

`uae,Sample Cleaning Company,sample-cleaning,cleaning,Dubai,Office Cleaning|Home Cleaning,,,Cleaning services for your space,no`

This example uses `no`, so it will not generate a live page.

Commit changes to `data/prospects.csv`. GitHub Actions runs the generator, commits static pages into `uae/`, `uk/`, and `usa/`, and Hostinger's existing Git integration should deploy those commits. Check both the Action result and the live URL before recording it in your Google Sheet.

Example live path once approved: `https://demo.marketingeraa.com/uae/business-slug/`.

## GitHub Actions permission

If the workflow fails with a `403` when trying to push, in your repository go to **Settings → Actions → General → Workflow permissions**, select **Read and write permissions**, and save. This requires appropriate repo admin access. Do not share credentials.

## Limitations and safeguards

- Keep the GitHub repository private. The included `.htaccess` attempts to block web access to `data/`, `tools/`, and `.github/` on Apache/LiteSpeed. **Test** these URLs after deploying: `/data/prospects.csv` and `/tools/build.py` must return 403/404. If either is readable, stop publishing and use a separate private repository/build host. Do not store confidential or personal prospect data in the CSV. HTML output remains public at the demo URL, even with noindex.
- Create previews only for research-qualified businesses; use rights-cleared assets; do not imply endorsement or operate a fake official site.
- Do not include personal phone numbers or emails without an appropriate legal basis.
- This generator **does not** search Google Maps, verify businesses, write Google Sheets, or independently schedule research. Those need separate authorized integrations.
- The `noindex` robots directive discourages indexing; it does **not** make the site private. For fully private demos, configure access controls on the hosting server.
- Hostinger may redeploy files on every commit; verify the path and monitor the deployment history, and back up your working site first.
