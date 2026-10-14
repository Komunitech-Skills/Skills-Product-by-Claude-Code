#!/usr/bin/env python3
"""Uji regresi proyeksi_kas.py. Jalankan: python3 tests/uji_regresi.py (dari folder skill).

Hanya library standar; membuat file sementara di folder temp sistem lalu menghapusnya.
"""
import json
import os
import subprocess
import sys
import tempfile

SCRIPT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "scripts", "proyeksi_kas.py")
GAGAL = []


def jalankan(csv_teks, *arg):
    with tempfile.TemporaryDirectory() as d:
        f = os.path.join(d, "rencana.csv")
        with open(f, "w", encoding="utf-8") as h:
            h.write(csv_teks)
        p = subprocess.run([sys.executable, SCRIPT, f] + list(arg), capture_output=True, text=True)
        return p.returncode, (json.loads(p.stdout) if p.returncode == 0 else json.loads(p.stderr))


def cek(nama, kondisi):
    print(("OK   " if kondisi else "GAGAL") + " " + nama)
    if not kondisi:
        GAGAL.append(nama)


CONTOH = """minggu;jenis;kategori;nominal;keterangan;kritis
semua;masuk;Penjualan tunai;12.000.000;;
9;masuk;Pelunasan piutang;15.000.000;PT Sinar;
semua;keluar;Bahan baku (supplier);7.000.000;;ya
tgl:25;keluar;Gaji karyawan;18.000.000;;ya
tgl:1;keluar;Sewa;6.500.000;;ya
tgl:10;keluar;Cicilan bank;4.250.000;;ya
5;keluar;Renovasi etalase;9.000.000;;tidak
"""

# 1. Contoh SKILL.md: angka tetap
k, h = jalankan(CONTOH, "--saldo-awal", "20jt", "--mulai", "2026-10-05")
r = h["ringkasan"]
cek("contoh: saldo minggu 8 = 0", h["per_minggu"][7]["saldo_akhir"] == 0)
cek("contoh: batas aman default 14.326.923", h["asumsi_dan_sumber"]["batas_aman"] == 14326923)
cek("contoh: defisit struktural terdeteksi", r["defisit_struktural"] and r["arus_kas_bersih"] == -15250000)
op = {o["opsi"].split(" ")[0]: o for o in h["simulasi_opsi"]}
cek("contoh: supplier saldo terendah 14.000.000", op["Negosiasi"]["saldo_terendah_baru"] == 14000000)
cek("contoh: supplier tertunda 14.000.000, setelah dibayar 4.750.000",
    op["Negosiasi"]["jatuh_setelah_horizon"] == 14000000 and op["Negosiasi"]["saldo_setelah_kewajiban_tertunda"] == 4750000)
cek("contoh: supplier bukan hanya_menunda", op["Negosiasi"]["hanya_menunda"] is False)
cek("contoh: gabungan 18.750.000", op["Gabungan"]["saldo_terendah_baru"] == 18750000)
cek("contoh: peringatan cicilan jatuh setelah horizon",
    any("Cicilan bank" in p and "setelah periode" in p for p in h["peringatan"]))

# 2. Pos wajib selalu kritis, bonus bukan non-kritis
WAJIB = """minggu;jenis;kategori;nominal;kritis
semua;masuk;Penjualan;2jt;
3;keluar;Cicilan mesin jahit;2jt;
4;keluar;Pajak kendaraan (STNK);1jt;
5;keluar;Angsuran leasing kendaraan;3jt;
6;keluar;Gaji dan bonus;10jt;
7;keluar;Bonus akhir tahun karyawan;4jt;
8;keluar;THR karyawan;6jt;tidak
9;keluar;Renovasi dapur;8jt;
10;keluar;Iklan Meta;1jt;
"""
k, h = jalankan(WAJIB, "--saldo-awal", "1jt")
tunda = [o for o in h["simulasi_opsi"] if o["opsi"].startswith("Tunda")]
digeser = {x["kategori"] for o in tunda for x in o["rincian_digeser"]}
for pos in ("Cicilan mesin jahit", "Pajak kendaraan (STNK)", "Angsuran leasing kendaraan", "Gaji dan bonus",
            "Bonus akhir tahun karyawan", "THR karyawan"):
    cek(f"wajib tidak digeser: {pos}", pos not in digeser)
cek("non-kritis tebakan digeser: Renovasi dapur", "Renovasi dapur" in digeser)
cek("peringatan THR ditandai 'tidak' tetap kritis", any("THR karyawan" in p and "KRITIS" in p for p in h["peringatan"]))
cek("peringatan daftar ditebak tidak kritis",
    any("DITEBAK tidak kritis" in p and "Renovasi dapur" in p and "Iklan Meta" in p for p in h["peringatan"]))

# 3. hanya_menunda: kewajiban didorong ke luar horizon tanpa menyelesaikan masalah
TUNDA = """minggu;jenis;kategori;nominal
semua;masuk;Penjualan;5jt
semua;keluar;Belanja stok bahan;6jt
"""
k, h = jalankan(TUNDA, "--saldo-awal", "10jt", "--batas-aman", "0")
o = [x for x in h["simulasi_opsi"] if x["opsi"].startswith("Negosiasi")][0]
cek("hanya_menunda: saldo terendah tampak aman", o["saldo_terendah_baru"] >= 0)
cek("hanya_menunda: label true & saldo setelah tertunda negatif",
    o["hanya_menunda"] is True and o["saldo_setelah_kewajiban_tertunda"] < 0)
cek("defisit struktural (-13 jt)", h["ringkasan"]["defisit_struktural"] and h["ringkasan"]["arus_kas_bersih"] == -13000000)

# 4. Format minggu versi awam
AWAM = """minggu;kategori;nominal
minggu 6;Penjualan;1jt
minggu ke-3;Penjualan;2jt
mg 1-2;Penjualan;3jt
setiap 2 minggu mulai minggu 3;Penjualan;4jt
"""
k, h = jalankan(AWAM, "--saldo-awal", "0")
m = [x["masuk"] for x in h["per_minggu"]]
cek("format awam diterima tanpa baris dilewati", k == 0 and not h["baris_dilewati"])
cek("format awam: nilai per minggu", m[:7] == [3000000, 3000000, 6000000, 0, 4000000, 1000000, 4000000])

# 5. Jumlah minggu & error
k, h = jalankan(TUNDA, "--saldo-awal", "10jt", "--jumlah-minggu", "26")
cek("26 minggu", k == 0 and len(h["per_minggu"]) == 26)
k, h = jalankan(TUNDA, "--saldo-awal", "10jt", "--jumlah-minggu", "3")
cek("3 minggu ditolak", k == 2)
k, h = jalankan("a;b\n1;2\n", "--saldo-awal", "0")
cek("kolom hilang ditolak", k == 2 and "Kolom wajib" in h["error"])
k, h = jalankan(CONTOH, "--saldo-awal", "abc")
cek("saldo rusak ditolak", k == 2)

# v1.0.3 (uji OpenClaw 2026-10-01): narasi salah minggu cicilan → script mencetak kejadian per minggu.
# Mulai Senin 5 Okt 2026: tgl 10 → minggu 1 (5–11 Okt), 6 (9–15 Nov), 10 (7–13 Des);
# tgl 25 → minggu 3 (19–25 Okt), 8 (23–29 Nov), 12 (21–27 Des).
k, h = jalankan(CONTOH, "--saldo-awal", "20jt", "--mulai", "2026-10-05")
pm = h["per_minggu"]
cicilan = [m["minggu"] for m in pm if any(x["kategori"] == "Cicilan bank" for x in m["kejadian"]["keluar"])]
gaji = [m["minggu"] for m in pm if any(x["kategori"] == "Gaji karyawan" for x in m["kejadian"]["keluar"])]
cek("kejadian: cicilan di minggu 1, 6, 10", cicilan == [1, 6, 10])
cek("kejadian: gaji di minggu 3, 8, 12", gaji == [3, 8, 12])
cek("kejadian_teks minggu 12 menyebut gaji, bukan cicilan",
    "Gaji karyawan Rp 18.000.000" in pm[11]["kejadian_teks"] and "Cicilan" not in pm[11]["kejadian_teks"])
cek("kejadian diurutkan nominal terbesar dulu",
    [x["nominal"] for x in pm[7]["kejadian"]["keluar"]]
    == sorted([x["nominal"] for x in pm[7]["kejadian"]["keluar"]], reverse=True))
cek("kejadian_minggu_kritis memuat minggu saldo terendah",
    any(t.startswith("Minggu %d:" % h["ringkasan"]["minggu_saldo_terendah"])
        for t in h["ringkasan"]["kejadian_minggu_kritis"]))
cek("jumlah kejadian keluar = total keluar per minggu",
    all(sum(x["nominal"] for x in m["kejadian"]["keluar"]) == m["keluar"] for m in pm))
with tempfile.TemporaryDirectory() as d:
    f = os.path.join(d, "r.csv")
    with open(f, "w", encoding="utf-8") as fh:
        fh.write(CONTOH)
    out = subprocess.run([sys.executable, SCRIPT, f, "--saldo-awal", "20jt", "--mulai", "2026-10-05",
                          "--format", "teks"], capture_output=True, text=True).stdout
cek("format teks mencetak 'Kejadian per minggu'", "Kejadian per minggu" in out and "- Minggu 10: keluar:" in out)

# ---------------------------------------------------------------- v1.0.5 (uji OpenClaw 2026-10-14)
# (a) pemisah CSV: ';' berlebih di akhir baris membuat Sniffer gagal → seluruh file ditolak.
TRAIL = ("minggu;jenis;kategori;nominal;keterangan;kritis\n"
         "semua;masuk;Penjualan;5jt;;\n"
         "10;masuk;Pelunasan piutang;18.000.000;;;\n"
         "semua;keluar;Bahan;3jt;;;;\n"
         "4;keluar;Oli armada;9.000.000;;\n")
k, h = jalankan(TRAIL, "--saldo-awal", "12jt")
cek("pemisah: baris dengan ';' berlebih tetap dibaca (bukan 'Kolom wajib')", k == 0 and not h["baris_dilewati"])
cek("pemisah: terdeteksi titik koma", k == 0 and h["asumsi_dan_sumber"]["pemisah_input"] == "titik koma")
cek("pemisah: pelunasan 18 jt masuk minggu 10", k == 0 and h["per_minggu"][9]["masuk"] == 23000000)
k, h = jalankan("minggu;kategori;nominal;\nsemua;Penjualan;5jt;\n3;Sewa;2jt;;\n", "--saldo-awal", "1jt")
cek("pemisah: judul dengan ';' di akhir diterima", k == 0 and h["per_minggu"][2]["keluar"] == 2000000)
k, h = jalankan("minggu,kategori,nominal\nsemua,Penjualan,5000000\n3,Sewa,2000000\n", "--saldo-awal", "1jt")
cek("pemisah: koma tetap dikenali", k == 0 and h["asumsi_dan_sumber"]["pemisah_input"] == "koma"
    and h["per_minggu"][2]["keluar"] == 2000000)
k, h = jalankan("minggu\tkategori\tnominal\nsemua\tPenjualan\t5jt\n", "--saldo-awal", "1jt")
cek("pemisah: tab dikenali", k == 0 and h["asumsi_dan_sumber"]["pemisah_input"] == "tab")
k, h = jalankan("minggu,kategori,nominal\nsemua,Penjualan,5000000\n3,Pelunasan piutang,12,000,000\n",
                "--saldo-awal", "1jt")
cek("pemisah: baris kelebihan isian dilewati dengan nomor baris & isinya",
    k == 0 and h["baris_dilewati"] and h["baris_dilewati"][0]["baris"] == 3
    and "12,000,000" in h["baris_dilewati"][0]["isi"] and "lebih banyak" in h["baris_dilewati"][0]["alasan"])
k, h = jalankan("tanggal;keterangan;masuk;keluar\n2026-10-20;jual;5jt;\n", "--saldo-awal", "1jt")
cek("pemisah: galat kolom wajib menyebut baris judul & kolom terbaca",
    k == 2 and "Kolom wajib" in h["error"] and h["detail"]["baris_judul"] == 1
    and h["detail"]["kolom_terbaca"] == ["tanggal", "keterangan", "masuk", "keluar"])


def jalankan_berkas(csv_teks, berkas_lain, *arg):
    """Seperti jalankan(), plus berkas tambahan {nama: isi}; '{d}' di argumen diganti folder sementara."""
    with tempfile.TemporaryDirectory() as d:
        f = os.path.join(d, "rencana.csv")
        with open(f, "w", encoding="utf-8") as fh:
            fh.write(csv_teks)
        for nama, isi in berkas_lain.items():
            with open(os.path.join(d, nama), "w", encoding="utf-8") as fh:
                fh.write(isi)
        p = subprocess.run([sys.executable, SCRIPT, f] + [x.replace("{d}", d) for x in arg],
                           capture_output=True, text=True)
        keluaran = p.stdout if p.returncode == 0 else p.stderr
        try:
            return p.returncode, json.loads(keluaran)
        except ValueError:
            return p.returncode, keluaran


# Hitungan independen (tanpa script): mulai Senin 5 Okt 2026 → tgl 25 di minggu 3, 8, 12;
# tgl 1 di minggu 4, 9, 13; tgl 10 di minggu 1, 6, 10; tgl 15 di minggu 2, 6, 11.
def saldo_manual(saldo, masuk, keluar):
    hasil = []
    for w in range(1, 14):
        saldo += masuk.get(w, 0) - keluar.get(w, 0)
        hasil.append(saldo)
    return hasil


def tambah(d, minggu, nominal):
    for w in minggu:
        d[w] = d.get(w, 0) + nominal


BASIS_MASUK, BASIS_KELUAR = {}, {}
tambah(BASIS_MASUK, range(1, 14), 12000000)
tambah(BASIS_MASUK, [9], 15000000)
tambah(BASIS_KELUAR, range(1, 14), 7000000)
tambah(BASIS_KELUAR, [3, 8, 12], 18000000)
tambah(BASIS_KELUAR, [4, 9, 13], 6500000)
tambah(BASIS_KELUAR, [1, 6, 10], 4250000)


def salin(d):
    return dict(d)


# (b) beberapa opsi dalam SATU panggilan, keluaran ringkas per opsi
ARG = ["--saldo-awal", "20jt", "--mulai", "2026-10-05", "--ringkas"]
k, h = jalankan(CONTOH, *ARG,
                "--opsi", "Tunda renovasi | geser Renovasi etalase ke minggu 9",
                "--opsi", "pinjaman 20jt minggu 2",
                "--opsi", "Hemat bahan | kurangi Bahan baku 10%; tambah keluar Cicilan KUR 1,8jt tgl:15")
op = h.get("opsi_pengguna", []) if k == 0 else []
cek("opsi: 3 opsi dihitung dalam satu panggilan", k == 0 and len(op) == 3 and not any(o.get("error") for o in op))
cek("opsi: tiap opsi punya titik terendah, minggu minus, saldo akhir",
    all({"saldo_terendah", "minggu_terendah", "minggu_negatif", "saldo_akhir", "deskripsi", "ringkasan_teks"} <= set(o)
        for o in op))
cek("opsi: --ringkas tanpa per_minggu/per_kategori", k == 0 and "per_minggu" not in h and "per_kategori" not in h)
m1, k1 = salin(BASIS_MASUK), salin(BASIS_KELUAR)
tambah(k1, [9], 9000000)
cek("opsi 1 (renovasi ke minggu 9) = hitungan manual",
    len(op) == 3 and op[0]["saldo_akhir_per_minggu"] == saldo_manual(20000000, m1, k1)
    and op[0]["saldo_akhir_per_minggu"][7] == 9000000)
m2, k2 = salin(BASIS_MASUK), salin(BASIS_KELUAR)
tambah(k2, [5], 9000000)
tambah(m2, [2], 20000000)
cek("opsi 2 (pinjaman 20 jt minggu 2) = hitungan manual, terendah minggu 8 Rp 20 jt",
    len(op) == 3 and op[1]["saldo_akhir_per_minggu"] == saldo_manual(20000000, m2, k2)
    and op[1]["minggu_terendah"] == 8 and op[1]["saldo_terendah"] == 20000000)
cek("opsi 2: bentuk singkat ditebak sebagai PEMASUKAN", len(op) == 3 and op[1]["deskripsi"][0].startswith("Pemasukan baru"))
m3, k3 = salin(BASIS_MASUK), salin(BASIS_KELUAR)
tambah(k3, [5], 9000000)
tambah(k3, range(1, 14), -700000)
tambah(k3, [2, 6, 11], 1800000)
s3 = saldo_manual(20000000, m3, k3)
cek("opsi 3 (bahan -10% + cicilan KUR tgl 15) = hitungan manual",
    len(op) == 3 and op[2]["saldo_akhir_per_minggu"] == s3 and op[2]["saldo_terendah"] == min(s3) == 2000000
    and op[2]["saldo_akhir"] == s3[-1] == 8450000)

# (c) deskripsi opsi menyebut persis pos, nominal, minggu asal → tujuan
cek("deskripsi opsi 1 persis", len(op) == 3 and op[0]["deskripsi"] == ["Renovasi etalase Rp 9.000.000: minggu 5 → minggu 9"])
cek("deskripsi opsi 3 menyebut kedua perubahan",
    len(op) == 3 and op[2]["deskripsi"] == [
        "Bahan baku (supplier): Rp 7.000.000 → Rp 6.300.000 di minggu 1–13 (13 kali; total pengeluaran berkurang Rp 9.100.000)",
        "Pengeluaran baru: Cicilan KUR Rp 1.800.000 di minggu 2, 6, 11 (3 kali, total Rp 5.400.000)"])
cek("ringkasan_teks memuat deskripsi + hasil",
    len(op) == 3 and "minggu 5 → minggu 9" in op[0]["ringkasan_teks"]
    and "titik terendah minggu 13" in op[0]["ringkasan_teks"] and "minggu minus: tidak ada" in op[0]["ringkasan_teks"])
cek("rincian menyebut nomor baris CSV", len(op) == 3 and op[0]["rincian"][0]["baris"] == 8)

# Opsi bawaan "percepat piutang" yang memajukan DUA pembayaran: deskripsi wajib menyebut keduanya.
DUA = """minggu;jenis;kategori;nominal;keterangan
semua;masuk;Penjualan;9jt;
5;masuk;Pelunasan piutang;11jt;DP hampers
13;masuk;Pelunasan piutang;11jt;pelunasan hampers
semua;keluar;Bahan;4,5jt;
3;keluar;Mixer;15jt;
"""
k, h = jalankan(DUA, "--saldo-awal", "2jt", "--batas-aman", "10jt")
pp = [o for o in h["simulasi_opsi"] if o["opsi"].startswith("Percepat")] if k == 0 else []
cek("bawaan piutang: deskripsi menyebut kedua pembayaran",
    len(pp) == 1 and pp[0]["jumlah_pos_digeser"] == 2 and pp[0]["deskripsi"] == [
        "Pelunasan piutang (DP hampers) Rp 11.000.000: minggu 5 → minggu 3",
        "Pelunasan piutang (pelunasan hampers) Rp 11.000.000: minggu 13 → minggu 11"])
cek("bawaan piutang: catatan memperingatkan lebih dari satu pembayaran",
    len(pp) == 1 and "2 pembayaran sekaligus" in pp[0]["catatan"])
cek("bawaan piutang: rincian_digeser memuat nomor baris", len(pp) == 1
    and [r["baris"] for r in pp[0]["rincian_digeser"]] == [3, 4])
k, h = jalankan(DUA, "--saldo-awal", "2jt", "--batas-aman", "10jt",
                "--opsi", "Hanya DP | percepat Pelunasan piutang dari minggu 5 ke minggu 3")
o = h["opsi_pengguna"][0] if k == 0 else {}
cek("opsi per pos: hanya DP yang dimajukan", o.get("deskripsi") == [
    "Pelunasan piutang (DP hampers) Rp 11.000.000: minggu 5 → minggu 3"])

# Pengaman & batas
k, h = jalankan(CONTOH, *ARG, "--opsi", "tunda gaji 1 minggu", "--opsi", "geser Bahan ke minggu 9",
                "--opsi", "hapus Renovasi")
op = h.get("opsi_pengguna", []) if k == 0 else []
cek("gaji tidak boleh digeser (galat per opsi, bukan seluruh run)",
    k == 0 and "kewajiban kritis" in op[0].get("error", "") and not op[2].get("error"))
cek("pos berulang tanpa 'dari minggu' → galat jelas", len(op) == 3 and "ada di 13 minggu" in op[1].get("error", ""))
cek("hapus: deskripsi", len(op) == 3 and op[2]["deskripsi"] == [
    "Renovasi etalase Rp 9.000.000 di minggu 5 dihapus (tidak jadi dikeluarkan)"])
k, h = jalankan(CONTOH, *ARG, "--opsi", "hapus Mesin press")
cek("pos tidak ada → galat menyebut pos yang ada", k == 0 and "Pos yang ada" in h["opsi_pengguna"][0]["error"])
k, h = jalankan(CONTOH, *ARG, *sum([["--opsi", "hapus Renovasi"] for _ in range(6)], []))
cek("maks. 4 opsi; sisanya dilaporkan", k == 0 and len(h["opsi_pengguna"]) == 4
    and any("2 opsi lain TIDAK dihitung" in p for p in h["peringatan"]))
k, h = jalankan(CONTOH, *ARG, "--opsi", "Tunda jauh | tunda Renovasi etalase 10 minggu")
o = h["opsi_pengguna"][0] if k == 0 else {}
cek("geser ke luar periode: kewajiban tertunda dihitung",
    o.get("jatuh_setelah_horizon") == 9000000 and o.get("saldo_setelah_kewajiban_tertunda") == o.get("saldo_akhir", 0) - 9000000
    and o.get("deskripsi") == ["Renovasi etalase Rp 9.000.000: minggu 5 → setelah minggu 13"])
k, h = jalankan(CONTOH, *ARG, "--opsi", "Cicil | cicil Renovasi 3 kali mulai minggu 5 setiap 4 minggu")
o = h["opsi_pengguna"][0] if k == 0 else {}
cek("cicil: dibagi rata, jumlah tetap", [r["nominal_baru"] for r in o.get("rincian", [])] == [3000000] * 3
    and [r["ke_minggu"] for r in o.get("rincian", [])] == [5, 9, 13])
k, h = jalankan("minggu;kategori;nominal\nsemua;Penjualan;5jt\n2;Mesin;10jt\n", "--saldo-awal", "1jt",
                "--opsi", "cicil Mesin 3 kali mulai minggu 2")
o = h["opsi_pengguna"][0] if k == 0 else {}
cek("cicil: sisa pembulatan di cicilan terakhir", [r["nominal_baru"] for r in o.get("rincian", [])]
    == [3333333, 3333333, 3333334])
k, h = jalankan_berkas(CONTOH, {"opsi.txt": "# komentar\nTunda renovasi | tunda Renovasi etalase 4 minggu\n\n"
                                              "Batal renovasi: hapus Renovasi etalase\n"},
                       *ARG, "--file-opsi", "{d}/opsi.txt")
cek("--file-opsi: 2 opsi terbaca, label 'Nama: aksi' dikenali",
    k == 0 and [o["opsi"] for o in h["opsi_pengguna"]] == ["Tunda renovasi", "Batal renovasi"])
k, h = jalankan(CONTOH, "--saldo-awal", "20jt", "--mulai", "2026-10-05", "--terapkan", "tunda Renovasi etalase 4 minggu")
cek("--terapkan: tabel sesudah tindakan, batas aman tetap dari rencana asli",
    k == 0 and h["per_minggu"][7]["saldo_akhir"] == 9000000 and h["asumsi_dan_sumber"]["batas_aman"] == 14326923
    and h["peringatan"][0].startswith("TABEL INI SUDAH MEMAKAI TINDAKAN"))
k, h = jalankan(CONTOH, "--saldo-awal", "20jt", "--mulai", "2026-10-05", "--terapkan", "tunda gaji 1 minggu")
cek("--terapkan gaji ditolak", k == 2 and "kewajiban kritis" in h["error"])
k, h = jalankan(CONTOH, *ARG, "--opsi", "Rekrut | ubah Gaji karyawan jadi 20jt")
o = h["opsi_pengguna"][0] if k == 0 else {}
cek("ubah gaji (skenario disepakati) dihitung, catatan kritis sekali saja",
    not o.get("error") and o.get("minggu_negatif") == [8, 13] and len(o.get("catatan", [])) == 1)
v = subprocess.run([sys.executable, SCRIPT, "--versi"], capture_output=True, text=True).stdout.strip()
cek("versi script 1.0.5", v.endswith("1.0.5"))
with tempfile.TemporaryDirectory() as d:
    f, out = os.path.join(d, "r.csv"), os.path.join(d, "hasil.csv")
    with open(f, "w", encoding="utf-8") as fh:
        fh.write(CONTOH)
    teks = subprocess.run([sys.executable, SCRIPT, f, *ARG, "--format", "teks", "--output-csv", out,
                           "--opsi", "Tunda renovasi | geser Renovasi etalase ke minggu 9"],
                          capture_output=True, text=True).stdout
    with open(out, encoding="utf-8-sig") as fh:
        isi_csv = fh.read()
cek("format teks --ringkas: tanpa tabel, ada 'Opsi Anda'", "| Mg |" not in teks and "Opsi Anda" in teks
    and "Opsi 1 – Tunda renovasi: Renovasi etalase Rp 9.000.000: minggu 5 → minggu 9" in teks)
cek("CSV keluaran memuat baris simulasi opsi", "SIMULASI OPSI" in isi_csv and "Opsi 1: Tunda renovasi" in isi_csv)

print(f"\n{'SEMUA LULUS' if not GAGAL else str(len(GAGAL)) + ' GAGAL'}")
sys.exit(1 if GAGAL else 0)
