# Vikunja Tugas: Kelola Tugas Tim Tanpa Biaya Bulanan

**Ketik "tugas apa yang harus selesai hari ini?", "tambahkan tugas cek stok cat, jatuh tempo Jumat, tugaskan ke Budi", atau tempel notulen rapat WA — AI Anda langsung membaca dan menyiapkan tugas di Vikunja, aplikasi manajemen tugas gratis yang jalan di komputer/server sendiri.**

> Komunitech **tidak berafiliasi** dengan proyek Vikunja. Vikunja adalah software open-source (AGPL-3.0) milik komunitasnya sendiri; skill dan panduan ini adalah karya orisinal Komunitech untuk mempermudah pemakaiannya bagi pemilik usaha Indonesia.

## Manfaat
- ✅ **Tanpa biaya per user, selamanya.** Vikunja gratis, jalan di komputer/server Anda sendiri — tidak ada tagihan bulanan seperti Trello Standard, ClickUp, atau Asana untuk tim kecil.
- ✅ **Cukup ngobrol, bukan klik-klik menu.** "Tugas apa yang telat?", "tambahkan tugas ... jatuh tempo Jumat depan" — AI yang menerjemahkan ke Vikunja, termasuk tanggal gaya Indonesia ("besok", "lusa", "Jumat depan", "25/10").
- ✅ **Notulen WA jadi to-do list dalam sekali tempel.** Rangkuman rapat/grup WA diubah jadi draf daftar tugas terstruktur (siapa, apa, kapan) yang Anda periksa dulu sebelum benar-benar dibuat — bukan sekadar disalin manual satu per satu.
- ✅ **Tahu siapa pegang apa, tanpa buka aplikasi.** Ringkasan tugas terbuka dikelompokkan per anggota tim (termasuk yang belum ada penanggung jawabnya), dan laporan pagi otomatis ke Telegram (lewat OpenClaw) memuat tugas hari ini & yang terlambat.
- ✅ **Aman untuk data tim.** Default hanya membaca. Menambah tugas dan menandai selesai selalu lewat pratinjau dan butuh persetujuan Anda. Token akses disimpan aman dan tidak pernah ditampilkan.

## Cocok untuk siapa
- Toko/usaha kecil-menengah, kantor konsultan, kafe, bengkel — tim 3–20 orang yang butuh daftar tugas bersama tanpa berlangganan SaaS.
- Pemilik/admin yang ingin cukup bertanya ke AI agent (diuji di OpenClaw) tanpa menghafal tampilan Vikunja.
- Tim yang koordinasi kerjanya masih lewat grup WA dan sering ada tugas "hilang" karena tenggelam di chat.

**Kurang cocok:** belum punya server/komputer yang bisa menyala terus untuk Vikunja (lihat instalasi — bisa laptop kantor biasa); butuh sub-tugas, tugas berulang otomatis, atau tampilan Kanban lewat AI (masih harus lewat layar Vikunja langsung di v1.0.x); tim besar (>20 orang) dengan struktur organisasi kompleks — Vikunja tetap bisa, tapi nilai tambah skill ini paling terasa di tim kecil.

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

Atau tempel notulen WA:
```
- Andi: follow up supplier semen besok
- Rina: kirim invoice ke PT Jaya lusa
```
AI menjawab draf yang bisa langsung Anda cek sebelum dikirim ke Vikunja — bukan janji, hasil sungguhan (lihat `examples/`).

**Hasil uji (OpenClaw, uji otomatis agent, 2026-10-02):** rata-rata nilai 6,0 tanpa skill menjadi 8,5 dengan skill (skala 10). Pembeda terbesar ada di keamanan: saat token ditempel di chat dan diminta "hapus semua tugas lama", nilainya 4 tanpa skill menjadi 9 dengan skill. Untuk mengurai notulen biasa menjadi tugas, AI tanpa skill sudah setara (8 vs 8). Jujur: uji ini memakai data contoh dan aplikasi Vikunja tidak dijalankan; sambungan ke Vikunja asli (versi 2.6.0) sudah diuji terpisah oleh pembuat. Rincian: `examples/00-openclaw-sebelum-sesudah.md`.

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
1. **Vikunja** sudah terpasang dan menyala. Belum? Ikuti `docs/panduan-vikunja.md` di paket (unduh binary resmi ±15–30 menit), **termasuk langkah pengamanan wajib** (ikat ke `127.0.0.1`, jangan buka ke internet), atau pakai **jasa setup Komunitech**.
2. Salin folder `vikunja-tugas` ke folder skills AI agent:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |

(Panduan lengkap termasuk Windows: `CARA-INSTAL.md` di dalam paket.)

3. Buat token API di Vikunja (Settings > API Tokens, izin sesuai kebutuhan — lihat `docs/panduan-vikunja.md` §6), lalu simpan sekali (di terminal Anda sendiri, bukan di chat): `python3 ~/.openclaw/skills/vikunja-tugas/scripts/vikunja.py simpan-kunci` (Windows: `python` / `py`).
4. Coba: "Cek Vikunja saya sudah nyambung belum?"

## FAQ
**Apakah data tugas tim saya dikirim ke server Komunitech atau pihak lain?**
Tidak. Script ini hanya menghubungi Vikunja **milik Anda sendiri** (biasanya `127.0.0.1`, komputer/server Anda). Tidak ada data yang dikirim ke Komunitech atau internet, kecuali Anda sendiri mengatur jadwal laporan ke Telegram.

**Saya belum punya Vikunja, apa saya perlu server mahal?**
Tidak — satu file program kecil yang bisa dijalankan di laptop/PC kantor biasa yang menyala saat jam kerja. Untuk laporan pagi otomatis, komputer itu perlu menyala saat jadwalnya (lihat `docs/panduan-vikunja.md` §7), atau gunakan jasa setup Komunitech untuk memasangnya di mini PC/VPS.

**Bisakah AI menghapus tugas atau mengubah tim tanpa sepengetahuan saya?**
Tidak. Skill ini sengaja **tidak punya** perintah hapus tugas/proyek atau ubah anggota tim. Menambah tugas dan menandai selesai selalu menunjukkan pratinjau dulu dan baru berjalan setelah Anda menjawab "ya".
