#!/usr/bin/env python3
"""Kalkulator PPN Indonesia (tarif 12%, DPP nilai lain 11/12 untuk non-mewah).

Dasar: UU HPP, PMK 131/2024 (berlaku 1 Januari 2025). Status per 2026-09-23.
- Barang/jasa NON-mewah : PPN = 12% x (11/12 x harga)  -> efektif 11% dari harga.
- Barang MEWAH (PPnBM)  : PPN = 12% x harga.

Hanya library standar Python 3.8+. Tidak ada akses jaringan.

Contoh:
  python3 hitung_ppn.py --harga "Rp 1.000.000"
  python3 hitung_ppn.py --harga 1110000 --mode termasuk
  python3 hitung_ppn.py --harga 250jt --jenis mewah --status-pkp pkp --format json
"""
import argparse
import json
import re
import sys
from decimal import Decimal, ROUND_FLOOR, ROUND_HALF_UP, InvalidOperation

TANGGAL_ATURAN = "2026-09-23"
DASAR_ATURAN = "UU HPP & PMK 131/2024 (PPN 12%; DPP nilai lain 11/12 untuk barang/jasa non-mewah)"

# Tarif efektif terhadap harga (DPP). Disimpan sebagai pecahan tepat.
TARIF_NOMINAL = Decimal(12) / Decimal(100)
FAKTOR_NILAI_LAIN = {"umum": Decimal(11) / Decimal(12), "mewah": Decimal(1)}
# Tarif efektif (dipakai agar tidak ada pembulatan berantai): umum 11/100, mewah 12/100
TARIF_EFEKTIF = {"umum": Decimal(11) / Decimal(100), "mewah": Decimal(12) / Decimal(100)}


CATATAN_PEMBULATAN = ("PPN dihitung dari DPP persis lalu dibulatkan ke bawah sekali ke rupiah penuh "
                      "(tidak pernah melebihi tarif). Mode harga termasuk PPN: DPP = rupiah bulat terbesar "
                      "dengan DPP + PPN <= harga; sisanya ditampilkan. Pembulatan ini belum dicocokkan dengan "
                      "Coretax; bila Coretax menampilkan angka berbeda, ikuti Coretax.")


# ---------------------------------------------------------------- angka & format
_PENGALI = [("miliar", 10 ** 9), ("milyar", 10 ** 9), ("juta", 10 ** 6), ("ribu", 10 ** 3),
            ("jt", 10 ** 6), ("rb", 10 ** 3), ("k", 10 ** 3), ("m", 10 ** 9)]


def _cek_ribuan(bagian, asli, nama):
    if not (1 <= len(bagian[0]) <= 3) or any(len(b) != 3 for b in bagian[1:]):
        raise ValueError("{}: '{}' tidak dikenali. Pakai titik untuk ribuan dan koma untuk desimal, "
                         "mis. 1.250.000 atau 1.250.000,50".format(nama, asli))


def parse_angka(nilai, nama="angka"):
    """Baca angka format Indonesia: 'Rp 15.000', '15.000,50', '1,5 jt', '4,8 M', '15000'.

    Titik = pemisah ribuan, koma = desimal. Satu titik diikuti bukan 3 digit (mis. '2.5') dianggap desimal.
    Akhiran: rb/ribu/k (x1.000), jt/juta (x1.000.000), M/miliar (x1.000.000.000).
    """
    if isinstance(nilai, bool) or nilai is None:
        raise ValueError("{}: nilai kosong atau tidak valid".format(nama))
    if isinstance(nilai, Decimal):
        return nilai
    if isinstance(nilai, int):
        return Decimal(nilai)
    if isinstance(nilai, float):
        return Decimal(str(nilai))
    asli = str(nilai)
    s = asli.strip().lower().replace("\u00a0", "").replace(" ", "")
    s = re.sub(r"^(rp|idr)\.?", "", s)
    s = re.sub(r"[,.]-+$", "", s)          # '15.000,-'
    if s.endswith("%"):
        s = s[:-1]
    pengali = 1
    for akhiran, kali in _PENGALI:
        if s.endswith(akhiran):
            s, pengali = s[: -len(akhiran)], kali
            break
    negatif = s.startswith("-")
    if negatif:
        s = s[1:]
    if not s or not re.fullmatch(r"[\d.,]+", s) or not re.search(r"\d", s):
        raise ValueError("{}: '{}' bukan angka yang valid".format(nama, asli))
    if "," in s and "." in s:
        if s.rfind(",") < s.rfind("."):
            raise ValueError("{}: '{}' memakai format Inggris. Tulis dengan titik untuk ribuan dan koma "
                             "untuk desimal, mis. 1.250.000,50".format(nama, asli))
        utuh, _, desimal = s.rpartition(",")
        _cek_ribuan(utuh.split("."), asli, nama)
        s = utuh.replace(".", "") + "." + desimal
    elif "," in s:
        bagian = s.split(",")
        if len(bagian) == 2:
            s = (bagian[0] or "0") + "." + bagian[1]       # koma tunggal = desimal
        else:
            _cek_ribuan(bagian, asli, nama)                # 1,250,000 (gaya ekspor)
            s = s.replace(",", "")
    elif "." in s:
        bagian = s.split(".")
        if len(bagian) == 2 and (len(bagian[1]) != 3 or bagian[0] in ("", "0")):
            s = (bagian[0] or "0") + "." + bagian[1]       # '2.5', '0.500' = desimal
        else:
            _cek_ribuan(bagian, asli, nama)
            s = s.replace(".", "")
    try:
        d = Decimal(s) * pengali
    except InvalidOperation:
        raise ValueError("{}: '{}' bukan angka yang valid".format(nama, asli))
    return -d if negatif else d


def format_rp(d, desimal=False):
    """Decimal -> 'Rp 1.250.000' (desimal=True menampilkan ',50' bila ada pecahan)."""
    d = Decimal(d).quantize(Decimal("0.01") if desimal else Decimal(1), ROUND_HALF_UP)
    neg = d < 0
    d = abs(d)
    teks = "{:,}".format(int(d)).replace(",", ".")
    if desimal:
        pecahan = "{:.2f}".format(d).split(".")[1]
        if pecahan != "00":
            teks += "," + pecahan
    return ("-" if neg else "") + "Rp " + teks


def format_angka(d):
    d = Decimal(d).normalize()
    teks = "{:f}".format(d)
    utuh, _, pecahan = teks.partition(".")
    utuh = "{:,}".format(int(utuh)).replace(",", ".")
    return utuh + ("," + pecahan if pecahan else "")


def ke_json(d):
    if isinstance(d, Decimal):
        return int(d) if d == d.to_integral_value() else float(d.quantize(Decimal("0.01"), ROUND_HALF_UP))
    raise TypeError(str(type(d)))


def bulatkan(nilai, cara):
    """Pembulatan rupiah penuh. 'bawah' = buang pecahan; 'terdekat' = >= 0,5 naik."""
    return Decimal(nilai).quantize(Decimal(1), ROUND_FLOOR if cara == "bawah" else ROUND_HALF_UP)


# ---------------------------------------------------------------- perhitungan inti
def hitung_ppn_dari_dpp(dpp, jenis="umum", pembulatan="bawah"):
    """Dari harga sebelum pajak (DPP) -> rincian PPN. dpp dalam rupiah (boleh pecahan)."""
    if jenis not in TARIF_EFEKTIF:
        raise ValueError("jenis harus 'umum' atau 'mewah'")
    dpp = Decimal(dpp)
    if dpp < 0:
        raise ValueError("harga tidak boleh negatif")
    dpp_nilai_lain_tepat = dpp * FAKTOR_NILAI_LAIN[jenis]
    ppn = bulatkan(dpp * TARIF_EFEKTIF[jenis], pembulatan)
    return {
        "jenis": jenis,
        "dpp": dpp,
        "dpp_nilai_lain": dpp_nilai_lain_tepat.quantize(Decimal("0.01"), ROUND_HALF_UP),
        "tarif_ppn_persen": Decimal(12),
        "tarif_efektif_persen": TARIF_EFEKTIF[jenis] * 100,
        "ppn": ppn,
        "total": dpp + ppn,
    }


def hitung_ppn_dari_total(total, jenis="umum", pembulatan="bawah"):
    """Dari harga yang SUDAH termasuk PPN -> pisahkan DPP & PPN.

    DPP dipilih = angka rupiah penuh terbesar sehingga DPP + PPN(DPP) <= harga termasuk PPN.
    Sisa (biasanya Rp 0-1) dilaporkan sebagai 'selisih_pembulatan'.
    """
    total = Decimal(total)
    if total < 0:
        raise ValueError("harga tidak boleh negatif")
    tarif = TARIF_EFEKTIF[jenis]
    kira = (total / (1 + tarif)).quantize(Decimal(1), ROUND_FLOOR) + 2
    dpp = kira
    while dpp > 0 and dpp + bulatkan(dpp * tarif, pembulatan) > total:
        dpp -= 1
    hasil = hitung_ppn_dari_dpp(dpp, jenis, pembulatan)
    hasil["harga_termasuk_ppn_input"] = total
    hasil["selisih_pembulatan"] = total - hasil["total"]
    return hasil


# ---------------------------------------------------------------- CLI
class ParserID(argparse.ArgumentParser):
    def error(self, message):
        sys.stderr.write("ERROR: argumen tidak valid ({}).\nLihat bantuan: python3 hitung_ppn.py --help\n"
                         .format(message))
        sys.exit(2)


def buat_teks(h, a, catatan):
    baris = []
    judul = "SIMULASI PPN (TIDAK BOLEH DITAGIHKAN)" if a.status_pkp == "non-pkp" else "PERHITUNGAN PPN"
    baris.append("=== {} ===".format(judul))
    baris.append("Jenis             : {}".format(
        "Barang/jasa umum (non-mewah) - DPP nilai lain 11/12" if h["jenis"] == "umum"
        else "Barang mewah (kena PPnBM) - 12% x harga"))
    if a.mode == "termasuk":
        baris.append("Harga termasuk PPN: {}".format(format_rp(h["harga_termasuk_ppn_input"], True)))
    if a.qty != 1:
        baris.append("Jumlah            : {} x {}".format(format_angka(a.qty), format_rp(a.harga_satuan, True)))
    baris.append("DPP (harga jual)  : {}".format(format_rp(h["dpp"], True)))
    if h["jenis"] == "umum":
        baris.append("DPP nilai lain    : {}  (11/12 x DPP)".format(format_rp(h["dpp_nilai_lain"], True)))
        baris.append("PPN 12%           : {}  (12% x DPP nilai lain = efektif 11%)".format(format_rp(h["ppn"])))
    else:
        baris.append("PPN 12%           : {}  (12% x DPP)".format(format_rp(h["ppn"])))
    baris.append("TOTAL (DPP + PPN) : {}".format(format_rp(h["total"], True)))
    if a.mode == "termasuk" and h["selisih_pembulatan"] != 0:
        baris.append("Selisih pembulatan: {} (harga termasuk PPN - total hitung)".format(
            format_rp(h["selisih_pembulatan"], True)))
    if a.status_pkp != "non-pkp":
        # Blok siap tempel untuk penawaran/chat: WAJIB memuat baris DPP nilai lain (non-mewah) agar pembaca
        # tidak mengira "12% x harga" salah hitung.
        baris.append("")
        baris.append("--- Teks siap tempel (penawaran/chat) ---")
        baris.append("Harga sebelum PPN (DPP)  : {}".format(format_rp(h["dpp"], True)))
        if h["jenis"] == "umum":
            baris.append("DPP nilai lain (11/12)   : {}".format(format_rp(h["dpp_nilai_lain"], True)))
            baris.append("PPN 12% x DPP nilai lain : {}".format(format_rp(h["ppn"])))
        else:
            baris.append("PPN 12% (barang mewah)   : {}".format(format_rp(h["ppn"])))
        baris.append("Total                    : {}".format(format_rp(h["total"], True)))
    baris.append("")
    baris.append("Pembulatan: " + CATATAN_PEMBULATAN)
    for c in catatan:
        baris.append("! " + c)
    baris.append("")
    baris.append("Dasar: {} - berlaku per {}. Ini alat bantu hitung, bukan nasihat pajak; "
                 "untuk kasus khusus hubungi DJP (Kring Pajak 1500200) atau konsultan pajak.".format(
                     DASAR_ATURAN, TANGGAL_ATURAN))
    return "\n".join(baris)


def main(argv=None):
    p = ParserID(description="Kalkulator PPN 12% (DPP nilai lain 11/12 untuk non-mewah).")
    p.add_argument("--harga", required=True, help="Harga per unit, mis. 'Rp 1.000.000' atau 1,5jt")
    p.add_argument("--qty", default="1", help="Jumlah unit (default 1)")
    p.add_argument("--mode", choices=["sebelum", "termasuk"], default="sebelum",
                   help="'sebelum' = harga belum termasuk PPN (default); 'termasuk' = harga sudah termasuk PPN")
    p.add_argument("--jenis", choices=["umum", "mewah"], default="umum",
                   help="'umum' = non-mewah (default); 'mewah' = barang kena PPnBM")
    p.add_argument("--status-pkp", choices=["pkp", "non-pkp", "belum-tahu"], default="belum-tahu",
                   help="Status penjual. Hanya PKP yang boleh memungut PPN.")
    p.add_argument("--format", choices=["teks", "json"], default="teks")
    a = p.parse_args(argv)

    try:
        harga = parse_angka(a.harga, "harga")
        qty = parse_angka(a.qty, "qty")
        if harga < 0:
            raise ValueError("harga tidak boleh negatif")
        if qty <= 0:
            raise ValueError("qty harus lebih dari 0")
        a.harga_satuan, a.qty = harga, qty
        nilai = harga * qty
        if a.mode == "sebelum":
            h = hitung_ppn_dari_dpp(nilai, a.jenis)
        else:
            h = hitung_ppn_dari_total(nilai, a.jenis)
    except ValueError as e:
        sys.stderr.write("ERROR: {}\n".format(e))
        return 2

    catatan = []
    if a.status_pkp == "non-pkp":
        catatan.append("Penjual BUKAN PKP: TIDAK BOLEH memungut PPN atau membuat faktur pajak. "
                       "Angka di atas hanya simulasi; tagih harga tanpa PPN.")
        if a.mode == "termasuk":
            catatan.append("Bagi non-PKP, seluruh harga {} adalah harga jual biasa (tanpa PPN).".format(
                format_rp(nilai, True)))
    elif a.status_pkp == "belum-tahu":
        catatan.append("Pastikan penjual sudah dikukuhkan sebagai PKP sebelum menagih PPN. "
                       "Jika belum PKP, jangan cantumkan PPN di tagihan.")
    if nilai == 0:
        catatan.append("Harga 0: tidak ada PPN.")
    if a.jenis == "mewah":
        catatan.append("PPnBM (pajak barang mewah) dihitung terpisah dan TIDAK termasuk di sini.")

    if a.format == "json":
        keluaran = {
            "status_pkp": a.status_pkp,
            "boleh_memungut_ppn": a.status_pkp == "pkp",
            "mode": a.mode,
            "harga_satuan": harga,
            "qty": qty,
            "hasil": h,
            "pembulatan": CATATAN_PEMBULATAN,
            "catatan": catatan,
            "dasar_aturan": DASAR_ATURAN,
            "berlaku_per": TANGGAL_ATURAN,
        }
        print(json.dumps(keluaran, default=ke_json, ensure_ascii=False, indent=2))
    else:
        print(buat_teks(h, a, catatan))
    return 0


if __name__ == "__main__":
    sys.exit(main())
