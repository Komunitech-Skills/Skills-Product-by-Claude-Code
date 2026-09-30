# 00 - Uji banding pesaing: `referrals` (marketingskills) vs `program-referral-loyalitas`

> Uji independen Tahap 6 (2026-09-30). Skill pesaing **hanya dibaca untuk dinilai** (tidak disalin): https://github.com/coreyhaines31/marketingskills/blob/main/skills/referrals/SKILL.md (versi 2.0.1, MIT, Corey Haines; dibaca lewat raw.githubusercontent.com pada 2026-09-30). Catatan: skill kita diadaptasi dari sumber ini (lihat `ATTRIBUTION.md`), jadi ini sekaligus uji "menang telak atas sumbernya" (ATM).
>
> Skenario: sama dengan `06-uji-toko-hijab-shopee-wa.md`.

## Ringkasan pendekatan pesaing (dengan kata-kata penguji)
Pesaing meminta konteks dulu (jenis program, B2B/B2C, LTV, CAC, alat yang dipakai, anggaran), menjelaskan loop "momen pemicu -> berbagi -> konversi -> hadiah", pilihan hadiah satu sisi/dua sisi/bertingkat, anjuran menampilkan angka yang terasa lebih besar, daftar metrik, daftar periksa peluncuran, urutan email pengingat (hari 7/30/60), dan daftar alat SaaS (Rewardful, Tolt, Mention Me, Dub.co, Stripe, PartnerStack). Tidak ada perhitungan, script, template S&K, atau konteks Indonesia.

## Hasil bila skenario 1 dijalankan dengan pendekatan pesaing (disimulasikan penguji)
- Agent akan bertanya LTV, CAC, alat referral yang dipakai, B2B/B2C (sebagian sudah dijawab di prompt, sebagian tidak relevan untuk UMKM).
- Menyarankan dua sisi (sesuai), "lead with bigger number" -> "potongan Rp14.500" alih-alih "10%" (sesuai; skill kita juga memuat aturan ini).
- Menyarankan **hadiah bertingkat** dan **email pengingat hari 7/30/60 ke non-referrer**; untuk WA Indonesia ini condong ke pesan berulang yang bisa dianggap spam.
- Menyarankan alat Rewardful/Tolt/Stripe: berbasis Stripe/SaaS, tidak cocok untuk penjual Shopee + WA.
- Angka Rp36.000, Rp19.100, kuota 20, rugi Rp23.900 untuk opsi besar **tidak muncul** kecuali agent menghitung sendiri (tanpa aturan pembulatan).
- Mengutip "referred customers 16-25% higher LTV" tanpa sumber.

## Penilaian berdampingan (1-5)
| Kriteria | Pesaing `referrals` | Skill kita |
|---|---|---|
| Ketepatan angka (biaya, impas, kuota, poin) | 1 (tidak ada) | 5 (script, terverifikasi) |
| Siap pakai (S&K, teks, lembar catatan) | 2 (template email generik) | 5 |
| Relevansi Indonesia (Rupiah, Shopee/WA, UU) | 1 | 5 |
| Kepatuhan & etika (spam, PDP, piramida) | 2 (ada fraud rules singkat; tidak ada kepatuhan lokal) | 5 |
| Loyalitas poin/stempel & liability | 0 (tidak dicakup) | 5 |
| Strategi umum (momen, viral, afiliasi) | 4 (kuat untuk SaaS, bagian viral produk & afiliasi) | 4 (fokus UMKM; mekanisme viral produk digital sengaja tidak dipakai) |
| Kemudahan untuk awam | 2 (istilah LTV/CAC/SaaS) | 4 |
| **Total (maks 35)** | **12** | **33** |

## Kelebihan pesaing yang patut dipelajari (tanpa disalin)
- Diagnostik "apakah produk cocok viral dulu" sebelum memberi hadiah. Untuk UMKM bisa diterjemahkan sebagai "perbaiki produk/layanan dulu bila pelanggan belum puas" (skill kita sudah menyinggung lewat momen puas, bisa ditegaskan).
- Rencana uji A/B hadiah (nominal vs persen, satu vs dua sisi). Skill kita punya rencana 30 hari tetapi tidak menyarankan uji dua varian secara eksplisit. Temuan rendah.

**Kesimpulan:** skill kita **menang telak** atas pesaing/sumbernya untuk pasar sasaran. Nilai tambah ATM (script, lokalisasi, S&K, kepatuhan, poin & liability) nyata.
