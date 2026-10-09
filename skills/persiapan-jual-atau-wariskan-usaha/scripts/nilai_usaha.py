#!/usr/bin/env python3
"""Perkiraan RENTANG nilai usaha kecil. Semua kelipatan/persentase wajib dari pengguna.

Pakai: python3 scripts/nilai_usaha.py --laba 2023=120000000 2024=150000000 2025=180000000 \
  --kelipatan 1.5 3 --aset 300000000 --utang 80000000 [opsi]   (Windows: python / py)
Hasil = alat bantu diskusi, BUKAN penilaian resmi dan BUKAN janji harga laku.
"""
import argparse
import json
import sys
from decimal import ROUND_HALF_UP, Decimal, InvalidOperation

ILUSTRASI = ("1.5", "2.5", "3.5")  # hanya bila --ilustrasi; BUKAN angka pasar


def rp(x):
    n = int(Decimal(x).quantize(Decimal(1), rounding=ROUND_HALF_UP))
    s = f"{abs(n):,}".replace(",", ".")
    return ("-" if n < 0 else "") + "Rp" + s


def dec(teks, nama):
    try:
        v = Decimal(str(teks).replace("_", ""))
    except InvalidOperation:
        raise ValueError(f"{nama}: '{teks}' bukan angka")
    if not v.is_finite():
        raise ValueError(f"{nama}: '{teks}' bukan angka")
    return v


def non_negatif(teks, nama):
    v = dec(teks, nama)
    if v < 0:
        raise ValueError(f"{nama} tidak boleh negatif")
    return v


def persen(teks, nama):
    v = non_negatif(teks, nama)
    if v > 100:
        raise ValueError(f"{nama} harus 0-100")
    return v


def parse_laba(items):
    hasil = {}
    for it in items:
        if "=" not in it:
            raise ValueError(f"--laba harus 'tahun=jumlah', bukan '{it}'")
        th, jml = it.split("=", 1)
        th = th.strip()
        if not (th.isdigit() and len(th) == 4):
            raise ValueError(f"tahun tidak valid: '{th}'")
        if th in hasil:
            raise ValueError(f"tahun ganda: {th}")
        hasil[th] = dec(jml, f"laba {th}")  # boleh negatif (rugi)
    return hasil


def hitung(laba, kelipatan, aset=None, utang=Decimal(0), diskon_aset=Decimal(0),
           gaji_diambil=Decimal(0), gaji_pengganti=Decimal(0), biaya_sekali=Decimal(0),
           diskon_pemilik=Decimal(0), biaya_transaksi=Decimal(0),
           kebutuhan_bulanan=None, bulan=None):
    out = {"peringatan": [], "metode": []}
    if not laba and aset is None:
        raise ValueError("butuh minimal laba (--laba) atau aset (--aset)")
    kunci = sorted(laba)[-3:]
    if laba:
        if len(laba) < 3:
            out["peringatan"].append("Laba kurang dari 3 tahun: rentang kurang kuat dan sulit diyakinkan ke calon pembeli.")
        norm = {k: laba[k] + gaji_diambil - gaji_pengganti + biaya_sekali for k in kunci}
        out["laba_normalisasi"] = {k: norm[k] for k in kunci}
        rata = sum(norm.values()) / len(norm)
        terakhir = norm[kunci[-1]]
        out["laba_rata"] = rata
        out["laba_terakhir"] = terakhir
        basis = rata
        if terakhir < rata:
            basis = terakhir
            out["peringatan"].append("Laba tahun terakhir lebih rendah dari rata-rata: dipakai angka tahun terakhir (lebih hati-hati).")
        out["basis"] = basis
        if basis <= 0:
            out["peringatan"].append("Laba normalisasi nol/negatif: metode kelipatan laba tidak dipakai.")
        else:
            lo, hi = min(kelipatan), max(kelipatan)
            faktor = (Decimal(100) - diskon_pemilik) / 100
            batas = []
            for k in (lo, hi):
                batas.append(basis * k * faktor)
            out["metode"].append({"nama": "Kelipatan laba normalisasi", "rendah": batas[0], "tinggi": batas[1],
                                  "rumus": f"basis laba x kelipatan [{lo}-{hi}] x (100 - diskon ketergantungan pemilik {diskon_pemilik}%)/100"})
    if aset is not None:
        bersih = aset * (Decimal(100) - diskon_aset) / 100 - utang
        out["aset_bersih"] = bersih
        if bersih < 0:
            out["peringatan"].append("Utang melebihi nilai aset: nilai aset bersih negatif (jangan dibaca sebagai harga jual).")
        out["metode"].append({"nama": "Nilai aset bersih", "rendah": bersih, "tinggi": bersih,
                              "rumus": f"aset {rp(aset)} x (100 - penyesuaian {diskon_aset}%)/100 - utang {rp(utang)}"})
    if not out["metode"]:
        raise ValueError("tidak ada metode yang bisa dihitung")
    rendah = min(m["rendah"] for m in out["metode"])
    tinggi = max(m["tinggi"] for m in out["metode"])
    out["rentang_bruto"] = (rendah, tinggi)
    bt = (Decimal(100) - biaya_transaksi) / 100
    out["rentang_bersih"] = (rendah * bt, tinggi * bt)
    out["biaya_transaksi_persen"] = biaya_transaksi
    if kebutuhan_bulanan is not None and bulan is not None:
        perlu = kebutuhan_bulanan * bulan
        out["kebutuhan_pasca"] = perlu
        out["selisih_vs_kebutuhan"] = (out["rentang_bersih"][0] - perlu, out["rentang_bersih"][1] - perlu)
    return out


def tampil(o):
    b = []
    b.append("PERKIRAAN RENTANG NILAI USAHA (alat bantu diskusi, bukan penilaian resmi)")
    if "laba_normalisasi" in o:
        b.append("Laba setelah penyesuaian per tahun: " + "; ".join(f"{k}: {rp(v)}" for k, v in o["laba_normalisasi"].items()))
        b.append(f"Rata-rata {rp(o['laba_rata'])}; tahun terakhir {rp(o['laba_terakhir'])}; basis dipakai {rp(o['basis'])}")
    for m in o["metode"]:
        b.append(f"- {m['nama']}: {rp(m['rendah'])} s/d {rp(m['tinggi'])}  [{m['rumus']}]")
    r = o["rentang_bruto"]
    b.append(f"Rentang gabungan: {rp(r[0])} s/d {rp(r[1])}")
    r = o["rentang_bersih"]
    b.append(f"Setelah biaya transaksi {o['biaya_transaksi_persen']}%: {rp(r[0])} s/d {rp(r[1])}")
    if "kebutuhan_pasca" in o:
        s = o["selisih_vs_kebutuhan"]
        b.append(f"Kebutuhan hidup setelah keluar: {rp(o['kebutuhan_pasca'])}; selisih hasil bersih vs kebutuhan: {rp(s[0])} s/d {rp(s[1])}")
    for p in o["peringatan"]:
        b.append("PERINGATAN: " + p)
    b.append("Catatan: kelipatan/persentase adalah ASUMSI dari pengguna, bukan angka pasar. Pajak, BPHTB, dan biaya notaris belum dihitung.")
    return "\n".join(b)


def jsonable(o):
    if isinstance(o, dict):
        return {k: jsonable(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [jsonable(v) for v in o]
    if isinstance(o, Decimal):
        return int(o.quantize(Decimal(1), rounding=ROUND_HALF_UP))
    return o


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--laba", nargs="*", default=[], help="tahun=laba bersih, mis. 2025=180000000 (maks 3 tahun terakhir dipakai)")
    p.add_argument("--kelipatan", nargs="*", default=[], help="kelipatan laba (rendah tinggi), dari pengguna")
    p.add_argument("--ilustrasi", action="store_true", help="pakai kelipatan ilustrasi 1,5/2,5/3,5 (BUKAN angka pasar)")
    p.add_argument("--aset"); p.add_argument("--utang", default="0")
    p.add_argument("--penyesuaian-aset", default="0", help="persen potongan nilai aset (usang/susut)")
    p.add_argument("--gaji-diambil", default="0", help="gaji/ambil pribadi pemilik per tahun yang ada di biaya")
    p.add_argument("--gaji-pengganti", default="0", help="gaji manajer pengganti per tahun")
    p.add_argument("--biaya-sekali", default="0", help="biaya sekali jalan per tahun yang tidak berulang")
    p.add_argument("--diskon-pemilik", default="0", help="persen potongan karena usaha bergantung pada pemilik")
    p.add_argument("--biaya-transaksi", default="0", help="persen biaya (notaris, perantara, dll.)")
    p.add_argument("--kebutuhan-bulanan"); p.add_argument("--bulan")
    p.add_argument("--json", action="store_true")
    try:
        a = p.parse_args(argv)
        laba = parse_laba(a.laba)
        kel = [non_negatif(k, "kelipatan") for k in a.kelipatan]
        if laba and not kel:
            if a.ilustrasi:
                kel = [Decimal(k) for k in ILUSTRASI]
                print("PERINGATAN: kelipatan 1,5-3,5 hanyalah ILUSTRASI, bukan angka pasar. Minta pengguna/penasihat menetapkan sendiri.", file=sys.stderr)
            else:
                raise ValueError("kelipatan wajib diisi pengguna (--kelipatan rendah tinggi) atau pakai --ilustrasi")
        if any(k == 0 for k in kel):
            raise ValueError("kelipatan tidak boleh nol")
        if (a.kebutuhan_bulanan is None) != (a.bulan is None):
            raise ValueError("--kebutuhan-bulanan dan --bulan harus bersamaan")
        o = hitung(
            laba, kel,
            aset=non_negatif(a.aset, "aset") if a.aset is not None else None,
            utang=non_negatif(a.utang, "utang"),
            diskon_aset=persen(a.penyesuaian_aset, "penyesuaian aset"),
            gaji_diambil=non_negatif(a.gaji_diambil, "gaji diambil"),
            gaji_pengganti=non_negatif(a.gaji_pengganti, "gaji pengganti"),
            biaya_sekali=non_negatif(a.biaya_sekali, "biaya sekali"),
            diskon_pemilik=persen(a.diskon_pemilik, "diskon pemilik"),
            biaya_transaksi=persen(a.biaya_transaksi, "biaya transaksi"),
            kebutuhan_bulanan=non_negatif(a.kebutuhan_bulanan, "kebutuhan") if a.kebutuhan_bulanan is not None else None,
            bulan=non_negatif(a.bulan, "bulan") if a.bulan is not None else None,
        )
    except ValueError as e:
        print(f"GAGAL: {e}", file=sys.stderr)
        return 2
    except SystemExit as e:
        return e.code if isinstance(e.code, int) else 2
    print(json.dumps(jsonable(o), ensure_ascii=False, indent=1) if a.json else tampil(o))
    return 0


if __name__ == "__main__":
    sys.exit(main())
