# 04 — Input tidak lengkap: keripik pisang

> Uji independen Tahap 6 (2026-09-29). Penguji: agent terpisah dari pembuat. Output agent dihasilkan oleh sesi `claude -p` baru (Claude Code, simulasi agent) dengan skill terpasang di folder sementara `.claude/skills/` (tanpa folder `examples/`). Nama usaha fiktif.

## Input pengguna

> Harga keripik pisang aku enaknya berapa ya? Mau mulai jual online juga.

## Output agent (dengan skill, apa adanya)

Supaya angkanya pas dan bukan tebakan, aku butuh beberapa data dulu. Jawab singkat saja, perkiraan juga boleh.

1. **Ukuran dan isi kemasan**: berapa gram per bungkus, dan rasanya apa saja (original, balado, cokelat, dll.)?
2. **Modal (HPP) per bungkus**: pisang, minyak, bumbu, kemasan, dan upah kalau ada yang dibayar per produksi. Kalau belum pernah dihitung, sebut perkiraannya, nanti kutandai "HPP perkiraan".
3. **Harga sekarang** (kalau sudah jual offline), dan **harga 3–5 keripik pisang sejenis** di toko online yang bisa kamu lihat: terendah, tengah, dan tertinggi.
4. **Jual online lewat mana?** Shopee, Tokopedia, TikTok Shop, atau WhatsApp/Instagram? Tiap kanal punya potongan berbeda. Kalau sudah tahu potongannya, sebutkan.
5. **Tujuan utamanya**: cepat dapat pembeli, untung maksimal, atau juga mau punya reseller?

Dengan data itu aku bisa hitung:
- harga minimum supaya tidak rugi, setelah dipotong biaya marketplace;
- harga eceran yang pas, dan harga cantik seperti Rp 19.900;
- harga reseller atau paket hemat, kalau kamu mau;
- batas diskon yang masih aman untuk promo.

Kalau mau cepat, kirim saja HPP dan ukuran bungkusnya. Sisanya kupakai asumsi standar: margin minimal 40% untuk makanan, jual langsung tanpa potongan, dan non-PKP.

## Verifikasi penguji

- Tanya **sekali** dalam satu pesan, tepat **5 pertanyaan** (ukuran, HPP, harga pesaing, kanal, tujuan) ✔ sesuai SKILL.md.
- Tidak mengarang angka ✔. Menawarkan jalur cepat dengan default yang disebutkan (margin 40% makanan, 0% potongan, non-PKP) ✔. Merujuk tanda "HPP perkiraan" ✔.
- Kekurangan kecil: tidak menyebut skill **hitung-hpp** / **harga-jual-marketplace** secara nama (hanya "potongan berbeda").

**Nilai: 9/10.**
