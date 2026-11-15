#!/usr/bin/env python3
"""patch_asterid_vsop_mercury.py -- registers vsop2013_mercury.bin in ASTERID.html (already patched for Venus) and generalises vpAudit.
Usage: python3 patch_asterid_vsop_mercury.py ASTERID.html VSOP2013.ctl OUT.html IPS_TOL
Every replacement must match exactly once (checked)."""
import sys, re, json
src, ctl, out, ips_tol = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
b = open(src, encoding='utf-8', newline='').read()
n0 = len(b.encode('utf-8'))

def rep(s, old, new, cnt=1):
    c = s.count(old)
    if c != cnt:
        raise SystemExit('anchor count %d != %d for: %s' % (c, cnt, old[:80]))
    return s.replace(old, new)

# ---- Mercury rows of VSOP2013.ctl: JD, a l k h q p, X Y Z (ecliptic), X Y Z (ICRS)  (same row layout as the Venus table)
L = [l.rstrip('\r') for l in open(ctl, encoding='ascii', errors='replace').read().split('\n')]
h = [j for j, l in enumerate(L) if 'PLANETARY EPHEMERIS' in l]
assert 'MERCURY' in L[h[0]]
L = L[h[0]:h[1]] if len(h) > 1 else L[h[0]:]  # the .ctl holds all nine planets; Mercury is the first block
rows, i = [], 0
while i < len(L):
    m = re.match(r'\s*Julian Date JD\s+([0-9.]+)', L[i])
    if m:
        v = [[float(x) for x in L[i + j].split()] for j in (1, 2, 3)]
        assert all(len(x) == 6 for x in v)
        rows.append([float(m.group(1))] + v[0] + v[1][:3] + v[2][:3]); i += 4
    else:
        i += 1
assert len(rows) == 11
def fmt(x):
    s = repr(x)
    return s
CT0 = '[' + ','.join('[' + ','.join(fmt(x) for x in r) + ']' for r in rows) + ']'

# ---- old vpAudit: keep the Venus table verbatim
a = b.index('window.vpAudit=function(){')
e = b.index("(function(){'use strict';\nif(typeof SM==='undefined'||!window.__SKY", a)
old = b[a:e]
ci = old.index('CT=[[') + 3
cj = old.index(']];\n let me=0') + 2
CT1 = old[ci:cj]

new = r'''window.vpAudit=function(){const G='VSOP2013 planets',A=[],NMS=['Mercury','Venus'],
 add=(n,res,tol,u,note)=>A.push({g:G,n,res,tol,u,ok:Math.abs(res)<=tol,note}),
 CT={0:%s,1:%s},TM={0:'272 359',1:'289 646'},
 IT={0:[%s,'tolerance = 0.064\u2033 (largest declared IPS2000 vs DE406 difference on heliocentric longitude of any planet; no Mercury-specific value is documented here) at the aphelion distance 0.467 au = 1.5e-7 au; VSOP2013 vs INPOP10a (0.06 mas, 1890\u20132000) is negligible; observed 9.0e-8 au (about 0.048\u2033 at a = 0.387 au)'],1:[2e-7,'tolerance = quadrature of declared errors (IPS2000 vs DE406 and VSOP2013 vs INPOP10a, both \u2264 0.03\u2033 on the longitude of Venus); the two theories are fitted to different ephemerides']};
 for(const k of VSP.AV){const nm=NMS[k]||('Planet '+k),ct=CT[k],fn='vsop2013_'+VSP.NM[k]+'.bin';
  if(!ct||!VSP.ready(k)){A.push({g:G,n:nm+' vs VSOP2013.ctl and IPS2000',info:fn+' not loaded: checks skipped',ok:true});continue}
  let me=0,mq=0,mel=0;
  for(const r of ct){const o=VSP.ecl(k,r[0]),q=VSP.equ(k,r[0]),el=VSP.elems(k,r[0]);
   for(let i=0;i<3;i++){me=Math.max(me,Math.abs(o[i]-r[7+i]));mq=Math.max(mq,Math.abs(q[i]-r[10+i]))}
   for(let i=0;i<6;i++){let d=Math.abs(el[i]-r[1+i]);if(i===1)d=Math.min(d,2*Math.PI-d);mel=Math.max(mel,d)}}
  add(nm+' X,Y,Z (dynamical ecliptic J2000) vs VSOP2013.ctl, 11 epochs 1890\u20132000, max |\u0394|',me,1e-10,'au','ctl = full series, printed to 10 decimals (rounding 5e-11); series read from '+fn+' ('+TM[k]+' terms + mean motion of l)');
  add(nm+' X,Y,Z in ICRS (README rotation \u03b5, \u03c6) vs VSOP2013.ctl, max |\u0394|',mq,1e-10,'au');
  add(nm+' elliptic elements a, l, k, h, q, p vs VSOP2013.ctl, max |\u0394| (l modulo 2\u03c0)',mel,1e-10,'','a in au, l in rad, k, h, q, p dimensionless; mean longitude includes the mean-motion term that VSOP2013.f adds to the l series');
  let mc=0;for(let i=0;i<11;i++){const jd=1903670.5+73000*i,o=VSP.ecl(k,jd),p=IPS.helio(k,jd);mc=Math.max(mc,Math.hypot(o[0]-p[0],o[1]-p[1],o[2]-p[2]))}
  add(nm+' VSOP2013 vs IPS2000 (independent theory), 11 epochs 500\u20132498, max 3-D |\u0394|',mc,IT[k][0],'au',IT[k][1])}
 return A};
''' % (CT0, CT1, ips_tol)
b = b[:a] + new + b[e:]

b = rep(b, 'AV=[1], // k = 0..6', 'AV=[0,1], // k = 0..6')
b = rep(b, 'VSOP2013.ctl (IMCCE; the Sun, and Venus when vsop2013_venus.bin is loaded)',
        'VSOP2013.ctl (IMCCE; the Sun, and Mercury and Venus when vsop2013_mercury.bin and vsop2013_venus.bin are loaded)')
b = rep(b, 'heliocentric Venus, dynamical ecliptic and ICRS J2000', 'heliocentric Mercury and Venus, dynamical ecliptic and ICRS J2000')
b = rep(b, 'no truncation; Venus from the full VSOP2013 series when vsop2013_venus.bin is loaded)',
        'no truncation; Mercury and Venus from the full VSOP2013 series when vsop2013_mercury.bin and vsop2013_venus.bin are loaded)')
b = rep(b, '(Venus: the full VSOP2013 series once vsop2013_venus.bin is loaded)',
        '(Mercury and Venus: the full VSOP2013 series once vsop2013_mercury.bin and vsop2013_venus.bin are loaded)')
open(out, 'w', encoding='utf-8', newline='').write(b)
print('size', n0, '->', len(b.encode('utf-8')), 'limit 26214400, free', 26214400 - len(b.encode('utf-8')))
