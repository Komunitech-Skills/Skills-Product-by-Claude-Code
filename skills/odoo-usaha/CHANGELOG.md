# Riwayat perubahan — odoo-usaha

Catatan teknis per versi (dipindah dari README agar halaman pembeli ringkas).

## Riwayat versi
- **1.0.5 (2 Okt 2026)** — bagian "ATURAN WAJIB" di awal SKILL.md (uji ulang OpenClaw): bila pengguna menempel kunci/token/password di chat, agent tidak boleh menulis ulang satu karakter pun darinya (tidak utuh, tidak awalan, tidak disamarkan), cukup menyebut "kunci yang Anda tempel", dan memakai templat balasan baku (anggap kunci sudah bocor, cabut lalu simpan yang baru sendiri dari terminal). Ditambah uji regresi.
- **1.0.4 (2 Okt 2026)** — dari uji OpenClaw sebelum/sesudah: kunci API tidak pernah dicetak sebagian pun (tanpa awalan, akhiran, atau bintang berawalan); `simpan-kunci` dan `cek` hanya menyebut bahwa kunci tersimpan/terbaca. SKILL.md dan contoh 01 serta 09 diperbarui.
- **1.0.3 (1 Okt 2026)** — petunjuk lokasi script ditambahkan di SKILL.md: script ada di subfolder `scripts/` di folder skill; agent dilarang mencari script atau file pengguna ke seluruh disk (mis. `find /`).
- **1.0.2 (30 Sep 2026)** — panduan §5: sisa saran hak akses versi lama (Billing/Own Documents) dihapus; hanya satu tabel hak akses.
- **1.0.1 (30 Sep 2026)** — perbaikan dari uji ke Odoo Community 18 & 19 asli: (1) hak *Own Documents* tidak lagi menghasilkan angka penjualan/faktur kecil (bisa Rp 0) diam-diam — `cek` menampilkan cakupan data, laporan memberi **PERINGATAN DATA SEBAGIAN** + kode 9 (`--terima-sebagian` bila memang disengaja); (2) `piutang --per-tanggal` di masa lalu tidak lagi memasukkan faktur yang belum terbit dan memperhitungkan pelunasan setelah tanggal itu; (3) panduan hak pengguna diperbaiki secara jujur (Odoo tidak punya peran Penjualan baca-saja; pengaman tulis ada di script); (4) keterangan "barang masuk terjadwal" di stok menipis; (5) ENV `ODOO_HOST_DIIZINKAN` dihapus (host hanya lewat `atur --izinkan-host`).
- **1.0.0 (30 Sep 2026)** — rilis awal.
