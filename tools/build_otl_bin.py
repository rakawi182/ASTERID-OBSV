#!/usr/bin/env python3
"""Build otl_fes2014b_1.bin: global ocean tide loading grid (FES2014b, spherical harmonics to degree/order 100) for ASTERID.

Why: ASTERID has ocean tide loading (OTL) only at the TOPOCENTRIC station (BLQ values + HARDISP-style admittance to 342 waves).
This file lets the same chain run at any HUD location: per grid cell it holds the BLQ-style complex amplitude of the 11 main waves
(M2 S2 N2 K2 K1 O1 P1 Q1 Mf Mm Ssa) for the radial, west and south displacement, so the decoder returns exactly the structure of OD.blq.

Inputs (all in the working folder or given on the command line)
  data_wh.npz   FES2014b.v1 water-height SH coefficients (cm), columns csin_*/ccos_* = Cbar, Sbar of IERS Conventions 2010 eq. 6.19-6.20
  load_Love_numbers_from_Gegout_250.txt   load Love numbers h'_n, l'_n, k'_n (degree 1 is 0 in that file, see H1/L1 below)

Method (IERS Conventions 2010, sec. 6.3.1 and 7.1.2; Farrell 1972)
  xi_f(lat,lon,t) = Re[ Z_xi e^{i theta_f} ],  Z_xi = e^{i chi_f} sum_n sum_m Pbar_nm(sin lat) sum_{+-} (Cbar - i Sbar) e^{+-i m lon}
  u_up    = 3 rho_w/rho_E sum_n h'_n /(2n+1) xi_n
  u_north = 3 rho_w/rho_E sum_n l'_n /(2n+1) d xi_n / d lat
  u_east  = 3 rho_w/rho_E sum_n l'_n /(2n+1) (1/cos lat) d xi_n / d lon        (rho_w 1025, rho_E 5517 kg/m3)
  BLQ form: u = A cos(theta_f + bias - phi), bias = 0 (semidiurnal), 90 (diurnal), 180 (long period) as in ASTERID otlDisp;
  stored per component: A cos(phi) and A sin(phi) (phi = BLQ phase lag, deg), so phi = atan2(Im, Re) after bilinear interpolation.
  Effective chi_f used here equals that bias for every wave. (The list on p. 3 of Explanations_about_FES2014b.pdf gives -90 / 0 for
  the waves with Hf<0 (Q1 O1 P1 Mf Mm Ssa); with it those waves come out 180 deg off against the station BLQ, with chi = bias they agree.)

Layout (little endian), same idea as gpt3_1.bin
  0   'OTLB'
  4   u8 version (1), u8 ncol (66), u16 nlat, u16 nlon, u16 0
  12  u32 rawLen   bytes after inflating the payload
  16  u32 crc32    of the inflated payload
  20  payload      raw DEFLATE of:
        ncol x (f64 lo, f64 step)                    column table
        ncol x nlat*nlon int16                       column-major; latitude rows (90-r/2 ... -90+r/2) delta coded along longitude
                                                      (r/2 ... 360-r/2), int16 wrap-around
  value (m) = lo + (q + 32768) * step      (q = decoded int16),  step = 1e-5 m
Columns: for w in (M2,S2,N2,K2,K1,O1,P1,Q1,Mf,Mm,Ssa): for comp in (U,W,S): Re, Im      (66 = 11 x 3 x 2)

usage: python3 build_otl_bin.py [res_deg=1.0] [out=otl_fes2014b_1.bin] [folder_with_inputs=.]
"""
import sys, struct, zlib, os
import numpy as np

LMAX = 100
WAVES = ['M2', 'S2', 'N2', 'K2', 'K1', 'O1', 'P1', 'Q1', 'Mf', 'Mm', 'Ssa']
DOOD = {'M2': 255.555, 'S2': 273.555, 'N2': 245.655, 'K2': 275.555, 'K1': 165.555, 'O1': 145.555, 'P1': 163.555, 'Q1': 135.655,
        'Mf': 75.555, 'Mm': 65.455, 'Ssa': 57.555}
BAND = {'M2': 2, 'S2': 2, 'N2': 2, 'K2': 2, 'K1': 1, 'O1': 1, 'P1': 1, 'Q1': 1, 'Mf': 0, 'Mm': 0, 'Ssa': 0}
BIAS = {0: 180., 1: 90., 2: 0.}
RHOW, RHOE = 1025.0, 5517.0
# degree 1 is 0 in the Gegout file. Displacement of the crust under degree-1 ocean load (the CE-frame values of Farrell 1972 /
# Blewitt 2003 as far as I know them: h'1 -0.29, l'1 0.11; NOT taken from a file you supplied - check them). With 0 / 0 the M2 radial
# amplitude at the station is 8.6 % above the BLQ, with these 3.7 %.
H1, L1 = -0.290, 0.113


def love(folder):
    h = np.zeros(LMAX + 1); l = np.zeros(LMAX + 1)
    for ln in open(os.path.join(folder, 'load_Love_numbers_from_Gegout_250.txt')):
        p = ln.replace('D', 'E').split()
        if p and int(p[0]) <= LMAX:
            h[int(p[0])], l[int(p[0])] = float(p[1]), float(p[2])
    h[1], l[1] = H1, L1
    return h, l


def coefs(folder):
    d = np.load(os.path.join(folder, 'data_wh.npz'))
    dd = np.round(d['doodson'], 3)
    C = {}
    for w in WAVES:
        s = np.abs(dd - DOOD[w]) < 1e-6
        n, m = d['l'][s], d['m'][s]
        a = {k: np.zeros((LMAX + 1, LMAX + 1)) for k in ('cp', 'sp', 'cm', 'sm')}
        a['cp'][n, m] = d['csin_plus'][s]; a['sp'][n, m] = d['ccos_plus'][s]
        a['cm'][n, m] = d['csin_minus'][s]; a['sm'][n, m] = d['ccos_minus'][s]
        C[w] = a
    return C


def plm(lat):
    """fully normalised Pbar_nm(sin lat) and dPbar_nm/dlat, shape (nlat, LMAX+1, LMAX+1)"""
    lat = np.asarray(lat, float); t = np.sin(lat); u = np.cos(lat); N = LMAX + 1
    P = np.zeros((len(lat), N + 1, N + 1)); P[:, 0, 0] = 1.0
    P[:, 1, 1] = np.sqrt(3.0) * u
    for m in range(2, N + 1):
        P[:, m, m] = np.sqrt((2 * m + 1) / (2.0 * m)) * u * P[:, m - 1, m - 1]
    for m in range(0, N):
        P[:, m + 1, m] = np.sqrt(2 * m + 3) * t * P[:, m, m]
    for m in range(0, N + 1):
        for n in range(m + 2, N + 1):
            a = np.sqrt((2 * n - 1) * (2 * n + 1) / ((n - m) * (n + m)))
            b = np.sqrt((2 * n + 1) * (n + m - 1) * (n - m - 1) / ((2 * n - 3) * (n - m) * (n + m)))
            P[:, n, m] = a * t * P[:, n - 1, m] - b * P[:, n - 2, m]
    dP = np.zeros((len(lat), LMAX + 1, LMAX + 1))
    for n in range(LMAX + 1):
        for m in range(n + 1):
            up = np.sqrt(((2 - (m == 0)) / 2.0) * (n - m) * (n + m + 1)) if m < n else 0.0
            dP[:, n, m] = up * P[:, n, m + 1] - m * (t / u) * P[:, n, m]
    return P[:, :LMAX + 1, :LMAX + 1], dP


def synth(a, w, lat, lon, h, l, Pc=None):
    """complex amplitudes (u = Re[Z e^{i theta}], metres) of up, east, north displacement on the grid lat x lon (rad)"""
    P, dP = Pc if Pc is not None else plm(lat)
    n = np.arange(LMAX + 1); m = n
    k = 3 * RHOW / RHOE * 0.01                              # cm of water -> m of displacement
    wu = np.where(n > 0, h / (2 * n + 1.0), 0.0) * k
    wh = np.where(n > 0, l / (2 * n + 1.0), 0.0) * k
    ph = np.exp(1j * np.deg2rad(BIAS[BAND[w]]))
    Ap = a['cp'] - 1j * a['sp']; Am = a['cm'] - 1j * a['sm']
    ep = np.exp(1j * np.outer(lon, m)); em = np.exp(-1j * np.outer(lon, m))
    f = lambda wt, Q: (np.einsum('n,lnm,nm->lm', wt, Q, Ap), np.einsum('n,lnm,nm->lm', wt, Q, Am))
    Up, Um = f(wu, P); Np_, Nm_ = f(wh, dP); Ep, Em = f(wh, P)
    Zu = ph * (Up @ ep.T + Um @ em.T)
    Zn = ph * (Np_ @ ep.T + Nm_ @ em.T)
    Ze = ph * ((1j * m * Ep) @ ep.T + (-1j * m * Em) @ em.T) / np.cos(lat)[:, None]
    return Zu, Ze, Zn


def blq_columns(Zu, Ze, Zn, w):
    """-> list of (Re, Im) arrays for U, W, S; value = A e^{i phi_lag}, phi_lag = bias - arg(Z)"""
    out = []
    for Z in (Zu, -Ze, -Zn):                                # up, west, south
        phi = np.deg2rad(BIAS[BAND[w]]) - np.angle(Z)
        A = np.abs(Z)
        out += [A * np.cos(phi), A * np.sin(phi)]
    return out


def grid(res):
    nla, nlo = int(round(180 / res)), int(round(360 / res))
    lat = 90 - res / 2 - res * np.arange(nla); lon = res / 2 + res * np.arange(nlo)
    return nla, nlo, lat, lon


def main(res=1.0, dst='otl_fes2014b_1.bin', folder='.'):
    h, l = love(folder); C = coefs(folder)
    nla, nlo, lat, lon = grid(res)
    Pc = plm(np.deg2rad(lat))
    cols = []
    for w in WAVES:
        Zu, Ze, Zn = synth(C[w], w, np.deg2rad(lat), np.deg2rad(lon), h, l, Pc)
        cols += blq_columns(Zu, Ze, Zn, w)
        print(w, 'max |U| %.2f mm' % (np.abs(Zu).max() * 1e3))
    step = 1e-5; table, planes = b'', []
    for c in cols:
        q = np.round(c / step).astype(np.int64)
        lo = float(q.min() * step); n = q - q.min()
        assert n.max() <= 65535, n.max()
        qq = (n - 32768).astype(np.int32)
        dq = np.diff(qq, axis=1, prepend=0).astype('<i2')   # int32 -> int16 wraps modulo 2**16
        table += struct.pack('<dd', lo, step); planes.append(dq.tobytes())
    raw = table + b''.join(planes)
    co = zlib.compressobj(9, zlib.DEFLATED, -15); z = co.compress(raw) + co.flush()
    out = b'OTLB' + struct.pack('<BBHHH', 1, len(cols), nla, nlo, 0) + struct.pack('<II', len(raw), zlib.crc32(raw)) + z
    open(dst, 'wb').write(out)
    print(dst, len(out), 'bytes', round(len(out) / 2**20, 3), 'MiB; raw', len(raw), '; grid', nla, 'x', nlo)


if __name__ == '__main__':
    a = sys.argv
    main(float(a[1]) if len(a) > 1 else 1.0, a[2] if len(a) > 2 else 'otl_fes2014b_1.bin', a[3] if len(a) > 3 else '.')
