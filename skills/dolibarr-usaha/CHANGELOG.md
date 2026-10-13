# Riwayat perubahan — dolibarr-usaha

Catatan teknis per versi.

## Catatan revisi 1.0.12 (2026-10-02)
- Aturan baru di SKILL.md: bila pengguna menempel kunci/token/password di chat, agent tidak boleh menulis ulang satu karakter pun darinya (tidak utuh, tidak awalan, tidak disamarkan) dan cukup menyebut "kunci yang Anda tempel".

## Catatan revisi 1.0.11 (2026-10-02)
- Bagian "ATURAN WAJIB" di awal SKILL.md (temuan uji OpenClaw): pesan untuk pelanggan hanya berupa draf teks, agent dilarang menawarkan "kirim langsung" lewat WA/email/Telegram, setiap draf ditutup kalimat baku "Draf di atas siap Anda salin dan kirim sendiri lewat WA.", file CSV wajib diolah dengan `piutang-csv`, dan keluaran script ditempel apa adanya.
- `piutang-csv` kini mencetak baris "Sumber: file CSV ekspor ..." dan kalimat draf-saja di akhir. Uji regresi bertambah.

## Catatan revisi 1.0.10 (2026-10-02)
- Perintah baru `piutang-csv`: membaca file CSV ekspor invoice Dolibarr (tanpa koneksi dan tanpa kunci API) dan menghitung umur piutang lewat script. Judul kolom Indonesia/Inggris dikenali, pemisah otomatis, baris rusak ditulis sebagai DILEWATI.
- Larangan kirim langsung ke pelanggan diperjelas: tagihan/pengingat hanya draf yang dikirim sendiri oleh pemilik atau staf. Uji regresi menjadi 98 tes.

## Catatan revisi 1.0.9 (2026-10-01)
- Petunjuk lokasi script ditambahkan di SKILL.md: script ada di subfolder `scripts/` di folder skill. Agent dilarang mencari script atau file pengguna ke seluruh disk (mis. `find /`).

## Catatan revisi 1.0.8 (2026-09-29)
- Pengaman: singkatan opsi baris perintah tidak lagi diterima (mis. `--y` tidak bisa dibaca sebagai `--ya`), sehingga konfirmasi tidak terpicu tanpa sengaja. Ditambah uji regresi.

## Catatan revisi 1.0.7 (2026-09-29)
- Baris "Aturan kerja" ditambahkan di SKILL.md: agent tidak boleh memasang paket/aplikasi sendiri, tidak membuka atau mencari file di luar yang diberikan pengguna, dan hasil yang ditulis ke file harus disebut lokasinya (folder kerja, bukan `/tmp`).

## Catatan revisi 1.0.6 (2026-09-29)
- Aturan kredensial & jadwal (SKILL.md dan `references/openclaw-jadwal.md`): agent tidak pernah mencari, membaca, atau menampilkan token/API key dari environment, file konfigurasi, atau riwayat. Jadwal hanya dibuat setelah pengguna membalas "ya" atas perintah dan jam yang ditunjukkan.

## Catatan revisi 1.0.5 (2026-09-25)
- Galat server 5xx atau jawaban yang terpotong saat MENULIS ke Dolibarr kini dilaporkan sebagai kode keluar 8 ("data MUNGKIN SUDAH TERSIMPAN, periksa dulu, jangan langsung mengulang"), bukan galat biasa.
- Draf kosong milik perintah lain tidak lagi menahan pembuatan draf baru; pesan penahan menyebut jenis drafnya. Judul halaman galat dari proxy tidak lagi tercetak dua kali.

## Catatan revisi 1.0.4 (2026-09-25)
- Pembuatan draf invoice aman bila koneksi putus atau timeout di tengah jalan: kode keluar baru 8 ("tidak pasti"), tiap draf diberi kode perintah di catatan privatnya, dan pembuatan ulang ditahan (kode 7) bila ada draf kosong atau sebagian dari perintah yang sama. Pesan menjelaskan apa yang harus dicek di Dolibarr.

## Catatan revisi 1.0.3 (2026-09-25)
- Pencegah draf invoice ganda kini mengenali draf kembar walau ada baris bersen (diskon, harga ,50), karena Dolibarr menyimpan total per baris dengan 2 desimal. Hitungan DPP/PPN Komunitech tidak berubah.
- `--kunci-file` kini selalu mengalahkan variabel lingkungan `DOLIBARR_API_KEY`, dengan peringatan bila keduanya ada; file kunci yang tidak ada atau kosong ditolak (kode 5).

## Catatan revisi 1.0.2 (2026-09-25)
- Opsi global dihormati di posisi mana pun (sebelum/sesudah subperintah); nilai yang bertentangan ditolak (kode 2). Perintah simpan-kunci menyebut path lengkap dan menolak menimpa file kunci tanpa `--ya`.
- Modul Stok dideteksi lewat explorer/swagger.json; draf atau pelanggan ganda diblokir (kode 7). 70 tes lulus.

## Catatan revisi 1.0.1 (2026-09-24)
- Revisi dari uji independen pertama (6/10): panduan Dolibarr ikut dalam paket ZIP; bila modul Stok belum aktif ditulis "Modul Stok belum aktif" (bukan HABIS palsu); panduan dua pengguna (baca-saja dan pembuat draf); kunci yang salah dibersihkan atau ditolak tanpa traceback; cek ganda per HP/email; beberapa perbaikan kecil. 63 tes lulus.

## Catatan revisi 1.0.0 (2026-09-24)
- Rilis awal (uji internal): mengoperasikan Dolibarr lokal lewat REST API resmi (cek koneksi dan hak kunci, cari/tambah pelanggan, draf invoice PPN 12% x DPP 11/12, piutang dan umur piutang, stok menipis, laporan harian).
