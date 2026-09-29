# Contoh 6 (Uji Independen — Akun B) — Input Tidak Lengkap

**Input pengguna:**
> "mau jual kue"

## Simulasi respons yang benar menurut SKILL.md
Sesuai bagian **Input**: dua hal wajib belum ada sama sekali — (1) ide dalam satu kalimat yang lebih spesifik (jenis kue apa, target siapa) dan (2) harga rencana. Kanal yang dimiliki juga tidak disebut (tidak wajib, tapi menentukan metode uji). Instruksi eksplisit: *"Jika info wajib kurang, tanyakan sekali dalam satu pesan berisi daftar pertanyaan singkat bernomor."*

Respons agent yang sesuai (satu pesan, bukan berkali-kali tanya satu-satu):
> "Boleh, biar hasil tesnya tepat sasaran, tolong dijawab singkat ya:
> 1. Kue apa (mis. kue kering lebaran, cake ulang tahun, brownies)? Buat siapa kira-kira?
> 2. Rencana harga per unit/paket berapa (kasar tidak apa-apa)?
> 3. Kanal yang sudah kamu punya: kira-kira berapa kontak WA aktif, follower IG, atau pelanggan tetap?
> 4. Sudah pernah coba jual kue serupa sebelumnya?
> (Kalau mau cepat, aku bisa pakai asumsi wajar dan sebutkan asumsinya — tinggal bilang saja.)"

## Penilaian
- **Sesuai:** satu pesan, pertanyaan bernomor, singkat, dan menyertakan opsi "asumsi wajar" sesuai prinsip CLAUDE.md "instan tapi powerful" (kalau pengguna ingin cepat).
- **Konsisten batasan skill:** "jual kue" tidak menyentuh kategori terlarang (Kapan TIDAK Digunakan poin skema piramida/klaim medis/produk ilegal), jadi skill tetap lanjut memproses setelah info didapat — tidak ditolak.
- **Tidak melompat ke asumsi tanpa izin:** skill tidak langsung mengarang harga/kanal sendiri lalu jalan tanpa konfirmasi — ini penting karena "harga rencana" adalah input Wajib=Ya, beda dengan kolom Tidak Wajib lain yang punya default eksplisit di tabel Input.

## Kalau pengguna menjawab singkat sekadarnya
Skenario lanjutan: pengguna balas "kue kering lebaran, Rp150.000/toples, kontak WA 25 orang". Ini sudah cukup (info wajib lengkap: ide + harga; kanal disebut) → skill lanjut normal ke Langkah 1 (susun hipotesis) tanpa perlu tanya ulang. Diuji cocok dengan alur Contoh 1–5: begitu dua info wajib ada, skill tidak menahan proses lebih lama dari yang perlu.

## Catatan penguji
Alur "tanya sekali, satu pesan, bernomor, + opsi asumsi cepat" konsisten dipraktikkan di seluruh SKILL.md (bagian Input & prinsip CLAUDE.md Bagian 1). Tidak ditemukan celah pada skenario ini.
