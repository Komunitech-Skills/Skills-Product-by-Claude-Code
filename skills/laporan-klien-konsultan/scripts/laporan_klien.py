#!/usr/bin/env python3
"""laporan-klien-konsultan (Komunitech) - log kerja lokal + draf laporan progres per klien.

Untuk konsultan/freelancer (pajak, hukum, IT, desain, marketing, dst.) yang harus rutin
mengirim laporan progres ke klien. Semua data disimpan di SATU file CSV lokal (tidak ada
database eksternal, tidak ada akun, tidak ada kirim data ke mana pun). Hanya library
standar Python 3.8+, lintas OS (Windows: `python`/`py`).

Skema kolom log (satu baris = satu pekerjaan yang dicatat):
  tanggal,klien,proyek,pekerjaan,jam,status,kendala,butuh_dari_klien
  - tanggal: YYYY-MM-DD
  - status: selesai | berjalan | terkendala
  - jam: opsional, boleh kosong (mis. konsultasi tanpa hitungan jam)
  - kendala: hambatan di pihak konsultan (opsional)
  - butuh_dari_klien: sesuatu yang perlu klien berikan/putuskan (opsional)

Lokasi file log (urutan prioritas):
  1. --file PATH
  2. ENV KOMUNITECH_LAPORAN_KLIEN_FILE
  3. default: log-kerja-klien.csv (folder kerja saat ini)

Perintah tulis (`catat`) langsung menambah baris (auto-membuat file+header bila belum ada).
Perintah baca (`laporan`, `daftar-klien`) tidak pernah mengubah file.

Sejak 1.0.5 pembacaan file toleran, sehingga file catatan milik pengguna sendiri bisa langsung
dipakai dengan `--file catatan-saya.csv` (tanpa menyalin baris satu per satu):
  - pemisah koma, titik koma, tab, atau |; BOM UTF-8/UTF-16; encoding Windows (cp1252)
  - header umum ID/EN (Tanggal/Date, Klien/Client, Kerjaan/Kegiatan/Task, Durasi/Hours, ...)
  - durasi "2,5 jam", "90 menit", "1 jam 30 menit", "1:30", "2h", "45m", "2.5"
  - tanggal 2026-09-22, 22/09/2026, 22-09-2026, 22 Sep 2026, 22 September 2026
  - kolom opsional Keterangan/Catatan dan Rencana/Next step
Jam disimpan & ditampilkan sampai 2 desimal (menit dibulatkan per baris), dan total jam =
penjumlahan persis jam per baris yang tampil.

Contoh:
  python3 laporan_klien.py catat --klien "PT Maju Jaya" --proyek "Pembukuan bulanan" \\
      --pekerjaan "Rekonsiliasi bank September" --jam 2.5 --status selesai
  python3 laporan_klien.py catat --klien "PT Maju Jaya" --proyek "Pembukuan bulanan" \\
      --pekerjaan "Susun draf SPT Masa PPN" --status berjalan \\
      --butuh-klien "Faktur pajak masukan Oktober belum dikirim"
  python3 laporan_klien.py laporan --klien "PT Maju Jaya" --periode mingguan \\
      --rencana "Selesaikan draf SPT Masa" --rencana "Jadwalkan review dengan klien" --json

Kode keluar: 0 = normal. 1 = input/file tidak valid. 2 = argumen salah tulis.
3 = draf berhasil dibuat TAPI ada pola mirip data pribadi/rahasia terdeteksi di salah satu
    kolom teks -- lihat pesan di stderr, TINJAU ULANG sebelum dikirim ke klien (lihat SKILL.md).
"""
import argparse
import csv
import json
import os
import re
import sys
from datetime import date, datetime, timedelta
from pathlib import Path

APLIKASI = "laporan-klien-konsultan"
VERSI = "1.0.5"
SKEMA = 1

KOLOM = ["tanggal", "klien", "proyek", "pekerjaan", "jam", "status", "kendala", "butuh_dari_klien"]
STATUS_VALID = ("selesai", "berjalan", "terkendala")
LABEL_STATUS = {"selesai": "Selesai", "berjalan": "Berjalan", "terkendala": "Terkendala"}

BULAN = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli",
         "Agustus", "September", "Oktober", "November", "Desember"]
NAMA_BULAN = {"jan": 1, "feb": 2, "peb": 2, "mar": 3, "apr": 4, "mei": 5, "may": 5, "jun": 6,
              "jul": 7, "agu": 8, "agt": 8, "aug": 8, "sep": 9, "okt": 10, "oct": 10,
              "nov": 11, "nop": 11, "des": 12, "dec": 12}
HARI = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"]

# Pola deteksi data pribadi/rahasia klien -- deteksi saja (tidak memblokir), sama seperti
# skill laporan-otomatis-terjadwal. Batas kata (\b) supaya tidak salah kena kata yang cuma
# "kebetulan mengandung" polanya (mis. "unik" tidak kena "nik").
POLA_SENSITIF = [
    ("NIK", re.compile(r"\bnik\b", re.IGNORECASE)),
    ("nomor KTP", re.compile(r"\b(no\.?\s*ktp|nomor\s*ktp|ktp)\b", re.IGNORECASE)),
    ("nomor HP/telepon (angka)", re.compile(
        r"(?<![\w+\-/#])\(?(\+62|62|0)[\s.\-]?8\d{1,3}\)?(?:[\s.\-]?\d){6,10}(?![\w])")),
    ("email pribadi", re.compile(r"\b[\w.+-]+@[\w-]+\.[a-zA-Z]{2,}\b")),
    ("kata sandi/kredensial", re.compile(
        r"\b(password|kata\s*sandi|kredensial|api\s*key|access\s*token|secret\s*key)\b",
        re.IGNORECASE)),
    ("dokumen rahasia disebut eksplisit", re.compile(r"\brahasia\b", re.IGNORECASE)),
]


class Gagal(Exception):
    def __init__(self, pesan, **detail):
        super().__init__(pesan)
        self.pesan = pesan
        self.detail = detail


# ---------------------------------------------------------------------------
# Util umum
# ---------------------------------------------------------------------------

def cari_file(arg_file):
    if arg_file:
        return Path(arg_file).expanduser()
    env = os.environ.get("KOMUNITECH_LAPORAN_KLIEN_FILE")
    if env:
        return Path(env).expanduser()
    return Path("log-kerja-klien.csv")


def aman_csv(teks):
    """Cegah formula injection bila file dibuka di Excel/Sheets (=, +, -, @ di awal sel)."""
    teks = "" if teks is None else str(teks)
    if teks[:1] in ("=", "+", "-", "@"):
        return "'" + teks
    return teks


def baca_tanggal(teks, acuan=None):
    acuan = acuan or date.today()
    if teks is None:
        return acuan
    t = teks.strip().lower()
    if t in ("", "hari-ini", "hariini", "today"):
        return acuan
    if t in ("kemarin", "yesterday"):
        return acuan - timedelta(days=1)
    bersih = teks.strip()
    # Excel kadang menulis "2026-09-22 00:00:00"
    if re.match(r"^\d{4}-\d{2}-\d{2}[ T]\d{1,2}:\d{2}", bersih):
        bersih = bersih[:10]
    for fmt in ("%Y-%m-%d", "%d-%m-%Y", "%d/%m/%Y", "%d/%m/%y", "%d-%m-%y", "%Y/%m/%d",
                "%d.%m.%Y"):
        try:
            return datetime.strptime(bersih, fmt).date()
        except ValueError:
            continue
    m = re.match(r"^(?:[A-Za-z]+,?\s+)?(\d{1,2})\s+([A-Za-z]+)\.?\s+(\d{4})$", bersih)
    if m:
        bln = NAMA_BULAN.get(m.group(2).lower()[:3])
        if bln:
            try:
                return date(int(m.group(3)), bln, int(m.group(1)))
            except ValueError:
                pass
    raise Gagal(f"Tanggal '{teks}' tidak dikenali. Pakai format YYYY-MM-DD (mis. 2026-09-24), "
                "DD/MM/YYYY (mis. 24/09/2026), '24 Sep 2026', 'hari-ini', atau 'kemarin'.")


_SATUAN_JAM = ("jam", "j", "h", "hr", "hrs", "hour", "hours")
_SATUAN_MENIT = ("menit", "mnt", "m", "min", "mins", "minute", "minutes")
_POLA_DURASI = re.compile(r"(-?\d+(?:[.,]\d+)?)\s*([a-z]*)")


def _angka(teks):
    return float(teks.replace(",", "."))


def parse_jam(teks):
    """Baca durasi jadi jam desimal, dibulatkan 2 desimal (supaya total = jumlah yang tampil).

    Menerima: 2 | 2.5 | 2,5 | "2,5 jam" | "90 menit" | "1 jam 30 menit" | "1:30" | "2h" | "45m".
    """
    if teks is None or str(teks).strip() == "":
        return None
    asli = str(teks).strip()
    t = asli.lower().strip()
    nilai = None
    m = re.match(r"^(\d{1,2}):(\d{2})$", t)
    if m:
        nilai = int(m.group(1)) + int(m.group(2)) / 60
    else:
        try:
            nilai = _angka(t)
        except ValueError:
            potongan = _POLA_DURASI.findall(t)
            sisa = _POLA_DURASI.sub("", t).replace("dan", "").replace("&", "")
            if potongan and not sisa.strip(" .,+"):
                total = 0.0
                for angka, satuan in potongan:
                    if satuan in _SATUAN_JAM or satuan == "":
                        total += _angka(angka)
                    elif satuan in _SATUAN_MENIT:
                        total += _angka(angka) / 60
                    else:
                        total = None
                        break
                nilai = total
    if nilai is None:
        raise Gagal(f"Jam '{asli}' tidak dikenali. Contoh yang benar: 2 | 2,5 | 2.5 | "
                    "'2,5 jam' | '90 menit' | '1 jam 30 menit' | '1:30'.")
    if nilai < 0:
        raise Gagal("Jam tidak boleh negatif.")
    if nilai > 24:
        raise Gagal(f"Jam '{asli}' tidak masuk akal untuk satu pekerjaan (>24 jam). "
                     "Pecah jadi beberapa baris `catat` bila memang lintas hari.")
    return round(nilai + 1e-9, 2)


def jumlah_jam(daftar):
    """Jumlah persis jam 2-desimal (dihitung dalam satuan seperseratus jam, tanpa galat float)."""
    return sum(int(round(j * 100)) for j in daftar) / 100


def format_jam(nilai):
    """Tampilkan sampai 2 desimal dengan koma (3,25 jam), tanpa pembulatan ulang."""
    if nilai is None:
        return "-"
    nilai = round(float(nilai), 2)
    if nilai.is_integer():
        return f"{int(nilai)} jam"
    return f"{nilai:.2f}".rstrip("0").rstrip(".").replace(".", ",") + " jam"


def format_jam_menit(nilai):
    """'9,75 jam (9 jam 45 menit)' bila menitnya bulat; selain itu sama dengan format_jam."""
    dasar = format_jam(nilai)
    if nilai is None or float(nilai).is_integer():
        return dasar
    menit_total = float(nilai) * 60
    if abs(menit_total - round(menit_total)) > 1e-6:
        return dasar
    j, mn = divmod(int(round(menit_total)), 60)
    teks = (f"{j} jam {mn} menit" if j else f"{mn} menit")
    return f"{dasar} ({teks})"


def normalisasi_status(teks):
    t = re.sub(r"[^\w\s-]", "", (teks or "").lower()).strip() or "berjalan"
    alias = {
        "selesai": "selesai", "done": "selesai", "tuntas": "selesai", "beres": "selesai",
        "berjalan": "berjalan", "progress": "berjalan", "in progress": "berjalan",
        "sedang berjalan": "berjalan", "ongoing": "berjalan", "on progress": "berjalan",
        "in-progress": "berjalan", "proses": "berjalan", "dalam proses": "berjalan",
        "dikerjakan": "berjalan", "sedang dikerjakan": "berjalan", "belum selesai": "berjalan",
        "wip": "berjalan", "completed": "selesai", "complete": "selesai", "ok": "selesai",
        "terkendala": "terkendala", "kendala": "terkendala", "stuck": "terkendala",
        "blocked": "terkendala", "tertunda": "terkendala",
    }
    if t not in alias:
        raise Gagal(f"Status '{teks}' tidak dikenali. Pakai salah satu: {', '.join(STATUS_VALID)}.")
    return alias[t]


def tanggal_indo(d):
    return f"{HARI[d.weekday()]}, {d.day} {BULAN[d.month - 1]} {d.year}"


def format_periode_label(d1, d2):
    if d1 == d2:
        return tanggal_indo(d1)
    return f"{d1.day} {BULAN[d1.month - 1]} {d1.year} - {d2.day} {BULAN[d2.month - 1]} {d2.year}"


def judul_periode(label_periode, awal, akhir):
    """'Minggu ini (21 September 2026 - 27 September 2026)' atau, untuk rentang kustom
    (label kosong), cukup '22 September 2026 - 26 September 2026' -- tanpa kata ganda."""
    rentang = format_periode_label(awal, akhir)
    return f"{label_periode} ({rentang})" if label_periode else rentang


def rentang_periode(nama, acuan):
    nama = (nama or "minggu-ini").strip().lower()
    if nama in ("mingguan",):
        nama = "minggu-ini"
    if nama in ("bulanan",):
        nama = "bulan-ini"
    if nama == "minggu-ini":
        a = acuan - timedelta(days=acuan.weekday())
        return "Minggu ini", a, a + timedelta(days=6)
    if nama == "minggu-lalu":
        a = acuan - timedelta(days=acuan.weekday() + 7)
        return "Minggu lalu", a, a + timedelta(days=6)
    if nama == "bulan-ini":
        a = acuan.replace(day=1)
        akhir_bulan = (a.replace(month=a.month % 12 + 1, day=1) if a.month != 12
                       else a.replace(year=a.year + 1, month=1, day=1)) - timedelta(days=1)
        return f"Bulan {BULAN[a.month - 1]} {a.year}", a, akhir_bulan
    if nama == "bulan-lalu":
        pertama_bulan_ini = acuan.replace(day=1)
        akhir_bulan_lalu = pertama_bulan_ini - timedelta(days=1)
        a = akhir_bulan_lalu.replace(day=1)
        return f"Bulan {BULAN[a.month - 1]} {a.year}", a, akhir_bulan_lalu
    raise Gagal("--periode harus salah satu: mingguan, bulanan, minggu-ini, minggu-lalu, "
                "bulan-ini, bulan-lalu (atau pakai --dari/--sampai).")


def deteksi_sensitif(teks, sumber, temuan_keluar):
    if not teks:
        return
    for nama_pola, pola in POLA_SENSITIF:
        if pola.search(teks):
            temuan_keluar.append(
                f"{sumber} berisi '{teks}' -- mengandung pola mirip {nama_pola}. Sesuai UU PDP "
                "(UU 27/2022), catat seperlunya saja dan tinjau ulang sebelum draf ini dikirim "
                "ke klien atau disimpan lebih lama dari perlu."
            )


# ---------------------------------------------------------------------------
# Baca/tulis log
# ---------------------------------------------------------------------------

def pastikan_file(path):
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", newline="", encoding="utf-8") as f:
            csv.writer(f).writerow(KOLOM)
        return True
    return False


ALIAS_KOLOM = {
    "tanggal": ("tanggal", "tgl", "date", "hari tanggal", "hari/tanggal", "tanggal kerja",
                "tanggal pekerjaan", "day"),
    "klien": ("klien", "client", "customer", "pelanggan", "nama klien", "client name",
              "perusahaan", "company"),
    "proyek": ("proyek", "projek", "project", "nama proyek", "project name", "layanan",
               "service", "job"),
    "pekerjaan": ("pekerjaan", "kerjaan", "kegiatan", "aktivitas", "aktifitas", "activity",
                  "task", "tugas", "deskripsi", "description", "uraian", "uraian pekerjaan",
                  "item", "work", "detail pekerjaan"),
    "jam": ("jam", "durasi", "duration", "hours", "hour", "hrs", "jumlah jam", "lama",
            "waktu", "time", "time spent", "jam kerja"),
    "status": ("status", "progress", "progres", "keadaan", "state"),
    "kendala": ("kendala", "hambatan", "blocker", "blockers", "issue", "issues", "masalah"),
    "butuh_dari_klien": ("butuh dari klien", "kebutuhan klien", "butuh klien",
                         "need from client", "needs from client", "waiting on client",
                         "menunggu klien"),
    "keterangan": ("keterangan", "ket", "catatan", "notes", "note", "remarks", "komentar",
                   "comment", "comments"),
    "rencana": ("rencana", "rencana berikutnya", "next", "next step", "next steps",
                "tindak lanjut", "follow up", "langkah berikutnya"),
}
WAJIB_BACA = ("tanggal", "pekerjaan")
_POLA_BUTUH_KLIEN = re.compile(r"\b(menunggu|nunggu|tunggu|butuh|perlu|belum (dikirim|diberi|ada))\b",
                               re.IGNORECASE)


def _norm_header(h):
    h = (h or "").replace("\ufeff", "").strip().lower()
    h = re.sub(r"[_\-]+", " ", h)
    h = re.sub(r"\s*\(.*?\)\s*", " ", h)  # "Durasi (jam)" -> "durasi"
    return re.sub(r"\s+", " ", h).strip()


def _petakan_header(fieldnames):
    peta = {}
    for asli in fieldnames:
        n = _norm_header(asli)
        for kunci, alias in ALIAS_KOLOM.items():
            if kunci not in peta and (n == kunci.replace("_", " ") or n in alias):
                peta[kunci] = asli
                break
    return peta


def _dekode(path):
    data = path.read_bytes()
    if data.startswith(b"\xff\xfe") or data.startswith(b"\xfe\xff"):
        return data.decode("utf-16"), "utf-16"
    try:
        return data.decode("utf-8-sig"), "utf-8"
    except UnicodeDecodeError:
        return data.decode("cp1252", errors="replace"), "cp1252"


def _tebak_pemisah(teks):
    baris_awal = [b for b in teks.splitlines() if b.strip()][:20]
    if not baris_awal:
        return ","
    try:
        return csv.Sniffer().sniff("\n".join(baris_awal), delimiters=",;\t|").delimiter
    except csv.Error:
        header = baris_awal[0]
        return max(",;\t|", key=header.count) if any(c in header for c in ";\t|") else ","


def baca_log(path):
    """Baca file log skill ATAU file catatan milik pengguna (format toleran, lihat docstring)."""
    if not path.exists():
        raise Gagal(f"File log '{path}' tidak ditemukan. Catat pekerjaan dulu dengan perintah "
                    "`catat`, atau jalankan `init` untuk membuat file kosong.")
    teks, encoding = _dekode(path)
    if not teks.strip():
        raise Gagal(
            f"File log '{path}' kosong total (0 byte, tanpa baris header) -- ini beda dari "
            "\"belum ada catatan\": file yang benar selalu punya baris header pertama "
            f"({','.join(KOLOM)}) meski belum ada data. Kemungkinan file rusak/terhapus isinya "
            "tanpa sengaja. Jalankan `init --file <path>` untuk membuat ulang filenya (data lama "
            "tidak bisa dipulihkan otomatis -- cek backup bila ada), lalu `catat` ulang."
        )
    pemisah = _tebak_pemisah(teks)
    try:
        r = csv.reader(teks.splitlines(), delimiter=pemisah)
        semua_baris = [b for b in r if any(sel.strip() for sel in b)]
    except csv.Error as e:
        raise Gagal(f"File '{path}' tidak bisa dibaca sebagai CSV: {e}. Simpan ulang dari "
                    "Excel/Sheets sebagai 'CSV (dipisah koma)' lalu coba lagi.")
    header = semua_baris[0]
    peta = _petakan_header(header)
    hilang = [k for k in WAJIB_BACA if k not in peta]
    if hilang:
        nama_ramah = {"tanggal": "Tanggal/Date", "pekerjaan": "Pekerjaan/Kerjaan/Kegiatan/Task"}
        raise Gagal(
            f"File '{path}' tidak punya kolom wajib: {', '.join(nama_ramah[k] for k in hilang)}. "
            f"Header yang terbaca: {header} (pemisah '{pemisah}'). Kolom yang dikenali: "
            "Tanggal, Klien, Proyek, Pekerjaan/Kerjaan, Jam/Durasi, Status, Kendala, "
            "Butuh dari klien, Keterangan/Catatan, Rencana (atau padanan Inggrisnya). "
            "Ganti nama kolom di baris pertama file, lalu coba lagi."
        )
    idx = {k: header.index(v) for k, v in peta.items()}
    info = {"encoding": encoding, "pemisah": pemisah, "kolom": {k: peta[k] for k in peta},
            "tanpa_kolom_klien": "klien" not in peta}
    hasil = []
    for nomor, b in enumerate(semua_baris[1:], start=2):
        if len(b) > len(header):
            raise Gagal(
                f"Baris {nomor} '{path.name}' punya {len(b)} kolom, padahal header {len(header)} "
                f"kolom (pemisah '{pemisah}'). Biasanya karena angka berkoma seperti 2,5 tidak "
                "diberi tanda kutip. Perbaiki dengan menulis \"2,5 jam\" (pakai kutip), atau "
                "simpan ulang dari Excel/Sheets sebagai CSV, atau pakai titik koma (;) sebagai "
                "pemisah kolom."
            )

        def ambil(k):
            if k not in idx or idx[k] >= len(b):
                return ""
            v = (b[idx[k]] or "").strip()
            return v[1:] if v[:1] == "'" and v[1:2] in ("=", "+", "-", "@") else v

        try:
            tgl = baca_tanggal(ambil("tanggal")) if ambil("tanggal") else None
            if tgl is None:
                raise Gagal("kolom tanggal kosong.")
            status = normalisasi_status(ambil("status"))
            jam = parse_jam(ambil("jam"))
        except Gagal as e:
            raise Gagal(f"Baris {nomor} '{path.name}': {e.pesan}")
        keterangan = ambil("keterangan")
        butuh = ambil("butuh_dari_klien")
        dari_keterangan = False
        if keterangan and not butuh and "butuh_dari_klien" not in peta \
                and re.search(r"\bklien\b|\bclient\b", keterangan, re.IGNORECASE) \
                and _POLA_BUTUH_KLIEN.search(keterangan):
            butuh, keterangan, dari_keterangan = keterangan, "", True
        hasil.append({
            "tanggal": tgl, "klien": ambil("klien"), "proyek": ambil("proyek"),
            "pekerjaan": ambil("pekerjaan"), "jam": jam, "status": status,
            "kendala": ambil("kendala"), "butuh_dari_klien": butuh,
            "keterangan": keterangan, "rencana": ambil("rencana"),
            "butuh_dari_keterangan": dari_keterangan,
        })
    baca_log.info_terakhir = info
    return hasil


baca_log.info_terakhir = {}


def tulis_baris(path, entri):
    baru = pastikan_file(path)
    with path.open("a", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow([aman_csv(entri[k]) if k != "jam" else ("" if entri[k] is None else entri[k])
                    for k in KOLOM])
    return baru


# ---------------------------------------------------------------------------
# Perintah
# ---------------------------------------------------------------------------

def cmd_init(args):
    path = cari_file(args.file)
    if path.exists() and not args.paksa:
        raise Gagal(f"File '{path}' sudah ada. Pakai --paksa untuk menimpanya dengan file kosong "
                    "baru (isi lama akan hilang -- cadangkan dulu bila perlu).")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        csv.writer(f).writerow(KOLOM)
    hasil = {"dibuat": str(path)}
    if args.json:
        print(json.dumps(hasil, ensure_ascii=False, indent=2))
    else:
        print(f"File log baru dibuat: {path}")
    return 0


def cmd_catat(args):
    path = cari_file(args.file)
    klien = (args.klien or "").strip()
    proyek = (args.proyek or "").strip()
    pekerjaan = (args.pekerjaan or "").strip()
    if not klien:
        raise Gagal("--klien wajib diisi (nama klien/perusahaan).")
    if not proyek:
        raise Gagal("--proyek wajib diisi (nama proyek/layanan, mis. 'Pembukuan bulanan').")
    if not pekerjaan:
        raise Gagal("--pekerjaan wajib diisi (apa yang dikerjakan, dalam satu kalimat).")
    tgl = baca_tanggal(args.tanggal)
    jam = parse_jam(args.jam)
    status = normalisasi_status(args.status)
    kendala = (args.kendala or "").strip()
    butuh = (args.butuh_klien or "").strip()

    peringatan = []
    deteksi_sensitif(pekerjaan, "Kolom pekerjaan", peringatan)
    deteksi_sensitif(kendala, "Kolom kendala", peringatan)
    deteksi_sensitif(butuh, "Kolom butuh_dari_klien", peringatan)

    entri = {"tanggal": tgl.isoformat(), "klien": klien, "proyek": proyek, "pekerjaan": pekerjaan,
             "jam": jam, "status": status, "kendala": kendala, "butuh_dari_klien": butuh}
    file_baru = tulis_baris(path, entri)

    hasil = {"skema": SKEMA, "dicatat": {**entri, "jam": jam}, "file": str(path),
             "file_baru_dibuat": file_baru, "peringatan": peringatan}
    if args.json:
        print(json.dumps(hasil, ensure_ascii=False, indent=2, default=str))
    else:
        print(f"Tercatat: [{LABEL_STATUS[status]}] {klien} / {proyek} -- {pekerjaan} "
              f"({tgl.isoformat()}{', ' + format_jam(jam) if jam is not None else ''})")
        if file_baru:
            print(f"(File log baru dibuat di: {path})")
    if peringatan:
        for p in peringatan:
            print("PERINGATAN: " + p, file=sys.stderr)
        return 3
    return 0


def cmd_daftar_klien(args):
    path = cari_file(args.file)
    entri = baca_log(path)
    klien = sorted({e["klien"] for e in entri if e["klien"]})
    if args.json:
        print(json.dumps({"file": str(path), "klien": klien}, ensure_ascii=False, indent=2))
    else:
        if not klien:
            print(f"Belum ada catatan di '{path}'.")
        else:
            print(f"Klien tercatat di '{path}':")
            for k in klien:
                print(f"- {k}")
    return 0


def _dedup_urut(items):
    dilihat = set()
    hasil = []
    for it in items:
        if it and it not in dilihat:
            dilihat.add(it)
            hasil.append(it)
    return hasil


def susun_laporan(entri_periode, klien, label_periode, awal, akhir, rencana_manual, catatan):
    selesai = [e for e in entri_periode if e["status"] == "selesai"]
    berjalan = [e for e in entri_periode if e["status"] == "berjalan"]
    terkendala = [e for e in entri_periode if e["status"] == "terkendala"]

    berjam = [e for e in entri_periode if e["jam"] is not None]
    tanpa_jam = len(entri_periode) - len(berjam)
    # total = jumlah PERSIS jam per baris (sudah 2 desimal), jadi selalu sama dengan
    # penjumlahan angka yang tampil di daftar pekerjaan.
    total_jam = jumlah_jam(e["jam"] for e in berjam) if berjam else 0.0
    per_proyek = {}
    for e in berjam:
        kunci = e["proyek"] or "(tanpa nama proyek)"
        per_proyek.setdefault(kunci, []).append(e["jam"])
    per_proyek = {k: jumlah_jam(v) for k, v in per_proyek.items()}

    kendala = _dedup_urut(e["kendala"] for e in entri_periode)
    butuh = _dedup_urut(e["butuh_dari_klien"] for e in entri_periode)

    # Rencana berikutnya TIDAK pernah dikarang dari judul tugas ("Lanjutkan ..." x3).
    # Sumber: --rencana dari pengguna > kolom Rencana di file > isian [isi: ...] untuk diisi.
    isian = 0
    if rencana_manual:
        rencana = [r.strip() for r in rencana_manual if r.strip()]
    else:
        rencana = _dedup_urut(e["rencana"] for e in entri_periode)
        ada_rencana = {e["pekerjaan"] for e in entri_periode if e["rencana"]}
        for e in berjalan + terkendala:
            if e["pekerjaan"] not in ada_rencana:
                rencana.append(f"[isi: langkah berikutnya untuk \"{e['pekerjaan']}\" "
                               "+ target tanggal]")
                isian += 1
        if not rencana and entri_periode:
            rencana.append("[isi: rencana periode berikutnya]")
            isian += 1
    if isian:
        catatan.append(
            f"Rencana berikutnya berisi {isian} isian [isi: ...]. Isi dari catatan/rencana "
            "pengguna (atau tanyakan sekali), lalu buat ulang dengan --rencana \"...\" -- "
            "jangan dikirim ke klien dengan isian kosong dan jangan mengarang rencana."
        )
    if any(e.get("butuh_dari_keterangan") for e in entri_periode):
        catatan.append(
            "Sebagian 'Butuh dari klien' diambil dari kolom Keterangan yang menyebut klien "
            "dan kata menunggu/butuh -- pastikan memang hal yang ditunggu dari klien."
        )

    if not entri_periode:
        catatan.append(
            f"Tidak ada catatan pekerjaan untuk '{klien}' pada periode "
            f"{format_periode_label(awal, akhir)} "
            f"({awal.isoformat()} s/d {akhir.isoformat()}). Laporan di bawah kosong -- jangan "
            "mengarang isi; catat dulu pekerjaannya dengan perintah `catat`."
        )
    if tanpa_jam:
        catatan.append(
            f"{tanpa_jam} dari {len(entri_periode)} entri tidak mencatat jam -- total jam di "
            "bawah TIDAK termasuk entri tersebut (bukan dianggap 0)."
        )

    bagian = {
        "selesai": selesai, "berjalan": berjalan, "terkendala": terkendala,
        "kendala": kendala, "butuh_dari_klien": butuh, "rencana": rencana,
        "total_jam": total_jam, "entri_tanpa_jam": tanpa_jam, "per_proyek": per_proyek,
        "jumlah_entri": len(entri_periode), "rencana_perlu_diisi": isian,
    }

    ringkasan = (
        f"{judul_periode(label_periode, awal, akhir) if label_periode else 'Periode ' + format_periode_label(awal, akhir)}: "
        f"{len(selesai)} pekerjaan selesai, {len(berjalan)} sedang berjalan"
        + (f", {len(terkendala)} terkendala" if terkendala else "")
        + f". Total jam tercatat: {format_jam_menit(total_jam) if berjam else 'tidak ada jam dicatat'}."
    )
    bagian["ringkasan"] = ringkasan
    return bagian


def _baris_kerja(e, dengan_tanggal=True):
    rincian = []
    if e["proyek"]:
        rincian.append(e["proyek"])
    if dengan_tanggal:
        rincian.append(e["tanggal"].isoformat())
    if e["jam"] is not None:
        rincian.append(format_jam(e["jam"]))
    inti = e["pekerjaan"] + (f" ({', '.join(rincian)})" if rincian else "")
    if e.get("keterangan"):
        inti += f" -- {e['keterangan']}"
    return inti


def buat_markdown(klien, label_periode, awal, akhir, b):
    L = []
    L.append(f"# Laporan Progres -- {klien}")
    L.append(f"**Periode:** {judul_periode(label_periode, awal, akhir)}\n")
    L.append("## Ringkasan")
    L.append(b["ringkasan"] + "\n")
    L.append("## Yang Selesai")
    L += [f"- {_baris_kerja(e)}" for e in b["selesai"]] or ["- (tidak ada pekerjaan selesai pada periode ini)"]
    L.append("")
    L.append("## Yang Sedang Berjalan")
    L += [f"- {_baris_kerja(e)}" for e in b["berjalan"]] or ["- (tidak ada pekerjaan berjalan)"]
    L.append("")
    if b["terkendala"]:
        L.append("## Terkendala")
        L += [f"- {_baris_kerja(e)}" for e in b["terkendala"]]
        L.append("")
    L.append("## Butuh dari Klien")
    L += [f"- {x}" for x in b["butuh_dari_klien"]] or ["- Tidak ada yang dibutuhkan saat ini."]
    L.append("")
    L.append("## Kendala Saat Ini")
    L += [f"- {x}" for x in b["kendala"]] or ["- Tidak ada kendala berarti."]
    L.append("")
    L.append("## Rencana Berikutnya")
    L += [f"- {x}" for x in b["rencana"]] or ["- (isi rencana berikutnya sebelum mengirim)"]
    L.append("")
    L.append("## Total Jam")
    if b["per_proyek"]:
        L.append(f"**Total: {format_jam_menit(b['total_jam'])}**" +
                  (f" (dari {b['jumlah_entri'] - b['entri_tanpa_jam']} entri berjam; "
                   f"{b['entri_tanpa_jam']} entri tanpa jam tidak dihitung)" if b["entri_tanpa_jam"] else ""))
        if list(b["per_proyek"]) != ["(tanpa nama proyek)"]:
            for p, j in sorted(b["per_proyek"].items()):
                L.append(f"- {p}: {format_jam(j)}")
    else:
        L.append("Tidak ada jam yang dicatat pada periode ini.")
    L.append("\n---")
    L.append("_Draf disusun otomatis dari catatan kerja lokal. Tinjau sebelum dikirim ke klien._")
    return "\n".join(L)


def buat_teks_email(klien, label_periode, awal, akhir, b):
    L = []
    L.append(f"Subjek: Laporan Progres{' ' + label_periode if label_periode else ''} -- {klien} "
             f"({format_periode_label(awal, akhir)})\n")
    L.append(f"Yth. Bapak/Ibu {klien},\n")
    L.append(f"Berikut laporan progres untuk periode {format_periode_label(awal, akhir)}.\n")
    L.append(f"Ringkasan: {b['ringkasan']}\n")
    L.append("Yang sudah selesai:")
    L += [f"- {_baris_kerja(e, dengan_tanggal=False)}" for e in b["selesai"]] or ["- (belum ada yang selesai pada periode ini)"]
    L.append("\nYang sedang berjalan:")
    L += [f"- {_baris_kerja(e, dengan_tanggal=False)}" for e in b["berjalan"]] or ["- (tidak ada pekerjaan berjalan)"]
    if b["terkendala"]:
        L.append("\nTerkendala:")
        L += [f"- {_baris_kerja(e, dengan_tanggal=False)}" for e in b["terkendala"]]
    if b["butuh_dari_klien"]:
        L.append("\nMohon bantuan/keputusan dari Bapak/Ibu untuk:")
        L += [f"- {x}" for x in b["butuh_dari_klien"]]
    if b["rencana"]:
        L.append("\nRencana berikutnya:")
        L += [f"- {x}" for x in b["rencana"]]
    L.append("\nDemikian laporan ini kami sampaikan. Silakan hubungi kami bila ada pertanyaan.\n")
    L.append("Hormat kami,\n[Nama Anda]")
    return "\n".join(L)


def buat_teks_wa(klien, label_periode, awal, akhir, b):
    L = []
    L.append(f"*Laporan Progres -- {klien}*")
    L.append(f"_{judul_periode(label_periode, awal, akhir)}_\n")
    L.append(b["ringkasan"] + "\n")
    L.append("*Selesai:*")
    L += [f"- {_baris_kerja(e, dengan_tanggal=False)}" for e in b["selesai"]] or ["- Belum ada"]
    L.append("\n*Berjalan:*")
    L += [f"- {_baris_kerja(e, dengan_tanggal=False)}" for e in b["berjalan"]] or ["- Tidak ada"]
    if b["terkendala"]:
        L.append("\n*Terkendala:*")
        L += [f"- {_baris_kerja(e, dengan_tanggal=False)}" for e in b["terkendala"]]
    if b["butuh_dari_klien"]:
        L.append("\n*Butuh dari Bapak/Ibu:*")
        L += [f"- {x}" for x in b["butuh_dari_klien"]]
    if b["rencana"]:
        L.append("\n*Rencana berikutnya:*")
        L += [f"- {x}" for x in b["rencana"]]
    return "\n".join(L)


def cmd_laporan(args):
    path = cari_file(args.file)
    klien = (args.klien or "").strip()
    if not klien:
        raise Gagal("--klien wajib diisi.")
    semua = baca_log(path)

    acuan = baca_tanggal(args.tanggal_acuan) if args.tanggal_acuan else date.today()
    if args.dari or args.sampai:
        if not (args.dari and args.sampai):
            raise Gagal("--dari dan --sampai harus diisi berdua.")
        awal = baca_tanggal(args.dari)
        akhir = baca_tanggal(args.sampai)
        if akhir < awal:
            raise Gagal("--sampai lebih awal dari --dari.")
        label_periode = ""  # rentang kustom: cukup tampilkan tanggalnya (bukan "Periode periode kustom")
    else:
        label_periode, awal, akhir = rentang_periode(args.periode, acuan)

    catatan = []
    info = getattr(baca_log, "info_terakhir", {}) or {}
    if info.get("tanpa_kolom_klien"):
        for e in semua:
            e["klien"] = klien
        catatan.append(f"File '{path.name}' tidak punya kolom Klien -- semua baris dianggap "
                       f"pekerjaan untuk '{klien}'. Pastikan file ini memang khusus klien tersebut.")
    if info.get("encoding") == "cp1252":
        catatan.append(f"File '{path.name}' bukan UTF-8 (dibaca sebagai Windows-1252) -- cek "
                       "huruf beraksen/simbol di draf.")
    cocok_klien = [e for e in semua if e["klien"].strip().lower() == klien.lower()]
    if not cocok_klien and semua:
        klien_ada = sorted({e["klien"] for e in semua})
        raise Gagal(f"Tidak ada catatan untuk klien '{klien}' di '{path}'. Klien yang tercatat: "
                    f"{', '.join(klien_ada) if klien_ada else '(kosong)'}.")
    entri_periode = [e for e in cocok_klien if awal <= e["tanggal"] <= akhir]
    entri_periode.sort(key=lambda e: e["tanggal"])

    peringatan = []
    b = susun_laporan(entri_periode, klien, label_periode, awal, akhir, args.rencana, catatan)

    for e in entri_periode:
        deteksi_sensitif(e["pekerjaan"], f"Baris {e['tanggal'].isoformat()} (pekerjaan)", peringatan)
        deteksi_sensitif(e["kendala"], f"Baris {e['tanggal'].isoformat()} (kendala)", peringatan)
        deteksi_sensitif(e["butuh_dari_klien"], f"Baris {e['tanggal'].isoformat()} (butuh_dari_klien)",
                          peringatan)
        deteksi_sensitif(e["keterangan"], f"Baris {e['tanggal'].isoformat()} (keterangan)", peringatan)
        deteksi_sensitif(e["rencana"], f"Baris {e['tanggal'].isoformat()} (rencana)", peringatan)

    markdown = buat_markdown(klien, label_periode, awal, akhir, b)
    teks_email = buat_teks_email(klien, label_periode, awal, akhir, b)
    teks_wa = buat_teks_wa(klien, label_periode, awal, akhir, b)

    hasil = {
        "skema": SKEMA, "klien": klien, "periode": {
            "label": label_periode or "kustom", "awal": awal.isoformat(), "akhir": akhir.isoformat(),
        },
        "total_jam_teks": format_jam_menit(b["total_jam"]),
        "rencana_perlu_diisi": b["rencana_perlu_diisi"],
        "jumlah_entri": b["jumlah_entri"], "total_jam": b["total_jam"],
        "jam_per_proyek": b["per_proyek"], "entri_tanpa_jam": b["entri_tanpa_jam"],
        "rincian": [{"tanggal": e["tanggal"].isoformat(), "pekerjaan": e["pekerjaan"],
                     "proyek": e["proyek"], "jam": e["jam"], "status": e["status"]}
                    for e in entri_periode],
        "selesai": [e["pekerjaan"] for e in b["selesai"]],
        "berjalan": [e["pekerjaan"] for e in b["berjalan"]],
        "terkendala": [e["pekerjaan"] for e in b["terkendala"]],
        "kendala": b["kendala"], "butuh_dari_klien": b["butuh_dari_klien"],
        "rencana_berikutnya": b["rencana"], "ringkasan": b["ringkasan"],
        "teks_email": teks_email, "teks_wa": teks_wa, "markdown": markdown,
        "catatan": catatan, "peringatan": peringatan,
        "catatan_internal": "Draf ini untuk ditinjau KONSULTAN sebelum dikirim ke klien -- "
                             "skill ini tidak pernah mengirim apa pun secara otomatis.",
    }

    if args.json:
        print(json.dumps(hasil, ensure_ascii=False, indent=2, default=str))
    else:
        print("=== VERSI EMAIL ===\n")
        print(teks_email)
        print("\n=== VERSI WA/TELEGRAM ===\n")
        print(teks_wa)
        print("\n=== VERSI MARKDOWN (dokumen) ===\n")
        print(markdown)
        if catatan:
            print("\n--- CATATAN ---")
            for c in catatan:
                print("- " + c)
    if peringatan:
        print("\n--- PERINGATAN: pola mirip data pribadi/rahasia (lihat SKILL.md) ---", file=sys.stderr)
        for p in peringatan:
            print("PERINGATAN: " + p, file=sys.stderr)
        return 3
    return 0


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def build_parser():
    ap = argparse.ArgumentParser(prog="laporan_klien.py", description=__doc__.splitlines()[0], allow_abbrev=False)
    ap.add_argument("--file", help="Path file log CSV (default: log-kerja-klien.csv atau "
                                     "ENV KOMUNITECH_LAPORAN_KLIEN_FILE)")
    sub = ap.add_subparsers(dest="perintah", required=True)

    p_init = sub.add_parser("init", help="Buat file log kosong", allow_abbrev=False)
    p_init.add_argument("--paksa", action="store_true", help="Timpa file yang sudah ada")
    p_init.add_argument("--json", action="store_true")
    p_init.set_defaults(func=cmd_init)

    p_catat = sub.add_parser("catat", help="Catat satu pekerjaan", allow_abbrev=False)
    p_catat.add_argument("--klien", required=True)
    p_catat.add_argument("--proyek", required=True)
    p_catat.add_argument("--pekerjaan", required=True)
    p_catat.add_argument("--tanggal", help="YYYY-MM-DD, 'hari-ini' (default), atau 'kemarin'")
    p_catat.add_argument("--jam", help="Jam kerja, mis. 2 atau 2,5 (opsional)")
    p_catat.add_argument("--status", default="berjalan",
                          help="selesai | berjalan (default) | terkendala")
    p_catat.add_argument("--kendala", default="", help="Hambatan di pihak konsultan (opsional)")
    p_catat.add_argument("--butuh-klien", dest="butuh_klien", default="",
                          help="Yang perlu diberikan/diputuskan klien (opsional)")
    p_catat.add_argument("--json", action="store_true")
    p_catat.set_defaults(func=cmd_catat)

    p_daftar = sub.add_parser("daftar-klien", help="Lihat daftar klien yang tercatat", allow_abbrev=False)
    p_daftar.add_argument("--json", action="store_true")
    p_daftar.set_defaults(func=cmd_daftar_klien)

    p_lap = sub.add_parser("laporan", help="Susun draf laporan progres satu klien (file log skill "
                           "atau file catatan CSV milik pengguna via --file)", allow_abbrev=False)
    p_lap.add_argument("--klien", required=True)
    p_lap.add_argument("--periode", default="minggu-ini",
                        help="mingguan/bulanan, minggu-ini (default)/minggu-lalu/bulan-ini/bulan-lalu")
    p_lap.add_argument("--dari", help="Tanggal awal kustom YYYY-MM-DD (butuh --sampai)")
    p_lap.add_argument("--sampai", help="Tanggal akhir kustom YYYY-MM-DD (butuh --dari)")
    p_lap.add_argument("--tanggal-acuan", dest="tanggal_acuan",
                        help="Anggap hari ini = tanggal ini (default: hari ini sungguhan; "
                             "berguna untuk menguji jadwal Jumat)")
    p_lap.add_argument("--rencana", action="append",
                        help="Satu butir rencana berikutnya (bisa diulang). Tanpa ini, rencana "
                             "diambil dari kolom Rencana di file; bila tidak ada, muncul isian "
                             "[isi: ...] untuk pekerjaan berjalan/terkendala.")
    p_lap.add_argument("--json", action="store_true")
    p_lap.set_defaults(func=cmd_laporan)

    return ap


def main(argv=None):
    ap = build_parser()
    args = ap.parse_args(argv)
    try:
        return args.func(args) or 0
    except Gagal as e:
        print(f"Error: {e.pesan}", file=sys.stderr)
        return 1
    except (OSError, UnicodeDecodeError) as e:
        print(f"Error file: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
