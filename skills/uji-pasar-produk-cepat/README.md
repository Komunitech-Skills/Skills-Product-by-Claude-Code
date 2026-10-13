# Uji Pasar Produk Cepat

**Tahu produk barumu laku sebelum produksi besar, dengan angka, bukan feeling.**

## Manfaat
- Tahu asumsi mana yang paling berbahaya dan diuji dulu, tidak semua sekaligus.
- Pilih eksperimen murah yang cocok kanalmu: pre-order WA, sistem PO, sampel di bazar, landing page + WA, listing marketplace uji, konten TikTok, survei Google Form.
- Kriteria lulus ditetapkan SEBELUM uji, jadi tidak ada angka yang digeser setelah hasil keluar.
- Hasil dihitung script (konversi, rentang wajar, perbandingan dua varian), bukan dikira-kira, lengkap dengan peringatan kalau sampel terlalu sedikit.
- Keputusan jelas: LANJUT, UBAH, atau STOP, plus pilihan pivot bila perlu.

## Cocok untuk siapa
- Pemilik UMKM (makanan beku, kue, fesyen, kerajinan, jasa) yang mau meluncurkan varian atau produk baru.
- Yang sudah punya ide dan mau menguji dua pilihan (harga, kemasan, rasa, kalimat iklan).
- Profesional yang mau menguji layanan baru ke kontak sendiri.
- Belum punya ide sama sekali? Mulai dari `brainstorming-ide-usaha`. Ide baru satu kalimat? `validasi-ide-produk-baru` dulu, lalu pakai skill ini.

## Contoh sebelum & sesudah
**Sebelum:** "Aku mau produksi 200 pack dimsum mentai. Kayaknya laku sih."
**Sesudah:** "Kirim penawaran ke 80 kontak, target 15% bayar DP dalam 5 hari." Hasil: 14 dari 80 (17,5%, rentang wajar 10,7%-27,3%) -> LANJUT BERTAHAP: produksi 40 pack dulu, bukan 200, lalu uji pengiriman beku. Modal terlindungi.

**Hasil uji (OpenClaw, uji otomatis agent, v1.0.4):** rata-rata nilai 6,0 tanpa skill menjadi 9,0 dengan skill (skala 10). Pada kasus brownies matcha yang ditawarkan ke 12 orang (5 bilang mau, 0 transfer), skill memisahkan minat lisan 41,7% dari konversi nyata 0/12 = 0% (rentang wajar 95%: 0%-24%), memutuskan tegas ULANGI UJI, meminta DP kecil Rp10-20 ribu, dan menambah sampel minimal 30 sebelum modal Rp15 juta keluar. Catatan jujur: tanpa skill, logikanya sudah sehat (minat bukan pembelian, sampel kecil), tetapi tanpa angka rentang, tanpa keputusan tegas, dan ada satu perbandingan yang salah hitung. Rincian: `examples/00-openclaw-sebelum-sesudah.md`. Hasil di bot Telegram ada di bagian "Bukti uji di bot Telegram" di bawah. Codex, Claude Code, dan Cursor belum diuji langsung (format skill-nya sama).

## Cara pakai
Cukup tulis dalam bahasa biasa:
- "Aku mau tes varian mentai untuk dimsum beku, mulai dari mana?"
- "Harga 35 ribu vs 45 ribu, dari 60 orang: 9 beli vs 15 beli. Mana yang menang?"
- "Buatkan catatan eksperimen dan langkah berikutnya."

Script (opsional, Python standar): `python3 scripts/hasil_eksperimen.py hasil --ditawari 80 --aksi 14 --target 15` (Windows: `python` atau `py`). Skill tetap berguna walau script tidak bisa dijalankan.

## Instalasi singkat
Salin folder `uji-pasar-produk-cepat` ke folder skills agent kamu:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |

Panduan lengkap (termasuk Windows): lihat `docs/instalasi.md` (di dalam paket bernama `CARA-INSTAL.md`).

## Bukti uji di bot Telegram

Diuji di bot OpenClaw asli (grup uji Komunitech, tautan hanya terbuka untuk anggota grup): gelombang 7, 2026-10-05.
- Tanpa skill: https://t.me/c/4407409583/734/748 — skor 7
- Dengan skill: https://t.me/c/4407409583/735/751 — skor 8,5
Verdik gelombang: LULUS — DENGAN memisahkan minat lisan 41,7% dari konversi nyata 0/12 dengan rentang Wilson 0–24%, lalu memberi keputusan tegas plus langkah DP berbatas waktu yang bisa di-refund dan target 30 kontak baru; TANPA memberi saran praktis yang benar (minta DP, batch kecil) tetapi tanpa angka konversi atau rentang ketidakpastian.

## FAQ
**1. Bedanya dengan Tes Ide Sebelum Modal Habis (`validasi-ide-produk-baru`)?**
Itu untuk mengubah ide jadi hipotesis dan menjalankan satu uji 7 hari pertama. Ini untuk eksekusi lanjutan: beberapa asumsi, membandingkan dua varian, catatan eksperimen, dan keputusan berbasis rentang wajar.

**2. Saya hanya punya sedikit kontak. Masih bisa?**
Bisa, tapi hasilnya "sinyal arah". Skill akan menandai sampel kecil dan menyarankan uji berulang atau kanal tambahan (listing, titip kafe).

**3. Apakah hasilnya pasti akurat?**
Tidak. Ini alat bantu keputusan skala UMKM, bukan penelitian ilmiah. Teman dekat cenderung membuat hasil terlalu optimis, dan angka ambang adalah patokan praktis. Skill ini tidak menggantikan izin usaha (PIRT/BPOM/halal) untuk produk yang memerlukannya.

## Atribusi
Diadaptasi dari kerangka open source (product-on-purpose/pm-skills, Apache-2.0; phuryn/pm-skills, MIT) dan ditulis ulang untuk konteks Indonesia. Tidak berafiliasi dengan pembuat sumber. Lihat `ATTRIBUTION.md`.
