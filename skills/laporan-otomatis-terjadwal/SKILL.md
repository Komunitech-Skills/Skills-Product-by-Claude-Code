---
name: laporan-otomatis-terjadwal
description: Menyiapkan laporan rutin (harian/mingguan/bulanan) di OpenClaw yang otomatis terkirim ke Telegram (default) atau WhatsApp nomor terpisah -- penjualan, keuangan/kas, stok menipis, piutang jatuh tempo, ringkasan bulanan -- memakai ulang skill rekap-penjualan-csv/laporan-keuangan-emkm/arus-kas-13minggu/tagih-piutang, lalu membuat & menguji jadwal `openclaw automations`. Gunakan saat pengguna minta "laporan otomatis", "kirim laporan tiap pagi/Senin/tanggal 1", "jadwalkan rekap ke WA/Telegram", scheduled report, recurring report, auto-send report. Bukan untuk menghitung laporan sekali pakai (langsung ke skill sumbernya) atau broadcast/kirim pesan ke pelanggan.
---

# Laporan Otomatis Terjadwal

> **Aturan kerja:** Jangan menginstal paket/aplikasi (mis. `pip install`) — bila perlu, tunjukkan caranya dan biarkan pengguna yang memasang; jangan membuka atau mencari file selain yang diberikan pengguna, isi folder skill ini, dan file yang disebut di langkah kerja; jangan menulis file baru tanpa menyebut lokasinya, dan simpan hasil di folder kerja yang disepakati (bukan /tmp).

## Tujuan
Membuat pengguna OpenClaw yang awam teknologi punya laporan rutin (penjualan, kas,
stok, piutang, ringkasan bulanan) yang **otomatis terkirim** ke Telegram atau WhatsApp
tanpa mereka membuka file atau menghitung manual tiap minggu.

## Kapan digunakan
- "Buatkan laporan penjualan otomatis tiap Senin pagi."
- "Kirimi saya rekap kas mingguan ke Telegram."
- "Ingatkan stok yang menipis tiap hari."
- "Kirim ringkasan bulanan ke WA saya."
- Pengguna sudah punya file ekspor CSV rutin (kasir/marketplace/bank/aplikasi stok) dan ingin
  hasilnya dikirim otomatis, bukan dihitung manual tiap kali.

## Kapan TIDAK digunakan
- Laporan sekali pakai, tanpa perlu berulang → langsung pakai skill sumbernya (`rekap-penjualan-csv`,
  `laporan-keuangan-emkm`, `arus-kas-13minggu`, `tagih-piutang`) tanpa membuat jadwal.
- Onboarding awal / belum tahu skill apa yang cocok → `karyawan-ai-mulai`.
- Cek/perbaiki pengaturan keamanan OpenClaw → `cek-privasi-openclaw` (boleh disarankan sebagai
  langkah lanjutan, terutama sebelum mengaktifkan kanal WhatsApp).
- Mengirim pesan/promo ke **pelanggan** secara rutin (broadcast) → **tolak**, arahkan ke
  `broadcast-wa` (yang tetap perlu dikirim manual/resmi, bukan otomatis lewat OpenClaw).
- Laporan berisi identitas pasien/data kesehatan spesifik → hanya boleh angka operasional agregat
  (jumlah kunjungan, pendapatan, jam ramai), **tanpa** nama/diagnosis pasien.
- Data sumber tidak pernah ada di komputer (butuh integrasi API marketplace/kasir) → jelaskan
  bahwa OpenClaw tidak menarik data otomatis dari platform itu; solusi tahap ini adalah ekspor
  CSV manual berkala ke folder, atau arahkan ke jasa setup untuk integrasi lanjutan.

## Input — wawancara maksimal 5 pertanyaan

Tanyakan **sekali**, dalam satu pesan bernomor. Jika pengguna sudah menyebutkan sebagian di
kalimat pemicu (mis. "laporan penjualan tiap Senin pagi ke Telegram"), jangan tanya ulang hal
yang sudah jelas -- tanyakan sisanya saja.

| # | Pertanyaan | Wajib? | Default jika tidak dijawab |
|---|---|---|---|
| 1 | Laporan apa? (penjualan harian, kas mingguan, stok menipis, piutang jatuh tempo, ringkasan bulanan, atau lainnya) | Ya | Tanyakan ulang sekali; kalau tetap tidak jelas, minta contoh angka yang ingin dilihat |
| 2 | Sumber datanya di mana? Folder berisi file CSV (ekspor kasir/marketplace/bank/aplikasi stok), atau file yang akan dikirim manual ke chat setiap kali? | Ya | Sarankan folder `Dokumen/Laporan-AI/masuk/` (atau `laporan/masuk/` di workspace) |
| 3 | Jadwalnya kapan, dan komputer/laptop biasanya menyala jam segitu? (zona waktu default **Asia/Jakarta**) | Ya | Harian 07:00; mingguan Senin 07:00; bulanan tanggal 1 pukul 07:00 -- **semua WIB (Asia/Jakarta)** |
| 4 | Mau dikirim ke Telegram atau WhatsApp? | Tidak | **Telegram** (lebih aman -- lihat Langkah 4) |
| 5 | Dikirim ke siapa? (harus pemilik/admin sendiri, bukan grup/pelanggan) | Ya | Tanyakan ID chat Telegram atau nomor WA pemilik; tanpa ini jadwal tidak bisa dibuat |

Jika pengguna ingin cepat ("langsung aja", "terserah"): pakai default di atas, sebutkan
asumsinya, dan tetap **wajib** menanyakan siapa penerimanya (poin 5) karena ini menentukan ke
mana data usaha dikirim.

## Langkah kerja

> **Lokasi script:** semua script skill ini ada di subfolder `scripts/` di folder yang sama dengan SKILL.md ini (folder skill). Jalankan dari sana; jangan mencari script atau file pengguna ke seluruh disk (mis. `find /`) — itu lambat dan menyentuh data pribadi di luar folder kerja.

### 1. Pilih resep laporan
Cocokkan jawaban wawancara ke salah satu resep di `templates/`:

| Resep | File | Memakai skill/logika |
|---|---|---|
| Penjualan harian/mingguan | `templates/RESEP-penjualan.md` | `rekap-penjualan-csv` |
| Stok menipis | `templates/RESEP-stok-menipis.md` | **Jalur utama:** skill `buku-stok` (`scripts/stok.py info`/`laporan menipis`, hanya baca). **Jalur cadangan** (bila `buku-stok` tidak dipakai): CSV stok lengkap dari aplikasi kasir/inventori lain, dibaca & dibandingkan manual terhadap ambang -- skill ini **tidak** punya script hitung stok sendiri |
| Kas mingguan / proyeksi kas | `templates/RESEP-kas-mingguan.md` | `arus-kas-13minggu` |
| Piutang jatuh tempo | `templates/RESEP-piutang-jatuh-tempo.md` | `tagih-piutang` |
| Ringkasan bulanan (keuangan) | `templates/RESEP-ringkasan-bulanan.md` | `laporan-keuangan-emkm` |

Tidak ada resep yang pas (mis. laporan ads Meta/TikTok, laporan klinik)? Jelaskan jujur bahwa
resep khusus belum tersedia, lalu tawarkan menyusun manual mengikuti pola resep yang paling
mirip (kolom sumber → metrik → format pesan), dengan angka tetap lewat script pada Langkah 3.

Salin resep yang dipilih ke workspace pengguna sebagai `laporan/RESEP-<nama-laporan>.md`, isi
bagian yang bertanda `<isi>` dengan jawaban wawancara (folder sumber, kolom, jadwal, tujuan).
Ini jadi dokumentasi tetap: kalau pengguna lupa jadwalnya menghitung apa, tinggal buka file ini.

### 2. Cek kesiapan sumber data (SEBELUM menjanjikan jadwal)
Untuk resep **stok menipis dengan `buku-stok`**, langkah ini diganti oleh `stok.py info --json`
(lihat `templates/RESEP-stok-menipis.md`) -- lewati ke Langkah 3. Untuk resep berbasis CSV
(penjualan, kas, piutang, ringkasan bulanan, atau stok tanpa `buku-stok`):

```bash
python3 <folder-skill-ini>/scripts/cek_sumber_data.py --folder "<folder-sumber>" \
  --pola "*.csv" --label "<label-data, mis. penjualan>" --maks-umur-hari <lihat tabel>
```
(Windows: ganti `python3` dengan `python` atau `py`.)

**`--maks-umur-hari` HARUS lebih ketat dari irama jadwal**, supaya file basi (mis. ekspor minggu
lalu yang lupa diganti) tidak lolos tanpa peringatan dan terkirim ulang seolah data baru:

| Jadwal | `--maks-umur-hari` |
|---|---|
| Harian | `1` |
| Mingguan | `6` |
| Bulanan | `27` |

- Kalau `"siap": false` → **jangan lanjut membuat jadwal**. Tunjukkan `pesan` dari hasil JSON
  apa adanya ke pengguna, minta mereka menyiapkan file dulu, lalu berhenti di sini.
- Kalau ada `peringatan` (mis. file sudah lama) → sampaikan ke pengguna sebelum lanjut.
- Kalau pengguna kemungkinan mengekspor **satu file per hari** (dilihat dari `file_lain_cocok`
  di hasil, atau langsung ditanyakan) padahal jadwalnya mingguan/bulanan: jalankan ulang dengan
  `--daftar-semua`, lihat daftar `file_cocok`, lalu **gabungkan** (concat, satu baris header saja)
  file-file yang tanggalnya masuk periode target menjadi satu file sebelum Langkah 3. Kalau
  pengguna hanya punya satu ekspor per periode (disarankan, lebih sederhana), langkah ini tidak
  perlu.

### 3. Hitung & rakit contoh laporan (uji manual pertama)
1. Jalankan script skill sumber sesuai resep (lihat tabel Langkah 1 dan `SKILL.md` skill
   tersebut untuk argumen lengkap), dengan file (atau file gabungan) dari Langkah 2.
2. **Cek periode hasil terhadap periode yang diminta.** Kalau script sumber mengembalikan
   rentang tanggal (mis. `periode.awal`/`periode.akhir` dari `rekap-penjualan-csv`), bandingkan
   dengan periode yang seharusnya dicakup jadwal ini (mis. laporan Senin pagi = Senin-Minggu
   minggu lalu). Kalau rentangnya **tidak mencakup penuh** periode itu (mis. cuma 1 hari untuk
   laporan mingguan, atau bulan yang salah) -- **jangan kirim sebagai laporan periode itu**.
   Beri tahu pengguna: "Data yang tersedia mencakup <awal>-<akhir>, bukan seluruh <periode yang
   diminta>" dan hentikan (sama seperti data kosong -- lihat Langkah 2), jangan diam-diam
   mengirim angka yang cakupannya berbeda dari yang dijanjikan ke pengguna.
3. Ambil angka-angka kunci dari output JSON script itu (JANGAN mengarang atau membulatkan
   sendiri -- salin apa adanya).
4. Susun JSON pesan (lihat skema di `scripts/susun_pesan.py`, bagian atas file) berisi maksimal
   4-6 baris angka utama + 1 daftar pendek (mis. 3-5 produk terlaris) -- **tanpa nama/kontak
   pelanggan perorangan**, sesuai UU PDP. Isi `catatan` dengan hal netral (mis. cakupan periode),
   dan `peringatan` dengan hal yang perlu diwaspadai (mis. baris dilewati, data mendekati batas
   umur) -- keduanya tampil beda di pesan akhir (lihat Langkah 4 `susun_pesan.py`).
5. Format pesan akhir:
   ```bash
   python3 <folder-skill-ini>/scripts/susun_pesan.py --data <file-json-pesan> --maks-baris 15
   ```
   - Exit code **3** berarti script mendeteksi pola mirip data pribadi (NIK/KTP/nomor HP/email)
     di salah satu baris (lihat pesan di stderr, bukan di pesan itu sendiri). **Berhenti**,
     tinjau ulang baris yang dituding bersama pengguna, dan jangan lanjut membuat/mengaktifkan
     jadwal sebelum yakin baris itu memang aman (agregat, bukan identitas orang) atau sudah
     dihapus dari pesan.
6. Tunjukkan hasil pesan ini ke pengguna sebagai **contoh laporan pertama**, sebelum jadwal
   dibuat, supaya mereka tahu persis apa yang akan mereka terima nanti.

### 4. Tentukan kanal pengiriman
- **Telegram = default.** Kalau belum ada bot: pandu buat bot lewat @BotFather, lalu
  `openclaw channels add --channel telegram --token <token>` (lihat `references/openclaw.md`
  §3). Tidak ada risiko blokir karena memakai API resmi. Perintah `channels add` itu **diketik
  pengguna sendiri**; agent tidak pernah meminta token ditempel di chat dan tidak pernah mencarinya
  di environment, `openclaw.json`, atau riwayat.
- **WhatsApp hanya dengan syarat berikut, semuanya harus dipenuhi:**
  1. Nomor **terpisah** dari nomor WA usaha/pribadi utama (dokumentasi resmi OpenClaw sendiri
     menyarankan ini).
  2. Laporan **hanya** dikirim ke pemilik sendiri -- **tidak pernah** ke grup atau pelanggan.
  3. Pengguna sudah membaca peringatan risiko dan **setuju secara tertulis** (balasan "ya, saya
     mengerti risikonya") sebelum jadwal WA dibuat: *"OpenClaw memakai WhatsApp Web (tidak
     resmi, lewat scan QR), bukan WhatsApp Business API resmi. Syarat Layanan WhatsApp melarang
     pengiriman pesan otomatis massal/non-personal, sehingga ada risiko nomor diblokir. Untuk
     laporan ke diri sendiri risikonya rendah (volume kecil, ke nomor sendiri), tapi tetap ada.
     Telegram tidak punya risiko ini. Lanjut pakai WhatsApp, atau pindah ke Telegram?"*
  4. Nomor pemilik harus sudah ada di `allowFrom` kanal WA itu (lihat `references/openclaw.md`
     §4) supaya jadwal boleh mengirim proaktif ke DM.
- Jika pengguna tetap ingin kirim ke **grup** atau ke **banyak pelanggan** sekaligus: **tolak**,
  jelaskan ini melanggar ToS WhatsApp (dianggap bulk/auto-messaging) dan aturan Komunitech,
  arahkan ke `broadcast-wa` (dikirim manual/resmi, bukan otomatis).

### 5. Buat jadwal (SELALU minta izin eksplisit sebelum menjalankan perintah)
Ringkas dulu ke pengguna: laporan apa, dari data mana, jadwal & zona waktu, dikirim ke kanal &
tujuan apa. Minta konfirmasi "Lanjut? (ya/tidak)", lalu **berhenti dan tunggu balasan** (permintaan
awal bukan persetujuan). Perintah ditolak (`requires credentials`, `token missing`, Gateway mati) →
berhenti, beri langkah persiapan; jangan menyelidiki kredensial. Setelah "ya", jalankan (lihat
`references/openclaw.md` §1-§2 untuk semua opsi & alasan pemilihannya; Windows: `python`/`py`):

```bash
openclaw automations add "<jadwal cron, mis. 0 7 * * 1>" \
  "Jalankan resep laporan di laporan/RESEP-<nama>.md untuk periode <periode>. Tulis ringkas dalam Bahasa Indonesia, maksimal 15 baris, angka penting di atas, format Rupiah 'Rp 1.250.000', TANPA nama/kontak pelanggan perorangan. Kalau file sumber belum ada/kosong, katakan itu dengan jelas -- JANGAN kirim angka nol." \
  --name "<Nama jadwal, mis. Laporan penjualan Senin>" --tz "Asia/Jakarta" --session isolated \
  --announce --channel telegram --to "<ID chat Telegram pemilik>"
```
Ini "Bentuk A" (jadwal & pesan sebagai argumen posisi, TANPA `--cron`) -- **jangan** menambahkan
`--cron`/`--at`/`--every` di perintah ini sekaligus, karena begitu salah satunya dipakai,
argumen posisi pertama berarti nama job, bukan jadwal, dan bentrok dengan `--name` (CLI menolak).
Untuk pengingat sekali jalan (`--at`) atau interval (`--every`), pakai "Bentuk B" (opsi penuh,
tanpa argumen posisi) -- lihat `references/openclaw.md` §1 untuk kedua bentuk lengkap, keduanya
sudah dibuktikan jalan di Gateway uji.

Untuk WhatsApp (hanya setelah syarat §4 dipenuhi): ganti baris terakhir dengan
`--channel whatsapp --to "+62..."`.

Kalau `exec`/perintah komputer tidak diizinkan di platform yang dipakai (atau bukan OpenClaw):
beri perintah ini sebagai teks siap salin-tempel untuk dijalankan pengguna sendiri di terminal
tempat OpenClaw berjalan, atau arahkan ke Control UI (`Settings → Automations`).

**Ambil `id` dari hasil `add`** (field `"id"` di output JSON, mis.
`"1307d905-fe39-4490-9b62-2468ee9e1b94"`) dan **pakai id itu** untuk semua langkah berikutnya
(6-7). `run`/`disable`/`enable`/`edit`/`rm` **hanya menerima id, BUKAN nama** -- diuji langsung
di Gateway OpenClaw: memakai nama di situ menjawab `"Automation not found"`. Kalau id tidak
sempat dicatat, cari lagi dengan `openclaw automations list --json` (cocokkan lewat field
`"name"`) atau `openclaw automations show "<nama persis>" --json` (`show` saja yang menerima
nama persis selain id).

### 6. Uji sekali sebelum aktif
```bash
openclaw automations run <id> --wait
```
Tunjukkan hasil run ini ke pengguna sebagai bukti jadwal bekerja, **sebelum** menyatakan jadwal
"aktif". Kalau run gagal atau hasilnya beda dari contoh Langkah 3, cek lagi resep/argumen --
jangan aktifkan jadwal yang belum terbukti jalan.

### 7. Jelaskan cara melihat/menjeda/mengubah/menghapus jadwal
Sertakan ringkasan ini ke pengguna setelah jadwal aktif (detail lengkap di
`references/openclaw.md` §5):
```bash
openclaw automations list --all          # lihat semua jadwal (termasuk yang nonaktif)
openclaw automations show <id>            # lihat detail satu jadwal (juga menerima nama persis)
openclaw automations disable <id>         # jeda sementara (WAJIB id)
openclaw automations enable <id>          # aktifkan lagi (WAJIB id)
openclaw automations edit <id> --cron "..." --to "..."   # ubah jadwal/tujuan (WAJIB id)
openclaw automations rm <id>              # hapus permanen (WAJIB id)
```
Ingatkan pengguna: kalau lupa id, jalankan `openclaw automations list --all` dulu untuk
mencarinya lewat nama jadwal.

### 8. Ingatkan syarat "komputer harus menyala"
Jelaskan **sebelum** jadwal dianggap selesai (lihat `references/mesin-24-jam.md` untuk teks
lengkap & opsi): jadwal berjalan di dalam proses Gateway OpenClaw -- kalau komputer mati/tidur
saat jam jadwal, laporan **tidak terkirim**. Tawarkan 3 opsi (laptop/mini PC yang selalu
menyala, VPS milik member sendiri, atau **jasa setup Komunitech** -- disebut sebagai opsi,
tanpa menyebut harga) dan sarankan `cek-privasi-openclaw` sebagai langkah lanjutan bila kanal
baru saja dibuka ke WhatsApp/publik.

## Format output
Pesan laporan mengikuti keluaran `susun_pesan.py`: judul tebal, subjudul (periode), lalu
maksimal ~15 baris berisi angka penting dahulu, daftar pendek (opsional), catatan netral, dan
peringatan (⚠️) di bagian bawah bila ada -- catatan & peringatan tampil beda supaya pengguna
tahu mana info biasa dan mana yang perlu diwaspadai. Contoh lengkap tiap resep ada di
`references/contoh-pesan.md`.

## Contoh
**Input pengguna:** "Buatkan laporan penjualan otomatis tiap Senin jam 7 pagi, kirim ke
Telegram saya."

**Alur:** tanyakan sumber data & tujuan (ID chat Telegram) → cek folder sumber siap (umur data <
6 hari untuk mingguan) → hitung lewat `rekap-penjualan-csv` → cek periode hasil mencakup Senin-
Minggu lalu → rakit & tunjukkan contoh pesan → buat jadwal
`openclaw automations add "0 7 * * 1" ... --tz Asia/Jakarta --announce --channel telegram --to "<chat-id>"`
→ catat `id` dari hasilnya → uji dengan `openclaw automations run <id> --wait` → tunjukkan cara
lihat/jeda/hapus jadwal (pakai `id`) → ingatkan syarat komputer menyala.

## Checklist sebelum jadwal dianggap aktif
- [ ] Sumber data sudah dicek (`cek_sumber_data.py` atau `stok.py info` untuk buku-stok) dan
      berstatus siap (atau pengguna sudah diberi tahu apa yang kurang, dan proses berhenti di
      situ). `--maks-umur-hari` sesuai irama jadwal (harian 1 / mingguan 6 / bulanan 27).
- [ ] Periode hasil hitung sudah dicek mencakup penuh periode yang diminta (Langkah 3.2) --
      bukan cuma 1 hari untuk laporan mingguan, dsb.
- [ ] Contoh laporan pertama sudah ditunjukkan ke pengguna sebelum jadwal dibuat.
- [ ] `susun_pesan.py` tidak keluar dengan exit code 3 (indikasi data pribadi) untuk contoh ini,
      atau sudah ditinjau ulang bersama pengguna sampai aman.
- [ ] Penerima adalah pemilik/admin sendiri, bukan grup/pelanggan.
- [ ] Kalau kanal WhatsApp: nomor terpisah + persetujuan risiko tertulis sudah didapat.
- [ ] `id` jadwal (dari hasil `automations add`) sudah dicatat.
- [ ] Jadwal sudah diuji sekali (`automations run <id> --wait`) dan hasilnya sesuai sebelum
      dianggap aktif.
- [ ] Pengguna sudah diberi tahu cara melihat/menjeda/mengubah/menghapus jadwal (dengan `id`).
- [ ] Pengguna sudah diberi tahu jadwal butuh komputer menyala terus + opsi-opsinya.

## Batasan & penanganan error
- **Kredensial & jadwal (wajib):** JANGAN pernah mencari, membaca, atau menampilkan token/API key/kredensial dari environment (`env`, `printenv`), file konfigurasi (mis. `openclaw.json`, `.env`), atau riwayat; kanal Telegram diatur lewat pairing/konfigurasi OpenClaw oleh pengguna sendiri. Buat jadwal hanya setelah pengguna membalas "ya" atas perintah + jam yang ditunjukkan; kanal belum siap atau perintah ditolak → berhenti dan beri langkah persiapannya, jangan menyelidiki sendiri.
- **Data tidak ada/kosong → tidak pernah mengirim angka nol.** Selalu jalankan
  `cek_sumber_data.py` dulu; kalau tidak siap, hentikan proses dan tunjukkan pesannya apa
  adanya. Prompt automation juga sudah diberi instruksi eksplisit untuk melakukan hal yang sama
  saat jadwal berjalan sendiri nanti (lihat Langkah 5).
- **Tidak ada broadcast/kirim massal.** Tujuan pengiriman selalu satu penerima (pemilik/admin),
  tidak pernah grup atau banyak pelanggan sekaligus.
- **Data basi/tidak lengkap tidak pernah dikirim seolah data terbaru.** `--maks-umur-hari` diatur
  lebih ketat dari irama jadwal (Langkah 2), dan periode hasil hitung selalu dicek terhadap
  periode yang diminta (Langkah 3.2) sebelum dikirim. Folder dengan banyak file per periode
  (mis. ekspor harian untuk laporan mingguan) memakai `--daftar-semua` + penggabungan file,
  bukan hanya file terbaru.
- **Tanpa data pribadi pelanggan.** `susun_pesan.py` mendeteksi (bukan memblokir) pola NIK/KTP/
  nomor HP/email dengan batas kata (tidak salah kena kata seperti "unik"/"Klinik") dan keluar
  dengan **exit code 3** bila ada -- penjelasannya hanya di stderr, **tidak** ditambahkan ke isi
  pesan yang dikirim. Exit code ini WAJIB ditindaklanjuti (lihat Langkah 3.5): tinjau ulang baris
  yang dituding sebelum mengaktifkan jadwal. Laporan piutang/CS hanya boleh berisi jumlah/nominal
  agregat, bukan daftar nama+kontak.
- **Klinik/kesehatan:** hanya angka operasional agregat (kunjungan, pendapatan, jam ramai).
  Jangan pernah menjadwalkan laporan berisi nama pasien atau diagnosis.
- **Gateway harus menyala** saat jam jadwal -- kalau tidak, run tidak pernah terjadi (bukan
  gagal dengan pesan error, tapi memang tidak berjalan). Ini bukan bug skill; jelaskan ke
  pengguna dan arahkan ke `references/mesin-24-jam.md`.
- **Buat jadwal lewat chat WhatsApp:** menurut riset OpenClaw ini masih perlu diuji langsung
  (`docs.openclaw.ai` menyebut mendukung, tapi kombinasi persisnya belum dicoba tim kami saat
  skill ini ditulis). Jika perintah `openclaw automations add` gagal atau berperilaku aneh saat
  dipicu dari chat WA, jelaskan itu ke pengguna dan tawarkan menjalankan perintah yang sama dari
  Control UI atau terminal.
- **Setiap run memakai token model** (biaya ditanggung pengguna). Sarankan `--session isolated`
  (sudah dipakai di contoh) supaya jadwal tidak mencampuri sesi chat utama, dan model yang lebih
  hemat untuk laporan rutin bila tersedia (`--model`).
- **Python tidak bisa dijalankan:** hitung manual mengikuti langkah script sumber (lihat
  `SKILL.md` skill itu masing-masing) dan beri tahu pengguna bahwa hasil belum diverifikasi
  script; untuk `cek_sumber_data.py`, cukup periksa manual apakah folder ada isinya dan file
  tidak 0 byte sebelum melanjutkan.
- **Jangan mengirim isi file pengguna ke layanan eksternal.** Semua perhitungan berjalan lokal;
  yang keluar dari komputer hanya teks yang dikirim ke penyedia model AI (sama seperti percakapan
  biasa) dan pesan hasil ke Telegram/WhatsApp yang dipilih pengguna sendiri.
