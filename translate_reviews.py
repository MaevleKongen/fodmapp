import re, os

# ── Translations for the two review quotes ──
new_keys = {
    "nb": {
        "rev_q1": "imponerende f\u00f8rsteinntrykk \u2013 denne kommer jeg til \u00e5 bruke mye!",
        "rev_q2": "Jeg liker denne appen veldig godt! Lett \u00e5 navigere.",
    },
    "en": {
        "rev_q1": "Impressive first impression \u2013 I\u2019m going to use this a lot!",
        "rev_q2": "I really like this app! Easy to navigate.",
    },
    "sv": {
        "rev_q1": "Imponerande f\u00f6rsta intryck \u2013 den h\u00e4r kommer jag att anv\u00e4nda mycket!",
        "rev_q2": "Jag gillar den h\u00e4r appen verkligen! L\u00e4tt att navigera.",
    },
    "da": {
        "rev_q1": "Imponerende f\u00f8rsteindtryk \u2013 denne kommer jeg til at bruge meget!",
        "rev_q2": "Jeg kan virkelig godt lide denne app! Nem at navigere.",
    },
    "fr": {
        "rev_q1": "Premi\u00e8re impression impressionnante \u2013 je vais beaucoup utiliser cette appli\u00a0!",
        "rev_q2": "J\u2019aime vraiment cette application\u00a0! Facile \u00e0 naviguer.",
    },
    "es": {
        "rev_q1": "\u00a1Primera impresi\u00f3n impresionante \u2013 voy a usar esta aplicaci\u00f3n mucho!",
        "rev_q2": "\u00a1Me gusta mucho esta aplicaci\u00f3n! F\u00e1cil de navegar.",
    },
    "de": {
        "rev_q1": "Beeindruckender erster Eindruck \u2013 diese App werde ich viel nutzen!",
        "rev_q2": "Diese App gef\u00e4llt mir wirklich gut! Einfach zu bedienen.",
    },
    "it": {
        "rev_q1": "Prima impressione impressionante \u2013 la user\u00f2 moltissimo!",
        "rev_q2": "Mi piace davvero questa app! Facile da navigare.",
    },
    "pt": {
        "rev_q1": "Primeira impress\u00e3o impressionante \u2013 vou usar muito este app!",
        "rev_q2": "Gosto muito deste aplicativo! F\u00e1cil de navegar.",
    },
    "nl": {
        "rev_q1": "Indrukwekkende eerste indruk \u2013 deze app ga ik veel gebruiken!",
        "rev_q2": "Ik vind deze app echt geweldig! Makkelijk te navigeren.",
    },
    "ru": {
        "rev_q1": "\u0412\u043f\u0435\u0447\u0430\u0442\u043b\u044f\u044e\u0449\u0435\u0435 \u043f\u0435\u0440\u0432\u043e\u0435 \u0432\u043f\u0435\u0447\u0430\u0442\u043b\u0435\u043d\u0438\u0435 \u2013 \u0431\u0443\u0434\u0443 \u043f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u044c\u0441\u044f \u044d\u0442\u0438\u043c \u043f\u0440\u0438\u043b\u043e\u0436\u0435\u043d\u0438\u0435\u043c \u043c\u043d\u043e\u0433\u043e!",
        "rev_q2": "\u041c\u043d\u0435 \u043e\u0447\u0435\u043d\u044c \u043d\u0440\u0430\u0432\u0438\u0442\u0441\u044f \u044d\u0442\u043e \u043f\u0440\u0438\u043b\u043e\u0436\u0435\u043d\u0438\u0435! \u0423\u0434\u043e\u0431\u043d\u0430\u044f \u043d\u0430\u0432\u0438\u0433\u0430\u0446\u0438\u044f.",
    },
    "pl": {
        "rev_q1": "Imponuj\u0105ce pierwsze wra\u017cenie \u2013 b\u0119d\u0119 tego u\u017cywa\u0107 bardzo cz\u0119sto!",
        "rev_q2": "Bardzo podoba mi si\u0119 ta aplikacja! \u0141atwa w nawigacji.",
    },
    "fi": {
        "rev_q1": "Vaikuttava ensikokemus \u2013 t\u00e4t\u00e4 aion k\u00e4ytt\u00e4\u00e4 paljon!",
        "rev_q2": "Pid\u00e4n t\u00e4st\u00e4 sovelluksesta todella paljon! Helppo navigoida.",
    },
    "tr": {
        "rev_q1": "Etkileyici ilk izlenim \u2013 bunu \u00e7ok kullanaca\u011f\u0131m!",
        "rev_q2": "Bu uygulamas\u0131n\u0131 \u00e7ok be\u011fendim! Kullan\u0131m\u0131 kolay.",
    },
    "ko": {
        "rev_q1": "\uc778\uc0c1\uc801\uc778 \uccab\uc778\uc0c1 \u2013 \uc774 \uc571\uc744 \uc790\uc8fc \uc0ac\uc6a9\ud560 \uac83 \uac19\uc544\uc694!",
        "rev_q2": "\uc774 \uc571\uc774 \uc815\ub9d0 \ub9c8\uc74c\uc5d0 \ub4e4\uc5b4\uc694! \ud0d0\uc0c9\ud558\uae30 \uc27d\uc2b5\ub2c8\ub2e4.",
    },
    "ja": {
        "rev_q1": "\u5370\u8c61\u7684\u306a\u7b2c\u4e00\u5370\u8c61 \u2013 \u3053\u308c\u306f\u3088\u304f\u4f7f\u3044\u305d\u3046\u3067\u3059\uff01",
        "rev_q2": "\u3053\u306e\u30a2\u30d7\u30ea\u304c\u672c\u5f53\u306b\u6c17\u306b\u5165\u3063\u3066\u3044\u307e\u3059\uff01\u30ca\u30d3\u30b2\u30fc\u30c8\u3057\u3084\u3059\u3044\u3002",
    },
    "zh-Hans": {
        "rev_q1": "\u7b2c\u4e00\u5370\u8c61\u975e\u5e38\u4e0d\u9519\u2014\u2014\u6211\u4f1a\u7ecf\u5e38\u4f7f\u7528\u8fd9\u6b3e\u5e94\u7528\uff01",
        "rev_q2": "\u6211\u975e\u5e38\u559c\u6b22\u8fd9\u6b3e\u5e94\u7528\uff01\u5bfc\u822a\u5f88\u65b9\u4fbf\u3002",
    },
    "zh-Hant": {
        "rev_q1": "\u7b2c\u4e00\u5370\u8c61\u975e\u5e38\u597d\u2014\u2014\u6211\u6703\u7d93\u5e38\u4f7f\u7528\u9019\u6b3e\u61c9\u7528\uff01",
        "rev_q2": "\u6211\u975e\u5e38\u559c\u6b61\u9019\u6b3e\u61c9\u7528\uff01\u5c0e\u822a\u5f88\u65b9\u4fbf\u3002",
    },
    "hi": {
        "rev_q1": "\u092a\u094d\u0930\u092d\u093e\u0935\u0936\u093e\u0932\u0940 \u092a\u0939\u0932\u0940 \u091b\u093e\u092a \u2013 \u092e\u0948\u0902 \u0907\u0938\u0947 \u092c\u0939\u0941\u0924 \u0907\u0938\u094d\u0924\u0947\u092e\u093e\u0932 \u0915\u0930\u0928\u0947 \u0935\u093e\u0932\u093e \u0939\u0942\u0901!",
        "rev_q2": "\u092e\u0941\u091d\u0947 \u092f\u0939 \u0910\u092a \u0935\u093e\u0915\u0908 \u092c\u0939\u0941\u0924 \u092a\u0938\u0902\u0926 \u0939\u0948! \u0928\u0947\u0935\u093f\u0917\u0947\u091f \u0915\u0930\u0928\u093e \u0906\u0938\u093e\u0928 \u0939\u0948\u0964",
    },
    "ar": {
        "rev_q1": "\u0627\u0646\u0637\u0628\u0627\u0639 \u0623\u0648\u0644 \u0631\u0627\u0626\u0639 \u2013 \u0633\u0623\u0633\u062a\u062e\u062f\u0645 \u0647\u0630\u0627 \u0627\u0644\u062a\u0637\u0628\u064a\u0642 \u0643\u062b\u064a\u0631\u0627\u064b!",
        "rev_q2": "\u0623\u062d\u0628 \u0647\u0630\u0627 \u0627\u0644\u062a\u0637\u0628\u064a\u0642 \u062c\u062f\u0627\u064b! \u0633\u0647\u0644 \u0627\u0644\u062a\u0635\u0641\u062d.",
    },
    "th": {
        "rev_q1": "\u0e04\u0e27\u0e32\u0e21\u0e1b\u0e23\u0e30\u0e17\u0e31\u0e1a\u0e43\u0e08\u0e41\u0e23\u0e01\u0e17\u0e35\u0e48\u0e19\u0e48\u0e32\u0e17\u0e36\u0e48\u0e07 \u2013 \u0e09\u0e31\u0e19\u0e08\u0e30\u0e43\u0e0a\u0e49\u0e41\u0e2d\u0e1b\u0e19\u0e35\u0e49\u0e1a\u0e48\u0e2d\u0e22\u0e21\u0e32\u0e01!",
        "rev_q2": "\u0e09\u0e31\u0e19\u0e0a\u0e2d\u0e1a\u0e41\u0e2d\u0e1b\u0e19\u0e35\u0e49\u0e21\u0e32\u0e01! \u0e19\u0e33\u0e17\u0e32\u0e07\u0e44\u0e14\u0e49\u0e07\u0e48\u0e32\u0e22",
    },
    "id": {
        "rev_q1": "Kesan pertama yang mengesankan \u2013 saya akan sering menggunakan ini!",
        "rev_q2": "Saya sangat menyukai aplikasi ini! Mudah dinavigasi.",
    },
    "lt": {
        "rev_q1": "\u012espūdingas pirmas \u012esp\u016bdis \u2013 \u0161i\u0105 programėlę naudosiu dažnai!",
        "rev_q2": "Man labai patinka \u0161i programėlė! Lengva naršyti.",
    },
}

# ── Update i18n.js ──
i18n_path = '/sessions/wizardly-pensive-albattani/mnt/outputs/js/i18n.js'
with open(i18n_path, 'r', encoding='utf-8') as f:
    content = f.read()

def make_replacer(nv):
    def r(m): return m.group(1) + nv + m.group(3)
    return r

total = 0
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
                block = block[:last[-1].end()] + f',\n    "{key}": "{val}"' + block[last[-1].end():]
        total += 1
    content = content[:bs] + block + content[be:]

with open(i18n_path, 'w', encoding='utf-8') as f:
    f.write(content)
print(f"i18n.js: {total} review translation keys added.")

# ── Add data-i18n to review quotes in index.html ──
idx_path = '/sessions/wizardly-pensive-albattani/mnt/outputs/index.html'
with open(idx_path, 'r', encoding='utf-8') as f:
    html = f.read()

# Replace hardcoded quote text with data-i18n versions
html = html.replace(
    '<p class="review-quote">\u201cimponerende f\u00f8rsteinntrykk \u2013 denne kommer jeg til \u00e5 bruke mye!\u201d</p>',
    '<p class="review-quote" data-i18n="rev_q1">imponerende f\u00f8rsteinntrykk \u2013 denne kommer jeg til \u00e5 bruke mye!</p>'
)
html = html.replace(
    '<p class="review-quote">\u201cI really like this app! Easy to navigate.\u201d</p>',
    '<p class="review-quote" data-i18n="rev_q2">I really like this app! Easy to navigate.</p>'
)

with open(idx_path, 'w', encoding='utf-8') as f:
    f.write(html)

# Verify
q1_ok = 'data-i18n="rev_q1"' in html
q2_ok = 'data-i18n="rev_q2"' in html
print(f"index.html: rev_q1={'OK' if q1_ok else 'MISSING'}, rev_q2={'OK' if q2_ok else 'MISSING'}")
print("Done.")
