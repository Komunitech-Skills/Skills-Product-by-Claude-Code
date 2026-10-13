# Uji 02 — Jasa servis AC, invoice bulanan DPP + PPN (normal)

- **Penguji:** agent independen Akun B. Acuan 26 Sep 2026 (WIB). Data rekaan.
- **Permintaan:** "CV Sejuk Teknik, kontrak servis AC bulanan. Catat invoice Juni–Agustus PT Graha Niaga DPP 4,55 juta + PPN, Klinik Pratama Sehat DPP 1.234.567 tempo 14 hari, Hotel Melati DPP 7.777.777 PPN 12% (barang mewah — sengaja diuji) tempo 45 hari, servis rumah Bu Dewi 350 ribu. Graha transfer 5.050.500 tgl 5/9, Hotel bayar 8,7 juta. Graha bayar invoice Juli dipotong PPh 23."

## Perintah & output penting
```
catat --pelanggan "PT Graha Niaga" --nota "INV/2026/06/001" --tanggal 30/06/2026 --dpp 4.550.000 --ppn 11
→ Rp 5.050.500 | jatuh tempo Kamis, 30 Juli 2026 (30 hari)
  Catatan: DPP Rp 4.550.000 + PPN 12% x DPP nilai lain 11/12 = Rp 500.500 (efektif 11%, dibulatkan ke bawah) ...
  Pembulatan ini belum dicocokkan dengan Coretax ...
  Catatan: Nota ini sudah lewat jatuh tempo 58 hari; langsung masuk daftar terlewat.
catat ... --dpp 1.234.567 --ppn 11 --jatuh-tempo "14 hari"   → Rp 1.370.369, JT 12 Sep 2026
catat ... --dpp 7.777.777 --ppn 12 --termin 45                → Rp 8.711.110, JT 29 Agu 2026
catat --pelanggan "Bu Dewi (rumah)" --tanggal "21 Sep 26" --nominal "350rb" → Catatan: tahun 2 angka dibaca 2026
catat ... --nota "inv 2026 06 001" → GAGAL: Nota INV/2026/06/001 sudah tercatat ... Tidak dicatat dobel.
bayar --pelanggan "Graha" --jumlah "5.050.500" --tanggal 05/09/2026 → INV/2026/06/001 LUNAS (alokasi JT paling awal)
bayar --pelanggan "Hotel Melati" --jumlah "8,7 jt" → sisa Rp 11.110
bayar --nota INV/2026/07/001 --jumlah 4.959.500 → sisa Rp 91.000
potong --nota INV/2026/07/001 --jumlah 91rb --alasan "PPh 23 2% x DPP, bukti potong diterima" → pratinjau → --ya → LUNAS
```
`umur --per 31/08/2026`: total Rp 25.232.979; belum JT 6.420.869 (25,4%) | 1–30 13.761.610 (54,5%) | 31–60 5.050.500 (20,0%).
`umur` hari ini: total Rp 6.781.979; belum JT 5.400.500 (79,6%) | 1–30 1.381.479 (20,4%).
`rekap --periode bulan-ini`: nota baru 1 (Rp 350.000), pembayaran 3 kali Rp 18.710.000, potongan Rp 91.000.

## Verifikasi independen (Decimal)
| Pos | Hitung manual | Script |
|---|---|---|
| PPN 11 atas 4.550.000 = floor(4.550.000 × 12% × 11/12) | 500.500 → total 5.050.500 | ✅ |
| PPN 11 atas 1.234.567 = floor(135.802,37) | 135.802 → 1.370.369 | ✅ |
| PPN 12 atas 7.777.777 = floor(933.333,24) | 933.333 → 8.711.110 | ✅ |
| JT: 30/06+30, 31/07+30, 31/08+30, 29/08+14, 15/07+45 | 30/07, 30/08, 30/09, 12/09, 29/08 | ✅ |
| Hari lewat per 26/09 | 58, 27, 14, 28 | ✅ |
| Posisi per 31/08 (nota ≤ 31/08, bayar belum ada): Graha Jun lewat 32 → 31–60; Graha Jul lewat 1 → 1–30; Hotel lewat 2 → 1–30; Graha Agu & Klinik belum JT | 6.420.869 / 13.761.610 / 5.050.500; total 25.232.979; persen 25,4 / 54,5 / 20,0 | ✅ |
| Posisi hari ini: 5.050.500 + 1.370.369 + 350.000 + 11.110 | 6.781.979 | ✅ |
| Pembayaran September: 5.050.500 + 8.700.000 + 4.959.500 | 18.710.000 | ✅ |
| PPh 23 2% × DPP 4.550.000 | 91.000 | ✅ (sisa 0) |

Ekspor `--format tagih-piutang` → `hitung_telat.py --file` (skill tagih-piutang, salinan) membaca 4 nota terbuka, total Rp 6.781.979 dan bucket sama (Hotel Melati: nominal 8.711.110, dibayar 8.700.000).

## Catatan temuan
- **PPh 23 (P3):** bila pelanggan Anda pemotong PPh 23 (badan usaha), tarif 2% untuk jasa sesuai UU PPh Pasal 23 ayat (1) huruf c; pastikan ke pelanggan. Skill tidak membahasnya; pengguna awam akan melihat "kurang bayar Rp 91.000" dan bisa menagih ulang pelanggan. `potong` berfungsi, tetapi rekap melabelinya "Potongan (retur/diskon/hapus)". Saran: satu baris panduan di Langkah C ("dipotong PPh 23 → `potong --alasan "PPh 23, bukti potong No ..."`, jangan ditagih") dan label terpisah di rekap.
- Pratinjau `potong` dan pesan dobel nota jelas. Catatan Coretax selalu muncul (sesuai standar CLAUDE.md).

**Nilai skenario: lulus.**
