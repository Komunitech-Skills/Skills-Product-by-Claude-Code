# listmonk Newsletter: Kirim Email ke Pelanggan Tanpa Mailchimp

**Suruh AI Anda menyiapkan kontak, menulis email promo dalam bahasa Indonesia, mengujinya ke diri sendiri, menjadwalkan, dan membaca berapa yang membuka dan mengklik, memakai listmonk, aplikasi newsletter gratis yang jalan di komputer/server Anda sendiri, tanpa biaya bulanan per jumlah kontak.**

> Komunitech **tidak berafiliasi** dengan proyek listmonk. listmonk adalah software open-source (lisensi AGPL-3.0) milik pengembangnya; skill dan panduan ini karya orisinal Komunitech. Mailchimp adalah merek pihak ketiga yang disebut hanya sebagai pembanding.

## Manfaat
- ✅ **Bebas biaya per kontak.** Mailchimp menarik biaya makin mahal seiring daftar membesar; listmonk gratis, Anda hanya membayar pengirim email (SMTP) yang murah atau ber-paket gratis.
- ✅ **Aman secara hukum dan reputasi.** Pengingat persetujuan UU PDP 27/2022, **double opt-in**, tautan berhenti berlangganan wajib, dan **menolak daftar tanpa persetujuan (beli, scraping, grup WA, vendor, "dapat dari teman")**.
- ✅ **AI tidak bisa "kelepasan kirim".** Sebelum email keluar ke daftar, AI menampilkan jumlah penerima dan menunggu jawaban "ya" Anda; kirim ditolak bila versi isi yang sama belum diuji-kirim ke alamat milik Anda sendiri (tidak ada jalan pintas), atau bila tautan berhenti berlangganan tidak benar-benar ada (tautan di dalam komentar HTML tidak dihitung).
- ✅ **CSV/Excel berantakan jadi rapi.** Email rusak, duplikat, salah ketik (`gmial.com`), dan yang menolak, dibuang atau ditandai otomatis; angka dihitung script, bukan dikira.
- ✅ **Email Indonesia siap kirim.** Subjek, sapaan nama, ajakan pesan WhatsApp, dan cek risiko spam.
- ✅ **Tahu hasilnya.** Terkirim, dibuka, klik, tautan terlaris, dengan catatan jujur cara membaca angka.

## Cocok untuk siapa
- UMKM yang punya **daftar pelanggan sendiri** (pembeli toko, peserta kelas, member) dan ingin kirim promo/kabar bulanan.
- Freelancer, penulis, kreator, dan komunitas dengan newsletter rutin.
- Yang sudah pakai OpenClaw/Codex/Claude Code/Cursor dan ingin AI mengurus pekerjaan email marketing.

**Kurang cocok:** yang belum punya daftar pelanggan yang sah (skill ini menolak daftar beli); yang butuh blast WhatsApp; yang tidak mau memasang server/Docker dan tidak mau memakai jasa setup. Butuh **layanan pengirim email (SMTP)** dan **domain email sendiri**; biaya SMTP di luar paket ini.

## Contoh sebelum & sesudah
**Sebelum (tanpa skill):** AI menyarankan "gunakan Mailchimp" atau menulis email umum tanpa tahu API listmonk; impor CSV berantakan dilakukan manual; tidak ada pengingat persetujuan; mudah salah kirim ke seluruh daftar.

**Sesudah:** "Ini kontak.csv, masukkan ke newsletter" ->
```
Kontak valid dan siap diimpor : 5
Email tidak valid (dibuang)   : 1
Duplikat (dibuang)            : 1
Menolak/belum setuju (dibuang): 1
Perlu dicek manual (salah ketik?): baris 5: t***@gmial.com (mungkin maksudnya @gmail.com)
```
"Kirim promo sekarang" ->
```
  list 'Newsletter Toko Uji' (opt-in double): 2 penerima
  Uji-kirim ke diri sendiri: SUDAH (isi sama)
BELUM DIKIRIM. WAJIB tanya pengguna: 'Kirim ke sekitar 2 orang di list tsb? (ya/tidak)'
```
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
1. **listmonk** terpasang dan menyala: ikuti `docs/panduan-listmonk.md` (Docker; Windows/macOS/Linux; ±30-60 menit termasuk SMTP dan verifikasi domain) atau pakai **jasa setup Komunitech**.
2. Salin folder `listmonk-newsletter` ke lokasi skill platform Anda (detail semua platform di `docs/instalasi.md`):
   - **OpenClaw / Codex / Claude Code / Cursor:** rujuk `docs/instalasi.md` untuk folder skill masing-masing.
3. Buat akun API berizin terbatas (panduan §7) lalu jalankan sendiri `python3 scripts/listmonk.py simpan-akun` (Windows: `python`/`py`). **Jangan tempel token di chat.**
4. Daftarkan email Anda sendiri (maks. 3) untuk uji kirim: jalankan sendiri `python3 scripts/listmonk.py simpan-alamat-uji --email emailanda@...`. Uji kirim hanya boleh ke alamat ini.
5. Ketik "Cek listmonk saya nyambung belum".

## FAQ
**Apakah ini menjamin email tidak masuk spam?** Tidak. Masuk-inbox ditentukan penyedia SMTP, verifikasi domain (SPF/DKIM/DMARC), kualitas daftar, dan isi email. Skill memberi cek dasar dan panduan verifikasi, bukan jaminan.

**Bisakah saya mengimpor kontak dari daftar yang saya beli atau kumpulkan dari medsos?** Tidak. Skill hanya menerima kontak yang mendaftar sendiri: formulir di website, kotak opt-in saat checkout, atau persetujuan tertulis/terekam. Daftar beli, vendor, database, hasil scraping, grup WA, dan "dapat dari teman" ditolak karena tidak ada persetujuan orang-orangnya (UU PDP 27/2022) dan email Anda bisa diblokir. Sumber yang tidak dikenal harus Anda konfirmasi dan jawabannya dicatat. Catatan jujur: saringan ini pengaman tambahan berbasis kata kunci, bukan jaminan hukum; tanggung jawab tetap pada pemilik daftar.

**Apakah saya bisa memakai listmonk di laptop saja?** Untuk belajar, ya. Untuk newsletter sungguhan, tautan konfirmasi dan berhenti harus bisa dibuka penerima, jadi listmonk perlu server dengan HTTPS (panduan §2, §4) atau jasa setup Komunitech.

## Batasan yang jujur
**Pengaman ini melindungi dari kelalaian agent, bukan dari orang yang punya akses shell.** Gerbang uji-kirim, konfirmasi jumlah penerima, alamat uji, dan saringan sumber persetujuan mencegah agent salah kirim atau lupa menguji. Orang/agent dengan akses shell ke komputer Anda tetap bisa memalsukan berkas catatan lokal (`listmonk-uji.json`, alamat uji), memakai terminal palsu, atau memanggil API listmonk langsung. Catatan uji-kirim diberi tanda HMAC dengan kunci di folder konfigurasi Anda agar suntingan iseng terdeteksi, tetapi itu bukan pengaman terhadap penyerang. Tetap gunakan akun API berperan terbatas dan periksa ringkasan sebelum menjawab "ya".

Diuji pembuat pada listmonk 6.2.0 asli dengan SMTP penampung lokal. Belum diuji: pengiriman lewat Brevo/Amazon SES sungguhan, kotak masuk Gmail/Yahoo, Windows/macOS. Skill bukan nasihat hukum.
