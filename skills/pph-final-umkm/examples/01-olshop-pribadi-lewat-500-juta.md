# 01 — Olshop orang pribadi, omzet melewati Rp500 juta di bulan Agustus

**Skenario:** S1 — permintaan normal. Penjual online perorangan memberi omzet Januari–Agustus.

**Input pengguna (persis):**
> Saya jualan baju online, atas nama pribadi (bukan PT). Omzet 2026: Jan 38jt, Feb 42jt, Mar 55jt, Apr 61jt, Mei 70jt, Jun 88jt, Jul 95jt, Agu 102jt. Pajaknya berapa per bulan?

**Perintah yang dijalankan agent:**
```bash
python3 <folder-skill>/scripts/pph_final.py --jenis op --tahun 2026 --omzet 38jt 42jt 55jt 61jt 70jt 88jt 95jt 102jt
```

## Output

## PPh Final UMKM 0,5% - Tahun 2026 (Orang pribadi)

| Bulan | Omzet | Omzet kumulatif | Omzet kena pajak | PPh final 0,5% | PPh 22 marketplace (info) | Setor paling lambat | Keterangan |
|---|---:|---:|---:|---:|---:|---|---|
| Januari | Rp 38.000.000 | Rp 38.000.000 | Rp 0 | Rp 0 | - | 2026-02-15 | masih dalam Rp500 juta bebas |
| Februari | Rp 42.000.000 | Rp 80.000.000 | Rp 0 | Rp 0 | - | 2026-03-15 | masih dalam Rp500 juta bebas |
| Maret | Rp 55.000.000 | Rp 135.000.000 | Rp 0 | Rp 0 | - | 2026-04-15 | masih dalam Rp500 juta bebas |
| April | Rp 61.000.000 | Rp 196.000.000 | Rp 0 | Rp 0 | - | 2026-05-15 | masih dalam Rp500 juta bebas |
| Mei | Rp 70.000.000 | Rp 266.000.000 | Rp 0 | Rp 0 | - | 2026-06-15 | masih dalam Rp500 juta bebas |
| Juni | Rp 88.000.000 | Rp 354.000.000 | Rp 0 | Rp 0 | - | 2026-07-15 | masih dalam Rp500 juta bebas |
| Juli | Rp 95.000.000 | Rp 449.000.000 | Rp 0 | Rp 0 | - | 2026-08-15 | masih dalam Rp500 juta bebas |
| Agustus | Rp 102.000.000 | Rp 551.000.000 | Rp 51.000.000 | Rp 255.000 | - | 2026-09-15 | melewati Rp500 juta; hanya Rp 51.000.000 yang kena pajak |
| **Total** | **Rp 551.000.000** | | | **Rp 255.000** | - | | |

**Ringkasan**
- Omzet kumulatif tahun 2026: Rp 551.000.000
- Total PPh final periode ini: Rp 255.000
- Batas Rp500 juta bebas pajak sudah terlewati (Agustus).
- Sisa ruang sebelum batas Rp4,8 miliar: Rp 4.249.000.000

**Catatan penting**
- Orang pribadi: omzet s.d. Rp500 juta setahun tidak dikenai PPh final. Batas ini untuk total omzet SEMUA usaha Anda dalam setahun.
- Tarif 0,5% dihitung dari OMZET (peredaran bruto), bukan dari laba.
- Pembulatan: PPh tiap bulan dibulatkan ke bawah ke rupiah penuh (pecahan rupiah dibuang).
- Batas setor tercantum = tanggal 15 bulan berikutnya (ketentuan umum PMK 81/2024); cek DJP bila jatuh di hari libur.
- PP 20/2026: ketentuan masa transisi untuk CV/firma/PT dan batas jangka waktu pemakaian tarif 0,5% belum kami verifikasi. Cek pajak.go.id atau Kring Pajak 1500200 sebelum mengambil keputusan.
- Tidak berlaku untuk penghasilan dari jasa pekerjaan bebas (mis. dokter, notaris, konsultan) dan penghasilan lain yang dikecualikan PP 55/2022.

_Dasar: PP 55/2022 jo. PP 20/2026 (PPh Final UMKM 0,5%); PMK 37/2025 (PPh 22 marketplace). Berlaku per 2026-09-23. Ini alat bantu hitung, bukan nasihat pajak. Untuk kepastian, hubungi DJP (Kring Pajak 1500200 / pajak.go.id) atau konsultan pajak._

**Penjelasan singkat:** Januari–Juli Anda belum bayar PPh final karena omzet kumulatif masih di bawah Rp500 juta. Di **Agustus** omzet kumulatif menjadi Rp551 juta, jadi **hanya Rp51 juta** (bagian di atas Rp500 juta) yang kena 0,5% → **Rp255.000**. Mulai September, seluruh omzet tiap bulan kena 0,5%.

⚠️ Batas setor PPh Agustus adalah **15 September 2026**, dan hari ini sudah 23 September. Jika belum disetor, segera setor dan tanyakan ke DJP/konsultan soal kemungkinan sanksi keterlambatan.

## Catatan penguji
- Angka dicek independen: 38+42+55+61+70+88+95 = 449 jt; +102 = 551 jt; kena 51 jt × 0,5% = Rp255.000. Benar, termasuk perlakuan proporsional bulan yang melewati batas.
- Catatan "belum terverifikasi" (PP 20/2026) tampil sebagai kehati-hatian, bukan kepastian — sesuai checklist.
- Kurang: script tidak menandai batas setor yang **sudah lewat** (Agustus → 15 Sep); peringatan di atas ditambahkan agent secara manual.
