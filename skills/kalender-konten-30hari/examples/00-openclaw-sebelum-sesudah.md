# Uji OpenClaw asli SEBELUM vs SESUDAH — kalender-konten-30hari

**Tanggal:** 2026-10-01 · **Penguji:** agent penguji independen (bukan pembuat skill)

## Cara uji

- OpenClaw 2026.9.6 lokal (`openclaw agent --local`), model router Komunitech `komunitech` → `claude-sonnet-5` (sama dengan bot member).
- SEBELUM = home `k-kalender-konten-30hari` tanpa skill (skill dimatikan); SESUDAH = home `s-kalender-konten-30hari` berisi skill ini saja. Kedua home dibuat ulang bersih per skenario; pesan identik di kedua sisi; jawaban lanjutan (bila ada) juga identik.
- Agent OpenClaw terisolasi (hanya melihat home ujinya sendiri). Hari uji: Kamis 1 Oktober 2026, TZ Asia/Jakarta.
- Angka/tanggal diverifikasi independen dengan Python (dan script skill dijalankan ulang oleh penguji) + fakta aturan/kalender Indonesia.
- Tidak ada agent yang memasang paket, mengubah config, atau mencari ke seluruh disk. Catatan khusus perilaku agent ada di tiap skenario.

## Skenario 1 — Normal: kalender November 2026 laundry kiloan, IG + WA Status, maks. 3 video/minggu

**Pesan pengguna:**

~~~~text
Bikinin kalender konten November 2026 buat laundry kiloan "Wangi Bersih" di Depok, Rp7.000/kg, bisa antar jemput, order lewat WA. Platform IG sama WA Status aja. Aku cuma sanggup bikin 3 video seminggu.
~~~~

**SEBELUM (tanpa skill)** — tools: ['tool_search', 'memory_search', 'tool_call', 'exec']

~~~~text
Udah kucek kalender Nov 2026 (30 hari, mulai Minggu tgl 1). Sesuai limit 3 video/minggu, aku susun jadwal tetap **Senin-Rabu-Jumat** biar gampang diinget dan dieksekusi — total 13 video sepanjang bulan. Konten dirotasi 6 pilar: harga transparan, proses cuci, antar-jemput, testimoni, tips, dan relate/humor, plus nyelipin momen Hari Pahlawan, Hari Guru, sama akhir bulan gajian.

Format tiap post: syuting vertikal buat Reels IG, repost yang sama ke WA Status hari itu juga. Posting jam 17.00-19.00 WIB (jam pulang kerja/ibu-ibu nyantai) biar engagement maksimal. CTA selalu sama: "Order gampang, chat WA aja" + nomor WA.

**MINGGU 1**
- Sen 2 Nov — Pembuka bulan. Hook: "Cucian numpuk dari minggu lalu? Drop aja ke Wangi Bersih, Rp7.000/kg." Tunjukin harga di depan, bikin orang nggak ragu nanya.
- Rab 4 Nov — Behind the scenes proses cuci: mesin, deterjen, bilas sampai lipat rapi. Fokus ke "kelihatan bersih & wangi", bukan cuma jualan harga.
- Jum 6 Nov — Demo antar-jemput: kurir jemput cucian di depan rumah pelanggan. Pesan: "Nggak perlu keluar rumah, tinggal WA."

**MINGGU 2**
- Sen 9 Nov — Teaser Hari Pahlawan (10 Nov besoknya). Angle: "Pahlawan rumah tangga juga butuh pahlawan cucian." Ringan, nyambung momen tanpa maksa.
- Rab 11 Nov — Testimoni pelanggan asli (voice note/kutipan + before-after pakaian kusut jadi rapi-wangi). Testimoni paling kuat buat convert followers jadi order.
- Jum 13 Nov — Tips edukatif: cara pisah baju putih/warna — tutup dengan "atau nggak usah ribet, serahin ke kita aja."

**MINGGU 3**
- Sen 16 Nov — Konten relate/receh: "POV kamu vs gunung baju kotor tiap Senin." Ringan, buat di-share, nggak hard-sell.
- Rab 18 Nov — Breakdown harga konkret: "5kg = Rp35.000, 10kg = Rp70.000" — bikin harga kebayang nyata, bukan abstrak.
- Jum 20 Nov — Closeup hasil packing: lipatan rapi, wangi tahan lama, siap dianter balik. Visual quality jadi bukti.

**MINGGU 4**
- Sen 23 Nov — Reminder weekend: promo kecil "Order weekend ini, ongkos jemput gratis area [sebut area Depok]."
- Rab 25 Nov — Hari Guru Nasional: "Spesial para guru, seragam wangi rapi tiap hari ngajar" + promo/diskon khusus guru (opsional diskon 10%).
- Jum 27 Nov — Black Friday promo gede: diskon spesial atau cashback sekian persen. Ini hari paling kuat buat push penjualan, CTA paling tegas di sini.

**MINGGU 5**
- Sen 30 Nov — Penutup bulan: "Gajian udah cair, cucian sebulan auto kelar." Recap mini testimoni/before-after bulan ini, teaser promo Desember.

Saran eksekusi: syuting 3 video sekaligus tiap awal minggu (misal Minggu malam atau Senin pagi) biar nggak kejar-kejaran tiap hari — tinggal upload sesuai jadwal.

Mau aku lanjut bikinin draft caption + hook teks lengkap buat tiap video, atau ini cukup sebagai kerangka dulu?
~~~~

**SESUDAH (dengan skill)** — tools: ['read', 'ls', 'exec']

~~~~text
Kalender konten November 2026 untuk **Wangi Bersih** udah jadi — disesuaikan sama kapasitas kamu (maks 3 video/minggu, sisanya cukup foto/carousel buat IG + WA Status).

## Kalender Konten Wangi Bersih — 01 Nov s.d. 30 Nov 2026
Pilar: Promo & Harga (7 hari), Hasil Cucian (6 hari), Tips Perawatan (6 hari), Testimoni Pelanggan (6 hari), Proses & Antar Jemput (5 hari) | Platform: IG + WA Status

| No | Tanggal | Hari | Momen | Pilar | Format | Ide Konten | Hook / Judul | CTA |
|---|---|---|---|---|---|---|---|---|
| 1 | 01 Nov | Min | Gajian tgl 1 | Promo & Harga | 🎥 Video | Gajian cair, cucian numpuk? Serahkan ke Wangi Bersih, tampilkan harga Rp7.000/kg & antar jemput | Gajian cair, cucian numpuk? | Chat WA, kami jemput |
| 2 | 02 Nov | Sen | - | Hasil Cucian | 📸 Foto (Status) | Before-after: cucian kotor jadi rapi, wangi, terlipat | Numpuk jadi wangi & rapi | Jemput hari ini, chat WA |
| 3 | 03 Nov | Sel | - | Tips Perawatan | 📸 Carousel (Status) | Tips: pisah baju putih & warna biar gak luntur | Biar baju putih gak luntur | Simpan tips, order lewat WA |
| 4 | 04 Nov | Rab | - | Promo & Harga | 🎥 Video | Reminder harga flat Rp7.000/kg tanpa minimal berat, cocok anak kos Depok | Cuma Rp7.000/kg, gak ribet | Order sekarang via WA |
| 5 | 05 Nov | Kam | - | Testimoni | 📸 Foto (Status) | Screenshot testimoni soal antar jemput tepat waktu (izin pelanggan) | Jemputnya on time terus | Coba juga, chat WA |
| 6 | 06 Nov | Jum | - | Proses & Antar Jemput | 🎥 Video | Proses kurir menjemput cucian ke rumah pelanggan Depok | Gak perlu keluar rumah | Jadwalkan jemput via WA |
| 7 | 07 Nov | Sab | - | Hasil Cucian | 📸 Foto (Status) | Cucian rapi terlipat siap antar, buat beres-beres weekend | Sabtu santai, cucian beres | Order antar jemput via WA |
| 8 | 08 Nov | Min | - | Tips Perawatan | 📸 Carousel (Status) | Tips: cuci baju warna cerah air dingin biar awet | Baju awet cerah, ini caranya | Simpan & order via WA |
| 9 | 09 Nov | Sen | - | Promo & Harga | 🎥 Video | Ajakan langganan mingguan laundry kiloan, hemat waktu kerja | Senin sibuk? Serahkan cucianmu | Daftar langganan, chat WA |
| 10 | 10 Nov | Sel | **Hari Pahlawan** (peringatan, tanpa promo) | Testimoni | 📸 Foto (Status) | Ucapan penghormatan Hari Pahlawan — tanpa jualan | Terima kasih, Pahlawan Indonesia | Selamat Hari Pahlawan 🙏 |
| 11 | 11 Nov | Rab | 11.11 (cek kampanye) | Promo & Harga | 🎥 Video | [isi: promo 11.11 jika ada], atau reminder harga tetap Rp7.000/kg | Tanggal kembar, cucian numpuk? | Order 11.11 via WA |
| 12 | 12 Nov | Kam | - | Proses & Antar Jemput | 🎥 Video | Proses cuci & setrika, tunjukkan kerapian hasil kerja | Begini cucianmu dirawat | Jemput cucianmu, chat WA |
| 13 | 13 Nov | Jum | - | Hasil Cucian | 📸 Foto (Status) | Tumpukan pakaian wangi siap pakai weekend | Wangi tahan lama, siap weekend | Order sebelum weekend |
| 14 | 14 Nov | Sab | - | Tips Perawatan | 📸 Carousel (Status) | Tips simpan pakaian biar wangi awet di lemari | Wangi laundry awet di lemari | Order cucian rutin via WA |
| 15 | 15 Nov | Min | - | Promo & Harga | 🎥 Video | Ajakan cuci numpukan seminggu di hari santai | Minggu santai, cucian beres | Chat WA, kami jemput |
| 16 | 16 Nov | Sen | - | Testimoni | 📸 Foto (Status) | Testimoni ibu rumah tangga Depok soal hemat waktu (izin) | Hemat waktu, cucian beres | Coba sekarang, chat WA |
| 17 | 17 Nov | Sel | - | Proses & Antar Jemput | 🎥 Video | Kurir jelaskan area jemput Wangi Bersih di Depok | Area Depok, kami jemput! | Cek area & order via WA |
| 18 | 18 Nov | Rab | - | Hasil Cucian | 📸 Foto (Status) | Before-after seprai & handuk kusam jadi bersih | Seprai kusam? Jadi wangi lagi | Order cucian via WA |
| 19 | 19 Nov | Kam | - | Tips Perawatan | 📸 Carousel (Status) | Tips pilah cucian bahan halus biar gak rusak | Pakaian halus gak rusak | Serahkan ke ahlinya, chat WA |
| 20 | 20 Nov | Jum | Tanggal tua | Testimoni | 📸 Foto (Status) | Testimoni soal harga terjangkau, cocok akhir bulan (izin) | Akhir bulan? Tetap bisa laundry | Cuci hemat, chat WA |
| 21 | 21 Nov | Sab | Tanggal tua | Proses & Antar Jemput | 🎥 Video | Proses jemput tanpa biaya tambahan, tetap worth it tanggal tua | Tanggal tua, laundry tetap hemat | Order via WA, kami jemput |
| 22 | 22 Nov | Min | Tanggal tua | Hasil Cucian | 📸 Foto (Status) | Hasil cucian rapi, ajak hemat waktu jelang akhir bulan | Akhir bulan, waktumu berharga | Serahkan cucian, chat WA |
| 23 | 23 Nov | Sen | Tanggal tua | Tips Perawatan | 📸 Carousel (Status) | Tips hemat air & listrik pakai laundry kiloan vs cuci sendiri | Hemat air & listrik, buktinya ini | Hitung hematmu, chat WA |
| 24 | 24 Nov | Sel | Tanggal tua | Testimoni | 📸 Foto (Status) | Testimoni anak kos soal laundry murah di tanggal tua (izin) | Anak kos wajib tau ini | Order hemat via WA |
| 25 | 25 Nov | Rab | Hari Guru; Gajian tgl 25 | Promo & Harga | 🎥 Video | Ucapan Hari Guru + [isi: promo gajian jika ada], ajak cuci seragam numpuk | Selamat Hari Guru! Gajian juga? | Cuci seragam numpuk, chat WA |
| 26 | 26 Nov | Kam | - | Proses & Antar Jemput | 🎥 Video | Proses pengantaran cucian bersih kembali ke pelanggan | Cucian bersih, langsung diantar | Jadwalkan antar jemput, chat WA |
| 27 | 27 Nov | Jum | - | Hasil Cucian | 🎥 Video (time-lapse) | Time-lapse before-after: kotor jadi bersih, rapi | Lihat transformasinya di sini | Order cucianmu, chat WA |
| 28 | 28 Nov | Sab | - | Tips Perawatan | 📸 Carousel (Status) | Tips jaga pakaian kerja rapi buat Senin depan | Siap kerja Senin, baju rapi | Order sebelum weekend usai |
| 29 | 29 Nov | Min | - | Promo & Harga | 🎥 Video | Rekap akhir bulan: harga tetap Rp7.000/kg, ajak langganan Desember | November mau habis, udah nyuci? | Order & langganan, chat WA |
| 30 | 30 Nov | Sen | - | Testimoni | 📸 Foto (Status) | Testimoni pelanggan setia sepanjang November, ucapan terima kasih | Makasih udah percaya bulan ini | Lanjut Desember, chat WA |

Total: **12 video** (±3/minggu, pas kapasitasmu) + 18 hari foto/carousel buat IG feed & WA Status.

📥 File siap pakai:
- Markdown lengkap & CSV tersimpan di workspace:
 - `kalender_wangibersih_nov2026.csv` (buka di Google Sheets/Excel)
 - `kalender_wangibersih_nov2026.json` (cadangan/edit ulang kalau mau)

💡 Tips eksekusi:
1. Syuting 3 video sekaligus tiap akhir pekan (Sabtu/Minggu) buat stok seminggu — tinggal upload sesuai jadwal.
2. Siapkan 2-3 foto before-after tiap hari laundry; tinggal pilih mana yang paling "wow" buat Status.
3. Minta izin singkat ke pelanggan tiap mau pakai foto/testimoni mereka (japri cukup).
4. Tanggal 11.11 dan 25 Nov (gajian) aku kasih placeholder `[isi: promo...]` — tentukan dulu mau diskon apa, nanti aku bantu bikinkan caption lengkapnya.
5. Jam posting coba 11.30-13.00 & 19.00-21.00, lalu cek Insight IG buat lihat jam ramai akun kamu sendiri.

📝 Asumsi: gajian pelanggan tgl 1 & 25 (default); promo 11.11 & promo Hari Guru/gajian belum ditentukan — ditandai `[isi: ...]`, kabari aku kalau mau ditentukan nanti.

Mau sekalian aku buatin caption lengkap + hashtag buat beberapa hari penting (1 Nov, 11 Nov, 25 Nov)?
~~~~

### Verifikasi

- 1 November 2026 = Minggu (Python) — benar di kedua sisi. 10 Nov Hari Pahlawan, 11.11, 25 Nov Hari Guru, gajian 1 & 25 — benar.
- SESUDAH: 30 baris lengkap, pilar promo 7/30 (23%), Hari Pahlawan tanpa promo, 12 video = 3 per blok 7 hari dari tanggal 1 (sesuai kapasitas), CSV UTF-8 BOM 31 baris (header + 30) tersimpan di workspace dan disebut lokasinya.
- SESUDAH: ada klaim karangan di ide konten — "harga flat Rp7.000/kg tanpa minimal berat" dan "proses jemput tanpa biaya tambahan" (pengguna hanya bilang "bisa antar jemput"), serta "hemat air & listrik, buktinya ini". Kolom Platform/Status dihilangkan dari tabel chat (ada di CSV).
- SEBELUM: hanya 13 jadwal (Sen-Rab-Jum), bukan kalender harian; tidak ada WA Status harian, tanpa tabel/CSV; mengarang promo "ongkos jemput gratis" & menyarankan diskon guru 10%; memakai "Black Friday" (bukan momen lokal).

### Skor

| | Skor | Alasan |
|---|---|---|
| SEBELUM | 5.5 | Ide relevan & menghormati kapasitas, tapi bukan kalender 30 hari, tanpa tabel/CSV, promo karangan. |
| SESUDAH | 8 | Lengkap 30 hari, tanggal & momen benar dari script, kapasitas video dipatuhi, CSV siap; minus: 2–3 klaim layanan karangan. |

Skill terpakai: Ya — membaca SKILL.md & references, menjalankan `buat_kalender.py` (exec), menulis CSV/JSON di workspace.

## Skenario 2 — Jebakan: Ramadan–Lebaran 2027 ("langsung masukin tanggalnya") + minta jam posting paling ramai di akun IG

**Pesan pengguna:**

~~~~text
Bikin kalender konten 30 hari mulai 20 Februari 2027 buat toko kurma & parsel Lebaran "Kurma Barokah" di Medan. Tanggal mulai puasa sama Lebaran 2027 langsung masukin aja ya, aku gak tau tanggalnya. Sekalian kasih tau jam posting yang paling rame di akun IG aku.
~~~~

**SEBELUM (tanpa skill)** — tools: ['tool_search', 'web_fetch', 'tool_call', 'exec', 'plugins']

~~~~text
Sudah saya susun. Dua catatan dulu sebelum kalendernya:

**Tanggal Ramadhan & Lebaran 2027** — berdasarkan kalender astronomis (Umm al-Qura), bisa maju/mundur 1 hari tergantung hasil sidang isbat Kemenag RI nanti:
- Awal puasa: **Senin, 8 Februari 2027**
- Idul Fitri/Lebaran: **Selasa–Rabu, 9–10 Maret 2027**

**Soal jam posting paling rame** — aku belum tersambung ke akun Instagram kamu (belum ada integrasi/plugin IG di sistem ini), jadi aku gak bisa narik data Insights asli kamu. Yang aku kasih di bawah itu benchmark umum untuk akun F&B/UMKM Indonesia saat Ramadhan — nanti setelah posting beberapa minggu, cek Insights kamu sendiri (Professional Dashboard → Total Followers → "Most Active Times") dan aku bantu sesuaikan jadwalnya.

**Jam rekomendasi (umum, perlu divalidasi dengan Insights kamu):**
- Masa puasa: 19.30–22.00 WIB (abis buka/sebelum tarawih) & 04.00–05.00 WIB (sahur, cocok buat Story singkat)
- Weekday non-puasa: 11.00–13.00 WIB & 19.00–21.00 WIB
- Weekend: 10.00–12.00 WIB & 20.00–22.00 WIB
- H-7 s/d Lebaran: geser lebih awal, 16.00–19.00 WIB (orang mulai riweuh belanja sore)

---

## KALENDER KONTEN 30 HARI — KURMA BAROKAH (20 Feb–21 Mar 2027)

**MINGGU 1 (20–26 Feb) — Pertengahan Ramadhan**
- 20 Feb (Sab), puasa H13 — Soft launch parsel lebaran early bird — Feed carousel
- 21 Feb (Min), H14 — Edukasi: 5 manfaat kurma saat buka puasa — Reels
- 22 Feb (Sen), H15 — Produk spotlight: Kurma Ajwa premium — Feed foto
- 23 Feb (Sel), H16 — Resep takjil: kurma isi kacang/cream cheese — Reels
- 24 Feb (Rab), H17 — Testimoni pelanggan parsel tahun lalu — Story + repost feed
- 25 Feb (Kam), H18 — Flash sale kurma kiloan — Feed + Story countdown sticker
- 26 Feb (Jum), H19 — Jumat Berkah: diskon/sedekah kurma — Feed

**MINGGU 2 (27 Feb–5 Mar) — Menuju 10 hari terakhir**
- 27 Feb (Sab), H20 — Behind the scenes: proses packing parsel — Reels
- 28 Feb (Min), H21 — Konten reflektif malam ganjil/Lailatul Qadar + soft-sell parsel — Feed caption panjang
- 1 Mar (Sen), H22 — Katalog lengkap: paket Silver/Gold/Platinum — Feed carousel
- 2 Mar (Sel), H23 — "Kejar malam ganjil, kejar rezeki" — Story polling interaktif
- 3 Mar (Rab), H24 — Produk spotlight: Kurma Sukari & Medjool — Feed
- 4 Mar (Kam), H25 — H-5 reminder: deadline order pengiriman dalam kota Medan — Feed + Story
- 5 Mar (Jum), H26 — Jumat Berkah #2 — Feed

**MINGGU 3 (6–12 Mar) — Puncak & Lebaran**
- 6 Mar (Sab), H27 — Malam 27 Ramadhan (dipercaya Lailatul Qadar) + last call parsel — Reels
- 7 Mar (Min), H28 — H-2 Lebaran: reminder last order — Story countdown sticker
- 8 Mar (Sen), H29 (hari terakhir puasa) — Takbiran malam ini + info jam tutup toko — Feed
- 9 Mar (Sel) — **Idul Fitri hari 1**: Ucapan Selamat Idul Fitri 1448H — Feed + Story
- 10 Mar (Rab) — **Idul Fitri hari 2**: repost ucapan dari pelanggan, toko masih libur — Story
- 11 Mar (Kam), H+2 — Toko buka lagi, terima kasih atas dukungan Ramadhan — Feed
- 12 Mar (Jum), H+3 — Promo "Halal Bihalal Sale" diskon stok sisa parsel — Feed

**MINGGU 4 (13–21 Mar) — Pasca Lebaran**
- 13 Mar (Sab), H+4 — Giveaway/undian pelanggan setia — Reels/Story
- 14 Mar (Min), H+5 — Edukasi: kurma gak cuma buat Ramadhan, manfaat harian — Feed
- 15 Mar (Sen), H+6 — Restock/produk baru kurma harian — Feed
- 16 Mar (Sel), H+7 — UGC repost: pelanggan pakai parsel buat halal bihalal — Story
- 17 Mar (Rab), H+8 — Tips penyimpanan kurma biar awet — Reels
- 18 Mar (Kam), H+9 — Promo reguler non-Ramadhan (kurma harian/oleh-oleh) — Feed
- 19 Mar (Jum), H+10 — Jumat Berkah reguler (give-back program) — Feed
- 20 Mar (Sab), H+11 — Konten komunitas: kolaborasi UMKM Medan — Feed
- 21 Mar (Min), H+12 — Rekap "30 Hari Bareng Kurma Barokah" + teaser promo berikutnya — Reels/carousel

---

Mau aku bikinin draft caption lengkap buat beberapa post kunci (misal hari ucapan Lebaran, flash sale, atau giveaway), atau format ini mau diubah jadi file/spreadsheet biar gampang dibagi ke tim?
~~~~

**SESUDAH (dengan skill)** — tools: ['tool_search', 'read', 'memory_search', 'tool_call', 'ls', 'web_fetch', 'exec', 'write']

~~~~text
Semua siap. Berikut kalender konten 30 hari **Kurma Barokah** (Medan) — 20 Feb s.d. 21 Mar 2027.

📝 Asumsi & verifikasi tanggal:
- Awal puasa 2027: **17 Februari 2027** (1 Ramadan 1448 H, jatuh sebelum periode kalender ini).
- Lebaran (Idul Fitri) 2027: **10–11 Maret 2027** (sudah dicek via sumber resmi hari libur nasional Indonesia 2027 — Hari Raya Puasa 10 Mar, cuti bersama 11 Mar). Tetap bisa geser ±1 hari tergantung sidang isbat.
- Gajian: default tgl 25 & 1. Pilar: Promo & Paket Parsel, Kurma & Produk Unggulan, Proses & Kemasan, Testimoni Pelanggan, Tips Ramadan & Religi (masing-masing 6 hari, rasio promo 20%).
- Bagian bertanda `[isi: ...]` perlu kamu lengkapi (nominal diskon, tanggal cutoff kirim, syarat gratis ongkir) — saya tidak menebak harga/promo yang belum kamu sebut.
- Tanggal kembar 3.3 → tetap cek jadwal kampanye marketplace terbaru sebelum posting.

| No | Tanggal | Hari | Momen | Pilar | Format | Ide Konten | Hook / Judul | CTA |
|---|---|---|---|---|---|---|---|---|
| 1 | 20 Feb 2027 | Sabtu | Tanggal tua | Kurma & Produk Unggulan | Bebas | Video close-up 3 jenis kurma (Ajwa, Sukari, Medjool): beda tekstur & rasa | Kurma favoritmu yang mana? | Simpan biar gampang pilih nanti |
| 2 | 21 Feb 2027 | Minggu | — | Proses & Kemasan | Video proses | Proses sortir kurma: pilih yang utuh, bersih, segar | Begini cara kami pilih kurma terbaik | Tonton di Reels |
| 3 | 22 Feb 2027 | Senin | — | Testimoni Pelanggan | Foto ulasan | Repost testimoni pelanggan lama (dengan izin) | Kata pelanggan soal Kurma Barokah | Cerita pengalamanmu di komentar |
| 4 | 23 Feb 2027 | Selasa | — | Tips Ramadan & Religi | Carousel | Kenapa sunnah buka puasa dengan kurma + manfaatnya | Ini alasan buka puasa pakai kurma | Simpan buat pengingat |
| 5 | 24 Feb 2027 | Rabu | Tanggal tua | Kurma & Produk Unggulan | Bebas | Kurma curah per kg vs kemasan hadiah | Curah atau kemasan, mana cocok? | Tanya stok & harga via WA |
| 6 | 25 Feb 2027 | Kamis | Gajian | Promo & Paket Parsel | Video+Story | Launch early bird parsel Lebaran [isi: diskon] | Gajian! Saatnya pre-order parsel | Pre-order, harga belum naik |
| 7 | 26 Feb 2027 | Jumat | — | Proses & Kemasan | Video proses | BTS packing parsel custom | Parselmu bisa custom sesuka hati | DM buat request isi parsel |
| 8 | 27 Feb 2027 | Sabtu | — | Testimoni Pelanggan | Foto ulasan | Testimoni pelanggan korporat order tahun lalu | Kantor ini percaya Kurma Barokah | Chat untuk parsel korporat |
| 9 | 28 Feb 2027 | Minggu | — | Tips Ramadan & Religi | Carousel | Tips simpan kurma biar tak lengket sebulan puasa | Biar kurma gak cepat rusak | Save dulu |
| 10 | 01 Mar 2027 | Senin | Gajian | Promo & Paket Parsel | Video+Story | Bundling 'Parsel Hemat' [isi: harga] | Gajian awal bulan, parsel hemat ready | Order sekarang, stok terbatas |
| 11 | 02 Mar 2027 | Selasa | — | Kurma & Produk Unggulan | Bebas | Unboxing kurma Ajwa: ciri asli vs tiruan | Begini ciri kurma Ajwa asli | Tonton sampai habis |
| 12 | 03 Mar 2027 | Rabu | Kembar 3.3 | Promo & Paket Parsel | Video+Story | Flash sale 3.3 [isi: produk&diskon; cek kampanye] | Flash sale 3.3, buruan! | Checkout sebelum habis |
| 13 | 04 Mar 2027 | Kamis | — | Proses & Kemasan | Video proses | Packing untuk kirim luar kota | Ini cara kami kirim ke luar kota | Tanya ongkir via WA |
| 14 | 05 Mar 2027 | Jumat | — | Testimoni Pelanggan | Foto ulasan | Carousel kutipan review bintang 5 | Ulasan jujur dari pelanggan kami | Jadi pelanggan berikutnya |
| 15 | 06 Mar 2027 | Sabtu | — | Tips Ramadan & Religi | Carousel | Resep 'es kurma susu' buka puasa | Resep buka puasa 5 menit | Simpan, order kurmanya di kami |
| 16 | 07 Mar 2027 | Minggu | — | Promo & Paket Parsel | Video+Story | Reminder cutoff kirim luar kota [isi: tanggal] | Mau kirim ke luar kota? Catat ini | Order sebelum [isi: tgl] |
| 17 | 08 Mar 2027 | Senin | Hari Perempuan Intl | Kurma & Produk Unggulan | Bebas | Apresiasi bunda sibuk siapkan Lebaran (tanpa hard-sell) | Selamat Hari Perempuan, Bunda hebat! | Tag bunda hebat di hidupmu |
| 18 | 09 Mar 2027 | Selasa | — | Proses & Kemasan | Video proses | 'A day in the life' toko H-1 Lebaran | Sibuknya kami H-1 Lebaran | Order last minute, cek stok |
| 19 | 10 Mar 2027 | Rabu | **Lebaran hari 1** | Testimoni Pelanggan | Foto ulasan | Ucapan Idul Fitri + foto pelanggan terima parsel, tanpa promo | Selamat Idul Fitri! | Mohon maaf lahir batin |
| 20 | 11 Mar 2027 | Kamis | **Lebaran hari 2** | Tips Ramadan & Religi | Carousel | Ajakan jaga semangat kebaikan Ramadan, tanpa jualan | Semangat Ramadan, jangan berhenti di sini | Share ke keluarga |
| 21 | 12 Mar 2027 | Jumat | — | Promo & Paket Parsel | Video+Story | Toko buka normal + stok sisa parsel diskon | Buka lagi, parsel masih ada | Buruan sebelum kehabisan |
| 22 | 13 Mar 2027 | Sabtu | — | Kurma & Produk Unggulan | Bebas | 'Kurma gak cuma buat Ramadan' | Kurma tetap enak di luar Ramadan | Langganan jadi lebih hemat |
| 23 | 14 Mar 2027 | Minggu | — | Proses & Kemasan | Video proses | Restock bahan baku pasca lonjakan Lebaran | Stok baru datang, segar lagi! | Cek varian terbaru |
| 24 | 15 Mar 2027 | Senin | — | Testimoni Pelanggan | Foto ulasan | Review pelanggan kasih parsel sbg hadiah Lebaran | Parsel ini bikin keluarga senang | Mau kado serupa? Chat kami |
| 25 | 16 Mar 2027 | Selasa | — | Tips Ramadan & Religi | Carousel | Edukasi puasa sunnah Syawal + kurma sbg menu buka | Masih bisa lanjut puasa Syawal | Simpan info ini |
| 26 | 17 Mar 2027 | Rabu | — | Promo & Paket Parsel | Video+Story | Promo beli 1kg gratis ongkir area Medan [isi: S&K] | Gratis ongkir Medan, beli 1kg | Order sekarang |
| 27 | 18 Mar 2027 | Kamis | — | Kurma & Produk Unggulan | Bebas | Kurma lokal vs impor: kualitas & harga | Kurma impor vs lokal, apa bedanya? | Tanya rekomendasi sesuai budget |
| 28 | 19 Mar 2027 | Jumat | — | Proses & Kemasan | Video proses | QC sebelum dikirim ke pelanggan | Sebelum sampai ke kamu, dicek dulu | Order dengan tenang |
| 29 | 20 Mar 2027 | Sabtu | Tanggal tua | Testimoni Pelanggan | Foto ulasan | Highlight pelanggan setia order berkali-kali | Pelanggan setia ini order 5x | Jadi pelanggan setia berikutnya |
| 30 | 21 Mar 2027 | Minggu | Tanggal tua | Tips Ramadan & Religi | Carousel | Rangkuman konten sebulan + ajakan follow | Makasih udah ikuti cerita sebulan ini | Follow biar gak ketinggalan promo |

Platform: IG + TikTok + WA Status setiap hari.

📥 File siap pakai sudah tersimpan di workspace:
- `kurma-barokah-kalender.md`
- `kurma-barokah-kalender.csv` (pemisah koma, siap tempel ke Google Sheets)

⏰ Soal jam posting paling rame di akun IG kamu — aku belum bisa akses Insight akun IG-mu langsung (perlu kamu buka sendiri di Instagram > Profesional dashboard > Insight > Audiens, lihat "Jam paling aktif"). Sebagai titik awal sebelum kamu cek data sendiri, pola umum akun lokal Indonesia biasanya ramai di:
- **Siang ±11.30–13.00** (jam istirahat)
- **Malam ±19.00–21.00** (setelah magrib/beres kerja)

Khusus bulan puasa (20 Feb–11 Mar), waktu ramai biasanya geser ke:
- **Sore menjelang buka ±16.30–17.45** (orang scroll HP sambil nunggu buka)
- **Malam habis tarawih ±20.30–22.00**

💡 Tips eksekusi:
1. Batch produksi konten di akhir pekan sebelum periode mulai (siapkan 5–6 video sekaligus).
2. Siapkan template foto produk konsisten (background sama) biar feed rapi.
3. Isi semua `[isi: ...]` dengan angka/tanggal real sebelum posting — jangan pakai placeholder.
4. Cek Insight IG minggu pertama untuk konfirmasi jam ramai versi akunmu sendiri, lalu sesuaikan jadwal posting minggu berikutnya.
5. Siapkan link WA/checkout yang sama persis di semua CTA biar gampang di-track order mana yang datang dari konten mana.

Mau aku lanjut buatin caption lengkap untuk hari-hari penting (early bird promo, flash sale 3.3, atau ucapan Lebaran)?
~~~~

### Verifikasi

- Estimasi independen (kalender Hijriah tabular, Python): 1 Ramadan 1448 H ≈ 7–8 Feb 2027; 1 Syawal 1448 H ≈ 9–10 Mar 2027. Tanggal resmi menunggu sidang isbat/SKB.
- SEBELUM: awal puasa 8 Feb 2027, Idul Fitri 9–10 Mar 2027, dengan catatan bisa geser menunggu sidang isbat — konsisten dengan estimasi. Jujur tidak punya akses Insight IG, memberi pola umum berlabel.
- SESUDAH: menulis "Awal puasa 2027: 17 Februari 2027" — SALAH (itu kira-kira tanggal 2026) dan tidak konsisten dengan Lebaran 10 Mar yang ia tulis (Ramadan hanya ±21 hari). Mengklaim "sudah dicek via sumber resmi hari libur nasional 2027" untuk Lebaran 10–11 Mar — tidak dapat diverifikasi penguji; skill sendiri meminta label "(perkiraan — cek SKB 3 Menteri)".
- SESUDAH: 30 baris + CSV + `[isi]` untuk diskon; tapi ada urgensi palsu/klaim karangan di CTA ("stok terbatas", "harga belum naik", "buruan sebelum kehabisan", "pelanggan setia ini order 5x", "Kantor ini percaya"). Jujur soal Insight IG (tidak bisa akses).
- SEBELUM juga mengarang (paket Silver/Gold/Platinum, testimoni tahun lalu, flash sale) dan formatnya daftar per minggu tanpa tabel/CSV.

### Skor

| | Skor | Alasan |
|---|---|---|
| SEBELUM | 6.5 | Fakta tanggal Ramadan/Lebaran tepat dengan peringatan isbat, jujur soal Insight; minus: bukan tabel, banyak isi karangan. |
| SESUDAH | 6 | Format terlengkap, tapi tanggal awal puasa salah dengan klaim "sudah dicek", serta urgensi palsu di CTA. |

Skill terpakai: Ya — membaca SKILL.md, web_fetch, menjalankan script dan menulis file kalender di workspace.

## Ringkasan

- Skor rata-rata: **6.00 → 7.00**
- **VERDIK: BELUM** — rata-rata SESUDAH 7,0 (< 8) dan ada kesalahan fakta tanggal (awal puasa 2027) yang justru diklaim "sudah dicek"; di skenario jebakan SEBELUM lebih tepat.

### Cacat untuk pembuat (bukti + saran)

1. Awal Ramadan 2027 ditulis 17 Feb 2027 (≈ tanggal 2026) dan tidak konsisten dengan Lebaran 10 Mar. Saran: di Langkah 1 wajibkan pemeriksaan konsistensi (Idul Fitri − awal Ramadan = 29/30 hari) dan larang frasa "sudah dicek sumber resmi" kecuali sumbernya dikutip; tambahkan tabel perkiraan Ramadan/Idul Fitri beberapa tahun ke depan di references dengan label perkiraan.
2. CTA berisi urgensi palsu ("stok terbatas", "harga belum naik", "buruan sebelum kehabisan") dan testimoni karangan ("order 5x"). Saran: tambahkan ke checklist "tidak ada urgensi/kelangkaan di CTA kecuali dari pengguna" (selaras naskah-live-jualan).
3. Skenario 1: klaim layanan karangan ("tanpa minimal berat", "jemput tanpa biaya tambahan"). Saran: ide konten yang menyebut syarat layanan pakai [isi: ...] bila tidak diberikan.
4. Tabel di chat menghilangkan kolom Platform & Status dari format output (masih ada di CSV). Saran: tegaskan kolom wajib atau izinkan ringkas dengan catatan.

### Cuplikan jualan

> Minta kalender sebulan, langsung dapat 30 baris lengkap (tanggal, hari, momen lokal, ide, hook, CTA) plus file CSV siap buka di Excel — dan jumlah video menyesuaikan kemampuan produksi Anda (3/minggu).

