#!/usr/bin/env python3
"""Perkiraan RENTANG nilai usaha kecil. Semua kelipatan/persentase wajib dari pengguna.

Pakai: python3 scripts/nilai_usaha.py --laba 2023=120000000 2024=150000000 2025=180000000 \
  --kelipatan 1.5 3 --aset 300000000 --utang 80000000 --biaya-sekali 2024=12000000 [opsi]
  (Windows: python / py)
Hasil = alat bantu diskusi, BUKAN penilaian resmi dan BUKAN janji harga laku.

Versi 1.0.1:
- --biaya-sekali per tahun (TAHUN=JUMLAH, boleh diulang); hanya ditambahkan ke tahun itu.
- Utang diperlakukan sama di kedua metode: keduanya dihitung SEBELUM utang, lalu utang
  dikurangkan sekali (dilunasi pemilik dari hasil jual, atau --utang-ikut bila utang ikut
  berpindah/tetap di badan usaha). Kebutuhan hidup dibandingkan dengan hasil bersih ke pemilik.
- --porsi untuk jual/beli sebagian (mis. bagian sekutu CV atau saham PT).
"""
import argparse
import json
import sys
from decimal import ROUND_HALF_UP, Decimal, InvalidOperation

ILUSTRASI = ("1.5", "2.5", "3.5")  # hanya bila --ilustrasi; BUKAN angka pasar
BATAS_ANGKA = Decimal(10) ** 15  # Rp1.000 triliun; di atas ini dianggap salah ketik
TAHUN_MIN, TAHUN_MAKS = 1900, 2100


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
    if abs(v) > BATAS_ANGKA:
        raise ValueError(f"{nama}: '{teks}' terlalu besar (maks. 1.000 triliun); cek salah ketik")
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


def cek_tahun(th, nama):
    th = th.strip()
    if not (th.isdigit() and len(th) == 4 and TAHUN_MIN <= int(th) <= TAHUN_MAKS):
        raise ValueError(f"{nama}: tahun tidak valid: '{th}' (tulis 4 angka, mis. 2025)")
    return th


def parse_laba(items):
    hasil = {}
    for it in items:
        if "=" not in it:
            raise ValueError(f"--laba harus 'tahun=jumlah', bukan '{it}'")
        th, jml = it.split("=", 1)
        th = cek_tahun(th, "--laba")
        if th in hasil:
            raise ValueError(f"tahun ganda: {th}")
        hasil[th] = dec(jml, f"laba {th}")  # boleh negatif (rugi)
    return hasil


def parse_biaya_sekali(items, laba):
    """TAHUN=JUMLAH (boleh beberapa; tahun sama dijumlahkan). Angka tanpa tahun hanya
    diterima bila --laba berisi tepat satu tahun (dipasang ke tahun itu)."""
    hasil = {}
    for it in items:
        if "=" in it:
            th, jml = it.split("=", 1)
            th = cek_tahun(th, "--biaya-sekali")
        else:
            if len(laba) != 1:
                raise ValueError(
                    f"--biaya-sekali '{it}' harus disertai tahun kejadiannya, mis. --biaya-sekali 2024={it}; "
                    "biaya sekali jalan hanya ditambahkan ke tahun terjadinya, bukan ke semua tahun")
            th, jml = next(iter(laba)), it
        if th not in laba:
            raise ValueError(f"--biaya-sekali {th}: tahun itu tidak ada di --laba")
        hasil[th] = hasil.get(th, Decimal(0)) + non_negatif(jml, f"biaya sekali {th}")
    return hasil


def hitung(laba, kelipatan, aset=None, utang=Decimal(0), diskon_aset=Decimal(0),
           gaji_diambil=Decimal(0), gaji_pengganti=Decimal(0), biaya_sekali=None,
           diskon_pemilik=Decimal(0), biaya_transaksi=Decimal(0),
           kebutuhan_bulanan=None, bulan=None, porsi=Decimal(100), utang_ikut=False):
    biaya_sekali = biaya_sekali or {}
    out = {"peringatan": [], "metode": []}
    if not laba and aset is None:
        raise ValueError("butuh minimal laba (--laba) atau aset (--aset)")
    kunci = sorted(laba)[-3:]
    basis = None
    if laba:
        if len(laba) < 3:
            out["peringatan"].append("Laba kurang dari 3 tahun: rentang kurang kuat dan sulit diyakinkan ke calon pembeli.")
        tak_dipakai = sorted(th for th in biaya_sekali if th not in kunci)
        if tak_dipakai:
            out["peringatan"].append("Biaya sekali jalan tahun " + ", ".join(tak_dipakai)
                                     + " tidak dipakai: di luar 3 tahun terakhir.")
        norm = {k: laba[k] + gaji_diambil - gaji_pengganti + biaya_sekali.get(k, Decimal(0)) for k in kunci}
        out["laba_normalisasi"] = norm
        out["biaya_sekali"] = {k: biaya_sekali[k] for k in kunci if k in biaya_sekali}
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
            out["peringatan"].append("Laba setelah penyesuaian nol/negatif: metode kelipatan laba tidak dipakai; benahi laba dulu.")
        else:
            lo, hi = min(kelipatan), max(kelipatan)
            faktor = (Decimal(100) - diskon_pemilik) / 100
            out["metode"].append({"nama": "Kelipatan laba normalisasi (nilai usaha berjalan, sebelum utang)",
                                  "rendah": basis * lo * faktor, "tinggi": basis * hi * faktor,
                                  "rumus": f"basis laba x kelipatan [{lo}-{hi}] x (100 - diskon ketergantungan pemilik {diskon_pemilik}%)/100"})
    if aset is not None:
        nilai_aset = aset * (Decimal(100) - diskon_aset) / 100
        out["nilai_aset"] = nilai_aset
        out["aset_bersih"] = nilai_aset - utang
        if nilai_aset - utang < 0:
            out["peringatan"].append("Utang melebihi nilai aset: aset dikurangi utang negatif (jangan dibaca sebagai harga jual).")
        out["metode"].append({"nama": "Nilai aset setelah penyesuaian (batas bawah bila hanya aset dijual, sebelum utang)",
                              "rendah": nilai_aset, "tinggi": nilai_aset,
                              "rumus": f"aset {rp(aset)} x (100 - penyesuaian {diskon_aset}%)/100"})
    if not out["metode"]:
        raise ValueError(f"laba setelah penyesuaian nol/negatif (basis {rp(basis)}) dan aset tidak diisi: "
                         "nilai usaha belum bisa dihitung; isi --aset atau benahi laba dulu")
    laba_m = [m for m in out["metode"] if m["nama"].startswith("Kelipatan")]
    if laba_m:
        rendah, tinggi = laba_m[0]["rendah"], laba_m[0]["tinggi"]
        if aset is not None and out["nilai_aset"] > rendah:
            out["peringatan"].append(
                f"Nilai aset ({rp(out['nilai_aset'])}) lebih tinggi dari batas bawah kelipatan laba: "
                "harga di bawah nilai aset kurang masuk akal; bandingkan dengan menjual aset saja.")
    else:
        rendah = tinggi = out["nilai_aset"]
    out["rentang_bruto"] = (rendah, tinggi)  # nilai usaha 100%, sebelum utang

    # Utang: dikurangkan SEKALI, sama untuk kedua metode.
    if porsi < 100 and utang > 0 and not utang_ikut:
        utang_ikut = True
        out["peringatan"].append("Jual/beli sebagian: utang badan usaha tetap di usaha, jadi dikurangkan dulu dari nilai sebelum dikalikan porsi.")
    out["utang"] = utang
    out["utang_ikut"] = utang_ikut
    out["porsi"] = porsi
    p = porsi / 100
    if utang_ikut:
        harga = ((rendah - utang) * p, (tinggi - utang) * p)
    else:
        harga = (rendah * p, tinggi * p)
    out["harga"] = harga
    bt = biaya_transaksi / 100
    out["rentang_bersih"] = tuple(h - max(h, Decimal(0)) * bt for h in harga)  # biaya transaksi tidak dari angka negatif
    out["biaya_transaksi_persen"] = biaya_transaksi
    dilunasi = Decimal(0) if utang_ikut else utang
    out["utang_dilunasi_pemilik"] = dilunasi
    out["hasil_bersih_pemilik"] = tuple(r - dilunasi for r in out["rentang_bersih"])
    if out["hasil_bersih_pemilik"][0] < 0:
        out["peringatan"].append("Di batas bawah, hasil bersih ke pemilik negatif: utang/biaya lebih besar dari harga.")
    if kebutuhan_bulanan is not None and bulan is not None:
        perlu = kebutuhan_bulanan * bulan
        out["kebutuhan_pasca"] = perlu
        out["selisih_vs_kebutuhan"] = tuple(h - perlu for h in out["hasil_bersih_pemilik"])
    return out


def tampil(o):
    b = []
    b.append("PERKIRAAN RENTANG NILAI USAHA (alat bantu diskusi, bukan penilaian resmi)")
    if "laba_normalisasi" in o:
        b.append("Laba setelah penyesuaian per tahun: " + "; ".join(f"{k}: {rp(v)}" for k, v in o["laba_normalisasi"].items()))
        if o.get("biaya_sekali"):
            b.append("Biaya sekali jalan ditambahkan kembali HANYA ke tahunnya: "
                     + "; ".join(f"{k}: {rp(v)}" for k, v in o["biaya_sekali"].items()))
        b.append(f"Rata-rata {rp(o['laba_rata'])}; tahun terakhir {rp(o['laba_terakhir'])}; basis dipakai {rp(o['basis'])}")
    for m in o["metode"]:
        b.append(f"- {m['nama']}: {rp(m['rendah'])} s/d {rp(m['tinggi'])}  [{m['rumus']}]")
    r = o["rentang_bruto"]
    b.append(f"Nilai usaha 100% (sebelum utang): {rp(r[0])} s/d {rp(r[1])}")
    if o["utang"] > 0:
        if o["utang_ikut"]:
            b.append(f"Utang {rp(o['utang'])}: ikut berpindah/tetap di badan usaha, jadi dikurangkan dari nilai sebelum harga.")
        else:
            b.append(f"Utang {rp(o['utang'])}: dilunasi pemilik dari hasil jual (pembeli menerima usaha bebas utang).")
    if o["porsi"] < 100:
        b.append(f"Porsi yang berpindah: {o['porsi']}%")
    h = o["harga"]
    b.append(f"Harga yang dibayar pembeli/penerus: {rp(h[0])} s/d {rp(h[1])}")
    r = o["rentang_bersih"]
    b.append(f"Setelah biaya transaksi {o['biaya_transaksi_persen']}%: {rp(r[0])} s/d {rp(r[1])}")
    s = o["hasil_bersih_pemilik"]
    b.append(f"Hasil bersih ke pemilik (setelah biaya dan utang yang dilunasi): {rp(s[0])} s/d {rp(s[1])}")
    if "aset_bersih" in o:
        b.append(f"Aset dikurangi utang, seluruh usaha (gambaran bila usaha ditutup dan aset dijual): {rp(o['aset_bersih'])}")
    if "kebutuhan_pasca" in o:
        s = o["selisih_vs_kebutuhan"]
        b.append(f"Kebutuhan hidup setelah keluar: {rp(o['kebutuhan_pasca'])}; selisih hasil bersih ke pemilik vs kebutuhan: {rp(s[0])} s/d {rp(s[1])}")
    for p in o["peringatan"]:
        b.append("PERINGATAN: " + p)
    b.append("Catatan: kelipatan/persentase adalah ASUMSI dari pengguna, bukan angka pasar. Pajak, BPHTB, dan biaya notaris belum dihitung.")
    return "\n".join(b)


def jsonable(o):
    if isinstance(o, dict):
        return {k: jsonable(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [jsonable(v) for v in o]
    if isinstance(o, bool):
        return o
    if isinstance(o, Decimal):
        return int(o.quantize(Decimal(1), rounding=ROUND_HALF_UP))
    return o


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--laba", nargs="*", default=[], help="tahun=laba bersih, mis. 2025=180000000 (maks 3 tahun terakhir dipakai)")
    p.add_argument("--kelipatan", nargs="*", default=[], help="kelipatan laba (rendah tinggi), dari pengguna")
    p.add_argument("--ilustrasi", action="store_true", help="pakai kelipatan ilustrasi 1,5/2,5/3,5 (BUKAN angka pasar)")
    p.add_argument("--aset"); p.add_argument("--utang", default="0")
    p.add_argument("--utang-ikut", action="store_true",
                   help="utang ikut berpindah ke pembeli/tetap di badan usaha (bukan dilunasi pemilik dari hasil jual)")
    p.add_argument("--porsi", default="100", help="persen kepemilikan yang berpindah (mis. 40 untuk bagian sekutu 40%%)")
    p.add_argument("--penyesuaian-aset", default="0", help="persen potongan nilai aset (usang/susut)")
    p.add_argument("--gaji-diambil", default="0", help="gaji/ambil pribadi pemilik per tahun yang ada di biaya")
    p.add_argument("--gaji-pengganti", default="0", help="gaji manajer pengganti per tahun")
    p.add_argument("--biaya-sekali", action="extend", nargs="+", default=[],
                   help="TAHUN=JUMLAH biaya sekali jalan yang tidak berulang, mis. 2024=12000000 (boleh beberapa)")
    p.add_argument("--diskon-pemilik", default="0", help="persen potongan karena usaha bergantung pada pemilik")
    p.add_argument("--biaya-transaksi", default="0", help="persen biaya (notaris, perantara, dll.)")
    p.add_argument("--kebutuhan-bulanan"); p.add_argument("--bulan")
    p.add_argument("--json", action="store_true")
    try:
        a = p.parse_args(argv)
        laba = parse_laba(a.laba)
        if a.biaya_sekali and not laba:
            raise ValueError("--biaya-sekali butuh --laba")
        biaya_sekali = parse_biaya_sekali(a.biaya_sekali, laba)
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
        porsi = persen(a.porsi, "porsi")
        if porsi == 0:
            raise ValueError("porsi harus lebih dari 0")
        o = hitung(
            laba, kel,
            aset=non_negatif(a.aset, "aset") if a.aset is not None else None,
            utang=non_negatif(a.utang, "utang"),
            diskon_aset=persen(a.penyesuaian_aset, "penyesuaian aset"),
            gaji_diambil=non_negatif(a.gaji_diambil, "gaji diambil"),
            gaji_pengganti=non_negatif(a.gaji_pengganti, "gaji pengganti"),
            biaya_sekali=biaya_sekali,
            diskon_pemilik=persen(a.diskon_pemilik, "diskon pemilik"),
            biaya_transaksi=persen(a.biaya_transaksi, "biaya transaksi"),
            kebutuhan_bulanan=non_negatif(a.kebutuhan_bulanan, "kebutuhan") if a.kebutuhan_bulanan is not None else None,
            bulan=non_negatif(a.bulan, "bulan") if a.bulan is not None else None,
            porsi=porsi, utang_ikut=a.utang_ikut,
        )
    except ValueError as e:
        print(f"GAGAL: {e}", file=sys.stderr)
        return 2
    except ArithmeticError as e:  # termasuk decimal.InvalidOperation pada angka ekstrem
        print(f"GAGAL: angka tidak bisa dihitung ({e.__class__.__name__}); cek salah ketik", file=sys.stderr)
        return 2
    except SystemExit as e:
        return e.code if isinstance(e.code, int) else 2
    print(json.dumps(jsonable(o), ensure_ascii=False, indent=1) if a.json else tampil(o))
    return 0


if __name__ == "__main__":
    sys.exit(main())
