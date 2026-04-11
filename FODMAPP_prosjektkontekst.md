# FODMAPP nettside – prosjektkontekst

## App og selskap
- **App:** FODMAPP – Flutter/FlutterFlow, v1.0.9, iOS + Android
- **Selskap:** Telemark Software Solutions AS
- **Domene:** fodmapp.com
- **Kontakt:** post@fodmapp.com

## Abonnementer
| Plan | AI-interaksjoner/mnd |
|------|----------------------|
| Free | 20 |
| Plus | 300 |
| Pro | 1000 |
(Tilgjengelig månedlig eller årlig)

## Teknisk stack
- **Auth:** Email/passord, Google Sign-In, Apple Sign-In
- **Backend:** Firebase (Auth, Firestore, Storage)
- **AI:** Google Gemini — skal IKKE nevnes i brukervendt innhold. Kun lov i privacy policy, T&C og delete-siden
- **Barkodefunksjon:** Open Food Facts (4,4+ millioner produkter) — skryt av dette aktivt
- **Abonnement:** RevenueCat
- **i18n:** 23 språk: `nb, en, sv, da, fr, es, ru, th, zh-Hans, ar, de, pl, lt, fi, pt, it, zh-Hant, hi, ko, ja, tr, id, nl` — nb er primærspråk

---

## Filer
Alle filer ligger i `/sessions/.../mnt/outputs/` (eller brukerens valgte mappe):

```
index.html
about.html
manual.html
delete.html
privacypolicy.html
termsandconditions.html
js/i18n.js   (~490KB, 23 språk, ~210+ nøkler per språk)
```

---

## Regler som alltid gjelder

1. **Rekkefølge på funksjoner overalt:** 📸 AI Kamera → 🏷️ Strekkodeskanner → 💬 AI Chat
2. **Aldri nevn Google Gemini** i brukervendt innhold
3. **Free tier = 20** AI-interaksjoner/mnd
4. **Open Food Facts = 4,4+ millioner produkter** – nevn dette aktivt og positivt
5. **i18n.js redigeres alltid med Python-scripts** (ikke Edit-verktøyet direkte – for stor fil)
6. **Alle tekstendringer oversettes til alle 23 språk** i i18n.js
7. **Copyright:** `© 2025 FODMAPP · Telemark Software Solutions AS`

---

## Hva som allerede er gjort

### Generelt (alle sider)
- Copyright: `© 2025 FODMAPP · Telemark Software Solutions AS`
- Hreflang-tagger for alle 23 språk + canonical + x-default
- SEO: Unike `<title>`, `<meta description>`, `<meta keywords>` og Twitter Card per side

### index.html
- Stats-bar: `4.4M+` produkter (erstattet AI-stat), med i18n-nøkkel `stat_products`
- Feature-kort og faner i riktig rekkefølge: 📸 Kamera → 🏷️ Barcode → 💬 Chat
- Gammel kamera/chat accordion erstattet med **tabbet seksjon** ("Three tools. One app.")
  - **Kamera-fane:** 6 kort – enkeltmat, måltider, restaurantmenyer, kjøleskap, drikke, FODMAP-score 0–100
  - **Barcode-fane:** 3 kort – 4,4M produkter, AI-analyse, sikker shopping (terrafarget aksentlinje på hover)
  - **Chat-fane:** 6 kort – matvurdering, restaurantretter, ukesmeny, handleliste, FODMAP-spørsmål, stressmestring
- Kamera er default aktiv fane
- `hero_p`: kamera → barcode → chat rekkefølge
- FAQ: Free=20, Plus=300, Pro=1000. Ingen Google Gemini-nevning

### manual.html
- 4 seksjoner i rekkefølge: 📸 AI Kamera → 🏷️ Strekkodeskanner → 💬 AI Chat → ✦ Tips
- Seksjonstitler er midtstilte
- **Tips-seksjon (6 kort):**
  - t1: Ta klare bilder
  - t2: Internettforbindelse
  - t3: Bygg rutiner
  - t4: Personvern først
  - t5: Porsjonsstørrelse teller (ny)
  - t6: Bruk appen gjennom hele FODMAP-prosessen (ny – kortversjon, ingen lang forklaringstekst etter ".")

### about.html
- Nevner 4,4M produkter (Open Food Facts), ingen Google Gemini
- "23 languages" (spesifikt tall)

### privacypolicy.html
- Dato: 10. april 2026
- Login: email/passord, Google Sign-In, Apple Sign-In
- Datadeling nevner: Open Food Facts (barcode lookups) og RevenueCat (subscription)

### termsandconditions.html
- Full T&C med 10 seksjoner (tidligere var den tom/placeholder)
- Ingen "Last updated"-dato
- tc_s4p: Free=20/mnd, Plus=300, Pro=1000

### delete.html
- del_s1p1: nevner Free, Plus, Pro
- del_s2h/p: Google og Apple login (OAuth)

### js/i18n.js – viktige nøkler (alle 23 språk)
| Nøkkel | Innhold |
|--------|---------|
| `feat_tab_tag/title/sub` | Ny tabbet seksjon på index |
| `ch1h–ch6h` / `ch1p–ch6p` | Chat-kort (manualen og indeks) |
| `cam1h–cam6h` / `cam1p–cam6p` | Kamera-kort |
| `bc1h–bc3h` / `bc1p–bc3p` | Barcode-kort |
| `t1h–t6h` / `t1p–t6p` | Tips-kort inkl. t5 (porsjon) og t6 (FODMAP-faser) |
| `tc_s1h–tc_s10h/p` | T&C seksjoner |
| `stat_products` | "4.4M+ / Produkter i databasen" |
| `hero_p` | Herο-tekst med kamera-først rekkefølge |
| `man_intro` | Manualtekst med kamera-først rekkefølge |
| `man_chat_tag/title/sub` | Chat-seksjon i manual |
| `man_cam_tag/title/sub` | Kamera-seksjon i manual |
| `man_bc_tag/title/sub` | Barcode-seksjon i manual |
| `man_tag/title` | Tips-seksjon i manual ("Godt å vite") |

---

## i18n.js – struktur
```javascript
const T = {
  "nb": { "lang_title": "...", "hero_p": "...", ... },  // ~210 nøkler
  "da": { ... },
  "sv": { ... },
  // ... alle 23 språk
  "en": { ... }  // en er sist i filen, har færre nøkler (fallback i HTML)
};
```
**Viktig:** Bruk alltid Python til å redigere filen. Inserter nye nøkler ved å finne språkblokken med regex og sette inn etter åpningskrøllen `{`. Verifiser alltid at antall nøkler er 23 etter endringer.

---

## Gjenstående forslag (ikke implementert)
- [ ] Kundeanmeldelser / testimonials
- [ ] Offisielle App Store / Google Play-badges
- [ ] Demo-video eller animert GIF
- [ ] Sammenligningstabell for abonnementer (Free vs Plus vs Pro)
- [ ] Eksempler på faktiske AI-svar (skjermbilder)
- [ ] Utvidet FAQ (offline-bruk, hvilke land, gjeninnføringsfase)
- [ ] "Anbefalt av" / faglig troverdighet (Monash University etc.)
- [ ] E-post/push-påmelding ("Få beskjed om nye funksjoner")
