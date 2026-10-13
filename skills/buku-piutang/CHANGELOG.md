# Riwayat perubahan — buku-piutang

Catatan teknis per versi.

## Catatan revisi 1.0.5 (2026-10-13)
- Batasan di SKILL.md ditambah satu aturan: setiap tarif/aturan disebut dengan dasar aturan + tahun; angka hanya dari script/input pengguna; nilai yang tidak diberikan pengguna ditandai asumsi (tanpa label "wajar/umum/lazim" yang tidak bersumber).
- Contoh uji `examples/02`: keterangan PPh 23 kini bersyarat dan bersumber (bila pelanggan pemotong PPh 23/badan usaha, tarif 2% untuk jasa sesuai UU PPh Pasal 23 ayat (1) huruf c; pastikan ke pelanggan).

## Catatan revisi 1.0.4 (2026-10-01)
- Petunjuk lokasi script ditambahkan di SKILL.md: script ada di subfolder `scripts/` di folder skill. Agent dilarang mencari script atau file pengguna ke seluruh disk (mis. `find /`).

## Catatan revisi 1.0.3 (2026-09-29)
- Pengaman: singkatan opsi baris perintah tidak lagi diterima (mis. `--y` tidak bisa dibaca sebagai `--ya`), sehingga konfirmasi tidak terpicu tanpa sengaja. Ditambah uji regresi.

## Catatan revisi 1.0.2 (2026-09-29)
- Baris "Aturan kerja" ditambahkan di SKILL.md: agent tidak boleh memasang paket/aplikasi sendiri, tidak membuka atau mencari file di luar yang diberikan pengguna, dan hasil yang ditulis ke file harus disebut lokasinya (folder kerja, bukan `/tmp`).

## Catatan revisi 1.0.1 (2026-09-29)
- Aturan kredensial & jadwal (SKILL.md dan `references/openclaw-jadwal.md`): agent tidak pernah mencari, membaca, atau menampilkan token/API key dari environment, file konfigurasi, atau riwayat. Jadwal hanya dibuat setelah pengguna membalas "ya" atas perintah dan jam yang ditunjukkan.
- Hasil uji independen v1.0.0 (8/10) dan perbandingan pesaing tercatat di `examples/`.

## Catatan revisi 1.0.0 (2026-09-26)
- Rilis awal (uji internal): buku piutang pelanggan lokal (database SQLite, Python standar). Catat nota/bon, pembayaran sebagian/lunas/kelebihan (deposit) tanpa saldo minus diam-diam, saldo per pelanggan, umur piutang, jatuh tempo, impor CSV nota/kasir, rekap JSON, draf tagihan dengan tautan wa.me (dikirim manusia), ringkasan harian OpenClaw, serta backup/restore yang aman.
