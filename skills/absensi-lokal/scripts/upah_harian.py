#!/usr/bin/env python3
"""upah_harian.py (absensi-lokal, Komunitech) - upah mingguan/periode pekerja HARIAN LEPAS tanpa database.

Untuk warung/bengkel/toko yang menggaji harian (mis. tiap Sabtu): upah = hari x tarif harian
(+ setengah hari), lembur, tambahan, potongan/kasbon. Lembur dicek terhadap MINIMUM PP 35/2021:
  upah sebulan  = upah harian x 25 (pola 6 hari kerja) atau x 21 (pola 5 hari)   (Pasal 33 ayat (1))
  upah sejam    = upah sebulan / 173                                             (Pasal 32 ayat (2))
  hari kerja    : jam ke-1 x 1,5; jam berikutnya x 2 (per hari)                  (Pasal 31 ayat (1))
  hari libur    : pola 6: jam 1-7 x2, jam 8 x3, jam 9-11 x4; pola 5: jam 1-8 x2, jam 9 x3, jam 10-12 x4
                                                                                 (Pasal 31 ayat (2) a & (3))
  lembur minimum = jam setara x upah sebulan / 173, dibulatkan SEKALI ke rupiah terdekat per pekerja.
Bila pemilik membayar lembur dengan tarif per jam sendiri (--pekerja "...; tarif-lembur=15rb"), script
memakai tarif itu untuk total DAN memberi peringatan bila di bawah minimum, plus total versi minimum.

Hanya library standar; tidak menyimpan apa pun. Contoh:
  python3 upah_harian.py --pola 6 --periode "28 Sep - 3 Okt 2026" \
      --pekerja "Agus; tarif=120rb; hari=6; lembur=2; tarif-lembur=15rb" \
      --pekerja "Budi; tarif=110rb; hari=5; potongan=200rb" \
      --pekerja "Cici; tarif=100rb; hari=5; setengah=1" --json
  python3 upah_harian.py --file pekerja.csv --json
"""
import argparse
import csv
import io
import json
import os
import re
import sys
from decimal import Decimal

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from absensi import (PEMBAGI_UPAH_SEJAM, TANGGA_LIBUR, bulat_rp, dstr, fjam, jam_setara_hari_kerja,  # noqa: E402
                     jam_setara_libur, parse_angka, rp)

VERSI = "1.0.8"
KALI_POLA = {"6": 25, "5": 21}
MAKS_LEMBUR_HARI = Decimal(4)     # PP 35/2021 Pasal 26 ayat (1)
MAKS_LEMBUR_MINGGU = Decimal(18)  # PP 35/2021 Pasal 26 ayat (1)
BATAS_TER_HARIAN_0 = Decimal(450000)  # PMK 168/2023: upah sehari s.d. Rp450.000 -> 0%
DISCLAIMER = ("Lembur minimum: PP 35/2021 Pasal 31-33 (upah harian x 25/21 = upah sebulan; upah sejam = 1/173), "
              "dibulatkan ke rupiah terdekat. PPh 21 tidak dihitung (upah sehari s.d. Rp450.000 umumnya 0%, "
              "PMK 168/2023). Alat bantu hitung, bukan nasihat hukum; kasus khusus tanyakan ke Disnaker/konsultan.")
SINONIM = {
    "nama": ["nama", "pekerja", "karyawan"],
    "tarif": ["tarif", "upah", "upah-harian", "upah_harian", "upahharian", "gaji-harian", "harian"],
    "hari": ["hari", "hari-penuh", "hari_penuh", "masuk", "hadir"],
    "setengah": ["setengah", "setengah-hari", "setengah_hari", "1/2"],
    "lembur": ["lembur", "lembur-kerja", "lembur_kerja", "lembur-hari-kerja"],
    "lembur_libur": ["lembur-libur", "lembur_libur", "lemburlibur"],
    "tarif_lembur": ["tarif-lembur", "tarif_lembur", "tariflembur", "lembur-per-jam", "lembur_per_jam"],
    "tambahan": ["tambahan", "bonus", "uang-makan", "uang_makan"],
    "potongan": ["potongan", "kasbon", "potong"],
    "pola": ["pola", "pola-kerja", "hari-kerja", "hari_kerja"],
}


class Gagal(Exception):
    pass


def kunci(k):
    k = k.strip().lower().replace(" ", "-")
    for std, alias in SINONIM.items():
        if k in alias:
            return std
    return None


def angka(teks, nama, label, boleh_kosong=True):
    if teks is None or str(teks).strip() == "":
        if boleh_kosong:
            return Decimal(0)
        raise Gagal("%s: %s wajib diisi." % (label, nama))
    v = parse_angka(str(teks).strip())
    if v is None or v < 0:
        raise Gagal("%s: %s '%s' tidak terbaca (contoh: 120000, 120rb, Rp 120.000)." % (label, nama, teks))
    return v


def daftar_jam(teks, label, nama):
    """'2' / '2+1' / '2, 1,5' -> [Decimal] (satu angka = satu hari)."""
    if teks is None or str(teks).strip() == "":
        return []
    hasil = []
    for b in re.split(r"[+/]|\s+|;(?=\s*\d)", str(teks).replace(", ", "+")):
        b = b.strip().lower().replace("jam", "").strip()
        if not b:
            continue
        v = parse_angka(b)
        if v is None or v < 0:
            raise Gagal("%s: jam %s '%s' tidak terbaca (contoh: 2, 1,5, 2+1 untuk dua hari)." % (label, nama, teks))
        if v > 0:
            hasil.append(v)
    return hasil


def baca_pekerja_teks(teks):
    bag = [x.strip() for x in teks.split(";") if x.strip()]
    if not bag:
        raise Gagal("Data pekerja kosong.")
    d = {}
    if "=" not in bag[0]:
        d["nama"] = bag.pop(0)
    for b in bag:
        if "=" not in b:
            raise Gagal("Bagian '%s' perlu format kunci=nilai (mis. tarif=120rb)." % b)
        k, v = b.split("=", 1)
        std = kunci(k)
        if std is None:
            raise Gagal("Kunci '%s' tidak dikenal. Pakai: tarif, hari, setengah, lembur, lembur-libur, tarif-lembur, "
                        "tambahan, potongan, pola." % k.strip())
        d[std] = v.strip()
    return d


def baca_csv(path):
    with open(path, "rb") as f:
        mentah = f.read()
    for enc in ("utf-8-sig", "cp1252"):
        try:
            teks = mentah.decode(enc)
            break
        except UnicodeDecodeError:
            continue
    try:
        dialek = csv.Sniffer().sniff(teks[:2048], delimiters=",;\t")
    except csv.Error:
        dialek = csv.excel
    rows = list(csv.reader(io.StringIO(teks), dialek))
    if not rows:
        raise Gagal("File kosong.")
    hdr = [kunci(h) for h in rows[0]]
    if "nama" not in hdr or "tarif" not in hdr:
        raise Gagal("CSV perlu kolom nama dan tarif (upah harian). Kolom terbaca: %s" % ", ".join(rows[0]))
    out = []
    for r in rows[1:]:
        if not any(c.strip() for c in r):
            continue
        out.append({h: (r[i].strip() if i < len(r) else "") for i, h in enumerate(hdr) if h})
    return out


def hitung_pekerja(d, pola_umum):
    label = d.get("nama") or "Pekerja"
    peringatan = []
    tarif = angka(d.get("tarif"), "tarif (upah harian)", label, boleh_kosong=False)
    if tarif == 0:
        raise Gagal("%s: tarif harian harus lebih dari 0." % label)
    hari = angka(d.get("hari"), "hari", label)
    setengah = angka(d.get("setengah"), "setengah hari", label)
    pola = str(d.get("pola") or pola_umum).strip().replace("hari", "").strip()
    if pola not in KALI_POLA:
        raise Gagal("%s: pola kerja '%s' tidak dikenal; pakai 6 (6 hari kerja/minggu) atau 5." % (label, pola))
    lembur = daftar_jam(d.get("lembur"), label, "lembur")
    lembur_libur = daftar_jam(d.get("lembur_libur"), label, "lembur libur")
    tarif_lembur = d.get("tarif_lembur")
    tarif_lembur = angka(tarif_lembur, "tarif lembur", label) if tarif_lembur not in (None, "") else None
    tambahan = angka(d.get("tambahan"), "tambahan", label)
    potongan = angka(d.get("potongan"), "potongan", label)

    if hari + setengah > 7:
        peringatan.append("%s: %s hari + %s setengah hari lebih dari 7 hari; pastikan periodenya memang lebih dari "
                          "seminggu." % (label, fjam(hari), fjam(setengah)))
    upah_hadir = bulat_rp(tarif * hari + tarif * setengah / 2)
    upah_sebulan = tarif * KALI_POLA[pola]
    setara = Decimal(0)
    rincian = []
    for j in lembur:
        s = jam_setara_hari_kerja(j)
        setara += s
        rincian.append("hari kerja %s jam = %s jam setara" % (fjam(j), fjam(s)))
        if j > MAKS_LEMBUR_HARI:
            peringatan.append("%s: lembur %s jam dalam sehari melebihi batas 4 jam/hari (PP 35/2021 Pasal 26)."
                              % (label, fjam(j)))
    for j in lembur_libur:
        s, salah = jam_setara_libur(j, pola)
        if salah:
            raise Gagal("%s: lembur hari libur %s jam %s." % (label, fjam(j), salah))
        setara += s
        rincian.append("hari libur %s jam = %s jam setara" % (fjam(j), fjam(s)))
    jam_total = sum(lembur, Decimal(0)) + sum(lembur_libur, Decimal(0))
    if sum(lembur, Decimal(0)) > MAKS_LEMBUR_MINGGU:
        peringatan.append("%s: lembur hari kerja %s jam melebihi 18 jam/minggu (PP 35/2021 Pasal 26)."
                          % (label, fjam(sum(lembur, Decimal(0)))))
    lembur_min = bulat_rp(setara * upah_sebulan / PEMBAGI_UPAH_SEJAM) if setara else 0
    if tarif_lembur is not None and jam_total:
        lembur_bayar = bulat_rp(jam_total * tarif_lembur)
        dasar_bayar = "tarif pemilik %s/jam x %s jam" % (rp(tarif_lembur), fjam(jam_total))
        if lembur_bayar < lembur_min:
            peringatan.append("%s: lembur dibayar %s (%s) DI BAWAH minimum PP 35/2021 %s; selisih %s. Upah lembur "
                              "di bawah minimum berisiko dipersoalkan pekerja/Disnaker; keputusan tetap di pemilik." % (
                                  label, rp(lembur_bayar), dasar_bayar, rp(lembur_min), rp(lembur_min - lembur_bayar)))
    else:
        lembur_bayar = lembur_min
        dasar_bayar = "minimum PP 35/2021" if jam_total else "-"
    bruto = upah_hadir + lembur_bayar + bulat_rp(tambahan)
    bersih = bruto - bulat_rp(potongan)
    bersih_min = upah_hadir + max(lembur_bayar, lembur_min) + bulat_rp(tambahan) - bulat_rp(potongan)
    if bersih < 0:
        peringatan.append("%s: potongan %s lebih besar dari upah %s; tanyakan ke pemilik sisa kasbon dibawa ke "
                          "periode berikutnya atau tidak." % (label, rp(potongan), rp(bruto)))
    if tarif > BATAS_TER_HARIAN_0:
        peringatan.append("%s: upah harian %s di atas Rp450.000, PPh 21 harian bisa terutang (PMK 168/2023); hitung "
                          "dengan skill pph21-ter atau konsultan pajak." % (label, rp(tarif)))
    return {
        "nama": label, "tarif": tarif, "pola": int(pola), "hari": hari, "setengah_hari": setengah,
        "upah_hadir": upah_hadir,
        "rumus_upah_hadir": "%s x %s hari%s" % (rp(tarif), fjam(hari),
                                                (" + %s x 1/2 x %s" % (rp(tarif), fjam(setengah))) if setengah else ""),
        "lembur_jam": jam_total, "lembur_jam_setara": setara, "lembur_rincian": rincian,
        "upah_sebulan_dasar_lembur": upah_sebulan,
        "upah_sejam": (upah_sebulan / PEMBAGI_UPAH_SEJAM).quantize(Decimal("0.01")),
        "lembur_minimum_pp35": lembur_min, "lembur_dibayar": lembur_bayar, "dasar_lembur_dibayar": dasar_bayar,
        "tambahan": bulat_rp(tambahan), "potongan": bulat_rp(potongan), "total_dibayar": bersih,
        "total_versi_minimum_pp35": bersih_min, "peringatan": peringatan,
    }


def teks_hasil(hasil, periode):
    t = ["UPAH HARIAN%s" % (" - " + periode if periode else "")]
    for i, h in enumerate(hasil, 1):
        t.append("%d. %s (%s per hari, %d hari kerja seminggu)" % (i, h["nama"], rp(h["tarif"]), h["pola"]))
        t.append("   Hadir: %s = %s" % (h["rumus_upah_hadir"], rp(h["upah_hadir"])))
        if h["lembur_jam"]:
            t.append("   Lembur %s jam (%s): %s" % (fjam(h["lembur_jam"]), "; ".join(h["lembur_rincian"]),
                                                   rp(h["lembur_dibayar"]) + " [" + h["dasar_lembur_dibayar"] + "]"))
            t.append("   Minimum PP 35/2021: %s x %d -> upah sebulan %s / 173 = %s/jam x %s jam setara = %s" % (
                rp(h["tarif"]), KALI_POLA[str(h["pola"])], rp(h["upah_sebulan_dasar_lembur"]),
                ("Rp " + format(h["upah_sejam"], ",.2f").replace(",", "_").replace(".", ",").replace("_", ".")),
                fjam(h["lembur_jam_setara"]), rp(h["lembur_minimum_pp35"])))
        if h["tambahan"]:
            t.append("   Tambahan: %s" % rp(h["tambahan"]))
        if h["potongan"]:
            t.append("   Potongan/kasbon: -%s" % rp(h["potongan"]))
        t.append("   DIBAYAR: %s" % rp(h["total_dibayar"]))
        if h["total_versi_minimum_pp35"] != h["total_dibayar"]:
            t.append("   (bila lembur sesuai minimum PP 35/2021: %s)" % rp(h["total_versi_minimum_pp35"]))
    total = sum(h["total_dibayar"] for h in hasil)
    total_min = sum(h["total_versi_minimum_pp35"] for h in hasil)
    t.append("TOTAL DIBAYAR: %s" % rp(total))
    if total_min != total:
        t.append("Total versi lembur minimum PP 35/2021: %s" % rp(total_min))
    per = [p for h in hasil for p in h["peringatan"]]
    if per:
        t.append("PERHATIAN (%d):" % len(per))
        t.extend("- " + p for p in per)
    t.append(DISCLAIMER)
    return "\n".join(t), total, total_min


def ke_json(x):
    if isinstance(x, Decimal):
        return int(x) if x == x.to_integral_value() else float(dstr(x))
    if isinstance(x, dict):
        return {k: ke_json(v) for k, v in x.items()}
    if isinstance(x, list):
        return [ke_json(v) for v in x]
    return x


def main(argv=None):
    p = argparse.ArgumentParser(description="Upah pekerja harian lepas (tanpa database).", allow_abbrev=False)
    p.add_argument("--pekerja", action="append", default=[],
                   help='"Nama; tarif=120rb; hari=6; setengah=1; lembur=2+1; lembur-libur=3; tarif-lembur=15rb; '
                        'tambahan=20rb; potongan=200rb; pola=6"')
    p.add_argument("--file", help="CSV: nama,tarif,hari,setengah,lembur,lembur_libur,tarif_lembur,tambahan,potongan,pola")
    p.add_argument("--pola", default="6", help="Pola kerja umum: 6 (default) atau 5 hari/minggu")
    p.add_argument("--periode", default="", help="Label periode, mis. '28 Sep - 3 Okt 2026'")
    p.add_argument("--json", action="store_true")
    a = p.parse_args(argv)
    try:
        data = [baca_pekerja_teks(x) for x in a.pekerja]
        if a.file:
            data += baca_csv(a.file)
        if not data:
            raise Gagal("Isi minimal satu --pekerja atau --file.")
        hasil = [hitung_pekerja(d, str(a.pola)) for d in data]
        teks, total, total_min = teks_hasil(hasil, a.periode)
    except (Gagal, OSError) as e:
        pesan = str(e) if isinstance(e, Gagal) else "File tidak bisa dibaca: %s" % e
        if a.json:
            print(json.dumps({"ok": False, "error": pesan}, ensure_ascii=False))
        else:
            print("GAGAL: " + pesan, file=sys.stderr)
        return 1
    if a.json:
        print(json.dumps(ke_json({"ok": True, "versi": VERSI, "mode": "baca", "periode": a.periode,
                                  "pekerja": hasil, "total_dibayar": total, "total_versi_minimum_pp35": total_min,
                                  "peringatan": [x for h in hasil for x in h["peringatan"]],
                                  "disclaimer": DISCLAIMER, "teks": teks}), ensure_ascii=False, indent=1))
    else:
        print(teks)
    return 0


if __name__ == "__main__":
    sys.exit(main())
