# 04 — Input buruk: nomor aneh, tanggal, nilai ambigu, nama ambigu, CSV rusak/formula, DB rusak/terkunci

- **Hasil: LULUS BERSYARAT.** Tidak ada crash/traceback, tidak ada penulisan ke file rusak (sha256 sama), formula injection tertangani. Namun **jalur pemulihan DB rusak gagal (T1, tinggi)** dan nama ambigu dengan satu kontak batal dipilih diam-diam (S2).

## Ringkasan
| Kelompok | Input | Hasil | Nilai |
|---|---|---|---|
| Nomor | `+62 812-0000-4001`, `0812-0000-4001`, `  0812   0000   4001 ` | ketiganya = 6281200004001; dua terakhir ditolak **duplikat** dengan kode kontak ✔ | ✔ |
| | `0812-` / `12345` / `0812-0000-40121234` | ditolak dengan alasan jelas | ✔ |
| | `62 0812 0000 4003`, `(+62)812-…`, `0062 812 …`, `812-…`, `0812.0000.4014` | dinormalisasi benar (+ peringatan "0 setelah 62") | ✔ |
| | `6.28120000400E+12` | ditolak + cara memperbaiki di Excel | ✔ |
| | `0812abc0004`, `… ext 2`, dua nomor dengan "/" | ditolak | ✔ |
| | `+60 12-345 6789` | diterima + peringatan luar negeri | ✔ |
| | nama berisi nomor (`--nama 0812-0000-4011`) | ditolak | ✔ |
| Tanggal (acuan Kamis 24/9) | `20/9` | ditolak: "sudah lewat 4 hari… tulis lengkap dengan tahunnya" ✔ | ✔ |
| | `31/9`, `2026-13-01`, `9/25` | "tidak ada di kalender" | ✔ |
| | `kemarin` sebagai follow-up | diterima + "langsung masuk TERLAMBAT" | ✔ |
| | `Kamis` (hari ini Kamis) | Kamis depan 1/10 + catatan | ✔ |
| | `Senin` → 28/9, `25/9` → 25/9, `tgl 3` → 3 Okt + catatan, `1/10/26` → 1 Okt | ✔ | ✔ |
| | `nanti sore`, `akhir bulan` | ditolak + contoh format | ✔ (agent tanya) |
| | `--masuk besok` | ditolak (masa depan) | ✔ |
| Nilai | `5m`, `1,2 m`, `1.500 jt`, `4,5`, `sejuta`, `-50rb` | ditolak dengan pertanyaan balik | ✔ |
| | `Rp 1.250.000,00`, `450.000`, `1.5jt` | 1.250.000 / 450.000 / 1.500.000 | ✔ |
| Nama ambigu | dua "Bu Sari" + "Sarinah"; `--kontak "Bu Sari"` / `"Sari"` / `"sari"` | ditolak "Ada 2 kontak yang cocok" + `pilihan` (Sarinah tidak ikut) ✔ | ✔ |
| | salah satu Bu Sari (K0018) **batal**; pemilik: "Bu Sari yang kemarin batal ternyata jadi order 2 jt" → `catat --kontak "Bu Sari" --tahap deal --nilai "2 jt"` | **K0017 (yang aktif) dijadikan deal tanpa bertanya**; K0018 tetap batal | ✖ **S2** |
| CSV rusak (`rusak.csv`) | `=HYPERLINK(...)` di nama, `=1+2`/`@SUM`/`-cmd|calc`/`+tambahan` di kebutuhan | disimpan sebagai teks; ekspor memberi `'` di depan (`'=HYPERLINK…`, `'=1+2`) ✔ | ✔ |
| | baris dengan tanda kutip tak tertutup | jadi kontak bernama **"Bu Eka;0812-0000-4106;kue lapis"** tanpa nomor (impor tidak memeriksa nomor di dalam nama, padahal `tambah` menolak) | ✖ rendah |
| | baris kosong `;;;;;` di baris 9 | baris sesudahnya dilaporkan dengan nomor salah: Bu Gina (baris file **10**) disebut "baris 9" | ✖ rendah |
| | ANSI/cp1252 "Ibu Réni" | terbaca + peringatan encoding ✔ | ✔ |
| | kosong / hanya header / biner / .xlsx / tanpa kolom nama / file tidak ada | pesan jelas, tidak ada yang tersimpan (biner: pesan memuat sampah biner, kosmetik) | ✔ |
| Ekspor | file sudah ada / berakhiran .db | ditolak (`--timpa` / harus .csv) | ✔ |
| DB terkunci | proses lain `BEGIN EXCLUSIVE`, `KOMUNITECH_CRM_TIMEOUT=2` | tulis & baca gagal setelah 2 detik dengan pesan "Data aman… ulangi"; setelah kunci lepas, perintah sukses | ✔ |
| DB rusak (header ditimpa) | `hari-ini`, `tambah`, `info` | ditolak, petunjuk backup/restore; file tidak diubah (sha256 sama) | ✔ |
| | **`restore --dari <cadangan sehat> --ya`** | **GAGAL: "Database rusak (file is not a database)… Pulihkan dari cadangan: restore"** — berputar ke saran yang sama | ✖ **T1** |
| DB rusak di tengah file / file 0 byte | `restore --ya` | berhasil, 19 kontak kembali ✔ | ✔ |
| Bukan DB crm / 0 byte | `hari-ini` → "bukan database crm-wa"; `init --ya` tidak menimpa | ✔ | ✔ |
| Hapus data (PDP) | `hapus --kontak Sarinah` → pratinjau → `--ya` | terhapus + riwayat, pesan "cadangan lama masih memuat data ini" ✔ | ✔ |
| Harga/catatan di kolom kebutuhan | `--kebutuhan "kue ultah 450rb, suaminya pelit"` | draf: "Soal **kue ultah 450rb, suaminya pelit**, boleh saya bantu…" — isi kebutuhan masuk draf apa adanya | ✖ **S5** |
| `draf --pesan` dengan & % # ? | tautan ter-encode benar (%26 %25 %23 %3F) | ✔ |

## Reproduksi T1 (tinggi)
```bash
python3 scripts/crm.py init --nama-usaha X --pengirim Y --ya --db /tmp/a/crm.db
python3 scripts/crm.py tambah --nama A --wa 0812-0000-0001 --db /tmp/a/crm.db   # cadangan harian dibuat
python3 -c "f=open('/tmp/a/crm.db','r+b'); f.write(b'X'*100)"                  # header rusak (mis. sinkron Drive gagal)
python3 scripts/crm.py backup --daftar --db /tmp/a/crm.db
python3 scripts/crm.py restore --dari /tmp/a/backup-crm/<file>.db --ya --db /tmp/a/crm.db
# -> GAGAL: Database rusak (file is not a database)... Pulihkan dari cadangan: ... restore
```
Penyebab: `cmd_restore` (crm.py:2170-2177) memakai `sqlite3.backup()` ke file tujuan yang rusak; SQLite menolak membuka tujuan. Salinan mentah "sebelum-restore" sudah dibuat (baik), tapi file tujuan tidak diganti. Saran: setelah salinan mentah, hapus/ganti file tujuan (tulis ke file sementara lalu `os.replace`). Dampak: pengguna awam/agent terjebak di saran yang berputar; risiko agent "memperbaiki" dengan menghapus DB.

## Transkrip asli
<details><summary>Bagian 1: nomor, tanggal, nilai, nama ambigu, CSV</summary>

```text
### A. Belum init
$ [2026-09-24] crm.py hari-ini
GAGAL: Database CRM belum ada di <uji>/s04/crm.db. Jalankan dulu: crm.py init (lalu --ya setelah pengguna setuju).
[kode keluar 1]

$ [2026-09-24] crm.py init --nama-usaha Toko Uji --pengirim Uji --ya
TERSIMPAN. Database CRM siap.
Database CRM baru: <uji>/s04/crm.db
Nama usaha: Toko Uji | Pengirim draf: Uji | Sapaan default: Kak | Zona: WIB
Cadangan otomatis: <uji>/s04/backup-crm
[kode keluar 0]

$ [2026-09-24] crm.py init --nama-usaha Toko Uji --pengirim Uji --ya
GAGAL: Database CRM sudah ada di <uji>/s04/crm.db. Tidak dibuat ulang (data aman). Untuk mengubah nama usaha/pengirim pakai: crm.py atur.
[kode keluar 1]

### B. Nomor aneh
$ [2026-09-24] crm.py tambah --nama Satu --wa +62 812-0000-4001
Tersimpan K0001: Satu | 0812-0000-4001 | Baru | sumber Tidak diketahui | follow-up Kamis, 24 September 2026
Catatan: Follow-up belum disebut; dijadwalkan hari ini (lead baru sebaiknya dibalas hari yang sama).
[kode keluar 0]

$ [2026-09-24] crm.py tambah --nama Satu Lagi --wa 0812-0000-4001
GAGAL: Nomor 0812-0000-4001 sudah tersimpan sebagai K0001 Satu (baru). Tidak ditambah dobel. Untuk mencatat obrolan baru pakai: crm.py catat --kontak K0001 --isi "...". Jika memang orang berbeda dengan nomor yang sama, ulangi dengan --izinkan-duplikat.
[kode keluar 1]

$ [2026-09-24] crm.py tambah --nama Satu Spasi --wa   0812   0000   4001 
GAGAL: Nomor 0812-0000-4001 sudah tersimpan sebagai K0001 Satu (baru). Tidak ditambah dobel. Untuk mencatat obrolan baru pakai: crm.py catat --kontak K0001 --isi "...". Jika memang orang berbeda dengan nomor yang sama, ulangi dengan --izinkan-duplikat.
[kode keluar 1]

$ [2026-09-24] crm.py tambah --nama Dua --wa 0812-
GAGAL: Nomor '0812-' tidak wajar: 3 digit setelah 62 (nomor HP Indonesia 9-12 digit, mis. 0812-0000-1234).
[kode keluar 1]

$ [2026-09-24] crm.py tambah --nama Tiga --wa 62 0812 0000 4003
Tersimpan K0002: Tiga | 0812-0000-4003 | Baru | sumber Tidak diketahui | follow-up Kamis, 24 September 2026
Catatan: Nomor '62 0812 0000 4003' berisi 0 setelah kode negara; angka 0 itu dibuang.
Catatan: Follow-up belum disebut; dijadwalkan hari ini (lead baru sebaiknya dibalas hari yang sama).
[kode keluar 0]

$ [2026-09-24] crm.py tambah --nama Empat --wa 6.28120000400E+12
GAGAL: Nomor '6.28120000400E+12' rusak: Excel mengubahnya menjadi angka ilmiah. Di Excel, format kolom nomor sebagai Teks lalu ketik ulang/ekspor ulang.
[kode keluar 1]

$ [2026-09-24] crm.py tambah --nama Lima --wa 0812abc0004
GAGAL: Nomor '0812abc0004' berisi huruf. Tulis angkanya saja, mis. 0812-0000-1234.
[kode keluar 1]

$ [2026-09-24] crm.py tambah --nama Enam --wa 0812 0000 4006 / 0813 0000 4007
GAGAL: Ada lebih dari satu nomor di '0812 0000 4006 / 0813 0000 4007'. Simpan satu nomor WA saja per kontak; nomor lain bisa ditulis di catatan.
[kode keluar 1]

$ [2026-09-24] crm.py tambah --nama Tujuh --wa +60 12-345 6789
Tersimpan K0003: Tujuh | +60123456789 | Baru | sumber Tidak diketahui | follow-up Kamis, 24 September 2026
Catatan: Nomor +60 12-345 6789 bukan nomor Indonesia (+60...); pastikan kode negaranya benar.
Catatan: Follow-up belum disebut; dijadwalkan hari ini (lead baru sebaiknya dibalas hari yang sama).
[kode keluar 0]

$ [2026-09-24] crm.py tambah --nama Delapan --wa (+62)812-0000-4008
Tersimpan K0004: Delapan | 0812-0000-4008 | Baru | sumber Tidak diketahui | follow-up Kamis, 24 September 2026
Catatan: Follow-up belum disebut; dijadwalkan hari ini (lead baru sebaiknya dibalas hari yang sama).
[kode keluar 0]

$ [2026-09-24] crm.py tambah --nama Sembilan --wa 0062 812 0000 4009
Tersimpan K0005: Sembilan | 0812-0000-4009 | Baru | sumber Tidak diketahui | follow-up Kamis, 24 September 2026
Catatan: Follow-up belum disebut; dijadwalkan hari ini (lead baru sebaiknya dibalas hari yang sama).
[kode keluar 0]

$ [2026-09-24] crm.py tambah --nama Sepuluh --wa 812-0000-4010
Tersimpan K0006: Sepuluh | 0812-0000-4010 | Baru | sumber Tidak diketahui | follow-up Kamis, 24 September 2026
Catatan: Follow-up belum disebut; dijadwalkan hari ini (lead baru sebaiknya dibalas hari yang sama).
[kode keluar 0]

$ [2026-09-24] crm.py tambah --nama Sebelas --wa 12345
GAGAL: Nomor '12345' tidak dikenali. Nomor Indonesia diawali 08, 62, atau +62.
[kode keluar 1]

$ [2026-09-24] crm.py tambah --nama 0812-0000-4011
GAGAL: Kolom nama berisi nomor telepon. Isi nama di --nama dan nomor di --wa.
[kode keluar 1]

$ [2026-09-24] crm.py tambah --nama Dua Belas --wa 0812-0000-40121234
GAGAL: Nomor '0812-0000-40121234' tidak wajar: 15 digit setelah 62 (nomor HP Indonesia 9-12 digit, mis. 0812-0000-1234).
[kode keluar 1]

$ [2026-09-24] crm.py tambah --nama Tiga Belas --wa +62 812 0000 4013 ext 2
GAGAL: Nomor '+62 812 0000 4013 ext 2' berisi huruf. Tulis angkanya saja, mis. 0812-0000-1234.
[kode keluar 1]

$ [2026-09-24] crm.py tambah --nama Empat Belas --wa 0812.0000.4014
Tersimpan K0007: Empat Belas | 0812-0000-4014 | Baru | sumber Tidak diketahui | follow-up Kamis, 24 September 2026
Catatan: Follow-up belum disebut; dijadwalkan hari ini (lead baru sebaiknya dibalas hari yang sama).
[kode keluar 0]

### C. Tanggal
$ [2026-09-24] crm.py tambah --nama Tgl Lewat --wa 0812-0000-4020 --followup 20/9
GAGAL: Tanggal '20/9' (20 Sep 2026) sudah lewat 4 hari. Kalau memang tanggal itu, tulis lengkap dengan tahunnya (mis. 20/9/2026); kalau maksudnya tahun depan, tulis tahunnya juga.
[kode keluar 1]

$ [2026-09-24] crm.py tambah --nama Tgl Tidak Ada --wa 0812-0000-4021 --followup 31/9
GAGAL: Tanggal '31/9' tidak ada di kalender.
[kode keluar 1]

$ [2026-09-24] crm.py tambah --nama Tgl Kemarin --wa 0812-0000-4022 --followup kemarin
Tersimpan K0008: Tgl Kemarin | 0812-0000-4022 | Baru | sumber Tidak diketahui | follow-up Rabu, 23 September 2026
Catatan: 23 Sep 2026 sudah lewat 1 hari, jadi kontak ini langsung masuk daftar TERLAMBAT.
[kode keluar 0]

$ [2026-09-24] crm.py tambah --nama Tgl Nanti Sore --wa 0812-0000-4023 --followup nanti sore
GAGAL: Tanggal 'nanti sore' tidak dikenali. Contoh yang bisa: 3/10, 3 Okt, 3/10/2026, besok, lusa, Jumat, 3 hari lagi, minggu depan.
[kode keluar 1]

$ [2026-09-24] crm.py tambah --nama Tgl Masuk Besok --wa 0812-0000-4024 --masuk besok
GAGAL: Tanggal 'besok' (25 Sep 2026) ada di masa depan; tanggal kejadian harus hari ini atau sebelumnya.
[kode keluar 1]

$ [2026-09-24] crm.py tambah --nama Tgl Kamis --wa 0812-0000-4025 --followup Kamis
Tersimpan K0009: Tgl Kamis | 0812-0000-4025 | Baru | sumber Tidak diketahui | follow-up Kamis, 1 Oktober 2026
Catatan: Hari ini juga Kamis; dipakai Kamis depan (1 Okt 2026).
[kode keluar 0]

$ [2026-09-24] crm.py tambah --nama Tgl 25/9 --wa 0812-0000-4026 --followup 25/9
Tersimpan K0010: Tgl 25/9 | 0812-0000-4026 | Baru | sumber Tidak diketahui | follow-up Jumat, 25 September 2026
[kode keluar 0]

$ [2026-09-24] crm.py tambah --nama Tgl tgl 3 --wa 0812-0000-4027 --followup tgl 3
Tersimpan K0011: Tgl tgl 3 | 0812-0000-4027 | Baru | sumber Tidak diketahui | follow-up Sabtu, 3 Oktober 2026
Catatan: Bulan tidak disebut; dipakai 3 Okt 2026 (tanggal 3 terdekat).
[kode keluar 0]

$ [2026-09-24] crm.py tambah --nama Tgl 2026-13-01 --wa 0812-0000-4028 --followup 2026-13-01
GAGAL: Tanggal '2026-13-01' tidak ada di kalender.
[kode keluar 1]

$ [2026-09-24] crm.py tambah --nama Tgl 9/25 --wa 0812-0000-4029 --followup 9/25
GAGAL: Tanggal '9/25' tidak ada di kalender.
[kode keluar 1]

$ [2026-09-24] crm.py tambah --nama Tgl akhir bulan --wa 0812-0000-4030 --followup akhir bulan
GAGAL: Tanggal 'akhir bulan' tidak dikenali. Contoh yang bisa: 3/10, 3 Okt, 3/10/2026, besok, lusa, Jumat, 3 hari lagi, minggu depan.
[kode keluar 1]

$ [2026-09-24] crm.py tambah --nama Tgl Senin --wa 0812-0000-4031 --followup Senin
Tersimpan K0012: Tgl Senin | 0812-0000-4031 | Baru | sumber Tidak diketahui | follow-up Senin, 28 September 2026
[kode keluar 0]

$ [2026-09-24] crm.py tambah --nama Tgl 1/10/26 --wa 0812-0000-4032 --followup 1/10/26
Tersimpan K0013: Tgl 1/10/26 | 0812-0000-4032 | Baru | sumber Tidak diketahui | follow-up Kamis, 1 Oktober 2026
[kode keluar 0]

### D. Nilai
$ [2026-09-24] crm.py tambah --nama N1 --wa 0812-0000-4040 --nilai 5m
GAGAL: Nilai '5m' ambigu: 'm' itu juta atau miliar? Tulis 'jt' atau 'miliar'.
[kode keluar 1]

$ [2026-09-24] crm.py tambah --nama N2 --wa 0812-0000-4041 --nilai 1.500 jt
GAGAL: Nilai '1.500 jt' ambigu (mis. '1.500 jt' = 1,5 juta atau 1.500 juta?). Tulis mis. '1,5 jt' atau '1500000'.
[kode keluar 1]

$ [2026-09-24] crm.py tambah --nama N3 --wa 0812-0000-4042 --nilai 4,5
GAGAL: Nilai '4,5' ambigu. Tulis mis. '4,5 jt', '450rb', atau '4.500.000'.
[kode keluar 1]

$ [2026-09-24] crm.py tambah --nama N4 --wa 0812-0000-4043 --nilai=-50rb
GAGAL: Nilai '-50rb' tidak boleh negatif.
[kode keluar 1]

$ [2026-09-24] crm.py tambah --nama N5 --wa 0812-0000-4044 --nilai Rp 1.250.000,00
Tersimpan K0014: N5 | 0812-0000-4044 | Baru | sumber Tidak diketahui | nilai Rp 1.250.000 | follow-up Kamis, 24 September 2026
Catatan: Follow-up belum disebut; dijadwalkan hari ini (lead baru sebaiknya dibalas hari yang sama).
[kode keluar 0]

$ [2026-09-24] crm.py tambah --nama N6 --wa 0812-0000-4045 --nilai 1,2 m
GAGAL: Nilai '1,2 m' ambigu: 'm' itu juta atau miliar? Tulis 'jt' atau 'miliar'.
[kode keluar 1]

$ [2026-09-24] crm.py tambah --nama N7 --wa 0812-0000-4046 --nilai sejuta
GAGAL: Nilai 'sejuta' tidak dikenali. Contoh: 450rb, 4,5 jt, 4.500.000.
[kode keluar 1]

$ [2026-09-24] crm.py tambah --nama N8 --wa 0812-0000-4047 --nilai 450.000
Tersimpan K0015: N8 | 0812-0000-4047 | Baru | sumber Tidak diketahui | nilai Rp 450.000 | follow-up Kamis, 24 September 2026
Catatan: Follow-up belum disebut; dijadwalkan hari ini (lead baru sebaiknya dibalas hari yang sama).
[kode keluar 0]

$ [2026-09-24] crm.py tambah --nama N9 --wa 0812-0000-4048 --nilai 1.5jt
Tersimpan K0016: N9 | 0812-0000-4048 | Baru | sumber Tidak diketahui | nilai Rp 1.500.000 | follow-up Kamis, 24 September 2026
Catatan: Follow-up belum disebut; dijadwalkan hari ini (lead baru sebaiknya dibalas hari yang sama).
[kode keluar 0]

### E. Nama ambigu
$ [2026-09-24] crm.py tambah --nama Bu Sari --wa 0812-0000-4050 --kebutuhan kue A
Tersimpan K0017: Bu Sari | 0812-0000-4050 | Baru | sumber Tidak diketahui | follow-up Kamis, 24 September 2026
Catatan: Follow-up belum disebut; dijadwalkan hari ini (lead baru sebaiknya dibalas hari yang sama).
[kode keluar 0]

$ [2026-09-24] crm.py tambah --nama Bu Sari --wa 0812-0000-4051 --kebutuhan kue B
Tersimpan K0018: Bu Sari | 0812-0000-4051 | Baru | sumber Tidak diketahui | follow-up Kamis, 24 September 2026
Catatan: Follow-up belum disebut; dijadwalkan hari ini (lead baru sebaiknya dibalas hari yang sama).
Catatan: Nama mirip kontak lain: K0017 Bu Sari (0812-****-4050). Jika orangnya sama, gabungkan dengan crm.py gabung.
[kode keluar 0]

$ [2026-09-24] crm.py tambah --nama Sarinah --wa 0812-0000-4052
Tersimpan K0019: Sarinah | 0812-0000-4052 | Baru | sumber Tidak diketahui | follow-up Kamis, 24 September 2026
Catatan: Follow-up belum disebut; dijadwalkan hari ini (lead baru sebaiknya dibalas hari yang sama).
[kode keluar 0]

$ [2026-09-24] crm.py catat --kontak Bu Sari --isi tes
GAGAL: Ada 2 kontak yang cocok dengan 'Bu Sari'. Tanyakan yang mana (sebut kodenya).
[kode keluar 1]

$ [2026-09-24] crm.py catat --kontak Sari --isi tes
GAGAL: Ada 2 kontak yang cocok dengan 'Sari'. Tanyakan yang mana (sebut kodenya).
[kode keluar 1]

$ [2026-09-24] crm.py catat --kontak sari --isi tes
GAGAL: Ada 2 kontak yang cocok dengan 'sari'. Tanyakan yang mana (sebut kodenya).
[kode keluar 1]

$ [2026-09-24] crm.py catat --kontak K0999 --isi tes
GAGAL: Kontak K0999 tidak ada. Cek dengan: crm.py daftar --tahap semua
[kode keluar 1]

$ [2026-09-24] crm.py catat --kontak 0812-0000-4051 --tahap batal --alasan belum butuh
Dicatat K0018 Bu Sari: tahap baru -> batal (alasan: belum butuh); jadwal follow-up dihapus.
Sekarang: Batal | tanpa jadwal follow-up
[kode keluar 0]

--- satu Bu Sari batal; pengguna: 'Bu Sari yang kemarin batal ternyata jadi order 2 jt'
$ [2026-09-24] crm.py catat --kontak Bu Sari --tahap deal --nilai 2 jt
Dicatat K0017 Bu Sari: tahap baru -> deal; nilai Rp 2.000.000.
Sekarang: Deal | nilai Rp 2.000.000 | follow-up Kamis, 24 September 2026
[kode keluar 0]

$ [2026-09-24] crm.py catat --kontak Bu Sari --tahap batal
GAGAL: Tahap batal butuh alasan singkat (mis. harga terlalu mahal, tidak ada respon, pilih penjual lain, belum butuh). Tanyakan ke pengguna lalu isi --alasan.
[kode keluar 1]

$ [2026-09-24] crm.py catat --kontak Bu Sari --isi halo --tahap bogus
GAGAL: Tahap 'bogus' tidak dikenal. Pilihan: baru, dihubungi, ditawar, deal, selesai, batal.
[kode keluar 1]

### F. CSV rusak
$ [2026-09-24] crm.py impor <uji>/csv/rusak.csv
PRATINJAU (belum disimpan):
Impor rusak.csv: 8 baris dibaca.
Kolom dikenali: nama <- 'nama', wa <- 'no wa', kebutuhan <- 'kebutuhan', nilai <- 'nilai', followup <- 'follow up', tgl_masuk <- 'tgl masuk'
Kontak baru: 2 | Duplikat dilewati: 1 | Baris bermasalah dilewati: 5
+ (baru) =HYPERLINK("http://contoh.invalid/x","Klik") | 0812-****-4101 | baru | Tidak diketahui
+ (baru) Bu Eka;0812-0000-4106;kue lapis | - | baru | Tidak diketahui
= baris 9 Bu Gina: sudah ada (baris 2 di file ini)
! baris 3: Nomor '6.28120000411E+12' rusak: Excel mengubahnya menjadi angka ilmiah. Di Excel, format kolom nomor sebagai Teks lalu ketik ulang/ekspor ulang
! baris 4: Nilai '5m' ambigu: 'm' itu juta atau miliar? Tulis 'jt' atau 'miliar'
! baris 5: Nilai '1.500 jt' ambigu (mis. '1.500 jt' = 1,5 juta atau 1.500 juta?). Tulis mis. '1,5 jt' atau '1500000'
! baris 6: Ada lebih dari satu nomor di '0812 0000 4104 / 0813 0000 4105'. Simpan satu nomor WA saja per kontak; nomor lain bisa ditulis di catatan
! baris 8: Tanggal 'besok' (25 Sep 2026) ada di masa depan; tanggal kejadian harus hari ini atau sebelumnya

Simpan? Jalankan perintah yang sama + --ya setelah pengguna setuju.
[kode keluar 0]

$ [2026-09-24] crm.py impor <uji>/csv/rusak.csv --ya
TERSIMPAN.
Impor rusak.csv: 8 baris dibaca.
Kolom dikenali: nama <- 'nama', wa <- 'no wa', kebutuhan <- 'kebutuhan', nilai <- 'nilai', followup <- 'follow up', tgl_masuk <- 'tgl masuk'
Kontak baru: 2 | Duplikat dilewati: 1 | Baris bermasalah dilewati: 5
+ K0020 =HYPERLINK("http://contoh.invalid/x","Klik") | 0812-****-4101 | baru | Tidak diketahui
+ K0021 Bu Eka;0812-0000-4106;kue lapis | - | baru | Tidak diketahui
= baris 9 Bu Gina: sudah ada (baris 2 di file ini)
! baris 3: Nomor '6.28120000411E+12' rusak: Excel mengubahnya menjadi angka ilmiah. Di Excel, format kolom nomor sebagai Teks lalu ketik ulang/ekspor ulang
! baris 4: Nilai '5m' ambigu: 'm' itu juta atau miliar? Tulis 'jt' atau 'miliar'
! baris 5: Nilai '1.500 jt' ambigu (mis. '1.500 jt' = 1,5 juta atau 1.500 juta?). Tulis mis. '1,5 jt' atau '1500000'
! baris 6: Ada lebih dari satu nomor di '0812 0000 4104 / 0813 0000 4105'. Simpan satu nomor WA saja per kontak; nomor lain bisa ditulis di catatan
! baris 8: Tanggal 'besok' (25 Sep 2026) ada di masa depan; tanggal kejadian harus hari ini atau sebelumnya
Cadangan sebelum perubahan: <uji>/s04/backup-crm/crm-20260924-090000-impor.db
[kode keluar 0]

$ [2026-09-24] crm.py impor <uji>/csv/ansi.csv
PRATINJAU (belum disimpan):
Impor ansi.csv: 1 baris dibaca.
Kolom dikenali: nama <- 'nama', wa <- 'hp'
Kontak baru: 1 | Duplikat dilewati: 0 | Baris bermasalah dilewati: 0
+ (baru) Ibu Réni | 0812-****-4108 | baru | Tidak diketahui
Catatan: File bukan UTF-8; dibaca sebagai Windows-1252 (ANSI). Periksa huruf khusus di nama.

Simpan? Jalankan perintah yang sama + --ya setelah pengguna setuju.
[kode keluar 0]

$ [2026-09-24] crm.py impor <uji>/csv/kosong.csv
GAGAL: File kosong.csv kosong.
[kode keluar 1]

$ [2026-09-24] crm.py impor <uji>/csv/header-saja.csv
PRATINJAU (belum disimpan):
Impor header-saja.csv: 0 baris dibaca.
Kolom dikenali: nama <- 'nama', wa <- 'no wa'
Kontak baru: 0 | Duplikat dilewati: 0 | Baris bermasalah dilewati: 0

Simpan? Jalankan perintah yang sama + --ya setelah pengguna setuju.
[kode keluar 0]

$ [2026-09-24] crm.py impor <uji>/csv/biner.csv
GAGAL: Kolom nama tidak ditemukan. Header file: <~300 byte sampah biner, dipotong penguji>. Beri judul kolom 'nama' (dan 'no wa', 'sumber', 'tahap', 'nilai', 'kebutuhan', 'label' bila ada). Contoh: templates/kontak-contoh.csv.
[kode keluar 1]

$ [2026-09-24] crm.py impor <uji>/csv/data.xlsx
GAGAL: File data.xlsx belum didukung langsung. Di Excel/Sheets: File > Save As/Download > CSV, lalu kirim file CSV-nya.
[kode keluar 1]

$ [2026-09-24] crm.py impor <uji>/csv/tanpa-nama.csv
GAGAL: Kolom nama tidak ditemukan. Header file: telepon, alamat. Beri judul kolom 'nama' (dan 'no wa', 'sumber', 'tahap', 'nilai', 'kebutuhan', 'label' bila ada). Contoh: templates/kontak-contoh.csv.
[kode keluar 1]

$ [2026-09-24] crm.py impor <uji>/csv/tidak-ada.csv
GAGAL: File <uji>/csv/tidak-ada.csv tidak ditemukan.
[kode keluar 1]

$ [2026-09-24] crm.py ekspor --csv <uji>/s04/ekspor.csv
Ekspor 21 kontak ke <uji>/s04/ekspor.csv (pemisah ';', UTF-8, aman dibuka di Excel).
File ini berisi nomor HP pelanggan (data pribadi). Data pelanggan (nomor HP) adalah data pribadi (UU 27/2022 PDP): simpan di komputer ini, jangan dibagikan ke grup, hapus bila pelanggan meminta.
[kode keluar 0]

$ [2026-09-24] crm.py ekspor --csv <uji>/s04/ekspor.csv
GAGAL: File <uji>/s04/ekspor.csv sudah ada. Pakai nama lain atau tambahkan --timpa bila memang ingin ditimpa.
[kode keluar 1]

$ [2026-09-24] crm.py ekspor --csv <uji>/s04/ekspor.db
GAGAL: Nama file ekspor harus berakhiran .csv.
[kode keluar 1]
```
</details>
<details><summary>Bagian 2: DB terkunci/rusak, restore, hapus, draf</summary>

```text
### G. DB terkunci (proses lain memegang kunci tulis), KOMUNITECH_CRM_TIMEOUT=2
$ [2026-09-24] crm.py tambah --nama Saat Terkunci --wa 0812-0000-4200
GAGAL: Database CRM sedang dipakai program lain (mis. jadwal OpenClaw atau jendela lain) dan tidak selesai dalam 2 detik. Data aman, tidak rusak. Tunggu sebentar lalu ulangi perintah yang sama. Jangan hapus file database.
[kode keluar 1]

(durasi 2 detik)
$ [2026-09-24] crm.py hari-ini --tanpa-draf
GAGAL: Database CRM sedang dipakai program lain (mis. jadwal OpenClaw atau jendela lain) dan tidak selesai dalam 2 detik. Data aman, tidak rusak. Tunggu sebentar lalu ulangi perintah yang sama. Jangan hapus file database.
[kode keluar 1]

$ [2026-09-24] crm.py rekap
GAGAL: Database CRM sedang dipakai program lain (mis. jadwal OpenClaw atau jendela lain) dan tidak selesai dalam 2 detik. Data aman, tidak rusak. Tunggu sebentar lalu ulangi perintah yang sama. Jangan hapus file database.
[kode keluar 1]

$ [2026-09-24] crm.py impor <uji>/csv/ansi.csv --ya
TERSIMPAN.
Impor ansi.csv: 1 baris dibaca.
Kolom dikenali: nama <- 'nama', wa <- 'hp'
Kontak baru: 1 | Duplikat dilewati: 0 | Baris bermasalah dilewati: 0
+ K0022 Ibu Réni | 0812-****-4108 | baru | Tidak diketahui
Catatan: File bukan UTF-8; dibaca sebagai Windows-1252 (ANSI). Periksa huruf khusus di nama.
Cadangan sebelum perubahan: <uji>/s04/backup-crm/crm-20260924-090000-impor-2.db
[kode keluar 0]

$ [2026-09-24] crm.py tambah --nama Setelah Kunci Lepas --wa 0812-0000-4200
Tersimpan K0023: Setelah Kunci Lepas | 0812-0000-4200 | Baru | sumber Tidak diketahui | follow-up Kamis, 24 September 2026
Catatan: Follow-up belum disebut; dijadwalkan hari ini (lead baru sebaiknya dibalas hari yang sama).
[kode keluar 0]

### H. DB rusak / 0 byte / bukan DB crm
$ [2026-09-24] crm.py hari-ini
GAGAL: File <uji>/s04/rusak.db rusak atau bukan database crm-wa. Jangan hapus file itu. Pulihkan dari cadangan: crm.py backup --daftar, lalu crm.py restore --dari <file> (pratinjau dulu).
[kode keluar 1]

$ [2026-09-24] crm.py tambah --nama Z --wa 0812-0000-4201
GAGAL: File <uji>/s04/rusak.db rusak atau bukan database crm-wa. Jangan hapus file itu. Pulihkan dari cadangan: crm.py backup --daftar, lalu crm.py restore --dari <file> (pratinjau dulu).
[kode keluar 1]

$ [2026-09-24] crm.py info
GAGAL: File <uji>/s04/rusak.db rusak atau bukan database crm-wa. Jangan hapus file itu. Pulihkan dari cadangan: crm.py backup --daftar, lalu crm.py restore --dari <file> (pratinjau dulu).
[kode keluar 1]

(file rusak tidak diubah: sha256 sama)
$ [2026-09-24] crm.py hari-ini
GAGAL: File <uji>/s04/tengah-rusak.db rusak atau bukan database crm-wa. Jangan hapus file itu. Pulihkan dari cadangan: crm.py backup --daftar, lalu crm.py restore --dari <file> (pratinjau dulu).
[kode keluar 1]

$ [2026-09-24] crm.py info
GAGAL: File <uji>/s04/tengah-rusak.db rusak atau bukan database crm-wa. Jangan hapus file itu. Pulihkan dari cadangan: crm.py backup --daftar, lalu crm.py restore --dari <file> (pratinjau dulu).
[kode keluar 1]

$ [2026-09-24] crm.py tambah --nama Z --wa 0812-0000-4202
GAGAL: File <uji>/s04/tengah-rusak.db rusak atau bukan database crm-wa. Jangan hapus file itu. Pulihkan dari cadangan: crm.py backup --daftar, lalu crm.py restore --dari <file> (pratinjau dulu).
[kode keluar 1]

$ [2026-09-24] crm.py hari-ini
GAGAL: File <uji>/s04/nol.db bukan database crm-wa (no such table: meta). File itu tidak diubah; periksa --db.
[kode keluar 1]

$ [2026-09-24] crm.py init --ya
GAGAL: File <uji>/s04/nol.db sudah ada dan bukan database crm-wa; tidak ditimpa. Pakai --db lain.
[kode keluar 1]

$ [2026-09-24] crm.py hari-ini
GAGAL: File <uji>/s04/lain.db bukan database crm-wa (no such table: meta). File itu tidak diubah; periksa --db.
[kode keluar 1]

$ [2026-09-24] crm.py init --ya
GAGAL: File <uji>/s04/lain.db sudah ada dan bukan database crm-wa; tidak ditimpa. Pakai --db lain.
[kode keluar 1]

### I. Restore
$ [2026-09-24] crm.py backup --daftar
Cadangan di <uji>/s04/backup-crm:
- crm-20260924-090000-harian.db
- crm-20260924-090000-impor-2.db
- crm-20260924-090000-impor.db
[kode keluar 0]

$ [2026-09-24] crm.py restore --dari <uji>/s04/backup-crm/crm-20260924-090000-impor.db
PRATINJAU (belum disimpan):
Database <uji>/s04/rusak.db akan diganti dengan cadangan crm-20260924-090000-impor.db (19 kontak). Database saat ini disalin dulu apa adanya ke folder backup-crm.

Lanjut? Jalankan perintah yang sama + --ya setelah pengguna setuju.
[kode keluar 0]

$ [2026-09-24] crm.py restore --dari <uji>/s04/backup-crm/crm-20260924-090000-impor.db --ya
GAGAL: Database rusak (file is not a database). Jangan hapus file itu. Pulihkan dari cadangan: crm.py backup --daftar, lalu crm.py restore --dari <file>.
[kode keluar 1]

$ [2026-09-24] crm.py hari-ini --tanpa-draf
GAGAL: File <uji>/s04/rusak.db rusak atau bukan database crm-wa. Jangan hapus file itu. Pulihkan dari cadangan: crm.py backup --daftar, lalu crm.py restore --dari <file> (pratinjau dulu).
[kode keluar 1]

$ [2026-09-24] crm.py restore --dari <uji>/s04/tengah-rusak.db
GAGAL: File <uji>/s04/tengah-rusak.db rusak atau bukan database crm-wa. Jangan hapus file itu. Pulihkan dari cadangan: crm.py backup --daftar, lalu crm.py restore --dari <file> (pratinjau dulu).
[kode keluar 1]

### J. Hapus data pelanggan (PDP)
$ [2026-09-24] crm.py hapus --kontak Sarinah
PRATINJAU (belum disimpan):
Hapus permanen K0019 Sarinah (0812-0000-4052) beserta 1 riwayat.
Catatan privasi: file cadangan lama di <uji>/s04/backup-crm masih memuat data ini; hapus file cadangan lama bila pelanggan meminta datanya dihapus total.

Simpan? Jalankan perintah yang sama + --ya setelah pengguna setuju.
[kode keluar 0]

$ [2026-09-24] crm.py hapus --kontak Sarinah --ya
TERSIMPAN.
Hapus permanen K0019 Sarinah (0812-0000-4052) beserta 1 riwayat.
Catatan privasi: file cadangan lama di <uji>/s04/backup-crm masih memuat data ini; hapus file cadangan lama bila pelanggan meminta datanya dihapus total.
Cadangan sebelum perubahan: <uji>/s04/backup-crm/crm-20260924-090000-hapus.db
[kode keluar 0]

$ [2026-09-24] crm.py lihat --kontak Sarinah
GAGAL: Kontak 'Sarinah' tidak ditemukan. Cek ejaan atau lihat: crm.py daftar --tahap semua
[kode keluar 1]

### K. Isi kebutuhan berisi harga/catatan pribadi -> masuk draf?
$ [2026-09-24] crm.py tambah --nama Bu Harga --wa 0812-0000-4300 --kebutuhan kue ultah 450rb, suaminya pelit --nilai 450rb --catatan RAHASIA: pernah telat bayar
Tersimpan K0024: Bu Harga | 0812-0000-4300 | Baru | sumber Tidak diketahui | nilai Rp 450.000 | follow-up Kamis, 24 September 2026
Catatan: Follow-up belum disebut; dijadwalkan hari ini (lead baru sebaiknya dibalas hari yang sama).
[kode keluar 0]

$ [2026-09-24] crm.py draf --kontak Bu Harga
Draf untuk K0024 Bu Harga (sapaan-awal) - periksa dulu, lalu kirim sendiri:
Halo Bu Harga, terima kasih sudah menghubungi Toko Uji. Saya Uji. Soal kue ultah 450rb, suaminya pelit, boleh saya bantu jelaskan pilihan dan harganya? Kira-kira dibutuhkan untuk kapan ya?
Buka tautan ini, periksa pesannya, lalu tekan Kirim:
https://wa.me/6281200004300?text=Halo%20Bu%20Harga%2C%20terima%20kasih%20sudah%20menghubungi%20Toko%20Uji.%20Saya%20Uji.%20Soal%20kue%20ultah%20450rb%2C%20suaminya%20pelit%2C%20boleh%20saya%20bantu%20jelaskan%20pilihan%20dan%20harganya%3F%20Kira-kira%20dibutuhkan%20untuk%20kapan%20ya%3F
Setelah terkirim, balas: "terkirim K0024".
[kode keluar 0]

$ [2026-09-24] crm.py draf --kontak Bu Harga --pesan Halo Bu, ini harga final Rp 450.000 & ongkir 20% ya? #promo
Draf untuk K0024 Bu Harga (pesan-sendiri) - periksa dulu, lalu kirim sendiri:
Halo Bu, ini harga final Rp 450.000 & ongkir 20% ya? #promo
Buka tautan ini, periksa pesannya, lalu tekan Kirim:
https://wa.me/6281200004300?text=Halo%20Bu%2C%20ini%20harga%20final%20Rp%20450.000%20%26%20ongkir%2020%25%20ya%3F%20%23promo
Setelah terkirim, balas: "terkirim K0024".
[kode keluar 0]
```
</details>
<details><summary>rusak.csv</summary>

```text
nama;no wa;kebutuhan;nilai;follow up;tgl masuk
=HYPERLINK("http://contoh.invalid/x","Klik");0812-0000-4101;=1+2;450rb;;
Bu Ani;6.28120000411E+12;kue;;;
Pak Beni;0812-0000-4102;@SUM(A1:A3);5m;;
Mbak Cici;0812-0000-4103;-cmd|calc;1.500 jt;31/9;
Kak Dodi;0812 0000 4104 / 0813 0000 4105;;;;
"Bu Eka;0812-0000-4106;kue "lapis;
Om Fajar;0812-0000-4107;+tambahan;2 jt;kemarin;besok
;;;;;
Bu Gina;+62 812-0000-4101;dobel dgn baris 2;;;
```
</details>
