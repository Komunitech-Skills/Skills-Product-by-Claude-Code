#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Uji regresi laporan_emkm.py (hanya library standar).

Jalankan: python3 uji_regresi.py   -> keluar 0 bila semua lulus.
Data uji ditulis ke folder sementara dan dihapus setelah selesai.
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile

SINI = os.path.dirname(os.path.abspath(__file__))
SCRIPT = os.path.join(SINI, "laporan_emkm.py")

DATA = {
    # 3 bulan, termasuk KUR, angsuran, kasbon, air mineral, iuran, PB1
    "tiga_bulan.csv": """Tanggal,Keterangan,Masuk,Keluar
01/01/2026,Saldo awal,"Rp 5.000.000",
03/01/2026,Penjualan nasi box,"Rp 4.000.000",
05/01/2026,Belanja bahan,,"Rp 1.500.000"
10/01/2026,Bayar listrik,,"Rp 300.000"
20/01/2026,Ambil untuk keperluan rumah tangga,,"Rp 700.000"
02/02/2026,Pencairan KUR BRI,"Rp 10.000.000",
04/02/2026,Penjualan nasi box,"Rp 3.000.000",
06/02/2026,Kulakan gas melon 10 tabung,,"Rp 200.000"
07/02/2026,Beli air mineral gelas 2 dus,,"Rp 50.000"
08/02/2026,Iuran kebersihan pasar,,"Rp 20.000"
10/02/2026,Kasbon Pak Darto,,"Rp 300.000"
12/02/2026,Bayar pajak restoran PB1,,"Rp 100.000"
02/03/2026,Angsuran KUR BRI ke-1,,"Rp 1.000.000"
05/03/2026,Penjualan nasi box,"Rp 5.000.000",
10/03/2026,Potong kasbon Pak Darto,"Rp 100.000",
""",
    "kurung.csv": """Tanggal;Keterangan;Masuk;Keluar
05/01/2026;Penjualan;1.000.000;
06/01/2026;Beli tepung;;(200.000)
07/01/2026;Koreksi;(50.000);
TOTAL;;;
""",
    "warung.csv": """Tanggal,Keterangan,Masuk,Keluar
01/08/2026,Hasil jualan,"Rp 3.000.000",
02/08/2026,Kulakan sembako,,"Rp 1.000.000"
""",
    "rugi.csv": """Tanggal,Keterangan,Masuk,Keluar
01/08/2026,Penjualan,"Rp 1.000.000",
02/08/2026,Gaji karyawan,,"Rp 1.500.000"
""",
}


def jalan(args, harap_kode=0):
    p = subprocess.run([sys.executable, SCRIPT] + args, capture_output=True, text=True, encoding="utf-8")
    if p.returncode != harap_kode:
        raise AssertionError("kode keluar {} (harap {}) untuk {}\n{}".format(p.returncode, harap_kode, args, p.stderr))
    return json.loads(p.stdout) if "--format" in args and p.returncode == 0 else p


def cek(nama, kondisi, info=""):
    if not kondisi:
        raise AssertionError("GAGAL: {} {}".format(nama, info))
    print("  ok  " + nama)


def main():
    tmp = tempfile.mkdtemp(prefix="uji-emkm-")
    try:
        for n, isi in DATA.items():
            with open(os.path.join(tmp, n), "w", encoding="utf-8") as f:
                f.write(isi)
        f3 = os.path.join(tmp, "tiga_bulan.csv")

        # --- klasifikasi (S2) & kasbon
        d = jalan([f3, "--format", "json"])
        kat = {t["keterangan"]: t["kategori"] for t in d["rincian_transaksi"]}
        cek("kulakan gas = pembelian", kat["Kulakan gas melon 10 tabung"] == "pembelian_bahan")
        cek("air mineral = pembelian", kat["Beli air mineral gelas 2 dus"] == "pembelian_bahan")
        cek("iuran kebersihan pasar = beban lain", kat["Iuran kebersihan pasar"] == "beban_lain")
        cek("PB1 = pajak daerah", kat["Bayar pajak restoran PB1"] == "beban_pajak_lain")
        cek("kasbon = piutang lain", kat["Kasbon Pak Darto"] == "piutang_lain" and
            kat["Potong kasbon Pak Darto"] == "piutang_lain")
        cek("kasbon di neraca 200.000", d["posisi_keuangan"]["aset"]["piutang_lain"] == 200000)
        # --- S1 angsuran ditanyakan, PB1 ditanyakan, status SEMENTARA
        cek("angsuran ditanyakan", any("BUNGA" in q and "Baris 14" in q for q in d["pertanyaan"]), d["pertanyaan"])
        cek("PB1 ditanyakan", any("PB1" in q for q in d["pertanyaan"]))
        cek("status SEMENTARA saat ada pertanyaan", d["status"] == "SEMENTARA")
        # kas akhir = 5.000.000 + 22.100.000 - 4.170.000
        cek("kas akhir penuh", d["posisi_keuangan"]["aset"]["kas_dan_setara_kas"] == 22930000,
            d["posisi_keuangan"]["aset"]["kas_dan_setara_kas"])
        cek("neraca seimbang", d["posisi_keuangan"]["seimbang_hitungan"])

        # --- --bunga memecah angsuran
        d = jalan([f3, "--bunga", "14=150.000", "--format", "json"])
        cek("bunga jadi beban keuangan", d["laba_rugi"]["beban_keuangan"] == 150000)
        cek("utang bank = 10jt - 850rb", d["posisi_keuangan"]["liabilitas"]["utang_bank_pinjaman"] == 9150000)
        cek("angsuran tidak ditanyakan lagi", not any("BUNGA" in q for q in d["pertanyaan"]))
        cek("seimbang setelah --bunga", d["posisi_keuangan"]["seimbang_hitungan"])
        jalan([f3, "--bunga", "14=2jt"], harap_kode=1)
        jalan([f3, "--bunga", "3=1000"], harap_kode=1)

        # --- B1 penggulungan saldo awal
        d = jalan([f3, "--periode-awal", "2026-02-01", "--periode-akhir", "2026-02-28", "--format", "json"])
        # kas awal Feb = 5.000.000 + 4.000.000 - 2.500.000 = 6.500.000
        cek("B1 kas awal Februari digulirkan", d["saldo_awal"]["kas"] == 6500000, d["saldo_awal"]["kas"])
        # kas akhir Feb = 6.500.000 + 13.000.000 - 670.000
        cek("B1 kas akhir Februari", d["posisi_keuangan"]["aset"]["kas_dan_setara_kas"] == 18830000,
            d["posisi_keuangan"]["aset"]["kas_dan_setara_kas"])
        cek("B1 modal awal Feb = 6.500.000", d["saldo_awal"]["modal"] == 6500000)
        cek("B1 neraca seimbang", d["posisi_keuangan"]["seimbang_hitungan"])
        cek("B1 asumsi disebut", any("digulirkan" in x for x in d["asumsi"]))
        d = jalan([f3, "--periode-awal", "2026-03-01", "--utang-bank-awal", "0", "--format", "json"])
        cek("B1 utang bank digulirkan ke Maret", d["saldo_awal"]["utang_bank"] == 10000000)
        cek("B1 kasbon digulirkan ke Maret", d["saldo_awal"]["piutang_lain"] == 300000)
        d = jalan([f3, "--periode-awal", "2026-03-01", "--kas-awal", "7jt", "--saldo-awal-per", "awal-periode",
                   "--format", "json"])
        cek("B1 --saldo-awal-per awal-periode tidak menggulir", d["saldo_awal"]["kas"] == 7000000)
        d = jalan([f3, "--periode-awal", "2026-02-01", "--modal-awal", "5jt", "--format", "json"])
        cek("B1 modal input ikut digulirkan (tetap seimbang)", d["posisi_keuangan"]["seimbang_hitungan"])

        # --- S5 tanda kurung
        d = jalan([os.path.join(tmp, "kurung.csv"), "--kas-awal", "1jt", "--format", "json"])
        tepung = [t for t in d["rincian_transaksi"] if t["keterangan"] == "Beli tepung"][0]
        cek("S5 (200.000) di Keluar tetap keluar", tepung["arah"] == "keluar" and tepung["nilai"] == 200000)
        cek("S5 minus di Masuk jadi baris bermasalah", any(b["baris"] == 4 for b in d["baris_bermasalah"]))
        cek("TOTAL di kolom tanggal dilewati", not any("TOTAL" in b["alasan"] for b in d["baris_bermasalah"]))

        # --- S3 angka mustahil -> SEMENTARA, bukan seimbang
        fw = os.path.join(tmp, "warung.csv")
        d = jalan([fw, "--kas-awal", "1jt", "--persediaan-akhir", "5jt", "--format", "json"])
        cek("S3 HPP negatif -> SEMENTARA", d["status"] == "SEMENTARA" and d["anomali"])
        cek("S3 tidak dilabeli seimbang", d["posisi_keuangan"]["seimbang"] is False)
        p = jalan([fw, "--kas-awal", "1jt", "--persediaan-akhir", "5jt"])
        cek("S3 teks tidak memakai ✔ seimbang", "Neraca seimbang" not in p.stdout)

        # --- S4 selisih kas
        d = jalan([fw, "--kas-awal", "1jt", "--kas-akhir-aktual", "2.900.000", "--format", "json"])
        cek("S4 tanpa opsi: tidak seimbang", d["posisi_keuangan"]["selisih"] == -100000)
        d = jalan([fw, "--kas-awal", "1jt", "--kas-akhir-aktual", "2.900.000", "--catat-selisih-kas",
                   "--format", "json"])
        cek("S4 dengan opsi: seimbang", d["posisi_keuangan"]["seimbang"])
        cek("S4 laba turun 100.000", d["laba_rugi"]["laba_bersih"] == 1900000)
        jalan([fw, "--catat-selisih-kas"], harap_kode=1)

        # --- ringkasan rugi
        d = jalan([os.path.join(tmp, "rugi.csv"), "--format", "json"])
        cek("ringkasan rugi tanpa persen negatif", "rugi sekitar Rp 50.000" in d["ringkasan_awam"] and
            "-" not in d["ringkasan_awam"].split("RUGI")[1].split(".")[0], d["ringkasan_awam"])
        p = jalan([os.path.join(tmp, "rugi.csv")])
        cek("tren tidak tampil untuk 1 bulan", "Tren per periode" not in p.stdout)

        # --- file rusak
        kosong = os.path.join(tmp, "kosong.csv")
        open(kosong, "w").close()
        jalan([kosong], harap_kode=1)
        jalan([os.path.join(tmp, "tidak-ada.csv")], harap_kode=1)
        print("SEMUA UJI LULUS")
        return 0
    except AssertionError as e:
        print(e)
        return 1
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
