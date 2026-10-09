#!/usr/bin/env python3
"""Alokasi anggaran iklan bulanan per kanal & minggu untuk UMKM Indonesia.

Hanya library standar Python 3.8+. Lintas OS (Windows: `python` atau `py`).
Semua uang memakai decimal.Decimal (tanpa float). Rupiah dibulatkan ke rupiah terdekat
(setengah ke atas); total SELALU sama dengan anggaran: selisih pembulatan ditampilkan dan
ditambahkan ke bagian terbesar. Tidak ada prediksi hasil: yang dihitung hanya pembagian
uang, batas impas, dan batas uji.

Contoh:
  python3 alokasi_anggaran.py --anggaran 10jt --tujuan penjualan --aov 150rb --margin 40%
"""
import argparse
import json
import re
import sys
from decimal import Decimal, ROUND_HALF_UP, ROUND_CEILING, getcontext

getcontext().prec = 40

NOL, SERATUS = Decimal(0), Decimal(100)
HARI_PER_MINGGU = 7
PORSI_CPA_AMAN = Decimal("0.7")   # target CPA = 70% laba kotor per pesanan (30% sisa)
PORSI_UJI = Decimal("0.3")        # 30% anggaran kanal untuk uji kreatif/audiens

KANAL = ["meta", "tiktok", "shopee", "tiktokshop", "google"]
NAMA_KANAL = {"meta": "Meta (IG/FB)", "tiktok": "TikTok Ads", "shopee": "Shopee Ads",
              "tiktokshop": "TikTok Shop Ads", "google": "Google Ads"}
# Titik awal pembagian (persen relatif), bukan hasil riset pasti. 0 = tidak dipakai untuk tujuan itu.
BOBOT = {
    "penjualan": {"meta": 35, "tiktok": 20, "shopee": 20, "tiktokshop": 15, "google": 10},
    "awareness": {"meta": 40, "tiktok": 40, "shopee": 5, "tiktokshop": 5, "google": 10},
    "leads":     {"meta": 55, "tiktok": 15, "shopee": 0, "tiktokshop": 0, "google": 30},
}
# Batas uji: anggaran MINIMAL per iklan per hari (aturan praktis Komunitech, BUKAN syarat platform).
MIN_HARIAN = {"meta": 25000, "tiktok": 30000, "shopee": 10000, "tiktokshop": 20000, "google": 25000}

# Kata kunci (awalan kata) yang memicu catatan kategori terbatas.
KATA_KATEGORI = {
    "kesehatan": ["kesehatan", "skincare", "kosmetik", "kecantikan", "suplemen", "vitamin", "herbal", "jamu",
                  "obat", "klinik", "farmasi", "apotek", "dokter", "rumah sakit", "diet", "perawatan kulit"],
    "keuangan": ["keuangan", "pinjaman", "pinjol", "investasi", "asuransi", "kredit", "koperasi", "saham"],
    "kripto": ["kripto", "crypto", "aset digital", "bitcoin"],
}
ALIAS_KANAL = {
    "meta": "meta", "ig": "meta", "instagram": "meta", "fb": "meta", "facebook": "meta",
    "tiktok": "tiktok", "tt": "tiktok",
    "shopee": "shopee",
    "tiktokshop": "tiktokshop", "tokopedia": "tiktokshop", "tokped": "tiktokshop",
    "google": "google", "gads": "google",
}
MARKETPLACE = ["shopee", "tiktokshop"]
# Kanal penjualan utama (tempat pembeli bertransaksi) mendapat bobot = 2x bobot kanal pendukung terbesar.
PENGALI_UTAMA = 2
JENIS = ["umum", "marketplace", "jasa-lokal"]
# Urutan prioritas kanal bila anggaran kecil memaksa memilih (paling cocok dulu). 'umum' = menurut bobot tujuan.
PRIORITAS = {
    "marketplace": ["shopee", "tiktokshop", "meta", "tiktok", "google"],
    "jasa-lokal": ["google", "meta", "tiktok", "shopee", "tiktokshop"],
}
NAMA_JENIS = {"umum": "usaha umum", "marketplace": "penjualan marketplace", "jasa-lokal": "jasa lokal"}

DILARANG = ["judi", "togel", "slot online", "rokok", "vape", "miras", "narkoba", "senjata",
            "obat keras", "pinjol ilegal", "gambling", "casino", "porn", "bokep"]
CATATAN_KATEGORI = {
    "kesehatan": "Kategori TERBATAS: iklan layanan/produk kesehatan (obat, suplemen, klinik, kosmetik) "
                 "punya aturan platform dan aturan iklan kesehatan Indonesia; hindari klaim sembuh, "
                 "foto sebelum/sesudah, dan testimoni medis. Baca kebijakan iklan resmi platform "
                 "sebelum tayang dan konsultasikan ke tenaga kesehatan/pihak berwenang.",
    "keuangan": "Kategori TERBATAS: pinjaman, investasi, asuransi, dan jasa keuangan umumnya butuh "
                "izin/verifikasi platform dan izin resmi (OJK). Jangan menjanjikan untung/bunga pasti. "
                "Baca kebijakan iklan resmi platform sebelum tayang.",
    "kripto": "Kategori TERBATAS: iklan kripto/aset digital dilarang atau butuh izin/verifikasi di "
              "banyak platform. Jangan menjanjikan profit. Cek kebijakan iklan terbaru tiap platform "
              "dan aturan pedagang aset kripto di Indonesia sebelum tayang.",
}


class Gagal(ValueError):
    """Input tidak bisa dibaca / ambigu -> dihentikan dengan pesan jelas."""


# --------------------------------------------------------------------------------------
# Parsing angka format Indonesia
# --------------------------------------------------------------------------------------
SATUAN = {"rb": 10 ** 3, "ribu": 10 ** 3, "k": 10 ** 3, "jt": 10 ** 6, "juta": 10 ** 6,
          "miliar": 10 ** 9, "milyar": 10 ** 9}
_RE_RUPIAH = re.compile(r"(?:(?:rp|idr)\.?\s*)?(\d[\d.,]*)\s*([a-z]+)?", re.I)
_TITIK_RIBU = re.compile(r"[1-9]\d{0,2}(\.\d{3})+")


def parse_rupiah(teks, nama="nilai"):
    """'1.500.000', '1,5jt', '500rb', 'Rp2 juta' -> int rupiah. Ambigu/rusak -> Gagal."""
    s = str(teks).replace(" ", " ").strip().lower()
    s = re.sub(r"[.,]-$", "", s)          # 'Rp 3.000.000,-' -> 'rp 3.000.000'
    m = _RE_RUPIAH.fullmatch(s)
    if not m:
        raise Gagal(f"{nama} '{teks}' tidak terbaca. Contoh yang benar: 1.500.000 | 1,5jt | 500rb | 2 juta.")
    angka, satuan = m.group(1), m.group(2)
    if satuan is not None:
        if satuan == "m":
            raise Gagal(f"{nama} '{teks}': huruf 'M' bisa berarti juta atau miliar. Tulis 'jt'/'juta' atau 'miliar'.")
        if satuan not in SATUAN:
            raise Gagal(f"{nama} '{teks}': satuan '{satuan}' tidak dikenal. Pakai rb/ribu, jt/juta, atau miliar.")
    ada_titik, ada_koma = "." in angka, "," in angka
    if not ada_titik and not ada_koma:
        nilai = Decimal(angka)
    elif ada_titik and ada_koma:
        if not re.fullmatch(r"[1-9]\d{0,2}(\.\d{3})+,\d+", angka):
            raise Gagal(f"{nama} '{teks}' ambigu. Pakai titik untuk ribuan dan koma untuk desimal (1.500.000 atau 1,5jt).")
        nilai = Decimal(angka.replace(".", "").replace(",", "."))
    elif ada_titik:
        if not _TITIK_RIBU.fullmatch(angka):
            raise Gagal(f"{nama} '{teks}' ambigu: titik dipakai sebagai pemisah ribuan (1.500.000). "
                        "Untuk desimal pakai koma (1,5jt).")
        if satuan is not None:
            raise Gagal(f"{nama} '{teks}' ambigu (1.500jt = 1.500 juta atau 1,5 juta?). "
                        "Tulis '1,5jt' atau angka penuh.")
        nilai = Decimal(angka.replace(".", ""))
    else:  # hanya koma
        if angka.count(",") > 1:
            raise Gagal(f"{nama} '{teks}' ambigu (koma berulang). Pakai titik untuk ribuan: 1.500.000.")
        depan, belakang = angka.split(",")
        if not belakang:
            raise Gagal(f"{nama} '{teks}' tidak terbaca (koma tanpa angka di belakangnya).")
        if len(belakang) == 3:
            raise Gagal(f"{nama} '{teks}' ambigu: '{angka}' bisa ribuan (gaya Inggris) atau desimal. "
                        "Tulis 1.500 / 1500 untuk seribu lima ratus, atau 1,5jt untuk satu setengah juta.")
        if satuan is None:
            raise Gagal(f"{nama} '{teks}': desimal tanpa satuan tidak dipakai. Tulis angka bulat rupiah "
                        "(mis. 1500) atau pakai satuan (1,5rb).")
        nilai = Decimal(depan + "." + belakang)
    if satuan is not None:
        nilai *= SATUAN[satuan]
    if nilai != nilai.to_integral_value():
        raise Gagal(f"{nama} '{teks}' menghasilkan pecahan rupiah. Tulis angka bulat rupiah.")
    if nilai <= 0:
        raise Gagal(f"{nama} '{teks}' harus lebih dari 0.")
    return int(nilai)


def parse_persen(teks, nama="persen"):
    """'40', '40%', '32,5%' -> Decimal persen (0 < p <= 100). Nilai <= 1 tanpa '%' dianggap ambigu."""
    s = str(teks).strip().lower().replace(" ", "")
    ada_persen = s.endswith("%")
    if ada_persen:
        s = s[:-1]
    if not re.fullmatch(r"\d+(?:[.,]\d+)?", s):
        raise Gagal(f"{nama} '{teks}' tidak terbaca. Contoh: 40 atau 40% atau 32,5%.")
    if s.count(".") + s.count(",") == 1 and re.fullmatch(r"\d{1,3}[.,]\d{3}", s):
        raise Gagal(f"{nama} '{teks}' ambigu. Tulis persen dengan 1-2 angka desimal (mis. 32,5%).")
    p = Decimal(s.replace(",", "."))
    if p <= 0 or p > 100:
        raise Gagal(f"{nama} '{teks}' harus lebih dari 0 dan paling tinggi 100%.")
    if p <= 1 and not ada_persen:
        alt = format((p * SERATUS).normalize(), "f").replace(".", ",")
        asli = format(p.normalize(), "f").replace(".", ",")
        raise Gagal(f"{nama} '{teks}' ambigu: {teks} berarti {asli}% atau {alt}%? "
                    f"Tulis '{alt}%' (atau '{asli}%').")
    return p


def parse_margin(teks):
    """Seperti parse_persen, tetapi margin nol/negatif dijelaskan (setiap penjualan rugi)."""
    s = str(teks).strip().lower().replace(" ", "").replace(",", ".")
    if s.endswith("%"):
        s = s[:-1]
    try:
        nilai = Decimal(s)
    except Exception:
        nilai = None
    if nilai is not None and nilai <= 0:
        raise Gagal(f"--margin '{teks}': margin nol atau negatif berarti SETIAP penjualan rugi sebelum biaya iklan. "
                    "Iklan tidak akan menolong: perbaiki harga jual atau harga pokok dulu (lihat skill "
                    "strategi-harga-produk / hitung-hpp), lalu hitung ulang.")
    return parse_persen(teks, "--margin")


def parse_tujuan(teks):
    """'penjualan' -> {'penjualan': 100}; 'awareness:30,penjualan:70' -> porsi (total wajib 100)."""
    bagian = [x.strip() for x in re.split(r"[,;]", str(teks).lower()) if x.strip()]
    if not bagian:
        raise Gagal("--tujuan kosong. Pilihan: penjualan, awareness, leads, atau campuran (awareness:30,penjualan:70).")
    if len(bagian) == 1 and ":" not in bagian[0]:
        if bagian[0] not in BOBOT:
            raise Gagal(f"--tujuan '{bagian[0]}' tidak dikenal. Pilihan: {', '.join(sorted(BOBOT))}, "
                        "atau campuran dengan porsi (mis. awareness:30,penjualan:70).")
        return {bagian[0]: 100}
    porsi = {}
    for b in bagian:
        if b.count(":") != 1:
            raise Gagal(f"--tujuan '{b}' salah format. Tujuan campuran ditulis nama:persen, mis. awareness:30,penjualan:70.")
        nama, angka = [x.strip() for x in b.split(":")]
        if nama not in BOBOT:
            raise Gagal(f"--tujuan '{nama}' tidak dikenal. Pilihan: {', '.join(sorted(BOBOT))}.")
        angka = angka.rstrip("%").strip()
        if not re.fullmatch(r"[1-9]\d{0,2}", angka):
            raise Gagal(f"--tujuan porsi '{angka}' untuk {nama} harus bilangan bulat lebih dari 0.")
        if nama in porsi:
            raise Gagal(f"--tujuan: '{nama}' disebut dua kali.")
        porsi[nama] = int(angka)
    if sum(porsi.values()) != 100:
        raise Gagal(f"--tujuan: total porsi {sum(porsi.values())}%, harus tepat 100% "
                    "(mis. awareness:30,penjualan:70).")
    return porsi


def bobot_gabungan(porsi):
    """Bobot kanal = rata-rata tertimbang bobot tiap tujuan menurut porsinya."""
    return {k: Decimal(sum(p * BOBOT[t][k] for t, p in porsi.items())) / 100 for k in KANAL}


def parse_kanal(teks):
    """'meta,ig, tiktok shop' -> ['meta','tiktokshop'] (alias diterima), plus catatan alias."""
    hasil, catatan = [], []

    def norm(t):
        t = re.sub(r"[-_\s]", "", t.strip().lower())
        return t[:-3] if t.endswith("ads") and t[:-3] in ALIAS_KANAL else t
    for potong in re.split(r"[,;]", teks):
        if not potong.strip():
            continue
        bagian = [potong] if norm(potong) in ALIAS_KANAL else potong.split()
        for t in bagian:
            n = norm(t)
            if n not in ALIAS_KANAL:
                raise Gagal(f"--kanal '{t.strip()}' tidak dikenal. Pilihan: {', '.join(KANAL)} "
                            "(alias: ig, instagram, fb, facebook, tiktok shop, tokopedia, google ads).")
            k = ALIAS_KANAL[n]
            if n in ("tokopedia", "tokped"):
                catatan.append("Tokopedia dihitung sebagai TikTok Shop Ads. Cek di Seller Center apakah iklan "
                               "toko Anda dikelola lewat sana.")
            if k not in hasil:
                hasil.append(k)
    return hasil, catatan


# --------------------------------------------------------------------------------------
# Hitung
# --------------------------------------------------------------------------------------
def bulat(x):
    return int(Decimal(x).quantize(Decimal(1), rounding=ROUND_HALF_UP))


def bagi(total, bobot):
    """Bagi `total` (int rupiah) menurut bobot. Tiap bagian dibulatkan ke terdekat; selisih dari
    total ditambahkan ke bagian dengan bobot terbesar (yang pertama bila seri).
    Kembali (daftar_bagian, sisa) dengan sisa = total - jumlah_pembulatan (bisa negatif)."""
    bobot = [Decimal(b) for b in bobot]
    jml = sum(bobot)
    bagian = [bulat(Decimal(total) * b / jml) for b in bobot]
    sisa = total - sum(bagian)
    if sisa:
        bagian[bobot.index(max(bobot))] += sisa
    return bagian, sisa


def layak(b, bobot_minggu, k, min_harian):
    """Kanal layak bila minggu TERKECIL-nya cukup untuk 1 iklan berbatas uji selama 7 hari.
    Dasar yang sama dipakai untuk 'iklan aktif maks' (>= 1 berarti layak)."""
    per_minggu, _ = bagi(b, bobot_minggu)
    return min(per_minggu) >= HARI_PER_MINGGU * min_harian[k]


def pilih_kanal(anggaran, bobot, kanal_diminta, bobot_minggu, min_harian, prioritas, cadangan):
    """Tentukan kanal aktif (kanal_diminta berurutan). Aturan bila uang terlalu tipis:
    1. Saring dengan dasar minggu terkecil (lihat layak()).
    2. Bila kanal berprioritas tertinggi sendiri tidak layak, kanal berprioritas terendah dibuang
       (uang dipusatkan); bila tidak, kanal tidak layak berprioritas terendah yang dibuang. Ulangi.
    3. Bila tersisa satu kanal dan masih tidak layak, cari kanal lain (dari `cadangan`, menurut
       prioritas) yang layak dengan seluruh anggaran.
    Kembali (aktif, dikeluarkan{kanal: alasan}, masih_di_bawah_batas)."""
    aktif = sorted([k for k in kanal_diminta if bobot[k] > 0], key=prioritas.index)
    dikeluarkan = {k: "kurang cocok untuk tujuan ini" for k in kanal_diminta if bobot[k] == 0}
    if not aktif:
        raise Gagal("Tidak ada kanal yang cocok untuk tujuan ini. Untuk 'leads' pakai meta/google/tiktok.")
    awal = aktif[:]
    while True:
        bag, _ = bagi(anggaran, [bobot[k] for k in aktif])
        lemah = [k for k, b in zip(aktif, bag) if not layak(b, bobot_minggu, k, min_harian)]
        if not lemah:
            break
        if len(aktif) == 1:
            for k in awal:
                if k != aktif[0] and k in cadangan and layak(anggaran, bobot_minggu, k, min_harian):
                    dikeluarkan[aktif[0]] = (f"anggaran sebulan tidak cukup untuk menguji di sini; "
                                             f"dialihkan ke {NAMA_KANAL[k]} yang masih layak")
                    dikeluarkan.pop(k, None)
                    aktif = [k]
                    lemah = []
                    break
            break
        buang = aktif[-1] if aktif[0] in lemah else [k for k in aktif if k in lemah][-1]
        if buang in lemah:
            dikeluarkan[buang] = "minggu terkecilnya di bawah batas uji (kurang dari 7 hari x minimum harian)"
        else:
            dikeluarkan[buang] = (f"anggaran dipusatkan ke {NAMA_KANAL[aktif[0]]} (prioritas tertinggi) "
                                  "karena uang terlalu tipis untuk dibagi")
        aktif.remove(buang)
    return [k for k in kanal_diminta if k in aktif], dikeluarkan, bool(lemah)


def tentukan_kanal_utama(a, jenis, kanal_diminta):
    """Kanal tempat penjualan terbanyak terjadi. Dari --kanal-utama; bila kosong dan --jenis marketplace,
    marketplace pertama (Shopee, lalu TikTok Shop) yang ada di kanal yang dipakai. Lainnya None."""
    if getattr(a, "kanal_utama", None):
        daftar, _ = parse_kanal(a.kanal_utama)
        if len(daftar) != 1:
            raise Gagal("--kanal-utama hanya satu kanal (tempat penjualan terbanyak), mis. --kanal-utama shopee.")
        k = daftar[0]
        if k not in kanal_diminta:
            raise Gagal(f"--kanal-utama {NAMA_KANAL[k]} tidak ada di --kanal. Tambahkan ke --kanal atau pilih "
                        "kanal utama lain.")
        return k
    if jenis == "marketplace":
        return next((k for k in MARKETPLACE if k in kanal_diminta), None)
    return None


def hitung(a):
    anggaran = parse_rupiah(a.anggaran, "--anggaran")
    if anggaran < 100000:
        raise Gagal("--anggaran di bawah Rp100.000 per bulan terlalu kecil untuk iklan berbayar. "
                    "Pakai konten organik dulu (lihat skill kalender-konten-30hari).")
    porsi = parse_tujuan(a.tujuan)
    campuran = len(porsi) > 1
    tujuan = next(iter(porsi)) if not campuran else "campuran: " + " + ".join(f"{t} {p}%" for t, p in porsi.items())
    bobot = bobot_gabungan(porsi)
    perlu_aov = "penjualan" in porsi or "leads" in porsi
    minggu = a.minggu
    if not 1 <= minggu <= 5:
        raise Gagal("--minggu harus 1 sampai 5.")
    bobot_minggu = [Decimal(1)] * minggu
    if a.bobot_minggu:
        if len(a.bobot_minggu) != minggu:
            raise Gagal(f"--bobot-minggu harus {minggu} angka (sesuai --minggu), diberi {len(a.bobot_minggu)}.")
        bobot_minggu = []
        for t in a.bobot_minggu:
            if not re.fullmatch(r"[1-9]\d?", t):
                raise Gagal(f"--bobot-minggu '{t}' harus bilangan bulat 1-99.")
            bobot_minggu.append(Decimal(t))

    kanal_diminta, catatan = KANAL[:], []
    if a.kanal:
        kanal_diminta, catatan = parse_kanal(a.kanal)
        if not kanal_diminta:
            raise Gagal("--kanal kosong.")

    kategori = (a.kategori or "umum").strip().lower()
    for kata in DILARANG:
        if kata in kategori:
            raise Gagal(f"Kategori '{a.kategori}' dilarang/sangat dibatasi di platform iklan utama; "
                        "rencana anggaran tidak disusun.")
    cocok = False
    for kunci, teks in CATATAN_KATEGORI.items():
        if any(re.search(r"\b" + re.escape(kata), kategori) for kata in KATA_KATEGORI[kunci]):
            catatan.append(teks)
            cocok = True
    if a.kategori and kategori != "umum" and not cocok:
        catatan.append(f"Kategori '{a.kategori}': cek dulu apakah termasuk kategori terbatas di kebijakan "
                       "iklan resmi tiap platform.")

    min_harian = dict(MIN_HARIAN)
    if a.min_harian:
        m = parse_rupiah(a.min_harian, "--min-harian")
        min_harian = {k: m for k in KANAL}

    # ---- target dari margin & AOV
    target = None
    aov = parse_rupiah(a.aov, "--aov") if a.aov else None
    margin = parse_margin(a.margin) if a.margin else None
    closing = parse_persen(a.closing, "--closing") if a.closing else None
    if "penjualan" in porsi and (aov is None or margin is None):
        raise Gagal("Untuk tujuan 'penjualan' wajib isi --aov (harga rata-rata per pesanan) dan --margin "
                    "(margin kotor, mis. 40%). Tanpa keduanya target CPA/ROAS tidak bisa dihitung.")
    if "leads" in porsi and (aov is None or margin is None or closing is None):
        raise Gagal("Untuk tujuan 'leads' wajib isi --aov (nilai rata-rata satu penjualan), --margin, dan "
                    "--closing (persen calon pembeli yang akhirnya membeli, mis. 20%).")
    if (aov is None) != (margin is None):
        raise Gagal("--aov dan --margin harus diisi berpasangan.")
    if aov is not None:
        m = margin / SERATUS
        laba = Decimal(aov) * m
        target = {
            "aov": aov, "margin_persen": str(margin),
            "laba_kotor_per_pesanan": bulat(laba),
            "roas_impas": str((Decimal(1) / m).quantize(Decimal("0.01"), rounding=ROUND_CEILING)),
            "cpa_impas": bulat(laba),
            "cpa_target": bulat(laba * PORSI_CPA_AMAN),
            "roas_target": str((Decimal(aov) / (laba * PORSI_CPA_AMAN)).quantize(Decimal("0.01"), rounding=ROUND_CEILING)),
        }
        if closing is not None:
            c = closing / SERATUS
            target["closing_persen"] = str(closing)
            target["cpl_impas"] = bulat(laba * c)
            target["cpl_target"] = bulat(laba * c * PORSI_CPA_AMAN)
        target["pesanan_minimal_impas"] = int((Decimal(anggaran) / laba).to_integral_value(rounding=ROUND_CEILING))
        impas = Decimal(target["roas_impas"])
        if impas >= 10:
            catatan.append(f"PERINGATAN margin sangat tipis: ROAS impas {koma(target['roas_impas'])}x (hampir mustahil "
                           "dicapai iklan berbayar). Perbaiki harga jual / harga pokok / biaya dulu (skill "
                           "strategi-harga-produk, hitung-hpp) sebelum menaikkan anggaran iklan.")
        elif impas >= 5:
            catatan.append(f"Margin tipis: ROAS impas {koma(target['roas_impas'])}x cukup berat. Pertimbangkan "
                           "menaikkan harga atau menekan biaya sebelum memperbesar iklan, dan mulai dari anggaran uji kecil.")
    elif not perlu_aov:
        catatan.append("Tanpa --aov/--margin: rencana awareness tidak menghitung CPA/ROAS (memang bukan tolok ukurnya).")

    # ---- kanal & minggu
    jenis = a.jenis
    utama = tentukan_kanal_utama(a, jenis, kanal_diminta)
    if utama is not None and set(porsi) != {"awareness"}:
        if bobot[utama] == 0:
            catatan.append(f"{NAMA_KANAL[utama]} disebut sebagai sumber penjualan utama, tetapi tidak cocok untuk "
                           "tujuan ini (mis. leads); porsinya tidak dinaikkan.")
        else:
            lain = [bobot[k] for k in kanal_diminta if k != utama and bobot[k] > 0]
            if lain:
                bobot[utama] = max(bobot[utama], PENGALI_UTAMA * max(lain))
            catatan.append(f"Kanal penjualan utama: {NAMA_KANAL[utama]} -> porsinya dibuat {PENGALI_UTAMA}x kanal "
                           "pendukung terbesar (iklan di tempat pembeli bertransaksi dulu; kanal lain sebagai "
                           "pendukung). Ganti dengan --kanal-utama bila penjualan terbanyak datang dari kanal lain.")
    prioritas = PRIORITAS.get(jenis) or sorted(KANAL, key=lambda k: (-bobot[k], KANAL.index(k)))
    if utama is not None:
        prioritas = [utama] + [k for k in prioritas if k != utama]
    cadangan = kanal_diminta if (a.kanal or jenis == "marketplace") else [k for k in kanal_diminta if k not in MARKETPLACE]
    if utama is not None and utama not in cadangan:
        cadangan = cadangan + [utama]
    if campuran:
        catatan.append("Tujuan campuran: bobot kanal = rata-rata tertimbang bobot tiap tujuan menurut porsinya "
                       "(titik awal). Target CPA/ROAS berlaku untuk bagian penjualan/leads; bagian awareness "
                       "dinilai dari jangkauan, bukan CPA.")
    aktif, dikeluarkan, _ = pilih_kanal(anggaran, bobot, kanal_diminta, bobot_minggu, min_harian, prioritas, cadangan)
    hari_total = HARI_PER_MINGGU * minggu
    bobot_kanal = [bobot[k] for k in aktif]
    bag_kanal, sisa_kanal = bagi(anggaran, bobot_kanal)
    hasil_kanal = []
    sisa_minggu = {}
    for k, b in zip(aktif, bag_kanal):
        per_minggu, sm = bagi(b, bobot_minggu)
        if sm:
            sisa_minggu[k] = sm
        uji = bulat(Decimal(b) * PORSI_UJI)
        iklan_maks = min(p // (HARI_PER_MINGGU * min_harian[k]) for p in per_minggu)
        item = {"kanal": k, "nama": NAMA_KANAL[k], "bobot": (int(bobot[k]) if bobot[k] == int(bobot[k]) else float(bobot[k])), "anggaran": b,
                "persen": str((Decimal(b) * SERATUS / anggaran).quantize(Decimal("0.1"), rounding=ROUND_HALF_UP)),
                "aman": b - uji, "uji": uji, "per_minggu": per_minggu,
                "rata_per_hari": bulat(Decimal(b) / hari_total),
                "min_harian_per_iklan": min_harian[k], "iklan_aktif_maks": int(iklan_maks)}
        if iklan_maks < 1:
            item["hari_tayang_terbiayai"] = int(min(b // min_harian[k], hari_total))
        hasil_kanal.append(item)
    for x in hasil_kanal:
        if x["iklan_aktif_maks"] < 1:
            catatan.append(f"Anggaran DI BAWAH batas uji untuk {x['nama']} (minggu terkecil kurang dari 7 hari x "
                           f"{rp(x['min_harian_per_iklan'])}): iklan hanya bisa tayang sebagian hari atau dengan 1 iklan "
                           "berbudget kecil. Kumpulkan anggaran dulu atau andalkan konten organik. Sudah tidak ada "
                           "kanal lain yang lebih layak untuk anggaran ini.")
    if len(hasil_kanal) == 1 and len(kanal_diminta) > 1:
        catatan.append(f"Hanya {hasil_kanal[0]['nama']} yang dipertahankan karena anggaran terlalu tipis untuk dibagi "
                       f"(aturan: prioritas untuk {NAMA_JENIS[jenis]}; ubah dengan --jenis umum|marketplace|jasa-lokal).")
    total_minggu = [sum(x["per_minggu"][i] for x in hasil_kanal) for i in range(minggu)]
    assert sum(x["anggaran"] for x in hasil_kanal) == anggaran
    assert sum(total_minggu) == anggaran
    return {
        "anggaran": anggaran, "tujuan": tujuan, "porsi_tujuan": porsi, "jenis": jenis, "minggu": minggu, "hari_tayang": hari_total,
        "bobot_minggu": [int(b) for b in bobot_minggu], "target": target, "kanal": hasil_kanal,
        "total_per_minggu": total_minggu, "sisa_pembulatan_kanal": sisa_kanal,
        "sisa_pembulatan_minggu": sisa_minggu,
        "kanal_dikeluarkan": {NAMA_KANAL[k]: v for k, v in dikeluarkan.items()},
        "catatan": catatan,
    }


# --------------------------------------------------------------------------------------
# Momen belanja per bulan (SAMA dengan tabel references/momen-belanja.md; ubah keduanya bersamaan)
# --------------------------------------------------------------------------------------
# (bulan, tanggal, nama, puncak?) -- hanya momen bertanggal TETAP. Ramadan/Lebaran tidak ditebak.
MOMEN_TETAP = [
    (1, 1, "Tahun Baru", False),
    (8, 17, "17 Agustus", False),
    (9, 9, "Tanggal kembar 9.9 (kampanye marketplace)", True),
    (10, 10, "Tanggal kembar 10.10 (kampanye marketplace)", True),
    (11, 11, "Tanggal kembar 11.11 (kampanye marketplace; BUKAN Harbolnas)", True),
    (12, 12, "Harbolnas (Hari Belanja Online Nasional) & tanggal kembar 12.12", True),
    (12, 22, "Hari Ibu", True),
    (12, 25, "Natal", True),
]
MOMEN_SELALU = [
    "Gajian sekitar tanggal 25-1 (minggu 4 dan hari evaluasi); tanggal tua 15-24 (minggu 3-4) - pola bulanan",
    "Ramadan & Lebaran: tanggal berubah tiap tahun - TIDAK dihitung script; tanyakan/cek keputusan pemerintah",
    "Awal bulan/bonus/THR: bervariasi - tanyakan pola pembeli",
]
_RE_BULAN = re.compile(r"(\d{4})-(\d{1,2})")


def minggu_ke(tanggal, minggu=4):
    """Minggu script (1-7 = minggu 1, 8-14 = minggu 2, ...); None bila di luar hari tayang (hari evaluasi)."""
    m = (tanggal - 1) // HARI_PER_MINGGU + 1
    return m if m <= minggu else None


def momen_bulan(teks, minggu=4):
    """Daftar momen untuk bulan 'YYYY-MM' diambil dari tabel tetap di atas, dipetakan ke minggu script."""
    t = _RE_BULAN.fullmatch(str(teks).strip())
    if not t or not 1 <= int(t.group(2)) <= 12:
        raise Gagal(f"--momen '{teks}' harus berbentuk TAHUN-BULAN, mis. 2026-10.")
    tahun, bulan = int(t.group(1)), int(t.group(2))
    daftar, bobot = [], [1] * minggu
    for b, tgl, nama, puncak in MOMEN_TETAP:
        if b != bulan:
            continue
        mg = minggu_ke(tgl, minggu)
        daftar.append({"tanggal": f"{tgl}/{bulan}/{tahun}", "nama": nama, "minggu": mg, "puncak": puncak})
        if puncak and mg:
            bobot[mg - 1] = 2
    if bulan == 7:
        daftar.append({"tanggal": f"sekitar Juli {tahun}", "nama": "Tahun ajaran baru (seragam, alat tulis, tas, les)",
                       "minggu": None, "puncak": False})
    return {"bulan": f"{tahun}-{bulan:02d}", "momen": daftar, "pola_bulanan": MOMEN_SELALU,
            "saran_bobot_minggu": bobot}


def teks_momen(m):
    o = [f"## Kalender momen {m['bulan']} (dari tabel references/momen-belanja.md)"]
    if m["momen"]:
        o.append("| Tanggal | Momen | Minggu script |")
        o.append("|---|---|---|")
        for x in m["momen"]:
            mg = f"Minggu {x['minggu']}" if x["minggu"] else "di luar 28 hari tayang / cek sendiri"
            o.append(f"| {x['tanggal']} | {x['nama']} | {mg} |")
    else:
        o.append("Tidak ada momen bertanggal TETAP di tabel untuk bulan ini (tetap cek pola bulanan di bawah).")
    o.append("Pola bulanan & momen tidak tetap:")
    o.extend(f"- {x}" for x in m["pola_bulanan"])
    o.append("Saran --bobot-minggu (minggu momen puncak = 2): " + " ".join(map(str, m["saran_bobot_minggu"])))
    return "\n".join(o)


# --------------------------------------------------------------------------------------
# Format
# --------------------------------------------------------------------------------------
def rp(n):
    return ("-" if n < 0 else "") + "Rp" + f"{abs(int(n)):,}".replace(",", ".")


def koma(teks):
    return str(teks).replace(".", ",")


def teks_laporan(h):
    o = []
    o.append(f"# Rencana Alokasi Anggaran Iklan - {rp(h['anggaran'])} / bulan")
    o.append(f"Tujuan: **{h['tujuan']}** | {h['minggu']} minggu x 7 hari = {h['hari_tayang']} hari tayang "
             "(sisa hari bulan dipakai evaluasi tanpa menambah anggaran).\n")
    t = h["target"]
    if t:
        o.append("## Target dari margin (batas impas, bukan prediksi)")
        o.append(f"- Harga rata-rata per pesanan: {rp(t['aov'])}; margin kotor {koma(t['margin_persen'])}% "
                 f"-> laba kotor per pesanan {rp(t['laba_kotor_per_pesanan'])}")
        o.append(f"- **Titik impas ROAS = 1/margin = {koma(t['roas_impas'])}x** (di bawah ini iklan merugi); "
                 f"CPA impas {rp(t['cpa_impas'])}")
        o.append(f"- **Target aman** (sisakan 30% laba kotor): CPA maks {rp(t['cpa_target'])}, "
                 f"ROAS minimal {koma(t['roas_target'])}x")
        if "cpl_impas" in t:
            o.append(f"- Leads (closing {koma(t['closing_persen'])}%): biaya per lead impas {rp(t['cpl_impas'])}, "
                     f"target maks {rp(t['cpl_target'])}")
        o.append(f"- Agar anggaran bulan ini sekadar impas dibutuhkan minimal {t['pesanan_minimal_impas']} pesanan "
                 f"(= omzet {rp(t['pesanan_minimal_impas'] * t['aov'])}); ini syarat impas, BUKAN perkiraan hasil.\n")
    o.append("## Anggaran per kanal")
    o.append("| Kanal | Anggaran | % | Aman 70% | Uji 30% |")
    o.append("|---|---:|---:|---:|---:|")
    for x in h["kanal"]:
        o.append(f"| {x['nama']} | {rp(x['anggaran'])} | {koma(x['persen'])}% | {rp(x['aman'])} | {rp(x['uji'])} |")
    o.append(f"| **Total** | **{rp(h['anggaran'])}** | 100% | | |\n")
    o.append("## Rencana per minggu")
    o.append("| Kanal | " + " | ".join(f"Minggu {i+1}" for i in range(h["minggu"])) + " | Jumlah |")
    o.append("|---|" + "---:|" * (h["minggu"] + 1))
    for x in h["kanal"]:
        o.append(f"| {x['nama']} | " + " | ".join(rp(p) for p in x["per_minggu"]) + f" | {rp(x['anggaran'])} |")
    o.append("| **Total** | " + " | ".join(f"**{rp(p)}**" for p in h["total_per_minggu"]) + f" | **{rp(h['anggaran'])}** |\n")
    o.append("## Batas uji (aturan praktis Komunitech, bukan syarat platform; cek minimum di Ads Manager)")
    o.append("| Kanal | Rata-rata per hari | Min. per iklan/hari | Iklan aktif maks |")
    o.append("|---|---:|---:|---:|")
    for x in h["kanal"]:
        if x["iklan_aktif_maks"] >= 1:
            akhir = str(x["iklan_aktif_maks"])
        else:
            akhir = f"0 - DI BAWAH BATAS (cukup untuk {x['hari_tayang_terbiayai']} hari tayang 1 iklan)"
        o.append(f"| {x['nama']} | {rp(x['rata_per_hari'])} | {rp(x['min_harian_per_iklan'])} | {akhir} |")
    o.append("")
    if h["kanal_dikeluarkan"]:
        o.append("Kanal tidak dipakai: " + "; ".join(f"{k} ({v})" for k, v in h["kanal_dikeluarkan"].items())
                 + ". Anggarannya sudah dialihkan ke kanal yang dipakai (total tetap sama).")
    sk = h["sisa_pembulatan_kanal"]
    sm = h["sisa_pembulatan_minggu"]
    terbesar = max(h["kanal"], key=lambda x: x["bobot"])["nama"]
    bagian = [f"antar kanal {rp(sk)} (ditambahkan ke {terbesar})"] if sk else []
    bagian += [f"{NAMA_KANAL[k]} antar minggu {rp(v)}" for k, v in sm.items()]
    o.append("Sisa pembulatan: " + ("; ".join(bagian) if bagian else "Rp0") + ". Total tetap sama dengan anggaran.")
    if h["catatan"]:
        o.append("\n## Catatan")
        o.extend(f"- {c}" for c in h["catatan"])
    o.append("\nAngka pembagian ini titik awal yang bisa diubah, bukan janji hasil. Tidak ada jaminan penjualan.")
    return "\n".join(o)


def buat_parser():
    p = argparse.ArgumentParser(allow_abbrev=False, description="Alokasi anggaran iklan bulanan per kanal & minggu.")
    p.add_argument("--anggaran", help="anggaran sebulan, mis. 10jt, 1.500.000, 500rb (wajib kecuali hanya --momen)")
    p.add_argument("--momen", help="bulan rencana TAHUN-BULAN, mis. 2026-10: cetak momen belanja bulan itu dari tabel "
                                   "referensi + minggu script + saran --bobot-minggu. Boleh dipakai tanpa --anggaran")
    p.add_argument("--tujuan", default="penjualan",
                   help="penjualan | awareness | leads, atau campuran berporsi total 100, mis. awareness:30,penjualan:70")
    p.add_argument("--jenis", choices=JENIS, default="umum",
                   help="dipakai bila anggaran kecil memaksa memilih kanal: marketplace (Shopee/TikTok Shop dulu), "
                        "jasa-lokal (Google/Meta dulu), umum (menurut bobot tujuan)")
    p.add_argument("--aov", help="harga rata-rata per pesanan (atau nilai satu penjualan untuk leads)")
    p.add_argument("--margin", help="margin kotor setelah biaya admin marketplace & ongkir, mis. 40%%")
    p.add_argument("--closing", help="khusus leads: persen calon pembeli yang jadi membeli, mis. 20%%")
    p.add_argument("--kanal", help="pilihan: " + ",".join(KANAL) + " (default semua)")
    p.add_argument("--kanal-utama", help="kanal tempat penjualan terbanyak terjadi (mis. shopee); porsinya dibuat "
                                         "2x kanal pendukung terbesar. Default: Shopee/TikTok Shop bila --jenis marketplace")
    p.add_argument("--minggu", type=int, default=4, help="jumlah minggu (1-5, default 4)")
    p.add_argument("--bobot-minggu", nargs="+", help="bobot bulat per minggu, mis. 1 1 1 2 (momen belanja di minggu 4)")
    p.add_argument("--min-harian", help="ganti batas uji minimum per iklan per hari untuk semua kanal")
    p.add_argument("--kategori", default="umum", help="jenis produk; kesehatan/keuangan/kripto mendapat catatan aturan iklan")
    p.add_argument("--json", action="store_true", help="keluaran JSON")
    return p


def main(argv=None):
    try:
        argv = list(sys.argv[1:] if argv is None else argv)
        for i, t in enumerate(argv[:-1]):   # '--margin -10%' dibaca argparse sebagai opsi; gabungkan
            if t == "--margin" and argv[i + 1].startswith("-"):
                argv[i:i + 2] = ["--margin=" + argv[i + 1]]
                break
        a = buat_parser().parse_args(argv)
        m = momen_bulan(a.momen, a.minggu if 1 <= a.minggu <= 5 else 4) if a.momen else None
        if not a.anggaran:
            if not m:
                raise Gagal("--anggaran wajib diisi (atau pakai --momen TAHUN-BULAN untuk daftar momen saja).")
            print(json.dumps(m, ensure_ascii=False, indent=2) if a.json else teks_momen(m))
            return 0
        h = hitung(a)
        if m:
            h["momen"] = m
    except Gagal as e:
        print(f"GAGAL: {e}", file=sys.stderr)
        return 2
    if a.json:
        print(json.dumps(h, ensure_ascii=False, indent=2))
    else:
        print(teks_laporan(h) + ("\n\n" + teks_momen(h["momen"]) if "momen" in h else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
