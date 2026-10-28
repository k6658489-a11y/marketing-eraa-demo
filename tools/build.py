import csv, html, pathlib, re
ROOT = pathlib.Path(__file__).resolve().parents[1]
CSV = ROOT/'data'/'prospects.csv'
THEMES = {
 'cleaning':('#0e7490','#e0f2fe','Clean spaces, confident first impressions','clean'),
 'plumbing':('#1d4ed8','#dbeafe','Trusted service, straightforward solutions','plumb'),
 'landscaping':('#15803d','#dcfce7','Outdoor spaces made to shine','land'),
 'beauty':('#9d174d','#fce7f3','A beautiful experience begins here','beauty'),
 'automotive':('#b45309','#fef3c7','Care for every detail','auto'),
 'consulting':('#4f46e5','#e0e7ff','Expertise that moves businesses forward','consult'),
 'general':('#334155','#e2e8f0','Professional service, thoughtfully presented','general'),
}
ALLOWED_COUNTRIES={'uae','uk','usa'}
def esc(v): return html.escape((v or '').strip(),quote=True)
def slug(v): return re.sub(r'[^a-z0-9-]+','-',v.lower().strip()).strip('-')[:70]
def main():
 rows=list(csv.DictReader(CSV.open(encoding='utf-8-sig',newline='')))
 written=[]
 for i,row in enumerate(rows,2):
  if (row.get('approved_for_demo') or '').strip().lower() != 'yes': continue
  country=(row.get('country') or '').strip().lower(); name=(row.get('business_name') or '').strip()
  if country not in ALLOWED_COUNTRIES or not name: raise ValueError(f'Row {i}: invalid country or missing business_name')
  key=slug(row.get('slug') or name)
  if not key or key in {'test-business','.','..'}: raise ValueError(f'Row {i}: invalid or reserved slug')
  out=ROOT/country/key/'index.html'
  if out.exists(): raise ValueError(f'Row {i}: duplicate path {country}/{key}')
  industry=(row.get('industry') or 'general').lower().strip(); accent,light,headline,_=THEMES.get(industry, THEMES['general'])
  city=esc(row.get('city')); company=esc(name); sector=esc(industry.title() if industry else 'Business')
  services=[esc(x) for x in (row.get('services') or '').split('|') if x.strip()][:6]
  if not services: services=['Professional service','Customer-focused approach','Contact for details']
  details=''.join(f'<article class="service"><span>0{n}</span><h3>{item}</h3><p>Ask the business for current availability and details.</p></article>' for n,item in enumerate(services,1))
  email=esc(row.get('business_email')); phone=esc(row.get('business_phone'))
  email_link=f'<a href="mailto:{email}">Email business</a>' if email else ''
  phone_link=f'<a href="tel:{esc(re.sub(r"[^0-9+]", "", row.get("business_phone") or ""))}">Call business</a>' if phone else ''
  cta=email_link or phone_link or '<span>Contact details to be confirmed</span>'
  style_variant=int(sum(map(ord, key))%3)
  klass=['layout-a','layout-b','layout-c'][style_variant]
  doc=f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex,nofollow,noarchive"><title>{company} — Unofficial Website Concept | Marketing Eraa</title><style>
  :root{{--accent:{accent};--soft:{light}}}*{{box-sizing:border-box}}body{{margin:0;font:16px/1.6 system-ui,-apple-system,Segoe UI,sans-serif;background:#f8fafc;color:#152238}}a{{color:inherit}}.notice{{background:#0f172a;color:#fff;text-align:center;padding:11px 18px;font-size:12px}}.wrap{{max-width:1120px;margin:auto;padding:0 26px}}header{{display:flex;justify-content:space-between;align-items:center;gap:20px;padding:26px 0}}.brand{{font-weight:800;font-size:22px}}header a{{text-decoration:none;color:var(--accent);font-weight:700}}.hero{{background:linear-gradient(125deg,var(--soft),#fff);border-radius:32px;padding:80px 7%;min-height:420px;display:flex;flex-direction:column;justify-content:center}}.layout-b .hero{{text-align:center;align-items:center;border-radius:8px}}.layout-c .hero{{background:linear-gradient(140deg,#111827,#273449);color:white}}.eyebrow{{color:var(--accent);font-weight:700;text-transform:uppercase;letter-spacing:.15em;font-size:12px}}.layout-c .eyebrow{{color:#a5f3fc}}h1{{font-size:clamp(34px,6vw,70px);line-height:1.08;letter-spacing:-.05em;margin:12px 0 22px;max-width:820px}}.intro{{font-size:18px;max-width:650px;opacity:.83}}.pill{{display:inline-block;background:var(--accent);color:#fff;border-radius:999px;padding:12px 22px;text-decoration:none;font-weight:700;margin-top:24px}}section{{padding:60px 0}}h2{{font-size:34px;letter-spacing:-.035em}}.cards{{display:grid;grid-template-columns:repeat(3,1fr);gap:18px}}.service{{background:white;border:1px solid #e5e7eb;border-radius:20px;padding:24px}}.service span{{color:var(--accent);font-weight:700}}.service h3{{font-size:20px}}.contact{{background:var(--soft);border-radius:24px;padding:36px}}.contact a{{margin-right:18px;color:var(--accent);font-weight:700}}footer{{padding:26px 0;border-top:1px solid #e2e8f0;color:#64748b;font-size:13px}}@media(max-width:680px){{header{{align-items:flex-start}}.hero{{padding:64px 28px}}.cards{{grid-template-columns:1fr}}}}
  </style></head><body class="{klass}"><div class="notice">UNOFFICIAL WEBSITE DESIGN CONCEPT • Created by Marketing Eraa • Not affiliated with or approved by the featured business</div><div class="wrap"><header><div class="brand">{company}</div><a href="#contact">Get in touch</a></header><main><div class="hero"><div class="eyebrow">{sector} {(' • '+city) if city else ''}</div><h1>{esc(row.get('headline')) or esc(headline)}</h1><p class="intro">A preview concept for {company}. Text and service information must be confirmed with the business before publication as an official site.</p><a class="pill" href="#services">Explore services</a></div><section id="services"><div class="eyebrow">Our services</div><h2>How we can help</h2><div class="cards">{details}</div></section><section id="contact"><div class="contact"><div class="eyebrow">Connect</div><h2>Contact {company}</h2><p>Information displayed here is based on independent research and may require confirmation.</p>{cta}</div></section></main><footer>Unofficial demonstration by Marketing Eraa. Not a business-operated website. No enquiries are collected on this page.</footer></div></body></html>'''
  out.parent.mkdir(parents=True,exist_ok=True); out.write_text(doc,encoding='utf-8')
  written.append(str(out.relative_to(ROOT)))
 print('Generated',len(written),'demo pages')
 for p in written:print(p)
if __name__=='__main__': main()
