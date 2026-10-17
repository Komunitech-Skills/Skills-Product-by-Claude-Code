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
  python3 buat_invoice.py --file invoice.json --html invoice-{nomor}.html     (nama berkas dari nomor invoice)
  python3 buat_invoice.py --file invoice.json --html .                        (folder: invoice-<nomor>.html)
  python3 buat_invoice.py --file invoice.json --nomor-terakhir INV/2026/09/0007
  python3 buat_invoice.py --file invoice.json --nomor-terakhir INV/2026/09/0007 --counter-file nomor-invoice.json
  (--counter-file mencatat setiap nomor yang dibuat + nama pembeli agar invoice berikutnya tidak bernomor dobel)
  (dengan --html, baris 'BERKAS: <path absolut>' = path yang dilampirkan ke chat; v1.0.7)
  python3 buat_invoice.py --file invoice.json --html invoice-{nomor}.html --txt invoice-{nomor}.txt
  (v1.0.8: --txt menulis versi teks biasa .txt -> baris 'BERKAS TEKS: <path absolut>', cadangan bila kanal chat
   menolak berkas HTML)
"""
import argparse
import datetime
import html
import json
import os
import re
import sys
from decimal import Decimal, ROUND_FLOOR, ROUND_HALF_UP

sys.dont_write_bytecode = True  # jangan membuat __pycache__ di folder skill
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hitung_ppn import hitung_ppn_dari_dpp, parse_angka, format_rp, format_angka, ke_json  # noqa: E402

BATAS_METERAI = Decimal(5000000)
TARIF_METERAI = Decimal(10000)
TANGGAL_ATURAN = "2026-09-23"
VERSI = "1.0.8"
TARIF_PPH23_JASA = Decimal(2)   # UU PPh Pasal 23 ayat (1) huruf c; tanpa NPWP 100% lebih tinggi (ayat 1a)
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


ROMAWI = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI", "XII"]


def _bulan_token(tok):
    """Token bulan: '09'/'9' (1-12, maks. 2 digit) atau angka Romawi I-XII. Kembalikan (bulan, gaya) atau None."""
    if tok.isdigit() and len(tok) <= 2 and 1 <= int(tok) <= 12:
        return int(tok), "angka{}".format(len(tok))
    if tok.upper() in ROMAWI:
        return ROMAWI.index(tok.upper()) + 1, "romawi" if tok.isupper() else "romawi-kecil"
    return None


def _tulis_bulan(bulan, gaya):
    if gaya.startswith("romawi"):
        r = ROMAWI[bulan - 1]
        return r if gaya == "romawi" else r.lower()
    return str(bulan).zfill(2 if gaya == "angka2" else 1)


def nomor_berikutnya(terakhir, tgl=None, urut_lanjut=False):
    """Nomor baru = nomor terakhir + 1, dengan aturan ganti periode.

    Mengenali tahun (4 digit 19xx/20xx), bulan di sebelah tahun (01-12 atau Romawi I-XII), dan angka urut
    (angka lain; bila lebih dari satu, yang paling kanan). Contoh: INV/2026/09/0012, 012/INV/IX/2026, INV-2026-0012.
    - Periode tanggal dokumen SAMA dengan periode nomor terakhir -> urut + 1 (0012 -> 0013).
    - Periode dokumen LEBIH BARU (ganti bulan/tahun) -> tahun/bulan diganti ke periode dokumen dan urut mulai
      0001 (atau urut + 1 bila urut_lanjut=True, untuk usaha yang nomornya tidak di-reset).
    - Periode dokumen LEBIH LAMA -> error (nomor mundur; isi nomor manual bila memang disengaja).
    Kembalikan (nomor_baru, keterangan).
    """
    s = str(terakhir or "").strip()
    if not s:
        raise ValueError("nomor terakhir kosong")
    tok = re.split(r"([/\-.\s_]+)", s)
    idx = [i for i in range(0, len(tok), 2) if tok[i]]
    i_tahun = next((i for i in reversed(idx) if re.fullmatch(r"(19|20)\d\d", tok[i])), None)
    i_bulan = None
    if i_tahun is not None:
        for j in (i_tahun + 2, i_tahun - 2):
            if 0 <= j < len(tok) and j != i_tahun and tok[j] and _bulan_token(tok[j]):
                # angka urut tetap harus ada di luar tahun/bulan
                if any(re.search(r"\d", tok[k]) for k in idx if k not in (i_tahun, j)):
                    i_bulan = j
                    break
    kandidat = [i for i in idx if i not in (i_tahun, i_bulan) and re.search(r"\d", tok[i])]
    if not kandidat:
        raise ValueError("nomor terakhir '{}' tidak mengandung angka urut (contoh benar: INV/2026/09/0012)"
                         .format(s))
    i_urut = kandidat[-1]
    m = re.search(r"(\d+)(?!.*\d)", tok[i_urut])
    angka = m.group(1)

    def pasang(n):
        t = list(tok)
        t[i_urut] = t[i_urut][:m.start(1)] + str(n).zfill(len(angka)) + t[i_urut][m.end(1):]
        return t

    urut_lama = int(angka)
    if tgl is None or i_tahun is None:
        baru = "".join(pasang(urut_lama + 1))
        return baru, "Nomor terakhir dibaca: {} -> nomor baru: {} (urut {} + 1).".format(s, baru, urut_lama)

    th_lama = int(tok[i_tahun])
    bl_lama, gaya = _bulan_token(tok[i_bulan]) if i_bulan is not None else (None, None)
    per_lama = (th_lama, bl_lama or 0)
    per_dok = (tgl.year, tgl.month if bl_lama else 0)
    label_lama = "{:02d}/{}".format(bl_lama, th_lama) if bl_lama else str(th_lama)
    label_dok = "{:02d}/{}".format(tgl.month, tgl.year) if bl_lama else str(tgl.year)
    if per_dok < per_lama:
        raise ValueError("tanggal dokumen ({}) lebih lama dari periode nomor terakhir {} ({}). Nomor tidak boleh "
                         "mundur; periksa tanggal atau isi 'nomor' manual bila memang disengaja."
                         .format(tanggal_id(tgl), s, label_lama))
    if per_dok == per_lama:
        baru = "".join(pasang(urut_lama + 1))
        return baru, "Nomor terakhir dibaca: {} -> nomor baru: {} (urut {} + 1).".format(s, baru, urut_lama)
    t = pasang(urut_lama + 1 if urut_lanjut else 1)
    t[i_tahun] = str(tgl.year)
    if i_bulan is not None:
        t[i_bulan] = _tulis_bulan(tgl.month, gaya)
    baru = "".join(t)
    if urut_lanjut:
        ket = ("Nomor terakhir dibaca: {} -> nomor baru: {}. Periode berganti ({} -> {}); urut dilanjutkan "
               "(--urut-lanjut).".format(s, baru, label_lama, label_dok))
    else:
        ket = ("Nomor terakhir dibaca: {} -> nomor baru: {}. Periode berganti ({} -> {}), jadi nomor urut mulai "
               "lagi dari 1. Jika usaha Anda melanjutkan nomor lintas {}, jalankan ulang dengan --urut-lanjut."
               .format(s, baru, label_lama, label_dok, "bulan" if bl_lama else "tahun"))
    return baru, ket


def baca_counter(path):
    """Isi file counter: {"INV/2026/10": 13, "terbit": {"INV/2026/10/0013": "<nama pembeli>", ...}}."""
    data = {}
    if os.path.exists(path):
        try:
            with open(path, encoding="utf-8") as f:
                data = json.load(f)
        except (OSError, json.JSONDecodeError):
            raise ValueError("file counter '{}' rusak atau tidak bisa dibaca".format(path))
        if not isinstance(data, dict) or not isinstance(data.get("terbit", {}), dict):
            raise ValueError("file counter '{}' harus berisi objek JSON".format(path))
    return data


def nomor_dari_counter(path, prefix, tgl, data=None):
    kunci = "{}/{}/{:02d}".format(prefix, tgl.year, tgl.month)
    if data is None:
        data = baca_counter(path)
    urut = int(data.get(kunci, 0)) + 1
    data[kunci] = urut
    return "{}/{:04d}".format(kunci, urut), data


def nama_berkas_dari_nomor(nomor):
    """v1.0.6: nomor invoice -> potongan nama berkas aman ('/' dan karakter lain -> '-').
    '001/INV/X/2026' -> '001-INV-X-2026'."""
    t = re.sub(r"[^A-Za-z0-9._]+", "-", str(nomor)).strip("-.")
    return t or "tanpa-nomor"


def kalimat_meterai_sisa(total, dibayar, sisa, termin):
    """v1.0.7: kalimat meterai untuk uang yang MASIH akan diterima, dihitung dari angka (bukan dikira).
    Pembanding: meterai Rp10.000 wajib bila nilai dokumen > Rp5.000.000 (di atas); tepat Rp5.000.000 tidak wajib.
    Contoh: sisa Rp5.075.000 -> 'di atas Rp5.000.000' -> wajib. Agent menyalin kalimat ini apa adanya."""
    if sisa <= 0 or total <= BATAS_METERAI:
        return ""

    def banding(nilai):
        return "di atas Rp5.000.000" if nilai > BATAS_METERAI else "tidak lebih dari Rp5.000.000"

    def akibat(nilai):
        return "wajib bermeterai Rp10.000" if nilai > BATAS_METERAI else "tidak wajib meterai"

    if termin:
        bagian = ["{} {} ({}: {})".format(t["nama"], format_rp(t["jumlah"]), banding(t["jumlah"]),
                                          akibat(t["jumlah"])) for t in termin]
        return "Kuitansi tiap termin dinilai sendiri-sendiri: " + "; ".join(bagian) + "."
    return "Sisa tagihan {} {}, jadi kuitansi pelunasan sekali bayar untuk sisa ini {}.".format(
        format_rp(sisa), banding(sisa), akibat(sisa))


def path_html(arg, jenis_dokumen, nomor, ekstensi=".html"):
    """v1.0.6: nama berkas HTML SELALU diturunkan dari nomor dokumen yang dicetak di chat.
    - arg memuat '{nomor}'  -> diganti nomor aman ('invoice-{nomor}.html' -> 'invoice-001-INV-X-2026.html')
    - arg folder (sudah ada, atau berakhir '/' atau '\\') -> '<jenis>-<nomor aman>.html' di folder itu
    - selain itu dipakai apa adanya (kompatibel dengan versi lama).
    v1.0.8: ekstensi='.txt' untuk --txt (aturan nama sama)."""
    aman = nama_berkas_dari_nomor(nomor)
    if "{nomor}" in arg:
        return arg.replace("{nomor}", aman)
    if arg.endswith(("/", "\\")) or os.path.isdir(arg):
        return os.path.join(arg, "{}-{}{}".format(jenis_dokumen, aman, ekstensi))
    return arg


def path_txt(arg, jenis_dokumen, nomor):
    """v1.0.8: path berkas teks (.txt). Aturan nama sama dengan path_html; akhiran SELALU '.txt' (ditambahkan bila
    belum ada) karena kanal chat (mis. OpenClaw) hanya menerima dokumen teks biasa berakhiran .txt."""
    path = path_html(arg, jenis_dokumen, nomor, ".txt")
    akar, ekstensi = os.path.splitext(path)
    if ekstensi.lower() in (".html", ".htm"):
        return akar + ".txt"   # 'invoice-{nomor}.html' diberikan ke --txt -> 'invoice-....txt', bukan '.html.txt'
    return path if ekstensi.lower() == ".txt" else path + ".txt"


def siapkan_folder(arg, path):
    """v1.0.8: argumen folder berakhiran '/' atau '\\' yang belum ada -> folder dibuat. Folder induk lain yang tidak
    ada -> ValueError SEBELUM ada berkas yang ditulis (tidak ada HTML yang tertulis setengah jalan)."""
    if arg.endswith(("/", "\\")):
        os.makedirs(arg, exist_ok=True)
    induk = os.path.dirname(os.path.abspath(path))
    if not os.path.isdir(induk):
        raise ValueError("folder '{}' tidak ada; buat foldernya dulu atau pakai folder kerja yang sudah ada".format(induk))


def cegah_dobel(data, nomor, pembeli, manual=False):
    """v1.0.5: catat setiap nomor yang dibuat di file counter (nomor -> nama pembeli) agar tidak dobel.

    - Nomor belum pernah dibuat -> dipakai.
    - Sudah dibuat untuk pembeli YANG SAMA -> dianggap revisi, nomor tetap.
    - Sudah dibuat untuk pembeli LAIN -> nomor otomatis dinaikkan ke nomor berikutnya yang belum dipakai
      pembeli lain; nomor manual (kolom 'nomor' di JSON) -> error.
    Kembalikan (nomor, catatan atau None).
    """
    terbit = data.setdefault("terbit", {})
    awal, catatan = nomor, None
    if terbit.get(nomor) not in (None, pembeli):
        if manual:
            raise ValueError("nomor {} sudah pernah dibuat untuk {} (tercatat di file counter). Nomor invoice tidak "
                             "boleh dobel; pakai nomor lain atau hapus 'nomor' agar dibuat otomatis."
                             .format(nomor, terbit[nomor]))
        while terbit.get(nomor) not in (None, pembeli):
            nomor = nomor_berikutnya(nomor)[0]
        catatan = ("nomor {} sudah dipakai untuk {} (tercatat di file counter), jadi dipakai nomor {}. Sampaikan ke "
                   "pengguna.".format(awal, terbit[awal], nomor))
    if terbit.get(nomor) == pembeli:
        akhir = nomor   # nomor terakhir yang sudah terpakai berurutan setelah nomor ini
        try:
            while nomor_berikutnya(akhir)[0] in terbit:
                akhir = nomor_berikutnya(akhir)[0]
        except ValueError:
            pass
        catatan = ((catatan + " ") if catatan else "") + (
            "Nomor {} sudah pernah dibuat untuk pembeli yang sama: dianggap revisi (nomor tidak berubah). Bila ini "
            "invoice BARU, jalankan ulang dengan --nomor-terakhir {}.".format(nomor, akhir))
    terbit[nomor] = pembeli
    m = re.fullmatch(r"(.+/\d{4}/\d{2})/(\d+)", nomor)
    if m:  # counter per bulan ikut maju (mis. setelah --nomor-terakhir), agar mode counter tidak mengulang nomor
        data[m.group(1)] = max(int(data.get(m.group(1), 0)), int(m.group(2)))
    return nomor, catatan


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

    # PPh 23 (info saja: dipotong & disetor pembeli/pemberi kerja; TIDAK mengubah total tagihan)
    pph23 = None
    cfg23 = d.get("pph23") or False
    if cfg23:
        if not isinstance(cfg23, dict):
            cfg23 = {"aktif": bool(cfg23)}
        if cfg23.get("aktif", True):
            if jenis_dok != "invoice":
                raise ValueError("pph23 hanya untuk invoice (bukan kuitansi)")
            tanpa_npwp = bool(cfg23.get("tanpa_npwp", False))
            tarif = parse_angka(cfg23["tarif"], "pph23.tarif") if cfg23.get("tarif") not in (None, "") \
                else TARIF_PPH23_JASA * (2 if tanpa_npwp else 1)
            if not 0 < tarif <= 15:
                raise ValueError("pph23.tarif harus di atas 0 s.d. 15 (persen)")
            if cfg23.get("dasar") not in (None, ""):
                dasar = rupiah_bulat(parse_angka(cfg23["dasar"], "pph23.dasar"))
                sumber_dasar = "diisi pengguna"
                if dasar <= 0 or dasar > setelah_diskon + ongkir:
                    raise ValueError("pph23.dasar harus lebih dari 0 dan tidak melebihi nilai sebelum PPN ({})"
                                     .format(format_rp(setelah_diskon + ongkir)))
            else:
                dasar = setelah_diskon
                sumber_dasar = "subtotal setelah diskon, tanpa PPN" + (" dan tanpa ongkir" if ongkir else "")
            potong = (dasar * tarif / 100).quantize(Decimal(1), ROUND_FLOOR)
            pph23 = {"tarif": tarif, "dasar": dasar, "sumber_dasar": sumber_dasar, "pph23": potong,
                     "tanpa_npwp": tanpa_npwp, "estimasi_diterima_bersih": total - potong}

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

    # bea meterai (wajib bila penerimaan uang di dokumen > Rp5.000.000; tepat Rp5.000.000 tidak wajib)
    peringatan = []
    kalimat_sisa = kalimat_meterai_sisa(total, dibayar, sisa, termin)
    if dibayar > BATAS_METERAI:
        pesan = ("Dokumen ini menyatakan penerimaan uang {} (di atas Rp5.000.000). Bea meterai Rp10.000 "
                 "terutang (UU 10/2020): tempel meterai atau bubuhkan e-meterai sebelum ditandatangani."
                 .format(format_rp(dibayar)))
        if kalimat_sisa:
            pesan += " " + kalimat_sisa
        meterai = {"wajib": True, "nilai_penerimaan": dibayar, "pesan": pesan}
    else:
        pesan = "Tidak perlu meterai: dokumen tidak menyatakan penerimaan uang di atas Rp5.000.000."
        if kalimat_sisa:
            pesan += " Catatan: " + kalimat_sisa
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
        "ppn": ppn, "pph23": pph23, "total": total, "pembayaran": bayar, "dibayar": dibayar, "sisa": max(sisa, Decimal(0)),
        "termin": termin, "status": status, "meterai": meterai, "peringatan": peringatan,
        "terbilang_total": terbilang(total),
        "terbilang_diterima": terbilang(dibayar) if dibayar else None,
        "rekening": d.get("rekening") or [], "catatan": str(d.get("catatan") or ""),
        "tanda_tangan": d.get("tanda_tangan") or {},
    }


# ---------------------------------------------------------------- data yang belum diberikan
ISI = "[isi]"
ISI_KOTA = "[isi kota]"
ISI_NAMA = "[isi nama penanda tangan]"


def kolom_kosong(h):
    """Data yang tidak diberikan pengguna -> placeholder [isi ...], tidak pernah dikarang."""
    tt = h["tanda_tangan"] if isinstance(h["tanda_tangan"], dict) else {}
    kosong = []
    if not str(tt.get("kota") or "").strip():
        kosong.append("kota")
    if not str(tt.get("nama") or "").strip():
        kosong.append("nama penanda tangan")
    return kosong


# ---------------------------------------------------------------- output Markdown
def teks_rekening(r, esc):
    """v1.0.6: 'a.n. ...' hanya bila nama pemilik rekening diberikan pengguna (tidak ditebak dari nama usaha)."""
    teks = "{} {}".format(esc(r.get("bank", "")), esc(r.get("nomor", ""))).strip()
    an = str(r.get("atas_nama") or "").strip()
    return "{} a.n. {}".format(teks, esc(an)) if an else teks


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


def teks_pph23(h, esc=None):
    q = h["pph23"]
    return ("_Info PPh 23 (dipotong & disetor oleh {}, tidak mengurangi total tagihan): {}% x {} = {}. "
            "Estimasi diterima bersih: {}. Mohon kirimkan bukti potong PPh 23._".format(
                (esc or md)(h["pembeli"]["nama"]), format_angka(q["tarif"]).replace(".", ","), format_rp(q["dasar"]),
                format_rp(q["pph23"]), format_rp(q["estimasi_diterima_bersih"])))


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
    if h.get("pph23"):
        out += ["", teks_pph23(h)]
    if h["termin"]:
        out += ["", "**Jadwal pembayaran**", "", "| Termin | Persen | Jumlah | Jatuh tempo |", "|---|---:|---:|---|"]
        for t in h["termin"]:
            out.append("| {} | {} | {} | {} |".format(
                md(t["nama"]), "{}%".format(format_angka(t["persen"])) if t["persen"] is not None else "-",
                format_rp(t["jumlah"]), tanggal_id(t["jatuh_tempo"]) if t["jatuh_tempo"] else "-"))
    if h["rekening"] and h["sisa"] > 0:
        out += ["", "**Pembayaran ke:**"]
        for r in h["rekening"]:
            out.append("- " + teks_rekening(r, md))
    if h["catatan"]:
        out += ["", "**Catatan:** " + md(h["catatan"])]
    tt = h["tanda_tangan"]
    out += ["", "{}, {}".format(md(tt.get("kota")) if tt.get("kota") else ISI_KOTA, tanggal_id(h["tanggal"]))]
    if h["meterai"]["wajib"]:
        out.append("[ Meterai Rp10.000 ]")
    out += ["", "", "**{}**".format(md(tt["nama"]) if tt.get("nama") else ISI_NAMA)]
    if tt.get("jabatan"):
        out.append(md(tt["jabatan"]))
    out.append(md(h["penjual"]["nama"]))
    return "\n".join(out)


# ---------------------------------------------------------------- output teks biasa (.txt)
def polos(x):
    """Teks pengguna untuk berkas .txt: satu baris, tanpa escape Markdown."""
    return re.sub(r"\s*[\r\n]+\s*", " ", str(x if x is not None else "")).strip()


def teks_polos(h, nomor):
    """v1.0.8: versi teks biasa (tanpa Markdown/tabel) dari bagian dokumen untuk pembeli, untuk berkas .txt
    cadangan yang bisa dilampirkan di kanal chat yang menolak HTML. Angka sama persis dengan markdown() (hanya
    menampilkan hasil hitung(), tidak ada hitungan baru); 'Info untuk penjual' tidak ikut."""
    kuitansi = h["jenis_dokumen"] == "kuitansi"
    out = ["KUITANSI" if kuitansi else "INVOICE", "",
           "No.: " + polos(nomor), "Tanggal: " + tanggal_id(h["tanggal"])]
    if h["jatuh_tempo"]:
        out.append("Jatuh tempo: " + tanggal_id(h["jatuh_tempo"]))
    out += ["Status: " + h["status"], ""]
    if kuitansi:
        out.append("Telah terima dari: " + polos(h["pembeli"]["nama"]))
        out.append("Uang sejumlah: " + format_rp(h["dibayar"]))
        out.append("Terbilang: " + teks_terbilang(h))
        out.append("Untuk pembayaran: " + ", ".join(polos(b["nama"]) for b in h["baris"]))
        if h["sisa"] > 0:
            out.append("Sisa yang belum dibayar: {} dari total {}".format(format_rp(h["sisa"]), format_rp(h["total"])))
        out.append("")
    for label, p in (("Dari", h["penjual"]), ("Kepada", h["pembeli"])):
        out.append("{}: {}".format(label, polos(p.get("nama"))))
        for k in ("alamat", "telepon", "email"):
            if p.get(k):
                out.append("   " + polos(p[k]))
        if p.get("npwp"):
            out.append("   NPWP: " + polos(p["npwp"]))
    out += ["", "Rincian:"]
    for b in h["baris"]:
        qty = format_angka(b["qty"]) + (" " + polos(b["satuan"]) if b["satuan"] else "")
        s = "{}. {}: {} x {}".format(b["no"], polos(b["nama"]), qty, format_rp(b["harga"], True))
        if b["diskon"]:
            s += " = {}, diskon {}, jumlah {}".format(format_rp(b["bruto"]),
                                                      label_diskon(b["diskon"], b["diskon_persen"]),
                                                      format_rp(b["jumlah"]))
        else:
            s += " = " + format_rp(b["jumlah"])
        out.append(s)
    out += ["", "Subtotal: " + format_rp(h["subtotal"])]
    if h["diskon"]:
        out.append("Diskon: -" + label_diskon(h["diskon"], h["diskon_persen"]))
    if h["ongkir"]:
        out.append("Ongkos kirim: " + format_rp(h["ongkir"]))
    if h["ppn"]:
        p = h["ppn"]
        out.append("DPP: " + format_rp(p["dpp"]))
        if p["jenis"] == "umum":
            out.append("DPP nilai lain (11/12): " + format_rp(p["dpp_nilai_lain"], True))
        out.append("PPN 12%: " + format_rp(p["ppn"]))
    out.append("TOTAL: " + format_rp(h["total"]))
    if tampil_sisa(h):
        for p in h["pembayaran"]:
            out.append("{}: -{}".format(polos(label_bayar(h, p)), format_rp(p["jumlah"])))
        out.append("{}: {}".format(label_sisa(h), format_rp(h["sisa"])))
    if not kuitansi:
        out += ["", "Terbilang: " + teks_terbilang(h)]
    if h.get("pph23"):
        out += ["", teks_pph23(h, polos).strip("_")]
    if h["termin"]:
        out += ["", "Jadwal pembayaran:"]
        for t in h["termin"]:
            out.append("- {}{}: {}{}".format(
                polos(t["nama"]), " ({}%)".format(format_angka(t["persen"])) if t["persen"] is not None else "",
                format_rp(t["jumlah"]), ", jatuh tempo " + tanggal_id(t["jatuh_tempo"]) if t["jatuh_tempo"] else ""))
    if h["rekening"] and h["sisa"] > 0:
        out += ["", "Pembayaran ke:"]
        for r in h["rekening"]:
            out.append("- " + teks_rekening(r, polos))
    if h["catatan"]:
        out += ["", "Catatan: " + polos(h["catatan"])]
    tt = h["tanda_tangan"]
    out += ["", "{}, {}".format(polos(tt.get("kota")) if tt.get("kota") else ISI_KOTA, tanggal_id(h["tanggal"]))]
    if h["meterai"]["wajib"]:
        out.append("[ Meterai Rp10.000 ]")
    out += ["", "", polos(tt["nama"]) if tt.get("nama") else ISI_NAMA]
    if tt.get("jabatan"):
        out.append(polos(tt["jabatan"]))
    out.append(polos(h["penjual"]["nama"]))
    return "\n".join(out) + "\n"


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
    if h.get("pph23"):
        # v1.0.8: nama pembeli tanpa escape Markdown (e() sudah meng-escape HTML); sebelumnya 'PT A_B' -> 'PT A\_B'
        tb += "<p class='kecil'><em>{}</em></p>".format(e(teks_pph23(h, polos).strip("_")))
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
            teks_rekening(r, e) for r in h["rekening"]) + "</p>"
    cat = "<p class='kecil'><strong>Catatan:</strong> {}</p>".format(e(h["catatan"])) if h["catatan"] else ""
    tt = h["tanda_tangan"]
    meterai = "<div class='meterai'>Meterai<br>Rp10.000</div><br>" if h["meterai"]["wajib"] else "<br><br><br>"
    ttd = "<div class='ttd'>{}, {}<br>{}<strong>{}</strong>{}<br>{}</div>".format(
        e(tt.get("kota") or ISI_KOTA), e(tanggal_id(h["tanggal"])), meterai,
        e(tt.get("nama") or ISI_NAMA), "<br>" + e(tt["jabatan"]) if tt.get("jabatan") else "", e(pj.get("nama")))
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
    p.add_argument("--html", help="Simpan juga versi HTML siap cetak ke path ini. Boleh memuat {nomor} "
                   "(diganti nomor invoice, '/' jadi '-'), mis. invoice-{nomor}.html; atau berupa folder "
                   "(nama berkas otomatis dari nomor)")
    p.add_argument("--txt", help="v1.0.8: simpan juga versi teks biasa (.txt, tanpa Markdown) ke path ini; aturan "
                   "{nomor}/folder sama dengan --html. Cadangan lampiran bila kanal chat menolak berkas HTML")
    p.add_argument("--nomor-terakhir", help="Nomor invoice terakhir, mis. INV/2026/09/0007 -> dibuat 0008")
    p.add_argument("--urut-lanjut", action="store_true",
                   help="Dengan --nomor-terakhir: saat bulan/tahun berganti, urut dilanjutkan (bukan mulai 0001)")
    p.add_argument("--counter-file", help="File JSON penyimpan nomor urut & nomor yang sudah dibuat (dibuat/diperbarui "
                   "otomatis); mencegah nomor dobel, bisa digabung dengan --nomor-terakhir")
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
        data_counter = baca_counter(a.counter_file) if a.counter_file else None
        catatan_nomor = None
        keterangan_nomor = None
        if d.get("nomor"):
            nomor = str(d["nomor"])
        elif a.nomor_terakhir:
            nomor, keterangan_nomor = nomor_berikutnya(a.nomor_terakhir, h["tanggal"], a.urut_lanjut)
        elif a.counter_file:
            nomor, data_counter = nomor_dari_counter(a.counter_file, prefix, h["tanggal"], data_counter)
            keterangan_nomor = "Nomor dari file counter: {}.".format(nomor)
        else:
            nomor = "{}/{}/{:02d}/0001".format(prefix, h["tanggal"].year, h["tanggal"].month)
            catatan_nomor = ("Nomor urut memakai 0001. Sebutkan nomor dokumen terakhir Anda agar nomor berurutan "
                             "(--nomor-terakhir) atau pakai --counter-file.")
        if data_counter is not None:
            calon = nomor
            nomor, dobel = cegah_dobel(data_counter, nomor, str(h["pembeli"]["nama"]), manual=bool(d.get("nomor")))
            if dobel:
                h["peringatan"].append(dobel[0].upper() + dobel[1:])
            keterangan_nomor = "{}{}{}Nomor tercatat di file pencatat nomor (pakai file yang sama untuk dokumen " \
                "berikutnya; di chat cukup sebut 'nomor terakhir sudah dicatat', lokasi berikut hanya untuk " \
                "terminal/IDE: {}).".format(keterangan_nomor or "", " " if keterangan_nomor else "",
                                      "Nomor yang dipakai: {} ({} sudah terpakai). ".format(nomor, calon)
                                      if nomor != calon else "", os.path.abspath(a.counter_file))
    except ValueError as ex:
        sys.stderr.write("ERROR: {}\n".format(ex))
        return 2

    if catatan_nomor:
        h["peringatan"].append(catatan_nomor)
    if a.nomor_terakhir and nomor.strip() == a.nomor_terakhir.strip():
        h["peringatan"].append("Nomor {} sama dengan nomor terakhir yang Anda sebut. Nomor dokumen baru harus "
                               "nomor terakhir + 1; pakai ini hanya bila memang revisi.".format(nomor))
    path_berkas = path_html(a.html, h["jenis_dokumen"], nomor) if a.html else None
    path_teks = path_txt(a.txt, h["jenis_dokumen"], nomor) if a.txt else None
    try:
        if path_berkas and path_teks and os.path.normcase(os.path.abspath(path_berkas)) == \
                os.path.normcase(os.path.abspath(path_teks)):
            raise ValueError("--html dan --txt menunjuk berkas yang sama ({}); pakai nama berbeda, mis. "
                             "--html invoice-{{nomor}}.html --txt invoice-{{nomor}}.txt".format(path_berkas))
        for arg, path in ((a.html, path_berkas), (a.txt, path_teks)):
            if path:
                siapkan_folder(arg, path)
    except (ValueError, OSError) as ex:
        sys.stderr.write("ERROR: {}\n".format(ex.strerror if isinstance(ex, OSError) and ex.strerror else ex))
        return 2
    try:
        if path_berkas:
            with open(path_berkas, "w", encoding="utf-8") as f:
                f.write(html_dok(h, nomor))
        if path_teks:
            with open(path_teks, "w", encoding="utf-8", newline="\n") as f:
                f.write(teks_polos(h, nomor))
        if data_counter is not None:
            sementara = a.counter_file + ".tmp"   # tulis dulu ke file sementara agar counter tidak rusak setengah jalan
            with open(sementara, "w", encoding="utf-8") as f:
                json.dump(data_counter, f, ensure_ascii=False, indent=2)
            os.replace(sementara, a.counter_file)
    except OSError as ex:
        sys.stderr.write("ERROR: gagal menulis file: {}\n".format(ex.strerror or ex))
        return 2

    if a.format == "json":
        h2 = dict(h)
        h2["nomor"] = nomor
        h2["keterangan_nomor"] = keterangan_nomor
        h2["perlu_diisi"] = kolom_kosong(h)
        h2["html_disimpan_ke"] = os.path.abspath(path_berkas) if path_berkas else None
        h2["txt_disimpan_ke"] = os.path.abspath(path_teks) if path_teks else None
        print(json.dumps(h2, default=lambda x: x.isoformat() if isinstance(x, datetime.date) else ke_json(x),
                         ensure_ascii=False, indent=2))
    else:
        print(markdown(h, nomor))
        print("")
        print("---")
        print("Info untuk penjual (jangan ikut dikirim):")
        if keterangan_nomor:
            print("- Nomor: " + keterangan_nomor)
        print("- Bea meterai: " + h["meterai"]["pesan"])
        if h["ppn"]:
            print("- PPN dihitung dengan DPP nilai lain 11/12 (PMK 131/2024, berlaku per {}): dari DPP persis lalu "
                  "dibulatkan ke bawah sekali. Pembulatan ini belum dicocokkan dengan Coretax; bila berbeda, ikuti "
                  "Coretax. Invoice ini bukan faktur pajak; buat faktur pajak di Coretax.".format(TANGGAL_ATURAN))
        if h.get("pph23"):
            q = h["pph23"]
            print("- PPh 23 (info, TIDAK mengubah total tagihan): {}% x {} ({}) = {}, dibulatkan ke bawah. Dipotong & "
                  "disetor oleh {} (pemberi kerja/pembeli jasa) saat membayar; Anda menerima bukti potong (simpan "
                  "untuk SPT Tahunan). Bila Anda memakai PPh final UMKM 0,5% dan sudah memberi Surat Keterangan PP 55 "
                  "ke pembeli, PPh 23 tidak dipotong - matikan pph23. Estimasi diterima bersih: {} - {} = {}.{}{} Dasar: UU PPh Pasal 23 "
                  "(jasa 2%; tanpa NPWP 100% lebih tinggi). Pembulatan belum dicocokkan dengan Coretax.".format(
                      format_angka(q["tarif"]).replace(".", ","), format_rp(q["dasar"]), q["sumber_dasar"],
                      format_rp(q["pph23"]), h["pembeli"]["nama"], format_rp(h["total"]), format_rp(q["pph23"]),
                      format_rp(q["estimasi_diterima_bersih"]),
                      " Bila ada DP/termin, PPh 23 dipotong per pembayaran sesuai porsinya." if h["dibayar"] or
                      h["termin"] else "",
                      " Bila invoice juga berisi barang (bukan jasa), isi pph23.dasar dengan nilai jasanya saja."
                      if q["sumber_dasar"] != "diisi pengguna" else ""))
        print("- Pembulatan: jumlah baris & diskon dibulatkan ke rupiah terdekat.")
        for w in h["peringatan"]:
            print("- PERHATIAN: " + w)
        kosong = kolom_kosong(h)
        if kosong:
            print("- PERLU DIISI: {} belum diberikan, ditulis \"{}\" di dokumen. Tanyakan ke pengguna atau "
                  "biarkan ia mengisi sendiri; jangan dikarang.".format(", ".join(kosong), ISI))
        if path_berkas or path_teks:
            urutan = []
            if path_berkas:
                urutan.append("lampirkan berkas di baris BERKAS (siap cetak) SEKALI")
            if path_teks:
                urutan.append(("bila gagal, " if path_berkas else "") + "lampirkan berkas di baris BERKAS TEKS "
                              "(versi teks) SEKALI")
            media = (" Bila satu-satunya cara melampirkan adalah baris lampiran di dalam balasan terakhir (mis. "
                     "MEDIA:<path>), lampirkan HANYA berkas di baris BERKAS TEKS, satu baris untuk dokumen ini, dan "
                     "pakai kalimat status netral (berhasil-tidaknya tidak diketahui)." if path_teks else "")
            print("- Berkas dibuat (nama berkas dari nomor {}), untuk invoice maupun kuitansi. Urutan: {}; pakai alat "
                  "kirim/lampir yang melaporkan berhasil/gagal, path PERSIS seperti di baris di bawah (jangan menyusun "
                  "atau menebak path) dan jangan mengulang dengan opsi lain.{} SESUDAH itu tulis balasan terakhir "
                  "berisi dokumen LENGKAP (bagian di atas garis ---): teks yang ditulis sebelum pemanggilan alat bisa "
                  "tidak sampai ke pengguna di Telegram/WhatsApp, jadi jangan menulis \"sudah di atas\". Tawarkan "
                  "\"balas 'kirim file'\" hanya bila percobaan melampirkan gagal atau hasilnya tidak diketahui, dengan "
                  "kalimat awam (tanpa kata HTML, path, sistem, error). Bila pengguna membalas 'kirim file': pakai "
                  "lagi path di bawah, JANGAN jalankan script lagi (nomor akan naik).".format(
                      nomor, "; ".join(urutan), media))
        if path_berkas:
            print("BERKAS: " + os.path.abspath(path_berkas))
        if path_teks:
            print("BERKAS TEKS: " + os.path.abspath(path_teks))
    return 0


if __name__ == "__main__":
    sys.exit(main())
