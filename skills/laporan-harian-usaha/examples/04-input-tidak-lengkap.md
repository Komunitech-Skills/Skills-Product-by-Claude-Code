# 04 — Input tidak lengkap: belum ada alat terpasang

**Input pengguna:** `kirim laporan harian dong`

(Komputer baru. Tidak ada kasir.db, stok.db, absensi.db, atau pengingat/DAFTAR.csv di lokasi default. HOME kosong.)

**Langkah agent sesuai SKILL.md:** "Tidak perlu bertanya apa pun untuk laporan pertama: langsung jalankan." Agent menjalankan `scripts/laporan.py`, dan hasilnya:

```
LAPORAN HARIAN USAHA
Kamis, 24 September 2026
Dibuat 2026-09-24 21:00 WIB

PENJUALAN
Belum ada data (kasir-lokal belum dipakai di komputer ini).

STOK
Belum ada data (buku-stok belum dipakai di komputer ini).

KEHADIRAN
Belum ada data (absensi-lokal belum dipakai di komputer ini).

TAGIHAN & FOLLOW-UP
Belum ada data (pengingat-follow-up belum dipakai di komputer ini).

PERLU PERHATIAN
1. Belum ada data dari alat mana pun (kasir-lokal, buku-stok, absensi-lokal, pengingat-follow-up). Jika alatnya sudah dipakai di lokasi lain, beri tahu lokasinya (opsi --kasir-db, --stok-db, --absensi-db, --pengingat).

Sumber: belum ada alat terbaca (hanya dibaca).
```

**Balasan agent** (langkah A.2: bagian "Belum ada data" dijelaskan, lalu tanya lokasi. Satu pesan, tanpa mengirim kerangka kosong berulang):

> Laporan belum bisa berisi angka karena di komputer ini saya belum menemukan data dari alat Komunitech mana pun.
> Supaya laporannya terisi, mohon jawab singkat:
> 1. Alat apa yang sudah Bapak/Ibu pakai? (Kasir Lokal / Buku Stok / Absensi Lokal / Pengingat Follow-up)
> 2. Kalau sudah dipakai, datanya disimpan di folder mana? (mis. `D:\DataToko` atau flashdisk). Kalau tidak tahu, cukup jawab "default".
> 3. Laporannya mau dikirim ke Telegram tiap malam? Jam berapa? (default 21.00 WIB)
>
> Kalau belum memakai alat apa pun: laporan ini butuh minimal satu alat, misalnya Kasir Lokal untuk penjualan. Untuk data dari Moka/Majoo/Excel, pakai skill Rekap Penjualan CSV.

**Catatan penguji**
- Script menangani kasus ini dengan benar: kode keluar 0, tidak ada angka karangan, dan butir "Belum ada data dari alat mana pun" menunjuk opsi lokasi.
- Pertanyaan diajukan sekali dalam satu pesan ✔. Isi pertanyaan disusun penguji dari langkah A.2 dan C. SKILL.md tidak punya aturan eksplisit untuk kasus **semua** bagian kosong, dan instruksi A.1 "Kirim `teks` apa adanya" bisa membuat agent mengirim kerangka kosong ini. Lebih berbahaya lagi pada jadwal Pilihan 1 (tanpa AI): kerangka kosong akan terkirim ke Telegram setiap malam (RINGAN–SEDANG).
- Argumen buruk ditangani ramah: `--tanggal besok` → "tidak dikenali", `2026-09-30` → "belum terjadi", `31/02/2026` → "tidak ada di kalender", zona salah → daftar pilihan WIB/WITA/WIT. Semua keluar dengan kode 2.
