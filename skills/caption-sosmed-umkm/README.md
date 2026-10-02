# Caption Jualan Siap Posting dalam Detik

**Ketik nama produkmu, dapat 3 caption jualan yang siap posting.**

## Manfaat
- ✅ 3 gaya sekaligus: storytelling, langsung jualan, dan santai
- ✅ Otomatis disesuaikan untuk Instagram, TikTok, Facebook, atau WA Status
- ✅ Selalu ada hook di awal dan ajakan beli (CTA) yang jelas
- ✅ Hashtag campuran umum, niche, dan lokal
- ✅ Aman: tidak mengarang klaim seperti "halal", "BPOM", "tanpa pengawet", atau "stok terbatas" yang tidak kamu sebutkan, dan menolak klaim kesehatan untuk jamu/makanan/kosmetik

## Cocok untuk siapa
- Pemilik UMKM dan online shop yang posting setiap hari
- Admin media sosial yang kehabisan ide caption

## Contoh sebelum & sesudah
**Sebelum:** 30 menit memikirkan caption untuk satu foto produk.

**Sesudah (cukup ketik):** "Buatin caption IG buat nastar keju, 1 toples Rp85rb, order via WA"
→ 3 variasi caption lengkap dengan hashtag dan tips jam posting.

## Instalasi singkat
Salin folder `caption-sosmed-umkm` ke folder skills AI agent kamu. Panduan lengkap per platform ada di `CARA-INSTAL.md` di dalam paket.

## FAQ
**Apakah harus pakai bahasa formal?**
Tidak. Minta saja "lebih santai" atau "lebih formal", nanti caption-nya direvisi.

**Bisa untuk jasa, bukan produk?**
Bisa. Ceritakan jasamu seperti menceritakan produk.

**Apakah hasilnya selalu sama?**
Tidak. Setiap kali diminta, hasilnya variasi baru.

## Catatan revisi 1.1.2 (2026-10-01)
- Format per platform dipertegas: Instagram wajib 80-150 kata (tanpa hashtag) dan 3-8 hashtag di SETIAP variasi; paragraf maks. 2-3 kalimat.
- Klaim kesehatan (meredakan, mengatasi, "pas asam lambung naik", detox, pengganti obat, dst.) dilarang untuk pangan/jamu/kosmetik sesuai aturan iklan BPOM, termasuk bentuk halusnya; diganti alternatif aman (rasa, aroma, tradisi, cara menikmati).
- Fakta produk hanya dari kamu: bahan, "tanpa pengawet", stok, antar/ongkir, dan testimoni karangan tidak ditambahkan; yang kurang ditulis [isi: ...].
- Script baru `scripts/cek_caption.py` (+ `cek_fakta.py`, tes `uji_regresi.py`, Python standar) menghitung kata & hashtag dan menandai klaim karangan/kesehatan sebelum caption dikirim ke kamu.
