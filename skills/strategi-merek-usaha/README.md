# Strategi Merek Usaha: Nama & Penawaran yang Siap Jual

**Dari "bingung namanya" ke nama teruji dan penawaran yang jujur, sudah dihitung labanya.**

> **Yang Anda butuhkan:** AI agent yang mendukung skill (OpenClaw, Claude Code, Codex, atau Cursor — langganan AI-nya ditanggung sendiri) di komputer Windows/Mac/Linux. Python 3 (bawaan Mac/Linux, unduh gratis di Windows) untuk skrip hitung; tanpa Python skill tetap berjalan dengan hitungan oleh AI. Tidak perlu API key atau akun tambahan dari Komunitech.

## Manfaat
- 10 opsi nama dengan skor 0-100 yang **dihitung script** (panjang, suku kata, ejaan, kemiripan dengan merek yang kamu sebut, arti, keunikan), bukan sekadar selera.
- Pengingat cek arti negatif di bahasa daerah dan slang, plus **daftar cek domain, handle IG/TikTok, dan merek di PDKI** (langkah demi langkah, kelas Nice).
- Penawaran lengkap: nilai, bonus, garansi, batas waktu/stok yang jujur, nama paket.
- **Laba per unit dihitung** sebelum promo ditulis, jadi tidak jual rugi tanpa sadar.
- Teks siap tempel untuk WhatsApp, Instagram, dan marketplace, dengan ceklis kepatuhan UU Perlindungan Konsumen.

## Cocok untuk
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
Salin folder `strategi-merek-usaha` ke folder skills AI agent kamu:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |

Panduan lengkap (termasuk Windows): lihat `CARA-INSTAL.md` di dalam paket (`docs/instalasi.md`).

## Skill pelengkap
`positioning-persona-usaha` (target & tagline), `luncurkan-produk-baru`, `hitung-hpp`, `harga-jual-marketplace`, `caption-sosmed-umkm`, `copy-landing-page`, `promo-kalender`.

## Bukti uji di bot Telegram

Diuji di bot OpenClaw asli (grup uji Komunitech, tautan hanya terbuka untuk anggota grup): gelombang 8, 2026-10-05.
- Tanpa skill: https://t.me/c/4407409583/788/809 — skor 6
- Dengan skill: https://t.me/c/4407409583/789/811 — skor 8
Verdik gelombang: LULUS — DENGAN membuang "STOK TINGGAL 5" dari teks siap tempel (hanya bila stok nyata), memberi 3 caption dan menghitung margin 48,6% → 35,7% (turun Rp7.000, 41%); TANPA menaruh "Stok tinggal 5, buruan" di teks siap tempel lalu baru bertanya apakah stoknya benar.

## FAQ
**Apakah nama pilihan skill ini pasti tidak dipakai orang lain?**
Tidak. Skill hanya membandingkan dengan merek yang kamu sebutkan dan memberi langkah cek. Hasil akhir ada di pencarian domain, handle, dan PDKI yang kamu lakukan.

**Boleh bikin "stok tinggal 3" supaya orang buru-buru beli?**
Hanya bila memang benar. Skill menolak kelangkaan palsu dan menawarkan versi jujur (kuota nyata, batas tanggal yang ditegakkan).

**Apakah harus bisa Python?**
Tidak. Agent yang menjalankan script; bila tidak bisa, hitungan manual dengan rumus di `references/`.

Kredit sumber terbuka dan lisensi: lihat `ATTRIBUTION.md`. Tidak berafiliasi dengan pembuat sumber.

## Riwayat perubahan

Versi terkini: **1.0.4**. Rincian teknis tiap versi ada di `CHANGELOG.md` di folder skill ini.
