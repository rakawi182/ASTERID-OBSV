#!/usr/bin/env python3
"""
build_vsop2013_bin.py -- VSOP2013pN.dat (IMCCE, Simon et al. 2013, A&A 557, A49) -> vsop2013_<planet>.bin for ASTERID

Usage:   python3 build_vsop2013_bin.py VSOP2013p2.dat [out.bin]
         (planet index 1..9 is read from the file header; default out = vsop2013_<planet>.bin)

Binary layout (little endian), the same body layout as the Earth-Moon barycentre series embedded in ASTERID.html:
  "VS13" or "VS14"          4 bytes  magic (VS14: the multipliers j = 0..12, 15, 16 are int16 instead of int8; chosen automatically when needed)
  u8   planet index         1 = Mercury ... 9 = Pluto
  u8   ns                   number of series (variable iv 1..6 x time power it)
  u16  nd                   number of distinct arguments (17 integer multipliers)
  ns x { u8 iv, u8 it, u32 nt, u32 nb }      series table; nb = terms stored in float64
  nd x { 17 multipliers: int8 (VS14: int16) for j = 0..12, 15, 16 and uint16 for j = 13 (argument mu) }
  per series, per term (sorted by decreasing |S|+|C|):
        u16 index into the argument table, then S, C as float64 (first nb terms, |S|+|C| >= 1e-5)
        or float32 (remaining terms)
The first term of the l series with it = 1 (constant frequency, all multipliers 0) is NOT stored, as in VSOP2013.f:
the reader must add freqpla * T to l (Mercury ... Neptune: 26087.90314068555, 10213.28554743445, 6283.075850353215,
3340.612434145457, 529.6909615623250, 213.2990861084880, 74.78165903077800, 38.13297222612500 rad per thousand years;
Pluto: 0.3595362285049309), then reduce l modulo 2 pi.
Term = T^it (S sin F + C cos F), F = sum a(i) ll(i), T in thousands of Julian years TDB from J2000.
"""
import struct, sys, re, os

NAMES = ['MERCURY', 'VENUS', 'EMB', 'MARS', 'JUPITER', 'SATURN', 'URANUS', 'NEPTUNE', 'PLUTO']
BIG = 1e-5


def parse(path):
    series = []
    cur = None
    with open(path, 'r', encoding='ascii', errors='replace') as f:
        for ln in f:
            ln = ln.rstrip('\r\n')
            if not ln.strip():
                continue
            if ln.lstrip().startswith('VSOP2013'):
                ip, iv, it, nt = int(ln[9:12]), int(ln[12:15]), int(ln[15:18]), int(ln[18:25])
                cur = dict(ip=ip, iv=iv, it=it, nt=nt, terms=[])
                series.append(cur)
                continue
            # fixed columns, Fortran format (i5,1x,4i3,1x,5i3,1x,4i4,1x,i6,1x,3i3,2(f20.16,1x,i3))
            num = int(ln[0:5])
            a = [int(ln[6 + 3 * i:9 + 3 * i]) for i in range(4)]
            a += [int(ln[19 + 3 * i:22 + 3 * i]) for i in range(5)]
            a += [int(ln[35 + 4 * i:39 + 4 * i]) for i in range(4)]
            a += [int(ln[52:58])]
            a += [int(ln[59 + 3 * i:62 + 3 * i]) for i in range(3)]
            s = float(ln[68:88]) * 10.0 ** int(ln[89:92])
            c = float(ln[92:112]) * 10.0 ** int(ln[113:116])
            # cross-check against whitespace tokens
            tk = ln.split()
            if len(tk) == 17 + 1 + 4 and [int(x) for x in tk[1:18]] != a:
                raise SystemExit('column parse mismatch at term %d' % num)
            if cur['iv'] == 2 and cur['it'] == 1 and num == 1:
                # secular mean-motion term of the l series: VSOP2013.f drops it and adds freqpla * T instead
                if any(a):
                    raise SystemExit('unexpected first term of the l series')
                cur['nt'] -= 1
                continue
            cur['terms'].append((tuple(a), s, c))
    return series


def main():
    if len(sys.argv) < 2:
        raise SystemExit(__doc__)
    src = sys.argv[1]
    series = parse(src)
    ip = series[0]['ip']
    for s in series:
        if s['ip'] != ip or len(s['terms']) != s['nt']:
            raise SystemExit('header/term count mismatch in series iv=%d it=%d' % (s['iv'], s['it']))
    out = sys.argv[2] if len(sys.argv) > 2 else 'vsop2013_%s.bin' % NAMES[ip - 1].lower()
    dic, order = {}, []
    for s in series:
        s['terms'].sort(key=lambda t: -(abs(t[1]) + abs(t[2])))  # stable: ties keep file order
        for a, _, _ in s['terms']:
            if a not in dic:
                dic[a] = len(order)
                order.append(a)
    if len(order) > 65535:
        raise SystemExit('too many distinct arguments')
    wide = any(not -128 <= v <= 127 for a in order for j, v in enumerate(a) if j != 13)
    b = bytearray(b'VS14' if wide else b'VS13')  # VS14 = same layout, multipliers (except j = 13) int16: needed when one exceeds int8 (Mars: Jupiter multiplier up to +-144)
    b += struct.pack('<BBH', ip, len(series), len(order))
    for s in series:
        nb = sum(1 for _, x, y in s['terms'] if abs(x) + abs(y) >= BIG)
        s['nb'] = nb
        b += struct.pack('<BBII', s['iv'], s['it'], s['nt'], nb)
    for a in order:
        for j, v in enumerate(a):
            if j == 13:
                b += struct.pack('<H', v)
            else:
                b += struct.pack('<h' if wide else '<b', v)
    for s in series:
        for n, (a, x, y) in enumerate(s['terms']):
            b += struct.pack('<H', dic[a])
            b += struct.pack('<dd' if n < s['nb'] else '<ff', x, y)
    open(out, 'wb').write(b)
    nt = sum(s['nt'] for s in series)
    print('%s: planet %d (%s), %d series, %d terms, %d distinct arguments -> %s (%.3f MiB)' %
          (src, ip, NAMES[ip - 1], len(series), nt, len(order), out, len(b) / 1048576))


if __name__ == '__main__':
    main()
