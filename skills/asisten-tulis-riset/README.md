# Artikel Berbasis Riset, Tanpa Karangan

**Tulis artikel, blog SEO, whitepaper, atau newsletter yang berdasar data nyata — lengkap dengan
kutipan yang bisa ditelusuri ulang, bukan angka karangan AI.**

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

Panduan lengkap (termasuk Windows): lihat `CARA-INSTAL.md` di dalam paket.

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

## Catatan revisi 1.0.4 (2026-10-01)
dari uji ulang OpenClaw: skill kini ikut terbaca saat pengguna minta "bikinin esai/tugas kuliah/makalah/skripsi" (pemicu di deskripsi) dan aturan integritas akademik dipertegas: hanya kerangka, sumber, umpan balik, dan parafrase berkutipan; tidak menawarkan draf utuh untuk "ditulis ulang/dibumbui". Setiap angka/fakta, termasuk perbandingan biaya (mis. tarif EDC), wajib berkutipan [n] atau [perlu sumber]; `cek_sitasi.py` dijalankan dan ringkasannya ditampilkan.
