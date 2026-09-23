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


# Ketentuan KUR menurut teks Permenko Perekonomian No. 1 Tahun 2026 (berlaku 13 Jan 2026).
# Dicek 2026-09-23; lihat references/regulasi.md. Bunga efektif per tahun; tenor dalam bulan.
DASAR_KUR = "Permenko Perekonomian No. 1 Tahun 2026 (berlaku 13 Januari 2026)"
ATURAN_KUR = {
    "super-mikro": {"min": 0, "maks": 10_000_000, "pasal_plafon": "Pasal 29",
                    "tenor": {"modal-kerja": 36, "investasi": 60}, "pasal_tenor": "Pasal 31"},
    "mikro": {"min": 10_000_000, "maks": 100_000_000, "pasal_plafon": "Pasal 36",
              "tenor": {"modal-kerja": 36, "investasi": 60}, "pasal_tenor": "Pasal 38"},
    "kecil": {"min": 100_000_000, "maks": 500_000_000, "pasal_plafon": "Pasal 43",
              "tenor": {"modal-kerja": 48, "investasi": 60}, "pasal_tenor": "Pasal 45"},
}


def jenis_dari_plafon(P):
    if P <= 10_000_000:
        return "super-mikro"
    if P <= 100_000_000:
        return "mikro"
    if P <= 500_000_000:
        return "kecil"
    return None


def bunga_acuan_kur(jenis, sektor, akad):
    """Kembalikan (bunga % atau None, pasal, catatan)."""
    if jenis == "super-mikro":
        return Decimal(3), "Pasal 30", None
    pasal = "Pasal 37" if jenis == "mikro" else "Pasal 44"
    if sektor is None:
        return None, pasal, "sektor belum diisi (--sektor produksi / perdagangan-ekspor / perdagangan)"
    if sektor in ("produksi", "perdagangan-ekspor"):
        return Decimal(6), pasal, None
    tangga = {1: 6, 2: 7} if jenis == "mikro" else {1: 6, 2: 7, 3: 8, 4: 9}
    if akad in tangga:
        return Decimal(tangga[akad]), pasal, None
    if jenis == "mikro":
        return None, "Pasal 36 ayat (3)", ("KUR mikro sektor perdagangan non-ekspor paling banyak 2 kali akad — "
                                            "akad ke-%d tidak tersedia" % akad)
    return None, pasal, "bunga untuk akad ke-%d KUR kecil perdagangan non-ekspor tidak diatur di pasal ini — tanyakan bank" % akad


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
    p.add_argument("--bunga", help="Suku bunga PER TAHUN dalam persen, mis. 6 atau '6,5%%'. Boleh kosong bila "
                   "--kur dipakai dan jenis/sektor KUR diketahui (bunga acuan Permenko 1/2026)")
    p.add_argument("--bunga-contoh", action="store_true",
                   help="Tandai bunga sebagai ANGKA CONTOH (belum dari bank) — akan diberi label di output")
    p.add_argument("--tenor", required=True, type=int, help="Jangka waktu dalam BULAN, mis. 36")
    p.add_argument("--kur", action="store_true", help="Cek plafon, bunga acuan, tenor, NPWP & agunan terhadap Permenko 1/2026")
    p.add_argument("--jenis-kur", choices=["super-mikro", "mikro", "kecil"], help="Default: ditebak dari plafon")
    p.add_argument("--sektor", choices=["produksi", "perdagangan-ekspor", "perdagangan"],
                   help="produksi = selain perdagangan (pertanian, industri pengolahan, jasa produksi, dll.)")
    p.add_argument("--akad-ke", type=int, default=1, help="KUR ke berapa di jenis yang sama (default 1)")
    p.add_argument("--penggunaan", choices=["modal-kerja", "investasi"], help="Untuk cek tenor maksimal")
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
    a.bunga_dari_acuan = False
    if a.akad_ke < 1:
        gagal("--akad-ke minimal 1.")
    cek_kur = None
    if a.kur or a.jenis_kur or a.sektor:
        jenis = a.jenis_kur or jenis_dari_plafon(P)
        if jenis is None:
            gagal(f"Plafon {rp(P)} di atas batas KUR kecil Rp 500.000.000 (Pasal 43 Permenko 1/2026). "
                  "Ini bukan KUR; hapus --kur untuk simulasi kredit biasa.")
        at = ATURAN_KUR[jenis]
        cek_kur = {"dasar": DASAR_KUR, "jenis": jenis, "sektor": a.sektor, "akad_ke": a.akad_ke,
                   "sesuai": [], "perhatian": []}
        if not (at["min"] < P <= at["maks"]):
            cek_kur["perhatian"].append(f"Plafon {rp(P)} di luar rentang KUR {jenis} ({rp(at['min'])} < plafon ≤ "
                                        f"{rp(at['maks'])}, {at['pasal_plafon']}).")
        else:
            cek_kur["sesuai"].append(f"Plafon masuk rentang KUR {jenis} ({at['pasal_plafon']}).")
        acuan, pasal_b, cat_b = bunga_acuan_kur(jenis, a.sektor, a.akad_ke)
        cek_kur["bunga_acuan_efektif_persen"] = float(acuan) if acuan is not None else None
        cek_kur["pasal_bunga"] = pasal_b
        if cat_b:
            cek_kur["perhatian"].append(cat_b)
    if a.bunga is None:
        if cek_kur is None or cek_kur.get("bunga_acuan_efektif_persen") is None:
            alasan = (" Catatan: " + "; ".join(cek_kur["perhatian"])) if cek_kur and cek_kur["perhatian"] else ""
            gagal("Suku bunga belum diisi. Isi --bunga (dari bank), atau pakai --kur dengan --sektor "
                  "(dan --akad-ke) agar dipakai bunga acuan Permenko 1/2026." + alasan)
        a.bunga = str(cek_kur["bunga_acuan_efektif_persen"])
        a.bunga_dari_acuan = True
        sumber_bunga = (f"ACUAN {DASAR_KUR} {cek_kur['pasal_bunga']} — efektif/tahun; konfirmasi ke bank penyalur")
    else:
        sumber_bunga = ("ANGKA CONTOH — cek bank/kur.ekon.go.id" if a.bunga_contoh else "diisi pengguna/bank")
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
    if cek_kur is not None:
        at = ATURAN_KUR[cek_kur["jenis"]]
        acuan = cek_kur.get("bunga_acuan_efektif_persen")
        if acuan is not None and float(bunga) != acuan:
            cek_kur["perhatian"].append(f"Bunga yang dipakai {float(bunga)}% berbeda dari bunga acuan KUR {acuan}% efektif/tahun "
                                        f"({cek_kur['pasal_bunga']}). Jika bank menyebut angka FLAT, bandingkan dengan "
                                        "'bunga_flat_setara' di hasil anuitas; jika lebih tinggi, tanyakan ke bank.")
        if a.penggunaan:
            tmax = at["tenor"][a.penggunaan]
            if n > tmax:
                cek_kur["perhatian"].append(f"Tenor {n} bulan melebihi batas awal {tmax} bulan untuk {a.penggunaan} "
                                            f"KUR {cek_kur['jenis']} ({at['pasal_tenor']}); perpanjangan hanya lewat ketentuan bank.")
            else:
                cek_kur["sesuai"].append(f"Tenor {n} bulan ≤ batas {tmax} bulan untuk {a.penggunaan} ({at['pasal_tenor']}).")
        else:
            cek_kur["perhatian"].append("Penggunaan belum diisi (--penggunaan modal-kerja/investasi); batas tenor: "
                                        f"modal kerja {at['tenor']['modal-kerja']} bulan, investasi {at['tenor']['investasi']} bulan "
                                        f"({at['pasal_tenor']}).")
        if cek_kur["jenis"] == "kecil" or (cek_kur["jenis"] == "mikro" and P > 50_000_000):
            cek_kur["sesuai"].append("Wajib punya NPWP (" + ("Pasal 41" if cek_kur["jenis"] == "kecil" else "Pasal 34") + ").")
        if P <= 100_000_000:
            cek_kur["sesuai"].append("Plafon ≤ Rp 100.000.000: bank TIDAK BOLEH meminta agunan tambahan (Pasal 20 ayat 1).")
        else:
            cek_kur["sesuai"].append("Plafon > Rp 100.000.000: bank boleh meminta agunan tambahan (Pasal 20 ayat 2).")
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

    if cek_kur is not None and cek_kur.get("bunga_acuan_efektif_persen") is not None:
        acuan = Decimal(str(cek_kur["bunga_acuan_efektif_persen"]))
        ja = jadwal_anuitas(P, acuan, n)
        flat_setara = Decimal(sum(x["bunga"] for x in ja)) / P / n * 12 * 100
        cek_kur["bunga_flat_setara_acuan_persen"] = float(round(flat_setara, 2))
        cek_kur["cicilan_anuitas_pada_bunga_acuan"] = ja[0]["cicilan"]
        if "flat" in hasil_metode:
            ef = efektif_setara(P, Decimal(hasil_metode["flat"]["cicilan_per_bulan"]), n)
            if ef > acuan + Decimal("0.05"):
                teks = (f"Bunga KUR diatur {float(acuan)}% EFEKTIF/tahun ({cek_kur['pasal_bunga']}); untuk tenor {n} bulan, "
                        f"bunga FLAT yang setara hanya ±{float(round(flat_setara, 2))}%/tahun. ")
                if a.bunga_dari_acuan:
                    teks += (f"Kolom FLAT pada simulasi ini hanya ILUSTRASI bila angka {float(bunga)}% dihitung flat "
                             f"(setara efektif ±{float(round(ef, 2))}%) — yang berlaku untuk KUR adalah kolom ANUITAS/efektif.")
                else:
                    teks += (f"Hitungan flat {float(bunga)}% setara efektif ±{float(round(ef, 2))}% — bila bank menawarkan "
                             f"flat {float(bunga)}% untuk KUR, minta penjelasan dan tabel angsuran resmi.")
                cek_kur["perhatian"].append(teks)

    out = {
        "input": {"plafon": P, "bunga_per_tahun_persen": float(bunga),
                  "sumber_bunga": sumber_bunga,
                  "tenor_bulan": n, "tenor_tahun": round(n / 12, 2)},
        "hasil": hasil_metode,
        "rencana_penggunaan_dana": rincian,
        "cek_ketentuan_kur": cek_kur,
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
    if cek_kur:
        print(f"\nCek ketentuan KUR {cek_kur['jenis']} ({cek_kur['dasar']}):")
        for x in cek_kur["sesuai"]:
            print("  ✔ " + x)
        for x in cek_kur["perhatian"]:
            print("  ⚠ " + x)
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
