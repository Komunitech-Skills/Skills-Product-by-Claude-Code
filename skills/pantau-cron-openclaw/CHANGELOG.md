# Riwayat perubahan — pantau-cron-openclaw

Catatan teknis per versi.

## Catatan revisi 1.0.3 (2026-10-13)
- Pembersihan kata teknis di jawaban untuk pengguna awam: nama perintah/CLI ikut dilarang muncul, kata "Gateway" diganti "OpenClaw", dan setelah memasang, jadwal dan cara menjeda ditampilkan dalam kalimat biasa ("minta saya menjeda jadwal ini"); perintah teknis hanya bila pengguna memintanya. Logika dan script tidak berubah.

## Catatan revisi 1.0.2 (2026-10-12)
- Revisi dari uji OpenClaw asli (skor 4,63 naik ke 8,19): deskripsi diganti dengan kata pemicu yang lebih mudah dikenali ("jadwal otomatis gagal", "laporan otomatis mati", "kabari kalau laporan saya gagal").
- Ditambah bagian "PENOLAKAN": permintaan memantau komputer, akun, atau aktivitas karyawan/pasangan/orang lain diam-diam ditolak dengan kalimat pertama baku, lalu langsung dilanjutkan dengan rencana contoh untuk jadwal milik sendiri.
- Ditambah "BAHASA KE PENGGUNA" (daftar kata yang dilarang muncul, mis. cron, ping, token, Gateway; diganti "jadwal otomatis" dan "lapor selesai") dan "PENUTUP BAKU" (satu kalimat jujur bahwa pemasangan penuh belum teruji otomatis, "Lanjut? (ya/tidak)", dan tepat tiga pertanyaan). Alamat folder ditulis sebagai `[isian: ...]`.

## Catatan revisi 1.0.1 (2026-10-12)
- Revisi setelah uji pertama (skor 5,25 naik ke 6,75; script terbukti benar pada 800 kasus acak, tetapi perilaku agent saat OpenClaw tidak bisa dihubungi perlu dibenahi): ditambah "ATURAN BERHENTI" (bila perintah `openclaw automations/cron` gagal sekali, agent berhenti memakainya, tidak membaca atau mengubah konfigurasi, tidak memeriksa atau membuat token, tidak menjalankan `openclaw doctor` atau me-restart).
- "Mode terblokir": pekerjaan lokal tetap jalan, lalu agent menampilkan rencana lengkap siap salin dalam satu pesan (tabel job, kalimat "lapor selesai", perintah pengawas) dan satu kalimat awam apa yang perlu dibereskan pengguna. Prinsip "kerjakan dulu, tanya di akhir" (maksimal 3 pertanyaan), blok hasil BERMASALAH/OK, dan penolakan baku ditambahkan; deskripsi disesuaikan.

## Catatan revisi 1.0.0 (2026-10-12)
- Rilis awal (uji internal): memantau jadwal/laporan otomatis OpenClaw milik sendiri agar kegagalan tidak diam-diam: mendaftarkan tiap job (jadwal, toleransi, WIB/WITA/WIT), menambah baris "lapor selesai" di akhir job, dan satu pengawas yang mengabari Telegram hanya bila ada yang terlambat atau hilang. Perhitungan status oleh script `pantau_cron.py`.
