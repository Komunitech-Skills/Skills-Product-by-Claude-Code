# Riwayat perubahan — audit-akun-iklan

Catatan teknis per versi (dipindah dari README agar halaman pembeli ringkas).

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
