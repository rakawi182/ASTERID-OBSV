# Sitasi dan sumber

Daftar pustaka dan sumber data yang mendasari ASTERID. Nomor `[n]` mengikuti halaman **ACCURACY · MODELS · REFERENCES** di dalam aplikasi. Untuk mengutip aplikasi ini, lihat [`CITATION.cff`](CITATION.cff).

## Model dan data (dari halaman referensi aplikasi)

1. Chapront J., Francou G., 2003, A&A 404, 735. Teori Bulan ELP/MPP02 (seri, konstanta, nilai uji).
2. Chapront J., Chapront-Touzé M., Francou G., 2002, A&A 387, 700 (penentuan parameter Bulan dari LLR, dasar fit LLR); Chapront J., Chapront-Touzé M., Francou G., 1999, A&A 343, 624.
3. Chapront-Touzé M., Chapront J., 1988, A&A 190, 342 (ELP 2000-85); 1991, *Lunar Tables and Programs from 4000 B.C. to A.D. 8000*, Willmann-Bell (JANUS 98.12, dipakai di luar |t| = 30 abad).
4. Simon J.-L., Francou G., Fienga A., Manche H., 2013, A&A 557, A49 (VSOP2013, berkas VSOP2013p3, `ftp.imcce.fr/pub/ephem/planets/vsop2013`); Fienga A. dkk., 2011, Celest. Mech. Dyn. Astron. 111, 363 (INPOP10a); Chapront J., Francou G., 2002, *Improved Planetary Solutions IPS2000* (pembanding independen); Standish E.M., 1998, dokumentasi JPL DE405/LE405 dan DE406.
5. Seri libasi Bulan LLIB04, LLIB245/403/405 dan pelengkapnya, polac.obspm.fr (Chapront dkk.); Moons M., 1982, *The Moon and the Planets* 27, 257; Meeus J., 1998, *Astronomical Algorithms* (2nd ed.), bab 53.
6. Petit G., Luzum B. (eds.), 2010, *IERS Conventions (2010)*, IERS Technical Note 36; Capitaine N., Wallace P.T., Chapront J., 2003, A&A 412, 567; Wallace P.T., Capitaine N., 2006, A&A 459, 981; Mathews P.M., Herring T.A., Buffett B.A., 2002, J. Geophys. Res. 107(B4), 2068.
7. IAU SOFA Board, *SOFA Software Collection* (`iauNut06a`, `iauEpv00`, `iauAtci13`, `iauAb`, `iauLd`): kasus uji yang dipakai dalam audit.
8. Stephenson F.R., Morrison L.V., Hohenkerk C.Y., 2016, Measurement of the Earth's rotation: 720 BC to AD 2015, *Proc. R. Soc. A* 472, 20160404. DOI: [10.1098/rspa.2016.0404](https://doi.org/10.1098/rspa.2016.0404), beserta Suplemennya.
9. Espenak F., Meeus J., 2006, NASA/TP-2006-214141; Espenak F., NASA GSFC Eclipse Web Site (keadaan gerhana 2026 sebagai acuan); Urban S.E., Seidelmann P.K. (eds.), 2013, *Explanatory Supplement to the Astronomical Almanac* (3rd ed.).
10. Archinal B.A. dkk., 2011, Celest. Mech. Dyn. Astron. 109, 101 (radius rata-rata Bulan 1737,4 km).
11. Katalog bintang: berkas `star_c.json` yang disertakan dengan proyek (**sumber tidak dinyatakan**); 12 baris dikoreksi dari daftar sebelumnya, 30 baris dibulatkan ke 1′ ditandai `*`.
12. Morrison L.V., Stephenson F.R., Hohenkerk C.Y., Zawilski M., 2021, Addendum 2020 to "Measurement of the Earth's rotation: 720 BC to AD 2015", *Proc. R. Soc. A* 477, 20200776. DOI: [10.1098/rspa.2020.0776](https://doi.org/10.1098/rspa.2020.0776); materi elektronik: DOI [10.6084/m9.figshare.c.5300925](https://doi.org/10.6084/m9.figshare.c.5300925). ΔT = TT−UT1 untuk −720…+1810 dari spline Tabel S15.
13. HM Nautical Almanac Office, UK Hydrographic Office, *Historical values of ΔT and LOD*, <http://astro.ukho.gov.uk/nao/lvm> (pembanding independen dalam audit).
14. IERS Earth Orientation Centre, seri **EOP 20 C04** (harian, 1962–sekarang); IERS Rapid Service/Prediction Centre, **Bulletin A**; tabel detik kabisat IERS (Bulletin C). <https://hpiers.obspm.fr/eoppc/eop/eopc04/>, <https://datacenter.iers.org/eop.php>.
15. Espenak F., Meeus J., 2006 (rev. 2007), *Five Millennium Canon of Solar Eclipses: −1999 to +3000*, NASA/TP-2006-214141; 2009, *Five Millennium Canon of Lunar Eclipses*, NASA/TP-2009-214172; *Five Millennium Catalog of Solar Eclipses*, NASA/TP-2008-214170, dan *of Lunar Eclipses*, NASA/TP-2009-214173, <http://eclipse.gsfc.nasa.gov/SEcat5/>. Penomoran Saros: van den Bergh G., 1955, *Periodicity and Variation of Solar (and Lunar) Eclipses*, Tjeenk Willink, Haarlem.
16. Meeus J., 1998, *Astronomical Algorithms* (2nd ed.), bab 7 (hari Julian dan tanggal kalender); Urban & Seidelmann, 2013.
17. Williams J.G., Boggs D.H., 2016, Secular tidal changes in lunar orbit and Earth rotation, *Celest. Mech. Dyn. Astron.* 126, 89–129. DOI: [10.1007/s10569-016-9702-3](https://doi.org/10.1007/s10569-016-9702-3) (dikutip oleh [12]; tidak dipakai dalam perhitungan).

## Model lain yang disebut di dalam aplikasi

- Böhm J. dkk., *IERS Conventions 2010*, gradien troposfer asimetris (APG.F), derajat dan orde 9.
- Model troposfer **GPT3** dan fungsi pemetaan **VMF3** dengan tunda zenit Saastamoinen. † Rujukan umum untuk VMF3/GPT3: Landskron D., Böhm J., 2018, *J. Geodesy* 92, 349–360.
- Pemuatan non-pasang **ESMGFZ** (NTAL, NTOL, HYDL, SLEL), GFZ Potsdam.
- Meteorologi waktu nyata: ECMWF IFS HRES melalui API [Open-Meteo](https://open-meteo.com).
- Mosaik fotografis **LROC-WAC** dan model ketinggian **LRO GLD100** (cakram Bulan di halaman MOON FACE). † Rujukan umum: Robinson M.S. dkk., 2010, *Space Sci. Rev.* 150, 81 (LROC); Scholten F. dkk., 2012, *J. Geophys. Res.* 117, E00H17 (GLD100).

† Tidak tercantum di halaman referensi aplikasi; ditambahkan sebagai rujukan umum dan sebaiknya diverifikasi sebelum dipublikasikan.

## Catatan lisensi data pihak ketiga

Kode ASTERID berlisensi MIT, tetapi data dan seri yang tertanam atau dipanggil berasal dari penyedia lain (IMCCE / Observatoire de Paris, IERS, NASA, GFZ Potsdam, ECMWF dan Open-Meteo, serta publikasi ilmiah di atas). Ketentuan penggunaan dan atribusi mengikuti penyedia masing-masing. Katalog bintang `star_c.json` belum punya sumber yang dinyatakan; lengkapi atribusinya sebelum mendistribusikan ulang secara terpisah dari aplikasi.
