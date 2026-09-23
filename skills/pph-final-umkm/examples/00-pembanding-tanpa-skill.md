# 00 — Uji A/B: S1 dengan vs tanpa skill

**Input pengguna (sama persis dengan S1):**
> Saya jualan baju online, atas nama pribadi (bukan PT). Omzet 2026: Jan 38jt, Feb 42jt, Mar 55jt, Apr 61jt, Mei 70jt, Jun 88jt, Jul 95jt, Agu 102jt. Pajaknya berapa per bulan?

## Output TANPA skill (AI agent biasa, tanpa membaca skill)
```
Untuk UMKM orang pribadi berlaku PPh Final 0,5% (PP 55/2022), dengan omzet
sampai Rp500 juta per tahun tidak dikenai pajak.

Total omzet Jan–Agu = Rp551.000.000
Omzet kena pajak = 551 jt − 500 jt = Rp51.000.000
PPh final = 0,5% × Rp51.000.000 = Rp255.000

Jadi Januari–Juli Rp0, Agustus Rp255.000. Mulai September semua omzet kena 0,5%.
Setor paling lambat tanggal 15 bulan berikutnya.
Catatan: tarif 0,5% untuk orang pribadi hanya boleh dipakai maksimal 7 tahun.
```

## Output DENGAN skill
Lihat `01-olshop-pribadi-lewat-500-juta.md`: tabel 8 bulan (omzet, kumulatif, omzet kena pajak, PPh, PPh 22, tanggal setor per bulan, keterangan), ringkasan (sisa ruang ke Rp4,8 miliar), catatan penting (omzet semua usaha, dasar omzet bukan laba, pembulatan, status PP 20/2026 yang belum terverifikasi), disclaimer + dasar aturan bertanggal, dan peringatan bahwa batas setor Agustus sudah lewat.

## Perbandingan
| Aspek | Tanpa skill | Dengan skill |
|---|---|---|
| Angka Agustus | Benar (Rp255.000) | Benar, dihitung script & diverifikasi |
| Tabel per bulan + tanggal setor | Tidak ada tabel; tanggal hanya umum | Ada, tanggal per bulan |
| Omzet kumulatif per bulan | Tidak | Ya (berguna untuk bulan-bulan berikutnya) |
| Status aturan terbaru (PP 20/2026) | Tidak disebut; malah menyatakan pasti "maksimal 7 tahun", padahal referensi skill mencatat batas jangka waktu ini dilaporkan berubah/dihapus dan BELUM TERVERIFIKASI | Disebut sebagai belum terverifikasi + arahkan ke DJP |
| Batas Rp4,8 miliar | Tidak | Ya (sisa ruang) |
| Disclaimer & rujukan | Tidak ada | Ada |

## Penilaian
Angka inti sama, tetapi skill **jelas lebih baik**: tabel per bulan yang bisa dipakai terus sepanjang tahun, tanggal setor per bulan, dan — terpenting — tidak menyatakan sebagai kepastian klaim yang mungkin sudah berubah (batas 7 tahun). Jawaban tanpa skill terlihat meyakinkan tetapi berisiko menyesatkan.
