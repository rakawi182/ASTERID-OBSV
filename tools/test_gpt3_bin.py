#!/usr/bin/env python3
"""Check ASTERID's GPT3 grid decoder (gpt3At in ASTERID.html + gpt3_1.bin) against gpt3_1.npz.

usage: python3 test_gpt3_bin.py ASTERID.html gpt3_1.npz gpt3_1.bin      (needs Node.js and NumPy)
The JavaScript pieces (inflate, GPT3 core, grid decoder) are cut out of ASTERID.html and run in Node; the reference is a
Python port of the same GPT3 formulas applied to the exact .npz coefficients, so the differences printed here are
only the effect of the file format (Hs rounded to 0.1 m), the decoder and the grid indexing.
"""
import sys, re, json, math, datetime, subprocess, tempfile, os
import numpy as np

html, npz, binf = sys.argv[1:4]
s = open(html, encoding='utf8').read()
zl = re.search(r'<script id="zl">\n(.*?)\nconst __zt', s, re.S).group(1)
vm = s[s.index('const VMS='):s.index('const LATD=')]
core = s[s.index('function doyOf'):s.index('/* ---- refraction: two-component')]
d = np.load(npz)
rng = np.random.default_rng(7)
pts = [[float(rng.uniform(-89.9, 89.9)), float(rng.uniform(-180, 360)), float(rng.uniform(51544, 88069)),
        None if rng.random() < .5 else float(rng.uniform(-50, 4500))] for _ in range(400)]
pts += [[89.9, 10, 60000.3, None], [-89.9, 200, 60000.3, None], [0.1, 0.1, 60000.3, 0], [10, 359.9, 60000.3, 100],
        [10, -0.2, 60000.3, 100], [10, 180, 60000.3, None], [10, -180, 60000.3, None], [-7.609444, 112.595556, 61000.7, 583.355]]
tmp = tempfile.mkdtemp()
open(f'{tmp}/m.js', 'w').write(zl + '\n' + vm + '\n' + core + '\nmodule.exports={gpt3,gpt3At,g3Parse};\n')
open(f'{tmp}/pts.json', 'w').write(json.dumps(pts))
js = f"""const m=require('{tmp}/m.js'),fs=require('fs');const b=fs.readFileSync({json.dumps(binf)});
m.g3Parse(b.buffer.slice(b.byteOffset,b.byteOffset+b.length));const pts=JSON.parse(fs.readFileSync('{tmp}/pts.json'));
console.log(JSON.stringify(pts.map(p=>{{const r=m.gpt3At(p[0],p[1],p[2],p[3]);return [r.p,r.T,r.e,r.undu,r.ah,r.aw,r.h]}})))
const st=m.gpt3At(-7.609444,112.595556,61000.7,583.355),ex=m.gpt3(61000.7,583.355);
console.error(JSON.stringify([st.p-ex.p,st.T-ex.T,st.e-ex.e,st.ah-ex.ah,st.aw-ex.aw]))"""
r = subprocess.run(['node', '-e', js], capture_output=True, text=True, check=True)
out = json.loads(r.stdout)

def doy(mjd):
    t = datetime.datetime(1970, 1, 1) + datetime.timedelta(days=mjd - 40587)
    return (t - datetime.datetime(t.year, 1, 1)).total_seconds() / 86400 + 1

def ref(lat, lon, mjd, h):
    lat = max(-89.5, min(89.5, lat)); x = ((lon - .5) % 360 + 360) % 360
    i0 = min(178, math.floor(89.5 - lat)); j0 = math.floor(x); j1 = (j0 + 1) % 360
    wp = 89.5 - lat - i0; wl = x - j0; ids = [i0*360+j0, (i0+1)*360+j0, i0*360+j1, (i0+1)*360+j1]
    a = doy(mjd) / 365.25 * 2 * math.pi; cf, sf, ch, sh = math.cos(a), math.sin(a), math.cos(2*a), math.sin(2*a)
    ip = lambda r: (1-wl)*((1-wp)*r[0]+wp*r[1]) + wl*((1-wp)*r[2]+wp*r[3])
    if h is None: h = ip([d['Hs'][i] + d['undu'][i] for i in ids])
    P, T, E, U, AH, AW = [], [], [], [], [], []
    for i in ids:
        S = lambda k, sc=1: (lambda c: c[0]+c[1]*cf+c[2]*sf+c[3]*ch+c[4]*sh)([v*sc for v in d[k][i]])
        un = d['undu'][i]; red = h - un - d['Hs'][i]
        T0, p0, Q, dTi = S('T'), S('p'), S('Q', 1e-3), S('dT', 1e-3)
        Tv = T0*(1+.6077*Q); cc = 9.80665*28.965e-3/(8.3143*Tv) if Tv > 0 else 0
        pi = p0*math.exp(-cc*red)/100; e0 = Q*p0/(.622+.378*Q)/100
        P.append(pi); T.append(T0+dTi*red-273.15); E.append(e0*(100*pi/p0)**(S('la')+1)); U.append(un)
        AH.append(S('ah', 1e-3)); AW.append(S('aw', 1e-3))
    return [ip(P), ip(T), ip(E), ip(U), ip(AH), ip(AW), h]

errs = np.array([[abs(a-b) for a, b in zip(ref(*p), o)] for p, o in zip(pts, out)])
print(len(pts), 'sites (random, poles, longitude wrap), model height and given height')
for n, e in zip(['p hPa', 'T K', 'e hPa', 'undulation m', 'a_h', 'a_w', 'h m'], errs.T):
    print(f'max |JS(bin) - reference(npz)|  {n:13s} {e.max():.3e}')
print('station, bin vs the four embedded cells (p hPa, T K, e hPa, a_h, a_w):', r.stderr.strip())
