# Etterarbeid: app- og selskapsside

Vilkårene og personvernerklæringen på nettsiden er oppdatert (versjon 2.0, 13. august 2026).
Dette dokumentet lister det som **ikke** kan gjøres fra nettside-repoet, men som må på plass
for at tekstene skal stemme med virkeligheten.

> Tekstene er skrevet for å være juridisk solide og selskapsvennlige innenfor lovens rammer,
> men de er ikke kvalitetssikret av advokat. Med helseopplysninger i 23 markeder bør en
> advokat lese gjennom sluttresultatet før publisering.

---

## 1. Må fikses før publisering

- [ ] **Organisasjonsnummer og forretningsadresse.**
      GDPR art. 13(1)(a) og ehandelsloven § 8 krever at behandlingsansvarlig kan identifiseres.
      Nettsiden har i dag bare navn, e-post og domene. Sett inn org.nr og adresse i:
      - `js/i18n.js` → nøkkelen `tc_s1p` (alle 23 språk)
      - `js/i18n.js` → nøkkelen `pp_s17p` (alle 23 språk)
      - de tilsvarende engelske standardtekstene i `termsandconditions.html` og `privacypolicy.html`

- [ ] **Verifiser AI-kjeden, og skriv den riktig.**
      Erklæringen sier i dag at AI-integrasjonen leveres «gjennom apputviklingsplattformen vår
      (FlutterFlow) og Googles infrastruktur». Det er formulert slik fordi den faktiske veien
      ikke er bekreftet. Finn ut hvilken det er:
      - **Vertex AI (Google Cloud)** → sterkeste posisjon. Da kan du si eksplisitt at innhold
        ikke brukes til modelltrening, og angi EU-region.
      - **Gemini API med AI Studio-nøkkel** → vilkårene skiller på betalt/gratis nivå.
        Gratisnivået kan brukes til produktforbedring. Da må formuleringen justeres, og
        gratisnivå bør ikke brukes til helsedata i produksjon.
      - **FlutterFlow som mellomledd** → da er FlutterFlow **databehandler for helseopplysninger**
        og trenger databehandleravtale. Dette er lett å overse.

- [ ] **Navngi e-postleverandøren** i `pp_s8p` (databehandlerlisten) når den er valgt.
      Står nå som «e-postleverandøren vår».

---

## 2. App-endringer som tekstene nå forutsetter

Erklæringen lover disse funksjonene. Hvis de ikke finnes, er erklæringen uriktig.

- [ ] **Separat, ikke-forhåndsavkrysset samtykke til nyhetsbrev** ved registrering.
      Kan ikke ligge i «Godta vilkår»-avkrysningen — da er samtykket ugyldig
      (GDPR art. 7(2) og 7(4), markedsføringsloven § 15).
- [ ] **Av/på-bryter for nyhetsbrev** i appens innstillinger.
- [ ] **Avmeldingslenke i hver markedsførings-e-post** + avsenderidentitet.
- [ ] **Uttrykkelig samtykke til helseopplysninger** (art. 9(2)(a)) som egen dialog før
      AI-funksjonene åpnes — separat fra vilkårene, med mulighet til å si nei.
- [ ] **Tilbaketrekking av samtykke i innstillingene**, like enkelt som å gi det.
      Ved tilbaketrekking: stopp behandling og slett lagrede helseopplysninger.
- [ ] **Sletting av samtalehistorikk og enkeltregistreringer i appen.**
      Erklæringen sier «til du sletter dem».
- [ ] **Sletting av konto inne i appen.** Apple App Store Guideline 5.1.1(v) krever dette for
      apper med kontoopprettelse. `delete.html` viser i dag bare e-postruten → avvisningsrisiko
      i App Review.
- [ ] **Aldersgrense 16 år** ved registrering.
- [ ] **Loggføring av samtykkeversjon + tidspunkt** per bruker (vilkår, personvern, marketing).
      Vilkårene har nå versjonsnummer og dato nettopp for å kunne bevise hva som ble godtatt.
- [ ] **Påminnelse før prøveperioden utløper og betaling belastes.**
      Vilkårene og erklæringen lover nå denne e-posten uttrykkelig.

---

## 3. Verifiser at lagringstidene faktisk stemmer

Erklæringen oppgir konkrete tider. Sjekk at de er implementert:

| Data | Oppgitt i erklæringen |
|---|---|
| Bilder | slettes automatisk innen 24 timer |
| Kontodata etter sletting | fjernet innen 30 dager |
| Sikkerhetskopier | fjernet innen 90 dager |
| Krasjrapporter (Crashlytics) | inntil 90 dager |
| Bruksstatistikk (Analytics) | inntil 14 måneder |
| Kjøps-/regnskapsdokumentasjon | 5 år (bokføringsloven) |
| Markedsføringssamtykke | samtykkeperioden + 3 år som dokumentasjon |
| Support-korrespondanse | inntil 2 år |

Firebase Analytics har egen innstilling for oppbevaringstid — sett den til 14 måneder
hvis den står på noe annet.

---

## 4. Selskapsdokumentasjon (internt, ikke nettside)

- [ ] **Databehandleravtaler** med Google Cloud/Firebase, RevenueCat, FlutterFlow (hvis
      relevant, se punkt 1) og e-postleverandøren.
- [ ] **Protokoll over behandlingsaktiviteter** (GDPR art. 30).
- [ ] **DPIA / vurdering av personvernkonsekvenser** (art. 35). Sannsynligvis påkrevd:
      særlige kategorier (helse), i stor skala, med AI-behandling.
- [ ] **Rutine for avviksbehandling** — melding til Datatilsynet innen 72 timer.
      Erklæringen lover nå dette eksplisitt.
- [ ] **Oversikt over tredjelandsoverføringer** og hvilket grunnlag som gjelder for hver
      (SCC eller EU-US Data Privacy Framework).

---

## 5. App Store / Google Play

- [ ] **Google Play «Data safety»** må matche den nye erklæringen. Særlig:
      «Health and fitness» må deklareres som innsamlet og knyttet til brukeren, siden
      samtaler og symptomregistreringer nå lagres på kontoen.
- [ ] **Apple «App Privacy»-labels** tilsvarende: helsedata under «Data Linked to You».
- [ ] Butikkbeskrivelsene bør nevne prøveperiode + Plus, ikke gamle nivåer.

---

## 6. Markedsføring — MDR-risiko

Disclaimeren om at appen ikke er medisinsk utstyr hjelper bare hvis markedsføringen ikke
sier noe annet. «Intended purpose» leses ut av helheten.

- [ ] Gå gjennom markedsføringstekster for helsepåstander. Eksempel som bør mykes:
      `index.html` FAQ `q1a` — «to reduce digestive issues».
      Bruk «informasjon og veiledning» framfor formuleringer om å behandle eller lindre.
- [ ] Samme gjennomgang for App Store/Play-beskrivelser og Instagram-innhold.

---

## 7. Valgfrie forbedringer

- [ ] **Selvhost skrifttypene.** Nettsiden laster fra Google Fonts, som sender brukerens
      IP-adresse til Google ved hver sidelasting. Dette er nå opplyst i erklæringen
      (`pp_s15p`), men å laste fontene lokalt fjerner problemet helt.
- [ ] **Samtykke eller av/på for Firebase Analytics** i appen. Analytics er pseudonymt,
      ikke anonymt — erklæringen er rettet til å si dette korrekt.
- [ ] **Informasjonskapsel-banneret** på nettsiden sier «kun nødvendige», men har en
      «Avslå»-knapp som ikke gjør noe reelt. Enten fjern valget eller gjør det funksjonelt.
- [ ] Vurder å arkivere tidligere versjoner av vilkår og erklæring. Erklæringen sier at
      tidligere versjoner er tilgjengelige på forespørsel.

---

## Hva som ble endret på nettsiden

- `termsandconditions.html` — 13 → 22 punkter, ikrafttredelsesdato og versjon
- `privacypolicy.html` — omskrevet til GDPR art. 13-struktur, 17 punkter, i18n-klar
- `js/i18n.js` — 89 nye/oppdaterte nøkler × 23 språk; RTL for arabisk
- `index.html` — FAQ `q2a` (personvern) og `q5a` (pris/prøveperiode)
- `manual.html` — `t4p` (personvern-tipset)
- `delete.html` — hva som lagres og hva som slettes
- `css/site.css` — stiler for de nye tekstblokkene
- Metabeskrivelser og footer-år
