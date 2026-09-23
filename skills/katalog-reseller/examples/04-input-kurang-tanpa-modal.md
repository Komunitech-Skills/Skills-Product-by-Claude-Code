# 04 — Mau buka reseller tapi belum menyebut produk & modal (S4, input tidak lengkap)

## Input pengguna
> aku mau buka reseller nih buat produk aku, bikinin price list sama syaratnya ya

## Output
Siap, aku bantu susun program resellernya. Supaya harga tiap tier tidak bikin kamu atau resellermu rugi, aku perlu 5 hal ini:

1. **Produk apa** (boleh lebih dari satu), dan **modal/HPP per unit**, sudah termasuk kemasan & label. Kalau belum tahu modalnya, bisa dihitung dulu dengan skill `hitung-hpp`.
2. **Harga eceran** ke konsumen sekarang, kalau sudah ada. Kalau belum, aku usulkan dari modal.
3. **Tier yang kamu mau**: misalnya Dropshipper (1 pcs), Reseller (min. 12 pcs), Agen (min. 60 pcs), dan berapa diskon atau untung yang kamu inginkan. Kalau belum kebayang, aku pakai contoh dulu.
4. **Resellermu nanti jualan di mana?** Kalau di Shopee/Tokopedia/TikTok, kira-kira berapa persen potongannya? Ini penting, karena potongan marketplace sering membuat untung reseller jauh lebih kecil dari perkiraan.
5. **Boleh kasih diskon ke konsumen maksimal berapa persen?** Nanti jadi "harga minimum anjuran", supaya tidak ada yang banting harga.

Kalau mau cepat, cukup jawab nomor 1 dan 2. Sisanya aku isi dengan default dan aku sebutkan asumsinya.

Hasilnya: tabel harga internal (dengan margin kamu), daftar harga siap kirim ke reseller (tanpa modal), syarat & ketentuan kemitraan, dan pesan ajakan WA/IG yang jujur.

## Catatan penguji
- Sesuai SKILL.md: satu kali bertanya, maks. 5 pertanyaan bernomor, jalur cepat, tidak mengarang HPP. Pertanyaan no. 4 menunjukkan nilai khas skill (biaya jual mitra).
- Script dicek dengan input kosong: tanpa `--hpp` → `ERROR: isi --hpp …` kode 2; HPP 0 → `ERROR: HPP harus lebih dari 0`; mode diskon tanpa eceran → `ERROR` jelas ✓.
