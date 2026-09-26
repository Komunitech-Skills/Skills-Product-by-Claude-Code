#!/usr/bin/env python3
"""Analisis rasio keuangan UMKM (likuiditas, profitabilitas, solvabilitas, aktivitas, tren,
kesiapan kredit) dari neraca + laba rugi sederhana. Python standar saja, semua hitungan Decimal.

Contoh (Windows: ganti python3 dengan python atau py):
  python3 rasio.py --jenis dagang --penjualan "Rp 480.000.000" --hpp 408jt --laba-bersih 24jt \
      --kas 12jt --piutang 6jt --persediaan 40jt --aset-tetap 42jt --utang-usaha 20jt \
      --utang-lancar-lain 5jt --utang-jangka-panjang 15jt --modal 60jt --bulan 12
  python3 rasio.py data.csv --jenis jasa            # tabel: kolom 1 = pos, kolom berikutnya = periode
  python3 rasio.py data.json                        # {"periode": [{"label": "2025", ...}, ...]}
  python3 rasio.py hasil-emkm-jan.json hasil-emkm-feb.json   # output laporan_emkm.py --format json
Keluaran: --format teks (Markdown, default) | json.
"""
import argparse
import csv
import io
import json
import re
import sys
from datetime import date
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP

VERSI = "1.0.0"
D0 = Decimal(0)
D100 = Decimal(100)
HARI_SETAHUN = Decimal(365)


class Galat(Exception):
    pass


# ---------------------------------------------------------------- pos laporan keuangan
# kode: (label, boleh_negatif, sinonim untuk baris tabel)
POS = {
    "penjualan": ("Penjualan / pendapatan usaha bersih", False,
                  ["penjualan", "penjualan bersih", "pendapatan", "pendapatan usaha", "pendapatan usaha bersih",
                   "omzet", "omset", "total penjualan", "pendapatan bersih", "revenue", "sales"]),
    "penjualan_kredit": ("Penjualan tempo/kredit", False,
                         ["penjualan kredit", "penjualan tempo", "penjualan non tunai tempo", "credit sales"]),
    "hpp": ("Harga pokok penjualan (HPP)", False,
            ["hpp", "harga pokok penjualan", "beban pokok penjualan", "harga pokok", "hpp/beban pokok",
             "harga pokok produksi", "cogs", "cost of goods sold"]),
    "laba_kotor": ("Laba kotor", True, ["laba kotor", "gross profit"]),
    "laba_usaha": ("Laba usaha", True, ["laba usaha", "laba operasional", "laba operasi", "operating income"]),
    "beban_bunga": ("Beban bunga / keuangan", False,
                    ["beban bunga", "bunga pinjaman", "beban keuangan", "biaya bunga", "interest expense"]),
    "beban_pajak": ("Beban pajak penghasilan", False,
                    ["beban pajak", "beban pajak penghasilan", "pph", "pajak penghasilan", "pph final"]),
    "laba_bersih": ("Laba (rugi) bersih", True,
                    ["laba bersih", "laba rugi bersih", "laba (rugi) bersih", "rugi bersih", "laba", "keuntungan bersih",
                     "net income", "net profit", "laba setelah pajak"]),
    "kas": ("Kas & bank", False,
            ["kas", "kas dan bank", "kas & bank", "kas dan setara kas", "kas & setara kas", "uang kas", "kas bank",
             "cash", "saldo kas"]),
    "piutang": ("Piutang usaha", False,
                ["piutang", "piutang usaha", "piutang dagang", "piutang pelanggan", "accounts receivable"]),
    "persediaan": ("Persediaan / stok", False,
                   ["persediaan", "persediaan barang", "stok", "stok barang", "persediaan barang dagang", "inventory",
                    "persediaan bahan"]),
    "aset_lancar_lain": ("Aset lancar lain", False,
                         ["aset lancar lain", "aset lancar lainnya", "piutang lain", "piutang lain-lain",
                          "uang muka", "biaya dibayar dimuka", "kasbon karyawan"]),
    "aset_lancar": ("Total aset lancar", False,
                    ["aset lancar", "total aset lancar", "jumlah aset lancar", "aktiva lancar", "total aktiva lancar",
                     "current assets"]),
    "aset_tetap": ("Aset tetap (nilai buku)", False,
                   ["aset tetap", "aset tetap bersih", "aset tetap nilai buku", "aktiva tetap", "peralatan",
                    "peralatan dan kendaraan", "fixed assets"]),
    "total_aset": ("Total aset", False,
                   ["total aset", "jumlah aset", "total aktiva", "jumlah aktiva", "aset", "total assets"]),
    "persediaan_awal": ("Persediaan awal periode", False, ["persediaan awal", "stok awal"]),
    "piutang_awal": ("Piutang awal periode", False, ["piutang awal"]),
    "total_aset_awal": ("Total aset awal periode", False, ["total aset awal", "aset awal"]),
    "modal_awal": ("Modal awal periode", True, ["modal awal", "ekuitas awal"]),
    "utang_usaha": ("Utang usaha / pemasok", False,
                    ["utang usaha", "utang dagang", "utang pemasok", "utang supplier", "hutang usaha", "hutang dagang",
                     "accounts payable"]),
    "utang_lancar_lain": ("Utang jangka pendek lain", False,
                          ["utang lancar lain", "utang jangka pendek lain", "utang bank jangka pendek",
                           "bagian lancar utang bank", "utang pajak", "utang lain", "utang lain-lain",
                           "titipan pajak", "hutang lain"]),
    "utang_lancar": ("Total utang lancar (≤ 1 tahun)", False,
                     ["utang lancar", "total utang lancar", "liabilitas jangka pendek", "kewajiban lancar",
                      "liabilitas lancar", "utang jangka pendek", "hutang lancar", "current liabilities"]),
    "utang_jangka_panjang": ("Utang jangka panjang", False,
                             ["utang jangka panjang", "utang bank jangka panjang", "pinjaman jangka panjang",
                              "liabilitas jangka panjang", "kewajiban jangka panjang", "hutang jangka panjang",
                              "utang bank", "pinjaman bank", "utang kur"]),
    "total_utang": ("Total utang (liabilitas)", False,
                    ["total utang", "total liabilitas", "jumlah liabilitas", "jumlah utang", "total kewajiban",
                     "liabilitas", "total hutang", "total liabilities"]),
    "modal": ("Modal / ekuitas akhir", True,
              ["modal", "ekuitas", "modal akhir", "total ekuitas", "modal pemilik", "jumlah ekuitas", "equity"]),
    "cicilan_bulanan": ("Total cicilan pinjaman per bulan", False,
                        ["cicilan bulanan", "cicilan per bulan", "angsuran per bulan", "cicilan", "angsuran"]),
    "bulan": ("Panjang periode (bulan)", False, ["bulan", "jumlah bulan", "periode bulan", "lama periode"]),
    "hari": ("Panjang periode (hari)", False, ["hari", "jumlah hari"]),
}
KODE_META = {"bulan", "hari"}
SINONIM = {}
for _k, (_l, _n, _s) in POS.items():
    for _x in _s + [_k, _k.replace("_", " ")]:
        SINONIM[_x] = _k

JENIS = {
    "dagang": "Dagang (warung, toko, grosir, reseller, toko online)",
    "jasa": "Jasa (laundry, salon, bengkel, konsultan, jasa lain)",
    "manufaktur": "Produksi/manufaktur kecil (konveksi, makanan olahan, kuliner, katering, kerajinan)",
    "umum": "Umum (jenis usaha tidak disebut)",
}
ALIAS_JENIS = {
    "dagang": ["dagang", "warung", "toko", "kelontong", "sembako", "grosir", "retail", "ritel", "reseller",
               "dropship", "toko online", "online shop", "olshop", "distributor", "perdagangan"],
    "jasa": ["jasa", "laundry", "salon", "bengkel", "konsultan", "servis", "service", "travel", "klinik",
             "kursus", "fotografi", "agensi", "percetakan jasa"],
    "manufaktur": ["manufaktur", "produksi", "pabrik", "konveksi", "kuliner", "warung makan", "rumah makan",
                   "resto", "restoran", "katering", "catering", "makanan", "minuman", "kue", "bakery", "kerajinan",
                   "mebel", "furnitur", "industri"],
    "umum": ["umum", "campuran", "lainnya", "lain"],
}

# Ambang wajar: (arah, batas_baik, batas_waspada). arah "T" = makin tinggi makin baik, "R" = makin rendah.
# Pedoman praktis skill ini (bukan standar resmi OJK/bank) — dasar & sumber: references/ambang-wajar.md
AMBANG = {
    "rasio_lancar": {"dagang": ("T", "1.5", "1.0"), "jasa": ("T", "1.2", "1.0"),
                     "manufaktur": ("T", "1.5", "1.1"), "umum": ("T", "1.5", "1.0")},
    "rasio_cepat": {"dagang": ("T", "0.5", "0.2"), "jasa": ("T", "1.0", "0.7"),
                    "manufaktur": ("T", "0.8", "0.5"), "umum": ("T", "0.8", "0.5")},
    "rasio_kas": {"dagang": ("T", "0.2", "0.1"), "jasa": ("T", "0.3", "0.15"),
                  "manufaktur": ("T", "0.2", "0.1"), "umum": ("T", "0.2", "0.1")},
    "margin_kotor": {"dagang": ("T", "15", "8"), "jasa": ("T", "40", "25"),
                     "manufaktur": ("T", "25", "15"), "umum": ("T", "20", "10")},
    "margin_bersih": {"dagang": ("T", "5", "2"), "jasa": ("T", "15", "8"),
                      "manufaktur": ("T", "8", "4"), "umum": ("T", "8", "3")},
    "roa": {"dagang": ("T", "10", "5"), "jasa": ("T", "15", "7"),
            "manufaktur": ("T", "8", "4"), "umum": ("T", "10", "5")},
    "roe": {j: ("T", "15", "6") for j in JENIS},
    "der": {j: ("R", "1.0", "2.0") for j in JENIS},
    "dar": {j: ("R", "50", "67") for j in JENIS},
    "cakupan_bunga": {j: ("T", "3", "1.5") for j in JENIS},
    "hari_persediaan": {"dagang": ("R", "30", "60"), "manufaktur": ("R", "60", "90"), "umum": ("R", "45", "90")},
    "hari_piutang": {"dagang": ("R", "30", "45"), "jasa": ("R", "45", "60"),
                     "manufaktur": ("R", "45", "60"), "umum": ("R", "45", "60")},
}

# Saran tindakan per rasio (dipakai bila status waspada/bahaya)
SARAN = {
    "rasio_lancar": "Utang jangka pendek hampir/melebihi aset lancar. Tunda pembelian aset & prive besar, "
                    "negosiasikan tempo pemasok lebih panjang, tagih piutang lebih cepat, dan hindari menutup "
                    "utang dengan utang baru.",
    "rasio_cepat": "Aset lancar terlalu banyak tertahan di stok. Kurangi belanja stok yang lambat laku, "
                   "jual/promo barang lama, dan sisihkan kas cadangan minimal 1 bulan biaya tetap.",
    "rasio_kas": "Kas tunai tipis dibanding tagihan jangka pendek. Buat pos 'dana cadangan' terpisah, "
                 "setor rutin (mis. 5% dari penjualan harian), dan jadwalkan pembayaran besar setelah hari ramai.",
    "margin_kotor": "Selisih harga jual vs modal barang tipis. Cek harga beli di pemasok lain/beli lebih "
                    "banyak sekaligus, naikkan harga produk yang laris secara bertahap, dan kurangi barang "
                    "bermargin rendah (hitung per produk dengan skill hitung-hpp).",
    "margin_bersih": "Laba bersih kecil dibanding penjualan. Urutkan biaya operasional dari yang terbesar, "
                     "pangkas yang tidak menambah penjualan, dan cek apakah gaji/sewa sudah terlalu besar untuk "
                     "omzet sekarang.",
    "roa": "Aset belum menghasilkan laba sepadan. Jual/sewakan peralatan yang jarang dipakai, kurangi stok "
           "menumpuk, dan fokus pada produk/jasa yang paling laku.",
    "roe": "Hasil untuk modal pemilik rendah. Bandingkan dengan bunga pinjaman/deposito: bila di bawahnya, "
           "perbaiki margin dan efisiensi dulu sebelum menambah modal atau pinjaman.",
    "der": "Utang besar dibanding modal sendiri. Jangan ambil pinjaman baru dulu, dahulukan melunasi utang "
           "berbunga tertinggi, dan tahan prive agar laba menambah modal.",
    "dar": "Sebagian besar aset dibiayai utang. Kurangi ketergantungan pada pinjaman; tahan laba di usaha "
           "(prive secukupnya) agar porsi modal sendiri naik.",
    "cakupan_bunga": "Laba usaha hampir habis untuk bunga. Pertimbangkan restrukturisasi/negosiasi tenor ke "
                     "bank resmi, dan jangan menambah utang berbunga.",
    "hari_persediaan": "Stok terlalu lama mengendap. Catat stok per barang (skill buku-stok), stop belanja "
                       "barang yang tidak laku 30 hari, beli lebih sering dalam jumlah kecil, dan promo barang lama.",
    "hari_piutang": "Pelanggan terlalu lama membayar. Tetapkan batas tempo tertulis, kirim pengingat sopan "
                    "sebelum jatuh tempo (skill tagih-piutang), dan batasi bon untuk pelanggan yang telat.",
}

SARAN_KHUSUS = {
    "rugi": "Usaha sedang RUGI — hentikan kebocoran dulu: pisahkan uang pribadi dari uang usaha, daftar semua "
            "biaya bulanan dan potong yang tidak menambah penjualan, cek harga jual vs HPP per produk (skill "
            "hitung-hpp), dan jangan menambah pinjaman untuk menutup rugi.",
    "modal_negatif": "Modal sudah habis (utang lebih besar dari semua aset). Jangan ambil utang baru; susun daftar "
                     "semua utang + jatuh temponya, bicarakan penjadwalan ulang dengan pemberi pinjaman resmi, dan "
                     "pertimbangkan konsultasi ke pendamping UMKM/Dinas Koperasi setempat.",
}

NAMA_RASIO = {
    "rasio_lancar": ("Rasio lancar (current ratio)", "likuiditas", "x"),
    "rasio_cepat": ("Rasio cepat (quick ratio)", "likuiditas", "x"),
    "rasio_kas": ("Rasio kas (cash ratio)", "likuiditas", "x"),
    "modal_kerja": ("Modal kerja bersih", "likuiditas", "Rp"),
    "margin_kotor": ("Margin laba kotor", "profitabilitas", "%"),
    "margin_usaha": ("Margin laba usaha", "profitabilitas", "%"),
    "margin_bersih": ("Margin laba bersih", "profitabilitas", "%"),
    "roa": ("ROA disetahunkan (laba ÷ aset)", "profitabilitas", "%"),
    "roe": ("ROE disetahunkan (laba ÷ modal)", "profitabilitas", "%"),
    "der": ("DER (utang ÷ modal)", "solvabilitas", "x"),
    "dar": ("DAR (utang ÷ aset)", "solvabilitas", "%"),
    "cakupan_bunga": ("Cakupan bunga (laba usaha ÷ bunga)", "solvabilitas", "x"),
    "perputaran_persediaan": ("Perputaran persediaan (per periode)", "aktivitas", "x"),
    "hari_persediaan": ("Umur stok (hari)", "aktivitas", "hari"),
    "perputaran_piutang": ("Perputaran piutang (per periode)", "aktivitas", "x"),
    "hari_piutang": ("Lama piutang tertagih (hari)", "aktivitas", "hari"),
    "hari_utang": ("Lama bayar pemasok (hari)", "aktivitas", "hari"),
    "siklus_kas": ("Siklus kas (hari stok + hari piutang − hari utang)", "aktivitas", "hari"),
    "perputaran_aset": ("Perputaran aset disetahunkan", "aktivitas", "x"),
}
KELOMPOK = [("likuiditas", "Likuiditas — sanggup bayar tagihan jangka pendek?"),
            ("profitabilitas", "Profitabilitas — seberapa untung?"),
            ("solvabilitas", "Solvabilitas — seberapa besar bergantung pada utang?"),
            ("aktivitas", "Aktivitas — seberapa cepat stok & piutang jadi uang?")]


# ---------------------------------------------------------------- angka
def parse_angka(teks):
    """Nominal/angka gaya Indonesia → Decimal. None bila tidak terbaca.

    Diterima: 15000, "Rp 15.000", "15.000,50", "1,250,000.50", "(15.000)", "-15.000", "15rb", "1,5jt",
    "2 juta", "1,2 M", "15k", "15.000,-". Kosong/"-" → 0.
    """
    if teks is None:
        return None
    if isinstance(teks, (int, Decimal)):
        return Decimal(teks)
    if isinstance(teks, float):
        return Decimal(str(teks))
    s = str(teks).strip().lower()
    if s in ("", "-", "--", "–", "—", "nihil", "nol"):
        return D0
    negatif = False
    if s.startswith("(") and s.endswith(")"):
        negatif, s = True, s[1:-1].strip()
    s = s.replace("idr", "").replace("rp.", "").replace("rp", "").strip()
    s = re.sub(r"[.,]\s*-+$", "", s).strip()
    if s.startswith("-") or s.startswith("−"):
        negatif, s = True, s[1:].strip()
    elif s.endswith("-") and len(s) > 1:
        negatif, s = True, s[:-1].strip()
    kali = Decimal(1)
    m = re.search(r"(rb|ribu|k|jt|juta|m|miliar|milyar|t)\.?$", s)
    if m:
        kali = {"rb": 10 ** 3, "ribu": 10 ** 3, "k": 10 ** 3, "jt": 10 ** 6, "juta": 10 ** 6,
                "m": 10 ** 9, "miliar": 10 ** 9, "milyar": 10 ** 9, "t": 10 ** 12}[m.group(1)]
        kali = Decimal(kali)
        s = s[:m.start()].strip()
    s = s.replace(" ", "").replace(" ", "")
    if not s or not re.fullmatch(r"[\d.,]+", s) or not re.search(r"\d", s):
        return None
    if "," in s and "." in s:
        if s.rfind(",") > s.rfind("."):
            s = s.replace(".", "").replace(",", ".")
        else:
            s = s.replace(",", "")
    elif "," in s:
        b = s.split(",")
        if len(b) == 2 and (len(b[1]) != 3 or kali != 1):
            s = s.replace(",", ".")
        elif all(len(x) == 3 for x in b[1:]):
            s = s.replace(",", "")
        else:
            return None
    elif "." in s:
        b = s.split(".")
        if len(b) == 2 and (len(b[1]) != 3 or kali != 1):
            pass
        elif all(len(x) == 3 for x in b[1:]):
            s = s.replace(".", "")
        else:
            return None
    try:
        n = Decimal(s) * kali
    except InvalidOperation:
        return None
    return -n if negatif else n


def bulat(d, tempat=0):
    q = Decimal(1).scaleb(-tempat)
    return Decimal(d).quantize(q, rounding=ROUND_HALF_UP)


def rp(n):
    n = int(bulat(n))
    t = "{:,}".format(abs(n)).replace(",", ".")
    return ("−Rp " if n < 0 else "Rp ") + t


def angka_id(d, tempat):
    t = "{:,.{p}f}".format(bulat(d, tempat), p=tempat)
    return t.replace(",", "_").replace(".", ",").replace("_", ".")


def fmt(nilai, satuan):
    if nilai is None:
        return "—"
    if satuan == "Rp":
        return rp(nilai)
    if satuan == "%":
        return angka_id(nilai, 1) + "%"
    if satuan == "hari":
        return angka_id(nilai, 1) + " hari"
    return angka_id(nilai, 2) + "x"


def ke_json(o):
    if isinstance(o, Decimal):
        return int(o) if o == o.to_integral_value() else float(o)
    if isinstance(o, date):
        return o.isoformat()
    raise TypeError(type(o))


# ---------------------------------------------------------------- baca input
def normal_nama(teks):
    s = str(teks).strip().lower()
    s = re.sub(r"^[\d.\s)]+(?=[a-z])", "", s)       # "1. Kas" → "kas"
    s = re.sub(r"\s*\((rp|idr)\)\s*$", "", s)
    s = s.replace("*", "").replace(":", "").strip()
    s = re.sub(r"\s+", " ", s)
    return s


def cari_kode(nama):
    s = normal_nama(nama)
    if s in SINONIM:
        return SINONIM[s]
    s2 = s.replace("hutang", "utang").replace("aktiva", "aset").replace("&", "dan")
    return SINONIM.get(s2)


def baca_tabel(teks, nama_file):
    """Tabel: kolom 1 = pos, kolom berikutnya = periode. Pemisah ; , tab atau | (Markdown)."""
    baris_mentah = [b for b in teks.splitlines() if b.strip()]
    if not baris_mentah:
        raise Galat("File %s kosong." % nama_file)
    if all(b.strip().startswith("|") for b in baris_mentah[:2]):
        rows = []
        for b in baris_mentah:
            sel = [c.strip() for c in b.strip().strip("|").split("|")]
            if all(re.fullmatch(r":?-{2,}:?", c) for c in sel if c):
                continue
            rows.append(sel)
    else:
        contoh = "\n".join(baris_mentah[:5])
        pemisah = "\t" if "\t" in contoh else (";" if contoh.count(";") >= contoh.count(",") else ",")
        rows = [r for r in csv.reader(io.StringIO("\n".join(baris_mentah)), delimiter=pemisah)]
    if len(rows) < 2 or len(rows[0]) < 2:
        raise Galat("Tabel di %s tidak terbaca. Format: kolom pertama nama pos (Kas, Piutang, ...), "
                    "kolom berikutnya angka per periode, baris pertama judul periode." % nama_file)
    judul = rows[0]
    label = [j.strip() or "Periode %d" % i for i, j in enumerate(judul[1:], 1)]
    periode = [{"label": l, "_sumber": nama_file} for l in label]
    catatan = []
    for no, r in enumerate(rows[1:], 2):
        if not r or not r[0].strip():
            continue
        kode = cari_kode(r[0])
        if kode is None:
            catatan.append("Baris %d '%s' tidak dikenal → dilewati (ganti nama pos atau hapus bila bukan angka "
                           "laporan)." % (no, r[0].strip()))
            continue
        for i, p in enumerate(periode):
            sel = r[i + 1] if i + 1 < len(r) else ""
            if sel.strip() == "":
                continue
            p[kode] = sel
    return periode, catatan


def baca_emkm(d, nama_file):
    """Petakan output laporan_emkm.py --format json (skill laporan-keuangan-emkm) ke pos rasio."""
    lr, pk = d["laba_rugi"], d["posisi_keuangan"]
    a, l, e = pk["aset"], pk["liabilitas"], pk["ekuitas"]
    sa = d.get("saldo_awal", {})
    per = d.get("periode", {})
    p = {
        "label": per.get("teks") or nama_file, "_sumber": nama_file, "_emkm": True,
        "penjualan": lr.get("pendapatan_usaha_bersih"), "penjualan_kredit": lr.get("penjualan_tempo"),
        "hpp": lr.get("beban_pokok_penjualan"), "laba_kotor": lr.get("laba_kotor"),
        "laba_usaha": lr.get("laba_usaha"), "beban_bunga": lr.get("beban_keuangan"),
        "beban_pajak": lr.get("beban_pajak_penghasilan"), "laba_bersih": lr.get("laba_bersih"),
        "kas": a.get("kas_dan_setara_kas"), "piutang": a.get("piutang_usaha"),
        "persediaan": a.get("persediaan"), "aset_lancar_lain": a.get("piutang_lain"),
        "aset_tetap": a.get("aset_tetap_nilai_buku"), "total_aset": a.get("total_aset"),
        "utang_usaha": l.get("utang_usaha"), "modal": e.get("modal_akhir"),
        "total_utang": l.get("total_liabilitas"),
        "persediaan_awal": sa.get("persediaan"), "piutang_awal": sa.get("piutang"), "modal_awal": sa.get("modal"),
        "_utang_bank": l.get("utang_bank_pinjaman") or 0,
        "_titipan_pajak": l.get("utang_pajak_daerah_titipan") or 0,
        "_status_sumber": d.get("status", ""),
    }
    try:
        aw, ak = date.fromisoformat(per["awal"]), date.fromisoformat(per["akhir"])
        p["hari"] = (ak - aw).days + 1
        p["_tanggal_akhir"] = ak.isoformat()
    except (KeyError, TypeError, ValueError):
        pass
    if per.get("jumlah_bulan"):
        p["bulan"] = per["jumlah_bulan"]
    return p


def baca_file(path):
    try:
        with open(path, "rb") as f:
            mentah = f.read()
    except FileNotFoundError:
        raise Galat("File tidak ditemukan: %s" % path)
    except OSError as e:
        raise Galat("File %s tidak bisa dibuka: %s" % (path, e))
    if not mentah.strip():
        raise Galat("File %s kosong." % path)
    if mentah[:4] in (b"PK\x03\x04", b"%PDF") or b"\x00" in mentah[:1024]:
        raise Galat("File %s adalah Excel/PDF/biner. Simpan sebagai CSV (Excel: File → Save As → CSV) atau "
                    "tempel angkanya sebagai tabel teks." % path)
    try:
        teks = mentah.decode("utf-8-sig")
    except UnicodeDecodeError:
        teks = mentah.decode("latin-1")
    if path.lower().endswith(".json") or teks.lstrip().startswith(("{", "[")):
        try:
            d = json.loads(teks)
        except json.JSONDecodeError as e:
            raise Galat("File %s bukan JSON yang valid (%s)." % (path, e))
        if isinstance(d, dict) and "laba_rugi" in d and "posisi_keuangan" in d:
            return [baca_emkm(d, path)], [], {"nama_usaha": d.get("nama_usaha")} if d.get("nama_usaha") else {}
        if isinstance(d, dict) and "periode" in d and isinstance(d["periode"], list):
            meta = {k: v for k, v in d.items() if k != "periode"}
            per = []
            for i, x in enumerate(d["periode"], 1):
                if not isinstance(x, dict):
                    raise Galat("Isi 'periode' di %s harus daftar objek {pos: angka}." % path)
                q = dict(x)
                q.setdefault("label", "Periode %d" % i)
                q["_sumber"] = path
                per.append(q)
            return per, [], meta
        if isinstance(d, list):
            return [dict(x, _sumber=path) for x in d if isinstance(x, dict)], []
        if isinstance(d, dict):
            return [dict(d, _sumber=path)], []
        raise Galat("Struktur JSON %s tidak dikenal." % path)
    return baca_tabel(teks, path)


def normalisasi_periode(p, catatan):
    """Ubah semua nilai jadi Decimal; catat yang tidak terbaca / mustahil."""
    hasil = {"label": str(p.get("label", "Periode")), "asumsi": [], "peringatan": [], "mustahil": set()}
    for k, v in p.items():
        if k.startswith("_"):
            hasil[k] = v
            continue
        if k == "label":
            continue
        kode = k if k in POS else cari_kode(k)
        if kode is None:
            if k not in ("nama_usaha", "jenis", "jenis_usaha"):
                catatan.append("[%s] pos '%s' tidak dikenal → dilewati." % (hasil["label"], k))
            continue
        n = parse_angka(v)
        if n is None:
            hasil["peringatan"].append("%s = '%s' tidak terbaca sebagai angka → dianggap tidak diisi."
                                       % (POS[kode][0], v))
            continue
        if n < 0 and not POS[kode][1]:
            hasil["mustahil"].add(kode)
            hasil["peringatan"].append("%s bernilai negatif (%s) — mustahil untuk pos ini. Rasio yang memakainya "
                                       "tidak dihitung; periksa lagi angkanya." % (POS[kode][0], rp(n)))
        hasil[kode] = n
    return hasil


# ---------------------------------------------------------------- hitung
def lengkapi(p, cfg):
    """Turunkan pos yang tidak diisi (aset lancar, total aset, utang, modal, panjang periode) & cek konsistensi."""
    A, W = p["asumsi"], p["peringatan"]

    def ada(k):
        return p.get(k) is not None

    def jumlah(kode_total, komponen, label):
        isi = [k for k in komponen if ada(k)]
        if not isi:
            return
        tot = sum((p[k] for k in isi), D0)
        if ada(kode_total):
            if len(isi) == len(komponen) and tot != p[kode_total]:
                W.append("%s diisi %s, tetapi jumlah rinciannya %s (selisih %s). Dipakai angka yang diisi; "
                         "cek lagi." % (label, rp(p[kode_total]), rp(tot), rp(p[kode_total] - tot)))
            return
        p[kode_total] = tot
        if any(k in p["mustahil"] for k in isi):
            p["mustahil"].add(kode_total)
        kosong = [POS[k][0] for k in komponen if not ada(k)]
        if kosong:
            A.append("%s dihitung dari rincian; %s tidak diisi → dianggap Rp 0." % (label, ", ".join(kosong)))

    # utang bank dari EMKM: tidak diketahui porsi jatuh tempo ≤ 1 tahun
    if p.get("_emkm"):
        ub = Decimal(str(p.get("_utang_bank", 0)))
        tp = Decimal(str(p.get("_titipan_pajak", 0)))
        if cfg.get("bagian_lancar_utang_bank") is not None:
            lancar_bank = min(cfg["bagian_lancar_utang_bank"], ub)
            A.append("Bagian utang bank yang jatuh tempo ≤ 12 bulan: %s (sisanya jangka panjang)." % rp(lancar_bank))
        else:
            lancar_bank = ub
            if ub > 0:
                A.append("Seluruh utang bank %s dianggap utang lancar (konservatif). Bila sebagian baru jatuh "
                         "tempo setelah 12 bulan, isi --bagian-lancar-utang-bank (total pokok cicilan 12 bulan "
                         "ke depan)." % rp(ub))
        p["utang_lancar_lain"] = lancar_bank + tp
        p["utang_jangka_panjang"] = ub - lancar_bank
        if p.get("_status_sumber", "").startswith("SEMENTARA"):
            W.append("Laporan sumber berstatus SEMENTARA (masih ada pertanyaan di laporan-keuangan-emkm). "
                     "Rasio ikut sementara.")

    if ada("penjualan") and ada("hpp"):
        lk = p["penjualan"] - p["hpp"]
        if ada("laba_kotor") and p["laba_kotor"] != lk:
            W.append("Laba kotor diisi %s, tetapi penjualan − HPP = %s. Dipakai penjualan − HPP."
                     % (rp(p["laba_kotor"]), rp(lk)))
        p["laba_kotor"] = lk
    jumlah("aset_lancar", ["kas", "piutang", "persediaan", "aset_lancar_lain"], "Total aset lancar")
    jumlah("utang_lancar", ["utang_usaha", "utang_lancar_lain"], "Total utang lancar")
    def tular(hasil, *sumber):
        if any(k in p["mustahil"] for k in sumber):
            p["mustahil"].add(hasil)

    if not ada("total_aset") and ada("aset_lancar") and ada("aset_tetap"):
        p["total_aset"] = p["aset_lancar"] + p["aset_tetap"]
        tular("total_aset", "aset_lancar", "aset_tetap")
    elif not ada("total_aset") and ada("aset_lancar"):
        p["total_aset"] = p["aset_lancar"]
        tular("total_aset", "aset_lancar")
        A.append("Aset tetap tidak diisi → total aset = aset lancar saja.")
    if not ada("total_utang") and (ada("utang_lancar") or ada("utang_jangka_panjang")):
        p["total_utang"] = p.get("utang_lancar", D0) + p.get("utang_jangka_panjang", D0)
        tular("total_utang", "utang_lancar", "utang_jangka_panjang")
        if not ada("utang_jangka_panjang"):
            A.append("Utang jangka panjang tidak diisi → dianggap Rp 0.")
    if ada("total_utang") and not ada("utang_lancar") and not ada("utang_jangka_panjang"):
        W.append("Hanya total utang yang diisi; rasio likuiditas butuh utang lancar (jatuh tempo ≤ 12 bulan).")
    if not ada("modal") and ada("total_aset") and ada("total_utang"):
        p["modal"] = p["total_aset"] - p["total_utang"]
        tular("modal", "total_aset", "total_utang")
        A.append("Modal dihitung = total aset − total utang = %s." % rp(p["modal"]))
    if not ada("total_utang") and ada("total_aset") and ada("modal"):
        p["total_utang"] = p["total_aset"] - p["modal"]
        tular("total_utang", "total_aset", "modal")
        A.append("Total utang dihitung = total aset − modal = %s." % rp(p["total_utang"]))
    if ada("total_aset") and ada("total_utang") and ada("modal"):
        sel = p["total_aset"] - p["total_utang"] - p["modal"]
        p["selisih_neraca"] = sel
        if sel != 0:
            W.append("Neraca TIDAK SEIMBANG: total aset %s ≠ utang %s + modal %s (selisih %s). Rasio tetap "
                     "dihitung, tetapi cek ulang angka neraca." % (rp(p["total_aset"]), rp(p["total_utang"]),
                                                                  rp(p["modal"]), rp(sel)))
    # panjang periode
    if ada("hari") and p["hari"] > 0:
        p["hari"] = Decimal(p["hari"])
        if not ada("bulan") or p["bulan"] <= 0:
            p["bulan"] = p["hari"] * 12 / HARI_SETAHUN
    elif ada("bulan") and p["bulan"] > 0:
        p["hari"] = HARI_SETAHUN * p["bulan"] / 12
    else:
        p["bulan"], p["hari"] = Decimal(12), HARI_SETAHUN
        A.append("Panjang periode tidak disebut → dianggap laporan 1 tahun (12 bulan, 365 hari).")
    if p["bulan"] < 3:
        W.append("Periode pendek (%s bulan): angka yang disetahunkan (ROA, ROE, perputaran aset) bisa meleset "
                 "karena musim ramai/sepi." % angka_id(p["bulan"], 1))


def bagi(a, b):
    if a is None or b is None or b == 0:
        return None
    return Decimal(a) / Decimal(b)


def nilai_status(kode, nilai, jenis):
    tab = AMBANG.get(kode, {})
    if jenis not in tab or nilai is None:
        return None, ""
    arah, baik, was = tab[jenis]
    baik, was = Decimal(baik), Decimal(was)
    sat = NAMA_RASIO[kode][2]
    if arah == "T":
        st = "baik" if nilai >= baik else ("waspada" if nilai >= was else "bahaya")
        teks = "≥ %s baik · %s–%s waspada · < %s bahaya" % (fmt(baik, sat), fmt(was, sat), fmt(baik, sat),
                                                            fmt(was, sat))
    else:
        st = "baik" if nilai <= baik else ("waspada" if nilai <= was else "bahaya")
        teks = "≤ %s baik · %s–%s waspada · > %s bahaya" % (fmt(baik, sat), fmt(baik, sat), fmt(was, sat),
                                                            fmt(was, sat))
    return st, teks


TAFSIR = {
    "rasio_lancar": lambda v: "Setiap Rp 1 utang jangka pendek dijamin %s aset lancar." % rp_kecil(v),
    "rasio_cepat": lambda v: "Tanpa menjual stok, tersedia %s untuk tiap Rp 1 utang jangka pendek." % rp_kecil(v),
    "rasio_kas": lambda v: "Uang kas/bank yang ada menutup %s dari utang jangka pendek." % pct(v),
    "margin_kotor": lambda v: "Dari tiap Rp 100.000 penjualan, sisa setelah modal barang Rp %s." % ribu(v),
    "margin_usaha": lambda v: "Dari tiap Rp 100.000 penjualan, %s usaha Rp %s." % (lr(v), ribu(abs(v))),
    "margin_bersih": lambda v: "Dari tiap Rp 100.000 penjualan, %s bersih Rp %s." % (lr(v), ribu(abs(v))),
    "roa": lambda v: "Tiap Rp 100.000 aset usaha menghasilkan %s Rp %s setahun." % (lr(v), ribu(abs(v))),
    "roe": lambda v: "Tiap Rp 100.000 modal pemilik menghasilkan %s Rp %s setahun." % (lr(v), ribu(abs(v))),
    "der": lambda v: "Utang = %s dari modal sendiri." % pct(v),
    "dar": lambda v: "%s%% aset usaha dibiayai utang." % angka_id(v, 1),
    "cakupan_bunga": lambda v: "Laba usaha cukup untuk membayar bunga %s kali." % angka_id(v, 1),
    "perputaran_persediaan": lambda v: "Stok 'habis dan diisi ulang' sekitar %s kali dalam periode ini." % angka_id(v, 1),
    "hari_persediaan": lambda v: "Barang rata-rata diam di gudang/rak ±%s hari sebelum terjual." % angka_id(v, 0),
    "perputaran_piutang": lambda v: "Piutang tertagih ±%s kali dalam periode ini." % angka_id(v, 1),
    "hari_piutang": lambda v: "Uang dari penjualan tempo rata-rata masuk setelah ±%s hari." % angka_id(v, 0),
    "hari_utang": lambda v: "Pemasok rata-rata dibayar setelah ±%s hari." % angka_id(v, 0),
    "siklus_kas": lambda v: ("Uang usaha tertahan ±%s hari dari beli barang sampai uang kembali." % angka_id(v, 0)
                             if v >= 0 else "Pemasok dibayar setelah uang pelanggan masuk (±%s hari lebih "
                                            "dulu) — menguntungkan kas." % angka_id(-v, 0)),
    "perputaran_aset": lambda v: "Tiap Rp 1 aset menghasilkan penjualan %s setahun." % rp_kecil(v),
    "modal_kerja": lambda v: ("Aset lancar melebihi utang lancar sebesar %s." % rp(v) if v >= 0
                              else "Utang lancar melebihi aset lancar sebesar %s." % rp(-v)),
}


def lr(v):
    return "rugi" if v < 0 else "laba"


def rp_kecil(v):
    return "Rp " + angka_id(v, 2)


def pct(v):
    return angka_id(v * 100, 0) + "%"


def ribu(v_persen):
    return angka_id(v_persen * 1000, 0)


def rasio(kode, nilai, rumus, jenis, status=None, alasan=None, catatan=None):
    nama, kel, sat = NAMA_RASIO[kode]
    r = {"kode": kode, "nama": nama, "kelompok": kel, "satuan": sat, "rumus": rumus,
         "nilai": bulat(nilai, 4) if nilai is not None else None, "status": status, "ambang": "",
         "tafsiran": "", "alasan_tidak_dihitung": alasan}
    if nilai is not None:
        st, ambang = nilai_status(kode, nilai, jenis)
        r["ambang"] = ambang
        if status is None:
            r["status"] = st or "info"
        r["tafsiran"] = TAFSIR[kode](nilai) if kode in TAFSIR else ""
    else:
        r["status"] = status or "tidak_dihitung"
        _, r["ambang"] = nilai_status(kode, Decimal(1), jenis) if kode in AMBANG and jenis in AMBANG[kode] \
            else (None, "")
    if catatan:
        r["tafsiran"] = (r["tafsiran"] + " " + catatan).strip()
    return r


def hitung_periode(p, jenis):
    g = p.get
    R = []
    mus = p["mustahil"]

    def rusak(*kode):
        bad = [POS[k][0] for k in kode if k in mus]
        return ("data mustahil: " + ", ".join(bad)) if bad else None

    def kurang(*kode):
        miss = [POS[k][0] for k in kode if g(k) is None]
        return ("data belum ada: " + ", ".join(miss)) if miss else None

    hari, bulan = p["hari"], p["bulan"]
    faktor_tahun = HARI_SETAHUN / hari

    # --- likuiditas
    al, ul = g("aset_lancar"), g("utang_lancar")
    for kode, pembilang, rumus, komp in (
            ("rasio_lancar", al, "aset lancar ÷ utang lancar", ("aset_lancar", "utang_lancar")),
            ("rasio_cepat", (al - (g("persediaan") or D0)) if al is not None else None,
             "(aset lancar − persediaan) ÷ utang lancar", ("aset_lancar", "utang_lancar")),
            ("rasio_kas", g("kas"), "kas & bank ÷ utang lancar", ("kas", "utang_lancar"))):
        alasan = rusak(*komp, "persediaan") or kurang(*komp)
        if alasan:
            R.append(rasio(kode, None, rumus, jenis, alasan=alasan))
        elif ul == 0:
            R.append(rasio(kode, None, rumus, jenis, status="info",
                           alasan="tidak ada utang jangka pendek — tidak ada tagihan dekat yang harus dibayar "
                                  "(kondisi aman)"))
        else:
            R.append(rasio(kode, bagi(pembilang, ul), rumus, jenis))
    if al is not None and ul is not None and not rusak("aset_lancar", "utang_lancar"):
        R.append(rasio("modal_kerja", al - ul, "aset lancar − utang lancar", jenis, status="info"))

    # --- profitabilitas
    pj = g("penjualan")
    for kode, pembilang, rumus in (("margin_kotor", g("laba_kotor"), "laba kotor ÷ penjualan × 100"),
                                   ("margin_usaha", g("laba_usaha"), "laba usaha ÷ penjualan × 100"),
                                   ("margin_bersih", g("laba_bersih"), "laba bersih ÷ penjualan × 100")):
        if kode == "margin_usaha" and g("laba_usaha") is None:
            continue
        pos_pembilang = {"margin_kotor": "hpp", "margin_usaha": "laba_usaha", "margin_bersih": "laba_bersih"}[kode]
        alasan = rusak("penjualan", pos_pembilang) or kurang("penjualan", pos_pembilang if kode != "margin_kotor"
                                                             else "hpp")
        if alasan:
            R.append(rasio(kode, None, rumus, jenis, alasan=alasan))
        elif pj == 0:
            R.append(rasio(kode, None, rumus, jenis, alasan="penjualan Rp 0 — margin tidak bisa dihitung"))
        else:
            cat = "Usaha RUGI pada periode ini." if pembilang < 0 else None
            R.append(rasio(kode, bagi(pembilang, pj) * D100, rumus, jenis, catatan=cat))

    lb = g("laba_bersih")
    ta = g("total_aset")
    ta_rata = (ta + g("total_aset_awal")) / 2 if (ta is not None and g("total_aset_awal") is not None) else ta
    rumus_roa = "laba bersih ÷ %s × 100 × (365 ÷ %s hari)" % ("rata-rata total aset" if g("total_aset_awal")
                                                               is not None else "total aset",
                                                               angka_id(hari, 0))
    alasan = rusak("laba_bersih", "total_aset") or kurang("laba_bersih", "total_aset")
    if alasan:
        R.append(rasio("roa", None, rumus_roa, jenis, alasan=alasan))
    elif not ta_rata:
        R.append(rasio("roa", None, rumus_roa, jenis, alasan="total aset Rp 0"))
    else:
        R.append(rasio("roa", lb / ta_rata * D100 * faktor_tahun, rumus_roa, jenis,
                       catatan="Usaha RUGI pada periode ini." if lb < 0 else None))

    md = g("modal")
    md_rata = (md + g("modal_awal")) / 2 if (md is not None and g("modal_awal") is not None
                                             and g("modal_awal") > 0 and md > 0) else md
    rumus_roe = "laba bersih ÷ %s × 100 × (365 ÷ %s hari)" % ("rata-rata modal" if md_rata != md else "modal akhir",
                                                               angka_id(hari, 0))
    alasan = rusak("laba_bersih", "modal") or kurang("laba_bersih", "modal")
    if alasan:
        R.append(rasio("roe", None, rumus_roe, jenis, alasan=alasan))
    elif md <= 0:
        R.append(rasio("roe", None, rumus_roe, jenis, status="bahaya",
                       alasan="modal %s — %s; ROE tidak bermakna" %
                              (rp(md), "utang lebih besar dari aset (modal habis)" if md < 0 else "modal nol")))
    else:
        R.append(rasio("roe", lb / md_rata * D100 * faktor_tahun, rumus_roe, jenis,
                       catatan="Usaha RUGI pada periode ini." if lb < 0 else None))

    # --- solvabilitas
    tu = g("total_utang")
    alasan = rusak("total_utang", "modal") or kurang("total_utang", "modal")
    if alasan:
        R.append(rasio("der", None, "total utang ÷ modal", jenis, alasan=alasan))
    elif md <= 0:
        R.append(rasio("der", None, "total utang ÷ modal", jenis, status="bahaya" if tu > 0 else "info",
                       alasan="modal %s — utang tidak lagi ditopang modal sendiri; DER tidak bermakna" % rp(md)
                       if tu > 0 else "tidak ada utang dan modal nol"))
    else:
        R.append(rasio("der", tu / md, "total utang ÷ modal", jenis))
    alasan = rusak("total_utang", "total_aset") or kurang("total_utang", "total_aset")
    if alasan:
        R.append(rasio("dar", None, "total utang ÷ total aset × 100", jenis, alasan=alasan))
    elif ta == 0:
        R.append(rasio("dar", None, "total utang ÷ total aset × 100", jenis, alasan="total aset Rp 0"))
    else:
        R.append(rasio("dar", tu / ta * D100, "total utang ÷ total aset × 100", jenis))

    bb = g("beban_bunga")
    if bb is not None and bb > 0:
        if g("laba_usaha") is not None:
            ebit, sumber = g("laba_usaha"), "laba usaha ÷ beban bunga"
        elif lb is not None:
            ebit, sumber = lb + bb + (g("beban_pajak") or D0), "(laba bersih + bunga + pajak) ÷ beban bunga"
        else:
            ebit, sumber = None, "laba usaha ÷ beban bunga"
        if ebit is None:
            R.append(rasio("cakupan_bunga", None, sumber, jenis, alasan="data belum ada: laba"))
        else:
            R.append(rasio("cakupan_bunga", ebit / bb, sumber, jenis))

    # --- aktivitas
    hpp, ps = g("hpp"), g("persediaan")
    ps_rata = (ps + g("persediaan_awal")) / 2 if (ps is not None and g("persediaan_awal") is not None) else ps
    label_ps = "rata-rata persediaan" if g("persediaan_awal") is not None else "persediaan akhir"
    if jenis == "jasa" and not ps:
        pass
    else:
        alasan = rusak("hpp", "persediaan", "persediaan_awal") or kurang("hpp", "persediaan")
        if alasan:
            R.append(rasio("hari_persediaan", None, "%s × hari periode ÷ HPP" % label_ps, jenis, alasan=alasan))
        elif hpp == 0:
            R.append(rasio("hari_persediaan", None, "%s × hari periode ÷ HPP" % label_ps, jenis,
                           alasan="HPP Rp 0 — umur stok tidak bisa dihitung"))
        elif ps_rata == 0:
            r0 = rasio("hari_persediaan", D0, "%s × hari periode ÷ HPP" % label_ps, jenis)
            r0["tafsiran"] = "Tidak ada stok tersisa di akhir periode."
            R.append(r0)
        else:
            R.append(rasio("perputaran_persediaan", hpp / ps_rata, "HPP ÷ %s" % label_ps, jenis, status="info"))
            R.append(rasio("hari_persediaan", ps_rata * hari / hpp, "%s × hari periode ÷ HPP" % label_ps, jenis))

    pi = g("piutang")
    pi_rata = (pi + g("piutang_awal")) / 2 if (pi is not None and g("piutang_awal") is not None) else pi
    basis = g("penjualan_kredit") if g("penjualan_kredit") else pj
    label_basis = "penjualan tempo" if g("penjualan_kredit") else "total penjualan"
    label_pi = "rata-rata piutang" if g("piutang_awal") is not None else "piutang akhir"
    if pi is not None:
        alasan = rusak("piutang", "penjualan", "piutang_awal") or kurang("penjualan")
        rumus = "%s × hari periode ÷ %s" % (label_pi, label_basis)
        if alasan:
            R.append(rasio("hari_piutang", None, rumus, jenis, alasan=alasan))
        elif not basis:
            R.append(rasio("hari_piutang", None, rumus, jenis, alasan="penjualan Rp 0"))
        elif pi_rata == 0:
            r0 = rasio("hari_piutang", D0, rumus, jenis)
            r0["tafsiran"] = "Tidak ada piutang — semua penjualan sudah dibayar."
            R.append(r0)
        else:
            cat = None if g("penjualan_kredit") else ("Dihitung dari total penjualan (tunai + tempo), jadi angka "
                                                      "sebenarnya untuk pelanggan tempo lebih lama.")
            R.append(rasio("perputaran_piutang", basis / pi_rata, "%s ÷ %s" % (label_basis, label_pi), jenis,
                           status="info"))
            R.append(rasio("hari_piutang", pi_rata * hari / basis, rumus, jenis, catatan=cat))

    uu = g("utang_usaha")
    if uu is not None and hpp and "utang_usaha" not in mus and "hpp" not in mus:
        r0 = rasio("hari_utang", uu * hari / hpp, "utang usaha × hari periode ÷ HPP", jenis, status="info")
        if uu == 0:
            r0["tafsiran"] = "Tidak ada utang ke pemasok — belanja dibayar tunai."
        R.append(r0)
    nilai = {r["kode"]: r["nilai"] for r in R}
    if nilai.get("hari_persediaan") is not None and nilai.get("hari_piutang") is not None:
        sik = nilai["hari_persediaan"] + nilai["hari_piutang"] - (nilai.get("hari_utang") or D0)
        R.append(rasio("siklus_kas", sik, "hari stok + hari piutang − hari utang", jenis, status="info"))
    if pj is not None and ta and "total_aset" not in mus:
        R.append(rasio("perputaran_aset", pj / (ta_rata or ta) * faktor_tahun, "penjualan ÷ total aset × (365 ÷ "
                       "hari)", jenis, status="info"))
    for r in R:
        if r["kode"] in ("roa", "roe") and r["nilai"] is not None and r["nilai"] > 100:
            r["tafsiran"] += (" Angka >100% biasa terjadi bila aset/modal tercatat kecil (usaha rumahan, peralatan "
                              "pribadi tidak dicatat) atau periode pendek disetahunkan — jangan dijadikan patokan "
                              "tunggal.")
    return R


def status_cicilan(persen):
    if persen is None:
        return None
    if persen >= 100:
        return "⛔ laba tidak cukup untuk cicilan"
    if persen > 50:
        return "🔴 TERLALU BERAT"
    if persen > 30:
        return "🟡 BERAT, perlu hati-hati"
    return "🟢 AMAN"


def kesiapan_kredit(p, R):
    ni = {r["kode"]: r for r in R}
    cek = []
    lb, md = p.get("laba_bersih"), p.get("modal")

    def tambah(ok, teks):
        cek.append({"status": ok, "teks": teks})

    if lb is None:
        tambah("?", "Laba bersih belum diketahui — bank selalu menilai kemampuan bayar dari laba.")
    else:
        tambah("✓" if lb > 0 else "✗", "Usaha %s %s pada periode ini." % ("UNTUNG" if lb > 0 else "RUGI", rp(abs(lb))))
    if md is None or "modal" in p["mustahil"]:
        tambah("?", "Modal/ekuitas belum diketahui atau dihitung dari angka mustahil.")
    else:
        tambah("✓" if md > 0 else "✗", "Modal sendiri %s %s." % (rp(md), "positif" if md > 0 else
                                                               "habis/negatif — utang melebihi aset"))
    der = ni.get("der")
    if der and der["nilai"] is not None:
        tambah({"baik": "✓", "waspada": "⚠", "bahaya": "✗"}.get(der["status"], "?"),
               "DER %s (utang dibanding modal)." % fmt(der["nilai"], "x"))
    rl = ni.get("rasio_lancar")
    if rl:
        if rl["nilai"] is not None:
            tambah({"baik": "✓", "waspada": "⚠", "bahaya": "✗"}.get(rl["status"], "?"),
                   "Rasio lancar %s." % fmt(rl["nilai"], "x"))
        elif rl["status"] == "info":
            tambah("✓", "Tidak ada utang jangka pendek.")
    if p.get("selisih_neraca"):
        tambah("✗", "Neraca belum seimbang (selisih %s) — rapikan dulu sebelum dilampirkan." %
               rp(p["selisih_neraca"]))
    laba_bulan = (lb / p["bulan"]) if (lb is not None and p["bulan"]) else None
    hasil = {"laba_bersih_per_bulan": bulat(laba_bulan) if laba_bulan is not None else None, "cek": cek,
             "cicilan_bulanan": p.get("cicilan_bulanan"), "rasio_cicilan_persen": None, "status_cicilan": None}
    ci = p.get("cicilan_bulanan")
    if ci is not None and laba_bulan is not None:
        if laba_bulan <= 0:
            hasil["status_cicilan"] = "⛔ laba tidak cukup untuk cicilan"
            tambah("✗", "Cicilan %s/bulan tidak bisa ditutup dari laba (laba ≤ 0)." % rp(ci))
        else:
            persen = bulat(ci / laba_bulan * D100, 1)
            hasil["rasio_cicilan_persen"] = persen
            hasil["status_cicilan"] = status_cicilan(persen)
            tambah("✓" if persen <= 30 else ("⚠" if persen <= 50 else "✗"),
                   "Cicilan %s/bulan = %s dari laba bersih per bulan %s → %s." %
                   (rp(ci), angka_id(persen, 1) + "%", rp(laba_bulan), status_cicilan(persen)))
    buruk = sum(1 for c in cek if c["status"] == "✗")
    ragu = sum(1 for c in cek if c["status"] in ("⚠", "?"))
    hasil["kesimpulan"] = ("BELUM SIAP — perbaiki poin ✗ dulu" if buruk else
                           ("PERLU PERBAIKAN/DATA TAMBAHAN — lihat poin ⚠/?" if ragu else
                            "ANGKA CUKUP SEHAT untuk dibawa ke bank"))
    hasil["catatan"] = ("Ini pembacaan angka, bukan keputusan kredit. Bank juga menilai karakter, riwayat "
                        "SLIK OJK, agunan, legalitas, dan prospek usaha. Simulasi cicilan & dokumen KUR: skill "
                        "pengajuan-kur.")
    return hasil


def urut_masalah(R):
    bobot = {"bahaya": 0, "waspada": 1}
    return sorted([r for r in R if r["status"] in bobot and r["kode"] in SARAN],
                  key=lambda r: (bobot[r["status"]], [k for k in SARAN].index(r["kode"])))


def tren(periode_hasil):
    if len(periode_hasil) < 2:
        return []
    out = []
    kode_urut = list(NAMA_RASIO)
    for kode in kode_urut + ["penjualan", "laba_bersih"]:
        deret = []
        for ph in periode_hasil:
            if kode in ("penjualan", "laba_bersih"):
                deret.append(ph["data"].get(kode))
            else:
                r = next((x for x in ph["rasio"] if x["kode"] == kode), None)
                deret.append(r["nilai"] if r else None)
        if all(v is None for v in deret):
            continue
        a, b = deret[-2], deret[-1]
        item = {"kode": kode, "nilai": deret, "arah": "—", "perubahan": None}
        if a is not None and b is not None:
            item["perubahan"] = b - a
            if kode in ("penjualan", "laba_bersih"):
                arah_baik = "T"
                if a > 0:
                    item["pertumbuhan_persen"] = bulat((b - a) / a * D100, 1)
                else:
                    item["pertumbuhan_persen"] = None
                    item["catatan"] = "periode sebelumnya %s — tidak bisa dipersenkan" % ("nol" if a == 0
                                                                                            else "rugi")
            else:
                tab = AMBANG.get(kode, {})
                arah_baik = next(iter(tab.values()))[0] if tab else None
            if b == a:
                item["arah"] = "tetap"
            elif arah_baik is None:
                item["arah"] = "naik" if b > a else "turun"
            else:
                naik = b > a
                item["arah"] = ("membaik" if naik == (arah_baik == "T") else "memburuk") + (" (naik)" if naik
                                                                                            else " (turun)")
        out.append(item)
    return out


def ringkasan(ph, jenis):
    R = ph["rasio"]
    d = ph["data"]
    kal = []
    lb, pj = d.get("laba_bersih"), d.get("penjualan")
    if lb is not None:
        mb = next((r for r in R if r["kode"] == "margin_bersih" and r["nilai"] is not None), None)
        kal.append("Pada %s, usaha %s %s%s." % (ph["label"], "UNTUNG" if lb >= 0 else "RUGI", rp(abs(lb)),
                                                 (" (%s dari penjualan)" % fmt(mb["nilai"], "%")) if mb else ""))
    n = {s: [r for r in R if r["status"] == s] for s in ("baik", "waspada", "bahaya")}
    kal.append("Dari %d rasio yang dinilai terhadap ambang usaha %s: %d baik, %d waspada, %d bahaya." %
               (sum(len(v) for v in n.values()), jenis, len(n["baik"]), len(n["waspada"]), len(n["bahaya"])))
    if n["bahaya"]:
        kal.append("Paling mendesak: " + "; ".join("%s %s" % (r["nama"].split(" (")[0],
                                                              fmt(r["nilai"], r["satuan"]) if r["nilai"] is not None
                                                              else "(%s)" % r["alasan_tidak_dihitung"])
                                                  for r in n["bahaya"][:3]) + ".")
    elif n["waspada"]:
        kal.append("Perlu diperhatikan: " + "; ".join("%s %s" % (r["nama"].split(" (")[0],
                                                                 fmt(r["nilai"], r["satuan"]))
                                                      for r in n["waspada"][:3]) + ".")
    else:
        kal.append("Semua rasio yang bisa dihitung berada di rentang wajar — pertahankan.")
    return " ".join(kal)


def analisis(periode_mentah, jenis="umum", nama_usaha=None, cfg=None, catatan=None):
    cfg = cfg or {}
    catatan = list(catatan or [])
    if jenis not in JENIS:
        raise Galat("Jenis usaha '%s' tidak dikenal. Pilih: %s." % (jenis, ", ".join(JENIS)))
    periode = [normalisasi_periode(p, catatan) for p in periode_mentah]
    periode = [p for p in periode if any(p.get(k) is not None for k in POS if k not in KODE_META)]
    if not periode:
        raise Galat("Tidak ada angka laporan keuangan yang terbaca. Minimal isi penjualan, laba bersih, "
                    "aset/utang/modal (lihat templates/isian-rasio.csv).")
    if len(periode) > 1 and all(p.get("_tanggal_akhir") for p in periode):
        periode.sort(key=lambda p: p["_tanggal_akhir"])
    hasil_periode = []
    for i, p in enumerate(periode):
        if i > 0:  # saldo akhir periode sebelumnya = saldo awal periode ini (untuk rata-rata)
            prev = periode[i - 1]
            for k_awal, k in (("persediaan_awal", "persediaan"), ("piutang_awal", "piutang"),
                              ("total_aset_awal", "total_aset"), ("modal_awal", "modal")):
                if p.get(k_awal) is None and prev.get(k) is not None and k not in prev["mustahil"]:
                    p[k_awal] = prev[k]
        lengkapi(p, cfg)
        R = hitung_periode(p, jenis)
        data = {k: p.get(k) for k in POS if p.get(k) is not None}
        hasil_periode.append({"label": p["label"], "data": data, "rasio": R, "asumsi": p["asumsi"],
                              "peringatan": p["peringatan"], "selisih_neraca": p.get("selisih_neraca")})
    akhir = hasil_periode[-1]
    p_akhir = periode[-1]
    akhir["kesiapan_kredit"] = kesiapan_kredit(p_akhir, akhir["rasio"])
    masalah = urut_masalah(akhir["rasio"])
    saran = []
    lb_akhir, md_akhir = p_akhir.get("laba_bersih"), p_akhir.get("modal")
    lewati = set()
    if lb_akhir is not None and lb_akhir < 0:
        saran.append({"rasio": "Usaha rugi", "status": "bahaya", "saran": SARAN_KHUSUS["rugi"]})
        lewati.update({"margin_bersih", "roa", "roe"})
    if md_akhir is not None and md_akhir <= 0:
        saran.append({"rasio": "Modal habis/negatif", "status": "bahaya", "saran": SARAN_KHUSUS["modal_negatif"]})
        lewati.update({"roe", "der", "dar"})
    saran += [{"rasio": r["nama"], "status": r["status"], "saran": SARAN[r["kode"]]} for r in masalah
              if r["kode"] not in lewati]
    sisa = len(saran) - 5
    saran = saran[:5]
    if sisa > 0:
        saran.append({"rasio": "Lainnya", "status": "info", "saran": "%d masalah lain ada di tabel (status 🟡/🔴). "
                      "Kerjakan 3 saran teratas dulu, lalu hitung ulang bulan depan." % sisa})
    if not saran:
        saran = [{"rasio": "—", "status": "baik", "saran": "Pertahankan: hitung ulang rasio ini tiap bulan/kuartal "
                  "dan bandingkan trennya; sisihkan sebagian laba sebagai dana cadangan."}]
    status_data = "SEMENTARA" if any(ph["peringatan"] for ph in hasil_periode) else "LENGKAP"
    return {
        "versi_script": VERSI, "nama_usaha": nama_usaha or "[Nama Usaha]",
        "jenis_usaha": jenis, "jenis_usaha_teks": JENIS[jenis], "status_data": status_data,
        "periode": hasil_periode, "tren": tren(hasil_periode), "saran": saran,
        "ringkasan_awam": ringkasan(akhir, jenis), "catatan_input": catatan,
        "disclaimer": "Analisis angka untuk membantu pemilik usaha memahami kondisi keuangan. Bukan nasihat "
                      "investasi, bukan penilaian kredit, bukan laporan audit. Ambang wajar adalah pedoman praktis "
                      "(lihat references/ambang-wajar.md), bukan standar resmi OJK/bank. Untuk keputusan besar, "
                      "konsultasikan dengan akuntan atau pendamping UMKM.",
    }


# ---------------------------------------------------------------- tampilan
IKON = {"baik": "🟢 Baik", "waspada": "🟡 Waspada", "bahaya": "🔴 Bahaya", "info": "⚪ Info",
        "tidak_dihitung": "— Tidak dihitung"}


def teks(h):
    o = []
    akhir = h["periode"][-1]
    o.append("# Analisis Rasio Keuangan — %s" % h["nama_usaha"])
    o.append("Jenis usaha: %s · Periode dianalisis: %s · Status data: **%s**" %
             (h["jenis_usaha_teks"], ", ".join(p["label"] for p in h["periode"]), h["status_data"]))
    o.append("")
    o.append("## Ringkasan untuk pemilik")
    o.append(h["ringkasan_awam"])
    o.append("")
    for kel, judul in KELOMPOK:
        baris = [r for r in akhir["rasio"] if r["kelompok"] == kel]
        if not baris:
            continue
        o.append("## %s (%s)" % (judul, akhir["label"]))
        o.append("| Rasio | Nilai | Rumus | Wajar untuk jenis usaha ini | Status | Artinya |")
        o.append("|---|---|---|---|---|---|")
        for r in baris:
            arti = r["tafsiran"] if r["nilai"] is not None else ("Tidak dihitung: " + (r["alasan_tidak_dihitung"]
                                                                                       or "-"))
            o.append("| %s | %s | %s | %s | %s | %s |" % (r["nama"], fmt(r["nilai"], r["satuan"]), r["rumus"],
                                                         r["ambang"] or "—", IKON.get(r["status"], r["status"]),
                                                         arti))
        o.append("")
    if h["tren"]:
        o.append("## Tren antarperiode")
        labels = [p["label"] for p in h["periode"]]
        o.append("| Pos / rasio | " + " | ".join(labels) + " | Perubahan terakhir |")
        o.append("|---|" + "---|" * len(labels) + "---|")
        for t in h["tren"]:
            if t["kode"] in POS:
                nama, sat = POS[t["kode"]][0], "Rp"
            else:
                nama, _, sat = NAMA_RASIO[t["kode"]]
            ubah = t["arah"]
            if t.get("pertumbuhan_persen") is not None:
                ubah += " %s%s" % ("+" if t["pertumbuhan_persen"] >= 0 else "", angka_id(t["pertumbuhan_persen"], 1)
                                   + "%")
            elif t.get("catatan"):
                ubah += " (%s)" % t["catatan"]
            o.append("| %s | %s | %s |" % (nama, " | ".join(fmt(v, sat) for v in t["nilai"]), ubah))
        o.append("")
    k = akhir["kesiapan_kredit"]
    o.append("## Kesiapan pengajuan KUR/kredit (dari sisi angka)")
    o.append("**%s**" % k["kesimpulan"])
    for c in k["cek"]:
        o.append("- %s %s" % (c["status"], c["teks"]))
    if k["laba_bersih_per_bulan"] is not None:
        o.append("- Laba bersih rata-rata per bulan: %s." % rp(k["laba_bersih_per_bulan"]))
    if k["cicilan_bulanan"] is None:
        o.append("- Cicilan belum diisi. Untuk cek kemampuan bayar, sebutkan total cicilan per bulan (lama + "
                 "rencana) → --cicilan-bulanan.")
    o.append("_%s_" % k["catatan"])
    o.append("")
    o.append("## Saran tindakan (urut prioritas)")
    for i, s in enumerate(h["saran"], 1):
        o.append("%d. **%s** — %s" % (i, s["rasio"], s["saran"]))
    o.append("")
    perlu = [w for p in h["periode"] for w in (["[%s] %s" % (p["label"], x) for x in p["peringatan"]])]
    perlu += h["catatan_input"]
    if perlu:
        o.append("## Perlu dicek")
        o.extend("- " + x for x in perlu)
        o.append("")
    asumsi = [("[%s] %s" % (p["label"], x)) for p in h["periode"] for x in p["asumsi"]]
    o.append("## Asumsi yang dipakai")
    o.extend("- " + x for x in (asumsi or ["Tidak ada — semua angka diisi pengguna."]))
    o.append("- Ambang 'wajar' = pedoman praktis untuk jenis usaha %s (references/ambang-wajar.md)." % h["jenis_usaha"])
    o.append("")
    o.append("_Disclaimer: %s_" % h["disclaimer"])
    return "\n".join(o)


# ---------------------------------------------------------------- CLI
def tebak_jenis(teks):
    if not teks:
        return "umum"
    s = teks.strip().lower()
    for j, alias in ALIAS_JENIS.items():
        if s in alias:
            return j
    for j, alias in ALIAS_JENIS.items():
        if any(a in s for a in alias):
            return j
    raise Galat("Jenis usaha '%s' tidak dikenal. Pilih: dagang, jasa, manufaktur, atau umum." % teks)


def main(argv=None):
    ap = argparse.ArgumentParser(description="Analisis rasio keuangan UMKM (Decimal, format Rupiah Indonesia).")
    ap.add_argument("file", nargs="*", help="CSV/tabel Markdown/JSON, atau output laporan_emkm.py --format json")
    ap.add_argument("--jenis", default=None, help="dagang | jasa | manufaktur | umum (alias: warung, laundry, "
                                                  "katering, ...)")
    ap.add_argument("--nama-usaha")
    ap.add_argument("--label", help="Nama periode untuk input lewat opsi (mis. '2025')")
    ap.add_argument("--format", choices=["teks", "json"], default="teks")
    ap.add_argument("--bagian-lancar-utang-bank", help="Untuk input EMKM: pokok utang bank yang jatuh tempo "
                                                       "≤ 12 bulan")
    for k in POS:
        ap.add_argument("--" + k.replace("_", "-"), dest="pos_" + k, help=POS[k][0])
    argv = list(sys.argv[1:] if argv is None else argv)
    for i in range(len(argv) - 1):  # "--modal -4jt" → "--modal=-4jt" (angka negatif/dalam kurung)
        if argv[i] and argv[i + 1] and argv[i].startswith("--") and "=" not in argv[i] and re.match(r"^[-−]\s*(rp\.?\s*)?\d", argv[i + 1], re.I):
            argv[i], argv[i + 1] = argv[i] + "=" + argv[i + 1], None
    a = ap.parse_args([x for x in argv if x is not None])
    try:
        periode, catatan, meta = [], [], {}
        for f in a.file:
            r = baca_file(f)
            periode.extend(r[0])
            catatan.extend(r[1])
            if len(r) > 2:
                meta.update(r[2])
        opsi = {k: getattr(a, "pos_" + k) for k in POS if getattr(a, "pos_" + k) is not None}
        if opsi:
            if periode:
                periode[-1].update(opsi)  # opsi melengkapi/menimpa periode terakhir
            else:
                periode = [dict(opsi, label=a.label or "periode ini")]
        if not periode:
            raise Galat("Belum ada data. Beri file (CSV/JSON) atau angka lewat opsi, mis. --penjualan 480jt "
                        "--laba-bersih 24jt --kas 12jt ... (lihat --help).")
        jenis = tebak_jenis(a.jenis or meta.get("jenis_usaha") or meta.get("jenis"))
        cfg = {}
        if a.bagian_lancar_utang_bank is not None:
            v = parse_angka(a.bagian_lancar_utang_bank)
            if v is None or v < 0:
                raise Galat("--bagian-lancar-utang-bank tidak terbaca: %s" % a.bagian_lancar_utang_bank)
            cfg["bagian_lancar_utang_bank"] = v
        h = analisis(periode, jenis, a.nama_usaha or meta.get("nama_usaha"), cfg, catatan)
    except Galat as e:
        if a.format == "json":
            sys.stderr.write(json.dumps({"error": str(e)}, ensure_ascii=False) + "\n")
        else:
            sys.stderr.write("GALAT: %s\n" % e)
        return 2
    if a.format == "json":
        print(json.dumps(h, ensure_ascii=False, indent=2, default=ke_json))
    else:
        print(teks(h))
    return 0


if __name__ == "__main__":
    sys.exit(main())
