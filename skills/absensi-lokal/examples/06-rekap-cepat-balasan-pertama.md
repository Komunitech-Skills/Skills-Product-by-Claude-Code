# 06 — File mesin + permintaan rekap: hasilnya langsung di balasan pertama

**Skenario:** normal. Pemilik toko mengirim file ekspor mesin fingerprint bulan September dan minta rekap telat & bolong. Buku absensi belum pernah dibuat. Di bagian bawah ada dua varian: toko dengan Sabtu pulang lebih awal (pola 6 hari), dan pelanggan lama yang bulan berikutnya mengirim file baru.

**Yang diuji:** balasan PERTAMA sudah berisi rekap (bukan daftar pertanyaan), semua yang disebut pengguna dipakai sebagai pengaturan (bukan ditulis "anggapan saya"), pertanyaan penutup paling banyak 3, tidak ada alamat file, nama database, nama script, perintah, atau kode karyawan di dalam balasan, dan pelanggan lama tidak ditanya ulang soal pengaturan yang sudah tersimpan.

**Asal contoh (jujur):** keluaran di bawah adalah hasil menjalankan `rekap-cepat` (skill versi 1.0.11) pada data **fiktif** buatan pembuat skill; data September dibangkitkan oleh `tests/uji_regresi.py` (kelas `UjiRekapCepat`, 121 baris log, 3 karyawan, 1–30 September 2026). Ini bukan uji di bot OpenClaw/Telegram; bagian "Balasan agent" memperlihatkan bentuk balasan yang diminta SKILL.md, dengan isi rekap dari keluaran script.

## Data fiktif (pola yang disengaja)
- Andi (ID 1), Sari (ID 2), Joko (ID 3); Senin–Jumat, masuk 07.55 dan pulang 17.05 setiap hari kerja, kecuali yang disebut di bawah.
- Telat (batas 08.10 karena kelonggaran 10 menit): Andi 02/09 08.23, 15/09 08.12, 22/09 08.31; Joko 03/09 08.14, 10/09 08.16, 24/09 08.45; Joko 17/09 08.08 (tidak dihitung).
- 14/09 kosong untuk ketiganya; Sari kosong 21–22/09; Andi 25/09 tanpa jam pulang.

## Pesan pengguna (persis)

> Kak ini file dari mesin fingerprint toko aku bulan September (absen-sept.csv). Karyawan 3 orang: Andi (ID 1), Sari (ID 2), Joko (ID 3), semua kerja Senin–Jumat jam 08.00–17.00, istirahat 1 jam. Telat lebih dari 10 menit baru dihitung. Tolong rekap September: siapa aja yang telat & berapa kali, terus ada yang bolong gak absennya?

## Langkah agent (tidak ditampilkan ke pengguna)
Tanpa `info`, tanpa `init`, tanpa bertanya. Semua yang disebut pengguna (nama dan ID, Senin–Jumat, jam kerja, istirahat, kelonggaran 10 menit) dimasukkan sebagai opsi:
`rekap-cepat absen-sept.csv --daftar "Andi=1; Sari=2; Joko=3" --hari-kerja 5 --masuk 08.00 --pulang 17.00 --istirahat 60 --toleransi 10 --json` → tidak ada file atau database yang dibuat.

## Balasan agent (balasan pertama, sebelum pengguna menjawab apa pun)

> Sudah saya rekap dari file Anda.
>
> REKAP ABSENSI SEPTEMBER 2026
> Periode 01/09/2026-30/09/2026 | kelonggaran telat 10 menit
>
> 1. Andi
>    Hadir 21 dari 22 hari kerja | Tanpa keterangan 1
>    Terlambat 3x (1 jam 6 menit) | Pulang cepat 0x (0 menit)
>    Tanggal telat: 02/09, 15/09, 22/09
>    Jam kerja 161 jam 59 menit (+1 hari data tidak lengkap, belum dihitung)
>
> 2. Sari
>    Hadir 19 dari 22 hari kerja | Tanpa keterangan 3
>    Terlambat 0x (0 menit) | Pulang cepat 0x (0 menit)
>    Jam kerja 155 jam 10 menit
>
> 3. Joko
>    Hadir 21 dari 22 hari kerja | Tanpa keterangan 1
>    Terlambat 3x (1 jam 15 menit) | Pulang cepat 0x (0 menit)
>    Tanggal telat: 03/09, 10/09, 24/09
>    Jam kerja 169 jam 47 menit
>
> PERLU DICEK (1):
> - Andi 25/09/2026: hanya ada jam masuk (07.55); jam pulang tidak tercatat
>
> Hari kerja tanpa absen & tanpa keterangan (mohon dikonfirmasi: izin/sakit/cuti/alpa?):
> - Andi: 14/09
> - Sari: 14/09, 21/09, 22/09
> - Joko: 14/09
>
> Yang saya pakai untuk menghitung:
> - Jam kerja 08.00-17.00, istirahat 60 menit
> - 5 hari kerja seminggu, libur mingguan Sabtu dan Minggu
> - Kelonggaran telat 10 menit
> - Tidak ada tanggal merah atau libur khusus (anggapan saya, bisa diubah)
>
> Kosong untuk semua karyawan: Senin 14/09. Kemungkinan libur/tutup, atau file belum mencakup tanggal itu. Kalau memang libur, tanggal itu tidak dihitung sebagai bolong.
>
> Ini hitungan sementara dari file yang dikirim; belum ada data yang disimpan.
>
> 1) Tanggal Senin 14/09 kosong untuk semua karyawan. Apakah itu libur atau toko tutup?
> 2) Hari tanpa catatan absen: Sari 21/09, 22/09. Itu izin, sakit, cuti, atau alpa?
> 3) Mau saya simpan 121 catatan absen ini supaya bulan depan tinggal tambah file baru? Cukup balas "ya" bila mau; pertanyaan lain boleh dijawab nanti.

(Hanya "tidak ada tanggal merah" yang tertulis sebagai anggapan, karena pengguna memang tidak menyebut libur. Daftar karyawan diberikan pengguna, jadi baris "Daftar karyawan dibaca dari isi file" tidak muncul; bila pengguna tidak menyebut nama dan ID, script membacanya dari isi file dan mencatatnya sebagai anggapan.)

## Jawaban pengguna dan balasan kedua

> 14 itu toko tutup. Sari 21-22 izin. Iya simpan.

Agent menjalankan ulang `rekap-cepat ... --libur 2026-09-14` (hasilnya di bawah). Karena pengguna sudah menulis "Iya simpan" di pesan yang sama, agent **langsung menyimpan** (saat "ya" atas tawaran simpan): satu "ya" atas tawaran "simpan 121 catatan absen" adalah persetujuannya. Agent tidak mengirim ringkasan baru, tidak bertanya "Betul?", dan tidak menunggu "ya" kedua. Urutan kerjanya (tidak ditampilkan): jadwal, kelonggaran telat 10 menit, ketiga karyawan, 14/09 sebagai hari tutup, file dimasukkan, Sari izin 21-22/09. Balasan akhir satu kalimat jumlah ditambah satu kalimat kedua untuk libur/izin, tanpa lokasi file atau perintah, tanpa rekap ulang:

> 121 catatan sudah tersimpan: Andi 41, Sari 38, Joko 42. Tanggal 14/09 dicatat tutup dan Sari izin 21-22/09.

(Rekap ulang baru dikirim bila pengguna memintanya; bila diminta, Sari: Izin 2, tanpa keterangan 0.) Bila pengguna hanya membalas "ya" pada balasan pertama tanpa jawaban lain, hasilnya sama: simpan sekarang, hari kosong tetap "tanpa keterangan", pertanyaan samping yang belum dijawab dibiarkan.

Hasil `--libur 2026-09-14` (HANYA UNTUK AGENT, TIDAK DIKIRIM ke pengguna; ini rekap yang dihitung sebelum menyimpan, dan pertanyaan penutup di dalamnya tidak boleh ditanyakan lagi):

> Sudah saya rekap dari file Anda.
>
> REKAP ABSENSI SEPTEMBER 2026
> Periode 01/09/2026-30/09/2026 | kelonggaran telat 10 menit
> Libur/tutup: 14/09/2026
>
> 1. Andi
>    Hadir 21 dari 21 hari kerja
>    Terlambat 3x (1 jam 6 menit) | Pulang cepat 0x (0 menit)
>    Tanggal telat: 02/09, 15/09, 22/09
>    Jam kerja 161 jam 59 menit (+1 hari data tidak lengkap, belum dihitung)
>
> 2. Sari
>    Hadir 19 dari 21 hari kerja | Tanpa keterangan 2
>    Terlambat 0x (0 menit) | Pulang cepat 0x (0 menit)
>    Jam kerja 155 jam 10 menit
>
> 3. Joko
>    Hadir 21 dari 21 hari kerja
>    Terlambat 3x (1 jam 15 menit) | Pulang cepat 0x (0 menit)
>    Tanggal telat: 03/09, 10/09, 24/09
>    Jam kerja 169 jam 47 menit
>
> PERLU DICEK (1):
> - Andi 25/09/2026: hanya ada jam masuk (07.55); jam pulang tidak tercatat
>
> Hari kerja tanpa absen & tanpa keterangan (mohon dikonfirmasi: izin/sakit/cuti/alpa?):
> - Sari: 21/09, 22/09
>
> Yang saya pakai untuk menghitung:
> - Jam kerja 08.00-17.00, istirahat 60 menit
> - 5 hari kerja seminggu, libur mingguan Sabtu dan Minggu
> - Kelonggaran telat 10 menit
> - Libur/tutup: 14/09
>
> Ini hitungan sementara dari file yang dikirim; belum ada data yang disimpan.
>
> 1) Hari tanpa catatan absen: Sari 21/09, 22/09. Itu izin, sakit, cuti, atau alpa?
> 2) Andi 25/09 hanya ada jam masuk (07.55). Jam pulangnya berapa?
> 3) Mau saya simpan 121 catatan absen ini supaya bulan depan tinggal tambah file baru? Cukup balas "ya" bila mau; pertanyaan lain boleh dijawab nanti.

## Varian A — toko 6 hari, Sabtu pulang 13.00

Pesan pengguna: "Ini file absen Agustus. Senin–Sabtu jam 8–4, Sabtu sampai jam 1, istirahat sejam. 17 Agustus libur. Rekap telat & bolong." (4 karyawan fiktif; `AC-No.` 1–4; semua masuk 07.55, pulang 16.05, Sabtu 13.02.)

- **Dengan** `--hari-kerja 6 --masuk 08.00 --pulang 16.00 --istirahat 60 --libur 2026-08-17 --pulang-hari-pendek 13.00`: Andi "Pulang cepat 0x (0 menit)", "Jam kerja 168 jam 55 menit"; baris pengaturan "Sabtu pulang jam 13.00, tanpa potongan istirahat" (bukan anggapan). Hasilnya sama dengan jalur buku absensi tersimpan (dicek di `tests/uji_regresi.py`, `test_11`).
- **Tanpa** `--pulang-hari-pendek` (kesalahan yang dicegah SKILL.md): Andi "Pulang cepat 5x (14 jam 50 menit)", "Jam kerja 163 jam 55 menit". Script menandai "Sabtu dihitung hari kerja biasa, jam pulang sama dengan hari lain (anggapan saya, bisa diubah)" dan membuka pertanyaan penutup dengan: "Hari Sabtu banyak yang pulang lebih awal dari jam 16.00. Apakah Sabtu memang pulang lebih awal, dan jam berapa?"

## Varian B — pelanggan lama, bulan berikutnya

Buku absensi sudah ada dari alur simpan di atas (kelonggaran telat 10 menit, 14/09 tutup, Sari izin 21–22/09). Pada bulan berikutnya pengguna cukup mengirim file baru: "Ini file absen Oktober, tolong direkap." Agent tetap menjalankan `rekap-cepat absen-okt.csv --json` tanpa opsi dan tanpa `info`; script memakai pengaturan yang tersimpan sehingga tidak ada nilai bawaan yang menimpa (bila buku yang sudah ada diabaikan, rekap memakai "tanpa kelonggaran" dan izin Sari terhitung bolong: Joko 4x/83 menit, bukan 3x/75 menit; dicegah oleh `test_13` di `tests/uji_regresi.py`). File Oktober fiktif (dibangkitkan oleh `buat_csv_okt` di `tests/uji_regresi.py`: 22 hari kerja sungguhan, Andi telat 08.41 sekali, Joko 08.14 dan 08.07, Sari kosong 12-13/10, 128 catatan dari tiga karyawan) memuat satu orang yang belum terdaftar (ID 9 "Tamu"). Keluaran di bawah disalin dari teks siap kirim hasil menjalankan `test_14a`:

> Sudah saya rekap dari file Anda, dengan pengaturan yang sudah tersimpan di buku absensi.
>
> REKAP ABSENSI OKTOBER 2026
> Periode 01/10/2026-31/10/2026 | kelonggaran telat 10 menit
>
> 1. Andi
>    Hadir 22 dari 22 hari kerja
>    Terlambat 1x (41 menit) | Pulang cepat 0x (0 menit)
>    Jam kerja 178 jam 54 menit
>
> 2. Sari
>    Hadir 20 dari 22 hari kerja | Tanpa keterangan 2
>    Terlambat 0x (0 menit) | Pulang cepat 0x (0 menit)
>    Jam kerja 163 jam 20 menit
>
> 3. Joko
>    Hadir 22 dari 22 hari kerja
>    Terlambat 1x (14 menit) | Pulang cepat 0x (0 menit)
>    Jam kerja 179 jam 9 menit
>
> Hari kerja tanpa absen & tanpa keterangan (mohon dikonfirmasi: izin/sakit/cuti/alpa?):
> - Sari: 12/10, 13/10
>
> Yang saya pakai untuk menghitung:
> - Jadwal kerja yang sudah tersimpan: 08.00-17.00, istirahat 60 menit, 5 hari kerja seminggu
> - Kelonggaran telat 10 menit (dari buku absensi)
> - Tidak ada tanggal merah atau libur khusus yang tersimpan untuk periode ini (anggapan saya, bisa diubah)
> - Daftar karyawan dari buku absensi Anda (3 orang)
>
> Catatan dari file:
> - 1 baris dari orang yang tidak ada di buku absensi tidak dihitung: Tamu (ID 9).
>
> Ini hitungan dari file yang dikirim dengan pengaturan yang sudah tersimpan; file ini belum dimasukkan ke buku absensi Anda.
>
> 1) Ada catatan dari Tamu (ID 9) yang tidak ada di buku absensi. Kalau itu karyawan baru, sebutkan nama dan nomor ID-nya di mesin.
> 2) Hari tanpa catatan absen: Sari 12/10, 13/10. Itu izin, sakit, cuti, atau alpa?
> 3) Mau saya masukkan 128 catatan absen dari file ini ke buku absensi Anda, supaya tercatat bersama bulan-bulan sebelumnya? Cukup balas "ya" bila mau; pertanyaan lain boleh dijawab nanti.

Penutup tidak lagi menawarkan "simpan supaya bulan depan tinggal tambah file", karena buku sudah ada; yang ditawarkan adalah memasukkan file ini ke buku. Bila pengguna membalas "ya" (boleh bersama jawaban lain, mis. "12 dan 13 Sari izin, iya masukkan"), agent **langsung memasukkan file itu** dengan satu "ya" tadi sebagai persetujuan: tanpa pratinjau kedua, tanpa ringkasan baru, tanpa "Betul?", tanpa rekap ulang. Karyawan yang terdaftar disimpan; Tamu tidak menghentikan penyimpanan dan hanya disebut singkat di kalimat penutup, mis.: "128 catatan sudah tersimpan: Andi 44, Sari 40, Joko 44. Catatan Tamu (ID 9) belum disimpan karena belum terdaftar." Sari izin 12-13/10 dicatat bila sudah dijawab.

## Verifikasi (dihitung di luar script)
| Hal | Hitungan manual | Hasil script |
|---|---|---|
| Andi telat (September) | 23 + 12 + 31 = 66 menit, 3x | 3x, 1 jam 6 menit ✓ |
| Joko telat (September) | 14 + 16 + 45 = 75 menit, 3x (17/09 08.08 di bawah batas) | 3x, 1 jam 15 menit ✓ |
| Sari telat | tidak pernah di atas 08.10 | 0x ✓ |
| Hari kerja September 2026 | 22 (Selasa 1/9 s.d. Rabu 30/9, Senin–Jumat) | 22 ✓ |
| Sari hadir | 22 − 14/09 − 21/09 − 22/09 = 19 | 19 ✓ |
| Jam kerja Sari | 19 hari × (17.05 − 07.55 − 60 menit = 490 menit) = 9.310 menit | 155 jam 10 menit ✓ |
| Jam kerja Andi / Joko | dibaca ulang dari CSV mentah dengan skrip terpisah (selisih masuk–pulang − 60 menit, hari lengkap saja): 9.719 / 10.187 menit | 161 jam 59 menit / 169 jam 47 menit ✓ |
| Andi hari tidak lengkap | 25/09 tanpa jam pulang | 1 hari, tidak dihitung jam kerjanya ✓ |
| Varian A, Andi jam kerja | 20 hari × 430 + 5 Sabtu × 307 = 10.135 menit | 168 jam 55 menit ✓ |
| Varian A tanpa opsi Sabtu | 20 × 430 + 5 × (307 − 60) = 9.835 menit; pulang cepat 5 × 178 = 890 menit | 163 jam 55 menit; 5x (14 jam 50 menit) ✓ |
| Varian B, Andi / Joko (Oktober) | Andi 21 × 490 + (17.05 − 08.41 − 60 = 444) = 10.734 menit; Joko 20 × 490 + 471 + 478 = 10.749 menit; telat Andi 41, Joko 14 menit (08.07 di bawah batas) | 178 jam 54 menit / 179 jam 9 menit; 1x (41 menit) / 1x (14 menit) ✓ |
| Varian B, jumlah catatan | (22 + 20 + 22 hari) × 2 scan = 128; baris Tamu tidak dihitung | 128 ✓ (`test_14a`) |
| Tidak ada file/database dibuat | folder database tidak terbentuk dan buku yang sudah ada tidak berubah (ukuran dan waktu ubah sama) | dicek di `tests/uji_regresi.py` (kelas `UjiRekapCepat`) ✓ |

## Perbedaan dengan alur lama
Sebelumnya balasan pertama untuk pesan seperti ini hanya berisi lima pertanyaan (lokasi simpan, daftar karyawan, ID mesin, kelonggaran telat, hitung lembur?) dan menyebut alamat file database; rekap baru keluar setelah pengguna membalas "ya". Informasi itu sudah ada di pesan pengguna atau di dalam file, jadi sekarang dikerjakan dulu dan hanya hal yang benar-benar belum diketahui yang ditanyakan di akhir.
