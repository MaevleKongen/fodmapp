import re, os

# ─────────────────────────────────────────────
# Part 1: Add i18n keys for reviews + cookie
# ─────────────────────────────────────────────
i18n_path = '/sessions/wizardly-pensive-albattani/mnt/outputs/js/i18n.js'
with open(i18n_path, 'r', encoding='utf-8') as f:
    content = f.read()

new_keys = {
    "nb": {
        "rev_tag":      "\u2b50 Anmeldelser",
        "rev_title":    "Hva brukerne sier",
        "rev_sub":      "Ekte anmeldelser fra Google Play",
        "cookie_msg":   "Vi bruker kun n\u00f8dvendige informasjonskapsler for at nettstedet skal fungere. Ingen sporing eller reklame.",
        "cookie_accept":"Godta",
        "cookie_decline":"Avvis",
    },
    "en": {
        "rev_tag":      "\u2b50 Reviews",
        "rev_title":    "What users say",
        "rev_sub":      "Real reviews from Google Play",
        "cookie_msg":   "We use essential cookies only to keep the site running. No tracking or advertising.",
        "cookie_accept":"Accept",
        "cookie_decline":"Decline",
    },
    "sv": {
        "rev_tag":      "\u2b50 Recensioner",
        "rev_title":    "Vad anv\u00e4ndarna s\u00e4ger",
        "rev_sub":      "Riktiga recensioner fr\u00e5n Google Play",
        "cookie_msg":   "Vi anv\u00e4nder endast n\u00f6dv\u00e4ndiga cookies f\u00f6r att webbplatsen ska fungera. Ingen sp\u00e5rning eller reklam.",
        "cookie_accept":"Acceptera",
        "cookie_decline":"Avvisa",
    },
    "da": {
        "rev_tag":      "\u2b50 Anmeldelser",
        "rev_title":    "Hvad brugerne siger",
        "rev_sub":      "Rigtige anmeldelser fra Google Play",
        "cookie_msg":   "Vi bruger kun n\u00f8dvendige cookies for at holde sitet k\u00f8rende. Ingen sporing eller reklame.",
        "cookie_accept":"Accepter",
        "cookie_decline":"Afvis",
    },
    "fr": {
        "rev_tag":      "\u2b50 Avis",
        "rev_title":    "Ce que disent les utilisateurs",
        "rev_sub":      "Vrais avis Google Play",
        "cookie_msg":   "Nous utilisons uniquement des cookies essentiels au fonctionnement du site. Pas de tra\u00e7age ni de publicit\u00e9.",
        "cookie_accept":"Accepter",
        "cookie_decline":"Refuser",
    },
    "es": {
        "rev_tag":      "\u2b50 Rese\u00f1as",
        "rev_title":    "Lo que dicen los usuarios",
        "rev_sub":      "Rese\u00f1as reales de Google Play",
        "cookie_msg":   "Solo usamos cookies esenciales para el funcionamiento del sitio. Sin rastreo ni publicidad.",
        "cookie_accept":"Aceptar",
        "cookie_decline":"Rechazar",
    },
    "de": {
        "rev_tag":      "\u2b50 Bewertungen",
        "rev_title":    "Was Nutzer sagen",
        "rev_sub":      "Echte Bewertungen von Google Play",
        "cookie_msg":   "Wir verwenden nur notwendige Cookies f\u00fcr den Betrieb der Website. Kein Tracking, keine Werbung.",
        "cookie_accept":"Akzeptieren",
        "cookie_decline":"Ablehnen",
    },
    "it": {
        "rev_tag":      "\u2b50 Recensioni",
        "rev_title":    "Cosa dicono gli utenti",
        "rev_sub":      "Recensioni reali da Google Play",
        "cookie_msg":   "Usiamo solo cookie essenziali per il funzionamento del sito. Nessun tracciamento o pubblicit\u00e0.",
        "cookie_accept":"Accetta",
        "cookie_decline":"Rifiuta",
    },
    "pt": {
        "rev_tag":      "\u2b50 Avalia\u00e7\u00f5es",
        "rev_title":    "O que os usu\u00e1rios dizem",
        "rev_sub":      "Avalia\u00e7\u00f5es reais do Google Play",
        "cookie_msg":   "Usamos apenas cookies essenciais para o funcionamento do site. Sem rastreamento ou publicidade.",
        "cookie_accept":"Aceitar",
        "cookie_decline":"Recusar",
    },
    "nl": {
        "rev_tag":      "\u2b50 Beoordelingen",
        "rev_title":    "Wat gebruikers zeggen",
        "rev_sub":      "Echte beoordelingen van Google Play",
        "cookie_msg":   "We gebruiken alleen essenti\u00eble cookies voor de werking van de site. Geen tracking of advertenties.",
        "cookie_accept":"Accepteren",
        "cookie_decline":"Weigeren",
    },
    "ru": {
        "rev_tag":      "\u2b50 \u041e\u0442\u0437\u044b\u0432\u044b",
        "rev_title":    "\u0427\u0442\u043e \u0433\u043e\u0432\u043e\u0440\u044f\u0442 \u043f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u0435\u043b\u0438",
        "rev_sub":      "\u041d\u0430\u0441\u0442\u043e\u044f\u0449\u0438\u0435 \u043e\u0442\u0437\u044b\u0432\u044b \u0432 Google Play",
        "cookie_msg":   "\u041c\u044b \u0438\u0441\u043f\u043e\u043b\u044c\u0437\u0443\u0435\u043c \u0442\u043e\u043b\u044c\u043a\u043e \u043d\u0435\u043e\u0431\u0445\u043e\u0434\u0438\u043c\u044b\u0435 \u0444\u0430\u0439\u043b\u044b cookie \u0434\u043b\u044f \u0440\u0430\u0431\u043e\u0442\u044b \u0441\u0430\u0439\u0442\u0430. \u0411\u0435\u0437 \u043e\u0442\u0441\u043b\u0435\u0436\u0438\u0432\u0430\u043d\u0438\u044f \u0438 \u0440\u0435\u043a\u043b\u0430\u043c\u044b.",
        "cookie_accept":"\u041f\u0440\u0438\u043d\u044f\u0442\u044c",
        "cookie_decline":"\u041e\u0442\u043a\u043b\u043e\u043d\u0438\u0442\u044c",
    },
    "pl": {
        "rev_tag":      "\u2b50 Recenzje",
        "rev_title":    "Co m\u00f3wi\u0105 u\u017cytkownicy",
        "rev_sub":      "Prawdziwe recenzje z Google Play",
        "cookie_msg":   "U\u017cywamy tylko niezb\u0119dnych plik\u00f3w cookie do dzia\u0142ania strony. Bez \u015bledzenia i reklam.",
        "cookie_accept":"Akceptuj",
        "cookie_decline":"Odrzuc",
    },
    "fi": {
        "rev_tag":      "\u2b50 Arvostelut",
        "rev_title":    "Mit\u00e4 k\u00e4ytt\u00e4j\u00e4t sanovat",
        "rev_sub":      "Aidot arvostelut Google Playsta",
        "cookie_msg":   "K\u00e4yt\u00e4mme vain v\u00e4ltt\u00e4m\u00e4tt\u00f6mi\u00e4 ev\u00e4steit\u00e4 sivuston toimintaa varten. Ei seurantaa tai mainoksia.",
        "cookie_accept":"Hyv\u00e4ksy",
        "cookie_decline":"Hylk\u00e4\u00e4",
    },
    "tr": {
        "rev_tag":      "\u2b50 De\u011flendirmeler",
        "rev_title":    "Kullan\u0131c\u0131lar ne diyor",
        "rev_sub":      "Google Play'den ger\u00e7ek de\u011flendirmeler",
        "cookie_msg":   "Yaln\u0131zca sitenin \u00e7al\u0131\u015fmas\u0131 i\u00e7in gerekli \u00e7erezleri kullan\u0131yoruz. \u0130zleme veya reklam yok.",
        "cookie_accept":"Kabul Et",
        "cookie_decline":"Reddet",
    },
    "ko": {
        "rev_tag":      "\u2b50 \ub9ac\ubdf0",
        "rev_title":    "\uc0ac\uc6a9\uc790\ub4e4\uc758 \uc774\uc57c\uae30",
        "rev_sub":      "Google Play\uc758 \uc2e4\uc81c \ub9ac\ubdf0",
        "cookie_msg":   "\uc0ac\uc774\ud2b8 \uc6b4\uc601\uc5d0 \ud544\uc218\uc801\uc778 \ucfe0\ud0a4\ub9cc \uc0ac\uc6a9\ud569\ub2c8\ub2e4. \ucd94\uc801\uc774\ub098 \uad11\uace0 \uc5c6\uc74c.",
        "cookie_accept":"\uc218\ub77d",
        "cookie_decline":"\uac70\ubd80",
    },
    "ja": {
        "rev_tag":      "\u2b50 \u30ec\u30d3\u30e5\u30fc",
        "rev_title":    "\u30e6\u30fc\u30b6\u30fc\u306e\u58f0",
        "rev_sub":      "Google Play\u306e\u30ea\u30a2\u30eb\u30ec\u30d3\u30e5\u30fc",
        "cookie_msg":   "\u30b5\u30a4\u30c8\u306e\u52d5\u4f5c\u306b\u5fc5\u8981\u306a\u30af\u30c3\u30ad\u30fc\u306e\u307f\u4f7f\u7528\u3057\u307e\u3059\u3002\u30c8\u30e9\u30c3\u30ad\u30f3\u30b0\u3084\u5e83\u544a\u306f\u3042\u308a\u307e\u305b\u3093\u3002",
        "cookie_accept":"\u627f\u8a8d",
        "cookie_decline":"\u62d2\u5426",
    },
    "zh-Hans": {
        "rev_tag":      "\u2b50 \u8bc4\u4ef7",
        "rev_title":    "\u7528\u6237\u600e\u4e48\u8bf4",
        "rev_sub":      "Google Play \u771f\u5b9e\u8bc4\u4ef7",
        "cookie_msg":   "\u6211\u4eec\u4ec5\u4f7f\u7528\u7f51\u7ad9\u8fd0\u884c\u6240\u5fc5\u9700\u7684 Cookie\uff0c\u4e0d\u8fdb\u884c\u8ffd\u8e2a\u6216\u5e7f\u544a\u3002",
        "cookie_accept":"\u63a5\u53d7",
        "cookie_decline":"\u62d2\u7edd",
    },
    "zh-Hant": {
        "rev_tag":      "\u2b50 \u8a55\u50f9",
        "rev_title":    "\u7528\u6236\u600e\u9ebc\u8aaa",
        "rev_sub":      "Google Play \u771f\u5be6\u8a55\u50f9",
        "cookie_msg":   "\u6211\u5011\u50c5\u4f7f\u7528\u7db2\u7ad9\u904b\u884c\u6240\u5fc5\u9700\u7684 Cookie\uff0c\u4e0d\u9032\u884c\u8ffd\u8e64\u6216\u5ee3\u544a\u3002",
        "cookie_accept":"\u63a5\u53d7",
        "cookie_decline":"\u62d2\u7d55",
    },
    "hi": {
        "rev_tag":      "\u2b50 \u0938\u092e\u0940\u0915\u094d\u0937\u093e\u090f\u0902",
        "rev_title":    "\u0909\u092a\u092f\u094b\u0917\u0915\u0930\u094d\u0924\u093e \u0915\u094d\u092f\u093e \u0915\u0939\u0924\u0947 \u0939\u0948\u0902",
        "rev_sub":      "Google Play \u0915\u0940 \u0935\u093e\u0938\u094d\u0924\u0935\u093f\u0915 \u0938\u092e\u0940\u0915\u094d\u0937\u093e\u090f\u0902",
        "cookie_msg":   "\u0939\u092e \u0915\u0947\u0935\u0932 \u0906\u0935\u0936\u094d\u092f\u0915 \u0915\u0941\u0915\u0940\u091c \u0915\u093e \u0909\u092a\u092f\u094b\u0917 \u0915\u0930\u0924\u0947 \u0939\u0948\u0902\u0964 \u0915\u094b\u0908 \u091f\u094d\u0930\u0948\u0915\u093f\u0902\u0917 \u092f\u093e \u0935\u093f\u091c\u094d\u091e\u093e\u092a\u0928 \u0928\u0939\u0940\u0902\u0964",
        "cookie_accept":"\u0938\u094d\u0935\u0940\u0915\u093e\u0930 \u0915\u0930\u0947\u0902",
        "cookie_decline":"\u0905\u0938\u094d\u0935\u0940\u0915\u093e\u0930",
    },
    "ar": {
        "rev_tag":      "\u2b50 \u0627\u0644\u062a\u0642\u064a\u064a\u0645\u0627\u062a",
        "rev_title":    "\u0645\u0627\u0630\u0627 \u064a\u0642\u0648\u0644 \u0627\u0644\u0645\u0633\u062a\u062e\u062f\u0645\u0648\u0646",
        "rev_sub":      "\u062a\u0642\u064a\u064a\u0645\u0627\u062a \u062d\u0642\u064a\u0642\u064a\u0629 \u0645\u0646 Google Play",
        "cookie_msg":   "\u0646\u0633\u062a\u062e\u062f\u0645 \u0641\u0642\u0637 \u0645\u0644\u0641\u0627\u062a \u062a\u0639\u0631\u064a\u0641 \u0627\u0644\u0627\u0631\u062a\u0628\u0627\u0637 \u0627\u0644\u0636\u0631\u0648\u0631\u064a\u0629 \u0644\u062a\u0634\u063a\u064a\u0644 \u0627\u0644\u0645\u0648\u0642\u0639. \u0644\u0627 \u062a\u062a\u0628\u0639 \u0648\u0644\u0627 \u0625\u0639\u0644\u0627\u0646\u0627\u062a.",
        "cookie_accept":"\u0642\u0628\u0648\u0644",
        "cookie_decline":"\u0631\u0641\u0636",
    },
    "th": {
        "rev_tag":      "\u2b50 \u0e23\u0e35\u0e27\u0e34\u0e27",
        "rev_title":    "\u0e1c\u0e39\u0e49\u0e43\u0e0a\u0e49\u0e1e\u0e39\u0e14\u0e2d\u0e30\u0e44\u0e23",
        "rev_sub":      "\u0e23\u0e35\u0e27\u0e34\u0e27\u0e08\u0e23\u0e34\u0e07\u0e08\u0e32\u0e01 Google Play",
        "cookie_msg":   "\u0e40\u0e23\u0e32\u0e43\u0e0a\u0e49\u0e04\u0e38\u0e01\u0e01\u0e35\u0e49\u0e40\u0e09\u0e1e\u0e32\u0e30\u0e17\u0e35\u0e48\u0e08\u0e33\u0e40\u0e1b\u0e47\u0e19\u0e2a\u0e33\u0e2b\u0e23\u0e31\u0e1a\u0e01\u0e32\u0e23\u0e17\u0e33\u0e07\u0e32\u0e19\u0e02\u0e2d\u0e07\u0e40\u0e27\u0e47\u0e1a\u0e44\u0e0b\u0e15\u0e4c \u0e44\u0e21\u0e48\u0e21\u0e35\u0e01\u0e32\u0e23\u0e15\u0e34\u0e14\u0e15\u0e32\u0e21\u0e2b\u0e23\u0e37\u0e2d\u0e42\u0e06\u0e29\u0e13\u0e32",
        "cookie_accept":"\u0e22\u0e2d\u0e21\u0e23\u0e31\u0e1a",
        "cookie_decline":"\u0e1b\u0e0f\u0e34\u0e40\u0e2a\u0e18",
    },
    "id": {
        "rev_tag":      "\u2b50 Ulasan",
        "rev_title":    "Kata pengguna",
        "rev_sub":      "Ulasan nyata dari Google Play",
        "cookie_msg":   "Kami hanya menggunakan cookie penting untuk pengoperasian situs. Tidak ada pelacakan atau iklan.",
        "cookie_accept":"Terima",
        "cookie_decline":"Tolak",
    },
    "lt": {
        "rev_tag":      "\u2b50 Atsiliepimai",
        "rev_title":    "K\u0105 sako vartotojai",
        "rev_sub":      "Tikri atsiliepimai i\u0161 Google Play",
        "cookie_msg":   "Naudojame tik b\u016btinus slapukus svetain\u0117s veikimui. Joki\u0173 steb\u0117jim\u0173 ar reklamos.",
        "cookie_accept":"Priimti",
        "cookie_decline":"Atsisakyti",
    },
}

def make_replacer(nv):
    def r(m): return m.group(1) + nv + m.group(3)
    return r

inserted_total = 0
for lang, keys in new_keys.items():
    lp = rf'("{re.escape(lang)}":\s*\{{)(.*?)(?=\n  "[a-z]{{2,7}}":\s*\{{|\n\}};)'
    lm = re.search(lp, content, re.DOTALL)
    if not lm:
        print(f"  WARN: no block for {lang}")
        continue
    bs, be = lm.start(), lm.end()
    block = content[bs:be]
    for key, val in keys.items():
        kp = rf'("{re.escape(key)}":\s*")([^"]*?)(")'
        if re.search(kp, block):
            block = re.sub(kp, make_replacer(val), block, count=1)
        else:
            last = list(re.finditer(r'(\s+"[^"]+": "[^"]*")', block))
            if last:
                lmk = last[-1]
                block = block[:lmk.end()] + f',\n    "{key}": "{val}"' + block[lmk.end():]
                inserted_total += 1
    content = content[:bs] + block + content[be:]

with open(i18n_path, 'w', encoding='utf-8') as f:
    f.write(content)
print(f"i18n.js updated ({inserted_total} new keys inserted).")


# ─────────────────────────────────────────────
# Part 2: Add reviews section + cookie banner to index.html
# ─────────────────────────────────────────────
idx_path = '/sessions/wizardly-pensive-albattani/mnt/outputs/index.html'
with open(idx_path, 'r', encoding='utf-8') as f:
    html = f.read()

# --- CSS to inject (before closing </style>) ---
reviews_css = """
    /* ── Reviews ── */
    .reviews-section{background:var(--cream)}
    .reviews-grid{display:grid;grid-template-columns:1fr 1fr;gap:1.5rem;max-width:800px;margin:0 auto}
    .review-card{background:var(--white);border:1px solid var(--border);border-radius:var(--radius);padding:1.75rem 2rem;position:relative;transition:box-shadow .3s}
    .review-card:hover{box-shadow:var(--shadow-md)}
    .review-stars{color:#F59E0B;font-size:1.15rem;letter-spacing:.08em;margin-bottom:.85rem}
    .review-quote{font-size:.98rem;color:var(--charcoal);font-style:italic;line-height:1.75;margin-bottom:1.1rem}
    .review-author{font-weight:700;font-size:.9rem;color:var(--green-dark)}
    .review-meta{font-size:.78rem;color:var(--slate);margin-top:.2rem}
    .review-badge{display:inline-flex;align-items:center;gap:.35rem;font-size:.75rem;font-weight:600;color:var(--slate);background:var(--cream);border:1px solid var(--border);border-radius:2rem;padding:.2rem .65rem;margin-top:.6rem}
    @media(max-width:600px){.reviews-grid{grid-template-columns:1fr}}

    /* ── Cookie banner ── */
    .cookie-banner{display:none;position:fixed;bottom:0;left:0;right:0;background:#1C1C1C;color:rgba(255,255,255,.9);padding:.9rem 1.5rem;z-index:300;box-shadow:0 -4px 20px rgba(0,0,0,.25)}
    .cookie-banner.show{display:block}
    .cookie-inner{max-width:1140px;margin:0 auto;display:flex;align-items:center;gap:1rem;flex-wrap:wrap}
    .cookie-text{flex:1;font-size:.85rem;line-height:1.5;min-width:200px}
    .cookie-text a{color:#6BAF7D;text-decoration:underline}
    .cookie-btns{display:flex;gap:.5rem;flex-shrink:0}
    .cookie-accept{padding:.45rem 1.2rem;background:var(--green);color:#fff;border:none;border-radius:2rem;font-weight:600;font-size:.85rem;cursor:pointer;transition:background .2s;font-family:inherit}
    .cookie-accept:hover{background:#2D5A3D}
    .cookie-decline{padding:.45rem .9rem;background:transparent;color:rgba(255,255,255,.65);border:1px solid rgba(255,255,255,.3);border-radius:2rem;font-size:.85rem;cursor:pointer;transition:all .2s;font-family:inherit}
    .cookie-decline:hover{color:#fff;border-color:rgba(255,255,255,.65)}
    @media(max-width:560px){.cookie-inner{flex-direction:column;align-items:flex-start}.cookie-btns{width:100%}.cookie-accept,.cookie-decline{flex:1;text-align:center}}"""

html = html.replace('  </style>', reviews_css + '\n  </style>', 1)

# --- Reviews section HTML (insert after stats-bar, before features section) ---
reviews_html = """
  <section class="reviews-section"><div class="container text-center">
    <div class="reveal"><span class="section-tag" data-i18n="rev_tag">\u2b50 Reviews</span><h2 class="section-title" data-i18n="rev_title">What users say</h2><p class="section-sub" data-i18n="rev_sub">Real reviews from Google Play</p></div>
    <div class="reviews-grid">
      <div class="review-card reveal reveal-d1">
        <div class="review-stars">\u2605\u2605\u2605\u2605\u2605</div>
        <p class="review-quote">\u201cimponerende f\u00f8rsteinntrykk \u2013 denne kommer jeg til \u00e5 bruke mye!\u201d</p>
        <div class="review-author">Christoffer S.</div>
        <div class="review-meta">Samsung Galaxy S24</div>
        <div class="review-badge"><svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg> Google Play</div>
      </div>
      <div class="review-card reveal reveal-d2">
        <div class="review-stars">\u2605\u2605\u2605\u2605\u2605</div>
        <p class="review-quote">\u201cI really like this app! Easy to navigate.\u201d</p>
        <div class="review-author">Gouled Y.</div>
        <div class="review-meta">Motorola moto e13</div>
        <div class="review-badge"><svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg> Google Play</div>
      </div>
    </div>
  </div></section>"""

html = html.replace(
    '\n  <section id="features"',
    reviews_html + '\n  <section id="features"',
    1
)

# --- Cookie banner HTML (before </body>) ---
cookie_html = """
  <!-- Cookie banner -->
  <div class="cookie-banner" id="cookieBanner">
    <div class="cookie-inner">
      <p class="cookie-text" data-i18n="cookie_msg">We use essential cookies only to keep the site running. No tracking or advertising. <a href="privacypolicy.html" data-i18n-href>Privacy policy</a></p>
      <div class="cookie-btns">
        <button class="cookie-accept" id="cookieAccept" data-i18n="cookie_accept">Accept</button>
        <button class="cookie-decline" id="cookieDecline" data-i18n="cookie_decline">Decline</button>
      </div>
    </div>
  </div>"""

cookie_js = """
    // Cookie consent
    (function(){
      var b=document.getElementById('cookieBanner');
      if(!b)return;
      try{if(localStorage.getItem('cookieConsent'))return;}catch(e){}
      b.classList.add('show');
      document.getElementById('cookieAccept').addEventListener('click',function(){
        try{localStorage.setItem('cookieConsent','accepted');}catch(e){}
        b.classList.remove('show');
      });
      document.getElementById('cookieDecline').addEventListener('click',function(){
        try{localStorage.setItem('cookieConsent','declined');}catch(e){}
        b.classList.remove('show');
      });
    })();"""

html = html.replace('</body>', cookie_html + '\n  <script>' + cookie_js + '\n  </script>\n</body>', 1)

with open(idx_path, 'w', encoding='utf-8') as f:
    f.write(html)
print("index.html updated with reviews + cookie banner.")


# ─────────────────────────────────────────────
# Part 3: Add cookie banner to remaining 5 HTML files
# ─────────────────────────────────────────────
other_files = [
    '/sessions/wizardly-pensive-albattani/mnt/outputs/manual.html',
    '/sessions/wizardly-pensive-albattani/mnt/outputs/about.html',
    '/sessions/wizardly-pensive-albattani/mnt/outputs/delete.html',
    '/sessions/wizardly-pensive-albattani/mnt/outputs/privacypolicy.html',
    '/sessions/wizardly-pensive-albattani/mnt/outputs/termsandconditions.html',
]

cookie_css_minimal = """
    .cookie-banner{display:none;position:fixed;bottom:0;left:0;right:0;background:#1C1C1C;color:rgba(255,255,255,.9);padding:.9rem 1.5rem;z-index:300;box-shadow:0 -4px 20px rgba(0,0,0,.25)}
    .cookie-banner.show{display:block}
    .cookie-inner{max-width:1140px;margin:0 auto;display:flex;align-items:center;gap:1rem;flex-wrap:wrap}
    .cookie-text{flex:1;font-size:.85rem;line-height:1.5;min-width:200px}
    .cookie-text a{color:#6BAF7D;text-decoration:underline}
    .cookie-btns{display:flex;gap:.5rem;flex-shrink:0}
    .cookie-accept{padding:.45rem 1.2rem;background:#4D7C5B;color:#fff;border:none;border-radius:2rem;font-weight:600;font-size:.85rem;cursor:pointer;font-family:inherit}
    .cookie-accept:hover{background:#2D5A3D}
    .cookie-decline{padding:.45rem .9rem;background:transparent;color:rgba(255,255,255,.65);border:1px solid rgba(255,255,255,.3);border-radius:2rem;font-size:.85rem;cursor:pointer;font-family:inherit}
    .cookie-decline:hover{color:#fff;border-color:rgba(255,255,255,.65)}
    @media(max-width:560px){.cookie-inner{flex-direction:column;align-items:flex-start}.cookie-btns{width:100%}.cookie-accept,.cookie-decline{flex:1;text-align:center}}"""

for path in other_files:
    with open(path, 'r', encoding='utf-8') as f:
        h = f.read()
    if 'cookieBanner' in h:
        print(f"  skip (already has banner): {os.path.basename(path)}")
        continue
    h = h.replace('  </style>', cookie_css_minimal + '\n  </style>', 1)
    h = h.replace('</body>', cookie_html + '\n  <script>' + cookie_js + '\n  </script>\n</body>', 1)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(h)
    print(f"  cookie banner added: {os.path.basename(path)}")

print("All done.")
