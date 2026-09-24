#!/usr/bin/env python3
"""Rekap operasional kunjungan klinik dari file CSV — AGREGAT SAJA.

Tujuan: menghasilkan angka kunjungan per hari/poli/penjamin, jam ramai, dan
jumlah pasien tidak datang, TANPA pernah menampilkan data per-pasien
(nama, NIK, tanggal lahir, diagnosis, dll.) di output. Ini BUKAN alat rekam
medis dan BUKAN alat skrining/diagnosis — hanya rekap jumlah untuk laporan
operasional (lihat CLAUDE.md Komunitech & keputusan pemilik jalur 3, bidang
kesehatan: tanpa skrining/diagnosis/kalkulator medis).

Prinsip keandalan (v1.0.1, setelah uji independen):
- Status kehadiran diklasifikasikan dari daftar kata kunci "hadir" dan
  "tidak datang". Status yang TIDAK cocok dengan salah satu daftar
  DILAPORKAN sebagai "tidak dikenal" — tidak pernah diam-diam dihitung
  sebagai hadir.
- Format tanggal (hari/bulan vs bulan/hari) ditentukan SEKALI untuk seluruh
  file dari bukti tak ambigu di dalamnya (mis. tanggal > 12). Baris yang
  buktinya bertentangan dengan format mayoritas tetap dibaca memakai bukti
  lokalnya sendiri, tapi diberi peringatan agar pengguna mengecek.
- Semua angka agregat (total, hadir, tidak datang, persentase) dihitung
  eksplisit oleh script ini, bukan ditebak oleh agent.

Hanya memakai library standar Python (3.8+). Lintas OS (Windows/macOS/Linux).

Contoh pakai:
    python3 rekap_kunjungan.py --file kunjungan.csv
    python3 rekap_kunjungan.py --file kunjungan.csv --format json

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

# Pola nama/kata kolom yang mengandung data pribadi/klinis spesifik — kalau
# nama kolom mengandung salah satu pola ini, ISI kolom itu SENGAJA tidak
# pernah dibaca untuk ditampilkan (hanya nama kolomnya yang dilaporkan
# sebagai "diabaikan demi privasi pasien").
POLA_KOLOM_SENSITIF = [
    "nama", "nik", "ktp", "rm", "rekam medis", "bpjs", "diagnos", "diagnosa",
    "dx", "icd", "keluhan", "alamat", "telp", "telepon", "hp", "wa",
    "no. wa", "email", "lahir", "kontak", "ortu", "orang tua", "ibu",
    "ayah", "penanggung jawab", "asuransi no", "kartu",
]

# Alias nama kolom yang diterima (huruf kecil, tanpa spasi berlebih) untuk
# setiap kolom agregat yang DIPAKAI.
ALIAS_TANGGAL = ["tanggal", "tgl", "date", "tanggal kunjungan", "tanggal daftar"]
ALIAS_JAM = ["jam", "waktu", "jam kunjungan", "time"]
ALIAS_POLI = ["poli", "layanan", "unit", "poliklinik", "jenis layanan"]
ALIAS_PENJAMIN = ["penjamin", "pembayaran", "cara bayar", "jenis pasien", "kelas"]
ALIAS_STATUS = ["status", "status kunjungan", "status kehadiran", "keterangan"]

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


def _kolom_sensitif_di_header(header: list) -> list:
    hasil = []
    for h in header:
        hn = _normalisasi_header(h)
        if any(pola in hn for pola in POLA_KOLOM_SENSITIF):
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


def deteksi_urutan(teks_tanggal_list):
    """Tentukan urutan tanggal angka ('dmy'/Indonesia atau 'mdy'/AS) untuk
    SATU FILE dari bukti tak ambigu (angka > 12 hanya mungkin di posisi
    hari). Mengembalikan (urutan_mayoritas, jumlah_bukti_dmy,
    jumlah_bukti_mdy, baris_bertentangan) — baris_bertentangan berisi index
    (1-based, termasuk header) baris yang bukti lokalnya berlawanan dengan
    urutan mayoritas.
    """
    bukti_dmy = []   # list index baris
    bukti_mdy = []
    for i, teks in enumerate(teks_tanggal_list, start=2):  # baris data dimulai setelah header
        bagian_tanggal, _ = _pisah_tanggal_jam((teks or "").strip())
        m = POLA_ANGKA_3.match(bagian_tanggal)
        if not m:
            continue
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

    return mayoritas, len(bukti_dmy), len(bukti_mdy), bertentangan


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
# Baca file (deteksi encoding, S1)
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


def _teks_mencurigakan(nilai: str) -> bool:
    """Heuristik R2: teks bebas yang mungkin berisi nama orang, bukan
    kategori (mis. staf mengetik 'Cabut gigi FIKTIF Ani' di kolom poli)."""
    return len(nilai.split()) > 4


def rekap(header: list, baris: list) -> dict:
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

    kolom_sensitif_terpakai = _kolom_sensitif_di_header(header)

    # --- tentukan urutan tanggal SEKALI untuk seluruh file (B1b) ---
    urutan, n_dmy, n_mdy, baris_format_bertentangan = deteksi_urutan(
        [row.get(kolom_tanggal, "") for row in baris]
    )
    peringatan_tanggal = None
    if n_dmy > 0 and n_mdy > 0:
        contoh = ", ".join(str(i) for i in baris_format_bertentangan[:8])
        lebih = "" if len(baris_format_bertentangan) <= 8 else f" (+{len(baris_format_bertentangan) - 8} baris lain)"
        peringatan_tanggal = (
            f"Format tanggal tidak konsisten dalam satu file: {n_dmy} baris bergaya "
            f"Indonesia (hari/bulan), {n_mdy} baris bergaya Amerika (bulan/hari). "
            f"Baris ambigu diproses memakai format mayoritas ('{urutan}'); baris "
            f"bernomor {contoh}{lebih} punya bukti format berbeda dan sudah dibaca "
            "sesuai buktinya sendiri — mohon cek ulang baris tersebut."
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
    poli_mencurigakan = set()
    penjamin_mencurigakan = set()
    ada_sumber_jam = bool(kolom_jam)

    for row in baris:
        total += 1
        t, jam_dari_tanggal = parse_tanggal(row.get(kolom_tanggal, ""), urutan)
        if t is None:
            baris_tanggal_gagal += 1
        else:
            per_hari[t.isoformat()] += 1

        if kolom_poli:
            nilai = (row.get(kolom_poli) or "").strip() or "(tidak diisi)"
            per_poli[nilai] += 1
            if _teks_mencurigakan(nilai):
                poli_mencurigakan.add(nilai)
        if kolom_penjamin:
            nilai = (row.get(kolom_penjamin) or "").strip() or "(tidak diisi)"
            per_penjamin[nilai] += 1
            if _teks_mencurigakan(nilai):
                penjamin_mencurigakan.add(nilai)

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

    # R2: kolom dengan terlalu banyak nilai unik sering berarti teks bebas
    # (bisa memuat nama), bukan kategori tetap — beri peringatan terpisah.
    kolom_terlalu_beragam = []
    if kolom_poli and len(per_poli) > 20:
        kolom_terlalu_beragam.append(kolom_poli)
    if kolom_penjamin and len(per_penjamin) > 20:
        kolom_terlalu_beragam.append(kolom_penjamin)

    status_rincian = None
    if kolom_status:
        status_rincian = [
            {"nilai": k, "jumlah": v, "kategori": status_kategori[k]}
            for k, v in status_unik.most_common()
        ]

    hasil = {
        "total_pendaftaran": total,
        "total_baris": total,
        "urutan_tanggal_dipakai": urutan,
        "peringatan_format_tanggal": peringatan_tanggal,
        "baris_tanggal_tidak_terbaca": baris_tanggal_gagal,
        "per_hari": dict(sorted(per_hari.items())),
        "per_poli": dict(per_poli.most_common()) if kolom_poli else None,
        "per_penjamin": dict(per_penjamin.most_common()) if kolom_penjamin else None,
        "jam_ramai": (
            [{"jam": f"{j:02d}:00", "jumlah": n} for j, n in jam_ramai]
            if ada_sumber_jam else None
        ),
        "kolom_sensitif_diabaikan": kolom_sensitif_terpakai,
        "kolom_nilai_mencurigakan": {
            "poli": sorted(poli_mencurigakan),
            "penjamin": sorted(penjamin_mencurigakan),
        },
        "kolom_terlalu_beragam": kolom_terlalu_beragam,
    }

    if kolom_status:
        hasil["status_rincian"] = status_rincian
        hasil["hadir"] = hadir
        hasil["tidak_datang"] = tidak_datang
        hasil["status_tidak_dikenal_jumlah"] = tidak_dikenal_n
        hasil["status_kosong_jumlah"] = kosong_n
        hasil["persentase_hadir"] = _persen(hadir, total)
        hasil["persentase_tidak_datang"] = _persen(tidak_datang, total)
        hasil["persentase_tidak_dikenal"] = _persen(tidak_dikenal_n, total)
        hasil["catatan_pembulatan"] = "Persentase dibulatkan 1 desimal (round half up)."
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


def format_teks(hasil: dict) -> str:
    baris = []
    baris.append("REKAP OPERASIONAL KUNJUNGAN (agregat, tanpa nama/diagnosis)")
    baris.append(f"Total pendaftaran tercatat: {hasil['total_pendaftaran']}")
    if hasil["baris_tanggal_tidak_terbaca"]:
        baris.append(
            f"⚠️  {hasil['baris_tanggal_tidak_terbaca']} baris tanggalnya tidak terbaca "
            "dan tidak dihitung di rekap per hari."
        )
    if hasil.get("peringatan_format_tanggal"):
        baris.append(f"⚠️  {hasil['peringatan_format_tanggal']}")

    if hasil["hadir"] is not None:
        baris.append("")
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

    baris.append("")
    baris.append("Kunjungan per hari:")
    if hasil["per_hari"]:
        for tgl, n in hasil["per_hari"].items():
            baris.append(f"  {tgl}: {n}")
    else:
        baris.append("  (tidak ada)")

    if hasil["per_poli"] is not None:
        baris.append("")
        baris.append("Pendaftaran per poli/layanan:")
        for nama, n in hasil["per_poli"].items():
            baris.append(f"  {nama}: {n}")

    if hasil["per_penjamin"] is not None:
        baris.append("")
        baris.append("Pendaftaran per penjamin/cara bayar:")
        for nama, n in hasil["per_penjamin"].items():
            baris.append(f"  {nama}: {n}")

    if hasil["jam_ramai"] is not None:
        baris.append("")
        baris.append("Jam paling ramai (top 3):")
        if hasil["jam_ramai"]:
            for j in hasil["jam_ramai"]:
                baris.append(f"  {j['jam']}: {j['jumlah']} kunjungan")
        else:
            baris.append("  (kolom jam ada tapi tidak ada nilai yang terbaca)")

    mencurigakan = hasil.get("kolom_nilai_mencurigakan") or {}
    for label, kunci in (("poli/layanan", "poli"), ("penjamin/cara bayar", "penjamin")):
        nilai_curiga = mencurigakan.get(kunci) or []
        if nilai_curiga:
            baris.append("")
            baris.append(
                f"⚠️  Nilai di kolom {label} berisi lebih dari 4 kata — periksa apakah "
                "ini teks bebas yang mengandung nama pasien (jangan dikirim ke luar bila iya):"
            )
            for v in nilai_curiga:
                baris.append(f"  '{v}'")

    if hasil.get("kolom_terlalu_beragam"):
        baris.append("")
        baris.append(
            "⚠️  Kolom berikut punya lebih dari 20 nilai unik — kemungkinan diisi teks "
            "bebas (bukan kategori tetap), periksa apakah ini seharusnya kolom kategori: "
            + ", ".join(hasil["kolom_terlalu_beragam"])
        )

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
    args = ap.parse_args(argv)

    try:
        header, baris = baca_csv(args.file)
        hasil = rekap(header, baris)
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
