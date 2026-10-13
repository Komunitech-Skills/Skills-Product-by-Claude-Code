# Riwayat perubahan — kasir-lokal

Catatan teknis per versi.

## Catatan revisi 1.1.7 (2026-10-03)
- Jalur baru "rekap dari nota yang DITEMPEL di chat" (tanpa database kasir): script `scripts/rekap_nota.py` menghitung omzet, porsi per menu, jumlah nota per menu, rincian per cara bayar, dan mencocokkan uang laci. Nota bertanda BATAL/void dikecualikan, bon dipisah dari uang masuk.
- Ada "RINGKASAN SIAP TEMPEL untuk grup karyawan" yang hanya berisi angka gabungan, tanpa nama/nomor pelanggan dan tanpa bon per orang. Ini draf: pemilik yang mengirim ke grup.
- Pemicu baru di SKILL.md ("ini nota hari ini, rekap + cocokkan laci + bikinin laporan buat grup"), uji `tests/uji_rekap_nota.py`, dan rujukan di `references/perintah.md`.

## Catatan revisi 1.1.6 (2026-10-01)
- Petunjuk lokasi script ditambahkan di SKILL.md: script ada di subfolder `scripts/` di folder skill. Agent dilarang mencari script atau file pengguna ke seluruh disk (mis. `find /`).

## Catatan revisi 1.1.5 (2026-09-29)
- Pengaman: singkatan opsi baris perintah tidak lagi diterima (mis. `--y` tidak bisa dibaca sebagai `--ya`), sehingga konfirmasi tidak terpicu tanpa sengaja. Ditambah uji regresi.

## Catatan revisi 1.1.4 (2026-09-29)
- Baris "Aturan kerja" ditambahkan di SKILL.md: agent tidak boleh memasang paket/aplikasi sendiri, tidak membuka atau mencari file di luar yang diberikan pengguna, dan hasil yang ditulis ke file harus disebut lokasinya (folder kerja, bukan `/tmp`).

## Catatan revisi 1.1.3 (2026-09-29)
- Aturan kredensial & jadwal (SKILL.md dan `references/openclaw-jadwal.md`): agent tidak pernah mencari, membaca, atau menampilkan token/API key dari environment, file konfigurasi, atau riwayat. Jadwal hanya dibuat setelah pengguna membalas "ya" atas perintah dan jam yang ditunjukkan; bila kanal belum siap atau perintah ditolak, agent berhenti dan memberi langkah persiapan.

## Catatan revisi 1.1.2 (2026-09-26)
- Pembeli yang belum bayar (bon/utang) kini diarahkan ke skill `buku-piutang`, karena kasir hanya mencatat penjualan yang sudah dibayar. Bila `buku-piutang` belum terpasang, cara lama (buat tagihan dengan `buat-invoice`) tetap bisa dipakai. Diperbarui di SKILL.md, README, dan `references/perintah.md`.

## Catatan revisi 1.1.1 (2026-09-24)
- Menutup celah "formula injection" CSV: teks yang diawali tanda minus tidak lagi bisa dibaca spreadsheet sebagai rumus. Ditambah uji regresi.
- Uji ulang v1.1.1: skor 9/10, mode PBJT diverifikasi pada 900 nota.

## Catatan revisi 1.1.0 (2026-09-24)
- Mode pajak PBJT (Pajak Barang dan Jasa Tertentu, UU 1/2022); dukungan satuan barang; penanganan zona waktu; dan larangan memanipulasi nota.

## Catatan revisi 1.0.0 (2026-09-24)
- Rilis awal (uji internal): kasir UMKM satu outlet di komputer pemilik dengan database lokal, dioperasikan lewat chat.
