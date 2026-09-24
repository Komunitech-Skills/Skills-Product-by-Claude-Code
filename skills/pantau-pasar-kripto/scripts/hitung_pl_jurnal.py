#!/usr/bin/env python3
"""Rapikan jurnal trading kripto milik member & hitung P/L dari angka yang MEMBER masukkan.

TIDAK menghitung/mengira harga sendiri, TIDAK memberi rekomendasi beli/jual, dan TIDAK
menilai apakah rencana member "benar". Skrip ini murni: (1) merapikan baris jurnal,
(2) menghitung realized P/L per transaksi jual memakai metode FIFO (First In First Out)
atas lot pembelian yang dicatat member sendiri, termasuk biaya, dan (3) mendaftar rencana
tinjau-ulang yang member tulis sendiri dan sudah jatuh tempo.

Format kolom CSV wajib (header persis, boleh urutan bebas, pisah koma):
  tanggal            -> YYYY-MM-DD
  koin               -> kode singkat, mis. BTC (huruf besar/kecil bebas, dirapikan)
  aksi               -> "beli" atau "jual"
  jumlah_koin        -> angka desimal titik standar, mis. 0.015 (BUKAN format Indonesia)
  harga_satuan       -> harga per 1 unit koin dalam Rupiah, boleh format Indonesia
                         (mis. "Rp 1.500.000" / "1.500.000" / "1500000")
  biaya              -> total biaya/fee transaksi ini dalam Rupiah (boleh 0), format sama
  alasan_rencana     -> teks bebas milik member (opsional, boleh kosong)
  tinjau_ulang_pada  -> tanggal YYYY-MM-DD (opsional) -- kapan member ingin diingatkan
  tinjau_ulang_syarat -> teks bebas milik member, mis. "kalau turun 20% dari sini" (opsional)

Baris yang rusak (kolom wajib kosong, angka tidak valid, aksi bukan beli/jual, jual melebihi
stok tercatat) TIDAK menghentikan proses -- dicatat di "baris_bermasalah" dengan nomor baris
dan alasannya, baris lain tetap dihitung.

Pembulatan: semua angka Rupiah pada hasil akhir (proceeds, cost basis, P/L) dibulatkan ke
rupiah terdekat (pembulatan matematis biasa), sesuai standar CLAUDE.md. Jumlah koin TIDAK
dibulatkan (presisi desimal dipertahankan apa adanya).
"""

import argparse
import csv
import json
import sys
from collections import defaultdict, deque
from datetime import date, datetime
from decimal import Decimal, ROUND_HALF_UP

KOLOM_WAJIB = ["tanggal", "koin", "aksi", "jumlah_koin", "harga_satuan", "biaya"]


def bulat_rupiah(nilai):
    d = Decimal(str(nilai)).quantize(Decimal("1"), rounding=ROUND_HALF_UP)
    return int(d)


def parse_angka_id(teks):
    """Terima 'Rp 1.500.000', '1.500.000,50', '1500000', '1500000.5' -> float.

    Aturan: kalau ada koma DAN titik -> titik = ribuan, koma = desimal (format Indonesia).
    Kalau cuma ada koma -> koma = desimal. Kalau cuma ada titik (atau tidak ada keduanya)
    -> titik dianggap desimal standar (dipakai juga untuk jumlah_koin).
    """
    if teks is None:
        raise ValueError("kosong")
    s = str(teks).strip()
    if s == "":
        raise ValueError("kosong")
    s = s.replace("Rp", "").replace("rp", "").replace("RP", "").strip()
    s = s.replace(" ", "")
    if "," in s and "." in s:
        s = s.replace(".", "").replace(",", ".")
    elif "," in s:
        s = s.replace(",", ".")
    elif "." in s:
        bagian = s.split(".")
        # lebih dari satu titik (mis. "1.500.000"), atau satu titik dengan tepat 3 digit
        # di belakangnya (mis. "1.500") -> pola pemisah ribuan gaya Indonesia, hapus semua titik.
        # Titik dengan 1-2 digit di belakang (mis. "15.5") tetap dianggap desimal standar.
        if len(bagian) > 2 or len(bagian[-1]) == 3:
            s = s.replace(".", "")
    return float(s)


def parse_tanggal(teks):
    return datetime.strptime(teks.strip(), "%Y-%m-%d").date()


def muat_jurnal(path):
    baris_ok = []
    baris_bermasalah = []
    try:
        with open(path, "r", encoding="utf-8-sig", newline="") as f:
            reader = csv.DictReader(f)
            if reader.fieldnames is None:
                raise FileNotFoundError("header kosong")
            hilang = [k for k in KOLOM_WAJIB if k not in reader.fieldnames]
            if hilang:
                raise ValueError(f"kolom wajib hilang di header: {', '.join(hilang)}")
            for nomor, row in enumerate(reader, start=2):  # baris 1 = header
                try:
                    tgl = parse_tanggal(row["tanggal"])
                    koin = (row["koin"] or "").strip().upper()
                    if not koin:
                        raise ValueError("kolom 'koin' kosong")
                    aksi = (row["aksi"] or "").strip().lower()
                    if aksi not in ("beli", "jual"):
                        raise ValueError(f"kolom 'aksi' harus 'beli' atau 'jual', dapat '{row['aksi']}'")
                    jumlah = float(str(row["jumlah_koin"]).strip())
                    if jumlah <= 0:
                        raise ValueError("'jumlah_koin' harus lebih besar dari 0")
                    harga = parse_angka_id(row["harga_satuan"])
                    if harga < 0:
                        raise ValueError("'harga_satuan' tidak boleh negatif")
                    biaya = parse_angka_id(row.get("biaya") or "0")
                    if biaya < 0:
                        raise ValueError("'biaya' tidak boleh negatif")
                    baris_ok.append({
                        "baris": nomor,
                        "tanggal": tgl,
                        "koin": koin,
                        "aksi": aksi,
                        "jumlah_koin": jumlah,
                        "harga_satuan": harga,
                        "biaya": biaya,
                        "alasan_rencana": (row.get("alasan_rencana") or "").strip(),
                        "tinjau_ulang_pada": (row.get("tinjau_ulang_pada") or "").strip(),
                        "tinjau_ulang_syarat": (row.get("tinjau_ulang_syarat") or "").strip(),
                    })
                except (ValueError, KeyError) as e:
                    baris_bermasalah.append({"baris": nomor, "alasan": str(e)})
    except FileNotFoundError:
        raise
    return baris_ok, baris_bermasalah


def hitung_fifo(baris_ok):
    """Kembalikan (posisi_per_koin, realized_per_koin, baris_bermasalah_tambahan)."""
    lot = defaultdict(deque)  # koin -> deque of {"jumlah", "harga_satuan", "biaya_per_unit"}
    realized = defaultdict(list)
    bermasalah_tambahan = []

    urut = sorted(baris_ok, key=lambda r: (r["tanggal"], r["baris"]))
    for r in urut:
        koin = r["koin"]
        if r["aksi"] == "beli":
            biaya_per_unit = r["biaya"] / r["jumlah_koin"] if r["jumlah_koin"] else 0.0
            lot[koin].append({
                "jumlah": r["jumlah_koin"],
                "harga_satuan": r["harga_satuan"],
                "biaya_per_unit": biaya_per_unit,
                "tanggal": r["tanggal"],
            })
        else:  # jual
            sisa_jual = r["jumlah_koin"]
            biaya_jual_per_unit = r["biaya"] / r["jumlah_koin"] if r["jumlah_koin"] else 0.0
            cost_basis_total = 0.0
            jumlah_terpakai = 0.0
            while sisa_jual > 1e-12 and lot[koin]:
                l = lot[koin][0]
                ambil = min(l["jumlah"], sisa_jual)
                cost_basis_total += ambil * (l["harga_satuan"] + l["biaya_per_unit"])
                jumlah_terpakai += ambil
                l["jumlah"] -= ambil
                sisa_jual -= ambil
                if l["jumlah"] <= 1e-12:
                    lot[koin].popleft()
            if sisa_jual > 1e-12:
                bermasalah_tambahan.append({
                    "baris": r["baris"],
                    "alasan": (
                        f"Jual {r['jumlah_koin']} {koin} melebihi stok yang tercatat dari baris 'beli' "
                        f"sebelumnya (kekurangan {sisa_jual}). P/L dihitung hanya untuk bagian yang "
                        "ada lot-nya; sisanya diabaikan -- kemungkinan ada baris 'beli' yang belum dicatat."
                    ),
                })
            proceeds = jumlah_terpakai * r["harga_satuan"] - biaya_jual_per_unit * jumlah_terpakai
            pl = proceeds - cost_basis_total
            pl_persen = (pl / cost_basis_total * 100.0) if cost_basis_total > 0 else None
            realized[koin].append({
                "baris": r["baris"],
                "tanggal": r["tanggal"].isoformat(),
                "jumlah_terjual": round(jumlah_terpakai, 10),
                "proceeds": bulat_rupiah(proceeds),
                "cost_basis": bulat_rupiah(cost_basis_total),
                "biaya": bulat_rupiah(r["biaya"]),
                "pl": bulat_rupiah(pl),
                "pl_persen": round(pl_persen, 2) if pl_persen is not None else None,
            })

    posisi = {}
    for koin, lots in lot.items():
        jumlah_total = sum(l["jumlah"] for l in lots)
        if jumlah_total <= 1e-12:
            continue
        nilai_total = sum(l["jumlah"] * (l["harga_satuan"] + l["biaya_per_unit"]) for l in lots)
        posisi[koin] = {
            "jumlah_tersisa": round(jumlah_total, 10),
            "harga_rata_rata_perolehan": bulat_rupiah(nilai_total / jumlah_total) if jumlah_total else 0,
            "jumlah_lot": len(lots),
        }
    return posisi, realized, bermasalah_tambahan


def daftar_tinjau_ulang(baris_ok, hari_ini):
    hasil = []
    for r in baris_ok:
        if not r["tinjau_ulang_pada"]:
            continue
        try:
            tgl = parse_tanggal(r["tinjau_ulang_pada"])
        except ValueError:
            continue
        if tgl <= hari_ini:
            hasil.append({
                "baris": r["baris"],
                "koin": r["koin"],
                "tanggal_ditulis": r["tanggal"].isoformat(),
                "tinjau_ulang_pada": tgl.isoformat(),
                "jatuh_tempo": tgl < hari_ini,
                "syarat": r["tinjau_ulang_syarat"] or "(tidak ditulis syaratnya)",
                "alasan_rencana_asal": r["alasan_rencana"] or "(tidak ditulis)",
            })
    hasil.sort(key=lambda x: x["tinjau_ulang_pada"])
    return hasil


def main(argv=None):
    ap = argparse.ArgumentParser(description="Rapikan jurnal trading kripto & hitung P/L (FIFO) dari angka member.")
    ap.add_argument("--jurnal", required=True, help="Path ke JURNAL.csv milik member.")
    ap.add_argument("--hari-ini", default=None,
                     help="Tanggal 'hari ini' (YYYY-MM-DD) untuk cek jatuh tempo tinjau-ulang. "
                          "Default: tanggal sistem. Dipakai untuk pengujian deterministik.")
    args = ap.parse_args(argv)

    hari_ini = parse_tanggal(args.hari_ini) if args.hari_ini else date.today()

    try:
        baris_ok, baris_bermasalah = muat_jurnal(args.jurnal)
    except FileNotFoundError:
        print(json.dumps({"status": "error", "pesan": f"File jurnal tidak ditemukan: {args.jurnal}"},
                          ensure_ascii=False, indent=2))
        return 1
    except ValueError as e:
        print(json.dumps({"status": "error", "pesan": f"Jurnal tidak valid: {e}"},
                          ensure_ascii=False, indent=2))
        return 1

    if not baris_ok and not baris_bermasalah:
        print(json.dumps({"status": "error", "pesan": "Jurnal kosong, tidak ada baris untuk dihitung."},
                          ensure_ascii=False, indent=2))
        return 1

    posisi, realized, bermasalah_tambahan = hitung_fifo(baris_ok)
    semua_bermasalah = baris_bermasalah + bermasalah_tambahan
    semua_bermasalah.sort(key=lambda x: x["baris"])

    total_realized_pl = bulat_rupiah(sum(r["pl"] for lst in realized.values() for r in lst))

    hasil = {
        "status": "ok",
        "posisi_tersisa": posisi,
        "realized_per_koin": realized,
        "total_realized_pl": total_realized_pl,
        "baris_bermasalah": semua_bermasalah,
        "tinjau_ulang_jatuh_tempo": daftar_tinjau_ulang(baris_ok, hari_ini),
        "jumlah_baris_dihitung": len(baris_ok),
        "disclaimer": "Angka dari yang Anda catat sendiri, bukan nasihat investasi.",
    }
    print(json.dumps(hasil, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
