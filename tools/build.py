#!/usr/bin/env python3
"""Build clearly marked, responsive unofficial website concepts from approved CSV rows.
No private contact data is used. This script has no external dependencies.
"""
from __future__ import annotations
import csv
import hashlib
import html
import pathlib
import re
import sys
from dataclasses import dataclass

ROOT = pathlib.Path(__file__).resolve().parents[1]
CSV_FILE = ROOT / 'data' / 'prospects.csv'
VALID_COUNTRIES = {'uae', 'uk', 'usa'}
SLUG = re.compile(r'^[a-z0-9]+(?:-[a-z0-9]+)*$')
MARKER = 'ME-DEMO GENERATED'

@dataclass(frozen=True)
class Theme:
    key: str
    label: str
    ink: str
    bg: str
    accent: str
    glow: str
    hero: str
    eyebrow: str
    signature: str
    services: tuple[str, str, str]

THEMES = {
    'tailor': Theme('tailor','Bespoke tailoring','#1B2421','#F2EFE9','#9D7658','#D6BD9D','Made to fit. Designed to belong.','THE ART OF THE PERFECT FIT','Every detail tells a story.',('Tailoring','Alterations','Private Fittings')),
    'barber': Theme('barber','Barber & grooming','#20201E','#F5F1E9','#C7784F','#F1C4A3','Good style begins with the details.','A FRESH PERSPECTIVE ON GROOMING','Your next look starts here.',('Haircuts','Beard & Grooming','Styling')),
    'salon': Theme('salon','Beauty & styling','#342C37','#FBF3F3','#B36B91','#EAD3E1','A little time, beautifully yours.','A MOMENT FOR YOURSELF','A thoughtful space for self-care.',('Hair & Styling','Beauty Services','Appointments')),
    'shoe': Theme('shoe','Shoe & leather care','#2F251D','#F6F0E5','#A97049','#DBBD92','Quality deserves a second chapter.','CARE FOR WHAT YOU LOVE','Attention to every stitch and sole.',('Shoe Repairs','Leather Care','Key Services')),
    'alterations': Theme('alterations','Clothing alterations','#24313B','#F3F3EF','#678D9B','#D4E4E6','The right fit changes everything.','TAILORED TO YOUR EVERYDAY','Refresh, refine, rewear.',('Clothing Alterations','Repairs','Fitting Enquiries')),
    'cleaning': Theme('cleaning','Cleaning services','#163641','#EAF4F5','#398A91','#C4E2E2','A fresh space feels different.','A CLEARER FIRST IMPRESSION','The confidence of a clean space.',('Home Cleaning','Workplace Cleaning','Quote Enquiries')),
    'general': Theme('general','Local services','#23313C','#F5F2EA','#497F92','#DBE6E9','Your neighbourhood. Your next discovery.','MADE FOR LOCAL DISCOVERY','A better way to show what you do.',('Services','What to Expect','Get in Touch')),
}

def esc(value: object) -> str:
    return html.escape(str(value or '').strip(), quote=True)

def theme_for(industry: str) -> Theme:
    x = industry.casefold()
    if any(a in x for a in ('shoe', 'leather', 'key cutting', 'cobbler')): return THEMES['shoe']
    if any(a in x for a in ('alteration', 'garment repair', 'sewing')): return THEMES['alterations']
    if any(a in x for a in ('tailor', 'bespoke', 'suit')): return THEMES['tailor']
    if any(a in x for a in ('barber', 'gent', 'grooming')): return THEMES['barber']
    if any(a in x for a in ('salon', 'saloon', 'beauty', 'hair')): return THEMES['salon']
    if any(a in x for a in ('cleaning', 'wash')): return THEMES['cleaning']
    return THEMES['general']

def visual_art(theme: Theme) -> str:
    """Original CSS/SVG art: no borrowed business photography or invented testimonials."""
    name = theme.key
    primitives = {
      'tailor': '''<path d="M177 102l54-31 52 32 26 63-38 21-8-37v190H188V150l-8 37-38-21z"/><path d="M232 71l22 57-22 20-22-20z"/><path d="M232 148v192"/><path d="M198 227h19"/>''',
      'barber': '''<path d="M196 104c-17 24-10 55 14 85l91 106c22 27 48 10 31-12L246 164c-22-30-24-58-14-78"/><path d="M302 106c-15 12-29 34-38 60"/><path d="M168 101c28 20 49 24 66 15"/><circle cx="328" cy="307" r="22"/><circle cx="187" cy="310" r="22"/>''',
      'salon': '''<path d="M252 82c-65 0-101 57-93 111 9 58 48 104 93 104s84-46 93-104c8-54-28-111-93-111z"/><path d="M208 168c12-20 30-29 44-29s32 9 44 29"/><path d="M205 226c28 27 66 27 94 0"/><path d="M183 147c-36 78-18 153 25 187M321 147c36 78 18 153-25 187"/>''',
      'shoe': '''<path d="M120 271c31-6 52-13 74-43 15-19 20-43 27-82 16 28 33 52 59 68 25 16 48 26 84 37 18 5 20 37-2 45H147c-24 0-36-8-27-25z"/><path d="M129 291h230"/><path d="M220 204l44 22M214 220l42 21M204 238l35 16"/>''',
      'alterations': '''<path d="M165 117l45-30 30 33 30-33 45 30 30 69-44 19-10-24v156H189V181l-10 24-44-19z"/><path d="M209 88l31 61 30-61M240 149v189"/><path d="M156 270h64M252 270h64"/>''',
      'cleaning': '''<path d="M250 89l-14 66-64 17 64 15 14 67 15-67 64-15-64-17z"/><path d="M162 229l-8 32-33 10 33 8 8 33 9-33 32-8-32-10z"/><path d="M323 240l-9 38-38 10 38 9 9 39 10-39 38-9-38-10z"/>''',
      'general': '''<path d="M155 165l95-70 95 70v148H155z"/><path d="M193 314v-94h114v94"/><path d="M250 95v-35M166 100l-23-23M335 100l24-23"/>''',
    }
    path = primitives[name]
    return f'''<svg viewBox="0 0 500 420" role="img" aria-label="Original illustrative artwork for {esc(theme.label)}"><g fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="3.2">{path}</g><circle cx="250" cy="210" r="174" fill="none" stroke="currentColor" opacity=".16" stroke-width="1"/><circle cx="250" cy="210" r="194" fill="none" stroke="currentColor" opacity=".1" stroke-width="1"/></svg>'''

def read_records(csv_path: pathlib.Path) -> list[dict[str, str]]:
    required = {'country','business_name','slug','industry','city','services','approved_for_demo'}
    with csv_path.open('r', encoding='utf-8-sig', newline='') as stream:
        reader = csv.DictReader(stream)
        if not reader.fieldnames or not required.issubset(reader.fieldnames):
            raise ValueError('CSV must contain: ' + ', '.join(sorted(required)))
        seen = set()
        result = []
        for line, entry in enumerate(reader, start=2):
            if entry.get('approved_for_demo','').strip().casefold() != 'yes':
                continue
            country = entry.get('country','').strip().lower()
            slug = entry.get('slug','').strip().lower()
            name = entry.get('business_name','').strip()
            city = entry.get('city','').strip()
            if country not in VALID_COUNTRIES or not SLUG.fullmatch(slug):
                raise ValueError(f'Row {line}: invalid country/slug')
            if not name or not city or len(name)>120 or len(slug)>80:
                raise ValueError(f'Row {line}: missing/overlong business name, slug or city')
            if (country,slug) in seen:
                raise ValueError(f'Row {line}: duplicate {country}/{slug}')
            seen.add((country,slug))
            result.append({**entry, 'country':country,'slug':slug, 'business_name':name,'city':city})
    return result

def fingerprint(r: dict[str, str]) -> str:
    values = [r.get(k, '').strip() for k in ('country', 'business_name', 'slug', 'industry', 'city', 'services', 'headline')]
    return hashlib.sha256('\x1f'.join(values).encode('utf-8')).hexdigest()[:12]

def render_page(r: dict[str, str]) -> str:
    version = fingerprint(r)
    theme = theme_for(r.get('industry',''))
    name, city = esc(r['business_name']), esc(r['city'])
    key = f"{r['country']}/{r['slug']}"
    idea = esc(r.get('headline') or theme.hero)
    logo = ''.join(ch for ch in name if ch.isalnum() or ch.isspace()).split()[:3]
    mark = ''.join(chunk[0].upper() for chunk in logo)[:3] or 'ME'
    services = [x.strip() for x in re.split(r';|\|', r.get('services','')) if x.strip()]
    # Only illustrative section topics; avoid treating scraped free-text notes as verified service offerings.
    service_labels = list(theme.services)
    if len(services) >= 2 and all(len(x) < 46 for x in services[:3]):
        service_labels = services[:3]
    while len(service_labels) < 3:
        service_labels.append(theme.services[len(service_labels)])
    cards = ''
    desc = ['An example of how this service could be explained to local visitors.',
            'A clear way to present the work, process and common questions.',
            'An inviting place for customers to learn more before reaching out.']
    for idx, label in enumerate(service_labels[:3]):
        cards += f'''<article class="service-card"><span class="service-no">0{idx+1} / 03</span><span class="service-icon" aria-hidden="true">{'✦' if idx==0 else ('◎' if idx==1 else '↗')}</span><h3>{esc(label)}</h3><p>{desc[idx]}</p></article>'''
    illustration = visual_art(theme)
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex,nofollow,noarchive"><meta name="me-demo-version" content="{version}"><meta name="referrer" content="strict-origin-when-cross-origin">
<title>{name} — Unofficial website concept by Marketing Eraa</title>
<meta name="description" content="Unofficial, illustrative homepage concept for {name}. Not the company's official website.">
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@400;500;600;700;800&display=swap');
:root{{--ink:{theme.ink};--bg:{theme.bg};--accent:{theme.accent};--glow:{theme.glow};--white:#fffdf9}}
*{{box-sizing:border-box}}html{{scroll-behavior:smooth}}body{{margin:0;color:var(--ink);background:var(--bg);font-family:'DM Sans',system-ui,sans-serif}}a{{color:inherit;text-decoration:none}}.container{{width:min(1160px,calc(100% - 64px));margin:auto}}
.preview{{display:block;background:#18252b;color:#fff;letter-spacing:.04em;font-size:11px;font-weight:700;text-align:center;padding:13px 18px;line-height:1.5}}
.preview a{{text-decoration:underline;text-underline-offset:3px}}header{{background:var(--bg);border-bottom:1px solid #24343b18}}.nav{{min-height:91px;display:flex;justify-content:space-between;align-items:center;gap:16px}}.brand{{display:flex;align-items:center;gap:14px}}.brand-mark{{display:grid;place-items:center;background:var(--ink);color:#fff;font:800 19px 'Manrope',system-ui,sans-serif;height:48px;width:48px;border-radius:14px}}.brand strong{{display:block;font:800 16px 'Manrope',system-ui,sans-serif}}.brand small{{font-size:10px;text-transform:uppercase;letter-spacing:.15em;opacity:.6}}.navlinks{{display:flex;align-items:center;gap:30px;font-size:13px;font-weight:700}}.navlinks a:hover{{color:var(--accent)}}.navlinks .navcta{{background:var(--ink);color:white;border-radius:100px;padding:15px 20px}}.navlinks .navcta:hover{{color:white;background:var(--accent)}}
.hero{{position:relative;overflow:hidden;padding:90px 0 104px}}.hero-grid{{display:grid;grid-template-columns:1.02fr 1fr;gap:65px;align-items:center}}.eyebrow{{text-transform:uppercase;letter-spacing:.2em;font-size:11px;font-weight:800;color:var(--accent);display:inline-flex;align-items:center;gap:12px}}.eyebrow:before{{content:'';width:29px;height:1px;background:var(--accent)}}h1,h2,h3,p{{margin-top:0}}h1,h2{{font-family:Manrope,system-ui,sans-serif;letter-spacing:-.065em}}h1{{font-size:clamp(43px,5.1vw,75px);line-height:1.06;max-width:610px;margin:25px 0}}.hero p{{max-width:470px;color:var(--ink);opacity:.65;font-size:17px;line-height:1.75}}.actions{{display:flex;flex-wrap:wrap;gap:12px;margin-top:36px}}.button{{display:inline-flex;align-items:center;justify-content:center;min-height:53px;padding:0 23px;border-radius:100px;font-size:13px;font-weight:800;gap:14px}}.primary{{background:var(--ink);color:white}}.secondary{{border:1px solid #28383a44}}.primary:hover{{background:var(--accent)}}.secondary:hover{{background:#ffffff70}}.hero-art{{height:490px;position:relative;display:flex;align-items:center;justify-content:center;overflow:hidden;border-radius:10px 140px 10px 10px;background:radial-gradient(circle at 20% 20%,var(--glow),transparent 60%),linear-gradient(135deg,var(--ink),var(--accent));color:#fff9ed;box-shadow:20px 25px 0 -12px #00000010}}.hero-art svg{{width:80%;filter:drop-shadow(0 26px 10px #0002)}}.art-caption{{position:absolute;right:24px;bottom:23px;font-size:10px;font-weight:800;letter-spacing:.2em;text-transform:uppercase;opacity:.75}}.floating{{position:absolute;left:calc(50% - 10px);bottom:72px;background:var(--white);padding:19px 24px;box-shadow:0 12px 60px #0002;max-width:280px;border-left:4px solid var(--accent);font-family:Manrope;font-size:13px;font-weight:800}}
.section{{padding:95px 0}}.section-header{{display:flex;align-items:end;justify-content:space-between;gap:22px;margin-bottom:37px}}h2{{font-size:clamp(34px,4vw,52px);line-height:1.12;margin:12px 0 0;max-width:650px}}.section-sub{{max-width:340px;font-size:14px;line-height:1.75;opacity:.62}}.services{{background:#fffdfa}}.service-grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:15px}}.service-card{{min-height:294px;background:var(--bg);padding:30px;display:flex;flex-direction:column;border:1px solid #3332;transition:transform .2s}}.service-card:hover{{transform:translateY(-5px)}}.service-no{{font-size:10px;font-weight:800;opacity:.5;letter-spacing:.13em}}.service-icon{{font-size:37px;color:var(--accent);margin:22px 0 17px}}h3{{font:800 22px 'Manrope',system-ui,sans-serif;letter-spacing:-.04em;margin-bottom:12px}}.service-card p{{font-size:13px;line-height:1.7;opacity:.65}}.story-grid{{display:grid;grid-template-columns:1fr 1.05fr;gap:80px;align-items:center}}.story-visual{{min-height:385px;background:linear-gradient(145deg,var(--glow),#fff9f1);padding:40px;display:grid;place-items:center}}.story-visual blockquote{{margin:0;font:600 clamp(30px,3.5vw,48px)/1.28 'Manrope',system-ui,sans-serif;letter-spacing:-.06em}}.story-copy p{{font-size:15px;line-height:1.9;opacity:.69}}.step{{display:flex;gap:16px;border-top:1px solid #2232;padding:17px 0;font-size:14px}}.step b{{color:var(--accent)}}.visit{{background:var(--ink);color:white;padding:80px 0}}.visit-flex{{display:flex;justify-content:space-between;align-items:center;gap:40px}}.visit p{{opacity:.68;max-width:600px;line-height:1.8}}.visit .button{{background:white;color:var(--ink)}}.visit .eyebrow{{color:var(--glow)}}.visit .eyebrow:before{{background:var(--glow)}}footer{{background:#152025;color:#fff; padding:28px 0}}.footer-inner{{display:flex;justify-content:space-between;gap:20px;align-items:center;font-size:11px;opacity:.85}}.footer-inner a{{text-decoration:underline}}
@media(max-width:900px){{.hero-grid,.story-grid{{grid-template-columns:1fr;gap:30px}}.hero{{padding:50px 0 70px}}.hero-art{{height:360px;border-radius:8px 100px 8px 8px}}.floating{{left:auto;right:35px;bottom:35px}}.navlinks a:not(.navcta){{display:none}}.service-grid{{grid-template-columns:1fr}}.service-card{{min-height:220px}}.section-header,.visit-flex{{display:block}}.visit .button{{margin-top:20px}}}}
@media(max-width:520px){{.container{{width:calc(100% - 36px)}}.nav{{min-height:76px}}.brand small{{display:none}}.brand strong{{font-size:13px}}.brand-mark{{width:39px;height:39px;font-size:14px}}.navlinks .navcta{{padding:12px 14px;font-size:11px}}h1{{font-size:43px}}.hero-art{{height:330px}}.floating{{font-size:11px;max-width:205px;bottom:15px;right:15px}}.section{{padding:65px 0}}.footer-inner{{display:block;line-height:2}}}}
@media(prefers-reduced-motion:reduce){{html{{scroll-behavior:auto}}.service-card{{transition:none}}}}
</style></head><body data-demo-key="{esc(key)}" data-demo-version="{version}">
<!-- {MARKER} key={esc(key)} version={version} -->
<a class="preview" href="#about">UNOFFICIAL CONCEPT PREVIEW — Created by Marketing Eraa, not affiliated with {name}. Business details and visuals must be approved before launch.</a>
<header><div class="container nav"><div class="brand"><span class="brand-mark">{esc(mark)}</span><span><strong>{name}</strong><small>Website concept preview</small></span></div><nav class="navlinks" aria-label="Main navigation"><a href="#services">Services</a><a href="#about">About concept</a><a href="#visit">Visit concept</a><a class="navcta" href="#visit">Explore next step ↗</a></nav></div></header>
<main><section class="hero"><div class="container hero-grid"><div><div class="eyebrow">{esc(theme.eyebrow)}</div><h1>{idea}</h1><p>An illustrative new online experience for <b>{name}</b> in {city}. Imagine your services, location and customer enquiries—all presented in one polished place.</p><div class="actions"><a class="button primary" href="#services">Explore services <span aria-hidden="true">↗</span></a><a class="button secondary" href="#about">See the concept</a></div></div><div class="hero-art">{illustration}<div class="art-caption">{esc(theme.label)} / concept illustration</div></div></div><div class="floating">{esc(theme.signature)}</div></section>
<section class="section services" id="services"><div class="container"><div class="section-header"><div><div class="eyebrow">WHAT A WEBSITE COULD SHOW</div><h2>Simple to discover.<br>Easy to explore.</h2></div><p class="section-sub">Illustrative service categories for layout demonstration only. Final wording requires the business owner's confirmation.</p></div><div class="service-grid">{cards}</div></div></section>
<section class="section" id="about"><div class="container story-grid"><div class="story-visual"><blockquote>Made for the details people remember<span style="color:var(--accent)">.</span></blockquote></div><div class="story-copy"><div class="eyebrow">DESIGNED FOR CLARITY</div><h2>A better first impression starts online.</h2><p>This sample homepage demonstrates how a local business can introduce its work, show what makes it distinct, and give visitors a clear next step—all from a phone or desktop.</p><div class="step"><b>01</b> A clear introduction to the business</div><div class="step"><b>02</b> A focused service overview</div><div class="step"><b>03</b> Helpful directions and enquiry options</div></div></div></section>
<section class="visit" id="visit"><div class="container visit-flex"><div><div class="eyebrow">A MORE CONNECTED LOCAL PRESENCE</div><h2>Every enquiry<br>starts somewhere.</h2><p>Location concept: {city}. This is a presentation mockup, not the business's official website. Bookings, enquiry collection and business contact links are intentionally inactive until approved by the owner.</p></div><a class="button" href="https://marketingeraa.com/" rel="noopener noreferrer">Built as a concept by Marketing Eraa ↗</a></div></section></main>
<footer><div class="container footer-inner"><span>© 2026 Marketing Eraa — Unofficial concept for {name}</span><span>No affiliation implied • No forms collect personal information • <a href="https://marketingeraa.com/">marketingeraa.com</a></span></div></footer>
</body></html>'''

def build(root: pathlib.Path, csv_path: pathlib.Path) -> list[pathlib.Path]:
    records = read_records(csv_path)
    paths = []
    active_keys = {(r['country'], r['slug']) for r in records}
    # Only retire pages originally produced by THIS generator. Never delete manual pages.
    for country in VALID_COUNTRIES:
        folder = root / country
        if not folder.is_dir():
            continue
        for child in folder.iterdir():
            if not child.is_dir() or not SLUG.fullmatch(child.name):
                continue
            candidate = child / 'index.html'
            if (country, child.name) not in active_keys and candidate.is_file():
                sample = candidate.read_text(encoding='utf-8')
                if f'<!-- {MARKER} key={country}/{child.name} ' in sample:
                    candidate.unlink()
                    if not list(child.iterdir()):
                        child.rmdir()
    for r in records:
        location = root / r['country'] / r['slug'] / 'index.html'
        location.parent.mkdir(parents=True, exist_ok=True)
        output = render_page(r)
        if not location.exists() or location.read_text(encoding='utf-8') != output:
            location.write_text(output, encoding='utf-8')
        paths.append(location)
    return paths

if __name__ == '__main__':
    try:
        generated = build(ROOT, CSV_FILE)
    except Exception as err:
        print(f'BUILD FAILED: {err}', file=sys.stderr)
        raise SystemExit(1)
    print(f'Prepared {len(generated)} approved demo page(s)')
    for path in generated:
        print(' -', path.relative_to(ROOT).as_posix())
