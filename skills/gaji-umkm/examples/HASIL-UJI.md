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
