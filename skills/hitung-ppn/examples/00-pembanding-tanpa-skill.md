# 00 — Uji A/B: S1 dengan vs tanpa skill

**Input pengguna (sama persis dengan S1):**
> Saya PKP, mau tagih jasa maintenance server ke klien Rp 12.500.000 belum termasuk PPN. PPN-nya berapa dan totalnya jadi berapa?

## Output TANPA skill (AI agent biasa, tanpa membaca skill)
```
PPN yang berlaku sekarang 12%. Tapi untuk barang/jasa yang bukan barang mewah,
PPN 12% dihitung dari DPP nilai lain 11/12, jadi efektifnya 11%.

PPN = 11% x Rp 12.500.000 = Rp 1.375.000
Total = Rp 12.500.000 + Rp 1.375.000 = Rp 13.875.000

Jangan lupa buat faktur pajaknya ya.
```

## Output DENGAN skill
Lihat `01-jasa-pkp-harga-sebelum-ppn.md` (ringkas):
```
- Harga sebelum PPN (DPP): Rp 12.500.000
- DPP nilai lain (11/12): Rp 11.458.333,33
- PPN 12%: Rp 1.375.000 (setara 11% dari harga)
- Total dibayar klien: Rp 13.875.000
Cara hitung + aturan pembulatan (ke bawah) + catatan faktur Coretax
Dasar: UU HPP & PMK 131/2024, berlaku per 23 September 2026 + disclaimer + Kring Pajak
```

## Perbandingan
| Aspek | Tanpa skill | Dengan skill |
|---|---|---|
| Angka PPN & total | Benar (kasus angka bulat) | Benar, dihitung script & diverifikasi |
| DPP nilai lain (untuk isian faktur) | Tidak ditampilkan | Ditampilkan 2 desimal |
| Aturan pembulatan | Tidak disebut | Disebut (ke bawah, rupiah penuh) |
| Dasar hukum & tanggal berlaku | Tidak ada | Ada |
| Disclaimer/rujukan DJP | Tidak ada | Ada |
| Mode "harga sudah termasuk PPN" | Agent biasa rawan salah (mis. 12,5 jt ÷ 1,12) atau pembulatan tidak konsisten | Algoritma pasti: DPP bulat terbesar sehingga DPP + PPN ≤ harga |

## Penilaian
Untuk angka bulat seperti S1, agent tanpa skill yang pengetahuannya mutakhir **bisa** menghasilkan angka yang sama. Nilai tambah skill ada pada: kelengkapan (DPP nilai lain, pembulatan, dasar aturan bertanggal, disclaimer), konsistensi hasil pada kasus termasuk-PPN dan pecahan rupiah, serta pengingat PKP otomatis. Agent tanpa skill dengan pengetahuan lama sering masih memakai 12% penuh (total Rp 14.000.000) — kesalahan yang dicegah skill (lihat S3). **Kesimpulan: dengan skill lebih baik, tetapi selisihnya moderat untuk kasus sederhana.**
