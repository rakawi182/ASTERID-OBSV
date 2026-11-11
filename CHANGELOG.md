# Changelog

Format mengikuti [Keep a Changelog](https://keepachangelog.com/id-ID/1.1.0/).

## [B−V diperiksa silang, atlas rasi, dan heliacal] — 2026-11-11
### Ditambahkan
- **Tipe spektrum** untuk 8.494 bintang dari Bright Star Catalogue (CDS V/50) dan supplemennya (CDS V/36), untuk bintang yang tidak punya tipe dari Vol. 11. Tampil di daftar dan di kartu bintang.
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
