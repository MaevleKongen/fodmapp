const fs = require('fs');
const path = require('path');
const ROOT = path.resolve(__dirname, '..', '..', '..');
const src = fs.readFileSync(path.join(ROOT, 'js', 'i18n.js'), 'utf8');
// evaluate the file in a function scope, stubbing the browser globals it touches
const load = new Function(
  'localStorage', 'document',
  src.replace(/^const /gm, 'var ') + '\nreturn { T: T, LANGS: LANGS };'
);
const { T, LANGS } = load(
  { getItem: () => null, setItem: () => {} },
  { documentElement: {}, querySelectorAll: () => [], getElementById: () => null, createElement: () => ({}) }
);

const reqFile = process.argv[2] || path.join(__dirname, 'req_keys.json');
const req = Object.keys(JSON.parse(fs.readFileSync(reqFile, 'utf8')).en || {});
console.log('languages in T:', Object.keys(T).length, '| LANGS listed:', LANGS.length);

let bad = 0;
for (const code of LANGS.map((l) => l.code)) {
  if (!T[code]) { console.log('MISSING LANG BLOCK:', code); bad++; continue; }
  const miss = req.filter((k) => !(k in T[code]));
  const empty = req.filter((k) => k in T[code] && !String(T[code][k]).trim());
  if (miss.length || empty.length) {
    bad++;
    console.log(`${code}: missing=${miss.length} empty=${empty.length} ${miss.slice(0, 8).join(',')}`);
  }
}

// structural sanity: unbalanced tags inside translated values
const tagRe = /<(\/?)(ul|li|strong|h3|p|div|a)\b/gi;
for (const code of Object.keys(T)) {
  for (const k of req) {
    const v = T[code][k];
    if (!v) continue;
    const counts = {};
    let m;
    while ((m = tagRe.exec(v))) {
      const t = m[2].toLowerCase();
      counts[t] = (counts[t] || 0) + (m[1] ? -1 : 1);
    }
    for (const [t, n] of Object.entries(counts)) {
      if (n !== 0 && t !== 'br') {
        console.log(`UNBALANCED <${t}> (${n}) in ${code}.${k}`);
        bad++;
      }
    }
  }
}

console.log(bad ? `FAILED (${bad} issues)` : `OK: all ${LANGS.length} languages have all ${req.length} keys, tags balanced`);
process.exit(bad ? 1 : 0);
