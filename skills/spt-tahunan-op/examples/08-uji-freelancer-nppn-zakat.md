# 08 — Uji independen: freelancer NPPN + zakat + PPh 25 (normal)

**Input pengguna:** "Saya konsultan IT freelance di Jakarta, menikah belum punya anak. Fee 2025 total 450 juta, norma 50% (sudah cek tabel), sudah kirim pemberitahuan norma Februari. Zakat ke BAZNAS Rp5.625.500. Klien memotong PPh 21 total 9 juta, saya bayar angsuran PPh 25 total 6 juta."

**Perintah:** `python3 scripts/spt_op.py --status K/0 --tahun 2025 --nppn 450jt 50 --nppn-diberitahukan ya --zakat 5.625.500 --pph21-lain 9jt --pph25 6jt --hari-ini 2026-09-30`

**Output script (apa adanya):**

## Hitungan SPT Tahunan PPh Orang Pribadi — Tahun Pajak 2025 (status K/0)

**1. Penghasilan neto**

| Sumber | Neto |
|---|---|
| Usaha/pekerjaan bebas #1 — NPPN 50% × Rp 450.000.000 | Rp 225.000.000 |
| **Jumlah** | **Rp 225.000.000** |
| Dikurangi zakat (BAZNAS/LAZ resmi) | −Rp 5.625.500 |
| **Penghasilan neto** | **Rp 219.374.500** |

**2. PTKP & Penghasilan Kena Pajak (PKP)**

- Wajib pajak sendiri: Rp 54.000.000
- Status kawin: Rp 4.500.000
- **PTKP K/0: Rp 58.500.000**
- PKP = Rp 219.374.500 − Rp 58.500.000 = Rp 160.874.500 → dibulatkan ke bawah ribuan: **Rp 160.874.000**

**3. PPh terutang (tarif Pasal 17 UU HPP)**

- 5% × Rp 60.000.000 = Rp 3.000.000
- 15% × Rp 100.874.000 = Rp 15.131.100
- **PPh terutang: Rp 18.131.100**

**4. Kredit pajak (sudah dipotong/dibayar)**

- PPh 21 bukan pegawai / lainnya (bukti potong): Rp 9.000.000
- Angsuran PPh 25 yang sudah dibayar: Rp 6.000.000
- **Total kredit: Rp 15.000.000**

**5. Hasil: KURANG BAYAR**
PPh terutang Rp 18.131.100 − kredit Rp 15.000.000 = **Rp 3.131.100 harus disetor (PPh Pasal 29) sebelum lapor**.
Perkiraan angsuran PPh 25 tahun 2026: **Rp 760.925 per bulan**.

**Batas lapor:** 31 Maret 2026, diperpanjang khusus tahun pajak 2025 sampai 30 April 2026 (KEP-55/PJ/2026) — SUDAH LEWAT

**⚠️ Peringatan**
- Batas lapor (2026-04-30) SUDAH LEWAT per 2026-09-30. Tetap laporkan secepatnya; denda telat lapor SPT Tahunan OP Rp100.000 ditagih lewat STP; kurang bayar yang dibayar setelah batas juga kena bunga per bulan (tarif KMK bulanan — tidak dihitung di sini).

**Catatan**
- Persen norma NPPN wajib dicocokkan dengan lampiran PER-17/PJ/2015 sesuai KLU dan wilayah (10 ibu kota provinsi / ibu kota provinsi lain / daerah lain).
- Zakat hanya boleh dikurangkan bila dibayar ke BAZNAS/LAZ/lembaga yang disahkan pemerintah dan ada bukti setor. Zakat yang sudah dipotong lewat kantor (tercantum di bukti potong A1) JANGAN dimasukkan lagi di --zakat.
- Perkiraan angsuran PPh 25 tahun 2026 = (PPh terutang − PPh 21/22/23 yang dipotong) ÷ 12 (UU PPh Pasal 25 ayat (1)). Cocokkan dengan Lampiran 4 di Coretax.
- Kurang bayar (PPh Pasal 29) wajib dilunasi SEBELUM SPT dikirim. Di Coretax, SPT kurang bayar masuk 'SPT menunggu pembayaran' dan kode billing dibuat otomatis.

**Checklist dokumen**
- [ ] Akun Coretax aktif (login NIK/NPWP 16 digit) + kode verifikasi/otorisasi untuk tanda tangan SPT
- [ ] Daftar HARTA per 31 Desember (tanah/bangunan, kendaraan, tabungan, deposito, emas, investasi) dengan tahun perolehan & nilai
- [ ] Daftar UTANG per 31 Desember (KPR, kredit kendaraan, pinjaman) — nama pemberi pinjaman & sisa pokok
- [ ] Data keluarga & tanggungan (NIK) sesuai keadaan 1 Januari
- [ ] Bukti potong PPh 21 bukan pegawai (honor/fee) dari tiap pemberi penghasilan
- [ ] Bukti setor (NTPN) angsuran PPh 25 bulanan
- [ ] Rekap peredaran bruto per bulan (pencatatan) + bukti pemberitahuan penggunaan NPPN ke DJP
- [ ] Bukti setor zakat dari BAZNAS/LAZ resmi (nama, NIK/NPWP, jumlah, tanggal, nama lembaga)
- [ ] Saldo untuk melunasi PPh Pasal 29 (kode billing dari Coretax) sebelum SPT dikirim

_Alat bantu hitung, bukan konsultan pajak dan bukan nasihat pajak. Dasar: UU PPh s.t.d.t.d. UU 7/2021 (HPP) Pasal 7 & 17; PMK 101/PMK.010/2016 (PTKP); PMK 168/2023 (biaya jabatan, pembulatan PKP); PER-17/PJ/2015 & PMK 81/2024 (NPPN); PP 55/2022 jo. PP 20/2026 (PPh final UMKM); PP 60/2010 (zakat); PER-11/PJ/2025 (bentuk SPT Coretax); UU KUP Pasal 7; dicek per 30 September 2026. Pembulatan belum dicocokkan dengan hitungan otomatis Coretax. Skill ini tidak mengisi atau mengirim SPT atas nama Anda. Cocokkan dengan Coretax DJP, Kring Pajak 1500200, atau konsultan pajak terdaftar sebelum melapor._


**Hitungan independen penguji:** neto NPPN 450.000.000 × 50% = 225.000.000; − zakat 5.625.500 = 219.374.500; − PTKP K/0 58.500.000 = 160.874.500 → dibulatkan ke bawah ribuan **160.874.000** (menguji pembulatan PKP, PMK 168/2023 Ps. 8 ayat (4)); PPh = 3.000.000 + 15% × 100.874.000 (15.131.100) = 18.131.100; kredit 9.000.000 + 6.000.000 = 15.000.000 → **KURANG BAYAR 3.131.100** ✔. PPh 25 tahun 2026 = (18.131.100 − 9.000.000) ÷ 12 = 760.925 ✔.

**Penilaian:** benar termasuk pembulatan & PPh 25. Zakat diperlakukan sebagai pengurang penghasilan (UU PPh Ps. 9 ayat (1) huruf g, PP 60/2010) ✔. Catatan: skill tidak menyinggung bahwa jasa pekerjaan bebas tidak bisa memakai PPh final 0,5% (PP 55/2022 s.t.d.d. PP 20/2026) — relevan bila pengguna freelancer bertanya "pakai 0,5% saja?" (rendah).
