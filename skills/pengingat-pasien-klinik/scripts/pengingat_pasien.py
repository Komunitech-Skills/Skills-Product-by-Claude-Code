#!/usr/bin/env python3
"""Buku jadwal pengingat kontrol/vaksin pasien klinik, praktik mandiri, dan klinik hewan.

Hanya library standar Python 3.8+. Tidak ada akses jaringan, tidak mengirim pesan apa pun.
Data disimpan di satu file CSV lokal (default `pasien/DAFTAR.csv` di folder kerja pengguna).

Data yang disimpan SENGAJA minimal (prinsip minimalisasi data UU PDP 27/2022):
nama panggilan, nomor WA, jenis kunjungan umum (kontrol/vaksin/dll — BUKAN diagnosis),
tanggal kunjungan berikutnya, status, dan catatan persetujuan dihubungi. TIDAK ADA rekam medis,
diagnosis, NIK, atau riwayat pengobatan.

Subperintah
  tambah        Tambah pasien:      tambah --nama "Bu Sari" --wa "0812..." --jenis kontrol
                                     --tanggal "10 Okt" --persetujuan ya [--catatan "..."]
  daftar        Lihat jadwal aktif: daftar [--kapan terlambat|hari-ini|besok|h-3|minggu-ini|semua]
                                     [--tanpa-draf] [--klinik "Nama Klinik"]
  draf          Draf 1 pasien:      draf --id 3 [--klinik "Nama Klinik"]
  ubah-status   Ubah status:        ubah-status --id 3 --status sudah-diingatkan
                                     ubah-status --id 3 --status datang --berikutnya "3 bulan lagi"
                                     ubah-status --id 3 --status batal --alasan "pindah kota"
  ubah          Ubah data:          ubah --id 3 [--nama ..] [--wa ..] [--jenis ..] [--tanggal ..] [--catatan ..]
  hapus         Hapus permanen:     hapus --id 3            atau   hapus --wa 0812...   (lalu --ya)
  impor         Impor CSV:          impor pasien-baru.csv [--jenis-default kontrol] [--persetujuan-default ya]
  ringkasan     Ringkasan pemilik:  ringkasan [--samarkan] [--tanpa-nama]
  info          Info file & jumlah: info

Opsi umum: --file (default pasien/DAFTAR.csv), --hari-ini (tanggal acuan, untuk uji),
--tz (default Asia/Jakarta; WIB/WITA/WIT juga diterima), --json (keluaran JSON, bukan teks).

Aturan
  - Tanggal: ISO (2026-10-05), 05-10-2026, 5/10, 5 Okt, 5 Oktober 2026, "besok", "lusa",
    "3 hari lagi", "3 bulan lagi", nama hari ("Senin"). Selalu tanggal ke DEPAN (kunjungan
    berikutnya). Tahun tidak disebut -> dipilih tanggal terdekat ke depan, dengan Catatan.
  - `jenis` HARUS umum (kontrol, vaksin, cabut jahitan, cek gigi, vaksin hewan, groom, sunat, dll),
    BUKAN diagnosis/nama penyakit. Kata yang menyerupai diagnosis ditolak (kode keluar 2).
  - `nama_panggilan` dan `catatan` tidak boleh berisi nomor HP/email/NIK pihak lain (kode keluar 2).
  - Pasien dengan persetujuan "tidak" TIDAK PERNAH muncul di `daftar`/`draf`/`ringkasan`.
  - Tidak ada pengiriman pesan otomatis. Semua keluaran adalah DRAF untuk disalin & dikirim staf.
  - Baris CSV rusak tidak menghentikan program: dilaporkan di `baris_ditolak`, tetap disimpan
    apa adanya di posisinya. CSV aman dari suntikan rumus (=, +, @, -) ala Excel/Sheets.

Kode keluar: 0 = berhasil; 1 = input/perintah salah ("ERROR: ..." di stderr);
2 = ditolak karena berisi data pribadi pihak lain atau kata yang menyerupai diagnosis.
"""
import argparse
import csv
import io
import json
import os
import re
import sys
import tempfile
from datetime import date, datetime, timedelta, timezone

BULAN_ID = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus",
            "September", "Oktober", "November", "Desember"]
BULAN_PENDEK = ["Jan", "Feb", "Mar", "Apr", "Mei", "Jun", "Jul", "Agu", "Sep", "Okt", "Nov", "Des"]
HARI_ID = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"]
NAMA_BULAN = {}
for _i, _alias in enumerate([
        ("jan", "januari", "january"), ("feb", "febr", "februari", "pebruari", "february"),
        ("mar", "maret", "march"), ("apr", "april"), ("mei", "may"), ("jun", "juni", "june"),
        ("jul", "juli", "july"), ("agu", "agt", "ags", "agus", "agustus", "aug", "august"),
        ("sep", "sept", "september"), ("okt", "oktober", "oct", "october"),
        ("nov", "nop", "november", "nopember"), ("des", "desember", "dec", "december")], start=1):
    for _a in _alias:
        NAMA_BULAN[_a] = _i
NAMA_HARI = {"senin": 0, "selasa": 1, "rabu": 2, "kamis": 3, "jumat": 4, "jum'at": 4, "jumaat": 4,
             "sabtu": 5, "minggu": 6, "ahad": 6}
TZ_TETAP = {"asia/jakarta": 7, "asia/pontianak": 7, "wib": 7, "asia/makassar": 8, "wita": 8,
            "asia/jayapura": 9, "wit": 9}

STATUS = ["dijadwalkan", "sudah-diingatkan", "datang", "batal"]
STATUS_AKTIF = {"dijadwalkan", "sudah-diingatkan"}
PERSETUJUAN = ["ya", "tidak"]
KOLOM = ["id", "nama_panggilan", "wa", "jenis", "tanggal", "status", "persetujuan",
         "dibuat", "diingatkan_pada", "catatan"]
BATAS_BARU_LEWAT = 60  # hari

# Kata yang menandakan isian berisi diagnosis/nama penyakit, bukan jenis kunjungan umum.
# Daftar ini BUKAN daftar medis lengkap -- sekadar jaring pengaman kata yang paling umum.
KATA_DIAGNOSIS = {
    "kanker", "tumor", "kista", "hiv", "aids", "ims", "jantung", "stroke", "diabetes",
    "kencing manis", "hepatitis", "tbc", "tuberkulosis", "paru-paru basah", "gagal ginjal",
    "kolesterol", "hipertensi", "darah tinggi", "covid", "positif", "reaktif", "negatif hiv",
    "tumor jinak", "tumor ganas", "epilepsi", "ayan", "skizofrenia", "gangguan jiwa",
    "depresi", "bipolar", "gangguan mental", "keguguran", "aborsi", "kelamin", "rabies",
    "kusta", "campak", "difteri", "malaria", "demam berdarah", "dbd", "tifus", "tipes",
}


class Gagal(Exception):
    pass


class DataPribadi(Exception):
    pass


# ---------------------------------------------------------------- waktu & tanggal
def hari_ini_di(tz_nama):
    kunci = (tz_nama or "Asia/Jakarta").strip()
    try:
        from zoneinfo import ZoneInfo  # Python 3.9+
        return datetime.now(ZoneInfo(kunci)).date()
    except Exception:
        pass
    if kunci.lower() in TZ_TETAP:  # tanpa zoneinfo/tzdata (mis. Windows lama): tanpa DST
        return datetime.now(timezone(timedelta(hours=TZ_TETAP[kunci.lower()]))).date()
    raise Gagal(f"zona waktu '{tz_nama}' tidak dikenal. Pakai mis. Asia/Jakarta, Asia/Makassar, Asia/Jayapura")


def tgl_id(d, pendek=False):
    if pendek:
        return f"{d.day} {BULAN_PENDEK[d.month - 1]} {d.year}"
    return f"{HARI_ID[d.weekday()]}, {d.day} {BULAN_ID[d.month - 1]} {d.year}"


def _coba_tanggal(y, m, d):
    try:
        return date(y, m, d)
    except ValueError:
        return None


def _pilih_tahun_depan(hari, bulan, acuan):
    kandidat = [c for c in (_coba_tanggal(acuan.year + k, bulan, hari) for k in (-1, 0, 1, 2)) if c]
    if not kandidat:
        raise Gagal(f"tanggal {hari}/{bulan} tidak ada di kalender")
    lewat = [x for x in kandidat if acuan - timedelta(days=BATAS_BARU_LEWAT) <= x < acuan]
    if lewat:
        c = max(lewat)
        return c, (f"Tahun tidak disebut; dipakai {tgl_id(c, True)} yang baru lewat {(acuan - c).days} hari. "
                   "Kalau maksudnya tahun depan, tulis tahunnya.")
    c = min(x for x in kandidat if x >= acuan)
    return c, f"Tahun tidak disebut; dipakai {tgl_id(c, True)} (tanggal terdekat ke depan). Ubah bila maksudnya lain."


def parse_tanggal(teks, acuan):
    """Kembalikan (date, catatan|None). Selalu diarahkan ke depan (tanggal kunjungan berikutnya)."""
    if teks is None or str(teks).strip() == "":
        raise Gagal("tanggal kosong")
    asli = str(teks).strip()
    s = asli.lower().replace(",", " ")
    s = re.sub(r"^(tgl\.?|tanggal)\s*", "", s).strip()
    s = re.sub(r"\s+", " ", s)
    if s in ("hari ini", "hr ini", "sekarang", "today"):
        return acuan, None
    if s in ("besok", "bsk", "tomorrow"):
        return acuan + timedelta(days=1), None
    if s == "lusa":
        return acuan + timedelta(days=2), None
    m = re.fullmatch(r"\+?\s*(\d{1,3})\s*(hari|hr|h)?(\s*lagi)?", s)
    if m and (s.startswith("+") or m.group(2)):
        return acuan + timedelta(days=int(m.group(1))), None
    m = re.fullmatch(r"(\d{1,2})\s*minggu\s*lagi", s)
    if m:
        return acuan + timedelta(days=7 * int(m.group(1))), None
    m = re.fullmatch(r"(\d{1,2})\s*bulan\s*lagi", s)
    if m:
        n = int(m.group(1))
        y, bln = acuan.year, acuan.month + n
        y += (bln - 1) // 12
        bln = (bln - 1) % 12 + 1
        hari = min(acuan.day, 28) if bln == 2 else acuan.day
        d = _coba_tanggal(y, bln, hari)
        while d is None:
            hari -= 1
            d = _coba_tanggal(y, bln, hari)
        return d, (None if hari == acuan.day else
                   f"Tanggal {acuan.day} tidak ada di bulan itu; dipakai {tgl_id(d, True)}.")
    m = re.fullmatch(r"(hari )?([a-z']+)( depan)?", s)
    if m and m.group(2) in NAMA_HARI:
        target = NAMA_HARI[m.group(2)]
        selisih = (target - acuan.weekday()) % 7
        cat = None
        if selisih == 0:
            if m.group(3) != " depan":
                return acuan, None
            selisih = 7
        elif m.group(3) == " depan" and selisih < 7:
            cat = f"\"{m.group(2)} depan\" diartikan {HARI_ID[target]} terdekat berikutnya."
        return acuan + timedelta(days=selisih), cat
    m = re.fullmatch(r"(\d{4})[-/.](\d{1,2})[-/.](\d{1,2})", s)
    if m:
        d = _coba_tanggal(int(m.group(1)), int(m.group(2)), int(m.group(3)))
        if not d:
            raise Gagal(f"tanggal '{asli}' tidak ada di kalender")
        return d, None
    m = re.fullmatch(r"(\d{1,2})[-/.](\d{1,2})[-/.](\d{2}|\d{4})", s)
    if m:
        y = int(m.group(3))
        y = y + 2000 if y < 100 else y
        d = _coba_tanggal(y, int(m.group(2)), int(m.group(1)))
        if not d:
            raise Gagal(f"tanggal '{asli}' tidak ada di kalender (urutan dibaca hari/bulan/tahun)")
        return d, None
    m = re.fullmatch(r"(\d{1,2})[-/.](\d{1,2})", s)
    if m:
        hari, bulan = int(m.group(1)), int(m.group(2))
        if not 1 <= bulan <= 12:
            raise Gagal(f"tanggal '{asli}' tidak valid: bulan {bulan} (urutan dibaca hari/bulan)")
        return _pilih_tahun_depan(hari, bulan, acuan)
    m = re.fullmatch(r"(\d{1,2}) ?([a-z]+)\.?(?: (\d{2}|\d{4}))?", s)
    if m and m.group(2) in NAMA_BULAN:
        hari, bulan = int(m.group(1)), NAMA_BULAN[m.group(2)]
        if m.group(3):
            y = int(m.group(3))
            y = y + 2000 if y < 100 else y
            d = _coba_tanggal(y, bulan, hari)
            if not d:
                raise Gagal(f"tanggal '{asli}' tidak ada di kalender")
            return d, None
        return _pilih_tahun_depan(hari, bulan, acuan)
    m = re.fullmatch(r"(\d{1,2})", s)
    if m:
        hari = int(m.group(1))
        if not 1 <= hari <= 31:
            raise Gagal(f"tanggal '{asli}' tidak valid")
        y, bln = acuan.year, acuan.month
        for _ in range(14):
            c = _coba_tanggal(y, bln, hari)
            if c and c >= acuan:
                return c, (f"Bulan tidak disebut; dipakai {tgl_id(c, True)} (tanggal {hari} terdekat ke depan). "
                           "Ubah bila maksudnya lain.")
            bln += 1
            if bln > 12:
                y, bln = y + 1, 1
        raise Gagal(f"tanggal '{asli}' tidak bisa ditentukan")
    raise Gagal(f"tanggal '{asli}' tidak dikenali formatnya")


# --------------------------------------------------------------------------- nomor WA
def normalisasi_wa(teks):
    """Kembalikan (nomor '62...', [peringatan]). Menolak nomor yang tidak wajar."""
    asli = str(teks or "").strip()
    if not asli:
        raise Gagal("Nomor WA kosong.")
    if re.search(r"\d[.,]\d+\s*e\+?\d+", asli, re.I):
        raise Gagal(f"Nomor '{asli}' rusak: kemungkinan Excel mengubahnya jadi angka ilmiah. "
                    "Format kolom sebagai Teks lalu ketik ulang.")
    s = re.sub(r"(?i)^(no\.?|nomor|nmr|hp|wa|whatsapp|telp\.?|tel|phone)\s*[:.]?\s*", "", asli)
    if re.search(r"[A-Za-z]", s):
        raise Gagal(f"Nomor '{asli}' berisi huruf. Tulis angkanya saja, mis. 0812-0000-1234.")
    plus = s.startswith("+")
    d = re.sub(r"\D", "", s)
    peringatan = []
    if d.startswith("00"):
        d, plus = d[2:], True
    if d.startswith("62"):
        pass
    elif d.startswith("0"):
        d = "62" + d[1:]
    elif d.startswith("8") and not plus:
        d = "62" + d
    else:
        raise Gagal(f"Nomor '{asli}' tidak dikenali. Nomor Indonesia diawali 08, 62, atau +62.")
    sisa = d[2:]
    if sisa.startswith("0"):
        sisa = sisa.lstrip("0")
        peringatan.append(f"Nomor '{asli}' berisi 0 setelah kode negara; angka 0 itu dibuang.")
        d = "62" + sisa
    if not 9 <= len(sisa) <= 12:
        raise Gagal(f"Nomor '{asli}' tidak wajar: {len(sisa)} digit setelah 62 (nomor HP Indonesia "
                    "9-12 digit, mis. 0812-0000-1234).")
    if not sisa.startswith("8"):
        peringatan.append(f"Nomor '{asli}' bukan pola nomor HP; pastikan nomor ini memakai WhatsApp.")
    return d, peringatan


def tampil_wa(wa):
    if not wa:
        return "-"
    if wa.startswith("62"):
        lok = "0" + wa[2:]
        return f"{lok[:4]}-{lok[4:-4]}-{lok[-4:]}" if len(lok) >= 10 else lok
    return "+" + wa


def samar_nama(nama):
    kata = (nama or "").strip().split()
    if not kata:
        return "-"
    SAPAAN = {"bu", "ibu", "pak", "bapak", "mbak", "mas", "kak", "adik", "dek", "om", "tante", "bang"}
    depan = []
    while kata and kata[0].lower().rstrip(".") in SAPAAN and len(depan) < 1:
        depan.append(kata.pop(0))
    if kata:
        depan.append(kata[0][0].upper() + ".")
    return " ".join(depan) if depan else "-"


# --------------------------------------------------------------------------- validasi isi
POLA_TELEPON = re.compile(r"(?:\+?62|0)8\d{8,11}")
POLA_EMAIL = re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+")
POLA_NIK = re.compile(r"\b\d{16}\b")


def cek_data_pribadi(label, teks):
    teks = teks or ""
    ringkas = re.sub(r"[\s.-]", "", teks)  # buang pemisah umum (0812-1111-2222, 0812 1111 2222, dst.)
    if POLA_TELEPON.search(ringkas):
        raise DataPribadi(f"'{label}' berisi pola nomor HP ('{teks}'). Nomor HP hanya disimpan di kolom --wa.")
    if POLA_EMAIL.search(teks):
        raise DataPribadi(f"'{label}' berisi alamat email ('{teks}'). Skill ini tidak menyimpan email.")
    if POLA_NIK.search(teks) or POLA_NIK.search(ringkas):
        raise DataPribadi(f"'{label}' berisi pola NIK 16 digit ('{teks}'). Jangan simpan NIK di sini.")


def cek_diagnosis(label, teks):
    low = (teks or "").lower()
    for kata in KATA_DIAGNOSIS:
        if re.search(r"\b" + re.escape(kata) + r"\b", low):
            raise Gagal(
                f"'{label}' berisi kata yang menyerupai diagnosis/nama penyakit ('{kata}'). "
                "Skill ini HANYA menyimpan jenis kunjungan umum (kontrol, vaksin, cabut jahitan, "
                "cek gigi, vaksin hewan, groom, sunat, medical check up, dll), TANPA diagnosis atau "
                "rekam medis. Tulis ulang tanpa nama penyakit."
            )


def bersih(teks, maks=200):
    s = re.sub(r"[\x00-\x08\x0b-\x1f\x7f]", " ", str(teks or ""))
    s = re.sub(r"[ \t]+", " ", s).strip()
    return s[:maks]


def tambah_catatan(lama, baru):
    """Tambahkan potongan catatan baru ke catatan lama, tanpa pemisah '; ' yang menggantung bila lama kosong."""
    lama = (lama or "").strip()
    return bersih((lama + "; " + baru) if lama else baru, 200)


def rapikan_jenis(teks):
    s = bersih(teks, 60)
    if not s:
        raise Gagal("jenis kunjungan kosong. Contoh: kontrol, vaksin, cabut jahitan, cek gigi, vaksin hewan.")
    cek_diagnosis("jenis kunjungan", s)
    cek_data_pribadi("jenis kunjungan", s)
    return s[0].upper() + s[1:] if s else s


# --------------------------------------------------------------------------- CSV
def aman_csv(teks):
    """Cegah teks dibaca sebagai rumus saat CSV dibuka di Excel/Sheets."""
    teks = (teks or "").replace("\r", " ").replace("\n", " ").strip()
    if teks[:1] in ("=", "+", "@") or (teks[:1] == "-" and len(teks) > 1 and teks[1] != " "):
        return "'" + teks
    return teks


def baca_csv(path):
    """Kembalikan (header, [(no_baris, dict|None, alasan|None, sel_mentah)])."""
    if not os.path.exists(path):
        return None, []
    with open(path, "rb") as f:
        mentah = f.read()
    try:
        isi = mentah.decode("utf-8-sig")
    except UnicodeDecodeError:
        try:
            isi = mentah.decode("cp1252")
        except UnicodeDecodeError:
            raise Gagal(f"file {path} tidak bisa dibaca (encoding tidak dikenal). Buka di Excel lalu "
                        "Simpan Sebagai 'CSV UTF-8 (dipisahkan koma)'.")
    if not isi.strip():
        return [], []
    baris_pertama = isi.splitlines()[0]
    pemisah = ";" if baris_pertama.count(";") > baris_pertama.count(",") else ","
    pembaca = csv.reader(io.StringIO(isi), delimiter=pemisah)
    header = [h.strip().lower() for h in next(pembaca)]
    hasil = []
    for no, sel in enumerate(pembaca, start=2):
        if not any(x.strip() for x in sel):
            continue
        if len(sel) > len(header):
            hasil.append((no, None, f"jumlah kolom ({len(sel)}) lebih banyak dari header ({len(header)})", sel))
            continue
        lengkap = sel + [""] * (len(header) - len(sel))
        hasil.append((no, {header[i]: lengkap[i].strip() for i in range(len(header))}, None, sel))
    return header, hasil


def tulis_csv_atomik(path, baris):
    folder = os.path.dirname(os.path.abspath(path)) or "."
    os.makedirs(folder, exist_ok=True)
    fd, tmp = tempfile.mkstemp(prefix=".tmp-", suffix=".csv", dir=folder)
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="") as f:
            w = csv.writer(f)
            w.writerow(KOLOM)
            for b in baris:
                if isinstance(b, list):  # baris rusak: ditulis ulang apa adanya, hanya diamankan dari rumus
                    w.writerow([aman_csv(x) for x in b])
                else:
                    w.writerow([aman_csv(str(b.get(k, "") or "")) for k in KOLOM])
        os.replace(tmp, path)
    except Exception:
        if os.path.exists(tmp):
            os.remove(tmp)
        raise


def muat_daftar(path):
    header, isi = baca_csv(path)
    if header is None:
        return [], []
    baris, rusak = [], []
    for no, b, alasan, sel in isi:
        if b is None:
            rusak.append({"baris": no, "alasan": alasan})
            baris.append(sel)
            continue
        lengkap = {k: b.get(k, "") for k in KOLOM}
        lengkap["_no"] = no
        baris.append(lengkap)
    return baris, rusak


def id_berikutnya(baris):
    maks = 0
    for b in baris:
        if isinstance(b, dict):
            try:
                maks = max(maks, int(b.get("id") or 0))
            except ValueError:
                pass
    return maks + 1


def cari(baris, id_):
    for b in baris:
        if isinstance(b, dict) and str(b.get("id")) == str(id_):
            return b
    return None


# --------------------------------------------------------------------------- draf pesan
def buat_draf(row, klinik):
    nama = row["nama_panggilan"]
    jenis = row["jenis"].lower()
    tgl = tgl_id(datetime.strptime(row["tanggal"], "%Y-%m-%d").date(), pendek=True)
    pengirim = klinik.strip() if klinik and klinik.strip() else "kami"
    return (f"Halo {nama}, ini pengingat dari {pengirim} untuk jadwal {jenis} Anda pada {tgl}. "
            f"Mohon konfirmasi kehadiran Anda. Kalau perlu mengubah jadwal, silakan balas pesan ini. "
            f"Terima kasih.")


# --------------------------------------------------------------------------- kelompok jadwal
def kelompokkan(baris, acuan):
    kel = {"terlambat": [], "hari_ini": [], "h1": [], "h3": []}
    for b in baris:
        if not isinstance(b, dict):
            continue
        if b.get("status") not in STATUS_AKTIF or b.get("persetujuan") != "ya":
            continue
        try:
            t = datetime.strptime(b["tanggal"], "%Y-%m-%d").date()
        except ValueError:
            continue
        selisih = (t - acuan).days
        if selisih < 0:
            kel["terlambat"].append(b)
        elif selisih == 0:
            kel["hari_ini"].append(b)
        elif selisih == 1:
            kel["h1"].append(b)
        elif selisih == 3:
            kel["h3"].append(b)
    for k in kel:
        kel[k].sort(key=lambda b: b["tanggal"])
    return kel


# --------------------------------------------------------------------------- perintah
def op_tambah(a, baris, acuan):
    if a.persetujuan not in PERSETUJUAN:
        raise Gagal("--persetujuan wajib diisi 'ya' atau 'tidak' (apakah pasien setuju dihubungi lewat WA).")
    nama = bersih(a.nama, 60)
    if not nama:
        raise Gagal("--nama kosong. Isi nama panggilan pasien, mis. \"Bu Sari\".")
    cek_data_pribadi("nama", nama)
    wa, peringatan_wa = normalisasi_wa(a.wa)
    jenis = rapikan_jenis(a.jenis)
    tgl, catatan_tgl = parse_tanggal(a.tanggal, acuan)
    catatan = bersih(a.catatan or "", 200)
    if catatan:
        cek_data_pribadi("catatan", catatan)
        cek_diagnosis("catatan", catatan)
    baru = {
        "id": str(id_berikutnya(baris)), "nama_panggilan": nama, "wa": wa, "jenis": jenis,
        "tanggal": tgl.isoformat(), "status": "dijadwalkan", "persetujuan": a.persetujuan,
        "dibuat": acuan.isoformat(), "diingatkan_pada": "", "catatan": catatan,
    }
    baris.append(baru)
    peringatan = list(peringatan_wa)
    if catatan_tgl:
        peringatan.append(catatan_tgl)
    teks = (f"Tersimpan #{baru['id']}: {nama} | {jenis} | {tgl_id(tgl, True)} | "
            f"persetujuan: {a.persetujuan}")
    if a.persetujuan == "tidak":
        peringatan.append("Persetujuan 'tidak': pasien ini TIDAK akan muncul di daftar pengingat/draf/ringkasan "
                           "sampai persetujuannya diubah menjadi 'ya' (ubah --id ... lalu catat ulang bila pasien "
                           "berubah pikiran).")
    return {"ok": True, "mode": "tersimpan", "id": baru["id"], "teks": teks, "peringatan": peringatan}


def op_ubah(a, baris, acuan):
    row = cari(baris, a.id)
    if row is None:
        raise Gagal(f"id {a.id} tidak ditemukan.")
    peringatan = []
    if a.nama:
        nama = bersih(a.nama, 60)
        cek_data_pribadi("nama", nama)
        row["nama_panggilan"] = nama
    if a.wa:
        wa, p = normalisasi_wa(a.wa)
        row["wa"] = wa
        peringatan += p
    if a.jenis:
        row["jenis"] = rapikan_jenis(a.jenis)
    if a.tanggal:
        tgl, cat = parse_tanggal(a.tanggal, acuan)
        row["tanggal"] = tgl.isoformat()
        if cat:
            peringatan.append(cat)
    if a.catatan is not None:
        catatan = bersih(a.catatan, 200)
        if catatan:
            cek_data_pribadi("catatan", catatan)
            cek_diagnosis("catatan", catatan)
        row["catatan"] = catatan
    if a.persetujuan:
        if a.persetujuan not in PERSETUJUAN:
            raise Gagal("--persetujuan harus 'ya' atau 'tidak'.")
        row["persetujuan"] = a.persetujuan
    teks = f"Diubah #{row['id']}: {row['nama_panggilan']} | {row['jenis']} | {tgl_id(datetime.strptime(row['tanggal'], '%Y-%m-%d').date(), True)}"
    return {"ok": True, "mode": "tersimpan", "id": row["id"], "teks": teks, "peringatan": peringatan}


def op_ubah_status(a, baris, acuan):
    row = cari(baris, a.id)
    if row is None:
        raise Gagal(f"id {a.id} tidak ditemukan.")
    if a.status not in STATUS:
        raise Gagal(f"--status harus salah satu dari: {', '.join(STATUS)}")
    peringatan = []
    row["status"] = a.status
    if a.status == "sudah-diingatkan":
        row["diingatkan_pada"] = acuan.isoformat()
    elif a.status == "datang":
        if a.berikutnya:
            tgl, cat = parse_tanggal(a.berikutnya, acuan)
            catatan_lama = f"kunjungan sebelumnya {tgl_id(datetime.strptime(row['tanggal'], '%Y-%m-%d').date(), True)} selesai"
            row["catatan"] = tambah_catatan(row.get("catatan"), catatan_lama)
            row["tanggal"] = tgl.isoformat()
            row["status"] = "dijadwalkan"
            row["diingatkan_pada"] = ""
            if cat:
                peringatan.append(cat)
    elif a.status == "batal" and a.alasan:
        alasan = bersih(a.alasan, 120)
        cek_data_pribadi("alasan", alasan)
        row["catatan"] = tambah_catatan(row.get("catatan"), "batal: " + alasan)
    teks = f"#{row['id']} {row['nama_panggilan']}: status -> {row['status']}"
    if row["status"] == "dijadwalkan" and a.status == "datang":
        teks += f" | jadwal berikutnya {tgl_id(datetime.strptime(row['tanggal'], '%Y-%m-%d').date(), True)}"
    return {"ok": True, "mode": "tersimpan", "id": row["id"], "teks": teks, "peringatan": peringatan}


def op_hapus(a, baris):
    if not a.id and not a.wa:
        raise Gagal("sebutkan --id atau --wa yang mau dihapus.")
    cocok = []
    for b in baris:
        if not isinstance(b, dict):
            continue
        if a.id and str(b.get("id")) == str(a.id):
            cocok.append(b)
        elif a.wa:
            wa_target, _ = normalisasi_wa(a.wa)
            if b.get("wa") == wa_target:
                cocok.append(b)
    if not cocok:
        raise Gagal("tidak ada data yang cocok untuk dihapus.")
    ringkas = [f"#{b['id']} {b['nama_panggilan']} ({b['jenis']}, {b['tanggal']})" for b in cocok]
    if not a.ya:
        return {"ok": True, "mode": "pratinjau", "akan_dihapus": ringkas,
                "teks": "Akan dihapus PERMANEN:\n- " + "\n- ".join(ringkas) +
                        "\nUlangi perintah yang sama + --ya untuk menghapus sungguhan."}
    id_cocok = {id(b) for b in cocok}
    sisa = [b for b in baris if id(b) not in id_cocok]
    baris[:] = sisa
    return {"ok": True, "mode": "tersimpan", "dihapus": ringkas,
            "teks": "Dihapus permanen:\n- " + "\n- ".join(ringkas)}


def op_impor(a, baris, acuan):
    header, isi = baca_csv(a.path)
    if header is None:
        raise Gagal(f"file {a.path} tidak ditemukan.")
    kolom_nama = next((h for h in header if h in ("nama", "nama_panggilan", "pasien")), None)
    kolom_wa = next((h for h in header if h in ("wa", "no wa", "nomor", "hp", "whatsapp", "no_wa")), None)
    if not kolom_nama or not kolom_wa:
        raise Gagal("kolom 'nama' dan 'wa' (atau sejenisnya) tidak ditemukan di header CSV.")
    kolom_jenis = next((h for h in header if h in ("jenis", "jenis_kunjungan", "keperluan")), None)
    kolom_tgl = next((h for h in header if h in ("tanggal", "tgl", "jadwal", "tanggal_berikutnya")), None)
    kolom_persetujuan = next((h for h in header if h in ("persetujuan", "setuju", "consent")), None)
    if not kolom_persetujuan and not a.persetujuan_default:
        raise Gagal("file tidak punya kolom persetujuan, dan --persetujuan-default belum diisi. "
                    "Wajib menegaskan persetujuan pasien dihubungi (ya/tidak) sebelum impor.")
    diterima, ditolak = [], []
    for no, b, alasan, sel in isi:
        if b is None:
            ditolak.append({"baris": no, "alasan": alasan})
            continue
        try:
            nama = bersih(b[kolom_nama], 60)
            if not nama:
                raise Gagal("nama kosong")
            cek_data_pribadi("nama", nama)
            wa, _ = normalisasi_wa(b[kolom_wa])
            jenis = rapikan_jenis(b.get(kolom_jenis) or a.jenis_default or "kontrol")
            teks_tgl = b.get(kolom_tgl) or a.tanggal_default
            if not teks_tgl:
                raise Gagal("tanggal kosong dan --tanggal-default tidak diisi")
            tgl, _ = parse_tanggal(teks_tgl, acuan)
            persetujuan = (b.get(kolom_persetujuan) or a.persetujuan_default or "").strip().lower()
            if persetujuan not in PERSETUJUAN:
                raise Gagal(f"persetujuan '{persetujuan}' harus 'ya' atau 'tidak'")
            diterima.append({
                "id": None, "nama_panggilan": nama, "wa": wa, "jenis": jenis, "tanggal": tgl.isoformat(),
                "status": "dijadwalkan", "persetujuan": persetujuan, "dibuat": acuan.isoformat(),
                "diingatkan_pada": "", "catatan": "",
            })
        except (Gagal, DataPribadi) as e:
            ditolak.append({"baris": no, "alasan": str(e)})
    if not a.ya:
        contoh = [f"{d['nama_panggilan']} | {d['jenis']} | {d['tanggal']} | setuju:{d['persetujuan']}"
                  for d in diterima[:10]]
        teks = (f"Pratinjau impor {a.path}: {len(diterima)} pasien akan ditambahkan, "
                f"{len(ditolak)} baris ditolak.\n" + "\n".join(contoh) +
                ("\n... dan lainnya" if len(diterima) > 10 else "") +
                "\nUlangi perintah yang sama + --ya untuk menyimpan.")
        return {"ok": True, "mode": "pratinjau", "akan_ditambah": len(diterima), "ditolak": ditolak, "teks": teks}
    for d in diterima:
        d["id"] = str(id_berikutnya(baris))
        baris.append(d)
    return {"ok": True, "mode": "tersimpan", "ditambahkan": len(diterima), "ditolak": ditolak,
            "teks": f"Impor selesai: {len(diterima)} pasien ditambahkan, {len(ditolak)} baris ditolak."}


def op_daftar(a, baris, acuan):
    kel = kelompokkan(baris, acuan)
    if a.kapan:
        peta = {"terlambat": "terlambat", "hari-ini": "hari_ini", "besok": "h1", "h-1": "h1", "h-3": "h3"}
        if a.kapan == "minggu-ini":
            kunci = ["terlambat", "hari_ini", "h1", "h3"]
        elif a.kapan == "semua":
            kunci = list(kel.keys())
        else:
            if a.kapan not in peta:
                raise Gagal("--kapan harus salah satu dari: terlambat, hari-ini, besok/h-1, h-3, minggu-ini, semua")
            kunci = [peta[a.kapan]]
    else:
        kunci = ["terlambat", "hari_ini", "h1", "h3"]
    judul = {"terlambat": "TERLAMBAT", "hari_ini": "HARI INI", "h1": "BESOK (H-1)", "h3": "H-3"}
    baris_teks = []
    semua_baris = []
    for k in kunci:
        grup = kel.get(k, [])
        if not grup:
            continue
        baris_teks.append(f"{judul.get(k, k.upper())} ({len(grup)})")
        for b in grup[:20]:
            baris_teks.append(f"  #{b['id']} {b['nama_panggilan']} | {b['jenis']} | {tgl_id(datetime.strptime(b['tanggal'], '%Y-%m-%d').date(), True)} | {tampil_wa(b['wa'])}")
            semua_baris.append(b)
        if len(grup) > 20:
            baris_teks.append(f"  ... dan {len(grup) - 20} lainnya")
    if not baris_teks:
        baris_teks.append("Tidak ada jadwal pada kategori ini.")
    if not a.tanpa_draf and semua_baris:
        baris_teks.append("")
        baris_teks.append("DRAF PESAN (salin & kirim sendiri, JANGAN dikirim otomatis):")
        for b in semua_baris[:15]:
            baris_teks.append(f"\n#{b['id']} {b['nama_panggilan']} ({tampil_wa(b['wa'])}):")
            baris_teks.append(buat_draf(b, a.klinik))
        if len(semua_baris) > 15:
            baris_teks.append(f"\n... dan {len(semua_baris) - 15} lainnya. Pakai 'draf --id <id>' untuk melihatnya.")
    return {"ok": True, "mode": "baca", "kelompok": {k: len(v) for k, v in kel.items()}, "teks": "\n".join(baris_teks)}


def op_draf(a, baris):
    row = cari(baris, a.id)
    if row is None:
        raise Gagal(f"id {a.id} tidak ditemukan.")
    if row.get("persetujuan") != "ya":
        raise Gagal(f"pasien #{a.id} belum memberi persetujuan dihubungi (persetujuan={row.get('persetujuan')}). "
                    "Draf tidak dibuat.")
    return {"ok": True, "mode": "baca", "id": row["id"], "teks": buat_draf(row, a.klinik)}


def op_ringkasan(a, baris, acuan):
    kel = kelompokkan(baris, acuan)
    total_aktif = sum(1 for b in baris if isinstance(b, dict) and b.get("status") in STATUS_AKTIF)
    baris_teks = [f"Ringkasan pengingat pasien — {tgl_id(acuan)}",
                  f"Terlambat: {len(kel['terlambat'])} | Hari ini: {len(kel['hari_ini'])} | "
                  f"Besok (H-1): {len(kel['h1'])} | H-3: {len(kel['h3'])} | Total aktif dijadwalkan: {total_aktif}"]
    if not a.tanpa_nama:
        for k, label in (("terlambat", "Terlambat"), ("hari_ini", "Hari ini"), ("h1", "Besok"), ("h3", "H-3")):
            grup = kel[k]
            if not grup:
                continue
            nama_list = [(samar_nama(b["nama_panggilan"]) if a.samarkan else b["nama_panggilan"]) + f" ({b['jenis']})"
                         for b in grup[:20]]
            baris_teks.append(f"{label}: " + ", ".join(nama_list) + (f", ... +{len(grup)-20}" if len(grup) > 20 else ""))
    baris_teks.append("(Ringkasan ini TIDAK memuat nomor WA. Draf pesan ada di 'daftar' atau 'draf --id'.)")
    return {"ok": True, "mode": "baca", "teks": "\n".join(baris_teks)}


def op_info(a, baris, path):
    per_status = {}
    for b in baris:
        if isinstance(b, dict):
            per_status[b.get("status", "?")] = per_status.get(b.get("status", "?"), 0) + 1
    teks = f"File: {os.path.abspath(path)}\nTotal baris: {sum(1 for b in baris if isinstance(b, dict))}\n" + \
           "\n".join(f"  {k}: {v}" for k, v in per_status.items())
    return {"ok": True, "mode": "baca", "teks": teks, "per_status": per_status}


# --------------------------------------------------------------------------- main
def buat_parser():
    p = argparse.ArgumentParser(description="Pengingat kontrol/vaksin pasien klinik (lokal, tanpa rekam medis).")
    p.add_argument("--file", default=os.path.join("pasien", "DAFTAR.csv"))
    p.add_argument("--hari-ini", help="Tanggal acuan (untuk uji), format bebas mis. 2026-10-01")
    p.add_argument("--tz", default="Asia/Jakarta")
    p.add_argument("--json", action="store_true")
    sub = p.add_subparsers(dest="perintah", required=True)

    s = sub.add_parser("tambah")
    s.add_argument("--nama", required=True)
    s.add_argument("--wa", required=True)
    s.add_argument("--jenis", required=True)
    s.add_argument("--tanggal", required=True)
    s.add_argument("--persetujuan", required=True, choices=PERSETUJUAN)
    s.add_argument("--catatan", default="")

    s = sub.add_parser("ubah")
    s.add_argument("--id", required=True)
    s.add_argument("--nama")
    s.add_argument("--wa")
    s.add_argument("--jenis")
    s.add_argument("--tanggal")
    s.add_argument("--catatan")
    s.add_argument("--persetujuan", choices=PERSETUJUAN)

    s = sub.add_parser("ubah-status")
    s.add_argument("--id", required=True)
    s.add_argument("--status", required=True, choices=STATUS)
    s.add_argument("--berikutnya")
    s.add_argument("--alasan")

    s = sub.add_parser("hapus")
    s.add_argument("--id")
    s.add_argument("--wa")
    s.add_argument("--ya", action="store_true")

    s = sub.add_parser("impor")
    s.add_argument("path")
    s.add_argument("--jenis-default")
    s.add_argument("--tanggal-default")
    s.add_argument("--persetujuan-default", choices=PERSETUJUAN)
    s.add_argument("--ya", action="store_true")

    s = sub.add_parser("daftar")
    s.add_argument("--kapan", choices=["terlambat", "hari-ini", "besok", "h-1", "h-3", "minggu-ini", "semua"])
    s.add_argument("--tanpa-draf", dest="tanpa_draf", action="store_true")
    s.add_argument("--klinik", default="")

    s = sub.add_parser("draf")
    s.add_argument("--id", required=True)
    s.add_argument("--klinik", default="")

    s = sub.add_parser("ringkasan")
    s.add_argument("--samarkan", action="store_true")
    s.add_argument("--tanpa-nama", dest="tanpa_nama", action="store_true")

    sub.add_parser("info")
    return p


def main(argv=None):
    a = buat_parser().parse_args(argv)
    try:
        acuan = hari_ini_di(a.tz) if not a.hari_ini else parse_tanggal(a.hari_ini, hari_ini_di(a.tz))[0]
        baris, rusak = muat_daftar(a.file)
        hasil = None
        if a.perintah == "tambah":
            hasil = op_tambah(a, baris, acuan)
        elif a.perintah == "ubah":
            hasil = op_ubah(a, baris, acuan)
        elif a.perintah == "ubah-status":
            hasil = op_ubah_status(a, baris, acuan)
        elif a.perintah == "hapus":
            hasil = op_hapus(a, baris)
        elif a.perintah == "impor":
            hasil = op_impor(a, baris, acuan)
        elif a.perintah == "daftar":
            hasil = op_daftar(a, baris, acuan)
        elif a.perintah == "draf":
            hasil = op_draf(a, baris)
        elif a.perintah == "ringkasan":
            hasil = op_ringkasan(a, baris, acuan)
        elif a.perintah == "info":
            hasil = op_info(a, baris, a.file)

        if a.perintah in ("tambah", "ubah", "ubah-status", "hapus", "impor") and hasil.get("mode") == "tersimpan":
            tulis_csv_atomik(a.file, baris)
        if rusak:
            hasil.setdefault("baris_ditolak", rusak)
            if rusak and not a.json:
                hasil["teks"] += "\n\nPeringatan: ada baris rusak di file (tidak ikut diproses): " + \
                                  "; ".join(f"baris {r['baris']}: {r['alasan']}" for r in rusak)
    except DataPribadi as e:
        if a.json:
            print(json.dumps({"ok": False, "error": str(e)}, ensure_ascii=False))
        else:
            print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(2)
    except Gagal as e:
        if a.json:
            print(json.dumps({"ok": False, "error": str(e)}, ensure_ascii=False))
        else:
            print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)

    if a.json:
        print(json.dumps(hasil, ensure_ascii=False))
    else:
        print(hasil["teks"])
    sys.exit(0)


if __name__ == "__main__":
    main()
