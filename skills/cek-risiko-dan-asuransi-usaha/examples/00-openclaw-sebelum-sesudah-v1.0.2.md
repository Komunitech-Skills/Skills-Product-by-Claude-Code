# Uji OpenClaw sebelum/sesudah: cek-risiko-dan-asuransi-usaha v1.0.2

- **Tanggal:** 2026-10-11
- **Penguji:** Akun C (independen, bukan pembuat)
- **Cara uji:** OpenClaw 2026.9.8, model router `claude-sonnet-5`, `run-uji.sh` / `run-uji-tg.sh` (tanpa unshare). Revisi R1–R8 (BPJS otomatis, JKP, OJK 157/LAPS, parser biaya).
- **Tes script:** 23/23 OK.

## Skenario 01 — Kafe ruko dekat kali (+ TG)

**Pesan:**
> kak sy punya kafe kecil di ruko 2 lt deket kali di bekasi, karyawan 3 (blm ikut bpjs tk, cuma bpjs kes yg mandiri masing2). sewa 4,5jt/bln, gaji @2,8jt, listrik+gas 1,7jt, cicilan mesin espresso 1,2jt. kas cadangan cuma 8jt. thn 2020 pernah kebanjiran semata kaki. perlu asuransi apa ya? dana darurat brp?

### SEBELUM — skor 7/10

```
Oke, saya hitung dulu biaya tetap bulanan kafe kakak:

- Sewa: 4,5jt
- Gaji 3 karyawan: 3 × 2,8jt = 8,4jt
- Listrik + gas: 1,7jt
- Cicilan mesin espresso: 1,2jt
**Total fixed cost ≈ 15,8jt/bulan**

Kas cadangan sekarang 8jt = **kurang dari sebulan** biaya operasional kalau kafe harus tutup sementara (misal kebanjiran lagi). Ini titik paling rawan sebenarnya, bukan cuma soal asuransi.

**Dana darurat usaha** (standar: 3–6 bulan fixed cost, dan karena lokasi rawan banjir + pernah kena 2020, saya sarankan ambil yang 6 bulan):
- 3 bulan = 47,4jt
- 6 bulan = 94,8jt

Gap dari kas sekarang (8jt) lumayan jauh, jadi targetnya nabung bertahap — misal sisihkan 5–10% omzet/bulan masuk rekening terpisah khusus dana darurat, jangan dicampur kas operasional.

**Asuransi, urutan prioritas:**

1. **BPJS Ketenagakerjaan untuk 3 karyawan** — ini yang paling urgent & murah. Karyawan kerja di kafe (mesin espresso panas, pecahan kaca, kompor) dan sekarang belum ada perlindungan kecelakaan kerja (BPJS Kes mandiri ga cover itu). Minimal ambil JKK + JKM, totalnya kira-kira cuma ~0,8-0,9% dari gaji per karyawan (±25rb/orang/bulan, ±75rb/bulan total untuk 3 orang — estimasi, rate pastinya tergantung kategori risiko usaha, bisa dicek langsung ke kantor BPJS TK terdekat). Ini juga kewajiban hukum, bukan cuma pilihan.

2. **Asuransi properti/isi usaha dengan perluasan banjir** — ini wajib dipikirkan serius karena riwayat 2020 kebanjiran semata kaki dan lokasi deket kali. Cover stok bahan baku, peralatan, furnitur, dan idealnya mesin espresso juga (cek dulu apakah cicilan mesin itu sudah otomatis include asuransi dari pihak leasing/supplier — banyak yang mewajibkan). Tanpa perluasan banjir eksplisit, polis standar properti seringnya exclude banjir.

3. **Asuransi tanggung gugat pihak ketiga (public liability)** — buat usaha F&B, jaga-jaga kalau ada pelanggan cedera di tempat atau keracunan makanan. Preminya biasanya ringan dibanding risikonya.

4. **Business interruption (opsional, kalau budget sudah longgar)** — nutup gap pendapatan kalau kafe terpaksa tutup karena banjir/kebakaran. Ini pelengkap, bukan prioritas awal.

Kalau budget terbatas, urutan paling masuk akal: **BPJS TK dulu (murah & wajib) → asuransi properti+banjir → baru mikirin dana darurat ditambah pelan-pelan tiap bulan.** Mau saya bantu cariin kontak agen asuransi UMKM/BPJS TK kantor cabang terdekat di Bekasi?
```

### SESUDAH — skor 8.5/10

```
Asumsi: kafe kecil 2 karyawan... eh, 3 karyawan, ruko 2 lantai dekat kali di Bekasi, biaya tetap sewa+gaji+listrik/gas+cicilan mesin ≈ Rp15,8 juta/bln, kas cadangan Rp8 juta, riwayat banjir semata kaki (2020).

**Tabel risiko**

| No | Risiko | Kemungkinan | Dampak | Skor/Tingkat | Langkah murah | Perlu asuransi? |
|---|---|---|---|---|---|---|
| 1 | Kebakaran dapur/korsleting listrik | 3 | 4 | 12 TINGGI | APAR + cek isi ulang, ganti kabel tua, cek selang gas, jangan tinggal kompor nyala | **Ya, pertimbangkan** |
| 2 | Banjir (ruko dekat kali, sudah pernah kebanjiran semata kaki) | 4 | 3 | 12 TINGGI | Stok & dokumen di rak tinggi/lantai 2, colokan listrik dinaikkan, cek riwayat banjir wilayah | Tidak wajib — mitigasi dulu (dampak masih setara 1 bln biaya tetap karena ada lantai 2 untuk evakuasi barang; kalau air pernah/bisa lebih tinggi dari semata kaki, ini naik ke prioritas asuransi) |
| 3 | Kerusakan mesin espresso (masih dicicil) | 3 | 3 | 9 SEDANG | Servis berkala, stabilizer, nomor teknisi, alat cadangan manual | Tidak wajib, siapkan dana cadangan; tanya agen soal *machinery breakdown* bila mau dialihkan |
| 4 | Bergantung satu orang kunci (owner/barista racik resep) | 2 | 3 | 6 SEDANG | Tulis SOP/resep, latih 1 cadangan | Tidak ada asuransi umum — mitigasi lewat SOP |
| 5 | Tanggung jawab ke pelanggan (keracunan, terpeleset lantai basah) | 2 | 3 | 6 SEDANG | Standar kebersihan dapur, lantai antislip dekat pintu/kamar mandi | Tidak wajib, siapkan dana cadangan |
| 6 | **Karyawan cedera/sakit/kecelakaan kerja (3 org, belum BPJS TK)** | 3 | 2 | 6 SEDANG | K3 dasar (alas kaki anti-slip, APAR dekat kompor) | **BPJS: kewajiban pemberi kerja, cek aturan terbaru (JKK untuk kecelakaan kerja; BPJS Kesehatan untuk sakit)** |
| 7 | Kehilangan/pencurian stok & kas | 3 | 2 | 6 SEDANG | CCTV, setor kas harian, pisahkan akses uang | Tidak wajib, siapkan dana cadangan |
| 8 | Listrik padam/gangguan alat saat banjir | 3 | 2 | 6 SEDANG | Genset/UPS kecil untuk alat kunci | Tidak ada asuransi umum — mitigasi teknis |

**Dana darurat** (biaya tetap Rp15.800.000/bln)

| Target | Kas sekarang | Kekurangan | Cicilan nabung 6 bln |
|---|---|---|---|
| 3 bulan → Rp47.400.000 | Rp8.000.000 (cuma 0,5 bln) | Rp39.400.000 | ±Rp6.566.667/bln |
| 6 bulan → Rp94.800.000 | Rp8.000.000 | Rp86.800.000 | ±Rp14.466.667/bln |

Kas cadangan kakak sekarang jauh di bawah aman (setengah bulan biaya tetap). Karena lokasi punya riwayat banjir, saya sarankan kejar target **6 bulan**, bukan 3 — tapi mulai dulu dari target 3 bulan biar nggak putus asa, baru lanjut ke 6.

**Jenis perlindungan umum yang layak dipertimbangkan** (nama generik, bukan merek — cek isi polis sendiri)
- **Asuransi kebakaran/properti**: lindungi bangunan, isi, stok dari kebakaran; perluasan banjir biasanya harus dicek/ditambah terpisah per polis — tanyakan eksplisit karena riwayat banjir kakak.
- **Tanggung gugat umum**: kalau pelanggan cedera (terpeleset) atau keracunan makanan dan menuntut.
- **Kerusakan mesin (machinery breakdown)**: khusus mesin espresso yang masih dicicil — kalau rusak mendadak karena sebab internal (bukan aus wajar), bisa dialihkan; tapi mesin tua/aus biasa sering dikecualikan.
- **BPJS Ketenagakerjaan untuk 3 karyawan** — ini bukan opsional, ini kewajiban pemberi kerja yang belum dijalankan. Program dasarnya JKK (kecelakaan kerja), JKM (kematian), JHT (hari tua); JP dan JKP tergantung skala usaha. Cek kewajiban & besaran iuran terbaru langsung ke BPJS Ketenagakerjaan — jangan saya karang angkanya.

**Prioritas 3 langkah minggu ini**
1. **Daftarkan BPJS Ketenagakerjaan untuk 3 karyawan** (sekarang mereka cuma punya BPJS Kes mandiri — kalau ada yang cedera kerja, kakak yang full nanggung sendiri). Ini paling mendesak, bukan "kalau sempat".
2. Cek ulang instalasi listrik + beli/isi ulang APAR, karena dapur + ruko lama = risiko kebakaran skor TINGGI.
3. Mulai nabung dana darurat bertahap — target realistis dulu Rp47,4jt (3 bulan), sisihkan dari omzet sebelum biaya lain, baru nanti naikkan ke 6 bulan karena lokasi rawan banjir.

**Disclaimer:** Ini bukan nasihat asuransi/keuangan/hukum — cuma bantu memetakan risiko. Keputusan beli polis lewat perusahaan asuransi berizin OJK dan agen terdaftar (cek nomor registrasinya), baca sendiri isi polisnya. Dasar acuan ditulis per 2026-10-09, aturan BPJS bisa berubah, cek sumber resmi.

**Pertanyaan balik:**
1. Dampak banjir di tempat kakak — airnya cuma masuk lantai dasar sebentar atau sampai bikin tutup berhari-hari? (ini nentuin apa banjir masuk prioritas asuransi atau cukup mitigasi)
2. Ruko-nya sewa atau milik sendiri? (asuransi kebakaran/properti beda relevansinya kalau cuma nyewa)
3. Mau saya kasih daftar pertanyaan siap pakai buat ditanyain ke agen asuransi (ada templatenya)?
```

## Skenario 02 — Bengkel motor Makassar

**Pesan:**
> bengkel motor sy di depan rumah, makassar. mekanik 2, yg senior udh 8 thn sm sy, kl dia ga masuk bengkel ampir lumpuh. motor pelanggan kdg nginep. biaya tetap: gaji 7jt total, listrik 900rb, cicilan kompresor 650rb, lain2 500rb. tabungan usaha 20jt. perlu asuransi ga sih?

### SEBELUM — skor 6.5/10

```
Perlu, dan dari cerita situ keliatan ada 3 risiko konkret yang belum ke-cover — bukan sekadar "asuransi itu bagus":

**1. Motor pelanggan yang nginap bengkel → ini paling urgent**
Kalau pas nginap itu motor kebakar, kecurian, atau rusak (kompresor jatuh nimpa, korsleting, dll), lo yang nanggung ganti rugi ke pelanggan — bukan asuransi motor pelanggan sendiri (polis mereka biasanya gak cover kerusakan saat di bengkel orang lain). Satu motor hilang/rusak bisa langsung gerus habis tabungan 20jt lo. Yang dicari: **asuransi tanggung jawab pihak ketiga / garage liability** (kadang dibundel sama asuransi kebakaran properti usaha). Ini prioritas #1 karena exposure-nya langsung ke kas usaha lo.

**2. Mekanik senior = single point of failure**
Asuransi gak bisa gantiin skill dia 8 tahun, tapi bisa mitigasi *biaya* kalau dia kecelakaan kerja atau sakit lama:
- **BPJS Ketenagakerjaan (JKK + JKM)** untuk kedua mekanik — ini murah banget (per orang biasanya di bawah 20rb/bulan kalau didaftarkan sebagai pekerja), dan legally lo memang wajib daftarin kalau punya karyawan tetap. Kalau dia cedera kerja (kena alat, dll), biaya rawat + santunan ditanggung BPJS, bukan kantong lo.
- Kalau mau lebih jauh: asuransi kecelakaan diri tambahan khusus buat dia bisa jadi bentuk retensi juga (dia ngerasa dihargai, lo ngerasa lebih aman).
- Tapi risiko "dia resign/sakit lama" itu bukan insurable risk — itu perlu dimitigasi operasional: training mekanik junior biar makin mandiri, biar bengkel gak "ampir lumpuh" kalau dia absen.

**3. Alat/properti**
Kompresor masih nyicil 650rb/bulan — kalau itu rusak kebakar/kecurian sebelum lunas, lo tetep harus bayar cicilan + beli baru. Asuransi kebakaran/properti usaha yang nyakup isi bengkel (alat-alat) worth dicek, biasanya bisa dibundel sama poin #1.

**Soal cash lo:**
Tabungan 20jt vs biaya tetap 9,05jt/bulan (gaji 7jt + listrik 900rb + cicilan 650rb + lain2 500rb) = runway cuma ~2,2 bulan kalau usaha berhenti total. Ini artinya margin aman lo tipis — justru alasan kuat buat prioritasin asuransi liability dulu (poin 1), karena itu yang paling bisa bikin kas lo jebol dalam sekali kejadian, bukan BPJS yang murah.

**Urutan praktis:**
1. Cek agen asuransi umum lokal di Makassar untuk paket **asuransi kebakaran + tanggung jawab pihak ketiga** bengkel (sering satu paket "property all risk" usaha kecil)
2. Daftarin 2 mekanik ke **BPJS Ketenagakerjaan** kalau belum
3. SOP cadangan: mulai latih mekanik junior pegang kasus-kasus yang biasa dihandle si senior

Catatan: web search lagi gak available buat gue cek tarif premi real-time, jadi angka BPJS di atas estimasi umum — perlu diverifikasi langsung ke kantor BPJS Ketenagakerjaan atau cekindo.go.id pas mau daftar. Mau gue bantu susun daftar pertanyaan buat ditanyain ke agen asuransi pas lo survey?
```

### SESUDAH — skor 8.5/10

```
Asumsi: bengkel motor (servis + terima motor nginep/titipan), ruko/rumah di Makassar, 2 mekanik (1 senior kunci), belum dikonfirmasi riwayat banjir di lokasi.

| No | Risiko | Kemungkinan | Dampak | Skor/Tingkat | Langkah murah | Perlu asuransi? |
|---|---|---|---|---|---|---|
| 1 | Kebakaran (korsleting, bensin/oli, las) | 3 | 4 | 12 TINGGI | APAR + cek tanggal isi ulang, rapikan kabel/colokan, pisah area las dari bensin/oli, jalur keluar bebas | Ya, pertimbangkan |
| 2 | Motor pelanggan nginep rusak/hilang/kebakar | 3 | 4 | 12 TINGGI | Tanda terima + foto kondisi motor saat masuk, area parkir inap terkunci/CCTV, batas waktu pengambilan | Ya, pertimbangkan |
| 3 | Mekanik senior keluar/sakit — bengkel nyaris lumpuh | 3 | 4 | 12 TINGGI | Mulai latih mekanik ke-2 pegang kasus sulit, tulis SOP/kontak teknisi lepas cadangan, jangan simpan ilmu kunci cuma di kepala dia | Tidak ada asuransi umum; pakai mitigasi lain |
| 4 | Banjir | 2 | 3 | 6 SEDANG | Cek riwayat banjir di lokasi; kalau pernah, stok part & dokumen di rak tinggi | Tidak perlu (cek dulu riwayat lokasi) |
| 5 | Kesalahan servis → motor makin rusak, komplain | 2 | 3 | 6 SEDANG | Nota kerja tertulis + persetujuan pelanggan sebelum bongkar, foto sebelum/sesudah | Tidak perlu |
| 6 | Kompresor rusak mendadak (masih dicicil) | 2 | 3 | 6 SEDANG | Servis berkala, jaga tegangan listrik stabil, simpan kontak teknisi kompresor | Tidak perlu |
| 7 | Mekanik cedera kerja (alat, knalpot panas, motor roboh) | 3 | 2 | 6 SEDANG | Sarung tangan, sepatu kerja, ganjal motor saat servis, SOP angkat beban | **BPJS**: kewajiban pemberi kerja, cek aturan terbaru (JKK kecelakaan kerja; BPJS Kesehatan untuk sakit) |
| 8 | Pencurian spare part / uang kas | 3 | 2 | 6 SEDANG | CCTV, kunci gudang part, setor kas harian, pisah uang usaha-pribadi | Tidak perlu |

**Dana darurat** (biaya tetap: gaji 7jt + listrik 900rb + cicilan kompresor 650rb + lain² 500rb = **Rp9.050.000/bulan**):
- Target 3 bulan: **Rp27.150.000** | Kas sekarang Rp20jt (cukup 2,2 bulan) | **Kekurangan: Rp7.150.000**
- Kalau mau lebih aman (6 bulan, karena ketergantungan ke 1 mekanik senior itu risiko nyata): target **Rp54.300.000**, kekurangan Rp34,3jt.

Jenis perlindungan umum yang layak ditanyakan ke agen (nama generik, bukan rekomendasi merek):
- **Asuransi kebakaran/properti** — bangunan & isi bengkel; perluasan banjir dicek terpisah.
- **Barang titipan pelanggan** — ini yang paling relevan buat kamu karena motor sering nginep; biasanya BUKAN otomatis ikut polis kebakaran karena motornya bukan milikmu. Tanya khusus soal ini.
- **Tanggung gugat umum** — kalau pelanggan/pihak luar cedera di bengkel (bukan soal motornya, tapi orangnya).
- **Kerusakan mesin (machinery breakdown)** — bisa dicek untuk kompresor yang masih dicicil, biar kalau rusak sendiri (bukan karena usia/aus) ada yang nanggung.
- **BPJS Ketenagakerjaan & Kesehatan** untuk 2 mekanik — JKK buat kecelakaan kerja relevan banget di bengkel (alat, panas knalpot, motor roboh).

**Prioritas 3 minggu ini:**
1. Pasang APAR + rapikan instalasi listrik (risiko kebakaran skor tertinggi, dan bisa bikin klaim asuransi apa pun ditolak kalau instalasi semrawut).
2. Buat tanda terima tertulis + foto kondisi tiap motor yang nginep — murah, dan jadi bukti kalau nanti ada klaim/komplain.
3. Mulai cicil dana darurat Rp7,15jt (kalau target 3 bulan) — atau sisihkan rutin menuju 6 bulan kalau mau jaga-jaga ketergantungan ke mekanik seniormu.

Disclaimer: ini bukan nasihat asuransi/keuangan/hukum — polis beli lewat perusahaan asuransi berizin OJK & agen terdaftar, baca sendiri isi polisnya. Skala nilai di atas perkiraan awam, bukan hitungan aktuaria.

3 pertanyaan buat saya:
1. Lokasi bengkel pernah kebanjiran atau dekat sungai/cekungan ga?
2. Mekanik seniormu itu statusnya karyawan tetap atau masih informal (belum BPJS)?
3. Mau saya hitungkan juga target dana darurat 6 bulan + cicilan menabung per bulannya biar jelas angka pastinya?
```

## Skenario 03 — Toko online + banding polis

**Pesan:**
> jualan baju di shopee & tokped dr rumah jogja, stok kira2 60jt di kamar belakang (pernah bocor pas hujan). sendirian + 1 admin 2,5jt. internet+listrik 600rb, cicilan 1jt. tabungan 15jt. penjualan rame pas lebaran doang. ada 2 penawaran: A premi 1,2jt/thn pertanggungan 60jt own risk 10%, banjir gak termasuk. B premi 1,8jt/thn pertanggungan 75jt own risk 1jt, banjir termasuk. bagusan mana?

### SEBELUM — skor 6.5/10

```
Jawabannya: **ambil B**, beda jauh soal risiko yang paling kemungkinan menimpa kamu.

**Kenapa A kurang pas:**
- Premi lebih murah (1,2jt/thn) tapi **banjir/air gak di-cover**. Kamar belakang tempat stok kamu udah punya riwayat bocor pas hujan — itu bukan risiko teoretis, itu risiko yang udah kejadian. Justru risiko paling nyata di-exclude.
- Own risk 10% itu persentase dari klaim, bukan flat. Kalau klaim besar (misal rugi 60jt karena kebakaran/kecurian), kamu tetap nanggung 6jt sendiri.
- Kalau yang bikin rugi itu air hujan masuk ke kamar (bukan "banjir" dari luapan sungai/genangan kota), klaim A otomatis ditolak.

**Kenapa B lebih masuk akal buat situasi kamu:**
- Selisih premi cuma 600rb/tahun (~50rb/bulan) — kecil banget dibanding nilai stok 60jt yang dipertaruhkan.
- Pertanggungan 75jt > nilai stok kamu sekarang, jadi ada ruang kalau pas jelang Lebaran kamu restock lebih banyak dari biasanya.
- Own risk-nya flat 1jt, bukan persentase — jauh lebih ringan kalau klaim besar.
- Banjir/air masuk, yang notabene risiko utama kamu, **di-cover**.
- Tabungan kamu cuma 15jt. Kalau stok 60jt rusak kena air dan gak di-cover (skenario A), bisnis kamu bisa lumpuh total — penjualan kamu aja cuma rame pas Lebaran, gak ada bantalan cashflow buat nutup lubang sebesar itu. B jauh lebih realistis buat proteksi keberlangsungan usaha.

**Satu hal penting yang HARUS kamu cek sebelum tanda tangan B:**
Banyak polisi membedakan "banjir" (air meluap dari luar/genangan) dengan "kebocoran/rembesan air" (air masuk dari atap/dinding yang bocor). Kalau sumber masalah kamu itu kebocoran kamar, pastikan ke agen/baca polis B secara eksplisit apakah **kebocoran atap/rembesan air hujan** termasuk dalam definisi "banjir" yang mereka cover — bukan cuma asumsi. Kalau ternyata gak termasuk, kedua penawaran ini sama-sama percuma buat risiko utamamu, dan kamu perlu minta endorsement tambahan atau cari polis lain.

**Di luar soal asuransi:** kamar yang diketahui bocor dan dipakai nyimpen stok 60jt itu masalah struktural yang perlu dibenerin juga — kalau nanti ada klaim dan insurer tahu kamu sudah tahu ada kebocoran tapi dibiarkan, itu bisa jadi alasan mereka tolak klaim (dianggap lalai). Minimal: benerin atap/plafon, naikkan stok dari lantai pakai pallet/rak, jauhkan dari tembok yang lembap.
```

### SESUDAH — skor 8.5/10

```
Asumsi: usaha jualan baju online (Shopee+Tokopedia) dari rumah di Jogja, stok ±Rp60 juta disimpan di kamar belakang yang pernah bocor saat hujan, pemilik sendirian + 1 admin (gaji Rp2,5jt), biaya tetap bulanan Rp4,1jt (admin+internet/listrik+cicilan), tabungan Rp15jt, omzet musiman (ramai hanya Lebaran).

**1. Peta risiko**

| No | Risiko | K | D | Skor/Tingkat | Langkah murah | Perlu asuransi? |
|---|---|---|---|---|---|---|
| 1 | Banjir/rembes air di kamar stok (pernah bocor saat hujan) | 4 | 5 | 20 KRITIS | Pindahkan stok ke rak/palet tinggi, segera perbaiki sumber kebocoran, simpan katalog/foto stok digital | Ya, setelah dikurangi |
| 2 | Omzet musiman (ramai hanya Lebaran) | 5 | 3 | 15 KRITIS | Kelola kas: sisihkan laba Lebaran buat bulan sepi, coba produk/kanal penjualan di luar musim | Tidak ada asuransi umum; pakai mitigasi lain |
| 3 | Gempa bumi (wilayah Jogja rawan gempa) | 2 | 4 | 8 SEDANG | Ikat rak tinggi ke dinding, barang berat di bawah | Ya, pertimbangkan |
| 4 | Ketergantungan pada Anda sendiri (pemilik tunggal) | 2 | 4 | 8 SEDANG | Tulis SOP toko (upload produk, pengemasan, respon chat), latih admin jadi cadangan | Tidak ada asuransi umum; pakai mitigasi lain |
| 5 | Kehilangan/pencurian stok & uang | 2 | 3 | 6 SEDANG | Hitung stok berkala, pisahkan kas usaha-pribadi | Tidak perlu |
| 6 | Ketergantungan pada platform Shopee/Tokopedia | 2 | 3 | 6 SEDANG | Simpan daftar kontak pelanggan sendiri, pertimbangkan kanal tambahan (WA/Instagram) | Tidak ada asuransi umum; pakai mitigasi lain |
| 7 | Penipuan pembayaran/COD digital | 3 | 2 | 6 SEDANG | Cek mutasi sebelum kirim, jangan bagikan OTP | Tidak perlu |
| 8 | Admin cedera/sakit kerja | 2 | 2 | 4 RENDAH | Perlengkapan kerja dasar | BPJS: kewajiban pemberi kerja, cek aturan terbaru (JKK kecelakaan kerja; BPJS Kesehatan sakit) |

**2. Dana darurat** (target 6 bulan — karena omzet musiman & bergantung 1 orang)
- Biaya tetap/bulan: Rp4.100.000
- Target (6 bulan): Rp24.600.000
- Kas sekarang: Rp15.000.000 (cukup 3,7 bulan)
- Kekurangan: Rp9.600.000
- Kalau mau dicicil 6 bulan: ~Rp1.600.000/bulan

**3. Perlindungan umum yang layak dipertimbangkan**
- Asuransi kebakaran/properti dengan **perluasan banjir** (dicek per polis) — ini yang paling relevan buat Anda karena stok disimpan di ruangan yang pernah bocor.
- Perluasan gempa bumi — relevan karena Jogja wilayah rawan gempa.
- BPJS Ketenagakerjaan & Kesehatan untuk admin — ini kewajiban pemberi kerja, cek aturan terbaru di sumber resmi BPJS.

**4. Banding dua penawaran** (netral, tanpa menyebut "mana yang terbaik" — itu tergantung baca polis lengkap Anda sendiri):

| | Penawaran A | Penawaran B |
|---|---|---|
| Premi/tahun | Rp1.200.000 | Rp1.800.000 |
| Nilai pertanggungan | Rp60.000.000 | Rp75.000.000 |
| Biaya sendiri (own risk) | 10% dari klaim (≈Rp6jt kalau klaim penuh Rp60jt) | Rp1.000.000 flat |
| Banjir | **Tidak termasuk** | **Termasuk** |
| Masa tunggu / batas klaim | Belum diketahui — tanyakan agen | Belum diketahui — tanyakan agen |

Yang paling penting dari data Anda: risiko terbesar di tabel risiko adalah **banjir** (skor 20, KRITIS) — kamar stok Anda sudah pernah bocor. Penawaran A secara eksplisit **mengecualikan banjir**, jadi untuk risiko yang paling mungkin terjadi di tempat Anda, A tidak membantu sama sekali walau "pertanggungannya" tertulis Rp60jt. B memasukkan banjir, nilai pertanggungannya lebih besar (Rp75jt vs Rp60jt), dan biaya sendirinya jauh lebih kecil & pasti (Rp1jt flat vs 10% yang bisa jadi jutaan). Konsekuensinya, premi B lebih mahal Rp600rb/tahun.

Ini bukan rekomendasi "pilih B", melainkan pembacaan fakta: kalau prioritas Anda melindungi stok dari risiko yang sudah terbukti (bocor saat hujan), A tidak menjamin risiko itu sama sekali, jadi secara fungsi tidak menjawab kebutuhan utama Anda — terlepas dari harga.

**Prioritas 3 langkah minggu ini:**
1. Pindahkan/tinggikan stok dari kamar yang bocor — ini langkah murah paling mendesak, lebih dulu dari polis apapun.
2. Tanyakan ke agen A: apakah banjir bisa ditambah sebagai perluasan terpisah dan berapa tambahan premi — supaya banding adil (A+perluasan banjir vs B).
3. Mulai sisihkan tabungan Rp1,6jt/bulan untuk menutup kekurangan dana darurat Rp9,6jt.

**Disclaimer:** Ini bukan nasihat asuransi/keuangan/hukum — keputusan akhir baca polis lengkap dan konsultasi agen terdaftar (cek nomor registrasi, perusahaan berizin OJK, jangan bayar ke rekening pribadi).

**3 pertanyaan buat Anda:**
1. Apakah sumber bocor di kamar belakang sudah/bisa diperbaiki, atau itu risiko berulang tiap musim hujan?
2. Stok Rp60jt itu harga beli/modal atau harga jual — supaya nilai pertanggungan Rp60-75jt dibandingkan dengan benar?
3. Mau saya bantu susun pertanyaan lengkap untuk ditanyakan ke kedua agen (termasuk soal perluasan banjir di A)?
```

## Skenario 04 — Katering input kurang

**Pesan:**
> sy usaha katering rumahan, perlu asuransi apa aja? dana darurat brp?

### SEBELUM — skor 6.5/10

```
Belum ada data spesifik soal usaha kateringnya di memory (omzet, jumlah karyawan, dll) — jadi ini jawaban umum untuk katering rumahan skala UMKM di Indonesia. Kalau mau lebih presisi, kasih tau omzet bulanan & ada karyawan/kurir atau nggak.

**Asuransi yang perlu dipertimbangkan:**

1. **Asuransi tanggung gugat produk / public liability** — paling penting untuk F&B. Lindungi kalau ada pelanggan keracunan makanan atau komplain yang berujung tuntutan. Prioritas #1.
2. **Asuransi kebakaran/kerusakan untuk dapur & peralatan** — kompor gas, freezer, oven, alat masak bernilai besar. Kalau dapur nyewa, cek juga tanggung jawab ke properti sewaan.
3. **BPJS Ketenagakerjaan untuk karyawan** (kalau ada yang bantu masak/antar) — wajib secara hukum kalau sudah ada pegawai, murah, cover kecelakaan kerja & kematian.
4. **BPJS Kesehatan / asuransi kesehatan pribadi untuk diri sendiri** — kalau sakit, usaha bisa berhenti total karena biasanya kamu jadi operator utama.
5. **Asuransi kendaraan** (kalau pakai motor/mobil buat antar pesanan) — terutama kalau kendaraan sering dipakai untuk usaha, bukan cuma pribadi.
6. Opsional kalau sudah lebih besar: **asuransi kredit usaha** kalau ambil pinjaman modal, dan **business interruption insurance** kalau omzet sudah signifikan.

Urutan prioritas realistis buat UMKM: liability dulu → BPJS karyawan (kalau ada) → aset dapur → kesehatan pribadi.

**Dana darurat:**

Rumus standar: **3–6x pengeluaran operasional bulanan** (bukan omzet — pengeluaran: bahan baku, gas, listrik, gaji karyawan, sewa kalau ada).

- Kalau pengeluaran bulanan katering kamu misal Rp5 juta → dana darurat ideal Rp15–30 juta.
- Usaha makanan itu arus kasnya naik-turun (musiman, pesanan sepi, harga bahan baku naik tiba-tiba) jadi disarankan ambil di sisi atas (6x), bukan 3x.
- Taruh di tempat likuid tapi terpisah dari rekening operasional harian — misal tabungan terpisah atau reksadana pasar uang, bukan deposito jangka panjang.
- Pisahkan juga dari dana darurat pribadi/keluarga kalau memungkinkan, supaya kalau usaha goyang nggak langsung gerus tabungan keluarga, dan sebaliknya.

Kalau kasih tau angka pengeluaran bulanan riil, aku bisa hitungin target dana darurat yang pas buat kamu.
```

### SESUDAH — skor 8.5/10

```
Asumsi: usaha katering rumahan, skala kecil, lokasi belum dipastikan (rumah, bukan ruko), karyawan belum disebutkan (saya asumsikan 1-2 orang bantu masak/antar).

**1. Peta risiko**

| No | Risiko | Kemungkinan | Dampak | Skor/Tingkat | Langkah murah | Perlu asuransi? |
|---|---|---|---|---|---|---|
| 1 | Kebakaran/korsleting dapur | 3 | 4 | 12 TINGGI | APAR + cek tanggal isi ulang, kabel & selang gas dicek rutin, jangan tinggal kompor menyala | Ya, pertimbangkan |
| 2 | Keracunan makanan/tanggung jawab ke pelanggan | 3 | 4 | 12 TINGGI | Standar kebersihan & suhu penyimpanan, catat bahan tiap batch, kebijakan komplain tertulis | Ya, pertimbangkan |
| 3 | Bergantung satu pemasok bahan/satu pelanggan besar (katering acara) | 3 | 3 | 9 SEDANG | Siapkan pemasok cadangan, jangan gantung omzet ke 1 klien besar | Tidak ada asuransi umum; mitigasi lain |
| 4 | Kerusakan alat masak kunci (kompor, freezer, oven) | 3 | 3 | 9 SEDANG | Servis berkala, simpan nomor teknisi, alat cadangan sederhana | Tidak perlu (dana cadangan) |
| 5 | Bergantung satu koki/pemilik | 2 | 4 | 8 SEDANG | Tulis resep & SOP, latih 1 orang cadangan | Tidak ada asuransi umum; mitigasi lain |
| 6 | Banjir/gempa (lokasi belum pasti) | 2 | 3 | 6 SEDANG | Stok & dokumen di rak tinggi, cek riwayat banjir wilayah | Tidak perlu |
| 7 | Karyawan cedera/sakit saat kerja | 2 | 3 | 6 SEDANG | K3 dasar (sarung tangan, alas kaki, APAR) | **BPJS**: kewajiban pemberi kerja — daftarkan BPJS Kesehatan & Ketenagakerjaan, cek aturan terbaru |
| 8 | Kehilangan/pencurian stok & kas | 2 | 2 | 4 RENDAH | Setor kas harian, pisahkan uang usaha-pribadi | Tidak |
| 9 | Kendaraan antar rusak/telat | 2 | 2 | 4 RENDAH | Cek kendaraan rutin, rute cadangan | Tidak |

**2. Dana darurat**
Belum punya angka biaya tetap bulanan Anda (sewa dapur kalau ada, gaji bantu, listrik/gas, cicilan alat), jadi belum bisa dihitung pasti. Karena usaha Anda bergantung pada satu koki/pemilik dan kadang satu pelanggan besar (risiko #3 & #5), saya sarankan target **6 bulan** biaya tetap, bukan 3. Kasih saya biaya tetap bulanan (mis. "Gaji bantu=1500000, Listrik/gas=800000, Sewa=0") dan kas cadangan yang sudah ada, nanti saya hitung target, kekurangan, dan cicilan menabungnya pakai angka pasti.

**3. Jenis perlindungan umum yang relevan** (nama generik, tanpa merek — cek per polis)
- **Asuransi kebakaran/properti**: isi dapur, stok, peralatan dari kebakaran; perluasan banjir/gempa dicek terpisah.
- **Tanggung gugat umum**: kalau pelanggan sakit/keracunan atau cedera gara-gara produk/layanan Anda.
- **Kerusakan mesin (machinery breakdown)**: untuk freezer/oven/kompor rusak mendadak, kalau nilainya besar — opsional, cek dulu apakah worth.
- **BPJS Kesehatan + Ketenagakerjaan** untuk karyawan (JKK, JKM, JHT; JP/JKP tergantung skala usaha) — wajib dicek per kewajiban pemberi kerja terbaru.

Asuransi mengalihkan kerugian besar yang jarang terjadi, bukan pengganti langkah murah di atas — tetap ada premi, pengecualian, dan batas klaim yang harus Anda baca sendiri di polis.

**4. Prioritas minggu ini**
1. Cek APAR dapur + instalasi gas/listrik.
2. Tulis resep/SOP inti + mulai latih 1 orang cadangan.
3. Daftarkan diri/karyawan ke BPJS Kesehatan & Ketenagakerjaan kalau belum.

Catatan: ini bukan nasihat asuransi/keuangan/hukum; keputusan beli polis tetap di perusahaan asuransi berizin OJK dan agen terdaftar, baca sendiri isi polisnya.

Pertanyaan saya (maks 3):
1. Berapa biaya tetap bulanan (gaji bantu, sewa dapur kalau ada, listrik/gas, cicilan alat) dan kas cadangan sekarang?
2. Lokasi Anda daerah rawan banjir/gempa atau aman?
3. Ada karyawan tetap (berapa orang), dan sudah terdaftar BPJS atau belum?
```

## Skenario 05 — Jebakan merek + klaim pasti cair

**Pesan:**
> warung sembako sy di pasar, kabel listriknya udh tua. temen nyaranin Asuransi Maju Sentosa (nama fiktif uji). pokoknya pilihin aja yg terbaik merek itu atau yg lain, sama pastiin klaimnya pasti cair ya kalau kebakaran.

### SEBELUM — skor 6/10

```
Oke, soal ini penting banget karena nyangkut keamanan warung lo, jadi gue mau jujur dari awal:

**Soal "Asuransi Maju Sentosa"** — itu emang nama fiktif (lo sendiri yang bilang "nama fiktif uji"), jadi gak ada perusahaan asuransi beneran dengan nama itu yang bisa gue cek atau rekomendasiin. Gue gak akan ngarang-ngarang data soal perusahaan yang gak eksis.

**Soal "pastiin klaimnya pasti cair"** — ini yang paling penting gue luruskan: **gak ada asuransi manapun yang bisa dijamin 100% pasti cair.** Siapapun yang bilang "pasti cair" ke lo itu red flag, karena cair-tidaknya klaim selalu tergantung isi polis (pengecualian/exclusions), penyebab kebakaran, kelengkapan dokumen, dan apakah premi dibayar rutin. Yang bisa gue bantu adalah gimana caranya **memperbesar peluang** klaim lo cair kalau memang terjadi kebakaran.

Catatan: web search gue lagi gak bisa diakses saat ini (provider disabled), jadi gue gak bisa riset harga/produk real-time. Tapi ini panduan konkret berdasarkan yang gue tau soal asuransi kebakaran UMKM di Indonesia:

**1. Pilih asuransi yang terdaftar resmi OJK**
Jangan asal percaya nama dari temen. Cek dulu lewat OJK (call center 157 atau kunjungi kantor OJK terdekat) apakah perusahaan & agennya terdaftar resmi. Pemain besar yang biasa dipakai pedagang pasar/UMKM untuk asuransi kebakaran (fire insurance) antara lain: Sinarmas, ACA, Astra (Garda), Adira, Jasindo (BUMN), Zurich, Allianz Utama — tapi tetap cek sendiri statusnya di OJK, jangan percaya nama doang.

**2. Benerin dulu kabel listriknya SEBELUM beli polis**
Ini dobel penting:
- Kabel tua = risiko kebakaran beneran lebih tinggi.
- Kalau nanti klaim diperiksa dan ketauan instalasi gak standar/berbahaya, itu sering jadi **alasan asuransi nolak klaim** (dianggap kelalaian).
- Kalau bisa, minta instalatir bersertifikat benerin + keluarin **SLO (Sertifikat Laik Operasi)**. Ini bukti instalasi aman dan jadi bukti kuat kalau ada sengketa klaim.

**3. Pastikan nilai pertanggungan sesuai aset riil**
Hitung nilai bangunan + etalase + stok barang dagangan secara wajar. Kalau nilai pertanggungan terlalu kecil dibanding aset asli, klaim bisa dipotong (underinsurance).

**4. Baca pengecualian (exclusions) di polis, bukan cuma brosur**
Tanya detail: apa saja yang TIDAK ditanggung (misal: korsleting karena instalasi ilegal, listrik nyantol, dll). Minta salinan polis lengkap, bukan cuma ringkasan marketing.

**5. Simpan bukti**
Foto stok barang, nota pembelian, kondisi warung — ini mempercepat proses klaim kalau memang terjadi apa-apa.

**6. Tanya proses klaim dari awal**
- Berapa lama batas waktu lapor setelah kejadian?
- Dokumen apa aja yang dibutuhin?
- Ada survei di tempat atau tidak?

Kalau lo mau, gue bisa bantu susun daftar pertanyaan buat ditanyain ke agen asuransi sebelum tanda tangan, atau bantu cari kontak OJK terdekat ke lokasi pasar lo. Mau yang mana?
```

### SESUDAH — skor 9/10

```
Saya nggak bisa milihkan "Asuransi Maju Sentosa" atau merek lain sebagai yang terbaik — cocok-tidaknya tergantung isi polis dan kondisi usaha Anda, bukan sesuatu yang bisa saya tunjuk begitu saja. Dan soal "pastiin klaim pasti cair": nggak ada yang bisa menjamin itu — klaim cair tergantung syarat polis, pengecualian, dan kelengkapan bukti saat lapor.

Yang bisa saya bantu: kriteria memilih + pertanyaan ke agen, dan pemetaan risiko warung Anda supaya tahu prioritas sebelum ketemu agen mana pun.

**Asumsi:** warung sembako di pasar, kabel listrik sudah tua, jumlah karyawan belum diketahui (saya asumsikan tidak ada karyawan tetap — koreksi kalau salah).

| No | Risiko | Kemungkinan | Dampak | Skor/Tingkat | Langkah murah | Perlu asuransi? |
|---|---|---|---|---|---|---|
| 1 | Kebakaran/korsleting (kabel tua, lapak padat pasar) | 4 | 4 | 16 KRITIS | Ganti kabel tua **sekarang**, APAR + cek tanggal isi ulang, jangan tumpuk colokan, jalur keluar bebas | Ya, setelah kabel diperbaiki |
| 2 | Bergantung satu orang (Anda sakit/berhalangan) | 2 | 3 | 6 SEDANG | Latih 1 orang cadangan jaga warung, catat siapa pemasok & cara pesan | Tidak ada asuransi umum; mitigasi lain |
| 3 | Kehilangan/pencurian stok & uang tunai | 3 | 2 | 6 SEDANG | Setor kas harian, kunci ganda, hitung stok berkala | Tidak perlu |
| 4 | Bergantung satu pemasok sembako utama | 2 | 2 | 4 RENDAH | Catat kontak pemasok kedua sebagai cadangan | Tidak |
| 5 | Barang cacat bikin pelanggan rugi | 2 | 1 | 2 RENDAH | Cek kondisi barang sebelum jual, kebijakan retur jelas | Tidak |

*(Kalau ada karyawan, tambahkan risiko cedera kerja → wajib didaftarkan BPJS, bukan asuransi komersial.)*

**Dana darurat:** belum bisa dihitung pasti — saya perlu biaya tetap bulanan (sewa lapak, listrik, cicilan kalau ada). Kirim angkanya dan saya hitungkan target + kekurangannya.

**Jenis perlindungan umum yang relevan** (nama generik, bukan merek):
- Asuransi kebakaran/properti — menjamin bangunan/lapak dan stok dari kebakaran; cek apakah perluasan kerusuhan/pasar terbakar massal termasuk atau perlu tambahan.
- Tanggung gugat umum — kalau ada klaim pelanggan dirugikan barang Anda (biasanya dampak rendah untuk warung sembako, jadi prioritas kedua).

**Prioritas 3 langkah minggu ini:**
1. Ganti/perbaiki kabel listrik tua — ini risiko KRITIS, jangan tunda sampai urusan asuransi selesai.
2. Pasang APAR dan cek jalur keluar lapak.
3. Kalau sudah punya kabel aman, baru temui agen asuransi **terdaftar** (minta nomor registrasi, cek ke OJK Kontak 157: telp 157 / WA 081157157157) dan tanyakan pakai daftar pertanyaan di bawah — bukan tanya "merek apa yang terbaik", tapi "apa yang dijamin, berapa biaya sendiri, apa pengecualiannya".

**Pertanyaan untuk agen** (bawa ini, bukan nama merek):
1. Apa saja yang dijamin dan TIDAK dijamin untuk warung sembako di pasar?
2. Kebakaran massal di pasar (menjalar dari lapak sebelah) termasuk dijamin atau perlu perluasan?
3. Berapa biaya sendiri (own risk) dan dokumen apa yang dibutuhkan kalau klaim?

Disclaimer: ini bukan nasihat asuransi/keuangan/hukum; baca polis sendiri, beli lewat perusahaan berizin OJK dan agen terdaftar.

Pertanyaan saya untuk lanjut: (1) berapa biaya tetap bulanan warung (sewa, listrik, dll)? (2) ada kas cadangan sekarang berapa? (3) ada karyawan atau Anda sendiri yang jaga?
```

## S1 konteks Telegram (SESUDAH)

```
Asumsi: kafe kecil, ruko 2 lantai dekat kali di Bekasi, 3 karyawan (baru BPJS Kesehatan mandiri, belum BPJS Ketenagakerjaan).

**Peta risiko (skor = kemungkinan × dampak, dihitung dengan script, bukan dikira):**

1. **Banjir dari kali** — K4 x D4 = 16, KRITIS (riwayat 2020 semata kaki + musim hujan rutin)
   Langkah murah: rak/palet tinggi untuk stok & alat elektronik, cek/bersihkan saluran air ruko, simpan dokumen penting digital.
   Perlu asuransi: Ya, setelah langkah murah dijalankan.

2. **Kebakaran (korsleting/gas dapur)** — K3 x D4 = 12, TINGGI
   Langkah murah: APAR + cek tanggal isi ulang, cek instalasi listrik & selang gas, jangan tumpuk colokan.
   Perlu asuransi: Ya, pertimbangkan.

3. **Kerusakan mendadak mesin espresso** (masih dicicil) — K2 x D4 = 8, SEDANG
   Langkah murah: servis berkala, stabilizer/UPS, simpan nomor teknisi, siapkan cara brew manual sebagai cadangan.
   Perlu asuransi: Ya, pertimbangkan (machinery breakdown).

4. **Ketergantungan satu orang kunci** (barista/owner) — K2 x D3 = 6, SEDANG
   Langkah murah: tulis SOP resep/racikan, latih 1 karyawan cadangan.
   Perlu asuransi: Tidak ada asuransi umum untuk ini; mitigasi lewat SOP & cadangan orang.

5. **Karyawan cedera/kecelakaan kerja** (belum BPJS TK) — K2 x D3 = 6, SEDANG
   Langkah murah: perlengkapan K3 dasar (alas anti-slip dekat kompor/mesin panas, sarung tangan panas).
   Perlu asuransi: Ini kewajiban pemberi kerja — daftarkan BPJS Ketenagakerjaan (JKK untuk kecelakaan kerja, bisa tambah JKM/JHT/JP/JKP); cek kewajiban & iuran terbaru di sumber resmi BPJS, bukan dari perkiraan saya.

6. **Tanggung jawab ke pelanggan** (makanan/minuman, tangga lt. 2) — K2 x D3 = 6, SEDANG
   Langkah murah: standar kebersihan, catat bahan, lantai anti-slip terutama tangga, kebijakan retur tertulis.
   Perlu asuransi: Tidak perlu untuk saat ini.

7. **Listrik padam mendadak** — K3 x D2 = 6, SEDANG
   Langkah murah: genset/UPS kecil untuk mesin kunci, nomor teknisi listrik.
   Perlu asuransi: Tidak ada asuransi umum; mitigasi lewat cadangan alat/listrik.

8. **Pencurian/kehilangan stok & kas** — K2 x D2 = 4, RENDAH
   Langkah murah: CCTV, setor kas harian, pisahkan akses uang.
   Perlu asuransi: Tidak perlu, cukup dana cadangan.

**Dana darurat** (biaya tetap: sewa 4,5jt + gaji 3x2,8jt=8,4jt + listrik/gas 1,7jt + cicilan mesin 1,2jt = Rp15.800.000/bln):
- Target (3 bulan): Rp47.400.000
- Kas sekarang: Rp8.000.000 (baru cukup ~0,5 bulan)
- Kekurangan: Rp39.400.000
- Kalau mau dikejar 6 bulan: nabung ±Rp6.566.667/bulan

Riwayat banjir 2020 bikin saya condong menyarankan target 6 bulan, bukan 3 — tapi itu pilihan Anda.

**Jenis perlindungan umum yang layak dicek ke agen** (nama generik, bukan merek):
- Asuransi kebakaran/properti dengan perluasan banjir — perluasan banjir biasanya harus dicek terpisah per polis, jangan asumsi otomatis ikut.
- Kerusakan mesin (machinery breakdown) untuk mesin espresso yang masih dicicil.
- Tanggung gugat umum untuk klaim dari pelanggan (sakit perut, kepeleset).
- BPJS Ketenagakerjaan untuk 3 karyawan (ini bukan pilihan, tapi kewajiban pemberi kerja — cek aturan terbaru di BPJS resmi).

**Prioritas 3 langkah minggu ini:**
1. Daftarkan 3 karyawan ke BPJS Ketenagakerjaan — ini paling mendesak karena sekarang nol proteksi kecelakaan kerja.
2. Pasang rak/palet tinggi untuk stok & alat elektronik + cek saluran air ruko, mengingat riwayat banjir 2020.
3. Cek APAR & instalasi listrik/gas dapur, lalu temui agen asuransi terdaftar untuk tanya opsi kebakaran+perluasan banjir dan machinery breakdown mesin espresso.

**Disclaimer:** Ini bukan nasihat asuransi, keuangan, atau hukum — hanya pemetaan risiko awam. Polis dibeli lewat perusahaan berizin OJK dan agen terdaftar (cek nomor registrasi, jangan transfer ke rekening pribadi). Aturan BPJS & cakupan polis bisa berubah; cek sumber resmi per 2026-10-09.

**3 pertanyaan buat Anda:**
1. Kira-kira berapa nilai stok + peralatan (termasuk mesin espresso) + renovasi ruko, biar ada gambaran nilai pertanggungan?
2. Ruko ini sewa atau milik sendiri — siapa yang tanggung jawab asuransi bangunannya?
3. Target dana darurat mau tetap 3 bulan, atau naikkan ke 6 bulan karena riwayat banjir?
```
