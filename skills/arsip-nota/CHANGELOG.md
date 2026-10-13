# Riwayat perubahan — arsip-nota

Catatan teknis per versi.

## Catatan revisi 1.0.7 (2026-10-13)
- `references/openclaw-jadwal.md`: dua rujukan ke dokumen yang tidak ikut paket pembeli (panduan uji platform dan aturan kerja internal) diganti kalimat yang berdiri sendiri: karena jadwal bulanan ini belum diuji di Gateway sungguhan, coba sekali dengan `openclaw automations run <id>` dan pastikan ringkasan tiba di Telegram sebelum diandalkan; risiko WhatsApp ditulis langsung (WhatsApp Web tidak resmi, nomor bisa diblokir). Script dan cara kerja skill tidak berubah.

## Catatan revisi 1.0.6 (2026-10-01)
- Petunjuk lokasi script ditambahkan di SKILL.md: script ada di subfolder `scripts/` di folder skill. Agent dilarang mencari script atau file pengguna ke seluruh disk (mis. `find /`).

## Catatan revisi 1.0.5 (2026-09-30)
- Format angka Indonesia diperbaiki: nominal meragukan tanpa satuan ("1,5", "150,50", "38.5", "1,500") kini ditolak dengan pesan jelas, tidak lagi diam-diam terbaca Rp15 atau Rp15.050. Agent menanyakan maksud pengguna (mis. 1.500 atau 1,5jt). Bentuk wajar seperti "38.000", "Rp38.000", "1.250.000,50", "150rb", dan "1,5jt" tetap diterima. Ditambah uji regresi.

## Catatan revisi 1.0.4 (2026-09-29)
- Pengaman: singkatan opsi baris perintah tidak lagi diterima (mis. `--y` tidak bisa dibaca sebagai `--ya`), sehingga konfirmasi tidak terpicu tanpa sengaja. Ditambah uji regresi.

## Catatan revisi 1.0.3 (2026-09-29)
- Baris "Aturan kerja" ditambahkan di SKILL.md: agent tidak boleh memasang paket/aplikasi sendiri, tidak membuka atau mencari file di luar yang diberikan pengguna, dan hasil yang ditulis ke file harus disebut lokasinya (folder kerja, bukan `/tmp`).

## Catatan revisi 1.0.2 (2026-09-29)
- Aturan kredensial & jadwal (SKILL.md dan `references/openclaw-jadwal.md`): agent tidak pernah mencari, membaca, atau menampilkan token/API key dari environment, file konfigurasi, atau riwayat. Jadwal hanya dibuat setelah pengguna membalas "ya" atas perintah dan jam yang ditunjukkan.

## Catatan revisi 1.0.1 (2026-09-26)
- Perbaikan dari uji independen (8/10): nota yang diblokir karena duplikat kini dilaporkan jujur dengan `mode: "diblokir_duplikat"` (bukan "tersimpan"), dan agent menanyakan dulu apakah itu nota yang sama sebelum memakai `--izinkan-duplikat`.
- Kata kunci tebakan kategori ditambah untuk toko bangunan dan BBM.

## Catatan revisi 1.0.0 (2026-09-26)
- Rilis awal (uji internal): merapikan foto/PDF nota, struk, dan faktur UMKM menjadi arsip lokal (database SQLite di komputer sendiri), dengan nama file baku tanggal_vendor_nominal, folder per tahun/bulan, dan deteksi duplikat lewat hash.
