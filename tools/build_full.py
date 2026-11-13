#!/usr/bin/env python3
"""Make the single-file release: ASTERID.html with gpt3_1.bin (window.__GPT3_B64), opole_0p5.bin (window.__OPOLE_B64),
otl_fes2014b_1.bin (window.__OTL_B64) and apl_rp_1.bin (window.__APL_B64) embedded as base64.

usage: python3 build_full.py ASTERID.html gpt3_1.bin opole_0p5.bin otl_fes2014b_1.bin apl_rp_1.bin ASTERID_full.html
The result is about 33 MiB: too big for the 25 MiB browser upload of the repository, fine for a GitHub Release asset.
Opened from file:// it needs no .bin file next to it.
"""
import sys, base64
html, gbin, obin, tbin, abin, out = sys.argv[1:7]
s = open(html, encoding='utf8').read()
KEYS = ('__GPT3_B64', '__OPOLE_B64', '__OTL_B64', '__APL_B64')
assert s.count('</body>') == 1 and not any(('window.' + k + '="') in s for k in KEYS)
b = [base64.b64encode(open(f, 'rb').read()).decode() for f in (gbin, obin, tbin, abin)]
i = s.rindex('</body>')
s = s[:i] + '<script>' + ''.join('window.' + k + '="' + v + '";' for k, v in zip(KEYS, b)) + '</script>\n' + s[i:]
open(out, 'w', encoding='utf8').write(s)
print(out, round(len(s.encode('utf8')) / 2**20, 2), 'MiB')
