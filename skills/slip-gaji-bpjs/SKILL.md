---
name: slip-gaji-bpjs
description: Membuat slip gaji per karyawan dan rekap payroll bulanan untuk usaha Indonesia: gaji pokok, tunjangan, lembur sesuai PP 35/2021, potongan BPJS Kesehatan & Ketenagakerjaan (JHT, JP dengan batas upah terbaru, JKK, JKM), PPh 21 TER, take home pay, dan biaya total perusahaan; hasil slip siap cetak (Markdown + HTML) dan CSV rekap, plus peringatan upah di bawah UMK. Gunakan saat pengguna minta "buat slip gaji", "hitung gaji karyawan", "potongan BPJS", "payroll bulan ini", atau payslip, payroll Indonesia. Untuk PPh 21 setahun saja pakai pph21-ter; untuk THR pakai hitung-thr.
---

# Slip Gaji + BPJS + PPh 21

> **Aturan kerja:** Jangan menginstal paket/aplikasi (mis. `pip install`) — bila perlu, tunjukkan caranya dan biarkan pengguna yang memasang; jangan membuka atau mencari file selain yang diberikan pengguna, isi folder skill ini, dan file yang disebut di langkah kerja; jangan menulis file baru tanpa menyebut lokasinya, dan simpan hasil di folder kerja yang disepakati (bukan /tmp).

## Tujuan
Mengubah daftar gaji karyawan menjadi slip gaji siap cetak/kirim dan rekap payroll yang benar hitungannya: iuran BPJS sesuai batas upah terbaru, lembur sesuai PP 35/2021, PPh 21 metode TER, take home pay, dan total biaya perusahaan.

## Kapan digunakan
- "Buatkan slip gaji September untuk 5 karyawan saya" (dengan daftar/CSV/Excel yang disimpan sebagai CSV).
- "Gaji 7 juta, potongan BPJS dan pajaknya berapa? Take home pay-nya?"
- "Hitung lembur karyawan: 2 jam Senin, 3 jam Rabu, 8 jam hari Minggu."
- "Berapa total biaya perusahaan untuk gaji dan BPJS bulan ini?"

## Kapan TIDAK digunakan
- Hanya PPh 21 setahun/Desember/karyawan resign tanpa slip → `pph21-ter`. THR → `hitung-thr`.
- Pesangon/PHK, gross-up (pajak ditanggung perusahaan), karyawan WNA, gaji mata uang asing, iuran BPJS keluarga tambahan, BPJS pekerja bukan penerima upah → jelaskan di luar cakupan; arahkan ke BPJS, Disnaker, atau konsultan.
- Menentukan UMK → skill tidak menyimpan angka UMK; minta pengguna mengisi dari SK Gubernur/Disnaker.

## Input
| Info | Wajib? | Default jika tidak diberikan |
|---|---|---|
| Periode gaji (bulan & tahun) | Ya | — (tanyakan) |
| Per karyawan: nama, status PTKP (TK/0…K/3), gaji pokok | Ya | — (tanyakan) |
| Tunjangan tetap / tidak tetap, bonus, potongan lain (kasbon) | Tidak | 0 |
| Jam lembur per hari (hari kerja & hari libur) | Tidak | Tanpa lembur |
| Tarif JKK perusahaan (0,24/0,54/0,89/1,27/1,74%; PP 44/2015, tetap dipakai setelah PP 6/2025) | Tidak | 0,24% — sebutkan asumsi |
| UMK/UMP daerah (angka dari pengguna) | Tidak | Tidak dicek — sebutkan |
| Pola kerja 5 atau 6 hari/minggu | Tidak | 5 hari |
| Nama perusahaan | Tidak | Kosong |
| Sektor/KLU (untuk PPh 21 DTP 2026) | Hanya bila gaji tetap ≤ Rp 10 jt | Tanyakan; jangan diasumsikan |
| Bruto tetap & teratur Januari 2026 (atau bulan pertama kerja) — syarat DTP **≤ Rp 10.000.000** | Bila `dtp=ya` | Gaji pokok + tunjangan tetap bulan ini, dengan peringatan |
| Desember/karyawan berhenti: total bruto pajak & PPh 21 Januari s.d. bulan lalu, **mulai kerja bulan apa** (atau jumlah bulan kerja tahun ini) | Ya (bulan itu saja) | — (tanyakan; script menolak bila kosong) |

Jika info wajib kurang, tanyakan **sekali** dalam satu pesan bernomor (maks. 5 pertanyaan). Jika pengguna ingin cepat, pakai default dan sebutkan asumsinya.

## Langkah kerja

> **Lokasi script:** semua script skill ini ada di subfolder `scripts/` di folder yang sama dengan SKILL.md ini (folder skill). Jalankan dari sana; jangan mencari script atau file pengguna ke seluruh disk (mis. `find /`) — itu lambat dan menyentuh data pribadi di luar folder kerja.
1. Susun data karyawan menjadi CSV (pemisah `;` atau `,`) dengan kolom seperti `templates/karyawan-contoh.csv`. Kolom wajib: `nama`, `ptkp`, `gaji_pokok`. Kolom opsional: `jabatan`, `nik`, `tunjangan_tetap`, `tunjangan_tidak_tetap`, `lembur_hari_kerja` (jam per hari dipisah `+`, mis. `2+3+1`), `lembur_hari_libur` (mis. `8+5`; pola 6 hari: akhiran `p` bila libur resmi jatuh di hari kerja terpendek, mis. `5p`), `lembur_rp` (nominal lembur jadi, bila tidak pakai jam), `bonus`/`thr`, `potongan_lain`, `zakat`, `jkk_persen`, `ikut_jp`/`ikut_bpjs_tk`/`ikut_bpjs_kesehatan` (ya/tidak), `dtp` (ya/tidak; hanya masa 2026, sektor/KLU sudah dikonfirmasi, dan `bruto_tetap_januari` ≤ Rp 10 jt — bila tidak memenuhi, script otomatis memotong PPh normal dan memberi ⚠️), `bruto_tetap_januari`, `dasar_bpjs_kesehatan`, dan untuk Desember/berhenti: `berhenti`, `bruto_sd_bulan_lalu`, `pph21_sd_bulan_lalu`, `iuran_sd_bulan_lalu`, serta **wajib** `jumlah_bulan_kerja` atau `bulan_mulai` (1 bila sejak Januari).
   **Data gaji = data pribadi sensitif:** tulis CSV input dan folder `--out` di **folder kerja yang disepakati dengan pengguna** (mis. folder kerja OpenClaw/agent atau folder yang ia sebut), **bukan `/tmp`** atau folder sementara lain; sebutkan path lengkapnya (di aplikasi chat seperti Telegram/WhatsApp: cukup "disimpan di folder kerja asisten", **tanpa path**).
2. Jalankan (path relatif terhadap folder SKILL.md ini; Windows: `python` atau `py`):
   ```bash
   python3 <folder-skill-ini>/scripts/payroll.py --data karyawan.csv --periode 2026-09 --perusahaan "CV Maju Jaya" --umk "5.396.761" --jkk 0,54 --out payroll-2026-09
   ```
   Satu karyawan tanpa CSV: `--nama Budi --ptkp K/1 --gaji-pokok 6jt --tunjangan-tetap 500rb --lembur-hari-kerja 2+3`.
   Opsi lain: `--hari-kerja 6`, `--batas-jp <nilai>` (wajib bila periode di luar Maret 2025–Februari 2027), `--pemisah-csv ,`, `--format json`.
3. Script membuat 3 file di folder `--out`: `slip-gaji-YYYY-MM.md` (tempel ke chat/dokumen), `slip-gaji-YYYY-MM.html` (buka di browser → Cetak/Save as PDF; satu slip per halaman), `rekap-payroll-YYYY-MM.csv` (buka di Excel). Bila ada satu saja data karyawan yang salah, **tidak ada file dibuat** dan script menampilkan daftar kesalahannya.
4. Sampaikan ke pengguna (di aplikasi chat ikuti juga bagian **Penyajian di aplikasi chat** di bawah): rekap dari script, **baris "Total biaya gaji perusahaan = … " disalin persis dari keluaran script** (jangan menjumlah ulang total apa pun di kepala; bila butuh total lain, jalankan script dengan `--format json`), lokasi file (hanya di terminal/IDE; di aplikasi chat tidak), setiap ⚠️ peringatan (UMK, lembur > 4 jam, JKK tidak standar, dsb.), asumsi yang dipakai, dan disclaimer. Bila CSV input dibuat oleh agent dari data chat, **tawarkan untuk menghapusnya** setelah slip jadi (hapus hanya bila pengguna setuju).
5. **Fallback tanpa Python:** hitung manual dengan rumus di bawah, tulis langkahnya, tabel TER ada di `references/tabel-ter.md`, dan beri tahu pengguna bahwa hasil dihitung manual (slip HTML/CSV tidak dibuat).

## Penyajian di aplikasi chat (Telegram/WhatsApp) — WAJIB
Bila percakapan lewat aplikasi chat (Telegram, WhatsApp, dsb.) atau tidak jelas apakah tabel akan tampil rapi, pembeli harus **melihat slipnya langsung di chat**, bukan hanya diberi file:
1. **Baca isi `slip-gaji-YYYY-MM.md`** yang dibuat script (atau pakai `--format json`), lalu tulis ulang sebagai **teks rata** (pola di bawah). Angka **disalin persis**, tidak dihitung ulang. **Tanpa tabel Markdown** (Telegram tidak merender tabel) dan tanpa blok kode; maks. ±40 baris per slip.
2. **1–3 karyawan:** tampilkan semua slip utuh. **Lebih dari 3:** tampilkan 3 slip pertama utuh + rekap satu baris per karyawan (nama — take home pay — biaya perusahaan) + total dari script; slip lainnya ada di file.
3. Setelah slip: total biaya gaji perusahaan (salin baris script), setoran BPJS Kesehatan / BPJS Ketenagakerjaan / PPh 21, ⚠️ peringatan, asumsi, pembulatan, disclaimer singkat.
4. **File:** lampirkan slip HTML (siap cetak/PDF) dan rekap CSV bila kanal/alat bisa mengirim file. Bila tidak bisa, **jangan sebut nama file atau path** (buang baris `File:` dari keluaran script) dan tutup dengan: *Balas "kirim file" bila ingin slip lengkap siap cetak (PDF) dan rekap Excel.* Bila pengguna membalas "kirim file" tetapi lampiran tetap tidak bisa, jelaskan dengan bahasa sederhana bahwa file tersimpan di komputer tempat asisten berjalan, dan tawarkan menampilkan slip karyawan lain satu per satu di chat.

Pola satu slip (teks rata):
```
SLIP GAJI — <Perusahaan>
Periode: <Bulan Tahun>
Nama: <nama> (<jabatan>) · PTKP <status>

PENDAPATAN
- Gaji pokok: Rp …
- Tunjangan tetap / tidak tetap / Lembur / Bonus: Rp … (satu baris per pos yang tidak nol)
Total pendapatan: Rp …

POTONGAN
- BPJS Kesehatan 1%: Rp …
- BPJS TK JHT 2%: Rp … · JP 1%: Rp …
- PPh 21: Rp … (TER <kategori> <tarif>)
- Kasbon/potongan lain: Rp …
Total potongan: Rp …

TAKE HOME PAY: Rp …

Ditanggung perusahaan (tidak memotong gaji): BPJS Kes 4% Rp …; JHT 3,7% Rp …; JKK Rp …; JKM Rp …; JP 2% Rp …
```
Baris pos yang nilainya Rp 0 boleh dihilangkan; bila DTP, tampilkan "PPh 21 dipotong", "PPh 21 DTP dibayar tunai" (nilai sama), dan "setoran ke negara Rp 0" seperti di slip MD.

## Rumus (untuk hitung manual)
Dasar & sumber: `references/regulasi.md` (berlaku per 2026-09-23; JKK/JKP dicek ulang 2026-10-15 terhadap PP 37/2021 & PP 6/2025).
- Upah tetap = gaji pokok + tunjangan tetap.
- BPJS Kesehatan: dasar = upah tetap, minimal UMK, maksimal Rp 12.000.000 → perusahaan 4%, karyawan 1%.
- JHT: perusahaan 3,7%, karyawan 2% × upah tetap (tanpa batas). JKK (perusahaan) tarif risiko × upah tetap. JKM (perusahaan) 0,3%.
- JKK & JKP (PP 6/2025 Pasal 11 ayat (5), berlaku 7 Feb 2025; pengalihan 0,14% ini sudah ada sejak PP 37/2021): tarif JKK yang dibayar perusahaan **tetap 0,24–1,74%**; 0,14% di dalamnya dialihkan untuk JKP, sehingga PP itu menyebut porsi JKK murni 0,10/0,40/0,75/1,13/1,60%. Angka itu **bukan** tarif tagihan — jangan dipakai sebagai `jkk_persen`, dan **jangan menambah iuran JKP** (dibayar pemerintah 0,22% + rekomposisi JKK 0,14%).
- JP: dasar = upah tetap maks **Rp 11.086.300** (mulai Maret 2026; Rp 10.547.400 untuk Maret 2025–Feb 2026) → perusahaan 2%, karyawan 1%.
- Lembur: upah sejam = upah tetap ÷ 173 (bila ada tunjangan tidak tetap dan upah tetap < 75% total upah, pakai 75% total upah). Hari kerja: jam ke-1 × 1,5, jam berikutnya × 2. Hari libur (5 hari kerja): jam 1–8 × 2, jam 9 × 3, jam 10–12 × 4.
- Bruto pajak = semua pendapatan + JKK + JKM + BPJS Kesehatan 4% (bagian perusahaan). PPh 21 = TER (kategori dari PTKP) × bruto pajak; Desember/bulan berhenti: hitung ulang setahun (lihat skill `pph21-ter`).
- Take home pay = total pendapatan − (BPJS Kes 1% + JHT 2% + JP 1% + PPh 21 + zakat + potongan lain) [+ PPh 21 DTP tunai bila berhak].
- PPh 21 DTP (PMK 105/2025 Pasal 2 ayat 1, Pasal 5, Lampiran B; ringkasan `references/dtp-pmk105.md`): PPh 21 **tetap dipotong** (baris potongan), lalu nilai yang sama **dibayar tunai** (baris pendapatan "PPh 21 DTP dibayar tunai"), jadi gaji bersih tidak berkurang karena pajak — **bukan** gaji + DTP. Setoran PPh 21 ke negara untuk bagian DTP = Rp 0.
- Biaya perusahaan = penghasilan kotor (gaji pokok + tunjangan + lembur + bonus) + BPJS Kes 4% + JHT 3,7% + JKK + JKM + JP 2% (porsi perusahaan saja). Iuran porsi karyawan & PPh 21 **tidak** ditambah lagi — sudah termasuk di penghasilan kotor.
- Pembulatan: iuran & lembur ke rupiah terdekat; PPh 21 ke bawah. Belum dicocokkan dengan aplikasi BPJS/Coretax.

## Format output
```
**Rekap payroll <Bulan Tahun> — <Perusahaan>** (<n> karyawan)
| Nama | Total pendapatan | Potongan | PPh 21 | Take home pay | Biaya perusahaan |
(aplikasi chat: tanpa tabel — slip utuh teks rata dulu, lalu rekap satu baris per karyawan)
- Setor BPJS Kesehatan / BPJS Ketenagakerjaan / PPh 21
File: slip (MD, HTML siap cetak), rekap CSV — terminal/IDE: sebut lokasinya; aplikasi chat: lampirkan atau tawarkan "balas 'kirim file'" (tanpa path)
⚠️ Peringatan · Asumsi · Pembulatan
_Disclaimer + dasar aturan + tanggal berlaku_
```
Satu slip (isi file MD/HTML): identitas & periode → tabel Pendapatan → tabel Potongan → **TAKE HOME PAY** → iuran yang ditanggung perusahaan → keterangan PPh 21 → kolom tanda tangan (HTML).

## Contoh
**Input pengguna:** "Slip gaji September 2026 untuk Budi (K/1) gaji pokok 5 juta, tunjangan tetap 500 ribu, uang makan 600 ribu, lembur 2 jam dan 3 jam hari kerja plus 8 jam hari Minggu, kasbon 100 ribu. UMK 5.396.761, JKK 0,54%."

**Output (ringkas, dari script):** Lembur Rp 794.798 (upah sejam Rp 5.500.000 ÷ 173; 3,5 + 5,5 + 16 jam setara) → total pendapatan Rp 6.894.798; potongan BPJS Kes Rp 55.000, JHT Rp 110.000, JP Rp 55.000, PPh 21 Rp 53.707 (TER B 0,75% × bruto pajak Rp 7.160.998), kasbon Rp 100.000 → **take home pay Rp 6.521.091**; biaya perusahaan Rp 7.474.498.

## Checklist sebelum mengirim hasil
- [ ] Semua angka dari script (atau ditandai "dihitung manual"), termasuk total biaya gaji perusahaan (disalin dari baris script, bukan dijumlah sendiri).
- [ ] Batas JP sesuai periode; BPJS Kesehatan maks Rp 12 jt; JHT tanpa batas.
- [ ] Peringatan UMK disampaikan bila UMK diisi; bila tidak, sebutkan cek dilewati.
- [ ] Desember/karyawan berhenti memakai data Januari s.d. bulan lalu (hitung ulang).
- [ ] DTP hanya bila pengguna mengonfirmasi sektor/KLU, masa pajak 2026, dan bruto tetap Januari/bulan pertama kerja ≤ Rp 10 jt.
- [ ] Bila DTP: slip menampilkan PPh 21 dipotong, DTP dibayar tunai (nilai sama), setoran ke negara Rp 0, dan take home pay dari script (tidak pernah "gaji + DTP").
- [ ] Desember/berhenti: jumlah bulan kerja (atau bulan mulai) diisi sesuai fakta, bukan ditebak.
- [ ] JKK memakai tarif tagihan 0,24–1,74% (bukan porsi 0,10–1,60% di PP 37/2021 & PP 6/2025) dan tidak ada baris iuran JKP.
- [ ] Asumsi (JKK, pola kerja), pembulatan, dan disclaimer tercantum.
- [ ] Aplikasi chat: minimal 1 slip utuh (maks. 3) tampil langsung di chat sebagai teks rata tanpa tabel; tidak ada path file; file dilampirkan atau ditawarkan "balas 'kirim file'".

## Batasan & penanganan error
- Kode keluar 2 + pesan `ERROR:` untuk PTKP salah (mis. K/4), angka rusak, periode salah, jam lembur hari libur melebihi aturan, kolom Desember kosong, atau batas JP periode belum diketahui. Sampaikan dengan bahasa sederhana dan minta data yang benar.
- Batas 18 jam lembur/minggu tidak bisa dicek tanpa data per minggu; ingatkan pengguna.
- Pekerja berupah harian (upah sebulan = upah sehari × 25 atau × 21, PP 35/2021 Pasal 33) dan upah satuan hasil tidak didukung otomatis: minta pengguna mengisi upah sebulan hasil konversi sebagai `gaji_pokok`, atau isi `lembur_rp` sendiri.
- Data gaji adalah data pribadi: jangan kirim ke layanan luar; simpan file slip di komputer pengguna saja.
- Uji otomatis: `python3 <folder-skill-ini>/scripts/test_payroll.py`.
