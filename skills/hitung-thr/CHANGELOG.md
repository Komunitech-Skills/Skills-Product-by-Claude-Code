# Riwayat perubahan — hitung-thr

Catatan teknis per versi (dipindah dari README agar halaman pembeli ringkas).

## Catatan revisi 1.0.11 (2026-10-14)
- Uji ulang 1.0.10 (3 skenario, sisi dengan skill): rata-rata 8,0, tanpa salah angka; cacat "hanya bertanya" dan "istilah teknis" hilang. Sisa: pengumuman memakai "kami"/"Manajemen" bila nama usaha tidak diberikan → `thr.py` kini menulis `[isi: nama usaha]` (dan salinan `gaji-umkm/scripts/mesin/thr.py` disinkronkan).

## Catatan revisi 1.0.10 (2026-10-14)
Perbaikan dari uji OpenClaw sebelum/sesudah 1.0.9 (2026-10-14, 6,1 → 8,0, LULUS tipis). Rumus dan angka hitungan tidak berubah; `thr.py` tidak diubah (salinan di gaji-umkm tetap identik).
- **Data kurang → hitung dulu, tanya di akhir (maks. 3).** Pola lama "tanyakan sekali, maks. 5 pertanyaan" diganti: hari raya tidak disebut → hitung untuk perkiraan Idul Fitri berikutnya (atau Natal bila konteksnya Natal) dengan asumsi disebut di kalimat pertama; tanggal masuk tidak ada → "sudah lama" dianggap ≥ 12 bulan, bulan masuk saja → rentang (tanggal 1 s.d. akhir bulan), tanpa keterangan → dua baris (≥ 12 bulan = 1 × upah; < 12 bulan = rumus proporsional dengan contoh angka); teks grup ditunda sampai tanggal pasti. (Temuan uji: skenario data kurang hanya berisi 5 pertanyaan tanpa angka, nilai 6,5.)
- Opsi baru `scripts/tahun_hijriah.py <tanggal> --berikutnya idul-fitri|idul-adha`: perkiraan hari raya pertama pada/sesudah tanggal itu + batas H-7, tanpa web. 4 uji otomatis baru (42 lulus).
- **Blok baru "UNTUK AGENT SAJA":** larangan kata proses di balasan (skill, script, nama file, path folder kerja, nama skill lain, "belum terpasang"); cara membersihkan baris keluaran script sebelum ditempel (baris "File rekap", "asumsi skill", nama kolom); rujukan pajak cukup kalimat awam ("Pajak THR dihitung terpisah, bisa saya bantu bila diminta."). Lokasi file tidak lagi disebut; tawaran hapus data gaji tanpa path; `--csv` hanya bila diminta. (Temuan uji: "pakai script resmi skill THR", "skill `pph21-ter` (belum terpasang di sini)", path sandbox muncul di 3 dari 5 balasan.)
- **Nama usaha tidak dikarang:** jenis usaha ("bengkel motor", "toko bangunan") bukan nama usaha → `[isi: nama usaha]`; sama untuk nama pimpinan, tanggal pembayaran pasti, kontak HR. (Temuan uji: "Bengkel Motor", "Toko Bangunan" di teks grup.)
- Belum diuji ulang di OpenClaw.

## Catatan revisi 1.0.9 (2026-10-05)
- Pemeriksaan ulang PPh 21 DTP terhadap teks PMK 105/2025 (Pasal 2 ayat 1, Pasal 5, Pasal 6 ayat 6, Lampiran B): angka "THR diterima" **sudah benar** (sama dengan THR, tidak ditambah DTP). Kalimat penjelasan kini menulis jelas bahwa PPh 21 tetap dipotong, nilai yang sama dibayar tunai kembali, dan setoran ke negara untuk bagian DTP Rp 0. Tambah tes regresi dan ringkasan dasar hukum `references/dtp-pmk105.md`. **PERLU REVIEW konsultan pajak.**

## Catatan revisi 1.0.6 (2026-10-02)
- **Privasi pengumuman grup:** hasil selalu dua blok terpisah — **A. Rekap per orang (khusus pemilik/HR)** dan **B. Teks grup tanpa nama & nominal per orang**. Permintaan "sebut masing-masing dapat berapa di grup" ditolak sopan untuk bagian per orang; teks grup berisi jadwal cair, dasar aturan, dan cara menerima rincian pribadi. Opsi baru `--format pengumuman` mencetak teks grup saja. AI tidak menawarkan kirim otomatis/menyambungkan WhatsApp — hasil berupa draf yang kamu tempel sendiri. (Temuan uji 2026-10-02: saat dipasang bersama `laporan-status-kantor`, nominal per orang sempat masuk teks grup.)
- **Tanggal masuk di masa depan** (setelah hari ini) kini diberi ⚠️ agar dikonfirmasi (mungkin salah ketik tahun). Tanggal masuk setelah hari raya tidak lagi menghentikan seluruh rekap: orang itu ditandai belum berhak (Rp 0) dengan ⚠️.
- Bila tanggal cair tidak disebut, dipakai aturan umum **paling lambat H-7** (Permenaker 6/2016) sebagai asumsi — AI tidak mencari tanggal di web berulang-ulang.
- Kolom `gaji_sebulan` dikenali sebagai gaji pokok; judul rekap tidak lagi berakhir "— -" bila nama usaha kosong. Salinan `thr.py` di gaji-umkm disinkronkan (sha256 baru di `SUMBER.json`); 38 uji otomatis hitung-thr dan 41 uji gaji-umkm lulus.

## Catatan revisi 1.0.5 (2026-10-01)
- **Cek tanggal Lebaran/Idul Adha:** `scripts/tahun_hijriah.py <tanggal> --cek idul-fitri` (atau `idul-adha`) kini memberi PERINGATAN bila tanggal yang disebut bukan 1 Syawal/10 Zulhijah (selisih > 2 hari dari perkiraan), lengkap dengan perkiraan tanggal hari raya dan batas bayar H-7-nya. AI wajib menjalankannya dan menyampaikan sekali dengan sopan (tanggal resmi tetap menunggu penetapan pemerintah/SKB); bila kamu bersikeras, hasil tetap dihitung dengan tanggalmu. (Temuan uji: "Lebaran 20 Maret 2027" = 11 Syawal 1448 H; perkiraan Idul Fitri ±10 Maret 2027, batas bayar 3 Maret 2027.)
- Nama karyawan **tidak diperlukan**: AI langsung memakai "Karyawan 1, 2, …" tanpa bertanya (temuan uji: agent sempat menanyakan nama dulu).
- `thr.py` tidak berubah (salinan di gaji-umkm tetap identik); 33 uji otomatis lulus (4 uji baru).

## Catatan revisi 1.0.4 (2026-10-01)
- Tahun Hijriah hari raya kini **dihitung** dengan script kecil `scripts/tahun_hijriah.py` (kalender Hijriah tabular; mis. 10 Maret 2027 = 1 Syawal 1448 H), bukan ditebak. Bila tidak dihitung, tahun Hijriah tidak dicantumkan (temuan uji: Lebaran Maret 2027 sempat ditulis 1449 H).
- AI diinstruksikan tidak memakai nama dari contoh (mis. "Budi") di balasan; bila nama karyawan tidak diberikan, dipakai "Karyawan 1, 2, …".
- Instruksi: script dijalankan dari subfolder `scripts/` di folder skill. Script `thr.py` tidak berubah (salinannya di gaji-umkm tetap identik); 29 uji otomatis lulus (3 uji baru).
