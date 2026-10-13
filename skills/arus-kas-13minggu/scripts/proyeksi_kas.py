#!/usr/bin/env python3
"""Proyeksi arus kas mingguan (default 13 minggu) untuk UMKM.

Membaca rencana penerimaan & pengeluaran dari CSV, menghitung saldo akhir per minggu,
menandai minggu kas negatif / di bawah batas aman, dan mensimulasikan beberapa opsi
tindakan (percepat tagihan piutang, mundurkan bayar supplier, tunda belanja non-kritis).

Hanya library standar Python 3.8+. Tidak ada akses jaringan. Versi 1.0.4 (2026-10-13).

Format CSV input (pemisah , ; tab atau | dideteksi otomatis; judul kolom boleh variasi):
    minggu;jenis;kategori;nominal;keterangan;kritis
    semua;masuk;Penjualan tunai;15.000.000;;
    3;masuk;Pelunasan piutang;Rp 8.500.000;Toko Maju;
    tgl:25;keluar;Gaji;Rp 12.000.000;4 karyawan;ya
    tgl:1;keluar;Sewa;5.000.000;;ya
    5;keluar;Renovasi etalase;7.500.000;;tidak

Kolom `minggu` menerima: 3 | 1-13 | 2,6,10 | semua | setiap 2 | setiap 2 mulai 3 |
tgl:25 (minggu yang memuat tanggal 25 tiap bulan; butuh --mulai).

Pembulatan: setiap nominal dibulatkan ke rupiah penuh terdekat (0,5 ke atas) sebelum dijumlah,
sehingga semua total adalah bilangan bulat rupiah dan penjumlahan di Excel akan sama persis.
"""
import argparse
import calendar
import csv
import io
import json
import re
import sys
from datetime import date, datetime, timedelta
from decimal import ROUND_HALF_UP, Decimal, InvalidOperation

# ---------------------------------------------------------------- util angka & format

def parse_angka(teks):
    """'Rp 15.000' / '15.000,50' / '15,000.50' / '1.250.000' / '15jt' / '2,5 juta' -> Decimal atau None."""
    if teks is None:
        return None
    s = str(teks).strip().lower()
    if not s:
        return None
    pengali = Decimal(1)
    m = re.search(r"(miliar|milyar|m\b|juta|jt|ribu|rb|k\b)\s*$", s)
    if m:
        kata = m.group(1)
        pengali = Decimal({"miliar": 10**9, "milyar": 10**9, "m": 10**9, "juta": 10**6, "jt": 10**6,
                           "ribu": 1000, "rb": 1000, "k": 1000}[kata])
        s = s[:m.start()].strip()
    negatif = s.startswith("-") or (s.startswith("(") and s.endswith(")"))
    s = re.sub(r"\b(rp|idr)\b\.?", "", s)
    s = re.sub(r"[,.]\s*-\s*$", "", s)
    s = re.sub(r"[^\d,.]", "", s).strip(".,")
    if not s:
        return None
    if "," in s and "." in s:
        if s.rfind(",") > s.rfind("."):
            s = s.replace(".", "").replace(",", ".")
        else:
            s = s.replace(",", "")
    elif "," in s:
        bagian = s.split(",")
        s = s.replace(",", ".") if (len(bagian) == 2 and len(bagian[1]) != 3) else s.replace(",", "")
    elif "." in s:
        bagian = s.split(".")
        if len(bagian) > 2 or len(bagian[1]) == 3:
            s = s.replace(".", "")
    try:
        nilai = Decimal(s) * pengali
    except InvalidOperation:
        return None
    return -nilai if negatif else nilai


def bulat(nilai):
    return int(Decimal(nilai).quantize(Decimal(1), rounding=ROUND_HALF_UP))


def rp(n):
    n = int(n)
    tanda = "-" if n < 0 else ""
    return f"{tanda}Rp {abs(n):,}".replace(",", ".")


def parse_tanggal(teks):
    teks = (teks or "").strip()
    for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%d-%m-%Y", "%d.%m.%Y"):
        try:
            return datetime.strptime(teks, fmt).date()
        except ValueError:
            pass
    return None


def fmt_tgl(d):
    bln = ["Jan", "Feb", "Mar", "Apr", "Mei", "Jun", "Jul", "Agu", "Sep", "Okt", "Nov", "Des"]
    return f"{d.day} {bln[d.month - 1]}"


def gagal(pesan, detail=None, kode=2):
    data = {"error": pesan}
    if detail:
        data["detail"] = detail
    print(json.dumps(data, ensure_ascii=False, indent=2), file=sys.stderr)
    sys.exit(kode)

# ---------------------------------------------------------------- baca input

ALIAS = {
    "minggu": ["minggu", "minggu ke", "minggu_ke", "week", "periode", "jadwal", "kapan"],
    "jenis": ["jenis", "tipe", "arah", "type", "masuk/keluar"],
    "kategori": ["kategori", "pos", "item", "uraian", "nama", "category", "akun"],
    "nominal": ["nominal", "jumlah", "nilai", "amount", "rp", "rupiah", "besar"],
    "keterangan": ["keterangan", "catatan", "ket", "note", "notes", "deskripsi"],
    "kritis": ["kritis", "wajib", "penting", "critical", "bisa ditunda"],
}
KATA_MASUK = ["penjualan", "jual", "omzet", "piutang", "pelunasan", "tagihan masuk", "dp ", "uang muka",
              "penerimaan", "pemasukan", "pinjaman masuk", "pencairan", "modal masuk", "setoran modal",
              "termin masuk", "pendapatan"]
KATA_PIUTANG = ["piutang", "pelunasan", "tagihan", "termin masuk", "invoice"]
KATA_SUPPLIER = ["bahan", "supplier", "pemasok", "stok", "belanja barang", "kulakan", "persediaan", "material"]
KATA_NONKRITIS = ["renovasi", "peralatan", "alat baru", "aset", "mesin", "iklan", "marketing", "promosi",
                  "prive", "perjalanan", "dekorasi", "investasi", "seragam", "event", "sponsor",
                  "ekspansi", "cabang baru", "kendaraan", "furnitur", "laptop", "hp baru"]
# Kewajiban yang SELALU kritis (tidak boleh ikut simulasi "tunda"), apa pun isi kolom `kritis`.
KATA_WAJIB = ["gaji", "upah", "cicilan", "angsuran", "leasing", "kredit", "pajak", "ppn", "pph", "thr",
              "bpjs", "bonus karyawan", "bunga"]
# Biasanya kritis (dicek sebelum daftar non-kritis), tetapi boleh diubah pengguna lewat kolom `kritis`.
KATA_KRITIS = ["sewa", "listrik", "air", "pdam", "internet", "bahan", "supplier", "bonus", "tagihan", "asuransi"]


def ada_kata(teks, daftar):
    """Cocokkan kata utuh di awal kata (mis. 'air' tidak cocok dengan 'kursi pairing')."""
    t = (teks or "").lower()
    return next((k for k in daftar if re.search(r"(?<![a-z])" + re.escape(k), t)), None)


def cari_kolom(header):
    peta = {}
    norm = [(h or "").strip().lower() for h in header]
    for kunci, alias in ALIAS.items():
        for i, h in enumerate(norm):
            if h in alias:
                peta[kunci] = header[i]
                break
        if kunci not in peta:
            for i, h in enumerate(norm):
                if any(a in h for a in alias if len(a) > 3):
                    if header[i] not in peta.values():
                        peta[kunci] = header[i]
                        break
    return peta


def baca_csv(path):
    try:
        mentah = open(path, "rb").read()
    except OSError as e:
        gagal(f"File tidak bisa dibuka: {path}", str(e))
    for enc in ("utf-8-sig", "cp1252", "latin-1"):
        try:
            teks = mentah.decode(enc)
            break
        except UnicodeDecodeError:
            continue
    if not teks.strip():
        gagal("File input kosong.")
    try:
        dialek = csv.Sniffer().sniff(teks[:4096], delimiters=",;\t|")
    except csv.Error:
        dialek = csv.excel
    return list(csv.DictReader(io.StringIO(teks), dialect=dialek))


def minggu_dari_tanggal(hari, mulai, n):
    """Minggu (1..n) yang memuat tanggal `hari` tiap bulan."""
    hasil = []
    for w in range(1, n + 1):
        awal = mulai + timedelta(days=7 * (w - 1))
        for k in range(7):
            d = awal + timedelta(days=k)
            akhir_bln = calendar.monthrange(d.year, d.month)[1]
            if d.day == min(hari, akhir_bln):
                hasil.append(w)
                break
    return hasil


def parse_minggu(teks, n, mulai):
    s = (teks or "").strip().lower()
    if not s:
        raise ValueError("kolom minggu kosong")
    # bentuk awam: "minggu 6", "minggu ke-6", "mg 3-5", "setiap 2 minggu mulai minggu 3"
    s = re.sub(r"\b(?:minggu|mg|pekan)\s*(?:ke\s*-?\s*)?(?=\d)", "", s)
    s = re.sub(r"\bke\s*-\s*(?=\d)", "", s).strip()
    if s in ("semua", "tiap minggu", "setiap minggu", "rutin", "mingguan", "all", "*"):
        return list(range(1, n + 1))
    m = re.fullmatch(r"(?:tgl|tanggal|bulanan)\s*[:=]?\s*(\d{1,2})", s)
    if m:
        if mulai is None:
            raise ValueError("format tgl:N butuh tanggal mulai (--mulai YYYY-MM-DD)")
        hari = int(m.group(1))
        if not 1 <= hari <= 31:
            raise ValueError("tanggal harus 1–31")
        return minggu_dari_tanggal(hari, mulai, n)
    m = re.fullmatch(r"(?:setiap|tiap)\s*(\d+)(?:\s*minggu)?(?:\s*mulai\s*(\d+))?", s)
    if m:
        lang, awal = int(m.group(1)), int(m.group(2) or 1)
        if lang < 1:
            raise ValueError("interval minimal 1")
        return list(range(awal, n + 1, lang))
    hasil = set()
    for bag in re.split(r"[,&/ ]+|\bdan\b", s):
        bag = bag.strip()
        if not bag:
            continue
        r = re.fullmatch(r"(\d+)\s*[-–]\s*(\d+)", bag)
        if r:
            a, b = int(r.group(1)), int(r.group(2))
            if a > b:
                a, b = b, a
            hasil.update(range(a, b + 1))
        elif bag.isdigit():
            hasil.add(int(bag))
        else:
            raise ValueError(f"format minggu tidak dikenal: '{teks}'")
    return sorted(hasil)


def tebak_jenis(jenis, kategori):
    j = (jenis or "").strip().lower()
    if j in ("masuk", "in", "penerimaan", "pemasukan", "+", "kredit", "debit masuk", "m"):
        return "masuk"
    if j in ("keluar", "out", "pengeluaran", "biaya", "-", "k", "beban"):
        return "keluar"
    if j:
        return None
    return "masuk" if ada_kata(kategori, KATA_MASUK) else "keluar"


def tebak_kritis(nilai, kategori, jenis):
    """Kembalikan (kritis: True/False/None, sumber) dengan sumber 'wajib' | 'pengguna' | 'tebakan' | None."""
    if jenis == "masuk":
        return None, None
    if ada_kata(kategori, KATA_WAJIB):
        return True, "wajib"
    v = (nilai or "").strip().lower()
    if v in ("ya", "y", "yes", "wajib", "kritis", "1", "true"):
        return True, "pengguna"
    if v in ("tidak", "t", "no", "n", "bisa ditunda", "0", "false", "opsional"):
        return False, "pengguna"
    if ada_kata(kategori, KATA_KRITIS):
        return True, "tebakan"
    if ada_kata(kategori, KATA_NONKRITIS):
        return False, "tebakan"
    return None, None  # tidak diketahui

# ---------------------------------------------------------------- hitung

def proyeksi(item, n, saldo_awal):
    masuk = [0] * (n + 1)
    keluar = [0] * (n + 1)
    for it in item:
        w = it["minggu"]
        if 1 <= w <= n:
            if it["jenis"] == "masuk":
                masuk[w] += it["nominal"]
            else:
                keluar[w] += it["nominal"]
    saldo = []
    s = saldo_awal
    for w in range(1, n + 1):
        s = s + masuk[w] - keluar[w]
        saldo.append(s)
    return masuk[1:], keluar[1:], saldo


def ringkas_saldo(saldo, batas):
    neg = [i + 1 for i, s in enumerate(saldo) if s < 0]
    bawah = [i + 1 for i, s in enumerate(saldo) if 0 <= s < batas]
    terendah = min(range(len(saldo)), key=lambda i: saldo[i])
    return neg, bawah, terendah + 1, saldo[terendah]


def geser(item, syarat, delta, n, batas_minggu=None):
    """Salin item; item yang memenuhi syarat digeser `delta` minggu (dibatasi 1..n+?)."""
    baru, tergeser, keluar_horizon, rincian = [], 0, 0, []
    for it in item:
        it2 = dict(it)
        if syarat(it) and (batas_minggu is None or it["minggu"] <= batas_minggu):
            w = max(1, it["minggu"] + delta)
            if w != it["minggu"]:
                tergeser += it["nominal"]
                if w > n:
                    keluar_horizon += it["nominal"]
                rincian.append({"kategori": it["kategori"], "keterangan": it["keterangan"],
                                "nominal": it["nominal"], "dari_minggu": it["minggu"],
                                "ke_minggu": w if w <= n else f"setelah minggu {n}"})
            it2["minggu"] = w
        baru.append(it2)
    return baru, tergeser, keluar_horizon, rincian


def main():
    p = argparse.ArgumentParser(description="Proyeksi arus kas mingguan (13 minggu) untuk UMKM")
    p.add_argument("file", help="CSV rencana penerimaan & pengeluaran")
    p.add_argument("--saldo-awal", required=True, help="Saldo kas+bank di awal minggu 1, mis. 'Rp 25.000.000'")
    p.add_argument("--batas-aman", help="Saldo minimum yang dianggap aman. Default: rata-rata pengeluaran 1 minggu")
    p.add_argument("--mulai", help="Tanggal awal minggu 1 (YYYY-MM-DD atau DD/MM/YYYY)")
    p.add_argument("--jumlah-minggu", type=int, default=13, help="Default 13 (boleh 4–26)")
    p.add_argument("--geser-piutang", type=int, default=2, help="Simulasi: piutang ditagih N minggu lebih cepat (default 2)")
    p.add_argument("--geser-supplier", type=int, default=2, help="Simulasi: bayar supplier mundur N minggu (default 2)")
    p.add_argument("--geser-nonkritis", type=int, default=4, help="Simulasi: belanja non-kritis ditunda N minggu (default 4)")
    p.add_argument("--output-csv", help="Tulis tabel proyeksi untuk Excel ke file ini")
    p.add_argument("--pemisah", choices=[";", ","], default=";", help="Pemisah kolom CSV output (default ; untuk Excel Indonesia)")
    p.add_argument("--format", choices=["json", "teks"], default="json")
    a = p.parse_args()

    n = a.jumlah_minggu
    if not 4 <= n <= 26:
        gagal("Jumlah minggu harus antara 4 dan 26.")
    sa = parse_angka(a.saldo_awal)
    if sa is None:
        gagal(f"Saldo awal tidak terbaca: '{a.saldo_awal}'. Contoh yang benar: 'Rp 25.000.000'.")
    saldo_awal = bulat(sa)
    mulai = None
    if a.mulai:
        mulai = parse_tanggal(a.mulai)
        if mulai is None:
            gagal(f"Tanggal mulai tidak terbaca: '{a.mulai}'. Pakai format 2026-10-05 atau 05/10/2026.")

    baris = baca_csv(a.file)
    if not baris:
        gagal("File hanya berisi judul kolom, belum ada data.")
    kolom = cari_kolom(list(baris[0].keys()))
    hilang = [k for k in ("minggu", "kategori", "nominal") if k not in kolom]
    if hilang:
        gagal("Kolom wajib tidak ditemukan: " + ", ".join(hilang),
              {"kolom_tersedia": list(baris[0].keys()),
               "yang_dibutuhkan": "minggu, kategori, nominal (opsional: jenis, keterangan, kritis)"})

    item, dilewati, peringatan = [], [], []
    ditebak_nonkritis, setelah_horizon = set(), []
    for no, r in enumerate(baris, start=2):
        kat = (r.get(kolom["kategori"]) or "").strip()
        if not kat and not (r.get(kolom["nominal"]) or "").strip():
            continue  # baris kosong
        nom = parse_angka(r.get(kolom["nominal"]))
        if nom is None:
            dilewati.append({"baris": no, "alasan": f"nominal tidak terbaca: '{r.get(kolom['nominal'])}'"})
            continue
        if nom < 0:
            dilewati.append({"baris": no, "alasan": "nominal negatif; tulis angka positif dan isi kolom jenis (masuk/keluar)"})
            continue
        jenis = tebak_jenis(r.get(kolom.get("jenis", ""), "") if "jenis" in kolom else "", kat)
        if jenis is None:
            dilewati.append({"baris": no, "alasan": f"jenis tidak dikenal: '{r.get(kolom['jenis'])}' (pakai masuk/keluar)"})
            continue
        try:
            mg = parse_minggu(r.get(kolom["minggu"]), n, mulai)
        except ValueError as e:
            dilewati.append({"baris": no, "alasan": str(e)})
            continue
        luar = [w for w in mg if not 1 <= w <= n]
        if luar:
            peringatan.append(f"Baris {no} ({kat}): minggu {luar} di luar 1–{n}, diabaikan.")
        mg = [w for w in mg if 1 <= w <= n]
        if not mg:
            dilewati.append({"baris": no, "alasan": "tidak ada minggu yang valid"})
            continue
        ket = (r.get(kolom["keterangan"]) or "").strip() if "keterangan" in kolom else ""
        isian_kritis = r.get(kolom["kritis"]) if "kritis" in kolom else ""
        kritis, sumber_kritis = tebak_kritis(isian_kritis, kat, jenis)
        if sumber_kritis == "wajib" and (isian_kritis or "").strip().lower() in (
                "tidak", "t", "no", "n", "bisa ditunda", "0", "false", "opsional"):
            peringatan.append(f"Baris {no} ({kat}): ditandai 'tidak kritis', tetapi gaji/cicilan/angsuran/leasing/"
                              "pajak/THR/BPJS selalu diperlakukan KRITIS dan tidak ikut simulasi 'tunda'.")
        if jenis == "keluar" and kritis is False and sumber_kritis == "tebakan":
            ditebak_nonkritis.add(kat)
        low = kat.lower() + " " + ket.lower()
        spek = (r.get(kolom["minggu"]) or "").strip().lower()
        mt = re.fullmatch(r"(?:tgl|tanggal|bulanan)\s*[:=]?\s*(\d{1,2})", spek)
        if mt and mulai is not None:
            hari = int(mt.group(1))
            akhir_h = mulai + timedelta(days=7 * n - 1)
            for k in range(1, 8):
                d = akhir_h + timedelta(days=k)
                if d.day == min(hari, calendar.monthrange(d.year, d.month)[1]):
                    setelah_horizon.append(f"{kat} ({rp(bulat(nom))}) jatuh {fmt_tgl(d)} {d.year}, "
                                           f"{k} hari setelah minggu {n}")
                    break
        for w in mg:
            item.append({"minggu": w, "jenis": jenis, "kategori": kat or "(tanpa nama)",
                         "nominal": bulat(nom), "keterangan": ket, "kritis": kritis,
                         "piutang": jenis == "masuk" and bool(ada_kata(low, KATA_PIUTANG)),
                         "supplier": (jenis == "keluar" and sumber_kritis != "wajib"
                                      and bool(ada_kata(low, KATA_SUPPLIER)))})

    if not item:
        gagal("Tidak ada baris valid yang bisa dihitung.", {"baris_dilewati": dilewati})

    masuk, keluar, saldo = proyeksi(item, n, saldo_awal)
    total_keluar = sum(keluar)
    if a.batas_aman:
        b = parse_angka(a.batas_aman)
        if b is None or b < 0:
            gagal(f"Batas aman tidak terbaca: '{a.batas_aman}'.")
        batas, sumber_batas = bulat(b), "diisi pengguna"
    else:
        batas = bulat(Decimal(total_keluar) / n)
        sumber_batas = "ASUMSI: rata-rata pengeluaran 1 minggu (belum dikonfirmasi pengguna)"

    neg, bawah, w_rendah, s_rendah = ringkas_saldo(saldo, batas)

    # rincian per kategori per minggu
    urutan_kat = {"masuk": [], "keluar": []}
    per_kat = {}
    for it in item:
        key = (it["jenis"], it["kategori"])
        if it["kategori"] not in urutan_kat[it["jenis"]]:
            urutan_kat[it["jenis"]].append(it["kategori"])
        per_kat.setdefault(key, [0] * n)[it["minggu"] - 1] += it["nominal"]

    # kejadian per minggu: pos apa saja yang jatuh di minggu itu (untuk dikutip apa adanya di narasi)
    kejadian = {w: {"masuk": [], "keluar": []} for w in range(1, n + 1)}
    for it in item:
        if 1 <= it["minggu"] <= n:
            kejadian[it["minggu"]][it["jenis"]].append(
                {"kategori": it["kategori"], "nominal": it["nominal"], "keterangan": it["keterangan"]})
    for w in kejadian:
        for j in ("masuk", "keluar"):
            kejadian[w][j].sort(key=lambda x: -x["nominal"])

    def kalimat_kejadian(w):
        bag = []
        for j, label in (("keluar", "keluar"), ("masuk", "masuk")):
            isi = "; ".join(f"{x['kategori']}{' (' + x['keterangan'] + ')' if x['keterangan'] else ''} "
                            f"{rp(x['nominal'])}" for x in kejadian[w][j])
            bag.append(f"{label}: {isi or '-'}")
        return f"Minggu {w}: " + " | ".join(bag)

    minggu_data = []
    s_awal = saldo_awal
    for w in range(1, n + 1):
        d = {"minggu": w, "saldo_awal": s_awal, "masuk": masuk[w - 1], "keluar": keluar[w - 1],
             "bersih": masuk[w - 1] - keluar[w - 1], "saldo_akhir": saldo[w - 1],
             "status": "NEGATIF" if saldo[w - 1] < 0 else ("DI BAWAH BATAS AMAN" if saldo[w - 1] < batas else "AMAN")}
        if mulai:
            aw = mulai + timedelta(days=7 * (w - 1))
            d["periode"] = f"{fmt_tgl(aw)} – {fmt_tgl(aw + timedelta(days=6))}"
            d["tanggal_awal"] = aw.isoformat()
        d["kejadian"] = kejadian[w]
        d["kejadian_teks"] = kalimat_kejadian(w) + (f" ({d['periode']})" if mulai else "")
        minggu_data.append(d)
        s_awal = saldo[w - 1]

    # ------------------------------------------------ simulasi opsi tindakan
    bermasalah = sorted(set(neg + bawah))
    opsi = []
    if bermasalah:
        w1 = bermasalah[0]
        wz = bermasalah[-1]

        def evaluasi(nama, item2, digeser, lewat, rincian, catatan):
            _, _, sal2 = proyeksi(item2, n, saldo_awal)
            ng, bw, wr, sr = ringkas_saldo(sal2, batas)
            return {"opsi": nama, "nominal_digeser": digeser, "jatuh_setelah_horizon": lewat,
                    "saldo_terendah_baru": sr, "minggu_terendah_baru": wr,
                    "perbaikan_saldo_terendah": sr - s_rendah,
                    "minggu_negatif_baru": ng, "minggu_di_bawah_batas_baru": bw,
                    "saldo_akhir_per_minggu_baru": sal2,
                    "rincian_digeser": rincian[:30], "catatan": catatan}

        gp, gs, gn = a.geser_piutang, a.geser_supplier, a.geser_nonkritis
        it_p, d_p, _, r_p = geser(item, lambda x: x["piutang"] and x["minggu"] > w1 - 1, -gp, n)
        if d_p:
            opsi.append(evaluasi(f"Percepat tagihan piutang {gp} minggu", it_p, d_p, 0, r_p,
                                 "Asumsi pelanggan mau bayar lebih cepat (mis. diberi potongan kecil untuk bayar cepat)."))
        it_s, d_s, l_s, r_s = geser(item, lambda x: x["supplier"], gs, n, batas_minggu=wz)
        if d_s:
            opsi.append(evaluasi(f"Negosiasi termin supplier mundur {gs} minggu", it_s, d_s, l_s, r_s,
                                 "Hanya pembayaran bahan/supplier sampai minggu bermasalah terakhir yang digeser."))
        it_n, d_n, l_n, r_n = geser(item, lambda x: x["jenis"] == "keluar" and x["kritis"] is False, gn, n, batas_minggu=wz)
        if d_n:
            opsi.append(evaluasi(f"Tunda belanja non-kritis {gn} minggu", it_n, d_n, l_n, r_n,
                                 "Hanya pos yang ditandai/terdeteksi tidak kritis (renovasi, alat baru, iklan, prive, dll.)."))
        if len(opsi) >= 2:
            gab = item
            dg = lw = 0
            rg = []
            for syarat, delta, bm in ((lambda x: x["piutang"] and x["minggu"] > w1 - 1, -gp, None),
                                      (lambda x: x["supplier"], gs, wz),
                                      (lambda x: x["jenis"] == "keluar" and x["kritis"] is False, gn, wz)):
                gab, d, l, r = geser(gab, syarat, delta, n, batas_minggu=bm)
                dg += d
                lw += l
                rg += r
            opsi.append(evaluasi("Gabungan semua opsi di atas", gab, dg, lw, rg, "Kombinasi opsi yang tersedia."))
        for o in opsi:
            lewat = o["jatuh_setelah_horizon"]
            setelah = o["saldo_akhir_per_minggu_baru"][-1] - lewat
            o["saldo_setelah_kewajiban_tertunda"] = setelah
            o["hanya_menunda"] = bool(lewat) and setelah < 0
            o["di_bawah_batas_setelah_kewajiban_tertunda"] = bool(lewat) and setelah < batas
            if lewat:
                o["catatan"] += (f" PERHATIAN: {rp(lewat)} jatuh setelah minggu {n} — kewajiban tetap ada, hanya pindah "
                                 f"waktu. Setelah dibayar, saldo menjadi {rp(setelah)}.")
            if o["hanya_menunda"]:
                o["catatan"] += (" HANYA MENUNDA: opsi ini tidak menyelesaikan masalah, hanya memindahkan kekurangan "
                                 "ke setelah periode proyeksi. Jangan ditulis sebagai solusi.")

    kebutuhan_negatif = max(0, -s_rendah)
    kebutuhan_batas = max(0, batas - s_rendah)
    tidak_diketahui = sorted({it["kategori"] for it in item if it["jenis"] == "keluar" and it["kritis"] is None})
    if tidak_diketahui:
        peringatan.append("Pos pengeluaran berikut belum jelas kritis/tidak (tidak ikut simulasi 'tunda'): "
                          + ", ".join(tidak_diketahui) + ". Isi kolom 'kritis' (ya/tidak) bila perlu.")
    if ditebak_nonkritis:
        peringatan.append("Pos berikut DITEBAK tidak kritis dan ikut simulasi 'tunda belanja non-kritis': "
                          + ", ".join(sorted(ditebak_nonkritis)) + ". Konfirmasi ke pengguna bahwa pos ini memang bisa ditunda.")
    if setelah_horizon:
        peringatan.append("Pos bulanan berikutnya jatuh tak lama setelah periode proyeksi (belum masuk tabel): "
                          + "; ".join(setelah_horizon) + ". Pastikan saldo akhir cukup untuk itu.")
    bersih = sum(masuk) - total_keluar
    if bersih < 0:
        peringatan.append(f"DEFISIT STRUKTURAL: selama {n} minggu uang keluar lebih besar {rp(-bersih)} daripada uang masuk "
                          f"(rata-rata {rp(bulat(Decimal(-bersih) / n))}/minggu). Menggeser jadwal tidak cukup; perlu menaikkan "
                          "pemasukan atau memangkas biaya rutin.")
    if not any(it["piutang"] for it in item):
        peringatan.append("Tidak ada pos pelunasan piutang terdeteksi (kategori mengandung 'piutang'/'pelunasan'/'tagihan').")

    hasil = {
        "asumsi_dan_sumber": {
            "saldo_awal": saldo_awal, "batas_aman": batas, "batas_aman_sumber": sumber_batas,
            "jumlah_minggu": n, "tanggal_mulai": mulai.isoformat() if mulai else None,
            "pembulatan": "Setiap nominal dibulatkan ke rupiah penuh terdekat (0,5 ke atas) sebelum dijumlah.",
        },
        "ringkasan": {
            "total_masuk": sum(masuk), "total_keluar": total_keluar,
            "arus_kas_bersih": bersih,
            "defisit_struktural": bersih < 0,
            "rata_rata_arus_kas_bersih_per_minggu": bulat(Decimal(bersih) / n),
            "saldo_akhir_minggu_terakhir": saldo[-1],
            "saldo_terendah": s_rendah, "minggu_saldo_terendah": w_rendah,
            "minggu_negatif": neg, "minggu_di_bawah_batas_aman": bawah,
            "minggu_bermasalah_pertama": bermasalah[0] if bermasalah else None,
            "tambahan_dana_agar_tidak_negatif": kebutuhan_negatif,
            "tambahan_dana_agar_di_atas_batas_aman": kebutuhan_batas,
            "kejadian_minggu_kritis": [minggu_data[w - 1]["kejadian_teks"]
                                       for w in sorted(set(neg + bawah + [w_rendah]))],
        },
        "per_minggu": minggu_data,
        "per_kategori": {j: {k: per_kat[(j, k)] for k in urutan_kat[j]} for j in ("masuk", "keluar")},
        "simulasi_opsi": opsi,
        "baris_dilewati": dilewati,
        "peringatan": peringatan,
    }

    if a.output_csv:
        tulis_csv(a.output_csv, a.pemisah, hasil, n, mulai)
        hasil["file_csv"] = a.output_csv

    if a.format == "json":
        print(json.dumps(hasil, ensure_ascii=False, indent=2))
    else:
        cetak_teks(hasil)


def tulis_csv(path, sep, h, n, mulai):
    judul = ["Keterangan"] + [f"Minggu {w}" for w in range(1, n + 1)] + ["Total"]
    rows = [judul]
    if mulai:
        rows.append(["Periode"] + [m.get("periode", "") for m in h["per_minggu"]] + [""])
    pm = h["per_minggu"]
    rows.append(["Saldo awal"] + [m["saldo_awal"] for m in pm] + [""])
    rows.append(["PENERIMAAN"] + [""] * (n + 1))
    for k, v in h["per_kategori"]["masuk"].items():
        rows.append(["  " + k] + v + [sum(v)])
    rows.append(["Total penerimaan"] + [m["masuk"] for m in pm] + [h["ringkasan"]["total_masuk"]])
    rows.append(["PENGELUARAN"] + [""] * (n + 1))
    for k, v in h["per_kategori"]["keluar"].items():
        rows.append(["  " + k] + v + [sum(v)])
    rows.append(["Total pengeluaran"] + [m["keluar"] for m in pm] + [h["ringkasan"]["total_keluar"]])
    rows.append(["Arus kas bersih"] + [m["bersih"] for m in pm] + [h["ringkasan"]["arus_kas_bersih"]])
    rows.append(["Saldo akhir"] + [m["saldo_akhir"] for m in pm] + [""])
    rows.append(["Batas aman"] + [h["asumsi_dan_sumber"]["batas_aman"]] * n + [""])
    rows.append(["Status"] + [m["status"] for m in pm] + [""])
    try:
        with open(path, "w", encoding="utf-8-sig", newline="") as f:
            csv.writer(f, delimiter=sep).writerows(rows)
    except OSError as e:
        gagal(f"Gagal menulis file CSV: {path}", str(e))


def cetak_teks(h):
    r, a = h["ringkasan"], h["asumsi_dan_sumber"]
    print(f"Saldo awal: {rp(a['saldo_awal'])} | Batas aman: {rp(a['batas_aman'])} ({a['batas_aman_sumber']})")
    print()
    print("| Mg | Periode | Masuk | Keluar | Bersih | Saldo akhir | Status |")
    print("|---|---|---:|---:|---:|---:|---|")
    for m in h["per_minggu"]:
        tanda = {"NEGATIF": "🔴 NEGATIF", "DI BAWAH BATAS AMAN": "🟡 Di bawah batas", "AMAN": "🟢 Aman"}[m["status"]]
        print(f"| {m['minggu']} | {m.get('periode', '-')} | {rp(m['masuk'])} | {rp(m['keluar'])} | "
              f"{rp(m['bersih'])} | {rp(m['saldo_akhir'])} | {tanda} |")
    print()
    print(f"Total masuk {rp(r['total_masuk'])}, total keluar {rp(r['total_keluar'])}, "
          f"saldo akhir {rp(r['saldo_akhir_minggu_terakhir'])}.")
    print(f"Saldo terendah {rp(r['saldo_terendah'])} di minggu {r['minggu_saldo_terendah']}.")
    if r["defisit_struktural"]:
        print(f"DEFISIT STRUKTURAL: arus kas bersih {rp(r['arus_kas_bersih'])} "
              f"({rp(r['rata_rata_arus_kas_bersih_per_minggu'])}/minggu).")
    if r["minggu_negatif"]:
        print(f"Minggu NEGATIF: {r['minggu_negatif']} → butuh tambahan {rp(r['tambahan_dana_agar_tidak_negatif'])} agar tidak minus.")
    if r["minggu_di_bawah_batas_aman"]:
        print(f"Minggu di bawah batas aman: {r['minggu_di_bawah_batas_aman']}.")
    if r["tambahan_dana_agar_di_atas_batas_aman"]:
        print(f"Agar selalu di atas batas aman butuh tambahan {rp(r['tambahan_dana_agar_di_atas_batas_aman'])}.")
    print()
    print("Kejadian per minggu (kutip nomor minggu & pos dari sini, jangan menyimpulkan sendiri):")
    for m in h["per_minggu"]:
        print(f"- {m['kejadian_teks']}")
    print()
    for o in h["simulasi_opsi"]:
        print(f"- Simulasi '{o['opsi']}' (menggeser {rp(o['nominal_digeser'])}): saldo terendah jadi "
              f"{rp(o['saldo_terendah_baru'])} (minggu {o['minggu_terendah_baru']}), minggu negatif "
              f"{o['minggu_negatif_baru'] or 'tidak ada'}, minggu di bawah batas {o['minggu_di_bawah_batas_baru'] or 'tidak ada'}. "
              f"{o['catatan']}")
    for d in h["baris_dilewati"]:
        print(f"! Baris {d['baris']} dilewati: {d['alasan']}")
    for p in h["peringatan"]:
        print(f"! {p}")
    if h.get("file_csv"):
        print(f"File Excel/CSV: {h['file_csv']}")


if __name__ == "__main__":
    main()
