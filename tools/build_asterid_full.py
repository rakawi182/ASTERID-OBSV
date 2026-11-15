#!/usr/bin/env python3
"""Make the single-file release: ASTERID.html with 4 .bin files and the VSOP2013 planet files embedded.

usage: python3 build_asterid_full.py ASTERID.html gpt3_1.bin opole_0p5.bin otl_fes2014b_1.bin apl_rp_1.bin ASTERID_full.html [vsop2013_<planet>.bin ...]
Without arguments (Run button) the default file names in the current folder are used.
Without VSOP2013 files every vsop2013_*.bin next to ASTERID.html is used. The planet key (= VSP.NM) comes from the file name
and is checked against the planet index in the .bin header (VS13/VS14).
"""
import sys, os, re, glob, json, base64

NM = {1: 'mercury', 2: 'venus', 4: 'mars', 5: 'jupiter', 6: 'saturn', 7: 'uranus', 8: 'neptune'}  # VSOP2013 index -> VSP.NM

def vsop_key(path):
    b = open(path, 'rb').read()
    assert b[:4] in (b'VS13', b'VS14'), path + ': bukan berkas vsop2013 .bin'
    name = NM.get(b[4])
    assert name, path + ': indeks planet %d di header tidak dikenal' % b[4]
    m = re.fullmatch(r'vsop2013_([a-z]+)\.bin', os.path.basename(path))
    assert m and m.group(1) == name, path + ': nama berkas tidak cocok dengan planet di header (' + name + ')'
    return name, b

# Jika dijalankan lewat Terminal dengan argumen lengkap
if len(sys.argv) >= 7:
    html, gbin, obin, tbin, abin, out = sys.argv[1:7]
    extra = sys.argv[7:]
# Jika dijalankan lewat tombol "Run" (tanpa argumen)
else:
    print("Argumen tidak diberikan, menggunakan file default...")
    html = "ASTERID.html"
    gbin = "gpt3_1.bin"
    obin = "opole_0p5.bin"
    tbin = "otl_fes2014b_1.bin"
    abin = "apl_rp_1.bin"
    out = "ASTERID_full.html"
    extra = []

try:
    s = open(html, encoding='utf8').read()
    KEYS = ('__GPT3_B64', '__OPOLE_B64', '__OTL_B64', '__APL_B64')
    assert s.count('</body>') == 1 and not any(('window.' + k + '="') in s for k in KEYS) and 'window.__VSOP_B64={' not in s
    assert s.count('</head>') == 1 and s.index('</head>') < s.index('<script')

    vs = extra or sorted(glob.glob(os.path.join(os.path.dirname(os.path.abspath(html)), 'vsop2013_*.bin')))
    assert vs, 'tidak ada vsop2013_*.bin'
    print("Membaca 4 file .bin + %d file VSOP2013 dan melakukan encode..." % len(vs))
    v = {}
    for f in vs:
        name, raw = vsop_key(f)
        assert name not in v, 'planet ganda: ' + name
        v[name] = base64.b64encode(raw).decode()
    b = [base64.b64encode(open(f, 'rb').read()).decode() for f in (gbin, obin, tbin, abin)]

    print("Menggabungkan ke dalam HTML...")
    i = s.rindex('</body>')
    s = s[:i] + '<script>' + ''.join('window.' + k + '="' + x + '";' for k, x in zip(KEYS, b)) + '</script>\n' + s[i:]
    # VSOP2013 di <head>: kode planet meminta .bin saat start-up, sebelum skrip di akhir <body> jalan (muat gagal, status tetap 'fail')
    i = s.index('</head>')
    s = s[:i] + '<script>window.__VSOP_B64=' + json.dumps(v, separators=(',', ':')) + ';</script>\n' + s[i:]

    open(out, 'w', encoding='utf8', newline='').write(s)
    print("VSOP2013 tertanam:", ', '.join(sorted(v, key=lambda n: list(NM.values()).index(n))))
    if len(v) < 7:
        print("PERINGATAN: hanya %d dari 7 planet tertanam. Di luar 500–2498 CE planet yang tidak tertanam tidak ditampilkan (tidak ada cadangan); di dalam rentang itu ia memakai IPS2000." % len(v))
    print("Selesai:", out, round(len(s.encode('utf8')) / 2**20, 2), 'MiB')

except FileNotFoundError as e:
    print(f"Error: File tidak ditemukan. Pastikan semua file ada di folder 'aster'. Detail: {e}")
