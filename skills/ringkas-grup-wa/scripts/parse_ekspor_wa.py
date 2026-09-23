#!/usr/bin/env python3
"""Mem-parsing ekspor chat WhatsApp (.txt atau .zip "Tanpa Media") menjadi JSON terstruktur.

Hanya memakai pustaka standar Python (3.8+). Mendukung format ekspor Android & iOS,
berbahasa Indonesia maupun Inggris, termasuk variasi umum:
  - Android: "12/09/26, 17.05 - Nama: pesan"  atau  "12/09/26 17.05 - Nama: pesan"
  - Android (EN, AM/PM): "9/12/26, 5:05 PM - Name: msg"
  - iOS:     "[12/09/26, 17.05.22] Nama: pesan"

Output: JSON ke stdout. Semua perhitungan (tanggal relatif, ambang waktu, statistik)
dilakukan lewat kode ini, bukan dikira-kira oleh model AI di atasnya.

Jalankan:
    python3 parse_ekspor_wa.py <file.txt|file.zip> [opsi]
    python3 parse_ekspor_wa.py --help

Windows: pakai `python` atau `py` bila `python3` tidak dikenali.
"""
import argparse
import io
import json
import re
import sys
import unicodedata
import zipfile
from datetime import date, datetime, timedelta

# ---------------------------------------------------------------------------
# Pembersihan teks
# ---------------------------------------------------------------------------

# Karakter tak terlihat yang sering disisipkan WhatsApp sebelum nama pengirim
# atau di awal baris (LRM U+200E, RLM U+200F, NBSP U+00A0, BOM U+FEFF, zero-width U+200B).
KARAKTER_TAK_TERLIHAT = re.compile("[‎‏ ﻿​]")


def bersihkan_baris(baris):
    baris = KARAKTER_TAK_TERLIHAT.sub(" ", baris)
    baris = baris.replace(" ", " ")
    baris = baris.rstrip("\r\n")
    return baris


# ---------------------------------------------------------------------------
# Pembacaan file (.txt / .zip)
# ---------------------------------------------------------------------------

ENCODING_DICOBA = ["utf-8-sig", "utf-8", "cp1252", "latin-1"]


def _decode(raw_bytes, nama_untuk_pesan):
    for enc in ENCODING_DICOBA:
        try:
            return raw_bytes.decode(enc)
        except (UnicodeDecodeError, LookupError):
            continue
    raise ValueError(
        f"tidak bisa membaca '{nama_untuk_pesan}': encoding tidak dikenali "
        f"(dicoba {', '.join(ENCODING_DICOBA)})"
    )


def baca_teks_ekspor(path):
    """Kembalikan (teks, nama_file_txt_asli). Menerima .txt langsung atau .zip berisi .txt."""
    try:
        with open(path, "rb") as f:
            data = f.read()
    except FileNotFoundError:
        raise ValueError(f"file tidak ditemukan: {path}")
    except OSError as e:
        raise ValueError(f"tidak bisa membuka file '{path}': {e}")

    if zipfile.is_zipfile(path):
        try:
            with zipfile.ZipFile(path) as zf:
                nama_txt = [n for n in zf.namelist() if n.lower().endswith(".txt")]
                if not nama_txt:
                    raise ValueError(f"'{path}' adalah ZIP tapi tidak berisi file .txt")
                # Prioritaskan nama yang mengandung "chat" (nama bawaan WhatsApp: _chat.txt)
                nama_txt.sort(key=lambda n: (0 if "chat" in n.lower() else 1, n))
                target = nama_txt[0]
                raw = zf.read(target)
        except zipfile.BadZipFile:
            raise ValueError(f"'{path}' rusak: bukan file ZIP yang valid")
        return _decode(raw, target), target

    if len(data) == 0:
        return "", path

    return _decode(raw_bytes=data, nama_untuk_pesan=path), path


# ---------------------------------------------------------------------------
# Pola baris pesan
# ---------------------------------------------------------------------------

# Tanggal: pemisah / . atau -, 1-2 digit hari&bulan, 2 atau 4 digit tahun.
_TANGGAL = r"(\d{1,2})[/.\-](\d{1,2})[/.\-](\d{2,4})"
# Waktu: HH.MM atau HH:MM, opsional detik, opsional AM/PM atau pagi/siang/sore/malam.
_WAKTU = r"(\d{1,2})[:.](\d{2})(?:[:.](\d{2}))?\s*([AaPp][Mm]|pagi|siang|sore|malam|dini\s*hari)?"

POLA_ANDROID = re.compile(
    rf"^\s*{_TANGGAL},?\s+{_WAKTU}\s*[-–]\s*(.*)$"
)
POLA_IOS = re.compile(
    rf"^\s*\[{_TANGGAL},?\s+{_WAKTU}\]\s*(.*)$"
)

POLA_PENGIRIM = re.compile(r"^([^:\n]{1,100}?):\s(.*)$", re.DOTALL)

PLACEHOLDER_MEDIA = {
    "<media omitted>", "<media tidak disertakan>", "media dihilangkan",
    "‎<media omitted>", "gambar dihilangkan", "image omitted", "video omitted",
    "video dihilangkan", "audio omitted", "audio dihilangkan", "gif omitted",
    "sticker omitted", "stiker dihilangkan", "dokumen dihilangkan", "document omitted",
    "kontak dihilangkan", "contact card omitted",
}
PLACEHOLDER_DIHAPUS = {
    "this message was deleted", "you deleted this message",
    "pesan ini dihapus", "anda menghapus pesan ini",
}

# Frasa sistem umum (ID & EN) yang tidak memakai "Nama:" tapi tetap satu baris pesan valid.
PENANDA_SISTEM = (
    "messages and calls are end-to-end encrypted", "pesan dan panggilan terenkripsi",
    "created group", "membuat grup", "changed the subject", "mengubah subjek",
    "added", "ditambahkan", "left", "keluar", "removed", "menghapus",
    "changed this group's icon", "mengubah ikon grup", "joined using", "bergabung menggunakan",
    "changed the group description", "mengubah deskripsi grup", "security code changed",
    "kode keamanan berubah", "missed voice call", "panggilan suara tidak terjawab",
    "missed video call", "panggilan video tidak terjawab", "changed their phone number",
    "mengganti nomor telepon", "turned on disappearing messages", "mengaktifkan pesan sekali lihat",
    "turned off disappearing messages", "menonaktifkan pesan sekali lihat",
)


def _jenis_pesan(sender, teks):
    t = teks.strip().lower()
    if t in PLACEHOLDER_MEDIA:
        return "media"
    if t in PLACEHOLDER_DIHAPUS:
        return "dihapus"
    if sender is None:
        return "sistem"
    return "obrolan"


def _pisah_pengirim(rest):
    """rest -> (pengirim atau None, teks). None berarti baris sistem (tanpa 'Nama:')."""
    m = POLA_PENGIRIM.match(rest)
    if not m:
        return None, rest
    calon_nama, teks = m.group(1).strip(), m.group(2)
    # Baris sistem kadang memuat ':' juga (jarang). Heuristik: nama sistem umumnya
    # panjang & memuat frasa penanda -> anggap bukan nama pengirim.
    rendah = rest.lower()
    if any(p in rendah for p in PENANDA_SISTEM) and len(calon_nama) > 40:
        return None, rest
    return calon_nama, teks


# ---------------------------------------------------------------------------
# Deteksi format tanggal (d/m vs m/d) & bahasa
# ---------------------------------------------------------------------------

def deteksi_urutan_tanggal(triple_list):
    """triple_list: list (a, b, tahun_str). Kembalikan ('d/m'|'m/d', catatan_list)."""
    catatan = []
    a_lebih_12 = any(int(a) > 12 for a, b, y in triple_list)
    b_lebih_12 = any(int(b) > 12 for a, b, y in triple_list)
    if a_lebih_12 and not b_lebih_12:
        return "d/m", catatan
    if b_lebih_12 and not a_lebih_12:
        return "m/d", catatan
    if a_lebih_12 and b_lebih_12:
        catatan.append(
            "Tanggal tidak konsisten (kedua posisi pernah > 12) — sebagian tanggal "
            "mungkin salah baca. Default dipakai: d/m (Indonesia)."
        )
        return "d/m", catatan
    catatan.append(
        "Urutan tanggal ambigu (hari & bulan sama-sama ≤ 12 di semua pesan). "
        "Default dipakai: d/m (Indonesia). Cek tanggal bila hasil terasa janggal."
    )
    return "d/m", catatan


def _tahun_lengkap(y):
    y = int(y)
    return y + 2000 if y < 100 else y


def buat_tanggal(a, b, y, urutan):
    tahun = _tahun_lengkap(y)
    hari, bulan = (int(a), int(b)) if urutan == "d/m" else (int(b), int(a))
    try:
        return date(tahun, bulan, hari)
    except ValueError:
        return None


_PERIODE_HARI = {"pagi": "am", "siang": "pm_awal", "sore": "pm", "malam": "pm_malam"}


def buat_waktu(jam, menit, detik, penanda):
    jam = int(jam)
    menit = int(menit)
    detik = int(detik) if detik else 0
    catatan = None
    if penanda:
        p = penanda.strip().lower().replace(" ", "")
        if p in ("am", "pm"):
            if p == "am":
                if jam == 12:
                    jam = 0
            else:  # pm
                if jam != 12:
                    jam += 12
        elif p in _PERIODE_HARI:
            kelas = _PERIODE_HARI[p]
            if kelas == "am":
                if jam == 12:
                    jam = 0
            elif kelas == "pm_awal":  # "siang": ~11.00-15.00
                if jam not in (12,) and jam < 12:
                    jam += 12
            elif kelas == "pm":  # "sore": ~15.00-19.00, tidak ada "12 sore"
                if jam < 12:
                    jam += 12
            else:  # "pm_malam" -> "malam": ~19.00-23.00; "12 malam" = tengah malam (00.00)
                if jam == 12:
                    jam = 0
                elif jam < 12:
                    jam += 12
            catatan = f"kata '{penanda.strip()}' ditafsirkan sebagai jam {jam:02d}"
    if not (0 <= jam <= 23 and 0 <= menit <= 59 and 0 <= detik <= 59):
        return None, "jam/menit di luar rentang wajar"
    return (jam, menit, detik), catatan


# ---------------------------------------------------------------------------
# Parser utama
# ---------------------------------------------------------------------------

def parse_pesan(teks):
    """Kembalikan (list pesan, format_terdeteksi, urutan_tanggal, catatan_list)."""
    baris_list = [bersihkan_baris(b) for b in teks.splitlines()]

    # Pass 1: cari semua kecocokan awal-pesan untuk menentukan format & urutan tanggal.
    kecocokan = []  # (index, format_tag, a, b, y, jam, menit, detik, penanda, rest)
    jumlah_android = 0
    jumlah_ios = 0
    for i, baris in enumerate(baris_list):
        m = POLA_IOS.match(baris)
        if m:
            jumlah_ios += 1
            a, b, y, jam, menit, detik, penanda, rest = m.groups()
            kecocokan.append((i, "ios", a, b, y, jam, menit, detik, penanda, rest))
            continue
        m = POLA_ANDROID.match(baris)
        if m:
            jumlah_android += 1
            a, b, y, jam, menit, detik, penanda, rest = m.groups()
            kecocokan.append((i, "android", a, b, y, jam, menit, detik, penanda, rest))

    catatan_global = []
    if not kecocokan:
        return [], None, None, [
            "Tidak ada baris pesan yang dikenali. File mungkin kosong, bukan ekspor "
            "chat WhatsApp, atau formatnya di luar variasi yang didukung."
        ]

    format_terdeteksi = "ios" if jumlah_ios >= jumlah_android else "android"
    urutan_tanggal, catatan_urutan = deteksi_urutan_tanggal([(a, b, y) for (_, _, a, b, y, *_r) in kecocokan])
    catatan_global += catatan_urutan

    # Pass 2: bangun pesan, menggabungkan baris lanjutan (multi-baris) ke pesan sebelumnya.
    pesan = []
    idx_pesan_terakhir = None
    posisi_cocok = {k[0]: k for k in kecocokan}
    for i, baris in enumerate(baris_list):
        if i in posisi_cocok:
            _, fmt, a, b, y, jam, menit, detik, penanda, rest = posisi_cocok[i]
            tgl = buat_tanggal(a, b, y, urutan_tanggal)
            wkt, catatan_waktu = buat_waktu(jam, menit, detik, penanda)
            if tgl is None or wkt is None:
                catatan_global.append(
                    f"Baris {i + 1}: tanggal/waktu tidak valid ('{baris.strip()[:60]}'), dilewati."
                )
                continue
            pengirim, isi = _pisah_pengirim(rest)
            jenis = _jenis_pesan(pengirim, isi)
            waktu_dt = datetime(tgl.year, tgl.month, tgl.day, *wkt)
            pesan.append({
                "waktu": waktu_dt.isoformat(),
                "pengirim": pengirim,
                "teks": isi,
                "jenis": jenis,
            })
            idx_pesan_terakhir = len(pesan) - 1
        else:
            if not baris.strip():
                continue
            if idx_pesan_terakhir is None:
                # Baris sebelum pesan pertama dikenali (mis. header aplikasi) -> abaikan.
                continue
            pesan[idx_pesan_terakhir]["teks"] += "\n" + baris

    return pesan, format_terdeteksi, urutan_tanggal, catatan_global


# ---------------------------------------------------------------------------
# Filter rentang waktu
# ---------------------------------------------------------------------------

_POLA_ISO_DT = re.compile(r"^\d{4}-\d{2}-\d{2}([ T]\d{1,2}:\d{2}(:\d{2})?)?$")


def urai_titik_waktu(nilai, sekarang):
    """Terima ISO, atau 'kemarin[ HH:MM]', 'hari ini[ HH:MM]', 'besok[ HH:MM]'."""
    if nilai is None:
        return None
    nilai = nilai.strip()
    if _POLA_ISO_DT.match(nilai):
        nilai_norm = nilai.replace(" ", "T", 1) if " " in nilai and "T" not in nilai else nilai
        try:
            return datetime.fromisoformat(nilai_norm)
        except ValueError:
            raise ValueError(f"tanggal/waktu ISO tidak valid: '{nilai}'")

    rendah = nilai.lower()
    dasar = None
    sisa_jam = "00:00"
    for kata, delta in (("kemarin", -1), ("hari ini", 0), ("besok", 1)):
        if rendah == kata or rendah.startswith(kata + " "):
            dasar = (sekarang + timedelta(days=delta)).date()
            sisa = nilai[len(kata):].strip()
            if sisa:
                sisa_jam = sisa
            break
    if dasar is None:
        raise ValueError(
            f"format --sejak/--sampai tidak dikenali: '{nilai}'. "
            "Pakai ISO (2026-09-12 17:00), atau 'kemarin 17:00' / 'hari ini' / 'besok'."
        )
    m = re.match(r"^(\d{1,2})[:.](\d{2})$", sisa_jam)
    if not m:
        raise ValueError(f"jam pada '{nilai}' tidak dikenali, contoh yang benar: 'kemarin 17:00'")
    jam, menit = int(m.group(1)), int(m.group(2))
    if not (0 <= jam <= 23 and 0 <= menit <= 59):
        raise ValueError(f"jam pada '{nilai}' di luar rentang wajar")
    return datetime(dasar.year, dasar.month, dasar.day, jam, menit)


def filter_rentang(pesan, sejak, sampai):
    hasil = pesan
    if sejak is not None:
        hasil = [p for p in hasil if datetime.fromisoformat(p["waktu"]) >= sejak]
    if sampai is not None:
        hasil = [p for p in hasil if datetime.fromisoformat(p["waktu"]) <= sampai]
    return hasil


# ---------------------------------------------------------------------------
# Penyamaran (anonimisasi)
# ---------------------------------------------------------------------------

POLA_NOMOR_TELEPON = re.compile(
    r"(?:\+?62|0)[\s\-]?8[0-9]{2,3}(?:[\s\-]?[0-9]{3,4}){1,3}"
)


def samarkan_nomor_dalam_teks(teks):
    return POLA_NOMOR_TELEPON.sub("[nomor disamarkan]", teks)


def samarkan_pengirim(pesan):
    """Ganti nama/nomor pengirim -> 'Anggota N' (urutan kemunculan pertama). Nomor di isi pesan juga disamarkan."""
    pemetaan = {}
    urutan = []
    terlihat = set()
    for p in pesan:
        if p["pengirim"] and p["pengirim"] not in terlihat:
            terlihat.add(p["pengirim"])
            urutan.append(p["pengirim"])
    for i, nama in enumerate(urutan, start=1):
        pemetaan[nama] = f"Anggota {i}"
    for p in pesan:
        if p["pengirim"]:
            p["pengirim"] = pemetaan[p["pengirim"]]
        p["teks"] = samarkan_nomor_dalam_teks(p["teks"])
    return pesan, pemetaan


# ---------------------------------------------------------------------------
# Statistik & pengelompokan per hari
# ---------------------------------------------------------------------------

def hitung_statistik(pesan):
    per_pengirim = {}
    per_jam = [0] * 24
    media = 0
    dihapus = 0
    sistem = 0
    for p in pesan:
        if p["jenis"] == "sistem":
            sistem += 1
            continue
        if p["jenis"] == "media":
            media += 1
        if p["jenis"] == "dihapus":
            dihapus += 1
        if p["pengirim"]:
            per_pengirim[p["pengirim"]] = per_pengirim.get(p["pengirim"], 0) + 1
        jam = datetime.fromisoformat(p["waktu"]).hour
        per_jam[jam] += 1

    jam_ramai = None
    if any(per_jam):
        jam_maks = max(range(24), key=lambda h: per_jam[h])
        jam_ramai = f"{jam_maks:02d}:00-{(jam_maks + 1) % 24:02d}:00"

    return {
        "total_pesan": len(pesan),
        "per_pengirim": dict(sorted(per_pengirim.items(), key=lambda kv: -kv[1])),
        "jam_paling_ramai": jam_ramai,
        "jumlah_media": media,
        "jumlah_dihapus": dihapus,
        "jumlah_pesan_sistem": sistem,
    }


def kelompokkan_per_hari(pesan):
    per_hari = {}
    for p in pesan:
        tgl = datetime.fromisoformat(p["waktu"]).date().isoformat()
        per_hari.setdefault(tgl, []).append(p)
    hasil = []
    for tgl in sorted(per_hari):
        daftar = per_hari[tgl]
        hasil.append({
            "tanggal": tgl,
            "jumlah_pesan": len(daftar),
            "statistik": hitung_statistik(daftar),
            "pesan": daftar,
        })
    return hasil


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser(
        description="Parsing ekspor chat WhatsApp (.txt/.zip) menjadi JSON terstruktur + statistik."
    )
    ap.add_argument("file", help="Path file ekspor chat WhatsApp (.txt atau .zip 'Tanpa Media')")
    ap.add_argument("--sejak", help="Hanya pesan sejak waktu ini. ISO ('2026-09-12 17:00') atau 'kemarin 17:00'/'hari ini'/'besok'.")
    ap.add_argument("--sampai", help="Hanya pesan sampai waktu ini. Format sama seperti --sejak.")
    ap.add_argument("--hari-terakhir", type=int, help="Hanya pesan dalam N hari terakhir (dihitung dari --sekarang atau waktu sekarang).")
    ap.add_argument("--sekarang", help="Override waktu 'sekarang' (ISO), untuk pengujian/hasil yang bisa diulang. Default: waktu saat script dijalankan.")
    ap.add_argument("--samarkan", action="store_true", help="Samarkan nama/nomor pengirim jadi 'Anggota 1..n' dan nomor telepon di isi pesan.")
    ap.add_argument("--indent", type=int, default=2, help="Indentasi JSON output (default 2; pakai 0 untuk satu baris ringkas).")
    args = ap.parse_args()

    sekarang = datetime.now()
    if args.sekarang:
        try:
            sekarang = datetime.fromisoformat(args.sekarang.replace(" ", "T", 1))
        except ValueError:
            print(f"Error: --sekarang tidak valid: '{args.sekarang}'", file=sys.stderr)
            sys.exit(1)

    try:
        teks, nama_sumber = baca_teks_ekspor(args.file)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    if teks.strip() == "":
        hasil = {
            "file": args.file,
            "sumber_teks": nama_sumber,
            "format_terdeteksi": None,
            "urutan_tanggal": None,
            "catatan": ["File ekspor kosong atau tidak berisi teks yang bisa dibaca."],
            "filter": {"sejak": args.sejak, "sampai": args.sampai, "hari_terakhir": args.hari_terakhir},
            "disamarkan": bool(args.samarkan),
            "jumlah_anggota_disamarkan": 0 if args.samarkan else None,
            "statistik": hitung_statistik([]),
            "hari": [],
        }
        print(json.dumps(hasil, ensure_ascii=False, indent=args.indent or None))
        sys.exit(0)

    pesan, fmt, urutan, catatan = parse_pesan(teks)

    sejak_dt = None
    sampai_dt = None
    try:
        if args.sejak:
            sejak_dt = urai_titik_waktu(args.sejak, sekarang)
        if args.sampai:
            sampai_dt = urai_titik_waktu(args.sampai, sekarang)
        if args.hari_terakhir is not None:
            if args.hari_terakhir < 0:
                raise ValueError("--hari-terakhir harus 0 atau lebih")
            batas = (sekarang - timedelta(days=args.hari_terakhir)).replace(hour=0, minute=0, second=0, microsecond=0)
            sejak_dt = batas if sejak_dt is None else max(sejak_dt, batas)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    pesan_terfilter = filter_rentang(pesan, sejak_dt, sampai_dt)
    if (sejak_dt or sampai_dt) and not pesan_terfilter and pesan:
        catatan.append("Tidak ada pesan pada rentang waktu yang diminta; rentang yang tersedia ada di 'rentang_pesan_asli'.")

    pemetaan_samaran = None
    if args.samarkan:
        pesan_terfilter, pemetaan_samaran = samarkan_pengirim(pesan_terfilter)

    rentang_asli = None
    if pesan:
        rentang_asli = {"pertama": pesan[0]["waktu"], "terakhir": pesan[-1]["waktu"]}

    hasil = {
        "file": args.file,
        "sumber_teks": nama_sumber,
        "format_terdeteksi": fmt,
        "urutan_tanggal": urutan,
        "catatan": catatan,
        "rentang_pesan_asli": rentang_asli,
        "filter": {
            "sejak": sejak_dt.isoformat() if sejak_dt else None,
            "sampai": sampai_dt.isoformat() if sampai_dt else None,
            "hari_terakhir": args.hari_terakhir,
        },
        "disamarkan": bool(args.samarkan),
        "jumlah_anggota_disamarkan": len(pemetaan_samaran) if pemetaan_samaran else None,
        "statistik": hitung_statistik(pesan_terfilter),
        "hari": kelompokkan_per_hari(pesan_terfilter),
    }
    print(json.dumps(hasil, ensure_ascii=False, indent=args.indent or None))
    sys.exit(0)


if __name__ == "__main__":
    main()
