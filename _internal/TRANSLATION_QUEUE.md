# Oversettelseskø — 26 nøkler til 21 språk

**Midlertidig arbeidsfil. Slett den når køen er tom.**

Engelsk (`en`-blokken i `js/i18n.js`) og norsk (`nb`) er ferdig oppdatert
per **20. august 2026** — begge reflekterer nå appens faktiske adferd,
inkludert endringene fra 20. august (chat slettes etter 24 timer,
Firebase Analytics med annonse-ID aktiv, Resend navngitt, velkomstmail
aktiv, CDN-omtale, Firebase Performance). De øvrige **21 språkene** har
fortsatt gamle verdier på nøklene under, som nå er **uriktige**.

> ⛔ **`main` må ikke oppdateres før køen er tom.** GitHub Pages publiserer fra `main`
> til fodmapp.com. Merges branchen nå, blir 21 av 23 språk stående med påstander som
> er dokumentert feil — verre enn å vente.

## Kilde

`js/i18n.js`, blokken `"en"` **slik den står nå** (20. august-versjonen). Den er fasit.
Ikke oversett fra HTML-filene og ikke fra eldre kopier. `nb`-blokken kan brukes som
referanse for tone/terminologi på skandinaviske språk.

## Nøkler

| Nøkkel | Fil | Hva som er endret (kumulativt 13.–20. aug) |
|---|---|---|
| `pp_s2p` | privacypolicy | Kortversjonen: **chat slettes automatisk etter 24 t**; bilder lagres ikke; nyhetsbrev i innstillingene; sletting i appen |
| `pp_s3p` | privacypolicy | Utvidet a/c/d/e/f + ny g) posisjon. **e) omskrevet 20. aug:** Analytics-hendelser knyttet til bruker-ID, **annonse-ID på Android**, Firebase Performance, onboarding-steg. c) chat-24t-note |
| `pp_s5p` | privacypolicy | **NY 20. aug:** «trial-/betalingspåminnelser» fjernet fra tjenestemelding-grunnlaget (vi sender ingen) |
| `pp_s6p` | privacypolicy | AI-kjeden (Firebase AI Logic/Vertex AI, FlutterFlow ute); **Lagring og sletting omskrevet 20. aug: chat 24 t (app + serverrutine hver time); runde 2: AI-analyse inntil 30 dager (ikke 90), chat-konteksten presisert (toleranseprofil, protokollstatus, siste AI-analyse, skanninger)** |
| `pp_s7p` | privacypolicy | Ingen egen trial-påminnelse; nyhetsbrev av som standard; **velkomstmail omtales nå som aktiv (Resend i drift)** |
| `pp_s8p` | privacypolicy | Databehandlerliste: FlutterFlow ut; Firebase AI Logic/Vertex AI, Overpass, **Resend (navngitt) og CDN-punkt (LottieFiles/Google Fonts) inn; «performance monitoring» i Firebase-punktet** |
| `pp_s9p` | privacypolicy | Database i EU, AI + noen serverfunksjoner utenfor EØS |
| `pp_s10p` | privacypolicy | **Egen rad: chat slettes etter 24 t.** Bilder lagres ikke/48 t; Analytics 2 mnd; brukstellere; feilrapporter; **runde 2: markedsføringssamtykke-raden følger kontoen (3-årsformuleringen fjernet)** |
| `tc_s10p` | terms | Ingen egen påminnelse før trekk; nyhetsbrev i innstillingene; ingen server-push; **velkomstmail aktiv** |
| `tc_s14p` | terms | Tredjepartsliste: Firebase AI Logic/Vertex AI, Overpass, **Resend, innholdsnettverk** |
| `tc_s15p` | terms | Sletting av konto skjer i appen |
| `tc_updated` / `pp_updated` | begge | **Datoen er allerede maskinelt byttet 13→20 i alle 23 språk** — kun kontroll, ny oversettelse ikke nødvendig |
| `del_s1p1` | delete | Telefonnummer, profilbilde, brukstellere, aldersbekreftelse |
| `del_s1p2` | delete | Bilder lagres ikke/48 t; **chat 24 t**; sletting i appen |
| `del_s1p3` | delete | Gemini via Firebase AI Logic/Vertex AI; tilbaketrekking i appen |
| `del_s3h` | delete | «Slik sletter du kontoen din» |
| `del_s3p1` | delete | Sletting i appen er hovedveien |
| `del_s3p2` | delete | Delvis sletting: data / chat / trekke AI-samtykke |
| `del_s3p3` | delete | E-post som reserve + Google/Apple-tilgang |
| `del_s4p1` | delete | Brukstellere; «mellomlagrede bilder» fjernet |
| `del_s4p2` | delete | Feilrapporter/vurderinger slettes ikke automatisk |
| `q2a` | index (FAQ) | **Chat 24 t**; bilder lagres ikke; sletting i appen |
| `q6a` | index (FAQ) | Kun tallfiks: «over 23 språk» → «23 språk» (fjern det lokale «over»-ordet) |
| `pp_s15p` | privacypolicy | **NY 20. aug (runde 2):** nettsiden laster også bilder/butikkmerker fra Apple/Wikimedia (IP-overføring) |
| `cookie_msg` | alle sider | **NY 20. aug (runde 2):** personvernlenken (`<a href=\"privacypolicy.html\">…</a>`) må inn i banner-teksten — applyLang overskriver innerHTML og mistet lenken |
| `t4p` | manual | **Chat 24 t**; bilder lagres ikke |

## Språk å oversette til (21)

`id` `da` `de` `es` `fr` `it` `lt` `nl` `pl` `pt` `fi` `sv` `tr` `ru` `ar` `hi` `th`
`zh-Hans` `zh-Hant` `ja` `ko`

(`en` og `nb` er ferdige.)

## Konvensjoner som må holdes

- **HTML beholdes ordrett.** `<ul>`, `<li>`, `<h3>`, `<strong>`, `<br>`, `<a href="...">`
  og entiteter (`&ndash;` `&rsquo;` `&laquo;` `&raquo;` `&rarr;`) skal stå som i engelsk.
  Bare tekstinnholdet oversettes. `_internal/tools/i18n/validate.js` sjekker at taggene balanserer.
- **Arabisk:** tall og gateadresser må ligge i `<span dir="ltr">…</span>`, ellers snur
  bidi-algoritmen sifferrekkene. Dette gjelder allerede identitetsblokken; pass på hvis
  nye tall kommer inn («24 timer», «annonse-ID»-omtaler o.l.).
- **Fransk:** mellomrom (helst `&nbsp;`) foran kolon, semikolon, utropstegn og spørsmålstegn.
- **Kinesisk og japansk:** fullbreddes tegnsetting (`：`, `、`, `。`) uten etterfølgende
  mellomrom.
- **Artikkelhenvisninger** til GDPR beholdes med lokal konvensjon
  (art. 9(2)(a) / Art. 9 Abs. 2 Buchst. a osv.), slik det allerede er gjort i de øvrige
  nøklene på samme språk. Sjekk nabonøklene før du finner opp noe nytt.
- **Menyveier i appen** (Profil → Data og personvern → Faresone → Slett konto,
  «Nyhetsbrev på e-post») må matche appens faktiske oversettelser. Der de ikke er kjent,
  bruk språkets naturlige oversettelse — men noter det, så det kan sjekkes mot appen.
- **NB: appens interne vilkårsside** (byttes til v2.0 i appen, norsk + engelsk med engelsk
  fallback) skal også oversettes i samme økt — se `APP_COMPLIANCE_TODO.md` §0b. Teksten
  ligger i custom-funksjonene `vilkaarDelTittel`/`vilkaarDelTekst` i FlutterFlow-prosjektet.

## Etter oversettelse

1. `python3 _internal/tools/i18n/inject.py lang_<code>.json` for hvert språk
2. `node _internal/tools/i18n/validate.js` — alle 23 språk, alle nøkler, balanserte tagger
3. Rendersjekk i Chromium på minst `ar`, `fr`, `zh-Hans` og `nb`
4. Slett denne filen
