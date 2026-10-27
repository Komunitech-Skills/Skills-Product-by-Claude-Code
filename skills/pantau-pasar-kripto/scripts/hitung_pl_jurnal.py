#!/usr/bin/env python3
"""Rapikan jurnal trading kripto milik member & hitung P/L dari angka yang MEMBER masukkan.

TIDAK menghitung/mengira harga sendiri, TIDAK memberi rekomendasi beli/jual, dan TIDAK
menilai apakah rencana member "benar". Skrip ini murni: (1) merapikan baris jurnal,
(2) menghitung realized P/L per transaksi jual memakai metode FIFO (First In First Out)
atas lot pembelian yang dicatat member sendiri, termasuk biaya, (3) mendaftar rencana
tinjau-ulang yang member tulis sendiri dan sudah jatuh tempo, dan (4) sejak v1.0.12 menyusun
TEKS CHAT siap kirim (`--keluaran teks`, atau field JSON `teks_bagian`) -- dipecah sendiri bila
panjang, supaya agent tidak menulis ulang rincian (uji Telegram G25: rincian tulisan agent
mengurangkan fee dua kali).

Format kolom CSV wajib (header persis, boleh urutan bebas). Pemisah kolom **koma (,) atau
titik-koma (;)** -- dideteksi otomatis dari baris header (titik-koma umum dipakai Excel
lokal Indonesia). BOM UTF-8 di awal file (ditulis Excel) dan file yang tidak murni UTF-8
(karakter aneh di teks bebas) ditangani otomatis, tidak menggagalkan seluruh file:
  tanggal            -> YYYY-MM-DD
  koin               -> kode singkat, mis. BTC (huruf besar/kecil bebas, dirapikan)
  aksi               -> "beli" atau "jual"
  jumlah_koin        -> angka desimal, mis. "0.015" atau "0,015". Gaya dibaca PER KOLOM (v1.0.12):
                         "12.000" dibaca dua belas ribu HANYA bila kolom ini bergaya Indonesia
                         (ada koma desimal / titik ribuan bertingkat, dan tidak ada angka bertitik
                         desimal seperti "0.5"); selain itu dibaca 12 dan diberi catatan "Perhatian".
  harga_satuan       -> harga per 1 unit koin dalam Rupiah: "Rp 1.500.000", "1.500.000", "1500000",
                         "1500000,50", "0.152", ".152", "Rp. 850", "rp850", "IDR 850" (dibaca persis,
                         tanpa float). nan/inf/"1_000"/format campur aduk ditolak.
  biaya              -> total biaya/fee transaksi ini dalam Rupiah (boleh 0), format sama
  platform           -> OPSIONAL: "dalam-negeri" / "luar-negeri" per baris (default --platform)
  alasan_rencana     -> teks bebas milik member (opsional, boleh kosong)
  tinjau_ulang_pada  -> tanggal YYYY-MM-DD (opsional) -- kapan member ingin diingatkan
  tinjau_ulang_syarat -> teks bebas milik member, mis. "kalau turun 20% dari sini" (opsional)

Baris yang rusak TIDAK menghentikan proses -- dicatat di "baris_bermasalah" (Bahasa Indonesia).
Bila baris yang ditolak memengaruhi hitungan (beli koin yang kemudian dijual, jual yang ditolak,
tanggal tidak terbaca, jual melebihi stok) hasil ditandai `status_hasil: "BELUM LENGKAP"` dan
angka PPh disebut "sementara".

Hitungan memakai pecahan eksak (fractions.Fraction) -- berapa pun digit desimalnya, tanpa
pembulatan di tengah. Pembulatan HANYA di hasil akhir: Rupiah ke rupiah terdekat (setengah
menjauhi nol), PPh dibulatkan ke bawah per transaksi.

Pemeriksaan kewajaran biaya (v1.0.5, field `cek_biaya`), filter periode (`--periode`/`--dari`/
`--sampai`: hanya membatasi transaksi JUAL yang dijumlahkan; FIFO tetap memakai seluruh riwayat).

Estimasi PPh final (field `estimasi_pajak`, v1.0.6; batas tanggal v1.0.11; platform per baris
v1.0.12): tarif PMK 50/2025 (0,21% / 1% dari nilai JUAL) hanya untuk transaksi jual sejak
1 Agustus 2025. Jual sebelum tanggal itu (aturan lama, PMK 68/PMK.03/2022) tidak diestimasi --
didaftar di `jual_sebelum_1_agustus_2025` + `catatan_aturan_lama`.
"""

import argparse
import csv
import io
import json
import math
import re
import sys
from collections import defaultdict, deque
from datetime import date, datetime
from decimal import Decimal, ROUND_DOWN, ROUND_HALF_UP, localcontext
from fractions import Fraction

VERSI = "1.0.12"
KOLOM_WAJIB = ["tanggal", "koin", "aksi", "jumlah_koin", "harga_satuan", "biaya"]
BATAS_PESAN = 3800          # maks. karakter per bagian teks chat (batas Telegram 4.096, sisakan ruang)
PENANDA_BAGIAN = "––– kirim sebagai pesan terpisah: bagian {n} dari {m} –––"
DISCLAIMER = "Informasi, bukan nasihat investasi. Keputusan & risiko sepenuhnya milik Anda."


class JurnalTidakValid(Exception):
    """Masalah pada file jurnal itu sendiri (bukan pada satu baris) -- header hilang,
    kolom wajib tidak ada, file tidak ditemukan, dsb. Selalu pesan Bahasa Indonesia."""


# ---------------------------------------------------------------------------
# Angka: pembulatan & pembacaan (eksak, tanpa float)
# ---------------------------------------------------------------------------

def _ke_fraction(nilai):
    if isinstance(nilai, Fraction):
        return nilai
    if isinstance(nilai, (int, Decimal)):
        return Fraction(nilai)
    return Fraction(Decimal(str(nilai)))


def bulat_rupiah(nilai):
    """Ke rupiah terdekat, setengah menjauhi nol (sama dengan ROUND_HALF_UP Decimal)."""
    f = _ke_fraction(nilai)
    tanda = -1 if f < 0 else 1
    return tanda * math.floor(abs(f) + Fraction(1, 2))


def _bulat_2_desimal(f):
    f = _ke_fraction(f)
    tanda = -1 if f < 0 else 1
    sen = math.floor(abs(f) * 100 + Fraction(1, 2))
    return tanda * sen / 100.0


def _fraction_ke_decimal(f):
    """Pecahan berpenyebut 2^a*5^b (hasil jumlah/kurang angka desimal) -> Decimal eksak."""
    f = _ke_fraction(f)
    with localcontext() as ctx:
        ctx.prec = 400
        return (Decimal(f.numerator) / Decimal(f.denominator)).normalize()


def angka_koin_teks(f):
    """Jumlah koin gaya Indonesia, tanpa pemisah ribuan: 0.01 -> '0,01', 12000 -> '12000'."""
    d = _fraction_ke_decimal(f)
    s = format(d, "f")
    if "." in s:
        s = s.rstrip("0").rstrip(".")
    return s.replace(".", ",")


def _jumlah_json(f):
    """Angka koin untuk JSON (kompatibel versi lama: float, 10 desimal)."""
    return round(float(_ke_fraction(f)), 10)


RE_PREFIX_RP = re.compile(r"^(rp\.?|idr)\s*", re.I)
RE_BULAT = re.compile(r"^\d+$")
RE_RIBUAN_TITIK = re.compile(r"^[1-9]\d{0,2}(\.\d{3})+$")
RE_ID_PENUH = re.compile(r"^[1-9]\d{0,2}(\.\d{3})+,\d+$")
RE_KOMA_DES = re.compile(r"^\d*,\d+$")
RE_TITIK_DES = re.compile(r"^\d*\.\d+$")
RE_TIGA_DIGIT_SATU_PEMISAH = re.compile(r"^[1-9]\d{0,2}[.,]\d{3}$")
RE_RIBUAN_SPASI = re.compile(r"^[1-9]\d{0,2}([ \u00a0\u202f]\d{3})+(,\d+)?$")   # "1 500 000" (v1.0.12)
RE_RUPIAH_KOMA_TIGA = re.compile(r"^[1-9]\d{0,2},\d{3}$")   # "1,500": 1,5 atau 1.500? (v1.0.12)


def _pisah_tanda(s):
    neg = False
    if s.startswith("-"):
        neg, s = True, s[1:].strip()
    return neg, s


def _parse_rupiah(teks):
    """Kembalikan (Decimal, ada_prefix_rp). Format tidak dikenal -> ValueError."""
    if teks is None:
        raise ValueError("nilainya kosong")
    s = str(teks).strip()
    if s == "":
        raise ValueError("nilainya kosong")
    neg, s = _pisah_tanda(s)
    m = RE_PREFIX_RP.match(s)
    ada_prefix = bool(m)
    if m:
        s = s[m.end():].strip()
        neg2, s = _pisah_tanda(s)
        neg = neg or neg2
    if RE_BULAT.match(s):
        angka = s
    elif RE_RIBUAN_SPASI.match(s):
        angka = re.sub(r"[ \u00a0\u202f]", "", s).replace(",", ".")
    elif RE_RIBUAN_TITIK.match(s):
        angka = s.replace(".", "")
    elif RE_ID_PENUH.match(s):
        angka = s.replace(".", "").replace(",", ".")
    elif RE_KOMA_DES.match(s):
        angka = s.replace(",", ".")
    elif RE_TITIK_DES.match(s):
        angka = s
    else:
        raise ValueError(
            f"'{teks}' bukan angka Rupiah yang bisa dibaca (contoh yang benar: 1.500.000 / "
            "1500000 / 1500000,50 / Rp 850).")
    if angka.startswith("."):
        angka = "0" + angka
    d = Decimal(angka)
    return (-d if neg else d), ada_prefix


def parse_angka_id(teks):
    """'Rp 1.500.000', '1.500.000,50', '1500000', '0.152', 'IDR 850' -> Decimal (eksak).

    Dipakai untuk kolom Rupiah (harga_satuan, biaya) -- BUKAN untuk jumlah_koin."""
    return _parse_rupiah(teks)[0]


def _bersihkan_koin(teks):
    if teks is None:
        raise ValueError("nilainya kosong")
    s = str(teks).strip().replace(" ", "")
    if s == "":
        raise ValueError("nilainya kosong")
    return s


def deteksi_gaya_jumlah(daftar_teks):
    """'id' bila kolom jumlah_koin bergaya Indonesia (koma desimal / titik ribuan bertingkat) dan
    TIDAK ada angka bertitik desimal (mis. '0.5'); selain itu 'titik'."""
    bukti_id = False
    ada_titik_desimal = False
    for t in daftar_teks:
        try:
            _, s = _pisah_tanda(_bersihkan_koin(t))
        except ValueError:
            continue
        if RE_KOMA_DES.match(s) or RE_ID_PENUH.match(s) or (RE_RIBUAN_TITIK.match(s) and s.count(".") >= 2):
            bukti_id = True
        elif RE_TITIK_DES.match(s) and not RE_RIBUAN_TITIK.match(s):
            ada_titik_desimal = True
    return "id" if bukti_id and not ada_titik_desimal else "titik"


def parse_jumlah_koin(teks, gaya=None):
    """Jumlah koin -> Decimal eksak. gaya='id' (kolom bergaya Indonesia): titik = ribuan, koma =
    desimal. Selain itu titik ATAU koma = tanda desimal, keduanya sekaligus ditolak."""
    s0 = _bersihkan_koin(teks)
    neg, s = _pisah_tanda(s0)
    if gaya == "id":
        if RE_BULAT.match(s):
            angka = s
        elif RE_RIBUAN_TITIK.match(s):
            angka = s.replace(".", "")
        elif RE_ID_PENUH.match(s) or RE_KOMA_DES.match(s):
            angka = s.replace(".", "").replace(",", ".")
        else:
            raise ValueError(f"'{teks}' bukan angka yang bisa dibaca untuk jumlah koin (kolom ini memakai "
                             "koma sebagai tanda desimal, mis. '0,015').")
    else:
        if "," in s and "." in s:
            raise ValueError(
                f"'{teks}' memakai koma dan titik sekaligus -- untuk jumlah koin pakai satu saja "
                "sebagai tanda desimal, mis. '0.015' atau '0,015'.")
        if RE_BULAT.match(s) or RE_TITIK_DES.match(s):
            angka = s
        elif RE_KOMA_DES.match(s):
            angka = s.replace(",", ".")
        else:
            raise ValueError(f"'{teks}' bukan angka yang bisa dibaca untuk jumlah koin.")
    if angka.startswith("."):
        angka = "0" + angka
    d = Decimal(angka)
    return -d if neg else d


# ---------------------------------------------------------------------------
# Terbilang (untuk catatan "Perhatian": dibaca 1,5 koin, satu koma lima)
# ---------------------------------------------------------------------------

_SATUAN = ["nol", "satu", "dua", "tiga", "empat", "lima", "enam", "tujuh", "delapan", "sembilan",
           "sepuluh", "sebelas"]


def _terbilang_bulat(n):
    if n < 12:
        return _SATUAN[n]
    if n < 20:
        return _terbilang_bulat(n - 10) + " belas"
    if n < 100:
        return _terbilang_bulat(n // 10) + " puluh" + (" " + _terbilang_bulat(n % 10) if n % 10 else "")
    if n < 200:
        return "seratus" + (" " + _terbilang_bulat(n - 100) if n - 100 else "")
    if n < 1000:
        return _terbilang_bulat(n // 100) + " ratus" + (" " + _terbilang_bulat(n % 100) if n % 100 else "")
    if n < 2000:
        return "seribu" + (" " + _terbilang_bulat(n - 1000) if n - 1000 else "")
    for besar, nama in ((10 ** 12, "triliun"), (10 ** 9, "miliar"), (10 ** 6, "juta"), (10 ** 3, "ribu")):
        if n >= besar:
            if n >= besar * 1000 and besar == 10 ** 12:
                return " ".join(_SATUAN[int(c)] for c in str(n))
            sisa = n % besar
            return _terbilang_bulat(n // besar) + " " + nama + (" " + _terbilang_bulat(sisa) if sisa else "")
    return str(n)


def terbilang(teks_angka):
    """'1,5' -> 'satu koma lima'; '12000' -> 'dua belas ribu'."""
    bulat, _, des = teks_angka.partition(",")
    kata = _terbilang_bulat(int(bulat or "0"))
    if des:
        kata += " koma " + " ".join(_SATUAN[int(c)] for c in des)
    return kata


# ---------------------------------------------------------------------------
# Baca file jurnal
# ---------------------------------------------------------------------------

def parse_tanggal(teks, nama_field="tanggal"):
    try:
        return datetime.strptime(teks.strip(), "%Y-%m-%d").date()
    except (ValueError, AttributeError):
        raise ValueError(f"{nama_field} '{teks}' bukan tanggal valid (format harus YYYY-MM-DD, mis. 2026-09-24).")


def _baca_teks_tahan_encoding(path):
    with open(path, "rb") as f:
        mentah = f.read()
    try:
        return mentah.decode("utf-8-sig"), None
    except UnicodeDecodeError:
        return (
            mentah.decode("utf-8-sig", errors="replace"),
            "Sebagian karakter di file jurnal bukan UTF-8 murni (mis. hasil salin dari "
            "aplikasi lain) -- karakter itu diganti '�', teks lain tidak terpengaruh.",
        )


def _deteksi_pemisah(baris_header):
    if baris_header.count(";") > baris_header.count(","):
        return ";"
    return ","


PLATFORM_ALIAS = {"dalam-negeri": "dalam-negeri", "dalam negeri": "dalam-negeri", "dalam": "dalam-negeri",
                  "luar-negeri": "luar-negeri", "luar negeri": "luar-negeri", "luar": "luar-negeri"}


def muat_jurnal(path, info=None):
    """Kembalikan (baris_ok, baris_bermasalah, peringatan_global). Bila `info` (dict) diberikan,
    diisi: 'ditolak' (koin/aksi/tanggal mentah baris yang ditolak), 'catatan' (Perhatian), 'ragu'."""
    if info is None:
        info = {}
    info.setdefault("ditolak", [])
    info.setdefault("catatan", [])
    info.setdefault("ragu", [])
    try:
        teks, peringatan_encoding = _baca_teks_tahan_encoding(path)
    except FileNotFoundError:
        raise JurnalTidakValid(f"File jurnal tidak ditemukan: {path}")
    except OSError as e:
        raise JurnalTidakValid(f"File jurnal tidak bisa dibaca: {e}")

    if teks.strip() == "":
        raise JurnalTidakValid("File jurnal kosong (tidak ada isi sama sekali, termasuk baris header).")

    baris_pertama = teks.splitlines()[0] if teks.splitlines() else ""
    pemisah = _deteksi_pemisah(baris_pertama)

    peringatan_global = [peringatan_encoding] if peringatan_encoding else []
    baris_ok = []
    baris_bermasalah = []

    reader = csv.DictReader(io.StringIO(teks), delimiter=pemisah)
    if reader.fieldnames is None:
        raise JurnalTidakValid("File jurnal tidak punya baris header.")
    reader.fieldnames = [(k or "").strip() for k in reader.fieldnames]
    hilang = [k for k in KOLOM_WAJIB if k not in reader.fieldnames]
    if hilang:
        raise JurnalTidakValid(
            f"Kolom wajib hilang di header: {', '.join(hilang)}. "
            f"(Pemisah kolom yang terdeteksi: '{pemisah}' -- kalau file Anda memakai pemisah "
            "lain, ganti dulu ke koma atau titik-koma.)"
        )
    semua = list(enumerate(reader, start=2))  # baris 1 = header
    gaya = deteksi_gaya_jumlah([row.get("jumlah_koin") for _, row in semua])
    info["gaya_jumlah_koin"] = gaya

    for nomor, row in semua:
        mentah_koin = (row.get("koin") or "").strip().upper()
        mentah_aksi = (row.get("aksi") or "").strip().lower()
        tgl = None
        try:
            tgl = parse_tanggal(row["tanggal"])
            koin = mentah_koin
            if not koin:
                raise ValueError("kolom 'koin' kosong")
            aksi = mentah_aksi
            if aksi not in ("beli", "jual"):
                raise ValueError(f"kolom 'aksi' harus 'beli' atau 'jual', dapat '{row['aksi']}'")
            asli_jumlah = (row["jumlah_koin"] or "").strip()
            jumlah = parse_jumlah_koin(asli_jumlah, gaya)
            if jumlah <= 0:
                raise ValueError("'jumlah_koin' harus lebih besar dari 0")
            harga = parse_angka_id(row["harga_satuan"])
            if harga < 0:
                raise ValueError("'harga_satuan' tidak boleh negatif")
            asli_biaya = (row.get("biaya") or "").strip() or "0"
            biaya, prefix_biaya = _parse_rupiah(asli_biaya)
            if biaya < 0:
                raise ValueError("'biaya' tidak boleh negatif")
            mentah_platform = (row.get("platform") or "").strip().lower()
            platform = None
            if mentah_platform:
                platform = PLATFORM_ALIAS.get(mentah_platform)
                if platform is None:
                    raise ValueError(f"kolom 'platform' harus 'dalam-negeri' atau 'luar-negeri', dapat "
                                     f"'{row.get('platform')}'")
        except (ValueError, KeyError, ArithmeticError) as e:
            baris_bermasalah.append({"baris": nomor, "alasan": str(e)})
            info["ditolak"].append({"baris": nomor, "koin": mentah_koin, "aksi": mentah_aksi, "tanggal": tgl})
            continue

        # Catatan pembacaan (tanpa pemisah + terbilang) untuk angka koin yang bisa dibaca dua cara.
        _, inti = _pisah_tanda(asli_jumlah.replace(" ", ""))
        if RE_TIGA_DIGIT_SATU_PEMISAH.match(inti) and not (gaya == "id" and "," in inti):
            dibaca = angka_koin_teks(jumlah)
            kalimat = f"baris {nomor}: jumlah koin '{asli_jumlah}' dibaca {dibaca} koin, {terbilang(dibaca)}"
            if gaya == "id":
                # kolom bergaya Indonesia: titik = ribuan, cukup diberi tahu (tidak ditahan)
                kalimat += " (kolom jumlah koin Anda memakai titik ribuan & koma desimal)."
            else:
                alt = inti.replace(".", "").replace(",", "")
                kalimat += (f". Bila maksudnya {alt} koin, tulis {alt} lalu hitung ulang; untung setelah "
                            "pajak ditahan dulu sampai dipastikan.")
                info["ragu"].append(nomor)
            info["catatan"].append(kalimat)
        if prefix_biaya and 0 < biaya < 1:
            kalimat = (f"baris {nomor}: biaya '{asli_biaya}' dibaca Rp{angka_koin_teks(biaya)} (kurang dari Rp1) -- "
                       "periksa nominal")
            # saran angka lain hanya bila 3 digit di belakang pemisah (pola ribuan, mis. "Rp 0.152")
            m3 = re.match(r"^0[.,](\d{3})$", _pisah_tanda(RE_PREFIX_RP.sub("", asli_biaya.strip()).strip())[1])
            if m3:
                alt = m3.group(1).lstrip("0") or "0"
                kalimat += f"; bila maksudnya Rp{alt}, tulis {alt} lalu hitung ulang."
            else:
                kalimat += " di riwayat exchange."
            info["catatan"].append(kalimat)
            info["ragu"].append(nomor)
        for nama_kolom, asli in (("harga_satuan", (row.get("harga_satuan") or "").strip()), ("biaya", asli_biaya)):
            inti_rp = _pisah_tanda(RE_PREFIX_RP.sub("", _pisah_tanda(asli)[1]).strip())[1]
            if RE_RUPIAH_KOMA_TIGA.match(inti_rp):
                ribuan = inti_rp.replace(",", "")
                info["catatan"].append(
                    f"baris {nomor}: {nama_kolom} '{asli}' dibaca Rp{inti_rp} (koma = tanda desimal). Bila "
                    f"maksudnya Rp{ribuan[:-3]}.{ribuan[-3:]}, tulis {ribuan} lalu hitung ulang; untung setelah "
                    "pajak ditahan dulu sampai dipastikan.")
                info["ragu"].append(nomor)
        baris_ok.append({
            "baris": nomor,
            "tanggal": tgl,
            "koin": koin,
            "aksi": aksi,
            "jumlah_koin": jumlah,
            "harga_satuan": harga,
            "biaya": biaya,
            "platform": platform,
            "alasan_rencana": (row.get("alasan_rencana") or "").strip(),
            "tinjau_ulang_pada": (row.get("tinjau_ulang_pada") or "").strip(),
            "tinjau_ulang_syarat": (row.get("tinjau_ulang_syarat") or "").strip(),
        })

    return baris_ok, baris_bermasalah, peringatan_global


# ---------------------------------------------------------------------------
# FIFO (eksak)
# ---------------------------------------------------------------------------

def hitung_fifo(baris_ok):
    """Kembalikan (posisi_per_koin, realized_per_koin, baris_bermasalah_tambahan)."""
    lot = defaultdict(deque)
    realized = defaultdict(list)
    bermasalah_tambahan = []

    urut = sorted(baris_ok, key=lambda r: (r["tanggal"], r["baris"]))
    for r in urut:
        koin = r["koin"]
        jumlah = _ke_fraction(r["jumlah_koin"])
        harga = _ke_fraction(r["harga_satuan"])
        biaya = _ke_fraction(r["biaya"])
        if r["aksi"] == "beli":
            lot[koin].append({"sisa": jumlah, "harga": harga, "biaya_per_unit": biaya / jumlah,
                              "tanggal": r["tanggal"]})
            continue
        sisa_jual = jumlah
        modal = Fraction(0)
        terpakai = Fraction(0)
        while sisa_jual > 0 and lot[koin]:
            l = lot[koin][0]
            ambil = min(l["sisa"], sisa_jual)
            modal += ambil * (l["harga"] + l["biaya_per_unit"])
            terpakai += ambil
            l["sisa"] -= ambil
            sisa_jual -= ambil
            if l["sisa"] == 0:
                lot[koin].popleft()
        if sisa_jual > 0:
            bermasalah_tambahan.append({
                "baris": r["baris"],
                "alasan": (
                    f"Jual {angka_koin_teks(jumlah)} {koin} melebihi stok yang tercatat dari baris 'beli' "
                    f"sebelumnya (kekurangan {angka_koin_teks(sisa_jual)}). P/L dihitung hanya untuk bagian "
                    "yang ada lot-nya; sisanya diabaikan -- kemungkinan ada baris 'beli' yang belum dicatat."
                ),
            })
        if terpakai > 0:
            fee = biaya * terpakai / jumlah
            hasil_bersih = terpakai * harga - fee
            pl = hasil_bersih - modal
            realized[koin].append({
                "baris": r["baris"],
                "tanggal": r["tanggal"].isoformat(),
                "jumlah_terjual": _jumlah_json(terpakai),
                "jumlah_terjual_teks": angka_koin_teks(terpakai),
                "proceeds": bulat_rupiah(hasil_bersih),
                "cost_basis": bulat_rupiah(modal),
                "biaya": bulat_rupiah(r["biaya"]),
                "biaya_terhitung": bulat_rupiah(fee),
                "pl": bulat_rupiah(pl),
                # persen hanya bila modal setelah dibulatkan > Rp0 (hindari "Rp0 (+100,00%)")
                "pl_persen": _bulat_2_desimal(pl / modal * 100) if bulat_rupiah(modal) > 0 else None,
            })

    posisi = {}
    for koin, lots in lot.items():
        jumlah_total = sum((l["sisa"] for l in lots), Fraction(0))
        if jumlah_total <= 0:
            continue
        nilai_total = sum((l["sisa"] * (l["harga"] + l["biaya_per_unit"]) for l in lots), Fraction(0))
        posisi[koin] = {
            "jumlah_tersisa": _jumlah_json(jumlah_total),
            "jumlah_tersisa_teks": angka_koin_teks(jumlah_total),
            "harga_rata_rata_perolehan": bulat_rupiah(nilai_total / jumlah_total),
            "jumlah_lot": len(lots),
        }
    return posisi, realized, bermasalah_tambahan


# ---------------------------------------------------------------------------
# Pemeriksaan biaya (v1.0.5) -- hanya MENANDAI
# ---------------------------------------------------------------------------
BATAS_BIAYA_WAJAR_PERSEN = 1.0
RASIO_BEDA_JAUH = 1.5
SELISIH_MIN_POIN = 0.05


def _pid(x):
    return f"{x:.2f}".replace(".", ",")


def _median(nilai):
    v = sorted(nilai)
    n = len(v)
    if n == 0:
        return None
    return v[n // 2] if n % 2 else (v[n // 2 - 1] + v[n // 2]) / 2.0


def _beda_jauh(a, b):
    if b is None or b <= 0:
        return False
    return abs(a - b) >= SELISIH_MIN_POIN and (a >= b * RASIO_BEDA_JAUH or a * RASIO_BEDA_JAUH <= b)


def periksa_biaya(baris_ok):
    data = []
    for r in baris_ok:
        nilai = _ke_fraction(r["jumlah_koin"]) * _ke_fraction(r["harga_satuan"])
        if nilai <= 0:
            continue
        data.append((r, float(_ke_fraction(r["biaya"]) / nilai * 100)))
    hasil = []
    med_sisi = {a: _median([p for r, p in data if r["aksi"] == a and p > 0]) for a in ("beli", "jual")}
    for i, (r, persen) in enumerate(data):
        alasan = []
        if persen > BATAS_BIAYA_WAJAR_PERSEN:
            alasan.append(f"biaya {_pid(persen)}% dari nilai transaksi, di atas {BATAS_BIAYA_WAJAR_PERSEN:.0f}% "
                          "(fee + pajak di exchange Indonesia umumnya jauh di bawah ini)")
        grup = [p for rr, p in data if p > 0 and rr["aksi"] == r["aksi"]]
        if len(grup) >= 3:
            lain, label = grup, f"transaksi {r['aksi']} lain"
        elif len(grup) == 2:
            lain, label = [p for j, (rr, p) in enumerate(data)
                           if j != i and p > 0 and rr["aksi"] == r["aksi"]], f"transaksi {r['aksi']} lain"
        else:
            semua = [p for _, p in data if p > 0]
            lain, label = (semua if len(semua) >= 3 else []), "transaksi lain"
        med_lain = _median(lain)
        if persen > 0 and _beda_jauh(persen, med_lain):
            alasan.append(f"biaya {_pid(persen)}% berbeda jauh dari {label} (median {_pid(med_lain)}%)")
        if alasan:
            hasil.append({
                "baris": r["baris"], "tanggal": r["tanggal"].isoformat(), "koin": r["koin"], "aksi": r["aksi"],
                "biaya": bulat_rupiah(r["biaya"]), "biaya_persen": round(persen, 3), "alasan": "; ".join(alasan),
            })
    catatan_sisi = None
    if med_sisi["beli"] and med_sisi["jual"] and _beda_jauh(med_sisi["jual"], med_sisi["beli"]):
        catatan_sisi = (f"Rata-rata (median) biaya JUAL {_pid(med_sisi['jual'])}% vs BELI {_pid(med_sisi['beli'])}% "
                        "berbeda jauh -- cek tabel fee resmi exchange Anda.")
    return hasil, catatan_sisi


# ---------------------------------------------------------------------------
# Estimasi PPh final kripto -- HANYA dihitung di sini (v1.0.6; batas tanggal v1.0.11; per baris v1.0.12)
# Dasar: PMK 50/2025 (berlaku 1 Agustus 2025), ringkasan resmi https://www.pajak.go.id/index.php/en/node/117234
#  - objek PPh = penghasilan PENJUAL -> basis = nilai transaksi JUAL; BELI tidak dikenai PPh.
#  - 0,21% bila lewat PPMSE yang merupakan PAKD dalam negeri (dipungut PAKD); 1% bila lewat PPMSE bukan
#    PAKD dalam negeri; bila PPMSE itu belum ditunjuk pemungut, wajib disetor sendiri oleh penjual.
#  - Penyerahan aset kripto tidak dikenai PPN (PMK 50/2025 Pasal 2 ayat (1): dipersamakan dengan surat
#    berharga; artikel DJP https://www.pajak.go.id/id/artikel/beli-kripto-tidak-lagi-kena-ppn, dicek
#    2026-10-27). PPN atas JASA platform/fee exchange tetap ada (bagian biaya exchange).
#  - Jual sebelum 1 Agustus 2025: aturan lama PMK 68/PMK.03/2022 -> tidak diestimasi.
# ---------------------------------------------------------------------------
TARIF_PPH_KRIPTO = {"dalam-negeri": Decimal("0.21"), "luar-negeri": Decimal("1")}
TGL_BERLAKU_PMK50 = date(2025, 8, 1)
KET_PLATFORM = {
    "dalam-negeri": "PAKD dalam negeri berizin OJK (mis. Indodax) -- PPh dipungut otomatis oleh exchange",
    "luar-negeri": "PPMSE bukan PAKD dalam negeri (exchange luar negeri) -- bila exchange itu belum ditunjuk "
                   "sebagai pemungut, PPh wajib disetor sendiri oleh penjual",
}
KALIMAT_PPN = "Penyerahan aset kripto tidak dikenai PPN (Pasal 2 ayat (1))."


def _rp(x):
    return ("-" if x < 0 else "") + "Rp" + f"{abs(x):,}".replace(",", ".")


def _tarif_teks(tarif):
    return format(tarif.normalize(), "f").replace(".", ",")


def hitung_estimasi_pajak(baris_ok, platform, dari=None, sampai=None, total_realized_pl=0):
    rinci = []
    sebelum_berlaku = []
    nilai_per = {"dalam-negeri": Fraction(0), "luar-negeri": Fraction(0)}
    pph_per = {"dalam-negeri": 0, "luar-negeri": 0}
    for r in sorted(baris_ok, key=lambda x: (x["tanggal"], x["baris"])):
        if r["aksi"] != "jual":
            continue
        if (dari and r["tanggal"] < dari) or (sampai and r["tanggal"] > sampai):
            continue
        nilai = _ke_fraction(r["jumlah_koin"]) * _ke_fraction(r["harga_satuan"])
        if r["tanggal"] < TGL_BERLAKU_PMK50:
            sebelum_berlaku.append({"baris": r["baris"], "tanggal": r["tanggal"].isoformat(), "koin": r["koin"],
                                    "nilai_jual": bulat_rupiah(nilai)})
            continue
        plat = r.get("platform") or platform
        tarif = TARIF_PPH_KRIPTO[plat]
        pph = math.floor(nilai * Fraction(tarif) / 100)   # dibulatkan ke bawah, sama dgn bot-trading-kripto
        nilai_per[plat] += nilai
        pph_per[plat] += pph
        rinci.append({"baris": r["baris"], "tanggal": r["tanggal"].isoformat(), "koin": r["koin"],
                      "platform": plat, "tarif_persen": float(tarif),
                      "nilai_jual": bulat_rupiah(nilai), "estimasi_pph": pph})
    total_nilai = nilai_per["dalam-negeri"] + nilai_per["luar-negeri"]
    total_pph = pph_per["dalam-negeri"] + pph_per["luar-negeri"]
    dipakai = sorted({x["platform"] for x in rinci}) or [platform]
    if len(dipakai) == 1:
        p = dipakai[0]
        tt = _tarif_teks(TARIF_PPH_KRIPTO[p])
        teks = (f"Estimasi PPh Pasal 22 final {tt}% (PMK 50/2025, untuk jual sejak 1 Agustus 2025) = "
                f"{tt}% x total nilai JUAL {_rp(bulat_rupiah(total_nilai))} = {_rp(total_pph)}. "
                "Transaksi BELI tidak dikenai PPh.")
    else:
        teks = ("Estimasi PPh Pasal 22 final (PMK 50/2025, untuk jual sejak 1 Agustus 2025) = 0,21% x nilai JUAL "
                f"dalam negeri {_rp(bulat_rupiah(nilai_per['dalam-negeri']))} ({_rp(pph_per['dalam-negeri'])}) + "
                f"1% x nilai JUAL luar negeri {_rp(bulat_rupiah(nilai_per['luar-negeri']))} "
                f"({_rp(pph_per['luar-negeri'])}) = {_rp(total_pph)}. Transaksi BELI tidak dikenai PPh.")
    catatan_lama = None
    if sebelum_berlaku:
        catatan_lama = (f"{len(sebelum_berlaku)} transaksi jual bertanggal sebelum 1 Agustus 2025 TIDAK diestimasi: "
                        "untuk transaksi itu berlaku aturan lama (PMK 68/PMK.03/2022), yang digantikan PMK 50/2025 "
                        "mulai 1 Agustus 2025. Cek potongan pajak di riwayat transaksi exchange atau tanyakan ke "
                        "konsultan pajak/DJP.")
        teks += " " + catatan_lama
    return {
        "dasar_hukum": "PMK 50/2025, berlaku 1 Agustus 2025 -- hanya untuk transaksi jual sejak tanggal itu "
                       "(ringkasan resmi: https://www.pajak.go.id/index.php/en/node/117234)",
        "jenis": "PPh Pasal 22 final, dipungut dari PENJUAL",
        "platform": dipakai[0] if len(dipakai) == 1 else "campuran",
        "keterangan_platform": KET_PLATFORM[dipakai[0]] if len(dipakai) == 1 else
        KET_PLATFORM["dalam-negeri"] + "; " + KET_PLATFORM["luar-negeri"],
        "tarif_persen": float(TARIF_PPH_KRIPTO[dipakai[0]]) if len(dipakai) == 1 else None,
        "basis": "nilai transaksi JUAL (jumlah koin x harga satuan, sebelum fee). Transaksi BELI tidak dikenai "
                 "PPh. " + KALIMAT_PPN + " PMK 50/2025, sejak 1 Agustus 2025.",
        "per_transaksi_jual": rinci,
        "jual_sebelum_1_agustus_2025": sebelum_berlaku,
        "catatan_aturan_lama": catatan_lama,
        "total_nilai_jual": bulat_rupiah(total_nilai),
        "total_estimasi_pph": total_pph,
        "total_pph_dalam_negeri": pph_per["dalam-negeri"],
        "total_pph_luar_negeri": pph_per["luar-negeri"],
        "ringkasan_teks": teks,
        "sudah_termasuk_di_kolom_biaya": "TIDAK DIKETAHUI -- jangan disimpulkan dari kemiripan angka; cek kolom "
                                          "pajak/PPh di riwayat transaksi exchange",
        "pl_bila_pph_belum_di_kolom_biaya": total_realized_pl - total_pph,
        "pl_bila_pph_dalam_negeri_sudah_di_kolom_biaya": total_realized_pl - pph_per["luar-negeri"],
        "catatan": "Estimasi per transaksi dibulatkan ke bawah ke rupiah penuh; pembulatan exchange bisa berbeda "
                   "beberapa rupiah. Bukan perhitungan SPT/nasihat pajak -- kepastian ke konsultan pajak/DJP.",
    }


def daftar_tinjau_ulang(baris_ok, hari_ini):
    hasil = []
    for r in baris_ok:
        if not r["tinjau_ulang_pada"]:
            continue
        try:
            tgl = parse_tanggal(r["tinjau_ulang_pada"], "tinjau_ulang_pada")
        except ValueError:
            continue
        if tgl <= hari_ini:
            hasil.append({
                "baris": r["baris"],
                "koin": r["koin"],
                "tanggal_ditulis": r["tanggal"].isoformat(),
                "tinjau_ulang_pada": tgl.isoformat(),
                "jatuh_tempo": tgl < hari_ini,
                "syarat": r["tinjau_ulang_syarat"] or "(tidak ditulis syaratnya)",
                "alasan_rencana_asal": r["alasan_rencana"] or "(tidak ditulis)",
            })
    hasil.sort(key=lambda x: x["tinjau_ulang_pada"])
    return hasil


def hitung_rentang_periode(periode, hari_ini):
    if periode == "bulan-ini":
        return hari_ini.replace(day=1), hari_ini
    if periode == "tahun-ini":
        return hari_ini.replace(month=1, day=1), hari_ini
    return None, None


def nilai_kelengkapan(baris_ok, info, bermasalah_fifo):
    """Kembalikan daftar alasan hasil BELUM LENGKAP (kosong = lengkap)."""
    alasan = []
    jual_valid = defaultdict(list)
    for r in baris_ok:
        if r["aksi"] == "jual":
            jual_valid[r["koin"]].append(r["tanggal"])
    for d in info.get("ditolak", []):
        if d["tanggal"] is None:
            alasan.append(f"baris {d['baris']} ditolak dan tanggalnya tidak terbaca -- urutan FIFO tidak bisa "
                          "dipastikan.")
        elif d["aksi"] == "jual":
            alasan.append(f"baris {d['baris']} (jual {d['koin'] or '?'}) ditolak -- untung/rugi transaksi itu "
                          "belum masuk total.")
        elif d["aksi"] != "beli":
            # v1.0.12: aksi tidak terbaca ('Buy', 'pembelian', kosong) -- bisa beli (lot FIFO hilang) atau
            # jual (untung/rugi hilang), jadi selalu dianggap memengaruhi hasil.
            alasan.append(f"baris {d['baris']} ({d['koin'] or 'koin ?'}) ditolak dan aksinya tidak terbaca "
                          f"('{d['aksi']}') -- bisa beli atau jual, jadi modal & untung/rugi bisa salah. Tulis "
                          "'beli' atau 'jual'.")
        elif not d["koin"]:
            # beli tanpa nama koin: bisa jadi lot FIFO untuk koin apa pun yang dijual sesudahnya
            if any(t >= d["tanggal"] for lst in jual_valid.values() for t in lst):
                alasan.append(f"baris {d['baris']} (beli, kolom koin kosong) ditolak padahal ada penjualan "
                              "sesudahnya -- modal & untung/rugi bisa salah. Isi nama koinnya.")
        elif any(t >= d["tanggal"] for t in jual_valid.get(d["koin"], [])):
            alasan.append(f"baris {d['baris']} (beli {d['koin']}) ditolak padahal {d['koin']} dijual sesudahnya -- "
                          f"modal & untung/rugi {d['koin']} bisa salah.")
    for b in bermasalah_fifo:
        alasan.append(f"baris {b['baris']}: jual melebihi stok yang tercatat -- ada baris beli yang belum dicatat.")
    return alasan


# ---------------------------------------------------------------------------
# Teks chat siap kirim (v1.0.12)
# ---------------------------------------------------------------------------
_BULAN = ["Jan", "Feb", "Mar", "Apr", "Mei", "Jun", "Jul", "Agu", "Sep", "Okt", "Nov", "Des"]


def _tgl(iso):
    d = date.fromisoformat(iso)
    return f"{d.day} {_BULAN[d.month - 1]} {d.year}"


def _rp_tanda(x):
    return ("+" if x > 0 else "") + _rp(x)


def _persen(p, pl=None):
    if p is None or pl == 0:
        return ""
    return f" ({'+' if p > 0 else ''}{p:.2f}%)".replace(".", ",")


def susun_teks(h, ringkas=False):
    """Susun teks chat dari dict hasil. Kembalikan string (belum dipecah)."""
    blok = []
    lengkap = h["status_hasil"] == "LENGKAP"
    kepala = ["Rekap jurnal kripto (FIFO, dari angka yang Anda catat)"]
    if h["periode"]["dari"] or h["periode"]["sampai"]:
        kepala.append(f"Periode jual: {_tgl(h['periode']['dari']) if h['periode']['dari'] else 'awal'} s/d "
                      f"{_tgl(h['periode']['sampai']) if h['periode']['sampai'] else 'akhir'}")
    if lengkap:
        kepala.append(f"Hasil: LENGKAP -- {h['jumlah_baris_dihitung']} baris dihitung"
                      + (", tidak ada baris ditolak." if not h["baris_bermasalah"] else
                         f", {len(h['baris_bermasalah'])} baris ditolak (tidak ada penjualan sesudahnya yang "
                         "terpengaruh; sisa koin bisa kurang sampai baris itu diperbaiki)."))
    else:
        kepala.append("Hasil: BELUM LENGKAP -- angka di bawah sementara. Perbaiki dulu:")
        kepala += [f"• {a}" for a in h["alasan_belum_lengkap"]]
    blok.append("\n".join(kepala))

    jual = sorted((r | {"koin": k} for k, v in h["realized_per_koin"].items() for r in v),
                  key=lambda r: (r["tanggal"], r["baris"]))
    if jual:
        b = ["Untung/rugi yang sudah dijual (fee beli masuk modal, fee jual memotong hasil jual):"]
        for r in jual:
            if ringkas:
                b.append(f"• {_tgl(r['tanggal'])} {r['koin']} {r['jumlah_terjual_teks']}: "
                         f"{_rp_tanda(r['pl'])}{_persen(r['pl_persen'], r['pl'])}")
                continue
            baris = (f"• {r['koin']} jual {_tgl(r['tanggal'])} ({r['jumlah_terjual_teks']} {r['koin']}): "
                     f"hasil jual bersih {_rp(r['proceeds'])} (sudah dipotong fee {_rp(r['biaya_terhitung'])}) "
                     f"- modal {_rp(r['cost_basis'])} = {_rp_tanda(r['pl'])}{_persen(r['pl_persen'], r['pl'])}")
            if r["proceeds"] - r["cost_basis"] != r["pl"]:
                baris += " (selisih Rp1 karena pembulatan)"
            b.append(baris)
        b.append(f"Total untung/rugi (sebelum pajak): {_rp_tanda(h['total_realized_pl'])}")
        blok.append("\n".join(b))
    else:
        blok.append("Belum ada transaksi jual yang dihitung.")

    if h["posisi_tersisa"]:
        b = ["Sisa koin & rata-rata modal (termasuk fee beli):"]
        for k, p in sorted(h["posisi_tersisa"].items()):
            b.append(f"• {k}: {p['jumlah_tersisa_teks']} @ {_rp(p['harga_rata_rata_perolehan'])}")
        blok.append("\n".join(b))

    p = h["estimasi_pajak"]
    sifat = h["sifat_angka_pph"]
    if p["per_transaksi_jual"] or p["jual_sebelum_1_agustus_2025"]:
        b = ["Pajak (PMK 50/2025, untuk jual sejak 1 Agustus 2025):",
             "• PPh Pasal 22 final dihitung dari nilai JUAL (jumlah x harga, sebelum fee); beli tidak kena PPh. "
             + KALIMAT_PPN]
        if not ringkas:
            for x in p["per_transaksi_jual"]:
                plat = "dalam negeri" if x["platform"] == "dalam-negeri" else "luar negeri"
                b.append(f"• {x['koin']} {_tgl(x['tanggal'])}, {plat} "
                         f"{_tarif_teks(TARIF_PPH_KRIPTO[x['platform']])}% x {_rp(x['nilai_jual'])} = "
                         f"{_rp(x['estimasi_pph'])}")
        dn, ln = p["total_pph_dalam_negeri"], p["total_pph_luar_negeri"]
        total = f"Total estimasi PPh: {_rp(p['total_estimasi_pph'])}"
        if dn and ln:
            total += (f" (dalam negeri {_rp(dn)}, dipungut exchange; luar negeri {_rp(ln)}, wajib disetor "
                      "sendiri bila exchange itu belum memungut)")
        elif ln:
            total += " (luar negeri: wajib disetor sendiri bila exchange itu belum memungut)"
        else:
            total += " (dalam negeri: dipungut otomatis oleh exchange)"
        b.append(total)
        if sifat == "tetap":
            b.append("Angka PPh ini tetap untuk data di atas.")
        else:
            b.append("Angka PPh ini sementara -- ada baris yang ditolak/ragu, akan berubah setelah diperbaiki.")
        if p["catatan_aturan_lama"]:
            b.append(p["catatan_aturan_lama"])
        blok.append("\n".join(b))

        total_pl = h["total_realized_pl"]
        if h["untung_setelah_pajak_ditahan"]:
            blok.append("Untung setelah pajak: ditahan dulu sampai baris yang ditolak/ragu dipastikan.")
        elif p["per_transaksi_jual"]:
            b = ["Untung setelah pajak (apakah PPh sudah masuk kolom biaya tidak diketahui -- cek riwayat "
                 "transaksi exchange):",
                 f"• Bila PPh belum ada di kolom biaya: {_rp(total_pl)} - {_rp(p['total_estimasi_pph'])} = "
                 f"{_rp(p['pl_bila_pph_belum_di_kolom_biaya'])}"]
            if dn and ln:
                b.append(f"• Bila PPh dalam negeri sudah dipotong exchange & masuk kolom biaya: {_rp(total_pl)} - "
                         f"{_rp(ln)} = {_rp(p['pl_bila_pph_dalam_negeri_sudah_di_kolom_biaya'])} (tinggal PPh "
                         "luar negeri)")
            elif dn:
                b.append(f"• Bila PPh sudah masuk kolom biaya: {_rp(total_pl)} (tidak dikurangi lagi)")
            blok.append("\n".join(b))

    perhatian = list(h["catatan_perhatian"])
    perhatian += [f"baris {x['baris']}: {x['alasan']}" for x in h["baris_bermasalah"]]
    perhatian += [f"baris {c['baris']} ({c['koin']} {c['aksi']} {_tgl(c['tanggal'])}): {c['alasan']} -- cek di "
                  "riwayat exchange." for c in h["cek_biaya"]]
    if h["cek_biaya_beli_vs_jual"]:
        perhatian.append(h["cek_biaya_beli_vs_jual"])
    perhatian += h["peringatan_global"]
    if perhatian:
        blok.append("\n".join(["Perhatian:"] + [f"• {x}" for x in perhatian]))

    if h["tinjau_ulang_jatuh_tempo"]:
        b = ["Rencana tinjau ulang yang Anda tulis sendiri (sudah waktunya):"]
        for t in h["tinjau_ulang_jatuh_tempo"]:
            b.append(f"• {t['koin']} (baris {t['baris']}, {_tgl(t['tinjau_ulang_pada'])}): \"{t['syarat']}\"")
        blok.append("\n".join(b))

    blok.append("Bukan perhitungan SPT/nasihat pajak; kepastian ke konsultan pajak/DJP.\n" + DISCLAIMER)
    return "\n\n".join(blok)


def pecah_teks(teks, batas=BATAS_PESAN):
    """Pecah di batas paragraf/baris; tiap bagian <= batas karakter."""
    if len(teks) <= batas:
        return [teks]
    satuan = []
    for par in teks.split("\n\n"):
        if len(par) <= batas:
            satuan.append(("p", par))
            continue
        for baris in par.split("\n"):
            while len(baris) > batas:
                # potong di spasi terakhir sebelum batas (bukan di tengah kata/angka)
                potong = baris.rfind(" ", batas // 2, batas)
                if potong <= 0:
                    potong = batas
                satuan.append(("b", baris[:potong].rstrip()))
                baris = baris[potong:].lstrip()
            satuan.append(("b", baris))
    bagian, kini = [], ""
    for jenis, isi in satuan:
        sambung = "\n\n" if jenis == "p" else "\n"
        calon = isi if not kini else kini + sambung + isi
        if len(calon) <= batas:
            kini = calon
        else:
            bagian.append(kini)
            kini = isi
    if kini:
        bagian.append(kini)
    return bagian


def siapkan_teks(h):
    """Kembalikan (mode, daftar_bagian). Mode ringkas hanya dipakai bila teks lengkap terlalu panjang DAN
    versi ringkas memang lebih pendek."""
    lengkap = susun_teks(h)
    mode, teks = "lengkap", lengkap
    if len(lengkap) > BATAS_PESAN:
        ringkas = susun_teks(h, ringkas=True)
        if len(ringkas) < len(lengkap):
            mode, teks = "ringkas", ringkas
    return mode, pecah_teks(teks)


def gabung_bagian(bagian):
    if len(bagian) == 1:
        return bagian[0]
    m = len(bagian)
    return "\n\n".join(PENANDA_BAGIAN.format(n=i, m=m) + "\n" + b for i, b in enumerate(bagian, start=1))


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

class _Parser(argparse.ArgumentParser):
    argv_mentah = None

    def _minta_teks(self):
        a = list(self.argv_mentah if self.argv_mentah is not None else sys.argv[1:])
        return "--keluaran=teks" in a or any(x == "--keluaran" and y == "teks" for x, y in zip(a, a[1:]))

    def error(self, message):
        pesan = "Pilihan perintah tidak dikenali: " + message
        if self._minta_teks():
            print(pesan)
        else:
            print(json.dumps({"status": "error", "pesan": pesan}, ensure_ascii=False, indent=2))
        sys.exit(1)


def _cetak(hasil, keluaran):
    if keluaran == "teks":
        print(gabung_bagian(hasil["teks_bagian"]))
    else:
        print(json.dumps(hasil, ensure_ascii=False, indent=2))


def _keluar_error(pesan, keluaran="json"):
    if keluaran == "teks":
        print(pesan)
    else:
        print(json.dumps({"status": "error", "pesan": pesan}, ensure_ascii=False, indent=2))
    return 1


def proses(args):
    try:
        hari_ini = parse_tanggal(args.hari_ini, "--hari-ini") if args.hari_ini else date.today()
        dari, sampai = hitung_rentang_periode(args.periode, hari_ini)
        if args.dari:
            dari = parse_tanggal(args.dari, "--dari")
        if args.sampai:
            sampai = parse_tanggal(args.sampai, "--sampai")
        if dari and sampai and dari > sampai:
            raise ValueError(f"--dari ({dari.isoformat()}) tidak boleh setelah --sampai ({sampai.isoformat()}).")
    except ValueError as e:
        return _keluar_error(str(e), args.keluaran)

    info = {}
    try:
        baris_ok, baris_bermasalah, peringatan_global = muat_jurnal(args.jurnal, info)
    except JurnalTidakValid as e:
        return _keluar_error(str(e), args.keluaran)

    if not baris_ok and not baris_bermasalah:
        teks = "Jurnal masih kosong (header ada, belum ada transaksi tercatat).\n\n" + DISCLAIMER
        hasil = {
            "status": "ok", "versi_skrip": VERSI, "status_hasil": "LENGKAP", "alasan_belum_lengkap": [],
            "posisi_tersisa": {}, "realized_per_koin": {}, "total_realized_pl": 0, "baris_bermasalah": [],
            "tinjau_ulang_jatuh_tempo": [], "cek_biaya": [], "cek_biaya_beli_vs_jual": None,
            "cek_biaya_keterangan": None, "jumlah_baris_dihitung": 0, "peringatan_global": peringatan_global,
            "pesan": "Jurnal masih kosong (header ada, belum ada transaksi tercatat).",
            "mode_teks": "lengkap", "jumlah_bagian": 1, "teks_bagian": [teks],
            "disclaimer": "Angka dari yang Anda catat sendiri, bukan nasihat investasi.",
        }
        _cetak(hasil, args.keluaran)
        return 0

    posisi, realized_semua, bermasalah_tambahan = hitung_fifo(baris_ok)
    semua_bermasalah = sorted(baris_bermasalah + bermasalah_tambahan, key=lambda x: x["baris"])

    if dari or sampai:
        realized = {}
        for koin, entri in realized_semua.items():
            terpilih = [r for r in entri
                        if (not dari or date.fromisoformat(r["tanggal"]) >= dari)
                        and (not sampai or date.fromisoformat(r["tanggal"]) <= sampai)]
            if terpilih:
                realized[koin] = terpilih
    else:
        realized = dict(realized_semua)

    total_realized_pl = sum(r["pl"] for lst in realized.values() for r in lst)
    cek_biaya, catatan_sisi = periksa_biaya(baris_ok)
    alasan_belum = nilai_kelengkapan(baris_ok, info, bermasalah_tambahan)
    ada_ragu = bool(info["ragu"])
    sifat_pph = "tetap" if not (semua_bermasalah or ada_ragu) else "sementara"

    hasil = {
        "status": "ok",
        "versi_skrip": VERSI,
        "status_hasil": "LENGKAP" if not alasan_belum else "BELUM LENGKAP",
        "alasan_belum_lengkap": alasan_belum,
        "periode": {
            "dari": dari.isoformat() if dari else None,
            "sampai": sampai.isoformat() if sampai else None,
            "keterangan": "hanya membatasi transaksi jual yang dihitung; posisi_tersisa & FIFO tetap penuh"
                          if (dari or sampai) else "semua transaksi",
        },
        "posisi_tersisa": posisi,
        "realized_per_koin": realized,
        "total_realized_pl": total_realized_pl,
        "baris_bermasalah": semua_bermasalah,
        "baris_ragu": sorted(set(info["ragu"])),
        "catatan_perhatian": info["catatan"],
        "gaya_jumlah_koin": info.get("gaya_jumlah_koin"),
        "tinjau_ulang_jatuh_tempo": daftar_tinjau_ulang(baris_ok, hari_ini),
        "cek_biaya": cek_biaya,
        "cek_biaya_beli_vs_jual": catatan_sisi,
        "cek_biaya_keterangan": (
            "Baris di 'cek_biaya' hanya DITANDAI agar dicek ke riwayat transaksi exchange (mis. salah ketik, "
            "biaya lain). Sebabnya tidak ditebak (juga tidak disimpulkan apakah PPh sudah termasuk); P/L tetap dihitung "
            "dari angka yang dicatat.") if (cek_biaya or catatan_sisi) else None,
        "estimasi_pajak": hitung_estimasi_pajak(baris_ok, args.platform, dari, sampai, total_realized_pl),
        "sifat_angka_pph": sifat_pph,
        "untung_setelah_pajak_ditahan": bool(alasan_belum or ada_ragu),
        "jumlah_baris_dihitung": len(baris_ok),
        "peringatan_global": peringatan_global,
        "disclaimer": "Angka dari yang Anda catat sendiri, bukan nasihat investasi.",
    }
    mode, bagian = siapkan_teks(hasil)
    hasil["mode_teks"] = mode
    hasil["jumlah_bagian"] = len(bagian)
    hasil["teks_bagian"] = bagian
    _cetak(hasil, args.keluaran)
    return 0


def main(argv=None):
    ap = _Parser(description="Rapikan jurnal trading kripto & hitung P/L (FIFO) dari angka member.")
    ap.argv_mentah = argv
    ap.add_argument("--jurnal", required=True, help="Path ke JURNAL.csv milik member.")
    ap.add_argument("--hari-ini", default=None,
                    help="Tanggal 'hari ini' (YYYY-MM-DD) untuk cek jatuh tempo tinjau-ulang & filter periode.")
    ap.add_argument("--periode", choices=["semua", "bulan-ini", "tahun-ini"], default="semua",
                    help="Batasi transaksi JUAL yang dijumlahkan (FIFO tetap memakai seluruh riwayat 'beli').")
    ap.add_argument("--dari", default=None, help="Batas awal (YYYY-MM-DD), menimpa --periode kalau diisi.")
    ap.add_argument("--sampai", default=None, help="Batas akhir (YYYY-MM-DD), menimpa --periode kalau diisi.")
    ap.add_argument("--platform", choices=["dalam-negeri", "luar-negeri"], default="dalam-negeri",
                    help="Default tempat transaksi untuk estimasi PPh (kolom 'platform' per baris menimpanya): "
                         "dalam-negeri (PAKD berizin OJK, 0,21%%) atau luar-negeri (1%%).")
    ap.add_argument("--keluaran", choices=["json", "teks"], default="json",
                    help="json (default, termasuk field teks_bagian) atau teks chat siap kirim.")
    ap.add_argument("--versi", action="version", version=f"hitung_pl_jurnal.py {VERSI}")
    args = ap.parse_args(argv)
    try:
        return proses(args)
    except Exception:  # noqa: BLE001 -- jangan pernah menampilkan traceback ke member
        return _keluar_error("Maaf, terjadi kesalahan tak terduga saat menghitung jurnal. File jurnal Anda tidak "
                             "diubah. Coba kirim ulang file jurnalnya; bila tetap gagal, hubungi admin Komunitech.",
                             args.keluaran)


if __name__ == "__main__":
    sys.exit(main())
