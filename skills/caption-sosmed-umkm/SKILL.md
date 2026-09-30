---
name: caption-sosmed-umkm
description: Membuat caption media sosial (Instagram, TikTok, Facebook, WhatsApp Status) berbahasa Indonesia untuk produk UMKM, lengkap dengan hook, CTA, dan hashtag. Gunakan saat pengguna minta caption, copywriting, teks promosi, atau konten jualan untuk diposting di media sosial (social media caption, product post, promo copy). Bukan untuk membalas ulasan pelanggan atau menulis judul/deskripsi listing marketplace.
---

# Caption Sosmed UMKM

> **Aturan kerja:** Jangan menginstal paket/aplikasi (mis. `pip install`) — bila perlu, tunjukkan caranya dan biarkan pengguna yang memasang; jangan membuka atau mencari file selain yang diberikan pengguna, isi folder skill ini, dan file yang disebut di langkah kerja; jangan menulis file baru tanpa menyebut lokasinya, dan simpan hasil di folder kerja yang disepakati (bukan /tmp).

Menghasilkan caption jualan yang terasa lokal, tidak kaku, dan mendorong pembeli bertindak.

## Kapan TIDAK digunakan
- Membalas ulasan/komentar pelanggan → pakai skill `balas-ulasan-pelanggan`.
- Judul & deskripsi produk untuk Shopee/Tokopedia/TikTok Shop → pakai skill `listing-marketplace`.
- Pesan broadcast WhatsApp ke daftar kontak → pakai skill `broadcast-wa`.
- Produk ilegal, obat/suplemen dengan klaim menyembuhkan, rokok elektrik, judi, investasi bodong → tolak dengan sopan.

## Alur kerja

1. **Kumpulkan info minimum.** Jika belum ada, tanyakan sekaligus dalam satu pesan:
   - Produk & keunggulan utama
   - Platform (IG / TikTok / FB / WA Status)
   - Target pembeli (contoh: ibu muda, mahasiswa, pekerja kantoran)
   - Promo/harga (opsional)
   - Cara order (DM, link bio, WA, Shopee, dll.)

   **Kapan harus bertanya:** jika produknya belum jelas, atau platform WA Status tanpa harga/cara order.
   Selain itu, **langsung kerjakan**: pakai asumsi wajar (default platform: Instagram), tulis placeholder
   seperti `[harga]` atau `[nomor WA]` untuk info yang belum ada, dan sebutkan asumsinya di akhir.
2. **Tulis 3 variasi** dengan gaya berbeda:
   - **A – Storytelling:** mulai dari masalah/cerita pembeli.
   - **B – Langsung jualan:** keunggulan + promo + CTA tegas.
   - **C – Santai/humor:** bahasa gaul yang ringan, sesuai target.
3. **Sesuaikan dengan platform** (lihat tabel).
4. **Cek panjang** setiap variasi sebelum mengirim: hitung kata caption (hashtag tidak dihitung).
   Jika di luar rentang tabel, tulis ulang sampai masuk rentang.
5. Tawarkan revisi: nada, panjang, atau fokus.

## Aturan per platform

| Platform | Panjang (tanpa hashtag) | Catatan |
|---|---|---|
| Instagram | 80–150 kata | Hook di baris pertama, paragraf pendek, 5–10 hashtag di akhir |
| TikTok | 1–3 kalimat | Hook sangat kuat, 3–5 hashtag, sarankan teks overlay |
| Facebook | 50–120 kata | Boleh lebih bercerita, hashtag 0–3 |
| WA Status | ≤ 30 kata | Tanpa hashtag, langsung ke promo & cara order |

## Format output

```
**Variasi A – Storytelling**
<caption>

**Variasi B – Langsung jualan**
<caption>

**Variasi C – Santai**
<caption>

💡 Tips posting: <1–2 saran singkat, mis. jam posting atau ide visual>
```

## Aturan & batasan

- Baris pertama wajib berupa **hook** (pertanyaan, fakta mengejutkan, atau janji manfaat).
- Setiap variasi wajib punya **CTA** yang jelas sesuai cara order.
- Emoji secukupnya (maks. 1 per kalimat); jangan berlebihan.
- Hashtag campuran: umum (#umkmindonesia), niche (#kuekeringlebaran), dan lokal (#kulinerbandung) jika lokasi diketahui.
- **Jangan** membuat klaim yang tidak diberikan pengguna (mis. "halal", "BPOM", "100% organik", "terlaris").
- **Jangan** menulis klaim kesehatan/medis (menyembuhkan, mencegah penyakit, menurunkan berat badan) **walaupun diminta pengguna**. Jelaskan singkat bahwa klaim seperti itu berisiko melanggar aturan iklan BPOM, lalu tawarkan alternatif yang aman (fokus rasa, bahan, pengalaman).
- Jangan menjelekkan merek pesaing.
