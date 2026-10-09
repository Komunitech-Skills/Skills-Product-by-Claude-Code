# Uji 05: input tidak lengkap, di luar cakupan, dan data rusak (penguji independen, 2026-09-29)

## Skenario 4 - input tidak lengkap
**Input:** "min, bulan depan aku mau launching produk baru nih, bantuin ya"

**Jawaban agen (mengikuti bagian Input SKILL.md, satu pesan):**
> Siap bantu! Supaya rencananya pas, jawab singkat ya (boleh nomornya saja):
> 1) Produknya apa & harga normalnya?
> 2) Tanggal pasti launching bulan depan (mis. 7 November), atau "secepatnya"?
> 3) Jenisnya: makanan/minuman, kosmetik/perawatan, atau lainnya?
> 4) Kanal yang sudah ada: kira-kira berapa kontak WA, pengikut IG/TikTok, dan punya toko marketplace?
> 5) Anggaran promo + iklan (boleh Rp 0)?
> Opsional: stok awal & kapan barang siap, target pesanan.
> Kalau mau langsung jalan, balas "pakai default": aku anggap produk non-makanan, tanggal 3 November 2026 (35 hari dari hari ini), dan hanya kanal gratis - asumsinya kutulis di awal rencana.

**Lanjutan (pengguna: "pakai default"):** agen menjalankan `--tanggal 2026-11-03 --jenis lain --hari-ini 2026-09-29` -> 39 tugas, T0 Selasa 3 Nov 2026, T-30 Minggu 4 Okt (tugas strategi/harga, tidak digeser karena bukan tugas hari kerja), T-28 Selasa 6 Okt pemasok. Bagian Asumsi ditulis paling atas. Tanggal 35 hari = 29 Sep + 35 = 3 Nov (benar).
**Vonis:** LULUS. Satu pesan, daftar pendek, ada jalan pintas default. Catatan: pengguna bilang "bulan depan" - agen yang baik memakai 35 hari (masih bulan depan); skill tidak mengatur penafsiran kata relatif, tetapi default-nya kebetulan cocok.

## Skenario 5 - di luar cakupan
**Input:** "Tolong bikin rencana launching aplikasi kasir SaaS saya di Product Hunt, plus hitung valuasi buat investor."

**Jawaban agen:**
> Skill ini khusus peluncuran produk fisik/jasa UMKM (WA, marketplace, IG/TikTok, bazar), jadi peluncuran aplikasi/SaaS di Product Hunt dan valuasi investor di luar cakupannya - saya tidak akan memaksakan jadwal UMKM ke sana. Untuk valuasi dan dokumen investor, sebaiknya dengan konsultan keuangan/penasihat hukum. Kalau aplikasi kasirmu juga dijual ke toko-toko lewat demo langsung, bazar UMKM, atau komunitas WA pedagang, bagian itu bisa saya bantu buatkan jadwal bertanggal dan pesan siap tempelnya.
**Vonis:** LULUS. Menolak dengan sopan, tidak mengarang, menawarkan bagian yang masih relevan. Sesuai "Kapan TIDAK digunakan".

## Uji script dengan data rusak dan kasus tepi
Semua dijalankan nyata dengan `python3 -B scripts/jadwal_peluncuran.py`.

| Input | Hasil | Vonis |
|---|---|---|
| `--tanggal 2026-02-30` | `Galat: tanggal '2026-02-30' tidak valid; pakai format TTTT-BB-HH, mis. 2026-11-14`, kode 2 | benar |
| `--tanggal ""` / `14-11-2026` / `2026/11/14` | Galat, kode 2 | benar |
| `--tanggal 2026-1-5` / `" 2026-11-14 "` | diterima (5 Jan / 14 Nov) | wajar, toleran |
| `--hari-ini kemarin` | Galat, kode 2 | benar |
| `--libur-tambahan "2026-11-13,,2026-11-12 "` (T0 14 Nov) | isian kosong diabaikan; stok T-2 (Kam 12 Nov, ditutup) mundur ke Rabu 11 Nov | benar |
| T0 di libur: `2026-12-25` | Perhatian: "Tanggal peluncuran jatuh di Natal: pemasok/kurir bisa libur..." | benar |
| T0 di Idulfitri: `2026-03-21` | peringatan Idulfitri; T-2 stok (Kamis 19 Mar Nyepi, Rabu 18 cuti) mundur ke Selasa 17 Mar; T+1 kirim (Minggu 22) maju ke Rabu 25 Mar (lewat 23-24 cuti bersama) | tanggal benar; tetapi tidak ada peringatan khusus musim Lebaran (ekspedisi/pemasok libur ±1 minggu, harga bahan naik) - hanya pesan umum |
| Waktu pendek: `--tanggal 2026-10-10 --hari-ini 2026-09-29` | "Waktu tersisa 11 hari (<30)", 13 tugas bertanda LEWAT, plus peringatan tanggal kembar 10.10 | benar |
| Waktu pendek TANPA `--hari-ini` | tidak ada peringatan waktu pendek, tidak ada tanda LEWAT | **bug kegunaan**: perintah utama di SKILL.md langkah 5 tidak memakai `--hari-ini`, dan script tidak memakai tanggal hari ini sebagai bawaan |
| Tanggal sudah lewat: `2026-09-01 --hari-ini 2026-09-29` | "Tanggal peluncuran sudah lewat." | benar |
| `2028-03-01` | peringatan "Daftar libur nasional untuk 2028 belum ada" | benar |
| `2027-12-20` (T+30 = 19 Jan 2028) | tidak ada peringatan, padahal tugas Jan 2028 dihitung tanpa data libur 2028 | bug kecil: peringatan hanya memeriksa tahun T0, bukan rentang T-30..T+30 |
| `--format csv` untuk 2026-11-10 | CSV di stdout, peringatan 11.11 ke stderr dengan awalan `# PERHATIAN` | benar |
| `tests/uji_regresi.py` | 10 tes OK | benar |

Tampilan md: bila tugas hasil geser jatuh di tanggal yang sama dengan tugas lain, judul tanggal memakai label T dari tugas pertama (mis. tugas bazar T-5 yang digeser tampil di bawah "Jumat, 2027-01-08 (T-7)"). Tanggalnya benar, label T-nya menyesatkan sedikit; catatan "digeser dari ..." tetap menjelaskan.
