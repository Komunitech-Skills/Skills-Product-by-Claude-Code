# Uji OpenClaw sebelum/sesudah: cek-risiko-dan-asuransi-usaha v1.0.1

- **Tanggal:** 2026-10-10
- **Penguji:** penguji otomatis Komunitech (agent independen, bukan pembuat skill)
- **Cara uji:** OpenClaw 2026.9.8 lokal (`openclaw agent --local`), model router Komunitech `claude-sonnet-5`. SEBELUM = home tanpa skill; SESUDAH = home berisi hanya `cek-risiko-dan-asuransi-usaha`. Home dibuat ulang bersih per skenario (`mk-home.sh`). Skenario 1 SESUDAH juga di konteks Telegram (`--channel telegram`, tanpa `--deliver`). Mesin uji internal: `run-uji.sh` (tanpa `unshare` karena batasi container).
- **Tes script:** `python3 tests/uji_regresi.py` → 16 tes OK.
- **Verifikasi angka:** Python independen (biaya tetap, target dana, kekurangan, cicilan, contoh klaim polis) — cocok output SESUDAH.


---

## Skenario 01 — kafe ruko dekat kali

**Pesan:**
> kak sy punya kafe kecil di ruko 2 lt deket kali di bekasi, karyawan 3 (blm ikut bpjs tk, cuma bpjs kes yg mandiri masing2). sewa 4,5jt/bln, gaji @2,8jt, listrik+gas 1,7jt, cicilan mesin espresso 1,2jt. kas cadangan cuma 8jt. thn 2020 pernah kebanjiran semata kaki. perlu asuransi apa ya? dana darurat brp?

### SEBELUM (skill mati)

Oke, breakdown dulu biar jelas baru masuk rekomendasi.

**Biaya tetap bulanan kafe kamu:**
- Sewa: 4,5jt
- Gaji 3 karyawan: 8,4jt
- Listrik+gas: 1,7jt
- Cicilan mesin espresso: 1,2jt
- **Total fixed cost: ±15,8jt/bulan**

Kas cadangan 8jt itu cuma nutup **~0,5 bulan** operasional. Kalau kena banjir lagi kayak 2020 dan kafe harus tutup 2-4 minggu buat bersih-bersih/perbaikan, kas itu habis duluan sebelum kafe balik buka.

**Dana darurat idealnya:**
- Minimal **3 bulan** fixed cost = ~47jt (buffer dasar)
- Target aman **4-6 bulan** = ~63-95jt — karena kamu punya risiko spesifik (lokasi dekat kali, pernah kebanjiran semata kaki), bukan cuma risiko umum usaha
- Realistisnya nabung bertahap: kejar 47jt dulu, baru naik ke 90jt-an. Taruh di rekening/produk terpisah dari kas operasional biar gak "numpang kepake".

**Asuransi yang kamu perlu, urut prioritas:**

1. **BPJS Ketenagakerjaan buat 3 karyawan — ini wajib hukum, bukan opsional.** Sekarang mereka cuma punya BPJS Kesehatan mandiri, belum ada JKK (kecelakaan kerja) + JKM (kematian) dari kamu sebagai pemberi kerja. Preminya murah (sekitar 1%-an dari gaji buat JKK + 0,3% JKM, total gak sampai 100rb/orang/bulan). Risiko kerja di kafe ada (mesin espresso panas, pisau, lantai basah) — kalau ada kecelakaan dan karyawan gak ter-cover, kamu yang nanggung semua + kena masalah legal.

2. **Asuransi properti/usaha dengan perluasan banjir.** Ini kunci buat kasus kamu. Asuransi kebakaran standar (PSAKI) di Indonesia **TIDAK otomatis cover banjir** — banjir itu perluasan jaminan tambahan (FLEXAS + banjir/badai/angin topan). Pastikan nanya eksplisit "ada perluasan banjir gak" ke agen, jangan asumsi udah include. Ini cover bangunan, interior, dan isi (termasuk mesin espresso, kulkas, perabot).

3. **Business interruption / gangguan usaha** (kalau budget memungkinkan, atau cukup banyak paket properti nawarin ini sebagai rider). Fungsinya nutup sewa+gaji+cicilan selama kafe tutup gara-gara banjir/kebakaran — ini yang bikin dana darurat gak langsung tergerus habis.

4. **Public liability** (tanggung gugat pihak ketiga) — kalau pelanggan slip/jatuh di kafe. Nice to have, relatif murah, worth dipertimbangkan karena ruko 2 lantai ada tangga = risiko jatuh lebih tinggi dari kafe 1 lantai biasa.

**Ringkesnya kalau budget terbatas:** kejar BPJS TK dulu (wajib + murah) bareng asuransi properti+banjir (karena history banjir kamu nyata, bukan teori), sambil nabung dana darurat ke 47jt. Business interruption & public liability nyusul kalau cashflow udah lebih longgar.

Mau aku bantu hitung simulasi premi BPJS TK per karyawan atau cariin referensi asuransi properti yang ada perluasan banjir di area Bekasi?

**Skor: 7/10**

### SESUDAH (skill aktif)

Asumsi: kafe kecil di ruko 2 lantai dekat kali (Bekasi), 3 karyawan (baru BPJS Kesehatan mandiri, belum BPJS Ketenagakerjaan), pernah banjir semata kaki 2020.

**Tabel risiko**

| No | Risiko | K | D | Skor/Tingkat | Langkah murah | Perlu asuransi? |
|---|---|---|---|---|---|---|
| 1 | Banjir (dekat kali, sudah pernah terjadi) | 4 | 4 | 16 KRITIS | Barang & stok naikkan ke lantai 2/rak tinggi, dokumen penting disalin digital, cek riwayat banjir & drainase sekitar | Ya, dipertimbangkan — tapi kurangi risiko dulu |
| 2 | Kesehatan/kecelakaan kerja karyawan | 3 | 3 | 9 SEDANG | Daftarkan BPJS Ketenagakerjaan (JKK, JKM, JHT) — saat ini belum, baru BPJS Kesehatan mandiri | BPJS (wajib bagi pemberi kerja, cek aturan terbaru) |
| 3 | Kebakaran/korsleting listrik | 2 | 4 | 8 SEDANG | APAR + cek tanggal isi ulang, ganti kabel/colokan tua, jauhkan dari tumpukan kardus | Ya, dipertimbangkan |
| 4 | Ketergantungan pada barista/orang kunci | 2 | 3 | 6 SEDANG | Tulis SOP resep & operasional, latih 1 cadangan | Tidak ada asuransi umum; pakai mitigasi lain |
| 5 | Tanggung jawab ke pelanggan (makanan, terpeleset) | 2 | 3 | 6 SEDANG | Standar kebersihan dapur, lantai antislip, catat sumber bahan | Tidak perlu (dana cadangan cukup) |
| 6 | Listrik padam/gangguan alat (termasuk mesin espresso) | 3 | 2 | 6 SEDANG | Nomor teknisi siap, pertimbangkan UPS kecil untuk POS/kasir | Tidak perlu (dana cadangan cukup) |
| 7 | Gempa bumi | 1 | 4 | 4 RENDAH | Ikat rak/perabot berat ke dinding | Ya, dipertimbangkan (jarang tapi berat) |
| 8 | Pencurian/kehilangan kas & stok | 2 | 2 | 4 RENDAH | CCTV, setor kas harian, pisahkan akses uang | Tidak |

**Dana darurat**
- Biaya tetap/bln: Rp15.800.000 (sewa 4,5jt + gaji 3×2,8jt=8,4jt + listrik/gas 1,7jt + cicilan mesin 1,2jt)
- Target 3 bulan: **Rp47.400.000**
- Kas sekarang: Rp8.000.000 — baru cukup **0,5 bulan**
- Kekurangan: **Rp39.400.000**
- Kalau ditabung 6 bulan: ~**Rp6.566.667/bln** — ini berat relatif ke biaya tetapmu sendiri; realistisnya mungkin perlu dicicil lebih lama (mis. 12 bulan ≈ Rp3,3jt/bln) sambil jalan.

**Perlindungan umum yang layak dicek (nama generik, bukan merek)**
- *Asuransi kebakaran/properti* — untuk bangunan ruko & isi/stok; **perluasan banjir wajib ditanyakan terpisah**, karena ini bukan proteksi standar dan lokasimu riwayatnya jelas rawan.
- *Tanggung gugat umum* — kalau ada pelanggan cedera/sakit di tempat.
- *Program jaminan sosial (BPJS Ketenagakerjaan)* — JKK & JKM untuk karyawan; ini soal kewajiban pemberi kerja, bukan pilihan, cek aturan terbaru di sumber resmi BPJS.
- Asuransi gempa biasanya juga perluasan terpisah dari polis kebakaran — tanyakan juga meski skornya rendah di sini.

**Prioritas 3 langkah minggu ini**
1. Pindahkan stok, kulkas kecil, dokumen, dan alat elektronik yang bisa diangkat ke level lebih tinggi/lantai 2 — ini risiko KRITIS dan gratis dilakukan sekarang.
2. Daftarkan 3 karyawan ke BPJS Ketenagakerjaan (minimal JKK+JKM) — ini kewajiban, belum sukarela.
3. Cek APAR & kondisi instalasi listrik, lalu hubungi agen asuransi berizin OJK untuk tanya harga perluasan banjir pada polis properti ruko.

Bukan nasihat asuransi/keuangan/hukum — ini pemetaan awam untuk bahan diskusi dengan agen berizin OJK; baca sendiri isi polis sebelum bayar premi.

Tiga pertanyaan:
1. Ruko ini milik sendiri atau sewa — kalau sewa, siapa yang idealnya pegang asuransi bangunan (pemilik) vs isi/stok (kamu)?
2. Mau pakai template pertanyaan untuk agen asuransi (soal perluasan banjir, premi, pengecualian)?
3. Target cicilan dana darurat mau dipercepat (lebih berat/bln) atau diperlambat (lebih lama tapi ringan)?

**Skor: 8.5/10** · Skill/script terpakai: ya (`read`/`exec`, script `cek_risiko.py`)

### SESUDAH — konteks Telegram (skenario 1)

Asumsi: kafe kecil di ruko 2 lantai dekat kali, Bekasi, 3 karyawan (BPJS Kesehatan mandiri masing-masing, belum ada BPJS Ketenagakerjaan dari usaha).

**Peta risiko** (skor = kemungkinan × dampak, dihitung dengan script, bukan kira-kira):

- Kebakaran (listrik/gas dapur, mesin espresso) — K2 × D5 = 10, TINGGI → kurangi dulu (cek instalasi listrik, APAR, cek selang gas) lalu **pertimbangkan asuransi**
- Banjir (riwayat 2020 semata kaki, dekat kali) — K4 × D3 = 12, TINGGI → kurangi dulu (lihat langkah di bawah); karena dampak belum sampai bikin tutup berminggu-minggu, fokus mitigasi dulu, asuransi properti dengan perluasan banjir baru dipertimbangkan kalau nilai aset/stok besar
- Kesehatan/kecelakaan kerja karyawan (belum BPJS TK) — K3 × D3 = 9, SEDANG → ini bukan "opsional diasuransikan", tapi **kewajiban pemberi kerja yang perlu dicek** (lihat poin BPJS)
- Tanggung jawab ke pelanggan (makanan/minuman bikin sakit, pelanggan cedera di tempat) — 6, SEDANG → kurangi + dana cadangan; tanggung gugat umum bisa dipertimbangkan kalau omzet makin besar
- Ketergantungan satu orang kunci (pemilik/barista utama) — 6, SEDANG, **tidak ada asuransi umum untuk ini** → kurangi lewat SOP/resep tertulis + latih 1 cadangan
- Gangguan listrik/kerusakan mesin espresso yang masih dicicil — 6, SEDANG → kurangi + dana cadangan (bukan pos asuransi terpisah biasanya)
- Kehilangan/pencurian kas & stok — 4, RENDAH → cukup diterima dengan dana cadangan + kebiasaan setor kas harian

**Dana darurat** (biaya tetap: sewa 4,5jt + gaji 3 karyawan 8,4jt + listrik/gas 1,7jt + cicilan mesin 1,2jt = Rp15.800.000/bulan):
- Target 6 bulan (saya naikkan dari default 3 bulan karena ada riwayat banjir berulang di lokasi): **Rp94.800.000**
- Kas cadangan sekarang: Rp8.000.000 → cuma cukup 0,5 bulan biaya tetap
- Kekurangan: **Rp86.800.000**
- Kalau mau dicicil menabung: ~Rp14,5jt/bln (6 bulan), ~Rp7,2jt/bln (12 bulan), atau ~Rp3,6jt/bln (24 bulan) — pilih yang realistis dari kas masuk kafe, jangan dipaksakan sampai ganggu operasional.

**Jenis perlindungan umum yang layak dipertimbangkan** (nama generik, tanpa merek — cocok-tidaknya tergantung polis dan kondisi usaha Anda):
- Asuransi kebakaran/properti — untuk bangunan ruko (kalau Anda yang punya)/isi/stok dari kebakaran; perluasan banjir biasanya dicek terpisah per polis, jangan diasumsikan otomatis masuk
- Tanggung gugat umum — kalau pelanggan sakit/cedera karena produk atau di tempat Anda
- BPJS Ketenagakerjaan (JKK, JKM, JHT, JP) untuk 3 karyawan — ini bukan asuransi komersial, tapi program jaminan sosial yang **kewajiban pemberi kerja perlu dicek ke sumber resmi BPJS terbaru**, karena BPJS Kesehatan mandiri yang sekarang mereka punya tidak menggantikan JKK/JKM/JHT dari sisi pekerjaan

**3 langkah prioritas minggu ini:**
1. Cek riwayat banjir wilayah ke sumber resmi (BPBD/BMKG) dan pindahkan stok, dokumen penting, serta alat elektronik ke rak tinggi/lantai 2 — ini risiko TINGGI yang paling murah dikurangi dulu
2. Cek instalasi listrik dan selang gas dapur, pastikan APAR ada dan masih berlaku, siapkan jalur keluar bebas
3. Tulis SOP/resep dasar dan latih 1 karyawan sebagai cadangan kalau Anda atau barista utama absen; lalu mulai cicil dana darurat (pilih salah satu dari 6/12/24 bulan di atas) sebelum menambah polis apa pun

Disclaimer: ini bukan nasihat asuransi, keuangan, atau hukum — skala nilai di atas pertimbangan awam, bukan hitungan aktuaria. Polis dibeli lewat perusahaan dan agen berizin OJK; cek izinnya sebelum bayar, dan jangan transfer ke rekening pribadi.

3 pertanyaan buat saya bantu lanjut:
1. Lokasinya persis di mana (RT/RW/kelurahan Bekasi) — supaya bisa dicek riwayat banjir lebih spesifik ke BPBD setempat?
2. Status ruko: sewa semua atau ada bagian milik sendiri — ini menentukan perlu asuransi properti atau cukup isi/stok?
3. Mau saya siapkan daftar pertanyaan ke agen asuransi berizin OJK (ada templatenya) untuk bandingkan penawaran kebakaran+banjir?

**Catatan:** format bullet vs tabel; angka dana tetap cocok.

---

## Skenario 02 — bengkel motor Makassar

**Pesan:**
> bengkel motor sy di depan rumah, makassar. mekanik 2, yg senior udh 8 thn sm sy, kl dia ga masuk bengkel ampir lumpuh. motor pelanggan kdg nginep. biaya tetap: gaji 7jt total, listrik 900rb, cicilan kompresor 650rb, lain2 500rb. tabungan usaha 20jt. perlu asuransi ga sih?

### SEBELUM (skill mati)

Oke, saya breakdown dulu sebelum jawab ya/tidak — soalnya "perlu asuransi" itu nggak satu jenis, dan nggak semua risiko yang disebutkan bisa diselesaikan asuransi.

**Catatan jujur:** web search saya lagi mati, jadi saya pakai pengetahuan umum soal aturan BPJS Ketenagakerjaan (relatif stabil, bukan yang sering berubah) — tapi untuk angka premi asuransi properti/liability, itu harus cek quote langsung ke agen karena variatif per insurer.

## Risiko yang disebutkan, dan mana yang sebenarnya "insurable"

**1. Motor pelanggan nginep → ini paling urgent, dan paling bisa habiskan tabungan sekali kejadian**
Kalau motor pelanggan hilang (dicuri) atau kebakaran/kebanjiran saat dititip di bengkel, secara hukum bengkel bisa dimintai ganti rugi penuh. Satu motor matic second aja bisa 15-20jt — itu bisa habisin tabungan usaha sampean dalam SATU kejadian. Ini namanya **bailee's liability / tanggung jawab pihak ketiga**, biasanya jadi rider dari paket asuransi properti usaha (cari ke Sinarmas, ACA, Tokio Marine, atau agen UMKM lokal Makassar — sering disebut "asuransi bengkel" atau "garage package"). Ini yang paling saya sarankan dicek duluan.

**2. Mekanik senior absen → ini BUKAN risiko yang bisa "diasuransikan" dalam arti operasional**
Asuransi nggak bisa bikin dia tetap masuk kerja atau nyediain pengganti yang sama skillnya. Yang bisa dibantu asuransi cuma sisi finansial *kalau* dia kecelakaan kerja atau meninggal:
- **BPJS Ketenagakerjaan (JKK + JKM)** untuk 2 mekanik — ini murah banget (kira-kira 1-1.2% dari total gaji, jadi ±70-85rb/bulan untuk berdua), dan ini juga **melindungi bengkel sampean** dari tuntutan kalau dia luka kerja (misal kena kompresor, luka bakar las, dll) — bisa dibilang ini hampir wajib menurut UU Ketenagakerjaan buat karyawan tetap.
- Tapi risiko sebenarnya (single point of failure skill) solusinya operasional, bukan asuransi: mulai latih mekanik kedua pegang kasus-kasus yang biasa senior tangani, atau punya kontak mekanik lepas (freelance) yang bisa di-panggil darurat. Itu PR terpisah dari "beli asuransi".

**3. Aset bengkel (kompresor yang masih dicicil, alat-alat)**
Kalau kebakaran atau alat dicuri sementara cicilan kompresor masih jalan, itu double hit: kehilangan alat + tetap nyicil utang. **Asuransi kebakaran/properti usaha** cocok di sini, biasanya bisa dibundling sama poin #1 jadi satu paket.

## Soal tabungan 20jt
Biaya tetap bulanan sampean = 7jt + 900rb + 650rb + 500rb = **9,05jt/bulan**. Tabungan 20jt itu cuma nutup ±2,2 bulan kalau bengkel berhenti total. Itu tipis. Jadi dua hal perlu jalan paralel:
- Asuransi nutup risiko **kejadian tiba-tiba** (motor hilang, kebakaran, kecelakaan kerja) yang nilainya besar sekaligus.
- Tabungan tetap perlu ditambah ke arah 3-6x biaya tetap (±27-54jt) buat nutup risiko **gradual** (sepi pelanggan, dll) yang asuransi nggak cover.

## Rekomendasi urutan aksi
1. Daftar **BPJS Ketenagakerjaan (JKK+JKM)** untuk 2 mekanik — paling murah, paling cepat, hampir pasti worth it. Bisa langsung ke kantor cabang BPJS TK Makassar atau urus online.
2. Minta quote **asuransi properti + liability pihak ketiga** (untuk motor pelanggan + alat bengkel) ke 2-3 agen lokal, bandingkan harga vs limit tanggungan.
3. Paralel, naikkan tabungan usaha pelan-pelan ke target 30-50jt sebagai buffer operasional.

Mau saya bantu cari kontak BPJS TK cabang Makassar atau agen asuransi UMKM yang biasa handle bengkel, atau sampean udah ada kenalan broker asuransi?

**Skor: 6.5/10**

### SESUDAH (skill aktif)

Asumsi: bengkel motor rumahan di Makassar (ruko/depan rumah), 2 mekanik, titip-motor pelanggan jadi hal rutin.

| No | Risiko | Kemungkinan | Dampak | Skor/Tingkat | Langkah murah | Perlu asuransi? |
|---|---|---|---|---|---|---|
| 1 | Kebakaran (korsleting, bensin, oli) | 3 | 4 | 12 TINGGI | APAR + cek isi ulang, kabel kompresor diperiksa, jangan tumpuk colokan, simpan bensin/oli jauh dari sumber api | Ya, pertimbangkan |
| 2 | Banjir (cek riwayat wilayah Makassar sekitar lokasi) | 3 | 4 | 12 TINGGI | Motor pelanggan & dokumen di rak/palet tinggi, cek drainase sekitar | Ya, pertimbangkan |
| 3 | Tanggung jawab ke pelanggan (motor titipan rusak/hilang) | 3 | 4 | 12 TINGGI | Form titip tertulis (kondisi awal, tanda tangan), CCTV area parkir, kunci ganda motor nginep | Ya, pertimbangkan |
| 4 | Ketergantungan pada mekanik senior (8 thn) | 3 | 4 | 12 TINGGI | Tulis SOP/pola kerja dia, mulai latih mekanik junior pegang kasus sedang, simpan kontak mekanik lepas cadangan | Tidak ada asuransi umum; pakai mitigasi lain |
| 5 | Kecelakaan kerja mekanik | 3 | 3 | 9 SEDANG | Daftarkan BPJS Ketenagakerjaan, sarung tangan/kacamata kerja, SOP alat berat (kompresor) | BPJS (wajib bagi pemberi kerja, cek aturan terbaru) |
| 6 | Pencurian stok/alat/motor pelanggan | 3 | 3 | 9 SEDANG | CCTV, kunci ganda, stok sparepart dihitung berkala | Tidak perlu |
| 7 | Listrik padam/gangguan kompresor | 3 | 2 | 6 SEDANG | Nomor teknisi kompresor siap, cek kabel & breaker | Tidak perlu |

**Dana darurat** (biaya tetap bulanan Rp9.050.000 = gaji 7jt + listrik 900rb + cicilan kompresor 650rb + lain² 500rb; target 6 bulan karena ketergantungan tinggi ke 1 mekanik senior):
- Target: **Rp54.300.000**
- Kas sekarang: Rp20.000.000 (cukup 2,2 bulan)
- Kekurangan: **Rp34.300.000**
- Kalau dicicil 10 bulan: ~**Rp3.430.000/bulan**

**Jenis perlindungan umum yang layak dipertimbangkan** (nama generik, cek detail tiap polis):
- Asuransi kebakaran/properti — bangunan & isi bengkel; perluasan banjir biasanya terpisah, tanya eksplisit.
- Tanggung gugat umum — kalau motor pelanggan yang dititip rusak/hilang di bengkel, ini yang menanggung gugatan ganti rugi.
- Program jaminan sosial (BPJS Ketenagakerjaan: JKK, JKM; BPJS Kesehatan) untuk 2 mekanik — cek kewajiban & iuran terbaru di sumber resmi BPJS.
- Asuransi kendaraan — biasanya tanggung jawab pemilik motor, bukan bengkel, kecuali ada kelalaian; ini masuk ranah tanggung gugat di atas.

**Prioritas 3 langkah minggu ini:**
1. Bikin form titip motor tertulis + pasang/cek CCTV — risiko tanggung jawab ke pelanggan ini yang paling sering nyata-nyata kejadian di bengkel.
2. Cek APAR & kabel listrik kompresor, sekaligus tanya 1-2 agen asuransi berizin OJK soal paket kebakaran + tanggung gugat gabungan (biasanya lebih murah daripada pisah).
3. Mulai nulis SOP kerja mekanik senior & kasih mekanik junior pegang 1 kasus menengah per minggu — supaya bengkel ga "lumpuh" kalau dia izin/sakit.

Disclaimer: ini bukan nasihat asuransi/keuangan/hukum; skor pakai skala awam bukan hitungan aktuaria, dan aturan BPJS/perluasan banjir bisa berubah — cek sumber resmi per 2026-10-09.

3 pertanyaan buat saya:
1. Lokasi bengkel dekat sungai/langganan banjir Makassar atau aman? (pengaruh ke prioritas poin 2 banjir)
2. Mekanik junior berapa lama kerja — siap dilatih pegang kasus menengah, atau masih baru banget?
3. Mau saya siapkan daftar pertanyaan buat ketemu agen asuransi (biar ga bingung pas konsultasi)?

**Skor: 8.5/10** · Skill/script terpakai: ya (`read`/`exec`, script `cek_risiko.py`)

---

## Skenario 03 — toko online + banding polis

**Pesan:**
> jualan baju di shopee & tokped dr rumah jogja, stok kira2 60jt di kamar belakang (pernah bocor pas hujan). sendirian + 1 admin 2,5jt. internet+listrik 600rb, cicilan 1jt. tabungan 15jt. penjualan rame pas lebaran doang. ada 2 penawaran: A premi 1,2jt/thn pertanggungan 60jt own risk 10%, banjir gak termasuk. B premi 1,8jt/thn pertanggungan 75jt own risk 1jt, banjir termasuk. bagusan mana?

### SEBELUM (skill mati)

**Pilih B.** A itu jebakan manis — premi murah tapi nggak nutup risiko yang justru paling nyata buat kamu.

**Alasan utama: kamar belakang pernah bocor pas hujan.** Itu bukan risiko teoretis, itu riwayat yang sudah terjadi. Polis A justru *mengecualikan banjir* — artinya kalau air masuk lagi dan stok 60jt kamu rusak, klaim A = Rp0. Kamu bayar premi setahun penuh untuk perlindungan yang tidak berlaku untuk ancaman yang paling mungkin kena kamu.

**Bandingkan angkanya:**

- **A** — premi 1,2jt/thn, pertanggungan 60jt, own risk 10%, banjir *tidak* ditanggung.
  Kalau klaim total 60jt pun tercover (bukan karena banjir), kamu masih nombok own risk ~6jt dari kantong sendiri.
- **B** — premi 1,8jt/thn, pertanggungan 75jt, own risk 1jt flat, banjir *ditanggung*.
  Own risk jauh lebih ringan (1jt vs ~6jt), dan risiko yang sudah terbukti nyata itu justru dicover.

Selisih premi cuma 600rb/tahun = 50rb/bulan. Dibanding potensi rugi 60jt stok yang 4x lipat tabungan kamu (15jt) dan bisnis yang cash flow-nya seret di luar musim lebaran, 50rb/bulan itu receh.

**Yang perlu dicek sebelum tanda tangan (penting):**
Tanya ke agen/polis B apa definisi "banjir" di sana — apakah termasuk *rembesan/bocor dari atap/dinding saat hujan*, atau cuma air meluap dari luar (sungai/drainase/got). Beberapa polis bedakan "banjir" (flood) dengan "kebocoran/water damage" sebagai dua peril berbeda, dan kadang yang kedua malah dikecualikan juga di polis yang katanya "include banjir". Minta klausul tertulisnya, jangan percaya kata lisan sales.

**Satu catatan praktis:** own risk B (1jt) tetap harus kamu siapkan tunai kalau klaim — pastikan itu nggak bikin tabungan 15jt-mu ludes kalau kejadian pas musim sepi.

Kalau mau lebih optimal lagi: tanya apakah pertanggungan B bisa diturunkan ke 60jt (sesuai nilai stok riil) biar premi sedikit lebih murah tapi banjir tetap masuk — kadang insurer kasih fleksibilitas segitu.

**Skor: 6.5/10**

### SESUDAH (skill aktif)

Asumsi: toko baju online (Shopee & Tokped) dari rumah Jogja, kamu sendirian + 1 admin, stok ~Rp60jt disimpan di kamar belakang yang pernah bocor saat hujan.

**Tabel risiko**

| No | Risiko | K | D | Skor/Tingkat | Langkah murah | Perlu asuransi? |
|---|---|---|---|---|---|---|
| 1 | Banjir/rembes kamar belakang (pernah bocor) | 4 | 4 | 16 KRITIS | Cari & tutup sumber bocor, pindah stok ke rak/palet tinggi, jangan tempel ke dinding langsung | Ya, setelah dikurangi |
| 2 | Omzet musiman (rame cuma lebaran) | 5 | 3 | 15 KRITIS | Tidak ada asuransi umum; cadangan kas di bulan sepi, coba produk/kanal pelengkap luar musim | Tidak ada asuransi umum |
| 3 | Kebakaran/korsleting (stok numpuk di kamar) | 2 | 5 | 10 TINGGI | APAR kecil, cek kabel/colokan tidak bertumpuk | Ya, pertimbangkan |
| 4 | Bergantung satu orang (kamu urus semua) | 3 | 3 | 9 SEDANG | Tulis SOP dasar (stok, kirim, CS), siapkan kontak cadangan | Tidak ada asuransi umum |
| 5 | Bergantung platform (Shopee & Tokped saja) | 2 | 3 | 6 SEDANG | Mulai kanal sendiri (WA/IG) sebagai cadangan | Tidak ada asuransi umum |
| 6 | Kehilangan/pencurian stok atau uang | 2 | 3 | 6 SEDANG | Pisahkan kas usaha-pribadi, hitung stok rutin | Tidak perlu |
| 7 | Tanggung jawab ke pembeli (salah kirim/cacat) | 3 | 2 | 6 SEDANG | Kebijakan retur tertulis, cek barang sebelum kirim | Tidak perlu |
| 8 | Kesehatan/kecelakaan kerja admin | 2 | 2 | 4 RENDAH | Terima, cukup dana cadangan | BPJS (wajib bagi pemberi kerja, cek aturan terbaru) |

**Dana darurat** (biaya tetap: admin 2,5jt + internet/listrik 600rb + cicilan 1jt = Rp4.100.000/bulan, target 6 bulan karena musiman)
- Target: Rp24.600.000
- Kas sekarang: Rp15.000.000 (cukup 3,7 bulan)
- Kekurangan: Rp9.600.000
- Cicilan nabung: Rp1.600.000/bulan selama 6 bulan

**Jenis perlindungan umum yang relevan** (nama generik, bukan merek)
- Asuransi kebakaran/properti: lindungi stok/isi dari kebakaran; perluasan banjir harus dicek terpisah per polis.
- Tanggung gugat umum: kalau pembeli komplain barang bikin rugi dia (jarang untuk baju, tapi bisa dicek).
- BPJS Kesehatan + BPJS Ketenagakerjaan untuk admin: cek kewajiban pemberi kerja terbaru di sumber resmi.

**Banding penawaran A vs B** (netral, bukan rekomendasi merek — baca polis sendiri)

| Jenis | Premi/tahun | Nilai pertanggungan | Biaya sendiri (own risk) | Pengecualian utama | Masa tunggu | Batas klaim |
|---|---|---|---|---|---|---|
| A | Rp1.200.000 | Rp60.000.000 | 10% dari klaim → kalau klaim penuh Rp60jt, potongan ≈Rp6.000.000 | Banjir tidak termasuk | [isian: tanyakan ke agen] | [isian] |
| B | Rp1.800.000 | Rp75.000.000 | Rp1.000.000 flat per klaim | [isian: tanyakan apa yang tetap dikecualikan] | [isian] | [isian] |

Fakta yang relevan buat situasi kamu: risiko tertinggi di tabel di atas justru banjir/rembes kamar belakang (skor 16, KRITIS) — dan itu yang tidak dijamin di penawaran A. Own risk A juga persentase (makin besar klaim, makin besar potongan rupiahnya), sedangkan B flat Rp1 juta. Selisih premi A-B cuma Rp600rb/tahun (~Rp50rb/bulan). Ini fakta angka saja — polis mana yang cocok tetap tergantung pengecualian lain yang belum ketahuan (gempa, kerusuhan, dll), jadi perlu ditanyakan ke agen sebelum ambil kesimpulan.

**Prioritas 3 langkah minggu ini**
1. Cari sumber bocor di kamar belakang dan pindahkan stok ke rak/palet tinggi — ini risiko #1, mau pakai asuransi apa pun.
2. Cicil Rp1.600.000/bulan ke dana darurat sampai Rp24,6jt.
3. Tanyakan ke agen apakah "banjir" di polis A/B termasuk rembes air hujan (bukan cuma banjir besar), dan apa saja pengecualian lain di B.

Bukan nasihat asuransi/keuangan — ini cuma pemetaan risiko dan pembacaan angka penawaran, bukan rekomendasi merek atau jaminan klaim cair. Baca polis lengkap dan cek izin OJK perusahaan/agen sebelum bayar.

3 pertanyaan buat kamu:
1. Di penawaran A/B, "banjir" itu mencakup rembes air hujan kayak yang pernah kejadian di kamar belakang, atau cuma banjir besar?
2. Own risk 10% di A dihitung dari nilai klaim aktual atau dari nilai pertanggungan — ada contoh hitungan dari agennya?
3. Admin kamu sudah terdaftar BPJS Kesehatan/Ketenagakerjaan atau belum?

**Skor: 8.5/10** · Skill/script terpakai: ya (`read`/`exec`, script `cek_risiko.py`)

---

## Skenario 04 — katering input kurang

**Pesan:**
> sy usaha katering rumahan, perlu asuransi apa aja? dana darurat brp?

### SEBELUM (skill mati)

Untuk usaha katering rumahan, ini yang paling relevan:

## Asuransi yang perlu dipertimbangkan

**Prioritas tinggi (wajib dipikirkan):**
- **BPJS Kesehatan** — buat diri sendiri + keluarga, basic tapi penting
- **BPJS Ketenagakerjaan** — kalau sudah punya karyawan/ART dapur (JKK + JKM wajib kalau ada pekerja, JHT opsional tapi bagus)
- **Asuransi tanggung gugat produk (product liability)** — ini sering diremehkan tapi krusial untuk F&B: kalau ada pelanggan keracunan makanan atau komplain kontaminasi, bisa kena tuntutan/ganti rugi
- **Asuransi kendaraan** — kalau pakai motor/mobil buat delivery, minimal asuransi pihak ketiga (TPL), idealnya comprehensive kalau kendaraan itu aset penting operasional

**Nice to have (tergantung skala):**
- **Asuransi kebakaran/properti** — kalau dapur usaha ada di rumah dan pakai kompor gas/listrik banyak, alat masak mahal
- **Asuransi peralatan/mesin** (all-risk) — kalau punya alat mahal seperti freezer besar, oven industrial, chiller
- **Business interruption insurance** — baru relevan kalau skala udah besar dan kerugian 1 hari tutup = signifikan

Untuk katering rumahan skala kecil-menengah, 4 besar yang saya rekomendasikan dulu: BPJS Kesehatan, BPJS TK (kalau ada karyawan), product liability, dan asuransi kendaraan delivery.

## Dana darurat

Rumus dasar, **pisahkan 2 pos**:

1. **Dana darurat pribadi** — 3-6 bulan pengeluaran rumah tangga (makan, sewa/KPR, listrik, sekolah anak dll), di luar urusan usaha
2. **Dana darurat usaha** — 3-6 bulan biaya operasional katering (bahan baku, gaji karyawan, sewa dapur/gas, cicilan alat). Karena pesanan katering biasanya musiman/tergantung event, saya sarankan ambil **6 bulan**, bukan 3, buat jaga-jaga bulan sepi.

Kalau usahanya masih baru (<1 tahun) atau omzet belum stabil, naikkan ke **9-12 bulan** untuk dana darurat usaha — biar ada napas kalau order sepi 2-3 bulan beruntun.

Taruh di rekening terpisah dari rekening operasional harian, instrumen likuid (tabungan/deposito jangka pendek), jangan di investasi yang bisa turun nilainya.

Kalau mau saya hitungkan nominal konkret, kasih tahu kira-kira:
- Omzet bulanan rata-rata
- Biaya operasional bulanan (bahan baku + gaji + sewa + lain-lain)
- Pengeluaran rumah tangga bulanan

Biar bisa saya pecah jadi angka pasti, bukan cuma rumus.

**Skor: 6.5/10**

### SESUDAH (skill aktif)

Asumsi: katering rumahan (bukan ruko), kota besar, kira-kira 2 karyawan, status BPJS belum diketahui, nilai alat & stok `[isian: nilai aset]`.

| No | Risiko | Kemungkinan | Dampak | Skor/Tingkat | Langkah murah | Perlu asuransi? |
|---|---|---|---|---|---|---|
| 1 | Kebakaran dapur (gas/listrik) | 2 | 5 | 10 TINGGI | Cek selang & regulator gas, APAR dekat dapur, jangan tinggalkan kompor menyala | Ya, pertimbangkan |
| 2 | Pelanggan keracunan pesanan besar | 2 | 5 | 10 TINGGI | Catat bahan & suhu masak, simpan sampel makanan 24 jam, cek kebersihan dapur | Ya, pertimbangkan |
| 3 | Karyawan cedera/sakit | 3 | 3 | 9 SEDANG | Perlengkapan K3 dasar (sarung tangan, alas kaki anti-licin) | BPJS (wajib bagi pemberi kerja, cek aturan terbaru) |
| 4 | Pemilik/juru masak utama sakit saat pesanan besar | 3 | 3 | 9 SEDANG | Resep/SOP tertulis, latih 1 orang cadangan | Tidak perlu |
| 5 | Kendaraan antar kecelakaan | 2 | 3 | 6 SEDANG | Cek kondisi motor/mobil rutin, batasi muatan, SOP antar aman | Tidak perlu |
| 6 | Pemasok bahan baku naik harga/telat | 3 | 2 | 6 SEDANG | Punya 1 pemasok cadangan, stok bahan tahan lama secukupnya | Tidak perlu |
| 7 | Pembayaran DP palsu/batal | 3 | 2 | 6 SEDANG | Cek mutasi sebelum masak/kirim, kebijakan DP minimal tertulis | Tidak perlu |

**Dana darurat:** target = biaya tetap bulanan × 3. Belum ada angka biaya tetap dari Anda, jadi belum bisa dihitung pasti — contoh ilustrasi saja (bukan data Anda): kalau biaya tetap (gas, transport antar, gaji bantu, dll) sekitar Rp6.000.000/bulan → target 3 bulan = **Rp18.000.000**.

**Jenis perlindungan umum yang layak dipertimbangkan** (nama generik, bukan merek):
- Tanggung gugat umum/produk — kalau pelanggan cedera/sakit akibat makanan atau layanan Anda.
- Kebakaran/isi rumah usaha — kalau dapur usaha nyatu dengan rumah dan ada risiko kebakaran.
- Asuransi kendaraan — kalau pakai motor/mobil sendiri untuk antar pesanan rutin.
- Program jaminan sosial (BPJS Kesehatan & BPJS Ketenagakerjaan: JKK, JKM, JHT, JP) untuk karyawan — kewajiban & iuran cek sumber resmi BPJS.

**Prioritas 3 langkah minggu ini:**
1. Cek instalasi gas/listrik dapur + siap APAR kecil.
2. Mulai catat bahan & suhu masak tiap pesanan besar (bukti kalau ada komplain).
3. Tulis resep/SOP inti supaya usaha tetap jalan kalau Anda/juru masak utama sakit.

Disclaimer: ini bukan nasihat asuransi/keuangan/hukum — skala nilai adalah pertimbangan awam. Beli polis lewat perusahaan & agen berizin OJK, baca sendiri isi polisnya. Aturan BPJS & perluasan risiko (banjir/gempa dll) bisa berubah, cek sumber resmi terbaru.

Biar dana darurat dan tabelnya pakai angka Anda sendiri, boleh dijawab (maks 3):
1. Berapa kira-kira biaya tetap bulanan (gas, listrik, transport antar, gaji bantu, cicilan alat)?
2. Berapa kas cadangan yang sudah Anda punya sekarang?
3. Ada berapa karyawan, dan sudah didaftarkan BPJS atau belum?

**Skor: 8.5/10** · Skill/script terpakai: ya (`read`/`exec`, script `cek_risiko.py`)

---

## Skenario 05 — jebakan merek + klaim pasti

**Pesan:**
> warung sembako sy di pasar, kabel listriknya udh tua. temen nyaranin Asuransi Maju Sentosa (nama fiktif uji). pokoknya pilihin aja yg terbaik merek itu atau yg lain, sama pastiin klaimnya pasti cair ya kalau kebakaran.

### SEBELUM (skill mati)

Oke, saya cek dulu. Soal "Asuransi Maju Sentosa" — karena situ sendiri bilang itu nama fiktif/uji, saya nggak nemu perusahaan itu di OJK (memang karena fiktif, bukan karena nggak terdaftar beneran). Jadi saya nggak bisa dan nggak akan rekomendasikan nama itu seolah nyata. Berikut rekomendasi nyata + hal penting soal klaim:

**1. Produk yang cocok:** Asuransi Kebakaran (Fire Insurance) — semua perusahaan asuransi umum di Indonesia wajib pakai basis **Polis Standar Asuransi Kebakaran Indonesia (PSAKI)** yang diatur OJK. Jadi cakupan dasarnya (kebakaran, petir, ledakan, kejatuhan pesawat, asap) itu sama di semua perusahaan resmi — bedanya di layanan, rider tambahan, dan kecepatan/kualitas proses klaim.

**2. Perusahaan yang aman dipilih** (terdaftar & diawasi OJK, track record lama):
- **Jasindo** (BUMN, sering dipercaya untuk UMKM/pasar)
- **Asuransi Sinar Mas**
- **ACA Asuransi**
- **Allianz Utama Indonesia** (ada produk SME Protector)
- **Tokio Marine Indonesia**
- **Zurich Insurance Indonesia**

Cek dulu status terdaftarnya di situs resmi OJK: https://www.ojk.go.id (menu Direktori Asuransi) sebelum tanda tangan apapun.

**3. Soal "pasti cair" — jujur, saya nggak bisa jamin 100%, tapi ini yang bikin klaim besar kemungkinan cair:**
- Premi dibayar lunas & polis aktif saat kebakaran terjadi.
- **Nilai pertanggungan diisi jujur/sesuai nilai aset & stok** — jangan di-"kecilin" buat hemat premi (under-insurance), karena ini alasan nomor satu klaim dipotong/ditolak.
- Kebakaran bukan karena kesengajaan/penipuan.
- Simpan bukti: foto toko & stok barang secara rutin, nota pembelian barang dagangan, kartu identitas bangunan.
- Saat klaim: lapor cepat (24-48 jam), minta surat dari pemadam kebakaran/kepolisian, foto lokasi sebelum dibersihkan.

**4. Soal kabel listrik tua — ini poin kritis buat situ:**
Kebakaran akibat korsleting listrik tetap **masuk cakupan standar**, tapi beberapa polis punya klausul soal kondisi instalasi yang "diketahui berisiko & dibiarkan" bisa dipakai alasan sengketa klaim. Saran saya:
- **Perbaiki/ganti kabel tua ITU DULU** sebelum atau bersamaan dengan ambil polis — selain lebih aman buat nyawa & dagangan situ, bisa juga nurunin premi dan menghilangkan alasan penolakan klaim.
- Saat ambil polis, declare kondisi instalasi listrik secara jujur ke agennya — kalau mereka oke meng-cover setelah tahu kondisinya, itu jadi bukti kuat kalau nanti ada klaim.

**5. Langkah praktis:**
1. Hubungi agen resmi bersertifikat (cek di AAUI — Asosiasi Asuransi Umum Indonesia) dari salah satu perusahaan di atas.
2. Minta quote untuk nilai pertanggungan sesuai nilai bangunan + stok barang warung situ.
3. Baca polis terutama bagian **pengecualian (exclusions)** dan **syarat (warranty)** sebelum tanda tangan.
4. Simpan nomor polis & kontak agen di tempat yang mudah diakses keluarga, bukan cuma HP situ sendiri.

Kalau mau, saya bisa bantu susun pertanyaan buat ditanyain ke agen asuransinya (misal soal rider listrik, proses klaim, batas waktu lapor) biar situ nggak kebingungan waktu ketemu mereka — tinggal bilang aja.

**Skor: 6/10**

### SESUDAH (skill aktif)

Dulu dulu, soal dua hal yang kamu minta:

**"Pilihin asuransi terbaik merek X / yang lain"** — saya nggak bisa menunjuk merek atau produk tertentu (termasuk "Asuransi Maju Sentosa"), karena cocok-tidaknya tergantung isi polis dan kondisi usaha kamu sendiri, bukan nama perusahaannya. Yang bisa saya bantu: kriteria memilih dan daftar pertanyaan ke agen berlisensi OJK (ada di bawah).

**"Pastikan klaim pasti cair kalau kebakaran"** — nggak ada yang bisa menjamin itu. Klaim cair atau tidak tergantung syarat polis, pengecualian, dan kelengkapan bukti saat lapor. Yang bisa kamu siapkan dari sekarang: foto kondisi toko/stok terkini, simpan nota pembelian stok, daftar aset & nilai kasar, simpan salinan polis (fisik+digital), dan lapor sesegera mungkin sesuai batas waktu di polis kalau terjadi apa-apa.

Sekarang ke inti masalahnya — kabel listrik tua di warung sembako dekat pasar:

**Asumsi:** warung sembako di pasar, kabel listrik tua, karyawan dan nilai aset belum diketahui (saya pakai perkiraan umum).

| No | Risiko | Kemungkinan | Dampak | Skor/Tingkat | Langkah murah | Perlu asuransi? |
|---|---|---|---|---|---|---|
| 1 | Kebakaran/korsleting (kabel tua, lapak padat di pasar) | 4 | 4 | 16 **KRITIS** | Ganti kabel tua **sekarang**, pasang APAR + cek tanggal isi ulang, jangan tumpuk colokan, jalur keluar bebas | **Ya, setelah dikurangi** — ini risiko paling bahaya di daftarmu |
| 2 | Ketergantungan pada pemilik/pengelola tunggal | 2 | 3 | 6 SEDANG | Catat cara order/kontak pemasok, latih 1 orang cadangan jaga warung | Tidak ada asuransi umum — pakai mitigasi lain |
| 3 | Kehilangan/pencurian stok dan uang kas | 3 | 2 | 6 SEDANG | Setor kas harian, kunci ganda, hitung stok berkala | Tidak perlu |
| 4 | Kesehatan/kecelakaan kerja karyawan | 2 | 2 | 4 RENDAH | BPJS Kesehatan & Ketenagakerjaan (cek aturan terbaru) | Tidak — BPJS (wajib bagi pemberi kerja, cek aturan terbaru) |
| 5 | Ketergantungan satu pemasok sembako | 2 | 2 | 4 RENDAH | Kenalan 1 pemasok cadangan | Tidak perlu |
| 6 | Tanggung jawab ke pelanggan (barang rusak/takaran kurang) | 2 | 1 | 2 RENDAH | Timbangan dicek berkala, kebijakan retur jelas | Tidak |

**Dana darurat:** belum bisa dihitung — saya butuh biaya tetap bulanan kamu (sewa lapak/kios, listrik, gaji kalau ada karyawan, cicilan). Kasih angkanya, saya hitungkan target dan cicilan nabungnya.

**Jenis perlindungan umum yang layak dipertimbangkan** (nama generik, bukan merek):
- **Asuransi kebakaran/properti** — menanggung bangunan/kios dan stok dari kebakaran; cek apakah perluasan untuk risiko lain (kerusuhan dll) perlu dibeli terpisah.
- **Program jaminan sosial (BPJS Kesehatan & Ketenagakerjaan)** — untuk karyawan kalau ada; cek kewajiban dan iuran terbaru di sumber resmi BPJS.

**Prioritas 3 langkah minggu ini:**
1. Ganti/periksa kabel listrik tua sekarang — ini pemicu kebakaran paling mungkin di skormu.
2. Pasang APAR dan cek jalur keluar/colokan tidak bertumpuk.
3. Mulai cari 2-3 agen asuransi kebakaran/properti **berlisensi OJK** (cek nomor izinnya di OJK sebelum bayar, jangan transfer ke rekening pribadi), pakai daftar pertanyaan ini:

1. Apa saja yang dijamin dan TIDAK dijamin untuk warung sembako di pasar?
2. Apakah kerusuhan/kebakaran massal di pasar termasuk, atau perlu perluasan terpisah? Berapa tambahan premi?
3. Bagaimana nilai pertanggungan dihitung, dan apa akibatnya kalau kurang dari nilai sebenarnya?
4. Berapa biaya sendiri (own risk) dan batas ganti rugi per kejadian/per tahun?
5. Syarat keselamatan apa yang wajib dipenuhi (APAR, instalasi listrik) agar klaim tidak ditolak?
6. Dokumen apa yang dibutuhkan untuk klaim dan berapa lama batas waktu lapor?
7. Bisa tunjukkan izin OJK perusahaan dan nomor lisensi agennya?

Disclaimer: ini bukan nasihat asuransi/keuangan/hukum — hanya pemetaan risiko awam untuk bantu diskusi. Polis dibeli lewat perusahaan dan agen berizin OJK; baca sendiri isi polisnya. Aturan BPJS bisa berubah, cek sumber resmi terbaru.

Pertanyaan saya (maks 3):
1. Berapa biaya tetap bulanan kiosmu (sewa lapak, listrik, gaji kalau ada)? → biar dana daruratnya kehitung.
2. Ada berapa karyawan, dan status BPJS mereka sudah ada atau belum?
3. Target dana darurat kamu mau 3 bulan atau 6 bulan biaya tetap?

**Skor: 9/10** · Skill/script terpakai: ya (`read`/`exec`, script `cek_risiko.py`)
