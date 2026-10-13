# Promo 11.11 Sampai Lebaran, Tetap Untung

**Rencana promo lengkap untuk momen belanja besar, dengan hitungan margin yang langsung memberi tahu kalau diskonmu bikin rugi.**

## Manfaat
- ✅ Tahu diskon maksimal yang aman sebelum promo dimulai, bukan setelah rugi
- ✅ Bandingkan diskon, flash sale, bundling, beli 2 gratis 1, voucher, dan gratis ongkir dalam satu tabel
- ✅ Tahu berapa unit yang harus terjual agar laba sama dengan hari biasa dan agar biaya iklan tertutup
- ✅ Linimasa bertanggal (H-14 sampai H+7; Lebaran H-30 sampai H+14) lengkap dengan nama hari
- ✅ Syarat & ketentuan promo yang jujur, siap tempel, dan aman dari aturan perlindungan konsumen

## Cocok untuk siapa
- Seller Shopee, Tokopedia, TikTok Shop yang ingin ikut 9.9, 10.10, 11.11, 12.12 Harbolnas
- Pemilik toko online & offline yang merencanakan promo Ramadan, Lebaran, gajian, tahun baru, atau back to school
- Admin/marketing yang harus mengajukan rencana & anggaran promo ke pemilik usaha

## Contoh sebelum & sesudah
**Sebelum:** "Kasih diskon 30% aja biar laku." Setelah 11.11 selesai, omzet naik tapi saldo tidak bertambah karena laba per kaos tinggal Rp 2.820.

**Sesudah (cukup ketik):** "Mau ikut 11.11. Kaos harga 89 ribu, modal 52 ribu, potongan Shopee total 10% + 1.250 per pesanan. Biasanya laku 50 per minggu. Enaknya promo apa?"
→ Tabel 3 opsi: diskon 30% (⚠️ tipis, laba Rp 2.820/kaos), diskon 20% (✅ laba Rp 10.830), bundling 3 kaos Rp 229.000 (✅ laba Rp 16.283/kaos), diskon maksimal agar tidak rugi 33,5%, target minimal 124 kaos agar laba setara minggu biasa, plus linimasa dan S&K promo.

**Hasil uji (angka nyata):** uji banding tanpa vs dengan skill oleh agen penguji independen (simulasi Claude Code; serum harga Rp 120.000, modal Rp 45.000, rencana diskon 40% di 11.11).
- Tanpa skill: satu skenario dihitung benar (laba Rp 17.110 per serum), tetapi laba toner diskon 30% meleset ("sekitar Rp 16.000", yang benar Rp 16.950), tidak ada batas diskon aman, linimasa tanpa tanggal, dan disarankan memasang harga coret tanpa peringatan hukum.
- Dengan skill: semua mekanisme (diskon, bundling, beli 2 gratis 1, voucher, subsidi ongkir) dibandingkan dalam satu tabel. Diskon maksimal sebelum rugi 56,2% (serum) dan 40,5% (toner dengan ongkir); diskon 40% perlu terjual 3,47 kali lipat penjualan biasa agar laba setara; laba bersih kampanye Rp 4.643.100 setelah iklan; linimasa bertanggal; ada peringatan harga coret (UU 8/1999 Pasal 11 huruf f).
- Skor penguji independen: 8 dari 10; 300 dari 300 kombinasi hitungan cocok dengan kalkulator terpisah.

## Cara pakai
Setelah terpasang, cukup ketik permintaan biasa ke AI agent kamu, misalnya:
- "Bikinin rencana promo Harbolnas 12.12 buat 3 produk saya"
- "Diskon 25% buat skincare harga 120 ribu modal 70 ribu masih untung nggak?"
- "Susun jadwal promo Lebaran tahun depan, Lebarannya perkiraan 10 Maret 2027"

## Instalasi singkat
Salin folder `promo-kalender` ke folder skills AI agent kamu:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |

Panduan lengkap (termasuk Windows): lihat `CARA-INSTAL.md` di dalam paket.

**Status uji (jujur):** sudah diuji di OpenClaw (uji otomatis oleh agen AI, bukan oleh manusia) dan Claude Code (simulasi agen penguji). Codex dan Cursor memakai format SKILL.md yang sama, tetapi belum kami uji langsung.

## Catatan penting
- Ringkasan aturan promo (UU 8/1999 tentang Perlindungan Konsumen, berlaku per 23 September 2026) **bukan nasihat hukum**. Untuk undian berhadiah, tanyakan ke Dinas Sosial/Kemensos.
- Hitungan laba memakai angka modal dan potongan platform yang kamu berikan, jadi pastikan sesuai rincian di Seller Center-mu.

## FAQ
**Saya tidak tahu persen potongan marketplace saya. Bagaimana?**
Buka rincian penghasilan satu pesanan di Seller Center, atau menu biaya layanan. Skill sengaja tidak memakai angka tebakan karena tarif berbeda per kategori dan sering berubah.

**Tanggal Lebaran tahun depan belum pasti. Tetap bisa dibuat jadwalnya?**
Bisa. Pakai tanggal perkiraan, dan jadwal akan diberi label "perkiraan" sampai ada pengumuman resmi pemerintah.

**Apakah boleh menaikkan harga dulu lalu diberi diskon besar?**
Tidak. Itu dilarang UU Perlindungan Konsumen. Skill selalu memakai harga normal yang benar-benar berlaku dan menghitung persen hemat yang jujur.

## Catatan revisi 1.0.3 (2026-10-01)
- Temuan uji OpenClaw: target dihitung untuk promo 3 hari, tetapi linimasa & S&K memakai 1 hari; S&K memuat janji "dikirim maks 2 hari kerja" yang tidak disebut pemilik.
- Durasi promo kini ditetapkan sekali di awal dan wajib sama di target, linimasa, dan S&K (ada butir checklist). Hal operasional yang tidak diberikan pemilik (waktu kirim, kuota, retur) ditulis `[isi: …]`, bukan dikarang. Script tidak berubah.
