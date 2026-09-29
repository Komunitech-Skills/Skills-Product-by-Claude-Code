#!/usr/bin/env python3
"""Generator dataset fiktif penguji independen. Menulis CSV (format campur) + truth JSON (angka asli)."""
import json, random
from datetime import date, timedelta

def fmt_id(v, gaya):
    """tulis angka dengan gaya Indonesia macam-macam."""
    if gaya == "titik" and v >= 1000:
        return f"{v:,}".replace(",", ".")
    if gaya == "rb" and v >= 1000 and v % 100 == 0:
        s = f"{v/1000:.1f}".replace(".", ",")
        return s.rstrip("0").rstrip(",") + "rb"
    if gaya == "rp":
        return "Rp " + f"{v:,}".replace(",", ".")
    if gaya == "jt" and v % 100000 == 0:
        return (f"{v/1e6:.1f}".replace(".", ",")) + "jt"
    return str(v)

def tulis(nama, kolom, baris, target=None):
    truth = {}
    with open(nama + ".csv", "w") as f:
        f.write(",".join(["tanggal"] + kolom) + "\n")
        if target:
            f.write(",".join(["TARGET"] + [str(target.get(k, "")) for k in kolom]) + "\n")
        for t, vals in baris:
            sel = []
            for k in kolom:
                v = vals.get(k)
                if v is None:
                    sel.append("")
                elif isinstance(v, tuple):  # (nilai, teks)
                    truth.setdefault(k, {})[t.isoformat()] = v[0]
                    s = v[1]
                    sel.append(f'"{s}"' if "," in s else s)
                elif isinstance(v, str):
                    sel.append(f'"{v}"' if "," in v else v)
                else:
                    truth.setdefault(k, {})[t.isoformat()] = v
                    sel.append(str(v))
            f.write(",".join([t.isoformat()] + sel) + "\n")
    json.dump(truth, open(nama + ".truth.json", "w"), indent=1)

HARI_LAP = date(2026, 9, 29)  # Selasa

# ---------- S1 pabrik garmen 45 hari, Minggu libur
r = random.Random(11)
mulai = HARI_LAP - timedelta(days=44)
baris = []
stok = 9000
for i in range(45):
    t = mulai + timedelta(days=i)
    if t.weekday() == 6:
        baris.append((t, {"catatan": "libur"}))
        continue
    out = r.randint(1150, 1290)
    rej = r.randint(18, 30)
    down = r.randint(10, 40)
    absen = r.choice([0, 1, 1, 2, 2, 3])
    pakai = round(out * 1.6) // 10 * 10
    hari_ke = 44 - i
    catatan = ""
    if hari_ke <= 4:  # 4 hari terakhir reject naik bertahap
        rej = [52, 44, 38, 33][hari_ke - 0] if hari_ke < 4 else 31
        rej = {4: 31, 3: 33, 2: 38, 1: 44, 0: 52}[hari_ke]
    if hari_ke == 0:
        down = 95
        catatan = "mesin jahit obras line 3 sering putus benang"
    if hari_ke == 2:
        catatan = "operator baru 3 orang masuk line 3"
    if t == date(2026, 9, 4):
        out, rej, down = 610, 26, 240  # listrik padam
        catatan = "listrik padam 4 jam"
    stok -= pakai
    if t == date(2026, 9, 23):
        stok += 10000
    if stok < 4500 and hari_ke > 5:
        stok += 12000  # restok
    gaya = r.choice(["titik", "biasa", "rb"])
    baris.append((t, {"output_pcs": (out, fmt_id(out, gaya)), "reject_pcs": rej, "downtime_menit": down,
                      "absen": absen, "stok_kain_m": (stok, fmt_id(stok, "titik")), "pakai_kain_m": pakai,
                      "catatan": catatan}))
tulis("s1-garmen", ["output_pcs", "reject_pcs", "downtime_menit", "absen", "stok_kain_m", "pakai_kain_m", "catatan"],
      baris, target={"output_pcs": "1.200", "reject_pcs": 40, "absen": 3})

# ---------- S2 distributor 30 hari, telat kirim naik
r = random.Random(22)
mulai = HARI_LAP - timedelta(days=29)
baris = []
for i in range(30):
    t = mulai + timedelta(days=i)
    kirim = r.randint(180, 215)
    hari_ke = 29 - i
    if hari_ke <= 9:
        telat = 6 + (9 - hari_ke) * 2 + r.randint(-1, 1)  # naik pelan
    else:
        telat = r.randint(4, 9)
    ret = r.randint(1, 4)
    kel = r.choice([0, 0, 1, 1, 2])
    cat = ""
    if hari_ke == 9:
        cat = "2 armada masuk bengkel; ganti ke ekspedisi pihak ketiga"
    baris.append((t, {"pengiriman": kirim, "telat_kirim": telat, "retur": ret, "keluhan": kel, "catatan": cat}))
tulis("s2-distributor", ["pengiriman", "telat_kirim", "retur", "keluhan", "catatan"], baris,
      target={"telat_kirim": 15, "keluhan": 3})

# ---------- S3 kafe 21 hari, stok
r = random.Random(33)
mulai = HARI_LAP - timedelta(days=20)
baris = []
susu, kopi = 70, 12000
for i in range(21):
    t = mulai + timedelta(days=i)
    akhir_pekan = t.weekday() >= 5
    trx = r.randint(170, 200) + (60 if akhir_pekan else 0)
    omzet = trx * 29500
    omzet = round(omzet, -5)
    ps = round(trx * 0.09)
    pk = trx * 16
    susu -= ps
    kopi -= pk
    if susu < 25 and i < 18:
        susu += 70
    if kopi < 4000 and i < 20:
        kopi += 10000
    waste = r.randint(3, 8)
    baris.append((t, {"transaksi": trx, "penjualan_rp": (omzet, fmt_id(omzet, r.choice(["rp", "jt"]))),
                      "stok_susu_liter": susu, "pakai_susu_liter": ps, "stok_kopi_gr": (kopi, fmt_id(kopi, "titik")),
                      "pakai_kopi_gr": pk, "waste_porsi": waste}))
tulis("s3-kafe", ["transaksi", "penjualan_rp", "stok_susu_liter", "pakai_susu_liter", "stok_kopi_gr", "pakai_kopi_gr", "waste_porsi"],
      baris, target={"penjualan_rp": "Rp 5.000.000"})

# ---------- S4 hanya 5 hari
mulai = HARI_LAP - timedelta(days=4)
baris = [(mulai + timedelta(days=i), {"output_pcs": o, "reject_pcs": j}) for i, (o, j) in
         enumerate([(820, 12), (840, 14), (805, 17), (830, 19), (810, 24)])]
tulis("s4-5hari", ["output_pcs", "reject_pcs"], baris, target={"reject_pcs": 20})
print("ok")
