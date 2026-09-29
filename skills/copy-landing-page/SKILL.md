---
name: copy-landing-page
description: Membuat teks halaman jualan berbahasa Indonesia untuk landing page, link-in-bio, dan halaman produk di website/toko online sendiri — headline, masalah, manfaat, bukti sosial, penawaran, garansi, FAQ, dan CTA WhatsApp — lengkap versi panjang, versi pendek satu layar HP, 3 variasi headline, meta title/description SEO, dan tautan wa.me siap pakai. Gunakan saat pengguna minta landing page, sales page, halaman penjualan, page produk, link in bio, atau copy website (landing page copy, sales page copy, product page copy, website sales copy). Bukan untuk caption media sosial (pakai caption-sosmed-umkm), judul/deskripsi Shopee/Tokopedia/TikTok Shop (pakai listing-marketplace), atau pesan broadcast WhatsApp (pakai broadcast-wa).
---

# Copy Landing Page

> **Aturan kerja:** Jangan menginstal paket/aplikasi (mis. `pip install`) — bila perlu, tunjukkan caranya dan biarkan pengguna yang memasang; jangan membuka atau mencari file selain yang diberikan pengguna, isi folder skill ini, dan file yang disebut di langkah kerja; jangan menulis file baru tanpa menyebut lokasinya, dan simpan hasil di folder kerja yang disepakati (bukan /tmp).

Mengubah info produk seadanya menjadi teks halaman jualan yang lengkap, jujur, dan siap tempel — untuk landing page sendiri, link-in-bio (Linktree/Saweria/bio Instagram), atau halaman produk di website/toko online.

## Kapan digunakan
- "Buatkan landing page untuk keripik pedas saya, harga 25 ribu."
- "Bikin halaman jualan buat jasa servis AC, mau tampilan link in bio."
- "Tuliskan copy untuk halaman produk kursus online saya di website."
- Memperbaiki landing page lama yang sepi pembeli atau CTA-nya tidak jelas.

## Kapan TIDAK digunakan
- Caption Instagram/TikTok/Facebook/WA Status → pakai skill `caption-sosmed-umkm`.
- Judul & deskripsi produk Shopee/Tokopedia/TikTok Shop → pakai skill `listing-marketplace`.
- Pesan broadcast WhatsApp ke daftar kontak → pakai skill `broadcast-wa`.
- Proposal kerja sama/kemitraan B2B → pakai skill `proposal-kerjasama`.
- Slide/pitch deck presentasi → pakai skill `presentasi-instan`.
- Produk ilegal, obat/suplemen dengan klaim menyembuhkan, rokok elektrik, judi, investasi ilegal → tolak dengan sopan.

## Input
Tanyakan (atau simpulkan dari cerita pengguna):
1. Produk/jasa apa, dan siapa target pembelinya?
2. Harga, dan apakah ada harga coret/diskon **asli** (harga sebelumnya benar-benar pernah berlaku)?
3. Masalah/keinginan apa yang diselesaikan buat pembeli?
4. Cara pemesanan: nomor WhatsApp (untuk tombol CTA), metode bayar (transfer/COD/QRIS), ongkir/area kirim.
5. Bukti sosial yang **benar-benar ada** (testimoni asli, jumlah pelanggan nyata, izin edar/sertifikat resmi) — jangan pernah mengarang.
6. Nada yang diinginkan: santai, profesional, atau "bahasa ibu-ibu" (hangat, akrab, banyak sapaan).
7. Format tujuan: landing page lengkap, halaman produk website, atau versi pendek link-in-bio.

**Kalau info kurang:** tanyakan SEKALI dalam satu pesan berisi daftar poin di atas yang belum terjawab. Kalau pengguna ingin cepat, pakai default berikut dan sebutkan di akhir sebagai asumsi:
- Nada: santai-profesional (ramah tapi tidak lebay).
- Metode bayar: Transfer & QRIS (sebut "cek metode yang tersedia di tokomu").
- Nomor WA: tulis placeholder `[NOMOR WA KAMU]` — beri tahu pengguna untuk menggantinya.
- Tidak ada testimoni/angka penjualan yang disebut sama sekali (lebih baik kosong daripada karangan).

## Langkah kerja
1. **Cek kepatuhan dulu.** Baca [references/dasar-hukum-klaim.md](references/dasar-hukum-klaim.md). Kalau produk masuk kategori sensitif (obat, suplemen, kosmetik, makanan/minuman berklaim kesehatan, jasa medis/klinik, keuangan/investasi), tandai klaim yang butuh izin resmi dan JANGAN tuliskan klaim tersebut kecuali pengguna memastikan izin/sertifikatnya ada.
2. **Susun struktur halaman** mengikuti kerangka di [references/struktur-halaman.md](references/struktur-halaman.md): Headline → Sub-headline → Masalah → Manfaat (3–5, fokus hasil bukan fitur) → Cara Kerja/Cara Pesan (3–4 langkah) → Bukti Sosial → Penawaran (harga, ongkir, cara bayar) → Garansi/Retur → FAQ → CTA penutup.
3. **Tulis 3 variasi headline** dengan pendekatan berbeda (hasil, pertanyaan, sebelum/sesudah) — lihat contoh formula di references.
4. **Bukti sosial:** jika pengguna memberi testimoni/data asli, pakai kata-kata mereka (boleh dirapikan, jangan diubah maknanya). Jika tidak ada, tulis placeholder `[ISI TESTIMONI ASLI — nama & kota pembeli]` — JANGAN PERNAH mengarang testimoni, jumlah pelanggan, rating bintang, atau angka "terjual X pcs".
5. **Bangun tombol CTA WhatsApp.** Susun pesan WA singkat yang relevan (mis. "Halo, saya mau pesan [produk] dari halaman ini"), lalu bentuk tautan `https://wa.me/62<nomor>?text=<pesan ter-encode>`. Kalau ada Python, jalankan `python3 scripts/bangun_tautan_wa.py wa --nomor "<nomor>" --pesan "<pesan>"` untuk encoding yang benar dan validasi format nomor. Kalau Python tidak tersedia, encode manual (ganti spasi dengan `%20`, dst.) dan sebutkan ke pengguna agar dicek sekali sebelum dipakai.
6. **Tulis versi pendek** (link-in-bio / satu layar HP): headline + 1 kalimat manfaat utama + 1 bukti sosial singkat (atau dilewati kalau tidak ada) + tombol CTA. Maksimal setara satu layar ponsel tanpa scroll panjang.
7. **Buat meta title & meta description SEO.** Meta title target ≤60 karakter, meta description ≤155 karakter (batas ditampilkan Google bisa berbeda per perangkat, ini batas aman umum). Kalau ada Python: `python3 scripts/bangun_tautan_wa.py meta --title "..." --desc "..."` menghitung panjang persis dan menandai jika melebihi batas. Kalau tidak ada Python, hitung karakter manual dan tampilkan angkanya.
8. **Ceklis klaim berisiko** (wajib ditampilkan di akhir output): tandai setiap kalimat yang menyinggung kesehatan/obat/BPOM/halal/"nomor 1"/"dijamin"/harga coret, sesuai daftar di references/dasar-hukum-klaim.md, dan minta pengguna mengonfirmasi dasarnya sebelum publish.
9. Tutup dengan ringkasan asumsi yang dipakai (kalau ada) dan pengingat: ganti placeholder `[NOMOR WA KAMU]` / `[ISI TESTIMONI ASLI]` sebelum halaman dipublikasikan.

## Format Output
Selalu berikan dalam urutan ini:

1. **Versi Lengkap (Landing Page)** — seluruh struktur di Langkah 2, format Markdown dengan heading per bagian, siap ditempel ke page builder (Google Sites, WordPress, Carrd, dsb.) atau dirapikan sendiri.
2. **Versi Pendek (Link-in-Bio / 1 Layar HP)** — ringkas seperti Langkah 6.
3. **3 Variasi Headline** — dengan catatan singkat pendekatan masing-masing (hasil / pertanyaan / sebelum-sesudah), untuk dites bergantian.
4. **Meta Title & Meta Description** — teks + jumlah karakter aktual, ditandai ✅ jika dalam batas, ⚠️ jika melebihi.
5. **Tautan WhatsApp siap pakai** — `https://wa.me/62...` hasil encoding, plus versi teks pesan aslinya (belum di-encode) supaya mudah dicek pengguna.
6. **Ceklis Kepatuhan** — daftar klaim yang perlu diverifikasi pengguna sebelum publish (atau "Tidak ada klaim berisiko terdeteksi" bila memang bersih).
7. **Asumsi yang dipakai** (bila ada default yang dipakai karena input awal kurang lengkap).

## Contoh
Lihat [examples/uji-pembuat-01-keripik-pedas.md](examples/uji-pembuat-01-keripik-pedas.md) untuk contoh lengkap dari permintaan "buatkan landing page untuk keripik pedas saya, harga 25 ribu" sampai ke output siap tempel (dibuat oleh pembuat skill, bukan pengganti pengujian independen Tahap 6).

## Batasan & Penanganan Error
- **Tidak pernah mengarang** testimoni, jumlah pelanggan, rating, angka "terjual", atau hitung mundur/stok palsu. Kosongkan dengan placeholder daripada mengisi angka rekaan.
- **Klaim kesehatan/obat/kosmetik/pangan berklaim khusus** ("menyembuhkan", "menghilangkan", "aman untuk ibu hamil", dll.) hanya boleh dituliskan jika pengguna menegaskan sudah punya izin edar BPOM yang sesuai; jika ragu, ganti dengan manfaat umum yang aman ("membantu menjaga", bukan klaim medis) dan catat di ceklis kepatuhan.
- **Label "halal"** hanya dicantumkan bila pengguna menyatakan produknya sudah bersertifikat BPJPH/MUI atau terdaftar self-declare; jika tidak, jangan mencantumkan kata "halal" sama sekali.
- **Harga coret** hanya untuk harga sebelumnya yang benar-benar pernah berlaku pada produk yang sama, bukan angka rekaan untuk kesan diskon besar.
- **Bukan untuk marketplace, caption sosmed, atau broadcast WA** — arahkan ke skill terkait bila itu yang diminta (lihat "Kapan TIDAK digunakan").
- **Bukan jaminan hasil SEO/ranking** — meta title/description hanya dioptimalkan formatnya (panjang & kejelasan), bukan jaminan peringkat pencarian.
- **Skrining medis/diagnosis** tidak termasuk cakupan skill ini walau produknya jasa klinik/kesehatan — hanya teks pemasaran umum non-diagnosis.
- **Tautan wa.me** memakai kode negara `62` menggantikan `0` di depan nomor Indonesia; jika pengguna memberi nomor dengan format lain, konfirmasi dulu sebelum membentuk tautan.
- **Input di luar cakupan** (mis. minta desain visual/HTML penuh, minta iklan berbayar, minta hosting) → jelaskan bahwa skill ini fokus pada teks, sarankan tempel ke page builder pilihan pengguna sendiri.
