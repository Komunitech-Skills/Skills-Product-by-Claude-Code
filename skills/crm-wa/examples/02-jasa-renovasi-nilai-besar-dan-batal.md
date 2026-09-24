# 02 — Jasa renovasi: nilai proyek besar, batal beralasan, deal yang dibatalkan (normal)

- **Data fiktif:** "Bangun Rapi Renovasi", zona **WITA**, sapaan default "Bapak", 7 prospek Agustus–September 2026 (0813-0000-20xx, satu nomor kantor 0411).
- **Hasil: LULUS** (angka 100% cocok di 3 periode), temuan S1 muncul lebih parah (deal besar tampil "telat 38 hari").

## Yang diuji & hasil
| Kasus | Hasil |
|---|---|
| Nilai `85 jt`, `1,2 M`, `Rp 245.000.000,-`, `37 jt 500 rb`, `48,75 jt` | Rp85.000.000 / Rp1.200.000.000 / Rp245.000.000 / Rp37.500.000 / Rp48.750.000 ✔ |
| Nomor kantor `(0411) 000-2002` | diterima + peringatan "bukan nomor HP" ✔ (tampilan "0411-000-2002" oke) |
| Nama lembaga "PT Maju Bersama", "CV Sinar Jaya" | draf "Halo **Bapak/Ibu di** CV Sinar Jaya" ✔; "Dr. Andi" dipakai apa adanya ✔ |
| Ditawar → deal dengan nilai final 80 jt (RAB 85 jt, ditawar 78) | nilai deal = 80 jt; draf tidak menyebut angka ✔ |
| Batal "pilih vendor lain", "belum ada dana", "klien pindah kota, batal order" | 2 dibakukan, 1 disimpan apa adanya ✔; alasan wajib ✔ |
| Pak Rudi deal 8/9 (`--tanggal kemarin`) lalu batal 15/9 | tanggal deal dihapus, tidak dihitung deal September ✔ + peringatan jelas |
| "Senin depan" diucapkan Sabtu 15/8 | Senin 17/8 + catatan "kalau maksudnya minggu berikutnya, sebut tanggalnya" ✔ |
| Irama follow-up Ibu Maya: sapaan → FU-1 (+3) → pilihan-mudah (+4) → **pamit** → stop + saran batal "tidak ada respon" | sesuai tabel perintah.md ✔. `terkirim` ke-4 setelah pamit tetap diterima (hanya peringatan) — rendah. |
| Selesai → `terkirim` ucapan terima kasih → `--berikutnya "30 hari lagi"` (tawaran ulang) | 22 Okt ✔ |
| `draf` untuk kontak batal | ditolak dengan alasan ✔ |
| Zona WITA | judul "(WITA)", `info` memperingatkan beda jam komputer ✔ |

## Verifikasi angka independen
Agustus:
```
lead_masuk     OK    hitung-sendiri=5  script=5
deal_jumlah    OK    hitung-sendiri=2  script=2
deal_nilai     OK    hitung-sendiri=320000000  script=320000000
rata_nilai     OK    hitung-sendiri=160000000  script=160000000
rata_hari      OK    hitung-sendiri=14.5  script=14.5
batal_periode  OK    hitung-sendiri=2  script=2
konversi       OK    hitung-sendiri=40.0  script=40.0
win_rate       OK    hitung-sendiri=50.0  script=50.0
sumber         OK    hitung-sendiri={'Website/Google': [1, 1, 80000000], 'Pameran/Event': [1, 0, 0], 'Referensi': [1, 1, 240000000], 'Iklan': [1, 0, 0], 'Instagram': [1, 0, 0]}  script={'Referensi': [1, 1, 240000000], 'Website/Google': [1, 1, 80000000], 'Iklan': [1, 0, 0], 'Instagram': [1, 0, 0], 'Pameran/Event': [1, 0, 0]}
terbaik        OK    hitung-sendiri=Referensi  script=Referensi
posisi         OK    hitung-sendiri={'selesai': [1, 80000000], 'batal': [3, 1255500000], 'deal': [2, 560000000], 'dihubungi': [1, 48750000]}  script={'dihubungi': [1, 48750000], 'deal': [2, 560000000], 'selesai': [1, 80000000], 'batal': [3, 1255500000]}
nomor HP (62xxxxxxxxx / 08xx) di rekap --json: tidak ada
nama kontak di rekap --json: tidak ada
TOTAL BEDA: 0
```
September: TOTAL BEDA: 0. Semua waktu: TOTAL BEDA: 0.
Cek tangan "semua waktu": lama closing Gunawan 3/8→14/8 = 11, Fitri 10/8→28/8 = 18, Sinar Jaya 2/9→10/9 = 8 → 37/3 = 12,33 → **12,3** ✔; rata nilai 640 jt/3 = 213.333.333,3 → **Rp213.333.333** ✔; konversi 3/7 = 42,857% → **42,9%** ✔; win rate 3/6 = 50,0% ✔.

## Temuan
- **S1 (sedang), paling terasa di usaha jasa:** Bu Fitri deal 28/8 (Rp240 jt) tetap membawa jadwal pra-deal 17/8 → `hari-ini` 24/9: "FU 17 Agu (**telat 38 hari**)" dengan draf konfirmasi-order yang menanyakan "detail pengiriman/jadwal dan pembayarannya". CV Sinar Jaya sama (telat 20 hari). "Nilai prospek yang perlu disapa: Rp560.000.000" seluruhnya deal yang sudah menang.
- Rendah: alasan batal bebas ("klien pindah kota, batal order") diteruskan apa adanya ke `rekap --json` yang berlabel `data_sensitif: false`; bila pemilik menulis nama di alasan, nama ikut keluar.
- Kosmetik: draf konfirmasi-order generik ("pengiriman") kurang pas untuk jasa renovasi, tapi masih wajar.

## Transkrip asli
<details><summary>Keluaran lengkap crm.py</summary>

```text
$ [2026-08-03] crm.py init --nama-usaha Bangun Rapi Renovasi --pengirim Hadi --sapaan Bapak --zona WITA --ya
TERSIMPAN. Database CRM siap.
Database CRM baru: <uji>/s02/crm.db
Nama usaha: Bangun Rapi Renovasi | Pengirim draf: Hadi | Sapaan default: Bapak | Zona: WITA
Cadangan otomatis: <uji>/s02/backup-crm
[kode keluar 0]

$ [2026-08-03] crm.py tambah --nama Pak Gunawan --wa 0813-0000-2001 --sumber google maps --kebutuhan renovasi dapur + kanopi --nilai 85 jt --label survey, makassar
Tersimpan K0001: Pak Gunawan | 0813-0000-2001 | Baru | sumber Website/Google | nilai Rp 85.000.000 | follow-up Senin, 3 Agustus 2026 | label: survey, makassar
Catatan: Follow-up belum disebut; dijadwalkan hari ini (lead baru sebaiknya dibalas hari yang sama).
[kode keluar 0]

$ [2026-08-05] crm.py tambah --nama PT Maju Bersama --wa (0411) 000-2002 --sumber pameran --kebutuhan renovasi kantor lantai 2 --nilai 1,2 M
Tersimpan K0002: PT Maju Bersama | 0411-000-2002 | Baru | sumber Pameran/Event | nilai Rp 1.200.000.000 | follow-up Rabu, 5 Agustus 2026
Catatan: Nomor 0411-000-2002 bukan nomor HP (mungkin telepon kantor); pastikan nomor ini memakai WhatsApp.
Catatan: Follow-up belum disebut; dijadwalkan hari ini (lead baru sebaiknya dibalas hari yang sama).
[kode keluar 0]

$ [2026-08-10] crm.py tambah --nama Bu Fitri --wa +62 813-0000-2003 --sumber referensi --kebutuhan tambah kamar lantai 2 --nilai Rp 245.000.000,-
Tersimpan K0003: Bu Fitri | 0813-0000-2003 | Baru | sumber Referensi | nilai Rp 245.000.000 | follow-up Senin, 10 Agustus 2026
Catatan: Follow-up belum disebut; dijadwalkan hari ini (lead baru sebaiknya dibalas hari yang sama).
[kode keluar 0]

$ [2026-08-12] crm.py tambah --nama Dr. Andi --wa 0813 0000 2004 --sumber iklan --kebutuhan pagar & carport --nilai 37 jt 500 rb
Tersimpan K0004: Dr. Andi | 0813-0000-2004 | Baru | sumber Iklan | nilai Rp 37.500.000 | follow-up Rabu, 12 Agustus 2026
Catatan: Follow-up belum disebut; dijadwalkan hari ini (lead baru sebaiknya dibalas hari yang sama).
[kode keluar 0]

$ [2026-08-20] crm.py tambah --nama Ibu Maya --wa 081300002005 --sumber ig --kebutuhan kamar mandi 2 unit --nilai 48,75 jt
Tersimpan K0005: Ibu Maya | 0813-0000-2005 | Baru | sumber Instagram | nilai Rp 48.750.000 | follow-up Kamis, 20 Agustus 2026
Catatan: Follow-up belum disebut; dijadwalkan hari ini (lead baru sebaiknya dibalas hari yang sama).
[kode keluar 0]

$ [2026-08-06] crm.py catat --kontak Gunawan --tahap ditawar --isi survey selesai, RAB dikirim 85jt, minta 78 --nilai 78 jt --followup 10/8
Dicatat K0001 Pak Gunawan: catatan "survey selesai, RAB dikirim 85jt, minta 78"; tahap baru -> ditawar; nilai Rp 78.000.000; follow-up Senin, 10 Agustus 2026.
Sekarang: Ditawar | nilai Rp 78.000.000 | follow-up Senin, 10 Agustus 2026
[kode keluar 0]

$ [2026-08-14] crm.py catat --kontak Gunawan --tahap deal --isi sepakat 80 jt, DP 30% --nilai 80 jt --followup 3 hari lagi
Dicatat K0001 Pak Gunawan: catatan "sepakat 80 jt, DP 30%"; tahap ditawar -> deal; nilai Rp 80.000.000; follow-up Senin, 17 Agustus 2026.
Sekarang: Deal | nilai Rp 80.000.000 | follow-up Senin, 17 Agustus 2026
[kode keluar 0]

$ [2026-08-08] crm.py catat --kontak PT Maju --tahap ditawar --isi presentasi ke GA --followup 2 minggu lagi
Dicatat K0002 PT Maju Bersama: catatan "presentasi ke GA"; tahap baru -> ditawar; follow-up Sabtu, 22 Agustus 2026.
Sekarang: Ditawar | nilai Rp 1.200.000.000 | follow-up Sabtu, 22 Agustus 2026
[kode keluar 0]

$ [2026-08-25] crm.py catat --kontak PT Maju --tahap batal --alasan pilih vendor lain --isi kalah tender, beda 8%
Dicatat K0002 PT Maju Bersama: catatan "kalah tender, beda 8%"; tahap ditawar -> batal (alasan: pilih penjual lain); jadwal follow-up dihapus.
Sekarang: Batal | nilai Rp 1.200.000.000 | tanpa jadwal follow-up
[kode keluar 0]

$ [2026-08-15] crm.py catat --kontak Fitri --tahap nego --followup Senin depan
Dicatat K0003 Bu Fitri: tahap baru -> ditawar; follow-up Senin, 17 Agustus 2026.
Sekarang: Ditawar | nilai Rp 245.000.000 | follow-up Senin, 17 Agustus 2026
Catatan: "Senin depan" diartikan Senin terdekat (17 Agu 2026). Kalau maksudnya minggu berikutnya, sebut tanggalnya.
[kode keluar 0]

$ [2026-08-28] crm.py catat --kontak Fitri --tahap closing --isi OK 240jt, termin 3x --nilai 240 jt
Dicatat K0003 Bu Fitri: catatan "OK 240jt, termin 3x"; tahap ditawar -> deal; nilai Rp 240.000.000.
Sekarang: Deal | nilai Rp 240.000.000 | follow-up Senin, 17 Agustus 2026
[kode keluar 0]

$ [2026-08-18] crm.py catat --kontak Andi --tahap batal --alasan belum ada dana
Dicatat K0004 Dr. Andi: tahap baru -> batal (alasan: belum ada dana); jadwal follow-up dihapus.
Sekarang: Batal | nilai Rp 37.500.000 | tanpa jadwal follow-up
[kode keluar 0]

$ [2026-08-22] crm.py terkirim --kontak Maya
Dicatat: pesan ke K0005 Ibu Maya sudah dikirim. Follow-up berikutnya: Senin, 24 Agustus 2026.
Catatan: Tahap otomatis naik dari baru ke dihubungi.
[kode keluar 0]

$ [2026-08-27] crm.py terkirim --kontak Maya
Dicatat: pesan ke K0005 Ibu Maya sudah dikirim. Follow-up berikutnya: Minggu, 30 Agustus 2026.
[kode keluar 0]

$ [2026-08-31] crm.py terkirim --kontak Maya
Dicatat: pesan ke K0005 Ibu Maya sudah dikirim. Follow-up berikutnya: Jumat, 4 September 2026.
[kode keluar 0]

$ [2026-09-04] crm.py draf --kontak Maya
Draf untuk K0005 Ibu Maya (pamit) - periksa dulu, lalu kirim sendiri:
Halo Ibu Maya, saya Hadi dari Bangun Rapi Renovasi. Saya tidak ingin mengganggu, jadi ini pesan terakhir dari saya soal kamar mandi 2 unit. Kalau suatu saat butuh, tinggal chat nomor ini ya. Terima kasih atas waktunya.
Buka tautan ini, periksa pesannya, lalu tekan Kirim:
https://wa.me/6281300002005?text=Halo%20Ibu%20Maya%2C%20saya%20Hadi%20dari%20Bangun%20Rapi%20Renovasi.%20Saya%20tidak%20ingin%20mengganggu%2C%20jadi%20ini%20pesan%20terakhir%20dari%20saya%20soal%20kamar%20mandi%202%20unit.%20Kalau%20suatu%20saat%20butuh%2C%20tinggal%20chat%20nomor%20ini%20ya.%20Terima%20kasih%20atas%20waktunya.
Setelah terkirim, balas: "terkirim K0005".
[kode keluar 0]

$ [2026-09-04] crm.py terkirim --kontak Maya
Dicatat: pesan ke K0005 Ibu Maya sudah dikirim. Tidak ada jadwal follow-up berikutnya.
Catatan: Sudah 3 pesan follow-up tanpa kemajuan (terakhir pesan pamit). Jadwal dihentikan. Jika tetap tidak ada balasan, tandai batal: crm.py catat --kontak K0005 --tahap batal --alasan "tidak ada respon".
[kode keluar 0]

$ [2026-09-04] crm.py terkirim --kontak Maya
Dicatat: pesan ke K0005 Ibu Maya sudah dikirim. Tidak ada jadwal follow-up berikutnya.
Catatan: Sudah 4 pesan follow-up tanpa kemajuan (terakhir pesan pamit). Jadwal dihentikan. Jika tetap tidak ada balasan, tandai batal: crm.py catat --kontak K0005 --tahap batal --alasan "tidak ada respon".
[kode keluar 0]

$ [2026-09-02] crm.py tambah --nama CV Sinar Jaya --wa 0813-0000-2006 --sumber website --kebutuhan gudang baja ringan --nilai 320 jt --tahap ditawar
Tersimpan K0006: CV Sinar Jaya | 0813-0000-2006 | Ditawar | sumber Website/Google | nilai Rp 320.000.000 | follow-up Jumat, 4 September 2026
Catatan: Follow-up belum disebut; dijadwalkan 4 Sep 2026 (2 hari lagi). Ubah bila perlu.
[kode keluar 0]

$ [2026-09-07] crm.py tambah --nama Pak Rudi --wa 0813-0000-2007 --sumber referensi --kebutuhan cat ulang rumah --nilai 18 jt --masuk 1/9
Tersimpan K0007: Pak Rudi | 0813-0000-2007 | Baru | sumber Referensi | nilai Rp 18.000.000 | follow-up Senin, 7 September 2026
Catatan: Follow-up belum disebut; dijadwalkan hari ini (lead baru sebaiknya dibalas hari yang sama).
[kode keluar 0]

$ [2026-09-09] crm.py catat --kontak Rudi --tahap deal --tanggal kemarin
Dicatat K0007 Pak Rudi: tahap baru -> deal.
Sekarang: Deal | nilai Rp 18.000.000 | follow-up Senin, 7 September 2026
[kode keluar 0]

$ [2026-09-15] crm.py catat --kontak Rudi --tahap batal --alasan klien pindah kota, batal order --isi DP dikembalikan
Dicatat K0007 Pak Rudi: catatan "DP dikembalikan"; tahap deal -> batal (alasan: klien pindah kota, batal order); jadwal follow-up dihapus.
Sekarang: Batal | nilai Rp 18.000.000 | tanpa jadwal follow-up
Catatan: Kontak mundur dari deal ke batal; tanggal deal dihapus dari rekap.
[kode keluar 0]

$ [2026-09-10] crm.py catat --kontak Sinar Jaya --tahap deal --isi SPK ditandatangani
Dicatat K0006 CV Sinar Jaya: catatan "SPK ditandatangani"; tahap ditawar -> deal.
Sekarang: Deal | nilai Rp 320.000.000 | follow-up Jumat, 4 September 2026
[kode keluar 0]

$ [2026-09-20] crm.py catat --kontak Gunawan --tahap selesai --isi serah terima
Dicatat K0001 Pak Gunawan: catatan "serah terima"; tahap deal -> selesai; jadwal follow-up dihapus.
Sekarang: Selesai | nilai Rp 80.000.000 | tanpa jadwal follow-up
[kode keluar 0]

$ [2026-09-21] crm.py terkirim --kontak Gunawan
Dicatat: pesan ke K0001 Pak Gunawan sudah dikirim. Tidak ada jadwal follow-up berikutnya.
[kode keluar 0]

$ [2026-09-22] crm.py terkirim --kontak Gunawan --berikutnya 30 hari lagi
Dicatat: pesan ke K0001 Pak Gunawan sudah dikirim. Follow-up berikutnya: Kamis, 22 Oktober 2026.
[kode keluar 0]

$ [2026-09-24] crm.py hari-ini
FOLLOW-UP CRM - Kamis, 24 September 2026 (WITA)
Terlambat: 2 | Hari ini: 0 | Besok: 0 | Belum dijadwalkan: 1
Nilai prospek yang perlu disapa: Rp 560.000.000

TERLAMBAT (2)
1. K0003 Bu Fitri | Referensi | Deal | Rp 240.000.000 | tambah kamar lantai 2 | FU 17 Agu (telat 38 hari) | 0813-0000-2003
   Catatan terakhir 28 Agu: "OK 240jt, termin 3x"
2. K0006 CV Sinar Jaya | Website/Google | Deal | Rp 320.000.000 | gudang baja ringan | FU 4 Sep (telat 20 hari) | 0813-0000-2006
   Catatan terakhir 10 Sep: "SPK ditandatangani"

BELUM DIJADWALKAN (1)
1. K0005 Ibu Maya | Instagram | Dihubungi | Rp 48.750.000 | kamar mandi 2 unit | 0813-0000-2005

DRAF PESAN (periksa, lalu kirim sendiri lewat tautan; bot tidak mengirim apa pun)

K0003 Bu Fitri [konfirmasi-order]:
Halo Bu Fitri, saya Hadi dari Bangun Rapi Renovasi. Terima kasih sudah memutuskan order tambah kamar lantai 2. Mohon dibantu konfirmasi detail pengiriman/jadwal dan pembayarannya ya. Kalau ada yang ingin diubah, kabari saya.
https://wa.me/6281300002003?text=Halo%20Bu%20Fitri%2C%20saya%20Hadi%20dari%20Bangun%20Rapi%20Renovasi.%20Terima%20kasih%20sudah%20memutuskan%20order%20tambah%20kamar%20lantai%202.%20Mohon%20dibantu%20konfirmasi%20detail%20pengiriman%2Fjadwal%20dan%20pembayarannya%20ya.%20Kalau%20ada%20yang%20ingin%20diubah%2C%20kabari%20saya.

K0006 CV Sinar Jaya [konfirmasi-order]:
Halo Bapak/Ibu di CV Sinar Jaya, saya Hadi dari Bangun Rapi Renovasi. Terima kasih sudah memutuskan order gudang baja ringan. Mohon dibantu konfirmasi detail pengiriman/jadwal dan pembayarannya ya. Kalau ada yang ingin diubah, kabari saya.
https://wa.me/6281300002006?text=Halo%20Bapak%2FIbu%20di%20CV%20Sinar%20Jaya%2C%20saya%20Hadi%20dari%20Bangun%20Rapi%20Renovasi.%20Terima%20kasih%20sudah%20memutuskan%20order%20gudang%20baja%20ringan.%20Mohon%20dibantu%20konfirmasi%20detail%20pengiriman%2Fjadwal%20dan%20pembayarannya%20ya.%20Kalau%20ada%20yang%20ingin%20diubah%2C%20kabari%20saya.

Balas misalnya: "terkirim K0001", "Bu Rina deal 4,2 jt", "tunda K0002 ke Senin", "K0003 batal, kemahalan".
[kode keluar 0]

$ [2026-09-24] crm.py draf --kontak Sinar Jaya
Draf untuk K0006 CV Sinar Jaya (konfirmasi-order) - periksa dulu, lalu kirim sendiri:
Halo Bapak/Ibu di CV Sinar Jaya, saya Hadi dari Bangun Rapi Renovasi. Terima kasih sudah memutuskan order gudang baja ringan. Mohon dibantu konfirmasi detail pengiriman/jadwal dan pembayarannya ya. Kalau ada yang ingin diubah, kabari saya.
Buka tautan ini, periksa pesannya, lalu tekan Kirim:
https://wa.me/6281300002006?text=Halo%20Bapak%2FIbu%20di%20CV%20Sinar%20Jaya%2C%20saya%20Hadi%20dari%20Bangun%20Rapi%20Renovasi.%20Terima%20kasih%20sudah%20memutuskan%20order%20gudang%20baja%20ringan.%20Mohon%20dibantu%20konfirmasi%20detail%20pengiriman%2Fjadwal%20dan%20pembayarannya%20ya.%20Kalau%20ada%20yang%20ingin%20diubah%2C%20kabari%20saya.
Setelah terkirim, balas: "terkirim K0006".
[kode keluar 0]

$ [2026-09-24] crm.py draf --kontak PT Maju
GAGAL: Kontak berstatus batal; tidak perlu dihubungi. Pindahkan tahapnya dulu jika ingin menyapa lagi.
[kode keluar 1]

$ [2026-09-24] crm.py rekap --periode bulan-lalu
REKAP CRM Bangun Rapi Renovasi - bulan Agustus 2026 (1 Agu 2026 - 31 Agu 2026)
Data per Kamis, 24 September 2026 WITA

POSISI SAAT INI (semua kontak)
- Baru      :   0 kontak | Rp 0
- Dihubungi :   1 kontak | Rp 48.750.000
- Ditawar   :   0 kontak | Rp 0
- Deal      :   2 kontak | Rp 560.000.000
- Selesai   :   1 kontak | Rp 80.000.000
- Batal     :   3 kontak
Pipeline terbuka (baru+dihubungi+ditawar): 1 kontak, Rp 48.750.000

PERIODE BULAN AGUSTUS 2026
Lead masuk: 5
Deal baru: 2 senilai Rp 320.000.000
Rata-rata nilai deal: Rp 160.000.000 | Rata-rata lama closing: 14,5 hari
Batal: 2
Konversi lead periode ini: 2 dari 5 = 40,0% (1 masih berjalan, 2 batal)
Win rate (yang sudah diputuskan): 2 dari 4 = 50,0%

SUMBER LEAD (lead masuk periode ini)
1. Referensi: 1 lead, 1 deal (100,0%), Rp 240.000.000
2. Website/Google: 1 lead, 1 deal (100,0%), Rp 80.000.000
3. Iklan: 1 lead, 0 deal (0,0%), Rp 0
4. Instagram: 1 lead, 0 deal (0,0%), Rp 0
5. Pameran/Event: 1 lead, 0 deal (0,0%), Rp 0
Sumber terbaik: Referensi (nilai deal terbesar). Sampel kecil (<5 lead), jadikan petunjuk saja.

ALASAN BATAL: belum ada dana (1), pilih penjual lain (1)

FOLLOW-UP SAAT INI: terlambat 2, hari ini 0, besok 0, belum dijadwalkan 1
Ketik "follow-up hari ini" untuk daftar & draf pesannya.

Rumus perhitungan: tambahkan --rumus.
[kode keluar 0]

$ [2026-09-24] crm.py rekap --periode bulan-ini
REKAP CRM Bangun Rapi Renovasi - bulan September 2026 (1 Sep 2026 - 30 Sep 2026)
Data per Kamis, 24 September 2026 WITA

POSISI SAAT INI (semua kontak)
- Baru      :   0 kontak | Rp 0
- Dihubungi :   1 kontak | Rp 48.750.000
- Ditawar   :   0 kontak | Rp 0
- Deal      :   2 kontak | Rp 560.000.000
- Selesai   :   1 kontak | Rp 80.000.000
- Batal     :   3 kontak
Pipeline terbuka (baru+dihubungi+ditawar): 1 kontak, Rp 48.750.000

PERIODE BULAN SEPTEMBER 2026
Lead masuk: 2
Deal baru: 1 senilai Rp 320.000.000
Rata-rata nilai deal: Rp 320.000.000 | Rata-rata lama closing: 8,0 hari
Batal: 1
Konversi lead periode ini: 1 dari 2 = 50,0% (0 masih berjalan, 1 batal)
Win rate (yang sudah diputuskan): 1 dari 2 = 50,0%

SUMBER LEAD (lead masuk periode ini)
1. Website/Google: 1 lead, 1 deal (100,0%), Rp 320.000.000
2. Referensi: 1 lead, 0 deal (0,0%), Rp 0
Sumber terbaik: Website/Google (nilai deal terbesar). Sampel kecil (<5 lead), jadikan petunjuk saja.

ALASAN BATAL: klien pindah kota, batal order (1)

FOLLOW-UP SAAT INI: terlambat 2, hari ini 0, besok 0, belum dijadwalkan 1
Ketik "follow-up hari ini" untuk daftar & draf pesannya.

Rumus perhitungan: tambahkan --rumus.
[kode keluar 0]

$ [2026-09-24] crm.py rekap --periode semua
REKAP CRM Bangun Rapi Renovasi - semua waktu (semua data)
Data per Kamis, 24 September 2026 WITA

POSISI SAAT INI (semua kontak)
- Baru      :   0 kontak | Rp 0
- Dihubungi :   1 kontak | Rp 48.750.000
- Ditawar   :   0 kontak | Rp 0
- Deal      :   2 kontak | Rp 560.000.000
- Selesai   :   1 kontak | Rp 80.000.000
- Batal     :   3 kontak
Pipeline terbuka (baru+dihubungi+ditawar): 1 kontak, Rp 48.750.000

PERIODE SEMUA WAKTU
Lead masuk: 7
Deal baru: 3 senilai Rp 640.000.000
Rata-rata nilai deal: Rp 213.333.333 | Rata-rata lama closing: 12,3 hari
Batal: 3
Konversi lead periode ini: 3 dari 7 = 42,9% (1 masih berjalan, 3 batal)
Win rate (yang sudah diputuskan): 3 dari 6 = 50,0%

SUMBER LEAD (lead masuk periode ini)
1. Website/Google: 2 lead, 2 deal (100,0%), Rp 400.000.000
2. Referensi: 2 lead, 1 deal (50,0%), Rp 240.000.000
3. Iklan: 1 lead, 0 deal (0,0%), Rp 0
4. Instagram: 1 lead, 0 deal (0,0%), Rp 0
5. Pameran/Event: 1 lead, 0 deal (0,0%), Rp 0
Sumber terbaik: Website/Google (nilai deal terbesar). Sampel kecil (<5 lead), jadikan petunjuk saja.

ALASAN BATAL: belum ada dana (1), klien pindah kota, batal order (1), pilih penjual lain (1)

FOLLOW-UP SAAT INI: terlambat 2, hari ini 0, besok 0, belum dijadwalkan 1
Ketik "follow-up hari ini" untuk daftar & draf pesannya.
Catatan: periode ini masih baru; konversi akan naik bila lead yang masih berjalan jadi deal.

Rumus perhitungan: tambahkan --rumus.
[kode keluar 0]

$ [2026-09-24] crm.py info
CRM-WA 1.0.0
Database: <uji>/s02/crm.db
Usaha: Bangun Rapi Renovasi | Pengirim: Hadi | Sapaan: Bapak | Zona: WITA
Kontak: baru 0, dihubungi 1, ditawar 0, deal 2, selesai 1, batal 3 (total 7)
Pemeriksaan database: ok
Cadangan: 24 file di <uji>/s02/backup-crm
Terakhir: crm-20260922-090000-harian.db
Catatan: Jam komputer (13:43) berbeda dengan jam WITA (21:43). CRM tetap memakai jam WITA untuk 'hari ini' dan jadwal follow-up.
[kode keluar 0]
```
</details>
