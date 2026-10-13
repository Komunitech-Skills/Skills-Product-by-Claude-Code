# Riwayat perubahan — hitung-thr

Catatan teknis per versi (dipindah dari README agar halaman pembeli ringkas).

## Catatan revisi 1.0.4 (2026-10-01)
- Tahun Hijriah hari raya kini **dihitung** dengan script kecil `scripts/tahun_hijriah.py` (kalender Hijriah tabular; mis. 10 Maret 2027 = 1 Syawal 1448 H), bukan ditebak. Bila tidak dihitung, tahun Hijriah tidak dicantumkan (temuan uji: Lebaran Maret 2027 sempat ditulis 1449 H).
- AI diinstruksikan tidak memakai nama dari contoh (mis. "Budi") di balasan; bila nama karyawan tidak diberikan, dipakai "Karyawan 1, 2, …".
- Instruksi: script dijalankan dari subfolder `scripts/` di folder skill. Script `thr.py` tidak berubah (salinannya di gaji-umkm tetap identik); 29 uji otomatis lulus (3 uji baru).

## Catatan revisi 1.0.5 (2026-10-01)
- **Cek tanggal Lebaran/Idul Adha:** `scripts/tahun_hijriah.py <tanggal> --cek idul-fitri` (atau `idul-adha`) kini memberi PERINGATAN bila tanggal yang disebut bukan 1 Syawal/10 Zulhijah (selisih > 2 hari dari perkiraan), lengkap dengan perkiraan tanggal hari raya dan batas bayar H-7-nya. AI wajib menjalankannya dan menyampaikan sekali dengan sopan (tanggal resmi tetap menunggu penetapan pemerintah/SKB); bila kamu bersikeras, hasil tetap dihitung dengan tanggalmu. (Temuan uji: "Lebaran 20 Maret 2027" = 11 Syawal 1448 H; perkiraan Idul Fitri ±10 Maret 2027, batas bayar 3 Maret 2027.)
- Nama karyawan **tidak diperlukan**: AI langsung memakai "Karyawan 1, 2, …" tanpa bertanya (temuan uji: agent sempat menanyakan nama dulu).
- `thr.py` tidak berubah (salinan di gaji-umkm tetap identik); 33 uji otomatis lulus (4 uji baru).

## Catatan revisi 1.0.6 (2026-10-02)
- **Privasi pengumuman grup:** hasil selalu dua blok terpisah — **A. Rekap per orang (khusus pemilik/HR)** dan **B. Teks grup tanpa nama & nominal per orang**. Permintaan "sebut masing-masing dapat berapa di grup" ditolak sopan untuk bagian per orang; teks grup berisi jadwal cair, dasar aturan, dan cara menerima rincian pribadi. Opsi baru `--format pengumuman` mencetak teks grup saja. AI tidak menawarkan kirim otomatis/menyambungkan WhatsApp — hasil berupa draf yang kamu tempel sendiri. (Temuan uji 2026-10-02: saat dipasang bersama `laporan-status-kantor`, nominal per orang sempat masuk teks grup.)
- **Tanggal masuk di masa depan** (setelah hari ini) kini diberi ⚠️ agar dikonfirmasi (mungkin salah ketik tahun). Tanggal masuk setelah hari raya tidak lagi menghentikan seluruh rekap: orang itu ditandai belum berhak (Rp 0) dengan ⚠️.
- Bila tanggal cair tidak disebut, dipakai aturan umum **paling lambat H-7** (Permenaker 6/2016) sebagai asumsi — AI tidak mencari tanggal di web berulang-ulang.
- Kolom `gaji_sebulan` dikenali sebagai gaji pokok; judul rekap tidak lagi berakhir "— -" bila nama usaha kosong. Salinan `thr.py` di gaji-umkm disinkronkan (sha256 baru di `SUMBER.json`); 38 uji otomatis hitung-thr dan 41 uji gaji-umkm lulus.

## Catatan revisi 1.0.9 (2026-10-05)
- Pemeriksaan ulang PPh 21 DTP terhadap teks PMK 105/2025 (Pasal 2 ayat 1, Pasal 5, Pasal 6 ayat 6, Lampiran B): angka "THR diterima" **sudah benar** (sama dengan THR, tidak ditambah DTP). Kalimat penjelasan kini menulis jelas bahwa PPh 21 tetap dipotong, nilai yang sama dibayar tunai kembali, dan setoran ke negara untuk bagian DTP Rp 0. Tambah tes regresi dan ringkasan dasar hukum `references/dtp-pmk105.md`. **PERLU REVIEW konsultan pajak.**
