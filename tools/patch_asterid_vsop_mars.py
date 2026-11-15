#!/usr/bin/env python3
"""patch_asterid_vsop_mars.py -- registers vsop2013_mars.bin in ASTERID.html (already patched for Venus and Mercury), adds VS14 (int16 multiplier) support to the
reader, and extends vpAudit. Usage: python3 patch_asterid_vsop_mars.py ASTERID.html VSOP2013.ctl OUT.html IPS_TOL NOTE_FILE
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
k0 = [j for j in range(len(h)) if 'MARS' in L[h[j]]][0]
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
# reader: VS13 or VS14 (int16 multipliers)
b = rep(b, "if(u.length<8||String.fromCharCode(u[0],u[1],u[2],u[3])!=='VS13')throw new Error('not a vsop2013 .bin file');",
        "const mg=String.fromCharCode(u[0],u[1],u[2],u[3]);if(u.length<8||(mg!=='VS13'&&mg!=='VS14'))throw new Error('not a vsop2013 .bin file');const w16=mg==='VS14';")
b = rep(b, "if(j===13){a=dv.getUint16(o,true);o+=2}else a=dv.getInt8(o++);w+=", "if(j===13){a=dv.getUint16(o,true);o+=2}else if(w16){a=dv.getInt16(o,true);o+=2}else a=dv.getInt8(o++);w+=")
b = rep(b, 'AV=[0,1], // k = 0..6', 'AV=[0,1,2], // k = 0..6')
b = rep(b, "NMS=['Mercury','Venus'],", "NMS=['Mercury','Venus','Mars'],")
b = rep(b, 'CT={0:[[', 'CT={2:%s,0:[[' % CT2)
b = rep(b, "TM={0:'272 359',1:'289 646'}", "TM={0:'272 359',1:'289 646',2:'309 139'}")
b = rep(b, 'IT={0:[1.5e-7,', "IT={2:[%s,'%s'],0:[1.5e-7," % (ips_tol, note))
b = rep(b, 'the Sun, and Mercury and Venus when vsop2013_mercury.bin and vsop2013_venus.bin are loaded)',
        'the Sun, and Mercury, Venus and Mars when vsop2013_mercury.bin, vsop2013_venus.bin and vsop2013_mars.bin are loaded)')
b = rep(b, 'heliocentric Mercury and Venus, dynamical', 'heliocentric Mercury, Venus and Mars, dynamical')
b = rep(b, 'no truncation; Mercury and Venus from the full VSOP2013 series when vsop2013_mercury.bin and vsop2013_venus.bin are loaded)',
        'no truncation; Mercury, Venus and Mars from the full VSOP2013 series when vsop2013_mercury.bin, vsop2013_venus.bin and vsop2013_mars.bin are loaded)')
b = rep(b, '(Mercury and Venus: the full VSOP2013 series once vsop2013_mercury.bin and vsop2013_venus.bin are loaded)',
        '(Mercury, Venus and Mars: the full VSOP2013 series once vsop2013_mercury.bin, vsop2013_venus.bin and vsop2013_mars.bin are loaded)')
open(out, 'w', encoding='utf-8', newline='').write(b)
print('size', n0, '->', len(b.encode('utf-8')), 'free', 26214400 - len(b.encode('utf-8')))
