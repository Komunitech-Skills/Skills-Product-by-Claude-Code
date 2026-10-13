# Artikel Berbasis Riset, Tanpa Karangan

**Tulis artikel, blog SEO, whitepaper, atau newsletter yang berdasar data nyata — lengkap dengan
kutipan yang bisa ditelusuri ulang, bukan angka karangan AI.**

Diuji AI penguji independen di OpenClaw: 7 → 9 dari 10 pada artikel berbasis data resmi (sumber resmi benar-benar dibuka dan dikutip bernomor, klaim tanpa data ditandai `[perlu sumber]`; tanpa skill, artikel hanya bersandar pada 1 sumber tanpa kutipan bernomor).

> **Yang Anda butuhkan:** AI agent yang mendukung skill (OpenClaw, Claude Code, Codex, atau Cursor — langganan AI-nya ditanggung sendiri) di komputer Windows/Mac/Linux. Python 3 (bawaan Mac/Linux, unduh gratis di Windows) untuk skrip hitung; tanpa Python skill tetap berjalan dengan hitungan oleh AI. Tidak perlu API key atau akun tambahan dari Komunitech.

## Manfaat
- ✅ Angka dan klaim penting diberi kutipan `[1][2]` yang menunjuk sumber yang benar-benar dibuka; yang belum ketemu sumbernya ditandai `[perlu sumber]`, bukan diisi angka karangan. Tetap baca ulang sebelum terbit.
- ✅ Prioritas sumber resmi Indonesia (BPS, kementerian, OJK/BI, jurnal ilmiah di portal SINTA/Garuda) sudah disiapkan.
- ✅ Struktur SEO dasar (SEO = agar artikel mudah ditemukan di Google): judul, meta description (ringkasan yang tampil di hasil pencarian), sub-judul H2/H3, dan kata kunci langsung terpasang untuk artikel web.
- ✅ Ada pemeriksa kutipan otomatis (`cek_sitasi.py`) yang membantu menangkap kutipan bolong atau URL duplikat.
- ✅ Menolak dengan sopan bila diminta menulis tugas kuliah untuk diserahkan sebagai karya sendiri, lalu menawarkan kerangka, daftar sumber, atau penyuntingan tulisan Anda sendiri.

## Cocok untuk siapa
- Konsultan/profesional yang perlu artikel yang menunjukkan keahlian (thought leadership) untuk website atau LinkedIn.
- Pemilik UMKM/usaha yang ingin konten blog SEO tapi tidak sempat riset sendiri.
- Dosen/guru yang menyiapkan materi presentasi atau newsletter berbasis data terkini.
- Tim marketing/humas yang butuh whitepaper (laporan panduan mendalam) atau newsletter (kabar berkala lewat email) rutin yang terlihat kredibel.

## Contoh sebelum & sesudah
**Sebelum:** minta AI biasa "tulis artikel tentang tren UMKM digital" → dapat artikel lancar tapi
angka-angkanya sering terdengar meyakinkan padahal tidak jelas dari mana, dan tidak ada cara
membuktikannya ke pembaca.

**Sesudah (cukup ketik):** "Tolong tulisin artikel blog sekitar 800 kata buat website konsultan bisnis saya soal manfaat QRIS buat UMKM, pakai data resmi Bank Indonesia ya, jangan ngarang angka. Langsung jadi aja ya."

Cuplikan artikel (dipotong; dari `examples/00-openclaw-sebelum-sesudah.md`):
```
# Manfaat QRIS bagi UMKM: Apa Kata Data Resmi Bank Indonesia
Meta description: Data terbaru Bank Indonesia menunjukkan QRIS makin dipakai UMKM. Simak manfaat, biaya, dan cara memulainya untuk bisnis Anda.
…
Di sisi merchant, QRIS kini menjangkau 44,86 juta pedagang, dan 96,68% darinya adalah pelaku UMKM [1]. …
BI menetapkan Merchant Discount Rate (MDR) — biaya yang dibebankan ke merchant, bukan ke pembeli — sebesar 0% untuk Usaha Mikro (UMI) pada transaksi hingga Rp500.000, dan 0,3% untuk transaksi di atas itu [4]. …
[perlu sumber: data resmi mengenai dampak langsung QRIS terhadap kenaikan omzet UMKM secara spesifik belum ditemukan di sumber yang dibuka untuk artikel ini — …]

Daftar Pustaka
[4] MDR QRIS Bagi Merchant: Kategorisasi dan Simulasi. Bank Indonesia. Kebijakan tarif efektif 15 Maret 2025. https://www.bi.go.id/id/publikasi/ruang-media/cerita-bi/Pages/mdr-qris.aspx. Diakses 1 Oktober 2026.
```

## Cara pakai
Setelah terpasang, cukup ketik permintaan biasa ke AI agent Anda, misalnya:
- "Tulis artikel SEO tentang cara memilih supplier lokal, untuk blog toko online saya"
- "Buatin whitepaper singkat soal peluang bisnis franchise makanan 2026"
- "Newsletter bulanan buat klien konsultan pajak, bahas aturan terbaru"
- "Materi presentasi seminar literasi keuangan untuk UMKM, pakai data resmi"

## Instalasi singkat
Salin folder `asisten-tulis-riset` ke folder skills AI agent Anda:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |

Panduan lengkap (termasuk Windows): lihat `docs/instalasi.md` (di dalam paket bernama `CARA-INSTAL.md`).

**Hasil uji (jujur):** satu sumber, skor 1–10.
- **Uji OpenClaw, uji otomatis agent** (angka dari `examples/00-openclaw-sebelum-sesudah.md`): artikel blog QRIS dengan data resmi Bank Indonesia: nilai 7 tanpa skill menjadi 9 dengan skill. Tanpa skill, artikel hanya bersandar pada 1 sumber tanpa kutipan bernomor dan tanpa meta description; dengan skill ada 4 sumber resmi yang benar-benar dibuka, kutipan `[1]`-`[4]`, meta description siap tempel, dan klaim tanpa data ditandai `[perlu sumber]`. Uji ulang v1.0.5 pada permintaan esai tugas kuliah "biar tidak ketahuan AI": nilai 5 tanpa skill (menawarkan "versi draf utuh") menjadi 9 dengan skill, yang menolak lalu menawarkan kerangka, daftar sumber, dan umpan balik atas tulisan Anda sendiri; rata-rata dengan skill 8,9 dari 4 sesi, semuanya 8 ke atas. Catatan jujur: tanpa skill pun AI yang sama sudah mengambil angka resmi BI yang benar, pembedanya ada di ketertelusuran sumber.

**Status uji (jujur):** sudah diuji di OpenClaw (uji otomatis agent) dan Claude Code (simulasi agent); Codex dan Cursor belum diuji langsung (format skill-nya sama).

## FAQ
**Apakah AI-nya benar-benar mencari sumber sendiri, atau hanya mengarang?**
Bergantung pada AI agent yang Anda pakai: bila agent Anda punya kemampuan pencarian web, skill ini akan
memakainya dan hanya mengutip sumber yang benar-benar dibuka. Bila agent Anda tidak punya akses internet,
skill akan memberi tahu Anda secara jujur di awal dan menawarkan untuk menempelkan sumber/data sendiri, atau
membuat kerangka dengan tanda `[perlu sumber]` di bagian yang butuh data, tanpa mengarang angka (tetap periksa sebelum terbit).

**Bisa dipakai untuk tugas kuliah/skripsi?**
Tidak untuk tulisan yang akan diserahkan sebagai karya Anda sendiri — skill ini akan menolak dan
menawarkan bantuan mencari sumber atau menyunting draf yang sudah Anda tulis sendiri, agar tidak
melanggar aturan integritas akademik kampus.

**Gaya kutipannya bisa diubah ke format akademik (APA, gaya daftar pustaka yang lazim di kampus)?**
Bisa. Defaultnya gaya sederhana `[1]` `[2]` yang mudah dibaca orang awam; tinggal minta "pakai gaya APA"
untuk tulisan yang lebih formal/akademik.

## Riwayat perubahan

Versi terkini: **1.0.6**. Rincian teknis tiap versi ada di `CHANGELOG.md` di folder skill ini.
