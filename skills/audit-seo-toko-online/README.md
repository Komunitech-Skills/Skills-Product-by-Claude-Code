# Kenapa Toko Online Anda Tidak Muncul di Google

**Kirim link atau tempel halaman toko online Anda, langsung dapat skor per bagian, daftar perbaikan urut prioritas, dan teks pengganti siap tempel — bukan sekadar saran umum "perbaiki SEO-nya" (SEO = membenahi website agar mudah ditemukan di Google).**

Diuji AI penguji independen di OpenClaw: 7,0 → 8,75 dari 10 (temuan inti benar di kedua sisi; pembedanya: tanpa skill AI menulis ulang halaman Anda dengan fakta yang tidak pernah Anda sebut, dengan skill teks pengganti siap tempel hanya memakai data Anda dan ada skor per bagian).

> **Yang Anda butuhkan:** AI agent yang mendukung skill (OpenClaw, Claude Code, Codex, atau Cursor — langganan AI-nya ditanggung sendiri) di komputer Windows/Mac/Linux. Python 3 (bawaan Mac/Linux, unduh gratis di Windows) untuk menjalankan skrip pendukung skill ini; tanpa Python skill tetap berjalan, AI mengerjakannya langsung tetapi hasil angka sebaiknya Anda cek ulang. Tidak perlu API key atau akun tambahan dari Komunitech.

## Manfaat
- ✅ Angka dihitung, bukan dikira: panjang judul halaman (title) & deskripsi Google (meta description) dihitung persis lewat skrip, bukan tebak-tebakan "kayaknya kepanjangan"
- ✅ Cek data terstruktur (JSON-LD, kode tersembunyi yang membantu Google memahami toko Anda) yang sering dilewatkan — termasuk cek khusus `LocalBusiness`/`Product` dengan format alamat Indonesia, plus contoh JSON-LD siap isi
- ✅ Daftar perbaikan diurutkan **dampak × kemudahan**, jadi tahu mana yang dikerjakan duluan
- ✅ Termasuk cek konsistensi NAP (Nama-Alamat-Telepon) untuk Google Business Profile/Maps — penting untuk warung, bengkel, klinik, dan usaha lokal lain
- ✅ Jujur soal batasan: tidak mengarang angka volume pencarian, skor kecepatan, atau janji ranking #1, dan tidak menyarankan cara curang (beli backlink = tautan murah dari situs lain, beli ulasan, keyword stuffing = menjejalkan kata kunci berlebihan)

## Cocok untuk siapa
- Pemilik toko online (WooCommerce/WordPress, Shopify, situs buatan sendiri) yang merasa "sudah bikin website tapi kok sepi dari Google"
- Pemilik usaha lokal (warung, bengkel, servis panggilan, klinik, salon) yang mau usahanya lebih gampang ditemukan di Google Maps
- Siapa pun yang baru pindah/redesain website dan mau mengecek apakah ada yang rusak (mis. lupa mematikan mode "coming soon" yang menyembunyikan halaman dari Google)
- **Bukan untuk:** judul/deskripsi Shopee/Tokopedia/TikTok Shop (pakai `listing-marketplace`), menulis landing page dari nol (pakai `copy-landing-page`), atau caption sosmed (pakai paket konten mingguan, `konten-mingguan`)

## Contoh sebelum & sesudah
**Sebelum:** Pemilik warung tanya "kenapa ya warung saya susah dicari di Google padahal udah punya website" — tanpa tahu title halamannya cuma "Home", tidak ada meta description, alamat di website beda dengan yang di Google Maps, dan tidak ada satu pun foto bertanda alt text (teks pengganti gambar).

**Sesudah (cukup ketik):** "Tolong audit SEO website warung ayam geprek saya. Saya tempel isi halamannya ya. Kata kunci yang saya mau ditarget: 'ayam geprek Cibiru'…"

Cuplikan hasil (dipotong; uji simulasi oleh pembuat skill, 25 Sep 2026, data fiktif — dari `examples/uji-pembuat-01-warung-ayam-geprek.md`):
```
# Laporan Audit SEO: Ayam Geprek Bu Sri
| Bagian | Skor | Catatan singkat |
| Judul & meta description | ❌ | Title cuma "Home", meta description kosong |
| Heading & struktur isi | ⚠️ | Ada 1 H1 (bagus), tapi lompat ke H3 tanpa H2 |
| Google Business Profile/Maps & lokal (manual) | ❌ | Alamat website TIDAK konsisten dengan Google Bisnisku (NAP) |
…
1. **Samakan alamat website dengan Google Bisnisku (NAP)** — Dampak: Tinggi · Kemudahan: Mudah
2. **Ganti judul (title) halaman** — Dampak: Tinggi · Kemudahan: Mudah
…
**Title baru (36 karakter):**
Ayam Geprek Bu Sri - Cibiru, Bandung
```
Hasil lengkapnya juga memuat 8 perbaikan berurutan, deskripsi (meta description) baru, dan contoh JSON-LD `LocalBusiness` yang sudah terisi.

## Cara pakai
Setelah terpasang, cukup ketik permintaan biasa ke AI agent Anda, misalnya:
- "Audit SEO website toko saya: https://tokosaya.com/produk/keripik-pedas"
- "Kenapa toko online saya nggak muncul di Google? Ini saya tempel HTML halamannya..."
- "Cek Google Bisnisku warung saya, alamatnya udah bener belum"

Kalau AI agent Anda tidak bisa membuka link secara langsung, dia akan minta Anda menempel isi halaman (caranya dijelaskan saat diminta — tinggal klik kanan → "Lihat Sumber Halaman" lalu salin-tempel). Kalau info penting (nama usaha, kata kunci target) belum Anda sebutkan, AI akan tanya sekali dalam satu pesan.

## Instalasi singkat
Salin folder `audit-seo-toko-online` ke folder skills AI agent Anda:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |

Panduan lengkap (termasuk Windows): lihat `docs/instalasi.md` (di dalam paket bernama `CARA-INSTAL.md`).

**Hasil uji (angka nyata):** uji OpenClaw (lingkungan uji terpisah), 2 Okt 2026 (v1.0.4), skor 1–10 penguji independen: tanpa skill **7,0** → dengan skill **8,75** (LULUS). Sumber: `examples/00-openclaw-sebelum-sesudah.md`. Dua skenario: audit halaman produk nyata (tanpa skill 6 → dengan skill 9) dan jebakan beli backlink/ulasan palsu (8 → 8,5). Pada audit halaman, AI tanpa skill menulis ulang file Anda dan menambahkan fakta yang tidak pernah Anda sebut (mis. "masa simpan 3 bulan"); dengan skill teks siap tempel memakai data Anda saja, sisanya ditandai `[isi: ...]`, plus skor per bagian. Catatan jujur: pada skenario jebakan AI tanpa skill sudah menolak dengan baik; keunggulan skill jelas pada audit halaman nyata.

**Status uji (jujur):** sudah diuji di OpenClaw (uji sebelum/sesudah otomatis agent, 2026-10-02). Claude Code (simulasi agent). Codex dan Cursor belum uji platform asli.

## FAQ
**Apakah ini menjamin toko saya jadi peringkat 1 di Google?**
Tidak, dan tidak ada yang bisa menjamin itu — peringkat Google dipengaruhi banyak faktor di luar satu halaman (persaingan, waktu, faktor lain). Skill ini fokus membenahi hal-hal dasar yang benar-benar dalam kendali Anda dan bisa dicek, dengan jujur menyebutkan kalau ada data yang tidak tersedia.

**Harus punya akun Google Search Console atau tools SEO berbayar?**
Tidak wajib. Pengecekan teknis dilakukan dari file HTML yang Anda tempel/kirim linknya, tanpa akun atau API key. Untuk kecepatan halaman & Google Business Profile, Anda cukup jawab beberapa pertanyaan singkat — skill ini tidak butuh login ke akun mana pun.

**Bagaimana kalau website saya WordPress dan pakai plugin SEO (Yoast/RankMath)?**
Tetap bisa diaudit. Ada catatan khusus di hasil audit soal data terstruktur (JSON-LD) yang disisipkan plugin lewat JavaScript — supaya cara Anda mengambil HTML (Simpan Halaman vs Lihat Sumber Halaman) tidak membuat hasilnya salah dibaca.

Skill ini diadaptasi dari struktur marketing skill open-source (MIT, coreyhaines31/marketingskills); teks, contoh Indonesia, dan checklist milik Komunitech. Komunitech tidak berafiliasi dengan pembuat sumber.

## Riwayat perubahan

Versi terkini: **1.0.5**. Rincian teknis tiap versi ada di `CHANGELOG.md` di folder skill ini.
