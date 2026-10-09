#!/usr/bin/env python3
"""Jadwal peluncuran produk (T-30 s.d. T+30) berbasis tanggal, memakai Python standar saja.

Contoh:
  python3 scripts/jadwal_peluncuran.py --tanggal 2026-11-14 --produk "Sambal Botol Bu Rina" --jenis pangan
  python3 scripts/jadwal_peluncuran.py --tanggal 2026-11-14 --format csv > jadwal.csv
  python3 scripts/jadwal_peluncuran.py --tanggal 2026-11-14 --jenis jasa   # tanpa tugas stok/kemasan/kirim
--hari-ini bawaannya tanggal hari ini (date.today()) sehingga peringatan waktu pendek/tugas LEWAT selalu aktif.
Windows: pakai `python` atau `py` sebagai ganti `python3`.

Aturan:
- Tugas "hari kerja" (pemasok, cetak label, urus izin, bank, ekspedisi) TIDAK ditaruh di Sabtu/Minggu/libur.
  Sebelum peluncuran digeser MUNDUR ke hari kerja sebelumnya; sesudahnya digeser MAJU. Hari kerja = Senin-Jumat.
- Tugas konten/percakapan (posting, WA, live) tetap di tanggalnya; bila jatuh di libur diberi catatan.
- Daftar libur = SKB 3 Menteri 2026 & 2027 (lihat LIBUR di bawah). Tahun lain: hanya Minggu yang dianggap libur + peringatan.
"""
import argparse
import csv
import io
import json
import sys
from datetime import date, datetime, timedelta

# Sumber: SKB Menag, Menaker, MenPANRB. 2026: No. 1497/2025, 2/2025, 5/2025 (19 Sep 2025).
# 2027: No. 1205/2026, 3/2026, 2/2026 (15 Sep 2026). Salinan dari skill kalender-pajak (dicek 2026-09-26);
# Daftar 2026 (25 tanggal) dan 2027 (26 tanggal) sudah dicocokkan 51/51 dengan SKB resmi (setneg.go.id, 2026-09-29).
# Selalu cocokkan dengan pengumuman terbaru pemerintah.
# jenis: L = libur nasional, C = cuti bersama.
LIBUR = {
    "2026-01-01": "Tahun Baru 2026", "2026-01-16": "Isra Mikraj",
    "2026-02-16": "Cuti bersama Imlek", "2026-02-17": "Tahun Baru Imlek",
    "2026-03-18": "Cuti bersama Nyepi", "2026-03-19": "Hari Suci Nyepi",
    "2026-03-20": "Cuti bersama Idulfitri", "2026-03-21": "Idulfitri 1447 H", "2026-03-22": "Idulfitri 1447 H",
    "2026-03-23": "Cuti bersama Idulfitri", "2026-03-24": "Cuti bersama Idulfitri",
    "2026-04-03": "Wafat Yesus Kristus", "2026-04-05": "Paskah",
    "2026-05-01": "Hari Buruh", "2026-05-14": "Kenaikan Yesus Kristus", "2026-05-15": "Cuti bersama Kenaikan",
    "2026-05-27": "Iduladha 1447 H", "2026-05-28": "Cuti bersama Iduladha", "2026-05-31": "Waisak",
    "2026-06-01": "Hari Lahir Pancasila", "2026-06-16": "1 Muharam 1448 H",
    "2026-08-17": "Hari Kemerdekaan RI", "2026-08-25": "Maulid Nabi",
    "2026-12-24": "Cuti bersama Natal", "2026-12-25": "Natal",
    "2027-01-01": "Tahun Baru 2027", "2027-01-05": "Isra Mikraj",
    "2027-02-05": "Cuti bersama Imlek", "2027-02-06": "Tahun Baru Imlek", "2027-03-08": "Hari Suci Nyepi",
    "2027-03-09": "Cuti bersama Idulfitri", "2027-03-10": "Idulfitri 1448 H", "2027-03-11": "Idulfitri 1448 H",
    "2027-03-12": "Cuti bersama Idulfitri", "2027-03-15": "Cuti bersama Idulfitri",
    "2027-03-25": "Cuti bersama Wafat Yesus Kristus", "2027-03-26": "Wafat Yesus Kristus", "2027-03-28": "Paskah",
    "2027-05-01": "Hari Buruh", "2027-05-06": "Kenaikan Yesus Kristus", "2027-05-17": "Iduladha 1448 H",
    "2027-05-18": "Cuti bersama Iduladha", "2027-05-19": "Cuti bersama Waisak", "2027-05-20": "Waisak",
    "2027-06-01": "Hari Lahir Pancasila", "2027-06-06": "1 Muharam 1449 H",
    "2027-08-15": "Maulid Nabi", "2027-08-17": "Hari Kemerdekaan RI",
    "2027-12-24": "Cuti bersama Natal", "2027-12-25": "Natal", "2027-12-26": "Isra Mikraj",
}
TAHUN_DATA = {2026, 2027}
HARI = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"]

# (offset, fase, kanal/bidang, tugas, hari_kerja, jenis) ; jenis: "*" semua, "fisik" semua kecuali jasa
# (stok/kemasan/kirim), "pangan" hanya makanan/minuman, "kosmetik" hanya kosmetik/perawatan, "jasa" hanya jasa.
TUGAS = [
    (-30, "Pra-peluncuran", "Strategi", "Tulis 1 kalimat janji produk, calon pembeli utama, dan target angka (mis. jumlah pesanan hari 1-7)", False, "*"),
    (-30, "Pra-peluncuran", "Harga", "Kunci HPP dan harga tayang; hitung margin setelah biaya marketplace (skill hitung-hpp, harga-jual-marketplace)", False, "*"),
    (-30, "Legalitas", "Izin", "Cek status izin & label: NIB, PIRT/BPOM, sertifikat halal (pangan). Ini pengingat; keputusan tetap di instansi resmi", True, "pangan"),
    (-30, "Legalitas", "Izin", "Cek apakah produk perawatan/kosmetik sudah notifikasi BPOM dan label sesuai aturan", True, "kosmetik"),
    (-28, "Stok & operasional", "Pemasok", "Pesan bahan/barang dan kemasan untuk stok awal; minta kepastian tanggal tiba tertulis", True, "fisik"),
    (-28, "Legalitas", "Label", "Finalkan teks label kemasan (komposisi, netto, produsen, tanggal kedaluwarsa, nomor izin/halal) lalu minta cek 2 orang", True, "pangan"),
    (-28, "Legalitas", "Label", "Finalkan teks label kosmetik (nama, komposisi/bahan, netto, produsen, nomor notifikasi BPOM, cara pakai, peringatan, kedaluwarsa); cek klaim manfaat tidak berlebihan; minta cek 2 orang", True, "kosmetik"),
    (-25, "Pra-peluncuran", "Aset", "Foto/video produk: minimal 1 foto putih bersih, 1 foto suasana, 1 video 15 detik (skill foto-produk-brief)", False, "*"),
    (-25, "Pra-peluncuran", "Waitlist", "Buat formulir daftar tunggu (Google Form atau tautan wa.me) dengan 3 isian: nama panggilan, nomor WA, rasa/varian diminati", False, "*"),
    (-21, "Pra-peluncuran", "Instagram/TikTok", "Posting teaser 1: masalah pelanggan + petunjuk produk (belum sebut nama/harga); ajak isi daftar tunggu", False, "*"),
    (-21, "Pra-peluncuran", "WA grup/komunitas", "Kabari 10-20 teman dekat/pelanggan lama lewat WA pribadi (bukan blast) dan minta mereka jadi 'tim pertama'", False, "*"),
    (-18, "Pra-peluncuran", "Marketplace", "Siapkan draf listing di marketplace (judul, foto, deskripsi, variasi, berat & ukuran paket) - skill listing-marketplace", False, "*"),
    (-16, "Stok & operasional", "Pemasok", "Cek kemajuan produksi/pesanan pemasok; bila mundur >3 hari, geser tanggal peluncuran SEKARANG", True, "fisik"),
    (-14, "Soft launch", "Waitlist", "Buka soft launch untuk daftar tunggu: pre-order terbatas (mis. 30-50 unit) dengan tanggal kirim jelas (paling lambat T-10); catat jumlah pre-order (dipakai untuk hitungan stok/kapasitas)", False, "*"),
    (-14, "Pra-peluncuran", "Instagram/TikTok", "Posting teaser 2: di balik layar pembuatan/produksi", False, "*"),
    (-12, "Pra-peluncuran", "KOL mikro", "Kirim sampel/undangan ke 3-5 kreator mikro yang cocok (1.000-50.000 pengikut); catat kesepakatan tertulis di chat", False, "*"),
    (-10, "Stok & operasional", "Pengemasan", "Beli kemasan pengiriman (dus, bubble wrap, lakban, stiker) untuk stok pesanan hari 1-14", True, "fisik"),
    (-10, "Stok & operasional", "Uji", "Uji coba kirim 2 paket ke alamat teman di luar kota; catat lama tiba dan kondisi barang", True, "fisik"),
    (-10, "Soft launch", "Kirim", "Kirim pre-order soft launch (batch kecil dari produksi pertama) dan unggah resi; umpan balik baru ditanya setelah barang tiba", True, "fisik"),
    (-10, "Soft launch", "Layanan", "Layani klien percobaan soft launch (3-5 klien, harga khusus terbatas) sesuai jadwal yang sudah dijanjikan", False, "jasa"),
    (-5, "Soft launch", "Umpan balik", "Setelah barang/layanan diterima, tanya 10 pembeli soft launch: 3 hal disuka, 1 hal kurang; perbaiki listing/label/kemasan bila perlu", False, "*"),
    (-7, "Stok & operasional", "Kapasitas", "Tetapkan kapasitas layanan (jumlah klien/slot per minggu), batas antrean, dan aturan tutup pendaftaran bila penuh", False, "jasa"),
    (-7, "Promo", "Harga", "Putuskan promo peluncuran (aturan di references/aturan-promo.md); hitung margin di harga promo terendah", False, "*"),
    (-7, "Stok & operasional", "Stok", "Hitung stok awal = (pre-order soft launch + perkiraan pesanan minggu 1) x 1,3 dan bandingkan dengan stok; tetapkan batas 'stok habis' dan pesan ulang", True, "fisik"),
    (-5, "Pra-peluncuran", "Instagram/TikTok", "Posting teaser 3: countdown + tanggal & jam peluncuran + tautan daftar tunggu", False, "*"),
    (-5, "Pra-peluncuran", "Offline", "Bila ikut bazar/titip jual: konfirmasi stan/tempat, jam, dan barang/materi yang dibawa", True, "*"),
    (-3, "Pra-peluncuran", "Marketplace", "Selesaikan listing (belum aktif/atur jadwal tayang), pasang voucher toko & iklan dengan anggaran harian kecil", False, "*"),
    (-3, "Legalitas", "Label", "Pastikan foto listing menampilkan label & nomor izin yang benar; sama dengan kemasan fisik", False, "pangan"),
    (-3, "Legalitas", "Label", "Pastikan foto listing menampilkan label, nomor notifikasi BPOM, dan klaim yang sama dengan kemasan fisik", False, "kosmetik"),
    (-2, "Stok & operasional", "Stok", "Stok fisik sudah di tangan dan dihitung ulang; kemasan pengiriman siap; barang tersimpan di tempat layak", True, "fisik"),
    (-2, "Peluncuran", "Tim", "Rapat 15 menit: siapa balas chat, siapa kemas, siapa posting; siapkan jawaban cepat (skill balas-chat-cs)", False, "*"),
    (-1, "Peluncuran", "Semua kanal", "Go/No-Go: barang/kapasitas layanan siap, harga & promo terpasang, listing tayang terjadwal, akun iklan aktif, nomor WA berfungsi", False, "*"),
    (-1, "Peluncuran", "WA grup/komunitas", "Kirim pengingat H-1 ke daftar tunggu (satu per satu atau lewat siaran WA resmi bagi yang sudah opt-in)", False, "*"),
    (0, "Peluncuran", "Semua kanal", "Pagi: aktifkan listing, posting pengumuman utama di IG/TikTok, story dengan tautan, kirim pesan ke daftar tunggu", False, "*"),
    (0, "Peluncuran", "Live/TikTok", "Siang/malam: sesi live singkat 30-60 menit atau posting video 'unboxing' (skill naskah-live-jualan)", False, "*"),
    (0, "Peluncuran", "Operasional", "Balas semua chat <15 menit, kemas pesanan sore itu, catat pesanan & kendala per jam", False, "*"),
    (0, "Peluncuran", "Pengukuran", "Malam: catat 5 angka hari-1 (kunjungan, chat, pesanan, omzet, sisa barang/slot)", False, "*"),
    (1, "Pasca-peluncuran", "Kirim", "T+1: kirim pesanan pertama (semua pesanan masuk di hari-1); unggah resi; kabari pembeli lewat pesan singkat", True, "fisik"),
    (1, "Pasca-peluncuran", "Konten", "Posting ucapan terima kasih + bukti sosial (tangkapan layar pesanan/testimoni dengan izin)", False, "*"),
    (3, "Pasca-peluncuran", "Ulasan", "Minta ulasan dari pembeli yang barangnya sudah tiba (sekali saja, sopan); balas ulasan (skill balas-ulasan-pelanggan)", False, "*"),
    (3, "Pasca-peluncuran", "Pengukuran", "Tinjau 3 hari pertama: pesanan vs target, keluhan terbanyak, biaya iklan vs omzet", False, "*"),
    (7, "Pasca-peluncuran", "Pengukuran", "Laporan minggu 1 (skill laporan-iklan-mingguan + rekap penjualan); putuskan lanjut/ubah/stop tiap kanal", False, "*"),
    (7, "Pasca-peluncuran", "Stok & operasional", "Pesan ulang stok bila sisa < kebutuhan 2 minggu; tetapkan waktu tunggu pemasok", True, "fisik"),
    (14, "Pasca-peluncuran", "Promo", "Akhiri/ubah promo peluncuran; umumkan harga normal secara jujur (tanpa coret harga palsu)", False, "*"),
    (14, "Pasca-peluncuran", "Konten", "Posting pelajaran: testimoni, tanya-jawab dari chat, 'ternyata pembeli suka ini'", False, "*"),
    (21, "Pasca-peluncuran", "Retensi", "Hubungi pembeli pertama: tanya kepuasan, tawarkan pembelian ulang/paket hemat (satu pesan pribadi)", False, "*"),
    (30, "Pasca-peluncuran", "Pengukuran", "Tinjauan 30 hari: omzet, margin nyata, pembeli ulang, keluhan; putuskan produk lanjut/perbaiki/tambah varian", False, "*"),
    (30, "Pasca-peluncuran", "Pengukuran", "Catat 3 pelajaran dan 3 perbaikan untuk peluncuran berikutnya di file terpisah", False, "*"),
]

KEMBAR = [(9, 9), (10, 10), (11, 11), (12, 12)]  # tanggal kembar marketplace: persaingan iklan/ongkir ketat


def parse_tanggal(s):
    try:
        return datetime.strptime(s.strip(), "%Y-%m-%d").date()
    except ValueError:
        raise ValueError(f"tanggal '{s}' tidak valid; pakai format TTTT-BB-HH, mis. 2026-11-14")


def libur_nama(d, ekstra):
    k = d.isoformat()
    if k in ekstra:
        return ekstra[k]
    if k in LIBUR:
        return LIBUR[k]
    if d.weekday() == 6:
        return "Minggu"
    return None


def hari_kerja(d, ekstra):
    return d.weekday() < 5 and d.isoformat() not in LIBUR and d.isoformat() not in ekstra


def geser(d, arah, ekstra):
    """Geser ke hari kerja terdekat: arah -1 mundur, +1 maju."""
    while not hari_kerja(d, ekstra):
        d += timedelta(days=arah)
    return d


# Mode izin edar belum terbit (--izin belum): tugas yang menerima pesanan/uang/promo dilarang sebelum izin terbit.
FASE_JUAL = {"Soft launch", "Promo", "Peluncuran", "Pasca-peluncuran"}
TUGAS_BOLEH_TANPA_IZIN = {"Strategi", "Harga", "Aset", "Izin", "Label", "Pemasok", "Pengemasan", "Kapasitas", "Tim"}
TEKS_WAITLIST_TANPA_BAYAR = ("Buka DAFTAR TUNGGU tanpa pembayaran (hanya kumpulkan nama & nomor WA; "
                             "tulis jelas: 'belum menerima pesanan dan belum menerima uang'). Pre-order/penjualan ditunda sampai izin terbit")
OFFSET_RINGKAS = {-30, -14, -7, -3, -1, 0, 1, 7, 30}


def bangun(tgl, jenis="pangan", ekstra=None, hari_ini=None, izin="sudah", ringkas=False):
    ekstra = ekstra or {}
    baris = []
    izin_belum = izin == "belum"
    for off, fase, kanal, tugas, hk, j in TUGAS:
        if j == "fisik":
            if jenis == "jasa":
                continue
        elif j != "*" and j != jenis:
            continue
        if ringkas and off not in OFFSET_RINGKAS and fase != "Legalitas":
            continue
        dijual = False
        if izin_belum:
            if fase == "Soft launch":
                if kanal == "Waitlist":
                    tugas = TEKS_WAITLIST_TANPA_BAYAR
                else:
                    continue  # kirim/layani/umpan balik soft launch: tidak ada penjualan sebelum izin
            elif fase in FASE_JUAL or kanal in ("Marketplace", "Offline", "KOL mikro"):
                dijual = kanal not in TUGAS_BOLEH_TANPA_IZIN
        asli = tgl + timedelta(days=off)
        d = geser(asli, -1 if off < 0 else 1, ekstra) if hk else asli
        cat = []
        if d != asli:
            cat.append(f"digeser dari {asli.isoformat()} ({HARI[asli.weekday()]}) karena bukan hari kerja")
        if not hk:
            n = libur_nama(d, ekstra)
            if n:
                cat.append(f"jatuh di {n}: jadwalkan posting, jangan andalkan pemasok/kurir")
        if d != asli and off > 0:
            cat.append(f"dikerjakan {HARI[d.weekday()]} {d.isoformat()} (= T+{(d - tgl).days})")
        if dijual:
            cat.append("TUNDA: dilarang sebelum izin edar terbit; mulai hanya setelah izin terbit")
        if hari_ini and d < hari_ini:
            cat.append("LEWAT: kerjakan secepatnya atau padatkan jadwal")
        baris.append({"tanggal": d.isoformat(), "hari": HARI[d.weekday()],
                      "t": ("T%+d" % off) if off else "T0", "fase": fase, "bidang": kanal,
                      "tugas": tugas, "catatan": "; ".join(cat), "selesai": ""})
    baris.sort(key=lambda r: (r["tanggal"], int(r["t"][1:]), r["fase"], r["bidang"]))
    return baris


def peringatan(tgl, hari_ini=None, ekstra=None, izin="sudah", izin_terbit=None, jenis="lain"):
    w = []
    if izin == "belum":
        w.append("IZIN EDAR BELUM TERBIT: dilarang menjual, menerima pre-order/DP, atau mempromosikan sambil menerima pesanan sebelum izin terbit "
                 "(kosmetik: notifikasi BPOM; pangan olahan: PIRT/BPOM MD; obat/suplemen/alat kesehatan: izin edar BPOM/Kemenkes). "
                 "Yang boleh sekarang: riset, daftar tunggu TANPA pembayaran, persiapan konten/aset. T0 harus sesudah izin terbit. "
                 "Dasar umum: UU Kesehatan dan peraturan BPOM tentang izin edar; cek ke BPOM/Dinkes; nomor peraturan sengaja tidak disebut (verifikasi sendiri di situs resmi).")
        if izin_terbit is None:
            w.append("Perkiraan tanggal izin terbit belum diisi (--izin-terbit): T0 di jadwal ini hanya KANDIDAT dan wajib digeser setelah izin benar-benar terbit.")
    ekstra = ekstra or {}
    tahun = sorted({(tgl + timedelta(days=o)).year for o in (-30, 30)})
    kurang = [y for y in tahun if y not in TAHUN_DATA]
    if kurang:
        w.append(f"Daftar libur nasional untuk {', '.join(map(str, kurang))} belum ada di skill ini (jadwal T-30..T+30 menyentuh tahun itu); "
                 "hanya hari Minggu yang dianggap libur di tahun tersebut. Cek SKB terbaru.")
    lebaran = sorted(date.fromisoformat(k) for k, v in LIBUR.items() if "Idulfitri" in v)
    if lebaran:
        awal, akhir = tgl - timedelta(days=7), tgl + timedelta(days=7)
        for y in sorted({d.year for d in lebaran}):
            ly = [d for d in lebaran if d.year == y]
            if awal <= max(ly) + timedelta(days=5) and akhir >= min(ly) - timedelta(days=7):
                w.append(f"Peluncuran (T-7..T+7) bersinggungan dengan Lebaran/cuti bersama Idulfitri {y} "
                         f"({min(ly).isoformat()} s.d. {max(ly).isoformat()}) dan musim mudik/arus balik: pemasok, pabrik, dan ekspedisi bisa libur "
                         "atau lambat sekitar 1 minggu, harga bahan bisa naik, pembeli sibuk mudik. Majukan pesanan bahan/kemasan, "
                         "tetapkan tanggal kirim terakhir sebelum libur, atau pertimbangkan geser peluncuran.")
    n = libur_nama(tgl, ekstra)
    if n:
        w.append(f"Tanggal peluncuran jatuh di {n}: pemasok/kurir bisa libur; pastikan stok dan kemasan siap sehari sebelumnya.")
    for bln, hr in KEMBAR:
        try:
            k = date(tgl.year, bln, hr)
        except ValueError:
            continue
        if abs((tgl - k).days) <= 2:
            w.append(f"Dekat tanggal kembar {hr}.{bln} (marketplace): biaya iklan dan persaingan biasanya naik; pertimbangkan geser, atau manfaatkan sebagai momen.")
    if hari_ini:
        sisa = (tgl - hari_ini).days
        if sisa < 0:
            w.append("Tanggal peluncuran sudah lewat.")
        elif sisa < 30:
            w.append(f"Waktu tersisa {sisa} hari (<30): tugas sebelum hari ini ditandai LEWAT; padatkan atau geser peluncuran.")
    return w


def teks_md(produk, tgl, jenis, baris, warn):
    o = [f"# Jadwal peluncuran: {produk}", "",
         f"- Tanggal peluncuran (T0): **{HARI[tgl.weekday()]}, {tgl.isoformat()}**",
         f"- Jenis produk: {jenis}", f"- Jumlah tugas: {len(baris)}", ""]
    if warn:
        o.append("## Perhatian")
        o += [f"- {x}" for x in warn]
        o.append("")
    tgl_now = None
    for r in baris:
        if r["tanggal"] != tgl_now:
            tgl_now = r["tanggal"]
            o += ["", f"### {r['hari']}, {r['tanggal']}" + (" (T0)" if r["t"] == "T0" else "")]
        c = f" _({r['catatan']})_" if r["catatan"] else ""
        o.append(f"- [ ] **{r['t']}** [{r['fase']} | {r['bidang']}] {r['tugas']}{c}")
    o += ["", "Catatan: jadwal libur dari SKB 2026/2027 dan bisa berubah; label/izin hanya pengingat, cek situs resmi instansi."]
    return "\n".join(o) + "\n"


def main(argv=None):
    p = argparse.ArgumentParser(description="Jadwal peluncuran produk T-30..T+30")
    p.add_argument("--tanggal", required=True, help="tanggal peluncuran TTTT-BB-HH")
    p.add_argument("--produk", default="Produk baru")
    p.add_argument("--jenis", choices=["pangan", "kosmetik", "lain", "jasa"], default="lain",
                   help="pangan = makanan/minuman (tambah cek PIRT/BPOM/halal); kosmetik; jasa (tanpa tugas stok/kemasan/kirim); lain")
    p.add_argument("--hari-ini", help="TTTT-BB-HH; bawaan = hari ini (date.today()); tandai tugas yang sudah lewat")
    p.add_argument("--libur-tambahan", default="", help="tanggal libur/tutup tambahan: 2026-11-20,2026-11-21")
    p.add_argument("--format", choices=["md", "csv", "json"], default="md")
    p.add_argument("--izin", choices=["sudah", "belum", "tidak-wajib"], default="sudah",
                   help="status izin edar (notifikasi BPOM/PIRT/BPOM MD/izin obat-alkes); 'belum' = tunda penjualan, pre-order, promo sampai izin terbit")
    p.add_argument("--izin-terbit", help="perkiraan tanggal izin terbit TTTT-BB-HH; T0 digeser ke minimal 7 hari sesudahnya")
    p.add_argument("--ringkas", action="store_true", help="versi ringkas (tugas kunci saja); dipakai bila rencana >43 tugas")
    a = p.parse_args(argv)
    try:
        tgl = parse_tanggal(a.tanggal)
        hi = parse_tanggal(a.hari_ini) if a.hari_ini else date.today()
        ekstra = {}
        for x in filter(None, (s.strip() for s in a.libur_tambahan.split(","))):
            ekstra[parse_tanggal(x).isoformat()] = "libur tambahan (dari pengguna)"
        it = parse_tanggal(a.izin_terbit) if a.izin_terbit else None
    except ValueError as e:
        print(f"Galat: {e}", file=sys.stderr)
        return 2
    geser_t0 = None
    if a.izin == "belum" and it and tgl < it + timedelta(days=7):
        geser_t0 = (tgl, it + timedelta(days=7))
        tgl = geser_t0[1]
    baris = bangun(tgl, a.jenis, ekstra, hi, a.izin, a.ringkas)
    warn = peringatan(tgl, hi, ekstra, a.izin, it, a.jenis)
    if geser_t0:
        warn.insert(1, f"T0 digeser dari {geser_t0[0].isoformat()} ke {geser_t0[1].isoformat()} (izin terbit {it.isoformat()} + 7 hari persiapan).")
    if a.format == "json":
        print(json.dumps({"produk": a.produk, "t0": tgl.isoformat(), "peringatan": warn, "tugas": baris},
                         ensure_ascii=False, indent=2))
    elif a.format == "csv":
        buf = io.StringIO()
        w = csv.DictWriter(buf, fieldnames=list(baris[0].keys()))
        w.writeheader()
        w.writerows(baris)
        sys.stdout.write(buf.getvalue())
        for x in warn:
            print(f"# PERHATIAN: {x}", file=sys.stderr)
    else:
        sys.stdout.write(teks_md(a.produk, tgl, a.jenis, baris, warn))
    return 0


if __name__ == "__main__":
    sys.exit(main())
