# Checklist Anti-Spam / Anti-Blokir WhatsApp

Untuk pesan PERTAMA ke nomor yang belum pernah chat dengan kita. Tujuannya: dibalas, bukan dilaporkan/diblokir.

## Sebelum kirim
- [ ] Nomor didapat dari sumber yang sah & bisa dijelaskan (lihat `dasar-hukum-wa.md`) — bukan beli database/bocoran/scraping login.
- [ ] Pesan **menyebut asal kontak** secara eksplisit (lihat `pola-pembuka.md`).
- [ ] Pesan **punya opsi keluar yang sopan** ("boleh diabaikan bila tidak relevan", "maaf mengganggu bila...").
- [ ] Foto profil & nama akun WA pengirim jelas mewakili usaha/diri sendiri (bukan foto kosong/nomor tanpa identitas — nomor "misterius" jauh lebih sering dicurigai & dilaporkan).
- [ ] Isi pesan sudah dijalankan lewat `scripts/cek_pesan.py cek` dan peringatannya sudah ditinjau.

## Isi pesan
- [ ] Maksimal 1 link (idealnya tanpa link di pesan pertama — link asing dari nomor tak dikenal sering dicurigai phishing).
- [ ] Tidak ada huruf kapital berlebihan ("PROMO GILA", "GRATIS!!!").
- [ ] Tidak ada klaim "gratis 100%", "dijamin", urgensi palsu ("stok terakhir", "harga naik besok") kecuali benar dan diberikan pengguna.
- [ ] Emoji secukupnya: idealnya 0–1, maksimal 3 (script memberi peringatan bila lebih dari 3); emoji berlebihan + kapital = pola khas spam.
- [ ] Panjang wajar untuk satu layar HP (lihat batas di `scripts/cek_pesan.py`) — pesan yang terlalu panjang di kontak pertama sering tidak dibaca sampai habis.

## Jam & pola kirim
- [ ] Kirim jam 08.00–20.00 waktu **setempat penerima** (WIB/WITA/WIT — cek dulu lokasi prospek, jangan asumsikan WIB untuk semua Indonesia).
- [ ] Hindari kirim beruntun ke banyak nomor asing dalam waktu sangat singkat dari nomor pribadi (bukan WhatsApp Business API resmi) — pola ini yang paling sering memicu pemblokiran otomatis WhatsApp. Beri jeda wajar antar-kontak (skill ini untuk kontak satu per satu oleh manusia, bukan pengiriman otomatis/massal — kalau butuh kirim ke banyak kontak, itu ranah `broadcast-wa` dengan aturan persetujuan tersendiri).
- [ ] Satu prospek = satu pesan pembuka. Jangan kirim ulang/variasi lain ke nomor yang sama dalam waktu berdekatan hanya karena belum dibalas (itu ranah `follow-up-prospek`, dengan jeda hari yang terjadwal).

## Jika prospek membalas negatif
- [ ] Jika diminta berhenti/tidak nyaman: ucapkan terima kasih singkat, hormati, jangan hubungi lagi lewat saluran apa pun.
- [ ] Jangan berdebat atau meyakinkan ulang setelah penolakan jelas.
- [ ] Jika dilaporkan sebagai spam (chat menghilang/terblokir), jangan buat nomor/akun baru untuk mengulang pola yang sama — evaluasi dulu sumber kontak & isi pesannya.

## Setelah kirim
- [ ] Catat hasilnya (dibalas/tidak, tertarik/tidak) untuk keperluan lanjutan — kalau butuh menindaklanjuti prospek yang diam, lanjut ke skill `follow-up-prospek`.
