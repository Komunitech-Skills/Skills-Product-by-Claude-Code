# Dasar Aturan PPh Final UMKM — berlaku per 23 September 2026

> Ringkasan untuk alat bantu hitung, bukan nasihat pajak. Butir berlabel **BELUM TERVERIFIKASI** tidak boleh disampaikan sebagai kepastian; arahkan pengguna ke DJP (Kring Pajak 1500200 / pajak.go.id) atau konsultan pajak.

## PPh Final 0,5% (PP 55/2022 sebagaimana diubah PP 20/2026, ditetapkan 22 April 2026)
| Hal | Ketentuan | Status |
|---|---|---|
| Tarif | 0,5% × peredaran bruto (omzet) | Terverifikasi |
| Subjek | WP orang pribadi, PT perorangan, koperasi dengan omzet ≤ Rp4,8 miliar setahun | Terverifikasi |
| Orang pribadi | Omzet s.d. **Rp500 juta setahun tidak dikenai pajak**; 0,5% atas omzet di atasnya | Terverifikasi |
| Badan | Tanpa pembebasan Rp500 juta | Terverifikasi (dipakai skill) |
| CV, firma, PT biasa | Dikeluarkan dari skema; ada masa transisi | Lama transisi **BELUM TERVERIFIKASI** |
| Batas jangka waktu pemakaian tarif 0,5% | PP 55/2022 Pasal 59: OP 7 tahun pajak; koperasi, CV, firma, PT perorangan 4; PT 3; sejak tahun terdaftar (terdaftar sebelum PP 23/2018 → sejak 2018). Script menghitung tahun akhirnya dengan `--tahun-terdaftar` (v1.0.3) | Teks PP 55/2022 terverifikasi; perubahan/penghapusan oleh PP 20/2026 **BELUM TERVERIFIKASI** — selalu disebut bersama peringatan ini |
| Omzet melewati Rp4,8 M di tengah tahun | Berdasarkan PP 55/2022: tarif 0,5% tetap sampai akhir tahun pajak, tahun berikutnya tarif umum | Perlu dicek ulang terhadap PP 20/2026 — skill menyebut "umumnya" + arahkan ke DJP |
| Batas setor | Tanggal 15 bulan berikutnya (PMK 81/2024 Pasal 94); jatuh hari libur (Sabtu, Minggu, libur nasional, cuti bersama) → paling lambat hari kerja berikutnya (Pasal 100 ayat (1)) | Pasal dicocokkan dengan naskah resmi oleh skill kalender-pajak (2026-09-26). Data libur `libur-nasional-2026.csv` & `-2027.csv` disalin dari kalender-pajak (SKB 3 menteri; 2027 PERLU REVIEW terhadap lampiran resmi). Tahun tanpa data → hanya Sabtu/Minggu + peringatan |
| Penghasilan dikecualikan | Mis. jasa sehubungan pekerjaan bebas (dokter, notaris, konsultan, dll.) | Berdasarkan PP 55/2022; perlu dicek ulang |

## PPh 22 Marketplace (PMK 37/2025) — berlaku 1 Agustus 2026
- Marketplace yang ditunjuk memungut 0,5% dari omzet bruto pedagang dalam negeri (dilaporkan: Tokopedia, Shopee, Lazada, Blibli; TikTok Shop **BELUM TERVERIFIKASI**).
- Pedagang orang pribadi dengan omzet ≤ Rp500 juta dikecualikan **jika menyampaikan surat pernyataan** ke marketplace; bisa juga mengunggah SKB.
- DJP menyatakan ini bukan pajak baru, melainkan mekanisme pemungutan yang dapat diperhitungkan. **Cara memperhitungkannya terhadap PPh final UMKM tidak dihitung otomatis oleh skill** — arahkan ke DJP/konsultan.

## Keputusan desain skill
- PPh per bulan dibulatkan ke bawah ke rupiah penuh.
- Omzet kumulatif dihitung per tahun pajak (Januari–Desember).
- PPh 22 marketplace ditampilkan sebagai kolom informasi, tidak dikurangkan.

## Sumber
- DJP — PP 20/2026: https://www.pajak.go.id/en/node/119950
- DDTC — omzet s.d. Rp500 juta tetap bebas: https://news.ddtc.co.id/berita/nasional/1819765/ada-pp-baru-omzet-hingga-rp500-juta-bebas-pajak-masih-berlaku
- DJP — PPh 22 marketplace PMK 37/2025: https://pajak.go.id/en/node/120044
- DDTC — pajak marketplace & SKB: https://news.ddtc.co.id/berita/nasional/1821248/pajak-marketplace-segera-berlaku-merchant-perlu-pastikan-upload-skb
