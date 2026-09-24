#!/usr/bin/env python3
"""Rekap operasional kunjungan klinik dari file CSV — AGREGAT SAJA.

Tujuan: menghasilkan angka kunjungan per hari/poli/penjamin, jam ramai, dan
jumlah pasien tidak datang, TANPA pernah menampilkan data per-pasien
(nama, NIK, tanggal lahir, diagnosis, dll.) di output. Ini BUKAN alat rekam
medis dan BUKAN alat skrining/diagnosis — hanya rekap jumlah untuk laporan
operasional (lihat CLAUDE.md Komunitech & keputusan pemilik jalur 3, bidang
kesehatan: tanpa skrining/diagnosis/kalkulator medis).

Prinsip keandalan & privasi (v1.0.3, setelah tiga ronde uji independen):
- Status kehadiran diklasifikasikan dari daftar kata kunci "hadir" dan
  "tidak datang". Status yang TIDAK cocok dengan salah satu daftar
  DILAPORKAN sebagai "tidak dikenal" — tidak pernah diam-diam dihitung
  sebagai hadir.
- Format tanggal (hari/bulan vs bulan/hari) ditentukan SEKALI untuk seluruh
  file dari bukti tak ambigu di dalamnya (mis. tanggal > 12). Baris yang
  buktinya bertentangan dengan format mayoritas tetap dibaca memakai bukti
  lokalnya sendiri, tapi diberi peringatan agar pengguna mengecek. File
  tanpa bukti sama sekali (semua hari/bulan ≤ 12) diberi peringatan bahwa
  ini asumsi, bukan kepastian, dengan cara mengesampingkannya lewat
  `--urutan-tanggal`.
- Semua angka agregat (total, hadir, tidak datang, persentase) dihitung
  eksplisit oleh script ini, bukan ditebak oleh agent.
- SATU fungsi penyaring (`_nilai_aman_ditampilkan`, dipakai lewat
  `_pisah_aman_dan_sembunyikan`) menentukan nilai kategori apa (status,
  poli, penjamin) yang aman dicetak ulang. Nilai yang tidak lolos TIDAK
  PERNAH dicetak — hanya digabung jadi angka agregat "N baris, K nilai
  berbeda disembunyikan". Syarat lolos (SEMUA harus benar): muncul di
  ≥ `MIN_FREKUENSI_TAMPIL` baris (k-anonimitas sederhana — nilai yang
  cuma muncul 1-2 kali kemungkinan besar salah isi/data satu pasien,
  bukan kategori asli), maksimal 3 kata, tanpa digit, tanpa "@", bukan
  pola inisial ("S.A."), bukan pola kode ICD ("J06"/"K02.1"), bukan pola
  sapaan+nama ("Bu Ani"), dan kolom belum melewati `MAKS_NILAI_UNIK_TAMPIL`
  nilai unik yang sudah ditampilkan. Ini mencegah kolom yang sebenarnya
  berisi teks bebas (nama, no. HP, diagnosis, inisial, email) bocor lewat
  bagian "rincian" walau nama kolomnya lolos deteksi kolom sensitif.
- Baris yang jumlah kolomnya TIDAK COCOK dengan header (mis. ekspor CSV
  dengan koma tanpa tanda kutip yang menggeser semua nilai satu kolom)
  DIKELUARKAN dari rincian per hari/poli/penjamin/status (supaya angka
  tidak salah diam-diam), tapi tetap dihitung di total pendaftaran dengan
  peringatan eksplisit — script tidak pernah menebak kolom mana yang benar
  untuk baris yang bergeser.

Hanya memakai library standar Python (3.8+). Lintas OS (Windows/macOS/Linux).

Contoh pakai:
    python3 rekap_kunjungan.py --file kunjungan.csv
    python3 rekap_kunjungan.py --file kunjungan.csv --format json
    python3 rekap_kunjungan.py --file kunjungan.csv --urutan-tanggal mdy

Windows: ganti "python3" dengan "python" atau "py".
"""
from __future__ import annotations

import argparse
import csv
import io
import json
import re
import sys
from collections import Counter
from datetime import date, datetime
from decimal import ROUND_HALF_UP, Decimal

# Pola (regex, dicocokkan per KATA/token, bukan potongan huruf bebas) nama
# kolom yang mengandung data pribadi/klinis spesifik — kalau nama kolom
# mengandung salah satu token ini, ISI kolom itu SENGAJA tidak pernah dibaca
# untuk ditampilkan (hanya nama kolomnya yang dilaporkan sebagai "diabaikan
# demi privasi pasien"). Kolom yang benar-benar dipakai skill (tanggal, jam,
# poli, penjamin, status) TIDAK PERNAH dilaporkan di sini meski pola cocok
# (lihat `_kolom_sensitif_di_header`), supaya tidak ada pernyataan yang
# saling bertentangan (mis. "Waktu" dipakai untuk jam tapi disebut sensitif).
POLA_KOLOM_SENSITIF = [
    r"\bnama\b", r"\bnik\b", r"\bktp\b", r"\brm\b", r"\brekam medis\b",
    r"\bbpjs\b", r"\bdiagnos\w*\b", r"\bdx\b", r"\bicd[\w-]*\b",
    r"\bkeluhan\b", r"\balamat\b", r"\btelp\w*\b", r"\btelepon\b", r"\bhp\b",
    r"\bwa\b", r"\bemail\b", r"\blahir\b", r"\bkontak\b", r"\bortu\b",
    r"\borang tua\b", r"\bibu\b", r"\bayah\b", r"\bpenanggung jawab\b",
    r"\basuransi no\w*\b", r"\bkartu\b",
]
POLA_KOLOM_SENSITIF_REGEX = [re.compile(p) for p in POLA_KOLOM_SENSITIF]

# Alias nama kolom yang diterima (huruf kecil, tanpa spasi berlebih) untuk
# setiap kolom agregat yang DIPAKAI. "keterangan"/catatan bebas SENGAJA
# TIDAK dimasukkan sebagai alias status (lihat B2, HASIL-UJI.md v1.0.1):
# kolom catatan bebas sering berisi nama/no. HP/diagnosis, bukan kategori
# kehadiran, dan hanya nama kolom yang eksplisit menyebut "status"/
# "kehadiran" yang dipakai.
ALIAS_TANGGAL = [
    "tanggal", "tgl", "date", "tanggal kunjungan", "tgl kunjungan",
    "tanggal daftar", "tgl daftar", "tanggal periksa", "tgl periksa",
    "tanggal pelayanan",
]
ALIAS_JAM = ["jam", "waktu", "jam kunjungan", "time"]
ALIAS_POLI = ["poli", "layanan", "unit", "poliklinik", "jenis layanan"]
ALIAS_PENJAMIN = ["penjamin", "pembayaran", "cara bayar", "jenis pasien", "kelas"]
ALIAS_STATUS = ["status", "status kunjungan", "status kehadiran"]

# Kata kunci status "TIDAK DATANG" (dicocokkan setelah normalisasi: huruf
# kecil, tanda baca dibuang, spasi dirapikan).
KATA_TIDAK_DATANG = [
    "tidak datang", "tdk datang", "tidak hadir", "tdk hadir", "tidak jadi",
    "belum datang", "mangkir", "no show", "noshow", "batal", "dibatalkan",
    "cancel", "absen", "reschedule tidak konfirmasi",
]
# Singkatan yang HANYA cocok bila nilainya persis sama dengan salah satu ini
# (dicocokkan penuh, bukan sebagai potongan kata, karena terlalu pendek
# untuk dicocokkan sebagai substring tanpa risiko salah tangkap).
SINGKATAN_TIDAK_DATANG = {"th", "nd", "ts"}

# Kata kunci status "HADIR" (pasien datang/dilayani).
KATA_HADIR = [
    "hadir", "datang", "selesai", "terlaksana", "berhasil", "dilayani",
    "checked in", "checkin", "check in", "sudah periksa", "sudah dilayani",
    "terlayani", "konsul selesai", "kontrol selesai",
]
SINGKATAN_HADIR = {"h", "y", "ok"}

# B2: pola "sapaan + nama" (mis. "Bu Ani", "Pak Budi") — nilai yang cocok
# pola ini tidak pernah dicetak ulang apa adanya, dipakai oleh fungsi
# penyaring tunggal `_nilai_aman_ditampilkan`.
POLA_SAPAAN_NAMA = re.compile(
    r"\b(bu|pak|ibu|bapak|sdr|sdri|tn|ny|nyonya|tuan|mr|mrs|ms)\.?\s+[a-z]+",
    re.IGNORECASE,
)
# Pola inisial (mis. "S.A.", "S. A.", "A.B.C.") — 1-4 huruf bertitik.
POLA_INISIAL = re.compile(r"^([A-Za-z]\.\s?){1,4}$")
# Pola kode diagnosis ICD-10 (mis. "J06", "K02.1") — huruf + 2 digit +
# opsional titik-desimal. Sudah tertangkap juga oleh aturan "tanpa digit",
# tapi dicek eksplisit sesuai permintaan uji, dan dijaga tetap benar bila
# aturan digit lain berubah di masa depan.
POLA_ICD = re.compile(r"^[A-Za-z]\d{2}(\.\d+)?$")
# Jumlah maksimum nilai unik yang boleh dicetak individual per kolom
# kategori (status/poli/penjamin) — sisanya digabung jadi agregat.
MAKS_NILAI_UNIK_TAMPIL = 20
# B2-sisa (k-anonimitas sederhana): nilai kategori hanya dicetak individual
# bila muncul di sekurang-kurangnya sekian baris. Nilai yang muncul 1-2
# kali kemungkinan besar salah isi atau data satu pasien saja (mis. nama,
# inisial, email yang nyasar ke kolom status/poli/penjamin), bukan
# kategori asli — kategori asli klinik (mis. "Reschedule", "Rujuk")
# biasanya muncul berulang. Bisa diatur (mis. via impor modul untuk
# klinik dengan volume data sangat kecil), tapi default aman untuk
# ekspor harian/mingguan klinik.
MIN_FREKUENSI_TAMPIL = 3

BULAN = {
    "jan": 1, "januari": 1, "january": 1,
    "feb": 2, "februari": 2, "february": 2, "peb": 2, "pebruari": 2,
    "mar": 3, "maret": 3, "march": 3,
    "apr": 4, "april": 4,
    "mei": 5, "may": 5,
    "jun": 6, "juni": 6, "june": 6,
    "jul": 7, "juli": 7, "july": 7,
    "agu": 8, "agt": 8, "agus": 8, "agustus": 8, "aug": 8, "august": 8,
    "sep": 9, "sept": 9, "september": 9,
    "okt": 10, "oktober": 10, "oct": 10, "october": 10,
    "nov": 11, "nop": 11, "november": 11, "nopember": 11,
    "des": 12, "desember": 12, "dec": 12, "december": 12,
}

POLA_ISO = re.compile(r"^(\d{4})[-/.](\d{1,2})[-/.](\d{1,2})$")
POLA_ANGKA_3 = re.compile(r"^(\d{1,2})[-/.](\d{1,2})[-/.](\d{2}|\d{4})$")
POLA_NAMA_BULAN = re.compile(r"^(\d{1,2})[\s\-/]+([A-Za-z]+)\.?[\s\-/,]+(\d{2}|\d{4})$")
# Memisahkan "tanggal[ T]jam" mis. "2026-09-01 08:15", "2026-09-01T08:15:00".
POLA_PISAH_JAM = re.compile(r"^(.*?)[ T](\d{1,2}[:.]\d{2}(?::\d{2})?)$")


class DataError(Exception):
    pass


def _normalisasi_header(h: str) -> str:
    return " ".join(h.strip().lower().split())


def _normalisasi_teks(t: str) -> str:
    """Huruf kecil, tanda baca umum dibuang, spasi dirapikan — untuk cocokkan status."""
    t = (t or "").strip().lower()
    t = re.sub(r"[._\-/]", " ", t)
    t = re.sub(r"\s+", " ", t).strip()
    return t


def _cari_kolom(header_asli: list, alias: list) -> "str | None":
    norm = {_normalisasi_header(h): h for h in header_asli}
    for a in alias:
        if a in norm:
            return norm[a]
    return None


def _kolom_sensitif_di_header(header: list, kolom_dipakai: set) -> list:
    """R10: cocokkan pola sensitif per token (word boundary), dan jangan
    pernah laporkan kolom yang benar-benar dipakai skill (tanggal, jam,
    poli, penjamin, status) sebagai kolom sensitif."""
    hasil = []
    for h in header:
        if h in kolom_dipakai:
            continue
        hn = _normalisasi_header(h)
        if any(p.search(hn) for p in POLA_KOLOM_SENSITIF_REGEX):
            hasil.append(h)
    return sorted(set(hasil))


# ---------------------------------------------------------------------------
# Tanggal & jam
# ---------------------------------------------------------------------------

def _tahun(t) -> int:
    t = int(t)
    return t + 2000 if t < 100 else t


def _buat_tanggal(y: int, m: int, d: int):
    try:
        return date(y, m, d)
    except ValueError:
        return None


def _pisah_tanggal_jam(teks: str):
    """Pisahkan teks tanggal dari jam bila digabung ('2026-09-01 08:15')."""
    teks = teks.strip()
    m = POLA_PISAH_JAM.match(teks)
    if m:
        return m.group(1).strip(), m.group(2).replace(".", ":")
    return teks, None


def deteksi_urutan(teks_tanggal_list, indeks_diabaikan=None):
    """Tentukan urutan tanggal angka ('dmy'/Indonesia atau 'mdy'/AS) untuk
    SATU FILE dari bukti tak ambigu (angka > 12 hanya mungkin di posisi
    hari). Mengembalikan (urutan_mayoritas, jumlah_bukti_dmy,
    jumlah_bukti_mdy, total_baris_berpola_angka, baris_bertentangan) —
    `total_baris_berpola_angka` = jumlah baris bertanggal angka a/b/tahun
    (ambigu maupun tidak), dipakai untuk mendeteksi file yang SAMA SEKALI
    tidak punya bukti (R12). `baris_bertentangan` berisi index (1-based,
    termasuk header) baris yang bukti lokalnya berlawanan dengan urutan
    mayoritas. `indeks_diabaikan` (opsional, set index 1-based termasuk
    header) melewati baris yang bergeser kolomnya (lihat B2-sisa butir 3)
    supaya tidak ikut jadi "bukti" format tanggal yang sebenarnya rusak.
    """
    indeks_diabaikan = indeks_diabaikan or set()
    bukti_dmy = []   # list index baris
    bukti_mdy = []
    total_pola_angka = 0
    for i, teks in enumerate(teks_tanggal_list, start=2):  # baris data dimulai setelah header
        if i in indeks_diabaikan:
            continue
        bagian_tanggal, _ = _pisah_tanggal_jam((teks or "").strip())
        m = POLA_ANGKA_3.match(bagian_tanggal)
        if not m:
            continue
        total_pola_angka += 1
        a, b = int(m.group(1)), int(m.group(2))
        if a > 12:
            bukti_dmy.append(i)
        elif b > 12:
            bukti_mdy.append(i)

    if len(bukti_dmy) >= len(bukti_mdy):
        mayoritas = "dmy"
        bertentangan = bukti_mdy
    else:
        mayoritas = "mdy"
        bertentangan = bukti_dmy

    return mayoritas, len(bukti_dmy), len(bukti_mdy), total_pola_angka, bertentangan


def parse_tanggal(teks: str, urutan_default: str = "dmy"):
    """Parse satu nilai tanggal (boleh mengandung jam sekaligus).

    Mendukung ISO (yyyy-mm-dd), angka a/b/tahun sesuai `urutan_default`
    KECUALI bila salah satu angka > 12 (maka urutan itu dipakai apa pun
    `urutan_default`, karena tak ambigu), dan nama bulan ID/EN
    ("2 Sept 2026", "1 September 2026", "1-Sep-2026").
    Mengembalikan (tanggal_atau_None, jam_atau_None_dari_bagian_waktu).
    """
    if not teks:
        return None, None
    bagian_tanggal, jam_teks = _pisah_tanggal_jam(teks.strip())
    jam = _parse_jam(jam_teks) if jam_teks else None

    m = POLA_ISO.match(bagian_tanggal)
    if m:
        return _buat_tanggal(int(m.group(1)), int(m.group(2)), int(m.group(3))), jam

    m = POLA_ANGKA_3.match(bagian_tanggal)
    if m:
        a, b, y = int(m.group(1)), int(m.group(2)), _tahun(m.group(3))
        if a > 12:
            d, bl = a, b
        elif b > 12:
            d, bl = b, a
        else:
            d, bl = (a, b) if urutan_default == "dmy" else (b, a)
        return _buat_tanggal(y, bl, d), jam

    m = POLA_NAMA_BULAN.match(bagian_tanggal)
    if m:
        bl = BULAN.get(m.group(2).lower().rstrip("."))
        if bl:
            return _buat_tanggal(_tahun(m.group(3)), bl, int(m.group(1))), jam

    return None, jam


def _parse_jam(teks: str):
    teks = (teks or "").strip()
    if not teks:
        return None
    teks = teks.replace(".", ":")
    for fmt in ("%H:%M", "%H:%M:%S"):
        try:
            return datetime.strptime(teks, fmt).hour
        except ValueError:
            continue
    return None


# ---------------------------------------------------------------------------
# Status kehadiran
# ---------------------------------------------------------------------------

def klasifikasi_status(nilai_asli: str) -> str:
    """Kembalikan 'hadir', 'tidak_datang', 'kosong', atau 'tidak_dikenal'."""
    n = _normalisasi_teks(nilai_asli)
    if not n:
        return "kosong"
    if n in SINGKATAN_TIDAK_DATANG:
        return "tidak_datang"
    if n in SINGKATAN_HADIR:
        return "hadir"
    if any(k in n for k in KATA_TIDAK_DATANG):
        return "tidak_datang"
    if any(k in n for k in KATA_HADIR):
        return "hadir"
    return "tidak_dikenal"


# ---------------------------------------------------------------------------
# B2: penyaring TUNGGAL nilai kategori aman-ditampilkan (status/poli/penjamin)
# ---------------------------------------------------------------------------

def _nilai_aman_ditampilkan(nilai: str) -> bool:
    """True bila SATU nilai kategori (status/poli/penjamin) aman dicetak
    ulang apa adanya berdasarkan POLANYA SAJA (belum menghitung syarat
    frekuensi — itu ada di `_pisah_aman_dan_sembunyikan`): tanpa digit,
    tanpa "@", maksimal 3 kata, dan tidak cocok pola inisial ("S.A."),
    kode ICD ("J06"), atau sapaan+nama ("Bu Ani", "Pak Budi"). Dipakai
    untuk SEMUA jalur output lewat `_pisah_aman_dan_sembunyikan` — satu
    fungsi, satu aturan, supaya tidak ada jalur yang lupa menyaring
    (lihat B2)."""
    n = (nilai or "").strip()
    if not n:
        return True  # nilai kosong direpresentasikan terpisah ("(kosong)"/"(tidak diisi)"), aman
    if "@" in n:
        return False
    if re.search(r"\d", n):
        return False
    if len(n.split()) > 3:
        return False
    if POLA_INISIAL.match(n):
        return False
    if POLA_ICD.match(n):
        return False
    if POLA_SAPAAN_NAMA.search(n):
        return False
    return True


def _pisah_aman_dan_sembunyikan(counter: Counter, ambang_frekuensi: int = MIN_FREKUENSI_TAMPIL):
    """Pisahkan isi sebuah Counter nilai->jumlah menjadi:
    - daftar nilai AMAN (lolos `_nilai_aman_ditampilkan` DAN muncul di
      sekurang-kurangnya `ambang_frekuensi` baris — k-anonimitas
      sederhana, lihat B2-sisa — dibatasi `MAKS_NILAI_UNIK_TAMPIL` nilai
      unik pertama berdasarkan frekuensi),
    - jumlah baris yang nilainya disembunyikan,
    - jumlah nilai unik berbeda yang disembunyikan.
    Nilai yang disembunyikan TIDAK PERNAH muncul di hasil apa pun (B2) —
    hanya dua angka agregat di atas yang dilaporkan. Nilai kosong ("")
    selalu dianggap "aman secara pola" tapi TETAP tunduk pada ambang
    frekuensi seperti nilai lain (representasinya, mis. "(tidak diisi)",
    sudah bukan string kosong lagi saat masuk Counter ini).
    """
    aman = []
    baris_disembunyikan = 0
    kategori_disembunyikan = 0
    for nilai, jumlah in counter.most_common():
        if (
            len(aman) < MAKS_NILAI_UNIK_TAMPIL
            and jumlah >= ambang_frekuensi
            and _nilai_aman_ditampilkan(nilai)
        ):
            aman.append((nilai, jumlah))
        else:
            baris_disembunyikan += jumlah
            kategori_disembunyikan += 1
    return aman, baris_disembunyikan, kategori_disembunyikan


# ---------------------------------------------------------------------------
# Baca file (deteksi encoding, S1 & R9)
# ---------------------------------------------------------------------------

def _decode_bytes(mentah: bytes):
    if mentah.startswith(b"\xff\xfe") or mentah.startswith(b"\xfe\xff"):
        try:
            return mentah.decode("utf-16"), "utf-16"
        except UnicodeDecodeError:
            pass
    if mentah.startswith(b"\xef\xbb\xbf"):
        try:
            return mentah.decode("utf-8-sig"), "utf-8-sig"
        except UnicodeDecodeError:
            pass
    # R9: UTF-16 TANPA BOM — banyak byte NUL (\x00) berselang-seling adalah
    # ciri khas teks ASCII/Latin yang dikodekan UTF-16. Tentukan endian dari
    # posisi byte NUL pada karakter pertama (LE: byte tinggi/NUL ada di
    # posisi genap setelah karakter; BE: NUL di posisi ganjil sebelum
    # karakter) alih-alih menebak — supaya tidak salah pilih LE/BE yang
    # sama-sama "berhasil" didekode tapi hasilnya kacau, dan pesan error
    # tidak menyesatkan ("kolom tanggal tidak ditemukan").
    contoh = mentah[:4096]
    if contoh and (contoh.count(b"\x00") / len(contoh)) > 0.2:
        if len(mentah) >= 2 and mentah[0] != 0 and mentah[1] == 0:
            urutan_coba = ("utf-16-le", "utf-16-be")
        elif len(mentah) >= 2 and mentah[0] == 0 and mentah[1] != 0:
            urutan_coba = ("utf-16-be", "utf-16-le")
        else:
            urutan_coba = ("utf-16-le", "utf-16-be")
        for enc in urutan_coba:
            try:
                return mentah.decode(enc), enc
            except UnicodeDecodeError:
                continue
    for enc in ("utf-8", "cp1252", "latin-1"):
        try:
            return mentah.decode(enc), enc
        except UnicodeDecodeError:
            continue
    raise DataError(
        "Encoding file tidak dikenali. Buka file di Excel/LibreOffice lalu "
        "simpan ulang sebagai 'CSV UTF-8 (Comma delimited)'."
    )


def baca_csv(path_or_text: str, is_text: bool = False):
    if is_text:
        teks = path_or_text
    else:
        try:
            with open(path_or_text, "rb") as f:
                mentah = f.read()
        except FileNotFoundError:
            raise DataError(f"File tidak ditemukan: {path_or_text}")
        except OSError as e:
            raise DataError(f"Gagal membuka file: {e}")
        teks = _decode_bytes(mentah)[0]

    contoh = teks[:4096]
    try:
        dialect = csv.Sniffer().sniff(contoh, delimiters=",;\t|")
    except csv.Error:
        dialect = csv.excel
    reader = csv.DictReader(io.StringIO(teks), dialect=dialect)
    baris = [row for row in reader]
    header = reader.fieldnames or []
    if not header:
        raise DataError("File CSV kosong atau tidak punya baris header.")
    return header, baris


# ---------------------------------------------------------------------------
# Rekap
# ---------------------------------------------------------------------------

def _persen(bagian: int, total: int) -> float:
    if total <= 0:
        return 0.0
    nilai = Decimal(bagian) / Decimal(total) * Decimal(100)
    return float(nilai.quantize(Decimal("0.1"), rounding=ROUND_HALF_UP))


def _baris_bergeser(row: dict, header: list) -> bool:
    """True bila jumlah kolom baris ini TIDAK COCOK dengan header dengan
    cara yang BERISI DATA (bukan sekadar pemisah kosong di ujung baris) —
    mis. ekspor CSV dengan koma tanpa tanda kutip yang menggeser semua
    nilai satu kolom ke kanan/kiri. `csv.DictReader` menaruh nilai kolom
    lebih di bawah kunci `None` (list) bila baris kepanjangan, dan mengisi
    `None` untuk kolom yang hilang bila baris kependekan.

    Dua pengecualian (S5, ditemukan penguji independen di v1.0.3) supaya
    file dengan pemisah di ujung SETIAP baris (mis. ';' penutup yang tidak
    ada di header) tidak salah dianggap "bergeser" padahal datanya utuh:
    - Kolom lebih (`None`): bila SEMUA nilai ekstra itu string kosong,
      ini cuma pemisah penutup tanpa isi — bukan pergeseran.
    - Kolom kurang: bila HANYA kolom TERAKHIR di header yang bernilai
      `None` (satu kolom saja, di ujung), ini biasanya kolom kosong yang
      pemisah penutupnya dihilangkan saat ekspor — bukan pergeseran.
    Baris yang tetap dianggap bergeser TIDAK BOLEH ditebak kolomnya;
    dikeluarkan dari rincian per hari/poli/penjamin/status (lihat B2-sisa
    butir 3), hanya dihitung di total pendaftaran dengan peringatan."""
    kelebihan = row.get(None)
    if kelebihan is not None:
        if not all((v or "").strip() == "" for v in kelebihan):
            return True
    kolom_kurang = [k for k in header if row.get(k) is None]
    if not kolom_kurang:
        return False
    if len(kolom_kurang) == 1 and header and kolom_kurang[0] == header[-1]:
        return False
    return True


def rekap(header: list, baris: list, urutan_tanggal_paksa: str = "auto") -> dict:
    if not baris:
        raise DataError(
            "File tidak berisi baris data (hanya header). "
            "Cek apakah file ekspor sudah benar."
        )

    kolom_tanggal = _cari_kolom(header, ALIAS_TANGGAL)
    kolom_jam = _cari_kolom(header, ALIAS_JAM)
    kolom_poli = _cari_kolom(header, ALIAS_POLI)
    kolom_penjamin = _cari_kolom(header, ALIAS_PENJAMIN)
    kolom_status = _cari_kolom(header, ALIAS_STATUS)

    if not kolom_tanggal:
        raise DataError(
            "Tidak menemukan kolom tanggal (dicoba: "
            + ", ".join(ALIAS_TANGGAL)
            + "). Beri nama kolom tanggal kunjungan, mis. 'Tanggal'."
        )

    kolom_dipakai = {
        k for k in (kolom_tanggal, kolom_jam, kolom_poli, kolom_penjamin, kolom_status) if k
    }
    kolom_sensitif_terpakai = _kolom_sensitif_di_header(header, kolom_dipakai)

    # --- B2-sisa butir 3: baris yang jumlah kolomnya bergeser dari header ---
    # dideteksi dulu, supaya baris itu (a) tidak ikut jadi bukti format
    # tanggal, dan (b) dikeluarkan dari rincian per hari/poli/penjamin/status.
    indeks_bergeser = [
        i for i, row in enumerate(baris, start=2) if _baris_bergeser(row, header)
    ]
    set_bergeser = set(indeks_bergeser)
    peringatan_bergeser = None
    if indeks_bergeser:
        if len(indeks_bergeser) > 0.5 * len(baris):
            # S5: mayoritas baris "bergeser" biasanya berarti masalah
            # STRUKTUR (pemisah kolom salah, atau setiap baris punya
            # pemisah tambahan di ujung) — bukan beberapa baris rusak
            # satu-satu. Pesan diarahkan ke perbaikan struktur, bukan
            # daftar nomor baris yang bisa mencapai ratusan.
            peringatan_bergeser = (
                "Struktur header dan baris tidak cocok — periksa pemisah kolom/ekspor CSV-nya "
                f"({len(indeks_bergeser)} dari {len(baris)} baris tidak cocok header, jauh lebih "
                "dari beberapa baris rusak). Kemungkinan pemisah kolomnya salah (mis. file ';' "
                "dibaca sebagai ',', atau sebaliknya), atau setiap baris punya pemisah tambahan "
                "di ujung yang tidak ada di baris header. Perbaiki file aslinya lalu jalankan "
                "ulang — rekap ini TIDAK bisa diandalkan sampai itu diperbaiki."
            )
        else:
            contoh_b = ", ".join(str(i) for i in indeks_bergeser[:8])
            lebih_b = (
                "" if len(indeks_bergeser) <= 8 else f" (+{len(indeks_bergeser) - 8} baris lain)"
            )
            peringatan_bergeser = (
                f"{len(indeks_bergeser)} baris jumlah kolomnya tidak cocok dengan header "
                "(kemungkinan ada koma tanpa tanda kutip di salah satu nilai, sehingga semua "
                "nilai di baris itu bergeser kolom) — baris bernomor "
                f"{contoh_b}{lebih_b}. Baris ini TETAP dihitung di total pendaftaran, tapi "
                "DIKELUARKAN dari rincian per hari/poli/penjamin/status karena script tidak "
                "bisa menebak kolom mana yang benar. Mohon cek & perbaiki file aslinya."
            )

    # --- tentukan urutan tanggal SEKALI untuk seluruh file (B1b, R12) ---
    peringatan_tanggal = None
    if urutan_tanggal_paksa in ("dmy", "mdy"):
        urutan = urutan_tanggal_paksa
        peringatan_tanggal = (
            f"Urutan tanggal dipaksa manual ke '{urutan}' lewat --urutan-tanggal "
            "(deteksi otomatis tidak dijalankan)."
        )
    else:
        urutan, n_dmy, n_mdy, total_pola_angka, baris_format_bertentangan = deteksi_urutan(
            [row.get(kolom_tanggal, "") for row in baris], indeks_diabaikan=set_bergeser
        )
        if n_dmy > 0 and n_mdy > 0:
            contoh = ", ".join(str(i) for i in baris_format_bertentangan[:8])
            lebih = (
                "" if len(baris_format_bertentangan) <= 8
                else f" (+{len(baris_format_bertentangan) - 8} baris lain)"
            )
            peringatan_tanggal = (
                f"Format tanggal tidak konsisten dalam satu file: {n_dmy} baris bergaya "
                f"Indonesia (hari/bulan), {n_mdy} baris bergaya Amerika (bulan/hari). "
                f"Baris ambigu diproses memakai format mayoritas ('{urutan}'); baris "
                f"bernomor {contoh}{lebih} punya bukti format berbeda dan sudah dibaca "
                "sesuai buktinya sendiri — mohon cek ulang baris tersebut."
            )
        elif n_dmy == 0 and n_mdy == 0 and total_pola_angka > 0:
            # R12: tidak ada bukti tegas sama sekali (semua hari & bulan <= 12) —
            # jangan diam-diam pakai dmy tanpa memberi tahu ini cuma asumsi.
            peringatan_tanggal = (
                f"Tidak ada bukti tegas urutan tanggal di file ini (semua nilai hari & "
                f"bulan pada {total_pola_angka} baris ≤ 12, bisa dibaca dua cara). "
                f"Diasumsikan format Indonesia (hari/bulan) — hasil ini BISA SALAH bila "
                "file sebenarnya bergaya Amerika (bulan/hari). Untuk memastikan, jalankan "
                "ulang dengan tambahan '--urutan-tanggal mdy' dan bandingkan hasilnya."
            )

    per_hari = Counter()
    per_poli = Counter()
    per_penjamin = Counter()
    per_jam = Counter()
    status_unik = Counter()          # nilai ASLI -> jumlah
    status_kategori = {}             # nilai ASLI -> kategori
    hadir = tidak_datang = tidak_dikenal_n = kosong_n = 0
    baris_tanggal_gagal = 0
    total = 0
    ada_sumber_jam = bool(kolom_jam)

    for i, row in enumerate(baris, start=2):
        total += 1
        if i in set_bergeser:
            # Jangan menebak kolom mana yang benar — lewati sepenuhnya dari
            # semua rincian (per hari/poli/penjamin/status/jam), tapi tetap
            # terhitung di total_pendaftaran (sudah +1 di atas).
            continue
        t, jam_dari_tanggal = parse_tanggal(row.get(kolom_tanggal, ""), urutan)
        if t is None:
            baris_tanggal_gagal += 1
        else:
            per_hari[t.isoformat()] += 1

        if kolom_poli:
            nilai = (row.get(kolom_poli) or "").strip() or "(tidak diisi)"
            per_poli[nilai] += 1
        if kolom_penjamin:
            nilai = (row.get(kolom_penjamin) or "").strip() or "(tidak diisi)"
            per_penjamin[nilai] += 1

        jam = None
        if kolom_jam:
            jam = _parse_jam(row.get(kolom_jam, ""))
        elif jam_dari_tanggal is not None:
            jam = jam_dari_tanggal
            ada_sumber_jam = True
        if jam is not None:
            per_jam[jam] += 1

        if kolom_status:
            nilai_status = (row.get(kolom_status) or "").strip()
            kategori = klasifikasi_status(nilai_status)
            kunci = nilai_status if nilai_status else "(kosong)"
            status_unik[kunci] += 1
            status_kategori[kunci] = kategori
            if kategori == "hadir":
                hadir += 1
            elif kategori == "tidak_datang":
                tidak_datang += 1
            elif kategori == "kosong":
                kosong_n += 1
            else:
                tidak_dikenal_n += 1

    jam_ramai = per_jam.most_common(3)

    # B2: saring SEMUA nilai kategori lewat SATU fungsi sebelum ditampilkan.
    poli_aman, poli_baris_sembunyi, poli_kategori_sembunyi = _pisah_aman_dan_sembunyikan(per_poli)
    penjamin_aman, penjamin_baris_sembunyi, penjamin_kategori_sembunyi = _pisah_aman_dan_sembunyikan(per_penjamin)

    status_rincian = None
    status_baris_sembunyi = status_kategori_sembunyi = 0
    if kolom_status:
        status_aman, status_baris_sembunyi, status_kategori_sembunyi = _pisah_aman_dan_sembunyikan(status_unik)
        status_rincian = [
            {"nilai": nilai, "jumlah": jumlah, "kategori": status_kategori[nilai]}
            for nilai, jumlah in status_aman
        ]

    total_dapat_dibaca = total - len(indeks_bergeser)

    hasil = {
        "total_pendaftaran": total,
        "total_baris": total,
        "total_dapat_dibaca": total_dapat_dibaca,
        "baris_bergeser_jumlah": len(indeks_bergeser),
        "peringatan_baris_bergeser": peringatan_bergeser,
        "urutan_tanggal_dipakai": urutan,
        "peringatan_format_tanggal": peringatan_tanggal,
        "baris_tanggal_tidak_terbaca": baris_tanggal_gagal,
        "per_hari": dict(sorted(per_hari.items())),
        "per_poli": dict(poli_aman) if kolom_poli else None,
        "per_penjamin": dict(penjamin_aman) if kolom_penjamin else None,
        "jam_ramai": (
            [{"jam": f"{j:02d}:00", "jumlah": n} for j, n in jam_ramai]
            if ada_sumber_jam else None
        ),
        "kolom_sensitif_diabaikan": kolom_sensitif_terpakai,
        "nilai_disembunyikan": {
            "poli": (
                {"baris": poli_baris_sembunyi, "nilai_berbeda": poli_kategori_sembunyi}
                if kolom_poli else None
            ),
            "penjamin": (
                {"baris": penjamin_baris_sembunyi, "nilai_berbeda": penjamin_kategori_sembunyi}
                if kolom_penjamin else None
            ),
            "status": (
                {"baris": status_baris_sembunyi, "nilai_berbeda": status_kategori_sembunyi}
                if kolom_status else None
            ),
        },
    }

    if kolom_status:
        hasil["status_rincian"] = status_rincian
        hasil["hadir"] = hadir
        hasil["tidak_datang"] = tidak_datang
        hasil["status_tidak_dikenal_jumlah"] = tidak_dikenal_n
        hasil["status_kosong_jumlah"] = kosong_n
        hasil["persentase_hadir"] = _persen(hadir, total_dapat_dibaca)
        hasil["persentase_tidak_datang"] = _persen(tidak_datang, total_dapat_dibaca)
        hasil["persentase_tidak_dikenal"] = _persen(tidak_dikenal_n, total_dapat_dibaca)
        hasil["catatan_pembulatan"] = (
            "Persentase dibulatkan 1 desimal (round half up), dihitung dari baris yang "
            "kolomnya bisa dibaca" + (
                f" ({total_dapat_dibaca} dari {total} baris, {len(indeks_bergeser)} baris "
                "bergeser dikeluarkan)" if indeks_bergeser else ""
            ) + "."
        )
    else:
        hasil["status_rincian"] = None
        hasil["hadir"] = None
        hasil["tidak_datang"] = None
        hasil["status_tidak_dikenal_jumlah"] = None
        hasil["status_kosong_jumlah"] = None
        hasil["persentase_hadir"] = None
        hasil["persentase_tidak_datang"] = None
        hasil["persentase_tidak_dikenal"] = None
        hasil["catatan_pembulatan"] = None

    return hasil


def _format_daftar_kategori(judul: str, aman_dict: dict, sembunyi: dict, total: int) -> list:
    """R13: cetak daftar nilai aman + persentase, lalu satu baris agregat
    untuk nilai yang disembunyikan (bila ada) — TANPA pernah mencetak nilai
    yang disembunyikan itu sendiri (B2)."""
    baris = ["", judul]
    if aman_dict:
        for nama, n in aman_dict.items():
            persen = f" ({_persen(n, total)}%)" if total else ""
            baris.append(f"  {nama}: {n}{persen}")
    else:
        baris.append("  (tidak ada nilai yang aman ditampilkan)")
    if sembunyi and sembunyi.get("baris"):
        baris.append(
            f"  (nilai lain disembunyikan demi privasi): {sembunyi['baris']} baris, "
            f"{sembunyi['nilai_berbeda']} nilai berbeda — kemungkinan teks bebas "
            "(bisa memuat nama/kontak), periksa data asli bila perlu"
        )
    return baris


def format_teks(hasil: dict) -> str:
    baris = []
    baris.append("REKAP OPERASIONAL KUNJUNGAN (agregat, tanpa nama/diagnosis)")
    baris.append(f"Total pendaftaran tercatat: {hasil['total_pendaftaran']}")
    if hasil.get("peringatan_baris_bergeser"):
        baris.append(f"⚠️  {hasil['peringatan_baris_bergeser']}")
    if hasil["baris_tanggal_tidak_terbaca"]:
        baris.append(
            f"⚠️  {hasil['baris_tanggal_tidak_terbaca']} baris tanggalnya tidak terbaca "
            "dan tidak dihitung di rekap per hari."
        )
    if hasil.get("peringatan_format_tanggal"):
        baris.append(f"⚠️  {hasil['peringatan_format_tanggal']}")

    tidak_ada_baris_terbaca = hasil.get("total_dapat_dibaca") == 0
    if tidak_ada_baris_terbaca:
        baris.append(
            "⚠️  Tidak ada baris yang bisa dibaca dari file ini (semua baris bermasalah "
            "strukturnya — lihat peringatan di atas). Rekap TIDAK berisi data yang bisa "
            "diandalkan; perbaiki file aslinya dulu sebelum dipakai."
        )

    nilai_disembunyikan = hasil.get("nilai_disembunyikan") or {}

    if hasil["hadir"] is not None:
        baris.append("")
        if tidak_ada_baris_terbaca:
            baris.append("(tidak ada baris yang bisa dibaca untuk dihitung status kehadirannya)")
        else:
            baris.append(
                f"Hadir: {hasil['hadir']} ({hasil['persentase_hadir']}%) — "
                f"Tidak datang: {hasil['tidak_datang']} ({hasil['persentase_tidak_datang']}%)"
            )
        if hasil["status_tidak_dikenal_jumlah"]:
            baris.append(
                f"⚠️  Status TIDAK DIKENAL (bukan hadir, bukan tidak-datang — belum "
                f"dihitung ke keduanya, mohon cek manual): {hasil['status_tidak_dikenal_jumlah']} "
                f"baris ({hasil['persentase_tidak_dikenal']}%)"
            )
        if hasil["status_kosong_jumlah"]:
            baris.append(f"⚠️  Status kosong (tidak diisi): {hasil['status_kosong_jumlah']} baris")
        baris.append("")
        baris.append("Rincian nilai status yang ditemukan (cek klasifikasinya sudah benar):")
        for s in hasil["status_rincian"]:
            baris.append(f"  '{s['nilai']}' -> {s['kategori']} ({s['jumlah']} baris)")
        status_sembunyi = nilai_disembunyikan.get("status")
        if status_sembunyi and status_sembunyi.get("baris"):
            baris.append(
                f"  (nilai status lain disembunyikan demi privasi): "
                f"{status_sembunyi['baris']} baris, {status_sembunyi['nilai_berbeda']} nilai "
                "berbeda — kemungkinan berisi teks bebas (nama/no. HP/diagnosis), cek data asli"
            )

    baris.append("")
    baris.append("Kunjungan per hari:")
    if hasil["per_hari"]:
        for tgl, n in hasil["per_hari"].items():
            baris.append(f"  {tgl}: {n}")
    else:
        baris.append("  (tidak ada)")

    if hasil["per_poli"] is not None:
        baris.extend(_format_daftar_kategori(
            "Pendaftaran per poli/layanan:", hasil["per_poli"],
            nilai_disembunyikan.get("poli"), hasil["total_dapat_dibaca"],
        ))

    if hasil["per_penjamin"] is not None:
        baris.extend(_format_daftar_kategori(
            "Pendaftaran per penjamin/cara bayar:", hasil["per_penjamin"],
            nilai_disembunyikan.get("penjamin"), hasil["total_dapat_dibaca"],
        ))

    if hasil["jam_ramai"] is not None:
        baris.append("")
        baris.append("Jam paling ramai (top 3):")
        if hasil["jam_ramai"]:
            for j in hasil["jam_ramai"]:
                baris.append(f"  {j['jam']}: {j['jumlah']} kunjungan")
        else:
            baris.append("  (kolom jam ada tapi tidak ada nilai yang terbaca)")

    if hasil["kolom_sensitif_diabaikan"]:
        baris.append("")
        baris.append(
            "Catatan privasi: kolom berikut TIDAK dibaca isinya dan diabaikan demi "
            "kerahasiaan data pasien (UU PDP 27/2022; UU 17/2023 Ps. 301; PP 28/2024 Ps. 788-789): "
            + ", ".join(hasil["kolom_sensitif_diabaikan"])
        )

    if hasil.get("catatan_pembulatan"):
        baris.append("")
        baris.append(f"Catatan: {hasil['catatan_pembulatan']}")

    baris.append("")
    baris.append(
        "Catatan: ini rekap operasional (jumlah), bukan rekam medis, "
        "bukan alat skrining/diagnosis, dan tidak menampilkan data per-pasien. "
        "Cek hasil rekap di atas tidak memuat nama sebelum dikirim/dipublikasikan."
    )
    return "\n".join(baris)


def main(argv=None):
    ap = argparse.ArgumentParser(
        description="Rekap agregat kunjungan klinik dari CSV (tanpa nama/diagnosis di output)."
    )
    ap.add_argument("--file", required=True, help="Path file CSV ekspor kunjungan klinik.")
    ap.add_argument(
        "--format", choices=["teks", "json"], default="teks",
        help="Format output (default: teks).",
    )
    ap.add_argument(
        "--urutan-tanggal", choices=["auto", "dmy", "mdy"], default="auto",
        help="Urutan tanggal angka: dmy (hari/bulan/tahun, Indonesia) atau mdy (bulan/hari/tahun, "
             "AS). Default auto (deteksi dari isi file, lihat peringatan bila ambigu).",
    )
    args = ap.parse_args(argv)

    try:
        header, baris = baca_csv(args.file)
        hasil = rekap(header, baris, urutan_tanggal_paksa=args.urutan_tanggal)
    except DataError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    if args.format == "json":
        print(json.dumps(hasil, ensure_ascii=False, indent=2))
    else:
        print(format_teks(hasil))
    return 0


if __name__ == "__main__":
    sys.exit(main())
