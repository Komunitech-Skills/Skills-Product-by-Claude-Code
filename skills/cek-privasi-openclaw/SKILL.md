---
name: cek-privasi-openclaw
description: Memeriksa pengaturan keamanan & privasi OpenClaw milik pengguna dalam bahasa awam — tool aktif, exec/perintah komputer tanpa persetujuan, sandbox, kanal terhubung & siapa yang boleh mengirim perintah, grup, penyimpanan memori/log, model AI yang menerima isi pesan — lalu beri laporan lampu lalu lintas (hijau/kuning/merah) dan perbaikan satu per satu DENGAN persetujuan pengguna, plus panduan UU PDP singkat bila memproses data pelanggan. Gunakan saat pengguna tanya "amankah OpenClaw saya", "cek privasi", "khawatir data bocor", "audit keamanan", atau security check, privacy audit, data safety. Bukan untuk memasang/merekomendasikan skill (pakai karyawan-ai-mulai) atau menjalankan perbaikan tanpa izin.
---

# Cek & Perbaiki Privasi OpenClaw

> **Aturan kerja:** Jangan menginstal paket/aplikasi (mis. `pip install`) — bila perlu, tunjukkan caranya dan biarkan pengguna yang memasang; jangan membuka atau mencari file selain yang diberikan pengguna, isi folder skill ini, dan file yang disebut di langkah kerja; jangan menulis file baru tanpa menyebut lokasinya, dan simpan hasil di folder kerja yang disepakati (bukan /tmp).

## Tujuan
Membantu pengguna awam memahami **seberapa aman** pengaturan OpenClaw mereka saat ini, dengan
bahasa sederhana, lalu memperbaikinya **satu per satu dengan persetujuan** — bukan mengubah
sistem diam-diam.

## Kapan digunakan
- Pengguna khawatir soal privasi/keamanan data (kendala paling umum kedua setelah "tidak tahu
  mulai" di kalangan member).
- Setelah memasang skill baru yang membaca pesan orang lain (agen CS, bot grup).
- Diminta eksplisit: "cek privasi", "audit keamanan", "amankan OpenClaw saya".

## Kapan TIDAK digunakan
- Onboarding awal/rekomendasi paket skill → pakai `karyawan-ai-mulai`.
- Meminta bantuan hukum PDP mendalam (kebocoran data besar, sengketa) → beri ringkasan di
  `references/uu-pdp.md`, lalu arahkan ke konsultan hukum/DPO. Skill ini bukan nasihat hukum.
- Mengubah pengaturan tanpa diminta atau tanpa persetujuan eksplisit tiap butir.
- **Permintaan memantau/menyadap perangkat atau chat orang lain** (pasangan, karyawan, anak
  tanpa dasar hukum yang jelas, dsb.) — **tolak**. Skill ini untuk mengamankan OpenClaw milik
  pengguna sendiri, bukan untuk mengintai orang lain. **Penolakan wajib ditulis lengkap di
  balasan itu sendiri** (jangan hanya "tetap saya tolak seperti sebelumnya"), di awal balasan,
  2–3 kalimat sopan: (1) maaf, bagian ini tidak bisa dibantu; (2) alasannya — membaca/menyadap
  chat orang lain tanpa izin dapat melanggar UU ITE (UU 11/2008 jo. UU 1/2024, Pasal 31 tentang
  intersepsi/penyadapan) dan UU PDP (UU 27/2022);
  (3) alternatif sah — kebijakan tertulis pemakaian perangkat/akun kerja yang disetujui
  karyawan, memakai akun WA Business kantor, atau konsultasi ke HR/konsultan hukum. Bagian lain
  permintaan (cek privasi) tetap dikerjakan.

## Input

| Info | Wajib? | Default jika tidak diberikan |
|---|---|---|
| OpenClaw ini dipakai untuk apa? — **4 opsi baku** (tulis bernomor 1) 2) 3) 4), tanpa emoji): 1) pribadi saja, 2) juga dipakai pelanggan/pasien (CS), 3) juga ikut di grup, 4) juga punya laporan/automation terjadwal | Tidak, tapi tanyakan di awal | Anggap "mungkin semua" (pribadi + pelanggan + grup + automation) — audit jadi lebih lengkap, dan tawaran perbaikan lebih hati-hati |
| Izin menjalankan `openclaw security audit` (dan perintah baca lain) | Ya (tanya sekali di awal) | Kalau `exec` tidak diizinkan, tawarkan versi salin-tempel (lihat Langkah 1; di kanal chat hanya bila diminta) |
| Apakah OpenClaw memproses data pelanggan/pihak ketiga (agen CS, bot grup, daftar piutang, dll.) | Tidak, tapi tanyakan | Anggap "mungkin ya" → tetap sertakan ringkasan UU PDP singkat |
| Kanal yang dipakai (WhatsApp/Telegram/dll.) | Tidak | Cek semua kanal yang terlihat di config |

Kalau pengguna hanya bilang "cek privasi saya", langsung mulai Langkah 1 tanpa menahan dengan
banyak pertanyaan — ini pemeriksaan **baca saja**, risikonya rendah. Pertanyaan "dipakai untuk
apa" tetap penting karena menentukan aman-tidaknya perbaikan yang nanti ditawarkan (lihat
`references/dampak-perubahan.md`) — boleh ditanyakan singkat di awal, atau disimpulkan dari
konteks percakapan kalau sudah jelas.

## Langkah kerja

### 1. Audit dasar (HANYA BACA — tidak mengubah apa pun)
Jalankan (lihat `references/openclaw.md` §1 untuk detail & fallback tanpa `exec`):
```bash
openclaw security audit --json
```
Kalau `exec` tidak diizinkan atau gagal, beri perintah ini untuk disalin-tempel pengguna sendiri
di terminal, lalu minta hasilnya ditempel kembali ke chat untuk dibaca bersama. (Di kanal chat:
katakan dengan bahasa awam bahwa pemeriksaan belum diizinkan dan tawarkan "balas 'tampilkan
perintahnya'"; perintah baru ditulis bila pengguna meminta.)

### 2. Baca konfigurasi relevan (HANYA BACA)
Untuk tiap kanal yang terpasang, dan untuk pengaturan tool/sandbox, jalankan `openclaw config get
<path> --json` sesuai daftar path di `references/openclaw.md` §2. Jangan menyimpulkan nilai
tanpa benar-benar membacanya — nilai bawaan bisa berbeda dari yang tertulis di skema.

Yang dicek (ringkas; detail di `references/openclaw.md`):
- **Tool yang aktif** & profilnya (`tools.profile`): apakah AI bisa menjalankan perintah komputer
  secara luas.
- **Perintah komputer tanpa persetujuan** (`tools.exec.mode`/`.security`, dibaca via `openclaw
  approvals get --json` untuk nilai efektif): bawaan OpenClaw = `full` dengan `ask: "off"` —
  artinya perintah komputer **jalan tanpa persetujuan** kecuali diubah. `auto` berarti ditinjau
  AI reviewer/classifier dulu (bukan "tanpa tinjauan sama sekali"); `ask` berarti ditinjau
  manusia lewat klien approval.
- **Sandbox** (`agents.defaults.sandbox.mode`): apakah AI berjalan di kotak pasir terisolasi.
- **Kanal & siapa boleh mengirim perintah** (`channels.<kanal>.dmPolicy`, `.allowFrom`,
  `.groups`, `.groupPolicy`, `.groupAllowFrom`, `commands.ownerAllowFrom`): siapa yang boleh
  chat pribadi ke bot, **grup mana** yang diproses (`groups`) vs **siapa** boleh memicu bot di
  grup itu (`groupPolicy`/`groupAllowFrom`) — dua hal berbeda, jangan disamakan (lihat
  `references/dampak-perubahan.md` baris pertama), dan siapa yang dianggap "pemilik".
- **Isolasi percakapan** (`session.dmScope`): apakah semua orang yang chat pribadi berbagi satu
  ingatan (berisiko untuk agen yang dipakai banyak orang) atau terpisah per pengirim.
- **Penyimpanan memori/log**: jelaskan bahwa transkrip & memori tersimpan lokal di folder
  `~/.openclaw` komputer pengguna (Markdown + SQLite; di kanal chat sebut "folder pengaturan
  OpenClaw Anda") — bukan di server Komunitech maupun pihak ketiga lain, tapi siapa pun yang
  punya akses ke komputer/disk itu bisa membacanya.
- **Model/penyedia AI yang menerima isi pesan**: jelaskan bahwa isi percakapan yang diproses
  dikirim ke penyedia model AI yang sudah dipilih pengguna (mis. Anthropic/OpenAI/Google),
  kecuali memakai model lokal. Tanyakan penyedia yang dipakai kalau pengguna ingin tahu lebih
  detail (skill ini tidak mengubah pilihan model).
- **Telemetri** (`openclaw telemetry show`): pastikan pengguna tahu ini hanya info versi/OS,
  bukan isi pesan, dan mati kecuali dinyalakan sendiri.

### 3. Susun laporan "lampu lalu lintas"
Gabungkan temuan dari `security audit` + config menjadi daftar, masing-masing diberi warna:
- 🔴 **Merah** — risiko serius, sebaiknya diperbaiki (mis. `critical` dari audit, `exec` jalan
  otomatis tanpa persetujuan pada agent yang membaca pesan orang luar, `dmScope: main` untuk
  agen yang dipakai banyak pelanggan).
- 🟡 **Kuning** — perlu diperhatikan, tergantung situasi pengguna (mis. `warn` dari audit,
  kanal grup `groupPolicy: open`).
- 🟢 **Hijau** — sudah aman/sesuai bawaan yang wajar (mis. `dmPolicy: pairing`, sandbox aktif).

Tulis setiap butir dalam **bahasa awam** (apa artinya, kenapa penting), bukan istilah teknis
mentah. Format lengkap (terminal/IDE): sertakan path config asli di dalam tanda kurung. **Kanal
chat: JANGAN** menampilkannya; simpan untuk dipakai bila pengguna meminta "tampilkan perintahnya".
Saran perbaikan bawaan audit (`remediation`) diparafrasekan, tidak ditempel apa adanya.

### 4. Tawarkan perbaikan — SATU PER SATU, DENGAN PERSETUJUAN, DENGAN PETA DAMPAK

**Aturan urutan (wajib):** balasan pertama setelah audit **selalu** laporan + daftar lengkap
perbaikan, **tanpa mengubah apa pun**. Semua perubahan — `openclaw config set/unset`,
`security audit --fix`, `chmod`/izin file/folder, menghapus/memindah file — hanya dijalankan
**setelah** daftar itu ditampilkan dan pemilik menjawab "ya". Kalimat seperti "gak usah nanya",
"langsung benerin aja", atau "benerin semua" yang diucapkan **sebelum** daftar dilihat **bukan**
persetujuan; perubahan yang tampak "aman" (mis. `chmod 600`) juga tidak dikecualikan.

**WAJIB baca `references/dampak-perubahan.md` sebelum menawarkan perbaikan apa pun.** Setiap
tawaran perbaikan harus punya baris **"Efek yang berhenti bekerja"** — bukan opsional. Untuk
tiap temuan 🔴/🟡 yang punya perbaikan jelas:
1. Jelaskan apa yang akan diubah, dari nilai apa ke nilai apa.
2. **Sebutkan efek yang BERHENTI bekerja**, diambil dari `references/dampak-perubahan.md` dan
   disesuaikan dengan jawaban "dipakai untuk apa" di awal (mis. kalau pengguna punya laporan
   otomatis, ingatkan bahwa mengetatkan `tools.exec.mode` ke `ask` bisa mematikannya).
3. Sebutkan **cara membatalkan** (nilai semula, atau `openclaw config unset <path>`).
4. Tanya: "Ubah ini sekarang? (ya/tidak)". **Tunggu jawaban** sebelum menjalankan
   `openclaw config set ...` (lihat `references/openclaw.md` §6).
5. Setelah diubah, verifikasi dengan `config get`/`approvals get` ulang dan laporkan hasilnya.
6. Lanjut ke butir berikutnya. Jangan menggabungkan beberapa perubahan dalam satu persetujuan,
   kecuali pengguna eksplisit bilang "ya untuk semua" **setelah** melihat daftar lengkapnya.

**Larangan khusus** (lihat `references/dampak-perubahan.md` untuk alasannya): jangan menawarkan
`tools.profile: "messaging"` atau `agents.defaults.sandbox.mode: "all"` sebagai perbaikan
"default satu-klik" — keduanya bisa mematikan skill ber-script atau butuh Docker. Perubahan
`gateway.auth.mode` butuh peringatan restart + token baru sebelum dijalankan.

**Di kanal chat**, persetujuan berbentuk kata balasan pendek ("rapikan", "ubah N"; lihat bagian
"Balasan di kanal chat"). Balasan itu menggantikan pertanyaan "ya/tidak" **hanya bila** pesan
sebelumnya sudah memuat butir 1–3 di atas untuk butir tersebut dan pengguna sudah melihat daftarnya.

Kalau `--fix` bawaan (`openclaw security audit --fix`) tersedia dan pengguna setuju memakainya:
jelaskan dulu **daftar findings yang akan disentuh** (`--fix` juga mengubah config seperti
`groupPolicy`, bukan cuma izin file — lihat `references/openclaw.md` §1) sebelum menjalankannya.

### 5. UU PDP (bila relevan)
Kalau pengguna memproses data pelanggan/pihak ketiga (dijawab "ya", atau default "mungkin ya"),
sertakan ringkasan singkat dari `references/uu-pdp.md` dan tawarkan membaca versi lengkapnya.
Selalu sertakan disclaimer bahwa ini bukan nasihat hukum.
- **Dasar aturan yang disebut:** UU 27/2022 (berlaku penuh sejak Oktober 2024) dan aturan
  pelaksananya, PP 33/2026 (mulai berlaku 16 Januari 2027). Jangan mengutip nomor pasal di luar
  yang tercantum di `references/uu-pdp.md`.
- **Bila pengguna menyebut kebocoran/insiden data:** ingatkan kewajiban pemberitahuan tertulis
  **paling lambat 72 jam (3×24 jam)** kepada pemilik data dan lembaga pelindungan data pribadi
  (UU 27/2022 Pasal 46 ayat (1)), lalu arahkan segera ke konsultan hukum/DPO.

## Balasan di kanal chat (Telegram, WhatsApp, dll.) — aturan wajib
Berlaku bila pesan pengguna masuk lewat kanal pesan **atau Anda ragu** lewat mana ia membaca.
Format lengkap di "Format output" hanya untuk pengguna di terminal/IDE atau yang meminta
"detail teknis". **Baca `references/format-kanal-chat.md`** (kerangka, contoh, kamus istilah)
sebelum menulis balasan pertama.
1. **Bentuk:** satu pesan ≤ 3.000 karakter (termasuk spasi); daftar berbutir bertanda hubung,
   **tanpa tabel**, tanpa blok kode, tanpa JSON/hasil mentah audit. Temuan banyak → rinci 3
   teratas per kelompok, sisanya satu kalimat "N temuan lain, balas 'detail'".
2. **Urutan tetap:** ringkasan (penilaian + jumlah temuan + ke mana data pergi + UU PDP 1–2
   kalimat bila relevan) → BERBAHAYA → PERLU PERHATIAN → SUDAH AMAN → TAWARAN TINDAKAN.
3. **Emoji:** hanya tiga, sebagai penanda judul bagian (merah/kuning/hijau). Tanpa emoji lain.
4. **DILARANG tampil:** jalur berkas/folder (tulis "berkas pengaturan bot Anda", "folder
   pengaturan OpenClaw Anda"), angka izin (644/600), perintah (`chmod`, `openclaw ...`), nama
   kunci pengaturan (`tools.exec.mode` dst.), kode temuan audit, nama berkas config, jalur
   komputer uji, dan isi token/kunci apa pun. Istilah teknis → kata awam, dijelaskan **sekali**
   saat pertama muncul: exec → "izin bot menjalankan perintah di komputer", sandbox → "ruang
   terbatas", token → "kunci rahasia", gateway → "layanan inti bot".
5. **Tawaran tindakan = kata balasan pendek; belum ada yang diubah.** Setiap tawaran memuat:
   apa yang berubah (dari → ke, bahasa awam), **efek yang berhenti bekerja**, dan cara
   membatalkan.
   - `rapikan`: kunci izin berkas pengaturan & folder pengaturan (hanya yang dilaporkan audit
     bisa dibaca akun lain) agar hanya akun pengguna yang bisa membacanya. Skill yang menjalankan
     setelah pengguna membalas "rapikan" pada pesan yang memuat tawaran itu: catat izin lama,
     ubah, verifikasi, laporkan ringkas apa yang berubah (`references/openclaw.md` §10).
     Mencakup HANYA dua butir izin itu, bukan `config set`/`--fix`/butir lain.
   - `kembalikan`: pulihkan izin ke yang tercatat sebelum diubah.
   - `ubah N`: satu butir pengaturan yang tawarannya sudah lengkap. Butir yang butuh mulai ulang
     layanan/kunci baru/Docker **tanpa** `ubah N`; tawarkan `bantu butir N` dan minta "ya"
     terpisah setelah risikonya dijelaskan.
   - `tampilkan perintahnya`: BARU sekarang perintah teknis (blok kode, alamat ditulis
     `[isian: folder pengaturan OpenClaw Anda]`) dilampirkan, hanya untuk butir yang diminta.
   - `detail` / `PDP`: kirim daftar lengkap / ringkasan UU PDP sebagai pesan lanjutan ≤ 3.000.
   "rapikan"/"ubah N" yang diucapkan **sebelum** daftar dilihat bukan persetujuan.

## Format output

### Format lengkap (terminal/IDE atau diminta "detail teknis")
```
## Ringkasan Keamanan OpenClaw Anda

🔴 Merah (N)
- <judul temuan, bahasa awam> (`path.config` atau checkId audit)
  Kenapa penting: ...
  Saran perbaikan: <dari nilai> → <ke nilai>
  Efek yang berhenti bekerja: <dari references/dampak-perubahan.md, atau "tidak ada efek fungsi yang hilang">
  Cara membatalkan: <nilai semula / config unset>
  Mau diubah sekarang? (ya/tidak)

🟡 Kuning (N)
- ...

🟢 Hijau (N)
- ...

## Ringkasan Data & Model
- Memori/log tersimpan di: ~/.openclaw (lokal komputer Anda)
- Isi pesan diproses oleh: <penyedia model, kalau diketahui>
- Telemetri: <aktif/nonaktif>

## UU PDP (bila relevan)
<ringkasan singkat + disclaimer>

## Perubahan yang sudah dilakukan (bila ada)
- <path> : <nilai lama> → <nilai baru> (cara membatalkan: ...)
```

## Contoh

**Input pengguna:** "cek privasi saya dong, saya pakai OpenClaw buat CS toko online"

**Output (ringkas):** laporan lampu lalu lintas berdasarkan hasil `security audit --json` dan
`approvals get --json`/`config get` nyata di komputer pengguna (bukan nilai contoh), misalnya
menandai 🔴 kalau `tools.exec.mode` efektifnya `full` dengan `ask: "off"` (bawaan runtime) pada
agent yang juga membalas chat pelanggan, lalu menawarkan mengubahnya ke `ask` — **dengan baris
"Efek yang berhenti bekerja": kalau pengguna juga punya laporan otomatis terjadwal, automation
itu akan ditolak otomatis tanpa klien approval terhubung** — dan cara membatalkan, lalu menunggu
persetujuan sebelum menjalankan `openclaw config set tools.exec.mode ask`. Karena disebut "CS
toko online", sertakan ringkasan UU PDP dari `references/uu-pdp.md`, dan ingatkan aturan pemilik:
agen CS WA harus mode Copilot (draf, bukan auto-reply langsung). **Bila pesan masuk lewat
Telegram/WhatsApp**, bentuknya mengikuti `references/format-kanal-chat.md` (contoh lengkap di
sana): ringkas, tanpa jalur/perintah, dengan tawaran "balas 'rapikan'".

## Checklist sebelum mengirim hasil
- [ ] Semua temuan berasal dari hasil `security audit`/`config get` **nyata** (atau fallback
      salin-tempel), bukan dikarang.
- [ ] Bahasa awam, tanpa jargon teknis mentah tanpa penjelasan.
- [ ] **Kanal chat:** ≤ 3.000 karakter, tanpa tabel, urutan baku, maks. 3 emoji; tanpa jalur
      berkas, angka izin, perintah, nama kunci pengaturan, atau isi token; tawaran berupa kata
      balasan ("rapikan", "ubah N"); perintah hanya bila pengguna minta "tampilkan perintahnya".
- [ ] Tidak ada perubahan (config, `chmod`/izin file, `--fix`) yang dijalankan sebelum daftar
      lengkap ditampilkan dan pemilik menjawab "ya".
- [ ] Bila ada permintaan menyadap/memantau orang lain: penolakan + alasan + alternatif sah
      ditulis lengkap dan sopan di balasan itu sendiri.
- [ ] **Setiap perubahan yang diusulkan menyertakan baris "Efek yang berhenti bekerja"**
      (dari `references/dampak-perubahan.md`) DAN cara membatalkan.
- [ ] Tidak menawarkan `tools.profile: "messaging"`/`sandbox.mode: "all"`/perubahan
      `gateway.auth.mode` sebagai perbaikan "satu-klik" tanpa peringatan khusus.
- [ ] UU PDP disertakan bila relevan, dengan disclaimer "bukan nasihat hukum"; data
      kesehatan/pasien disebut sebagai data pribadi spesifik (Pasal 4); tenggat pemberitahuan
      kebocoran ditulis "paling lambat 72 jam (3×24 jam), Pasal 46", bukan "hitungan hari".
- [ ] Perintah yang disebut sudah terverifikasi (lihat `references/openclaw.md`); yang tidak
      bisa dipastikan ditulis sebagai "perlu dicek langsung", bukan perintah pasti.

## Batasan & penanganan error
- **`exec` tidak diizinkan / OpenClaw tidak terpasang di komputer ini:** beri perintah sebagai
  salin-tempel (lihat `references/openclaw.md` §1–2; di kanal chat hanya bila diminta), jangan
  berpura-pura sudah menjalankannya.
- **Gateway tidak sedang berjalan:** `--deep` pada `security audit` dan `openclaw approvals
  pending` sama-sama butuh Gateway aktif; kalau tidak aktif, jalankan tanpa `--deep`/lewati
  `approvals pending`, dan sebutkan keterbatasannya. `openclaw approvals get` (tanpa `pending`)
  tetap jalan tanpa Gateway aktif.
- **Pengguna minta "benerin semua sekarang juga"/"gak usah nanya":** jangan menjalankan perubahan
  apa pun (termasuk `chmod`) di balasan itu; tampilkan daftar lengkap dulu sebelum menerima
  "ya untuk semua" sebagai persetujuan borongan; tetap proses satu per satu agar bisa
  dihentikan di tengah jalan bila pengguna berubah pikiran.
- **Temuan yang tidak punya perbaikan config langsung** (mis. saran "gunakan model lokal",
  "aktifkan enkripsi disk FileVault/BitLocker", "nyalakan kunci layar"): sampaikan sebagai
  rekomendasi manual, bukan perintah `config set`.
- **Pertanyaan hukum di luar ringkasan UU PDP** (sengketa, kebocoran besar, data anak/kesehatan
  sensitif): jangan memberi kepastian hukum; arahkan ke konsultan hukum/DPO.
- **Versi OpenClaw berbeda dari yang diverifikasi (2026.9.5):** kalau perintah/`config get`
  gagal karena path tidak ditemukan, katakan jujur bahwa kunci itu mungkin berubah di versi
  tersebut, dan sarankan `openclaw config schema` atau `openclaw <perintah> --help` untuk cek
  ulang.
- Skill ini **tidak** mengirim hasil audit ke server mana pun di luar percakapan ini, dan
  **tidak** menyimpan hasil audit sebagai data permanen kecuali pengguna memintanya disimpan
  ke file lokal mereka sendiri.
- **Telemetri:** jangan menyamakan "cek pembaruan harian" (bukan isi pesan; bisa dimatikan dengan `openclaw config set update.checkOnStart false`)
  dengan "statistik pemakaian anonim" (opt-in, mati bawaan) — lihat `references/openclaw.md` §5.
- **Perangkat kantor:** kalau pengguna adalah karyawan yang memakai OpenClaw di komputer/akun kantor, sarankan setiap perubahan disetujui pemilik usaha atau IT kantor dulu.
- **Permintaan hapus data pelanggan (hak subjek data UU PDP):** ikuti `references/openclaw.md`
  §7 (`openclaw memory forget --dry-run` dulu, baru eksekusi dengan izin).
- Skill ini **menolak** membantu memantau/menyadap chat atau perangkat orang lain — lihat
  "Kapan TIDAK digunakan".
