# 03 — Karyawan + toko online PPh final + zakat, perkiraan tahun berjalan (normal)

**Input pengguna (persis):**
> Aku karyawan K/2, perkiraan A1 2026 neto 132 juta, PPh 21 setahun 3.225.000. Istri? nggak kerja. Aku juga jualan online di Shopee atas nama sendiri, omzet setahun kira2 380 juta. Tiap bulan zakat penghasilan ke BAZNAS 275 ribu (bayar sendiri, bukan lewat kantor). Kira-kira SPT 2026 nanti gimana?

**Pemetaan agent:** status K/2, tahun 2026 (belum berakhir → perkiraan), satu `--a1`, omzet final 380 jt (≤ Rp500 jt → PPh final 0), zakat 12 × 275.000 = 3.300.000.

**Perintah:**
```bash
python3 scripts/spt_op.py --status K/2 --tahun 2026 --a1 132jt 3.225.000 --omzet-final 380jt --zakat 3,3jt --hari-ini 2026-09-30
```

**Output script (apa adanya):**

## Hitungan SPT Tahunan PPh Orang Pribadi — Tahun Pajak 2026 (status K/2)

**1. Penghasilan neto**

| Sumber | Neto |
|---|---|
| Bukti potong #1 (neto dari bukti potong) | Rp 132.000.000 |
| **Jumlah** | **Rp 132.000.000** |
| Dikurangi zakat (BAZNAS/LAZ resmi) | −Rp 3.300.000 |
| **Penghasilan neto** | **Rp 128.700.000** |

**2. PTKP & Penghasilan Kena Pajak (PKP)**

- Wajib pajak sendiri: Rp 54.000.000
- Status kawin: Rp 4.500.000
- Tanggungan 2 orang × Rp 4.500.000: Rp 9.000.000
- **PTKP K/2: Rp 67.500.000**
- PKP = Rp 128.700.000 − Rp 67.500.000 = Rp 61.200.000 → dibulatkan ke bawah ribuan: **Rp 61.200.000**

**3. PPh terutang (tarif Pasal 17 UU HPP)**

- 5% × Rp 60.000.000 = Rp 3.000.000
- 15% × Rp 1.200.000 = Rp 180.000
- **PPh terutang: Rp 3.180.000**

**4. Kredit pajak (sudah dipotong/dibayar)**

- PPh 21 — Bukti potong #1: Rp 3.225.000
- **Total kredit: Rp 3.225.000**

**5. Hasil: LEBIH BAYAR**
Kredit Rp 3.225.000 − PPh terutang Rp 3.180.000 = **Rp 45.000 lebih bayar**.
Info: omzet PPh final 0,5% Rp 380.000.000 (PPh final disetor Rp 0) dilaporkan terpisah, tidak mengubah angka di atas.

**Batas lapor:** 31 Maret 2027 (tidak bergeser walau hari libur — lapor lebih awal)

**⚠️ Peringatan**
- Tahun pajak 2026 belum berakhir per 2026-09-30: hasil ini PERKIRAAN. Hitung ulang setelah semua bukti potong tahun 2026 diterima (biasanya Januari–Februari 2027).

**Catatan**
- Zakat hanya boleh dikurangkan bila dibayar ke BAZNAS/LAZ/lembaga yang disahkan pemerintah dan ada bukti setor. Zakat yang sudah dipotong lewat kantor (tercantum di bukti potong A1) JANGAN dimasukkan lagi di --zakat.
- Omzet PPh final 0,5% (Rp 380.000.000) TIDAK ikut dihitung tarif Pasal 17; dilaporkan di lampiran penghasilan final / rekap peredaran bruto beserta PPh final yang sudah disetor (Rp 0).
- Omzet final setahun tidak lebih dari Rp500 juta: untuk orang pribadi bagian ini bebas PPh final 0,5% (PP 55/2022 s.t.d.d. UU HPP), tetapi omzetnya tetap dilaporkan di SPT.
- Lebih bayar Rp 45.000: pilih 'dikembalikan' (restitusi; untuk kondisi Anda umumnya lewat pengembalian pendahuluan, Pasal 17D UU KUP) atau 'dikompensasikan' ke tahun depan. Siapkan semua bukti potong asli.

**Checklist dokumen**
- [ ] Akun Coretax aktif (login NIK/NPWP 16 digit) + kode verifikasi/otorisasi untuk tanda tangan SPT
- [ ] Daftar HARTA per 31 Desember (tanah/bangunan, kendaraan, tabungan, deposito, emas, investasi) dengan tahun perolehan & nilai
- [ ] Daftar UTANG per 31 Desember (KPR, kredit kendaraan, pinjaman) — nama pemberi pinjaman & sisa pokok
- [ ] Data keluarga & tanggungan (NIK) sesuai keadaan 1 Januari
- [ ] Bukti potong PPh 21 dari SETIAP pemberi kerja (1 lembar; A1 swasta / A2 ASN) — cek sudah muncul otomatis di Coretax
- [ ] Rekap omzet PP 55 per bulan + bukti setor (NTPN) PPh final 0,5% / dokumen tagihan marketplace
- [ ] Bukti setor zakat dari BAZNAS/LAZ resmi (nama, NIK/NPWP, jumlah, tanggal, nama lembaga)
- [ ] Nomor rekening bank atas nama sendiri bila memilih restitusi

_Alat bantu hitung, bukan konsultan pajak dan bukan nasihat pajak. Dasar: UU PPh s.t.d.t.d. UU 7/2021 (HPP) Pasal 7 & 17; PMK 101/PMK.010/2016 (PTKP); PMK 168/2023 (biaya jabatan, pembulatan PKP); PER-17/PJ/2015 & PMK 81/2024 (NPPN); PP 55/2022 jo. PP 20/2026 (PPh final UMKM); PP 60/2010 (zakat); PER-11/PJ/2025 (bentuk SPT Coretax); UU KUP Pasal 7; dicek per 30 September 2026. Pembulatan belum dicocokkan dengan hitungan otomatis Coretax. Skill ini tidak mengisi atau mengirim SPT atas nama Anda. Cocokkan dengan Coretax DJP, Kring Pajak 1500200, atau konsultan pajak terdaftar sebelum melapor._

**Penjelasan bahasa awam (ditulis agent):**
> Omzet Shopee Rp380 juta tidak dihitung dengan tarif gaji, karena masuk PPh final 0,5% — dan karena belum lewat Rp500 juta setahun, untuk orang pribadi bagian itu bebas pajak (tetap dilaporkan). Zakat ke BAZNAS Rp3,3 juta mengurangi penghasilan neto, sehingga PPh setahun Rp3.180.000, sedikit lebih kecil dari yang dipotong kantor. Perkiraan: **lebih bayar Rp45.000**. Angka final baru pasti setelah A1 2026 terbit di awal 2027.

**Peta ke Coretax:** A1 → Lampiran 1 · omzet Shopee → Lampiran 2 (penghasilan final) & L-3B · zakat → pengurang penghasilan (Lampiran 5/Bagian B) · LB → Bagian E & G.

**Langkah berikutnya:** simpan bukti setor zakat BAZNAS (nama, NIK/NPWP, tanggal, jumlah) dan rekap omzet bulanan; lapor paling lambat 31 Maret 2027. Untuk lebih bayar sekecil ini, banyak orang memilih kompensasi agar proses cepat.

**Verifikasi manual:** 132.000.000 − 3.300.000 = 128.700.000; − 67.500.000 = 61.200.000; 3.000.000 + 15% × 1.200.000 (180.000) = 3.180.000; 3.225.000 − 3.180.000 = **45.000 LB** ✔.
