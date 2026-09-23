#!/usr/bin/env python3
"""
periksa_draf.py — Memeriksa draf balasan CS sebelum dikirim admin.

Memeriksa DUA hal, hanya dengan Python standar (tanpa dependensi luar):
1. Nominal Rupiah yang disebut di draf tapi TIDAK ditemukan di basis
   pengetahuan (cs/PENGETAHUAN.md) -> potensi mengarang HARGA.
   Menangkap juga harga tanpa awalan "Rp" (mis. "harganya 79.000", "cuma
   250.000") dan harga berpengali (mis. "89rb", "2 jt", "1,5 juta").
2. Pola data sensitif di draf (mirip NIK/KTP 16 digit, nomor kartu, kode
   OTP/verifikasi, PIN, password) -> jangan sampai bocor balik ke pelanggan.

**PENTING — yang TIDAK diperiksa script ini:** STOK tidak diperiksa sama
sekali (tidak ada cara membedakan klaim stok dari angka lain secara aman).
Klaim stok ("tinggal 2", "masih ada", "sudah habis") tetap wajib dicek
manual oleh admin terhadap `PENGETAHUAN.md` / data toko sebenarnya.

Pemakaian:
    python3 periksa_draf.py --pengetahuan cs/PENGETAHUAN.md --draf draf.txt
    python3 periksa_draf.py --pengetahuan cs/PENGETAHUAN.md --draf -   (baca draf dari stdin)

Keluaran: ringkasan teks + JSON di baris terakhir (mudah dibaca skrip lain).
Exit code: 0 = bersih, 1 = ada temuan yang perlu dicek manusia, 2 = error input.
"""

import argparse
import json
import re
import sys


def baca_teks(path):
    if path == "-":
        return sys.stdin.read()
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        print(f"Error: file tidak ditemukan: {path}", file=sys.stderr)
        sys.exit(2)
    except OSError as e:
        print(f"Error membaca {path}: {e}", file=sys.stderr)
        sys.exit(2)


# ---------------------------------------------------------------------------
# 1. Deteksi nominal Rupiah (dengan/tanpa "Rp", dengan/tanpa pengali rb/jt)
# ---------------------------------------------------------------------------

KATA_PENGALI = {
    "rb": 1_000, "ribu": 1_000, "k": 1_000,
    "jt": 1_000_000, "juta": 1_000_000,
}
KATA_KUNCI_HARGA = r"harga|cuma|hanya|jadi|total|ongkir|diskon|promo"

# Satu pola gabungan: [kata kunci harga]? [Rp]? angka [pengali]?
# Angka ikut dianggap "nominal Rupiah" HANYA bila didahului kata kunci
# harga, dan/atau didahului "Rp", dan/atau diikuti pengali (rb/ribu/k/jt/
# juta) -- supaya nomor pesanan/tanggal/HP biasa tidak ikut tertangkap.
POLA_NOMINAL = re.compile(
    r"(?:(?P<kw>" + KATA_KUNCI_HARGA + r")\w*\s+)?"
    r"(?:(?P<rp>Rp\.?)\s*)?"
    r"(?P<num>\d[\d.,]*)"
    r"(?:\s*(?P<mult>ribu|rb|k|juta|jt)\b)?",
    re.IGNORECASE,
)


def normalisasi_angka(mentah):
    """Ubah '22.000' / '22,000' / '22000' / '22.000,50' jadi integer rupiah.
    Aturan: titik/koma sebagai ribuan bila diikuti persis 3 digit lalu batas.
    Sisa titik/koma (desimal) dibuang, dibulatkan ke bawah."""
    s = mentah.strip().rstrip(".,")
    if not s:
        return None
    bersih = re.sub(r"[.,](?=\d{3}(\D|$))", "", s)
    bersih = re.split(r"[.,]", bersih)[0]
    if not bersih.isdigit():
        return None
    try:
        return int(bersih)
    except ValueError:
        return None


def normalisasi_dengan_pengali(mentah, kata_pengali):
    """Ubah angka pendek + kata pengali ('89'+'rb', '1,5'+'juta', '2'+'jt')
    jadi integer rupiah. Koma/titik diikuti 1-2 digit di akhir dianggap
    desimal (mis. '1,5'); selain itu dianggap pemisah ribuan biasa."""
    s = mentah.strip().rstrip(".,")
    faktor = KATA_PENGALI.get(kata_pengali.lower())
    if faktor is None or not s:
        return None
    m = re.match(r"^(\d+)[.,](\d{1,2})$", s)
    if m:
        angka = float(f"{m.group(1)}.{m.group(2)}")
    else:
        bersih = re.sub(r"[.,]", "", s)
        if not bersih.isdigit():
            return None
        angka = float(bersih)
    return int(angka * faktor)


def ekstrak_nominal(teks):
    """Ambil semua nominal Rupiah yang disebut eksplisit di teks: didahului
    'Rp', didahului kata kunci harga (harga/cuma/hanya/jadi/total/ongkir/
    diskon/promo), dan/atau diikuti pengali (rb/ribu/k/jt/juta)."""
    hasil = set()
    for m in POLA_NOMINAL.finditer(teks):
        kw, rp, num, mult = m.group("kw"), m.group("rp"), m.group("num"), m.group("mult")
        if not (kw or rp or mult):
            continue  # angka biasa (tanggal, nomor pesanan, dll.) -> abaikan
        if mult:
            angka = normalisasi_dengan_pengali(num, mult)
        else:
            angka = normalisasi_angka(num)
        if angka is not None and angka > 0:
            hasil.add(angka)
    return hasil


# ---------------------------------------------------------------------------
# 2. Deteksi data sensitif (dengan pengurangan positif palsu)
# ---------------------------------------------------------------------------

KATA_NEGASI = re.compile(r"\b(jangan|tidak perlu|tidak usah|hindari|dilarang|mohon jangan)\b", re.IGNORECASE)
KATA_KONTEKS_PESANAN = re.compile(r"\b(pesanan|order|resi|invoice|faktur)\b", re.IGNORECASE)
PEMISAH_KALIMAT = re.compile(r"[.!?\n]")


def kalimat_sekitar(teks, posisi):
    """Kalimat yang memuat posisi karakter `posisi` (dibatasi tanda baca akhir kalimat)."""
    awal = 0
    for m in PEMISAH_KALIMAT.finditer(teks, 0, posisi):
        awal = m.end()
    akhir_match = PEMISAH_KALIMAT.search(teks, posisi)
    akhir = akhir_match.start() if akhir_match else len(teks)
    return teks[awal:akhir]


def cuplikan_di(teks, start, end, lebar=15):
    return teks[max(0, start - lebar): end + lebar].strip()


def cek_data_sensitif(teks):
    temuan = []
    span_terpakai = []  # (start, end) yang sudah dilaporkan, untuk cegah dobel

    def tumpang_tindih(a, b):
        return a[0] < b[1] and b[0] < a[1]

    def tambah(label, start, end):
        span = (start, end)
        if any(tumpang_tindih(span, s) for s in span_terpakai):
            return
        span_terpakai.append(span)
        temuan.append({"jenis": label, "cuplikan": cuplikan_di(teks, start, end)})

    # NIK 16 digit persis -- kecuali konteksnya jelas nomor pesanan/resi/invoice
    for m in re.finditer(r"\b\d{16}\b", teks):
        konteks = teks[max(0, m.start() - 25): m.start()]
        if KATA_KONTEKS_PESANAN.search(konteks):
            continue
        tambah("NIK/nomor identitas 16 digit", m.start(), m.end())

    # Nomor kartu 13-19 digit (boleh berspasi/strip) -- lewati bila sudah
    # ditangkap sebagai NIK (span tumpang tindih otomatis dilewati oleh
    # tambah()), dan lewati bila konteksnya nomor pesanan/resi/invoice.
    for m in re.finditer(r"\b(?:\d[ -]?){13,19}\b", teks):
        konteks = teks[max(0, m.start() - 25): m.start()]
        if KATA_KONTEKS_PESANAN.search(konteks):
            continue
        tambah("Nomor kartu (mirip kartu debit/kredit)", m.start(), m.end())

    # Kata kunci OTP/PIN/password/CVV -- lewati bila kalimatnya peringatan
    # ("jangan kirim kode OTP ke siapa pun", dsb.)
    pola_kata = [
        ("Kata kunci OTP", re.compile(r"\bOTP\b", re.IGNORECASE)),
        ("Kata kunci PIN", re.compile(r"\bPIN\b", re.IGNORECASE)),
        ("Kata kunci password/kata sandi", re.compile(r"\b(password|kata sandi)\b", re.IGNORECASE)),
        ("CVV/CVC kartu", re.compile(r"\bcvv\b|\bcvc\b", re.IGNORECASE)),
    ]
    for label, pola in pola_kata:
        for m in pola.finditer(teks):
            kalimat = kalimat_sekitar(teks, m.start())
            if KATA_NEGASI.search(kalimat):
                continue  # kalimat peringatan, bukan bocor data
            if label == "Kata kunci PIN":
                setelah = teks[m.end(): m.end() + 12].strip().lower()
                if setelah.startswith("lokasi"):
                    continue  # "kirim pin lokasi" = titik lokasi, bukan PIN rahasia
            tambah(label, m.start(), m.end())

    # Kode OTP/verifikasi berupa angka 4-6 digit di dekat kata "kode"/
    # "verifikasi", TANPA harus menyebut kata "OTP" secara eksplisit.
    for m in re.finditer(
        r"\b(?:kode|verifikasi)\w*\b[^\d]{0,15}(\d{4,6})\b", teks, re.IGNORECASE
    ):
        kalimat = kalimat_sekitar(teks, m.start())
        if KATA_NEGASI.search(kalimat):
            continue
        tambah("Kode verifikasi/OTP (angka) tanpa kata 'OTP' eksplisit", m.start(1), m.end(1))

    return temuan


def main():
    ap = argparse.ArgumentParser(description="Periksa draf balasan CS sebelum dikirim (harga & data sensitif; TIDAK memeriksa stok).")
    ap.add_argument("--pengetahuan", required=True, help="Path ke cs/PENGETAHUAN.md")
    ap.add_argument("--draf", required=True, help="Path ke file draf balasan, atau - untuk stdin")
    args = ap.parse_args()

    teks_pengetahuan = baca_teks(args.pengetahuan)
    teks_draf = baca_teks(args.draf)

    nominal_pengetahuan = ekstrak_nominal(teks_pengetahuan)
    nominal_draf = ekstrak_nominal(teks_draf)
    nominal_tidak_ditemukan = sorted(nominal_draf - nominal_pengetahuan)

    temuan_sensitif = cek_data_sensitif(teks_draf)

    bersih = not nominal_tidak_ditemukan and not temuan_sensitif

    print("=== Hasil periksa draf (harga & data sensitif -- STOK TIDAK diperiksa) ===")
    if nominal_tidak_ditemukan:
        print(f"[PERIKSA] {len(nominal_tidak_ditemukan)} nominal di draf TIDAK ditemukan di basis pengetahuan:")
        for n in nominal_tidak_ditemukan:
            print(f"  - Rp {n:,}".replace(",", "."))
        print("  -> Cek manual: mungkin salah ketik, atau memang belum ada di PENGETAHUAN.md (jangan kirim sebelum dicek).")
    else:
        print("[OK] Semua nominal Rupiah di draf ditemukan di basis pengetahuan (atau draf tidak menyebut nominal).")

    if temuan_sensitif:
        print(f"[PERIKSA] {len(temuan_sensitif)} kemungkinan data sensitif di draf:")
        for t in temuan_sensitif:
            print(f"  - {t['jenis']}: ...{t['cuplikan']}...")
        print("  -> Jangan kirim data ini ke pelanggan lewat chat biasa; arahkan ke kanal resmi/eskalasi.")
    else:
        print("[OK] Tidak ada pola data sensitif (NIK/kartu/OTP/PIN/password) terdeteksi di draf.")

    print("[INGAT] Klaim STOK ('tinggal 2', 'masih ada', dst.) TIDAK diperiksa script ini -- cek manual ke data toko.")

    hasil_json = {
        "bersih": bersih,
        "nominal_tidak_ditemukan_di_pengetahuan": nominal_tidak_ditemukan,
        "data_sensitif_terdeteksi": temuan_sensitif,
        "catatan": "Script tidak memeriksa klaim stok.",
    }
    print(json.dumps(hasil_json, ensure_ascii=False))

    sys.exit(0 if bersih else 1)


if __name__ == "__main__":
    main()
