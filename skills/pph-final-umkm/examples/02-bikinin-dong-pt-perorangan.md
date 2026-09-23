# 02 — "bikinin dong", PT perorangan dengan omzet semester 1 digabung

**Skenario:** S2 — permintaan singkat. Badan (PT perorangan), data mulai Juli dengan omzet Januari–Juni sebagai angka gabungan.

**Input pengguna (persis):**
> bikinin dong itungan pph final PT perorangan aku. jan-jun totalnya 900jt, juli 150jt, agustus 180jt

**Perintah yang dijalankan agent:**
```bash
python3 <folder-skill>/scripts/pph_final.py --jenis badan --jenis-badan pt-perorangan --tahun 2026 --bulan-awal 7 --omzet-sebelumnya 900jt --omzet 150jt 180jt
```

## Output

## PPh Final UMKM 0,5% - Tahun 2026 (Badan (PT perorangan))

Omzet sebelum periode ini: Rp 900.000.000

| Bulan | Omzet | Omzet kumulatif | Omzet kena pajak | PPh final 0,5% | PPh 22 marketplace (info) | Setor paling lambat | Keterangan |
|---|---:|---:|---:|---:|---:|---|---|
| Juli | Rp 150.000.000 | Rp 1.050.000.000 | Rp 150.000.000 | Rp 750.000 | - | 2026-08-15 | - |
| Agustus | Rp 180.000.000 | Rp 1.230.000.000 | Rp 180.000.000 | Rp 900.000 | - | 2026-09-15 | - |
| **Total** | **Rp 330.000.000** | | | **Rp 1.650.000** | - | | |

**Ringkasan**
- Omzet kumulatif tahun 2026: Rp 1.230.000.000
- Total PPh final periode ini: Rp 1.650.000
- Sisa ruang sebelum batas Rp4,8 miliar: Rp 3.570.000.000

**Catatan penting**
- Badan: 0,5% x seluruh omzet, tanpa pembebasan Rp500 juta.
- Tarif 0,5% dihitung dari OMZET (peredaran bruto), bukan dari laba.
- Pembulatan: PPh tiap bulan dibulatkan ke bawah ke rupiah penuh (pecahan rupiah dibuang).
- Batas setor tercantum = tanggal 15 bulan berikutnya (ketentuan umum PMK 81/2024); cek DJP bila jatuh di hari libur.
- PP 20/2026: ketentuan masa transisi untuk CV/firma/PT dan batas jangka waktu pemakaian tarif 0,5% belum kami verifikasi. Cek pajak.go.id atau Kring Pajak 1500200 sebelum mengambil keputusan.
- Tidak berlaku untuk penghasilan dari jasa pekerjaan bebas (mis. dokter, notaris, konsultan) dan penghasilan lain yang dikecualikan PP 55/2022.

_Dasar: PP 55/2022 jo. PP 20/2026 (PPh Final UMKM 0,5%); PMK 37/2025 (PPh 22 marketplace). Berlaku per 2026-09-23. Ini alat bantu hitung, bukan nasihat pajak. Untuk kepastian, hubungi DJP (Kring Pajak 1500200 / pajak.go.id) atau konsultan pajak._

**Penjelasan singkat:** Karena usaha Anda berbentuk **PT perorangan (badan)**, tidak ada pembebasan Rp500 juta — seluruh omzet tiap bulan kena 0,5%. Juli: Rp750.000, Agustus: Rp900.000.

Catatan tambahan:
- Untuk Januari–Juni (omzet Rp900 juta) PPh finalnya seharusnya sudah disetor tiap bulan, totalnya 0,5% × Rp900.000.000 = **Rp4.500.000**. Kalau belum, beri tahu saya omzet per bulannya agar saya buatkan tabel lengkap.
- Batas setor Agustus (15 September 2026) sudah lewat hari ini (23 September). Jika belum disetor, segera setor dan konsultasikan kemungkinan sanksinya.

## Catatan penguji
- Parameter `--bulan-awal` dan `--omzet-sebelumnya` dipakai dengan benar; perlakuan badan tanpa pembebasan Rp500 juta benar (150 jt × 0,5% = 750.000; 180 jt × 0,5% = 900.000).
- Kurang: script tidak memberi catatan bahwa PPh atas `omzet-sebelumnya` untuk badan juga terutang (Rp4,5 jt); agent harus menambahkannya sendiri. Juga tidak ada penanda batas setor yang sudah lewat.
