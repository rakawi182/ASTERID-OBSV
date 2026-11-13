<p align="center"><img src="icon-192.png" alt="Logo ASTERID" width="120"></p>

<h1 align="center">ASTERID</h1>

<p align="center"><b>Sun · Earth · Moon</b> — ephemeris, eclipse prediction, dan lunar observation dalam satu berkas HTML</p>

<p align="center"><a href="https://rakawi182.github.io/ASTERID-OBSV/"><b>▶ Buka aplikasi</b></a></p>

> _A single-file astronomy web app: Sun–Moon ephemeris, eclipse prediction and lunar observation tools, with an in-page audit against published test vectors._

## Ringkasan

ASTERID adalah aplikasi web satu berkas (`ASTERID.html`) untuk perhitungan astronomi posisi dan eclipse. Seluruh series dan data tertanam di dalam berkas, sehingga aplikasi berjalan offline, dan setiap hasil dapat diuji langsung di halaman lewat **Ephemeris Audit** terhadap test vectors dari publikasi.

## Fitur

Aplikasi memiliki sembilan halaman:

| Halaman | Isi |
|---|---|
| **SKY VIEW** | Peta langit dalam horizon frame (stereographic projection) yang mengikuti sensor gerak perangkat (gyroscope) atau geseran jari. Menampilkan bintang Hipparcos berwarna dari B−V, constellation lines, celestial equator dan ecliptic, Matahari, planet Merkurius–Neptunus (dengan magnitude), serta Bulan dengan phase dan topocentric parallax. Pada gerhana bulan, umbra dan penumbra ikut digambar. Mode kamera (AR) bersifat opsional, dan waktu mengikuti jam global. Sensor dan kamera hanya aktif lewat HTTPS |
| **PLANETS** | Merkurius sampai Neptunus: geocentric apparent place (true equator and equinox of date) dari series IPS2000 penuh (500–2498 CE) dengan light-time delay dan aberration. Setiap planet menampilkan RA/Dec, ecliptic λ/β, jarak ke Bumi dan Matahari, altitude/azimuth (di stasiun TOPOCENTRIC memakai rantai koreksi penuh tab TOPOCENTRIC; di lokasi HUD lain memakai rantai yang sama tanpa data khusus stasiun (deflection of the vertical dihitung per lokasi di dalam area DEM dan XGM), dengan refraction dari grid GPT3 global atau standard atmosphere, dan kartu diberi label), elongation, phase angle dan illuminated fraction, angular diameter, magnitude (Mallama & Hilton 2018), arah gerak (prograde/retrograde), serta next rise, transit, dan set. Ketuk planet untuk membukanya di SKY VIEW |
| **HUD** | Celestial sphere dengan layer dan kontrol pandangan; observer (horizon, PZX), spherical trigonometry lab, astronomical triangle PZX 3D; posisi Matahari dan Bulan; syzygy dan eclipse; jalur gerhana matahari (peta dan lokal); **Ephemeris Audit** |
| **ORBIT · ANGLES** | Segitiga Sun–Earth–Moon: elongation, phase angle, jarak, dan tampilan 3D ecliptic plane |
| **MOON FACE** | Efemeris fisik Bulan (phase, libration, sub-solar point, position angle sumbu) dengan cakram dari mosaik LROC-WAC dan relief GLD100; gerhana bulan; appulse Bulan dengan bintang katalog |
| **TIME SCALES** | Konverter time scales (UTC, UT1, TT, TCG, ERA, GMST/GST, dan lainnya) |
| **TOPOCENTRIC** | Posisi topocentric untuk **stasiun tetap** Jolotundo (Mt. Pawitra; −7,609444°, 112,595556°, 583,355 m), bukan lokasi HUD: refraction, atmospheric gradients (APG), tropospheric delay VMF3, RTM reference surface, real-time meteorology (ECMWF), dan non-tidal loading |
| **ECLIPSE CATALOG** | Katalog gerhana NASA −1999…+3000 (11.898 gerhana matahari dan 12.064 gerhana bulan) dengan Saros series |
| **STAR CATALOG** | Katalog Hipparcos: 8.870 bintang V ≤ 6,5 (new reduction 2007; proper motion dan parallax dari HGCA/Gaia EDR3 untuk 8.429 bintang). Tersedia apparent place, altitude dan azimuth pada lokasi dan waktu HUD, B−V (cross-checked dengan GCPD, BSC, Ducati), spectral type (BSC, Hipparcos), bintang ganda/majemuk, dan data bintang variabel (Vol. 11 dan GCVS 5.1). Fitur lain: atlas rasi (peta stereografik, overlay Almagest), kalkulator heliacal rising/setting (model Schaefer 1993), pencarian nomor HIP, nama, atau rasi (misalnya "orion" atau "cma"), badge rasi IAU di tiap baris, pengurutan MAG/HIP/ALT/RA, serta filter HUD stars, above horizon, dan multiple |

Kontrol waktu simulasi (maju/mundur, kecepatan, lunar phase, eclipse, perigee/apogee) tersedia di bagian atas halaman.

**Ephemeris Audit** menjalankan pengujian langsung di halaman terhadap test vectors dari publikasi: VSOP2013, IPS2000, JANUS, SOFA, IERS, LLIB, Meeus, dan NASA/Espenak, termasuk transit Mercury 2019 dan Venus 2012.

## Inti perhitungan

| Komponen | Model dan sumber |
|---|---|
| **Sun dan Earth** | VSOP2013 |
| **Planet (Mercury–Neptune)** | IPS2000 (Chapront & Francou 2002): full Poisson series tanpa truncation untuk 500–2498 CE (35.432 terms, disimpan lossless). Apparent place dihitung dengan light-time delay, aberration, dan precession–nutation frame yang sama dengan Matahari dan Bulan |
| **Moon** | ELP/MPP02 (LLR fit); JANUS dipakai di luar \|t\| = 30 century |
| **Stars** | Katalog Hipparcos (new reduction, van Leeuwen 2007), posisi epoch J1991.25 dipropagasi linear ke J2000. Untuk 8.429 bintang dipakai long-term proper motion Hipparcos–Gaia dan parallax Gaia EDR3 (HGCA, Brandt 2021). Magnitude V dan color dari ESA SP-1200 (1997). Apparent place memakai jalur yang sama dengan HUD (parallax, light deflection, aberration, precession–nutation) |
| **Constellations** | Batas rasi IAU (Delporte 1930, tabel Roman 1987) pada posisi yang diprecess ke B1875.0 |
| **Precession–nutation** | IAU 2006/2000A (setara `iauNut06a` SOFA) |
| **ΔT** | Spline Morrison dkk. (2021) untuk −720…+2019, lalu parabola jangka panjang di luar tabel |
| **EOP** | Series IERS 20 C04 dan Bulletin A, tertanam di dalam berkas |
| **Non-tidal loading** | ESMGFZ (NTAL, NTOL, HYDL, SLEL) |

## Cara memakai

1. Buka <https://rakawi182.github.io/ASTERID-OBSV/> di browser, **atau** unduh `ASTERID.html` dan buka langsung di browser (Chrome, Firefox, Edge, dan sebagainya).
2. Aplikasi hampir seluruhnya berjalan **offline** karena semua data dan series sudah tertanam. Pengecualiannya adalah **real-time meteorology** (ECMWF IFS HRES melalui [Open-Meteo](https://open-meteo.com)) yang membutuhkan internet. Hasilnya disimpan di `localStorage` hingga 6 jam. Lokasi HUD lain di dalam area DEM dan XGM mengambil permintaannya sendiri (empat lokasi terakhir disimpan). Tanpa data itu, aplikasi memakai model GPT3.

Ukuran berkas sekitar 25 MB (24,7 MiB) karena seluruh series ephemeris dan data tertanam; sebagian disimpan dengan lossless compression. Pemuatan pertama lewat data seluler cukup berat.

Satu data tidak tertanam: **`gpt3_1.bin`** (1,8 MiB), grid GPT3 global (1° × 1°) untuk refraction di lokasi HUD di luar stasiun. Berkas ini diletakkan di folder yang sama dengan `ASTERID.html` dan dimuat saat dibutuhkan, sehingga `ASTERID.html` tetap di bawah batas unggah browser GitHub (25 MiB). Dibuka lewat `file://`, browser memblokir pemuatan otomatis; pilih `gpt3_1.bin` dengan tombol **LOAD gpt3_1.bin** di tab PLANETS, atau pakai **`ASTERID_full.html`** dari halaman Releases (±33 MiB, satu berkas yang sudah memuat grid itu). Tanpa grid, aplikasi memakai standard refraction dan banner menyebutkannya. Dengan cara yang sama, **`opole_0p5.bin`** (2,0 MiB) membawa koefisien ocean pole tide loading global (Desai 2002, 0,5° × 0,5°) untuk lokasi HUD di luar stasiun (tombol **LOAD opole_0p5.bin**), dan **`otl_fes2014b_1.bin`** (1,5 MiB) membawa grid ocean tide loading global dari FES2014b (harmonik bola derajat 100, 11 gelombang utama, 1° × 1°; tombol **LOAD otl_fes2014b_1.bin**); **`apl_rp_1.bin`** (0,8 MiB) membawa grid atmospheric pressure loading global gelombang S1/S2 dan turunannya (Ray & Ponte 2003, load Love number Gegout, 1° × 1°; tombol **LOAD apl_rp_1.bin**); `ASTERID_full.html` memuat keempatnya.

## Pasang sebagai aplikasi (PWA)

1. Buka <https://rakawi182.github.io/ASTERID-OBSV/> di Chrome (Android) atau Safari (iPhone), lalu tunggu hingga halaman terbuka penuh.
2. Chrome: menu ⋮ → **Pasang aplikasi** / **Tambahkan ke layar utama**. Safari: **Bagikan** → **Tambah ke Layar Utama**.
3. Setelah dibuka sekali, aplikasi berjalan offline. Setiap kali dibuka, versi terbaru diperiksa di background dan dipakai pada pembukaan berikutnya.

Untuk mengaktifkan GitHub Pages: **Settings → Pages → Deploy from a branch → main / (root)**. Jika berkas HTML diganti namanya, ubah `APP_FILE` di `sw.js` dan `index.html`.

## Memperbarui data tertanam

Skrip `update_asterid_data.py` (Python 3 dan NumPy) memperbarui series **EOP IERS** dan grid **ESMGFZ** loading di dalam `ASTERID.html` tanpa membangun ulang aplikasi. Contoh:

```bash
# C04 dan Bulletin A baru
python3 update_asterid_data.py ASTERID.html --c04 EOP_20u24_C04_one_file_1962-now.txt --bulletin bulletina-xxxix-043.txt

# hanya Bulletin A mingguan
python3 update_asterid_data.py ASTERID.html --bulletin bulletina-xxxix-044.txt

# hanya C04
python3 update_asterid_data.py ASTERID.html --c04 EOP_20u24_C04_one_file_1962-now.txt
```

Opsi yang berguna: `--out BERKAS` (menulis ke berkas lain, disarankan agar berkas lama menjadi backup), `--dry-run` (hanya melaporkan), `--force`, dan `--ntal/--ntol/--hydl/--slel` untuk berkas CSV ESMGFZ. Rincian lengkap ada di docstring pada bagian atas skrip.

Sumber berkas IERS: <https://hpiers.obspm.fr/eoppc/eop/eopc04/> dan <https://datacenter.iers.org/eop.php> (C04), serta <https://datacenter.iers.org/eop.php> dan <https://maia.usno.navy.mil> (Bulletin A). Setelah pembaruan, unggah ulang `ASTERID.html` ke repositori agar versi online ikut berubah.

## Akurasi dan keterbatasan

Angka berikut adalah ketidakpastian yang dinyatakan di dalam aplikasi (halaman **ACCURACY · MODELS · REFERENCES** dan **Ephemeris Audit**), bukan klaim baru.

**Sun, Moon, dan model dasar**
- JANUS: 0,5″ + 0,75″·|t| (longitude). VSOP2013 EMB: 0,02 mas (1890–2000) hingga 0,03″ (900–3100) terhadap INPOP10a. Truncation series nutation R06: 0,1 µas.
- Di luar |t| = 30 century, Bulan JANUS diselaraskan ke ELP/MPP02 melalui fitted longitude correction. Hasil sebelum −1000 **tidak diverifikasi secara independen**.
- Tabel lunar features dimasukkan manual dan baik hingga sekitar ±1° (±30 km) pada posisi selenographic.
- Batas gerhana matahari historis cocok dengan ephemeris dan ΔT dalam ±20 detik untuk −708…1567.

**Stars**
- Katalog memakai new reduction Hipparcos (2007). Untuk 8.429 bintang, proper motion dan parallax berasal dari HGCA (Hipparcos–Gaia, Gaia EDR3), dipropagasi linear dari J1991.25.
- Radial velocity: Hipparcos Vol. 1 Tabel 1.2.3 (21 bintang), lalu Gaia DR2 melalui HGCA (σ ≤ 5 km/s), selebihnya 0.
- B−V berasal dari Hipparcos (dengan source code H39 pada label) dan dikoreksi untuk 218 bintang yang menyimpang lebih dari 0,05 mag dari konsensus minimal dua kompilasi (GCPD, BSC, Ducati). V (source code H7) dikoreksi dengan aturan yang sama untuk 87 bintang non-variabel. Kompilasi tersebut tidak sepenuhnya independen satu sama lain.
- Alt/Az bersifat geometric (tanpa refraction).

**Planets**
- IPS2000 hanya berlaku untuk 500–2498 CE; di luar rentang itu tab PLANETS kosong dan SKY VIEW tidak menggambar planet.
- Selisih IPS2000 terhadap DE406 yang dinyatakan penyusunnya pada heliocentric longitude maksimum 0,006″ (Neptune) hingga 0,064″ (Saturn).
- Series disimpan lossless sebagai float64 persis seperti berkas `ips2000.*`. Pada 11 epoch uji `notice.txt`, hasilnya cocok hingga 7×10⁻¹¹ au, yaitu batas pembulatan nilai acuan 10 desimal.
- Transit Mercury 11 November 2019 dan Venus 6 Juni 2012 cocok dengan Espenak dalam 0,04″ dan 0,4″ (acuan Venus dicetak dalam arcsecond bulat), dan dalam 0,3 s untuk waktu minimum separation.
- Alt/azimuth planet memakai rantai TOPOCENTRIC penuh di stasiun tetap (dalam 1 km dari lokasi HUD). Di lokasi lain rantai yang sama berjalan lewat `compute(R,E,{lat,lon,h})` tanpa data yang hanya ada di stasiun: solid Earth tide, pole tide, polar motion, s′, diurnal aberration, dan VMF3 diterapkan; refraction dari grid GPT3 global (`gpt3_1.bin`; tekanan, suhu, dan uap air pada tinggi orografi model sel 1°, plus gradien APG di bawah 15°) atau, bila berkas itu belum termuat, standard atmosphere (1010 hPa, 10 °C, kering). Di dalam area DEM dan XGM di sekitar stasiun (jarak ke tepi DEM ≥ 6 km dan di selatan 7,5° LS: sekitar 12 km ke utara, 7 km ke timur dan barat, 4,7 km ke selatan dari stasiun), deflection of the vertical dihitung di lokasi HUD itu sendiri (XGM2019e di lokasi tersebut ditambah RTM dari DEM dengan lokasi sebagai pengamat; ±2 detik setelah lokasi berubah, hasilnya di-cache), tinggi dari tinggi stasiun ditambah selisih DEM, dan meteorology dari ECMWF live yang diambil di lokasi itu sendiri (satu permintaan per lokasi, koordinat dibulatkan ke 0,01°, sel IFS 0,1°; p, T, e direduksi dari elevasi titik pada respons ke tinggi lokasi; aktif bila saklar ECMWF ON dan waktu dalam ±1 jam dari jam perangkat) atau, bila tidak tersedia, dari empat sel GPT3 tertanam di sekitar stasiun dengan bobot bilinear lokasi itu. Gerbangnya berupa kotak, bukan lingkaran: DEM (±30 × 26 km, tidak berpusat di stasiun) dan grid XGM hanya mencakup sekitar stasiun, sehingga lokasi harus berjarak ≥ 6 km dari setiap tepi DEM (RTM hanya kehilangan massa di luar jarak itu) dan berada di dalam empat sel GPT3 tertanam (lintang ≤ −7,5°); di luar area itu deflection tidak diterapkan (dapat mencapai detik busur). Tidak diterapkan di luar stasiun: ESMGFZ; atmospheric pressure loading S1/S2 (`apl_rp_1.bin`, radial; grid dibatasi derajat 10 (S1: 20), sehingga di stasiun menyimpang hingga sekitar 0,1 mm dari konstanta stasiun), ocean pole tide (`opole_0p5.bin`) dan ocean tide loading (`otl_fes2014b_1.bin`, dekat pantai dapat menyimpang beberapa persen amplitudo karena derajat 100) diterapkan dari grid global bila berkasnya termuat; di luar area DEM dan XGM juga ECMWF live. Konsistensi diaudit terhadap rantai TOPOCENTRIC di stasiun (selisih tidak boleh melebihi sudut yang dibentuk perpindahan khusus stasiun). Tinggi orografi model dapat berbeda dari tinggi sebenarnya; selisih 100 m mengubah tekanan sekitar 12 hPa.
- Magnitude planet (Mallama & Hilton 2018), angular diameter, serta rise, transit, dan set planet belum memiliki test vectors di audit.

Aplikasi ini adalah alat bantu penelitian. Untuk publikasi, verifikasi hasil kunci dengan sumber independen.

## Struktur repositori

```
.
├── ASTERID.html              # aplikasi (satu berkas)
├── gpt3_1.bin                # grid GPT3 global untuk refraction di luar stasiun (dimuat sesuai kebutuhan)
├── opole_0p5.bin             # koefisien ocean pole tide loading global (Desai 2002, 0,5°) untuk lokasi di luar stasiun (dimuat sesuai kebutuhan)
├── otl_fes2014b_1.bin        # grid ocean tide loading global (FES2014b, derajat 100, 1°) untuk lokasi di luar stasiun (dimuat sesuai kebutuhan)
├── apl_rp_1.bin              # grid atmospheric pressure loading global S1/S2 (Ray & Ponte 2003, 1°) untuk lokasi di luar stasiun (dimuat sesuai kebutuhan)
├── update_asterid_data.py    # pembaru data EOP IERS dan ESMGFZ loading
├── index.html                # entry point GitHub Pages
├── manifest.webmanifest      # metadata PWA
├── sw.js                     # service worker (offline)
├── icon-192.png  icon-512.png  maskable-512.png
├── apple-touch-icon.png  favicon.svg   # logo dan ikon
├── tools/                    # build_gpt3_bin.py, build_opole_bin.py, build_otl_bin.py, build_apl_bin.py, build_full.py, test_*_bin.py, otl_decoder.js (opsional)
├── README.md
├── CHANGELOG.md
├── CITATION.cff              # metadata sitasi (tombol "Cite this repository")
├── CITATIONS.md              # daftar pustaka dan sumber data
├── LICENSE                   # MIT
└── .gitignore
```

## Proyek terkait

[OSS ΩLDJAVA](https://github.com/rakawi182/OSS_OLDJAVA): aplikasi archaeoastronomy dan kalender Jawa Kuno dalam satu berkas HTML.

## Sitasi

Jika Anda memakai ASTERID dalam penelitian, kutip repositori ini (lihat `CITATION.cff` atau tombol **Cite this repository** di GitHub) beserta pustaka ilmiah yang mendasarinya di [`CITATIONS.md`](CITATIONS.md).

## Lisensi

Kode di repositori ini dilisensikan di bawah [MIT License](LICENSE). Data dan model pihak ketiga (VSOP2013, IPS2000, ELP/MPP02, data IERS, katalog gerhana NASA, katalog Hipparcos (ESA), HGCA, GCVS, BSC, GCPD, Ducati, ESMGFZ, mosaik LROC-WAC dan GLD100, Open-Meteo, dan lainnya) tetap tunduk pada ketentuan masing-masing penyedia; lihat [`CITATIONS.md`](CITATIONS.md).

## Kontribusi

Laporan bug dan saran sangat disambut lewat [Issues](../../issues). Mohon sertakan tanggal dan jam input, lokasi observer, hasil yang diharapkan, dan sumber pembandingnya.
