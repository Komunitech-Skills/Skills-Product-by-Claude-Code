# HASIL UJI — arsip-nota v1.0.0

Penguji: agen independen (bukan pembuat skill), hanya membaca folder `skills/arsip-nota/`. Tanggal uji: 26 September 2026.
Lingkungan uji: folder sementara terpisah dari repo (`.../scratchpad/rt-arsip/`), data seluruhnya fiktif.

## Ringkasan pengujian
1. Audit kode `scripts/arsip.py` (1012 baris): hanya modul standar (`argparse, csv, hashlib, json, os, re, shutil, sqlite3, sys, decimal, pathlib`). **Tidak ditemukan** perintah destruktif tersembunyi, pengiriman data keluar (tidak ada `socket`/`requests`/`urllib`/`http`), pembacaan kredensial/SSH key/browser data, pola unduh-lalu-jalankan-langsung, kode ter-obfuscate, atau instruksi tersembunyi mencurigakan di SKILL.md/README. Tidak ada API key/token tertanam. **Aman dijalankan.**
2. Tes regresi bawaan (`tests/uji_regresi.py`, 44 skenario) — **SEMUA LULUS**.
3. `python3 scripts/validate.py --skill arsip-nota` — **lulus** (1 skill valid, katalog sesuai).
4. 3 skenario normal (warung 10 foto, toko bangunan faktur PDF, freelancer struk bensin/ojek) — lihat `examples/01`(punya pembuat)`, 03, 04`. Total nominal diverifikasi independen dengan penjumlahan manual (setara `Decimal`) di ketiganya: **cocok persis** dengan output script (2.422.500 / 15.500.000 / 102.500).
5. 1 skenario input tidak lengkap (tanggal & nominal kosong, flag wajib hilang) — `examples/05` — selalu gagal bersih, tidak pernah menulis data salah.
6. 1 skenario luar cakupan (minta OCR otomatis, minta hapus nota lama) — `examples/05` — struktural tidak bisa dijalankan (tidak ada perintah untuk itu), sesuai batasan SKILL.md.
7. Data rusak (nama file emoji/karakter Windows terlarang, file 0 byte, duplikat hash sama beda nama, tanggal tidak ada di kalender, tanggal masa depan, 4 varian nominal format Indonesia, folder `--db` belum ada, DB rusak/teks biasa, DB 0 byte) — `examples/06` — 7/8 kelompok kasus lulus penuh, 1 temuan sedang (lihat di bawah).
8. Ekspor CSV → impor nyata ke `kas-umkm` di database sementara terpisah — `examples/07` — **berhasil tanpa error**, 10 baris, Rp 2.422.500, angka cocok di kedua sisi setelah dihitung ulang independen.
9. Uji A/B tanpa skill vs dengan skill — `examples/00-pembanding-tanpa-skill.md` — skill memberi nilai tambah jelas (nominal selalu tepat karena diparser & dijumlah SQL, bukan dikira manual; nama file konsisten; file asli aman; bisa dicari ulang).
10. Uji banding pesaing (ComposioHQ `invoice-organizer` & sejenis, dinilai dari deskripsi publik, tidak disalin) — `examples/00-banding-pesaing.md` — arsip-nota unggul di lokalisasi Indonesia, deteksi duplikat berbasis hash yang pasti, dan integrasi nyata teruji ke `kas-umkm`; pesaing unggul di satu hal (OCR terintegrasi dalam satu skill, di luar cakupan arsip-nota by design).
11. `scripts/uji_openclaw.sh` **tidak dijalankan** sesuai instruksi tugas.

## Skor kualitas: **8 / 10**

**Alasan:**
- (+) Keamanan data sangat baik: tidak pernah menghapus file, wajib pratinjau sebelum tulis, deteksi duplikat berbasis hash yang bisa diverifikasi ulang, backup otomatis sebelum tulis pertama per hari, pesan error selalu berisi langkah pemulihan.
- (+) Perhitungan uang benar & teruji: parser nominal format Indonesia (`1.250.000`, `Rp 45rb`, `4,5jt`, desimal dengan pembulatan `ROUND_HALF_UP`) diverifikasi independen dan selalu tepat; totalisasi lewat SQL `SUM()`, bukan dikira-kira agent.
- (+) Integrasi lintas skill (ekspor → `kas-umkm impor`) terbukti berfungsi nyata, bukan cuma diklaim di dokumentasi.
- (+) Penanganan nama file lintas OS (karakter terlarang Windows, nama terlarang `CON`/`PRN`, emoji di file sumber) tangguh — dibuktikan lulus di kasus ekstrem.
- (+) Uji A/B dan uji banding pesaing menunjukkan nilai tambah nyata, bukan generik.
- (−) **Temuan sedang:** field `mode` pada respons `tambah` yang diblokir `perlu_izin` (duplikat persis) berbunyi `"tersimpan"` walau `--ya` disertakan padahal tidak ada apa pun yang benar-benar tersimpan (tidak ada `id` baru, file tidak disalin, jumlah nota tidak bertambah — diverifikasi langsung). Berisiko menyesatkan agent yang hanya membaca `mode` tanpa memeriksa `perlu_izin`; dampak dimitigasi oleh instruksi eksplisit SKILL.md (wajib cek `perlu_izin` & tanya dulu), tapi tetap bug di kode yang sebaiknya diperbaiki sebelum rilis (bukan blocker fatal, karena tidak pernah benar-benar menyimpan data salah — hanya label status yang keliru).
- (−) **Temuan rendah:** kamus kata kunci tebak-kategori (`KATEGORI`) condong ke usaha kuliner/sembako (kata kunci `bahan-baku` seperti "sembako", "grosir") dan tidak mencakup istilah umum usaha lain yang disebut eksplisit di skenario uji: toko bangunan ("semen", "cat", "bangunan" tidak ada di kata kunci manapun → jatuh ke Lain-lain) dan BBM freelancer (nama vendor nyata "SPBU"/"Pertamina" tidak ada di kata kunci `transportasi`, hanya kata generik "bensin"/"bbm"). Bukan kesalahan data (nominal/tanggal tetap benar, dan SKILL.md sudah mewajibkan menyampaikan baris "Asumsi" agar bisa dikoreksi pengguna), tapi mengurangi akurasi rekap otomatis untuk sektor non-kuliner.
- Skor tidak lebih rendah karena kedua temuan tidak menyebabkan kehilangan data, tidak menyebabkan penghapusan file, dan selalu bisa dikoreksi lewat mekanisme yang sudah ada (`--izinkan-duplikat` yang tetap ditanyakan lewat `perlu_izin`, `--kategori` manual).

## Temuan (ringkas per tingkat)
| Tingkat | Temuan | Lokasi |
|---|---|---|
| Sedang | `mode: "tersimpan"` keliru pada jalur `perlu_izin` duplikat + `--ya` (tidak ada yang benar-benar tersimpan) | `scripts/arsip.py` fungsi `cmd_tambah`, baris ±633; dibuktikan di `examples/06` bagian 3 |
| Rendah | Kata kunci tebak kategori tidak mencakup istilah toko bangunan (semen, cat, bangunan) dan BBM bermerek (SPBU, Pertamina) | `scripts/arsip.py` konstanta `KATEGORI`; dibuktikan di `examples/03` dan `examples/04` |
| Rendah (bukan cacat) | Foto yang sama difoto ulang dengan kompresi/kualitas berbeda tidak terdeteksi hash sama — sudah didokumentasikan sendiri di SKILL.md bagian Batasan, dan tertangani sebagian lewat `duplikat` (kemungkinan-dobel by tanggal+vendor+nominal). Tidak diuji ulang karena sudah diakui dokumentasi. | SKILL.md bagian "Batasan & penanganan error" |

## Rekomendasi
1. **Perbaiki** label `mode` pada jalur `perlu_izin` di `cmd_tambah` agar tidak pernah bernilai `"tersimpan"` kecuali data benar-benar ditulis ke indeks.
2. **Pertimbangkan** menambah kata kunci kategori untuk sektor non-kuliner (mis. toko bangunan: semen, cat, bata, paku, besi; BBM: spbu, pertamina, shell, bp — untuk `transportasi`), atau cukup catat sebagai batasan yang jelas di SKILL.md kalau tidak ingin diperluas sekarang.
3. Tidak ada temuan yang menghalangi status `lulus` — kedua temuan bersifat perbaikan kualitas, bukan blocker keamanan/kebenaran data.
