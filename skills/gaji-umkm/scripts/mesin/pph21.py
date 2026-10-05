#!/usr/bin/env python3
"""Kalkulator PPh Pasal 21 metode TER (PP 58/2023, PMK 168/2023) untuk pemberi kerja Indonesia.

Subperintah:
  bulan    PPh 21 satu bulan (masa selain Masa Pajak Terakhir) = TER bulanan x bruto sebulan.
  setahun  Tabel Januari–Desember (atau sebagian tahun) + hitung ulang Masa Pajak Terakhir
           (Desember / bulan berhenti bekerja) dengan tarif Pasal 17.
  harian   Pegawai tidak tetap yang dibayar harian/borongan/satuan (TER harian atau Pasal 17 x 50%).
  tabel    Tampilkan tabel TER (A, B, C, harian) dari ter_tabel.json.

Contoh:
  python3 pph21.py bulan --ptkp K/0 --bruto 10jt
  python3 pph21.py bulan --ptkp TK/0 --bruto 6jt --dtp
  python3 pph21.py setahun --ptkp K/0 --gaji 10jt --iuran 100rb
  python3 pph21.py setahun --ptkp TK/0 --gaji 17,5jt --iuran 100rb --akhir 8 --status berhenti
  python3 pph21.py setahun --ptkp K/1 --data gaji.csv --dtp --format json
  python3 pph21.py harian --upah 500rb --hari 20
  python3 pph21.py harian --total 15jt --hari 5

Hanya library standar Python 3.8+. Tidak ada akses jaringan. Keluar dengan kode 2 bila input salah.
"""
import argparse
import csv
import io
import json
import sys
from decimal import Decimal

import ter_core as tc

ALIAS_BULAN = {
    "jan": 1, "feb": 2, "peb": 2, "mar": 3, "apr": 4, "mei": 5, "may": 5, "jun": 6, "jul": 7,
    "agu": 8, "agt": 8, "ags": 8, "aug": 8, "sep": 9, "okt": 10, "oct": 10, "nov": 11, "nop": 11,
    "des": 12, "dec": 12,
}


class InputError(Exception):
    pass


def parse_bulan(teks):
    s = str(teks).strip().lower()
    if s.isdigit() and 1 <= int(s) <= 12:
        return int(s)
    for alias, no in ALIAS_BULAN.items():
        if s.startswith(alias):
            return no
    raise InputError("Bulan '{}' tidak dikenali (pakai 1–12 atau nama bulan)".format(teks))


def angka(nilai, nama, boleh_negatif=False):
    try:
        return tc.parse_angka(nilai, nama, boleh_negatif=boleh_negatif)
    except ValueError as e:
        raise InputError(str(e))


def ke_json(obj):
    if isinstance(obj, Decimal):
        return tc.angka_json(obj)
    if isinstance(obj, dict):
        return {k: ke_json(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [ke_json(v) for v in obj]
    return obj


# ---------------------------------------------------------------- bulan
def cmd_bulan(args):
    ptkp = tc.normalisasi_ptkp(args.ptkp)
    kat = tc.kategori_ter(ptkp)
    bruto = angka(args.bruto, "--bruto")
    tarif, bawah, atas = tc.tarif_ter_bulanan(bruto, kat)
    pph = tc.bulat_bawah(bruto * tarif / 100)
    premi = angka(args.premi_perusahaan, "--premi-perusahaan") if args.premi_perusahaan else Decimal(0)
    potongan = angka(args.potongan_lain, "--potongan-lain") if args.potongan_lain else Decimal(0)
    if premi > bruto:
        raise InputError("--premi-perusahaan ({}) lebih besar dari --bruto ({})".format(
            tc.format_rp(premi), tc.format_rp(bruto)))
    peringatan = []
    dtp_ok = False
    if args.dtp:
        dasar = angka(args.bruto_tetap, "--bruto-tetap") if args.bruto_tetap else bruto - premi
        ok, alasan = tc.cek_syarat_dtp(args.tahun, dasar)
        if ok:
            dtp_ok = True
            if not args.bruto_tetap:
                peringatan.append("Syarat DTP (maks Rp 10.000.000) dicek memakai bruto bulan ini {} karena "
                                  "--bruto-tetap tidak diisi. Syarat resmi memakai gaji + tunjangan tetap & teratur "
                                  "bulan Januari 2026 (atau bulan pertama kerja) — pastikan angkanya sama."
                                  .format(tc.format_rp(dasar)))
        else:
            peringatan.append("Tidak memenuhi syarat PPh 21 DTP: {}. PPh 21 dipotong normal.".format(alasan))
    # PMK 105/2025 Pasal 2 ayat 1 & Pasal 5 ayat 1/5, Lampiran B: PPh 21 tetap DIPOTONG, lalu PPh 21 DTP
    # dibayarkan tunai -> bersihnya pegawai menerima bruto; bagian DTP tidak disetor (setoran Rp 0).
    dipotong = pph
    dtp = pph if dtp_ok else Decimal(0)
    setor = dipotong - dtp
    diterima = bruto - premi - dipotong - potongan + dtp
    catatan = [
        "Berlaku untuk masa Januari–November (dan setiap bulan pegawai tidak tetap yang dibayar bulanan). "
        "Desember atau bulan berhenti bekerja wajib dihitung ulang: pakai subperintah 'setahun'.",
        "Bruto = seluruh penghasilan bulan itu: gaji, tunjangan, lembur, bonus/THR yang dibayar bulan itu, "
        "plus premi JKK, JKM, dan BPJS Kesehatan bagian perusahaan.",
        "Uang diterima pegawai = bruto − premi bagian perusahaan (--premi-perusahaan) − PPh 21 dipotong − "
        "potongan lain (--potongan-lain, mis. iuran BPJS bagian karyawan) + PPh 21 DTP tunai (bila DTP). Rincian slip gaji "
        "lengkap: skill slip-gaji-bpjs.",
        tc.CATATAN_PEMBULATAN,
    ]
    if dtp_ok:
        catatan.insert(0, "PPh 21 DTP (PMK 105/2025 Pasal 2 ayat 1, Pasal 5, Lampiran B): PPh 21 tetap DIPOTONG "
                          "seperti biasa, lalu nilai yang sama WAJIB dibayarkan TUNAI kembali ke pegawai bersama gaji "
                          "(bukan penghasilan kena pajak). Hasil bersihnya pegawai menerima gaji tanpa berkurang pajak "
                          "— BUKAN gaji + DTP. Bagian DTP tidak disetor ke negara (setoran Rp 0), tetapi tetap dibuat "
                          "bukti potong dan dilaporkan di SPT Masa PPh 21/26 paling lambat 31 Januari 2027 "
                          "(lewat batas itu insentif gugur dan PPh yang dipotong wajib disetor — Pasal 6 ayat 5–6). "
                          "Sektor/KLU harus sudah dikonfirmasi (Lampiran A PMK 105/2025).")
    return {
        "jenis": "bulan",
        "ptkp": ptkp,
        "kategori": kat,
        "bruto": bruto,
        "tarif_ter_persen": tarif,
        "rentang_baris": {"di_atas": bawah, "sampai_dengan": atas},
        "pph21": pph,
        "dtp": dtp_ok,
        "pph21_dipotong_dari_gaji": dipotong,
        "pph21_dtp_dibayar_tunai": dtp,
        "pph21_disetor_ke_negara": setor,
        "premi_perusahaan": premi,
        "potongan_lain": potongan,
        "diterima_pegawai": diterima,
        "peringatan": peringatan,
        "catatan": catatan,
    }


def teks_bulan(h):
    atas = h["rentang_baris"]["sampai_dengan"]
    bawah = h["rentang_baris"]["di_atas"]
    if bawah == 0:
        rentang = "s.d. {}".format(tc.format_rp(atas))
    elif atas is None:
        rentang = "di atas {}".format(tc.format_rp(bawah))
    else:
        rentang = "di atas {} s.d. {}".format(tc.format_rp(bawah), tc.format_rp(atas))
    baris = [
        "**PPh 21 bulanan (metode TER)**",
        "- Status PTKP: {} → TER kategori {}".format(h["ptkp"], h["kategori"]),
        "- Penghasilan bruto sebulan: {}".format(tc.format_rp(h["bruto"], desimal=True)),
        "- Baris tabel: {} → tarif {}".format(rentang, tc.format_persen(h["tarif_ter_persen"])),
    ]
    if h["dtp"]:
        baris += [
            "- PPh 21 terutang: {}".format(tc.format_rp(h["pph21"])),
            "- **PPh 21 dipotong dari gaji: {}**".format(tc.format_rp(h["pph21_dipotong_dari_gaji"])),
            "- **PPh 21 DTP yang WAJIB dibayar tunai ke pegawai bersama gaji: {}** (PMK 105/2025 Pasal 5)".format(
                tc.format_rp(h["pph21_dtp_dibayar_tunai"])),
            "- **Setoran PPh 21 ke negara untuk pegawai ini: {}** (bagian DTP tidak disetor; tetap dibuat bukti "
            "potong & dilaporkan di SPT Masa)".format(tc.format_rp(h["pph21_disetor_ke_negara"])),
        ]
    else:
        baris.append("- **PPh 21 dipotong: {}**".format(tc.format_rp(h["pph21"])))
        baris.append("- PPh 21 disetor ke negara: {}".format(tc.format_rp(h["pph21_disetor_ke_negara"])))
    rumus = [tc.format_rp(h["bruto"], desimal=True)]
    if h["premi_perusahaan"]:
        rumus.append("− {} (premi bagian perusahaan, tidak dibayar ke pegawai)".format(
            tc.format_rp(h["premi_perusahaan"], True)))
    rumus.append("− {} (PPh 21 dipotong)".format(tc.format_rp(h["pph21_dipotong_dari_gaji"])))
    if h["potongan_lain"]:
        rumus.append("− {} (potongan lain)".format(tc.format_rp(h["potongan_lain"], True)))
    if h["dtp"]:
        rumus.append("+ {} (PPh 21 DTP tunai)".format(tc.format_rp(h["pph21_dtp_dibayar_tunai"])))
    baris.append("- **Uang yang diterima pegawai{}: {}** = {}".format(
        "" if h["potongan_lain"] else " (sebelum potongan lain seperti iuran BPJS karyawan)",
        tc.format_rp(h["diterima_pegawai"], True), " ".join(rumus)))
    baris += [
        "",
        "Cara hitung: {} × {} = {} (dibulatkan ke bawah ke rupiah penuh).".format(
            tc.format_persen(h["tarif_ter_persen"]), tc.format_rp(h["bruto"], desimal=True),
            tc.format_rp(h["pph21"])),
    ]
    if h["peringatan"]:
        baris += ["", "⚠️ Peringatan:"] + ["- " + p for p in h["peringatan"]]
    baris += ["", "Catatan:"] + ["- " + c for c in h["catatan"]]
    baris += ["", "_" + tc.DISCLAIMER + "_"]
    return "\n".join(baris)


# ---------------------------------------------------------------- setahun
KOLOM_BRUTO_KOMPONEN = ["gaji", "gaji_pokok", "tunjangan", "tunjangan_tetap", "tunjangan_tidak_tetap", "lembur",
                        "bonus", "thr", "premi_jkk_jkm", "jkk", "jkm", "premi_bpjs_kesehatan", "bpjs_kesehatan",
                        "natura", "lainnya"]


def _baca_csv(path):
    try:
        with open(path, "rb") as f:
            mentah = f.read()
    except OSError as e:
        raise InputError("File '{}' tidak bisa dibaca: {}".format(path, e.strerror))
    for enc in ("utf-8-sig", "cp1252"):
        try:
            teks = mentah.decode(enc)
            break
        except UnicodeDecodeError:
            continue
    contoh = teks[:2048]
    try:
        dialek = csv.Sniffer().sniff(contoh, delimiters=",;\t")
    except csv.Error:
        dialek = csv.excel
    r = csv.DictReader(io.StringIO(teks), dialect=dialek)
    if not r.fieldnames:
        raise InputError("File CSV kosong")
    norm = {f: (f or "").strip().lower().replace(" ", "_") for f in r.fieldnames}
    baris = []
    for i, row in enumerate(r, start=2):
        d = {norm[k]: (v or "").strip() for k, v in row.items() if k is not None}
        if not any(d.values()):
            continue
        d["_baris"] = i
        baris.append(d)
    if "bulan" not in norm.values():
        raise InputError("CSV wajib punya kolom 'bulan' (ditemukan: {})".format(", ".join(r.fieldnames)))
    return baris


def _data_dari_csv(path):
    hasil = []
    for d in _baca_csv(path):
        label = "baris {}".format(d["_baris"])
        bulan = parse_bulan(d["bulan"])
        if d.get("bruto"):
            bruto = angka(d["bruto"], "{} kolom bruto".format(label))
        else:
            komponen = [k for k in KOLOM_BRUTO_KOMPONEN if d.get(k)]
            if not komponen:
                raise InputError("{}: isi kolom 'bruto' atau komponen penghasilan (gaji, tunjangan, lembur, "
                                 "bonus, thr, premi_jkk_jkm, premi_bpjs_kesehatan)".format(label))
            bruto = sum((angka(d[k], "{} kolom {}".format(label, k)) for k in komponen), Decimal(0))
        item = {
            "bulan": bulan,
            "bruto": bruto,
            "iuran": angka(d["iuran_pensiun"], label + " iuran_pensiun") if d.get("iuran_pensiun") else Decimal(0),
            "zakat": angka(d["zakat"], label + " zakat") if d.get("zakat") else Decimal(0),
            "pph_dipotong": angka(d["pph_dipotong"], label + " pph_dipotong") if d.get("pph_dipotong") else None,
            "bruto_tetap": angka(d["bruto_tetap"], label + " bruto_tetap") if d.get("bruto_tetap") else None,
        }
        hasil.append(item)
    return hasil


def _data_dari_argumen(args):
    if args.gaji is None:
        raise InputError("Isi --gaji (bruto tetap per bulan) atau --data file.csv")
    gaji = angka(args.gaji, "--gaji")
    iuran = angka(args.iuran, "--iuran") if args.iuran else Decimal(0)
    zakat = angka(args.zakat, "--zakat") if args.zakat else Decimal(0)
    if not 1 <= args.mulai <= args.akhir <= 12:
        raise InputError("--mulai dan --akhir harus 1–12 dan mulai <= akhir")
    tambahan = {}
    for t in args.tambahan or []:
        if "=" not in t:
            raise InputError("--tambahan harus berformat BULAN=NOMINAL, mis. 7=20jt atau Des=60jt")
        b, n = t.split("=", 1)
        bln = parse_bulan(b)
        tambahan[bln] = tambahan.get(bln, Decimal(0)) + angka(n, "--tambahan bulan {}".format(b))
    data = []
    for bln in range(args.mulai, args.akhir + 1):
        data.append({"bulan": bln, "bruto": gaji + tambahan.get(bln, Decimal(0)), "iuran": iuran, "zakat": zakat,
                     "pph_dipotong": None, "bruto_tetap": gaji})
    luar = [b for b in tambahan if not args.mulai <= b <= args.akhir]
    if luar:
        raise InputError("--tambahan untuk bulan {} berada di luar rentang --mulai/--akhir".format(luar))
    return data


def cmd_setahun(args):
    ptkp = tc.normalisasi_ptkp(args.ptkp)
    kat = tc.kategori_ter(ptkp)
    data = _data_dari_csv(args.data) if args.data else _data_dari_argumen(args)
    if not data:
        raise InputError("Tidak ada data bulan")
    bulan_list = [d["bulan"] for d in data]
    if len(set(bulan_list)) != len(bulan_list):
        raise InputError("Ada bulan ganda di data: {}".format(sorted(b for b in bulan_list if bulan_list.count(b) > 1)))
    data.sort(key=lambda d: d["bulan"])
    terakhir = data[-1]["bulan"]
    ada_masa_terakhir = args.status == "berhenti" or terakhir == 12
    peringatan = []
    if args.dtp and args.tahun != 2026:
        raise InputError("PPh 21 DTP PMK 105/2025 hanya untuk Masa Pajak Januari–Desember 2026")

    # syarat DTP pegawai tetap: bruto tetap & teratur bulan Jan 2026 / bulan pertama kerja <= Rp10 jt
    dtp_ok = False
    if args.dtp:
        pertama = data[0]
        dasar = pertama["bruto_tetap"] if pertama["bruto_tetap"] is not None else None
        if dasar is None:
            raise InputError("Untuk --dtp, isi kolom 'bruto_tetap' (gaji + tunjangan tetap & teratur) di CSV "
                             "atau pakai --gaji, agar syarat maks Rp10 jt bisa dicek")
        if tc.cek_dtp_bulanan(dasar):
            dtp_ok = True
        else:
            peringatan.append("Tidak memenuhi syarat PPh 21 DTP: bruto tetap & teratur bulan {} = {} (> Rp 10.000.000). "
                              "PPh 21 dipotong normal.".format(tc.NAMA_BULAN[pertama["bulan"] - 1],
                                                                tc.format_rp(dasar)))

    rows = []
    total_pph_sebelum = Decimal(0)
    for d in data:
        is_terakhir = ada_masa_terakhir and d["bulan"] == terakhir
        if is_terakhir:
            rows.append({"bulan": d["bulan"], "nama_bulan": tc.NAMA_BULAN[d["bulan"] - 1], "bruto": d["bruto"],
                         "tarif_ter_persen": None, "pph21": None, "masa_terakhir": True})
            continue
        pph, tarif = tc.pph_ter_bulanan(d["bruto"], kat)
        dipotong = d["pph_dipotong"] if d["pph_dipotong"] is not None else pph
        if d["pph_dipotong"] is not None and d["pph_dipotong"] != pph:
            peringatan.append("{}: PPh yang benar-benar dipotong ({}) berbeda dari hitungan TER ({}). Yang dipakai "
                              "untuk Masa Pajak Terakhir adalah angka yang benar-benar dipotong.".format(
                                  tc.NAMA_BULAN[d["bulan"] - 1], tc.format_rp(d["pph_dipotong"]), tc.format_rp(pph)))
        total_pph_sebelum += dipotong
        rows.append({"bulan": d["bulan"], "nama_bulan": tc.NAMA_BULAN[d["bulan"] - 1], "bruto": d["bruto"],
                     "tarif_ter_persen": tarif, "pph21_ter": pph, "pph21": dipotong, "masa_terakhir": False})

    hasil = {
        "jenis": "setahun",
        "tahun": args.tahun,
        "ptkp": ptkp,
        "kategori": kat,
        "status": args.status,
        "dtp": dtp_ok,
        "bulan": rows,
        "peringatan": peringatan,
    }

    total_bruto = sum((d["bruto"] for d in data), Decimal(0))
    total_iuran = sum((d["iuran"] for d in data), Decimal(0))
    total_zakat = sum((d["zakat"] for d in data), Decimal(0))
    n = args.jumlah_bulan or len(data)
    if ada_masa_terakhir:
        mt = tc.hitung_masa_terakhir(total_bruto, total_iuran, total_zakat, n, ptkp, total_pph_sebelum,
                                     disetahunkan=args.disetahunkan)
        rows[-1]["pph21"] = mt["pph_masa_terakhir"]
        hasil["masa_terakhir"] = mt
        hasil["nama_masa_terakhir"] = tc.NAMA_BULAN[terakhir - 1]
        total_dipotong = mt["pph_terutang"]
    else:
        hasil["masa_terakhir"] = None
        total_dipotong = total_pph_sebelum
        peringatan.append("Data berakhir di bulan {} dan status pegawai 'aktif', jadi belum ada Masa Pajak Terakhir. "
                          "Semua bulan memakai TER. Hitung ulang di Desember (atau bulan berhenti bekerja)."
                          .format(tc.NAMA_BULAN[terakhir - 1]))

    # DTP per bulan
    if dtp_ok:
        for r in rows:
            r["dtp"] = r["pph21"] if r["pph21"] > 0 else Decimal(0)
        if hasil["masa_terakhir"] and hasil["masa_terakhir"]["pph_masa_terakhir"] < 0:
            peringatan.append("Kelebihan PPh 21 DTP di Masa Pajak Terakhir ({}) TIDAK dikembalikan ke pegawai "
                              "(PMK 105/2025 Pasal 5 ayat 5).".format(
                                  tc.format_rp(-hasil["masa_terakhir"]["pph_masa_terakhir"])))

    hasil["ringkasan"] = {
        "total_bruto": total_bruto,
        "total_iuran_pensiun": total_iuran,
        "total_zakat": total_zakat,
        "jumlah_bulan": n,
        "pph21_terutang_setahun": total_dipotong,
        "pph21_dipotong_sebelum_masa_terakhir": total_pph_sebelum,
        "kelebihan_dikembalikan": (-hasil["masa_terakhir"]["pph_masa_terakhir"]
                                   if hasil["masa_terakhir"] and hasil["masa_terakhir"]["pph_masa_terakhir"] < 0
                                   and not dtp_ok else Decimal(0)),
        "total_dtp_dibayar_tunai": sum((r.get("dtp", Decimal(0)) for r in rows), Decimal(0)) if dtp_ok else Decimal(0),
        # PMK 105/2025 Pasal 6 ayat 6: PPh yang dipotong untuk bagian DTP tidak disetor selama insentif berlaku
        "pph21_disetor_ke_negara": Decimal(0) if dtp_ok else total_dipotong,
    }
    if args.disetahunkan:
        peringatan.append("Mode disetahunkan HANYA untuk pegawai yang kewajiban pajak subjektifnya mulai/berakhir "
                          "di tengah tahun (mis. WNA datang/meninggalkan Indonesia, meninggal dunia). Pegawai yang "
                          "sekadar pindah kerja TIDAK disetahunkan.")
    hasil["catatan"] = [
        "Masa Pajak Terakhir: PPh 21 = PPh setahun (tarif Pasal 17 × PKP) − PPh yang sudah dipotong bulan sebelumnya. "
        "Bila hasilnya negatif, kelebihan dikembalikan ke pegawai paling lambat akhir bulan berikutnya "
        "(kecuali PPh DTP).",
        "Bruto tiap bulan harus mencakup seluruh penghasilan: gaji, tunjangan, lembur, bonus/THR, PLUS premi JKK, JKM, "
        "dan iuran BPJS Kesehatan bagian perusahaan (PMK 168/2023 Pasal 5 ayat 3). JHT/JP bagian perusahaan tidak "
        "dimasukkan; JHT 2% + JP 1% bagian karyawan diisi sebagai iuran (pengurang).",
        "Biaya jabatan 5% dari bruto, maks Rp 500.000 × jumlah bulan bekerja (maks Rp 6.000.000 setahun).",
        "Status PTKP ditentukan keadaan awal tahun (1 Januari).",
        tc.CATATAN_PEMBULATAN,
    ]
    return hasil


def teks_setahun(h):
    dtp = h["dtp"]
    out = ["**PPh 21 {} — status {} (TER kategori {})**".format(h["tahun"], h["ptkp"], h["kategori"]), ""]
    kepala = "| Bulan | Penghasilan bruto | Tarif TER | PPh 21 dipotong |"
    garis = "|---|---:|---:|---:|"
    if dtp:
        kepala += " PPh 21 DTP (dibayar tunai) |"
        garis += "---:|"
    out += [kepala, garis]
    for r in h["bulan"]:
        tarif = "Pasal 17 (hitung ulang)" if r["masa_terakhir"] else tc.format_persen(r["tarif_ter_persen"])
        pph = r["pph21"]
        pph_teks = tc.format_rp(pph) if pph >= 0 else "({}) lebih potong".format(tc.format_rp(-pph))
        baris = "| {} | {} | {} | {} |".format(r["nama_bulan"], tc.format_rp(r["bruto"], desimal=True), tarif, pph_teks)
        if dtp:
            baris += " {} |".format(tc.format_rp(r.get("dtp", 0)))
        out.append(baris)
    rk = h["ringkasan"]
    out.append("| **Jumlah** | **{}** | | **{}** |{}".format(
        tc.format_rp(rk["total_bruto"], desimal=True), tc.format_rp(rk["pph21_terutang_setahun"]),
        " **{}** |".format(tc.format_rp(rk["total_dtp_dibayar_tunai"])) if dtp else ""))
    mt = h["masa_terakhir"]
    if mt:
        out += ["", "**Hitung ulang Masa Pajak Terakhir ({})**".format(h["nama_masa_terakhir"])]
        out.append("- Penghasilan bruto {} bulan: {}".format(rk["jumlah_bulan"], tc.format_rp(mt["total_bruto"], True)))
        out.append("- Biaya jabatan 5% (maks {}): {}".format(tc.format_rp(mt["biaya_jabatan_maks"]),
                                                          tc.format_rp(mt["biaya_jabatan"], True)))
        if mt["iuran_pensiun"]:
            out.append("- Iuran pensiun/JHT/JP dibayar pegawai: {}".format(tc.format_rp(mt["iuran_pensiun"], True)))
        if mt["zakat"]:
            out.append("- Zakat/sumbangan keagamaan wajib lewat perusahaan: {}".format(tc.format_rp(mt["zakat"], True)))
        out.append("- Penghasilan neto: {}".format(tc.format_rp(mt["neto"], True)))
        if mt["disetahunkan"]:
            out.append("- Neto disetahunkan (× 12/{}): {}".format(rk["jumlah_bulan"],
                                                                 tc.format_rp(mt["neto_disetahunkan"], True)))
        out.append("- PTKP {}: {}".format(h["ptkp"], tc.format_rp(mt["ptkp"])))
        out.append("- PKP (dibulatkan ke bawah ke ribuan): {}".format(tc.format_rp(mt["pkp"])))
        for r in mt["rincian_pasal17"]:
            out.append("  - {} × {} = {}".format(tc.format_persen(r["tarif"]), tc.format_rp(r["dasar"]),
                                                  tc.format_rp(r["pajak"], True)))
        if mt["disetahunkan"]:
            out.append("- PPh setahun penuh {} × {}/12 = {}".format(tc.format_rp(mt["pph_setahun_penuh"], True),
                                                                   rk["jumlah_bulan"], tc.format_rp(mt["pph_terutang"])))
        out.append("- PPh 21 terutang {}: {}".format("bagian tahun" if rk["jumlah_bulan"] < 12 else "setahun",
                                                    tc.format_rp(mt["pph_terutang"])))
        out.append("- Sudah dipotong bulan-bulan sebelumnya: {}".format(tc.format_rp(mt["pph_sudah_dipotong"])))
        akhir = mt["pph_masa_terakhir"]
        if akhir >= 0:
            out.append("- **PPh 21 dipotong di {}: {}**".format(h["nama_masa_terakhir"], tc.format_rp(akhir)))
        else:
            out.append("- **Lebih potong {}: {}** → {}".format(
                h["nama_masa_terakhir"], tc.format_rp(-akhir),
                "tidak dikembalikan karena PPh DTP" if dtp else
                "wajib dikembalikan ke pegawai paling lambat akhir bulan berikutnya"))
    out += ["", "**Ringkasan setahun**",
            "- Total bruto: {}".format(tc.format_rp(rk["total_bruto"], True)),
            "- Total PPh 21 {} (kredit pajak pegawai di SPT Tahunan): {}".format(
                "terutang" if mt else "dipotong s.d. bulan terakhir data", tc.format_rp(rk["pph21_terutang_setahun"]))]
    if rk["kelebihan_dikembalikan"]:
        out.append("- Kelebihan potong yang harus dikembalikan: {}".format(tc.format_rp(rk["kelebihan_dikembalikan"])))
    if dtp:
        out.append("- PPh 21 terutang setahun yang ditanggung pemerintah (hasil hitung ulang Masa Pajak Terakhir): {}".format(tc.format_rp(rk["pph21_terutang_setahun"])))
        out.append("- PPh 21 DTP yang benar-benar dibayar tunai ke pegawai (jumlah bulan yang positif): {}".format(
            tc.format_rp(rk["total_dtp_dibayar_tunai"])))
        out.append("- **Tiap bulan PPh 21 tetap DIPOTONG (kolom \"PPh 21 dipotong\"), lalu angka kolom \"PPh 21 DTP "
                   "(dibayar tunai)\" WAJIB dibayarkan tunai kembali ke pegawai bersama gaji** (PMK 105/2025 Pasal 5, "
                   "Lampiran B): uang diterima pegawai = gaji − PPh 21 dipotong + DTP tunai − potongan lain, jadi "
                   "gaji tidak berkurang karena pajak (BUKAN gaji + DTP).")
        out.append("- **Setoran PPh 21 ke negara untuk pegawai ini: {}** (bagian DTP tidak disetor; tetap dibuat bukti "
                   "potong & dilapor di SPT Masa PPh 21/26 paling lambat 31 Januari 2027).".format(
                       tc.format_rp(rk["pph21_disetor_ke_negara"])))
        if rk["total_dtp_dibayar_tunai"] != rk["pph21_terutang_setahun"]:
            out.append("  Selisih {} = kelebihan DTP yang tidak dikembalikan (PMK 105/2025 Pasal 5 ayat 5).".format(
                tc.format_rp(rk["total_dtp_dibayar_tunai"] - rk["pph21_terutang_setahun"])))
    if h["peringatan"]:
        out += ["", "⚠️ Peringatan:"] + ["- " + p for p in h["peringatan"]]
    out += ["", "Catatan:"] + ["- " + c for c in h["catatan"]]
    out += ["", "_" + tc.DISCLAIMER + "_"]
    return "\n".join(out)


# ---------------------------------------------------------------- harian
def cmd_harian(args):
    if args.hari is None or args.hari < 1:
        raise InputError("--hari wajib diisi (jumlah hari kerja, minimal 1)")
    if (args.upah is None) == (args.total is None):
        raise InputError("Isi salah satu: --upah (upah sehari) ATAU --total (total upah borongan/satuan) dengan --hari")
    if args.upah is not None:
        sehari = angka(args.upah, "--upah")
        cara = "upah harian"
        total = sehari * args.hari
    else:
        total = angka(args.total, "--total")
        sehari = total / args.hari
        cara = "rata-rata sehari (total ÷ hari kerja)"
    h = tc.pph_harian(sehari)
    total_pph = h["pph"] * args.hari
    dtp_ok = bool(args.dtp) and sehari <= tc.BATAS_DTP_HARIAN
    peringatan = []
    if args.dtp and not dtp_ok:
        peringatan.append("Tidak memenuhi syarat PPh 21 DTP: rata-rata upah sehari {} > Rp 500.000.".format(
            tc.format_rp(sehari, True)))
    return {
        "jenis": "harian",
        "cara": cara,
        "hari": args.hari,
        "bruto_total": total,
        "bruto_sehari": sehari,
        "metode": h["metode"],
        "tarif_persen": h["tarif"],
        "dasar_sehari": h["dasar"],
        "pph_sehari": h["pph"],
        "pph_total": total_pph,
        "dtp": dtp_ok,
        "peringatan": peringatan,
        "catatan": [
            "Untuk pegawai tidak tetap yang TIDAK dibayar bulanan. Yang dibayar bulanan memakai TER bulanan "
            "(subperintah 'bulan').",
            "Sampai Rp 2.500.000 sehari: TER harian (0% s.d. Rp 450.000; 0,5% di atasnya). Di atas Rp 2.500.000 "
            "sehari: tarif Pasal 17 × 50% bruto sehari.",
            "Pemotong membuat bukti potong per hari kerja (PMK 168/2023, contoh Lampiran).",
            tc.CATATAN_PEMBULATAN,
        ],
    }


def teks_harian(h):
    out = ["**PPh 21 pegawai tidak tetap (harian/borongan)**",
           "- Upah: {} untuk {} hari → dasar {}: {}".format(
               tc.format_rp(h["bruto_total"], True), h["hari"], h["cara"], tc.format_rp(h["bruto_sehari"], True))]
    if h["tarif_persen"] is not None:
        out.append("- Metode: TER harian {} × {} = {} per hari".format(
            tc.format_persen(h["tarif_persen"]), tc.format_rp(h["bruto_sehari"], True), tc.format_rp(h["pph_sehari"])))
    else:
        out.append("- Metode: di atas Rp 2.500.000 sehari → tarif Pasal 17 × 50% × {} = {} per hari".format(
            tc.format_rp(h["bruto_sehari"], True), tc.format_rp(h["pph_sehari"])))
    out.append("- **Total PPh 21 {} hari: {}**".format(h["hari"], tc.format_rp(h["pph_total"])))
    if h["dtp"]:
        out.append("- Memenuhi batas PPh 21 DTP (≤ Rp 500.000/hari) bila KLU perusahaan tercantum di PMK 105/2025: "
                   "PPh {} tetap dipotong, lalu {} dibayar tunai kembali ke pekerja → pekerja menerima upah {} "
                   "(tidak berkurang pajak); setoran ke negara Rp 0.".format(
                       tc.format_rp(h["pph_total"]), tc.format_rp(h["pph_total"]),
                       tc.format_rp(h["bruto_total"], True)))
    if h["peringatan"]:
        out += ["", "⚠️ Peringatan:"] + ["- " + p for p in h["peringatan"]]
    out += ["", "Catatan:"] + ["- " + c for c in h["catatan"]] + ["", "_" + tc.DISCLAIMER + "_"]
    return "\n".join(out)


# ---------------------------------------------------------------- tabel
def cmd_tabel(args):
    t = tc.muat_tabel()
    kategori = [args.kategori.upper()] if args.kategori else ["A", "B", "C", "harian"]
    hasil = {"jenis": "tabel", "kategori_ptkp": t["kategori_ptkp"], "tabel": {}}
    for k in kategori:
        key = "harian" if k.lower() == "harian" else k
        if key not in t:
            raise InputError("Kategori harus A, B, C, atau harian")
        hasil["tabel"][key] = [{"di_atas": b, "sampai_dengan": a, "tarif_persen": r} for b, a, r in t[key]]
    return hasil


def teks_tabel(h):
    out = []
    for k, baris in h["tabel"].items():
        judul = "TER harian (bruto sehari)" if k == "harian" else "TER bulanan kategori {} ({})".format(
            k, ", ".join(h["kategori_ptkp"][k]))
        out += ["### " + judul, "", "| Penghasilan bruto | Tarif |", "|---|---:|"]
        for i, r in enumerate(baris):
            if i == 0:
                rentang = "s.d. {}".format(tc.format_rp(r["sampai_dengan"]))
            elif r["sampai_dengan"] is None:
                rentang = "di atas {}".format(tc.format_rp(r["di_atas"]))
            else:
                rentang = "di atas {} s.d. {}".format(tc.format_rp(r["di_atas"]), tc.format_rp(r["sampai_dengan"]))
            out.append("| {} | {} |".format(rentang, tc.format_persen(r["tarif_persen"])))
        out.append("")
    return "\n".join(out).rstrip() + "\n"


# ---------------------------------------------------------------- main
def buat_parser():
    p = argparse.ArgumentParser(description="Kalkulator PPh 21 metode TER (PP 58/2023, PMK 168/2023)")
    sub = p.add_subparsers(dest="perintah")

    b = sub.add_parser("bulan", help="PPh 21 satu bulan dengan TER bulanan")
    b.add_argument("--ptkp", required=True, help="Status PTKP: TK/0, TK/1, TK/2, TK/3, K/0, K/1, K/2, K/3")
    b.add_argument("--bruto", required=True, help="Penghasilan bruto sebulan, mis. 10jt atau 'Rp 10.000.000'")
    b.add_argument("--dtp", action="store_true", help="Terapkan PPh 21 DTP PMK 105/2025 (KLU harus sudah dicek)")
    b.add_argument("--bruto-tetap", help="Gaji + tunjangan tetap & teratur Januari 2026/bulan pertama kerja "
                                         "(syarat DTP maks Rp10 jt; default: bruto bulan ini)")
    b.add_argument("--tahun", type=int, default=2026)
    b.add_argument("--premi-perusahaan", help="Premi JKK/JKM/BPJS Kesehatan bagian perusahaan yang ikut di --bruto "
                                              "(tidak dibayar ke pegawai)")
    b.add_argument("--potongan-lain", help="Potongan gaji lain, mis. iuran BPJS bagian karyawan (untuk uang diterima)")

    s = sub.add_parser("setahun", help="Tabel per bulan + hitung ulang Masa Pajak Terakhir")
    s.add_argument("--ptkp", required=True)
    s.add_argument("--data", help="CSV: bulan, bruto (atau komponen), iuran_pensiun, zakat, pph_dipotong, bruto_tetap")
    s.add_argument("--gaji", help="Bruto tetap per bulan (bila tanpa CSV)")
    s.add_argument("--iuran", help="Iuran JHT+JP/dana pensiun yang dibayar PEGAWAI per bulan")
    s.add_argument("--zakat", help="Zakat/sumbangan keagamaan wajib lewat perusahaan per bulan")
    s.add_argument("--tambahan", action="append", help="Penghasilan tidak teratur BULAN=NOMINAL (bisa diulang)")
    s.add_argument("--mulai", type=int, default=1, help="Bulan mulai bekerja di tahun ini (default 1)")
    s.add_argument("--akhir", type=int, default=12, help="Bulan terakhir data (default 12)")
    s.add_argument("--status", choices=["aktif", "berhenti"], default="aktif",
                   help="'berhenti' bila bulan terakhir data adalah bulan pegawai berhenti bekerja")
    s.add_argument("--jumlah-bulan", type=int, help="Jumlah bulan bekerja (default: banyaknya bulan di data)")
    s.add_argument("--disetahunkan", action="store_true",
                   help="Hanya bila kewajiban pajak subjektif mulai/berakhir di tengah tahun (WNA datang/pergi)")
    s.add_argument("--dtp", action="store_true", help="Terapkan PPh 21 DTP PMK 105/2025 (KLU harus sudah dicek)")
    s.add_argument("--tahun", type=int, default=2026)

    h = sub.add_parser("harian", help="Pegawai tidak tetap: harian/borongan/satuan")
    h.add_argument("--upah", help="Upah sehari")
    h.add_argument("--total", help="Total upah borongan/satuan (dibagi --hari)")
    h.add_argument("--hari", type=int, help="Jumlah hari kerja")
    h.add_argument("--dtp", action="store_true", help="Cek batas PPh 21 DTP (<= Rp500.000 sehari)")

    t = sub.add_parser("tabel", help="Tampilkan tabel TER")
    t.add_argument("--kategori", help="A, B, C, atau harian (default semua)")

    for sp in (b, s, h, t):
        sp.add_argument("--format", choices=["teks", "json"], default="teks")
    return p


def main(argv=None):
    p = buat_parser()
    args = p.parse_args(argv)
    if not args.perintah:
        p.print_help()
        return 2
    fungsi = {"bulan": (cmd_bulan, teks_bulan), "setahun": (cmd_setahun, teks_setahun),
              "harian": (cmd_harian, teks_harian), "tabel": (cmd_tabel, teks_tabel)}[args.perintah]
    try:
        hasil = fungsi[0](args)
    except (InputError, ValueError) as e:
        print("ERROR: {}".format(e), file=sys.stderr)
        return 2
    except RuntimeError as e:
        print("ERROR: {}".format(e), file=sys.stderr)
        return 3
    if args.format == "json":
        print(json.dumps(ke_json(hasil), ensure_ascii=False, indent=2))
    else:
        print(fungsi[1](hasil))
    return 0


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8")
            sys.stderr.reconfigure(encoding="utf-8")
        except (AttributeError, ValueError):
            pass
    sys.exit(main())
