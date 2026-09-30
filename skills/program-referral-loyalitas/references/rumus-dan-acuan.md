# Rumus & Acuan (untuk hitung manual bila script tidak bisa jalan)

Semua angka di skill ini seharusnya keluar dari `scripts/hitung_referral.py`. Rumus ini hanya cadangan; bila dipakai, tulis "dihitung manual".

## Istilah
- **AOV** = nilai pesanan rata-rata (Rp).
- **Margin kotor** = laba kotor / harga jual (bukan markup = laba / modal).
- **Laba kotor per pesanan (LPO)** = AOV x margin, dibulatkan ke rupiah terdekat.
- **Referral berhasil** = teman benar-benar membeli dan pesanannya selesai. Hadiah dibayar hanya untuk ini.

## Rumus
| Hal | Rumus |
|---|---|
| Biaya per referral | hadiah perujuk + hadiah/diskon teman + biaya lain |
| Hadiah persen | AOV x persen (dibulatkan ke rupiah terdekat) |
| Laba pesanan pertama setelah hadiah | LPO - biaya per referral |
| Pesanan untuk balik modal | naik ke atas (biaya per referral / LPO), minimal 1 |
| Bulan balik modal | naik ke atas ((pesanan balik modal - 1) / frekuensi beli per bulan) |
| Laba kotor seumur pelanggan | LPO x frekuensi per bulan x umur pelanggan (bulan) |
| Batas hadiah aman | turun ke bawah (laba seumur pelanggan x 30%) |
| Hadiah perujuk maksimal | batas aman - hadiah teman - biaya lain (minimal 0) |
| Hadiah poin (% belanja) | nilai 1 poin / belanja per 1 poin |
| Porsi margin yang dipakai poin | hadiah poin % / margin % |
| Poin per transaksi | turun ke bawah (nilai transaksi / belanja per poin) |
| Biaya poin per bulan (maks) | omzet x hadiah poin % |
| Liability poin (maks) | poin beredar x nilai 1 poin |
| Perkiraan setelah breakage | nilai maks x (1 - breakage %) |
| Pembeli baru (simulasi) | perujuk x teman per perujuk x % teman membeli (tiap tahap dibulatkan ke orang terdekat) |
| ROI referral | (laba kotor dari pembeli baru - biaya hadiah) / biaya hadiah |

## Aturan praktis (bukan hukum, sebutkan sebagai "aturan praktis")
- Total hadiah per referral <= 30% dari laba kotor seumur pelanggan (dapat disesuaikan lewat `--porsi-ltv`).
- Hadiah poin sebaiknya <= 50% dari margin kotor; >= 100% margin berarti rugi tiap penukaran.
- Sisihkan dana sebesar liability poin maksimal bila ingin menjamin semua poin bisa ditukar.
- Angka skenario bawaan simulasi (merujuk 5/10/15% pelanggan, 1-2 teman per perujuk, 20-30% teman membeli) adalah tebakan awal untuk latihan, bukan benchmark pasar. Ganti dengan data sendiri setelah 1 bulan.

## Metrik pantau
Perujuk aktif (merujuk >= 1 orang dalam 30 hari), tingkat teman yang membeli, biaya per referral berhasil, persen pelanggan baru dari teman, laba pesanan pertama setelah hadiah, poin beredar & yang ditukar.
