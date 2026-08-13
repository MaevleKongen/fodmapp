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

## Merk

`applyLang()` setter `el.innerHTML`, ikke `textContent`. HTML i verdiene er derfor tilsiktet
— og betyr at ubalanserte tagger ødelegger sidestrukturen. Kjør `validate.js` etter enhver
endring i `js/i18n.js`.
