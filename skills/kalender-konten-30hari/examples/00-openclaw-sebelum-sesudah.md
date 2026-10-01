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



## Uji ulang 2026-10-01

**Versi diuji:** 1.0.4 · **Penguji:** agent penguji independen (bukan pembuat) · OpenClaw lokal terisolasi, home baru `r6k-kalender-konten-30hari` (SEBELUM, tanpa skill) dan `r6-kalender-konten-30hari` (SESUDAH, skill ini saja), dibuat ulang per skenario. Pesan identik dengan uji pertama.

### Skenario 1 (ulang) — pesan sama persis

**SEBELUM (tanpa skill)** — tools: ['tool_search', 'memory_search', 'tool_call']

~~~~text
Siap, ini kalender konten November 2026 buat **Wangi Bersih** (laundry kiloan Depok, Rp7.000/kg, antar-jemput, order via WA) — khusus IG + WA Status, dengan budget 3 video/minggu.

**Pola kerja:**
- Video (Reels IG + repost WA Status) di hari **Senin, Rabu, Jumat** → total 13 video sebulan, pas rata-rata 3x/minggu.
- Hari lain cukup konten ringan: foto, banner promo, screenshot testimoni, atau polling stiker di WA Status (gak perlu edit video, 5 menit kelar).
- Saran syuting: rekam 3 video sekaligus tiap akhir pekan/awal minggu, baru dijadwalkan posting — biar gak kejar tayang tiap hari.

---

**MINGGU 1 (1–7 Nov)**
- Min 1: WA Status — quote pembuka bulan + jam buka/tutup
- **Sen 2 (VIDEO)**: Proses cuci kilat + promo "Welcome November" — ajak order sebelum baju numpuk
- Sel 3: IG Feed foto — banner harga Rp7.000/kg + gratis antar-jemput
- **Rab 4 (VIDEO)**: Behind the scene — sortir & pisah warna biar baju gak luntur
- Kam 5: WA Status — screenshot chat testimoni pelanggan
- **Jum 6 (VIDEO)**: "Weekend numpuk cucian? Tinggal WA, kami jemput!" (CTA antar-jemput)
- Sab 7: WA Status — promo "Sabtu-Minggu tetap jalan, order kapan aja"

**MINGGU 2 (8–14 Nov)**
- Min 8: WA Status — foto hasil lipatan rapi & wangi
- **Sen 9 (VIDEO)**: Musim hujan males jemur? Serahin ke Wangi Bersih (angle solusi)
- Sel 10: Hari Pahlawan — IG feed + WA Status: "Pahlawan rumah tangga, biar cucian kami yang urus" + promo spesial sehari
- **Rab 11 (VIDEO)**: Testimoni pelanggan (rekam langsung/voice over ulasan)
- Kam 12: WA Status — polling stiker "Wangi favorit: Lavender atau Bunga?"
- **Jum 13 (VIDEO)**: Proses packing rapi, wangi tahan lama — ala "unboxing" laundry
- Sab 14: WA Status — reminder area jangkauan antar-jemput Depok

**MINGGU 3 (15–21 Nov)**
- Min 15: IG Feed carousel — "5 Alasan Pilih Wangi Bersih"
- **Sen 16 (VIDEO)**: Edukasi cara order — screen record chat WA step by step
- Sel 17: WA Status — foto motor/armada antar-jemput
- **Rab 18 (VIDEO)**: Day in the life kurir antar-jemput keliling Depok
- Kam 19: WA Status — testimoni baru pelanggan
- **Jum 20 (VIDEO)**: FAQ — jawab "berapa lama proses?", "area mana aja?"
- Sab 21: WA Status — promo weekend "cucian numpuk, jemput hari ini juga"

**MINGGU 4 (22–28 Nov)**
- Min 22: IG Feed — foto before-after tempat cuci, kesan bersih & higienis
- **Sen 23 (VIDEO)**: Promo gajian — bonus/diskon kiloan jelang akhir bulan
- Sel 24: WA Status — countdown promo gajian (H-3, H-2, H-1)
- **Rab 25 (VIDEO)**: Testimoni/UGC kedua — bandingin worth-it-nya Rp7rb/kg
- Kam 26: Hari Guru Nasional — WA Status ucapan + opsional promo guru
- **Jum 27 (VIDEO)**: Proses cuci express buat yang mau traveling weekend
- Sab 28: WA Status — reminder kuota harian, "order cepat biar gak antre"

**MINGGU 5 (29–30 Nov)**
- Min 29: IG Feed carousel — recap testimoni & momen seru bulan ini
- **Sen 30 (VIDEO)**: Recap closing November + teaser promo awal Desember

---

**Tips cepat:**
- Semua video Reels tinggal di-screen record/share ulang ke WA Status, jadi 1 konten = 2 platform, hemat waktu.
- Hari non-video tetap WAJIB isi WA Status minimal 1x biar status gak kosong (foto produk/testimoni paling gampang).
- CTA tetap konsisten di tiap konten: "Order gampang, tinggal WA — jemput & antar gratis."

Mau aku bikinin juga draft caption lengkap + hashtag buat ke-13 video itu, atau template desain IG feed-nya?
~~~~

**SESUDAH (dengan skill 1.0.4)** — tools: ['read', 'ls', 'exec']

~~~~text
Ini dia — **Kalender Konten November 2026 — Laundry Wangi Bersih (Depok)**
Rp7.000/kg · Antar-jemput · Order via WA · Platform: **IG + WA Status**
Cek: maksimal 3 video/minggu (sudah pas, lihat kolom Format — hari lain cukup foto, bukan video).

| No | Tanggal | Hari | Momen | Pilar | Format | Ide Konten | Hook / Judul | CTA |
|---|---|---|---|---|---|---|---|---|
| 1 | 01 Nov | Minggu | Gajian tgl 1 | Promo | Foto | Banner promo cuci kiloan Rp7.000/kg, ajak beresin cucian numpuk | Gajian cair, cucian numpuk? Serahin aja | Order/jadwalkan jemput via WA |
| 2 | 02 Nov | Senin | | Hasil Cuci | Foto | Before-after cucian kotor → bersih wangi, rapi dilipat | Beda banget kan hasilnya? | Cek sendiri, order via WA |
| 3 | 03 Nov | Selasa | | Tips | **Video** | Tips pisahkan baju putih & warna biar nggak luntur | Baju putih luntur? Ini sebabnya | Simpan tipsnya, order via WA |
| 4 | 04 Nov | Rabu | | Promo | Foto | Foto timbangan + harga Rp7.000/kg, contoh hitungan | Rp7.000/kg aja, udah wangi rapi | Order lewat WA, kami jemput |
| 5 | 05 Nov | Kamis | | Testimoni | **Video** | Pelanggan cerita kenapa langganan (dengan izin) `[isi: rekam testimoni asli]` | Kata pelanggan tetap kami | Mau coba juga? Chat WA |
| 6 | 06 Nov | Jumat | | Antar Jemput | Foto | Kurir jemput cucian di depan rumah pelanggan | Nggak usah keluar rumah, kami jemput | Jadwalkan jemput via WA |
| 7 | 07 Nov | Sabtu | | Hasil Cuci | **Video** | Proses lipat & packing cucian rapi siap diantar | Rapi gini siap dianter ke rumahmu | Order cuci kiloan via WA |
| 8 | 08 Nov | Minggu | | Tips | Carousel | Tips simpan pakaian biar nggak apek musim hujan | Musim hujan, baju gampang apek? | Serahin ke kami, order via WA |
| 9 | 09 Nov | Senin | | Promo | Foto | Ajakan rutin cuci kiloan tiap minggu | Senin produktif, cucian beres | Chat WA buat jadwal rutin |
| 10 | 10 Nov | Selasa | Hari Pahlawan (peringatan — tanpa jualan) | Testimoni | **Video** | Ucapan Hari Pahlawan + apresiasi pelanggan & tim, tanpa penawaran apa pun | Selamat Hari Pahlawan | Terima kasih sudah percaya ke kami |
| 11 | 11 Nov | Rabu | Tanggal kembar 11.11 (cek kampanye marketplace) | Promo | Foto | Promo 11.11 `[isi: promo jika ada]`; kalau belum ada, ajak beresin cucian sebelum akhir pekan | 11.11, waktunya beres-beres cucian | Order lewat WA, cek promo 11.11 |
| 12 | 12 Nov | Kamis | | Antar Jemput | **Video** | POV kurir antar cucian bersih sampai depan pintu | Nyampe rumah udah wangi | Order antar jemput via WA |
| 13 | 13 Nov | Jumat | | Hasil Cuci | Foto | Seragam kerja/sekolah wangi rapi bebas noda | Seragam kerja wangi lagi | Order cuci kiloan via WA |
| 14 | 14 Nov | Sabtu | | Tips | **Video** | Tips hilangkan bau apek di lemari | Lemari bau apek? Coba ini | Cucian numpuk? Serahin lewat WA |
| 15 | 15 Nov | Minggu | | Promo | Foto | Promo akhir pekan, ajak beresin cucian sebelum minggu baru | Minggu santai, cucian beres duluan | Jadwalkan jemput akhir pekan via WA |
| 16 | 16 Nov | Senin | | Testimoni | Foto | Testimoni pelanggan (dengan izin) `[isi: foto & kutipan asli]` | Udah coba, langsung langganan | Gabung jadi pelanggan tetap, chat WA |
| 17 | 17 Nov | Selasa | | Antar Jemput | **Video** | Behind the scene tim siap-siap jemput cucian pagi | Pagi-pagi, tim udah siap jemput | Order jemput hari ini via WA |
| 18 | 18 Nov | Rabu | | Hasil Cuci | Foto | Cucian anak kos/karyawan rapi dilipat dalam kantong | Anak kos juga wajib coba ini | Order cuci kiloan via WA |
| 19 | 19 Nov | Kamis | | Tips | **Video** | Tips cara lipat baju biar nggak kusut | Biar baju nggak gampang kusut | Males ngelipat? Serahin lewat WA |
| 20 | 20 Nov | Jumat | Tanggal tua — nilai/hemat | Testimoni | Foto | Testimoni soal harga terjangkau di akhir bulan `[isi: kutipan asli]` | Akhir bulan, dompet aman | Tetap bisa cuci hemat, chat WA |
| 21 | 21 Nov | Sabtu | Tanggal tua | Antar Jemput | **Video** | Ingatkan hemat tenaga & waktu, cukup WA, kami jemput | Tanggal tua, hemat tenaga & waktu | Order jemput sekarang via WA |
| 22 | 22 Nov | Minggu | Tanggal tua | Hasil Cuci | Foto | Hitung-hitungan hemat dibanding nyuci sendiri | Itung-itung, lebih hemat lho | Coba hitung sendiri, chat WA |
| 23 | 23 Nov | Senin | Tanggal tua | Tips | Carousel | Tips hemat waktu & air dengan serahkan cucian | Biar nyuci nggak boros air & waktu | Serahin ke kami aja, chat WA |
| 24 | 24 Nov | Selasa | Tanggal tua | Testimoni | **Video** | Testimoni singkat soal harga bersahabat `[isi: rekam asli]` | Harga segini, hasilnya memuaskan | Yuk coba juga, chat WA |
| 25 | 25 Nov | Rabu | Hari Guru + gajian tgl 25 | Promo | Foto | Ucapan Hari Guru + ajakan beresin seragam sekolah pas gajian | Selamat Hari Guru! Gajian, cucian beres | Order cuci kiloan via WA |
| 26 | 26 Nov | Kamis | | Antar Jemput | **Video** | Proses packing cucian rapi sebelum diantar balik | Dibungkus rapi sebelum balik ke rumahmu | Order antar jemput via WA |
| 27 | 27 Nov | Jumat | | Hasil Cuci | Foto | Seprai & handuk bersih wangi | Seprai numpuk? Gampang, serahin aja | Order cuci kiloan via WA |
| 28 | 28 Nov | Sabtu | | Tips | **Video** | Tips simpan pakaian rapi biar awet wangi | Lemari rapi, baju awet wangi | Laundry numpuk? Order via WA |
| 29 | 29 Nov | Minggu | | Promo | Foto | Rekap ajakan beresin cucian sebelum Desember mulai sibuk | Akhir November, beresin cucian dulu | Order sekarang via WA |
| 30 | 30 Nov | Senin | | Testimoni | Foto | Rekap testimoni pelanggan selama November `[isi: kumpulan testimoni asli]` | Makasih udah percaya bulan ini | Yuk mulai langganan bulan depan, WA |

Sebaran pilar: Promo 7, Hasil Cuci 6, Tips 6, Testimoni 6, Antar Jemput 5 — jualan langsung ~23%, sisanya nilai/edukasi/hiburan.

📥 CSV sudah tersimpan: `kalender_wangibersih_november2026.csv` di workspace (pemisah koma, siap tempel ke Google Sheets).

💡 Tips eksekusi:
1. Shooting semua video (3/minggu = total 12 video) sekaligus tiap akhir pekan sebelumnya, pakai HP saja — cukup klip jemput, lipat, packing, dan quote testimoni.
2. Siapkan 1 folder foto "before-after" dan "hasil rapi dilipat" — bisa dipakai ulang untuk beberapa hari Promo/Hasil Cuci.
3. Minta izin tertulis singkat (japri WA) tiap kali pakai foto/kutipan pelanggan sebagai testimoni.
4. Tanggal 10 Nov (Hari Pahlawan) sengaja tanpa jualan — jangan diganti promo.
5. Cek tanggal 11.11 mendekati hari-H untuk promo marketplace terbaru biar bisa disesuaikan kontennya.

📝 Asumsi: gajian tgl 1 & 25 (default); belum ada info promo khusus 11.11 atau testimoni pelanggan asli — bagian itu saya tandai `[isi: ...]`, tinggal kamu isi.

Mau sekalian aku buatin caption lengkap untuk salah satu hari (misal hari 1 atau hari promo 11.11)?
~~~~

### Skenario 2 (ulang) — pesan sama persis

**SEBELUM (tanpa skill)** — tools: ['tool_search', 'memory_search', 'tool_call', 'web_fetch']

~~~~text
Siap, ini kalender kontennya. Beberapa catatan dulu sebelum tabelnya:

**Tanggal penting Ramadan–Lebaran 2027** (hasil hisab astronomis via API kalender Hijriah — Kemenag biasanya baru menetapkan resmi lewat Sidang Isbat H-1, jadi mungkin geser 1 hari, tapi aman dipakai buat rencana konten):
- 🌙 Awal Puasa (1 Ramadan 1448H): **Senin, 8 Februari 2027**
- 🎉 Lebaran/Idul Fitri (1 Syawal 1448H): **Selasa, 9 Maret 2027**

Jadi kalender 30 hari (20 Feb–21 Mar 2027) kamu ini pas banget mulai dari pertengahan Ramadan, nanjak ke 10 hari terakhir (masa pre-order parsel paling kenceng), Lebaran, sampai Syawal — momentumnya pas untuk jualan kurma & parsel.

## Kalender Konten 30 Hari — Kurma Barokah

| # | Tanggal | Hari | Momen | Tema Konten | Ide Format/Caption |
|---|---------|------|-------|-------------|---------------------|
| 1 | 20 Feb | Sab | Ramadan 13 | Pembuka kalender promo | Carousel "5 Jenis Kurma Favorit buat Takjil" |
| 2 | 21 Feb | Min | Ramadan 14 | Edukasi gizi | Reels: manfaat kurma buat buka puasa |
| 3 | 22 Feb | Sen | Ramadan 15 (pertengahan) | Promo tengah bulan | Flash sale kurma kiloan 24 jam |
| 4 | 23 Feb | Sel | Ramadan 16 | Testimoni | Repost story/review pelanggan |
| 5 | 24 Feb | Rab | Ramadan 17 (Nuzulul Qur'an) | Spesial religi | Ucapan + promo "kurma teman tadarus" |
| 6 | 25 Feb | Kam | Ramadan 18 | Behind the scene | Video proses packing kurma |
| 7 | 26 Feb | Jum | Ramadan 19 | Jumat Berkah | Promo paket sedekah takjil |
| 8 | 27 Feb | Sab | Ramadan 20 | **Buka pre-order parsel Lebaran** | Pengumuman + link order |
| 9 | 28 Feb | Min | Ramadan 21 (malam ganjil 1) | Itikaf & malam Lailatul Qadar | Konten reflektif + kurma bekal itikaf |
| 10 | 1 Mar | Sen | Ramadan 22 | Reveal produk | Unboxing isi paket parsel |
| 11 | 2 Mar | Sel | Ramadan 23 (malam ganjil) | Promo premium | Paket Ajwa/Medjool spesial |
| 12 | 3 Mar | Rab | Ramadan 24 | Edukasi pilihan | Carousel paket Silver/Gold/Platinum |
| 13 | 4 Mar | Kam | Ramadan 25 (malam ganjil) | Testimoni korporat | Review hampers kantor/instansi |
| 14 | 5 Mar | Jum | Ramadan 26 | Jumat Berkah + flash sale | Promo terbatas |
| 15 | 6 Mar | Sab | Ramadan 27 (malam ganjil, kuat Lailatul Qadar) | Konten spesial religi | Doa + promo parsel sedekah yatim |
| 16 | 7 Mar | Min | Ramadan 28 | **Reminder batas order** | CTA "H-2, pesan sekarang biar sampai sebelum Lebaran!" |
| 17 | 8 Mar | Sen | Ramadan 29 (puasa terakhir) | Countdown Lebaran | "Besok Lebaran!" + info jam toko tutup |
| 18 | 9 Mar | Sel | **HARI LEBARAN** | Ucapan Idul Fitri | "Selamat Idul Fitri 1448H, mohon maaf lahir batin" + info libur |
| 19 | 10 Mar | Rab | Syawal 2 | Halal bihalal | Foto tim + ucapan lanjutan |
| 20 | 11 Mar | Kam | Syawal 3 | Buka toko lagi | Info jam operasional + stok ready |
| 21 | 12 Mar | Jum | Syawal 4 | Promo after-Lebaran | "Lebaran belum berakhir" diskon sisa stok |
| 22 | 13 Mar | Sab | Syawal 5 | Oleh-oleh open house | Kurma buat tamu halal bihalal |
| 23 | 14 Mar | Min | Syawal 6 | Puasa Syawal | Tips kurma buka puasa sunnah |
| 24 | 15 Mar | Sen | Syawal 7 | Testimoni pasca-Lebaran | UGC pelanggan |
| 25 | 16 Mar | Sel | Syawal 8 | Interaksi | Giveaway kecil buat followers |
| 26 | 17 Mar | Rab | Syawal 9 | Edukasi | Cara simpan kurma biar awet |
| 27 | 18 Mar | Kam | Syawal 10 | Resep kreatif | Olahan kurma non-Lebaran (energy ball/smoothie) |
| 28 | 19 Mar | Jum | Syawal 11 | Jumat Berkah reguler | Promo mingguan |
| 29 | 20 Mar | Sab | Syawal 12 | Interaktif | Polling/Q&A produk favorit |
| 30 | 21 Mar | Min | Syawal 13 | Recap & teaser | Terima kasih + bocoran promo berikutnya |

## Jam Posting

Aku belum punya akses ke Insights IG akun kamu (belum ada integrasi/koneksi akun di sini), jadi ini **benchmark umum** untuk akun F&B Indonesia selama Ramadan–Lebaran, bukan data real akunmu:

- **Selama Ramadan (hari 1–17, 20 Feb–8 Mar):** 16.00–17.30 WIB (golden hour jelang buka puasa) dan 20.00–21.30 WIB (habis tarawih, orang santai scroll HP). Alternatif pagi: 05.00–06.00 (abis sahur sebelum tidur lagi).
- **Lebaran & Syawal (9–21 Mar):** 11.00–13.00 WIB (jam istirahat/kumpul) dan 19.30–21.00 WIB (malam santai).

Biar akurat, cek sendiri di akun kamu: Profesional Dashboard → Insights → "Aktivitas Followers" (ada jam-per-jam kapan followers paling online). Kirim screenshot-nya ke aku kalau mau, nanti aku bantu sesuaikan jadwal postingnya ke jam yang benar-benar pas buat akun kamu.
~~~~

**SESUDAH (dengan skill 1.0.4)** — tools: ['tool_search', 'read', 'exec', 'write']

~~~~text
Kalender konten 30 hari untuk **Kurma Barokah** (kurma & parsel Lebaran, Medan) sudah jadi. Dua hal penting dulu:

⚠️ **Tanggal 1 Ramadan & Idulfitri 2027 belum resmi** — sidang isbat Kemenag baru menentukan mendekati waktunya. Saya pakai *perkiraan kasar*: awal Ramadan 1448H ±8 Feb 2027, Idulfitri ±10 Mar 2027 (berarti 20 Feb–21 Mar 2027 ada di tengah Ramadan menuju Lebaran). **Cek lagi ke SKB 3 Menteri / pengumuman Kemenag mendekati Februari 2027** dan geser tanggal di kalender ini kalau meleset.

📊 **Jam posting rame**: saya tidak punya akses ke Instagram Insight toko Anda, jadi tidak bisa kasih angka pasti. Titik awal umum untuk akun lokal Indonesia: **siang ±11.30–13.00 (jam istirahat)** dan **malam ±19.00–21.00**. Untuk Ramadan khususnya, banyak akun F&B/kuliner lokal justru makin ramai di **jelang buka puasa (16.30–18.00)** dan **selepas tarawih (20.30–22.00)**. Ini perkiraan umum, bukan data akun Anda — cek Insight IG Anda sendiri (Profesional Dashboard → Insight → aktivitas pengikut) untuk angka pastinya, lalu sesuaikan jadwal ini.

## Kalender Konten Kurma Barokah — 20 Feb s.d. 21 Mar 2027
Pilar: Promo Parsel & Kurma (6 hari), Edukasi Kurma (6), Proses & Kemasan (6), Testimoni Pelanggan (6), Ucapan Ramadan Lebaran (6) | Platform: IG + TikTok + WA Status

| No | Tanggal | Hari | Momen | Pilar | Format | Ide Konten | Hook / Judul | CTA |
|---|---|---|---|---|---|---|---|---|
| 1 | 20 Feb 2027 | Sabtu | Tanggal tua | Edukasi Kurma | Carousel | Kenalan jenis kurma yang dijual (ajwa, medjool, sukari — [isi: jenis yg dijual]) & kegunaannya untuk takjil/parsel | Kurma apa yang cocok buat buka puasamu? | Simpan dulu, checkout pas gajian |
| 2 | 21 Feb 2027 | Minggu | Tanggal tua | Proses & Kemasan | Video proses | Proses sortir kurma lalu dikemas ke wadah sebelum dijual | Begini cara kami kemas kurma biar tetap segar | Tonton sampai habis |
| 3 | 22 Feb 2027 | Senin | Tanggal tua | Testimoni Pelanggan | Foto/Story | Testimoni (izin) pengalaman beli kurma untuk buka puasa keluarga | Kata pelanggan soal kurma kami | Cerita pengalamanmu di komentar |
| 4 | 23 Feb 2027 | Selasa | Tanggal tua | Ucapan Ramadan Lebaran | Bebas | Suasana toko menyambut pertengahan Ramadan, rak kurma & parsel mulai disiapkan | Ramadan sudah separuh jalan, semangat! | Mampir toko / chat WA |
| 5 | 24 Feb 2027 | Rabu | Tanggal tua | Edukasi Kurma | Carousel | Tips memilih kurma berkualitas: tekstur, warna, kemasan | Begini cara pilih kurma yang bagus | Simpan sebelum belanja |
| 6 | 25 Feb 2027 | Kamis | Gajian (25) | Promo Parsel & Kurma | Video+Story | Pilihan paket parsel Lebaran [isi: paket & harga], mulai pre-order | Baru gajian? Checklist parsel Lebaran! | Order via WA [isi: no. WA] |
| 7 | 26 Feb 2027 | Jumat | — | Proses & Kemasan | Video proses | Proses menyusun isi parsel [isi: isi parsel] jadi hampers rapi | Intip proses packing parsel kami | DM tanya pilihan isi parsel |
| 8 | 27 Feb 2027 | Sabtu | — | Testimoni Pelanggan | Foto/Story | Testimoni (izin) pelanggan korporat yang pesan parsel banyak untuk kantor | Kantor ini pesan parsel di sini | Mau pesan untuk kantor? Chat kami |
| 9 | 28 Feb 2027 | Minggu | — | Ucapan Ramadan Lebaran | Bebas | Suasana ngabuburit, ajak follower share menu buka puasa favorit | Ngabuburit sambil cari kurma favorit | Komen menu buka puasamu |
| 10 | 01 Mar 2027 | Senin | Gajian (1) | Promo Parsel & Kurma | Video+Story | Paket kurma kiloan [isi: ukuran & harga] untuk stok Ramadan-Lebaran | Gajian awal bulan, stok kurma sebulan | Order via WA |
| 11 | 02 Mar 2027 | Selasa | — | Edukasi Kurma | Carousel | Manfaat kurma untuk energi saat sahur & buka puasa | Kenapa kurma wajib ada pas sahur? | Simpan sebagai pengingat sahur |
| 12 | 03 Mar 2027 | Rabu | Tanggal kembar 3.3 (cek kampanye) | Promo Parsel & Kurma | Video+Story | Promo 3.3 untuk parsel [isi: detail promo]; jika belum ada, tampilkan katalog paket | Promo 3.3, checklist parsel Lebaran | Cek promo di WA |
| 13 | 04 Mar 2027 | Kamis | — | Proses & Kemasan | Video proses | Proses packing & kirim parsel untuk pelanggan luar kota [isi: jangkauan kirim] | Siap kirim parsel ke luar kota | Tanya ongkir via WA |
| 14 | 05 Mar 2027 | Jumat | — | Testimoni Pelanggan | Foto/Story | Testimoni (izin) kirim parsel ke keluarga luar kota karena tidak mudik | Kangen keluarga? Kirim kurma lewat kami | Mau kirim juga? Chat kami |
| 15 | 06 Mar 2027 | Sabtu | — | Ucapan Ramadan Lebaran | Bebas | Countdown santai menuju Lebaran (perkiraan), ajak share rencana Lebaran | Lebaran sebentar lagi (perkiraan) | Share rencana Lebaranmu |
| 16 | 07 Mar 2027 | Minggu | — | Promo Parsel & Kurma | Video+Story | Info batas order terakhir sebelum Lebaran [isi: tanggal batas] + katalog paket | Mau kirim sebelum Lebaran? Cek jadwalnya | Order & tanya jadwal kirim |
| 17 | 08 Mar 2027 | Senin | Hari Perempuan Internasional | Edukasi Kurma | Carousel | Ide kado kurma/parsel untuk ibu/istri/rekan perempuan | Parsel kurma, hadiah manis buat perempuan hebat | Pesan kado spesial via WA |
| 18 | 09 Mar 2027 | Selasa | — | Proses & Kemasan | Video proses | Suasana toko mulai ramai pesanan terakhir menjelang Lebaran (perkiraan) | Toko makin sibuk menjelang Lebaran | Masih bisa pesan, chat kami |
| 19 | 10 Mar 2027 | Rabu | **Idulfitri 1448H (perkiraan, cek SKB 3 Menteri)** — peringatan | Testimoni Pelanggan | Foto/Story | Ucapan Selamat Idulfitri + foto pelanggan (izin) momen Lebaran bersama keluarga — **tanpa promosi** | Selamat Idulfitri 1448 H | Mohon maaf lahir dan batin |
| 20 | 11 Mar 2027 | Kamis | Lebaran H+1 (perkiraan) — peringatan | Ucapan Ramadan Lebaran | Bebas | Ucapan silaturahmi, foto kebersamaan tim merayakan Lebaran — **tanpa promosi** | Taqabbalallahu minna wa minkum | Selamat merayakan bersama keluarga |
| 21 | 12 Mar 2027 | Jumat | — | Promo Parsel & Kurma | Video+Story | Info toko buka kembali pasca Lebaran, restock kurma & sisa parsel [isi: promo restock] | Kurma Barokah buka lagi, yuk re-stock | Kunjungi toko / order WA |
| 22 | 13 Mar 2027 | Sabtu | — | Edukasi Kurma | Carousel | Tips menyimpan kurma agar tahan lama setelah Lebaran | Kurma sisa Lebaran? Simpan begini | Share ke teman yang masih punya stok |
| 23 | 14 Mar 2027 | Minggu | — | Proses & Kemasan | Video proses | Suasana toko merapikan stok & kemasan pasca Lebaran | Beres-beres toko setelah Lebaran | Follow terus update toko |
| 24 | 15 Mar 2027 | Senin | — | Testimoni Pelanggan | Foto/Story | Testimoni (izin) pengalaman terima/kirim parsel dari toko | Parsel sampai tepat waktu | Terima kasih, order lagi via WA |
| 25 | 16 Mar 2027 | Selasa | — | Ucapan Ramadan Lebaran | Bebas | Ajakan halal bihalal, foto kumpul keluarga ngemil kurma | Masih suasana halal bihalal | Share momen halal bihalalmu |
| 26 | 17 Mar 2027 | Rabu | — | Promo Parsel & Kurma | Video+Story | Info kurma tetap tersedia di luar musim Lebaran [isi: varian & harga] | Ngidam kurma di luar Lebaran? Tetap ada | Order kapan saja via WA |
| 27 | 18 Mar 2027 | Kamis | — | Edukasi Kurma | Carousel | Ide kurma sebagai oleh-oleh acara/arisan/kunjungan keluarga di Medan | Kurma, oleh-oleh yang selalu pas | Pesan untuk oleh-oleh via WA |
| 28 | 19 Mar 2027 | Jumat | — | Proses & Kemasan | Video proses | Proses repacking kurma ke kemasan kecil/ekonomis untuk oleh-oleh | Kurma dikemas pas buat oleh-oleh | Tanya pilihan kemasan via WA |
| 29 | 20 Mar 2027 | Sabtu | Tanggal tua | Testimoni Pelanggan | Foto/Story | Testimoni (izin) tetap beli kurma di tanggal tua karena harga [isi: info harga] terjangkau | Tetap hemat, tetap ada kurma | Cek kurma harga bersahabat di WA |
| 30 | 21 Mar 2027 | Minggu | Tanggal tua | Ucapan Ramadan Lebaran | Bebas | Ucapan terima kasih ke pelanggan sepanjang Ramadan-Lebaran, ajak follow | Terima kasih sudah jadi bagian Ramadan kami | Follow terus biar gak ketinggalan promo |

📥 File tersimpan di workspace:
- `kurma-barokah/kalender.md` (tabel lengkap)
- `kurma-barokah/kalender.csv` (pemisah `;`, siap buka di Excel; pakai `,` kalau mau Google Sheets — bilang saja)

💡 **Tips eksekusi:**
1. Batch produksi konten Sabtu/Minggu (hari tanggal tua, lebih santai) agar stok konten cukup untuk hari sibuk pra-Lebaran.
2. Siapkan 1-2 foto produk/parsel berkualitas dari awal untuk dipakai ulang di beberapa hari.
3. Tanggal 19-20 Mar (Idulfitri) **jangan jadwalkan apapun yang berbau jualan** — cuma ucapan.
4. Cek Insight IG minggu pertama berjalan untuk tahu jam rame sebenarnya, lalu geser jadwal posting ke situ.
5. Pantau pengumuman Kemenag soal 1 Ramadan & Idulfitri 2027 mendekati Februari — siap geser tanggal hari ke-19/20 kalau beda dari perkiraan.

📝 **Asumsi yang saya pakai** (boleh dikoreksi):
- Gajian pelanggan tgl 25 & 1 (default)
- Kurma Barokah terima order via WA (nomor belum saya tahu — tandai `[isi: ...]`)
- Jangkauan kirim luar kota belum dikonfirmasi
- Belum ada data promo 3.3 spesifik — tabel pakai placeholder

Mau saya lanjutkan dengan caption lengkap untuk hari-hari penting (gajian, 3.3, Idulfitri)? Atau isi kolom `[isi: ...]` kalau Anda kasih detail paket/harga/nomor WA-nya sekarang.
~~~~

### Verifikasi (Python, penguji)

- 1 Nov 2026 = Minggu ✔; 10 Nov Hari Pahlawan, 11.11, 25 Nov Hari Guru ✔ (SESUDAH). SEBELUM menaruh Hari Guru di **Kamis 26 Nov** — salah (25 Nov).
- SESUDAH skenario 1: video di hari 3,5,7 / 10,12,14 / 17,19,21 / 24,26,28 = 3 per blok 7 hari, total 12 ✔; pilar Promo 7/30 = 23% ✔; Hari Pahlawan tanpa jualan ✔. Klaim layanan karangan lama ("tanpa minimal berat", "jemput tanpa biaya") **tidak muncul lagi**; testimoni & promo 11.11 memakai `[isi]`. Sisa ringan: "bebas noda", "hitung-hitungan hemat dibanding nyuci sendiri", "nggak boros air". SEBELUM: CTA "jemput & antar gratis", "promo spesial sehari" di Hari Pahlawan, "kuota harian ... biar gak antre" (urgensi karangan), "cuci express".
- Kalender Hijriah tabular (Python): 1 Ramadan 1448 H ≈ **8 Feb 2027**, 1 Syawal ≈ **10 Mar 2027** (selisih 30 hari). SESUDAH: "±8 Feb 2027", "Idulfitri ±10 Mar 2027", berlabel perkiraan + cek SKB/Kemenag ✔, konsisten ✔, tanpa klaim "sudah dicek" ✔. Hari dalam tabel (20 Feb Sabtu … 21 Mar Minggu) benar semua. CSV `kurma-barokah/kalender.csv` diperiksa penguji: 31 baris (header + 30), kolom Platform & Status ada.
- SESUDAH skenario 2 — **kesalahan baru:** Tips #3 menulis "Tanggal **19-20 Mar** (Idulfitri) jangan jadwalkan jualan", padahal tabelnya sendiri menaruh Idulfitri di **10–11 Mar** (19–20 adalah nomor baris). Selain itu kolom Momen 20–24 Feb diberi "Tanggal tua" padahal itu pertengahan Ramadan; momen Ramadan penting untuk toko parsel (THR ±H-7, Nuzulul Qur'an, 10 malam terakhir) tidak muncul sama sekali.
- SESUDAH: tidak ada urgensi palsu di CTA ("stok terbatas"/"buruan" hilang) ✔. Sisa: hook testimoni "Kantor ini pesan parsel di sini" dan "Parsel sampai tepat waktu" tanpa `[isi]` (diberi label "(izin)").
- SEBELUM skenario 2: 1 Ramadan 8 Feb, Idulfitri 9 Mar dengan catatan isbat — dalam rentang wajar; label "Ramadan 13 … 29" per baris konsisten dan momen Ramadan (Nuzulul Qur'an, malam ganjil, batas order) relevan. Minus: mengarang paket Silver/Gold/Platinum, flash sale, "promo terbatas", testimoni korporat, "diskon sisa stok"; tanpa CSV.
- Jam posting: kedua sisi jujur tidak punya akses Insight IG ✔.

### Status cacat lama

| Cacat uji pertama | Status |
|---|---|
| 1. Awal Ramadan 2027 = 17 Feb + "sudah dicek" | **Beres** — ±8 Feb, berlabel perkiraan, konsisten dengan ±10 Mar |
| 2. Urgensi palsu di CTA | **Beres** |
| 3. Klaim layanan karangan (skenario 1) | **Beres** (sisa klaim ringan) |
| 4. Kolom Platform/Status hilang dari tabel chat | **Belum** di chat (ada di CSV) — tidak termasuk catatan revisi |

**Regresi / cacat baru:** tanggal Idulfitri salah di Tips ("19-20 Mar"); momen Ramadan diganti "Tanggal tua".

### Skor

| | Sebelum | Sesudah | Alasan |
|---|---|---|---|
| Skenario 1 | 5.5 | 8.5 | SESUDAH 30 baris + CSV, kapasitas video dipatuhi, momen benar, tanpa klaim karangan besar; SEBELUM Hari Guru salah tanggal, "antar-jemput gratis" karangan, bukan kalender harian. |
| Skenario 2 | 7 | 7 | SESUDAH tanggal Ramadan/Lebaran kini benar & jujur, format & CSV terlengkap, tanpa urgensi palsu — tetapi Tips menyebut Idulfitri 19–20 Mar (salah) dan momen Ramadan hilang; SEBELUM lebih kaya momen Ramadan namun penuh promo karangan. |
| **Rata-rata** | **6.25** | **7.75** | |

**VERDIK: BELUM** — SESUDAH 7,75 (< 8) dan ada kesalahan tanggal di output (Idulfitri "19-20 Mar" di Tips). Cacat utama uji pertama (17 Feb + "sudah dicek", urgensi palsu) sudah beres.

Sisa untuk pembuat: (1) bila periode berada di Ramadan, script/Langkah kerja menandai "Ramadan hari ke-N (perkiraan)" di kolom Momen dan menambah THR (±H-7 Lebaran), Nuzulul Qur'an, 10 malam terakhir — jangan beri label "Tanggal tua" di tengah Ramadan; (2) checklist: setiap tanggal yang disebut di Tips/catatan harus sama dengan tabel (jangan memakai nomor baris sebagai tanggal).

### Cuplikan jualan (jujur)

> Minta kalender November, langsung dapat 30 baris (tanggal, hari, momen, ide, hook, CTA) + CSV, dengan 3 video per minggu persis sesuai kemampuan Anda — tanpa skill, bot menaruh Hari Guru di tanggal 26 dan menjanjikan "antar-jemput gratis" yang tidak pernah Anda tawarkan.


## Uji ulang 2026-10-01 (anti-karang)

**Versi diuji:** 1.0.5 · **Penguji:** agent penguji independen (bukan pembuat) · OpenClaw lokal terisolasi (`openclaw agent --local`, model router `komunitech`), home baru `r9k-kalender-konten-30hari` (SEBELUM, tanpa skill) dan `r9-kalender-konten-30hari` (SESUDAH, skill ini saja), dibuat ulang bersih per skenario. Pesan skenario 1–2 identik dengan uji pertama. Skenario 3 = varian baru (usaha kue kering, mulai 1 Maret 2027 — akhir Ramadan + Idulfitri di tengah periode, 2 video/minggu) untuk melihat apakah perbaikan tanggal bukan hafalan kasus Kurma Barokah.

Bukti script dijalankan: `tools` SESUDAH memuat `exec` di semua skenario; folder kerja agent berisi `fakta.txt` (persis pesan pengguna), `kalender.json`/`.md`/`.csv`, dan `jawaban.md` (file untuk `--cek-teks`). Penguji menjalankan ulang `buat_kalender.py --cek-teks <balasan final> --fakta-file <pesan>` dan menghitung tanggal Hijriah sendiri (algoritma tabular, Python).

### Skenario 1 (ulang9) — pesan sama persis

~~~~text
Bikinin kalender konten November 2026 buat laundry kiloan "Wangi Bersih" di Depok, Rp7.000/kg, bisa antar jemput, order lewat WA. Platform IG sama WA Status aja. Aku cuma sanggup bikin 3 video seminggu.
~~~~

**SEBELUM (tanpa skill)** — tools: ['memory_search', 'tool_call', 'write'] · kalender lengkap hanya di lampiran `kalender-konten-wangibersih-nov2026.md` (isinya dicatat di Verifikasi)

~~~~text
Kalender konten November 2026 buat Wangi Bersih udah jadi — disusun sesuai kapasitas 3 video/minggu (Senin-Rabu-Jumat), ditambah foto/carousel di hari lain dan WA Status santai di weekend, total 30 hari ter-cover.

**Ringkasan struktur:**
- **Video (IG Reels + WA Status):** Senin/Rabu/Jumat — before-after, tutorial order, proses jemput, testimoni, behind the scenes
- **Foto/Carousel (IG Feed + WA Status):** Selasa/Kamis — edukasi, FAQ, promo, testimoni
- **WA Status aja:** Sabtu/Minggu — promo singkat, reminder jadwal

Ada momen khusus (10 Nov Hari Pahlawan) dipakai buat promo, dan minggu terakhir ditutup rekap + teaser Desember.

File lengkap tersimpan di:

Mau aku bikinin juga draft caption lengkap per hari, atau ini cukup sebagai outline dulu?
~~~~

**SESUDAH (dengan skill 1.0.5)** — tools: ['read', 'write', 'exec', 'edit'] · lampiran: `kalender_nov2026.csv`

~~~~text
Siap, kalender konten November 2026 buat **Wangi Bersih** (laundry kiloan Depok) udah jadi. Sudah dicek-silang dengan fakta yang kamu kasih — hasilnya **LULUS**.

## Kalender Konten Wangi Bersih — 01 Nov 2026 s.d. 30 Nov 2026
Pilar: Promo & Harga (6 hari), Hasil Kerja (6 hari), Tips Perawatan (6 hari), Testimoni Pelanggan (6 hari), Proses & Tim (6 hari) | Platform: Instagram + WA Status

Kemampuan produksi 3 video/minggu sudah diikuti: cuma 13 dari 30 hari pakai video IG (tersebar rata ±3x/minggu), sisanya cukup foto buat WA Status aja — jadi targetmu realistis buat dijalankan.

| No | Tanggal | Hari | Momen | Pilar | Platform | Format | Ide Konten | Hook/Judul | CTA |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 01 Nov | Minggu | Hari gajian (tgl 1) | Promo & Harga | IG+WA | Video | Video pengingat selepas gajian: cucian numpuk langsung dibereskan, Rp7.000/kg + antar jemput | Gajian! Laundry numpuk langsung beresin | Chat WA jadwalin jemput |
| 2 | 02 Nov | Senin |  | Hasil Kerja | WA Status | Foto | Foto cucian bersih & wangi, dilipat rapi siap diantar | Hasil cucian rapi siap anter balik | Order via WA |
| 3 | 03 Nov | Selasa |  | Tips Perawatan | WA Status | Foto | Tips pisahkan baju putih & warna sebelum dicuci biar gak luntur | Baju putih kena luntur? Ini sebabnya | Tanya-tanya ke WA kami |
| 4 | 04 Nov | Rabu |  | Testimoni Pelanggan | IG+WA | Video | Testimoni pelanggan Depok soal layanan antar jemput [isi: kutipan asli, izin pelanggan] | Kata pelanggan soal Wangi Bersih | Gabung jadi pelanggan, chat WA |
| 5 | 05 Nov | Kamis |  | Proses & Tim | WA Status | Foto | Foto kurir menjemput cucian pelanggan di Depok | Gak perlu keluar rumah, kami jemput | Order antar jemput via WA |
| 6 | 06 Nov | Jumat |  | Promo & Harga | IG+WA | Video | Rincian harga Rp7.000/kg + antar jemput, cocok buat akhir pekan sibuk | Cuci kiloan cuma 7 ribu per kg | Order sekarang lewat WA |
| 7 | 07 Nov | Sabtu |  | Hasil Kerja | WA Status | Foto | Tumpukan cucian bersih siap diantar Sabtu pagi | Weekend bersih, cucian beres | Jemput cucianmu, chat WA |
| 8 | 08 Nov | Minggu |  | Tips Perawatan | WA Status | Foto | Tips simpan sementara cucian yang nunggu dijemput biar gak apek | Cucian numpuk? Simpan dulu begini | Jadwalin jemput via WA |
| 9 | 09 Nov | Senin |  | Testimoni Pelanggan | IG+WA | Video | Pelanggan Depok cerita order lewat WA gak ribet [isi: kutipan asli, izin pelanggan] | Order laundry gak pernah semudah ini | Coba order WA sekarang |
| 10 | 10 Nov | Selasa | Hari Pahlawan — ucapan, tanpa hard-selling | Proses & Tim | WA Status | Foto | Ucapan Hari Pahlawan, foto tim nuansa merah putih, khusus ucapan terima kasih | Selamat Hari Pahlawan dari Wangi Bersih | Terima kasih pelanggan setia |
| 11 | 11 Nov | Rabu | Tanggal kembar 11.11 — cek kampanye marketplace | Promo & Harga | IG+WA | Video | [isi: promo 11.11 kalau ada]. Kalau tidak: pengingat harga Rp7.000/kg + antar jemput | 11.11 saatnya beresin cucian numpuk | Order sekarang via WA |
| 12 | 12 Nov | Kamis |  | Hasil Kerja | WA Status | Foto | Cucian wangi rapi hasil laundry hari itu | Wangi tahan lama, ini buktinya | Order cuci kiloan, chat WA |
| 13 | 13 Nov | Jumat |  | Tips Perawatan | IG+WA | Video | Tips melipat baju rapi, sambil kenalin layanan cuci kiloan | Biar baju gak gampang kusut, gini caranya | Serahin ke Wangi Bersih, chat WA |
| 14 | 14 Nov | Sabtu |  | Testimoni Pelanggan | WA Status | Foto | Testimoni pelanggan soal antar jemput [isi: izin pelanggan] | Pelanggan puas, ini katanya | Jadi pelanggan berikutnya, chat WA |
| 15 | 15 Nov | Minggu |  | Proses & Tim | WA Status | Foto | Tim bersiap jemput cucian pelanggan pagi hari | Minggu pagi, siap jemput cucianmu | Order via WA, kami jemput |
| 16 | 16 Nov | Senin |  | Promo & Harga | IG+WA | Video | Pengingat awal minggu: Rp7.000/kg + antar jemput biar hemat waktu | Senin sibuk, laundry biar kami urus | Chat WA buat order |
| 17 | 17 Nov | Selasa |  | Hasil Kerja | WA Status | Foto | Cucian rapi siap diantar kembali | Rapi dan wangi, siap dianter balik | Order laundrymu, chat WA |
| 18 | 18 Nov | Rabu |  | Tips Perawatan | IG+WA | Video | Tips merawat baju favorit saat dicuci kiloan biar gak cepat rusak | Baju favorit perlu perawatan juga | Percayakan ke Wangi Bersih, chat WA |
| 19 | 19 Nov | Kamis |  | Testimoni Pelanggan | WA Status | Foto | Testimoni soal harga terjangkau Rp7.000/kg [isi: izin pelanggan] | Harga ramah kantong, kata pelanggan | Order sekarang via WA |
| 20 | 20 Nov | Jumat | Tanggal tua — konten hemat | Proses & Tim | IG+WA | Video | "Tanggal tua tetap laundry hemat": Rp7.000/kg + antar jemput | Tanggal tua, laundry tetap jalan | Order hemat via WA |
| 21 | 21 Nov | Sabtu | Tanggal tua — konten hemat | Hasil Kerja | WA Status | Foto | Cucian tetap bersih wangi meski budget ketat | Tanggal tua, cucian tetap wangi | Order hemat, chat WA |
| 22 | 22 Nov | Minggu | Tanggal tua — konten hemat | Tips Perawatan | WA Status | Foto | Tips atur jadwal cuci mingguan biar gak numpuk & hemat | Atur jadwal cuci, dompet lebih aman | Jadwalin rutin via WA |
| 23 | 23 Nov | Senin | Tanggal tua — konten hemat | Testimoni Pelanggan | IG+WA | Video | Testimoni pelanggan tetap pakai Wangi Bersih di tanggal tua [isi: izin pelanggan] | Tanggal tua tetap laundry, ini alasannya | Coba juga, chat WA |
| 24 | 24 Nov | Selasa | Tanggal tua — konten hemat | Proses & Tim | WA Status | Foto | Tim tetap jemput cucian pelanggan di tengah tanggal tua | Tetap jemput cucianmu, tanggal tua pun | Order via WA |
| 25 | 25 Nov | Rabu | Hari Guru Nasional; Hari gajian (tgl 25) | Promo & Harga | IG+WA | Video | Ucapan Hari Guru + pengingat gajian: cucian numpuk dibereskan Rp7.000/kg | Selamat Hari Guru, gajian juga nih | Order laundry lewat WA |
| 26 | 26 Nov | Kamis |  | Hasil Kerja | WA Status | Foto | Hasil cucian bersih wangi siap diantar | Udah wangi, udah rapi | Order cuci kiloan, chat WA |
| 27 | 27 Nov | Jumat |  | Tips Perawatan | IG+WA | Video | Tips simpan baju bersih biar wanginya tahan lama | Biar wangi laundry tahan lama | Serahin cucianmu, chat WA |
| 28 | 28 Nov | Sabtu |  | Testimoni Pelanggan | WA Status | Foto | Testimoni soal antar jemput yang praktis [isi: izin pelanggan] | Praktis, gak perlu keluar rumah | Coba order WA sekarang |
| 29 | 29 Nov | Minggu |  | Proses & Tim | WA Status | Foto | Tim tutup akhir bulan dengan jemputan terakhir | Akhir bulan, cucian tetap diurus | Order via WA |
| 30 | 30 Nov | Senin |  | Promo & Harga | IG+WA | Video | Rekap akhir bulan ajak coba cuci kiloan Rp7.000/kg + antar jemput | Akhir November, mulai kebiasaan baru | Order laundrymu via WA |

💡 **Tips eksekusi:**
- Syuting 3 video sekaligus di akhir pekan buat stok sepekan, biar gak rebutan waktu di hari kerja.
- Simpan foto hasil cucian rapi tiap hari sebagai stok WA Status — gak perlu foto dadakan tiap pagi.
- Cek jam ramai followers di Insight IG sendiri buat jam posting; titik awal: siang (±11.30-13.00) & malam (±19.00-21.00).
- Minta izin dulu sebelum pakai foto/testimoni pelanggan.
- Tanggal 11.11: putuskan dulu mau bikin promo khusus atau nggak — kalau ya, tulis syarat & batas waktunya jelas.

📝 **Asumsi:** gajian pelanggan pakai default tgl 25 & 1 (gak kamu sebutkan); promo 11.11 belum ditentukan jadi dikasih alternatif non-promo; testimoni/kutipan pelanggan perlu diisi dari testimoni asli dengan izin (belum kamu kasih).

File CSV (siap tempel ke Google Sheets, separator koma) juga udah aku simpan di workspace:

Mau aku bikinin caption lengkap buat salah satu hari dulu (misal hari gajian 1 Nov atau 11.11)?
~~~~

### Skenario 2 (ulang9) — pesan sama persis

~~~~text
Bikin kalender konten 30 hari mulai 20 Februari 2027 buat toko kurma & parsel Lebaran "Kurma Barokah" di Medan. Tanggal mulai puasa sama Lebaran 2027 langsung masukin aja ya, aku gak tau tanggalnya. Sekalian kasih tau jam posting yang paling rame di akun IG aku.
~~~~

**SEBELUM** — tools: ['tool_search', 'memory_search', 'tool_call']

~~~~text
Oke, catatan dulu soal data yang kepake supaya jelas basisnya:

**1. Tanggal Ramadan & Lebaran 2027** — saya gak bisa akses internet barusan (web search lagi off), jadi ini saya hitung manual dari kalender Hijriah (hisab), **estimasi**, bukan hasil sidang isbat Kemenag (baru diumumkan resmi H-1/H-2):
- **1 Ramadan 1448H ≈ Senin, 8 Februari 2027**
- **1 Syawal / Idul Fitri 1448H ≈ Rabu, 10 Maret 2027**
- Meleset ±1 hari itu wajar (tergantung rukyatul hilal), nanti update aja kalau Kemenag udah rilis resmi.

**2. Jam posting "paling rame"** — saya juga gak punya akses ke Insight akun IG kamu (gak ada data tersimpan di memori & gak bisa narik API IG dari sini). Yang saya kasih di bawah itu **benchmark umum** buat akun F&B/UMKM Indonesia, bukan data asli akunmu. Cek sendiri di **IG Insights → Audiens → Jam Paling Aktif** biar presisi, nanti tinggal geser jam di kalender ini.

---

## Kalender Konten 30 Hari — Kurma Barokah (20 Feb – 21 Mar 2027)

**Minggu 1 — Ramadan pertengahan (hari ke-13 s/d 19)**
| Tgl | Hari | Tema | Ide Konten | Jam Post |
|---|---|---|---|---|
| 20 Feb | Sab | Restock kurma fresh | Reel unboxing Medjool & Ajwa baru datang | 16:00 & 20:30 |
| 21 Feb | Min | Edukasi manfaat kurma | Carousel 5 manfaat kurma buat buka puasa | 10:00 & 17:00 |
| 22 Feb | Sen | Promo tengah Ramadan | Diskon 10% khusus 3 hari | 12:00 & 17:30 |
| 23 Feb | Sel | Produk unggulan | Foto/video parsel best seller | 17:00 & 20:00 |
| 24 Feb | Rab | Testimoni | Repost/review pelanggan | 16:30 & 20:00 |
| 25 Feb | Kam | Behind the scenes | Reel proses packing parsel | 17:00 & 20:30 |
| 26 Feb | Jum | Jumat Berkah | Promo spesial Jumat + sedekah kurma | 11:00 & 17:00 |

**Minggu 2 — 10 hari terakhir Ramadan (hari ke-20 s/d 26)**
| Tgl | Hari | Tema | Ide Konten | Jam Post |
|---|---|---|---|---|
| 27 Feb | Sab | Reminder 10 hari terakhir | "Siapin parsel Lebaran dari sekarang!" countdown mulai | 10:00 & 19:00 |
| 28 Feb | Min | Malam ganjil/Lailatul Qadar | Konten reflektif + soft selling | 10:30 & 20:30 |
| 1 Mar | Sen | Parsel custom | Promo bisa request isi parsel sendiri | 12:00 & 17:30 |
| 2 Mar | Sel | Flash sale | Diskon kejutan 24 jam | 16:00 & 20:00 |
| 3 Mar | Rab | Q&A interaktif | Tanya-jawab soal kurma & ongkir | 17:00 & 20:00 |
| 4 Mar | Kam | UGC/testimoni | Repost foto customer | 16:30 & 20:30 |
| 5 Mar | Jum | Deadline preorder H-7 | Reminder batas order luar kota | 11:00 & 17:00 |

**Minggu 3 — Jelang Lebaran & Hari-H (hari ke-27, 28, 29, 30, Idul Fitri)**
| Tgl | Hari | Tema | Ide Konten | Jam Post |
|---|---|---|---|---|
| 6 Mar | Sab | Malam 27 spesial | Bonus produk / flash promo | 10:00 & 21:00 |
| 7 Mar | Min | Deadline H-3 | Batas order pengiriman dalam kota Medan | 10:30 & 19:00 |
| 8 Mar | Sen | Last call H-2 | Order terakhir + info jam tutup toko | 12:00 & 18:00 |
| 9 Mar | Sel | Malam Takbiran (H-1) | Reel suasana takbiran + ucapan | 17:00 & 20:00 |
| **10 Mar** | **Rab** | **IDUL FITRI 🎉** | Ucapan Selamat Idul Fitri 1448H | 07:00 & 10:00 |
| 11 Mar | Kam | Lebaran hari 2 | Momen tim/toko, low-key | 10:00 & 19:00 |
| 12 Mar | Jum | Info libur | Reminder tanggal toko buka kembali | 11:00 & 17:00 |

**Minggu 4 — Pasca Lebaran, buka kembali (hari ke-4 s/d 12 Syawal)**
| Tgl | Hari | Tema | Ide Konten | Jam Post |
|---|---|---|---|---|
| 13 Mar | Sab | Teaser buka lagi | "Lebaran belum berakhir" promo | 10:00 & 19:00 |
| 14 Mar | Min | Toko buka resmi | Pengumuman + promo welcome back | 10:00 & 19:00 |
| 15 Mar | Sen | Puasa Syawal | Edukasi + stok kurma masih tersedia | 12:00 & 19:00 |
| 16 Mar | Sel | Promo sisa stok | Diskon kurma sisa Lebaran | 17:00 & 20:00 |
| 17 Mar | Rab | Testimoni pasca-Lebaran | Review pelanggan parsel terkirim | 16:30 & 20:00 |
| 18 Mar | Kam | Recap best seller | Produk paling laku selama Ramadan | 17:00 & 20:30 |
| 19 Mar | Jum | Jumat Berkah lanjutan | Promo normal mingguan | 11:00 & 17:00 |
| 20 Mar | Sab | Giveaway kecil | Ajak follow + undian penutup | 10:00 & 19:00 |
| 21 Mar | Min | Recap 30 hari | Ucapan terima kasih + teaser produk/rencana berikutnya | 10:30 & 19:00 |

---

**Catatan jam posting (benchmark umum, bukan data real akunmu):**
- Selama Ramadan: siang (11:00–12:00), sore jelang buka puasa (16:00–18:00 — ini biasanya puncak scroll), malam setelah tarawih (20:00–21:00).
- Setelah Lebaran (normal): siang istirahat (11:00–13:00) & malam santai (19:00–21:00).
- Weekend geser lebih pagi (09:00–11:00) karena orang gak buru-buru kerja.

Mau saya convert ini ke file Excel/Google Sheet biar gampang diisi caption lengkap & gambar?
~~~~

**SESUDAH** — tools: ['read', 'ls', 'exec', 'write'] · lampiran: `kurma-barokah-kalender/kalender.md` + `kalender.csv` (30 baris lengkap, kolom Platform & Status ada)

~~~~text
Lulus cek-silang (tanggal hari besar & klaim sesuai fakta). Hasilnya sudah lengkap, ini rangkuman untuk kamu.

## Kalender Konten Kurma Barokah — 20 Feb s.d. 21 Mar 2027 (30 hari)
Pilar: Promo & Parsel Lebaran (7 hari) · Proses Produksi & Packing (6) · Testimoni Pelanggan (6) · Tips Kurma & Edukasi (6) · Ramadan & Silaturahmi (5) | Platform: IG + TikTok + WA Status

**Catatan tanggal (perkiraan, belum resmi — cek sidang isbat Kemenag/SKB 3 Menteri mendekati waktunya):**
- Awal Ramadan 1448H: ±8 Feb 2027 (jadi periode 20 Feb masuk Ramadan hari ke-13–30)
- Idulfitri 1448H: ±10 Mar 2027 (10–11 Mar = hari H & H+1, diisi ucapan saja, tanpa promo)
- 12 Mar–21 Mar = fase pasca-Lebaran (info toko buka, halal bihalal, restock)

| No | Tanggal | Hari | Momen | Pilar | Ide Konten | Hook | CTA |
|---|---|---|---|---|---|---|---|
| 1 | 20 Feb | Sabtu | Ramadan h-13 | Promo | Reels buka pre-order parsel Lebaran | "Pre-order parsel Lebaran sudah dibuka!" | Order via [isi: kontak] |
| 5 | 24 Feb | Rabu | Nuzulul Qur'an | Ramadan & Silaturahmi | Konten reflektif malam Nuzulul Qur'an | "Malam Nuzulul Qur'an, momen istimewa" | Bagikan ke orang terdekat |
| 6 | 25 Feb | Kamis | Gajian tgl 25 | Promo | Parsel sesuai budget gajian | "Gajian udah cair, siapin parsel" | Order via [isi: kontak] |
| 9 | 28 Feb | Minggu | Awal 10 malam terakhir | Tips | Tips simpan kurma buat sahur | "Sahur 10 malam terakhir, kurma wajib ada" | Order via [isi: kontak] |
| 12 | 3 Mar | Rabu | THR cair ±H-7; tgl kembar 3.3 | Promo | Ajak order pakai THR | "THR cair, langsung checkout" | Order via [isi: kontak] |
| 18 | 9 Mar | Selasa | Malam takbiran | Proses | Packing terakhir sebelum hari H | "Takbiran tiba, parsel terakhir dikirim" | Cek status di [isi: kontak] |
| 19 | 10 Mar | Rabu | **Idulfitri** | Testimoni | Ucapan Lebaran, tanpa jualan | "Selamat Idulfitri dari Kurma Barokah" | Mohon maaf lahir & batin |
| 20 | 11 Mar | Kamis | Lebaran H+1 | Tips | Tips simpan sisa kurma, tanpa jualan | "Masih ada sisa kurma di rumah?" | — |
| 22 | 13 Mar | Sabtu | Pasca-Lebaran H+3 | Promo | Info toko buka lagi | "Kurma Barokah sudah buka lagi!" | Order via [isi: kontak] |
| 30 | 21 Mar | Minggu | — | Tips | Edukasi varian kurma [isi: varian yang dijual] | "Kenalan sama kurma favoritmu" | Tanya via [isi: kontak] |

(30 baris lengkap ada di file — lihat lampiran di bawah, tidak saya potong di sini biar tidak kepanjangan di chat.)

**Jam posting IG paling ramai:** paling akurat ya cek langsung di Insight/Professional Dashboard akunmu sendiri (Audience → Jam Aktif) — itu data real followers kamu, bukan tebakan saya. Sebagai patokan awal umum (bukan data akunmu):
- Siang: ±11.30–13.00 (jam istirahat)
- Malam: ±19.00–21.00
- Selama Ramadan biasanya geser lebih ramai sekitar jam buka puasa–habis tarawih: ±19.00–22.00

📝 Yang masih perlu kamu lengkapi (ditandai `[isi: ...]` di tabel):
- Kontak/nomor WA buat order (belum kamu sebutkan)
- Promo spesifik di hari gajian & tanggal kembar 3.3 (kalau ada)
- Varian kurma yang dijual (buat konten edukasi hari ke-30)

Tips eksekusi:
- Batch bikin video proses/packing sebelum Ramadan mulai sibuk
- Mulai minta izin testimoni pelanggan dari sekarang biar stok konten siap
- Jangan jadwalkan promo di 10–11 Mar (Idulfitri & H+1) — khusus ucapan
- Cek kampanye resmi marketplace dulu sebelum janji promo 3.3

File lengkap tersimpan di `kurma-barokah-kalender/`:

Mau saya buatin caption lengkap buat salah satu tanggal di atas (misal hari pre-order atau hari Idulfitri)?
~~~~

### Skenario 3 (BARU, varian) — kue kering Semarang, 1–30 Maret 2027, 2 video/minggu

~~~~text
Tolong bikinin kalender konten 30 hari mulai 1 Maret 2027 buat usaha kue kering "Dapur Bu Sari" di Semarang. Jualan nastar Rp95.000/toples, order lewat WA, kirim dalam kota aja. Platform IG sama TikTok, aku sanggupnya 2 video seminggu.
~~~~

**SEBELUM** — tools: ['tool_search', 'web_fetch', 'tool_call']

~~~~text
Oke, sebelum bikin kalendernya aku cek dulu — ternyata **1-30 Maret 2027 itu momen emas**: estimasi Lebaran (Idulfitri 1448H) jatuh **10-11 Maret 2027** (sesuai perkiraan hari libur nasional yang sudah diumumkan, plus cuti bersama 12 & 15 Maret). Jadi:

- **1-9 Maret** = 10 hari terakhir Ramadan → masa pre-order kue kering paling ramai
- **10-11 Maret** = Lebaran, toko libur
- **12-15 Maret** = masa open house / halal bihalal → restock & repeat order
- **16-30 Maret** = pasca-lebaran, waktunya bangun pelanggan tetap (bukan cuma musiman)

Aku susun kalendernya mengikuti fase ini. Format: 9 video (IG Reels + TikTok, repost sama) sesuai kapasitas 2x/minggu, sisanya feed/story ringan yang gampang dibikin sendiri. Semua CTA konsisten: **nastar Rp95.000/toples, order via WA, kirim dalam kota Semarang aja.**

**FASE 1 — Dorong Pre-Order (1-9 Maret)**
- Sen 1/3 (Feed): Foto nastar close-up + caption "H-9 Lebaran, udah booking belum?" + info harga & WA
- **Sel 2/3 (VIDEO #1):** Behind-the-scene bikin nastar (gulung adonan, isi selai, masuk oven, ASMR style). Hook: "Renyah, lumer di mulut — intip dapur Bu Sari"
- Rab 3/3 (Story): Polling "Nanas original atau mau coba varian keju?"
- Kam 4/3 (Feed): Testimoni pelanggan (screenshot WA/foto toples)
- **Jum 5/3 (VIDEO #2):** "3 alasan harus stok dari sekarang" — slot produksi terbatas jelang Lebaran
- Sab 6/3 (Feed): Foto kemasan toples, angle "cocok buat parcel/hampers Lebaran"
- Min 7/3 (Story): Countdown "H-3 sebelum pre-order tahap 1 ditutup"
- Sen 8/3 (Feed, libur Nyepi — bukan hari toko tutup): Reminder stok terbatas + nomor WA jelas
- **Sel 9/3 (VIDEO #3):** "H-1 Lebaran, LAST CALL!" — cepat & energik, batas order terakhir hari ini

**FASE 2 — Lebaran, toko libur (10-11 Maret)**
- Rab 10/3 (Feed): Ucapan "Selamat Idulfitri 1448H, Mohon Maaf Lahir Batin" — tanpa jualan
- Kam 11/3 (Story): Ucapan lanjutan / repost momen hangat, tetap soft, no hard-sell

**FASE 3 — Buka Lagi, Open House Season (12-15 Maret)**
- **Jum 12/3 (VIDEO #4):** "Dapur Bu Sari buka lagi!" — restock fresh, pas buat open house/halal bihalal
- Sab 13/3 (Feed): Foto meja open house dengan nastar sebagai sajian andalan
- Min 14/3 (Story): Testimoni "masih fresh walau abis lebaran"
- Sen 15/3 (Feed, cuti bersama): "Stok terbatas pasca-lebaran, buruan order" — banyak permintaan susulan

**FASE 4 — Sustain & Bangun Langganan Tetap (16-30 Maret)**
- **Sel 16/3 (VIDEO #5):** Kompilasi review/testimoni jujur pelanggan
- Rab 17/3 (Feed): Edukasi bahan premium yang dipakai
- Kam 18/3 (Story): Q&A — jawab pertanyaan soal cara order & area kirim
- **Jum 19/3 (VIDEO #6):** Posisikan nastar sebagai jajanan harian, bukan cuma musiman lebaran
- Sab 20/3 (Feed): Lifestyle shot — nastar nemenin ngopi santai
- Min 21/3 (Story): Polling "Nastar favorit buat nemenin ngopi/teh?"
- Sen 22/3 (Feed): Proses packing & kirim dalam kota, tunjukkan rapi & cepat
- **Sel 23/3 (VIDEO #7):** FAQ — harga, cara order, area kirim, daya tahan toples
- Rab 24/3 (Feed): Repost UGC kalau ada pelanggan posting nastar di story mereka
- Kam 25/3 (Story): Cerita personal Bu Sari lagi packing pesanan
- **Jum 26/3 (VIDEO #8):** Mini promo akhir bulan (mis. beli 3 toples gratis ongkir dalam kota)
- Sab 27/3 (Feed): Foto produk + harga jelas, CTA order reguler
- Min 28/3 (Story): Recap "makasih udah support Maret ini!" + testimoni singkat
- Sen 29/3 (Feed): Teaser konten/promo bulan depan
- **Sel 30/3 (VIDEO #9):** Wrap-up bulan Maret, ajakan follow terus buat update produk

**Tips praktis:**
- Jam posting disaranin 10-11 pagi atau 16-18 sore (jam orang scroll santai/mikir makan)
- Pin highlight IG khusus "Cara Order" biar link WA selalu gampang ditemu
- Hashtag campuran: #NastarSemarang #DapurBuSari #KueKeringLebaran #NastarEnak #OlehOlehSemarang #UMKMSemarang
- Video Mar 9 & Mar 12 paling krusial — itu titik deadline order dan titik buka-lagi, jangan sampai telat upload

Mau aku bikinin draft caption lengkap per video juga, atau versi file (Google Sheet/Doc) biar gampang dicoret-coret?
~~~~

**SESUDAH — keandalan:** skenario ini dijalankan **4 kali** dengan skill (home & sesi baru tiap kali); SEBELUM berhasil pada percobaan pertama.
1. Percobaan 1: tools jalan (file `kalender_isi.json`, `jawaban.md` 30 baris sudah ditulis di workspace) tetapi **tidak ada balasan** — agent kena batas waktu 900 detik (rc=124).
2. Percobaan 2 & 3: `The model did not produce a response before the model idle timeout…` — berhenti setelah agent menulis kerangka JSON besar (±12,8 KB) dan hendak menulis isi 30 baris sekaligus. Uji "Halo" di home tanpa skill segera sesudahnya berjalan normal (jadi router tidak sedang mati).
3. Percobaan 4: berhasil dalam 5,5 menit — balasan di bawah.

**SESUDAH (percobaan 4)** — tools: ['read', 'ls', 'exec', 'write', 'edit'] · file kerja: `dapur-bu-sari/fakta.txt`, `kalender.json/.md/.csv`, `jawaban.md`

~~~~text
Oke, ini kalender konten 30 hari buat **Dapur Bu Sari** (nastar Rp95.000/toples, order WA, kirim dalam kota Semarang), 1–30 Maret 2027.

**Catatan penting dulu:** periode ini pas banget nyentuh akhir Ramadan sampai Idulfitri — tanggalnya masih **perkiraan** (nunggu sidang isbat/SKB 3 Menteri), jadi pantau pengumuman resminya nanti ya. Perkiraan: akhir Ramadan ~8-9 Maret, Idulfitri ~10 Maret 2027.

Pilar: Promo Nastar (9 hari), Proses Dapur (6 hari), Tips Kue Kering (5 hari), Cerita Semarang (5 hari), Testimoni Pelanggan (5 hari) | Platform: IG + TikTok

| No | Tanggal | Hari | Momen | Pilar | Platform | Format | Ide Konten | Hook / Judul | CTA |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 01 Mar | Senin | Ramadan h-22 (perkiraan); Gajian tgl 1 | Promo Nastar | IG | Foto/Carousel | Foto toples nastar + harga Rp95.000/toples, cara order WA, cocok THR/gajian awal bulan | Gajian tanggal 1? Saatnya stok nastar | Order via WA, kirim dalam kota Semarang |
| 2 | 02 Mar | Selasa | Ramadan h-23 (perkiraan) | Proses Dapur | IG | Foto/Carousel | Proses membuat adonan nastar di dapur | Sebelum jadi nastar, adonannya begini | Chat WA buat tanya-tanya |
| 3 | 03 Mar | Rabu | Ramadan h-24; Tanggal kembar 3.3 | Promo Nastar | **IG+TikTok** | **Video** | Proses isi selai nanas sampai siap panggang + info harga | Isi nanasnya padat, bukan cuma manis doang | Order lewat WA sekarang |
| 4 | 04 Mar | Kamis | Ramadan h-25 (perkiraan) | Tips Kue Kering | IG | Carousel | Tips simpan nastar di toples kedap udara biar renyah | Biar nastar awet renyah, begini caranya | Simpan postingan ini |
| 5 | 05 Mar | Jumat | Ramadan h-26 (perkiraan) | Cerita Semarang | IG | Foto/Carousel | Ngemil nastar sambil ngopi sore, toko di Semarang, kirim dalam kota | Sore-sore, teman ngopinya nastar | Chat WA ya |
| 6 | 06 Mar | Sabtu | Ramadan h-27 (perkiraan) | Testimoni Pelanggan | **IG+TikTok** | **Video** | Proses packing pesanan siap kirim dalam kota | Pesanan hari ini siap dikirim | Order via WA |
| 7 | 07 Mar | Minggu | Ramadan h-28 (perkiraan) | Promo Nastar | IG | Foto/Carousel | Foto nastar + harga, camilan akhir pekan sambil nunggu buka puasa | Camilan buka puasa, ada nastar juga | Order sekarang via WA |
| 8 | 08 Mar | Senin | Ramadan h-29; Hari Perempuan Internasional | Proses Dapur | IG | Foto/Carousel | Proses manggang nastar sampai keemasan, usaha dijalankan Bu Sari | Dari dapur Bu Sari, satu per satu dipanggang | Dukung usaha lokal, order WA |
| 9 | 09 Mar | Selasa | Ramadan h-30; H-1 Lebaran (perkiraan) | Promo Nastar | IG | Foto/Carousel | Pre-order terakhir sebelum libur Lebaran + harga + [isi: batas waktu order] | H-1 Lebaran, nastar sudah di tangan? | Pesan sekarang via WA |
| 10 | 10 Mar | Rabu | **Idulfitri (perkiraan) — tanpa hard-selling** | Cerita Semarang | **IG+TikTok** | **Video** | Ucapan Selamat Idulfitri dari Dapur Bu Sari, tanpa jualan | Selamat Idulfitri dari Dapur Bu Sari | Mohon maaf lahir dan batin |
| 11 | 11 Mar | Kamis | Lebaran H+1 (perkiraan) — tanpa hard-selling | Testimoni Pelanggan | IG | Foto/Carousel | Foto suasana meja Lebaran dengan toples nastar, ucapan hangat | Masih suasana Lebaran, nastar nemenin | Selamat Lebaran, maaf lahir batin |
| 12 | 12 Mar | Jumat | Pasca-Lebaran H+2 | Promo Nastar | IG | Foto/Carousel | Pengumuman buka lagi + [isi: tanggal mulai layani] + harga | Dapur Bu Sari sudah buka lagi | Order via WA |
| 13 | 13 Mar | Sabtu | Pasca-Lebaran H+3 | Proses Dapur | **IG+TikTok** | **Video** | Restock bahan, mulai produksi lagi | Dapur mulai ngebul lagi pasca Lebaran | Chat WA sekarang |
| 14 | 14 Mar | Minggu | Pasca-Lebaran H+4 | Tips Kue Kering | IG | Carousel | Tips habiskan stok nastar sisa Lebaran biar tak mubazir | Nastar Lebaran masih sisa? Coba ini | Mau nastar baru? Order WA |
| 15 | 15 Mar | Senin | Pasca-Lebaran H+5 | Cerita Semarang | IG | Foto/Carousel | Suasana halal bihalal keluarga dengan nastar | Halal bihalal belum lengkap tanpa nastar | Order nastarnya di WA |
| 16 | 16 Mar | Selasa | Pasca-Lebaran H+6 | Testimoni Pelanggan | IG | Foto/Carousel | Foto kemasan toples baru dikirim ke pelanggan (dengan izin) | Satu toples lagi sampai ke pelanggan | Giliran kamu? Order WA |
| 17 | 17 Mar | Rabu | Pasca-Lebaran H+7 | Promo Nastar | **IG+TikTok** | **Video** | Unboxing toples Rp95.000, tampilkan tekstur dari dekat | Intip isi toples nastar dari dekat | Order via WA sekarang |
| 18 | 18 Mar | Kamis | Pasca-Lebaran H+8 | Proses Dapur | IG | Foto/Carousel | Proses cetak bentuk nastar sebelum panggang | Bentuknya dicetak satu-satu | Order via WA |
| 19 | 19 Mar | Jumat | Pasca-Lebaran H+9 | Tips Kue Kering | IG | Carousel | Cara bedakan nastar yang baru dibuka dari warna & aroma | Nastar yang baru dibuka itu ciri-cirinya begini | Mau coba? Order WA |
| 20 | 20 Mar | Sabtu | Pasca-Lebaran H+10 | Cerita Semarang | **IG+TikTok** | **Video** | Suasana akhir pekan di Semarang nikmatin nastar, ajak follower share momen | Akhir pekan di Semarang, ngemil apa? | Share momen, tag Dapur Bu Sari |
| 21 | 21 Mar | Minggu | Pasca-Lebaran H+11 | Testimoni Pelanggan | IG | Foto/Carousel | Repost chat WA pelanggan yang order ulang (dengan izin) | Pelanggan order lagi | Mau coba juga? Order WA |
| 22 | 22 Mar | Senin | Pasca-Lebaran H+12 | Promo Nastar | IG | Foto/Carousel | Foto nastar siap kirim dalam kota + harga | Ngemil sore ini, nastar aja | Order via WA |
| 23 | 23 Mar | Selasa | Pasca-Lebaran H+13 | Proses Dapur | IG | Foto/Carousel | Proses menata nastar ke toples sebelum dikirim | Sebelum dikirim, ditata rapi dulu | Chat WA sekarang |
| 24 | 24 Mar | Rabu | Pasca-Lebaran H+14 | Tips Kue Kering | **IG+TikTok** | **Video** | Tips menyajikan nastar untuk tamu di rumah + harga | Ada tamu dadakan? Nastar solusinya | Stok dari sekarang, order WA |
| 25 | 25 Mar | Kamis | Gajian tgl 25 | Promo Nastar | IG | Foto/Carousel | Foto toples nastar, ajak order bertepatan gajian | Gajian tanggal 25, waktunya self-reward | Order nastar via WA |
| 26 | 26 Mar | Jumat | — | Cerita Semarang | IG | Foto/Carousel | Cerita kenapa Dapur Bu Sari rutin bikin nastar tiap bulan di Semarang | Kenapa nastar selalu dicari-cari? | Cari tahu rasanya, order WA |
| 27 | 27 Mar | Sabtu | — | Testimoni Pelanggan | **IG+TikTok** | **Video** | Proses terima & kemas pesanan dari chat WA sampai siap kirim | Dari chat WA sampai siap kirim, begini alurnya | Order gampang, tinggal chat WA |
| 28 | 28 Mar | Minggu | — | Promo Nastar | IG | Foto/Carousel | Foto nastar camilan santai akhir pekan + harga | Minggu santai, ditemani nastar | Order via WA buat besok dikirim |
| 29 | 29 Mar | Senin | — | Proses Dapur | IG | Foto/Carousel | Proses siapkan bahan baku untuk batch berikutnya | Awal minggu, dapur mulai sibuk lagi | Chat WA |
| 30 | 30 Mar | Selasa | — | Tips Kue Kering | IG | Carousel | Rekap tips seputar nastar sebulan ini | Rangkuman tips nastar sebulan ini | Simpan postingan & order WA |

**💡 Tips eksekusi:**
- 2 video/minggu (IG+TikTok) sudah ditaruh di hari No. 3, 6, 10, 13, 17, 20, 24, 27 — hari lain cukup foto/carousel IG aja, sesuai kemampuan produksimu.
- Syuting video sekaligus di akhir pekan buat beberapa hari ke depan (batch), jangan kejar tayang harian.
- Siapin stok foto toples nastar dari berbagai angle di awal bulan buat hari-hari non-video.
- Cek Insight IG/Analytics TikTok sendiri untuk tahu jam posting paling ramai di akunmu.
- Pantau pengumuman resmi tanggal Idulfitri (SKB 3 Menteri/sidang isbat) menjelang Maret 2027, karena tanggal di kalender ini masih perkiraan ±1 hari.

**📝 Asumsi:**
- Gajian pelanggan dipakai default tgl 25 & 1.
- Belum ada info promo khusus Lebaran/THR darimu, jadi baris 9 & 12 ditandai `[isi: ...]` — tinggal kamu lengkapi sebelum posting.
- Produksi 2 video/minggu IG+TikTok, hari lain IG saja (foto/carousel).

File CSV siap tempel ke Excel/Spreadsheet tersimpan di:
📥 `/opt/ochome/.openclaw/workspace/dapur-bu-sari/kalender.csv` (pemisah `;`, cocok Excel Indonesia — kalau mau pakai Google Sheets bisa aku bikinin versi pemisah koma juga).

Mau lanjut aku bikinin caption lengkap buat hari-hari tertentu (misalnya hari video atau hari Lebaran)?
~~~~

### Verifikasi (Python, penguji)

- **Hijriah 1448 H (tabular, dihitung penguji):** 1 Ramadan = **Senin 8 Feb 2027**, 17 Ramadan = 24 Feb, 21 Ramadan = 28 Feb, 1 Syawal = **Rabu 10 Mar 2027** (Ramadan 30 hari). Hari: 1 Nov 2026 Minggu, 20 Feb 2027 Sabtu, 1 Mar 2027 Senin, 10 Mar 2027 Rabu, 21 Mar 2027 Minggu, 30 Mar 2027 Selasa — semua tabel SESUDAH benar.
- **S2 SESUDAH:** "Ramadan h-13" di 20 Feb ✔, Nuzulul Qur'an 24 Feb ✔, awal 10 malam terakhir 28 Feb ✔, THR ±H-7 = 3 Mar ✔, takbiran 9 Mar ✔, Idulfitri 10 Mar & H+1 tanpa jualan ✔, berlabel perkiraan + sidang isbat/SKB ✔; **Tips memakai 10–11 Mar** (cacat "19–20 Mar" beres) ✔; tidak ada "Tanggal tua" di tengah Ramadan ✔. `--cek-teks` pada balasan+lampiran: 1 GAGAL **palsu** (script menganggap kalimat penutup "…misal hari pre-order atau hari Idulfitri" sebagai tanggal Idulfitri 20 Feb) — bukan kesalahan output; catatan untuk pembuat.
- **S3 SESUDAH:** 1 Mar = "Ramadan h-22" ✔ (8 Feb + 21 hari), Idulfitri ±10 Mar ✔, video di No. 3, 6, 10, 13, 17, 20, 24, 27 = tepat 2 per minggu (Senin–Minggu) ✔; Idulfitri & H+1 tanpa jualan ✔; `--cek-teks`: LULUS (0 GAGAL). Asumsi gajian 25 & 1 disebut ✔.
- **S1 SESUDAH:** video di No. 1,4,6 / 9,11,13 / 16,18,20 / 23,25,27 / 30 → ≤ 3 per minggu ✔ (13 video); Hari Pahlawan 10 Nov tanpa hard-selling ✔; 11.11 dengan `[isi: promo]` ✔; Hari Guru 25 Nov (Rabu) ✔; kolom Platform kini ada di chat ✔. `--cek-teks`: LULUS (0 GAGAL, 1 CEK "favorit" = "baju favorit", wajar). Jam posting ±11.30–13.00 / 19.00–21.00 = saran awal dari references, disebut "perkiraan, cek Insight" ✔.
- **Fakta karangan SESUDAH (sisa):** S1 hook "Wangi tahan lama, ini buktinya" (klaim kecil). S2: "Pre-order parsel Lebaran sudah dibuka", "Kurma Barokah sudah buka lagi!" (mengandaikan toko tutup), "tempat produksi Kurma Barokah, Medan", platform TikTok & WA Status ditambahkan tanpa ditanya dan tidak di Asumsi. **S3: "Isi nanasnya padat, bukan cuma manis doang", "Bentuknya dicetak satu-satu", "Order via WA buat besok dikirim"** — klaim produk & janji pengiriman yang tidak pernah disebut pengguna dan **lolos** `cek_fakta.py`.
- **SEBELUM:** S1 (lampiran) "antar-jemput **gratis** area Depok", "diskon/bonus ongkir Hari Pahlawan", "deterjen & pewangi premium", promo referral; Hari Guru tidak ada; di chat hanya ringkasan. S2: tanggal 8 Feb/10 Mar kali ini benar, tetapi mengarang Medjool & Ajwa, diskon 10%, flash sale, giveaway, "promo sisa stok", jadwal tutup toko, dan jam posting presisi per baris (16:00 & 20:30) — 3 GAGAL `cek_fakta`. S3: Idulfitri 10–11 Mar benar, tetapi mengklaim "sesuai perkiraan hari libur nasional **yang sudah diumumkan**, plus cuti bersama 12 & 15 Maret" dan "8/3 libur Nyepi" (tidak dapat diverifikasi penguji; dinyatakan seolah resmi), "slot produksi terbatas", "stok terbatas", "gratis ongkir", "bahan premium", "varian keju" — 5 GAGAL.

### Status cacat lama

| Cacat | Status |
|---|---|
| Awal Ramadan 2027 salah + "sudah dicek" | **Beres** (±8 Feb, perkiraan) — juga benar di varian S3 |
| Urgensi palsu di CTA | **Beres** (S1–S3 tanpa "stok terbatas/buruan") |
| Klaim layanan karangan (S1) | **Beres** ("antar-jemput gratis"/"tanpa minimal" tidak muncul) |
| Kolom Platform/Status di chat | **Sebagian** — Platform ada; Status hanya di CSV/lampiran |
| Idulfitri "19–20 Mar" di Tips (uji ulang ke-1) | **Beres** (10–11 Mar) |
| "Tanggal tua" di tengah Ramadan, momen Ramadan hilang | **Beres** (Ramadan hari ke-N, Nuzulul Qur'an, 10 malam terakhir, THR, takbiran) |

**Regresi / cacat baru:** (1) **Keandalan** — varian S3 gagal membalas pada 3 dari 4 percobaan (timeout 900 dtk / model idle timeout) saat agent menulis JSON 30 baris sekaligus; bagi member di Telegram itu berarti tidak ada jawaban. (2) Klaim produk & janji kirim karangan di S3 ("isi nanasnya padat", "besok dikirim") yang tidak tertangkap `cek_fakta.py`. (3) S2 di chat hanya 10 baris kunci (30 baris lengkap dikirim sebagai lampiran .md + .csv) — dapat diterima, tetapi lebih ringkas dari uji sebelumnya.

### Skor

| | Sebelum | Sesudah | Alasan |
|---|---|---|---|
| Skenario 1 | 5 | 8.5 | SESUDAH 30 baris di chat + CSV, 3 video/minggu dipatuhi, momen & tanggal benar, `[isi]` untuk promo/testimoni; sisa "wangi tahan lama". SEBELUM cuma ringkasan di chat, "antar-jemput gratis" & diskon karangan. |
| Skenario 2 | 6.5 | 8 | SESUDAH tanggal & momen Ramadan lengkap dan jujur (perkiraan), Tips konsisten, jam posting jujur; minus pre-order/"buka lagi"/platform tambahan tanpa ditanya, tabel chat dipangkas. SEBELUM tanggal benar tapi penuh produk & promo karangan. |
| Skenario 3 (varian) | 5.5 | 7 | SESUDAH tanggal, kapasitas, label perkiraan benar; tetapi klaim produk & janji kirim dikarang dan 3/4 percobaan tidak membalas. SEBELUM klaim "sudah diumumkan" + urgensi/ongkir karangan. |
| **Rata-rata** | **5.67** | **7.83** | |

**VERDIK: BELUM (nyaris)** — perbaikan tanggal sudah kokoh (benar di kasus lama **dan** varian baru, tanpa klaim "resmi"), urgensi palsu hilang, dan script cek benar-benar dijalankan. Tetapi varian S3 masih memuat fakta karangan yang akan diposting ("isi nanasnya padat", "dicetak satu-satu", "besok dikirim") dan **gagal membalas pada 3 dari 4 percobaan** — dua syarat LULUS (tanpa fakta karangan; andal untuk awam) belum terpenuhi.

Sisa untuk pembuat: (1) keandalan — minta agent mengisi JSON per blok (mis. 10 baris per tulis) atau sediakan `--isi` dari CSV/teks sederhana agar tidak satu panggilan raksasa; uji 3× berturut-turut di OpenClaw untuk periode 30 hari dengan Ramadan; (2) Langkah 0: kualitas produk ("padat", "renyah", "dicetak satu-satu") dan janji layanan ("besok dikirim", "pre-order", "toko tutup/buka lagi") hanya bila disebut pengguna — tambahkan pola ke `cek_fakta.py` (`besok\s+dikirim`, `pre-?order`, `buka\s+lagi`, kata sifat rasa/tekstur); (3) platform yang tidak disebut pengguna → tanyakan atau tulis di Asumsi; (4) `--cek-teks`: jangan menganggap tanggal dari kalimat lain di baris yang sama (GAGAL palsu S2).

### Cuplikan jualan (jujur)

> Tanpa skill, bot menulis "Lebaran 10–11 Maret sesuai libur nasional yang sudah diumumkan" dan menjanjikan "gratis ongkir" yang tidak pernah Anda tawarkan; dengan skill, setiap hari Ramadan ditandai "Ramadan hari ke-N (perkiraan, menunggu sidang isbat)", Idulfitri ±10 Maret 2027 dan H+1 diisi ucapan tanpa jualan, dan jumlah video persis sesuai kemampuan Anda — plus file CSV siap buka di Excel.
