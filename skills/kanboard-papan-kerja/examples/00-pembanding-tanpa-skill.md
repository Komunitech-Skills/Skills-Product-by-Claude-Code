# Uji A/B — tanpa skill vs dengan skill (skenario normal pertama: papan produksi konveksi)

**Penguji:** agent penguji independen (Claude Code), 2026-09-30, terhadap **Kanboard v1.2.54 asli** milik penguji (lihat `06-uji-konveksi-produksi.md`), data yang sama.
**Jujur soal metode:** sisi "tanpa skill" **tidak** dijalankan oleh sesi agent terpisah; penguji menjalankan pendekatan yang lazim dipakai agent umum yang hanya tahu dokumentasi API Kanboard: `curl` JSON-RPC dengan token aplikasi yang ditempel, metode bawaan `createProject`, `getOverdueTasks`/`getMyOverdueTasks`, tanggal dikirim apa adanya, dan "hari ini" dari jam lokal mesin (UTC). Semua perintah di bawah dijalankan sungguhan ke Kanboard yang sama.

## Permintaan
> "Buatkan papan produksi untuk Konveksi Mekar Jaya, isi order-order ini (seragam SD tenggat 02/10 jam 10.00, dst.), lalu kasih laporan yang telat, jatuh tempo hari ini, dan yang macet."

## A. Tanpa skill (hasil nyata)
```
## Tanpa skill: pendekatan umum agent (curl JSON-RPC + metode bawaan getOverdueTasks / getMyOverdueTasks)
getOverdueTasks (token aplikasi) jumlah: 11
 - 2 Kaos panitia 17-an 50 pcs | proyek Produksi Konveksi Mekar Jaya | date_due 1790755200
 - 8 Mukena 15 pcs | proyek Produksi Konveksi Mekar Jaya | date_due 1790722800
 - 9 Jaket himpunan 40 pcs | proyek Produksi Konveksi Mekar Jaya | date_due 1790571600
 - 10 Topi event lari 100 pcs | proyek Produksi Konveksi Mekar Jaya | date_due 1790503200
 - 14 ORD-1001 Bu Rahma - 3 pashmina | proyek Order Toko Hijab Nadia | date_due 1790690400
 - 15 ORD-1002 Kak Sinta - bergo 2 | proyek Order Toko Hijab Nadia | date_due 1790762400
 - 17 ORD-1004 Pak Anton - retur salah warna | proyek Order Toko Hijab Nadia | date_due 1790744400
 - 18 ORD-1000 Bu Dewi - diterima | proyek Order Toko Hijab Nadia | date_due 1790676000
 - 19 ORD-1005 Ibu Yani - gamis (tenggat diisi di layar) | proyek Order Toko Hijab Nadia | date_due 1790773075
 - 20 Feed IG Klinik Gigi Ceria (9 post) | proyek Proyek Studio Desain Kirana | date_due 1790758800
 - 22 Company profile CV Bangun | proyek Proyek Studio Desain Kirana | date_due 1790769600
getMyOverdueTasks (sari): []
## Tanpa skill: hitung "hari ini" dengan tanggal lokal mesin (UTC) pada jam 01:00 WIB 1 Okt (=30 Sep 18:00 UTC)
naif (tanggal UTC) 'hari ini' papan 1: [(2, 'Kaos panitia 17-an 50 pcs'), (3, 'Batik PDH Kelurahan 35 pcs'), (5, 'Rompi proyek 80 pcs'), (7, 'Kemeja kantor 10 pcs')]
## Tanpa skill: createProject default -> kolom bawaan
{"jsonrpc":"2.0","result":4,"id":1}
['Backlog', 'Ready', 'Work in progress', 'Done']
{"jsonrpc":"2.0","result":true,"id":1}
## Tanpa skill: date_due "02/10/2026 10:00" (format Indonesia DD/MM) dikirim apa adanya
{"jsonrpc":"2.0","result":28,"id":1}
tersimpan sbg 2026-02-10 17:00:00+07:00
{"jsonrpc":"2.0","result":true,"id":1}
```
Masalah yang terlihat:
1. **Token:** agent umum meminta alamat + token ditempel di chat, dan cenderung memakai token aplikasi `jsonrpc` (akses penuh ke semua papan, `getOverdueTasks` hanya jalan dengan token ini).
2. **Papan:** `createProject` menghasilkan kolom bawaan bahasa Inggris `Backlog / Ready / Work in progress / Done` — tidak sesuai alur konveksi; agent harus mengarang kolom sendiri tanpa batas WIP.
3. **Tanggal salah fatal:** `"02/10/2026 10:00"` (gaya Indonesia) disimpan Kanboard sebagai **10 Februari 2026** 17:00 WIB (dibaca m/d/Y, jam dalam zona server UTC).
4. **Terlambat salah:** `getOverdueTasks` = 11 kartu, termasuk #10 "Topi event lari" dan #18 "Bu Dewi - diterima" yang sudah di kolom **Selesai/Diterima**; epoch mentah tanpa tanggal terbaca; `getMyOverdueTasks` untuk akun pribadi = `[]` (hanya kartu yang ditugaskan ke dirinya).
5. **"Hari ini" salah di batas malam:** pada 1 Okt 01:00 WIB, tanggal UTC mesin masih 30 Sep → daftar #2, #3, #5, #7 (dua sudah kemarin, #11 yang benar-benar hari ini hilang).
6. **Macet:** tidak ada konsep bawaan; harus menulis kode sendiri dari `date_moved`.
7. **Keamanan:** tidak ada pratinjau/konfirmasi, tidak ada penolakan hapus (API yang sama bisa `removeProject` — penguji memakainya untuk membersihkan papan uji A/B), tidak ada allowlist host.

## B. Dengan skill (hasil nyata, `06-uji-konveksi-produksi.md`)
- Papan 6 kolom sesuai alur konveksi (Order Masuk → … → Selesai, Produksi batas 5), dibuat setelah pratinjau + `--ya`; nama ganda ditolak.
- Tenggat "Jumat jam 10:00" → 2 Okt 10:00 WIB, tersimpan benar di server UTC (03:00 UTC) maupun Asia/Jakarta; PIC dicocokkan dengan anggota papan.
- Laporan satu pesan siap Telegram: terlambat 3 / hari ini 3 / macet 3 — **semua cocok** dengan hitungan ulang independen di 3 zona (WIB/WITA/WIT) × 2 zona server × 2 akun (`verifikasi.txt`, 12/12 COCOK); kolom terakhir tidak dihitung terlambat/macet; batas tengah malam WIB benar.
- Token tidak pernah ditempel/ditampilkan; metode hapus terkunci.

## Kesimpulan
Dengan skill **jelas lebih baik**: angka benar (tanpa skill: 11 "terlambat" dari `getOverdueTasks`, padahal yang benar 9 — skill dengan token aplikasi yang sama juga menghitung 9, selisihnya 2 kartu di kolom Selesai/Diterima; tanggal 02/10 jadi Februari), papan langsung sesuai usaha, dan jauh lebih aman. Catatan jujur: skill masih bisa salah jam bila pengguna menulis "jam 3 sore" (→ 03:00) — lihat HASIL-UJI.
