#!/usr/bin/env python3
"""Buat kerangka kalender konten (default 30 hari) dengan tanggal, hari, momen lokal, pilar, dan
platform yang sudah benar. Kolom ide/hook/CTA dikosongkan untuk diisi AI agent.

Yang dilakukan script (supaya tanggal & rotasi tidak salah):
- Nama hari dalam Bahasa Indonesia untuk setiap tanggal.
- Menandai momen tanggal tetap (HUT RI, Hari Batik, Sumpah Pemuda, Hari Ibu, dll.), tanggal kembar
  (1.1 s.d. 12.12; 12.12 = Harbolnas), hari gajian, dan "tanggal tua".
- Momen yang tanggalnya berubah tiap tahun TIDAK ditebak: Ramadan, Idulfitri, dan Imlek diambil dari tabel
  PERKIRAAN di bawah (sama dengan references/momen-dan-pilar.md) dan selalu berlabel "perkiraan"; bila pengguna
  memberi tanggal, pakai --awal-ramadan / --idulfitri / --imlek. Bila rentang mencakup Ramadan, tiap hari diberi
  "Ramadan hari ke-N", plus Nuzulul Qur'an, 10 malam terakhir, batas THR (±H-7), H-1, Idulfitri & H+1.
  Momen lain (Idul Adha, Waisak, dll.) masukkan lewat --momen "YYYY-MM-DD:Nama".
- --cek-teks: cek-silang teks jawaban (tips/catatan/tabel yang ditempel) — tanggal hari besar yang disebut
  harus sama dengan tabel; periode yang mencakup Ramadan wajib menyebut Ramadan; dengan --fakta, klaim
  layanan/produk yang tidak disebut pengguna ditandai GAGAL (memakai cek_fakta.py).
- Rotasi pilar konten; hari promo (tanggal kembar, gajian, momen bertipe promo) dipaksa ke pilar promo,
  hari peringatan (mis. 30 Sep, 1 Okt, 10 Nov) tidak pernah diberi pilar promo.

Hanya library standar Python 3.8+. Contoh:
  python3 buat_kalender.py --mulai 2026-10-01 --pilar "Edukasi,Promo,Di Balik Layar,Testimoni,Hiburan" \
      --platform "IG,TikTok,WA Status" --momen "2026-10-17:Ulang tahun toko ke-3" --format csv --pemisah ";"
"""
import argparse
import csv
import io
import json
import os
import re
import sys
from datetime import date, datetime, timedelta

# Windows: pastikan teks Indonesia/emoji tercetak tanpa error encoding
for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass

HARI = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"]
BULAN = ["", "Jan", "Feb", "Mar", "Apr", "Mei", "Jun", "Jul", "Agu", "Sep", "Okt", "Nov", "Des"]

# (bulan, tanggal): (nama, tipe). tipe: promo | tema | peringatan
MOMEN_TETAP = {
    (1, 1): ("Tahun Baru", "tema"),
    (2, 14): ("Hari Valentine", "tema"),
    (3, 8): ("Hari Perempuan Internasional", "tema"),
    (4, 21): ("Hari Kartini", "tema"),
    (5, 1): ("Hari Buruh", "tema"),
    (5, 2): ("Hari Pendidikan Nasional", "tema"),
    (6, 1): ("Hari Lahir Pancasila", "tema"),
    (7, 23): ("Hari Anak Nasional", "tema"),
    (8, 17): ("HUT Kemerdekaan RI", "tema"),
    (9, 4): ("Hari Pelanggan Nasional", "tema"),
    (9, 30): ("Peringatan G30S", "peringatan"),
    (10, 1): ("Hari Kesaktian Pancasila", "peringatan"),
    (10, 2): ("Hari Batik Nasional", "tema"),
    (10, 22): ("Hari Santri", "tema"),
    (10, 28): ("Hari Sumpah Pemuda", "tema"),
    (11, 10): ("Hari Pahlawan", "peringatan"),
    (11, 25): ("Hari Guru Nasional", "tema"),
    (12, 22): ("Hari Ibu", "tema"),
    (12, 25): ("Hari Natal", "tema"),
    (12, 31): ("Malam Tahun Baru", "tema"),
}
FORMAT_PILAR = [
    ("promo", "Video pendek + Story/Status"),
    ("jual", "Video pendek + Story/Status"),
    ("edukasi", "Carousel / video tips"),
    ("tips", "Carousel / video tips"),
    ("testimoni", "Foto ulasan / Story"),
    ("bukti", "Foto ulasan / Story"),
    ("balik", "Video pendek proses"),
    ("proses", "Video pendek proses"),
    ("ulasan", "Foto ulasan / Story"),
    ("review", "Foto ulasan / Story"),
    ("resep", "Carousel / video tips"),
    ("koleksi", "Foto/video produk"),
    ("ootd", "Video try-on / mix-match"),
    ("bts", "Video pendek proses"),
    ("hiburan", "Video tren / polling"),
    ("interaksi", "Polling / kuis Story"),
]
# Perkiraan hari besar yang tanggalnya berubah tiap tahun — HARUS SAMA dengan tabel di
# references/momen-dan-pilar.md (diuji di uji_regresi.py). BELUM TERVERIFIKASI, bisa bergeser ±1 hari.
PERKIRAAN = {
    "imlek": {2027: date(2027, 2, 6)},
    "awal_ramadan": {2027: date(2027, 2, 8), 2028: date(2028, 1, 28)},
    "idulfitri": {2027: date(2027, 3, 10)},
}
TAHUN_HIJRIAH = {2027: 1448, 2028: 1449}
LABEL_PERKIRAAN = "perkiraan, menunggu sidang isbat / cek SKB 3 Menteri"
# Kata kunci per jenis hari besar (untuk mengenali momen pengguna & cek teks)
KUNCI_HARI_BESAR = {
    "idulfitri": r"idul\s*fitri|lebaran|hari\s+raya\s+idul|1\s+syawal",
    "awal_ramadan": r"awal\s+(?:ramadan|ramadhan|puasa)|1\s+rama[dh]+an|mulai\s+puasa|puasa\s+pertama",
    "imlek": r"imlek",
    "nuzulul": r"nuzulul",
}
# Untuk cek teks: "Idulfitri/1 Syawal" harus tepat di hari H; "Lebaran" boleh H-1 s.d. H+1.
KUNCI_CEK = {
    "idulfitri": r"idul\s*fitri|1\s+syawal|hari\s+raya\s+idul",
    "lebaran": r"lebaran",
    "awal_ramadan": KUNCI_HARI_BESAR["awal_ramadan"],
    "imlek": r"imlek",
    "nuzulul": r"nuzulul",
}
KOLOM = ["No", "Tanggal", "Hari", "Momen", "Pilar", "Platform", "Format", "Ide Konten", "Hook / Judul",
         "CTA", "Status"]


def galat(pesan):
    print("ERROR: " + pesan, file=sys.stderr)
    sys.exit(1)


def parse_tanggal(teks, nama="Tanggal"):
    t = teks.strip()
    for fmt in ("%Y-%m-%d", "%d-%m-%Y", "%d/%m/%Y", "%Y/%m/%d"):
        try:
            return datetime.strptime(t, fmt).date()
        except ValueError:
            pass
    galat("{} '{}' tidak dikenali. Pakai format YYYY-MM-DD, mis. 2026-10-01.".format(nama, teks))


def fmt_tgl(d):
    return "{:02d} {} {}".format(d.day, BULAN[d.month], d.year)


def default_mulai(hari_ini):
    return date(hari_ini.year + (hari_ini.month == 12), hari_ini.month % 12 + 1, 1)


def format_untuk(pilar):
    p = pilar.lower()
    for kunci, fmt in FORMAT_PILAR:
        if kunci in p:
            return fmt
    return "Bebas (sesuaikan ide)"


POLA_RELATIF = re.compile(r"(?:pasca|setelah|jelang|menjelang|H\s*[-+]\s*\d+)[\s-]*(?:lebaran|idul\s*fitri)"
                          r"|(?:lebaran|idul\s*fitri)\s+H\s*[-+]\s*\d+", re.IGNORECASE)


def jenis_hari_besar(nama):
    """Jenis hari besar yang DIMAKSUD nama momen ("Pasca-Lebaran H+3"/"H-7 Lebaran" bukan hari Lebaran)."""
    nama = POLA_RELATIF.sub(" ", nama)
    for jenis, pola in KUNCI_HARI_BESAR.items():
        if re.search(pola, nama, re.IGNORECASE):
            return jenis
    return None


def hitung_perkiraan(mulai, akhir, override, momen_user):
    """Kembalikan (momen per tanggal, tanggal kunci). override: {jenis: date} dari pengguna.
    Momen pengguna (--momen) yang namanya menyebut Idulfitri/awal Ramadan/Imlek dianggap tanggal dari pengguna."""
    override = dict(override)
    for d, daftar in momen_user.items():
        for nama, _ in daftar:
            j = jenis_hari_besar(nama)
            if j in ("idulfitri", "awal_ramadan", "imlek") and j not in override:
                override[j] = d
    momen, kunci = {}, {"idulfitri": set(), "lebaran": set(), "awal_ramadan": set(), "imlek": set(), "nuzulul": set(),
                        "ramadan": set()}

    def tambah(d, nama, tipe="tema"):
        if mulai - timedelta(days=60) <= d <= akhir + timedelta(days=60):
            momen.setdefault(d, []).append((nama, tipe))

    for th in range(mulai.year - 1, akhir.year + 2):
        sumber = {}
        for jenis in ("awal_ramadan", "idulfitri", "imlek"):
            o = override.get(jenis)
            if o is not None and abs(o.year - th) == 0:
                sumber[jenis] = (o, "dari pengguna")
            elif PERKIRAAN[jenis].get(th) and not (o is not None and abs((o - PERKIRAAN[jenis][th]).days) < 200):
                sumber[jenis] = (PERKIRAAN[jenis][th], LABEL_PERKIRAAN)
        hijriah = TAHUN_HIJRIAH.get(th)
        teks_h = " {} H".format(hijriah) if hijriah else ""
        if "imlek" in sumber:
            d, lbl = sumber["imlek"]
            kunci["imlek"].add(d)
            if not _ada_momen_user(momen_user, d, "imlek"):
                tambah(d, "Imlek ({})".format(lbl))
        if "awal_ramadan" in sumber:
            awal, lbl = sumber["awal_ramadan"]
            idul = sumber.get("idulfitri", (None, None))[0]
            if idul is not None and not 29 <= (idul - awal).days <= 30:
                idul = None  # tidak konsisten (Ramadan 29–30 hari) -> jangan dipakai berpasangan
            panjang = (idul - awal).days if idul else 29
            kunci["awal_ramadan"].add(awal)
            kunci["nuzulul"].add(awal + timedelta(days=16))
            for n in range(1, panjang + 1):
                d = awal + timedelta(days=n - 1)
                kunci["ramadan"].add(d)
                nama = "Ramadan hari ke-{} ({})".format(n, lbl)
                if n == 1:
                    nama = "Awal Ramadan{} — ".format(teks_h) + nama
                    if _ada_momen_user(momen_user, d, "awal_ramadan"):
                        nama = "Ramadan hari ke-1"
                if n == 17:
                    nama += "; Nuzulul Qur'an (±17 Ramadan)"
                if n == 21:
                    nama += "; awal 10 malam terakhir Ramadan"
                tambah(d, nama)
        if "idulfitri" in sumber:
            idul, lbl = sumber["idulfitri"]
            kunci["idulfitri"].add(idul)
            kunci["lebaran"].update({idul - timedelta(days=1), idul, idul + timedelta(days=1)})
            tambah(idul - timedelta(days=7), "Batas THR cair ±H-7 Lebaran (cek aturan Kemnaker)", "promo")
            tambah(idul - timedelta(days=1), "H-1 Lebaran / malam takbiran ({})".format(lbl))
            if not _ada_momen_user(momen_user, idul, "idulfitri"):
                tambah(idul, "Idulfitri{} ({}) — ucapan, tanpa hard-selling".format(teks_h, lbl), "peringatan")
            tambah(idul + timedelta(days=1), "Lebaran H+1 ({}) — ucapan, tanpa hard-selling".format(lbl), "peringatan")
            for n in range(2, 15):
                tambah(idul + timedelta(days=n), "Pasca-Lebaran H+{} ({}) — info toko buka/jadwal kirim, halal bihalal"
                       .format(n, "perkiraan" if lbl == LABEL_PERKIRAAN else lbl))
    return momen, kunci


def _ada_momen_user(momen_user, d, jenis):
    return any(jenis_hari_besar(n) == jenis for n, _ in momen_user.get(d, []))


SUFIKS_PERINGATAN = " — hari peringatan/hari raya: konten ucapan/penghormatan, hindari hard-selling"


def momen_hari(d, gajian, momen_user):
    """Kembalikan list (nama, tipe) untuk tanggal d."""
    daftar = []
    for nama, tipe in momen_user.get(d, []):
        daftar.append((nama, tipe))
    if (d.month, d.day) in MOMEN_TETAP:
        daftar.append(MOMEN_TETAP[(d.month, d.day)])
    if d.day == d.month:
        if d.month == 12:
            daftar.append(("Harbolnas 12.12 (cek jadwal resmi)", "promo"))
        elif d.month >= 9:
            daftar.append(("Tanggal kembar {0}.{0} — musim promo akhir tahun (cek kampanye marketplace)".format(d.month), "promo"))
        else:
            daftar.append(("Tanggal kembar {0}.{0} (cek kampanye marketplace)".format(d.month), "promo"))
    akhir_bulan = (d + timedelta(days=1)).month != d.month
    for g in gajian:
        if d.day == g or (akhir_bulan and g > d.day):
            daftar.append(("Hari gajian (tgl {})".format(g if g <= d.day else "akhir bulan"), "promo"))
            break
    if not daftar and 20 <= d.day <= 24 and 25 in gajian:
        daftar.append(("Tanggal tua — konten hemat/nilai", "tema"))
    return daftar


def susun(mulai, jumlah, pilar, platform, gajian, momen_user):
    idx_promo = next((i for i, p in enumerate(pilar) if "promo" in p.lower() or "jual" in p.lower()), None)
    hari = [mulai + timedelta(days=i) for i in range(jumlah)]
    info = [momen_hari(d, gajian, momen_user) for d in hari]
    paksa_promo = [any(t == "promo" for _, t in m) for m in info]
    larang_promo = [any(t == "peringatan" for _, t in m) for m in info]
    tanggal_tua = [any(n.startswith("Tanggal tua") for n, _ in m) for m in info]
    bentrok = []
    for i, d in enumerate(hari):
        if paksa_promo[i] and larang_promo[i]:
            promo = [n for n, t in info[i] if t == "promo" and not n.startswith("Hari gajian")]
            if promo:
                bentrok.append("Momen promo '{}' pada {} bertepatan dengan hari peringatan ({}); TIDAK dijadwalkan "
                               "sebagai promo — geser tanggalnya.".format(
                                   "; ".join(promo), fmt_tgl(d), "; ".join(n for n, t in info[i] if t == "peringatan")))

    baris, putar = [], 0
    for i, d in enumerate(hari):
        if paksa_promo[i] and not larang_promo[i] and idx_promo is not None:
            p = pilar[idx_promo]
        else:
            p = None
            for _ in range(len(pilar)):
                kandidat = pilar[putar % len(pilar)]
                putar += 1
                dekat_promo = any(paksa_promo[j] for j in (i - 1, i + 1) if 0 <= j < len(hari))
                if idx_promo is not None and kandidat == pilar[idx_promo] and (
                        larang_promo[i] or dekat_promo or tanggal_tua[i]):
                    continue
                p = kandidat
                break
            if p is None:
                p = next((x for j, x in enumerate(pilar) if j != idx_promo), pilar[0])
        catatan = "; ".join(n for n, _ in info[i])
        if larang_promo[i]:
            catatan += SUFIKS_PERINGATAN
        baris.append({
            "No": i + 1, "Tanggal": d.isoformat(), "Tanggal_tampil": fmt_tgl(d), "Hari": HARI[d.weekday()],
            "Momen": catatan, "Pilar": p, "Platform": " + ".join(platform), "Format": format_untuk(p),
            "Ide Konten": "", "Hook / Judul": "", "CTA": "", "Status": "Belum",
        })
    return baris, bentrok


KATA_PROMO = re.compile(r"\b(?:promo|diskon|sale|potongan|gratis|cashback|flash|voucher|beli\s*\d+|harga\s+spesial)\b",
                        re.IGNORECASE)


def periksa_isi(baris, gajian, momen_user):
    """Hitung ulang momen per tanggal pada hasil isian dan peringatkan promo di hari yang tidak pantas."""
    pesan = []
    for r in baris:
        d = parse_tanggal(r["Tanggal"])
        info = momen_hari(d, gajian, momen_user)
        peringatan = [n for n, t in info if t == "peringatan"]
        hitungan = "; ".join(n for n, _ in info) + (SUFIKS_PERINGATAN if peringatan else "")
        momen_isi = r["Momen"]
        if not momen_isi.strip():
            r["Momen"] = hitungan
        else:
            alasan = []
            for n, _ in info:
                j = jenis_hari_besar(n) or ("ramadan" if re.search(r"ramadan", n, re.IGNORECASE) else None)
                pola = r"ramadan|ramadhan|puasa" if j == "ramadan" else (KUNCI_HARI_BESAR.get(j) if j else None)
                if pola and not re.search(pola, momen_isi, re.IGNORECASE):
                    alasan.append("momen '{}' dari tabel hilang".format(n.split(" (")[0]))
            if re.search(r"tanggal\s+tua", momen_isi, re.IGNORECASE) and not any(
                    n.startswith("Tanggal tua") for n, _ in info):
                alasan.append("'Tanggal tua' tidak berlaku di tanggal ini")
            for j in ("idulfitri", "awal_ramadan", "imlek"):
                if re.search(KUNCI_HARI_BESAR[j], POLA_RELATIF.sub(" ", momen_isi), re.IGNORECASE) \
                        and not any(jenis_hari_besar(n) == j for n, _ in info):
                    alasan.append("menyebut {} padahal tabel tidak menaruhnya di tanggal ini".format(j.replace("_", " ")))
            if alasan:
                r["Momen"] = hitungan
                pesan.append("Baris {} ({}): kolom Momen diganti dengan hasil script ({}). Sesuaikan ide/hook baris "
                             "ini.".format(r["No"], r["Tanggal_tampil"], "; ".join(alasan)))
        teks = " ".join([r["Pilar"], r["Ide Konten"], r["Hook / Judul"], r["CTA"]])
        berbau_promo = bool(re.search(r"promo|jual", r["Pilar"], re.IGNORECASE)) or bool(KATA_PROMO.search(teks))
        if peringatan and berbau_promo:
            pesan.append("Baris {} ({}) adalah hari peringatan ({}) tetapi berisi promo/jualan — ganti dengan konten "
                         "penghormatan/edukasi.".format(r["No"], r["Tanggal_tampil"], "; ".join(peringatan)))
        elif any(n.startswith("Tanggal tua") for n, _ in info) and re.search(r"promo|jual", r["Pilar"], re.IGNORECASE):
            pesan.append("Baris {} ({}) jatuh di tanggal tua tetapi berpilar promo — sebaiknya konten nilai/hemat.".format(
                r["No"], r["Tanggal_tampil"]))
    return pesan


POLA_TGL = re.compile(r"(?P<d1>\d{1,2})(?:\s*[-–/]\s*(?P<d2>\d{1,2}))?\s+(?P<bln>jan(?:uari)?|feb(?:ruari)?|mar(?:et)?"
                      r"|apr(?:il)?|mei|jun(?:i)?|jul(?:i)?|agu(?:stus)?|agt|sep(?:t(?:ember)?)?|okt(?:ober)?"
                      r"|nov(?:ember)?|des(?:ember)?)\b\.?(?:\s+(?P<th>20\d\d))?", re.IGNORECASE)
BULAN_KE = {"jan": 1, "feb": 2, "mar": 3, "apr": 4, "mei": 5, "jun": 6, "jul": 7, "agu": 8, "agt": 8, "sep": 9,
            "okt": 10, "nov": 11, "des": 12}
PENGHALANG = re.compile(r"\||sebelum|sampai|hingga|batas|s\.?\s?d\.?|s/d|H\s*[-+]\s*\d|pasca|setelah|order|kirim"
                        r"|pre-?order|jelang|thr|nuzulul|imlek|ramadan hari", re.IGNORECASE)


def _tanggal_token(m, mulai, akhir):
    bln = BULAN_KE[m.group("bln").lower()[:3]]
    tengah = mulai + (akhir - mulai) / 2
    hasil = []
    for hari in filter(None, (m.group("d1"), m.group("d2"))):
        calon = []
        tahun = [int(m.group("th"))] if m.group("th") else [mulai.year - 1, mulai.year, mulai.year + 1]
        for th in tahun:
            try:
                calon.append(date(th, bln, int(hari)))
            except ValueError:
                pass
        if calon:
            hasil.append(min(calon, key=lambda x: abs((x - tengah).days)))
    return hasil


def cek_teks(teks, kunci, mulai, akhir):
    """Cek-silang tanggal hari besar di teks jawaban terhadap tabel perkiraan/pengguna."""
    temuan = []
    nama_jenis = {"idulfitri": "Idulfitri", "lebaran": "Lebaran", "awal_ramadan": "awal Ramadan", "imlek": "Imlek",
                  "nuzulul": "Nuzulul Qur'an"}
    for baris in teks.splitlines():
        tokens = list(POLA_TGL.finditer(baris))
        if not tokens:
            continue
        kw = [(jenis, km) for jenis, pola in KUNCI_CEK.items() for km in re.finditer(pola, baris, re.IGNORECASE)]
        for tm in tokens:
            calon = []
            for jenis, km in kw:
                if km.end() <= tm.start():      # "Idulfitri ±10 Mar"
                    celah = baris[km.end():tm.start()]
                    if len(celah) > 25 or PENGHALANG.search(celah) or POLA_TGL.search(celah) or "," in celah:
                        continue
                elif tm.end() <= km.start():    # "10 Mar (Idulfitri)" — hanya bila menempel langsung
                    celah = baris[tm.end():km.start()]
                    if not re.fullmatch(r"\s*(?:\d{4})?\s*[(\[:—–-]?\s*[*_]*\s*", celah):
                        continue
                else:
                    continue
                calon.append((len(celah), jenis))
            if not calon:
                continue
            jenis = min(calon)[1]
            boleh = kunci.get(jenis) or set()
            tgl = _tanggal_token(tm, mulai, akhir)
            if not boleh:
                if any(mulai - timedelta(days=45) <= x <= akhir + timedelta(days=45) for x in tgl):
                    temuan.append("CEK: '{}' menyebut tanggal {} — tidak ada di tabel perkiraan; pastikan dari "
                                  "pengguna, atau tulis [isi: tanggal].".format(tm.group(0).strip(), nama_jenis[jenis]))
                continue
            if len(tgl) == 2 and tgl[0] < tgl[1]:   # rentang "10–11 Mar (Idulfitri)": harus memuat hari H
                rentang = {tgl[0] + timedelta(days=i) for i in range((tgl[1] - tgl[0]).days + 1)}
                longgar = boleh | (kunci.get("lebaran") or set() if jenis == "idulfitri" else set())
                benar = bool(rentang & boleh) and rentang <= longgar
            else:
                benar = all(x in boleh for x in tgl)
            if not benar:
                acuan = ", ".join(fmt_tgl(x) for x in sorted(boleh)
                                  if mulai - timedelta(days=90) <= x <= akhir + timedelta(days=90)) or "-"
                temuan.append("GAGAL: '{}' disebut sebagai {} ('{}'), padahal tabel: {}. Samakan dengan tabel "
                              "kalender (jangan memakai nomor baris sebagai tanggal).".format(
                                  tm.group(0).strip(), nama_jenis[jenis], baris.strip()[:80], acuan))
    ramadan = kunci.get("ramadan") or set()
    if any(mulai <= d <= akhir for d in ramadan) and not re.search(r"ramadan|ramadhan|puasa", teks, re.IGNORECASE):
        temuan.append("GAGAL: periode {} s.d. {} mencakup Ramadan (perkiraan) tetapi teks tidak menyebut Ramadan sama "
                      "sekali. Momen Ramadan tidak boleh hilang atau diganti.".format(fmt_tgl(mulai), fmt_tgl(akhir)))
    return list(dict.fromkeys(temuan))


def cek_fakta_teks(teks, fakta):
    """Pakai cek_fakta.py (folder yang sama) untuk klaim yang dikarang. Jam diabaikan (jam posting = saran umum)."""
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import cek_fakta  # noqa: E402
    return ["{}: [fakta] {}".format(t["level"], t["pesan"]) for t in cek_fakta.periksa(teks, fakta, {"jam"})]


def baca_teks(path):
    try:
        with open(path, encoding="utf-8-sig") as f:
            return f.read()
    except FileNotFoundError:
        galat("File tidak ditemukan: {}".format(path))
    except (UnicodeDecodeError, OSError) as e:
        galat("File {} tidak bisa dibaca sebagai teks UTF-8: {}".format(path, e))


def baca_isi(path):
    """Baca baris kalender yang sudah diisi. Hari dihitung ulang dari tanggal agar tidak salah."""
    try:
        with open(path, encoding="utf-8-sig") as f:
            data = json.load(f)
    except FileNotFoundError:
        galat("File tidak ditemukan: {}".format(path))
    except (ValueError, UnicodeDecodeError) as e:
        galat("File {} bukan JSON yang valid: {}".format(path, e))
    baris = data.get("baris") if isinstance(data, dict) else data
    if not isinstance(baris, list) or not baris:
        galat("JSON harus berisi daftar baris (kunci \"baris\") yang tidak kosong.")
    hasil = []
    for i, b in enumerate(baris, start=1):
        if not isinstance(b, dict) or not b.get("Tanggal"):
            galat("Baris ke-{} tidak punya kolom 'Tanggal'.".format(i))
        d = parse_tanggal(str(b["Tanggal"]), "Tanggal baris ke-{}".format(i))
        r = {k: ("" if b.get(k) is None else str(b.get(k))) for k in KOLOM}
        r["No"] = i
        r["Tanggal"] = d.isoformat()
        r["Tanggal_tampil"] = fmt_tgl(d)
        r["Hari"] = HARI[d.weekday()]
        r["Pilar"] = r["Pilar"] or "-"
        r["Status"] = r["Status"] or "Belum"
        hasil.append(r)
    kosong = [str(r["No"]) for r in hasil if not r["Ide Konten"].strip()]
    if kosong:
        print("PERINGATAN: kolom 'Ide Konten' masih kosong di baris: " + ", ".join(kosong), file=sys.stderr)
    return hasil


def main():
    p = argparse.ArgumentParser(description="Kerangka kalender konten dengan momen lokal Indonesia.")
    p.add_argument("--mulai", help="tanggal mulai YYYY-MM-DD (default: tanggal 1 bulan depan)")
    p.add_argument("--hari", type=int, default=30, help="jumlah hari (7–92), default 30")
    p.add_argument("--pilar", default="Edukasi,Promo,Di Balik Layar,Testimoni,Hiburan",
                   help="pilar konten dipisah koma (2–7)")
    p.add_argument("--platform", default="IG,TikTok,WA Status", help="platform dipisah koma")
    p.add_argument("--gajian", default="25,1", help="tanggal gajian pelanggan dipisah koma, default 25,1")
    p.add_argument("--momen", action="append", default=[],
                   help="momen tambahan \"YYYY-MM-DD:Nama\" atau \"YYYY-MM-DD:Nama:promo|tema|peringatan\". Boleh diulang")
    p.add_argument("--tanpa-momen-nasional", action="store_true", help="jangan tandai momen tanggal tetap")
    p.add_argument("--awal-ramadan", help="tanggal 1 Ramadan dari pengguna YYYY-MM-DD (default: tabel perkiraan)")
    p.add_argument("--idulfitri", help="tanggal Idulfitri dari pengguna YYYY-MM-DD (default: tabel perkiraan)")
    p.add_argument("--imlek", help="tanggal Imlek dari pengguna YYYY-MM-DD (default: tabel perkiraan)")
    p.add_argument("--tanpa-perkiraan", action="store_true", help="jangan pakai tabel perkiraan Ramadan/Idulfitri/Imlek")
    p.add_argument("--cek-teks", help="file teks jawaban (tips, catatan, tabel) untuk dicek-silang tanggal hari besar & "
                                      "fakta; pakai bersama --isi atau --mulai/--hari")
    p.add_argument("--fakta", help="salinan persis pesan pengguna, untuk cek klaim yang dikarang (cek_fakta.py)")
    p.add_argument("--fakta-file", help="file .txt berisi salinan persis pesan pengguna")
    p.add_argument("--format", choices=["md", "csv", "json"], default="md")
    p.add_argument("--pemisah", default=",", help="pemisah CSV: ',' (Google Sheets) atau ';' (Excel Indonesia)")
    p.add_argument("--output", help="simpan ke file ini (default: tampil di layar)")
    p.add_argument("--isi", help="file JSON berisi baris yang SUDAH diisi ide (hasil --format json yang dilengkapi); "
                                 "script hanya memeriksa & mengekspor ke md/csv")
    p.add_argument("--hari-ini", help=argparse.SUPPRESS)
    a = p.parse_args()

    if not 7 <= a.hari <= 92:
        galat("--hari harus antara 7 dan 92.")
    hari_ini = parse_tanggal(a.hari_ini, "--hari-ini") if a.hari_ini else date.today()
    mulai = parse_tanggal(a.mulai, "--mulai") if a.mulai else default_mulai(hari_ini)
    pilar = [x.strip() for x in a.pilar.split(",") if x.strip()]
    if not 2 <= len(pilar) <= 7:
        galat("Isi 2 sampai 7 pilar konten, dipisah koma.")
    if len(set(x.lower() for x in pilar)) != len(pilar):
        galat("Ada nama pilar yang sama. Pakai nama pilar yang berbeda.")
    platform = [x.strip() for x in a.platform.split(",") if x.strip()]
    if not platform:
        galat("Isi minimal 1 platform.")
    try:
        gajian = sorted({int(x) for x in a.gajian.split(",") if x.strip()})
    except ValueError:
        galat("--gajian harus berisi angka tanggal, mis. 25 atau 25,1.")
    if any(not 1 <= g <= 31 for g in gajian):
        galat("Tanggal gajian harus 1–31.")
    if a.pemisah not in (",", ";", "\\t", "\t"):
        galat("--pemisah hanya boleh ',' atau ';' (atau \\t).")
    pemisah = "\t" if a.pemisah in ("\\t", "\t") else a.pemisah

    momen_user = {}
    for m in a.momen:
        bagian = m.split(":")
        if len(bagian) < 2 or not bagian[1].strip():
            galat("Format --momen harus \"YYYY-MM-DD:Nama\" (dapat: '{}').".format(m))
        tipe = "tema"
        if len(bagian) >= 3 and bagian[-1].strip().lower() in ("promo", "tema", "peringatan"):
            tipe = bagian[-1].strip().lower()
            nama = ":".join(bagian[1:-1]).strip()
        else:
            nama = ":".join(bagian[1:]).strip()
        d = parse_tanggal(bagian[0], "Tanggal momen")
        momen_user.setdefault(d, []).append((nama, tipe))

    global MOMEN_TETAP
    if a.tanpa_momen_nasional:
        MOMEN_TETAP = {}
    if a.fakta is not None and a.fakta_file:
        galat("Pilih salah satu: --fakta atau --fakta-file.")
    fakta = a.fakta if a.fakta is not None else (baca_teks(a.fakta_file) if a.fakta_file else None)
    if fakta is not None and not fakta.strip():
        galat("Fakta kosong. Isi dengan salinan persis pesan pengguna.")
    override = {}
    for jenis, nilai in (("awal_ramadan", a.awal_ramadan), ("idulfitri", a.idulfitri), ("imlek", a.imlek)):
        if nilai:
            override[jenis] = parse_tanggal(nilai, "--" + jenis.replace("_", "-"))
    baris_isi = baca_isi(a.isi) if a.isi else None
    if baris_isi:
        mulai = parse_tanggal(baris_isi[0]["Tanggal"])
        akhir = parse_tanggal(baris_isi[-1]["Tanggal"])
        a.hari = len(baris_isi)
    else:
        akhir = mulai + timedelta(days=a.hari - 1)
    momen_semua = {d: list(v) for d, v in momen_user.items()}
    kunci = {}
    if not a.tanpa_perkiraan:
        momen_pk, kunci = hitung_perkiraan(mulai, akhir, override, momen_user)
        for d, v in momen_pk.items():
            momen_semua.setdefault(d, []).extend(v)

    if a.cek_teks:
        teks = baca_teks(a.cek_teks)
        temuan = cek_teks(teks, kunci, mulai, akhir)
        if fakta is not None:
            temuan += cek_fakta_teks(teks, fakta)
        gagal = [x for x in temuan if x.startswith("GAGAL")]
        for x in temuan:
            print(x)
        print("HASIL: {} ({} GAGAL, {} CEK)".format("GAGAL" if gagal else "LULUS", len(gagal), len(temuan) - len(gagal)))
        sys.exit(2 if gagal else 0)

    if baris_isi:
        baris = baris_isi
        bentrok = periksa_isi(baris, gajian, momen_semua)
        if fakta is not None:
            for b in baris:
                isi = " | ".join([b["Ide Konten"], b["Hook / Judul"], b["CTA"]])
                for x in cek_fakta_teks(isi, fakta):
                    if x.startswith("GAGAL"):
                        bentrok.append("Baris {} ({}): {}".format(b["No"], b["Tanggal_tampil"], x))
        pilar = list(dict.fromkeys(b["Pilar"] for b in baris))
    else:
        baris, bentrok = susun(mulai, a.hari, pilar, platform, gajian, momen_semua)
    di_luar = sorted(d.isoformat() for d in momen_user if not mulai <= d <= akhir)

    hitung = {}
    for b in baris:
        hitung[b["Pilar"]] = hitung.get(b["Pilar"], 0) + 1
    ringkasan = {"mulai": mulai.isoformat(), "selesai": akhir.isoformat(), "jumlah_hari": a.hari,
                 "sebaran_pilar": hitung, "momen_di_luar_rentang": di_luar, "peringatan": list(bentrok)}
    idx_promo = next((x for x in pilar if "promo" in x.lower() or "jual" in x.lower()), None)
    if idx_promo and hitung.get(idx_promo, 0) > 0.4 * a.hari:
        ringkasan["peringatan"].append(
            "Pilar {} mengisi {} dari {} hari (>40%). Audiens mudah bosan; pertimbangkan menambah pilar non-promo.".format(
                idx_promo, hitung[idx_promo], a.hari))

    if a.format == "json":
        teks = json.dumps({"ringkasan": ringkasan, "baris": baris}, ensure_ascii=False, indent=2)
    elif a.format == "csv":
        buf = io.StringIO()
        w = csv.writer(buf, delimiter=pemisah, lineterminator="\n")
        w.writerow(KOLOM)
        for b in baris:
            w.writerow([b["No"], b["Tanggal"]] + [b[k] for k in KOLOM[2:]])
        teks = buf.getvalue()
    else:
        out = ["Kalender konten {} s.d. {} ({} hari)".format(fmt_tgl(mulai), fmt_tgl(akhir), a.hari), "",
               "| " + " | ".join(KOLOM) + " |", "|" + "---|" * len(KOLOM)]
        for b in baris:
            sel = [str(b["No"]), b["Tanggal_tampil"]] + [str(b[k]).replace("|", "/").replace("\n", " ") for k in KOLOM[2:]]
            out.append("| " + " | ".join(sel) + " |")
        out.append("")
        out.append("Sebaran pilar: " + ", ".join("{} {}".format(k, v) for k, v in hitung.items()))
        if di_luar:
            out.append("Momen di luar rentang (diabaikan): " + ", ".join(di_luar))
        for w in ringkasan["peringatan"]:
            out.append("PERINGATAN: " + w)
        teks = "\n".join(out) + "\n"

    if a.output:
        try:
            # utf-8-sig agar Excel membaca huruf/emoji dengan benar
            with open(a.output, "w", encoding="utf-8-sig" if a.format == "csv" else "utf-8", newline="") as f:
                f.write(teks)
        except OSError as e:
            galat("Gagal menyimpan ke {}: {}".format(a.output, e))
        print("Tersimpan: {}".format(a.output))
        print(json.dumps(ringkasan, ensure_ascii=False))
    else:
        sys.stdout.write(teks)
        if a.format == "csv":
            print(json.dumps(ringkasan, ensure_ascii=False), file=sys.stderr)
    if any("GAGAL" in w for w in ringkasan["peringatan"]):
        print("Ada GAGAL (klaim yang tidak disebut pengguna). Perbaiki barisnya lalu jalankan ulang.", file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()
