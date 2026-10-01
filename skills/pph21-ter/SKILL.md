---
name: pph21-ter
description: Menghitung PPh 21 karyawan metode TER (PP 58/2023, PMK 168/2023) per bulan dan setahun: kategori TER A/B/C dari status PTKP, hitung ulang Desember/bulan berhenti kerja dengan tarif Pasal 17, karyawan masuk/keluar di tengah tahun, pekerja harian lepas, dan PPh 21 DTP 2026 (PMK 105/2025). Gunakan saat pengguna tanya "PPh 21 gaji", "potongan pajak karyawan", "TER", "PPh 21 Desember", "pajak karyawan resign", atau employee income tax, withholding tax Indonesia. Untuk slip gaji + BPJS lengkap pakai slip-gaji-bpjs; untuk THR pakai hitung-thr; untuk PPh UMKM 0,5% pakai pph-final-umkm.
---

# PPh 21 Karyawan (Metode TER)

> **Aturan kerja:** Jangan menginstal paket/aplikasi (mis. `pip install`) — bila perlu, tunjukkan caranya dan biarkan pengguna yang memasang; jangan membuka atau mencari file selain yang diberikan pengguna, isi folder skill ini, dan file yang disebut di langkah kerja; jangan menulis file baru tanpa menyebut lokasinya, dan simpan hasil di folder kerja yang disepakati (bukan /tmp).

## Tujuan
Menghitung PPh 21 yang wajib dipotong pemberi kerja dari gaji karyawan dengan angka pasti dari tabel resmi PP 58/2023, lengkap dengan tabel per bulan, hitung ulang Desember (atau bulan berhenti kerja), dan ringkasan setahun yang siap ditempel ke laporan/chat.

## Kapan digunakan
- "Gaji 10 juta, K/0, PPh 21-nya berapa sebulan?"
- "Hitung PPh 21 setahun karyawan saya, Desember kok potongannya besar?"
- "Karyawan resign Agustus, PPh 21 terakhirnya berapa?" / "Karyawan baru masuk September."
- Pekerja harian lepas / borongan: "tukang 20 hari, upah 250 ribu sehari."
- Cek apakah karyawan dapat PPh 21 DTP 2026 (PMK 105/2025).

## Kapan TIDAK digunakan
- Slip gaji lengkap + BPJS + take home pay → pakai `slip-gaji-bpjs`. THR → pakai `hitung-thr`.
- PPh Final UMKM 0,5% → `pph-final-umkm`. PPN → `hitung-ppn`.
- Pesangon, uang pensiun sekaligus, dan pencairan JHT (dikenai PPh 21 final dengan aturan tersendiri, bukan TER), honorarium bukan pegawai/freelancer, komisaris, WNA non-residen (PPh 26), gross-up/tunjangan pajak, PNS/TNI/Polri → jelaskan di luar cakupan dan arahkan ke konsultan pajak atau Kring Pajak 1500200.

## Input
| Info | Wajib? | Default jika tidak diberikan |
|---|---|---|
| Status PTKP per 1 Januari (TK/0 … K/3) | Ya | — (tanyakan) |
| Penghasilan bruto per bulan (gaji + tunjangan + lembur + bonus/THR bulan itu + premi JKK, JKM, BPJS Kesehatan bagian perusahaan) | Ya | — (tanyakan) |
| Iuran JHT 2% + JP 1% (atau dana pensiun) yang dipotong dari karyawan | Tidak | 0 — sebutkan asumsi; bila karyawan ikut BPJS TK, sarankan diisi |
| Bulan mulai kerja / bulan berhenti kerja tahun ini | Tidak | Januari–Desember, aktif |
| Bonus/THR/penghasilan tidak teratur dan bulannya | Tidak | Tidak ada |
| Zakat lewat perusahaan ke BAZNAS/LAZ resmi | Tidak | 0 |
| Sektor/KLU perusahaan (untuk PPh 21 DTP 2026) | Hanya bila relevan* | Jangan diasumsikan — tanyakan |

\*Tanyakan sektor HANYA bila tahun 2026 dan gaji tetap ≤ Rp 10 juta: "Apakah usaha Anda di industri alas kaki, tekstil & pakaian jadi, furnitur, kulit & barang kulit, atau pariwisata, dan KLU utamanya tercantum di Lampiran A PMK 105/2025?" Jangan pernah menganggap perusahaan berhak DTP tanpa jawaban "ya".

Jika info wajib kurang, tanyakan **sekali** dalam satu pesan bernomor (maks. 5 pertanyaan). Jika pengguna ingin cepat, pakai default dan sebutkan asumsinya di akhir.

## Langkah kerja

> **Lokasi script:** semua script skill ini ada di subfolder `scripts/` di folder yang sama dengan SKILL.md ini (folder skill). Jalankan dari sana; jangan mencari script atau file pengguna ke seluruh disk (mis. `find /`) — itu lambat dan menyentuh data pribadi di luar folder kerja.
1. Tentukan jenis pegawai: **tetap** (gaji bulanan teratur), **tidak tetap dibayar bulanan**, atau **tidak tetap harian/borongan**.
2. Jalankan script (path relatif terhadap folder SKILL.md ini; Windows: ganti `python3` dengan `python` atau `py`). Angka boleh ditulis `10jt`, `Rp 10.000.000`, `15,5jt`.
   - Satu bulan (Jan–Nov, atau pegawai tidak tetap bulanan):
     `python3 <folder-skill-ini>/scripts/pph21.py bulan --ptkp K/0 --bruto 10jt`
   - Setahun, gaji tetap sama tiap bulan:
     `python3 <folder-skill-ini>/scripts/pph21.py setahun --ptkp K/1 --gaji 12jt --iuran 360rb --tambahan Mar=12jt --tambahan Des=5jt`
     (`--iuran` = JHT 2% + JP 1% bagian karyawan per bulan; `--tambahan BULAN=NOMINAL` untuk THR/bonus.)
   - Masuk di tengah tahun: tambah `--mulai 9`. Berhenti kerja: `--akhir 8 --status berhenti`.
   - Gaji berbeda tiap bulan: buat CSV kolom `bulan,bruto,iuran_pensiun,zakat,pph_dipotong,bruto_tetap` (hanya `bulan` & `bruto` yang wajib; `pph_dipotong` = angka yang benar-benar dipotong bila beda) lalu `--data gaji.csv`.
   - PPh 21 DTP 2026 (hanya bila sektor sudah dikonfirmasi): tambah `--dtp` — berlaku di `bulan` **dan** `setahun`. Contoh satu bulan: `python3 <folder-skill-ini>/scripts/pph21.py bulan --ptkp TK/0 --bruto 6jt --dtp` (opsional `--bruto-tetap` = gaji + tunjangan tetap Januari 2026, `--premi-perusahaan`, `--potongan-lain` untuk iuran BPJS karyawan).
   - WNA yang baru datang/meninggalkan Indonesia di tengah tahun: tambah `--disetahunkan`. **Jangan** dipakai untuk karyawan yang sekadar pindah kerja.
   - Harian/borongan: `python3 <folder-skill-ini>/scripts/pph21.py harian --upah 250rb --hari 20` atau `--total 4,5jt --hari 10`.
   - `--format json` untuk angka mentah; `python3 <folder-skill-ini>/scripts/pph21.py tabel --kategori B` menampilkan tabel TER.
3. Tulis hasil memakai format di bawah dengan angka dari script **apa adanya**. Sampaikan setiap peringatan script.
   - **Bila DTP:** kutip apa adanya baris script "PPh 21 dipotong dari gaji", "PPh 21 DTP yang WAJIB dibayar tunai", dan "Uang yang diterima pegawai". DTP **bukan** sekadar "tidak dipotong": menurut PMK 105/2025 Pasal 5, nilai PPh 21 itu wajib dibayarkan **tunai** oleh pemberi kerja ke pegawai bersama gaji (contoh: gaji Rp 6.000.000 + DTP Rp 45.000 = diterima Rp 6.045.000). Jangan pernah menulis "gaji diterima utuh" untuk pegawai penerima DTP.
   - Pakai bahasa awam: sebut "KLU (kode jenis usaha di data pajak perusahaan)", "TER (tarif potongan bulanan dari tabel resmi)", "Masa Pajak Terakhir (Desember atau bulan karyawan berhenti)", "DTP (pajak yang dibayar pemerintah)" saat istilah itu pertama muncul.
4. Bila Desember/bulan berhenti menghasilkan angka negatif: jelaskan bahwa itu kelebihan potong yang wajib dikembalikan ke karyawan paling lambat akhir bulan berikutnya (kecuali DTP).
5. **Fallback tanpa Python:** hitung manual dengan rumus di bawah dan tabel di `references/tabel-ter.md` (dibuat otomatis dari tabel resmi), tulis setiap langkah, dan beri tahu pengguna bahwa hasil dihitung manual.
6. Periksa checklist sebelum mengirim.

## Rumus (untuk hitung manual)
Dasar: PP 58/2023, PMK 168/2023, UU HPP; berlaku per 2026-09-23. Rincian & sumber: `references/regulasi.md`.
1. Kategori: **A** = TK/0, TK/1, K/0 · **B** = TK/2, TK/3, K/1, K/2 · **C** = K/3.
2. Januari–November: **PPh 21 = tarif TER × bruto sebulan**. Baris tabel "di atas X s.d. Y": X tidak termasuk, Y termasuk.
3. Desember / bulan berhenti kerja (n = jumlah bulan bekerja tahun ini):
   - Biaya jabatan = 5% × bruto, maks Rp 500.000 × n (maks Rp 6.000.000).
   - Neto = bruto − biaya jabatan − iuran JHT/JP/pensiun karyawan − zakat lewat perusahaan.
   - PKP = neto − PTKP (TK/0 54 jt; +4,5 jt kawin; +4,5 jt per tanggungan, maks 3), **dibulatkan ke bawah ke ribuan**.
   - PPh setahun = 5% × s.d. 60 jt + 15% × 60–250 jt + 25% × 250–500 jt + 30% × 500 jt–5 M + 35% × di atas 5 M.
   - PPh bulan terakhir = PPh setahun − PPh yang sudah dipotong bulan-bulan sebelumnya.
4. Harian: s.d. Rp 450.000/hari 0%; di atas s.d. Rp 2.500.000/hari 0,5%; di atas Rp 2.500.000/hari: 5% (lapisan Pasal 17) × 50% × upah sehari.

**Pembulatan:** PPh dibulatkan ke bawah ke rupiah penuh; PKP ke bawah ke ribuan. Belum dicocokkan dengan Coretax; bila berbeda, ikuti Coretax.

## Format output
```
**PPh 21 <tahun> — <nama/jabatan bila ada>, status <PTKP> (TER kategori <A/B/C>)**
| Bulan | Penghasilan bruto | Tarif TER | PPh 21 dipotong | (PPh 21 DTP) |
... (dari script)
**Hitung ulang Desember/bulan berhenti** (rincian biaya jabatan, iuran, neto, PTKP, PKP, lapisan tarif)
**Ringkasan setahun:** total bruto, total PPh 21, kelebihan yang dikembalikan (bila ada)
(Bila DTP) **PPh 21 dipotong dari gaji: Rp 0 · DTP dibayar tunai ke pegawai: Rp … · Uang diterima pegawai: Rp …** (dari script)
Asumsi: <daftar default yang dipakai>
⚠️ <peringatan script>
_Alat bantu hitung, bukan nasihat pajak. Dasar: PP 58/2023, PMK 168/2023, UU HPP, PMK 105/2025, berlaku per 23 September 2026. Kasus khusus: Kring Pajak 1500200 atau konsultan pajak._
```

## Contoh
**Input pengguna:** "Karyawan saya K/0 gaji 10 juta sebulan, iuran pensiun dipotong 100 ribu. PPh 21 setahun berapa?"

**Perintah:** `python3 <folder-skill-ini>/scripts/pph21.py setahun --ptkp K/0 --gaji 10jt --iuran 100rb`

**Output (ringkas):**
```
| Januari–November | Rp 10.000.000 | 2% | Rp 200.000 per bulan |
| Desember | Rp 10.000.000 | Pasal 17 (hitung ulang) | Rp 515.000 |
Desember: bruto 120.000.000 − biaya jabatan 6.000.000 − iuran 1.200.000 = neto 112.800.000;
PKP 112.800.000 − 58.500.000 = 54.300.000; PPh setahun 5% = Rp 2.715.000; dikurangi 11 × 200.000 → Rp 515.000.
```
(Angka ini sama dengan contoh resmi di Penjelasan PP 58/2023.)

## Checklist sebelum mengirim hasil
- [ ] Angka berasal dari script (atau ditandai "dihitung manual").
- [ ] Kategori TER sesuai status PTKP per 1 Januari; K/3 = kategori C.
- [ ] Bruto sudah termasuk premi JKK, JKM, BPJS Kesehatan bagian perusahaan bila ada; JHT/JP bagian perusahaan TIDAK dimasukkan.
- [ ] Desember/bulan berhenti dihitung ulang dengan Pasal 17, bukan TER.
- [ ] DTP hanya dipakai bila pengguna mengonfirmasi sektor/KLU.
- [ ] Bila DTP: tertulis bahwa DTP **dibayar tunai** ke pegawai dan "uang diterima pegawai" = gaji + DTP tunai (dikutip dari script), bukan "gaji utuh".
- [ ] Asumsi, peringatan, pembulatan, dan disclaimer ada; format `Rp 1.250.000`.

## Batasan & penanganan error
- Script keluar dengan kode 2 dan pesan `ERROR: ...` untuk PTKP tidak valid (mis. K/4 → pakai K/3), angka rusak, format Inggris (`1,250,000.50`), bulan ganda, atau rentang bulan salah. Sampaikan dengan bahasa sederhana dan minta data yang benar.
- Status PTKP berubah di tengah tahun (menikah/punya anak) tidak mengubah PTKP tahun berjalan; berlaku tahun berikutnya.
- Karyawan pindah kerja: pemberi kerja baru boleh menggabungkan penghasilan dari pemberi kerja lama hanya bila karyawan menyerahkan bukti potong Masa Pajak Terakhir dari kantor lama — di luar hitungan otomatis; jelaskan dan arahkan ke konsultan.
- Uji otomatis: `python3 <folder-skill-ini>/scripts/test_pph21.py` (mencocokkan tabel dengan salinan resmi dan semua contoh resmi PMK 168/2023 & PMK 105/2025).
