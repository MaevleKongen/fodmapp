#!/usr/bin/env python3
"""Bygger de statiske språksidene til fodmapp.com fra js/i18n.js (runde rSpraak, nov 2026).

    python -X utf8 _internal/tools/i18n/bygg_spraak.py          bygger alt (idempotent)
    python -X utf8 _internal/tools/i18n/bygg_spraak.py --sjekk  skriver ingenting, exit 1 hvis noe er utdatert

Kilder: rotsidene (index.html, manual.html, ...: engelsk, med data-i18n-merker) og js/i18n.js (alle tekstene).
Resultat:
  /<språk>/<side>.html  ferdig oversatt HTML: lang, dir, title, meta, canonical, hreflang, butikklenker, app-bilder
  rotsidene             samme merker, bare hode, språkvelger og skript byttes; den engelske teksten røres ikke
  /en/, /nb/            små videresendingssider (engelsk bor på rota, norsk på /no/)
  404.html, sitemap.xml, llms.txt

Endrer du en tekst: rediger js/i18n.js (inject.py) og den statiske engelske HTML-en på rota, kjør validate.js og
dette skriptet, og publiser de genererte filene sammen med endringen. Rediger ALDRI filene i språkmappene for hånd.
Ikke legg til .nojekyll (se _config.yml): da blir _internal/ synlig på nettet.
"""
import html
import json
import pathlib
import re
import sys

sys.dont_write_bytecode = True   # ingen __pycache__ i publiseringsgrunnlaget
from inject import find_lang_block  # noqa: E402

ROT = pathlib.Path(__file__).resolve().parents[3]
DOMENE = 'https://fodmapp.com'
SIDER = ['index.html', 'manual.html', 'about.html', 'delete.html', 'privacypolicy.html', 'termsandconditions.html']
# Automatisk språkvalg på forsiden / ut fra nettleserens språk. AV: siden har aldri gjort det før (js/i18n.js brukte bare
# lagret valg), oppgaven ba ikke om det, og det krever at roboter skilles ut på user-agent (ligner cloaking), mot Googles
# råd om språkvideresending og med annonselandingen som innsats. Søk og AI finner språksidene via hreflang og sitemap uansett.
# Skal det på, gjør det som et eget, målt valg: sett True, bygg, kjør kontroll_nettleser.mjs med --auto.
AUTO_SPRAAK = False

# App Store-land og Play (hl, gl) per språk. Alle er sjekket mot itunes.apple.com/lookup (resultCount 1) 2. nov 2026.
LAND = {
    'id': ('id', 'id', 'ID'), 'da': ('dk', 'da', 'DK'), 'de': ('de', 'de', 'DE'), 'es': ('es', 'es', 'ES'),
    'fr': ('fr', 'fr', 'FR'), 'it': ('it', 'it', 'IT'), 'lt': ('lt', 'lt', 'LT'), 'nl': ('nl', 'nl', 'NL'),
    'nb': ('no', 'no', 'NO'), 'pl': ('pl', 'pl', 'PL'), 'pt': ('pt', 'pt-PT', 'PT'), 'fi': ('fi', 'fi', 'FI'),
    'sv': ('se', 'sv', 'SE'), 'tr': ('tr', 'tr', 'TR'), 'ru': ('ru', 'ru', 'RU'), 'ar': ('sa', 'ar', 'SA'),
    'hi': ('in', 'hi', 'IN'), 'th': ('th', 'th', 'TH'), 'zh-Hans': ('cn', 'zh-CN', 'CN'),
    'zh-Hant': ('tw', 'zh-TW', 'TW'), 'ja': ('jp', 'ja', 'JP'), 'ko': ('kr', 'ko', 'KR'),
}
APPLE_ID = 'id6761849984'
PLAY_ID = 'com.telemarksoftwaresolutions.fodmapp'
APPLE_EN = f'https://apps.apple.com/us/app/low-fodmap-ibs-app-fodmapp/{APPLE_ID}'
PLAY_EN = f'https://play.google.com/store/apps/details?id={PLAY_ID}'

# Tekster som skriptene henter mens siden kjører. Alt annet står ferdig i HTML-en.
KJORETID = ['web_f82_rull_hint', 'web_f82_demo_pause', 'web_f82_demo_spill',
            'web_f210_karusell_kort', 'web_f210_karusell_neste', 'web_f210_karusell_forrige']
# (nøkkel for tittel, nøkkel for beskrivelse) per side. Bare eksisterende, oversatte tekster: ingen nye påstander.
META = {
    'index.html': ('ft_desc', 'feat_sub'), 'manual.html': ('man_h1', 'man_intro'), 'about.html': ('ab_h1', 'ab_intro'),
    'delete.html': ('del_h1', 'del_intro'), 'privacypolicy.html': ('pp_h1', 'pp_intro'),
    'termsandconditions.html': ('tc_h1', 'tc_intro'),
}
HODE_A, HODE_B = '<!-- rSpraak:hode -->', '<!-- /rSpraak:hode -->'
KJOR_A, KJOR_B = '<!-- rSpraak:kjoretid -->', '<!-- /rSpraak:kjoretid -->'


def les_i18n():
    src = (ROT / 'js' / 'i18n.js').read_text(encoding='utf-8').replace('\r\n', '\n')
    langs = [dict(code=c, flag=f, name=n) for c, f, n in
             re.findall(r'\{code:"([^"]+)",flag:"([^"]+)",name:"([^"]+)"\}', src)]
    t = {}
    for l in langs:
        a, b = find_lang_block(src, l['code'])
        blokk = {}
        for m in re.finditer(r'^\s*"([^"]+)"\s*:\s*("(?:[^"\\]|\\.)*")\s*,?\s*$', src[a:b], re.M):
            blokk[m.group(1)] = json.loads(m.group(2))
        t[l['code']] = blokk
    return langs, t


def sti(kode):
    """Språkmappa: /no/ for norsk, / for engelsk, små bokstaver ellers (GitHub Pages skiller på store og små)."""
    if kode == 'en':
        return ''
    if kode == 'nb':
        return 'no/'
    return kode.lower() + '/'


def side_url(kode, side):
    return f"{DOMENE}/{sti(kode)}{'' if side == 'index.html' else side}"


def ren_tekst(v):
    return re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', v))).strip()


def attr(s):
    return html.escape(s, quote=True)


def kort(s, n=200):
    """Beskrivelsen: helst hele setninger, aldri over n tegn."""
    if len(s) <= n:
        return s
    biter = re.split(r'(?<=[.!?。！？।])\s*', s)
    ut = ''
    for b in biter:
        if len(ut) + len(b) + 1 > n:
            break
        ut = (ut + ' ' + b).strip()
    if ut:
        return ut
    kutt = s[:n].rsplit(' ', 1)[0]
    return kutt + '…'


def tittel(kode, side, t):
    v = ren_tekst(t[kode][META[side][0]]).rstrip('.。।')
    if side == 'index.html':
        return f'FODMAPP – {v}'
    return v if 'FODMAPP' in v else f'{v} – FODMAPP'


def beskrivelse(kode, side, t):
    return kort(ren_tekst(t[kode][META[side][1]]))


# ---------------------------------------------------------------- hodet

def startskript(kode, side, langs):
    """Kjøres FØR siden tegnes. ?lang= sendes til riktig sti. Bare rotsidene (engelsk) kan sende noen videre av seg selv:
    et valg brukeren har gjort tidligere (slik siden virket før rSpraak). En språkside blir der den er. Roboter har ingen
    lagret verdi og blir alltid der de er, uten at skriptet ser på user-agent. Med AUTO_SPRAAK også nettleserens språk
    på forsiden, men aldri fra en annen side på fodmapp.com og aldri uten lagring (da kunne ingen velge engelsk igjen)."""
    k = {l['code']: sti(l['code']) for l in langs}
    f = '' if side == 'index.html' else side
    auto = ''
    if AUTO_SPRAAK and kode == 'en' and side == 'index.html':
        auto = ("else if(o&&document.referrer.indexOf(location.origin)!==0&&"
                "!/bot|crawl|spider|slurp|preview|fetch|lighthouse|headless|google|bing|facebook|perplexity|chatgpt/i.test(navigator.userAgent)){"
                "var L=navigator.languages||[navigator.language];for(var i=0;i<L.length;i++){var v=V(L[i]);if(v){if(v!=='en')t=v;break}}}")
    return ('<script>(function(C,F,K){try{'
            "var N='fodmapp-lang',H=function(k){return Object.prototype.hasOwnProperty.call(K,k)},"
            "V=function(x){x=String(x||'').replace('_','-').toLowerCase();var b=x.split('-')[0];"
            "if(b==='nb'||b==='no'||b==='nn')return'nb';if(b==='zh')return/hant|tw|hk|mo/.test(x)?'zh-Hant':'zh-Hans';"
            "return H(b)?b:null},"
            "s=location.search,m=s.match(/[?&]lang=([^&#]*)/),q=m?V(decodeURIComponent(m[1])):null,t=null,g=null,o=0;"
            "try{g=localStorage.getItem(N);o=1}catch(e){}"
            "if(m){s=s.replace(/([?&])lang=[^&#]*(&?)/,function(a,p,e){return e?p:''});if(q){t=q;try{localStorage.setItem(N,q)}catch(e){}}}"
            f"else if(C==='en'){{if(g&&H(g)){{if(g!=='en')t=g}}{auto}}}"
            "if(t&&t!==C)location.replace('/'+K[t]+F+s+location.hash);"
            "else if(m&&q)history.replaceState(null,'',location.pathname+s+location.hash)"
            f"}}catch(e){{}}}})({json.dumps(kode)},{json.dumps(f)},{json.dumps(k, separators=(',', ':'))});</script>")


def json_ld(kode, side, t, langs):
    apple, play = butikk_urler(kode)
    d = {
        '@context': 'https://schema.org', '@type': 'SoftwareApplication', 'name': 'FODMAPP',
        'operatingSystem': 'iOS, Android', 'applicationCategory': 'HealthApplication',
        'description': ren_tekst(t[kode]['ft_desc']), 'url': side_url(kode, side),
        'image': f'{DOMENE}/images/og-fodmapp.png', 'installUrl': [apple, play], 'sameAs': [apple, play],
        'publisher': {'@type': 'Organization', 'name': 'Telemark Software Solutions AS'},
        'inLanguage': [l['code'] for l in langs],
    }
    return json.dumps(d, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')


def butikk_urler(kode):
    if kode == 'en':
        return APPLE_EN, PLAY_EN
    cc, hl, gl = LAND[kode]
    return f'https://apps.apple.com/{cc}/app/{APPLE_ID}', f'{PLAY_EN}&hl={hl}&gl={gl}'


def hode(kode, side, langs, nl):
    d = [HODE_A, f'<link rel="canonical" href="{side_url(kode, side)}">',
         f'<link rel="alternate" hreflang="x-default" href="{side_url("en", side)}">']
    d += [f'<link rel="alternate" hreflang="{l["code"]}" href="{side_url(l["code"], side)}">' for l in langs]
    # 320 px: logoen gikk inn under språkknappen
    d.append('<style>a.lang-option{text-decoration:none}@media(max-width:340px){.logo{font-size:1.12rem;gap:.35rem}.logo img{height:36px}}</style>')
    d.append('<noscript><style>.lang-btn{display:none}.lang-overlay{display:block;position:static;opacity:1;'
             'background:none;backdrop-filter:none}.lang-modal{transform:none;box-shadow:none;max-height:none;'
             'max-width:none;margin:1rem auto}.lang-modal-close{display:none}'
             '.lang-grid{grid-template-columns:repeat(auto-fill,minmax(170px,1fr))}</style></noscript>')
    d.append(startskript(kode, side, langs))
    d.append(HODE_B)
    return nl.join('  ' + x for x in d).lstrip()


def kjoretid(kode, side, t, nl, pre):
    bruk = side in ('index.html', 'manual.html')
    tekst = json.dumps({kode: {k: t[kode][k] for k in KJORETID}}, ensure_ascii=False, separators=(',', ':')) if bruk else '{}'
    tekst = tekst.replace('</', '<\\/')
    return (f'{KJOR_A}<script>var currentLang={json.dumps(kode)},T={tekst};</script>'
            f'<script src="{pre}js/spraak.js"></script>{KJOR_B}')


def spraakvelger(kode, side, langs, til_rot):
    f = '' if side == 'index.html' else side
    ut = []
    for l in langs:
        href = til_rot + sti(l['code']) + f or './'
        if til_rot == '' and not sti(l['code']) and not f:
            href = './'
        aktiv = ' active' if l['code'] == kode else ''
        ut.append(f'<a class="lang-option{aktiv}" href="{href}" hreflang="{l["code"]}" lang="{l["code"]}" '
                  f'data-kode="{l["code"]}"><span class="lang-flag">{l["flag"]}</span>{l["name"]}</a>')
    return ''.join(ut)


# ---------------------------------------------------------------- HTML-gjennomgang

MASKE = re.compile(r'<!--.*?-->|<script\b.*?</script\s*>|<style\b.*?</style\s*>', re.S | re.I)
TAGG = re.compile(r'''<([a-zA-Z][a-zA-Z0-9-]*)((?:\s+(?:"[^"]*"|'[^']*'|[^'">])*)?)>''')


def maskert(s):
    """Samme lengde som s, men skript, stil og kommentarer er blanket ut, så tagger inni dem ikke telles."""
    return MASKE.sub(lambda m: ' ' * len(m.group(0)), s)


def attr_verdi(attrs, navn):
    m = re.search(r'(?:^|\s)' + re.escape(navn) + r'''\s*=\s*"([^"]*)"''', attrs)
    return m.group(1) if m else None


def sett_attr(attrs, navn, verdi):
    v = f'{navn}="{verdi}"'
    ny, n = re.subn(r'(^|\s)' + re.escape(navn) + r'''\s*=\s*"[^"]*"''', lambda m: m.group(1) + v, attrs, count=1)
    return ny if n else attrs + ' ' + v


def fjern_attr(attrs, navn):
    return re.sub(r'\s+' + re.escape(navn) + r'''(\s*=\s*"[^"]*")?(?=\s|$|/)''', '', attrs, count=1)


def finn_slutt(m, navn, start):
    """Slutten av elementet navn som begynner ved start (start = etter starttaggen): teller bare samme taggnavn."""
    d = 1
    for t in re.finditer(r'<(/?)' + re.escape(navn) + r'''(?:\s(?:"[^"]*"|'[^']*'|[^'">])*)?(/?)>''', m[start:], re.I):
        if t.group(1):
            d -= 1
            if d == 0:
                return start + t.start()
        elif not t.group(2):
            d += 1
    raise SystemExit(f'fant ikke sluttag for <{navn}> ved {start}')


def app_bilde_mappe(kode, html_tekst):
    m = re.search(r'APP_BILDE_SPRAAK=(\[[^\]]*\]),APP_BILDE_RESERVE="([^"]+)"', html_tekst)
    if not m:
        return None
    return kode if kode in json.loads(m.group(1)) else m.group(2)


def bilde_attrs(attrs, mappe):
    b = attr_verdi(attrs, 'data-app-bilde')
    grunn = f'images/app/{mappe}/{b}'
    attrs = sett_attr(attrs, 'src', f'{grunn}.webp')
    if re.search(r'\sdata-stor\b', attrs):
        attrs = sett_attr(attrs, 'srcset', f'{grunn}.webp 600w, {grunn}_860.webp 860w')
    return attrs


def gjengi(s, kode, t, bare_attr=False):
    """Det applyLang() og de små skriptene gjør i nettleseren, gjort på forhånd: data-i18n (innhold), data-i18n-ph
    (placeholder), data-i18n-aria (aria-label), data-alt (alt) og app-bildene. Mangler nøkkelen, står engelsk (som før).
    bare_attr: rotsiden. Der står den engelske teksten fra før, bare attributtene må fylles inn."""
    tt = t[kode]
    m = maskert(s)
    mappe = app_bilde_mappe(kode, s)
    biter = []  # (start, slutt, ny)
    for tagg in TAGG.finditer(m):
        navn, a0 = tagg.group(1), tagg.group(2)
        # Attributtene leses fra originalen (masken er lik utenfor skript/stil/kommentarer).
        attrs = a0
        ny = attrs
        k = attr_verdi(attrs, 'data-i18n-ph')
        if k and tt.get(k):
            ny = sett_attr(ny, 'placeholder', attr(html.unescape(tt[k])))
        k = attr_verdi(attrs, 'data-i18n-aria')
        if k and tt.get(k):
            ny = sett_attr(ny, 'aria-label', attr(html.unescape(tt[k])))
        k = attr_verdi(attrs, 'data-alt')
        if k and tt.get(k):
            ny = sett_attr(ny, 'alt', attr(html.unescape(tt[k])))
        if mappe and attr_verdi(attrs, 'data-app-bilde'):
            ny = bilde_attrs(ny, mappe)
        if ny != attrs:
            biter.append((tagg.start(2), tagg.end(2), ny))
        k = attr_verdi(attrs, 'data-i18n')
        if k and tt.get(k) and not bare_attr:
            biter.append((tagg.end(), finn_slutt(m, navn, tagg.end()), tt[k]))
    # Ytterste vinner, som i nettleseren; bakfra, så indeksene holder.
    biter.sort(key=lambda b: (b[0], -b[1]))
    ut, slutt_ytre = [], -1
    forrige = 0
    for a, b, ny in biter:
        if a < slutt_ytre:
            continue
        ut.append(s[forrige:a])
        ut.append(ny)
        forrige = b
        slutt_ytre = b
    ut.append(s[forrige:])
    return tlf_etikett(''.join(ut))


def tlf_etikett(s):
    """Telefonenes aria-label er bildets alt-tekst (settAppBilder gjør det samme når siden kjører)."""
    def en(m):
        i = re.search(r'''<img\b[^>]*?\salt="([^"]*)"''', s[m.end():m.end() + 600])
        return m.group(1) + (i.group(1) if i else m.group(2)) + m.group(3)
    return re.sub(r'''(<div class="tlf-kropp"[^>]*?\saria-label=")([^"]*)(")''', en, s)


def anmeldelser(s, kode):
    """«Oversatt fra ...» skal synes uten JavaScript også: skjult bare når sitatet står på originalspråket."""
    def kort_(m):
        orig = m.group(1)
        kropp = m.group(0)
        def span(sm):
            a = fjern_attr(sm.group(1), 'hidden')
            if orig == kode:
                a += ' hidden'
            return f'<span{a}>'
        return re.sub(r'<span((?:\s+[^>]*)?\sclass="review-ovs"[^>]*)>', span, kropp, count=1)
    return re.sub(r'data-orig="([^"]+)".*?review-ovs[^>]*>', kort_, s, flags=re.S)


def rens_rot(s, side, langs, t):
    """Rotsiden, engelsk: bytter hode, språkvelger og skript, teksten røres ikke. f(f(x)) = f(x)."""
    nl = '\r\n' if '\r\n' in s else '\n'
    s = re.sub(r'<html\b[^>]*>', '<html lang="en" dir="ltr">', s, count=1)
    s = gjengi(s, 'en', t, bare_attr=True)
    # Hodet: enten markørene fra forrige bygg, eller de gamle canonical/hreflang-linjene.
    if HODE_A in s:
        s = s[:s.index(HODE_A)] + '\0' + s[s.index(HODE_B) + len(HODE_B):]
    else:
        m = re.search(r'(?:[ \t]*<!-- Hreflang[^\n]*\n)?[ \t]*<link rel="canonical"[^\n]*\n(?:[ \t]*<link rel="alternate"[^\n]*\n)*', s)
        if not m:
            raise SystemExit(f'{side}: fant ikke canonical')
        s = s[:m.start()] + '  \0' + nl + s[m.end():]
    s = s.replace('\0', hode('en', side, langs, nl))
    # Skriptene: i18n.js (2,3 MB) lastes ikke lenger, teksten står i HTML-en.
    if KJOR_A in s:
        s = s[:s.index(KJOR_A)] + '\0' + s[s.index(KJOR_B) + len(KJOR_B):]
    else:
        if s.count('<script src="js/i18n.js"></script>') != 1:
            raise SystemExit(f'{side}: fant ikke i18n.js-skriptet')
        s = s.replace('<script src="js/i18n.js"></script>', '\0')
    s = s.replace('\0', kjoretid('en', side, t, nl, ''))
    s, n = re.subn(r'(<div class="lang-grid" id="langGrid">).*?(</div>)',
                   lambda m: m.group(1) + spraakvelger('en', side, langs, '') + m.group(2), s, count=1, flags=re.S)
    if n != 1:
        raise SystemExit(f'{side}: fant ikke språkvelgeren')
    # Språklista etter hovedinnholdet: uten JavaScript (og for roboter) kommer teksten først. Den er position:fixed ellers.
    m = re.search(r'[ \t]*(<div class="lang-overlay" id="langOverlay".*?</div></div></div>)\r?\n?', s, re.S)
    if not m:
        raise SystemExit(f'{side}: fant ikke språklista')
    s = s[:m.start()] + s[m.end():]
    i = s.index('<footer')
    s = s[:i] + m.group(1) + nl + '  ' + s[i:]
    if side == 'index.html':
        s, n = re.subn(r'(<script type="application/ld\+json">\s*).*?(\s*</script>)',
                       lambda m: m.group(1) + json_ld('en', side, t, langs) + m.group(2), s, count=1, flags=re.S)
        if n != 1:
            raise SystemExit('index.html: fant ikke strukturerte data')
    return anmeldelser(s, 'en')


def sett_meta(s, attributt, navn, verdi):
    """Bytter content på en meta-tagg hvis den finnes."""
    return re.sub(rf'(<meta {attributt}="{re.escape(navn)}" content=")[^"]*(">)',
                  lambda m: m.group(1) + attr(verdi) + m.group(2), s)


def spraakside(rot, kode, side, langs, t):
    nl = '\r\n' if '\r\n' in rot else '\n'
    s = gjengi(rot, kode, t)
    retning = 'rtl' if kode == 'ar' else 'ltr'
    s = re.sub(r'<html\b[^>]*>', f'<html lang="{kode}" dir="{retning}">', s, count=1)
    # Hode, velger, skript for dette språket
    s = s[:s.index(HODE_A)] + hode(kode, side, langs, nl) + s[s.index(HODE_B) + len(HODE_B):]
    s = s[:s.index(KJOR_A)] + kjoretid(kode, side, t, nl, '') + s[s.index(KJOR_B) + len(KJOR_B):]
    s = re.sub(r'(<div class="lang-grid" id="langGrid">).*?(</div>)',
               lambda m: m.group(1) + spraakvelger(kode, side, langs, '../') + m.group(2), s, count=1, flags=re.S)
    # Tittel og meta: ferdige tekster fra i18n.js
    ti, be = tittel(kode, side, t), beskrivelse(kode, side, t)
    s = re.sub(r'<title>.*?</title>', lambda m: f'<title>{attr(ti)}</title>', s, count=1, flags=re.S)
    s = re.sub(r'<meta name="description" content="[^"]*">', lambda m: f'<meta name="description" content="{attr(be)}">', s, count=1)
    s = re.sub(r'[ \t]*<meta name="keywords"[^>]*>\r?\n?', '', s, count=1)
    s = re.sub(r'[ \t]*<meta property="og:image:alt"[^>]*>\r?\n?', '', s, count=1)
    for a, n, v in (('property', 'og:title', ti), ('property', 'og:description', be), ('property', 'og:url', side_url(kode, side)),
                    ('name', 'twitter:title', ti), ('name', 'twitter:description', be)):
        s = sett_meta(s, a, n, v)
    # Vanlige attributter uten egen nøkkel i malen
    s = s.replace('title="Change language"', f'title="{attr(ren_tekst(t[kode]["lang_title"]))}"')
    s = s.replace('title="Download"', f'title="{attr(ren_tekst(t[kode]["nav_download"]).rstrip(" ↓↓"))}"')
    s = s.replace('<p>Email <a href="mailto:', f'<p>{t[kode]["ph_email"]} <a href="mailto:')
    # Butikklenkene til riktig land
    apple, play = butikk_urler(kode)
    s = s.replace(f'href="{APPLE_EN}"', f'href="{apple}"').replace(f'href="{PLAY_EN}"', f'href="{attr(play)}"')
    if side == 'index.html':
        s, n = re.subn(r'(<script type="application/ld\+json">\s*).*?(\s*</script>)',
                       lambda m: m.group(1) + json_ld(kode, side, t, langs) + m.group(2), s, count=1, flags=re.S)
        if n != 1:
            raise SystemExit(f'{kode}/{side}: fant ikke strukturerte data')
    s = anmeldelser(s, kode)
    return til_undermappe(s, kode, side)


def til_undermappe(s, kode, side):
    """Siden ligger én mappe ned: stier til filer må starte med ../. Lenker mellom sidene er relative og blir i språket."""
    s = re.sub(r'''((?:src|href|data-src|poster)=")((?:images|css|js|videos|rapport)/)''', r'\1../\2', s)
    s = re.sub(r'(srcset=")([^"]*)"', lambda m: m.group(1) + re.sub(r'(^|,\s*)(images/)', r'\1../\2', m.group(2)) + '"', s)
    # Skriptene bygger to stier selv
    n1 = s.count("'images/app/'")
    s = s.replace("'images/app/'", "'../images/app/'")
    s = s.replace('"video": "videos/demo-ny.mp4"', '"video": "../videos/demo-ny.mp4"')
    if side == 'index.html' and n1 != 1:
        raise SystemExit(f'{kode}: ventet én \'images/app/\' i skriptet, fant {n1}')
    # /xx/ er den kanoniske adressen, ikke /xx/index.html
    s = s.replace('href="index.html#', 'href="./#').replace('href="index.html"', 'href="./"')
    if re.search(r'''(?<!\.\./)(?<![\w/.:-])(?:images|videos|rapport)/[\w./-]+\.(?:png|webp|jpe?g|mp4|pdf|svg)''', maskert(s)):
        rest = re.findall(r'''(?<!\.\./)(?<![\w/.:-])(?:images|videos|rapport)/[\w./-]+\.(?:png|webp|jpe?g|mp4|pdf|svg)''', maskert(s))
        raise SystemExit(f'{kode}/{side}: filsti ikke flyttet: {rest[:3]}')
    return s


# ---------------------------------------------------------------- små filer

def stub(mal_rel, mal_abs, lagre=None):
    """Videresending for /en/* og /nb/*: engelsk bor på rota, norsk på /no/. Ingen indeksering."""
    js = f"try{{localStorage.setItem('fodmapp-lang',{json.dumps(lagre)})}}catch(e){{}}" if lagre else ''
    return ('<!DOCTYPE html>\n<html lang="en">\n<head>\n<meta charset="UTF-8">\n<title>FODMAPP</title>\n'
            f'<meta name="robots" content="noindex">\n<link rel="canonical" href="{mal_abs}">\n'
            f'<meta http-equiv="refresh" content="0; url={mal_rel}">\n'
            f"<script>{js}location.replace({json.dumps(mal_rel)}+location.search+location.hash);</script>\n"
            f'</head>\n<body><a href="{mal_rel}">{mal_abs}</a></body>\n</html>\n')


def side_404(langs):
    lenker = ''.join(f'<li><a href="/{sti(l["code"])}" hreflang="{l["code"]}" lang="{l["code"]}">{l["flag"]} {l["name"]}</a></li>'
                     for l in langs)
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="robots" content="noindex">
<title>404 – FODMAPP</title>
<link rel="icon" type="image/png" href="/images/logo.png">
<style>body{{font-family:system-ui,sans-serif;background:#FBF8F3;color:#23302A;margin:0;padding:3rem 16px;text-align:center}}
img{{width:64px;height:64px}}h1{{font-size:1.4rem;margin:1rem 0 2rem}}ul{{list-style:none;padding:0;margin:0 auto;max-width:640px;display:grid;grid-template-columns:repeat(auto-fill,minmax(170px,1fr));gap:.4rem}}
a{{display:block;padding:.5rem;border-radius:.6rem;color:inherit;text-decoration:none;background:#fff}}a:hover{{background:#E8F3EC}}</style>
<script>(function(){{var p=location.pathname,m=p.match(/^\\/([^\\/]+)(\\/.*)?$/);if(!m)return;var l=m[1].toLowerCase();
if(l!==m[1]&&/^[a-z]{{2}}(-han[st])?$/.test(l))location.replace('/'+l+(m[2]||'/')+location.search+location.hash)}})();</script>
</head>
<body><a href="/" style="display:inline-block;background:none"><img src="/images/logo.png" alt="FODMAPP"></a>
<h1>404 – FODMAPP</h1>
<ul>{lenker}</ul>
</body>
</html>
'''


def sitemap(langs):
    d = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"',
         '        xmlns:xhtml="http://www.w3.org/1999/xhtml">']
    for side in SIDER:
        for l in langs:
            d.append('  <url>')
            d.append(f'    <loc>{side_url(l["code"], side)}</loc>')
            d.append(f'    <xhtml:link rel="alternate" hreflang="x-default" href="{side_url("en", side)}"/>')
            d += [f'    <xhtml:link rel="alternate" hreflang="{a["code"]}" href="{side_url(a["code"], side)}"/>' for a in langs]
            d.append('  </url>')
    d.append('</urlset>')
    return '\n'.join(d) + '\n'


def llms(langs, t, rot):
    """llms.txt: bare tekster som allerede står på siden. Ingen nye påstander, ingen vurderinger."""
    en = t['en']
    def fra_siden(side):
        # Teksten som står på den engelske siden (meta-beskrivelsene har egne salgsord som ikke skal gjentas her).
        k = META[side][1]
        return ren_tekst(en[k]) if en.get(k) else ren_tekst(re.search(r'data-i18n="' + k + r'">(.*?)</', rot[side], re.S).group(1))
    apple, play = butikk_urler('en')
    navn = {'index.html': 'Home', 'manual.html': 'Manual', 'about.html': 'About', 'delete.html': 'Delete account and data',
            'privacypolicy.html': 'Privacy policy', 'termsandconditions.html': 'Terms and conditions'}
    tekst = {s: fra_siden(s) for s in SIDER}
    d = ['# FODMAPP', '', f'> {ren_tekst(en["ft_desc"])}', '', ren_tekst(en['man_intro']), '',
         f'{ren_tekst(en["man210_plus_p"])}', '',
         '- Platforms: iOS and Android', f'- Languages: {len(langs)}', '- Publisher: Telemark Software Solutions AS',
         f'- App Store: {apple}', f'- Google Play: {play}', '', '## Pages in English', '']
    d += [f'- [{navn[s]}]({side_url("en", s)}): {tekst[s]}' for s in SIDER]
    d += ['', '## Every language', '',
          'Each language has the same six pages as complete HTML in that language, for example '
          f'{side_url("nb", "manual.html")}.', '']
    d += [f'- [{l["name"]}]({side_url(l["code"], "index.html")})' for l in langs if l['code'] != 'en']
    d += ['', '## Sitemap', '', f'- {DOMENE}/sitemap.xml']
    return '\n'.join(d) + '\n'


# ---------------------------------------------------------------- hovedløp

def main():
    sjekk = '--sjekk' in sys.argv
    langs, t = les_i18n()
    if len(langs) != len(t) or 'en' not in t:
        raise SystemExit('LANGS og T stemmer ikke')
    mangler = [l['code'] for l in langs if l['code'] not in LAND and l['code'] != 'en']
    if mangler:
        raise SystemExit(f'LAND mangler {mangler}')
    filer = {}
    rot = {}
    for side in SIDER:
        kilde = (ROT / side).read_bytes().decode('utf-8')
        ny = rens_rot(kilde, side, langs, t)
        rot[side] = ny
        filer[side] = ny
    for l in langs:
        if l['code'] == 'en':
            continue
        for side in SIDER:
            filer[sti(l['code']) + side] = spraakside(rot[side], l['code'], side, langs, t)
    for side in SIDER:
        f = '' if side == 'index.html' else side
        filer['en/' + side] = stub('../' + f if f else '../', f'{DOMENE}/{f}', lagre='en')
        filer['nb/' + side] = stub('../no/' + f, f'{DOMENE}/no/{f}')
    filer['404.html'] = side_404(langs)
    filer['sitemap.xml'] = sitemap(langs)
    filer['llms.txt'] = llms(langs, t, rot)

    utdatert = []
    for navn, tekst in filer.items():
        p = ROT / navn
        gammel = p.read_bytes().decode('utf-8') if p.exists() else None
        if gammel is None or gammel.replace('\r\n', '\n') != tekst.replace('\r\n', '\n'):
            utdatert.append(navn)
            if not sjekk:
                p.parent.mkdir(parents=True, exist_ok=True)
                p.write_bytes(tekst.encode('utf-8'))
    # Filer i språkmappene som ikke lenger bygges (gammel side, gammel kode) skal bort.
    mapper = {sti(l['code']).rstrip('/') for l in langs if l['code'] != 'en'} | {'en', 'nb'}
    foreldet = [str(f.relative_to(ROT)).replace('\\', '/') for m in mapper if (ROT / m).is_dir() for f in (ROT / m).iterdir()
                if str(f.relative_to(ROT)).replace('\\', '/') not in filer]
    if sjekk:
        if utdatert or foreldet:
            print(f'UTDATERT: {len(utdatert)} filer {utdatert[:6]}; foreldet: {foreldet[:6]}. Kjør bygg_spraak.py.')
            sys.exit(1)
        print(f'OK: {len(filer)} filer er à jour')
        return
    for f in foreldet:
        (ROT / f).unlink()
    print(f'{len(filer)} filer, {len(utdatert)} skrevet, {len(foreldet)} fjernet')


if __name__ == '__main__':
    main()
