#!/usr/bin/env python3
"""
periksa_draf.py — Memeriksa draf balasan CS sebelum dikirim admin.

Memeriksa DUA hal, hanya dengan Python standar (tanpa dependensi luar):
1. Nominal Rupiah yang disebut di draf tapi TIDAK ditemukan di basis
   pengetahuan (cs/PENGETAHUAN.md) -> potensi mengarang HARGA.
   Menangkap: "Rp 22.000" / "IDR 79.000", harga berpengali ("89rb", "2 jt",
   "1,5 juta"), angka berpemisah ribuan format titik di mana pun disebut
   ("Pashmina Ceruti 79.000", "89.000" di basis pengetahuan meski tanpa
   "Rp"), dan angka polos >=4 digit bila ada kata kunci harga di kalimat
   yang sama ("harganya jadi 199000"). Persentase, satuan (pcs/kg/kali/dst.),
   dan tahun (19xx/20xx) SENGAJA dikecualikan supaya tidak salah tangkap.
2. Pola data sensitif di draf (mirip NIK/KTP 16 digit, nomor kartu, kode
   OTP/verifikasi, PIN, password) -> jangan sampai bocor balik ke pelanggan.
   Kalimat "peringatan" (mengandung "jangan", "tidak pernah", dst.) hanya
   dikecualikan bila kalimat itu TIDAK memuat kode/angka 4-8 digit -- kalau
   ada angkanya, tetap ditandai (itu kebocoran nyata, bukan sekadar imbauan).

**PENTING — yang TIDAK diperiksa script ini:** STOK tidak diperiksa sama
sekali (tidak ada cara membedakan klaim stok dari angka lain secara aman).
Klaim stok ("tinggal 2", "masih ada", "sudah habis") tetap wajib dicek
manual oleh admin terhadap `PENGETAHUAN.md` / data toko sebenarnya.

Pemakaian:
    python3 periksa_draf.py --pengetahuan cs/PENGETAHUAN.md --draf draf.txt
    python3 periksa_draf.py --pengetahuan cs/PENGETAHUAN.md --draf -   (baca draf dari stdin)

Keluaran: ringkasan teks + JSON di baris terakhir (mudah dibaca skrip lain).
Exit code: 0 = bersih, 1 = ada temuan yang perlu dicek manusia, 2 = error input
(file tidak ada / tidak bisa dibaca sebagai teks sama sekali).
"""

import argparse
import json
import re
import sys

ENKODING_DICOBA = ("utf-8-sig", "utf-8", "cp1252", "latin-1")


def baca_teks(path):
    """Baca file (atau stdin bila path == '-') sebagai teks. Dicoba beberapa
    enkoding berurutan (UTF-8 -> Windows-1252 -> Latin-1) supaya basis
    pengetahuan yang disimpan dari Excel/Notepad Windows tetap terbaca,
    bukan menyebabkan traceback. Bila semuanya gagal -> exit 2 (bukan
    exit 1, supaya tidak tertukar dengan arti 'ada temuan')."""
    try:
        if path == "-":
            data = sys.stdin.buffer.read()
        else:
            with open(path, "rb") as f:
                data = f.read()
    except FileNotFoundError:
        print(f"Error: file tidak ditemukan: {path}", file=sys.stderr)
        sys.exit(2)
    except OSError as e:
        print(f"Error membaca {path}: {e}", file=sys.stderr)
        sys.exit(2)

    for enc in ENKODING_DICOBA:
        try:
            return data.decode(enc)
        except (UnicodeDecodeError, LookupError):
            continue

    print(
        f"Error: {path} tidak bisa dibaca sebagai teks (bukan UTF-8/Windows-1252/Latin-1 yang valid). "
        "Simpan ulang file sebagai teks biasa (UTF-8) lalu coba lagi.",
        file=sys.stderr,
    )
    sys.exit(2)


# ---------------------------------------------------------------------------
# 1. Deteksi nominal Rupiah
# ---------------------------------------------------------------------------

KATA_PENGALI = {
    "rb": 1_000, "ribu": 1_000, "k": 1_000,
    "jt": 1_000_000, "juta": 1_000_000,
}
KATA_KUNCI_HARGA = r"harga|cuma|hanya|jadi|total|ongkir|diskon|promo|aja|saja"

UNIT_KUANTITAS = (
    r"pcs?|buah|pasang|orang|porsi|lembar|botol|kg|gram|gr|ml|liter|cm|mm|"
    r"meter|m2|hari|jam|menit|kali|x|unit"
)


def diikuti_non_uang(teks, posisi_setelah):
    """True bila persis setelah angka ada tanda persen atau satuan kuantitas
    (pcs, kg, hari, kali, dst.) -- berarti itu jumlah/ukuran, bukan harga."""
    ekor = teks[posisi_setelah: posisi_setelah + 20].lstrip(" \t")
    if ekor.startswith("%"):
        return True
    if re.match(r"^[/\-]?\s*(?:" + UNIT_KUANTITAS + r")\b", ekor, re.IGNORECASE):
        return True
    return False


def sepertinya_tahun(angka_mentah):
    return bool(re.match(r"^(19|20)\d{2}$", angka_mentah))


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
    """Ambil semua nominal Rupiah yang disebut di teks lewat 4 pola:
    (1) diawali 'Rp'/'IDR', (2) angka + pengali rb/ribu/k/jt/juta,
    (3) angka berpemisah ribuan format titik ('79.000') di mana pun --
    tidak perlu kata kunci, supaya harga tanpa 'Rp' & tanpa bersebelahan
    dengan kata kunci (mis. nama produk di antaranya) tetap tertangkap,
    (4) angka polos >=4 digit HANYA bila ada kata kunci harga di kalimat
    yang sama (dan bukan pola tahun 19xx/20xx)."""
    hasil = set()

    # (1) Rp / IDR -- boleh langsung diikuti pengali ("Rp 89rb"). Tidak
    # difilter oleh diikuti_non_uang(): "Rp"/pengali sudah jadi penanda uang
    # yang jelas, walau diikuti "/pcs" dsb. (harga per satuan, mis. "55rb/pcs").
    for m in re.finditer(
        r"(?:Rp|IDR)\.?\s*(\d[\d.,]*)\s*(ribu|rb|k|juta|jt)?\b", teks, re.IGNORECASE
    ):
        num, mult = m.group(1), m.group(2)
        angka = normalisasi_dengan_pengali(num, mult) if mult else normalisasi_angka(num)
        if angka:
            hasil.add(angka)

    # (2) angka + pengali tanpa "Rp" di depan (mis. "55rb/pcs", "1,5 juta")
    for m in re.finditer(r"\b(\d+(?:[.,]\d{1,2})?)\s*(ribu|rb|k|juta|jt)\b", teks, re.IGNORECASE):
        angka = normalisasi_dengan_pengali(m.group(1), m.group(2))
        if angka:
            hasil.add(angka)

    # (3) angka berpemisah ribuan (titik), berdiri sendiri
    for m in re.finditer(r"\b\d{1,3}(?:\.\d{3})+\b", teks):
        if diikuti_non_uang(teks, m.end()):
            continue
        angka = normalisasi_angka(m.group(0))
        if angka and angka >= 1000:
            hasil.add(angka)

    # (4) angka polos >=4 digit, hanya bila ada kata kunci harga di kalimat yang sama
    for kalimat in re.split(r"(?<=[.!?\n])", teks):
        if not re.search(KATA_KUNCI_HARGA, kalimat, re.IGNORECASE):
            continue
        for m in re.finditer(r"\b\d{4,}\b", kalimat):
            if sepertinya_tahun(m.group(0)):
                continue
            if diikuti_non_uang(kalimat, m.end()):
                continue
            angka = normalisasi_angka(m.group(0))
            if angka:
                hasil.add(angka)

    return hasil


# ---------------------------------------------------------------------------
# 2. Deteksi data sensitif (dengan pengurangan positif palsu)
# ---------------------------------------------------------------------------

KATA_NEGASI = re.compile(
    r"\b(jangan|tidak perlu|tidak usah|tidak pernah|hindari|dilarang|mohon jangan)\b",
    re.IGNORECASE,
)
KATA_KONTEKS_PESANAN = re.compile(r"\b(pesanan|order|resi|invoice|faktur)\b", re.IGNORECASE)
KATA_NIK_KTP = re.compile(r"\b(NIK|KTP)\b", re.IGNORECASE)
PEMISAH_KALIMAT = re.compile(r"[.!?\n]")


def kalimat_sekitar(teks, posisi):
    """Kalimat yang memuat posisi karakter `posisi` (dibatasi tanda baca akhir kalimat)."""
    awal = 0
    for m in PEMISAH_KALIMAT.finditer(teks, 0, posisi):
        awal = m.end()
    akhir_match = PEMISAH_KALIMAT.search(teks, posisi)
    akhir = akhir_match.start() if akhir_match else len(teks)
    return teks[awal:akhir]


def kalimat_ada_kode(kalimat):
    """True bila kalimat memuat angka 4-8 digit -- dipakai untuk membatalkan
    pengecualian kalimat peringatan (mis. 'jangan share kode OTP 482913'
    tetap harus ditandai, walau ada kata 'jangan')."""
    return re.search(r"\b\d{4,8}\b", kalimat) is not None


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

    # NIK 16 digit persis. Prioritas: bila kata "NIK"/"KTP" eksplisit ada
    # tepat sebelum angka -> SELALU ditandai (mengalahkan konteks pesanan).
    # Baru kalau tidak ada label NIK/KTP, konteks "pesanan/order/resi/
    # invoice/faktur" di dekatnya membebaskan dari tanda (nomor pesanan).
    for m in re.finditer(r"\b\d{16}\b", teks):
        konteks = teks[max(0, m.start() - 30): m.start()]
        if KATA_NIK_KTP.search(konteks):
            tambah("NIK/nomor identitas 16 digit", m.start(), m.end())
            continue
        if KATA_KONTEKS_PESANAN.search(konteks):
            continue
        tambah("NIK/nomor identitas 16 digit", m.start(), m.end())

    # Nomor kartu 13-19 digit (boleh berspasi/strip) -- aturan sama.
    for m in re.finditer(r"\b(?:\d[ -]?){13,19}\b", teks):
        konteks = teks[max(0, m.start() - 30): m.start()]
        if KATA_NIK_KTP.search(konteks):
            tambah("Nomor kartu (mirip kartu debit/kredit)", m.start(), m.end())
            continue
        if KATA_KONTEKS_PESANAN.search(konteks):
            continue
        tambah("Nomor kartu (mirip kartu debit/kredit)", m.start(), m.end())

    # Kata kunci OTP/PIN/password/CVV -- kalimat "peringatan" (jangan/tidak
    # pernah/dst.) dikecualikan HANYA bila kalimat itu tidak memuat kode
    # angka 4-8 digit; kalau ada angkanya, tetap ditandai (kebocoran nyata).
    pola_kata = [
        ("Kata kunci OTP", re.compile(r"\bOTP\b", re.IGNORECASE)),
        ("Kata kunci PIN", re.compile(r"\bPIN\b", re.IGNORECASE)),
        ("Kata kunci password/kata sandi", re.compile(r"\b(password|kata sandi)\b", re.IGNORECASE)),
        ("CVV/CVC kartu", re.compile(r"\bcvv\b|\bcvc\b", re.IGNORECASE)),
    ]
    for label, pola in pola_kata:
        for m in pola.finditer(teks):
            kalimat = kalimat_sekitar(teks, m.start())
            if KATA_NEGASI.search(kalimat) and not kalimat_ada_kode(kalimat):
                continue  # kalimat peringatan tanpa kode -> bukan bocor data
            if label == "Kata kunci PIN":
                setelah = teks[m.end(): m.end() + 12].strip().lower()
                if setelah.startswith("lokasi"):
                    continue  # "kirim pin lokasi" = titik lokasi, bukan PIN rahasia
            tambah(label, m.start(), m.end())

    # Kode OTP/verifikasi berupa angka 4-6 digit di dekat kata "kode"/
    # "verifikasi", TANPA harus menyebut kata "OTP" eksplisit. Dikecualikan
    # bila kata "kode" diikuti "pos/booking/promo/voucher/referral/unik/
    # produk/diskon" (bukan kode keamanan).
    for m in re.finditer(
        r"\b(?:kode(?!\s+(?:pos|booking|promo|voucher|referral|unik|produk|diskon))\w*|verifikasi\w*)\b"
        r"[^\d]{0,15}(\d{4,6})\b",
        teks,
        re.IGNORECASE,
    ):
        kalimat = kalimat_sekitar(teks, m.start())
        if KATA_NEGASI.search(kalimat) and not kalimat_ada_kode(kalimat):
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
