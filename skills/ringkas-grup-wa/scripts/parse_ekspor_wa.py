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

ENCODING_DICOBA = ["utf-8-sig", "utf-8", "utf-16", "utf-16-le", "utf-16-be", "cp1252", "latin-1"]


def _hitung_baris_cocok_pesan(teks):
    """Jumlah baris (dari 50 baris pertama) yang cocok pola pesan WhatsApp. Dipakai untuk
    memilih kandidat decode UTF-16 yang benar saat tidak ada BOM (LE vs BE bisa sama-sama
    'berhasil' didecode tanpa error, tapi hanya satu yang menghasilkan teks yang masuk akal)."""
    n = 0
    for baris in teks.splitlines()[:50]:
        b = bersihkan_baris(baris)
        if POLA_ANDROID.match(b) or POLA_IOS.match(b):
            n += 1
    return n


def _decode(raw_bytes, nama_untuk_pesan):
    kandidat = []
    for enc in ENCODING_DICOBA:
        try:
            kandidat.append((enc, raw_bytes.decode(enc)))
        except (UnicodeDecodeError, LookupError):
            continue
    if not kandidat:
        raise ValueError(
            f"tidak bisa membaca '{nama_untuk_pesan}': encoding tidak dikenali "
            f"(dicoba {', '.join(ENCODING_DICOBA)})"
        )
    terbaik = max(
        kandidat,
        key=lambda kv: (_hitung_baris_cocok_pesan(kv[1]), -ENCODING_DICOBA.index(kv[0])),
    )
    if _hitung_baris_cocok_pesan(terbaik[1]) > 0:
        return terbaik[1]
    # Tidak ada kandidat yang cocok pola pesan sama sekali -> pakai urutan prioritas awal
    # (utf-8 dkk.) apa adanya; parse_pesan() yang akan melaporkan bila tetap tidak terbaca.
    return kandidat[0][1]


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
    pasangan_unik = {(a, b) for a, b, y in triple_list}
    if len(pasangan_unik) == 1:
        catatan.append(
            "PERINGATAN: hanya ada SATU kombinasi tanggal di seluruh pesan yang diproses — "
            "besar kemungkinan semuanya terjadi dalam SATU hari yang sama, terlepas dari "
            "urutan d/m atau m/d yang dipakai. Jika tanggal yang tertulis di ringkasan terasa "
            "jauh/keliru, ini murni soal cara membaca tanggal, bukan pesan yang tercampur dari "
            "hari berbeda — sampaikan ini apa adanya ke pengguna, jangan diam-diam dianggap benar."
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
            "chat WhatsApp, atau formatnya di luar variasi yang didukung. Jika file berasal "
            "dari convert/edit/copy-paste manual (bukan langsung dari menu 'Ekspor chat' "
            "WhatsApp), coba ekspor ulang atau simpan ulang file sebagai teks UTF-8."
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
# Penyamaran (anonimisasi) — BERSIFAT UPAYA TERBAIK (best-effort), bukan jaminan mutlak.
# Selalu periksa `kemungkinan_nama_tersisa` di output sebelum membagikan hasil.
# ---------------------------------------------------------------------------

# Nomor Indonesia (awalan 62/0 + 8xx).
POLA_NOMOR_TELEPON_ID = re.compile(
    r"(?:\+?62|0)[\s\-]?8[0-9]{2,3}(?:[\s\-]?[0-9]{3,4}){1,3}"
)
# Nomor internasional berformat "+<kode negara> ..." (mis. +1, +65, +44), minimal 8 digit total.
POLA_NOMOR_TELEPON_INTL = re.compile(
    r"\+[1-9][0-9]{0,2}[\s\-]?[0-9]{2,4}(?:[\s\-]?[0-9]{2,4}){1,4}"
)


def samarkan_nomor_dalam_teks(teks):
    teks = POLA_NOMOR_TELEPON_ID.sub("[nomor disamarkan]", teks)
    teks = POLA_NOMOR_TELEPON_INTL.sub("[nomor disamarkan]", teks)
    return teks


# Kata yang TIDAK dianggap nama meski berhuruf kapital di awal (sapaan, kata umum, hari, bulan,
# istilah dagang umum). Dipakai untuk (a) memilih alias nama depan yang aman disubstitusikan,
# dan (b) menyaring kandidat nama sisa agar tidak penuh angka/kata umum yang salah tangkap.
KATA_UMUM_STOP = {
    "pak", "bu", "bapak", "ibu", "mas", "mbak", "kak", "kakak", "bang", "abang",
    "adik", "adek", "dek", "om", "tante", "gan", "sis", "bro", "min", "admin",
    "saya", "kamu", "anda", "dia", "kita", "kami", "mereka", "semua", "tim", "grup", "group",
    "pagi", "siang", "sore", "malam", "hari", "ini", "itu", "nanti", "besok", "kemarin", "tadi",
    "oke", "baik", "siap", "iya", "tidak", "boleh", "terima", "kasih", "selamat", "halo", "hai",
    "media", "pesan", "chat", "toko", "invoice", "harga", "total", "promo", "stok", "order",
    "ready", "anggota", "orang", "you", "your", "messages", "calls", "security", "missed",
    "senin", "selasa", "rabu", "kamis", "jumat", "sabtu", "minggu",
    "januari", "februari", "maret", "april", "mei", "juni", "juli", "agustus",
    "september", "oktober", "november", "desember",
    "rp", "dp", "po", "pcs", "cod", "wa", "whatsapp", "group",
}

# 1-3 kata berturut-turut diawali huruf kapital (menangkap nama seperti "Sari", "Pak Nanda",
# "Budi Santoso"). Dipakai untuk mendeteksi nama di pesan sistem & kandidat nama sisa.
POLA_NAMA_TOKEN = r"[A-Z][A-Za-z''.\-]*(?:\s+[A-Z][A-Za-z''.\-]*){0,2}"

POLA_AKSI_SISTEM_OBJEK = re.compile(
    rf"\b(?:menambahkan|ditambahkan oleh|dihapus oleh|mengeluarkan|removed|added)\s+({POLA_NAMA_TOKEN})\b"
)
POLA_NAMA_AWAL_BARIS = re.compile(rf"^({POLA_NAMA_TOKEN})\b")

POLA_HONORIFIK = re.compile(
    r"\b(?:Pak|Bu|Bapak|Ibu|Mas|Mbak|Kak|Kakak|Bang|Abang|Om|Tante)\s+([A-Z][a-zA-Z]{2,})\b",
    re.IGNORECASE,
)
POLA_MENTION = re.compile(r"@([A-Z][a-zA-Z]{2,}(?:\s[A-Z][a-zA-Z]{2,})?)\b")


def _bukan_kata_umum(token):
    return token.lower() not in KATA_UMUM_STOP


def ekstrak_nama_sistem(teks):
    """Nama yang disebut di satu baris pesan sistem (pelaku di awal, objek setelah kata kerja aksi)."""
    hasil = []
    m = POLA_NAMA_AWAL_BARIS.match(teks)
    if m and _bukan_kata_umum(m.group(1).split()[0]):
        hasil.append(m.group(1))
    m2 = POLA_AKSI_SISTEM_OBJEK.search(teks)
    if m2 and _bukan_kata_umum(m2.group(1).split()[0]):
        hasil.append(m2.group(1))
    return hasil


def kumpulkan_nama_anggota(pesan):
    """Urutan nama unik (nama penuh) sesuai kemunculan pertama: dari `pengirim`, lalu dari nama
    yang disebut di pesan sistem (mis. 'Sari menambahkan Ridho')."""
    urutan = []
    terlihat = set()

    def tambah(nama):
        if nama and nama not in terlihat:
            terlihat.add(nama)
            urutan.append(nama)

    for p in pesan:
        if p["pengirim"]:
            tambah(p["pengirim"])
    for p in pesan:
        if p["jenis"] == "sistem":
            for n in ekstrak_nama_sistem(p["teks"]):
                tambah(n)
    return urutan


def _bangun_alias_token(nama_anggota):
    """Kata depan/panggilan umum dari nama multi-kata (mis. 'Budi Santoso' -> juga 'Budi'),
    HANYA bila kata itu unik milik satu anggota (tidak dipakai anggota lain) & bukan kata umum."""
    pemilik_token = {}
    token_ambigu = set()
    for nama in nama_anggota:
        for tok in nama.split():
            tok_l = tok.lower()
            if len(tok) < 3 or not _bukan_kata_umum(tok):
                continue
            if tok_l in pemilik_token and pemilik_token[tok_l] != nama:
                token_ambigu.add(tok_l)
            else:
                pemilik_token[tok_l] = nama
    return {t: n for t, n in pemilik_token.items() if t not in token_ambigu}


def samarkan_pengirim(pesan, nama_saya=None):
    """Samarkan (best-effort) seluruh identitas pihak ketiga: pengirim, nama yang disebut di ISI
    pesan/@mention/pesan sistem, sapaan+nama ("Pak Nanda") yang bukan anggota terdaftar, dan
    nomor telepon (Indonesia & internasional). Kembalikan (pesan, pemetaan_anggota,
    daftar_kemungkinan_nama_tersisa)."""
    nama_anggota = kumpulkan_nama_anggota(pesan)
    pemetaan = {nama: f"Anggota {i}" for i, nama in enumerate(nama_anggota, start=1)}
    nama_lower_ke_pemilik = {n.lower(): n for n in nama_anggota}
    alias_token = _bangun_alias_token(nama_anggota)  # token_lower -> nama pemilik

    kandidat = sorted(set(nama_anggota) | set(alias_token), key=len, reverse=True)
    pola_anggota = None
    if kandidat:
        pola_anggota = re.compile(
            r"\b(" + "|".join(re.escape(k) for k in kandidat) + r")\b", re.IGNORECASE
        )

    orang_map = {}  # kunci lower -> "Orang N"

    def ganti_orang(kunci_lower):
        if kunci_lower not in orang_map:
            orang_map[kunci_lower] = f"Orang {len(orang_map) + 1}"
        return orang_map[kunci_lower]

    def ganti_anggota(m):
        cocok = m.group(1)
        cocok_l = cocok.lower()
        pemilik = nama_lower_ke_pemilik.get(cocok_l) or alias_token.get(cocok_l)
        return pemetaan[pemilik] if pemilik else cocok

    def _label_sendiri(nama):
        # Jangan samarkan ulang label "Anggota N"/"Orang N" yang sudah dihasilkan di atas
        # (mis. mention regex menangkap "@Anggota" dari "@Anggota 5" hasil substitusi sebelumnya).
        return nama.split()[0].lower() in ("anggota", "orang")

    def ganti_honorifik(m):
        if _label_sendiri(m.group(1)):
            return m.group(0)
        return ganti_orang(m.group(1).lower())

    def ganti_mention(m):
        if _label_sendiri(m.group(1)):
            return m.group(0)
        return ganti_orang(m.group(1).lower())

    def proses_teks(teks):
        if pola_anggota:
            teks = pola_anggota.sub(ganti_anggota, teks)
        # Sapaan + nama yang BUKAN anggota terdaftar (mis. "Pak Nanda" bila belum tertangkap
        # di atas) -> "Orang N". Ganti seluruh frasa (sapaan+nama) agar tidak menyisakan nama.
        teks = POLA_HONORIFIK.sub(ganti_honorifik, teks)
        # @mention nama yang bukan anggota terdaftar -> "Orang N".
        teks = POLA_MENTION.sub(ganti_mention, teks)
        teks = samarkan_nomor_dalam_teks(teks)
        return teks

    for p in pesan:
        if p["pengirim"]:
            pemilik = nama_lower_ke_pemilik.get(p["pengirim"].lower())
            p["pengirim"] = pemetaan.get(pemilik, pemetaan.get(p["pengirim"], p["pengirim"]))
        p["teks"] = proses_teks(p["teks"])

    # Verifikasi sisa: kandidat kata/frasa berhuruf kapital yang masih tersisa di teks setelah
    # semua substitusi di atas — bukan jaminan nama, tapi wajib dicek manual sebelum dibagikan.
    tersisa = set()
    for p in pesan:
        for m in re.finditer(POLA_NAMA_TOKEN, p["teks"]):
            kata = m.group(0).split()
            # Buang kata umum/label di awal frasa satu per satu (mis. "Toko Jaya Makmur"
            # -> "Jaya Makmur" tetap layak dicek meski "Toko" adalah kata umum).
            while kata and (kata[0] in ("Anggota", "Orang") or not _bukan_kata_umum(kata[0])):
                kata.pop(0)
            if kata:
                tersisa.add(" ".join(kata))

    return pesan, pemetaan, sorted(tersisa)


# ---------------------------------------------------------------------------
# Kandidat "Perlu Perhatian" — checklist berbasis pola, untuk memastikan agent tidak
# melewatkan pesan penting di grup padat (recall tinggi, presisi ditentukan agent).
# ---------------------------------------------------------------------------

_KW_UANG = re.compile(r"\bRp\.?\s?\d|\b\d[\d.,]*\s?(rb|ribu|jt|juta|k)\b", re.IGNORECASE)
_KW_TENGGAT = re.compile(
    r"\b(besok|lusa|hari ini|minggu depan|bulan depan|tenggat|deadline|jatuh tempo|"
    r"paling lambat|sebelum jam|senin|selasa|rabu|kamis|jumat|sabtu|minggu)\b|"
    r"\bjam\s?\d{1,2}\b",
    re.IGNORECASE,
)
_KW_KEPUTUSAN = re.compile(
    r"\b(deal|fix|disepakati|diputuskan|oke fix|sepakat|komplain|kecewa|gagal|rusak|"
    r"refund|batal|retur|urgent|penting|masalah|protes|tolong dibantu|approve|acc)\b",
    re.IGNORECASE,
)


def tandai_kandidat_perhatian(pesan, nama_saya=None):
    """Daftar pesan `jenis: obrolan` yang mengandung sinyal 'perlu perhatian'. WAJIB dipakai
    sebagai checklist minimum oleh agent (lihat SKILL.md) — bukan pengganti penilaian akhir."""
    hasil = []
    for p in pesan:
        if p["jenis"] != "obrolan":
            continue
        teks = p["teks"]
        sinyal = []
        if "?" in teks:
            sinyal.append("tanda_tanya")
        if nama_saya and re.search(rf"@?\b{re.escape(nama_saya)}\b", teks, re.IGNORECASE):
            sinyal.append("mention_saya")
        elif "@" in teks:
            sinyal.append("mention_umum")
        if _KW_UANG.search(teks):
            sinyal.append("uang_nominal")
        if _KW_TENGGAT.search(teks):
            sinyal.append("tenggat_tanggal")
        if _KW_KEPUTUSAN.search(teks):
            sinyal.append("keputusan_komplain")
        if sinyal:
            hasil.append({
                "waktu": p["waktu"], "pengirim": p["pengirim"], "teks": p["teks"], "sinyal": sinyal,
            })
    return hasil


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
    ap.add_argument("--samarkan", action="store_true", help="Samarkan (best-effort) pengirim, nama di isi pesan/@mention/pesan sistem, sapaan+nama non-anggota, dan nomor telepon. Selalu cek 'kemungkinan_nama_tersisa' di output sebelum membagikan hasil.")
    ap.add_argument("--nama-saya", help="Nama Anda persis seperti di grup, untuk menandai pesan sendiri ('dari_saya') dan mendeteksi mention langsung ke Anda di 'kandidat_perlu_perhatian'.")
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
            "kemungkinan_nama_tersisa": [],
            "kandidat_perlu_perhatian": [],
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

    if args.nama_saya:
        for p in pesan_terfilter:
            p["dari_saya"] = bool(p["pengirim"]) and p["pengirim"].strip().lower() == args.nama_saya.strip().lower()

    # Checklist kandidat "perlu perhatian" dihitung SEBELUM penyamaran, dari teks asli,
    # supaya deteksi kata kunci tidak terganggu oleh label "Anggota N"/"Orang N".
    kandidat_perhatian = tandai_kandidat_perhatian(pesan_terfilter, args.nama_saya)

    pemetaan_samaran = None
    nama_tersisa = []
    if args.samarkan:
        pesan_terfilter, pemetaan_samaran, nama_tersisa = samarkan_pengirim(pesan_terfilter, args.nama_saya)
        # Samarkan juga kutipan di checklist kandidat_perhatian agar konsisten dengan pesan utama.
        # Bila --nama-saya diberikan, cocokkan dengan label samaran-nya (nama asli sudah diganti).
        nama_saya_untuk_kandidat = args.nama_saya
        if args.nama_saya and pemetaan_samaran:
            for asli, label in pemetaan_samaran.items():
                if asli.lower() == args.nama_saya.strip().lower():
                    nama_saya_untuk_kandidat = label
                    break
        kandidat_perhatian = tandai_kandidat_perhatian(pesan_terfilter, nama_saya_untuk_kandidat)

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
        "kemungkinan_nama_tersisa": nama_tersisa,
        "kandidat_perlu_perhatian": kandidat_perhatian,
        "statistik": hitung_statistik(pesan_terfilter),
        "hari": kelompokkan_per_hari(pesan_terfilter),
    }
    print(json.dumps(hasil, ensure_ascii=False, indent=args.indent or None))
    sys.exit(0)


if __name__ == "__main__":
    main()
