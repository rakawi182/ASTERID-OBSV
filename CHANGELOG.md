# Changelog

Format mengikuti [Keep a Changelog](https://keepachangelog.com/id-ID/1.1.0/).

## [ESMGFZ: analisis sampai 2026-11-19, prakiraan 324F sampai 2026-11-29, dan pembaru data yang mengenal prakiraan] — 2026-11-21

### Ditambahkan
- Deret non-tidal loading (NTAL, NTOL, HYDL, SLEL) di stasiun Jolotundo (frame CM) diperpanjang dari `*_2026_pointsubset.csv` (analisis): NTAL dan NTOL sampai 2026-11-19 21:00 (+8 sampel 3-jaman), HYDL dan SLEL sampai 11-19 12:00 (+1 sampel harian). Bagian yang tumpang tindih dengan data tertanam (2026-11-10…18) identik dengan float32 yang tersimpan.
- Disambung dengan prakiraan `*_2026_324F_pointsubset.csv`: NTAL dan NTOL 11-20 00:00 sampai 11-29 21:00 (80 sampel), HYDL dan SLEL 11-20 12:00 sampai 11-29 12:00 (10 sampel). Analisis dan prakiraan bersambung tanpa celah. Kolom `dg` pada HYDL tidak dipakai.
- `NTD` menyimpan `fc` (sampel prakiraan pertama) dan `fb` (sampel analisis terakhir; sama dengan `fc` bila bersambung). `ntlSeries` mengembalikan `src` (0 analisis, 1 jembatan linear bila ada celah, 2 prakiraan). Tanpa `fb`/`fc` perilaku lama tetap.
- `update_asterid_data.py`: opsi `--ntal-fc`, `--ntol-fc`, `--hydl-fc`, `--slel-fc` untuk CSV prakiraan. CSV analisis (`--ntal` dan seterusnya) memperpanjang analisis dan menggantikan sampel prakiraan yang dicakupnya (harus bersambung dengan analisis tertanam). CSV prakiraan menggantikan seluruh bagian prakiraan; sampel sebelum akhir analisis diabaikan, dan celah dijembatani linear. Skrip melaporkan selisih prakiraan lama terhadap analisis baru, memperbarui keterangan di bawah kartu, dan menolak HTML tanpa dukungan prakiraan.

### Diubah
- Kartu NTAL, NTOL, HYDL, SLEL di tab TOPOCENTRIC kini berlabel menurut sumber ("ESMGFZ, interpolated", "ESMGFZ forecast, interpolated", atau "linear bridge over data gap"). "Last value held" baru muncul setelah akhir deret (kini 2026-11-29), sebelumnya setelah 11-18.
- Audit: dua pemeriksaan baru. Nilai 5 epoch di sekitar 2026-11-19 terhadap interpolasi numpy CSV analisis, dan bendera sumber dibaca dari penanda `fb`/`fc` tiap deret (tidak terpaku pada tanggal), sehingga tetap berlaku setelah pembaruan berikutnya. Nilai prakiraan sengaja tidak dipaku di audit karena berganti tiap terbitan; skrip melaporkannya saat memuat.

### Verifikasi
- Di Node: 21 blok skrip lolos `node --check`; pemeriksaan non-tidal lama (2×10⁻⁷ mm) dan dua pemeriksaan baru lolos. Skrip diuji dari data lama dengan kedelapan CSV: hasilnya identik byte demi byte dengan `ASTERID.html` ini. Skenario sintetis: analisis menimpa sebagian prakiraan, prakiraan baru dengan celah (jembatan), analisis melewati akhir prakiraan, pembaruan sebagian deret, CSV dengan celah, dan prakiraan yang berakhir sebelum analisis (dua terakhir ditolak). Audit di Node lolos pada semua hasil. Halaman belum dibuka di browser, sehingga jumlah total audit (297 sebelumnya, kini seharusnya 299) belum dikonfirmasi di halaman.

### Keterbatasan
- Nilai prakiraan bersifat sementara. Pada HYDL dan SLEL, interval 11-19 12:00 sampai 11-20 12:00 menginterpolasi antara sampel analisis terakhir dan sampel prakiraan pertama, tetapi diberi label analisis.
- Bila hanya sebagian deret diperbarui, keterangan di bawah kartu memakai akhir analisis paling awal dan awal prakiraan paling awal.
- Ukuran: `ASTERID.html` 25.999.803 byte (+6.266 byte dari versi unggahan; sisa 214.597 byte di bawah 25 MiB).

## [Panorama dan tinggi 24 jam pindah ke SKY VIEW; suhu pada tinggi target di kartu PLANETS] — 2026-11-19

### Diubah
- Panel SKY PANORAMA · HORIZON dan ALTITUDE · 24 H (WIB) dipindah dari tab HUD ke tab SKY VIEW, tepat di bawah peta langit (`data-p` dari `hud` menjadi `sky`). Isi dan perhitungan panel tidak berubah; panel hanya digambar saat tab SKY VIEW aktif, dan posisinya dikoreksi tiap detik bila panel SKY VIEW baru dibuat sesudahnya (cadangan: di bawah kartu HUD seperti semula).
- Kartu ECMWF di tab PLANETS kini menampilkan Temperature, Dew point, Pressure, dan Relative humidity pada tinggi target (grup "At target height"). Baris itu sebelumnya disembunyikan oleh daftar `sk`; sejak kartu direduksi ke tinggi situs, nilainya berbeda dari grup "At API elevation" (di stasiun: elevasi model 541 m, tinggi target 554,5 m), sehingga tidak lagi berulang.
- `README.md`: baris SKY VIEW menyebut kedua panel.

### Verifikasi
- Logika penempatan diuji dengan DOM minimal di Node: tab HUD tidak menampilkan panel, tab SKY VIEW menampilkan panel peta langit lalu panorama, tab PLANETS tidak menampilkannya. Semua blok skrip lolos `node --check`. Tampilan belum diuji di perangkat.

### Keterbatasan
- Ukuran: `ASTERID.html` 25.991.117 byte (+108 byte dari entri sebelumnya; sisa 223.283 byte di bawah 25 MiB).

## [Laju rotasi sidereal: terbit, transit, dan terbenam planet] — 2026-11-18

### Diubah
- `RATE2` (blok PLANETS), `RATE` (SKY VIEW, `basisAt`) dan `RATE` (jejak sub-titik Matahari dan Bulan di HUD) ditulis `1.00273790935*7.2921159e-5` = 7,3121×10⁻⁵ rad/s. Laju sebenarnya (dGMST/dUT1) adalah 1,00273790935 putaran per hari UT1 = 7,2921159×10⁻⁵ rad/s; angka 7,2921159×10⁻⁵ sudah memuat faktor 1,0027379, jadi faktor itu terhitung dua kali dan laju terlalu besar 0,274 %. Kini `1.00273790935*2*Math.PI/86400` di ketiga tempat.
- `window.__plRate` mengekspos laju yang dipakai iterasi sudut jam planet, hanya untuk audit.

### Dampak
- Next rise, Next transit, dan Next set planet jatuh lebih awal sebesar 0,273 % dari sisa waktu ke peristiwa (sekitar 3 menit untuk peristiwa 19 jam lagi, hingga 4 menit pada 24 jam) dan waktu yang tampil merayap lebih lambat sekitar 10 detik per jam selama jam berjalan, lalu melompat ketika peristiwa lewat. Itu sebabnya angkanya terlihat berubah-ubah.
- Jejak sub-titik HUD (24 jam ke belakang) bergeser sampai sekitar 1° bujur di ujung jejaknya. Di SKY VIEW dampaknya diabaikan karena `gast0` disegarkan tiap `refresh`.
- Rise, set, dan transit Matahari dan Bulan di HUD tidak terpengaruh (memakai `skySmp` dan ephemeris langsung, bukan iterasi laju).

### Ditambahkan
- Baris audit "Planet events": laju rotasi sidereal iterasi sudut jam dibanding 360,98564736629° per hari (selisih relatif 8,0×10⁻¹³, toleransi 10⁻⁹; sebelum perbaikan 2,7×10⁻³).

### Verifikasi
- Iterasi sudut jam yang sama dijalankan di Node untuk bintang tetap (tanpa gerak planet dan tanpa interpolasi, sehingga galat hanya berasal dari laju): transit 19,31 jam lagi lebih awal 189,8 s, 7,31 jam lagi lebih awal 71,8 s; dengan laju benar galatnya 0,000 s. Tampilan lama: 19:15:11, 19:15:21, 19:15:30, 19:15:40 UTC pada jam ke 0, 1, 2, 3 (merayap ±10 s per jam), sedangkan nilai sebenarnya tetap 19:18:20 UTC.
- Semua blok skrip lolos `node --check`.

### Keterbatasan
- Mesin planet lengkap (VSOP2013 atau IPS2000 dengan modul SKY) tidak dapat dijalankan di lingkungan uji ini, sehingga posisi planet sebenarnya dan `plData` tidak diuji ujung ke ujung; yang diuji adalah konstanta dan iterasinya.
- Ukuran: `ASTERID.html` 25.991.009 byte (+466 byte dari entri sebelumnya; sisa 223.391 byte di bawah 25 MiB).

## [SKY NOW: terbit dan terbenam Matahari stabil dan sama dengan HUD] — 2026-11-18

### Diubah
- Waktu terbit dan terbenam Matahari di panel SKY NOW (tab PLANETS) kini diambil dari `SM.evCache()`, sumber yang sama dengan "Next sunrise" dan "Next sunset" di HUD (ephemeris presisi, bisection sampai milidetik, hanya dihitung ulang setelah peristiwa berikutnya lewat). Tinggi Matahari di judul panel dan klasifikasi DAY / TWILIGHT / NIGHT memakai `SM.skySmp` yang sama. `sun24` tetap dipakai untuk pita senja 24 jam dan sebagai cadangan jika HUD tidak tersedia. Nilai terakhir yang valid ditahan sesaat ketika cache HUD belum menyegarkan diri sesudah peristiwa lewat.

### Penyebab
- `sun24` mencuplik tinggi Matahari tiap 5 menit mulai dari "sekarang" tanpa interpolasi dan dihitung ulang tiap menit. Waktu yang tampil adalah peristiwa sebenarnya ditambah 0 sampai 5 menit, naik 1 menit tiap menit lalu melompat mundur (gigi gergaji), dan selalu lebih lambat dari HUD.
- Jendela 24 jam (287 langkah × 5 menit = 1435 menit) lebih pendek dari selang antar-terbit (sekitar 1440 menit), sehingga terbit atau terbenam berikutnya kosong sekitar 5 menit sesudah peristiwa.
- Bukan efek toposentrik: paralaks Matahari 8,8″ (0,0024°) setara kurang dari 1 detik waktu.

### Verifikasi
- Kode `sunAlt` dan `sun24` asli dijalankan di Node (−7,522°, 112,566°, 18 Nov 2026; rumus Matahari yang sama): terbit sebenarnya 05:00:41 WIB, terbenam 17:29:01 WIB. Tampilan lama berada 0,82 sampai 4,92 menit di atas nilai sebenarnya, dengan terbit kosong 5 dari 1440 menit dan terbenam kosong 6 menit.
- Logika baru diuji dengan stub di Node: nilai tetap selama jam berjalan 12 menit, bertahan saat cache HUD belum segar, kembali ke cadangan jika HUD tidak tersedia. Semua blok skrip lolos `node --check`. Belum diuji langsung di perangkat.

### Keterbatasan
- Waktu terbit dan terbenam planet di kartu planet tidak diperiksa dalam perubahan ini.
- Ukuran: `ASTERID.html` 25.990.543 byte (+604 byte dari entri sebelumnya; sisa 223.857 byte di bawah 25 MiB).

## [Tinggi situs HUD dan kartu cuaca PLANETS] — 2026-11-18

### Diubah
- Permintaan ECMWF untuk lokasi HUD selain stasiun kini memakai koordinat dibulatkan ke 0,0001° (sebelumnya 0,01°, sehingga titik bisa bergeser hingga sekitar 0,8 km). Elevasi DEM Open-Meteo kini dibaca di titik situs (situs uji: 23,1 m menjadi 27,0 m). Kunci cache `ecmwf_site_*` berubah; cache lama tidak terpakai lagi.
- Kartu ECMWF di tab PLANETS kini mereduksi p, T, e ke tinggi situs (sama dengan hitungan refraksi); sebelumnya ditampilkan pada elevasi model (Δh = 0). Ditambah baris Model elevation (API DEM) dan Target height.
- Tata letak kartu PLANETS: label dan nilai boleh membungkus, judul grup berlebar penuh, header kartu bisa pindah baris, sehingga tidak ada lagi overflow horizontal di layar sempit. Baris "Interpolated hours · w" menjadi "Model hours (UTC) · weight".
- Teks yang menyebut berkas pembanding diganti menjadi "reference implementation" (label tab TOPOCENTRIC, keterangan kartu, teks self-test, komentar kode).
- Halaman ACCURACY · MODELS · REFERENCES: ditambah rujukan [18] Copernicus DEM GLO-30, [19] XGM2019e, dan [20] George (1960), serta catatan metode tinggi situs dan K-index. `CITATIONS.md` mengikuti penomoran itu; `README.md`: baris HUD menyebut kartu tinggi situs.

### Ditambahkan
- Kartu **SITE HEIGHT · DEM + XGM** di panel OBSERVER: H (DEM 30 m), N (grid XGM2019e), h = H + N, dan h pada rantai TOPOCENTRIC (HELL + DEM(situs) − DEM(stasiun)). Di luar cakupan DEM atau XGM nilai tampil "—" beserta rentang valid. `siteHeights(lat,lon)` diekspor di `ASTERID_TOPO`. Keterangan kartu menyebut bahwa Copernicus GLO-30 adalah model permukaan (kanopi dan bangunan ikut terhitung), jadi H bukan tinggi tanah gundul.
- Kartu ECMWF tab PLANETS dan tab TOPOCENTRIC: **K-index** dihitung dari tingkat tekanan IFS 0,25° (K = (T850 − T500) + Td850 − (T700 − Td700), interpolasi linear dalam waktu), karena IFS HRES 9 km tidak punya tingkat tekanan dan `k_index` bernilai null di kedua model (dicek langsung pada API: semua null untuk `ecmwf_ifs` dan `ecmwf_ifs025`). Satu request kecil tambahan (`models=ecmwf_ifs025`, lima variabel) berjalan paralel dengan request utama dan disimpan di `raw.__k`, sehingga ikut cache dan jam UTC yang sama. Jika gagal, K-index tidak tampil dan kartu utama tidak terpengaruh.
- Di tab TOPOCENTRIC baris K-index memuat nilai hitungan itu (dengan suku-sukunya), dan baris yang null sepanjang respons (mis. Lightning density) diberi catatan "not provided by IFS HRES". Di tab PLANETS, baris "Not in the IFS HRES output" menyebut variabel opsional yang null sepanjang respons (sekarang `k_index lightning_density`), sehingga "Variables rejected: none" tidak lagi membingungkan. Densitas petir tidak disediakan kedua model dan tidak ditampilkan.
- Self-test baru: K-index (33, 35, 37 pada jam awal, tengah, akhir), nilai null di luar jendela atau dengan input hilang, URL request, dan daftar variabel null.

### Verifikasi
- `siteHeights` diuji di Node dengan kode dan data yang sama: stasiun H 554,509 / N 28,846 / h 583,356 m (rantai 583,355 m); (−7,521951°, 112,566089°) H 27,002 / N 28,872 / h 55,873 m; di luar DEM dan XGM bernilai null.
- Semua blok skrip lolos `node --check`. Jangkar `update_asterid_data.py` (blok EOP dan NTD, teks FCN) identik; `build_full.py` dan `build_asterid_full.py` menghasilkan berkas identik pada uji dengan berkas biner contoh.
- DOI Copernicus DEM (10.5270/ESA-c5d3d65) dan XGM2019e (10.1007/s00190-020-01398-0) dicocokkan dengan sumber daring.
- Fungsi K-index dan self-test barunya dijalankan di Node: 0 pemeriksaan gagal. Pengecekan langsung pada API (di HP): `k_index` dan `lightning_density` null untuk `ecmwf_ifs` dan `ecmwf_ifs025`. Request `models=ecmwf_ifs025` ke `/v1/ecmwf` dengan lima variabel tingkat tekanan dicoba langsung di HP: respons 96 jam per jam, satuan °C, sel 0,25° di −7,5°, 112,5°; `ecKindex` dijalankan pada respons itu (K = 34,4 pada 2026-11-18 00:26 UTC; rentang 26,8–37,3 selama 96 jam).

### Keterbatasan
- Selisih undulasi GPT3 terinterpolasi dan XGM di situs uji 0,41 m (sekitar 0,05 hPa pada target ECMWF); tidak disamakan.
- K-index berlaku untuk sel 0,25° (sekitar 25 km, 3-jam), bukan sel 9 km; nilainya baru ada setelah pengambilan data jam UTC berikutnya (awalan cache dinaikkan ke `ecmwf_cache_m3_`).
- Ukuran: `ASTERID.html` 25.989.939 byte (+9.820 byte; sisa 224.461 byte di bawah 25 MiB).

## [Perbaikan model ΔT] — 2026-11-16
### Diubah
- `dtModel`: spline Addendum 2020 sebelum 1956 (ramp halus ke C01 pada 1950–1956), IERS EOP C01 UT1−TAI untuk 1956–1972, tabel `DTD` dari 1972. `DTD` turun dari 1658 ke 781 node (node sebelum 1970 dan node setengah tahunan yang menyimpang di 1970–2009 dibuang). Hasil untuk y ≤ 1790 dan y ≥ 2027 tidak berubah.
- Teks caption, referensi [12] dan [14], serta batasan disesuaikan.
### Ditambahkan
- Ephemeris Audit, kelompok ΔT: pemeriksaan spline 1820–1950, C01 vs USNO 1956–1972, spline vs USNO per era, tabel 1975–2003, kemulusan 1790–1972, dan kontinuitas sambungan 1956/1972.
### Dihapus
- Baris audit epoch 1904,6 (acuan −6,55 s berasal dari tabel yang bermasalah).
### Verifikasi
- Seluruh audit: 297 pemeriksaan. Terhadap USNO 1956–1972: 0,01 s rms (sebelumnya 0,25 s); terhadap IERS C01 1972–2019: 0,06–0,07 s rms (sebelumnya 1,7–5,5 s).
### Keterbatasan
- Terhadap USNO 1810–1900 selisihnya 2,0–3,5 s rms (model berbeda). Node C01 1956–1972 tertanam, jadi bukan uji independen.
- Ukuran: `ASTERID.html` 25.971.029 byte.

## [Rentang planet −4000…+8000] — 2026-11-15
### Diubah
- **Rentang tab PLANETS dan SKY VIEW diperluas dari 500–2498 CE (rentang IPS2000) ke −4000…+8000** (rentang deret VSOP2013 dan model Bumi; `VSP.JD0/JD1` = JD 260045 / 4643045, sama dengan modul Matahari). Gerbang `plCompute` kini memakai rentang VSOP2013, bukan rentang IPS2000.
- Di dalam 500–2498 CE perilaku tidak berubah: VSOP2013 bila `.bin` termuat, jika tidak IPS2000. **Di luar 500–2498 CE tidak ada cadangan IPS2000**: `plCompute` meminta ketujuh `.bin` (`VSP.want`) dan mengembalikan `null` sampai semuanya siap; tab PLANETS menampilkan status muat per planet dan tombol LOAD bila sebuah berkas gagal diambil (mis. dari `file://`), sedangkan SKY VIEW tidak menggambar planet. Di luar −4000…+8000 tab PLANETS menampilkan pesan rentang.
- Tab PLANETS menampilkan keterangan di luar 500–2498 CE: posisi hanya dari VSOP2013, tanpa deret pembanding independen, beserta galat longitude yang dinyatakan penyusun (Merkurius 0,20″, Venus 0,15″, Mars 1,74″, Jupiter 4,47″, Saturnus 11,73″, Uranus 2,45″, Neptunus 1,27″; README IMCCE, −4000…+8000). Teks status planet dan panel SKY VIEW menyebut bahwa IPS2000 hanya berlaku di 500–2498 CE.
### Ditambahkan
- Ephemeris Audit, grup **VSOP2013 planets**: satu pemeriksaan baru per planet (grup dari 35 menjadi 42, lalu 49 dengan pemeriksaan ctl di bawah): jalur cepat (blok Chebyshev) terhadap deret eksak di 10 epoch dari JD 260100 (−4000) sampai JD 4642000 (+7999), toleransi 3×10⁻¹¹ au; hasil terburuk Merkurius 1,3×10⁻¹¹ au (44 %). Seluruh audit lulus 286 dari 286 di Chromium (279 dengan pemeriksaan rentang saja) (berkas sebelum penambalan: 272 dari 272, hasil terburuk grup tetap 86 %).
- Ephemeris Audit, grup **VSOP2013 planets**: pemeriksaan **jalur cepat terhadap `VSOP2013.ctl`** per planet (X, Y, Z ICRS, 11 epoch 1890–2000, toleransi 10⁻¹⁰ au seperti deret eksak; blok Chebyshev dibentuk dulu dengan 4 panggilan). Hasil 5,0–6,1×10⁻¹¹ au untuk Merkurius sampai Uranus (50–61 %), sama dengan deret eksak. Grup kini 49 pemeriksaan dan seluruh audit 286 dari 286, hasil terburuk grup 88 %.
- Teks "Models and data" di dalam aplikasi diperbarui: referensi [4] menyebut berkas VSOP2013p1…p8 (Matahari/Bumi dan ketujuh planet) dan IPS2000 sebagai pembanding serta cadangan hanya di 500–2498 CE; panel akurasi mendapat baris **Planets (PLANETS tab, SKY VIEW)** (galat longitude yang dinyatakan penyusun: 1890–2000 dalam mas, selain itu −4000…+8000 dalam detik busur, dengan catatan tanpa deret independen di luar 500–2498 CE, dan "not computed" di luar −4000…+8000); keterangan kartu PLANETS dan catatan panel Audit disesuaikan.
- `tools/patch_asterid_range.py`: penambal untuk `ASTERID.html` (setiap penggantian harus cocok tepat 1 kali).
### Verifikasi
- `plCompute` di 15 epoch antara −3990 dan +7990 (dan di 400, 498, 502, 2496, 2500 CE sekitar batas IPS2000): tujuh planet terhitung; arah tampak jalur cepat berbeda dari deret eksak paling besar 1,8 µas. Di 8100 dan −4100 hasilnya `null` (di luar rentang).
- Tampilan tab PLANETS dengan jam halaman digeser ke −3000, 1500, 7000, dan 9000: kartu planet tampil di −3000, 1500, dan 7000 (dengan keterangan rentang di luar 500–2498), pesan rentang di 9000. Jalur gagal (`vsop2013_neptune.bin` dijawab 404): di 1500 CE Neptunus jatuh ke IPS2000, di −3000 CE tab menampilkan pesan, status muat, dan tombol LOAD tanpa kartu.
- Derau pembulatan deret eksak jauh dari J2000: elemen VSOP2013 yang dihitung pembaca JavaScript (double) dibandingkan dengan evaluasi presisi diperluas (longdouble, pembaca Python terpisah dari format `.bin`) di tujuh epoch −4000…+8000 untuk Merkurius dan Neptunus. Selisih terbesar: 7×10⁻¹² rad pada longitude rata-rata Merkurius (≈ 3×10⁻¹² au) dan 2,3×10⁻¹³ au pada sumbu panjang Neptunus; elemen lain ≤ 2×10⁻¹⁵. Jauh di bawah galat teori.
### Keterbatasan
- Di luar 500–2498 CE tidak ada deret independen untuk membandingkan; satu-satunya batas akurasi adalah galat yang dinyatakan penyusun VSOP2013 (terbesar jauh dari jendela pencocokan 1890–2000). Selisih Neptunus terhadap IPS2000 yang belum dijelaskan (lihat entri Neptunus) tidak bisa diteliti di luar 500–2498 CE.
- Ketidakpastian ΔT dan rotasi Bumi pada epoch jauh tidak termasuk angka di atas; ia memengaruhi altitude/azimuth serta rise, transit, dan set.
- Kecepatan di ponsel belum diukur; di Chromium desktop jalur cepat di epoch jauh sama cepatnya dengan epoch modern (blok Chebyshev terbentuk dan lulus pemeriksaan di semua epoch uji).
- Ukuran: `ASTERID.html` 25.975.555 byte (+3.157 byte; sisa 238.845 byte di bawah 25 MiB). `sw.js` tidak menambah berkas data; komentarnya diperbarui.

## [VSOP2013 untuk Neptunus] — 2026-11-15
### Ditambahkan
- **`vsop2013_neptune.bin`** (3,8 MiB): deret VSOP2013 penuh untuk Neptunus (Simon dkk. 2013; berkas IMCCE `VSOP2013p8.dat`, 65 series, 322.572 suku, tanpa truncation; suku gerak rata-rata pada deret l tidak disimpan, sehingga 322.571 suku; 41.375 argumen berbeda). Semua pengali muat di int8 (format `VS13`; berkas planet lain tidak berubah). Terhadap blok Neptunus di `VSOP2013.ctl` (11 epoch 1890–2000) selisih maksimum 8,0×10⁻¹¹ au per komponen XYZ; elemen cocok hingga 4,8×10⁻¹¹ (batas pembulatan acuan 10 desimal; pada jarak 30 au pembulatan XYZ acuan dominan), diperiksa dengan pembaca independen `tools/test_vsop2013_bin.py`.
- Baris LED **VSOP NEP** dan baris status di tab PLANETS untuk Neptunus (daftar planet `AV` menjadi `[0,1,2,3,4,5,6]`, yaitu ketujuh planet).
- Ephemeris Audit, grup **VSOP2013 planets**: empat pemeriksaan baru untuk Neptunus (total 28): X, Y, Z ekliptik dinamis (79 % dari toleransi 10⁻¹⁰), X, Y, Z ICRS (86 %), dan elemen elips (48 %); dan VSOP2013 terhadap IPS2000 (11 epoch 500–2498): selisih 3-D maksimum 2,0×10⁻³ au, toleransi 2,5×10⁻³ au (lihat di bawah). Seluruh audit lulus 265 dari 265 di Chromium.
- `tools/patch_asterid_vsop_neptune.py`: penambal untuk `ASTERID.html` yang sudah memuat Merkurius sampai Uranus.
### Diubah
- **Selisih Neptunus terhadap IPS2000 jauh lebih besar daripada planet lain.** Maksimum 3-D 2,0×10⁻³ au (299.000 km): 13,6″ pada longitude heliosentris di 500 CE, 12,3″ pada 700 CE, 4,6″ pada 1500 CE, 0,6″ pada 1900 CE (di dalam jendela pencocokan VSOP2013 1890–2000), 1,6″ pada 2100 CE, 4,6″ pada 2498 CE. Ini melampaui galat yang dinyatakan penyusun VSOP2013 (1,27″ untuk −4000…+8000) dan selisih IPS2000 terhadap DE406 (0,006″ untuk Neptunus). Kedua pembaca cocok dengan acuannya (VSOP2013.ctl 8×10⁻¹¹ au, notice.txt IPS2000 7×10⁻¹¹ au), sehingga ini selisih antara dua teori acuan (INPOP10a versus DE406), bukan galat pembacaan. Penyebab pastinya belum diteliti dan dokumentasi yang dipegang tidak menyatakan teori mana yang lebih dekat ke posisi sebenarnya pada 500 CE. Toleransi audit 2,5×10⁻³ au adalah selisih teramati + 25 % sebagai pagar regresi, bukan validasi; toleransi berdasarkan galat yang dinyatakan penyusun (1,8×10⁻⁴ au pada jarak perihelion 29,73 au) terlampaui 11 kali dan memang tidak dipakai.
- Tab PLANETS dan SKY VIEW: posisi heliosentris Neptunus dari VSOP2013 bila berkas termuat, jika tidak IPS2000. Pada 2026-11-15 12:00 UTC arah tampak Neptunus dari kedua deret berbeda 240 mas.
- Kini ketujuh planet memakai VSOP2013; IPS2000 menjadi cadangan (berkas `.bin` belum termuat) dan pembanding independen di audit. Rentang PLANETS dan SKY VIEW tetap 500–2498 CE (rentang IPS2000); perluasan ke −4000…+8000 menunggu keputusan.
- Teks antarmuka dan keterangan audit menyebut Merkurius sampai Neptunus. `sw.js` ikut menyimpan `vsop2013_neptune.bin`.
- Ukuran dan waktu: `ASTERID.html` 25.969.914 byte (sisa 244.486 byte di bawah 25 MiB). Pada Chromium desktop `plCompute` untuk tujuh planet (semuanya dari VSOP2013) sekitar 48 ms per panggilan; kecepatan di ponsel belum diukur.

## [VSOP2013 untuk Uranus] — 2026-11-15
### Ditambahkan
- **`vsop2013_uranus.bin`** (3,8 MiB): deret VSOP2013 penuh untuk Uranus (Simon dkk. 2013; berkas IMCCE `VSOP2013p7.dat`, 59 series, 330.581 suku, tanpa truncation; suku gerak rata-rata pada deret l tidak disimpan, sehingga 330.580 suku; 39.478 argumen berbeda). Semua pengali muat di int8 (format `VS13`; berkas planet lain tidak berubah). Terhadap blok Uranus di `VSOP2013.ctl` (11 epoch 1890–2000) selisih maksimum 6,0×10⁻¹¹ au per komponen (batas pembulatan acuan 10 desimal), diperiksa dengan pembaca independen `tools/test_vsop2013_bin.py`.
- Baris LED **VSOP URA** dan baris status di tab PLANETS untuk Uranus (daftar planet `AV` menjadi `[0,1,2,3,4,5]`).
- Ephemeris Audit, grup **VSOP2013 planets**: empat pemeriksaan baru untuk Uranus (total 24): X, Y, Z ekliptik dinamis 6,0×10⁻¹¹ au, X, Y, Z ICRS dan elemen elips (toleransi masing-masing 10⁻¹⁰, terburuk 60 %); dan VSOP2013 terhadap IPS2000 (11 epoch 500–2498): selisih 3-D maksimum 7,8×10⁻⁵ au, toleransi 2,2×10⁻⁴ au. Seluruh audit lulus 261 dari 261 di Chromium.
- `tools/patch_asterid_vsop_uranus.py`: penambal untuk `ASTERID.html` yang sudah memuat Merkurius, Venus, Mars, Jupiter, dan Saturn.
### Diubah
- Tab PLANETS dan SKY VIEW: posisi heliosentris Uranus dari VSOP2013 bila berkas termuat, jika tidak IPS2000. Pada 2026-11-15 12:00 UTC arah tampak Uranus dari kedua deret berbeda 146 mas.
- Selisih terhadap IPS2000: 0,81″ pada longitude heliosentris di 500 CE, 0,66″ pada 700 CE, 0,42″ pada 1100 CE, 0,04–0,09″ pada 1700–2100 CE, lalu naik lagi ke 0,44″ pada 2298 CE. Pola ini sesuai dengan sifat VSOP2013 (dicocokkan ke INPOP10a pada 1890–2000) dibanding IPS2000 (dicocokkan ke DE406); kedua pembaca cocok dengan acuannya masing-masing hingga 5×10⁻¹¹ au, sehingga ini bukan galat pembacaan. Toleransi 2,2×10⁻⁴ au berasal dari galat longitude 2,45″ yang dinyatakan penyusun VSOP2013 untuk −4000…+8000 (README IMCCE) pada jarak perihelion 18,29 au; selisih teramati memakai 35 % toleransi itu. Tidak ada angka galat IPS2000 khusus Uranus di dokumentasi yang dipegang.
- Rentang PLANETS dan SKY VIEW tetap 500–2498 CE selama Neptunus memakai IPS2000.
- Teks antarmuka dan keterangan audit menyebut Merkurius, Venus, Mars, Jupiter, Saturn, dan Uranus. `sw.js` ikut menyimpan `vsop2013_uranus.bin`.
- Ukuran dan waktu: `ASTERID.html` 25.967.111 byte (sisa 247.289 byte di bawah 25 MiB). Pada Chromium desktop `plCompute` untuk tujuh planet (enam dari VSOP2013) sekitar 52 ms per panggilan (sebelumnya sekitar 40 ms dengan lima); kecepatan di ponsel belum diukur.

## [VSOP2013 untuk Saturn] — 2026-11-15
### Ditambahkan
- **`vsop2013_saturn.bin`** (4,0 MiB): deret VSOP2013 penuh untuk Saturn (Simon dkk. 2013; berkas IMCCE `VSOP2013p6.dat`, 80 series, 350.525 suku, tanpa truncation; suku gerak rata-rata pada deret l tidak disimpan, sehingga 350.524 suku; 37.460 argumen berbeda). Semua pengali muat di int8 (format `VS13`; berkas planet lain tidak berubah). Terhadap blok Saturn di `VSOP2013.ctl` (11 epoch 1890–2000) selisih maksimum 6,5×10⁻¹¹ au per komponen (batas pembulatan acuan 10 desimal), diperiksa dengan pembaca independen `tools/test_vsop2013_bin.py`.
- Baris LED **VSOP SAT** dan baris status di tab PLANETS untuk Saturn (daftar planet `AV` menjadi `[0,1,2,3,4]`).
- Ephemeris Audit, grup **VSOP2013 planets**: empat pemeriksaan baru untuk Saturn (total 20): X, Y, Z ekliptik dinamis 6,5×10⁻¹¹ au, X, Y, Z ICRS 5,4×10⁻¹¹ au, dan elemen elips 5,0×10⁻¹¹ (toleransi masing-masing 10⁻¹⁰); dan VSOP2013 terhadap IPS2000 (11 epoch 500–2498): selisih 3-D maksimum 2,1×10⁻⁵ au, toleransi 5,1×10⁻⁴ au. Seluruh audit lulus 257 dari 257 di Chromium.
- `tools/patch_asterid_vsop_saturn.py`: penambal untuk `ASTERID.html` yang sudah memuat Merkurius, Venus, Mars, dan Jupiter.
### Diubah
- Tab PLANETS dan SKY VIEW: posisi heliosentris Saturn dari VSOP2013 bila berkas termuat, jika tidak IPS2000. Pada 2026-11-15 12:00 UTC arah tampak Saturn dari kedua deret berbeda 36 mas.
- Selisih terhadap IPS2000: 0,49″ pada longitude heliosentris di 500 CE, 0,24″ pada 700 CE, lalu 0,06–0,14″ dari 900 CE ke atas, sejalan dengan selisih IPS2000 terhadap DE406 yang dinyatakan penyusunnya (hingga 0,064″ untuk Saturn). Toleransi 5,1×10⁻⁴ au berasal dari galat longitude 11,73″ yang dinyatakan penyusun VSOP2013 untuk −4000…+8000 (README IMCCE) pada jarak perihelion 9,0 au; selisih teramati hanya 4 % dari toleransi itu, jadi toleransi ini longgar untuk rentang 500–2498 CE.
- Rentang PLANETS dan SKY VIEW tetap 500–2498 CE selama planet lain memakai IPS2000.
- Teks antarmuka dan keterangan audit menyebut Merkurius, Venus, Mars, Jupiter, dan Saturn. `sw.js` ikut menyimpan `vsop2013_saturn.bin`.
- Ukuran dan waktu: `ASTERID.html` 25.964.545 byte (sisa 249.855 byte di bawah 25 MiB). Pada Chromium desktop `plCompute` untuk tujuh planet (lima dari VSOP2013) sekitar 40 ms per panggilan (sebelumnya sekitar 34 ms dengan empat); kecepatan di ponsel belum diukur.

## [VSOP2013 untuk Jupiter] — 2026-11-15
### Ditambahkan
- **`vsop2013_jupiter.bin`** (3,7 MiB): deret VSOP2013 penuh untuk Jupiter (Simon dkk. 2013; berkas IMCCE `VSOP2013p5.dat`, 80 series, 324.608 suku, tanpa truncation; suku gerak rata-rata pada deret l tidak disimpan, sehingga 324.607 suku; 37.462 argumen berbeda). Semua pengali argumen muat di int8, jadi berkas ini berformat `VS13` (pembuat memilih sendiri; berkas Merkurius, Venus, dan Mars tidak berubah). Terhadap blok Jupiter di `VSOP2013.ctl` (11 epoch 1890–2000) selisih maksimum 5,4×10⁻¹¹ au per komponen (batas pembulatan acuan 10 desimal), diperiksa dengan pembaca independen `tools/test_vsop2013_bin.py`.
- Baris LED **VSOP JUP** dan baris status di tab PLANETS untuk Jupiter (daftar planet `AV` menjadi `[0,1,2,3]`).
- Ephemeris Audit, grup **VSOP2013 planets**: empat pemeriksaan baru untuk Jupiter (total 16): X, Y, Z ekliptik dinamis 5,4×10⁻¹¹ au, X, Y, Z ICRS 5,2×10⁻¹¹ au, dan elemen elips 4,8×10⁻¹¹ (toleransi masing-masing 10⁻¹⁰); dan VSOP2013 terhadap IPS2000 (11 epoch 500–2498): selisih 3-D maksimum 4,9×10⁻⁵ au, toleransi 1,1×10⁻⁴ au. Seluruh audit lulus 253 dari 253 di Chromium.
- `tools/patch_asterid_vsop_jupiter.py`: penambal untuk `ASTERID.html` yang sudah memuat Merkurius, Venus, dan Mars (daftar planet, tabel `.ctl` Jupiter, dan `vpAudit`; setiap penggantian harus cocok tepat satu kali).
### Diubah
- Tab PLANETS dan SKY VIEW: posisi heliosentris Jupiter dari VSOP2013 bila berkas termuat, jika tidak IPS2000. Pada 2026-11-15 12:00 UTC arah tampak Jupiter dari kedua deret berbeda 49 mas.
- Selisih terhadap IPS2000 lebih besar daripada untuk planet dalam: 1,9″ pada longitude heliosentris di 500 CE, 1,3″ pada 1100 CE, 0,41″ pada 1700 CE, 0,12″ pada 1900 CE, lalu naik lagi ke 0,74″ pada 2498 CE. Pola ini sesuai dengan sifat VSOP2013 (dicocokkan ke INPOP10a pada 1890–2000) dibanding IPS2000 (dicocokkan ke DE406); kedua pembaca cocok dengan acuannya masing-masing hingga 5×10⁻¹¹ au, sehingga ini bukan galat pembacaan. Toleransi 1,1×10⁻⁴ au berasal dari galat longitude 4,47″ yang dinyatakan penyusun VSOP2013 untuk −4000…+8000 (README IMCCE) pada jarak perihelion 4,95 au; selisih teramati memakai 45 % toleransi itu. Tidak ada angka galat IPS2000 khusus Jupiter di dokumentasi yang dipegang.
- Rentang PLANETS dan SKY VIEW tetap 500–2498 CE selama planet lain memakai IPS2000.
- Teks antarmuka dan keterangan audit menyebut Merkurius, Venus, Mars, dan Jupiter. `sw.js` ikut menyimpan `vsop2013_jupiter.bin`.
- Ukuran dan waktu: `ASTERID.html` 25.962.018 byte (sisa 252.382 byte di bawah 25 MiB). Pada Chromium desktop `plCompute` untuk tujuh planet (empat dari VSOP2013) sekitar 34 ms per panggilan (sebelumnya sekitar 27 ms dengan tiga); kecepatan di ponsel belum diukur.

## [VSOP2013 untuk Mars] — 2026-11-15
### Ditambahkan
- **`vsop2013_mars.bin`** (4,3 MiB): deret VSOP2013 penuh untuk Mars (Simon dkk. 2013; berkas IMCCE `VSOP2013p4.dat`, 52 series, 309.140 suku, tanpa truncation; suku gerak rata-rata pada deret l tidak disimpan, sehingga 309.139 suku; 41.884 argumen berbeda). Terhadap blok Mars di `VSOP2013.ctl` (11 epoch 1890–2000) selisih maksimum 5,0×10⁻¹¹ au per komponen (batas pembulatan acuan 10 desimal).
- **Format `VS14`**: pada Mars pengali argumen Jupiter mencapai ±144, di luar rentang int8 yang dipakai format `VS13`. Pembuat kini memilih sendiri: `VS13` bila semua pengali muat di int8, selain itu `VS14` dengan pengali int16 (tata letak lain sama). Berkas Merkurius dan Venus tetap `VS13` dan dibuat ulang byte demi byte identik; pembaca di `ASTERID.html` (`VSP`) dan `tools/test_vsop2013_bin.py` menerima keduanya. Mesin EMB tidak disentuh.
- Baris LED **VSOP MAR** dan baris status di tab PLANETS untuk Mars (daftar planet `AV` menjadi `[0,1,2]`).
- Ephemeris Audit, grup **VSOP2013 planets**: empat pemeriksaan baru untuk Mars (total 12): X, Y, Z ekliptik dinamis 5,0×10⁻¹¹ au, X, Y, Z ICRS 5,0×10⁻¹¹ au, dan elemen elips 5,0×10⁻¹¹ (toleransi masing-masing 10⁻¹⁰); dan VSOP2013 terhadap IPS2000 (11 epoch 500–2498): selisih 3-D maksimum 4,0×10⁻⁶ au, toleransi 1,2×10⁻⁵ au. Selisih ini jauh lebih besar daripada untuk Merkurius dan Venus dan tumbuh ke masa lalu (0,50″ pada 500 CE, paling besar 0,02″ dari 1499 CE); toleransinya berasal dari galat longitude 1,74″ yang dinyatakan penyusun VSOP2013 untuk −4000…+8000 pada jarak perihelion Mars 1,381 au, dan angka teramati dicatat di keterangan baris. Seluruh audit: 249 dari 249 lulus di Chromium (sebelumnya 245).
- `tools/patch_asterid_vsop_mars.py`: penambal untuk `ASTERID.html` yang sudah memuat Merkurius dan Venus (menambah dukungan `VS14` pada pembaca, daftar planet, tabel `.ctl` Mars, dan `vpAudit`; setiap penggantian harus cocok tepat satu kali).
### Diubah
- Tab PLANETS dan SKY VIEW: posisi heliosentris Mars dari VSOP2013 bila berkas termuat, jika tidak IPS2000. Pada 2026-11-15 12:00 UTC tampak Mars dari kedua deret berbeda 6,1 mas.
- Rentang PLANETS dan SKY VIEW tetap 500–2498 CE selama planet lain memakai IPS2000. Perluasan rentang menunggu planet lain.
- Teks antarmuka dan keterangan audit menyebut Merkurius, Venus, dan Mars. `sw.js` ikut menyimpan `vsop2013_mars.bin`.
- Ukuran dan waktu: `ASTERID.html` 25.959.505 byte (sisa 254.895 byte di bawah 25 MiB). Pada Chromium desktop `plCompute` untuk tujuh planet (tiga dari VSOP2013) sekitar 27 ms per panggilan (sebelumnya 19 ms dengan dua); kecepatan di ponsel belum diukur.

## [VSOP2013 untuk Merkurius] — 2026-11-15
### Ditambahkan
- **`vsop2013_mercury.bin`** (3,3 MiB): deret VSOP2013 penuh untuk Merkurius (Simon dkk. 2013; berkas IMCCE `VSOP2013p1.dat`, 62 series, 272.360 suku, tanpa truncation; suku gerak rata-rata pada deret l tidak disimpan, seperti pada Venus, sehingga 272.359 suku). Argumen disimpan sebagai kamus tanpa duplikat (38.614 argumen berbeda). Format dan pembuatnya sama dengan Venus (`tools/build_vsop2013_bin.py`); dibuat ulang dari `VSOP2013p1.dat` tanpa perubahan pada pembuat. Terhadap `VSOP2013.ctl` (blok Merkurius, 11 epoch 1890–2000) selisih maksimum 4,9×10⁻¹¹ au per komponen (sekitar 7 m; batas pembulatan acuan 10 desimal).
- Baris LED **VSOP MER** dan baris status di tab PLANETS untuk Merkurius (pembaca dan antarmuka sudah generik; hanya daftar planet `AV` yang diubah dari `[1]` menjadi `[0,1]`).
- Ephemeris Audit, grup **VSOP2013 planets**: `vpAudit` kini berulang atas semua planet di `VSP.AV`; baris `VSOP2013.ctl` Merkurius (11 epoch, sekitar 1,9 KB) ditanam di samping baris Venus. Empat pemeriksaan baru untuk Merkurius (total 8): X, Y, Z ekliptik dinamis 4,7×10⁻¹¹ au, X, Y, Z ICRS 5,0×10⁻¹¹ au, dan elemen elips 4,9×10⁻¹¹ (toleransi masing-masing 10⁻¹⁰); dan VSOP2013 terhadap IPS2000 (11 epoch 500–2498): selisih 3-D maksimum 9,0×10⁻⁸ au, toleransi 1,5×10⁻⁷ au. Toleransi terakhir ini berasal dari selisih terbesar IPS2000 terhadap DE406 yang dinyatakan penyusunnya untuk longitude heliosentris planet mana pun (0,064″), pada jarak aphelion Merkurius 0,467 au; angka khusus Merkurius tidak tersedia di dokumentasi yang kami pegang, dan selisih teramati dicatat di keterangan baris. Baris Venus tidak berubah. Seluruh audit: 245 dari 245 lulus di Chromium (sebelumnya 241); transit Merkurius 11 November 2019 (kini lewat VSOP2013 Merkurius) tetap cocok dengan Espenak (0,036″ dan 0,24 s).
- `tools/patch_asterid_vsop_mercury.py`: penambal untuk `ASTERID.html` yang sudah memuat modul `VSP` (setiap penggantian harus cocok tepat satu kali; membaca blok Merkurius dari `VSOP2013.ctl`).
### Diubah
- Tab PLANETS dan SKY VIEW: posisi heliosentris Merkurius dari VSOP2013 bila berkas termuat, jika tidak IPS2000 seperti sebelumnya. Pada 2026-11-15 12:00 UTC tampak Merkurius dari kedua deret berbeda 3,1 mas.
- Rentang PLANETS dan SKY VIEW tetap 500–2498 CE selama planet lain memakai IPS2000. Perluasan rentang menunggu planet lain.
- Teks antarmuka dan keterangan audit menyebut Merkurius dan Venus. `sw.js` ikut menyimpan `vsop2013_mercury.bin`.
- Ukuran dan waktu: `ASTERID.html` 25.956.994 byte (24,76 MiB; +2,5 KB, sisa 257.406 byte di bawah 25 MiB). Pada Chromium desktop `plCompute` untuk tujuh planet (dua dari VSOP2013) sekitar 19 ms per panggilan; kecepatan di ponsel belum diukur.

## [VSOP2013 untuk Venus] — 2026-11-15
### Ditambahkan
- **`vsop2013_venus.bin`** (3,5 MiB): deret VSOP2013 penuh untuk Venus (Simon dkk. 2013; berkas IMCCE `VSOP2013p2.dat`, 60 series, 289.647 suku, tanpa truncation). Argumen (17 pengali bulat) disimpan sebagai kamus tanpa duplikat (41.158 argumen berbeda); koefisien S, C float64 untuk suku dengan |S|+|C| ≥ 10⁻⁵ dan float32 untuk sisanya. Suku gerak rata-rata pada deret l (pangkat waktu 1, semua pengali nol) tidak disimpan; seperti `VSOP2013.f`, pembaca menambahkan freqpla·T lalu mereduksi modulo 2π. `.bin` dibuat ulang dari `.dat` byte demi byte identik oleh `tools/build_vsop2013_bin.py`.
- **`VSP`** (blok SKY VIEW dan PLANETS, setelah IPS2000): pembaca `.bin`. Elemen elips a, l, k, h, q, p dihitung per argumen unik (sin dan cos sekali per argumen), lalu diubah ke X, Y, Z dengan algoritma `ELLXYZ` dari `VSOP2013.f` dan diputar ke ICRS dengan rotasi pada README VSOP2013 (ε, φ), kerangka yang sama dengan model Bumi. Dimuat sesuai kebutuhan: `fetch('vsop2013_venus.bin')` di PWA atau server, tombol **LOAD vsop2013_venus.bin** di tab PLANETS saat dibuka dari `file://`, atau `window.__VSOP_B64 = {venus: '…'}` untuk rilis satu berkas. Berkas yang ditolak (bukan berkas VSOP2013, ukuran tidak cocok) tidak pernah menghapus data yang sudah termuat.
- Baris LED **VSOP VEN** (NOT LOADED, LOADING…, LOADED, FAILED) dan baris status di tab PLANETS.
- Ephemeris Audit: grup baru **VSOP2013 planets** (4 pemeriksaan): X, Y, Z ekliptik dinamis, X, Y, Z ICRS, dan elemen elips Venus terhadap `VSOP2013.ctl` (11 epoch 1890–2000), masing-masing maksimum 4,9×10⁻¹¹ au (sekitar 7 m; batas pembulatan acuan 10 desimal, toleransi 10⁻¹⁰); dan Venus VSOP2013 terhadap IPS2000 (teori independen, 11 epoch 500–2498): selisih 3-D maksimum 7,4×10⁻⁸ au (toleransi 2×10⁻⁷). Tanpa berkas, grup ini hanya memuat satu baris informasi, dan cache audit mengikuti status muat. Seluruh audit lulus 241 / 241 dengan berkas termuat.
- `tools/`: `build_vsop2013_bin.py` (juga memuat format berkas), `test_vsop2013_bin.py` (decoder, deret, dan Kepler terhadap `VSOP2013.ctl`), `patch_asterid_vsop_venus.py` dengan `vsop2013_reader.js` (modul pembaca yang disisipkan; setiap penggantian harus cocok tepat satu kali).
### Diubah
- Tab PLANETS dan SKY VIEW: posisi heliosentris Venus dari VSOP2013 bila berkas termuat, jika tidak IPS2000 seperti sebelumnya. Planet lain tidak berubah. Pada 2026-11-15 12:00 UTC tampak Venus dari kedua deret berbeda 7,5 mas (jarak ke Bumi 1,0×10⁻⁸ au). Tampilan di PLANETS dihitung ulang begitu berkas selesai dimuat.
- Rentang PLANETS dan SKY VIEW tetap 500–2498 CE selama planet lain memakai IPS2000, juga untuk Venus (deret VSOP2013 Venus sendiri berlaku −4000…+8000). Perluasan rentang menunggu planet lain.
- `sw.js` ikut menyimpan `vsop2013_venus.bin` untuk penggunaan offline.
- Ukuran dan waktu: `ASTERID.html` 24,75 MiB (+11 KB, sisa sekitar 254 KiB di bawah 25 MiB). Pada Chromium desktop satu evaluasi deret Venus sekitar 2 ms dan pembacaan berkas sekitar 60 ms; kecepatan di ponsel belum diukur.
- Keterbatasan: selisih yang dinyatakan penyusunnya terhadap INPOP10a untuk Venus adalah 0,02 mas (longitude heliosentris) dan 0,002 km (jarak) pada 1890–2000, serta 0,15″ dan 4 km pada −4000…+8000. `build_full.py` belum menanam `vsop2013_venus.bin` ke `ASTERID_full.html`.

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
