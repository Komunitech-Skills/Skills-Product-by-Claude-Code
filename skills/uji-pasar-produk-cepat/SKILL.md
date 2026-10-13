---
name: uji-pasar-produk-cepat
description: Menjalankan uji pasar murah dan terukur untuk produk/menu/jasa yang sudah lolos validasi awal - mendaftar asumsi paling berisiko, memilih eksperimen dari menu UMKM (pre-order WA, sistem PO, sampel/tester di bazar, landing page + link WA, listing marketplace uji, konten TikTok uji minat, survei Google Form), menetapkan kriteria sukses SEBELUM uji, aturan jumlah sampel, log eksperimen, lalu menghitung konversi, rentang wajar (Wilson), perbandingan dua varian (uji z, Fisher tepat untuk sampel kecil), jumlah orang per varian (power 80%) dan memutuskan LANJUT / UBAH / STOP plus opsi pivot. Gunakan saat pengguna mau menguji beberapa asumsi atau membandingkan dua varian (harga, kemasan, rasa, pesan iklan), atau sudah punya angka hasil uji dan butuh keputusan (run market test, experiment design, A/B test UMKM, pivot or persevere, pre-order test). Untuk MENGUBAH ide jadi hipotesis dan uji 7 hari pertama -> validasi-ide-produk-baru; untuk hitung HPP -> hitung-hpp; untuk strategi harga -> harga-jual-marketplace.
---

# Uji Pasar Produk Cepat

> **Aturan kerja:** Jangan menginstal paket/aplikasi (mis. `pip install`) — bila perlu, tunjukkan caranya dan biarkan pengguna yang memasang; jangan membuka atau mencari file selain yang diberikan pengguna, isi folder skill ini, dan file yang disebut di langkah kerja; jangan menulis file baru tanpa menyebut lokasinya, dan simpan hasil di folder kerja yang disepakati (bukan /tmp).

## Tujuan
Menjalankan **eksekusi** uji pasar setelah ide sudah punya hipotesis: memilih asumsi yang paling berbahaya, memilih eksperimen murah, menetapkan angka lulus **sebelum** uji, mencatat, menghitung hasil dengan benar, lalu memutuskan **LANJUT / UBAH / STOP** (dan kalau ubah, ubah ke arah mana).

Skill ini melengkapi `validasi-ide-produk-baru`. Pembagian tugas:
- `validasi-ide-produk-baru` = dari ide satu kalimat jadi hipotesis + satu uji 7 hari pertama.
- `uji-pasar-produk-cepat` (ini) = beberapa asumsi sekaligus, banyak varian, membandingkan dua pilihan, catatan eksperimen berulang, dan keputusan berbasis rentang wajar (bukan hanya persen mentah). Jangan mengulang penyusunan hipotesis dari nol; kalau pengguna belum punya, ringkas dulu dalam satu kalimat atau arahkan ke skill itu.

## Kapan digunakan
- "Produk frozen food varian baru saya mau dites dulu, mana yang harus dites duluan?"
- "Harga Rp35.000 vs Rp45.000, mana yang lebih laku? Ini datanya."
- "Dari 80 orang yang saya tawari, 14 pre-order. Lanjut produksi atau tidak?"
- "Hasil tes minggu lalu kurang bagus, ubah apa dulu?"
- "Bikin catatan eksperimen supaya tidak lupa apa yang sudah dicoba."

## Kapan TIDAK digunakan
- Belum ada ide konkret -> skill ini belum bisa dipakai (butuh satu produk/ide spesifik). Baru punya ide dan belum pernah diuji sama sekali -> mulai dari `validasi-ide-produk-baru`.
- Hanya butuh hitung modal/HPP/margin -> `hitung-hpp`; strategi harga listing -> `harga-jual-marketplace`.
- Riset pasar besar (survei ribuan responden, proyeksi multi-tahun) atau uji klinis/keamanan produk. Skill ini hanya uji minat beli skala UMKM.
- Produk terlarang atau menyesatkan (skema piramida/MLM, klaim obat tanpa izin edar BPOM, investasi tanpa izin OJK, produk ilegal) -> tolak dengan sopan.
- Uji yang menipu pembeli: menjual barang yang memang tidak akan dibuat, menagih uang tanpa niat mengirim. Lihat aturan kejujuran di bawah.

## Input
| Info | Wajib? | Default bila kosong |
|---|---|---|
| Apa yang diuji (produk/varian/harga) dan untuk siapa | Ya | - (tanyakan) |
| Harga rencana dan HPP per unit (kasar boleh) | Ya untuk keputusan margin | Tanpa HPP: keputusan hanya dari minat, tandai "margin belum dicek" |
| Kanal yang dimiliki (kontak WA, follower, toko marketplace, akses bazar, akun TikTok) | Ya | Tanyakan; menentukan menu eksperimen |
| Sudah ada data hasil uji? (jumlah ditawari, jumlah beraksi) | Tidak | Anggap belum: mulai dari Langkah 1 |
| Batas waktu dan modal uji maksimal | Tidak | 7-14 hari, modal uji sekecil mungkin |

Kalau info wajib kurang, tanyakan **sekali** dalam satu pesan berisi daftar pertanyaan bernomor. Kalau pengguna ingin cepat, pakai default dan sebutkan asumsinya di akhir jawaban.

## Langkah Kerja

> **Lokasi script:** semua script skill ini ada di subfolder `scripts/` di folder yang sama dengan SKILL.md ini (folder skill). Jalankan dari sana; jangan mencari script atau file pengguna ke seluruh disk (mis. `find /`) — itu lambat dan menyentuh data pribadi di luar folder kerja.

### 1. Daftar asumsi paling berisiko
Tulis 5-8 asumsi yang harus benar agar usaha berjalan, dikelompokkan (detail + contoh di [`references/asumsi-dan-kriteria.md`](references/asumsi-dan-kriteria.md)):
**Minat** (ada yang mau?), **Harga** (mau bayar segini?), **Ulang** (beli lagi?), **Jangkauan** (bisa menjangkau pembeli lewat kanal ini?), **Produksi/kirim** (bisa dibuat & dikirim tanpa rusak/basi, terutama frozen/chilled?), **Untung** (margin masih ada setelah ongkir, kemasan, biaya platform?), **Izin/kepatuhan** (PIRT/BPOM/halal bila perlu).

Beri tiap asumsi dua nilai 1-5: **Dampak** kalau salah, dan **Ketidakpastian** (seberapa sedikit bukti yang ada). Skor prioritas = Dampak x Ketidakpastian. Uji dulu yang skornya tertinggi, **maksimal 1-2 asumsi per putaran**. Asumsi berdampak tinggi tapi sudah pasti benar tidak perlu diuji; asumsi tidak penting tidak perlu diuji.

### 2. Pilih eksperimen dari menu UMKM
Cocokkan asumsi dengan eksperimen dan kanal yang dimiliki. Ringkas (rinci, dengan cara jalan dan jebakan: [`references/menu-eksperimen-umkm.md`](references/menu-eksperimen-umkm.md)):

| Eksperimen | Menguji | Butuh | Sinyal terkuat (aksi nyata) |
|---|---|---|---|
| Pre-order via WA | Minat + harga | >= 30 kontak relevan | Transfer DP / konfirmasi bayar |
| Sistem PO (produksi setelah pesanan terkumpul) | Minat + harga + ulang | Kontak/toko | Pesanan terbayar sampai tenggat |
| Sampel/tester di bazar | Rasa + harga + ulang | Akses bazar/titip | Beli setelah coba, minta kontak untuk pesan lagi |
| Landing page + link WA | Minat + pesan iklan | Halaman sederhana + sedikit trafik | Klik lalu chat WA berisi pesan bawaan |
| Listing marketplace uji | Minat + harga + judul/foto | Toko marketplace | Pesanan masuk, bukan hanya dilihat/difavoritkan |
| Konten TikTok uji minat | Minat awal + sudut promosi | Akun (boleh baru) | Komentar "beli di mana" / klik ke WA. Tayangan saja bukan bukti |
| Survei Google Form | Alasan, preferensi, rentang harga | Daftar responden | Hanya pelengkap: opini, bukan bukti beli |

**Aturan emas: aksi lebih kuat dari kata.** Urutan kekuatan bukti: bayar > pesan/DP > daftar tunggu > klik > komentar/like > "kayaknya mau" di survei. Untuk asumsi berisiko tinggi, pilih eksperimen berbukti bayar.

**Aturan kejujuran:** pembeli uji harus bisa dilayani. Pre-order hanya untuk produk yang benar-benar akan dibuat bila target tercapai; sebutkan jelas tanggal kirim dan bahwa uang dikembalikan penuh bila produk batal dibuat. Jangan gunakan foto orang lain, testimoni palsu, atau stok/harga palsu. Tanpa klaim kesehatan yang tidak berizin.

### 3. Tetapkan kriteria SEBELUM uji (wajib)
Tulis ke pengguna, dan minta disimpan sebelum uji dimulai (angka tidak boleh digeser sesudah hasil keluar):
1. **Ukuran sukses tunggal** (mis. jumlah pre-order terbayar ÷ jumlah orang yang ditawari).
2. **Ambang lanjut** (T): batas persen agar LANJUT. **Ambang stop** (S): di bawah ini STOP. Antara S dan T = UBAH. Default kalau pengguna tidak punya patokan: T = 15%, S = T ÷ 2, dan sebutkan bahwa ini heuristik praktis, bukan angka baku. Untuk survei/klik/komentar ambangnya jauh lebih longgar karena buktinya lebih lemah; untuk bayar sungguhan, 5-15% dari kontak hangat sudah bagus.
3. **Jumlah sampel** dan **batas waktu** (aturan praktis di bawah).
4. **Ambang margin**: bila HPP diketahui, harga harus menyisakan margin yang pengguna anggap layak. Minta hitung dengan `hitung-hpp` bila belum ada.
5. **Apa yang dilakukan** untuk tiap hasil (lanjut = batch produksi berapa; ubah = variabel apa; stop = apa).

**Aturan praktis jumlah sampel** (kasar, tujuannya menghindari keputusan dari angka kebetulan):
- Di bawah 30 orang ditawari: hanya sinyal arah, jangan pakai untuk modal besar.
- 30-100 orang: cukup untuk memisahkan "jelas laku" dari "jelas tidak", dengan rentang wajar lebar (sekitar +-10 poin persen).
- Eksperimen berkonversi rendah (landing page, listing marketplace, TikTok: ambang 1-5%): pakai margin sekitar **separuh ambang** (mis. ambang 5% -> `--margin 2,5`), bukan +-10.
- Bandingkan dua varian: di bawah 50 orang **per varian** hasilnya hanya sinyal arah. Jumlah yang dibutuhkan agar selisih bisa terdeteksi (power 80%, alfa 5%, dihitung script `sampel --banding`), **per varian**: 10% vs 20% = 199; 15% vs 25% = 250; 10% vs 15% = 686; 20% vs 25% = 1.094. Selisih 5 poin hampir selalu di luar jangkauan UMKM: uji perbedaan yang lebih besar atau terima "belum ada pemenang".
- Kelompok yang dibandingkan harus setara: kanal, hari, dan jenis orang yang sama; ubah **satu hal saja** antara varian.
- Tidak punya sampel sebanyak itu? Jalankan berulang kali (beberapa minggu) atau uji dua-tiga pilihan besar saja, bukan puluhan varian.
- Hitung tepatnya: satu uji `python3 scripts/hasil_eksperimen.py sampel --margin 5 --perkiraan 20`; dua varian `python3 scripts/hasil_eksperimen.py sampel --banding --a 15 --b 25`. Script memperingatkan bila margin >= perkiraan atau hasilnya < 30 orang.

### 4. Jalankan dan catat di log eksperimen
Beri pengguna pesan/materi siap pakai (draf pesan, caption, deskripsi listing, pertanyaan Google Form) sesuai eksperimen. Pakai [`templates/log-eksperimen.md`](templates/log-eksperimen.md): satu baris per eksperimen berisi tanggal, asumsi, eksperimen, kanal, kriteria, hasil, keputusan, pelajaran. Catat juga **alasan orang tidak membeli** (tanya 3-5 orang yang menolak, satu pertanyaan saja: "Yang bikin ragu apa?") karena ini bahan terbaik untuk ubah/pivot.

Selama uji: jangan menawar target, jangan menambah atau menghapus orang dari hitungan seenaknya, jangan mengubah tawaran di tengah jalan (kecuali fatal; kalau begitu mulai hitung ulang).

### 5. Hitung hasil dengan script (jangan dikira-kira)
Jalankan (Windows: `python` atau `py`; script hanya memakai Python standar):

```
python3 scripts/hasil_eksperimen.py hasil --ditawari 80 --aksi 14 --target 15
python3 scripts/hasil_eksperimen.py hasil --ditawari 12 --aksi 5 --bayar 0 --target 15   # 5 bilang mau, 0 transfer
python3 scripts/hasil_eksperimen.py banding --a-ditawari 60 --a-aksi 9 --b-ditawari 60 --b-aksi 15
python3 scripts/hasil_eksperimen.py sampel --margin 5 --perkiraan 20
python3 scripts/hasil_eksperimen.py sampel --banding --a 15 --b 25
```

**Bedakan "bilang mau" dari bayar:** `--aksi` = yang beraksi nyata (bayar/DP/transfer/pesan berbayar). Bila pengguna hanya melapor "mau" atau "minat", isi `--bayar` dengan jumlah yang benar-benar sudah bayar (0 bila belum ada). Minat lisan **bukan konversi**; jangan pernah memakainya sebagai dasar LANJUT.

Script mengeluarkan konversi, **rentang wajar 95% (Wilson)**, peringatan sampel kecil, dan keputusan sesuai ambang. Untuk dua varian, script memakai uji z dua proporsi, dan otomatis beralih ke **uji Fisher tepat** bila sampel kecil (< 50 per varian atau ada sel harapan < 5). Pada sampel kecil script **tidak pernah** menyatakan pemenang pasti; paling jauh "ada tanda ... tapi sampel terlalu kecil untuk yakin". Bacakan hasilnya ke pengguna dengan bahasa awam ("dengan data ini, angka sebenarnya kemungkinan besar ada di antara 11% dan 27%"; "selisih sebesar ini jarang muncul hanya karena kebetulan"), jangan sekadar menempel angka. Jangan menyebut p-value sebagai "peluang benar" atau "yakin 95% varian B lebih baik".

Kalau script tidak bisa dijalankan, hitung manual: konversi = aksi ÷ ditawari x 100%; bandingkan dengan T dan S; sebutkan bahwa rentang wajar tidak dihitung dan tandai hasil "perkiraan". Jangan mengarang rentang.

Kalau script menolak input (mis. aksi > ditawari, jumlah nol, bukan angka), jelaskan masalahnya, minta pengguna cek catatan, jangan menebak angka.

### 6. Putuskan: LANJUT / UBAH / STOP
| Hasil | Keputusan | Tindakan |
|---|---|---|
| **Komitmen nyata (bayar/DP/transfer) = 0**, berapa pun yang bilang "mau" | **BELUM ADA KOMITMEN: ULANGI UJI** (tidak boleh LANJUT) | Minta DP/pre-order berbayar kecil dari yang bilang mau; jangan keluarkan modal produksi |
| Sampel < 30 orang (berapa pun konversinya) | **ULANGI UJI dengan sampel lebih besar** (tidak boleh LANJUT) | Tawari minimal 30 kontak baru; paling banyak siapkan sebesar pesanan yang sudah dibayar |
| Konversi >= T, batas bawah rentang >= T, dan sampel >= 30 | **LANJUT** (kuat) | Produksi batch pertama; jadwalkan uji ulang saat skala naik |
| Konversi >= T tapi batas bawah < T, sampel >= 30 | **LANJUT BERTAHAP** | Batch kecil atau tambah sampel dulu; jangan modal besar |
| S <= konversi < T | **UBAH** | Ubah **satu** variabel (Langkah 7) dan uji ulang, maksimal 2 putaran ubah |
| Konversi < S | **STOP** | Berhenti atau pivot; jangan tambah modal. Jika batas atas rentang masih >= T dan sampel kecil, boleh satu uji ulang murah |
| Dua varian, selisih meyakinkan (p < 0,05, sampel >= 50 per varian) | Pilih pemenang | Pemenang jadi acuan uji berikutnya |
| Dua varian, p < 0,05 tapi sampel kecil | Pemenang sementara | Uji ulang dengan jumlah dari `sampel --banding` sebelum modal besar |
| Dua varian, tidak meyakinkan | Belum ada pemenang | Pilih yang lebih murah/mudah, atau uji ulang lebih besar |

**Terjemahkan ke jumlah orang yang perlu ditawari (wajib saat LANJUT/LANJUT BERTAHAP):** target pembeli (mis. unit/pesanan yang ingin terjual) ÷ konversi = orang yang perlu ditawari. Hitung dua kali: dengan konversi hasil uji (perkiraan tengah) dan dengan **batas bawah** rentang (skenario hati-hati). Contoh: ingin 60 pembeli, konversi 17,5%, batas bawah 10,7% -> 60 ÷ 0,175 = 343 orang (tengah) dan 60 ÷ 0,107 = 561 orang (hati-hati). Kalau kontak yang dimiliki kurang dari itu, kecilkan batch atau tambah kanal. Bulatkan ke atas.

**Urutan wajib: cek margin DULU, baru menyimpulkan.** Sebelum margin/HPP diketahui, dilarang menulis "tidak ada downside", "pasti aman", "tanpa risiko", atau "pasti untung", termasuk saat memilih pemenang dua varian (harga lebih tinggi bisa saja menurunkan margin pasar, harga lebih rendah bisa menggerus untung). Tulis: "pemenang dari sisi minat; margin belum dicek", lalu hitung margin (`hitung-hpp`) atau minta HPP. Sebelum LANJUT, cek juga margin dan **asumsi lain yang belum diuji** (ulang beli, ongkir/pendinginan, izin). LANJUT pada satu asumsi belum berarti semuanya aman: sebutkan asumsi berisiko berikutnya untuk putaran uji selanjutnya.

### 7. Kalau UBAH atau STOP: opsi pivot
Diagnosis dulu dari alasan penolakan, lalu pilih **satu** arah (detail di [`references/asumsi-dan-kriteria.md`](references/asumsi-dan-kriteria.md)):
- **Pivot pembeli:** produk sama, calon pembeli lain (mis. dari ibu rumah tangga ke kantin/kafe/reseller).
- **Pivot masalah:** produk sama, dijual sebagai solusi masalah lain (mis. bekal anak jadi stok praktis anak kos).
- **Pivot penawaran:** ubah kemasan/ukuran/paket/harga (paket hemat, porsi kecil coba-coba, langganan mingguan).
- **Pivot kanal:** ganti kanal (WA -> marketplace, bazar -> titip kantin, reseller).
- **Pivot produk:** ganti isi (rasa/varian lain) sambil mempertahankan pembeli dan kanal yang sudah bereaksi baik.
- **Stop bersih:** catat pelajaran, hentikan dengan hormat (kembalikan DP), dan mulai ide berikutnya. Kalah murah lebih baik daripada menang mahal.

## Format Output
Susun jawaban ringkas berurutan sesuai tahap yang relevan (jangan memaksakan semua tahap bila pengguna hanya membawa data hasil):
1. **Asumsi & prioritas** (tabel: asumsi, dampak, ketidakpastian, skor, diuji/ditunda)
2. **Rencana eksperimen** (eksperimen, kanal, jumlah sampel, tenggat, siapa melakukan apa)
3. **Kriteria yang dikunci** (ukuran, T, S, sampel, tindakan per hasil)
4. **Materi siap pakai** (pesan/caption/listing/form)
5. **Hasil & keputusan** (keluaran script + penjelasan awam + LANJUT/UBAH/STOP)
6. **Baris log eksperimen** siap salin dan **langkah berikutnya** (satu kalimat)
Sebutkan asumsi yang dipakai di akhir.

## Contoh singkat
Pengguna: "Saya jualan dimsum beku, mau tes varian mentai. Sudah kirim penawaran ke 80 kontak WA, 14 pre-order bayar DP. Target awal saya 15%."
-> Jalankan `hasil --ditawari 80 --aksi 14 --target 15`: konversi 17,5%, rentang wajar 10,7%-27,3%, keputusan **LANJUT BERTAHAP** (batas bawah di bawah target). Sarankan batch kecil, uji ulang ke 60 kontak baru, dan uji asumsi berikutnya (kualitas setelah pengiriman beku). Contoh lengkap ada di [`examples/`](examples/).

## Batasan & Penanganan Error
- Ini uji minat skala UMKM, **bukan bukti ilmiah**. Rentang wajar mengasumsikan orang yang ditawari dipilih kurang lebih acak; kontak yang sangat akrab (keluarga, teman dekat) membuat hasil terlalu optimis: pisahkan atau turunkan bobotnya.
- Pre-order yang dibayar sahabat karena sungkan bukan bukti pasar. Cari sinyal dari orang yang tidak kenal dekat.
- Data kurang (tidak tahu berapa yang ditawari): tanyakan; jangan menebak. Bila tidak bisa dipastikan, hitung hanya dari yang benar-benar tercatat dan tandai hasil sebagai batas atas.
- Aksi > ditawari, jumlah negatif/nol, atau bukan angka: tolak dengan pesan jelas dan minta pengguna cek catatan.
- Uji yang melibatkan uang pembeli: ingatkan kejujuran, tenggat, dan pengembalian dana. Ini bukan nasihat hukum, dan bukan pengganti izin usaha (PIRT/BPOM/halal) untuk produk yang memerlukannya.
- Untuk pembeli dari luar kontak sendiri (iklan berbayar) hasil bisa berbeda jauh; sebut ini sebelum modal iklan besar.
- Skill ini tidak menjamin produk laku; hanya mengurangi risiko keputusan dari perasaan.
