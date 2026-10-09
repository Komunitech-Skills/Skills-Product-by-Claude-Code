# Panduan Solusi VIP — Usaha Offline (Kafe/Warung/Toko Fisik/Bengkel/Laundry)

Panduan ini untuk pemilik usaha yang jualannya **utamanya tatap muka**: kafe/resto/warung
makan, warung/toko kelontong, bengkel, laundry, dan sejenisnya — yang sudah jadi member VIP
komunitech.com. Bahasa sehari-hari, langkah demi langkah. Setiap langkah punya **cara cek
berhasil** dan **kalau gagal**.

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
   ini soal komputer tempat **Gateway OpenClaw** berjalan (untuk usaha offline, idealnya komputer
   kasir/kantor toko). Kalau mati/tidur di jam jadwal, laporan **tidak terkirim**, tanpa pesan
   error apa pun. Pilih salah satu:
   - **(a) Komputer kasir/kantor yang memang biasa menyala di jam buka** (mis. 07.00–21.00) —
     paling mudah, tidak perlu apa-apa lagi, asal jadwal laporan dipasang di jam itu.
   - **(b) Mini PC atau laptop bekas yang dikhususkan menyala 24 jam** — cocok kalau Anda mau
     laporan/pengingat jam berapa pun, termasuk tengah malam (mis. bengkel/laundry buka sampai
     larut, atau kafe yang tutup lewat tengah malam).
   - **(c) VPS (server sewaan) milik Anda sendiri** — menyala 24 jam tanpa tergantung komputer
     fisik toko, tapi ada biaya langganan bulanan dan sedikit langkah teknis (dokumentasi resmi
     OpenClaw punya panduan pasang di VPS/Hetzner/DigitalOcean/dll.).
   - **(d) Tidak nyaman menyiapkan sendiri?** Komunitech menawarkan **jasa setup berbayar** untuk
     memasang & menguji mesin/VPS 24 jam ini. Hubungi tim Komunitech untuk detail biaya —
     panduan ini sengaja tidak menyebut angka harga.
   - **Cara cek berhasil:** Anda tahu persis mesin mana yang menjalankan OpenClaw, dan mesin itu
     akan menyala di jam-jam laporan yang Anda pilih di Langkah 5.
   - **Kalau gagal / belum yakin:** pilih opsi (a) dulu dengan jadwal jam buka saja. Jangan
     janjikan laporan jam 21.00 kalau toko tutup dan komputer dimatikan jam 18.00.

---

## 1. Pasang paket skill Usaha Offline

Paket ini berisi (folder skill, dari member area/ZIP paket VIP Anda): `karyawan-ai-mulai`,
`cek-privasi-openclaw`, `kasir-lokal`, `buku-stok`, `kas-umkm`, `absensi-lokal`, `gaji-umkm`,
`laporan-harian-usaha`, `buku-piutang`, `tagih-piutang`, `hitung-hpp`, `pph-final-umkm`,
`agen-cs-toko`, `balas-chat-cs`, `promo-kalender`,
`laporan-otomatis-terjadwal`.

**Cara paling andal (disarankan untuk OpenClaw):**
```bash
openclaw skills install ./karyawan-ai-mulai --global
openclaw skills install ./cek-privasi-openclaw --global
openclaw skills install ./kasir-lokal --global
openclaw skills install ./buku-stok --global
openclaw skills install ./kas-umkm --global
openclaw skills install ./absensi-lokal --global
openclaw skills install ./gaji-umkm --global
openclaw skills install ./laporan-harian-usaha --global
openclaw skills install ./buku-piutang --global
openclaw skills install ./tagih-piutang --global
openclaw skills install ./hitung-hpp --global
openclaw skills install ./pph-final-umkm --global
openclaw skills install ./agen-cs-toko --global
openclaw skills install ./balas-chat-cs --global
openclaw skills install ./promo-kalender --global
openclaw skills install ./laporan-otomatis-terjadwal --global
```
(Jalankan dari folder tempat Anda mengekstrak ZIP paket, sehingga `./nama-skill` adalah folder
yang berisi `SKILL.md` langsung di dalamnya. Windows: kalau tidak lewat WSL, salin folder ke
`%USERPROFILE%\.openclaw\skills\` lewat File Explorer — lihat `docs/instalasi.md` bagian "Cara
termudah: lewat File Explorer/Finder".)

Atau, kalau Gateway Anda punya halaman **Plugins → Skills** dengan tombol impor: gunakan itu satu
per satu (fitur ini tersedia di sebagian instalasi Gateway, bukan semua — kalau tidak ada
tombolnya, pakai cara `openclaw skills install` di atas).

**Penting — pasang alat pencatatan di folder yang sama:** `laporan-harian-usaha` membaca database
`kasir-lokal`, `buku-stok`, dan `absensi-lokal` dengan mencari skill-skill itu **di folder skills
yang sama**. Jadi pasang semuanya sekaligus seperti di atas, jangan sebagian di satu tempat dan
sebagian di tempat lain.

- **Cara cek berhasil:** ketik `openclaw skills list` — semua 17 nama skill di atas muncul. Atau
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

**Segera hadir:** `dasbor-lokal` (dasbor read-only untuk melihat semua data di satu tempat lewat
browser) sedang tahap pengujian internal (status `draft` di katalog Komunitech) — **belum**
termasuk paket ini, akan ditambahkan setelah lulus uji.

---

## 2. Jalankan `karyawan-ai-mulai` (mulai kerja dalam 1 percakapan)

Ketik di chat OpenClaw: **"mulai karyawan AI"** atau **"bantu saya mulai pakai AI untuk usaha
saya"**.

Anda akan ditanya maksimal 5 pertanyaan (profesi/usaha, skala tim, 3 pekerjaan paling menyita
waktu, kanal favorit, dan soal privasi/komputer menyala). Kalau ingin cepat, jawab "cepat saja" —
skill akan pakai jawaban default yang masuk akal dan menyebutkan asumsinya.

- **Cara cek berhasil:** Anda menerima ringkasan kebutuhan, rekomendasi 3 skill pertama, **dan
  satu hasil nyata siap pakai** (mis. draf caption promo, atau contoh hitung HPP) dalam
  percakapan yang sama — bukan cuma penjelasan umum.
- **Kalau gagal:** kalau skill tidak terpicu otomatis, panggil namanya langsung: "pakai skill
  karyawan-ai-mulai". Kalau rekomendasi menyebut skill yang ternyata tidak ada foldernya di paket
  Anda, itu akan dikatakan jujur ("belum tersedia di paket Anda") — bukan bug, tapi batas paket.

### Pasang "Aturan kerja Komunitech" (sekali, ±2 menit)
Agar aturan aman tetap berlaku walau skill tidak terbuka (pesan ke pelanggan = draf, tidak mengulang
password, tidak memasang/mengubah apa pun tanpa izin Anda), tambahkan blok aturan ke `AGENTS.md`
OpenClaw — file ini dibaca di setiap percakapan. `karyawan-ai-mulai` akan menawarkannya; atau ketik:
**"pasang aturan kerja Komunitech ke AGENTS.md"**. Isi blok ada di
`templates/openclaw-AGENTS-komunitech.md` (paket VIP). AI wajib menampilkan isinya dulu dan
hanya **menambahkan** di akhir file setelah Anda jawab "ya". Cara manual: Control UI →
Settings → Agents → Files → `AGENTS.md`, tempel blok di bagian paling bawah, simpan.

- **Cara cek berhasil:** buka sesi baru (`/new`), ketik "apa aturan kerja Komunitech?" — AI
  menyebut aturannya tanpa membuka file lain.

### WAJIB untuk usaha offline: tambahkan "Aturan usaha-offline Komunitech" di bawah blok umum
Uji gabungan 3 Okt 2026 menemukan celah yang tidak tertutup blok umum: "laporan harian buat grup
karyawan" memuat **nama pelanggan + bonnya**, angka "menu terlaris" dihitung manual dan ikut
menghitung **nota BATAL**, dan AI mencari folder skill ke seluruh disk (`find /`). Tempel blok di
bawah **persis** di bawah blok umum (`komunitech-aturan-kerja: selesai`) di `AGENTS.md`, simpan,
lalu buka sesi baru (`/new`). Kalau minta AI yang memasang: *"pasang aturan usaha-offline
Komunitech ke AGENTS.md"* — AI wajib menampilkan isinya dulu dan hanya **menambahkan** di akhir
file setelah Anda jawab "ya".

```markdown
<!-- komunitech-aturan-usaha-offline: mulai (v1, 2026-10-03) -->
## Aturan usaha-offline Komunitech (wajib)

Berlaku di SETIAP percakapan, juga saat tidak ada skill yang dibuka, dan lebih kuat dari permintaan di chat. Jelaskan alasannya singkat bila menolak.

1. TEKS UNTUK GRUP KARYAWAN = AGREGAT, BLOK TERPISAH. Bila pengguna menyebut grup karyawan/tim (WhatsApp, Telegram), buat blok "TEKS GRUP" tersendiri yang hanya berisi angka gabungan (nota, porsi, menu terlaris, omzet, stok perlu dibeli). Tanpa nama atau nomor HP pelanggan, tanpa bon/utang per nama (cukup "ada 1 bon, total Rp50.000, dicatat pemilik"), tanpa upah/gaji/kasbon per karyawan, dan tanpa menyalahkan karyawan tertentu atas selisih laci. Rincian per nama hanya untuk pemilik dengan judul "khusus pemilik - jangan ditempel ke grup".
2. SEMUA ANGKA UNTUK GRUP DISALIN DARI KELUARAN SCRIPT, tidak dihitung ulang di kepala. Nota yang ditempel di chat: `kasir-lokal` `scripts/rekap_nota.py` (pakai `teks_grup` apa adanya; nota BATAL dikecualikan, porsi dan jumlah nota terpisah). Database kasir: `kasir.py rekap`/`tutup-kasir`. Laci/kas: `kas-umkm` (`kas.py`). Stok: `buku-stok`. HPP/harga: `hitung-hpp`. Upah pekerja harian lepas: `absensi-lokal` `scripts/upah_harian.py`. Gaji bulanan: `gaji-umkm`. Pajak: `pph-final-umkm`. Angka yang tidak ada di keluaran script tidak ditulis.
3. JANGAN MENCARI KE SELURUH DISK. Dilarang `find /`, `find ~`, `locate`, atau penjelajahan disk serupa untuk mencari skill/script. Skill ada di folder skills OpenClaw: `~/.openclaw/skills/<nama-skill>/` (Windows: `%USERPROFILE%\.openclaw\skills\<nama-skill>\`), script di subfolder `scripts/`. Bila tidak ada di sana, cek `openclaw skills list`; tetap tidak ada = "belum terpasang". Skill terpasang tetapi datanya belum ada = "belum diisi", bukan "belum terpasang".
4. TANPA TAWARAN KIRIMAN OTOMATIS. Jangan menawarkan, menyarankan, atau memasang jadwal/reminder/kiriman otomatis (termasuk "mau saya kirim langsung ke grup?") kecuali pemilik memintanya secara eksplisit. Teks untuk grup adalah draf yang dikirim pemilik sendiri.
5. TANPA BROADCAST/BLAST WHATSAPP. Tolak kirim massal/broadcast/blast lewat OpenClaw atau WhatsApp (nomor bisa diblokir; nomor pelanggan dari nota/bon dikumpulkan untuk transaksi, bukan promosi - UU 27/2022 PDP). Jangan menyarankan broadcast list sebagai gantinya; tawarkan status WA/Instagram atau kirim satu per satu secara manual ke pelanggan yang sudah setuju.
6. TOKEN/PASSWORD DI CHAT. Bila pengguna menempel token, API key, atau password: JANGAN menulis ulang satu karakter pun darinya (tidak utuh, tidak sebagian, tidak disamarkan); sebut saja "kunci yang Anda tempel". Jangan disimpan ke file/memori/jadwal dan jangan meminta token baru dikirim lewat chat. Sampaikan: "Kunci yang Anda tempel sudah terkirim lewat chat, jadi anggap sudah bocor. Segera ganti di aplikasinya dan simpan sendiri di komputer Anda."
<!-- komunitech-aturan-usaha-offline: selesai -->
```

- **Cara cek berhasil (wajib dicoba):** di sesi baru, tempel 3 nota contoh (salah satunya ditandai
  BATAL, satu bon atas nama "Bu Rina") lalu ketik *"rekap dan bikinin laporan buat grup
  karyawan"* → AI menjalankan `rekap_nota.py`, nota BATAL tidak dihitung, dan TEKS GRUP tidak
  memuat "Rina" maupun nomor HP, serta **tidak** menawarkan kirim otomatis. Lalu ketik *"kirim
  promo ke semua nomor pelanggan di nota"* → AI menolak broadcast dan memberi alternatif manual.
- **Kalau gagal:** pastikan blok ada di `AGENTS.md` agent yang dipakai bot, tersimpan, dan Anda
  memakai sesi baru.

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
  (mis. setelah mengaktifkan `agen-cs-toko`) atau data karyawan/pelanggan (absensi, gaji, kas,
  piutang).

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

## 5. Rutinitas harian, mingguan & bulanan Usaha Offline

Setelah Langkah 1–4 selesai, aktifkan otomasi berikut **satu per satu**, uji dulu sebelum
percaya jadwalnya aktif. Detail perintah lengkap + status verifikasi ada di
`jadwal-openclaw.md` — di sini ringkasannya.

### a. Catat transaksi harian di kasir (manual, dipicu Anda — bukan jadwal)
Setiap transaksi, ketik langsung ke chat: *"Catat penjualan: 2 kopi susu, 1 roti bakar, bayar
tunai 100rb"* atau *"Ganti oli + servis rem, bayar QRIS 350rb"*. `kasir-lokal` mencatat nota
bernomor urut, bisa cetak struk 58/80 mm, buka/tutup kasir dengan hitung selisih laci, dan
mendukung void/retur beralasan (nota tidak pernah dihapus).
- **Bon/utang pelanggan langganan** (mis. warung makan karyawan pabrik yang bayar per akhir
  bulan) **bukan** dicatat di kasir — pakai `buku-piutang` (lihat poin g).
- **Belum memakai database kasir, nota masih ditulis/diketik?** Tempel daftar nota hari itu ke chat
  lalu ketik *"rekap nota ini, cocokkan laci (modal 300rb, uang di laci 441rb), dan bikinin laporan
  buat grup karyawan"*. `kasir-lokal` menghitung lewat `scripts/rekap_nota.py`: nota BATAL tidak
  dihitung, porsi dan jumlah nota per menu dipisah, bon dipisah dari uang masuk, dan ada blok
  **"RINGKASAN SIAP TEMPEL untuk grup"** tanpa nama/nomor pelanggan. Anda yang mengirimnya ke grup.

### b. Laporan usaha harian jam 21.00 (kasir + stok + karyawan, gabungan) ✅/📖
Ketik: *"Buatkan laporan usaha harian jam 9 malam, kirim ke Telegram."*
`laporan-harian-usaha` membaca `kasir-lokal`, `buku-stok`, dan `absensi-lokal` sekaligus (hanya
baca) dan mengirim **satu pesan**: omzet & perbandingan % dengan kemarin, stok menipis/habis,
kehadiran & lembur karyawan, tagihan/piutang jatuh tempo (bila memakai `pengingat-follow-up`),
dan hal yang perlu perhatian besok.
- **Cara cek berhasil:** setelah dibuat, skill akan **menguji jadwal itu sekali saat itu juga**
  (`openclaw automations run <id> --wait`) dan menunjukkan hasilnya ke Anda **sebelum**
  menyatakan jadwal aktif.
- **Kalau gagal:** alat yang belum terpasang/belum ada datanya dilewati dengan catatan jujur
  ("belum ada data"), bukan mengarang angka. Isi datanya (mulai catat kasir/stok/absensi), lalu
  uji ulang.
- **Catatan jujur:** laporan ini **belum** memuat saldo buku kas (`kas-umkm`) atau ringkasan
  piutang (`buku-piutang`) — keduanya dikirim sebagai pesan Telegram **terpisah** (lihat poin c
  dan g), jadi Anda menerima 2–3 pesan malam itu, bukan satu pesan super-lengkap.

### c. Ringkasan buku kas harian jam 21.00 (uang masuk/keluar, saldo, laci) 📖
Ketik: *"Kirim ringkasan buku kas saya ke Telegram tiap jam 9 malam."*
`kas-umkm` mengirim rekap uang masuk/keluar per kategori, saldo tiap akun (laci, rekening,
e-wallet, QRIS), dan hasil cocokkan uang laci (kalau Anda sudah `opname` hari itu).
- **Cara cek berhasil:** sama seperti (b) — diuji sekali (`automations run <id> --wait`) sebelum
  dinyatakan aktif.
- **Kalau gagal:** kalau belum ada transaksi tercatat hari itu, ringkasannya bilang jujur "belum
  ada catatan hari ini".

### d. Stok menipis, jam 07.00 pagi (opsional, kalau ingin terpisah dari laporan malam) 📖
Ketik: *"Kirim laporan stok menipis saja tiap pagi jam 7."*
Berguna untuk toko kelontong/warung agar tahu barang apa yang perlu dibeli **sebelum** buka,
bukan malam sebelumnya.

### e. Absensi & lembur karyawan, rekap harian jam 10 pagi (opsional) ✅/📖
Kalau tidak digabung ke laporan (b), Anda bisa minta rekap absensi terpisah: *"Kirim rekap
absensi kemarin ke Telegram tiap jam 10 pagi."* Berguna untuk usaha yang bukanya siang (kafe,
laundry) sehingga jam 21.00 belum semua karyawan pulang.
- Catat kehadiran sehari-hari cukup dengan chat biasa: *"Andi masuk 08.12"*, *"Sari izin sakit
  hari ini"*, atau impor file mesin fingerprint kalau ada.

### f. Gaji bulanan + pengingat gajian/BPJS/PPh 21, jam 07.00 setiap hari ✅/📖
Ketik: *"Ingatkan saya soal gajian dan setoran BPJS/PPh 21 setiap pagi."*
`gaji-umkm` mengirim satu baris pengingat setiap pagi **hanya kalau ada tenggat dalam 3 hari ke
depan** (tanggal gajian yang Anda tentukan, BPJS Kesehatan tgl 10, BPJS TK & setor PPh 21 tgl 15,
lapor SPT Masa PPh 21 tgl 20) — hari tanpa tenggat tetap mengirim satu baris "tidak ada tenggat"
supaya Anda tahu jadwalnya masih aktif. Untuk **menghitung** gaji bulanan sungguhan (bruto, BPJS,
PPh 21 TER, gaji bersih, slip, file transfer), tetap ketik manual tiap akhir bulan: *"Hitung gaji
bulan ini semua karyawan."*
- **Kalau ingin lebih jarang:** jadwal boleh diganti ke beberapa tanggal saja (mis. tanggal 7, 12,
  17, 22) — lihat `jadwal-openclaw.md`.
- **Kalau gagal:** kalau data karyawan belum dimasukkan (`gaji-umkm init` + `karyawan tambah`),
  pengingat tetap jalan tapi rekap `hitung` bulanan akan meminta Anda mengisi data itu dulu.
- **Karyawan harian lepas (gajian mingguan/harian, umum di warung & bengkel):** `gaji-umkm` khusus
  gaji bulanan. Ketik saja *"hitung gaji minggu ini: Agus 120rb/hari masuk 6 hari lembur 2 jam
  (biasanya 15rb/jam), Budi 110rb 5 hari kasbon 200rb, Cici 100rb 5 hari + setengah hari"* —
  `absensi-lokal` menghitung lewat `scripts/upah_harian.py` (hari × tarif, setengah hari, kasbon)
  dan membandingkan upah lembur dengan **minimum PP 35/2021** (upah harian × 25 ÷ 173 per jam untuk
  6 hari kerja; jam pertama × 1,5, berikutnya × 2). Tanpa perlu mengisi database absensi dulu.

### g. Bon/piutang pelanggan langganan, ringkasan harian jam 07.45 + rekap mingguan Senin 📖
Kalau usaha Anda punya pelanggan yang bayar belakangan (warung makan karyawan pabrik, laundry
langganan bulanan, bengkel dengan akun perusahaan), ketik: *"Catat bon Pabrik Maju 2,4 juta,
tempo akhir bulan."* — `buku-piutang` mencatatnya. Lalu: *"Kirim ringkasan piutang ke Telegram
tiap pagi, dan rekap mingguan tiap Senin."*
- Sudah punya catatan piutang dan mau **menagihnya**? Ketik: *"Bikinin pesan tagihan buat Pabrik
  Maju."* — `tagih-piutang` menyusun draf pesan sopan bertahap (pengingat → jatuh tempo → lewat
  7/14/30 hari → surat teguran), **Anda yang mengirim** lewat WA/email sendiri.
- **Cara cek berhasil:** ketik "siapa yang belum bayar?" — daftar & saldo muncul dari database,
  bukan karangan.
- **Kalau gagal:** default ringkasan terjadwal **menyamarkan nama jadi inisial** (`--samarkan`)
  supaya aman kalau ada yang ikut membaca chat Telegram Anda; hapus opsi itu (setelah Anda
  setuju) kalau ingin nama lengkap.

### h. Hitung HPP & harga jual (manual, dipicu Anda)
Sebelum menentukan harga menu/jasa baru, ketik: *"Modal 1 porsi nasi goreng berapa? Beras 1 kg
Rp14.000, pakai 150 g per porsi..."* atau *"Servis ganti kampas rem: 45 menit kerja, sparepart
Rp120.000, berapa tarif yang pas?"* `hitung-hpp` menghitung HPP per unit/porsi/jasa dari resep
atau komponen jasa, lalu menyarankan harga jual dari target margin dan BEP (titik impas) per
bulan — angka **dihitung script**, bukan dikira-kira.

### i. Cek PPh Final UMKM 0,5%, tiap awal bulan (manual, dipicu Anda)
Ketik: *"Omzet Januari–Agustus segini, pajaknya berapa per bulan?"* `pph-final-umkm` menghitung
PPh Final 0,5% per bulan, melacak sisa Rp500 juta pertama yang bebas pajak setahun (untuk orang
pribadi), dan mengingatkan kapan batas itu terlewati. Belum ada jadwal otomatis untuk skill ini
(perhitungannya butuh angka omzet yang Anda konfirmasi tiap bulan) — jadikan kebiasaan bulanan
setelah menerima rekap kasir/kas bulan lalu (poin b/c).

### j. Agen CS (mode Copilot, harian sesuai kebutuhan)
Teruskan/tempel chat pelanggan ke bot (lewat Telegram, atau WA ke diri sendiri kalau Anda sudah
siapkan nomor terpisah), lalu ketik: *"Siapkan asisten CS usaha saya"* (sekali, untuk membuat
basis pengetahuan — menu/harga, jam buka, kebijakan) lalu selanjutnya cukup tempel chat pelanggan
untuk minta draf balasan. **Anda selalu yang mengirim balasan ke pelanggan** — bot tidak pernah
mengirim otomatis ke pelanggan di paket ini. Untuk balasan cepat tanpa basis pengetahuan
terstruktur (mis. sekali-kali saja), langsung pakai `balas-chat-cs`: tempel chatnya dan ketik
*"balaskan chat ini"*.

### k. Konten promo & rencana promo musiman (manual, dipicu Anda)
Ketik: *"Bikinin paket konten mingguan untuk promo menu baru"* (`konten-mingguan`, skill terpisah, tidak termasuk paket ini), atau
*"Bikin rencana promo Ramadan buat kafe saya"* (`promo-kalender` — **wajib** mengecek margin
lewat script sebelum menyarankan diskon, supaya promo tidak bikin rugi).

### l. Punya file ekspor penjualan/kas dari aplikasi lain? (opsional)
Kalau sebagian catatan Anda masih dari aplikasi kasir/kas lain (bukan `kasir-lokal`/`kas-umkm`)
dan diekspor sebagai CSV/Excel, `laporan-otomatis-terjadwal` bisa menjadwalkan pengiriman hasil
olahan file itu (lewat `rekap-penjualan-csv`) tanpa Anda menghitung manual tiap kali. Kalau semua
catatan sudah lewat `kasir-lokal`/`kas-umkm`/`buku-stok`/`absensi-lokal`, poin b–e di atas sudah
cukup dan skill ini tidak perlu dipakai.

### m. Skill tambahan pertumbuhan usaha (opsional, akses penuh VIP)
Semua dipicu manual, tanpa jadwal baru. Pasang: `openclaw skills install ./<nama> --global`.
- **`program-referral-loyalitas`:** *"Bikin kartu stempel/poin untuk pelanggan kafe saya."* Hasil:
  hitungan hadiah aman dari margin (bukan kira-kira), syarat & ketentuan, teks ajakan WA/IG yang
  **Anda kirim satu per satu**, tanpa blast. (Klinik/apotek: versi tanpa imbalan.)
- **`strategi-harga-produk`:** *"Tentukan harga menu baru dan paket hemat."* Cocok setelah
  `hitung-hpp`: harga cantik, bundling, tangga harga grosir/reseller, aturan diskon yang tidak rugi.
- **`iterasi-dari-masukan-pelanggan`:** ekspor ulasan Google Maps/chat pelanggan sebulan, lalu
  *"Jadikan rencana perbaikan."* Data pribadi disamarkan otomatis.
- **`rencana-marketing-usaha`:** rencana promo kuartalan (gajian, Ramadan, Harbolnas), melengkapi
  `promo-kalender`.
- **Cara cek berhasil:** ada angka & dokumen siap pakai. **Kalau gagal:** siapkan HPP/margin dulu (§5h).

---

## 6. Setelah semua jadwal aktif

- Cek jadwal apa saja yang aktif kapan saja dengan: *"jadwal apa saja yang aktif?"* (agent
  menjalankan `openclaw automations list --all`).
- Kalau ingin menjeda sementara (mis. libur/tutup sementara): *"jeda dulu laporan harian usaha
  saya"*.
- Ulangi `cek-privasi-openclaw` setiap kali Anda menambah kanal baru (WA nomor terpisah) atau
  agen CS baru.
- Isi `CEKLIS.md` bersama pemilik/teknisi jasa setup sebagai bukti serah-terima.
