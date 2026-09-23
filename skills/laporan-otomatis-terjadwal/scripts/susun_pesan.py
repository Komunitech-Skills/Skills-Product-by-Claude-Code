#!/usr/bin/env python3
"""Merakit pesan laporan ringkas (siap kirim ke WA/Telegram) dari angka JSON.

Dipakai SETELAH angka dihitung oleh script skill lain (mis. rekap-penjualan-csv,
laporan-keuangan-emkm, arus-kas-13minggu, tagih-piutang) atau skill ini sendiri
(cek_sumber_data.py). Script ini TIDAK menghitung ulang apa pun -- hanya
memformat Rupiah dan merapikan tata letak supaya angka penting ada di atas dan
pesan tidak lebih dari batas baris (default 15, sesuai aturan skill: ringkas
untuk layar HP).

Hanya library standar Python (3.8+). Input JSON lewat --data <file> atau '-'
(stdin). Output: teks pesan ke stdout. Exit code != 0 + pesan error jelas ke
stderr bila input tidak valid.

Skema input (semua field opsional kecuali "judul"):
{
  "judul": "Laporan Penjualan Harian",
  "subjudul": "Selasa, 23 Sep 2026",
  "baris": [
    {"label": "Total omzet", "nilai": 4500000, "rupiah": true},
    {"label": "Jumlah transaksi", "nilai": 32},
    {"label": "Dibanding kemarin", "teks": "+12% dari Senin (Rp 4.020.000)"}
  ],
  "daftar": [
    {"judul": "Produk terlaris", "item": ["Kopi susu -- Rp 1.200.000", "Roti bakar -- Rp 800.000"]}
  ],
  "catatan": ["2 baris data dilewati (tanggal tidak terbaca)."],
  "peringatan": ["Data 3 hari terakhir belum masuk."]
}

"baris" tampil sebagai "Label: nilai" di bagian atas pesan (angka penting dulu).
"daftar" tampil sebagai sub-bagian berjudul dengan bullet.
"catatan" dan "peringatan" tampil di bagian bawah, ditandai jelas.
TIDAK ADA field untuk nama/kontak pelanggan perorangan -- sengaja tidak
disediakan supaya penyusun laporan tidak menaruh data pribadi pelanggan di
pesan ini (UU PDP). Data pelanggan tetap boleh dilihat di file detail lokal.
"""
import argparse
import json
import re
import sys

KATA_TERLARANG = ("nomor hp", "no. hp", "no hp", "nomor telepon", "nik", "no. ktp", "no ktp")


def format_rupiah(nilai):
    try:
        n = round(float(nilai))
    except (TypeError, ValueError):
        raise ValueError(f"Nilai rupiah tidak valid: {nilai!r}")
    negatif = n < 0
    n = abs(n)
    teks = f"{n:,}".replace(",", ".")
    return ("-Rp " if negatif else "Rp ") + teks


def format_angka(nilai):
    if isinstance(nilai, float) and nilai.is_integer():
        nilai = int(nilai)
    if isinstance(nilai, float):
        teks = f"{nilai:,.2f}".replace(",", "@").replace(".", ",").replace("@", ".")
        return teks
    if isinstance(nilai, int):
        return f"{nilai:,}".replace(",", ".")
    return str(nilai)


def cek_data_pribadi(teks, peringatan_keluar):
    rendah = teks.lower()
    for kata in KATA_TERLARANG:
        if kata in rendah:
            peringatan_keluar.append(
                f"Baris berisi kata '{kata}' -- kemungkinan data pribadi pelanggan/karyawan. "
                "Sesuai UU PDP, laporan rutin sebaiknya hanya berisi angka agregat, bukan identitas "
                "orang. Baris ini tetap disertakan; periksa kembali sebelum jadwal diaktifkan."
            )


def main():
    p = argparse.ArgumentParser(description="Rakit pesan laporan ringkas dari data JSON")
    p.add_argument("--data", default="-", help="File JSON berisi data laporan, atau '-' untuk stdin (default)")
    p.add_argument("--maks-baris", type=int, default=15, help="Batas jumlah baris pesan (default 15)")
    a = p.parse_args()

    try:
        mentah = sys.stdin.read() if a.data == "-" else open(a.data, "r", encoding="utf-8").read()
    except OSError as e:
        print(f"ERROR: gagal membaca --data: {e}", file=sys.stderr)
        sys.exit(1)

    try:
        data = json.loads(mentah)
    except json.JSONDecodeError as e:
        print(f"ERROR: JSON input tidak valid: {e}", file=sys.stderr)
        sys.exit(1)

    if not isinstance(data, dict) or not data.get("judul"):
        print("ERROR: JSON input wajib berupa objek dengan field 'judul' berisi teks.", file=sys.stderr)
        sys.exit(1)

    peringatan_pdp = []
    baris_pesan = [f"*{data['judul']}*"]
    if data.get("subjudul"):
        baris_pesan.append(str(data["subjudul"]))
    baris_pesan.append("")

    for b in data.get("baris", []):
        label = b.get("label")
        if not label:
            print("ERROR: setiap item 'baris' wajib punya 'label'.", file=sys.stderr)
            sys.exit(1)
        if "teks" in b:
            nilai_teks = str(b["teks"])
        elif "nilai" not in b:
            print(f"ERROR: item baris '{label}' wajib punya 'nilai' atau 'teks'.", file=sys.stderr)
            sys.exit(1)
        elif b.get("rupiah"):
            try:
                nilai_teks = format_rupiah(b["nilai"])
            except ValueError as e:
                print(f"ERROR: {e} (baris '{label}')", file=sys.stderr)
                sys.exit(1)
        else:
            nilai_teks = format_angka(b["nilai"])
        baris_gabungan = f"{label}: {nilai_teks}"
        cek_data_pribadi(baris_gabungan, peringatan_pdp)
        baris_pesan.append(baris_gabungan)

    for seksi in data.get("daftar", []):
        judul_seksi = seksi.get("judul", "")
        item = seksi.get("item", [])
        if not item:
            continue
        baris_pesan.append("")
        if judul_seksi:
            baris_pesan.append(f"*{judul_seksi}*")
        for it in item:
            teks_item = f"- {it}"
            cek_data_pribadi(teks_item, peringatan_pdp)
            baris_pesan.append(teks_item)

    catatan = list(data.get("catatan", [])) + list(data.get("peringatan", [])) + peringatan_pdp
    if catatan:
        baris_pesan.append("")
        for c in catatan:
            baris_pesan.append(f"⚠️ {c}")

    # Rapikan baris kosong berurutan
    rapi = []
    for b in baris_pesan:
        if b == "" and rapi and rapi[-1] == "":
            continue
        rapi.append(b)
    while rapi and rapi[-1] == "":
        rapi.pop()

    dipotong = False
    isi_baris = [b for b in rapi if b != ""]
    if len(isi_baris) > a.maks_baris:
        # Potong dari bawah (catatan/daftar), sisakan judul + baris angka utama
        batas_wajib = 3 + len(data.get("baris", []))  # judul+subjudul+kosong + semua "baris"
        hasil_potong = []
        jumlah_isi = 0
        for b in rapi:
            if b != "":
                if jumlah_isi >= a.maks_baris - 1:
                    dipotong = True
                    continue
                jumlah_isi += 1
            hasil_potong.append(b)
        rapi = hasil_potong
        while rapi and rapi[-1] == "":
            rapi.pop()
        if dipotong:
            rapi.append("(disingkat -- lihat file detail di folder arsip laporan)")

    print("\n".join(rapi))
    if peringatan_pdp:
        # Info tambahan untuk agent (bukan bagian pesan yang dikirim), lewat stderr
        for pesan in peringatan_pdp:
            print(f"INFO: {pesan}", file=sys.stderr)


if __name__ == "__main__":
    main()
