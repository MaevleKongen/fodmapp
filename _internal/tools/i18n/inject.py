#!/usr/bin/env python3
"""Inject/update i18n keys into js/i18n.js for one or more languages.

Usage: inject.py <json-file> [<json-file> ...]
Each JSON file: {"<lang>": {"<key>": "<value with HTML>", ...}, ...}
Values are plain (unescaped) strings; this script handles JS string escaping.
"""
import json, pathlib, re, sys

I18N = pathlib.Path(__file__).resolve().parents[3] / 'js' / 'i18n.js'


def js_escape(s: str) -> str:
    """Escape for a double-quoted JS string literal."""
    return json.dumps(s, ensure_ascii=False)[1:-1]


def find_lang_block(src: str, lang: str):
    m = re.search(r'\n  "' + re.escape(lang) + r'": \{', src)
    if not m:
        raise KeyError(f'language block not found: {lang}')
    start = m.end()
    # block ends at the next closing brace indented by exactly 2 spaces.
    # (the final language block ends "\n  }\n};" rather than "\n  },")
    e = re.search(r'\n  \}', src[start:])
    if not e:
        raise ValueError(f'unterminated block for {lang}')
    return start, start + e.start()


def find_value_span(block: str, key: str):
    """Return (value_start, value_end) inside block for "key": "...", or None."""
    m = re.search(r'"' + re.escape(key) + r'"\s*:\s*"', block)
    if not m:
        return None
    i = m.end()
    while i < len(block):
        c = block[i]
        if c == '\\':
            i += 2
            continue
        if c == '"':
            return m.end(), i
        i += 1
    raise ValueError(f'unterminated string for key {key}')


def inject(src: str, lang: str, kv: dict):
    start, end = find_lang_block(src, lang)
    block = src[start:end]
    updated = added = 0
    for key, val in kv.items():
        esc = js_escape(val)
        span = find_value_span(block, key)
        if span:
            block = block[:span[0]] + esc + block[span[1]:]
            updated += 1
        else:
            block = '\n    "' + key + '": "' + esc + '",' + block
            added += 1
    return src[:start] + block + src[end:], updated, added


def main():
    src = I18N.read_text(encoding='utf-8')
    total_u = total_a = 0
    for f in sys.argv[1:]:
        data = json.loads(pathlib.Path(f).read_text(encoding='utf-8'))
        for lang, kv in data.items():
            src, u, a = inject(src, lang, kv)
            total_u += u
            total_a += a
            print(f'  {lang:8} updated={u:3} added={a:3}')
    I18N.write_text(src, encoding='utf-8')
    print(f'TOTAL updated={total_u} added={total_a}')


if __name__ == '__main__':
    main()
