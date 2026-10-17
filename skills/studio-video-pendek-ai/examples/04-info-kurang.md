# Skenario 4 (input tidak lengkap)
Input: "bikinin video promo dong"
Perilaku yang diharapkan SKILL: tanya SEKALI, maks. 5 pertanyaan, dalam satu pesan; bila pengguna ingin cepat, pakai default + asumsi.
Respons agen (simulasi):
"Supaya videonya pas, jawab singkat ya: 1) Apa produk/jasanya? 2) Harga & promo persisnya? 3) Durasi (15/30/45/60 dtk; default 30)? 4) Rekam HP atau pakai alat video AI? 5) Jualan lewat mana (WA/marketplace)? Kalau mau cepat, ketik 'lanjut' dan saya pakai default: 30 dtk, jualan, rekam HP, santai."
Uji lanjutan: pengguna balas "lanjut". Kendala ditemukan: tanpa produk sama sekali, default tidak bisa memberi naskah spesifik; agen harus memakai placeholder [produk]/[harga] dan menyatakan bahwa angka tidak ditebak (SKILL: "Angka hanya dari pengguna"). SKILL tidak menuliskan eksplisit apa yang dilakukan bila TIDAK ada produk sama sekali (default hanya untuk durasi/platform/gaya). Temuan Rendah.
Hasil: PASS dengan catatan.

## Penyegaran v1.0.5 (2026-10-17)
Keluaran dan hasil uji di atas (PASS dengan catatan) **tidak diubah** dan tetap sesuai v1.0.5: tanya sekali, maks. 5 pertanyaan; bila pengguna menjawab "lanjut" tanpa produk, pakai `[NAMA PRODUK]`/`[HARGA]`/`[isi: ...]` sesuai Aturan Fakta (tidak menebak). Tambahan v1.0.5 bila naskah dibuat dengan default: hook ≤ 3 dtk, teks layar CTA `[nomor WA]`, dan shot list rekam HP langsung di hasil pertama (default = rekam HP).
