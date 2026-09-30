# 07 — Uji independen: karyawan 2 pemberi kerja, TK/0 (normal)

**Input pengguna:** "2025 saya kerja di 2 tempat. A1 pertama neto 72 juta PPh 21 900rb, A1 kedua (Jul–Des) neto 48,5 juta PPh 21 nol. Belum nikah."

**Perintah:** `python3 scripts/spt_op.py --status TK/0 --tahun 2025 --a1 72jt 900rb --a1 48,5jt 0 --hari-ini 2026-09-30`

**Output script (apa adanya):**

## Hitungan SPT Tahunan PPh Orang Pribadi — Tahun Pajak 2025 (status TK/0)

**1. Penghasilan neto**

| Sumber | Neto |
|---|---|
| Bukti potong #1 (neto dari bukti potong) | Rp 72.000.000 |
| Bukti potong #2 (neto dari bukti potong) | Rp 48.500.000 |
| **Jumlah** | **Rp 120.500.000** |
| **Penghasilan neto** | **Rp 120.500.000** |

**2. PTKP & Penghasilan Kena Pajak (PKP)**

- Wajib pajak sendiri: Rp 54.000.000
- **PTKP TK/0: Rp 54.000.000**
- PKP = Rp 120.500.000 − Rp 54.000.000 = Rp 66.500.000 → dibulatkan ke bawah ribuan: **Rp 66.500.000**

**3. PPh terutang (tarif Pasal 17 UU HPP)**

- 5% × Rp 60.000.000 = Rp 3.000.000
- 15% × Rp 6.500.000 = Rp 975.000
- **PPh terutang: Rp 3.975.000**

**4. Kredit pajak (sudah dipotong/dibayar)**

- PPh 21 — Bukti potong #1: Rp 900.000
- **Total kredit: Rp 900.000**

**5. Hasil: KURANG BAYAR**
PPh terutang Rp 3.975.000 − kredit Rp 900.000 = **Rp 3.075.000 harus disetor (PPh Pasal 29) sebelum lapor**.

**Batas lapor:** 31 Maret 2026, diperpanjang khusus tahun pajak 2025 sampai 30 April 2026 (KEP-55/PJ/2026) — SUDAH LEWAT

**⚠️ Peringatan**
- Batas lapor (2026-04-30) SUDAH LEWAT per 2026-09-30. Tetap laporkan secepatnya; denda telat lapor SPT Tahunan OP Rp100.000 ditagih lewat STP; kurang bayar yang dibayar setelah batas juga kena bunga per bulan (tarif KMK bulanan — tidak dihitung di sini).

**Catatan**
- Punya 2 bukti potong pekerjaan: tiap pemberi kerja sudah memakai PTKP penuh, jadi saat digabung di SPT hampir selalu KURANG BAYAR. Ini normal, bukan kesalahan.
- Kurang bayar (PPh Pasal 29) wajib dilunasi SEBELUM SPT dikirim. Di Coretax, SPT kurang bayar masuk 'SPT menunggu pembayaran' dan kode billing dibuat otomatis.

**Checklist dokumen**
- [ ] Akun Coretax aktif (login NIK/NPWP 16 digit) + kode verifikasi/otorisasi untuk tanda tangan SPT
- [ ] Daftar HARTA per 31 Desember (tanah/bangunan, kendaraan, tabungan, deposito, emas, investasi) dengan tahun perolehan & nilai
- [ ] Daftar UTANG per 31 Desember (KPR, kredit kendaraan, pinjaman) — nama pemberi pinjaman & sisa pokok
- [ ] Data keluarga & tanggungan (NIK) sesuai keadaan 1 Januari
- [ ] Bukti potong PPh 21 dari SETIAP pemberi kerja (2 lembar; A1 swasta / A2 ASN) — cek sudah muncul otomatis di Coretax
- [ ] Saldo untuk melunasi PPh Pasal 29 (kode billing dari Coretax) sebelum SPT dikirim

_Alat bantu hitung, bukan konsultan pajak dan bukan nasihat pajak. Dasar: UU PPh s.t.d.t.d. UU 7/2021 (HPP) Pasal 7 & 17; PMK 101/PMK.010/2016 (PTKP); PMK 168/2023 (biaya jabatan, pembulatan PKP); PER-17/PJ/2015 & PMK 81/2024 (NPPN); PP 55/2022 jo. PP 20/2026 (PPh final UMKM); PP 60/2010 (zakat); PER-11/PJ/2025 (bentuk SPT Coretax); UU KUP Pasal 7; dicek per 30 September 2026. Pembulatan belum dicocokkan dengan hitungan otomatis Coretax. Skill ini tidak mengisi atau mengirim SPT atas nama Anda. Cocokkan dengan Coretax DJP, Kring Pajak 1500200, atau konsultan pajak terdaftar sebelum melapor._


**Hitungan independen penguji:** neto 72.000.000 + 48.500.000 = 120.500.000; PTKP TK/0 54.000.000; PKP 66.500.000; PPh = 3.000.000 + 15% × 6.500.000 (975.000) = 3.975.000; kredit 900.000 → **KURANG BAYAR 3.075.000** ✔. Cek kewajaran A1 #1: (72 jt − 54 jt) × 5% = 900.000 ✔ konsisten.

**Penilaian:** benar; catatan "2 bukti potong → hampir selalu kurang bayar" tepat dan membantu. Parser menerima `900rb` dan `48,5jt` dengan benar.
