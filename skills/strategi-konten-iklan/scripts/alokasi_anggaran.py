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
_RE_RUPIAH = re.compile(r"(?:rp\.?\s*)?(\d[\d.,]*)\s*([a-z]+)?", re.I)
_TITIK_RIBU = re.compile(r"[1-9]\d{0,2}(\.\d{3})+")


def parse_rupiah(teks, nama="nilai"):
    """'1.500.000', '1,5jt', '500rb', 'Rp2 juta' -> int rupiah. Ambigu/rusak -> Gagal."""
    s = str(teks).replace(" ", " ").strip().lower()
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
        raise Gagal(f"{nama} '{teks}' ambigu: 0,4 berarti 0,4% atau 40%? Tulis '40%' (atau '0,4%').")
    return p


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


def pilih_kanal(anggaran, tujuan, kanal_diminta, minggu, min_harian):
    """Tentukan kanal aktif. Kanal yang bagiannya di bawah batas uji dibuang satu per satu
    (bobot terkecil dulu; seri: yang paling belakang), lalu anggaran dibagi ulang."""
    bobot = BOBOT[tujuan]
    aktif = [k for k in kanal_diminta if bobot[k] > 0]
    dikeluarkan = {k: "kurang cocok untuk tujuan ini" for k in kanal_diminta if bobot[k] == 0}
    if not aktif:
        raise Gagal("Tidak ada kanal yang cocok untuk tujuan ini. Untuk 'leads' pakai meta/google/tiktok.")
    hari = HARI_PER_MINGGU * minggu
    while True:
        bag, _ = bagi(anggaran, [bobot[k] for k in aktif])
        lemah = [k for k, b in zip(aktif, bag) if b < hari * min_harian[k]]
        if not lemah or len(aktif) == 1:
            return aktif, dikeluarkan, bool(lemah)
        buang = sorted(lemah, key=lambda k: (bobot[k], -aktif.index(k)))[0]
        dikeluarkan[buang] = "bagian anggarannya di bawah batas uji"
        aktif.remove(buang)


def hitung(a):
    anggaran = parse_rupiah(a.anggaran, "--anggaran")
    if anggaran < 100000:
        raise Gagal("--anggaran di bawah Rp100.000 per bulan terlalu kecil untuk iklan berbayar. "
                    "Pakai konten organik dulu (lihat skill kalender-konten-30hari).")
    tujuan = a.tujuan
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

    kanal_diminta = KANAL[:]
    if a.kanal:
        kanal_diminta = []
        for t in re.split(r"[,\s;]+", a.kanal.strip().lower()):
            t = t.replace("-", "").replace("_", "").replace(" ", "")
            if not t:
                continue
            if t not in KANAL:
                raise Gagal(f"--kanal '{t}' tidak dikenal. Pilihan: {', '.join(KANAL)}.")
            if t not in kanal_diminta:
                kanal_diminta.append(t)
        if not kanal_diminta:
            raise Gagal("--kanal kosong.")

    catatan = []
    kategori = (a.kategori or "umum").strip().lower()
    for kata in DILARANG:
        if kata in kategori:
            raise Gagal(f"Kategori '{a.kategori}' dilarang/sangat dibatasi di platform iklan utama; "
                        "rencana anggaran tidak disusun.")
    for kunci, teks in CATATAN_KATEGORI.items():
        if kunci in kategori:
            catatan.append(teks)
    if a.kategori and kategori != "umum" and not any(k in kategori for k in CATATAN_KATEGORI):
        catatan.append(f"Kategori '{a.kategori}': cek dulu apakah termasuk kategori terbatas di kebijakan "
                       "iklan resmi tiap platform.")

    min_harian = dict(MIN_HARIAN)
    if a.min_harian:
        m = parse_rupiah(a.min_harian, "--min-harian")
        min_harian = {k: m for k in KANAL}

    # ---- target dari margin & AOV
    target = None
    aov = parse_rupiah(a.aov, "--aov") if a.aov else None
    margin = parse_persen(a.margin, "--margin") if a.margin else None
    closing = parse_persen(a.closing, "--closing") if a.closing else None
    if tujuan == "penjualan" and (aov is None or margin is None):
        raise Gagal("Untuk tujuan 'penjualan' wajib isi --aov (harga rata-rata per pesanan) dan --margin "
                    "(margin kotor, mis. 40%). Tanpa keduanya target CPA/ROAS tidak bisa dihitung.")
    if tujuan == "leads" and (aov is None or margin is None or closing is None):
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
    elif tujuan == "awareness":
        catatan.append("Tanpa --aov/--margin: rencana awareness tidak menghitung CPA/ROAS (memang bukan tolok ukurnya).")

    # ---- kanal & minggu
    aktif, dikeluarkan, di_bawah = pilih_kanal(anggaran, tujuan, kanal_diminta, minggu, min_harian)
    hari_total = HARI_PER_MINGGU * minggu
    bobot_kanal = [BOBOT[tujuan][k] for k in aktif]
    bag_kanal, sisa_kanal = bagi(anggaran, bobot_kanal)
    hasil_kanal = []
    sisa_minggu = {}
    for k, b in zip(aktif, bag_kanal):
        per_minggu, sm = bagi(b, bobot_minggu)
        if sm:
            sisa_minggu[k] = sm
        uji = bulat(Decimal(b) * PORSI_UJI)
        iklan_maks = min(p // (HARI_PER_MINGGU * min_harian[k]) for p in per_minggu)
        item = {"kanal": k, "nama": NAMA_KANAL[k], "bobot": BOBOT[tujuan][k], "anggaran": b,
                "persen": str((Decimal(b) * SERATUS / anggaran).quantize(Decimal("0.1"), rounding=ROUND_HALF_UP)),
                "aman": b - uji, "uji": uji, "per_minggu": per_minggu,
                "rata_per_hari": bulat(Decimal(b) / hari_total),
                "min_harian_per_iklan": min_harian[k], "iklan_aktif_maks": int(iklan_maks)}
        if iklan_maks < 1:
            item["hari_tayang_terbiayai"] = int(b // min_harian[k])
        hasil_kanal.append(item)
    if di_bawah:
        catatan.append("Anggaran DI BAWAH batas uji untuk kanal ini: iklan hanya bisa tayang sebagian hari "
                       "atau dengan 1 iklan berbudget kecil. Kumpulkan anggaran dulu atau andalkan konten organik.")
    total_minggu = [sum(x["per_minggu"][i] for x in hasil_kanal) for i in range(minggu)]
    assert sum(x["anggaran"] for x in hasil_kanal) == anggaran
    assert sum(total_minggu) == anggaran
    return {
        "anggaran": anggaran, "tujuan": tujuan, "minggu": minggu, "hari_tayang": hari_total,
        "bobot_minggu": [int(b) for b in bobot_minggu], "target": target, "kanal": hasil_kanal,
        "total_per_minggu": total_minggu, "sisa_pembulatan_kanal": sisa_kanal,
        "sisa_pembulatan_minggu": sisa_minggu,
        "kanal_dikeluarkan": {NAMA_KANAL[k]: v for k, v in dikeluarkan.items()},
        "catatan": catatan,
    }


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
        o.append("Kanal tidak dipakai: " + "; ".join(f"{k} ({v})" for k, v in h["kanal_dikeluarkan"].items()) + ".")
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
    p.add_argument("--anggaran", required=True, help="anggaran sebulan, mis. 10jt, 1.500.000, 500rb")
    p.add_argument("--tujuan", choices=sorted(BOBOT), default="penjualan")
    p.add_argument("--aov", help="harga rata-rata per pesanan (atau nilai satu penjualan untuk leads)")
    p.add_argument("--margin", help="margin kotor setelah biaya admin marketplace & ongkir, mis. 40%%")
    p.add_argument("--closing", help="khusus leads: persen calon pembeli yang jadi membeli, mis. 20%%")
    p.add_argument("--kanal", help="pilihan: " + ",".join(KANAL) + " (default semua)")
    p.add_argument("--minggu", type=int, default=4, help="jumlah minggu (1-5, default 4)")
    p.add_argument("--bobot-minggu", nargs="+", help="bobot bulat per minggu, mis. 1 1 1 2 (momen belanja di minggu 4)")
    p.add_argument("--min-harian", help="ganti batas uji minimum per iklan per hari untuk semua kanal")
    p.add_argument("--kategori", default="umum", help="jenis produk; kesehatan/keuangan/kripto mendapat catatan aturan iklan")
    p.add_argument("--json", action="store_true", help="keluaran JSON")
    return p


def main(argv=None):
    try:
        a = buat_parser().parse_args(argv)
        h = hitung(a)
    except Gagal as e:
        print(f"GAGAL: {e}", file=sys.stderr)
        return 2
    print(json.dumps(h, ensure_ascii=False, indent=2) if a.json else teks_laporan(h))
    return 0


if __name__ == "__main__":
    sys.exit(main())
