# Kurasi: pataanggs/indonesian-writing-skills

Tanggal tinjau: 2026-09-23 · Peninjau: agent kurator · Status: **PERLU REVIEW (pemilik)**

## 1. Identitas

| Item | Isi |
|---|---|
| Nama | indonesian-writing-skills: 2 skill (`indonesian-writing`, `bahasa-teknis-terkendali`) |
| URL | https://github.com/pataanggs/indonesian-writing-skills |
| Ditemukan lewat | Pencarian web "SKILL.md agent skills Indonesia" |
| Pembuat | pataanggs ("Indonesian Writing Skill contributors") |
| Update terakhir | 2026-09-17 (2 commit, keduanya 2026-09-17) |
| **Lisensi (file LICENSE dibaca langsung)** | **MIT**, "Copyright (c) 2026 Indonesian Writing Skill contributors". Ada `ATTRIBUTION.md` rinci. |

### Ringkasan isi
- `indonesian-writing` (SKILL.md 303 baris + 10 referensi: EYD V 578 baris, kata baku, pilihan kata, serapan, padanan istilah, frasa terlarang, kalimat, marketing, SEO, website-UX, akademik) dan `scripts/check.mjs` (linter Node untuk frasa slop dan kata tidak baku).
- `bahasa-teknis-terkendali`: bahasa terkendali untuk teks teknis dan instruksi antar-agent (terinspirasi prinsip ASD-STE100, bukan salinannya) dengan `scripts/lint.mjs`.
- `ATTRIBUTION.md` menyebut bahan awal: `ardianryan/eyd-v` (MIT), `fathurwithyou/indonesia-eyd-writing-skill` (MIT), `danyuchn/asd-ste100-skill` (MIT), dan `alvinindra/bahasa-skills` (tanpa lisensi, diklaim "hanya struktur, teks tidak disalin").

## 2. Audit keamanan (Tahap 3)

| Pemeriksaan | Hasil |
|---|---|
| `bin/cli.mjs` | Installer lokal (salin `skills/` ke direktori agent). Hanya modul `node:fs`/`os`/`path`. Tidak ada jaringan. Tidak dijalankan. |
| `scripts/check.mjs`, `lint.mjs` | Hanya membaca file teks dan menjalankan regex (`re.exec` adalah regex, bukan eksekusi perintah). Tidak ada jaringan atau `child_process`. |
| Kredensial / `curl \| bash` / obfuscation / injeksi | Tidak ada. |
| Karakter tersembunyi | Tidak ada. |

**Hasil audit keamanan: LULUS.**

## 3. Temuan lisensi / asal-usul (penting)

Perbandingan otomatis baris per baris (baris lebih dari 40 karakter, tanpa baris URL):
- **82 baris identik kata per kata** dengan `alvinindra/bahasa-skills` yang **tidak berlisensi**. Rinciannya: 52 di `references/frasa-terlarang.md`, 7 di `website-ux.md`, 7 di `akademik.md`, 5 di `marketing.md`, 4 di `examples/sebelum-sesudah.md`, 3 di `seo.md`, dan sisanya tersebar.
- **0 dari 82 baris itu** ditemukan di dua repo MIT yang disebut sebagai sumber (`ardianryan/eyd-v`, `fathurwithyou/indonesia-eyd-writing-skill`). Artinya baris itu kemungkinan besar berasal dari repo tak berlisensi, bertentangan dengan klaim `ATTRIBUTION.md` bahwa "isi teksnya tidak disalin".
- `bahasa-teknis-terkendali`: tidak ditemukan baris identik dengan alvinindra.

Sebagian baris itu pendek dan faktual (misalnya "Save / Cancel / Delete → Simpan / Batal / Hapus"), yang bisa jadi tidak dilindungi hak cipta. Namun tabel frasa terlarang lengkap dengan penggantinya adalah susunan kreatif. Lisensi MIT dari pataanggs **tidak dapat memberi izin atas teks yang bukan miliknya**.

## 4. Penilaian

- **Kualitas: 8/10.** Paling lengkap secara kaidah (EYD V per pasal, dengan tiga koreksi atas klaim keliru yang beredar), sumbernya berlabel, dan ada linter.
- **Tumpang tindih:** sama dengan bahasa-skills, yaitu lapisan mutu bahasa untuk semua skill tulis kita.
- **Keputusan: INSPIRASI SAJA — PERLU REVIEW.** Sesuai aturan "ragu → jangan masuk produk berbayar". Pengecualian yang bisa diusulkan ke pemilik:
  - `references/eyd-v.md` dan `kata-baku.md` (ringkasan peraturan resmi, tanpa baris identik yang signifikan) dan `bahasa-teknis-terkendali` bisa dikurasi (MIT) **setelah** pemilik menyetujui. Relevansi `bahasa-teknis-terkendali` untuk UMKM rendah.
  - Sumber MIT yang lebih bersih untuk kaidah EYD: `ardianryan/eyd-v` dan `fathurwithyou/indonesia-eyd-writing-skill`. Keduanya layak ditinjau penuh di sesi berikutnya.

## 5. Usulan jika disetujui
- Port linter `check.mjs` ke Python standar (`scripts/cek_bahasa.py`) dengan daftar aturan yang kita susun sendiri dari EYD V/KBBI. Linter ini dipakai sebagai pemeriksa akhir opsional di skill tulis (caption, surat, broadcast).
- Atribusi MIT pataanggs (dan upstream MIT yang relevan) di `ATTRIBUTION.md`.
