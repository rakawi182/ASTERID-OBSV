"""test_vsop2013_bin.py -- checks a vsop2013_<planet>.bin against VSOP2013.ctl (elements and heliocentric X,Y,Z, dynamical ecliptic J2000).
Usage: python3 test_vsop2013_bin.py vsop2013_venus.bin VSOP2013.ctl
Reads the .bin with an independent NumPy decoder, sums the series, adds the mean motion of l (VSOP2013.f: freqpla) and solves Kepler as ELLXYZ does.
The reference is printed to 10 decimals, so about 5e-11 per component is the floor."""
import struct,numpy as np,re,sys,math
CI0=[4.402608631669,3.176134461576,1.753470369433,6.203500014141,4.091360003050,1.713740719173,5.598641292287,2.805136360408,2.326989734620,.599546107035,.874018510107,5.481225395663,5.311897933164,0,5.198466400630,1.627905136020,2.355555638750]
CI1=[26087.90314068555,10213.28554743445,6283.075850353215,3340.612434145457,1731.170452721855,1704.450855027201,1428.948917844273,1364.756513629990,1361.923207632842,529.6909615623250,213.2990861084880,74.78165903077800,38.13297222612500,.3595362285049309,77713.7714481804,84334.6615717837,83286.9142477147]
FREQ=[26087.90314068555,10213.28554743445,6283.075850353215,3340.612434145457,529.6909615623250,213.2990861084880,74.78165903077800,38.13297222612500,0.3595362285049309]
b=open(sys.argv[1],'rb').read();assert b[:4] in(b'VS13',b'VS14');W16=b[:4]==b'VS14';ip=b[4];ns=b[5];nd=struct.unpack_from('<H',b,6)[0];o=8
sr=[]
for i in range(ns):
    iv,it,nt,nb=struct.unpack_from('<BBII',b,o);o+=10;sr.append((iv,it,nt,nb))
dw=np.zeros(nd);dp=np.zeros(nd)
for d in range(nd):
    w=f=0
    for j in range(17):
        if j==13:a=struct.unpack_from('<H',b,o)[0];o+=2
        elif W16:a=struct.unpack_from('<h',b,o)[0];o+=2
        else:a=struct.unpack_from('<b',b,o)[0];o+=1
        w+=a*CI1[j];f+=a*CI0[j]
    dw[d]=w;dp[d]=f
data=[]
for iv,it,nt,nb in sr:
    dt1=np.dtype([('d','<u2'),('s','<f8'),('c','<f8')]);a1=np.frombuffer(b,dt1,nb,o);o+=nb*dt1.itemsize
    dt2=np.dtype([('d','<u2'),('s','<f4'),('c','<f4')]);a2=np.frombuffer(b,dt2,nt-nb,o);o+=(nt-nb)*dt2.itemsize
    data.append((iv,it,np.concatenate([a1['d'],a2['d']]),np.concatenate([a1['s'],a2['s']]).astype(float),np.concatenate([a1['c'],a2['c']]).astype(float)))
assert o==len(b),(o,len(b))
def els(tau):
    r=[0]*6
    for iv,it,d,S,C in data:
        g=dp[d]+dw[d]*tau
        r[iv-1]+=(S*np.sin(g)+C*np.cos(g)).sum()*(tau**it if it else 1)
    r[1]=(r[1]+FREQ[ip-1]*tau)%(2*math.pi);return r
def kep(v):
    xa,xl,xk,xh,xq,xp=v;xfi=math.sqrt(1-xk*xk-xh*xh);u=1/(1+xfi);ex2=xk*xk+xh*xh;ex=math.sqrt(ex2);ex3=ex2*ex;gm=xl-math.atan2(xh,xk)
    e=xl+(ex-.125*ex3)*math.sin(gm)+.5*ex2*math.sin(2*gm)+.375*ex3*math.sin(3*gm)
    for _ in range(60):
        ce=math.cos(e);se=math.sin(e);z3i=xk*se-xh*ce;dl=xl-e+z3i;rsa=1-(xk*ce+xh*se);e+=dl/rsa
        if abs(dl)<1e-15:break
    xcw=(-xk+ce+u*xh*z3i)/rsa;xsw=(-xh+se-u*xk*z3i)/rsa;xm=xp*xcw-xq*xsw;xr=xa*rsa;xki=math.sqrt(1-xq*xq-xp*xp)
    return [xr*(xcw-2*xp*xm),xr*(xsw+2*xq*xm),-2*xr*xki*xm]
txt=open(sys.argv[2]).read().replace('\r','')
name=['MERCURY','VENUS','EMB','MARS','JUPITER','SATURN','URANUS','NEPTUNE','PLUTO'][ip-1]
blk=[x for x in re.split(r'PLANETARY EPHEMERIS VSOP2013\s+',txt) if x.startswith(name)][0]
ep=re.findall(r'Julian Date JD\s+([\d.]+) \(TDB\)\n(.*)\n(.*)\n(.*)',blk)
mx=[0]*6;mxy=0
for jd,l1,l2,l3 in ep:
    tau=(float(jd)-2451545.0)/365250
    ref=[float(x) for x in l1.split()];xy=[float(x) for x in l2.split()][:3]
    v=els(tau);p=kep(v)
    for i in range(6):
        d=abs(v[i]-ref[i])
        if i==1:d=min(d,2*math.pi-d)
        mx[i]=max(mx[i],d)
    mxy=max(mxy,max(abs(p[i]-xy[i]) for i in range(3)))
print(name,len(ep),'epochs; max|d| a,l,k,h,q,p:',['%.1e'%x for x in mx],' xyz: %.1e au = %.4f km'%(mxy,mxy*149597870.7))
