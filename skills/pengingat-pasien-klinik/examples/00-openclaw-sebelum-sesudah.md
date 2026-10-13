# Uji OpenClaw SEBELUM vs SESUDAH — pengingat-pasien-klinik

Sumber: `solusi-vip/klinik/UJI-OPENCLAW.md` (rincian: `solusi-vip/klinik/uji-openclaw/03-pengingat-kontrol-info-kurang.md` dan `03-pengingat-kontrol-info-kurang-ulang.md`). Tanggal uji: 2026-10-01 (Asia/Jakarta). Versi skill saat uji: uji pertama tidak dicatat di sumber (sebelum revisi 1.0.6); uji ulang = 1.0.6 (versi katalog saat ini 1.0.8). Penguji: agent penguji independen (bukan pembuat skill).

Berkas ini hanya menyalin ringkasan dari catatan uji internal di atas; balasan utuh kedua sisi ada di berkas sumber. Semua data pasien fiktif.

## Cara uji
- OpenClaw lokal (`openclaw agent --local`, tanpa Telegram/gateway), model router Komunitech yang sama dengan bot member (`ninerouter/komunitech`, jawaban `claude-sonnet-5`).
- SEBELUM = home tanpa skill solusi; SESUDAH = home dengan paket skill Klinik. Workspace awal identik.
- Pesan member giliran 1 (info kurang): "tolong catat pasien buat diingetin kontrol ya: Bu Rina, kontrol behel bulan depan". Giliran 2 (identik di kedua sisi): nomor WA, tanggal 3 November, pasien sudah setuju diingatkan lewat WA, minta draf pesan.
- Tanggal dicek penguji dengan Python (3 Nov 2026 = Selasa; H-3 = 31 Okt, H-1 = 2 Nov); isi `pasien/DAFTAR.csv` hasil agent diperiksa.

## Skor (skala 10)

| # | Skenario | Tanpa skill | Dengan skill (uji pertama) | Dengan skill (uji ulang, v1.0.6) | Pembeda satu kalimat |
|---|---|---|---|---|---|
| 1 | Catat pasien untuk pengingat kontrol, info kurang (tanpa nomor WA, tanggal, persetujuan) | 3 | 8,5 | 9 | Tanpa skill pasien dicatat tanpa nomor WA atau persetujuan, agent menjanjikan kirim otomatis H-2/H-1 ke pasien dan mengubah konfigurasi gateway sendiri; dengan skill agent menanyakan dua hal wajib (nomor WA dan persetujuan ya/tidak), mencatat satu baris lewat script, dan menandai draf "salin dan kirim sendiri, bukan kiriman otomatis". |
| | **Rata-rata** (satu skenario) | **3** | **8,5** | **9** | |

## Verdik
**LULUS uji ulang** (kata sumber: ketiga skill klinik yang diuji ulang LULUS; cacat yang dilaporkan hilang).

## Catatan jujur
- Satu skenario saja di OpenClaw. Sisi tanpa skill tidak diulang pada uji ulang.
- Cacat uji pertama sisi dengan skill: contoh perintah di SKILL.md (`<perintah> [opsi] --json`) gagal (kode 2, script menolak `--json` di akhir) sehingga agent mencoba ulang, dan agent menjalankan `find / -name pengingat_pasien.py` ke seluruh disk. Pada uji ulang 0 panggilan gagal dari 2 panggilan `exec` (dulu 4); tidak adanya `find /` disimpulkan dari jumlah panggilan (argumen alat tidak dibaca).
- Regresi kecil uji ulang: kalimat "Nanti sistem akan menandainya di daftar H-3, H-1, dan hari-H secara otomatis" bisa dibaca admin awam seolah ada pengingat yang jalan sendiri, padahal pengelompokan hanya muncul saat daftar diminta (jadwal ringkasan harian belum dipasang di uji ini). Tidak menjanjikan kirim ke pasien.
- Perilaku berisiko sisi tanpa skill pada uji pertama (mengubah `openclaw.json` home uji `kosong-klinik`) hanya terjadi di home uji, bukan bot produksi.
- Jadwal otomatis ringkasan pagi Telegram belum teruji di uji ini karena gateway sengaja tidak dijalankan.
- Bahan pendukung kualitatif (tanpa skor): tampilan Telegram gelombang 2-3 pada 2026-10-02 di bot OpenClaw asli (`koordinasi/telegram-gelombang-2-3-2026-10-02.md`): sisi tanpa skill memasang pengingat OTOMATIS (cron) yang lalu dihapus, sedangkan dengan skill tanggal benar, izin tercatat, pasien tanpa izin disaring, dan draf untuk disalin staf. Uji gabungan paket klinik 2026-10-02 (`solusi-vip/klinik/UJI-GABUNGAN-2026-10-02.md`) menemukan celah lain (diagnosis dibuang diam-diam, teks grup memuat nama + jenis kunjungan bernada penyakit) yang dicatat di revisi 1.0.7 README skill.
