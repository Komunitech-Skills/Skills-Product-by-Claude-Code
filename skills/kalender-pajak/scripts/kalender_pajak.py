#!/usr/bin/env python3
"""Kalender tenggat SETOR & LAPOR pajak Indonesia (PMK 81/2024) per profil wajib pajak.

Hanya JADWAL, bukan menghitung besaran pajak. Python standar saja, lintas OS.

Contoh (Windows: ganti python3 dengan python atau py):
  python3 kalender_pajak.py --profil op-umkm,pemberi-kerja --tahun 2026
  python3 kalender_pajak.py --profil badan-pkp --tahun 2026 --bulan-mulai 10 --format ics --keluar pajak.ics
  python3 kalender_pajak.py --profil badan-pkp,pemberi-kerja,pemotong --hari-ini 2026-09-25
  python3 kalender_pajak.py --profil op-umkm --tahun 2027 --format ics --acara-pengingat --keluar pajak.ics
  python3 kalender_pajak.py --daftar-profil

Keluar kode 0 = sukses, 2 = input salah (pesan 'ERROR: ...', tanpa traceback).
"""
import argparse
import calendar
import csv
import datetime as dt
import hashlib
import io
import json
import re
import sys
from pathlib import Path

SINI = Path(__file__).resolve().parent
REF = SINI.parent / "references"
TANGGAL_CEK = "2026-09-26"
VERSI = "1.0.7"
TAHUN_MIN, TAHUN_MAKS = 2025, 2100

BULAN = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus",
         "September", "Oktober", "November", "Desember"]
BLN = ["Jan", "Feb", "Mar", "Apr", "Mei", "Jun", "Jul", "Agu", "Sep", "Okt", "Nov", "Des"]
HARI = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"]

# ---------------------------------------------------------------------------
# Aturan (sumber & status verifikasi: references/aturan-tenggat.md)
# setor/lapor: 15 / 20 = tanggal itu bulan berikutnya; "akhir" = hari terakhir bulan berikutnya;
# None = tidak ada acara terpisah. "unggah" = batas unggah faktur (tidak bergeser, lihat catatan).
# ---------------------------------------------------------------------------
KEWAJIBAN_MASA = {
    "pph-final-umkm": {
        "pajak": "PPh Final UMKM 0,5% (PP 55/2022)",
        "setor": 15, "lapor": None,
        "catatan": "Setor yang tervalidasi dianggap sudah lapor SPT Masa (PMK 81/2024). "
                   "Hanya bila ada PPh terutang: orang pribadi tidak setor selama omzet kumulatif "
                   "setahun masih <= Rp500 juta. Besarannya: skill pph-final-umkm (bila terpasang).",
    },
    "pph21": {
        "pajak": "PPh 21/26 (pemberi kerja)",
        "setor": 15, "lapor": 20, "nama_spt": "SPT Masa PPh 21/26",
        "catatan": "Besarannya: skill pph21-ter (bila terpasang). Bukti potong dibuat di Coretax.",
    },
    "unifikasi": {
        "pajak": "PPh Unifikasi (PPh 4(2), 15, 22, 23, 26 non-pegawai)",
        "setor": 15, "lapor": 20, "nama_spt": "SPT Masa PPh Unifikasi",
        "catatan": "Untuk pemotong/pemungut, mis. potong PPh 23 jasa atau PPh 4(2) sewa.",
    },
    "ppn": {
        "pajak": "PPN (PKP)",
        "setor": "akhir", "lapor": "akhir", "nama_spt": "SPT Masa PPN",
        "unggah": 20,
        "catatan": "Setor paling lambat akhir bulan berikutnya DAN sebelum SPT Masa PPN dikirim. "
                   "PKP tetap lapor walau nihil. Faktur pajak keluaran wajib diunggah & mendapat "
                   "persetujuan DJP paling lambat tgl 20 bulan berikutnya setelah tanggal pembuatan faktur "
                   "(PER-11/PJ/2025 Ps. 44 ayat 1); faktur yang tidak disetujui bukan faktur pajak sah. "
                   "Batas unggah faktur TIDAK bergeser walau tgl 20 hari libur (PER-11/PJ/2025 tidak memuat "
                   "ketentuan pergeseran; PERLU REVIEW) - unggah sebelum tgl 20. Besarannya: skill hitung-ppn (bila terpasang).",
    },
    "pph25": {
        "pajak": "PPh 25 (angsuran bulanan)",
        "setor": 15, "lapor": None,
        "catatan": "Batas lapor SPT Masa PPh 25 tgl 20, tetapi setoran yang tervalidasi (ada NTPN) "
                   "dianggap sudah lapor pada tanggal setor (PMK 81/2024 Ps. 171 ayat 10) - jadi cukup setor paling lambat tgl 15. "
                   "Angsuran nihil tidak perlu setor.",
    },
}

KEWAJIBAN_TAHUNAN = {
    "spt-op": {
        "pajak": "SPT Tahunan PPh Orang Pribadi",
        "bulan_ke": 3,
        "judul": "LAPOR SPT Tahunan PPh Orang Pribadi",
        "catatan": "Paling lambat 3 bulan setelah akhir tahun pajak. Kurang bayar (PPh 29) dilunasi "
                   "SEBELUM SPT dikirim. Tidak bergeser meski hari libur (PMK 81/2024 Ps. 169); lapor lebih awal. "
                   "DJP kadang memberi perpanjangan khusus lewat pengumuman.",
    },
    "spt-badan": {
        "pajak": "SPT Tahunan PPh Badan",
        "bulan_ke": 4,
        "judul": "LAPOR SPT Tahunan PPh Badan",
        "catatan": "Paling lambat akhir bulan ke-4 setelah akhir tahun buku (dianggap tahun buku "
                   "Januari-Desember). Kurang bayar (PPh 29) dilunasi SEBELUM SPT dikirim. Tidak bergeser "
                   "meski hari libur (PMK 81/2024 Ps. 169); lapor lebih awal.",
    },
    "bukti-a1": {
        "pajak": "Bukti potong PPh 21 tahunan (BPA1, dulu 1721-A1)",
        "bulan_ke": 1,
        "judul": "BERIKAN bukti potong BPA1 ke karyawan",
        "catatan": "Paling lama 1 bulan setelah masa pajak terakhir (PER-2/PJ/2024). Karyawan butuh ini "
                   "untuk SPT Tahunan. Tanggal ditampilkan tanpa pergeseran (PERLU REVIEW).",
    },
}

PROFIL = {
    "op-umkm": (["pph-final-umkm", "spt-op"],
                "Orang pribadi usaha, PPh final 0,5% (PP 55/2022)"),
    "op-karyawan": (["spt-op"], "Orang pribadi karyawan/pekerja tanpa usaha"),
    "op-pembukuan": (["pph25", "spt-op"],
                     "Orang pribadi usaha/pekerjaan bebas dengan tarif umum (pembukuan/norma)"),
    "badan-umkm": (["pph-final-umkm", "spt-badan"],
                   "PT perorangan/koperasi yang memakai PPh final 0,5%"),
    "badan-umum": (["pph25", "spt-badan"], "Badan dengan tarif umum, bukan PKP"),
    "badan-pkp": (["ppn", "pph25", "spt-badan"], "Badan PKP (memungut PPN), tarif umum"),
    "pkp": (["ppn"], "Tambahan: sudah dikukuhkan PKP (untuk orang pribadi/badan UMKM yang PKP)"),
    "pemberi-kerja": (["pph21", "bukti-a1"], "Tambahan: punya karyawan (memotong PPh 21)"),
    "pemotong": (["unifikasi"], "Tambahan: memotong PPh 23/4(2)/15/22/26 (mis. bayar jasa, sewa)"),
}

SEMUA_KEWAJIBAN = list(KEWAJIBAN_MASA) + list(KEWAJIBAN_TAHUNAN)

# SPT Tahunan: batasnya diatur PMK 81/2024 Ps. 169 dan TIDAK bergeser walau jatuh di hari libur
# (Ps. 173 ayat 1 hanya menggeser pelaporan Ps. 171 & 172; Ps. 172 = PPN membangun sendiri & PPN
# pemanfaatan dari luar Daerah Pabean oleh bukan-PKP). Dicocokkan dengan naskah resmi 2026-09-26.
TAHUNAN_TIDAK_GESER = ("spt-op", "spt-badan")

# Kebijakan khusus DJP yang sudah diketahui (tanggal di kalender TIDAK diubah; hanya diberi catatan).
# KEP-55/PJ/2026 TIDAK memperpanjang jatuh tempo: jatuh tempo SPT OP TP 2025 tetap 31 Mar 2026;
# yang dihapus hanya sanksi administratif (denda/bunga) bila lapor/bayar s.d. 30 Apr 2026, khusus
# orang pribadi. Sumber resmi: https://pajak.go.id/en/node/119611 (dicek 2026-09-30).
# Badan: KEP-71/PJ/2026 juga TIDAK mengubah jatuh tempo (4 bulan setelah akhir tahun pajak); sanksi
# denda/bunga dihapus bila lapor/bayar s.d. 1 bulan setelah jatuh tempo. Sumber resmi:
# https://www.pajak.go.id/id/pengumuman/kebijakan-penghapusan-sanksi-administratif-atas-keterlambatan-pembayaran-dan-pelaporan-1
PERPANJANGAN_KHUSUS = {
    ("spt-op", 2025): ("jatuh tempo tetap 31 Mar 2026; KEP-55/PJ/2026 menghapus sanksi denda/bunga "
                       "bila lapor/bayar paling lambat 30 Apr 2026 (khusus orang pribadi, bukan perpanjangan)"),
    ("spt-badan", 2025): ("jatuh tempo tetap; KEP-71/PJ/2026 menghapus sanksi denda/bunga bila lapor/bayar "
                          "paling lambat 1 bulan setelah jatuh tempo (bukan perpanjangan)"),
}

DISCLAIMER = (
    "Bukan nasihat pajak. Dasar: PMK 81/2024 (berlaku 1 Jan 2025), PP 55/2022 jo. PP 20/2026, "
    "PER-2/PJ/2024, PER-11/PJ/2025, SKB 3 Menteri libur nasional & cuti bersama; dicek " + TANGGAL_CEK +
    " (pasal tenggat PMK 81/2024 & PER-11/PJ/2025 dicocokkan dengan naskah resmi di pajak.go.id; "
    "sebagian butir lain dari sumber sekunder). DJP kadang memundurkan tenggat lewat "
    "pengumuman khusus - cek pengumuman DJP terbaru (pajak.go.id, Kring Pajak 1500200). "
    "Pembulatan/perhitungan pajak tidak dilakukan skill ini dan belum dicocokkan dengan Coretax. "
    "Untuk kasus Anda, konsultasikan dengan konsultan pajak atau Account Representative (AR)."
)


class InputSalah(Exception):
    pass


# ---------------------------------------------------------------------------
# Data libur
# ---------------------------------------------------------------------------
def muat_libur(ekstra=None, tahun_pengguna=None):
    """Kembalikan (dict tanggal -> keterangan, set tahun yang punya data RESMI dari references/).
    Tanggal dari file --libur (buatan pengguna) tetap dipakai untuk menggeser, tetapi tahunnya
    TIDAK dianggap punya data resmi (peringatan tetap muncul); tahunnya dicatat ke `tahun_pengguna`."""
    libur, tahun_ada = {}, set()
    resmi = sorted(REF.glob("libur-nasional-*.csv"))
    berkas = [(f, True) for f in resmi] + [(Path(p), False) for p in (ekstra or [])]
    for f, dari_resmi in berkas:
        if not f.is_file():
            raise InputSalah("file libur '%s' tidak ditemukan" % f)
        try:
            with f.open(newline="", encoding="utf-8-sig") as h:
                r = csv.DictReader(h)
                if not r.fieldnames or "tanggal" not in r.fieldnames:
                    raise InputSalah("file libur '%s' harus punya kolom 'tanggal' (dan opsional "
                                     "'jenis','keterangan')" % f.name)
                for no, b in enumerate(r, start=2):
                    try:
                        t = dt.date.fromisoformat((b.get("tanggal") or "").strip())
                    except ValueError:
                        raise InputSalah("file libur '%s' baris %d: tanggal '%s' bukan format "
                                         "YYYY-MM-DD" % (f.name, no, b.get("tanggal")))
                    jenis = (b.get("jenis") or "libur").strip()
                    ket = (b.get("keterangan") or "").strip()
                    sisa = [x.strip() for x in (b.get(None) or []) if x and x.strip()]
                    if sisa:  # koma tanpa tanda kutip di keterangan -> gabungkan, jangan terpotong
                        ket = ", ".join([ket] + sisa) if ket else ", ".join(sisa)
                    ket = ket or "hari libur"
                    libur[t] = ("cuti bersama: " if jenis == "cuti" and not ket.lower().startswith("cuti")
                                else "") + ket
                    if dari_resmi:
                        tahun_ada.add(t.year)
                    elif tahun_pengguna is not None:
                        tahun_pengguna.add(t.year)
        except UnicodeDecodeError:
            raise InputSalah("file libur '%s' bukan teks UTF-8" % f.name)
    return libur, tahun_ada


def hari_libur(t, libur):
    """Alasan tanggal ini bukan hari kerja (mis. 'Sabtu & Idulfitri 1447 H'), atau None."""
    bagian = []
    if t.weekday() >= 5:
        bagian.append(HARI[t.weekday()])
    if t in libur:
        bagian.append(libur[t])
    return " & ".join(bagian) or None


def geser(t, libur, tahun_ada, kurang):
    """Geser ke hari kerja berikutnya. Kembalikan (tanggal akhir, [alasan]).
    Tahun tanpa data libur yang dilewati dicatat ke `kurang`."""
    alasan = []
    while True:
        if t.year not in tahun_ada:
            kurang.add(t.year)
        a = hari_libur(t, libur)
        if not a:
            return t, alasan
        alasan.append("%s: %s" % (fmt_pendek(t), a))
        t += dt.timedelta(days=1)


def hari_kerja_sebelum(t, libur):
    """Hari kerja terakhir SEBELUM tanggal t (saran menyelesaikan tenggat yang tidak bergeser)."""
    t -= dt.timedelta(days=1)
    while hari_libur(t, libur):
        t -= dt.timedelta(days=1)
    return t


# ---------------------------------------------------------------------------
# Tanggal
# ---------------------------------------------------------------------------
def bulan_berikut(th, bl, n=1):
    i = th * 12 + (bl - 1) + n
    return i // 12, i % 12 + 1


def tgl_aturan(th, bl, aturan):
    if aturan == "akhir":
        return dt.date(th, bl, calendar.monthrange(th, bl)[1])
    return dt.date(th, bl, aturan)


def fmt_pendek(t):
    return "%d %s" % (t.day, BLN[t.month - 1])


def fmt_panjang(t):
    return "%s, %d %s %d" % (HARI[t.weekday()], t.day, BULAN[t.month - 1], t.year)


# ---------------------------------------------------------------------------
# Susun acara
# ---------------------------------------------------------------------------
def urai_profil(teks_list):
    kewajiban, profil_dipakai = [], []
    for teks in teks_list:
        for p in re.split(r"[,\s;]+", teks.strip().lower()):
            if not p:
                continue
            if p in PROFIL:
                profil_dipakai.append(p)
                kewajiban += PROFIL[p][0]
            elif p in SEMUA_KEWAJIBAN:
                profil_dipakai.append(p)
                kewajiban.append(p)
            else:
                raise InputSalah("profil/kewajiban '%s' tidak dikenal. Pilihan profil: %s. "
                                 "Pilihan kewajiban: %s. Lihat --daftar-profil."
                                 % (p, ", ".join(PROFIL), ", ".join(SEMUA_KEWAJIBAN)))
    if not kewajiban:
        raise InputSalah("isi --profil, mis. --profil op-umkm atau --profil badan-pkp,pemberi-kerja")
    unik = []
    for k in kewajiban:
        if k not in unik:
            unik.append(k)
    return profil_dipakai, unik


def uid(*bagian):
    h = hashlib.sha1("|".join(str(b) for b in bagian).encode("utf-8")).hexdigest()[:20]
    return "%s@kalender-pajak.komunitech" % h


def buat_acara(kewajiban, awal, akhir, libur, tahun_ada):
    """Acara dengan tanggal akhir (sesudah geser) di [awal, akhir]."""
    acara, kurang = [], set()

    def tambah(kode, jenis, judul, pajak, masa_label, normal, bisa_geser, catatan):
        cek, libur_tetap, saran = set(), None, None
        if bisa_geser:
            final, alasan = geser(normal, libur, tahun_ada, cek)
        else:
            final, alasan = normal, []
            if normal.year not in tahun_ada:
                cek.add(normal.year)
            libur_tetap = hari_libur(normal, libur)
            if libur_tetap:
                saran = hari_kerja_sebelum(normal, libur)
        if awal <= final <= akhir:
            kurang.update(cek)
            acara.append({
                "tanggal": final, "tanggal_normal": normal, "kode": kode, "jenis": jenis,
                "judul": judul, "pajak": pajak, "masa": masa_label, "alasan_geser": alasan,
                "bisa_geser": bisa_geser, "catatan": catatan, "libur_tetap": libur_tetap,
                "uid": uid(kode, jenis, masa_label),
                "saran_sebelum": saran,
            })

    # masa pajak yang mungkin tenggatnya jatuh di rentang (mundur 3 bulan cukup: geser maks. beberapa hari)
    th, bl = bulan_berikut(awal.year, awal.month, -3)
    while (th, bl) <= (akhir.year, akhir.month):
        masa_label = "%s %d" % (BLN[bl - 1], th)
        nth, nbl = bulan_berikut(th, bl)
        for k in kewajiban:
            a = KEWAJIBAN_MASA.get(k)
            if not a:
                continue
            ts = tgl_aturan(nth, nbl, a["setor"])
            tl = tgl_aturan(nth, nbl, a["lapor"]) if a["lapor"] is not None else None
            if a.get("unggah"):
                tu = tgl_aturan(nth, nbl, a["unggah"])
                tambah(k, "unggah", "UNGGAH faktur pajak keluaran bulan %s (batas persetujuan DJP)" % masa_label,
                       "Faktur Pajak Keluaran (PKP)", masa_label, tu, False, a["catatan"])
            if tl is not None and tl == ts:
                tambah(k, "setor+lapor", "SETOR & LAPOR %s masa %s" % (a["nama_spt"].replace("SPT Masa ", ""), masa_label),
                       a["pajak"], masa_label, ts, True, a["catatan"])
            else:
                tambah(k, "setor", "SETOR %s masa %s" % (a["pajak"], masa_label), a["pajak"],
                       masa_label, ts, True, a["catatan"])
                if tl is not None:
                    tambah(k, "lapor", "LAPOR %s masa %s" % (a["nama_spt"], masa_label), a["pajak"],
                           masa_label, tl, True, a["catatan"])
        th, bl = nth, nbl

    for k in kewajiban:
        a = KEWAJIBAN_TAHUNAN.get(k)
        if not a:
            continue
        for tp in range(awal.year - 2, akhir.year + 1):
            yth, ybl = bulan_berikut(tp, 12, a["bulan_ke"])
            normal = tgl_aturan(yth, ybl, "akhir")
            tambah(k, "tahunan", "%s tahun pajak %d" % (a["judul"], tp), a["pajak"],
                   "Tahun pajak %d" % tp, normal, False, a["catatan"])
            if acara and acara[-1]["kode"] == k and acara[-1]["masa"] == "Tahun pajak %d" % tp:
                acara[-1]["perpanjangan"] = PERPANJANGAN_KHUSUS.get((k, tp))

    urut = {k: i for i, k in enumerate(SEMUA_KEWAJIBAN)}
    jenis_urut = {"setor": 0, "setor+lapor": 1, "lapor": 2, "unggah": 3, "tahunan": 4}
    acara.sort(key=lambda e: (e["tanggal"], jenis_urut[e["jenis"]], urut[e["kode"]]))
    return acara, kurang


# ---------------------------------------------------------------------------
# Keluaran
# ---------------------------------------------------------------------------
def ket_geser(e):
    teks = "-"
    if e.get("libur_tetap"):
        teks = ("jatuh pada hari libur (%s) dan TIDAK bergeser - selesaikan paling lambat hari kerja "
                "sebelumnya: %s" % (e["libur_tetap"], fmt_panjang(e["saran_sebelum"])))
        if e["kode"] in TAHUNAN_TIDAK_GESER:
            teks += "; tidak bergeser meski hari libur (PMK 81/2024 Ps. 169); lapor lebih awal"
    elif e["alasan_geser"]:
        teks = "bergeser dari %s (%s)" % (fmt_pendek(e["tanggal_normal"]), "; ".join(e["alasan_geser"]))
    if e.get("perpanjangan"):
        teks = e["perpanjangan"] if teks == "-" else teks + "; " + e["perpanjangan"]
    return teks


def pesan_kurang(kurang, tahun_ada, tahun_pengguna=None):
    if not kurang:
        return None
    pakai = sorted(set(kurang) & set(tahun_pengguna or ()))
    teks = ("PERINGATAN: data libur nasional/cuti bersama resmi tahun %s belum ada di skill (tersedia: %s). "
            % (", ".join(str(t) for t in sorted(kurang)), ", ".join(str(t) for t in sorted(tahun_ada)) or "-"))
    if pakai:
        teks += ("Untuk tahun %s dipakai data libur dari pengguna (file --libur, belum diverifikasi, bisa "
                 "belum lengkap) ditambah Sabtu/Minggu - tanggal bisa kurang tepat. Cocokkan dengan SKB 3 "
                 "Menteri tahun tersebut. " % ", ".join(str(t) for t in pakai))
        sisa = sorted(set(kurang) - set(pakai))
        if sisa:
            teks += "Untuk tahun %s hanya Sabtu/Minggu yang diperhitungkan. " % ", ".join(str(t) for t in sisa)
        return teks.rstrip()
    return teks + ("Untuk tahun itu hanya Sabtu/Minggu yang diperhitungkan - tanggal bisa kurang tepat. "
                   "Cek SKB 3 Menteri tahun tersebut dan tambahkan file references/libur-nasional-<tahun>.csv "
                   "atau pakai --libur <file.csv>.")


CATATAN_ICS = (
    "Catatan pengingat: file .ics memuat pengingat H-3 & H-1 pukul 09.00 (VALARM). Apple Calendar & "
    "Outlook biasanya memakainya, tetapi Google Calendar sering MENGABAIKAN pengingat dari file impor dan "
    "memakai notifikasi default kalender. Di Google Calendar: atur notifikasi default kalender tujuan "
    "(mis. 3 hari & 1 hari sebelumnya) atau buat ulang file dengan --acara-pengingat (acara pengingat "
    "terpisah H-3 & H-1). Impor ulang: UID tetap sama sehingga Apple/Outlook umumnya memperbarui acara, "
    "tetapi Google Calendar bisa tetap membuat duplikat - hapus kalender lama/impor ke kalender baru bila "
    "perlu."
)


CATATAN_ICS_PENGINGAT = (
    "Catatan pengingat: file .ics memuat pengingat H-3 & H-1 pukul 09.00 (VALARM) DAN acara pengingat "
    "terpisah H-3 & H-1 per tenggat (untuk Google Calendar yang sering mengabaikan pengingat dari file "
    "impor). Impor ulang: UID tetap sama sehingga Apple/Outlook umumnya memperbarui acara, tetapi Google "
    "Calendar bisa tetap membuat duplikat - hapus kalender lama/impor ke kalender baru bila perlu."
)


def baris_info(info):
    """Baris cakupan periode & sumber data libur (untuk md/checklist/hari-ini)."""
    o = ["Cakupan: tenggat yang **jatuh** pada %s s.d. %s (termasuk tenggat masa pajak bulan sebelum "
         "periode). %s" % (fmt_panjang(info["awal"]), fmt_panjang(info["akhir"]), info["cakupan_lanjut"]),
         "Data libur: %s." % info["sumber_libur"]]
    return o


BATAS_BEBAS_OP = 500000000
_SATUAN_RP = [("miliar", 10 ** 9), ("milyar", 10 ** 9), ("juta", 10 ** 6), ("ribu", 10 ** 3), ("jt", 10 ** 6),
              ("rb", 10 ** 3), ("m", 10 ** 9), ("k", 10 ** 3)]


def rupiah(teks, nama):
    """'600jt' | '1,2 M' | '48.000.000' | 'Rp 50 juta' -> int rupiah (>= 0)."""
    asli = str(teks)
    t = re.sub(r"(?i)^\s*(rp\.?|idr)\s*", "", asli.strip()).lower().replace(" ", "")
    kali = 1
    for akhiran, k in _SATUAN_RP:
        if t.endswith(akhiran):
            t, kali = t[:-len(akhiran)], k
            break
    if kali > 1:
        t = t.replace(",", ".") if t.count(",") == 1 and "." not in t else t.replace(",", "")
        if t.count(".") > 1:
            raise InputSalah("%s: '%s' tidak dikenali (mis. 600jt, 1,2 miliar, 48.000.000)" % (nama, asli))
    else:
        if not re.fullmatch(r"\d{1,3}(\.\d{3})+|\d+", t):
            raise InputSalah("%s: '%s' tidak dikenali (mis. 600jt, 1,2 miliar, 48.000.000)" % (nama, asli))
        t = t.replace(".", "")
    try:
        nilai = float(t) * kali
    except ValueError:
        raise InputSalah("%s: '%s' bukan angka" % (nama, asli))
    if nilai < 0:
        raise InputSalah("%s tidak boleh negatif" % nama)
    return int(round(nilai))


def fmt_rp(n):
    return "Rp " + "{:,}".format(int(n)).replace(",", ".")


def hitung_lewat_batas(tahun, omzet_bulanan, sumber, libur, tahun_ada, kurang):
    """Bulan pertama omzet kumulatif orang pribadi MELEWATI Rp500 juta (PP 55/2022: s.d. Rp500 juta tidak
    dikenai PPh final). omzet_bulanan: list omzet Januari, Februari, ... (maks 12)."""
    baris, kum, lewat = [], 0, None
    for i, o in enumerate(omzet_bulanan, start=1):
        sebelum = kum
        kum += o
        baris.append("- %s %d: omzet %s, kumulatif %s%s" % (
            BULAN[i - 1], tahun, fmt_rp(o), fmt_rp(kum),
            "  <- MELEWATI Rp500 juta" if sebelum <= BATAS_BEBAS_OP < kum else ""))
        if lewat is None and sebelum <= BATAS_BEBAS_OP < kum:
            lewat = (i, sebelum, kum)
    o = ["**Kapan omzet kumulatif melewati Rp500 juta** (orang pribadi; dihitung script, %s)" % sumber,
         "Rumus: kumulatif = jumlah omzet Januari s.d. bulan itu. Omzet s.d. Rp500 juta setahun tidak dikenai "
         "PPh final (PP 55/2022); bulan pertama kumulatif > Rp500 juta = masa pertama yang wajib setor."] + baris
    hasil = {"sumber": sumber, "bulan_lewat": None, "kumulatif_akhir": kum}
    if lewat:
        i, sebelum, sesudah = lewat
        th, bl = bulan_berikut(tahun, i, 1)
        normal = tgl_aturan(th, bl, 15)
        t, alasan = geser(normal, libur, tahun_ada, kurang)
        o.append("Hasil: omzet kumulatif melewati Rp500 juta pada **%s %d** (s.d. %s %s; s.d. %s %s). Masa "
                 "sebelumnya tidak ada setoran PPh final. Omzet %s %d yang kena pajak = %s - Rp 500.000.000 = %s; "
                 "bulan-bulan sesudahnya seluruh omzet kena. Setoran pertama (masa %s %d) paling lambat **%s**%s."
                 % (BULAN[i - 1], tahun, BULAN[i - 2] if i > 1 else "awal tahun", fmt_rp(sebelum), BULAN[i - 1],
                    fmt_rp(sesudah), BULAN[i - 1], tahun, fmt_rp(sesudah), fmt_rp(sesudah - BATAS_BEBAS_OP),
                    BULAN[i - 1], tahun, fmt_panjang(t),
                    (" (bergeser dari %s karena %s)" % (fmt_pendek(normal), "; ".join(alasan))) if alasan else ""))
        hasil.update({"bulan_lewat": i, "kumulatif_sebelum": sebelum, "kumulatif_sesudah": sesudah,
                      "omzet_kena_bulan_lewat": sesudah - BATAS_BEBAS_OP, "setor_pertama": t.isoformat()})
    else:
        o.append("Hasil: s.d. %s %d omzet kumulatif %s, belum melewati Rp500 juta (sisa %s). Belum ada "
                 "setoran PPh final untuk masa-masa ini." % (BULAN[len(omzet_bulanan) - 1], tahun, fmt_rp(kum),
                                                            fmt_rp(BATAS_BEBAS_OP - kum)))
    o.append("Besaran pajaknya tidak dihitung di sini - pakai skill pph-final-umkm bila terpasang. Badan "
             "(PT perorangan/koperasi) tidak mendapat pembebasan Rp500 juta.")
    hasil["teks"] = o
    return hasil


def blok_omzet(info):
    om = info.get("omzet")
    return ([""] + om["teks"]) if om else []


def keluaran_md(acara, info):
    o = []
    o.append("## Kalender Pajak %s - %s" % (info["judul_rentang"], info["label_profil"]))
    o.append("")
    o.append("Kewajiban: %s" % ", ".join(info["kewajiban_nama"]))
    o += [""] + baris_info(info)
    if info["peringatan"]:
        o += ["", "> **%s**" % info["peringatan"]]
    o.append("")
    if not acara:
        o.append("_Tidak ada tenggat dalam rentang ini._")
    else:
        o.append("| Tanggal | Kegiatan | Keterangan |")
        o.append("|---|---|---|")
        for e in acara:
            o.append("| %s | %s | %s |" % (fmt_panjang(e["tanggal"]), e["judul"], ket_geser(e)))
    o += blok_omzet(info)
    o += ["", "**Catatan per kewajiban**"]
    for k in info["kewajiban"]:
        a = KEWAJIBAN_MASA.get(k) or KEWAJIBAN_TAHUNAN[k]
        o.append("- %s: %s" % (a["pajak"], a["catatan"]))
    o += ["", "**Aturan pergeseran:** tenggat setor & lapor bulanan yang jatuh pada Sabtu, Minggu, "
              "libur nasional, atau cuti bersama bergeser ke hari kerja berikutnya (PMK 81/2024). "
              "SPT Tahunan dan batas unggah faktur pajak ditampilkan tanpa pergeseran (lebih aman bila "
              "ternyata boleh bergeser); bila jatuh di hari libur, disebutkan hari kerja sebelumnya. Sebaiknya setor/lapor 2-3 hari sebelum tenggat.",
          "", "_%s_" % DISCLAIMER]
    return "\n".join(o) + "\n"


def keluaran_checklist(acara, info):
    o = ["## Checklist Pajak Bulanan - %s" % info["label_profil"], ""] + baris_info(info) + [""]
    if info["peringatan"]:
        o += ["> **%s**" % info["peringatan"], ""]
    bulan_ini = None
    for e in acara:
        kunci = (e["tanggal"].year, e["tanggal"].month)
        if kunci != bulan_ini:
            bulan_ini = kunci
            o += ["", "### %s %d" % (BULAN[kunci[1] - 1], kunci[0])]
        tambahan = " (%s)" % ket_geser(e) if ket_geser(e) != "-" else ""
        o.append("- [ ] **%s %s** - %s%s" % (HARI[e["tanggal"].weekday()][:3], fmt_pendek(e["tanggal"]),
                                               e["judul"], tambahan))
    if not acara:
        o.append("_Tidak ada tenggat dalam rentang ini._")
    o += blok_omzet(info)
    o += ["", "Sebelum setor: siapkan angka (skill pph-final-umkm / pph21-ter / hitung-ppn bila terpasang), buat kode "
              "billing di Coretax, bayar, simpan bukti penerimaan negara (BPN/NTPN).",
          "", "_%s_" % DISCLAIMER]
    return "\n".join(o) + "\n"


def keluaran_hari_ini(acara, info, hari_ini, rentang):
    o = ["## Tenggat pajak %d hari ke depan (%s s.d. %s) - %s" % (
        rentang, fmt_panjang(hari_ini), fmt_panjang(hari_ini + dt.timedelta(days=rentang)),
        info["label_profil"]), ""]
    if info["peringatan"]:
        o += ["> **%s**" % info["peringatan"], ""]
    if not acara:
        o.append("Tidak ada tenggat dalam %d hari ke depan." % rentang)
    else:
        o.append("| Sisa | Tanggal | Kegiatan | Keterangan |")
        o.append("|---|---|---|---|")
        for e in acara:
            sisa = (e["tanggal"] - hari_ini).days
            label = "HARI INI" if sisa == 0 else ("besok" if sisa == 1 else "%d hari lagi" % sisa)
            o.append("| %s | %s | %s | %s |" % (label, fmt_panjang(e["tanggal"]), e["judul"], ket_geser(e)))
    berikut = info.get("berikutnya") or []
    if berikut:
        t = berikut[0]["tanggal"]
        o += ["", "Tenggat berikutnya sesudah rentang ini: **%s** (%d hari lagi) - %s" % (
            fmt_panjang(t), (t - hari_ini).days, "; ".join(e["judul"] for e in berikut))]
    o += blok_omzet(info)
    o += [""] + ["Data libur: %s." % info["sumber_libur"]]
    o += ["", "_%s_" % DISCLAIMER]
    return "\n".join(o) + "\n"


def keluaran_csv(acara):
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator="\n")
    w.writerow(["tanggal", "hari", "kegiatan", "jenis", "kewajiban", "pajak", "masa", "tanggal_normal",
                "keterangan_geser", "catatan"])
    for e in acara:
        w.writerow([e["tanggal"].isoformat(), HARI[e["tanggal"].weekday()], e["judul"], e["jenis"], e["kode"],
                    e["pajak"], e["masa"], e["tanggal_normal"].isoformat(),
                    ket_geser(e) if ket_geser(e) != "-" else "", e["catatan"]])
    return buf.getvalue()


def keluaran_json(acara, info):
    return json.dumps({
        "profil": info["profil"], "kewajiban": info["kewajiban"], "rentang": info["rentang"],
        "peringatan": info["peringatan"], "tanggal_cek_aturan": TANGGAL_CEK, "versi": VERSI,
        "sumber_libur": info["sumber_libur"],
        "tenggat_berikutnya": [{"tanggal": e["tanggal"].isoformat(), "kegiatan": e["judul"]}
                               for e in (info.get("berikutnya") or [])],
        "acara": [{
            "tanggal": e["tanggal"].isoformat(), "tanggal_normal": e["tanggal_normal"].isoformat(),
            "kegiatan": e["judul"], "jenis": e["jenis"], "kewajiban": e["kode"], "masa": e["masa"],
            "bergeser_karena": e["alasan_geser"], "libur_tidak_bergeser": e["libur_tetap"],
            "saran_hari_kerja_sebelumnya": e["saran_sebelum"].isoformat() if e.get("saran_sebelum") else None,
            "keterangan": ket_geser(e),
            "catatan": e["catatan"], "uid": e["uid"],
        } for e in acara],
        "omzet_lewat_500jt": ({k: v for k, v in info["omzet"].items()} if info.get("omzet") else None),
        "disclaimer": DISCLAIMER,
    }, ensure_ascii=False, indent=2) + "\n"


def ics_escape(teks):
    return (teks.replace("\\", "\\\\").replace(";", "\\;").replace(",", "\\,")
            .replace("\r\n", "\\n").replace("\n", "\\n").replace("\r", "\\n"))


def ics_lipat(baris):
    """Lipat baris > 75 oktet (RFC 5545 3.1) tanpa memotong karakter UTF-8."""
    hasil, sekarang, batas = [], "", 75
    for ch in baris:
        if len((sekarang + ch).encode("utf-8")) > batas:
            hasil.append(sekarang)
            sekarang, batas = " " + ch, 75
        else:
            sekarang += ch
    hasil.append(sekarang)
    return "\r\n".join(hasil)


def keluaran_ics(acara, info, sekarang_utc, acara_pengingat=False):
    stamp = sekarang_utc.strftime("%Y%m%dT%H%M%SZ")
    b = ["BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//Komunitech//kalender-pajak " + VERSI + "//ID",
         "CALSCALE:GREGORIAN", "METHOD:PUBLISH", "X-WR-CALNAME:" + ics_escape("Kalender Pajak - " + info["label_profil"]),
         "X-WR-TIMEZONE:Asia/Jakarta"]
    for e in acara:
        desk = "%s\nMasa: %s\n%s\n%s\nTenggat normal: %s\n\n%s" % (
            e["judul"], e["masa"], e["catatan"],
            ("Keterangan: " + ket_geser(e)) if ket_geser(e) != "-" else "Tidak bergeser.",
            fmt_panjang(e["tanggal_normal"]), DISCLAIMER)
        b += ["BEGIN:VEVENT", "UID:" + e["uid"], "DTSTAMP:" + stamp,
              "DTSTART;VALUE=DATE:" + e["tanggal"].strftime("%Y%m%d"),
              "DTEND;VALUE=DATE:" + (e["tanggal"] + dt.timedelta(days=1)).strftime("%Y%m%d"),
              "SUMMARY:" + ics_escape("Pajak: " + e["judul"]),
              "DESCRIPTION:" + ics_escape(desk),
              "CATEGORIES:" + ics_escape("Pajak"),
              "TRANSP:TRANSPARENT"]
        # Pengingat H-3 & H-1 pukul 09.00 waktu perangkat (acara sepanjang hari mulai 00.00)
        for trig, label in (("-P2DT15H", "3 hari lagi"), ("-PT15H", "besok")):
            b += ["BEGIN:VALARM", "ACTION:DISPLAY", "TRIGGER:" + trig,
                  "DESCRIPTION:" + ics_escape("%s: %s" % (label, e["judul"])), "END:VALARM"]
        b.append("END:VEVENT")
        if acara_pengingat:
            # Acara pengingat terpisah (untuk Google Calendar yang sering mengabaikan VALARM impor)
            for hari, kode in ((3, "h3"), (1, "h1")):
                t = e["tanggal"] - dt.timedelta(days=hari)
                b += ["BEGIN:VEVENT", "UID:" + uid(e["kode"], e["jenis"], e["masa"], kode), "DTSTAMP:" + stamp,
                      "DTSTART;VALUE=DATE:" + t.strftime("%Y%m%d"),
                      "DTEND;VALUE=DATE:" + (t + dt.timedelta(days=1)).strftime("%Y%m%d"),
                      "SUMMARY:" + ics_escape("Pengingat H-%d pajak: %s (tenggat %s)" % (
                          hari, e["judul"], fmt_panjang(e["tanggal"]))),
                      "DESCRIPTION:" + ics_escape("Tenggat: %s\n%s\n\n%s" % (
                          fmt_panjang(e["tanggal"]), e["judul"], DISCLAIMER)),
                      "CATEGORIES:" + ics_escape("Pajak"), "TRANSP:TRANSPARENT", "END:VEVENT"]
    b.append("END:VCALENDAR")
    return "\r\n".join(ics_lipat(x) for x in b) + "\r\n"


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def daftar_profil():
    o = ["Profil (boleh digabung dengan koma, mis. badan-pkp,pemberi-kerja,pemotong):"]
    for k, (kw, ket) in PROFIL.items():
        o.append("  %-14s %s  -> %s" % (k, ket, ", ".join(kw)))
    o.append("Kewajiban tunggal juga boleh dipakai langsung: " + ", ".join(SEMUA_KEWAJIBAN))
    return "\n".join(o) + "\n"


class Parser(argparse.ArgumentParser):
    def error(self, message):
        raise InputSalah("argumen tidak valid: %s. Lihat --help." % message)


def angka(teks, nama, bawah, atas):
    try:
        n = int(str(teks).strip())
    except ValueError:
        raise InputSalah("%s harus angka bulat, bukan '%s'" % (nama, teks))
    if not bawah <= n <= atas:
        raise InputSalah("%s harus %d-%d (sekarang %d)" % (nama, bawah, atas, n))
    return n


def nama_bulan(teks):
    """Terima 10, 'Okt', 'oktober', 'Oct'."""
    t = str(teks).strip().lower()
    for i, (panjang, pendek) in enumerate(zip(BULAN, BLN), start=1):
        if t in (panjang.lower(), pendek.lower()) or (len(t) >= 3 and panjang.lower().startswith(t)):
            return i
    lain = {"may": 5, "aug": 8, "oct": 10, "dec": 12, "agt": 8, "ags": 8}
    return lain.get(t, teks)


def jalankan(argv, sekarang_utc=None):
    p = Parser(description="Kalender tenggat setor & lapor pajak Indonesia (PMK 81/2024).")
    p.add_argument("--profil", action="append", default=[],
                   help="profil/kewajiban, dipisah koma. Lihat --daftar-profil")
    p.add_argument("--tahun", help="tahun awal kalender (default: tahun ini)")
    p.add_argument("--bulan-mulai", default="1", help="bulan awal kalender 1-12 (default 1)")
    p.add_argument("--jumlah-bulan", default="12", help="panjang kalender 1-24 bulan (default 12)")
    p.add_argument("--hari-ini", help="YYYY-MM-DD: tampilkan tenggat N hari ke depan dari tanggal ini "
                                      "('hari-ini' = tanggal komputer)")
    p.add_argument("--rentang", default="14", help="N hari untuk --hari-ini (1-90, default 14)")
    p.add_argument("--format", default="md", help="md | checklist | csv | ics | json")
    p.add_argument("--keluar", help="simpan ke file ini (disarankan untuk ics)")
    p.add_argument("--libur", action="append", default=[], help="file CSV libur tambahan (kolom tanggal,jenis,keterangan)")
    p.add_argument("--acara-pengingat", action="store_true",
                   help="khusus --format ics: tambah acara pengingat terpisah H-3 & H-1 (untuk Google Calendar)")
    p.add_argument("--daftar-profil", action="store_true", help="tampilkan daftar profil lalu keluar")
    g = p.add_mutually_exclusive_group()
    g.add_argument("--omzet-bulanan", help="omzet per bulan mulai Januari, dipisah koma/titik koma/spasi "
                                           "(mis. '48jt;45jt;52jt'): hitung bulan omzet kumulatif melewati Rp500 juta")
    g.add_argument("--omzet-setahun", help="perkiraan omzet setahun (mis. 600jt), dianggap merata per bulan")
    a = p.parse_args(argv)

    if a.daftar_profil:
        return daftar_profil().encode("utf-8"), None

    fmt = a.format.strip().lower()
    if fmt not in ("md", "checklist", "csv", "ics", "json"):
        raise InputSalah("format '%s' tidak dikenal; pilih md, checklist, csv, ics, atau json" % a.format)
    if a.acara_pengingat and fmt != "ics":
        raise InputSalah("--acara-pengingat hanya untuk --format ics")
    profil, kewajiban = urai_profil(a.profil)
    tahun_pengguna = set()
    libur, tahun_ada = muat_libur(a.libur, tahun_pengguna)
    sekarang_utc = sekarang_utc or dt.datetime.now(dt.timezone.utc)

    if a.hari_ini:
        if a.hari_ini.strip().lower() in ("hari-ini", "sekarang", "today"):
            hari_ini = dt.date.today()
        else:
            try:
                hari_ini = dt.date.fromisoformat(a.hari_ini.strip())
            except ValueError:
                raise InputSalah("--hari-ini harus tanggal YYYY-MM-DD (mis. 2026-09-25), bukan '%s'" % a.hari_ini)
        if not TAHUN_MIN <= hari_ini.year <= TAHUN_MAKS:
            raise InputSalah("tahun harus %d-%d" % (TAHUN_MIN, TAHUN_MAKS))
        rentang = angka(a.rentang, "--rentang", 1, 90)
        awal, akhir = hari_ini, hari_ini + dt.timedelta(days=rentang)
        judul = "%s s.d. %s" % (awal.isoformat(), akhir.isoformat())
    else:
        tahun = angka(a.tahun or dt.date.today().year, "--tahun", TAHUN_MIN, TAHUN_MAKS)
        bm = angka(nama_bulan(a.bulan_mulai), "--bulan-mulai", 1, 12)
        jb = angka(a.jumlah_bulan, "--jumlah-bulan", 1, 24)
        awal = dt.date(tahun, bm, 1)
        ath, abl = bulan_berikut(tahun, bm, jb - 1)
        akhir = tgl_aturan(ath, abl, "akhir")
        judul = ("%s %d" % (BULAN[bm - 1], tahun)) if jb == 1 else "%s %d - %s %d" % (
            BULAN[bm - 1], tahun, BULAN[abl - 1], ath)

    acara, kurang = buat_acara(kewajiban, awal, akhir, libur, tahun_ada)
    omzet = None
    if a.omzet_bulanan or a.omzet_setahun:
        if "pph-final-umkm" not in kewajiban or "badan-umkm" in profil:
            raise InputSalah("--omzet-bulanan/--omzet-setahun hanya untuk orang pribadi PPh final 0,5% "
                             "(profil op-umkm); badan tidak mendapat pembebasan Rp500 juta")
        th_omzet = awal.year
        if a.omzet_setahun:
            setahun = rupiah(a.omzet_setahun, "--omzet-setahun")
            if setahun % 12:
                per = [setahun // 12 + (1 if i < setahun % 12 else 0) for i in range(12)]
            else:
                per = [setahun // 12] * 12
            sumber = "perkiraan %s setahun dibagi rata 12 bulan = %s/bulan%s" % (
                fmt_rp(setahun), fmt_rp(setahun // 12), "" if setahun % 12 == 0 else " (sisa pembagian dibagi ke bulan awal)")
        else:
            # pemisah: ; spasi ", " atau koma di antara dua nilai bersatuan (48jt,45jt). "1,2jt" = desimal.
            bag = [x for x in re.split(r"[;\s]+|,(?=\s)|(?<=[a-z]),(?=\d)", a.omzet_bulanan.strip().lower()) if x]
            if not 1 <= len(bag) <= 12:
                raise InputSalah("--omzet-bulanan harus berisi 1-12 nilai (Januari dst.), sekarang %d" % len(bag))
            per = [rupiah(x, "omzet %s" % BULAN[i]) for i, x in enumerate(bag)]
            sumber = "omzet per bulan dari pengguna"
        omzet = hitung_lewat_batas(th_omzet, per, sumber, libur, tahun_ada, kurang)
    berikutnya = []
    if a.hari_ini:
        # tenggat terdekat sesudah rentang (cari sampai 400 hari; tanpa memengaruhi peringatan)
        lanjut, _ = buat_acara(kewajiban, akhir + dt.timedelta(days=1), akhir + dt.timedelta(days=400),
                               libur, tahun_ada)
        if lanjut:
            berikutnya = [e for e in lanjut if e["tanggal"] == lanjut[0]["tanggal"]]
    lth, lbl = akhir.year, akhir.month
    if akhir != tgl_aturan(lth, lbl, "akhir"):
        lth, lbl = bulan_berikut(lth, lbl, -1)
    cakupan_lanjut = "Tenggat masa pajak %s %d dan sesudahnya jatuh setelah periode ini" % (BULAN[lbl - 1], lth)
    if any(k in kewajiban for k in ("spt-op", "spt-badan", "bukti-a1")):
        cakupan_lanjut += "; begitu juga kewajiban tahunan untuk tahun pajak %d" % akhir.year
    cakupan_lanjut += " - buat kalender periode berikutnya untuk melihatnya."
    sumber_libur = ("SKB 3 Menteri libur nasional & cuti bersama " + ", ".join(
        str(t) for t in sorted(tahun_ada)) if tahun_ada else "data resmi belum ada")
    sumber_libur += " (file: %s)" % (", ".join(f.name for f in sorted(REF.glob("libur-nasional-*.csv"))) or "-")
    if a.libur:
        sumber_libur += "; data libur dari pengguna, belum diverifikasi (file: %s)" % ", ".join(
            Path(x).name for x in a.libur)
    # tahun rentang yang tidak punya data juga diperingatkan walau tidak ada acara di sana
    for th in range(awal.year, akhir.year + 1):
        if th not in tahun_ada:
            kurang.add(th)
    info = {
        "profil": profil, "kewajiban": kewajiban, "rentang": [awal.isoformat(), akhir.isoformat()],
        "judul_rentang": judul, "label_profil": ", ".join(profil),
        "kewajiban_nama": [(KEWAJIBAN_MASA.get(k) or KEWAJIBAN_TAHUNAN[k])["pajak"] for k in kewajiban],
        "peringatan": pesan_kurang(kurang, tahun_ada, tahun_pengguna),
        "awal": awal, "akhir": akhir, "cakupan_lanjut": cakupan_lanjut, "sumber_libur": sumber_libur,
        "berikutnya": berikutnya, "omzet": omzet,
    }
    if a.hari_ini and fmt == "md":
        teks = keluaran_hari_ini(acara, info, awal, (akhir - awal).days)
    elif fmt == "md":
        teks = keluaran_md(acara, info)
    elif fmt == "checklist":
        teks = keluaran_checklist(acara, info)
    elif fmt == "csv":
        teks = keluaran_csv(acara)
    elif fmt == "json":
        teks = keluaran_json(acara, info)
    else:
        teks = keluaran_ics(acara, info, sekarang_utc, a.acara_pengingat)
    data = teks.encode("utf-8")
    if a.keluar:
        try:
            Path(a.keluar).write_bytes(data)
        except OSError as e:
            raise InputSalah("tidak bisa menulis '%s': %s" % (a.keluar, e.strerror or e))
        pesan = "Tersimpan: %s (%d tenggat)" % (a.keluar, len(acara))
        if fmt == "ics":
            pesan += "\n" + (CATATAN_ICS if not a.acara_pengingat else CATATAN_ICS_PENGINGAT)
        if info["peringatan"]:
            pesan += "\n" + info["peringatan"]
        return (pesan + "\n").encode("utf-8"), None
    peringatan = info["peringatan"] if fmt in ("csv", "ics") else None
    if fmt == "ics":
        peringatan = "\n".join(x for x in (peringatan, CATATAN_ICS_PENGINGAT if a.acara_pengingat
                                            else CATATAN_ICS) if x)
    return data, peringatan


def main(argv=None):
    try:
        data, peringatan = jalankan(sys.argv[1:] if argv is None else argv)
    except InputSalah as e:
        sys.stderr.write("ERROR: %s\n" % e)
        return 2
    except KeyboardInterrupt:
        return 130
    if peringatan:
        sys.stderr.write(peringatan + "\n")
    out = getattr(sys.stdout, "buffer", None)
    if out is not None:
        out.write(data)
        out.flush()
    else:
        sys.stdout.write(data.decode("utf-8"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
