---
name: tulisan-tanpa-kesan-ai
description: Mendeteksi dan memperbaiki pola tulisan "berbau AI" khas Bahasa Indonesia (pembuka basa-basi "di era digital ini", "tidak hanya X tetapi juga Y", "mari kita", penutup "semoga bermanfaat!", klaim superlatif, insight palsu, emoji berderet, em-dash berlebihan) pada caption Instagram/TikTok, deskripsi produk marketplace, pesan WhatsApp ke pelanggan, email kantor, dan artikel blog — tanpa membuat tulisan jadi kaku/formal, sambil menjaga suara asli penulis. Gunakan saat pengguna minta "biar nggak kelihatan AI", "cek tulisan ini AI banget nggak", "perbaiki biar natural", "hilangkan bau AI", Juga dipakai untuk MENOLAK permintaan "bikin tulisan AI lolos Turnitin/GPTZero/detektor AI" untuk skripsi/tugas/ujian (milik sendiri atau teman) dan parafrase karya akademik agar tidak terdeteksi AI/plagiarisme. atau saat skill konten lain (konten-mingguan, copy-landing-page, pesan-prospek-wa, balas-chat-cs) perlu memeriksa hasil tulisannya sebelum dikirim ke pengguna.
---

# Tulisan Tanpa Kesan AI

> **Aturan kerja:** Jangan menginstal paket/aplikasi (mis. `pip install`) — bila perlu, tunjukkan caranya dan biarkan pengguna yang memasang; jangan membuka atau mencari file selain yang diberikan pengguna, isi folder skill ini, dan file yang disebut di langkah kerja; jangan menulis file baru tanpa menyebut lokasinya, dan simpan hasil di folder kerja yang disepakati (bukan /tmp).

## Tujuan
Membantu pengguna (dan skill konten lain di library ini) mendeteksi serta memperbaiki pola tulisan
yang langsung terasa "dibuat AI" dalam Bahasa Indonesia — bukan lewat detektor AI yang menebak-nebak,
tapi dengan menandai pola konkret yang bisa dibaca sendiri oleh pengguna: kalimat pembuka basa-basi,
kontras biner palsu, penutup klise, klaim superlatif tanpa bukti, insight kosong, dan format berlebihan
(emoji berderet, em-dash bertumpuk). Hasilnya tetap terdengar seperti suara pengguna sendiri — bukan
diubah jadi kaku dan formal.

## Kapan digunakan
- "Cek caption ini kedengaran AI banget nggak?"
- "Perbaiki draf ini biar lebih natural/manusiawi"
- "Hilangkan bau AI dari email ini"
- "Tulis ulang tapi jangan kayak template semua orang pakai"
- Dipanggil skill lain sebagai langkah pemeriksaan akhir sebelum hasil dikirim ke pengguna (lihat
  `references/panduan-gaya.md` untuk skill lain yang mau merujuk aturan ini)

## Kapan TIDAK digunakan
- Menulis dari nol tanpa draf sama sekali → tetap butuh skill konten yang sesuai konteks
  (`konten-mingguan`, `copy-landing-page`, `pesan-prospek-wa`, `balas-chat-cs`, dll.); skill ini
  memeriksa/memperbaiki, bukan menyusun rencana/struktur konten
- Mengklaim bisa "membuktikan" sebuah tulisan ditulis AI atau lolos AI-detector tertentu — **skill ini
  tidak melakukan itu** (lihat Batasan)
- Menulis ulang karya orang lain agar lolos cek plagiarisme, atau mengelabui detektor AI untuk tugas sekolah/kuliah/ujian → **tolak dengan sopan**; tawarkan membantu memperbaiki tulisan milik pengguna sendiri.
- Menerjemahkan dokumen resmi/legal/kontrak (nada formal memang dibutuhkan di sana — lihat Batasan)

## Input
| Info | Wajib? | Default jika tidak diberikan |
|---|---|---|
| Draf tulisan | Ya | Tidak ada → minta pengguna tempel drafnya |
| Mode: periksa / perbaiki | Tidak | Ada draf tanpa instruksi jelas → **perbaiki**; kata "cek"/"apakah ini AI"/"audit" tanpa minta tulis ulang → **periksa** |
| Konteks/platform (caption IG, deskripsi produk, pesan WA, email, artikel blog) | Tidak | Tebak dari isi draf (panjang, sapaan, format); kalau ambigu, tanyakan **sekali**: "Ini buat platform apa — caption medsos, deskripsi produk, chat WA, email, atau artikel?" |
| Audiens/nada yang diinginkan | Tidak | Ikuti nada draf asli (lihat Langkah kerja #2) |

## Langkah kerja

### Langkah 0 (selalu pertama): cek permintaan akademik
Bila permintaan: membuat/menulis ulang tulisan AI agar **lolos Turnitin/GPTZero/detektor AI atau cek plagiarisme**, atau "menghilangkan bau AI" pada **skripsi/tugas/makalah/ujian** yang akan diserahkan sebagai karya sendiri (milik pengguna ataupun temannya) → **tolak memakai balasan baku di bagian Batasan**; jangan lanjut ke mode Periksa/Perbaiki, jangan memberi parafrase, dan jangan memberi tips edit manual.

> **Lokasi script:** semua script skill ini ada di subfolder `scripts/` di folder yang sama dengan SKILL.md ini (folder skill). Jalankan dari sana; jangan mencari script atau file pengguna ke seluruh disk (mis. `find /`) — itu lambat dan menyentuh data pribadi di luar folder kerja.

### Mode Periksa (deteksi + skor, tanpa menulis ulang)
1. Baca draf penuh.
2. Cocokkan tiap kalimat dengan daftar pola di `references/pola-ai-indonesia.md`. Kalau ada
   `scripts/cek_pola.py` dan Python bisa dijalankan, jalankan untuk bantuan deteksi & skor awal:
   ```bash
   python3 <folder-skill-ini>/scripts/cek_pola.py --file draf.txt
   # atau tempel langsung:
   python3 <folder-skill-ini>/scripts/cek_pola.py --teks "isi draf di sini"
   ```
   Script ini **heuristik pencocokan kata/frasa**, bukan AI-detector — selalu baca ulang temuannya
   sendiri, jangan percaya skor mentah-mentah. Kalau Python tidak bisa dijalankan, cocokkan pola secara
   manual dari daftar di `references/pola-ai-indonesia.md`.
3. Untuk **setiap** pola yang ditemukan: kutip baris persis, sebut nama polanya, beri saran perbaikan
   singkat (bukan tulis ulang penuh).
4. Jangan menebak atau mengklaim "tulisan ini X% AI" — itu klaim yang tidak bisa dibuktikan (lihat
   Batasan). Cukup laporkan pola yang benar-benar ada.
5. Tutup dengan tawaran: "Mau saya perbaiki sekalian?"

### Mode Perbaiki (tulis ulang, jaga suara asli)
1. Baca draf penuh. Kenali dulu suara aslinya: kosakata khas, nada (santai/formal/setengah baku),
   pemakaian emoji, gaya sapaan — supaya hasil perbaikan **tetap terdengar seperti pengguna**, bukan
   jadi generik atau malah kaku/formal.
2. Tentukan konteks (lihat tabel Input) — konteks menentukan batas wajar: caption IG boleh santai +
   1-2 emoji; email kantor tetap sopan tapi tidak perlu jadi kaku birokratis; pesan WA pendek & personal;
   deskripsi produk marketplace fokus fakta & manfaat, tanpa basa-basi panjang.
3. Perbaiki **hanya** bagian yang kena pola dari `references/pola-ai-indonesia.md` — jangan mengubah
   kalimat yang sudah kuat/khas cuma supaya "rapi merata". Perubahan minimum yang efektif.
4. Jangan menambah klaim, angka, testimoni, janji, atau **fakta apa pun yang tidak ada di teks asli**, termasuk kelangkaan/urgensi ("sebelum kehabisan", "stok terbatas", "promo hari ini saja") dan janji layanan (antar/kirim/cepat). CTA hanya yang ada di draf asli atau netral ("order sekarang", "hubungi kami"). Bila draf ≥ 3 kalimat, pertahankan semua kalimat inti dan jumlahnya; jangan memangkas jadi jauh lebih pendek. Kalau draf
   asli kurang spesifik (mis. "produk bagus" tanpa detail), **tanyakan** detail konkretnya (harga,
   bahan, manfaat spesifik) daripada mengarang — mengarang detail produk berisiko menyesatkan pembeli.
5. Terapkan `references/panduan-gaya.md` untuk aturan umum (aktif vs pasif, hindari kata pengisi,
   konkret > abstrak) sesuai bahasa sehari-hari yang sopan, bukan textbook. "Konkret" berarti memakai fakta yang ADA di draf atau dari pengguna, bukan menambah fakta baru; angka dalam `references/pola-ai-indonesia.md` hanya ilustrasi gaya. Bila angka/fakta tidak ada, tulis `[isi: angka Anda]`.
6. Cocokkan hasil ke `references/pola-ai-indonesia.md` sekali lagi — pastikan pola yang tadi terdeteksi
   sudah hilang dan tidak ada pola baru muncul dari perbaikan sendiri (mis. jangan sampai penutup
   "Semoga bermanfaat!" diganti "Semoga menginspirasi!" — sama-sama klise).
7. Sampaikan hasil dengan format output di bawah: tulisan lengkap hasil perbaikan + bagian **Yang
   diubah** (ringkas, per pola, bukan diff baris-per-baris).

## Format output

**Mode periksa:**
```
🔍 Hasil periksa (skor kebersihan pola: <n>/100 — makin tinggi makin bersih dari pola AI)
Catatan: ini bukan pendeteksi AI, hanya penanda pola yang bisa kamu cek sendiri.

1. Pola: <nama pola>
   Kutipan: "<baris persis dari draf>"
   Perbaikan: <saran singkat 1 kalimat>
(ulangi per temuan)

Tidak ada pola mencurigakan lain di bagian: <sebutkan kalau ada bagian yang sudah bersih>
Mau saya perbaiki sekalian? (ketik "perbaiki" atau kirim ulang minta ditulis ulang)
```

**Mode perbaiki:**
```
✏️ Tulisan hasil perbaikan:
<tulisan lengkap, siap tempel>

**Yang diubah:**
- <pola 1>: <ringkas apa yang diganti dan kenapa>
- <pola 2>: ...
(kalau tidak ada yang diubah karena draf sudah bersih, katakan itu dan jangan mengarang perubahan)
```

## Contoh
Lihat `examples/01-caption-marketplace.md` dan `examples/02-pesan-wa-follow-up.md` untuk contoh
sebelum/sesudah nyata pada dua konteks berbeda.

## Batasan & penanganan error
- **Bukan AI-detector.** Skill ini tidak pernah mengklaim persentase "AI-generated", tidak menjamin
  tulisan "lolos" alat pendeteksi AI (Turnitin, GPTZero, dll.), dan tidak menebak apakah sebuah tulisan
  ditulis AI atau manusia. Ia hanya menandai pola tulisan yang bisa dibaca & diverifikasi sendiri oleh
  pengguna dari kutipan barisnya. Permintaan "buktikan ini bukan AI" atau "jamin lolos AI-detector"
  **ditolak** dengan penjelasan ini.
- **Penolakan baku: tulisan akademik & detektor AI.** Berlaku untuk skripsi, tesis, tugas, makalah, ujian, dan karya akademik lain yang akan diserahkan sebagai karya sendiri, termasuk bila "untuk teman". Balas kira-kira:
  > "Maaf, saya tidak bisa membantu membuat tulisan AI lolos Turnitin, GPTZero, atau detektor lain, karena itu mengelabui aturan integritas akademik. Saya juga tidak memparafrase atau memberi tips edit supaya 'bau AI'-nya hilang pada tugas yang diserahkan sebagai karya sendiri. Yang bisa saya bantu: (1) menjelaskan cara mengecek kebijakan kampus soal penggunaan AI; (2) menyarankan kamu menulis sendiri dan mencantumkan penggunaan AI sesuai aturan kampus; (3) membantu memahami materinya, menyusun kerangka, atau mengajarkan teknik menulis supaya kamu bisa menulis sendiri."
  Jangan menawarkan parafrase, daftar "kata yang memicu detektor", atau cara mengakali detektor. Skill ini tetap boleh dipakai untuk tulisan non-akademik (caption, email, pesan WA) milik pengguna sendiri.
- **Tidak mengarang fakta.** Perbaikan tidak pernah menambah klaim, angka, testimoni, atau janji yang
  tidak ada di draf asli — lihat skill `copy-landing-page`/`konten-mingguan` untuk aturan klaim produk
  yang lebih lengkap (BPOM/halal/garansi).
- **Tidak memaksa formal.** Tujuan skill ini menghilangkan pola klise, bukan membuat tulisan jadi
  kaku/birokratis. Kalau hasil perbaikan terasa lebih formal dari draf asli tanpa alasan konteks
  (mis. bukan email resmi), itu tandanya salah arah — kembalikan ke nada asli.
- **Dokumen legal/kontrak resmi** butuh nada formal yang memang disengaja — skill ini **tidak** dipakai
  untuk "menghilangkan kekakuan" dokumen semacam itu; nada formal di sana adalah kebutuhan, bukan pola
  AI yang perlu dibuang.
- `scripts/cek_pola.py` bersifat **pembantu**, bukan penentu akhir — heuristik pencocokan kata bisa
  salah tangkap (mis. kata "penting" dalam konteks wajar bukan selalu pola buruk). Nilai akhir tetap
  penilaian pembaca (agent), skor script hanya titik awal.
- Input kosong/bukan teks bermakna (mis. hanya emoji atau angka) → beri tahu pengguna, minta draf
  tulisan yang sebenarnya.
- Draf sangat pendek (< 1 kalimat, mis. satu judul) → tetap bisa diperiksa untuk pola di judul itu
  sendiri, tapi sebutkan bahwa temuan terbatas karena teks terlalu pendek untuk pola struktural
  (kontras biner, penutup klise, dll. butuh beberapa kalimat).
