#!/usr/bin/env python3
"""Skor ide usaha tertimbang + titik impas kasar.

Bagian dari skill `brainstorming-ide-usaha`. Python standar saja (tanpa paket
pihak ketiga), berjalan lintas OS (Linux/macOS: `python3`, Windows: `python`
atau `py`).

Perintah:
  skor   -- hitung skor tertimbang & peringkat dari file ide (CSV) + bobot (JSON, opsional)
  impas  -- hitung titik impas kasar (unit) dari modal awal & margin per unit
  rencana -- hitungan rupiah rencana uji 7 hari: margin bersih per unit setelah potongan
             aplikasi/marketplace, laba uji, unit untuk menutup biaya uji, target harian

Contoh:
  python3 skor_ide.py skor --ide ide.csv --bobot bobot.json
  python3 skor_ide.py skor --ide ide.csv               # tanpa bobot -> pakai default/sama rata
  python3 skor_ide.py impas --modal 5000000 --margin 15000
  python3 skor_ide.py impas --modal Rp5.000.000 --margin 15rb
  python3 skor_ide.py skor --ide -  < ide.csv            # baca CSV dari stdin, tanpa menulis file
  python3 skor_ide.py rencana --harga 25rb --modal-unit 14rb --potongan-persen 20 --biaya-uji 300rb --target 30

Format file: lihat templates/format-data-skor.md di folder skill.
"""
import argparse
import csv
import json
import math
import re
import sys
from pathlib import Path

NILAI_MIN = 1
NILAI_MAX = 5

# Bobot default resmi skill ini (dipakai otomatis kalau --bobot tidak
# diberikan DAN nama kolom kriteria di file ide sama persis dengan ini).
# Lihat SKILL.md Langkah C.5 dan templates/format-data-skor.md.
BOBOT_DEFAULT = {
    "kesesuaian_modal": 5,
    "potensi_permintaan": 4,
    "kemudahan_eksekusi": 3,
    "kecocokan_keahlian": 2,
    "potensi_margin": 4,
}

# Cegah UnicodeEncodeError kalau output di-redirect ke konsol non-UTF-8
# (mis. Command Prompt Windows lama) dan skrip mencetak emoji/simbol.
for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(errors="replace")
    except Exception:
        pass


class DataTidakValid(Exception):
    """Dilempar saat data ide/bobot/parameter impas tidak valid."""


# ---------------------------------------------------------------------------
# Pembacaan file (encoding & pemisah CSV gaya Excel Indonesia)
# ---------------------------------------------------------------------------

_STDIN_CACHE = None


def _baca_file_teks(path, label):
    global _STDIN_CACHE
    if str(path) == "-":
        # Data ide lewat stdin (heredoc/pipe) supaya agent tidak perlu menulis file.
        if _STDIN_CACHE is None:
            _STDIN_CACHE = sys.stdin.buffer.read()
        data = _STDIN_CACHE
        if not data.strip():
            raise DataTidakValid(f"data {label} dari stdin kosong")
        for enc in ("utf-8-sig", "cp1252"):
            try:
                return data.decode(enc)
            except UnicodeDecodeError:
                continue
        raise DataTidakValid(f"data {label} dari stdin bukan teks yang bisa dibaca")
    p = Path(path)
    try:
        data = p.read_bytes()
    except FileNotFoundError:
        raise DataTidakValid(f"file {label} tidak ditemukan: {path}")
    except IsADirectoryError:
        raise DataTidakValid(f"path {label} yang diberikan adalah folder, bukan file: {path}")
    except OSError as e:
        raise DataTidakValid(f"tidak bisa membaca file {label} ({path}): {e}")

    # utf-8-sig juga membuang BOM yang ditambahkan Excel ("CSV UTF-8").
    for enc in ("utf-8-sig", "cp1252"):
        try:
            return data.decode(enc)
        except UnicodeDecodeError:
            continue
    raise DataTidakValid(
        f"file {label} ({path}) tidak bisa dibaca sebagai teks — encoding tidak dikenali. "
        "Simpan ulang sebagai CSV UTF-8."
    )


def _normalisasi_nama_kolom(nama):
    """Untuk pencocokan nama kolom yang tidak peduli huruf besar/kecil, spasi,
    atau garis bawah (mis. 'Nama_Ide', 'NAMA IDE', 'nama_ide' dianggap sama)."""
    return re.sub(r"[\s_]+", "", nama.strip().casefold())


def _deteksi_pemisah(baris_pertama):
    try:
        dialect = csv.Sniffer().sniff(baris_pertama, delimiters=",;")
        return dialect.delimiter
    except csv.Error:
        # Excel Indonesia sering memakai ';' karena ',' dipakai sebagai desimal.
        return ";" if baris_pertama.count(";") > baris_pertama.count(",") else ","


def _parse_csv_ide(path):
    teks = _baca_file_teks(path, "ide")
    baris_teks = [b for b in teks.splitlines()]
    if not baris_teks:
        raise DataTidakValid("file ide kosong")
    pemisah = _deteksi_pemisah(baris_teks[0])
    baris_mentah = list(csv.reader(baris_teks, delimiter=pemisah))
    # Simpan nomor baris FISIK (posisi asli di file) sebelum baris kosong
    # dibuang, supaya pesan error selalu menunjuk baris yang benar di file
    # aslinya (bukan nomor setelah baris kosong ikut dihitung/dibuang).
    baris_bernomor = [[i + 1, b] for i, b in enumerate(baris_mentah) if b]
    if not baris_bernomor:
        raise DataTidakValid("file ide kosong")

    no_header, header_mentah = baris_bernomor[0]
    header = [h.strip() for h in header_mentah]
    if not header or header == [""]:
        raise DataTidakValid("file ide tidak punya baris header")

    data_rows = baris_bernomor[1:]
    if not data_rows:
        raise DataTidakValid("file ide kosong atau tidak punya baris data")

    # Kolom tanpa nama di ujung (koma ekor gaya Excel, mis. header
    # "nama_ide,a,b,") dibuang otomatis kalau memang kosong di semua baris
    # data. Kalau ada isinya, itu kesalahan nyata dan dilaporkan jelas.
    while header and header[-1] == "":
        posisi = len(header)
        isi_ada = any(
            len(baris) >= posisi and baris[posisi - 1].strip()
            for _, baris in data_rows
        )
        if isi_ada:
            raise DataTidakValid(
                f"baris {no_header}: kolom ke-{posisi} tidak punya nama (header kosong), tapi "
                "sebagian baris data mengisi nilai di kolom itu. Beri nama kolom, atau hapus "
                "isinya kalau memang tidak dipakai."
            )
        header = header[:-1]
        for baris_info in data_rows:
            if len(baris_info[1]) >= posisi:
                baris_info[1] = baris_info[1][: posisi - 1] + baris_info[1][posisi:]

    if not header or header == [""]:
        raise DataTidakValid("file ide tidak punya baris header")

    # Cocokkan nama kolom tanpa peduli huruf besar/kecil, spasi, atau garis
    # bawah. Header dengan dua kolom yang jadi sama setelah dinormalisasi
    # (mis. "nama_ide,a,a") ditolak, karena sebelumnya nilai kolom terakhir
    # diam-diam menimpa nilai kolom pertama tanpa peringatan.
    ternormalisasi = [_normalisasi_nama_kolom(h) for h in header]
    kelompok = {}
    for pos, (asli, norm) in enumerate(zip(header, ternormalisasi), start=1):
        kelompok.setdefault(norm, []).append((pos, asli))
    ganda = {norm: v for norm, v in kelompok.items() if len(v) > 1}
    if ganda:
        detail = "; ".join(
            ", ".join(f"{asli!r} (kolom ke-{pos})" for pos, asli in v)
            for v in ganda.values()
        )
        raise DataTidakValid(
            f"baris {no_header}: header punya nama kolom kembar (dianggap sama kalau huruf "
            f"besar/kecil, spasi, dan garis bawah diabaikan): {detail}. Ganti salah satu nama "
            "kolom supaya unik."
        )

    idx_nama_ide = next((i for i, n in enumerate(ternormalisasi) if n == "namaide"), None)
    if idx_nama_ide is None:
        raise DataTidakValid(
            "file ide wajib punya kolom 'nama_ide' "
            f"(header terbaca: {header}; pemisah kolom terdeteksi: {pemisah!r})"
        )
    header[idx_nama_ide] = "nama_ide"  # kanonis, meski aslinya mis. 'Nama_Ide'/'NAMA IDE'

    return header, data_rows, pemisah


def kolom_kriteria_dari_file(path):
    """Nama kolom kriteria (semua kolom selain nama_ide) di file ide."""
    header, _, _ = _parse_csv_ide(path)
    return [k for k in header if k != "nama_ide"]


def _parse_angka_nilai(mentah):
    s = mentah.strip()
    # Terima koma sebagai desimal (format Indonesia) selama tidak ada titik,
    # supaya "3.5" (format internasional) tidak salah diubah jadi "3.5.5".
    if "," in s and "." not in s:
        s = s.replace(",", ".")
    return float(s)


def baca_bobot(path):
    teks = _baca_file_teks(path, "bobot")
    try:
        mentah = json.loads(teks)
    except json.JSONDecodeError as e:
        raise DataTidakValid(f"file bobot bukan JSON valid: {e}")
    if not isinstance(mentah, dict) or not mentah:
        raise DataTidakValid("file bobot harus berupa objek JSON tidak kosong, mis. {\"kriteria\": 3}")

    bobot = {}
    for kunci, nilai in mentah.items():
        if isinstance(nilai, bool):
            raise DataTidakValid(f"bobot untuk '{kunci}' harus berupa angka, bukan true/false")
        try:
            angka = float(nilai)
        except (TypeError, ValueError):
            raise DataTidakValid(f"bobot untuk '{kunci}' bukan angka: {nilai!r}")
        if not math.isfinite(angka):
            raise DataTidakValid(
                f"bobot untuk '{kunci}' bukan angka wajar (nan/infinity tidak diterima): {nilai!r}"
            )
        if angka <= 0:
            raise DataTidakValid(f"bobot untuk '{kunci}' harus lebih besar dari 0 (nilai: {angka})")
        bobot[kunci] = angka
    return bobot


def baca_ide(path, kriteria):
    header, data_rows, pemisah = _parse_csv_ide(path)

    kolom_kriteria_ada = [k for k in header if k != "nama_ide"]
    hilang_di_ide = set(kriteria) - set(kolom_kriteria_ada)
    hilang_di_bobot = set(kolom_kriteria_ada) - set(kriteria)
    if hilang_di_ide:
        raise DataTidakValid(
            f"kolom kriteria di file bobot tidak ada di file ide: {sorted(hilang_di_ide)}"
        )
    if hilang_di_bobot:
        raise DataTidakValid(
            f"kolom kriteria di file ide tidak ada di file bobot: {sorted(hilang_di_bobot)}"
        )

    ide = []
    nama_terpakai = {}  # bentuk dinormalisasi (huruf kecil, spasi dirapikan) -> nomor baris
    for no, baris in data_rows:
        # `no` adalah nomor baris FISIK di file (dihitung sebelum baris kosong
        # dibuang), jadi tetap benar meski ada baris kosong di tengah file.

        # Bug utama yang diperbaiki di v1.0.1: baris dengan koma desimal tanpa
        # kutip (mis. "Ide Y,3,5,4" dengan pemisah ',') menghasilkan jumlah
        # kolom yang tidak sama dengan header. Sebelumnya csv.DictReader
        # membuang/menggeser kolom itu diam-diam (skor jadi salah tanpa
        # peringatan). Sekarang baris seperti ini DITOLAK secara eksplisit,
        # di baris mana pun (bukan cuma baris data pertama).
        if len(baris) != len(header):
            raise DataTidakValid(
                f"baris {no}: jumlah kolom ({len(baris)}) tidak sama dengan jumlah kolom header "
                f"({len(header)}, pemisah kolom yang dipakai: {pemisah!r}). Kalau ini karena koma "
                "desimal tanpa kutip (mis. 3,5), tulis pakai titik (3.5) atau beri tanda kutip "
                '("3,5").'
            )

        row_map = dict(zip(header, [c.strip() for c in baris]))
        nama = (row_map.get("nama_ide") or "").strip()
        if not nama:
            raise DataTidakValid(f"baris {no}: 'nama_ide' kosong")

        kunci_dup = " ".join(nama.split()).casefold()
        if kunci_dup in nama_terpakai:
            raise DataTidakValid(
                f"baris {no}: nama_ide '{nama}' duplikat dengan baris {nama_terpakai[kunci_dup]} "
                "(besar/kecil huruf dan spasi ganda diabaikan saat membandingkan)"
            )
        nama_terpakai[kunci_dup] = no

        skor_kriteria = {}
        for k in kriteria:
            mentah = row_map.get(k, "")
            if not mentah:
                raise DataTidakValid(f"baris {no} ('{nama}'), kolom '{k}': nilai kosong")
            try:
                angka = _parse_angka_nilai(mentah)
            except ValueError:
                raise DataTidakValid(f"baris {no} ('{nama}'), kolom '{k}': bukan angka ({mentah!r})")
            if not math.isfinite(angka):
                raise DataTidakValid(
                    f"baris {no} ('{nama}'), kolom '{k}': nilai bukan angka wajar (nan/infinity tidak diterima): {mentah!r}"
                )
            if not (NILAI_MIN <= angka <= NILAI_MAX):
                raise DataTidakValid(
                    f"baris {no} ('{nama}'), kolom '{k}': nilai {angka:g} di luar rentang {NILAI_MIN}-{NILAI_MAX}"
                )
            skor_kriteria[k] = angka
        ide.append({"nama_ide": nama, "skor_kriteria": skor_kriteria})
    return ide


def hitung_skor(ide, bobot):
    total_bobot = sum(bobot.values())
    hasil = []
    for item in ide:
        jumlah_tertimbang = sum(item["skor_kriteria"][k] * b for k, b in bobot.items())
        skor_akhir = jumlah_tertimbang / total_bobot
        hasil.append({**item, "skor_tertimbang": round(skor_akhir, 3)})
    hasil.sort(key=lambda x: x["skor_tertimbang"], reverse=True)
    for peringkat, item in enumerate(hasil, start=1):
        item["peringkat"] = peringkat
    return hasil


def deteksi_seri(hasil_terurut):
    seri = []
    i = 0
    while i < len(hasil_terurut):
        j = i
        while j + 1 < len(hasil_terurut) and hasil_terurut[j + 1]["skor_tertimbang"] == hasil_terurut[i]["skor_tertimbang"]:
            j += 1
        if j > i:
            seri.append([hasil_terurut[k]["nama_ide"] for k in range(i, j + 1)])
        i = j + 1
    return seri


def cetak_tabel_skor(hasil, bobot, sumber_bobot):
    lebar_nama = max(8, max(len(h["nama_ide"]) for h in hasil))
    header = f"{'Peringkat':<10}{'Nama Ide':<{lebar_nama + 2}}{'Skor Tertimbang':>16}"
    print(header)
    print("-" * len(header))
    for h in hasil:
        print(f"{h['peringkat']:<10}{h['nama_ide']:<{lebar_nama + 2}}{h['skor_tertimbang']:>16.3f}")

    seri = deteksi_seri(hasil)
    if seri:
        print()
        print("PERINGATAN: skor seri terdeteksi (putuskan lewat untung-rugi kualitatif, bukan asal pilih):")
        for grup in seri:
            print(f"   - {', '.join(grup)}")

    print()
    print(f"Bobot kriteria dipakai (total bobot = {sum(bobot.values()):g}; sumber: {sumber_bobot}):")
    for k, v in bobot.items():
        print(f"   - {k}: {v:g}")


def _cocokkan_bobot_default(kolom):
    """Cocokkan nama kolom kriteria di file ide dengan BOBOT_DEFAULT, tanpa
    peduli huruf besar/kecil, spasi, atau garis bawah (mis. 'Kesesuaian_Modal'
    dianggap sama dengan 'kesesuaian_modal'). Mengembalikan dict bobot dengan
    KEY memakai nama kolom ASLI di file (bukan nama default), atau None kalau
    kumpulan kolomnya tidak cocok dengan bobot default sama sekali."""
    norm_default = {_normalisasi_nama_kolom(k): v for k, v in BOBOT_DEFAULT.items()}
    norm_kolom = {_normalisasi_nama_kolom(k): k for k in kolom}
    if set(norm_kolom) != set(norm_default):
        return None
    return {norm_kolom[norm]: nilai for norm, nilai in norm_default.items()}


def cmd_skor(args):
    peringatan_bobot = None
    try:
        if args.bobot:
            bobot = baca_bobot(args.bobot)
            sumber_bobot = f"file '{args.bobot}'"
        else:
            kolom = kolom_kriteria_dari_file(args.ide)
            if not kolom:
                raise DataTidakValid("file ide tidak punya kolom kriteria selain 'nama_ide'")
            bobot_cocok = _cocokkan_bobot_default(kolom)
            if bobot_cocok is not None:
                bobot = bobot_cocok
                sumber_bobot = "default resmi skill (--bobot tidak diberikan; lihat templates/format-data-skor.md)"
            else:
                bobot = {k: 1.0 for k in kolom}
                sumber_bobot = (
                    "sama rata/semua kriteria bobot 1 (--bobot tidak diberikan dan nama kolom "
                    "tidak cocok dengan bobot default resmi)"
                )
                # Sebelumnya jatuh ke sama rata secara diam-diam (sumber cuma
                # disebut di baris terakhir keluaran, mudah terlewat). Kini
                # dicetak sebagai PERINGATAN eksplisit di ATAS keluaran.
                peringatan_bobot = (
                    "PERINGATAN: nama kolom kriteria di file ide (" + ", ".join(kolom) + ") "
                    "tidak cocok dengan bobot default resmi skill ini (" +
                    ", ".join(BOBOT_DEFAULT) + "). Semua kriteria dipakai dengan bobot SAMA "
                    "RATA — kalau ini bukan yang dimaksud, beri file --bobot, atau perbaiki "
                    "nama kolom di file ide (huruf besar/kecil, spasi, garis bawah diabaikan "
                    "saat mencocokkan)."
                )
        ide = baca_ide(args.ide, list(bobot.keys()))
    except DataTidakValid as e:
        print(f"Data tidak valid: {e}", file=sys.stderr)
        return 1

    if peringatan_bobot:
        print(peringatan_bobot)
        print()

    hasil = hitung_skor(ide, bobot)
    cetak_tabel_skor(hasil, bobot, sumber_bobot)
    return 0


# ---------------------------------------------------------------------------
# Titik impas kasar
# ---------------------------------------------------------------------------

_AKHIRAN_PENGALI = (
    ("miliar", 1_000_000_000),
    ("m", 1_000_000_000),
    ("juta", 1_000_000),
    ("jt", 1_000_000),
    ("ribu", 1_000),
    ("rb", 1_000),
)

_POLA_RIBUAN_INDONESIA = re.compile(r"-?\d{1,3}(\.\d{3})+(,\d+)?$")


def parse_rupiah(mentah):
    """Terima angka biasa (5000000), format ribuan Indonesia (5.000.000),
    dengan/tanpa 'Rp' di depan (Rp5.000.000), dan singkatan (5jt, 15rb)."""
    asli = mentah
    s = mentah.strip()
    if not s:
        raise DataTidakValid("nilai rupiah kosong")
    s = s.replace(" ", "")
    if s[:2].lower() == "rp":
        s = s[2:]
    if not s:
        raise DataTidakValid(f"nilai rupiah tidak valid: {asli!r}")

    pengali = 1
    lower = s.lower()
    for akhiran, kali in _AKHIRAN_PENGALI:
        if lower.endswith(akhiran) and len(s) > len(akhiran):
            s = s[: -len(akhiran)]
            pengali = kali
            break

    if not s:
        raise DataTidakValid(f"nilai rupiah tidak valid: {asli!r}")

    if _POLA_RIBUAN_INDONESIA.match(s):
        # format "5.000.000" atau "5.000.000,50" -> titik ribuan, koma desimal
        s = s.replace(".", "").replace(",", ".")
    elif "," in s and "." not in s:
        # format "15000,5" -> koma desimal saja
        s = s.replace(",", ".")

    try:
        angka = float(s) * pengali
    except ValueError:
        raise DataTidakValid(
            f"nilai rupiah tidak valid: {asli!r} — pakai angka biasa (5000000), format ribuan "
            "(5.000.000), 'Rp5.000.000', atau singkatan (5jt, 15rb)"
        )
    if not math.isfinite(angka):
        raise DataTidakValid(f"nilai rupiah bukan angka wajar (nan/infinity tidak diterima): {asli!r}")
    return angka


def _tipe_rupiah_cli(mentah):
    try:
        return parse_rupiah(mentah)
    except DataTidakValid as e:
        raise argparse.ArgumentTypeError(str(e))


def _tipe_persen_cli(mentah):
    s = mentah.strip().rstrip("%").replace(",", ".")
    try:
        nilai = float(s)
    except ValueError:
        raise argparse.ArgumentTypeError(f"persen tidak valid: {mentah!r} — contoh: 20 atau 20,5")
    if not math.isfinite(nilai):
        raise argparse.ArgumentTypeError(f"persen bukan angka wajar: {mentah!r}")
    return nilai


def format_rupiah(nilai):
    dibulatkan = round(nilai, 2)
    if dibulatkan == int(dibulatkan):
        angka = f"{int(dibulatkan):,}".replace(",", ".")
    else:
        mentah = f"{dibulatkan:,.2f}"
        bagian_bulat, bagian_desimal = mentah.split(".")
        bagian_bulat = bagian_bulat.replace(",", ".")
        angka = f"{bagian_bulat},{bagian_desimal}"
    return f"Rp{angka}"


def hitung_impas(modal, margin):
    if not math.isfinite(modal):
        raise DataTidakValid(f"modal awal bukan angka wajar (nan/infinity tidak diterima): {modal!r}")
    if not math.isfinite(margin):
        raise DataTidakValid(f"margin per unit bukan angka wajar (nan/infinity tidak diterima): {margin!r}")
    if modal <= 0:
        raise DataTidakValid(f"modal awal harus lebih besar dari 0 (nilai: {modal:g})")
    if margin <= 0:
        raise DataTidakValid(f"margin per unit harus lebih besar dari 0 (nilai: {margin:g})")
    if modal < 1:
        raise DataTidakValid(f"modal awal kurang dari Rp1 — masukkan dalam rupiah bulat (nilai: {modal:g})")
    if margin < 1:
        raise DataTidakValid(
            f"margin per unit kurang dari Rp1 — masukkan dalam rupiah bulat, atau pakai skill "
            f"'hitung-hpp' untuk perhitungan presisi (nilai: {margin:g})"
        )
    return math.ceil(modal / margin)


def cmd_impas(args):
    try:
        unit_impas = hitung_impas(args.modal, args.margin)
    except DataTidakValid as e:
        print(f"Data tidak valid: {e}", file=sys.stderr)
        return 1

    print(f"{'Modal awal':<19}: {format_rupiah(args.modal)}")
    print(f"{'Margin per unit':<19}: {format_rupiah(args.margin)}")
    print(f"{'Titik impas (BEP)':<19}: {unit_impas:,} unit".replace(",", "."))
    print()
    print("Catatan: ini perkiraan KASAR (modal awal / margin per unit, dibulatkan ke atas).")
    print("Tidak memperhitungkan biaya tetap bulanan berulang, pajak, atau penyusutan.")
    print("Untuk modal per unit presisi dari resep/BOM, pakai skill 'hitung-hpp'.")
    print("Catatan istilah: 'unit' di sini bisa berarti transaksi, pelanggan, atau siklus langganan — sesuaikan dengan jenis usahamu.")
    return 0


def hitung_rencana(harga, modal_unit, potongan_persen=0.0, biaya_uji=0.0, target=10, modal_awal=None):
    """Hitungan rupiah rencana uji 7 hari. Semua nominal dibulatkan ke rupiah terdekat.

    potongan_rp      = round(harga x potongan_persen / 100)    (komisi aplikasi/marketplace)
    margin_unit      = harga - potongan_rp - modal_unit          (untung bersih per unit)
    margin_persen    = margin_unit / harga x 100
    laba_uji         = target x margin_unit - biaya_uji          (bila target tercapai)
    unit_tutup_biaya = ceil(biaya_uji / margin_unit)
    unit_impas_modal = ceil(modal_awal / margin_unit)            (bila modal_awal diisi)
    ambang           = berhenti < ceil(30% target) <= perbaiki < target <= lanjut
    """
    for nama, nilai in (("harga jual", harga), ("modal per unit", modal_unit), ("biaya uji", biaya_uji)):
        if not math.isfinite(nilai):
            raise DataTidakValid(f"{nama} bukan angka wajar: {nilai!r}")
    if harga < 1:
        raise DataTidakValid(f"harga jual per unit harus minimal Rp1 (nilai: {harga:g})")
    if modal_unit < 0:
        raise DataTidakValid(f"modal per unit tidak boleh negatif (nilai: {modal_unit:g})")
    if biaya_uji < 0:
        raise DataTidakValid(f"biaya uji tidak boleh negatif (nilai: {biaya_uji:g})")
    if not (0 <= potongan_persen < 100):
        raise DataTidakValid(f"potongan aplikasi/marketplace harus 0 sampai di bawah 100 persen (nilai: {potongan_persen:g})")
    if target < 1:
        raise DataTidakValid(f"target 7 hari minimal 1 unit/pesanan (nilai: {target})")
    if modal_awal is not None and modal_awal < 0:
        raise DataTidakValid(f"modal awal tidak boleh negatif (nilai: {modal_awal:g})")

    harga, modal_unit, biaya_uji = round(harga), round(modal_unit), round(biaya_uji)
    potongan_rp = round(harga * potongan_persen / 100)
    margin = harga - potongan_rp - modal_unit
    hasil = {
        "harga": harga, "potongan_persen": potongan_persen, "potongan_rp": potongan_rp,
        "modal_unit": modal_unit, "margin_unit": margin,
        "margin_persen": round(margin * 100 / harga, 1),
        "biaya_uji": biaya_uji, "target": target,
        "omzet_target": target * harga,
        "laba_uji": target * margin - biaya_uji,
        "ambang_perbaiki": math.ceil(target * 0.3),
        "target_kumulatif": {3: math.ceil(target * 0.3), 5: math.ceil(target * 0.6), 7: target},
        "rugi_per_unit": margin <= 0,
        "unit_tutup_biaya": None, "unit_impas_modal": None, "modal_awal": None,
    }
    if margin > 0:
        hasil["unit_tutup_biaya"] = math.ceil(biaya_uji / margin) if biaya_uji else 0
        if modal_awal:
            hasil["modal_awal"] = round(modal_awal)
            hasil["unit_impas_modal"] = math.ceil(round(modal_awal) / margin)
    return hasil


def _rp(n):
    return ("-" if n < 0 else "") + format_rupiah(abs(n))


def _persen(x):
    return f"{x:g}".replace(".", ",") + "%"


def _unit(n):
    return f"{n:,}".replace(",", ".")


def cmd_rencana(args):
    try:
        r = hitung_rencana(args.harga, args.modal_unit, args.potongan_persen, args.biaya_uji,
                           args.target, args.modal)
    except DataTidakValid as e:
        print(f"Data tidak valid: {e}", file=sys.stderr)
        return 1
    w = 30
    print(f"{'Harga jual per unit':<{w}}: {format_rupiah(r['harga'])}")
    if r["potongan_persen"]:
        print(f"{'Potongan aplikasi/marketplace':<{w}}: {_persen(r['potongan_persen'])} = {format_rupiah(r['potongan_rp'])}")
    print(f"{'Modal per unit (bahan+kemasan)':<{w}}: {format_rupiah(r['modal_unit'])}")
    print(f"{'Untung bersih per unit':<{w}}: {_rp(r['margin_unit'])} ({_persen(r['margin_persen'])} dari harga)")
    if r["rugi_per_unit"]:
        print()
        print("PERINGATAN: RUGI/TIDAK UNTUNG per unit. Jangan uji dengan harga ini - naikkan harga,")
        print("turunkan modal per unit, atau pilih kanal tanpa potongan (mis. pesan langsung via WA).")
        return 0
    print(f"{'Biaya uji 7 hari':<{w}}: {format_rupiah(r['biaya_uji'])}")
    print(f"{'Target 7 hari':<{w}}: {_unit(r['target'])} unit/pesanan (omzet {format_rupiah(r['omzet_target'])})")
    print(f"{'Laba uji bila target tercapai':<{w}}: {_rp(r['laba_uji'])}")
    print(f"{'Unit untuk menutup biaya uji':<{w}}: {_unit(r['unit_tutup_biaya'])}")
    if r["unit_impas_modal"] is not None:
        print(f"{'Balik modal awal ' + format_rupiah(r['modal_awal']):<{w}}: {_unit(r['unit_impas_modal'])} unit")
    tk = r["target_kumulatif"]
    print(f"{'Target kumulatif':<{w}}: Hari 3 >= {_unit(tk[3])}, Hari 5 >= {_unit(tk[5])}, Hari 7 >= {_unit(tk[7])}")
    print(f"{'Keputusan Hari 7':<{w}}: >= {_unit(r['target'])} lanjut | {_unit(r['ambang_perbaiki'])}-{_unit(r['target'] - 1)} perbaiki & uji ulang | < {_unit(r['ambang_perbaiki'])} hentikan/ganti ide")
    if r["unit_tutup_biaya"] > r["target"]:
        print("PERINGATAN: target 7 hari belum menutup biaya uji - kecilkan biaya uji atau naikkan target.")
    print()
    print("Rumus: untung/unit = harga - potongan - modal per unit; laba uji = target x untung/unit - biaya uji.")
    print("Pembulatan ke rupiah terdekat. Perkiraan kasar, bukan HPP lengkap (pakai skill 'hitung-hpp').")
    return 0


def buat_parser():
    p = argparse.ArgumentParser(description="Skor ide usaha tertimbang + titik impas kasar")
    sub = p.add_subparsers(dest="perintah", required=True)

    p_skor = sub.add_parser("skor", help="Hitung skor tertimbang & peringkat ide")
    p_skor.add_argument("--ide", required=True,
                        help="Path file CSV daftar ide di folder kerja pengguna, atau '-' untuk membaca dari stdin")
    p_skor.add_argument(
        "--bobot",
        required=False,
        default=None,
        help=(
            "Path file JSON bobot kriteria (opsional). Kalau tidak diberikan, "
            "dipakai bobot default resmi (bila nama kolom kriteria cocok) atau bobot sama rata."
        ),
    )
    p_skor.set_defaults(func=cmd_skor)

    p_impas = sub.add_parser("impas", help="Hitung titik impas kasar (unit)")
    p_impas.add_argument(
        "--modal", required=True, type=_tipe_rupiah_cli,
        help="Modal awal (Rupiah). Terima 5000000, 5.000.000, Rp5.000.000, atau 5jt",
    )
    p_impas.add_argument(
        "--margin", required=True, type=_tipe_rupiah_cli,
        help="Margin/untung per unit (Rupiah). Terima format yang sama dengan --modal",
    )
    p_impas.set_defaults(func=cmd_impas)

    p_ren = sub.add_parser("rencana", help="Hitungan rupiah rencana uji 7 hari")
    p_ren.add_argument("--harga", required=True, type=_tipe_rupiah_cli, help="Harga jual per unit (Rupiah)")
    p_ren.add_argument("--modal-unit", required=True, type=_tipe_rupiah_cli,
                       help="Modal per unit: bahan + kemasan + ongkos langsung (Rupiah)")
    p_ren.add_argument("--potongan-persen", type=_tipe_persen_cli, default=0.0,
                       help="Potongan/komisi aplikasi atau marketplace dalam persen (0 bila jual langsung via WA)")
    p_ren.add_argument("--biaya-uji", type=_tipe_rupiah_cli, default=0.0,
                       help="Total uang keluar khusus uji 7 hari: sampel, cetak, iklan, ongkir promo (Rupiah)")
    p_ren.add_argument("--target", type=int, default=10, help="Target unit/pesanan dalam 7 hari (default 10)")
    p_ren.add_argument("--modal", type=_tipe_rupiah_cli, default=None,
                       help="Opsional: modal awal alat/peralatan untuk dihitung balik modalnya (Rupiah)")
    p_ren.set_defaults(func=cmd_rencana)

    return p


_OPSI_RUPIAH = ("--modal", "--margin", "--harga", "--modal-unit", "--biaya-uji")


def _gabungkan_opsi_negatif(argv):
    """argparse memperlakukan mis. '--modal -5jt' sebagai kekurangan argumen,
    karena nilainya diawali '-' dan bukan angka murni. Gabungkan jadi
    '--modal=-5jt' supaya nilainya tetap diproses lewat parse_rupiah dan
    pengguna dapat pesan error Bahasa Indonesia yang jelas (bukan pesan
    argparse bawaan dalam Bahasa Inggris)."""
    hasil = []
    i = 0
    while i < len(argv):
        tok = argv[i]
        if (
            tok in _OPSI_RUPIAH
            and i + 1 < len(argv)
            and argv[i + 1].startswith("-")
            and not argv[i + 1].startswith("--")
        ):
            hasil.append(f"{tok}={argv[i + 1]}")
            i += 2
            continue
        hasil.append(tok)
        i += 1
    return hasil


def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]
    argv = _gabungkan_opsi_negatif(argv)
    parser = buat_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
