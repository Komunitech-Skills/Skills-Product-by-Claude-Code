# 02 — Freelancer desain grafis dengan NPPN (normal)

**Input pengguna (persis):**
> saya freelancer desain grafis di Bandung, belum nikah tapi nanggung ibu. total fee 2025 sekitar 240jt. udah lapor pakai norma di coretax bulan februari. klien2 motong pph 21 totalnya 2,4jt. norma saya katanya 32% (udah cek tabel). pajak saya berapa?

**Pemetaan agent:** status TK/1 (ibu kandung yang ditanggung = 1 tanggungan), NPPN bruto 240 jt × 32% (angka dari pengguna, Bandung termasuk 10 ibu kota provinsi), pemberitahuan NPPN = ya, PPh 21 bukan pegawai 2,4 jt.

**Perintah:**
```bash
python3 scripts/spt_op.py --status TK/1 --tahun 2025 --nppn 240jt 32 --nppn-diberitahukan ya --pph21-lain 2,4jt --hari-ini 2026-09-30
```

**Output script (apa adanya):**

## Hitungan SPT Tahunan PPh Orang Pribadi — Tahun Pajak 2025 (status TK/1)

**1. Penghasilan neto**

| Sumber | Neto |
|---|---|
| Usaha/pekerjaan bebas #1 — NPPN 32% × Rp 240.000.000 | Rp 76.800.000 |
| **Jumlah** | **Rp 76.800.000** |
| **Penghasilan neto** | **Rp 76.800.000** |

**2. PTKP & Penghasilan Kena Pajak (PKP)**

- Wajib pajak sendiri: Rp 54.000.000
- Tanggungan 1 orang × Rp 4.500.000: Rp 4.500.000
- **PTKP TK/1: Rp 58.500.000**
- PKP = Rp 76.800.000 − Rp 58.500.000 = Rp 18.300.000 → dibulatkan ke bawah ribuan: **Rp 18.300.000**

**3. PPh terutang (tarif Pasal 17 UU HPP)**

- 5% × Rp 18.300.000 = Rp 915.000
- **PPh terutang: Rp 915.000**

**4. Kredit pajak (sudah dipotong/dibayar)**

- PPh 21 bukan pegawai / lainnya (bukti potong): Rp 2.400.000
- **Total kredit: Rp 2.400.000**

**5. Hasil: LEBIH BAYAR**
Kredit Rp 2.400.000 − PPh terutang Rp 915.000 = **Rp 1.485.000 lebih bayar**.
Perkiraan angsuran PPh 25 tahun 2026: **Rp 0 per bulan**.

**Batas lapor:** 31 Maret 2026 (jatuh tempo formal tetap). Khusus tahun pajak 2025: sanksi administrasi (denda & bunga) dihapus bila lapor dan/atau bayar paling lambat 30 April 2026 (KEP-55/PJ/2026) — JATUH TEMPO SUDAH LEWAT

**⚠️ Peringatan**
- Batas lapor (2026-03-31) SUDAH LEWAT per 2026-09-30 (masa penghapusan sanksi KEP-55/PJ/2026 s.d. 2026-04-30 juga sudah berakhir). Tetap laporkan secepatnya; denda telat lapor SPT Tahunan OP Rp100.000 ditagih lewat STP.

**Catatan**
- Persen norma NPPN wajib dicocokkan dengan lampiran PER-17/PJ/2015 sesuai KLU dan wilayah (10 ibu kota provinsi / ibu kota provinsi lain / daerah lain).
- Perkiraan angsuran PPh 25 tahun 2026 = (PPh terutang − PPh 21/22/23 yang dipotong) ÷ 12 (UU PPh Pasal 25 ayat (1)). Cocokkan dengan Lampiran 4 di Coretax.
- Lebih bayar Rp 1.485.000: pilih 'dikembalikan' (restitusi; untuk kondisi Anda umumnya lewat pengembalian pendahuluan, Pasal 17D UU KUP) atau 'dikompensasikan' ke tahun depan. Siapkan semua bukti potong asli.

**Checklist dokumen**
- [ ] Akun Coretax aktif (login NIK/NPWP 16 digit) + kode verifikasi/otorisasi untuk tanda tangan SPT
- [ ] Daftar HARTA per 31 Desember (tanah/bangunan, kendaraan, tabungan, deposito, emas, investasi) dengan tahun perolehan & nilai
- [ ] Daftar UTANG per 31 Desember (KPR, kredit kendaraan, pinjaman) — nama pemberi pinjaman & sisa pokok
- [ ] Data keluarga & tanggungan (NIK) sesuai keadaan 1 Januari
- [ ] Bukti potong PPh 21 bukan pegawai (honor/fee) dari tiap pemberi penghasilan
- [ ] Rekap peredaran bruto per bulan (pencatatan) + bukti pemberitahuan penggunaan NPPN ke DJP
- [ ] Nomor rekening bank atas nama sendiri bila memilih restitusi

_Alat bantu hitung, bukan konsultan pajak dan bukan nasihat pajak. Dasar: UU PPh s.t.d.t.d. UU 7/2021 (HPP) Pasal 7 & 17; PMK 101/PMK.010/2016 (PTKP); PMK 168/2023 (biaya jabatan, pembulatan PKP); PER-17/PJ/2015 & PMK 81/2024 (NPPN); PP 55/2022 jo. PP 20/2026 (PPh final UMKM); PP 60/2010 (zakat); PER-11/PJ/2025 (bentuk SPT Coretax); UU KUP Pasal 7; dicek per 30 September 2026. Pembulatan belum dicocokkan dengan hitungan otomatis Coretax. Skill ini tidak mengisi atau mengirim SPT atas nama Anda. Cocokkan dengan Coretax DJP, Kring Pajak 1500200, atau konsultan pajak terdaftar sebelum melapor._

**Penjelasan bahasa awam (ditulis agent):**
> Dengan norma, penghasilan bersih Anda dianggap 32% dari fee: Rp76,8 juta. Setelah dikurangi PTKP Rp58,5 juta, yang kena pajak Rp18,3 juta × 5% = Rp915.000. Klien sudah memotong Rp2,4 juta (karena PPh 21 bukan pegawai dipotong per pembayaran tanpa melihat PTKP), jadi Anda **lebih bayar Rp1.485.000**. Anda bisa minta dikembalikan (restitusi) atau dikompensasikan ke tahun depan.

**Peta ke Coretax:** peredaran bruto & norma → Lampiran 3 (neto usaha/pekerjaan bebas, L-3A-4 dan rekap L-3B) · bukti potong PPh 21 bukan pegawai → daftar bukti potong/kredit (Bagian D) · lebih bayar → Bagian E & G (pilih dikembalikan/kompensasi).

**Langkah berikutnya:** kumpulkan semua bukti potong dari klien (cek jumlahnya sama dengan 2,4 jt), rekap fee per bulan, dan bukti pemberitahuan NPPN. Jatuh tempo TP 2025 (31 Maret 2026) dan masa penghapusan sanksi KEP-55 (s.d. 30 April 2026) sudah lewat → lapor secepatnya (denda Rp100.000).

**Verifikasi manual:** 240.000.000 × 32% = 76.800.000; − 58.500.000 = 18.300.000; × 5% = 915.000; 2.400.000 − 915.000 = **1.485.000 LB** ✔.

> **Catatan v1.0.1 (2026-09-30):** teks batas lapor & peringatan di atas diperbarui ke output script v1.0.1 (jatuh tempo formal TP 2025 tetap 31 Maret 2026; KEP-55/PJ/2026 hanya menghapus sanksi s.d. 30 April 2026). Angka tidak berubah.
