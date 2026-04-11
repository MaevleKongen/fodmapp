import re, os

# ── Part 1: Update hero_p + feat_sub in i18n.js (knips/snap instead of pek/point) ──

i18n_path = '/sessions/wizardly-pensive-albattani/mnt/outputs/js/i18n.js'
with open(i18n_path, 'r', encoding='utf-8') as f:
    content = f.read()

updates = {
    "nb": {
        "hero_p":   "Ikke mer googling. Ikke mer pinlige \u00f8yeblikk p\u00e5 restaurant. Bare knips, skann eller sp\u00f8r \u2013 og spis uten frykt.",
        "feat_sub": "Over 4,4 millioner produkter \u2013 der hvert ingrediens analyseres av AI. Ingen gjetting, ingen leting. Bare knips, skann eller sp\u00f8r.",
    },
    "en": {
        "hero_p":   "No more googling. No more embarrassing moments at restaurants. Just snap a photo, scan, or ask \u2014 and eat without fear.",
        "feat_sub": "Over 4.4 million products \u2013 every ingredient analyzed by AI. No guessing, no searching. Just snap a photo, scan, or ask.",
    },
    "sv": {
        "hero_p":   "Sluta googla. Inga fler pinsamma stunder p\u00e5 restaurangen. Bara ta en bild, skanna eller fr\u00e5ga \u2013 och \u00e4t utan r\u00e4dsla.",
        "feat_sub": "\u00d6ver 4,4 miljoner produkter \u2013 varje ingrediens analyseras av AI. Ingen gissning, ingen s\u00f6kning. Bara ta en bild, skanna eller fr\u00e5ga.",
    },
    "da": {
        "hero_p":   "Ikke mere googling. Ikke mere pinlige \u00f8jeblikke p\u00e5 restaurant. Bare knips, scan eller sp\u00f8rg \u2013 og spis uden frygt.",
        "feat_sub": "Over 4,4 millioner produkter \u2013 hvert ingrediens analyseres af AI. Ingen g\u00e6tteri, ingen s\u00f8gning. Bare knips, scan eller sp\u00f8rg.",
    },
    "fr": {
        "hero_p":   "Fini de googler. Fini les moments g\u00eanants au restaurant. Photographiez, scannez ou demandez \u2014 et mangez sans crainte.",
        "feat_sub": "Plus de 4,4 millions de produits \u2013 chaque ingr\u00e9dient analys\u00e9 par l'IA. Z\u00e9ro devinette, z\u00e9ro recherche. Photographiez, scannez ou demandez.",
    },
    "es": {
        "hero_p":   "Nada m\u00e1s de buscar en Google. Nada m\u00e1s de momentos inc\u00f3modos en restaurantes. Fotograf\u00eda, escanea o pregunta \u2014 y come sin miedo.",
        "feat_sub": "M\u00e1s de 4,4 millones de productos \u2013 cada ingrediente analizado por IA. Sin adivinar, sin buscar. Solo fotograf\u00eda, escanea o pregunta.",
    },
    "de": {
        "hero_p":   "Kein Googeln mehr. Keine peinlichen Momente im Restaurant mehr. Fotografiere, scann oder frag \u2013 und iss ohne Angst.",
        "feat_sub": "\u00dcber 4,4 Millionen Produkte \u2013 jede Zutat analysiert von KI. Kein Raten, kein Suchen. Fotografiere, scann oder frag.",
    },
    "it": {
        "hero_p":   "Niente pi\u00f9 ricerche su Google. Niente pi\u00f9 momenti imbarazzanti al ristorante. Scatta una foto, scansiona o chiedi \u2014 e mangia senza paura.",
        "feat_sub": "Oltre 4,4 milioni di prodotti \u2013 ogni ingrediente analizzato dall'IA. Nessuna supposizione, nessuna ricerca. Scatta una foto, scansiona o chiedi.",
    },
    "pt": {
        "hero_p":   "Chega de pesquisar no Google. Chega de momentos constrangedores em restaurantes. Fotografe, escaneie ou pergunte \u2014 e coma sem medo.",
        "feat_sub": "Mais de 4,4 milh\u00f5es de produtos \u2013 cada ingrediente analisado por IA. Sem adivinha\u00e7\u00e3o, sem pesquisa. Fotografe, escaneie ou pergunte.",
    },
    "nl": {
        "hero_p":   "Geen gegoogle meer. Geen g\u00eanante momenten meer in restaurants. Maak een foto, scan of vraag \u2014 en eet zonder angst.",
        "feat_sub": "Meer dan 4,4 miljoen producten \u2013 elk ingredi\u00ebnt geanalyseerd door AI. Geen giswerk, geen zoeken. Maak een foto, scan of vraag.",
    },
    "ru": {
        "hero_p":   "\u0411\u043e\u043b\u044c\u0448\u0435 \u043d\u0438\u043a\u0430\u043a\u0438\u0445 \u043f\u043e\u0438\u0441\u043a\u043e\u0432 \u0432 Google. \u0411\u043e\u043b\u044c\u0448\u0435 \u043d\u0438\u043a\u0430\u043a\u0438\u0445 \u043d\u0435\u043b\u043e\u0432\u043a\u0438\u0445 \u043c\u043e\u043c\u0435\u043d\u0442\u043e\u0432 \u0432 \u0440\u0435\u0441\u0442\u043e\u0440\u0430\u043d\u0430\u0445. \u041f\u0440\u043e\u0441\u0442\u043e \u0441\u0444\u043e\u0442\u043e\u0433\u0440\u0430\u0444\u0438\u0440\u0443\u0439, \u043e\u0442\u0441\u043a\u0430\u043d\u0438\u0440\u0443\u0439 \u0438\u043b\u0438 \u0441\u043f\u0440\u043e\u0441\u0438 \u2014 \u0438 \u0435\u0448\u044c \u0431\u0435\u0437 \u0441\u0442\u0440\u0430\u0445\u0430.",
        "feat_sub": "\u0411\u043e\u043b\u0435\u0435 4,4 \u043c\u0438\u043b\u043b\u0438\u043e\u043d\u0430 \u043f\u0440\u043e\u0434\u0443\u043a\u0442\u043e\u0432 \u2013 \u043a\u0430\u0436\u0434\u044b\u0439 \u0438\u043d\u0433\u0440\u0435\u0434\u0438\u0435\u043d\u0442 \u0430\u043d\u0430\u043b\u0438\u0437\u0438\u0440\u0443\u0435\u0442\u0441\u044f \u0418\u0418. \u041d\u0438\u043a\u0430\u043a\u043e\u0433\u043e \u0443\u0433\u0430\u0434\u044b\u0432\u0430\u043d\u0438\u044f, \u043d\u0438\u043a\u0430\u043a\u0438\u0445 \u043f\u043e\u0438\u0441\u043a\u043e\u0432. \u0421\u0444\u043e\u0442\u043e\u0433\u0440\u0430\u0444\u0438\u0440\u0443\u0439, \u043e\u0442\u0441\u043a\u0430\u043d\u0438\u0440\u0443\u0439 \u0438\u043b\u0438 \u0441\u043f\u0440\u043e\u0441\u0438.",
    },
    "pl": {
        "hero_p":   "Koniec z googlowaniem. Koniec z kr\u0119puj\u0105cymi chwilami w restauracjach. Sfotografuj, zeskanuj lub zapytaj \u2014 i jedz bez obaw.",
        "feat_sub": "Ponad 4,4 miliona produkt\u00f3w \u2013 ka\u017cdy sk\u0142adnik analizowany przez AI. \u017badnego zgadywania, \u017cadnego szukania. Sfotografuj, zeskanuj lub zapytaj.",
    },
    "fi": {
        "hero_p":   "Ei en\u00e4\u00e4 googlettamista. Ei en\u00e4\u00e4 kiusallisia hetki\u00e4 ravintoloissa. Ota kuva, skannaa tai kysy \u2014 ja sy\u00f6 ilman pelkoa.",
        "feat_sub": "Yli 4,4 miljoonaa tuotetta \u2013 jokainen ainesosa analysoitu teko\u00e4lyll\u00e4. Ei arvausta, ei etsimist\u00e4. Ota kuva, skannaa tai kysy.",
    },
    "tr": {
        "hero_p":   "Art\u0131k Google'da arama yok. Art\u0131k restoranlarda utan\u00e7 verici anlar yok. Foto\u011frafla, tara ya da sor \u2014 ve korkusuzca ye.",
        "feat_sub": "4,4 milyonun \u00fczerinde \u00fcr\u00fcn \u2013 her i\u00e7erik yapay zeka taraf\u0131ndan analiz edilir. Tahmin yok, arama yok. Foto\u011frafla, tara ya da sor.",
    },
    "ko": {
        "hero_p":   "\ub354 \uc774\uc0c1 \uad6c\uae00 \uac80\uc0c9 \uc5c6\uc774. \ub354 \uc774\uc0c1 \uc2dd\ub2f9\uc5d0\uc11c\uc758 \ub2f9\ud669\uc2a4\ub7ec\uc6b4 \uc21c\uac04 \uc5c6\uc774. \uc0ac\uc9c4\uc744 \ucc0d\uac70\ub098, \uc2a4\uce94\ud558\uac70\ub098, \ubb3c\uc5b4\ubcf4\uc138\uc694 \u2014 \ub450\ub824\uc6c0 \uc5c6\uc774 \ub4dc\uc138\uc694.",
        "feat_sub": "440\ub9cc \uac1c \uc774\uc0c1\uc758 \uc81c\ud488 \u2013 \ubaa8\ub4e0 \uc131\ubd84\uc744 AI\uac00 \ubd84\uc11d\ud569\ub2c8\ub2e4. \ucd94\uce21\ub3c4 \uc5c6\uace0, \uac80\uc0c9\ub3c4 \uc5c6\uc774. \uc0ac\uc9c4\uc744 \ucc0d\uac70\ub098, \uc2a4\uce94\ud558\uac70\ub098, \ubb3c\uc5b4\ubcf4\uc138\uc694.",
    },
    "ja": {
        "hero_p":   "\u3082\u3046Google\u3067\u8abf\u3079\u306a\u304f\u3066\u3044\u3044\u3002\u3082\u3046\u30ec\u30b9\u30c8\u30e9\u30f3\u3067\u6c17\u307e\u305a\u3044\u601d\u3044\u3092\u3057\u306a\u304f\u3066\u3044\u3044\u3002\u5199\u771f\u3092\u64ae\u3063\u3066\u3001\u30b9\u30ad\u30e3\u30f3\u3057\u3066\u3001\u307e\u305f\u306f\u805e\u3044\u3066 \u2014 \u6050\u308c\u305a\u306b\u98df\u3079\u3088\u3046\u3002",
        "feat_sub": "440\u4e07\u4ee5\u4e0a\u306e\u88fd\u54c1 \u2013 \u3059\u3079\u3066\u306e\u6210\u5206\u3092AI\u304c\u5206\u6790\u3057\u307e\u3059\u3002\u63a8\u6e2c\u306a\u3057\u3001\u691c\u7d22\u306a\u3057\u3002\u5199\u771f\u3092\u64ae\u3063\u3066\u3001\u30b9\u30ad\u30e3\u30f3\u3057\u3066\u3001\u307e\u305f\u306f\u805e\u3044\u3066\u3002",
    },
    "zh-Hans": {
        "hero_p":   "\u4e0d\u518d\u9700\u8981\u641c\u7d22\u5f15\u64ce\u3002\u4e0d\u518d\u6709\u5728\u9910\u5385\u5c34\u5c2c\u7684\u65f6\u523b\u3002\u53ea\u9700\u62cd\u7167\u3001\u626b\u63cf\u6216\u8be2\u95ee\u2014\u2014\u65e0\u60e7\u996e\u98df\u3002",
        "feat_sub": "\u8d85\u8fc7440\u4e07\u79cd\u4ea7\u54c1\u2014\u2014\u6bcf\u79cd\u6210\u5206\u5747\u7531AI\u5206\u6790\u3002\u65e0\u9700\u731c\u6d4b\uff0c\u65e0\u9700\u641c\u7d22\u3002\u62cd\u7167\u3001\u626b\u63cf\u6216\u8be2\u95ee\u5373\u53ef\u3002",
    },
    "zh-Hant": {
        "hero_p":   "\u4e0d\u518d\u9700\u8981Google\u641c\u5c0b\u3002\u4e0d\u518d\u6709\u5728\u9910\u5ef3\u5c37\u5c2c\u7684\u6642\u523b\u3002\u53ea\u9700\u62cd\u7167\u3001\u6383\u63cf\u6216\u8a62\u554f\u2014\u2014\u7121\u61fc\u98f2\u98df\u3002",
        "feat_sub": "\u8d85\u904e440\u842c\u7a2e\u7522\u54c1\u2014\u2014\u6bcf\u7a2e\u6210\u5206\u5747\u7531AI\u5206\u6790\u3002\u7121\u9700\u731c\u6e2c\uff0c\u7121\u9700\u641c\u5c0b\u3002\u62cd\u7167\u3001\u6383\u63cf\u6216\u8a62\u554f\u5373\u53ef\u3002",
    },
    "hi": {
        "hero_p":   "\u0905\u092c \u0917\u0942\u0917\u0932 \u092a\u0930 \u0916\u094b\u091c\u0928\u0947 \u0915\u0940 \u091c\u0930\u0942\u0930\u0924 \u0928\u0939\u0940\u0902\u0964 \u0930\u0947\u0938\u094d\u091f\u094b\u0930\u0947\u0902\u091f \u092e\u0947\u0902 \u0936\u0930\u094d\u092e\u0928\u093e\u0915 \u092a\u0932 \u0928\u0939\u0940\u0902\u0964 \u092c\u0938 \u092b\u093c\u094b\u091f\u094b \u0932\u0947\u0902, \u0938\u094d\u0915\u0948\u0928 \u0915\u0930\u0947\u0902 \u092f\u093e \u092a\u0942\u091b\u0947\u0902 \u2014 \u0914\u0930 \u092c\u093f\u0928\u093e \u0921\u0930 \u0915\u0947 \u0916\u093e\u090f\u0902\u0964",
        "feat_sub": "44 \u0932\u093e\u0916 \u0938\u0947 \u0905\u0927\u093f\u0915 \u0909\u0924\u094d\u092a\u093e\u0926 \u2013 \u0939\u0930 \u0938\u093e\u092e\u0917\u094d\u0930\u0940 AI \u0926\u094d\u0935\u093e\u0930\u093e \u0935\u093f\u0936\u094d\u0932\u0947\u0937\u093f\u0924\u0964 \u0915\u094b\u0908 \u0905\u0928\u0941\u092e\u093e\u0928 \u0928\u0939\u0940\u0902, \u0915\u094b\u0908 \u0916\u094b\u091c \u0928\u0939\u0940\u0902\u0964 \u092b\u093c\u094b\u091f\u094b \u0932\u0947\u0902, \u0938\u094d\u0915\u0948\u0928 \u0915\u0930\u0947\u0902 \u092f\u093e \u092a\u0942\u091b\u0947\u0902\u0964",
    },
    "ar": {
        "hero_p":   "\u0644\u0627 \u0645\u0632\u064a\u062f \u0645\u0646 \u0627\u0644\u0628\u062d\u062b \u0641\u064a \u062c\u0648\u062c\u0644. \u0644\u0627 \u0645\u0632\u064a\u062f \u0645\u0646 \u0627\u0644\u0645\u0648\u0627\u0642\u0641 \u0627\u0644\u0645\u062d\u0631\u062c\u0629 \u0641\u064a \u0627\u0644\u0645\u0637\u0627\u0639\u0645. \u0641\u0642\u0637 \u0627\u0644\u062a\u0642\u0637 \u0635\u0648\u0631\u0629\u060c \u0623\u0648 \u0627\u0645\u0633\u062d\u060c \u0623\u0648 \u0627\u0633\u0623\u0644 \u2014 \u0648\u0643\u0644 \u0628\u0644\u0627 \u062e\u0648\u0641.",
        "feat_sub": "\u0623\u0643\u062b\u0631 \u0645\u0646 4.4 \u0645\u0644\u064a\u0648\u0646 \u0645\u0646\u062a\u062c \u2013 \u0643\u0644 \u0645\u0643\u0648\u0646 \u064a\u062d\u0644\u0644\u0647 \u0627\u0644\u0630\u0643\u0627\u0621 \u0627\u0644\u0627\u0635\u0637\u0646\u0627\u0639\u064a. \u0644\u0627 \u062a\u062e\u0645\u064a\u0646\u060c \u0644\u0627 \u0628\u062d\u062b. \u0627\u0644\u062a\u0642\u0637 \u0635\u0648\u0631\u0629\u060c \u0623\u0648 \u0627\u0645\u0633\u062d\u060c \u0623\u0648 \u0627\u0633\u0623\u0644.",
    },
    "th": {
        "hero_p":   "\u0e44\u0e21\u0e48\u0e15\u0e49\u0e2d\u0e07\u0e04\u0e49\u0e19\u0e2b\u0e32 Google \u0e2d\u0e35\u0e01\u0e15\u0e48\u0e2d\u0e44\u0e1b \u0e44\u0e21\u0e48\u0e15\u0e49\u0e2d\u0e07\u0e40\u0e1c\u0e0a\u0e34\u0e0d\u0e01\u0e31\u0e1a\u0e04\u0e27\u0e32\u0e21\u0e2d\u0e36\u0e14\u0e2d\u0e31\u0e14\u0e43\u0e19\u0e23\u0e49\u0e32\u0e19\u0e2d\u0e32\u0e2b\u0e32\u0e23 \u0e40\u0e1e\u0e35\u0e22\u0e07\u0e16\u0e48\u0e32\u0e22\u0e23\u0e39\u0e1b \u0e2a\u0e41\u0e01\u0e19 \u0e2b\u0e23\u0e37\u0e2d\u0e16\u0e32\u0e21 \u2014 \u0e41\u0e25\u0e49\u0e27\u0e01\u0e34\u0e19\u0e42\u0e14\u0e22\u0e44\u0e21\u0e48\u0e15\u0e49\u0e2d\u0e07\u0e01\u0e25\u0e31\u0e27",
        "feat_sub": "\u0e1c\u0e25\u0e34\u0e15\u0e20\u0e31\u0e13\u0e11\u0e4c\u0e21\u0e32\u0e01\u0e01\u0e27\u0e48\u0e32 4.4 \u0e25\u0e49\u0e32\u0e19\u0e23\u0e32\u0e22\u0e01\u0e32\u0e23 \u2013 \u0e17\u0e38\u0e01\u0e2a\u0e48\u0e27\u0e19\u0e1c\u0e2a\u0e21\u0e27\u0e34\u0e40\u0e04\u0e23\u0e32\u0e30\u0e2b\u0e4c\u0e42\u0e14\u0e22 AI \u0e44\u0e21\u0e48\u0e15\u0e49\u0e2d\u0e07\u0e40\u0e14\u0e32 \u0e44\u0e21\u0e48\u0e15\u0e49\u0e2d\u0e07\u0e04\u0e49\u0e19 \u0e40\u0e1e\u0e35\u0e22\u0e07\u0e16\u0e48\u0e32\u0e22\u0e23\u0e39\u0e1b \u0e2a\u0e41\u0e01\u0e19 \u0e2b\u0e23\u0e37\u0e2d\u0e16\u0e32\u0e21",
    },
    "id": {
        "hero_p":   "Tidak perlu lagi googling. Tidak ada lagi momen memalukan di restoran. Ambil foto, pindai, atau tanya \u2014 dan makan tanpa rasa takut.",
        "feat_sub": "Lebih dari 4,4 juta produk \u2013 setiap bahan dianalisis oleh AI. Tanpa tebak-tebakan, tanpa pencarian. Ambil foto, pindai, atau tanya.",
    },
    "lt": {
        "hero_p":   "Nebereikia ie\u0161koti internete. Nebereikia g\u0117dingų akimirk\u0173 restoranuose. Tiesiog fotografuok, nuskenuok arba paklusk \u2014 ir valgyk be baim\u0117s.",
        "feat_sub": "Daugiau nei 4,4 mln. produkt\u0173 \u2013 kiekvien\u0105 ingredient\u0105 analizuoja DI. Jokio sp\u0117liojimo, jokios paie\u0161kos. Fotografuok, nuskenuok arba paklusk.",
    },
}

def make_replacer(nv):
    def replacer(m):
        return m.group(1) + nv + m.group(3)
    return replacer

replaced = 0
for lang, keys in updates.items():
    lang_pattern = rf'("{re.escape(lang)}":\s*\{{)(.*?)(?=\n  "[a-z]{{2,7}}":\s*\{{|\n\}};)'
    lang_match = re.search(lang_pattern, content, re.DOTALL)
    if not lang_match:
        print(f"  WARN: no block for {lang}")
        continue
    bs, be = lang_match.start(), lang_match.end()
    block = content[bs:be]
    for key, new_val in keys.items():
        kp = rf'("{re.escape(key)}":\s*")([^"]*?)(")'
        if re.search(kp, block):
            block = re.sub(kp, make_replacer(new_val), block, count=1)
            replaced += 1
        else:
            last = list(re.finditer(r'(\s+"[^"]+": "[^"]*")', block))
            if last:
                lm = last[-1]
                block = block[:lm.end()] + f',\n    "{key}": "{new_val}"' + block[lm.end():]
                replaced += 1
                print(f"  + inserted {key} into {lang}")
    content = content[:bs] + block + content[be:]

with open(i18n_path, 'w', encoding='utf-8') as f:
    f.write(content)
print(f"i18n.js: {replaced} changes saved.")

# ── Part 2: Update HTML fallback texts ──
html_files = [
    '/sessions/wizardly-pensive-albattani/mnt/outputs/index.html',
    '/sessions/wizardly-pensive-albattani/mnt/outputs/about.html',
    '/sessions/wizardly-pensive-albattani/mnt/outputs/manual.html',
    '/sessions/wizardly-pensive-albattani/mnt/outputs/delete.html',
    '/sessions/wizardly-pensive-albattani/mnt/outputs/privacypolicy.html',
    '/sessions/wizardly-pensive-albattani/mnt/outputs/termsandconditions.html',
]

# Map i18n key -> new English fallback text (shown if JS fails)
html_fallbacks = {
    'hero_p':    'No more googling. No more embarrassing moments at restaurants. Just snap a photo, scan, or ask \u2014 and eat without fear.',
    'feat_sub':  'Over 4.4 million products \u2013 every ingredient analyzed by AI. No guessing, no searching. Just snap a photo, scan, or ask.',
    'cta_title': 'Stop living around your gut.',
    'cta_p':     'Download free. Eat without fear. iOS \u0026 Android \u2013 23 languages.',
}

total_html = 0
for path in html_files:
    if not os.path.exists(path):
        continue
    with open(path, 'r', encoding='utf-8') as f:
        html = f.read()
    original = html
    for key, new_text in html_fallbacks.items():
        # Replace fallback text inside elements with data-i18n="key"
        # Pattern: data-i18n="key">OLD_TEXT<
        pattern = rf'(data-i18n="{re.escape(key)}">)([^<]*?)(<)'
        html = re.sub(pattern, lambda m: m.group(1) + new_text + m.group(3), html)
    if html != original:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(html)
        total_html += 1
        print(f"  HTML updated: {os.path.basename(path)}")

print(f"HTML files updated: {total_html}")
print("All done.")
