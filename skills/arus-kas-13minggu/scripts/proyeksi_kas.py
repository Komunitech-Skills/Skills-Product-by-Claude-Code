#!/usr/bin/env python3
"""Proyeksi arus kas mingguan (default 13 minggu) untuk UMKM.

Membaca rencana penerimaan & pengeluaran dari CSV, menghitung saldo akhir per minggu,
menandai minggu kas negatif / di bawah batas aman, mensimulasikan opsi bawaan (percepat
tagihan piutang, mundurkan bayar supplier, tunda belanja non-kritis), dan menghitung
sampai 4 opsi buatan sendiri dalam SATU panggilan (`--opsi`, boleh diulang).

Hanya library standar Python 3.8+. Tidak ada akses jaringan. Versi 1.0.5 (2026-10-14).

Format CSV input (pemisah ; , tab atau | dideteksi dari baris judul; judul kolom boleh variasi):
    minggu;jenis;kategori;nominal;keterangan;kritis
    semua;masuk;Penjualan tunai;15.000.000;;
    3;masuk;Pelunasan piutang;Rp 8.500.000;Toko Maju;
    tgl:25;keluar;Gaji;Rp 12.000.000;4 karyawan;ya
    tgl:1;keluar;Sewa;5.000.000;;ya
    5;keluar;Renovasi etalase;7.500.000;;tidak
Pemisah berlebih / sel kosong di akhir baris diabaikan. Baris yang isiannya lebih banyak
dari judul kolom dilewati dan dilaporkan (nomor baris + isinya).

Kolom `minggu` menerima: 3 | 1-13 | 2,6,10 | semua | setiap 2 | setiap 2 mulai 3 |
tgl:25 (minggu yang memuat tanggal 25 tiap bulan; butuh --mulai).

Opsi buatan sendiri (`--opsi "Nama opsi | aksi; aksi"`, maks. 4 per panggilan):
    geser <pos> ke minggu N            geser <pos> dari minggu A ke minggu N
    tunda|mundurkan <pos> K minggu     percepat|majukan <pos> K minggu
    ubah <pos> jadi <nominal>          kurangi|naikkan <pos> <persen>% | <nominal>
    hapus <pos>                        cicil <pos> K kali mulai minggu N [setiap S minggu]
    tambah masuk|keluar <nama> <nominal> minggu <N | 1-13 | semua> | tgl:<T>
<pos> = nama kategori (atau sebagian), boleh dibatasi `dari minggu A`.
Gaji/upah/THR/cicilan/pajak/BPJS tidak pernah digeser, dikurangi, dicicil, atau dihapus.

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
from datetime import datetime, timedelta
from decimal import ROUND_HALF_UP, Decimal, InvalidOperation

VERSI = "1.0.5"
MAKS_OPSI = 4

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


def periode_minggu(w, mulai):
    if not mulai:
        return None
    aw = mulai + timedelta(days=7 * (w - 1))
    return f"{fmt_tgl(aw)} – {fmt_tgl(aw + timedelta(days=6))}"


def rentang(ws):
    """[1,2,3,5,9,10] -> '1–3, 5, 9, 10'."""
    ws = sorted(set(ws))
    bag, i = [], 0
    while i < len(ws):
        j = i
        while j + 1 < len(ws) and ws[j + 1] == ws[j] + 1:
            j += 1
        if j >= i + 2:
            bag.append(f"{ws[i]}–{ws[j]}")
        else:
            bag.extend(str(x) for x in ws[i:j + 1])
        i = j + 1
    return ", ".join(bag) or "-"


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
KOLOM_WAJIB = ("minggu", "kategori", "nominal")
PEMISAH_KANDIDAT = [(";", "titik koma"), (",", "koma"), ("\t", "tab"), ("|", "garis tegak")]
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
ISIAN_TIDAK = ("tidak", "t", "no", "n", "bisa ditunda", "0", "false", "opsional")


def ada_kata(teks, daftar):
    """Cocokkan kata utuh di awal kata (mis. 'air' tidak cocok dengan 'kursi pairing')."""
    t = (teks or "").lower()
    return next((k for k in daftar if re.search(r"(?<![a-z])" + re.escape(k), t)), None)


def cari_kolom(header):
    """Petakan judul kolom ke indeks: {'minggu': 0, 'kategori': 2, ...}."""
    peta = {}
    norm = [(h or "").strip().lower() for h in header]
    for kunci, alias in ALIAS.items():
        for i, h in enumerate(norm):
            if h and h in alias and i not in peta.values():
                peta[kunci] = i
                break
        if kunci not in peta:
            for i, h in enumerate(norm):
                if h and any(a in h for a in alias if len(a) > 3) and i not in peta.values():
                    peta[kunci] = i
                    break
    return peta


def _sel_judul(baris, sep):
    sel = [c.strip() for c in next(csv.reader([baris], delimiter=sep), [])]
    while sel and not sel[-1]:
        sel.pop()  # toleransi pemisah berlebih di akhir baris judul
    return sel


def baca_csv(path):
    """Kembalikan (header, peta kolom, pemisah, daftar (no_baris, sel, teks_baris))."""
    try:
        with open(path, "rb") as fh:
            mentah = fh.read()
    except OSError as e:
        gagal(f"File tidak bisa dibuka: {path}", str(e))
    teks = None
    for enc in ("utf-8-sig", "cp1252", "latin-1"):
        try:
            teks = mentah.decode(enc)
            break
        except UnicodeDecodeError:
            continue
    if not teks or not teks.strip():
        gagal("File input kosong.")
    teks = teks.replace("\r\n", "\n").replace("\r", "\n")
    baris_teks = teks.split("\n")

    # Cari baris judul (maks. 10 baris berisi pertama) & pemisah yang mengenali kolom wajib terbanyak.
    pilihan, dicoba = None, []
    for idx in [i for i, b in enumerate(baris_teks) if b.strip()][:10]:
        terbaik = None
        for sep, nama_sep in PEMISAH_KANDIDAT:
            sel = _sel_judul(baris_teks[idx], sep)
            peta = cari_kolom(sel)
            skor = (sum(k in peta for k in KOLOM_WAJIB), len(peta), len(sel))
            if terbaik is None or skor > terbaik[0]:
                terbaik = (skor, sep, nama_sep, sel, peta)
        dicoba.append((idx, terbaik))
        if terbaik[0][0] == len(KOLOM_WAJIB):
            pilihan = (idx, terbaik)
            break
    if pilihan is None:
        idx, (skor, sep, nama_sep, sel, peta) = max(dicoba, key=lambda x: x[1][0])
        hilang = [k for k in KOLOM_WAJIB if k not in peta]
        gagal("Kolom wajib tidak ditemukan: " + ", ".join(hilang),
              {"baris_judul": idx + 1, "isi_baris_judul": baris_teks[idx][:150],
               "kolom_terbaca": sel, "pemisah_dicoba": "titik koma (;), koma (,), tab, garis tegak (|)",
               "yang_dibutuhkan": "minggu, kategori, nominal (opsional: jenis, keterangan, kritis)"})
    idx, (_, sep, nama_sep, header, peta) = pilihan

    rows = []
    rd = csv.reader(io.StringIO(teks), delimiter=sep)
    for sel in rd:
        no = rd.line_num
        if no <= idx + 1:
            continue  # baris sebelum judul & baris judul
        rows.append((no, [c.strip() for c in sel], baris_teks[no - 1][:150] if no - 1 < len(baris_teks) else ""))
    return header, peta, nama_sep, idx + 1, rows


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
    if s in ("semua", "semua minggu", "tiap minggu", "setiap minggu", "rutin", "mingguan", "all", "*"):
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
    if v in ISIAN_TIDAK:
        return False, "pengguna"
    if ada_kata(kategori, KATA_KRITIS):
        return True, "tebakan"
    if ada_kata(kategori, KATA_NONKRITIS):
        return False, "tebakan"
    return None, None  # tidak diketahui


def buat_item(minggu, jenis, kat, nominal, ket, kritis, sumber_kritis, baris):
    low = kat.lower() + " " + (ket or "").lower()
    return {"minggu": minggu, "jenis": jenis, "kategori": kat or "(tanpa nama)", "nominal": nominal,
            "keterangan": ket or "", "kritis": kritis, "wajib": sumber_kritis == "wajib", "baris": baris,
            "piutang": jenis == "masuk" and bool(ada_kata(low, KATA_PIUTANG)),
            "supplier": jenis == "keluar" and sumber_kritis != "wajib" and bool(ada_kata(low, KATA_SUPPLIER))}


def muat_item(header, kolom, rows, n, mulai):
    item, dilewati, peringatan = [], [], []
    ditebak_nonkritis, setelah_horizon = set(), []
    lebar = len(header)

    def ambil(sel, kunci):
        i = kolom.get(kunci)
        return sel[i] if i is not None and i < len(sel) else ""

    for no, sel, mentah in rows:
        if not any(sel):
            continue  # baris kosong / hanya pemisah
        lebih = [c for c in sel[lebar:] if c]
        if lebih:
            dilewati.append({"baris": no, "isi": mentah,
                             "alasan": f"isian lebih banyak ({lebar + len(sel[lebar:])}) dari judul kolom ({lebar}); "
                                       "kemungkinan pemisah kolom ikut dipakai di dalam angka/keterangan "
                                       "(mis. 12,000,000) atau kolom bergeser. Perbaiki baris ini."})
            continue
        kat = ambil(sel, "kategori")
        nom_teks = ambil(sel, "nominal")
        if not kat and not nom_teks:
            continue  # baris kosong
        nom = parse_angka(nom_teks)
        if nom is None:
            dilewati.append({"baris": no, "isi": mentah, "alasan": f"nominal tidak terbaca: '{nom_teks}'"})
            continue
        if nom < 0:
            dilewati.append({"baris": no, "isi": mentah,
                             "alasan": "nominal negatif; tulis angka positif dan isi kolom jenis (masuk/keluar)"})
            continue
        jenis_teks = ambil(sel, "jenis")
        jenis = tebak_jenis(jenis_teks, kat)
        if jenis is None:
            dilewati.append({"baris": no, "isi": mentah,
                             "alasan": f"jenis tidak dikenal: '{jenis_teks}' (pakai masuk/keluar)"})
            continue
        spek = ambil(sel, "minggu")
        try:
            mg = parse_minggu(spek, n, mulai)
        except ValueError as e:
            dilewati.append({"baris": no, "isi": mentah, "alasan": str(e)})
            continue
        luar = [w for w in mg if not 1 <= w <= n]
        if luar:
            peringatan.append(f"Baris {no} ({kat}): minggu {luar} di luar 1–{n}, diabaikan.")
        mg = [w for w in mg if 1 <= w <= n]
        if not mg:
            dilewati.append({"baris": no, "isi": mentah, "alasan": "tidak ada minggu yang valid"})
            continue
        ket = ambil(sel, "keterangan")
        isian_kritis = ambil(sel, "kritis")
        kritis, sumber_kritis = tebak_kritis(isian_kritis, kat, jenis)
        if sumber_kritis == "wajib" and (isian_kritis or "").strip().lower() in ISIAN_TIDAK:
            peringatan.append(f"Baris {no} ({kat}): ditandai 'tidak kritis', tetapi gaji/cicilan/angsuran/leasing/"
                              "pajak/THR/BPJS selalu diperlakukan KRITIS dan tidak ikut simulasi 'tunda'.")
        if jenis == "keluar" and kritis is False and sumber_kritis == "tebakan":
            ditebak_nonkritis.add(kat)
        mt = re.fullmatch(r"(?:tgl|tanggal|bulanan)\s*[:=]?\s*(\d{1,2})", spek.strip().lower())
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
            item.append(buat_item(w, jenis, kat, bulat(nom), ket, kritis, sumber_kritis, no))
    return item, dilewati, peringatan, ditebak_nonkritis, setelah_horizon

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


def catat(aksi, it, grup, ke=None, baru=None):
    """Satu baris rincian perubahan (internal; `ke_minggu` selalu angka)."""
    return {"aksi": aksi, "baris": it.get("baris"), "jenis": it["jenis"], "kategori": it["kategori"],
            "keterangan": it["keterangan"], "nominal": it["nominal"], "dari_minggu": it["minggu"],
            "ke_minggu": it["minggu"] if ke is None else ke,
            "nominal_baru": it["nominal"] if baru is None else baru, "_grup": grup}


def rincian_keluaran(rincian, n):
    keluar = []
    for r in rincian:
        d = {k: v for k, v in r.items() if k != "_grup"}
        if d["baris"] is None:
            d["baris"] = "baru (dari opsi)"
        if isinstance(d["ke_minggu"], int) and d["ke_minggu"] > n:
            d["ke_minggu"] = f"setelah minggu {n}"
        if d["aksi"] == "tambah":
            d["dari_minggu"], d["nominal"] = None, 0
        elif d["aksi"] == "hapus":
            d["ke_minggu"], d["nominal_baru"] = None, 0
        keluar.append(d)
    return keluar


def label_pos(r):
    return r["kategori"] + (f" ({r['keterangan']})" if r.get("keterangan") else "")


def nama_minggu(w, n):
    return f"minggu {w}" if w <= n else f"setelah minggu {n}"


def jelaskan(rincian, n):
    """Ubah rincian perubahan menjadi kalimat persis: pos, nominal, minggu asal → tujuan."""
    grup, urut = {}, []
    for r in rincian:
        if r["_grup"] not in grup:
            grup[r["_grup"]] = []
            urut.append(r["_grup"])
        grup[r["_grup"]].append(r)
    out = []
    for g in urut:
        rs = grup[g]
        r0, aksi, lab = rs[0], rs[0]["aksi"], label_pos(rs[0])
        if aksi == "geser":
            delta = r0["ke_minggu"] - r0["dari_minggu"]
            if len(rs) <= 3:
                for r in rs:
                    out.append(f"{lab} {rp(r['nominal'])}: minggu {r['dari_minggu']} → {nama_minggu(r['ke_minggu'], n)}")
            else:
                lewat = sum(r["nominal"] for r in rs if r["ke_minggu"] > n)
                s = (f"{lab} {rp(r0['nominal'])} di minggu {rentang([r['dari_minggu'] for r in rs])} "
                     f"({len(rs)} kali): masing-masing {'mundur' if delta > 0 else 'maju'} {abs(delta)} minggu")
                if lewat:
                    s += f"; {rp(lewat)} di antaranya pindah ke setelah minggu {n}"
                out.append(s)
        elif aksi == "ubah":
            dalam = [r for r in rs if r["dari_minggu"] <= n]
            selisih = sum(r["nominal_baru"] - r["nominal"] for r in dalam)
            jenis = "pemasukan" if r0["jenis"] == "masuk" else "pengeluaran"
            s = f"{lab}: {rp(r0['nominal'])} → {rp(r0['nominal_baru'])} di minggu {rentang([r['dari_minggu'] for r in rs])}"
            if len(rs) > 1 and selisih:
                s += f" ({len(rs)} kali; total {jenis} {'bertambah' if selisih > 0 else 'berkurang'} {rp(abs(selisih))})"
            out.append(s)
        elif aksi == "hapus":
            tot = sum(r["nominal"] for r in rs)
            s = (f"{lab} {rp(r0['nominal'])} di minggu {rentang([r['dari_minggu'] for r in rs])} dihapus "
                 f"(tidak jadi {'diterima' if r0['jenis'] == 'masuk' else 'dikeluarkan'})")
            if len(rs) > 1:
                s = s[:-1] + f"; {len(rs)} kali, total {rp(tot)})"
            out.append(s)
        elif aksi == "tambah":
            jenis = "pemasukan" if r0["jenis"] == "masuk" else "pengeluaran"
            s = f"{jenis.capitalize()} baru: {lab} {rp(r0['nominal'])} di minggu {rentang([r['ke_minggu'] for r in rs])}"
            if len(rs) > 1:
                s += f" ({len(rs)} kali, total {rp(r0['nominal'] * len(rs))})"
            out.append(s)
        elif aksi == "cicil":
            bag = ", ".join(f"{rp(r['nominal_baru'])} {nama_minggu(r['ke_minggu'], n)}" for r in rs)
            out.append(f"{lab} {rp(r0['nominal'])} di minggu {r0['dari_minggu']} dicicil {len(rs)} kali: {bag}")
    return out


def geser(item, syarat, delta, n, batas_minggu=None, grup="bawaan"):
    """Salin item; item yang memenuhi syarat digeser `delta` minggu (minimal minggu 1)."""
    baru, tergeser, keluar_horizon, rincian = [], 0, 0, []
    for it in item:
        it2 = dict(it)
        if syarat(it) and (batas_minggu is None or it["minggu"] <= batas_minggu):
            w = max(1, it["minggu"] + delta)
            if w != it["minggu"]:
                tergeser += it["nominal"]
                if w > n:
                    keluar_horizon += it["nominal"]
                rincian.append(catat("geser", it, (grup, it["kategori"], it["keterangan"], it["nominal"], w - it["minggu"]), ke=w))
            it2["minggu"] = w
        baru.append(it2)
    return baru, tergeser, keluar_horizon, rincian

# ---------------------------------------------------------------- opsi buatan sendiri

_NOM = r"(?:rp\.?\s*)?\d[\d.,]*(?:\s*(?:miliar|milyar|juta|jt|ribu|rb|k|m)\b)?"
_DAFTAR = r"\d+(?:\s*(?:[-–,]|dan)\s*\d+)*"
_SEL = r"(?:\s+(?:di|dari|pada)\s+minggu\s+(?:ke\s*-?\s*)?(?P<sel>" + _DAFTAR + r"))?"
_SPEK = (r"(?:(?:di|pada)\s+)?(?:minggu\s+(?:ke\s*-?\s*)?(?P<spek1>semua|" + _DAFTAR + r")"
         r"|(?P<spek2>(?:tgl|tanggal)\s*[:=]?\s*\d{1,2}|semua(?:\s+minggu)?|(?:tiap|setiap)\s+minggu"
         r"|(?:setiap|tiap)\s*\d+\s*minggu(?:\s*mulai\s*(?:minggu\s*)?\d+)?))")
_PER = r"(?:\s*(?:per|/)\s*(?:minggu|kali))?"
POLA_AKSI = [
    ("tambah", re.compile(r"tambah(?:kan)?\s+(?P<jenis>masuk|keluar|pemasukan|pengeluaran|penerimaan)\s+"
                          r"(?P<kat>.+?)\s+(?P<nom>" + _NOM + r")" + _PER + r"\s+" + _SPEK, re.I)),
    ("cicil", re.compile(r"(?:cicil|pecah|bagi)\s+(?P<pos>.+?)" + _SEL + r"\s+(?:jadi\s+|menjadi\s+)?(?P<k>\d+)\s*"
                         r"(?:x|kali)\s+(?:mulai\s+)?minggu\s+(?:ke\s*-?\s*)?(?P<w>\d+)"
                         r"(?:\s+(?:setiap|tiap)\s+(?P<step>\d+)\s+minggu)?", re.I)),
    ("geser_ke", re.compile(r"(?:geser|pindah(?:kan)?|tunda|undur|mundurkan|percepat|majukan)\s+(?P<pos>.+?)"
                            + _SEL + r"\s+ke\s+minggu\s+(?:ke\s*-?\s*)?(?P<ke>\d+)", re.I)),
    ("geser_rel", re.compile(r"(?P<verb>geser|pindah(?:kan)?|tunda|undur|mundurkan|mundur|percepat|majukan|maju)\s+"
                             r"(?P<pos>.+?)" + _SEL + r"\s+(?P<tanda>[+-])?\s*(?P<k>\d+)\s+minggu"
                             r"(?:\s+(?P<arah>lebih\s+(?:cepat|awal|lambat|lama)|mundur|maju))?", re.I)),
    ("ubah", re.compile(r"(?:ubah|ganti|jadikan)\s+(?P<pos>.+?)" + _SEL + r"\s+(?:jadi|menjadi)\s+(?P<nom>" + _NOM + r")"
                        + _PER, re.I)),
    ("skala", re.compile(r"(?P<verb>kurangi|potong|pangkas|hemat|turunkan|naikkan|tingkatkan)\s+(?P<pos>.+?)" + _SEL
                         + r"\s+(?:sebesar\s+|sebanyak\s+)?(?:(?P<persen>\d+(?:[.,]\d+)?)\s*(?:%|persen)|(?P<nom>"
                         + _NOM + r"))" + _PER, re.I)),
    ("hapus", re.compile(r"(?:hapus|batalkan|batal|hilangkan|coret|tanpa)\s+(?P<pos>.+?)" + _SEL, re.I)),
    # bentuk singkat tanpa kata kerja: "pinjaman KUR 20jt minggu 2" (jenis ditebak; ditolak bila ragu)
    ("tambah", re.compile(r"(?P<jenis>)(?P<kat>[^\d\s].*?)\s+(?P<nom>" + _NOM + r")" + _PER + r"\s+" + _SPEK, re.I)),
]
KATA_DANA_MASUK = ["pinjaman", "modal", "suntikan", "dana talangan", "hibah"]
KATA_KERJA = {"geser", "pindah", "pindahkan", "tunda", "undur", "mundurkan", "mundur", "percepat", "majukan", "maju",
              "ubah", "ganti", "jadikan", "kurangi", "potong", "pangkas", "hemat", "turunkan", "naikkan",
              "tingkatkan", "hapus", "batalkan", "batal", "hilangkan", "coret", "tanpa", "cicil", "pecah", "bagi",
              "tambah", "tambahkan"}
CONTOH_AKSI = ("geser Renovasi ke minggu 9 | tunda Renovasi 4 minggu | percepat Pelunasan dari minggu 9 ke minggu 7 | "
               "ubah Bahan baku jadi 6jt | kurangi Bahan baku 10% | hapus Mesin press | "
               "cicil Renovasi 3 kali mulai minggu 5 | tambah masuk Pinjaman KUR 20jt minggu 2 | "
               "tambah keluar Cicilan KUR 1,8jt tgl:15")


def parse_daftar(s):
    hasil = set()
    for bag in re.split(r"\s*(?:,|\bdan\b)\s*", s.strip()):
        r = re.fullmatch(r"(\d+)\s*[-–]\s*(\d+)", bag.strip())
        if r:
            a, b = sorted((int(r.group(1)), int(r.group(2))))
            hasil.update(range(a, b + 1))
        elif bag.strip().isdigit():
            hasil.add(int(bag.strip()))
    return hasil


def parse_aksi(teks):
    t = " ".join(teks.strip().split()).rstrip(".")
    for nama, pola in POLA_AKSI:
        m = pola.fullmatch(t)
        if m:
            return nama, m.groupdict()
    return None, None


def pisah_opsi(teks):
    """'Nama | aksi; aksi' -> (nama, [aksi...]). Tanpa '|', nama = teks opsi itu sendiri."""
    teks = " ".join((teks or "").split())
    if "|" in teks:
        label, isi = teks.split("|", 1)
    else:
        label, isi = teks, teks
        # toleransi 'Nama: aksi; aksi' (titik dua + spasi; 'tgl:15' tidak terpengaruh)
        if ": " in teks:
            l2, i2 = teks.split(": ", 1)
            if parse_aksi(i2.split(";")[0])[0]:
                label, isi = l2, i2
    aksi = [x.strip() for x in isi.split(";") if x.strip()]
    return label.strip() or isi.strip(), aksi


def cari_pos(item, pos, sel):
    p = " ".join(pos.lower().split())
    kandidat = [i for i, it in enumerate(item) if sel is None or it["minggu"] in sel]
    for uji in (lambda it: it["kategori"].lower() == p,
                lambda it: p in it["kategori"].lower(),
                lambda it: p in (it["kategori"] + " " + it["keterangan"]).lower()
                or p in f"{it['kategori']} ({it['keterangan']})".lower(),
                lambda it: all(k in (it["kategori"] + " " + it["keterangan"]).lower() for k in p.split())):
        idx = [i for i in kandidat if uji(item[i])]
        if idx:
            return idx
    return []


def terapkan_opsi(item, teks, n, mulai):
    """Terapkan satu opsi ke salinan item. Kembalikan dict dengan item baru + rincian, atau 'error'."""
    label, aksi_list = pisah_opsi(teks)
    item2 = [dict(x) for x in item]
    rincian, catatan = [], []
    if not aksi_list:
        return {"opsi": label, "error": "Opsi kosong.", "contoh_aksi": CONTOH_AKSI}
    nama_pos = sorted({it["kategori"] for it in item})

    def salah(pesan):
        return {"opsi": label, "error": pesan, "contoh_aksi": CONTOH_AKSI}

    for no_aksi, a_teks in enumerate(aksi_list, 1):
        jenis_aksi, g = parse_aksi(a_teks)
        if not jenis_aksi:
            return salah(f"Aksi tidak dikenali: '{a_teks}'.")
        if jenis_aksi == "tambah":
            kat = g["kat"].strip()
            if g["jenis"]:
                jenis = "masuk" if g["jenis"].lower() in ("masuk", "pemasukan", "penerimaan") else "keluar"
            elif kat.split()[0].lower() in KATA_KERJA:
                return salah(f"Aksi tidak dikenali: '{a_teks}'.")
            elif ada_kata(kat, KATA_WAJIB):
                jenis = "keluar"
            elif ada_kata(kat, KATA_MASUK + KATA_DANA_MASUK):
                jenis = "masuk"
            elif ada_kata(kat, KATA_SUPPLIER + KATA_NONKRITIS + KATA_KRITIS):
                jenis = "keluar"
            else:
                return salah(f"Tidak jelas pemasukan atau pengeluaran: '{a_teks}'. Tulis 'tambah masuk ...' "
                             "atau 'tambah keluar ...'.")
            nom = parse_angka(g["nom"])
            if nom is None or nom <= 0:
                return salah(f"Nominal tidak terbaca di '{a_teks}'.")
            spek = g["spek1"] or g["spek2"]
            try:
                mg = parse_minggu(spek, n, mulai)
            except ValueError as e:
                return salah(f"{e} (di '{a_teks}').")
            luar = [w for w in mg if not 1 <= w <= n]
            if luar:
                catatan.append(f"'{a_teks}': minggu {luar} di luar 1–{n}, diabaikan.")
            mg = [w for w in mg if 1 <= w <= n]
            if not mg:
                return salah(f"Tidak ada minggu yang valid di '{a_teks}'.")
            kritis, sumber = tebak_kritis("", kat, jenis)
            for w in mg:
                it = buat_item(w, jenis, kat, bulat(nom), "", kritis, sumber, None)
                item2.append(it)
                rincian.append(catat("tambah", it, (no_aksi,), ke=w))
            continue

        sel = parse_daftar(g["sel"]) if g.get("sel") else None
        pos = g["pos"].strip()
        idx = cari_pos(item2, pos, sel)
        if not idx:
            di = f" di minggu {rentang(sel)}" if sel else ""
            return salah(f"Pos '{pos}'{di} tidak ditemukan. Pos yang ada: {', '.join(nama_pos)}.")
        if jenis_aksi != "ubah" and not (jenis_aksi == "skala" and g["verb"].lower() in ("naikkan", "tingkatkan")):
            wajib = sorted({item2[i]["kategori"] for i in idx if item2[i]["wajib"]})
            if wajib:
                pesan = (f"{', '.join(wajib)} tidak disimulasikan digeser/dikurangi/dicicil/dihapus: gaji, upah, THR, "
                         "cicilan, pajak, dan BPJS adalah kewajiban kritis dan tidak boleh disarankan ditunda.")
                idx = [i for i in idx if not item2[i]["wajib"]]
                if not idx:
                    return salah(pesan)
                catatan.append(pesan)
        if jenis_aksi == "geser_ke":
            ke = int(g["ke"])
            if ke < 1:
                return salah(f"Minggu tujuan harus ≥ 1 (di '{a_teks}').")
            if len({item2[i]["minggu"] for i in idx}) > 1:
                ws = sorted({item2[i]["minggu"] for i in idx})
                return salah(f"'{pos}' ada di {len(ws)} minggu ({rentang(ws)}). Untuk memindah satu pembayaran tulis "
                             f"'geser {pos} dari minggu {ws[0]} ke minggu {ke}', atau geser semuanya dengan "
                             f"'mundurkan {pos} 2 minggu' / 'majukan {pos} 2 minggu'.")
            for i in idx:
                it = item2[i]
                if it["minggu"] != ke:
                    rincian.append(catat("geser", it, (no_aksi, i), ke=ke))
                    it["minggu"] = ke
        elif jenis_aksi == "geser_rel":
            k = int(g["k"])
            verb, arah = g["verb"].lower(), (g.get("arah") or "").lower()
            maju = verb in ("percepat", "majukan", "maju") or g.get("tanda") == "-" or \
                any(x in arah for x in ("cepat", "awal", "maju"))
            delta = -k if maju else k
            for i in idx:
                it = item2[i]
                w = max(1, it["minggu"] + delta)
                if w == 1 and it["minggu"] + delta < 1:
                    catatan.append(f"{label_pos(it)} minggu {it['minggu']}: tidak bisa lebih awal dari minggu 1.")
                if w != it["minggu"]:
                    rincian.append(catat("geser", it, (no_aksi, it["kategori"], it["keterangan"], it["nominal"],
                                                       w - it["minggu"]), ke=w))
                    it["minggu"] = w
        elif jenis_aksi in ("ubah", "skala"):
            if jenis_aksi == "ubah":
                nom = parse_angka(g["nom"])
                if nom is None or nom < 0:
                    return salah(f"Nominal tidak terbaca di '{a_teks}'.")
                hitung = lambda lama: bulat(nom)
            else:
                naik = g["verb"].lower() in ("naikkan", "tingkatkan")
                if g.get("persen"):
                    pr = Decimal(g["persen"].replace(",", "."))
                    hitung = lambda lama: bulat(Decimal(lama) * (1 + (pr if naik else -pr) / 100))
                else:
                    nom = parse_angka(g["nom"])
                    if nom is None:
                        return salah(f"Nominal tidak terbaca di '{a_teks}'.")
                    hitung = lambda lama: bulat(Decimal(lama) + (nom if naik else -nom))
            for i in idx:
                it = item2[i]
                baru = hitung(it["nominal"])
                if baru < 0:
                    catatan.append(f"{label_pos(it)}: hasil pengurangan di bawah nol, dijadikan Rp 0.")
                    baru = 0
                if baru != it["nominal"]:
                    if it["wajib"]:
                        catatan.append(f"{label_pos(it)} adalah kewajiban kritis; perubahan nominalnya harus sudah "
                                       "disepakati (mis. jumlah karyawan berubah).")
                    rincian.append(catat("ubah", it, (no_aksi, it["kategori"], it["keterangan"], it["nominal"], baru),
                                         baru=baru))
                    it["nominal"] = baru
        elif jenis_aksi == "hapus":
            for i in idx:
                rincian.append(catat("hapus", item2[i], (no_aksi, item2[i]["kategori"], item2[i]["keterangan"],
                                                         item2[i]["nominal"])))
            buang = set(idx)
            item2 = [it for j, it in enumerate(item2) if j not in buang]
        elif jenis_aksi == "cicil":
            if len(idx) != 1:
                ws = sorted({item2[i]["minggu"] for i in idx})
                return salah(f"'{pos}' cocok dengan {len(idx)} pembayaran (minggu {rentang(ws)}). Pilih satu: "
                             f"'cicil {pos} dari minggu {ws[0]} {g['k']} kali mulai minggu {g['w']}'.")
            k, w0, step = int(g["k"]), int(g["w"]), int(g.get("step") or 1)
            if not 2 <= k <= 26 or w0 < 1 or step < 1:
                return salah(f"Cicilan harus 2–26 kali, mulai minggu ≥ 1 (di '{a_teks}').")
            i = idx[0]
            asal = item2[i]
            bagian = bulat(Decimal(asal["nominal"]) / k)
            jumlah = [bagian] * (k - 1) + [asal["nominal"] - bagian * (k - 1)]
            baru = []
            for j, nominal in enumerate(jumlah):
                it = dict(asal)
                it["minggu"], it["nominal"] = w0 + j * step, nominal
                baru.append(it)
                rincian.append(catat("cicil", asal, (no_aksi, i), ke=it["minggu"], baru=nominal))
            item2 = item2[:i] + baru + item2[i + 1:]
    if not rincian:
        catatan.append("Tidak ada perubahan (pos sudah di minggu/nominal itu).")
    catatan = list(dict.fromkeys(catatan))  # buang catatan kembar, urutan tetap
    return {"opsi": label, "item": item2, "rincian": rincian, "catatan": catatan, "error": None}

# ---------------------------------------------------------------- utama

def main():
    for aliran in (sys.stdout, sys.stderr):  # Windows: konsol cp1252 tidak bisa mencetak "→", "–", emoji
        try:
            aliran.reconfigure(encoding="utf-8")
        except (AttributeError, ValueError):
            pass
    p = argparse.ArgumentParser(description="Proyeksi arus kas mingguan (13 minggu) untuk UMKM")
    p.add_argument("file", help="CSV rencana penerimaan & pengeluaran")
    p.add_argument("--saldo-awal", required=True, help="Saldo kas+bank di awal minggu 1, mis. 'Rp 25.000.000'")
    p.add_argument("--batas-aman", help="Saldo minimum yang dianggap aman. Default: rata-rata pengeluaran 1 minggu")
    p.add_argument("--mulai", help="Tanggal awal minggu 1 (YYYY-MM-DD atau DD/MM/YYYY)")
    p.add_argument("--jumlah-minggu", type=int, default=13, help="Default 13 (boleh 4–26)")
    p.add_argument("--geser-piutang", type=int, default=2, help="Simulasi: piutang ditagih N minggu lebih cepat (default 2)")
    p.add_argument("--geser-supplier", type=int, default=2, help="Simulasi: bayar supplier mundur N minggu (default 2)")
    p.add_argument("--geser-nonkritis", type=int, default=4, help="Simulasi: belanja non-kritis ditunda N minggu (default 4)")
    p.add_argument("--opsi", action="append", default=[],
                   help="Opsi buatan sendiri 'Nama | aksi; aksi' (boleh diulang, maks. 4). Lihat docstring.")
    p.add_argument("--file-opsi", help="Berkas teks berisi satu opsi per baris (baris '#' diabaikan)")
    p.add_argument("--terapkan", help="Terapkan satu opsi ke tabel utama (tabel 'sesudah tindakan'), format sama dengan --opsi")
    p.add_argument("--ringkas", action="store_true", help="Keluaran tanpa rincian per minggu/kategori (untuk jalan opsi)")
    p.add_argument("--output-csv", help="Tulis tabel proyeksi untuk Excel ke file ini")
    p.add_argument("--pemisah", choices=[";", ","], default=";", help="Pemisah kolom CSV OUTPUT (default ; untuk Excel Indonesia)")
    p.add_argument("--format", choices=["json", "teks"], default="json")
    p.add_argument("--versi", action="version", version=f"proyeksi_kas.py {VERSI}")
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

    daftar_opsi = list(a.opsi)
    if a.file_opsi:
        try:
            with open(a.file_opsi, encoding="utf-8-sig") as fh:
                daftar_opsi += [b.strip() for b in fh if b.strip() and not b.strip().startswith("#")]
        except OSError as e:
            gagal(f"Berkas opsi tidak bisa dibuka: {a.file_opsi}", str(e))

    header, kolom, nama_sep, baris_judul, rows = baca_csv(a.file)
    if not rows or not any(any(sel) for _, sel, _ in rows):
        gagal("File hanya berisi judul kolom, belum ada data.")
    item, dilewati, peringatan, ditebak_nonkritis, setelah_horizon = muat_item(header, kolom, rows, n, mulai)
    if not item:
        gagal("Tidak ada baris valid yang bisa dihitung.", {"baris_dilewati": dilewati})

    # batas aman default dihitung dari rencana ASLI (sebelum --terapkan) agar tabel sebelum/sesudah sebanding
    if a.batas_aman:
        b = parse_angka(a.batas_aman)
        if b is None or b < 0:
            gagal(f"Batas aman tidak terbaca: '{a.batas_aman}'.")
        batas, sumber_batas = bulat(b), "diisi pengguna"
    else:
        batas = bulat(Decimal(sum(proyeksi(item, n, saldo_awal)[1])) / n)
        sumber_batas = "ASUMSI: rata-rata pengeluaran 1 minggu (belum dikonfirmasi pengguna)"

    diterapkan = None
    if a.terapkan:
        t = terapkan_opsi(item, a.terapkan, n, mulai)
        if t["error"]:
            gagal("Tindakan --terapkan tidak bisa dipakai: " + t["error"], {"contoh_aksi": CONTOH_AKSI})
        item = t["item"]
        lewat_t = sum(it["nominal"] for it in item if it["minggu"] > n and it["jenis"] == "keluar")
        diterapkan = {"opsi": t["opsi"], "deskripsi": jelaskan(t["rincian"], n),
                      "rincian": rincian_keluaran(t["rincian"], n), "catatan": t["catatan"],
                      "jatuh_setelah_horizon": lewat_t}
        peringatan.insert(0, f"TABEL INI SUDAH MEMAKAI TINDAKAN '{t['opsi']}': " + "; ".join(diterapkan["deskripsi"]) + ".")
        if lewat_t:
            peringatan.insert(1, f"{rp(lewat_t)} pengeluaran pindah ke setelah minggu {n} karena tindakan ini — "
                                 "kewajiban tetap ada, hanya pindah waktu.")

    masuk, keluar, saldo = proyeksi(item, n, saldo_awal)
    total_keluar = sum(keluar)
    neg, bawah, w_rendah, s_rendah = ringkas_saldo(saldo, batas)

    # rincian per kategori per minggu
    urutan_kat = {"masuk": [], "keluar": []}
    per_kat = {}
    for it in item:
        if not 1 <= it["minggu"] <= n:
            continue
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
        for j in ("keluar", "masuk"):
            isi = "; ".join(f"{x['kategori']}{' (' + x['keterangan'] + ')' if x['keterangan'] else ''} "
                            f"{rp(x['nominal'])}" for x in kejadian[w][j])
            bag.append(f"{j}: {isi or '-'}")
        return f"Minggu {w}: " + " | ".join(bag)

    minggu_data = []
    s_awal = saldo_awal
    for w in range(1, n + 1):
        d = {"minggu": w, "saldo_awal": s_awal, "masuk": masuk[w - 1], "keluar": keluar[w - 1],
             "bersih": masuk[w - 1] - keluar[w - 1], "saldo_akhir": saldo[w - 1],
             "status": "NEGATIF" if saldo[w - 1] < 0 else ("DI BAWAH BATAS AMAN" if saldo[w - 1] < batas else "AMAN")}
        if mulai:
            d["periode"] = periode_minggu(w, mulai)
            d["tanggal_awal"] = (mulai + timedelta(days=7 * (w - 1))).isoformat()
        d["kejadian"] = kejadian[w]
        d["kejadian_teks"] = kalimat_kejadian(w) + (f" ({d['periode']})" if mulai else "")
        minggu_data.append(d)
        s_awal = saldo[w - 1]

    def hasil_simulasi(sal2, lewat):
        ng, bw, wr, sr = ringkas_saldo(sal2, batas)
        setelah = sal2[-1] - lewat
        return ng, bw, wr, sr, setelah, bool(lewat) and setelah < 0

    def kalimat_hasil(ng, bw, wr, sr, akhir, lewat, setelah):
        per = periode_minggu(wr, mulai)
        s = (f"titik terendah minggu {wr}{' (' + per + ')' if per else ''} {rp(sr)}; "
             f"minggu minus: {rentang(ng) if ng else 'tidak ada'}; "
             f"di bawah batas aman: {rentang(bw) if bw else 'tidak ada'}; saldo akhir minggu {n} {rp(akhir)}")
        if lewat:
            s += (f"; {rp(lewat)} pengeluaran pindah ke setelah minggu {n} (tetap harus dibayar) → "
                  f"setelah dibayar saldo {rp(setelah)}")
        return s

    # ------------------------------------------------ simulasi opsi bawaan
    bermasalah = sorted(set(neg + bawah))
    opsi = []
    if bermasalah:
        w1 = bermasalah[0]
        wz = bermasalah[-1]

        def evaluasi(nama, item2, digeser, lewat, rincian, catatan):
            _, _, sal2 = proyeksi(item2, n, saldo_awal)
            ng, bw, wr, sr = ringkas_saldo(sal2, batas)
            desk = jelaskan(rincian, n)
            return {"opsi": nama, "deskripsi": desk, "jumlah_pos_digeser": len(rincian),
                    "nominal_digeser": digeser, "jatuh_setelah_horizon": lewat,
                    "saldo_terendah_baru": sr, "minggu_terendah_baru": wr,
                    "perbaikan_saldo_terendah": sr - s_rendah,
                    "minggu_negatif_baru": ng, "minggu_di_bawah_batas_baru": bw,
                    "saldo_akhir_per_minggu_baru": sal2,
                    "rincian_digeser": rincian_keluaran(rincian, n)[:30], "catatan": catatan}

        gp, gs, gn = a.geser_piutang, a.geser_supplier, a.geser_nonkritis
        it_p, d_p, _, r_p = geser(item, lambda x: x["piutang"] and x["minggu"] > w1 - 1, -gp, n, grup="p")
        if d_p:
            opsi.append(evaluasi(f"Percepat tagihan piutang {gp} minggu", it_p, d_p, 0, r_p,
                                 "Asumsi pelanggan mau bayar lebih cepat (mis. diberi potongan kecil untuk bayar cepat)."
                                 + (f" Opsi ini memajukan {len(r_p)} pembayaran sekaligus (lihat deskripsi); bila hanya "
                                    "sebagian yang realistis, hitung dengan --opsi untuk pos itu saja."
                                    if len(r_p) > 1 else "")))
        it_s, d_s, l_s, r_s = geser(item, lambda x: x["supplier"], gs, n, batas_minggu=wz, grup="s")
        if d_s:
            opsi.append(evaluasi(f"Negosiasi termin supplier mundur {gs} minggu", it_s, d_s, l_s, r_s,
                                 "Hanya pembayaran bahan/supplier sampai minggu bermasalah terakhir yang digeser."))
        it_n, d_n, l_n, r_n = geser(item, lambda x: x["jenis"] == "keluar" and x["kritis"] is False, gn, n,
                                    batas_minggu=wz, grup="n")
        if d_n:
            opsi.append(evaluasi(f"Tunda belanja non-kritis {gn} minggu", it_n, d_n, l_n, r_n,
                                 "Hanya pos yang ditandai/terdeteksi tidak kritis (renovasi, alat baru, iklan, prive, dll.)."))
        if len(opsi) >= 2:
            gab = item
            dg = lw = 0
            rg = []
            for g_id, syarat, delta, bm in (("p", lambda x: x["piutang"] and x["minggu"] > w1 - 1, -gp, None),
                                            ("s", lambda x: x["supplier"], gs, wz),
                                            ("n", lambda x: x["jenis"] == "keluar" and x["kritis"] is False, gn, wz)):
                gab, d, l, r = geser(gab, syarat, delta, n, batas_minggu=bm, grup=g_id)
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
            o["ringkasan_teks"] = (f"{o['opsi']}: " + "; ".join(o["deskripsi"]) + ". Hasil: "
                                   + kalimat_hasil(o["minggu_negatif_baru"], o["minggu_di_bawah_batas_baru"],
                                                   o["minggu_terendah_baru"], o["saldo_terendah_baru"],
                                                   o["saldo_akhir_per_minggu_baru"][-1], lewat, setelah) + ".")
            if lewat:
                o["catatan"] += (f" PERHATIAN: {rp(lewat)} jatuh setelah minggu {n} — kewajiban tetap ada, hanya pindah "
                                 f"waktu. Setelah dibayar, saldo menjadi {rp(setelah)}.")
            if o["hanya_menunda"]:
                o["catatan"] += (" HANYA MENUNDA: opsi ini tidak menyelesaikan masalah, hanya memindahkan kekurangan "
                                 "ke setelah periode proyeksi. Jangan ditulis sebagai solusi.")

    # ------------------------------------------------ opsi buatan sendiri (satu panggilan)
    opsi_pengguna = []
    if len(daftar_opsi) > MAKS_OPSI:
        peringatan.append(f"Hanya {MAKS_OPSI} opsi pertama yang dihitung; {len(daftar_opsi) - MAKS_OPSI} opsi lain "
                          "TIDAK dihitung. Tawarkan ke pengguna sebagai lanjutan.")
    for no_op, teks_op in enumerate(daftar_opsi[:MAKS_OPSI], 1):
        t = terapkan_opsi(item, teks_op, n, mulai)
        if t["error"]:
            opsi_pengguna.append({"no": no_op, "opsi": t["opsi"], "teks_opsi": teks_op, "error": t["error"],
                                  "contoh_aksi": t["contoh_aksi"]})
            continue
        _, _, sal2 = proyeksi(t["item"], n, saldo_awal)
        lewat = sum(it["nominal"] for it in t["item"] if it["minggu"] > n and it["jenis"] == "keluar")
        masuk_lewat = sum(it["nominal"] for it in t["item"] if it["minggu"] > n and it["jenis"] == "masuk")
        ng, bw, wr, sr, setelah, menunda = hasil_simulasi(sal2, lewat)
        desk = jelaskan(t["rincian"], n)
        catatan = list(t["catatan"])
        if masuk_lewat:
            catatan.append(f"{rp(masuk_lewat)} pemasukan pindah ke setelah minggu {n} (belum dihitung di tabel).")
        if menunda:
            catatan.append("HANYA MENUNDA: setelah kewajiban yang tertunda dibayar, saldo minus. Jangan ditulis sebagai solusi.")
        opsi_pengguna.append({
            "no": no_op, "opsi": t["opsi"], "teks_opsi": teks_op, "deskripsi": desk,
            "saldo_terendah": sr, "minggu_terendah": wr, "periode_terendah": periode_minggu(wr, mulai),
            "minggu_negatif": ng, "minggu_di_bawah_batas": bw, "saldo_akhir": sal2[-1],
            "perubahan_saldo_terendah": sr - s_rendah,
            "jatuh_setelah_horizon": lewat, "saldo_setelah_kewajiban_tertunda": setelah, "hanya_menunda": menunda,
            "saldo_akhir_per_minggu": sal2, "rincian": rincian_keluaran(t["rincian"], n), "catatan": catatan,
            "ringkasan_teks": (f"Opsi {no_op} – {t['opsi']}: " + "; ".join(desk) + ". Hasil: "
                               + kalimat_hasil(ng, bw, wr, sr, sal2[-1], lewat, setelah) + "."),
        })

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
        "versi_script": VERSI,
        "asumsi_dan_sumber": {
            "saldo_awal": saldo_awal, "batas_aman": batas, "batas_aman_sumber": sumber_batas,
            "jumlah_minggu": n, "tanggal_mulai": mulai.isoformat() if mulai else None,
            "pemisah_input": nama_sep, "baris_judul": baris_judul,
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
        "opsi_pengguna": opsi_pengguna,
        "baris_dilewati": dilewati,
        "peringatan": peringatan,
    }
    if diterapkan:
        hasil["tindakan_diterapkan"] = diterapkan

    if a.output_csv:
        tulis_csv(a.output_csv, a.pemisah, hasil, n, mulai)
        hasil["file_csv"] = a.output_csv

    if a.ringkas:
        hasil.pop("per_minggu")
        hasil.pop("per_kategori")
        for o in hasil["simulasi_opsi"]:
            o.pop("rincian_digeser", None)
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
    if h.get("tindakan_diterapkan"):
        t = h["tindakan_diterapkan"]
        rows.append([""] * (n + 2))
        rows.append([f"Tabel sudah memakai tindakan: {t['opsi']} ({'; '.join(t['deskripsi'])})"] + [""] * (n + 1))
    ok = [o for o in h.get("opsi_pengguna", []) if not o.get("error")]
    if ok:
        rows.append([""] * (n + 2))
        rows.append(["SIMULASI OPSI (saldo akhir per minggu)"] + [""] * (n + 1))
        for o in ok:
            rows.append([f"Opsi {o['no']}: {o['opsi']} ({'; '.join(o['deskripsi'])})"] + o["saldo_akhir_per_minggu"] + [""])
    try:
        with open(path, "w", encoding="utf-8-sig", newline="") as f:
            csv.writer(f, delimiter=sep).writerows(rows)
    except OSError as e:
        gagal(f"Gagal menulis file CSV: {path}", str(e))


def cetak_teks(h):
    r, a = h["ringkasan"], h["asumsi_dan_sumber"]
    print(f"Saldo awal: {rp(a['saldo_awal'])} | Batas aman: {rp(a['batas_aman'])} ({a['batas_aman_sumber']})")
    print()
    if "per_minggu" in h:
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
    if "per_minggu" in h:
        print("Kejadian per minggu (kutip nomor minggu & pos dari sini, jangan menyimpulkan sendiri):")
        for m in h["per_minggu"]:
            print(f"- {m['kejadian_teks']}")
    else:
        print("Kejadian minggu kritis:")
        for t in r["kejadian_minggu_kritis"]:
            print(f"- {t}")
    print()
    for o in h["simulasi_opsi"]:
        print(f"- Simulasi bawaan {o['ringkasan_teks']} {o['catatan']}")
    if h.get("opsi_pengguna"):
        print()
        print("Opsi Anda (salin deskripsi & angka apa adanya):")
        for o in h["opsi_pengguna"]:
            if o.get("error"):
                print(f"- Opsi {o['no']} – {o['opsi']}: GALAT — {o['error']} Contoh aksi: {o['contoh_aksi']}")
            else:
                print(f"- {o['ringkasan_teks']}" + (f" Catatan: {' '.join(o['catatan'])}" if o["catatan"] else ""))
    for d in h["baris_dilewati"]:
        print(f"! Baris {d['baris']} dilewati: {d['alasan']}" + (f" Isi: {d['isi']}" if d.get("isi") else ""))
    for p in h["peringatan"]:
        print(f"! {p}")
    if h.get("file_csv"):
        print(f"File Excel/CSV: {h['file_csv']}")


if __name__ == "__main__":
    main()
