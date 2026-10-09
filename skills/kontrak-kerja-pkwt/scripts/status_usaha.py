#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Hitung klasifikasi usaha (mikro/kecil/menengah/besar) dan batas bawah upah usaha mikro/kecil.
Hanya library standar Python. Hasilnya HASIL PERHITUNGAN, bukan penetapan status: konfirmasi dengan NIB/OSS.

Dasar (lihat references/dasar-hukum.md bagian 2 baris 7b dan bagian 4 baris 2):
  - PP 7/2021 Pasal 35: UMKM dikelompokkan berdasarkan MODAL USAHA ATAU HASIL PENJUALAN TAHUNAN.
      Modal usaha (tanpa tanah & bangunan tempat usaha; ayat (2)-(3), untuk pendirian/pendaftaran):
        mikro  s.d. Rp1 miliar | kecil > Rp1 M s.d. Rp5 M | menengah > Rp5 M s.d. Rp10 M | di atasnya: besar
      Hasil penjualan tahunan (ayat (4)-(5), untuk kemudahan, pelindungan & pemberdayaan;
      usaha yang sudah berjalan sebelum PP berlaku memakai kriteria ini, ayat (6)):
        mikro  s.d. Rp2 miliar | kecil > Rp2 M s.d. Rp15 M | menengah > Rp15 M s.d. Rp50 M | di atasnya: besar
  - UU 13/2003 Pasal 90B jo. UU 6/2023; PP 36/2021 Pasal 36 (tidak diubah PP 51/2023 maupun PP 49/2025):
      upah minimum dikecualikan bagi usaha mikro & kecil; upah berdasarkan kesepakatan, paling sedikit
      (a) 50% rata-rata konsumsi masyarakat DI TINGKAT PROVINSI, dan
      (b) 25% di atas garis kemiskinan DI TINGKAT PROVINSI (data BPS).
      Rumus skill: batas bawah = maks(50% x konsumsi provinsi, 125% x garis kemiskinan provinsi),
      tiap komponen dibulatkan KE ATAS ke rupiah (aman: tidak pernah di bawah batas).

Contoh:
  python3 status_usaha.py --omzet 3,5 miliar
  python3 status_usaha.py --omzet 800jt --modal 300jt --upah 3jt --provinsi "Jawa Barat" \
      --konsumsi-provinsi 1.650.000 --garis-kemiskinan-provinsi 560.000
"""
import argparse
import json
import math
import os
import re
import sys

sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hitung_pkwt import InputError, parse_rupiah as _parse_rupiah_dasar  # noqa: E402

M = 10 ** 9
BATAS_MODAL = [(1 * M, "mikro"), (5 * M, "kecil"), (10 * M, "menengah")]
BATAS_OMZET = [(2 * M, "mikro"), (15 * M, "kecil"), (50 * M, "menengah")]
TEKS_MODAL = "modal usaha (tanpa tanah & bangunan): mikro s.d. Rp1 miliar; kecil > Rp1 miliar s.d. Rp5 miliar; " \
             "menengah > Rp5 miliar s.d. Rp10 miliar (PP 7/2021 Pasal 35 ayat (3))"
TEKS_OMZET = "hasil penjualan tahunan: mikro s.d. Rp2 miliar; kecil > Rp2 miliar s.d. Rp15 miliar; " \
             "menengah > Rp15 miliar s.d. Rp50 miliar (PP 7/2021 Pasal 35 ayat (5))"
KONFIRMASI = "Ini hasil perhitungan dari angka yang Anda berikan, bukan penetapan status. " \
             "Konfirmasi dengan dokumen NIB/OSS (skala usaha tercantum di NIB) atau Dinas Koperasi & UKM."


def parse_rupiah(teks, nama):
    """Tambahan untuk omzet/modal: 'miliar'/'milyar'/'M'/'T' (triliun)."""
    if teks is None:
        return None
    s = str(teks).strip().lower().replace(" ", "")
    for akhiran, faktor in (("triliun", 10 ** 12), ("miliar", M), ("milyar", M), ("m", M)):
        if s.endswith(akhiran) and re.fullmatch(r"(rp)?[0-9.,]+", s[: -len(akhiran)] or "x"):
            angka = s[: -len(akhiran)].replace("rp", "").replace(",", ".")
            if angka.count(".") > 1:
                raise InputError("{}: '{}' membingungkan; tulis mis. 3,5 miliar".format(nama, teks))
            return int(round(float(angka) * faktor))
    return _parse_rupiah_dasar(teks, nama)


def kelas(nilai, tabel):
    for batas, nama in tabel:
        if nilai <= batas:
            return nama
    return "besar"


def fmt_rp(n):
    return "Rp{:,}".format(n).replace(",", ".")


def hitung(omzet=None, modal=None, upah=None, konsumsi=None, garis_kemiskinan=None, provinsi=None):
    om = parse_rupiah(omzet, "omzet (hasil penjualan tahunan)")
    mo = parse_rupiah(modal, "modal usaha")
    up = parse_rupiah(upah, "upah")
    ko = parse_rupiah(konsumsi, "rata-rata konsumsi provinsi")
    gk = parse_rupiah(garis_kemiskinan, "garis kemiskinan provinsi")
    if provinsi and re.match(r"\s*(kota|kab\.?|kabupaten)\b", provinsi, flags=re.I):
        raise InputError("acuan batas upah usaha mikro/kecil adalah TINGKAT PROVINSI (PP 36/2021 Pasal 36), "
                         "bukan '{}'. Isi nama provinsinya, mis. 'Jawa Barat'.".format(provinsi.strip()))
    h = {"omzet": om, "modal": mo, "kelas_omzet": None, "kelas_modal": None, "peringatan": [],
         "dasar": [TEKS_OMZET, TEKS_MODAL], "konfirmasi": KONFIRMASI}
    if om is not None:
        h["kelas_omzet"] = kelas(om, BATAS_OMZET)
    if mo is not None:
        h["kelas_modal"] = kelas(mo, BATAS_MODAL)

    umk = {k: (v in ("mikro", "kecil")) for k, v in (("omzet", h["kelas_omzet"]), ("modal", h["kelas_modal"]))
           if v is not None}
    if not umk:
        h["status"] = "belum bisa dihitung"
        h["umk"] = None
        h["peringatan"].append("Omzet setahun dan modal usaha belum diisi: JANGAN menyimpulkan status usaha. "
                               "Tulis [isi: status usaha — cek NIB/OSS] atau tanyakan omzet setahun.")
    elif len(set(umk.values())) == 1:
        h["umk"] = list(umk.values())[0]
        dasar = " & ".join("{} ({})".format(k, h["kelas_" + k]) for k in umk)
        h["status"] = ("usaha mikro/kecil" if h["umk"] else "bukan usaha mikro/kecil") + \
            " menurut hasil perhitungan " + dasar
    else:
        h["umk"] = None
        h["status"] = "TIDAK PASTI: omzet → {}, modal → {}".format(h["kelas_omzet"], h["kelas_modal"])
        h["peringatan"].append("Kriteria omzet dan modal memberi hasil berbeda. PP 7/2021 Pasal 35 ayat (4)-(5): "
                               "kemudahan & pelindungan memakai hasil penjualan tahunan; ayat (2)-(3): modal untuk "
                               "pendirian/pendaftaran. Skill tidak memutuskan — cek skala usaha di NIB/OSS.")
    if om is None and mo is not None:
        h["peringatan"].append("Hanya modal yang diisi. Usaha yang sudah berjalan juga dinilai dari hasil penjualan "
                               "tahunan (ayat (4)-(6)); tanyakan omzet setahun bila ada.")

    # batas bawah upah usaha mikro/kecil (tingkat provinsi)
    bu = {"provinsi": provinsi or None, "konsumsi": ko, "garis_kemiskinan": gk, "batas": None, "upah": up,
          "memenuhi": None}
    if ko is not None or gk is not None:
        komp = []
        if ko is not None:
            bu["batas_50_konsumsi"] = math.ceil(ko * 50 / 100)
            komp.append(bu["batas_50_konsumsi"])
        if gk is not None:
            bu["batas_125_garis_kemiskinan"] = math.ceil(gk * 125 / 100)
            komp.append(bu["batas_125_garis_kemiskinan"])
        if ko is not None and gk is not None:
            bu["batas"] = max(komp)
        else:
            bu["batas_sementara"] = max(komp)
            h["peringatan"].append("Batas bawah upah butuh KEDUA angka provinsi (rata-rata konsumsi & garis "
                                   "kemiskinan, BPS). Angka yang ada baru batas sementara.")
        acuan = bu["batas"] if bu["batas"] is not None else bu.get("batas_sementara")
        if up is not None:
            bu["memenuhi"] = up >= acuan
            if not bu["memenuhi"]:
                h["peringatan"].append("Upah {} di bawah batas bawah usaha mikro/kecil {} (PP 36/2021 Pasal 36)."
                                       .format(fmt_rp(up), fmt_rp(acuan)))
    if h["umk"] is False:
        bu["catatan"] = "Bukan usaha mikro/kecil menurut perhitungan → upah wajib ≥ UMK/UMP (angka dari pengguna)."
    h["batas_upah_umk"] = bu
    return h


def teks(h):
    b = ["STATUS USAHA (hasil perhitungan, PP 7/2021 Pasal 35)"]
    if h["omzet"] is not None:
        b.append("- Hasil penjualan tahunan {} → {}".format(fmt_rp(h["omzet"]), h["kelas_omzet"]))
    if h["modal"] is not None:
        b.append("- Modal usaha {} → {}".format(fmt_rp(h["modal"]), h["kelas_modal"]))
    b.append("- Kesimpulan perhitungan: {}".format(h["status"]))
    b.append("- " + h["konfirmasi"])
    b.append("Kriteria: " + TEKS_OMZET + "; " + TEKS_MODAL + ".")
    bu = h["batas_upah_umk"]
    b.append("")
    b.append("BATAS BAWAH UPAH USAHA MIKRO/KECIL (PP 36/2021 Pasal 36 — tingkat PROVINSI, data BPS)")
    wil = bu["provinsi"] or "[isi: nama provinsi]"
    if "batas_50_konsumsi" in bu:
        b.append("- 50% x rata-rata konsumsi provinsi {} {} = {}".format(wil, fmt_rp(bu["konsumsi"]),
                                                                       fmt_rp(bu["batas_50_konsumsi"])))
    else:
        b.append("- 50% x rata-rata konsumsi provinsi {} = [isi: angka BPS provinsi]".format(wil))
    if "batas_125_garis_kemiskinan" in bu:
        b.append("- 125% x garis kemiskinan provinsi {} {} = {}".format(
            wil, fmt_rp(bu["garis_kemiskinan"]), fmt_rp(bu["batas_125_garis_kemiskinan"])))
    else:
        b.append("- 125% x garis kemiskinan provinsi {} = [isi: angka BPS provinsi]".format(wil))
    if bu["batas"] is not None:
        b.append("- Batas bawah = yang lebih besar = {}".format(fmt_rp(bu["batas"])))
    if bu["upah"] is not None and bu["memenuhi"] is not None:
        b.append("- Upah {} → {}".format(fmt_rp(bu["upah"]), "memenuhi" if bu["memenuhi"] else "DI BAWAH batas"))
    if bu.get("catatan"):
        b.append("- " + bu["catatan"])
    if h["peringatan"]:
        b.append("")
        b.append("PERINGATAN")
        b.extend("- " + p for p in h["peringatan"])
    return "\n".join(b)


def buat_parser():
    p = argparse.ArgumentParser(description="Klasifikasi usaha (PP 7/2021 Ps. 35) & batas upah usaha mikro/kecil")
    p.add_argument("--omzet", help="hasil penjualan setahun, mis. '3,5 miliar', '800jt', 'Rp2.000.000.000'")
    p.add_argument("--modal", help="modal usaha tanpa tanah & bangunan tempat usaha")
    p.add_argument("--upah", help="upah sebulan yang direncanakan")
    p.add_argument("--provinsi", help="nama PROVINSI tempat kerja (bukan kota/kabupaten)")
    p.add_argument("--konsumsi-provinsi", help="rata-rata konsumsi per kapita sebulan provinsi (BPS)")
    p.add_argument("--garis-kemiskinan-provinsi", help="garis kemiskinan provinsi per kapita sebulan (BPS)")
    p.add_argument("--format", default="teks", choices=["teks", "json"])
    return p


def main(argv=None):
    a = buat_parser().parse_args(argv)
    try:
        h = hitung(a.omzet, a.modal, a.upah, a.konsumsi_provinsi, a.garis_kemiskinan_provinsi, a.provinsi)
    except InputError as e:
        print("ERROR: {}".format(e), file=sys.stderr)
        return 2
    print(json.dumps(h, ensure_ascii=False, indent=2) if a.format == "json" else teks(h))
    return 0


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8")
            sys.stderr.reconfigure(encoding="utf-8")
        except (ValueError, OSError):
            pass
    sys.exit(main())
