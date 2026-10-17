#!/usr/bin/env python3
"""pantau-website-toko (Komunitech) - ringkasan status website/toko online.

Dua mode, TANPA paket tambahan (hanya library standar Python 3.8+, lintas OS,
Windows: `python`/`py`):

1. Lewat Uptime Kuma (https://github.com/louislam/uptime-kuma, MIT) milik pengguna sendiri:
   membaca **status page JSON publik resminya** (`/api/status-page/<slug>` dan
   `/api/status-page/heartbeat/<slug>`) - endpoint ini memang dirancang untuk dibaca publik
   tanpa token/API key. Uptime Kuma TIDAK disertakan/didistribusikan di sini; pengguna
   memasangnya sendiri mengikuti `docs/panduan-uptime-kuma.md`.
2. Tanpa Uptime Kuma sama sekali: `cek-cepat` melakukan SATU KALI permintaan HTTP + (bila
   https) pemeriksaan sertifikat SSL langsung ke alamat yang diberikan pengguna.

Perintah:
  pantau.py cek        --status-url URL   (atau --url BASE --slug SLUG)
  pantau.py ringkasan  --status-url URL   [--log PATH] [--json]
  pantau.py mingguan   [--log PATH] [--hari 7] [--json]
  pantau.py cek-cepat  URL                [--timeout 10] [--json]

Kode keluar: 0 = berhasil, angka lain = lihat pesan "GALAT:" (juga field "kode_keluar" di --json).

Skill ini untuk memantau SITUS/AKUN MILIK SENDIRI (toko online, checkout, link bio, domain
sendiri). Jangan dipakai untuk memantau situs pihak lain secara berulang/agresif - lihat
SKILL.md bagian "Kapan TIDAK digunakan".
"""
import argparse
import datetime as dt
import json
import os
import re
import socket
import ssl
import sys
import tempfile
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

APLIKASI = "pantau-website-toko"
VERSI = "1.0.11"
UA = f"{APLIKASI}/{VERSI} (+komunitech.com; baca status-page publik saja)"

# Konstanta status Uptime Kuma (sama persis dengan src/util.ts versi resmi)
DOWN, UP, PENDING, MAINTENANCE = 0, 1, 2, 3
LABEL_STATUS = {DOWN: "TURUN", UP: "AKTIF", PENDING: "MENUNGGU", MAINTENANCE: "PEMELIHARAAN"}

DEFAULT_LOG = str(Path.home() / ".komunitech" / "pantau-website-log.jsonl")
TIMEOUT_DEFAULT = 10
BATAS_UMUR_LOG_HARI = 90  # baris log lebih lama dari ini diabaikan otomatis (bukan dihapus)


class Gagal(Exception):
    """Galat yang pesannya aman ditunjukkan apa adanya ke pengguna."""

    def __init__(self, pesan, kode=1, **data):
        super().__init__(pesan)
        self.pesan = pesan
        self.kode = kode
        self.data = data


# ======================================================================== util HTTP/JSON

def http_get_json(url, timeout):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            status = resp.status
            body = resp.read()
    except urllib.error.HTTPError as e:
        status = e.code
        body = e.read()
    except urllib.error.URLError as e:
        alasan = getattr(e, "reason", e)
        raise Gagal(f"tidak bisa dihubungi ke {url} ({alasan})", kode=4)
    except socket.timeout:
        raise Gagal(f"waktu tunggu habis (timeout) menghubungi {url}", kode=4)
    except ValueError as e:
        raise Gagal(f"alamat tidak valid: {e}", kode=2)
    try:
        data = json.loads(body.decode("utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError):
        cuplikan = body[:120].decode("utf-8", errors="replace")
        raise Gagal(
            f"respons dari {url} bukan JSON yang valid (kode HTTP {status}). "
            f"Cek alamat/slug status page. Cuplikan: {cuplikan!r}",
            kode=4,
        )
    return status, data


POLA_STATUS_URL = re.compile(r"^(https?://[^/\s]+)/status/([A-Za-z0-9_-]+)/?$")


def urai_alamat(args):
    """Kembalikan (base, slug) dari --status-url ATAU (--url + --slug)."""
    if getattr(args, "status_url", None):
        m = POLA_STATUS_URL.match(args.status_url.strip())
        if not m:
            raise Gagal(
                "Alamat status page tidak dikenali. Bentuk yang benar: "
                "http://ALAMAT:PORT/status/NAMA-SLUG (lihat di address bar browser saat "
                "membuka status page Uptime Kuma Anda).",
                kode=2,
            )
        return m.group(1), m.group(2)
    if not getattr(args, "url", None) or not getattr(args, "slug", None):
        raise Gagal(
            "Wajib isi --status-url (alamat lengkap status page) ATAU keduanya --url dan --slug.",
            kode=2,
        )
    return args.url.rstrip("/"), args.slug


def api_status_page(base, slug):
    return f"{base}/api/status-page/{slug}"


def api_heartbeat(base, slug):
    return f"{base}/api/status-page/heartbeat/{slug}"


def cek_status_page_response(status, data, slug):
    if status == 404 or (isinstance(data, dict) and str(data.get("msg", "")).lower().find("not found") >= 0):
        raise Gagal(
            f"Status page '{slug}' tidak ditemukan. Cek ejaan slug, atau status page belum "
            f"dipublikasikan (Publish) di pengaturan Uptime Kuma.",
            kode=4,
        )
    if status != 200:
        raise Gagal(
            f"Uptime Kuma merespons kode {status}: {data.get('msg', '') if isinstance(data, dict) else ''}",
            kode=4,
        )


def semua_monitor(config_data):
    """List monitor gabungan dari semua grup publicGroupList, dengan nama grup."""
    hasil = []
    for grup in config_data.get("publicGroupList") or []:
        for m in grup.get("monitorList") or []:
            hasil.append({**m, "_grup": grup.get("name", "")})
    return hasil


# ============================================================================== perintah A: cek

def cmd_cek(args):
    base, slug = urai_alamat(args)
    status, data = http_get_json(api_status_page(base, slug), args.timeout)
    cek_status_page_response(status, data, slug)
    cfg = data.get("config", {})
    monitors = semua_monitor(data)
    hasil = {
        "ok": True,
        "base": base,
        "slug": slug,
        "judul": cfg.get("title"),
        "dipublikasikan": bool(cfg.get("published")),
        "jumlah_monitor": len(monitors),
        "sertifikat_ssl_ditampilkan": bool(cfg.get("showCertificateExpiry")),
    }
    if args.json:
        cetak_json(hasil)
        return
    print(f"TERSAMBUNG ke Uptime Kuma - status page '{slug}'")
    print(f"Alamat : {base}")
    print(f"Judul  : {hasil['judul']}")
    print(f"Dipublikasikan: {'ya' if hasil['dipublikasikan'] else 'TIDAK (pengguna belum menekan Publish)'}")
    print(f"Jumlah monitor: {hasil['jumlah_monitor']}")
    if not hasil["sertifikat_ssl_ditampilkan"]:
        print("Catatan: opsi 'Show Certificate Expiry' belum diaktifkan di status page ini, "
              "jadi sisa hari SSL tidak akan muncul di 'ringkasan' (aktifkan di pengaturan "
              "status page Uptime Kuma bila ingin melihatnya).")


# ============================================================================== perintah B: ringkasan

def urai_waktu_kuma(teks):
    """Format waktu heartbeat Uptime Kuma: 'YYYY-MM-DD HH:MM:SS(.ffffff)' UTC."""
    teks = teks.strip()
    for pola in ("%Y-%m-%d %H:%M:%S.%f", "%Y-%m-%d %H:%M:%S"):
        try:
            return dt.datetime.strptime(teks, pola).replace(tzinfo=dt.timezone.utc)
        except ValueError:
            continue
    raise Gagal(f"format waktu heartbeat tidak dikenali: {teks!r}")


WIB = dt.timezone(dt.timedelta(hours=7), "WIB")


def jam_wib(t):
    """'2026-09-26 14:22 WIB (07:22 UTC)' - pengguna awam membaca jam WIB."""
    if t is None:
        return "-"
    return f"{t.astimezone(WIB).strftime('%Y-%m-%d %H:%M')} WIB ({t.astimezone(dt.timezone.utc).strftime('%H:%M')} UTC)"


def daftar_insiden(beats, sekarang):
    """Kelompokkan heartbeat TURUN yang BERURUTAN menjadi satu insiden (kejadian).
    Insiden mulai di heartbeat TURUN pertama, selesai di heartbeat bukan-TURUN berikutnya
    (atau masih berlangsung sampai `sekarang`). Durasi = selesai - mulai (menit, eksplisit)."""
    insiden = []
    if not beats:
        return insiden
    waktu = [urai_waktu_kuma(b["time"]) for b in beats]
    aktif = None
    for i, b in enumerate(beats):
        if b["status"] == DOWN:
            if aktif is None:
                aktif = {"mulai": waktu[i], "jumlah_titik": 0}
            aktif["jumlah_titik"] += 1
        elif aktif is not None:
            aktif["selesai"] = waktu[i]
            aktif["masih_berlangsung"] = False
            insiden.append(aktif)
            aktif = None
    if aktif is not None:
        aktif["selesai"] = sekarang
        aktif["masih_berlangsung"] = True
        insiden.append(aktif)
    for x in insiden:
        x["menit"] = max(0.0, (x["selesai"] - x["mulai"]).total_seconds() / 60.0)
    return insiden


def hitung_downtime_jendela(beats, sekarang):
    """Durasi TURUN (menit) yang benar-benar terekam di daftar heartbeat yang diambil (paling
    banyak 100 titik terakhir dari server), dan JUMLAH INSIDEN (rangkaian heartbeat TURUN
    berurutan = 1 insiden; bukan jumlah heartbeat). Dihitung eksplisit, bukan tebakan."""
    if not beats:
        return 0.0, None, None, 0
    waktu = [urai_waktu_kuma(b["time"]) for b in beats]
    insiden = daftar_insiden(beats, sekarang)
    total_menit = sum(x["menit"] for x in insiden)
    return total_menit, waktu[0], waktu[-1], len(insiden)


def cmd_ringkasan(args):
    base, slug = urai_alamat(args)
    status, cfg_data = http_get_json(api_status_page(base, slug), args.timeout)
    cek_status_page_response(status, cfg_data, slug)
    _, hb_data = http_get_json(api_heartbeat(base, slug), args.timeout)

    heartbeat_list = hb_data.get("heartbeatList", {}) or {}
    uptime_list = hb_data.get("uptimeList", {}) or {}
    monitors = semua_monitor(cfg_data)
    if not monitors:
        raise Gagal(
            f"Status page '{slug}' belum berisi monitor apa pun (grup kosong). "
            f"Tambahkan monitor ke grup status page ini dulu di Uptime Kuma.",
            kode=4,
        )

    tampilkan_ssl = bool(cfg_data.get("config", {}).get("showCertificateExpiry"))
    sekarang = dt.datetime.now(dt.timezone.utc)
    hasil_monitor = []
    for m in monitors:
        mid = str(m["id"])
        beats = heartbeat_list.get(mid, [])
        beats_sorted = sorted(beats, key=lambda b: b["time"])
        current = beats_sorted[-1] if beats_sorted else None
        uptime24 = uptime_list.get(f"{mid}_24")
        menit_turun, mulai, akhir, jumlah_insiden = hitung_downtime_jendela(beats_sorted, sekarang)
        insiden = daftar_insiden(beats_sorted, sekarang)
        titik_turun = sum(1 for b in beats_sorted if b["status"] == DOWN)
        cert_hari = m.get("certExpiryDaysRemaining")
        cert_hari = cert_hari if isinstance(cert_hari, int) else None
        monitor_https = str(m.get("url") or "").lower().startswith("https://")
        # Uptime Kuma sendiri HANYA mengisi certExpiryDaysRemaining saat sertifikat TEPERCAYA
        # (tlsInfo.valid=true di kode sumbernya) - untuk https self-signed/tidak tepercaya,
        # field ini kosong walau "Show Certificate Expiry" sudah aktif. Diam saja di sini akan
        # terlihat seperti skill lupa mengecek SSL, padahal itu keterbatasan Uptime Kuma sendiri
        # (temuan uji independen 2026-09-26) - beri catatan eksplisit, bukan diam.
        catatan_ssl = None
        if cert_hari is None and monitor_https and tampilkan_ssl:
            catatan_ssl = ("SSL tidak terbaca dari Uptime Kuma (biasanya karena sertifikatnya "
                            "tidak tepercaya/self-signed - Uptime Kuma hanya melaporkan sisa hari "
                            "untuk sertifikat yang valid) - cek dengan 'cek-cepat' untuk melihat "
                            "sisa harinya langsung.")
        hasil_monitor.append({
            "id": m["id"],
            "nama": m.get("name"),
            "grup": m.get("_grup"),
            "tipe": m.get("type"),
            "status_kode": current["status"] if current else None,
            "status": LABEL_STATUS.get(current["status"], "TIDAK DIKETAHUI") if current else "BELUM ADA DATA",
            "ping_ms": current.get("ping") if current else None,
            "uptime_24_jam_persen": round(uptime24 * 100, 2) if isinstance(uptime24, (int, float)) else None,
            "jendela_menit_turun": round(menit_turun, 1),
            "jendela_jumlah_insiden": jumlah_insiden,
            "jendela_jumlah_heartbeat_turun": titik_turun,
            "jendela_insiden": [{
                "mulai": x["mulai"].isoformat(), "mulai_wib": jam_wib(x["mulai"]),
                "selesai": None if x["masih_berlangsung"] else x["selesai"].isoformat(),
                "selesai_wib": None if x["masih_berlangsung"] else jam_wib(x["selesai"]),
                "masih_berlangsung": x["masih_berlangsung"],
                "menit": round(x["menit"], 1),
                "jumlah_heartbeat_turun": x["jumlah_titik"],
            } for x in insiden],
            "jendela_mulai": mulai.isoformat() if mulai else None,
            "jendela_akhir": akhir.isoformat() if akhir else None,
            "jendela_mulai_wib": jam_wib(mulai) if mulai else None,
            "jendela_akhir_wib": jam_wib(akhir) if akhir else None,
            "jendela_jumlah_titik": len(beats_sorted),
            "sisa_hari_ssl": cert_hari,
            "catatan_ssl": catatan_ssl,
        })

    hasil = {"ok": True, "base": base, "slug": slug, "judul": cfg_data.get("config", {}).get("title"),
             "waktu_cek": sekarang.isoformat(), "monitor": hasil_monitor}

    if args.json:
        cetak_json(hasil)
    else:
        cetak_ringkasan_teks(hasil)

    if not args.tanpa_log:
        for m in hasil_monitor:
            tulis_log(args.log, {
                "ts": sekarang.isoformat(),
                "base": base,
                "slug": slug,
                "monitor_id": m["id"],
                "monitor_nama": m["nama"],
                "status_kode": m["status_kode"],
                "uptime_24_jam_persen": m["uptime_24_jam_persen"],
                "ping_ms": m["ping_ms"],
                "sisa_hari_ssl": m["sisa_hari_ssl"],
            })


def cetak_ringkasan_teks(hasil):
    print(f"RINGKASAN STATUS - {hasil['judul']} ({hasil['slug']})")
    print(f"Diperiksa: {jam_wib(dt.datetime.fromisoformat(hasil['waktu_cek']))}")
    print("-" * 60)
    for m in hasil["monitor"]:
        tanda = {"AKTIF": "OK", "TURUN": "!!", "MENUNGGU": "..", "PEMELIHARAAN": "**"}.get(m["status"], "??")
        print(f"[{tanda}] {m['nama']}  (grup: {m['grup'] or '-'})")
        print(f"     Status sekarang : {m['status']}"
              + (f", ping {m['ping_ms']} ms" if m["ping_ms"] is not None else ""))
        if m["uptime_24_jam_persen"] is not None:
            print(f"     Uptime 24 jam   : {m['uptime_24_jam_persen']}% (dihitung Uptime Kuma sendiri)")
        else:
            print("     Uptime 24 jam   : belum ada data (monitor baru ditambahkan)")
        if m["jendela_jumlah_titik"]:
            print(f"     Kejadian TURUN dalam {m['jendela_jumlah_titik']} cek terakhir yang terbaca "
                  f"({m['jendela_mulai_wib']} s/d {m['jendela_akhir_wib']}): "
                  f"{m['jendela_jumlah_insiden']} kejadian, total {m['jendela_menit_turun']} menit "
                  f"(HANYA jendela ini, bukan seluruh hari/minggu)")
            for no, x in enumerate(m["jendela_insiden"], 1):
                if x["masih_berlangsung"]:
                    print(f"       {no}. turun sejak {x['mulai_wib']} - MASIH TURUN, sudah {x['menit']} menit")
                else:
                    print(f"       {no}. {x['mulai_wib']} s/d {x['selesai_wib']} - {x['menit']} menit")
        if m["sisa_hari_ssl"] is not None:
            peringatan = "  <-- SEGERA PERPANJANG" if m["sisa_hari_ssl"] <= 14 else ""
            print(f"     Sertifikat SSL  : {m['sisa_hari_ssl']} hari lagi{peringatan}")
        elif m.get("catatan_ssl"):
            print(f"     Sertifikat SSL  : {m['catatan_ssl']}")
        print()
    print("Catatan: 'Uptime 24 jam' & sertifikat SSL diambil apa adanya dari Uptime Kuma "
          "(sisa hari SSL hanya tampil bila 'Show Certificate Expiry' aktif di status page & "
          "monitornya https). Ringkasan mingguan lihat perintah 'mingguan' (baca log lokal skill ini).")


# ============================================================================== log lokal & mingguan

def tulis_log(path, rec):
    p = Path(path)
    try:
        p.parent.mkdir(parents=True, exist_ok=True)
        with p.open("a", encoding="utf-8") as f:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    except OSError as e:
        # Log gagal ditulis TIDAK boleh menggagalkan perintah 'ringkasan' itu sendiri.
        print(f"PERINGATAN: gagal menulis log lokal ke {path}: {e}", file=sys.stderr)


def baca_log(path):
    p = Path(path)
    if not p.is_file():
        return [], 0
    baris_rusak = 0
    hasil = []
    with p.open("r", encoding="utf-8") as f:
        for baris in f:
            baris = baris.strip()
            if not baris:
                continue
            try:
                hasil.append(json.loads(baris))
            except json.JSONDecodeError:
                baris_rusak += 1
    return hasil, baris_rusak


def cmd_mingguan(args):
    catatan, baris_rusak = baca_log(args.log)
    if not catatan:
        raise Gagal(
            f"Belum ada data di log lokal ({args.log}). Jalankan 'ringkasan' minimal beberapa kali "
            f"(idealnya terjadwal harian lewat OpenClaw - lihat references/openclaw-jadwal.md) "
            f"sebelum minta ringkasan mingguan.",
            kode=4,
        )
    sekarang = dt.datetime.now(dt.timezone.utc)
    batas = sekarang - dt.timedelta(hours=24 * args.hari)
    dipakai = []
    for rec in catatan:
        try:
            ts = dt.datetime.fromisoformat(rec["ts"])
        except (KeyError, ValueError):
            continue
        if ts >= batas:
            dipakai.append({**rec, "_ts": ts})

    if not dipakai:
        raise Gagal(
            f"Ada {len(catatan)} baris log, tapi tidak satu pun dalam {args.hari} hari terakhir. "
            f"Log paling lama tersimpan di {args.log}.",
            kode=4,
        )

    per_monitor = {}
    for rec in dipakai:
        kunci = (rec.get("base"), rec.get("slug"), rec.get("monitor_id"))
        per_monitor.setdefault(kunci, {"nama": rec.get("monitor_nama"), "titik": []})
        per_monitor[kunci]["titik"].append(rec)

    ringkasan_monitor = []
    for kunci, info in per_monitor.items():
        titik = info["titik"]
        uptime_valid = [t["uptime_24_jam_persen"] for t in titik if isinstance(t.get("uptime_24_jam_persen"), (int, float))]
        jumlah_turun = sum(1 for t in titik if t.get("status_kode") == DOWN)
        cert_terakhir = next((t["sisa_hari_ssl"] for t in sorted(titik, key=lambda x: x["_ts"], reverse=True)
                               if t.get("sisa_hari_ssl") is not None), None)
        ringkasan_monitor.append({
            "monitor_id": kunci[2],
            "nama": info["nama"],
            "jumlah_observasi": len(titik),
            "rata_rata_uptime_24_jam_persen": round(sum(uptime_valid) / len(uptime_valid), 2) if uptime_valid else None,
            "jumlah_observasi_turun": jumlah_turun,
            "sisa_hari_ssl_terakhir": cert_terakhir,
        })
    ringkasan_monitor.sort(key=lambda x: x["nama"] or "")

    hasil = {
        "ok": True,
        "hari": args.hari,
        "dari": min(t["_ts"] for t in dipakai).isoformat(),
        "sampai": max(t["_ts"] for t in dipakai).isoformat(),
        "jumlah_observasi_total": len(dipakai),
        "baris_log_rusak_diabaikan": baris_rusak,
        "monitor": ringkasan_monitor,
    }
    if args.json:
        cetak_json(hasil)
        return

    print(f"RINGKASAN {args.hari} HARI TERAKHIR (dari log lokal skill ini, bukan dari Uptime Kuma langsung)")
    print(f"Data terekam: {hasil['dari']} s/d {hasil['sampai']} UTC ({hasil['jumlah_observasi_total']} kali cek)")
    if baris_rusak:
        print(f"({baris_rusak} baris log rusak diabaikan)")
    if hasil["jumlah_observasi_total"] < args.hari:
        print(f"PERHATIAN: baru {hasil['jumlah_observasi_total']} kali data untuk periode {args.hari} hari - "
              f"jalankan 'ringkasan' lebih sering (idealnya harian terjadwal) agar rata-rata ini makin akurat.")
    print("-" * 60)
    for m in hasil["monitor"]:
        print(f"{m['nama']} (id {m['monitor_id']})")
        print(f"     Observasi        : {m['jumlah_observasi']}x")
        if m["rata_rata_uptime_24_jam_persen"] is not None:
            print(f"     Rata-rata uptime : {m['rata_rata_uptime_24_jam_persen']}% "
                  f"(rata-rata dari {m['jumlah_observasi']} kali baca 'uptime 24 jam' Uptime Kuma, "
                  f"BUKAN uptime resmi 7 hari)")
        else:
            print("     Rata-rata uptime : tidak ada data uptime pada observasi ini")
        print(f"     Terdeteksi TURUN : {m['jumlah_observasi_turun']}x dari {m['jumlah_observasi']} kali cek")
        if m["sisa_hari_ssl_terakhir"] is not None:
            print(f"     Sisa SSL (terakhir dicek): {m['sisa_hari_ssl_terakhir']} hari")
        print()


# ============================================================================== perintah D: cek-cepat

def urai_url_target(url_teks):
    from urllib.parse import urlparse
    url_teks = url_teks.strip()
    if not re.match(r"^https?://", url_teks, re.IGNORECASE):
        url_teks = "https://" + url_teks
    parsed = urlparse(url_teks)
    if not parsed.hostname:
        raise Gagal(f"alamat tidak dikenali: {url_teks!r}", kode=2)
    return url_teks, parsed


def _urai_notafter_dari_der(der_bytes):
    """Baca 'notAfter' dari sertifikat DER mentah TANPA memverifikasinya (dipakai hanya untuk
    tetap menampilkan sisa hari saat sertifikat tidak terpercaya). Memakai fungsi decoder
    bawaan modul ssl (bagian dari Python standar, tanpa paket tambahan apa pun); bila fungsi
    ini tidak tersedia di versi Python tertentu, sisa hari untuk sertifikat tidak terpercaya
    cukup ditampilkan sebagai '-' (lihat pemanggilnya)."""
    try:
        decoder = ssl._ssl._test_decode_cert
    except AttributeError:
        return None
    try:
        pem = ssl.DER_cert_to_PEM_cert(der_bytes)
        with tempfile.NamedTemporaryFile(mode="w", suffix=".pem", delete=False) as f:
            f.write(pem)
            nama_file = f.name
        try:
            return decoder(nama_file)
        finally:
            try:
                os.remove(nama_file)
            except OSError:
                pass
    except (ssl.SSLError, OSError, ValueError):
        return None


def cek_ssl_langsung(host, port, timeout):
    hasil = {"valid": None, "sisa_hari": None, "kedaluwarsa": None, "catatan": None}
    ctx = ssl.create_default_context()
    cert = None
    try:
        with socket.create_connection((host, port), timeout=timeout) as sock:
            with ctx.wrap_socket(sock, server_hostname=host) as ssock:
                cert = ssock.getpeercert()
        hasil["valid"] = True
    except ssl.SSLCertVerificationError as e:
        hasil["valid"] = False
        hasil["catatan"] = f"sertifikat TIDAK terpercaya/hostname tidak cocok ({e.verify_message if hasattr(e, 'verify_message') else e})"
        # Dengan verify_mode=CERT_NONE, getpeercert() sengaja mengembalikan dict kosong (perilaku
        # baku Python) walau sertifikatnya sendiri sudah diterima. Untuk tetap bisa menunjukkan
        # sisa hari (dengan status TIDAK VALID yang jelas), baca tanggalnya dari data DER mentah.
        try:
            ctx_bebas = ssl._create_unverified_context()
            with socket.create_connection((host, port), timeout=timeout) as sock:
                with ctx_bebas.wrap_socket(sock, server_hostname=host) as ssock:
                    der = ssock.getpeercert(binary_form=True)
            cert = _urai_notafter_dari_der(der) if der else None
        except OSError:
            cert = None
    except socket.timeout:
        raise Gagal(f"waktu tunggu habis saat memeriksa SSL ke {host}:{port}")
    except (OSError, ssl.SSLError) as e:
        raise Gagal(f"tidak bisa memeriksa SSL ke {host}:{port} ({e})")

    if cert and cert.get("notAfter"):
        try:
            kedaluwarsa = dt.datetime.strptime(cert["notAfter"], "%b %d %H:%M:%S %Y %Z").replace(tzinfo=dt.timezone.utc)
        except ValueError:
            kedaluwarsa = None
        if kedaluwarsa:
            hasil["sisa_hari"] = (kedaluwarsa - dt.datetime.now(dt.timezone.utc)).days
            hasil["kedaluwarsa"] = kedaluwarsa.date().isoformat()
    return hasil


class _TanpaIkutiRedirect(urllib.request.HTTPRedirectHandler):
    """Menonaktifkan pengikutan redirect otomatis bawaan urllib, supaya tiap kode 3xx dan
    tujuannya (header Location) bisa direkam sebagai 'rantai redirect', bukan hilang begitu
    saja di balik status HTTP tujuan akhir (temuan uji independen 2026-09-26, v1.0.0)."""

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def minta_dengan_rantai_redirect(url_awal, timeout, maks_hop=8):
    """Kirim GET, ikuti redirect MANUAL (bukan otomatis) supaya tiap hop tercatat.
    Kembalikan (kode_akhir, url_akhir, rantai) dengan rantai = [(url, kode, tujuan), ...].
    Sertifikat tidak terpercaya di hop mana pun otomatis dicoba ulang tanpa verifikasi
    (perilaku sama seperti v1.0.0), supaya laporan tetap berguna."""
    opener_verifikasi = urllib.request.build_opener(_TanpaIkutiRedirect)
    opener_bebas = urllib.request.build_opener(
        _TanpaIkutiRedirect, urllib.request.HTTPSHandler(context=ssl._create_unverified_context())
    )
    rantai = []
    url = url_awal
    for _ in range(maks_hop + 1):
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        try:
            with opener_verifikasi.open(req, timeout=timeout) as resp:
                kode = resp.status
        except urllib.error.HTTPError as e:
            kode = e.code
            if 300 <= kode < 400 and e.headers.get("Location"):
                tujuan = urllib.parse.urljoin(url, e.headers.get("Location"))
                rantai.append((url, kode, tujuan))
                url = tujuan
                continue
            return kode, url, rantai
        except urllib.error.URLError as e:
            alasan = getattr(e, "reason", e)
            if not (isinstance(alasan, ssl.SSLCertVerificationError) or "CERTIFICATE_VERIFY_FAILED" in str(alasan)):
                raise
            # Sertifikat tidak terpercaya: ulangi hop INI saja tanpa verifikasi (bagian SSL di
            # bawah tetap menandai TIDAK VALID apa adanya lewat cek_ssl_langsung).
            try:
                with opener_bebas.open(req, timeout=timeout) as resp:
                    kode = resp.status
            except urllib.error.HTTPError as e2:
                kode = e2.code
                if 300 <= kode < 400 and e2.headers.get("Location"):
                    tujuan = urllib.parse.urljoin(url, e2.headers.get("Location"))
                    rantai.append((url, kode, tujuan))
                    url = tujuan
                    continue
                return kode, url, rantai
        return kode, url, rantai
    raise Gagal(f"terlalu banyak redirect (>{maks_hop}) dimulai dari {url_awal}.", kode=4)


def cmd_cek_cepat(args):
    url_teks, parsed = urai_url_target(args.url)
    t0 = time.monotonic()
    try:
        kode, url_akhir, rantai = minta_dengan_rantai_redirect(url_teks, args.timeout)
        elapsed_ms = round((time.monotonic() - t0) * 1000, 1)
    except socket.timeout:
        raise Gagal(f"waktu tunggu habis ({args.timeout} detik) menghubungi {url_teks}. "
                     f"Situs mungkin sangat lambat atau tidak merespons.", kode=4)
    except urllib.error.URLError as e:
        raise Gagal(f"tidak bisa menghubungi {url_teks}: {getattr(e, 'reason', e)}. "
                     f"Cek ejaan alamat/domain, atau situsnya sedang benar-benar mati.", kode=4)

    # Sertifikat SSL diperiksa untuk host TUJUAN AKHIR (setelah redirect, bila ada) - itu yang
    # sesungguhnya dilihat pelanggan di browser mereka.
    parsed_akhir = urllib.parse.urlparse(url_akhir)

    kategori = "OK" if 200 <= kode < 300 else ("REDIRECT" if 300 <= kode < 400 else
               ("GALAT KLIEN (4xx)" if 400 <= kode < 500 else "GALAT SERVER (5xx)"))

    ssl_info = None
    if parsed_akhir.scheme == "https":
        port = parsed_akhir.port or 443
        try:
            ssl_info = cek_ssl_langsung(parsed_akhir.hostname, port, args.timeout)
        except Gagal as g:
            ssl_info = {"valid": None, "sisa_hari": None, "kedaluwarsa": None, "catatan": g.pesan}

    rantai_out = [{"dari": a, "kode": b, "ke": c} for a, b, c in rantai]
    hasil = {
        "ok": True, "url": url_teks, "url_akhir": url_akhir, "kode_http": kode, "kategori": kategori,
        "waktu_respons_ms": elapsed_ms, "rantai_redirect": rantai_out, "ssl": ssl_info,
    }
    if args.json:
        cetak_json(hasil)
        return

    print(f"CEK CEPAT: {url_teks}")
    if rantai_out:
        langkah = " -> ".join([f"{r['kode']}" for r in rantai_out] + [str(kode)])
        print(f"Redirect: {langkah}  (tujuan akhir: {url_akhir})")
    print(f"HTTP    : {kode} ({kategori})")
    print(f"Respons : {elapsed_ms} ms (total, termasuk redirect bila ada)" if rantai_out else f"Respons : {elapsed_ms} ms")
    if ssl_info is None:
        print("SSL     : - (alamat http://, bukan https://)")
    elif ssl_info["sisa_hari"] is not None:
        peringatan = "  <-- SEGERA PERPANJANG" if ssl_info["sisa_hari"] <= 14 else ""
        tanda_valid = "" if ssl_info["valid"] else "  [PERINGATAN: sertifikat tidak terpercaya]"
        print(f"SSL     : {ssl_info['sisa_hari']} hari lagi (kedaluwarsa {ssl_info['kedaluwarsa']}){peringatan}{tanda_valid}")
    else:
        print(f"SSL     : tidak bisa diperiksa ({ssl_info['catatan']})")


# ============================================================================== main

def cetak_json(obj):
    print(json.dumps(obj, ensure_ascii=False, indent=2))


def buat_parser():
    ap = argparse.ArgumentParser(prog="pantau.py", description="Ringkasan status website/toko online (Uptime Kuma atau langsung).")
    sub = ap.add_subparsers(dest="perintah", required=True)

    def tambah_umum(p):
        p.add_argument("--timeout", type=float, default=TIMEOUT_DEFAULT, help=f"detik (default {TIMEOUT_DEFAULT})")
        p.add_argument("--json", action="store_true", help="keluaran JSON terstruktur")

    p = sub.add_parser("cek", help="cek koneksi ke status page Uptime Kuma")
    p.add_argument("--status-url")
    p.add_argument("--url")
    p.add_argument("--slug")
    tambah_umum(p)
    p.set_defaults(func=cmd_cek)

    p = sub.add_parser("ringkasan", help="ringkasan status semua monitor di satu status page")
    p.add_argument("--status-url")
    p.add_argument("--url")
    p.add_argument("--slug")
    p.add_argument("--log", default=DEFAULT_LOG, help=f"file log lokal untuk 'mingguan' (default {DEFAULT_LOG})")
    p.add_argument("--tanpa-log", action="store_true", help="jangan menulis ke log lokal")
    tambah_umum(p)
    p.set_defaults(func=cmd_ringkasan)

    p = sub.add_parser("mingguan", help="ringkasan dari log lokal (hasil beberapa kali 'ringkasan')")
    p.add_argument("--log", default=DEFAULT_LOG)
    p.add_argument("--hari", type=int, default=7)
    tambah_umum(p)
    p.set_defaults(func=cmd_mingguan)

    p = sub.add_parser("cek-cepat", help="cek sekali tanpa Uptime Kuma: HTTP status, waktu respons, sisa hari SSL")
    p.add_argument("url")
    tambah_umum(p)
    p.set_defaults(func=cmd_cek_cepat)

    return ap


def main(argv=None):
    ap = buat_parser()
    args = ap.parse_args(argv)
    try:
        args.func(args)
        return 0
    except Gagal as g:
        if getattr(args, "json", False):
            cetak_json({"ok": False, "error": g.pesan, "kode_keluar": g.kode, **g.data})
        else:
            print(f"GALAT: {g.pesan}", file=sys.stderr)
        return g.kode
    except KeyboardInterrupt:
        print("\nDibatalkan.", file=sys.stderr)
        return 130


if __name__ == "__main__":
    sys.exit(main())
