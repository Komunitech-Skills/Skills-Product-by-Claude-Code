# Panduan Solusi VIP — Klinik & Praktik Mandiri

Untuk klinik pratama/gigi/kecantikan/fisioterapi, praktik dokter/bidan mandiri yang sudah jadi
member VIP komunitech.com. Bahasa sehari-hari, langkah demi langkah.

**Batasan penting yang berlaku di SELURUH panduan ini:** paket ini **hanya** untuk edukasi
pasien, balasan chat umum non-diagnosis, dan laporan operasional agregat (jumlah kunjungan,
pendapatan, jam ramai) **tanpa nama/diagnosis pasien**. Paket ini **tidak** melakukan
skrining, diagnosis, kalkulator medis (dosis/BMI klinis), interpretasi hasil lab, atau triase
kegawatdaruratan. Semua instruksi medis (obat, pantangan, tanda bahaya) harus berasal persis
dari dokter/tenaga kesehatan — tidak pernah ditebak AI.

---

## 0. Prasyarat

1. **OpenClaw sudah terpasang dan bisa diajak chat.** Ketik "halo" untuk memastikan.
2. **Mesin yang menjalankan OpenClaw perlu menyala di jam laporan/edukasi terjadwal.** Pilih:
   - **(a)** Komputer resepsionis/admin yang memang menyala di jam praktik.
   - **(b)** Mini PC/laptop khusus menyala 24 jam.
   - **(c)** VPS milik klinik sendiri.
   - **(d)** **Jasa setup berbayar Komunitech** — hubungi tim Komunitech untuk detail biaya
     (tidak dicantumkan di sini).
   - **Cara cek berhasil:** Anda tahu mesin mana yang menjalankan Gateway OpenClaw, dan mesin itu
     akan menyala di jam yang dipilih di Langkah 5.
   - **Kalau gagal/belum yakin:** pilih jadwal di jam praktik saja dulu (mis. laporan sore
     sebelum tutup), bukan tengah malam.

3. **Siapa yang meninjau materi medis?** Semua leaflet/pengingat/FAQ berisi instruksi medis
   **wajib ditinjau dokter/tenaga kesehatan klinik** sebelum dikirim ke pasien — skill ini
   merapikan bahasa, bukan menggantikan tinjauan profesional.

---

## 1. Pasang paket skill Klinik

Skill: `karyawan-ai-mulai`, `cek-privasi-openclaw`, `edukasi-pasien-klinik`, `agen-cs-toko`,
`balas-ulasan-pelanggan`, `konten-mingguan`, `laporan-status-kantor`, `kebijakan-privasi-pdp`,
`sop-onboarding`, `kontrak-kerja-pkwt`, `pengingat-pasien-klinik`.

```bash
openclaw skills install ./karyawan-ai-mulai --global
openclaw skills install ./cek-privasi-openclaw --global
openclaw skills install ./edukasi-pasien-klinik --global
openclaw skills install ./agen-cs-toko --global
openclaw skills install ./balas-ulasan-pelanggan --global
openclaw skills install ./konten-mingguan --global
openclaw skills install ./laporan-status-kantor --global
openclaw skills install ./kebijakan-privasi-pdp --global
openclaw skills install ./sop-onboarding --global
openclaw skills install ./kontrak-kerja-pkwt --global
openclaw skills install ./pengingat-pasien-klinik --global
```
(Jalankan dari folder hasil ekstrak ZIP paket. Windows tanpa WSL: salin folder skill lewat File
Explorer ke `%USERPROFILE%\.openclaw\skills\` — lihat `docs/instalasi.md`.)

- **Cara cek berhasil:** `openclaw skills list` menampilkan ke-11 nama skill di atas.
- **Kalau gagal:** lihat bagian "Kalau gagal" yang sama di panduan toko-online (pesan "already
  exists" = aman; skill tidak terbaca = buka sesi baru; `exec` ditolak = salin manual).

---

## 2. Jalankan `karyawan-ai-mulai`

Ketik: **"mulai karyawan AI untuk klinik saya"**. Jawab pertanyaan singkat (jenis
praktik/klinik, skala tim, 3 pekerjaan paling menyita waktu, kanal favorit, privasi/komputer
menyala). Anda akan menerima rekomendasi 3 skill pertama + 1 hasil nyata (mis. draf leaflet dari
poin yang Anda berikan) di percakapan yang sama.

- **Cara cek berhasil:** ada hasil nyata siap pakai, bukan cuma penjelasan.
- **Kalau gagal:** panggil langsung "pakai skill karyawan-ai-mulai".

---

## 3. Jalankan `cek-privasi-openclaw`

**Wajib** dijalankan sebelum `agen-cs-toko` dipakai untuk membalas chat pasien sungguhan, karena
data kesehatan adalah data pribadi spesifik menurut UU PDP. Ketik: **"cek privasi saya, saya
pakai OpenClaw untuk klinik"**.

- **Cara cek berhasil:** laporan lampu lalu lintas + ringkasan singkat UU PDP untuk data
  pelanggan/pasien, dengan disclaimer "bukan nasihat hukum".
- **Kalau gagal:** ikuti fallback salin-tempel bila `exec` tidak diizinkan.
- Ulangi setiap kali menambah kanal WA nomor terpisah atau agen CS baru.

---

## 4. Hubungkan bot Telegram

Sama seperti paket toko-online: buat bot via @BotFather → `openclaw channels add --channel
telegram --token <token>` → kirim "halo" ke bot → setujui pairing → catat ID chat lewat
@userinfobot.

- **Cara cek berhasil:** bot membalas pesan tes, ID chat sudah dicatat (**bukan** di dokumen
  yang dibagikan ke pihak lain).
- **Kalau gagal:** lihat langkah setara di `toko-online/PANDUAN.md` §4.

WhatsApp untuk klinik **hanya** untuk notifikasi ke pemilik/PIC sendiri, nomor terpisah dari
nomor yang dipakai pasien untuk daftar, dengan persetujuan risiko tertulis — lihat kotak
peringatan di `jadwal-openclaw.md`.

---

## 5. Rutinitas Klinik

### a. Balasan chat umum non-diagnosis (mode Copilot, harian — bukan jadwal)
Admin meneruskan/menempel pertanyaan pasien (jadwal, biaya, BPJS, cara daftar, atau keluhan
gejala yang **tidak dijawab**, hanya diarahkan) ke bot, lalu ketik: *"Siapkan balasan untuk
pasien ini."* Basis pengetahuan klinik disiapkan sekali lewat `agen-cs-toko` (jam buka, biaya,
BPJS, kebijakan). **Admin yang mengirim balasan ke pasien** — bot tidak pernah kirim otomatis.
- Pertanyaan gejala/medis selalu dijawab dengan kalimat baku "sebaiknya dikonsultasikan langsung
  ke dokter" + tawaran jadwal konsultasi, **tidak pernah** dijawab isi medisnya.

### b. Edukasi pasien (leaflet, pengingat, FAQ, konten medsos) — dipicu per kasus
Setelah tindakan/kunjungan, dokter memberi poin instruksi (obat, pantangan, tanda bahaya) ke
admin, lalu ketik ke bot: *"Buatkan leaflet WA perawatan setelah [tindakan], poinnya: ..."*.
Skill **tidak menambah/menebak** instruksi medis apa pun.
- **Cara cek berhasil:** leaflet/pesan hanya berisi poin yang benar-benar Anda berikan, ditandai
  `[isi ...]` untuk bagian yang belum lengkap (mis. nomor kontak klinik).
- **Kalau gagal (dokter belum sempat memberi poin):** skill akan meminta poinnya dulu, tidak
  mengarang instruksi medis.
- **Pengingat kontrol/vaksin per pasien** (tanggal kontrol berikutnya, bukan instruksi medis)
  memakai skill terpisah `pengingat-pasien-klinik` — lihat §5i.

### c. Konten edukasi kesehatan mingguan (Jumat sore, terjadwal)
Ketik: *"Tiap Jumat sore kirimi saya ide konten edukasi kesehatan untuk klinik, dengan sumber
resmi."* Isinya topik + draf konten bersumber Kemenkes/WHO/organisasi profesi resmi (dengan
tautan & tanggal), **bukan** klaim menyembuhkan/testimoni/before-after (dilarang Permenkes
1787/2010). Draf tetap **wajib ditinjau dokter** sebelum diposting.
- **Cara cek berhasil:** setiap draf mencantumkan baris "Sumber: ..." dan nama+alamat klinik+
  tanggal publikasi.
- **Kalau gagal:** kalau sumber resmi untuk topik itu tidak ditemukan, skill akan bilang jujur,
  bukan mengarang rujukan.

### d. Laporan operasional klinik (agregat, tanpa identitas pasien)
Ketik: *"Kirimi saya laporan operasional klinik tiap [harian/mingguan] jam [...] — jumlah
kunjungan, jam ramai, pendapatan, tanpa nama pasien."* Sumber data: file CSV kunjungan dari
sistem pendaftaran/kasir klinik, ditaruh di folder yang ditunjuk. Format laporan format 3P
(Progres-Rencana-Kendala) dari `laporan-status-kantor`, atau ringkasan angka murni dari
`edukasi-pasien-klinik` (jumlah kunjungan per hari/poli/penjamin, tidak datang, jam ramai).
- **Cara cek berhasil:** laporan hanya berisi angka agregat — **tidak ada** satu pun nama/NIK/
  diagnosis pasien. Uji sekali (`automations run <id> --wait`) sebelum jadwal aktif.
- **Kalau gagal:** kalau CSV berisi kolom yang mencurigakan (mis. nama pasien tertulis di kolom
  status), skill akan menyembunyikannya otomatis dan memberi tahu — **jangan** minta skill
  membuka file asli untuk "melengkapi" nilai yang disembunyikan itu.

### e. Balasan ulasan klinik (manual, dipicu Anda)
Untuk ulasan Google Maps/media sosial klinik: tempel isi ulasan, ketik *"Balaskan ulasan ini."*
`balas-ulasan-pelanggan` menyiapkan draf, Anda yang memposting.

### f. Kebijakan privasi klinik & persetujuan data pasien (manual, dipicu Anda)
Data pasien (termasuk keluhan/riwayat kesehatan) adalah **data pribadi spesifik** menurut UU PDP,
jadi butuh perhatian ekstra. Ketik: *"Buatkan kebijakan privasi untuk klinik saya"* atau
*"Buatkan kalimat persetujuan data untuk formulir pendaftaran pasien."* `kebijakan-privasi-pdp`
juga bisa **mengecek** kebijakan yang sudah ada, dan menyiapkan **tanggapan** kalau ada pasien
minta datanya dihapus atau (amit-amit) terjadi kebocoran data.
- **Cara cek berhasil:** draf mencantumkan bagian data kesehatan/pasien secara khusus, dan bagian
  yang belum Anda isi ditandai `[isi: ...]`, bukan dikarang.
- **Ingat:** ini draf, **bukan nasihat hukum** — untuk klinik dengan banyak pasien, tetap minta
  ditinjau konsultan hukum sebelum dipakai resmi.

### g. Onboarding staf/admin baru (manual, dipicu Anda)
Ada admin, kasir, atau asisten baru mulai kerja? Ketik: *"Buatkan paket onboarding untuk admin
baru di klinik saya, mulai Senin depan."* `sop-onboarding` menyiapkan checklist dokumen, jadwal
hari pertama–90 hari (dihitung, bukan dikira), pesan sambutan, buku saku, dan formulir evaluasi —
ada varian khusus klinik. **Bukan untuk kompetensi/sertifikasi tenaga medis (STR/SIP)** — itu di
luar cakupan, arahkan ke Dinkes/lembaga sertifikasi.

### h. Kontrak kerja staf kontrak (manual, dipicu Anda)
Untuk staf **non-medis** yang dikontrak (admin, kasir, office boy, dll.), ketik: *"Buatkan
kontrak kerja 1 tahun untuk admin baru klinik saya."* `kontrak-kerja-pkwt` menyusun draf PKWT
sesuai aturan, menghitung uang kompensasi akhir kontrak, dan bisa **memeriksa** draf kontrak yang
sudah ada untuk klausul berbahaya (mis. tanpa BPJS, masa percobaan yang dilarang di PKWT).
- **Batasan:** bukan untuk status kepegawaian tenaga medis (dokter/perawat dengan STR/SIP) yang
  biasanya punya aturan tersendiri — untuk itu konsultasikan ke konsultan hukum ketenagakerjaan.

### i. Pengingat kontrol/vaksin pasien (buku jadwal harian, terjadwal ke Telegram pemilik/PIC)
`pengingat-pasien-klinik` adalah **buku jadwal lokal minimal** — hanya nama panggilan, nomor WA,
jenis kunjungan umum (kontrol, vaksin, cabut jahitan, dll.), dan tanggal. **Tidak ada
diagnosis/rekam medis** yang disimpan.

1. **Catat pasien** saat pasien dijadwalkan kontrol/vaksin berikutnya. Ketik ke agent, mis.:
   *"Catat Bu Sari, kontrol gigi 10 hari lagi, WA 0812-0000-1111, dia setuju diingatkan lewat WA."*
   - **Tanyakan persetujuan pasien secara eksplisit** sebelum mencatat — jangan pernah diasumsikan
     "ya". Pasien yang menolak tetap tercatat (agar staf tidak bertanya ulang) tapi **tidak pernah
     muncul** di daftar harian maupun draf pesan.
   - **Cara cek berhasil:** agent membalas satu baris konfirmasi berisi nama, jenis kunjungan,
     tanggal, dan status persetujuan.
   - **Kalau gagal:** field wajib kurang (nama/WA/jenis/tanggal/persetujuan) — agent akan
     menanyakan sekali dalam satu pesan, isi saja jawabannya.
2. **Daftar harian & draf pesan (dipakai staf tiap pagi, bukan otomatis):** ketik *"siapa yang
   harus diingatkan hari ini?"* — muncul daftar TERLAMBAT/HARI INI/BESOK/H-3 plus **draf pesan WA
   sopan siap disalin**. **Staf sendiri yang menyalin dan mengirim** dari WA klinik — tidak ada
   pengiriman otomatis maupun broadcast.
   - **Cara cek berhasil:** setiap draf ditandai "salin & kirim sendiri, JANGAN dikirim otomatis"
     dan hanya berisi nama, jenis kunjungan umum, dan tanggal — tidak ada saran medis.
3. **Setelah pasien datang/batal:** ketik *"Bu Sari sudah datang, jadwalkan lagi 3 bulan lagi"*
   atau *"Pak Budi batal, pindah kota"* — jadwal berikutnya (atau penghentian) tercatat otomatis.
4. **Ringkasan harian ke Telegram pemilik/PIC (terjadwal, jam 07.30 WIB — opsional):** ketik
   *"kirim ringkasan pengingat pasien tiap pagi jam 7.30 ke Telegram saya"*. Ringkasan berisi
   **jumlah** TERLAMBAT/HARI INI/BESOK/H-3 (nama boleh disamarkan jadi inisial) — **tidak pernah**
   memuat nomor WA. Lihat perintah persis di `jadwal-openclaw.md` §5.
   - **Cara cek berhasil:** uji sekali (`automations run <id> --wait`), pastikan hasilnya tidak
     memuat nomor WA sebelum jadwal dianggap aktif.
5. **Hapus data atas permintaan pasien:** begitu pasien minta datanya dihapus, langsung ketik
   *"Bu Sari minta datanya dihapus"* — agent menampilkan pratinjau lalu meminta konfirmasi sebelum
   menghapus permanen (UU PDP 27/2022). **Jangan ditunda.**
- **Batasan:** hanya jenis kunjungan umum (kontrol, vaksin, cek gigi, dll.) yang boleh dicatat —
  **bukan** nama penyakit/diagnosis/hasil pemeriksaan; skill menolak sendiri isian yang
  menyerupai itu. Bukan pengganti sistem antrean/rekam medis elektronik klinik.

### j. Skill tambahan klinik (opsional, akses penuh VIP)
- **`program-referral-loyalitas` (manual) - versi TANPA imbalan:** untuk fasilitas kesehatan skill
  hanya merancang edukasi, pengingat kontrol (kirim staf via §5i), dan kartu info klinik.
  **Tanpa diskon/poin/hadiah/komisi untuk merujuk pasien** (Permenkes 1787/2010 dan kode etik
  profesi). Ditandai PERLU REVIEW tenaga medis/hukum. *"Bikin program edukasi & kartu info klinik
  tanpa hadiah."*
- **`iterasi-dari-masukan-pelanggan` (manual, bulanan):** ekspor ulasan Google Maps/survei
  kepuasan, lalu *"Jadikan masukan pasien bulan ini rencana perbaikan layanan."* Fokus antrean,
  keramahan, kebersihan, jam layanan. Data disamarkan; **jangan menempel isi keluhan medis/diagnosis**.
  Balasan ke ulasan tetap lewat `balas-ulasan-pelanggan` (staf yang mengirim).
- **Cara cek berhasil:** hasilnya tidak memuat imbalan rujukan maupun nama/nomor pasien.

---

## 6. Setelah semua jadwal aktif

- Cek jadwal aktif: *"jadwal apa saja yang aktif?"*
- Jeda sementara (mis. klinik tutup/renovasi): *"jeda dulu semua laporan klinik."*
- Jalankan ulang `cek-privasi-openclaw` setiap ada perubahan kanal/agen.
- Isi `CEKLIS.md` untuk serah-terima, termasuk siapa dokter/tenaga kesehatan yang meninjau
  materi edukasi.
