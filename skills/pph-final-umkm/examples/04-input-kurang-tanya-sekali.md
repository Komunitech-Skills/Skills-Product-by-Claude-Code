# 04 — Input kurang: hanya omzet satu bulan

**Skenario:** S4 — input tidak lengkap. Jenis wajib pajak dan omzet bulan-bulan sebelumnya tidak disebut, padahal menentukan apakah batas Rp500 juta sudah terlewati.

**Input pengguna (persis):**
> Omzet saya bulan September 75 juta, pajaknya berapa?

## Output (balasan pertama — bertanya sekali)

Bisa saya hitungkan. Supaya hasilnya benar, saya perlu 3 hal:

1. Usaha Anda atas nama **pribadi** atau **badan** (PT perorangan, koperasi, CV, dll.)?
2. Berapa **total omzet Januari–Agustus 2026**? (Untuk orang pribadi, Rp500 juta pertama setahun bebas pajak, jadi omzet bulan-bulan sebelumnya menentukan.)
3. Apakah ada PPh 22 yang sudah dipotong marketplace di bulan September? (Kalau tidak ada, lewati saja.)

Kalau Anda ingin cepat, saya bisa anggap orang pribadi dengan omzet Januari–Agustus Rp0 — tetapi hasilnya bisa **keliru** kalau sebenarnya sudah ada omzet sebelumnya.

**Balasan pengguna:**
> pribadi, jan-agu totalnya kira2 470 juta. ga jualan di marketplace

**Perintah:**
```bash
python3 <folder-skill>/scripts/pph_final.py --jenis op --tahun 2026 --bulan-awal 9 --omzet-sebelumnya 470jt --omzet 75jt
```

## Output (balasan kedua)

## PPh Final UMKM 0,5% - Tahun 2026 (Orang pribadi)

Omzet sebelum periode ini: Rp 470.000.000

| Bulan | Omzet | Omzet kumulatif | Omzet kena pajak | PPh final 0,5% | PPh 22 marketplace (info) | Setor paling lambat | Keterangan |
|---|---:|---:|---:|---:|---:|---|---|
| September | Rp 75.000.000 | Rp 545.000.000 | Rp 45.000.000 | Rp 225.000 | - | 2026-10-15 | melewati Rp500 juta; hanya Rp 45.000.000 yang kena pajak |
| **Total** | **Rp 75.000.000** | | | **Rp 225.000** | - | | |

**Ringkasan**
- Omzet kumulatif tahun 2026: Rp 545.000.000
- Total PPh final periode ini: Rp 225.000
- Batas Rp500 juta bebas pajak sudah terlewati (September).
- Sisa ruang sebelum batas Rp4,8 miliar: Rp 4.255.000.000

**Catatan penting**
- Orang pribadi: omzet s.d. Rp500 juta setahun tidak dikenai PPh final. Batas ini untuk total omzet SEMUA usaha Anda dalam setahun.
- Tarif 0,5% dihitung dari OMZET (peredaran bruto), bukan dari laba.
- Pembulatan: PPh tiap bulan dibulatkan ke bawah ke rupiah penuh (pecahan rupiah dibuang).
- Batas setor tercantum = tanggal 15 bulan berikutnya (ketentuan umum PMK 81/2024); cek DJP bila jatuh di hari libur.
- PP 20/2026: ketentuan masa transisi untuk CV/firma/PT dan batas jangka waktu pemakaian tarif 0,5% belum kami verifikasi. Cek pajak.go.id atau Kring Pajak 1500200 sebelum mengambil keputusan.
- Tidak berlaku untuk penghasilan dari jasa pekerjaan bebas (mis. dokter, notaris, konsultan) dan penghasilan lain yang dikecualikan PP 55/2022.

_Dasar: PP 55/2022 jo. PP 20/2026 (PPh Final UMKM 0,5%); PMK 37/2025 (PPh 22 marketplace). Berlaku per 2026-09-23. Ini alat bantu hitung, bukan nasihat pajak. Untuk kepastian, hubungi DJP (Kring Pajak 1500200 / pajak.go.id) atau konsultan pajak._

**Penjelasan singkat:** Dengan omzet Januari–Agustus Rp470 juta, September adalah bulan Anda melewati Rp500 juta. Yang kena pajak hanya **Rp45 juta** (Rp545 juta − Rp500 juta), jadi PPh final September **Rp225.000**, setor paling lambat 15 Oktober 2026. Mulai Oktober, seluruh omzet bulanan kena 0,5%.

Karena angka Januari–Agustus masih "kira-kira", hasil ini ikut perkiraan. Kalau nanti angka pastinya berbeda, kabari saya untuk dihitung ulang.

## Catatan penguji
- Bertanya sekali, 3 pertanyaan bernomor, menjelaskan kenapa omzet sebelumnya penting, dan menawarkan default dengan risikonya. Sesuai SKILL.md.
- Angka dicek independen: 470 + 75 = 545 jt → kena 45 jt × 0,5% = Rp225.000.
