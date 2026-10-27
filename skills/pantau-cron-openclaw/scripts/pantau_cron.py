#!/usr/bin/env python3
"""Pantau cron OpenClaw ala "dead man's switch": tiap job mengirim `ping` saat sukses;
`cek` membandingkan ping terakhir dengan jadwal + toleransi.

Hanya Python standar (3.8+), lintas OS. Windows: ganti `python3` dengan `python` atau `py`.
Data tersimpan LOKAL di satu folder (default: ~/pantau-cron, atau --folder, atau
variabel lingkungan PANTAU_CRON_DIR):
  jobs.json        daftar job (nama, jadwal, zona, toleransi)
  ping/<nama>.log  satu baris per ping (waktu UTC, catatan)
  alarm.json       ingatan alarm yang sudah dikabarkan (supaya tidak berulang-ulang)
  healthchecks.json (opsional, dibuat pengguna sendiri) nama-job -> URL ping layanan luar

Perintah: tambah, hapus, daftar, ping, cek, riwayat, bungkus, jalankan.   Resolusi waktu: 1 menit.
  bungkus  : (job-perintah OpenClaw) susun --command-argv baru yang menjalankan argv LAMA UTUH lalu
             lapor selesai; --buang mengembalikan argv lama persis. Berkas script milik pemilik tidak disentuh.
  jalankan : dipakai oleh argv hasil bungkus: jalankan argv lama tanpa shell, teruskan keluaran & kode
             keluarnya, catat lapor selesai diam-diam hanya bila kode keluar 0.
  hapus --terima-lapor : berhenti mengawasi job, tetapi lapor selesai dari perintah buatan pemilik
             tetap diterima (kode keluar 0, tidak dicatat, tidak ke layanan luar) agar jadwalnya tidak gagal.
Zona: WIB (UTC+7), WITA (UTC+8), WIT (UTC+9), UTC. Indonesia tidak memakai jam musim panas.
"""
import argparse
import datetime as dt
import json
import os
import re
import shlex
import subprocess
import sys
import unicodedata
import urllib.request

VERSI = "1.0.6"
ZONA = {"WIB": 7, "WITA": 8, "WIT": 9, "UTC": 0}
ALIAS_ZONA = {"ASIA/JAKARTA": "WIB", "ASIA/PONTIANAK": "WIB", "ASIA/MAKASSAR": "WITA",
              "ASIA/JAYAPURA": "WIT", "ETC/UTC": "UTC", "GMT": "UTC"}
BULAN = ["Jan", "Feb", "Mar", "Apr", "Mei", "Jun", "Jul", "Agu", "Sep", "Okt", "Nov", "Des"]
MAKS_HARI_CARI = 366 * 8 + 10   # cukup untuk 29 Februari berikutnya
MAKS_TERLEWAT = 500
MAKS_PING_SIMPAN = 200
MAKS_DUR_TOLERANSI = 7 * 1440
MAKRO = {"@yearly": "0 0 1 1 *", "@annually": "0 0 1 1 *", "@monthly": "0 0 1 * *",
         "@weekly": "0 0 * * 0", "@daily": "0 0 * * *", "@midnight": "0 0 * * *",
         "@hourly": "0 * * * *"}
NAMA_HARI = {"sun": 0, "mon": 1, "tue": 2, "wed": 3, "thu": 4, "fri": 5, "sat": 6}
NAMA_BULAN = {m: i + 1 for i, m in enumerate(
    ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"])}


class GalatPantau(Exception):
    """Galat yang pesannya boleh langsung ditampilkan ke pengguna."""


# ---------------------------------------------------------------- zona & waktu
def normal_zona(teks):
    z = (teks or "WIB").strip().upper()
    z = ALIAS_ZONA.get(z, z)
    if z not in ZONA:
        raise GalatPantau("Zona '%s' tidak dikenal. Pakai WIB, WITA, WIT, atau UTC." % teks)
    return z


def ke_lokal(utc, zona):
    """datetime aware-UTC -> datetime naif waktu setempat."""
    return (utc + dt.timedelta(hours=ZONA[zona])).replace(tzinfo=None)


def dari_lokal(lokal, zona):
    return (lokal - dt.timedelta(hours=ZONA[zona])).replace(tzinfo=dt.timezone.utc)


def baca_waktu_utc(teks):
    """'2026-10-12T14:02:11Z' atau ISO dengan offset -> aware UTC. Naif dianggap WIB."""
    t = str(teks).strip()
    if t.endswith(("Z", "z")):
        t = t[:-1] + "+00:00"
    try:
        w = dt.datetime.fromisoformat(t)
    except ValueError:
        raise GalatPantau("Format waktu tidak dikenal: '%s'. Contoh: 2026-10-12T21:40+07:00" % teks)
    if w.tzinfo is None:
        w = w.replace(tzinfo=dt.timezone(dt.timedelta(hours=7)))
    return w.astimezone(dt.timezone.utc)


def iso_utc(w):
    return w.astimezone(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def sekarang_utc(opsi):
    if opsi:
        return baca_waktu_utc(opsi)
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0)


def lantai_menit(w):
    return w.replace(second=0, microsecond=0)


def fmt_waktu(lokal, zona, tahun_ini=None):
    s = "%d %s" % (lokal.day, BULAN[lokal.month - 1])
    if tahun_ini is not None and lokal.year != tahun_ini:
        s += " %d" % lokal.year
    return "%s %02d.%02d %s" % (s, lokal.hour, lokal.minute, zona)


def fmt_durasi(menit):
    menit = int(menit)
    if menit < 1:
        return "kurang dari 1 menit"
    hari, sisa = divmod(menit, 1440)
    jam, mnt = divmod(sisa, 60)
    bagian = []
    if hari:
        bagian.append("%d hari" % hari)
    if jam:
        bagian.append("%d jam" % jam)
    if mnt and not hari:
        bagian.append("%d menit" % mnt)
    return " ".join(bagian)


# ---------------------------------------------------------------- parsing cron
def _angka(tok, lo, hi, alias, nama):
    t = tok.strip().lower()
    if t in alias:
        return alias[t]
    if not t.isdigit():
        raise GalatPantau("Kolom %s berisi '%s' yang tidak dikenal." % (nama, tok))
    n = int(t)
    if n < lo or n > hi:
        raise GalatPantau("Kolom %s: nilai %d di luar rentang %d-%d." % (nama, n, lo, hi))
    return n


def _kolom(teks, lo, hi, alias, nama, hari=False):
    nilai = set()
    if teks == "":
        raise GalatPantau("Kolom %s kosong." % nama)
    for bagian in teks.split(","):
        if bagian == "":
            raise GalatPantau("Kolom %s: ada koma berlebih." % nama)
        langkah = None
        dasar = bagian
        if "/" in bagian:
            dasar, ls = bagian.split("/", 1)
            if not ls.isdigit() or int(ls) < 1:
                raise GalatPantau("Kolom %s: langkah '/%s' harus bilangan bulat >= 1." % (nama, ls))
            langkah = int(ls)
        if dasar == "*":
            a, b = lo, (6 if hari else hi)
        elif "-" in dasar:
            x, y = dasar.split("-", 1)
            a, b = _angka(x, lo, hi, alias, nama), _angka(y, lo, hi, alias, nama)
            if a > b:
                raise GalatPantau("Kolom %s: rentang %s terbalik." % (nama, dasar))
        else:
            a = _angka(dasar, lo, hi, alias, nama)
            b = hi if langkah else a
        nilai.update(range(a, b + 1, langkah or 1))
    if hari:
        nilai = {0 if v == 7 else v for v in nilai}
    return nilai


def parse_cron(teks):
    """Cron 5 kolom: menit jam tgl-bulan bulan hari-minggu. Dukung *, */n, a-b, a-b/n, daftar a,b."""
    if not isinstance(teks, str) or not teks.strip():
        raise GalatPantau("Jadwal cron kosong.")
    t = MAKRO.get(teks.strip().lower(), teks.strip())
    kol = t.split()
    if len(kol) == 6:
        raise GalatPantau("Cron 6 kolom (dengan detik) tidak didukung. Pakai 5 kolom: menit jam tanggal bulan hari.")
    if len(kol) != 5:
        raise GalatPantau("Jadwal cron harus 5 kolom (menit jam tanggal bulan hari), bukan %d: '%s'." % (len(kol), teks))
    return {
        "teks": " ".join(kol),
        "menit": sorted(_kolom(kol[0], 0, 59, {}, "menit")),
        "jam": sorted(_kolom(kol[1], 0, 23, {}, "jam")),
        "tgl": _kolom(kol[2], 1, 31, {}, "tanggal"),
        "bulan": _kolom(kol[3], 1, 12, NAMA_BULAN, "bulan"),
        "hari": _kolom(kol[4], 0, 7, NAMA_HARI, "hari-minggu", hari=True),
        "tgl_bintang": kol[2].startswith("*"),
        "hari_bintang": kol[4].startswith("*"),
    }


def _hari_cocok(spec, d):
    if d.month not in spec["bulan"]:
        return False
    tgl_ok = d.day in spec["tgl"]
    hari_ok = ((d.weekday() + 1) % 7) in spec["hari"]
    if spec["tgl_bintang"] or spec["hari_bintang"]:
        return tgl_ok and hari_ok
    return tgl_ok or hari_ok


def _jam_terakhir(spec, batas):
    for h in reversed(spec["jam"]):
        if batas and h > batas[0]:
            continue
        for m in reversed(spec["menit"]):
            if batas and h == batas[0] and m > batas[1]:
                continue
            return h, m
    return None


def _jam_pertama(spec, batas):
    for h in spec["jam"]:
        if batas and h < batas[0]:
            continue
        for m in spec["menit"]:
            if batas and h == batas[0] and m < batas[1]:
                continue
            return h, m
    return None


def sebelumnya(spec, t, inklusif=True):
    """Jadwal terakhir <= t (atau < t bila inklusif=False). t naif, waktu setempat."""
    t = t.replace(second=0, microsecond=0)
    if not inklusif:
        t -= dt.timedelta(minutes=1)
    d = t.date()
    for i in range(MAKS_HARI_CARI):
        if _hari_cocok(spec, d):
            hm = _jam_terakhir(spec, (t.hour, t.minute) if i == 0 else None)
            if hm:
                return dt.datetime(d.year, d.month, d.day, hm[0], hm[1])
        d -= dt.timedelta(days=1)
    raise GalatPantau("Jadwal '%s' tidak pernah jatuh pada tanggal yang nyata (mis. 31 Februari)." % spec["teks"])


def berikutnya(spec, t):
    """Jadwal pertama yang > t (benar-benar sesudah t)."""
    t = t.replace(second=0, microsecond=0) + dt.timedelta(minutes=1)
    d = t.date()
    for i in range(MAKS_HARI_CARI):
        if _hari_cocok(spec, d):
            hm = _jam_pertama(spec, (t.hour, t.minute) if i == 0 else None)
            if hm:
                return dt.datetime(d.year, d.month, d.day, hm[0], hm[1])
        d += dt.timedelta(days=1)
    raise GalatPantau("Jadwal '%s' tidak pernah jatuh pada tanggal yang nyata (mis. 31 Februari)." % spec["teks"])


# ---------------------------------------------------------------- penyimpanan
def folder_data(opsi):
    f = opsi or os.environ.get("PANTAU_CRON_DIR") or os.path.join(os.path.expanduser("~"), "pantau-cron")
    return os.path.abspath(f)


def slug(teks):
    t = unicodedata.normalize("NFKD", str(teks)).encode("ascii", "ignore").decode("ascii").lower()
    t = re.sub(r"[^a-z0-9]+", "-", t).strip("-")[:40].strip("-")
    if not t:
        raise GalatPantau("Nama job kosong atau tidak bisa dipakai. Pakai huruf/angka, mis. laporan-harian.")
    return t


def _tulis_atomik(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    tmp = path + ".tmp%d" % os.getpid()
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2, sort_keys=True)
    os.replace(tmp, path)


def _baca_json(path, bawaan):
    if not os.path.exists(path):
        return bawaan
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (ValueError, OSError):
        raise GalatPantau("Berkas pantauan (%s) rusak atau tidak terbaca. Salin dulu berkasnya (mis. jadi .cadangan), "
                          "lalu hapus yang rusak agar bisa dibuat ulang. Tidak ada yang ditimpa." % os.path.basename(path))
    if not isinstance(data, dict):
        raise GalatPantau("Isi berkas %s tidak sesuai format (harus objek JSON)." % os.path.basename(path))
    return data


def muat_job(folder):
    data = _baca_json(os.path.join(folder, "jobs.json"), {"versi": 1, "jobs": {}})
    jobs = data.get("jobs")
    if not isinstance(jobs, dict):
        raise GalatPantau("jobs.json tidak sesuai format (kunci 'jobs' hilang).")
    return data


def simpan_job(folder, data):
    _tulis_atomik(os.path.join(folder, "jobs.json"), data)


def validasi_job(nama, j):
    try:
        spec = parse_cron(j.get("jadwal"))
        zona = normal_zona(j.get("zona"))
        tol = int(j.get("toleransi_menit"))
        dibuat = baca_waktu_utc(j.get("dibuat"))
    except (GalatPantau, TypeError, ValueError, AttributeError) as e:
        raise GalatPantau("Job '%s' di jobs.json tidak valid (%s). Perbaiki dengan perintah tambah --ganti." % (nama, e))
    return spec, zona, tol, dibuat


def _path_log(folder, nama):
    return os.path.join(folder, "ping", nama + ".log")


def baca_ping(folder, nama):
    """Daftar (waktu aware-UTC, catatan) urut naik. Baris rusak dilewati."""
    hasil = []
    p = _path_log(folder, nama)
    if not os.path.exists(p):
        return hasil
    with open(p, "r", encoding="utf-8", errors="replace") as f:
        for baris in f:
            bagian = baris.rstrip("\n").split("\t", 1)
            try:
                w = dt.datetime.strptime(bagian[0], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=dt.timezone.utc)
            except ValueError:
                continue
            hasil.append((w, bagian[1] if len(bagian) > 1 else ""))
    hasil.sort(key=lambda x: x[0])
    return hasil


def catat_ping(folder, nama, waktu, catatan=""):
    p = _path_log(folder, nama)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    catatan = re.sub(r"[\t\r\n]+", " ", catatan or "")[:200]
    with open(p, "a", encoding="utf-8") as f:
        f.write("%s\t%s\n" % (iso_utc(waktu), catatan))
    if os.path.getsize(p) > 64 * 1024:
        sisa = baca_ping(folder, nama)[-MAKS_PING_SIMPAN:]
        tmp = p + ".tmp%d" % os.getpid()
        with open(tmp, "w", encoding="utf-8") as f:
            for w, c in sisa:
                f.write("%s\t%s\n" % (iso_utc(w), c))
        os.replace(tmp, p)


# ---------------------------------------------------------------- evaluasi
def evaluasi(nama, j, pings, sekarang):
    """Status satu job pada waktu `sekarang` (aware UTC). Kembalikan dict."""
    spec, zona, tol, dibuat = validasi_job(nama, j)
    now = lantai_menit(ke_lokal(sekarang, zona))
    dibuat_l = ke_lokal(dibuat, zona)
    terakhir = pings[-1][0] if pings else None
    terakhir_l = ke_lokal(terakhir, zona) if terakhir else None

    batas_dikira = now - dt.timedelta(minutes=tol)   # jadwal S terlewat bila S < now - toleransi
    jatuh_tempo = sebelumnya(spec, batas_dikira, inklusif=False)
    terlewat = 0
    s = jatuh_tempo
    while s >= dibuat_l and (terakhir_l is None or s > terakhir_l) and terlewat < MAKS_TERLEWAT:
        terlewat += 1
        s = sebelumnya(spec, s, inklusif=False)
    kena_batas = terlewat >= MAKS_TERLEWAT

    if terlewat == 0:
        status = "OK"
    elif terlewat == 1 and terakhir is not None:
        status = "TERLAMBAT"
    else:
        status = "HILANG"
    menunggu = status == "OK" and terakhir is None and jatuh_tempo < dibuat_l
    nxt = berikutnya(spec, now)
    selisih_menit = int((now - jatuh_tempo).total_seconds() // 60)
    return {
        "nama": nama, "status": status, "jadwal": spec["teks"], "zona": zona, "toleransi_menit": tol,
        "ping_terakhir": iso_utc(terakhir) if terakhir else None,
        "ping_terakhir_lokal": fmt_waktu(terakhir_l, zona, now.year) if terakhir else None,
        "jadwal_jatuh_tempo": jatuh_tempo.strftime("%Y-%m-%dT%H:%M") + " " + zona if terlewat else None,
        "jadwal_jatuh_tempo_lokal": fmt_waktu(jatuh_tempo, zona, now.year),
        "terlewat": terlewat, "terlewat_minimal": kena_batas,
        "lewat_menit": selisih_menit if terlewat else 0,
        "jadwal_berikutnya": nxt.strftime("%Y-%m-%dT%H:%M") + " " + zona,
        "jadwal_berikutnya_lokal": fmt_waktu(nxt, zona, now.year),
        "menunggu_jadwal_pertama": menunggu,
        "terdaftar_lokal": fmt_waktu(dibuat_l, zona, now.year),
    }


def kalimat_masalah(h):
    jml = ("%d+" if h["terlewat_minimal"] else "%d") % h["terlewat"]
    if h["status"] == "TERLAMBAT":
        return ("%s %s: jadwal %s belum ada kabar \"selesai\", lewat %s dari jadwal (toleransi %d menit). Terakhir lapor selesai %s."
                % (h["status"], h["nama"], h["jadwal_jatuh_tempo_lokal"], fmt_durasi(h["lewat_menit"]),
                   h["toleransi_menit"], h["ping_terakhir_lokal"]))
    if h["ping_terakhir"] is None:
        return ("HILANG %s: belum pernah lapor selesai sejak didaftarkan (%s jadwal terlewat, terakhir %s). "
                "Cek apakah langkah \"lapor selesai\" sudah ditambahkan di akhir jadwal otomatis itu." % (h["nama"], jml, h["jadwal_jatuh_tempo_lokal"]))
    return ("HILANG %s: tidak ada lapor selesai sejak %s (%s jadwal terlewat, terakhir %s)."
            % (h["nama"], h["ping_terakhir_lokal"], jml, h["jadwal_jatuh_tempo_lokal"]))


def susun_laporan(hasil, sekarang, hanya_masalah=False, pulih=None, tersembunyi=None):
    """Teks laporan ringkas (ASCII) untuk Telegram. Kembalikan (teks, ada_kabar)."""
    pulih = pulih or []
    tersembunyi = tersembunyi or set()
    if not hasil:
        return "BELUM_ADA_JOB", False
    zona0 = hasil[0]["zona"]
    now0 = ke_lokal(sekarang, zona0)
    masalah = [h for h in hasil if h["status"] != "OK"]
    tampil = [h for h in masalah if h["nama"] not in tersembunyi]
    ok = [h for h in hasil if h["status"] == "OK"]
    if hanya_masalah and not tampil and not pulih:
        return ("SUDAH_DIKABARKAN" if masalah else "SEMUA_OK"), False
    judul = "PANTAU CRON - %s" % fmt_waktu(now0, zona0, None)
    baris = [judul]
    if tampil:
        baris.append("BERMASALAH (%d dari %d):" % (len(masalah), len(hasil)))
        baris += ["- " + kalimat_masalah(h) for h in tampil]
    elif not hanya_masalah:
        baris.append("Semua %d job aman." % len(hasil))
    for n in pulih:
        baris.append("PULIH %s: sudah lapor selesai lagi." % n)
    if not hanya_masalah:
        if ok:
            baris.append("OK (%d):" % len(ok))
        for h in ok:
            if h["menunggu_jadwal_pertama"]:
                baris.append("- %s: terdaftar sejak %s, jadwal pertama %s belum tiba." % (h["nama"], h["terdaftar_lokal"], h["jadwal_berikutnya_lokal"]))
            else:
                baris.append("- %s: terakhir lapor selesai %s; berikutnya %s." % (h["nama"], h["ping_terakhir_lokal"], h["jadwal_berikutnya_lokal"]))
    elif ok:
        baris.append("OK (%d): %s" % (len(ok), ", ".join(h["nama"] for h in ok)))
    return "\n".join(baris), True


# ---------------------------------------------------------------- perintah
def cmd_tambah(a):
    folder = folder_data(a.folder)
    nama = slug(a.nama)
    if a.jam:
        m = re.match(r"^(\d{1,2})[.:](\d{2})$", a.jam.strip())
        if not m or int(m.group(1)) > 23 or int(m.group(2)) > 59:
            raise GalatPantau("Jam '%s' tidak valid. Contoh: 21.00 atau 07:45." % a.jam)
        jadwal = "%d %d * * *" % (int(m.group(2)), int(m.group(1)))
    elif a.jadwal:
        jadwal = a.jadwal
    else:
        raise GalatPantau("Isi --jadwal (cron 5 kolom, mis. \"0 21 * * *\") atau --jam (harian, mis. 21.00).")
    spec = parse_cron(jadwal)
    zona = normal_zona(a.zona)
    sekarang = sekarang_utc(a.sekarang)
    now = lantai_menit(ke_lokal(sekarang, zona))
    n1 = berikutnya(spec, now)
    n2 = berikutnya(spec, n1)
    jarak = int((n2 - n1).total_seconds() // 60)
    if a.toleransi is None:
        tol = 30 if jarak > 60 else max(1, jarak // 2)
    else:
        tol = a.toleransi
    if tol < 1 or tol > MAKS_DUR_TOLERANSI:
        raise GalatPantau("Toleransi harus 1 sampai %d menit." % MAKS_DUR_TOLERANSI)
    data = muat_job(folder)
    lama = data["jobs"].get(nama)
    dilepas = _tidak_diawasi(lama)
    if dilepas and not a.ganti:
        lama = None   # job yang dilepas (hapus --terima-lapor) boleh diawasi lagi tanpa --ganti
    if lama is not None and not a.ganti:
        raise GalatPantau("Job '%s' sudah terdaftar. Tambahkan --ganti bila ingin menimpa pengaturannya." % nama)
    dibuat = iso_utc(sekarang)
    catatan_riwayat = None
    if lama is not None:
        # Riwayat lapor selesai (berkas ping) TIDAK pernah dihapus oleh --ganti.
        # Hitungan terlewat dipertahankan bila jadwal & zona sama, kecuali --mulai-ulang.
        sama = isinstance(lama, dict) and lama.get("jadwal") == spec["teks"] and lama.get("zona") == zona
        try:
            dibuat_lama = iso_utc(baca_waktu_utc(lama.get("dibuat"))) if isinstance(lama, dict) else None
        except GalatPantau:
            dibuat_lama = None
        if dilepas:
            # Selama dilepas, lapor selesai sengaja tidak dicatat: hitungan lama tidak boleh dipakai
            # (akan menimbulkan HILANG palsu untuk seluruh masa tidak diawasi), walau jadwal sama.
            catatan_riwayat = ("Job ini sempat tidak diawasi: hitungan terlewat dimulai dari sekarang; "
                               "riwayat lapor selesai tetap disimpan.")
        elif sama and dibuat_lama and not a.mulai_ulang:
            dibuat = dibuat_lama
            catatan_riwayat = "Riwayat dan hitungan lama dipertahankan (jadwal sama)."
        elif a.mulai_ulang:
            catatan_riwayat = "Hitungan terlewat dimulai ulang dari sekarang; riwayat lapor selesai tetap disimpan."
        else:
            catatan_riwayat = "Jadwal/zona berubah: hitungan terlewat dimulai dari sekarang; riwayat lapor selesai tetap disimpan."
    elif a.mulai_ulang:
        raise GalatPantau("--mulai-ulang hanya untuk job yang sudah terdaftar (bersama --ganti).")
    data["jobs"][nama] = {"jadwal": spec["teks"], "zona": zona, "toleransi_menit": tol, "dibuat": dibuat}
    simpan_job(folder, data)
    print("Terdaftar: %s | jadwal \"%s\" %s | toleransi %d menit | jadwal berikutnya %s"
          % (nama, spec["teks"], zona, tol, fmt_waktu(n1, zona, now.year)))
    if catatan_riwayat:
        print(catatan_riwayat)
    if tol >= jarak:
        print("Peringatan: toleransi (%d menit) >= jarak antar jadwal (%d menit); kecilkan toleransi agar keterlambatan terdeteksi."
              % (tol, jarak))
    print("Berikutnya: tambahkan langkah \"lapor selesai\" di akhir job %s agar pantauan tahu job ini sukses." % nama)


def _tidak_diawasi(j):
    return isinstance(j, dict) and j.get("diawasi") is False


def cmd_hapus(a):
    folder = folder_data(a.folder)
    nama = slug(a.nama)
    data = muat_job(folder)
    if nama not in data["jobs"]:
        raise GalatPantau("Job '%s' tidak ada. Lihat daftar dengan perintah daftar." % nama)
    if a.terima_lapor:
        # Lapor selesai ada di perintah buatan pemilik: job dilepas dari pengawasan, tetapi `ping`
        # tetap diterima (kode keluar 0) supaya jadwal/rantai perintah pemilik tidak tercatat gagal.
        j = data["jobs"][nama]
        if not isinstance(j, dict):
            j = {}
        j["diawasi"] = False
        data["jobs"][nama] = j
        simpan_job(folder, data)
        if a.hapus_riwayat and os.path.exists(_path_log(folder, nama)):
            os.remove(_path_log(folder, nama))
        print("Job '%s' tidak diawasi lagi; lapor selesai dari perintahnya tetap diterima tanpa galat dan tanpa kabar." % nama)
        return
    del data["jobs"][nama]
    simpan_job(folder, data)
    p = _path_log(folder, nama)
    if a.hapus_riwayat and os.path.exists(p):
        os.remove(p)
    print("Job '%s' dihapus dari pantauan%s." % (nama, " (riwayat lapor selesai ikut dihapus)" if a.hapus_riwayat else "; riwayat lapor selesai dibiarkan"))


def _url_luar(folder, nama):
    try:
        d = _baca_json(os.path.join(folder, "healthchecks.json"), {})
    except GalatPantau:
        return None
    u = d.get(nama)
    if isinstance(u, str) and re.match(r"^https?://\S+$", u.strip()):
        return u.strip()
    return None


def _lapor_selesai(folder, nama, w, catatan="", tanpa_luar=False, keluar=sys.stdout):
    """Catat lapor selesai + (opsional) kabar ke layanan luar milik pengguna. Pesan ke `keluar` (None = diam)."""
    if keluar is None:
        with open(os.devnull, "w") as diam:
            return _lapor_selesai(folder, nama, w, catatan, tanpa_luar, diam)
    data = muat_job(folder)
    if nama not in data["jobs"]:
        raise GalatPantau("Job '%s' belum terdaftar, lapor selesai tidak dicatat. Daftarkan dulu dengan perintah tambah (nama, jadwal, zona)."
                          % nama)
    if _tidak_diawasi(data["jobs"][nama]):
        # Diam total (kode keluar 0): keluaran job perintah bisa sampai ke chat.
        return
    catat_ping(folder, nama, w, catatan)
    zona = normal_zona(data["jobs"][nama].get("zona"))
    print("Lapor selesai dicatat: %s pada %s" % (nama, fmt_waktu(ke_lokal(w, zona), zona)), file=keluar)
    url = None if tanpa_luar else _url_luar(folder, nama)
    if url:
        try:
            urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "pantau-cron"}), timeout=8).read(64)
            print("Kabar ke layanan luar milik Anda: terkirim.", file=keluar)
        except Exception:   # jaringan mati tidak boleh membuat job utama gagal
            print("Peringatan: kabar ke layanan luar gagal (jaringan/alamat). Catatan di komputer Anda tetap tersimpan.", file=sys.stderr)


def cmd_ping(a):
    _lapor_selesai(folder_data(a.folder), slug(a.nama), sekarang_utc(a.sekarang), a.catatan, a.tanpa_luar)


# ---------------------------------------------------------------- job-perintah (--command-argv)
def _argv_dari_teks(teks):
    if teks == "-":
        teks = sys.stdin.read()
    try:
        argv = json.loads(teks)
    except ValueError:
        raise GalatPantau("Isi --argv-lama harus daftar JSON persis seperti di daftar jadwal, mis. "
                          "[\"python3\", \"/rumah/laporan.py\", \"--hari\", \"ini\"].")
    if not isinstance(argv, list) or not argv or not all(isinstance(x, str) for x in argv) or argv[0] == "":
        raise GalatPantau("--argv-lama harus daftar JSON berisi teks (minimal satu, yang pertama tidak kosong).")
    return argv


def _posisi_bungkus(argv):
    """Indeks '--' pemisah bila argv adalah hasil `bungkus` (… pantau_cron.py jalankan <nama> … -- <argv lama>)."""
    for i in range(len(argv) - 1):
        if argv[i].replace("\\", "/").endswith("pantau_cron.py") and argv[i + 1] == "jalankan":
            if "--" in argv[i + 2:]:
                return argv.index("--", i + 2)
    return None


def _ada_ping_milik_pemilik(argv):
    return any("pantau_cron.py" in x and re.search(r"\bping\b", x) for x in argv) or (
        any(x.replace("\\", "/").endswith("pantau_cron.py") for x in argv) and "ping" in argv)


def cmd_bungkus(a):
    argv = _argv_dari_teks(a.argv_lama)
    pos = _posisi_bungkus(argv)
    if a.buang:
        if pos is None:
            if _ada_ping_milik_pemilik(argv):
                raise GalatPantau("Lapor selesai di job ini ada di dalam perintah atau berkas milik Anda sendiri, bukan bungkus "
                                  "pantauan. Saya tidak mengubahnya; bila ingin dihapus, ubah sendiri bagian itu.")
            print("Job ini tidak dibungkus pantauan; perintahnya dibiarkan apa adanya.", file=sys.stderr)
            hasil = argv
        else:
            hasil = argv[pos + 1:]
            if not hasil:
                raise GalatPantau("Bungkus pantauan tidak berisi perintah lama; tidak ada yang bisa dikembalikan.")
    else:
        nama = slug(a.nama or "")
        if pos is not None:
            print("Job ini sudah dibungkus pantauan; tidak dibungkus dua kali.", file=sys.stderr)
            hasil = argv
        elif _ada_ping_milik_pemilik(argv):
            raise GalatPantau("Perintah job ini sudah memuat lapor selesai sendiri; jangan ditambah lagi (tercatat dua kali).")
        else:
            hasil = [a.python or sys.executable or "python3", os.path.abspath(__file__), "jalankan", nama]
            if a.folder or os.environ.get("PANTAU_CRON_DIR"):
                hasil += ["--folder", folder_data(a.folder)]
            hasil += ["--"] + argv
            try:
                if nama not in muat_job(folder_data(a.folder))["jobs"]:
                    print("Peringatan: job '%s' belum terdaftar di pantauan; daftarkan dengan perintah tambah." % nama, file=sys.stderr)
            except GalatPantau:
                pass
    teks = json.dumps(hasil, ensure_ascii=False)
    if a.id:
        print("openclaw automations edit %s --command-argv %s" % (shlex.quote(a.id), shlex.quote(teks)))
    else:
        print(teks)


def cmd_jalankan(a):
    argv = list(a.argv)
    if not argv:
        raise GalatPantau("Tidak ada perintah yang dijalankan (tulis setelah --).")
    sys.stdout.flush()
    try:
        kode = subprocess.run(argv).returncode
    except OSError as e:
        print("GALAT: perintah job tidak bisa dijalankan (%s). Lapor selesai tidak dicatat." % e.strerror, file=sys.stderr)
        return 127
    if kode < 0:
        kode = 128 - kode   # dimatikan sinyal: ikuti kebiasaan shell (128 + nomor sinyal), bukan angka negatif
    if kode == 0:
        try:   # keluaran job tetap milik job: sukses = diam total (tidak ada teks pantauan di stdout/stderr)
            _lapor_selesai(folder_data(a.folder), slug(a.nama), sekarang_utc(a.sekarang), "", False, keluar=None)
        except GalatPantau as e:
            print("Peringatan pantauan: %s" % e, file=sys.stderr)
    return kode


def _hitung_semua(folder, sekarang):
    data = muat_job(folder)
    hasil = [evaluasi(n, j, baca_ping(folder, n), sekarang) for n, j in sorted(data["jobs"].items())
             if not _tidak_diawasi(j)]
    return hasil


def cmd_daftar(a):
    folder = folder_data(a.folder)
    sekarang = sekarang_utc(a.sekarang)
    data = muat_job(folder)
    hasil = _hitung_semua(folder, sekarang)
    for h in hasil:
        h["layanan_luar"] = _url_luar(folder, h["nama"]) is not None
    dilepas = sorted(n for n, j in data["jobs"].items() if _tidak_diawasi(j))
    if a.json:
        print(json.dumps({"folder": folder, "jobs": hasil, "tidak_diawasi": dilepas}, ensure_ascii=False, indent=2))
        return
    print("Folder data Anda: %s" % ("(folder pilihan Anda)" if a.folder or os.environ.get("PANTAU_CRON_DIR") else "(folder bawaan di komputer Anda)"))
    if dilepas:
        print("Tidak diawasi lagi (lapor selesai tetap diterima tanpa galat): %s" % ", ".join(dilepas))
    if not hasil:
        print("Belum ada job terdaftar. Tambahkan dengan perintah tambah (nama + jadwal, mis. tiap hari 21.00).")
        return
    for h in hasil:
        print("- %s | \"%s\" %s | toleransi %d mnt | terakhir lapor selesai: %s | berikutnya %s | terdaftar sejak %s%s"
              % (h["nama"], h["jadwal"], h["zona"], h["toleransi_menit"], h["ping_terakhir_lokal"] or "belum ada",
                 h["jadwal_berikutnya_lokal"], h["terdaftar_lokal"], " | layanan luar: ya" if h["layanan_luar"] else ""))


def cmd_cek(a):
    if a.openclaw:
        a.hanya_masalah = True
    folder = folder_data(a.folder)
    sekarang = sekarang_utc(a.sekarang)
    hasil = _hitung_semua(folder, sekarang)
    pulih, tersembunyi = [], set()
    alarm_path = os.path.join(folder, "alarm.json")
    alarm = _baca_json(alarm_path, {}) if (a.hanya_masalah and not a.tanpa_catat) else {}
    if a.hanya_masalah and not a.tanpa_catat:
        baru = {}
        for h in hasil:
            lama = alarm.get(h["nama"])
            if h["status"] == "OK":
                if isinstance(lama, dict):
                    pulih.append(h["nama"])
                continue
            try:
                umur = (sekarang - baca_waktu_utc(lama["waktu"])).total_seconds() / 3600.0 if isinstance(lama, dict) else None
            except (GalatPantau, KeyError, TypeError):
                umur = None
            if isinstance(lama, dict) and lama.get("status") == h["status"] and umur is not None and 0 <= umur < a.ulang_jam:
                tersembunyi.add(h["nama"])
                baru[h["nama"]] = lama
            else:
                baru[h["nama"]] = {"status": h["status"], "waktu": iso_utc(sekarang)}
        if baru != alarm:
            _tulis_atomik(alarm_path, baru)
    if a.json:
        print(json.dumps({"waktu": iso_utc(sekarang), "ada_masalah": any(h["status"] != "OK" for h in hasil),
                          "pulih": pulih, "sudah_dikabarkan": sorted(tersembunyi), "jobs": hasil},
                         ensure_ascii=False, indent=2))
    else:
        teks, _ = susun_laporan(hasil, sekarang, a.hanya_masalah, pulih, tersembunyi)
        if a.openclaw and teks in ("SEMUA_OK", "SUDAH_DIKABARKAN", "BELUM_ADA_JOB"):
            teks = "NO_REPLY"     # OpenClaw tidak mengirim apa pun bila keluaran job persis NO_REPLY
        print(teks)
    if a.kode_keluar and not a.openclaw and any(h["status"] != "OK" for h in hasil):
        sys.exit(2)


def cmd_riwayat(a):
    folder = folder_data(a.folder)
    nama = slug(a.nama)
    data = muat_job(folder)
    if nama not in data["jobs"]:
        raise GalatPantau("Job '%s' tidak ada. Lihat daftar dengan perintah daftar." % nama)
    spec, zona, tol, _ = validasi_job(nama, data["jobs"][nama])
    pings = baca_ping(folder, nama)[-max(1, a.n):][::-1]
    baris = []
    for w, c in pings:
        wl = ke_lokal(w, zona)
        s = sebelumnya(spec, wl)
        d = int((wl - s).total_seconds() // 60)
        baris.append({"waktu": iso_utc(w), "waktu_lokal": fmt_waktu(wl, zona),
                      "jadwal_terdekat": s.strftime("%Y-%m-%dT%H:%M"), "selisih_menit": d,
                      "dalam_toleransi": d <= tol, "catatan": c})
    if a.json:
        print(json.dumps({"nama": nama, "riwayat": baris}, ensure_ascii=False, indent=2))
        return
    if not baris:
        print("Job '%s' belum pernah lapor selesai." % nama)
        return
    print("Riwayat lapor selesai %s (terbaru dulu):" % nama)
    for b in baris:
        ket = ("sesuai jadwal (+%d mnt)" % b["selisih_menit"]) if b["dalam_toleransi"] else (
            "di luar toleransi (+%s dari jadwal %s)" % (fmt_durasi(b["selisih_menit"]), b["jadwal_terdekat"][11:].replace(":", ".")))
        print("- %s | %s%s" % (b["waktu_lokal"], ket, (" | " + b["catatan"]) if b["catatan"] else ""))


# ---------------------------------------------------------------- CLI
def bangun_parser():
    umum = argparse.ArgumentParser(add_help=False)
    umum.add_argument("--folder", help="folder data (default ~/pantau-cron atau PANTAU_CRON_DIR)")
    umum.add_argument("--sekarang", help="(uji/simulasi) waktu ISO, mis. 2026-10-12T21:40+07:00; tanpa offset = WIB")
    p = argparse.ArgumentParser(description="Pantau job terjadwal ala dead man's switch (data lokal).")
    p.add_argument("--versi", action="version", version=VERSI)
    sub = p.add_subparsers(dest="perintah", required=True)

    s = sub.add_parser("tambah", parents=[umum], help="daftarkan job")
    s.add_argument("nama")
    s.add_argument("--jadwal", help='cron 5 kolom, mis. "0 21 * * *"')
    s.add_argument("--jam", help="jalan tiap hari pada jam ini, mis. 21.00 (alternatif --jadwal)")
    s.add_argument("--zona", default="WIB", help="WIB (default), WITA, WIT, UTC")
    s.add_argument("--toleransi", type=int, help="menit boleh terlambat (default 30, atau separuh jarak jadwal bila rapat)")
    s.add_argument("--ganti", action="store_true",
                   help="timpa pengaturan job yang sudah ada; riwayat lapor selesai selalu disimpan, hitungan lama "
                        "dipertahankan bila jadwal & zona sama (job yang sempat dilepas selalu mulai dari sekarang)")
    s.add_argument("--mulai-ulang", action="store_true",
                   help="(bersama --ganti) mulai ulang hitungan terlewat dari sekarang; riwayat tetap disimpan")
    s.set_defaults(f=cmd_tambah)

    s = sub.add_parser("hapus", parents=[umum], help="berhenti memantau job")
    s.add_argument("nama")
    s.add_argument("--hapus-riwayat", action="store_true")
    s.add_argument("--terima-lapor", action="store_true",
                   help="lapor selesai ada di perintah buatan pemilik: lepas dari pengawasan, tetapi ping tetap diterima (kode 0)")
    s.set_defaults(f=cmd_hapus)

    s = sub.add_parser("daftar", parents=[umum], help="tampilkan semua job")
    s.add_argument("--json", action="store_true")
    s.set_defaults(f=cmd_daftar)

    s = sub.add_parser("ping", parents=[umum], help="catat bahwa job baru saja sukses (panggil di akhir job)")
    s.add_argument("nama")
    s.add_argument("--catatan", default="")
    s.add_argument("--tanpa-luar", action="store_true", help="jangan ping layanan luar walau healthchecks.json ada")
    s.set_defaults(f=cmd_ping)

    s = sub.add_parser("cek", parents=[umum], help="bandingkan ping terakhir dengan jadwal + toleransi")
    s.add_argument("--hanya-masalah", action="store_true",
                   help="keluarkan laporan HANYA bila ada TERLAMBAT/HILANG/PULIH; selain itu satu kata (SEMUA_OK dst.)")
    s.add_argument("--ulang-jam", type=float, default=6.0, help="jangan kabarkan masalah yang sama lagi dalam N jam (default 6)")
    s.add_argument("--tanpa-catat", action="store_true", help="jangan simpan ingatan alarm (alarm.json)")
    s.add_argument("--kode-keluar", action="store_true", help="keluar dengan kode 2 bila ada masalah")
    s.add_argument("--openclaw", action="store_true",
                   help="untuk job-perintah OpenClaw: seperti --hanya-masalah, tetapi saat tenang mencetak NO_REPLY (tidak dikirim), selalu kode 0")
    s.add_argument("--json", action="store_true")
    s.set_defaults(f=cmd_cek)

    s = sub.add_parser("bungkus", parents=[umum],
                       help="susun --command-argv baru: argv lama utuh + lapor selesai (atau --buang untuk mengembalikan)")
    s.add_argument("nama", nargs="?", help="nama job di pantauan (wajib kecuali --buang)")
    s.add_argument("--argv-lama", required=True, help="argv job sekarang, daftar JSON persis dari daftar jadwal; '-' = baca stdin")
    s.add_argument("--buang", action="store_true", help="kembalikan argv lama persis (berhenti memantau job ini)")
    s.add_argument("--id", help="cetak perintah edit OpenClaw lengkap dengan kutip yang benar (shell POSIX)")
    s.add_argument("--python", help="program Python untuk argv baru (default: Python yang menjalankan perintah ini)")
    s.set_defaults(f=cmd_bungkus)

    s = sub.add_parser("jalankan", parents=[umum],
                       help="(dipakai argv hasil bungkus) jalankan argv lama, lapor selesai bila kode keluar 0")
    s.add_argument("nama")
    s.add_argument("argv", nargs="*", help="tulis sesudah --: argv lama job, utuh")
    s.set_defaults(f=cmd_jalankan)

    s = sub.add_parser("riwayat", parents=[umum], help="ping terakhir sebuah job")
    s.add_argument("nama")
    s.add_argument("-n", type=int, default=20)
    s.add_argument("--json", action="store_true")
    s.set_defaults(f=cmd_riwayat)
    return p


def main(argv=None):
    for st in (sys.stdout, sys.stderr):
        try:
            st.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass
    argv = list(sys.argv[1:] if argv is None else argv)
    sisa = None
    if argv[:1] == ["jalankan"] and "--" in argv:
        # semua sesudah '--' pertama = argv lama job, dilewatkan utuh tanpa ditafsirkan
        i = argv.index("--")
        argv, sisa = argv[:i], argv[i + 1:]
    a = bangun_parser().parse_args(argv)
    if sisa is not None:
        a.argv = sisa
    if a.perintah == "bungkus" and not a.buang and not a.nama:
        print("GALAT: nama job wajib diisi (kecuali --buang).", file=sys.stderr)
        return 1
    try:
        kode = a.f(a)
    except GalatPantau as e:
        print("GALAT: %s" % e, file=sys.stderr)
        return 1
    return kode if isinstance(kode, int) else 0


if __name__ == "__main__":
    sys.exit(main())
