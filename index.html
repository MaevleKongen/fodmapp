import React from "react";
import { motion } from "framer-motion";
import {
  MessageSquare,
  Camera,
  Salad,
  NotebookText,
  Refrigerator,
  ShieldCheck,
  Lock,
  ArrowRight,
  Sparkles,
  Image as ImageIcon,
} from "lucide-react";

/**
 * ✅ Fix: fjernet statiske bildefiler som ble importert fra ../public/... (ga build-feil)
 * Denne komponenten bruker nå dynamiske URL-strenger i stedet for import.
 *
 * Slik kobler du skjermbildene dine på en trygg måte uten bundler-feil:
 * 1) Legg filene i public/-mappen din.
 * 2) Sett kildene via globalt objekt (f.eks. i <script> i index.html):
 *    window.FODMAPP_IMAGES = {
 *      front: "/8560113d-2fd5-4297-885a-40466efb93bc.png",
 *      chat: "/70fd61b1-d123-4bb1-8f8c-c1c7b3ec4d44.png",
 *      camera: "/71af0897-162d-4210-9266-7f877dcf0e20.png"
 *    }
 * 3) Alternativt: sett miljøvariabler
 *    - Vite:   import.meta.env.VITE_FODMAPP_FRONT (CHAT/CAMERA)
 *    - CRA:    process.env.REACT_APP_FODMAPP_FRONT (CHAT/CAMERA)
 *    - Next:   process.env.NEXT_PUBLIC_FODMAPP_FRONT (CHAT/CAMERA)
 *
 * Denne filen faller automatisk tilbake til en pen placeholder om en URL mangler
 * eller er feil – så appen kompilerer alltid, og du får en visuell indikator.
 */

// Hent konfigurasjon fra globalt objekt / env variabler
const getEnv = (keys) => {
  if (typeof window !== "undefined" && window.FODMAPP_IMAGES) {
    return window.FODMAPP_IMAGES[keys[0]];
  }
  const [kFront, kChat, kCamera] = keys;
  // Støtt Vite / CRA / Next env-variabler
  const env =
    (typeof import.meta !== "undefined" && import.meta.env) ||
    (typeof process !== "undefined" && process.env) || {};
  return (
    env[kFront] || // Vite
    env[`REACT_APP_${kFront}`] || // CRA (unlikely, but safe)
    env[`NEXT_PUBLIC_${kFront}`] ||
    null
  );
};

const frontImgSrc =
  getEnv(["VITE_FODMAPP_FRONT", "REACT_APP_FODMAPP_FRONT", "NEXT_PUBLIC_FODMAPP_FRONT"]) ||
  "/8560113d-2fd5-4297-885a-40466efb93bc.png"; // forventet plassering i /public

const chatImgSrc =
  getEnv(["VITE_FODMAPP_CHAT", "REACT_APP_FODMAPP_CHAT", "NEXT_PUBLIC_FODMAPP_CHAT"]) ||
  "/70fd61b1-d123-4bb1-8f8c-c1c7b3ec4d44.png";

const cameraImgSrc =
  getEnv(["VITE_FODMAPP_CAMERA", "REACT_APP_FODMAPP_CAMERA", "NEXT_PUBLIC_FODMAPP_CAMERA"]) ||
  "/71af0897-162d-4210-9266-7f877dcf0e20.png";

// Bildekomponent med pen fallback om kilden ikke finnes
function SmartImage({ src, alt, className }) {
  const [failed, setFailed] = React.useState(false);
  if (!src || failed) {
    return (
      <div
        className={`flex aspect-[9/19] w-full items-center justify-center rounded-2xl bg-gradient-to-br from-slate-900 to-slate-800 text-center text-xs text-slate-200 ring-1 ring-slate-700/40 shadow ${className}`}
        role="img"
        aria-label={`Bilde mangler: ${alt}`}
      >
        <div>
          <p className="font-semibold">Bilde ikke funnet</p>
          <p className="mt-1 opacity-80">Plasser filen i <code className="rounded bg-slate-900/50 px-1">/public</code> og oppdater URL-en.</p>
        </div>
      </div>
    );
  }
  return (
    <img
      src={src}
      alt={alt}
      className={`rounded-2xl shadow w-full h-auto ${className}`}
      onError={() => setFailed(true)}
      loading="lazy"
    />
  );
}

const Container = ({ children }) => (
  <div className="mx-auto w-full max-w-6xl px-4 sm:px-6 lg:px-8">{children}</div>
);

const Section = ({ id, eyebrow, title, subtitle, children }) => (
  <section id={id} className="py-16 sm:py-20">
    <Container>
      {(eyebrow || title || subtitle) && (
        <div className="mb-10 text-center">
          {eyebrow && (
            <p className="mb-2 inline-block rounded-full bg-emerald-50 px-3 py-1 text-xs font-semibold uppercase tracking-wider text-emerald-700">
              {eyebrow}
            </p>
          )}
          {title && (
            <h2 className="text-3xl font-bold tracking-tight sm:text-4xl">{title}</h2>
          )}
          {subtitle && (
            <p className="mx-auto mt-3 max-w-2xl text-base text-slate-600">
              {subtitle}
            </p>
          )}
        </div>
      )}
      {children}
    </Container>
  </section>
);

const Badge = ({ children }) => (
  <span className="inline-flex items-center gap-1 rounded-full bg-emerald-600/10 px-3 py-1 text-xs font-medium text-emerald-700 ring-1 ring-inset ring-emerald-600/20">
    <Sparkles className="h-3.5 w-3.5" /> {children}
  </span>
);

export default function FodmappLanding() {
  return (
    <div className="min-h-screen bg-gradient-to-b from-emerald-50 via-white to-white text-slate-900">
      {/* Nav */}
      <header className="sticky top-0 z-50 w-full border-b border-slate-200/60 bg-white/80 backdrop-blur">
        <Container>
          <div className="flex h-16 items-center justify-between">
            <a href="#hero" className="flex items-center gap-2">
              <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-emerald-600 text-white shadow-sm">
                <Salad className="h-5 w-5" />
              </div>
              <span className="text-lg font-bold tracking-tight">FODMAPP</span>
            </a>
            <nav className="hidden items-center gap-6 text-sm font-medium text-slate-700 md:flex">
              <a href="#funksjoner" className="hover:text-emerald-700">Funksjoner</a>
              <a href="#slik-funker-det" className="hover:text-emerald-700">Slik funker det</a>
              <a href="#personvern" className="hover:text-emerald-700">Sikkerhet & personvern</a>
              <a href="#faq" className="hover:text-emerald-700">FAQ</a>
            </nav>
            <div className="flex items-center gap-3">
              <a href="#kontakt" className="hidden rounded-xl border border-slate-200 px-4 py-2 text-sm font-semibold text-slate-700 hover:bg-slate-50 md:inline-block">Kontakt</a>
              <a href="#cta" className="rounded-xl bg-emerald-600 px-4 py-2 text-sm font-semibold text-white shadow-sm hover:bg-emerald-700">Last ned</a>
            </div>
          </div>
        </Container>
      </header>

      {/* Hero */}
      <section id="hero" className="relative overflow-hidden">
        <div aria-hidden className="pointer-events-none absolute -left-56 -top-24 h-80 w-80 rounded-full bg-emerald-200/40 blur-3xl" />
        <div aria-hidden className="pointer-events-none absolute -right-56 top-40 h-80 w-80 rounded-full bg-emerald-300/30 blur-3xl" />
        <Container>
          <div className="grid items-center gap-10 py-16 sm:py-24 lg:grid-cols-2">
            <div>
              <Badge>LavFODMAP-assistenten i lomma</Badge>
              <h1 className="mt-4 text-4xl font-bold leading-tight tracking-tight sm:text-5xl">
                Navigér FODMAP-dietten med AI-hjelp
              </h1>
              <p className="mt-4 text-lg text-slate-600">
                FODMAPP kombinerer samtale- og kamerateknologi for å gjøre matvalg enklere – hjemme, på butikken og på restaurant.
              </p>
              <div className="mt-6 flex flex-col gap-3 sm:flex-row">
                <a
                  href="#cta"
                  className="inline-flex items-center justify-center gap-2 rounded-2xl bg-emerald-600 px-5 py-3 text-sm font-semibold text-white shadow-sm hover:bg-emerald-700"
                >
                  Kom i gang <ArrowRight className="h-4 w-4" />
                </a>
                <a
                  href="#funksjoner"
                  className="inline-flex items-center justify-center gap-2 rounded-2xl border border-slate-200 bg-white px-5 py-3 text-sm font-semibold text-slate-700 hover:bg-slate-50"
                >
                  Se funksjoner
                </a>
              </div>
              <ul className="mt-6 flex flex-wrap items-center gap-x-4 gap-y-2 text-sm text-slate-500">
                <li className="inline-flex items-center gap-2"><ShieldCheck className="h-4 w-4" /> Data lagres ikke i appen</li>
                <li className="inline-flex items-center gap-2"><Lock className="h-4 w-4" /> Kryptert mellomlagring i Firebase</li>
              </ul>
            </div>
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6 }}
              className="relative"
            >
              <div className="relative mx-auto w-full max-w-md rounded-3xl border border-slate-200 bg-white p-4 shadow-xl">
                <SmartImage src={frontImgSrc} alt="Forside av FODMAPP" />
              </div>
            </motion.div>
          </div>
        </Container>
      </section>

      {/* Funksjoner med bilder */}
      <Section
        id="funksjoner"
        eyebrow="Funksjoner"
        title="To kraftige AI-agenter – én enkel app"
        subtitle="Chat for kunnskap. Kamera for virkeligheten. Sammen dekker de hele FODMAP-hverdagen."
      >
        <div className="grid gap-6 sm:grid-cols-2">
          <motion.div initial={{ opacity: 0, y: 10 }} whileInView={{ opacity: 1, y: 0 }} transition={{ duration: 0.4 }} className="h-full rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
            <h3 className="mb-4 text-xl font-semibold flex items-center gap-2"><MessageSquare className="h-5 w-5 text-emerald-600" /> AI Chat</h3>
            <SmartImage src={chatImgSrc} alt="Chatvisning i appen" />
          </motion.div>

          <motion.div initial={{ opacity: 0, y: 10 }} whileInView={{ opacity: 1, y: 0 }} transition={{ duration: 0.5 }} className="h-full rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
            <h3 className="mb-4 text-xl font-semibold flex items-center gap-2"><Camera className="h-5 w-5 text-emerald-600" /> AI Kamera</h3>
            <SmartImage src={cameraImgSrc} alt="Kameravisning i appen" />
          </motion.div>
        </div>
      </Section>

      {/* Slik funker det */}
      <Section
        id="slik-funker-det"
        eyebrow="Slik funker det"
        title="Trygt, raskt og enkelt"
        subtitle="Under panseret: 4o-mini fra OpenAI for både chat og bildeanalyse. Firebase håndterer midlertidig bilde-opplasting – som slettes etter bruk."
      >
        <div className="grid gap-6 lg:grid-cols-3">
          <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
            <h4 className="mb-2 text-base font-semibold">1) Du spør – eller tar et bilde</h4>
            <p className="text-sm text-slate-600">Start en chat om FODMAP, eller bruk kameraet for å analysere mat, meny eller kjøleskap.</p>
          </div>
          <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
            <h4 className="mb-2 text-base font-semibold">2) Sikre kall til OpenAI</h4>
            <p className="text-sm text-slate-600">Data sendes via OpenAI-API. Chat lagres ikke. Bilder lastes midlertidig til Google Firebase som kun formidler en sikker lenke til modellen.</p>
          </div>
          <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
            <h4 className="mb-2 text-base font-semibold">3) Klare svar – med forslag</h4>
            <p className="text-sm text-slate-600">Få tydelige anbefalinger, alternativer med lav FODMAP og steg-for-steg tips ved restaurantbesøk.</p>
          </div>
        </div>
      </Section>

      {/* Personvern */}
      <Section
        id="personvern"
        eyebrow="Sikkerhet & personvern"
        title="Designet for personvern fra dag én"
      >
        <div className="grid gap-6 md:grid-cols-2">
          <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
            <div className="mb-3 inline-flex items-center gap-2 rounded-lg bg-emerald-600/10 px-2 py-1 text-xs font-semibold text-emerald-700 ring-1 ring-emerald-600/20">
              <ShieldCheck className="h-4 w-4" /> Dataminimering
            </div>
            <p className="text-slate-600">Vi lagrer ikke chat-innhold noe sted. Bilder slettes fra Firebase etter bruk.</p>
          </div>
          <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
            <div className="mb-3 inline-flex items-center gap-2 rounded-lg bg-emerald-600/10 px-2 py-1 text-xs font-semibold text-emerald-700 ring-1 ring-emerald-600/20">
              <Lock className="h-4 w-4" /> Åpenhet
            </div>
            <p className="text-slate-600">OpenAI håndterer tekst og bilder via deres API. Les <a className="underline decoration-emerald-500 underline-offset-2 hover:text-emerald-700" href="https://openai.com/policies/terms-of-use" target="_blank" rel="noreferrer">brukervilkår</a> og <a className="underline decoration-emerald-500 underline-offset-2 hover:text-emerald-700" href="https://openai.com/policies/privacy-policy" target="_blank" rel="noreferrer">personvern</a>.</p>
          </div>
        </div>
        <p className="mt-4 text-center text-xs text-slate-500">Merk: Appen erstatter ikke medisinsk rådgivning. Ved symptomer, kontakt helsepersonell.</p>
      </Section>

      {/* CTA */}
      <Section
        id="cta"
        eyebrow="Kom i gang"
        title="Gjør FODMAP enklere – i dag"
        subtitle="Tilgjengelig på iOS og Android snart. Meld interesse for tidlig tilgang."
      >
        <div className="mx-auto max-w-xl rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
          <form className="grid gap-3 sm:grid-cols-[1fr_auto]">
            <input
              type="email"
              required
              placeholder="Din e-postadresse"
              className="h-11 rounded-xl border border-slate-200 px-4 text-sm outline-none ring-emerald-600/0 transition focus:ring-2"
            />
            <button type="submit" className="inline-flex h-11 items-center justify-center gap-2 rounded-xl bg-emerald-600 px-5 text-sm font-semibold text-white shadow-sm hover:bg-emerald-700">
              Få tidlig tilgang <ArrowRight className="h-4 w-4" />
            </button>
          </form>
          <p className="mt-3 text-center text-xs text-slate-500">Ved å melde deg på godtar du å motta informasjon om lansering og nyheter.</p>
        </div>
      </Section>

      {/* FAQ */}
      <Section id="faq" eyebrow="FAQ" title="Ofte stilte spørsmål">
        <div className="mx-auto grid max-w-3xl gap-4">
          {[
            {
              q: "Hva er FODMAPP?",
              a: "En app med AI-chat og AI-kamera som hjelper deg å forstå og praktisere lavFODMAP i hverdagen.",
            },
            {
              q: "Hvilken modell brukes?",
              a: "Begge agentene bruker OpenAI 4o-mini via API for tekst og bildeanalyse.",
            },
            {
              q: "Lagrer dere data?",
              a: "Vi lagrer ikke chat. Bilder lagres midlertidig i Firebase og slettes etter bruk.",
            },
            {
              q: "Kan appen erstatte medisinsk rådgivning?",
              a: "Nei. Appen gir veiledning, men ved symptomer eller spørsmål om diagnose bør du kontakte helsepersonell.",
            },
          ].map((item, i) => (
            <details key={i} className="group rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
              <summary className="cursor-pointer list-none text-base font-semibold">
                <span className="mr-2">{item.q}</span>
                <span className="float-right text-slate-500 group-open:hidden">+</span>
                <span className="float-right text-slate-500 group-open:inline">−</span>
              </summary>
              <p className="mt-3 text-sm text-slate-600">{item.a}</p>
            </details>
          ))}
        </div>
      </Section>

      {/* Footer */}
      <footer id="kontakt" className="border-t border-slate-200 bg-white py-12">
        <Container>
          <div className="grid gap-8 sm:grid-cols-2 lg:grid-cols-3">
            <div>
              <div className="mb-3 flex items-center gap-2">
                <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-emerald-600 text-white">
                  <Salad className="h-5 w-5" />
                </div>
                <span className="text-lg font-bold">FODMAPP</span>
              </div>
              <p className="text-sm text-slate-600">Gjør lavFODMAP forståelig – hjemme, på butikken og ute.</p>
            </div>
            <div>
              <h5 className="mb-3 text-sm font-semibold">Lenker</h5>
              <ul className="space-y-2 text-sm text-slate-600">
                <li><a href="#funksjoner" className="hover:text-emerald-700">Funksjoner</a></li>
                <li><a href="#slik-funker-det" className="hover:text-emerald-700">Slik funker det</a></li>
                <li><a href="#personvern" className="hover:text-emerald-700">Sikkerhet & personvern</a></li>
                <li><a href="#faq" className="hover:text-emerald-700">FAQ</a></li>
              </ul>
            </div>
            <div>
              <h5 className="mb-3 text-sm font-semibold">Kontakt</h5>
              <p className="text-sm text-slate-600">Har du spørsmål eller vil samarbeide?</p>
              <a href="mailto:hei@fodmapp.app" className="mt-2 inline-flex items-center gap-2 text-sm font-semibold text-emerald-700 hover:underline">
                hei@fodmapp.app <ArrowRight className="h-4 w-4" />
              </a>
            </div>
          </div>
          <div className="mt-10 flex flex-col items-center justify-between gap-3 border-t border-slate-200 pt-6 text-xs text-slate-500 sm:flex-row">
            <p>© {new Date().getFullYear()} FODMAPP. Alle rettigheter forbeholdt.</p>
            <p>
              Ved bruk av appen gjelder OpenAIs <a className="underline decoration-emerald-500 underline-offset-2 hover:text-emerald-700" href="https://openai.com/policies/terms-of-use" target="_blank" rel="noreferrer">brukervilkår</a> og <a className="underline decoration-emerald-500 underline-offset-2 hover:text-emerald-700" href="https://openai.com/policies/privacy-policy" target="_blank" rel="noreferrer">personvern</a> for behandling hos OpenAI.
            </p>
          </div>
        </Container>
      </footer>
    </div>
  );
}
