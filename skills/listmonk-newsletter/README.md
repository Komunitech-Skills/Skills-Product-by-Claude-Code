# Newsletter Email Tanpa Biaya per Kontak

**Suruh AI Anda menyiapkan kontak, menulis email promo dalam bahasa Indonesia, mengujinya ke diri sendiri, menjadwalkan, dan membaca berapa yang membuka dan mengklik. Semua lewat listmonk, aplikasi newsletter gratis yang jalan di komputer/server Anda sendiri, tanpa biaya bulanan per jumlah kontak (biaya server, domain, dan layanan pengirim email tetap ada).**

Diuji AI penguji independen di OpenClaw (dengan server listmonk tiruan dan data contoh, bukan pengiriman email sungguhan): 4,0 → 8,7 dari 10 pada uji ulang v1.0.6 (13 Okt 2026, server tiruan; uji 2 Okt 5,5 → 9,0) (tanpa skill, AI langsung memasukkan 21 kontak berstatus "sudah konfirmasi" termasuk alamat salah ketik dan membuat draf tanpa tautan berhenti berlangganan; dengan skill ada pratinjau dulu, alamat salah ketik ditahan, dan tautan berhenti tersedia).

> **Yang Anda butuhkan:** AI agent yang mendukung skill (OpenClaw, Claude Code, Codex, atau Cursor — langganan AI-nya ditanggung sendiri) di komputer Windows/Mac/Linux (Windows dan macOS belum diuji langsung). Python 3 (bawaan Mac/Linux, unduh gratis di Windows) untuk menjalankan skrip pendukung skill ini; tanpa Python skill tetap berjalan, AI mengerjakannya langsung tetapi hasil angka sebaiknya Anda cek ulang. Software tambahan: Listmonk (gratis, open-source; panduan pemasangan disertakan), dijalankan di komputer/server Anda sendiri; layanan pengirim email (SMTP), domain, dan server ber-HTTPS (alamat aman berawalan https://) untuk newsletter sungguhan adalah biaya tersendiri di luar paket ini. Tidak perlu API key atau akun tambahan dari Komunitech.

## Manfaat
- ✅ **Bebas biaya per kontak.** Mailchimp menarik biaya makin mahal seiring daftar membesar; listmonk sendiri gratis. Biaya yang tetap ada: pengirim email (SMTP, "kantor pos" untuk email) yang murah atau ber-paket gratis, domain, dan server sewaan (VPS) bila tidak dipasang di komputer Anda.
- ✅ **Membantu menjaga kepatuhan hukum dan reputasi pengirim.** Pengingat persetujuan UU PDP 27/2022, **double opt-in** (pendaftar mengklik tautan konfirmasi di email dulu), tautan berhenti berlangganan wajib, dan **menolak daftar tanpa persetujuan (beli, hasil menyedot data situs/scraping, grup WA, vendor, "dapat dari teman")**; saringan ini berbasis kata kunci, bukan jaminan hukum.
- ✅ **AI dirancang agar tidak "kelepasan kirim".** Sebelum email keluar ke daftar, AI menampilkan jumlah penerima dan menunggu jawaban "ya" Anda; kirim ditolak bila versi isi yang sama belum diuji-kirim ke alamat milik Anda sendiri (tanpa jalan pintas di dalam skill), atau bila tautan berhenti berlangganan tidak benar-benar ada (tautan di dalam komentar HTML tidak dihitung). Pengaman ini melindungi dari kelalaian agent, bukan dari orang yang punya akses penuh ke komputer Anda (lihat "Batasan yang jujur").
- ✅ **File daftar kontak berantakan jadi rapi.** Bisa berupa CSV (tabel sederhana dari Excel/Google Sheets) atau Excel. Email rusak, duplikat, salah ketik (`gmial.com`), dan yang menolak, dibuang atau ditandai otomatis; angka dihitung program kecil (script), bukan dikira.
- ✅ **Email Indonesia siap kirim, dan tahu hasilnya.** Subjek, sapaan nama, ajakan pesan WhatsApp, dan cek risiko spam; lalu terkirim, dibuka, klik, dan tautan terlaris, dengan catatan jujur cara membaca angka.

## Cocok untuk siapa
- UMKM yang punya **daftar pelanggan sendiri** (pembeli toko, peserta kelas, member) dan ingin kirim promo/kabar bulanan.
- Freelancer, penulis, kreator, dan komunitas dengan newsletter rutin.
- Yang sudah pakai OpenClaw/Codex/Claude Code/Cursor dan ingin AI mengurus pekerjaan email marketing.

**Kurang cocok:** yang belum punya daftar pelanggan yang sah (skill ini menolak daftar beli); yang butuh kirim pesan massal (blast) lewat WhatsApp; yang tidak mau memasang server/Docker (aplikasi pembungkus untuk menjalankan server) dan tidak mau memakai jasa setup. Butuh **layanan pengirim email (SMTP)** dan **domain email sendiri**; biaya SMTP, domain, dan server di luar paket ini.

## Contoh sebelum & sesudah
**Sebelum (tanpa skill):** AI menyarankan "gunakan Mailchimp" atau menulis email umum tanpa tahu cara memakai listmonk lewat program (API); impor CSV berantakan dilakukan manual; tidak ada pengingat persetujuan; mudah salah kirim ke seluruh daftar.

**Sesudah:** "Ini kontak.csv, masukkan ke newsletter" ->
```
Kontak valid dan siap diimpor : 5
Email tidak valid (dibuang)   : 1
Duplikat (dibuang)            : 1
Menolak/belum setuju (dibuang): 1
Perlu dicek manual (salah ketik?) - TETAP disertakan: 1
  baris 5: t***@gmial.com (mungkin maksudnya @gmail.com)
```
AI lalu bertanya sekali apakah alamat yang tampak salah ketik mau dibetulkan dulu. "Kirim promo sekarang" (padahal email belum diuji-kirim ke diri sendiri) ->
```
  list 'Newsletter Toko Uji' (opt-in double): 2 penerima
  Uji-kirim ke diri sendiri: BELUM / isi berubah sejak uji
DITOLAK: lakukan 'uji-kirim' ke email Anda sendiri dulu (isi harus sama persis).
```
Setelah email diuji-kirim ke diri sendiri, barulah AI menanyakan "Kirim ke sekitar 2 orang di list tsb? (ya/tidak)" dan menunggu jawaban Anda.
"Hasilnya gimana?" -> `Dibuka (perkiraan): 1 = 50,0%` / `Klik tautan: 1 = 50,0%` / tautan terlaris. (Contoh nyata dari listmonk 6.2.0 dengan data fiktif; lihat `examples/`.)

## Cara pakai
Setelah listmonk terpasang dan tersambung, cukup ketik:
- "Cek listmonk saya sudah nyambung belum"
- "Periksa daftar pelanggan ini (kontak.xlsx), lalu masukkan ke newsletter" (AI akan menanyakan asal persetujuan)
- "Kirim email konfirmasi ke pelanggan baru"
- "Buatkan email promo diskon 15% sampai Minggu, ajakan pesan lewat WA"
- "Kirim contoh ke email saya dulu"
- "Jadwalkan Senin jam 9 pagi" / "Kirim sekarang"
- "Email kemarin berapa yang buka dan klik?"
- "Si Ani minta datanya dihapus"

## Instalasi singkat
1. **listmonk** terpasang dan menyala: ikuti `docs/panduan-listmonk.md` (memakai Docker, yaitu aplikasi pembungkus untuk menjalankan server; panduan untuk Windows/macOS/Linux, tetapi Windows/macOS belum diuji langsung; ±30-60 menit termasuk SMTP dan verifikasi domain) atau pakai **jasa setup Komunitech**.
2. Salin folder `listmonk-newsletter` ke folder skills AI agent (detail semua platform: `docs/instalasi.md`, di dalam paket bernama `CARA-INSTAL.md`):

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |

3. Buat akun API (akun akses untuk program) berizin terbatas (bagian 7 "Akun khusus AI" di `docs/panduan-listmonk.md`) lalu jalankan sendiri `python3 scripts/listmonk.py simpan-akun` (Windows: `python`/`py`). **Jangan tempel token (kunci rahasia) di chat.**
4. Daftarkan email Anda sendiri (maks. 3) untuk uji kirim: jalankan sendiri `python3 scripts/listmonk.py simpan-alamat-uji --email emailanda@...`. Uji kirim hanya boleh ke alamat ini.
5. Ketik "Cek listmonk saya nyambung belum".

Komunitech tidak berafiliasi dengan listmonk maupun Mailchimp (hanya disebut sebagai pembanding). listmonk (AGPL-3.0) tidak ikut didistribusikan di paket ini; skill dan panduannya karya Komunitech. Rincian: `ATTRIBUTION.md`.

**Hasil uji (angka nyata):** dua sumber yang terpisah.
- **Uji OpenClaw, uji otomatis agent, 2 Okt 2026** (tugas impor pendaftar pada v1.0.5, tugas daftar beli dari v1.0.4; angka dari `examples/00-openclaw-sebelum-sesudah.md`; versi terkini 1.0.6, pembaruan kecil sesudah uji: larangan menulis ulang kunci yang ditempel di chat): rata-rata nilai 5,5 tanpa skill menjadi 9,0 dengan skill (skala 10). Pada tugas impor pendaftar, AI tanpa skill langsung memasukkan 21 kontak berstatus "sudah konfirmasi" (melewati double opt-in), termasuk alamat salah ketik gmial.com, dan membuat draf tanpa tautan berhenti berlangganan; dengan skill ada pratinjau dulu, alamat salah ketik ditahan, draf lengkap dengan tautan berhenti, dan tidak ada yang terkirim (nilai 3 menjadi 9). Pada permintaan impor daftar beli, AI tanpa skill pun sudah menolak (8 vs 9). Catatan jujur: uji OpenClaw memakai server tiruan dan data contoh, jadi yang dinilai perilaku AI, bukan pengiriman email sungguhan.
- **Uji pembuat pada listmonk 6.2.0 asli** dengan SMTP penampung lokal (server surat percobaan di komputer sendiri). Belum diuji: pengiriman lewat Brevo/Amazon SES sungguhan, kotak masuk Gmail/Yahoo, dan Windows/macOS.

- **Uji ulang v1.0.6, 13 Okt 2026** (OpenClaw 2026.10.2, penguji independen, server listmonk tiruan, data contoh dibuat ulang mengikuti uji pertama): tanpa skill **4,0** → dengan skill **8,7** (selisih 4,7; lulus acuan kami). Tanpa skill 21 kontak langsung dimasukkan berstatus sudah konfirmasi (double opt-in dilewati) dan draf tanpa tautan berhenti; dengan skill tidak ada penulisan ke daftar pelanggan sebelum Anda mengonfirmasi, dan kampanye memuat tautan berhenti. Catatan jujur: alamat pengirim masih dikarang dan lokasi dua berkas tidak disebut; uji-kirim, jadwal, dan pengiriman sungguhan tidak diuji.

**Status uji (jujur):** sudah diuji di OpenClaw (uji otomatis agent, server tiruan) dan oleh pembuat pada listmonk asli; Codex, Claude Code, dan Cursor belum diuji langsung (format skill-nya sama). Skill bukan nasihat hukum.

## FAQ
**Apakah ini menjamin email tidak masuk spam?** Tidak. Masuk-inbox ditentukan penyedia SMTP, verifikasi domain (SPF/DKIM/DMARC, tanda pengenal agar email Anda tidak dianggap palsu), kualitas daftar, dan isi email. Skill memberi cek dasar dan panduan verifikasi, bukan jaminan.

**Bisakah saya mengimpor kontak dari daftar yang saya beli atau kumpulkan dari medsos?** Tidak. Skill hanya menerima kontak yang mendaftar sendiri: formulir di website, kotak opt-in saat checkout, atau persetujuan tertulis/terekam. Daftar beli, vendor, database, hasil menyedot data situs (scraping), grup WA, dan "dapat dari teman" ditolak karena tidak ada persetujuan orang-orangnya (UU PDP 27/2022) dan email Anda bisa diblokir. Sumber yang tidak dikenal harus Anda konfirmasi dan jawabannya dicatat. Catatan jujur: saringan ini pengaman tambahan berbasis kata kunci, bukan jaminan hukum; tanggung jawab tetap pada pemilik daftar.

**Apakah saya bisa memakai listmonk di laptop saja?** Untuk belajar, ya. Untuk newsletter sungguhan, tautan konfirmasi dan berhenti harus bisa dibuka penerima, jadi listmonk perlu server dengan HTTPS (`docs/panduan-listmonk.md`, bagian 2 "Pilih tempat memasang" dan 4 "Pasang listmonk dengan Docker Compose") atau jasa setup Komunitech.

## Batasan yang jujur
**Pengaman ini melindungi dari kelalaian agent, bukan dari orang yang punya akses terminal (jendela perintah) ke komputer Anda.** Gerbang uji-kirim, konfirmasi jumlah penerima, alamat uji, dan saringan sumber persetujuan mencegah agent salah kirim atau lupa menguji. Orang/agent dengan akses terminal (shell) ke komputer Anda tetap bisa memalsukan berkas catatan lokal (`listmonk-uji.json`, alamat uji), memakai terminal palsu, atau memanggil pintu akses (API) listmonk langsung. Catatan uji-kirim diberi tanda keaslian (HMAC) dengan kunci di folder konfigurasi Anda agar suntingan iseng terdeteksi, tetapi itu bukan pengaman terhadap penyerang. Tetap gunakan akun API berperan terbatas dan periksa ringkasan sebelum menjawab "ya".

## Riwayat perubahan

Versi terkini: **1.0.6**. Rincian teknis tiap versi ada di `CHANGELOG.md` di folder skill ini.
