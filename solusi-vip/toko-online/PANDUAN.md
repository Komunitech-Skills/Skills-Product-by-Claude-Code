# Panduan Solusi VIP — Toko Online

Panduan ini untuk pemilik toko online/marketplace (Shopee, Tokopedia, TikTok Shop, atau toko
offline+online) yang sudah jadi member VIP komunitech.com. Bahasa sehari-hari, langkah demi
langkah. Setiap langkah punya **cara cek berhasil** dan **kalau gagal**.

Tidak perlu paham istilah teknis. Kalau ragu di satu langkah, berhenti di situ dan tanya ke
grup member/Komunitech — jangan lanjut menebak.

---

## 0. Prasyarat

1. **OpenClaw sudah terpasang dan bisa diajak chat.** Semua member VIP memang sudah memakai
   OpenClaw. Kalau belum pernah dipakai sama sekali, buka chat OpenClaw dan pastikan bisa
   membalas pesan biasa dulu (ketik "halo").
   - **Cara cek berhasil:** OpenClaw membalas pesan "halo" Anda.
   - **Kalau gagal:** OpenClaw belum aktif/terpasang. Ikuti pemasangan awal OpenClaw dulu
     (`https://openclaw.ai/install.sh` untuk Mac/Linux, installer Windows dari situs resmi), atau
     minta jasa setup Komunitech.

2. **Komputer/mesin yang menjalankan OpenClaw perlu menyala terus** supaya laporan otomatis dan
   pengingat benar-benar terkirim di jamnya. Ini **bukan** soal komputer yang Anda pakai chat —
   ini soal komputer tempat **Gateway OpenClaw** berjalan. Kalau mati/tidur di jam jadwal,
   laporan **tidak terkirim**, tanpa pesan error apa pun. Pilih salah satu:
   - **(a) Laptop/PC toko yang memang biasa menyala di jam kerja** (mis. 07.00–21.00) — paling
     mudah, tidak perlu apa-apa lagi, asal jadwal laporan dipasang di jam itu.
   - **(b) Mini PC atau laptop bekas yang dikhususkan menyala 24 jam** — cocok kalau Anda mau
     laporan jam berapa pun, termasuk malam.
   - **(c) VPS (server sewaan) milik Anda sendiri** — menyala 24 jam tanpa tergantung komputer
     fisik, tapi ada biaya langganan bulanan dan sedikit langkah teknis (dokumentasi resmi
     OpenClaw punya panduan pasang di VPS/Hetzner/DigitalOcean/dll.).
   - **(d) Tidak nyaman menyiapkan sendiri?** Komunitech menawarkan **jasa setup berbayar** untuk
     memasang & menguji mesin/VPS 24 jam ini. Hubungi tim Komunitech untuk detail biaya —
     panduan ini sengaja tidak menyebut angka harga.
   - **Cara cek berhasil:** Anda tahu persis mesin mana yang menjalankan OpenClaw, dan mesin itu
     akan menyala di jam-jam laporan yang Anda pilih di Langkah 5.
   - **Kalau gagal / belum yakin:** pilih opsi (a) dulu dengan jadwal jam kerja saja. Jangan
     janjikan laporan jam 21.00 kalau toko tutup dan komputer dimatikan jam 18.00.

---

## 1. Pasang paket skill Toko Online

Paket ini berisi (folder skill, dari member area/ZIP paket VIP Anda): `karyawan-ai-mulai`,
`cek-privasi-openclaw`, `listing-marketplace`, `harga-jual-marketplace`,
`balas-ulasan-pelanggan`, `analisis-ulasan`, `promo-kalender`, `naskah-live-jualan`, `buku-stok`,
`agen-cs-toko`, `foto-produk-brief`, `laporan-otomatis-terjadwal`, `rekap-penjualan-csv`,
`konten-mingguan`, `pesan-prospek-wa`, `crm-wa`, `analisis-excel`, `brainstorming-ide-usaha`.

**Cara paling andal (disarankan untuk OpenClaw):**
```bash
openclaw skills install ./karyawan-ai-mulai --global
openclaw skills install ./cek-privasi-openclaw --global
openclaw skills install ./listing-marketplace --global
openclaw skills install ./harga-jual-marketplace --global
openclaw skills install ./balas-ulasan-pelanggan --global
openclaw skills install ./analisis-ulasan --global
openclaw skills install ./promo-kalender --global
openclaw skills install ./naskah-live-jualan --global
openclaw skills install ./buku-stok --global
openclaw skills install ./agen-cs-toko --global
openclaw skills install ./foto-produk-brief --global
openclaw skills install ./laporan-otomatis-terjadwal --global
openclaw skills install ./rekap-penjualan-csv --global
openclaw skills install ./konten-mingguan --global
openclaw skills install ./pesan-prospek-wa --global
openclaw skills install ./crm-wa --global
openclaw skills install ./analisis-excel --global
openclaw skills install ./brainstorming-ide-usaha --global
```
(Jalankan dari folder tempat Anda mengekstrak ZIP paket, sehingga `./nama-skill` adalah folder
yang berisi `SKILL.md` langsung di dalamnya. Windows: kalau tidak lewat WSL, salin folder ke
`%USERPROFILE%\.openclaw\skills\` lewat File Explorer — lihat `docs/instalasi.md` bagian "Cara
termudah: lewat File Explorer/Finder".)

Atau, kalau Gateway Anda punya halaman **Plugins → Skills** dengan tombol impor: gunakan itu satu
per satu (fitur ini tersedia di sebagian instalasi Gateway, bukan semua — kalau tidak ada
tombolnya, pakai cara `openclaw skills install` di atas).

- **Cara cek berhasil:** ketik `openclaw skills list` — semua 18 nama skill di atas muncul. Atau
  ketik di chat: "skill apa saja yang saya punya?" (bila `exec` diizinkan agent akan menjalankan
  `openclaw skills list` untuk Anda).
- **Kalau gagal:**
  - Pesan "already exists" → skill itu sudah terpasang, aman dilewati.
  - Skill tidak muncul di `skills list` tapi Anda yakin sudah pasang → pastikan yang disalin
    adalah folder skill (langsung ada `SKILL.md` di dalamnya), bukan folder ZIP pembungkusnya.
    Buka sesi/chat OpenClaw yang baru (ketik `/new` kalau tersedia) — skill baru terbaca di
    percakapan berikutnya, bukan langsung di percakapan yang sedang berjalan.
  - `exec`/perintah komputer ditolak → salin folder secara manual lewat File Explorer/Finder ke
    `~/.openclaw/skills/`.

---

## 2. Jalankan `karyawan-ai-mulai` (mulai kerja dalam 1 percakapan)

Ketik di chat OpenClaw: **"mulai karyawan AI"** atau **"bantu saya mulai pakai AI untuk toko
saya"**.

Anda akan ditanya maksimal 5 pertanyaan (profesi/usaha, skala tim, 3 pekerjaan paling menyita
waktu, kanal favorit, dan soal privasi/komputer menyala). Kalau ingin cepat, jawab "cepat saja" —
skill akan pakai jawaban default yang masuk akal dan menyebutkan asumsinya.

- **Cara cek berhasil:** Anda menerima ringkasan kebutuhan, rekomendasi 3 skill pertama, **dan
  satu hasil nyata siap pakai** (mis. 3 draf caption promo) dalam percakapan yang sama — bukan
  cuma penjelasan umum.
- **Kalau gagal:** kalau skill tidak terpicu otomatis, panggil namanya langsung: "pakai skill
  karyawan-ai-mulai". Kalau rekomendasi menyebut skill yang ternyata tidak ada foldernya di paket
  Anda, itu akan dikatakan jujur ("belum tersedia di paket Anda") — bukan bug, tapi batas paket.

---

## 3. Jalankan `cek-privasi-openclaw`

Setelah skill terpasang (terutama `agen-cs-toko`, yang membaca pesan pelanggan), ketik: **"cek
privasi saya"**.

Skill akan menjalankan `openclaw security audit --json` dan memeriksa beberapa pengaturan
(`config get`/`approvals get`), lalu memberi laporan lampu lalu lintas (🔴/🟡/🟢) dengan bahasa
awam. **Perbaikan hanya dijalankan satu per satu, dengan izin Anda** — tidak ada yang diubah
diam-diam.

- **Cara cek berhasil:** Anda menerima laporan dengan minimal daftar 🟢/🟡/🔴 dan penjelasan
  "efek yang berhenti bekerja" untuk tiap saran perbaikan, bukan cuma daftar teknis mentah.
- **Kalau gagal:** kalau `exec` tidak diizinkan, skill memberi perintah salin-tempel untuk
  dijalankan sendiri di terminal tempat OpenClaw berjalan, lalu tempel hasilnya kembali ke chat.
- Jalankan skill ini **lagi** setiap kali Anda memasang skill baru yang membaca pesan orang lain
  (mis. setelah mengaktifkan `agen-cs-toko`).

---

## 4. Hubungkan bot Telegram (kanal default)

Ini kanal **resmi** dan **tanpa risiko blokir**, jadi jadi default untuk semua laporan/rekap ke
Anda sebagai pemilik.

1. Buka Telegram, cari **@BotFather**, kirim `/newbot`, ikuti instruksinya (beri nama bot), salin
   **token** yang diberikan.
2. Ketik ke OpenClaw: *"Tambahkan kanal Telegram dengan token ini: <token>"*, atau jalankan
   sendiri:
   ```bash
   openclaw channels add --channel telegram --token <token-dari-BotFather>
   ```
3. Buka chat dengan bot Anda di Telegram, kirim pesan apa saja (mis. "halo"). Ini memicu
   **pairing** — persetujuan untuk pengirim baru.
4. Setujui pairing (kalau tidak otomatis tersetujui): `openclaw pairing list telegram`, lalu
   `openclaw pairing approve telegram <KODE>` (kode berlaku 1 jam).
5. Catat **ID chat Telegram** Anda — dibutuhkan untuk semua jadwal di Langkah 5. Cara paling
   mudah untuk pemula: buka chat dengan bot **@userinfobot** di Telegram, dia akan menampilkan ID
   Anda. Simpan angka itu.

- **Cara cek berhasil:** bot Telegram Anda membalas pesan "halo" dengan jawaban dari OpenClaw,
  dan Anda sudah punya angka ID chat.
- **Kalau gagal:**
  - Bot tidak membalas → pastikan token disalin persis (tanpa spasi tambahan), dan pairing sudah
    disetujui.
  - Tidak tahu cara lihat ID chat → gunakan @userinfobot, atau minta tim Komunitech membantu di
    sesi pendampingan.

**Soal WhatsApp:** paket ini **tidak** memakai WhatsApp untuk laporan otomatis secara bawaan.
Kalau Anda tetap ingin WA untuk notifikasi ke diri sendiri, baca dulu kotak peringatan di
`jadwal-openclaw.md` §"WhatsApp" — wajib nomor terpisah + persetujuan risiko tertulis.

---

## 5. Rutinitas harian & mingguan Toko Online

Setelah Langkah 1–4 selesai, aktifkan otomasi berikut **satu per satu**, uji dulu sebelum
percaya jadwalnya aktif. Detail perintah lengkap + status verifikasi ada di
`jadwal-openclaw.md` — di sini ringkasannya.

### a. Laporan harian jam 21.00 (omzet + stok menipis)
Ketik: *"Buatkan laporan toko harian jam 9 malam, kirim ke Telegram."*
Isinya: omzet hari ini, produk terlaris, stok menipis/habis, barang tidak laku, nilai
persediaan (dari `buku-stok` bila Anda sudah mencatat stok di sana, atau dari
`rekap-penjualan-csv` kalau sumbernya file penjualan CSV/Excel).
- **Cara cek berhasil:** setelah dibuat, skill akan **menguji jadwal itu sekali saat itu juga**
  (`openclaw automations run <id> --wait`) dan menunjukkan hasilnya ke Anda **sebelum**
  menyatakan jadwal aktif.
- **Kalau gagal:** kalau folder data kosong/file belum ada, laporan akan bilang jujur "data belum
  ada di folder X" — bukan mengarang angka. Isi folder data yang ditunjuk, lalu uji ulang.

### b. Stok menipis (bagian dari laporan harian, atau terpisah)
Sudah termasuk di laporan (a) kalau Anda memakai `buku-stok`. Kalau ingin laporan stok terpisah
dari laporan omzet, minta: *"Kirim laporan stok menipis saja tiap pagi jam 8."*

### c. Balas ulasan pelanggan (manual, dipicu Anda — bukan jadwal)
Kapan pun ada ulasan baru di Shopee/Tokopedia/TikTok Shop/Google Maps, tempel isi ulasannya dan
ketik: *"Balaskan ulasan ini."* `balas-ulasan-pelanggan` menyiapkan draf balasan — **Anda yang
menempelkan balasannya** ke platform. Ini bukan jadwal otomatis karena ulasan baru datang kapan
saja, bukan di jam tetap.

### d. Konten mingguan (paket konten Jumat sore + pengingat posting harian)
Ketik: *"Tiap Jumat sore kirimi saya paket konten minggu depan untuk toko saya."*
Anda akan menerima 5–7 ide konten + caption siap tempel + jam posting yang disarankan, dikirim
tiap Jumat, plus pengingat ringan tiap pagi berisi caption hari itu.
- **Penting:** OpenClaw **tidak memposting otomatis** ke Instagram/TikTok/Facebook. Paket konten
  disiapkan, Anda yang menjadwalkan lewat penjadwal bawaan platform (mis. Meta Business Suite)
  atau posting manual.
- **Cara cek berhasil:** paket konten pertama diuji langsung (dijalankan sekali) sebelum jadwal
  Jumat sungguhan aktif.
- **Kalau gagal:** kalau profil usaha belum tersimpan, skill akan menanyakannya sekali di awal —
  jawab sekali saja, tidak perlu diulang tiap minggu.

### e. Agen CS (mode Copilot, harian sesuai kebutuhan)
Teruskan/tempel chat pelanggan ke bot (lewat Telegram, atau WA ke diri sendiri kalau Anda sudah
siapkan nomor terpisah), lalu ketik: *"Siapkan asisten CS toko saya"* (sekali, untuk membuat
basis pengetahuan) lalu selanjutnya cukup tempel chat pelanggan untuk minta draf balasan. **Anda
selalu yang mengirim balasan ke pelanggan** — bot tidak pernah mengirim otomatis ke pelanggan di
paket ini. Rekap harian pertanyaan pelanggan bisa dijadwalkan (lihat `jadwal-openclaw.md` §CS).

### f. Pesan perkenalan ke calon pelanggan/reseller baru (manual, dipicu Anda)
Dapat kontak baru dari pameran, Google Maps, IG, atau referral dan mau kirim chat pembuka? Ketik:
*"Saya dapat kontak toko oleh-oleh ini dari pameran UMKM kemarin, mau nawarin jadi reseller,
tolong bikinkan pesan perkenalannya."* `pesan-prospek-wa` menulis 3 varian pesan (singkat/
sedang/dengan nilai), sudah dicek script (bukan spam, jam kirim wajar, ada opsi keluar) plus
tautan wa.me. **Anda yang mengirim satu per satu** — bukan untuk banyak kontak sekaligus (kalau
butuh kirim promo massal, itu `broadcast-wa`, bukan skill ini).
- **Kalau gagal:** kalau Anda belum menyebutkan dari mana kontak itu didapat, skill akan
  menanyakannya dulu — pesan tidak dibuat sebelum asal kontak jelas (wajib, aturan UU PDP).

### g. Catat calon pembeli & follow-up harian (CRM lokal)
Ketik: *"Catat: Bu Rina dari IG, 0812-xxxx, tanya kue ulang tahun, kira-kira 450 ribu."* atau
*"Bu Rina jadi order 4,2 juta."* — `crm-wa` menyimpan semuanya di **database di komputer Anda
sendiri** (bukan cloud/langganan bulanan). Anda bisa mengaktifkan pengiriman daftar "siapa yang
harus di-follow-up hari ini" (lengkap dengan **draf pesan + tautan wa.me**) ke Telegram setiap
pagi — lihat `jadwal-openclaw.md` §7.
- **Cara cek berhasil:** ketik "hari ini saya harus follow-up siapa saja?" — daftar & draf pesan
  muncul dari database, bukan karangan.
- **Kalau gagal:** kalau baru mulai dan database belum ada, skill akan menanyakan nama usaha &
  nama pengirim sekali di awal, lalu langsung siap dipakai.
- **Bukan untuk kirim otomatis/broadcast.** Draf disiapkan, **Anda yang membuka tautan & menekan
  Kirim** sendiri — sama seperti `pesan-prospek-wa`.

### h. Analisis data Excel/CSV toko (manual, dipicu Anda)
Kalau Anda punya file Excel/CSV sendiri (bukan ekspor kasir/marketplace — untuk itu pakai
`rekap-penjualan-csv`), misalnya biaya operasional atau data stok manual, kirim filenya lalu
ketik: *"Analisis file ini, pengeluaran terbesar di mana?"* atau *"Bandingkan Agustus vs
September."* `analisis-excel` menjawab dengan tabel siap tempel dan angka yang **dihitung
script**, bukan dikira-kira.
- **Kalau gagal:** kalau file berformat tidak biasa (banyak tabel dalam satu sheet, baris Total
  di tengah), skill akan menandai bagian yang meragukan dan bertanya dulu sebelum memberi angka
  final — jangan minta "pokoknya langsung jawab" untuk file seperti itu.

### i. Brainstorming ide usaha/promo baru (manual, dipicu Anda)
Bingung mau jualan apa lagi, butuh ide promo, atau usaha sedang sepi? Ketik: *"Usaha laundry
saya sepi, ada ide promo atau produk tambahan?"* `brainstorming-ide-usaha` menggali batasan nyata
Anda (modal, waktu, SDM), memunculkan beberapa pendekatan, menyaringnya dengan skor (bukan
feeling), lalu menutup dengan **rencana aksi 7 hari** yang bisa langsung dikerjakan.
- **Cara cek berhasil:** Anda menerima 2–3 ide dengan untung-rugi masing-masing + rencana 7 hari,
  bukan cuma daftar ide acak.

---

## 6. Setelah semua jadwal aktif

- Cek jadwal apa saja yang aktif kapan saja dengan: *"jadwal apa saja yang aktif?"* (agent
  menjalankan `openclaw automations list --all`).
- Kalau ingin menjeda sementara (mis. libur toko): *"jeda dulu laporan harian toko saya"*.
- Ulangi `cek-privasi-openclaw` setiap kali Anda menambah kanal baru (WA nomor terpisah) atau
  agen CS baru.
- Isi `CEKLIS.md` bersama pemilik/teknisi jasa setup sebagai bukti serah-terima.
