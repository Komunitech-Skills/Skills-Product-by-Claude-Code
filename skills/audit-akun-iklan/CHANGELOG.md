# Riwayat perubahan — audit-akun-iklan

Catatan teknis per versi (dipindah dari README agar halaman pembeli ringkas).

## Catatan revisi 1.0.8 (2026-10-26)
- Memperbaiki tiga temuan uji coba di konteks Telegram (21 Okt 2026, versi 1.0.7, nilai 6,5): (1) verdik kini selalu satu label (BONCOS / RAWAN BONCOS / TIPIS / SEHAT). Bila ROAS aktual belum Anda sebut, AI memberi label sementara dari ROAS impas dan cerita Anda (impas 2,5 atau lebih dan Anda merasa rugi = RAWAN BONCOS sementara; selain itu TIPIS sementara; SEHAT tidak pernah tanpa ROAS aktual) plus satu kalimat tentang angka yang memastikan. Tidak ada lagi "belum bisa dipastikan". Bila ada beberapa jalur, label terburuk yang dipakai. (2) Tiga tindakan hari ini harus langsung mengurangi rugi (bila ROAS aktual per jalur sudah ada: kurangi/jeda dulu jalur yang RUGI; bila belum ada: kurangi jalur dengan impas tertinggi; jalur lain baru ditambah setelah ROAS 7 harinya terbukti di atas impasnya; target ROAS minimal sama dengan impas, cek komisi afiliasi atau jeda iklan terburuk), lengkap dengan angka; cek keamanan dan iklan ditolak pindah ke satu baris "Juga cek". (3) Kalimat "File kerja: ..." dan kata proses (file, berkas, script, skrip, path, folder, tool) dilarang di balasan chat; satu-satunya pengecualian menawarkan "balas kirim file".
- Perbaikan lanjutan setelah pemeriksaan independen (masih 1.0.8, belum dirilis): contoh pertama di SKILL.md (toko gamis) kini memakai verdik TIPIS (sementara) dan tindakan yang menekan rugi, bukan pengaman cepat; saat harga/modal belum ada, tindakan memakai rumus impas dan angka yang sudah ada, tanpa angka karangan; ditambah daftar periksa sebelum kirim; kata "file" saat minta bukti diganti "ekspor CSV" / "unduhan laporan"; catatan v1.0.8 ditambahkan di contoh 04.
- Pemeriksaan kedua: aturan tindakan (a) dibedakan menurut ada/tidaknya ROAS aktual (jalur RUGI dikurangi lebih dulu), tidak lagi menyuruh menambah anggaran jalur yang ROAS aktualnya belum terbukti, ambang impas 2,5 membandingkan angka persis sebelum pembulatan, dan cek komisi afiliasi hanya bila afiliasi disebut pemilik.
- Angka dan pembulatan identik dengan 1.0.7; skrip hanya berganti penanda versi. Tes regresi aturan baru ditambahkan. Belum diuji ulang di bot Telegram asli.

## Catatan revisi 1.0.7 (2026-10-16)
- Prinsip "jawab dulu, tanya kemudian": bila Anda hanya menulis sebagian data (mis. beberapa angka dan "rasanya boncos"), AI kini langsung memberi audit pendahuluan di balasan pertama: titik impas per jalur iklan (ROAS/ROI impas, laba per pesanan, pesanan impas per bulan), verdik boncos/tipis/sehat dengan asumsi yang ditandai, tiga tindakan yang bisa dilakukan hari itu, dan skor kesehatan sementara.
- Pertanyaan lanjutan pindah ke akhir balasan dan dibatasi maksimal 5 (sebelumnya sampai 8 pertanyaan di awal, sebelum ada hasil).
- Skor tetap dari skrip: bukti 30-59% disebut "perkiraan awal", di bawah 30% angka skor tidak disebut karena menyesatkan; skor penuh dan rencana 7 hari menunggu jawaban Anda. Rumus dan logika hitung skrip tidak berubah (hanya penanda versi).

## Catatan revisi 1.0.6 (2026-10-13)
- Rujukan ke skill arsip diganti: `caption-sosmed-umkm` diganti `konten-mingguan` (SKILL.md, bagian Kapan TIDAK digunakan); konstanta VERSI skrip disamakan.

## Catatan revisi 1.0.5 (2026-10-01)
- Keamanan: bila Anda tidak sengaja menempel password/OTP/token di chat, AI tidak akan mengulang, menyimpan, atau memakainya — Anda akan diminta segera mengganti password dan mengaktifkan verifikasi 2 langkah, lalu audit lanjut dari ekspor data/screenshot saja.
- Script kini otomatis menyamarkan pola password/OTP/token/nomor kartu di catatan audit menjadi `[DISAMARKAN]`.

## Catatan revisi 1.0.4 (2026-10-01)
- Setiap ROAS yang Anda sebut (target maupun rata-rata) kini selalu dibandingkan dengan ROAS impas oleh script dan dinyatakan **RUGI / IMPAS / UNTUNG** beserta perkiraan rugi/laba per pesanan.
- Iklan klinik & fasilitas kesehatan: saran mengikuti Permenkes 1787/2010 (tanpa testimoni pasien, tanpa promo diskon, tanpa janji hasil).
- Lokasi file kerja yang dibuat selalu disebutkan.
