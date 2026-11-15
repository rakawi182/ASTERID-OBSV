#!/usr/bin/env python3
"""Make the single-file release: ASTERID.html with gpt3_1.bin (window.__GPT3_B64), opole_0p5.bin (window.__OPOLE_B64),
otl_fes2014b_1.bin (window.__OTL_B64), apl_rp_1.bin (window.__APL_B64) and the VSOP2013 planet files
(window.__VSOP_B64 = {mercury:..., venus:..., ...}, placed in <head>) embedded as base64.

usage: python3 build_full.py ASTERID.html gpt3_1.bin opole_0p5.bin otl_fes2014b_1.bin apl_rp_1.bin ASTERID_full.html [vsop2013_<planet>.bin ...]
If no VSOP2013 file is given, every vsop2013_*.bin next to ASTERID.html is used.
Each VSOP2013 key is the planet name (= VSP.NM in ASTERID.html); it is taken from the file name and checked against the
planet index in the .bin header (VS13/VS14), so a misnamed file is rejected. The result is far above 25 MiB: too big for the
25 MiB browser upload of the repository, fine for a GitHub Release asset.
Opened from file:// it needs no .bin file next to it.
"""
import sys, os, re, glob, json, base64

NM = {1: 'mercury', 2: 'venus', 4: 'mars', 5: 'jupiter', 6: 'saturn', 7: 'uranus', 8: 'neptune'}  # VSOP2013 index -> VSP.NM

def vsop_key(path):
    b = open(path, 'rb').read()
    assert b[:4] in (b'VS13', b'VS14'), path + ': not a vsop2013 .bin file'
    name = NM.get(b[4])
    assert name, path + ': unknown planet index %d in header' % b[4]
    m = re.fullmatch(r'vsop2013_([a-z]+)\.bin', os.path.basename(path))
    assert m and m.group(1) == name, path + ': file name does not match planet in header (' + name + ')'
    return name, b

def main():
    html, gbin, obin, tbin, abin, out = sys.argv[1:7]
    vs = sys.argv[7:] or sorted(glob.glob(os.path.join(os.path.dirname(os.path.abspath(html)), 'vsop2013_*.bin')))
    s = open(html, encoding='utf8').read()
    KEYS = ('__GPT3_B64', '__OPOLE_B64', '__OTL_B64', '__APL_B64')
    assert s.count('</body>') == 1 and not any(('window.' + k + '="') in s for k in KEYS) and 'window.__VSOP_B64={' not in s
    assert s.count('</head>') == 1 and s.index('</head>') < s.index('<script')
    assert vs, 'no vsop2013_*.bin found'
    v = {}
    for f in vs:
        name, b = vsop_key(f)
        assert name not in v, 'duplicate planet: ' + name
        v[name] = base64.b64encode(b).decode()
    b = [base64.b64encode(open(f, 'rb').read()).decode() for f in (gbin, obin, tbin, abin)]
    js = ''.join('window.' + k + '="' + x + '";' for k, x in zip(KEYS, b))
    i = s.rindex('</body>')
    s = s[:i] + '<script>' + js + '</script>\n' + s[i:]
    # VSOP2013 goes into <head>: the planet code asks for its .bin during start-up, before a script at the end of <body> has run
    # (then the load fails and the status stays 'fail'); the four lazily used files above are fine at the end.
    i = s.index('</head>')
    s = s[:i] + '<script>window.__VSOP_B64=' + json.dumps(v, separators=(',', ':')) + ';</script>\n' + s[i:]
    open(out, 'w', encoding='utf8', newline='').write(s)
    print('VSOP2013 embedded:', ', '.join(sorted(v, key=lambda n: list(NM.values()).index(n))))
    if len(v) < 7:
        print('WARNING: only %d of 7 planets embedded. Outside 500-2498 CE the missing planets are not shown (there is no fallback there); inside it they fall back to IPS2000.' % len(v))
    print(out, round(len(s.encode('utf8')) / 2**20, 2), 'MiB')

main()
