#!/usr/bin/env python3
# Memperbarui data tertanam di ASTERID.html: EOP IERS (C04 + Bulletin A) dan ESMGFZ (analisis + prakiraan).
# Versi Python murni (tanpa bash) -> jalan langsung di Pydroid3 (tombol Run).
#
#   run_asterid_update.py            -> menulis ASTERID_FULL.html
#   run_asterid_update.py --dry-run  -> hanya laporan, tidak menulis apa pun
#
# Berkas dicari di folder DIR. Yang dipilih otomatis:
#   - C04 dan Bulletin A: berkas terbaru menurut waktu ubah
#   - ESMGFZ analisis   : *_<tahun>_pointsubset.csv
#   - ESMGFZ prakiraan  : *_<tahun>_<hari>F_pointsubset.csv (nomor hari tertinggi, mis. 324F -> 331F)
# Versi pada nama (v1.0 atau v1_0) tidak dipaku. Bagian yang tidak ditemukan dilewati dengan peringatan.
# ASTERID.html tidak diubah (hasil ke ASTERID_FULL.html).
import os, re, sys, glob, fnmatch, subprocess

DIR = os.environ.get("ASTERID_DIR", "/storage/emulated/0/Download/ASTERID_PRIME/update")
IN, OUT, UPD = "ASTERID.html", "ASTERID_FULL.html", "update_asterid_data.py"
DRY = "--dry-run" in sys.argv[1:]

def die(msg):
    print("ERROR:", msg); sys.exit(1)

if not os.path.isdir(DIR):
    here = os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else os.getcwd()
    if os.path.isfile(os.path.join(here, UPD)):
        DIR = here
    else:
        die("folder %s tidak ada" % DIR)
os.chdir(DIR)
print("Folder:", DIR)

if not os.path.isfile(UPD): die("%s tidak ada di %s" % (UPD, DIR))
if not os.path.isfile(IN):  die("%s tidak ada di %s" % (IN, DIR))
with open(UPD, encoding="utf-8", errors="replace") as f:
    if "--ntal-fc" not in f.read():
        die("%s versi lama (tanpa --ntal-fc); ganti dengan yang baru" % UPD)

def natkey(s):  # urut versi, setara sort -V
    return [int(t) if t.isdigit() else t for t in re.split(r"(\d+)", s)]

def last_by_name(pattern, rx=None):
    L = [f for f in glob.glob(pattern) if os.path.isfile(f) and (rx is None or re.fullmatch(rx, f))]
    return max(L, key=natkey) if L else ""

def last_by_time(pattern):
    L = [f for f in glob.glob(pattern) if os.path.isfile(f)]
    return max(L, key=os.path.getmtime) if L else ""

args, used = [], []
c04 = last_by_time("EOP_*_C04_*.txt")
bul = last_by_time("bulletina-*.txt")
if c04: args += ["--c04", c04]; used.append("C04        : " + c04)
else:   print("PERINGATAN: berkas C04 tidak ditemukan, EOP C04 dilewati")
if bul: args += ["--bulletin", bul]; used.append("Bulletin A : " + bul)
else:   print("PERINGATAN: Bulletin A tidak ditemukan, dilewati")

for K in ("NTAL", "NTOL", "HYDL", "SLEL"):
    k = K.lower()
    an = last_by_name("ESMGFZ_%s_cm_v*_pointsubset.csv" % K,
                      r"ESMGFZ_%s_cm_v.*_[0-9]{4}_pointsubset\.csv" % K)
    fc = last_by_name("ESMGFZ_%s_cm_v*F_pointsubset.csv" % K,
                      r"ESMGFZ_%s_cm_v.*_[0-9]{4}_[0-9]{3}F_pointsubset\.csv" % K)
    if an: args += ["--" + k, an]; used.append("%s analisis : %s" % (K, an))
    else:  print("PERINGATAN: %s analisis tidak ditemukan, dilewati" % K)
    if fc: args += ["--%s-fc" % k, fc]; used.append("%s prakiraan: %s" % (K, fc))
    else:  print("PERINGATAN: %s prakiraan tidak ditemukan, tanpa prakiraan" % K)

if not args: die("tidak ada berkas data yang ditemukan di %s" % DIR)

print("Berkas yang dipakai:")
for u in used: print("  " + u)

cmd = [sys.executable, UPD, IN, "--out", OUT, "--start", "1962-01-01"] + args
if DRY: cmd.append("--dry-run")
print("\nMenjalankan:", " ".join(cmd), "\n")
r = subprocess.run(cmd)
if r.returncode != 0: die("updater gagal (kode %d)" % r.returncode)
print("\nSelesai (dry-run, tidak ada yang ditulis)." if DRY else "\nSelesai -> %s" % os.path.join(DIR, OUT))
