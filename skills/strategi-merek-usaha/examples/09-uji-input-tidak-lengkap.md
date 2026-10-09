# Uji 09 (input tidak lengkap)

> Uji independen 2026-09-30.

**Input pengguna:** "bikinin nama brand dong sama promonya biar laku"

## Keluaran agent (mengikuti aturan tanya sekali, maks. 5 pertanyaan)
Siap bantu! Supaya namanya pas dan promonya tidak bikin rugi, jawab singkat ya (boleh sebagian):
1. Jual apa, dan di kota/daerah mana?
2. Pembelinya siapa (mis. ibu rumah tangga, mahasiswa, kantor)?
3. Gaya nama yang disuka: kalem, gaul, nuansa daerah, atau Inggris? Ada kata yang wajib/dihindari?
4. Merek pesaing yang kamu tahu (3-10 nama)?
5. Untuk promo: harga jual, modal per unit, dan potongan marketplace (%) bila jualan di Shopee/Tokopedia/TikTok Shop.

Kalau mau cepat, balas "langsung aja" — saya kerjakan dengan asumsi (nama ramah 2-3 suku kata berbahasa Indonesia; kemiripan merek ditandai "belum diperiksa"; promo berupa rancangan tanpa hitungan, ditandai **belum dihitung**) dan asumsinya saya tulis.

## Lanjutan: pengguna membalas "langsung aja, jualan keripik pisang di Lampung, Shopee"
Agent menjalankan versi cepat: 10 nama ber-skor (kolom kemiripan = 3 "belum diperiksa" karena tidak ada daftar merek), penawaran berupa rancangan 6 komponen dengan `[isi: harga]`, `[isi: modal]`, `[isi: potongan Shopee %]` dan label **"belum dihitung"**; tidak menebak persentase potongan Shopee.

Cek script tanpa merek (penguji): `skor_nama.py` mencetak "kemiripan belum diperiksa (tidak ada daftar merek)" untuk setiap nama, sesuai SKILL.md.

## Penilaian penguji
- Lulus: satu pesan, 5 pertanyaan, opsi "langsung aja" dengan asumsi eksplisit; tidak mengarang angka atau potongan marketplace.
