# Uji A/B — Tanpa skill vs dengan skill (skenario normal #1: warung sembako 2 tahun)

> Penguji independen (Akun B), 2026-09-26. Permintaan dan data sama persis dengan `03-warung-sembako-dua-tahun-uji-akun-b.md`.
> **Keterbatasan:** jawaban "tanpa skill" adalah simulasi agent umum oleh penguji tanpa membaca SKILL.md/references. Ini bukan sesi model terpisah, jadi dicatat apa adanya.

**Permintaan:** "Ini angka warung sembako saya 2024 dan 2025 [tabel]. Omzet naik tapi kok kas makin tipis? Saya mau ambil KUR cicilan 750 ribu per bulan, aman nggak?"

## A. Tanpa skill (jawaban agent umum, diringkas)
> Berikut analisis rasio keuangan warung Ibu tahun 2025:
> - **Current ratio** = 58,7 ÷ 29 = 2,02 → baik (standar industri 2 kali).
> - **Quick ratio** = (58,7 − 48) ÷ 29 = 0,37 → **sangat rendah**, jauh di bawah standar 1,5. Ini tanda likuiditas bermasalah.
> - **Debt to equity** = 29 ÷ 47,7 = 0,61 → baik (di bawah 0,9).
> - **Net profit margin** = 16,8 ÷ 420 = 4% → rendah.
> - **ROA** = 16,8 ÷ 76,7 = 21,9%; **ROE** = 35,2% → baik.
>
> Kenapa kas tipis? Kemungkinan karena stok bertambah dan utang ke supplier naik. Saran: kelola stok, tagih piutang, pisahkan uang pribadi dan usaha, buat anggaran.
>
> Soal KUR: laba per bulan sekitar 1,4 juta. Cicilan 750 ribu itu lebih dari separuh laba, jadi **cukup berat**. Sebaiknya pertimbangkan plafon yang lebih kecil. Umumnya bank menyarankan cicilan maksimal 30–40% dari penghasilan.
>
> *Catatan: konsultasikan dengan ahli keuangan.*

Ciri khas jawaban tanpa skill:
1. Memakai **standar perusahaan umum (Kasmir: quick ratio 1,5)** untuk warung → rasio cepat 0,37 dicap "sangat rendah/bermasalah". Menurut logika `references/ambang-wajar.md`, ambang itu membuat hampir semua warung sehat dinilai bahaya.
2. **Tidak ada perbandingan 2024** kecuali kalimat umum. Tidak ada angka rasio kas 0,47 → 0,22, DER 0,35 → 0,61, atau margin kotor 15% → 14%.
3. **Tidak menghitung umur stok, lama piutang, lama bayar pemasok, atau siklus kas.** Padahal itu jawaban langsung untuk "kenapa kas tipis".
4. Hitungan di kepala, tanpa jejak rumus/verifikasi. Tidak ada status per rasio, tidak ada ambang tertulis dan sumbernya.
5. Saran generik ("kelola stok, buat anggaran"). Batas cicilan "30–40%" disebut tanpa dasar.
6. Disclaimer tipis. Tidak menyebut bahwa keputusan kredit ada di bank (SLIK, agunan, dll.).

## B. Dengan skill (output `scripts/rasio.py`, lengkap di `03-warung-sembako-dua-tahun-uji-akun-b.md`)
- Ringkasan awam: untung Rp 16,8 jt (4,0%), 7 baik / 4 waspada / 0 bahaya, yang perlu diperhatikan: rasio cepat, margin kotor, margin bersih.
- 4 tabel (likuiditas, profitabilitas, solvabilitas, aktivitas) berisi nilai, rumus, ambang **dagang**, status, dan arti sehari-hari.
- Tabel tren 19 baris: rasio kas 0,47 → 0,22, DER 0,35 → 0,61, margin kotor 15,0% → 14,0%, penjualan & laba +16,7%.
- Kesiapan KUR: ✓/✗ per poin, cicilan 53,6% → 🔴 TERLALU BERAT (ambang sama dengan `pengajuan-kur`), bank yang memutuskan.
- 5 saran berurutan dan konkret (kecilkan plafon, promo stok lama, cek harga beli, pangkas biaya, catat stok per barang) plus rujukan skill terkait.
- Asumsi & disclaimer lengkap (bukan nasihat investasi/kredit, ambang bukan standar OJK/bank).

## Penilaian berdampingan (1–5)
| Aspek | Tanpa skill | Dengan skill |
|---|:-:|:-:|
| Ketepatan angka (diverifikasi Decimal) | 4 (benar untuk yang dihitung) | 5 (35/35 cocok) |
| Kelengkapan rasio | 2 | 5 |
| Ambang sesuai jenis usaha | 1 (standar perusahaan umum) | 5 |
| Menjawab "kenapa kas tipis" | 2 | 4 (tren & siklus kas; tren campur basis menyamarkan kenaikan umur stok, lihat HASIL-UJI) |
| Kesiapan KUR & kejujuran soal bank | 3 | 5 |
| Saran konkret | 2 | 4 |
| Bahasa awam & siap tempel | 3 | 5 |
| **Total (maks 35)** | **17** | **33** |

**Kesimpulan:** dengan skill **jelas lebih baik**. Syarat A/B Tahap 6 terpenuhi, jadi skor tidak dibatasi 6.

## Bahan "sebelum/sesudah" untuk README
- **Sebelum:** "Quick ratio 0,37, jauh di bawah standar 1,5, likuiditas bermasalah. Kelola stok dan buat anggaran."
- **Sesudah:** "Rasio cepat 0,37 🟡 (warung wajar ≥ 0,5). Rasio kas turun dari 0,47 ke 0,22 dan utang pemasok naik dari 15 jt ke 26 jt: kas terserap ke stok. Cicilan 750 rb = 53,6% laba per bulan → terlalu berat. Kecilkan plafon atau pilih tenor lebih panjang."
