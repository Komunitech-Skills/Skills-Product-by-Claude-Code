---
name: strategi-merek-usaha
description: Membantu menamai usaha/produk (kriteria mudah diucap orang Indonesia, cek arti negatif di bahasa daerah/slang, 10 opsi dengan skor matriks lewat script, panduan cek domain .id/.com, handle IG/TikTok, dan pangkalan merek DJKI/PDKI beserta kelas Nice) lalu merumuskan penawaran (offer) yang menjual (nilai, bonus, garansi, kelangkaan jujur sesuai UU Perlindungan Konsumen, hitung laba per unit) dengan teks siap tempel untuk WhatsApp, Instagram, dan marketplace. Pakai saat pengguna bilang "kasih nama usaha", "nama produk apa ya", "bikin nama brand", "nama ini bagus nggak", "cara cek merek", "bikin penawaran", "promo biar laku", "bonus apa yang cocok", "garansi", "paket hemat", business naming, brand name ideas, offer design, value stack, bonus, guarantee, scarcity.
---

# Strategi Merek Usaha: Nama & Penawaran

> **Aturan kerja:** Jangan menginstal paket/aplikasi (mis. `pip install`) — bila perlu, tunjukkan caranya dan biarkan pengguna yang memasang; jangan membuka atau mencari file selain yang diberikan pengguna, isi folder skill ini, dan file yang disebut di langkah kerja; jangan menulis file baru tanpa menyebut lokasinya, dan simpan hasil di folder kerja yang disepakati (bukan /tmp).

## Tujuan
Dua hasil siap pakai: (A) **nama** usaha/produk yang mudah diucap, aman dari arti buruk, dan sudah lewat cek dasar; (B) **penawaran** yang jelas alasan belinya, hitungan labanya benar, dan kalimatnya jujur serta siap ditempel ke WA, IG, atau marketplace.

## Kapan digunakan
- "Bantu cari nama untuk usaha sambal/laundry/toko hijab saya." / "Nama produk baru ini enaknya apa?"
- "Nama ini bagus nggak? Ada yang mirip nggak?" / "Gimana cara cek nama sudah dipakai orang?"
- "Bikin penawaran yang bikin orang mau beli." / "Bonus dan garansi apa yang aman untuk saya?"
- "Promo saya nggak laku, penawarannya kurang apa?"

## Kapan TIDAK digunakan
- Menentukan target pasar dan positioning -> `positioning-persona-usaha` (kerjakan dulu bila belum jelas siapa pembelinya).
- Jadwal dan teks peluncuran -> `luncurkan-produk-baru`. Caption harian -> `konten-mingguan`. Halaman jualan panjang -> `copy-landing-page`.
- Harga jual dan HPP -> `hitung-hpp`, `harga-jual-marketplace` (skill ini hanya memakai angka yang diberikan).
- **Nasihat hukum merek** (boleh/tidak didaftarkan, sengketa, somasi, lisensi): tidak dijawab. Lihat Batasan.
- Logo, desain kemasan, dan jingle: di luar cakupan (boleh beri brief singkat).

## Input
| Info | Wajib? | Bila tidak diberikan |
|---|---|---|
| Produk/jasa, calon pembeli, kota/daerah | Ya | Tanyakan |
| Untuk A: gaya nama (kalem/gaul/daerah/Inggris), kata yang wajib/dihindari | Tidak | Asumsikan ramah, 2-3 suku kata, Indonesia; sebut asumsinya |
| Untuk A: **daftar merek/pesaing yang sudah kamu tahu** (5-10) | Tidak | Minta; tanpa daftar, kolom kemiripan dinilai 3 ("belum diperiksa") |
| Untuk B: harga jual, modal (HPP), potongan marketplace (%) | Ya untuk hitungan | Tanya; tanpa angka, beri rancangan tanpa hitungan dan tandai "belum dihitung" |
| Untuk B: bonus yang mungkin (biaya modal per unit), stok/kapasitas, batas waktu yang nyata | Tidak | Usulkan bonus murah dan tandai "isi angka asli" |

**Aturan tanya:** bila info wajib kurang, tanyakan **sekali** dalam satu pesan berisi daftar singkat (maks. 5 pertanyaan). Bila pengguna ingin cepat, langsung kerjakan dengan default yang masuk akal dan tulis asumsinya di bagian "Asumsi".

> **Lokasi script:** semua script skill ini ada di subfolder `scripts/` di folder yang sama dengan SKILL.md ini (folder skill). Jalankan dari sana; jangan mencari script atau file pengguna ke seluruh disk (mis. `find /`) — itu lambat dan menyentuh data pribadi di luar folder kerja.

## Bagian A: Penamaan

### A1. Pahami usahanya
Ringkas 3 baris: apa yang dijual, ke siapa, kesan yang diinginkan. Tanyakan kata yang sudah dipakai/disukai pemilik dan yang ingin dihindari. Kriteria lengkap: `references/kriteria-nama.md`.

### A2. Buat 10 opsi
- Campur pendekatan: deskriptif ("Sambal Cobek Rina"), berasal dari kata daerah/serapan, gabungan kata, akhiran/awalan (-ku, Kita, Nusa), dan satu opsi berani. Beri **satu kalimat alasan** per opsi.
- Hindari nama yang hanya menempel pada merek besar ("Indomilk Baru"), nama orang terkenal, nama lembaga/instansi, dan kata yang dilarang sebagai klaim (mis. "Halal", "BPOM", "Asli" tanpa dasar).
- Tulis opsi ke CSV memakai `templates/nama.csv` (kolom `nama`, `aman_makna`, `khas`, `relevan`). **Simpan CSV di folder kerja pengguna** (mis. `merek/nama-<usaha>.csv`), **jangan** di dalam folder skill, dan sebut lokasinya ke pengguna ("File kerja: …").

### A3. Periksa arti dan bunyi (manual, jangan mengarang)
- Untuk tiap nama tanyakan: adakah arti buruk/lucu di bahasa daerah (Jawa, Sunda, Batak, Minang, Bugis, Betawi, Madura, dan daerah pembeli), di slang/plesetan, atau saat disingkat/dibaca cepat? Bila kamu tidak yakin arti sebuah kata daerah, **jangan menebak**; tulis "perlu ditanyakan ke penutur asli" dan minta pengguna bertanya ke 3 orang dari daerah berbeda.
- **Bacakan nama seperti kata Inggris** (dan slang internet) yang mirip: ada arti buruk? (mis. "Sneakuy" terbaca "sneaky" = licik → `aman_makna` 1). Script juga menandai kemiripan dengan daftar kata Inggris berkonotasi buruk, tetapi daftar itu ringkas — tetap periksa sendiri.
- **Bandingkan bunyi dengan setiap pesaing yang disebut pengguna**, bukan hanya ejaannya ("Kicks Klin" dibaca sama dengan "Kick Clean" → terlalu mirip). Masukkan **semua** nama pesaing yang disebut pengguna ke `--merek`.
- Jangan mengklaim asal-usul atau arti slang/daerah tanpa sumber (mis. "akhiran -uy khas Medan"); bila tidak yakin, tulis "perlu ditanyakan ke penutur asli".
- Alasan ejaan dari script (mis. `3 konsonan berturut 'ncl' di 'Kinclong'`) disalin **persis** — jangan menebak sendiri huruf mana yang dimaksud.
- Uji ucap: bisa dieja lewat telepon/voice note tanpa salah? Sekali dengar bisa ditulis? Nilai 1-5 ke `aman_makna`, `khas`, `relevan` berikut alasan singkat. Penilaian = pendapat, bukan fakta; katakan begitu.

### A4. Skor lewat script
```
python3 scripts/skor_nama.py nama.csv --merek "Merek A, Merek B"      # Windows: python atau py
python3 scripts/skor_nama.py nama.csv --merek-file merek.txt --bobot "kemiripan=30,khas=10"
```
- Script menghitung panjang huruf, suku kata, kemudahan ejaan, **kemiripan ejaan dan bunyi kira-kira** (c/q/ck→k, ph/v→f, z→s, x→ks, ee/ea→i, oo→u, -s jamak dibuang, huruf ganda dirapatkan) dengan daftar merek **yang diberikan pengguna**, serta **kemiripan dengan kata Inggris umum berkonotasi buruk**; sisanya dari nilai manual. Skala 0-100. Bobot memakai titik untuk desimal.
- **Kata generik** (kopi, toko, warung, kedai, depot, bengkel, laundry, jaya, dst.; daftar lengkap di `scripts/skor_nama.py`) dibuang dari kedua sisi sebelum cek kemiripan, supaya merek "Kopi" tidak menandai semua nama berkata "kopi". Tambah kata umum lain dengan `--generik "sambal,nasi"`; matikan bawaan dengan `--tanpa-generik`. Bagian khas nama (mis. "Kenangan") tetap dibandingkan. Tetap: masukkan **merek utuh** pesaing ("Kopi Kenangan"), bukan kata umum saja. Nama tanpa huruf (mis. "2.5") ditolak.
- Nama berstatus **TANDAI** (terlalu mirip merek yang diberikan — ejaan atau bunyi —, mirip kata Inggris berkonotasi buruk, atau arti negatif) tidak boleh direkomendasikan; sebut alasannya ke pengguna. Selisih <= 5 poin = **SETARA**: putuskan lewat uji ucap 5 orang dan hasil cek ketersediaan.
- Bila script tidak bisa dijalankan, hitung manual: skor = jumlah(bobot x nilai 1-5) / jumlah bobot x 20 (bobot awal: panjang 10, suku kata 10, ejaan 10, kemiripan 20, aman makna 20, khas 15, relevan 15). Aturan skor tiap kriteria ada di `references/kriteria-nama.md`.
- Normalisasi bunyi hanya perkiraan dan script tidak tahu merek yang tidak disebutkan. Nama Inggris dan singkatan dihitung suku katanya kira-kira.

### A5. Cek ketersediaan (agent hanya MENYARANKAN)
Agent **tidak mengklaim** sebuah nama "tersedia" atau "aman". Beri daftar cek untuk 3 nama teratas, dan biarkan pengguna yang memeriksa:
1. **Domain**: .id (registrar resmi via pandi.id) dan .com; cari juga varian ejaan.
2. **Handle**: Instagram, TikTok, nama toko Shopee/Tokopedia/TikTok Shop, Google Maps, WhatsApp Business.
3. **Pencarian umum**: nama + kota/jenis usaha di Google dan marketplace. Adakah usaha sejenis dengan nama sama/mirip?
4. **Merek terdaftar**: langkah PDKI di `references/cek-merek-pdki.md`.
Tandai tiap butir "belum dicek" sampai pengguna melapor hasilnya.

### A6. Cek merek DJKI (praktis, tanpa opini hukum)
Ikuti `references/cek-merek-pdki.md` (baca tabel kelasnya, lalu **sebut nomor kelas Nice** di jawaban, mis. jasa cuci/perawatan sepatu = kelas 37, produk perawatan sepatu yang dijual = kelas 3 sebagai kelas terkait): buka pdki-indonesia.dgip.go.id, cari nama dan varian ejaan/bunyi, filter kelas Nice yang sesuai produk **dan kelas terkait**, catat temuan (nama, kelas, status) di tabel, lalu bawa ke konsultan kekayaan intelektual bila ada yang mirip atau bila akan mendaftar. Agent tidak menyimpulkan "boleh/tidak boleh".

### A7. Keluaran nama
Tabel 10 opsi + skor, 3 pilihan teratas dengan alasan, daftar cek per nama (status "belum dicek"), pertanyaan penutup: "Mau saya buatkan tagline dan bio dari nama pilihanmu?" (arahkan ke `positioning-persona-usaha` untuk tagline mendalam).

## Bagian B: Rumusan Penawaran

### B1. Nilai dulu, bukan diskon
Penawaran yang kuat menaikkan nilai di mata pembeli, tidak sekadar memotong harga. Cek 4 tuas (`references/rumus-penawaran.md`): hasil yang diinginkan pembeli, keyakinan bahwa berhasil (bukti/garansi), kecepatan hasil, dan kerepotan pembeli. Tanya: tuas mana yang paling lemah untuk produk ini? Perbaiki satu tuas dulu.

### B2. Susun 6 komponen
1. **Inti**: apa yang diterima, dengan angka/ukuran nyata (mis. "sambal 180 g, tahan 3 bulan tanpa kulkas" hanya bila benar).
2. **Bonus**: 1-3 bonus, masing-masing menjawab satu keberatan pembeli ("takut tidak tahu cara pakai" -> kartu resep), murah bagi kamu tetapi berguna bagi pembeli (kartu resep, stiker, konsultasi 10 menit, gratis kirim ulang bila rusak). Bonus harus nyata; jangan menaksir nilai bonus dengan angka karangan ("senilai Rp500.000") tanpa pembanding harga yang benar-benar dijual.
3. **Garansi**: pilih jenis yang sanggup kamu penuhi (ganti barang rusak/salah kirim, uang kembali dengan syarat jelas, coba dulu). Tulis syarat dan batas waktunya. Jangan menulis "100% garansi" tanpa syarat.
4. **Kelangkaan/batas waktu yang JUJUR**: hanya kapasitas produksi nyata, batch, stok nyata, atau tanggal berakhir yang benar-benar ditegakkan. Aturan lengkap dan larangan ada di `references/kata-dan-klaim.md`.
5. **Nama penawaran**: 3 opsi pendek (mis. "Paket Sarapan Pedas").
6. **Harga & cara bayar**: harga jelas, opsi COD/transfer/QRIS/paylater sesuai yang benar-benar tersedia.

### B3. Hitung labanya (wajib lewat script)
```
python3 scripts/hitung_penawaran.py --harga 38000 --hpp 17000 --platform 8 --diskon 0 \
  --bonus "Stiker=500;Kartu resep=800" --refund 2 --margin-minimal 25
```
Nominal boleh ditulis gaya Indonesia (`38000`, `38.000`, `Rp38.000`, `38rb`, `1,5jt`, `38.000,50`); persen boleh `7,5` atau `10%`. Bentuk ambigu seperti `38.5` atau `38,000` ditolak dengan pesan GAGAL: tanya pengguna, jangan ditebak. Harga/HPP di bawah Rp1.000 diberi PERINGATAN (mungkin maksudnya ribuan).
Keluaran: harga tayang, potongan platform, HPP, biaya bonus (biaya modal), perkiraan refund, **laba per unit**, margin, dan ruang biaya bonus maksimum. Rupiah dibulatkan ke rupiah terdekat. Bila **RUGI** atau margin di bawah target: kurangi bonus/diskon atau naikkan harga sebelum menulis materi. Bandingkan minimal dua versi (mis. diskon 15% vs bonus). Tanpa Python: rumus di `references/rumus-penawaran.md`. Potongan platform = angka dari pengguna (cek di pusat penjual masing-masing); jangan menebak.

### B4. Tulis materi siap tempel
Untuk kanal yang diminta (default: WA + IG + marketplace):
- **WhatsApp**: 1 pesan ke kontak yang sudah pernah berinteraksi/bersedia dihubungi (bukan blast ke nomor acak), maks. ±8 baris, ada ajakan membalas.
- **Instagram**: caption pendek + 3 alternatif kalimat pembuka.
- **Marketplace**: judul (jelas produk + ukuran + keunggulan nyata), 3 poin manfaat, kalimat garansi.
Semua angka, syarat garansi, tanggal berakhir, dan stok harus sama persis dengan hasil B3 dan fakta pengguna. **Klaim produk** — ukuran/isi (mis. "200 ml"), bahan, "asli", "alami", "tanpa pengawet", daya tahan, hasil pemakaian — hanya ditulis bila pengguna menyebutnya; selain itu `[isi: ukuran]`, `[isi: tanpa pengawet? ya/tidak]`, dst. Bagian lain yang belum diketahui juga ditulis `[isi: ...]`. Template: `templates/penawaran.md`.

### B5. Periksa kepatuhan sebelum tayang
Jalankan ceklis di `references/kata-dan-klaim.md`: klaim berlebihan, harga coret yang benar-benar pernah berlaku, batas waktu/stok nyata, hadiah/bonus benar-benar diberikan, tanpa testimoni karangan, produk teregulasi (pangan, kosmetik, obat, suplemen) mengikuti aturan BPOM/halal, tanda #iklan untuk endorse.

### B6. Uji kecil
Sarankan uji 7 hari: dua versi penawaran ke dua kelompok kecil, catat jumlah balasan dan pembeli. Pertahankan versi yang labanya lebih besar, bukan yang balasannya paling banyak.

## Format output
**Mode chat (Telegram/WhatsApp, termasuk lewat OpenClaw, atau pengguna awam yang minta cepat):** kirim ringkasan dulu (maks. ±25 baris, tanpa tabel lebar): 3 nama teratas + skor **atau** penawaran final + laba per unit, satu teks siap tempel, dan daftar "yang perlu kamu cek sendiri". Tutup dengan tawaran: "Mau versi lengkap? Balas: lengkap."

Mode lengkap:
```
# Strategi Merek — <nama usaha/produk>
## Ringkasan (nama pilihan, penawaran, laba per unit, langkah pertama)
## 1. Asumsi & fakta
## 2. Nama: 10 opsi, skor, 3 teratas, daftar cek (belum dicek)
## 3. Cek merek PDKI: langkah + tabel temuan (diisi pengguna)
## 4. Penawaran: 6 komponen + hitungan laba
## 5. Teks siap tempel (WA, IG, marketplace)
## 6. Ceklis kepatuhan & uji 7 hari
```
Selalu tutup dengan: asumsi, yang perlu dicek pengguna, dan disclaimer.

## Contoh singkat
Input: "Nama untuk sambal cobek rumahan Malang, harga Rp38.000, modal Rp17.000, jual di Shopee."
Keluaran ringkas: 10 nama + skor (mis. "Cabe Gendis 86/100, layak dicek"), daftar cek domain/handle/PDKI (belum dicek), penawaran "Paket Sarapan Pedas" (sambal + stiker + kartu resep; laba Rp15.900/unit, margin 41,8% dengan potongan platform 8% yang diberikan pengguna), teks WA siap tempel. Contoh nyata: `examples/`.

## Batasan & penanganan error
- **Bukan nasihat hukum atau merek.** Skill tidak menyatakan sebuah nama boleh didaftarkan, bebas dari sengketa, atau tidak melanggar merek pihak lain. Hasil PDKI dan keputusan pendaftaran ada di DJKI dan konsultan kekayaan intelektual. Pertanyaan hukum (mis. "aman dari gugatan?") dijawab dengan arahan ke konsultan KI.
- **Tidak mengklaim ketersediaan** domain, handle, atau merek. Semua berstatus "belum dicek" sampai pengguna melapor.
- **Tidak mengarang** testimoni, jumlah pembeli, penghargaan, sertifikat, stok, tanggal, maupun klaim produk (ukuran, bahan, "tanpa pengawet"). Pakai `[isi: ...]`.
- **File kerja** (CSV nama, draf penawaran) hanya ditulis ke folder kerja pengguna, tidak pernah ke folder skill; selalu sebut lokasinya.
- **Kelangkaan palsu ditolak:** stok "tinggal 3" padahal banyak, penghitung waktu yang diulang terus, harga coret yang tidak pernah berlaku, bonus/hadiah yang tidak diberikan. Tawarkan versi jujur. Dasar: **UU No. 8 Tahun 1999 tentang Perlindungan Konsumen**, Pasal 9, 10, 11, 12, 13 (untuk penjual) dan 17 (untuk pelaku usaha periklanan/agensi) (ringkasan per 2026-09-30, bukan kutipan resmi; baca teks lengkap di peraturan.go.id atau JDIH BPK).
- **Klaim berisiko** (kesehatan, "menyembuhkan", "pasti langsing", "termurah se-Indonesia", "BPOM/halal" tanpa nomor): ganti dengan versi yang bisa dibuktikan. Pangan/kosmetik/obat: arahkan cek aturan BPOM dan sertifikasi halal.
- **Bukan blast:** pesan WA hanya untuk kontak yang sudah berinteraksi/bersedia; skill tidak mengirim pesan sendiri.
- Input terlalu tipis ("bikin nama"): tanyakan sekali (5 pertanyaan) atau kerjakan versi cepat dengan asumsi.
- Nama yang diberikan pengguna sudah jelas milik merek terkenal: sarankan ganti, jangan dipoles.
- Script gagal/tak ada Python: hitung manual dengan rumus di A4/B3; pesan "GAGAL: ..." menjelaskan baris CSV yang salah.
