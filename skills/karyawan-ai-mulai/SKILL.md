---
name: karyawan-ai-mulai
description: Onboarding "Starter Kit Karyawan AI" untuk pengguna OpenClaw yang belum tahu mulai dari mana — wawancara maks. 5 pertanyaan, rekomendasi paket skill dari library Komunitech, bantu pasang skill (dengan izin), jalankan satu tugas pertama nyata, rencana 7 hari, dan arahkan ke cek privasi. Gunakan saat pengguna bilang "mulai karyawan AI", "bantu saya mulai pakai AI di bisnis", "setup asisten", "gimana caranya mulai", atau get started with AI employee, AI onboarding, setup AI assistant. Bukan untuk memeriksa/mengubah pengaturan keamanan (pakai cek-privasi-openclaw) atau menjalankan tugas spesifik (langsung pakai skill terkait, mis. rekap-penjualan-csv).
---

# Starter Kit "Karyawan AI" — Onboarding

> **Aturan kerja:** Jangan menginstal paket/aplikasi (mis. `pip install`) — bila perlu, tunjukkan caranya dan biarkan pengguna yang memasang; jangan membuka atau mencari file selain yang diberikan pengguna, isi folder skill ini, dan file yang disebut di langkah kerja; jangan menulis file baru tanpa menyebut lokasinya, dan simpan hasil di folder kerja yang disepakati (bukan /tmp).

## Tujuan
Membuat pengguna OpenClaw yang awam teknologi **mulai memakai** library skill Komunitech
dalam satu percakapan: dari "tidak tahu mulai dari mana" sampai punya hasil nyata di tangan
dan rencana 7 hari yang jelas.

## Kapan digunakan
- Pemicu: "mulai karyawan AI", "bantu saya mulai pakai AI di bisnis", "setup asisten",
  "gimana cara mulai pakai OpenClaw untuk bisnis saya", "onboarding", "karyawan AI".
- Pengguna baru pertama kali, atau ingin mengatur ulang paket kerjanya.

## Kapan TIDAK digunakan
- Pengguna sudah tahu skill apa yang mau dipakai dan tinggal jalan → langsung arahkan ke
  skill itu, jangan wawancara ulang.
- Permintaan tentang keamanan/privasi OpenClaw → pakai `cek-privasi-openclaw` (skill ini hanya
  **menyebut** dan menawarkannya di langkah terakhir).
- Menjadwalkan laporan otomatis secara mendetail (jadwal, sumber data, format) → arahkan ke
  skill `laporan-otomatis-terjadwal` (atau `buku-stok` untuk stok). Skill ini hanya menyebutnya
  sebagai "ide otomasi lanjutan" di rekomendasi awal, tidak menyusun jadwal penuh.

## Input — wawancara maksimal 5 pertanyaan

Tanyakan **sekali**, dalam satu pesan bernomor. Kalau OpenClaw berjalan di WhatsApp/kanal yang
mendukung tool `ask_user` dengan pilihan, tawarkan pilihan bernomor 1️⃣–4️⃣ per pertanyaan (maks.
4 opsi) supaya pengguna cukup membalas angka; kalau tidak, tanyakan sebagai teks biasa.

| # | Pertanyaan | Wajib? | Default jika tidak dijawab |
|---|---|---|---|
| 1 | Profesi/peran & industri usaha (mis. "owner toko F&B", "konsultan", "admin kantor") | Ya | Tanyakan ulang sekali; kalau tetap tidak ada, pakai "paket umum" |
| 2 | Skala tim — **4 opsi baku**: 1️⃣ solo, 2️⃣ 2–15 orang, 3️⃣ 16–50 orang, 4️⃣ 50+ orang (usaha 50+ dengan banyak cabang: tanyakan juga jumlah cabang) | Tidak | "solo" |
| 3 | 3 pekerjaan yang paling menyita waktu (bebas, boleh kurang dari 3) | Ya | Kalau kosong, tanyakan ulang sekali; kalau tetap kosong, pakai paket default industri |
| 4 | Kanal favorit untuk dibantu AI — **4 opsi baku**: 1️⃣ Telegram, 2️⃣ WhatsApp (nomor terpisah, baca risikonya dulu), 3️⃣ langsung di komputer, 4️⃣ belum tahu/terserah | Tidak | "Telegram" (kanal resmi, tanpa risiko blokir — lihat §7 `references/openclaw.md`) |
| 5 | Apakah ada kekhawatiran soal privasi/data, dan apakah komputer/laptop biasanya menyala terus (untuk laporan otomatis nanti) | Tidak | Anggap "ada kekhawatiran" (lebih aman) dan "komputer tidak selalu menyala" |

Kalau pengguna bilang "cepat saja" / "terserah" / ingin langsung mulai: **jangan** menahan di
wawancara. Pakai default di atas, sebutkan asumsinya secara singkat di akhir, dan lanjutkan.

## Langkah kerja

> **Lokasi script:** semua script skill ini ada di subfolder `scripts/` di folder yang sama dengan SKILL.md ini (folder skill). Jalankan dari sana; jangan mencari script atau file pengguna ke seluruh disk (mis. `find /`) — itu lambat dan menyentuh data pribadi di luar folder kerja.

1. **Wawancara** (lihat tabel Input). Tulis ringkasan satu paragraf dari jawaban sebelum lanjut,
   supaya pengguna bisa mengoreksi kalau salah tangkap.
2. **Cocokkan ke rekomendasi skill.** Gunakan `references/peta-skill.md` (tabel statis) sebagai
   sumber kebenaran. Kalau ingin hasil yang konsisten secara terprogram, jalankan (opsional):
   ```bash
   python3 <folder-skill-ini>/scripts/peta_kebutuhan.py --tugas "<tugas 1>" --tugas "<tugas 2>" \
     --tugas "<tugas 3>" --industri "<industri>" --json
   ```
   (Windows: `python`/`py`.) Kalau Python tidak bisa dijalankan, cocokkan **manual** memakai
   tabel di `references/peta-skill.md` — jangan menyebut nama skill yang tidak ada di tabel itu.
3. **Rekomendasikan minimal 3 skill "paket kerja pertama"** + alasan 1 baris per skill, dan
   sebutkan 1 ide otomasi lanjutan (tidak wajib dipasang sekarang) — lihat §5 di
   `references/openclaw.md`. **Selalu terapkan aturan pemilik** di §7 `references/openclaw.md`
   saat memberi rekomendasi/otomasi (kanal default Telegram, WA hanya nomor terpisah + izin
   risiko, CS WA selalu mode Copilot, kripto hanya riset/notifikasi, tanpa scraping marketplace).
   Untuk usaha 50+ karyawan dengan banyak cabang, sarankan eksplisit memisahkan rekap/laporan
   **per cabang** (satu file/folder data per cabang), bukan digabung jadi satu.
4. **Cek skill yang sudah terpasang, DAN pastikan yang belum terpasang benar-benar ADA di paket
   pembeli.** Ikuti `references/openclaw.md` §1 (`openclaw skills list`, atau baca folder skills
   bila `exec` tidak diizinkan) untuk yang sudah terpasang. Untuk rekomendasi yang belum
   terpasang, cek juga apakah foldernya ada di dalam Starter Kit/paket yang diunduh pengguna
   (lihat §2) sebelum berjanji memasangnya — **jangan asumsikan semua skill di
   `references/peta-skill.md` otomatis ada di paket pembeli** (bundle bisa berbeda-beda, dan
   sebagian skill library terus bertambah). Kalau skill yang direkomendasikan ternyata tidak ada
   di kedua tempat (belum terpasang DAN tidak ada foldernya), katakan jujur: *"<nama skill> belum
   tersedia di paket Anda saat ini"*, lalu ganti dengan skill terdekat dari
   `references/peta-skill.md` atau paket umum. Tandai hasilnya: sudah ada / perlu dipasang (ada
   foldernya) / belum tersedia di paket.
5. **Pandu pemasangan skill yang belum ada — SELALU minta izin eksplisit dulu.** Ikuti
   `references/openclaw.md` §2: cari dulu folder hasil ekstrak Starter Kit (biasanya di folder
   Unduhan), lalu pasang. Jangan pernah memasang tanpa konfirmasi "ya/lanjut" dari pengguna.
   Kalau muncul pesan "already exists", jelaskan artinya dan tanya dulu sebelum memakai `--force`.
   Verifikasi hasil pasang dengan `openclaw skills info <nama>`. Jangan memasang dari sumber di
   luar paket Komunitech tanpa izin eksplisit terpisah. Jangan mempublikasikan skill apa pun ke
   ClawHub. Kalau `exec`/`read`/`write` tidak diizinkan (mis. profil tool `messaging`), jelaskan
   ke pengguna dan beri langkah salin-tempel manual — lihat catatan prasyarat di
   `references/openclaw.md` §1.
6. **Jalankan SATU tugas pertama nyata** memakai skill yang paling relevan dari rekomendasi,
   dengan data pengguna kalau ada, atau data contoh (`examples/` skill terkait) kalau belum ada.
   Pengguna harus melihat **hasil siap pakai** di menit pertama, bukan penjelasan umum.
7. **Simpan profil kerja** (bukan data pribadi pelanggan) ke memori lokal sesuai
   `references/openclaw.md` §4, supaya skill lain tidak bertanya ulang hal yang sama.
8. **Tawarkan memasang "Aturan kerja Komunitech" ke `AGENTS.md` workspace** (OpenClaw saja).
   Alasan untuk pengguna (1 kalimat): OpenClaw membaca `AGENTS.md` di setiap percakapan, jadi
   aturan aman (pesan ke pelanggan = draf, tidak mengulang password, tidak memasang apa pun tanpa
   izin, dll.) tetap berlaku walau skill tidak terbuka. Langkah:
   a. Tampilkan **isi lengkap** `references/aturan-kerja-agents.md` di chat dulu.
   b. Baca `AGENTS.md` di workspace OpenClaw (biasanya `~/.openclaw/workspace/AGENTS.md`; jangan
      mencari ke seluruh disk — bila tidak ada di sana, tanyakan lokasinya). Kalau sudah ada
      baris `komunitech-aturan-kerja: mulai`, katakan "sudah terpasang" dan lewati (bila versinya
      lebih lama, tawarkan mengganti **hanya** blok di antara penanda `mulai`…`selesai`).
   c. Minta konfirmasi eksplisit ("ya/tidak"). Setelah "ya": **tambahkan** blok di akhir file
      (append), jangan menimpa atau mengubah isi lain. File belum ada → buat baru berisi blok itu.
   d. Sebutkan lokasi lengkap file dan bahwa aturan berlaku mulai **sesi baru** (`/new`).
   `write`/`exec` tidak diizinkan, atau pengguna memakai platform lain → beri langkah salin-tempel
   manual (Control UI: Settings → Agents → Files → AGENTS.md). Pengguna menolak → lanjut saja.
9. **Beri rencana 7 hari** — satu kebiasaan baru per hari, memakai skill dari rekomendasi.
   Format lihat di bawah. Sesuaikan urutan dengan tugas prioritas pengguna.
10. **Tawarkan cek privasi.** Jelaskan singkat (2 kalimat) apa yang dicek `cek-privasi-openclaw`,
   dan tanyakan apakah mau langsung dijalankan sekarang atau nanti. **Jangan** menjalankannya
   sendiri di sini — itu tanggung jawab skill `cek-privasi-openclaw`.

## Format output

```
## Ringkasan Anda
<1 paragraf: profesi, skala tim, tugas prioritas, kanal, catatan privasi/komputer>

## Rekomendasi Paket Kerja Pertama
1. **<skill>** — <alasan 1 baris>
2. **<skill>** — <alasan 1 baris>
3. **<skill>** — <alasan 1 baris>

Ide otomasi lanjutan (opsional, bisa nanti): <1 kalimat>

## Status Pemasangan
- Sudah terpasang: <daftar atau "belum ada">
- Perlu dipasang: <daftar, ada foldernya di paket> → [tunggu izin pengguna sebelum memasang]
- Belum tersedia di paket Anda: <daftar, bila ada> — dipakai skill pengganti: <nama>

## Hasil Tugas Pertama
<hasil nyata dari skill yang dijalankan — bukan penjelasan, tapi output siap pakai>

## Rencana 7 Hari
| Hari | Kebiasaan baru | Skill |
|---|---|---|
| 1 | ... | ... |
| 2 | ... | ... |
| ... | ... | ... |
| 7 | ... | ... |

## Aturan Kerja Komunitech
<isi blok ditampilkan> — boleh saya tambahkan ke akhir AGENTS.md Anda (<lokasi>)? (ya/tidak)
[setelah "ya"] Ditambahkan ke <lokasi lengkap>; berlaku mulai sesi baru (/new).

## Privasi
Data Anda tetap di komputer Anda. Mau saya jalankan cek privasi dasar sekarang (skill
`cek-privasi-openclaw`), atau lain kali saja?

**Asumsi yang dipakai (bila ada default):** <sebutkan>
```

## Contoh

**Input pengguna:** "mulai karyawan AI, saya owner toko kopi kecil, tim 4 orang, paling capek
bikin caption tiap hari, balas chat WA, sama rekap jualan tiap minggu, semua lewat WhatsApp,
laptop kadang mati"

**Output (ringkas):**
```
## Ringkasan Anda
Anda owner toko kopi (F&B), tim 4 orang, ingin dibantu untuk caption harian, balas chat
pelanggan, dan rekap penjualan mingguan — semua lewat WhatsApp. Laptop tidak selalu menyala,
jadi laporan otomatis terjadwal belum cocok dulu untuk Anda.

## Rekomendasi Paket Kerja Pertama
1. **caption-sosmed-umkm** — caption siap tempel tiap hari, hemat waktu bikin konten.
2. **balas-chat-cs** — draf balasan chat pelanggan dari FAQ sampai komplain.
3. **rekap-penjualan-csv** — kirim file penjualan mingguan, langsung dapat rekap omzet & tren.

Ide otomasi lanjutan: laporan mingguan otomatis lewat Telegram (lebih stabil dari WA Web),
tapi perlu komputer menyala terus — bisa dibahas nanti.

## Status Pemasangan
- Sudah terpasang: belum ada
- Perlu dipasang: caption-sosmed-umkm, balas-chat-cs, rekap-penjualan-csv → boleh saya pasang
  sekarang ke folder skill global OpenClaw Anda? (ya/tidak)

[setelah "ya"]
## Hasil Tugas Pertama
<contoh: 3 caption siap tempel untuk promo kopi hari ini, dari brief singkat pengguna>

## Rencana 7 Hari
| Hari | Kebiasaan baru | Skill |
|---|---|---|
| 1 | Minta 1 caption pagi sebelum buka toko | caption-sosmed-umkm |
| 2 | Coba draf balasan untuk 3 chat pelanggan | balas-chat-cs |
| 3 | Kirim file penjualan kemarin, minta rekap singkat | rekap-penjualan-csv |
| 4 | Minta caption untuk promo mingguan | caption-sosmed-umkm |
| 5 | Balas 5 chat pelanggan pakai draf AI | balas-chat-cs |
| 6 | Review rekap penjualan minggu ini | rekap-penjualan-csv |
| 7 | Evaluasi: skill mana paling membantu, lanjut paket berikutnya? | — |

## Privasi
Data Anda tetap di komputer Anda. Mau saya jalankan cek privasi dasar sekarang, atau lain kali?
```

## Checklist sebelum mengirim hasil
- [ ] Wawancara maksimal 5 pertanyaan, dalam satu pesan.
- [ ] Rekomendasi skill berasal dari `references/peta-skill.md` (atau script), bukan tebakan.
- [ ] Skill yang belum terpasang sudah dicek benar-benar ada foldernya di paket pembeli sebelum
      dijanjikan — bukan diasumsikan otomatis ada.
- [ ] Tidak ada pemasangan skill tanpa izin eksplisit pengguna.
- [ ] Ada minimal satu hasil nyata siap pakai (bukan cuma rencana).
- [ ] Blok aturan kerja ditampilkan dulu dan hanya ditambahkan (append) ke AGENTS.md setelah
      "ya"; isi AGENTS.md lain tidak diubah; tidak dipasang dua kali.
- [ ] Rencana 7 hari konkret dan sesuai prioritas pengguna.
- [ ] Menyebut fakta yang belum pasti dengan jujur (mis. skill tidak ada padanan, otomasi
      butuh komputer menyala).
- [ ] Tidak menjanjikan hal di luar §"Batasan" (posting otomatis medsos, auto-trading,
      diagnosis medis, dll.).
- [ ] Mengikuti aturan pemilik (§7 `references/openclaw.md`): Telegram sebagai kanal default,
      WA hanya nomor terpisah + izin risiko, CS WA mode Copilot, kripto hanya riset/notifikasi,
      tanpa scraping marketplace via login browser.

## Batasan & penanganan error
- **Kredensial & jadwal (wajib):** JANGAN pernah mencari, membaca, atau menampilkan token/API key/kredensial dari environment (`env`, `printenv`), file konfigurasi (mis. `openclaw.json`, `.env`), atau riwayat; kanal Telegram diatur lewat pairing/konfigurasi OpenClaw oleh pengguna sendiri. Buat jadwal hanya setelah pengguna membalas "ya" atas perintah + jam yang ditunjukkan; kanal belum siap atau perintah ditolak → berhenti dan beri langkah persiapannya, jangan menyelidiki sendiri.
- **Industri/tugas tanpa padanan di `peta-skill.md`:** katakan jujur, jangan mengarang nama
  skill. Tawarkan paket umum atau skill terdekat.
- **Skill yang direkomendasikan (mis. `laporan-otomatis-terjadwal`, `buku-stok`, atau skill baru
  lain) ternyata tidak ada di paket pembeli** (tidak terpasang DAN tidak ada foldernya di Starter
  Kit): jangan berjanji memasangnya. Katakan jujur "belum tersedia di paket Anda saat ini" dan
  pakai skill pengganti terdekat dari `references/peta-skill.md`.
- **`exec`/perintah komputer tidak diizinkan:** ikuti fallback di `references/openclaw.md` —
  beri perintah salin-tempel, jangan berhenti begitu saja.
- **Skill baru dipasang tapi belum "terlihat":** ini normal (snapshot skill dibaca ulang tiap
  sesi baru). Minta pengguna mengulang permintaan atau membuka sesi baru.
- **Pengguna minta otomasi terjadwal tapi komputer tidak menyala 24 jam:** jelaskan jujur bahwa
  jadwal tidak akan berjalan kalau Gateway OpenClaw mati/komputer tidur, dan sarankan opsi
  (komputer yang selalu menyala, atau tunda dulu otomasi).
- **Data sensitif** (kesehatan pasien, keuangan pribadi orang lain, dsb.) yang muncul saat
  wawancara: jangan disimpan ke memori lokal kecuali perlu untuk pekerjaan itu sendiri, dan
  ingatkan pengguna soal UU PDP bila menyangkut data pelanggan/karyawan.
- **Permintaan di luar cakupan library** (posting otomatis ke Instagram/TikTok, auto-trading
  kripto, skrining/diagnosis medis, clone wajah/suara, scraping/narik data marketplace lewat
  login browser otomatis, auto-reply langsung ke pelanggan di WA tanpa Copilot): tolak dengan
  sopan, jelaskan alasannya singkat sesuai §7 `references/openclaw.md`, dan arahkan ke
  `cek-privasi-openclaw` atau skill lain yang relevan bila ada.
- **Usaha besar/multi-cabang (50+ karyawan):** jangan menggabung data semua cabang jadi satu
  rekap tanpa diminta — sarankan file/folder data terpisah per cabang agar laporan tetap akurat.
- Skill ini **tidak** memasang paket dari luar Starter Kit Komunitech, **tidak** mempublikasikan
  apa pun ke ClawHub, dan **tidak** mengirim data pengguna ke server di luar penyedia model AI
  yang sudah dipilih pengguna sendiri.
