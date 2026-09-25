#!/usr/bin/env python3
"""Pemeriksa rincian penawaran harga tender/pengadaan pemerintah + jadwal mundur.

Hanya library standar Python 3.8+. Tanpa akses jaringan. Lintas OS
(macOS/Linux: python3, Windows: py atau python).

1) Cek rincian harga (volume x harga satuan, subtotal, PPN, total, terbilang, % HPS):
     python3 cek_penawaran.py harga rincian.csv --ppn nonmewah --hps "Rp 250.000.000"
   Kolom CSV (judul kolom boleh bervariasi): uraian, volume, satuan, harga satuan.
   Kolom opsional: no, harga satuan hps.
   Pemisah ; , tab atau | dikenali otomatis. Format angka "Rp1.250.000,00", "1,5", "1.500" diterima.

2) Jadwal mundur dari batas akhir unggah penawaran (hari kerja):
     python3 cek_penawaran.py jadwal --batas "2026-10-15 14:00" \
       --penjelasan 2026-10-06 --libur 2026-10-12 --hari-ini 2026-09-25

Aturan pembulatan (standar Komunitech):
  - Jumlah per baris = volume x harga satuan, dibulatkan ke rupiah terdekat (0,5 naik).
  - PPN dihitung persis dari DPP lalu DIBULATKAN KE BAWAH sekali.
    Non-mewah: 12% x (11/12 x DPP) = 11% x DPP. Mewah: 12% x DPP.
  - Harga termasuk PPN: DPP = rupiah bulat terbesar dengan DPP + PPN <= harga; sisa ditampilkan.
  - Belum dicocokkan dengan Coretax / aplikasi SPSE.
"""
import argparse
import csv
import io
import json
import re
import sys
from datetime import date, datetime, timedelta
from decimal import Decimal, ROUND_HALF_UP, ROUND_FLOOR, InvalidOperation
from fractions import Fraction

TARIF = {"nonmewah": Fraction(11, 100), "mewah": Fraction(12, 100), "tidak": Fraction(0)}
BATAS_KEWAJARAN = Decimal("80")          # % HPS -> klarifikasi kewajaran harga
BATAS_JAMINAN_PENAWARAN = 10_000_000_000  # HPS > Rp10 miliar -> jaminan penawaran (cek dokumen)
BATAS_PAKET_UMK = 15_000_000_000          # pagu s.d. Rp15 miliar -> dicadangkan UMK & koperasi
HARI = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"]
BULAN = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus",
         "September", "Oktober", "November", "Desember"]
POLA_TOTAL = re.compile(r"^\s*(sub\s*-?\s*total|total|grand\s*total|jumlah(\s+total|\s+harga|\s+akhir)?|"
                        r"ppn|pajak|dpp|terbilang|dibulatkan|pembulatan)\b", re.I)


class InputSalah(Exception):
    pass


# ---------------------------------------------------------------- angka
def parse_angka(teks, nama="angka"):
    """'Rp1.250.000,00' -> 1250000 ; '1,5' -> 1.5 ; '1.500' -> 1500 ; '2.5' -> 2.5 ; '15,000.50' -> 15000.5"""
    if teks is None or str(teks).strip() == "":
        raise InputSalah(f"{nama} kosong")
    s = str(teks).strip().lower().replace(" ", "").replace("\u00a0", "")
    s = re.sub(r"[.,]-+$", "", s)          # "Rp 25.000,-"
    s = s.replace("rp.", "").replace("rp", "").replace("idr", "")
    pengali = Decimal(1)
    for akhiran, kali in (("juta", 10**6), ("jt", 10**6), ("ribu", 10**3), ("rb", 10**3)):
        if s.endswith(akhiran):
            s, pengali = s[: -len(akhiran)], Decimal(kali)
            break
    if not re.fullmatch(r"-?[\d.,]+", s or "x") or not re.search(r"\d", s):
        raise InputSalah(f"{nama} tidak bisa dibaca sebagai angka: {teks!r}")
    if "," in s and "." in s:
        if s.rfind(",") > s.rfind("."):
            s = s.replace(".", "").replace(",", ".")   # 1.250.000,50
        else:
            s = s.replace(",", "")                     # 1,250,000.50
    elif "," in s:
        bagian = s.split(",")
        if len(bagian) == 2 and len(bagian[1]) != 3:
            s = s.replace(",", ".")                    # 1,5 / 1250000,00
        elif len(bagian) == 2 and pengali != 1:
            s = s.replace(",", ".")                    # 1,250jt -> 1.25 juta
        else:
            s = s.replace(",", "")                     # 1,250,000
    elif s.count(".") > 1 or (s.count(".") == 1 and len(s.split(".")[1]) == 3 and pengali == 1):
        s = s.replace(".", "")                         # 1.250.000 / 1.500
    try:
        return Decimal(s) * pengali
    except InvalidOperation:
        raise InputSalah(f"{nama} tidak bisa dibaca sebagai angka: {teks!r}")


def bulat(x):
    if isinstance(x, Fraction):
        x = Decimal(x.numerator) / Decimal(x.denominator)
    return int(Decimal(x).quantize(Decimal("1"), rounding=ROUND_HALF_UP))


def ppn_bawah(dpp, tarif):
    """PPN persis dari DPP lalu dibulatkan ke bawah sekali."""
    p = Fraction(dpp) * tarif
    return p.numerator // p.denominator


def dpp_dari_bruto(bruto, tarif):
    """DPP bulat terbesar dengan DPP + PPN <= bruto."""
    if tarif == 0:
        return bruto
    d = int(Fraction(bruto) / (1 + tarif))
    while d + 1 + ppn_bawah(d + 1, tarif) <= bruto:
        d += 1
    while d > 0 and d + ppn_bawah(d, tarif) > bruto:
        d -= 1
    return d


def rupiah(n):
    s = f"{abs(int(n)):,}".replace(",", ".")
    return ("-Rp" if n < 0 else "Rp") + s


def angka_id(d):
    d = Decimal(d).normalize()
    if d == d.to_integral_value():
        return f"{int(d):,}".replace(",", ".")
    bulatnya, pecahan = f"{d:f}".split(".")
    return f"{int(bulatnya):,}".replace(",", ".") + "," + pecahan


def persen_id(p):
    return f"{p:.2f}".replace(".", ",") + "%"


def terbilang(n):
    satuan = ["", "satu", "dua", "tiga", "empat", "lima", "enam", "tujuh", "delapan",
              "sembilan", "sepuluh", "sebelas"]

    def t(x):
        if x < 12:
            return satuan[x]
        if x < 20:
            return t(x - 10) + " belas"
        if x < 100:
            return (t(x // 10) + " puluh " + t(x % 10)).strip()
        if x < 200:
            return ("seratus " + t(x - 100)).strip()
        if x < 1000:
            return (t(x // 100) + " ratus " + t(x % 100)).strip()
        if x < 2000:
            return ("seribu " + t(x - 1000)).strip()
        for besar, nama in ((10**12, "triliun"), (10**9, "miliar"), (10**6, "juta"), (10**3, "ribu")):
            if x >= besar:
                return (t(x // besar) + f" {nama} " + t(x % besar)).strip()
        return ""

    if n == 0:
        return "Nol Rupiah"
    hasil = re.sub(r"\s+", " ", t(abs(int(n)))).strip()
    return ("Minus " if n < 0 else "") + hasil.title() + " Rupiah"


# ---------------------------------------------------------------- baca CSV
KUNCI_KOLOM = {
    "no": ("no", "no.", "nomor", "#"),
    "uraian": ("uraian", "uraian pekerjaan", "uraian barang", "nama barang", "nama", "item",
               "barang", "jenis barang", "pekerjaan", "deskripsi", "spesifikasi", "description"),
    "volume": ("volume", "vol", "vol.", "qty", "kuantitas", "jumlah barang", "banyak", "kuantum"),
    "satuan": ("satuan", "sat", "sat.", "unit", "uom"),
    "harga": ("harga satuan", "harga", "harga satuan (rp)", "harga (rp)", "unit price", "harga penawaran"),
    "hps": ("harga satuan hps", "hps satuan", "hps", "harga hps"),
}


def _norm(s):
    return re.sub(r"\s+", " ", (s or "").strip().lower().replace("_", " "))


def kenali_header(baris):
    peta = {}
    for i, sel in enumerate(baris):
        n = _norm(sel)
        n2 = re.sub(r"\(.*?\)", "", n).strip()
        for kunci, sinonim in KUNCI_KOLOM.items():
            if kunci in peta:
                continue
            if n in sinonim or n2 in sinonim:
                peta[kunci] = i
                break
    if "uraian" in peta and ("volume" in peta or "harga" in peta):
        return peta
    return None


def baca_teks(path):
    if path == "-":
        return sys.stdin.read()
    try:
        with open(path, "rb") as f:
            data = f.read()
    except OSError as e:
        raise InputSalah(f"file tidak bisa dibuka: {path} ({e.strerror})")
    for enc in ("utf-8-sig", "cp1252", "latin-1"):
        try:
            return data.decode(enc)
        except UnicodeDecodeError:
            continue
    raise InputSalah("encoding file tidak dikenali; simpan ulang sebagai CSV UTF-8")


def tebak_pemisah(teks):
    contoh = [b for b in teks.splitlines()[:15] if b.strip()]
    skor = {}
    for p in (";", "\t", "|", ","):
        jml = [b.count(p) for b in contoh]
        if jml and min(jml) > 0:
            skor[p] = min(jml)
    for p in (";", "\t", "|"):   # utamakan pemisah yang tidak bentrok dengan desimal koma
        if p in skor:
            return p
    return "," if "," in skor else ";"


def perbaiki_koma(sel, lebar):
    """Pemisah koma + angka 'Rp1.250.000,00' tanpa tanda kutip terpecah jadi 2 sel. Gabungkan kembali."""
    sel = list(sel)
    i = 1
    while len(sel) > lebar and i < len(sel):
        if re.fullmatch(r"\d{1,2}", sel[i].strip()) and re.search(r"\d\.\d{3}\s*$", sel[i - 1]):
            sel[i - 1] = sel[i - 1] + "," + sel[i]
            del sel[i]
        else:
            i += 1
    return sel


def baca_rincian(path):
    teks = baca_teks(path)
    if not teks.strip():
        raise InputSalah("file kosong")
    pemisah = tebak_pemisah(teks)
    semua = list(csv.reader(io.StringIO(teks), delimiter=pemisah))
    peta, mulai = None, 0
    for i, b in enumerate(semua[:15]):
        peta = kenali_header(b)
        if peta:
            mulai = i + 1
            break
    catatan = []
    if not peta:
        # tanpa judul kolom: tebak urutan
        contoh = next((b for b in semua if any(x.strip() for x in b)), [])
        if len(contoh) >= 5 and re.fullmatch(r"\d+\.?", contoh[0].strip() or "x"):
            peta = {"no": 0, "uraian": 1, "volume": 2, "satuan": 3, "harga": 4}
        else:
            peta = {"uraian": 0, "volume": 1, "satuan": 2, "harga": 3}
        catatan.append("Judul kolom tidak ditemukan; dianggap urutan: " +
                       ", ".join(k for k, _ in sorted(peta.items(), key=lambda x: x[1])) + ".")
    for wajib in ("volume", "harga"):
        if wajib not in peta:
            raise InputSalah(f"kolom '{wajib}' tidak ditemukan. Judul kolom yang dikenali: uraian, volume, satuan, harga satuan")
    lebar = max(peta.values()) + 1
    return semua[mulai:], peta, lebar, pemisah, catatan, mulai


def ambil(sel, peta, kunci):
    i = peta.get(kunci)
    return sel[i].strip() if i is not None and i < len(sel) else ""


def hitung(path, ppn="tidak", termasuk_ppn=False, hps=None, pagu=None):
    baris_data, peta, lebar, pemisah, catatan, offset = baca_rincian(path)
    item, dilewati, masalah, total_tertempel = [], [], [], []
    for no_file, sel in enumerate(baris_data, start=offset + 1):
        if not any(x.strip() for x in sel):
            continue
        if len(sel) > lebar and pemisah == ",":
            sel = perbaiki_koma(sel, lebar)
        uraian = ambil(sel, peta, "uraian")
        vol_t, sat, harga_t = ambil(sel, peta, "volume"), ambil(sel, peta, "satuan"), ambil(sel, peta, "harga")
        hps_t = ambil(sel, peta, "hps")
        if POLA_TOTAL.match(uraian) or (not uraian and POLA_TOTAL.match(ambil(sel, peta, "no"))):
            nilai = next((x for x in (harga_t, vol_t, *reversed(sel)) if re.search(r"\d", x or "")), "")
            try:
                total_tertempel.append((uraian or ambil(sel, peta, "no"), int(parse_angka(nilai)) if nilai else None))
            except InputSalah:
                total_tertempel.append((uraian, None))
            dilewati.append(f"baris {no_file}: '{uraian}' dianggap baris total/pajak -> tidak dihitung ulang")
            continue
        if not vol_t and not harga_t:
            if uraian:
                dilewati.append(f"baris {no_file}: '{uraian}' tanpa volume & harga -> dianggap judul bagian")
            continue
        try:
            if not uraian:
                raise InputSalah("uraian kosong")
            vol = parse_angka(vol_t, "volume")
            harga = parse_angka(harga_t, "harga satuan")
            if vol <= 0 or harga < 0:
                raise InputSalah("volume harus > 0 dan harga satuan tidak boleh negatif")
        except InputSalah as e:
            masalah.append(f"baris {no_file} ('{uraian or '?'}'): {e}")
            continue
        jumlah = bulat(vol * harga)
        it = {"no": len(item) + 1, "uraian": uraian, "volume": vol, "satuan": sat or "-",
              "harga_satuan": harga, "jumlah": jumlah}
        if hps_t:
            try:
                h = parse_angka(hps_t, "harga satuan HPS")
                it["hps_satuan"] = h
                if h > 0:
                    it["persen_hps"] = (harga / h * 100).quantize(Decimal("0.01"), ROUND_HALF_UP)
            except InputSalah as e:
                masalah.append(f"baris {no_file}: {e}")
        item.append(it)
    if not item:
        raise InputSalah("tidak ada baris rincian yang valid. " + ("; ".join(masalah) if masalah else ""))

    tarif = TARIF[ppn]
    subtotal = sum(i["jumlah"] for i in item)
    if termasuk_ppn:
        dpp = dpp_dari_bruto(subtotal, tarif)
        nilai_ppn = ppn_bawah(dpp, tarif)
        total = subtotal
        sisa = subtotal - dpp - nilai_ppn
    else:
        dpp = subtotal
        nilai_ppn = ppn_bawah(dpp, tarif)
        total = dpp + nilai_ppn
        sisa = 0

    hasil = {"item": item, "subtotal": subtotal, "dpp": dpp, "ppn": nilai_ppn, "total": total,
             "sisa_pembulatan": sisa, "mode_ppn": ppn, "harga_termasuk_ppn": termasuk_ppn,
             "terbilang": terbilang(total), "baris_dilewati": dilewati, "baris_bermasalah": masalah,
             "catatan": catatan, "peringatan": [], "info": []}
    P, I = hasil["peringatan"], hasil["info"]
    if masalah:
        P.append(f"{len(masalah)} baris tidak bisa dibaca dan TIDAK ikut dihitung -> TOTAL BELUM FINAL. Perbaiki dulu.")
    for label, nilai in total_tertempel:
        if nilai is None:
            continue
        cocok = [("subtotal", subtotal), ("DPP", dpp), ("PPN", nilai_ppn), ("total", total)]
        if any(nilai == v for _, v in cocok):
            I.append(f"Baris '{label}' di file ({rupiah(nilai)}) cocok dengan hitungan script.")
        else:
            P.append(f"Baris '{label}' di file bernilai {rupiah(nilai)} tetapi TIDAK cocok dengan hitungan script "
                     f"(subtotal {rupiah(subtotal)}, total {rupiah(total)}). Cek rumus di Excel/dokumen.")
    for it in item:
        if "persen_hps" in it and it["persen_hps"] > 100:
            I.append(f"Item {it['no']} '{it['uraian']}': harga satuan {persen_id(it['persen_hps'])} dari HPS satuan "
                     f"(evaluasi umumnya pada total, tapi cek aturan dokumen pemilihan).")
    if hps is not None:
        hps = int(hps)
        if hps <= 0:
            P.append("Nilai HPS harus lebih dari 0; perbandingan HPS dilewati.")
        else:
            persen = (Decimal(total) / Decimal(hps) * 100).quantize(Decimal("0.01"), ROUND_HALF_UP)
            batas80 = int((Decimal(hps) * BATAS_KEWAJARAN / 100).to_integral_value(ROUND_FLOOR))
            hasil.update({"hps": hps, "persen_hps": persen, "batas_80_hps": batas80,
                          "selisih_hps": hps - total})
            if total > hps:
                P.append(f"Total penawaran MELEBIHI HPS sebesar {rupiah(total - hps)} ({persen_id(persen)} HPS). "
                         "Penawaran di atas HPS dinyatakan gugur pada evaluasi harga (kecuali ketentuan khusus di dokumen pemilihan).")
            elif Decimal(total) < Decimal(hps) * BATAS_KEWAJARAN / 100:
                P.append(f"Total penawaran {persen_id(persen)} HPS (< 80% HPS = di bawah {rupiah(batas80)}). "
                         "Pokja/Pejabat Pengadaan akan melakukan KLARIFIKASI KEWAJARAN HARGA: siapkan rincian "
                         "harga dasar (bukti harga pemasok/upah/alat). Jika dinyatakan wajar dan menang, "
                         "biasanya wajib menaikkan jaminan pelaksanaan menjadi 5% dari nilai HPS (cek dokumen pemilihan).")
            if hps > BATAS_JAMINAN_PENAWARAN:
                I.append("HPS > Rp10 miliar: tender barang/konstruksi/jasa lainnya umumnya mensyaratkan JAMINAN PENAWARAN "
                         "1%-3% dari HPS. Cek nilai & masa berlakunya di dokumen pemilihan.")
    if pagu is not None:
        pagu = int(pagu)
        hasil["pagu"] = pagu
        if total > pagu:
            P.append(f"Total penawaran melebihi pagu anggaran ({rupiah(pagu)}).")
        if pagu <= BATAS_PAKET_UMK:
            I.append("Pagu s.d. Rp15 miliar: paket barang/konstruksi/jasa lainnya pada dasarnya dicadangkan untuk "
                     "usaha mikro, usaha kecil, dan koperasi (Perpres 16/2018 jo. 46/2025 Pasal 65), kecuali paket "
                     "yang menuntut kemampuan teknis yang tidak dapat dipenuhi UMK.")
    if ppn == "tidak":
        I.append("Tanpa PPN (penyedia bukan PKP). Jika Anda PKP, jalankan ulang dengan --ppn nonmewah.")
    return hasil


def tampil_harga(h):
    out = ["RINCIAN PENAWARAN HARGA (hasil hitung script)", ""]
    lebar_u = min(40, max(8, *(len(i["uraian"]) for i in h["item"])))
    out.append(f"{'No':>3}  {'Uraian':<{lebar_u}}  {'Volume':>10}  {'Sat':<8}  {'Harga Satuan':>18}  {'Jumlah':>18}")
    for i in h["item"]:
        u = i["uraian"] if len(i["uraian"]) <= lebar_u else i["uraian"][: lebar_u - 1] + "~"
        hs = rupiah(bulat(i["harga_satuan"])) if i["harga_satuan"] == i["harga_satuan"].to_integral_value() \
            else "Rp" + angka_id(i["harga_satuan"])
        out.append(f"{i['no']:>3}  {u:<{lebar_u}}  {angka_id(i['volume']):>10}  {i['satuan'][:8]:<8}  "
                   f"{hs:>18}  {rupiah(i['jumlah']):>18}")
    out.append("")
    label = {"nonmewah": "PPN 12% x 11/12 DPP (efektif 11%)", "mewah": "PPN 12% (barang mewah)",
             "tidak": "PPN (tidak dipungut: bukan PKP)"}[h["mode_ppn"]]
    if h["harga_termasuk_ppn"]:
        out.append(f"Jumlah (harga sudah termasuk PPN)  : {rupiah(h['subtotal'])}")
        out.append(f"DPP                                : {rupiah(h['dpp'])}")
        out.append(f"{label:<35}: {rupiah(h['ppn'])}")
        if h["sisa_pembulatan"]:
            out.append(f"Sisa pembulatan                    : {rupiah(h['sisa_pembulatan'])}")
    else:
        out.append(f"Subtotal (DPP)                     : {rupiah(h['subtotal'])}")
        out.append(f"{label:<35}: {rupiah(h['ppn'])}")
    out.append(f"TOTAL PENAWARAN                    : {rupiah(h['total'])}")
    out.append(f"Terbilang: {h['terbilang']}")
    if "hps" in h:
        out.append("")
        out.append(f"HPS                                : {rupiah(h['hps'])}")
        out.append(f"Penawaran terhadap HPS             : {persen_id(h['persen_hps'])}")
        out.append(f"Batas 80% HPS                      : {rupiah(h['batas_80_hps'])}")
        out.append(f"Selisih (HPS - penawaran)          : {rupiah(h['selisih_hps'])}")
    for judul, isi in (("PERINGATAN", h["peringatan"]), ("Baris bermasalah", h["baris_bermasalah"]),
                       ("Info", h["info"]), ("Baris dilewati", h["baris_dilewati"]), ("Catatan", h["catatan"])):
        if isi:
            out.append("")
            out.append(f"{judul}:")
            out.extend(f"  - {x}" for x in isi)
    out.append("")
    out.append("Pembulatan: jumlah baris ke rupiah terdekat; PPN dihitung persis dari DPP lalu dibulatkan ke bawah. "
               "Belum dicocokkan dengan Coretax/SPSE. Pastikan format & aturan pembulatan mengikuti dokumen pemilihan.")
    return "\n".join(out)


# ---------------------------------------------------------------- jadwal
def parse_tanggal(teks, nama="tanggal"):
    if teks is None or not str(teks).strip():
        raise InputSalah(f"{nama} kosong")
    s = re.sub(r"\s+", " ", str(teks).strip().replace("pukul", "").replace("jam", "").replace("WIB", "")
               .replace("wib", "")).strip()
    s = s.replace(".", ":") if re.search(r"\d{1,2}\.\d{2}$", s) and s.count(".") == 1 else s
    for fmt in ("%Y-%m-%d %H:%M", "%Y-%m-%d", "%d-%m-%Y %H:%M", "%d-%m-%Y", "%d/%m/%Y %H:%M", "%d/%m/%Y",
                "%Y/%m/%d %H:%M", "%Y/%m/%d"):
        try:
            return datetime.strptime(s, fmt)
        except ValueError:
            continue
    raise InputSalah(f"{nama} tidak dikenali: {teks!r}. Pakai format 2026-10-15 atau 15-10-2026 (jam opsional 14:00)")


def baca_libur(teks):
    if not teks:
        return set()
    hasil = set()
    potongan = []
    for bagian in teks:
        try:
            with open(bagian, encoding="utf-8-sig") as f:
                potongan.extend(re.split(r"[,;\s]+", f.read()))
                continue
        except OSError:
            pass
        potongan.extend(re.split(r"[,;]+", bagian))
    for p in potongan:
        p = p.strip()
        if p:
            hasil.add(parse_tanggal(p, "tanggal libur").date())
    return hasil


def tgl_id(d):
    return f"{HARI[d.weekday()]}, {d.day} {BULAN[d.month - 1]} {d.year}"


def hari_kerja(d, libur, sabtu):
    return d not in libur and (d.weekday() < 5 or (sabtu and d.weekday() == 5))


def mundur(dari, n, libur, sabtu):
    d = dari
    while n > 0:
        d -= timedelta(days=1)
        if hari_kerja(d, libur, sabtu):
            n -= 1
    return d


def jadwal(batas, hari_ini, pengumuman=None, penjelasan=None, libur=(), sabtu=False,
           konstruksi=False, jaminan=False):
    libur = set(libur)
    tb = batas.date()
    jam = batas.strftime("%H:%M") if (batas.hour or batas.minute) else None
    peringatan, tugas = [], []
    if not hari_kerja(tb, libur, sabtu):
        peringatan.append("Batas unggah jatuh di hari libur/akhir pekan. Cek ulang jadwal di SPSE (bisa salah ketik).")
    if tb < hari_ini:
        peringatan.append("Batas unggah SUDAH LEWAT dibanding tanggal hari ini.")

    def tambah(tgl, kode, isi):
        tugas.append({"tanggal": tgl, "kode": kode, "tugas": isi})

    if pengumuman:
        tambah(pengumuman.date(), "Pengumuman",
               "Unduh dokumen pemilihan dari SPSE; baca syarat kualifikasi, KBLI/SBU, metode evaluasi, HPS, jadwal. "
               "Putuskan ikut/tidak (cek kelayakan).")
    if penjelasan:
        tp = penjelasan.date()
        tambah(tp, "Penjelasan",
               "Ikuti pemberian penjelasan (aanwijzing) di SPSE; ajukan pertanyaan tertulis sebelum sesi ditutup.")
        tambah(_maju(tp, 1, libur, sabtu), "Penjelasan+1",
               "Cek Berita Acara Pemberian Penjelasan & adendum dokumen pemilihan; sesuaikan rencana penawaran.")
    rencana = [
        (7, "Kumpulkan dokumen: NIB & KBLI (OSS), NPWP, status PKP, akta & pengesahan, pengalaman/kontrak, "
            "tenaga ahli & peralatan. Cek masa berlaku semua izin/sertifikat." +
            (" Cek SBU (subklasifikasi & kualifikasi) dan SKK personel, sisa kemampuan paket (SKP)." if konstruksi else "") +
            (" AJUKAN JAMINAN PENAWARAN ke bank/asuransi/penjaminan (proses bisa beberapa hari)." if jaminan else "")),
        (5, "Susun dokumen teknis: spesifikasi/brosur, metode pelaksanaan, jadwal, surat dukungan (bila diminta). "
            "Minta harga tertulis dari pemasok."),
        (3, "Finalisasi harga: jalankan cek_penawaran.py (volume x harga, PPN, total, % HPS, terbilang). "
            "Siapkan surat penawaran (masa berlaku sesuai dokumen), tanda tangan pihak berwenang."),
        (2, "Pemeriksaan silang: checklist administrasi/teknis/harga; cocokkan nama paket, kode tender, nilai "
            "angka vs terbilang; cek format & ukuran file." +
            (" Cek jaminan penawaran asli: nama paket, nilai, masa berlaku, bisa dicairkan (verifikasi ke penerbit)." if jaminan else "")),
        (1, "UNGGAH penawaran lengkap di SPSE (jangan tunggu hari terakhir). Simpan bukti/tanda terima unggah; "
            "cek file terbaca."),
    ]
    for n, isi in rencana:
        tambah(mundur(tb, n, libur, sabtu), f"H-{n}", isi)
    tambah(tb, "H", "Batas akhir unggah" + (f" pukul {jam}" if jam else "") +
           ". Hanya perbaikan darurat; unggah ulang paling lambat beberapa jam sebelum batas. "
           "Pastikan status penawaran 'terkirim'.")
    tugas.sort(key=lambda t: (t["tanggal"], 0 if t["kode"] in ("Pengumuman", "Penjelasan") else 1))
    for t in tugas:
        t["status"] = "TERLEWAT - kerjakan segera" if t["tanggal"] < hari_ini else (
            "HARI INI" if t["tanggal"] == hari_ini else "")
        if not hari_kerja(t["tanggal"], libur, sabtu) and t["kode"] not in ("H", "Pengumuman", "Penjelasan", "Penjelasan+1"):
            t["status"] = (t["status"] + " (hari libur)").strip()
    sisa = 0
    d = hari_ini
    while d < tb:
        if hari_kerja(d, libur, sabtu):
            sisa += 1
        d += timedelta(days=1)
    if 0 <= sisa < 3 and tb >= hari_ini:
        peringatan.append(f"Sisa hanya {sisa} hari kerja sebelum hari batas. Prioritaskan dokumen wajib & unggah awal.")
    if penjelasan and penjelasan.date() > tb:
        peringatan.append("Tanggal penjelasan setelah batas unggah - kemungkinan salah input.")
    return {"batas": batas, "hari_ini": hari_ini, "sisa_hari_kerja": sisa, "tugas": tugas,
            "peringatan": peringatan, "libur": sorted(libur), "sabtu_kerja": sabtu}


def _maju(d, n, libur, sabtu):
    while n > 0:
        d += timedelta(days=1)
        if hari_kerja(d, libur, sabtu):
            n -= 1
    return d


def tampil_jadwal(j):
    b = j["batas"]
    jam = b.strftime(" pukul %H:%M") if (b.hour or b.minute) else ""
    out = [f"JADWAL MUNDUR PENAWARAN - batas unggah {tgl_id(b.date())}{jam}",
           f"Hari ini: {tgl_id(j['hari_ini'])} | sisa hari kerja sebelum hari batas: {j['sisa_hari_kerja']}",
           "Hari kerja: Senin-" + ("Sabtu" if j["sabtu_kerja"] else "Jumat") +
           (f"; libur yang dikecualikan: {', '.join(d.isoformat() for d in j['libur'])}" if j["libur"] else
            "; libur nasional/cuti bersama BELUM dimasukkan (tambahkan --libur)"), ""]
    for t in j["tugas"]:
        st = f"  [{t['status']}]" if t["status"] else ""
        out.append(f"[ ] {t['kode']:<12} {tgl_id(t['tanggal'])}{st}")
        out.append(f"      {t['tugas']}")
    if j["peringatan"]:
        out.append("")
        out.append("PERINGATAN:")
        out.extend(f"  - {p}" for p in j["peringatan"])
    out.append("")
    out.append("Jadwal resmi selalu yang tertera di SPSE (bisa berubah lewat adendum). Cek ulang setiap hari.")
    return "\n".join(out)


# ---------------------------------------------------------------- CLI
def ke_json(o):
    if isinstance(o, Decimal):
        return str(o)
    if isinstance(o, (date, datetime)):
        return o.isoformat()
    raise TypeError(type(o))


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    if argv and argv[0] not in ("harga", "jadwal", "-h", "--help"):
        argv.insert(0, "harga")   # kompatibel: cek_penawaran.py file.csv
    ap = argparse.ArgumentParser(description="Pemeriksa penawaran harga & jadwal mundur tender (Komunitech).")
    sub = ap.add_subparsers(dest="perintah")
    h = sub.add_parser("harga", help="cek rincian harga dari CSV")
    h.add_argument("csv", help="file CSV rincian (atau - untuk stdin)")
    h.add_argument("--ppn", choices=["tidak", "nonmewah", "mewah"], default="tidak",
                   help="tidak (bukan PKP, default) | nonmewah (12%% x 11/12) | mewah (12%%)")
    h.add_argument("--termasuk-ppn", action="store_true", help="harga satuan di CSV sudah termasuk PPN")
    h.add_argument("--hps", help="nilai total HPS (sudah termasuk PPN), mis. 'Rp 250.000.000'")
    h.add_argument("--pagu", help="nilai pagu anggaran (opsional)")
    h.add_argument("--json", action="store_true")
    j = sub.add_parser("jadwal", help="jadwal mundur dari batas unggah penawaran")
    j.add_argument("--batas", required=True, help="batas akhir unggah, mis. '2026-10-15 14:00'")
    j.add_argument("--pengumuman")
    j.add_argument("--penjelasan")
    j.add_argument("--hari-ini", help="default: tanggal komputer")
    j.add_argument("--libur", action="append", help="tanggal libur dipisah koma, atau path file berisi tanggal")
    j.add_argument("--sabtu-kerja", action="store_true", help="Sabtu dihitung hari kerja")
    j.add_argument("--konstruksi", action="store_true", help="tambahkan tugas SBU/SKK/SKP")
    j.add_argument("--jaminan", action="store_true", help="tambahkan tugas jaminan penawaran")
    j.add_argument("--json", action="store_true")
    try:
        a = ap.parse_args(argv)
    except SystemExit as e:
        return e.code if isinstance(e.code, int) else 2
    try:
        if a.perintah == "harga":
            hps = int(parse_angka(a.hps, "HPS")) if a.hps else None
            pagu = int(parse_angka(a.pagu, "pagu")) if a.pagu else None
            hasil = hitung(a.csv, a.ppn, a.termasuk_ppn, hps, pagu)
            print(json.dumps(hasil, default=ke_json, ensure_ascii=False, indent=2) if a.json else tampil_harga(hasil))
        elif a.perintah == "jadwal":
            batas = parse_tanggal(a.batas, "batas unggah")
            hari_ini = parse_tanggal(a.hari_ini, "hari ini").date() if a.hari_ini else date.today()
            hasil = jadwal(batas, hari_ini,
                           parse_tanggal(a.pengumuman, "tanggal pengumuman") if a.pengumuman else None,
                           parse_tanggal(a.penjelasan, "tanggal penjelasan") if a.penjelasan else None,
                           baca_libur(a.libur), a.sabtu_kerja, a.konstruksi, a.jaminan)
            print(json.dumps(hasil, default=ke_json, ensure_ascii=False, indent=2) if a.json else tampil_jadwal(hasil))
        else:
            ap.print_help()
            return 2
    except InputSalah as e:
        print(f"GALAT: {e}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
