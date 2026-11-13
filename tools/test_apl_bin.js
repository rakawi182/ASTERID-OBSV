// node test_apl_bin.js ASTERID.html apl_rp_1.bin ref.json   - decoder and apGrid checked against float64 numpy reference
const fs=require('fs'),vm=require('vm');
const html=fs.readFileSync(process.argv[2],'utf8');
// 1. every <script> must compile
let bad=0,n=0;for(const m of html.matchAll(/<script[^>]*>([\s\S]*?)<\/script>/g)){n++;try{new vm.Script(m[1])}catch(e){bad++;console.log('SYNTAX',e.message)}}
console.log('scripts compiled:',n-bad,'of',n);
// 2. pull the pieces
const cut=(a,b)=>{const i=html.indexOf(a);if(i<0)throw new Error('missing '+a);const j=html.indexOf(b,i);return html.slice(i,j)};
const zl=cut('const __zi=','const __zt=');
const crc=cut('function g3crc','function g3Parse');
const od=cut('const OD={','const FA=OD.fa');
const fa=cut('const FA=OD.fa','function fundArgs')+cut('function fundArgs','function aplRad');
const apl=cut('function aplRad','/* ---- non-tidal loading');
const ap=cut('const AP={','/* ---- frames ---- */');
const ctx={atob,Math,console,window:{},fetch:null,Float64Array,Int32Array,Int16Array,Uint8Array,Uint32Array,Uint16Array,DataView,String,Error,Promise};
vm.createContext(ctx);
vm.runInContext('const D2R=Math.PI/180;'+zl+crc+od+fa+apl+ap+';this.AP=AP;this.apParse=apParse;this.apGrid=apGrid;this.aplRad=aplRad;this.OD=OD;',ctx);
const buf=fs.readFileSync(process.argv[3]);ctx.apParse(buf.buffer.slice(buf.byteOffset,buf.byteOffset+buf.length));
const ref=JSON.parse(fs.readFileSync(process.argv[4],'utf8'));
let mx=0,mr=0;for(const p of ref.pts){const g=ctx.apGrid(p.lat,p.lon);ctx.AP.W.forEach((k,q)=>{mx=Math.max(mx,Math.abs(g[k].C-p.v[2*q]),Math.abs(g[k].S-p.v[2*q+1]));mr=Math.max(mr,Math.hypot(p.v[2*q],p.v[2*q+1]))})}
console.log('apGrid vs numpy bilinear (float64), '+ref.pts.length+' points, max |d| = '+mx.toExponential(2)+' m (max amplitude '+mr.toExponential(2)+' m)');
// 3. aplRad with station constants unchanged, and with grid coefficients at the station
const t=61000.25,a0=ctx.aplRad(t),a1=ctx.aplRad(t,ctx.OD.apls);console.log('aplRad default vs explicit station set:',a0-a1);
const g=ctx.apGrid(-7.609444,112.595556);let dm=0,dmax=0;for(const k of ctx.AP.W){dm=Math.max(dm,Math.hypot(g[k].C-ctx.OD.apls[k].C,g[k].S-ctx.OD.apls[k].S))}
let rms=0,mxs=0;for(let i=0;i<24*30;i++){const tt=61000+i/24,d=ctx.aplRad(tt,g)-ctx.aplRad(tt);rms+=d*d;mxs=Math.max(mxs,Math.abs(d))}
console.log('grid at the station vs station constants: max |dC,S| '+(dm*1e3).toFixed(3)+' mm; hourly series over 30 d: rms '+(Math.sqrt(rms/720)*1e3).toFixed(3)+' mm, max '+(mxs*1e3).toFixed(3)+' mm');
