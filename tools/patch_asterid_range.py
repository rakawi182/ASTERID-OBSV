#!/usr/bin/env python3
"""Perluas rentang tab PLANETS dan SKY VIEW di ASTERID.html dari 500-2498 CE (IPS2000)
ke -4000..+8000 (rentang deret VSOP2013 dan model Bumi).

Pemakaian: python3 patch_asterid_range.py ASTERID.html ASTERID_out.html
Syarat: ASTERID.html sudah memuat ketujuh planet VSOP2013 (AV=[0,1,2,3,4,5,6]).
Setiap penggantian harus cocok tepat 1 kali; bila tidak, skrip berhenti tanpa menulis apa pun.

Desain:
 - di dalam 500-2498 CE perilaku lama dipertahankan: VSOP2013, cadangan IPS2000 bila .bin belum termuat;
 - di luar 500-2498 CE tidak ada cadangan IPS2000; plCompute meminta SEMUA .bin planet (VSP.want) dan
   mengembalikan null sampai ketujuhnya siap (tab menampilkan status muat + tombol LOAD);
 - di luar -4000..+8000 (VSP.JD0/JD1 = 260045/4643045, sama dengan modul Matahari) plCompute mengembalikan null.
"""
import sys

src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8', newline='').read()
n0 = len(s.encode('utf-8'))

R = []  # (jangkar, pengganti)

# 1. batas rentang VSOP2013 diekspor dari modul VSP
R.append(("return{NM,IP,AV,ST,ready,load,pick,ecl,equ,elems,fast,AM,want(k)",
          "return{NM,IP,AV,ST,ready,load,pick,ecl,equ,elems,fast,AM,JD0:260045,JD1:4643045,want(k)"))

# 2. PHL: cadangan IPS2000 hanya di dalam rentangnya sendiri
R.append(("const PHL=(k,t)=>VSP.fast(k,t)||IPS.equ(IPS.helio(k,t));",
          "let plWhy='';\nconst PHL=(k,t)=>VSP.fast(k,t)||((t>=IPS.JD0&&t<=IPS.JD1)?IPS.equ(IPS.helio(k,t)):null);"))

# 3. gerbang plCompute
R.append(("||jt<IPS.JD0+1||jt>IPS.JD1-1)return null;",
          "||jt<VSP.JD0+1||jt>VSP.JD1-1){plWhy='range';return null}\n"
          " if(jt<IPS.JD0+1||jt>IPS.JD1-1){let rd=true;for(let k=0;k<7;k++){VSP.want(k);if(!VSP.ready(k))rd=false}if(!rd){plWhy='vsop';return null}}\n"
          " plWhy='';"))

# 4. pesan tab PLANETS bila tidak ada data
R.append(("B.innerHTML='<div class=\"cap\">Planets are available from 500 to 2498 CE (IPS2000) within the VSOP2013 range of the Earth model.</div>';return}",
          "B.innerHTML=plWhy==='vsop'?'<div class=\"cap\" style=\"margin-bottom:8px\">Outside 500–2498 CE the planets come from the VSOP2013 files only (there is no IPS2000 fallback there), and not all seven are loaded yet.</div>'+vsN():'<div class=\"cap\">Planets are available from −4000 to +8000 (VSOP2013 range of the Earth model).</div>';return}"))

# 5. keterangan rentang di luar 500-2498 + definisi rngN
R.append(("let vsS='';const vsN=",
          "const rngN=()=>{const jt=DATA.ms/864e5+2440587.5;return(jt<IPS.JD0+1||jt>IPS.JD1-1)?'<div class=\"cap\" style=\"margin-bottom:8px\">Outside 500–2498 CE the positions come from VSOP2013 alone; there is no independent series to compare with. Declared error of the heliocentric longitude against INPOP10a over −4000…+8000 (IMCCE README): Mercury 0.20″, Venus 0.15″, Mars 1.74″, Jupiter 4.47″, Saturn 11.73″, Uranus 2.45″, Neptune 1.27″; the largest errors lie far from the fit window 1890–2000.</div>':''};\nlet vsS='';const vsN="))
R.append(("B.innerHTML=ban+vsN()+ecp+", "B.innerHTML=ban+vsN()+rngN()+ecp+"))

# 6. teks status per planet
R.append(("planets without a loaded file use IPS2000.${", "planets without a loaded file use IPS2000 (500–2498 CE only).${"))
R.append(("IPS2000 is used until it is ready.</div>", "IPS2000 is used until it is ready (500–2498 CE only).</div>"))
R.append(("cannot be fetched from file://; IPS2000 is used.", "cannot be fetched from file://; IPS2000 is used (500–2498 CE only; outside it this planet is not shown)."))

# 7. teks panel SKY VIEW
old7 = ("PLANETS draws Mercury to Neptune from the full IPS2000 series (Chapront &amp; Francou 2002, 500–2498 CE, no truncation; Mercury, Venus, Mars, Jupiter, Saturn, Uranus and Neptune from the full VSOP2013 series when vsop2013_mercury.bin, vsop2013_venus.bin, vsop2013_mars.bin, vsop2013_jupiter.bin, vsop2013_saturn.bin, vsop2013_uranus.bin and vsop2013_neptune.bin are loaded)")
new7 = ("PLANETS draws Mercury to Neptune from the full VSOP2013 series (Simon et al. 2013, −4000…+8000, no truncation) when vsop2013_mercury.bin, vsop2013_venus.bin, vsop2013_mars.bin, vsop2013_jupiter.bin, vsop2013_saturn.bin, vsop2013_uranus.bin and vsop2013_neptune.bin are loaded; within 500–2498 CE a planet whose file is not loaded falls back to the full IPS2000 series (Chapront &amp; Francou 2002, no truncation), outside it all seven files are required")
R.append((old7, new7))

# 8. audit: jalur cepat vs deret eksak di seluruh rentang
R.append(("or more')}}\n return A};",
          "or more')}\n"
          "  {let mf=0;for(const jd of[260100.5,700000.3,1200000.7,1721000.1,2159190.3,3000000.4,3500000.8,3900000.2,4300000.6,4642000.5]){const e=VSP.equ(k,jd);let f;for(let c=0;c<4;c++)f=VSP.fast(k,jd);for(let i=0;i<3;i++)mf=Math.max(mf,Math.abs(e[i]-f[i]))}\n"
          "   add(nm+' fast path vs exact series, 10 epochs across \\u22124000\\u2026+8000, max |\\u0394|',mf,3e-11,'au','Epochs from JD 260100 (\\u22124000) to JD 4642000 (+7999); the exact series has more rounding noise far from J2000 (arguments grow with |T|)')}\n"
          "  {let mf=0;for(const r of ct){let f;for(let c=0;c<4;c++)f=VSP.fast(k,r[0]);for(let i=0;i<3;i++)mf=Math.max(mf,Math.abs(f[i]-r[10+i]))}\n"
          "   add(nm+' fast path (Chebyshev blocks) X,Y,Z in ICRS vs VSOP2013.ctl, 11 epochs 1890\\u20132000, max |\\u0394|',mf,1e-10,'au','Same reference and tolerance as the exact series (ctl printed to 10 decimals, rounding 5e-11); blocks are built from the 4th call on each epoch')}}\n return A};"))


# 9. teks "Models and data" di dalam aplikasi: referensi [4], baris Planets di panel akurasi, kartu PLANETS, catatan audit
R.append(("(VSOP2013, files VSOP2013p3 for the Sun and VSOP2013p2 for Venus, ftp.imcce.fr/pub/ephem/planets/vsop2013)",
          "(VSOP2013, files VSOP2013p3 for the Sun and Earth, VSOP2013p1 for Mercury, p2 for Venus, p4 for Mars, p5 for Jupiter, p6 for Saturn, p7 for Uranus and p8 for Neptune, ftp.imcce.fr/pub/ephem/planets/vsop2013)"))
R.append(("notice (independent cross-check of the Sun; source of the planet positions in the PLANETS tab and SKY VIEW, except Venus when its VSOP2013 file is loaded)",
          "notice (500-2498 CE: independent cross-check of the Sun and of the seven planets; fallback for the planet positions in the PLANETS tab and SKY VIEW within 500-2498 CE when the VSOP2013 file of a planet is not loaded)"))
R.append(("+k('Not modelled here',",
          "+k('Planets (PLANETS tab, SKY VIEW)',!inI?'not computed outside \\u22124000\\u2026+8000':y>=1890&&y<=2000?'VSOP2013 full series, Mercury to Neptune (needs the .bin files; IPS2000 fallback only within 500\\u20132498 CE): heliocentric longitude vs INPOP10a, authors, 1890\\u20132000: Mercury 0.06, Venus 0.02, Mars 0.93, Jupiter 0.20, Saturn 0.24, Uranus 2.19, Neptune 0.38 mas':'VSOP2013 full series, Mercury to Neptune (needs the .bin files; IPS2000 fallback only within 500\\u20132498 CE): heliocentric longitude vs INPOP10a, authors, \\u22124000\\u2026+8000: Mercury 0.20, Venus 0.15, Mars 1.74, Jupiter 4.47, Saturn 11.73, Uranus 2.45, Neptune 1.27\\u2033; largest far from 1890\\u20132000'+(jd>=1903670.5&&jd<=2633670.5?'':' (no independent series outside 500\\u20132498 CE)'))+k('Not modelled here',"))
R.append(("planets without a loaded file keep the IPS2000 series. Full series",
          "planets without a loaded file keep the IPS2000 series (only within 500-2498 CE; outside it all seven files are required, range -4000..+8000). Full series"))
R.append(("from the full IPS2000 series (Mercury, Venus, Mars, Jupiter, Saturn, Uranus and Neptune: the full VSOP2013 series once vsop2013_mercury.bin, vsop2013_venus.bin, vsop2013_mars.bin, vsop2013_jupiter.bin, vsop2013_saturn.bin, vsop2013_uranus.bin and vsop2013_neptune.bin are loaded) with light-time and aberration.",
          "from the full VSOP2013 series (Mercury, Venus, Mars, Jupiter, Saturn, Uranus and Neptune, -4000 to +8000, once vsop2013_mercury.bin, vsop2013_venus.bin, vsop2013_mars.bin, vsop2013_jupiter.bin, vsop2013_saturn.bin, vsop2013_uranus.bin and vsop2013_neptune.bin are loaded; within 500-2498 CE the full IPS2000 series is used for a planet whose file is not loaded) with light-time and aberration."))
R.append(("IPS2000 notice.txt (EMB cross-check and the planet series of the PLANETS tab)",
          "IPS2000 notice.txt (500-2498 CE: EMB cross-check and independent planet series)"))

for a, b in R:
    c = s.count(a)
    if c != 1:
        sys.exit('JANGKAR cocok %d kali (harus 1): %r' % (c, a[:80]))
for a, b in R:
    s = s.replace(a, b)
open(dst, 'w', encoding='utf-8', newline='').write(s)
n1 = len(s.encode('utf-8'))
print('ukuran', n0, '->', n1, '(+%d); sisa di bawah 25 MiB: %d' % (n1 - n0, 26214400 - n1))
