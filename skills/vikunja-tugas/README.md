# Vikunja Tugas: Kelola Tugas Tim Tanpa Biaya Bulanan

**Ketik "tugas apa yang harus selesai hari ini?", "tambahkan tugas cek stok cat, jatuh tempo Jumat, tugaskan ke Budi", atau tempel notulen rapat WA — AI Anda langsung membaca dan menyiapkan tugas di Vikunja, aplikasi manajemen tugas gratis yang jalan di komputer/server sendiri.**

*Diuji AI penguji independen: 6,0 → 8,5 dari 10 (pembeda terbesar: menolak hapus massal dan menolak memakai kunci akses yang ditempel di chat; untuk mengurai notulen biasa hasilnya setara).*

> Komunitech **tidak berafiliasi** dengan proyek Vikunja. Vikunja adalah software open-source (kode terbuka, lisensi AGPL-3.0) milik komunitasnya sendiri; skill dan panduan ini adalah karya orisinal Komunitech untuk mempermudah pemakaiannya bagi pemilik usaha Indonesia.

> **Yang Anda butuhkan:** AI agent yang mendukung skill (OpenClaw, Claude Code, Codex, atau Cursor — langganan AI-nya ditanggung sendiri) di komputer Windows/Mac/Linux. Python 3 (bawaan Mac/Linux, unduh gratis di Windows) untuk skrip hitung; tanpa Python skill tetap berjalan dengan hitungan oleh AI. Software tambahan: Vikunja (gratis, open-source; panduan pemasangan disertakan). Tidak perlu API key atau akun tambahan dari Komunitech.

## Manfaat
- ✅ **Tanpa biaya per user.** Vikunja gratis dan berjalan di komputer/server Anda sendiri, jadi tidak ada tagihan bulanan per orang seperti pada layanan Trello, ClickUp, atau Asana berbayar (langganan AI Anda tetap ditanggung sendiri).
- ✅ **Cukup ngobrol, bukan klik-klik menu.** "Tugas apa yang telat?", "tambahkan tugas ... jatuh tempo Jumat depan" — AI yang menerjemahkan ke Vikunja, termasuk tanggal gaya Indonesia ("besok", "lusa", "Jumat depan", "25/10"). Diuji di OpenClaw dengan data contoh (Vikunja tidak dijalankan); sambungan ke Vikunja asli diuji terpisah (lihat Hasil uji).
- ✅ **Notulen WA jadi daftar tugas dalam sekali tempel.** Rangkuman rapat/grup WA diubah jadi draf daftar tugas terstruktur (siapa, apa, kapan) yang Anda periksa dulu sebelum benar-benar dibuat. Jujur: untuk sekadar menguraikan notulen, AI tanpa skill sudah sama baiknya; nilai skill ada di pratinjau dan penyimpanan langsung ke Vikunja.
- ✅ **Tahu siapa pegang apa, tanpa buka aplikasi.** Ringkasan tugas terbuka dikelompokkan per anggota tim (termasuk yang belum ada penanggung jawabnya). Laporan pagi otomatis ke Telegram (lewat OpenClaw; jadwal ini belum diuji langsung) memuat tugas hari ini dan yang terlambat.
- ✅ **Dirancang hati-hati untuk data tim.** Default hanya membaca. Menambah tugas dan menandai selesai ditampilkan sebagai pratinjau dulu dan baru dijalankan setelah Anda menjawab "ya". Kunci akses (token) disimpan di komputer Anda dan tidak ditampilkan oleh skill ini.

## Cocok untuk siapa
- Toko/usaha kecil-menengah, kantor konsultan, kafe, bengkel — tim 3–20 orang yang butuh daftar tugas bersama tanpa berlangganan aplikasi bulanan.
- Pemilik/admin yang ingin cukup bertanya ke AI agent (diuji di OpenClaw) tanpa menghafal tampilan Vikunja.
- Tim yang koordinasi kerjanya masih lewat grup WA dan sering ada tugas "hilang" karena tenggelam di chat.

**Kurang cocok:** belum punya server/komputer yang bisa menyala terus untuk Vikunja (lihat instalasi — bisa laptop kantor biasa); butuh sub-tugas, tugas berulang otomatis, atau tampilan papan kartu (Kanban) lewat AI (untuk saat ini masih harus lewat layar Vikunja langsung); tim besar (>20 orang) dengan struktur organisasi kompleks — Vikunja tetap bisa, tapi nilai tambah skill ini paling terasa di tim kecil.

## Contoh sebelum & sesudah
**Sebelum:** buka Vikunja → cari proyek → klik "+ New Task" → ketik judul → klik kalender pilih tanggal → cari nama di kolom assignee → simpan. Untuk tahu status tim: buka tiap proyek satu-satu, baca satu per satu tugas siapa pegang apa.

**Sesudah:** ketik *"Tambahkan tugas untuk Toko Bangunan: cek stok cat tembok, jatuh tempo Jumat, tugaskan ke Budi, prioritas tinggi"*:
```
PRATINJAU TAMBAH TUGAS
1.
   Judul : Cek stok cat tembok
   Proyek: Toko Bangunan Sinar Jaya (id 2)
   Tenggat: Jumat, 2 Oktober 2026
   Prioritas: 3 (tinggi)
   Ditugaskan ke: budi

Belum disimpan. Ulangi perintah yang sama + --ya untuk menyimpan ke Vikunja.
```
Setelah "ya":
```
TERSIMPAN 1 TUGAS DI VIKUNJA:
- #8 Cek stok cat tembok (proyek id 2)
```
(Contoh nyata dari uji dengan Vikunja 2.6.0 asli.)

Atau minta AI mengubah catatan rapat jadi daftar tugas. Ini cuplikan jawaban asli dari uji di OpenClaw (tanggal dihitung dari Jumat, 2 Oktober 2026; PIC = penanggung jawab tugas; belum disimpan ke Vikunja sebelum Anda setuju):
```
1. **Follow up supplier bata**
   - PIC: Budi
   - Tenggat: sebelum Rabu, 7 Oktober 2026

2. **Kirim invoice ke PT ABC** (urgent)
   - PIC: Siti
   - Tenggat: Sabtu, 3 Oktober 2026

3. **Beli semen 50 sak untuk proyek Pak Haryo**
   - PIC: Andi
   - Tenggat: ⚠️ tidak disebutkan di notulen
...
Mau saya langsung masukkan ke Vikunja sekarang (termasuk yang PIC/tanggalnya belum jelas), atau tunggu kamu lengkapi dulu poin #3 dan #4?
```

## Cara pakai
Setelah Vikunja terpasang dan tersambung, cukup ketik permintaan biasa:
- "Cek Vikunja saya sudah nyambung belum"
- "Tugas apa yang harus selesai hari ini?", "yang telat apa saja?"
- "Tambahkan tugas ... jatuh tempo besok, tugaskan ke Siti"
- "Tandai tugas #12 selesai"
- "Siapa pegang tugas apa sekarang?"
- "Ini notulen rapat tadi, tolong jadikan daftar tugas"
- "Kirim tugas hari ini ke Telegram saya tiap jam 7 pagi" (OpenClaw)

## Instalasi singkat
1. **Vikunja** sudah terpasang dan menyala. Belum? Ikuti `docs/panduan-vikunja.md` di paket (unduh program resminya, ±15–30 menit), **termasuk langkah pengamanan wajib** (batasi agar hanya bisa dibuka dari komputer itu sendiri, alamat `127.0.0.1`, dan jangan buka ke internet), atau pakai **jasa setup Komunitech**. Panduan ini dicoba langsung di Linux; pemasangan di Windows/Mac belum dicoba langsung.
2. Salin folder `vikunja-tugas` ke folder skills AI agent:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |

(Panduan lengkap termasuk Windows: `CARA-INSTAL.md` di dalam paket.)

3. Buat kunci akses (token API) di Vikunja (Settings > API Tokens, izin sesuai kebutuhan — lihat `docs/panduan-vikunja.md` §6), lalu simpan sekali (di terminal Anda sendiri, bukan di chat): `python3 ~/.openclaw/skills/vikunja-tugas/scripts/vikunja.py simpan-kunci` (Windows: `python` / `py`).
4. Coba: "Cek Vikunja saya sudah nyambung belum?"

**Hasil uji (jujur):**
- **Uji OpenClaw, 2 Oktober 2026** (penguji AI independen; angka dari `examples/00-openclaw-sebelum-sesudah.md`, dua skenario dengan data contoh): rata-rata nilai 6,0 tanpa skill menjadi 8,5 dengan skill (skala 10). Pembeda terbesar ada di keamanan: saat kunci akses (token) ditempel di chat dan diminta "hapus semua tugas lama", nilainya 4 tanpa skill menjadi 9 dengan skill. Untuk mengurai notulen biasa menjadi tugas, AI tanpa skill sudah setara (8 vs 8). Pada uji ini aplikasi Vikunja tidak dijalankan.
- **Uji sambungan ke Vikunja asli (versi 2.6.0, di Linux):** dilakukan terpisah oleh pembuat dan penguji independen; rincian di `examples/HASIL-UJI.md`.

**Status uji (jujur):** diuji di OpenClaw. Pemasangan Vikunja di Windows/Mac, jadwal laporan otomatis ke Telegram, serta Claude Code, Codex, dan Cursor belum diuji langsung (format skill-nya sama).

## FAQ
**Apakah data tugas tim saya dikirim ke server Komunitech atau pihak lain?**
Tidak. Skrip skill ini hanya menghubungi Vikunja **milik Anda sendiri** (biasanya di komputer Anda sendiri). Skrip tidak mengirim data ke Komunitech; satu-satunya kiriman keluar adalah laporan ke Telegram bila Anda sendiri mengaktifkan jadwalnya. Seperti memakai AI agent pada umumnya, isi percakapan Anda tetap diproses layanan AI yang Anda pakai.

**Saya belum punya Vikunja, apa saya perlu server mahal?**
Tidak — satu file program kecil yang bisa dijalankan di laptop/PC kantor biasa yang menyala saat jam kerja. Untuk laporan pagi otomatis, komputer itu perlu menyala saat jadwalnya (lihat `docs/panduan-vikunja.md` §7), atau gunakan jasa setup Komunitech untuk memasangnya di mini PC atau server sewaan (VPS).

**Bisakah AI menghapus tugas atau mengubah tim tanpa sepengetahuan saya?**
Skill ini sengaja **tidak punya** perintah hapus tugas/proyek atau ubah anggota tim. Menambah tugas dan menandai selesai menunjukkan pratinjau dulu dan baru berjalan setelah Anda menjawab "ya". Sebagai lapis pengaman tambahan, buat kunci akses Vikunja dengan izin seperlunya saja (lihat `docs/panduan-vikunja.md` bagian 6).
