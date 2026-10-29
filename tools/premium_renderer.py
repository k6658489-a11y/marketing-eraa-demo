"""Marketing Eraa premium editorial demo renderer.

The visible design is inspired by the approved ASCOT premium concept.  External
stock photos are illustrative; no client-owned media, quotes, ratings, or
operational claims are invented. Python standard library only.
"""
from __future__ import annotations
from pathlib import Path
import html
import re

TEMPLATE = Path(__file__).with_name('templates') / 'premium_base.html'

# Deliberately distinct palettes, editorial imagery, services, and journeys.
# Photo URLs are generic Unsplash references, NOT the featured business's work.
PROFILES = {
 'tailor': dict(
  label='contemporary tailoring', ink='#142338', ink2='#0d1828', blue='#3865d8', blue2='#2447a4', gold='#c8a270', cream='#f7f4ef', paper='#fefdf9', muted='#68717c', hero3='#243647', overlay='rgba(14,24,39,.94)', position='50% 38%',
  eyebrow='CONTEMPORARY TAILORING · A DIGITAL ATELIER', hero1='Wear your own', hero2='story.',
  description='A more considered expression of personal style. Discover how a distinctive digital atelier could bring beautiful tailoring and effortless enquiries into focus.',
  intro1='For the moments that matter,', intro2='every detail', intro3='deserves its place.',
  introdesc='A beautifully considered online experience where visitors can learn about the craft, explore the possibilities and take their next step with confidence.', sign='Considered. Always.',
  service_title1='Craft, considered.', service_title2='Style, personal.',
  services=['Bespoke tailoring','Occasionwear','Personal fittings'],
  descriptions=['A refined way to present custom garments and personal style.','A space to showcase style for special moments and occasions.','Turn curiosity into a clear request for a private conversation.'],
  service_kicks=['SIGNATURE','OCCASION','DETAIL'],
  statement1='Not just a suit.', statement2='A statement of you.', statementdesc='An editorial first impression, designed around personal expression.',
  craftlabel='The finer things are in the details.', craft1='Every detail.', craft2='Every decision.', craft3='Every you.', craftdesc='Thoughtful visual storytelling and elegant navigation give craftsmanship room to shine while making the next step effortless.',
  features=['Personal expression','Craft made visible','Effortless enquiries'],featuredesc=['Present each service with style and clarity.','Give fabrics, fittings and details space.','Keep the next step visible and simple.'],
  journey1='From first idea',journey2='to final impression.',journeysteps=['Discover','Discuss','Refine'],journeydesc=['Explore the style direction and available services.','A future enquiry experience could begin a personal conversation.','Bring the customer journey together around care and detail.'],
  gallery1='A lookbook',gallery2='of possibility.',gallerycaps=['Classic refinement','The fabric story','Made to express'],
  contact1='Great style starts',contact2='with a conversation.', contactdesc='@@CITY@@ — a proposed location and enquiry section. Final directions, details and contact options would be connected only with the business owner’s approval.',
  action='Enquire about a fitting', herocta='Explore the craft',nav1='The Atelier',nav2='Our Craft',foot='An unofficial editorial concept of a refined tailoring website.',
  photos=['photo-1519085360753-af0119f7cbe7','photo-1598033129183-c4f50c736f10','photo-1551232864-3f0890e580d9','photo-1527719327859-c6ce80353573','photo-1523398002811-999ca8dec234','photo-1503341504253-dff4815485f1','photo-1591047139829-d91aecb6caea','photo-1490114538077-0a7f8cb49891']),
 'barber':dict(
  label='modern grooming',ink='#1e2926',ink2='#101b1b',blue='#b98763',blue2='#9a6948',gold='#d8af84',cream='#f5efe6',paper='#fffdfa',muted='#707776',hero3='#344035',overlay='rgba(16,27,25,.92)',position='54% 38%',
  eyebrow='THE MODERN GROOMING EXPERIENCE',hero1='A fresh look.',hero2='A finer feeling.',
  description='More than a place for a haircut. Imagine an online first impression built around sharp details, confident style and an easy path to a visit.',
  intro1='Confidence can begin',intro2='with one detail',intro3='— the way you feel.',
  introdesc='An inviting digital space to discover grooming services, understand the experience and find the studio with ease.',sign='Sharp. Considered. Personal.',
  service_title1='All about',service_title2='the details.',services=['Signature haircuts','Beard & grooming','Personal styling'],descriptions=['A clear space to introduce haircut options and the studio’s style.','Present grooming services with simple descriptions and beautiful visual context.','An approachable first step for people looking for a new look.'],service_kicks=['CUT','GROOM','STYLE'],
  statement1='Your style.',statement2='Your signature.',statementdesc='A grooming brand presentation with character, craft and clarity.',
  craftlabel='Confidence lives in the finishing touches.',craft1='Cut with intention.',craft2='Made to',craft3='feel personal.',craftdesc='A website can make the atmosphere visible before a first visit: clear services, strong imagery and a welcoming experience.',
  features=['A recognisable look','Services at a glance','Simple visit enquiries'],featuredesc=['Establish a distinctive visual identity.','Help customers see possible services.','Make the next step easy to find.'],
  journey1='A new look',journey2='starts here.',journeysteps=['Explore','Choose','Visit'],journeydesc=['Discover the studio and illustrative grooming categories.','Find the service that fits an individual style.','Use a future approved booking or direction option.'],
  gallery1='The art',gallery2='of the everyday.',gallerycaps=['The atmosphere','The detail','The ritual'],
  contact1='Make the next',contact2='visit effortless.',contactdesc='@@CITY@@ — concept location section. Actual opening hours, appointments and contact details require confirmation by the business.',
  action='Explore booking',herocta='Explore the services',nav1='The Studio',nav2='Our Services',foot='An unofficial concept for a confident modern grooming presence.',
  photos=['photo-1503951914875-452162b0f3f1','photo-1599351431202-1e0f0137899a','photo-1621605815971-fbc98d665033','photo-1517832606294-7ae9b720a186','photo-1599351431202-1e0f0137899a','photo-1503951914875-452162b0f3f1','photo-1621605815971-fbc98d665033','photo-1517832606294-7ae9b720a186']),
 'shoe':dict(
  label='shoe and leather care',ink='#35241d',ink2='#1e1714',blue='#a97248',blue2='#895934',gold='#dfb47e',cream='#f6efe6',paper='#fffcf6',muted='#7f7469',hero3='#3c332b',overlay='rgba(29,22,18,.94)',position='53% 45%',
  eyebrow='SHOE REPAIR · LEATHER CARE · CRAFT',hero1='Good things',hero2='deserve longer.',
  description='Beautifully made possessions have stories worth keeping. Imagine a premium digital workshop where care, repair and craftsmanship come to life.',
  intro1='Because the things we love',intro2='are worth caring for',intro3='a little longer.',
  introdesc='A digital destination for customers to explore possible repair services, discover the approach and enquire about restoring favourite pieces.',sign='Restore. Revive. Rewear.',
  service_title1='Craftsmanship',service_title2='with purpose.',services=['Shoe repairs','Leather care','Key cutting'],descriptions=['Give common shoe-repair work a clean, approachable introduction.','Explain the possibilities for leather items and everyday upkeep.','Show complementary services clearly when confirmed by the owner.'],service_kicks=['REPAIR','CARE','DETAIL'],
  statement1='Worth keeping.',statement2='Worth caring for.',statementdesc='A contemporary expression of practical craft.',
  craftlabel='Care is in the smallest detail.',craft1='A second life.',craft2='Made for',craft3='the everyday.',craftdesc='Visitors should understand the service without guesswork: what may be possible, where to visit and how to start an enquiry.',
  features=['Craft at the centre','Repair categories','Easy enquiries'],featuredesc=['Let the work speak visually.','Organise common customer questions.','Give every visitor a clear next step.'],
  journey1='Thoughtful repair,',journey2='simple steps.',journeysteps=['Explore','Bring it in','Restore'],journeydesc=['Learn about illustrative care and repair services.','Visit the location to discuss a specific item.','Agree final options with the business directly.'],
  gallery1='The beauty',gallery2='of the details.',gallerycaps=['Classic materials','Hands at work','Everyday essentials'],
  contact1='Your favourites',contact2='are worth a visit.',contactdesc='@@CITY@@ — a proposed location and enquiry section. Repair pricing, availability and opening times require confirmation by the business.',
  action='Request repair advice',herocta='Explore the craft',nav1='The Workshop',nav2='Our Services',foot='An unofficial website concept honouring shoe and leather care.',
  photos=['photo-1542291026-7eec264c27ff','photo-1525966222134-fcfa99b8ae77','photo-1533867617858-e7b97e060509','photo-1614252369475-531eba835eb1','photo-1533867617858-e7b97e060509','photo-1525966222134-fcfa99b8ae77','photo-1542291026-7eec264c27ff','photo-1614252369475-531eba835eb1']),
 'alterations':dict(
  label='clothing alterations',ink='#1e2b39',ink2='#101924',blue='#7799b4',blue2='#52748b',gold='#c8ae94',cream='#f2f1ed',paper='#fdfcf8',muted='#687580',hero3='#313c4b',overlay='rgba(16,25,35,.92)',position='54% 38%',
  eyebrow='ALTERATIONS · SEWING · THE PERFECT FIT',hero1='Feel the fit.',hero2='Love the look.',
  description='Your favourite clothes deserve a considered fit. Picture a calm, beautiful digital studio that makes alterations and repair enquiries easy.',
  intro1='Small adjustments.',intro2='A better fit.',intro3='A whole new feeling.',
  introdesc='An elevated online first impression where customers can understand garment alterations, find the studio and take the next step with confidence.',sign='Refine. Refresh. Rewear.',
  service_title1='For the clothes',service_title2='you love.',services=['Clothing alterations','Garment repairs','Fitting enquiries'],descriptions=['Introduce alterations as a clear and approachable service category.','Give thoughtful care and maintenance a visible place.','Guide customers toward discussing their fitting needs.'],service_kicks=['FIT','CARE','DETAIL'],
  statement1='The little changes.',statement2='The big difference.',statementdesc='Beautifully presented clothing care, made accessible.',
  craftlabel='A thoughtful finish changes everything.',craft1='Rewear with care.',craft2='Made to',craft3='fit your life.',craftdesc='A useful website is equal parts beautiful and practical: explain possibilities, show location information and keep it effortless to enquire.',
  features=['Approachable service','Clear process','Visit information'],featuredesc=['Show what may be possible.','Explain the journey without complexity.','Make finding the studio straightforward.'],
  journey1='From wardrobe',journey2='to a better fit.',journeysteps=['Explore','Discuss','Refine'],journeydesc=['Find illustrative alteration categories.','Consider the garment and required adjustments.','Get a fitting plan directly from the business.'],
  gallery1='A world',gallery2='of small details.',gallerycaps=['Material & form','Everyday care','Thoughtful style'],
  contact1='A better fit',contact2='starts here.',contactdesc='@@CITY@@ — a proposed location and contact section. Actual prices, appointments and business details require the owner’s confirmation.',
  action='Explore fittings',herocta='Explore services',nav1='The Studio',nav2='Alterations',foot='An unofficial premium concept for local alterations and fitting services.',
  photos=['photo-1598032895397-b9472444bf93','photo-1605000797499-95a51c5269ae','photo-1558769132-cb1aea458c5e','photo-1592878904946-b3cd8ae243d0','photo-1605000797499-95a51c5269ae','photo-1598032895397-b9472444bf93','photo-1558769132-cb1aea458c5e','photo-1592878904946-b3cd8ae243d0']),
}
# Other types use a polished, neutral professional design instead of plain artwork.
PROFILES['salon']={**PROFILES['barber'], 'label':'beauty and wellbeing', 'eyebrow':'A MODERN BEAUTY EXPERIENCE', 'hero1':'Make room', 'hero2':'for yourself.', 'description':'An inviting beauty destination deserves an equally inviting digital experience.', 'service_title1':'Your beauty,','service_title2':'your moment.', 'services':['Hair styling','Beauty care','Appointments'], 'action':'Explore appointments', 'herocta':'Explore services', 'foot':'An unofficial premium concept for a beauty studio.'}
PROFILES['cleaning']={**PROFILES['alterations'], 'label':'professional cleaning', 'eyebrow':'CLEANING SERVICES · A FRESH START', 'hero1':'A better space.', 'hero2':'A brighter day.', 'description':'A clean, welcoming digital experience for customers exploring home and workplace cleaning options.', 'services':['Home cleaning','Office cleaning','Quote enquiries'], 'action':'Request a quote', 'herocta':'See services', 'foot':'An unofficial premium website concept for local cleaning services.'}
PROFILES['general']={**PROFILES['alterations'], 'label':'local business services', 'eyebrow':'A MORE BEAUTIFUL LOCAL PRESENCE', 'hero1':'A better first', 'hero2':'impression.', 'services':['What we do','How it works','Get in touch'], 'action':'Explore an enquiry', 'foot':'An unofficial premium concept for a local business.'}

def pick_theme(industry: str) -> str:
 s=(industry or '').lower()
 if any(x in s for x in ('shoe','leather','key cutting','cobbler')):return 'shoe'
 if any(x in s for x in ('alteration','sewing','garment repair')):return 'alterations'
 if any(x in s for x in ('tailor','bespoke','suit')):return 'tailor'
 if any(x in s for x in ('barber','gent','grooming')):return 'barber'
 if any(x in s for x in ('beauty','salon','saloon','spa')):return 'salon'
 if any(x in s for x in ('cleaning','wash','janitorial')):return 'cleaning'
 return 'general'

def render_premium(record:dict[str,str],version:str) -> str:
 """All business-provided values are escaped; no contact collection is introduced."""
 key=f"{record['country']}/{record['slug']}"
 theme=pick_theme(record.get('industry',''))
 p=PROFILES[theme]
 name=record['business_name'].strip()
 city=record['city'].strip()
 industry=record.get('industry','').strip()
 # Source-derived categories appear ONLY in a clearly labelled illustrative block.
 incoming=[s.strip() for s in re.split(r'[;|]',record.get('services','')) if s.strip()]
 if len(incoming)>=2 and all(len(s)<=46 for s in incoming[:3]):
  services=(incoming+list(p['services']))[:3]
 else: services=list(p['services'])
 brand_words=[x for x in re.findall(r'\w+',name) if x]
 mark=''.join(x[0] for x in brand_words[:2]).upper() or 'ME'
 loc_short=city.split(',')[0].strip()[:42]
 data={
  'KEY':key,'VERSION':version,'NAME':name,'CITY':city,'MARK':mark,'LOCATION_LABEL':loc_short.upper()+' · CONCEPT',
  'INDUSTRY_LABEL':p['label'],'NAV_1':p['nav1'],'NAV_2':p['nav2'],'ACTION':p['action'],
  'EYEBROW':p['eyebrow'],'HERO_1':p['hero1'],'HERO_2':p['hero2'],'HERO_DESC':p['description'],
  'HERO_CTA':p['herocta'],'HERO_TAG':theme.upper()+' / PREMIUM DESIGN CONCEPT',
  'INTRO_EYEBROW':'THE '+name.upper()+' EXPERIENCE / CONCEPT',
  'INTRO_1':p['intro1'],'INTRO_2':p['intro2'],'INTRO_3':p['intro3'],
  'INTRO_DESC':p['introdesc'],'INTRO_SIGN':p['sign'],
  'SERVICE_EYEBROW':'01 / EXPLORE THE POSSIBILITIES',
  'SERVICES_TITLE_1':p['service_title1'],'SERVICES_TITLE_2':p['service_title2'],
  'STATEMENT_EYEBROW':'DESIGNED FOR A BETTER FIRST IMPRESSION',
  'STATEMENT_1':p['statement1'],'STATEMENT_2':p['statement2'],
  'STATEMENT_DESC':p['statementdesc'],'STATEMENT_SIGN':name+' / '+loc_short,
  'CRAFT_IMAGE_LABEL':p['craftlabel'],'CRAFT_1':p['craft1'],'CRAFT_2':p['craft2'],'CRAFT_3':p['craft3'],
  'CRAFT_DESC':p['craftdesc'],'JOURNEY_1':p['journey1'],'JOURNEY_2':p['journey2'],
  'GALLERY_1':p['gallery1'],'GALLERY_2':p['gallery2'],
  'CONTACT_EYEBROW':'A MORE CONNECTED LOCAL EXPERIENCE / CONCEPT',
  'CONTACT_1':p['contact1'],'CONTACT_2':p['contact2'],
  'CONTACT_DESC':p['contactdesc'].replace('@@CITY@@',city), 'FOOT_DESC':p['foot'],
  'COLOR_INK':p['ink'],'COLOR_INK2':p['ink2'],'COLOR_BLUE':p['blue'],'COLOR_BLUE2':p['blue2'],
  'COLOR_GOLD':p['gold'],'COLOR_CREAM':p['cream'],'COLOR_PAPER':p['paper'],'COLOR_MUTED':p['muted'],
  'COLOR_HERO3':p['hero3'],'COLOR_HERO_OVERLAY':p['overlay'],'HERO_POSITION':p['position'],
  'PILL_1':services[0],'PILL_2':services[1],'PILL_3':loc_short,
 }
 for i in range(1,4):
  data[f'SERVICE_{i}']=services[i-1]
  data[f'SERVICE_DESC_{i}']=p['descriptions'][i-1]
  data[f'SERVICE_KICK_{i}']=p['service_kicks'][i-1]
  data[f'FEATURE_{i}']=p['features'][i-1]
  data[f'FEATURE_DESC_{i}']=p['featuredesc'][i-1]
  data[f'JOURNEY_STEP_{i}']=p['journeysteps'][i-1]
  data[f'JOURNEY_DESC_{i}']=p['journeydesc'][i-1]
  data[f'GALLERY_CAP_{i}']=p['gallerycaps'][i-1]
 for i,photo in enumerate(p['photos']):
  # Public stock imagery for illustration only. Production should use owner-approved assets.
  data[f'PHOTO_{i}']='https://images.unsplash.com/'+photo+'?auto=format&fit=crop&w='+('1700' if i==0 else '1000')+'&q=82'
 output=TEMPLATE.read_text(encoding='utf8')
 # Set business-specific CSS selectors without exposing unescaped string in CSS.
 for token,value in data.items():output=output.replace('@@'+token+'@@',html.escape(str(value),quote=True))
 # Html escaping of fixed colors is harmless; HTML escaping of CSS rgba strings is harmless.
 leftover=re.findall(r'@@[A-Z][A-Z0-9_]*@@',output)
 if leftover:raise ValueError('Template tokens missing: '+', '.join(sorted(set(leftover))))
 # Required by existing GitHub cleanup and Apps Script verification.
 output=output.replace('<body ',f'<!-- ME-DEMO GENERATED key={key} version={version} -->\n<body ',1)
 return output
