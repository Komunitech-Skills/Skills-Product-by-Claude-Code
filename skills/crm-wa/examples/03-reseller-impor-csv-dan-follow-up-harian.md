# 03 — Reseller hijab: impor kontak CSV (Google Contacts & ekspor kontak WA), follow-up harian, ekspor (normal)

- **Data fiktif:** "Grosir Hijab Nisa", 21–24 Sep 2026. File uji (dibuat penguji, pola kolom mengikuti format umum):
  - `google-baru.csv` — ekspor Google Contacts format baru (First/Middle/Last Name, Labels "\* myContacts ::: Reseller", Phone 1/Phone 2, nilai ganda "a ::: b").
  - `google-lama.csv` — format "Google CSV" lama (Name, Given Name, Group Membership, Phone 1 - Type/Value).
  - `wa-ekspor.csv` — gaya ekstensi pengekspor kontak WhatsApp (`Name,Number,Label`, nomor 62…, nama "~ …", baris tanpa nama).
  - `wa-ekspor-nomor.csv` — daftar manual `Nama;Nomor;Keterangan`.
  - `besar.csv` — 300 kontak (uji volume).
- **Hasil: LULUS BERSYARAT.** Alur follow-up harian & angka benar (TOTAL BEDA: 0), tetapi impor punya 2 cacat sedang (S3, S4) dan banjir daftar harian setelah impor besar (S6).

## Hasil impor
| File | Hasil | Penilaian |
|---|---|---|
| Google baru | 3 masuk, 1 duplikat dalam file (Doni = nomor Rina) ✔, 2 dilewati: "nama kosong" ✔ dan **Wati "+62 812-0000-3003 ::: +62 813-0000-3004" ditolak "24 digit"** | ✖ nilai ganda Google tidak dipecah; pesan membingungkan |
| | Bu Endang: Phone 1 = rumah 021-0000-3005, Phone 2 = HP 0812-0000-3006 → **disimpan nomor rumah**, HP diabaikan (hanya peringatan "bukan nomor HP"); tampilan "0210-000-3005" salah format | ✖ |
| | Labels "\* myContacts ::: Reseller" disimpan sebagai **satu** label "\* mycontacts ::: reseller" → `daftar --label reseller` = **0 kontak** | ✖ |
| Google lama | 2 masuk, nama dari kolom Name ✔ | ✔ |
| Ekspor WA `Name,Number` | Kolom **Number tidak dikenali** → pratinjau: 3 kontak baru **tanpa nomor** ("-"), hanya catatan kecil "Kolom diabaikan: Number" | ✖ **S3** |
| `Nama;Nomor;Keterangan` | Kolom **Nomor tidak dikenali** → 2 kontak tanpa nomor | ✖ **S3** |
| Impor ulang ekspor sendiri (`kontak.csv`) | 5 duplikat dilewati, kolom kode/link_wa/tgl_deal diabaikan ✔ | ✔ |
| 300 kontak | pratinjau benar; setelah `--ya` **semua** dijadwalkan follow-up hari ini → `hari-ini` = 351 baris / 29 KB berisi 300 nama + nomor (`--samarkan --tanpa-draf` masih 22 KB) | ✖ **S6** |

## Follow-up harian (21–24 Sep)
- 21/9 `hari-ini --tanpa-draf` → 5 hari ini ✔; `terkirim` Rina & Agus → dihubungi, FU 23/9 ✔.
- Siska "order 2,5 jt, transfer besok" → deal + FU besok ✔; 22/9 "sudah transfer" → selesai, jadwal dihapus ✔.
- 22/9 & 24/9: `--maks-draf` dihormati; Bu Endang (nomor rumah) tetap dibuatkan tautan wa.me ke 622100003005.
- Draf "Halo Kak Siska Reseller Bogor" / "Pak Heru Grosir" — nama kontak Google yang berisi keterangan ikut masuk sapaan (data pengguna; kosmetik).
- Sapaan-awal untuk kontak lama hasil impor tetap "terima kasih sudah menghubungi…" — kurang pas untuk pelanggan lama (rendah).

## Ekspor & jembatan
- `ekspor --format pengingat` → 3 prospek, tanpa nomor HP ✔. `perintah_pengingat` dijalankan sungguhan ke `pengingat-follow-up/scripts/cek_jatuh_tempo.py tambah` → 3/3 kode keluar 0 ✔.
  **Tetapi (S7):** perintah itu tidak menyertakan `--file`, sehingga pengingat-follow-up menulis ke `./pengingat/DAFTAR.csv` di **folder kerja saat itu** (bukan `KomunitechData`). Dalam uji ini folder kerja penguji kebetulan root repo, sehingga `pengingat/DAFTAR.csv` (3 nama fiktif + tanggal + nominal) terbentuk di root repo; sudah dipindahkan koordinator. Lihat HASIL-UJI S7.
- `ekspor --csv kontak.csv` (path relatif) menulis ke folder kerja dan pesan hanya menyebut "ke kontak.csv", **bukan path lengkap** (S7).
- CSV `;` UTF-8 BOM, peringatan PDP ✔. `--samarkan`: nama → "R."/"Bu E.", nomor disamarkan, link kosong ✔.

## Transkrip asli
<details><summary>Keluaran lengkap crm.py</summary>

```text
$ [2026-09-21] crm.py init --nama-usaha Grosir Hijab Nisa --pengirim Nisa --sapaan Kak --ya
TERSIMPAN. Database CRM siap.
Database CRM baru: <uji>/s03/crm.db
Nama usaha: Grosir Hijab Nisa | Pengirim draf: Nisa | Sapaan default: Kak | Zona: WIB
Cadangan otomatis: <uji>/s03/backup-crm
[kode keluar 0]

$ [2026-09-21] crm.py impor <uji>/csv/google-baru.csv --sumber-default referensi
PRATINJAU (belum disimpan):
Impor google-baru.csv: 6 baris dibaca.
Kolom dikenali: catatan <- 'Notes', label <- 'Labels', wa <- 'Phone 1 - Value'
Kontak baru: 3 | Duplikat dilewati: 1 | Baris bermasalah dilewati: 2
+ (baru) Rina Susanti | 0812-****-3001 | baru | Referensi
+ (baru) Agus | 0812-****-3002 | baru | Referensi
+ (baru) Bu Endang | 0210-****-3005 | baru | Referensi
= baris 7 Doni: sudah ada (baris 2 di file ini)
! baris 4: Nomor '+62 812-0000-3003 ::: +62 813-0000-3004' tidak wajar: 24 digit setelah 62 (nomor HP Indonesia 9-12 digit, mis. 0812-0000-1234)
! baris 6: nama kosong
Catatan: Baris 5: Nomor 0210-000-3005 bukan nomor HP (mungkin telepon kantor); pastikan nomor ini memakai WhatsApp.
Catatan: Kolom diabaikan: Middle Name, Phonetic First Name, Phonetic Middle Name, Phonetic Last Name, Name Prefix, Name Suffix, Nickname, File As dan 10 lainnya.

Simpan? Jalankan perintah yang sama + --ya setelah pengguna setuju.
[kode keluar 0]

$ [2026-09-21] crm.py impor <uji>/csv/google-baru.csv --sumber-default referensi --ya
TERSIMPAN.
Impor google-baru.csv: 6 baris dibaca.
Kolom dikenali: catatan <- 'Notes', label <- 'Labels', wa <- 'Phone 1 - Value'
Kontak baru: 3 | Duplikat dilewati: 1 | Baris bermasalah dilewati: 2
+ K0001 Rina Susanti | 0812-****-3001 | baru | Referensi
+ K0002 Agus | 0812-****-3002 | baru | Referensi
+ K0003 Bu Endang | 0210-****-3005 | baru | Referensi
= baris 7 Doni: sudah ada (baris 2 di file ini)
! baris 4: Nomor '+62 812-0000-3003 ::: +62 813-0000-3004' tidak wajar: 24 digit setelah 62 (nomor HP Indonesia 9-12 digit, mis. 0812-0000-1234)
! baris 6: nama kosong
Catatan: Baris 5: Nomor 0210-000-3005 bukan nomor HP (mungkin telepon kantor); pastikan nomor ini memakai WhatsApp.
Catatan: Kolom diabaikan: Middle Name, Phonetic First Name, Phonetic Middle Name, Phonetic Last Name, Name Prefix, Name Suffix, Nickname, File As dan 10 lainnya.
Cadangan sebelum perubahan: <uji>/s03/backup-crm/crm-20260921-090000-impor.db
[kode keluar 0]

$ [2026-09-21] crm.py impor <uji>/csv/google-lama.csv --sumber-default fb --ya
TERSIMPAN.
Impor google-lama.csv: 2 baris dibaca.
Kolom dikenali: nama <- 'Name', catatan <- 'Notes', wa <- 'Phone 1 - Value'
Kontak baru: 2 | Duplikat dilewati: 0 | Baris bermasalah dilewati: 0
+ K0004 Siska Reseller Bogor | 0812-****-3008 | baru | Facebook
+ K0005 Pak Heru Grosir | 0812-****-3009 | baru | Facebook
Catatan: Kolom diabaikan: Additional Name, Yomi Name, Given Name Yomi, Additional Name Yomi, Family Name Yomi, Name Prefix, Name Suffix, Initials dan 18 lainnya.
Cadangan sebelum perubahan: <uji>/s03/backup-crm/crm-20260921-090000-impor-2.db
[kode keluar 0]

$ [2026-09-21] crm.py impor <uji>/csv/wa-ekspor.csv --sumber-default wa
PRATINJAU (belum disimpan):
Impor wa-ekspor.csv: 4 baris dibaca.
Kolom dikenali: nama <- 'Name', label <- 'Label'
Kontak baru: 3 | Duplikat dilewati: 0 | Baris bermasalah dilewati: 1
+ (baru) Mbak Tari | - | baru | WhatsApp langsung
+ (baru) ~ Yuni Olshop | - | baru | WhatsApp langsung
+ (baru) Mas Bagus | - | baru | WhatsApp langsung
! baris 4: nama kosong
Catatan: Kolom diabaikan: Number.

Simpan? Jalankan perintah yang sama + --ya setelah pengguna setuju.
[kode keluar 0]

$ [2026-09-21] crm.py impor <uji>/csv/wa-ekspor-nomor.csv --sumber-default wa
PRATINJAU (belum disimpan):
Impor wa-ekspor-nomor.csv: 2 baris dibaca.
Kolom dikenali: nama <- 'Nama', catatan <- 'Keterangan'
Kontak baru: 2 | Duplikat dilewati: 0 | Baris bermasalah dilewati: 0
+ (baru) Mbak Tari | - | baru | WhatsApp langsung
+ (baru) Kak Lia | - | baru | WhatsApp langsung
Catatan: Kolom diabaikan: Nomor.

Simpan? Jalankan perintah yang sama + --ya setelah pengguna setuju.
[kode keluar 0]

$ [2026-09-21] crm.py daftar --tahap semua
DAFTAR KONTAK (semua): 5 kontak
1. K0001 Rina Susanti | Referensi | Baru | FU 21 Sep (hari ini) | 0812-0000-3001
2. K0002 Agus | Referensi | Baru | FU 21 Sep (hari ini) | 0812-0000-3002
3. K0003 Bu Endang | Referensi | Baru | FU 21 Sep (hari ini) | 0210-000-3005
4. K0004 Siska Reseller Bogor | Facebook | Baru | FU 21 Sep (hari ini) | 0812-0000-3008
5. K0005 Pak Heru Grosir | Facebook | Baru | FU 21 Sep (hari ini) | 0812-0000-3009
Total nilai yang ditampilkan: Rp 0
[kode keluar 0]

$ [2026-09-21] crm.py hari-ini --tanpa-draf
FOLLOW-UP CRM - Senin, 21 September 2026 (WIB)
Terlambat: 0 | Hari ini: 5 | Besok: 0 | Belum dijadwalkan: 0
Nilai prospek yang perlu disapa: Rp 0

HARI INI (5)
1. K0001 Rina Susanti | Referensi | Baru | FU 21 Sep (hari ini) | 0812-0000-3001
   Catatan terakhir 21 Sep: "reseller Bekasi"
2. K0002 Agus | Referensi | Baru | FU 21 Sep (hari ini) | 0812-0000-3002
3. K0003 Bu Endang | Referensi | Baru | FU 21 Sep (hari ini) | 0210-000-3005
4. K0004 Siska Reseller Bogor | Facebook | Baru | FU 21 Sep (hari ini) | 0812-0000-3008
5. K0005 Pak Heru Grosir | Facebook | Baru | FU 21 Sep (hari ini) | 0812-0000-3009

Balas misalnya: "terkirim K0001", "Bu Rina deal 4,2 jt", "tunda K0002 ke Senin", "K0003 batal, kemahalan".
[kode keluar 0]

$ [2026-09-21] crm.py terkirim --kontak Rina
Dicatat: pesan ke K0001 Rina Susanti sudah dikirim. Follow-up berikutnya: Rabu, 23 September 2026.
Catatan: Tahap otomatis naik dari baru ke dihubungi.
[kode keluar 0]

$ [2026-09-21] crm.py terkirim --kontak Agus
Dicatat: pesan ke K0002 Agus sudah dikirim. Follow-up berikutnya: Rabu, 23 September 2026.
Catatan: Tahap otomatis naik dari baru ke dihubungi.
[kode keluar 0]

$ [2026-09-21] crm.py catat --kontak Siska --tahap order --nilai 2,5 jt --isi ambil 50 pcs, transfer besok --followup besok
Dicatat K0004 Siska Reseller Bogor: catatan "ambil 50 pcs, transfer besok"; tahap baru -> deal; nilai Rp 2.500.000; follow-up Selasa, 22 September 2026.
Sekarang: Deal | nilai Rp 2.500.000 | follow-up Selasa, 22 September 2026
[kode keluar 0]

$ [2026-09-22] crm.py hari-ini --maks-draf 3
FOLLOW-UP CRM - Selasa, 22 September 2026 (WIB)
Terlambat: 2 | Hari ini: 1 | Besok: 2 | Belum dijadwalkan: 0
Nilai prospek yang perlu disapa: Rp 2.500.000

TERLAMBAT (2)
1. K0003 Bu Endang | Referensi | Baru | FU 21 Sep (telat 1 hari) | 0210-000-3005
2. K0005 Pak Heru Grosir | Facebook | Baru | FU 21 Sep (telat 1 hari) | 0812-0000-3009

HARI INI (1)
1. K0004 Siska Reseller Bogor | Facebook | Deal | Rp 2.500.000 | FU 22 Sep (hari ini) | 0812-0000-3008
   Catatan terakhir 21 Sep: "ambil 50 pcs, transfer besok"

BESOK (2)
1. K0001 Rina Susanti | Referensi | Dihubungi | FU 23 Sep | 0812-0000-3001
   Catatan terakhir 21 Sep: "reseller Bekasi"
2. K0002 Agus | Referensi | Dihubungi | FU 23 Sep | 0812-0000-3002

DRAF PESAN (periksa, lalu kirim sendiri lewat tautan; bot tidak mengirim apa pun)

K0003 Bu Endang [sapaan-awal]:
Halo Bu Endang, terima kasih sudah menghubungi Grosir Hijab Nisa. Saya Nisa. Ada yang bisa saya bantu? Kira-kira dibutuhkan untuk kapan ya?
https://wa.me/622100003005?text=Halo%20Bu%20Endang%2C%20terima%20kasih%20sudah%20menghubungi%20Grosir%20Hijab%20Nisa.%20Saya%20Nisa.%20Ada%20yang%20bisa%20saya%20bantu%3F%20Kira-kira%20dibutuhkan%20untuk%20kapan%20ya%3F

K0005 Pak Heru Grosir [sapaan-awal]:
Halo Pak Heru Grosir, terima kasih sudah menghubungi Grosir Hijab Nisa. Saya Nisa. Ada yang bisa saya bantu? Kira-kira dibutuhkan untuk kapan ya?
https://wa.me/6281200003009?text=Halo%20Pak%20Heru%20Grosir%2C%20terima%20kasih%20sudah%20menghubungi%20Grosir%20Hijab%20Nisa.%20Saya%20Nisa.%20Ada%20yang%20bisa%20saya%20bantu%3F%20Kira-kira%20dibutuhkan%20untuk%20kapan%20ya%3F

K0004 Siska Reseller Bogor [konfirmasi-order]:
Halo Kak Siska Reseller Bogor, saya Nisa dari Grosir Hijab Nisa. Terima kasih sudah memutuskan order dengan kami. Mohon dibantu konfirmasi detail pengiriman/jadwal dan pembayarannya ya. Kalau ada yang ingin diubah, kabari saya.
https://wa.me/6281200003008?text=Halo%20Kak%20Siska%20Reseller%20Bogor%2C%20saya%20Nisa%20dari%20Grosir%20Hijab%20Nisa.%20Terima%20kasih%20sudah%20memutuskan%20order%20dengan%20kami.%20Mohon%20dibantu%20konfirmasi%20detail%20pengiriman%2Fjadwal%20dan%20pembayarannya%20ya.%20Kalau%20ada%20yang%20ingin%20diubah%2C%20kabari%20saya.

Balas misalnya: "terkirim K0001", "Bu Rina deal 4,2 jt", "tunda K0002 ke Senin", "K0003 batal, kemahalan".
[kode keluar 0]

$ [2026-09-22] crm.py catat --kontak Siska --isi sudah transfer --tahap lunas
Dicatat K0004 Siska Reseller Bogor: catatan "sudah transfer"; tahap deal -> selesai; jadwal follow-up dihapus.
Sekarang: Selesai | nilai Rp 2.500.000 | tanpa jadwal follow-up
[kode keluar 0]

$ [2026-09-23] crm.py catat --kontak Rina --tahap ditawar --nilai 1,8 jt --isi minta harga reseller 30 pcs --followup Jumat
Dicatat K0001 Rina Susanti: catatan "minta harga reseller 30 pcs"; tahap dihubungi -> ditawar; nilai Rp 1.800.000; follow-up Jumat, 25 September 2026.
Sekarang: Ditawar | nilai Rp 1.800.000 | follow-up Jumat, 25 September 2026
[kode keluar 0]

$ [2026-09-23] crm.py catat --kontak Heru --tahap batal --alasan sudah beli di tempat lain
Dicatat K0005 Pak Heru Grosir: tahap baru -> batal (alasan: pilih penjual lain); jadwal follow-up dihapus.
Sekarang: Batal | tanpa jadwal follow-up
[kode keluar 0]

$ [2026-09-24] crm.py hari-ini --maks-draf 2
FOLLOW-UP CRM - Kamis, 24 September 2026 (WIB)
Terlambat: 2 | Hari ini: 0 | Besok: 1 | Belum dijadwalkan: 0
Nilai prospek yang perlu disapa: Rp 0

TERLAMBAT (2)
1. K0003 Bu Endang | Referensi | Baru | FU 21 Sep (telat 3 hari) | 0210-000-3005
2. K0002 Agus | Referensi | Dihubungi | FU 23 Sep (telat 1 hari) | 0812-0000-3002

BESOK (1)
1. K0001 Rina Susanti | Referensi | Ditawar | Rp 1.800.000 | FU 25 Sep | 0812-0000-3001
   Catatan terakhir 23 Sep: "minta harga reseller 30 pcs"

DRAF PESAN (periksa, lalu kirim sendiri lewat tautan; bot tidak mengirim apa pun)

K0003 Bu Endang [sapaan-awal]:
Halo Bu Endang, terima kasih sudah menghubungi Grosir Hijab Nisa. Saya Nisa. Ada yang bisa saya bantu? Kira-kira dibutuhkan untuk kapan ya?
https://wa.me/622100003005?text=Halo%20Bu%20Endang%2C%20terima%20kasih%20sudah%20menghubungi%20Grosir%20Hijab%20Nisa.%20Saya%20Nisa.%20Ada%20yang%20bisa%20saya%20bantu%3F%20Kira-kira%20dibutuhkan%20untuk%20kapan%20ya%3F

K0002 Agus [follow-up-1]:
Halo Kak Agus, saya Nisa dari Grosir Hijab Nisa. Menyambung obrolan kita sebelumnya, apakah masih ada yang ingin ditanyakan? Kalau berkenan, saya kirimkan foto atau detail tambahan supaya lebih mudah memilih.
https://wa.me/6281200003002?text=Halo%20Kak%20Agus%2C%20saya%20Nisa%20dari%20Grosir%20Hijab%20Nisa.%20Menyambung%20obrolan%20kita%20sebelumnya%2C%20apakah%20masih%20ada%20yang%20ingin%20ditanyakan%3F%20Kalau%20berkenan%2C%20saya%20kirimkan%20foto%20atau%20detail%20tambahan%20supaya%20lebih%20mudah%20memilih.

Balas misalnya: "terkirim K0001", "Bu Rina deal 4,2 jt", "tunda K0002 ke Senin", "K0003 batal, kemahalan".
[kode keluar 0]

$ [2026-09-24] crm.py ekspor --csv <uji>/s03/prospek-pengingat.csv --format pengingat
Ekspor 3 prospek aktif ke <uji>/s03/prospek-pengingat.csv (format pengingat-follow-up, TANPA nomor HP).
Di skill pengingat-follow-up, tambahkan per baris dengan perintah 'tambah' (lihat 'perintah_pengingat' di JSON). Jangan jalankan jadwal kedua skill untuk prospek yang sama, nanti pengingatnya dobel.
[kode keluar 0]

$ [2026-09-24] crm.py ekspor --csv <uji>/s03/kontak.csv
Ekspor 5 kontak ke <uji>/s03/kontak.csv (pemisah ';', UTF-8, aman dibuka di Excel).
File ini berisi nomor HP pelanggan (data pribadi). Data pelanggan (nomor HP) adalah data pribadi (UU 27/2022 PDP): simpan di komputer ini, jangan dibagikan ke grup, hapus bila pelanggan meminta.
[kode keluar 0]

$ [2026-09-24] crm.py ekspor --csv <uji>/s03/kontak-samar.csv --samarkan
Ekspor 5 kontak ke <uji>/s03/kontak-samar.csv (pemisah ';', UTF-8, aman dibuka di Excel).
[kode keluar 0]

$ [2026-09-24] crm.py impor <uji>/s03/kontak.csv
PRATINJAU (belum disimpan):
Impor kontak.csv: 5 baris dibaca.
Kolom dikenali: nama <- 'nama', wa <- 'no_wa', sumber <- 'sumber', label <- 'label', tahap <- 'tahap', nilai <- 'nilai', kebutuhan <- 'kebutuhan', followup <- 'followup', alasan_batal <- 'alasan_batal', tgl_masuk <- 'tgl_masuk'
Kontak baru: 0 | Duplikat dilewati: 5 | Baris bermasalah dilewati: 0
= baris 2 Rina Susanti: sudah ada (K0001 Rina Susanti)
= baris 3 Agus: sudah ada (K0002 Agus)
= baris 4 Bu Endang: sudah ada (K0003 Bu Endang)
= baris 5 Siska Reseller Bogor: sudah ada (K0004 Siska Reseller Bogor)
= baris 6 Pak Heru Grosir: sudah ada (K0005 Pak Heru Grosir)

Simpan? Jalankan perintah yang sama + --ya setelah pengguna setuju.
[kode keluar 0]

$ [2026-09-24] crm.py daftar --label reseller
DAFTAR KONTAK (aktif, label reseller): 0 kontak
(kosong)
[kode keluar 0]

$ [2026-09-24] crm.py cek-duplikat
CEK DUPLIKAT: 5 kontak diperiksa
Tidak ada duplikat.
[kode keluar 0]

$ [2026-09-24] crm.py rekap --periode minggu-ini
REKAP CRM Grosir Hijab Nisa - minggu ini (21 Sep 2026 - 27 Sep 2026)
Data per Kamis, 24 September 2026 WIB

POSISI SAAT INI (semua kontak)
- Baru      :   1 kontak | Rp 0
- Dihubungi :   1 kontak | Rp 0
- Ditawar   :   1 kontak | Rp 1.800.000
- Deal      :   0 kontak | Rp 0
- Selesai   :   1 kontak | Rp 2.500.000
- Batal     :   1 kontak
Pipeline terbuka (baru+dihubungi+ditawar): 3 kontak, Rp 1.800.000

PERIODE MINGGU INI
Lead masuk: 5
Deal baru: 1 senilai Rp 2.500.000
Rata-rata nilai deal: Rp 2.500.000 | Rata-rata lama closing: 0,0 hari
Batal: 1
Konversi lead periode ini: 1 dari 5 = 20,0% (3 masih berjalan, 1 batal)
Win rate (yang sudah diputuskan): 1 dari 2 = 50,0%

SUMBER LEAD (lead masuk periode ini)
1. Facebook: 2 lead, 1 deal (50,0%), Rp 2.500.000
2. Referensi: 3 lead, 0 deal (0,0%), Rp 0
Sumber terbaik: Facebook (nilai deal terbesar). Sampel kecil (<5 lead), jadikan petunjuk saja.

ALASAN BATAL: pilih penjual lain (1)

FOLLOW-UP SAAT INI: terlambat 2, hari ini 0, besok 1, belum dijadwalkan 0
Ketik "follow-up hari ini" untuk daftar & draf pesannya.
Catatan: periode ini masih baru; konversi akan naik bila lead yang masih berjalan jadi deal.

Rumus perhitungan: tambahkan --rumus.
[kode keluar 0]
```
</details>

<details><summary>File CSV uji</summary>

```text
## google-baru.csv
First Name,Middle Name,Last Name,Phonetic First Name,Phonetic Middle Name,Phonetic Last Name,Name Prefix,Name Suffix,Nickname,File As,Organization Name,Organization Title,Organization Department,Birthday,Notes,Photo,Labels,E-mail 1 - Label,E-mail 1 - Value,Phone 1 - Label,Phone 1 - Value,Phone 2 - Label,Phone 2 - Value
Rina,,Susanti,,,,,,,,,,,,reseller Bekasi,,* myContacts ::: Reseller,,,Mobile,+62 812-0000-3001,,
Agus,,,,,,,,,,Toko Agus Jaya,,,,,,* myContacts ::: Reseller,,,Mobile,0812-0000-3002,,
Wati,,Lestari,,,,,,,,,,,,,,* myContacts,,,Mobile,+62 812-0000-3003 ::: +62 813-0000-3004,,
Bu Endang,,,,,,,,,,,,,,,,* myContacts ::: Reseller,,,Home,021-0000-3005,Mobile,0812-0000-3006
,,,,,,,,,,,,,,,,* myContacts,,,Mobile,0812-0000-3007,,
Doni,,,,,,,,,,,,,,,,* myContacts ::: Reseller,,,Mobile,0812-0000-3001,,
## google-lama.csv
Name,Given Name,Additional Name,Family Name,Yomi Name,Given Name Yomi,Additional Name Yomi,Family Name Yomi,Name Prefix,Name Suffix,Initials,Nickname,Short Name,Maiden Name,Birthday,Gender,Location,Billing Information,Directory Server,Mileage,Occupation,Hobby,Sensitivity,Priority,Subject,Notes,Language,Photo,Group Membership,Phone 1 - Type,Phone 1 - Value
Siska Reseller Bogor,Siska,,,,,,,,,,,,,,,,,,,,,,,,,,,* myContacts,Mobile,+6281200003008
Pak Heru Grosir,Heru,,,,,,,,,,,,,,,,,,,,,,,,,,,* myContacts,Mobile,081200003009
## wa-ekspor.csv
Name,Number,Label
Mbak Tari,6281200003010,Reseller
~ Yuni Olshop,6281200003011,
,6281200003012,
Mas Bagus,6281200003013,Pelanggan baru
## wa-ekspor-nomor.csv
Nama;Nomor;Keterangan
Mbak Tari;081200003010;reseller Depok
Kak Lia;081200003014;tanya harga grosir
```
</details>
