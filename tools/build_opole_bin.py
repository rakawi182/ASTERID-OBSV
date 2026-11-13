#!/usr/bin/env python3
"""Build opole_0p5.bin (global ocean pole tide loading coefficients, 0.5 x 0.5 deg) from opoleloadcoefcmcor.npz.

Source: Desai (2002) ocean pole tide loading coefficients, CM frame (IERS Conventions 2010 sec. 7.1.5), array 'load_coef' (259200, 8):
  lon (0.25 ... 359.75), lat (-89.75 ... 89.75), then Re/Im of u_radial, u_north, u_east (dimensionless m/m after K, see below).
  Order: longitude varies fastest (720), latitude ascending (360 rows, south to north).

Layout (little endian), same idea as gpt3_1.bin
  0   'OPLB'
  4   u8 version (1), u8 ncol (6), u16 nlat (360), u16 nlon (720), u16 0
  12  u32 rawLen   bytes after inflating the payload
  16  u32 crc32    of the inflated payload
  20  payload      raw DEFLATE of:
        ncol x (f64 lo, f64 step)                    column table
        ncol x nlat*nlon int16                       column-major; each latitude row (-89.75 ... 89.75) delta coded along longitude
                                                      (0.25 ... 359.75), int16 wrap-around
  value = lo + (q + 32768) * step
Columns: urRe, urIm, unRe, unIm, ueRe, ueIm  (order of the source file).
Lossless at the 1e-5 resolution of the source file.
"""
import sys, struct, zlib
import numpy as np
COLS = ['urRe', 'urIm', 'unRe', 'unIm', 'ueRe', 'ueIm']
NLAT, NLON = 360, 720

def decimals(c, cap=8):
    for dec in range(cap + 1):
        if np.allclose(np.round(c, dec), c, atol=1e-12, rtol=0):
            return dec
    raise ValueError('column is not a rounded decimal')

def main(src, dst):
    a = np.load(src)['load_coef']  # noqa
    jj, ii = np.arange(NLAT * NLON) % NLON, np.arange(NLAT * NLON) // NLON
    assert a.shape == (NLAT * NLON, 8)
    assert np.allclose(a[:, 0], 0.25 + 0.5 * jj) and np.allclose(a[:, 1], -89.75 + 0.5 * ii)
    table, planes = b'', []
    for k, name in enumerate(COLS):
        c = a[:, 2 + k]
        dec = decimals(c); step = 10.0 ** -dec
        n = np.round(c / step).astype(np.int64).reshape(NLAT, NLON)
        d = np.diff(n, axis=1, prepend=n[:, :1])           # delta[:,0] = 0
        assert abs(d).max() < 32768, (name, abs(d).max())
        assert abs(n[:, 0]).max() < 2**31
        table += struct.pack('<d', step)
        planes.append(n[:, 0].astype('<i4').tobytes() + d.astype('<i2').tobytes())
        print(name, 'decimals', dec, 'max |delta|', int(abs(d).max()))
    raw = table + b''.join(planes)
    co = zlib.compressobj(9, zlib.DEFLATED, -15)
    z = co.compress(raw) + co.flush()
    out = b'OPLB' + struct.pack('<BBHHH', 1, len(COLS), NLAT, NLON, 0) + struct.pack('<II', len(raw), zlib.crc32(raw)) + z
    open(dst, 'wb').write(out)
    print(dst, len(out), 'bytes', round(len(out) / 2**20, 3), 'MiB; raw', len(raw))

if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else 'opoleloadcoefcmcor.npz', sys.argv[2] if len(sys.argv) > 2 else 'opole_0p5.bin')
