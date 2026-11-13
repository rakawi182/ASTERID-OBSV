#!/usr/bin/env python3
"""Build gpt3_1.bin (global GPT3 1-degree grid, the coefficients ASTERID uses) from gpt3_1.npz.

Layout (little endian)
  0   'GP3B'
  4   u8 version (1), u8 ncol (37), u16 nlat (180), u16 nlon (360), u16 0
  12  u32 rawLen   bytes after inflating the payload
  16  u32 crc32    of the inflated payload
  20  payload      raw DEFLATE (RFC 1951) of:
        ncol x (f64 lo, f64 step)                    column table
        ncol x nlat*nlon int16                       column-major; each latitude row (89.5 ... -89.5) is
                                                      delta coded along longitude (0.5 ... 359.5), int16 wrap-around
  value = lo + (q + 32768) * step      (q = decoded int16)
Columns: undu, Hs, p[0..4], T[0..4], Q[0..4], dT[0..4], la[0..4], ah[0..4], aw[0..4]
Every column except Hs is stored losslessly at the decimal resolution of the .npz (all values are rounded there);
Hs (model orography, m) is rounded to 0.1 m. Units as in the .npz (p Pa, T K, Q kg/kg, dT K/m, ah/aw in 1e-3).
"""
import sys, struct, zlib
import numpy as np

COLS = [('undu', 0), ('Hs', 0)] + [(k, j) for k in ('p', 'T', 'Q', 'dT', 'la', 'ah', 'aw') for j in range(5)]
NLAT, NLON = 180, 360

def decimals(c, cap=8):
    for dec in range(cap + 1):
        if np.allclose(np.round(c, dec), c, atol=1e-12, rtol=0):
            return dec
    raise ValueError('column is not a rounded decimal')

def main(src, dst):
    d = np.load(src)
    lat, lon = d['lat'], d['lon']
    # grid order: latitude 89.5 ... -89.5 (rows), longitude 0.5 ... 359.5 (columns; the .npz prints it wrapped to +-180)
    ii, jj = np.divmod(np.arange(NLAT * NLON), NLON)
    assert lat.shape == (NLAT * NLON,) and np.allclose(lat, 89.5 - ii)
    assert np.allclose(((lon - (0.5 + jj) + 180) % 360) - 180, 0)
    table, planes = b'', []
    for k, j in COLS:
        c = d[k] if d[k].ndim == 1 else d[k][:, j]
        dec = 1 if k == 'Hs' else decimals(c)
        step = 10.0 ** -dec
        lo = float(np.round(c, dec).min())
        n = np.round((np.round(c, dec) - lo) / step).astype(np.int64)
        assert n.max() <= 65535, (k, j, n.max())
        q = (n - 32768).astype(np.int32).reshape(NLAT, NLON)
        dq = np.diff(q, axis=1, prepend=0).astype('<i2')   # int32 -> int16 wraps modulo 2**16
        table += struct.pack('<dd', lo, step)
        planes.append(dq.tobytes())
    raw = table + b''.join(planes)
    co = zlib.compressobj(9, zlib.DEFLATED, -15)
    z = co.compress(raw) + co.flush()
    out = b'GP3B' + struct.pack('<BBHHH', 1, len(COLS), NLAT, NLON, 0) + struct.pack('<II', len(raw), zlib.crc32(raw)) + z
    open(dst, 'wb').write(out)
    print(dst, len(out), 'bytes', round(len(out) / 2**20, 3), 'MiB; raw', len(raw))

if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else 'gpt3_1.npz', sys.argv[2] if len(sys.argv) > 2 else 'gpt3_1.bin')
