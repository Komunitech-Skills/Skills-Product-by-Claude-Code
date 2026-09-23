#!/usr/bin/env python3
"""Rekonsiliasi mutasi rekening bank dengan catatan penjualan / invoice.

Dua perintah:
  deteksi   : tebak baris judul & kolom file mutasi bank (dan catatan) untuk DIKONFIRMASI pengguna.
  cocokkan  : cocokkan transaksi, hasilkan laporan: cocok persis, cocok parsial,
              tidak ditemukan di bank, tidak ditemukan di catatan, dan penjelasan selisih.

Keamanan & privasi:
  - Hanya library standar Python 3.8+, tanpa akses jaringan, hanya membaca file yang disebut.
  - Tidak menyimpan apa pun kecuali file --output-csv yang diminta.
  - Deretan angka panjang (>= 8 digit, mis. nomor rekening/kartu) di keterangan disamarkan
    menjadi ****1234 secara default (matikan dengan --tampilkan-lengkap).

Pembulatan: setiap nominal dibulatkan ke rupiah penuh terdekat (0,5 ke atas) sebelum dicocokkan
dan dijumlah, jadi sen (mis. ,00 di mutasi bank) tidak memengaruhi hasil kecuali >= 0,5.
"""
import argparse
import csv
import io
import itertools
import json
import re
import sys
from datetime import date, datetime
from decimal import ROUND_HALF_UP, Decimal, InvalidOperation

# ============================================================ util

BULAN = {
    "jan": 1, "januari": 1, "january": 1, "feb": 2, "februari": 2, "february": 2, "peb": 2,
    "mar": 3, "maret": 3, "march": 3, "apr": 4, "april": 4, "mei": 5, "may": 5,
    "jun": 6, "juni": 6, "june": 6, "jul": 7, "juli": 7, "july": 7,
    "agu": 8, "agt": 8, "agus": 8, "agustus": 8, "aug": 8, "august": 8,
    "sep": 9, "sept": 9, "september": 9, "okt": 10, "oktober": 10, "oct": 10, "october": 10,
    "nov": 11, "nop": 11, "november": 11, "des": 12, "desember": 12, "dec": 12, "december": 12,
}


def gagal(pesan, detail=None):
    data = {"error": pesan}
    if detail is not None:
        data["detail"] = detail
    print(json.dumps(data, ensure_ascii=False, indent=2), file=sys.stderr)
    sys.exit(2)


def bulat(d):
    return int(d.quantize(Decimal(1), rounding=ROUND_HALF_UP))


def rp(n):
    return ("-" if n < 0 else "") + f"Rp {abs(int(n)):,}".replace(",", ".")


def parse_angka(teks):
    """Angka format Indonesia/Inggris. Kembalikan (Decimal, tanda_dk) atau (None, None).

    tanda_dk: 'CR'/'DB' bila teks memuat akhiran CR/DB/K/D, selain itu None.
    '1,500,000.00 CR' | '1.500.000,00' | 'Rp 15.000' | '(25.000)' | '-25000' | '15.000,-'
    """
    if teks is None:
        return None, None
    s = str(teks).strip().upper().replace(" ", " ")
    if not s or s in ("-", "0-"):
        return None, None
    dk = None
    m = re.search(r"\s*\b(CR|DB|KR|DR|K|D|C)\b\.?\s*$", s)
    if m:
        dk = "CR" if m.group(1) in ("CR", "KR", "K", "C") else "DB"
        s = s[:m.start()]
    negatif = s.strip().startswith("-") or (s.strip().startswith("(") and s.strip().endswith(")"))
    s = re.sub(r"\b(RP|IDR)\b\.?", "", s)
    s = re.sub(r"[,.]\s*-\s*$", "", s)
    s = re.sub(r"[^\d,.]", "", s).strip(".,")
    if not s:
        return None, None
    if "," in s and "." in s:
        if s.rfind(",") > s.rfind("."):
            s = s.replace(".", "").replace(",", ".")
        else:
            s = s.replace(",", "")
    elif "," in s:
        b = s.split(",")
        s = s.replace(",", ".") if (len(b) == 2 and len(b[1]) != 3) else s.replace(",", "")
    elif "." in s:
        b = s.split(".")
        if len(b) > 2 or len(b[1]) == 3:
            s = s.replace(".", "")
    try:
        v = Decimal(s)
    except InvalidOperation:
        return None, None
    return (-v if negatif else v), dk


POLA_ISO = re.compile(r"^(\d{4})[-/.](\d{1,2})[-/.](\d{1,2})")
POLA_DMY = re.compile(r"^(\d{1,2})[-/.](\d{1,2})[-/.](\d{2,4})\b")
POLA_DM = re.compile(r"^(\d{1,2})[-/.](\d{1,2})$")
POLA_NAMA = re.compile(r"^(\d{1,2})[\s\-/]+([A-Za-z]+)\.?[\s\-/,]+(\d{2,4})\b")
POLA_RAPAT = re.compile(r"^(\d{4})(\d{2})(\d{2})$")


def parse_tanggal(teks, urutan="dmy", tahun_default=None):
    """Kembalikan (date|None, butuh_tahun: bool)."""
    t = (teks or "").strip().strip("'\"").strip()
    if not t or t.upper().startswith("PEND"):
        return None, False
    t = re.sub(r"^(senin|selasa|rabu|kamis|jumat|jum'at|sabtu|minggu|mon|tue|wed|thu|fri|sat|sun)[a-z]*,?\s+", "",
               t, flags=re.I)

    def buat(y, m, d):
        try:
            return date(y, m, d)
        except ValueError:
            return None

    m = POLA_ISO.match(t)
    if m:
        return buat(int(m.group(1)), int(m.group(2)), int(m.group(3))), False
    m = POLA_DMY.match(t)
    if m:
        a, b, y = int(m.group(1)), int(m.group(2)), int(m.group(3))
        y = y + 2000 if y < 100 else y
        d, bl = (a, b) if urutan == "dmy" else (b, a)
        return buat(y, bl, d), False
    m = POLA_NAMA.match(t)
    if m and m.group(2).lower() in BULAN:
        y = int(m.group(3))
        y = y + 2000 if y < 100 else y
        return buat(y, BULAN[m.group(2).lower()], int(m.group(1))), False
    m = POLA_RAPAT.match(t)
    if m:
        return buat(int(m.group(1)), int(m.group(2)), int(m.group(3))), False
    m = POLA_DM.match(t)
    if m:
        if tahun_default is None:
            return None, True
        a, b = int(m.group(1)), int(m.group(2))
        d, bl = (a, b) if urutan == "dmy" else (b, a)
        if isinstance(tahun_default, tuple):  # periode melewati pergantian tahun (awal, akhir)
            awal, akhir = tahun_default
            th = awal.year if (bl, d) >= (awal.month, awal.day) else akhir.year
            return buat(th, bl, d), False
        return buat(tahun_default, bl, d), False
    return None, False


def samarkan(teks):
    """Samarkan deret >= 8 digit, termasuk yang dipisah spasi/tanda hubung (mis. 0021-01-000123-50-9)."""
    def ganti(m):
        digit = re.sub(r"\D", "", m.group(0))
        return "****" + digit[-4:]
    pola = r"\d{4}(?: \d{4}){2,}|\d+(?:-\d+)+|\d{8,}"
    def mungkin(m):
        n = len(re.sub(r"\D", "", m.group(0)))
        batas = 10 if "-" in m.group(0) else 8  # tanggal 12-09-2026 (8 digit) tidak disamarkan
        return ganti(m) if n >= batas else m.group(0)
    return re.sub(pola, mungkin, teks or "")


def norm(s):
    return re.sub(r"[^a-z0-9]", "", (s or "").lower())

# ============================================================ baca file

def baca_teks(path):
    try:
        mentah = open(path, "rb").read()
    except OSError as e:
        gagal(f"File tidak bisa dibuka: {path}", str(e))
    if mentah[:4] == b"PK\x03\x04":
        gagal(f"File {path} adalah Excel (.xlsx). Simpan dulu sebagai CSV: Excel → File → Save As → CSV.")
    if mentah[:5] == b"%PDF-":
        gagal(f"File {path} adalah PDF. Unduh mutasi dalam format CSV/Excel dari internet banking, "
              "atau salin tabelnya ke spreadsheet lalu simpan sebagai CSV.")
    for enc in ("utf-8-sig", "cp1252", "latin-1"):
        try:
            return mentah.decode(enc)
        except UnicodeDecodeError:
            continue
    return mentah.decode("latin-1", errors="replace")


def tebak_pemisah(teks):
    baris = [b for b in teks.splitlines()[:60] if b.strip()]
    skor = {}
    for sep in (",", ";", "\t", "|"):
        hit = [len(next(csv.reader([b], delimiter=sep))) for b in baris]
        banyak = [h for h in hit if h >= 3]
        skor[sep] = (len(banyak), max(hit) if hit else 0)
    return max(skor, key=lambda k: skor[k])


KATA = {
    "tanggal": ["tanggal transaksi", "tgl transaksi", "transaction date", "tanggal", "tgl", "date",
                "post date", "posting date", "tgl_tran", "trx date", "tanggal posting", "value date"],
    "keterangan": ["keterangan", "deskripsi", "description", "uraian", "remark", "remarks", "desk_tran",
                   "narasi", "berita", "detail transaksi", "transaksi", "details", "memo"],
    "kredit": ["kredit", "credit", "mutasi kredit", "mutasi_kredit", "cr", "uang masuk", "masuk", "setoran"],
    "debet": ["debet", "debit", "mutasi debet", "mutasi_debet", "mutasi debit", "db", "uang keluar", "keluar",
              "penarikan"],
    "nominal": ["jumlah", "nominal", "amount", "mutasi", "nilai", "total", "jumlah (idr)"],
    "dk": ["d/k", "db/cr", "cr/db", "dk", "d/c", "k/d", "jenis", "tipe", "type", "debit/credit"],
    "saldo": ["saldo", "balance", "saldo akhir", "saldo_akhir_mutasi", "running balance"],
}
KATA_CATAT = {
    "tanggal": ["tanggal bayar", "tgl bayar", "tanggal", "tgl", "date", "tanggal invoice", "tanggal transaksi",
                "tanggal pesanan", "waktu"],
    "nominal": ["total", "nominal", "jumlah", "total bayar", "grand total", "amount", "nilai", "tagihan",
                "total tagihan", "harga"],
    "ref": ["no invoice", "nomor invoice", "invoice", "no. invoice", "no faktur", "nomor", "no", "ref",
            "referensi", "no pesanan", "order id", "kode"],
    "nama": ["pelanggan", "nama pelanggan", "customer", "nama", "pembeli", "klien", "konsumen", "supplier",
             "vendor", "pemasok", "nama supplier", "penerima"],
    "status": ["status", "status pesanan", "status bayar"],
    "metode": ["metode", "metode bayar", "cara bayar", "pembayaran", "payment", "payment method"],
}


def cocok_kata(sel, daftar):
    s = (sel or "").strip().lower().strip("\"' ")
    if not s:
        return 0
    if s in daftar:
        return 2
    if any(len(k) > 3 and k in s for k in daftar):
        return 1
    return 0


def petakan(header, kamus):
    peta, terpakai = {}, set()
    for kunci, daftar in kamus.items():
        terbaik, skor = None, 0
        for i, h in enumerate(header):
            if i in terpakai:
                continue
            if kunci in ("nominal", "kredit", "debet") and re.search(r"saldo|balance", h or "", re.I):
                continue
            sk = cocok_kata(h, daftar)
            if sk > skor:
                terbaik, skor = i, sk
        if terbaik is not None:
            peta[kunci] = header[terbaik].strip()
            terpakai.add(terbaik)
    return peta


def baca_tabel(path, baris_judul=None, kamus=KATA):
    teks = baca_teks(path)
    if not teks.strip():
        gagal(f"File {path} kosong.")
    sep = tebak_pemisah(teks)
    semua = list(csv.reader(io.StringIO(teks), delimiter=sep))
    if baris_judul:
        idx = baris_judul - 1
        if not 0 <= idx < len(semua):
            gagal(f"Baris judul {baris_judul} di luar isi file ({len(semua)} baris).")
    else:
        idx = None
        for i, row in enumerate(semua[:60]):
            skor = sum(1 for c in row if any(cocok_kata(c, d) for d in kamus.values()))
            ada_tgl = any(cocok_kata(c, kamus["tanggal"]) for c in row)
            if ada_tgl and skor >= 2:
                idx = i
                break
        if idx is None:
            gagal(f"Baris judul kolom di {path} tidak ditemukan otomatis. Sebutkan dengan --baris-judul-bank / "
                  "--baris-judul-catatan (nomor baris, mulai 1).",
                  {"10_baris_pertama": [" | ".join(r) for r in semua[:10]]})
    header = [h.strip().strip("'\"") for h in semua[idx]]
    # kolom tanpa nama diberi nama agar bisa dirujuk
    header = [h if h else f"kolom_{i + 1}" for i, h in enumerate(header)]
    # judul kolom ganda (mis. dua "Description") diberi akhiran _2, _3 agar tidak saling menimpa
    dilihat = {}
    for i, h in enumerate(header):
        if h in dilihat:
            dilihat[h] += 1
            header[i] = f"{h}_{dilihat[h]}"
        else:
            dilihat[h] = 1
    data = []
    for no, row in enumerate(semua[idx + 1:], start=idx + 2):
        if not any(c.strip() for c in row):
            continue
        rec = {header[i]: (row[i] if i < len(row) else "") for i in range(len(header))}
        # kolom lebih banyak dari judul (mis. BCA: 'Jumlah' lalu 'CR' di kolom tanpa judul)
        for j in range(len(header), len(row)):
            rec[f"kolom_{j + 1}"] = row[j]
        rec["__baris__"] = no
        data.append(rec)
    pembuka = "\n".join(",".join(r) for r in semua[:idx])
    return header, data, sep, idx + 1, pembuka


def tebak_format(header):
    h = " | ".join(x.lower() for x in header)
    if "tanggal transaksi" in h and "cabang" in h:
        return "mirip ekspor BCA (tebakan)"
    if "tgl_tran" in h or "mutasi_debet" in h or "desk_tran" in h:
        return "mirip ekspor BRI (tebakan)"
    if "post date" in h and "journal" in h:
        return "mirip ekspor BNI (tebakan)"
    if ("val. date" in h or "value date" in h) and ("reference" in h or "transaction code" in h):
        return "mirip ekspor Mandiri (tebakan)"
    return "format umum"


def tahun_dari_teks(teks):
    """Tahun dari bagian atas file (mis. 'Periode : 25/12/2025 - 05/01/2026').

    Kembalikan int, atau tuple (tgl_awal, tgl_akhir) bila periode melewati pergantian tahun."""
    tgl = [parse_tanggal(x)[0] for x in re.findall(r"\d{1,2}[/-]\d{1,2}[/-]20\d{2}|20\d{2}-\d{1,2}-\d{1,2}", teks or "")]
    tgl = [t for t in tgl if t]
    if len(tgl) >= 2 and tgl[0].year != tgl[-1].year:
        return (tgl[0], tgl[-1])
    th = re.findall(r"\b(20\d{2})\b", teks or "")
    return int(th[-1]) if th else None

# ============================================================ perintah: deteksi

def cmd_deteksi(a):
    hasil = {}
    header, data, sep, bj, pembuka = baca_tabel(a.bank, a.baris_judul_bank, KATA)
    peta = petakan(header, KATA)
    if "dk" not in peta:
        kunci_kol = list(header) + sorted({k for r in data for k in r if k.startswith("kolom_") and k not in header})
        for k in kunci_kol:
            nilai = [(r.get(k) or "").strip().upper() for r in data if (r.get(k) or "").strip()]
            if nilai and sum(v in ("CR", "DB", "D", "K", "C", "DR", "KR") for v in nilai) >= 0.8 * len(nilai):
                peta["dk"] = k
                break
    contoh = []
    for r in data[:3]:
        contoh.append({k: samarkan(r.get(v, "")) for k, v in peta.items()})
    saran = []
    if "kredit" in peta or "debet" in peta:
        saran.append("Kolom debet & kredit terpisah terdeteksi.")
    elif "nominal" in peta:
        sampel = [parse_angka(r.get(peta["nominal"]))[1] for r in data[:20]]
        if "dk" in peta:
            saran.append(f"Satu kolom nominal + kolom penanda '{peta['dk']}' (CR/DB).")
        elif any(sampel):
            saran.append("Satu kolom nominal dengan akhiran CR/DB di angkanya.")
        else:
            cari = [k for k in header if k.startswith("kolom_")]
            saran.append("Satu kolom nominal TANPA penanda CR/DB. Tanyakan pengguna: apakah uang keluar ditulis "
                         "negatif? Jika ada kolom tanpa judul berisi CR/DB, pakai --bank-dk " + (cari[0] if cari else "<kolom>"))
    hasil["bank"] = {
        "file": a.bank, "pemisah": {"\t": "tab"}.get(sep, sep), "baris_judul": bj,
        "format_tebakan": tebak_format(header), "kolom_tersedia": header,
        "kolom_terdeteksi": peta, "contoh_3_baris": contoh, "jumlah_baris_data": len(data),
        "tahun_di_bagian_atas_file": (lambda t: f"{t[0].isoformat()}..{t[1].isoformat()}" if isinstance(t, tuple)
                                      else t)(tahun_dari_teks(pembuka)), "catatan": saran,
    }
    if a.catatan:
        h2, d2, sep2, bj2, _ = baca_tabel(a.catatan, a.baris_judul_catatan, KATA_CATAT)
        p2 = petakan(h2, KATA_CATAT)
        hasil["catatan"] = {
            "file": a.catatan, "pemisah": {"\t": "tab"}.get(sep2, sep2), "baris_judul": bj2,
            "kolom_tersedia": h2, "kolom_terdeteksi": p2, "jumlah_baris_data": len(d2),
            "contoh_3_baris": [{k: samarkan(r.get(v, "")) for k, v in p2.items()} for r in d2[:3]],
        }
    hasil["langkah_berikutnya"] = ("KONFIRMASI pemetaan kolom ke pengguna, lalu jalankan perintah 'cocokkan' "
                                   "dengan argumen --bank-* dan --catat-* yang sudah disetujui.")
    print(json.dumps(hasil, ensure_ascii=False, indent=2))

# ============================================================ perintah: cocokkan

KATA_BIAYA_BANK = ["biaya adm", "biaya admin", "adm bulanan", "bunga", "pajak bunga", "pajak", "admin fee",
                   "materai", "biaya kartu", "biaya transfer", "bi-fast fee", "charge"]
STATUS_BATAL = ["batal", "dibatalkan", "cancel", "refund", "retur", "gagal", "void"]


def ambil_bank(a, header, data, tahun_def):
    def kol(nama, nilai):
        if nilai and nilai not in header and nilai not in data[0]:
            gagal(f"Kolom bank '{nilai}' ({nama}) tidak ada.", {"kolom_tersedia": header})
        return nilai

    kt = kol("tanggal", a.bank_tanggal)
    kk_list = [kol("keterangan", k) for k in (a.bank_keterangan or [])]
    kkr, kdb = kol("kredit", a.bank_kredit), kol("debet", a.bank_debet)
    kn, kdk = kol("nominal", a.bank_nominal), kol("dk", a.bank_dk)
    if not kt:
        gagal("Kolom tanggal bank wajib (--bank-tanggal).")
    if not (kkr or kdb or kn):
        gagal("Sebutkan kolom nominal bank: --bank-kredit/--bank-debet, atau --bank-nominal (+ --bank-dk).")

    hasil, lewat, perlu_tahun, pend = [], {}, 0, []
    for r in data:
        if (r.get(kt) or "").strip().strip("'").upper().startswith("PEND"):
            ket_p = " ".join(str(r.get(k, "") or "").strip() for k in kk_list if k).strip()
            nil = parse_angka(r.get(kkr or kn))[0] if (kkr or kn) else None
            pend.append({"baris_file": r["__baris__"], "keterangan": ket_p,
                         "nominal": bulat(abs(nil)) if nil else None})
            continue
        tgl, butuh = parse_tanggal(r.get(kt), a.urutan_tanggal, tahun_def)
        if tgl is None:
            if butuh:
                perlu_tahun += 1
            alasan = "tanggal kosong/tidak terbaca (mis. baris ringkasan saldo)"
            lewat[alasan] = lewat.get(alasan, 0) + 1
            continue
        masuk = keluar = None
        if kkr or kdb:
            vk = parse_angka(r.get(kkr))[0] if kkr else None
            vd = parse_angka(r.get(kdb))[0] if kdb else None
            if vk:
                masuk = abs(vk)
            if vd:
                keluar = abs(vd)
        else:
            v, dk = parse_angka(r.get(kn))
            if v is not None:
                if kdk:
                    penanda = (r.get(kdk) or "").strip().upper()
                    if penanda in ("CR", "C", "K", "KR", "KREDIT", "CREDIT", "MASUK", "+"):
                        dk = "CR"
                    elif penanda in ("DB", "D", "DR", "DEBET", "DEBIT", "KELUAR", "-"):
                        dk = "DB"
                if dk == "CR":
                    masuk = abs(v)
                elif dk == "DB":
                    keluar = abs(v)
                elif a.bank_tanpa_penanda == "negatif-keluar":
                    masuk, keluar = (v, None) if v > 0 else (None, -v)
                else:
                    gagal("Kolom nominal bank tidak punya penanda masuk/keluar (CR/DB). Tentukan --bank-dk, "
                          "atau --bank-tanpa-penanda negatif-keluar jika uang keluar ditulis minus.")
        if not masuk and not keluar:
            alasan = "nominal kosong/tidak terbaca"
            lewat[alasan] = lewat.get(alasan, 0) + 1
            continue
        ket = " ".join(str(r.get(k, "") or "").strip() for k in kk_list if k).strip()
        for arah, nilai in (("masuk", masuk), ("keluar", keluar)):
            if nilai:
                hasil.append({"id": f"B{r['__baris__']}" + ("" if not (masuk and keluar) else arah[0]),
                              "baris": r["__baris__"], "tanggal": tgl, "nominal": bulat(nilai),
                              "arah": arah, "keterangan": ket})
    return hasil, lewat, perlu_tahun, pend


def ambil_catatan(a, header, data):
    def kol(nama, nilai, wajib=False):
        if wajib and not nilai:
            gagal(f"Kolom catatan untuk {nama} wajib (--catat-{nama}).", {"kolom_tersedia": header})
        if nilai and nilai not in header:
            gagal(f"Kolom catatan '{nilai}' ({nama}) tidak ada.", {"kolom_tersedia": header})
        return nilai

    kt, kn = kol("tanggal", a.catat_tanggal, True), kol("nominal", a.catat_nominal, True)
    kr, km = kol("ref", a.catat_ref), kol("nama", a.catat_nama)
    ks, kmet = kol("status", a.catat_status), kol("metode", a.catat_metode)
    abaikan_metode = [x.strip().lower() for x in (a.abaikan_metode or "").split(",") if x.strip()]
    hasil, lewat, dibuang = [], {}, {}
    for r in data:
        if ks and any(k in (r.get(ks) or "").lower() for k in STATUS_BATAL):
            dibuang["status batal/refund"] = dibuang.get("status batal/refund", 0) + 1
            continue
        if kmet and abaikan_metode and (r.get(kmet) or "").strip().lower() in abaikan_metode:
            dibuang[f"metode {r.get(kmet).strip()}"] = dibuang.get(f"metode {r.get(kmet).strip()}", 0) + 1
            continue
        tgl, _ = parse_tanggal(r.get(kt), a.urutan_tanggal, None)
        if tgl is None:
            lewat["tanggal tidak terbaca"] = lewat.get("tanggal tidak terbaca", 0) + 1
            continue
        v, _ = parse_angka(r.get(kn))
        if v is None or v <= 0:
            lewat["nominal kosong/tidak valid"] = lewat.get("nominal kosong/tidak valid", 0) + 1
            continue
        hasil.append({"id": f"C{r['__baris__']}", "baris": r["__baris__"], "tanggal": tgl, "nominal": bulat(v),
                      "ref": (r.get(kr) or "").strip() if kr else "", "nama": (r.get(km) or "").strip() if km else ""})
    return hasil, lewat, dibuang


KATA_UMUM_NAMA = {"toko", "bapak", "ibu", "pak", "bu", "mas", "mbak", "sdri", "sdr", "cv", "pt", "ud", "tbk",
                  "jaya", "abadi", "makmur", "sentosa", "maju", "sejahtera", "mandiri", "utama", "indonesia",
                  "group", "grup", "store", "shop", "official", "penjualan", "jual", "transfer", "bayar",
                  "pembayaran", "invoice", "inv", "dan", "the", "agt", "agu", "sep", "okt", "nov", "des", "jan",
                  "feb", "mar", "apr", "mei", "jun", "jul", "supplier", "vendor"}
KATA_MERCHANT = ["qris", "settlement", "edc", "mdr", "merchant", "shopeepay", "gopay", "ovo", "dana"]


def token(teks):
    return re.findall(r"[a-z0-9]+", (teks or "").lower())


SAPAAN_BADAN = {"toko", "bapak", "ibu", "pak", "bu", "mas", "mbak", "sdri", "sdr", "cv", "pt", "ud", "tbk"}


def kata_nama(c):
    """Kata khas nama pelanggan/supplier (huruf, >= 3 huruf, bukan kata umum)."""
    return {t for t in token(c["nama"]) if len(t) >= 3 and t.isalpha() and t not in KATA_UMUM_NAMA}


def kata_nama_umum(c):
    """Untuk nama yang seluruhnya kata umum (mis. 'CV Makmur Sentosa'): semua katanya harus muncul."""
    return {t for t in token(c["nama"]) if len(t) >= 3 and t.isalpha() and t not in SAPAAN_BADAN}


def cocok_ref(c, b):
    """No. invoice ada di keterangan bank sebagai 'kata utuh' (tidak menempel ke huruf/angka lain)."""
    ref = (c["ref"] or "").strip().lower()
    if not ref:
        return False
    ket = (b["keterangan"] or "").lower()
    varian = {ref, re.sub(r"[\s\-/_.]", "", ref), re.sub(r"[\s\-/_.]+", " ", ref)}
    for v in varian:
        if not v:
            continue
        hanya_angka = v.replace(" ", "").isdigit()
        if hanya_angka and (len(v.replace(" ", "")) < 4 or v.replace(" ", "") == str(b["nominal"])
                            or v.replace(" ", "") == str(c["nominal"])):
            continue
        if len(v) < 3:
            continue
        if re.search(r"(?<![a-z0-9])" + re.escape(v) + r"(?![a-z0-9])", ket):
            return True
    return False


def cocok_nama(c, b):
    tb = set(token(b["keterangan"]))
    kn = kata_nama(c)
    if kn:
        return bool(kn & tb)
    ku = kata_nama_umum(c)
    return len(ku) >= 2 and ku <= tb


def petunjuk_teks(c, b):
    """True bila no. invoice atau nama pelanggan catatan muncul (sebagai kata utuh) di keterangan bank."""
    return cocok_ref(c, b) or cocok_nama(c, b)


def cocokkan(bank, catat, a):
    tol_hari, maks_hari, maks_nama = a.toleransi_hari, a.maks_hari_parsial, max(a.maks_hari_parsial, a.maks_hari_nama)
    tol_rp = bulat(parse_angka(a.toleransi_nominal)[0] or Decimal(0))
    sel_rp = bulat(parse_angka(a.toleransi_selisih)[0] or Decimal(0))
    sel_pct = Decimal(str(a.toleransi_persen)) / 100
    keluar = a.arah == "keluar"
    pihak = "supplier" if keluar else "pelanggan"
    pakaiB, pakaiC = set(), set()
    hasil = []
    petunjuk = {(c["id"], b["id"]): petunjuk_teks(c, b) for c in catat for b in bank}

    def konflik(c, b):
        """Keterangan bank memuat nama/ref catatan LAIN yang masih terbuka, tetapi bukan milik c."""
        if petunjuk[(c["id"], b["id"])]:
            return None
        kn = kata_nama(c)
        for c2 in catat:
            if c2["id"] == c["id"] or c2["id"] in pakaiC:
                continue
            if petunjuk[(c2["id"], b["id"])] and not (kata_nama(c2) & kn and kn):
                return c2
        return None

    def selisih_hari(c, b):
        return (b["tanggal"] - c["tanggal"]).days

    def catat_hasil(status, cs, bs, alasan):
        tc, tb = sum(c["nominal"] for c in cs), sum(b["nominal"] for b in bs)
        hasil.append({"status": status, "catatan": cs, "bank": bs, "total_catatan": tc, "total_bank": tb,
                      "selisih": tc - tb, "alasan": alasan})
        pakaiC.update(c["id"] for c in cs)
        pakaiB.update(b["id"] for b in bs)

    def sisaC():
        return [c for c in catat if c["id"] not in pakaiC]

    def sisaB():
        return [b for b in bank if b["id"] not in pakaiB]

    def pasang_satu(kandidat, buat):
        for *_, c, b in sorted(kandidat, key=lambda x: x[:-2]):
            if c["id"] in pakaiC or b["id"] in pakaiB:
                continue
            r = buat(c, b)
            if r:
                catat_hasil(*r)

    def teks_hari(dh):
        return "tanggal sama" if dh == 0 else f"tanggal bank {dh:+d} hari"

    # 0. nama/no. invoice cocok + nominal sama (jendela lebar: --maks-hari-nama)
    kand = [(abs(selisih_hari(c, b)), c["baris"], b["baris"], c, b) for c in sisaC() for b in sisaB()
            if petunjuk[(c["id"], b["id"])] and abs(c["nominal"] - b["nominal"]) <= tol_rp
            and abs(selisih_hari(c, b)) <= maks_nama]

    def buat0(c, b):
        dh = selisih_hari(c, b)
        if abs(dh) <= tol_hari:
            return "COCOK", [c], [b], f"nominal sama, {teks_hari(dh)}, nama/no. invoice ada di keterangan bank"
        return "PARSIAL", [c], [b], f"nominal & nama sama, tetapi tanggal berbeda {dh:+d} hari"
    pasang_satu(kand, buat0)

    # 1. nominal sama + tanggal dalam toleransi, tanpa konflik nama
    kand = [(abs(selisih_hari(c, b)), 0 if selisih_hari(c, b) >= 0 else 1, c["baris"], b["baris"], c, b)
            for c in sisaC() for b in sisaB()
            if abs(c["nominal"] - b["nominal"]) <= tol_rp and abs(selisih_hari(c, b)) <= tol_hari]

    def buat1(c, b):
        if konflik(c, b):
            return None
        return ("COCOK", [c], [b], f"nominal sama, {teks_hari(selisih_hari(c, b))}"
                + ("" if not (c["nama"] or c["ref"]) else "; nama tidak terlihat di keterangan bank — cek sekilas"))
    pasang_satu(kand, buat1)

    def kombinasi(calon, target):
        for k in (2, 3):
            for kombo in itertools.combinations(calon, k):
                if abs(sum(x["nominal"] for x in kombo) - target) <= tol_rp:
                    return kombo
        return None

    # 2b. satu transaksi bank = gabungan 2–3 catatan
    for b in sorted(sisaB(), key=lambda x: -x["nominal"]):
        if b["id"] in pakaiB:
            continue
        calon = [c for c in sisaC() if c["nominal"] < b["nominal"] and abs(selisih_hari(c, b)) <= maks_hari
                 and not konflik(c, b)]
        calon = sorted(calon, key=lambda c: (0 if petunjuk[(c["id"], b["id"])] else 1,
                                             abs(selisih_hari(c, b))))[:a.maks_kandidat]
        kombo = kombinasi(calon, b["nominal"])
        if kombo:
            catat_hasil("PARSIAL", list(kombo), [b], f"1 transaksi bank = gabungan {len(kombo)} catatan")

    # 2c. satu catatan dibayar dengan 2–3 transaksi bank
    for c in sorted(sisaC(), key=lambda x: -x["nominal"]):
        if c["id"] in pakaiC:
            continue
        calon = [b for b in sisaB() if b["nominal"] < c["nominal"] and -tol_hari <= selisih_hari(c, b) <= maks_hari
                 and not konflik(c, b)]
        calon = sorted(calon, key=lambda b: (0 if petunjuk[(c["id"], b["id"])] else 1,
                                             abs(selisih_hari(c, b))))[:a.maks_kandidat]
        kombo = kombinasi(calon, c["nominal"])
        if kombo:
            catat_hasil("PARSIAL", [c], list(kombo), f"1 catatan dibayar dengan {len(kombo)} transaksi bank")

    def alasan_beda(c, b, d):
        lebih = "bank lebih kecil" if d > 0 else "bank lebih besar"
        if any(k in (b["keterangan"] or "").lower() for k in KATA_MERCHANT):
            return f"nominal beda {rp(abs(d))} ({lebih}; kemungkinan dipotong biaya merchant QRIS/EDC/MDR)"
        if keluar:
            return f"nominal beda {rp(abs(d))} ({lebih}; kemungkinan biaya transfer, diskon/potongan supplier, atau salah ketik)"
        return f"nominal beda {rp(abs(d))} ({lebih}; kemungkinan potongan biaya transfer/admin, ongkir, atau salah ketik)"

    # 2d. nominal beda tipis, tanggal dalam toleransi (berpetunjuk dulu), tanpa konflik
    kand = []
    for c in sisaC():
        for b in sisaB():
            d = abs(c["nominal"] - b["nominal"])
            batas = max(sel_rp, bulat(Decimal(c["nominal"]) * sel_pct))
            if 0 < d <= batas and abs(selisih_hari(c, b)) <= tol_hari:
                kand.append((0 if petunjuk[(c["id"], b["id"])] else 1, d, abs(selisih_hari(c, b)),
                             c["baris"], b["baris"], c, b))
    pasang_satu(kand, lambda c, b: None if konflik(c, b) else
                ("PARSIAL", [c], [b], alasan_beda(c, b, c["nominal"] - b["nominal"])))

    # 2e. nama/no. invoice cocok, nominal beda: hanya bila bank <= catatan (bayar sebagian) atau selisih <= 50%
    kand = []
    for c in sisaC():
        for b in sisaB():
            dh = selisih_hari(c, b)
            if petunjuk[(c["id"], b["id"])] and -maks_nama <= dh <= maks_nama and (
                    b["nominal"] <= c["nominal"] or abs(c["nominal"] - b["nominal"]) <= c["nominal"] * 0.5):
                kand.append((abs(dh), c["baris"], b["baris"], c, b))

    def buat2e(c, b):
        d = c["nominal"] - b["nominal"]
        if any(k in (b["keterangan"] or "").lower() for k in KATA_MERCHANT):
            return "PARSIAL", [c], [b], "nama/ref cocok, " + alasan_beda(c, b, d)
        if d > 0:
            teks = f"{rp(d)} lebih kecil (kemungkinan baru {'dibayar' if keluar else 'bayar'} sebagian)"
        else:
            teks = f"{rp(-d)} lebih besar (cek apakah termasuk pembayaran lain)"
        return "PARSIAL", [c], [b], "nama/no. invoice cocok, nominal bank " + teks
    pasang_satu(kand, buat2e)

    # 2a. nominal sama, tanggal di luar toleransi (<= maks_hari_parsial), tanpa konflik nama
    kand = [(abs(selisih_hari(c, b)), c["baris"], b["baris"], c, b) for c in sisaC() for b in sisaB()
            if abs(c["nominal"] - b["nominal"]) <= tol_rp and abs(selisih_hari(c, b)) <= maks_hari]
    pasang_satu(kand, lambda c, b: None if konflik(c, b) else
                ("PARSIAL", [c], [b], f"nominal sama, tetapi tanggal berbeda {selisih_hari(c, b):+d} hari; "
                                      "nama tidak terlihat di keterangan bank"))

    # 3. nominal & tanggal cocok tetapi keterangan bank memuat nama pihak lain → kemungkinan tertukar
    kand = [(abs(selisih_hari(c, b)), c["baris"], b["baris"], c, b) for c in sisaC() for b in sisaB()
            if abs(c["nominal"] - b["nominal"]) <= tol_rp and abs(selisih_hari(c, b)) <= tol_hari]

    def buat3(c, b):
        lain = konflik(c, b)
        nama_lain = (lain["nama"] or lain["ref"]) if lain else "pihak lain"
        return ("PARSIAL", [c], [b], f"KEMUNGKINAN TERTUKAR: nominal & tanggal sama, tetapi keterangan bank memuat "
                                     f"nama/ref '{nama_lain}', bukan '{c['nama'] or c['ref']}' — cek manual")
    pasang_satu(kand, buat3)

    for c in sisaC():
        if keluar:
            al = "tidak ada pembayaran keluar yang cocok (belum dibayar, dibayar tunai/rekening lain, atau salah catat)"
        else:
            al = "tidak ada transfer yang cocok (belum dibayar, dibayar tunai, masuk ke rekening lain, atau salah catat)"
        catat_hasil("TIDAK ADA DI BANK", [c], [], al)
    for b in sisaB():
        k = (b["keterangan"] or "").lower()
        if any(x in k for x in KATA_BIAYA_BANK):
            al = ("kemungkinan biaya/pajak bank — bukan pembayaran ke " + pihak) if keluar else \
                 "kemungkinan bunga/biaya/pajak bank — bukan penjualan"
        elif keluar:
            al = "tidak ada di catatan pembelian (pengeluaran lain, lupa dicatat, penarikan tunai, atau keperluan pribadi)"
        else:
            al = "tidak ada di catatan (pemasukan lain, lupa dicatat, atau dana pribadi)"
        catat_hasil("TIDAK ADA DI CATATAN", [], [b], al)
    return hasil


def cmd_cocokkan(a):
    hb, db, _, bj, pembuka = baca_tabel(a.bank, a.baris_judul_bank, KATA)
    if not db:
        gagal("File mutasi bank tidak berisi baris data di bawah judul kolom.")
    hc, dc, _, _, _ = baca_tabel(a.catatan, a.baris_judul_catatan, KATA_CATAT)
    if not dc:
        gagal("File catatan tidak berisi baris data.")

    catat, lewat_c, dibuang_c = ambil_catatan(a, hc, dc)
    tahun_def = a.tahun or tahun_dari_teks(pembuka) or (catat[0]["tanggal"].year if catat else None)
    bank_all, lewat_b, perlu_tahun, pend = ambil_bank(a, hb, db, tahun_def)
    peringatan = []
    if perlu_tahun and not tahun_def:
        gagal("Tanggal di mutasi bank tanpa tahun (mis. '02/09'). Sebutkan tahunnya dengan --tahun 2026.")
    if not a.tahun and any(POLA_DM.match((r.get(a.bank_tanggal) or "").strip().strip("'")) for r in db[:50]):
        th_teks = (f"{tahun_def[0].year}/{tahun_def[1].year} sesuai periode di atas file"
                   if isinstance(tahun_def, tuple) else str(tahun_def))
        peringatan.append(f"Tanggal bank tanpa tahun; dianggap tahun {th_teks}. Pastikan benar (ubah dengan --tahun).")
    bank = [b for b in bank_all if a.arah == "semua" or b["arah"] == a.arah]
    diabaikan_arah = len(bank_all) - len(bank)
    if a.dari or a.sampai:
        dari = parse_tanggal(a.dari)[0] if a.dari else date.min
        sampai = parse_tanggal(a.sampai)[0] if a.sampai else date.max
        if dari is None or sampai is None:
            gagal("Format --dari/--sampai tidak terbaca. Pakai 2026-09-01 atau 01/09/2026.")
        bank = [b for b in bank if dari <= b["tanggal"] <= sampai]
        catat = [c for c in catat if dari <= c["tanggal"] <= sampai]
    if not bank:
        gagal("Tidak ada transaksi bank yang bisa dicocokkan (cek arah/kolom/periode).",
              {"baris_bank_dilewati": lewat_b})
    if not catat:
        gagal("Tidak ada catatan yang bisa dicocokkan (cek kolom/periode).",
              {"baris_catatan_dilewati": lewat_c, "dibuang": dibuang_c})

    periode_b = (min(b["tanggal"] for b in bank), max(b["tanggal"] for b in bank))
    periode_c = (min(c["tanggal"] for c in catat), max(c["tanggal"] for c in catat))
    if (periode_c[0] - periode_b[1]).days > 7 or (periode_b[0] - periode_c[1]).days > 7:
        peringatan.append("Periode bank dan catatan hampir tidak beririsan — mungkin file/bulan yang dipakai salah.")
    elif abs((periode_c[0] - periode_b[0]).days) > 7 or abs((periode_c[1] - periode_b[1]).days) > 7:
        peringatan.append("Periode bank dan catatan berbeda > 7 hari. Transaksi di ujung periode bisa muncul "
                          "sebagai tidak cocok; pertimbangkan --dari/--sampai.")

    hasil = cocokkan(bank, catat, a)
    lengkap = a.tampilkan_lengkap

    def ringkas(status):
        g = [h for h in hasil if h["status"] == status]
        return {"jumlah_kelompok": len(g), "total_catatan": sum(h["total_catatan"] for h in g),
                "total_bank": sum(h["total_bank"] for h in g)}

    total_c = sum(c["nominal"] for c in catat)
    total_b = sum(b["nominal"] for b in bank)
    r = {s: ringkas(s) for s in ("COCOK", "PARSIAL", "TIDAK ADA DI BANK", "TIDAK ADA DI CATATAN")}
    sel_parsial = sum(h["selisih"] for h in hasil if h["status"] == "PARSIAL")
    sel_cocok = sum(h["selisih"] for h in hasil if h["status"] == "COCOK")  # > 0 hanya bila --toleransi-nominal > 0
    penjelasan = {
        "total_catatan": total_c, "total_bank": total_b, "selisih_total (catatan - bank)": total_c - total_b,
        "dari_catatan_tidak_ada_di_bank": r["TIDAK ADA DI BANK"]["total_catatan"],
        "dari_bank_tidak_ada_di_catatan": -r["TIDAK ADA DI CATATAN"]["total_bank"],
        "dari_selisih_nominal_cocok_parsial": sel_parsial,
        "dari_selisih_dalam_toleransi_cocok": sel_cocok,
    }
    cek = (penjelasan["dari_catatan_tidak_ada_di_bank"] + penjelasan["dari_bank_tidak_ada_di_catatan"]
           + sel_parsial + sel_cocok)
    penjelasan["cek_rumus_seimbang"] = (cek == total_c - total_b)
    penjelasan["catatan_seimbang"] = ("Seimbang hanya berarti angka penjelasan cocok dengan total selisih — BUKAN bukti "
                                      "setiap pasangan benar. Periksa pasangan PARSIAL dan yang bertanda KEMUNGKINAN TERTUKAR.")
    tertukar = [h for h in hasil if "TERTUKAR" in h["alasan"]]

    def tampil(item, sumber):
        d = {"baris_file": item["baris"], "tanggal": item["tanggal"].isoformat(), "nominal": item["nominal"]}
        if sumber == "b":
            d["keterangan"] = item["keterangan"] if lengkap else samarkan(item["keterangan"])
            d["arah"] = item["arah"]
        else:
            d["ref"], d["nama"] = item["ref"], item["nama"]
        return d

    detail = []
    urut = {"TIDAK ADA DI BANK": 0, "TIDAK ADA DI CATATAN": 1, "PARSIAL": 2, "COCOK": 3}
    for h in sorted(hasil, key=lambda h: (urut[h["status"]],
                                          min([x["tanggal"] for x in h["catatan"] + h["bank"]]))):
        detail.append({"status": h["status"], "alasan": h["alasan"], "selisih": h["selisih"],
                       "catatan": [tampil(c, "c") for c in h["catatan"]],
                       "bank": [tampil(b, "b") for b in h["bank"]]})

    out = {
        "pengaturan": {"arah": a.arah, "toleransi_hari": a.toleransi_hari, "maks_hari_parsial": a.maks_hari_parsial,
                       "toleransi_nominal": a.toleransi_nominal, "toleransi_selisih": a.toleransi_selisih,
                       "toleransi_persen": a.toleransi_persen, "tahun_default_bank": (f"{tahun_def[0].isoformat()}..{tahun_def[1].isoformat()}"
                                              if isinstance(tahun_def, tuple) else tahun_def),
                       "pembulatan": "nominal dibulatkan ke rupiah penuh (0,5 ke atas)",
                       "kolom_bank": {k: v for k, v in (("tanggal", a.bank_tanggal), ("keterangan", a.bank_keterangan),
                                                        ("kredit", a.bank_kredit), ("debet", a.bank_debet),
                                                        ("nominal", a.bank_nominal), ("dk", a.bank_dk)) if v},
                       "baris_judul_bank": bj},
        "periode": {"bank": [periode_b[0].isoformat(), periode_b[1].isoformat()],
                    "catatan": [periode_c[0].isoformat(), periode_c[1].isoformat()]},
        "ringkasan": {"jumlah_transaksi_bank": len(bank), "jumlah_catatan": len(catat),
                      "per_status": r, "penjelasan_selisih": penjelasan},
        "detail": detail,
        "dilewati": {"bank": lewat_b, "catatan": lewat_c, "catatan_dibuang": dibuang_c,
                     "bank_arah_lain_diabaikan": diabaikan_arah},
        "transaksi_tertunda_pend": [dict(p, keterangan=(p["keterangan"] if lengkap else samarkan(p["keterangan"])))
                                    for p in pend],
        "kemungkinan_tertukar": len(tertukar),
        "peringatan": peringatan,
        "privasi": "Nomor panjang (>= 8 digit, termasuk yang dipisah spasi/tanda hubung) di keterangan disamarkan." if not lengkap else
                   "PERINGATAN: keterangan ditampilkan lengkap; jangan bagikan output ini.",
    }
    if pend:
        peringatan.append(f"{len(pend)} transaksi berstatus PEND (tertunda) tidak dihitung — cek di mutasi periode berikutnya.")
    if tertukar:
        peringatan.append(f"{len(tertukar)} pasangan bertanda KEMUNGKINAN TERTUKAR (nama di bank berbeda dengan catatan) — cek manual.")
    if a.output_csv:
        tulis_csv(a.output_csv, a.pemisah, detail)
        out["file_csv"] = a.output_csv
        peringatan.append(f"File {a.output_csv} berisi data transaksi — hapus setelah dipakai, jangan dibagikan.")
    if a.format == "teks":
        cetak_teks(out)
    else:
        print(json.dumps(out, ensure_ascii=False, indent=2))


def tulis_csv(path, sep, detail):
    rows = [["Status", "Alasan", "Tgl catatan", "Ref/Invoice", "Nama", "Nominal catatan",
             "Tgl bank", "Keterangan bank", "Nominal bank", "Selisih (catatan-bank)"]]
    for d in detail:
        rows.append([d["status"], d["alasan"],
                     " + ".join(c["tanggal"] for c in d["catatan"]), " + ".join(c["ref"] for c in d["catatan"]),
                     " + ".join(c["nama"] for c in d["catatan"]), sum(c["nominal"] for c in d["catatan"]),
                     " + ".join(b["tanggal"] for b in d["bank"]), " | ".join(b["keterangan"] for b in d["bank"]),
                     sum(b["nominal"] for b in d["bank"]), d["selisih"]])
    try:
        with open(path, "w", encoding="utf-8-sig", newline="") as f:
            csv.writer(f, delimiter=sep).writerows(rows)
    except OSError as e:
        gagal(f"Gagal menulis {path}", str(e))


def cetak_teks(o):
    r = o["ringkasan"]
    p = r["penjelasan_selisih"]
    print(f"Periode bank {o['periode']['bank'][0]} s.d. {o['periode']['bank'][1]}; "
          f"catatan {o['periode']['catatan'][0]} s.d. {o['periode']['catatan'][1]}")
    print(f"Total catatan {rp(p['total_catatan'])} | total bank ({o['pengaturan']['arah']}) {rp(p['total_bank'])} | "
          f"selisih {rp(p['selisih_total (catatan - bank)'])} | rumus seimbang: {p['cek_rumus_seimbang']} "
          "(seimbang ≠ semua pasangan benar)")
    for s, v in r["per_status"].items():
        print(f"- {s}: {v['jumlah_kelompok']} kelompok, catatan {rp(v['total_catatan'])}, bank {rp(v['total_bank'])}")
    print()
    for d in o["detail"]:
        c = "; ".join(f"{x['tanggal']} {x['ref'] or x['nama']} {rp(x['nominal'])}" for x in d["catatan"]) or "-"
        b = "; ".join(f"{x['tanggal']} {x['keterangan'][:40]} {rp(x['nominal'])}" for x in d["bank"]) or "-"
        print(f"[{d['status']}] catatan: {c} || bank: {b} || {d['alasan']}")
    for w in o["peringatan"]:
        print("! " + w)


def main():
    p = argparse.ArgumentParser(description="Rekonsiliasi mutasi bank vs catatan penjualan/invoice")
    sub = p.add_subparsers(dest="perintah")

    def umum(sp):
        sp.add_argument("--bank", required=True, help="CSV mutasi rekening dari internet banking")
        sp.add_argument("--baris-judul-bank", type=int, help="Nomor baris judul kolom (mulai 1) jika deteksi salah")
        sp.add_argument("--baris-judul-catatan", type=int)

    d = sub.add_parser("deteksi", help="Tebak kolom untuk dikonfirmasi pengguna")
    umum(d)
    d.add_argument("--catatan", help="CSV catatan penjualan/invoice")
    d.add_argument("--urutan-tanggal", default="dmy", choices=["dmy", "mdy"])

    c = sub.add_parser("cocokkan", help="Cocokkan transaksi")
    umum(c)
    c.add_argument("--catatan", required=True)
    c.add_argument("--bank-tanggal", required=True)
    c.add_argument("--bank-keterangan", action="append",
                   help="Kolom keterangan; boleh diulang untuk menggabungkan beberapa kolom (mis. Description dan Description_2)")
    c.add_argument("--bank-kredit", help="Kolom uang masuk")
    c.add_argument("--bank-debet", help="Kolom uang keluar")
    c.add_argument("--bank-nominal", help="Kolom nominal tunggal (dengan CR/DB atau kolom --bank-dk)")
    c.add_argument("--bank-dk", help="Kolom penanda CR/DB (D/K)")
    c.add_argument("--bank-tanpa-penanda", choices=["error", "negatif-keluar"], default="error",
                   help="Jika nominal tunggal tanpa CR/DB: 'negatif-keluar' = angka minus adalah uang keluar")
    c.add_argument("--catat-tanggal", required=True)
    c.add_argument("--catat-nominal", required=True)
    c.add_argument("--catat-ref", help="Kolom no. invoice/pesanan")
    c.add_argument("--catat-nama", help="Kolom nama pelanggan")
    c.add_argument("--catat-status", help="Kolom status (baris batal/refund dibuang)")
    c.add_argument("--catat-metode", help="Kolom metode bayar")
    c.add_argument("--abaikan-metode", default="tunai,cash",
                   help="Nilai metode yang tidak lewat bank (default: tunai,cash)")
    c.add_argument("--arah", choices=["masuk", "keluar", "semua"], default="masuk",
                   help="masuk = cocokkan uang masuk dgn penjualan (default); keluar = pembayaran ke supplier")
    c.add_argument("--toleransi-hari", type=int, default=3, help="Selisih tanggal untuk cocok persis (default 3)")
    c.add_argument("--maks-hari-parsial", type=int, default=14, help="Jendela hari untuk cocok parsial (default 14)")
    c.add_argument("--maks-hari-nama", type=int, default=31,
                   help="Jendela hari bila nama/no. invoice ada di keterangan bank (default 31)")
    c.add_argument("--toleransi-nominal", default="0", help="Beda nominal yg masih dianggap sama (default 0)")
    c.add_argument("--toleransi-selisih", default="10000", help="Beda nominal tipis utk parsial (default Rp 10.000)")
    c.add_argument("--toleransi-persen", type=float, default=1.0, help="...atau persen dari nominal (default 1)")
    c.add_argument("--maks-kandidat", type=int, default=15, help="Batas kandidat kombinasi (default 15)")
    c.add_argument("--tahun", type=int, help="Tahun untuk tanggal bank tanpa tahun (mis. '02/09')")
    c.add_argument("--urutan-tanggal", default="dmy", choices=["dmy", "mdy"])
    c.add_argument("--dari", help="Batasi periode mulai (YYYY-MM-DD)")
    c.add_argument("--sampai", help="Batasi periode akhir (YYYY-MM-DD)")
    c.add_argument("--output-csv", help="Tulis detail hasil ke CSV (UTF-8 BOM)")
    c.add_argument("--pemisah", choices=[";", ","], default=";")
    c.add_argument("--format", choices=["json", "teks"], default="json")
    c.add_argument("--tampilkan-lengkap", action="store_true", help="Jangan samarkan nomor panjang di keterangan")

    a = p.parse_args()
    if a.perintah == "deteksi":
        cmd_deteksi(a)
    elif a.perintah == "cocokkan":
        if a.toleransi_hari < 0 or a.maks_hari_parsial < a.toleransi_hari:
            gagal("--toleransi-hari harus >= 0 dan --maks-hari-parsial >= --toleransi-hari.")
        for nama in ("toleransi_nominal", "toleransi_selisih"):
            if parse_angka(getattr(a, nama))[0] is None:
                gagal(f"Nilai --{nama.replace('_', '-')} tidak terbaca.")
        cmd_cocokkan(a)
    else:
        p.print_help()
        sys.exit(2)


if __name__ == "__main__":
    main()
