#!/usr/bin/env python3
"""build_apl_bin.py - global S1/S2-family atmospheric pressure loading grid for ASTERID.

Input : Ray_Ponte_2003_mbar.txt   Ray & Ponte (2003) atmospheric tide, pressure in mbar, fully normalised
                                  spherical-harmonic coefficients (P1, S1, K1, T2, S2, R2; degree/order 10, S1 to 20)
        load_Love_numbers_from_Gegout_250.txt   n, h'_n, l'_n, k'_n (Gegout)
Output: apl_rp_1.bin  (1 deg x 1 deg cell centres, north first; 6 waves x (C, S) radial displacement, m)

Method (radial only, as the station chain aplRad):
  p(phi,lam,t) = sum_lm Pbar_lm(sin phi) [ C+ cos(chi + m lam - eps+) + C- cos(chi - m lam - eps-) ]  (x (-1)^m, Condon-Shortley)
  u_r = (3/rho_E) sum_n h'_n/(2n+1) * (p_n/g)          rho_E = 5517 kg/m3, g = 9.80665 m/s2, p in Pa
  u_r = Re[(C + iS) exp(i chi)]  with chi the Doodson argument that aplRad() builds from the Doodson number.
File layout (little endian): 'APLB', u8 version=1, u8 nc=12, u16 nla=180, u16 nlo=360, u16 0, u32 raw length,
  u32 CRC-32(raw), then raw-deflate(raw); raw = float64 step[nc], then per column: int32 base[nla], int16 delta[nla*nlo]
  (value = base + running sum of delta along longitude; physical value = value*step[column]).
Usage: python3 build_apl_bin.py Ray_Ponte_2003_mbar.txt load_Love_numbers_from_Gegout_250.txt [apl_rp_1.bin]
"""
import sys, math, zlib, struct
import numpy as np

CON = ['P1', 'S1', 'K1', 'T2', 'S2', 'R2']
G, RHOE = 9.80665, 5517.0
NLA, NLO = 180, 360

def read_rp(path):
    rows = []
    for ln in open(path).read().replace('\r', '').split('\n')[3:]:
        p = ln.split()
        if len(p) >= 12:
            rows.append((p[1], int(p[2]), int(p[3])) + tuple(map(float, p[4:])))
    return rows

def read_love(path):
    h = {}
    for ln in open(path):
        p = ln.replace('D', 'E').split()
        if len(p) >= 4:
            h[int(p[0])] = float(p[1])
    return h

def pbar(lmax, x):
    """fully normalised associated Legendre functions (no Condon-Shortley phase), x = sin(lat), array -> P[l][m] arrays"""
    x = np.asarray(x, float); u = np.sqrt(1 - x * x)
    P = np.zeros((lmax + 1, lmax + 1) + x.shape)
    P[0, 0] = 1.0
    for m in range(1, lmax + 1):
        P[m, m] = (math.sqrt(3.0) if m == 1 else math.sqrt((2 * m + 1) / (2.0 * m))) * u * P[m - 1, m - 1]
    for m in range(0, lmax):
        P[m + 1, m] = math.sqrt(2 * m + 3) * x * P[m, m]
    for m in range(0, lmax + 1):
        for l in range(m + 2, lmax + 1):
            a = math.sqrt((4.0 * l * l - 1) / (l * l - m * m)); b = math.sqrt(((l - 1.0) ** 2 - m * m) / (4.0 * (l - 1) ** 2 - 1))
            P[l, m] = a * (x * P[l - 1, m] - b * P[l - 2, m])
    return P

def synth(rows, love, con, lat, lon):
    """complex radial amplitude (m) at arrays lat (n,), lon (k,) -> (n,k)"""
    lmax = max(r[1] for r in rows if r[0] == con)
    P = pbar(lmax, np.sin(np.radians(lat))); lam = np.radians(lon)
    out = np.zeros((len(lat), len(lon)), complex)
    for r in rows:
        if r[0] != con: continue
        l, m = r[1], r[2]; Csp, Ccp, Csm, Ccm = r[3:7]
        cp, cm = math.hypot(Csp, Ccp), math.hypot(Csm, Ccm); ep, em = math.atan2(Csp, Ccp), math.atan2(Csm, Ccm)
        z = cp * np.exp(1j * (m * lam - ep)) + cm * np.exp(1j * (-m * lam - em))        # (k,)
        out += (-1) ** m * (3.0 / RHOE * love[l] / (2 * l + 1) * 100.0 / G) * P[l, m][:, None] * z[None, :]
    return out

def main():
    rp, lv = read_rp(sys.argv[1]), read_love(sys.argv[2]); outp = sys.argv[3] if len(sys.argv) > 3 else 'apl_rp_1.bin'
    lat = 90 - 0.5 - np.arange(NLA); lon = 0.5 + np.arange(NLO)
    cols = []
    for c in CON:
        u = synth(rp, lv, c, lat, lon); cols += [u.real, u.imag]
    steps, blocks = [], []
    for a in cols:
        dmax = 0.0
        step = 1e-8
        q = np.rint(a / step).astype(np.int64)
        d = np.diff(q, axis=1); dmax = np.abs(d).max()
        if dmax > 32000:
            step = 1e-8 * math.ceil(dmax / 32000 * 10) / 10; q = np.rint(a / step).astype(np.int64); d = np.diff(q, axis=1)
        delta = np.zeros_like(q); delta[:, 1:] = d
        assert np.abs(delta).max() < 32768
        steps.append(step); blocks.append(q[:, 0].astype('<i4').tobytes() + delta.astype('<i2').tobytes())
    raw = np.array(steps, '<f8').tobytes() + b''.join(blocks)
    co = zlib.compressobj(9, zlib.DEFLATED, -15); z = co.compress(raw) + co.flush()
    hdr = b'APLB' + struct.pack('<BBHHHII', 1, 12, NLA, NLO, 0, len(raw), zlib.crc32(raw) & 0xFFFFFFFF)
    open(outp, 'wb').write(hdr + z)
    print('wrote', outp, len(hdr + z), 'bytes; raw', len(raw), '; steps', steps)

if __name__ == '__main__':
    main()
