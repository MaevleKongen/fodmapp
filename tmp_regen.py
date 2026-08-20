# -*- coding: utf-8 -*-
import re, json
src = open("js/i18n.js", encoding="utf-8").read()
m = re.search(r'
  "en": \{(.*?)
  \}', src, re.S)
out = {}
for mm in re.finditer(r'"((?:[^"\\]|\\.)+)": "((?:[^"\\]|\\.)*)"', m.group(1)):
    out[json.loads('"' + mm.group(1) + '"')] = json.loads('"' + mm.group(2) + '"')
with open("_internal/tools/i18n/req_keys.json", "w", encoding="utf-8", newline="
") as g:
    json.dump({"en": out}, g, ensure_ascii=False)
print("req_keys:", len(out))
