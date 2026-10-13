# Strategi Merek Usaha: Nama & Penawaran yang Siap Jual

**Dari "bingung namanya" ke nama teruji dan penawaran yang jujur, sudah dihitung labanya.**

> **Yang Anda butuhkan:** AI agent yang mendukung skill (OpenClaw, Claude Code, Codex, atau Cursor — langganan AI-nya ditanggung sendiri) di komputer Windows/Mac/Linux. Python 3 (bawaan Mac/Linux, unduh gratis di Windows) untuk skrip hitung; tanpa Python skill tetap berjalan dengan hitungan oleh AI. Tidak perlu API key atau akun tambahan dari Komunitech.

## Manfaat
- 10 opsi nama dengan skor 0-100 yang **dihitung script** (panjang, suku kata, ejaan, kemiripan dengan merek yang kamu sebut, arti, keunikan), bukan sekadar selera.
- Pengingat cek arti negatif di bahasa daerah dan slang, plus **daftar cek domain, handle IG/TikTok, dan merek di PDKI** (langkah demi langkah, kelas Nice).
- Penawaran lengkap: nilai, bonus, garansi, batas waktu/stok yang jujur, nama paket.
- **Laba per unit dihitung** sebelum promo ditulis, jadi tidak jual rugi tanpa sadar.
- Teks siap tempel untuk WhatsApp, Instagram, dan marketplace, dengan ceklis kepatuhan UU Perlindungan Konsumen.

## Cocok untuk siapa
- Pemilik usaha kecil-menengah yang baru mau menamai usaha atau produk.
- Penjual online yang promonya sepi atau labanya tipis.
- Admin/marketing yang butuh penawaran cepat dan aman.
Tidak cocok: nasihat hukum merek (sengketa, boleh/tidak boleh daftar), desain logo/kemasan.

## Contoh sebelum & sesudah
**Sebelum:** "Sambal saya namanya belum ada. Promonya diskon 30% terus tapi untungnya tipis."
**Sesudah:** 10 nama dengan skor (mis. "Cabe Gendis 86/100"), tabel cek domain/handle/PDKI (belum dicek, kamu yang mengisi), dan penawaran "Paket Sarapan Pedas" (sambal + kartu resep + stiker, garansi ganti rusak): laba Rp15.900 per botol dibanding Rp10.770 pada diskon 15%. Lihat `examples/`.

## Cara pakai
Ketik permintaan biasa:
- "Bantu cari nama untuk usaha kue kering saya di Bandung."
- "Nama ini mirip merek lain nggak? Merek yang saya tahu: ..."
- "Bikin penawaran sambal Rp38.000, modal Rp17.000, potongan Shopee 8%."
Script (opsional; tanpa Python skill tetap berjalan dengan rumus manual):
`python3 scripts/skor_nama.py nama.csv --merek "Merek A, Merek B"` dan `python3 scripts/hitung_penawaran.py --harga 38000 --hpp 17000 --platform 8` (Windows: `python` atau `py`).

## Penting
Skill ini **tidak** memastikan nama tersedia atau bisa didaftarkan, dan bukan nasihat hukum. Kamu yang mengecek domain, handle, dan PDKI; konsultan kekayaan intelektual yang menilai risiko merek.

## Instalasi singkat
Salin folder `strategi-merek-usaha` ke folder skills AI agent kamu (OpenClaw, Codex, Claude Code, Cursor). Lokasi lengkap: **`docs/instalasi.md`**.

## Skill pelengkap
`positioning-persona-usaha` (target & tagline), `luncurkan-produk-baru`, `hitung-hpp`, `harga-jual-marketplace`, `caption-sosmed-umkm`, `copy-landing-page`, `promo-kalender`.

**Hasil uji (angka nyata):** uji OpenClaw sebelum/sesudah otomatis agent, 2026-10-01 (uji ulang v1.0.3), skor 1–10 penguji independen. Sumber: `examples/00-openclaw-sebelum-sesudah.md`.
- Rata-rata 2 skenario: tanpa skill **6** → dengan skill **8,75** (LULUS).
- Bot Telegram asli (gelombang 8, 2026-10-05): tanpa skill **6** → dengan skill **8** — DENGAN menolak "STOK TINGGAL 5" palsu dan menghitung margin promo; TANPA menaruh urgency palsu di teks siap tempel.

**Status uji (jujur):** sudah diuji di OpenClaw (uji otomatis agent) dan Claude Code (simulasi agent); bot Telegram asli gelombang 8. Codex dan Cursor belum kami uji langsung. Cek domain/handle/PDKI tetap manual — bukan nasihat hukum merek.

Diadaptasi dari skill open-source (MIT); rincian di `ATTRIBUTION.md`. Tidak berafiliasi dengan pembuat sumber.

## FAQ
**Apakah nama pilihan skill ini pasti tidak dipakai orang lain?**
Tidak. Skill hanya membandingkan dengan merek yang kamu sebutkan dan memberi langkah cek. Hasil akhir ada di pencarian domain, handle, dan PDKI yang kamu lakukan.

**Boleh bikin "stok tinggal 3" supaya orang buru-buru beli?**
Hanya bila memang benar. Skill menolak kelangkaan palsu dan menawarkan versi jujur (kuota nyata, batas tanggal yang ditegakkan).

**Apakah harus bisa Python?**
Tidak. Agent yang menjalankan script; bila tidak bisa, hitungan manual dengan rumus di `references/`.

## Riwayat perubahan

Versi terkini: **1.0.4**. Rincian teknis tiap versi ada di `CHANGELOG.md` di folder skill ini.
