# Papan Tugas — Kolaborasi 2 Akun Claude Code

Dibuat 2026-09-25 atas permintaan pemilik. Dibaca oleh **kedua** sesi di awal setiap giliran.

## Pembagian jalur (tetap — supaya tidak ada pekerjaan dobel)

| Akun | Jalur | Branch kerja |
|---|---|---|
| **Akun A** (sesi utama, routine tiap 3 jam) | Jalur 2 — produk lokal pengganti SaaS; Jalur 3 — solusi member VIP (OpenClaw); uji ulang & perawatan skill yang sudah ada | `claude/determined-gates-rh7l38` |
| **Akun B** (akun kedua) | Jalur 1 — kurasi (ATM) & kreasi skill baru | branch sesi Akun B sendiri — **tulis namanya di bawah** |

Branch Akun B: `(isi di commit pertama Akun B)`

## Aturan main
1. **Mulai dari kode terbaru.** Di awal giliran: `git fetch origin claude/determined-gates-rh7l38` lalu `git merge --ff-only origin/claude/determined-gates-rh7l38` (atau `git merge` biasa bila sudah pernah commit). Jangan rebase / force-push branch orang lain.
2. **Ambil tugas hanya dari kolom jalurmu.** Ubah status jadi `dikerjakan (Akun X, tanggal)` lalu commit & push segera.
3. **Satu skill = satu akun.** Jangan menyentuh folder `skills/<nama>` milik jalur lain. Perlu perubahan di sana → tulis di bagian "Permintaan antar-akun".
4. **Semua aturan CLAUDE.md tetap berlaku** (uji independen, A/B, banding pesaing, validate.py, lisensi, tanpa data pribadi, hemat context). Batas agent paralel (keputusan pemilik 2026-09-25): **Akun A maks 2**, **Akun B maks 4** (kuota Akun B lebih besar). Tetap hentikan batch baru bila context sesi > 600 ribu token atau limit "rejected".
5. **catalog.csv**: tambah/ubah hanya baris skill milikmu. Konflik saat merge diselesaikan Akun A.
6. **Laporan**: `reports/YYYY-MM-DD.md` milik Akun A; Akun B menulis di `reports/YYYY-MM-DD-akun-b.md`.
7. Akun A menggabungkan branch Akun B (merge commit, bukan rebase) setiap giliran bila ada commit `skill: ... (lulus)` baru.

## Jalur 1 — Akun B (dioper dari Akun A)

Sumber riset: `research/sources/kurasi-terbukti-2026-09-24.md`, `research/backlog.md`, `research/harga.md`. Contoh skill kurasi yang sudah lulus dan bisa ditiru polanya: `skills/copy-landing-page`, `skills/audit-seo-toko-online`, `skills/rencana-pelajaran-guru`.

| # | Tugas | Sumber / catatan | Status |
|---|---|---|---|
| B1 | ATM `pesan-prospek-wa` — pesan perkenalan/penawaran pertama via WA ke calon pelanggan | coreyhaines31/marketingskills `cold-email` (MIT). Bedakan tegas dari `follow-up-prospek` (itu urutan susulan). Tanpa blast; dikirim manusia | belum |
| B2 | ATM `brainstorming-ide-usaha` — sesi curah gagasan terstruktur untuk ide produk/promo/usaha | obra/superpowers `brainstorming` (MIT) — tulis ulang ±90%, konteks UMKM | belum |
| B3 | Kreasi `kontrak-kerja-pkwt` (HR) | Backlog #15. Verifikasi aturan PKWT terbaru (PP 35/2021 + perubahan UU Cipta Kerja/putusan MK) dari sumber resmi; disclaimer; model Opus | belum |
| B4 | Kreasi `kebijakan-privasi-pdp` (Legal) | Backlog #26. UU 27/2022 PDP + peraturan pelaksana terbaru (verifikasi); disclaimer; Opus | belum |
| B5 | Kreasi `kalender-pajak` (Pajak) | Backlog #28. Jatuh tempo setor/lapor 2026 (PMK terbaru, Coretax); Opus | belum |
| B6 | Kreasi `analisis-excel` (Data) | Backlog #27 — bedakan dari `rekap-penjualan-csv`; script Python standar | belum |
| B7 | Kreasi `sop-onboarding` (HR) | Backlog #36 — bedakan dari `sop-writer` | belum |
| B8 | Kreasi `tender-checklist` (Sales) | Backlog #33 — LPSE/SPSE; verifikasi Perpres PBJ terbaru | belum |
| B9 | `atur-keuangan-pribadi` (openaccountant, MIT) | **TUNGGU keputusan pemilik** (sinyal bukti tipis) | tertahan |
| B10 | `spt-tahunan-op-helper` | Backlog #29 — musiman (Jan–Mar); kerjakan menjelang musim | nanti |

## Jalur 2 & 3 — Akun A

| # | Tugas | Status |
|---|---|---|
| A1 | `laporan-iklan-mingguan` (celah paket VIP toko online) | uji 5/10 → revisi berjalan (Akun A, 2026-09-25) |
| A2 | Uji ulang `dolibarr-usaha` v1.0.2 | selesai 8/10 — siap uji platform asli & beta; B1 (draf ganda saat DPP bersen) & B2 (ENV kunci mengalahkan --kunci-file tanpa peringatan) untuk v1.0.3 |
| A3 | Masukkan `solusi-vip/` ke paket ZIP VIP (`build.py`) | tunggu keputusan pemilik |
| A4 | Pengingat kontrol/vaksin per pasien (klinik) | tunggu keputusan pemilik (penyimpanan data pasien) |
| A5 | Laporan status terjadwal ke klien (konsultan) | tunggu keputusan pemilik (kirim ke pihak luar) |
| A6 | Uji platform asli & program beta (skill lulus) | butuh pemilik/tim (`docs/uji-platform.md`, `docs/program-beta.md`) |

## Uji untuk Akun A — dikerjakan Akun B (penguji lintas akun = lebih independen)

Aturan: Akun B **hanya menulis ke `skills/<nama>/examples/`** skill milik Akun A (tidak mengubah kode, SKILL.md, catalog.csv). Ikuti CLAUDE.md Tahap 6 (5 skenario/uji ulang klaim, verifikasi angka independen, A/B & banding pesaing untuk uji pertama, `validate.py`, `scripts/uji_openclaw.sh`). Tambahkan bagian baru di akhir `examples/HASIL-UJI.md` (jangan hapus isi lama) + skor 1–10. Commit `uji: <nama> vX.Y.Z <skor>/10` di branch Akun B → Akun A yang merge & memperbarui catalog.csv. Ambil hanya item berstatus `siap diuji`.

| # | Skill Akun A | Yang diuji | Status |
|---|---|---|---|
| U1 | `laporan-iklan-mingguan` v1.0.1 | Uji ulang setelah revisi 4 cacat tinggi (sel Results kosong, baris total varian, pemilihan kolom Google Ads, mata uang non-IDR) + cacat sedang; ulang repro di examples/HASIL-UJI.md; verifikasi angka Decimal. Model: Opus | menunggu revisi Akun A |
| U2 | `dolibarr-usaha` v1.0.3 | Uji ulang B1 (draf ganda saat DPP bersen) & B2 (ENV kunci vs --kunci-file) setelah diperbaiki | belum dijadwalkan |

## Permintaan antar-akun
_(tulis di sini: dari, untuk, isi, tanggal)_
