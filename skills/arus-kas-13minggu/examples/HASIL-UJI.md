# HASIL UJI — arus-kas-13minggu

- **Tanggal:** 2026-09-23
- **Penguji:** agent penguji independen (simulasi, Claude Code)
- **Lingkungan:** Python 3 lokal. Script dijalankan sungguhan di `/tmp/uji-arus-kas-13minggu/`. Verifikasi dengan script terpisah (`verif/verif.py`, `verif/banding.py`) yang menempatkan pos per **tanggal kalender**, bukan dengan algoritma script.
- **Skenario:** 01–05 + uji A/B (`00-pembanding-tanpa-skill.md`) + banding pesaing (`00-banding-pesaing.md`)

## Audit keamanan
- `scripts/proyeksi_kas.py`: hanya library standar. Tidak ada jaringan, `subprocess`, `eval`/`exec`, atau penghapusan file. Hanya membaca CSV yang diberikan dan menulis `--output-csv`.
- SKILL.md, README, `references/opsi-tindakan.md`, dan template bersih dari prompt injection. Ada pengaman yang baik: larangan menyarankan pinjol ilegal, menunda pajak, dan menunda gaji tanpa persetujuan. **Aman.**

## Verifikasi angka (independen)
| Uji | Hasil |
|---|---|
| Contoh di SKILL.md (20 jt, gaji tgl 25, …) | Cocok: minggu 8 = Rp 0, batas Rp 14.326.923, opsi 14.000.000 / 4.750.000 / 18.750.000 |
| S1 + 6 varian opsi | 13/13 minggu cocok (masuk, keluar, saldo, status) + batas aman |
| S2 Februari 2027: `tgl:31`, `tgl:30` → 28 Feb; `setiap 2 mulai 3` → 3,5,7,9,11,13; sewa 1 Jan (sebelum mulai) tidak dihitung; sewa 1 Apr di minggu 13 | Cocok 13/13 |
| Tahun kabisat 2028: `tgl:29/30/31` → 29 Feb | Benar |
| S3 + 5 varian | Cocok 13/13 |
| Data rusak/tepi: `Rp 1.500.000`, `1.500.000,50` (→ 1.500.001, setengah ke atas), `1.500.000,49`, `0`, `15jt`, `2,5 juta`, saldo `-5 juta`, `"2,6,10"`, `1-3`, pemisah `,`/`;`/tab, `abc`, `minggu 6`, nominal negatif, minggu 20, `tgl:32`, `tgl:` tanpa `--mulai`, file kosong, hanya header, kolom hilang, file tidak ada, tanggal mustahil | Semua ditangani: dihitung benar, atau dilewati/ditolak dengan pesan jelas (kode keluar 2 + JSON) |

**Kesimpulan akurasi:** angka saldo dan penempatan tanggal **100% benar** pada semua uji. Kelemahannya ada pada logika *simulasi opsi* (lihat cacat sedang), bukan pada aritmetika.

## Skor

| Kriteria | Skor (1–10) | Alasan singkat |
|---|---|---|
| Pemicu (description) | 9 | Frasa awam ("uang saya cukup sampai kapan", runway, 13-week) dan batas dengan laba rugi/rekap jelas |
| Kemudahan awam | 8 | Cukup bercerita; tabel 🟢🟡🔴 dan CSV Excel Indonesia. Istilah "batas aman" dijelaskan. |
| Kualitas output | 8 | Titik kritis + penyebab + opsi berangka. Namun agent harus menyaring sendiri simulasi yang menyesatkan. |
| Akurasi (angka/fakta) | 8 | Aritmetika dan tanggal sempurna. Tebakan "kritis" salah untuk cicilan/pajak/gaji+bonus. |
| Penanganan input kurang | 8 | Tanya sekali, 5 pertanyaan. Opsi >13 minggu tidak didokumentasikan. |
| Penanganan di luar cakupan | 9 | Rujukan skill tepat |
| Keamanan | 10 | Bersih, lokal, dengan pengaman nasihat |

## SKOR AKHIR: **7 / 10** — LULUS (dengan revisi yang disarankan sebelum rilis)

Uji A/B: skill **jelas lebih baik**. Tanpa skill, jawabannya bulanan dan menyimpulkan "aman", melewatkan minggu kritis Rp 6.300.000. Banding pesaing: skill kita unggul terhadap `cash-flow-forecaster` (OneWave, MIT), `cash-flow-forecast` (mohitagw15856, MIT), dan `cash-flow-snapshot` (Anthropic, Apache-2.0) untuk pembeli UMKM Indonesia. Keunggulannya ada pada konteks lokal, script deterministik, dan CSV siap pakai. Tidak ada cacat berat. Skor ditahan di 7 karena fokus uji ini adalah **kejujuran simulasi**, dan di sana ada dua cacat sedang yang bisa membuat pembeli awam salah paham bila agent hanya menyalin output script.

## Daftar cacat & saran perbaikan

### Berat
- Tidak ada.

### Sedang
1. **Tebakan "kritis" terbalik untuk pos wajib** (`scripts/proyeksi_kas.py` baris 230–243, `tebak_kritis`). `KATA_NONKRITIS` dicek **sebelum** `KATA_KRITIS`, sehingga "Cicilan mesin jahit", "Pajak kendaraan (STNK)", "Angsuran leasing kendaraan", "Gaji dan bonus", dan "Bonus akhir tahun karyawan" dianggap tidak kritis. Pos-pos itu lalu ikut digeser di simulasi "Tunda belanja non-kritis" (terbukti di uji tepi dan S1). Ini bertentangan dengan `references/opsi-tindakan.md` ("cicilan bank dan pajak sebaiknya tetap diperlakukan kritis", "dilarang menunda gaji tanpa persetujuan"). **Saran:** cek `KATA_KRITIS` (gaji, upah, cicilan, angsuran, pajak, sewa, bpjs, thr, bonus karyawan) lebih dulu. Keluarkan "bonus" dari `KATA_NONKRITIS` (baris 122–124). Tambahkan ke `peringatan` daftar pos yang ditebak tidak kritis agar agent mengonfirmasi ke pengguna.
2. **Simulasi yang hanya mendorong kewajiban ke luar horizon tampak menyelesaikan masalah** (baris 419–449). Contoh di S3: "Gabungan" melaporkan "minggu negatif: tidak ada, saldo terendah Rp 5.000.000", padahal Rp 16.500.000 kewajiban jatuh setelah minggu 13 sehingga saldo riilnya −Rp 9.500.000. Peringatan teks memang ada, tetapi angka utama menyesatkan. **Saran:** tambahkan ke setiap opsi `saldo_setelah_kewajiban_tertunda = saldo_akhir_minggu_n − jatuh_setelah_horizon`. Bila nilainya < 0 (atau < batas), beri label `"hanya_menunda": true` dan catatan "tidak menyelesaikan masalah". Di SKILL.md langkah 5 dan checklist: "opsi berlabel hanya_menunda tidak boleh ditulis sebagai solusi". Perbaiki juga contoh SKILL.md baris 119 ("Gabungan ketiganya → Rp 18.750.000") agar menyebut Rp 14.000.000 yang pindah ke setelah minggu 13.
3. **Masalah struktural tidak disampaikan.** Bila `ringkasan.arus_kas_bersih` < 0 (S1: −Rp 14.600.000, S3: −Rp 17.500.000), SKILL.md tidak meminta agent menyebutnya, sehingga opsi "geser jadwal" terkesan cukup. **Saran:** tambahkan ke "Format output → Kesimpulan" butir wajib "Arus kas 13 minggu: masuk Rp … vs keluar Rp … (turun/naik Rp …). Bila turun: masalah rutin, bukan hanya jadwal", dan satu butir checklist.

### Ringan
1. `--jumlah-minggu` (4–26) tidak disebut di SKILL.md (langkah 2), padahal pertanyaan "sampai Lebaran/akhir tahun" umum (S4). Tambahkan satu baris.
2. Pos rutin `tgl:N` yang jatuh **tepat setelah** minggu terakhir (S1: gaji 28 Des) tidak diberi tahu. Saran: script menambahkan `peringatan` "pos bulanan berikutnya jatuh 1–7 hari setelah horizon: …".
3. SKILL.md tidak meminta agent menjelaskan penempatan tanggal (bulan pendek, pos sebelum minggu 1, pos bulan berikutnya di minggu 13). Tambahkan ke checklist: "sebutkan penempatan tgl:29–31 di bulan pendek".
4. Format `minggu` versi awam ("minggu 6", "minggu ke-6", "setiap 2 minggu mulai minggu 3") ditolak (baris dilewati). Saran: regex menerima awalan "minggu (ke-)?".
5. "Pos belum jelas kritis" hanya berupa peringatan. Pos "Belanja stok" tetap digeser di simulasi supplier walau `kritis` kosong. Ini wajar, tetapi sebaiknya dijelaskan di SKILL.md.
6. Tidak ada panduan THR (H-7, 1 bulan gaji) di `references/opsi-tindakan.md` walau THR disebut di README.
7. README merujuk `CARA-INSTAL.md` dan SKILL/ATTRIBUTION merujuk `LISENSI.txt`, tetapi keduanya tidak ada di folder skill (mungkin dibuat di tahap paket). Pastikan ikut di bundel.

## Ide dari pesaing (bukan salinan)
Pisahkan pemasukan pasti vs perkiraan (saldo "hanya yang pasti"), tempatkan piutang sesuai kebiasaan telat bayar pelanggan, buat panduan "forecast vs aktual" mingguan, dan sediakan skenario pesimis otomatis (−20% penjualan) di script.
