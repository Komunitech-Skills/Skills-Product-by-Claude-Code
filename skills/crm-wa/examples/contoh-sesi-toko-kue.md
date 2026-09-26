# Contoh sesi: toko kue rumahan (data fiktif)

Keluaran **asli** `scripts/crm.py` 1.0.0, dijalankan pembuat skill pada 24 September 2026 dengan tanggal acuan
tetap (opsi uji `--hari-ini`, disembunyikan di bawah). Semua nama & nomor fiktif (`0812-0000-xxxx`).
Ini bukan hasil uji independen; hasil uji penguji terpisah akan disimpan di `examples/01-05` + `HASIL-UJI.md`.

Yang diperlihatkan: impor daftar lama (pratinjau → `--ya`), lead baru, nomor dobel ditolak, daftar follow-up +
draf + tautan wa.me, pemilik mengirim sendiri lalu `terkirim`, deal dengan nilai `4,275 jt`, batal wajib alasan,
versi disamarkan untuk dibagikan, dan rekap bulanan.

```text
### Kamis, 24 September 2026

$ python3 scripts/crm.py init --nama-usaha Dapur Bu Sari --pengirim Sari
PRATINJAU (belum dibuat):
Database CRM baru: ~/KomunitechData/crm/crm.db
Nama usaha: Dapur Bu Sari | Pengirim draf: Sari | Sapaan default: Kak | Zona: WIB
Cadangan otomatis: ~/KomunitechData/crm/backup-crm

Buat? Jalankan perintah yang sama + --ya setelah pengguna setuju.
[kode keluar 0]

$ python3 scripts/crm.py init --nama-usaha Dapur Bu Sari --pengirim Sari --ya
TERSIMPAN. Database CRM siap.
Database CRM baru: ~/KomunitechData/crm/crm.db
Nama usaha: Dapur Bu Sari | Pengirim draf: Sari | Sapaan default: Kak | Zona: WIB
Cadangan otomatis: ~/KomunitechData/crm/backup-crm
[kode keluar 0]

$ python3 scripts/crm.py impor kontak-lama.csv
PRATINJAU (belum disimpan):
Impor kontak-lama.csv: 5 baris dibaca.
Kolom dikenali: nama <- 'nama', wa <- 'no wa', sumber <- 'sumber', tahap <- 'tahap', nilai <- 'nilai', kebutuhan <- 'kebutuhan', label <- 'label', catatan <- 'catatan', followup <- 'follow up', tgl_masuk <- 'tgl masuk', alasan_batal <- 'alasan batal'
Kontak baru: 5 | Duplikat dilewati: 0 | Baris bermasalah dilewati: 0
+ (baru) Bu Rina | 0812-****-1001 | baru | Instagram
+ (baru) Pak Budi | 0812-****-1002 | ditawar | Referensi
+ (baru) Mbak Dewi | 0812-****-1003 | dihubungi | TikTok
+ (baru) Om Heru | 0812-****-1004 | deal | Walk-in
+ (baru) PT Contoh Sejahtera | 0812-****-1005 | batal | Website/Google

Simpan? Jalankan perintah yang sama + --ya setelah pengguna setuju.
[kode keluar 0]

$ python3 scripts/crm.py impor kontak-lama.csv --ya
TERSIMPAN.
Impor kontak-lama.csv: 5 baris dibaca.
Kolom dikenali: nama <- 'nama', wa <- 'no wa', sumber <- 'sumber', tahap <- 'tahap', nilai <- 'nilai', kebutuhan <- 'kebutuhan', label <- 'label', catatan <- 'catatan', followup <- 'follow up', tgl_masuk <- 'tgl masuk', alasan_batal <- 'alasan batal'
Kontak baru: 5 | Duplikat dilewati: 0 | Baris bermasalah dilewati: 0
+ K0001 Bu Rina | 0812-****-1001 | baru | Instagram
+ K0002 Pak Budi | 0812-****-1002 | ditawar | Referensi
+ K0003 Mbak Dewi | 0812-****-1003 | dihubungi | TikTok
+ K0004 Om Heru | 0812-****-1004 | deal | Walk-in
+ K0005 PT Contoh Sejahtera | 0812-****-1005 | batal | Website/Google
Cadangan sebelum perubahan: ~/KomunitechData/crm/backup-crm/crm-20260924-090000-impor.db
[kode keluar 0]

$ python3 scripts/crm.py tambah --nama Kak Nia --wa +62 812 0000 1006 --sumber ig --kebutuhan hampers lebaran 30 paket --nilai 6 jt
Tersimpan K0006: Kak Nia | 0812-0000-1006 | Baru | sumber Instagram | nilai Rp 6.000.000 | follow-up Kamis, 24 September 2026
Catatan: Follow-up belum disebut; dijadwalkan hari ini (lead baru sebaiknya dibalas hari yang sama).
[kode keluar 0]

$ python3 scripts/crm.py tambah --nama Nia --wa 081200001006 --sumber tiktok
GAGAL: Nomor 0812-0000-1006 sudah tersimpan sebagai K0006 Kak Nia (baru). Tidak ditambah dobel. Untuk mencatat obrolan baru pakai: crm.py catat --kontak K0006 --isi "...". Jika memang orang berbeda dengan nomor yang sama, ulangi dengan --izinkan-duplikat.
[kode keluar 1]

$ python3 scripts/crm.py hari-ini
FOLLOW-UP CRM - Kamis, 24 September 2026 (WIB)
Terlambat: 0 | Hari ini: 2 | Besok: 1 | Belum dijadwalkan: 0
Nilai prospek yang perlu disapa: Rp 6.450.000

HARI INI (2)
1. K0006 Kak Nia | Instagram | Baru | Rp 6.000.000 | hampers lebaran 30 paket | FU 24 Sep (hari ini) | 0812-0000-1006
2. K0001 Bu Rina | Instagram | Baru | Rp 450.000 | kue ulang tahun 2 tingkat | FU 24 Sep (hari ini) | 0812-0000-1001
   Catatan terakhir 24 Sep: "tanya harga via DM"

BESOK (1)
1. K0002 Pak Budi | Referensi | Ditawar | Rp 4.500.000 | katering 100 box | FU 25 Sep | 0812-0000-1002
   Catatan terakhir 24 Sep: "minta diskon 10%"

DRAF PESAN (periksa, lalu kirim sendiri lewat tautan; bot tidak mengirim apa pun)

K0006 Kak Nia [sapaan-awal]:
Halo Kak Nia, terima kasih sudah menghubungi Dapur Bu Sari. Saya Sari. Soal hampers lebaran 30 paket, boleh saya bantu jelaskan pilihan dan harganya? Kira-kira dibutuhkan untuk kapan ya?
https://wa.me/6281200001006?text=Halo%20Kak%20Nia%2C%20terima%20kasih%20sudah%20menghubungi%20Dapur%20Bu%20Sari.%20Saya%20Sari.%20Soal%20hampers%20lebaran%2030%20paket%2C%20boleh%20saya%20bantu%20jelaskan%20pilihan%20dan%20harganya%3F%20Kira-kira%20dibutuhkan%20untuk%20kapan%20ya%3F

K0001 Bu Rina [sapaan-awal]:
Halo Bu Rina, terima kasih sudah menghubungi Dapur Bu Sari. Saya Sari. Soal kue ulang tahun 2 tingkat, boleh saya bantu jelaskan pilihan dan harganya? Kira-kira dibutuhkan untuk kapan ya?
https://wa.me/6281200001001?text=Halo%20Bu%20Rina%2C%20terima%20kasih%20sudah%20menghubungi%20Dapur%20Bu%20Sari.%20Saya%20Sari.%20Soal%20kue%20ulang%20tahun%202%20tingkat%2C%20boleh%20saya%20bantu%20jelaskan%20pilihan%20dan%20harganya%3F%20Kira-kira%20dibutuhkan%20untuk%20kapan%20ya%3F

Balas misalnya: "terkirim K0001", "Bu Rina deal 4,2 jt", "tunda K0002 ke Senin", "K0003 batal, kemahalan".
[kode keluar 0]

$ python3 scripts/crm.py terkirim --kontak Bu Rina
Dicatat: pesan ke K0001 Bu Rina sudah dikirim. Follow-up berikutnya: Sabtu, 26 September 2026.
Catatan: Tahap otomatis naik dari baru ke dihubungi.
[kode keluar 0]

$ python3 scripts/crm.py terkirim --kontak Kak Nia
Dicatat: pesan ke K0006 Kak Nia sudah dikirim. Follow-up berikutnya: Sabtu, 26 September 2026.
Catatan: Tahap otomatis naik dari baru ke dihubungi.
[kode keluar 0]

### Jumat, 25 September 2026

$ python3 scripts/crm.py catat --kontak Pak Budi --isi setuju diskon 5%, DP besok --tahap deal --nilai 4,275 jt --followup besok
Dicatat K0002 Pak Budi: catatan "setuju diskon 5%, DP besok"; tahap ditawar -> deal; nilai Rp 4.275.000; follow-up Sabtu, 26 September 2026.
Sekarang: Deal | nilai Rp 4.275.000 | follow-up Sabtu, 26 September 2026
[kode keluar 0]

$ python3 scripts/crm.py catat --kontak Dewi --tahap batal
GAGAL: Tahap batal butuh alasan singkat (mis. harga terlalu mahal, tidak ada respon, pilih penjual lain, belum butuh). Tanyakan ke pengguna lalu isi --alasan.
[kode keluar 1]

$ python3 scripts/crm.py catat --kontak Dewi --tahap batal --alasan sudah beli di tempat lain
Dicatat K0003 Mbak Dewi: tahap dihubungi -> batal (alasan: pilih penjual lain); jadwal follow-up dihapus.
Sekarang: Batal | nilai Rp 350.000 | tanpa jadwal follow-up
[kode keluar 0]

$ python3 scripts/crm.py hari-ini --samarkan
FOLLOW-UP CRM - Sabtu, 26 September 2026 (WIB)
Terlambat: 0 | Hari ini: 3 | Besok: 0 | Belum dijadwalkan: 0
Nilai prospek yang perlu disapa: Rp 10.725.000

HARI INI (3)
1. K0006 Kak N. | Instagram | Dihubungi | Rp 6.000.000 | hampers lebaran 30 paket | FU 26 Sep (hari ini) | 0812-****-1006
2. K0002 Pak B. | Referensi | Deal | Rp 4.275.000 | katering 100 box | FU 26 Sep (hari ini) | 0812-****-1002
3. K0001 Bu R. | Instagram | Dihubungi | Rp 450.000 | kue ulang tahun 2 tingkat | FU 26 Sep (hari ini) | 0812-****-1001

DRAF PESAN (periksa, lalu kirim sendiri lewat tautan; bot tidak mengirim apa pun)

K0006 Kak N. [follow-up-1]:
Halo Kak N., saya Sari dari Dapur Bu Sari. Menyambung obrolan kita soal hampers lebaran 30 paket, apakah masih ada yang ingin ditanyakan? Kalau berkenan, saya kirimkan foto atau detail tambahan supaya lebih mudah memilih.
(tautan disembunyikan karena mode samarkan)

K0002 Pak B. [konfirmasi-order]:
Halo Pak B., saya Sari dari Dapur Bu Sari. Terima kasih sudah memutuskan order katering 100 box. Mohon dibantu konfirmasi detail pengiriman/jadwal dan pembayarannya ya. Kalau ada yang ingin diubah, kabari saya.
(tautan disembunyikan karena mode samarkan)

K0001 Bu R. [follow-up-1]:
Halo Bu R., saya Sari dari Dapur Bu Sari. Menyambung obrolan kita soal kue ulang tahun 2 tingkat, apakah masih ada yang ingin ditanyakan? Kalau berkenan, saya kirimkan foto atau detail tambahan supaya lebih mudah memilih.
(tautan disembunyikan karena mode samarkan)

Balas misalnya: "terkirim K0001", "Bu Rina deal 4,2 jt", "tunda K0002 ke Senin", "K0003 batal, kemahalan".
[kode keluar 0]

$ python3 scripts/crm.py rekap --bulan 2026-09
REKAP CRM Dapur Bu Sari - bulan September 2026 (1 Sep 2026 - 30 Sep 2026)
Data per Jumat, 25 September 2026 WIB

POSISI SAAT INI (semua kontak)
- Baru      :   0 kontak | Rp 0
- Dihubungi :   2 kontak | Rp 6.450.000
- Ditawar   :   0 kontak | Rp 0
- Deal      :   2 kontak | Rp 5.525.000
- Selesai   :   0 kontak | Rp 0
- Batal     :   2 kontak
Pipeline terbuka (baru+dihubungi+ditawar): 2 kontak, Rp 6.450.000

PERIODE BULAN SEPTEMBER 2026
Lead masuk: 6
Deal baru: 2 senilai Rp 5.525.000
Rata-rata nilai deal: Rp 2.762.500 | Rata-rata lama closing: 2,5 hari
Batal: 2
Konversi lead periode ini: 2 dari 6 = 33,3% (2 masih berjalan, 2 batal)
Win rate (yang sudah diputuskan): 2 dari 4 = 50,0%

SUMBER LEAD (lead masuk periode ini)
1. Referensi: 1 lead, 1 deal (100,0%), Rp 4.275.000
2. Walk-in: 1 lead, 1 deal (100,0%), Rp 1.250.000
3. Instagram: 2 lead, 0 deal (0,0%), Rp 0
4. TikTok: 1 lead, 0 deal (0,0%), Rp 0
5. Website/Google: 1 lead, 0 deal (0,0%), Rp 0
Sumber terbaik: Referensi (nilai deal terbesar). Sampel kecil (<5 lead), jadikan petunjuk saja.

ALASAN BATAL: harga terlalu mahal (1), pilih penjual lain (1)

FOLLOW-UP SAAT INI: terlambat 0, hari ini 0, besok 3, belum dijadwalkan 0
Catatan: periode ini masih baru; konversi akan naik bila lead yang masih berjalan jadi deal.

Rumus perhitungan: tambahkan --rumus.
[kode keluar 0]

```
