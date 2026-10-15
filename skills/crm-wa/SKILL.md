---
name: crm-wa
description: CRM lokal untuk alur jualan lewat WhatsApp (chat WA → ditawar → deal) di komputer pemilik (SQLite, tanpa langganan/internet), dioperasikan lewat chat biasa: simpan kontak & sumber lead (IG/TikTok/marketplace/referensi/walk-in), nomor WA otomatis jadi 62…, tahap pipeline, catatan obrolan, nilai potensi, jadwal follow-up, daftar "hari ini harus di-follow-up" dan "terlambat" + draf pesan sopan dengan tautan wa.me yang DIKIRIM SENDIRI oleh pemilik, rekap pipeline/konversi/sumber lead terbaik, impor/ekspor CSV, cek nomor dobel, pengingat harian ke Telegram (OpenClaw). Gunakan untuk "catat calon pembeli", "siapa yang harus di-follow-up hari ini", "Bu Rina jadi deal", "rekap penjualan per tahap", "daftar pelanggan buat promo", "data pelanggan", "kontak pembeli", CRM, sales pipeline, lead tracking, customer list, follow-up reminder. Promo hanya ke pelanggan yang setuju (opt-in), dikirim satu per satu. Bukan untuk kirim massal/broadcast.
---

# CRM WA (chat WA → ditawar → deal)

> **Aturan kerja:** Jangan menginstal paket/aplikasi (mis. `pip install`) — bila perlu, tunjukkan caranya dan biarkan pengguna yang memasang; jangan membuka atau mencari file selain yang diberikan pengguna, isi folder skill ini, dan file yang disebut di langkah kerja; jangan menulis file baru tanpa menyebut lokasinya, dan simpan hasil di folder kerja yang disepakati (bukan /tmp).

## Tujuan
Menjadi "CRM" pemilik usaha tanpa biaya bulanan: semua calon pembeli dan pelanggan ada di **satu file database di komputernya sendiri**, dan kamu (agent) yang mengoperasikannya lewat `scripts/crm.py`. Hasil: tidak ada lead yang lupa dibalas, setiap pagi ada daftar siapa yang harus disapa beserta **draf pesan + tautan wa.me** (pemilik tinggal klik, periksa, tekan Kirim), dan rekap jelas: berapa yang deal, nilainya, konversi, dan sumber lead mana yang paling menghasilkan.

## Kapan digunakan
- "Catat: Bu Rina dari IG, 0812-0000-1001, tanya kue ulang tahun 2 tingkat, kira-kira 450 ribu."
- "Pak Budi nawar jadi 4 juta, katanya mau diskusi istri dulu. Follow-up Jumat."
- "Bu Rina jadi order, 4,2 juta." / "Om Heru batal, kemahalan." / "Pesanan Pak Budi sudah beres."
- "Hari ini saya harus follow-up siapa saja?" / "Bikinin pesan buat Pak Budi."
- "Sudah saya kirim ke Bu Rina." / "Tunda Mbak Dewi ke Senin."
- "Rekap CRM bulan ini" / "sumber pembeli paling bagus dari mana?" / "berapa yang jadi deal minggu lalu?"
- "Masukkan daftar kontak ini" (CSV dari Excel/Google Contacts) / "cek nomor dobel" / "ekspor ke Excel".
- "Kirim daftar follow-up ke Telegram saya tiap pagi jam 8" (OpenClaw).
- "Bikinin daftar pelanggan buat promo" / "data pelanggan saya" / "kontak pembeli dari Shopee" → lihat aturan 10 (persetujuan promo).

## Kapan TIDAK digunakan
- **Kirim pesan otomatis/massal/broadcast ke pelanggan** → **tolak**. Keputusan pemilik: OpenClaw memakai WhatsApp Web (tidak resmi), pesan otomatis/massal bisa membuat nomor diblokir. Skill ini hanya menyiapkan draf + tautan wa.me; manusia yang mengirim **satu per satu**. Jangan pula menyarankan "broadcast WhatsApp Business/aplikasi lain" ke kontak yang belum setuju promo. Untuk promo ke pelanggan yang **sudah opt-in**: draf per kontak dari skill ini (aturan 9–10). Bila skill `broadcast-wa` terpasang (tidak termasuk paket Toko Online), itu hanya membantu menulis variasi teks promo + daftar wa.me untuk kontak yang setuju — pengiriman tetap satu per satu oleh pemilik, bukan blast. Belum terpasang → cukup pakai draf skill ini. Pengguna butuh kiriman otomatis/massal → jelaskan bahwa kiriman otomatis/massal resmi tersedia lewat WhatsApp Business Platform (API) resmi milik Meta, dengan template pesan yang disetujui & opt-in penerima (Kebijakan WhatsApp Business, whatsapp.com/legal/business-policy, dicek 15 Okt 2026), bukan lewat WhatsApp Web/OpenClaw, dan itu di luar skill ini; daftar wa.me dari skill ini hanya untuk dibuka & dikirim sendiri satu per satu (mode Copilot).
- Menulis **urutan pesan lengkap** (H+1/3/7/14) yang dipersonalisasi untuk satu prospek besar → `follow-up-prospek` (lalu jadwalnya dicatat di sini dengan `catat --followup`).
- Pengingat **tagihan/piutang/janji/timesheet** → `pengingat-follow-up`. Sudah memakai pengingat-follow-up untuk prospek? Jangan pantau prospek yang sama di dua tempat (pengingat dobel). Jembatan: `ekspor --format pengingat` (lihat Langkah F).
- Membalas chat/komplain pelanggan yang masuk → `balas-chat-cs` (satu chat) atau `agen-cs-toko` (CS toko dengan basis pengetahuan). Membuat surat/penawaran harga resmi → `surat-penawaran-harga`. Menagih yang sudah deal tapi belum bayar → `tagih-piutang`. Mencatat penjualan kasir → `kasir-lokal`.
- Mengambil data dari marketplace/IG dengan login browser (scraping) → tolak; minta pengguna mengekspor CSV sendiri.
- Laporan laba rugi/keuangan → `laporan-keuangan-emkm` (CRM hanya mencatat nilai potensi & deal, bukan pembukuan).
- Skill rujukan tidak terpasang: jelaskan singkat bedanya, lalu bantu sebisanya dengan draf bawaan skill ini.

## Aturan wajib
1. **Tidak pernah mengirim pesan ke pelanggan.** Tampilkan draf + tautan wa.me; pemilik yang membuka, memeriksa, dan menekan Kirim. Setelah pemilik bilang sudah kirim → `terkirim`.
2. **Angka dari script.** Nilai, total, konversi, jumlah hari, tanggal: salin dari output script. Jangan menghitung atau mengonversi tanggal sendiri; teruskan teks pengguna apa adanya (`--followup "Jumat"`).
3. **Jangan menebak kontak.** Jika script menjawab ambigu (`pilihan`: kode, nama, 4 digit akhir nomor, tahap; termasuk kontak yang batal), tanyakan "Bu Sari yang mana?" dengan daftar itu, lalu ulangi dengan kodenya. Jika nomor sudah terdaftar (`duplikat`), jangan menambah dobel; catat ke kontak yang ada.
4. **Perubahan besar** (`init`, `impor`, `hapus`, `gabung`, `restore`) dijalankan dulu tanpa `--ya` (pratinjau), tunjukkan ringkasannya (untuk `init`: **lokasi file database** yang akan dibuat), lalu **berhenti dan tunggu jawaban**. Ulangi **perintah yang sama + `--ya`** hanya setelah pengguna membalas setuju ("ya") di **pesan berikutnya** — permintaan awal ("pakai CRM buat usaha saya") **bukan** persetujuan, dan jangan pernah menjalankan pratinjau dan `--ya` dalam satu giliran. Tidak ada file/database yang boleh dibuat sebelum itu (script pun tidak membuatnya diam-diam: perintah lain menolak bila database belum ada). Perubahan kecil (`tambah`, `catat`, `tunda`, `terkirim`, `ubah`, `atur`) langsung tersimpan; sampaikan hasilnya agar bisa dikoreksi.
5. **Kolom kebutuhan = nama produk/jasa saja** ("kue ulang tahun 2 tingkat"). Harga → `--nilai`; komentar/cerita → `--catatan`/`--isi`. Script hanya memasukkan nama produk ke draf (angka rupiah & teks setelah koma dibuang) dan memperingatkan bila kolom itu berisi hal lain.
6. **Privasi:** nomor HP pelanggan = data pribadi (UU 27/2022 PDP). Jangan menampilkan daftar kontak lengkap ke grup; untuk laporan yang dibagikan pakai `--samarkan`. Catatan obrolan (`--isi`) bersifat pribadi dan tidak pernah masuk draf. Pelanggan minta datanya dihapus → `hapus` (pratinjau → `--ya`).
7. **Satu database = satu usaha (jangan pernah dicampur).** Awal setiap sesi jalankan `info` dan catat profil aktif (nama usaha + pengirim). Bila pengguna menyebut nama usaha/pemilik yang **berbeda** dari profil itu, **berhenti sebelum mencatat apa pun** dan tanyakan sekali: "Database ini milik usaha lain (<nama usaha> / <pengirim>). Mau (a) pakai database terpisah untuk usaha baru, misalnya `--db ~/KomunitechData/crm-<usaha-baru>/crm.db` (disarankan), atau (b) mengganti profil usaha di database ini?" Jangan menulis, membaca isi, merekap, atau menyusun draf dari data usaha lain untuk pengguna baru. Pilihan (a): langsung jalankan pratinjau `init --db <path baru>` (tanpa `--ya`) dan tampilkan lokasi file + profil usahanya **dalam pesan yang sama dengan pertanyaan (a)/(b)**, lalu tutup dengan "Buat sekarang? (ya/tidak)" supaya satu "ya" cukup (aturan 4); setelah itu pakai `--db` yang sama di semua perintah. Draf pesan selalu memakai nama usaha & pengirim dari profil aktif yang sudah dikonfirmasi pengguna ini, bukan dari obrolan atau data lain.
9. **Draf untuk banyak kontak ("semua kontak", "semua prospek"):** hanya kontak yang aktif. Kontak tahap `batal` (termasuk yang catatannya "minta jangan dihubungi") **dikecualikan** dan sebutkan alasannya ("Bu Sari tidak ikut: batal, minta jangan dihubungi"). Tetap draf + tautan wa.me satu per satu, tidak pernah kirim massal (aturan 1).
10. **Promo hanya ke pelanggan yang setuju (opt-in).** Permintaan "daftar pelanggan buat promo / kirim promo ke semua pembeli": hanya kontak berlabel `setuju-promo` (`daftar --label setuju-promo`). Label ini dipasang (`ubah --kontak .. --tambah-label setuju-promo` + `catat --isi "setuju promo via <chat/formulir>, <tanggal>"`) **hanya** bila pemilik menyatakan pelanggan itu sudah setuju dikabari promo; tanggal & sumber persetujuan belum disebut → tanyakan sekali, lalu catat (catatan persetujuan, UU 27/2022 PDP Pasal 20–21; Kebijakan WhatsApp Business: hanya ke yang opt-in). **Pembeli marketplace (Shopee/Tokopedia/TikTok Shop, termasuk dari file ekspor pesanan) default BELUM setuju**: datanya diberikan untuk pengiriman pesanan (UU 27/2022 PDP + aturan platform). Jangan impor ekspor pesanan marketplace sebagai daftar promo; tawarkan promo lewat fitur di dalam platform (voucher toko, fitur promo resmi platform yang berbasis pengikut/opt-in; BUKAN chat broadcast/blast marketplace ke pembeli yang belum opt-in, berisiko melanggar kebijakan platform) atau ajakan opt-in di kemasan. Kontak yang minta berhenti → `--hapus-label setuju-promo` dan catat. Tetap draf satu per satu (aturan 1), tanpa broadcast/blast.
8. Sampaikan setiap `peringatan`/`Catatan:` dari script (tanggal yang ditebak, nomor bukan HP, nilai deal belum diisi, dsb.).

## Cara menjalankan script
Path relatif terhadap folder berisi SKILL.md ini (Windows: ganti `python3` dengan `python` atau `py`):
```bash
python3 <folder-skill-ini>/scripts/crm.py <perintah> [opsi] --json
```
- JSON berisi `ok`, `mode` (`tersimpan`/`pratinjau`/`baca`), `perlu_konfirmasi`, `peringatan`, `error`, `teks` (siap tempel). Kode keluar 1 = gagal (pesan di `error`), 2 = perintah salah tulis.
- Database default `~/KomunitechData/crm/crm.db`; bisa diganti `--db PATH` (ditulis **setelah** nama perintah) atau ENV `KOMUNITECH_CRM_DB` / `KOMUNITECH_DATA`. Pakai lokasi yang sama di semua perintah.
- Nilai opsi yang diawali tanda minus ditulis `--isi="-50rb dari harga awal"` (pakai `=`).
- Semua perintah & opsi: `references/perintah.md`. Jadwal Telegram: `references/openclaw-jadwal.md`. Tanpa Python: `references/tanpa-python.md`.

## Input
| Info | Wajib? | Default |
|---|---|---|
| Nama usaha & nama pengirim (untuk draf) | Saat mulai (boleh kosong) | Draf memakai "kami" |
| Nama kontak | Ya | — (tanyakan) |
| Nomor WA | Sangat disarankan | Tanpa nomor: draf tanpa tautan |
| Sumber lead | Tidak | "Tidak diketahui" (tanyakan sekali; penting untuk rekap sumber terbaik) |
| Kebutuhan/produk yang diminati | Tidak | Kosong (draf lebih umum) |
| Nilai potensi (Rp) | Tidak | Kosong (tidak ikut dijumlah) |
| Tahap | Tidak | `baru` |
| Jadwal follow-up | Tidak | baru → hari ini; dihubungi/ditawar → 2 hari lagi (script menyebut asumsinya) |
| Alasan batal | Wajib bila batal | — (tanyakan: harga, tidak ada respon, pilih penjual lain, belum butuh, ...) |

Jika info wajib kurang, tanyakan **sekali** dalam satu pesan bernomor (maks. 5 pertanyaan). Jika pengguna ingin cepat, simpan yang ada dan sebutkan yang masih kosong.

## Langkah kerja

> **Lokasi script:** semua script skill ini ada di subfolder `scripts/` di folder yang sama dengan SKILL.md ini (folder skill). Jalankan dari sana; jangan mencari script atau file pengguna ke seluruh disk (mis. `find /`) — itu lambat dan menyentuh data pribadi di luar folder kerja.

### A. Mulai
1. `info --json`. Belum ada database → tanyakan nama usaha, nama yang dipakai di pesan, sapaan default (Kak/Bapak/Ibu), dan zona (WIB/WITA/WIT).
2. `init --nama-usaha "..." --pengirim "..." [--sapaan Kak] [--zona WIB]` → tunjukkan pratinjau **beserta path file database** → tanya "Buat database di lokasi ini? (ya/tidak)" → **tunggu balasan** → hanya bila "ya": ulangi + `--ya`. Pengguna sekaligus minta mencatat kontak? Catat nanti, setelah database dibuat.
3. Punya daftar kontak lama? Lanjut ke Langkah F (impor).

### B. Lead baru masuk
`tambah --nama "Bu Rina" --wa "0812-0000-1001" --sumber ig --kebutuhan "kue ulang tahun 2 tingkat" --nilai 450rb [--label "reseller"] [--followup besok] [--catatan "..."]`
- Nomor apa pun (`0812…`, `+62 812…`, `(0812) …`, `812…`) disimpan sebagai `62…`. Nomor tidak wajar, berisi huruf, dua nomor sekaligus, atau rusak karena Excel (`6.28E+12`) ditolak dengan alasan.
- Sumber dibakukan: ig→Instagram, tt→TikTok, tokped→Tokopedia, ref/teman→Referensi, walk in→Walk-in, dll.
- Nomor sudah ada → script menolak dan menyebut kontaknya. Catat ke kontak itu (`catat`). `--izinkan-duplikat` hanya bila pengguna menegaskan orangnya berbeda.
- Lead yang sudah lama masuk: `--masuk "20/9"` (agar rekap per periode benar).

### C. Setelah ngobrol / ada perkembangan
`catat --kontak "Pak Budi" [--isi "minta diskon 10%, diskusi istri"] [--tahap ditawar] [--nilai "4 jt"] [--followup Jumat] [--alasan ".."] [--tanggal kemarin]`
- Tahap: `baru` → `dihubungi` → `ditawar` → `deal` → `selesai`, atau `batal` (+ `--alasan`, wajib). Kata sehari-hari dikenali: nego/tawar → ditawar; jadi/order/closing → deal; lunas/beres → selesai; gak jadi/cancel → batal.
- Pindah tahap tanpa `--followup` → jadwal lama **selalu diganti**: dihubungi/ditawar → 2 hari lagi; **deal → jadwal konfirmasi order (pembayaran/pengiriman) 2 hari lagi**; selesai/batal → jadwal dihapus. Pengguna menyebut tanggal kirim/ambil → pakai `--followup` itu. Deal → isi nilai deal (`--nilai`); tanyakan bila script memperingatkan nilainya kosong.
- `--kontak` boleh nama, kode (`K0003`), atau nomor WA.
- Mundur dari deal (batal order) → pakai `--tahap batal --alasan ...`; tanggal deal dihapus dari rekap otomatis.
- Pindah jadwal saja: `tunda --kontak "Mbak Dewi" --ke Senin`. Ubah data: `ubah --kontak K0003 --wa ... / --nilai ... / --tambah-label vip`.

### D. Follow-up harian (inti)
1. `hari-ini` → tampilkan teks apa adanya: TERLAMBAT, HARI INI (prospek), ORDER BERJALAN (deal yang perlu konfirmasi pembayaran/pengiriman; tidak pernah disebut terlambat), BESOK, BELUM DIJADWALKAN, jumlah kontak yang sudah dikirimi pesan pamit, lalu DRAF PESAN (maks. 10) dengan tautan wa.me. Tiap kelompok dibatasi 20 baris (besok/belum dijadwalkan 10) + "... dan N lainnya"; seluruhnya: `--semua`.
2. Minta pemilik membuka tautan, **memeriksa**, dan menekan Kirim sendiri. Boleh memperhalus draf atas permintaan pemilik, lalu buat tautannya lewat script: `draf --kontak K0002 --pesan "<teks final>"` (jangan menyusun tautan wa.me sendiri). Harga/angka yang ditambahkan ke draf harus dari pemilik atau dari script.
3. Pemilik bilang sudah kirim → `terkirim --kontak K0002 [--berikutnya "3 hari lagi"]`. Irama otomatis: sapaan awal (baru → dihubungi, lanjut 2 hari) → follow-up ke-1 (+3 hari) → "pilihan mudah" (+4 hari) → **pesan pamit** → berhenti + saran tandai batal "tidak ada respon". Deal: pengingat order tiap 2 hari. Selesai: ucapan terima kasih; `--berikutnya "30 hari lagi"` untuk tawaran ulang.
4. Pelanggan membalas → kembali ke Langkah C.

### E. Rekap
`rekap [--periode bulan-ini|bulan-lalu|minggu-ini|minggu-lalu|hari-ini|kemarin|tahun-ini|semua | --bulan 2026-09 | --tanggal .. | --dari .. --sampai ..] [--rumus]`
Kirim `teks` apa adanya. Isinya: posisi semua kontak per tahap (jumlah & nilai), pipeline terbuka, lead masuk, deal baru & nilainya, rata-rata nilai deal & lama closing, konversi, win rate, sumber lead (terbaik ditandai; sampel < 5 lead diberi catatan), alasan batal, status follow-up. Pengguna bertanya "rumusnya?" → ulangi dengan `--rumus`. Rekap tidak memuat nomor HP.
Skill `laporan-harian-usaha` (bila nanti mendukung CRM) membaca `rekap --json` (kontrak di `references/perintah.md`).

### F. Impor, ekspor, duplikat
- `impor kontak.csv [--sumber-default ig] [--tahap-default baru] [--sebar 10]` → pratinjau (kolom dikenali, kontak baru, duplikat dilewati, baris bermasalah + nomor baris di file, jadwal) → setuju → `--ya` (cadangan dibuat dulu). Kolom dikenali otomatis: nama / no wa, hp, telepon, WhatsApp, Mobile, Number, Nomor / sumber / tahap / nilai / kebutuhan / label / catatan / follow up / tgl masuk; ekspor Google Contacts lama & baru (First/Last Name, Phone 1/2 - Value, nilai ganda `a ::: b`, Labels) dan pengekspor kontak WA (`Name,Number`). Beberapa nomor dalam satu baris → nomor HP (berlabel Mobile) dipakai, sisanya dicatat di riwayat. `.xlsx` → minta disimpan sebagai CSV. Contoh: `templates/kontak-contoh.csv`.
  - Pratinjau diawali **PERHATIAN: kolom nomor WA tidak ditemukan** → sampaikan, minta judul kolom nomor diganti `no wa`. `--ya` ditolak kecuali `--tanpa-nomor`.
  - Impor **tidak** menjadwalkan follow-up (kecuali ada kolom follow up), agar daftar harian tidak banjir. Mau disapa bertahap → `--sebar 10` (10 kontak per hari mulai hari ini).
- `ekspor [--tahap aktif] [--samarkan] [--ke file.csv] [--timpa]` → CSV `;` UTF-8 untuk Excel, aman dari formula injection. Default disimpan di folder data CRM (`.../crm/ekspor/`), bukan folder kerja; sebutkan **path lengkap** dari script ke pengguna. Ingatkan: file berisi data pribadi (script memperingatkan bila tujuan ada di dalam repositori git).
- `cek-duplikat` → nomor sama (hampir pasti orang sama) & nama sama nomor beda (periksa dulu). Gabungkan: `gabung --dari K0007 --ke K0001` (pratinjau → `--ya`).
- Pindah ke `pengingat-follow-up`: `ekspor --format pengingat [--file-pengingat <DAFTAR.csv>]` (tanpa nomor HP) → JSON `perintah_pengingat` berisi perintah `tambah --file <path lengkap>` per prospek. Konfirmasikan path `file_pengingat` ke pengguna sebelum menjalankannya; jangan jalankan dari folder proyek/repo tanpa `--file`.

### G. Pengingat otomatis (OpenClaw)
Ikuti `references/openclaw-jadwal.md`: `hari-ini` tiap pagi (default 08.00 WIB) ke **Telegram pemilik**. Jadwal hanya menjalankan perintah baca (`hari-ini`, `rekap`), tidak pernah menulis atau mengirim ke pelanggan. Tunjukkan perintah persis + jam & zona + tujuan, tanya "Lanjut? (ya/tidak)", lalu **tunggu jawaban** sebelum membuat jadwal. **JANGAN pernah mencari, membaca, atau menampilkan token/API key/kredensial** dari environment, file konfigurasi, atau riwayat; kanal Telegram diatur pengguna lewat pairing/konfigurasi OpenClaw. Kanal belum siap atau `automations add` ditolak → berhenti dan beri langkah persiapan dari referensi. WhatsApp hanya dengan nomor terpisah milik pemilik + persetujuan risiko tertulis. Beri tahu pemilik bahwa teks `hari-ini` memuat nama, nomor, tautan, **catatan obrolan terakhir, dan nilai rupiah** yang akan tersimpan di chat Telegram-nya; bila keberatan (atau kontaknya banyak) pakai `hari-ini --samarkan` atau `--tanpa-draf`. Claude Code/Codex/Cursor: pengguna cukup mengetik "follow-up hari ini" tiap pagi.

### H. Cadangan & hapus data
Cadangan otomatis sekali sehari saat ada perubahan (30 terakhir disimpan) dan sebelum impor/hapus/gabung/restore, di folder `backup-crm/` sebelah database. Manual: `backup`; daftar: `backup --daftar`; pulihkan: `restore --dari <file>` (pratinjau → `--ya`) — bisa walau database rusak total; file rusak dipindah ke `backup-crm/rusak-crm-<waktu>.db`, tidak dihapus. Rusak dan belum ada cadangan: `init --mulai-baru` (pratinjau → `--ya`), lalu impor ulang dari ekspor CSV terakhir bila ada. Cadangan harian dibuat **sebelum** perubahan pertama hari itu, jadi perubahan hari itu belum ikut. `hapus` menghapus kontak + riwayatnya permanen; sampaikan bahwa cadangan lama masih memuat data itu.

## Format output ke pengguna
- Simpan/ubah: satu-dua baris dari script, mis. `Tersimpan K0001: Bu Rina | 0812-0000-1001 | Baru | sumber Instagram | nilai Rp 450.000 | follow-up Kamis, 24 September 2026` + `Catatan:` bila ada.
- Follow-up harian: teks `hari-ini` apa adanya, diakhiri contoh balasan singkat ("terkirim K0001", "Bu Rina deal 4,2 jt", "tunda K0002 ke Senin").
- Rupiah `Rp 4.500.000`; persen `33,3%`; tanggal `Jumat, 25 September 2026` atau `25 Sep`.

## Contoh
**Input:** "Pak Budi (0812-0000-1002, referensi) nawar katering 100 box jadi 4,5 juta, mau diskusi istri. Follow-up Jumat." (hari ini Kamis 24 Sep 2026, kontak belum ada)
**Proses:** `tambah --nama "Pak Budi" --wa "0812-0000-1002" --sumber referensi --tahap ditawar --nilai "4,5 jt" --kebutuhan "katering 100 box" --followup Jumat --catatan "mau diskusi istri"`
**Output:**
```
Tersimpan K0002: Pak Budi | 0812-0000-1002 | Ditawar | sumber Referensi | nilai Rp 4.500.000 | follow-up Jumat, 25 September 2026
```
Jumat pagi, `hari-ini` (potongan):
```
HARI INI (1)
1. K0002 Pak Budi | Referensi | Ditawar | Rp 4.500.000 | katering 100 box | FU 25 Sep (hari ini) | 0812-0000-1002
   Catatan terakhir 24 Sep: "mau diskusi istri"

K0002 Pak Budi [follow-up-penawaran]:
Halo Pak Budi, saya Sari dari Dapur Bu Sari. Menindaklanjuti penawaran katering 100 box, apakah sudah sempat dipertimbangkan? Kalau ada yang kurang pas (harga, jumlah, atau jadwal), kabari saja, kita cari jalan tengahnya.
https://wa.me/6281200001002?text=Halo%20Pak%20Budi%2C%20saya%20Sari...
```
Contoh sesi lengkap: `examples/contoh-sesi-toko-kue.md`.

## Checklist sebelum menjawab
- [ ] Tidak ada pesan yang dikirim ke pelanggan oleh agent; draf ditandai "periksa lalu kirim sendiri".
- [ ] Angka, tanggal, persen dari script; `peringatan` disampaikan.
- [ ] Kontak ambigu/duplikat ditanyakan, bukan ditebak.
- [ ] Perubahan besar (termasuk `init`) sudah pratinjau + pengguna menjawab "ya" di pesan berikutnya sebelum `--ya`.
- [ ] Tidak menampilkan sintaks perintah ke pengguna awam; tanyakan dengan bahasa biasa ("Nomor WA Bu Dewi berapa?").
- [ ] Laporan untuk dibagikan memakai `--samarkan`; catatan pribadi tidak masuk draf.

## Batasan & penanganan error
- Bukan WhatsApp Business API (Platform resmi Meta), bukan inbox bersama, bukan alat broadcast. Tidak membaca chat WA otomatis; perkembangan dicatat dari cerita pemilik (atau chat yang ditempel pemilik).
- Satu database dipakai satu komputer. Jangan buka file yang sama dari dua komputer lewat Google Drive/Dropbox.
- Database terkunci (mis. jadwal sedang membaca) → script menunggu 15 detik lalu memberi pesan jelas; ulangi perintahnya. Database rusak → script menolak dengan petunjuk `backup --daftar` + `restore` (atau `init --mulai-baru` bila tidak ada cadangan); jangan hapus atau menimpa file database sendiri.
- Tanggal follow-up tanpa tahun yang baru saja lewat (mis. "20/9" diucapkan 24/9) ditolak: tanyakan maksudnya. Nilai ambigu (`5m`, `1.500 jt`, `4,5` tanpa satuan) ditolak: tanyakan ulang.
- Tautan wa.me hanya membuka WhatsApp dengan teks terisi; pengiriman tetap oleh manusia. Nomor luar negeri diterima dengan peringatan.
- Zona waktu mengikuti pengaturan (WIB default), bukan jam komputer/VPS. `info` memperingatkan bila berbeda.
- **Python tidak bisa dijalankan:** ikuti `references/tanpa-python.md` (tabel CSV manual, rumus konversi, draf manual) dan beri tahu pengguna "dihitung manual, mohon dicek".
