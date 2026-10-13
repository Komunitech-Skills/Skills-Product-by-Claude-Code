# Artikel Berbasis Riset, Tanpa Karangan

**Tulis artikel, blog SEO, whitepaper, atau newsletter yang berdasar data nyata — lengkap dengan
kutipan yang bisa ditelusuri ulang, bukan angka karangan AI.**

> **Yang Anda butuhkan:** AI agent yang mendukung skill (OpenClaw, Claude Code, Codex, atau Cursor — langganan AI-nya ditanggung sendiri) di komputer Windows/Mac/Linux. Python 3 (bawaan Mac/Linux, unduh gratis di Windows) untuk skrip hitung; tanpa Python skill tetap berjalan dengan hitungan oleh AI. Tidak perlu API key atau akun tambahan dari Komunitech.

## Manfaat
- ✅ Setiap angka dan klaim diberi kutipan `[1][2]` yang menunjuk sumber nyata — bukan halusinasi AI.
- ✅ Prioritas sumber resmi Indonesia (BPS, kementerian, OJK/BI, jurnal SINTA/Garuda) sudah disiapkan.
- ✅ Struktur SEO dasar (judul, meta description, H2/H3, kata kunci) langsung terpasang untuk artikel web.
- ✅ Ada pengecekan otomatis (`cek_sitasi.py`) yang menangkap kutipan bolong atau URL duplikat.
- ✅ Menolak dengan sopan bila diminta menulis tugas kuliah untuk diserahkan sebagai karya sendiri —
  aman dari masalah integritas akademik.

## Cocok untuk siapa
- Konsultan/profesional yang perlu artikel thought-leadership untuk website atau LinkedIn.
- Pemilik UMKM/usaha yang ingin konten blog SEO tapi tidak sempat riset sendiri.
- Dosen/guru yang menyiapkan materi presentasi atau newsletter berbasis data terkini.
- Tim marketing/humas yang butuh whitepaper atau newsletter rutin yang terlihat kredibel.

## Contoh sebelum & sesudah
**Sebelum:** minta AI biasa "tulis artikel tentang tren UMKM digital" → dapat artikel lancar tapi
angka-angkanya sering terdengar meyakinkan padahal tidak jelas dari mana, dan tidak ada cara
membuktikannya ke pembaca.

**Sesudah (cukup ketik):** "Tulis artikel blog 800 kata soal tren belanja online UMKM Indonesia 2026,
untuk website konsultan saya, ada datanya ya."
→ Artikel lengkap dengan sub-judul H2/H3, kutipan `[1]` `[2]` di tiap klaim penting, dan Daftar Pustaka
di bagian bawah berisi judul-lembaga-tahun-URL-tanggal akses. Bagian yang belum ketemu sumbernya ditandai
jelas `[perlu sumber]`, tidak diisi angka karangan.

**Hasil uji (OpenClaw, uji otomatis agent):** artikel blog QRIS dengan data resmi Bank Indonesia: nilai 7 tanpa skill menjadi 9 dengan skill. Tanpa skill, artikel hanya bersandar pada 1 sumber tanpa kutipan bernomor dan tanpa meta description; dengan skill ada 4 sumber resmi yang benar-benar dibuka, kutipan `[1]`-`[4]`, meta description siap tempel, dan klaim tanpa data ditandai `[perlu sumber]`. Uji ulang v1.0.5 pada permintaan esai tugas kuliah "biar tidak ketahuan AI": nilai 5 tanpa skill (menawarkan "versi draf utuh") menjadi 9 dengan skill, yang menolak lalu menawarkan kerangka, daftar sumber, dan umpan balik atas tulisanmu sendiri; rata-rata dengan skill 8,9 dari 4 sesi, semuanya 8 ke atas. Catatan jujur: tanpa skill pun AI yang sama sudah mengambil angka resmi BI yang benar, pembedanya ada di ketertelusuran sumber. Rincian: `examples/00-openclaw-sebelum-sesudah.md`. Claude Code diuji lewat simulasi agent; Codex dan Cursor belum diuji langsung (format skill-nya sama).

## Cara pakai
Setelah terpasang, cukup ketik permintaan biasa ke AI agent kamu, misalnya:
- "Tulis artikel SEO tentang cara memilih supplier lokal, untuk blog toko online saya"
- "Buatin whitepaper singkat soal peluang bisnis franchise makanan 2026"
- "Newsletter bulanan buat klien konsultan pajak, bahas aturan terbaru"
- "Materi presentasi seminar literasi keuangan untuk UMKM, pakai data resmi"

## Instalasi singkat
Salin folder `asisten-tulis-riset` ke folder skills AI agent kamu:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |

Panduan lengkap (termasuk Windows): lihat `docs/instalasi.md` (di dalam paket bernama `CARA-INSTAL.md`).

## FAQ
**Apakah AI-nya benar-benar mencari sumber sendiri, atau hanya mengarang?**
Bergantung pada AI agent yang kamu pakai: bila agentmu punya kemampuan pencarian web, skill ini akan
memakainya dan hanya mengutip sumber yang benar-benar dibuka. Bila agentmu tidak punya akses internet,
skill akan memberitahumu secara jujur di awal dan menawarkan kamu menempelkan sumber/data sendiri, atau
membuat kerangka dengan tanda `[perlu sumber]` di bagian yang butuh data — tidak pernah mengarang angka.

**Bisa dipakai untuk tugas kuliah/skripsi?**
Tidak untuk tulisan yang akan diserahkan sebagai karya kamu sendiri — skill ini akan menolak dan
menawarkan bantuan mencari sumber atau menyunting draf yang sudah kamu tulis sendiri, agar tidak
melanggar aturan integritas akademik kampus.

**Gaya kutipannya bisa diubah ke format akademik (APA)?**
Bisa. Defaultnya gaya sederhana `[1]` `[2]` yang mudah dibaca orang awam; tinggal minta "pakai gaya APA"
untuk tulisan yang lebih formal/akademik.

## Riwayat perubahan

Versi terkini: **1.0.5**. Rincian teknis tiap versi ada di `CHANGELOG.md` di folder skill ini.
