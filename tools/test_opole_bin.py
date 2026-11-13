#!/usr/bin/env python3
"""Check ASTERID's ocean pole tide grid decoder (opParse/opGrid in ASTERID.html + opole_0p5.bin).

usage: python3 test_opole_bin.py ASTERID.html opoleloadcoefcmcor.npz opole_0p5.bin opoleloadcmcor.txt   (needs Node.js and NumPy)
1) 500 random points + edge cases (pole, date line, 0 deg): JavaScript decoder vs bilinear interpolation of the exact .npz in float64.
2) IERS/Desai test case (opoleloadcmcor.txt; lat -43.75, lon 232.25; the 731-day series of m1, m2 and u_radial, u_north, u_east):
   pole offsets taken from the test file, displacement from the decoder.
"""
import sys, re, json, subprocess, tempfile
import numpy as np
html, npz, binf, tst = sys.argv[1:5]
s = open(html, encoding='utf8').read()
zl = re.search(r'<script id="zl">\n(.*?)\nconst __zt', s, re.S).group(1)
crc = s[s.index('function g3crc'):s.index('function g3Parse')]
op = s[s.index('const OP={'):s.index('/* ---- frames ---- */')]
tmp = tempfile.mkdtemp()
open(f'{tmp}/m.js', 'w').write(zl + '\n' + crc + '\n' + op + '\nmodule.exports={opParse,opGrid};\n')
A = 4.84813681109536e-6
G = np.load(npz)['load_coef'].reshape(360, 720, 8)
rng = np.random.default_rng(3)
pts = [[float(rng.uniform(-89.9, 89.9)), float(rng.uniform(-180, 360)), float(rng.uniform(-.4, .4)), float(rng.uniform(-.4, .4))] for _ in range(500)]
pts += [[-43.75, 232.25, .1, .2], [-43.75, -127.75, .1, .2], [89.99, .1, .1, .2], [-89.99, 359.99, .1, .2], [.1, 359.9, .1, .2], [.1, 0., .1, .2]]
T = np.array([r.split() for r in open(tst).read().splitlines()[26:] if r.strip()], float)
json.dump({'pts': pts, 'iers': T[:, [5, 6]].tolist()}, open(f'{tmp}/in.json', 'w'))
js = f"""const m=require('{tmp}/m.js'),fs=require('fs');const b=fs.readFileSync({json.dumps(binf)});
m.opParse(b.buffer.slice(b.byteOffset,b.byteOffset+b.length));const I=JSON.parse(fs.readFileSync('{tmp}/in.json')),A={A};
console.log(JSON.stringify({{pts:I.pts.map(p=>m.opGrid(p[2]*A,p[3]*A,p[0],p[1])),iers:I.iers.map(p=>m.opGrid(p[0]*A,p[1]*A,-43.75,232.25))}}))"""
o = json.loads(subprocess.run(['node', '-e', js], capture_output=True, text=True, check=True).stdout)

def ref(lat, lon, m1, m2):
    y = min(359, max(0, (lat + 89.75) / .5)); i0 = min(358, int(np.floor(y))); ty = y - i0
    x = ((lon - .25) / .5) % 720; j0 = int(np.floor(x)) % 720; j1 = (j0 + 1) % 720; tx = x - np.floor(x)
    c = ((1-tx)*(1-ty)*G[i0, j0] + tx*(1-ty)*G[i0, j1] + (1-tx)*ty*G[i0+1, j0] + tx*ty*G[i0+1, j1])[2:]
    a, b = m1 * A, m2 * A; K = 5.3394043696e3; t1 = a*.687 + b*.0036; t2 = b*.687 - a*.0036
    return [K*(t1*c[4]+t2*c[5]), K*(t1*c[2]+t2*c[3]), K*(t1*c[0]+t2*c[1])]
R = np.array([ref(*p) for p in [(p[0], p[1], p[2], p[3]) for p in pts]])
print('1) decoder vs float64 interpolation of the .npz, 506 points: max |diff| = %.2e m (max |value| %.2e m)' % (abs(np.array(o['pts']) - R).max(), abs(R).max()))
oi = np.array(o['iers'])
for name, k, c in (('radial', 7, 2), ('north', 8, 1), ('east', 9, 0)):
    d = oi[:, c] - T[:, k]
    print('2) IERS test case %-6s %d epochs: max |diff| = %.2e m (%.4f um), signal max %.3e m' % (name, len(T), abs(d).max(), abs(d).max() * 1e6, abs(T[:, k]).max()))
