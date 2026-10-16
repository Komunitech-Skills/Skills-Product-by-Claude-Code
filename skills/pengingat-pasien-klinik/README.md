# Kurangi Pasien Lupa Kontrol atau Vaksin

**Tiap pagi, minta asisten AI Anda daftar pasien yang harus diingatkan hari ini, lengkap dengan draf pesan WA sopan siap disalin staf — tanpa menyimpan rekam medis.**

Diuji AI penguji independen di OpenClaw (satu skenario): 3 → 8,5 dari 10, uji ulang setelah perbaikan 9 (tanpa skill pasien dicatat tanpa nomor WA atau persetujuan, pengiriman otomatis dijanjikan, dan pengaturan OpenClaw diubah sendiri; dengan skill persetujuan ditanyakan dan pesan hanya disiapkan sebagai draf untuk staf).

> **Penting:** skill ini **belum direview tenaga medis** dan bukan alat diagnosis. Data pasien disimpan minimal (nama panggilan, nomor WA, jenis kunjungan, tanggal), hanya di komputer klinik Anda. Pesan hanya draf yang dikirim staf klinik. Contoh di bawah fiktif.

> **Yang Anda butuhkan:** AI agent yang mendukung skill (OpenClaw, Claude Code, Codex, atau Cursor — langganan AI-nya ditanggung sendiri) di komputer Windows/Mac/Linux. Python 3 (bawaan Mac/Linux, unduh gratis di Windows) untuk menjalankan skrip pendukung skill ini; tanpa Python skill tetap berjalan, AI mengerjakannya langsung tetapi hasil angka sebaiknya Anda cek ulang. Tidak perlu API key atau akun tambahan dari Komunitech.

## Manfaat
- ✅ **Cukup ketik satu kalimat.** "Catat Bu Sari, kontrol gigi 10 hari lagi, WA 0812..., setuju diingatkan" langsung tersimpan.
- ✅ **Daftar H-3 (3 hari sebelum jadwal), H-1 (sehari sebelum), hari ini, dan terlambat** — jelas dan otomatis dari tanggal yang Anda masukkan, tidak perlu dihitung manual.
- ✅ **Draf pesan siap disalin**, sopan dan netral, tanpa istilah medis dan tanpa menyebut penyakit. Staf tinggal cek dan kirim dari WA klinik sendiri.
- ✅ **Data seminim mungkin**: hanya nama panggilan, nomor WA, jenis kunjungan umum (kontrol/vaksin/dll), dan tanggal. **Skill tidak menyimpan diagnosis, rekam medis, atau NIK (nomor KTP)** — dan skill ini dirancang menolak kalau ada yang tidak sengaja mengetik nama penyakit.
- ✅ **Persetujuan pasien dicatat**, dan ada perintah hapus data sekali ketik — dirancang mengikuti prinsip UU Pelindungan Data Pribadi (UU PDP); kepatuhan hukum klinik tetap tanggung jawab Anda.

## Cocok untuk siapa
- Klinik pratama, klinik gigi, klinik kecantikan, fisioterapi.
- Praktik mandiri dokter, dokter gigi, dan bidan.
- Klinik hewan (pengingat vaksin/kontrol untuk hewan peliharaan, WA ke pemiliknya).
- Pemilik atau penanggung jawab klinik yang sudah memakai OpenClaw dan ingin ringkasan harian otomatis di Telegram (jadwal otomatis ini belum diuji langsung).

## Contoh sebelum & sesudah
**Sebelum:** jadwal kontrol dan vaksin dicatat di buku atau diingat staf. Pasien lupa datang,
staf lupa mengingatkan, dan setiap kali harus mengetik pesan pengingat dari nol.

**Sesudah (cukup ketik):** "Siapa yang harus diingatkan hari ini?" Cuplikan hasil asli (dipotong; uji simulasi, data fiktif, hari acuan 26 Sep 2026, dari `examples/02-daftar-harian.md`):
```
HARI INI (1)
  #3 Kucing Mimi | Vaksin hewan | 26 Sep 2026 | 0812-9999-8888
BESOK (H-1) (1)
  #2 Pak Budi | Vaksin | 27 Sep 2026 | 0813-2222-3333

DRAF PESAN (salin & kirim sendiri, JANGAN dikirim otomatis):

#2 Pak Budi (0813-2222-3333):
Halo Pak Budi, ini pengingat dari kami untuk jadwal vaksin Anda pada 27 Sep 2026. Mohon
konfirmasi kehadiran Anda. Kalau perlu mengubah jadwal, silakan balas pesan ini. Terima kasih.
```
Staf tinggal salin, buka WA klinik, tempel, dan kirim. Pasien yang tidak setuju diingatkan sengaja tidak muncul di daftar. Sudah datang? "Kucing Mimi sudah datang vaksin. Jadwalkan lagi 1 bulan lagi." — jadwal berikutnya (26 Okt 2026) otomatis tercatat.

## Cara pakai
Setelah terpasang, cukup ketik permintaan biasa ke AI agent Anda, misalnya:
- "Catat pasien baru: Pak Budi, vaksin, tanggal 15 Oktober, WA 0813-2222-3333, setuju diingatkan."
- "Siapa yang harus diingatkan hari ini?" / "Ada yang terlewat?"
- "Bu Sari sudah datang, jadwalkan lagi 1 bulan lagi." / "Pak Budi batal, pindah kota."
- "Bu Sari minta datanya dihapus."
- "Impor daftar pasien kontrol ini." (tempel, atau unggah file tabel CSV dari Excel)
- "Kirim ringkasan pengingat pasien tiap pagi jam 7.30 ke Telegram saya." (khusus OpenClaw; jadwal otomatisnya belum diuji langsung)

**Penting:** asisten hanya **menyiapkan draf**. Staf klinik sendiri yang menyalin dan mengirimnya
ke pasien. Tidak ada pengiriman otomatis dan tidak ada broadcast — sesuai kebijakan Komunitech
untuk data kesehatan pasien.

## Instalasi singkat
Salin folder `pengingat-pasien-klinik` ke folder skills AI agent Anda:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |

Panduan lengkap (termasuk Windows): lihat `CARA-INSTAL.md` di dalam paket.

Ringkasan otomatis tiap pagi hanya tersedia di **OpenClaw** (jadwal ini belum diuji langsung), dan komputer yang menjalankannya
harus menyala pada jam tersebut (lihat `references/openclaw-jadwal.md`). Di Claude Code, Codex,
atau Cursor, skill ini dirancang tetap bisa dipakai sebagai buku jadwal manual — staf cukup mengetik
"daftar pengingat hari ini" setiap pagi. Pengujian langsung baru dilakukan di OpenClaw (di Claude Code
baru simulasi agent); Codex dan Cursor belum diuji.

**Hasil uji (angka nyata):** uji OpenClaw (uji otomatis agent, lingkungan uji terpisah), 2026-10-01, skor 1–10 penguji independen. Sumber: `examples/00-openclaw-sebelum-sesudah.md`. Satu skenario pengingat dengan info kurang (tanpa nomor WA dan tanpa persetujuan pasien), uji pertama: tanpa skill **3** → dengan skill **8,5**; uji ulang setelah perbaikan (v1.0.6) dengan skill **9** (sisi tanpa skill tidak diulang). Tanpa skill, AI mencatat pasien tanpa nomor WA dan persetujuan, menjanjikan pengiriman otomatis ke pasien, dan mengubah pengaturan OpenClaw sendiri; dengan skill, dua hal wajib (nomor WA dan persetujuan) ditanyakan dan pesan hanya disiapkan sebagai draf untuk staf. Jujur: hanya satu skenario yang diuji, jadwal ringkasan pagi ke Telegram belum diuji, dan pada uji ulang satu kalimat balasan AI ("akan menandainya di daftar H-3, H-1, dan hari-H secara otomatis") masih bisa terbaca seolah pengingat jalan sendiri, padahal daftar baru muncul saat Anda memintanya dan tidak ada pesan yang terkirim ke pasien. Uji pemasangan dan pemicu di OpenClaw: 6 dari 6 lulus (`examples/UJI-PLATFORM.md`).

## Bukti uji di bot Telegram

Diuji di bot Telegram uji (bot OpenClaw asli di grup uji internal Komunitech), 2 Okt 2026, tiga giliran percakapan. Skor tidak dicatat pada uji ini, dan versi skill yang diuji tidak tercatat (kira-kira 1.0.6).
- Tanpa skill: (pesan di grup uji internal Komunitech)
- Dengan skill: (pesan di grup uji internal Komunitech)
Hasilnya: tanpa skill, AI langsung memasang pengingat otomatis ke grup, melanggar aturan bahwa draf dikirim oleh staf. Dengan skill, tanggal dihitung benar ("3 hari lagi" menjadi Senin 5 Okt), izin pasien dicatat, pasien tanpa izin disaring, dan draf disiapkan untuk disalin staf.

Setelah uji ini skill diperbaiki di versi 1.0.7–1.0.8 (teks untuk grup staf tanpa nomor dan keterangan medis, izin pengingat tidak dianggap izin promosi, rujukan laporan dipertegas; versi terkini 1.0.9, sedangkan versi yang tampil di bot saat uji itu bukan 1.0.9). Perbaikan itu belum diuji ulang di bot Telegram.

## FAQ
**Apakah skill ini menyimpan rekam medis atau diagnosis pasien?**
Tidak. Yang disimpan hanya nama panggilan, nomor WA, jenis kunjungan umum (kontrol, vaksin, cabut
jahitan, dll.), dan tanggal. Skill ini dirancang menolak kalau isian jenis kunjungan atau catatan
menyerupai nama penyakit/diagnosis.

**Apakah pesan pengingat dikirim otomatis ke pasien?**
Tidak. Skill ini hanya menyiapkan draf. Staf klinik yang menyalin dan mengirimnya sendiri dari WA
klinik. Karena tidak ada pesan otomatis, risiko nomor WA klinik diblokir lebih kecil; staf tetap perlu memeriksa penerima sebelum mengirim.

**Bagaimana kalau pasien minta datanya dihapus?**
Tinggal minta ke asisten "hapus data [nama/nomor]". Data dihapus dari file lokal,
sesuai hak pasien menurut UU PDP 27/2022. Salinan cadangan atau berkas yang Anda buat sendiri perlu dihapus terpisah.

## Riwayat perubahan

Versi terkini: **1.0.9**. Rincian teknis tiap versi ada di `CHANGELOG.md` di folder skill ini.
