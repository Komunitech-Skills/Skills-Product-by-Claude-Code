#!/usr/bin/env python3
"""Uji regresi arsip.py. Jalankan: python3 tests/uji_regresi.py (dari folder skill ini).

Semua data FIKTIF, dibuat di folder sementara (tempfile), dihapus otomatis setelah selesai.
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile

DIR = os.path.dirname(os.path.abspath(__file__))
SCRIPT = os.path.join(DIR, "..", "scripts", "arsip.py")
GAGAL = []
WORK = tempfile.mkdtemp(prefix="arsip-nota-uji-")
DB = os.path.join(WORK, "data", "arsip.db")


def jalankan(*arg, db=True):
    argv = [sys.executable, SCRIPT] + list(arg)
    if db:
        argv += ["--db", DB]
    argv += ["--json"]
    p = subprocess.run(argv, capture_output=True, text=True, cwd=WORK)
    try:
        keluaran = json.loads(p.stdout or p.stderr or "{}")
    except json.JSONDecodeError:
        keluaran = {"_stdout": p.stdout, "_stderr": p.stderr}
    return p.returncode, keluaran


def cek(nama, kondisi):
    print(("OK   " if kondisi else "GAGAL") + " " + nama)
    if not kondisi:
        GAGAL.append(nama)


def buat_file(nama, isi):
    p = os.path.join(WORK, nama)
    os.makedirs(os.path.dirname(p) or WORK, exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        f.write(isi)
    return p


# ------------------------------------------------------------------ persiapan
foto1 = buat_file("in/nota1.jpg", "ISI-FOTO-NOTA-TOKO-A-001")
foto2 = buat_file("in/nota2.jpg", "ISI-FOTO-NOTA-TOKO-B-002")
foto3 = buat_file("in/nota3.pdf", "ISI-FOTO-NOTA-TOKO-C-003")
kosong = buat_file("in/kosong.jpg", "")

# 1. init tanpa --ya = pratinjau, tidak membuat file
k, h = jalankan("init")
cek("1. init pratinjau ok=True", h.get("ok") is True)
cek("2. init pratinjau mode=pratinjau", h.get("mode") == "pratinjau")
cek("3. init pratinjau belum membuat file", not os.path.exists(DB))

# 4. init --ya membuat indeks
k, h = jalankan("init", "--ya")
cek("4. init --ya tersimpan", k == 0 and h.get("mode") == "tersimpan")
cek("5. file indeks benar-benar ada", os.path.isfile(DB))

# 6. tambah tanpa --ya = pratinjau, file belum disalin
target_dugaan = os.path.join(WORK, "data", "arsip", "2026", "09",
                             "2026-09-20_Toko-Sembako-Bu-Yati_150000.jpg")
k, h = jalankan("tambah", "--file", foto1, "--tanggal", "20/09/2026", "--vendor", "Toko Sembako Bu Yati",
                "--nominal", "150000")
cek("6. tambah pratinjau ok", k == 0 and h.get("mode") == "pratinjau")
cek("7. tambah pratinjau belum menyalin file", not os.path.exists(target_dugaan))
cek("8. nama file tujuan sesuai pola tanggal_vendor_nominal", h.get("file_tujuan", "").endswith(
    "2026-09-20_Toko-Sembako-Bu-Yati_150000.jpg"))
cek("9. kategori ditebak (Bahan baku dari kata 'Sembako')", h.get("kategori") == "bahan-baku")

# 10. tambah --ya menyimpan, file sumber tetap ada (mode salin)
k, h = jalankan("tambah", "--file", foto1, "--tanggal", "20/09/2026", "--vendor", "Toko Sembako Bu Yati",
                "--nominal", "150000", "--ya")
cek("10. tambah --ya tersimpan", k == 0 and h.get("mode") == "tersimpan")
cek("11. file tujuan benar-benar ada", os.path.isfile(h.get("file_tujuan", "")))
cek("12. file sumber TIDAK terhapus (mode salin default)", os.path.isfile(foto1))
cek("13. isi file tujuan sama dengan sumber", open(h["file_tujuan"], encoding="utf-8").read() ==
    open(foto1, encoding="utf-8").read())

# 14. tambah file yang sama persis lagi -> perlu_izin duplikat, TIDAK tersimpan
k, h = jalankan("tambah", "--file", foto1, "--tanggal", "20/09/2026", "--vendor", "Toko Lain",
                "--nominal", "150000")
cek("14. duplikat persis terdeteksi (perlu_izin)", h.get("perlu_izin") == ["izinkan_duplikat"])
cek("15. duplikat: id nota lama disebut", h.get("duplikat", {}).get("id") == 1)

# 15b. BUG (v1.0.1): --ya TANPA --izinkan-duplikat dulu tidak boleh mengaku "tersimpan" - file itu
# sebenarnya tidak disalin dan tidak ada baris baru di indeks.
target_salah = os.path.join(WORK, "data", "arsip", "2026", "09", "2026-09-20_Toko-Lain_150000.jpg")
k, h = jalankan("tambah", "--file", foto1, "--tanggal", "20/09/2026", "--vendor", "Toko Lain",
                "--nominal", "150000", "--ya")
cek("15b. --ya tanpa --izinkan-duplikat: mode jujur 'diblokir_duplikat', BUKAN 'tersimpan'",
    h.get("mode") == "diblokir_duplikat")
cek("15c. --ya tanpa --izinkan-duplikat: tetap minta izin (perlu_izin)",
    h.get("perlu_izin") == ["izinkan_duplikat"])
cek("15d. --ya tanpa --izinkan-duplikat: file TIDAK ikut disalin", not os.path.exists(target_salah))
k, h = jalankan("info")
cek("15e. --ya tanpa --izinkan-duplikat: jumlah_nota TIDAK bertambah (masih 1)", h.get("jumlah_nota") == 1)

# 16. dengan --izinkan-duplikat --ya tetap bisa disimpan sebagai nota baru
k, h = jalankan("tambah", "--file", foto1, "--tanggal", "20/09/2026", "--vendor", "Toko Lain",
                "--nominal", "150000", "--izinkan-duplikat", "--ya")
cek("16. izinkan-duplikat berhasil menyimpan nota baru", k == 0 and h.get("id") == 2)

# 17. --pindah benar-benar memindahkan (sumber tidak ada lagi di lokasi lama)
k, h = jalankan("tambah", "--file", foto2, "--tanggal", "21/09/2026", "--vendor", "Toko B",
                "--nominal", "75000", "--pindah", "--ya")
cek("17. --pindah tersimpan", k == 0 and h.get("aksi") == "dipindah")
cek("18. file sumber sudah tidak ada di lokasi lama setelah --pindah", not os.path.exists(foto2))
cek("19. file tetap ada (hanya berpindah lokasi, bukan dihapus)", os.path.isfile(h.get("file_tujuan", "")))

# 20. nominal dengan satuan "rb"/"jt" dan kategori eksplisit
k, h = jalankan("tambah", "--file", foto3, "--tanggal", "22/09/2026", "--vendor", "Toko Peralatan Jaya",
                "--nominal", "1,2jt", "--kategori", "peralatan", "--ya")
cek("20. parser nominal '1,2jt' -> 1200000", h.get("nominal") == 1200000)
cek("21. kategori eksplisit dipakai apa adanya", h.get("kategori") == "peralatan")

# 22. file sumber tidak ada -> error jelas, bukan traceback
k, h = jalankan("tambah", "--file", os.path.join(WORK, "in", "tidak-ada.jpg"), "--tanggal", "20/09/2026",
                "--vendor", "X", "--nominal", "1000")
cek("22. file tidak ada -> ok=False dengan pesan error", k == 1 and h.get("ok") is False and "tidak ditemukan" in
    h.get("error", ""))

# 23. file kosong (0 byte) ditolak
k, h = jalankan("tambah", "--file", kosong, "--tanggal", "20/09/2026", "--vendor", "X", "--nominal", "1000")
cek("23. file kosong ditolak", k == 1 and "kosong" in h.get("error", ""))

# 24. tanggal masa depan ditolak
k, h = jalankan("tambah", "--file", foto1, "--tanggal", "01/01/2099", "--vendor", "X", "--nominal", "1000")
cek("24. tanggal masa depan ditolak", k == 1 and "masa depan" in h.get("error", ""))

# 25. tanggal tanpa tahun 4 digit ditolak (ambigu)
k, h = jalankan("tambah", "--file", foto1, "--tanggal", "20/09/26", "--vendor", "X", "--nominal", "1000")
cek("25. tanggal tahun 2 digit ditolak", k == 1 and "tahun" in h.get("error", "").lower())

# 26. nominal bukan angka ditolak
k, h = jalankan("tambah", "--file", foto1, "--tanggal", "20/09/2026", "--vendor", "X", "--nominal", "sekian")
cek("26. nominal tidak dikenali ditolak", k == 1 and "tidak dikenali" in h.get("error", ""))

# 27. nominal desimal dibulatkan + diberi peringatan
k, h = jalankan("tambah", "--file", buat_file("in/nota-desimal.jpg", "DESIMAL"), "--tanggal", "23/09/2026",
                "--vendor", "Toko Desimal", "--nominal", "10000.50", "--ya")
cek("27. nominal desimal dibulatkan ke rupiah terdekat", h.get("nominal") == 10001)
cek("28. peringatan pembulatan disebutkan", any("dibulatkan" in p for p in h.get("peringatan", [])))

# ------------------------------------------------------------------ cari & rekap & duplikat
k, h = jalankan("cari", "--vendor", "Toko Sembako Bu Yati")
cek("29. cari --vendor menemukan nota", h.get("jumlah") == 1 and h["nota"][0]["nominal"] == 150000)

k, h = jalankan("cari", "--nominal-min", "1000000")
cek("30. cari --nominal-min menyaring nominal besar saja", h.get("jumlah") == 1 and
    h["nota"][0]["vendor"] == "Toko Peralatan Jaya")

k, h = jalankan("cari", "--cari", "tidakketemu9999")
cek("31. cari kata yang tidak ada -> hasil kosong, bukan error", k == 0 and h.get("jumlah") == 0)

k, h = jalankan("rekap", "--bulan", "09/2026")
total_dugaan = 150000 + 150000 + 75000 + 1200000 + 10001
cek("32. rekap bulan menjumlahkan semua nota bulan itu", h.get("total_nominal") == total_dugaan)
cek("33. rekap jumlah_nota sesuai", h.get("jumlah_nota") == 5)

k, h = jalankan("rekap", "--bulan", "01/2020")
cek("34. rekap bulan tanpa nota -> total 0, bukan error", k == 0 and h.get("total_nominal") == 0)

k, h = jalankan("duplikat")
cek("35. duplikat mendeteksi file sama persis (nota 1 & 2)",
    any(sorted(d["id_nota"]) == [1, 2] for d in h.get("file_sama_persis", [])))

# ------------------------------------------------------------------ ekspor ke kas-umkm
csv_keluar = os.path.join(WORK, "ekspor.csv")
k, h = jalankan("ekspor", "--bulan", "09/2026", "--csv", csv_keluar)
cek("36. ekspor berhasil membuat file CSV", k == 0 and os.path.isfile(csv_keluar))
isi_csv = open(csv_keluar, encoding="utf-8-sig").read()
cek("37. header CSV sesuai format kas-umkm (Tanggal;Keterangan;Masuk;Keluar;Kategori)",
    isi_csv.splitlines()[0] == "Tanggal;Keterangan;Masuk;Keluar;Kategori")
cek("38. baris CSV memuat nominal di kolom Keluar", "150000" in isi_csv)

# ------------------------------------------------------------------ backup & restore
k, h = jalankan("backup", "--daftar")
cek("39. backup --daftar mengembalikan minimal satu cadangan (dibuat otomatis saat --ya)",
    k == 0 and len(h.get("cadangan", [])) >= 1)

cadangan = h["cadangan"][0]
k, h = jalankan("restore", "--dari", cadangan)
cek("40. restore tanpa --ya = pratinjau, tidak mengubah indeks", h.get("mode") == "pratinjau")

# ------------------------------------------------------------------ nama file aman lintas OS
k, h = jalankan("tambah", "--file", buat_file("in/nota-aneh.jpg", "ANEH"), "--tanggal", "24/09/2026",
                "--vendor", 'Toko "Aneh"/Test:CON*?<>|', "--nominal", "5000", "--ya")
cek("41. karakter terlarang Windows dihapus dari nama file", k == 0 and not any(
    c in os.path.basename(h["file_tujuan"]) for c in '<>:"/\\|?*'))

# ------------------------------------------------------------------ di luar cakupan / indeks belum ada
WORK2 = tempfile.mkdtemp(prefix="arsip-nota-uji2-")
DB2 = os.path.join(WORK2, "belum-ada.db")
p = subprocess.run([sys.executable, SCRIPT, "info", "--db", DB2, "--json"], capture_output=True, text=True)
h2 = json.loads(p.stdout)
cek("42. info di indeks yang belum ada -> ada=False, bukan error/traceback", h2.get("ok") is True and
    h2.get("ada") is False)

p = subprocess.run([sys.executable, SCRIPT, "cari", "--db", DB2, "--json"], capture_output=True, text=True)
h3 = json.loads(p.stdout)
cek("43. cari di indeks yang belum ada -> pesan jelas 'belum ada', bukan traceback",
    p.returncode == 1 and "belum ada" in h3.get("error", ""))
shutil.rmtree(WORK2, ignore_errors=True)

# ------------------------------------------------------------------ tebak kategori (v1.0.1: toko bangunan & BBM)
k, h = jalankan("tambah", "--file", buat_file("in/nota-bangunan.jpg", "BANGUNAN"), "--tanggal", "25/09/2026",
                "--vendor", "Toko Bangunan Sumber Rejeki", "--catatan", "beli semen 5 sak dan pasir",
                "--nominal", "450000", "--ya")
cek("45. kategori 'semen'/'pasir' ditebak sebagai Bahan baku (toko bangunan)", k == 0 and
    h.get("kategori") == "bahan-baku")

k, h = jalankan("tambah", "--file", buat_file("in/nota-bbm.jpg", "BBM"), "--tanggal", "25/09/2026",
                "--vendor", "SPBU Pertamina 34.123", "--nominal", "100000", "--ya")
cek("46. vendor 'SPBU Pertamina' ditebak sebagai Transportasi (BBM)", k == 0 and
    h.get("kategori") == "transportasi")

k, h = jalankan("tambah", "--file", buat_file("in/nota-pertalite.jpg", "PERTALITE"), "--tanggal", "25/09/2026",
                "--vendor", "Toko Kelontong Barokah", "--catatan", "isi Pertalite motor",
                "--nominal", "25000", "--ya")
cek("47. kata 'Pertalite' di catatan ditebak sebagai Transportasi (BBM)", k == 0 and
    h.get("kategori") == "transportasi")

# batas kata: 'cat' pada 'catatan'/'kecap' TIDAK boleh salah kena bahan-baku (regresi word-boundary)
k, h = jalankan("tambah", "--file", buat_file("in/nota-kecap.jpg", "KECAP"), "--tanggal", "25/09/2026",
                "--vendor", "Warung Kecap Manis Ibu Catur", "--catatan", "catatan bulanan warung",
                "--nominal", "30000", "--ya")
cek("48. 'cat' di dalam kata lain ('kecap'/'catatan') TIDAK salah tertebak Bahan baku",
    k == 0 and h.get("kategori") != "bahan-baku")
cek("49. tanpa kata kunci cocok -> jatuh ke Lain-lain", h.get("kategori") == "lain-lain")

# BP (merek SPBU) hanya cocok sebagai kata utuh, bukan substring acak
k, h = jalankan("tambah", "--file", buat_file("in/nota-atap.jpg", "ATAP"), "--tanggal", "25/09/2026",
                "--vendor", "Toko Atap Seng Makmur", "--nominal", "60000", "--ya")
cek("50. 'bp' di dalam kata 'atap' TIDAK salah tertebak Transportasi (BBM)",
    k == 0 and h.get("kategori") != "transportasi")

# ------------------------------------------------------------------ info akhir
k, h = jalankan("info")
cek("51. info akhir: jumlah_nota sesuai jumlah yang tersimpan (11)", h.get("jumlah_nota") == 11)

# ------------------------------------------------------------------ singkatan flag konfirmasi
# Regresi keamanan: argparse tidak boleh menerima singkatan (--y untuk --ya).
_db_singkat = os.path.join(WORK, "singkat", "arsip.db")
_p = subprocess.run([sys.executable, SCRIPT, "init", "--db", _db_singkat, "--y"], capture_output=True, text=True, cwd=WORK)
cek("52. singkatan flag konfirmasi (--y) ditolak dan tidak menulis apa pun",
    _p.returncode != 0 and "unrecognized arguments" in (_p.stdout + _p.stderr) and not os.path.exists(_db_singkat))

shutil.rmtree(WORK, ignore_errors=True)

print("\n" + ("SEMUA LULUS" if not GAGAL else "%d GAGAL: %s" % (len(GAGAL), ", ".join(GAGAL))))
sys.exit(1 if GAGAL else 0)
