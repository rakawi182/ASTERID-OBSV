# Changelog

Format mengikuti [Keep a Changelog](https://keepachangelog.com/id-ID/1.1.0/).

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
