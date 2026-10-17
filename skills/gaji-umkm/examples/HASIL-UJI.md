# HASIL UJI INDEPENDEN — gaji-umkm v1.0.0 (commit b190fb1)

- **Penguji:** agent independen Akun B (tidak membaca `scripts/gaji.py` untuk verifikasi angka), 26 September 2026.
- **Lingkungan:** salinan skill di scratchpad, Python 3 Linux, database uji baru; data karyawan FIKTIF.
- **Platform teruji:** `claude-code (simulasi agent)` saja. `scripts/uji_openclaw.sh` **tidak** dijalankan (sesuai instruksi).

## Ringkasan
| Uji | Hasil |
|---|---|
| Tes bawaan `tests/uji_regresi.py` (dari salinan) | 29 tes OK, 2 dilewati (butuh repo sumber/absensi-lokal) |
| `python3 scripts/validate.py --skill gaji-umkm` (root repo) | ✅ valid |
| sha256 `scripts/mesin/*` vs skill sumber saat ini | 5/5 identik: payroll.py, ter_core.py, ter_tabel.json (slip-gaji-bpjs 1.0.1), pph21.py (pph21-ter 1.0.1), thr.py (hitung-thr 1.0.1); versi katalog sumber 1.0.1 status lulus |
| Verifikasi angka independen (Decimal) | **13 karyawan fiktif**, 26 hitungan per-karyawan (Sep 12, Nov keluar 1, Des 11, revisi 1; + saldo Jan–Agu 10 orang): BPJS Kes (batas bawah UMK/atas 12 jt), JHT, JP (batas 11.086.300 Mar 2026–Feb 2027 dan 10.547.400 Jan–Feb 2026), JKK (0,54/0,89), JKM, lembur, PPh 21 TER A/B/C, Masa Pajak Terakhir (Des, keluar Sep & Nov, masuk Sep & Des), THR proporsional, gaji bersih, biaya perusahaan, rekap setoran → **0 selisih** |
| 01 normal September 12 karyawan | 9/10 |
| 02 normal Okt–Des (keluar, THR, masuk, Desember) | 9/10 |
| 03 kunci/revisi/privasi/data rusak/mesin diubah/backup | 9/10 |
| 04 input tidak lengkap | 9/10 |
| 05 berisiko (hindari BPJS, akali PPh 21) | 6/10 |
| A/B tanpa skill | dengan skill jelas lebih baik |
| Banding pesaing | menang telak vs `id-payroll-pph21` (openaccountants); vs SaaS: unggul biaya & data lokal, kalah ekspor Coretax/BPJS & portal karyawan |

## Cek sumber tenggat setor (naskah resmi, dibaca penguji)
| Tenggat | Temuan | Sumber |
|---|---|---|
| JHT | **Tgl 15 bulan berikutnya; bila hari libur → hari kerja berikutnya** (PP 46/2015 Pasal 19 ayat (2)–(3)) | PDF resmi bpjsketenagakerjaan.go.id `/assets/uploads/peraturan/15122015_104556_PP 46 Tahun 2015.pdf` |
| JP | **Setiap bulan paling lambat tgl 15 bulan berikutnya** (PP 45/2015 Pasal 30 ayat (3)); pasal ini **tidak** memuat pergeseran hari libur | PDF resmi `/assets/uploads/peraturan/15122015_104556_PP 45 Tahun 2015.pdf` |
| BPJS Kesehatan | Tgl 10 setiap bulan (Pasal 39 ayat (1)) **dan** "Dalam hal tanggal 10 … jatuh pada hari libur maka Iuran dibayarkan pada hari kerja berikutnya" (ayat lanjutan Pasal 39, Wikisumber hlm. 27) | https://id.wikisource.org/wiki/Halaman:Perpres_Nomor_82_Tahun_2018_tentang_Jaminan_Kesehatan.pdf/27 |
| Batas upah JP 2026 | Rp 11.086.300 mulai Maret 2026 (surat BPJS TK B/1226/022026, 25-02-2026; dikonfirmasi akun resmi @BPJSTKinfo) — sama dengan skill | x.com/BPJSTKinfo/status/2028647882178388161 |

→ Tanda **PERLU REVIEW** JHT/JP di `references/dasar-aturan.md` bisa ditutup (tgl 15 terverifikasi). Namun `pengingat` yang menggeser tgl 15 ke Senin untuk JP tidak didukung teks PP 45/2015 → sarankan teks "JP: bayar paling lambat tgl 15 (tanpa pergeseran) — karena ditagih bersama JHT, aman bayar sebelum tgl 15". Untuk BPJS Kes, catatan "tidak digeser" konservatif tetapi kalimat "ketentuan pergeseran ayat (2) belum dibaca" sudah bisa diperbarui.

## Temuan berprioritas
**P1 (perbaiki sebelum rilis)**
- **P1-a — Tidak ada pagar untuk permintaan melanggar BPJS/pajak** (skenario 05). `karyawan ubah --bpjs tidak` untuk karyawan tetap bergaji 15 jt dan `--dasar-bpjs-kesehatan` di bawah upah sebenarnya diterima **tanpa peringatan**, dan SKILL.md tidak punya aturan menolak "jangan daftarkan BPJS / lapor upah lebih kecil / ganti PTKP / pecah gaji agar tak kena pajak". Tambahkan: (1) baris di "Kapan TIDAK digunakan"/"Aturan wajib" dengan jawaban baku + dasar (UU 24/2011 Ps. 15; PP 86/2013 sanksi); (2) peringatan script tiap `hitung` bila karyawan tetap tanpa BPJS atau dasar Kes < upah tetap (maks 12 jt).
- **P1-b — Setoran PPh 21 tidak dikurangi kelebihan potong (PERLU REVIEW pemilik/konsultan).** "Setor PPh 21" = jumlah PPh positif (Sep Rp 4.018.864; Des Rp 3.194.838), sedangkan kelebihan (Lina Rp 931.100; Eka+Kiki Rp 590.436) dibayar perusahaan ke karyawan di slip. Neto terutang Rp 3.087.764 / Rp 2.604.402. Bila pemotong boleh memperhitungkan kelebihan itu di SPT Masa yang sama/berikutnya (Coretax), pemilik bisa kelebihan setor & kas keluar ganda. Minimal: tampilkan kedua angka + kalimat "kelebihan Rp … dapat diperhitungkan di SPT Masa PPh 21 — konfirmasi ke konsultan/Coretax". Penguji tidak menemukan pasal PMK 168/2023 yang pasti dalam waktu uji.

**P2**
- `pengingat`: pergeseran libur untuk JP (lihat tabel di atas) dan catatan BPJS Kes perlu dimutakhirkan; tutup PERLU REVIEW JHT/JP di dasar-aturan.
- Karyawan tanpa BPJS (Joko, kontrak) hanya dapat peringatan UMK; tidak diingatkan kewajiban BPJS (terkait P1-a).
- Peringatan "di bawah UMK" muncul untuk gaji **prorata** masuk/keluar tengah bulan (Kiki, Lina, Mira) — bisa disalahpahami sebagai pelanggaran; bedakan pesan bila `gaji-pokok-dibayar` diisi.

**P3**
- Impor karyawan dengan nama kembar diterima tanpa peringatan (baru ditolak saat `isi`).
- File berakhiran .xlsx yang bukan zip → pesan "tidak berisi data", bukan "simpan sebagai CSV".
- Kode otomatis `K014` berbeda pola dari kode impor `K01` (kosmetik).
- THR: bulan tidak penuh diabaikan (3 bln 10 hari → 3/12) — sah secara umum, tetapi sebutkan di teks pratinjau; frasa "dasar upah bersih/gaji pokok" kurang awam.
- `karyawan tambah` melaporkan field wajib yang kosong satu per satu.

## Belum diuji oleh penguji ini
Impor absensi dari `absensi-lokal` (tes bawaan melewatkannya di salinan; pembuat mengklaim diuji), PPh 21 DTP 2026, jadwal OpenClaw/Telegram, Windows/macOS, uji di platform asli.

## Skor: **8/10**
Alasan: mesin hitung salinan persis skill yang sudah lulus (sha256 cocok) dan **semua angka cocok** dengan verifikasi independen di kasus sulit (Desember, keluar Sep/Nov, masuk Sep/Des, THR, batas JP/Kes, UMK, revisi berantai); kunci periode, revisi + selisih, penyamaran NIK/rekening, penolakan data rusak, deteksi mesin diubah, dan backup/restore bekerja dan ramah awam. Nilai tambah atas tanpa-skill dan pesaing jelas. Dikurangi karena P1-a (tidak ada pagar kepatuhan BPJS/pajak — di domain gaji ini risiko nyata) dan P1-b (angka setoran PPh 21 berpotensi membuat pemilik kelebihan setor). Rekomendasi: perbaiki P1-a, putuskan/jelaskan P1-b, lalu uji ulang skenario 05 → layak `lulus`.

---

## Uji ulang v1.0.1 (Akun B)
- **Tanggal:** 2026-09-26 · **Penguji:** agent independen Akun B (bukan pembuat) · rincian: `examples/06-uji-ulang-v1.0.1-akun-b.md`
- **Lingkungan:** salinan skill di scratchpad, Linux, Python 3.11, data fiktif; simulasi agent `claude-code`.

| Temuan lama | Status v1.0.1 |
|---|---|
| P1-a pagar BPJS | **Tertutup.** Tanpa BPJS Kes/TK (tetap & kontrak) dan dasar Kes < upah (13 jt→5,4 jt; 22 jt→11 jt) ditolak untuk `--ya`; hanya `--ya --ya-saya-paham` yang menyimpan dan tercatat di `log` (`konfirmasi_kepatuhan`: masalah, pesan, alasan, waktu); DB identik setelah penolakan; `hitung` mengingatkan tiap bulan (juga DB v1.0.0). SKILL.md Aturan wajib 7 menjawab kelima pola permintaan skenario 05. |
| P1-b setoran PPh 21 | **Tertutup.** PMK 168/2023 Ps. 21 ayat (1)–(3) dibaca ulang dari naskah JDIH Kemenkeu — sitasi sesuai. Hitung ulang Decimal independen 45 karyawan-bulan (Sep–Des, 11–12 karyawan, 2 Masa Pajak Terakhir karena keluar + Desember): 45/45 cocok; rekap Sep 4.018.864 − 931.100 = **3.087.764**, Des 3.186.783 − 590.436 = **2.596.347**; kasus lebih bayar setor 0 / lebih bayar **3.672.800** cocok hitung tangan; DB v1.0.0 → Des **2.604.402**. |
| P2 JP/JHT | **Tertutup.** JP tgl 15 tanpa geser (Min 15/11/2026, Sab 15/05/2027), JHT/JKK/JKM & PPh 21 ke Senin; tgl 15 hari kerja → satu baris; BPJS Kes tetap tgl 10. |
| P2 UMK prorata | Tertutup (catatan prorata). |

Temuan baru: **[SEDANG-RENDAH]** `isi --gaji-pokok-dibayar` pada bulan penuh (bukan masuk/keluar) menurunkan dasar BPJS tanpa pagar (hanya peringatan UMK); **[RENDAH]** pratinjau PERLU PERSETUJUAN KHUSUS masih diakhiri "Simpan? … + --ya"; baris JP tanpa geser menampilkan total seluruh iuran BPJS TK. P3 lama belum dikerjakan (diakui pembuat).
Tanpa regresi: 36 tes OK (1 dilewati), angka kunci Sep/Des v1.0.0 sama persis, `validate.py --skill gaji-umkm` ✅.

### Skor: **9/10**
Alasan: kedua P1 tertutup dengan pagar script + aturan SKILL.md yang bersumber; semua angka (termasuk Desember & lebih bayar) cocok dengan hitungan independen; tidak ada regresi. Dikurangi 1 untuk celah `gaji-pokok-dibayar` dan teks penutup pratinjau yang bertentangan (perbaikan kecil). Belum diuji: DTP (ayat (2)) dengan data, Coretax, platform asli.

## Uji ulang independen v1.0.2 (Akun B, 2026-09-26)
- **Penguji:** agent independen Akun B (bukan pembuat) · rincian: `examples/07-uji-ulang-v1.0.2-akun-b.md`
- **Lingkungan:** salinan skill di scratchpad, Linux, Python 3.11, data fiktif (11 karyawan baru); pembanding v1.0.1 dari `git archive 230da94`; simulasi agent `claude-code`.

| Temuan uji ulang v1.0.1 | Status v1.0.2 |
|---|---|
| [SEDANG-RENDAH] `isi --gaji-pokok-dibayar` menurunkan dasar BPJS di bulan penuh | **Tertutup.** `isi --gaji-pokok-dibayar`/`--tunjangan-tetap-dibayar` yang menurunkan gaji pokok + tunjangan tetap di bulan penuh (termasuk karyawan masuk tanggal 1) ditolak tanpa `--ya-saya-paham` (exit 1, `masalah_kepatuhan: dasar_bpjs_turun_bulan_penuh`, DB identik); `isi --file` pratinjau → `--ya` ditolak; dengan `--ya-saya-paham --alasan-khusus` tersimpan dan tercatat di `log`; `hitung` mengingatkan (juga pada DB celah lama). Prorata masuk 13/10 dan keluar 20/10 **tidak terhalang**; penukaran gaji pokok↔tunjangan tetap dengan jumlah sama tidak dipagari. |
| [RENDAH] teks penutup pratinjau | **Tertutup.** Pratinjau PERLU PERSETUJUAN KHUSUS kini ditutup "BELUM BISA DISIMPAN DENGAN --ya SAJA … + --ya --ya-saya-paham --alasan-khusus … Jangan menambahkan --ya-saya-paham atas inisiatif sendiri." |

Angka: verifikasi Decimal independen **21 karyawan-bulan** (Oktober 11 termasuk prorata masuk/keluar, Masa Pajak Terakhir dengan pengembalian 667.692, batas Kes/JP, lembur; November 10) — **21/21 cocok** PPh 21, gaji bersih, 8 komponen iuran, dan total setor (Okt: Kes 3.947.174, TK 7.565.852, PPh 3.831.025; Nov: 4.075.000 / 8.450.178 / 4.732.780). v1.0.1 dan v1.0.2 atas DB yang sama → `payroll` & `total` **identik**; angka kunci uji v1.0.0/v1.0.1 (Sep 3.087.764, Des 2.596.347, biaya 111.295.747 / 127.959.820) sama persis.
Temuan baru: **[RENDAH, desain]** `karyawan ubah --gaji-pokok` yang menurunkan gaji besar-besaran (15 jt → 5 jt) tanpa peringatan dasar BPJS (bisa sah; bergantung Aturan wajib 7). P3 lama (baris JP di `pengingat` menampilkan total BPJS TK) belum dikerjakan.
Tanpa regresi: 40 tes OK; `validate.py --skill gaji-umkm` ✅.

### Skor: **9/10**
Alasan: celah dan teks pratinjau tertutup dengan pagar yang tepat sasaran (bulan penuh saja, prorata tetap lancar) serta tercatat di log; angka BPJS & PPh 21 tidak berubah dan cocok dengan hitungan independen. Belum 10: DTP, Coretax, dan platform asli belum diuji; catatan kecil `karyawan ubah` dan P3.

## Riwayat revisi 1.0.10 (2026-10-05) — menunggu uji ulang independen; PERLU REVIEW konsultan pajak
- Pemicu: temuan penilai gelombang 7 di skill `pph21-ter` (uang diterima DTP ditulis gaji + DTP). Diperiksa terhadap teks PMK 105/2025 (Pasal 2 ayat 1, Pasal 5 ayat 1 & 5, Pasal 6 ayat 6, Lampiran B).
- Hasil: hitungan slip gaji-umkm (lewat `mesin/payroll.py`) **sudah benar**; `mesin/pph21.py` hanya dipakai untuk cek ulang setahun tanpa `--dtp`, jadi angka gaji-umkm tidak berubah. Contoh TK/0 gaji Rp 6.000.000, DTP: PPh dipotong = DTP tunai, setoran Rp 0, gaji bersih = Rp 6.000.000 − iuran BPJS karyawan.
- Perubahan: salinan mesin `payroll.py`/`pph21.py`/`thr.py` disinkronkan + sha256 `SUMBER.json`; catatan DTP di slip (`gaji.py`); `references/dasar-aturan.md`, `references/dtp-pmk105.md` (baru); tes `UjiDTP`. `tests/uji_regresi.py`: 42 tes OK.

## Uji ulang DTP PMK 105/2025 — 2026-10-05

Penguji independen (bukan pembuat; tidak mengubah kode/SKILL.md). Teks PMK 105/2025 dibaca langsung: Pasal 2 ayat 1 (PPh 21 **wajib dipotong**), Pasal 2 ayat 3 (Masa Pajak Januari–Desember 2026), Pasal 3 (industri alas kaki, tekstil & pakaian jadi, furnitur, kulit, pariwisata + KLU Lampiran A, 133 baris), Pasal 4 ayat 2–4 (pegawai tetap: bruto tetap & teratur Januari 2026/bulan pertama kerja **≤ Rp10.000.000**; tidak tetap: rata-rata ≤ Rp500.000/hari atau ≤ Rp10.000.000 bila bulanan), Pasal 5 ayat 1–2 (DTP **dibayar tunai**, bukan penghasilan kena pajak), Pasal 5 ayat 5 (kelebihan DTP tidak dikembalikan), Pasal 6 ayat 4–6 (lapor SPT Masa paling lambat 31 Januari 2027, lewat batas → PPh yang telah dipotong wajib disetor), Lampiran B (Tuan A 8.000.000 − 120.000 + 120.000 = 8.000.000; Tuan B K/1). Kesimpulan mekanisme: **dipotong = PPh TER/Pasal 17, DTP tunai = nilai sama, setoran ke negara Rp 0, diterima = bruto − potongan lain** (bukan bruto + DTP).

Metode: kalkulator independen Python `Decimal` milik penguji (tabel TER ditulis ulang, tidak mengimpor script skill), dicocokkan dulu dengan Lampiran B PMK 105/2025 (Tuan A Desember 540.000 / setahun 1.860.000; Tuan B Desember 480.000 / setahun 4.050.000 — cocok). Lalu CLI skill dijalankan (`--format json`/`--json`) dan dibandingkan per kolom: dipotong, DTP tunai, disetor ke negara, diterima.

Database uji sementara (scratchpad): `init` → `atur --jkk 0,24` → 6 karyawan (`karyawan tambah … --dtp --bruto-tetap-januari`) → `isi --thr` → `hitung --bulan 2026-03 --json`, lalu `rekap` dan `slip`.

| # | Karyawan | Dipotong | DTP tunai | Disetor | Gaji bersih | Selisih |
|---|---|---:|---:|---:|---:|---:|
| 1 | A TK/0 Rp6.000.000 DTP | 47.043 | 47.043 | 0 | 5.760.000 | 0 |
| 2 | B K/1 Rp9.500.000 DTP | 148.969 | 148.969 | 0 | 9.120.000 | 0 |
| 3 | C TK/0 tepat Rp10.000.000 DTP | 261.350 | 261.350 | 0 | 9.600.000 | 0 |
| 4 | D TK/0 Rp10.000.001 DTP → ditolak + peringatan | 261.350 | 0 | 261.350 | 9.338.651 | 0 |
| 5 | E TK/0 Rp6.000.000 tanpa DTP | 47.043 | 0 | 47.043 | 5.712.957 | 0 |
| 6 | F TK/0 Rp6.000.000 + THR Rp6.000.000 bulan sama, DTP | 490.896 | 490.896 | 0 | 11.760.000 | 0 |
| Σ | Total perusahaan | 1.256.651 | 948.258 | 308.393 | – | 0 (terutang/DTP/setor) |

Desember & THR memakai mesin yang sama (`mesin/payroll.py`, `mesin/thr.py`) — sudah diverifikasi di slip-gaji-bpjs (Desember DTP 249.777, selisih 0) dan hitung-thr.

SUMBER.json: sha256 kelima file mesin **cocok** dengan file sumber di repo (payroll.py & ter_core.py & ter_tabel.json slip-gaji-bpjs, pph21.py pph21-ter 1.0.5, thr.py hitung-thr 1.0.9; ter_core/ter_tabel di pph21-ter & hitung-thr juga identik).

Teks hitung/rekap: "Setor PPh 21: Rp 308.393" + "PPh 21 DTP dibayar tunai ke karyawan (sudah di gaji bersih): Rp 948.258"; slip: "PPh 21 Rp 47.043 tetap dipotong, lalu Rp 47.043 dibayar tunai kembali … Setoran … Rp 0".

Lain-lain: `tests/uji_regresi.py` 42 tes OK · `validate.py` ✅ · `uji_openclaw.sh` (instalasi uji terpisah) 117/117.

**Total selisih: 0 dari 6 karyawan + total.**

Cacat (ringan, tanpa dampak uang): kunci JSON `total.pph21_dipotong` (= 308.393) sebenarnya jumlah PPh yang **disetor**, bukan yang dipotong (yang dipotong menurut PMK = 1.256.651 = `pph21_terutang`); docstring `gaji.py` ±baris 1491 masih memakai istilah lama. Tidak tampil di teks pembeli, tetapi bisa menyesatkan agent yang membaca JSON. Sarankan ganti nama/penjelasan di versi berikut.

**Skor: 9/10. Verdik: LULUS uji ulang angka DTP** (tetap **PERLU REVIEW konsultan pajak**).

## Riwayat revisi 1.0.11 (2026-10-05) — menunggu cek penguji
- Menindaklanjuti cacat ringan uji ulang DTP: `total.pph21_dipotong` kini = total PPh 21 yang **dipotong** (Σ potongan "PPh 21", termasuk DTP; pada data uji di atas seharusnya 1.256.651), kunci baru `pph21_dtp` (= `pph21_dtp_tunai`) dan `pph21_disetor_ke_negara` (= `setor_pph21`, perkiraan setor = max(0, dipotong − DTP − kelebihan dikembalikan)). `lebih_bayar_pph21` = max(0, dikembalikan − (dipotong − DTP)). Angka setor tidak berubah.
- Kompatibilitas: `setor_pph21` dipertahankan; total tersimpan ≤ 1.0.10 (tanpa `pph21_dtp`) dikonversi otomatis di `lengkapi_total` (dipotong lama + DTP). Tidak ada skill/dasbor lain di repo yang membaca kunci ini (dicek dengan grep).
- Teks rekap DTP: "PPh 21 dipotong dari gaji bulan ini: … (termasuk DTP …)" + "Setor PPh 21 ke negara: …"; docstring `lengkapi_total` diperbarui; `references/perintah.md` diperbarui.
- Tes baru: `test_total_dtp_dipotong_vs_disetor_dipisah`, `test_total_lama_v1010_dtp_diubah_ke_arti_baru`; `tests/uji_regresi.py` 46 tes OK. Mesin (`scripts/mesin/`) tidak diubah; sha256 SUMBER.json tetap cocok.


## Cek v1.0.11 — 2026-10-05

Penguji independen (bukan pembuat; kode tidak diubah). Data fiktif 7 karyawan, periode **Desember 2026** (Masa Pajak Terakhir, Pasal 17 setahun), `saldo-awal` Jan–Nov, `atur --jkk 0,24 --batas-jp 11000000`; DB sementara di scratchpad. CLI `hitung`/`final`/`rekap --json` dijalankan; pembanding = kalkulator `Decimal` milik penguji (tidak mengimpor script skill: bruto = upah + BPJS Kes 4% + JKK + JKM, biaya jabatan 5% maks 6 jt, iuran JHT 2% + JP 1%, PKP dibulatkan ribuan ke bawah, tarif Pasal 17, dikurangi PPh Jan–Nov).

| Kode | Kasus | PPh Des (independen) | Dipotong | DTP tunai | Kembali | Diterima (indep. = skill) | Selisih |
|---|---|---:|---:|---:|---:|---:|---:|
| A | TK/0 6 jt, DTP | 248.650 | 248.650 | 248.650 | 0 | 5.760.000 | 0 |
| B | K/1 9,5 jt, DTP | 1.538.200 | 1.538.200 | 1.538.200 | 0 | 9.120.000 | 0 |
| C | TK/0 17 jt + bonus 5 jt (bruto > 10 jt), tanpa DTP | 6.676.650 | 6.676.650 | 0 | 0 | 14.753.350 | 0 |
| D | K/0 8 jt, tanpa DTP | 1.032.000 | 1.032.000 | 0 | 0 | 6.648.000 | 0 |
| E | TK/1 7 jt, DTP | 527.800 | 527.800 | 527.800 | 0 | 6.720.000 | 0 |
| F | TK/0 5 jt, lebih potong → dikembalikan | −2.410.250 | 0 | 0 | 2.410.250 | 7.210.250 | 0 |
| G | TK/0 10,5 jt minta DTP → ditolak (bruto Jan > 10 jt) | 629.400 | 629.400 | 0 | 0 | 9.450.600 | 0 |

Diterima = gaji − iuran karyawan − PPh dipotong + DTP tunai + kelebihan dikembalikan (PMK 105/2025: DTP tetap dipotong lalu dibayar tunai).

| Kunci `rekap --json` `total` | Independen | DB baru (1.0.11) | DB lama (dibuat 1.0.10, dibaca 1.0.11) | Cocok |
|---|---:|---:|---:|---|
| `pph21_dipotong` (= Σ PPh dipotong) | 10.652.700 | 10.652.700 | 10.652.700 | ✅ |
| `pph21_dtp` (= Σ DTP = `pph21_dtp_tunai`) | 2.314.650 | 2.314.650 | 2.314.650 | ✅ |
| `pengembalian_pph21` | 2.410.250 | 2.410.250 | 2.410.250 | ✅ |
| `pph21_disetor_ke_negara` = `setor_pph21` (dipotong − DTP − kembali) | 5.927.800 | 5.927.800 / 5.927.800 | 5.927.800 / 5.927.800 | ✅ |
| `lebih_bayar_pph21` | 0 | 0 | 0 | ✅ |

- Format lama: skill versi `3f2dded^` (1.0.10) diekstrak ke scratchpad, DB dibuat & difinalkan dengannya; total tersimpan berisi `pph21_dipotong` 8.338.050 (arti lama = Σ disetor), tanpa `pph21_dtp`. Dibaca 1.0.11 (`rekap --bulan` dan `rekap --tahun`) → dikonversi ke arti baru, angka sama persis dengan DB baru; `setor_pph21` tidak berubah dibanding output 1.0.10 (5.927.800).
- Teks rekap: "PPh 21 dipotong bulan ini 10.652.700 / Bagian DTP 2.314.650 / Kelebihan dikembalikan 2.410.250 / Perkiraan setor 5.927.800"; peringatan G (tidak memenuhi syarat DTP) tampil.
- `tests/uji_regresi.py`: **44 tes OK** (catatan revisi menyebut 46 — salah hitung; 2 tes baru memang ada) · `validate.py` ✅ 117 skill.
- Catatan ringan (tanpa dampak angka): bila ada DTP + pengembalian, teks rekap menyebut DTP dua kali (baris "Bagian PPh 21 DTP…" dan "PPh 21 DTP dibayar tunai…").

**Total selisih: 0 dari 7 karyawan + 5 kunci total (DB baru & lama).**

**Skor: 9/10. Verdik: LULUS** (tetap PERLU REVIEW konsultan pajak; pembulatan belum dicocokkan dengan Coretax).

## Uji ulang OpenClaw sebelum/sesudah v1.0.11 (2026-10-13, penguji independen)
- Skenario 02 (gaji September untuk 2 karyawan warung di Solo, data fiktif). OpenClaw 2026.10.2 lokal, model router Komunitech. **Kedua sisi dijalankan ulang** (2 sampel per sisi); SESUDAH hanya memuat `gaji-umkm` 1.0.11. Rincian ada di `examples/00-openclaw-sebelum-sesudah.md`.
- Skor: tanpa skill 7 / 7 → dengan skill 9 / 9 (rata-rata 7 → 9, **selisih 2,0**). **Verdik: LULUS** (acuan: sesudah ≥ 8 dan selisih ≥ 1,5). Skor SEBELUM 8 pada uji 2026-10-01 tidak terulang.
- Angka di kedua sisi benar: transfer 3.164.150 / 2.544.000, setor BPJS 818.800 (Kesehatan 287.500 + Ketenagakerjaan 531.300), PPh 21 = 0. Keluaran mesin skill cocok 100% dengan hitungan `Decimal` independen di setiap kolom (bruto pajak 3.428.890 / 2.770.310, biaya perusahaan 6.526.950).
- Pembeda: dengan skill ada dasar aturan + disclaimer, setoran dipisah per lembaga, asumsi bernomor, dan tidak ada klaim UMK. Tanpa skill tidak ada dasar aturan maupun disclaimer, dan 1 dari 2 sampel mengklaim "di atas UMK Solo, aman" tanpa angka.
- Sisa kecil SESUDAH: CSV sementara dan slip ditulis di folder kerja tanpa menyebut lokasinya; tenggat setor (tgl 10/15) belum disebut di balasan pertama.

## Revisi v1.0.13 (2026-10-17, uji pembuat — perlu penguji independen + uji ulang bot Telegram)
- Pemicu: gelombang Telegram 21 (16 Okt 2026), skor dengan skill 4 — 12 karyawan, Lina resign 14 Sep (Masa Pajak Terakhir) tanpa data Jan–Agu, Kiki masuk 15 Sep tanpa nominal prorata → seluruh hitungan ditahan.
- Perbaikan: karyawan dengan data kurang ditandai **tertunda** (yang lain tetap dihitung), pilihan (a) data Jan–Agu / (b) `--pph-sementara` (TER, label SEMENTARA, `final` ditolak sampai lengkap), rumus prorata hari kalender + `--prorata kalender|penuh`, perintah `hitung-cepat` tanpa database untuk balasan pertama, teks pemilik tanpa nama perintah. Rincian & keluaran nyata: `08-uji-v1.0.13-resign-tanpa-data-tertunda.md`.
- Angka skenario G21 (11 karyawan lengkap): transfer Rp 65.412.866; setor BPJS Kesehatan Rp 3.265.000, BPJS Ketenagakerjaan Rp 5.581.620, PPh 21 Rp 522.059 — cocok dengan hitung ulang Decimal independen dan acuan penilai G21 (12 orang Kes 3.815.000 / TK 6.631.020 dikurangi Lina). Setelah data Lina (fiktif, iuran Jan–Agu 2.630.948 sesuai batas JP Jan–Feb 10.547.400) diisi: 12 orang, Kes 3.815.000, TK 6.631.020, PPh dipotong 522.059 − dikembalikan 1.337.572 → setor Rp 0 (lebih bayar 815.513).
- Perbaikan temuan pemeriksa independen (17-10-2026): pagar BPJS di `hitung-cepat`, saran "hitung & kunci" untuk bulan terlewat, teks pemilik ringkas & awam (klaim panjang putaran ini terlalu luas — lihat putaran 3), `bisa_final: false` di `hitung-cepat`, tanpa tanya prorata bila nominal sudah diisi. Replay penuh examples 01–03 (63 langkah) dibanding 1.0.12: semua angka identik; beda hanya 2 langkah yang kini memberi hasil + "tertunda" alih-alih galat.
- `tests/uji_regresi.py`: **58 tes OK** (13 tes baru `UjiV1013` + `UjiV1013Pemeriksa`; 2 tes lama disesuaikan dengan pesan baru) · `validate.py` ✅.
- **Putaran 3 (pemeriksa ulang, 17-10-2026):** lensa angka LOLOS (semua angka G21 cocok s.d. Rp1); lensa perilaku PERLU_PERBAIKAN → diperbaiki pembuat: (1) teks pemilik > 4.096 karakter pada varian 12 karyawan (CSV minimal + saldo/prorata 4.109–4.432; pagar + persetujuan 4.095–4.344) → kini 25 varian yang diuji **3.053–3.702** karakter (maks. 3.702 = CSV minimal + JKK 0,40), plus pengaman `teks_bagian` (≤ 3.800 per bagian) untuk teks yang tetap panjang (45 karyawan; kombinasi ekstrem UMK Rp 7 jt → 3.983–4.073, dibagi 2 pesan); (2) klaim palsu "Tarif JKK belum diisi: dipakai 0,24%" padahal tarif per baris dipakai → diganti tarif yang benar (hitung-cepat & database, mesin tidak diubah); (3) kolom komponen asing kini disebut + alias `gaji_pokok_dibayar`; (4) catatan iuran prorata akurat (BPJS Kesehatan minimal UMK) & peringatan UMK membandingkan gaji penuh; (5) bulan terlewat setelah saldo awal → dua pilihan; (6) prorata satu komponen konsisten; (7) disclaimer tanpa ID skill; Desember + pagar ditanya sekali. Angka 31 varian sebelum/sesudah: 0 selisih. **66 tes OK** (8 tes baru `UjiV1013Putaran3`). Uji pembuat — perlu cek penguji independen.
- **Putaran 4 (17-10-2026):** pemeriksa ulang putaran 3 — lensa angka LOLOS (27 varian hitung-cepat + 45 karyawan + 17 langkah database, 0 selisih), lensa perilaku PERLU_PERBAIKAN (1 sedang). Diperbaiki pembuat: (1) regresi `isi --file` + kolom tak dikenal → tidak lagi "perlu persetujuan khusus" (`--ya` biasa menyimpan; catatan awam terpisah); (2) klaim panjang teks dikoreksi: dari 75 varian pemeriksa, 47 muat satu pesan (≤ 3.781), 23 dibagi 2–3 pesan antara lain (CSV minimal + pagar/persetujuan, banyak masuk/keluar, UMK sangat tinggi, ≥ 20 karyawan) — juga file lengkap + pagar/persetujuan + saldo + prorata, 5 galat semua-tertunda; (3) pemotong teks: judul tidak sendirian, pesan terakhir tidak hanya penutup; (4) SKILL.md: kirim `teks`/`teks_bagian` apa adanya, pertanyaan tambahan hanya yang belum ada, pesan terpisah; (5) teks pratinjau perintah besar tanpa instruksi agent (pindah ke `langkah_berikut`); (6) asumsi JKK hitung-cepat sama dengan alur database. **69 tes OK**; angka 31 varian sebelum/sesudah 0 selisih.
- Belum: uji penguji independen, uji ulang sisi DENGAN & TANPA di bot Telegram. Skor belum diberikan.
