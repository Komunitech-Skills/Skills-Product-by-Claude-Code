#!/usr/bin/env python3
"""Uji regresi rekonsiliasi.py. Jalankan: python3 tests/uji_regresi.py (dari folder skill).

Data di tests/data/ adalah data FIKTIF dari uji independen (bukan data nasabah).
"""
import json
import os
import subprocess
import sys
import tempfile
import atexit

DIR = os.path.dirname(os.path.abspath(__file__))
SCRIPT = os.path.join(DIR, "..", "scripts", "rekonsiliasi.py")
DATA = os.path.join(DIR, "data")
GAGAL = []

BCA = ["--bank-tanggal", "Tanggal Transaksi", "--bank-keterangan", "Keterangan", "--bank-nominal", "Jumlah",
       "--bank-dk", "kolom_5"]


def jalankan(*arg):
    p = subprocess.run([sys.executable, SCRIPT] + list(arg), capture_output=True, text=True)
    return p.returncode, (json.loads(p.stdout) if p.returncode == 0 else json.loads(p.stderr or "{}"))


def d(nama):
    return os.path.join(DATA, nama)


def tmp(teks):
    f = tempfile.NamedTemporaryFile("w", suffix=".csv", delete=False, encoding="utf-8")
    f.write(teks)
    f.close()
    atexit.register(os.remove, f.name)
    return f.name


def cek(nama, kondisi):
    print(("OK   " if kondisi else "GAGAL") + " " + nama)
    if not kondisi:
        GAGAL.append(nama)


def pasangan(h):
    """{ref/nama catatan: (status, [keterangan bank])}"""
    out = {}
    for x in h["detail"]:
        for c in x["catatan"]:
            out[c["ref"] or c["nama"]] = (x["status"], [b["keterangan"] for b in x["bank"]], x["alasan"])
    return out


# S1 BCA: nama tidak boleh tertukar; rincian selisih +0,6 jt −0,662 jt +2,0065 jt
k, h = jalankan("cocokkan", "--bank", d("mutasi-bca-sept.csv"), "--catatan", d("penjualan-sept.csv"), *BCA,
                "--catat-tanggal", "Tanggal", "--catat-nominal", "Total", "--catat-ref", "No Invoice",
                "--catat-nama", "Pelanggan", "--catat-status", "Status", "--catat-metode", "Metode")
p = h["ringkasan"]["penjelasan_selisih"]
cek("S1 berjalan", k == 0)
cek("S1 tidak ada di bank = 600.000", p["dari_catatan_tidak_ada_di_bank"] == 600000)
cek("S1 tidak ada di catatan = -662.346", p["dari_bank_tidak_ada_di_catatan"] == -662346)
cek("S1 selisih parsial = 2.006.500", p["dari_selisih_nominal_cocok_parsial"] == 2006500)
cek("S1 rumus seimbang + catatan bukan bukti", p["cek_rumus_seimbang"] and "BUKAN bukti" in p["catatan_seimbang"])
ps = pasangan(h)
cek("S1 Dewi dipasang ke transfer DEWI", "DEWI" in " ".join(ps["INV-106"][1]))
cek("S1 Hendra dipasang ke transfer HENDRA (bayar sebagian)",
    "HENDRA" in " ".join(ps["INV-107"][1]) and ps["INV-107"][0] == "PARSIAL")
cek("S1 Andi Saputra tidak dipasang ke ANDIKA", ps["INV-112"][0] == "TIDAK ADA DI BANK")
cek("S1 PEND dilaporkan terpisah", len(h["transaksi_tertunda_pend"]) == 1
    and h["transaksi_tertunda_pend"][0]["nominal"] == 450000)

# S2 Mandiri: dua kolom "Description"; FAJAR tidak boleh ke Yulia; bunga dikenali
k, h = jalankan("cocokkan", "--bank", d("mutasi-mandiri-agustus.csv"), "--catatan", d("invoice-agustus.csv"),
                "--bank-tanggal", "Date", "--bank-keterangan", "Description", "--bank-keterangan", "Description_2",
                "--bank-debet", "Debit", "--bank-kredit", "Credit", "--catat-tanggal", "Tanggal",
                "--catat-nominal", "Grand Total", "--catat-ref", "No", "--catat-nama", "Nama Pelanggan")
ps = pasangan(h)
cek("S2 Yulia tidak dipasang ke FAJAR", not any("FAJAR" in x for x in ps["202"][1]))
cek("S2 Fajar dipasang ke FAJAR", any("FAJAR" in x for x in ps["207"][1]))
cek("S2 QRIS: alasan biaya merchant", "merchant" in ps["208"][2])
cek("S2 bunga jasa giro dikenali", any("BUNGA JASA GIRO" in b["keterangan"] and "bunga" in x["alasan"]
                                       for x in h["detail"] for b in x["bank"]))
cek("S2 nomor rekening disamarkan", not any("1234567890123" in b["keterangan"] for x in h["detail"] for b in x["bank"]))

# Ref numerik tidak menempel ke nominal; 2e dibatasi (bank 3,5x catatan tidak dipasang)
bank = tmp("Tanggal Transaksi,Keterangan,Cabang,Jumlah,,Saldo\n"
           "'10/09,TRSF E-BANKING CR 1009/FTSCY/WS95062 1050000.00 SITI AMINAH,'0000,\"1,050,000.00\",CR,\"1\"\n"
           "'11/09,TRSF E-BANKING CR BUDI HARTONO,'0000,\"1,050,000.00\",CR,\"1\"\n")
cat = tmp("Tanggal,No,Pelanggan,Total\n09/09/2026,105,Bambang,300000\n10/09/2026,106,Budi Hartono,300000\n")
k, h = jalankan("cocokkan", "--bank", bank, "--catatan", cat, *BCA, "--catat-tanggal", "Tanggal",
                "--catat-nominal", "Total", "--catat-ref", "No", "--catat-nama", "Pelanggan", "--tahun", "2026")
ps = pasangan(h)
cek("ref '105' tidak cocok dengan angka 1050000.00", ps["105"][0] == "TIDAK ADA DI BANK")
cek("2e: nama cocok tapi bank 3,5x catatan tidak dipasang", ps["106"][0] == "TIDAK ADA DI BANK")

# --toleransi-nominal > 0 tetap seimbang
k, h = jalankan("cocokkan", "--bank", d("mutasi-bri-okt.csv"), "--catatan", d("jual-okt.csv"),
                "--bank-tanggal", "TGL_TRAN", "--bank-keterangan", "DESK_TRAN", "--bank-debet", "MUTASI_DEBET",
                "--bank-kredit", "MUTASI_KREDIT", "--catat-tanggal", "Tanggal", "--catat-nominal", "Total",
                "--catat-ref", "No", "--catat-nama", "Pelanggan", "--toleransi-nominal", "200")
cek("toleransi-nominal 200: rumus seimbang", h["ringkasan"]["penjelasan_selisih"]["cek_rumus_seimbang"])

# Arah keluar: alasan tidak menyebut penjualan/pemasukan
k, h = jalankan("cocokkan", "--bank", d("mutasi-bri-okt-keluar.csv"), "--catatan", d("pembelian-okt.csv"),
                "--bank-tanggal", "TGL_TRAN", "--bank-keterangan", "DESK_TRAN", "--bank-debet", "MUTASI_DEBET",
                "--bank-kredit", "MUTASI_KREDIT", "--catat-tanggal", "Tanggal", "--catat-nominal", "Jumlah",
                "--catat-ref", "No Faktur", "--catat-nama", "Supplier", "--arah", "keluar")
teks = " ".join(x["alasan"] for x in h["detail"])
cek("arah keluar: tidak ada kata 'penjualan'/'pemasukan'", "penjualan" not in teks and "pemasukan" not in teks)
cek("arah keluar: rumus seimbang", h["ringkasan"]["penjelasan_selisih"]["cek_rumus_seimbang"])

# deteksi: saldo bukan nominal; kolom Supplier dikenali sebagai nama
k, h = jalankan("deteksi", "--bank", d("mutasi-bri-okt.csv"), "--catatan", d("pembelian-okt.csv"))
cek("deteksi BRI: nominal bukan kolom saldo", h["bank"]["kolom_terdeteksi"].get("nominal") != "SALDO_AKHIR_MUTASI")
cek("deteksi: Supplier = nama", h["catatan"]["kolom_terdeteksi"].get("nama") == "Supplier")

# Kemungkinan tertukar: nominal & tanggal sama, keterangan memuat nama catatan lain yang belum terpasang
bank = tmp("Tanggal,Keterangan,Kredit\n05/09/2026,TRF DARI WAWAN,500000\n")
cat = tmp("Tanggal,Pelanggan,Total\n05/09/2026,Yuni,500000\n20/09/2026,Wawan,200000\n")
k, h = jalankan("cocokkan", "--bank", bank, "--catatan", cat, "--bank-tanggal", "Tanggal",
                "--bank-keterangan", "Keterangan", "--bank-kredit", "Kredit", "--catat-tanggal", "Tanggal",
                "--catat-nominal", "Total", "--catat-nama", "Pelanggan")
ps = pasangan(h)
cek("nama lain di keterangan → PARSIAL 'KEMUNGKINAN TERTUKAR', bukan COCOK",
    ps["Yuni"][0] == "PARSIAL" and "TERTUKAR" in ps["Yuni"][2] and h["kemungkinan_tertukar"] == 1)

print(f"\n{'SEMUA LULUS' if not GAGAL else str(len(GAGAL)) + ' GAGAL'}")
sys.exit(1 if GAGAL else 0)
