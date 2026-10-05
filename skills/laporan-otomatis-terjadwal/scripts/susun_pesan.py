#!/usr/bin/env python3
"""Merakit pesan laporan ringkas (siap kirim ke WA/Telegram) dari angka JSON.

Dipakai SETELAH angka dihitung oleh script skill lain (mis. rekap-penjualan-csv,
laporan-keuangan-emkm, arus-kas-13minggu, tagih-piutang, buku-stok) atau skill ini
sendiri (cek_sumber_data.py). Script ini TIDAK menghitung ulang apa pun -- hanya
memformat Rupiah dan merapikan tata letak supaya angka penting ada di atas dan
pesan tidak lebih dari batas baris (default 15, sesuai aturan skill: ringkas
untuk layar HP).

Hanya library standar Python (3.8+). Input JSON lewat --data <file> atau '-'
(stdin). Output: teks pesan ke stdout.

Exit code:
  0  Normal, tidak ada indikasi data pribadi.
  1  Input tidak valid (JSON rusak/field wajib hilang) -- pesan error ke stderr,
     TIDAK ADA pesan dicetak ke stdout.
  3  Pesan berhasil dirakit dan DICETAK ke stdout seperti biasa, TAPI salah satu
     baris mengandung pola yang mirip data pribadi (NIK/KTP/nomor HP/email).
     Penjelasannya HANYA ditulis ke stderr, TIDAK ditambahkan ke isi pesan.
     Agent WAJIB berhenti sebelum mengaktifkan jadwal dan meninjau ulang baris
     yang dituding (lihat pesan di stderr) -- lihat SKILL.md.

Skema input (semua field opsional kecuali "judul"):
{
  "judul": "Laporan Penjualan Harian",
  "subjudul": "Selasa, 23 Sep 2026",
  "baris": [
    {"label": "Total omzet", "nilai": 4500000, "rupiah": true},
    {"label": "Jumlah transaksi", "nilai": 32},
    {"label": "Dibanding kemarin", "teks": "+12% dari Senin (Rp 4.020.000)"}
  ],
  "daftar": [
    {"judul": "Produk terlaris", "item": ["Kopi susu -- Rp 1.200.000", "Roti bakar -- Rp 800.000"]}
  ],
  "catatan": ["Data mencakup periode 21-22 Sep 2026 (2 hari)."],
  "peringatan": ["1 baris dilewati (tanggal tidak terbaca)."]
}

"baris" tampil sebagai "Label: nilai" di bagian atas pesan (angka penting dulu).
"nilai" rupiah sebaiknya angka JSON (4500000). Bila berupa teks, dibaca format
Indonesia ("38.000" = 38 ribu, "1.250.000,50", "Rp 38.000", "38rb", "1,5jt");
teks ragu ("38.5", "1,5", "1,500") membuat script keluar dengan exit 1.
"daftar" tampil sebagai sub-bagian berjudul dengan bullet -- bagian INI yang
dipotong lebih dulu bila pesan melebihi --maks-baris.
"catatan" = info netral (tanpa ikon peringatan, mis. cakupan periode, sumber data).
"peringatan" = hal yang perlu diwaspadai pengguna (ikon ⚠️, mis. baris dilewati,
data basi). Minimal SATU baris peringatan (bila ada) selalu dipertahankan walau
pesan dipotong.
TIDAK ADA field untuk nama/kontak pelanggan perorangan -- sengaja tidak
disediakan supaya penyusun laporan tidak menaruh data pribadi pelanggan di
pesan ini (UU PDP). Data pelanggan tetap boleh dilihat di file detail lokal.
Script ini juga MENDETEKSI (bukan mencegah) pola yang mirip data pribadi di
baris manapun -- lihat exit code 3 di atas.
"""
import argparse
import json
import re
import sys
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP

# Pola deteksi data pribadi -- semua pakai batas kata (\b) atau lookaround supaya
# tidak salah kena kata yang cuma "kebetulan mengandung" polanya, mis. \bnik\b
# TIDAK cocok dengan "unik"/"Klinik" (huruf sebelum "nik" adalah huruf, bukan
# batas kata di situ).
POLA_PDP = [
    ("NIK", re.compile(r"\bnik\b", re.IGNORECASE)),
    ("nomor KTP", re.compile(r"\b(no\.?\s*ktp|nomor\s*ktp|ktp)\b", re.IGNORECASE)),
    ("nomor HP/telepon (kata)", re.compile(
        r"\b(nomor|no\.?)\s*(hp|telepon|telp|wa|whatsapp)\b", re.IGNORECASE)),
    # Nomor HP polos atau dengan pemisah spasi/titik/strip (0812-0000-1234, +62 812 0000 1234);
    # tidak menempel ke huruf/angka lain (mis. nomor resi "JNE0812345678" tidak dianggap nomor HP).
    ("nomor HP/telepon (angka)", re.compile(
        r"(?<![\w+\-/#])\(?(\+62|62|0)[\s.\-]?8\d{1,3}\)?(?:[\s.\-]?\d){6,10}(?![\w])")),
    ("email", re.compile(r"\b[\w.+-]+@[\w-]+\.[a-zA-Z]{2,}\b")),
    ("alamat lengkap (kata)", re.compile(r"\balamat\s+(rumah|lengkap|tinggal)\b", re.IGNORECASE)),
]


SATUAN_RUPIAH = (("ribu", 1000), ("rb", 1000), ("k", 1000), ("juta", 10 ** 6), ("jt", 10 ** 6))
CONTOH_RUPIAH = "Contoh yang benar: 38000, \"38.000\", \"Rp38.000\", \"1.250.000,50\", \"38rb\", \"1,5jt\"."


def baca_rupiah_teks(teks):
    """Nilai rupiah berupa TEKS dibaca format Indonesia: titik = ribuan, koma = desimal.
    '38.000' / 'Rp 38.000' / '1.250.000,50' / '38rb' / '1,5jt'. Bentuk ragu ('38.5', '1,5', '1,500')
    ditolak (ValueError), tidak pernah ditebak diam-diam. Angka JSON (bukan teks) tidak lewat sini."""
    asli = str(teks).strip()
    s = asli.lower().replace("\u00a0", "").replace(" ", "")
    neg = s.startswith("-")
    s = s.lstrip("-")
    s = re.sub(r"^(rp|idr)\.?", "", s)
    s = re.sub(r"[,.]-+$", "", s)
    kali = 1
    for akhiran, k in SATUAN_RUPIAH:
        if s.endswith(akhiran) and s[: -len(akhiran)]:
            s, kali = s[: -len(akhiran)], k
            break
    if re.fullmatch(r"\d+", s):
        pass
    elif kali != 1 and re.fullmatch(r"\d+[.,]\d+", s):                 # 1,5jt
        s = s.replace(",", ".")
    elif re.fullmatch(r"[1-9]\d{0,2}(\.\d{3})+(,\d+)?", s):            # 38.000 / 1.250.000,50
        s = s.replace(".", "").replace(",", ".")
    elif re.fullmatch(r"\d{4,}[.,]\d{1,2}", s):                         # 38000.5 / 38000,50
        s = s.replace(",", ".")
    elif re.fullmatch(r"\d+[.,]\d+", s):                                # 38.5 / 1,5 / 1,500
        raise ValueError(f"Nilai rupiah {asli!r} meragukan (titik/koma bisa berarti ribuan atau desimal). "
                         + CONTOH_RUPIAH)
    else:
        raise ValueError(f"Nilai rupiah tidak valid: {asli!r}. " + CONTOH_RUPIAH)
    d = Decimal(s) * kali
    return -d if neg else d


def format_rupiah(nilai):
    if isinstance(nilai, bool):
        raise ValueError(f"Nilai rupiah tidak valid: {nilai!r}")
    try:
        if isinstance(nilai, str):
            d = baca_rupiah_teks(nilai)
        else:
            d = Decimal(str(float(nilai))) if isinstance(nilai, float) else Decimal(nilai)
        if not d.is_finite():
            raise ValueError
        n = int(d.quantize(Decimal(1), rounding=ROUND_HALF_UP))
    except (TypeError, ValueError, InvalidOperation) as e:
        if isinstance(e, ValueError) and str(e):
            raise
        raise ValueError(f"Nilai rupiah tidak valid: {nilai!r}")
    negatif = n < 0
    n = abs(n)
    teks = f"{n:,}".replace(",", ".")
    return ("-Rp " if negatif else "Rp ") + teks


def format_angka(nilai):
    if isinstance(nilai, float) and nilai.is_integer():
        nilai = int(nilai)
    if isinstance(nilai, float):
        teks = f"{nilai:,.2f}".replace(",", "@").replace(".", ",").replace("@", ".")
        return teks
    if isinstance(nilai, int):
        return f"{nilai:,}".replace(",", ".")
    return str(nilai)


def cek_data_pribadi(teks, sumber, temuan_keluar):
    for nama_pola, pola in POLA_PDP:
        if pola.search(teks):
            temuan_keluar.append(
                f"Baris {sumber} '{teks}' mengandung pola mirip {nama_pola} -- kemungkinan "
                "data pribadi pelanggan/karyawan. Sesuai UU PDP, laporan rutin sebaiknya "
                "hanya berisi angka agregat, bukan identitas orang. Tinjau ulang baris ini "
                "sebelum mengaktifkan jadwal."
            )


class Baris:
    """Satu baris pesan berlabel, supaya bisa dikelompokkan (header/angka/daftar/catatan)."""

    def __init__(self, teks, kelompok):
        self.teks = teks
        self.kelompok = kelompok  # "header" | "angka" | "daftar_judul" | "daftar_item" | "catatan" | "peringatan"


def main():
    p = argparse.ArgumentParser(description="Rakit pesan laporan ringkas dari data JSON")
    p.add_argument("--data", default="-", help="File JSON berisi data laporan, atau '-' untuk stdin (default)")
    p.add_argument("--maks-baris", type=int, default=15, help="Batas jumlah baris pesan (default 15)")
    a = p.parse_args()

    try:
        mentah = sys.stdin.read() if a.data == "-" else open(a.data, "r", encoding="utf-8").read()
    except OSError as e:
        print(f"ERROR: gagal membaca --data: {e}", file=sys.stderr)
        sys.exit(1)

    try:
        data = json.loads(mentah)
    except json.JSONDecodeError as e:
        print(f"ERROR: JSON input tidak valid: {e}", file=sys.stderr)
        sys.exit(1)

    if not isinstance(data, dict) or not data.get("judul"):
        print("ERROR: JSON input wajib berupa objek dengan field 'judul' berisi teks.", file=sys.stderr)
        sys.exit(1)

    temuan_pdp = []
    entri = [Baris(f"*{data['judul']}*", "header")]
    cek_data_pribadi(str(data["judul"]), "judul", temuan_pdp)
    if data.get("subjudul"):
        cek_data_pribadi(str(data["subjudul"]), "subjudul", temuan_pdp)
        entri.append(Baris(str(data["subjudul"]), "header"))

    for b in data.get("baris", []):
        label = b.get("label")
        if not label:
            print("ERROR: setiap item 'baris' wajib punya 'label'.", file=sys.stderr)
            sys.exit(1)
        if "teks" in b:
            nilai_teks = str(b["teks"])
        elif "nilai" not in b:
            print(f"ERROR: item baris '{label}' wajib punya 'nilai' atau 'teks'.", file=sys.stderr)
            sys.exit(1)
        elif b.get("rupiah"):
            try:
                nilai_teks = format_rupiah(b["nilai"])
            except ValueError as e:
                print(f"ERROR: {e} (baris '{label}')", file=sys.stderr)
                sys.exit(1)
        else:
            nilai_teks = format_angka(b["nilai"])
        baris_gabungan = f"{label}: {nilai_teks}"
        cek_data_pribadi(baris_gabungan, "angka", temuan_pdp)
        entri.append(Baris(baris_gabungan, "angka"))

    for seksi in data.get("daftar", []):
        judul_seksi = seksi.get("judul", "")
        item = seksi.get("item", [])
        if not item:
            continue
        if judul_seksi:
            entri.append(Baris(f"*{judul_seksi}*", "daftar_judul"))
        for it in item:
            teks_item = f"- {it}"
            cek_data_pribadi(teks_item, "daftar", temuan_pdp)
            entri.append(Baris(teks_item, "daftar_item"))

    for c in data.get("catatan", []):
        cek_data_pribadi(str(c), "catatan", temuan_pdp)
        entri.append(Baris(str(c), "catatan"))
    for pr in data.get("peringatan", []):
        cek_data_pribadi(str(pr), "peringatan", temuan_pdp)
        entri.append(Baris(f"⚠️ {pr}", "peringatan"))

    # --- Potong bila melebihi --maks-baris ---
    # Urutan pengorbanan: 1) item daftar (dari yang terakhir), lalu judul daftar
    # yang jadi kosong, 2) catatan netral (dari yang terakhir), TAPI selalu
    # sisakan minimal satu baris "peringatan" bila memang ada peringatan.
    # header dan angka TIDAK PERNAH dipotong.
    dipotong = False
    while len([e for e in entri if e.kelompok != "header" or True]) - 0 > 0:
        jumlah_saat_ini = len(entri) + (1 if dipotong else 0)  # +1 untuk baris notice bila sudah dipotong
        if jumlah_saat_ini <= a.maks_baris:
            break
        # Cari kandidat untuk dibuang, prioritas: daftar_item terakhir -> daftar_judul
        # yatim -> catatan terakhir -> (peringatan TIDAK dibuang kecuali >1 tersisa)
        idx_buang = None
        for i in range(len(entri) - 1, -1, -1):
            if entri[i].kelompok == "daftar_item":
                idx_buang = i
                break
        if idx_buang is None:
            # Buang judul daftar yang sudah tidak punya item di bawahnya
            for i in range(len(entri) - 1, -1, -1):
                if entri[i].kelompok == "daftar_judul":
                    ada_item_setelah = any(
                        e.kelompok == "daftar_item" for e in entri[i + 1:]
                        if e.kelompok in ("daftar_item", "daftar_judul", "catatan", "peringatan")
                    )
                    if not ada_item_setelah:
                        idx_buang = i
                        break
        if idx_buang is None:
            for i in range(len(entri) - 1, -1, -1):
                if entri[i].kelompok == "catatan":
                    idx_buang = i
                    break
        if idx_buang is None:
            jumlah_peringatan = sum(1 for e in entri if e.kelompok == "peringatan")
            if jumlah_peringatan > 1:
                for i in range(len(entri) - 1, -1, -1):
                    if entri[i].kelompok == "peringatan":
                        idx_buang = i
                        break
        if idx_buang is None:
            # Tidak ada lagi yang aman dibuang (hanya tersisa header/angka/1 peringatan)
            break
        del entri[idx_buang]
        dipotong = True

    # Bersihkan judul daftar yang jadi yatim (semua itemnya sudah dibuang di atas):
    # buang tiap daftar_judul yang tidak diikuti daftar_item sebelum daftar_judul
    # berikutnya (atau akhir daftar entri).
    entri_bersih = []
    for i, e in enumerate(entri):
        if e.kelompok == "daftar_judul":
            ada_item = False
            for nanti in entri[i + 1:]:
                if nanti.kelompok == "daftar_judul":
                    break
                if nanti.kelompok == "daftar_item":
                    ada_item = True
                    break
            if not ada_item:
                continue
        entri_bersih.append(e)
    entri = entri_bersih

    baris_akhir = [e.teks for e in entri]
    if dipotong:
        baris_akhir.append("(disingkat -- sebagian item tidak ditampilkan di pesan ini)")

    print("\n".join(baris_akhir))

    if temuan_pdp:
        for t in temuan_pdp:
            print(f"PERINGATAN-PDP: {t}", file=sys.stderr)
        sys.exit(3)


if __name__ == "__main__":
    main()
