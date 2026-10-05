# Uji 04 — Input tidak lengkap: "bikinin rencana marketing"

> Uji simulasi oleh agent penguji independen, 2026-09-29.

**Permintaan pengguna:** "bikinin rencana marketing"

**Perilaku yang diharapkan (SKILL.md, Aturan tanya):** info wajib (usaha & produk, harga & HPP, periode, tujuan, anggaran) belum ada -> tanya **sekali**, satu pesan, daftar bernomor pendek; tawarkan jalur cepat dengan default. Tidak mengarang HPP.

## Keluaran agent

Siap, saya bantu susun rencana marketing yang langsung bisa dijalankan. Supaya angkanya tepat, mohon jawab singkat (boleh sebagian):

1. **Usahanya apa & produk/jasa andalannya?** (mis. "kedai kopi di Bandung, es kopi susu")
2. **Harga jual dan modal (HPP) per produk/porsi?** (mis. "jual 25 rb, modal 9 rb"). Belum tahu modalnya? Saya bisa bantu hitung dulu dengan `hitung-hpp`.
3. **Jualan di mana saja?** (toko fisik, WhatsApp, Instagram, TikTok Shop, Shopee/Tokopedia, GoFood/GrabFood) — kalau di marketplace/aplikasi, berapa kira-kira potongannya (%)?
4. **Untuk berapa lama?** (3 bulan / setahun) — kalau tidak diisi saya pakai Oktober-Desember 2026.
5. **Tujuan utamanya apa?** (tambah omzet, tambah pesanan, pelanggan baru, ramai di jam sepi) — sebut angkanya kalau ada.
6. **Budget marketing total berapa?** Kalau belum tahu, saya pakai 5-10% dari target omzet dan tetap buat versi tanpa iklan (Rp 0).
7. **Kondisi sekarang & tenaga:** omzet/bulan kira-kira, sudah ada pelanggan tetap?, yang mengerjakan siapa dan berapa jam per minggu?

Kalau ingin cepat, jawab 1, 2, dan 6 saja — sisanya saya isi dengan asumsi yang saya tulis jelas di bagian atas rencana.

## Penilaian penguji
| Kriteria | Hasil |
|---|---|
| Satu pesan, daftar bernomor | ✔ |
| Tidak mengarang angka / HPP | ✔ (menawarkan `hitung-hpp`) |
| Default disebut (periode, 5-10% budget, skenario Rp 0) | ✔ sesuai tabel Input |
| Jalur cepat | ✔ |
| Bahasa awam | ✔ |
Catatan: 7 pertanyaan agak panjang untuk pengguna awam, tetapi tiap butir pendek dan ada opsi "jawab 1, 2, 6 saja". Lulus.
