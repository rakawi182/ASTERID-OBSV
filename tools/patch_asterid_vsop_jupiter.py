#!/usr/bin/env python3
"""patch_asterid_vsop_jupiter.py -- registers vsop2013_jupiter.bin in ASTERID.html (already patched for Mercury, Venus and Mars; the reader already
handles VS13 and VS14) and extends vpAudit. Usage: python3 patch_asterid_vsop_mars.py ASTERID.html VSOP2013.ctl OUT.html IPS_TOL NOTE_FILE
Every replacement must match exactly once (checked)."""
import sys, re
src, ctl, out, ips_tol, notef = sys.argv[1:6]
b = open(src, encoding='utf-8', newline='').read()
n0 = len(b.encode('utf-8'))
note = open(notef, encoding='utf-8').read().strip()
def rep(s, old, new):
    c = s.count(old)
    if c != 1: raise SystemExit('anchor count %d != 1 for: %s' % (c, old[:80]))
    return s.replace(old, new)
L = [l.rstrip('\r') for l in open(ctl, encoding='ascii', errors='replace').read().split('\n')]
h = [j for j, l in enumerate(L) if 'PLANETARY EPHEMERIS' in l]
k0 = [j for j in range(len(h)) if 'JUPITER' in L[h[j]]][0]
L = L[h[k0]:h[k0 + 1]]
rows, i = [], 0
while i < len(L):
    m = re.match(r'\s*Julian Date JD\s+([0-9.]+)', L[i])
    if m:
        v = [[float(x) for x in L[i + j].split()] for j in (1, 2, 3)]
        assert all(len(x) == 6 for x in v)
        rows.append([float(m.group(1))] + v[0] + v[1][:3] + v[2][:3]); i += 4
    else: i += 1
assert len(rows) == 11
CT2 = '[' + ','.join('[' + ','.join(repr(x) for x in r) + ']' for r in rows) + ']'
b = rep(b, 'AV=[0,1,2], // k = 0..6', 'AV=[0,1,2,3], // k = 0..6')
b = rep(b, "NMS=['Mercury','Venus','Mars'],", "NMS=['Mercury','Venus','Mars','Jupiter'],")
b = rep(b, 'CT={2:[[', 'CT={3:%s,2:[[' % CT2)
b = rep(b, "TM={0:'272 359',1:'289 646',2:'309 139'}", "TM={0:'272 359',1:'289 646',2:'309 139',3:'324 607'}")
b = rep(b, 'IT={2:[', "IT={3:[%s,'%s'],2:[" % (ips_tol, note))
for o, n in [
 ('the Sun, and Mercury, Venus and Mars when vsop2013_mercury.bin, vsop2013_venus.bin and vsop2013_mars.bin are loaded)',
  'the Sun, and Mercury, Venus, Mars and Jupiter when vsop2013_mercury.bin, vsop2013_venus.bin, vsop2013_mars.bin and vsop2013_jupiter.bin are loaded)'),
 ('heliocentric Mercury, Venus and Mars, dynamical', 'heliocentric Mercury, Venus, Mars and Jupiter, dynamical'),
 ('no truncation; Mercury, Venus and Mars from the full VSOP2013 series when vsop2013_mercury.bin, vsop2013_venus.bin and vsop2013_mars.bin are loaded)',
  'no truncation; Mercury, Venus, Mars and Jupiter from the full VSOP2013 series when vsop2013_mercury.bin, vsop2013_venus.bin, vsop2013_mars.bin and vsop2013_jupiter.bin are loaded)'),
 ('(Mercury, Venus and Mars: the full VSOP2013 series once vsop2013_mercury.bin, vsop2013_venus.bin and vsop2013_mars.bin are loaded)',
  '(Mercury, Venus, Mars and Jupiter: the full VSOP2013 series once vsop2013_mercury.bin, vsop2013_venus.bin, vsop2013_mars.bin and vsop2013_jupiter.bin are loaded)')]:
    b = rep(b, o, n)
open(out, 'w', encoding='utf-8', newline='').write(b)
print('size', n0, '->', len(b.encode('utf-8')), 'free', 26214400 - len(b.encode('utf-8')))
