# Contoh 04 - Input tidak lengkap
Pengguna: "Tolong rapikan masukan pelanggan saya."
Agent (satu pesan): "Siap! Supaya pas, mohon kirim: (1) masukan dari kanal mana saja (chat WA usaha, ulasan Shopee/Tokopedia/Google Maps, komentar IG/TikTok, survei) - boleh ekspor file atau salin-tempel, satu masukan per baris; (2) periode datanya; (3) jenis usaha. Kalau mau cepat, kirim apa yang ada dulu, nanti kita mulai dari situ dan pakai asumsi yang saya sebutkan."
Bila pengguna hanya menempel 6 komentar: agent membaca langsung, memberi 3 temuan + 2 tindakan, dan menyebut "data < 8, tanpa statistik".
Bila file rusak (kosong): script keluar dengan pesan "GAGAL: tidak ada masukan yang bisa dibaca (berkas kosong atau semua baris terlalu pendek)…" (kode 2); agent meminta ekspor ulang, tidak mengarang. *(Pesan & kode keluar dicek ulang dengan v1.0.12 pada 2026-10-16.)*
