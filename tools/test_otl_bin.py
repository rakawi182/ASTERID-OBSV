#!/usr/bin/env python3
"""Check otl_fes2014b_1.bin and its decoder (otl_decoder.js), and measure what the grid costs in accuracy.

usage: python3 test_otl_bin.py ASTERID.html otl_fes2014b_1.bin [folder_with_inputs=.]   (needs Node.js and NumPy; build_otl_bin.py in the same folder)
1) decoder (JavaScript, ASTERID's own inflate + crc) vs bilinear interpolation of the exact float64 grid, 400 random points + edge cases.
2) bilinear grid vs the spherical-harmonic synthesis evaluated directly at the same points (interpolation error of the grid),
   over the globe and in the Indonesian region (-12..8 N, 94..142 E).
3) the station Jolotundo (-7.609444, 112.595556): grid result vs the BLQ values of ASTERID (OD.blq, 11 waves x U/W/S).
"""
import sys, re, json, subprocess, tempfile, os
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_otl_bin as B
html, binf = sys.argv[1:3]; folder = sys.argv[3] if len(sys.argv) > 3 else '.'
s = open(html, encoding='utf8').read()
zl = re.search(r'<script id="zl">\n(.*?)\nconst __zt', s, re.S).group(1)
crc = s[s.index('function g3crc'):s.index('function g3Parse')]
dec = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'otl_decoder.js')).read()
a = s.index('"blq":{'); b = s.index('},"apls"', a); BLQ = json.loads(s[a + 6:b + 1])
tmp = tempfile.mkdtemp(); open(f'{tmp}/m.js', 'w').write(zl + '\n' + crc + '\n' + dec + '\nmodule.exports={otParse,otGrid};\n')
rng = np.random.default_rng(5)
pts = [[float(rng.uniform(-89.9, 89.9)), float(rng.uniform(-180, 360))] for _ in range(400)]
pts += [[-7.609444, 112.595556], [89.99, .1], [-89.99, 359.99], [.1, 359.9], [.1, 0.], [-43.75, -127.75]]
reg = [[float(rng.uniform(-12, 8)), float(rng.uniform(94, 142))] for _ in range(300)]
json.dump({'p': pts + reg}, open(f'{tmp}/in.json', 'w'))
js = f"""const m=require('{tmp}/m.js'),fs=require('fs');const b=fs.readFileSync({json.dumps(binf)});m.otParse(b.buffer.slice(b.byteOffset,b.byteOffset+b.length));
const I=JSON.parse(fs.readFileSync('{tmp}/in.json'));console.log(JSON.stringify(I.p.map(p=>m.otGrid(p[0],p[1]))))"""
o = json.loads(subprocess.run(['node', '-e', js], capture_output=True, text=True, check=True).stdout)
# exact float64 grid and direct SH
hdr = open(binf, 'rb').read(12); nla, nlo = np.frombuffer(hdr[6:10], '<u2'); res = 180.0 / nla
h, l = B.love(folder); C = B.coefs(folder)
la = np.deg2rad(np.array([p[0] for p in pts + reg])); lo_ = np.deg2rad(np.array([p[1] for p in pts + reg]))
nla_, nlo_, glat, glon = B.grid(res); Pg = B.plm(np.deg2rad(glat))
Pp = B.plm(la); G = {}; D = {}
for w in B.WAVES:
    Zu, Ze, Zn = B.synth(C[w], w, np.deg2rad(glat), np.deg2rad(glon), h, l, Pg); G[w] = [x for x in B.blq_columns(Zu, Ze, Zn, w)]
    # direct SH at each point: synthesise the full (points x points) block once per wave and take the diagonal
    Zu, Ze, Zn = B.synth(C[w], w, la, lo_, h, l, Pp)
    cc = B.blq_columns(Zu, Ze, Zn, w); d = np.stack([np.diag(c) for c in cc], axis=1)
    D[w] = d
def bil(g, lat, lon):
    y = min(nla_ - 1, max(0, (90 - res / 2 - lat) / res)); i0 = min(nla_ - 2, int(np.floor(y))); ty = y - i0
    x = ((lon - res / 2) / res) % nlo_; j0 = int(np.floor(x)) % nlo_; j1 = (j0 + 1) % nlo_; tx = x - np.floor(x)
    return (1 - tx) * (1 - ty) * g[i0, j0] + tx * (1 - ty) * g[i0, j1] + (1 - tx) * ty * g[i0 + 1, j0] + tx * ty * g[i0 + 1, j1]
n0 = len(pts); mx1 = 0; mx2 = np.zeros(2); rms2 = [[], []]
for i, (la_, lo2) in enumerate([(p[0], p[1]) for p in pts + reg]):
    for k, w in enumerate(B.WAVES):
        ref = np.array([bil(G[w][c], la_, lo2) for c in range(6)])           # Re/Im of U, W, S
        j = np.array(o[i][w]).reshape(3, 2)                                   # A, phi(deg)
        zj = np.array([j[q, 0] * np.exp(1j * np.deg2rad(j[q, 1])) for q in range(3)])
        zr = ref[0::2] + 1j * ref[1::2]
        mx1 = max(mx1, abs(zj - zr).max())
        zd = D[w][i][0::2] + 1j * D[w][i][1::2]
        e = abs(zr - zd).max(); g = 0 if i < n0 else 1
        rms2[g].append(abs(zr - zd)); mx2[g] = max(mx2[g], e)
print('1) decoder vs float64 bilinear of the same grid, %d points x 11 waves x 3: max |diff| = %.2e m' % (n0 + len(reg), mx1))
for g, name in ((0, 'globe (406 pts)'), (1, 'Indonesia (300 pts)')):
    r = np.concatenate([x.ravel() for x in rms2[g]])
    print('2) grid (bilinear, %.2f deg) vs direct SH, %-20s: max %.3f mm, rms %.4f mm' % (res, name, mx2[g] * 1e3, np.sqrt(np.mean(r ** 2)) * 1e3))
i = n0 - 6
print('3) station Jolotundo, grid vs BLQ (ASTERID OD.blq):')
tot = []
for w in B.WAVES:
    zj = np.array(o[i][w]).reshape(3, 2); r = BLQ[w]
    for q, nm in enumerate('UWS'):
        zg = zj[q, 0] * np.exp(1j * np.deg2rad(zj[q, 1])); zb = r[2 * q] * np.exp(1j * np.deg2rad(r[2 * q + 1])); tot.append((w, nm, abs(zg - zb) * 1e3, zj[q, 0] * 1e3, r[2 * q] * 1e3))
d = np.array([t[2] for t in tot])
print('   33 values: rms |dZ| = %.3f mm, max = %.3f mm (%s %s); radial only: rms %.3f mm' % (np.sqrt(np.mean(d ** 2)), d.max(), *tot[int(d.argmax())][:2], np.sqrt(np.mean([t[2] ** 2 for t in tot if t[1] == 'U']))))
for t in tot:
    if t[1] == 'U' and t[0] in ('M2', 'S2', 'K1', 'O1'): print('   %-3s radial grid %.2f mm, BLQ %.2f mm, |dZ| %.2f mm' % (t[0], t[3], t[4], t[2]))
