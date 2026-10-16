#!/usr/bin/env python3
"""Pemeriksa rincian penawaran harga tender/pengadaan pemerintah + jadwal mundur.

Hanya library standar Python 3.8+. Tanpa akses jaringan. Lintas OS
(macOS/Linux: python3, Windows: py atau python).

1) Cek rincian harga (volume x harga satuan, subtotal, PPN, total, terbilang, % HPS):
     python3 cek_penawaran.py harga rincian.csv --ppn nonmewah --hps "Rp 250.000.000"
   Kolom CSV (judul kolom boleh bervariasi): uraian, volume, satuan, harga satuan.
   Kolom opsional: no, harga satuan hps, jumlah (jumlah tertulis di file -> dicek per baris).
   Baris total/pajak di file dicocokkan sesuai label: total/"setelah PPN", subtotal/"sebelum PPN"/DPP,
   "DPP Nilai Lain (11/12)" (= 11/12 x DPP, toleransi Rp1), PPN.
   Pemisah ; , tab atau | dikenali otomatis. Format angka "Rp1.250.000,00", "1,5", "1.500" diterima.
   HPS/pagu boleh "185jt", "2,4 M", "Rp2,4 miliar".
   --jenis konstruksi|barang|jasa-lainnya|konsultansi|terintegrasi (jenis pengadaan): menentukan pesan
   jaminan penawaran (Perpres 16/2018 jo. 46/2025 Pasal 30 ayat (2): hanya konstruksi & terintegrasi) dan
   jaminan pelaksanaan (Pasal 33: barang/konstruksi/jasa lainnya). Tanpa --jenis: asumsi disebut di Info.
   Kolom "Jumlah" (banyaknya) + "Jumlah Harga" sekaligus: Jumlah = volume, Jumlah Harga = jumlah per baris.

Kode keluar (harga & jadwal):
   0 = bersih (tidak ada PERINGATAN)
   1 = hasil tercetak, ada PERINGATAN (salah hitung, total tidak cocok, di atas HPS/di bawah 80%, dll.)
   2 = input buruk (GALAT: file/angka/tanggal tidak terbaca, argumen salah) - tidak ada hasil
   3 = hasil tercetak tetapi TOTAL BELUM FINAL (ada baris tak terbaca) - didahulukan dari 1

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
BATAS_JAMINAN_PENAWARAN = 10_000_000_000  # HPS > Rp10 miliar -> jaminan penawaran (Pasal 31; hanya konstruksi/terintegrasi)
JENIS = ["konstruksi", "barang", "jasa-lainnya", "konsultansi", "terintegrasi"]
JENIS_JAMINAN_PENAWARAN = {"konstruksi", "terintegrasi"}           # Pasal 30 ayat (2) jo. 46/2025
JENIS_JAMINAN_PELAKSANAAN = {"barang", "konstruksi", "jasa-lainnya", "terintegrasi"}   # Pasal 33 ayat (1)
JENIS_PAKET_UMK = {"barang", "konstruksi", "jasa-lainnya"}          # Pasal 65 ayat (3)
NAMA_JENIS = {"jasa-lainnya": "jasa lainnya"}   # teks untuk manusia (tanpa tanda hubung)
BATAS_PAKET_UMK = 15_000_000_000          # pagu s.d. Rp15 miliar -> dicadangkan UMK & koperasi
BATAS_JAMINAN_PELAKSANAAN = 200_000_000   # kontrak > Rp200 juta -> jaminan pelaksanaan (Pasal 33)
KODE_BERSIH, KODE_PERINGATAN, KODE_GALAT, KODE_BELUM_FINAL = 0, 1, 2, 3   # lihat docstring
HARI = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"]
BULAN = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus",
         "September", "Oktober", "November", "Desember"]
POLA_TOTAL = re.compile(r"^\s*(sub\s*-?\s*total|total|grand\s*total|jumlah(\s+total|\s+harga|\s+akhir)?|"
                        r"ppn|pajak|dpp|terbilang|dibulatkan|pembulatan)\b", re.I)
# Label ringkasan yang TIDAK dikenali POLA_TOTAL tetapi tampak seperti total (dilaporkan, tidak dibandingkan)
POLA_MIRIP_TOTAL = re.compile(r"\b(total|jumlah|nilai|harga\s+penawaran|keseluruhan|grand)\b", re.I)


class InputSalah(Exception):
    pass


# ---------------------------------------------------------------- angka
def parse_angka(teks, nama="angka", besar=False):
    """'Rp1.250.000,00' -> 1250000 ; '1,5' -> 1.5 ; '1.500' -> 1500 ; '2.5' -> 2.5 ; '15,000.50' -> 15000.5

    besar=True (khusus HPS/pagu): akhiran miliar/milyar/M juga dikenali ('2,4 M' -> 2400000000).
    Tidak dipakai untuk volume/harga baris karena 'm' di sana bisa berarti meter."""
    if teks is None or str(teks).strip() == "":
        raise InputSalah(f"{nama} kosong")
    s = str(teks).strip().lower().replace(" ", "").replace("\u00a0", "")
    s = re.sub(r"[.,]-+$", "", s)          # "Rp 25.000,-"
    s = s.replace("rp.", "").replace("rp", "").replace("idr", "")
    pengali = Decimal(1)
    akhiran_daftar = (("juta", 10**6), ("jt", 10**6), ("ribu", 10**3), ("rb", 10**3))
    if besar:
        akhiran_daftar = (("miliar", 10**9), ("milyar", 10**9), ("m", 10**9)) + akhiran_daftar
    for akhiran, kali in akhiran_daftar:
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
    "volume": ("volume", "vol", "vol.", "qty", "qty.", "quantity", "kuantitas", "jumlah barang", "banyak",
               "banyaknya", "kuantum", "jml", "jml.", "jml barang", "jumlah unit", "volume pekerjaan",
               "vol pekerjaan", "vol. pekerjaan"),
    "satuan": ("satuan", "sat", "sat.", "unit", "uom"),
    "harga": ("harga satuan", "harga", "harga satuan (rp)", "harga (rp)", "unit price", "harga penawaran"),
    "hps": ("harga satuan hps", "hps satuan", "hps", "harga hps"),
    "jumlah": ("jumlah", "jumlah harga", "total harga", "total", "sub total", "subtotal", "jumlah (rp)",
               "jumlah harga (rp)", "total harga (rp)", "nilai", "amount"),
}


def _norm(s):
    return re.sub(r"\s+", " ", (s or "").strip().lower().replace("_", " "))


def kenali_header(baris):
    peta, kand_jumlah = {}, []
    for i, sel in enumerate(baris):
        n = _norm(sel)
        n2 = re.sub(r"\(.*?\)", "", n).strip()
        if n in KUNCI_KOLOM["jumlah"] or n2 in KUNCI_KOLOM["jumlah"]:
            kand_jumlah.append((i, n2))
        for kunci, sinonim in KUNCI_KOLOM.items():
            if kunci in peta:
                continue
            if n in sinonim or n2 in sinonim:
                peta[kunci] = i
                break
    if len(kand_jumlah) >= 2:
        # Layout tabel barang umum: "Jumlah" (banyaknya) + "Jumlah Harga" (rupiah).
        # Kolom ber-harga/total/nilai/rp = jumlah per baris; kolom "Jumlah" polos = volume (bila belum ada).
        uang = [i for i, n in kand_jumlah if re.search(r"harga|total|nilai|amount|rp", n)]
        polos = [i for i, n in kand_jumlah if i not in uang]
        if uang:
            peta["jumlah"] = uang[0]
            if polos and "volume" not in peta:
                peta["volume"] = polos[0]
                peta["_jumlah_ganda"] = True
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
    if peta and peta.pop("_jumlah_ganda", False):
        catatan.append("Ada kolom 'Jumlah' dan 'Jumlah Harga': 'Jumlah' dibaca sebagai VOLUME (banyaknya), "
                       "'Jumlah Harga' sebagai jumlah rupiah per baris (dicek terhadap volume x harga satuan).")
    if not peta:
        # tanpa judul kolom: tebak urutan
        contoh = next((b for b in semua if any(x.strip() for x in b)), [])
        if len(contoh) >= 5 and re.fullmatch(r"\d+\.?", contoh[0].strip() or "x"):
            peta = {"no": 0, "uraian": 1, "volume": 2, "satuan": 3, "harga": 4}
        else:
            peta = {"uraian": 0, "volume": 1, "satuan": 2, "harga": 3}
        catatan.append("Judul kolom tidak ditemukan; dianggap urutan: " +
                       ", ".join(k for k, _ in sorted(peta.items(), key=lambda x: x[1])) + ".")
    judul_jumlah = _norm(semua[mulai - 1][peta["jumlah"]]) if (mulai and "jumlah" in peta
                     and peta["jumlah"] < len(semua[mulai - 1])) else ""
    if "volume" not in peta and "jumlah" in peta and re.search(r"harga|total|nilai|amount|rp", judul_jumlah):
        # v1.0.3: kolom uang (mis. "Jumlah Harga") TIDAK boleh dipakai sebagai volume
        raise InputSalah(f"kolom volume/banyaknya tidak dikenali (kolom '{semua[mulai - 1][peta['jumlah']].strip()}' "
                         "berisi rupiah, bukan volume). Ubah judul kolom banyaknya menjadi 'Volume' atau 'Qty'.")
    if "volume" not in peta and "jumlah" in peta:
        # judul "Jumlah" dipakai untuk banyaknya barang (tanpa kolom Volume) -> perlakukan sebagai volume
        peta["volume"] = peta.pop("jumlah")
        catatan.append("Kolom 'Jumlah' dibaca sebagai VOLUME (banyaknya), karena tidak ada kolom Volume/Qty.")
    for wajib in ("volume", "harga"):
        if wajib not in peta:
            raise InputSalah(f"kolom '{wajib}' tidak ditemukan. Judul kolom yang dikenali: uraian, volume, satuan, harga satuan")
    lebar = max(peta.values()) + 1
    return semua[mulai:], peta, lebar, pemisah, catatan, mulai


def ambil(sel, peta, kunci):
    i = peta.get(kunci)
    return sel[i].strip() if i is not None and i < len(sel) else ""


def label_total(uraian, sel):
    """Label baris total/pajak, atau None. Bila Uraian kosong, label boleh di kolom mana pun
    (layout Excel umum: ';;;;TOTAL;Rp341.775.000' dengan sel gabung)."""
    if uraian:
        return uraian if POLA_TOTAL.match(uraian) else None
    for x in sel:
        if x.strip() and POLA_TOTAL.match(x):
            return x.strip()
    return None


POLA_JENIS_PPN = re.compile(r"^\s*(ppn|pajak)", re.I)
POLA_JENIS_SUBTOTAL = re.compile(r"^\s*(sub\s*-?\s*total|dpp|jumlah(\s+harga)?(?!\s*[a-z]))", re.I)
# Label yang MENYEBUT basisnya sendiri (layout Excel PKP sejak PMK 131/2024)
POLA_NILAI_LAIN = re.compile(r"nilai\s+lain|11\s*/\s*12", re.I)
POLA_SEBELUM_PPN = re.compile(r"sebelum\s+(ppn|pajak)|belum\s+(termasuk\s+)?(ppn|pajak)|tanpa\s+(ppn|pajak)|"
                              r"\bexcl|\bdpp\b|dasar\s+pengenaan", re.I)
POLA_SESUDAH_PPN = re.compile(r"(setelah|sesudah|termasuk|incl\w*|\+|plus|dengan)\s*(ppn|pajak)", re.I)


def jenis_total(label):
    """'ppn' | 'dpp_lain' (DPP nilai lain 11/12) | 'dpp' (label menyebut 'sebelum PPN'/DPP) |
    'subtotal' (Jumlah/Subtotal, basis tidak disebut) | 'total' (total/grand total/sesudah PPN/dibulatkan)."""
    if POLA_JENIS_PPN.match(label):
        return "ppn"
    if POLA_NILAI_LAIN.search(label):
        return "dpp_lain"
    if POLA_SEBELUM_PPN.search(label):
        return "dpp"
    if POLA_SESUDAH_PPN.search(label):
        return "total"
    if POLA_JENIS_SUBTOTAL.match(label):
        return "subtotal"
    return "total"


def bandingkan_total(label, nilai, dpp, nilai_ppn, total, termasuk_ppn, P, I, sementara=False, ppn_mode=None):
    """Cocokkan baris total/pajak di file dengan angka script SESUAI labelnya.
    Tidak pernah menyatakan 'cocok' bila basisnya berbeda (sebelum vs sesudah PPN), dan tidak
    menyatakan 'cocok' bila hasil hitung masih SEMENTARA (TOTAL BELUM FINAL)."""
    jenis = jenis_total(label)
    ppn_aktif = nilai_ppn > 0
    kedua = (f"hasil hitung: sebelum PPN {rupiah(dpp)}, PPN {rupiah(nilai_ppn)}, sesudah PPN {rupiah(total)}"
             if ppn_aktif else f"hasil hitung: total {rupiah(total)}, tanpa PPN")

    def cocok(apa):
        if sementara:
            I.append(f"Baris '{label}' di file ({rupiah(nilai)}) sama dengan {apa} SEMENTARA - belum bisa dinyatakan "
                     f"cocok karena ada baris tak terbaca (TOTAL BELUM FINAL; {kedua}).")
        else:
            I.append(f"Baris '{label}' di file ({rupiah(nilai)}) cocok dengan {apa} ({kedua}).")

    if jenis == "ppn":
        if nilai == nilai_ppn:
            cocok("PPN hasil hitung")
        else:
            P.append(f"Baris '{label}' di file bernilai {rupiah(nilai)} tetapi PPN hasil hitung {rupiah(nilai_ppn)} "
                     f"(selisih {rupiah(nilai_ppn - nilai)}; {kedua}). Cek rumus PPN/DPP di Excel.")
        return
    if jenis == "dpp_lain":
        # DPP nilai lain = 11/12 x DPP (PMK 131/2024). Excel bisa membulatkan ke atas/bawah -> toleransi Rp1.
        persis = Fraction(dpp) * 11 / 12
        acuan = bulat(persis)
        teks_acuan = f"11/12 x {rupiah(dpp)} = {rupiah(acuan)}"
        if ppn_mode == "mewah":
            I.append(f"Baris '{label}': barang mewah memakai DPP penuh (12% x DPP), bukan DPP nilai lain 11/12.")
        if abs(Fraction(nilai) - persis) <= 1:
            cocok(f"DPP nilai lain ({teks_acuan})")
        else:
            P.append(f"Baris '{label}' di file bernilai {rupiah(nilai)} tetapi DPP nilai lain {teks_acuan} "
                     f"(selisih {rupiah(acuan - nilai)}; {kedua}). Cek rumus DPP nilai lain di Excel.")
        return
    if jenis == "dpp":
        if nilai == dpp:
            cocok("jumlah SEBELUM PPN")
        elif ppn_aktif and nilai == total:
            P.append(f"Baris '{label}' di file ({rupiah(nilai)}) sama dengan total SESUDAH PPN, padahal labelnya "
                     f"menyebut SEBELUM PPN/DPP ({kedua}). Perbaiki label atau rumusnya.")
        else:
            P.append(f"Baris '{label}' di file bernilai {rupiah(nilai)} tetapi jumlah SEBELUM PPN hasil hitung "
                     f"{rupiah(dpp)} (selisih {rupiah(dpp - nilai)}; {kedua}). Cek rumus di Excel.")
        return
    if jenis == "subtotal":
        if nilai == dpp:
            cocok("jumlah SEBELUM PPN")
        elif nilai == total and termasuk_ppn:
            cocok("jumlah harga yang SUDAH TERMASUK PPN")
        elif nilai == total:
            P.append(f"Baris '{label}' di file ({rupiah(nilai)}) sama dengan total SESUDAH PPN, padahal label ini "
                     f"biasanya berarti jumlah SEBELUM PPN ({kedua}). Pastikan label & rumusnya benar.")
        else:
            P.append(f"Baris '{label}' di file bernilai {rupiah(nilai)} tetapi jumlah hasil hitung "
                     f"{rupiah(total if termasuk_ppn else dpp)} (selisih {rupiah((total if termasuk_ppn else dpp) - nilai)}; "
                     f"{kedua}). Cek rumus di Excel.")
        return
    if nilai == total:
        cocok("TOTAL" + (" sesudah PPN" if ppn_aktif else "") + " hasil hitung")
    elif ppn_aktif and nilai == dpp:
        P.append(f"Baris '{label}' di file ({rupiah(nilai)}) = jumlah SEBELUM PPN. Total di file BELUM TERMASUK PPN: "
                 f"total yang benar {rupiah(total)} (sebelum PPN {rupiah(dpp)} + PPN {rupiah(nilai_ppn)}). "
                 "Total tanpa PPN di surat penawaran bisa menggugurkan/merugikan - perbaiki.")
    else:
        P.append(f"Baris '{label}' di file bernilai {rupiah(nilai)} tetapi TIDAK cocok dengan total hasil hitung "
                 f"{rupiah(total)} (selisih {rupiah(total - nilai)}; {kedua}). Cek rumus di Excel/dokumen.")


def pesan_pelaksanaan_terintegrasi(total, pagu):
    """Pekerjaan terintegrasi + pagu diisi: jaminan pelaksanaan mengacu pagu anggaran
    (Perpres 16/2018 jo. 12/2021 jo. 46/2025 Pasal 33 ayat (4)). Mengembalikan (peringatan?, teks) atau None."""
    if total <= BATAS_JAMINAN_PELAKSANAAN:
        return None
    batas80_pagu = int((Decimal(pagu) * BATAS_KEWAJARAN / 100).to_integral_value(ROUND_FLOOR))
    if Decimal(total) < Decimal(pagu) * BATAS_KEWAJARAN / 100:
        return (True, f"Pekerjaan terintegrasi: penawaran di bawah 80% pagu anggaran (< {rupiah(batas80_pagu)}). "
                      f"Bila menang, jaminan pelaksanaan 5% dari nilai total pagu = {rupiah(bulat(Decimal(pagu) * 5 / 100))} "
                      "(bukan 5% nilai kontrak; Perpres 16/2018 jo. 46/2025 Pasal 33 ayat (4)). Cek dokumen pemilihan.")
    return (False, f"Pekerjaan terintegrasi, kontrak > Rp200 juta: bila menang, siapkan jaminan pelaksanaan 5% dari "
                   f"nilai kontrak = {rupiah(bulat(Decimal(total) * 5 / 100))} (penawaran 80%-100% pagu anggaran; "
                   "Perpres 16/2018 jo. 46/2025 Pasal 33 ayat (4)). Perhitungkan di arus kas.")


def hitung(path, ppn="tidak", termasuk_ppn=False, hps=None, pagu=None, jenis=None):
    if jenis is not None and jenis not in JENIS:
        raise InputSalah(f"jenis pengadaan '{jenis}' tidak dikenal; pilih: {', '.join(JENIS)}")
    nama_jenis = NAMA_JENIS.get(jenis, jenis)
    pagu = int(pagu) if pagu is not None else None
    if pagu is not None and pagu <= 0:
        raise InputSalah("nilai pagu harus lebih dari 0 (contoh: --pagu \"Rp14 M\" atau --pagu 14000000000)")
    # pekerjaan terintegrasi + pagu diisi: jaminan dihitung dari pagu (Pasal 31 ayat (3), Pasal 33 ayat (4))
    pakai_pagu = jenis == "terintegrasi" and pagu is not None
    baris_data, peta, lebar, pemisah, catatan, offset = baca_rincian(path)
    item, dilewati, masalah, total_tertempel, selisih_baris, info_baris = [], [], [], [], [], []
    mirip_total = []   # (no_file, label, nilai): baris berlabel mirip total yang tidak dikenali -> dilaporkan
    for no_file, sel in enumerate(baris_data, start=offset + 1):
        if not any(x.strip() for x in sel):
            continue
        if len(sel) > lebar and pemisah == ",":
            sel = perbaiki_koma(sel, lebar)
        uraian = ambil(sel, peta, "uraian")
        vol_t, sat, harga_t = ambil(sel, peta, "volume"), ambil(sel, peta, "satuan"), ambil(sel, peta, "harga")
        hps_t, jumlah_t = ambil(sel, peta, "hps"), ambil(sel, peta, "jumlah")
        label = label_total(uraian, sel)
        if label is not None:
            nilai = next((x for x in (jumlah_t, harga_t, vol_t, *reversed(sel))
                          if re.search(r"\d", x or "") and not POLA_TOTAL.match(x or "")), "")
            try:
                total_tertempel.append((label, int(bulat(parse_angka(nilai))) if nilai else None))
            except InputSalah:
                total_tertempel.append((label, None))
            dilewati.append(f"baris {no_file}: '{label}' dianggap baris total/pajak -> tidak dihitung ulang")
            continue
        if not vol_t and not harga_t:
            if uraian:
                nilai_t = jumlah_t if re.search(r"\d", jumlah_t) else ""
                if nilai_t:
                    try:
                        mirip_total.append((no_file, uraian, bulat(parse_angka(nilai_t))))
                    except InputSalah:
                        mirip_total.append((no_file, uraian, None))
                    dilewati.append(f"baris {no_file}: '{uraian}' berisi angka di kolom Jumlah tanpa volume & harga "
                                    "-> tidak dihitung (lihat Info)")
                else:
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
        if jumlah_t:
            try:
                tertulis = parse_angka(jumlah_t, "jumlah tertulis")
                it["jumlah_file"] = bulat(tertulis)
                if abs(tertulis - vol * harga) >= 1:   # beda >= Rp1 bukan sekadar pembulatan
                    selisih_baris.append({"baris_file": no_file, "item": it["no"], "uraian": uraian,
                                          "volume": vol, "harga_satuan": harga, "jumlah_file": it["jumlah_file"],
                                          "jumlah_hitung": jumlah, "selisih": jumlah - it["jumlah_file"]})
            except InputSalah:
                info_baris.append(f"baris {no_file}: kolom Jumlah {jumlah_t!r} tidak terbaca -> tidak dibandingkan")
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
             "catatan": catatan, "peringatan": [], "info": [], "selisih_baris": selisih_baris,
             "total_belum_final": bool(masalah), "jenis": jenis}
    P, I = hasil["peringatan"], hasil["info"]
    if masalah:
        P.append(f"{len(masalah)} baris tidak bisa dibaca dan TIDAK ikut dihitung -> TOTAL BELUM FINAL. Perbaiki dulu.")
    if selisih_baris:
        P.append(f"{len(selisih_baris)} baris: kolom Jumlah di file TIDAK sama dengan volume x harga satuan "
                 "(lihat 'Baris salah hitung'). Hasil hitung memakai volume x harga satuan; perbaiki file Anda.")
        if all("jumlah_file" in i for i in item):
            jml_file = sum(i["jumlah_file"] for i in item)
            P.append(f"Jumlah kolom Jumlah di file {rupiah(jml_file)} vs hasil hitung {rupiah(subtotal)} "
                     f"(selisih {rupiah(subtotal - jml_file)}).")
    I.extend(info_baris)
    for label, nilai in total_tertempel:
        if nilai is None:
            continue
        bandingkan_total(label, nilai, dpp, nilai_ppn, total, termasuk_ppn, P, I, sementara=bool(masalah),
                         ppn_mode=ppn)
        if (selisih_baris and nilai_ppn > 0 and jenis_total(label) == "total" and not termasuk_ppn
                and all("jumlah_file" in i for i in item) and nilai == sum(i["jumlah_file"] for i in item)):
            P.append(f"Baris '{label}' di file ({rupiah(nilai)}) sama dengan jumlah kolom Jumlah di file = masih "
                     "SEBELUM PPN dan ikut salah hitung baris di atas.")
    for no_file, label, nilai in mirip_total:
        if nilai is None:
            I.append(f"Baris {no_file} '{label}': angka di kolom Jumlah tidak terbaca -> tidak diperiksa.")
            continue
        jenis = "tampak seperti baris total" if POLA_MIRIP_TOTAL.search(label) else "mungkin subtotal bagian/total"
        if nilai == dpp and nilai_ppn > 0:
            banding = f"nilainya SAMA dengan jumlah SEBELUM PPN hasil hitung ({rupiah(dpp)}; sesudah PPN {rupiah(total)})"
        elif nilai == total:
            banding = f"nilainya SAMA dengan total hasil hitung ({rupiah(total)})"
        else:
            banding = (f"nilainya TIDAK sama dengan jumlah sebelum PPN ({rupiah(dpp)}) maupun total ({rupiah(total)}) "
                       "hasil hitung")
        I.append(f"Baris {no_file} '{label}' ({rupiah(nilai)}) {jenis}, tetapi labelnya tidak dikenali -> TIDAK "
                 f"diperiksa otomatis; {banding}. Bila ini total penawaran, pastikan angkanya benar"
                 + (" (sementara: TOTAL BELUM FINAL)." if masalah else "."))
    for it in item:
        if "persen_hps" in it and it["persen_hps"] > 100:
            I.append(f"Item {it['no']} '{it['uraian']}': harga satuan {persen_id(it['persen_hps'])} dari HPS satuan "
                     f"(evaluasi umumnya pada total, tapi cek aturan dokumen pemilihan).")
    if hps is not None:
        hps = int(hps)
        if hps <= 0:
            raise InputSalah("nilai HPS harus lebih dari 0 (contoh: --hps \"Rp2,4 M\" atau --hps 2400000000)")
        else:
            persen = (Decimal(total) / Decimal(hps) * 100).quantize(Decimal("0.01"), ROUND_HALF_UP)
            batas80 = int((Decimal(hps) * BATAS_KEWAJARAN / 100).to_integral_value(ROUND_FLOOR))
            hasil.update({"hps": hps, "persen_hps": persen, "batas_80_hps": batas80,
                          "selisih_hps": hps - total})
            if total > hps:
                P.append(f"Total penawaran MELEBIHI HPS sebesar {rupiah(total - hps)} ({persen_id(persen)} HPS). "
                         "Penawaran di atas HPS dinyatakan gugur pada evaluasi harga (kecuali ketentuan khusus di dokumen pemilihan).")
            elif Decimal(total) < Decimal(hps) * BATAS_KEWAJARAN / 100:
                teks = (f"Total penawaran {persen_id(persen)} HPS (< 80% HPS = di bawah {rupiah(batas80)}). "
                        "Pokja/Pejabat Pengadaan akan melakukan KLARIFIKASI KEWAJARAN HARGA: siapkan rincian "
                        "harga dasar (bukti harga pemasok/upah/alat); tidak wajar -> gugur. ")
                if jenis == "konsultansi":
                    teks += ("Jasa konsultansi: jaminan pelaksanaan tidak diatur Pasal 33 (hanya barang/konstruksi/"
                             "jasa lainnya); ikuti dokumen pemilihan.")
                elif pakai_pagu:
                    teks += "Jaminan pelaksanaan pekerjaan terintegrasi dihitung dari pagu anggaran (lihat di bawah)."
                elif total > BATAS_JAMINAN_PELAKSANAAN:
                    teks += (f"Jika dinyatakan wajar dan menang, jaminan pelaksanaan menjadi 5% dari nilai HPS = "
                             f"{rupiah(bulat(Decimal(hps) * 5 / 100))} (bukan 5% nilai kontrak; Perpres 16/2018 jo. "
                             "46/2025 Pasal 33 ayat (3) huruf b"
                             + ("; pekerjaan terintegrasi: seharusnya dari pagu anggaran, isi --pagu untuk angka pasti"
                                if jenis == "terintegrasi" else "") + "; cek dokumen pemilihan).")
                else:
                    teks += ("Nilai kontrak s.d. Rp200 juta: jaminan pelaksanaan umumnya tidak diberlakukan "
                             "(berlaku untuk kontrak > Rp200 juta; cek dokumen pemilihan).")
                P.append(teks)
            elif total > BATAS_JAMINAN_PELAKSANAAN and not pakai_pagu:
                if jenis == "konsultansi":
                    I.append("Jasa konsultansi: jaminan pelaksanaan tidak diatur Pasal 33 Perpres 16/2018 jo. 46/2025 "
                             "(hanya barang/konstruksi/jasa lainnya); ikuti dokumen pemilihan.")
                else:
                    I.append(f"Kontrak > Rp200 juta: bila menang, siapkan jaminan pelaksanaan 5% dari nilai kontrak = "
                             f"{rupiah(bulat(Decimal(total) * 5 / 100))} (Perpres 16/2018 jo. 46/2025 Pasal 33; "
                             "berlaku juga untuk e-purchasing; tidak diperlukan hanya untuk jasa lainnya yang aset "
                             "penyedianya dikuasai pengguna"
                             + ("" if jenis else "; asumsi jenis barang/konstruksi/jasa lainnya, bukan konsultansi")
                             + "). Perhitungkan di arus kas.")
            if hps > BATAS_JAMINAN_PENAWARAN:
                dasar = pagu if pakai_pagu else hps
                satu, tiga = bulat(Decimal(dasar) / 100), bulat(Decimal(dasar) * 3 / 100)
                if jenis in JENIS_JAMINAN_PENAWARAN:
                    if pakai_pagu:
                        acuan = f"dari pagu anggaran {rupiah(pagu)} (pekerjaan terintegrasi, Pasal 31 ayat (3))"
                    elif jenis == "terintegrasi":
                        acuan = ("dari HPS sebagai gambaran (pekerjaan terintegrasi seharusnya dari pagu anggaran; "
                                 "isi --pagu untuk angka pasti)")
                    else:
                        acuan = "dari HPS"
                    hasil["dasar_jaminan_penawaran"] = "pagu" if pakai_pagu else "hps"
                    I.append(f"HPS > Rp10 miliar, pengadaan {nama_jenis}: WAJIB JAMINAN PENAWARAN 1%-3% {acuan} = "
                             f"{rupiah(satu)} s.d. {rupiah(tiga)} (Perpres 16/2018 jo. 46/2025 Pasal 30 ayat (2) & "
                             "Pasal 31). Cek nilai pasti & masa berlakunya di dokumen pemilihan.")
                elif jenis:
                    I.append(f"HPS > Rp10 miliar, pengadaan {nama_jenis}: sejak Perpres 46/2025, JAMINAN PENAWARAN hanya "
                             "untuk pekerjaan konstruksi & pekerjaan terintegrasi (Pasal 30 ayat (2)) -> umumnya "
                             "TIDAK diperlukan untuk jenis ini. Tetap ikuti dokumen pemilihan bila memintanya.")
                else:
                    I.append("HPS > Rp10 miliar - ASUMSI: jenis pengadaan tidak disebut (tambahkan --jenis). "
                             "JAMINAN PENAWARAN 1%-3% dari HPS "
                             f"({rupiah(satu)} s.d. {rupiah(tiga)}) hanya wajib bila pekerjaan KONSTRUKSI atau "
                             "TERINTEGRASI (terintegrasi: acuan pagu); untuk barang/jasa lainnya/konsultansi tidak "
                             "diperlukan sejak Perpres 46/2025 (Pasal 30 ayat (2) & Pasal 31). Cek dokumen pemilihan.")
    if pagu is not None:
        hasil["pagu"] = pagu
        if total > pagu:
            P.append(f"Total penawaran melebihi pagu anggaran ({rupiah(pagu)}).")
        if pakai_pagu:
            r = pesan_pelaksanaan_terintegrasi(total, pagu)
            if r:
                (P if r[0] else I).append(r[1])
        if pagu <= BATAS_PAKET_UMK and jenis in (None, *JENIS_PAKET_UMK):
            I.append("Pagu s.d. Rp15 miliar: paket barang/konstruksi/jasa lainnya pada dasarnya dicadangkan untuk "
                     "usaha mikro, usaha kecil, dan koperasi (Perpres 16/2018 jo. 46/2025 Pasal 65 ayat (3)), "
                     "kecuali paket yang menuntut kemampuan teknis yang tidak dapat dipenuhi UMK (Pasal 65 ayat (4)).")
    if ppn == "tidak":
        I.append("Tanpa PPN (penyedia bukan PKP). Jika Anda PKP, jalankan ulang dengan --ppn nonmewah.")
    return hasil


def pengingat(h):
    """Pengingat untuk tampilan teks saja (v1.0.9): tidak mengubah angka maupun isi hasil --json.
    1) Jaminan penawaran dipisah tegas dari jaminan pelaksanaan (HPS > Rp10 M sudah dibahas di Info).
    2) Potongan bendahara saat pembayaran (PPN & PPh) -> dampak arus kas."""
    jenis, hps, out = h.get("jenis"), h.get("hps"), []
    nama = NAMA_JENIS.get(jenis, jenis)
    dasar = ("jaminan penawaran hanya untuk pekerjaan konstruksi & pekerjaan terintegrasi dengan HPS di atas "
             "Rp10 miliar - Perpres 16/2018 jo. 46/2025 Pasal 30 ayat (2) & Pasal 31")
    beda = ("" if jenis == "konsultansi" else
            " Ini BERBEDA dengan jaminan pelaksanaan (kontrak di atas Rp200 juta, disiapkan bila menang).")
    if hps is not None and hps <= BATAS_JAMINAN_PENAWARAN:
        out.append(f"Jaminan penawaran: TIDAK disyaratkan Perpres untuk paket ini (HPS s.d. Rp10 miliar; {dasar}). "
                   f"Ikuti dokumen pemilihan bila tetap memintanya.{beda}")
    elif hps is None and jenis in JENIS_JAMINAN_PENAWARAN:
        out.append(f"Jaminan penawaran ({nama}): wajib bila HPS di atas Rp10 miliar, 1%-3% dari HPS"
                   + (" (terintegrasi: dari pagu anggaran)" if jenis == "terintegrasi" else "")
                   + f" - Pasal 30 ayat (2) & Pasal 31; sebutkan HPS untuk kepastian.{beda}")
    elif hps is None and jenis:
        out.append(f"Jaminan penawaran: TIDAK disyaratkan Perpres untuk pengadaan {nama} ({dasar}). "
                   f"Ikuti dokumen pemilihan bila tetap memintanya.{beda}")
    elif hps is None:
        out.append(f"Jaminan penawaran: {dasar}; barang/jasa lainnya/konsultansi tidak disyaratkan Perpres.{beda}")
    if jenis in ("konstruksi", "terintegrasi"):
        pph = "PPh final jasa konstruksi (PP 9/2022; tarif tergantung kualifikasi/SBU - tanyakan konsultan pajak)"
    elif jenis in ("jasa-lainnya", "konsultansi"):
        pph = "PPh atas jasa (umumnya PPh Pasal 23)"
    elif jenis == "barang":
        pph = "PPh Pasal 22 sebesar 1,5% dari harga tanpa PPN (pembelian barang)"
    else:
        pph = ("PPh Pasal 22 sebesar 1,5% dari harga tanpa PPN bila pembelian barang (jasa: umumnya PPh Pasal 23; "
               "konstruksi: PPh final)")
    if h["mode_ppn"] == "tidak":
        out.append(f"Saat dibayar: tanpa PPN (bukan PKP), tetapi bendahara instansi tetap memotong {pph} -> uang yang "
                   "masuk ke rekening lebih kecil dari total penawaran; siapkan arus kas.")
    else:
        out.append(f"Saat dibayar: bendahara instansi memungut PPN ({rupiah(h['ppn'])}) dan memotong {pph} -> uang "
                   "yang masuk ke rekening lebih kecil dari total penawaran; siapkan arus kas. Nilai penawaran & "
                   "perbandingan dengan HPS tetap TERMASUK PPN.")
    return out


def tampil_harga(h):
    out = ["RINCIAN PENAWARAN HARGA (hasil hitung)", ""]
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
    salah = [f"baris {s['baris_file']} (item {s['item']} '{s['uraian']}'): file {rupiah(s['jumlah_file'])} "
             f"!= hitung {angka_id(s['volume'])} x Rp{angka_id(s['harga_satuan'])} = {rupiah(s['jumlah_hitung'])} "
             f"(selisih {rupiah(s['selisih'])})" for s in h.get("selisih_baris", [])]
    for judul, isi in (("PERINGATAN", h["peringatan"]), ("Baris salah hitung", salah),
                       ("Baris bermasalah", h["baris_bermasalah"]),
                       ("Info", h["info"]), ("Baris dilewati", h["baris_dilewati"]), ("Catatan", h["catatan"])):
        if isi:
            out.append("")
            out.append(f"{judul}:")
            out.extend(f"  - {x}" for x in isi)
    out.append("")
    out.append("Pengingat:")
    out.extend(f"  - {x}" for x in pengingat(h))
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
        (3, "Finalisasi harga: hitung ulang volume x harga, PPN, total, % HPS, dan terbilang. "
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
    lewat = {"Pengumuman": "SUDAH LEWAT - pastikan dokumen pemilihan & adendum sudah diunduh",
             "Penjelasan": "SUDAH LEWAT - baca Berita Acara Penjelasan & adendum"}
    for t in tugas:
        t["status"] = lewat.get(t["kode"], "TERLEWAT - kerjakan segera") if t["tanggal"] < hari_ini else (
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
    h.add_argument("--jenis", choices=JENIS,
                   help="jenis pengadaan (menentukan info jaminan penawaran/pelaksanaan); tanpa ini asumsi disebut")
    h.add_argument("--json", action="store_true")
    j = sub.add_parser("jadwal", help="jadwal mundur dari batas unggah penawaran")
    j.add_argument("--batas", required=True, help="batas akhir unggah, mis. '2026-10-15 14:00'")
    j.add_argument("--pengumuman")
    j.add_argument("--penjelasan")
    j.add_argument("--hari-ini", help="default: tanggal komputer")
    j.add_argument("--libur", action="append", help="tanggal libur dipisah koma, atau path file berisi tanggal")
    j.add_argument("--sabtu-kerja", action="store_true", help="Sabtu dihitung hari kerja")
    j.add_argument("--konstruksi", action="store_true", help="tambahkan tugas SBU/SKK/SKP")
    j.add_argument("--jaminan", action="store_true", help="tambahkan tugas jaminan penawaran (hanya konstruksi/terintegrasi, HPS > Rp10 M)")
    j.add_argument("--json", action="store_true")
    try:
        a = ap.parse_args(argv)
    except SystemExit as e:
        # --help -> 0 ; argumen salah (argparse) -> 2 = input buruk
        return e.code if isinstance(e.code, int) else KODE_GALAT
    try:
        if a.perintah == "harga":
            hps = int(parse_angka(a.hps, "HPS", besar=True)) if a.hps else None
            pagu = int(parse_angka(a.pagu, "pagu", besar=True)) if a.pagu else None
            hasil = hitung(a.csv, a.ppn, a.termasuk_ppn, hps, pagu, a.jenis)
            print(json.dumps(hasil, default=ke_json, ensure_ascii=False, indent=2) if a.json else tampil_harga(hasil))
            if hasil["total_belum_final"]:
                return KODE_BELUM_FINAL   # hasil tetap tercetak; ada baris yang tidak ikut dihitung
            if hasil["peringatan"]:
                return KODE_PERINGATAN
        elif a.perintah == "jadwal":
            batas = parse_tanggal(a.batas, "batas unggah")
            hari_ini = parse_tanggal(a.hari_ini, "hari ini").date() if a.hari_ini else date.today()
            hasil = jadwal(batas, hari_ini,
                           parse_tanggal(a.pengumuman, "tanggal pengumuman") if a.pengumuman else None,
                           parse_tanggal(a.penjelasan, "tanggal penjelasan") if a.penjelasan else None,
                           baca_libur(a.libur), a.sabtu_kerja, a.konstruksi, a.jaminan)
            print(json.dumps(hasil, default=ke_json, ensure_ascii=False, indent=2) if a.json else tampil_jadwal(hasil))
            if hasil["peringatan"]:
                return KODE_PERINGATAN
        else:
            ap.print_help()
            return KODE_GALAT
    except InputSalah as e:
        print(f"GALAT: {e}", file=sys.stderr)
        return KODE_GALAT
    return KODE_BERSIH


if __name__ == "__main__":
    sys.exit(main())
