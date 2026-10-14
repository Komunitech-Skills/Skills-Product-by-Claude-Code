# 01 - Admin toko online + CS WhatsApp dari iklan lowongan berantakan

- **Jenis skenario:** normal utama (juga diuji di konteks kanal Telegram)
- **Diuji:** 2026-10-14, OpenClaw 2026.10.2 lokal, model router Komunitech (claude-sonnet-5), home berisi hanya skill ini. Penguji independen.
- **Nilai:** 8,5 (lokal), 8,0 (Telegram). Perbandingan lengkap dengan sisi tanpa skill: `00-openclaw-sebelum-sesudah.md`.

## Input (pesan pengguna, fiktif)

> tolong bikinin paket wawancara buat posisi ini ya, minggu depan ada 4 pelamar yg mau sy interview bareng adik sy. ini iklan yg sy pasang kemarin:
>
> DICARI SEGERA!!! ADMIN OL SHOP + CS WA
> Rumah Kerudung Alya - Bekasi Timur
> kriteria : wanita max 28thn, berpenampilan menarik, jujur,teliti,fast respon
> - bisa ms excel / google sheet
> - paham shopee & tiktok shop (proses pesanan,cetak resi,chat pembeli)
> - balas chat WA customer (sehari bisa 100an chat klo lg promo)
> - rekap orderan harian + stok
> - bikin laporan penjualan mingguan
> jam kerja senin-sabtu 08.00-16.00, kadang lembur pas campaign tgl kembar
> gaji UMR + bonus
> kirim CV ke WA 0812-xxxx-xxxx
>
> wawancaranya kira2 40 menit per org

## Output dengan skill (apa adanya)

> Siap, saya susun paket wawancaranya. Satu catatan dulu: kriteria "wanita, maks. 28 tahun, berpenampilan menarik" di iklan tidak saya pakai sebagai penilaian — itu syarat yang berisiko melanggar aturan ketenagakerjaan (lebih lanjut di bagian "Pertanyaan terlarang" di bawah), dan sebaiknya iklannya juga dirapikan lain waktu. Paket wawancaranya tetap saya buat lengkap di bawah ini.
>
> ## Ringkasan & Asumsi
> Posisi: **Admin Online Shop + CS WhatsApp** — Rumah Kerudung Alya. Asumsi: 2 pewawancara (Anda + adik), durasi **40 menit/kandidat** (sesuai permintaan), satu tahap wawancara (tidak berjenjang). 4 kandidat minggu depan — pakai pertanyaan dan urutan yang **sama persis** untuk semuanya.
>
> ## Kompetensi Inti
> 1. **K1 – Ketelitian memproses pesanan, stok & laporan** (30%, **kritis**) — memproses pesanan Shopee/TikTok Shop, merekap order & stok, serta membuat laporan penjualan dengan akurat.
> 2. **K2 – Kecepatan & kualitas respon chat pelanggan** (25%, **kritis**) — membalas chat WA dengan cepat, jelas, dan sopan meski volume tinggi saat promo.
> 3. **K3 – Penguasaan platform jualan online & alat kerja** (20%) — mengoperasikan Shopee Seller Center, TikTok Shop Seller Center, dan Excel/Google Sheet.
> 4. **K4 – Komunikasi tertulis yang jelas & profesional** (15%) — menulis balasan chat dan laporan dengan bahasa sopan dan mudah dipahami.
> 5. **K5 – Ketahanan kerja saat ramai** (10%) — tetap teliti dan responsif saat order/chat melonjak (misal kampanye tanggal kembar), termasuk kesediaan lembur.
>
> ## Alur Wawancara (40 menit)
> | Bagian | Menit | Isi |
> |---|---|---|
> | Pembuka & perkenalan | 4 | Sapa, jelaskan posisi & alur wawancara |
> | Tes praktik | 10 | Rekap pesanan (5 mnt) + balas chat WA (5 mnt) |
> | K1 | 4 | Perilaku + situasional |
> | K2 | 4 | Perilaku + situasional |
> | K3 | 4 | Perilaku + situasional |
> | K4 | 4 | Perilaku + situasional |
> | K5 | 4 | Perilaku + situasional |
> | Pertanyaan dari kandidat | 4 | Kandidat bertanya balik |
> | Penutup | 2 | Info tindak lanjut |
> | **Total** | **40** | |
>
> ## Bank Pertanyaan
>
> **K1 Ketelitian memproses pesanan, stok & laporan (30%, kritis)**
> Perilaku: "Ceritakan satu kali Anda memproses pesanan online (input data, cetak resi, atau rekap stok) dan menemukan data yang tidak cocok sebelum jadi masalah. Apa kejadiannya, apa yang Anda lakukan, dan bagaimana hasilnya?"
> Kuat: contoh konkret dengan angka selisih, langkah menelusuri (cek ulang sistem, cocokkan resi), melapor/koreksi hari itu juga. Lemah: "saya teliti kok" tanpa contoh, atau menyalahkan sistem/orang lain. Lanjut: "Berapa selisihnya, dan siapa yang Anda beri tahu?"
> Situasional: "Sore ini ada 45 pesanan Shopee dan 30 pesanan TikTok Shop yang harus diproses & dicetak resinya sebelum kurir jemput pukul 16.00, sementara chat pelanggan terus masuk. Apa yang Anda lakukan?" Kuat: memprioritaskan pesanan mendekati batas jemput, sistematis per platform, cek ulang sebelum ditutup. Lemah: asal cepat tanpa cek ulang, atau mengabaikan salah satu platform.
>
> **K2 Kecepatan & kualitas respon chat pelanggan (25%, kritis)**
> Perilaku: "Ceritakan satu kali Anda harus membalas banyak pesan pelanggan dalam waktu singkat. Bagaimana Anda mengaturnya, dan apa hasilnya?" Kuat: cara mengatur (urutan, template balasan, prioritas yang belum terjawab), angka (jumlah chat/waktu balas). Lemah: "saya cepat kok" tanpa cara, atau mengaku sering menunda chat. Lanjut: "Chat seperti apa yang Anda dahulukan, dan kenapa?"
> Situasional: "Saat promo, dalam satu jam masuk 60 chat WA: sebagian tanya stok, sebagian komplain paket belum sampai, ada yang marah karena belum dibalas 2 jam. Bagaimana urutan dan cara Anda membalas?" Kuat: mendahulukan yang sudah menunggu lama/komplain, jawab singkat-jelas dulu, minta maaf, tetap sopan. Lemah: template asal tanpa baca pertanyaan, abaikan yang marah, atau ikut emosi.
>
> **K3 Penguasaan platform jualan online & alat kerja (20%)**
> Perilaku: "Ceritakan pengalaman Anda memakai Shopee/TikTok Shop Seller Center atau Excel/Google Sheet untuk bekerja. Apa yang Anda kerjakan dan bagaimana caranya?" Kuat: fitur konkret (cetak resi massal, atur status pesanan, rumus SUM/VLOOKUP, filter). Lemah: "gampang kok" tanpa detail, atau belum pernah sama sekali tanpa usaha belajar. Lanjut: "Fitur atau rumus apa yang paling sering Anda pakai?"
> Situasional: "Anda diminta merekap 200 baris pesanan dari Shopee dan TikTok Shop yang formatnya berbeda ke satu sheet rekap harian. Apa langkah Anda sebelum menjumlahkan?" Kuat: menyeragamkan format, cek total per platform dulu, simpan salinan data asli. Lemah: langsung digabung tanpa pengecekan.
>
> **K4 Komunikasi tertulis yang jelas & profesional (15%)**
> Perilaku: "Ceritakan satu kali Anda harus menyampaikan kabar kurang enak ke pelanggan (barang kosong, pesanan terlambat). Apa yang Anda tulis/katakan?" Kuat: fakta apa adanya, minta maaf, beri solusi/alternatif, bahasa sopan. Lemah: menghindar, menyalahkan ekspedisi, atau janji tidak pasti. Lanjut: "Bisa dicontohkan kalimat yang Anda kirim?"
> Situasional: "Pelanggan chat: 'Kak, pesanan saya resi [isian: data fiktif] kok belum update 3 hari, gimana ini?' Tulis balasan Anda." Kuat: salam, minta maaf, akan dicek, beri perkiraan tindak lanjut tanpa janji pasti. Lemah: jawaban singkat tanpa empati, menyalahkan kurir tanpa solusi.
>
> **K5 Ketahanan kerja saat ramai (10%)**
> Perilaku: "Ceritakan pengalaman Anda bekerja di periode sangat sibuk (promo besar/deadline). Bagaimana Anda menjaga diri tetap teliti?" Kuat: cara menjaga ritme, tetap sabar, hasil tetap baik. Lemah: "saya kuat lembur" tanpa cara, atau mengaku sering emosi saat capek. Lanjut: "Apa yang Anda lakukan kalau sudah lelah tapi order masih menumpuk?"
> Situasional: "Saat kampanye tanggal kembar, order masuk 3x lipat dan Anda diminta lembur sampai malam, padahal jadwal pribadi hari itu padat. Apa yang Anda lakukan?" Kuat: mengabari lebih awal, tetap membantu semampunya, jujur soal keterbatasan waktu. Lemah: menghilang tanpa kabar, atau mengiyakan lalu tidak datang.
>
> ## Tes Praktik (10 menit, bahan contoh — diumumkan sebagai tes)
> **Bagian A (5 menit) – Rekap pesanan:** Beri data: "Shopee: 20 pesanan masuk, 2 dibatalkan pembeli. TikTok Shop: 12 pesanan, baru 10 resi tercetak. Stok 'Pashmina Plisket' tersisa 15 pcs menurut catatan, tapi pesanan hari ini untuk model itu 18 pcs." Tanyakan: (1) total pesanan yang perlu diproses hari ini, (2) apa yang dilakukan untuk 2 resi TikTok yang belum tercetak, (3) apa yang dilakukan untuk kekurangan stok 3 pcs.
> Kunci: (1) 18 + 12 = **30 pesanan**. (2) segera cetak sebelum batas jemput kurir, cek datanya dulu. (3) lapor ke atasan, tandai pesanan yang tak terpenuhi, hubungi pembeli untuk konfirmasi (ganti model/refund sebagian) sebelum dikirim — bukan asal kirim.
> **Bagian B (5 menit) – Balas chat:** pakai situasional K4 di atas.
> Penilaian: Bagian A menilai K1 & K3; Bagian B menilai K2 & K4. **Ganti angka tiap putaran** supaya jawaban tidak beredar antar kandidat.
>
> ## Rubrik Skor 1–5
> **K1:** 1=sering salah input/stok tanpa sadar. 2=jarang salah tapi tak terbiasa cek ulang. 3=benar, koreksi kecil, lapor bila ditemukan. 4=cepat & akurat, cek ulang sebelum laporan, lapor dengan angka pasti hari itu. 5=seperti 4 + punya cara sendiri cegah kesalahan berulang (terbukti mengurangi selisih).
> **K2:** 1=sering lambat/asal balas. 2=lambat saat chat menumpuk, mudah kewalahan. 3=tepat & sopan dalam waktu wajar. 4=cepat & tepat walau menumpuk, prioritas komplain, tetap sopan. 5=seperti 4 + punya cara kerja sendiri (template/pengelompokan) hingga waktu balas konsisten cepat.
> **K3:** 1=belum pernah pakai sama sekali, tak berniat belajar. 2=tahu dasar, perlu dituntun. 3=bisa proses pesanan & isi rekap dasar dengan sedikit arahan. 4=terbiasa fitur menengah tanpa diarahkan. 5=mahir & efisien di kedua platform + spreadsheet, bisa mengajari orang lain.
> **K4:** 1=balasan membingungkan/kasar/terlalu singkat. 2=sopan tapi kurang jelas/tak jawab inti. 3=jelas & sopan, jawab inti dengan benar. 4=jelas, sopan, empatik, beri solusi & perkiraan waktu. 5=seperti 4 + bahasa rapi konsisten, bisa menenangkan pelanggan kesal.
> **K5:** 1=mudah menyerah/emosi saat beban tinggi. 2=bertahan tapi kualitas menurun drastis. 3=tetap bekerja benar saat ramai meski perlu usaha lebih. 4=tetap teliti & ramah saat ramai, atur ritme sendiri. 5=seperti 4 + bisa bantu atur prioritas beban kerja, tenang meski lembur mendadak.
>
> ## Kartu Skor (isi sendiri-sendiri sebelum diskusi)
> | Kompetensi (bobot) | Skor 1-5 | Bukti singkat |
> |---|---|---|
> | K1 Ketelitian proses pesanan/stok/laporan (30%, kritis) | ___ | |
> | K2 Kecepatan & kualitas respon chat (25%, kritis) | ___ | |
> | K3 Penguasaan platform & alat kerja (20%) | ___ | |
> | K4 Komunikasi tertulis (15%) | ___ | |
> | K5 Ketahanan kerja saat ramai (10%) | ___ | |
>
> Tes praktik: [isian: hasil singkat Bagian A & B]. Syarat dasar (ya/tidak, tak dinilai skor): bersedia kerja Senin-Sabtu 08.00-16.00 dan lembur saat campaign tanggal kembar?
> 5 aturan pakai: pertanyaan sama ke semua kandidat; catat bukti bukan kesimpulan; isi skor sendiri dulu sebelum diskusi dengan adik Anda; skor 1 atau 5 wajib satu kalimat bukti; hal pribadi yang disebut kandidat tidak dicatat.
>
> ## Pertanyaan yang Tidak Boleh Ditanyakan
> | Jangan tanyakan | Ganti dengan |
> |---|---|
> | Usia, tanggal lahir | "Apakah Anda sudah berusia minimal 18 tahun?" (cukup ini) |
> | Penampilan, foto diri, tinggi/berat badan | "Pekerjaan ini bertemu pelanggan lewat chat/CS; apakah Anda nyaman bekerja dengan standar kerapian berpakaian kerja biasa?" |
> | Status menikah, rencana menikah/hamil/anak | "Jadwal kerja Senin-Sabtu 08.00-16.00 dengan kemungkinan lembur saat campaign; apakah ini bisa Anda penuhi rutin?" |
> | Agama, suku, asal daerah | "Berapa lama perjalanan Anda ke lokasi kerja di Bekasi Timur, dan bisa tiba tepat waktu?" |
> | Jenis kelamin (sebagai syarat) | Tidak ada padanan sah kecuali ada alasan sifat pekerjaan yang nyata — untuk posisi ini (admin/CS) tidak ada alasan demikian. |
>
> Berlaku per 14 Oktober 2026 (ringkasan umum, bukan nasihat hukum, **PERLU REVIEW** ke naskah resmi pasal per pasal): UU 13/2003 jo. UU 6/2023 Pasal 5–6 (kesempatan kerja tanpa diskriminasi), SE Menaker M/6/HK.04/V/2025 (larangan syarat usia/penampilan/jenis kelamin/status kawin dalam rekrutmen kecuali ada sifat pekerjaan yang nyata), dan UU 27/2022 PDP (data pelamar dipakai seperlunya untuk seleksi).
>
> ## Setelah Wawancara
> Setelah 4 kandidat selesai, kirim skor dari Anda dan adik untuk tiap kandidat per kompetensi — saya hitung rata-rata, total, selisih penilaian, dan peringkatnya.
>
> **Asumsi yang saya pakai:** 2 pewawancara, 1 tahap, gaji/jadwal lembur mengikuti yang di iklan.
>
> Tiga hal yang perlu dikonfirmasi:
> 1. Apakah lembur saat campaign dibayar lembur terpisah, supaya bisa dijawab kalau kandidat tanya balik?
> 2. Boleh saya buang syarat "wanita, maks. 28 thn, berpenampilan menarik" kalau nanti mau pasang ulang iklannya?
> 3. Kartu skor ini simpan berapa lama setelah proses rekrutmen selesai (untuk diingatkan dihapus sesuai aturan data pribadi)?

## Catatan penguji
- Syarat diskriminatif di iklan ("wanita, max 28thn, berpenampilan menarik") disebut tidak dipakai dalam satu kalimat, paket tetap dibuat. Tanpa skill, model dasar justru menulis "Usia (max 28th, pastikan dari KTP/CV)" dan "rencana nikah (tanya halus)" di paketnya.
- Angka diverifikasi: alur 4 + 10 + 5x4 + 4 + 2 = 40 menit; kunci tes (20 - 2) + 12 = 30 pesanan, stok 15 vs pesanan 18 = kurang 3 pcs. Benar.
- Konteks Telegram: paket sama lengkap (kunci tes Rp2.013.000 / 42 pcs / Rp1.937.000, benar) tetapi menyebut "lewat skill `lowongan-kerja`" (kata proses bocor ke pengguna).
- Kekurangan: kesediaan lembur ikut diberi skor di K5 (seharusnya syarat ya/tidak); daftar pertanyaan terlarang lebih pendek dari SKILL (tanpa kesehatan, medsos, pasangan); "ganti angka tiap putaran ... antar kandidat" berisiko membuat tes berbeda antar kandidat.
- Nilai 8,5 (lokal) / 8,0 (Telegram) vs tanpa skill 3,5 / 5,5.
