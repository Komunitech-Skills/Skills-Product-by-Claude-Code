# 01 — Karyawan pindah kerja, dua bukti potong A1 (normal)

**Input pengguna (persis):**
> Tahun 2025 saya pindah kerja bulan Juli. Di A1 kantor lama penghasilan neto 90 juta, PPh 21 dipotong 1.350.000. Kantor baru neto 60 juta, PPh 21-nya nol. Saya menikah, anak satu. SPT saya nanti gimana?

**Pemetaan agent:** status K/1 (menikah + 1 anak per 1 Januari 2025), dua `--a1`, tahun 2025. Tanggal acuan = hari ini (2026-09-30).

**Perintah:**
```bash
python3 scripts/spt_op.py --status K/1 --tahun 2025 --a1 90jt 1.350.000 --a1 60jt 0 --hari-ini 2026-09-30
```

**Output script (apa adanya):**

## Hitungan SPT Tahunan PPh Orang Pribadi — Tahun Pajak 2025 (status K/1)

**1. Penghasilan neto**

| Sumber | Neto |
|---|---|
| Bukti potong #1 (neto dari bukti potong) | Rp 90.000.000 |
| Bukti potong #2 (neto dari bukti potong) | Rp 60.000.000 |
| **Jumlah** | **Rp 150.000.000** |
| **Penghasilan neto** | **Rp 150.000.000** |

**2. PTKP & Penghasilan Kena Pajak (PKP)**

- Wajib pajak sendiri: Rp 54.000.000
- Status kawin: Rp 4.500.000
- Tanggungan 1 orang × Rp 4.500.000: Rp 4.500.000
- **PTKP K/1: Rp 63.000.000**
- PKP = Rp 150.000.000 − Rp 63.000.000 = Rp 87.000.000 → dibulatkan ke bawah ribuan: **Rp 87.000.000**

**3. PPh terutang (tarif Pasal 17 UU HPP)**

- 5% × Rp 60.000.000 = Rp 3.000.000
- 15% × Rp 27.000.000 = Rp 4.050.000
- **PPh terutang: Rp 7.050.000**

**4. Kredit pajak (sudah dipotong/dibayar)**

- PPh 21 — Bukti potong #1: Rp 1.350.000
- **Total kredit: Rp 1.350.000**

**5. Hasil: KURANG BAYAR**
PPh terutang Rp 7.050.000 − kredit Rp 1.350.000 = **Rp 5.700.000 harus disetor (PPh Pasal 29) sebelum lapor**.

**Batas lapor:** 31 Maret 2026 (jatuh tempo formal tetap). Khusus tahun pajak 2025: sanksi administrasi (denda & bunga) dihapus bila lapor dan/atau bayar paling lambat 30 April 2026 (KEP-55/PJ/2026) — JATUH TEMPO SUDAH LEWAT

**⚠️ Peringatan**
- Batas lapor (2026-03-31) SUDAH LEWAT per 2026-09-30 (masa penghapusan sanksi KEP-55/PJ/2026 s.d. 2026-04-30 juga sudah berakhir). Tetap laporkan secepatnya; denda telat lapor SPT Tahunan OP Rp100.000 ditagih lewat STP; kurang bayar yang dibayar setelah jatuh tempo juga kena bunga per bulan (tarif KMK bulanan — tidak dihitung di sini).

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

**Penjelasan bahasa awam (ditulis agent):**
> Kurang bayar Rp5.700.000 ini wajar, bukan kesalahan kantor. Kantor lama dan kantor baru sama-sama menghitung pajak seolah-olah itu satu-satunya penghasilan Anda, jadi masing-masing memakai PTKP penuh (Rp63 juta) dan tarif 5%. Setelah digabung, penghasilan neto Anda Rp150 juta; PTKP hanya boleh dipakai sekali, dan Rp27 juta teratas masuk tarif 15%. Selisih itulah yang harus Anda setor sendiri.

**Peta ke Coretax:** kedua bukti potong → Lampiran 1 (cek sudah muncul otomatis) · neto, PTKP, PKP, PPh terutang → Induk Bagian B–C · kredit Rp1.350.000 & kurang bayar → Bagian D–E.

**Langkah berikutnya:** (1) buat konsep SPT di Coretax, pastikan kedua bukti potong masuk; (2) karena kurang bayar, bayar Rp5.700.000 lewat kode billing yang dibuat Coretax; (3) kirim SPT setelah pembayaran tervalidasi. Jatuh tempo TP 2025 (31 Maret 2026) dan masa penghapusan sanksi KEP-55/PJ/2026 (s.d. 30 April 2026) sudah lewat → lapor secepatnya; denda Rp100.000 dan bunga akan ditagih lewat STP.

**Verifikasi manual:** 150.000.000 − 63.000.000 = 87.000.000 → 5% × 60.000.000 = 3.000.000; 15% × 27.000.000 = 4.050.000; total 7.050.000 − 1.350.000 = **5.700.000** ✔ (sama dengan tes regresi kasus 02).

> **Catatan v1.0.1 (2026-09-30):** teks batas lapor & peringatan di atas diperbarui ke output script v1.0.1 (jatuh tempo formal TP 2025 tetap 31 Maret 2026; KEP-55/PJ/2026 hanya menghapus sanksi s.d. 30 April 2026). Angka tidak berubah.
