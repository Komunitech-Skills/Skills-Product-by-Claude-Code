# Skenario 1 (normal utama)

**Input (pesan pengguna):** "Tolong pantau laporan harian jam 21.00 dan tagih piutang 07.45 Senin-Jumat di OpenClaw saya, kabari lewat Telegram kalau ada yang gagal jalan."

**Output SESUDAH (skill aktif):**

> Saya sudah mulai memasang pemantauannya, tapi berhenti sejenak di satu langkah yang perlu dibereskan dulu — sesuai aturan kerja skill ini (tidak boleh coba-coba berulang kalau kanalnya belum siap).
>
> **Sudah selesai (aman, tanpa perlu persetujuan):**
> Dua jadwal sudah terdaftar untuk dipantau:
>
> | Nama | Jadwal | Zona | Toleransi | Jadwal berikutnya |
> |---|---|---|---|---|
> | Laporan harian | tiap hari 21.00 | WIB | 30 menit | 12 Okt 21.00 |
> | Tagih piutang pagi | Senin–Jumat 07.45 | WIB | 30 menit | 13 Okt 07.45 |
>
> **Yang masih memblokir pemasangan "pengawas" (bagian yang akan mengabari Telegram):**
> 1. **Telegram belum terhubung** di OpenClaw ini — statusnya baru "terpasang, belum dikonfigurasi". Belum ada tujuan untuk mengirim kabar gagal.
> 2. **Akses ke jadwal otomatis (automations) Gateway juga belum bisa dipakai** dari sisi saya — sistemnya minta token masuk (gateway.auth) yang belum diset, dan saya tidak bisa membetulkannya sendiri karena Gateway yang sedang jalan masih memegang kuncinya (perlu operator yang me-restart Gateway dari luar, bukan sesuatu yang boleh saya lakukan lewat perintah otomatis).
>
> **Yang perlu dilakukan (oleh Anda/pemilik Gateway) agar saya bisa lanjut:**
> 1. Hubungkan Telegram di OpenClaw (lewat Control UI/dashboard → Connect Channel → Telegram, masukkan token bot dari BotFather).
> 2. Setel token masuk Gateway (`gateway.auth`) lalu restart Gateway — ini langkah admin yang perlu dilakukan dari terminal/dashboard asli Gateway, bukan dari sesi chat saya.
>
> Begitu dua hal itu beres, beri tahu saya — saya langsung lanjutkan: ubah dua jadwal itu agar "lapor selesai" otomatis, pasang pengawas tiap jam + ringkasan harian, lalu uji kirim satu peringatan percobaan ke Telegram Anda sebelum dianggap aktif.

**Output SESUDAH, konteks Telegram:**

> Saya sudah mulai memasang pemantauan, tapi ketemu satu kendala teknis di Gateway yang perlu tindakan Anda. Berikut rangkumannya:
>
> **Sudah dikerjakan (tidak perlu konfirmasi, aman):**
> Dua jadwal sudah terdaftar di sistem pemantauan lokal:
>
> | Nama | Jadwal | Toleransi |
> |---|---|---|
> | laporan-harian | tiap hari 21.00 WIB | 30 menit |
> | piutang-pagi | Senin–Jumat 07.45 WIB | 30 menit |
>
> **Terblokir — butuh tindakan Anda:**
> Untuk menambahkan "ping" di akhir jadwal asli dan membuat 2 job pengawas (cek tiap jam + ringkasan 08.00, kirim ke Telegram), saya perlu akses ke fitur jadwal (automations) OpenClaw. Saat ini akses itu gagal dengan pesan "token mismatch" — Gateway OpenClaw Anda baru saja diberi token otorisasi baru, tapi prosesnya belum dimuat ulang (restart), dan Gateway ini berjalan manual (bukan lewat systemd/pm2), jadi saya tidak diizinkan me-restart-nya sendiri lewat sesi chat demi keamanan.
>
> **Yang saya butuhkan dari Anda:**
> 1. Restart proses Gateway OpenClaw secara manual di komputer/server tempat ia berjalan (hentikan proses yang sedang jalan, lalu jalankan ulang perintah start seperti biasa — kalau pakai service manager seperti systemd/pm2, tinggal `restart` lewat itu).
> 2. Setelah restart, beri tahu saya "sudah" — saya akan langsung lanjutkan: cek jadwal laporan & piutang yang sudah ada, tambahkan baris lapor-selesai di akhirnya, buat 2 jadwal pengawas, lalu uji satu peringatan palsu terkendali ke Telegram sebelum dianggap aktif (akan saya tunjukkan rencananya dulu, minta persetujuan Anda sebelum benar-benar dipasang).
>
> Kalau Anda tidak punya akses langsung ke server itu (misalnya ini dikelola pihak lain), beri tahu saya dan saya bantu cari jalan lain.

**Catatan penguji:** Di mesin uji ini tidak ada Gateway OpenClaw yang bisa dipakai (perintah automations ditolak: kredensial/token), jadi pemasangan jadwal TIDAK mungkin selesai di kedua sisi; yang dinilai adalah cara masing-masing menangani hal itu. SEBELUM: salah mengira permintaan ini hanya pengingat dan bertanya balik soal 'sumber data', mengutak-atik token Gateway sendiri (menulis gateway.auth ke konfigurasi), tanpa hasil yang bisa dipakai. SESUDAH: skill terpicu, dua job langsung didaftarkan ke pantauan lokal lewat skrip (tabel nama/jadwal/toleransi/jadwal berikutnya benar: 12 Okt 21.00 dan 13 Okt 07.45), lalu berhenti dengan penjelasan blokir dan apa yang akan dikerjakan setelahnya. Kurang: tidak menampilkan rencana (kalimat ping di akhir prompt, jadwal pengawas, tombol 'ya') walau blokir; bocor jargon ('Gateway', 'gateway.auth', 'BotFather'); agent sempat membaca openclaw.json, mengecek env token, dan menjalankan 'doctor --fix' di jalur diagnosa sendiri padahal aturan kerja skill melarang membaca konfigurasi/token (pelanggaran aturan sendiri). Skor SESUDAH tertahan oleh itu.

**Skor:** sebelum 3, sesudah 5,5. Perbandingan lengkap: `00-openclaw-sebelum-sesudah.md`.
