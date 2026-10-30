<p align="center"><img src="icon-192.png" alt="Logo ASTERID" width="120"></p>

<h1 align="center">ASTERID</h1>

<p align="center"><b>Sun · Earth · Moon</b> — efemeris, gerhana, dan pengamatan Bulan dalam satu berkas HTML</p>

<p align="center"><a href="https://rakawi182.github.io/ASTERID-OBSV/"><b>▶ Buka aplikasi</b></a></p>

> _A single-file astronomy web app: Sun–Moon ephemeris, eclipse prediction and lunar observation tools, with an in-page audit against published test vectors._

## Fitur

Aplikasi punya tujuh halaman:

| Halaman | Isi singkat |
|---|---|
| **HUD** | Tampilan bola langit dengan layer dan kontrol pandangan; pengamat (horizon, PZX), laboratorium trigonometri bola, segitiga astronomi PZX 3D; posisi Matahari dan Bulan; syzygy dan gerhana; jalur gerhana matahari (peta dan lokal); Ephemeris Audit |
| **ORBIT · ANGLES** | Segitiga Matahari–Bumi–Bulan: elongasi, sudut fase, jarak, tampilan 3D bidang ekliptika |
| **MOON FACE** | Efemeris fisik Bulan (fase, libasi, titik sub-solar, sudut posisi sumbu) dengan cakram dari mosaik LROC-WAC dan relief GLD100; gerhana bulan; appulse Bulan dengan bintang katalog |
| **TIME SCALES** | Konverter skala waktu (UTC, UT1, TT, TCG, ERA, GMST/GST, dan lainnya) |
| **TOPOCENTRIC** | Posisi toposentrik untuk pengamat: refraksi, gradien atmosfer (APG), tunda troposfer VMF3, permukaan acuan RTM, meteorologi waktu nyata (ECMWF), dan pemuatan non-pasang |
| **ECLIPSE CATALOG** | Katalog gerhana NASA −1999…+3000 (11.898 gerhana matahari dan 12.064 gerhana bulan) dengan deret Saros |
| **STAR CATALOG** | Katalog Hipparcos (ESA SP-1200): 8.870 bintang V ≤ 6,5 dengan tempat tampak (apparent place), tinggi dan azimut di lokasi dan waktu HUD, B−V, bintang ganda/majemuk, dan data bintang variabel (Vol. 11); pencarian nomor HIP atau nama, urutan MAG/HIP/ALT/RA, filter HUD stars, above horizon, dan multiple |

Kontrol waktu simulasi (maju/mundur, kecepatan, fase Bulan, gerhana, perigee/apogee) tersedia di atas halaman. **Ephemeris Audit** menjalankan uji langsung di halaman terhadap vektor uji publikasi (VSOP2013, IPS2000, JANUS, SOFA, IERS, LLIB, Meeus, NASA/Espenak).

Inti perhitungan:

- **Matahari dan planet:** VSOP2013.
- **Bulan:** ELP/MPP02 (fit LLR); JANUS dipakai di luar |t| = 30 abad.
- **Bintang:** katalog Hipparcos ESA SP-1200 (reduksi asli 1997), posisi epos J1991.25 dipropagasi linear ke J2000, lalu tempat tampak lewat jalur yang sama dengan HUD (paralaks, defleksi cahaya, aberasi, presesi–nutasi).
- **Presesi dan nutasi:** IAU 2006/2000A (setara `iauNut06a` SOFA).
- **ΔT:** spline Morrison dkk. (2021) untuk −720…+2019, lalu parabola jangka panjang di luar tabel.
- **EOP:** seri IERS 20 C04 dan Bulletin A tertanam di dalam berkas.
- **Pemuatan non-pasang:** ESMGFZ (NTAL, NTOL, HYDL, SLEL).

## Cara memakai

1. Buka <https://rakawi182.github.io/ASTERID-OBSV/> di browser, **atau** unduh `ASTERID.html` dan buka langsung di browser (Chrome, Firefox, Edge, dan sebagainya).
2. Aplikasi hampir seluruhnya berjalan **offline** karena semua data dan seri sudah tertanam. Pengecualian: **meteorologi waktu nyata** (ECMWF IFS HRES lewat [Open-Meteo](https://open-meteo.com)) butuh internet. Hasilnya disimpan di `localStorage` sampai 6 jam, dan tanpa data itu aplikasi memakai model GPT3.

Ukuran berkas sekitar 25 MB karena seluruh seri ephemeris dan data sudah tertanam. Pemuatan pertama lewat data seluler agak berat.

## Pasang sebagai aplikasi (PWA)

1. Buka <https://rakawi182.github.io/ASTERID-OBSV/> di Chrome (Android) atau Safari (iPhone) dan tunggu sampai terbuka penuh.
2. Chrome: menu ⋮ → **Pasang aplikasi** / **Tambahkan ke layar utama**. Safari: **Bagikan** → **Tambah ke Layar Utama**.
3. Setelah dibuka sekali, aplikasi berjalan offline. Setiap kali dibuka, versi terbaru diperiksa di latar belakang dan dipakai pada pembukaan berikutnya.

Mengaktifkan GitHub Pages: **Settings → Pages → Deploy from a branch → main / (root)**. Jika berkas HTML diganti namanya, ubah `APP_FILE` di `sw.js` dan `index.html`.

## Memperbarui data tertanam

Skrip `update_asterid_data.py` (Python 3 dan NumPy) memperbarui seri **EOP IERS** dan grid pemuatan **ESMGFZ** di dalam `ASTERID.html` tanpa membangun ulang aplikasi. Contoh:

```bash
# C04 dan Bulletin A baru
python3 update_asterid_data.py ASTERID.html --c04 EOP_20u24_C04_one_file_1962-now.txt --bulletin bulletina-xxxix-043.txt

# hanya Bulletin A mingguan
python3 update_asterid_data.py ASTERID.html --bulletin bulletina-xxxix-044.txt

# hanya C04
python3 update_asterid_data.py ASTERID.html --c04 EOP_20u24_C04_one_file_1962-now.txt
```

Opsi yang berguna: `--out BERKAS` (tulis ke berkas lain, disarankan agar yang lama jadi cadangan), `--dry-run` (hanya melapor), `--force`, dan `--ntal/--ntol/--hydl/--slel` untuk berkas CSV ESMGFZ. Rincian lengkap ada di docstring bagian atas skrip.

Sumber berkas IERS: <https://hpiers.obspm.fr/eoppc/eop/eopc04/> dan <https://datacenter.iers.org/eop.php> (C04), serta <https://datacenter.iers.org/eop.php> dan <https://maia.usno.navy.mil> (Bulletin A). Setelah memperbarui, unggah ulang `ASTERID.html` ke repo agar versi online ikut berubah.

## Akurasi dan keterbatasan

Angka berikut adalah ketidakpastian yang dinyatakan di dalam aplikasi (halaman **ACCURACY · MODELS · REFERENCES** dan **Ephemeris Audit**), bukan klaim baru:

- JANUS: 0,5″ + 0,75″·|t| (bujur). VSOP2013 EMB: 0,02 mas (1890–2000) sampai 0,03″ (900–3100) terhadap INPOP10a. Pemotongan seri nutasi R06: 0,1 µas.
- Di luar |t| = 30 abad, Bulan JANUS diselaraskan ke ELP/MPP02 lewat koreksi bujur terpasang. Hasil sebelum −1000 **tidak diverifikasi independen**.
- Tabel fitur Bulan dimasukkan manual dan baik sampai sekitar ±1° (±30 km) posisi selenografis.
- Batas gerhana matahari historis cocok dengan efemeris dan ΔT dalam ±20 detik untuk −708…1567.
- Katalog bintang memakai reduksi Hipparcos asli (1997), bukan reduksi baru (2007) maupun Gaia. Gerak diri dan paralaks dipropagasi linear dari J1991.25; kecepatan radial dipakai hanya untuk 21 bintang yang membutuhkannya, selebihnya 0. Alt/Az bersifat geometrik (tanpa refraksi).
- Aplikasi ini alat bantu penelitian. Untuk publikasi, verifikasi hasil kunci dengan sumber independen.

## Struktur repositori

```
.
├── ASTERID.html              # aplikasi (satu berkas)
├── update_asterid_data.py    # pembaru data EOP IERS dan pemuatan ESMGFZ
├── index.html                # pintu masuk GitHub Pages
├── manifest.webmanifest      # metadata PWA
├── sw.js                     # service worker (offline)
├── icon-192.png  icon-512.png  maskable-512.png
├── apple-touch-icon.png  favicon.svg   # logo dan ikon
├── README.md
├── CHANGELOG.md
├── CITATION.cff              # metadata sitasi (tombol "Cite this repository")
├── CITATIONS.md              # daftar pustaka dan sumber data
├── LICENSE                   # MIT
└── .gitignore
```

## Proyek terkait

[OSS ΩLDJAVA](https://github.com/rakawi182/OSS_OLDJAVA): aplikasi arkeoastronomi dan kalender Jawa Kuno dalam satu berkas HTML.

## Sitasi

Jika Anda memakai ASTERID dalam penelitian, kutip repositori ini (lihat `CITATION.cff` atau tombol **Cite this repository** di GitHub) dan juga pustaka ilmiah yang mendasarinya di [`CITATIONS.md`](CITATIONS.md).

## Lisensi

Kode di repositori ini dilisensikan di bawah [MIT License](LICENSE). Data dan model pihak ketiga (VSOP2013, ELP/MPP02, data IERS, katalog gerhana NASA, katalog Hipparcos (ESA), ESMGFZ, mosaik LROC-WAC dan GLD100, Open-Meteo, dan lainnya) tetap tunduk pada ketentuan penyedia masing-masing; lihat [`CITATIONS.md`](CITATIONS.md).

## Kontribusi

Laporan galat dan saran sangat disambut lewat [Issues](../../issues). Mohon sertakan tanggal dan jam masukan, lokasi pengamat, hasil yang diharapkan, dan sumber pembandingnya.
