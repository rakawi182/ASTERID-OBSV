"""python3 test_apl_bin.py Ray_Ponte_2003_mbar.txt load_Love_numbers_from_Gegout_250.txt ref.json - float64 reference (bilinear of direct synthesis on the same 1 deg cells) at random points, for test_apl_bin.js"""
import sys, json, numpy as np
from build_apl_bin import *
rp, lv = read_rp(sys.argv[1]), read_love(sys.argv[2])
lat = 90 - 0.5 - np.arange(NLA); lon = 0.5 + np.arange(NLO)
G_ = []
for c in CON:
    u = synth(rp, lv, c, lat, lon); G_ += [u.real, u.imag]
G_ = np.array(G_)
rng = np.random.default_rng(1); pts = []
for _ in range(500):
    la = rng.uniform(-89.5, 89.5); lo = rng.uniform(-180, 360)
    y = min(NLA - 1, max(0, 89.5 - la)); i0 = min(NLA - 2, int(np.floor(y))); ty = y - i0
    x = ((lo - 0.5) % NLO + NLO) % NLO; j0 = int(np.floor(x)) % NLO; j1 = (j0 + 1) % NLO; tx = x - np.floor(x)
    v = [(1-tx)*(1-ty)*c[i0, j0] + tx*(1-ty)*c[i0, j1] + (1-tx)*ty*c[i0+1, j0] + tx*ty*c[i0+1, j1] for c in G_]
    pts.append({'lat': la, 'lon': lo, 'v': v})
json.dump({'pts': pts}, open(sys.argv[3], 'w'))
print('amplitude max over grid (mm):', {c: round(float(np.hypot(G_[2*k], G_[2*k+1]).max()*1e3), 3) for k, c in enumerate(CON)})
