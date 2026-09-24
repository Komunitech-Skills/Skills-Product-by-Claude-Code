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
`balas-ulasan-pelanggan`, `konten-mingguan`, `laporan-status-kantor`.

```bash
openclaw skills install ./karyawan-ai-mulai --global
openclaw skills install ./cek-privasi-openclaw --global
openclaw skills install ./edukasi-pasien-klinik --global
openclaw skills install ./agen-cs-toko --global
openclaw skills install ./balas-ulasan-pelanggan --global
openclaw skills install ./konten-mingguan --global
openclaw skills install ./laporan-status-kantor --global
```
(Jalankan dari folder hasil ekstrak ZIP paket. Windows tanpa WSL: salin folder skill lewat File
Explorer ke `%USERPROFILE%\.openclaw\skills\` — lihat `docs/instalasi.md`.)

- **Cara cek berhasil:** `openclaw skills list` menampilkan ke-7 nama skill di atas.
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
- **Pengingat kontrol/vaksin per pasien** saat ini **belum** bisa dijadwalkan otomatis
  (menyimpan tanggal per pasien butuh data pribadi kesehatan — lihat "Celah" di
  `solusi-vip/README.md`). Untuk sekarang, buat pengingatnya per kasus saat pasien kontrol,
  dikirim manual oleh admin.

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

---

## 6. Setelah semua jadwal aktif

- Cek jadwal aktif: *"jadwal apa saja yang aktif?"*
- Jeda sementara (mis. klinik tutup/renovasi): *"jeda dulu semua laporan klinik."*
- Jalankan ulang `cek-privasi-openclaw` setiap ada perubahan kanal/agen.
- Isi `CEKLIS.md` untuk serah-terima, termasuk siapa dokter/tenaga kesehatan yang meninjau
  materi edukasi.
