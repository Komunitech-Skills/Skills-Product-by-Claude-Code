# Papan Saran Pelanggan Sendiri, Tanpa Biaya Bulanan

**Pelanggan mengusulkan dan memberi suara; AI Anda merapikan, menggabung duplikat, meringkas yang paling diminta, dan menyiapkan kabar "sudah kami perbaiki".**

Diuji AI penguji independen di OpenClaw (dengan server Fider tiruan berisi data contoh): 4,5 → 9 dari 10 (tanpa skill nama atau nomor pelanggan bisa ikut tampil di papan publik; dengan skill ada pratinjau, penyamaran data, dan penggabungan usulan kembar).

> Komunitech **tidak berafiliasi** dengan tim Fider (getfider). Fider adalah software gratis berkode terbuka (open-source, lisensi AGPL-3.0) milik pengembangnya dan **tidak ikut dalam paket ini**; skill dan panduan ini adalah karya orisinal Komunitech yang terhubung ke Fider lewat pintu data resminya (REST API, jalur bagi program untuk berbicara dengan Fider) di komputer/server Anda sendiri.

> **Yang Anda butuhkan:** AI agent yang mendukung skill (OpenClaw, Claude Code, Codex, atau Cursor — langganan AI-nya ditanggung sendiri) di komputer Windows/Mac/Linux. Python 3 (bawaan Mac/Linux, unduh gratis di Windows) untuk menjalankan skrip pendukung skill ini; tanpa Python skill tetap berjalan, AI mengerjakannya langsung tetapi hasil angka sebaiknya Anda cek ulang. Software tambahan: Fider (gratis, open-source; panduan pemasangan disertakan). Tidak perlu API key atau akun tambahan dari Komunitech.

## Manfaat
- ✅ **Pengganti layanan papan saran berlangganan (seperti Canny atau UserVoice).** Papan usulan + voting + status (Direncanakan, Dikerjakan, Selesai) jalan di komputer atau VPS (server sewaan) Anda; data tidak dititipkan ke pihak lain.
- ✅ **Catatan WA dan ulasan marketplace jadi usulan rapi.** Tempel catatan, AI menyusun judul, memeriksa yang sudah pernah masuk, dan **menyamarkan nomor HP/email** sebelum tampil di papan.
- ✅ **Perubahan ditulis setelah Anda setuju.** Perubahan tampil sebagai pratinjau dulu; baru ditulis ke papan setelah Anda bilang "ya".
- ✅ **Tahu apa yang paling diminta.** Ringkasan mingguan: usulan teratas menurut suara, yang baru masuk, dan yang baru selesai (bisa dijadwalkan tiap Senin ke Telegram; jadwal otomatis diuji di bot Telegram uji 2026-10-13, lihat `examples/UJI-JADWAL-TELEGRAM-2026-10-13.md`).
- ✅ **Kabar perbaikan siap kirim.** Ubah status lalu minta draf "sudah kami perbaiki" (sopan atau santai) untuk Anda kirim sendiri ke pelanggan.

## Cocok untuk siapa
- **UMKM & toko online** yang menerima saran lewat WhatsApp, DM, dan ulasan marketplace, tetapi sulit mencatat dan mengurutkannya.
- **Tim produk kecil, pengelola aplikasi berlangganan (SaaS), dan komunitas** yang butuh halaman "usulkan fitur" dan rencana pengembangan (roadmap) yang bisa dilihat publik.
- **Konsultan/agensi** yang mengelola papan saran untuk beberapa klien.

**Kurang cocok:** yang belum punya komputer/VPS yang menyala terus dan email pengirim (lihat panduan atau pakai jasa setup); yang hanya butuh membalas ulasan (pakai skill Komunitech lain, `balas-ulasan-pelanggan`, khusus untuk menulis balasan ulasan); yang ingin menganalisis ratusan chat sekaligus (pakai skill Komunitech lain, `iterasi-dari-masukan-pelanggan`, lalu impor hasilnya ke sini).

## Contoh sebelum & sesudah
**Sebelum:** 40 catatan WA dan ulasan berserakan; usulan "bayar QRIS" muncul 6 kali dengan kata berbeda; tidak jelas mana yang paling banyak diminta; pelanggan yang meminta jarang dikabari.

**Sesudah:** ketik *"Masukkan catatan WA ini ke papan saran."*
```
RENCANA MASUKKAN KE PAPAN dari catatan.txt: 4 butir
1. [BUAT  ] Seorang pelanggan minta bisa bayar pakai QRIS
      (nama dan nomor HP dari catatan tidak ikut ditulis; papan Fider biasanya publik)
2. [BUAT  ] Tolong ada notifikasi WA kalau pesanan sudah dikirim, minta 3 orang
3. [BUAT  ] Ongkir ke luar Jawa sering salah hitung. Kontak: [email disembunyikan]
4. [TAHAN] Tambah pembayaran QRIS
      MIRIP dengan #1 "Tambah pembayaran QRIS" (hanya petunjuk) - ditahan: tanyakan pemilik
PRATINJAU - BELUM ADA YANG DITULIS ke Fider. Tunggu persetujuan Anda dulu.
```
Balas "ya" → dibuat. Lalu: *"Gabungkan #3 ke #1"*, *"Apa yang paling banyak disuka minggu ini?"*, *"#5 sudah selesai, buatkan kabarnya."* (Contoh dengan data fiktif, dipersingkat dari format keluaran skill. Keluaran hasil uji, termasuk dari Fider v0.38.0 asli yang dijalankan pembuat skill, ada di folder `examples/`.)

## Cara pakai
Setelah Fider terpasang dan kunci akses (kunci API) disimpan, cukup ketik permintaan biasa ke AI agent Anda, misalnya:
- "Cek apakah Fider saya nyambung."
- "Masukkan catatan WA ini ke papan saran." (lalu tempel catatan)
- "Usulan apa yang paling banyak disukai minggu ini?"
- "Gabung usulan #3 ke #1 kalau memang sama maksudnya."
- "Usulan #5 sudah selesai, buatkan kabar untuk pelanggan (sopan)."

Perubahan ke papan ditampilkan sebagai **pratinjau** dulu; balas **"ya"** bila sudah benar, baru ditulis ke Fider.

## Instalasi singkat
Skill = folder `fider-masukan-pelanggan/`. Salin ke folder skill platform Anda (lokasi lengkap per platform di `docs/instalasi.md`): **OpenClaw**, **Codex**, **Claude Code**, **Cursor**. Lalu pasang Fider mengikuti **`docs/panduan-fider.md`** (lewat Docker, program untuk menjalankan aplikasi dalam kotak terisolasi, ±30 menit; butuh email pengirim; Windows dan macOS belum diuji langsung) dan buat kunci API. Kunci disimpan sendiri oleh Anda dengan `python3 scripts/fider.py simpan-kunci` (Windows: `python` atau `py`); **jangan tempel kunci di chat**.

**Tidak mau repot?** Ada **jasa setup berbayar Komunitech**: komputer/VPS, domain + HTTPS, Fider + database, email pengirim, kunci API, tag awal, dan jadwal ringkasan Telegram. Hubungi admin komunitech.com.

**Hasil uji (angka nyata):** uji OpenClaw (uji otomatis agent, lingkungan uji terpisah), 2026-10-02, skor 1–10 penguji independen. Sumber semua angka: `examples/00-openclaw-sebelum-sesudah.md`. Uji ini memakai server Fider tiruan berisi data contoh (bukan Fider asli), jadi yang dinilai adalah perilaku AI-nya.
- Uji ulang skill v1.0.5 (dua skenario): tanpa skill **4,5** → dengan skill **9,0** (LULUS).
- Uji ulang skill v1.0.7 (satu skenario): tanpa skill **5** → dengan skill **9** (LULUS).

Tanpa skill, nama/nomor pelanggan bisa masuk komentar publik; dengan skill, ada pratinjau + persetujuan "ya", data disensor, duplikat digabung. Terpisah dari uji di atas, pembuat skill menjalankan alurnya pada Fider v0.38.0 asli (Docker + PostgreSQL); catatannya ada di `examples/HASIL-UJI.md`.

**Status uji (jujur):** sudah diuji di OpenClaw (uji sebelum/sesudah otomatis agent, 2026-10-02) dan Claude Code (simulasi agent). Jadwal ringkasan ke Telegram (automations one-shot) diuji bot uji 2026-10-13. Codex dan Cursor belum kami uji langsung. Windows/macOS Fider dan HTTPS VPS sungguhan belum diverifikasi end-to-end.

## Bukti uji di bot Telegram

Uji terbaru: 27 Oktober 2026, versi 1.0.10, di bot OpenClaw asli (grup uji internal Komunitech, server Fider tiruan berisi data contoh), dengan pesan yang sama untuk kedua sisi: masukkan empat catatan pelanggan dari WA ke papan saran, lalu beri ringkasan usulan yang paling banyak diminta, tanpa menulis ke Fider sebelum dijawab. Skor 1-10 dari penilai independen: tanpa skill **7** → dengan skill **6** (selisih -1): **belum lulus acuan kami** (dengan skill di bawah 8, dan di uji ini skill kalah).

Dengan skill, kunci akses yang sudah tersimpan terbaca (masalah di uji sebelumnya teratasi), nomor HP pelanggan dibuang dari usulan, usulan QRIS yang mirip dengan yang sudah ada ditahan untuk Anda putuskan, dan tidak ada yang ditulis sebelum Anda menjawab. Namun bagian ringkasan usulan paling banyak diminta tidak dikerjakan: usulan QRIS (14 suara) hanya disebut "kemungkinan" terbanyak, tanpa urutan suara. Tanpa skill, bot memberi ringkasan peringkat usulan lengkap dengan jumlah suara dan tiga draf usulan baru, juga tanpa menulis apa pun.

Catatan jujur: satu pesan uji per sisi. Di sisi tanpa skill, bot sempat memakai berkas sisa uji lama di komputer uji (bukan folder skill), jadi pembandingnya agak lebih mudah dari kondisi pembeli sungguhan. Perbaikan ringkasan suara (versi 1.0.11) belum diuji ulang di bot Telegram.

Uji sebelumnya: 12 Okt 2026, di bot OpenClaw asli (grup uji internal Komunitech), dengan server Fider tiruan berisi data contoh di komputer uji dan pesan yang sama di kedua sisi. Tanpa skill skor **8** → dengan skill skor **5** (selisih −3): belum lulus acuan kami, dan hasil ini belum bisa dipakai sebagai ukuran nilai tambah skill.

Yang terjadi: bot dengan skill hanya membalas petunjuk menyimpan kunci akses, padahal kunci uji sudah tersimpan di komputer uji. Kunci itu tidak terbaca saat skill aktif, jadi pratinjau impor dan ringkasan usulan tidak keluar. Bot tanpa skill justru sempat memberi pratinjau impor dan ringkasan usulan QRIS (14 suara).

Catatan jujur: sesudah uji itu skill diperbaiki agar mencari dan membaca kunci sendiri (versi 1.0.8, 12 Okt 2026). Pemeriksaan internal sesudahnya lolos, tetapi uji ulang sebelum/sesudah di bot Telegram belum dilakukan, jadi skill ini belum terbukti unggul di Telegram. Uji otomatis agent sebelumnya (2 Okt 2026) dan uji jadwal ringkasan mingguan ke Telegram (13 Okt 2026) ada di bagian Instalasi singkat di atas.

## FAQ
**Apakah Fider dan biayanya gratis?** Fider gratis (AGPL-3.0) bila dipasang sendiri. Anda hanya membayar listrik/VPS dan email pengirim (banyak penyedia punya paket gratis kecil). Paket ini berisi skill, script, dan panduan Komunitech; Fider diunduh dari sumber resminya.

**Apakah AI bisa merusak papan saya?** Skill tidak punya perintah menghapus pos atau mengubah pengaturan. Penulisan (impor, tag, gabung, status, komentar) diminta persetujuan Anda lewat pratinjau dulu. Sebaiknya buat akun Collaborator (akun staf dengan hak terbatas) khusus AI (panduan Fider, bagian 6) dan cadangkan database (basis data) secara berkala (panduan Fider, bagian 10).

**Bagaimana dengan privasi pelanggan?** Papan Fider bisa dilihat publik. Skill menyamarkan nomor HP, telepon rumah/kantor, dan email otomatis, tetapi nama dan detail pesanan Anda periksa sendiri di pratinjau. Catat hanya usulan, bukan data pelanggan. Detail ada di panduan Fider, bagian 9.

## Riwayat perubahan

Versi terkini: **1.0.11**. Rincian teknis tiap versi ada di `CHANGELOG.md` di folder skill ini.
