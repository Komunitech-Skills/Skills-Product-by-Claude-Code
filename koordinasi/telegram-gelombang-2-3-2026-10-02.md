# Tampilan Telegram gelombang 2 & 3 — sebelum/sesudah (2026-10-02)

Dasar: persetujuan pemilik "setuju gelombang 2" dan "a, lanjut diskusi 2-3 giliran". Semua data uji fiktif. Pengirim: bot penguji (hanya `sendMessage`/`createForumTopic`/`getUpdates`), tanpa balasan otomatis; pesan lanjutan ditulis manual oleh agent Komunitech sebagai *reply*.

## Cara menampilkan "sebelum/sesudah" di Telegram
- 5 topik baru "⚪ SEBELUM tanpa skill: <skill>" (515–519). Di setelan OpenClaw topik itu diberi `skills: []` → bot di topik tsb. tidak melihat skill apa pun (dicek: `skillsSnapshot.skills = []`, prompt skill kosong).
- Pesan identik dikirim ke topik SEBELUM dan ke topik skill-nya (SESUDAH). SEBELUM dikirim lebih dulu.
- `channels.telegram.replyToMode` diubah `off` → `first` (atas masukan pemilik: bot tidak me-reply pesan penanya). Catatan: hanya potongan pertama (pesan status "Working") yang menjadi reply; jawaban akhir tetap tampil sebagai pesan biasa di topik.
- Backup setelan: `openclaw-real/openclaw.json.before-gelombang2-20261002-1155`. Revert: salin backup, gateway memuat ulang otomatis.

## Pesan terkirim (20 total: 10 per gelombang)
| Skill | Solusi VIP | SEBELUM | SESUDAH |
|---|---|---|---|
| hitung-hpp | usaha-offline | HPP Rp6.950 benar; dua pilihan harga (Rp10.700 / Rp9.400), bertanya definisi margin | HPP Rp6.950, harga Rp11.000 (margin 36,82%), BEP 114 bungkus/bln — cocok dengan contoh teruji |
| kontrak-kerja-pkwt | konsultan, klinik | **Gagal 2×** (model idle timeout router) | Kompensasi Rp3.534.946 + ganti rugi Pasal 62 Rp17.580.645 = Rp21.115.591; tanya status usaha mikro/kecil (PP 35/2021 Ps. 16 ayat 6); disclaimer |
| crm-wa (3 giliran) | toko-online, kantor | Mencatat ke CSV buatan sendiri; giliran 3: draf WA wajar, sisa tagihan Rp700rb | Giliran 1–2 baik (deteksi nama dobel, status Deal + DP). **Giliran 3 salah:** tercampur data uji lama usaha lain ("Dapur Mama Tia") → draf bertanda tangan "Tia", prospek orang lain ikut direkap |
| atur-keuangan-pribadi | kripto-keuangan | Anggaran & dana darurat 6–9× pengeluaran, tanpa script | Zero-based dari script; **cacat:** THR dihitung di pemasukan bulanan lalu disuruh disimpan lagi (dobel) → diperbaiki di 1.0.7 |
| pengingat-pasien-klinik (3 giliran) | klinik | **Memasang pengingat OTOMATIS** ke grup (cron) — melanggar keputusan pemilik (draf dikirim staf); pasien tanpa izin tidak dibuatkan draf | Tanggal benar ("3 hari lagi" → Senin 5 Okt), izin tercatat, Kevin (tanpa izin) disaring, draf untuk disalin staf |

## Tindakan setelah gelombang
- Cron "Pengingat kontrol behel" buatan sisi SEBELUM (akan kirim ke topik 515 tgl 4 Okt) **dihapus**.
- Data uji lama di bot produksi (`~/KomunitechData`, file CSV/JSON di workspace) dipindah ke `openclaw-real/data-uji-backup-20261002-1240/` agar gelombang berikutnya mulai bersih.
- Revisi: atur-keuangan-pribadi 1.0.7 (THR musiman), crm-wa (cek identitas usaha sebelum mencatat) — diuji ulang oleh penguji terpisah.

## Pelajaran
1. **Kirim berurutan**, tunggu jawaban selesai: 5 pesan sekaligus memicu timeout router.
2. **Reset data uji** sebelum tiap gelombang; workspace bot produksi dipakai bersama semua topik.
3. Sisi tanpa skill bisa membuat **jadwal otomatis** sendiri — cek `cron list` setiap selesai gelombang.
4. Jawaban hukum tanpa skill (PKWT) bisa melewati batas waktu model; dengan skill selesai normal.
