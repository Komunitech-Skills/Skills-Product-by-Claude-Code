#!/usr/bin/env python3
"""Hitung anggaran marketing: pembagian per kanal, target CAC/ROAS, titik impas iklan, dan corong (funnel).

Subperintah:
  alokasi : total anggaran + daftar kanal berpersen -> Rp per kanal (per bulan & per kuartal). Ada cadangan
            eksperimen (default 10% dari total). Jumlah Rp per kanal DIJAMIN sama dengan anggaran (sisa
            pembulatan dibagi dengan metode sisa terbesar).
  target  : harga jual + HPP + biaya platform -> margin per pesanan, CAC & ROAS titik impas, CAC & ROAS target
            (untuk laba yang diinginkan), anggaran iklan maksimal dari target omzet, dan pesanan MINIMAL agar iklan balik modal (bukan perkiraan hasil).
  funnel  : target pesanan + tingkat konversi tiap tahap -> jumlah orang yang harus dijangkau di tiap tahap.

Aturan pembulatan:
- Rupiah dibulatkan ke rupiah terdekat (alokasi memakai sisa terbesar agar jumlahnya pas).
- CAC titik impas & CAC target dibulatkan KE BAWAH (tidak pernah menyarankan biaya lebih besar dari batas).
- ROAS titik impas & target dibulatkan KE ATAS 2 desimal (tidak pernah menyarankan ROAS lebih rendah dari batas).
- Jumlah orang/pesanan di funnel dibulatkan KE ATAS.
Semua hitungan memakai Decimal. Biaya platform & tarif iklan TIDAK disimpan di script: isi dari Seller Center /
dasbor iklan. Hanya library standar Python 3.8+. Tidak ada akses jaringan.

Contoh:
  python3 alokasi_anggaran.py alokasi --anggaran "Rp 6.000.000" --bulan 3 --kanal "Meta Ads=30,TikTok=25,WA=15,Konten=20,Google Maps=10"
  python3 alokasi_anggaran.py target --harga-jual 45000 --hpp 18000 --biaya-platform 8 --biaya-per-pesanan 1500 --laba-target-per-pesanan 5000
  python3 alokasi_anggaran.py funnel --target-pesanan 300 --tahap "Jangkauan>Klik=2" --tahap "Klik>Chat=20" --tahap "Chat>Pesanan=30"
Windows: pakai `python` atau `py` sebagai ganti `python3`.
"""
import argparse
import json
import re
import sys
from decimal import Decimal, InvalidOperation, ROUND_CEILING, ROUND_FLOOR, ROUND_HALF_UP

D0 = Decimal(0)
D100 = Decimal(100)
# Satu set ambang margin untuk seluruh skill: < 15% TERLALU TIPIS (jangan iklan), 15-<25% TIPIS (iklan kecil,
# hati-hati), >= 25% AMAN.
BATAS_TERLALU_TIPIS = Decimal(15)
BATAS_AMAN = Decimal(25)


class Salah(Exception):
    pass


def angka(teks, nama, minimum=None, boleh_nol=True):
    """Parse 'Rp 1.500.000', '1500000', '1.500.000,50', '12,5' -> Decimal."""
    if isinstance(teks, (int, float, Decimal)):
        s = str(teks)
    else:
        s = str(teks).strip()
    s = re.sub(r"(?i)rp\.?", "", s).replace(" ", "").replace("%", "")
    if not s:
        raise Salah(f"{nama}: kosong")
    if "," in s and "." in s:
        s = s.replace(".", "").replace(",", ".")
    elif "," in s:
        s = s.replace(",", ".")
    elif re.fullmatch(r"\d{1,3}(\.\d{3})+", s):
        s = s.replace(".", "")
    try:
        v = Decimal(s)
    except InvalidOperation:
        raise Salah(f"{nama}: '{teks}' bukan angka")
    if not v.is_finite():
        raise Salah(f"{nama}: '{teks}' bukan angka")
    if v < 0:
        raise Salah(f"{nama}: tidak boleh negatif")
    if v == 0 and not boleh_nol:
        raise Salah(f"{nama}: harus lebih dari 0")
    if minimum is not None and v < minimum:
        raise Salah(f"{nama}: minimal {minimum}")
    return v


def bulat(v):
    return int(v.quantize(Decimal(1), rounding=ROUND_HALF_UP))


def lantai(v):
    return int(v.to_integral_value(rounding=ROUND_FLOOR))


def langit(v):
    return int(v.to_integral_value(rounding=ROUND_CEILING))


def langit2(v):
    return v.quantize(Decimal("0.01"), rounding=ROUND_CEILING)


def rp(n):
    return "Rp " + f"{int(n):,}".replace(",", ".")


def bagi_pas(total, bobot):
    """Bagi total (int rupiah) menurut bobot (Decimal) dengan metode sisa terbesar. Jumlah pasti = total."""
    jml = sum(bobot)
    mentah = [Decimal(total) * b / jml for b in bobot]
    dasar = [int(m.to_integral_value(rounding=ROUND_FLOOR)) for m in mentah]
    sisa = total - sum(dasar)
    urut = sorted(range(len(bobot)), key=lambda i: (mentah[i] - dasar[i], -i), reverse=True)
    for i in urut[:sisa]:
        dasar[i] += 1
    return dasar


def hitung_alokasi(anggaran, kanal, bulan, cadangan_persen):
    total = bulat(anggaran)
    if total < 1:
        raise Salah("anggaran minimal Rp 1 setelah pembulatan")
    if not kanal:
        raise Salah("--kanal kosong: isi minimal satu kanal, contoh \"Meta Ads=40,WA=60\"")
    nama_lihat = set()
    for n, _ in kanal:
        if n.lower() in nama_lihat:
            raise Salah(f"kanal '{n}' muncul dua kali")
        nama_lihat.add(n.lower())
    jumlah_persen = sum(p for _, p in kanal)
    if jumlah_persen != D100:
        raise Salah(f"persen kanal harus total 100 (sekarang {jumlah_persen}). Selisih {D100 - jumlah_persen}")
    cad = bulat(Decimal(total) * cadangan_persen / D100) if cadangan_persen else 0
    if cadangan_persen and total and cad == 0:
        cad = 0
    utama = total - cad
    bagian = bagi_pas(utama, [p for _, p in kanal])
    baris = []
    for (n, p), b in zip(kanal, bagian):
        baris.append({"kanal": n, "persen_dari_dana_kanal": str(p), "rupiah_total": b,
                      "rupiah_per_bulan": bulat(Decimal(b) / bulan),
                      "persen_dari_total": str((Decimal(b) * D100 / Decimal(total)).quantize(Decimal("0.1"), rounding=ROUND_HALF_UP)) if total else "0"})
    hasil = {"anggaran_total": total, "jumlah_bulan": bulan, "cadangan_eksperimen": cad,
             "cadangan_persen": str(cadangan_persen), "dana_untuk_kanal": utama, "kanal": baris,
             "cek_jumlah": sum(bagian) + cad == total}
    return hasil


def hitung_target(a):
    harga = a["harga_jual"]
    biaya_pl = harga * a["biaya_platform"] / D100
    margin = harga - a["hpp"] - biaya_pl - a["biaya_per_pesanan"]
    h = {"harga_jual": bulat(harga), "hpp": bulat(a["hpp"]), "biaya_platform_rp": bulat(biaya_pl),
         "biaya_per_pesanan": bulat(a["biaya_per_pesanan"]), "margin_kontribusi_per_pesanan": bulat(margin),
         "margin_persen": str((margin * D100 / harga).quantize(Decimal("0.1"), rounding=ROUND_HALF_UP))}
    if margin <= 0:
        h["status"] = "RUGI"
        h["catatan"] = ("Margin per pesanan sudah nol/negatif SEBELUM biaya iklan: iklan pasti menambah kerugian. "
                        "Naikkan harga / turunkan HPP dulu.")
        return h
    ulang = a["pembelian_ulang"]
    nilai = margin * (Decimal(1) + ulang)  # margin dari pesanan pertama + pembelian ulang rata-rata
    h["pembelian_ulang_rata_rata"] = str(ulang)
    h["margin_per_pelanggan_seumur_pakai"] = bulat(nilai)
    h["cac_impas_pesanan_pertama"] = lantai(margin)
    h["roas_impas_pesanan_pertama"] = str(langit2(harga / margin))
    if ulang > 0:
        h["cac_impas_dengan_pembelian_ulang"] = lantai(nilai)
    laba = a["laba_target"]
    if laba is not None:
        sisa = margin - laba
        if sisa <= 0:
            h["status"] = "TARGET LABA TIDAK MUNGKIN"
            h["catatan"] = f"Laba target per pesanan ({rp(bulat(laba))}) >= margin ({rp(bulat(margin))}); tidak ada ruang untuk iklan."
            return h
        h["laba_target_per_pesanan"] = bulat(laba)
        h["cac_target"] = lantai(sisa)
        h["roas_target"] = str(langit2(harga / sisa))
    cac_pakai = Decimal(h.get("cac_target", h["cac_impas_pesanan_pertama"]))
    if cac_pakai == 0:
        h["status"] = "TIPIS"
        h["catatan"] = "Margin per pesanan terlalu kecil (CAC batas < Rp 1)."
        return h
    mp = margin * D100 / harga
    if mp < BATAS_TERLALU_TIPIS:
        h["status"] = "TERLALU TIPIS"
        h["catatan"] = (f"Margin di bawah {BATAS_TERLALU_TIPIS}%: jangan pasang iklan berbayar dulu; perbaiki harga/HPP, "
                        "pakai kanal gratis/organik.")
    else:
        h["status"] = "AMAN" if mp >= BATAS_AMAN else "TIPIS"
    if a["anggaran_iklan"] is not None:
        pesanan = lantai(a["anggaran_iklan"] / cac_pakai)
        h["anggaran_iklan"] = bulat(a["anggaran_iklan"])
        h["pesanan_dari_iklan_bila_capai_cac"] = pesanan
        h["omzet_dari_iklan"] = bulat(harga * pesanan)
    if a["target_omzet"] is not None:
        pesanan_perlu = langit(a["target_omzet"] / harga)
        h["target_omzet"] = bulat(a["target_omzet"])
        h["pesanan_dibutuhkan"] = pesanan_perlu
        h["anggaran_iklan_maks_impas"] = bulat(Decimal(pesanan_perlu) * Decimal(h["cac_impas_pesanan_pertama"]))
        h["anggaran_iklan_maks_sesuai_target"] = bulat(Decimal(pesanan_perlu) * cac_pakai)
        h["catatan_anggaran"] = ("Kalau 'tanpa iklan' sebagian pesanan tetap datang (organik), iklan cukup menutup sisanya: "
                                 "kurangi pesanan_dibutuhkan dengan perkiraan pesanan organik.")
    return h


def hitung_funnel(target, tahap):
    if not tahap:
        raise Salah("--tahap kosong: contoh --tahap \"Klik>Chat=20\"")
    kebutuhan = [Decimal(langit(target))]
    urut = list(tahap)
    for nama, ke, persen in reversed(urut):
        kebutuhan.append(Decimal(langit(kebutuhan[-1] * D100 / persen)))
    kebutuhan.reverse()
    baris = []
    for i, (dari, ke, persen) in enumerate(urut):
        baris.append({"tahap": f"{dari} -> {ke}", "konversi_persen": str(persen), "dibutuhkan_di_awal": int(kebutuhan[i]),
                      "menghasilkan": int(kebutuhan[i + 1])})
    return {"target_pesanan": int(kebutuhan[-1]), "awal_corong": urut[0][0], "jumlah_awal_dibutuhkan": int(kebutuhan[0]),
            "tahap": baris}


def parse_kanal(daftar):
    hasil = []
    for item in daftar.split(","):
        item = item.strip()
        if not item:
            continue
        if "=" not in item:
            raise Salah(f"kanal '{item}': format harus Nama=persen")
        n, p = item.rsplit("=", 1)
        n = n.strip()
        if not n:
            raise Salah("nama kanal kosong")
        hasil.append((n, angka(p, f"persen {n}", boleh_nol=False)))
    return hasil


def parse_tahap(items):
    hasil = []
    for t in items:
        if "=" not in t or ">" not in t:
            raise Salah(f"tahap '{t}': format harus Dari>Ke=persen, contoh Klik>Chat=20")
        rute, p = t.rsplit("=", 1)
        dari, ke = [x.strip() for x in rute.split(">", 1)]
        if not dari or not ke:
            raise Salah(f"tahap '{t}': nama tahap tidak boleh kosong")
        persen = angka(p, f"konversi {rute}", boleh_nol=False)
        if persen > D100:
            raise Salah(f"konversi {rute}: tidak boleh lebih dari 100%")
        hasil.append((dari, ke, persen))
    return hasil


def cetak_alokasi(h):
    print(f"ANGGARAN {rp(h['anggaran_total'])} untuk {h['jumlah_bulan']} bulan")
    for b in h["kanal"]:
        print(f"- {b['kanal']}: {rp(b['rupiah_total'])} total ({b['persen_dari_total']}% dari anggaran), ~{rp(b['rupiah_per_bulan'])}/bulan")
    print(f"- Cadangan eksperimen ({h['cadangan_persen']}%): {rp(h['cadangan_eksperimen'])}")
    print(f"Cek: jumlah semua = anggaran ({'OK' if h['cek_jumlah'] else 'SALAH'}). Sisa pembulatan Rp diserap kanal dengan sisa terbesar.")


def cetak_target(h):
    print(f"Harga jual {rp(h['harga_jual'])} | HPP {rp(h['hpp'])} | biaya platform {rp(h['biaya_platform_rp'])} | biaya/pesanan {rp(h['biaya_per_pesanan'])}")
    print(f"Margin kontribusi per pesanan: {rp(h['margin_kontribusi_per_pesanan'])} ({h['margin_persen']}%)  STATUS: {h['status']}")
    if "catatan" in h:
        print("!! " + h["catatan"])
    for k, lbl in [("cac_impas_pesanan_pertama", "CAC titik impas (pesanan pertama)"), ("roas_impas_pesanan_pertama", "ROAS titik impas"),
                   ("cac_impas_dengan_pembelian_ulang", "CAC impas termasuk pembelian ulang"), ("cac_target", "CAC target"),
                   ("roas_target", "ROAS target"), ("pesanan_dari_iklan_bila_capai_cac", "Minimal pesanan agar balik modal iklan (bukan perkiraan)"),
                   ("omzet_dari_iklan", "Omzet minimal dari iklan (bukan perkiraan)"), ("pesanan_dibutuhkan", "Jumlah pesanan yang dibutuhkan untuk target omzet"),
                   ("anggaran_iklan_maks_impas", "Batas atas anggaran iklan, impas (hanya bila SEMUA pesanan dari iklan; bukan saran belanja)"),
                   ("anggaran_iklan_maks_sesuai_target", "Batas atas anggaran iklan, sesuai target laba (hanya bila SEMUA pesanan dari iklan; bukan saran belanja)")]:
        if k in h:
            v = h[k]
            uang = k not in ("roas_impas_pesanan_pertama", "roas_target", "pesanan_dari_iklan_bila_capai_cac", "pesanan_dibutuhkan")
            print(f"- {lbl}: {rp(v) if uang else v}")
    if "pesanan_dari_iklan_bila_capai_cac" in h:
        print("Cara baca: angka 'minimal' = syarat agar iklan tidak rugi, BUKAN perkiraan hasil iklan.")
    if "catatan_anggaran" in h:
        print(h["catatan_anggaran"])


def cetak_funnel(h):
    print(f"Target {h['target_pesanan']} pesanan -> perlu {h['jumlah_awal_dibutuhkan']} di awal corong ({h['awal_corong']})")
    for t in h["tahap"]:
        print(f"- {t['tahap']}: konversi {t['konversi_persen']}% -> butuh {t['dibutuhkan_di_awal']} untuk dapat {t['menghasilkan']}")


def main(argv=None):
    ap = argparse.ArgumentParser(description="Anggaran marketing UMKM: alokasi, target CAC/ROAS, funnel")
    sp = ap.add_subparsers(dest="cmd", required=True)
    a = sp.add_parser("alokasi")
    a.add_argument("--anggaran", required=True)
    a.add_argument("--kanal", required=True, help='"Meta Ads=30,TikTok=25,WA=45" (total 100)')
    a.add_argument("--bulan", default="3")
    a.add_argument("--cadangan-eksperimen", default="10", help="persen dari total (default 10)")
    t = sp.add_parser("target")
    t.add_argument("--harga-jual", required=True)
    t.add_argument("--hpp", required=True)
    t.add_argument("--biaya-platform", default="0", help="persen dari harga (admin+layanan+ongkir program)")
    t.add_argument("--biaya-per-pesanan", default="0", help="Rp tetap/pesanan (packing, biaya proses)")
    t.add_argument("--laba-target-per-pesanan", default=None)
    t.add_argument("--pembelian-ulang", default="0", help="rata-rata pembelian ulang per pelanggan (mis. 0,5)")
    t.add_argument("--anggaran-iklan", default=None)
    t.add_argument("--target-omzet", default=None)
    f = sp.add_parser("funnel")
    f.add_argument("--target-pesanan", required=True)
    f.add_argument("--tahap", action="append", required=True)
    for p in (a, t, f):
        p.add_argument("--format", choices=["teks", "json"], default="teks")
    args = ap.parse_args(argv)
    try:
        if args.cmd == "alokasi":
            try:
                bulan_d = angka(args.bulan, "bulan")
            except Salah:
                bulan_d = Decimal(0)
            if bulan_d != bulan_d.to_integral_value() or bulan_d < 1:
                raise Salah(f"GAGAL: bulan harus bilangan bulat minimal 1 (diterima '{args.bulan}'). Contoh: --bulan 3")
            bulan = int(bulan_d)
            cad = angka(args.cadangan_eksperimen, "cadangan eksperimen")
            if cad > 50:
                raise Salah("cadangan eksperimen maksimal 50%")
            h = hitung_alokasi(angka(args.anggaran, "anggaran", boleh_nol=False), parse_kanal(args.kanal), bulan, cad)
            out = cetak_alokasi
        elif args.cmd == "target":
            harga = angka(args.harga_jual, "harga jual", boleh_nol=False)
            pl = angka(args.biaya_platform, "biaya platform")
            if pl >= D100:
                raise Salah("biaya platform harus di bawah 100%")
            opt = lambda v, n: None if v is None else angka(v, n)
            h = hitung_target({"harga_jual": harga, "hpp": angka(args.hpp, "HPP"), "biaya_platform": pl,
                               "biaya_per_pesanan": angka(args.biaya_per_pesanan, "biaya per pesanan"),
                               "laba_target": opt(args.laba_target_per_pesanan, "laba target"),
                               "pembelian_ulang": angka(args.pembelian_ulang, "pembelian ulang"),
                               "anggaran_iklan": opt(args.anggaran_iklan, "anggaran iklan"),
                               "target_omzet": opt(args.target_omzet, "target omzet")})
            out = cetak_target
        else:
            h = hitung_funnel(angka(args.target_pesanan, "target pesanan", boleh_nol=False), parse_tahap(args.tahap))
            out = cetak_funnel
    except Salah as e:
        print("ERROR: " + str(e), file=sys.stderr)
        return 2
    except ArithmeticError:
        print("ERROR: GAGAL: angka terlalu besar atau tidak wajar; periksa kembali input.", file=sys.stderr)
        return 2
    if args.format == "json":
        print(json.dumps(h, ensure_ascii=False, indent=2))
    else:
        out(h)
    return 0


if __name__ == "__main__":
    sys.exit(main())
