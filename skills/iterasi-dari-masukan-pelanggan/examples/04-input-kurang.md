# Contoh 04 - Input tidak lengkap
Pengguna: "Tolong rapikan masukan pelanggan saya."
Agent (satu pesan): "Siap! Supaya pas, mohon kirim: (1) masukan dari kanal mana saja (chat WA usaha, ulasan Shopee/Tokopedia/Google Maps, komentar IG/TikTok, survei) - boleh ekspor file atau salin-tempel, satu masukan per baris; (2) periode datanya; (3) jenis usaha. Kalau mau cepat, kirim apa yang ada dulu, nanti kita mulai dari situ dan pakai asumsi yang saya sebutkan."
Bila pengguna hanya menempel 6 komentar: agent membaca langsung, memberi 3 temuan + 2 tindakan, dan menyebut "data < 8, tanpa statistik".
Bila file rusak (kosong): script keluar dengan pesan "Tidak ada masukan yang bisa dibaca" (kode 2); agent meminta ekspor ulang, tidak mengarang.
