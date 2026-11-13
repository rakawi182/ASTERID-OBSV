# Changelog

Format mengikuti [Keep a Changelog](https://keepachangelog.com/id-ID/1.1.0/).

## [Atmospheric pressure loading global] — 2026-11-13
### Ditambahkan
- **`apl_rp_1.bin`** (0,8 MiB): grid global atmospheric pressure loading (radial) dari model pasang surut atmosfer Ray & Ponte (2003; koefisien harmonik bola tekanan dalam mbar untuk P1, S1, K1, T2, S2, R2, derajat/orde 10, S1 sampai 20) dan load Love number Gegout (h′ₙ). Sel 1° × 1°, 6 gelombang × (C, S) = 12 kolom (resolusi 10⁻⁸ m, int16 delta sepanjang bujur, basis int32 per baris, deflate; format seperti `opole_0p5.bin`: fetch, pemilih berkas, atau tertanam di `ASTERID_full.html` sebagai `window.__APL_B64`).
- Metode: p = Σ P̄ₗₘ [C⁺ cos(χ + mλ − ε⁺) + C⁻ cos(χ − mλ − ε⁻)] dengan fase Condon–Shortley (−1)ᵐ, lalu uᵣ = (3/ρE) Σ h′ₙ/(2n+1) · pₙ/g (ρE = 5517 kg/m³, g = 9,80665 m/s²). Konvensi (arah ±m, fase Condon–Shortley, tanda ε) ditentukan dengan mencocokkan konstanta stasiun yang sudah tertanam; hanya kombinasi ini yang memberi fase koheren pada keenam gelombang.
- **`apGrid(lat,lon)`**: interpolasi bilinear C dan S di lokasi HUD, hasilnya berbentuk sama dengan `OD.apls`; **`aplRad(mjd, A)`** menerima himpunan koefisien opsional (tanpa argumen tetap konstanta stasiun, selisih 0).
- Uji (`tools/test_apl_bin.py`, `tools/test_apl_bin.js`): decoder dan `apGrid` terhadap interpolasi float64 pada 500 titik acak: 4,8×10⁻⁹ m (kuantisasi); amplitudo maksimum global S2 1,36 mm, S1 0,66 mm; seluruh `<script>` di `ASTERID.html` terkompilasi.
- `tools/`: `build_apl_bin.py`, `test_apl_bin.py`, `test_apl_bin.js`, `patch_asterid_apl.py`.
### Diubah
- Tab PLANETS di lokasi HUD selain stasiun kini menerapkan atmospheric pressure loading dari grid global; banner menyebutkannya, atau menyatakan bahwa berkas belum termuat (tombol **LOAD apl_rp_1.bin**). Di stasiun tidak berubah (konstanta stasiun). Tanpa berkas, hasil sama seperti sebelumnya. Teks bantuan dan komentar `compute()` disesuaikan; ESMGFZ tetap hanya di stasiun.
- Keterbatasan: grid dibatasi derajat 10 (S1: 20) dan hanya komponen radial (seperti rantai stasiun). Di Jolotundo grid terhadap konstanta stasiun: selisih maksimum C, S 0,086 mm; deret per jam 30 hari rms 0,071 mm, maksimum 0,139 mm (amplitudo S2 grid 0,95 kali konstanta stasiun, S1 sekitar 0,4 kali). Asal selisih ini belum dijelaskan (perlakuan laut/inverted barometer atau derajat 1 pada konstanta stasiun belum dapat dipastikan). Selisih 1 mm menggeser posisi topocentric Bulan sekitar 0,5 µas, jadi 0,14 mm sekitar 0,07 µas.
- Ukuran `ASTERID.html` 24,69 MiB.

## [Ocean tide loading global] — 2026-11-13
### Ditambahkan
- **`otl_fes2014b_1.bin`** (1,5 MiB): grid global ocean tide loading dari koefisien harmonik bola FES2014b.v1 (derajat/orde 100, tinggi air; delivery 7 Desember 2019 di grace.obs-mip.fr, memuat koreksi Doodson Sa 056.555 dan S1 164.555) dan load Love number Gegout. Untuk 11 gelombang utama (M2, S2, N2, K2, K1, O1, P1, Q1, Mf, Mm, Ssa) tersimpan amplitudo dan fase gaya BLQ komponen radial, barat, dan selatan per sel 1° × 1° (66 kolom Re/Im, resolusi 0,01 mm, int16 delta sepanjang bujur, deflate; format seperti `gpt3_1.bin`: fetch, pemilih berkas, atau tertanam di `ASTERID_full.html` sebagai `window.__OTL_B64`). Varian 0,5° (3,8 MiB) dibuat dengan `build_otl_bin.py 0.5`.
- **`otGrid(lat,lon)`**: interpolasi bilinear bagian nyata dan imajiner, mengembalikan struktur yang sama dengan `OD.blq`; `otlDisp(mjdTT,dT,B)` menerima BLQ lokasi sebagai argumen ketiga, sehingga admittance 342 gelombang dan modulasi nodal yang dipakai stasiun berlaku di mana pun.
- Metode: IERS Conventions 2010 §6.3.1 dan §7.1.2 (Farrell 1972): ρw = 1025, ρE = 5517 kg/m³, h′ₙ dan l′ₙ dari berkas Gegout. Derajat 1 (nol di berkas itu) diisi h′₁ = −0,290 dan l′₁ = 0,113 (nilai literatur frame CE, bukan dari berkas; dapat diubah di `H1, L1`). χ efektif sama dengan bias HARDISP (0°, 90°, 180°); daftar χ pada `Explanations_about_FES2014b.pdf` membuat Q1, O1, P1, Mf, Mm, dan Ssa meleset 180° terhadap BLQ stasiun.
- Uji (`tools/test_otl_bin.py`, Node.js dan NumPy): decoder terhadap interpolasi float64 grid yang sama pada 706 titik: 6,6×10⁻⁶ m (kuantisasi); grid 1° terhadap sintesis langsung SH: maksimum 0,81 mm global dan 1,24 mm di Indonesia (grid 0,5°: 0,16 dan 0,27 mm); di Jolotundo terhadap BLQ stasiun (33 nilai) rms 0,19 mm, maksimum 0,65 mm (K1 radial); deret per jam selama 2026 radial selisih maksimum 2,3 mm (rms 0,8 mm) dari sinyal maksimum 45,7 mm. Di Onsala M2 radial 3,63 mm (contoh BLQ IERS TN36, model CSR4.0: 3,52 mm). Jalur stasiun tidak berubah (selisih 0 terhadap versi sebelumnya).
- `tools/`: `build_otl_bin.py`, `test_otl_bin.py`, `otl_decoder.js`; `build_full.py` kini menanam ketiga grid; `sw.js` ikut menyimpan `otl_fes2014b_1.bin`.
### Diubah
- Tab PLANETS di lokasi HUD selain stasiun kini menerapkan ocean tide loading dari grid global; banner menyebutkannya, atau menyatakan bahwa berkas belum termuat (tombol **LOAD otl_fes2014b_1.bin**). Di stasiun tidak berubah (BLQ stasiun). Tanpa berkas, hasil sama seperti sebelumnya.
- Keterbatasan: SH derajat 100 menghaluskan beban sekitar 200 km, sehingga dalam beberapa ratus km dari pantai selisih terhadap model lokal dapat mencapai beberapa persen amplitudo (di Jolotundo sekitar 4–5%). Selisih 1 mm menggeser posisi topocentric Bulan sekitar 0,5 µas.
- Ukuran `ASTERID.html` 24,68 MiB.

## [Ocean pole tide loading global] — 2026-11-13
### Ditambahkan
- **`opole_0p5.bin`** (2,0 MiB): koefisien ocean pole tide loading global Desai (2002), frame CM, grid 0,5° × 0,5° (259.200 sel; Re/Im dari u_radial, u_north, u_east) dari `opoleloadcoefcmcor.npz`. Disimpan tanpa galat pada resolusi 10⁻⁶ aslinya (int16 delta sepanjang bujur, basis int32 per baris, deflate). Format dan pemuatan seperti `gpt3_1.bin` (fetch, pemilih berkas, atau tertanam di `ASTERID_full.html` sebagai `window.__OPOLE_B64`).
- **`opGrid(m1,m2,lat,lon)`**: interpolasi bilinear enam koefisien di lokasi HUD (bujur melingkar, lintang dijepit di ±89,75°), lalu rumus yang sama dengan `optDisp` (IERS Conventions 2010 §7.1.5, γ₂ = 0,687 + 0,0036i, K = 5339,4 m/rad).
- Uji: di titik grid uji IERS/Desai (−43,75°, 232,25°; 731 hari `opoleloadcmcor.txt`) selisih maksimum 7,9×10⁻¹⁰ m (radial), 7,0×10⁻¹¹ m (utara), 1,4×10⁻¹¹ m (timur); decoder terhadap interpolasi float64 `.npz` pada 506 titik: 2,4×10⁻¹⁸ m; di stasiun grid dan sel tertanam sama sampai 10⁻¹⁹ m.
- `tools/`: `build_opole_bin.py`, `test_opole_bin.py`; `build_full.py` kini menanam kedua grid; `sw.js` ikut menyimpan `opole_0p5.bin`.
### Diubah
- Tab PLANETS di lokasi HUD selain stasiun (di dalam maupun di luar area DEM/XGM) kini menerapkan ocean pole tide loading dari grid global; banner menyebutkannya, atau menyatakan bahwa berkas belum termuat (dengan tombol **LOAD opole_0p5.bin**). Di stasiun tidak berubah (sel tertanam). Tanpa berkas, hasil sama seperti sebelumnya.
- Ukuran `ASTERID.html` 24,68 MiB.
### Diperbaiki
- **`meanPole()` (IERS 2010, pers. 7.25 dan Tabel 7.7)**: koefisien kuadrat dan kubik x̄ₚ sebelum 2010,0 salah (−0,62872 dan +0,03; seharusnya +0,18413 dan +0,007024), dan model linear setelah 2010,0 memakai (t − 2010) padahal Tabel 7.7 memakai t − 2000,0 untuk kedua bagian. Akibatnya x̄ₚ meleset sekitar 76 mas dan ȳₚ sekitar 6 mas pada November 2026 (x̄ₚ = 228,1 mas, ȳₚ = 342,0 mas yang benar), dan m₁, m₂ ikut meleset. Dampak: pole tide padat dan ocean pole tide di semua lokasi, sekitar 0,2 mm radial dan 0,2 mm utara di Jolotundo (dihitung dengan eq. 7.26 di lokasi; maksimum radial global sekitar 2,5 mm). Diperiksa terhadap `annual.pole` IERS (35 titik, 1976–2010): selisih maksimum x̄ₚ 2,1 mas (rms 0,71) dan ȳₚ 0,27 mas (rms 0,14); kode lama menyimpang sampai 788 mas pada x̄ₚ. Kini kontinu di 2010,0 (99,654 / 352,605 mas) dengan turunan yang sama (7,614 dan −0,629 mas/tahun).
### Ditambahkan (audit)
- **3 baris di Ephemeris Audit** (grup Topocentric corrections; total kini 240 pemeriksaan): `meanPole()` terhadap nilai tahunan `annual.pole` IERS (35 titik 1976–2010; selisih 2,107 mas, batas 5 mas), kontinuitas posisi di 2010,0 (0,001 mas, batas 0,005 mas), dan kontinuitas kemiringan di 2010,0 (1,1×10⁻⁴ mas/tahun, batas 5×10⁻⁴). Dengan `meanPole()` lama ketiganya gagal (788 mas, 17,8 mas, 9,4 mas/tahun), sehingga kesalahan itu kini tertangkap audit.
### Catatan
- Besarnya: untuk m₁, m₂ ≈ 0,1–0,2″, maksimum global sekitar 1,1 mm (vertikal) dan 0,3 mm (horizontal); efeknya pada alt/az Matahari, Bulan, dan planet jauh di bawah 10⁻⁶″.

## [Koreksi DEM dan XGM di luar radius 4,5 km] — 2026-11-13
### Diubah
- **Gerbang deflection of the vertical**: lingkaran `NEAR_KM` = 4,5 km diganti `siteNear()`, sebuah kotak: jarak ke tepi DEM ≥ `DEM_MARGIN_KM` (6 km) dan lokasi berada di dalam empat sel GPT3 tertanam (lintang ≤ −7,5°). Lingkaran 4,5 km lama termuat seluruhnya; jangkauannya sekitar 12 km ke utara, 7 km ke timur dan barat, 4,7 km ke selatan dari stasiun (selatan dibatasi tepi DEM, yang tidak berpusat di stasiun). Di dalam area itu XGM2019e dan RTM (prisma dan tesseroid) dihitung di lokasi HUD.
- Titik uji −7.521951, 112.566089 (10,26 km NNW stasiun, 10,0 km dari tepi utara DEM) kini tercakup: ξ −7,07″, η −1,32″ (XGM2019e −6,84″ / −1,48″ + RTM −0,23″ / +0,16″), h = 55,8 m.
- **ECMWF IFS HRES per koordinat**: lokasi HUD di dalam area DEM dan XGM kini mengambil data ECMWF sendiri (`ecSiteEnsure`; koordinat dibulatkan ke 0,01°, sel IFS 0,1°, 14 variabel dan jendela tanggal sama dengan stasiun, satu permintaan per jam UTC). `ecUrl` dan `ecFetch` menerima lokasi (tanpa argumen tetap stasiun, string URL identik); p, T, e direduksi dari elevasi pada respons ke tinggi lokasi oleh `ecParse` yang sama. Disimpan di memori untuk 6 lokasi dan di `localStorage` (`ecmwf_site_*`, 4 lokasi, 6 jam); saklar ECMWF berlaku untuk semua lokasi. Jika permintaan gagal, meteorology dari empat sel GPT3 tertanam dan banner menyebut galatnya; percobaan ulang paling cepat setelah 60 detik.
- Bobot bilinear GPT3 dihitung per lokasi (`g3Frac`, `gpt3S`) dan tidak lagi memakai bobot stasiun; di stasiun hasilnya identik.
- Banner dan teks bantuan tab PLANETS serta TOPOCENTRIC diperbarui (area DEM/XGM, bukan radius).
### Ditambahkan
- Tiga baris audit TOPOCENTRIC (string URL permintaan ECMWF untuk lokasi, dan dua baris berikut): titik uji terhadap run Python (numpy: XGM2019e bilinear dan prisma planar pada DEM yang sama; selisih maksimum 5×10⁻⁵″, toleransi 2×10⁻³″) dan gerbang `siteNear` (titik di dalam dan di luar, ECMWF hanya ≤ 4,5 km, bobot GPT3 di stasiun). Audit TOPOCENTRIC 69/69 lolos di Chromium headless; alur ECMWF per lokasi (permintaan, cache, kegagalan, stasiun tidak terganggu) diuji dengan `fetch` tiruan karena jaringan tidak tersedia, jadi belum dengan respons Open-Meteo sungguhan.
### Belum dikerjakan
- ECMWF live untuk lokasi di luar area DEM dan XGM: tinggi lokasi di sana hanya dari orografi model GPT3, sehingga reduksi tekanan kurang andal.
- Lokasi di utara 7,5° LS membutuhkan sel GPT3 baris berikutnya (grid global) agar gerbangnya bisa diperluas.
- Nilai di lokasi selain stasiun tidak punya referensi independen untuk kebenaran absolut; audit memeriksa konsistensi dan kecocokan dengan perhitungan Python.

## [GPT3 global untuk refraction di luar stasiun] — 2026-11-13
### Ditambahkan
- **`gpt3_1.bin`** (1,8 MiB): grid GPT3 global 1° × 1° (64.800 sel; `undu`, `Hs`, `p`, `T`, `Q`, `dT`, `la`, `a_h`, `a_w`) dari `gpt3_1.npz`. Semua kolom disimpan tanpa galat pada resolusi desimal aslinya (int16, delta sepanjang bujur, deflate, CRC32); hanya `Hs` dibulatkan 0,1 m (selisih tekanan ≤ 0,006 hPa). Dimuat dengan `fetch` saat lokasi HUD berada di luar stasiun; dapat dipilih manual lewat tombol **LOAD gpt3_1.bin** bila `fetch` tidak mungkin (`file://`).
- **Refraction di tab PLANETS di luar stasiun** kini memakai integral refraction yang sama dengan tab TOPOCENTRIC dengan p dan e dari GPT3 di lokasi HUD (tinggi orografi model), ditambah gradien APG di bawah 15°. Tanpa `gpt3_1.bin`, tetap standard refraction dan banner menyatakannya.
- `tools/`: `build_gpt3_bin.py` (membuat `gpt3_1.bin`), `build_full.py` (membuat `ASTERID_full.html` untuk Releases, grid tertanam), `test_gpt3_bin.py` (decoder terhadap `.npz`: 408 lokasi, selisih maksimum 0,0055 hPa untuk tekanan dan 0,00024 K untuk suhu, hanya dari pembulatan `Hs`).
- `sw.js` ikut menyimpan `gpt3_1.bin` di cache.

### Diubah
- **`compute(R,E,site)`**: tanpa argumen `site` tetap stasiun (keluaran identik); dengan `{lat,lon,h}` rantai TOPOCENTRIC berjalan di lokasi mana pun tanpa data khusus stasiun (loading, ocean pole tide, deflection of the vertical, cuaca langsung). Tab PLANETS di luar stasiun kini memakai jalur ini, sehingga solid tide, pole tide, polar motion, diurnal aberration, dan VMF3 ikut diterapkan; `hudAltAz` dihapus. Baris audit 'Planets (HUD location)' kini membandingkan `compute()` di lokasi bebas yang diletakkan di stasiun dengan rantai stasiun (batas: sudut yang dibentuk perpindahan khusus stasiun, toleransi 1 µas). Audit 231/231 lolos di Chromium headless.
- **Deflection of the vertical dalam radius 4,5 km**: di lokasi HUD 1–4,5 km dari stasiun, `siteDefl()` menghitung XGM2019e di lokasi itu ditambah RTM (prisma dan tesseroid) dari DEM dengan lokasi sebagai pengamat; `rtmCompute`, `rtmTess`, dan `tessObs` menerima lokasi (bawaan: stasiun). Tinggi lokasi = tinggi stasiun + selisih DEM, meteorology dari empat sel GPT3 tertanam. Hasil di-cache per lokasi (4 desimal) dan dihitung lewat `setTimeout` (±2 detik); banner menampilkan ξ/η XGM, RTM, dan total. Di luar 4,5 km tidak diterapkan karena DEM dan XGM hanya mencakup sekitar stasiun. **ECMWF live dalam radius yang sama**: `ecSel()` menerima tinggi elipsoid target dan `ecParse()` mereduksi p, T, e dari tinggi model ke tinggi lokasi (sama seperti di stasiun); data tetap diambil di stasiun, karena sel IFS HRES 0,1° mencakup radius 4,5 km. Tab PLANETS kini memanggil `ecEnsure` di stasiun dan dalam radius itu (sebelumnya hanya tab TOPOCENTRIC yang memuat data), dan banner menyebut sumber meteorology. Audit 234/234 (baris baru: reduksi tinggi seleksi ECMWF untuk lokasi dekat). Audit deflection: `siteDeflCalc()` di stasiun sama dengan `DEFL` (jalur kode yang sama; nilai di lokasi lain tidak punya referensi independen).
- Teks bantuan TOPOCENTRIC diperbarui (OTL/APL tidak lagi 'tidak dimodelkan' secara umum, melainkan khusus stasiun).
- `gpt3()` dipecah menjadi `gpt3c()` (inti, menerima empat sel) dan pembungkus yang memakai empat sel tertanam di stasiun; keluaran di stasiun identik dan audit tidak berubah.
- Alasan tidak ditanam: berkas satu-satunya akan melewati batas unggah browser GitHub 25 MiB.

### Belum dikerjakan
- Deflection of the vertical di luar radius 4,5 km dari stasiun tidak diterapkan (DEM dan XGM hanya mencakup sekitar stasiun).

## [Planet dan audit planet] — 2026-11-12
### Ditambahkan
- **Tab PLANETS**: Merkurius sampai Neptunus dari deret IPS2000 penuh (Chapront & Francou 2002; 500–2498 M, 35.432 suku, tanpa pemotongan) dengan tunda cahaya, aberasi, dan kerangka presesi–nutasi yang sama dengan Matahari dan Bulan. Tiap planet menampilkan RA/Dek, λ/β tanggal, jarak ke Bumi dan Matahari, tinggi/azimut tampak lewat rantai tab TOPOCENTRIC, elongasi, sudut fase dan bagian tersinari, diameter sudut, magnitudo (Mallama & Hilton 2018), arah gerak, serta terbit, kulminasi, dan terbenam berikutnya. Ketuk planet untuk membukanya di SKY VIEW.
- **Planet di SKY VIEW**: tombol PLANETS menggambar Merkurius sampai Neptunus dengan paralaks toposentris dan magnitudo; planet dapat diketuk untuk detail.
- **Audit planet di Ephemeris Audit** (12 baris; total 231 pemeriksaan): posisi heliosentris tujuh planet pada 11 epoch 500–2498 M terhadap nilai uji `notice.txt` IPS2000 (toleransi 2×10⁻¹⁰ au, dari pembulatan nilai acuan 10 desimal), dan saat serta separasi minimum geosentris transit Merkurius 11 November 2019 dan Venus 6 Juni 2012 terhadap Espenak (RASC Observer's Handbook 2019 dan 2012), serta konsistensi rumus alt/az lokasi bebas dengan rantai TOPOCENTRIC di stasiun (0,3″, batas 1″).

### Diubah
- IPS2000 kini juga menjadi sumber posisi planet (sebelumnya hanya pembanding independen EMB di audit). Keterangan audit dan rujukan [4] di dalam aplikasi, README, dan `CITATIONS.md` disesuaikan.
- Tab PLANETS di lokasi HUD selain stasiun TOPOCENTRIC kini menampilkan alt/az geometric topocentric dari lokasi HUD dengan standard refraction dan label yang jelas (sebelumnya alt/az apparent selalu untuk Jolotundo walau rise/transit/set memakai lokasi HUD).
- Ukuran berkas 24,7 MiB.

### Diperbaiki
- Deret IPS2000 kini disimpan float64 penuh persis seperti berkas `ips2000.*` (sebelumnya amplitudo int32 per planet dan fase uint32, yang menyimpang sampai 3,1×10⁻⁷ au dari nilai uji `notice.txt` untuk Uranus). Kini selisihnya paling besar 7×10⁻¹¹ au di semua planet; hasil perhitungan planet berubah sampai ukuran selisih itu.

### Keterbatasan yang diketahui
- Rantai TOPOCENTRIC (DEM/RTM, grid ESMGFZ, GPT3, cuaca ECMWF) terkunci di satu stasiun, Jolotundo. Tab PLANETS memakainya hanya bila lokasi HUD dalam 1 km dari stasiun; di lokasi lain alt/az geometric topocentric dengan standard refraction, dan kartu menyatakannya.
- Magnitudo, diameter sudut, serta terbit, kulminasi, dan terbenam planet belum punya vektor uji di audit.

## [B−V diperiksa silang, atlas rasi, dan heliacal] — 2026-11-11
### Ditambahkan
- **Tab SKY VIEW**: langit dalam bingkai horizon (stereografik) yang mengikuti gyroscope HP atau geseran jari, cubit untuk zoom, ketuk bintang untuk detail. Bintang Hipparcos berwarna dari B−V dengan tempat tampak dari `SM.starApp`, garis rasi, Matahari, Bulan dengan fase dan paralaks toposentris, dan bayangan umbra/penumbra gerhana bulan (radius Bumi diperbesar 1%; menghasilkan U 1,151 dan P 2,184 untuk gerhana 3 Maret 2026, sama dengan katalog NASA). Ekuator langit (tanda jam RA dan kutub NCP/SCP) dan ekliptika epos tanggal (tanda longitudo) dapat dinyalakan. Tombol waktu meneruskan ke jam global; model langit siang opsional, dengan bintang dan garis rasi redup yang dapat dinyalakan terpisah; mode kamera (AR) opsional. Planet belum digambar.
- **Tipe spektrum** untuk 8.868 bintang: 8.494 dari Bright Star Catalogue (CDS V/50) dan supplemennya (CDS V/36), dan 374 sisanya dari Hipparcos Main Catalogue (CDS I/239, kolom SpType), untuk bintang yang tidak punya tipe dari Vol. 11. Tampil di daftar dan di kartu bintang, dengan label sumber.
- **Pemeriksaan silang V** terhadap GCPD (≥ 3 pengamatan), BSC, dan Ducati. Untuk 87 bintang yang bukan variabel periodik atau tak terpecahkan (flag H52 bukan P/U), bila minimal dua kompilasi sepakat dalam 0,03 mag dan berbeda lebih dari 0,05 mag dari V Hipparcos, V yang dipakai adalah rata-rata kompilasi (kalkulator heliacal, magnitudo absolut, atlas, penggaris V); nilai Hipparcos tetap tampil di label. Bintang variabel tetap memakai V median Hipparcos 1989–93.
- **Kode sumber V** (kolom H7 Hipparcos Main Catalogue: G = fotometri multiwarna darat, H = turunan dari Hp + warna + kelas luminositas, T = fotometri Tycho; 2.360, 6.414, dan 96 bintang) pada baris V baru di blok Photometry kartu bintang. Menurut SP-1200 Vol. 1 §2.1, V turunan punya galat sistematis sekitar 0,01 mag (bintang G/K) hingga 0,03–0,08 mag (bintang terpaut pemerahan, superraksasa, ganda).
- **Kode sumber B−V** (kolom H39 Hipparcos Main Catalogue, ESA SP-1200 Vol. 1 §2.1: G = pengamatan darat, T = hasil transformasi BT−VT Tycho) di label B−V pada kartu bintang. Pada pemeriksaan silang, nilai T menyimpang lebih dari 0,05 mag dari kompilasi pada 6,8% kasus, nilai G pada 1,0%.
- **Pemeriksaan silang B−V** terhadap GCPD (Mermilliod, CDS II/168), BSC (V/50, V/36), dan Ducati 2002 (CDS II/237). Untuk 218 bintang yang nilai Hipparcos-nya menyimpang lebih dari 0,05 mag dari konsensus minimal dua kompilasi (selisih antar kompilasi ≤ 0,03 mag), kartu menampilkan rata-rata kompilasi dan menyimpan nilai Hipparcos di label sumber.
- **Atlas rasi** di tab STAR CATALOG: peta stereografik per rasi dengan batas IAU (Delporte 1930, tabel Roman 1987, CDS VI/42), garis figur, dan overlay Almagest (identifikasi Verbunt & van Gent 2012; detail kartu dari Jaschek 1987, CDS V/61).
- **Kalkulator heliacal rising/setting** di kartu bintang, memakai model visibilitas Schaefer (1993, *Vistas in Astronomy* 36, 311–361); kelembapan relatif dapat disalin dari panel cuaca.
- Baris χ² percepatan (HGCA) di kartu bintang.

### Diubah
- Astrometri bintang: posisi epos J1991.25 dari reduksi baru Hipparcos (van Leeuwen 2007, CDS I/311). Untuk 8.429 bintang, gerak diri adalah nilai jangka panjang Hipparcos–Gaia dan paralaksnya dari Gaia EDR3 (HGCA, Brandt 2021). Kecepatan radial: Hipparcos Vol. 1 Tabel 1.2.3 (21 bintang), lalu Gaia DR2 via HGCA (σ ≤ 5 km/s), selebihnya 0.
- Data bintang variabel dilengkapi GCVS 5.1 (Samus dkk. 2017) untuk 1.269 bintang.
- Kode tab STAR CATALOG, katalog gerhana, tabel `D`, dan deret ELP disimpan terkompresi lossless. Hasil perhitungan dan tampilan identik; ukuran berkas 23,6 MiB.

## [Rasi dan kartu bintang] — 2026-10-31
### Ditambahkan
- Rasi IAU untuk semua 8.870 bintang (batas Delporte 1930, tabel Roman 1987), tampil sebagai lencana di tiap baris, di kartu detail, dan sebagai baris Constellation di tab LOCATION. Penamaan Bayer/Flamsteed ditulis lengkap (misalnya α Canis Majoris) di bawah judul kartu.
- Pencarian dapat memakai nama atau singkatan rasi.
- Kartu detail bintang bergaya HUD: readout, tab LOCATION/ASTROMETRY/PHOTOMETRY/ALL, chip asal data (derived, estimate, σπ/π), bola langit alt-az 3D dengan jalur harian, terbit/kulminasi/terbenam, posisi Matahari dan Bulan, serta diagram H–R mini.

### Diubah
- Daftar nama bintang diperbaiki (20 entri) dan tabel Watts disimpan terkompresi lossless (ukuran berkas di bawah 25 MiB).

## [Katalog bintang Hipparcos] — 2026-10-30
### Ditambahkan
- Halaman **STAR CATALOG**: 8.870 bintang Hipparcos (ESA SP-1200) dengan V ≤ 6,5, tempat tampak, tinggi/azimut di lokasi dan waktu HUD, B−V, multiplisitas, dan data variabilitas (Vol. 11). Pencarian, urutan MAG/HIP/ALT/RA, filter HUD stars, above horizon, dan multiple.
- Bar progres saat hitungan tempat tampak berjalan.

### Diubah
- Sumber katalog bintang kini dinyatakan: Hipparcos (ESA SP-1200, 1997). Rujukan [11] di aplikasi dan `CITATIONS.md` diperbarui; catatan "sumber tidak dinyatakan" dihapus.
- Daftar 80 bintang HUD dan appulse memakai posisi, gerak diri, dan paralaks Hipparcos.
- Ukuran berkas sekitar 25 MB.

### Diperbaiki
- Ganti urutan atau filter di STAR CATALOG jauh lebih cepat: hasil hitungan disimpan 60 detik, hitungan dibagi bertahap, dan tombol tidak lagi tertahan jeda sentuhan.

## [Rilis publik pertama] — 2026-10-28
### Ditambahkan
- Aplikasi `ASTERID.html` (satu berkas) dan pembaru data `update_asterid_data.py` (seri EOP IERS dan grid pemuatan ESMGFZ).
- **PWA**: dapat dipasang di layar utama dan berjalan offline (`manifest.webmanifest`, `sw.js`, `index.html`), beserta logo dan set ikon.
- Dokumentasi: README, LICENSE (MIT), CITATION.cff, CITATIONS.md.
