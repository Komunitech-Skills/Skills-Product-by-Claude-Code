# Skenario 1: katering rumahan nasi box (normal, juga konteks Telegram)

**Input:** "Saya punya katering rumahan nasi box, menunya ayam goreng & ayam bakar, telur balado, sambal, sama sayur santan. Staf 3 orang, cuma ada kulkas 1 pintu, belum punya termometer. bikinin checklist keamanan pangan harian & aturan buat staf, sekalian log suhu"

## Catatan
Output di bawah adalah versi konteks Telegram (versi lokal setara, nilai 8,5; lihat 00-openclaw-sebelum-sesudah.md).

Catatan penguji: batas suhu konsisten dengan references (kulkas ≤ 5 °C, ayam ≥ 74 °C, telur ≥ 63 °C, 2 jam/1 jam di atas 32 °C). Tegas tidak mengarang angka log tanpa termometer. Perizinan hanya petunjuk + PERLU REVIEW, tanpa pasal. Model dasar menulis isi ke file di server, sehingga di Telegram pengguna hanya menerima nama file. Nilai: sebelum 4,5 (Telegram) / 5,5 (lokal), sesudah 8,5.

## Output SESUDAH (skill aktif)

# Paket Keamanan Pangan - Katering Rumahan Nasi Box

**Asumsi** (karena belum disebutkan, saya isi dan boleh dikoreksi):
- 3 staf dapur, 1 penanggung jawab merangkap salah satu staf
- 1 kulkas pintu tunggal, tidak ada freezer terpisah
- Belum ada termometer pangan
- Menu: ayam goreng, ayam bakar, telur balado, sambal, sayur santan, disajikan dalam nasi box
- Jam antar box: `[isian: jam antar]` — nanti saya sebut batas waktu umumnya
- Penafian: ini kebiasaan kerja aman, bukan pengganti pelatihan penjamah makanan resmi atau pemeriksaan Dinkes.

---

## 1. Daftar Periksa Harian

**Saat datang**
☐ Cuci tangan sabun 20 detik, rambut tertutup, kuku pendek
☐ Staf sakit (muntah/diare/demam/kuning)? Tidak pegang makanan, lapor dulu
☐ Cek tanda hama & sampah semalam sudah dibuang
☐ Baca kondisi kulkas (dingin terasa normal / pintu rapat), catat di log suhu

**Sebelum mulai masak**
☐ Meja & alat dibersihkan lalu disanitasi
☐ Talenan dipisah: 1 khusus ayam mentah, 1 khusus telur/sayur/matang
☐ Bahan lama di depan (FIFO); cek tanggal ayam, telur, santan — buang yang sudah lewat
☐ Santan baru tidak dicampur sisa santan kemarin

**Saat masak & kemas nasi box**
☐ Ayam goreng & ayam bakar matang sampai bagian paling tebal (bukan kira-kira, nanti diukur — lihat bagian log suhu)
☐ Telur balado dimasak matang penuh, tidak setengah matang
☐ Sayur santan dimasak sampai mendidih penuh, tidak dipanaskan setengah-setengah
☐ Nasi, lauk, sambal yang sudah matang jangan dibiarkan di suhu ruang lebih dari **2 jam** sebelum dikemas/diantar
☐ Tulis jam selesai masak di dekat wadah, supaya tahu batas 2 jam
☐ Tangan dicuci lagi setiap pindah dari pegang ayam mentah ke pegang telur/sambal/nasi matang

**Sebelum antar / saat tutup**
☐ Box ditutup rapat, tidak menumpuk kena udara luar terlalu lama
☐ Sisa lauk yang tidak jadi dikirim: dinginkan cepat (wadah dangkal, tidak ditutup rapat saat masih panas) lalu masuk kulkas, atau dibuang bila sudah lewat batas waktu
☐ Semua bahan sisa diberi label nama + tanggal
☐ Alat, talenan, meja, lantai dibersihkan; sampah dibuang
☐ Baca & catat kondisi kulkas terakhir; paraf: ____

---

## 2. Mingguan / Bulanan

☐ Cek celah/lubang masuk hama, bersihkan sampah tersembunyi (belakang kulkas, bawah meja)
☐ Bersihkan dalam kulkas total — rak, karet pintu, tumpahan — buang yang kadaluarsa
☐ Cek saluran air dapur tidak tersumbat/bau
☐ Stok sabun cuci tangan & sanitizer cukup untuk minggu depan
☐ Review tanggal semua bahan kering (bumbu, minyak) — FIFO
☐ Kalau sudah beli termometer: uji kalibrasi pakai air es (harus baca sekitar 0 °C)

---

## 3. Log Suhu

**Catatan penting — belum ada termometer:**
Log suhu **tidak bisa diisi dengan angka yang benar** tanpa alat ukur. Mengisi angka kira-kira sama saja membohongi diri sendiri — kalau ada kejadian (ayam kurang matang, pelanggan sakit), log itu tidak ada gunanya untuk membuktikan apa pun.

**Saran:** beli termometer pangan tusuk (probe thermometer) — tersedia online/toko alat masak, kisaran murah, cukup satu untuk cek ayam/telur dan kulkas. Ini investasi kecil yang paling penting untuk usaha ayam & telur.

**Sementara belum ada termometer, pakai checklist visual + waktu (bukan pengganti, hanya jaga-jaga):**
☐ Ayam goreng/bakar: potong bagian paling tebal, pastikan tidak ada bagian merah muda/berdarah, uap/air yang keluar bening
☐ Telur balado: kuning telur sudah padat, tidak basah/meleleh
☐ Sayur santan: sudah mendidih penuh, bukan sekadar hangat
☐ Kulkas: isi tidak terlalu padat (udara dingin perlu sirkulasi), pintu rapat, tidak ada bau tidak wajar atau bahan yang terasa hangat di bagian dalam
☐ Catat **jam mulai** makanan matang berada di suhu ruang — batas aman 2 jam (1 jam bila dapur sangat panas, di atas 32°C)

**Begitu termometer sudah ada, batas yang harus dipakai:**
- Kulkas: ≤ 5°C
- Ayam/unggas matang (bagian paling tebal): ≥ 74°C
- Telur matang: ≥ 63°C (lebih baik matang penuh untuk katering)
- Sayur santan setelah mendidih: tidak perlu diukur rutin, cukup mendidih penuh lalu segera disajikan/didinginkan
- **Jika melebihi batas:** bahan berisiko tinggi (ayam, telur, santan) yang sudah di suhu ruang/suhu tidak aman total lebih dari 2 jam → **buang**, jangan dipakai lagi. Jangan dicium dulu untuk menilai aman atau tidak.

Format catatan harian (isi manual di kertas/HP sampai ada termometer):
`Tanggal | Jam mulai matang | Menu | Jam dikemas/antar | OK (ya/tidak) | Paraf`

---

## 4. Kartu Aturan Staf (10 Poin — tempel di dapur)

1. Cuci tangan sabun 20 detik: sebelum kerja, habis toilet, habis pegang ayam mentah, sampah, HP, uang.
2. Sakit perut, muntah, diare, demam, mata kuning: jangan pegang makanan, lapor dulu, pulang dulu.
3. Talenan ayam mentah **terpisah** dari talenan telur/sayur/sambal. Jangan ditukar meski sudah dicuci sekilas.
4. Ayam & telur matang sampai dalam — potong, lihat warnanya, jangan kira-kira karena terburu-buru.
5. Sayur santan dimasak sampai mendidih penuh, tidak dihangatkan setengah-setengah.
6. Nasi box yang sudah jadi: jangan dibiarkan di meja lebih dari 2 jam sebelum diantar. Catat jam selesai masak.
7. Sisa lauk dinginkan cepat (wadah dangkal, jangan ditutup rapat saat masih panas), baru masuk kulkas.
8. Semua bahan diberi label nama + tanggal. Yang lama dipakai dulu. Lewat tanggal: **buang**, jangan diganti label/tanggal.
9. Bersihkan dulu, baru sanitasi. Kain lap kotor diganti, jangan dipakai lap ayam lalu lap meja makan.
10. Ragu apakah ayam/telur sudah matang atau bahan masih aman? Buang, tanya penanggung jawab. Jangan ambil risiko demi hemat.

---

## 5. Peta Risiko Menu

**Ayam goreng & ayam bakar**
- Risiko: Salmonella/Campylobacter, kontaminasi silang ke bahan lain
- Cara aman: talenan terpisah, matang sampai dalam (tidak merah muda), cuci tangan setelah pegang mentah

**Telur balado**
- Risiko: Salmonella bila kurang matang
- Cara aman: masak sampai kuning telur padat, simpan telur mentah di kulkas, cuci tangan setelah pegang cangkang mentah

**Sambal**
- Risiko relatif lebih kecil (cabai dimasak, umumnya asam/panas membantu), tapi tetap rawan kalau cabai mentah/bawang dipotong di talenan yang baru dipakai untuk ayam mentah
- Cara aman: talenan bumbu terpisah dari talenan ayam mentah, cuci tangan sebelum pegang bumbu

**Sayur santan**
- Risiko: cepat basi, bisa jadi media bakteri kalau dibiarkan hangat lama
- Cara aman: masak matang penuh, jangan dicampur santan baru+lama, habiskan di hari yang sama, jangan dibiarkan di suhu ruang lama

**Nasi (dalam nasi box)**
- Risiko: Bacillus cereus (spora tahan panas masak, bisa muncul lagi kalau nasi dibiarkan hangat lama)
- Cara aman: setelah matang, jangan dibiarkan di suhu ruang berjam-jam sebelum dikemas; kalau tidak langsung diantar, dinginkan cepat atau tahan panas (≥60°C)

**Kontaminasi silang spesifik dapur Anda:** talenan ayam mentah vs talenan telur/sayur/sambal — ini titik paling rawan dengan menu Anda. Pisahkan fisik (warna beda kalau bisa), dan jangan letakkan ayam mentah di rak kulkas di atas telur/sayur matang.

**Alergen:** telur (ada di telur balado, bisa juga di gorengan ayam kalau ada campuran telur di adonan tepung). Kalau ada pelanggan yang tanya alergi, jawab: "diproses di dapur yang juga mengolah telur" — jangan bilang "aman" tanpa itu.

---

## 6. Perizinan (PERLU REVIEW — cek ke Dinkes/OSS setempat, ini ringkasan umum per 2026-10-06, bukan nasihat hukum mengikat)

- **NIB (OSS)** — dasar legal semua usaha, daftar online lewat OSS.
- **SLHS (Sertifikat Laik Higiene Sanitasi) + pelatihan penjamah makanan** — relevan untuk katering/jasa boga, lewat Dinkes kabupaten/kota.
- **PIRT/SPP-IRT** — relevan **kalau** suatu saat Anda jual produk kemasan terpisah (misalnya sambal botolan dijual lepas, bukan hanya di nasi box harian) — lewat Dinkes.
- **Sertifikasi halal** — relevan untuk makanan yang diperdagangkan; usaha mikro-kecil bisa lewat jalur Self Declare di BPJPH.

Langkah awal paling praktis: hubungi Dinkes kabupaten/kota tempat usaha untuk tanya syarat SLHS jasa boga, sambil urus NIB lewat OSS.

---

**Pertanyaan untuk saya sesuaikan lebih lanjut:**
1. Berapa porsi nasi box per hari, dan berapa lama jarak dari jam ayam/telur matang sampai box diantar ke pelanggan?
2. Kulkas 1 pintu itu ada kompartemen freezer kecil, atau murni untuk dingin (chiller) saja?
3. Nasi box ini dijual harian langsung saja, atau ada rencana jual produk terpisah (misalnya sambal kemasan) yang butuh PIRT?

Pengingat: angka suhu di atas acuan ilmiah umum — cocokkan lagi dengan Dinkes setempat, dan checklist ini bukan pengganti pelatihan penjamah makanan resmi.
