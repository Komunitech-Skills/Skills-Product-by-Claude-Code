# Ringkas Grup WA, Tahu Mana yang Perlu Dibalas

**Kirim ekspor chat grup, dalam semenit tahu mana yang perlu ditanggapi — tanpa scroll ratusan pesan.**

*Diuji AI penguji independen: 7,5 → 8 dari 10 di OpenClaw (8,5 pada v1.0.4 setelah perbaikan dan uji ulang; selisih skor kecil); pembedanya: ringkasan dengan skill memuat kutipan asli, jam, dan tabel tugas siapa-kapan, sedangkan tanpa skill berupa narasi dengan satu kutipan tanpa jam dan tanpa tabel tugas.*

> **Yang Anda butuhkan:** AI agent yang mendukung skill (OpenClaw, Claude Code, Codex, atau Cursor — langganan AI-nya ditanggung sendiri) di komputer Windows/Mac/Linux. Python 3 (bawaan Mac/Linux, unduh gratis di Windows) untuk menjalankan skrip pendukung skill ini; tanpa Python skill tetap berjalan, AI mengerjakannya langsung tetapi hasil angka sebaiknya Anda cek ulang. Tidak perlu API key atau akun tambahan dari Komunitech.

## Manfaat
- ✅ Memilah otomatis: **Perlu Perhatian** (pertanyaan ke Anda, keputusan, tenggat, uang, komplain) vs **Info** vs **Obrolan**.
- ✅ **Daftar tindakan** siap tindak lanjut: siapa mengerjakan apa, kapan tenggatnya.
- ✅ **Kutipan asli + jam** untuk tiap poin penting, jadi mudah dicek langsung di grup — poin yang dirangkum merujuk ke pesan aslinya, bukan dikarang. Grup ramai (ratusan pesan/hari)? Otomatis dipilah **per hari**.
- ✅ Bisa **menyamarkan nama & nomor** anggota kalau isinya sensitif, sebelum diproses AI (upaya terbaik — AI agent Anda akan menyebutkan bila ada kata yang perlu dicek manual sebelum dibagikan).
- ✅ Memakai fitur **ekspor chat resmi WhatsApp** — tanpa nomor bot, sehingga risiko nomor diblokir jauh lebih kecil, dan tidak ada yang "mendengar" grup Anda diam-diam.

## Cocok untuk siapa
- Pemilik usaha/tim yang ikut banyak grup kerja, proyek, atau komunitas dan sering ketinggalan info penting.
- Ketua RT/komunitas/organisasi yang perlu ringkasan diskusi grup untuk rapat berikutnya.
- Siapa pun yang baru buka HP setelah lama offline dan grup sudah ratusan pesan.

**Bukan untuk:** memantau chat/grup orang lain tanpa izin mereka (mis. menyadap karyawan atau pasangan) — skill ini menolak permintaan seperti itu.

## Contoh sebelum & sesudah
**Sebelum:** scroll manual 200+ pesan grup toko, khawatir kelewat pertanyaan penting soal pembayaran supplier atau perubahan harga.

**Sesudah (cukup ketik):** "Ringkas grup Renovasi Toko Nanda ini, aku Pak Nanda, tolong yang perlu aku tanggapi apa aja." (sambil melampirkan file ekspor chat)
→ Dalam beberapa detik: daftar hal yang butuh keputusan Anda lengkap dengan kutipan dan jam, daftar tugas siapa-kapan, dan sisanya dihitung sebagai info/obrolan. Cuplikan nyata dari uji (data fiktif):
```
📋 RINGKASAN GRUP: Renovasi Toko Nanda
…
── 12 Sep 2026 (63 pesan) ──
🔴 PERLU PERHATIAN (6)
1. [11.00] Sari: "@Pak Nanda invoice semen dan keramik dari Fajar totalnya Rp 12.500.000 udah
   termasuk ongkir, boleh langsung dibayar?"
   → dijawab Anda (13.00): transfer DP 50% dulu, Rp 6.250.000, sisanya saat barang sampai lengkap.
   Sudah dieksekusi Sari (15.30, DP terkirim).
…
3. [17.30] Sari: "@Pak Nanda sisa pembayaran ke Fajar Rp 6.250.000, ditransfer sekarang atau
   nanti pas toko buka Senin pak?"
   → ⚠️ belum ada jawaban dari Anda di file ini — yang menjawab "gpp kalau mau nyusul senin juga
   aman" (17.35) adalah Fajar sendiri, bukan keputusan Anda. Perlu ditegaskan kapan sisa
   Rp 6.250.000 ini benar-benar ditransfer.
```

## Cara pakai

### 1. Ekspor chat dari WhatsApp (sekali per ringkasan, ±30 detik)

**Di Android:**
1. Buka grup WA yang mau diringkas.
2. Ketuk ⋮ (titik tiga di pojok kanan atas) → **Lainnya** → **Ekspor chat**.
3. Pilih **"Tanpa Media"** (lebih cepat & filenya kecil).
4. Kirim file `.zip`/`.txt` yang muncul ke chat AI agent Anda, atau simpan ke folder yang bisa diakses AI agent (mis. folder Unduhan).

**Di iPhone:**
1. Buka grup WA yang mau diringkas.
2. Ketuk nama grup di atas → gulir ke bawah → **Ekspor Chat**.
3. Pilih **"Tanpa Media"**.
4. Pilih cara kirim (mis. simpan ke Files, kirim ke email/AirDrop ke komputer, atau ke chat AI agent Anda bila didukung).

### 2. Minta diringkas

Cukup ketik ke AI agent Anda, misalnya:
- "Ringkas grup ini, yang perlu saya tanggapi aja."
- "Rekap grup kerja 3 hari terakhir."
- "Apa yang saya lewatkan di grup sejak kemarin jam 5 sore?"

Kalau grup sangat sensitif (ada anggota keluarga/pelanggan/pasien), tambahkan: "samarkan nama anggotanya" — nama & nomor akan diganti "Anggota 1, Anggota 2, ..." sebelum diproses.

## Instalasi singkat
Salin folder `ringkas-grup-wa` ke folder skills AI agent Anda:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex (belum diuji langsung) | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor (belum diuji langsung) | `~/.cursor/skills/` |

Panduan lengkap (termasuk Windows): lihat `CARA-INSTAL.md` di dalam paket.

**Hasil uji (angka nyata):** uji banding tanpa vs dengan skill oleh agen penguji independen (simulasi Claude Code; grup renovasi toko, 99 pesan; sumber: `examples/00-pembanding-tanpa-skill.md` dan `examples/HASIL-UJI.md`).
- Tanpa skill: ringkasan berupa narasi; nominal dibulatkan ("Rp 12 jutaan"), tanpa kutipan atau jam, dan keliru menyimpulkan "keputusan sudah diambil" / "sisanya menyusul" padahal pemilik belum menjawab (sisa pembayaran Rp 6.250.000 dan budget material masih menggantung).
- Dengan skill: 11 butir Perlu Perhatian dengan kutipan asli + jam, tabel tugas siapa-kapan, statistik dihitung script (program kecil), dan 2 hal yang belum dijawab pemilik ditandai ⚠️ "belum ada jawaban dari Anda".
- Skor akhir penguji independen (v1.0.1): 8 dari 10; 68 dari 68 uji otomatis bawaan lulus.
- Sumber lain, uji OpenClaw 2026-10-01 (agen penguji independen): 7,5 → 8 (8,5 pada v1.0.4 setelah perbaikan dan uji ulang; selisih kecil) (lihat `examples/00-openclaw-sebelum-sesudah.md`). Perbaikan 1.0.5 dan 1.0.6 belum tercatat diuji ulang di OpenClaw.

**Status uji (jujur):** sudah diuji di OpenClaw (uji otomatis oleh agen AI, bukan oleh manusia) dan Claude Code (simulasi agen penguji). Codex dan Cursor memakai format SKILL.md yang sama, tetapi belum kami uji langsung.

## FAQ

**Apakah skill ini bisa memantau grup secara langsung/otomatis, bukan cuma dari file ekspor?**
Bisa, tapi itu jalur terpisah yang lebih rumit (bot dengan nomor WhatsApp khusus ikut masuk ke grup) dan **wajib** diberitahukan ke anggota grup. Jalur file ekspor (bawaan skill ini) jauh lebih sederhana, dengan risiko nomor diblokir jauh lebih kecil, dan cocok untuk hampir semua kebutuhan. Tanyakan ke AI agent Anda kalau memang butuh mode langsung — ada panduannya, tapi disarankan hanya untuk pengguna yang sudah nyaman dengan konfigurasi teknis atau lewat jasa pendampingan.

**Apakah isi chat saya dikirim ke server Komunitech?**
Tidak. Skill ini berjalan di komputer/AI agent Anda sendiri. File ekspor diproses secara lokal oleh program kecil (script Python), lalu ringkasannya diproses oleh penyedia AI yang Anda pakai (mis. Anthropic/OpenAI) — sama seperti percakapan biasa dengan AI agent Anda.

**Kalau grup sangat aktif (ribuan pesan sebulan), apakah tetap bisa dipakai?**
Bisa. Minta rentang waktu tertentu (mis. "3 hari terakhir" atau "sejak kemarin sore") supaya hasilnya tetap ringkas dan relevan; untuk grup sangat ramai, hasil otomatis dipecah per hari.

## Riwayat perubahan

Versi terkini: **1.0.6**. Rincian teknis tiap versi ada di `CHANGELOG.md` di folder skill ini.
