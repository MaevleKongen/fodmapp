# i18n-verktøy

Små hjelpeskript for `js/i18n.js`, som holder 23 språk i én fil. Filen er stor nok til at
manuell redigering fort gir ubalanserte tagger eller nøkler som mangler på ett språk.

## `inject.py`

Setter inn eller oppdaterer nøkler i én eller flere språkblokker.

```
python3 _internal/tools/i18n/inject.py <fil.json> [<fil.json> ...]
```

Hver JSON-fil har formen `{"<språkkode>": {"<nøkkel>": "<verdi med HTML>", ...}, ...}`.
Verdiene skrives som vanlig tekst — skriptet håndterer JS-escaping. Nøkler som finnes fra
før blir overskrevet, nye legges til øverst i blokken.

## `validate.js`

```
node _internal/tools/i18n/validate.js [nøkkelfil.json]
```

Laster `js/i18n.js` i et funksjonsscope med stubbet `localStorage` og `document`, og sjekker

- at alle språk i `LANGS` har en blokk,
- at alle nøkler i nøkkelfilen finnes og ikke er tomme på hvert språk,
- at `<ul>`, `<li>`, `<strong>`, `<h3>`, `<p>`, `<div>` og `<a>` balanserer i hver verdi.

Uten argument brukes `req_keys.json`, som lister nøklene fra vilkårene,
personvernerklæringen og de delte sidetekstene. Exit-kode 1 ved feil.

## `bygg_spraak.py`

Bygger de statiske språksidene. `js/i18n.js` og de engelske rotsidene er kilden. Hver side finnes ferdig oversatt som
`/<språk>/<side>.html` (`/no/`, `/pl/`, `/zh-hans/` ...), med `lang`, `dir`, title, beskrivelse, canonical, hreflang og
butikklenker per land, og teksten står i HTML-en uten JavaScript. Sidene laster bare `js/spraak.js`, ikke `js/i18n.js`.

```
python -X utf8 _internal/tools/i18n/bygg_spraak.py           # idempotent
python -X utf8 _internal/tools/i18n/bygg_spraak.py --sjekk   # exit 1 hvis noe er utdatert
python -X utf8 _internal/tools/i18n/kontroll_spraak.py       # alle språk x alle sider
```

Etter enhver tekstendring: `inject.py` (eller ditt eget skript) → den statiske engelske HTML-en → `validate.js` →
`bygg_spraak.py` → `kontroll_spraak.py`, og publiser språkmappene sammen med endringen. Rediger aldri filene i
språkmappene for hånd. Ikke legg til `.nojekyll`: da blir `_internal/` synlig på nettet (se `_config.yml`).

## Merk

Verdiene legges inn som HTML i språksidene (`bygg_spraak.py`), ikke som ren tekst. HTML i verdiene er derfor tilsiktet
— og betyr at ubalanserte tagger ødelegger sidestrukturen. Kjør `validate.js` etter enhver
endring i `js/i18n.js`.
