# Riwayat perubahan — audit-akun-iklan

Catatan teknis per versi (dipindah dari README agar halaman pembeli ringkas).

## Catatan revisi 1.0.5 (2026-10-01)
- Keamanan: bila Anda tidak sengaja menempel password/OTP/token di chat, AI tidak akan mengulang, menyimpan, atau memakainya — Anda akan diminta segera mengganti password dan mengaktifkan verifikasi 2 langkah, lalu audit lanjut dari ekspor data/screenshot saja.
- Script kini otomatis menyamarkan pola password/OTP/token/nomor kartu di catatan audit menjadi `[DISAMARKAN]`.

## Catatan revisi 1.0.4 (2026-10-01)
- Setiap ROAS yang Anda sebut (target maupun rata-rata) kini selalu dibandingkan dengan ROAS impas oleh script dan dinyatakan **RUGI / IMPAS / UNTUNG** beserta perkiraan rugi/laba per pesanan.
- Iklan klinik & fasilitas kesehatan: saran mengikuti Permenkes 1787/2010 (tanpa testimoni pasien, tanpa promo diskon, tanpa janji hasil).
- Lokasi file kerja yang dibuat selalu disebutkan.
