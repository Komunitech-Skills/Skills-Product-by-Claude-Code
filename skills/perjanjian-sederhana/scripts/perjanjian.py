#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Alat bantu angka & pemeriksaan draf perjanjian sederhana (Bahasa Indonesia).

Subperintah:
  terbilang   Ubah nominal menjadi kata:  terbilang "Rp 15.500.000"
  tanggal     Kalimat pembuka tanggal:    tanggal 2026-09-23
  termin      Jadwal pembayaran bertahap: termin --total "Rp 10.000.000" --persen 30,40,30
  bagihasil   Simulasi nisbah bagi hasil: bagihasil --persen 60,40 --pihak "Pemodal,Pengelola" --contoh "Rp 12.500.000"
  denda       Hitung denda keterlambatan: denda --nilai "Rp 5.000.000" --persen-per-hari 0,1 --hari 30 --maks-persen 5
  sampai      Tanggal berakhir:           sampai 2026-10-01 --bulan 12   (-> 30 September 2027)
  retainer    Jadwal bayar bulanan:       retainer --per-bulan "Rp 3.000.000" --bulan 6 --mulai 2026-10-01 --tanggal-bayar 5
  meterai     Kebutuhan bea meterai:      meterai --rangkap 2
  cek         Periksa draf (.md/.txt):    cek draf.md
  bagi        Naskah siap kirim di chat:  bagi draf.md --maks 3800   (teks biasa, "Bagian 1/N", potong antar-pasal)
  cek-balasan Periksa balasan chat:       cek-balasan balasan.txt    (jalur berkas, istilah proses, format kanal)

Hanya library standar Python 3.8+. Tanpa akses jaringan.
Pembulatan: semua nominal dibulatkan ke rupiah terdekat (0,5 ke atas); sisa pembulatan
pada termin/bagi hasil diletakkan di baris terakhir agar total selalu tepat.
"""
import argparse
import json
import os
import re
import sys
from datetime import date, datetime, timedelta
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP, ROUND_FLOOR

VERSI = "1.0.9"
MAKS_PESAN = 3800              # batas aman per pesan chat (Telegram memotong di 4.096 karakter)
TARIF_METERAI = 10000          # UU 10/2020 Pasal 5 (berlaku per 2026-09-23)
BATAS_DOKUMEN_UANG = 5000000   # dokumen penerimaan uang > Rp5.000.000 kena meterai
BATAS_RUJUK_PROFESIONAL = 500000000  # patokan kebijakan skill (bukan aturan hukum)

SATUAN = ["", "satu", "dua", "tiga", "empat", "lima", "enam", "tujuh", "delapan", "sembilan",
          "sepuluh", "sebelas"]
HARI = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"]
BULAN = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September",
         "Oktober", "November", "Desember"]


class GalatInput(Exception):
    pass


# ---------------------------------------------------------------------------
def parse_rupiah(teks):
    if teks is None:
        raise GalatInput("Nominal kosong.")
    s = str(teks).strip().lower()
    s = s.replace("idr", "").replace("rp.", "").replace("rp", "").strip()
    s = re.sub(r"[.,]\s*-+$", "", s).strip()
    neg = s.startswith("-")
    if neg:
        s = s[1:].strip()
    kali = Decimal(1)
    m = re.search(r"(rb|ribu|k|jt|juta|miliar|milyar|m)\.?$", s)
    if m:
        if m.group(1) == "m":
            raise GalatInput("Singkatan 'm' ambigu (juta atau miliar?). Tulis 'jt'/'juta' atau 'miliar'.")
        kali = {"rb": 1000, "ribu": 1000, "k": 1000, "jt": 10 ** 6, "juta": 10 ** 6,
                "miliar": 10 ** 9, "milyar": 10 ** 9}[m.group(1)]
        kali = Decimal(kali)
        s = s[:m.start()].strip()
    s = s.replace(" ", "")
    if not s or not re.fullmatch(r"[\d.,]+", s):
        raise GalatInput("Nominal '{}' tidak terbaca. Contoh: 'Rp 1.500.000', '1500000', '1,5jt'.".format(teks))
    if "," in s and "." in s:
        s = s.replace(".", "").replace(",", ".") if s.rfind(",") > s.rfind(".") else s.replace(",", "")
    elif "," in s:
        b = s.split(",")
        if len(b) == 2 and (len(b[1]) != 3 or kali != 1):
            s = s.replace(",", ".")
        elif all(len(x) == 3 for x in b[1:]):
            s = s.replace(",", "")
        else:
            raise GalatInput("Nominal '{}' tidak terbaca.".format(teks))
    elif "." in s:
        b = s.split(".")
        if len(b) == 2 and (len(b[1]) != 3 or kali != 1):
            pass
        elif all(len(x) == 3 for x in b[1:]):
            s = s.replace(".", "")
        else:
            raise GalatInput("Nominal '{}' tidak terbaca.".format(teks))
    try:
        v = Decimal(s) * kali
    except InvalidOperation:
        raise GalatInput("Nominal '{}' tidak terbaca.".format(teks))
    if neg:
        raise GalatInput("Nominal tidak boleh negatif: '{}'.".format(teks))
    return v


def parse_persen(teks):
    try:
        v = Decimal(str(teks).strip().replace("%", "").replace(",", "."))
    except InvalidOperation:
        raise GalatInput("Persentase '{}' tidak terbaca.".format(teks))
    if v < 0:
        raise GalatInput("Persentase tidak boleh negatif.")
    return v


def daftar_persen(teks):
    bagian = [x for x in re.split(r"[;/]|,(?!\d)|\s+", teks.strip()) if x]
    if len(bagian) == 1 and "," in teks and "." not in teks:
        # "30,40,30" -> pisah koma
        bagian = [x for x in teks.split(",") if x.strip()]
    return [parse_persen(x) for x in bagian]


def bulat(d):
    return int(Decimal(d).quantize(Decimal(1), rounding=ROUND_HALF_UP))


def rp(n):
    return "Rp " + "{:,}".format(int(n)).replace(",", ".")


def angka_id(d):
    s = "{:f}".format(Decimal(d).normalize())
    return s.replace(".", ",")


def _terbilang_int(n):
    if n < 12:
        return SATUAN[n]
    if n < 20:
        return SATUAN[n - 10] + " belas"
    if n < 100:
        return (SATUAN[n // 10] + " puluh " + _terbilang_int(n % 10)).strip()
    if n < 200:
        return ("seratus " + _terbilang_int(n - 100)).strip()
    if n < 1000:
        return (SATUAN[n // 100] + " ratus " + _terbilang_int(n % 100)).strip()
    if n < 2000:
        return ("seribu " + _terbilang_int(n - 1000)).strip()
    for nilai, nama in ((10 ** 12, "triliun"), (10 ** 9, "miliar"), (10 ** 6, "juta"), (10 ** 3, "ribu")):
        if n >= nilai:
            return (_terbilang_int(n // nilai) + " " + nama + " " + _terbilang_int(n % nilai)).strip()
    return ""


def terbilang(n):
    n = int(n)
    if n == 0:
        return "nol"
    if n >= 10 ** 15:
        raise GalatInput("Nominal terlalu besar untuk ditulis terbilang.")
    return re.sub(r"\s+", " ", _terbilang_int(n)).strip()


def terbilang_rupiah(nilai):
    d = Decimal(nilai).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    rupiah = int(d.to_integral_value(rounding=ROUND_FLOOR))
    sen = int((d - rupiah) * 100)
    teks = terbilang(rupiah) + " rupiah"
    if sen:
        teks += " " + terbilang(sen) + " sen"
    return teks


def format_nominal(nilai):
    d = Decimal(nilai).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    if d == d.to_integral_value():
        return rp(int(d))
    rupiah = int(d.to_integral_value(rounding=ROUND_FLOOR))
    return rp(rupiah) + ",{:02d}".format(int((d - rupiah) * 100))


def parse_tanggal(teks):
    for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%d-%m-%Y", "%d.%m.%Y"):
        try:
            return datetime.strptime(teks.strip(), fmt).date()
        except ValueError:
            continue
    raise GalatInput("Tanggal '{}' tidak terbaca. Contoh: 2026-09-23 atau 23/09/2026.".format(teks))


# ---------------------------------------------------------------------------
def cmd_terbilang(a):
    v = parse_rupiah(a.nominal)
    catatan = []
    if v != v.to_integral_value():
        catatan.append("Nominal mengandung sen. Jika maksudnya juta/ribu, tulis satuannya (mis. '2,5jt' atau '2,5 juta').")
    elif 0 < v < 1000:
        catatan.append("Nominal di bawah Rp 1.000. Pastikan tidak lupa satuan 'rb'/'jt'.")
    return {"nominal": format_nominal(v), "terbilang": terbilang_rupiah(v),
            "siap_tempel": "{} ({})".format(format_nominal(v), terbilang_rupiah(v)), "catatan": catatan}


def tambah_bulan(d, n):
    y, m = divmod(d.month - 1 + n, 12)
    y += d.year
    m += 1
    hari_maks = (date(y + (m // 12), m % 12 + 1, 1) - timedelta(days=1)).day
    return date(y, m, min(d.day, hari_maks))


def tanggal_panjang(d):
    return "{} {} {}".format(d.day, BULAN[d.month - 1], d.year)


def cmd_sampai(a):
    mulai = parse_tanggal(a.mulai)
    isi = [x for x in (a.hari, a.bulan, a.tahun) if x is not None]
    if len(isi) != 1:
        raise GalatInput("Isi tepat satu: --hari, --bulan, atau --tahun.")
    n = isi[0]
    if n <= 0:
        raise GalatInput("Lama jangka waktu harus lebih dari 0.")
    if a.hari is not None:
        akhir, satuan = mulai + timedelta(days=n - 1), "hari"
    else:
        bln = n if a.bulan is not None else n * 12
        target = tambah_bulan(mulai, bln)
        # jika tanggal dipangkas (mis. 31 Jan + 1 bulan -> 28 Feb), berakhir di akhir bulan itu
        akhir = target if target.day != mulai.day else target - timedelta(days=1)
        satuan = "bulan" if a.bulan is not None else "tahun"
    kalimat = "selama {} ({}) {}, terhitung sejak tanggal {} sampai dengan tanggal {}".format(
        n, terbilang(n), satuan, tanggal_panjang(mulai), tanggal_panjang(akhir))
    return {"mulai": mulai.isoformat(), "berakhir": akhir.isoformat(), "berakhir_teks": tanggal_panjang(akhir),
            "hari_berakhir": HARI[akhir.weekday()], "kalimat": kalimat,
            "catatan": "Tanggal berakhir = sehari sebelum ulang tanggal mulai (hitungan kalender)."}


def cmd_retainer(a):
    per_bulan = bulat(parse_rupiah(a.per_bulan))
    if per_bulan <= 0 or a.bulan <= 0:
        raise GalatInput("--per-bulan dan --bulan harus lebih dari 0.")
    if a.bulan > 120:
        raise GalatInput("--bulan maksimal 120.")
    mulai = parse_tanggal(a.mulai)
    if mulai.day > 28:
        raise GalatInput("Untuk retainer, pilih tanggal mulai 1-28 agar periode bulanan tidak tumpang tindih.")
    if not 1 <= a.tanggal_bayar <= 28:
        raise GalatInput("--tanggal-bayar harus 1-28 agar ada di setiap bulan.")
    jadwal = []
    for i in range(a.bulan):
        awal = tambah_bulan(mulai, i)
        nxt = tambah_bulan(mulai, i + 1)
        akhir = nxt if nxt.day != mulai.day else nxt - timedelta(days=1)
        if a.bayar == "di-muka":
            jatuh = awal if a.tanggal_bayar is None else date(awal.year, awal.month, a.tanggal_bayar)
            if jatuh < awal:
                jatuh = awal
        else:
            nb = tambah_bulan(date(akhir.year, akhir.month, 1), 1) if akhir.day >= a.tanggal_bayar else \
                date(akhir.year, akhir.month, 1)
            jatuh = date(nb.year, nb.month, a.tanggal_bayar)
        jadwal.append({"bulan_ke": i + 1, "periode": "{} s.d. {}".format(tanggal_panjang(awal), tanggal_panjang(akhir)),
                       "jatuh_tempo": tanggal_panjang(jatuh), "nilai": per_bulan, "nilai_teks": rp(per_bulan)})
    total = per_bulan * a.bulan
    return {"per_bulan": per_bulan, "per_bulan_teks": "{} ({})".format(rp(per_bulan), terbilang_rupiah(per_bulan)),
            "jumlah_bulan": a.bulan, "total": total, "total_teks": "{} ({})".format(rp(total), terbilang_rupiah(total)),
            "bayar": a.bayar, "jadwal": jadwal,
            "catatan": "Cocok untuk jasa berulang (admin sosmed, konsultan bulanan). Pastikan pekerjaan tetap mandiri "
                       "(bukan jam kerja/perintah seperti karyawan)."}


def cmd_tanggal(a):
    if not a.tanggal:
        # Tanggal tanda tangan TIDAK diisi otomatis (hari ini belum tentu hari penandatanganan).
        return {"tanggal": None, "hari": None, "tanggal_panjang": "[isi: tanggal]",
                "kalimat_pembuka": "Pada hari ini, [isi: hari], tanggal [isi: tanggal] bulan [isi: bulan] tahun "
                                   "[isi: tahun]",
                "catatan": "Tanggal penandatanganan tidak diberikan, jadi dibiarkan kosong untuk diisi saat tanda "
                           "tangan. Jalankan ulang dengan tanggal (mis. tanggal 2026-10-05) bila sudah pasti."}
    d = parse_tanggal(a.tanggal)
    kalimat = "Pada hari ini, {}, tanggal {} bulan {} tahun {} ({})".format(
        HARI[d.weekday()], terbilang(d.day), BULAN[d.month - 1], terbilang(d.year),
        d.strftime("%d-%m-%Y"))
    return {"tanggal": d.isoformat(), "hari": HARI[d.weekday()],
            "tanggal_panjang": "{} {} {}".format(d.day, BULAN[d.month - 1], d.year), "kalimat_pembuka": kalimat}


def bagi_proporsional(total, persen):
    """Bagi total (int rupiah) sesuai persen; sisa pembulatan ke baris terakhir."""
    hasil = [bulat(Decimal(total) * p / 100) for p in persen[:-1]]
    hasil.append(total - sum(hasil))
    return hasil


def cmd_termin(a):
    total = bulat(parse_rupiah(a.total))
    if total <= 0:
        raise GalatInput("Total harus lebih dari 0.")
    persen = daftar_persen(a.persen)
    if not persen:
        raise GalatInput("Isi --persen, contoh: --persen 30,40,30")
    if sum(persen) != 100:
        raise GalatInput("Jumlah persen termin = {}%, harus tepat 100%.".format(angka_id(sum(persen))))
    nama = [x.strip() for x in a.nama.split(",")] if a.nama else []
    jadwal = [x.strip() for x in a.jadwal.split(";")] if a.jadwal else []
    if a.nama and len(nama) != len(persen):
        raise GalatInput("Jumlah --nama ({}) tidak sama dengan jumlah termin ({}).".format(len(nama), len(persen)))
    if a.jadwal and len(jadwal) != len(persen):
        raise GalatInput("Jumlah --jadwal ({}) tidak sama dengan jumlah termin ({}). Pisahkan dengan ';'.".format(
            len(jadwal), len(persen)))
    nilai = bagi_proporsional(total, persen)
    baris = []
    for i, (p, v) in enumerate(zip(persen, nilai)):
        baris.append({"termin": i + 1, "nama": nama[i] if nama else "Termin {}".format(i + 1),
                      "persen": angka_id(p), "nilai": v, "nilai_teks": rp(v), "terbilang": terbilang_rupiah(v),
                      "jadwal": jadwal[i] if jadwal else None})
    return {"total": total, "total_teks": rp(total), "total_terbilang": terbilang_rupiah(total), "termin": baris,
            "cek_total": sum(nilai) == total,
            "catatan_pembulatan": "Tiap termin dibulatkan ke rupiah terdekat; sisa pembulatan masuk termin terakhir."}


def cmd_bagihasil(a):
    persen = daftar_persen(a.persen)
    if len(persen) < 2:
        raise GalatInput("Bagi hasil minimal untuk 2 pihak, contoh: --persen 60,40")
    if sum(persen) != 100:
        raise GalatInput("Jumlah nisbah = {}%, harus tepat 100%.".format(angka_id(sum(persen))))
    pihak = [x.strip() for x in a.pihak.split(",")] if a.pihak else \
        ["Pihak {}".format(["Pertama", "Kedua", "Ketiga", "Keempat", "Kelima"][i] if i < 5 else i + 1)
         for i in range(len(persen))]
    if len(pihak) != len(persen):
        raise GalatInput("Jumlah --pihak ({}) tidak sama dengan jumlah nisbah ({}).".format(len(pihak), len(persen)))
    hasil = {"nisbah": [{"pihak": n, "persen": angka_id(p)} for n, p in zip(pihak, persen)],
             "dasar": a.dasar,
             "catatan": ["Nisbah dihitung dari {} (definisikan dengan jelas di perjanjian).".format(
                 "laba bersih" if a.dasar == "laba" else "omzet/pendapatan kotor")]}
    if a.dasar == "omzet":
        hasil["catatan"].append("Bagi hasil dari omzet tetap dibayar walau usaha rugi; pastikan pengelola "
                                "sanggup menanggung biaya operasional.")
    contoh = []
    for c in (a.contoh or []):
        v = bulat(parse_rupiah(c))
        if v < 0:
            raise GalatInput("Contoh nilai tidak boleh negatif.")
        pembagian = bagi_proporsional(v, persen)
        contoh.append({"nilai": v, "nilai_teks": rp(v),
                       "pembagian": [{"pihak": n, "nilai": x, "nilai_teks": rp(x), "terbilang": terbilang_rupiah(x)}
                                     for n, x in zip(pihak, pembagian)]})
    hasil["contoh"] = contoh
    hasil["catatan_pembulatan"] = "Bagian tiap pihak dibulatkan ke rupiah terdekat; sisa pembulatan ke pihak terakhir."
    return hasil


def cmd_denda(a):
    nilai = bulat(parse_rupiah(a.nilai))
    if a.hari < 0:
        raise GalatInput("--hari tidak boleh negatif.")
    if (a.persen_per_hari is None) == (a.per_hari is None):
        raise GalatInput("Pilih salah satu: --persen-per-hari (mis. 0,1) atau --per-hari (mis. 'Rp 50.000').")
    if a.persen_per_hari is not None:
        p = parse_persen(a.persen_per_hari)
        per_hari = Decimal(nilai) * p / 100
        dasar = "{}% x {} per hari".format(angka_id(p), rp(nilai))
    else:
        per_hari = parse_rupiah(a.per_hari)
        dasar = "{} per hari".format(rp(bulat(per_hari)))
    denda_mentah = bulat(per_hari * a.hari)
    maks = None
    if a.maks_persen is not None:
        maks = bulat(Decimal(nilai) * parse_persen(a.maks_persen) / 100)
    elif a.maks is not None:
        maks = bulat(parse_rupiah(a.maks))
    denda = min(denda_mentah, maks) if maks is not None else denda_mentah
    catatan = []
    if maks is None:
        catatan.append("Tidak ada batas maksimum denda. Sebaiknya beri batas (mis. 5% dari nilai) agar wajar.")
    if nilai and denda * 100 > nilai * 10:
        catatan.append("Denda melebihi 10% dari nilai kewajiban; berisiko dinilai tidak wajar. Pertimbangkan batas lebih rendah.")
    return {"nilai_kewajiban": nilai, "dasar": dasar, "hari_terlambat": a.hari,
            "denda_per_hari": bulat(per_hari), "denda_sebelum_batas": denda_mentah, "batas_maksimum": maks,
            "denda": denda, "denda_teks": rp(denda), "terbilang": terbilang_rupiah(denda), "catatan": catatan}


def cmd_meterai(a):
    if a.rangkap is None:
        a.rangkap = 2 if a.jenis == "perjanjian" else 1
    if a.rangkap < 1:
        raise GalatInput("--rangkap minimal 1.")
    hasil = {"tarif_per_meterai": TARIF_METERAI, "dasar": "UU 10/2020 tentang Bea Meterai (tarif tetap Rp10.000)"}
    if a.jenis == "perjanjian":
        total = TARIF_METERAI * a.rangkap
        hasil.update({"wajib": True, "jumlah_meterai": a.rangkap, "total_biaya": total, "total_teks": rp(total),
                      "penjelasan": "Surat perjanjian beserta rangkapnya adalah objek bea meterai berapa pun nilainya. "
                                    "Bea meterai terutang saat dokumen ditandatangani. Untuk dokumen yang dibuat dua "
                                    "pihak atau lebih, masing-masing pihak menanggung meterai atas dokumen yang "
                                    "diterimanya. Meterai bukan syarat sah perjanjian; dokumen yang belum bermeterai "
                                    "dapat dilunasi kemudian (pemeteraian kemudian) bila akan dipakai sebagai alat bukti."})
    else:
        if a.nilai is None:
            raise GalatInput("Untuk --jenis kwitansi isi --nilai (nominal uang yang diterima).")
        nilai = bulat(parse_rupiah(a.nilai))
        wajib = nilai > BATAS_DOKUMEN_UANG
        hasil.update({"wajib": wajib, "nilai": nilai, "jumlah_meterai": a.rangkap if wajib else 0,
                      "total_biaya": TARIF_METERAI * a.rangkap if wajib else 0,
                      "penjelasan": ("Dokumen penerimaan uang bernilai lebih dari Rp5.000.000 wajib bermeterai."
                                     if wajib else "Nilai tidak lebih dari Rp5.000.000: kwitansi tidak wajib bermeterai.")})
    hasil["tips"] = "Gunakan meterai tempel asli atau e-meterai dari kanal resmi; tanda tangan mengenai sebagian meterai."
    return hasil


# ---------------------------------------------------------------------------
PASAL_WAJIB = [
    ("para pihak", r"yang bertanda tangan di bawah ini|para pihak|pihak pertama"),
    ("ruang lingkup/objek", r"ruang lingkup|objek perjanjian|lingkup pekerjaan|objek sewa|tujuan"),
    ("hak dan kewajiban", r"hak dan kewajiban|kewajiban"),
    ("jangka waktu", r"jangka waktu|masa berlaku"),
    ("wanprestasi", r"wanprestasi|cidera janji|ingkar janji"),
    ("keadaan memaksa", r"keadaan memaksa|force majeure|overmacht"),
    ("penyelesaian sengketa", r"penyelesaian (perselisihan|sengketa)"),
    ("lain-lain/penutup", r"lain-lain|ketentuan penutup|penutup"),
    ("tanda tangan", r"tanda tangan|pihak pertama\s*\n[\s\S]*pihak kedua"),
]
POLA_BAHAYA = [
    (r"\b(jual beli|hibah|balik nama)\b[^.\n]{0,80}\b(tanah|rumah|bangunan|apartemen|ruko|lahan|kavling|kaveling|"
     r"shm|shgb|sertifikat)\b|\bakta jual beli\b|\bajb\b|\bppat\b|\bppjb\b|pengikatan jual beli|\bkavling\b|\bkaveling\b",
     "Jual beli/pengikatan jual beli tanah, kavling, atau bangunan wajib lewat notaris/PPAT (PP 24/1997 Ps. 37). "
     "Rujuk ke notaris/PPAT."),
    (r"\b(saham|penyertaan modal|investor|investasi|dana investasi)\b(?! pemilik)|"
     r"\b(imbal hasil|keuntungan|profit|return|bagi hasil|hasil)\s+(tetap|pasti|dijamin|minimal)\b|"
     r"\b(keuntungan|imbal hasil|profit|bagi hasil|return)\b[^.\n]{0,15}\d+(?:[.,]\d+)?\s?%\s?(per|/|setiap|tiap)\s?"
     r"(bulan|minggu|tahun|hari)|\bmodal\s+(kembali|balik)\s+(utuh|penuh|100)",
     "Unsur investasi/imbal hasil tetap atau pasti. Rujuk ke pengacara (dan cek aturan OJK bila menghimpun dana)."),
    (r"\b(warga negara asing|wna|perusahaan asing|luar negeri|foreign|usd|dolar|dollar|sgd)\b",
     "Melibatkan pihak/mata uang asing. Wajib bahasa Indonesia (UU 24/2009 Ps. 31) + dwibahasa; rujuk ke pengacara."),
    (r"\b(jaminan fidusia|fidusia|hak tanggungan|gadai|agunan|jaminan sertifikat|bpkb)\b|sebagai jaminan|"
     r"\bbunga\b[^.\n]{0,20}\d+(?:[.,]\d+)?\s?%|\bpinjam(an)? uang\b|\b(utang|hutang)[ -]piutang\b",
     "Pinjam-meminjam uang dengan bunga dan/atau jaminan (BPKB, sertifikat, fidusia). Perlu akta/pendaftaran "
     "khusus dan cermat soal bunga; rujuk ke notaris/pengacara."),
    (r"\bharga (jual )?(kembali )?(minimum|minimal|terendah)\b|"
     r"(dilarang|tidak boleh|tidak diperkenankan|wajib tidak)\s+menjual[^.\n]{0,40}(di bawah|lebih (murah|rendah))|"
     r"menjual dengan harga (tidak kurang dari|minimal|serendah-rendahnya)|banting harga|\bmap\b|"
     r"minimum advertised price",
     "Klausul harga jual kembali minimum/larangan banting harga: berisiko melanggar UU 5/1999 Ps. 8 "
     "(persaingan usaha). Ganti dengan 'harga jual yang disarankan' atau rujuk ke pengacara."),
    (r"\b(perjanjian kerja(?! ?sama)|pkwt|pkwtt|karyawan tetap|karyawan kontrak|pesangon)\b",
     "Unsur perjanjian kerja (ketenagakerjaan). Di luar cakupan skill; rujuk ke konsultan HR/pengacara."),
    (r"\bwaralaba|franchise\b", "Waralaba punya aturan khusus; rujuk ke pengacara."),
]


# Pos biaya yang wajib dibebankan ke SATU pihak saja (v1.0.5). Urutan penting: pos spesifik dulu.
POS_BIAYA = [
    ("iuran/retribusi pasar", r"(?:iuran|retribusi)(?:\s+\w+){0,2}\s+pasar|retribusi"),
    ("iuran lingkungan", r"iuran\s+(?:lingkungan|rt|rw|warga)"),
    ("iuran (lainnya)", r"\biuran\b"),
    ("listrik", r"\blistrik\b"),
    ("air", r"\bair\b|\bpdam\b"),
    ("internet", r"\binternet\b|\bwifi\b"),
    ("kebersihan", r"\bkebersihan\b|\bsampah\b"),
    ("keamanan", r"\bkeamanan\b"),
    ("PBB", r"\bpbb\b|pajak bumi"),
    ("perbaikan besar", r"perbaikan\s+besar"),
    ("perbaikan kecil", r"perbaikan\s+kecil"),
]
POLA_SEPIHAK = (r"\b(mengunci|menyegel|menggembok|mengambil alih|membongkar paksa)\b[^.\n]{0,60}"
                r"(objek sewa|kios|toko|tempat|ruko|alat|barang)|pengosongan (paksa|sepihak)|"
                r"mengosongkan[^.\n]{0,40}(secara sepihak|secara paksa|sendiri)|(mengambil|menarik)[^.\n]{0,40}secara paksa|"
                r"tanpa (melalui )?(proses hukum|putusan pengadilan)")
POLA_BEBAN = r"membayar|dibayar|menanggung|ditanggung|tanggungan|beban|atas biaya|biaya .* oleh"


def _pihak_di(baris, sewa):
    b = baris.lower()
    ada = set()
    if re.search(r"pihak\s+pertama", b):
        ada.add("PIHAK PERTAMA")
    if re.search(r"pihak\s+kedua", b):
        ada.add("PIHAK KEDUA")
    if sewa:
        if re.search(r"\bpemilik\b|yang menyewakan", b):
            ada.add("PIHAK PERTAMA")
        if re.search(r"\bpenyewa\b", b):
            ada.add("PIHAK KEDUA")
    return ada


def cek_kewajiban(teks):
    """Cek konsistensi beban biaya: tiap pos (listrik, air, iuran, PBB, perbaikan) hanya ke satu pihak.

    Baris dibaca satu per satu. Pihak = pihak yang disebut di baris itu, atau pihak dari konteks
    "PIHAK X wajib:" / judul "Kewajiban PIHAK X" bila baris tidak menyebut pihak. Baris yang menyebut
    kedua pihak atau "masing-masing"/"bersama" dilewati (tidak bisa dipastikan). Hasil: (peta, konflik).
    """
    sewa = bool(re.search(r"\bsewa\b", teks.lower()))
    konteks = None
    peta = {}
    for no, baris in enumerate(teks.splitlines(), 1):
        b = baris.lower()
        if "tinjau pengacara" in b:
            continue
        if re.match(r"\s*#", baris):
            pk = _pihak_di(baris, False) if "kewajiban" in b else set()
            konteks = next(iter(pk)) if len(pk) == 1 else None
            continue
        m = re.search(r"(pihak\s+pertama|pihak\s+kedua)\s+wajib\s*:", b)
        if m:
            konteks = "PIHAK PERTAMA" if "pertama" in m.group(1) else "PIHAK KEDUA"
            continue
        if re.match(r"\s*\(\d+\)", baris):
            konteks = None
        if not re.search(POLA_BEBAN, b) and not (konteks and re.match(r"\s*[a-z]\.\s", b)):
            continue
        if re.search(r"masing-masing|bersama-sama|dibagi\s+(dua|rata)|patungan", b):
            continue
        if konteks and re.match(r"\s*[a-z]\.\s", b):
            pihak = {konteks}  # butir "a. ..." di bawah "PIHAK X wajib:" -> subjeknya PIHAK X
        else:
            pihak = _pihak_di(baris, sewa)
            if not pihak and konteks:
                pihak = {konteks}
        if len(pihak) != 1:
            continue
        pihak = next(iter(pihak))
        sisa = b
        for pos, pola in POS_BIAYA:
            if re.search(pola, sisa):
                peta.setdefault(pos, {}).setdefault(pihak, []).append(no)
                sisa = re.sub(pola, " ", sisa)
    konflik = []
    for pos, per in peta.items():
        if len(per) > 1:
            konflik.append("Beban '{}' bertentangan: {}. Tetapkan satu pihak saja dan samakan di semua pasal "
                           "serta daftar asumsi.".format(pos, "; ".join(
                               "{} (baris {})".format(p, ", ".join(str(x) for x in nos)) for p, nos in sorted(per.items()))))
    ringkas = {pos: sorted(per) for pos, per in peta.items()}
    return ringkas, konflik


def cari_nominal(teks):
    """Temukan pola 'Rp X (terbilang ...)' dan cek kecocokannya."""
    hasil = []
    for m in re.finditer(r"Rp\.?\s?([\d.]+(?:,\d{1,2})?)\s*(?:,-)?\s*\(\s*([a-zA-Z ]+?)\s*\)", teks):
        angka_teks, kata = m.group(1), m.group(2).strip().lower()
        try:
            v = parse_rupiah(angka_teks)
        except GalatInput:
            continue
        seharusnya = terbilang_rupiah(v)
        kata_n = re.sub(r"\s+", " ", kata)
        if not kata_n.endswith(("rupiah", "sen")):
            kata_n_cmp, seharusnya_cmp = kata_n, re.sub(r" rupiah.*$", "", seharusnya)
        else:
            kata_n_cmp, seharusnya_cmp = kata_n, seharusnya
        hasil.append({"teks": m.group(0), "nilai": bulat(v), "terbilang_tertulis": kata_n,
                      "terbilang_seharusnya": seharusnya, "cocok": kata_n_cmp == seharusnya_cmp})
    return hasil


def cmd_cek(a):
    if not os.path.isfile(a.file):
        raise GalatInput("File '{}' tidak ditemukan.".format(a.file))
    with open(a.file, "rb") as f:
        data = f.read()
    if not data.strip():
        raise GalatInput("File draf kosong.")
    if data[:2] == b"PK":
        raise GalatInput("File ini .docx/ZIP. Simpan draf sebagai .md atau .txt dulu, lalu cek lagi.")
    if b"\x00" in data[:4096]:
        raise GalatInput("File tidak bisa dibaca sebagai teks.")
    try:
        teks = data.decode("utf-8-sig")
    except UnicodeDecodeError:
        teks = data.decode("latin-1")
    teks = re.sub(r"<!--[\s\S]*?-->", "", teks)  # abaikan blok panduan agent
    rendah = teks.lower()
    masalah, info = [], []
    placeholder = sorted(set(re.findall(r"\[\[[^\]]+\]\]|\[isi:[^\]\n]*\]", teks)))
    if placeholder:
        masalah.append("Masih ada {} isian kosong: {}".format(len(placeholder), ", ".join(placeholder[:15]) +
                                                              (" ..." if len(placeholder) > 15 else "")))
    if re.search(r"\[\[[^\]]+\]\]", teks):
        info.append("Gaya isian [[...]] ditemukan. Pakai satu gaya saja: [isi: ...] (perintah 'bagi' mengubahnya otomatis).")
    kosong = len(re.findall(r"_{5,}|\.{8,}", teks))
    tinjau = len(re.findall(r"TINJAU PENGACARA", teks))
    if tinjau:
        info.append("{} pasal bertanda TINJAU PENGACARA. Hapus tanda ini hanya setelah ditinjau/diputuskan.".format(tinjau))
    hilang = [nama for nama, pola in PASAL_WAJIB if not re.search(pola, rendah)]
    if hilang:
        masalah.append("Bagian standar belum ada: " + ", ".join(hilang))
    if not re.search(r"harga|pembayaran|imbalan|biaya|nisbah|bagi hasil|tanpa imbalan", rendah):
        info.append("Tidak ada pasal harga/pembayaran. Wajar untuk NDA; untuk jenis lain wajib ada.")
    if "meterai" not in rendah and "materai" not in rendah:
        masalah.append("Belum ada tempat/keterangan meterai Rp10.000 di bagian tanda tangan.")
    if "materai" in rendah:
        info.append("Ejaan baku adalah 'meterai' (bukan 'materai').")
    # penomoran pasal
    nomor = [int(x) for x in re.findall(r"(?im)^\s*#*\s*\**\s*pasal\s+(\d+)\b", teks)]
    if nomor:
        harap = list(range(1, len(nomor) + 1))
        if nomor != harap:
            masalah.append("Penomoran pasal tidak urut: {}".format(", ".join(str(x) for x in nomor)))
    else:
        masalah.append("Tidak ditemukan judul 'Pasal 1', 'Pasal 2', dst.")
    nominal = cari_nominal(teks)
    salah = [n for n in nominal if not n["cocok"]]
    for n in salah:
        masalah.append("Angka dan terbilang tidak cocok: '{}' -> seharusnya '{}'".format(n["teks"], n["terbilang_seharusnya"]))
    angka_tanpa_terbilang = 0
    for m in re.finditer(r"Rp\.?\s?\d[\d.]{3,}(?:,\d{1,2})?(?![\d.,]*\d)(?!\s*(?:,-)?\s*\()", teks):
        if "meterai" in rendah[max(0, m.start() - 25):m.start()] or "materai" in rendah[max(0, m.start() - 25):m.start()]:
            continue  # "Meterai Rp10.000" bukan nominal perjanjian
        angka_tanpa_terbilang += 1
    if angka_tanpa_terbilang:
        info.append("{} nominal belum disertai terbilang dalam kurung (disarankan untuk nominal penting).".format(
            angka_tanpa_terbilang))
    semua_nilai = [n["nilai"] for n in nominal]
    for m in re.finditer(r"Rp\.?\s?([\d.]{4,})", teks):
        try:
            semua_nilai.append(bulat(parse_rupiah(m.group(1))))
        except GalatInput:
            pass
    rujuk = []
    if semua_nilai and max(semua_nilai) >= BATAS_RUJUK_PROFESIONAL:
        rujuk.append("Ada nilai >= {} (patokan skill). Draf hanya bahan diskusi; wajib ditinjau pengacara.".format(
            rp(BATAS_RUJUK_PROFESIONAL)))
    # catatan peninjauan (> ⚠ TINJAU PENGACARA ...) tidak dihitung sebagai isi perjanjian
    isi_pasal = "\n".join(b for b in rendah.splitlines() if "tinjau pengacara" not in b)
    for pola, pesan in POLA_BAHAYA:
        if re.search(pola, isi_pasal):
            rujuk.append(pesan)
    # v1.0.6: klausul pengosongan/pengambilalihan sepihak (tanpa putusan pengadilan) bukan default
    sepihak = [b for b in rendah.splitlines() if "tinjau pengacara" not in b
               and not re.search(r"tidak akan|tidak boleh|dilarang|tanpa persetujuan pihak kedua atau putusan", b)
               and re.search(POLA_SEPIHAK, b)]
    if sepihak:
        pesan = ("Ada klausul pengosongan/pengambilalihan sepihak (kunci, segel, bongkar, ambil paksa) tanpa putusan "
                 "pengadilan. Default yang aman: teguran tertulis -> tenggat -> musyawarah/pengadilan.")
        if "tinjau pengacara" in rendah:
            info.append(pesan + " Pastikan pengguna sendiri yang memintanya dan peringatan risikonya tercantum.")
        else:
            masalah.append(pesan + " Ganti dengan mekanisme itu, atau (hanya bila diminta pengguna) beri tanda "
                                   "TINJAU PENGACARA + peringatan risiko.")
    beban, konflik = cek_kewajiban(teks)
    masalah.extend(konflik)
    if kosong:
        info.append("{} garis/titik isian (____ atau ........) ditemukan; pastikan memang untuk diisi tangan.".format(kosong))
    status = "SIAP DITINJAU" if not masalah and not rujuk else ("RUJUK PROFESIONAL" if rujuk else "PERLU PERBAIKAN")
    return {"file": os.path.basename(a.file), "status": status, "masalah": masalah, "rujuk_profesional": rujuk,
            "info": info, "jumlah_pasal": len(nomor), "nominal_diperiksa": nominal,
            "beban_biaya": beban}


# ---------------------------------------------------------------------------
# v1.0.9: naskah untuk kanal chat (Telegram/WhatsApp) & pemeriksa balasan
PEMISAH_PESAN = "<<<PESAN BERIKUTNYA>>>"
POLA_ISIAN_LAMA = re.compile(r"\[\[(.+?)\]\]")
POLA_BATAS = re.compile(r"(?i)^\s*(pasal\s+\d+\b|lampiran\b|demikian\b)")
POLA_AYAT = re.compile(r"^\s*\(\d+\)")


def baca_teks(path):
    if not os.path.isfile(path):
        raise GalatInput("File '{}' tidak ditemukan.".format(path))
    with open(path, "rb") as f:
        data = f.read()
    if not data.strip():
        raise GalatInput("File kosong.")
    if data[:2] == b"PK":
        raise GalatInput("File ini .docx/ZIP. Simpan sebagai .md atau .txt dulu.")
    if b"\x00" in data[:4096]:
        raise GalatInput("File tidak bisa dibaca sebagai teks.")
    try:
        return data.decode("utf-8-sig")
    except UnicodeDecodeError:
        return data.decode("latin-1")


def seragamkan_isian(teks):
    """[[X]] -> [isi: X] (satu gaya isian)."""
    return POLA_ISIAN_LAMA.sub(lambda m: "[isi: {}]".format(m.group(1).strip()), teks)


def _kapital(teks):
    """Huruf kapital, kecuali isi [isi: ...] dan [Meterai ...]."""
    bagian = re.split(r"(\[[^\]]*\])", teks)
    return "".join(b if b.startswith("[") else b.upper() for b in bagian)


def _bersih_sel(sel):
    sel = re.sub(r"(?i)<br\s*/?>", " ", sel)
    return re.sub(r"\s+", " ", sel.replace("**", "")).strip()


def _tabel_ke_baris(baris_tabel):
    sel = [[_bersih_sel(c) for c in b.strip().strip("|").split("|")] for b in baris_tabel
           if not re.match(r"^\s*\|?\s*:?-{2,}", b)]
    if not sel:
        return []
    kepala, isi = sel[0], sel[1:]
    if all(h.upper().startswith("PIHAK") for h in kepala if h):
        # tabel tanda tangan -> per pihak, berurutan ke bawah
        out = []
        for i, h in enumerate(kepala):
            out.append(h)
            out.extend(r[i] for r in isi if i < len(r) and r[i])
            out.append("")
        return out[:-1]
    out = []
    for r in isi:
        no = r[0] if kepala and kepala[0].lower() in ("no", "no.", "nomor") else ""
        pasangan = [(h, v) for h, v in zip(kepala, r) if v and not (no and h == kepala[0])]
        teks = "; ".join("{}: {}".format(h, v) if h else v for h, v in pasangan)
        out.append("{}. {}".format(no, teks) if no else "- " + teks)
    return out


def ke_teks_chat(teks):
    """Markdown draf -> teks biasa untuk chat: tanpa blok kode, tanpa judul #, tanpa tabel pipa."""
    teks = seragamkan_isian(re.sub(r"<!--[\s\S]*?-->", "", teks))
    hasil, tabel = [], []
    for b in teks.splitlines() + [""]:
        if re.match(r"^\s*\|.*\|\s*$", b):
            tabel.append(b)
            continue
        if tabel:
            hasil.extend(_tabel_ke_baris(tabel))
            tabel = []
        if re.match(r"^\s*(```|~~~)", b) or re.match(r"^\s*(-{3,}|\*{3,}|_{3,})\s*$", b):
            continue
        m = re.match(r"^\s*#{1,6}\s*(.*)$", b)
        if m:
            judul = _kapital(m.group(1).replace("**", "").strip())
            if hasil and re.match(r"^PASAL \d+$", hasil[-1]) and not re.match(r"^PASAL \d+", judul):
                hasil[-1] += " — " + judul
            else:
                hasil.append(judul)
            continue
        b = re.sub(r"^\s*>\s?", "", b).replace("**", "")
        hasil.append(b.rstrip())
    out = re.sub(r"\n{3,}", "\n\n", "\n".join(hasil)).strip()
    return out


def _potong_blok(blok, batas):
    """Blok terlalu panjang -> potong di batas ayat, lalu di batas baris (cadangan)."""
    baris = blok.split("\n")
    potongan, kini = [], []
    for b in baris:
        calon = "\n".join(kini + [b])
        if kini and len(calon) > batas and (POLA_AYAT.match(b) or len("\n".join(kini)) > batas * 0.5):
            potongan.append("\n".join(kini))
            kini = [b]
        else:
            kini.append(b)
    potongan.append("\n".join(kini))
    hasil = []
    for p in potongan:
        while len(p) > batas:
            hasil.append(p[:batas])
            p = p[batas:]
        hasil.append(p)
    return hasil


def bagi_pesan(teks, maks=MAKS_PESAN):
    if maks < 500:
        raise GalatInput("--maks terlalu kecil (minimal 500 karakter).")
    teks = ke_teks_chat(teks)
    blok, kini = [], []
    for b in teks.split("\n"):
        if POLA_BATAS.match(b) and len(b) < 120 and kini:
            blok.append("\n".join(kini).strip())
            kini = []
        kini.append(b)
    blok.append("\n".join(kini).strip())
    blok = [x for x in blok if x]
    ruang = maks - len("Bagian 99/99\n\n")
    catatan, siap = [], []
    for x in blok:
        if len(x) > ruang:
            catatan.append("Satu pasal/bagian lebih dari {} karakter; dipotong di batas ayat: {}".format(
                ruang, x.split("\n", 1)[0][:60]))
            siap.extend(_potong_blok(x, ruang))
        else:
            siap.append(x)
    pesan, kini = [], ""
    for x in siap:
        calon = (kini + "\n\n" + x) if kini else x
        if kini and len(calon) > ruang:
            pesan.append(kini)
            kini = x
        else:
            kini = calon
    if kini:
        pesan.append(kini)
    n = len(pesan)
    pesan = ["Bagian {}/{}\n\n{}".format(i + 1, n, p) for i, p in enumerate(pesan)]
    return {"jumlah_bagian": n, "maks_karakter": maks, "panjang": [len(p) for p in pesan],
            "total_karakter": len(teks), "bagian": pesan, "catatan": catatan}


def cmd_bagi(a):
    return bagi_pesan(baca_teks(a.file), a.maks)


POLA_BALASAN = [
    (r"(?:(?<=\s)|^|(?<=[`(\"']))(?:~|[A-Za-z]:)?[/\\](?:[\w.\-]+[/\\])+[\w.\-]*",
     "Menyebut jalur berkas/folder. Ganti dengan: \"Draf juga sudah saya simpan sebagai berkas. Balas 'kirim file' "
     "bila mau dikirim sebagai dokumen.\""),
    (r"\b[\w\-]+\.(?:md|txt|docx|pdf|json|py|html)\b", "Menyebut nama berkas. Jangan sebut nama/jalur berkas di chat."),
    (r"(?i)\b(?:workspace|folder kerja|direktori)\b", "Menyebut folder/workspace. Jangan sebut lokasi berkas di chat."),
    (r"(?i)\b(?:script|scripts|skrip|tool|tools|exec|python3?)\b",
     "Memakai istilah proses (script/skrip/tool/exec/python). Contoh pengganti: \"angka & terbilang sudah dihitung ulang\"."),
    (r"(?m)^\s*(?:```|~~~)", "Ada blok kode. Kirim naskah sebagai teks biasa, bukan di dalam blok kode."),
    (r"(?m)^\s*#{1,6}\s", "Ada judul Markdown (#/##). Pakai judul huruf kapital biasa, mis. PASAL 3 — HARGA SEWA."),
    (r"(?m)^\s*\|.*\|\s*$", "Ada tabel pipa (|). Ubah jadi baris pendek, mis. \"1. Pintu: baik\"."),
    (r"\[\[[^\]]+\]\]", "Ada isian gaya [[...]]. Pakai satu gaya saja: [isi: ...]."),
]


def periksa_balasan(teks, maks=MAKS_PESAN):
    masalah = []
    for pola, pesan in POLA_BALASAN:
        temu = sorted(set(m.group(0).strip() for m in re.finditer(pola, teks)))
        if temu:
            masalah.append("{} Ditemukan: {}".format(pesan, ", ".join(temu[:5])))
    pesan_list = [p.strip() for p in teks.split(PEMISAH_PESAN)] if PEMISAH_PESAN in teks else None
    if pesan_list is None:
        potong = re.split(r"(?m)^(?=\**\s*Bagian \d+/\d+)", teks)
        pesan_list = [p.strip() for p in potong if p.strip()]
    panjang = [len(p) for p in pesan_list]
    for i, n in enumerate(panjang):
        if n > maks:
            masalah.append("Pesan/bagian ke-{} panjangnya {} karakter (> {}). Pecah per pasal: \"Bagian 1/N\".".format(
                i + 1, n, maks))
    return {"status": "SIAP KIRIM" if not masalah else "PERLU PERBAIKAN", "masalah": masalah,
            "jumlah_pesan": len(pesan_list), "panjang_pesan": panjang, "maks_karakter": maks}


def cmd_cek_balasan(a):
    return periksa_balasan(baca_teks(a.file), a.maks)


# ---------------------------------------------------------------------------
def cetak_teks(perintah, h):
    o = []
    if perintah == "terbilang":
        o.append(h["siap_tempel"])
        o.extend("Catatan: " + c for c in h["catatan"])
    elif perintah == "sampai":
        o.append(h["kalimat"])
        o.append("Berakhir: {}, {}".format(h["hari_berakhir"], h["berakhir_teks"]))
    elif perintah == "retainer":
        o.append("Biaya per bulan: {}; {} bulan; total {}".format(h["per_bulan_teks"], h["jumlah_bulan"], h["total_teks"]))
        for j in h["jadwal"]:
            o.append("- Bulan ke-{} ({}): {} jatuh tempo {}".format(j["bulan_ke"], j["periode"], j["nilai_teks"],
                                                                  j["jatuh_tempo"]))
        o.append(h["catatan"])
    elif perintah == "tanggal":
        o.append(h["kalimat_pembuka"])
        if h.get("catatan"):
            o.append(h["catatan"])
    elif perintah == "termin":
        o.append("Total: {} ({})".format(h["total_teks"], h["total_terbilang"]))
        for t in h["termin"]:
            o.append("- {} ({}%): {} ({}){}".format(t["nama"], t["persen"], t["nilai_teks"], t["terbilang"],
                                                   ", " + t["jadwal"] if t["jadwal"] else ""))
        o.append("Cek total: {}".format("cocok" if h["cek_total"] else "TIDAK COCOK"))
        o.append(h["catatan_pembulatan"])
    elif perintah == "bagihasil":
        o.append("Nisbah: " + ", ".join("{} {}%".format(n["pihak"], n["persen"]) for n in h["nisbah"]))
        for c in h["contoh"]:
            o.append("Contoh bila {} = {}:".format("laba bersih" if h["dasar"] == "laba" else "omzet", c["nilai_teks"]))
            for p in c["pembagian"]:
                o.append("  - {}: {} ({})".format(p["pihak"], p["nilai_teks"], p["terbilang"]))
        o.extend(h["catatan"])
        o.append(h["catatan_pembulatan"])
    elif perintah == "denda":
        o.append("Dasar: {}; terlambat {} hari.".format(h["dasar"], h["hari_terlambat"]))
        o.append("Denda sebelum batas: {}".format(rp(h["denda_sebelum_batas"])))
        if h["batas_maksimum"] is not None:
            o.append("Batas maksimum: {}".format(rp(h["batas_maksimum"])))
        o.append("Denda: {} ({})".format(h["denda_teks"], h["terbilang"]))
        o.extend("Catatan: " + c for c in h["catatan"])
    elif perintah == "meterai":
        o.append("Wajib meterai: {}".format("YA" if h["wajib"] else "TIDAK"))
        if h["wajib"]:
            o.append("Jumlah meterai Rp10.000: {} lembar, total {}".format(h["jumlah_meterai"], rp(h["total_biaya"])))
        o.append(h["penjelasan"])
        o.append(h["tips"])
    elif perintah == "cek":
        o.append("Status draf: {} ({} pasal)".format(h["status"], h["jumlah_pasal"]))
        for judul, isi in (("Harus diperbaiki", h["masalah"]), ("Rujuk profesional", h["rujuk_profesional"]),
                           ("Info", h["info"])):
            if isi:
                o.append(judul + ":")
                o.extend("- " + x for x in isi)
        if h.get("beban_biaya"):
            o.append("Beban biaya per pos: " + "; ".join("{}: {}".format(k, " & ".join(v))
                                                         for k, v in h["beban_biaya"].items()))
        if h["nominal_diperiksa"]:
            o.append("Nominal + terbilang diperiksa: {} (cocok {})".format(
                len(h["nominal_diperiksa"]), sum(1 for n in h["nominal_diperiksa"] if n["cocok"])))
    elif perintah == "bagi":
        o.append(("\n\n" + PEMISAH_PESAN + "\n\n").join(h["bagian"]))
        if h["catatan"]:
            sys.stderr.write("".join("Catatan: " + c + "\n" for c in h["catatan"]))
    elif perintah == "cek-balasan":
        o.append("Status balasan: {} ({} pesan; panjang {})".format(
            h["status"], h["jumlah_pesan"], ", ".join(str(x) for x in h["panjang_pesan"])))
        o.extend("- " + m for m in h["masalah"])
    return "\n".join(o)


class ParserID(argparse.ArgumentParser):
    def error(self, message):
        pesan = message.replace("the following arguments are required", "argumen wajib belum diisi") \
                       .replace("unrecognized arguments", "argumen tidak dikenal") \
                       .replace("invalid choice", "pilihan tidak valid").replace("choose from", "pilih dari") \
                       .replace("expected one argument", "butuh satu nilai") \
                       .replace("invalid int value", "harus bilangan bulat")
        sys.stderr.write("GALAT: {}\nKetik --help untuk melihat cara pakai.\n".format(pesan))
        sys.exit(2)


def main(argv=None):
    induk = ParserID(add_help=False)
    induk.add_argument("--format", choices=["teks", "json"], default=argparse.SUPPRESS)
    p = ParserID(description="Alat bantu angka & pemeriksaan draf perjanjian sederhana.")
    p.add_argument("--format", choices=["teks", "json"], default="teks")
    p.add_argument("--versi", action="version", version="perjanjian.py " + VERSI)
    sub = p.add_subparsers(dest="perintah", parser_class=ParserID)
    s = sub.add_parser("terbilang", parents=[induk]); s.add_argument("nominal")
    s = sub.add_parser("tanggal", parents=[induk]); s.add_argument("tanggal", nargs="?")
    s = sub.add_parser("termin", parents=[induk])
    s.add_argument("--total", required=True); s.add_argument("--persen", required=True)
    s.add_argument("--nama", help="nama termin dipisah koma, mis. 'DP,Pelunasan'")
    s.add_argument("--jadwal", help="jadwal tiap termin dipisah ';'")
    s = sub.add_parser("bagihasil", parents=[induk])
    s.add_argument("--persen", required=True); s.add_argument("--pihak")
    s.add_argument("--dasar", choices=["laba", "omzet"], default="laba")
    s.add_argument("--contoh", action="append", help="nilai laba/omzet contoh (boleh berulang)")
    s = sub.add_parser("denda", parents=[induk])
    s.add_argument("--nilai", required=True); s.add_argument("--hari", type=int, required=True)
    s.add_argument("--persen-per-hari"); s.add_argument("--per-hari")
    s.add_argument("--maks-persen"); s.add_argument("--maks")
    s = sub.add_parser("meterai", parents=[induk])
    s.add_argument("--jenis", choices=["perjanjian", "kwitansi"], default="perjanjian")
    s.add_argument("--rangkap", type=int, help="jumlah rangkap asli (default: 2 untuk perjanjian, 1 untuk kwitansi)")
    s.add_argument("--nilai")
    s = sub.add_parser("sampai", parents=[induk]); s.add_argument("mulai")
    s.add_argument("--hari", type=int); s.add_argument("--bulan", type=int); s.add_argument("--tahun", type=int)
    s = sub.add_parser("retainer", parents=[induk])
    s.add_argument("--per-bulan", required=True); s.add_argument("--bulan", type=int, required=True)
    s.add_argument("--mulai", required=True); s.add_argument("--tanggal-bayar", type=int, default=5)
    s.add_argument("--bayar", choices=["di-muka", "di-belakang"], default="di-muka")
    s = sub.add_parser("cek", parents=[induk]); s.add_argument("file")
    s = sub.add_parser("bagi", parents=[induk]); s.add_argument("file")
    s.add_argument("--maks", type=int, default=MAKS_PESAN, help="maks. karakter per pesan (default 3800)")
    s = sub.add_parser("cek-balasan", parents=[induk]); s.add_argument("file")
    s.add_argument("--maks", type=int, default=MAKS_PESAN)
    a = p.parse_args(argv)
    if not a.perintah:
        p.print_help()
        return 2
    fungsi = {"terbilang": cmd_terbilang, "tanggal": cmd_tanggal, "termin": cmd_termin, "bagihasil": cmd_bagihasil,
              "denda": cmd_denda, "meterai": cmd_meterai, "cek": cmd_cek, "sampai": cmd_sampai,
              "retainer": cmd_retainer, "bagi": cmd_bagi, "cek-balasan": cmd_cek_balasan}[a.perintah]
    try:
        h = fungsi(a)
    except GalatInput as e:
        if a.format == "json":
            sys.stderr.write(json.dumps({"error": str(e)}, ensure_ascii=False) + "\n")
        else:
            sys.stderr.write("GALAT: {}\n".format(e))
        return 1
    print(json.dumps(h, ensure_ascii=False, indent=2) if a.format == "json" else cetak_teks(a.perintah, h))
    return 0


if __name__ == "__main__":
    for _aliran in (sys.stdout, sys.stderr):
        try:
            _aliran.reconfigure(encoding="utf-8")
        except (AttributeError, ValueError):
            pass
    sys.exit(main())
