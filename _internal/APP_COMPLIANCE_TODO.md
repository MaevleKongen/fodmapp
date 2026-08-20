# Etterarbeid: app- og selskapsside

Vilkårene og personvernerklæringen på nettsiden er oppdatert (versjon 2.0, nå datert
**20. august 2026**) og rettet mot **verifiseringsrapporten av 13. august 2026** pluss
en ny full gjennomgang **20. august 2026** (chat slettes automatisk etter 24 timer i
app + serverrutine; Firebase Analytics er aktiv igjen med annonse-ID deklarert i Play
og hendelser knyttet til bruker-ID; Resend er i drift og navngitt; velkomstmail aktiv;
Firebase Performance og CDN-er omtalt; Monash-referanser fjernet fra hele produktet).
Dette dokumentet lister det som **ikke** kan gjøres fra nettside-repoet, men som må på
plass for at tekstene skal stemme med virkeligheten.

> Tekstene er skrevet for å være juridisk solide og selskapsvennlige innenfor lovens rammer,
> men de er ikke kvalitetssikret av advokat. Med helseopplysninger i 23 markeder bør en
> advokat lese gjennom sluttresultatet før publisering.

---

## 0. BLOKKERER PUBLISERING

- [ ] **Oversettelse av de 24 endrede nøklene til de 21 gjenstående språkene.**
      Se `TRANSLATION_QUEUE.md` (oppdatert 20. aug). **Engelsk og norsk er ferdige**
      og reflekterer 20. august-tilstanden; de 21 andre språkene har fortsatt gamle,
      nå uriktige påstander (bl.a. bilder lagres 24 t, egen påminnelse før trekk,
      14 mnd bruksstatistikk, FlutterFlow som databehandler, sletting kun via e-post,
      og ingen omtale av 24-timers chatsletting).
      **Branchen må ikke merges til `main` før dette er gjort** — GitHub Pages publiserer
      fra `main`, så alt som ligger der er live på fodmapp.com.

- [x] **Appens interne vilkårstekst byttet til v2.0** (20. aug 2026, rapportens X1):
      TermsAndConditions-siden i appen viser nå de samme 22 punktene som nettsiden,
      på norsk og engelsk med engelsk fallback for de 21 øvrige språkene
      (custom-funksjonene `vilkaarDelTittel`/`vilkaarDelTekst` — oversettes i samme
      økt som nettside-køen). Godta-knappen logger nå også tidspunkt og
      aldersbekreftelse (`settVilkaarAkseptert`).
      **GJENSTÅR: bump `config.termsVersion` til neste heltall** i Firestore (config-dokumentet
      med `type == 'app'`) — men FØRST etter at (a) neste app-release med den nye
      vilkårssiden er ute OG (b) nettsiden er publisert. Bumper du før, re-godkjenner
      gamle appversjoner den gamle teksten. Re-godkjenningsgaten (`maaGodtaVilkaar`)
      virker og trigges av bumpen.

- [ ] **Publiser tekstene samtidig med eller etter neste app-release.**
      Fiksene i Del E av rapporten (samtykkegate, tilbaketrekking, chatsletting,
      nyhetsbrevbryter, aldersgrense, Analytics/Crashlytics) er pushet til FlutterFlow,
      men gjelder først fra neste release. Tekstene beskriver dem som gjeldende.

---

## 1. Lukket — verifisert i rapporten

Til dokumentasjon. Ingen handling.

- [x] **Organisasjonsnummer og forretningsadresse.** Org.nr. 936 367 194 og Østli 15,
      3718 Skien ligger som identitetsblokk i `tc_s1p` og `pp_s17p` på alle 23 språk.
      Nummeret og gateadressen er pakket i `<span dir="ltr">` fordi arabisk ellers
      snudde sifferrekkene og viste «194 367 936».
- [x] **AI-kjeden er verifisert:** Vertex AI via Firebase AI Logic. Ingen AI Studio,
      ingen Gemini-nøkkel i binæret, backend bruker service-account.
      **FlutterFlow er ikke ledd i kjeden** og er derfor fjernet fra databehandlerlisten.
      Treningspåstanden («vi bruker ikke innholdet til å trene egne modeller») holder.
- [x] **Firestore ligger i EU** (`eur3`, multi-region), med delete protection og PITR.
      Men `location: 'global'` for AI-behandlingen, og functions kjører delvis i
      us-central1 — derfor lover erklæringen ikke EU for AI eller serverfunksjoner.
- [x] **Kontosletting finnes i appen** (Profil → Data og personvern → Faresone).
      Apple 5.1.1(v) er dekket. `delete.html` er nå oppdatert til å si dette.
- [x] **Helsedata-samtykke, tilbaketrekking, chatsletting, nyhetsbrevbryter,
      aldersbekreftelse og samtykkelogging med tidspunkt** — bygget og pushet.
- [x] **Backup:** daglig, 49 dagers retention + PITR 7 dager. «Innen 90 dager» i teksten
      er en trygg øvre grense og er bevisst ikke skjerpet.

---

## 2. Må fikses i appen — reelle hull

- [ ] **Feilrapporter/appvurderinger: «inntil 2 år» krever en manuell slettingsrutine.**
      Ingen mekanisme finnes (`allow delete: if false` i rules, og `slett_alle_mine_data`
      treffer feil samlingsnavn `bug_reports` vs `bugReports`). Enten bygg en årlig
      opprydding (f.eks. scheduled function), eller før en kalenderrutine. Verifisert 20. aug.

- [ ] **GCS-lifecycle-regelen (48-timers bildesletting for eldre appversjoner) må
      bekreftes i Cloud Console** — påstanden i tekstene hviler på eierens opplysning;
      ingen regel er synlig i repoet. (Fra rapportens manuelle liste, gjentatt her.)

- [ ] **Kosmetisk app-tekstfeil:** zh-strengen i `trekk_ai_samtykke.dart` inneholder det
      russiske ordet «протокол» midt i kinesisk tekst. Fikses i oversettelsesøkta.


- [ ] **Betalingsveggen nevner verken prøveperiode, autofornyelse eller kvote.**
      Rapportens X8. Den gamle paywallen er aktiv 19 steder og har i tillegg hardkodet
      «Spar 37 %» der den reelle besparelsen er ~47 %.
      Vilkårene (`tc_s6p`) sier nå at *«hvilke funksjoner som inngår, eventuelle
      fair use-grenser og gjeldende priser alltid vises i appen før du kjøper»* —
      det må faktisk stemme. Dette er forbrukerrettslig (mfl. § 22) og et krav fra
      begge butikkene.

- [ ] **TrialGate-siden er kun oversatt til norsk.** 22 språk får tom tittel, tom
      fornyelsestekst og tom knapp på den *harde* betalingsgaten. Dette er
      forbrukerrettslig viktigere enn mye annet i listen.

- [ ] **Server-side opprydding ved kontosletting** (rapportens A3c). `onUserDeleted`
      finnes i FF-eksporten, men er ikke deployet. All sletting er i dag klientdrevet,
      uten batch/transaksjon, og svelger feil stille. Erklæringen lover sletting
      innen 30 dager.

- [ ] **Restsamlinger som overlever kontosletting** (A5c): `bugReports`, `app_ratings`,
      `plus_gaver` (inneholder e-postadresse), `fodmap_ratelimits`.
      `delete.html` opplyser nå ærlig at feilrapporter og vurderinger ikke slettes
      automatisk — men riktig løsning er å anonymisere eller slette dem.
      `plus_gaver` med e-post bør uansett ryddes.

- [ ] **Legacy-slettingen på `/manual`** sletter kun Auth-brukeren og etterlater alle
      Firestore-data. Må fjernes eller kobles til den ordentlige flyten.

- [ ] **Sletterekkefølgen:** data slettes før Auth-brukeren, så en
      `requires-recent-login`-feil gir en halvslettet konto. Snu rekkefølgen eller
      kjør re-autentisering først.

- [ ] **Google-/Apple-registrering får ingen egen aldersdialog.** `ageConfirmed16`
      settes ved vilkårsaksept, som i praksis dekker det, men en egen bekreftelse er
      renere. Bevisst utsatt fordi knappene brukes både til registrering og innlogging.

- [ ] **Sjekk ordlyden i samtykkedialogen for helseopplysninger.** Erklæringen
      (`pp_s4p`) sier at samtykket dekker *både* lagringen av samtaler og
      registreringer *og* overføringen til AI-leverandøren. Hvis dialogen i appen kun
      nevner AI-behandlingen, mangler det et art. 9-grunnlag for selve dagboken for
      brukere som sier nei til AI. Dialogteksten må dekke begge deler.

- [ ] **`slettAlleMineData()` nullstiller ikke `analyseSamtykke`** (X9) — neste
      AI-analyse kjører da uten ny samtykkedialog.

---

## 3. E-post — før noe sendes

- [ ] **Velkomstmailen er kodet, men ikke aktiv.** Resend-konto, DNS, `RESEND_API_KEY`
      og deploy mangler. Den deployede webhooken er sannsynligvis en eldre versjon uten
      koden. Tekstene sier «kan blant annet omfatte» og lover den derfor ikke — men
      ikke send noe før dette står.
- [ ] **Malene sier «Ubegrenset AI-analyse».** Det er feil: Plus har månedskvote
      (300 AI-kall som standard). Ordet «ubegrenset» må ut overalt — det er fjernet
      fra nettsiden.
- [ ] **Avsenderidentitet mangler i malen** (org.nr. og adresse). Krav etter
      ehandelsloven § 8 og markedsføringsloven.
- [ ] **Navngi e-postleverandøren** i `pp_s8p` når Resend er i drift.
      Står nå som «e-postleverandøren vår».
- [ ] **Avmeldingslenke i hver markedsførings-e-post.** Velkomstmailen er
      transaksjonell og trenger den ikke, nyhetsbrevet gjør det.
- [ ] **Ingen påminnelse før prøveperioden utløper** — eierens beslutning.
      Tekstene er rettet: Apple og Google varsler selv. Hvis dette snus senere,
      må `tc_s10p` og `pp_s7p` skrives om igjen.

---

## 4. Verifiser manuelt i konsollen

Kunne ikke sjekkes i verifiseringsøkten (`gcloud` ikke installert, konsolltilgang nede).

1. **GCS-bucket** — bekreft lifecycle-regelen og at bucketen ikke fortsatt inneholder
   bilder fra eldre appversjoner. Dagens app laster ingenting opp. Teksten sier
   «innen 48 timer» fordi GCS-lifecycle har døgnoppløsning.
2. **Firebase Auth provider-liste** — at ikke flere metoder (anonym, telefon) er
   *aktivert* server-side enn appen bruker.
3. **App Check enforcement** for Vertex AI / Firebase AI Logic, og
   API-nøkkelrestriksjoner i GCP.
4. **GA4-eiendommen** (`G-ZP24L9PGTN`) — at oppbevaringstiden står på 2 måneder
   (standard, ingen endring nødvendig) og at ingen BigQuery-eksport er på.
5. **RevenueCat-hostet iOS-paywall** — fornyelsestekst under CTA står som gjenstående
   i `MIGRERING-TRIAL.md`.
6. **Modellstrengen `gemini-3.5-flash`** — verifiser at den faktisk svarer i prod.

---

## 5. Lagringstider som nå står i erklæringen

| Data | Oppgitt | Status |
|---|---|---|
| Bilder | lagres ikke; eventuelle mellomlagrede slettes innen 48 timer | Rettet etter A2 |
| Kontodata etter sletting | fjernet innen 30 dager | Krever server-side opprydding, punkt 2 |
| Sikkerhetskopier | fjernet innen 90 dager | Reelt 49 dager — trygg margin |
| Krasjrapporter (Crashlytics) | inntil 90 dager | Crashlytics' standard, ingen innstilling |
| Bruksstatistikk (Analytics) | inntil 2 måneder på brukernivå | GA4s standard, ingen innstilling |
| Brukstellere på kontoen | så lenge kontoen finnes | Nytt, `Users`/`app_stats` |
| Kjøps-/regnskapsdokumentasjon | 5 år (bokføringsloven) | |
| Markedsføringssamtykke | samtykkeperioden + 3 år som dokumentasjon | |
| Support, feilrapporter og vurderinger | inntil 2 år | Slettes ikke automatisk i dag |

---

## 6. Selskapsdokumentasjon (internt, ikke nettside)

- [ ] **Databehandleravtaler** med Google Cloud/Firebase (dekker også Vertex AI),
      RevenueCat og Resend. FlutterFlow trenger **ikke** databehandleravtale for
      helseopplysninger — det er verifisert at plattformen ikke er ledd i AI-kjeden.
- [ ] **Protokoll over behandlingsaktiviteter** (GDPR art. 30).
- [ ] **DPIA / vurdering av personvernkonsekvenser** (art. 35). Sannsynligvis påkrevd:
      særlige kategorier (helse), i stor skala, med AI-behandling.
- [ ] **Rutine for avviksbehandling** — melding til Datatilsynet innen 72 timer.
      Erklæringen lover nå dette eksplisitt.
- [ ] **Oversikt over tredjelandsoverføringer.** Relevant fordi AI-behandlingen kjører
      på `location: 'global'` og noen serverfunksjoner ligger i us-central1.
      Noter grunnlaget for hver (SCC eller EU-US Data Privacy Framework).

---

## 7. App Store / Google Play

- [ ] **Google Play «Data safety»** må matche den nye erklæringen:
      «Health and fitness» som innsamlet og knyttet til brukeren.
      Crash logs og Analytics kan nå deklareres — begge er aktivert i appen.
- [ ] **Apple «App Privacy»-labels**: helsedata under «Data Linked to You».
- [ ] **Aldersmerking** i begge butikker, nå som appen har 16-årsgrense.
- [ ] Butikkbeskrivelsene bør nevne prøveperiode + Plus, ikke gamle nivåer eller
      promptantall.

---

## 8. Markedsføring — MDR-risiko

Disclaimeren om at appen ikke er medisinsk utstyr hjelper bare hvis markedsføringen ikke
sier noe annet. «Intended purpose» leses ut av helheten. Appen har god medisinsk
disclaimer på 24 språk, og paywalls/onboarding er rene.

- [ ] **Appens gamle interne vilkår pkt. 4** sier at AI-chatten gir informasjon om
      «symptomlindring». Mykes opp når in-app-vilkårene byttes ut (punkt 0).
- [ ] `index.html` FAQ `q1a` — «to reduce digestive issues». Bruk «informasjon og
      veiledning» framfor formuleringer om å behandle eller lindre.
- [ ] Samme gjennomgang for App Store-/Play-beskrivelser og Instagram-innhold.

---

## 9. Kodeopprydding (ingen tekstkonsekvens)

- [ ] `GemniniIBSkameraCall` (`api_calls.dart:14-57`) peker på AI Studio-endepunktet med
      tom nøkkel og har 0 kallsteder. Bør slettes — den er misvisende ved en revisjon.
- [ ] Pro-rester: `planType='pro'` skrives fortsatt, `quotasPro=500`, ubrukt Pro-paywall
      og «Unlock Premium Features» på 23 språk. Pro er ikke synlig for brukere.
- [ ] Foreldreløs Cloud Function `kameraAgent` (v1, nodejs20) — ingen kildekode, ingen
      kallsteder.
- [ ] Seks legacy-sider under `lib/gamle/` gjør egne Gemini-kall og er fortsatt rutet.
- [ ] `lastRcEventAt` skrives av webhooken, men finnes ikke i FF-skjemaet.

---

## 10. Valgfrie forbedringer på nettsiden

- [ ] **Selvhost skrifttypene.** Nettsiden laster fra Google Fonts, som sender brukerens
      IP-adresse til Google ved hver sidelasting. Dette er nå opplyst i erklæringen
      (`pp_s15p`), men å laste fontene lokalt fjerner problemet helt.
- [ ] **Informasjonskapsel-banneret** sier «kun nødvendige», men har en «Avslå»-knapp
      som ikke gjør noe reelt. Enten fjern valget eller gjør det funksjonelt.
- [ ] Vurder å arkivere tidligere versjoner av vilkår og erklæring. Erklæringen sier at
      tidligere versjoner er tilgjengelige på forespørsel.
- [ ] **Ikke legg til `.nojekyll` i repoet.** GitHub Pages serverer hele repoet på
      fodmapp.com, også markdown-filer. Denne fila, verifiseringsbriefen og
      oversettelseskøen lå opprinnelig i rota og ville da vært lesbare på
      `fodmapp.com/APP_COMPLIANCE_TODO.html` — altså en offentlig liste over våre egne
      udekkede hull. De er nå flyttet til `_internal/`, som Jekyll utelater, og
      `_config.yml` sier det eksplisitt. En `.nojekyll`-fil ville satt Jekyll ut av spill
      og gjort mappa offentlig igjen.

---

## Hva som ble endret på nettsiden

**Første runde (v2.0):**

- `termsandconditions.html` — 13 → 22 punkter, ikrafttredelsesdato og versjon
- `privacypolicy.html` — omskrevet til GDPR art. 13-struktur, 17 punkter, i18n-klar
- `js/i18n.js` — 89 nye/oppdaterte nøkler × 23 språk; RTL for arabisk
- `index.html` — FAQ `q2a` (personvern) og `q5a` (pris/prøveperiode)
- `manual.html` — `t4p` (personvern-tipset)
- `delete.html` — hva som lagres og hva som slettes
- `css/site.css` — stiler for de nye tekstblokkene
- Metabeskrivelser og footer-år

**Andre runde (etter verifiseringsrapporten) — 21 nøkler, foreløpig kun engelsk:**

- Bilder lagres ikke lenger «i inntil 24 timer» — de behandles direkte og forkastes;
  eldre versjoners opplastinger slettes innen 48 timer
- Løftet om egen påminnelse før trekk er fjernet — Apple og Google varsler selv
- Nyhetsbrevsamtykket beskrives der det faktisk gis: i appens innstillinger, av som standard
- AI-kjeden skrevet presist: Gemini via Firebase AI Logic og Vertex AI;
  FlutterFlow fjernet fra databehandlerlisten
- Ærlig beskrivelse av helsekonteksten som sendes til AI, og at lagret chathistorikk
  ikke sendes
- Nye datatyper opplyst: telefonnummer, profilbilde, brukstellere, feilrapporter og
  vurderinger, medisiner/menstruasjon/søvn/Bristol, triggerprofil og reintro-tester
- Ny bokstav g) om posisjon (Overpass/OpenStreetMap), som ikke lagres
- Bruksstatistikk 14 måneder → 2 måneder
- Overføringer: database i EU, men AI-behandlingen og noen serverfunksjoner er det ikke
- Push-varsler korrigert: appen sender ingen; påminnelser vises lokalt
- `delete.html` skrevet om — sletting i appen er nå hovedveien, e-post er reserveløsningen

**Struktur:**

- `_internal/` — arbeidsdokumenter og i18n-verktøy, holdt utenfor det publiserte nettstedet
- `_config.yml` — sier eksplisitt hva Jekyll skal utelate
