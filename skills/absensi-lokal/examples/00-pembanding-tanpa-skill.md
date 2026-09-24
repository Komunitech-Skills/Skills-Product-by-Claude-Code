# 00 — Uji A/B: skenario 01 tanpa skill vs dengan skill

**Permintaan sama** dengan contoh 01 (toko 6 karyawan pola 6 hari, `log-agustus.csv` 304 baris, lembur disetujui Andi 5/8 2 jam, Joko Minggu 9/8 8 jam, Sari Sabtu 15/8 1,5 jam, Rudi 17/8 5 jam; Rudi punya tunjangan tidak tetap Rp 1,5 jt).

**Cara uji "tanpa skill":** penguji berperan sebagai agent umum yang tidak memuat skill apa pun: membaca CSV, menulis skrip Python sekali pakai (`/tmp/uji-absensi-lokal/a/generik.py`), lalu menjawab. Pengetahuan PP 35/2021 dari ingatan umum (tangga pengali hari kerja & libur pola 6 hari diingat benar).

## Berdampingan

| Aspek | Tanpa skill (agent umum) | Dengan skill `absensi-lokal` |
|---|---|---|
| Hadir | Andi 25, Sari 25, Budi 25, Dewi 23, **Joko 26, Rudi 26** (hari Minggu/17 Agustus ikut dihitung "hadir") | 25 dari 25 hari kerja + "masuk di hari libur 1" dipisah |
| Terlambat (toleransi 5 mnt) | Andi 3x/19 mnt, Budi 6x/97 mnt, Rudi 3x/19 mnt … (detik ikut, 5 mnt 30 dtk dihitung telat; hari Minggu/libur ikut dicek) | Andi 2x/12 mnt, Budi 5x/1 jam 29 mnt, Rudi 2x/12 mnt (menit penuh, hanya hari kerja terjadwal) |
| Jam kerja | Sabtu ikut dipotong istirahat 1 jam (Andi 164,5 jam) | Sabtu hari pendek tanpa potongan (Andi 169 jam 17 mnt) |
| Lupa tap pulang Sari 12/08 | Diam-diam dianggap hadir, jam hari itu hilang | Muncul di **PERLU DICEK**, ditanyakan; setelah dijawab dicatat & jam dihitung |
| Dewi tidak absen 20–21/08 | Hanya "hadir 23" tanpa penjelasan | Daftar "tanpa keterangan" + pertanyaan izin/sakit/cuti/alpa |
| Tap ganda / tap istirahat / ID asing | Tap ganda tak berpengaruh (min/max), tap istirahat hilang tanpa laporan, ID 9 dibuang tanpa kabar | Dilaporkan di pratinjau (2 tap istirahat diabaikan, 1 ID tak dikenal) |
| Lembur Andi / Sari / Joko | Rp 76.879 / 53.468 / 343.931 (benar) | Rp 76.879 / 53.468 / 343.931 |
| Lembur Rudi (tunjangan tidak tetap) | **Rp 190.751** (dasar pokok + tetap Rp 3,3 jt; aturan 75% Pasal 32 ayat (4) terlewat) | **Rp 208.092** (dasar 75% × Rp 4,8 jt = Rp 3,6 jt) |
| Total lembur | Rp 665.029 (**kurang bayar Rp 17.341**) | Rp 682.370 |
| Lembur tanpa perintah (Joko 25/08 pulang 19.10) | Tidak dihitung (karena tidak ada di daftar) | Tidak dihitung, dasar Pasal 28 dijelaskan |
| Data tersimpan untuk bulan depan | Tidak — skrip sekali pakai, ulangi dari nol tiap bulan | Database lokal, impor ulang tidak dobel, backup otomatis |
| Konfirmasi sebelum mengubah data | Tidak relevan | Selalu pratinjau → "ya" |
| File untuk slip gaji / Excel | Tidak ada | `rekap.csv`, `rincian.csv`, CSV untuk `slip-gaji-bpjs` |
| Dasar hukum & disclaimer | Tidak ada | Pasal per jenis lembur + disclaimer |

## Penilaian
Dengan skill **jelas lebih baik**: angka lebih benar (aturan 75% dan hari pendek Sabtu), data ganjil tidak hilang diam-diam, hasil konsisten dan tersimpan untuk bulan berikutnya, dan ada jejak persetujuan lembur. Agent umum yang kuat bisa mendekati angka lembur dasar, tetapi hanya sekali pakai dan melewatkan kasus yang justru sering terjadi di UMKM (tunjangan tidak tetap, lupa tap, libur/Minggu dihitung hadir). Bahan "sebelum/sesudah" untuk README: kurang bayar lembur Rp 17.341 untuk satu sopir dalam sebulan, dan dua hari kerja yang "hilang" tanpa tanda.
