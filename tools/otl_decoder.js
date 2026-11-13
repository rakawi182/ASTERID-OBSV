/* Decoder for otl_fes2014b_1.bin (global FES2014b ocean tide loading grid), same style as opParse/opGrid.
   Needs __zi (inflate) and g3crc from ASTERID.html. otGrid(lat, lon) returns an object with the structure of OD.blq:
   {M2:[Aup, phiUp, Awest, phiWest, Asouth, phiSouth], ...}  amplitudes in m, BLQ phase lags in degrees, or null while the grid is not loaded. */
const OT={st:'idle',err:'',src:'',n:null,lo:null,step:null,NLA:0,NLO:0,NC:66,W:['M2','S2','N2','K2','K1','O1','P1','Q1','Mf','Mm','Ssa']};
function otParse(buf){const u=new Uint8Array(buf);if(u.length<20||String.fromCharCode(u[0],u[1],u[2],u[3])!=='OTLB')throw new Error('not an otl_fes2014b_1.bin file');
 const dv=new DataView(buf),nc=u[5],nla=dv.getUint16(6,true),nlo=dv.getUint16(8,true),rl=dv.getUint32(12,true),crc=dv.getUint32(16,true);
 if(u[4]!==1||nc!==66||nla*2<=0||nlo!==2*nla)throw new Error('unsupported otl_fes2014b_1.bin version');
 const raw=__zi(u.subarray(20),rl);if(g3crc(raw)!==crc)throw new Error('otl_fes2014b_1.bin checksum mismatch');
 const tb=new Float64Array(raw.buffer,raw.byteOffset,2*nc),n=new Int32Array(nc*nla*nlo),o0=raw.byteOffset+16*nc,lo=new Float64Array(nc),step=new Float64Array(nc);
 for(let c=0;c<nc;c++){lo[c]=tb[2*c];step[c]=tb[2*c+1];const d=new Int16Array(raw.buffer,o0+c*nla*nlo*2,nla*nlo);
  for(let r=0;r<nla;r++){let s=0;const k=c*nla*nlo+r*nlo;for(let j=0;j<nlo;j++){s=(s+d[r*nlo+j])<<16>>16;n[k+j]=s}}}
 OT.NLA=nla;OT.NLO=nlo;OT.n=n;OT.lo=lo;OT.step=step}
async function otLoad(){if(OT.n||OT.st==='busy')return;OT.st='busy';OT.err='';
 try{let buf;if(typeof window.__OTL_B64==='string'){const a=atob(window.__OTL_B64),b=new Uint8Array(a.length);for(let i=0;i<a.length;i++)b[i]=a.charCodeAt(i);buf=b.buffer;OT.src='embedded'}
  else{const r=await fetch('otl_fes2014b_1.bin');if(!r.ok)throw new Error('otl_fes2014b_1.bin: HTTP '+r.status);buf=await r.arrayBuffer();OT.src='otl_fes2014b_1.bin'}
  otParse(buf);OT.st='ready'}catch(e){OT.st='fail';OT.err=String(e&&e.message||e)}}
function otPick(file){OT.st='busy';return file.arrayBuffer().then(b=>{otParse(b);OT.st='ready';OT.err='';OT.src=file.name}).catch(e=>{OT.st='fail';OT.err=String(e&&e.message||e)})}
/* bilinear interpolation of the real and imaginary parts (A cos phi, A sin phi); longitude wraps, latitude is clamped to the outer cell centres */
function otGrid(lat,lon){if(!OT.n)return null;const NLA=OT.NLA,NLO=OT.NLO,N=NLA*NLO,res=180/NLA,y=Math.min(NLA-1,Math.max(0,(90-res/2-lat)/res)),i0=Math.min(NLA-2,Math.floor(y)),ty=y-i0,
 x=(((lon-res/2)/res)%NLO+NLO)%NLO,j0=Math.floor(x)%NLO,j1=(j0+1)%NLO,tx=x-Math.floor(x),
 ip=c=>{const o=c*N,a=OT.n[o+i0*NLO+j0],b=OT.n[o+i0*NLO+j1],d=OT.n[o+(i0+1)*NLO+j0],e=OT.n[o+(i0+1)*NLO+j1];return OT.lo[c]+((1-tx)*(1-ty)*a+tx*(1-ty)*b+(1-tx)*ty*d+tx*ty*e+32768)*OT.step[c]},out={};
 OT.W.forEach((w,k)=>{const r=[];for(let q=0;q<3;q++){const re=ip(6*k+2*q),im=ip(6*k+2*q+1);r.push(Math.hypot(re,im),Math.atan2(im,re)*180/Math.PI)}out[w]=r});return out}
