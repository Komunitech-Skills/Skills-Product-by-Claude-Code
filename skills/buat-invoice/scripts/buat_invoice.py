#!/usr/bin/env python3
"""Buat invoice / kuitansi profesional (Markdown + HTML siap cetak) dari file JSON.

Fitur: nomor otomatis, item + diskon per baris, diskon total, ongkir, PPN opsional (hanya PKP; logika sama
dengan skill hitung-ppn lewat scripts/hitung_ppn.py), DP/pembayaran & termin, sisa tagihan, terbilang,
rekening, jatuh tempo, dan penanda bea meterai Rp10.000 (UU 10/2020) bila dokumen menyatakan penerimaan
uang > Rp5.000.000.

Urutan hitung:
  jumlah baris   = qty x harga - diskon baris            (dibulatkan ke rupiah terdekat)
  subtotal       = jumlah semua baris
  setelah diskon = subtotal - diskon total               (diskon dibulatkan ke rupiah terdekat)
  DPP            = setelah diskon + ongkir (jika ongkir kena PPN)
  PPN            = 11% x DPP untuk non-mewah (12% x 11/12), 12% x DPP untuk mewah; dibulatkan ke bawah
  TOTAL          = setelah diskon + ongkir + PPN
  sisa tagihan   = TOTAL - pembayaran yang sudah diterima

Hanya library standar Python 3.8+. Tidak ada akses jaringan. File hanya ditulis ke path yang Anda berikan.

Contoh:
  python3 buat_invoice.py --file invoice.json
  python3 buat_invoice.py --file invoice.json --html invoice.html
  python3 buat_invoice.py --file invoice.json --nomor-terakhir INV/2026/09/0007
"""
import argparse
import datetime
import html
import json
import os
import re
import sys
from decimal import Decimal, ROUND_HALF_UP

sys.dont_write_bytecode = True  # jangan membuat __pycache__ di folder skill
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hitung_ppn import hitung_ppn_dari_dpp, parse_angka, format_rp, format_angka, ke_json  # noqa: E402

BATAS_METERAI = Decimal(5000000)
TARIF_METERAI = Decimal(10000)
TANGGAL_ATURAN = "2026-09-23"
NAMA_BULAN = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September",
              "Oktober", "November", "Desember"]


# ---------------------------------------------------------------- utilitas
def rupiah_bulat(d):
    return Decimal(d).quantize(Decimal(1), ROUND_HALF_UP)


def parse_tanggal(teks, nama):
    if isinstance(teks, datetime.date):
        return teks
    s = str(teks).strip()
    for fmt in ("%Y-%m-%d", "%d-%m-%Y", "%d/%m/%Y", "%d.%m.%Y"):
        try:
            return datetime.datetime.strptime(s, fmt).date()
        except ValueError:
            pass
    raise ValueError("{}: tanggal '{}' tidak dikenali (pakai 2026-09-23 atau 23/09/2026)".format(nama, teks))


def tanggal_id(d):
    return "{} {} {}".format(d.day, NAMA_BULAN[d.month - 1], d.year)


_SATUAN = ["", "satu", "dua", "tiga", "empat", "lima", "enam", "tujuh", "delapan", "sembilan", "sepuluh", "sebelas"]


def _terbilang(n):
    if n < 12:
        return _SATUAN[n]
    if n < 20:
        return _terbilang(n - 10) + " belas"
    if n < 100:
        return (_terbilang(n // 10) + " puluh " + _terbilang(n % 10)).strip()
    if n < 200:
        return ("seratus " + _terbilang(n - 100)).strip()
    if n < 1000:
        return (_terbilang(n // 100) + " ratus " + _terbilang(n % 100)).strip()
    if n < 2000:
        return ("seribu " + _terbilang(n - 1000)).strip()
    if n < 10 ** 6:
        return (_terbilang(n // 1000) + " ribu " + _terbilang(n % 1000)).strip()
    if n < 10 ** 9:
        return (_terbilang(n // 10 ** 6) + " juta " + _terbilang(n % 10 ** 6)).strip()
    if n < 10 ** 12:
        return (_terbilang(n // 10 ** 9) + " miliar " + _terbilang(n % 10 ** 9)).strip()
    if n < 10 ** 15:
        return (_terbilang(n // 10 ** 12) + " triliun " + _terbilang(n % 10 ** 12)).strip()
    raise ValueError("nilai terlalu besar untuk terbilang")


def terbilang(d):
    n = int(rupiah_bulat(d))
    if n < 0:
        return "Minus " + terbilang(-n)
    kata = "nol" if n == 0 else re.sub(r"\s+", " ", _terbilang(n))
    return " ".join(w.capitalize() for w in kata.split()) + " Rupiah"


def potongan(teks, dasar, nama):
    """Diskon '10%' (dari dasar) atau nominal rupiah. Hasil dibulatkan ke rupiah terdekat."""
    if teks in (None, "", 0, "0"):
        return Decimal(0), None
    persen = isinstance(teks, str) and teks.strip().endswith("%")
    nilai = parse_angka(teks, nama)
    if nilai < 0:
        raise ValueError("{} tidak boleh negatif".format(nama))
    if persen:
        if nilai > 100:
            raise ValueError("{} tidak boleh lebih dari 100%".format(nama))
        return rupiah_bulat(dasar * nilai / 100), nilai
    if nilai > dasar:
        raise ValueError("{} ({}) melebihi nilai yang didiskon ({})".format(nama, format_rp(nilai), format_rp(dasar)))
    return rupiah_bulat(nilai), None


def nomor_berikutnya(terakhir):
    m = re.search(r"(\d+)(?!.*\d)", terakhir)
    if not m:
        raise ValueError("nomor terakhir '{}' tidak mengandung angka urut".format(terakhir))
    angka = m.group(1)
    baru = str(int(angka) + 1).zfill(len(angka))
    return terakhir[:m.start(1)] + baru + terakhir[m.end(1):]


def nomor_dari_counter(path, prefix, tgl):
    kunci = "{}/{}/{:02d}".format(prefix, tgl.year, tgl.month)
    data = {}
    if os.path.exists(path):
        try:
            with open(path, encoding="utf-8") as f:
                data = json.load(f)
        except (OSError, json.JSONDecodeError):
            raise ValueError("file counter '{}' rusak atau tidak bisa dibaca".format(path))
        if not isinstance(data, dict):
            raise ValueError("file counter '{}' harus berisi objek JSON".format(path))
    urut = int(data.get(kunci, 0)) + 1
    data[kunci] = urut
    return "{}/{:04d}".format(kunci, urut), data


# ---------------------------------------------------------------- perhitungan
def hitung(d):
    jenis_dok = str(d.get("jenis_dokumen") or "invoice").strip().lower()
    if jenis_dok not in ("invoice", "kuitansi"):
        raise ValueError("jenis_dokumen harus 'invoice' atau 'kuitansi'")
    penjual = d.get("penjual") or {}
    pembeli = d.get("pembeli") or {}
    if not isinstance(penjual, dict) or not penjual.get("nama"):
        raise ValueError("penjual.nama wajib diisi")
    if not isinstance(pembeli, dict) or not pembeli.get("nama"):
        raise ValueError("pembeli.nama wajib diisi")

    items = d.get("items")
    if not isinstance(items, list) or not items:
        raise ValueError("'items' wajib berisi minimal 1 barang/jasa")
    baris = []
    for i, it in enumerate(items, 1):
        if not isinstance(it, dict) or not str(it.get("nama") or "").strip():
            raise ValueError("item ke-{}: 'nama' wajib diisi".format(i))
        nama = str(it["nama"]).strip()
        qty = parse_angka(it.get("qty", 1), "qty item '{}'".format(nama))
        harga = parse_angka(it.get("harga"), "harga item '{}'".format(nama))
        if qty <= 0:
            raise ValueError("qty item '{}' harus lebih dari 0".format(nama))
        if harga < 0:
            raise ValueError("harga item '{}' tidak boleh negatif".format(nama))
        bruto = rupiah_bulat(qty * harga)
        disk, disk_persen = potongan(it.get("diskon"), bruto, "diskon item '{}'".format(nama))
        baris.append({"no": i, "nama": nama, "qty": qty, "satuan": str(it.get("satuan") or ""),
                      "harga": harga, "bruto": bruto, "diskon": disk, "diskon_persen": disk_persen,
                      "jumlah": bruto - disk})
    subtotal = sum((b["jumlah"] for b in baris), Decimal(0))
    diskon, diskon_persen = potongan(d.get("diskon"), subtotal, "diskon total")
    setelah_diskon = subtotal - diskon
    ongkir = parse_angka(d.get("ongkir") or 0, "ongkir")
    if ongkir < 0:
        raise ValueError("ongkir tidak boleh negatif")
    ongkir = rupiah_bulat(ongkir)

    # PPN
    cfg_ppn = d.get("ppn") or False
    if isinstance(cfg_ppn, dict):
        ppn_aktif = bool(cfg_ppn.get("aktif", True))
        jenis_ppn = str(cfg_ppn.get("jenis") or "umum").lower()
        ongkir_kena = bool(cfg_ppn.get("ongkir_kena_ppn", True))
    else:
        ppn_aktif, jenis_ppn, ongkir_kena = bool(cfg_ppn), "umum", True
    pkp = bool(penjual.get("pkp", False))
    ppn = None
    if ppn_aktif:
        if not pkp:
            raise ValueError("PPN hanya boleh dipungut oleh PKP. Jika Anda sudah PKP, isi \"pkp\": true di data "
                             "penjual; jika belum, matikan PPN (\"ppn\": false).")
        if jenis_ppn not in ("umum", "mewah"):
            raise ValueError("ppn.jenis harus 'umum' atau 'mewah'")
        dpp = setelah_diskon + (ongkir if ongkir_kena else 0)
        ppn = hitung_ppn_dari_dpp(dpp, jenis_ppn, "bawah")
        ppn["ongkir_kena_ppn"] = ongkir_kena
    total = setelah_diskon + ongkir + (ppn["ppn"] if ppn else 0)

    # pembayaran
    bayar = []
    for i, p in enumerate(d.get("pembayaran") or [], 1):
        if not isinstance(p, dict):
            raise ValueError("pembayaran ke-{} harus berupa objek".format(i))
        jml = parse_angka(p.get("jumlah"), "jumlah pembayaran ke-{}".format(i))
        if jml <= 0:
            raise ValueError("jumlah pembayaran ke-{} harus lebih dari 0".format(i))
        tgl = parse_tanggal(p["tanggal"], "tanggal pembayaran ke-{}".format(i)) if p.get("tanggal") else None
        bayar.append({"tanggal": tgl, "jumlah": rupiah_bulat(jml), "keterangan": str(p.get("keterangan") or "")})
    if jenis_dok == "kuitansi" and not bayar:
        bayar = [{"tanggal": None, "jumlah": total, "keterangan": "Pembayaran"}]
    dibayar = sum((p["jumlah"] for p in bayar), Decimal(0))
    sisa = total - dibayar

    # termin
    termin = []
    daftar_termin = d.get("termin") or []
    if daftar_termin:
        sisa_alok = total
        for i, t in enumerate(daftar_termin, 1):
            if not isinstance(t, dict):
                raise ValueError("termin ke-{} harus berupa objek".format(i))
            terakhir = i == len(daftar_termin)
            if t.get("persen") not in (None, ""):
                persen = parse_angka(t["persen"], "persen termin ke-{}".format(i))
                if persen <= 0:
                    raise ValueError("persen termin ke-{} harus lebih dari 0".format(i))
                jml = sisa_alok if terakhir else rupiah_bulat(total * persen / 100)
            elif t.get("jumlah") not in (None, ""):
                persen = None
                jml = rupiah_bulat(parse_angka(t["jumlah"], "jumlah termin ke-{}".format(i)))
            else:
                raise ValueError("termin ke-{}: isi 'persen' atau 'jumlah'".format(i))
            sisa_alok -= jml
            termin.append({"nama": str(t.get("nama") or "Termin {}".format(i)), "persen": persen, "jumlah": jml,
                           "jatuh_tempo": parse_tanggal(t["jatuh_tempo"], "jatuh tempo termin ke-{}".format(i))
                           if t.get("jatuh_tempo") else None})
        total_persen = sum((t["persen"] for t in termin if t["persen"] is not None), Decimal(0))
        if all(t["persen"] is not None for t in termin) and total_persen != 100:
            raise ValueError("total persen termin harus 100% (sekarang {}%)".format(format_angka(total_persen)))
        if sum((t["jumlah"] for t in termin), Decimal(0)) != total or any(t["jumlah"] < 0 for t in termin):
            raise ValueError("jumlah semua termin ({}) harus sama dengan total ({})".format(
                format_rp(sum((t["jumlah"] for t in termin), Decimal(0))), format_rp(total)))

    # tanggal
    tgl = parse_tanggal(d["tanggal"], "tanggal") if d.get("tanggal") else datetime.date.today()
    jatuh_tempo = None
    if jenis_dok == "invoice" and sisa > 0:
        if d.get("jatuh_tempo"):
            jatuh_tempo = parse_tanggal(d["jatuh_tempo"], "jatuh_tempo")
        else:
            hari = parse_angka(d.get("jatuh_tempo_hari", 14), "jatuh_tempo_hari")
            if hari < 0 or hari != hari.to_integral_value():
                raise ValueError("jatuh_tempo_hari harus bilangan bulat >= 0")
            jatuh_tempo = tgl + datetime.timedelta(days=int(hari))
        if jatuh_tempo < tgl:
            raise ValueError("jatuh tempo ({}) lebih awal dari tanggal dokumen ({})".format(jatuh_tempo, tgl))

    if total <= 0:
        status = "NIHIL"
    elif sisa <= 0:
        status = "LUNAS"
    elif dibayar > 0:
        status = "SEBAGIAN DIBAYAR"
    else:
        status = "BELUM DIBAYAR"

    # bea meterai
    peringatan = []
    if dibayar > BATAS_METERAI:
        meterai = {"wajib": True, "nilai_penerimaan": dibayar,
                   "pesan": "Dokumen ini menyatakan penerimaan uang {} (> Rp5.000.000). Bea meterai Rp10.000 "
                            "terutang (UU 10/2020): tempel meterai atau bubuhkan e-meterai sebelum ditandatangani."
                   .format(format_rp(dibayar))}
    else:
        pesan = "Tidak perlu meterai: dokumen tidak menyatakan penerimaan uang di atas Rp5.000.000."
        if total > BATAS_METERAI and dibayar < total:
            pesan += (" Catatan: kuitansi/bukti lunas untuk pembayaran lebih dari Rp5.000.000 nanti wajib "
                      "bermeterai Rp10.000.")
        meterai = {"wajib": False, "nilai_penerimaan": dibayar, "pesan": pesan}
    if sisa < 0:
        peringatan.append("Pembayaran ({}) melebihi total ({}). Kelebihan {} perlu dikembalikan atau dicatat "
                          "sebagai deposit.".format(format_rp(dibayar), format_rp(total), format_rp(-sisa)))
    if pkp and not ppn_aktif:
        peringatan.append("Penjual PKP tetapi PPN dimatikan. Pastikan transaksi ini memang tidak terutang PPN.")
    if ppn_aktif and not penjual.get("npwp"):
        peringatan.append("Penjual PKP sebaiknya mencantumkan NPWP. Faktur pajak tetap dibuat terpisah di Coretax.")

    return {
        "jenis_dokumen": jenis_dok, "tanggal": tgl, "jatuh_tempo": jatuh_tempo,
        "penjual": penjual, "pembeli": pembeli, "baris": baris, "subtotal": subtotal,
        "diskon": diskon, "diskon_persen": diskon_persen, "setelah_diskon": setelah_diskon, "ongkir": ongkir,
        "ppn": ppn, "total": total, "pembayaran": bayar, "dibayar": dibayar, "sisa": max(sisa, Decimal(0)),
        "termin": termin, "status": status, "meterai": meterai, "peringatan": peringatan,
        "terbilang_total": terbilang(total),
        "terbilang_diterima": terbilang(dibayar) if dibayar else None,
        "rekening": d.get("rekening") or [], "catatan": str(d.get("catatan") or ""),
        "tanda_tangan": d.get("tanda_tangan") or {},
    }


# ---------------------------------------------------------------- output Markdown
def md(x):
    """Escape ringan karakter Markdown dari teks pengguna agar tabel/format tidak rusak."""
    t = str(x if x is not None else "").replace("\r", " ").replace("\n", " ")
    t = re.sub(r"([\\`*_\[\]<>|])", r"\\\1", t)
    return re.sub(r"^([#>+-])", r"\\\1", t.strip())


def blok_pihak(p):
    baris = ["**{}**".format(md(p.get("nama")))]
    for k in ("alamat", "telepon", "email"):
        if p.get(k):
            baris.append(md(p[k]))
    if p.get("npwp"):
        baris.append("NPWP: {}".format(md(p["npwp"])))
    return baris


def label_diskon(nilai, persen):
    return "{}{}".format(format_rp(nilai), " ({}%)".format(format_angka(persen)) if persen is not None else "")


def label_bayar(h, p):
    awal = "Diterima" if h["jenis_dokumen"] == "kuitansi" else "Sudah dibayar"
    return "{}{}{}".format(awal, " - " + p["keterangan"] if p["keterangan"] else "",
                           " ({})".format(tanggal_id(p["tanggal"])) if p["tanggal"] else "")


def label_sisa(h):
    return "SISA TAGIHAN" if h["jenis_dokumen"] == "invoice" else "Sisa belum dibayar"


def tampil_sisa(h):
    """Baris dibayar/sisa ditampilkan bila ada pembayaran (invoice) atau kuitansi tidak lunas penuh."""
    if h["jenis_dokumen"] == "invoice":
        return bool(h["pembayaran"])
    return h["dibayar"] != h["total"]


def teks_terbilang(h):
    """Satu terbilang saja: kuitansi = uang yang diterima; invoice = sisa tagihan (bila ada DP) atau total."""
    if h["jenis_dokumen"] == "kuitansi":
        return h["terbilang_diterima"] or terbilang(0)
    return terbilang(h["sisa"]) if h["pembayaran"] else h["terbilang_total"]


def markdown(h, nomor):
    judul = "KUITANSI" if h["jenis_dokumen"] == "kuitansi" else "INVOICE"
    out = ["# {}".format(judul), ""]
    info = "**No.:** {}  \n**Tanggal:** {}".format(md(nomor), tanggal_id(h["tanggal"]))
    if h["jatuh_tempo"]:
        info += "  \n**Jatuh tempo:** {}".format(tanggal_id(h["jatuh_tempo"]))
    info += "  \n**Status:** {}".format(h["status"])
    out += [info, ""]
    if h["jenis_dokumen"] == "kuitansi":
        out.append("Telah terima dari: **{}**  ".format(md(h["pembeli"]["nama"])))
        out.append("Uang sejumlah: **{}**  ".format(format_rp(h["dibayar"])))
        out.append("Terbilang: _{}_  ".format(teks_terbilang(h)))
        out.append("Untuk pembayaran: {}{}".format(", ".join(md(b["nama"]) for b in h["baris"]),
                                                  "  " if h["sisa"] > 0 else ""))
        if h["sisa"] > 0:
            out.append("Sisa yang belum dibayar: **{}** dari total {}".format(
                format_rp(h["sisa"]), format_rp(h["total"])))
        out.append("")
    out.append("**Dari:**  ")
    out.append("  \n".join(blok_pihak(h["penjual"])))
    out.append("")
    out.append("**Kepada:**  ")
    out.append("  \n".join(blok_pihak(h["pembeli"])))
    out += ["", "| No | Deskripsi | Qty | Harga | Diskon | Jumlah |", "|---:|---|---:|---:|---:|---:|"]
    for b in h["baris"]:
        out.append("| {} | {} | {}{} | {} | {} | {} |".format(
            b["no"], md(b["nama"]), format_angka(b["qty"]), " " + md(b["satuan"]) if b["satuan"] else "",
            format_rp(b["harga"], True), label_diskon(b["diskon"], b["diskon_persen"]) if b["diskon"] else "-",
            format_rp(b["jumlah"])))
    out.append("")
    out.append("| | |")
    out.append("|---|---:|")
    out.append("| Subtotal | {} |".format(format_rp(h["subtotal"])))
    if h["diskon"]:
        out.append("| Diskon | -{} |".format(label_diskon(h["diskon"], h["diskon_persen"])))
    if h["ongkir"]:
        out.append("| Ongkos kirim | {} |".format(format_rp(h["ongkir"])))
    if h["ppn"]:
        p = h["ppn"]
        out.append("| DPP | {} |".format(format_rp(p["dpp"])))
        if p["jenis"] == "umum":
            out.append("| DPP nilai lain (11/12) | {} |".format(format_rp(p["dpp_nilai_lain"], True)))
        out.append("| PPN 12% | {} |".format(format_rp(p["ppn"])))
    out.append("| **TOTAL** | **{}** |".format(format_rp(h["total"])))
    if tampil_sisa(h):
        for p in h["pembayaran"]:
            out.append("| {} | -{} |".format(md(label_bayar(h, p)), format_rp(p["jumlah"])))
        out.append("| **{}** | **{}** |".format(label_sisa(h), format_rp(h["sisa"])))
    if h["jenis_dokumen"] == "invoice":
        out.append("")
        out.append("Terbilang: _{}_".format(teks_terbilang(h)))
    if h["termin"]:
        out += ["", "**Jadwal pembayaran**", "", "| Termin | Persen | Jumlah | Jatuh tempo |", "|---|---:|---:|---|"]
        for t in h["termin"]:
            out.append("| {} | {} | {} | {} |".format(
                md(t["nama"]), "{}%".format(format_angka(t["persen"])) if t["persen"] is not None else "-",
                format_rp(t["jumlah"]), tanggal_id(t["jatuh_tempo"]) if t["jatuh_tempo"] else "-"))
    if h["rekening"] and h["sisa"] > 0:
        out += ["", "**Pembayaran ke:**"]
        for r in h["rekening"]:
            out.append("- {} {} a.n. {}".format(md(r.get("bank", "")), md(r.get("nomor", "")),
                                                md(r.get("atas_nama", ""))))
    if h["catatan"]:
        out += ["", "**Catatan:** " + md(h["catatan"])]
    tt = h["tanda_tangan"]
    out += ["", "{}{}".format(md(tt.get("kota")) + ", " if tt.get("kota") else "", tanggal_id(h["tanggal"]))]
    if h["meterai"]["wajib"]:
        out.append("[ Meterai Rp10.000 ]")
    out += ["", "", "**{}**".format(md(tt.get("nama") or h["penjual"]["nama"]))]
    if tt.get("jabatan"):
        out.append(md(tt["jabatan"]))
    return "\n".join(out)


# ---------------------------------------------------------------- output HTML
CSS = """
*{box-sizing:border-box}body{font-family:Arial,Helvetica,sans-serif;color:#222;margin:0;background:#f4f4f4}
.hal{max-width:800px;margin:24px auto;background:#fff;padding:40px;border:1px solid #ddd}
h1{margin:0;font-size:28px;letter-spacing:2px;color:#1f3a5f}.kepala{display:flex;justify-content:space-between;gap:16px;flex-wrap:wrap}
.info td{padding:2px 8px 2px 0;font-size:14px}.pihak{display:flex;gap:24px;margin:24px 0;flex-wrap:wrap}
.pihak div{flex:1;min-width:220px;font-size:14px;line-height:1.5}.label{font-size:12px;color:#666;text-transform:uppercase}
table.item{width:100%;border-collapse:collapse;font-size:14px}table.item th{background:#1f3a5f;color:#fff;padding:8px;text-align:left}
table.item td{padding:8px;border-bottom:1px solid #e5e5e5}.kanan{text-align:right}
table.ringkas{margin-left:auto;margin-top:12px;font-size:14px;min-width:300px}table.ringkas td{padding:4px 8px}
.total td{font-weight:bold;font-size:16px;border-top:2px solid #1f3a5f}.status{display:inline-block;padding:4px 10px;
border:2px solid #1f3a5f;font-weight:bold;font-size:13px}.terbilang{font-style:italic;margin:12px 0;font-size:14px}
.ttd{margin-top:40px;text-align:right;font-size:14px}.meterai{display:inline-block;border:1px dashed #999;padding:18px 10px;
margin:8px 0;font-size:11px;color:#888}.kecil{font-size:13px;line-height:1.5}
@media print{body{background:#fff}.hal{border:none;margin:0;padding:0;max-width:none}@page{size:A4;margin:18mm}}
"""


def e(x):
    return html.escape(str(x if x is not None else ""))


def html_dok(h, nomor):
    judul = "KUITANSI" if h["jenis_dokumen"] == "kuitansi" else "INVOICE"
    pj, pb = h["penjual"], h["pembeli"]

    def pihak(p):
        s = "<strong>{}</strong>".format(e(p.get("nama")))
        for k in ("alamat", "telepon", "email"):
            if p.get(k):
                s += "<br>" + e(p[k])
        if p.get("npwp"):
            s += "<br>NPWP: " + e(p["npwp"])
        return s

    info = "<tr><td>No.</td><td><strong>{}</strong></td></tr><tr><td>Tanggal</td><td>{}</td></tr>".format(
        e(nomor), e(tanggal_id(h["tanggal"])))
    if h["jatuh_tempo"]:
        info += "<tr><td>Jatuh tempo</td><td>{}</td></tr>".format(e(tanggal_id(h["jatuh_tempo"])))
    rows = ""
    for b in h["baris"]:
        rows += ("<tr><td>{}</td><td>{}</td><td class='kanan'>{}</td><td class='kanan'>{}</td>"
                 "<td class='kanan'>{}</td><td class='kanan'>{}</td></tr>").format(
            b["no"], e(b["nama"]), e(format_angka(b["qty"]) + (" " + b["satuan"] if b["satuan"] else "")),
            e(format_rp(b["harga"], True)), e(label_diskon(b["diskon"], b["diskon_persen"]) if b["diskon"] else "-"),
            e(format_rp(b["jumlah"])))
    rk = "<tr><td>Subtotal</td><td class='kanan'>{}</td></tr>".format(e(format_rp(h["subtotal"])))
    if h["diskon"]:
        rk += "<tr><td>Diskon</td><td class='kanan'>-{}</td></tr>".format(e(label_diskon(h["diskon"], h["diskon_persen"])))
    if h["ongkir"]:
        rk += "<tr><td>Ongkos kirim</td><td class='kanan'>{}</td></tr>".format(e(format_rp(h["ongkir"])))
    if h["ppn"]:
        p = h["ppn"]
        rk += "<tr><td>DPP</td><td class='kanan'>{}</td></tr>".format(e(format_rp(p["dpp"])))
        if p["jenis"] == "umum":
            rk += "<tr><td>DPP nilai lain (11/12)</td><td class='kanan'>{}</td></tr>".format(
                e(format_rp(p["dpp_nilai_lain"], True)))
        rk += "<tr><td>PPN 12%</td><td class='kanan'>{}</td></tr>".format(e(format_rp(p["ppn"])))
    rk += "<tr class='total'><td>TOTAL</td><td class='kanan'>{}</td></tr>".format(e(format_rp(h["total"])))
    if tampil_sisa(h):
        for p in h["pembayaran"]:
            rk += "<tr><td>{}</td><td class='kanan'>-{}</td></tr>".format(e(label_bayar(h, p)), e(format_rp(p["jumlah"])))
        rk += "<tr class='total'><td>{}</td><td class='kanan'>{}</td></tr>".format(e(label_sisa(h)), e(format_rp(h["sisa"])))
    kuit = ""
    if h["jenis_dokumen"] == "kuitansi":
        sisa = ("<br>Sisa yang belum dibayar: <strong>{}</strong> dari total {}".format(
            e(format_rp(h["sisa"])), e(format_rp(h["total"]))) if h["sisa"] > 0 else "")
        kuit = ("<p class='kecil'>Telah terima dari: <strong>{}</strong><br>Uang sejumlah: <strong>{}</strong><br>"
                "Terbilang: <em>{}</em><br>Untuk pembayaran: {}{}</p>").format(
            e(pb.get("nama")), e(format_rp(h["dibayar"])), e(teks_terbilang(h)),
            e(", ".join(b["nama"] for b in h["baris"])), sisa)
    tb = "<p class='terbilang'>Terbilang: {}</p>".format(e(teks_terbilang(h))) if h["jenis_dokumen"] == "invoice" else ""
    termin = ""
    if h["termin"]:
        termin = "<p class='label'>Jadwal pembayaran</p><table class='item'><tr><th>Termin</th><th class='kanan'>Persen</th>" \
                 "<th class='kanan'>Jumlah</th><th>Jatuh tempo</th></tr>"
        for t in h["termin"]:
            termin += "<tr><td>{}</td><td class='kanan'>{}</td><td class='kanan'>{}</td><td>{}</td></tr>".format(
                e(t["nama"]), e("{}%".format(format_angka(t["persen"])) if t["persen"] is not None else "-"),
                e(format_rp(t["jumlah"])), e(tanggal_id(t["jatuh_tempo"]) if t["jatuh_tempo"] else "-"))
        termin += "</table>"
    rek = ""
    if h["rekening"] and h["sisa"] > 0:
        rek = "<p class='label'>Pembayaran ke</p><p class='kecil'>" + "<br>".join(
            "{} {} a.n. {}".format(e(r.get("bank", "")), e(r.get("nomor", "")), e(r.get("atas_nama", "")))
            for r in h["rekening"]) + "</p>"
    cat = "<p class='kecil'><strong>Catatan:</strong> {}</p>".format(e(h["catatan"])) if h["catatan"] else ""
    tt = h["tanda_tangan"]
    meterai = "<div class='meterai'>Meterai<br>Rp10.000</div><br>" if h["meterai"]["wajib"] else "<br><br><br>"
    ttd = "<div class='ttd'>{}{}<br>{}<strong>{}</strong>{}</div>".format(
        e(tt.get("kota") + ", ") if tt.get("kota") else "", e(tanggal_id(h["tanggal"])), meterai,
        e(tt.get("nama") or pj.get("nama")), "<br>" + e(tt["jabatan"]) if tt.get("jabatan") else "")
    return """<!DOCTYPE html>
<html lang="id"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{judul} {nomor}</title><style>{css}</style></head><body><div class="hal">
<div class="kepala"><div><h1>{judul}</h1><div class="kecil">{penjual}</div></div>
<div><table class="info">{info}</table><span class="status">{status}</span></div></div>
{kuit}<div class="pihak"><div><div class="label">Kepada</div>{pembeli}</div></div>
<table class="item"><tr><th>No</th><th>Deskripsi</th><th class="kanan">Qty</th><th class="kanan">Harga</th>
<th class="kanan">Diskon</th><th class="kanan">Jumlah</th></tr>{rows}</table>
<table class="ringkas">{rk}</table>{tb}
{termin}{rek}{cat}{ttd}</div></body></html>
""".format(judul=judul, nomor=e(nomor), css=CSS, penjual=pihak(pj), info=info, status=e(h["status"]), kuit=kuit,
           pembeli=pihak(pb), rows=rows, rk=rk, tb=tb, termin=termin, rek=rek, cat=cat, ttd=ttd)


# ---------------------------------------------------------------- CLI
class ParserID(argparse.ArgumentParser):
    def error(self, message):
        sys.stderr.write("ERROR: argumen tidak valid ({}).\nLihat bantuan: python3 buat_invoice.py --help\n"
                         .format(message))
        sys.exit(2)


def main(argv=None):
    p = ParserID(description="Buat invoice/kuitansi (Markdown + HTML siap cetak) dari file JSON.")
    p.add_argument("--file", required=True, help="File JSON data invoice (lihat templates/contoh-invoice.json)")
    p.add_argument("--html", help="Simpan juga versi HTML siap cetak ke path ini")
    p.add_argument("--nomor-terakhir", help="Nomor invoice terakhir, mis. INV/2026/09/0007 -> dibuat 0008")
    p.add_argument("--counter-file", help="File JSON penyimpan nomor urut (dibuat/diperbarui otomatis)")
    p.add_argument("--format", choices=["markdown", "json"], default="markdown")
    a = p.parse_args(argv)

    try:
        try:
            with open(a.file, encoding="utf-8-sig") as f:
                d = json.load(f)
        except OSError as ex:
            raise ValueError("file '{}' tidak bisa dibaca: {}".format(a.file, ex.strerror or ex))
        except json.JSONDecodeError as ex:
            raise ValueError("JSON tidak valid (baris {}, kolom {}): {}".format(ex.lineno, ex.colno, ex.msg))
        if not isinstance(d, dict):
            raise ValueError("isi JSON harus berupa objek {...}. Lihat templates/contoh-invoice.json")
        h = hitung(d)
        prefix = str(d.get("prefix") or ("KWT" if h["jenis_dokumen"] == "kuitansi" else "INV")).strip("/")
        data_counter = None
        catatan_nomor = None
        if d.get("nomor"):
            nomor = str(d["nomor"])
        elif a.nomor_terakhir:
            nomor = nomor_berikutnya(a.nomor_terakhir)
        elif a.counter_file:
            nomor, data_counter = nomor_dari_counter(a.counter_file, prefix, h["tanggal"])
        else:
            nomor = "{}/{}/{:02d}/0001".format(prefix, h["tanggal"].year, h["tanggal"].month)
            catatan_nomor = ("Nomor urut memakai 0001. Sebutkan nomor dokumen terakhir Anda agar nomor berurutan "
                             "(--nomor-terakhir) atau pakai --counter-file.")
    except ValueError as ex:
        sys.stderr.write("ERROR: {}\n".format(ex))
        return 2

    if catatan_nomor:
        h["peringatan"].append(catatan_nomor)
    try:
        if a.html:
            with open(a.html, "w", encoding="utf-8") as f:
                f.write(html_dok(h, nomor))
        if data_counter is not None:
            with open(a.counter_file, "w", encoding="utf-8") as f:
                json.dump(data_counter, f, ensure_ascii=False, indent=2)
    except OSError as ex:
        sys.stderr.write("ERROR: gagal menulis file: {}\n".format(ex.strerror or ex))
        return 2

    if a.format == "json":
        h2 = dict(h)
        h2["nomor"] = nomor
        h2["html_disimpan_ke"] = a.html
        print(json.dumps(h2, default=lambda x: x.isoformat() if isinstance(x, datetime.date) else ke_json(x),
                         ensure_ascii=False, indent=2))
    else:
        print(markdown(h, nomor))
        print("")
        print("---")
        print("Info untuk penjual (jangan ikut dikirim):")
        print("- Bea meterai: " + h["meterai"]["pesan"])
        if h["ppn"]:
            print("- PPN dihitung dengan DPP nilai lain 11/12 (PMK 131/2024, berlaku per {}): dari DPP persis lalu "
                  "dibulatkan ke bawah sekali. Pembulatan ini belum dicocokkan dengan Coretax; bila berbeda, ikuti "
                  "Coretax. Invoice ini bukan faktur pajak; buat faktur pajak di Coretax.".format(TANGGAL_ATURAN))
        print("- Pembulatan: jumlah baris & diskon dibulatkan ke rupiah terdekat.")
        for w in h["peringatan"]:
            print("- PERHATIAN: " + w)
        if a.html:
            print("- Versi HTML siap cetak disimpan di: {}".format(a.html))
    return 0


if __name__ == "__main__":
    sys.exit(main())
