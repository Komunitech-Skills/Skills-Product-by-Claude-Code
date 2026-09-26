#!/usr/bin/env python3
"""resi-picking (Komunitech) - daftar ambil barang & urutan resi dari file ekspor pesanan marketplace.

Alat SEKALI JALAN, tanpa database/status tersimpan (beda dengan skill `buku-stok`): baca satu file
ekspor pesanan Shopee / Tokopedia / TikTok Shop (CSV, atau file XLSX yang sudah disimpan ulang sebagai
CSV dari Excel/Google Sheets), lalu hasilkan:
  1. Daftar ambil barang per SKU/varian (diurutkan per rak bila diberi file lokasi opsional).
  2. Urutan kemas/tempel resi, dikelompokkan per kurir.
Hasil ditulis sebagai file Markdown (siap cetak/tempel) di sebelah file pesanan, dan ringkasannya
dicetak ke layar. Hanya library standar Python 3.8+. TIDAK ada akses jaringan, scraping, atau login
marketplace - input murni dari file yang sudah diunduh pengguna sendiri.

Contoh:
  python3 resi.py pesanan-shopee.csv
  python3 resi.py pesanan.csv --lokasi lokasi-rak.csv --stok stok-buku-stok.csv --html --csv
  python3 resi.py pesanan.csv --kolom-no-pesanan "Order ID" --kolom-sku "-" --urut pesanan --json
"""
import argparse
import csv
import io
import json
import re
import sys
import unicodedata
from collections import OrderedDict
from pathlib import Path

VERSI = "1.0.2"
BATAS_UKURAN = 200 * 1024 * 1024


class Gagal(Exception):
    """Error yang pesannya aman ditampilkan ke pengguna."""

    def __init__(self, pesan, **detail):
        super().__init__(pesan)
        self.pesan = pesan
        self.detail = detail


# ---------------------------------------------------------------------------
# Util umum (angka, teks)
# ---------------------------------------------------------------------------

def norm(s):
    return re.sub(r"\s+", " ", str(s or "").replace("﻿", "")).strip().lower()


def norm_no_pesanan(t):
    t = (t or "").strip().lstrip("'").strip()
    if re.fullmatch(r"\d+\.0+", t):
        t = t.split(".")[0]
    return t


def _grup_ribuan_valid(bagian_bulat, pemisah):
    grup = bagian_bulat.split(pemisah)
    return 1 <= len(grup[0]) <= 3 and all(len(g) == 3 for g in grup[1:])


def parse_angka(teks):
    """Angka format Indonesia/Inggris -> float, atau None bila kosong/tidak valid/meragukan.

    Diterima: '15000', '15.000', '15,000', '1.250.000', '12,5', '2 pcs'.
    Ditolak (None): '15.000.00', '15000.500', notasi ilmiah '1.5E+06'.
    """
    if teks is None:
        return None
    if isinstance(teks, (int, float)):
        return float(teks)
    s = str(teks).strip().lower()
    if not s:
        return None
    if re.search(r"\d\s*e\s*[+-]?\s*\d", s):
        return None
    s = re.sub(r"[^\d,.\-]", "", s).strip(".,")
    if not s or s == "-":
        return None
    negatif = s.startswith("-")
    s = s.lstrip("-")
    if "-" in s:
        return None
    if "," in s and "." in s:
        desimal = "," if s.rfind(",") > s.rfind(".") else "."
        ribuan = "." if desimal == "," else ","
        bulat, _, pecahan = s.rpartition(desimal)
        if ribuan in pecahan or not _grup_ribuan_valid(bulat, ribuan):
            return None
        s = bulat.replace(ribuan, "") + "." + pecahan
    elif "," in s or "." in s:
        pemisah = "," if "," in s else "."
        bagian = s.split(pemisah)
        if len(bagian) == 2 and len(bagian[1]) != 3:
            s = bagian[0] + "." + bagian[1]
        elif _grup_ribuan_valid(s, pemisah):
            s = s.replace(pemisah, "")
        else:
            return None
    try:
        nilai = float(s)
    except ValueError:
        return None
    return -nilai if negatif else nilai


def fq(q):
    """Format jumlah: 12 / 1,5 (desimal pakai koma, jarang dipakai untuk qty pesanan)."""
    q = round(float(q) + 0.0, 3)
    if q == int(q):
        return str(int(q))
    return ("%.3f" % q).rstrip("0").rstrip(".").replace(".", ",")


def sel(r, idx):
    if idx is None or idx >= len(r):
        return ""
    return (r[idx] or "").strip()


# ---------------------------------------------------------------------------
# Membaca file tabel (CSV saja - lintas OS, tanpa dependensi luar)
# ---------------------------------------------------------------------------

def baca_tabel(path, label="file"):
    """Kembalikan (baris [list of list str], encoding). CSV dengan pemisah , ; tab atau |."""
    p = Path(path).expanduser()
    if not p.is_file():
        raise Gagal("%s '%s' tidak ditemukan." % (label.capitalize(), path))
    if p.stat().st_size > BATAS_UKURAN:
        raise Gagal("%s terlalu besar (> 200 MB)." % label.capitalize())
    if p.stat().st_size == 0:
        raise Gagal("%s '%s' kosong." % (label.capitalize(), p.name))
    if p.suffix.lower() in (".xlsx", ".xlsm", ".xls"):
        raise Gagal(
            "%s '%s' adalah file Excel (%s), belum bisa dibaca langsung. Di Excel/Google Sheets, "
            "pilih File > Save As / Simpan sebagai > CSV, lalu pakai file CSV itu." % (label.capitalize(), p.name, p.suffix))
    mentah = p.read_bytes()
    if mentah[:2] == b"PK":
        raise Gagal(
            "%s '%s' sebenarnya file Excel (.xlsx) walau namanya .csv. Buka di Excel/Google Sheets, "
            "lalu simpan ulang sebagai CSV asli." % (label.capitalize(), p.name))
    if b"\x00" in mentah[:4096]:
        raise Gagal("%s '%s' tampaknya bukan file teks/CSV (berisi data biner)." % (label.capitalize(), p.name))
    teks = None
    enc_dipakai = None
    for enc in ("utf-8-sig", "cp1252", "latin-1"):
        try:
            teks = mentah.decode(enc)
            enc_dipakai = enc
            break
        except UnicodeDecodeError:
            continue
    if teks is None:
        raise Gagal("%s '%s' tidak bisa dibaca sebagai teks." % (label.capitalize(), p.name))
    contoh = teks[:8192]
    try:
        dialek = csv.Sniffer().sniff(contoh, delimiters=",;\t|")
    except csv.Error:
        jml = {d: contoh.count(d) for d in ",;\t|"}
        pemisah = max(jml, key=jml.get) if any(jml.values()) else ","

        class dialek(csv.excel):
            delimiter = pemisah
    try:
        baris = [list(r) for r in csv.reader(io.StringIO(teks, newline=""), dialect=dialek)]
    except csv.Error as e:
        raise Gagal("%s '%s' rusak dan tidak bisa dibaca (%s). Buka di Excel lalu simpan ulang sebagai CSV." % (
            label.capitalize(), p.name, e))
    return baris, enc_dipakai


# ---------------------------------------------------------------------------
# Deteksi kolom fleksibel
# ---------------------------------------------------------------------------

# CATATAN JUJUR - PERLU REVIEW: kata kunci di bawah disusun dari nama kolom umum yang beredar di
# panduan/forum seller, dari skill `buku-stok`, dan dari pengecekan langsung ke halaman bantuan
# resmi (lihat `references/sumber-kolom-marketplace.md` untuk URL + tanggal cek). Entri yang
# BELUM dipastikan lewat halaman resmi (mayoritas Shopee/Tokopedia/Lazada/Blibli) ditandai
# "best-effort" di file referensi tsb - anggap sebagai dugaan masuk akal, bukan spesifikasi resmi.
# Karena itu, langkah kerja skill ini SELALU menunjukkan pemetaan kolom yang terdeteksi ke
# pengguna untuk dicek dulu sebelum daftar dibuat, dan pesan error selalu menyertakan daftar
# kolom yang ada di file + flag --kolom-... yang persis untuk melengkapi/membetulkannya.
SINONIM_PESANAN = OrderedDict([
    ("no_pesanan", ["no. pesanan", "no pesanan", "nomor pesanan", "order id", "order number",
                     "nomor invoice", "invoice", "invoice number", "no. invoice", "no invoice",
                     "order/adjustment id", "order adjustment id"]),
    ("sku", ["nomor referensi sku", "seller sku", "sku penjual", "nomor sku", "kode sku",
             "sku induk", "sku id", "sku reference no", "sku"]),
    ("nama", ["nama produk", "product name", "nama barang", "item name", "nama item"]),
    ("varian", ["nama variasi", "variation", "varian"]),
    ("qty", ["jumlah produk dibeli", "jumlah", "quantity", "qty"]),
    ("kurir", ["opsi pengiriman", "shipping provider name", "shipping provider", "nama penyedia pengiriman",
               "jasa kirim", "ekspedisi", "nama kurir", "kurir pengiriman", "logistik", "kurir"]),
    ("resi", ["no. resi", "nomor resi", "tracking id", "tracking number", "id pelacakan",
              "kode booking", "awb", "no resi", "nomor awb", "no. awb"]),
    ("catatan", ["catatan dari pembeli", "buyer note", "buyer message", "buyer remark",
                 "pesan pembeli", "catatan pembeli", "catatan"]),
    ("status", ["status pesanan", "order status", "order substatus", "substatus",
                "status terakhir", "status"]),
])

LABEL_FIELD = {
    "no_pesanan": "No. pesanan", "sku": "SKU", "nama": "Nama produk", "varian": "Variasi",
    "qty": "Jumlah", "kurir": "Kurir", "resi": "No. resi", "catatan": "Catatan pembeli",
    "status": "Status pesanan",
}

SINONIM_LOKASI = OrderedDict([
    ("sku", SINONIM_PESANAN["sku"]),
    ("lokasi", ["lokasi rak", "nomor rak", "kode rak", "lokasi", "rak", "location", "bin", "gudang"]),
])

SINONIM_STOK = OrderedDict([
    ("sku", SINONIM_PESANAN["sku"]),
    ("stok", ["stok saat ini", "sisa stok", "quantity", "qty", "stock", "stok"]),
    ("lokasi", SINONIM_LOKASI["lokasi"]),
    ("nama", ["nama produk", "nama"]),
])


def _token(s):
    """Pecah teks jadi tuple token kata: huruf/angka saja, tanpa pandang huruf besar/kecil,
    diakritik (mis. 'é'->'e'), underscore, spasi, atau tanda baca ('.', '/', '-', dst)."""
    s = str(s or "").replace("﻿", "")
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    s = re.sub(r"[^A-Za-z0-9]+", " ", s).strip().lower()
    return tuple(s.split())


def _token_sublist(kecil, besar):
    """True bila `kecil` (tuple token) muncul berurutan & utuh di dalam `besar`."""
    n, m = len(kecil), len(besar)
    if n == 0 or n > m:
        return False
    return any(besar[i:i + n] == kecil for i in range(m - n + 1))


def deteksi_kolom(header, sinonim):
    """header: list nama kolom. sinonim: {field: [kata...]} (urutan dalam list = prioritas).

    Pencocokan berbasis TOKEN KATA (bukan potongan huruf), jadi tanpa pandang huruf besar/kecil,
    diakritik, underscore, spasi, atau tanda baca:
      1) cocok PERSIS (seluruh token kolom == seluruh token sinonim) selalu dicoba lebih dulu,
         untuk semua sinonim tiap field secara berurutan.
      2) kalau tidak ada yang cocok persis, cocok SEBAGIAN: token sinonim harus muncul utuh &
         berurutan di dalam token kolom - mis. sinonim "kurir" cocok dengan kolom "Nama Kurir"
         (token: nama, kurir), TAPI TIDAK cocok dengan kolom "Kurirnya" atau "Sekurir-kurirnya"
         (token utuhnya "kurirnya"/"sekurir kurirnya", bukan "kurir" persis) - jadi tidak ada
         cocokan sebagian kata (partial-word match), hanya kata utuh yang jadi salah satu token.
      Ini menggantikan aturan lama "hanya kata sinonim >= 8 huruf yang boleh cocok sebagian", yang
      membuat sinonim pendek seperti "kurir"/"invoice"/"sku" tidak pernah kedeteksi otomatis pada
      header umum seperti "Nama Kurir" atau "No. Invoice".
    Satu kolom hanya dipakai untuk satu field (field diproses sesuai urutan dict `sinonim`).
    """
    ht = [_token(h) for h in header]
    dipakai, hasil = set(), {}
    for field, kata in sinonim.items():
        kata_tok = [_token(k) for k in kata]
        pilih = None
        for kt in kata_tok:
            if not kt:
                continue
            for i, toks in enumerate(ht):
                if i not in dipakai and toks == kt:
                    pilih = i
                    break
            if pilih is not None:
                break
        if pilih is None:
            for kt in kata_tok:
                if not kt:
                    continue
                for i, toks in enumerate(ht):
                    if i not in dipakai and toks and _token_sublist(kt, toks):
                        pilih = i
                        break
                if pilih is not None:
                    break
        if pilih is not None:
            hasil[field] = pilih
            dipakai.add(pilih)
    return hasil


def kolom_ambigu(header, sinonim, kol):
    """Field yang punya LEBIH DARI SATU kolom kandidat yang cocok sinonimnya (bukan cuma kolom yang
    akhirnya dipilih `deteksi_kolom`). Contoh: file punya kolom "SKU Induk" DAN "Nomor SKU" -
    keduanya cocok sinonim SKU, tapi hanya satu yang otomatis dipakai (urutan sinonim & posisi
    kolom), bukan menebak mana yang benar-benar dimaksud. Dipakai di `proses()` untuk memberi
    peringatan eksplisit ke pengguna + saran `--kolom-...`, hanya untuk field yang TIDAK dipetakan
    manual lewat override (yang sudah pasti/disengaja)."""
    ht = [_token(h) for h in header]
    ambigu = {}
    for field, kata in sinonim.items():
        if field not in kol:
            continue
        kata_tok = [t for t in (_token(k) for k in kata) if t]
        cocok = [i for i, toks in enumerate(ht) if toks and (
            toks in kata_tok or any(_token_sublist(kt, toks) for kt in kata_tok))]
        if len(cocok) > 1:
            ambigu[field] = [header[i] for i in cocok]
    return ambigu


def cari_header(baris, sinonim, minimal=2, maks_scan=15):
    """Cari baris judul kolom: baris (dari `maks_scan` pertama) dengan paling banyak kolom dikenali."""
    terbaik, skor_terbaik = None, 0
    for i, r in enumerate(baris[:maks_scan]):
        skor = len(deteksi_kolom(r, sinonim))
        if skor > skor_terbaik:
            terbaik, skor_terbaik = i, skor
    if terbaik is None or skor_terbaik < minimal:
        return None
    return terbaik


# ---------------------------------------------------------------------------
# Status pesanan: batal / retur / belum bayar dikecualikan dari picking
# ---------------------------------------------------------------------------

KATA_BATAL = ["batal", "dibatalkan", "cancel", "gagal", "failed", "expired", "kedaluwarsa"]
KATA_RETUR = ["retur", "return", "refund", "pengembalian", "dikembalikan"]
KATA_BELUM_BAYAR = ["belum bayar", "belum dibayar", "unpaid", "menunggu pembayaran"]
KATA_KECUALI = ["ditolak", "rejected"]  # mis. "Pengembalian Ditolak" -> pesanan tetap sah


def kategori_status(teks, abaikan=None):
    t = norm(teks)
    if not t:
        return "tanpa_status"
    if any(k in t for k in KATA_KECUALI):
        return "aktif"
    if abaikan is not None:
        return "dikecualikan" if any(k in t for k in abaikan) else "aktif"
    if any(k in t for k in KATA_BATAL):
        return "batal"
    if any(k in t for k in KATA_RETUR):
        return "retur"
    if any(k in t for k in KATA_BELUM_BAYAR):
        return "belum_bayar"
    return "aktif"


KATEGORI_DIKECUALIKAN = {"batal", "retur", "belum_bayar", "dikecualikan"}
LABEL_KATEGORI = {"batal": "batal", "retur": "retur", "belum_bayar": "belum bayar",
                  "dikecualikan": "dikecualikan manual (--abaikan-status)"}


# ---------------------------------------------------------------------------
# File pendukung opsional: lokasi rak & stok (cth. ekspor 'buku-stok laporan stok --csv')
# ---------------------------------------------------------------------------

def baca_pendukung(path, sinonim, label):
    baris, _ = baca_tabel(path, label=label)
    hi = cari_header(baris, sinonim, minimal=1)
    if hi is None:
        raise Gagal("Kolom di file %s ('%s') tidak dikenali. Pastikan ada kolom SKU." % (label, Path(path).name),
                    kolom_ada=(baris[0] if baris else []))
    header = baris[hi]
    kol = deteksi_kolom(header, sinonim)
    if "sku" not in kol:
        raise Gagal("Kolom SKU tidak ditemukan di file %s ('%s')." % (label, Path(path).name), kolom_ada=header)
    hasil = {}
    for r in baris[hi + 1:]:
        if not any((c or "").strip() for c in r):
            continue
        sku = sel(r, kol["sku"])
        if not sku:
            continue
        data = {f: sel(r, i) for f, i in kol.items() if f != "sku"}
        hasil[norm(sku)] = data
    return hasil, {f: header[i] for f, i in kol.items()}


# ---------------------------------------------------------------------------
# Proses utama
# ---------------------------------------------------------------------------

def proses(args):
    baris, encoding = baca_tabel(args.file, label="file pesanan")
    ada_override = any(getattr(args, "kolom_" + f, None) for f in SINONIM_PESANAN)
    hi = cari_header(baris, SINONIM_PESANAN, minimal=2)
    if hi is None and ada_override:
        # Nama kolom sama sekali tidak dikenali otomatis, tapi pengguna memetakan sendiri lewat
        # --kolom-... -> anggap baris pertama sebagai judul kolom.
        hi = 0
    if hi is None:
        kolom_ada = [c for c in (baris[0] if baris else [])][:40]
        semua_flag = ", ".join('--kolom-%s "Nama Kolom"' % f.replace("_", "-") for f in SINONIM_PESANAN)
        raise Gagal("Judul kolom pesanan tidak dikenali. Pastikan ini file ekspor PESANAN marketplace "
                    "(bukan laporan lain), dan bukan hasil buka-tutup di Excel yang mengubah nomor pesanan. "
                    "Kolom yang ada di file: %s. Kalau nama kolomnya memang tidak umum, sebutkan manual "
                    "salah satu atau lebih flag berikut (isi dengan nama kolom PERSIS seperti di file): %s."
                    % (", ".join(kolom_ada) if kolom_ada else "(file tidak punya baris sama sekali)", semua_flag),
                    kolom_ada=kolom_ada)
    header = baris[hi]
    kol = deteksi_kolom(header, SINONIM_PESANAN)
    header_norm = [norm(h) for h in header]

    # Pemetaan manual (--kolom-...) mengalahkan deteksi otomatis. "-" berarti abaikan kolom itu.
    for field in SINONIM_PESANAN:
        nilai = getattr(args, "kolom_" + field, None)
        if nilai is None:
            continue
        if nilai.strip() == "-":
            kol.pop(field, None)
            continue
        if norm(nilai) not in header_norm:
            raise Gagal("Kolom '%s' (untuk %s) tidak ada di file." % (nilai, LABEL_FIELD[field]), kolom_ada=header)
        idx = header_norm.index(norm(nilai))
        for f2, i2 in list(kol.items()):
            if i2 == idx and f2 != field:
                kol.pop(f2)
        kol[field] = idx

    field_dioverride = {f for f in SINONIM_PESANAN if getattr(args, "kolom_" + f, None) is not None}
    ambigu = {f: v for f, v in kolom_ambigu(header, SINONIM_PESANAN, kol).items() if f not in field_dioverride}

    pemetaan = {LABEL_FIELD[f]: header[i] for f, i in sorted(kol.items(), key=lambda x: x[1])}
    field_hilang = [f for f in ("no_pesanan", "qty") if f not in kol]
    if "sku" not in kol and "nama" not in kol:
        field_hilang.append("sku")  # SKU ATAU Nama; sarankan --kolom-sku dulu
    if field_hilang:
        label_hilang = [("SKU atau Nama produk" if f == "sku" and "nama" not in kol else LABEL_FIELD[f])
                         for f in field_hilang]
        saran_flag = " ".join('--kolom-%s "Nama Kolom Anda"' % f.replace("_", "-") for f in field_hilang)
        pemetaan_teks = ", ".join("%s=%s" % (k, v) for k, v in pemetaan.items()) if pemetaan else "(tidak ada kolom terdeteksi otomatis)"
        raise Gagal(
            "Kolom wajib tidak ketemu: %s. Kolom yang SUDAH terdeteksi otomatis: %s. Kolom yang ada di "
            "file ini: %s. Jalankan ulang sambil menambahkan, mis.: %s (isi dengan nama kolom PERSIS "
            "seperti di file)." % (", ".join(label_hilang), pemetaan_teks, ", ".join(header), saran_flag),
            kolom_ada=header, pemetaan_terdeteksi=pemetaan)

    abaikan = None
    if args.abaikan_status:
        abaikan = [norm(x) for x in args.abaikan_status.split(",") if x.strip()]

    # 1) Baca baris -> kelompokkan per pesanan
    urut, pesanan = [], {}
    lewat = {"nomor_pesanan_rusak": [], "tanpa_nomor_pesanan": [], "jumlah_tidak_terbaca": [],
             "jumlah_nol_atau_negatif": [], "tanpa_identitas_barang": [], "baris_duplikat": [],
             "baris_ringkasan_diabaikan": []}
    dilihat_dupe = set()
    no_sebelum = None
    pola_ringkasan = re.compile(r"^(grand\s*)?(total|subtotal|jumlah\s*total|ringkasan)\b")
    for no, r in enumerate(baris[hi + 1:], start=hi + 2):
        if not any((c or "").strip() for c in r):
            continue
        nop_raw = sel(r, kol["no_pesanan"])
        nop = norm_no_pesanan(nop_raw)
        sku = sel(r, kol.get("sku"))
        nama = sel(r, kol.get("nama"))
        varian = sel(r, kol.get("varian"))
        # Baris ringkasan/total di bagian bawah ekspor (tanpa nomor pesanan sendiri) -> jangan
        # dianggap lanjutan pesanan sebelumnya.
        if not nop and (pola_ringkasan.match(norm(sku)) or pola_ringkasan.match(norm(nama))):
            lewat["baris_ringkasan_diabaikan"].append(no)
            continue
        if re.search(r"\d[.,]\d+e\+?\d+", nop.lower()):
            lewat["nomor_pesanan_rusak"].append(no)
            continue
        if not nop:
            if no_sebelum:
                nop = no_sebelum
            else:
                lewat["tanpa_nomor_pesanan"].append(no)
                continue
        q = parse_angka(sel(r, kol["qty"]))
        if q is None:
            lewat["jumlah_tidak_terbaca"].append(no)
            continue
        if q <= 0:
            lewat["jumlah_nol_atau_negatif"].append(no)
            continue
        no_sebelum = nop
        if not sku and not nama:
            lewat["tanpa_identitas_barang"].append(no)
            continue
        kunci_dupe = (nop, norm(sku), norm(nama), norm(varian), round(q, 3))
        if kunci_dupe in dilihat_dupe:
            lewat["baris_duplikat"].append(no)
            continue
        dilihat_dupe.add(kunci_dupe)

        if nop not in pesanan:
            status = sel(r, kol.get("status"))
            pesanan[nop] = {
                "no": nop,
                "status": status,
                "kategori": kategori_status(status, abaikan) if "status" in kol else "tanpa_status",
                "resi": sel(r, kol.get("resi")).lstrip("'"),
                "kurir": sel(r, kol.get("kurir")),
                "catatan": [],
                "item": [],
            }
            urut.append(nop)
        ps = pesanan[nop]
        if not ps["resi"]:
            ps["resi"] = sel(r, kol.get("resi")).lstrip("'")
        if not ps["kurir"]:
            ps["kurir"] = sel(r, kol.get("kurir"))
        catatan = sel(r, kol.get("catatan"))
        if catatan and catatan not in ps["catatan"]:
            ps["catatan"].append(catatan)
        ps["item"].append({"baris": no, "sku": sku, "nama": nama, "varian": varian, "qty": q})

    if not pesanan:
        raise Gagal("Tidak ada baris pesanan yang bisa dibaca dari file. Cek kolom Jumlah/No. pesanan.",
                    pemetaan=pemetaan, baris_dilewati=lewat)

    dilewati_status = {}
    aktif = []
    for nop in urut:
        ps = pesanan[nop]
        if ps["kategori"] in KATEGORI_DIKECUALIKAN:
            label = LABEL_KATEGORI.get(ps["kategori"], ps["kategori"])
            dilewati_status[label] = dilewati_status.get(label, 0) + 1
            continue
        aktif.append(ps)

    if not aktif:
        raise Gagal("Semua %d pesanan di file ini berstatus batal/retur/belum bayar - tidak ada yang perlu "
                    "diambil/dikemas. Jika ini keliru, cek kolom status atau pakai --abaikan-status." % len(pesanan),
                    dilewati_status=dilewati_status)

    # 2) File pendukung opsional
    lokasi_map, stok_map = {}, {}
    pemetaan_lokasi = pemetaan_stok = None
    if args.lokasi:
        lokasi_map, pemetaan_lokasi = baca_pendukung(args.lokasi, SINONIM_LOKASI, "lokasi")
    if args.stok:
        stok_map, pemetaan_stok = baca_pendukung(args.stok, SINONIM_STOK, "stok")

    def cari_lokasi(sku_norm):
        if sku_norm in lokasi_map:
            return (lokasi_map[sku_norm].get("lokasi") or "").strip()
        if sku_norm in stok_map:
            return (stok_map[sku_norm].get("lokasi") or "").strip()
        return ""

    # 3) Daftar ambil barang (agregat per SKU/varian)
    ambil = OrderedDict()
    for ps in aktif:
        for it in ps["item"]:
            sku_norm = norm(it["sku"]) if it["sku"] else ""
            kunci = sku_norm if sku_norm else "nama:" + norm(it["nama"]) + "|" + norm(it["varian"])
            a = ambil.setdefault(kunci, {
                "sku": it["sku"] or "(tanpa SKU)",
                "nama": it["nama"] or "",
                "varian": it["varian"] or "",
                "qty": 0.0,
                "pesanan": set(),
                "lokasi": cari_lokasi(sku_norm) if sku_norm else "",
                "sku_dikenal": (not args.stok) or (sku_norm in stok_map) if sku_norm else None,
                "stok_tercatat": stok_map.get(sku_norm, {}).get("stok") if sku_norm else None,
            })
            a["qty"] += it["qty"]
            a["pesanan"].add(ps["no"])

    peringatan = []
    sku_tak_dikenal = sorted({a["sku"] for a in ambil.values() if a["sku_dikenal"] is False})
    if sku_tak_dikenal:
        peringatan.append("SKU tidak ada di file stok (%s): %s. Kemungkinan salah ketik atau produk baru."
                          % (Path(args.stok).name, ", ".join(sku_tak_dikenal)))
    if args.stok:
        for a in ambil.values():
            stok_angka = parse_angka(a.get("stok_tercatat")) if a.get("stok_tercatat") not in (None, "") else None
            a["stok_angka"] = stok_angka
            if stok_angka is not None and stok_angka < a["qty"]:
                peringatan.append("Stok '%s' kemungkinan kurang: butuh %s, stok tercatat %s."
                                  % (a["sku"], fq(a["qty"]), fq(stok_angka)))
    else:
        for a in ambil.values():
            a["stok_angka"] = None

    for label_lewat, nomor_baris in lewat.items():
        if nomor_baris:
            peringatan.append("%d baris '%s' dilewati (baris %s%s)." % (
                len(nomor_baris), label_lewat.replace("_", " "),
                ", ".join(str(n) for n in nomor_baris[:10]), ", ..." if len(nomor_baris) > 10 else ""))

    resi_kosong = [ps["no"] for ps in aktif if not ps["resi"]]
    if resi_kosong:
        peringatan.append("%d pesanan tanpa nomor resi (lihat kelompok '(Resi belum ada)' di urutan-resi)."
                          % len(resi_kosong))
    if dilewati_status:
        peringatan.append("Pesanan dilewati karena status: " +
                          ", ".join("%s (%d)" % (k, v) for k, v in dilewati_status.items()) +
                          ". Tidak masuk daftar ambil/urutan resi.")
    if "status" not in kol:
        peringatan.append("Kolom status tidak terdeteksi di file ini - SEMUA baris dianggap perlu dikemas. "
                          "Sebaiknya ekspor pesanan berstatus 'Perlu Dikirim/Siap Dikirim' saja dari Seller Center.")
    for field, kandidat in ambigu.items():
        peringatan.append(
            "Kolom untuk %s ambigu: ada %d kolom mirip di file (%s), yang dipakai: '%s'. Kalau salah, "
            "jalankan ulang dengan --kolom-%s \"Nama Kolom Persis\"." % (
                LABEL_FIELD[field], len(kandidat), ", ".join("'%s'" % k for k in kandidat),
                header[kol[field]], field.replace("_", "-")))

    daftar_ambil = sorted(
        ambil.values(),
        key=lambda a: (a["lokasi"] == "", a["lokasi"], a["sku"], a["nama"], a["varian"]))

    # 4) Urutan kemas/resi, dikelompokkan per kurir
    kelompok = OrderedDict()
    for ps in aktif:
        kurir = ps["kurir"] or "(tanpa kurir)"
        kelompok.setdefault(kurir, []).append(ps)

    def kunci_urut_pesanan(ps):
        if args.urut == "pesanan":
            return (ps["no"],)
        return (ps["resi"] == "", ps["resi"], ps["no"])

    kurir_terurut = sorted(kelompok.keys(), key=lambda k: (k == "(tanpa kurir)", k))
    for k in kurir_terurut:
        kelompok[k].sort(key=kunci_urut_pesanan)

    catatan_khusus = [ps for ps in aktif if ps["catatan"]]

    total_qty = sum(a["qty"] for a in daftar_ambil)
    kurir_ringkas = OrderedDict((k, len(v)) for k, v in kelompok.items())

    return {
        "file_pesanan": str(Path(args.file).resolve()),
        "encoding": encoding,
        "pemetaan_kolom": pemetaan,
        "kolom_ambigu": {LABEL_FIELD[f]: v for f, v in ambigu.items()},
        "pemetaan_lokasi": pemetaan_lokasi,
        "pemetaan_stok": pemetaan_stok,
        "jumlah_baris_dibaca": len(baris) - hi - 1,
        "jumlah_pesanan_total": len(pesanan),
        "jumlah_pesanan_aktif": len(aktif),
        "jumlah_sku_unik": len(daftar_ambil),
        "total_barang": round(total_qty, 3),
        "kurir": kurir_ringkas,
        "jumlah_pesanan_catatan_khusus": len(catatan_khusus),
        "jumlah_resi_kosong": len(resi_kosong),
        "dilewati_status": dilewati_status,
        "baris_dilewati": {k: len(v) for k, v in lewat.items() if v},
        "peringatan": peringatan,
        "daftar_ambil": daftar_ambil,
        "kelompok_kurir": kelompok,
        "catatan_khusus": catatan_khusus,
        "urut_dipakai": args.urut,
    }


# ---------------------------------------------------------------------------
# Rendering keluaran (Markdown siap cetak + HTML sederhana opsional)
# ---------------------------------------------------------------------------

def render_daftar_ambil(hasil, sumber_nama):
    t = []
    t.append("# Daftar Ambil Barang (Picking)")
    t.append("")
    t.append("Sumber pesanan: `%s` (%d baris dibaca, encoding %s)" % (
        sumber_nama, hasil["jumlah_baris_dibaca"], hasil["encoding"]))
    if hasil["pemetaan_lokasi"]:
        t.append("Lokasi rak: dipakai (%d SKU terdaftar)" % len(hasil["daftar_ambil"]))
    if hasil["pemetaan_stok"]:
        t.append("Cek stok: dipakai (dibandingkan dengan file stok yang diberikan)")
    t.append("")
    t.append("**Total: %d pesanan aktif, %d jenis barang, %s pcs.**" % (
        hasil["jumlah_pesanan_aktif"], hasil["jumlah_sku_unik"], fq(hasil["total_barang"])))
    t.append("")
    if hasil["catatan_khusus"]:
        t.append("## Pesanan dengan catatan khusus (baca dulu sebelum packing)")
        for ps in hasil["catatan_khusus"]:
            t.append("- Pesanan #%s: %s" % (ps["no"], " / ".join('"%s"' % c for c in ps["catatan"])))
        t.append("")
    t.append("## Ambil di rak")
    lok = object()
    for a in hasil["daftar_ambil"]:
        label_lok = a["lokasi"] or "(lokasi belum diisi)"
        if label_lok != lok:
            lok = label_lok
            t.append("")
            t.append("### %s" % label_lok)
        nama = a["nama"] + (" - " + a["varian"] if a["varian"] else "") if a["nama"] else "(nama tidak ada di file)"
        flag = ""
        if a["sku_dikenal"] is False:
            flag = "  _(SKU tidak ada di file stok)_"
        elif a["stok_angka"] is not None and a["stok_angka"] < a["qty"]:
            flag = "  _(stok tercatat %s, kemungkinan kurang)_" % fq(a["stok_angka"])
        t.append("- [ ] **%s** %s x %s pcs (%d pesanan)%s" % (
            a["sku"], nama, fq(a["qty"]), len(a["pesanan"]), flag))
    if hasil["peringatan"]:
        t.append("")
        t.append("## Peringatan")
        for p in hasil["peringatan"]:
            t.append("- %s" % p)
    return "\n".join(t) + "\n"


def render_urutan_resi(hasil, sumber_nama):
    t = []
    t.append("# Urutan Kemas / Tempel Resi")
    t.append("")
    t.append("Sumber pesanan: `%s`. Dikelompokkan per kurir, diurutkan per %s dalam tiap kurir." % (
        sumber_nama, "nomor resi" if hasil["urut_dipakai"] == "resi" else "nomor pesanan"))
    t.append("")
    t.append("**Total: %d pesanan, %d kurir.**" % (hasil["jumlah_pesanan_aktif"], len(hasil["kelompok_kurir"])))
    t.append("")
    for kurir, daftar in hasil["kelompok_kurir"].items():
        t.append("## %s (%d pesanan)" % (kurir, len(daftar)))
        for n, ps in enumerate(daftar, start=1):
            isi = "; ".join("%s x%s" % ((it["sku"] or it["nama"] or "?"), fq(it["qty"])) for it in ps["item"])
            resi = ps["resi"] or "(KOSONG - cek Seller Center)"
            baris = "%d. [ ] Pesanan #%s | Resi %s | %s" % (n, ps["no"], resi, isi)
            if ps["catatan"]:
                baris += " | CATATAN: %s" % (" / ".join('"%s"' % c for c in ps["catatan"]))
            t.append(baris)
        t.append("")
    if hasil["peringatan"]:
        t.append("## Peringatan")
        for p in hasil["peringatan"]:
            t.append("- %s" % p)
    return "\n".join(t) + "\n"


def html_sederhana(judul, markdown_teks):
    import html as _html
    isi = _html.escape(markdown_teks)
    return ("<!doctype html>\n<html lang=\"id\"><head><meta charset=\"utf-8\">"
            "<title>%s</title><style>"
            "body{font-family:Arial,Helvetica,sans-serif;margin:24px;color:#111}"
            "pre{white-space:pre-wrap;font-family:'Courier New',monospace;font-size:13px;line-height:1.5}"
            "@media print{body{margin:8px}}"
            "</style></head><body><pre>%s</pre></body></html>\n") % (_html.escape(judul), isi)


def tulis_csv_ambil(path, daftar_ambil, pemisah):
    with open(path, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f, delimiter=pemisah)
        w.writerow(["lokasi", "sku", "nama", "varian", "qty", "jumlah_pesanan"])
        for a in daftar_ambil:
            w.writerow([a["lokasi"], a["sku"], a["nama"], a["varian"], fq(a["qty"]), len(a["pesanan"])])


def tulis_csv_urutan(path, kelompok_kurir, pemisah):
    with open(path, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f, delimiter=pemisah)
        w.writerow(["urut", "kurir", "no_pesanan", "resi", "sku_dan_qty", "catatan"])
        for kurir, daftar in kelompok_kurir.items():
            for n, ps in enumerate(daftar, start=1):
                isi = "; ".join("%s x%s" % ((it["sku"] or it["nama"] or "?"), fq(it["qty"])) for it in ps["item"])
                w.writerow([n, kurir, ps["no"], ps["resi"], isi, " / ".join(ps["catatan"])])


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def buat_parser():
    p = argparse.ArgumentParser(
        prog="resi.py",
        description="resi-picking Komunitech - daftar ambil barang & urutan resi dari ekspor pesanan marketplace.")
    p.add_argument("file", help="File ekspor pesanan marketplace (CSV)")
    p.add_argument("--lokasi", help="File pemetaan SKU -> lokasi rak (CSV, kolom SKU & Lokasi)")
    p.add_argument("--stok", help="File stok untuk cross-check (CSV; bisa hasil 'buku-stok laporan stok --csv')")
    for field in SINONIM_PESANAN:
        p.add_argument("--kolom-%s" % field.replace("_", "-"),
                       help="Paksa kolom untuk %s (nama kolom persis, atau '-' untuk abaikan)" % LABEL_FIELD[field])
    p.add_argument("--abaikan-status",
                   help="Kata status yang dianggap batal/retur/belum-bayar, pisahkan koma. "
                        "MENGGANTI seluruh daftar bawaan: " + ", ".join(KATA_BATAL + KATA_RETUR + KATA_BELUM_BAYAR))
    p.add_argument("--urut", choices=["resi", "pesanan"], default="resi",
                   help="Urutan pesanan di dalam tiap kelompok kurir (default: nomor resi)")
    p.add_argument("--keluar-dir", help="Folder simpan hasil (default: folder file pesanan)")
    p.add_argument("--html", action="store_true", help="Ikut tulis versi .html (selain .md)")
    p.add_argument("--csv", action="store_true", help="Ikut tulis versi .csv (untuk Excel)")
    p.add_argument("--pemisah", default=";", help="Pemisah kolom CSV keluaran (default ';' untuk Excel Indonesia)")
    p.add_argument("--json", action="store_true", help="Cetak ringkasan sebagai JSON, bukan teks")
    return p


def main(argv=None):
    try:
        sys.stdout.reconfigure(errors="replace")
    except (AttributeError, ValueError):
        pass
    args = buat_parser().parse_args(argv)
    try:
        hasil = proses(args)
    except Gagal as e:
        out = {"ok": False, "error": e.pesan}
        out.update(e.detail)
        if args.json:
            print(json.dumps(out, ensure_ascii=False, indent=2, default=str))
        else:
            print("GAGAL: " + e.pesan, file=sys.stderr)
            for k, v in e.detail.items():
                print("  %s: %s" % (k, v), file=sys.stderr)
        return 1

    sumber = Path(args.file).name
    md_ambil = render_daftar_ambil(hasil, sumber)
    md_urutan = render_urutan_resi(hasil, sumber)

    keluar_dir = Path(args.keluar_dir).expanduser() if args.keluar_dir else Path(args.file).resolve().parent
    keluar_dir.mkdir(parents=True, exist_ok=True)
    file_keluaran = {}

    path_ambil_md = keluar_dir / "daftar-ambil.md"
    path_urutan_md = keluar_dir / "urutan-resi.md"
    path_ambil_md.write_text(md_ambil, encoding="utf-8")
    path_urutan_md.write_text(md_urutan, encoding="utf-8")
    file_keluaran["daftar_ambil_md"] = str(path_ambil_md)
    file_keluaran["urutan_resi_md"] = str(path_urutan_md)

    if args.html:
        path_ambil_html = keluar_dir / "daftar-ambil.html"
        path_urutan_html = keluar_dir / "urutan-resi.html"
        path_ambil_html.write_text(html_sederhana("Daftar Ambil Barang", md_ambil), encoding="utf-8")
        path_urutan_html.write_text(html_sederhana("Urutan Kemas / Tempel Resi", md_urutan), encoding="utf-8")
        file_keluaran["daftar_ambil_html"] = str(path_ambil_html)
        file_keluaran["urutan_resi_html"] = str(path_urutan_html)

    if args.csv:
        path_ambil_csv = keluar_dir / "daftar-ambil.csv"
        path_urutan_csv = keluar_dir / "urutan-resi.csv"
        tulis_csv_ambil(path_ambil_csv, hasil["daftar_ambil"], args.pemisah)
        tulis_csv_urutan(path_urutan_csv, hasil["kelompok_kurir"], args.pemisah)
        file_keluaran["daftar_ambil_csv"] = str(path_ambil_csv)
        file_keluaran["urutan_resi_csv"] = str(path_urutan_csv)

    if args.json:
        data = {"ok": True, "file_keluaran": file_keluaran}
        for k, v in hasil.items():
            if k in ("daftar_ambil", "kelompok_kurir", "catatan_khusus"):
                continue
            data[k] = v
        data["daftar_ambil"] = [
            {"sku": a["sku"], "nama": a["nama"], "varian": a["varian"], "lokasi": a["lokasi"],
             "qty": round(a["qty"], 3), "jumlah_pesanan": len(a["pesanan"]),
             "sku_dikenal": a["sku_dikenal"], "stok_tercatat": a["stok_angka"]}
            for a in hasil["daftar_ambil"]
        ]
        print(json.dumps(data, ensure_ascii=False, indent=2, default=str))
    else:
        print(md_ambil)
        print("\n---\n")
        print(md_urutan)
        print("File tersimpan:")
        for k, v in file_keluaran.items():
            print("  - %s: %s" % (k, v))
    return 0


if __name__ == "__main__":
    sys.exit(main())
