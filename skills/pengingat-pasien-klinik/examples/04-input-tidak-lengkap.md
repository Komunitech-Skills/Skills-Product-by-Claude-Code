# Skenario 04 (input tidak lengkap)

**Input pengguna:** "Catat pasien baru dong, kontrol minggu depan."

Tidak ada: nama panggilan, nomor WA, dan **tidak ada pernyataan persetujuan**. Sesuai SKILL.md
("Jika info wajib kurang, tanyakan sekali dalam satu pesan bernomor, termasuk pertanyaan
persetujuan. Jangan pernah mengasumsikan persetujuan 'ya'"), respons agent yang benar:

> Baik, sebelum saya catat, mohon lengkapi (jawab dalam satu pesan boleh sekaligus):
> 1. Nama panggilan pasiennya siapa (atau nama hewan + nama pemilik)?
> 2. Nomor WA yang bisa dihubungi berapa?
> 3. "Kontrol" apa — kontrol gigi, kontrol umum, kontrol pasca operasi, dll (sebutkan jenis
>    kunjungan saja, bukan nama penyakit)?
> 4. Tanggalnya "minggu depan" itu tanggal berapa persisnya, atau hari apa?
> 5. Apakah pasien ini sudah setuju dihubungi lewat WA untuk pengingat jadwalnya?

**Uji tambahan — coba jalankan dengan field kosong (mensimulasikan agent yang tetap memaksa
menjalankan tanpa bertanya):**
```bash
$ python3 scripts/pengingat_pasien.py --hari-ini 2026-09-26 tambah --nama "" \
    --wa "" --jenis "kontrol" --tanggal "minggu depan" --persetujuan ya
```
```
ERROR: --nama kosong. Isi nama panggilan pasien, mis. "Bu Sari".
```
(exit code 1)

Script gagal cepat dan jelas menyebut kolom mana yang kosong — konsisten dengan aturan
"tanyakan sekali", bukan menebak nama/WA yang tidak ada. Catatan kecil: pesan error hanya
menunjuk kolom `--nama` yang gagal duluan (argparse/validasi berurutan); `--wa` kosong akan
tertangkap di panggilan berikutnya setelah `--nama` diisi — bukan masalah karena agent tetap
wajib menanyakan **semua** field wajib sekaligus di awal per SKILL.md, bukan bergantung urutan
pesan error script. Lulus (dengan catatan kecil ini, tidak memengaruhi keamanan/privasi).
