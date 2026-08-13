# Oppdrag: verifiser appen mot nye brukervilkår og personvernerklæring

**Til:** Claude Code-sesjonen som har Firebase- og FlutterFlow-tilgang
**Fra:** sesjonen som skrev om de juridiske tekstene på nettsiden
**Repo som ble endret:** `MaevleKongen/fodmapp`, branch `claude/terms-conditions-update-rlgqhy`

---

## Bakgrunn

Brukervilkårene og personvernerklæringen på fodmapp.com er skrevet helt om
(versjon 2.0, 13. august 2026) og oversatt til 23 språk. Tekstene inneholder nå
**konkrete, etterprøvbare påstander** om hvordan appen faktisk virker: lagringstider,
hva som sendes til Gemini, hvilke samtykker som innhentes, hvilke e-poster som sendes.

Problemet: **tekstene ble skrevet uten tilgang til appen.** De bygger på hva eieren
oppga muntlig. En personvernerklæring som beskriver noe annet enn virkeligheten er i
seg selv et brudd på GDPR art. 5(1)(a) og art. 13 — så feil her er ikke kosmetiske.

**Din oppgave:** sjekk hver påstand nedenfor mot den faktiske appen og infrastrukturen,
og rapporter tilbake hvilke som stemmer og hvilke som ikke gjør det.

### Viktig om hvordan avvik skal håndteres

For hvert avvik finnes to mulige retninger, og **du skal ikke velge selv** — du skal
rapportere hva som er tilfelle og anbefale retning:

- **Fiks appen** → når teksten beskriver noe som burde vært sånn (f.eks. manglende
  samtykke-checkbox, manglende sletting i appen)
- **Fiks teksten** → når appen er greit som den er, men teksten sier noe feil
  (f.eks. hvis Analytics faktisk lagrer i 2 måneder og teksten sier 14)

Endring av tekst er dyrt: hver påstand står i `js/i18n.js` på **23 språk**. Derfor
oppgir jeg i18n-nøkkelen for hver påstand, slik at en tekstendring blir konkret.

---

## Del A — Firebase og infrastruktur

### A1. Hvor ligger Firestore geografisk?

```bash
firebase projects:list
firebase use <prosjekt-id>
firebase firestore:databases:list
```

**Påstand** (`pp_s9p`): «Der leverandørene våre tilbyr europeiske regioner, søker vi å
få opplysninger lagret og behandlet innenfor EU/EØS.»

- `eur3` eller `europe-*` → påstanden holder, og du kan foreslå at teksten skjerpes til
  å si det rett ut (sterkere posisjon overfor brukerne)
- `nam5` eller `us-*` → **helsedata ligger i USA**. Teksten holder fortsatt formelt
  («søker vi»), men overføringsgrunnlaget må bekreftes (SCC/DPF), og eieren bør vite det.
  Rapportér dette tydelig.

### A2. Slettes bilder faktisk innen 24 timer?

```bash
gcloud storage buckets describe gs://<prosjekt>.firebasestorage.app --format="value(lifecycle)"
# eller eldre bucket-navn:
gcloud storage buckets describe gs://<prosjekt>.appspot.com --format="value(lifecycle)"
# alternativt: gsutil lifecycle get gs://<bucket>
```

**Påstand** (`pp_s10p`, `pp_s3p` pkt. d, `pp_s6p`, `del_s1p2`, `tc_s7p` indirekte):
«Bilder — maksimalt 24 timer etter analysen», «slettes automatisk».

Dette er den mest gjentatte påstanden i erklæringen. Sjekk **begge** mulige mekanismer:
1. GCS lifecycle-regel med `age: 1` (dag) og `Delete`
2. En Cloud Function (scheduled) som sletter

Finnes ingen av dem → **påstanden er usann**, og bilder ligger der for alltid. Det er
det alvorligste mulige funnet i denne gjennomgangen. Rapportér umiddelbart.

Merk: GCS lifecycle har døgnoppløsning, ikke timer. En regel på `age: 1` sletter
inntil 48 timer etter opplasting i praksis. Hvis det er mekanismen, bør teksten si
«innen 48 timer» eller «innen én dag etter analysen». Flagg det.

### A3. Hvilke Cloud Functions finnes?

```bash
firebase functions:list
```

Se spesielt etter funksjoner som gjør dette:

| Funksjon vi har lovet | Påstand i | Finnes? |
|---|---|---|
| Påminnelse før prøveperioden utløper og betaling trekkes | `tc_s10p`, `pp_s7p` | |
| Velkomst-e-post | `tc_s10p`, `pp_s7p` | |
| Sletting av konto + tilhørende data | `pp_s10p`, `del_s4p1` | |
| Sletting av bilder (hvis ikke lifecycle-regel) | A2 over | |
| Utsending av nyhetsbrev | `pp_s7p` | |

**Trekk-varselet er særlig viktig.** Vilkårene lover det uttrykkelig, med fet skrift.
Apple og Google sender sine egne varsler — men vi har lovet vårt eget. Finnes det ikke,
er det enten en app-oppgave eller teksten må endres.

### A4. Hvilke innloggingsmetoder er aktive?

Firebase Console → Authentication → Sign-in method (eller `firebase apps:list` +
konsoll — CLI-en eksponerer ikke dette direkte).

**Påstand** (`tc_s5p`, `pp_s3p` pkt. a): «e-post og passord, Google-innlogging eller
Apple-innlogging».

Er noe **annet** aktivert (Facebook, anonym pålogging, telefon, magic link) →
erklæringen er ufullstendig og må utvides. Anonym pålogging er verdt å se etter
spesielt: den lager brukere uten samtykkesporing.

### A5. Datamodellen — stemmer datatabellen?

Hent `firestore.rules` og se på faktiske collections/felt. Trenger du et konkret
dokument, bruk et testbruker-dokument, ikke en ekte brukers data.

**Påstand** (`pp_s3p`) — erklæringen sier vi lagrer *dette og ikke mer*:

**a) Konto:** e-postadresse, fornavn, etternavn, passord (hashet), innloggingsmetode,
språkinnstilling, appversjon, land/region, dokumentasjon på samtykker (hvilken versjon
av vilkår og personvernerklæring som ble godtatt, når, og om det er samtykket til
markedsføring)

**b) Abonnement:** status og type, prøveperiodestatus, start- og fornyelsesdato,
pseudonym abonnent-ID hos RevenueCat, kjøpshistorikk fra appbutikken.
**Erklæringen sier uttrykkelig at vi aldri mottar eller lagrer kortopplysninger.**

**c) Helse:** AI-chatmeldinger, mat- og symptomregistreringer, AI-analyser,
FODMAP-poengsummer, anbefalinger knyttet til kontoen, samt historikken

**d) Bilder:** midlertidig

**e) Teknisk:** enhetsmodell, OS, appversjon, språk, Crashlytics-krasjrapporter,
Firebase Analytics-bruksstatistikk

**f) Korrespondanse:** support-e-poster

**Det du skal lete etter er felt som IKKE står i listen.** Vanlige kandidater:

- vekt, høyde, alder, kjønn, fødselsdato
- IBS-subtype eller diagnose satt som eget felt
- push-token (FCM) — **står ikke i erklæringen i dag, må legges til hvis det lagres**
- enhets-ID / IDFA / advertising ID
- geolokasjon
- kontaktliste, kalender
- lagrede/favorittmarkerte oppskrifter (sannsynligvis greit, men bør nevnes)
- rå API-logger med prompt-innhold

Hvert felt du finner som ikke er dekket → erklæringen må utvides (`pp_s3p`, 23 språk).

**Sjekk også at disse to feltene finnes**, for erklæringen lover dem:
- versjon + tidspunkt for godtatte vilkår/personvernerklæring
- flagg for markedsføringssamtykke (og gjerne tidspunkt for gitt/trukket)

Finnes de ikke, kan selskapet ikke bevise hva en bruker har samtykket til. Vilkårene
har fått versjonsnummer og dato nettopp for å muliggjøre dette.

### A6. Oppbevaringstid for Analytics — forventet avvik

Google Analytics 4 → Admin → Data retention.

**Påstand** (`pp_s10p`): «Bruksstatistikk — inntil 14 måneder, i aggregert form.»

**GA4 har 2 måneder som standardinnstilling.** Hvis den ikke er endret, er teksten
feil. To utfall:
- Sett innstillingen til 14 måneder → teksten stemmer
- La den stå på 2 måneder → teksten må endres til «inntil 2 måneder»

Sjekk samtidig om det finnes **BigQuery-eksport** av Analytics. Da lever dataene
videre i BigQuery uten 14-månedersgrensen, og erklæringen er ufullstendig.

### A7. Sikkerhetskopier — holder 90-dagerspåstanden?

**Påstand** (`pp_s10p`, `del_s4p1`): «fra sikkerhetskopier innen 90 dager».

Sjekk hva som faktisk finnes:
- Firestore PITR (point-in-time recovery) = **7 dager**, ikke 90
- Firestore scheduled backups = konfigurerbar oppbevaring
- Ingen backup i det hele tatt = påstanden er meningsløs

```bash
gcloud firestore backups schedules list --database='(default)'
gcloud firestore backups list
```

Er det ingen backups, bør teksten forenkles til at data slettes innen 30 dager, uten
90-dagerspåstanden. Er retention f.eks. 7 dager, skriv 7.

### A8. Crashlytics

**Påstand** (`pp_s10p`): «Krasjrapporter — inntil 90 dager.» Det er Crashlytics'
standard. Bekreft at det ikke er endret.

---

## Del B — FlutterFlow og app-kode

Dette er den viktigste delen. Spørsmål B1–B3 avgjør en åpen juridisk vurdering.

### B1. Hvor ligger Gemini-nøkkelen, og hvem kaller Google?

Dette er hovedspørsmålet. Let i den eksporterte FlutterFlow-koden etter API-nøkkel,
`generativelanguage`, `aiplatform`, `gemini`, `GoogleGenerativeAI`, custom actions og
API-kall.

Tre mulige svar, med helt ulike konsekvenser:

**(a) Nøkkelen ligger i appen / klienten kaller Google direkte**
→ Nøkkelen kan hentes ut av app-binæret av hvem som helst. Dette er et
sikkerhetsproblem, ikke bare et juridisk et: erklæringen lover
«krypterte forbindelser» og «tilgang begrenset til få personer», men en lekket nøkkel
gir hvem som helst tilgang til å bruke prosjektets AI-kvote — og i noen oppsett til
å nå data. **Rapportér som funn med høy prioritet.** Anbefal å flytte kallet til en
Cloud Function.

**(b) Kallet går via en Cloud Function / egen backend**
→ Ryddig. Bekreft hvilken Google-tjeneste den kaller (se B2).

**(c) Kallet går via FlutterFlows egen backend/proxy**
→ **Da er FlutterFlow databehandler for helseopplysninger.** Det utløser krav om
databehandleravtale (GDPR art. 28) og at FlutterFlow står i databehandlerlisten.
FlutterFlow er allerede oppført i `pp_s8p`, men som «apputviklingsplattformen som
AI-integrasjonen leveres gjennom» — en formulering som ble valgt bevisst fordi
sannheten ikke var kjent. Bekreft eller avkreft, så teksten kan bli presis.

### B2. Vertex AI eller AI Studio?

Se på endepunktet i koden:

| Endepunkt | Tjeneste | Konsekvens for teksten |
|---|---|---|
| `aiplatform.googleapis.com` | **Vertex AI** (Google Cloud) | Sterkeste posisjon. Innhold brukes ikke til modelltrening. Kan angi EU-region. |
| `generativelanguage.googleapis.com` | **Gemini API / AI Studio** | Skiller på betalt/gratis nivå. **Gratisnivået kan brukes til produktforbedring** — det er uforsvarlig for helsedata. |
| Firebase AI Logic / Vertex AI in Firebase | via Firebase-SDK | Beskriv Firebase som ledd i kjeden |

**Påstand** (`pp_s6p`, `tc_s12p`): «Vi bruker ikke innholdet ditt til å trene våre egne
AI-modeller» og «AI-leverandøren opptrer som vår databehandler og behandler innholdet på
vår instruks».

Er det AI Studio på gratisnivå → påstanden er i beste fall misvisende, og bruken bør
flyttes til Vertex AI eller betalt nivå. Dette er et konkret, viktig funn.

### B3. Hva sendes egentlig i prompten?

Finn den faktiske payloaden som sendes til Gemini.

**Påstand** (`pp_s6p`) — erklæringen er spesifikk her:

Sendes: chatteksten, bilder, ingredienslister for skannet strekkode, «begrenset kontekst
som er nødvendig for et fornuftig svar, som språket ditt og relevante tidligere meldinger
i samme samtale».

Sendes **ikke**: «navn, e-postadresse eller betalingsopplysninger».

Sjekk om prompten inneholder `uid`, e-post, navn, eller en systemprompt med
brukerprofil (alder/vekt/diagnose). Gjør den det, er påstanden usann og må rettes.
En bruker-UID er en pseudonym identifikator — sendes den, bør erklæringen si det.

### B4. Finnes samtykkedialogen for helsedata?

**Påstand** (`pp_s4p`, `tc_s19p`): uttrykkelig samtykke etter art. 9(2)(a), gitt i
«en egen dialog i appen **før AI-funksjonene gjøres tilgjengelige** for deg», og som
dekker både lagring av samtaler/registreringer og overføring til AI-leverandøren.

Sjekk:
- Finnes dialogen?
- Kommer den **før** første AI-bruk, eller etterpå?
- Er den **separat** fra «Godta vilkår», eller samme avkrysning?
- Kan brukeren si nei og fortsatt bruke resten av appen?
- Loggføres den (versjon + tidspunkt)?

Er samtykket bundlet med vilkårene, er det ugyldig etter art. 7(2) og 7(4). Da er
både appen og teksten feil.

### B5. Finnes separat nyhetsbrev-samtykke?

**Påstand** (`tc_s10p`, `pp_s7p`): samtykket til nyhetsbrev «gis separat fra din
godkjenning av disse vilkårene», er «frivillig», og er «ikke en forutsetning for å
opprette konto eller bruke FODMAPP».

Sjekk registreringsflyten:
- Egen checkbox for nyhetsbrev?
- Er den **ikke** forhåndsavkrysset? (forhåndsavkrysset = ugyldig samtykke)
- Er den skilt fra vilkårsavkrysningen?
- Finnes av/på-bryter i innstillingene?

Dette er det punktet eieren er mest opptatt av — han skal sende nyhetsbrev. Uten en
gyldig separat opt-in kan han ikke lovlig sende dem (markedsføringsloven § 15).

### B6. Kan brukeren slette konto inne i appen?

**Apple App Store Guideline 5.1.1(v)** krever at apper med kontoopprettelse tilbyr
sletting av konto **i appen**. Nettsiden (`delete.html`) viser i dag bare e-postruten.

Sjekk om funksjonen finnes i appen. Gjør den ikke det, er det avvisningsgrunn ved
neste App Review — uavhengig av personvern.

### B7. Kan brukeren slette samtalehistorikk og enkeltregistreringer?

**Påstand** (`pp_s3p`, `pp_s10p`, `q2a`, `t4p`): historikken lagres «til du sletter
dem», og «du kan slette dem når som helst».

Finnes ingen slettefunksjon i appen, er påstanden usann. Sjekk både hele historikken
og enkeltoppføringer.

### B8. Kan samtykket trekkes tilbake i innstillingene — og skjer det noe?

**Påstand** (`pp_s4p`): tilbaketrekking «i innstillingene i appen eller ved å kontakte
oss», og «det skal være like enkelt å trekke tilbake som å gi». Videre: ved
tilbaketrekking «stanser vi behandlingen og **sletter de lagrede helseopplysningene**».

Sjekk at det finnes en bryter, og at den faktisk trigger sletting — ikke bare setter
et flagg.

### B9. Aldersgrense

**Påstand** (`tc_s5p`, `pp_s13p`): minst 16 år.

Finnes det en aldersbekreftelse ved registrering? Uten den er 16-årsgrensen bare en
påstand i en tekst ingen leser. Sjekk også at aldersmerkingen i App Store / Play er
konsistent.

### B10. Prøveperiode og abonnement

**Påstand** (`tc_s6p`, `q5a`): prøveperioden er «for tiden 14 dager» med «full tilgang
til appens funksjoner», gis «én gang per bruker og per Apple-ID eller Google-konto»,
og etter den kreves FODMAPP Plus, tilgjengelig som måneds- eller årsabonnement.

Sjekk i RevenueCat og i App Store Connect / Play Console:
- Er introductory offer faktisk 14 dager?
- Er det full tilgang i prøveperioden, eller er noe begrenset?
- Finnes både måneds- og årsplan?
- Finnes det fortsatt et gammelt «Pro»-nivå i konfigurasjonen? (Nettsiden nevnte
  tidligere Free/Plus/Pro. Alle spor av Pro er fjernet fra tekstene — hvis produktet
  fortsatt finnes i butikken, må det avklares.)

### B11. E-postleverandør

**Påstand** (`pp_s8p`): databehandlerlisten inneholder «e-postleverandøren vår» uten navn.

Finn ut hvem det er (SendGrid, Brevo, Mailgun, Firebase Extensions, Resend …), så
navnet kan settes inn. Sjekk samtidig at markedsførings-e-postene faktisk har
avmeldingslenke og avsenderidentitet.

---

## Del C — Butikkerklæringer

### C1. Google Play «Data safety»

Må matche den nye erklæringen. Kritisk punkt: samtaler og symptomregistreringer lagres
nå på kontoen, så **«Health and fitness» må deklareres som innsamlet og knyttet til
brukeren**. Sjekk også at «Personal info», «Photos», «App activity» og «Crash logs»
stemmer.

### C2. Apple App Privacy

Tilsvarende: helsedata under «Data Linked to You». Sjekk at ingenting er deklarert som
«Data Not Linked to You» når det faktisk ligger på kontoen.

### C3. Butikkbeskrivelser

Skal ikke nevne gamle nivåer eller promptantall. Skal ikke inneholde medisinske
påstander (se MDR-punktet under).

---

## Del D — MDR-risiko i markedsføring

Tekstene sier nå uttrykkelig at appen **ikke er medisinsk utstyr** og ikke er tiltenkt
«diagnostisering, forebygging, overvåking, prediksjon, prognose, behandling eller
lindring» av sykdom — en formulering som speiler MDR art. 2(1) bevisst.

Men en slik disclaimer hjelper bare hvis markedsføringen ikke sier noe annet.
«Intended purpose» leses ut av helheten.

Sjekk app-tekster, onboarding, push-varsler, butikkbeskrivelser og eventuelle
in-app-meldinger for påstander om å behandle, kurere eller lindre. Rapportér
formuleringer som trekker i motsatt retning.

---

## Rapportformat

Lever tilbake en tabell med én rad per sjekkpunkt:

| ID | Sjekk | Resultat | Bevis | Anbefaling |
|---|---|---|---|---|
| A1 | Firestore-region | `eur3` | `firestore:databases:list` output | Skjerp `pp_s9p` til å si EU direkte |
| A2 | 24t bildesletting | MANGLER | ingen lifecycle-regel, ingen function | Fiks appen — dette er kritisk |
| … | | | | |

Bruk `OK` / `AVVIK` / `IKKE FUNNET` / `N/A`. For hvert `AVVIK`, si tydelig om
anbefalingen er **fiks appen** eller **fiks teksten**, og ved tekstendring: hvilken
i18n-nøkkel.

### Prioritér i denne rekkefølgen

1. **A2** (bildesletting) — mest gjentatte påstand i erklæringen
2. **B1 + B2** (Gemini-kjeden) — avgjør både sikkerhet og om treningspåstanden holder
3. **B4 + B5** (de to samtykkene) — avgjør om behandlingen av helsedata og
   nyhetsbrevutsendingen er lovlig i det hele tatt
4. **B6** (sletting i appen) — konkret App Review-risiko
5. **A5** (felt som ikke står i erklæringen)
6. **A6** (Analytics-oppbevaring — forventet avvik)
7. Resten

### Ikke gjør dette

- Ikke endre tekstene i `MaevleKongen/fodmapp` selv. Rapportér, så samles endringene
  ett sted — hver påstand finnes på 23 språk og må endres konsistent.
- Ikke les ekte brukeres helsedata for å bekrefte datamodellen. Bruk regler, skjema
  og testbrukere.
- Ikke endre produksjonsinnstillinger (f.eks. GA4-retention) uten at eieren har sagt ja.

---

## Kontekst du kan trenge

- Nettsidens tekster ligger i `termsandconditions.html`, `privacypolicy.html` og
  `js/i18n.js` (89 nøkler × 23 språk) i repoet nevnt øverst.
- `APP_COMPLIANCE_TODO.md` i samme repo har den opprinnelige oppgavelisten.
- Selskapet er Telemark Software Solutions AS, org.nr. 936 367 194,
  Østli 15, 3718 Skien.
- Tekstene er ikke kvalitetssikret av advokat. Med helseopplysninger i 23 markeder
  bør de leses av en jurist før publisering — men de bør stemme faktisk først, og
  det er det du finner ut nå.
