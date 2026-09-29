# Papan Saran Pelanggan Sendiri, Tanpa Biaya Bulanan

**Pelanggan mengusulkan dan memberi suara; AI Anda merapikan, menggabung duplikat, meringkas yang paling diminta, dan menyiapkan kabar "sudah kami perbaiki".**

> Komunitech **tidak berafiliasi** dengan tim Fider (getfider). Fider adalah software open-source (lisensi AGPL-3.0) milik pengembangnya dan **tidak ikut dalam paket ini**; skill dan panduan ini adalah karya orisinal Komunitech yang memanggil REST API resmi Fider di komputer/server Anda sendiri.

## Manfaat
- ✅ **Pengganti Canny/UserVoice tanpa langganan.** Papan usulan + voting + status (Direncanakan, Dikerjakan, Selesai) jalan di komputer atau VPS Anda; data tidak dititipkan ke pihak lain.
- ✅ **Catatan WA dan ulasan marketplace jadi usulan rapi.** Tempel catatan, AI menyusun judul, memeriksa yang sudah pernah masuk, dan **menyamarkan nomor HP/email** sebelum tampil di papan.
- ✅ **Tidak ada yang tertulis tanpa izin Anda.** Semua perubahan tampil sebagai pratinjau dulu; baru ditulis setelah Anda bilang "ya".
- ✅ **Tahu apa yang paling diminta.** Ringkasan mingguan: usulan teratas menurut suara, yang baru masuk, dan yang baru selesai (bisa dikirim tiap Senin ke Telegram).
- ✅ **Kabar perbaikan siap kirim.** Ubah status lalu minta draf "sudah kami perbaiki" (sopan atau santai) untuk Anda kirim sendiri ke pelanggan.

## Cocok untuk siapa
- **UMKM & toko online** yang menerima saran lewat WhatsApp, DM, dan ulasan marketplace, tetapi sulit mencatat dan mengurutkannya.
- **Tim produk kecil, aplikasi, SaaS, komunitas** yang butuh halaman "usulkan fitur" dan roadmap publik.
- **Konsultan/agensi** yang mengelola papan saran untuk beberapa klien.

**Kurang cocok:** yang belum punya komputer/VPS yang menyala terus dan email pengirim (lihat panduan atau pakai jasa setup); yang hanya butuh membalas ulasan (pakai `balas-ulasan-pelanggan`); yang ingin menganalisis ratusan chat sekaligus (pakai `iterasi-dari-masukan-pelanggan`, lalu impor hasilnya ke sini).

## Contoh sebelum & sesudah
**Sebelum:** 40 catatan WA dan ulasan berserakan; usulan "bayar QRIS" muncul 6 kali dengan kata berbeda; tidak jelas mana yang paling banyak diminta; pelanggan yang meminta tidak pernah dikabari.

**Sesudah:** ketik *"Masukkan catatan WA ini ke papan saran."*
```
RENCANA IMPOR dari catatan.txt: 4 butir
1. [BUAT  ] Pelanggan minta bisa bayar pakai QRIS (Bu Rina [nomor disembunyikan])
      1 nomor HP/email disembunyikan (papan Fider biasanya publik)
2. [BUAT  ] Tolong ada notifikasi WA kalau pesanan sudah dikirim, minta 3 orang
3. [BUAT  ] Ongkir ke luar Jawa sering salah hitung. Kontak: [email disembunyikan]
4. [TAHAN] Tambah pembayaran QRIS
      mirip dengan #1 "Tambah pembayaran QRIS" (kemiripan 100%)
PRATINJAU - BELUM ADA YANG DITULIS ke Fider. ...
```
Balas "ya" → dibuat. Lalu: *"Gabungkan #3 ke #1"*, *"Apa yang paling banyak disuka minggu ini?"*, *"#5 sudah selesai, buatkan kabarnya."* (Keluaran nyata dari Fider v0.38.0 ada di folder `examples/`.)

## Instalasi singkat
Skill = folder `fider-masukan-pelanggan/`. Salin ke folder skill platform Anda (lokasi lengkap per platform di `docs/instalasi.md`): **OpenClaw**, **Codex**, **Claude Code**, **Cursor**. Lalu pasang Fider mengikuti **`docs/panduan-fider.md`** (Windows/macOS/Linux lewat Docker, ±30 menit; butuh email pengirim) dan buat kunci API. Kunci disimpan sendiri oleh Anda dengan `python3 scripts/fider.py simpan-kunci` (Windows: `python` atau `py`); **jangan tempel kunci di chat**.

**Tidak mau repot?** Ada **jasa setup berbayar Komunitech**: komputer/VPS, domain + HTTPS, Fider + database, email pengirim, kunci API, tag awal, dan jadwal ringkasan Telegram. Hubungi admin komunitech.com.

## FAQ
**Apakah Fider dan biayanya gratis?** Fider gratis (AGPL-3.0) bila dipasang sendiri. Anda hanya membayar listrik/VPS dan email pengirim (banyak penyedia punya paket gratis kecil). Paket ini berisi skill, script, dan panduan Komunitech; Fider diunduh dari sumber resminya.

**Apakah AI bisa merusak papan saya?** Skill tidak punya perintah menghapus pos atau mengubah pengaturan. Semua penulisan (impor, tag, gabung, status, komentar) butuh persetujuan Anda lewat pratinjau. Sebaiknya buat akun Collaborator khusus AI (panduan §6) dan cadangkan database berkala (panduan §10).

**Bagaimana dengan privasi pelanggan?** Papan Fider bisa dilihat publik. Skill menyamarkan nomor HP, telepon rumah/kantor, dan email otomatis, tetapi nama dan detail pesanan Anda periksa sendiri di pratinjau. Catat hanya usulan, bukan data pelanggan. Detail ada di panduan §9.

## Status jujur
Versi 1.0.2, status uji. Diuji pada Fider **v0.38.0 asli** (Docker + PostgreSQL 17, Linux; Administrator dan Collaborator) plus 43 uji otomatis. **Belum diuji:** Windows/macOS, jadwal OpenClaw/Telegram, HTTPS di VPS sungguhan. Uji banding oleh penguji independen dan uji platform asli menyusul.
