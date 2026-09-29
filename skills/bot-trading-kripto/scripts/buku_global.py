#!/usr/bin/env python3
"""Buku LIVE GLOBAL + kunci akun untuk bot-trading-kripto (Python standar).

Masalah yang ditutup (uji ulang 1.0.3, N1-R1/N1-R2): batas `modal_maks_total` hanya dicatat di folder bot.
Folder yang disalin lalu dijalankan BERSAMAAN, atau `state.json` yang dihapus lalu dibangun ulang, bisa
membuat bot membeli melebihi batas. Solusi:

1. KUNCI AKUN (OS file lock) per akun bursa di ~/.komunitech/bot-trading-kripto/akun/akun-<sidik>.lock.
   Semua bot live yang memakai kunci API yang sama -- apa pun folder bot-nya -- bergiliran: hanya satu
   yang boleh membaca saldo, memutuskan, dan mengirim order pada satu waktu. POSIX: fcntl.flock;
   Windows: msvcrt.locking. Kunci OS lepas otomatis bila proses mati (tidak ada kunci basi).
2. BUKU GLOBAL per akun di ~/.komunitech/bot-trading-kripto/akun/akun-<sidik>.json, per pasangan:
   saldo koin milik member sebelum bot live pertama (patokan), posisi & modal terpakai GABUNGAN semua bot.
   Menghapus/menyalin folder bot tidak menyentuh buku ini.
3. Sebelum SETIAP order beli live: modal terpakai = yang TERBESAR dari buku folder, buku global, dan
   (saldo koin bursa - patokan) x harga + nilai order BELI yang masih terbuka di bursa.

<sidik> = SHA-256 dari nama bursa + API KEY PUBLIK saja (tidak pernah secret), dipotong 16 karakter.
Isi buku global tidak memuat kunci apa pun.

Batas jujur: pengguna yang punya akses shell ke komputer ini bisa menghapus/menyunting folder
~/.komunitech/bot-trading-kripto/akun/ SEKALIGUS state bot; memakai kunci API baru untuk akun yang sama
juga memulai buku global baru. Script tidak bisa mencegah itu (lihat SKILL.md "Batasan").
"""

import hashlib
import json
import os
import time
from datetime import datetime

from inti import D, NOL, WIB, bulat_uang, folder_stop_global, simpan_json_atomik, teks

TUNGGU_KUNCI_DETIK = 120


class BukuGlobalRusak(Exception):
    """Buku global tidak terbaca -> tidak ada order beli (pesan Bahasa Indonesia)."""


class AkunSibuk(Exception):
    """Kunci akun dipegang proses lain terlalu lama."""


def sidik_akun(bursa, api_key_publik):
    """Sidik akun = hash nama bursa + API key PUBLIK. Secret tidak pernah dipakai di sini."""
    return hashlib.sha256(f"komunitech-akun|{bursa}|{api_key_publik}".encode("utf-8")).hexdigest()[:16]


def folder_akun():
    return os.path.join(folder_stop_global(), "akun")


def path_buku(sidik):
    return os.path.join(folder_akun(), f"akun-{sidik}.json")


# ---------------------------------------------------------------------------- kunci OS lintas platform

if os.name == "nt":  # Windows
    import msvcrt

    def _kunci_nb(fd):
        os.lseek(fd, 0, os.SEEK_SET)
        msvcrt.locking(fd, msvcrt.LK_NBLCK, 1)       # OSError bila dipegang proses lain

    def _lepas(fd):
        os.lseek(fd, 0, os.SEEK_SET)
        msvcrt.locking(fd, msvcrt.LK_UNLCK, 1)
else:  # macOS / Linux
    import fcntl

    def _kunci_nb(fd):
        fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)  # BlockingIOError (OSError) bila dipegang

    def _lepas(fd):
        fcntl.flock(fd, fcntl.LOCK_UN)


class KunciAkun:
    """Kunci eksklusif satu akun bursa. Pakai: with KunciAkun(sidik): ..."""

    def __init__(self, sidik, tunggu=TUNGGU_KUNCI_DETIK):
        self.path = os.path.join(folder_akun(), f"akun-{sidik}.lock")
        self.tunggu = tunggu
        self.fd = None

    def ambil(self):
        os.makedirs(folder_akun(), exist_ok=True)
        fd = os.open(self.path, os.O_RDWR | os.O_CREAT, 0o600)
        try:
            if os.fstat(fd).st_size == 0:
                os.write(fd, b"0")                   # Windows mengunci byte ke-0
        except OSError:
            pass
        batas = time.monotonic() + self.tunggu
        while True:
            try:
                _kunci_nb(fd)
                self.fd = fd
                return self
            except OSError:
                if time.monotonic() >= batas:
                    os.close(fd)
                    raise AkunSibuk(f"akun bursa ini sedang dipakai proses bot lain lebih dari {self.tunggu} detik")
                time.sleep(0.05)

    def lepas(self):
        if self.fd is not None:
            try:
                _lepas(self.fd)
            except OSError:
                pass
            os.close(self.fd)
            self.fd = None

    def __enter__(self):
        return self.ambil()

    def __exit__(self, *a):
        self.lepas()


# ---------------------------------------------------------------------------- buku global

def muat_buku(sidik):
    p = path_buku(sidik)
    if not os.path.exists(p):
        return {"versi": 1, "catatan": "Buku LIVE global bot-trading-kripto. Jangan disunting/dihapus.",
                "pasangan": {}}
    try:
        with open(p, encoding="utf-8") as f:
            b = json.load(f)
        if not isinstance(b, dict) or not isinstance(b.get("pasangan"), dict):
            raise ValueError("struktur salah")
        for e in b["pasangan"].values():
            for k in ("posisi_koin", "biaya_perolehan"):
                D(str(e.get(k, "0")))
            if e.get("saldo_koin_awal_bursa") not in (None, ""):
                D(str(e["saldo_koin_awal_bursa"]))
        return b
    except (OSError, ValueError, TypeError, ArithmeticError, AttributeError) as e:
        raise BukuGlobalRusak(f"Buku live global '{p}' rusak/tidak terbaca ({type(e).__name__}). Tidak ada order "
                              "beli sampai diperiksa. Jangan dihapus diam-diam: hubungi dukungan Komunitech.")


def simpan_buku(sidik, buku):
    simpan_json_atomik(path_buku(sidik), buku)


def entri(buku, pasangan, state=None):
    """Entri satu pasangan. Entri BARU diisi dari buku live folder (migrasi 1.0.3 -> 1.0.4)."""
    e = buku["pasangan"].get(pasangan)
    if e is None:
        e = {"saldo_koin_awal_bursa": None, "posisi_koin": "0", "biaya_perolehan": "0",
             "jumlah_transaksi": 0, "diperbarui": None}
        if state:
            try:
                if D(str(state.get("biaya_perolehan") or "0")) > 0:
                    e["posisi_koin"] = teks(D(str(state.get("posisi_koin") or "0")))
                    e["biaya_perolehan"] = teks(D(str(state["biaya_perolehan"])))
            except ArithmeticError:
                pass
        buku["pasangan"][pasangan] = e
    return e


def catat_isi(e, isi, kutipan, sekarang=None):
    """Perbarui entri global dari satu isi order live (rata-rata tertimbang, sama dengan buku folder)."""
    pos, bp = D(str(e.get("posisi_koin", "0"))), D(str(e.get("biaya_perolehan", "0")))
    if isi["sisi"] == "beli":
        pos += isi["jumlah"]
        bp += isi["bersih"]
    else:
        porsi = bulat_uang(bp * isi["jumlah"] / pos, kutipan) if pos > 0 else NOL
        pos -= isi["jumlah"]
        bp = NOL if pos <= 0 else max(NOL, bp - porsi)
        pos = max(NOL, pos)
    e["posisi_koin"], e["biaya_perolehan"] = teks(pos), teks(bp)
    e["jumlah_transaksi"] = int(e.get("jumlah_transaksi", 0)) + 1
    e["diperbarui"] = (sekarang or datetime.now(WIB)).isoformat(timespec="seconds")
