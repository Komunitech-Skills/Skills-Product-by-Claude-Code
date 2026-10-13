# Tak Ada Lagi Pasien Lupa Kontrol atau Vaksin

**Setiap pagi, asisten AI Anda menyiapkan daftar pasien yang harus diingatkan hari ini, lengkap dengan draf pesan WA sopan siap disalin staf — tanpa menyimpan rekam medis.**

Diuji AI penguji independen di OpenClaw: 3 → 8,5 dari 10 (tanpa skill pasien dicatat tanpa persetujuan dan pengiriman otomatis dijanjikan; dengan skill persetujuan ditanyakan dan pesan hanya disiapkan sebagai draf untuk staf).

> **Penting:** skill ini **belum direview tenaga medis** dan bukan alat diagnosis. Data pasien disimpan minimal (nama panggilan, nomor WA, jenis kunjungan, tanggal), hanya di komputer klinik Anda. Pesan hanya draf yang dikirim staf klinik. Contoh di bawah fiktif.

> **Yang Anda butuhkan:** AI agent yang mendukung skill (OpenClaw, Claude Code, Codex, atau Cursor — langganan AI-nya ditanggung sendiri) di komputer Windows/Mac/Linux. Python 3 (bawaan Mac/Linux, unduh gratis di Windows) untuk skrip hitung; tanpa Python skill tetap berjalan dengan hitungan oleh AI. Tidak perlu API key atau akun tambahan dari Komunitech.

## Manfaat
- ✅ **Cukup ketik satu kalimat.** "Catat Bu Sari, kontrol gigi 10 hari lagi, WA 0812..., setuju diingatkan" langsung tersimpan.
- ✅ **Daftar H-3 (3 hari sebelum jadwal), H-1, hari ini, dan terlambat** — jelas dan otomatis dari tanggal yang Anda masukkan, tidak perlu dihitung manual.
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

**Sesudah (cukup ketik):** "Catat Bu Sari, kontrol gigi 10 hari lagi, WA 0812-0000-1111, dia setuju diingatkan."
→ Tersimpan. 3 hari sebelumnya, daftar pagi menampilkan (contoh dengan data fiktif, disusun mengikuti format keluaran skill):
```
H-3 (1)
  #1 Bu Sari | Kontrol gigi | 6 Okt 2026 | 0812-0000-1111

DRAF PESAN (salin & kirim sendiri, JANGAN dikirim otomatis):

#1 Bu Sari (0812-0000-1111):
Halo Bu Sari, ini pengingat dari kami untuk jadwal kontrol gigi Anda pada 6 Okt 2026. Mohon
konfirmasi kehadiran Anda. Kalau perlu mengubah jadwal, silakan balas pesan ini. Terima kasih.
```
Staf tinggal salin, buka WA klinik, tempel, dan kirim. Sudah datang? "Bu Sari sudah datang, jadwalkan lagi 3 bulan lagi" — jadwal berikutnya otomatis tercatat.

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

**Hasil uji (angka nyata):** uji OpenClaw (uji otomatis agent, home terisolasi), 2026-10-01, skor 1–10 penguji independen. Sumber: `examples/00-openclaw-sebelum-sesudah.md`. Satu skenario pengingat dengan info kurang (tanpa nomor WA dan tanpa persetujuan pasien), uji pertama: tanpa skill **3** → dengan skill **8,5**. Tanpa skill, AI mencatat pasien tanpa persetujuan dan menjanjikan pengiriman otomatis; dengan skill, persetujuan ditanyakan dan pesan hanya disiapkan sebagai draf untuk staf. Uji pemasangan dan pemicu di OpenClaw: 6 dari 6 lulus (`examples/UJI-PLATFORM.md`).

## Bukti uji di bot Telegram

Diuji di bot OpenClaw asli (grup uji Komunitech, tautan hanya terbuka untuk anggota grup): gelombang 2–3, 2026-10-02 (3 giliran). Versi yang diuji tidak tercatat di catatan gelombang (versi repo saat itu: 1.0.6).
- Tanpa skill: https://t.me/c/4407409583/515/571 — skor tidak dicatat di gelombang itu
- Dengan skill: https://t.me/c/4407409583/241/574 — skor tidak dicatat di gelombang itu
Verdik gelombang: tidak dicatat di gelombang itu — TANPA memasang pengingat otomatis (cron) ke grup, melanggar aturan draf dikirim staf; DENGAN menghitung tanggal benar ("3 hari lagi" menjadi Senin 5 Okt), mencatat izin, menyaring pasien tanpa izin, dan menyiapkan draf untuk disalin staf.

Diperbaiki di versi 1.0.7–1.0.8 (teks grup staf tanpa nomor/keterangan medis, izin pengingat bukan izin promo, rujukan laporan dipertegas; versi terkini 1.0.8), belum diuji ulang di bot Telegram.

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

Versi terkini: **1.0.8**. Rincian teknis tiap versi ada di `CHANGELOG.md` di folder skill ini.
