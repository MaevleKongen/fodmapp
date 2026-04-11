import re

path = '/sessions/wizardly-pensive-albattani/mnt/outputs/js/i18n.js'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

updates = {
    "nb": {
        "hero_p":    "Ikke mer googling. Ikke mer pinlige øyeblikk på restaurant. Bare pek, skann eller spør \u2013 og spis uten frykt.",
        "feat_sub":  "Over 4,4 millioner produkter \u2013 der hvert ingrediens analyseres av AI. Ingen gjetting, ingen leting. Bare pek, skann eller spør.",
        "cta_title": "Slutt å leve rundt magen din.",
        "cta_p":     "Last ned gratis. Spis uten frykt. iOS og Android \u2013 23 språk."
    },
    "en": {
        "hero_p":    "No more googling. No more embarrassing moments at restaurants. Just point, scan, or ask \u2014 and eat without fear.",
        "feat_sub":  "Over 4.4 million products \u2013 every ingredient analyzed by AI. No guessing, no searching. Just point, scan, or ask.",
        "cta_title": "Stop living around your gut.",
        "cta_p":     "Download free. Eat without fear. iOS & Android \u2013 23 languages."
    },
    "sv": {
        "hero_p":    "Sluta googla. Inga fler pinsamma stunder på restaurangen. Bara peka, skanna eller fråga \u2013 och ät utan rädsla.",
        "feat_sub":  "Över 4,4 miljoner produkter \u2013 varje ingrediens analyseras av AI. Ingen gissning, ingen sökning. Bara peka, skanna eller fråga.",
        "cta_title": "Sluta leva runt din mage.",
        "cta_p":     "Ladda ner gratis. Ät utan rädsla. iOS & Android \u2013 23 språk."
    },
    "da": {
        "hero_p":    "Ikke mere googling. Ikke mere pinlige øjeblikke på restaurant. Bare peg, scan eller spørg \u2013 og spis uden frygt.",
        "feat_sub":  "Over 4,4 millioner produkter \u2013 hvert ingrediens analyseres af AI. Ingen gætteri, ingen søgning. Bare peg, scan eller spørg.",
        "cta_title": "Stop med at leve rundt din mave.",
        "cta_p":     "Download gratis. Spis uden frygt. iOS og Android \u2013 23 sprog."
    },
    "fr": {
        "hero_p":    "Fini de googler. Fini les moments gênants au restaurant. Pointez, scannez ou demandez \u2014 et mangez sans crainte.",
        "feat_sub":  "Plus de 4,4 millions de produits \u2013 chaque ingrédient analysé par l'IA. Zéro devinette, zéro recherche. Pointez, scannez ou demandez.",
        "cta_title": "Arrêtez de vivre autour de votre ventre.",
        "cta_p":     "Téléchargement gratuit. Mangez sans crainte. iOS & Android \u2013 23 langues."
    },
    "es": {
        "hero_p":    "Nada más de buscar en Google. Nada más de momentos incómodos en restaurantes. Apunta, escanea o pregunta \u2014 y come sin miedo.",
        "feat_sub":  "Más de 4,4 millones de productos \u2013 cada ingrediente analizado por IA. Sin adivinar, sin buscar. Solo apunta, escanea o pregunta.",
        "cta_title": "Deja de vivir alrededor de tu intestino.",
        "cta_p":     "Descarga gratis. Come sin miedo. iOS y Android \u2013 23 idiomas."
    },
    "de": {
        "hero_p":    "Kein Googeln mehr. Keine peinlichen Momente im Restaurant mehr. Zeig, scann oder frag \u2013 und iss ohne Angst.",
        "feat_sub":  "Über 4,4 Millionen Produkte \u2013 jede Zutat analysiert von KI. Kein Raten, kein Suchen. Zeig, scann oder frag.",
        "cta_title": "Hör auf, um deinen Darm herumzuleben.",
        "cta_p":     "Kostenlos herunterladen. Iss ohne Angst. iOS & Android \u2013 23 Sprachen."
    },
    "it": {
        "hero_p":    "Niente più ricerche su Google. Niente più momenti imbarazzanti al ristorante. Punta, scansiona o chiedi \u2014 e mangia senza paura.",
        "feat_sub":  "Oltre 4,4 milioni di prodotti \u2013 ogni ingrediente analizzato dall'IA. Nessuna supposizione, nessuna ricerca. Punta, scansiona o chiedi.",
        "cta_title": "Smetti di vivere attorno al tuo intestino.",
        "cta_p":     "Scarica gratis. Mangia senza paura. iOS & Android \u2013 23 lingue."
    },
    "pt": {
        "hero_p":    "Chega de pesquisar no Google. Chega de momentos constrangedores em restaurantes. Aponte, escaneie ou pergunte \u2014 e coma sem medo.",
        "feat_sub":  "Mais de 4,4 milhões de produtos \u2013 cada ingrediente analisado por IA. Sem adivinhação, sem pesquisa. Aponte, escaneie ou pergunte.",
        "cta_title": "Pare de viver em torno do seu intestino.",
        "cta_p":     "Baixe grátis. Coma sem medo. iOS & Android \u2013 23 idiomas."
    },
    "nl": {
        "hero_p":    "Geen gegoogle meer. Geen gênante momenten meer in restaurants. Wijs, scan of vraag \u2014 en eet zonder angst.",
        "feat_sub":  "Meer dan 4,4 miljoen producten \u2013 elk ingrediënt geanalyseerd door AI. Geen giswerk, geen zoeken. Wijs, scan of vraag.",
        "cta_title": "Stop met leven rondom je darmen.",
        "cta_p":     "Gratis downloaden. Eet zonder angst. iOS & Android \u2013 23 talen."
    },
    "ru": {
        "hero_p":    "Больше никаких поисков в Google. Больше никаких неловких моментов в ресторанах. Просто укажи, отсканируй или спроси \u2014 и ешь без страха.",
        "feat_sub":  "Более 4,4 миллиона продуктов \u2013 каждый ингредиент анализируется ИИ. Никакого угадывания, никаких поисков. Укажи, отсканируй или спроси.",
        "cta_title": "Перестань жить вокруг своего кишечника.",
        "cta_p":     "Скачай бесплатно. Ешь без страха. iOS и Android \u2013 23 языка."
    },
    "pl": {
        "hero_p":    "Koniec z googlowaniem. Koniec z krępującymi chwilami w restauracjach. Wskaż, zeskanuj lub zapytaj \u2014 i jedz bez obaw.",
        "feat_sub":  "Ponad 4,4 miliona produktów \u2013 każdy składnik analizowany przez AI. Żadnego zgadywania, żadnego szukania. Wskaż, zeskanuj lub zapytaj.",
        "cta_title": "Przestań żyć wokół swojego jelita.",
        "cta_p":     "Pobierz za darmo. Jedz bez obaw. iOS & Android \u2013 23 języki."
    },
    "fi": {
        "hero_p":    "Ei enää googlettamista. Ei enää kiusallisia hetkiä ravintoloissa. Osoita, skannaa tai kysy \u2014 ja syö ilman pelkoa.",
        "feat_sub":  "Yli 4,4 miljoonaa tuotetta \u2013 jokainen ainesosa analysoitu tekoälyllä. Ei arvausta, ei etsimistä. Osoita, skannaa tai kysy.",
        "cta_title": "Lopeta suolesi ympärillä eläminen.",
        "cta_p":     "Lataa ilmaiseksi. Syö ilman pelkoa. iOS ja Android \u2013 23 kieltä."
    },
    "tr": {
        "hero_p":    "Artık Google'da arama yok. Artık restoranlarda utanç verici anlar yok. Sadece işaret et, tara ya da sor \u2014 ve korkusuzca ye.",
        "feat_sub":  "4,4 milyonun üzerinde ürün \u2013 her içerik yapay zeka tarafından analiz edilir. Tahmin yok, arama yok. İşaret et, tara ya da sor.",
        "cta_title": "Bağırsağın etrafında yaşamayı bırak.",
        "cta_p":     "Ücretsiz indir. Korkusuzca ye. iOS ve Android \u2013 23 dil."
    },
    "ko": {
        "hero_p":    "더 이상 구글 검색 없이. 더 이상 식당에서의 당황스러운 순간 없이. 가리키거나, 스캔하거나, 물어보세요 \u2014 두려움 없이 드세요.",
        "feat_sub":  "440만 개 이상의 제품 \u2013 모든 성분을 AI가 분석합니다. 추측도 없고, 검색도 없이. 가리키거나, 스캔하거나, 물어보세요.",
        "cta_title": "장 때문에 사는 삶을 그만두세요.",
        "cta_p":     "무료 다운로드. 두려움 없이 드세요. iOS & Android \u2013 23개 언어."
    },
    "ja": {
        "hero_p":    "もうGoogleで調べなくていい。もうレストランで気まずい思いをしなくていい。指を向けて、スキャンして、または聞いて \u2014 恐れずに食べよう。",
        "feat_sub":  "440万以上の製品 \u2013 すべての成分をAIが分析します。推測なし、検索なし。指を向けて、スキャンして、または聞いて。",
        "cta_title": "腸のために生きるのをやめよう。",
        "cta_p":     "無料ダウンロード。恐れずに食べよう。iOS & Android \u2013 23言語。"
    },
    "zh-Hans": {
        "hero_p":    "不再需要搜索引擎。不再有在餐厅尴尬的时刻。只需指向、扫描或询问\u2014\u2014无惧饮食。",
        "feat_sub":  "超过440万种产品\u2014\u2014每种成分均由AI分析。无需猜测，无需搜索。指向、扫描或询问即可。",
        "cta_title": "停止围绕肠胃生活。",
        "cta_p":     "免费下载。无惧饮食。iOS & Android \u2013 23种语言。"
    },
    "zh-Hant": {
        "hero_p":    "不再需要Google搜尋。不再有在餐廳尷尬的時刻。只需指向、掃描或詢問\u2014\u2014無懼飲食。",
        "feat_sub":  "超過440萬種產品\u2014\u2014每種成分均由AI分析。無需猜測，無需搜尋。指向、掃描或詢問即可。",
        "cta_title": "停止圍繞腸胃生活。",
        "cta_p":     "免費下載。無懼飲食。iOS & Android \u2013 23種語言。"
    },
    "hi": {
        "hero_p":    "अब गूगल पर खोजने की जरूरत नहीं। रेस्टोरेंट में शर्मनाक पल नहीं। बस इशारा करें, स्कैन करें या पूछें \u2014 और बिना डर के खाएं।",
        "feat_sub":  "44 लाख से अधिक उत्पाद \u2013 हर सामग्री AI द्वारा विश्लेषित। कोई अनुमान नहीं, कोई खोज नहीं। इशारा करें, स्कैन करें या पूछें।",
        "cta_title": "अपने पेट के इर्द-गिर्द जीना बंद करें।",
        "cta_p":     "मुफ्त डाउनलोड करें। बिना डर के खाएं। iOS & Android \u2013 23 भाषाएं।"
    },
    "ar": {
        "hero_p":    "لا مزيد من البحث في جوجل. لا مزيد من المواقف المحرجة في المطاعم. فقط أشر، أو امسح، أو اسأل \u2014 وكل بلا خوف.",
        "feat_sub":  "أكثر من 4.4 مليون منتج \u2013 كل مكون يحلله الذكاء الاصطناعي. لا تخمين، لا بحث. أشر، أو امسح، أو اسأل.",
        "cta_title": "توقف عن العيش حول أمعائك.",
        "cta_p":     "تحميل مجاني. كل بلا خوف. iOS و Android \u2013 23 لغة."
    },
    "th": {
        "hero_p":    "ไม่ต้องค้นหา Google อีกต่อไป ไม่ต้องเผชิญกับความอึดอัดในร้านอาหาร เพียงชี้ สแกน หรือถาม \u2014 แล้วกินโดยไม่ต้องกลัว",
        "feat_sub":  "ผลิตภัณฑ์มากกว่า 4.4 ล้านรายการ \u2013 ทุกส่วนผสมวิเคราะห์โดย AI ไม่ต้องเดา ไม่ต้องค้น เพียงชี้ สแกน หรือถาม",
        "cta_title": "หยุดใช้ชีวิตวนเวียนกับลำไส้ของคุณ",
        "cta_p":     "ดาวน์โหลดฟรี กินโดยไม่ต้องกลัว iOS & Android \u2013 23 ภาษา"
    },
    "id": {
        "hero_p":    "Tidak perlu lagi googling. Tidak ada lagi momen memalukan di restoran. Arahkan, pindai, atau tanya \u2014 dan makan tanpa rasa takut.",
        "feat_sub":  "Lebih dari 4,4 juta produk \u2013 setiap bahan dianalisis oleh AI. Tanpa tebak-tebakan, tanpa pencarian. Arahkan, pindai, atau tanya.",
        "cta_title": "Berhenti hidup mengelilingi usus Anda.",
        "cta_p":     "Unduh gratis. Makan tanpa rasa takut. iOS & Android \u2013 23 bahasa."
    },
    "lt": {
        "hero_p":    "Nebereikia ieškoti internete. Nebereikia gedingų akimirkų restoranuose. Tiesiog nurodyk, nuskenuok arba paklusk \u2014 ir valgyk be baimės.",
        "feat_sub":  "Daugiau nei 4,4 mln. produktų \u2013 kiekvieną ingredientą analizuoja DI. Jokio spėliojimo, jokios paieškos. Nurodyk, nuskenuok arba paklusk.",
        "cta_title": "Liaukis gyvens aplink savo žarnyną.",
        "cta_p":     "Atsisiųsti nemokamai. Valgyk be baimės. iOS & Android \u2013 23 kalbos."
    },
}

total_replaced = 0
total_inserted = 0

def make_replacer(nv):
    def replacer(m):
        return m.group(1) + nv + m.group(3)
    return replacer

for lang, keys in updates.items():
    lang_pattern = rf'("{re.escape(lang)}":\s*\{{)(.*?)(?=\n  "[a-z]{{2,7}}":\s*\{{|\n\}};)'
    lang_match = re.search(lang_pattern, content, re.DOTALL)
    if not lang_match:
        print(f"  WARN: lang block not found for {lang}")
        continue

    block_start = lang_match.start()
    block_end   = lang_match.end()
    block       = content[block_start:block_end]

    for key, new_val in keys.items():
        key_pattern = rf'("{re.escape(key)}":\s*")([^"]*?)(")'
        if re.search(key_pattern, block):
            block = re.sub(key_pattern, make_replacer(new_val), block, count=1)
            total_replaced += 1
        else:
            # Insert after last key in block
            last_matches = list(re.finditer(r'(\s+"[^"]+": "[^"]*")', block))
            if last_matches:
                lm = last_matches[-1]
                block = block[:lm.end()] + f',\n    "{key}": "{new_val}"' + block[lm.end():]
                total_inserted += 1
                print(f"  + inserted {key} into {lang}")
            else:
                print(f"  ERROR: could not insert {key} into {lang}")

    content = content[:block_start] + block + content[block_end:]

print(f"\nReplaced: {total_replaced}  Inserted: {total_inserted}  Total: {total_replaced+total_inserted}")

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Saved.")
