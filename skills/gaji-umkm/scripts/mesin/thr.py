#!/usr/bin/env python3
"""Hitung THR Keagamaan per karyawan + PPh 21 atas THR (metode TER) + batas bayar H-7.

Dasar (status per 2026-09-23, rincian di references/regulasi.md):
- Permenaker 6/2016 Pasal 2, 3, 5, 7, 10 dan SE Menaker M/3/HK.04.00/III/2026:
  masa kerja >= 12 bulan: 1 bulan upah; 1 s.d. < 12 bulan: masa kerja/12 x 1 bulan upah;
  < 1 bulan: tidak wajib. Upah 1 bulan = upah bersih ATAU upah pokok + tunjangan tetap.
  Harian lepas: rata-rata upah 12 bulan terakhir (>= 12 bulan) atau rata-rata per bulan selama masa kerja.
  Satuan hasil: rata-rata upah 12 bulan terakhir. Dibayar paling lambat 7 hari sebelum hari raya, penuh, tidak dicicil.
- PPh 21: THR masuk penghasilan bruto bulan dibayar; dipotong dengan TER bulanan (PP 58/2023, PMK 168/2023).

Contoh:
  python3 thr.py --hari-raya 2027-03-10 --nama-hari-raya "Idul Fitri 1448 H" --data karyawan.csv
  python3 thr.py --hari-raya 2026-12-25 --nama Budi --ptkp K/1 --gaji-pokok 5jt --tunjangan-tetap 500rb --mulai 2026-04-01

Hanya library standar Python 3.8+. Tidak ada akses jaringan. Keluar dengan kode 2 bila input salah.
"""
import argparse
import csv
import datetime
import io
import json
import re
import sys
from decimal import Decimal

import ter_core as tc

HARI = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"]
JENIS = {
    "tetap": "pkwtt", "pkwtt": "pkwtt", "permanen": "pkwtt", "karyawan_tetap": "pkwtt",
    "pkwt": "pkwt", "kontrak": "pkwt",
    "harian": "harian", "harian_lepas": "harian", "lepas": "harian", "phl": "harian",
    "satuan": "satuan", "satuan_hasil": "satuan", "borongan": "satuan", "borong": "satuan",
}
LABEL_JENIS = {"pkwtt": "Tetap (PKWTT)", "pkwt": "Kontrak (PKWT)", "harian": "Harian lepas", "satuan": "Satuan hasil"}
YA = {"ya", "y", "yes", "true", "1", "iya"}
TIDAK = {"tidak", "t", "no", "n", "false", "0", "tdk"}

DISCLAIMER = ("Alat bantu hitung, bukan nasihat hukum/pajak. Dasar: Permenaker 6/2016, SE Menaker "
              "M/3/HK.04.00/III/2026, PP 58/2023 & PMK 168/2023 (PPh 21 TER), berlaku per 23 September 2026. "
              "Untuk sengketa/kasus khusus hubungi Disnaker setempat, Posko THR (poskothr.kemnaker.go.id), "
              "Kring Pajak 1500200, atau konsultan.")


class InputError(Exception):
    pass


def angka(nilai, nama, default=None):
    if nilai is None or str(nilai).strip() == "":
        if default is None:
            raise InputError("{} wajib diisi".format(nama))
        return default
    try:
        return tc.parse_angka(nilai, nama)
    except ValueError as e:
        raise InputError(str(e))


def ya_tidak(nilai, nama, default):
    if nilai is None or str(nilai).strip() == "":
        return default
    s = str(nilai).strip().lower()
    if s in YA:
        return True
    if s in TIDAK:
        return False
    raise InputError("{}: isi 'ya' atau 'tidak' (bukan '{}')".format(nama, nilai))


def parse_tanggal(teks, nama):
    s = str(teks or "").strip()
    if not s:
        raise InputError("{} wajib diisi (format 2026-03-20 atau 20/03/2026)".format(nama))
    for pola in ("%Y-%m-%d", "%d/%m/%Y", "%d-%m-%Y", "%d.%m.%Y"):
        try:
            return datetime.datetime.strptime(s, pola).date()
        except ValueError:
            continue
    raise InputError("{}: '{}' bukan tanggal yang dikenali (pakai 2026-03-20 atau 20/03/2026)".format(nama, s))


def tambah_bulan(d, n):
    """Tanggal d ditambah n bulan; tanggal dipotong ke akhir bulan bila perlu (31 Jan + 1 bulan = 28/29 Feb)."""
    y, m = divmod(d.month - 1 + n, 12)
    y += d.year
    m += 1
    hari_akhir = [31, 29 if (y % 4 == 0 and (y % 100 != 0 or y % 400 == 0)) else 28, 31, 30, 31, 30, 31, 31, 30, 31,
                  30, 31][m - 1]
    return datetime.date(y, m, min(d.day, hari_akhir))


def bulan_penuh(mulai, sampai):
    """Jumlah bulan penuh masa kerja, INKLUSIF: tanggal mulai dan tanggal acuan sama-sama dihitung sebagai hari kerja.

    Contoh: 11 Mar 2026 s.d. 10 Mar 2027 = 12 bulan; 1 Jan s.d. 31 Jan = 1 bulan; 1 Jan s.d. 30 Jan = 0 bulan.
    Kembalikan -1 bila sampai < mulai.
    """
    if sampai < mulai:
        return -1
    akhir = sampai + datetime.timedelta(days=1)       # batas eksklusif
    n = (akhir.year - mulai.year) * 12 + (akhir.month - mulai.month)
    while n > 0 and tambah_bulan(mulai, n) > akhir:
        n -= 1
    while tambah_bulan(mulai, n + 1) <= akhir:
        n += 1
    return n


def kurang_hari_ke_bulan_berikut(mulai, sampai, n):
    """Berapa hari lagi sampai masa kerja genap n+1 bulan (untuk peringatan kasus tepi)."""
    return (tambah_bulan(mulai, n + 1) - (sampai + datetime.timedelta(days=1))).days


def format_tanggal(d):
    return "{}, {} {} {}".format(HARI[d.weekday()], d.day, tc.NAMA_BULAN[d.month - 1], d.year)


def daftar_upah(teks, nama):
    if teks is None or str(teks).strip() == "":
        return []
    hasil = []
    for b in [x for x in re.split(r"[+;|\s]+", str(teks).strip()) if x]:
        hasil.append(angka(b, nama))
    return hasil


# ---------------------------------------------------------------- hitung
def hitung_karyawan(r, cfg):
    label = r.get("nama") or "baris {}".format(r.get("_baris", "?"))
    if not r.get("nama"):
        raise InputError("{}: kolom 'nama' kosong".format(label))
    peringatan = []
    jenis_raw = (r.get("jenis") or "tetap").strip().lower().replace(" ", "_")
    if jenis_raw not in JENIS:
        raise InputError("{}: jenis '{}' tidak dikenali (pakai tetap, kontrak, harian, atau satuan)".format(
            label, r.get("jenis")))
    jenis = JENIS[jenis_raw]
    hari_raya = cfg["hari_raya"]

    # --- masa kerja
    acuan = hari_raya
    berhenti = parse_tanggal(r["tanggal_berhenti"], label + ": tanggal_berhenti") if r.get("tanggal_berhenti") else None
    berhak, alasan = True, ""
    if berhenti and berhenti < hari_raya:
        selisih = (hari_raya - berhenti).days
        if jenis == "pkwtt" and selisih <= 30:
            alasan = ("PHK {} hari sebelum hari raya (≤ 30 hari) — tetap berhak THR (Permenaker 6/2016 Pasal 7 "
                      "ayat 1).".format(selisih))
            acuan = berhenti
        elif jenis == "pkwtt":
            berhak, alasan = False, "Berhenti lebih dari 30 hari sebelum hari raya — tidak wajib THR."
        else:
            berhak, alasan = False, ("Hubungan kerja waktu tertentu berakhir sebelum hari raya — tidak wajib THR "
                                     "(Permenaker 6/2016 Pasal 7 ayat 3).")
    if r.get("masa_kerja_bulan"):
        masa = angka(r["masa_kerja_bulan"], label + ": masa_kerja_bulan")
        sumber_masa = "diisi pengguna"
    else:
        if not r.get("tanggal_mulai"):
            raise InputError("{}: isi tanggal_mulai (tanggal mulai kerja) atau masa_kerja_bulan".format(label))
        mulai = parse_tanggal(r["tanggal_mulai"], label + ": tanggal_mulai")
        n = bulan_penuh(mulai, acuan)
        if n < 0:
            raise InputError("{}: tanggal_mulai {} setelah tanggal hari raya/berhenti".format(label, mulai))
        masa = Decimal(n)
        sumber_masa = "bulan penuh dari {} s.d. {} (inklusif)".format(mulai.strftime("%d/%m/%Y"),
                                                                        acuan.strftime("%d/%m/%Y"))
        if n < 12:
            kurang = kurang_hari_ke_bulan_berikut(mulai, acuan, n)
            if 0 < kurang <= 3:
                peringatan.append("{}: masa kerja {} bulan, kurang {} hari lagi menjadi {} bulan{}. Aturan tidak mengatur "
                                  "pecahan bulan; pertimbangkan membulatkan ke atas agar tidak dipersoalkan (isi "
                                  "masa_kerja_bulan).".format(label, n, kurang, n + 1,
                                                              " (THR penuh)" if n + 1 == 12 else ""))
    if masa < 1:
        berhak, alasan = False, "Masa kerja kurang dari 1 bulan — belum wajib THR (Permenaker 6/2016 Pasal 2)."

    # --- upah 1 bulan
    if jenis in ("pkwtt", "pkwt"):
        pokok = angka(r.get("gaji_pokok"), label + ": gaji_pokok")
        tetap = angka(r.get("tunjangan_tetap"), label + ": tunjangan_tetap", Decimal(0))
        upah = pokok + tetap
        dasar_upah = "gaji pokok + tunjangan tetap" if tetap else "upah bersih/gaji pokok"
    else:
        daftar = daftar_upah(r.get("upah_bulanan"), label + ": upah_bulanan")
        if not daftar:
            raise InputError("{}: untuk pekerja {} isi upah_bulanan = upah yang diterima tiap bulan, dipisah '+', "
                             "mis. 3jt+3,2jt+2,8jt".format(label, LABEL_JENIS[jenis].lower()))
        if masa >= 12 or jenis == "satuan":
            if len(daftar) < 12:
                peringatan.append("{}: aturan memakai rata-rata 12 bulan terakhir, tetapi baru ada {} bulan data; "
                                  "rata-rata dihitung dari data yang ada.".format(label, len(daftar)))
            dipakai = daftar[-12:]
            dasar_upah = "rata-rata upah {} bulan terakhir".format(len(dipakai))
        else:
            dipakai = daftar
            dasar_upah = "rata-rata upah per bulan selama masa kerja ({} bulan data)".format(len(dipakai))
            if masa >= 1 and len(daftar) != int(masa) and len(daftar) != int(masa) + 1:
                peringatan.append("{}: jumlah data upah ({} bulan) tidak sama dengan masa kerja ({} bulan) — cek lagi."
                                  .format(label, len(daftar), masa))
        upah = sum(dipakai, Decimal(0)) / len(dipakai)

    # --- THR
    if not berhak:
        thr_aturan = Decimal(0)
        rumus = "tidak wajib"
    elif masa >= 12:
        thr_aturan = tc.bulat_terdekat(upah)
        rumus = "masa kerja ≥ 12 bulan → 1 × upah"
    else:
        thr_aturan = tc.bulat_terdekat(masa / 12 * upah)
        rumus = "{}/12 × upah".format(tc.format_persen(masa).rstrip("%"))
    thr = thr_aturan
    kebijakan = angka(r.get("thr_kebijakan"), label + ": thr_kebijakan", Decimal(-1))
    if kebijakan >= 0:
        if kebijakan >= thr_aturan:
            thr = tc.bulat_terdekat(kebijakan)
            if kebijakan > thr_aturan:
                rumus += " (dipakai nilai perusahaan yang lebih besar)"
        else:
            peringatan.append("{}: THR menurut kebijakan perusahaan ({}) lebih kecil dari minimum aturan ({}). "
                              "Yang wajib dibayar minimal {}.".format(label, tc.format_rp(kebijakan),
                                                                     tc.format_rp(thr_aturan), tc.format_rp(thr_aturan)))

    # --- PPh 21 atas THR
    pph = {"dihitung": False}
    bayar = cfg["tanggal_bayar"]
    mantan = bool(berhenti) and (bayar.year, bayar.month) > (berhenti.year, berhenti.month)
    if thr > 0 and mantan:
        # Mantan Pegawai: tarif Pasal 17 x bruto (PMK 168/2023 Pasal 12 ayat 8, Pasal 16 ayat 6; contoh Tuan O)
        pajak, rincian = tc.pasal17(thr)
        pph = {"dihitung": True, "metode": "mantan_pegawai", "tambahan_pph_thr": tc.bulat_bawah(pajak),
               "rincian_pasal17": rincian, "dtp": False}
        if ya_tidak(r.get("dtp"), label + ": dtp", False):
            peringatan.append("{}: PPh 21 DTP tidak diterapkan untuk mantan pegawai.".format(label))
    elif r.get("ptkp") and thr > 0 and jenis not in ("pkwtt", "pkwt"):
        tc.normalisasi_ptkp(r["ptkp"])
        pph = {"dihitung": False, "alasan": "Pekerja harian/satuan: PPh 21 memakai aturan pegawai tidak tetap "
               "(TER harian atau TER bulanan bila dibayar bulanan) — hitung dengan skill pph21-ter."}
    elif r.get("ptkp") and thr > 0:
        ptkp = tc.normalisasi_ptkp(r["ptkp"])
        kat = tc.kategori_ter(ptkp)
        if bayar.month == 12 or (berhenti and (berhenti.year, berhenti.month) == (bayar.year, bayar.month)):
            pph = {"dihitung": False, "alasan": "THR dibayar di Masa Pajak Terakhir (Desember/bulan berhenti): PPh 21 "
                   "dihitung ulang setahun — gunakan hitungan setahun (skill pph21-ter/slip-gaji-bpjs)."}
            peringatan.append("{}: {}".format(label, pph["alasan"]))
        else:
            if r.get("bruto_bulan_bayar"):
                reguler = angka(r["bruto_bulan_bayar"], label + ": bruto_bulan_bayar")
                sumber_reg = "diisi pengguna"
            else:
                reguler = upah
                sumber_reg = "perkiraan = gaji pokok + tunjangan tetap"
                peringatan.append("{}: bruto gaji bulan THR dibayar tidak diisi; dipakai gaji pokok + tunjangan tetap "
                                  "(belum termasuk lembur, tunjangan tidak tetap, premi JKK/JKM/BPJS Kesehatan). "
                                  "Isi bruto_bulan_bayar agar PPh 21 tepat.".format(label))
            pph_tanpa, t1 = tc.pph_ter_bulanan(reguler, kat)
            pph_dengan, t2 = tc.pph_ter_bulanan(reguler + thr, kat)
            dtp = ya_tidak(r.get("dtp"), label + ": dtp", False)
            if dtp:
                if r.get("bruto_tetap_januari"):
                    bruto_tetap = angka(r["bruto_tetap_januari"], label + ": bruto_tetap_januari")
                else:
                    bruto_tetap = upah
                    peringatan.append("{}: kolom bruto_tetap_januari kosong — syarat DTP dicek memakai gaji pokok + "
                                      "tunjangan tetap ({}).".format(label, tc.format_rp(upah)))
                ok, alasan_dtp = tc.cek_syarat_dtp(bayar.year, bruto_tetap)
                if not ok:
                    dtp = False
                    peringatan.append("{}: TIDAK memenuhi syarat PPh 21 DTP — {}. PPh 21 dipotong normal.".format(
                        label, alasan_dtp))
            pph = {"dihitung": True, "metode": "ter", "ptkp": ptkp, "kategori": kat, "bruto_reguler": reguler,
                   "sumber_bruto": sumber_reg, "tarif_tanpa_thr": t1, "pph_tanpa_thr": pph_tanpa,
                   "tarif_dengan_thr": t2, "pph_dengan_thr": pph_dengan, "tambahan_pph_thr": pph_dengan - pph_tanpa,
                   "dtp": dtp}
    elif thr > 0:
        pph = {"dihitung": False, "alasan": "Status PTKP tidak diisi — PPh 21 atas THR tidak dihitung."}

    tambahan = pph.get("tambahan_pph_thr", Decimal(0)) if pph.get("dihitung") and not pph.get("dtp") else Decimal(0)
    return {
        "nama": r.get("nama"), "jabatan": r.get("jabatan", ""), "jenis": jenis, "jenis_label": LABEL_JENIS[jenis],
        "masa_kerja_bulan": masa, "sumber_masa_kerja": sumber_masa, "upah_sebulan": upah, "dasar_upah": dasar_upah,
        "berhak": berhak, "alasan": alasan, "rumus": rumus, "thr_minimum": thr_aturan, "thr": thr, "pph21": pph,
        "thr_setelah_pph": thr - tambahan, "peringatan": peringatan,
    }


# ---------------------------------------------------------------- input/output
def norm_kolom(k):
    k = (k or "").strip().lower().replace(" ", "_").replace("-", "_")
    alias = {"nama_karyawan": "nama", "status_ptkp": "ptkp", "gaji": "gaji_pokok", "upah_pokok": "gaji_pokok",
             "tunjangan": "tunjangan_tetap", "mulai_kerja": "tanggal_mulai", "tgl_mulai": "tanggal_mulai",
             "tanggal_masuk": "tanggal_mulai", "status": "jenis", "status_kerja": "jenis", "masa_kerja": "masa_kerja_bulan",
             "tgl_berhenti": "tanggal_berhenti", "tanggal_keluar": "tanggal_berhenti", "upah": "upah_bulanan"}
    return alias.get(k, k)


def baca_csv(path):
    try:
        with open(path, "rb") as f:
            mentah = f.read()
    except OSError as e:
        raise InputError("File '{}' tidak bisa dibaca: {}".format(path, e.strerror))
    teks = None
    for enc in ("utf-8-sig", "cp1252"):
        try:
            teks = mentah.decode(enc)
            break
        except UnicodeDecodeError:
            continue
    if not teks or not teks.strip():
        raise InputError("File CSV kosong")
    try:
        dialek = csv.Sniffer().sniff(teks[:4096], delimiters=",;\t")
    except csv.Error:
        dialek = csv.excel
    rd = csv.DictReader(io.StringIO(teks), dialect=dialek)
    kolom = [norm_kolom(f) for f in (rd.fieldnames or [])]
    if "nama" not in kolom:
        raise InputError("CSV wajib punya kolom 'nama' (ditemukan: {})".format(", ".join(rd.fieldnames or [])))
    baris = []
    for i, row in enumerate(rd, start=2):
        d = {norm_kolom(k): (v or "").strip() for k, v in row.items() if k is not None}
        if any(d.values()):
            d["_baris"] = i
            baris.append(d)
    if not baris:
        raise InputError("CSV tidak berisi data karyawan")
    return baris


def pengumuman(cfg, perusahaan):
    return "\n".join([
        "Yth. Rekan-rekan karyawan {},".format(perusahaan or "kami"),
        "",
        "Menyambut {}, perusahaan akan membayarkan Tunjangan Hari Raya (THR) Keagamaan pada {} (paling lambat {}, "
        "yaitu 7 hari sebelum hari raya).".format(cfg["nama_hari_raya"], format_tanggal(cfg["tanggal_bayar"]),
                                                   format_tanggal(cfg["batas_bayar"])),
        "",
        "Ketentuan besaran THR (Permenaker 6/2016 & SE Menaker M/3/HK.04.00/III/2026):",
        "• Masa kerja 12 bulan atau lebih: 1 bulan upah (gaji pokok + tunjangan tetap).",
        "• Masa kerja 1 bulan s.d. kurang dari 12 bulan: masa kerja ÷ 12 × 1 bulan upah.",
        "• THR dibayar penuh, tidak dicicil, dan dikenai PPh 21 sesuai ketentuan pajak.",
        "",
        "Rincian THR masing-masing akan disampaikan secara pribadi. Jika ada pertanyaan, silakan hubungi bagian "
        "HR/keuangan.",
        "",
        "Selamat menyambut hari raya. Terima kasih atas kerja keras Bapak/Ibu.",
        "",
        "Salam,",
        "Manajemen {}".format(perusahaan or ""),
    ]).rstrip()


def teks_hasil(hasil, cfg, total, csv_path):
    o = ["**Rincian THR {} — {}**".format(cfg["nama_hari_raya"], cfg["perusahaan"] or "-"),
         "Hari raya: {} · **Batas bayar (H-7): {}** · Rencana bayar: {}".format(
             format_tanggal(cfg["hari_raya"]), format_tanggal(cfg["batas_bayar"]), format_tanggal(cfg["tanggal_bayar"])),
         "", "| Nama | Status | Masa kerja | Upah 1 bulan | Rumus | THR | PPh 21 karena THR | THR diterima |",
         "|---|---|---:|---:|---|---:|---:|---:|"]
    for h in hasil:
        p = h["pph21"]
        if p.get("dihitung"):
            pph_teks = tc.format_rp(p["tambahan_pph_thr"]) + (" (DTP)" if p["dtp"] else "")
        else:
            pph_teks = "–"
        o.append("| {} | {} | {} bln | {} | {} | **{}** | {} | {} |".format(
            h["nama"], h["jenis_label"], tc.format_persen(h["masa_kerja_bulan"]).rstrip("%"),
            tc.format_rp(h["upah_sebulan"]), h["rumus"], tc.format_rp(h["thr"]), pph_teks,
            tc.format_rp(h["thr_setelah_pph"])))
    o += ["| **Total** | | | | | **{}** | **{}** | **{}** |".format(
        tc.format_rp(total["thr"]), tc.format_rp(total["pph"]), tc.format_rp(total["diterima"])), ""]
    for h in hasil:
        if h["alasan"]:
            o.append("- {}: {}".format(h["nama"], h["alasan"]))
        p = h["pph21"]
        if not p.get("dihitung") and p.get("alasan") and "Masa Pajak Terakhir" not in p["alasan"]:
            o.append("- {}: {}".format(h["nama"], p["alasan"]))
        if p.get("dihitung") and p.get("metode") == "mantan_pegawai":
            o.append("- {}: THR dibayar setelah bulan berhenti bekerja → berstatus Mantan Pegawai: PPh 21 = tarif "
                     "Pasal 17 × bruto THR = {} (PMK 168/2023 Pasal 16 ayat 6), bukan TER.".format(
                         h["nama"], tc.format_rp(p["tambahan_pph_thr"])))
        elif p.get("dihitung"):
            o.append("- {}: PPh 21 bulan THR dibayar (TER {}) = {} × ({} + THR {}) = {}; tanpa THR {} × {} = {} → "
                     "tambahan {}{}.".format(
                         h["nama"], p["kategori"], tc.format_persen(p["tarif_dengan_thr"]),
                         tc.format_rp(p["bruto_reguler"]), tc.format_rp(h["thr"]), tc.format_rp(p["pph_dengan_thr"]),
                         tc.format_persen(p["tarif_tanpa_thr"]), tc.format_rp(p["bruto_reguler"]),
                         tc.format_rp(p["pph_tanpa_thr"]), tc.format_rp(p["tambahan_pph_thr"]),
                         " (ditanggung pemerintah, dibayar tunai — THR diterima utuh)" if p["dtp"] else ""))
    pr = [x for h in hasil for x in h["peringatan"]] + cfg["peringatan"]
    if pr:
        o += ["", "⚠️ Peringatan:"] + ["- " + x for x in pr]
    o += ["", "Catatan:",
          "- THR wajib dibayar penuh (tidak dicicil) paling lambat 7 hari sebelum hari raya. Terlambat: denda 5% dari "
          "total THR, dan THR tetap wajib dibayar (Permenaker 6/2016 Pasal 10).",
          "- THR bukan dasar iuran BPJS (iuran dihitung dari upah pokok + tunjangan tetap).",
          "- 'Tambahan PPh 21' = selisih PPh 21 bulan itu dengan dan tanpa THR (THR digabung ke bruto bulan dibayar, "
          "tarif TER bisa naik). Di Desember semua dihitung ulang setahun.",
          "- Pembulatan: THR ke rupiah terdekat; PPh 21 ke bawah ke rupiah penuh (belum dicocokkan dengan Coretax).",
          "- Masa kerja dihitung dalam bulan penuh sampai tanggal hari raya (asumsi skill; aturan tidak mengatur "
          "pecahan bulan). Ubah dengan kolom masa_kerja_bulan bila perusahaan memakai cara lain."]
    if csv_path:
        o += ["", "File rekap: " + csv_path]
    o += ["", "**Draf pengumuman untuk karyawan (siap kirim WA/email):**", "", "```", pengumuman(cfg, cfg["perusahaan"]),
          "```", "", "_" + DISCLAIMER + "_"]
    return "\n".join(o)


def ke_json(obj):
    if isinstance(obj, Decimal):
        return tc.angka_json(obj)
    if isinstance(obj, (datetime.date,)):
        return obj.isoformat()
    if isinstance(obj, dict):
        return {k: ke_json(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [ke_json(v) for v in obj]
    return obj


def buat_parser():
    p = argparse.ArgumentParser(description="Hitung THR Keagamaan + PPh 21 (Indonesia)")
    p.add_argument("--hari-raya", required=True, help="Tanggal hari raya, mis. 2027-03-10 atau 10/03/2027")
    p.add_argument("--nama-hari-raya", default="Hari Raya Keagamaan", help="mis. 'Idul Fitri 1448 H', 'Natal 2026'")
    p.add_argument("--tanggal-bayar", help="Rencana tanggal bayar (default: batas H-7)")
    p.add_argument("--hari-ini", help="Tanggal hari ini untuk cek keterlambatan (default: tanggal komputer)")
    p.add_argument("--perusahaan", default="")
    p.add_argument("--data", help="CSV karyawan")
    p.add_argument("--csv", help="Simpan rekap ke file CSV ini")
    p.add_argument("--format", choices=["teks", "json"], default="teks")
    for k in ("nama", "jabatan", "jenis", "ptkp", "gaji-pokok", "tunjangan-tetap", "mulai", "masa-kerja-bulan",
              "tanggal-berhenti", "upah-bulanan", "thr-kebijakan", "bruto-bulan-bayar", "dtp", "bruto-tetap-januari"):
        p.add_argument("--" + k)
    return p


def jalankan(args):
    hari_raya = parse_tanggal(args.hari_raya, "--hari-raya")
    batas = hari_raya - datetime.timedelta(days=7)
    bayar = parse_tanggal(args.tanggal_bayar, "--tanggal-bayar") if args.tanggal_bayar else batas
    hari_ini = parse_tanggal(args.hari_ini, "--hari-ini") if args.hari_ini else datetime.date.today()
    cfg = {"hari_raya": hari_raya, "batas_bayar": batas, "tanggal_bayar": bayar, "bulan_bayar": bayar.month,
           "nama_hari_raya": args.nama_hari_raya, "perusahaan": args.perusahaan, "peringatan": []}
    if bayar > batas:
        cfg["peringatan"].append("Rencana bayar {} melewati batas H-7 ({}). Keterlambatan dikenai denda 5% dari total "
                                 "THR (Permenaker 6/2016 Pasal 10).".format(format_tanggal(bayar), format_tanggal(batas)))
    elif hari_ini > batas:
        cfg["peringatan"].append("Hari ini ({}) sudah lewat batas bayar H-7 ({}).".format(
            format_tanggal(hari_ini), format_tanggal(batas)))
    if args.data:
        rows = baca_csv(args.data)
    else:
        if not args.nama:
            raise InputError("Isi --data karyawan.csv, atau untuk satu orang minimal --nama dan --gaji-pokok/--upah-bulanan")
        rows = [{"nama": args.nama, "jabatan": args.jabatan or "", "jenis": args.jenis or "", "ptkp": args.ptkp or "",
                 "gaji_pokok": args.gaji_pokok or "", "tunjangan_tetap": args.tunjangan_tetap or "",
                 "tanggal_mulai": args.mulai or "", "masa_kerja_bulan": args.masa_kerja_bulan or "",
                 "tanggal_berhenti": args.tanggal_berhenti or "", "upah_bulanan": args.upah_bulanan or "",
                 "thr_kebijakan": args.thr_kebijakan or "", "bruto_bulan_bayar": args.bruto_bulan_bayar or "",
                 "dtp": args.dtp or "", "bruto_tetap_januari": args.bruto_tetap_januari or ""}]
    hasil, galat = [], []
    for r in rows:
        try:
            hasil.append(hitung_karyawan(r, cfg))
        except (InputError, ValueError) as e:
            nama = r.get("nama") or "baris {}".format(r.get("_baris", "?"))
            galat.append(str(e) if str(e).startswith(nama) else "{}: {}".format(nama, e))
    return hasil, galat, cfg


def main(argv=None):
    args = buat_parser().parse_args(argv)
    try:
        hasil, galat, cfg = jalankan(args)
    except (InputError, ValueError) as e:
        print("ERROR: {}".format(e), file=sys.stderr)
        return 2
    if galat:
        print("ERROR: data berikut harus diperbaiki dulu:", file=sys.stderr)
        for g in galat:
            print("- " + g, file=sys.stderr)
        return 2
    total = {"thr": sum((h["thr"] for h in hasil), Decimal(0)),
             "pph": sum((h["pph21"].get("tambahan_pph_thr", Decimal(0)) for h in hasil if h["pph21"].get("dihitung")),
                        Decimal(0)),
             "diterima": sum((h["thr_setelah_pph"] for h in hasil), Decimal(0))}
    if args.csv:
        try:
            with open(args.csv, "w", encoding="utf-8-sig", newline="") as f:
                w = csv.writer(f, delimiter=";")
                w.writerow(["nama", "jabatan", "status", "masa_kerja_bulan", "upah_sebulan", "rumus", "thr",
                            "tambahan_pph21", "pph21_dtp", "thr_diterima", "keterangan"])
                for h in hasil:
                    p = h["pph21"]
                    w.writerow([h["nama"], h["jabatan"], h["jenis_label"], tc.angka_json(h["masa_kerja_bulan"]),
                                tc.angka_json(tc.bulat_terdekat(h["upah_sebulan"])), h["rumus"], tc.angka_json(h["thr"]),
                                tc.angka_json(p.get("tambahan_pph_thr", 0)) if p.get("dihitung") else "",
                                "ya" if p.get("dtp") else "", tc.angka_json(h["thr_setelah_pph"]), h["alasan"]])
        except OSError as e:
            print("ERROR: tidak bisa menulis {}: {}".format(args.csv, e.strerror), file=sys.stderr)
            return 2
    if args.format == "json":
        print(json.dumps(ke_json({"hari_raya": cfg["hari_raya"], "batas_bayar": cfg["batas_bayar"],
                                  "tanggal_bayar": cfg["tanggal_bayar"], "karyawan": hasil, "total": total,
                                  "peringatan_umum": cfg["peringatan"],
                                  "pengumuman": pengumuman(cfg, cfg["perusahaan"])}), ensure_ascii=False, indent=2))
    else:
        print(teks_hasil(hasil, cfg, total, args.csv))
    return 0


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8")
            sys.stderr.reconfigure(encoding="utf-8")
        except (AttributeError, ValueError):
            pass
    sys.exit(main())
