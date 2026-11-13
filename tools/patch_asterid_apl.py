#!/usr/bin/env python3
"""patch_asterid_apl.py - one-off patch that adds the global APL grid (apl_rp_1.bin) to ASTERID.html (outside the station)."""
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(old, new, n=1):
    global s
    c = s.count(old)
    assert c == n, (c, old[:80])
    s = s.replace(old, new)

# 1. aplRad takes an optional coefficient set (default: the station constants)
rep("function aplRad(mjd){", "function aplRad(mjd,A){A=A||OD.apls;")
rep("for(const k in OD.apls){const c=OD.apls[k],ds=", "for(const k in A){const c=A[k],ds=")

# 2. loader and bilinear interpolation of the global grid
AP = r"""/* ---- global atmospheric pressure loading grid: apl_rp_1.bin (1 deg x 1 deg cell centres, north first, 64 800 cells; lossless-to-1e-8 m int16 delta + int32 row base + deflate; tools/build_apl_bin.py).
   Ray & Ponte (2003) atmospheric tide (P1, S1, K1, T2, S2, R2; pressure harmonics to degree 10, S1 to 20) loaded with the Gegout load Love numbers h'n: radial displacement C, S per wave (u = C cos(chi) - S sin(chi), chi the Doodson argument of aplRad).
   Used away from the TOPOCENTRIC station (where the embedded constants stay the reference). Same loading as opole_0p5.bin: fetch (not from file://), file picker, or embedded in the single-file release (window.__APL_B64). ---- */
const AP={st:'idle',err:'',src:'',n:null,step:null,NLA:180,NLO:360,W:['P1','S1','K1','T2','S2','R2']};
function apParse(buf){const u=new Uint8Array(buf);if(u.length<20||String.fromCharCode(u[0],u[1],u[2],u[3])!=='APLB')throw new Error('not an apl_rp_1.bin file');
 const dv=new DataView(buf),nc=u[5],nla=dv.getUint16(6,true),nlo=dv.getUint16(8,true),rl=dv.getUint32(12,true),crc=dv.getUint32(16,true);
 if(u[4]!==1||nc!==12||nla!==180||nlo!==360)throw new Error('unsupported apl_rp_1.bin version');
 const raw=__zi(u.subarray(20),rl);if(g3crc(raw)!==crc)throw new Error('apl_rp_1.bin checksum mismatch');
 const step=new Float64Array(raw.buffer,0,nc),n=new Int32Array(nc*nla*nlo),blk=nla*4+nla*nlo*2;
 for(let c=0;c<nc;c++){const o=8*nc+c*blk,base=new Int32Array(raw.buffer,o,nla),d=new Int16Array(raw.buffer,o+nla*4,nla*nlo);
  for(let r=0;r<nla;r++){let s=base[r];const k=c*nla*nlo+r*nlo;n[k]=s;for(let j=1;j<nlo;j++){s+=d[r*nlo+j];n[k+j]=s}}}
 AP.step=step;AP.n=n}
async function apLoad(){if(AP.n||AP.st==='busy')return;AP.st='busy';AP.err='';
 try{let buf;if(typeof window.__APL_B64==='string'){const a=atob(window.__APL_B64),b=new Uint8Array(a.length);for(let i=0;i<a.length;i++)b[i]=a.charCodeAt(i);buf=b.buffer;AP.src='embedded'}
  else{const r=await fetch('apl_rp_1.bin');if(!r.ok)throw new Error('apl_rp_1.bin: HTTP '+r.status);buf=await r.arrayBuffer();AP.src='apl_rp_1.bin'}
  apParse(buf);AP.st='ready'}catch(e){AP.st='fail';AP.err=String(e&&e.message||e)}}
function apPick(file){AP.st='busy';return file.arrayBuffer().then(b=>{apParse(b);AP.st='ready';AP.err='';AP.src=file.name}).catch(e=>{AP.st='fail';AP.err=String(e&&e.message||e)})}
/* bilinear interpolation of C and S of the six waves at (lat, lon); longitude wraps, latitude is clamped to the outer cell centres (+-89.5).
   Returns {P1:{d,C,S},...} in m, the same shape as OD.apls (so aplRad(mjd,apGrid(lat,lon)) is the displacement at the site), or null while the grid is not loaded */
function apGrid(lat,lon){if(!AP.n)return null;const NLA=AP.NLA,NLO=AP.NLO,N=NLA*NLO,y=Math.min(NLA-1,Math.max(0,89.5-lat)),i0=Math.min(NLA-2,Math.floor(y)),ty=y-i0,x=(((lon-.5)%NLO)+NLO)%NLO,j0=Math.floor(x)%NLO,j1=(j0+1)%NLO,tx=x-Math.floor(x),
 ip=c=>{const o=c*N,a=AP.n[o+i0*NLO+j0],b=AP.n[o+i0*NLO+j1],d=AP.n[o+(i0+1)*NLO+j0],e=AP.n[o+(i0+1)*NLO+j1];return((1-tx)*(1-ty)*a+tx*(1-ty)*b+(1-tx)*ty*d+tx*ty*e)*AP.step[c]},out={};
 AP.W.forEach((k,q)=>{out[k]={d:OD.apls[k].d,C:ip(2*q),S:ip(2*q+1)}});return out}
"""
rep("/* ---- frames ---- */", AP + "/* ---- frames ---- */")

# 3. compute(): APL at a free site from the grid
rep("otb=stn?null:otGrid(lat,lon),", "otb=stn?null:otGrid(lat,lon),apb=stn?null:apGrid(lat,lon),")
rep("al=enu2xyz(0,0,stn?aplRad(U[0]+U[1]/86400):0,lat,lon),", "al=enu2xyz(0,0,stn?aplRad(U[0]+U[1]/86400):(apb?aplRad(U[0]+U[1]/86400,apb):0),lat,lon),")

# 4. export
rep("otGrid,otLoad,otPick,OT,meanPole", "otGrid,otLoad,otPick,OT,apGrid,apLoad,apPick,AP,meanPole")

# 5. PLANETS tab: load on demand, picker, button, banner
rep("if(!atSt&&TP.OT.st==='idle')TP.otLoad();", "if(!atSt&&TP.OT.st==='idle')TP.otLoad();if(!atSt&&TP.AP.st==='idle')TP.apLoad();")
rep("/opole/i.test(f.name)?'opPick':/otl/i.test(f.name)?'otPick':'g3Pick'", "/opole/i.test(f.name)?'opPick':/otl/i.test(f.name)?'otPick':/apl/i.test(f.name)?'apPick':'g3Pick'")
rep("'#g3Btn,#opBtn,#otBtn'", "'#g3Btn,#opBtn,#otBtn,#apBtn'")
rep("opr=TP.OP,otr=TP.OT,", "opr=TP.OP,otr=TP.OT,apr=TP.AP,")
BTN = '<button id="apBtn" type="button" style="font:inherit;color:var(--am);background:none;border:1px solid var(--am);padding:5px 10px;letter-spacing:.06em;cursor:pointer">LOAD apl_rp_1.bin</button>'
APN = ("apNote=atSt?'':apr.st==='ready'?` Atmospheric pressure loading (S1/S2 family, radial) is applied from the global Ray and Ponte (2003) grid (${apr.src}, pressure harmonics to degree 10 (S1 to 20) with load Love numbers, bilinear at this location, 1° cells); the grid is band-limited, so it differs somewhat from the station constants (up to about 0.1 mm radial at the station).`"
       ":` Atmospheric pressure loading is not applied: ${apr.st==='busy'?'loading apl_rp_1.bin':apr.st==='fail'?'apl_rp_1.bin could not be loaded: '+String(apr.err).replace(/</g,'&lt;')+'. It must sit next to this page, and cannot be fetched from file://':'apl_rp_1.bin not requested yet'}.`"
       "+(apr.st==='fail'?` " + BTN + "`:''),\n  ban=atSt?''")
rep("\n  ban=atSt?''", "\n  " + APN, 1)   # inserted before ban=
rep("opNote+otNote+", "opNote+otNote+apNote+", 2)
rep("Not applied, because those data exist only at the station: atmospheric pressure loading and non-tidal loading (ESMGFZ).", "Not applied, because those data exist only at the station: non-tidal loading (ESMGFZ).")
rep("atmospheric pressure loading, non-tidal loading (ESMGFZ), deflection of the vertical (the DEM", "non-tidal loading (ESMGFZ), deflection of the vertical (the DEM")

# 6. texts
rep("Ocean tide loading, atmospheric pressure loading and ESMGFZ non-tidal loading exist only for the station (the ocean pole tide loading is global:",
    "Ocean tide loading and ESMGFZ non-tidal loading exist only for the station (the atmospheric pressure loading of the S1/S2 family is global: apl_rp_1.bin, Ray and Ponte 2003, 1°, applied at other locations once loaded; the ocean pole tide loading is global:")
rep("the station-only data (atmospheric pressure loading, ESMGFZ) are left out;",
    "the station-only data (ESMGFZ) are left out; atmospheric pressure loading (S1/S2 family, radial) comes from the global Ray and Ponte grid apl_rp_1.bin (apGrid, then the same aplRad) once it is loaded, else it is left out;")
rep("with the ocean pole tide loading from the global Desai (2002) grid (opole_0p5.bin, loaded on demand)",
    "with the atmospheric pressure loading from the global Ray and Ponte (2003) grid (apl_rp_1.bin, loaded on demand), with the ocean pole tide loading from the global Desai (2002) grid (opole_0p5.bin, loaded on demand)")
open(dst, 'w', encoding='utf-8').write(s)
print('patched', len(s))
