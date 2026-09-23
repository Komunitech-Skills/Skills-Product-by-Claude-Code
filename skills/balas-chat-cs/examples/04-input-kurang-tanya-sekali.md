# 04 — Input tidak lengkap (tanya sekali)

**Skenario:** S4 — pengguna minta dibalaskan tetapi tidak menempel chat dan tidak memberi info toko.

**Input pengguna:**
> tolong balasin customer saya dong, dia nanya soal barang yg kemarin

## Output

Siap, saya bantu balas. Saya perlu beberapa info dulu ya:

1. **Tempel isi chat pelanggannya** (atau kirim tangkapan layarnya).
2. **Chat-nya di mana?** WhatsApp atau marketplace (Shopee/Tokopedia/TikTok Shop/lainnya)?
3. **Nama toko & produk** yang dimaksud.
4. Kalau pelanggan komplain: **solusi apa yang boleh ditawarkan** (tukar, refund, kirim ulang, belum tahu)?
5. **Nada** yang biasa dipakai: santai-akrab, ramah-sopan (default), atau formal?

Cukup kirim nomor 1 dan 3 kalau mau cepat — sisanya saya pakai default (WhatsApp, ramah-sopan, sapaan "Kak") dan bagian yang belum pasti saya tandai `[isi ...]`.

## Catatan penguji
- Sesuai SKILL.md: tanya sekali, maks. 5 pertanyaan, default disebut.
- Tidak menebak isi chat atau mengarang jawaban.
