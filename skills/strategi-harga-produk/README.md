# Harga Tepat, Laku, dan Tetap Untung

**Tentukan harga eceran, reseller, paket, dan promo dengan hitungan yang jelas, bukan feeling.**

Diuji AI penguji independen di OpenClaw: 7,0 → 9,0 dari 10 (versi 1.0.9, 3 Okt 2026; pesan yang sama tanpa dan dengan skill: toko PKP (Pengusaha Kena Pajak) menjual hampers). Margin dan pasal harga coret sudah benar di kedua sisi; pembedanya harga lantai Rp203.500 (harga terendah yang masih memenuhi margin minimum 40% untuk makanan), sedangkan AI tanpa skill tidak memberi harga lantai dan malah menyarankan menaikkan harga dulu beberapa hari sebelum dicoret.

> **Yang Anda butuhkan:** AI agent yang mendukung skill (OpenClaw, Claude Code, Codex, atau Cursor — langganan AI-nya ditanggung sendiri) di komputer Windows/Mac/Linux. Python 3 (bawaan Mac/Linux, unduh gratis di Windows) untuk menjalankan skrip pendukung skill ini; tanpa Python skill tetap berjalan, AI mengerjakannya langsung tetapi hasil angka sebaiknya Anda cek ulang. Tidak perlu API key atau akun tambahan dari Komunitech.

## Manfaat
- ✅ Harga yang disarankan dihitung agar **tidak di bawah batas untung** Anda (dari modal + potongan + margin minimum, yaitu untung dibagi harga jual, yang Anda tetapkan)
- ✅ Daftar harga reseller/grosir/agen siap kirim ke WA, lengkap untung Anda dan untung reseller per level (harga anjuran reseller dijaga sama dengan harga toko)
- ✅ Tahu dulu sebelum promo: "diskon 20% berarti penjualan harus naik 51% agar untung sama", plus alternatif promo yang lebih aman
- ✅ Paket hemat & hampers dicek: pembeli hemat berapa, Anda untung berapa
- ✅ Rencana naik harga saat bahan naik: berapa pelanggan boleh berkurang sebelum rugi, plus teks pengumuman yang sopan

## Cocok untuk siapa
- Pemilik toko roti/kue, katering, kedai, F&B rumahan
- Produsen & brand kecil yang mulai membuka reseller, grosir, atau agen
- Penjual online dan offline yang ingin merancang paket, harga cantik, atau promo tanggal kembar
- Penyedia jasa (desain, foto, les) yang ingin menyusun paket Hemat/Favorit/Premium

## Contoh sebelum & sesudah
**Sebelum:** "Mau promo diskon 20% biar rame." Setelah sebulan, toko ramai tapi uang di akhir bulan malah berkurang. Harga reseller ditentukan kira-kira, agen dapat harga yang ternyata hampir tidak untung.

**Sesudah (cukup ketik):** "Roti sobek saya jual 28 ribu, modal 11.500, sewa+gaji 6,5 juta, laku 600 sebulan. Mau buka reseller dan promo 20%."

Cuplikan balasan (dipotong; contoh buatan pembuat skill, bukan hasil uji independen; data fiktif, angka dari skrip hitung; dari `examples/contoh-01-roti-sobek-reseller-dan-promo.md`):
```
Ringkasan
- Harga eceran Rp28.000 dipertahankan (berbasis nilai: roti rumahan tanpa pengawet, margin 58,93%).
- Buka tangga reseller: Rp24.000 (≥10 pcs), Rp21.000 (≥50 pcs), Rp18.000 (≥200 pcs), semua di atas margin minimum 35%.
- Diskon 20% untuk semua pembeli tidak disarankan; ganti dengan "beli 5 gratis 1" khusus hari tertentu.

| Titik impas (BEP) | 394 pcs/bulan (±16 pcs per hari, 26 hari jual) |
| Batas aman | penjualan boleh turun 34,33% sebelum rugi |
…
Promo diskon 20%
- Harga promo Rp22.400 → laba per pcs turun dari Rp16.500 ke Rp10.900.
- Agar laba kotor sama, penjualan harus naik 51,38%: dari 600 menjadi minimal 909 pcs sebulan. Kapasitas oven dan tenaga cukup?
```
Hasil lengkapnya juga memuat tabel tangga harga reseller dan teks daftar harga siap tempel ke WA.

## Cara pakai
Setelah terpasang, cukup ketik permintaan biasa ke AI agent Anda, misalnya:
- "Harga bolu pandan saya enaknya berapa? Modal 19 ribu."
- "Bikinin harga reseller, grosir, agen untuk kopi susu literan saya, modal 22 ribu, jual 45 ribu."
- "Diskon 30% untuk 11.11 masih untung nggak? Modal 40rb, harga 89.900, jual di Shopee."
- "Hampers isi 3 toples, enaknya dijual berapa?"
- "Bahan naik, mending naik harga ke 29.900 atau 31.000?"

Hasilnya memuat asumsi yang dipakai, tabel angka, aturan promo, dan langkah minggu ini. Hasil simulasi "kalau harga naik, penjualan turun berapa" diberi label **perkiraan**.

Lebih lengkap bila dipakai bersama skill Komunitech lain: **hitung-hpp** (menghitung modal dari resep), **harga-jual-marketplace** (potongan Shopee/Tokopedia/TikTok Shop), **riset-harga-kompetitor** (harga pasar pesaing).

## Instalasi singkat
Salin folder `strategi-harga-produk` ke folder skills AI agent Anda:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |

Panduan lengkap (termasuk Windows): lihat `docs/instalasi.md` (di dalam paket bernama `CARA-INSTAL.md`). Tidak perlu API key, akun, atau instalasi tambahan. Hitungan memakai Python bawaan; bila Python tidak tersedia, AI menghitung manual dengan rumus yang ditampilkan.

**Hasil uji (angka nyata):** satu sumber, skor 1–10.
- **Uji OpenClaw, uji otomatis agent, v1.0.9, 3 Okt 2026** (angka dari `examples/00-openclaw-sebelum-sesudah.md`, bagian "Uji ulang v1.0.9"): pesan yang sama dikirim tanpa dan dengan skill pada skenario hampers toko PKP (Pengusaha Kena Pajak): tanpa skill **7,0** → dengan skill **9,0** (selisih +2,0; LULUS). Tiga varian lain (frozen food, nastar + diskon 15%, kopi bubuk + diskon 10%) hanya diuji dengan skill, jadi tidak dipakai sebagai angka sebelum/sesudah: 8,5, 9,0, dan 8,5. Tidak ada angka harga, diskon, atau margin yang salah di keempat balasan dengan skill; masih ada beberapa ungkapan longgar seperti "~28–29%" yang tidak salah. Pada hampers Rp189.000 (modal Rp110.000), skill membandingkan cara keliru (dibagi 1,12: margin 34,81%) dengan yang benar (DPP, yaitu harga sebelum PPN, Rp170.271, margin 35,4%), memberi harga lantai Rp203.500 untuk margin pangan 40%, dan menolak harga coret palsu (harga "asli" yang dicoret agar tampak diskon padahal tidak pernah dijual). Catatan jujur: tanpa skill, margin dan pasal harga coret sudah benar, tetapi AI menyarankan "naikin dulu ke Rp249.000 beberapa hari, baru promo" dan tidak memberi harga lantai. Versi terkini 1.0.10 (13 Okt 2026) hanya menambah aturan penulisan dasar aturan dan memperbarui contoh; belum diuji ulang di OpenClaw.

**Status uji (jujur):** sudah diuji di OpenClaw (uji otomatis agent) dan Claude Code (simulasi agent); Codex dan Cursor belum diuji langsung (format skill-nya sama).

## FAQ
**Apa bedanya margin dan markup? Saya bilang "untung 50%".**
Margin = untung dibagi harga jual; markup = untung dibagi modal. Modal Rp10.000 dijual Rp15.000 itu markup 50% tapi margin hanya 33,33%. Skill ini menampilkan keduanya dan bertanya bila maksud Anda belum jelas.

**Apakah skill ini bisa memastikan penjualan tidak turun kalau saya naik harga?**
Tidak ada yang bisa memastikan. Yang bisa dihitung: berapa penjualan boleh turun sebelum untung Anda lebih kecil dari sekarang. Perkiraan pada tiga tingkat kepekaan pembeli diberi label "perkiraan", dan skill menyarankan uji kecil dulu.

**Usaha saya PKP (Pengusaha Kena Pajak), bagaimana dengan PPN?**
Untung dihitung dari harga sebelum PPN. Bila ingin harga tayang cantik yang sudah termasuk PPN (mis. Rp49.900), skill menghitung DPP dan PPN-nya (tarif 12% × DPP nilai lain 11/12, dibulatkan ke bawah), margin dari DPP, dan harga tayang minimum termasuk PPN — untuk harga satuan, reseller, paket, promo, dan harga cantik. Pembulatan belum dicocokkan dengan Coretax (sistem pajak online DJP); untuk faktur resmi ikuti Coretax atau konsultan pajak. Bila bukan PKP, Anda tidak boleh memungut PPN.

## Atribusi & lisensi
Kerangka strategi harga diadaptasi dari dua karya berlisensi MIT: coreyhaines31/marketingskills (Corey Haines) dan phuryn/pm-skills (Pawel Huryn), lalu ditulis ulang untuk UMKM Indonesia dengan hitungan Rupiah buatan Komunitech. Teks lisensi asli ada di `LICENSE-MIT-marketingskills` dan `LICENSE-MIT-pm-skills`; rincian di `ATTRIBUTION.md`. Tidak berafiliasi dengan para pembuat sumber.

## Riwayat perubahan

Versi terkini: **1.0.10**. Rincian teknis tiap versi ada di `CHANGELOG.md` di folder skill ini.
