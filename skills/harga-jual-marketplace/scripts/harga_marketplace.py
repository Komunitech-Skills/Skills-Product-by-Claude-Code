#!/usr/bin/env python3
"""Hitung harga jual marketplace (Shopee, Tokopedia, TikTok Shop, dll.) agar target laba tercapai.

Dua mode:
1. Cari harga : dari modal + biaya platform + target -> harga minimal (balik modal) & harga rekomendasi.
2. Cek harga  : dari harga jual (--harga-jual) -> rincian potongan & laba bersih.

SEMUA persentase biaya platform diisi pengguna (cek Seller Center masing-masing; angka berubah-ubah).
PPh 22 marketplace 0,5% (PMK 37/2025, berlaku 1 Agustus 2026) ikut dihitung kecuali --pph22 tidak.

Asumsi dasar (tulis di hasil):
- Biaya persen (admin, layanan, pembayaran, iklan) & PPh 22 dihitung dari HARGA SETELAH VOUCHER TOKO.
- Biaya per pesanan dibagi rata ke jumlah barang per pesanan.
- Biaya dihitung tanpa pembulatan; tampilan dibulatkan ke rupiah terdekat.

Hanya library standar Python 3.8+. Tidak ada akses jaringan.

Contoh:
  python3 harga_marketplace.py --modal 35000 --admin 8 --layanan 4 --maks-layanan 10000 \
      --pembayaran 1,5 --per-pesanan 1250 --target-margin 20
  python3 harga_marketplace.py --modal 35000 --admin 8 --layanan 4 --harga-jual 59900
  python3 harga_marketplace.py --config platform.json --format json
"""
import argparse
import json
import re
import sys
from decimal import Decimal, ROUND_CEILING, ROUND_HALF_UP, InvalidOperation

TANGGAL_ATURAN = "2026-09-23"
VERSI = "1.0.4"
TARIF_PPH22 = Decimal("0.5")
BATAS_ATAS_HARGA = Decimal(10) ** 12
PERINGATAN_CONTOH = ("ANGKA CONTOH: persentase biaya platform di hasil ini berasal dari template contoh, BUKAN tarif "
                     "resmi. Ganti dengan angka terbaru dari Seller Center masing-masing sebelum memakai harga ini.")


# ---------------------------------------------------------------- angka & format
_PENGALI = [("miliar", 10 ** 9), ("milyar", 10 ** 9), ("juta", 10 ** 6), ("ribu", 10 ** 3),
            ("jt", 10 ** 6), ("rb", 10 ** 3), ("k", 10 ** 3)]


def _cek_ribuan(bagian, asli, nama):
    if not (1 <= len(bagian[0]) <= 3) or any(len(b) != 3 for b in bagian[1:]):
        raise ValueError("{}: '{}' tidak dikenali. Pakai titik untuk ribuan dan koma untuk desimal, "
                         "mis. 1.250.000 atau 1.250.000,50".format(nama, asli))


def parse_angka(nilai, nama="angka"):
    """Baca angka format Indonesia: 'Rp 15.000', '15.000,50', '1,5 jt', '2,5%', '15000'."""
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
    s = re.sub(r"[,.]-+$", "", s)
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
            s = (bagian[0] or "0") + "." + bagian[1]
        else:
            _cek_ribuan(bagian, asli, nama)
            s = s.replace(",", "")
    elif "." in s:
        bagian = s.split(".")
        if len(bagian) == 2 and (len(bagian[1]) != 3 or bagian[0] in ("", "0")):
            s = (bagian[0] or "0") + "." + bagian[1]
        else:
            _cek_ribuan(bagian, asli, nama)
            s = s.replace(".", "")
    try:
        d = Decimal(s) * pengali
    except InvalidOperation:
        raise ValueError("{}: '{}' bukan angka yang valid".format(nama, asli))
    return -d if negatif else d


def format_rp(d, desimal=False):
    d = Decimal(d).quantize(Decimal("0.01") if desimal else Decimal(1), ROUND_HALF_UP)
    neg = d < 0
    d = abs(d)
    teks = "{:,}".format(int(d)).replace(",", ".")
    if desimal:
        pecahan = "{:.2f}".format(d).split(".")[1]
        if pecahan != "00":
            teks += "," + pecahan
    return ("-" if neg else "") + "Rp " + teks


def format_persen(d):
    d = Decimal(d).quantize(Decimal("0.01"), ROUND_HALF_UP).normalize()
    teks = "{:f}".format(d)
    return teks.replace(".", ",") + "%"


def ke_json(d):
    if isinstance(d, Decimal):
        return int(d) if d == d.to_integral_value() else float(d.quantize(Decimal("0.01"), ROUND_HALF_UP))
    raise TypeError(str(type(d)))


# ---------------------------------------------------------------- model biaya
def angka_opsional(v, nama, default=None):
    if v is None or (isinstance(v, str) and not v.strip()):
        return default
    return parse_angka(v, nama)


def siapkan_platform(cfg, nama_default="Marketplace"):
    """Ubah dict konfigurasi (dari CLI/JSON) menjadi model biaya yang tervalidasi."""
    nama = str(cfg.get("nama") or nama_default)
    biaya = []
    for kunci, label in (("admin", "Biaya admin/komisi"), ("layanan", "Biaya layanan/program ongkir"),
                         ("pembayaran", "Biaya pembayaran/transaksi"), ("iklan", "Biaya iklan (perkiraan)")):
        persen = angka_opsional(cfg.get(kunci), "{} {}".format(kunci, nama), Decimal(0))
        maks = angka_opsional(cfg.get("maks_" + kunci), "maks_{} {}".format(kunci, nama))
        if persen < 0 or persen >= 100:
            raise ValueError("{} {}: persen harus 0 sampai di bawah 100".format(label, nama))
        if maks is not None and maks < 0:
            raise ValueError("batas maksimum {} {} tidak boleh negatif".format(kunci, nama))
        biaya.append({"kunci": kunci, "label": label, "persen": persen, "maks": maks})
    per_pesanan = angka_opsional(cfg.get("per_pesanan"), "biaya per pesanan " + nama, Decimal(0))
    qty = angka_opsional(cfg.get("qty_per_pesanan"), "qty per pesanan " + nama, Decimal(1))
    lain = angka_opsional(cfg.get("biaya_lain"), "biaya lain " + nama, Decimal(0))
    if per_pesanan < 0 or lain < 0:
        raise ValueError("biaya per pesanan / biaya lain {} tidak boleh negatif".format(nama))
    if qty <= 0 or qty != qty.to_integral_value():
        raise ValueError("qty per pesanan {} harus bilangan bulat >= 1".format(nama))

    voucher_teks = cfg.get("voucher")
    voucher = {"jenis": "tidak", "nilai": Decimal(0), "maks": None}
    if voucher_teks not in (None, "", 0, "0"):
        persen = isinstance(voucher_teks, str) and voucher_teks.strip().endswith("%")
        nilai = parse_angka(voucher_teks, "voucher " + nama)
        if nilai < 0:
            raise ValueError("voucher {} tidak boleh negatif".format(nama))
        if persen and nilai >= 100:
            raise ValueError("voucher persen {} harus di bawah 100%".format(nama))
        voucher = {"jenis": "persen" if persen else "rupiah", "nilai": nilai,
                   "maks": angka_opsional(cfg.get("maks_voucher"), "maks voucher " + nama)}

    pph22 = str(cfg.get("pph22", "ya")).strip().lower()
    if pph22 not in ("ya", "tidak"):
        raise ValueError("pph22 {} harus 'ya' atau 'tidak'".format(nama))
    return {"nama": nama, "biaya": biaya, "per_pesanan": per_pesanan, "qty_per_pesanan": qty,
            "biaya_lain": lain, "voucher": voucher, "pph22": pph22 == "ya"}


def rincian(harga, modal, pf):
    """Rincian potongan & laba untuk satu harga tayang (per unit)."""
    harga = Decimal(harga)
    v = pf["voucher"]
    if v["jenis"] == "persen":
        pot = harga * v["nilai"] / 100
        if v["maks"] is not None:
            pot = min(pot, v["maks"])
    elif v["jenis"] == "rupiah":
        pot = min(v["nilai"], harga)
    else:
        pot = Decimal(0)
    dasar = harga - pot  # harga setelah voucher toko = dasar biaya persen & PPh 22
    potongan = []
    for b in pf["biaya"]:
        if b["persen"] == 0:
            continue
        nilai = dasar * b["persen"] / 100
        kena_maks = b["maks"] is not None and nilai > b["maks"]
        if kena_maks:
            nilai = b["maks"]
        potongan.append({"nama": b["label"], "persen": b["persen"], "nilai": nilai, "kena_batas_maks": kena_maks})
    if pf["per_pesanan"]:
        potongan.append({"nama": "Biaya per pesanan (dibagi {} barang)".format(pf["qty_per_pesanan"]),
                         "persen": None, "nilai": pf["per_pesanan"] / pf["qty_per_pesanan"],
                         "kena_batas_maks": False})
    pph = dasar * TARIF_PPH22 / 100 if pf["pph22"] else Decimal(0)
    if pf["pph22"]:
        potongan.append({"nama": "PPh 22 marketplace", "persen": TARIF_PPH22, "nilai": pph,
                         "kena_batas_maks": False})
    total_potongan = sum((p["nilai"] for p in potongan), Decimal(0))
    diterima = dasar - total_potongan
    laba = diterima - modal - pf["biaya_lain"]
    return {
        "harga_tayang": harga,
        "voucher_toko": pot,
        "harga_setelah_voucher": dasar,
        "potongan": potongan,
        "total_potongan": total_potongan,
        "uang_diterima": diterima,
        "modal": modal,
        "biaya_lain": pf["biaya_lain"],
        "laba_bersih": laba,
        "margin_persen": (laba / dasar * 100) if dasar > 0 else None,
        "markup_persen": (laba / modal * 100) if modal > 0 else None,
    }


def memenuhi(r, target):
    jenis, nilai = target
    if jenis == "margin":
        return r["laba_bersih"] >= r["harga_setelah_voucher"] * nilai / 100 and r["laba_bersih"] >= 0
    if jenis == "laba":
        return r["laba_bersih"] >= nilai
    if jenis == "markup":
        return r["laba_bersih"] >= r["modal"] * nilai / 100
    return r["laba_bersih"] >= 0


def status_target(r, target):
    """Status harga terhadap target (v1.0.4): dikutip AI apa adanya, AI tidak menilai sendiri."""
    jenis, nilai = target
    if jenis == "impas":
        return None
    ok = memenuhi(r, target)
    if jenis == "margin":
        perlu = r["harga_setelah_voucher"] * nilai / 100
        nyata = "margin " + (format_persen(r["margin_persen"]) if r["margin_persen"] is not None else "-")
    elif jenis == "laba":
        perlu, nyata = nilai, "laba " + format_rp(r["laba_bersih"])
    else:
        perlu = r["modal"] * nilai / 100
        nyata = "markup " + (format_persen(r["markup_persen"]) if r["markup_persen"] is not None else "-")
    if ok:
        return "MEMENUHI target {} ({})".format(label_target(target), nyata)
    kurang = max(perlu, Decimal(0)) - r["laba_bersih"]
    return "DI BAWAH target {} ({}; laba kurang {} per barang)".format(label_target(target), nyata, format_rp(kurang))


def cari_harga(modal, pf, target):
    """Harga tayang (rupiah bulat) terkecil yang memenuhi target. Laba naik seiring harga (sudah dicek)."""
    if memenuhi(rincian(0, modal, pf), target):
        return Decimal(0)
    hi = Decimal(1)
    while not memenuhi(rincian(hi, modal, pf), target):
        hi *= 2
        if hi > BATAS_ATAS_HARGA:
            raise ValueError("target tidak mungkin tercapai dengan biaya ini (harga > Rp 1 triliun). "
                             "Periksa persentase biaya dan target.")
    lo = hi // 2
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if memenuhi(rincian(mid, modal, pf), target):
            hi = mid
        else:
            lo = mid
    return hi


def cek_kelayakan(pf, target):
    """Pastikan total persen < 100% agar harga naik -> laba naik (hasil pencarian pasti tepat)."""
    total = sum((b["persen"] for b in pf["biaya"]), Decimal(0)) + (TARIF_PPH22 if pf["pph22"] else 0)
    if target[0] == "margin":
        total += target[1]
    if total >= 100:
        raise ValueError("{}: total persen biaya{} = {} (>= 100%). Target tidak mungkin tercapai; turunkan "
                         "target margin atau periksa angka biaya.".format(
                             pf["nama"], " + target margin" if target[0] == "margin" else "", format_persen(total)))


def bulatkan_atas(nilai, kelipatan):
    if kelipatan <= 1:
        return nilai
    return (nilai / kelipatan).quantize(Decimal(1), ROUND_CEILING) * kelipatan


def banding(modal, pf, target, daftar_harga):
    out = []
    for h in daftar_harga or []:
        rr = rincian(h, modal, pf)
        out.append({"harga_tayang": h, "rincian": rr,
                    "memenuhi_target": memenuhi(rr, target) if target[0] != "impas" else rr["laba_bersih"] >= 0,
                    "status_target": status_target(rr, target)})
    return out


def hitung_platform(modal, pf, target, harga_jual=None, kelipatan=Decimal(500), daftar_banding=None):
    if harga_jual is not None:
        r0 = rincian(harga_jual, modal, pf)
        return {"platform": pf["nama"], "mode": "cek_harga", "rincian": r0,
                "status_target": status_target(r0, target), "banding": banding(modal, pf, target, daftar_banding)}
    cek_kelayakan(pf, target)
    h_min = cari_harga(modal, pf, ("impas", 0))
    h_target = cari_harga(modal, pf, target)
    h_rek = bulatkan_atas(h_target, kelipatan)
    return {
        "platform": pf["nama"],
        "mode": "cari_harga",
        "harga_minimal_impas": h_min,
        "harga_tepat_target": h_target,
        "harga_rekomendasi": h_rek,
        "rincian_minimal": rincian(h_min, modal, pf),
        "rincian_rekomendasi": rincian(h_rek, modal, pf),
        "status_target": status_target(rincian(h_rek, modal, pf), target),
        "banding": banding(modal, pf, target, daftar_banding),
    }


# ---------------------------------------------------------------- output teks
def label_target(target):
    jenis, nilai = target
    return {"margin": "margin {} dari harga setelah voucher".format(format_persen(nilai)),
            "laba": "laba {} per barang".format(format_rp(nilai)),
            "markup": "markup {} dari modal".format(format_persen(nilai)),
            "impas": "balik modal (laba Rp 0)"}[jenis]


def tabel_rincian(r):
    out = ["| Komponen | Nilai |", "|---|---:|",
           "| Harga tayang | {} |".format(format_rp(r["harga_tayang"]))]
    if r["voucher_toko"]:
        out.append("| Voucher toko | -{} |".format(format_rp(r["voucher_toko"])))
        out.append("| Harga setelah voucher | {} |".format(format_rp(r["harga_setelah_voucher"])))
    for p in r["potongan"]:
        label = p["nama"] + (" ({})".format(format_persen(p["persen"])) if p["persen"] is not None else "")
        if p["kena_batas_maks"]:
            label += " - kena batas maks."
        out.append("| {} | -{} |".format(label, format_rp(p["nilai"])))
    out.append("| **Uang diterima dari marketplace** | **{}** |".format(format_rp(r["uang_diterima"])))
    out.append("| Modal/HPP | -{} |".format(format_rp(r["modal"])))
    if r["biaya_lain"]:
        out.append("| Biaya lain per barang | -{} |".format(format_rp(r["biaya_lain"])))
    out.append("| **Laba bersih per barang** | **{}** |".format(format_rp(r["laba_bersih"])))
    m = format_persen(r["margin_persen"]) if r["margin_persen"] is not None else "-"
    k = format_persen(r["markup_persen"]) if r["markup_persen"] is not None else "-"
    out.append("| Margin (laba / harga setelah voucher) | {} |".format(m))
    out.append("| Markup (laba / modal) | {} |".format(k))
    return out


def tabel_banding(h, target):
    out = ["", "Banding harga (dihitung script; kutip baris ini, jangan menilai sendiri):", "",
           "| Harga tayang | Uang diterima | Laba/barang | Margin | Status target |", "|---:|---:|---:|---:|---|"]
    for b in h["banding"]:
        r = b["rincian"]
        st = b["status_target"] or ("untung" if r["laba_bersih"] >= 0 else "RUGI")
        out.append("| {} | {} | {} | {} | {} |".format(
            format_rp(r["harga_tayang"]), format_rp(r["uang_diterima"]), format_rp(r["laba_bersih"]),
            format_persen(r["margin_persen"]) if r["margin_persen"] is not None else "-", st))
    return out


def teks_hasil(hasil, modal, target, kelipatan, catatan):
    out = []
    if len(hasil) > 1:
        out.append("## Perbandingan harga per platform")
        out.append("")
        if hasil[0]["mode"] == "cari_harga":
            out.append("| Platform | Harga minimal (impas) | Harga rekomendasi | Laba/barang | Margin |")
            out.append("|---|---:|---:|---:|---:|")
            for h in hasil:
                r = h["rincian_rekomendasi"]
                out.append("| {} | {} | {} | {} | {} |".format(
                    h["platform"], format_rp(h["harga_minimal_impas"]), format_rp(h["harga_rekomendasi"]),
                    format_rp(r["laba_bersih"]), format_persen(r["margin_persen"]) if r["margin_persen"] is not None else "-"))
        else:
            out.append("| Platform | Harga jual | Uang diterima | Laba/barang | Margin |")
            out.append("|---|---:|---:|---:|---:|")
            for h in hasil:
                r = h["rincian"]
                out.append("| {} | {} | {} | {} | {} |".format(
                    h["platform"], format_rp(r["harga_tayang"]), format_rp(r["uang_diterima"]),
                    format_rp(r["laba_bersih"]), format_persen(r["margin_persen"]) if r["margin_persen"] is not None else "-"))
        out.append("")
    for h in hasil:
        if h["mode"] == "cari_harga":
            out.append("### {} - target {}".format(h["platform"], label_target(target)))
            out.append("- Harga minimal agar tidak rugi: **{}**".format(format_rp(h["harga_minimal_impas"])))
            out.append("- Harga tepat sesuai target: {}".format(format_rp(h["harga_tepat_target"])))
            out.append("- **Harga rekomendasi (dibulatkan ke atas kelipatan {}): {}**".format(
                format_rp(kelipatan), format_rp(h["harga_rekomendasi"])))
            out.append("")
            out.append("Rincian pada harga rekomendasi:")
            out.append("")
            out += tabel_rincian(h["rincian_rekomendasi"])
            out.append("")
            out.append("Status target pada harga rekomendasi: **{}**".format(h["status_target"]))
            if h["banding"]:
                out += tabel_banding(h, target)
        else:
            r = h["rincian"]
            out.append("### {} - cek harga {}".format(h["platform"], format_rp(r["harga_tayang"])))
            out.append("")
            out += tabel_rincian(r)
            if r["laba_bersih"] < 0:
                out.append("")
                out.append("RUGI {} per barang pada harga ini.".format(format_rp(-r["laba_bersih"])))
            if h["status_target"]:
                out.append("")
                out.append("Status target: **{}**".format(h["status_target"]))
            if h["banding"]:
                out += tabel_banding(h, target)
        out.append("")
    out.append("**Catatan & asumsi**")
    for c in catatan:
        out.append("- " + c)
    return "\n".join(out)


# ---------------------------------------------------------------- CLI
class ParserID(argparse.ArgumentParser):
    def error(self, message):
        sys.stderr.write("ERROR: argumen tidak valid ({}).\nLihat bantuan: python3 harga_marketplace.py --help\n"
                         .format(message))
        sys.exit(2)


def main(argv=None):
    p = ParserID(description="Harga jual marketplace: harga minimal, rekomendasi, dan cek laba bersih.")
    p.add_argument("--config", help="File JSON berisi modal, target, dan daftar platform (untuk perbandingan)")
    p.add_argument("--modal", help="Modal/HPP per barang termasuk kemasan, mis. 35.000")
    p.add_argument("--platform", default="Marketplace", help="Nama platform untuk label")
    for k, h in (("admin", "Biaya admin/komisi (%%)"), ("layanan", "Biaya layanan / program gratis ongkir (%%)"),
                 ("pembayaran", "Biaya pembayaran/transaksi (%%)"), ("iklan", "Biaya iklan (%%) - opsional")):
        p.add_argument("--" + k, help=h)
        p.add_argument("--maks-" + k, help="Batas maksimum {} per barang (Rp), jika ada".format(k))
    p.add_argument("--per-pesanan", help="Biaya tetap per pesanan (Rp), mis. biaya proses pesanan")
    p.add_argument("--qty-per-pesanan", help="Rata-rata jumlah barang per pesanan (default 1)")
    p.add_argument("--biaya-lain", help="Biaya lain per barang di luar modal (Rp), mis. packing tambahan")
    p.add_argument("--voucher", help="Voucher toko yang ditanggung penjual: '10%%' atau '5000'")
    p.add_argument("--maks-voucher", help="Batas maksimum potongan voucher persen (Rp)")
    p.add_argument("--pph22", choices=["ya", "tidak"], default=None,
                   help="Potong PPh 22 marketplace 0,5%% (default ya). 'tidak' bila sudah menyerahkan surat pernyataan/SKB")
    g = p.add_mutually_exclusive_group()
    g.add_argument("--target-margin", help="Target margin %% dari harga setelah voucher (default 20)")
    g.add_argument("--target-laba", help="Target laba bersih Rp per barang")
    g.add_argument("--target-markup", help="Target markup %% dari modal")
    p.add_argument("--harga-jual", help="Mode cek: harga tayang yang ingin dicek labanya (boleh digabung dengan "
                                        "--target-*, script lalu mencetak status target)")
    p.add_argument("--banding-harga", help="Harga lain yang ingin dicek terhadap target, dipisah ';', "
                                           "mis. '62.900;59.900' (v1.0.4)")
    p.add_argument("--bulatkan", default="500", help="Kelipatan pembulatan ke atas harga rekomendasi (default 500; 1 = tanpa)")
    p.add_argument("--format", choices=["teks", "json"], default="teks")
    a = p.parse_args(argv)

    try:
        cfg = {}
        if a.config:
            try:
                with open(a.config, encoding="utf-8-sig") as f:
                    cfg = json.load(f)
            except OSError as e:
                raise ValueError("file '{}' tidak bisa dibaca: {}".format(a.config, e.strerror or e))
            except json.JSONDecodeError as e:
                raise ValueError("JSON tidak valid (baris {}): {}".format(e.lineno, e.msg))
            if not isinstance(cfg, dict):
                raise ValueError("isi JSON harus objek {\"modal\": ..., \"platform\": [...]}")
        modal_teks = a.modal if a.modal is not None else cfg.get("modal")
        if modal_teks is None:
            raise ValueError("modal/HPP per barang wajib diisi (--modal)")
        modal = parse_angka(modal_teks, "modal")
        if modal < 0:
            raise ValueError("modal tidak boleh negatif")

        # target
        harga_jual = a.harga_jual if a.harga_jual is not None else cfg.get("harga_jual")
        target, asumsi_target = None, False
        for jenis, cli in (("margin", a.target_margin), ("laba", a.target_laba), ("markup", a.target_markup)):
            nilai = cli if cli is not None else cfg.get("target_" + jenis)
            if nilai is not None and target is None:
                target = (jenis, parse_angka(nilai, "target " + jenis))
        if harga_jual is not None:
            harga_jual = parse_angka(harga_jual, "harga jual")
            if harga_jual < 0:
                raise ValueError("harga jual tidak boleh negatif")
            target = target or ("impas", Decimal(0))
        elif target is None:
            target, asumsi_target = ("margin", Decimal(20)), True
        if target[1] < 0:
            raise ValueError("target tidak boleh negatif")
        kelipatan = parse_angka(a.bulatkan if a.bulatkan is not None else cfg.get("bulatkan", 500), "bulatkan")
        if kelipatan < 1 or kelipatan != kelipatan.to_integral_value():
            raise ValueError("--bulatkan harus bilangan bulat >= 1")

        # platform
        if cfg.get("platform"):
            if not isinstance(cfg["platform"], list):
                raise ValueError("'platform' di JSON harus berupa daftar")
            daftar = [siapkan_platform(x, "Platform {}".format(i + 1)) for i, x in enumerate(cfg["platform"])]
        else:
            cli = {"nama": a.platform}
            for k in ("admin", "layanan", "pembayaran", "iklan"):
                cli[k] = getattr(a, k)
                cli["maks_" + k] = getattr(a, "maks_" + k)
            cli.update({"per_pesanan": a.per_pesanan, "qty_per_pesanan": a.qty_per_pesanan,
                        "biaya_lain": a.biaya_lain, "voucher": a.voucher, "maks_voucher": a.maks_voucher,
                        "pph22": a.pph22 or cfg.get("pph22", "ya")})
            daftar = [siapkan_platform(cli)]
        if a.pph22 and cfg.get("platform"):
            for pf in daftar:
                pf["pph22"] = a.pph22 == "ya"
        bh = a.banding_harga if a.banding_harga is not None else cfg.get("banding_harga")
        daftar_banding = []
        if bh is not None:
            bagian = bh if isinstance(bh, list) else str(bh).split(";")
            for x in bagian:
                if str(x).strip():
                    v = parse_angka(x, "banding harga")
                    if v < 0:
                        raise ValueError("banding harga tidak boleh negatif")
                    daftar_banding.append(v)
        hasil = [hitung_platform(modal, pf, target, harga_jual, kelipatan, daftar_banding) for pf in daftar]
    except ValueError as e:
        sys.stderr.write("ERROR: {}\n".format(e))
        return 2

    catatan = []
    angka_contoh = bool(cfg.get("angka_contoh")) or any(
        "(contoh" in pf["nama"].lower() for pf in daftar)
    if angka_contoh:
        catatan.insert(0, PERINGATAN_CONTOH)
    if modal == 0:
        catatan.append("Modal diisi Rp 0. Pastikan ini benar; tanpa modal, harga minimal hanya menutup biaya platform.")
    if asumsi_target:
        catatan.append("Target belum disebut, dipakai asumsi margin 20% dari harga setelah voucher.")
    if all(not any(b["persen"] for b in pf["biaya"]) and not pf["per_pesanan"] for pf in daftar):
        catatan.append("Semua biaya platform 0. Isi biaya admin/layanan dari Seller Center agar hasil akurat.")
    catatan += [
        "Persentase biaya platform berasal dari input Anda. Cek angka terbaru di Seller Center masing-masing "
        "(berbeda per kategori & program, dan bisa berubah).",
        "Biaya persen dan PPh 22 dihitung dari harga setelah voucher toko. Jika platform Anda memakai dasar lain, "
        "hasil bisa sedikit berbeda.",
        "Biaya dihitung tanpa pembulatan; angka di tabel dibulatkan ke rupiah terdekat.",
    ]
    if any(pf["pph22"] for pf in daftar):
        catatan.append("PPh 22 marketplace 0,5% (PMK 37/2025, berlaku 1 Agustus 2026). Penjual orang pribadi dengan "
                       "omzet setahun s.d. Rp500 juta bisa dikecualikan jika sudah menyampaikan surat pernyataan ke "
                       "marketplace; hitung ulang dengan --pph22 tidak. PPh 22 ini bukan pajak baru; cara "
                       "memperhitungkannya dengan PPh final Anda, tanyakan ke DJP/konsultan.")
    else:
        catatan.append("PPh 22 marketplace tidak dipotong (dianggap sudah menyerahkan surat pernyataan/SKB). "
                       "Pastikan status ini benar di Seller Center.")
    catatan.append("Berlaku per {}. Alat bantu hitung, bukan nasihat pajak.".format(TANGGAL_ATURAN))

    if a.format == "json":
        print(json.dumps({"modal": modal, "target": {"jenis": target[0], "nilai": target[1]},
                          "target_asumsi": asumsi_target, "angka_contoh": angka_contoh,
                          "peringatan": PERINGATAN_CONTOH if angka_contoh else None,
                          "hasil": hasil, "catatan": catatan},
                         default=ke_json, ensure_ascii=False, indent=2))
    else:
        if angka_contoh:
            print("> **!!! " + PERINGATAN_CONTOH + " !!!**")
            print("")
        print(teks_hasil(hasil, modal, target, kelipatan, catatan))
    return 0


if __name__ == "__main__":
    sys.exit(main())
