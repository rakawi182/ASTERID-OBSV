/* ===== VSOP2013 planets (Simon, Francou, Fienga & Manche 2013, A&A 557, A49): one file per planet, vsop2013_<planet>.bin (tools/build_vsop2013_bin.py from the IMCCE files VSOP2013pN.dat), loaded on demand; planets without a loaded file keep the IPS2000 series. Full series, no truncation. Venus: 289 647 terms in VSOP2013p2.dat (289 646 stored: the mean-motion term of l is added from freqpla, as in VSOP2013.f), 41 158 distinct arguments; terms are stored as a deduplicated argument dictionary + float64 (|S|+|C|>=1e-5) / float32 coefficients. ===== */
const VSP=(()=>{const NM=['mercury','venus','mars','jupiter','saturn','uranus','neptune'],IP=[1,2,4,5,6,7,8],AV=[0,1,2], // k = 0..6 (Mercury..Neptune) -> VSOP2013 planet index; AV = planets that have a published .bin
 CI0=[4.402608631669,3.176134461576,1.753470369433,6.203500014141,4.091360003050,1.713740719173,5.598641292287,2.805136360408,2.326989734620,.599546107035,.874018510107,5.481225395663,5.311897933164,0,5.198466400630,1.627905136020,2.355555638750],
 CI1=[26087.90314068555,10213.28554743445,6283.075850353215,3340.612434145457,1731.170452721855,1704.450855027201,1428.948917844273,1364.756513629990,1361.923207632842,529.6909615623250,213.2990861084880,74.78165903077800,38.13297222612500,.3595362285049309,77713.7714481804,84334.6615717837,83286.9142477147],
 FQ=[26087.90314068555,10213.28554743445,6283.075850353215,3340.612434145457,529.6909615623250,213.2990861084880,74.78165903077800,38.13297222612500,.3595362285049309], // mean motion of l (VSOP2013.f: freqpla), rad per millennium; the l series carries no secular term
 AM=(()=>{const e=(23+26/60+21.41136/3600)*Math.PI/180,f=-.05188*Math.PI/648000,ce=Math.cos(e),se=Math.sin(e),cf=Math.cos(f),sf=Math.sin(f);return[[cf,-sf*ce,sf*se],[sf,cf*ce,-cf*se],[0,se,ce]]})(), // dynamical ecliptic J2000 -> ICRS (VSOP2013 README)
 ST=NM.map(()=>({st:'idle',err:'',src:'',d:null}));
 function parse(buf){const u=new Uint8Array(buf);const mg=String.fromCharCode(u[0],u[1],u[2],u[3]);if(u.length<8||(mg!=='VS13'&&mg!=='VS14'))throw new Error('not a vsop2013 .bin file');const w16=mg==='VS14';
  const dv=new DataView(buf),ip=u[4],ns=u[5],nd=dv.getUint16(6,true),k=IP.indexOf(ip);if(k<0)throw new Error('planet index '+ip+' is not used here');
  let o=8;const sr=[];let N=0;for(let i=0;i<ns;i++){const s={iv:u[o],it:u[o+1],nt:dv.getUint32(o+2,true),nb:dv.getUint32(o+6,true)};o+=10;s.o=N;N+=s.nt;sr.push(s)}
  const dw=new Float64Array(nd),dp=new Float64Array(nd);
  for(let d=0;d<nd;d++){let w=0,f=0;for(let j=0;j<17;j++){let a;if(j===13){a=dv.getUint16(o,true);o+=2}else if(w16){a=dv.getInt16(o,true);o+=2}else a=dv.getInt8(o++);w+=a*CI1[j];f+=a*CI0[j]}dw[d]=w;dp[d]=f}
  const D=new Uint16Array(N),S=new Float64Array(N),C=new Float64Array(N);let q=0;
  for(const s of sr)for(let n=0;n<s.nt;n++,q++){D[q]=dv.getUint16(o,true);if(n<s.nb){S[q]=dv.getFloat64(o+2,true);C[q]=dv.getFloat64(o+10,true);o+=18}else{S[q]=dv.getFloat32(o+2,true);C[q]=dv.getFloat32(o+6,true);o+=10}}
  if(o!==u.length)throw new Error('size mismatch ('+o+' of '+u.length+' bytes)');
  return{k,ip,sr,dw,dp,D,S,C,nd,N,sn:new Float64Array(nd),cs:new Float64Array(nd)}}
 function els(d,tau){const r=[0,0,0,0,0,0],{sr,dw,dp,D,S,C,nd,sn,cs}=d;for(let i=0;i<nd;i++){const g=dp[i]+dw[i]*tau;sn[i]=Math.sin(g);cs[i]=Math.cos(g)}
  for(const s of sr){let a=0;for(let i=s.o,e=s.o+s.nt;i<e;i++){const x=D[i];a+=S[i]*sn[x]+C[i]*cs[x]}r[s.iv-1]+=a*(s.it?Math.pow(tau,s.it):1)}
  const T2=2*Math.PI;let l=(r[1]+FQ[IP[d.k]-1]*tau)%T2;if(l<0)l+=T2;r[1]=l;return r}
 function kep(v){const[xa,xl,xk,xh,xq,xp]=v,xfi=Math.sqrt(1-xk*xk-xh*xh),u=1/(1+xfi),ex2=xk*xk+xh*xh,ex=Math.sqrt(ex2),ex3=ex2*ex,gm=xl-Math.atan2(xh,xk);
  let e=xl+(ex-.125*ex3)*Math.sin(gm)+.5*ex2*Math.sin(2*gm)+.375*ex3*Math.sin(3*gm),ce,se,z3i,rsa;
  for(let it=0;it<60;it++){ce=Math.cos(e);se=Math.sin(e);z3i=xk*se-xh*ce;const dl=xl-e+z3i;rsa=1-(xk*ce+xh*se);e+=dl/rsa;if(Math.abs(dl)<1e-15)break}
  const xcw=(-xk+ce+u*xh*z3i)/rsa,xsw=(-xh+se-u*xk*z3i)/rsa,xm=xp*xcw-xq*xsw,xr=xa*rsa,xki=Math.sqrt(1-xq*xq-xp*xp);
  return[xr*(xcw-2*xp*xm),xr*(xsw+2*xq*xm),-2*xr*xki*xm]}
 const ready=k=>!!(ST[k]&&ST[k].d),
  ecl=(k,jd)=>ST[k]&&ST[k].d?kep(els(ST[k].d,(jd-2451545)/365250)):null, // heliocentric X,Y,Z (au), dynamical ecliptic & equinox J2000; jd = TDB Julian date
  equ=(k,jd)=>{const o=ecl(k,jd);return o&&[0,1,2].map(i=>AM[i][0]*o[0]+AM[i][1]*o[1]+AM[i][2]*o[2])}, // same, ICRS (the frame of the VSOP2013 Earth)
  elems=(k,jd)=>ST[k]&&ST[k].d?els(ST[k].d,(jd-2451545)/365250):null;
 function install(buf,src){const d=parse(buf),s=ST[d.k];s.d=d;s.src=src;s.st='ready';s.err='';return d.k}
 async function load(k){const s=ST[k];if(!s||s.d||s.st==='busy'||AV.indexOf(k)<0)return;s.st='busy';s.err='';const f='vsop2013_'+NM[k]+'.bin',e=window.__VSOP_B64&&window.__VSOP_B64[NM[k]]; // embedded copy (single-file release) or fetch next to this page (not from file://)
  try{let buf,src;if(typeof e==='string'){const a=atob(e),b=new Uint8Array(a.length);for(let i=0;i<a.length;i++)b[i]=a.charCodeAt(i);buf=b.buffer;src='embedded'}else{const r=await fetch(f);if(!r.ok)throw new Error(f+': HTTP '+r.status);buf=await r.arrayBuffer();src=f}
   const k2=install(buf,src);if(k2!==k)throw new Error(f+' holds another planet')}catch(x){s.st='fail';s.err=String(x&&x.message||x)}}
 function pick(file){const m=NM.findIndex(n=>String(file.name).toLowerCase().indexOf(n)>=0),k0=m>=0?m:AV[0];ST[k0].st='busy';
  return file.arrayBuffer().then(b=>{const k=install(b,file.name);if(k!==k0&&!ST[k0].d)ST[k0].st='idle';return k}).catch(e=>{const s=ST[k0];s.st=s.d?'ready':'fail';s.err=String(e&&e.message||e)})} // a rejected file never discards data that is already loaded
 return{NM,IP,AV,ST,ready,load,pick,ecl,equ,elems,AM,want(k){if(AV.indexOf(k)>=0&&ST[k].st==='idle')load(k)}}})();
window.ASTERID_VSOP=VSP;
window.vpAudit=function(){const G='VSOP2013 planets',A=[];
 if(!VSP.ready(1)){A.push({g:G,n:'Venus vs VSOP2013.ctl and IPS2000',info:'vsop2013_venus.bin not loaded: checks skipped',ok:true});return A}
 const add=(n,res,tol,u,note)=>A.push({g:G,n,res,tol,u,ok:Math.abs(res)<=tol,note}),CT=[[2411545.0,0.723326846,3.0850544129,-0.0045575903,0.0051297811,0.0066724242,0.0288666759,-0.7178452078,0.0333612116,0.0419440586,-0.7178452043,0.0139241146,0.0517532468],[2415545.0,0.7233324174,1.837535548,-0.0045492198,0.0050926797,0.0066865271,0.0288624835,-0.1846603189,0.6945108298,0.0199735492,-0.1846601606,0.6292563055,0.294585804],[2419545.0,0.7233307847,0.5899962012,-0.0045138166,0.0050804051,0.0067036156,0.0288576099,0.606134187,0.394892364,-0.0297279072,0.6061342811,0.3741316134,0.1298042734],[2423545.0,0.7233242646,5.6256196213,-0.0044862176,0.0050923304,0.0067188329,0.0288543092,0.5740438364,-0.4462445681,-0.039175358,0.5740437374,-0.3938385063,-0.2134485135],[2427545.0,0.7233283654,4.3780843283,-0.0044962075,0.0051193425,0.0067338093,0.0288483287,-0.2299140883,-0.6883942737,0.0039995095,-0.2299142475,-0.6331803015,-0.2701579257],[2431545.0,0.7233426547,3.130624868,-0.0045185605,0.0050791039,0.0067486759,0.0288435809,-0.7188539134,0.0003328518,0.0415278154,-0.7188539175,-0.0162132431,0.0382334294],[2435545.0,0.72332487,1.8830820759,-0.00447874,0.0050664598,0.0067632182,0.0288410458,-0.2164925613,0.6851263387,0.0217837465,-0.2164924053,0.6199261557,0.292513693],[2439545.0,0.723326222,0.635526442,-0.0044880019,0.005096827,0.0067777408,0.0288357363,0.5874138776,0.4219151061,-0.0281948833,0.5874139778,0.3983146995,0.1419598205],[2443545.0,0.7233314949,5.6711894725,-0.0045224241,0.0050966509,0.0067942167,0.0288317136,0.593513803,-0.4198978251,-0.0399824355,0.5935137101,-0.3693448084,-0.2037088644],[2447545.0,0.7233310596,4.4236836479,-0.0045326382,0.0050523635,0.0068089673,0.0288282881,-0.1985959819,-0.6982283962,0.0019444959,-0.1985961433,-0.6413855038,-0.2759551516],[2451545.0,0.7233269276,3.176134927,-0.0045086048,0.0050312156,0.0068248163,0.0288221117,-0.7183022848,-0.0326544811,0.0410142477,-0.7183022964,-0.0462742464,0.0246406381]];
 let me=0,mq=0,mel=0;
 for(const r of CT){const o=VSP.ecl(1,r[0]),q=VSP.equ(1,r[0]),el=VSP.elems(1,r[0]);
  for(let i=0;i<3;i++){me=Math.max(me,Math.abs(o[i]-r[7+i]));mq=Math.max(mq,Math.abs(q[i]-r[10+i]))}
  for(let i=0;i<6;i++){let d=Math.abs(el[i]-r[1+i]);if(i===1)d=Math.min(d,2*Math.PI-d);mel=Math.max(mel,d)}}
 add('Venus X,Y,Z (dynamical ecliptic J2000) vs VSOP2013.ctl, 11 epochs 1890\u20132000, max |\u0394|',me,1e-10,'au','ctl = full series, printed to 10 decimals (rounding 5e-11); series read from vsop2013_venus.bin (289 646 terms + mean motion of l)');
 add('Venus X,Y,Z in ICRS (README rotation \u03b5, \u03c6) vs VSOP2013.ctl, max |\u0394|',mq,1e-10,'au');
 add('Venus elliptic elements a, l, k, h, q, p vs VSOP2013.ctl, max |\u0394| (l modulo 2\u03c0)',mel,1e-10,'','a in au, l in rad, k, h, q, p dimensionless; mean longitude includes the mean-motion term that VSOP2013.f adds to the l series');
 let mc=0;for(let i=0;i<11;i++){const jd=1903670.5+73000*i,o=VSP.ecl(1,jd),p=IPS.helio(1,jd);mc=Math.max(mc,Math.hypot(o[0]-p[0],o[1]-p[1],o[2]-p[2]))}
 add('Venus VSOP2013 vs IPS2000 (independent theory), 11 epochs 500\u20132498, max 3-D |\u0394|',mc,2e-7,'au','tolerance = quadrature of declared errors (IPS2000 vs DE406 and VSOP2013 vs INPOP10a, both \u2264 0.03\u2033 on the longitude of Venus); the two theories are fitted to different ephemerides');
 return A};
