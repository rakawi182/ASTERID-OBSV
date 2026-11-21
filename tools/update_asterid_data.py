#!/usr/bin/env python3
"""Update the data embedded in ASTERID.html (IERS EOP series and ESMGFZ loading grids).

Typical use (new IERS files downloaded):
  python3 update_asterid_data.py ASTERID.html --c04 EOP_20u24_C04_one_file_1962-now.txt --bulletin bulletina-xxxix-043.txt
  python3 update_asterid_data.py ASTERID.html --bulletin bulletina-xxxix-044.txt        # only the weekly Bulletin A
  python3 update_asterid_data.py ASTERID.html --c04 EOP_20u24_C04_one_file_1962-now.txt   # only the C04 series

Options:
  --out FILE      write to FILE instead of overwriting the input (recommended: keep the old file as a backup)
  --start DATE    first day of the embedded EOP table, YYYY-MM-DD or MJD. Default: the first day already in the file, so the
                  table never shrinks. The full IERS 20C04 series begins on 1962-01-01 (MJD 37665).
  --dry-run       parse and report everything, write nothing
  --force         accept a C04 file that ends before the C04 data already embedded (normally an error)
  --ntal/--ntol/--hydl/--slel            ESMGFZ loading CSV files, analysis (final) series
  --ntal-fc/--ntol-fc/--hydl-fc/--slel-fc  ESMGFZ loading CSV files, forecast (e.g. *_2026_324F_pointsubset.csv)

Rules: the embedded table is daily and gap-free. IERS 20C04 (final) ends at the C04 file's last day; Bulletin A adds rapid
(observed) values up to its last observation and predictions beyond. Days in the file that are newer than a new C04 file are kept
when no new Bulletin A is given.

ESMGFZ loading: each series is stored as analysis samples, then (optionally) forecast samples on the same grid. NTD keeps 'fc'
(first forecast sample) and 'fb' (last analysis sample, equal to 'fc' when the two are contiguous); the page labels each value by
source from them. An analysis CSV extends the analysis and replaces any forecast samples it covers (it must be contiguous with the
embedded analysis). A forecast CSV replaces the whole forecast part; samples at or before the analysis end are ignored, and a gap
between the analysis end and the first forecast sample is bridged linearly (flagged in the page). Replace forecasts with analysis
as soon as ESMGFZ publishes it, e.g.:
  python3 update_asterid_data.py ASTERID.html --out ASTERID_new.html \\
      --ntal ESMGFZ_NTAL_..._2026_pointsubset.csv --ntal-fc ESMGFZ_NTAL_..._2026_324F_pointsubset.csv   (same for ntol, hydl, slel)
"""
import argparse,base64,csv,datetime,json,re,sys,zlib
import numpy as np
ap=argparse.ArgumentParser(description='Update the data embedded in ASTERID.html (see the module docstring).')
ap.add_argument('html');ap.add_argument('--out');ap.add_argument('--c04');ap.add_argument('--bulletin');ap.add_argument('--start');ap.add_argument('--dry-run',action='store_true');ap.add_argument('--force',action='store_true')
for k in('ntal','ntol','hydl','slel'):ap.add_argument('--'+k);ap.add_argument('--'+k+'-fc',dest=k+'_fc')
a=ap.parse_args();out=a.out or a.html
s=open(a.html,encoding='utf-8').read()
def mjd_of(t):return (datetime.datetime.strptime(t,'%Y-%m-%dT%H:%M:%SZ')-datetime.datetime(1858,11,17)).total_seconds()/86400
def date_of(m):return (datetime.datetime(1858,11,17)+datetime.timedelta(days=float(m))).strftime('%Y-%m-%d')
def start_of(t):
    t=t.strip()
    return int(float(t)) if re.fullmatch(r'\d+(\.\d+)?',t) else int(mjd_of(t+'T00:00:00Z'))
# The EOP block lives in const D=JSON.parse(__zt("<base64 raw-deflate JSON>",<uncompressed byte length>)); D holds 'eop','c04','pr', ...
DRE=re.compile(r'const D=JSON\.parse\(__zt\("([A-Za-z0-9+/=]+)",(\d+)\)\);')
def load_D(txt):
    m=DRE.search(txt);assert m,'EOP block (const D=JSON.parse(__zt(...))) not found'
    raw=zlib.decompress(base64.b64decode(m.group(1)),-15);assert len(raw)==int(m.group(2)),'D length mismatch'
    d=json.loads(raw);assert all(k in d for k in('eop','c04','pr')),'D has no eop/c04/pr';return m,d
def dump_D(d):
    raw=json.dumps(d,separators=(',',':')).encode('utf-8');z=zlib.compressobj(9,zlib.DEFLATED,-15);b=z.compress(raw)+z.flush()
    assert zlib.decompress(b,-15)==raw
    return 'const D=JSON.parse(__zt("%s",%d));'%(base64.b64encode(b).decode(),len(raw))
# ---------------- EOP ----------------
if a.c04 or a.bulletin:
    m,DD=load_D(s);old_c04=int(DD['c04']);old_pr=int(DD['pr'])
    old={int(r[0]):r for r in DD['eop']};c04={};rap={};pred={};dxy={};issue=''
    if a.c04:
        for ln in open(a.c04):
            f=ln.split()
            if len(f)>=13 and f[0].isdigit() and len(f[0])==4:c04[int(float(f[4]))]=[float(f[7]),float(f[5]),float(f[6]),float(f[8]),float(f[9]),float(f[12])]
        assert c04,'no C04 rows'
    else:c04={int(k):[r[1],r[2],r[3],r[4],r[5],r[6]] for k,r in old.items() if k<=old_c04}
    c04_last=max(c04);old_first=int(min(old));old_last=int(max(old))
    if a.c04:  # how much did IERS revise the part of the series that was already embedded as final C04?
        both=[k for k in c04 if k in old and k<=old_c04]
        if both:
            rev=np.abs(np.array([[c04[k][i]-old[k][i+1] for i in range(6)] for k in both]));names=['UT1-UTC (s)','x (arcsec)','y (arcsec)','dX (arcsec)','dY (arcsec)','LOD (s)']
            print('C04 revisions over %d overlapping days (max |new - embedded|): '%len(both)+', '.join('%s %.2e'%(n,v) for n,v in zip(names,rev.max(0)))+('   <-- REVISED DATA: regenerate the audit reference rows' if rev.max()>2e-7 else ''))
        if c04_last<old_c04 and not a.force:sys.exit('ERROR: the C04 file ends (MJD %d, %s) before the C04 already embedded (MJD %d, %s): truncated or older file? Use --force to accept.'%(c04_last,date_of(c04_last),old_c04,date_of(old_c04)))
    if a.bulletin:
        txt=open(a.bulletin).read();mm=re.search(r'(\d+ \w+ \d{4})\s+Vol\. (\S+) No\. (\d+)',txt);issue='%s, Vol. %s No. %s'%mm.groups() if mm else ''
        for ln in txt.split('\n'):
            r=re.match(r'^\s+\d\d\s+\d+\s+\d+\s+(\d{5})\s+(-?[\d.]+)\s+[\d.]+\s+(-?[\d.]+)\s+[\d.]+\s+(-?[\d.]+)\s+[\d.]+\s*$',ln)
            if r:rap[int(r.group(1))]=[float(r.group(4)),float(r.group(2)),float(r.group(3))]
            r=re.match(r'^\s+\d{4}\s+\d+\s+\d+\s+(\d{5})\s+(-?[\d.]+)\s+(-?[\d.]+)\s+(-?[\d.]+)\s*$',ln)
            if r:pred[int(r.group(1))]=[float(r.group(4)),float(r.group(2)),float(r.group(3))]
        i=txt.find('IAU2000A Celestial Pole Offset')
        if i>0:
            for ln in txt[i:].split('\n'):
                r=re.match(r'^\s+(\d{5})\s+(-?[\d.]+)\s+[\d.]+\s+(-?[\d.]+)\s+[\d.]+\s*$',ln)
                if r:dxy[int(r.group(1))]=[float(r.group(2))/1e3,float(r.group(3))/1e3]
        assert rap and pred,'Bulletin A rapid/prediction tables not parsed'
        if not dxy:  # some Bulletin A issues carry no dX,dY table: keep the dX,dY already embedded (FCN_T0 unchanged)
            fm=re.search(r'const FCN_T0=(\d+)',s);assert fm,'FCN_T0 not found';f0=int(fm.group(1))
            dxy={k:[old[k][4],old[k][5]] for k in old if c04_last<k<=f0}
            if not dxy:dxy={c04_last:[c04[c04_last][3],c04[c04_last][4]]}
            print('WARNING: this Bulletin A has no dX,dY (celestial pole offset) table: keeping the embedded dX,dY up to MJD %d and holding the last value beyond (FCN_T0 unchanged)'%max(dxy))
    ser={}
    if a.c04 and not a.bulletin:  # keep the rapid/prediction days that are already embedded and newer than the new C04 end
        for k,r in old.items():
            if k>c04_last:ser[int(k)]=[r[1],r[2],r[3],r[4],r[5],r[6]]
    for k,v in c04.items():ser[k]=v
    first_b=min(list(rap)+list(pred)) if a.bulletin else None
    if a.bulletin:
        for k in range(c04_last+1,first_b):
            assert k in old,'gap MJD %d between C04 and Bulletin A is not in the old table: add finals2000A or the previous Bulletin A'%k
            ser[k]=[old[k][1],old[k][2],old[k][3],old[k][4],old[k][5],old[k][6]]
        prev=None
        for k in sorted(set(rap)|set(pred)):
            u,x,y=(rap.get(k) or pred.get(k));p=ser[k-1][0];ser[k]=[u,x,y,0,0,round(-(u-p),7)]
        dlast=max(dxy);d0=min(dxy)
        for k in sorted(ser):
            if k<=c04_last:continue
            if k<d0:f=(k-c04_last)/(d0-c04_last);ser[k][3]=ser[c04_last][3]+f*(dxy[d0][0]-ser[c04_last][3]);ser[k][4]=ser[c04_last][4]+f*(dxy[d0][1]-ser[c04_last][4])
            else:v=dxy[min(k,dlast)];ser[k][3],ser[k][4]=v
        fcn=max(dxy);pr=max(rap);last=max(ser)
    else:
        fcn=None;pr=max(old_pr,c04_last);last=max(ser)
    start=start_of(a.start) if a.start else old_first
    if min(ser)>start:print('WARNING: --start %s is earlier than the first available day (%s); the table starts there'%(date_of(start),date_of(min(ser))))
    rows=[[float(k)]+[round(x,7) for x in ser[k]] for k in sorted(ser) if k>=start]
    gaps=[int(rows[i][0]) for i in range(len(rows)-1) if rows[i+1][0]-rows[i][0]!=1];assert not gaps,'EOP table must be daily and gap-free; gap after MJD %s'%gaps[:5]
    assert len(rows)>=3 and rows[-1][0]>=old_last-366,'the new table ends much earlier than the embedded one: wrong input files?'
    DD['eop']=rows;DD['c04']=c04_last;DD['pr']=pr
    s=s[:m.start()]+dump_D(DD)+s[m.end():]
    if fcn:
        s,n=re.subn(r'const FCN_T0=\d+','const FCN_T0=%d'%fcn,s);assert n==1
        s,n=re.subn(r'last tabulated dX,dY \(MJD \d+\)','last tabulated dX,dY (MJD %d)'%fcn,s);assert n==1
    s,n=re.subn(r'beyond MJD \d+ \(\d{4}-\d\d-\d\d\) the table edge is held','beyond MJD %d (%s) the table edge is held'%(last,date_of(last)),s);assert n==1
    print('EOP: C04 to MJD %d (%s), Bulletin A %s: rapid to %d, predictions to %d (%s); FCN_T0 %s'%(c04_last,date_of(c04_last),issue,pr,last,date_of(last),fcn))
    print('EOP table: %d daily rows, MJD %d (%s) .. %d (%s), %.3f MB embedded'%(len(rows),rows[0][0],date_of(rows[0][0]),rows[-1][0],date_of(rows[-1][0]),len(json.dumps(rows,separators=(',',':')))/1e6))
# ---------------- ESMGFZ loading ----------------
FS=('ntal','ntol','hydl','slel')
files={k:getattr(a,k) for k in FS if getattr(a,k)};fcs={k:getattr(a,k+'_fc') for k in FS if getattr(a,k+'_fc')}
if files or fcs:
    m=re.search(r'const NTD=(\{.*?\});\n',s,re.S);assert m,'NTD block not found';NT=json.loads(m.group(1))
    assert 'src:m<=s.fb' in s,'this ASTERID.html has no forecast support (source flags): use the version that labels analysis/forecast'
    def read_csv(f,o):
        rows=list(csv.reader(open(f)));h=rows[0];cols=[i for i,c in enumerate(h) if c.startswith(('duEW','duNS','duV'))];assert len(cols)==3,'columns duEW, duNS, duV expected'
        t=np.array([mjd_of(r[0]) for r in rows[1:]]);v=np.array([[float(r[i]) for i in cols] for r in rows[1:]])
        idx=np.round((t-o['t0'])/o['dt']).astype(int);assert np.allclose(t,o['t0']+o['dt']*idx,atol=1e-6),'CSV times are not on the embedded grid'
        od=np.argsort(idx);idx=idx[od];v=v[od];assert np.all(np.diff(idx)>0),'duplicate CSV times';return idx,v
    for k in FS:
        if k not in files and k not in fcs:continue
        o=NT[k];arr=np.frombuffer(base64.b64decode(o['b']),dtype='<f4').reshape(-1,3).copy();n0=len(arr);t0=o['t0'];dt=o['dt']
        fi=int(round((o['fc']-t0)/dt)) if 'fc' in o else None   # index of the first forecast sample
        ae=(int(round((o['fb']-t0)/dt)) if o['fb']<o['fc'] else fi-1) if fi is not None else n0-1   # index of the last analysis sample
        A=arr[:ae+1];F=arr[fi:] if fi is not None else arr[:0];msg=[]
        if k in files:
            idx,v=read_csv(files[k],o);ov=idx<=ae;d=np.abs(A[idx[ov]]-v[ov]).max() if ov.any() else 0.
            new=idx>ae;ii=idx[new];vv=v[new]
            if len(ii):assert ii[0]==ae+1 and np.all(np.diff(ii)==1),'%s: new analysis samples are not contiguous with the embedded analysis (gap)'%k
            if fi is not None:   # how far off was the stored forecast where the analysis now covers it?
                cv=(idx>=fi)&(idx<fi+len(F))
                if cv.any():msg.append('stored forecast vs new analysis over %d samples: max |diff| = %.2e m'%(cv.sum(),np.abs(F[idx[cv]-fi]-v[cv]).max()))
            A=np.vstack([A,vv.astype('<f4')]) if len(ii) else A;ae+=len(ii)
            if fi is not None:   # forecast samples covered by the analysis are dropped
                if ae+1>fi:F=F[ae+1-fi:];fi=ae+1
                if len(F)==0:F=arr[:0];fi=None
            msg.insert(0,'analysis +%d samples, max |embedded - new CSV| over %d overlapping samples = %.2e m%s'%(len(ii),ov.sum(),d,'  <-- REVISED DATA: regenerate the audit reference rows' if d>1e-6 else ''))
        if k in fcs:
            idx,v=read_csv(fcs[k],o);keep=idx>ae
            assert keep.any(),'%s: the forecast CSV has no sample after the analysis end (%s)'%(k,date_of(t0+dt*ae))
            ii=idx[keep];vv=v[keep];assert np.all(np.diff(ii)==1),'%s: forecast samples are not contiguous'%k
            F=vv.astype('<f4');fi=int(ii[0]);msg.append('forecast %d samples (%d at or before the analysis end ignored)'%(len(ii),int((~keep).sum())))
        nb=(fi-ae-1) if fi is not None else 0
        B=np.column_stack([np.interp(np.arange(ae+1,fi),[ae,fi],[A[ae,q],F[0,q]]) for q in range(3)]).astype('<f4') if nb>0 else arr[:0]
        full=np.vstack([A,B,F]).astype('<f4');n=len(full)
        o2={'t0':t0,'dt':dt,'n':n}
        if fi is not None:fc=t0+dt*fi;o2['fb']=fc if nb==0 else t0+dt*ae;o2['fc']=fc
        o2['b']=base64.b64encode(full.tobytes()).decode();NT[k]=o2
        print('%s: analysis to %s (%d samples)%s; %s; %s'%(k.upper(),date_of(t0+dt*ae),ae+1,', forecast %s..%s (%d samples), bridge %d'%(date_of(t0+dt*fi),date_of(t0+dt*(n-1)),len(F),nb) if fi is not None else ', no forecast','; '.join(msg),'now %d samples'%n))
    s=s[:m.start()]+'const NTD='+json.dumps(NT,separators=(',',':'))+';\n'+s[m.end():]
    ael=[(o['fb'] if o['fb']<o['fc'] else o['fc']-o['dt']) if 'fc' in o else o['t0']+o['dt']*(o['n']-1) for o in NT.values()]
    fo=[o for o in NT.values() if 'fc' in o];cap='analysis 2024-01-01 to %s'%date_of(min(ael))
    if fo:cap+=', then forecast %s to %s'%(date_of(min(o['fc'] for o in fo)),date_of(max(o['t0']+o['dt']*(o['n']-1) for o in fo)))
    s,n=re.subn(r'analysis 2024-01-01 to \d{4}-\d\d-\d\d(?:, then forecast \d{4}-\d\d-\d\d to \d{4}-\d\d-\d\d)?, each row labelled',cap+', each row labelled',s);assert n==1,'ESMGFZ caption not found'
    print('ESMGFZ caption: '+cap)
if a.dry_run:print('dry run: nothing written')
else:open(out,'w',encoding='utf-8').write(s);print('written',out)