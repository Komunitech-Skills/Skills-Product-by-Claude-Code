# Riwayat perubahan — resi-picking

Catatan teknis per versi.

## Catatan revisi 1.0.4 (2026-10-01)
- Petunjuk lokasi script ditambahkan di SKILL.md: script ada di subfolder `scripts/` di folder skill. Agent dilarang mencari script atau file pengguna ke seluruh disk (mis. `find /`).

## Catatan revisi 1.0.3 (2026-09-29)
- Baris "Aturan kerja" ditambahkan di SKILL.md: agent tidak boleh memasang paket/aplikasi sendiri, tidak membuka atau mencari file di luar yang diberikan pengguna, dan hasil yang ditulis ke file harus disebut lokasinya (folder kerja, bukan `/tmp`).
- Uji ulang independen v1.0.2 lulus 9/10 (contoh uji ulang di `examples/`).

## Catatan revisi 1.0.2 (2026-09-26)
- Bila lebih dari satu kolom di file sama-sama cocok untuk satu isian (mis. "SKU Induk" dan "Nomor SKU"), script kini memberi peringatan yang menyebut semua kandidat, kolom yang dipakai, dan opsi `--kolom-...` untuk membetulkan. Sebelumnya kolom pertama dipilih diam-diam. Field baru `kolom_ambigu` di keluaran JSON. Uji regresi menjadi 29 tes.

## Catatan revisi 1.0.1 (2026-09-26)
- Revisi dari uji pertama (7/10): judul kolom dikenali per kata utuh (bukan potongan huruf), sehingga "Nama Kurir" atau "No. Invoice" kini terdeteksi. Sinonim judul kolom Shopee, Tokopedia, TikTok Shop, Lazada, dan Blibli diperluas; sumber dan status verifikasinya dicatat di `references/sumber-kolom-marketplace.md`.
- Pesan error kini selalu menyebut kolom yang sudah terdeteksi, semua nama kolom di file, dan opsi `--kolom-...` yang perlu ditambahkan; agent wajib menawarkan perintah itu.

## Catatan revisi 1.0.0 (2026-09-26)
- Rilis awal (uji internal): daftar ambil barang (picking list) per SKU/rak dan urutan kemas/tempel resi per kurir dari file ekspor pesanan marketplace (CSV), tanpa database.
