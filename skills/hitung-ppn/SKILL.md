---
name: hitung-ppn
description: Kalkulator PPN Indonesia 12% (DPP nilai lain 11/12, efektif 11% untuk non-mewah; 12% penuh untuk barang mewah) dari harga sebelum pajak atau harga sudah termasuk PPN, lengkap DPP, DPP nilai lain, PPN, total, pembulatan, dan peringatan bila penjual bukan PKP. Gunakan saat pengguna tanya "PPN-nya berapa", "harga include PPN", "pisahkan PPN", atau VAT calculator, tax-inclusive price, VAT Indonesia. Untuk membuat tagihan lengkap pakai buat-invoice; untuk PPh UMKM pakai pph-final-umkm.
---

# Hitung PPN

## Tujuan
Menghitung PPN dengan benar sesuai aturan 2025–2026 (tarif 12% dengan DPP nilai lain 11/12) dan menjelaskan hasilnya dengan bahasa sederhana, siap ditempel ke penawaran, chat, atau catatan.

## Kapan digunakan
- "Harga Rp 1.000.000, PPN-nya berapa?" / "Totalnya jadi berapa setelah PPN?"
- "Harga Rp 1.110.000 sudah termasuk PPN, harga pokoknya berapa?"
- Mengecek PPN di tagihan/penawaran supplier.
- Membandingkan barang biasa dengan barang mewah (kena PPnBM).

## Kapan TIDAK digunakan
- Membuat invoice/kuitansi lengkap → pakai skill `buat-invoice`.
- PPh Final UMKM 0,5% → pakai skill `pph-final-umkm`.
- Menghitung PPnBM, PPN impor, PPN "besaran tertentu" (mis. kendaraan bekas, emas, pulsa), atau barang/jasa yang dibebaskan PPN (mis. sembako, jasa kesehatan/pendidikan) → jelaskan bahwa di luar cakupan dan arahkan ke DJP/konsultan pajak.
- Membuat faktur pajak resmi → faktur dibuat di Coretax, bukan di sini.

## Input
| Info | Wajib? | Default jika tidak diberikan |
|---|---|---|
| Harga (per unit atau total) | Ya | — (tanyakan) |
| Harga itu sudah termasuk PPN atau belum | Ya | Anggap **belum termasuk** dan sebutkan asumsinya |
| Jenis: barang/jasa biasa atau barang mewah (kena PPnBM) | Tidak | Biasa (non-mewah) |
| Jumlah unit | Tidak | 1 |
| Status penjual: PKP / bukan PKP | Tidak | "belum tahu" → beri pengingat |
| Cara pembulatan | Tidak | Ke bawah (buang pecahan rupiah) |

Jika info wajib kurang, tanyakan **sekali** dalam satu pesan bernomor (maks. 5 pertanyaan). Jika pengguna ingin cepat, pakai default dan sebutkan asumsinya di akhir.

## Langkah kerja
1. Ambil angka dari pesan pengguna. Format Indonesia diterima: `Rp 1.250.000`, `1,5jt`, `15.000,50`.
2. Jalankan script (path relatif terhadap folder SKILL.md ini; Windows: ganti `python3` dengan `python` atau `py`):
   ```bash
   python3 <folder-skill-ini>/scripts/hitung_ppn.py --harga "1.000.000" --mode sebelum --jenis umum --status-pkp pkp
   ```
   - `--mode termasuk` bila harga sudah termasuk PPN.
   - `--jenis mewah` untuk barang mewah (kena PPnBM).
   - `--qty 10` bila harga per unit.
   - `--status-pkp non-pkp` bila penjual bukan PKP (hasil diberi label SIMULASI).
   - `--pembulatan terdekat` bila pengguna minta pembulatan biasa.
   - `--format json` bila butuh angka mentah.
3. Tulis hasil dengan format di bawah, **pakai angka dari script apa adanya**.
4. Bila penjual bukan PKP: tegaskan bahwa ia **tidak boleh memungut PPN** atau mencantumkan PPN di tagihan.
5. **Fallback tanpa Python:** jika script tidak bisa dijalankan, hitung manual dengan rumus di bawah, tulis tiap langkah, dan beri tahu pengguna bahwa hasil dihitung manual.
6. Periksa checklist sebelum mengirim.

## Rumus (untuk hitung manual)
Dasar: UU HPP & PMK 131/2024, berlaku per 2026-09-23. Detail & sumber: `references/regulasi.md`.

**A. Harga BELUM termasuk PPN (H = harga × jumlah)**
| Jenis | DPP | DPP nilai lain | PPN | Total |
|---|---|---|---|---|
| Biasa (non-mewah) | H | 11/12 × H | 12% × DPP nilai lain = **11% × H** | H + PPN |
| Mewah (PPnBM) | H | — (sama dengan H) | **12% × H** | H + PPN |

**B. Harga SUDAH termasuk PPN (T)**
- Biasa: DPP = T × 100/111. Mewah: DPP = T × 100/112.
- Bulatkan DPP ke rupiah penuh, hitung PPN dari DPP itu (rumus A), lalu cek DPP + PPN ≤ T. Jika lebih, kurangi DPP Rp1 dan hitung ulang.
- Selisih = T − (DPP + PPN); biasanya Rp0–Rp1 karena pembulatan.

**Pembulatan:** PPN dibulatkan ke rupiah penuh **ke bawah** (pecahan rupiah dibuang). PPN dihitung langsung 11% × DPP (secara matematis sama dengan 12% × 11/12 × DPP) agar tidak terjadi pembulatan berantai. DPP nilai lain ditampilkan 2 desimal sebagai informasi.

Contoh: H = Rp 1.000.000 → DPP nilai lain = Rp 916.666,67 → PPN = 12% × 916.666,67 = Rp 110.000 → Total Rp 1.110.000.

## Format output
```
**Perhitungan PPN** (<barang/jasa biasa | barang mewah>)
- Harga sebelum PPN (DPP): Rp ...
- DPP nilai lain (11/12): Rp ...          ← hanya untuk non-mewah
- PPN 12%: Rp ...  (setara 11% dari harga) ← atau "12% x harga" untuk mewah
- **Total dibayar: Rp ...**

Cara hitung: <1–2 kalimat rumus dengan angka pengguna>
Pembulatan: PPN dibulatkan ke bawah ke rupiah penuh.
<Peringatan PKP bila relevan>

_Dasar: UU HPP & PMK 131/2024, berlaku per 23 September 2026. Alat bantu hitung, bukan nasihat pajak; untuk kasus khusus hubungi DJP (Kring Pajak 1500200) atau konsultan pajak._
```

## Contoh
**Input pengguna:** "Harga jasa desain 7,5 juta sudah termasuk PPN. PPN-nya berapa? Saya PKP."

**Perintah:** `python3 <folder-skill-ini>/scripts/hitung_ppn.py --harga 7,5jt --mode termasuk --status-pkp pkp`

**Output:**
```
**Perhitungan PPN** (barang/jasa biasa)
- Harga termasuk PPN: Rp 7.500.000
- Harga sebelum PPN (DPP): Rp 6.756.757
- DPP nilai lain (11/12): Rp 6.193.693,92
- PPN 12%: Rp 743.243 (setara 11% dari DPP)
- **Total: Rp 7.500.000** (tanpa selisih pembulatan)

Cara hitung: DPP = 7.500.000 × 100/111 ≈ Rp 6.756.757; PPN = 11% × 6.756.757 = Rp 743.243,27 → dibulatkan ke bawah Rp 743.243.
Pembulatan: PPN dibulatkan ke bawah ke rupiah penuh.

_Dasar: UU HPP & PMK 131/2024, berlaku per 23 September 2026. Alat bantu hitung, bukan nasihat pajak; untuk kasus khusus hubungi DJP (Kring Pajak 1500200) atau konsultan pajak._
```

## Checklist sebelum mengirim hasil
- [ ] Angka berasal dari script (atau ditandai "dihitung manual").
- [ ] Jelas apakah harga awal termasuk/belum termasuk PPN, dan asumsinya disebut.
- [ ] Non-mewah memakai 11/12; mewah memakai 12% penuh.
- [ ] Peringatan PKP muncul bila status non-PKP atau belum diketahui.
- [ ] Pembulatan dijelaskan; format Rupiah `Rp 1.250.000`.
- [ ] Disclaimer + tanggal berlaku ada.

## Batasan & penanganan error
- Script keluar dengan kode 2 dan pesan `ERROR: ...` untuk angka tidak valid, harga negatif, atau jumlah 0. Sampaikan pesan itu dengan bahasa sederhana dan minta angka yang benar.
- Format angka Inggris (`1,250,000.50`) ditolak agar tidak salah baca; minta ditulis `1.250.000,50`.
- Pembulatan resmi di Coretax bisa berbeda Rp1 pada kasus tertentu; bila berbeda, ikuti angka Coretax.
- Barang/jasa dengan DPP atau tarif khusus, fasilitas dibebaskan/tidak dipungut, dan PPnBM di luar cakupan → arahkan ke DJP/konsultan.
- Batas pengusaha kecil (wajib jadi PKP) umumnya omzet Rp4,8 miliar setahun; pastikan ke DJP bila pengguna mendekati batas itu.
