#!/usr/bin/env python3
"""patch_asterid_vsop_venus.py -- adds the VSOP2013 planet reader (Venus) to ASTERID.html.

Usage: python3 patch_asterid_vsop_venus.py ASTERID.html ASTERID_out.html vsop2013_reader.js

Every edit is an exact-string replacement that must match exactly once (otherwise the script stops), so it cannot
silently patch the wrong place. The reader module (vsop2013_reader.js) is inserted right after the IPS2000 block."""
import sys

src, dst, modf = sys.argv[1:4]
s = open(src, encoding='utf-8').read()
mod = open(modf, encoding='utf-8').read().rstrip('\n')

def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n:
        raise SystemExit('anchor found %d times (expected %d): %r' % (c, n, old[:90]))
    s = s.replace(old, new)

# 1. reader module after the IPS2000 block
rep("return{helio,equ,JD0:1903670.5,JD1:2633670.5}})();",
    "return{helio,equ,JD0:1903670.5,JD1:2633670.5}})();\n" + mod)

# 2. plCompute: heliocentric planet position from VSOP2013 when its file is loaded, else IPS2000
rep("function plCompute(Eo){const ea=Eo.ea",
    "const PHL=(k,t)=>VSP.equ(k,t)||IPS.equ(IPS.helio(k,t)); // VSOP2013 (ICRS, like the Earth model) if loaded, else IPS2000\nfunction plCompute(Eo){const ea=Eo.ea")
rep("for(let k=0;k<7;k++){let r=IPS.equ(IPS.helio(k,jt)),g=[", "for(let k=0;k<7;k++){VSP.want(k);let r=PHL(k,jt),g=[")
rep("r=IPS.equ(IPS.helio(k,jt-d/CAU));", "r=PHL(k,jt-d/CAU);")

# 3. PLANETS tab: caption, file picker, status line and refresh when a file becomes ready
rep("Apparent geocentric places (true equator and equinox of date) from the full IPS2000 series with light-time and aberration.",
    "Apparent geocentric places (true equator and equinox of date) from the full IPS2000 series (Venus: the full VSOP2013 series once vsop2013_venus.bin is loaded) with light-time and aberration.")
rep("if(f&&window.ASTERID_TOPO)window.ASTERID_TOPO[/opole/i.test(f.name)?'opPick':",
    "if(f&&/vsop/i.test(f.name))VSP.pick(f);else if(f&&window.ASTERID_TOPO)window.ASTERID_TOPO[/opole/i.test(f.name)?'opPick':")
rep("e.target.closest('#g3Btn,#opBtn,#otBtn,#apBtn')", "e.target.closest('#g3Btn,#opBtn,#otBtn,#apBtn,#vsBtn')")
rep("function render(){if(typeof HR_R==='undefined'",
    "let vsS='';const vsN=()=>{let h='';for(const k of VSP.AV){const q=VSP.ST[k],nm=PNAME[k],f='vsop2013_'+VSP.NM[k]+'.bin';\n"
    "  if(q.st==='ready')h+=`<div class=\"cap\" style=\"margin-bottom:8px\">${nm}: full VSOP2013 series (Simon et al. 2013; ${q.src}), heliocentric in the ICRS like the Earth model; planets without a loaded file use IPS2000.${q.err?' The last file chosen was rejected: '+String(q.err).replace(/</g,'&lt;')+'.':''}</div>`;\n"
    "  else if(q.st==='busy')h+=`<div class=\"cap\" style=\"margin-bottom:8px\">${nm}: loading ${f}; IPS2000 is used until it is ready.</div>`;\n"
    "  else if(q.st==='fail')h+=`<div class=\"cap\" style=\"margin-bottom:8px\">${nm}: ${f} could not be loaded: ${String(q.err).replace(/</g,'&lt;')}. It must sit next to this page, and cannot be fetched from file://; IPS2000 is used. <button id=\"vsBtn\" type=\"button\" style=\"font:inherit;color:var(--am);background:none;border:1px solid var(--am);padding:5px 10px;letter-spacing:.06em;cursor:pointer\">LOAD ${f}</button></div>`}\n"
    "  return h};\n"
    "function render(){if(typeof HR_R==='undefined'")
rep("if(!DATA||Math.abs(ms-tD)>5000||loc!==locD){DATA=plData(ms);tD=ms;locD=loc}",
    "{const vx=VSP.AV.map(k=>VSP.ST[k].st).join();if(vx!==vsS){vsS=vx;DATA=null;tPLT=-1e18}}\n if(!DATA||Math.abs(ms-tD)>5000||loc!==locD){DATA=plData(ms);tD=ms;locD=loc}")
rep("B.innerHTML=ban+ecp+DATA.res.map(", "B.innerHTML=ban+vsN()+ecp+DATA.res.map(")

# 4. LED row
rep("const E=T.EC||(window.__ECX&&window.__ECX.EC);let c='x',l='IDLE';",
    "{const V=window.ASTERID_VSOP;if(V)for(const k of V.AV){const O=V.ST[k],[c2,l2]=mp(O.st);o.push(['VSOP '+V.NM[k].slice(0,3).toUpperCase(),c2,l2+(O.src?' \\u00b7 '+O.src:'')+(O.err&&O.st==='fail'?' \\u00b7 '+O.err:'')])}}\n"
    "const E=T.EC||(window.__ECX&&window.__ECX.EC);let c='x',l='IDLE';")

# 5. Ephemeris Audit: extra rows (window.vpAudit) and cache key that follows the load state
rep(".concat(window.scAudit?window.scAudit():[])", ".concat(window.scAudit?window.scAudit():[]).concat(window.vpAudit?window.vpAudit():[])", 2)
rep("key=(E.msrc||'')+'|'+WATTS.mode;",
    "key=(E.msrc||'')+'|'+WATTS.mode+'|'+(window.ASTERID_VSOP?window.ASTERID_VSOP.ST.map(q=>q.st).join(''):'');")
rep("'Planets (HUD location)':'internal consistency",
    "'VSOP2013 planets':'VSOP2013.ctl (IMCCE, full series): heliocentric Venus, dynamical ecliptic and ICRS J2000, and the elliptic elements; IPS2000 (Chapront & Francou 2002, notice.txt epochs) as independent cross-check','Planets (HUD location)':'internal consistency")

# 6. descriptive texts
rep("All test vectors run live in this page: VSOP2013.ctl (IMCCE), IPS2000 notice.txt",
    "All test vectors run live in this page: VSOP2013.ctl (IMCCE; the Sun, and Venus when vsop2013_venus.bin is loaded), IPS2000 notice.txt")
rep("(VSOP2013, file VSOP2013p3, ftp.imcce.fr/pub/ephem/planets/vsop2013)",
    "(VSOP2013, files VSOP2013p3 for the Sun and VSOP2013p2 for Venus, ftp.imcce.fr/pub/ephem/planets/vsop2013)")
rep("source of the planet positions in the PLANETS tab and SKY VIEW)",
    "source of the planet positions in the PLANETS tab and SKY VIEW, except Venus when its VSOP2013 file is loaded)")
rep("PLANETS draws Mercury to Neptune from the full IPS2000 series (Chapront &amp; Francou 2002, 500–2498 CE, no truncation) with light-time",
    "PLANETS draws Mercury to Neptune from the full IPS2000 series (Chapront &amp; Francou 2002, 500–2498 CE, no truncation; Venus from the full VSOP2013 series when vsop2013_venus.bin is loaded) with light-time")

open(dst, 'w', encoding='utf-8', newline='').write(s)
print('written', dst, len(s.encode('utf-8')), 'bytes')
