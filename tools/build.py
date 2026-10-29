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
    # Same source fingerprint as Google Apps Script; preserve verified URLs.
    try:
        from tools.premium_renderer import render_premium
    except ModuleNotFoundError:
        from premium_renderer import render_premium
    return render_premium(r, fingerprint(r))

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
