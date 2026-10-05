# 01 — Toko kue rumahan: 15 prospek dari IG/TikTok/referensi selama 2 minggu (normal)

- **Penguji:** agent penguji independen (bukan pembuat), simulasi Claude Code yang hanya membaca folder `crm-wa/`.
- **Data:** fiktif ("Dapur Mama Tia", nomor 0812-0000-10xx). DB di scratchpad (`--db`), `HOME` & `KOMUNITECH_DATA` palsu.
- **Cara:** tiap cerita pemilik diterjemahkan agent ke perintah sesuai SKILL.md Langkah B–E. Tanggal disimulasikan dengan opsi uji `--hari-ini` (10–24 Sep 2026).
- **Hasil: LULUS** (angka 100% cocok), dengan 2 temuan (S1 jadwal lama terbawa saat deal, S2 nama ambigu — lihat HASIL-UJI).

## Percakapan inti (ringkas)
| Pemilik bilang | Perintah agent (sesuai SKILL) | Hasil |
|---|---|---|
| "Catat Bu Rina dari IG, 0812-0000-1001, kue ultah 2 tingkat ±450rb, anaknya ultah 20/9" | `tambah --nama "Bu Rina" --wa ... --sumber ig --kebutuhan ... --nilai 450rb --catatan ...` | K0001, FU hari ini (asumsi disebut) |
| "Kak Nia +62 812 0000 1002 dari TikTok" | `tambah ... --wa "+62 812 0000 1002"` | disimpan 62812…, tampil 0812-0000-1002 |
| "Rina nawar jadi 400rb, follow-up besok" | `catat --kontak Rina --tahap nego --nilai 400rb --followup besok` | "nego" → Ditawar, besok = Sab 12 Sep |
| "Dewi batal, kemahalan" | `catat --kontak Dewi --tahap batal --alasan kemahalan` | alasan dibakukan "harga terlalu mahal" |
| "Bu Sari minta menu" (ada 2 Bu Sari) | `catat --kontak "Bu Sari" ...` | **ditolak ambigu** → agent tanya "Bu Sari yang mana: K0011 snack box arisan / K0014 kue pengantin?" ✔ |
| "Hari ini follow-up siapa?" (24 Sep) | `hari-ini` | 10 terlambat, 1 besok, 10 draf + tautan wa.me |
| "Sudah kukirim ke Kak Nia" | `terkirim --kontak K0002` | fu_ke 1 → FU +3 hari (27 Sep), draf berikutnya "pilihan-mudah" |
| "Rekap bulan ini" / "minggu lalu, rumusnya?" | `rekap` / `rekap --periode minggu-lalu --rumus` | lihat bawah |

## Verifikasi angka independen (query SQLite sendiri, `verif.py`, tanpa import crm.py)
Bulan September (1–30 Sep):
```
lead_masuk     OK    hitung-sendiri=15  script=15
deal_jumlah    OK    hitung-sendiri=5  script=5
deal_nilai     OK    hitung-sendiri=3875000  script=3875000
rata_nilai     OK    hitung-sendiri=775000  script=775000
rata_hari      OK    hitung-sendiri=2.6  script=2.6
batal_periode  OK    hitung-sendiri=3  script=3
konversi       OK    hitung-sendiri=33.3  script=33.3
win_rate       OK    hitung-sendiri=62.5  script=62.5
sumber         OK    hitung-sendiri={'Instagram': [6, 2, 1850000], 'TikTok': [4, 1, 175000], 'Referensi': [4, 2, 1850000], 'Walk-in': [1, 0, 0]}  script={'Referensi': [4, 2, 1850000], 'Instagram': [6, 2, 1850000], 'TikTok': [4, 1, 175000], 'Walk-in': [1, 0, 0]}
terbaik        OK    hitung-sendiri=Referensi  script=Referensi
posisi         OK    hitung-sendiri={'deal': [4, 2425000], 'dihubungi': [2, 725000], 'batal': [3, 2940000], 'selesai': [1, 1450000], 'ditawar': [1, 1100000], 'baru': [4, 5500000]}  script={'baru': [4, 5500000], 'dihubungi': [2, 725000], 'ditawar': [1, 1100000], 'deal': [4, 2425000], 'selesai': [1, 1450000], 'batal': [3, 2940000]}
nomor HP (62xxxxxxxxx / 08xx) di rekap --json: tidak ada
nama kontak di rekap --json: tidak ada
TOTAL BEDA: 0
```
Minggu lalu (14–20 Sep): TOTAL BEDA: 0. Hitung tangan: lead 4 (Hendra, Ratna, Dimas, Sari K0011); deal baru 2 (Lilis 17/9 Rp650.000 + Hendra 18/9 Rp1.200.000 = Rp1.850.000); lama closing (5+4)/2 = 4,5 hari; batal periode 2 (Dewi 14/9, Dimas 20/9; Sinta 13/9 tidak ikut) ✔.
Sumber terbaik bulan ini: Referensi dan Instagram **seri** Rp1.850.000 → pemecah seri konversi 50,0% > 33,3% → Referensi ✔ (sesuai rumus). "Nilai prospek yang perlu disapa" 24/9 = Rp8.650.000 = jumlah 10 kontak terlambat ✔.

## Pemeriksaan draf & tautan
- 33 tautan wa.me (s01–s03) di-*decode* ulang: host `wa.me`, path = nomor kontak di DB, `text` = draf persis, tidak ada spasi/koma/?/&/# mentah → **0 salah**.
- Draf tidak memuat nilai/harga dan tidak memuat isi catatan (catatan "anaknya ultah 20/9, suka coklat", "budget ketat" tidak muncul) ✔.
- `--samarkan`: nama → "Bu R.", nomor → 0812-****-1001, tautan disembunyikan ✔. Kosmetik: Bu Rina & Bu Ratna sama-sama "Bu R."; kalimat contoh statis di akhir ("Bu Rina deal 4,2 jt") kebetulan memuat nama kontak asli.

## Penilaian nada draf (bahasa Indonesia)
Sopan, tidak memaksa, natural ("Apa pun jawabannya tidak apa-apa", pesan pamit "Saya tidak ingin mengganggu"). Catatan: sapaan-awal untuk lead yang **sudah telat 5 hari** tetap berbunyi "terima kasih sudah menghubungi…" tanpa "maaf baru membalas"; "Terima kasih sudah memutuskan order" agak kaku; konfirmasi-order menanyakan pembayaran padahal catatan "DP 50% sudah transfer" (wajar karena draf sengaja tidak membaca catatan pribadi — pemilik tetap memeriksa).

## Temuan dari skenario ini
- **S1 (sedang):** pindah ke deal tanpa `--followup` mempertahankan jadwal lama pra-deal. Pak Anton deal 12/9 → "follow-up Jumat, 11 September" (sudah lewat); Om Hendra (ambil kue 26/9) muncul "telat 6 hari". Hasil 24/9: 5 dari 10 "TERLAMBAT" adalah deal yang sudah menang, dan "Nilai prospek yang perlu disapa" ikut menjumlah deal.
- **S2 (sedang)** diuji lanjut di 04: bila salah satu "Bu Sari" batal, script memilih yang aktif **tanpa bertanya**.

## Transkrip asli
<details><summary>Keluaran lengkap crm.py (420 baris)</summary>

```text
$ [2026-09-10] crm.py info
Database CRM belum ada (lokasi: <uji>/s01/crm.db). Mulai dengan: crm.py init --nama-usaha "..." --pengirim "..." (pratinjau, lalu --ya).
[kode keluar 0]

$ [2026-09-10] crm.py init --nama-usaha Dapur Mama Tia --pengirim Tia --sapaan Kak
PRATINJAU (belum dibuat):
Database CRM baru: <uji>/s01/crm.db
Nama usaha: Dapur Mama Tia | Pengirim draf: Tia | Sapaan default: Kak | Zona: WIB
Cadangan otomatis: <uji>/s01/backup-crm

Buat? Jalankan perintah yang sama + --ya setelah pengguna setuju.
[kode keluar 0]

$ [2026-09-10] crm.py init --nama-usaha Dapur Mama Tia --pengirim Tia --sapaan Kak --ya
TERSIMPAN. Database CRM siap.
Database CRM baru: <uji>/s01/crm.db
Nama usaha: Dapur Mama Tia | Pengirim draf: Tia | Sapaan default: Kak | Zona: WIB
Cadangan otomatis: <uji>/s01/backup-crm
[kode keluar 0]

$ [2026-09-10] crm.py tambah --nama Bu Rina --wa 0812-0000-1001 --sumber ig --kebutuhan kue ulang tahun 2 tingkat --nilai 450rb --catatan anaknya ultah 20/9, suka coklat
Tersimpan K0001: Bu Rina | 0812-0000-1001 | Baru | sumber Instagram | nilai Rp 450.000 | follow-up Kamis, 10 September 2026
Catatan: Follow-up belum disebut; dijadwalkan hari ini (lead baru sebaiknya dibalas hari yang sama).
[kode keluar 0]

$ [2026-09-10] crm.py tambah --nama Kak Nia --wa +62 812 0000 1002 --sumber tiktok --kebutuhan brownies 5 loyang --nilai 375rb
Tersimpan K0002: Kak Nia | 0812-0000-1002 | Baru | sumber TikTok | nilai Rp 375.000 | follow-up Kamis, 10 September 2026
Catatan: Follow-up belum disebut; dijadwalkan hari ini (lead baru sebaiknya dibalas hari yang sama).
[kode keluar 0]

$ [2026-09-10] crm.py tambah --nama Mbak Dewi --wa 081200001003 --sumber dari teman --kebutuhan hampers 20 paket --nilai 2,4 jt --catatan kantor suaminya, budget ketat
Tersimpan K0003: Mbak Dewi | 0812-0000-1003 | Baru | sumber Referensi | nilai Rp 2.400.000 | follow-up Kamis, 10 September 2026
Catatan: Follow-up belum disebut; dijadwalkan hari ini (lead baru sebaiknya dibalas hari yang sama).
[kode keluar 0]

$ [2026-09-11] crm.py tambah --nama Pak Anton --wa 0812 0000 1004 --sumber ig --kebutuhan tumpeng mini 30 --nilai 1,5 jt
Tersimpan K0004: Pak Anton | 0812-0000-1004 | Baru | sumber Instagram | nilai Rp 1.500.000 | follow-up Jumat, 11 September 2026
Catatan: Follow-up belum disebut; dijadwalkan hari ini (lead baru sebaiknya dibalas hari yang sama).
[kode keluar 0]

$ [2026-09-11] crm.py tambah --nama Sinta --wa 6281200001005 --sumber tt --kebutuhan cupcake 24 pcs --nilai 240rb
Tersimpan K0005: Sinta | 0812-0000-1005 | Baru | sumber TikTok | nilai Rp 240.000 | follow-up Jumat, 11 September 2026
Catatan: Follow-up belum disebut; dijadwalkan hari ini (lead baru sebaiknya dibalas hari yang sama).
[kode keluar 0]

$ [2026-09-12] crm.py tambah --nama Bu Lilis --wa 0812-0000-1006 --sumber referensi --kebutuhan kue lapis legit --nilai 650rb
Tersimpan K0006: Bu Lilis | 0812-0000-1006 | Baru | sumber Referensi | nilai Rp 650.000 | follow-up Sabtu, 12 September 2026
Catatan: Follow-up belum disebut; dijadwalkan hari ini (lead baru sebaiknya dibalas hari yang sama).
[kode keluar 0]

$ [2026-09-12] crm.py tambah --nama Kak Yoga --wa 0812-0000-1007 --sumber ig --kebutuhan dessert box 10 --nilai 350rb
Tersimpan K0007: Kak Yoga | 0812-0000-1007 | Baru | sumber Instagram | nilai Rp 350.000 | follow-up Sabtu, 12 September 2026
Catatan: Follow-up belum disebut; dijadwalkan hari ini (lead baru sebaiknya dibalas hari yang sama).
[kode keluar 0]

$ [2026-09-14] crm.py tambah --nama Om Hendra --wa 0812-0000-1008 --sumber referensi --kebutuhan kue ulang tahun kantor 3 tingkat --nilai 1,2 jt
Tersimpan K0008: Om Hendra | 0812-0000-1008 | Baru | sumber Referensi | nilai Rp 1.200.000 | follow-up Senin, 14 September 2026
Catatan: Follow-up belum disebut; dijadwalkan hari ini (lead baru sebaiknya dibalas hari yang sama).
[kode keluar 0]

$ [2026-09-10] crm.py terkirim --kontak Bu Rina
Dicatat: pesan ke K0001 Bu Rina sudah dikirim. Follow-up berikutnya: Sabtu, 12 September 2026.
Catatan: Tahap otomatis naik dari baru ke dihubungi.
[kode keluar 0]

$ [2026-09-11] crm.py catat --kontak Rina --isi minta desain unicorn, tawar 400rb --tahap nego --nilai 400rb --followup besok
Dicatat K0001 Bu Rina: catatan "minta desain unicorn, tawar 400rb"; tahap dihubungi -> ditawar; nilai Rp 400.000; follow-up Sabtu, 12 September 2026.
Sekarang: Ditawar | nilai Rp 400.000 | follow-up Sabtu, 12 September 2026
[kode keluar 0]

$ [2026-09-12] crm.py catat --kontak K0001 --tahap jadi --isi DP 50% sudah transfer
Dicatat K0001 Bu Rina: catatan "DP 50% sudah transfer"; tahap ditawar -> deal.
Sekarang: Deal | nilai Rp 400.000 | follow-up Sabtu, 12 September 2026
[kode keluar 0]

$ [2026-09-11] crm.py catat --kontak Nia --tahap dihubungi --isi tanya harga, belum balas lagi
Dicatat K0002 Kak Nia: catatan "tanya harga, belum balas lagi"; tahap baru -> dihubungi; follow-up Minggu, 13 September 2026.
Sekarang: Dihubungi | nilai Rp 375.000 | follow-up Minggu, 13 September 2026
Catatan: Follow-up belum disebut; dijadwalkan 13 Sep 2026 (2 hari lagi). Ubah bila perlu.
[kode keluar 0]

$ [2026-09-12] crm.py catat --kontak Dewi --tahap ditawar --isi kirim penawaran 2,4jt --followup Senin
Dicatat K0003 Mbak Dewi: catatan "kirim penawaran 2,4jt"; tahap baru -> ditawar; follow-up Senin, 14 September 2026.
Sekarang: Ditawar | nilai Rp 2.400.000 | follow-up Senin, 14 September 2026
[kode keluar 0]

$ [2026-09-14] crm.py catat --kontak Dewi --tahap batal --alasan kemahalan --isi pilih yang 1,8jt
Dicatat K0003 Mbak Dewi: catatan "pilih yang 1,8jt"; tahap ditawar -> batal (alasan: harga terlalu mahal); jadwal follow-up dihapus.
Sekarang: Batal | nilai Rp 2.400.000 | tanpa jadwal follow-up
[kode keluar 0]

$ [2026-09-12] crm.py catat --kontak Anton --tahap order --nilai 1,45 jt --isi ambil 15/9
Dicatat K0004 Pak Anton: catatan "ambil 15/9"; tahap baru -> deal; nilai Rp 1.450.000.
Sekarang: Deal | nilai Rp 1.450.000 | follow-up Jumat, 11 September 2026
[kode keluar 0]

$ [2026-09-15] crm.py catat --kontak Anton --tahap lunas
Dicatat K0004 Pak Anton: tahap deal -> selesai; jadwal follow-up dihapus.
Sekarang: Selesai | nilai Rp 1.450.000 | tanpa jadwal follow-up
[kode keluar 0]

$ [2026-09-13] crm.py catat --kontak Sinta --tahap batal --alasan cuma tanya
Dicatat K0005 Sinta: tahap baru -> batal (alasan: hanya bertanya); jadwal follow-up dihapus.
Sekarang: Batal | nilai Rp 240.000 | tanpa jadwal follow-up
[kode keluar 0]

$ [2026-09-14] crm.py catat --kontak Lilis --tahap ditawar --followup 17/9
Dicatat K0006 Bu Lilis: tahap baru -> ditawar; follow-up Kamis, 17 September 2026.
Sekarang: Ditawar | nilai Rp 650.000 | follow-up Kamis, 17 September 2026
[kode keluar 0]

$ [2026-09-17] crm.py catat --kontak Lilis --tahap deal --isi fix 2 loyang
Dicatat K0006 Bu Lilis: catatan "fix 2 loyang"; tahap ditawar -> deal.
Sekarang: Deal | nilai Rp 650.000 | follow-up Kamis, 17 September 2026
[kode keluar 0]

$ [2026-09-14] crm.py terkirim --kontak Yoga
Dicatat: pesan ke K0007 Kak Yoga sudah dikirim. Follow-up berikutnya: Rabu, 16 September 2026.
Catatan: Tahap otomatis naik dari baru ke dihubungi.
[kode keluar 0]

$ [2026-09-15] crm.py catat --kontak Hendra --tahap ditawar --nilai 1,2 jt --followup Jumat
Dicatat K0008 Om Hendra: tahap baru -> ditawar; nilai Rp 1.200.000; follow-up Jumat, 18 September 2026.
Sekarang: Ditawar | nilai Rp 1.200.000 | follow-up Jumat, 18 September 2026
[kode keluar 0]

$ [2026-09-17] crm.py tambah --nama Bu Ratna --wa 0812-0000-1009 --sumber tiktok --kebutuhan kue kering lebaran 10 toples --nilai 1,1 jt
Tersimpan K0009: Bu Ratna | 0812-0000-1009 | Baru | sumber TikTok | nilai Rp 1.100.000 | follow-up Kamis, 17 September 2026
Catatan: Follow-up belum disebut; dijadwalkan hari ini (lead baru sebaiknya dibalas hari yang sama).
[kode keluar 0]

$ [2026-09-18] crm.py tambah --nama Mas Dimas --wa 0812-0000-1010 --sumber ig --kebutuhan kue ultah anak --nilai 300rb
Tersimpan K0010: Mas Dimas | 0812-0000-1010 | Baru | sumber Instagram | nilai Rp 300.000 | follow-up Jumat, 18 September 2026
Catatan: Follow-up belum disebut; dijadwalkan hari ini (lead baru sebaiknya dibalas hari yang sama).
[kode keluar 0]

$ [2026-09-19] crm.py tambah --nama Bu Sari --wa 0812-0000-1011 --sumber referensi --kebutuhan snack box arisan 40 --nilai 1 jt
Tersimpan K0011: Bu Sari | 0812-0000-1011 | Baru | sumber Referensi | nilai Rp 1.000.000 | follow-up Sabtu, 19 September 2026
Catatan: Follow-up belum disebut; dijadwalkan hari ini (lead baru sebaiknya dibalas hari yang sama).
[kode keluar 0]

$ [2026-09-21] crm.py tambah --nama Kak Putri --wa 0812-0000-1012 --sumber tiktok --kebutuhan bento cake --nilai 150rb
Tersimpan K0012: Kak Putri | 0812-0000-1012 | Baru | sumber TikTok | nilai Rp 150.000 | follow-up Senin, 21 September 2026
Catatan: Follow-up belum disebut; dijadwalkan hari ini (lead baru sebaiknya dibalas hari yang sama).
[kode keluar 0]

$ [2026-09-22] crm.py tambah --nama Pak Joko --wa 0812-0000-1013 --sumber ig --kebutuhan tart pernikahan --nilai 3,5 jt
Tersimpan K0013: Pak Joko | 0812-0000-1013 | Baru | sumber Instagram | nilai Rp 3.500.000 | follow-up Selasa, 22 September 2026
Catatan: Follow-up belum disebut; dijadwalkan hari ini (lead baru sebaiknya dibalas hari yang sama).
[kode keluar 0]

$ [2026-09-23] crm.py tambah --nama Bu Sari --wa 0812-0000-1014 --sumber ig --kebutuhan kue pengantin --nilai 800rb
Tersimpan K0014: Bu Sari | 0812-0000-1014 | Baru | sumber Instagram | nilai Rp 800.000 | follow-up Rabu, 23 September 2026
Catatan: Follow-up belum disebut; dijadwalkan hari ini (lead baru sebaiknya dibalas hari yang sama).
Catatan: Nama mirip kontak lain: K0011 Bu Sari (0812-****-1011). Jika orangnya sama, gabungkan dengan crm.py gabung.
[kode keluar 0]

$ [2026-09-23] crm.py tambah --nama Mbak Wulan --wa 0812-0000-1015 --sumber walk-in --kebutuhan roti sobek 10 --nilai 200rb
Tersimpan K0015: Mbak Wulan | 0812-0000-1015 | Baru | sumber Walk-in | nilai Rp 200.000 | follow-up Rabu, 23 September 2026
Catatan: Follow-up belum disebut; dijadwalkan hari ini (lead baru sebaiknya dibalas hari yang sama).
[kode keluar 0]

$ [2026-09-18] crm.py catat --kontak Hendra --tahap deal --isi ok 1,2jt, ambil 26/9
Dicatat K0008 Om Hendra: catatan "ok 1,2jt, ambil 26/9"; tahap ditawar -> deal.
Sekarang: Deal | nilai Rp 1.200.000 | follow-up Jumat, 18 September 2026
[kode keluar 0]

$ [2026-09-19] crm.py catat --kontak Ratna --tahap ditawar --followup 25/9
Dicatat K0009 Bu Ratna: tahap baru -> ditawar; follow-up Jumat, 25 September 2026.
Sekarang: Ditawar | nilai Rp 1.100.000 | follow-up Jumat, 25 September 2026
[kode keluar 0]

$ [2026-09-20] crm.py catat --kontak Dimas --tahap batal --alasan tidak ada respon
Dicatat K0010 Mas Dimas: tahap baru -> batal (alasan: tidak ada respon); jadwal follow-up dihapus.
Sekarang: Batal | nilai Rp 300.000 | tanpa jadwal follow-up
[kode keluar 0]

$ [2026-09-21] crm.py catat --kontak Bu Sari --tahap dihubungi --isi minta menu
GAGAL: Ada 2 kontak yang cocok dengan 'Bu Sari'. Tanyakan yang mana (sebut kodenya).
[kode keluar 1]

$ [2026-09-22] crm.py catat --kontak Putri --tahap deal --nilai 175rb
Dicatat K0012 Kak Putri: tahap baru -> deal; nilai Rp 175.000.
Sekarang: Deal | nilai Rp 175.000 | follow-up Senin, 21 September 2026
[kode keluar 0]

$ [2026-09-23] crm.py catat --kontak Bu Sari --isi cek
GAGAL: Ada 2 kontak yang cocok dengan 'Bu Sari'. Tanyakan yang mana (sebut kodenya).
[kode keluar 1]

$ [2026-09-24] crm.py hari-ini
FOLLOW-UP CRM - Kamis, 24 September 2026 (WIB)
Terlambat: 10 | Hari ini: 0 | Besok: 1 | Belum dijadwalkan: 0
Nilai prospek yang perlu disapa: Rp 8.650.000

TERLAMBAT (10)
1. K0001 Bu Rina | Instagram | Deal | Rp 400.000 | kue ulang tahun 2 tingkat | FU 12 Sep (telat 12 hari) | 0812-0000-1001
   Catatan terakhir 12 Sep: "DP 50% sudah transfer"
2. K0002 Kak Nia | TikTok | Dihubungi | Rp 375.000 | brownies 5 loyang | FU 13 Sep (telat 11 hari) | 0812-0000-1002
   Catatan terakhir 11 Sep: "tanya harga, belum balas lagi"
3. K0007 Kak Yoga | Instagram | Dihubungi | Rp 350.000 | dessert box 10 | FU 16 Sep (telat 8 hari) | 0812-0000-1007
4. K0006 Bu Lilis | Referensi | Deal | Rp 650.000 | kue lapis legit | FU 17 Sep (telat 7 hari) | 0812-0000-1006
   Catatan terakhir 17 Sep: "fix 2 loyang"
5. K0008 Om Hendra | Referensi | Deal | Rp 1.200.000 | kue ulang tahun kantor 3 tingkat | FU 18 Sep (telat 6 hari) | 0812-0000-1008
   Catatan terakhir 18 Sep: "ok 1,2jt, ambil 26/9"
6. K0011 Bu Sari | Referensi | Baru | Rp 1.000.000 | snack box arisan 40 | FU 19 Sep (telat 5 hari) | 0812-0000-1011
7. K0012 Kak Putri | TikTok | Deal | Rp 175.000 | bento cake | FU 21 Sep (telat 3 hari) | 0812-0000-1012
8. K0013 Pak Joko | Instagram | Baru | Rp 3.500.000 | tart pernikahan | FU 22 Sep (telat 2 hari) | 0812-0000-1013
9. K0014 Bu Sari | Instagram | Baru | Rp 800.000 | kue pengantin | FU 23 Sep (telat 1 hari) | 0812-0000-1014
10. K0015 Mbak Wulan | Walk-in | Baru | Rp 200.000 | roti sobek 10 | FU 23 Sep (telat 1 hari) | 0812-0000-1015

BESOK (1)
1. K0009 Bu Ratna | TikTok | Ditawar | Rp 1.100.000 | kue kering lebaran 10 toples | FU 25 Sep | 0812-0000-1009

DRAF PESAN (periksa, lalu kirim sendiri lewat tautan; bot tidak mengirim apa pun)

K0001 Bu Rina [konfirmasi-order]:
Halo Bu Rina, saya Tia dari Dapur Mama Tia. Terima kasih sudah memutuskan order kue ulang tahun 2 tingkat. Mohon dibantu konfirmasi detail pengiriman/jadwal dan pembayarannya ya. Kalau ada yang ingin diubah, kabari saya.
https://wa.me/6281200001001?text=Halo%20Bu%20Rina%2C%20saya%20Tia%20dari%20Dapur%20Mama%20Tia.%20Terima%20kasih%20sudah%20memutuskan%20order%20kue%20ulang%20tahun%202%20tingkat.%20Mohon%20dibantu%20konfirmasi%20detail%20pengiriman%2Fjadwal%20dan%20pembayarannya%20ya.%20Kalau%20ada%20yang%20ingin%20diubah%2C%20kabari%20saya.

K0002 Kak Nia [follow-up-1]:
Halo Kak Nia, saya Tia dari Dapur Mama Tia. Menyambung obrolan kita soal brownies 5 loyang, apakah masih ada yang ingin ditanyakan? Kalau berkenan, saya kirimkan foto atau detail tambahan supaya lebih mudah memilih.
https://wa.me/6281200001002?text=Halo%20Kak%20Nia%2C%20saya%20Tia%20dari%20Dapur%20Mama%20Tia.%20Menyambung%20obrolan%20kita%20soal%20brownies%205%20loyang%2C%20apakah%20masih%20ada%20yang%20ingin%20ditanyakan%3F%20Kalau%20berkenan%2C%20saya%20kirimkan%20foto%20atau%20detail%20tambahan%20supaya%20lebih%20mudah%20memilih.

K0007 Kak Yoga [follow-up-1]:
Halo Kak Yoga, saya Tia dari Dapur Mama Tia. Menyambung obrolan kita soal dessert box 10, apakah masih ada yang ingin ditanyakan? Kalau berkenan, saya kirimkan foto atau detail tambahan supaya lebih mudah memilih.
https://wa.me/6281200001007?text=Halo%20Kak%20Yoga%2C%20saya%20Tia%20dari%20Dapur%20Mama%20Tia.%20Menyambung%20obrolan%20kita%20soal%20dessert%20box%2010%2C%20apakah%20masih%20ada%20yang%20ingin%20ditanyakan%3F%20Kalau%20berkenan%2C%20saya%20kirimkan%20foto%20atau%20detail%20tambahan%20supaya%20lebih%20mudah%20memilih.

K0006 Bu Lilis [konfirmasi-order]:
Halo Bu Lilis, saya Tia dari Dapur Mama Tia. Terima kasih sudah memutuskan order kue lapis legit. Mohon dibantu konfirmasi detail pengiriman/jadwal dan pembayarannya ya. Kalau ada yang ingin diubah, kabari saya.
https://wa.me/6281200001006?text=Halo%20Bu%20Lilis%2C%20saya%20Tia%20dari%20Dapur%20Mama%20Tia.%20Terima%20kasih%20sudah%20memutuskan%20order%20kue%20lapis%20legit.%20Mohon%20dibantu%20konfirmasi%20detail%20pengiriman%2Fjadwal%20dan%20pembayarannya%20ya.%20Kalau%20ada%20yang%20ingin%20diubah%2C%20kabari%20saya.

K0008 Om Hendra [konfirmasi-order]:
Halo Om Hendra, saya Tia dari Dapur Mama Tia. Terima kasih sudah memutuskan order kue ulang tahun kantor 3 tingkat. Mohon dibantu konfirmasi detail pengiriman/jadwal dan pembayarannya ya. Kalau ada yang ingin diubah, kabari saya.
https://wa.me/6281200001008?text=Halo%20Om%20Hendra%2C%20saya%20Tia%20dari%20Dapur%20Mama%20Tia.%20Terima%20kasih%20sudah%20memutuskan%20order%20kue%20ulang%20tahun%20kantor%203%20tingkat.%20Mohon%20dibantu%20konfirmasi%20detail%20pengiriman%2Fjadwal%20dan%20pembayarannya%20ya.%20Kalau%20ada%20yang%20ingin%20diubah%2C%20kabari%20saya.

K0011 Bu Sari [sapaan-awal]:
Halo Bu Sari, terima kasih sudah menghubungi Dapur Mama Tia. Saya Tia. Soal snack box arisan 40, boleh saya bantu jelaskan pilihan dan harganya? Kira-kira dibutuhkan untuk kapan ya?
https://wa.me/6281200001011?text=Halo%20Bu%20Sari%2C%20terima%20kasih%20sudah%20menghubungi%20Dapur%20Mama%20Tia.%20Saya%20Tia.%20Soal%20snack%20box%20arisan%2040%2C%20boleh%20saya%20bantu%20jelaskan%20pilihan%20dan%20harganya%3F%20Kira-kira%20dibutuhkan%20untuk%20kapan%20ya%3F

K0012 Kak Putri [konfirmasi-order]:
Halo Kak Putri, saya Tia dari Dapur Mama Tia. Terima kasih sudah memutuskan order bento cake. Mohon dibantu konfirmasi detail pengiriman/jadwal dan pembayarannya ya. Kalau ada yang ingin diubah, kabari saya.
https://wa.me/6281200001012?text=Halo%20Kak%20Putri%2C%20saya%20Tia%20dari%20Dapur%20Mama%20Tia.%20Terima%20kasih%20sudah%20memutuskan%20order%20bento%20cake.%20Mohon%20dibantu%20konfirmasi%20detail%20pengiriman%2Fjadwal%20dan%20pembayarannya%20ya.%20Kalau%20ada%20yang%20ingin%20diubah%2C%20kabari%20saya.

K0013 Pak Joko [sapaan-awal]:
Halo Pak Joko, terima kasih sudah menghubungi Dapur Mama Tia. Saya Tia. Soal tart pernikahan, boleh saya bantu jelaskan pilihan dan harganya? Kira-kira dibutuhkan untuk kapan ya?
https://wa.me/6281200001013?text=Halo%20Pak%20Joko%2C%20terima%20kasih%20sudah%20menghubungi%20Dapur%20Mama%20Tia.%20Saya%20Tia.%20Soal%20tart%20pernikahan%2C%20boleh%20saya%20bantu%20jelaskan%20pilihan%20dan%20harganya%3F%20Kira-kira%20dibutuhkan%20untuk%20kapan%20ya%3F

K0014 Bu Sari [sapaan-awal]:
Halo Bu Sari, terima kasih sudah menghubungi Dapur Mama Tia. Saya Tia. Soal kue pengantin, boleh saya bantu jelaskan pilihan dan harganya? Kira-kira dibutuhkan untuk kapan ya?
https://wa.me/6281200001014?text=Halo%20Bu%20Sari%2C%20terima%20kasih%20sudah%20menghubungi%20Dapur%20Mama%20Tia.%20Saya%20Tia.%20Soal%20kue%20pengantin%2C%20boleh%20saya%20bantu%20jelaskan%20pilihan%20dan%20harganya%3F%20Kira-kira%20dibutuhkan%20untuk%20kapan%20ya%3F

K0015 Mbak Wulan [sapaan-awal]:
Halo Mbak Wulan, terima kasih sudah menghubungi Dapur Mama Tia. Saya Tia. Soal roti sobek 10, boleh saya bantu jelaskan pilihan dan harganya? Kira-kira dibutuhkan untuk kapan ya?
https://wa.me/6281200001015?text=Halo%20Mbak%20Wulan%2C%20terima%20kasih%20sudah%20menghubungi%20Dapur%20Mama%20Tia.%20Saya%20Tia.%20Soal%20roti%20sobek%2010%2C%20boleh%20saya%20bantu%20jelaskan%20pilihan%20dan%20harganya%3F%20Kira-kira%20dibutuhkan%20untuk%20kapan%20ya%3F

Balas misalnya: "terkirim K0001", "Bu Rina deal 4,2 jt", "tunda K0002 ke Senin", "K0003 batal, kemahalan".
[kode keluar 0]

$ [2026-09-24] crm.py terkirim --kontak K0002
Dicatat: pesan ke K0002 Kak Nia sudah dikirim. Follow-up berikutnya: Minggu, 27 September 2026.
[kode keluar 0]

$ [2026-09-24] crm.py lihat --kontak K0002
K0002 Kak Nia
WA: 0812-0000-1002 | Sumber: TikTok | Label: -
Tahap: Dihubungi | Nilai: Rp 375.000 | Kebutuhan: brownies 5 loyang
Masuk: 10 Sep 2026 | Deal: - | Kontak terakhir: 24 Sep 2026 | Follow-up: Minggu, 27 September 2026
Riwayat (terbaru dulu):
- 2026-09-24 09:00 [kirim] Pesan follow-up-1 dikirim pemilik; follow-up berikutnya 27 Sep 2026
- 2026-09-11 09:00 [tahap] tahap baru -> dihubungi; follow-up Minggu, 13 September 2026
- 2026-09-11 09:00 [catatan] tanya harga, belum balas lagi
- 2026-09-10 09:00 [masuk] Kontak ditambahkan (sumber TikTok, tahap baru)

Draf berikutnya (pilihan-mudah), dikirim sendiri oleh pemilik:
Halo Kak Nia, saya Tia dari Dapur Mama Tia. Sekadar mengingatkan soal brownies 5 loyang. Supaya mudah, cukup balas angka saja: 1 = mau lanjut, 2 = masih pikir-pikir, 3 = belum perlu dulu. Apa pun jawabannya tidak apa-apa, terima kasih.
https://wa.me/6281200001002?text=Halo%20Kak%20Nia%2C%20saya%20Tia%20dari%20Dapur%20Mama%20Tia.%20Sekadar%20mengingatkan%20soal%20brownies%205%20loyang.%20Supaya%20mudah%2C%20cukup%20balas%20angka%20saja%3A%201%20%3D%20mau%20lanjut%2C%202%20%3D%20masih%20pikir-pikir%2C%203%20%3D%20belum%20perlu%20dulu.%20Apa%20pun%20jawabannya%20tidak%20apa-apa%2C%20terima%20kasih.
[kode keluar 0]

$ [2026-09-24] crm.py rekap --periode bulan-ini
REKAP CRM Dapur Mama Tia - bulan September 2026 (1 Sep 2026 - 30 Sep 2026)
Data per Kamis, 24 September 2026 WIB

POSISI SAAT INI (semua kontak)
- Baru      :   4 kontak | Rp 5.500.000
- Dihubungi :   2 kontak | Rp 725.000
- Ditawar   :   1 kontak | Rp 1.100.000
- Deal      :   4 kontak | Rp 2.425.000
- Selesai   :   1 kontak | Rp 1.450.000
- Batal     :   3 kontak
Pipeline terbuka (baru+dihubungi+ditawar): 7 kontak, Rp 7.325.000

PERIODE BULAN SEPTEMBER 2026
Lead masuk: 15
Deal baru: 5 senilai Rp 3.875.000
Rata-rata nilai deal: Rp 775.000 | Rata-rata lama closing: 2,6 hari
Batal: 3
Konversi lead periode ini: 5 dari 15 = 33,3% (7 masih berjalan, 3 batal)
Win rate (yang sudah diputuskan): 5 dari 8 = 62,5%

SUMBER LEAD (lead masuk periode ini)
1. Referensi: 4 lead, 2 deal (50,0%), Rp 1.850.000
2. Instagram: 6 lead, 2 deal (33,3%), Rp 1.850.000
3. TikTok: 4 lead, 1 deal (25,0%), Rp 175.000
4. Walk-in: 1 lead, 0 deal (0,0%), Rp 0
Sumber terbaik: Referensi (nilai deal terbesar). Sampel kecil (<5 lead), jadikan petunjuk saja.

ALASAN BATAL: hanya bertanya (1), harga terlalu mahal (1), tidak ada respon (1)

FOLLOW-UP SAAT INI: terlambat 9, hari ini 0, besok 1, belum dijadwalkan 0
Ketik "follow-up hari ini" untuk daftar & draf pesannya.
Catatan: periode ini masih baru; konversi akan naik bila lead yang masih berjalan jadi deal.

Rumus perhitungan: tambahkan --rumus.
[kode keluar 0]

$ [2026-09-24] crm.py rekap --periode minggu-lalu --rumus
REKAP CRM Dapur Mama Tia - minggu lalu (14 Sep 2026 - 20 Sep 2026)
Data per Kamis, 24 September 2026 WIB

POSISI SAAT INI (semua kontak)
- Baru      :   4 kontak | Rp 5.500.000
- Dihubungi :   2 kontak | Rp 725.000
- Ditawar   :   1 kontak | Rp 1.100.000
- Deal      :   4 kontak | Rp 2.425.000
- Selesai   :   1 kontak | Rp 1.450.000
- Batal     :   3 kontak
Pipeline terbuka (baru+dihubungi+ditawar): 7 kontak, Rp 7.325.000

PERIODE MINGGU LALU
Lead masuk: 4
Deal baru: 2 senilai Rp 1.850.000
Rata-rata nilai deal: Rp 925.000 | Rata-rata lama closing: 4,5 hari
Batal: 2
Konversi lead periode ini: 1 dari 4 = 25,0% (2 masih berjalan, 1 batal)
Win rate (yang sudah diputuskan): 1 dari 2 = 50,0%

SUMBER LEAD (lead masuk periode ini)
1. Referensi: 2 lead, 1 deal (50,0%), Rp 1.200.000
2. Instagram: 1 lead, 0 deal (0,0%), Rp 0
3. TikTok: 1 lead, 0 deal (0,0%), Rp 0
Sumber terbaik: Referensi (nilai deal terbesar). Sampel kecil (<5 lead), jadikan petunjuk saja.

ALASAN BATAL: harga terlalu mahal (1), tidak ada respon (1)

FOLLOW-UP SAAT INI: terlambat 9, hari ini 0, besok 1, belum dijadwalkan 0
Ketik "follow-up hari ini" untuk daftar & draf pesannya.
Catatan: periode ini masih baru; konversi akan naik bila lead yang masih berjalan jadi deal.

RUMUS
- Posisi saat ini = jumlah kontak & jumlah nilai potensi per tahap untuk SEMUA kontak (bukan hanya periode). Pipeline terbuka = baru + dihubungi + ditawar.
- Lead masuk = kontak dengan tanggal masuk di dalam periode.
- Deal baru = kontak yang pertama kali mencapai deal (atau langsung selesai) di dalam periode; nilai = jumlah kolom nilai kontak itu (kontak tanpa nilai dihitung jumlahnya, nilainya tidak).
- Konversi = lead masuk periode yang kini deal/selesai / lead masuk periode x 100%, dihitung pecahan persis lalu dibulatkan 1 desimal (0,05 ke atas).
- Win rate = (deal/selesai) / (deal/selesai + batal) dari lead masuk periode yang sudah diputuskan.
- Rata-rata nilai deal = jumlah nilai deal baru / jumlah deal baru yang bernilai, dibulatkan ke rupiah terdekat.
- Lama closing = rata-rata (tanggal deal - tanggal masuk) dalam hari, deal baru periode ini, 1 desimal.
- Sumber terbaik = sumber dengan nilai deal terbesar dari lead masuk periode; seri -> konversi lebih tinggi -> lead lebih banyak.
[kode keluar 0]

$ [2026-09-24] crm.py hari-ini --samarkan
FOLLOW-UP CRM - Kamis, 24 September 2026 (WIB)
Terlambat: 9 | Hari ini: 0 | Besok: 1 | Belum dijadwalkan: 0
Nilai prospek yang perlu disapa: Rp 8.275.000

TERLAMBAT (9)
1. K0001 Bu R. | Instagram | Deal | Rp 400.000 | kue ulang tahun 2 tingkat | FU 12 Sep (telat 12 hari) | 0812-****-1001
2. K0007 Kak Y. | Instagram | Dihubungi | Rp 350.000 | dessert box 10 | FU 16 Sep (telat 8 hari) | 0812-****-1007
3. K0006 Bu L. | Referensi | Deal | Rp 650.000 | kue lapis legit | FU 17 Sep (telat 7 hari) | 0812-****-1006
4. K0008 Om H. | Referensi | Deal | Rp 1.200.000 | kue ulang tahun kantor 3 tingkat | FU 18 Sep (telat 6 hari) | 0812-****-1008
5. K0011 Bu S. | Referensi | Baru | Rp 1.000.000 | snack box arisan 40 | FU 19 Sep (telat 5 hari) | 0812-****-1011
6. K0012 Kak P. | TikTok | Deal | Rp 175.000 | bento cake | FU 21 Sep (telat 3 hari) | 0812-****-1012
7. K0013 Pak J. | Instagram | Baru | Rp 3.500.000 | tart pernikahan | FU 22 Sep (telat 2 hari) | 0812-****-1013
8. K0014 Bu S. | Instagram | Baru | Rp 800.000 | kue pengantin | FU 23 Sep (telat 1 hari) | 0812-****-1014
9. K0015 Mbak W. | Walk-in | Baru | Rp 200.000 | roti sobek 10 | FU 23 Sep (telat 1 hari) | 0812-****-1015

BESOK (1)
1. K0009 Bu R. | TikTok | Ditawar | Rp 1.100.000 | kue kering lebaran 10 toples | FU 25 Sep | 0812-****-1009

DRAF PESAN (periksa, lalu kirim sendiri lewat tautan; bot tidak mengirim apa pun)

K0001 Bu R. [konfirmasi-order]:
Halo Bu R., saya Tia dari Dapur Mama Tia. Terima kasih sudah memutuskan order kue ulang tahun 2 tingkat. Mohon dibantu konfirmasi detail pengiriman/jadwal dan pembayarannya ya. Kalau ada yang ingin diubah, kabari saya.
(tautan disembunyikan karena mode samarkan)

K0007 Kak Y. [follow-up-1]:
Halo Kak Y., saya Tia dari Dapur Mama Tia. Menyambung obrolan kita soal dessert box 10, apakah masih ada yang ingin ditanyakan? Kalau berkenan, saya kirimkan foto atau detail tambahan supaya lebih mudah memilih.
(tautan disembunyikan karena mode samarkan)

K0006 Bu L. [konfirmasi-order]:
Halo Bu L., saya Tia dari Dapur Mama Tia. Terima kasih sudah memutuskan order kue lapis legit. Mohon dibantu konfirmasi detail pengiriman/jadwal dan pembayarannya ya. Kalau ada yang ingin diubah, kabari saya.
(tautan disembunyikan karena mode samarkan)

K0008 Om H. [konfirmasi-order]:
Halo Om H., saya Tia dari Dapur Mama Tia. Terima kasih sudah memutuskan order kue ulang tahun kantor 3 tingkat. Mohon dibantu konfirmasi detail pengiriman/jadwal dan pembayarannya ya. Kalau ada yang ingin diubah, kabari saya.
(tautan disembunyikan karena mode samarkan)

K0011 Bu S. [sapaan-awal]:
Halo Bu S., terima kasih sudah menghubungi Dapur Mama Tia. Saya Tia. Soal snack box arisan 40, boleh saya bantu jelaskan pilihan dan harganya? Kira-kira dibutuhkan untuk kapan ya?
(tautan disembunyikan karena mode samarkan)

K0012 Kak P. [konfirmasi-order]:
Halo Kak P., saya Tia dari Dapur Mama Tia. Terima kasih sudah memutuskan order bento cake. Mohon dibantu konfirmasi detail pengiriman/jadwal dan pembayarannya ya. Kalau ada yang ingin diubah, kabari saya.
(tautan disembunyikan karena mode samarkan)

K0013 Pak J. [sapaan-awal]:
Halo Pak J., terima kasih sudah menghubungi Dapur Mama Tia. Saya Tia. Soal tart pernikahan, boleh saya bantu jelaskan pilihan dan harganya? Kira-kira dibutuhkan untuk kapan ya?
(tautan disembunyikan karena mode samarkan)

K0014 Bu S. [sapaan-awal]:
Halo Bu S., terima kasih sudah menghubungi Dapur Mama Tia. Saya Tia. Soal kue pengantin, boleh saya bantu jelaskan pilihan dan harganya? Kira-kira dibutuhkan untuk kapan ya?
(tautan disembunyikan karena mode samarkan)

K0015 Mbak W. [sapaan-awal]:
Halo Mbak W., terima kasih sudah menghubungi Dapur Mama Tia. Saya Tia. Soal roti sobek 10, boleh saya bantu jelaskan pilihan dan harganya? Kira-kira dibutuhkan untuk kapan ya?
(tautan disembunyikan karena mode samarkan)

Balas misalnya: "terkirim K0001", "Bu Rina deal 4,2 jt", "tunda K0002 ke Senin", "K0003 batal, kemahalan".
[kode keluar 0]
```
</details>
