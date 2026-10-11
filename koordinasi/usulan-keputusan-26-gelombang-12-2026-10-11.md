# Usulan keputusan pemilik no. 26 — Gelombang Telegram 12

**Tanggal usulan:** 2026-10-11 (Akun C, cron otomasi)  
**Dasar:** `promosi/SEBELUM-SESUDAH.md` (LULUS, belum tampil di gelombang 1–11b), pra-cek `koordinasi/pracek-telegram-g12-2026-10-10.md` (semua LOLOS).

## Rekomendasi

**Setuju** kirim **gelombang 12**: **4 skill × 2 pesan (TANPA skill / DENGAN skill)** = **8 pesan**, di **topik forum baru** (mis. "G12 — tampilan sebelum/sesudah"), urutan berurutan dengan jeda, **tanpa** balas-otomatis antar-bot.

## Daftar skill & pesan uji (fiktif)

| # | Skill | Versi | Selisih OC (acuan promosi/uji) | Pesan uji (ringkas) |
|---|--------|-------|--------------------------------|---------------------|
| 1 | `iterasi-dari-masukan-pelanggan` | 1.0.10 | 6,9 → 8,6 (+1,7) | Toko Kue Nara: chat WA + ulasan Shopee Sept — apa dibenahi duluan? (data: `examples/data/chat-wa.txt`, ulasan Shopee) |
| 2 | `cek-risiko-dan-asuransi-usaha` | 1.0.2 | 6,6 → 9,0 (+2,4) | Kafe ruko dekat kali Bekasi, biaya & banjir 2020 (`01-kafe-bekasi.json`) |
| 3 | `cari-prospek-web` | 1.0.2 | 6,7 → 8,2 (+1,5) | Kemasan ramah lingkungan — 15 calon kafe/katering/toko kue Bandung + kontak + prioritas |
| 4 | `persiapan-jual-atau-wariskan-usaha` | 1.0.1 | 6,0 → 8,6 (+2,6) | Warung bakso Pak Joko Surabaya, laba & utang, mau jual 2026 (S1 uji OpenClaw) |

**Tidak ikut gelombang ini (sudah pra-cek LOLOS, cadangan gelombang berikutnya):** `checklist-keamanan-pangan-usaha` v1.0.0.

## Prosedur teknis (sama G11b)

1. Backup config + skill bot uji.
2. Buat pasangan topik TANPA/DENGAN per skill; topik TANPA → `skills: []`; topik DENGAN → hanya skill itu.
3. **Restart gateway** setelah ubah `channels.*` (`gw-cek.sh`).
4. Kirim berurutan (maks 8 pesan), kumpulkan jawaban, nilai tanpa→dengan, tulis `koordinasi/telegram-gelombang-12-<tanggal>.md`.
5. Lapor ringkas ke topik **242** (bukan gelombang tampilan tanpa persetujuan ini).

## Alasan

- Keempat skill **LULUS** gate OpenClaw (sesudah ≥ 8, selisih ≥ 1,5); pra-cek Telegram **LOLOS** (jawaban panjang utuh di chat, termasuk `cari-prospek-web` dengan alat web).
- `cari-prospek-web` **tidak** diarsip (keputusan 24: web_search hidup, uji ulang LULUS 2026-10-10).
- C5 (tagih-piutang, cek-risiko, persiapan-jual revisi) sudah diuji Akun C; branch gabungan `cursor/iterasi-otomatis-akun-c-2145` / lanjutan iterasi menunggu merge Akun A/B ke default + promosi.

## Jawaban pemilik (isi setelah balas di Telegram)

_(kosong — tunggu "setuju" / revisi daftar skill)_
