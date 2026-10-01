#!/usr/bin/env python3
"""Rapikan jurnal trading kripto milik member & hitung P/L dari angka yang MEMBER masukkan.

TIDAK menghitung/mengira harga sendiri, TIDAK memberi rekomendasi beli/jual, dan TIDAK
menilai apakah rencana member "benar". Skrip ini murni: (1) merapikan baris jurnal,
(2) menghitung realized P/L per transaksi jual memakai metode FIFO (First In First Out)
atas lot pembelian yang dicatat member sendiri, termasuk biaya, dan (3) mendaftar rencana
tinjau-ulang yang member tulis sendiri dan sudah jatuh tempo.

Format kolom CSV wajib (header persis, boleh urutan bebas). Pemisah kolom **koma (,) atau
titik-koma (;)** -- dideteksi otomatis dari baris header (titik-koma umum dipakai Excel
lokal Indonesia). BOM UTF-8 di awal file (ditulis Excel) dan file yang tidak murni UTF-8
(karakter aneh di teks bebas) ditangani otomatis, tidak menggagalkan seluruh file:
  tanggal            -> YYYY-MM-DD
  koin               -> kode singkat, mis. BTC (huruf besar/kecil bebas, dirapikan)
  aksi               -> "beli" atau "jual"
  jumlah_koin        -> angka desimal, titik ATAU koma sebagai tanda desimal (mis. "0.015"
                         atau "0,015") -- TIDAK boleh keduanya sekaligus dalam satu nilai
                         (itu ambigu: bukan format ribuan seperti kolom Rupiah).
  harga_satuan       -> harga per 1 unit koin dalam Rupiah, boleh format Indonesia
                         (mis. "Rp 1.500.000" / "1.500.000" / "1500000")
  biaya              -> total biaya/fee transaksi ini dalam Rupiah (boleh 0), format sama
  alasan_rencana     -> teks bebas milik member (opsional, boleh kosong)
  tinjau_ulang_pada  -> tanggal YYYY-MM-DD (opsional) -- kapan member ingin diingatkan
  tinjau_ulang_syarat -> teks bebas milik member, mis. "kalau turun 20% dari sini" (opsional)

Baris yang rusak (kolom wajib kosong, angka tidak valid, aksi bukan beli/jual, jual melebihi
stok tercatat) TIDAK menghentikan proses -- dicatat di "baris_bermasalah" dengan nomor baris
dan alasannya (Bahasa Indonesia), baris lain tetap dihitung.

Pemeriksaan kewajaran biaya (v1.0.5, field `cek_biaya`): baris yang biayanya > 1% nilai transaksi,
atau berbeda jauh (>= 1,5x, selisih >= 0,05 poin) dari median transaksi lain di sisi yang sama
(beli/jual), ditandai tanpa
menebak sebabnya; `cek_biaya_beli_vs_jual` menandai bila median biaya jual vs beli berbeda jauh. Jurnal yang valid tapi belum
punya transaksi (header saja) BUKAN error -- keluar status "ok" dengan hasil kosong.

Pembulatan: semua angka Rupiah pada hasil akhir (proceeds, cost basis, P/L) dibulatkan ke
rupiah terdekat (pembulatan matematis biasa), sesuai standar CLAUDE.md. Jumlah koin TIDAK
dibulatkan (presisi desimal dipertahankan apa adanya).

Filter periode (opsional, `--periode bulan-ini|tahun-ini|semua` atau `--dari`/`--sampai`
YYYY-MM-DD): hanya membatasi transaksi JUAL mana yang dihitung ke `realized_per_koin` &
`total_realized_pl` yang ditampilkan -- perhitungan FIFO tetap memakai SELURUH riwayat
'beli' (termasuk yang di luar periode) supaya cost basis tetap benar.
"""

import argparse
import csv
import io
import json
import sys
from collections import defaultdict, deque
from datetime import date, datetime
from decimal import Decimal, ROUND_HALF_UP

KOLOM_WAJIB = ["tanggal", "koin", "aksi", "jumlah_koin", "harga_satuan", "biaya"]


class JurnalTidakValid(Exception):
    """Masalah pada file jurnal itu sendiri (bukan pada satu baris) -- header hilang,
    kolom wajib tidak ada, file tidak ditemukan, dsb. Selalu pesan Bahasa Indonesia."""


def bulat_rupiah(nilai):
    d = Decimal(str(nilai)).quantize(Decimal("1"), rounding=ROUND_HALF_UP)
    return int(d)


def parse_angka_id(teks):
    """Terima 'Rp 1.500.000', '1.500.000,50', '1500000', '1500000.5' -> float.

    Dipakai untuk kolom Rupiah (harga_satuan, biaya) -- BUKAN untuk jumlah_koin, lihat
    `parse_jumlah_koin` untuk itu (aturan format berbeda, lihat docstring modul).
    """
    if teks is None:
        raise ValueError("nilainya kosong")
    s = str(teks).strip()
    if s == "":
        raise ValueError("nilainya kosong")
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
    try:
        return float(s)
    except ValueError:
        raise ValueError(f"'{teks}' bukan angka Rupiah yang bisa dibaca.")


def parse_jumlah_koin(teks):
    """Terima '0.015' ATAU '0,015' (satu tanda desimal saja) -> float. Kolom jumlah_koin
    TIDAK memakai pemisah ribuan gaya Rupiah -- titik dan koma di sini SELALU berarti
    tanda desimal, jadi kalau keduanya muncul sekaligus itu ambigu dan ditolak."""
    if teks is None:
        raise ValueError("nilainya kosong")
    s = str(teks).strip().replace(" ", "")
    if s == "":
        raise ValueError("nilainya kosong")
    if "," in s and "." in s:
        raise ValueError(
            f"'{teks}' memakai koma dan titik sekaligus -- untuk jumlah koin pakai satu saja "
            "sebagai tanda desimal, mis. '0.015' atau '0,015'."
        )
    s = s.replace(",", ".")
    try:
        return float(s)
    except ValueError:
        raise ValueError(f"'{teks}' bukan angka yang bisa dibaca untuk jumlah koin.")


def parse_tanggal(teks, nama_field="tanggal"):
    try:
        return datetime.strptime(teks.strip(), "%Y-%m-%d").date()
    except (ValueError, AttributeError):
        raise ValueError(f"{nama_field} '{teks}' bukan tanggal valid (format harus YYYY-MM-DD, mis. 2026-09-24).")


def _baca_teks_tahan_encoding(path):
    """Baca file sebagai teks, tahan BOM UTF-8 (umum dari Excel) dan karakter yang bukan
    UTF-8 murni (diganti, bukan menggagalkan seluruh file). Kembalikan (teks, peringatan)."""
    with open(path, "rb") as f:
        mentah = f.read()
    try:
        return mentah.decode("utf-8-sig"), None
    except UnicodeDecodeError:
        return (
            mentah.decode("utf-8-sig", errors="replace"),
            "Sebagian karakter di file jurnal bukan UTF-8 murni (mis. hasil salin dari "
            "aplikasi lain) -- karakter itu diganti '�', teks lain tidak terpengaruh.",
        )


def _deteksi_pemisah(baris_header):
    """';' umum dipakai Excel lokal Indonesia; ',' adalah default CSV biasa."""
    if baris_header.count(";") > baris_header.count(","):
        return ";"
    return ","


def muat_jurnal(path):
    """Kembalikan (baris_ok, baris_bermasalah, peringatan_global). Melempar
    `JurnalTidakValid` (pesan Bahasa Indonesia) kalau filenya sendiri bermasalah."""
    try:
        teks, peringatan_encoding = _baca_teks_tahan_encoding(path)
    except FileNotFoundError:
        raise JurnalTidakValid(f"File jurnal tidak ditemukan: {path}")
    except OSError as e:
        raise JurnalTidakValid(f"File jurnal tidak bisa dibaca: {e}")

    if teks.strip() == "":
        raise JurnalTidakValid("File jurnal kosong (tidak ada isi sama sekali, termasuk baris header).")

    baris_pertama = teks.splitlines()[0] if teks.splitlines() else ""
    pemisah = _deteksi_pemisah(baris_pertama)

    peringatan_global = [peringatan_encoding] if peringatan_encoding else []
    baris_ok = []
    baris_bermasalah = []

    reader = csv.DictReader(io.StringIO(teks), delimiter=pemisah)
    if reader.fieldnames is None:
        raise JurnalTidakValid("File jurnal tidak punya baris header.")
    hilang = [k for k in KOLOM_WAJIB if k not in reader.fieldnames]
    if hilang:
        raise JurnalTidakValid(
            f"Kolom wajib hilang di header: {', '.join(hilang)}. "
            f"(Pemisah kolom yang terdeteksi: '{pemisah}' -- kalau file Anda memakai pemisah "
            "lain, ganti dulu ke koma atau titik-koma.)"
        )

    for nomor, row in enumerate(reader, start=2):  # baris 1 = header
        try:
            tgl = parse_tanggal(row["tanggal"])
            koin = (row["koin"] or "").strip().upper()
            if not koin:
                raise ValueError("kolom 'koin' kosong")
            aksi = (row["aksi"] or "").strip().lower()
            if aksi not in ("beli", "jual"):
                raise ValueError(f"kolom 'aksi' harus 'beli' atau 'jual', dapat '{row['aksi']}'")
            jumlah = parse_jumlah_koin(row["jumlah_koin"])
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

    return baris_ok, baris_bermasalah, peringatan_global


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
            if jumlah_terpakai > 1e-12:
                # Kalau jumlah_terpakai == 0 (jual tanpa lot sama sekali, mis. belum pernah
                # ada 'beli'), tidak ada transaksi nyata yang bisa dihitung P/L-nya -- baris
                # 'baris_bermasalah' di atas sudah menjelaskan ini, tidak perlu entri
                # realized "0" yang menyesatkan (seolah ada penjualan senilai nol).
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


# v1.0.5: pemeriksaan kewajaran biaya per sisi transaksi (uji OpenClaw 2026-10-01: fee jual 0,4% vs
# lainnya 0,2% tidak ditandai). Skrip hanya MENANDAI; tidak menebak sebabnya dan tidak mengubah P/L.
BATAS_BIAYA_WAJAR_PERSEN = 1.0     # fee + pajak per transaksi di exchange Indonesia umumnya jauh di bawah 1%
RASIO_BEDA_JAUH = 1.5              # >= 1,5x (atau <= 1/1,5) dari median pembanding = berbeda jauh
SELISIH_MIN_POIN = 0.05            # abaikan selisih < 0,05 poin persen (pembulatan fee)


def _pid(x):
    """Persen gaya Indonesia: 0.4 -> '0,40'."""
    return f"{x:.2f}".replace(".", ",")


def _median(nilai):
    v = sorted(nilai)
    n = len(v)
    if n == 0:
        return None
    return v[n // 2] if n % 2 else (v[n // 2 - 1] + v[n // 2]) / 2.0


def _beda_jauh(a, b):
    if b is None or b <= 0:
        return False
    return abs(a - b) >= SELISIH_MIN_POIN and (a >= b * RASIO_BEDA_JAUH or a * RASIO_BEDA_JAUH <= b)


def periksa_biaya(baris_ok):
    """Kembalikan daftar baris dengan rasio biaya janggal (persen dari nilai transaksi)."""
    data = []
    for r in baris_ok:
        nilai = r["jumlah_koin"] * r["harga_satuan"]
        if nilai <= 0:
            continue
        data.append((r, r["biaya"] / nilai * 100.0))
    hasil = []
    med_sisi = {a: _median([p for r, p in data if r["aksi"] == a and p > 0]) for a in ("beli", "jual")}
    for i, (r, persen) in enumerate(data):
        alasan = []
        if persen > BATAS_BIAYA_WAJAR_PERSEN:
            alasan.append(f"biaya {_pid(persen)}% dari nilai transaksi, di atas {BATAS_BIAYA_WAJAR_PERSEN:.0f}% "
                          "(fee + pajak di exchange Indonesia umumnya jauh di bawah ini)")
        # Pembanding: median transaksi di SISI YANG SAMA (beli vs beli, jual vs jual). Grup >= 3 baris
        # memakai median grup (termasuk baris ini) agar satu pencilan tidak ikut menandai baris normal;
        # grup 2 baris dibanding dengan baris pasangannya; tanpa pasangan sesisi -> median semua baris (>= 3).
        grup = [p for rr, p in data if p > 0 and rr["aksi"] == r["aksi"]]
        if len(grup) >= 3:
            lain, label = grup, f"transaksi {r['aksi']} lain"
        elif len(grup) == 2:
            lain, label = [p for j, (rr, p) in enumerate(data)
                           if j != i and p > 0 and rr["aksi"] == r["aksi"]], f"transaksi {r['aksi']} lain"
        else:
            semua = [p for _, p in data if p > 0]
            lain, label = (semua if len(semua) >= 3 else []), "transaksi lain"
        med_lain = _median(lain)
        if persen > 0 and _beda_jauh(persen, med_lain):
            alasan.append(f"biaya {_pid(persen)}% berbeda jauh dari {label} (median {_pid(med_lain)}%)")
        if alasan:
            hasil.append({
                "baris": r["baris"], "tanggal": r["tanggal"].isoformat(), "koin": r["koin"], "aksi": r["aksi"],
                "biaya": bulat_rupiah(r["biaya"]), "biaya_persen": round(persen, 3), "alasan": "; ".join(alasan),
            })
    catatan_sisi = None
    if med_sisi["beli"] and med_sisi["jual"] and _beda_jauh(med_sisi["jual"], med_sisi["beli"]):
        catatan_sisi = (f"Rata-rata (median) biaya JUAL {_pid(med_sisi['jual'])}% vs BELI {_pid(med_sisi['beli'])}% "
                        "berbeda jauh -- cek tabel fee resmi exchange Anda.")
    return hasil, catatan_sisi


def daftar_tinjau_ulang(baris_ok, hari_ini):
    hasil = []
    for r in baris_ok:
        if not r["tinjau_ulang_pada"]:
            continue
        try:
            tgl = parse_tanggal(r["tinjau_ulang_pada"], "tinjau_ulang_pada")
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


def hitung_rentang_periode(periode, hari_ini):
    if periode == "bulan-ini":
        return hari_ini.replace(day=1), hari_ini
    if periode == "tahun-ini":
        return hari_ini.replace(month=1, day=1), hari_ini
    return None, None


def _keluar_error(pesan):
    print(json.dumps({"status": "error", "pesan": pesan}, ensure_ascii=False, indent=2))
    return 1


def main(argv=None):
    ap = argparse.ArgumentParser(description="Rapikan jurnal trading kripto & hitung P/L (FIFO) dari angka member.")
    ap.add_argument("--jurnal", required=True, help="Path ke JURNAL.csv milik member.")
    ap.add_argument("--hari-ini", default=None,
                     help="Tanggal 'hari ini' (YYYY-MM-DD) untuk cek jatuh tempo tinjau-ulang & filter periode. "
                          "Default: tanggal sistem. Dipakai untuk pengujian deterministik.")
    ap.add_argument("--periode", choices=["semua", "bulan-ini", "tahun-ini"], default="semua",
                     help="Batasi transaksi JUAL yang ditampilkan/dijumlahkan di realized P/L (FIFO tetap "
                          "memakai seluruh riwayat 'beli'). Default: semua.")
    ap.add_argument("--dari", default=None, help="Batas awal (YYYY-MM-DD), menimpa --periode kalau diisi.")
    ap.add_argument("--sampai", default=None, help="Batas akhir (YYYY-MM-DD), menimpa --periode kalau diisi.")
    args = ap.parse_args(argv)

    try:
        hari_ini = parse_tanggal(args.hari_ini, "--hari-ini") if args.hari_ini else date.today()
        dari, sampai = hitung_rentang_periode(args.periode, hari_ini)
        if args.dari:
            dari = parse_tanggal(args.dari, "--dari")
        if args.sampai:
            sampai = parse_tanggal(args.sampai, "--sampai")
        if dari and sampai and dari > sampai:
            raise ValueError(f"--dari ({dari.isoformat()}) tidak boleh setelah --sampai ({sampai.isoformat()}).")
    except ValueError as e:
        return _keluar_error(str(e))

    try:
        baris_ok, baris_bermasalah, peringatan_global = muat_jurnal(args.jurnal)
    except JurnalTidakValid as e:
        return _keluar_error(str(e))

    if not baris_ok and not baris_bermasalah:
        # Header valid, belum ada transaksi -- ini keadaan wajar (jurnal baru), bukan error.
        print(json.dumps({
            "status": "ok",
            "posisi_tersisa": {},
            "realized_per_koin": {},
            "total_realized_pl": 0,
            "baris_bermasalah": [],
            "tinjau_ulang_jatuh_tempo": [],
            "cek_biaya": [],
            "cek_biaya_beli_vs_jual": None,
            "cek_biaya_keterangan": None,
            "jumlah_baris_dihitung": 0,
            "peringatan_global": peringatan_global,
            "pesan": "Jurnal masih kosong (header ada, belum ada transaksi tercatat).",
            "disclaimer": "Angka dari yang Anda catat sendiri, bukan nasihat investasi.",
        }, ensure_ascii=False, indent=2))
        return 0

    posisi, realized_semua, bermasalah_tambahan = hitung_fifo(baris_ok)
    semua_bermasalah = baris_bermasalah + bermasalah_tambahan
    semua_bermasalah.sort(key=lambda x: x["baris"])

    if dari or sampai:
        realized = {}
        for koin, entri in realized_semua.items():
            terpilih = [
                r for r in entri
                if (not dari or date.fromisoformat(r["tanggal"]) >= dari)
                and (not sampai or date.fromisoformat(r["tanggal"]) <= sampai)
            ]
            if terpilih:
                realized[koin] = terpilih
    else:
        realized = realized_semua

    total_realized_pl = bulat_rupiah(sum(r["pl"] for lst in realized.values() for r in lst))
    cek_biaya, catatan_sisi = periksa_biaya(baris_ok)

    hasil = {
        "status": "ok",
        "periode": {
            "dari": dari.isoformat() if dari else None,
            "sampai": sampai.isoformat() if sampai else None,
            "keterangan": "hanya membatasi transaksi jual yang dihitung; posisi_tersisa & FIFO tetap penuh"
                          if (dari or sampai) else "semua transaksi",
        },
        "posisi_tersisa": posisi,
        "realized_per_koin": realized,
        "total_realized_pl": total_realized_pl,
        "baris_bermasalah": semua_bermasalah,
        "tinjau_ulang_jatuh_tempo": daftar_tinjau_ulang(baris_ok, hari_ini),
        "cek_biaya": cek_biaya,
        "cek_biaya_beli_vs_jual": catatan_sisi,
        "cek_biaya_keterangan": (
            "Baris di 'cek_biaya' hanya DITANDAI agar dicek ke riwayat transaksi exchange (mis. salah ketik, "
            "fee trading + PPh 0,21% tercampur, atau biaya lain). Sebabnya tidak ditebak; P/L tetap dihitung "
            "dari angka yang dicatat.") if (cek_biaya or catatan_sisi) else None,
        "jumlah_baris_dihitung": len(baris_ok),
        "peringatan_global": peringatan_global,
        "disclaimer": "Angka dari yang Anda catat sendiri, bukan nasihat investasi.",
    }
    print(json.dumps(hasil, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
