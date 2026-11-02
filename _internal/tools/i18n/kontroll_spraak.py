#!/usr/bin/env python3
"""Kontroll av språksidene: alle språk x alle sider (runde rSpraak). Uavhengig av byggeskriptet: tekstene leses ved å
kjøre js/i18n.js i Node (som validate.js), HTML-en med html.parser.

    python -X utf8 _internal/tools/i18n/kontroll_spraak.py [--rot <mappe>] [--vis-rest] [--lenker <fil med URL-er>]

Sjekker: lang og dir, title og beskrivelse, canonical, hreflang-par (begge veier), data-i18n = i18n.js, rå nøkler,
engelsk rest (tekst og attributter lik den engelske siden), interne lenker og ankre, butikklenker per land, strukturerte
data, forbudte ord, sitemap, llms.txt, videresendingene og hostingfilene. Exit 1 ved feil.
"""
import html
import json
import pathlib
import re
import subprocess
import sys
import xml.etree.ElementTree as ET
from html.parser import HTMLParser

args = sys.argv[1:]
ROT = pathlib.Path(args[args.index('--rot') + 1] if '--rot' in args else pathlib.Path(__file__).resolve().parents[3])
VIS_REST = '--vis-rest' in args
LENKEFIL = args[args.index('--lenker') + 1] if '--lenker' in args else None
DOMENE = 'https://fodmapp.com'
SIDER = ['index.html', 'manual.html', 'about.html', 'delete.html', 'privacypolicy.html', 'termsandconditions.html']
VOID = {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'source', 'track', 'wbr', 'path', 'circle', 'rect', 'line'}

# Lik engelsk med vilje: navn og ord som er like på språket. Hver linje er en vurdering, ikke et unntak for hele språket.
LIK_OK_ALLE = {
    # merkenavn, firma, adresse, personer og enheter i anmeldelsene
    'FODMAPP', 'FODMAP', 'FODMAPP logo', 'FODMAPP Plus', '⭐ FODMAPP Plus', 'App Store', 'Google Play', '· Google Play', 'iOS', 'Android',
    'iOS & Android', 'AI', 'AI · 24/7', 'OpenStreetMap', 'OpenStreetMap / Overpass', 'Open Food Facts', '© 2026 FODMAPP · Telemark Software Solutions AS',
    'Telemark Software Solutions AS', 'post@fodmapp.com', 'www.fodmapp.com', 'www.datatilsynet.no', 'Østli 15, 3718 Skien', 'Gemini', 'Claude',
    'Anthropic', 'Google', 'Google Firebase', 'Google Maps', 'Google (Google Cloud Vertex AI)', 'RevenueCat', 'Resend', 'Christoffer S.', 'Gouled Y.',
    'Karnekj', 'uskeivys', 'Meddern', 'chrbo86', 'Sannegilsen', 'Terje7755', 'Samsung Galaxy S24', 'Motorola moto e13',
    # språknavnene (velgeren og marqueen viser hvert språk på eget språk)
    'Norsk', 'Lietuvių', 'English',
    # ord som er like på språket (vurdert ett og ett; alle har en oversettelse i i18n.js som tilfeldigvis er lik)
    'FAQ', '✦ FAQ', 'Pause', 'Video', 'Menu', 'Tips', '✦ Tips', 'Demo', '▶ Demo', 'Logging', '📝 Logging', 'Filters', '🎛️ Filters', 'Contact', '✉ Contact',
    'Barcode', 'Scan', 'Animation', '💬 Feedback', '17. Force majeure', '17. Contact', 'Manual', 'Legal', 'Pages', 'Name', 'EU', 'Marketing.',
    'Version 2.1', 'Version 2.2', 'Version 2.3', 'Website:', 'Email:', 'Email', 'd) Images', 'AI Chat', '💬 AI Chat', 'E-mail',
}

# Språk -> (App Store-land, Google Play-land). Egen tabell, uavhengig av byggeskriptet.
BUTIKKLAND = {'en': ('us', ''), 'nb': ('no', 'NO'), 'da': ('dk', 'DK'), 'sv': ('se', 'SE'), 'fi': ('fi', 'FI'), 'de': ('de', 'DE'), 'fr': ('fr', 'FR'), 'es': ('es', 'ES'),
              'it': ('it', 'IT'), 'pt': ('pt', 'PT'), 'nl': ('nl', 'NL'), 'pl': ('pl', 'PL'), 'ru': ('ru', 'RU'), 'tr': ('tr', 'TR'), 'ja': ('jp', 'JP'), 'ko': ('kr', 'KR'),
              'zh-Hans': ('cn', 'CN'), 'zh-Hant': ('tw', 'TW'), 'hi': ('in', 'IN'), 'id': ('id', 'ID'), 'lt': ('lt', 'LT'), 'th': ('th', 'TH'), 'ar': ('sa', 'SA')}

DATO = re.compile(r'\d{1,2} [A-Za-z]+ \d{4} ?·?')   # f.eks. id: «20 November 2026» er likt i engelsk

feil = []
rest = {}


def F(s):
    feil.append(s)


def last_t():
    js = r"""
const fs=require('fs');const src=fs.readFileSync(process.argv[1],'utf8');
const {T,LANGS}=new Function('localStorage','document',src.replace(/^const /gm,'var ')+'\nreturn {T,LANGS}')(
 {getItem:()=>null,setItem(){}},{documentElement:{},querySelectorAll:()=>[],getElementById:()=>null,createElement:()=>({})});
process.stdout.write(JSON.stringify({T,LANGS}));"""
    r = subprocess.run(['node', '-e', js, str(ROT / 'js' / 'i18n.js')], capture_output=True, encoding='utf-8')
    if r.returncode:
        raise SystemExit(r.stderr)
    d = json.loads(r.stdout)
    return d['T'], d['LANGS']


T, LANGS = last_t()
KODER = [l['code'] for l in LANGS]
SPRAAKNAVN = {l['name'] for l in LANGS}
NOKLER = {k for b in T.values() for k in b}


def mappe(k):
    return '' if k == 'en' else 'no/' if k == 'nb' else k.lower() + '/'


def fil(k, s):
    return mappe(k) + s


def url(k, s):
    return f"{DOMENE}/{mappe(k)}{'' if s == 'index.html' else s}"


class Side(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack, self.i18n, self.tekster, self.attrs, self.lenker, self.ider = [], [], [], [], [], set()
        self.meta, self.canon, self.alt, self.html_attrs, self.tittel, self.ld = {}, [], [], {}, '', []
        self.i_stil = 0
        self.i_tittel = False
        self.i_ld = False
        self.i_noscript = 0
        self.h1 = 0

    def handle_starttag(self, tag, a):
        d = dict(a)
        if tag == 'html':
            self.html_attrs = d
        if tag == 'title':
            self.i_tittel = True
        if tag in ('script', 'style'):
            self.i_stil += 1
            self.i_ld = d.get('type') == 'application/ld+json'
            if d.get('src'):
                self.lenker.append(d['src'])
        if tag == 'noscript':
            self.i_noscript += 1
        if tag == 'h1':
            self.h1 += 1
        if d.get('id'):
            self.ider.add(d['id'])
        if d.get('name') and tag == 'a':
            self.ider.add(d['name'])
        if tag == 'meta':
            n = d.get('name') or d.get('property')
            if n:
                self.meta[n] = d.get('content', '')
        if tag == 'link':
            if d.get('rel') == 'canonical':
                self.canon.append(d.get('href'))
            if d.get('rel') == 'alternate' and d.get('hreflang'):
                self.alt.append((d['hreflang'], d.get('href')))
            if d.get('rel') in ('icon', 'stylesheet') and d.get('href'):
                self.lenker.append(d['href'])
        for n in ('href', 'src', 'data-src', 'poster'):
            if d.get(n) and tag != 'link' and tag != 'script':
                self.lenker.append(d[n])
        if d.get('srcset'):
            self.lenker += [x.strip().split(' ')[0] for x in d['srcset'].split(',')]
        for n in ('alt', 'title', 'aria-label', 'placeholder'):
            if d.get(n):
                self.attrs.append((n, d[n]))
        if tag not in VOID:
            e = {'tag': tag, 'k': d.get('data-i18n'), 'tekst': []}
            self.stack.append(e)
            if d.get('data-i18n'):
                self.i18n.append(e)

    def handle_startendtag(self, tag, a):
        self.handle_starttag(tag, a)
        if tag not in VOID:
            self.handle_endtag(tag)

    def handle_endtag(self, tag):
        if tag == 'title':
            self.i_tittel = False
        if tag in ('script', 'style'):
            self.i_stil -= 1
            self.i_ld = False
        if tag == 'noscript':
            self.i_noscript -= 1
        if tag in VOID:
            return
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i]['tag'] == tag:
                del self.stack[i:]
                break

    def handle_data(self, data):
        if self.i_tittel:
            self.tittel += data
        if self.i_ld:
            self.ld.append(data)
        if self.i_stil or self.i_noscript:
            return
        for e in self.stack:
            if e['k']:
                e['tekst'].append(data)
        s = data.strip()
        if s:
            self.tekster.append(re.sub(r'\s+', ' ', s))


def les(rel):
    p = ROT / rel
    if not p.exists():
        F(f'{rel}: finnes ikke')
        return None
    return p.read_bytes().decode('utf-8')


def parse(rel):
    s = les(rel)
    if s is None:
        return None
    a = Side()
    a.feed(s)
    a.raa = s
    return a


def ren(v):
    return re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', '', v))).strip()


SIDEDATA = {}
for k in KODER:
    for s in SIDER:
        SIDEDATA[(k, s)] = parse(fil(k, s))
if feil:
    print('\n'.join(feil[:30]))
    print(f'FEIL: {len(feil)} sider mangler')
    sys.exit(1)

tell = dict(sider=0, tekster=0, lenker=0, hreflang=0, i18n=0)
FORVENTET_ALT = sorted([(k, None) for k in KODER] + [('x-default', None)])


def lenke_mal(rel_side, href):
    """Oversetter en lenke til fil + anker slik GitHub Pages ville funnet den. None = ekstern, tom eller spesiell."""
    if not href or href.startswith(('http://', 'https://', 'mailto:', 'tel:', 'data:', 'javascript:', '//')):
        return None
    h, _, anker = href.partition('#')
    h = h.partition('?')[0]
    base = pathlib.PurePosixPath(rel_side).parent
    if h == '':
        return rel_side, anker
    if h.startswith('/'):
        rel = h.lstrip('/')
    else:
        d = []
        for b in (base / h).parts:
            if b == '..':
                if not d:
                    return ('UTENFOR:' + href, '')
                d.pop()
            elif b != '.':
                d.append(b)
        rel = '/'.join(d)
    if rel == '' or (ROT / rel).is_dir():
        rel = (rel + '/index.html').lstrip('/')
    elif not (ROT / rel).exists() and (ROT / (rel + '.html')).exists():
        rel += '.html'
    return rel, anker


for (k, s), a in SIDEDATA.items():
    rel = fil(k, s)
    tell['sider'] += 1
    # lang, dir
    if a.html_attrs.get('lang') != k:
        F(f'{rel}: lang={a.html_attrs.get("lang")}')
    if a.html_attrs.get('dir') != ('rtl' if k == 'ar' else 'ltr'):
        F(f'{rel}: dir={a.html_attrs.get("dir")}')
    # tittel, meta
    en = SIDEDATA[('en', s)]
    if not a.tittel.strip():
        F(f'{rel}: tom tittel')
    if not a.meta.get('description'):
        F(f'{rel}: mangler beskrivelse')
    if k != 'en' and a.tittel == en.tittel:
        F(f'{rel}: tittelen er engelsk')
    if k != 'en' and a.meta.get('description') == en.meta.get('description'):
        F(f'{rel}: beskrivelsen er engelsk')
    if k != 'en' and 'keywords' in a.meta:
        F(f'{rel}: engelske keywords')
    for n in ('og:title', 'og:description', 'twitter:title', 'twitter:description'):
        if k != 'en' and n in a.meta and a.meta[n] == en.meta.get(n):
            F(f'{rel}: {n} er engelsk')
    if a.h1 < 1:
        F(f'{rel}: ingen h1')
    # canonical
    if a.canon != [url(k, s)]:
        F(f'{rel}: canonical {a.canon}')
    if 'og:url' in a.meta and k != 'en' and a.meta['og:url'] != url(k, s):
        F(f'{rel}: og:url {a.meta["og:url"]}')
    # hreflang
    alt = dict(a.alt)
    if len(a.alt) != len(KODER) + 1 or len(alt) != len(KODER) + 1:
        F(f'{rel}: {len(a.alt)} hreflang')
    if alt.get('x-default') != url('en', s):
        F(f'{rel}: x-default {alt.get("x-default")}')
    for m in KODER:
        tell['hreflang'] += 1
        if alt.get(m) != url(m, s):
            F(f'{rel}: hreflang {m} = {alt.get(m)}')
        # Paret: søsteren må peke tilbake hit.
        if dict(SIDEDATA[(m, s)].alt).get(k) != url(k, s):
            F(f'{fil(m, s)}: peker ikke tilbake til {k}')
    # data-i18n = i18n.js, nøyaktig tekst
    for e in a.i18n:
        tell['i18n'] += 1
        v = T[k].get(e['k'])
        got = re.sub(r'\s+', ' ', ''.join(e['tekst'])).strip()
        if v:
            if got != ren(v):
                F(f'{rel}: {e["k"]} avviker fra i18n.js: «{got[:60]}» / «{ren(v)[:60]}»')
        elif k != 'en':
            F(f'{rel}: {e["k"]} mangler i i18n.js')
    # rå nøkler, plassholdere
    for t in a.tekster + [v for _, v in a.attrs]:
        tell['tekster'] += 1
        if t in NOKLER or re.fullmatch(r'(undefined|null|NaN)', t) or '{{' in t:
            F(f'{rel}: rå tekst «{t[:50]}»')
    # engelsk rest
    if k != 'en':
        ent = set(en.tekster) | {v for _, v in en.attrs}
        for t in a.tekster + [v for _, v in a.attrs]:
            if t in ent and re.search(r'[A-Za-z]{2}', t) and t not in LIK_OK_ALLE and t not in SPRAAKNAVN and not DATO.fullmatch(t):
                rest.setdefault(t, set()).add(f'{k}/{s}')
    # forbudte ord (ikke i juridiske sider, der Monash heller ikke skal stå)
    tekst = ' '.join(a.tekster) + ' ' + a.tittel + ' ' + a.meta.get('description', '')
    if re.search(r'monash', tekst, re.I):
        F(f'{rel}: Monash')
    if k == 'nb' and ('lav-FODMAP' in tekst or 'Lav-FODMAP' in tekst):
        F(f'{rel}: lav-FODMAP')
    if 'i18n.js' in a.raa.replace('data-i18n', '') and 'js/i18n.js' in ' '.join(a.lenker):
        F(f'{rel}: laster fortsatt i18n.js')
    # lenker
    for h in a.lenker:
        m = lenke_mal(rel, h)
        if m is None or h.endswith('videos/demo-ny.mp4'):   # valgfri video: bryteren vises bare hvis fila finnes
            continue
        tell['lenker'] += 1
        mal, anker = m
        if mal.startswith('UTENFOR:') or not (ROT / mal).exists():
            F(f'{rel}: død lenke {h}')
        elif anker and mal.endswith('.html'):
            mk = next(((x, y) for (x, y) in SIDEDATA if fil(x, y) == mal), None)
            if mk and anker not in SIDEDATA[mk].ider:
                F(f'{rel}: anker {h} finnes ikke')
    # lenker mellom språk: språkvelgeren skal ha alle språk, med riktig sti for denne siden
    for m in KODER:
        if not re.search(rf'<a class="lang-option[^"]*" href="[^"]*" hreflang="{m}" lang="{m}" data-kode="{m}">', a.raa):
            F(f'{rel}: språkvelgeren mangler {m}')
    if not re.search(rf'<a class="lang-option active" [^>]*data-kode="{k}">', a.raa):
        F(f'{rel}: velgeren viser ikke {k} som aktiv')
    for href, m in re.findall(r'<a class="lang-option[^"]*" href="([^"]*)" hreflang="[^"]*" lang="[^"]*" data-kode="([^"]*)">', a.raa):
        mal = lenke_mal(rel, href)
        if not mal or mal[0] != fil(m, s):
            F(f'{rel}: velgeren peker {m} til {href} ({mal})')
    # butikklenker
    apple = re.findall(r'href="(https://apps\.apple\.com/[^"]+)"', a.raa)
    play = [html.unescape(x) for x in re.findall(r'href="(https://play\.google\.com/[^"]+)"', a.raa)]
    cc, gl = BUTIKKLAND[k]
    for x in apple:
        if not x.startswith(f'https://apps.apple.com/{cc}/') or 'id6761849984' not in x:
            F(f'{rel}: App Store-lenken peker til feil land: {x}')
    for x in play:
        if (gl and f'&gl={gl}' not in x) or 'id=com.telemarksoftwaresolutions.fodmapp' not in x:
            F(f'{rel}: Play-lenken peker til feil land: {x}')
    if s in ('index.html', 'manual.html', 'about.html') and (not apple or not play):
        F(f'{rel}: mangler butikklenker')
    # strukturerte data
    if s == 'index.html':
        try:
            ld = json.loads(''.join(a.ld))
        except Exception as e:
            F(f'{rel}: strukturerte data er ugyldige: {e}')
            ld = {}
        if ld.get('@type') != 'SoftwareApplication' or ld.get('name') != 'FODMAPP' or ld.get('url') != url(k, s):
            F(f'{rel}: strukturerte data {ld.get("@type")} {ld.get("url")}')
        for n in ('aggregateRating', 'review', 'offers', 'award'):
            if n in ld:
                F(f'{rel}: strukturerte data har {n}')
        if k != 'en' and ld.get('description') == json.loads(''.join(SIDEDATA[('en', s)].ld)).get('description'):
            F(f'{rel}: strukturerte data er engelske')
    elif a.ld:
        F(f'{rel}: uventede strukturerte data')

for t, h in sorted(rest.items(), key=lambda x: -len(x[1])):
    F(f'engelsk rest ({len(h)} sider, f.eks. {sorted(h)[0]}): «{t[:90]}»')

# Sitemap
sm = les('sitemap.xml') or ''
try:
    ET.fromstring(sm)
except ET.ParseError as e:
    F(f'sitemap: ugyldig XML: {e}')
loc = re.findall(r'<loc>([^<]+)</loc>', sm)
forv = {url(k, s) for k in KODER for s in SIDER}
if set(loc) != forv or len(loc) != len(forv):
    F(f'sitemap: {len(loc)} adresser, ventet {len(forv)}')
if '?lang=' in sm:
    F('sitemap: ?lang= står igjen')
if sm.count('xhtml:link') != len(loc) * (len(KODER) + 1):
    F(f'sitemap: {sm.count("xhtml:link")} xhtml:link')
if 'Sitemap: https://fodmapp.com/sitemap.xml' not in (les('robots.txt') or ''):
    F('robots.txt mangler sitemap')
if not re.search(r'^Allow: /\s*$', les('robots.txt') or '', re.M) or re.search(r'^Disallow: /', les('robots.txt') or '', re.M):
    F('robots.txt stenger noe')

# llms.txt
lm = les('llms.txt') or ''
for u in re.findall(r'https://fodmapp\.com/[^\s)]*', lm):
    m = lenke_mal('x.html', u[len(DOMENE):])
    if m and not (ROT / m[0]).exists():
        F(f'llms.txt: død lenke {u}')
if re.search(r'monash|trigger|rating|review|cure|treat', lm, re.I):
    F('llms.txt: ord som ikke hører hjemme der')

# Videresendinger, 404, hosting
for s in SIDER:
    for d, m in (('en', ''), ('nb', 'no/')):
        x = les(f'{d}/{s}') or ''
        f = '' if s == 'index.html' else s
        if f'href="{DOMENE}/{m}{f}"' not in x or 'noindex' not in x or 'http-equiv="refresh"' not in x:
            F(f'{d}/{s}: videresendingen er feil')
if 'noindex' not in (les('404.html') or ''):
    F('404.html mangler noindex')
if (ROT / '.nojekyll').exists():
    F('.nojekyll finnes: _internal blir synlig')
if (les('CNAME') or '').strip() != 'fodmapp.com':
    F('CNAME er endret')
if '_internal' not in (les('_config.yml') or ''):
    F('_config.yml utelater ikke _internal')
for navn in ('js/i18n.js', 'js/spraak.js'):
    les(navn)

# Gamle lenker (fra fodmapp-kode, appen, butikkene, e-postene, annonsene)
if LENKEFIL:
    for u in pathlib.Path(LENKEFIL).read_text(encoding='utf-8').split():
        u0 = re.sub(r'^https?://(www\.)?fodmapp\.com', '', u)
        m = lenke_mal('x.html', u0 or '/')
        if m and not (ROT / m[0]).exists():
            F(f'gammel lenke død: {u}')

if VIS_REST:
    for t, h in sorted(rest.items(), key=lambda x: -len(x[1])):
        print(len(h), sorted(h)[:3], t[:120])
print(f'{len(KODER)} språk x {len(SIDER)} sider = {tell["sider"]} sider; {tell["i18n"]} data-i18n, {tell["hreflang"]} hreflang-par, '
      f'{tell["lenker"]} interne lenker, {tell["tekster"]} tekster')
if feil:
    for f in feil[:int(args[args.index("--maks")+1]) if "--maks" in args else 80]:
        print('FEIL', f)
    print(f'FEIL: {len(feil)}')
    sys.exit(1)
print('OK')
