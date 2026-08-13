# Oversettelseskø — 21 nøkler

**Midlertidig arbeidsfil. Slett den når køen er tom.**

Engelsk er rettet mot verifiseringsrapporten av 13. august 2026. De øvrige 22 språkene
har foreløpig de gamle verdiene, som nå er **uriktige**. Køen kjøres i én bolk til slutt,
når alle tekstendringer er ferdige, slik eieren har bedt om.

> ⛔ **`main` må ikke oppdateres før køen er tom.** GitHub Pages publiserer fra `main`
> til fodmapp.com. Merges branchen nå, blir 22 av 23 språk stående med påstander som
> er dokumentert feil — verre enn å vente.

## Kilde

`js/i18n.js`, blokken `"en"`. Den er fasit. Ikke oversett fra HTML-filene: de inneholder
den engelske fallback-teksten, som er identisk, men i18n-verdien er den som faktisk vises.

## Nøkler

| Nøkkel | Fil | Hva som er endret |
|---|---|---|
| `pp_s2p` | privacypolicy | Kortversjonen: bilder lagres ikke; nyhetsbrev slås på i innstillingene; sletting skjer i appen |
| `pp_s3p` | privacypolicy | Utvidet a/c/d/e/f + **ny bokstav g) posisjon**. Telefonnummer, profilbilde, brukstellere, feilrapporter, vurderinger, medisiner, menstruasjon, søvn, Bristol, triggerprofil, reintro-tester |
| `pp_s6p` | privacypolicy | AI-kjeden: Gemini via Firebase AI Logic og Vertex AI. FlutterFlow eksplisitt utenfor. Ærlig liste over helsekonteksten som sendes. Lagret chathistorikk sendes ikke |
| `pp_s7p` | privacypolicy | Ingen egen trial-påminnelse — Apple/Google varsler selv. Nyhetsbrev slås på under «Newsletter by email» i appens innstillinger, av som standard |
| `pp_s8p` | privacypolicy | Databehandlerliste: FlutterFlow ut, «Google (Firebase AI Logic / Vertex AI)» og OpenStreetMap/Overpass inn |
| `pp_s9p` | privacypolicy | Database i EU (Firestore, europeisk multi-region), men AI-behandlingen og noen serverfunksjoner er utenfor EØS |
| `pp_s10p` | privacypolicy | Bilder: lagres ikke / 48 t for eldre. Analytics: 14 mnd → **2 måneder**. Brukstellere og feilrapporter lagt til |
| `tc_s10p` | terms | Ingen egen påminnelse før trekk. Nyhetsbrev i innstillingene. Appen sender ingen push-varsler — påminnelser vises lokalt |
| `tc_s14p` | terms | Tredjepartsliste oppdatert: Firebase AI Logic/Vertex AI, Overpass |
| `tc_s15p` | terms | Sletting av konto skjer i appen (Profil → Data og personvern) |
| `del_s1p1` | delete | Telefonnummer, profilbilde, brukstellere, aldersbekreftelse, utvidet liste over registreringer |
| `del_s1p2` | delete | Bilder lagres ikke; eldre versjoners opplastinger slettes innen 48 t; sletting skjer i appen |
| `del_s1p3` | delete | Gemini via Firebase AI Logic og Vertex AI; tilbaketrekking under Profil → Data og personvern |
| `del_s3h` | delete | Overskrift: «How to request deletion» → «How to delete your account» |
| `del_s3p1` | delete | Sletting i appen er hovedveien |
| `del_s3p2` | delete | Delvis sletting: kun data, kun chathistorikk, eller trekke tilbake AI-samtykke |
| `del_s3p3` | delete | E-post som reserveløsning + Google/Apple-tilgang |
| `del_s4p1` | delete | Brukstellere lagt til; «mellomlagrede bilder» fjernet |
| `del_s4p2` | delete | Opplyser ærlig at feilrapporter og vurderinger ikke slettes automatisk |
| `q2a` | index (FAQ) | Bilder lagres ikke; sletting skjer i appen |
| `t4p` | manual | Samme |

`del_s3h`, `del_s3p1` og `del_s3p2` manglet i den engelske blokken fra før og falt tilbake
på HTML-teksten. De er nå lagt inn. De 22 andre språkene **har** dem allerede, med gammelt
innhold, så de skal overskrives som de øvrige.

## Språk å oversette til (22)

`id` `da` `de` `es` `fr` `it` `lt` `nl` `nb` `pl` `pt` `fi` `sv` `tr` `ru` `ar` `hi` `th`
`zh-Hans` `zh-Hant` `ja` `ko`

## Konvensjoner som må holdes

- **HTML beholdes ordrett.** `<ul>`, `<li>`, `<h3>`, `<strong>`, `<br>`, `<a href="...">`
  og entiteter (`&ndash;` `&rsquo;` `&laquo;` `&raquo;` `&rarr;`) skal stå som i engelsk.
  Bare tekstinnholdet oversettes. `_internal/tools/i18n/validate.js` sjekker at taggene balanserer.
- **Arabisk:** tall og gateadresser må ligge i `<span dir="ltr">…</span>`, ellers snur
  bidi-algoritmen sifferrekkene. Dette gjelder allerede identitetsblokken; pass på hvis
  nye tall kommer inn.
- **Fransk:** mellomrom (helst `&nbsp;`) foran kolon, semikolon, utropstegn og spørsmålstegn.
- **Kinesisk og japansk:** fullbreddes tegnsetting (`：`, `、`, `。`) uten etterfølgende
  mellomrom.
- **Artikkelhenvisninger** til GDPR beholdes med lokal konvensjon
  (art. 9(2)(a) / Art. 9 Abs. 2 Buchst. a osv.), slik det allerede er gjort i de øvrige
  nøklene på samme språk. Sjekk nabonøklene før du finner opp noe nytt.
- **Menyveier i appen** (Profil → Data og personvern → Faresone → Slett konto,
  «Newsletter by email») må matche appens faktiske oversettelser. Der de ikke er kjent,
  bruk språkets naturlige oversettelse — men noter det, så det kan sjekkes mot appen.

## Etter oversettelse

1. `python3 _internal/tools/i18n/inject.py lang_<code>.json` for hvert språk
2. `node _internal/tools/i18n/validate.js` — alle 23 språk, alle nøkler, balanserte tagger
3. Rendersjekk i Chromium på minst `ar`, `fr`, `zh-Hans` og `nb`
4. Slett denne filen
