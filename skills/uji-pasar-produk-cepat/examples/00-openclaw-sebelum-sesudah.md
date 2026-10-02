# Uji OpenClaw: sebelum/sesudah - uji-pasar-produk-cepat

- Tanggal: 2026-10-02
- Cara uji: OpenClaw 2026.9.6 lokal, model router Komunitech claude-sonnet-5 (sama dengan bot member). SEBELUM = skill dimatikan (home tanpa skill), SESUDAH = hanya skill ini aktif. Home bersih dibuat ulang untuk tiap skenario; pesan identik. Tidak ada pertanyaan balik dari agent di kedua sisi, jadi tidak ada lanjutan.
- Skill terpakai di SESUDAH: ya (agent membaca SKILL.md dan menjalankan perintah / script).
- Catatan keamanan: agent tidak memasang paket, tidak mengubah config, tidak menawarkan kirim otomatis ke pihak lain, tidak mencari ke seluruh disk.

## Skenario 1
**Pesan (identik di kedua sisi):**
> Kak aku lagi tes harga dimsum frozen. Yg Rp35.000 aku tawarin ke 60 orang, yg beli 9. Yg Rp45.000 aku tawarin ke 60 orang juga, yg beli 15. Jadi mending pake harga yg mana? Langsung produksi 300 pack aja boleh ga?

**Balasan SEBELUM (tanpa skill) - utuh:**

Datanya jelas: harga Rp45.000 menang di dua sisi.

**Conversion rate:**
- Rp35.000 → 9/60 = 15%
- Rp45.000 → 15/60 = 25%

**Revenue per 60 tawaran:**
- Rp35.000 → 9 × 35.000 = Rp315.000
- Rp45.000 → 15 × 45.000 = Rp675.000

Harga lebih tinggi malah lebih banyak yang beli *dan* omzetnya lebih dari 2x lipat. Kemungkinan Rp35.000 dulu dianggap "kok murah banget, kualitasnya gimana" — harga Rp45.000 justru lebih dipercaya atau memang targetnya lebih pas. Jadi pilih **Rp45.000**.

Soal langsung produksi 300 pack — jangan dulu, dengan catatan:

1. **Sampel 60 orang itu kecil.** Secara statistik, selisih 15% vs 25% ini belum cukup kuat untuk dibilang "pasti beda" (masih ada kemungkinan itu kebetulan, meski kecil). Enak di data, tapi belum 100% aman buat taruh modal besar.
2. **Dimsum frozen punya risiko stok** — kalau nggak laku sesuai perkiraan, duit kejebak di freezer dan ada masa simpan yang jalan terus.
3. Aku belum tau **margin/cost produksi per pack** — tanpa itu, "harga mana paling untung" belum lengkap. Revenue tinggi belum tentu profit tinggi kalau cost produksinya juga naik.

Saranku: validasi dulu dengan skala lebih besar dulu di Rp45.000 (misal tawarin ke 150-200 orang lagi) atau langsung produksi batch kecil dulu (50-100 pack) buat lihat konversi real + respons after-sales (rasa, komplain, repeat order). Baru scale ke 300 kalau datanya makin solid.

Mau aku bantu hitung breakeven/margin kalau kakak kasih tau cost produksi per pack?

**Balasan SESUDAH (skill aktif) - utuh:**

Oke, sudah aku hitung pakai metode uji pasar (bukan kira-kira persen mentah):

**Hasil dua varian (60 orang/varian):**
• Rp35.000: 9/60 = 15,0% beli (rentang wajar sebenarnya: 8,1%–26,1%)
• Rp45.000: 15/60 = 25,0% beli (rentang wajar sebenarnya: 15,8%–37,2%)
• Selisih +10 poin persen, tapi secara statistik ini BELUM meyakinkan (p=0,17 — idealnya di bawah 0,05). Supaya selisih segini bisa dibuktikan beneran, butuh sekitar 250 orang per varian (total 500), bukan 60.

**Jadi mending harga mana?**
Rp45.000. Bukan cuma karena persennya lebih tinggi, tapi karena batas bawah rentang wajarnya (15,8%) sudah di atas ambang target wajar 15%, sedangkan Rp35.000 batas bawahnya (8,1%) di bawah 15%. Rp45.000 lebih harga lebih mahal, konversi tidak lebih rendah, ya pilih itu — gak ada downside.

**Tentang langsung produksi 300 pack: JANGAN dulu, ini terlalu besar lompatannya.**
Kenapa: konversi 25% itu angka tengah dari sampel kecil (60 orang). Kalau mau jual 300 pack:
• Skenario optimis (pakai 25%): butuh ±1.200 orang ditawari
• Skenario hati-hati (pakai batas bawah 15,8%): butuh ±1.900 orang ditawari

Kalau kontak/jangkauanmu belum sebanyak itu, 300 pack berisiko numpuk/rusak (apalagi frozen, ada batas tanggal). Rekomendasiku:

1. Produksi batch kecil dulu (mis. 30–50 pack) dengan harga Rp45.000, tawarkan ke kontak baru (bukan yang sudah ditawari) untuk konfirmasi ulang
2. Cek margin: HPP per pack belum kamu sebut — pastikan Rp45.000 masih untung layak setelah bahan, kemasan, ongkir. Kalau belum dihitung, bisa pakai skill hitung-hpp
3. Setelah batch kecil laku sesuai target, baru naikkan ke 300 dan seterusnya bertahap

Baris log biar gak lupa:
2026-10-02 | Asumsi: Harga | Eksperimen: Pre-order WA 2 varian | Kanal: WA | Kriteria: T=15% | Hasil A=15% (8,1-26,1%), B=25% (15,8-37,2%), p=0,17 | Keputusan: Pilih B (Rp45rb), LANJUT BERTAHAP, bukan full 300 | Pelajaran: selisih 10 poin belum signifikan, perlu sampel lebih besar untuk pastikan

Langkah berikutnya: produksi batch kecil Rp45.000, tes ke 50-100 kontak baru, sambil cek HPP/margin.

**Verifikasi independen:**
- Konversi 15% dan 25% benar. Wilson 95% dihitung ulang: 9/60 = 8,1%-26,1%; 15/60 = 15,8%-37,2% (SESUDAH cocok persis).
- Uji z dua proporsi: z = 1,37, p = 0,171 (SESUDAH menulis 0,17, benar). Fisher tepat: p = 0,254 (tidak dipakai di sini; n = 60 per varian, jadi z sesuai aturan skill).
- Sampel 250 per varian untuk 15% vs 25%: cocok dengan tabel skill. 300 pack / 25% = 1.200 orang; 300 / 15,8% = 1.899 (cocok).
- SEBELUM: omzet per 60 tawaran 315.000 vs 675.000 benar, tetapi tanpa rentang/p-value; sarannya (150-200 orang lagi atau batch 50-100) masuk akal.
- SESUDAH: kalimat "tidak ada downside" berlebihan (margin belum dicek, padahal ia menyebutnya di langkah 2).

**Skor:** SEBELUM 7/10, SESUDAH 9/10.
SEBELUM sudah baik: hitung omzet, sadar sampel kecil, menolak 300 pack. SESUDAH menambah rentang wajar, p-value, jumlah sampel yang dibutuhkan, hitungan jangkauan untuk 300 pack, dan baris log eksperimen; lebih terukur dan siap dicatat. Selisihnya nyata tapi tidak dramatis.

---
## Skenario 2
**Pesan (identik di kedua sisi):**
> Kak, aku tawarin brownies kukus varian matcha ke 12 orang di grup WA, 5 bilang mau pre-order (blm ada yg transfer sih, baru bilang 'mau'). Berarti konversi 42% dong ya, bagus banget kan? Aku mau langsung beli bahan buat 400 box, modal 15 juta. Bener kan?

**Balasan SEBELUM (tanpa skill) - utuh:**

Whoa, tahan dulu Kak, sebelum duit 15 juta jalan. Ada beberapa hal yang menurutku perlu diluruskan:

**Soal "konversi 42%" itu nggak akurat.**
- 5 dari 12 "bilang mau" itu *minat verbal*, bukan konversi. Konversi beneran itu dihitung dari yang udah **transfer DP/bayar**, bukan yang cuma ngomong "mau".
- Di jualan online/pre-order, gap antara "mau" lisan dan "bayar beneran" itu biasanya gede banget — bisa cuma 30-60% dari yang ngomong mau yang akhirnya bayar. Jadi dari 5 orang itu, realistisnya mungkin cuma 2-4 yang beneran closing.
- Base 12 orang juga kekecilan buat narik kesimpulan apapun. Itu baru 1 grup WA, bukan representasi pasar.

**Soal lompat ke 400 box / 15 juta — ini yang paling riskan.**
- Kamu baru punya **5 minat, 0 transfer**, tapi mau produksi 400 box. Itu artinya kamu butuh ~395 box lagi terjual ke orang yang belum pernah kontak sama kamu soal ini.
- Kalau ternyata cuma closing 3-4 box, sisa 396 box brownies matcha itu modal nyangkut di bahan basah (butter, telur, matcha) yang gampang basi kalau nggak segera terjual.
- 15 juta modal di awal buat produk yang belum tervalidasi itu risiko besar buat skala UMKM.

**Yang lebih aman dilakukan sekarang:**
1. **Minta DP dulu** ke 5 orang yang bilang "mau" — baru yang transfer itu hitung sebagai order real.
2. **Produksi kecil dulu** sesuai jumlah yang udah DP + buffer tipis (misal order real 4, produksi 6-8 box).
3. Kalau laku lancar & ada yang nanya ulang/repeat order, baru naikin skala pelan-pelan (misal 2x lipat tiap batch), bukan langsung loncat ke 400.
4. Coba expand ke grup WA lain atau story/status buat lihat minat di luar 12 orang itu, biar datanya lebih valid.

Mau aku bantu bikin template chat buat nagih DP ke 5 orang itu, atau bantu hitung breakdown modal buat skala kecil dulu (misal 10-20 box)?

**Balasan SESUDAH (skill aktif) - utuh:**

Belum bener, Kak — dan untungnya ketahuan sebelum uang 15 juta keluar. Dua masalah:

**1. "Mau" ≠ pre-order**
Yang kuat itu transfer/DP, bukan kata "mau". Orang gampang bilang mau di chat grup buat basa-basi atau sungkan nolak temen. Sampai sekarang belum ada 1 pun yang bayar — jadi datanya masih "minat kasar", bukan bukti beli.

**2. Sampelnya kecil banget (12 orang)**
Aku hitungin pakai rentang wajar (Wilson), biar nggak keputusan dari angka kebetulan:

- Konversi: 5/12 = **41,7%**
- Tapi angka sebenarnya kemungkinan besar ada di antara **19% dan 68%** — rentangnya lebar banget
- 12 orang itu < 30, jadi ini baru **sinyal arah, bukan dasar modal besar**
- Keputusan: **LANJUT BERTAHAP** (bukan "lanjut gas penuh")

Ditambah, kalau 12 orang itu temen/kenalan deket di grup WA, mereka cenderung "mau" karena sungkan, bukan karena beneran mau beli. Itu bikin angkanya lebih optimis dari kenyataan pasar.

**Jangan beli bahan 400 box / modal 15 juta sekarang.** Kalau minat aslinya ternyata di ujung bawah rentang (19%), dari 12 orang itu cuma ~2-3 orang yang beneran beli — bayangin kalau itu terjadi di skala 400 box.

**Langkah yang lebih aman:**
1. Ke 5 yang bilang "mau" — minta DP sekarang juga, kasih tenggat (mis. 2 hari), baru itu hitung sebagai pre-order sah.
2. Tawarin ke minimal 30 orang total (campur yang kenal deket & yang nggak terlalu deket, biar nggak bias), pakai pesan pre-order yang jelas: harga, tanggal kirim, dan DP wajib.
3. Setelah terkumpul ≥30 data, aku hitungin ulang konversi + rentangnya — baru dari situ tentuin jumlah produksi riil, bukan langsung 400 box.
4. Kalau belum tau margin/HPP brownies matcha ini, aku bisa bantu hitung dulu sebelum masuk ke jumlah modal.

Mau aku bikinin draf pesan pre-order yang lebih "memaksa aksi" (minta DP, bukan cuma minat) buat ditawarin ke 30 orang itu?

**Verifikasi independen:**
- 5/12 = 41,7%. Wilson 95%: 19,3%-68,1% (SESUDAH menulis 19%-68%, benar).
- SEBELUM menyebut "biasanya cuma 30-60% dari yang bilang mau yang bayar": angka tanpa sumber, dikarang. Tidak ada rentang statistik.
- Kedua sisi menolak 400 box/Rp15 juta dan meminta DP lebih dulu (benar). SESUDAH menyebut keputusan "LANJUT BERTAHAP" meski sampel < 30 dan 0 transfer; lebih tepat "UBAH / uji ulang"; ringan.

**Skor:** SEBELUM 7/10, SESUDAH 9/10.
SEBELUM: nasihat tepat dan ramah, tetapi memuat statistik karangan. SESUDAH: menjelaskan "mau" bukan bukti, rentang wajar 19%-68% dihitung, ambang 30 orang, langkah DP bertenggat, tawar ke 30 orang. Sedikit lebih kuat dan lebih jujur soal data.

---
## Ringkasan
- Skor rata-rata: SEBELUM 7,0 -> SESUDAH 9,0.
- **VERDIK: LULUS** (sesudah >= 8, tidak ada kesalahan angka).
- Jujur: model tanpa skill sudah sehat secara logika (menolak lompat ke produksi besar). Pembeda skill ada pada angka yang dihitung (Wilson, uji z, kebutuhan sampel) dan format log eksperimen.

## Cacat untuk pembuat
1. Skenario 2: keputusan "LANJUT BERTAHAP" pada 12 orang / 0 transfer terkesan kontradiktif dengan peringatan sampel < 30; saran: untuk sampel < 30 dan tanpa aksi bayar, keluaran script/skill harus "UJI ULANG" dan bukan LANJUT.
2. Skenario 1: kalimat "tidak ada downside" mendahului pengecekan margin; saran: larang kata itu sebelum HPP diketahui.

## Cuplikan jualan
- "Dari 12 orang yang bilang 'mau', angka sebenarnya bisa 19% sampai 68% - bukan 42% pasti. Skill ini menghitung rentangnya sebelum Anda keluarkan Rp15 juta."
- "Harga Rp45.000 vs Rp35.000: selisih 15% vs 25% ternyata belum meyakinkan (p = 0,17); butuh sekitar 250 orang per varian untuk memastikan."
