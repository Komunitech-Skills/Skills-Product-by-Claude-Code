#!/usr/bin/env python3
"""Analisis selisih anggaran vs realisasi (budget vs actual variance) untuk UMKM.

Hanya library standar Python 3.8+. Tidak ada akses jaringan. Hanya membaca file yang
diberikan lewat --file (atau teks lewat --data / stdin); tidak menulis file apa pun.

Rumus (Komunitech; kerangka jenis selisih mengikuti praktik umum analisis varians):
  Selisih           = realisasi - anggaran  (Rp & % dari anggaran)
  Arah              : pendapatan naik = MENGUNTUNGKAN; biaya naik = MERUGIKAN (kebalikannya juga)
  Pendapatan (unit) : harga rata-rata P = nilai / unit
      efek volume   = (unit realisasi - unit anggaran) x P anggaran
      efek harga    = (P realisasi - P anggaran) x unit realisasi   (= selisih - efek volume)
      bauran (>= 2 produk berunit): volume total = (U_real_total - U_ang_total) x harga rata2 anggaran
                      bauran = jumlah efek volume per produk - volume total
  Biaya (kuantitas) : efek pemakaian/efisiensi = (Q realisasi - Q anggaran) x harga satuan anggaran
                      efek harga input         = selisih - efek pemakaian
  Biaya variabel    : anggaran disesuaikan = anggaran x faktor volume penjualan
                      (faktor = unit terjual realisasi / anggaran bila semua pendapatan berunit,
                       selain itu pendapatan realisasi / anggaran)
  Materialitas      : |selisih| >= ambang Rp ATAU |%| >= ambang % (default 500rb / 5%), bisa --aturan dan
Pembulatan: rupiah ke rupiah terdekat (0,5 ke atas). Komponen terakhir = selisih - komponen
lain, sehingga jumlah komponen SELALU sama persis dengan total selisih.
"""
import argparse
import csv
import io
import json
import re
import sys
from decimal import ROUND_HALF_UP, Decimal, InvalidOperation, getcontext

getcontext().prec = 40
VERSI = "1.0.1"
LABEL_AGENT = ("[UNTUK AGENT SAJA - jangan disalin apa adanya; sampaikan dengan bahasa awam, "
               "tanpa menyebut script/file/proses]")
DISCLAIMER = ("Analisis selisih ini alat bantu manajemen, bukan audit atau nasihat keuangan/pajak. "
              "Penyebab selisih perlu dicek ke bukti (nota, rekening, catatan stok).")


class Galat(Exception):
    def __init__(self, pesan, saran=""):
        super().__init__(pesan)
        self.pesan, self.saran = pesan, saran


# ------------------------------------------------------------------ parsing angka
PENGALI = {"rb": 10**3, "ribu": 10**3, "k": 10**3, "jt": 10**6, "juta": 10**6,
           "m": 10**9, "miliar": 10**9, "milyar": 10**9}


def parse_angka(teks, nama, boleh_kosong=True):
    """'Rp 45.000.000' | '45jt' | '1,5 juta' | '150rb' | '(5jt)' | '1.234,5' -> Decimal atau None."""
    if teks is None:
        return None
    asli = str(teks)
    s = asli.strip().lower()
    if s in ("", "-", "—", "n/a", "na"):
        if boleh_kosong:
            return None
        raise Galat(f"{nama}: kosong", "Isi angkanya, mis. 4.500.000 atau 4,5jt.")
    s = re.sub(r"^\s*(rp|idr)\.?\s*", "", s).strip()
    s = re.sub(r"\s*(unit|pcs|cup|porsi|jam|kg|liter|ltr|org|orang|x|buah|paket|kwh)\s*$", "", s)
    negatif = False
    if s.startswith("(") and s.endswith(")"):
        negatif, s = True, s[1:-1].strip()
    m = re.match(r"^(minus|min|-)\s*", s)
    if m:
        negatif, s = True, s[m.end():]
    s = re.sub(r"^\s*(rp|idr)\.?\s*", "", s).replace(" ", "")
    m = re.fullmatch(r"([0-9][0-9.,]*)(rb|ribu|k|jt|juta|m|miliar|milyar)?", s)
    if not m:
        raise Galat(f"{nama}: angka '{asli}' tidak terbaca",
                    "Tulis seperti 4500000, 4.500.000, 4,5jt, atau 450rb.")
    num, suf = m.group(1).strip(".,"), m.group(2)
    if "," in num and "." in num:
        num = num.replace(".", "").replace(",", ".") if num.rfind(",") > num.rfind(".") else num.replace(",", "")
    elif "," in num:
        b = num.split(",")
        if len(b) > 2:
            num = num.replace(",", "")
        elif len(b[1]) == 3 and not suf:
            num = num.replace(",", "")  # 45,000 gaya Excel Inggris = ribuan
        else:
            num = num.replace(",", ".")
    elif "." in num:
        b = num.split(".")
        if len(b) > 2 or len(b[1]) == 3:
            num = num.replace(".", "")
    try:
        v = Decimal(num) * Decimal(PENGALI[suf] if suf else 1)
    except InvalidOperation:
        raise Galat(f"{nama}: angka '{asli}' tidak terbaca", "Contoh: 4,5jt")
    return -v if negatif else v


def parse_persen(teks):
    s = str(teks).strip().replace("%", "").replace(",", ".")
    try:
        v = Decimal(s)
    except InvalidOperation:
        raise Galat(f"ambang persen '{teks}' tidak terbaca", "Contoh: 5 atau 7,5")
    if v < 0:
        raise Galat("ambang persen tidak boleh negatif", "Contoh: 5")
    return v


def bulat(x):
    return int(Decimal(x).quantize(Decimal(1), rounding=ROUND_HALF_UP))


def rp(n):
    n = int(n)
    return ("-" if n < 0 else "") + "Rp" + f"{abs(n):,}".replace(",", ".")


def rp_tanda(n):
    n = int(n)
    return ("+" if n > 0 else ("-" if n < 0 else "±")) + "Rp" + f"{abs(n):,}".replace(",", ".")


def fmt_unit(x):
    x = Decimal(x)
    if x == x.to_integral_value():
        return f"{int(x):,}".replace(",", ".")
    return f"{x.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP):,}".replace(",", "_").replace(".", ",").replace("_", ".")


def persen(sel, ang):
    if ang == 0:
        return None
    return (Decimal(sel) * 100 / abs(Decimal(ang))).quantize(Decimal("0.1"), rounding=ROUND_HALF_UP)


def pct(x):
    if x is None:
        return "tidak dianggarkan"
    s = f"{x:.1f}".replace(".", ",")
    return ("+" if x > 0 else "") + s + "%"


# ------------------------------------------------------------------ baca tabel
KOLOM = {
    "pos": ["pos", "akun", "item", "keterangan", "uraian", "nama", "pos anggaran", "kategori", "line item", "rincian"],
    "jenis": ["jenis", "tipe", "type", "kelompok jenis"],
    "sifat": ["sifat", "perilaku", "variabel/tetap"],
    "anggaran": ["anggaran", "budget", "target", "rencana", "rab", "plan", "nilai anggaran", "anggaran rp"],
    "realisasi": ["realisasi", "aktual", "actual", "real", "nilai realisasi", "realisasi rp", "hasil"],
    "unit_anggaran": ["unit anggaran", "qty anggaran", "kuantitas anggaran", "volume anggaran", "jumlah anggaran", "unit budget", "qty budget"],
    "unit_realisasi": ["unit realisasi", "qty realisasi", "kuantitas realisasi", "volume realisasi", "jumlah realisasi", "unit aktual", "qty actual", "qty aktual"],
    "harga_anggaran": ["harga anggaran", "harga satuan anggaran", "tarif anggaran", "harga budget"],
    "harga_realisasi": ["harga realisasi", "harga satuan realisasi", "tarif realisasi", "harga aktual"],
    "satuan": ["satuan", "unit satuan", "uom"],
}


def norm(h):
    return re.sub(r"\s+", " ", re.sub(r"[_\-/().:]+", " ", str(h).strip().lower())).strip()


def petakan_header(header):
    peta = {}
    for i, h in enumerate(header):
        n = norm(h)
        for kunci, alias in KOLOM.items():
            if kunci in peta:
                continue
            if n in alias:
                peta[kunci] = i
                break
    if "pos" not in peta and header:
        if norm(header[0]) not in sum(KOLOM.values(), []):
            peta["pos"] = 0
    return peta


def baca_teks(teks):
    baris = [b for b in teks.replace("\r\n", "\n").split("\n") if b.strip()]
    if not baris:
        raise Galat("data kosong", "Tempel tabel dengan kolom pos, anggaran, realisasi.")
    # tabel markdown
    if sum(1 for b in baris if b.strip().startswith("|")) >= 2:
        rows = []
        for b in baris:
            b = b.strip()
            if not b.startswith("|"):
                continue
            sel = [c.strip() for c in b.strip("|").split("|")]
            if all(re.fullmatch(r":?-{2,}:?", c) for c in sel if c):
                continue
            rows.append(sel)
        return rows
    kepala = baris[0]
    if "\t" in kepala:
        delim = "\t"
    elif ";" in kepala:
        delim = ";"
    elif "|" in kepala:
        delim = "|"
    else:
        delim = ","
    return [r for r in csv.reader(io.StringIO("\n".join(baris)), delimiter=delim)]


KATA_PENDAPATAN = ("penjualan", "pendapatan", "omzet", "omset", "revenue", "sales", "pemasukan", "income")
KATA_PENGURANG = ("biaya", "beban", "retur", "diskon", "potongan", "hpp", "harga pokok", "komisi marketplace", "refund")
KATA_BIAYA = ("gaji", "upah", "honor", "sewa", "listrik", "air", "iklan", "promosi", "ads", "ongkir", "ongkos",
              "transport", "bensin", "bbm", "internet", "pulsa", "lembur", "bahan", "kemasan", "perawatan",
              "servis", "service", "pajak", "asuransi", "bunga", "cicilan", "admin", "komisi", "bpjs", "thr",
              "atk", "perlengkapan", "penyusutan", "gas", "sampah", "keamanan", "langganan", "software",
              "pengiriman", "packing", "insentif", "bonus", "makan", "konsumsi", "operasional", "pemeliharaan", "rent", "salary", "wage", "utilit", "marketing",
              "shipping", "cogs", "expense", "cost", "deterjen", "sabun", "obat", "pakan", "bibit",
              "sparepart", "suku cadang", "pewangi", "plastik")
KATA_RINGKASAN = ("total", "jumlah", "subtotal", "laba", "rugi", "profit", "grand total", "net")


def tebak_jenis(pos):
    n = pos.lower()
    if any(k in n for k in KATA_PENGURANG):
        return "biaya", False
    if any(k in n for k in KATA_PENDAPATAN):
        return "pendapatan", False
    if any(re.search(r"(^|[^a-z])" + k, n) for k in KATA_BIAYA):
        return "biaya", False
    return "biaya", True


def baris_ringkasan(pos):
    n = norm(pos)
    return any(re.search(r"(^|\s)" + re.escape(k) + r"($|\s)", n) for k in KATA_RINGKASAN)


def jenis_dari(teks):
    n = norm(teks)
    if n in ("pendapatan", "penjualan", "pemasukan", "revenue", "income", "p", "omzet"):
        return "pendapatan"
    if n in ("biaya", "beban", "pengeluaran", "expense", "cost", "b", "hpp"):
        return "biaya"
    raise Galat(f"jenis '{teks}' tidak dikenal", "Isi kolom jenis dengan 'pendapatan' atau 'biaya'.")


def ambil_pos(rows, catatan):
    if len(rows) < 2:
        raise Galat("tabel minimal punya baris judul + 1 pos", "Contoh judul: pos;anggaran;realisasi")
    peta = petakan_header(rows[0])
    for wajib in ("anggaran", "realisasi"):
        if wajib not in peta:
            raise Galat(f"kolom '{wajib}' tidak ditemukan di baris judul: {rows[0]}",
                        "Beri judul kolom, mis. pos;anggaran;realisasi (boleh juga budget/actual, target/aktual).")
    data, dilewati, ringkasan = [], [], []
    tebak = []
    for no, r in enumerate(rows[1:], start=2):
        if not any(str(c).strip() for c in r):
            continue
        ambil = lambda k: (r[peta[k]] if k in peta and peta[k] < len(r) else None)  # noqa: E731
        pos = (ambil("pos") or "").strip() or f"Pos baris {no}"
        if baris_ringkasan(pos) and not ambil("jenis"):
            dilewati.append(f"'{pos}' (baris ringkasan; total & laba dihitung ulang)")
            try:
                ringkasan.append((pos, parse_angka(ambil("anggaran"), pos), parse_angka(ambil("realisasi"), pos)))
            except Galat:
                pass
            continue
        ang = parse_angka(ambil("anggaran"), f"{pos} - anggaran")
        real = parse_angka(ambil("realisasi"), f"{pos} - realisasi")
        ua = parse_angka(ambil("unit_anggaran"), f"{pos} - unit anggaran")
        ur = parse_angka(ambil("unit_realisasi"), f"{pos} - unit realisasi")
        ha = parse_angka(ambil("harga_anggaran"), f"{pos} - harga anggaran")
        hr = parse_angka(ambil("harga_realisasi"), f"{pos} - harga realisasi")
        if ang is None and ua is not None and ha is not None:
            ang = ua * ha
        if real is None and ur is not None and hr is not None:
            real = ur * hr
        if ang is None or real is None:
            dilewati.append(f"'{pos}' ({'anggaran' if ang is None else 'realisasi'} kosong)")
            continue
        if ang < 0 or real < 0:
            raise Galat(f"{pos}: nilai negatif ({rp(bulat(ang))} / {rp(bulat(real))})",
                        "Tulis nilai positif; arah (pendapatan/biaya) ditentukan oleh jenis pos.")
        if ambil("jenis") and str(ambil("jenis")).strip():
            jenis, tebakan = jenis_dari(ambil("jenis")), False
        else:
            jenis, tebakan = tebak_jenis(pos)
            if tebakan:
                tebak.append(pos)
        for nama_u, u, harga, nilai in (("anggaran", ua, ha, ang), ("realisasi", ur, hr, real)):
            if u is not None and harga is not None and u > 0:
                if abs(u * harga - nilai) > max(Decimal(1), abs(nilai) * Decimal("0.01")):
                    catatan.append(f"'{pos}': unit x harga {nama_u} ({rp(bulat(u * harga))}) tidak sama dengan "
                                   f"nilai {nama_u} ({rp(bulat(nilai))}); dipakai nilai, harga dihitung ulang = nilai/unit.")
        sifat = norm(ambil("sifat") or "")
        data.append({"pos": pos, "jenis": jenis, "jenis_tebakan": tebakan,
                     "anggaran": bulat(ang), "realisasi": bulat(real),
                     "unit_anggaran": ua, "unit_realisasi": ur,
                     "satuan": (ambil("satuan") or "").strip(),
                     "variabel": sifat.startswith("var") or sifat in ("v", "ikut volume", "ikut penjualan")})
    kosong = [x for x in dilewati if "kosong)" in x]
    if kosong:
        catatan.append("PERHATIAN: total, laba, dan margin belum lengkap karena ada pos tanpa angka (lihat 'Dilewati'). "
                       "Jangan sebut laba ini sebagai laba akhir; minta angkanya.")
    if tebak:
        catatan.append("Dianggap BIAYA karena nama pos tidak jelas (tanyakan bila ternyata pendapatan): " + ", ".join(tebak))
    if not data:
        raise Galat("tidak ada pos yang lengkap (anggaran DAN realisasi)", "Isi realisasi tiap pos, lalu kirim ulang.")
    nama = [d["pos"].lower() for d in data]
    dobel = sorted({n for n in nama if nama.count(n) > 1})
    if dobel:
        catatan.append("Nama pos dobel (dihitung terpisah, cek apakah terhitung dua kali): " + ", ".join(dobel))
    return data, dilewati, ringkasan


def cocokkan_ringkasan(ringkasan, tot, catatan):
    for pos, a, r in ringkasan:
        n = norm(pos)
        if "laba" in n or "rugi" in n or "profit" in n:
            k = "laba"
        elif any(x in n for x in ("pendapatan", "penjualan", "omzet", "omset")):
            k = "pendapatan"
        elif any(x in n for x in ("biaya", "beban", "pengeluaran")):
            k = "biaya"
        else:
            continue
        for lab, v, h in (("anggaran", a, tot[k]["anggaran"]), ("realisasi", r, tot[k]["realisasi"])):
            if v is not None and abs(bulat(v) - h) > 1:
                catatan.append(f"Baris '{pos}' di tabel ({lab} {rp(bulat(v))}) BEDA dengan hitungan dari pos ({rp(h)}): "
                               f"mungkin ada pos yang belum ditempel (pajak, cicilan, penyusutan) atau salah jumlah. Tanyakan.")


# ------------------------------------------------------------------ hitung
def dekomposisi(d, catatan):
    sel = d["realisasi"] - d["anggaran"]
    ua, ur = d["unit_anggaran"], d["unit_realisasi"]
    if ua is None or ur is None:
        return None
    if ua <= 0 or ur <= 0:
        catatan.append(f"'{d['pos']}': unit 0 atau negatif, pemecahan harga/volume dilewati.")
        return None
    pa = Decimal(d["anggaran"]) / ua
    pr = Decimal(d["realisasi"]) / ur
    vol = bulat((ur - ua) * pa)
    hasil = {"unit_anggaran": fmt_unit(ua), "unit_realisasi": fmt_unit(ur),
             "harga_satuan_anggaran": str(pa.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)),
             "harga_satuan_realisasi": str(pr.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))}
    if d["jenis"] == "pendapatan":
        hasil.update({"efek_volume": vol, "efek_harga": sel - vol})
    else:
        hasil.update({"efek_pemakaian": vol, "efek_harga_input": sel - vol})
    return hasil


def arah(jenis, sel):
    if sel == 0:
        return "sesuai"
    naik = sel > 0
    return "menguntungkan" if (naik == (jenis == "pendapatan")) else "merugikan"


def analisis(data, ambang_rp, ambang_pct, aturan, catatan):
    for d in data:
        d["selisih"] = d["realisasi"] - d["anggaran"]
        d["persen"] = persen(d["selisih"], d["anggaran"])
        d["arah"] = arah(d["jenis"], d["selisih"])
        d["dampak_laba"] = d["selisih"] if d["jenis"] == "pendapatan" else -d["selisih"]
        kena_rp = abs(d["selisih"]) >= ambang_rp
        kena_pct = d["persen"] is None and d["selisih"] != 0 or (d["persen"] is not None and abs(d["persen"]) >= ambang_pct)
        d["material"] = d["selisih"] != 0 and ((kena_rp and kena_pct) if aturan == "dan" else (kena_rp or kena_pct))
        d["tidak_dianggarkan"] = d["anggaran"] == 0 and d["realisasi"] > 0
        d["pemecahan"] = dekomposisi(d, catatan)

    pend = [d for d in data if d["jenis"] == "pendapatan"]
    biaya = [d for d in data if d["jenis"] == "biaya"]
    tot = {}
    for nama, kel in (("pendapatan", pend), ("biaya", biaya)):
        a = sum(d["anggaran"] for d in kel)
        r = sum(d["realisasi"] for d in kel)
        tot[nama] = {"anggaran": a, "realisasi": r, "selisih": r - a, "persen": persen(r - a, a),
                     "arah": arah(nama, r - a)}
    la = tot["pendapatan"]["anggaran"] - tot["biaya"]["anggaran"]
    lr = tot["pendapatan"]["realisasi"] - tot["biaya"]["realisasi"]
    tot["laba"] = {"anggaran": la, "realisasi": lr, "selisih": lr - la, "persen": persen(lr - la, la),
                   "arah": arah("pendapatan", lr - la),
                   "margin_anggaran": persen(la, tot["pendapatan"]["anggaran"]) if tot["pendapatan"]["anggaran"] else None,
                   "margin_realisasi": persen(lr, tot["pendapatan"]["realisasi"]) if tot["pendapatan"]["realisasi"] else None}
    if not pend:
        catatan.append("Tidak ada pos pendapatan: laba tidak bermakna, yang dianalisis hanya biaya.")

    # bauran penjualan (>= 2 pos pendapatan berunit)
    bauran = None
    berunit = [d for d in pend if d["pemecahan"]]
    if len(berunit) >= 2:
        ua_t = sum(d["unit_anggaran"] for d in berunit)
        ur_t = sum(d["unit_realisasi"] for d in berunit)
        harga_rata_ang = Decimal(sum(d["anggaran"] for d in berunit)) / ua_t
        vol_total = bulat((ur_t - ua_t) * harga_rata_ang)
        jumlah_vol = sum(d["pemecahan"]["efek_volume"] for d in berunit)
        jumlah_harga = sum(d["pemecahan"]["efek_harga"] for d in berunit)
        bauran = {"produk": [d["pos"] for d in berunit],
                  "unit_anggaran_total": fmt_unit(ua_t), "unit_realisasi_total": fmt_unit(ur_t),
                  "efek_volume_total": vol_total, "efek_bauran": jumlah_vol - vol_total,
                  "efek_harga": jumlah_harga,
                  "jumlah": vol_total + (jumlah_vol - vol_total) + jumlah_harga,
                  "selisih_produk_ini": sum(d["selisih"] for d in berunit),
                  "catatan": "Bauran hanya bermakna bila satuan antarproduk sebanding (mis. sama-sama cup/pcs)."}
        sat = {d["satuan"].lower() for d in berunit if d["satuan"]}
        if len(sat) > 1:
            catatan.append("Satuan produk berbeda (" + ", ".join(sorted(sat)) + "): efek bauran kurang bermakna; pakai efek harga/volume per produk.")

    # anggaran fleksibel untuk biaya variabel
    variabel = [d for d in biaya if d["variabel"]]
    fleks = None
    if variabel:
        if pend and all(d["pemecahan"] for d in pend):
            faktor = Decimal(sum(d["unit_realisasi"] for d in pend)) / Decimal(sum(d["unit_anggaran"] for d in pend))
            dasar = "unit terjual realisasi / anggaran"
            if len(pend) > 1:
                catatan.append("Biaya variabel disesuaikan dengan total unit terjual semua produk; bila bauran produk "
                               "bergeser (produk murah/mahal), angka 'setelah disesuaikan' hanya perkiraan kasar.")
        elif tot["pendapatan"]["anggaran"] > 0:
            faktor = Decimal(tot["pendapatan"]["realisasi"]) / Decimal(tot["pendapatan"]["anggaran"])
            dasar = "pendapatan realisasi / anggaran (unit tidak lengkap; kenaikan harga jual ikut terhitung)"
        else:
            faktor = None
        if faktor is not None:
            fleks = {"faktor_volume": str(faktor.quantize(Decimal("0.0001"), rounding=ROUND_HALF_UP)), "dasar": dasar, "pos": []}
            for d in variabel:
                adj = bulat(Decimal(d["anggaran"]) * faktor)
                d["anggaran_disesuaikan"] = adj
                d["efek_volume_penjualan"] = adj - d["anggaran"]
                d["selisih_setelah_disesuaikan"] = d["realisasi"] - adj
                fleks["pos"].append({"pos": d["pos"], "anggaran_disesuaikan": adj,
                                     "efek_volume_penjualan": adj - d["anggaran"],
                                     "selisih_setelah_disesuaikan": d["realisasi"] - adj,
                                     "persen_setelah_disesuaikan": persen(d["realisasi"] - adj, adj)})

    material = sorted([d for d in data if d["material"]], key=lambda d: (-abs(d["selisih"]), d["pos"]))
    for i, d in enumerate(material, start=1):
        d["peringkat"] = i
    jembatan = sorted([d for d in data if d["dampak_laba"] != 0], key=lambda d: -abs(d["dampak_laba"]))
    return tot, bauran, fleks, material, jembatan


def hasil_json(data, tot, bauran, fleks, material, jembatan, args, catatan, dilewati):
    def bersih(d):
        o = {k: d[k] for k in ("pos", "jenis", "anggaran", "realisasi", "selisih", "arah", "dampak_laba", "material")}
        o["persen"] = None if d["persen"] is None else str(d["persen"])
        o["peringkat_material"] = d.get("peringkat")
        o["tidak_dianggarkan"] = d["tidak_dianggarkan"]
        if d["jenis_tebakan"]:
            o["jenis_ditebak"] = True
        if d["pemecahan"]:
            o["pemecahan"] = d["pemecahan"]
        if "anggaran_disesuaikan" in d:
            o["anggaran_disesuaikan"] = d["anggaran_disesuaikan"]
            o["efek_volume_penjualan"] = d["efek_volume_penjualan"]
            o["selisih_setelah_disesuaikan"] = d["selisih_setelah_disesuaikan"]
        return o
    t = json.loads(json.dumps(tot, default=str))
    return {"versi": VERSI, "periode": args.periode,
            "ambang": {"rupiah": int(args._ambang_rp), "persen": str(args._ambang_pct), "aturan": args.aturan},
            "pos": [bersih(d) for d in data], "total": t,
            "material_urut": [d["pos"] for d in material],
            "jembatan_laba": [{"pos": d["pos"], "dampak_laba": d["dampak_laba"]} for d in jembatan],
            "bauran": bauran, "anggaran_fleksibel": json.loads(json.dumps(fleks, default=str)) if fleks else None,
            "cek_jumlah": cek_jumlah(data, tot, bauran),
            "catatan": catatan, "dilewati": dilewati, "disclaimer": DISCLAIMER}


def cek_jumlah(data, tot, bauran):
    ok = sum(d["dampak_laba"] for d in data) == tot["laba"]["selisih"]
    for d in data:
        p = d["pemecahan"]
        if p:
            k = (p.get("efek_volume", 0) + p.get("efek_harga", 0) + p.get("efek_pemakaian", 0) + p.get("efek_harga_input", 0))
            ok = ok and k == d["selisih"]
    if bauran:
        ok = ok and bauran["jumlah"] == bauran["selisih_produk_ini"]
    return "cocok" if ok else "TIDAK COCOK"


def teks(data, tot, bauran, fleks, material, jembatan, args, catatan, dilewati):
    L = [LABEL_AGENT, f"ANALISIS SELISIH ANGGARAN vs REALISASI{(' - ' + args.periode) if args.periode else ''}",
         f"Ambang material: {rp(args._ambang_rp)} {'ATAU' if args.aturan == 'atau' else 'DAN'} "
         f"{str(args._ambang_pct).replace('.', ',')}% dari anggaran", ""]
    L.append("RINGKASAN")
    for k, lab in (("pendapatan", "Total pendapatan"), ("biaya", "Total biaya"), ("laba", "Laba (pendapatan - biaya)")):
        t = tot[k]
        L.append(f"  {lab}: anggaran {rp(t['anggaran'])} | realisasi {rp(t['realisasi'])} | selisih "
                 f"{rp_tanda(t['selisih'])} ({pct(t['persen']) if t['persen'] is not None else 'persen tidak berlaku'}) {t['arah'].upper()}")
    if tot["laba"]["margin_anggaran"] is not None and tot["laba"]["margin_realisasi"] is not None:
        L.append(f"  Margin laba: anggaran {pct(tot['laba']['margin_anggaran']).lstrip('+')} -> realisasi "
                 f"{pct(tot['laba']['margin_realisasi']).lstrip('+')}")
    L += ["", "PER POS (selisih = realisasi - anggaran)"]
    for d in data:
        tanda = " [MATERIAL #%d]" % d["peringkat"] if d["material"] else ""
        tb = " [TIDAK DIANGGARKAN]" if d["tidak_dianggarkan"] else ""
        jt = ", ditebak" if d["jenis_tebakan"] else ""
        L.append(f"  {d['pos']} ({d['jenis']}{jt}): {rp(d['anggaran'])} -> {rp(d['realisasi'])} = "
                 f"{rp_tanda(d['selisih'])} ({pct(d['persen'])}) {d['arah'].upper()}{tanda}{tb}")
        p = d["pemecahan"]
        if p:
            if d["jenis"] == "pendapatan":
                L.append(f"      unit {p['unit_anggaran']} -> {p['unit_realisasi']}; harga rata2 {rp(bulat(Decimal(p['harga_satuan_anggaran'])))}"
                         f" -> {rp(bulat(Decimal(p['harga_satuan_realisasi'])))}; efek volume {rp_tanda(p['efek_volume'])}, "
                         f"efek harga {rp_tanda(p['efek_harga'])}")
            else:
                L.append(f"      kuantitas {p['unit_anggaran']} -> {p['unit_realisasi']}; harga satuan {rp(bulat(Decimal(p['harga_satuan_anggaran'])))}"
                         f" -> {rp(bulat(Decimal(p['harga_satuan_realisasi'])))}; efek jumlah/pemakaian "
                         f"{rp_tanda(p['efek_pemakaian'])}, efek harga satuan {rp_tanda(p['efek_harga_input'])}")
        if "anggaran_disesuaikan" in d:
            L.append(f"      biaya variabel: anggaran disesuaikan volume {rp(d['anggaran_disesuaikan'])} "
                     f"(efek volume penjualan {rp_tanda(d['efek_volume_penjualan'])}); selisih setelah disesuaikan "
                     f"{rp_tanda(d['selisih_setelah_disesuaikan'])} ({pct(persen(d['selisih_setelah_disesuaikan'], d['anggaran_disesuaikan']))})")
    if bauran:
        L += ["", f"BAURAN PENJUALAN ({', '.join(bauran['produk'])}): unit total {bauran['unit_anggaran_total']} -> "
              f"{bauran['unit_realisasi_total']}",
              f"  efek volume total {rp_tanda(bauran['efek_volume_total'])} + efek bauran {rp_tanda(bauran['efek_bauran'])} "
              f"+ efek harga {rp_tanda(bauran['efek_harga'])} = {rp_tanda(bauran['jumlah'])}"]
    if fleks:
        L.append(f"  Faktor volume penjualan untuk biaya variabel: {fleks['faktor_volume'].replace('.', ',')} ({fleks['dasar']})")
    L += ["", "POS MATERIAL (urut rupiah terbesar)"]
    if material:
        for d in material:
            L.append(f"  {d['peringkat']}. {d['pos']}: {rp_tanda(d['selisih'])} ({pct(d['persen'])}) {d['arah']}")
    else:
        L.append("  Tidak ada pos yang melewati ambang.")
    L += ["", f"JEMBATAN LABA: laba anggaran {rp(tot['laba']['anggaran'])}"]
    utama, sisa = jembatan[:6], jembatan[6:]
    for d in utama:
        L.append(f"  {rp_tanda(d['dampak_laba'])}  {d['pos']}")
    if sisa:
        L.append(f"  {rp_tanda(sum(d['dampak_laba'] for d in sisa))}  pos lain ({len(sisa)})")
    L.append(f"  = laba realisasi {rp(tot['laba']['realisasi'])} (cek jumlah: {cek_jumlah(data, tot, bauran)})")
    if catatan or dilewati:
        L += ["", "CATATAN"] + [f"  - {c}" for c in catatan] + [f"  - Dilewati: {x}" for x in dilewati]
    L += ["", DISCLAIMER]
    return "\n".join(L)


def main(argv=None):
    ap = argparse.ArgumentParser(description="Analisis selisih anggaran vs realisasi (Rupiah, Decimal).")
    ap.add_argument("--file", help="CSV/TSV/teks tabel (kolom: pos, anggaran, realisasi; opsional jenis, sifat, unit_anggaran, unit_realisasi, harga_anggaran, harga_realisasi, satuan)")
    ap.add_argument("--data", help="tabel sebagai teks (baris dipisah \\n atau baris baru)")
    ap.add_argument("--periode", default="", help="mis. 'Juli 2026' atau 'Kuartal 3 2026'")
    ap.add_argument("--ambang-rp", default="500rb", help="ambang material rupiah (default 500rb)")
    ap.add_argument("--ambang-persen", default="5", help="ambang material persen (default 5)")
    ap.add_argument("--aturan", choices=["atau", "dan"], default="atau", help="material bila salah satu (atau) / keduanya (dan) terlampaui")
    ap.add_argument("--variabel", default="", help="nama pos biaya variabel dipisah ';' (mis. 'HPP;Ongkir') bila kolom sifat tidak ada")
    ap.add_argument("--format", choices=["json", "teks"], default="json")
    args = ap.parse_args(argv)
    try:
        if args.file:
            try:
                with open(args.file, encoding="utf-8-sig") as f:
                    isi = f.read()
            except OSError as e:
                raise Galat(f"file tidak bisa dibuka: {e}", "Periksa nama file, atau tempel isinya lewat --data.")
        elif args.data is not None:
            isi = args.data.replace("\\n", "\n")
        else:
            isi = sys.stdin.read()
        args._ambang_rp = bulat(parse_angka(args.ambang_rp, "ambang rupiah", boleh_kosong=False))
        if args._ambang_rp < 0:
            raise Galat("ambang rupiah tidak boleh negatif", "Contoh: 500rb")
        args._ambang_pct = parse_persen(args.ambang_persen)
        catatan = []
        data, dilewati, ringkasan = ambil_pos(baca_teks(isi), catatan)
        if args.variabel:
            nama_var = {x.strip().lower() for x in args.variabel.split(";") if x.strip()}
            ketemu = set()
            for d in data:
                if d["pos"].lower() in nama_var:
                    if d["jenis"] != "biaya":
                        raise Galat(f"'{d['pos']}' bukan pos biaya", "--variabel hanya untuk pos biaya.")
                    d["variabel"] = True
                    ketemu.add(d["pos"].lower())
            if nama_var - ketemu:
                raise Galat("pos --variabel tidak ditemukan: " + ", ".join(sorted(nama_var - ketemu)),
                            "Tulis nama pos persis seperti di tabel.")
        tot, bauran, fleks, material, jembatan = analisis(data, args._ambang_rp, args._ambang_pct, args.aturan, catatan)
        cocokkan_ringkasan(ringkasan, tot, catatan)
    except Galat as g:
        print(json.dumps({"error": g.pesan, "saran": g.saran}, ensure_ascii=False), file=sys.stderr)
        return 2
    if args.format == "teks":
        print(teks(data, tot, bauran, fleks, material, jembatan, args, catatan, dilewati))
    else:
        print(json.dumps(hasil_json(data, tot, bauran, fleks, material, jembatan, args, catatan, dilewati),
                         ensure_ascii=False, indent=2, default=str))
    return 0


if __name__ == "__main__":
    sys.exit(main())
