# Usulan keputusan pemilik — gelombang tampilan 13 (Akun B, 2026-10-12)

**No. 29.** Dikirim ke Telegram topik "Ringkasan uji" (242) lewat bot penguji; jawaban pemilik di chat atau topik 242.

## Konteks

- Keputusan no. 28: gelombang 13 dst. untuk 17 skill `lulus` yang belum pernah tampil di bot asli, dikirim Akun B lewat bot uji kedua **@KTclaude2bot** (gateway aktif di sesi Akun B).
- Pra-cek `uji-tg.sh` 7 kandidat: `pracek-telegram-g13-2026-10-12.md` — 6 LOLOS, 1 GAGAL.

## Kandidat G13 (urut selisih promosi; `lolos_promosi`, sesudah ≥ 8, selisih ≥ 1,5)

| # | Skill | Tanpa → Dengan | Selisih | Pra-cek |
|---|---|---|---|---|
| 1–2 | `rapor-mingguan-ai` (tier vip) | 4,75 → 8,25 | +3,5 | LOLOS (4700 char; percobaan 1 timeout router) |
| 3–4 | `proses-pesanan-wa` | 5,5 → 8,4 | +2,9 | LOLOS (11202 char — pantau pemecahan pesan) |
| 5–6 | `analisis-selisih-anggaran` | 5,75 → 8,5 | +2,75 | LOLOS (3842 char) |
| 7–8 | `persiapan-jual-atau-wariskan-usaha` | 6,1 → 8,7 | +2,6 | LOLOS (8845 char) |
| 9–10 | `triase-email-masuk` | 5,5 → 8,0 | +2,5 | LOLOS (5116 char) — pengganti |

**Dicoret:** `landing-page-siap-tayang` (+3,7) — 2 dari 2 run bersih tidak memuat blok `index.html` di chat; hasil tidak bisa dinilai di Telegram. Perlu perbaikan skill (wajib tulis HTML utuh di chat atau lampirkan file) sebelum tampil.
**Cadangan:** `checklist-keamanan-pangan-usaha` (+2,4, LOLOS 7947 char).

Teks pesan: `koordinasi/alat-uji/pilot/msgs-g13.json` (data fiktif ditempel di pesan; mention @KTclaude2bot). Topik baru `G13 <skill> — TANPA/DENGAN skill`; topik TANPA `skills: []`; gateway restart sebelum kirim; 10 pesan berurutan dengan jeda (`kirim-urut2.py`); tanpa balas-otomatis.

## Usulan no. 29 (minta jawaban pemilik)

**a)** Setuju gelombang 13 = 10 pesan dari tabel di atas (rekomendasi).
**b)** Ganti isi: sebutkan skill (maks 5).
**c)** Tunda.

Setelah G13, antrean G14: `checklist-keamanan-pangan-usaha`, `sunting-tulisan-jelas`, `simulasi-cicilan-pinjaman`, `seleksi-cv-pelamar`, `cek-risiko-dan-asuransi-usaha`; lalu `cari-prospek-web` (butuh web_search hidup) dan `satu-lawan-satu-dan-umpan-balik` (perlu uji OpenClaw asli dulu).
