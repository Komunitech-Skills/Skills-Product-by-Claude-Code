# Telegram gelombang 4 — 5 skill selisih terbesar (2026-10-03)

Disetujui pemilik 2026-10-03 ("setuju, lanjut gelombang Telegram dengan 5 skill itu"). Skill dipilih dari urutan selisih skor uji internal OpenClaw (`examples/00-openclaw-sebelum-sesudah.md`).

## Cara
- 10 topik baru di grup uji: `G4 <skill> — TANPA skill` (setelan topik `skills: []`) dan `G4 <skill> — DENGAN skill`. Topik baru agar tidak terpengaruh riwayat gelombang lama.
- Bot produksi disamakan ke versi repo sebelum uji (cadangan dibuat): slip-gaji-bpjs diperbarui, spt-tahunan-op dipasang (belum ada). Setelan OpenClaw dicadangkan sebelum diubah; hot-reload.
- Bot penguji mengirim 10 pesan (1 per sisi per skill), berurutan, menunggu sesi selesai. Tanpa balas-otomatis. Data di pesan fiktif.

## Hasil (05.43–06.11 UTC)

| Skill | TANPA skill | DENGAN skill | Pembeda |
|---|---|---|---|
| surat-peringatan-karyawan | Langsung membuat SP2 lengkap | Menahan: SP1 10 Mar 2026 berakhir 9 Sep 2026, pelanggaran sesudahnya → sarankan SP1 baru kecuali PP perusahaan mengatur lain; minta konfirmasi | Paling jelas (sama dengan uji internal) |
| slip-gaji-bpjs | PPh 21 Desember **Rp165.000**, THP Rp7.035.000 (premi BPJS/JKK/JKM yang dibayar perusahaan tidak dimasukkan ke bruto pajak) | PPh 21 Desember **Rp321.595**, THP Rp6.878.405; biaya perusahaan Rp8.268.000; file slip md/html/csv; asumsi & catatan Coretax | Angka beda Rp156.595 (sama dengan uji internal) |
| spt-tahunan-op | **Tidak ada jawaban** (sesi selesai tanpa balasan) | Meluruskan: konsultan = pekerjaan bebas, PPh final 0,5% salah skema; tanpa pemberitahuan NPPN dianggap memilih pembukuan; minta 4 data sebelum hitung | Jelas, tetapi belum sampai angka (butuh 1 giliran lanjutan) |
| kontrak-kerja-pkwt | Ganti rugi sisa kontrak Rp17.580.645 benar, tetapi **uang kompensasi PKWT terlewat** (bilang tidak ada hak lain); mengaku web search mati | Kompensasi Rp3.534.946 + ganti rugi Rp17.580.645 = **Rp21.115.591** | Selisih Rp3,5 jt. Tanpa skill lebih baik daripada uji internal (dulu timeout/salah) |
| pengingat-follow-up | Angka & draf benar; **menawarkan "kirim langsung ke mereka"** dan berjanji mengingatkan Senin (tanpa jadwal nyata) | Tersimpan terstruktur (#1–#3), tahun yang diasumsikan disebut, total Rp7.250.000, draf dikirim sendiri | Pembeda di keamanan/pencatatan, bukan angka |

Verifikasi angka (kurator, python): slip-gaji bruto pajak 7.500.000 + BPJS Kes 4% 300.000 + JKK 0,24% 18.000 + JKM 0,3% 22.500 = 7.840.500 × TER B 1% = 78.405; ×11 = 862.455; setahun 94.086.000 − BJ 4.704.300 − JHT+JP 2.700.000 − PTKP K/1 63.000.000 = PKP 23.681.000 (dibulatkan ribuan) × 5% = 1.184.050; Desember 321.595 ✅. Kontrak: 8 bln 15/31 hari = 8,4839 bln; 8,4839/12 × 5 jt = 3.534.946; sisa 3,5161 × 5 jt = 17.580.645 ✅.

## Catatan / temuan
- **Mention berhasil**: balasan DENGAN skill pada SP & SPT kini diawali `@KTpenguji_bot` sehingga diskusi bisa berlanjut.
- **spt-tahunan-op TANPA skill tidak menjawab**: tercatat sebagai hasil (bot tanpa skill macet), bukan kesalahan uji.
- **kontrak-kerja-pkwt DENGAN skill**: masih menyebut "usaha mikro/kecil boleh kompensasi berdasarkan kesepakatan" — sudah tercatat di uji internal sebagai poin "ambang usaha kecil"; perlu dicek pembuat (perlu dasar pasal yang tepat). Tidak memengaruhi angka.
- **pengingat-follow-up DENGAN skill**: draf ke Toko Sinar memuat tenggat "paling lambat 6 Okt" yang tidak diminta pengguna (minor).
- Kuota 10 pesan habis. Giliran lanjutan (SP: jawab "ikut 6 bulan"; SPT: jawab 4 pertanyaan agar angka kurang bayar muncul) perlu persetujuan gelombang berikutnya.

## Giliran lanjutan (disetujui pemilik, 2 pesan, 06.23 UTC)
Dikirim sebagai *reply* ke jawaban bot di topik DENGAN skill.

| Skill | Balasan penguji | Hasil bot (DENGAN skill) |
|---|---|---|
| surat-peringatan-karyawan | "ikut default 6 bulan, bikinin SP1 baru" | SP1 baru lengkap; masa berlaku 3 Okt 2026 s.d. 2 Apr 2027 (dari script `masa_berlaku.py`); Berita Acara Klarifikasi; catatan alasan SP1 bukan SP2; disclaimer. ✅ |
| spt-tahunan-op | jawab 4 pertanyaan (jasa IT murni, tanpa pembukuan, Bandung, setor 0,5% Rp1,9 jt, tanpa potongan klien) | NPPN 50% → neto Rp190 jt − PTKP TK/0 Rp54 jt = PKP Rp136 jt → PPh 5%×60 jt + 15%×76 jt = **Rp14.400.000 kurang bayar** (✅ python); Rp1,9 jt tidak dikreditkan, jalur pengembalian; status "simulasi" karena tanpa pemberitahuan NPPN. |

Temuan:
- spt-tahunan-op: menyebut "batas lapor 31 Maret 2026" tanpa menyebut bahwa per Oktober 2026 SPT TP 2025 sudah **terlambat** (denda telat lapor + bunga) — perlu perbaikan kecil di skill. KLU 62020 vs 62010 (norma sama 50%) belum diverifikasi kurator. Jawaban memakai ±55 pemanggilan alat (pencarian lampiran PER-17), lama.
- **Gangguan infrastruktur:** gateway mati sekali karena memori (±13.16 WIB), lalu restart sendiri ±13.30 WIB karena instalasi OpenClaw bersama (`/tmp/uji-openclaw`) diperbarui ke 2026.9.8 oleh `scripts/uji_openclaw.sh` yang dijalankan agent revisi. Kedua jawaban tetap terkirim. Saran: gateway produksi memakai instalasi terpisah dari alat uji muat.
