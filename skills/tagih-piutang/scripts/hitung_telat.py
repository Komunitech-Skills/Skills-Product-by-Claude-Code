#!/usr/bin/env python3
"""Hitung keterlambatan piutang, tahap penagihan, dan (opsional) denda sesuai kesepakatan tertulis.

Hanya library standar Python (3.8+). Tidak ada akses jaringan.
Versi 1.0.4 (2026-10-01).

Mode 1 – satu tagihan:
  python3 hitung_telat.py --nominal "Rp 12.500.000" --jatuh-tempo 2026-08-24 --tanggal 2026-09-23
  python3 hitung_telat.py --nominal 12500000 --dibayar "Rp 2.500.000" --jatuh-tempo 2026-08-24 \
      --denda-persen 0,1 --denda-per hari --denda-maks 5% --tenggang 3 \
      --dasar-denda "Pasal 4 Perjanjian Pasok No. 07/PKS/2026"

Mode 2 – banyak tagihan (rekap umur piutang) dari CSV atau Excel .xlsx berkolom:
  pelanggan,no_invoice,nominal,jatuh_tempo[,dibayar][,sudah_diingatkan]
  Nama kolom umum ID/EN juga diterima (mis. no_faktur, nilai_faktur, sudah_dibayar, customer,
  due_date, amount, paid, "Nilai Faktur (Rp)"); kolom lain (no_wa, tanggal_faktur, ...) diabaikan.
  Bila hanya ada kolom sisa (sisa/outstanding/balance), sisa dipakai sebagai nominal belum dibayar.
  python3 hitung_telat.py --file piutang.csv --tanggal 2026-09-23
  python3 hitung_telat.py --file piutang.xlsx --sheet Piutang --tanggal 2026-09-23
  File .xlsx dibaca dengan library standar (zipfile + xml), TANPA openpyxl/pandas: jangan pernah menginstal
  paket untuk skill ini. File .xls lama / .ods / .numbers -> minta pengguna menyimpan ulang sebagai CSV.

Aturan hitung:
  - Hari terlambat = tanggal hitung - tanggal jatuh tempo (hari kalender).
  - Hari kena denda = hari terlambat - masa tenggang (minimal 0).
  - Denda dihitung dari SISA POKOK saat ini (nominal - sudah dibayar), bukan bunga berbunga.
  - Denda per bulan: setiap 30 hari atau bagiannya dihitung 1 bulan (kecuali --proporsional).
  - Denda dibatasi --denda-maks bila diisi. Semua nilai dibulatkan ke rupiah terdekat (0,5 ke atas).
"""
import argparse
import csv
import json
import math
import re
import sys
import zipfile
import xml.etree.ElementTree as ET
from datetime import date, datetime, timedelta
from decimal import Decimal, ROUND_HALF_UP, InvalidOperation

VERSI = "1.0.4"
BULAN = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli",
         "Agustus", "September", "Oktober", "November", "Desember"]
HARI = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"]
# singkatan bulan ID/EN untuk tanggal teks seperti "25 Sep 2026" / "1 Okt 2026" / "9 Agustus 2026"
_BULAN_TEKS = {"jan": 1, "feb": 2, "peb": 2, "mar": 3, "apr": 4, "mei": 5, "may": 5, "jun": 6, "jul": 7,
               "agu": 8, "agt": 8, "ags": 8, "aug": 8, "sep": 9, "okt": 10, "oct": 10, "nov": 11, "nop": 11,
               "des": 12, "dec": 12}

# Alias nama kolom (sudah dinormalkan: huruf kecil, isi kurung dibuang, non-alfanumerik -> "_").
# Urutan = prioritas bila ada dua kolom yang cocok.
ALIAS_KOLOM = {
    "pelanggan": ["pelanggan", "nama_pelanggan", "customer", "customer_name", "klien", "client", "nama_klien",
                  "debitur", "konsumen", "nama_toko", "toko", "mitra", "nama", "name"],
    "no_invoice": ["no_invoice", "nomor_invoice", "no_faktur", "nomor_faktur", "no_inv", "invoice_no",
                   "invoice_number", "invoice", "faktur", "no_nota", "nomor_nota", "nota", "no_tagihan",
                   "nomor_tagihan", "no_dokumen", "ref", "referensi"],
    "nominal": ["nominal", "nilai_faktur", "nilai_invoice", "nilai_tagihan", "total_tagihan", "jumlah_tagihan",
                "total_faktur", "total_invoice", "tagihan", "nilai", "total", "jumlah", "grand_total",
                "amount", "invoice_amount", "total_amount"],
    "sisa": ["sisa", "sisa_tagihan", "sisa_piutang", "outstanding", "balance", "saldo", "belum_dibayar",
             "amount_due", "balance_due"],
    "jatuh_tempo": ["jatuh_tempo", "tgl_jatuh_tempo", "tanggal_jatuh_tempo", "jatuhtempo", "tgl_jt", "jt",
                    "due_date", "due", "tempo", "batas_bayar", "tanggal_tempo"],
    "dibayar": ["dibayar", "sudah_dibayar", "terbayar", "sudah_bayar", "bayar", "pembayaran", "total_dibayar",
                "jumlah_dibayar", "paid", "amount_paid", "payment"],
    "sudah_diingatkan": ["sudah_diingatkan", "diingatkan", "jumlah_pengingat", "pengingat", "reminder",
                         "reminders", "jumlah_reminder"],
}


class InputSalah(Exception):
    pass


def parse_angka(teks, nama="angka"):
    if teks is None or str(teks).strip() == "":
        raise InputSalah(f"{nama} kosong")
    s = str(teks).strip().lower().replace(" ", "")
    s = re.sub(r"[.,]-$", "", s)  # "Rp 25.000,-"
    pengali = Decimal(1)
    for akhiran, kali in (("juta", 10**6), ("jt", 10**6), ("ribu", 10**3), ("rb", 10**3), ("k", 10**3)):
        if s.endswith(akhiran):
            s = s[: -len(akhiran)]
            pengali = Decimal(kali)
            break
    s = s.replace("rp", "").replace("idr", "")
    if pengali != 1 and re.fullmatch(r"\d{1,3}(\.\d{3})+", s):
        raise InputSalah(f"{nama} ambigu: {teks!r}. Tulis tanpa titik (mis. 1500rb) atau pakai koma desimal (mis. 1,5jt)")
    if not re.fullmatch(r"-?[\d.,]+", s or "x"):
        raise InputSalah(f"{nama} tidak bisa dibaca sebagai angka: {teks!r}")
    if "," in s and "." in s:
        s = s.replace(".", "").replace(",", ".") if s.rfind(",") > s.rfind(".") else s.replace(",", "")
    elif "," in s:
        b = s.split(",")
        s = s.replace(",", ".") if len(b) == 2 and len(b[1]) != 3 else s.replace(",", "")
    elif s.count(".") > 1 or (s.count(".") == 1 and len(s.split(".")[1]) == 3 and pengali == 1):
        s = s.replace(".", "")
    try:
        return Decimal(s) * pengali
    except InvalidOperation:
        raise InputSalah(f"{nama} tidak bisa dibaca sebagai angka: {teks!r}")


# ---------------------------------------------------------------- baca .xlsx tanpa paket tambahan
_NS = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"
_NS_R = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}"
_BATAS_XML = 50 * 1024 * 1024  # tolak isi XML > 50 MB (perlindungan file rusak/zip bomb)
MINTA_CSV = ("Buka file di Excel/Google Sheets/LibreOffice lalu Simpan Sebagai (Save As) \"CSV UTF-8\", "
             "kemudian kirim file CSV-nya.")


def _xml(z, nama):
    try:
        info = z.getinfo(nama)
    except KeyError:
        return None
    if info.file_size > _BATAS_XML:
        raise InputSalah(f"file Excel terlalu besar untuk dibaca ({nama}). " + MINTA_CSV)
    data = z.read(nama)
    if b"<!DOCTYPE" in data[:2048].upper():
        raise InputSalah("file Excel berisi DOCTYPE yang tidak didukung. " + MINTA_CSV)
    return ET.fromstring(data)


def _kolom_ke_indeks(ref):
    m = re.match(r"([A-Z]+)", ref or "")
    if not m:
        return None
    n = 0
    for c in m.group(1):
        n = n * 26 + ord(c) - 64
    return n - 1


def _angka_xlsx(v):
    try:
        d = Decimal(v)
    except InvalidOperation:
        return v
    d = d.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    return str(int(d)) if d == d.to_integral_value() else str(d).replace(".", ",")


def baca_xlsx(path, sheet=None):
    """Baca satu sheet .xlsx jadi list baris (list teks). Hanya zipfile + xml.etree dari library standar."""
    try:
        z = zipfile.ZipFile(path)
    except (zipfile.BadZipFile, OSError):
        raise InputSalah("file .xlsx tidak bisa dibuka (rusak, terkunci kata sandi, atau bukan .xlsx asli). " + MINTA_CSV)
    with z:
        wb = _xml(z, "xl/workbook.xml")
        if wb is None:
            raise InputSalah("isi file .xlsx tidak dikenali. " + MINTA_CSV)
        pr = wb.find(_NS + "workbookPr")
        tahun1904 = pr is not None and pr.get("date1904") in ("1", "true")
        sheets = [(s.get("name"), s.get(_NS_R + "id")) for s in wb.iter(_NS + "sheet")]
        if not sheets:
            raise InputSalah("file .xlsx tidak berisi sheet. " + MINTA_CSV)
        if sheet:
            cocok = [x for x in sheets if (x[0] or "").strip().lower() == sheet.strip().lower()]
            if not cocok:
                raise InputSalah(f"sheet {sheet!r} tidak ada. Sheet yang tersedia: {', '.join(x[0] for x in sheets)}")
            nama_sheet, rid = cocok[0]
        else:
            nama_sheet, rid = sheets[0]
        target = None
        rels = _xml(z, "xl/_rels/workbook.xml.rels")
        if rels is not None:
            for r in rels:
                if r.get("Id") == rid:
                    target = r.get("Target", "")
        if not target:
            target = "worksheets/sheet1.xml"
        target = target.lstrip("/")
        path_sheet = target if target.startswith("xl/") else "xl/" + target
        teks_bersama = []
        ss = _xml(z, "xl/sharedStrings.xml")
        if ss is not None:
            for si in ss.iter(_NS + "si"):
                teks_bersama.append("".join(t.text or "" for t in si.iter(_NS + "t")))
        ws = _xml(z, path_sheet)
        if ws is None:
            raise InputSalah(f"sheet {nama_sheet!r} tidak bisa dibaca. " + MINTA_CSV)
        hasil = []
        for row in ws.iter(_NS + "row"):
            isi = {}
            for i_auto, c in enumerate(row.iter(_NS + "c")):
                idx = _kolom_ke_indeks(c.get("r"))
                idx = i_auto if idx is None else idx
                jenis = c.get("t", "n")
                v = c.find(_NS + "v")
                if jenis == "inlineStr":
                    el = c.find(_NS + "is")
                    nilai = "".join(t.text or "" for t in el.iter(_NS + "t")) if el is not None else ""
                elif v is None or v.text is None:
                    nilai = ""
                elif jenis == "s":
                    try:
                        nilai = teks_bersama[int(v.text)]
                    except (ValueError, IndexError):
                        nilai = ""
                elif jenis in ("str", "e"):
                    nilai = v.text
                elif jenis == "b":
                    nilai = "TRUE" if v.text == "1" else "FALSE"
                else:
                    nilai = ("n", v.text)  # angka mentah; dibedakan agar tanggal serial bisa dikenali
                isi[idx] = nilai
            if isi:
                hasil.append([isi.get(i, "") for i in range(max(isi) + 1)])
    return hasil, tahun1904


def serial_ke_tanggal(teks, tahun1904=False):
    n = float(teks)
    awal = date(1904, 1, 1) if tahun1904 else date(1899, 12, 30)
    return (awal + timedelta(days=int(n))).isoformat()


def baris_dari_xlsx(path, sheet=None):
    data, tahun1904 = baca_xlsx(path, sheet)
    data = [b for b in data if any((x[1] if isinstance(x, tuple) else str(x)).strip() for x in b)]
    if not data:
        return []
    kepala = [str(x[1] if isinstance(x, tuple) else x).strip() for x in data[0]]
    hasil = []
    for b in data[1:]:
        d = {}
        for i, k in enumerate(kepala):
            if not k:
                continue
            x = b[i] if i < len(b) else ""
            if isinstance(x, tuple):
                if peta_kolom([k]).get("jatuh_tempo") == k:
                    try:
                        x = serial_ke_tanggal(x[1], tahun1904)
                    except (ValueError, OverflowError):
                        x = x[1]
                else:
                    x = _angka_xlsx(x[1])
            d[k] = x
        hasil.append(d)
    return hasil


def parse_tgl(teks, nama):
    t = str(teks or "").strip()
    for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%d-%m-%Y", "%d.%m.%Y", "%Y/%m/%d"):
        try:
            return datetime.strptime(t, fmt).date()
        except ValueError:
            pass
    m = re.fullmatch(r"(\d{1,2})[\s\-/]+([A-Za-z]+)\.?[\s\-/,]+(\d{4})", t)
    if m and m.group(2)[:3].lower() in _BULAN_TEKS:
        try:
            return date(int(m.group(3)), _BULAN_TEKS[m.group(2)[:3].lower()], int(m.group(1)))
        except ValueError:
            pass
    raise InputSalah(f"{nama} tidak dikenali: {teks!r}. Pakai format YYYY-MM-DD (mis. 2026-09-23), "
                     "DD/MM/YYYY, atau '23 Sep 2026'")


def normal_kolom(nama):
    t = re.sub(r"\(.*?\)", "", str(nama or "").strip().lower())
    return re.sub(r"[^0-9a-z]+", "_", t).strip("_")


def peta_kolom(nama_kolom):
    """{kanonik: nama kolom asli} dari daftar nama kolom file, memakai ALIAS_KOLOM."""
    normal = {}
    for k in nama_kolom:
        if k is None:
            continue
        n = normal_kolom(k)
        if n and n not in normal:
            normal[n] = k
    peta = {}
    dipakai = set()
    for kanon, alias in ALIAS_KOLOM.items():
        for a in alias:
            if a in normal and normal[a] not in dipakai:
                peta[kanon] = normal[a]
                dipakai.add(normal[a])
                break
    return peta


def tgl_hari(d):
    return f"{HARI[d.weekday()]}, {tgl_id(d)}"


def bulat(x):
    return int(Decimal(x).quantize(Decimal("1"), rounding=ROUND_HALF_UP))


def rupiah(n):
    return ("-" if n < 0 else "") + f"Rp {abs(int(n)):,}".replace(",", ".")


def tgl_id(d):
    return f"{d.day} {BULAN[d.month - 1]} {d.year}"


def tahap(hari):
    """Kembalikan (kode, label) tahap penagihan berdasarkan hari terlambat (negatif = sebelum jatuh tempo)."""
    if hari < -3:
        return 0, f"Belum jatuh tempo ({-hari} hari lagi) – kirim pengingat halus pada H-3"
    if hari < 0:
        return 1, f"Tahap 1 – pengingat halus sebelum jatuh tempo (H{hari})"
    if hari == 0:
        return 2, "Tahap 2 – hari jatuh tempo"
    if hari < 7:
        return 3, f"Tahap 3 – lewat jatuh tempo {hari} hari (konfirmasi ramah)"
    if hari < 14:
        return 4, f"Tahap 4 – lewat {hari} hari (pengingat tegas + minta tanggal bayar)"
    if hari < 30:
        return 5, f"Tahap 5 – lewat {hari} hari (pemberitahuan resmi + tawaran solusi/cicilan)"
    return 6, f"Tahap 6 – lewat {hari} hari (surat teguran resmi/somasi)"


def sesuaikan_riwayat(kode, label, hari, sudah_diingatkan):
    """Jangan langsung somasi bila belum pernah diingatkan. Kembalikan (kode, label, pesan_pembatasan|None)."""
    if sudah_diingatkan < 0:
        raise InputSalah("jumlah pengingat yang sudah dikirim tidak boleh negatif")
    maks = {0: 5 if hari >= 30 else 4, 1: 5}.get(sudah_diingatkan, 6)
    if kode <= maks:
        return kode, label, None
    nama = {4: f"Tahap 4 – lewat {hari} hari, belum pernah diingatkan (pengingat tegas + minta tanggal bayar)",
            5: f"Tahap 5 – lewat {hari} hari, pengingat sebelumnya {sudah_diingatkan}x (pemberitahuan resmi + tawaran solusi/cicilan)"}
    return maks, nama[maks], (f"Menurut umur piutang seharusnya {label.split(' (')[0]}, tetapi baru {sudah_diingatkan} pengingat "
                              f"terkirim. Mulai dari tahap {maks}; naikkan satu tahap bila 7 hari tanpa respons.")


def jadwal_berikutnya(kode, jt, tgl, hubungan):
    """Kalimat jadwal yang jelas: tenggat bayar yang diusulkan di pesan ini dan kapan tahap berikutnya dikirim.
    Jeda antartahap: 7 hari (bisnis) atau 14 hari (hubungan dekat: tetangga/kenalan/keluarga/pelanggan perorangan
    langganan). Tidak pernah menyarankan naik tahap kurang dari jeda itu."""
    jeda = 14 if hubungan == "dekat" else 7
    if kode < 0:
        return {"jeda_hari": jeda, "tenggat_bayar": None, "kirim_berikutnya": None, "kalimat": "Lunas – tidak ada tahap berikutnya."}
    if kode <= 2:
        nxt = {0: jt - timedelta(days=3), 1: jt, 2: jt + timedelta(days=3)}[kode]
        isi = {0: "tahap 1 (pengingat halus H-3)", 1: "tahap 2 (hari jatuh tempo)",
               2: "tahap 3 (konfirmasi ramah) bila belum ada pembayaran"}[kode]
        return {"jeda_hari": jeda, "tenggat_bayar": jt.isoformat(), "kirim_berikutnya": nxt.isoformat(),
                "kalimat": f"Kirim {isi} pada {tgl_hari(nxt)}."}
    tenggat = tgl + timedelta(days=jeda)
    kirim = tenggat + timedelta(days=1)
    if kode >= 6:
        lanjut = "konsultasikan ke advokat (mis. gugatan sederhana) — jangan kirim ancaman lain"
    elif hubungan == "dekat" and kode >= 3:
        lanjut = (f"ajak bicara langsung dulu; bila tetap belum ada kabar, kirim tahap {kode + 1} "
                  "(tetap dengan nada kekeluargaan)")
    else:
        lanjut = f"kirim tahap {kode + 1}"
    return {"jeda_hari": jeda, "tenggat_bayar": tenggat.isoformat(), "kirim_berikutnya": kirim.isoformat(),
            "kalimat": (f"Tenggat bayar di pesan ini: {tgl_hari(tenggat)} ({jeda} hari dari {tgl_id(tgl)}). "
                        f"Jika sampai tanggal itu belum ada pembayaran atau kabar, pada {tgl_hari(kirim)} {lanjut}.")}


def ember_umur(hari):
    if hari <= 0:
        return "Belum jatuh tempo"
    if hari <= 30:
        return "1–30 hari"
    if hari <= 60:
        return "31–60 hari"
    if hari <= 90:
        return "61–90 hari"
    return "> 90 hari"


def baca_denda_maks(teks, sisa):
    """'5%' -> 5% dari sisa pokok; 'Rp 500.000' / '500rb' / '500000' -> nominal. Tolak yang kemungkinan salah ketik."""
    t = str(teks).strip()
    if t.endswith("%"):
        p = parse_angka(t[:-1], "batas denda")
        if p <= 0 or p > 100:
            raise InputSalah("batas denda dalam persen harus di atas 0 dan maksimal 100%")
        return Decimal(sisa) * p / 100
    n = parse_angka(t, "batas denda")
    ada_satuan = bool(re.search(r"(?i)rp|idr|rb|ribu|jt|juta|k$", t))
    if n <= 100 and not ada_satuan:
        raise InputSalah(f"batas denda {t!r} ambigu: maksud Anda {t}% atau Rp {t}? Tulis dengan '%' atau 'Rp'.")
    if n < 1000:
        raise InputSalah(f"batas denda {t!r} kurang dari Rp 1.000 — kemungkinan salah ketik. "
                         "Tulis sebagai persen (mis. 5%) atau nominal lengkap (mis. Rp 500.000).")
    return n


def hitung_denda(sisa, hari_denda, a):
    if not a.denda_persen and not a.denda_tetap:
        return 0, None
    if a.denda_persen and a.denda_tetap:
        raise InputSalah("pilih salah satu: --denda-persen ATAU --denda-tetap")
    if hari_denda <= 0 or sisa <= 0:
        return 0, "Belum ada denda (masih dalam masa tenggang / belum terlambat / sudah lunas)."
    if a.denda_tetap:
        d = parse_angka(a.denda_tetap, "denda tetap")
        if d < 0:
            raise InputSalah("denda tetap tidak boleh negatif")
        denda = Decimal(d)
        rumus = f"Denda tetap sekali {rupiah(bulat(d))}"
    else:
        p = parse_angka(str(a.denda_persen).rstrip("%"), "persen denda")
        if p < 0 or p > 100:
            raise InputSalah("persen denda harus 0–100")
        harian = p if a.denda_per == "hari" else p / 30
        if harian > 1 and not a.konfirmasi_denda_tinggi:
            raise InputSalah(f"denda {format(p.normalize(), 'f').replace('.', ',')}% per {a.denda_per} sangat tinggi "
                             f"(setara > 1% per hari). Kemungkinan salah ketik (mis. 0,100 dibaca 0,1 atau 100?). "
                             "Cek angka di perjanjian; jika memang benar, ulangi dengan --konfirmasi-denda-tinggi.")
        if a.denda_per == "hari":
            periode = Decimal(hari_denda)
            satuan = f"{hari_denda} hari"
        else:
            periode = Decimal(hari_denda) / 30 if a.proporsional else Decimal(math.ceil(hari_denda / 30))
            satuan = (f"{hari_denda}/30 bulan" if a.proporsional else f"{int(periode)} bulan (per 30 hari atau bagiannya)")
        denda = Decimal(sisa) * p / 100 * periode
        rumus = f"{rupiah(sisa)} x {format(p.normalize(), 'f').replace('.', ',')}% x {satuan}"
    if a.denda_maks:
        maks = baca_denda_maks(a.denda_maks, sisa)
        if denda > maks:
            denda = maks
            rumus += f" → dibatasi maksimal {rupiah(bulat(maks))}"
    return bulat(denda), rumus


def satu(a, tgl):
    nominal = bulat(parse_angka(a.nominal, "nominal tagihan"))
    if nominal <= 0:
        raise InputSalah("nominal tagihan harus lebih dari 0")
    dibayar = sum(bulat(parse_angka(x, "pembayaran")) for x in (a.dibayar or []))
    if dibayar < 0:
        raise InputSalah("pembayaran tidak boleh negatif")
    if dibayar > nominal:
        raise InputSalah(f"total pembayaran ({rupiah(dibayar)}) melebihi nominal tagihan ({rupiah(nominal)})")
    jt = parse_tgl(a.jatuh_tempo, "tanggal jatuh tempo")
    if a.tenggang < 0:
        raise InputSalah("masa tenggang tidak boleh negatif")
    hari = (tgl - jt).days
    sisa = nominal - dibayar
    hari_denda = max(0, hari - a.tenggang)
    denda, rumus = hitung_denda(sisa, hari_denda, a)
    kode, label = tahap(hari)
    kode, label, dibatasi = sesuaikan_riwayat(kode, label, hari, a.sudah_diingatkan)
    peringatan = []
    if dibatasi:
        peringatan.append(dibatasi)
    if sisa == 0:
        label, kode = "Lunas – kirim ucapan terima kasih, tidak perlu penagihan", -1
    if (a.denda_persen or a.denda_tetap) and not a.dasar_denda:
        peringatan.append("Denda HANYA boleh ditagih jika sudah disepakati tertulis (kontrak/invoice/PO yang disetujui). "
                          "Isi --dasar-denda; jika tidak ada kesepakatan, jangan cantumkan denda di pesan.")
    if denda and denda > sisa:
        peringatan.append("Denda melebihi sisa pokok. Periksa kembali persen & batas denda di perjanjian; "
                          "denda yang berlebihan berisiko dipersoalkan/dikurangi hakim.")
    if a.hubungan == "dekat" and kode >= 5:
        peringatan.append("Hubungan dekat (tetangga/kenalan/keluarga): sebelum pemberitahuan resmi/surat, ajak bicara "
                          "langsung dulu; pesan tertulis tetap bernada kekeluargaan.")
    if kode == 6 and sisa >= 5_000_000:
        peringatan.append("Nilai besar & lewat 30 hari: pertimbangkan surat teguran resmi dan konsultasi ke advokat "
                          "bila tidak ada respons.")
    return {
        "nominal": nominal, "sudah_dibayar": dibayar, "sisa_tagihan": sisa,
        "jatuh_tempo": jt.isoformat(), "jatuh_tempo_teks": tgl_id(jt),
        "tanggal_hitung": tgl.isoformat(), "tanggal_hitung_teks": tgl_id(tgl),
        "hari_terlambat": hari, "masa_tenggang_hari": a.tenggang, "hari_kena_denda": hari_denda,
        "sudah_diingatkan": a.sudah_diingatkan,
        "tahap_kode": kode, "tahap": label,
        "denda": denda, "rumus_denda": rumus, "dasar_denda": a.dasar_denda,
        "total_ditagih": sisa + denda,
        "hubungan": a.hubungan,
        "jadwal": jadwal_berikutnya(kode, jt, tgl, a.hubungan),
        "peringatan": peringatan,
        "catatan": ["Hari terlambat dihitung per hari kalender.",
                    "Denda (jika ada) dihitung dari sisa pokok, dibulatkan ke rupiah terdekat."],
    }


def banyak(a, tgl):
    ext = a.file.lower().rsplit(".", 1)[-1] if "." in a.file else ""
    if ext in ("xls", "ods", "numbers", "xlsb"):
        raise InputSalah(f"format .{ext} tidak bisa dibaca tanpa menginstal paket (dan paket tidak boleh diinstal). "
                         + MINTA_CSV)
    try:
        with open(a.file, "rb") as f:
            zip_asli = f.read(4) == b"PK\x03\x04"
    except OSError as e:
        raise InputSalah(f"file tidak bisa dibuka: {e}")
    if ext in ("xlsx", "xlsm") or zip_asli:
        baris = baris_dari_xlsx(a.file, a.sheet)
    else:
        baris = baca_csv(a.file)
    return olah_baris(baris, tgl)


def baca_csv(path):
    try:
        with open(path, newline="", encoding="utf-8-sig") as f:
            contoh = f.read(4096)
            f.seek(0)
            try:
                dialek = csv.Sniffer().sniff(contoh, delimiters=",;\t|")
            except csv.Error:
                dialek = csv.excel
            return list(csv.DictReader(f, dialect=dialek))
    except OSError as e:
        raise InputSalah(f"file tidak bisa dibuka: {e}")
    except UnicodeDecodeError:
        raise InputSalah("encoding file tidak dikenali. " + MINTA_CSV)


def olah_baris(baris, tgl):
    if not baris:
        raise InputSalah("file kosong")
    asli = [k for k in baris[0].keys() if k]
    peta = peta_kolom(asli)
    kurang = [k for k in ("pelanggan", "jatuh_tempo") if k not in peta]
    if "nominal" not in peta and "sisa" not in peta:
        kurang.insert(1, "nominal")
    if kurang:
        contoh = {"pelanggan": "pelanggan / nama_pelanggan / customer / klien",
                  "nominal": "nominal / nilai_faktur / total / jumlah / amount (atau kolom sisa / outstanding)",
                  "jatuh_tempo": "jatuh_tempo / tgl_jatuh_tempo / due_date"}
        raise InputSalah("kolom wajib tidak ditemukan: " + "; ".join(f"{k} (nama yang dikenali: {contoh[k]})" for k in kurang)
                         + f". Kolom di file: {', '.join(str(x) for x in asli)}. Ganti nama judul kolom yang sesuai "
                         "di file, lalu jalankan ulang.")
    # kolom sisa dipakai bila tidak ada nominal, atau ada nominal tanpa kolom pembayaran (agar cicilan tidak hilang)
    pakai_sisa = "sisa" in peta and ("nominal" not in peta or "dibayar" not in peta)
    daftar, dilewati = [], []
    for no, b in enumerate(baris, start=2):
        mentah = {x: (v if isinstance(v, str) else ("" if v is None else str(v))).strip() for x, v in b.items() if x}
        if not any(mentah.values()):
            continue
        k = {kanon: mentah.get(asal, "") for kanon, asal in peta.items()}
        try:
            if pakai_sisa:
                nominal = bulat(parse_angka(k["sisa"], "sisa"))
                dibayar = 0
                if nominal == 0:
                    continue
            else:
                nominal = bulat(parse_angka(k["nominal"], "nominal"))
                dibayar = bulat(parse_angka(k["dibayar"], "dibayar")) if k.get("dibayar") else 0
            ingat_teks = k.get("sudah_diingatkan", "")
            if ingat_teks and not ingat_teks.isdigit():
                raise InputSalah(f"sudah_diingatkan harus angka bulat: {ingat_teks!r}")
            ingat = int(ingat_teks) if ingat_teks else 0
            jt = parse_tgl(k["jatuh_tempo"], "jatuh_tempo")
            if nominal <= 0 or dibayar < 0 or dibayar > nominal:
                raise InputSalah("nominal/dibayar tidak masuk akal")
        except InputSalah as e:
            dilewati.append({"baris": no, "alasan": str(e)})
            continue
        hari = (tgl - jt).days
        sisa = nominal - dibayar
        if sisa == 0:
            continue
        kode, label = tahap(hari)
        kode, label, _ = sesuaikan_riwayat(kode, label, hari, ingat)
        daftar.append({"pelanggan": k["pelanggan"], "no_invoice": k.get("no_invoice", ""), "sisa": sisa,
                       "jatuh_tempo": jt.isoformat(), "hari_terlambat": hari, "umur": ember_umur(hari),
                       "tahap_kode": kode, "tahap": label})
    daftar.sort(key=lambda x: (-x["hari_terlambat"], -x["sisa"]))
    urutan = ["Belum jatuh tempo", "1–30 hari", "31–60 hari", "61–90 hari", "> 90 hari"]
    rekap = {u: {"jumlah_invoice": 0, "total": 0} for u in urutan}
    for d in daftar:
        rekap[d["umur"]]["jumlah_invoice"] += 1
        rekap[d["umur"]]["total"] += d["sisa"]
    telat = [d for d in daftar if d["hari_terlambat"] > 0]
    return {"tanggal_hitung": tgl.isoformat(), "tanggal_hitung_teks": tgl_id(tgl),
            "ringkasan_grup": ringkasan_grup(tgl, daftar, telat),
            "total_piutang": sum(d["sisa"] for d in daftar),
            "total_telat": sum(d["sisa"] for d in telat), "jumlah_invoice_telat": len(telat),
            "rekap_umur": rekap, "kolom_dipakai": peta,
            "catatan_kolom": (f"Kolom {peta['sisa']!r} dipakai sebagai jumlah yang belum dibayar."
                              if pakai_sisa else None),
            "daftar": daftar, "baris_dilewati": dilewati}


def ringkasan_grup(tgl, daftar, telat):
    """Teks aman untuk grup/tim: hanya jumlah faktur & total (agregat), TANPA nama pelanggan, nomor invoice,
    nomor HP, atau sisa per pelanggan. Data per pelanggan tetap khusus pemilik/admin keuangan."""
    b = [f"Rekap piutang per {tgl_id(tgl)}:",
         f"- Faktur belum lunas: {len(daftar)}, total {rupiah(sum(d['sisa'] for d in daftar))}",
         f"- Sudah lewat jatuh tempo: {len(telat)} faktur, total {rupiah(sum(d['sisa'] for d in telat))}"]
    if telat:
        b.append(f"- Paling lama terlambat: {max(d['hari_terlambat'] for d in telat)} hari")
    b.append("Penagihan sedang ditindaklanjuti oleh bagian keuangan; rincian per pelanggan tidak dibagikan di grup.")
    return "\n".join(b)


def teks_satu(h):
    b = [f"Tagihan         : {rupiah(h['nominal'])}"]
    if h["sudah_dibayar"]:
        b.append(f"Sudah dibayar   : {rupiah(h['sudah_dibayar'])}")
    b.append(f"Sisa tagihan    : {rupiah(h['sisa_tagihan'])}")
    b.append(f"Jatuh tempo     : {h['jatuh_tempo_teks']}")
    b.append(f"Dihitung per    : {h['tanggal_hitung_teks']}")
    ht = h["hari_terlambat"]
    b.append(f"Keterlambatan   : {ht} hari" if ht > 0 else
             (f"Keterlambatan   : jatuh tempo hari ini" if ht == 0 else f"Keterlambatan   : belum jatuh tempo ({-ht} hari lagi)"))
    b.append(f"Tahap           : {h['tahap']}")
    if h["rumus_denda"]:
        b.append(f"Denda           : {rupiah(h['denda'])}  ({h['rumus_denda']})")
        if h["dasar_denda"]:
            b.append(f"Dasar denda     : {h['dasar_denda']}")
    b.append(f"TOTAL DITAGIH   : {rupiah(h['total_ditagih'])}")
    b.append(f"Jadwal          : {h['jadwal']['kalimat']}")
    for p in h["peringatan"]:
        b.append(f"\nPERINGATAN: {p}")
    b.append("")
    b += [f"* {c}" for c in h["catatan"]]
    return "\n".join(b)


def teks_banyak(h):
    b = [f"Rekap umur piutang per {h['tanggal_hitung_teks']} – total {rupiah(h['total_piutang'])}",
         f"Sudah lewat jatuh tempo: {h['jumlah_invoice_telat']} invoice, total {rupiah(h['total_telat'])}",
         "Kolom dipakai: " + ", ".join(f"{k}={v}" for k, v in h["kolom_dipakai"].items()), ""]
    if h.get("catatan_kolom"):
        b.insert(-1, "Catatan: " + h["catatan_kolom"])
    b += ["| Umur | Jumlah invoice | Total |", "|---|---|---|"]
    for u, v in h["rekap_umur"].items():
        b.append(f"| {u} | {v['jumlah_invoice']} | {rupiah(v['total'])} |")
    b += ["", "| Pelanggan | No. invoice | Sisa | Jatuh tempo | Terlambat | Tahap |", "|---|---|---|---|---|---|"]
    for d in h["daftar"]:
        t = f"{d['hari_terlambat']} hari" if d["hari_terlambat"] > 0 else "-"
        b.append(f"| {d['pelanggan']} | {d['no_invoice'] or '-'} | {rupiah(d['sisa'])} | {d['jatuh_tempo']} | {t} | {d['tahap']} |")
    if h["baris_dilewati"]:
        b.append("\nBaris dilewati:")
        b += [f"- baris {x['baris']}: {x['alasan']}" for x in h["baris_dilewati"]]
    b += ["", "### Ringkasan aman untuk grup (tanpa nama pelanggan — salin blok ini saja ke grup/tim)", "```",
          h["ringkasan_grup"], "```",
          "(Tabel per pelanggan di atas KHUSUS pemilik/admin keuangan — jangan ditempel ke grup.)"]
    return "\n".join(b)


def main():
    p = argparse.ArgumentParser(description="Hitung keterlambatan piutang & denda (sesuai kesepakatan tertulis)", allow_abbrev=False)
    p.add_argument("--nominal", help="Nominal tagihan, mis. 'Rp 12.500.000'")
    p.add_argument("--dibayar", action="append", help="Pembayaran sebagian (bisa diulang)")
    p.add_argument("--jatuh-tempo", help="Tanggal jatuh tempo YYYY-MM-DD")
    p.add_argument("--tanggal", help="Tanggal hitung YYYY-MM-DD (default hari ini)")
    p.add_argument("--tenggang", type=int, default=0, help="Masa tenggang tanpa denda (hari), default 0")
    p.add_argument("--denda-persen", help="Persen denda per periode, mis. 0,1 (artinya 0,1%%)")
    p.add_argument("--denda-per", choices=["hari", "bulan"], default="hari")
    p.add_argument("--proporsional", action="store_true", help="Denda bulanan dihitung proporsional per hari")
    p.add_argument("--denda-tetap", help="Denda tetap sekali bayar, mis. 'Rp 100.000'")
    p.add_argument("--denda-maks", help="Batas maksimal denda: '5%%' dari sisa pokok atau 'Rp 500.000'")
    p.add_argument("--sudah-diingatkan", type=int, default=0,
                   help="Jumlah pengingat yang SUDAH dikirim untuk tagihan ini (default 0 = belum pernah)")
    p.add_argument("--konfirmasi-denda-tinggi", action="store_true",
                   help="Konfirmasi bahwa denda > 1%%/hari memang sesuai perjanjian")
    p.add_argument("--hubungan", choices=["bisnis", "dekat"], default="bisnis",
                   help="dekat = tetangga/kenalan/keluarga/pelanggan perorangan langganan: jeda antartahap 14 hari "
                        "(bisnis: 7 hari)")
    p.add_argument("--dasar-denda", help="Rujukan kesepakatan tertulis, mis. 'Pasal 4 Perjanjian No. ...'")
    p.add_argument("--file", help="CSV atau .xlsx banyak tagihan: pelanggan,no_invoice,nominal,jatuh_tempo,dibayar,sudah_diingatkan")
    p.add_argument("--sheet", help="Nama sheet untuk file .xlsx (default: sheet pertama)")
    p.add_argument("--format", choices=["teks", "json", "keduanya"], default="keduanya")
    a = p.parse_args()
    try:
        tgl = parse_tgl(a.tanggal, "tanggal hitung") if a.tanggal else date.today()
        if a.file:
            h = banyak(a, tgl)
            tulis = teks_banyak
        else:
            if not a.nominal or not a.jatuh_tempo:
                raise InputSalah("isi --nominal dan --jatuh-tempo (atau pakai --file untuk banyak tagihan)")
            h = satu(a, tgl)
            tulis = teks_satu
    except InputSalah as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)
    if a.format in ("teks", "keduanya"):
        print(tulis(h))
    if a.format == "keduanya":
        print("\n--- JSON ---")
    if a.format in ("json", "keduanya"):
        print(json.dumps(h, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
