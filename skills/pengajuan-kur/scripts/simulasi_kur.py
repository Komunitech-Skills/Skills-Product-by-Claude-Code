#!/usr/bin/env python3
"""Simulasi cicilan pinjaman (KUR atau kredit usaha lain): anuitas vs flat, plus rasio kemampuan bayar.

Hanya library standar Python 3.8+. Tidak ada akses jaringan. Tidak ada suku bunga bawaan:
suku bunga WAJIB diisi (dari bank/pengguna, atau angka contoh yang diberi label jelas).

Rumus:
  Anuitas (bunga efektif, cicilan tetap):
      r = bunga_tahunan / 12 / 100
      cicilan = P x r / (1 - (1 + r)^-n)          (r = 0  ->  cicilan = P / n)
      bunga bulan k = sisa pokok x r ; pokok bulan k = cicilan - bunga bulan k
  Flat (bunga dihitung dari pokok awal sepanjang tenor):
      bunga per bulan = P x bunga_tahunan / 100 / 12
      pokok per bulan = P / n ; cicilan = pokok + bunga

Pembulatan: bunga dan pokok tiap bulan dibulatkan ke rupiah penuh terdekat (0,5 ke atas).
Selisih pembulatan ditaruh di cicilan TERAKHIR agar total pokok tepat sama dengan plafon.
Bank bisa membulatkan berbeda (mis. ke ratusan rupiah); angka final ikuti tabel angsuran resmi bank.
"""
import argparse
import csv
import json
import re
import sys
from decimal import ROUND_HALF_UP, Decimal, InvalidOperation, getcontext

getcontext().prec = 40


def gagal(pesan):
    print(json.dumps({"error": pesan}, ensure_ascii=False, indent=2), file=sys.stderr)
    sys.exit(2)


def parse_angka(teks):
    """'Rp 50.000.000' | '50jt' | '2,5 juta' | '6%' | '6,5' | '15,000.50' -> Decimal atau None."""
    if teks is None:
        return None
    s = str(teks).strip().lower().replace("%", "").strip()
    if not s:
        return None
    pengali = Decimal(1)
    m = re.search(r"(miliar|milyar|juta|jt|ribu|rb)\s*$", s)
    if m:
        pengali = Decimal({"miliar": 10**9, "milyar": 10**9, "juta": 10**6, "jt": 10**6,
                           "ribu": 1000, "rb": 1000}[m.group(1)])
        s = s[:m.start()].strip()
    s = re.sub(r"\b(rp|idr)\b\.?", "", s)
    s = re.sub(r"[,.]\s*-\s*$", "", s)
    negatif = s.startswith("-") or (s.startswith("(") and s.endswith(")"))
    s = re.sub(r"[^\d,.]", "", s).strip(".,")
    if not s:
        return None
    if "," in s and "." in s:
        s = s.replace(".", "").replace(",", ".") if s.rfind(",") > s.rfind(".") else s.replace(",", "")
    elif "," in s:
        b = s.split(",")
        s = s.replace(",", ".") if (len(b) == 2 and len(b[1]) != 3) else s.replace(",", "")
    elif "." in s:
        b = s.split(".")
        if len(b) > 2 or len(b[1]) == 3:
            s = s.replace(".", "")
    try:
        v = Decimal(s) * pengali
    except InvalidOperation:
        return None
    return -v if negatif else v


def bulat(x):
    return int(Decimal(x).quantize(Decimal(1), rounding=ROUND_HALF_UP))


def rp(n):
    return ("-" if n < 0 else "") + f"Rp {abs(int(n)):,}".replace(",", ".")


def cicilan_anuitas(P, r, n):
    if r == 0:
        return Decimal(P) / n
    return Decimal(P) * r / (1 - (1 + r) ** (-n))


def jadwal_anuitas(P, bunga_th, n):
    r = Decimal(bunga_th) / 12 / 100
    c = bulat(cicilan_anuitas(P, r, n))
    sisa, baris = P, []
    for k in range(1, n + 1):
        b = bulat(Decimal(sisa) * r)
        pokok = c - b
        if k == n or pokok > sisa:
            pokok = sisa
        sisa -= pokok
        baris.append({"bulan": k, "cicilan": pokok + b, "pokok": pokok, "bunga": b, "sisa_pokok": sisa})
    return baris


def jadwal_flat(P, bunga_th, n):
    b = bulat(Decimal(P) * Decimal(bunga_th) / 100 / 12)
    pk = bulat(Decimal(P) / n)
    sisa, baris = P, []
    for k in range(1, n + 1):
        pokok = sisa if k == n else min(pk, sisa)
        sisa -= pokok
        baris.append({"bulan": k, "cicilan": pokok + b, "pokok": pokok, "bunga": b, "sisa_pokok": sisa})
    return baris


def efektif_setara(P, cicilan, n):
    """Bunga efektif per tahun (%) yang menghasilkan cicilan anuitas = `cicilan` (bisection)."""
    if cicilan * n <= P:
        return Decimal(0)
    lo, hi = Decimal(0), Decimal("0.2")  # 0–20% per bulan
    for _ in range(200):
        mid = (lo + hi) / 2
        if cicilan_anuitas(P, mid, n) > cicilan:
            hi = mid
        else:
            lo = mid
    return (lo + hi) / 2 * 12 * 100


def plafon_maks(cicilan_maks, bunga_th, n, metode):
    """Plafon terbesar yang cicilannya <= cicilan_maks."""
    if cicilan_maks <= 0:
        return 0
    r = Decimal(bunga_th) / 12 / 100
    if metode == "anuitas":
        faktor = (Decimal(1) / n) if r == 0 else r / (1 - (1 + r) ** (-n))
    else:
        faktor = Decimal(1) / n + Decimal(bunga_th) / 100 / 12
    return int(Decimal(cicilan_maks) / faktor // 1000 * 1000)  # dibulatkan ke bawah per Rp 1.000


def kategori_rasio(rasio):
    if rasio is None:
        return None
    if rasio >= 100:
        return "TIDAK MAMPU — cicilan melebihi laba bersih"
    if rasio > 50:
        return "TERLALU BERAT"
    if rasio > 30:
        return "BERAT — perlu hati-hati"
    return "AMAN"


def main():
    p = argparse.ArgumentParser(description="Simulasi cicilan KUR/kredit usaha: anuitas vs flat + rasio kemampuan bayar")
    p.add_argument("--plafon", required=True, help="Jumlah pinjaman, mis. 'Rp 50.000.000' atau 50jt")
    p.add_argument("--bunga", required=True, help="Suku bunga PER TAHUN dalam persen, mis. 6 atau '6,5%%'")
    p.add_argument("--bunga-contoh", action="store_true",
                   help="Tandai bunga sebagai ANGKA CONTOH (belum dari bank) — akan diberi label di output")
    p.add_argument("--tenor", required=True, type=int, help="Jangka waktu dalam BULAN, mis. 36")
    p.add_argument("--metode", choices=["anuitas", "flat", "keduanya"], default="keduanya")
    p.add_argument("--laba-bersih", help="Laba bersih usaha per bulan (setelah semua biaya usaha)")
    p.add_argument("--biaya-rumah-tangga", help="Kebutuhan rumah tangga per bulan yang diambil dari laba (opsional)")
    p.add_argument("--cicilan-lain", default="0", help="Cicilan lain yang sedang berjalan per bulan (default 0)")
    p.add_argument("--target-rasio", type=float, default=30.0, help="Batas rasio aman (%%) untuk hitung plafon maksimal (default 30)")
    p.add_argument("--rincian-dana", help="Rencana penggunaan dana: 'Etalase=5jt; Bahan baku=Rp 15.000.000' "
                   "(dicek agar jumlahnya sama dengan plafon)")
    p.add_argument("--jadwal", action="store_true", help="Sertakan jadwal angsuran lengkap per bulan")
    p.add_argument("--output-csv", help="Tulis jadwal angsuran ke CSV (UTF-8 BOM)")
    p.add_argument("--pemisah", choices=[";", ","], default=";")
    p.add_argument("--format", choices=["json", "teks"], default="json")
    a = p.parse_args()

    P = parse_angka(a.plafon)
    if P is None or P <= 0:
        gagal(f"Plafon tidak terbaca atau tidak positif: '{a.plafon}'. Contoh: 'Rp 50.000.000' atau 50jt.")
    P = bulat(P)
    teks_bunga = str(a.bunga).lower()
    per_bulan = bool(re.search(r"(/|per|tiap|sebulan|\bbln\b|bulan)", teks_bunga)) and not re.search(r"tahun|thn|p\.?a", teks_bunga)
    bunga = parse_angka(re.sub(r"(per|/)?\s*(bulan|bln|tahun|thn|p\.?a\.?)|sebulan|setahun", "", teks_bunga))
    if bunga is not None and per_bulan:
        bunga = bunga * 12
    if bunga is None or bunga < 0:
        gagal(f"Suku bunga tidak terbaca: '{a.bunga}'. Isi bunga PER TAHUN dalam persen, mis. 6 atau 6,5.")
    if bunga > 60:
        gagal(f"Suku bunga {bunga}% per tahun tidak wajar. Pastikan yang diisi bunga per TAHUN (bukan per bulan "
              "dikali salah, atau nominal rupiah).")
    if not 1 <= a.tenor <= 360:
        gagal("Tenor harus 1–360 bulan (isi dalam BULAN, mis. 3 tahun = 36).")
    n = a.tenor
    lain = parse_angka(a.cicilan_lain)
    if lain is None or lain < 0:
        gagal(f"Cicilan lain tidak terbaca: '{a.cicilan_lain}'.")
    lain = bulat(lain)
    laba = None
    if a.laba_bersih:
        laba = parse_angka(a.laba_bersih)
        if laba is None:
            gagal(f"Laba bersih tidak terbaca: '{a.laba_bersih}'.")
        laba = bulat(laba)
    brt = 0
    if a.biaya_rumah_tangga:
        x = parse_angka(a.biaya_rumah_tangga)
        if x is None or x < 0:
            gagal(f"Biaya rumah tangga tidak terbaca: '{a.biaya_rumah_tangga}'.")
        brt = bulat(x)
    if not 1 <= a.target_rasio <= 100:
        gagal("--target-rasio harus 1–100 (persen).")

    peringatan = []
    if per_bulan:
        peringatan.append(f"Bunga diisi PER BULAN ({a.bunga}); dikonversi menjadi {bunga}% per tahun (x12). "
                          "Tanyakan ke bank apakah itu bunga flat atau efektif.")
    if bunga < 1 and bunga > 0:
        peringatan.append(f"Bunga {bunga}% per tahun sangat kecil — pastikan bukan bunga per BULAN.")
    if a.bunga_contoh:
        peringatan.append("Suku bunga yang dipakai adalah ANGKA CONTOH, bukan penawaran bank. Cek suku bunga KUR "
                          "terbaru di bank penyalur atau kur.ekon.go.id.")

    rincian = None
    if a.rincian_dana:
        pos = []
        for bag in re.split(r"[;\n]+", a.rincian_dana):
            if not bag.strip():
                continue
            if "=" not in bag:
                gagal(f"Rincian dana '{bag.strip()}' harus berbentuk Nama=Nominal, pisahkan dengan titik koma (;).")
            nama, nil = bag.split("=", 1)
            v = parse_angka(nil)
            if v is None or v <= 0:
                gagal(f"Nominal rincian '{nama.strip()}' tidak terbaca: '{nil.strip()}'.")
            pos.append({"pos": nama.strip(), "nominal": bulat(v)})
        tot = sum(x["nominal"] for x in pos)
        for x in pos:
            x["persen"] = float(round(Decimal(x["nominal"]) / tot * 100, 1))
        rincian = {"pos": pos, "total": tot, "plafon": P, "selisih_plafon_minus_total": P - tot,
                   "status": "SESUAI" if tot == P else ("KURANG DARI PLAFON" if tot < P else "MELEBIHI PLAFON")}
        if tot != P:
            peringatan.append(f"Total rencana penggunaan dana {rp(tot)} tidak sama dengan plafon {rp(P)} "
                              f"(selisih {rp(P - tot)}). Sesuaikan agar bank melihat rencana yang rapi.")

    metode = ["anuitas", "flat"] if a.metode == "keduanya" else [a.metode]
    hasil_metode = {}
    for m in metode:
        jd = jadwal_anuitas(P, bunga, n) if m == "anuitas" else jadwal_flat(P, bunga, n)
        total_bunga = sum(x["bunga"] for x in jd)
        total_bayar = sum(x["cicilan"] for x in jd)
        c1 = jd[0]["cicilan"]
        d = {
            "cicilan_per_bulan": c1,
            "cicilan_terakhir": jd[-1]["cicilan"],
            "total_bunga": total_bunga,
            "total_dibayar": total_bayar,
            "cek_total_pokok_sama_plafon": sum(x["pokok"] for x in jd) == P,
        }
        if m == "flat":
            d["bunga_efektif_setara_per_tahun_persen"] = float(round(efektif_setara(P, Decimal(c1), n), 2))
        else:
            d["bunga_flat_setara_per_tahun_persen"] = float(round(Decimal(total_bunga) / P / n * 12 * 100, 2))
        if laba is not None:
            dasar = laba - brt
            beban = c1 + lain
            rasio = float(round(Decimal(beban) / laba * 100, 1)) if laba > 0 else None
            d["kemampuan_bayar"] = {
                "laba_bersih_per_bulan": laba,
                "cicilan_lain": lain,
                "total_cicilan_per_bulan": beban,
                "rasio_cicilan_terhadap_laba_persen": rasio,
                "kategori": kategori_rasio(rasio) if rasio is not None else "TIDAK BISA DINILAI — laba nol/negatif",
                "sisa_laba_setelah_cicilan": laba - beban,
            }
            if brt:
                rasio2 = float(round(Decimal(beban) / dasar * 100, 1)) if dasar > 0 else None
                d["kemampuan_bayar"].update({
                    "biaya_rumah_tangga": brt,
                    "sisa_setelah_rumah_tangga_dan_cicilan": dasar - beban,
                    "rasio_terhadap_laba_setelah_rumah_tangga_persen": rasio2,
                    "kategori_setelah_rumah_tangga": (kategori_rasio(rasio2) if rasio2 is not None
                                                     else "TIDAK MAMPU — laba habis untuk rumah tangga"),
                })
            cmaks = bulat(Decimal(dasar) * Decimal(str(a.target_rasio)) / 100) - lain
            d["plafon_maks_pada_target_rasio"] = {
                "target_rasio_persen": a.target_rasio,
                "cicilan_maks_per_bulan": max(0, cmaks),
                "plafon_maks": plafon_maks(cmaks, bunga, n, m),
                "catatan": "dibulatkan ke bawah per Rp 1.000; dasar = laba bersih"
                           + (" dikurangi biaya rumah tangga" if brt else ""),
            }
        if a.jadwal or a.output_csv:
            d["jadwal"] = jd
        hasil_metode[m] = d

    out = {
        "input": {"plafon": P, "bunga_per_tahun_persen": float(bunga),
                  "sumber_bunga": "ANGKA CONTOH — cek bank/kur.ekon.go.id" if a.bunga_contoh else "diisi pengguna/bank",
                  "tenor_bulan": n, "tenor_tahun": round(n / 12, 2)},
        "hasil": hasil_metode,
        "rencana_penggunaan_dana": rincian,
        "pembulatan": "Bunga & pokok per bulan dibulatkan ke rupiah penuh (0,5 ke atas); selisih pembulatan di cicilan terakhir.",
        "peringatan": peringatan,
        "disclaimer": "Simulasi ini bukan penawaran atau jaminan persetujuan kredit. Angka final mengikuti perjanjian & "
                      "tabel angsuran resmi bank.",
    }
    if "anuitas" in hasil_metode and "flat" in hasil_metode:
        out["perbandingan"] = {
            "selisih_total_bunga_flat_minus_anuitas": hasil_metode["flat"]["total_bunga"] - hasil_metode["anuitas"]["total_bunga"],
            "penjelasan": "Pada angka bunga yang SAMA, flat lebih mahal karena bunga selalu dihitung dari pokok awal, "
                          "sedangkan anuitas/efektif menghitung bunga dari sisa pokok yang terus berkurang.",
        }
    if laba is not None and laba <= 0:
        peringatan.append("Laba bersih nol/negatif: usaha belum menghasilkan dana untuk membayar cicilan.")

    if a.output_csv:
        try:
            with open(a.output_csv, "w", encoding="utf-8-sig", newline="") as f:
                w = csv.writer(f, delimiter=a.pemisah)
                w.writerow(["Metode", "Bulan", "Cicilan", "Pokok", "Bunga", "Sisa pokok"])
                for m, d in hasil_metode.items():
                    for x in d["jadwal"]:
                        w.writerow([m, x["bulan"], x["cicilan"], x["pokok"], x["bunga"], x["sisa_pokok"]])
        except OSError as e:
            gagal(f"Gagal menulis {a.output_csv}: {e}")
        out["file_csv"] = a.output_csv
        if not a.jadwal:
            for d in hasil_metode.values():
                d.pop("jadwal", None)

    if a.format == "json":
        print(json.dumps(out, ensure_ascii=False, indent=2))
        return
    i = out["input"]
    print(f"Plafon {rp(i['plafon'])}, bunga {i['bunga_per_tahun_persen']}%/tahun ({i['sumber_bunga']}), tenor {n} bulan")
    for m, d in hasil_metode.items():
        print(f"\n[{m.upper()}] cicilan {rp(d['cicilan_per_bulan'])}/bulan (terakhir {rp(d['cicilan_terakhir'])}), "
              f"total bunga {rp(d['total_bunga'])}, total bayar {rp(d['total_dibayar'])}")
        if "bunga_efektif_setara_per_tahun_persen" in d:
            print(f"  setara bunga efektif ±{d['bunga_efektif_setara_per_tahun_persen']}%/tahun")
        kb = d.get("kemampuan_bayar")
        if kb:
            rs = kb['rasio_cicilan_terhadap_laba_persen']
            print(f"  rasio cicilan/laba {'-' if rs is None else str(rs) + '%'} → {kb['kategori']}; "
                  f"sisa laba {rp(kb['sisa_laba_setelah_cicilan'])}")
            if "kategori_setelah_rumah_tangga" in kb:
                r2 = kb['rasio_terhadap_laba_setelah_rumah_tangga_persen']
                print(f"  setelah biaya rumah tangga: rasio {'-' if r2 is None else str(r2) + '%'} → "
                      f"{kb['kategori_setelah_rumah_tangga']}; sisa {rp(kb['sisa_setelah_rumah_tangga_dan_cicilan'])}")
            pm = d["plafon_maks_pada_target_rasio"]
            print(f"  plafon maks agar rasio ≤ {pm['target_rasio_persen']}%: {rp(pm['plafon_maks'])}")
        if a.jadwal:
            for x in d["jadwal"]:
                print(f"  {x['bulan']:>3} | {rp(x['cicilan'])} | pokok {rp(x['pokok'])} | bunga {rp(x['bunga'])} | sisa {rp(x['sisa_pokok'])}")
    if rincian:
        print("\nRencana penggunaan dana:")
        for x in rincian["pos"]:
            print(f"  - {x['pos']}: {rp(x['nominal'])} ({x['persen']}%)")
        print(f"  Total {rp(rincian['total'])} → {rincian['status']}")
    if "perbandingan" in out:
        print(f"\nFlat lebih mahal {rp(out['perbandingan']['selisih_total_bunga_flat_minus_anuitas'])} total bunga.")
    for w in peringatan:
        print("! " + w)
    print(out["disclaimer"])


if __name__ == "__main__":
    main()
