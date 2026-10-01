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
4. **Daftar fakta.** Sebelum menulis, catat dalam hati "Fakta dari pengguna": hanya yang diucapkan pengguna (produk, harga, ukuran, lokasi, cara order). Apa pun di luar daftar itu tidak boleh muncul sebagai fakta; tulis `[isi: ...]` atau tanyakan.
5. **Cek sebelum kirim.** Simpan 3 variasi ke file kerja lalu jalankan
   `python3 <folder-skill-ini>/scripts/cek_caption.py --platform ig --teks-file caption.md --fakta "<kata-kata pengguna>"`
   (`python`/`py` di Windows; platform: `ig`, `tiktok`, `fb`, `wa`). Skrip menghitung kata, hashtag, dan menandai klaim karangan/kesehatan. Perbaiki semua GAGAL sampai `HASIL: LULUS`. Bila skrip tidak bisa dijalankan, hitung manual: kata (tanpa hashtag) dan jumlah hashtag per variasi harus masuk tabel.
6. Tawarkan revisi: nada, panjang, atau fokus.

## Aturan per platform

| Platform | Panjang (tanpa hashtag) | Catatan |
|---|---|---|
| Instagram | 80–150 kata | Hook di baris pertama, maks. 2–3 kalimat per paragraf (baris kosong di antaranya), **3–8 hashtag relevan di baris terakhir, wajib di SETIAP variasi** |
| TikTok | 8–60 kata (1–3 kalimat) | Hook sangat kuat, 3–5 hashtag, sarankan teks overlay |
| Facebook | 50–120 kata | Boleh lebih bercerita, hashtag 0–3 |
| WA Status | ≤ 30 kata | Tanpa hashtag, langsung ke promo & cara order |

## Format output

```
**Variasi A – Storytelling**
<caption, panjang sesuai tabel>
#hashtag1 #hashtag2 #hashtag3  (jumlah sesuai tabel)

**Variasi B – Langsung jualan**
<caption>
#hashtag ...

**Variasi C – Santai**
<caption>
#hashtag ...

💡 Tips posting: <1–2 saran singkat, mis. jam posting atau ide visual>
```

## Aturan & batasan

- Baris pertama wajib berupa **hook** (pertanyaan, fakta mengejutkan, atau janji manfaat).
- Setiap variasi wajib punya **CTA** yang jelas sesuai cara order.
- Emoji secukupnya (maks. 1 per kalimat); jangan berlebihan.
- Hashtag campuran: umum (#umkmindonesia), niche (#kuekeringlebaran), dan lokal (#kulinerbandung) jika lokasi diketahui.
- **Fakta hanya dari pengguna.** Jangan menambah fakta apa pun yang tidak diberikan: bahan, "tanpa pengawet", "100% alami", asal/daerah, ukuran, stok terbatas, gratis ongkir/siap antar, jam buka, "terlaris/favorit", label halal/BPOM/PIRT, angka pelanggan, dan **testimoni/pengalaman pribadi karangan** ("dulu aku juga..."). Butuh detail itu? Tulis `[isi: ...]` atau tanyakan. Cerita di Variasi A memakai situasi umum pembeli (bukan "aku/saya" fiktif).
- **Klaim kesehatan DILARANG walaupun diminta**, terutama untuk pangan, minuman, jamu/herbal, suplemen, dan kosmetik. Aturan iklan BPOM (Perka BPOM tentang pengawasan iklan pangan olahan/obat tradisional/kosmetik, serta UU 8/1999 Perlindungan Konsumen) melarang klaim mengobati, menyembuhkan, meredakan, mengatasi, mencegah penyakit, menurunkan berat badan/gula darah, detox, atau "pengganti obat". Itu juga mencakup bentuk halus: "bantu redakan kembung", "pas asam lambung naik", "menjaga imun", "bikin langsing". Jelaskan singkat ke pengguna, lalu tawarkan alternatif aman: rasa, aroma, tekstur, tradisi/kebiasaan minum, cara menikmati, bahan **yang disebut pengguna**, momen konsumsi (mis. "teman santai sore"). Pengguna perlu memastikan aturan terbaru di bpom.go.id; skill ini bukan nasihat hukum.
- Kata yang jangan dipakai di caption pangan/jamu/kosmetik: menyembuhkan, mengobati, meredakan, mengatasi, menurunkan (gula darah/kolesterol/berat badan), detox, melangsingkan, pemutih, anti-(penyakit), obat alami, terapi, khasiat, "bantu ... (penyakit)".
- Jangan menjelekkan merek pesaing.
