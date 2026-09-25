# Cek Kenapa Toko Online Kamu Tidak Muncul di Google

**Kirim link atau tempel halaman toko online kamu, langsung dapat skor per bagian, daftar perbaikan urut prioritas, dan teks pengganti siap tempel — bukan sekadar saran umum "perbaiki SEO-nya".**

## Manfaat
- ✅ Angka dihitung, bukan dikira: panjang title & meta description dihitung persis lewat script, bukan tebak-tebakan "kayaknya kepanjangan"
- ✅ Cek data terstruktur (JSON-LD) yang sering dilewatkan — termasuk cek khusus `LocalBusiness`/`Product` dengan format alamat Indonesia, plus contoh JSON-LD siap isi
- ✅ Daftar perbaikan diurutkan **dampak × kemudahan**, jadi tahu mana yang dikerjakan duluan, bukan daftar panjang tanpa prioritas
- ✅ Termasuk cek konsistensi NAP (Nama-Alamat-Telepon) untuk Google Business Profile/Maps — penting untuk warung, bengkel, klinik, dan usaha lokal lain
- ✅ Jujur soal batasan: tidak pernah mengarang angka volume pencarian, skor kecepatan, atau janji ranking #1, dan tidak akan menyarankan cara curang (beli backlink/ulasan, keyword stuffing)

## Cocok untuk siapa
- Pemilik toko online (WooCommerce/WordPress, Shopify, situs buatan sendiri) yang merasa "sudah bikin website tapi kok sepi dari Google"
- Pemilik usaha lokal (warung, bengkel, servis panggilan, klinik, salon) yang mau usahanya lebih gampang ditemukan di Google Maps
- Siapa pun yang baru pindah/redesain website dan mau memastikan tidak ada yang rusak (mis. lupa mematikan mode "coming soon" yang menyembunyikan halaman dari Google)
- **Bukan untuk:** judul/deskripsi Shopee/Tokopedia/TikTok Shop (pakai `listing-marketplace`), menulis landing page dari nol (pakai `copy-landing-page`), atau caption sosmed (pakai `caption-sosmed-umkm`)

## Contoh sebelum & sesudah
**Sebelum:** Pemilik warung tanya "kenapa ya warung saya susah dicari di Google padahal udah punya website" — tanpa tahu title halamannya cuma "Home", tidak ada meta description, alamat di website beda dengan yang di Google Maps, dan tidak ada satu pun foto bertanda alt text.

**Sesudah (cukup ketik):** "Tolong audit SEO website warung ayam geprek saya, ini linknya..."
→ Skor per bagian (title ❌, heading ⚠️, data lokal ❌), daftar perbaikan #1 "Ganti title 'Home' → 'Ayam Geprek Bu Sri - Pedas Level 1-10, [Kecamatan]'" (Dampak Tinggi, Mudah), #2 "Samakan alamat website dengan Google Maps", lengkap teks title/meta description baru siap tempel dan contoh JSON-LD `LocalBusiness` terisi. Lihat contoh penuh di `examples/uji-pembuat-01-warung-ayam-geprek.md`.

## Cara pakai
Setelah terpasang, cukup ketik permintaan biasa ke AI agent kamu, misalnya:
- "Audit SEO website toko saya: https://tokosaya.com/produk/keripik-pedas"
- "Kenapa toko online saya nggak muncul di Google? Ini saya tempel HTML halamannya..."
- "Cek Google Bisnisku warung saya, alamatnya udah bener belum"

Kalau AI agent kamu tidak bisa membuka link secara langsung, dia akan minta kamu menempel isi halaman (caranya dijelaskan saat diminta — tinggal klik kanan → "Lihat Sumber Halaman" lalu salin-tempel). Kalau info penting (nama usaha, kata kunci target) belum kamu sebutkan, AI akan tanya sekali dalam satu pesan.

## Instalasi singkat
Salin folder `audit-seo-toko-online` ke folder skills AI agent kamu:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |

Panduan lengkap (termasuk Windows): lihat `docs/instalasi.md` yang disertakan dalam paket.

## FAQ
**Apakah ini menjamin toko saya jadi peringkat 1 di Google?**
Tidak. Tidak ada yang bisa menjamin itu — peringkat Google dipengaruhi banyak faktor di luar satu halaman (persaingan, waktu, faktor lain). Skill ini fokus membenahi hal-hal dasar yang benar-benar dalam kendalimu dan bisa dicek, dengan jujur menyebutkan kalau ada data yang tidak tersedia.

**Harus punya akun Google Search Console atau tools SEO berbayar?**
Tidak. Semua pengecekan teknis dilakukan dari file HTML yang kamu tempel/kirim linknya, tanpa akun atau API key apa pun. Untuk kecepatan halaman & Google Business Profile, kamu cukup jawab beberapa pertanyaan singkat — skill ini tidak butuh login ke akun mana pun.

**Bagaimana kalau website saya WordPress dan pakai plugin SEO (Yoast/RankMath)?**
Tetap bisa diaudit. Ada catatan khusus di hasil audit soal data terstruktur (JSON-LD) yang disisipkan plugin lewat JavaScript — supaya cara kamu mengambil HTML (Simpan Halaman vs Lihat Sumber Halaman) tidak membuat hasilnya salah dibaca.
