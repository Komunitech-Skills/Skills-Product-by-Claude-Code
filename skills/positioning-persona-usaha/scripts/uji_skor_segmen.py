#!/usr/bin/env python3
"""Uji regresi skor_segmen.py. Jalankan: python3 uji_skor_segmen.py  (keluar 0 bila semua lulus)."""
import json
import os
import subprocess
import sys
import tempfile

SINI = os.path.dirname(os.path.abspath(__file__))
SCRIPT = os.path.join(SINI, "skor_segmen.py")
HEAD = "segmen,ukuran,daya_beli,kebutuhan,jangkauan_kanal,kecocokan_produk,persaingan,kemampuan_layani\n"
gagal = []


def jalan(isi, *args, nama="t.csv", bytes_=None):
    with tempfile.TemporaryDirectory() as d:
        p = os.path.join(d, nama)
        if bytes_ is not None:
            open(p, "wb").write(bytes_)
        elif isi is not None:
            open(p, "w", encoding="utf-8").write(isi)
        return subprocess.run([sys.executable, SCRIPT, p, *args], capture_output=True, text=True)


def cek(nama, kondisi, info=""):
    if not kondisi:
        gagal.append(f"{nama} {info}")


# 1. hitung manual: semua 5 -> 100; semua 1 -> 20; semua 3 -> 60
r = jalan(HEAD + "A,5,5,5,5,5,5,5\nB,1,1,1,1,1,1,1\nC,3,3,3,3,3,3,3\n", "--format", "json")
d = json.loads(r.stdout)
sk = {h["segmen"]: h["skor"] for h in d["hasil"]}
cek("semua5", sk["A"] == 100.0, sk)
cek("semua1", sk["B"] == 20.0, sk)
cek("semua3", sk["C"] == 60.0, sk)
cek("urut", [h["segmen"] for h in d["hasil"]] == ["A", "C", "B"])

# 2. hitung tangan: 4,4,4,5,5,2,4 -> (15*4+20*4+20*4+15*5+15*5+10*2+5*4)/100*20 = 410/100*20=82.0
r = jalan(HEAD + "X,4,4,4,5,5,2,4\n", "--format", "json")
cek("manual82", json.loads(r.stdout)["hasil"][0]["skor"] == 82.0, r.stdout)

# 3. bobot kustom: hanya daya_beli berbobot (yang lain 0) -> skor = 20 * nilai daya_beli
r = jalan(HEAD + "X,1,4,1,1,1,1,1\n", "--bobot",
          "ukuran=0,kebutuhan=0,jangkauan_kanal=0,kecocokan_produk=0,persaingan=0,kemampuan_layani=0,daya_beli=1",
          "--format", "json")
cek("bobot_kustom", json.loads(r.stdout)["hasil"][0]["skor"] == 80.0, r.stdout)

# 4. desimal koma & pemisah titik koma
r = jalan(HEAD.replace(",", ";") + "X;4,5;4;4;5;5;2;4\n", "--format", "json")
cek("titik_koma", r.returncode == 0 and json.loads(r.stdout)["hasil"][0]["skor"] > 82, r.stderr)

# 5. saran & titik lemah
r = jalan(HEAD + "Kuat,5,5,5,5,5,5,5\nSedang,3,3,3,3,3,3,3\nLemah,2,2,2,2,2,2,2\n")
cek("saran", "Utama" in r.stdout and "Kandidat" in r.stdout and "Tunda" in r.stdout, r.stdout)
cek("lemah", "[lemah:" in r.stdout)

# 6. tie-break: skor sama, daya beli lebih tinggi menang
r = jalan(HEAD + "P,5,1,3,3,3,3,3\nQ,1,5,3,3,3,3,3\n", "--bobot", "ukuran=20", "--format", "json")
h = json.loads(r.stdout)["hasil"]
cek("tie", h[0]["segmen"] == "Q" or h[0]["skor"] > h[1]["skor"], r.stdout)

# 7. data rusak -> kode 2 + pesan jelas, tanpa traceback
kasus = {
    "kosong": ("", "kosong"),
    "tanpa_kolom_segmen": ("nama,ukuran\nA,3\n", "segmen"),
    "kolom_kurang": ("segmen,ukuran\nA,3\n", "kurang"),
    "bukan_angka": (HEAD + "A,tinggi,3,3,3,3,3,3\n", "angka"),
    "di_luar_rentang": (HEAD + "A,6,3,3,3,3,3,3\n", "1-5"),
    "nol": (HEAD + "A,0,3,3,3,3,3,3\n", "1-5"),
    "ganda": (HEAD + "A,3,3,3,3,3,3,3\na,3,3,3,3,3,3,3\n", "ganda"),
    "nama_kosong": (HEAD + ",3,3,3,3,3,3,3\n", "kosong"),
    "hanya_judul": (HEAD, "Tidak ada baris"),
    "sel_kosong": (HEAD + "A,3,,3,3,3,3,3\n", "angka"),
}
for nama, (isi, kata) in kasus.items():
    r = jalan(isi)
    cek("rusak_" + nama, r.returncode == 2 and kata in r.stderr and "Traceback" not in r.stderr, r.stderr)
r = jalan(None, nama="tidak_ada.csv")
cek("file_hilang", r.returncode == 2 and "tidak ditemukan" in r.stderr, r.stderr)
r = jalan(None, bytes_=b"\xff\xfe\x00bad")
cek("bukan_utf8", r.returncode == 2 and "Traceback" not in r.stderr, r.stderr)
r = jalan(HEAD + "A,3,3,3,3,3,3,3\n", "--bobot", "gaib=3")
cek("kriteria_asing", r.returncode == 2 and "tidak dikenal" in r.stderr, r.stderr)
r = jalan(HEAD + "A,3,3,3,3,3,3,3\n", "--bobot", "ukuran=abc")
cek("bobot_bukan_angka", r.returncode == 2, r.stderr)
r = jalan(HEAD + "A,3,3,3,3,3,3,3\n", "--bobot", "ukuran=-5")
cek("bobot_negatif", r.returncode == 2, r.stderr)
nol = ",".join(f"{k}=0" for k in "ukuran daya_beli kebutuhan jangkauan_kanal kecocokan_produk persaingan kemampuan_layani".split())
r = jalan(HEAD + "A,3,3,3,3,3,3,3\n", "--bobot", nol)
cek("bobot_nol", r.returncode == 2, r.stderr)

# 7b. revisi v1.0.1
# B1: koma di nama segmen tanpa tanda kutip -> GAGAL jelas, bukan traceback
r = jalan(HEAD + "Ibu muda, pengajian,3,3,3,3,3,3,3\n")
cek("koma_tanpa_kutip", r.returncode == 2 and "GAGAL" in r.stderr and "tanda kutip" in r.stderr
    and "Traceback" not in r.stderr, r.stderr)
r = jalan(HEAD + '"Ibu muda, pengajian",3,3,3,3,3,3,3\n', "--format", "json")
cek("koma_berkutip", r.returncode == 0 and json.loads(r.stdout)["hasil"][0]["segmen"] == "Ibu muda, pengajian", r.stderr)
# B2: bobot inf/nan ditolak
for v in ("inf", "nan", "-inf", "1e999"):
    r = jalan(HEAD + "A,3,3,3,3,3,3,3\n", "--bobot", f"ukuran={v}")
    cek("bobot_" + v, r.returncode == 2 and "GAGAL" in r.stderr and "Traceback" not in r.stderr, r.stderr)
# B3: judul kolom ganda ditolak
r = jalan(HEAD.strip() + ",ukuran\nA,4,4,4,5,5,2,4,1\n")
cek("judul_ganda", r.returncode == 2 and "ganda" in r.stderr and "ukuran" in r.stderr, r.stderr)
# B4: bobot desimal titik diterima; koma memberi pesan yang menyebut titik
r = jalan(HEAD + "X,4,4,4,5,5,2,4\n", "--bobot", "ukuran=15.0", "--format", "json")
cek("bobot_titik", r.returncode == 0 and json.loads(r.stdout)["hasil"][0]["skor"] == 82.0, r.stderr)
r = jalan(HEAD + "X,4,4,4,5,5,2,4\n", "--bobot", "ukuran=1,5")
cek("bobot_koma", r.returncode == 2 and "titik" in r.stderr, r.stderr)
# B5: nama panjang tidak dipotong
nama = "Karyawan perantau & anak kos kerja di kawasan industri"
r = jalan(HEAD + nama + ",3,3,3,3,3,3,3\n")
cek("nama_utuh", nama in r.stdout, r.stdout)
# B6: CSV tab
r = jalan(HEAD.replace(",", "\t") + "X\t4\t4\t4\t5\t5\t2\t4\n", "--format", "json")
cek("tab", r.returncode == 0 and json.loads(r.stdout)["hasil"][0]["skor"] == 82.0, r.stderr)
# Aturan seri: 82 vs 79 (selisih 3) -> SETARA; 82 vs 77 (selisih 5 tepat) -> SETARA; 82 vs 76 (selisih 6) -> tidak
# X: 410/100*20=82; Y 4,4,4,4,4,2,4 -> (60+80+80+60+60+20+20)=380 -> 76; Z 4,4,4,5,4,2,4 -> 395 -> 79; W 4,4,4,4,5,1,4 -> 385 -> 77
r = jalan(HEAD + "X,4,4,4,5,5,2,4\nZ,4,4,4,5,4,2,4\n")
cek("seri_3", "SETARA" in r.stdout and "3 poin" in r.stdout, r.stdout)
r = jalan(HEAD + "X,4,4,4,5,5,2,4\nW,4,4,4,4,5,1,4\n", "--format", "json")
cek("seri_5_tepat", json.loads(r.stdout)["seri"] is not None, r.stdout)
r = jalan(HEAD + "X,4,4,4,5,5,2,4\nY,4,4,4,4,4,2,4\n")
cek("tidak_seri_6", "SETARA" not in r.stdout, r.stdout)
# Hitung karakter bio
r = subprocess.run([sys.executable, SCRIPT, "--hitung", "Adem dipakai seharian."], capture_output=True, text=True)
cek("hitung_polos", r.returncode == 0 and "Jumlah karakter: 22" in r.stdout and "MUAT" in r.stdout, r.stdout)
r = subprocess.run([sys.executable, SCRIPT, "--hitung", "Pesan via WA \U0001F447"], capture_output=True, text=True)
cek("hitung_emoji", "Jumlah karakter: 14" in r.stdout and "anggap panjangnya 15" in r.stdout, r.stdout)
r = subprocess.run([sys.executable, SCRIPT, "--hitung", "a" * 151], capture_output=True, text=True)
cek("hitung_panjang", "KEPANJANGAN" in r.stdout, r.stdout)
r = subprocess.run([sys.executable, SCRIPT], capture_output=True, text=True)
cek("tanpa_csv", r.returncode == 2 and "GAGAL" in r.stderr, r.stderr)

# 8. templat bawaan dapat dijalankan
r = subprocess.run([sys.executable, SCRIPT, os.path.join(SINI, "..", "templates", "segmen.csv")],
                   capture_output=True, text=True)
cek("templat", r.returncode == 0 and "Karyawati" in r.stdout, r.stderr)

if gagal:
    print("GAGAL:\n  " + "\n  ".join(gagal))
    sys.exit(1)
print("Semua uji lulus")
