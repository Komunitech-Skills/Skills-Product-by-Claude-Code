# 06 — Uji independen: karyawan 1 pemberi kerja, K/2 (normal)

Penguji independen, 2026-09-30. Agent headless (Claude Sonnet, `claude -p`) membaca SKILL.md dan menjalankan script; output agent lengkap ada di `00-pembanding-tanpa-skill.md`.

**Input pengguna:** "Saya karyawan di satu perusahaan, status menikah anak 2 (K/2). Di bukti potong A1 tahun 2025: penghasilan neto Rp180.000.000, PPh 21 yang dipotong Rp10.500.000. Hitung SPT tahunan saya: kurang bayar atau lebih bayar berapa, dan apa yang harus saya siapkan?"

**Perintah:** `python3 scripts/spt_op.py --status K/2 --tahun 2025 --a1 180jt 10.500.000 --hari-ini 2026-09-30`

**Output script (apa adanya):**

## Hitungan SPT Tahunan PPh Orang Pribadi — Tahun Pajak 2025 (status K/2)

**1. Penghasilan neto**

| Sumber | Neto |
|---|---|
| Bukti potong #1 (neto dari bukti potong) | Rp 180.000.000 |
| **Jumlah** | **Rp 180.000.000** |
| **Penghasilan neto** | **Rp 180.000.000** |

**2. PTKP & Penghasilan Kena Pajak (PKP)**

- Wajib pajak sendiri: Rp 54.000.000
- Status kawin: Rp 4.500.000
- Tanggungan 2 orang × Rp 4.500.000: Rp 9.000.000
- **PTKP K/2: Rp 67.500.000**
- PKP = Rp 180.000.000 − Rp 67.500.000 = Rp 112.500.000 → dibulatkan ke bawah ribuan: **Rp 112.500.000**

**3. PPh terutang (tarif Pasal 17 UU HPP)**

- 5% × Rp 60.000.000 = Rp 3.000.000
- 15% × Rp 52.500.000 = Rp 7.875.000
- **PPh terutang: Rp 10.875.000**

**4. Kredit pajak (sudah dipotong/dibayar)**

- PPh 21 — Bukti potong #1: Rp 10.500.000
- **Total kredit: Rp 10.500.000**

**5. Hasil: KURANG BAYAR**
PPh terutang Rp 10.875.000 − kredit Rp 10.500.000 = **Rp 375.000 harus disetor (PPh Pasal 29) sebelum lapor**.

**Batas lapor:** 31 Maret 2026 (jatuh tempo formal tetap). Khusus tahun pajak 2025: sanksi administrasi (denda & bunga) dihapus bila lapor dan/atau bayar paling lambat 30 April 2026 (KEP-55/PJ/2026) — JATUH TEMPO SUDAH LEWAT

**⚠️ Peringatan**
- Anda hanya punya 1 pemberi kerja, tetapi hasilnya KURANG BAYAR Rp 375.000. Biasanya kantor sudah menghitung ulang pajak setahun di gaji bulan terakhir (Desember atau bulan keluar), sehingga hasil SPT karyawan 1 kantor umumnya NIHIL. Sebelum lapor/bayar, CEK ULANG bukti potong A1 dengan HRD/bagian gaji: (1) status PTKP di A1 sama dengan status Anda per 1 Januari (mis. sudah menikah/punya anak tapi belum diperbarui di kantor); (2) angka 'penghasilan neto' dan 'PPh 21 dipotong' yang Anda masukkan sama persis dengan A1; (3) tidak ada A1 lain (mis. kantor lama/pembetulan). Bila A1 memang begitu, hasil ini yang dipakai; selisih kecil (beberapa rupiah) bisa karena pembulatan.
- Batas lapor (2026-03-31) SUDAH LEWAT per 2026-09-30 (masa penghapusan sanksi KEP-55/PJ/2026 s.d. 2026-04-30 juga sudah berakhir). Tetap laporkan secepatnya; denda telat lapor SPT Tahunan OP Rp100.000 ditagih lewat STP; kurang bayar yang dibayar setelah jatuh tempo juga kena bunga per bulan (tarif KMK bulanan — tidak dihitung di sini).

**Catatan**
- Kurang bayar (PPh Pasal 29) wajib dilunasi SEBELUM SPT dikirim. Di Coretax, SPT kurang bayar masuk 'SPT menunggu pembayaran' dan kode billing dibuat otomatis.

**Checklist dokumen**
- [ ] Akun Coretax aktif (login NIK/NPWP 16 digit) + kode verifikasi/otorisasi untuk tanda tangan SPT
- [ ] Daftar HARTA per 31 Desember (tanah/bangunan, kendaraan, tabungan, deposito, emas, investasi) dengan tahun perolehan & nilai
- [ ] Daftar UTANG per 31 Desember (KPR, kredit kendaraan, pinjaman) — nama pemberi pinjaman & sisa pokok
- [ ] Data keluarga & tanggungan (NIK) sesuai keadaan 1 Januari
- [ ] Bukti potong PPh 21 dari SETIAP pemberi kerja (1 lembar; A1 swasta / A2 ASN) — cek sudah muncul otomatis di Coretax
- [ ] Saldo untuk melunasi PPh Pasal 29 (kode billing dari Coretax) sebelum SPT dikirim

_Alat bantu hitung, bukan konsultan pajak dan bukan nasihat pajak. Dasar: UU PPh s.t.d.t.d. UU 7/2021 (HPP) Pasal 7 & 17; PMK 101/PMK.010/2016 (PTKP); PMK 168/2023 (biaya jabatan, pembulatan PKP); PER-17/PJ/2015 & PMK 81/2024 (NPPN); PP 55/2022 jo. PP 20/2026 (PPh final UMKM); PP 60/2010 (zakat); PER-11/PJ/2025 (bentuk SPT Coretax); UU KUP Pasal 7; dicek per 30 September 2026. Pembulatan belum dicocokkan dengan hitungan otomatis Coretax. Skill ini tidak mengisi atau mengirim SPT atas nama Anda. Cocokkan dengan Coretax DJP, Kring Pajak 1500200, atau konsultan pajak terdaftar sebelum melapor._


**Hitungan independen penguji:** PTKP K/2 = 54.000.000 + 4.500.000 + 2 × 4.500.000 = 67.500.000. PKP = 180.000.000 − 67.500.000 = 112.500.000 (sudah bulat ribuan). PPh = 5% × 60.000.000 (3.000.000) + 15% × 52.500.000 (7.875.000) = 10.875.000. Kredit 10.500.000 → **KURANG BAYAR 375.000** ✔ sama dengan script.

**Penilaian:** angka benar; peta Coretax & langkah bayar (kode billing otomatis) benar. Kekurangan: (1) teks batas lapor menulis "diperpanjang sampai 30 April 2026" — menurut DJP (pajak.go.id/en/node/119611) jatuh tempo formal tetap 31 Maret 2026, KEP-55 hanya menghapus sanksi s.d. 30 April; (2) agent menyebut "kantor baru" padahal pengguna hanya punya satu kantor (salah kutip kecil); (3) tidak ada saran "cek ke HRD" — untuk 1 pemberi kerja setahun penuh, PPh 21 Desember seharusnya sudah menyamakan dengan PPh terutang, jadi selisih Rp375.000 patut ditanyakan ke HRD (baseline tanpa skill justru menyebut ini).

> **Catatan v1.0.1 (2026-09-30):** teks batas lapor & peringatan di atas diperbarui ke output script v1.0.1 (jatuh tempo formal TP 2025 tetap 31 Maret 2026; KEP-55/PJ/2026 hanya menghapus sanksi s.d. 30 April 2026). Peringatan cek ulang A1 ke HRD (kekurangan #3 di atas) kini dikeluarkan script. Angka tidak berubah.
