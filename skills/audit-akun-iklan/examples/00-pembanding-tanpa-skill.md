# Uji A/B - tanpa skill vs dengan skill (penguji independen, Akun B)

> 2026-09-26, simulasi agent. Skenario normal 1 (`01-toko-skincare-tiktok-uji-akun-b.md`):
> toko skincare, TikTok Ads ke website Rp4,5 jt + TikTok Shop GMV Max Rp6 jt, serum Rp89rb, modal
> Rp32rb, potongan 14,5% + afiliasi 10%, kemas Rp1.500. Bukti yang sama diberikan ke kedua agent.
> Keterbatasan: output "tanpa skill" ditulis oleh agent umum yang sama tanpa membaca folder skill;
> ini simulasi, bukan uji buta dengan juri terpisah.

## A. Tanpa skill (ringkasan output agent umum)
> Berikut beberapa hal yang bisa dicek:
> 1. **Target audiens** – pastikan menyasar wanita 18–34 yang tertarik skincare.
> 2. **Materi** – gunakan video UGC yang autentik, hook 3 detik pertama, perbanyak variasi.
> 3. **Pixel** – pastikan TikTok Pixel terpasang dan event Complete Payment berjalan.
> 4. **Anggaran** – TikTok menyarankan anggaran minimal 50× CPA (?) agar lolos fase belajar.
> 5. **ROAS** – ROAS sehat untuk skincare biasanya 3–4. ROAS impas Anda kira-kira 89.000 ÷ (89.000 − 32.000) ≈ **1,56**.
> 6. **GMV Max** – coba naikkan anggaran agar algoritme punya lebih banyak data.
> 7. Keamanan akun – aktifkan 2FA.
> Secara umum akun Anda cukup baik tetapi perlu optimasi materi.

## B. Dengan skill
Skor **53,9/100 – Perlu perbaikan – final** (bukti 95,8% / 100%), 8 kategori per platform, 15 perbaikan
berurutan (dampak × kemudahan) + kenaikan skor per perbaikan, rencana Senin 28 Sep – Minggu 4 Okt,
ROAS impas **2,65** (laba Rp33.695 setelah potongan Rp21.805 + kemas), 3 masalah terbesar: admin
lama + 2FA mati, target ROI 2,0 < impas 2,65, event pelacakan meleset 27% dan satu kampanye tak tercatat.

## Perbandingan
| Aspek | Tanpa skill | Dengan skill |
|---|---|---|
| ROAS impas | **1,56 – salah** (lupa potongan 24,5% & kemas) → akan menyetujui target ROI 2,0 yang rugi | **2,65 – benar**, diverifikasi Decimal |
| Temuan target ROI 2,0 di bawah impas | Tidak ditemukan (malah menyarankan naikkan anggaran GMV Max) | Prioritas #3, +15 skor |
| Keamanan akun (admin lama) | Disebut umum di urutan akhir | Prioritas #1 dengan bukti |
| Skor & urutan kerja | Tidak ada; "cukup baik" (tanpa dasar) | 0–100 berbobot, cakupan bukti, urutan dampak × kemudahan |
| Rencana eksekusi | Tidak ada | 7 hari, ±1–2 jam/hari, hari "diam" untuk fase belajar |
| Klaim angka platform | "50× CPA (?)" tanpa sumber; "ROAS sehat 3–4" benchmark tak berdasar | Patokan diberi label; ROAS dibandingkan ke impas milik sendiri |
| Jujur soal bukti | Tidak membedakan yang sudah/belum dicek | `tidak_tahu` untuk T07/T17, disebut di "belum bisa dinilai" |

**Kesimpulan:** dengan skill **jelas lebih baik**. Selisih paling berbahaya ada di ROAS impas: tanpa
skill agent menghitung 1,56 dan tidak melihat bahwa target ROI 2,0 membuat setiap pesanan rugi.
Kelemahan versi skill yang terlihat di uji ini: saran T08 (naikkan anggaran untuk belajar) dan T09
(matikan ad group rugi) tidak direkonsiliasi otomatis.
