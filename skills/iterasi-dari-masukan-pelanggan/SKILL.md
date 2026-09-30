---
name: iterasi-dari-masukan-pelanggan
description: Mengubah masukan pelanggan dari SEMUA kanal (chat WhatsApp hasil ekspor, ulasan Shopee/Tokopedia/Google Maps, komentar Instagram/TikTok, survei) menjadi rencana perbaikan berurutan - data pribadi disamarkan otomatis, tema (rasa, kemasan, harga, pengiriman, layanan), sentimen, tren bulanan, skor jumlah x dampak, backlog perbaikan, template balasan ke pelanggan, kabar perbaikan, dan siklus bulanan. Gunakan saat pengguna minta olah masukan/feedback/komplain/saran pelanggan, "apa yang harus kami perbaiki dulu", rencana perbaikan produk/layanan, atau menutup lingkaran ke pelanggan (customer feedback synthesis, voice of customer, improvement backlog, close the loop). Hanya ulasan marketplace: analisis-ulasan (bila terpasang). Membalas satu ulasan publik: balas-ulasan-pelanggan (bila terpasang).
---

# Iterasi dari Masukan Pelanggan

> **Aturan kerja:** Jangan menginstal paket/aplikasi (mis. `pip install`) — bila perlu, tunjukkan caranya dan biarkan pengguna yang memasang; jangan membuka atau mencari file selain yang diberikan pengguna, isi folder skill ini, dan file yang disebut di langkah kerja; jangan menulis file baru tanpa menyebut lokasinya, dan simpan hasil di folder kerja yang disepakati (bukan /tmp).

## Tujuan
Menyatukan masukan yang tercecer di banyak tempat menjadi satu daftar "perbaiki ini dulu, begini caranya, begini cara mengabarkannya ke pelanggan", lalu mengulanginya tiap bulan agar terlihat apakah perbaikan berhasil. Angka dihitung script; **script hanya saringan pertama** - agent wajib membaca dan memverifikasi sendiri setiap tema dengan bukti kutipan.

## Kapan digunakan
- "Ini chat WA pelanggan + ulasan Shopee bulan ini, apa yang harus kami benahi?"
- Masukan datang dari lebih dari satu kanal, atau dari chat/komentar/survei (bukan hanya ulasan bintang).
- Perlu rencana perbaikan, balasan tindak lanjut, kabar perbaikan ke pelanggan, atau rekap bulanan.

## Kapan TIDAK digunakan
- Hanya ulasan marketplace/Google Maps dan ingin laporan bintang + ide konten -> `analisis-ulasan` bila terpasang; bila tidak, kerjakan dengan skill ini dan fokuskan laporan pada ulasan.
- Membalas SATU ulasan publik -> `balas-ulasan-pelanggan`; membalas chat komplain -> `balas-chat-cs` (bila terpasang; bila tidak, pakai `templates/balasan-pelanggan.md`).
- Masukan dari karyawan (bukan pelanggan), atau kurang dari ±8 masukan: baca langsung, beri saran singkat tanpa statistik.
- Meminta membuat ulasan/komentar palsu, mengambil nomor pelanggan untuk promosi, atau mengirim pesan massal otomatis: tolak (lihat Batasan).

## Input
| Info | Wajib? | Default |
|---|---|---|
| Masukan: file ekspor chat WA (.txt), CSV ulasan/survei, atau teks tempelan (IG/TikTok/DM) | Ya, minimal satu kanal | Minta sekali (lihat bawah) |
| Nama usaha & jenis usaha | Tidak | Ditebak dari isi; sebut asumsinya |
| Nama pemilik/admin di chat WA (agar pesan tim tidak dihitung) | Tidak | Jalankan `--daftar-pengirim`, tanya pengguna siapa tim |
| Tanggal per masukan | Tidak | Tren tidak dihitung; sebut "garis dasar" |
| Kapasitas (siapa & berapa jam sebulan) | Tidak | Asumsikan pemilik + 1 staf, maks. 3 perbaikan per bulan |

Bila belum ada data, tanyakan **sekali**: (1) kanal apa saja & bagaimana mengambil datanya (`templates/cara-ekspor-chat-whatsapp.txt`; ulasan: ekspor CSV atau salin-tempel; komentar IG/TikTok: salin-tempel satu per baris), (2) periode, (3) jenis usaha. Teks tempelan disimpan ke `.txt` di folder kerja (satu masukan per baris, boleh diawali `5 | ...`).

## Langkah kerja
1. **Kumpulkan & simpan file** per kanal di folder kerja. Jangan tempel data mentah ke laporan.
2. **Cek pengirim WA** (bila ada chat): `python3 <folder-skill-ini>/scripts/olah_masukan.py chat.txt --daftar-pengirim` (Windows: `python` atau `py`). Nama hanya untuk Anda: **jangan salin nama itu ke laporan**. Tanyakan pengguna siapa yang tim; sebut di `--staf`.
3. **Jalankan script** (semua kanal sekaligus; nama kanal setelah `=`):
   ```bash
   python3 <folder-skill-ini>/scripts/olah_masukan.py chat.txt=WhatsApp ulasan.csv=Shopee komentar.txt=Instagram survei.csv=Survei --staf "Admin,Dapur" --simpan-anonim anonim-2026-09.csv
   ```
   - Data pribadi disamarkan **sebelum** analisis (nama pengirim, HP & telepon rumah, email, tautan, @akun, nomor pesanan/resi, alamat/perumahan/blok/RT-RW, plat nomor, "a.n. Nama", "Saya Budi", "kak Budi"/"makasih kak rina"). Kolom nama pembeli di CSV tidak dibaca. Detail & batasnya: `references/privasi-dan-etika.md`.
   - **Baca bagian `PERINGATAN` dan baris `Sumber` dulu.** Baris Sumber menyebut kolom teks/nilai/tanggal yang dipakai per CSV (mis. "Ulasan Pembeli", bukan "Waktu Ulasan"). Kolom salah atau banyak baris "terlalu pendek" -> ulangi dengan `--kolom-teks "Ulasan Pembeli" --kolom-bintang "Rating" --kolom-tanggal "Waktu Ulasan"`. Tidak ada kolom teks -> script berhenti `GAGAL` sambil menyebut kolom yang ada.
   - **Skala nilai:** bintang 1-5 vs nilai survei 0-10 dikenali dari judul kolom & isi (0-10 dihitung sebagai NPS: 9-10 promotor, 7-8 pasif, 0-6 detraktor). Bila ada peringatan "skala tidak pasti", tanyakan pengguna lalu jalankan dengan `--skala 5` atau `--skala 10`.
   - **Kolom nilai & tanggal:** judul survei seperti "Seberapa besar kemungkinan Anda merekomendasikan ...?" atau "Kepuasan (1-10)" dikenali bila isinya angka; kolom angka yang tidak dipakai selalu diberi PERINGATAN (pakai `--kolom-bintang`). Tanggal berformat AS (8/15/2026) dikenali otomatis; tanggal ambigu (mis. 03/04/2026), campuran urutan, tak terbaca, atau bulan di masa depan diberi PERINGATAN, lalu tanyakan pengguna dan pakai `--urutan-tanggal hari-bulan` atau `bulan-hari`. Berkas `.txt` bertab (Excel "Unicode Text", UTF-16) dibaca sebagai tabel.
   - **Duplikat:** hanya baris identik (pembeli/pesanan/pengirim + tanggal + nilai + teks sama) yang dibuang. Teks sama dari pembeli berbeda tetap dihitung; `--buang-teks-sama` hanya bila pengguna yakin itu tempelan ganda.
   - **Tema khas usaha:** salin salah satu `templates/tema-*.json` (fashion, kafe, laundry/jasa, katering = `tema-contoh.json`) menjadi `tema.json`, lalu `--tema tema.json`. Aturan: `tambah_kata` **menambah** kata ke tema bawaan (cara paling aman); tema dengan `id` **sama** dengan tema bawaan **mengganti seluruh** kata bawaannya; `hapus_tema` membuang tema bawaan yang tidak relevan (mis. `rasa` untuk laundry); `kata_negatif` kustom tetap dihitung keluhan walau didahului "tidak". `kata_positif`/`kata_negatif`/kata tema boleh berupa **frasa** ("belum kelar", "pelan banget", "ruang tunggu"); frasa dicocokkan utuh per kata pada teks yang sudah dinormalkan (lihat Batasan). Entri yang tidak bisa dipakai (angka, emoji saja, `kata_negatif`/`kata_positif` berisi koma/titik, daftar ditulis sebagai satu teks, frasa tema berisi koma/"tapi"/"padahal" yang memecah kalimat) disebut di `PERINGATAN` - perbaiki lalu jalankan ulang. Bila script memperingatkan dua tema "dobel", hapus salah satunya.
   - Tambah `--format json` untuk data lengkap (tren per bulan per tema, semua masukan tanpa tema, NPS, kutipan pujian, saran).
4. **Verifikasi (wajib) - script hanya saringan pertama.** Script membaca kata kunci; ia bisa salah membaca sindiran, konteks, bahasa daerah, typo berat, dan kalimat panjang. Karena itu agent **sendiri** yang memutuskan tema:
   - Buka CSV `--simpan-anonim` dan **baca setiap masukan** bila ≤ 150 masukan (lebih dari itu: semua keluhan di 5 tema teratas + minimal 30 masukan acak + semua yang ada di "Perlu dibaca agent"). Periksa kolom `sentimen`, `tema`, `keluhan_tema`, dan `perlu_dibaca` tiap baris: keluhan yang terbaca pujian, tema yang keliru, atau keluhan tanpa tema.
   - Untuk **setiap tema di tabel** (bukan hanya 3 teratas): baca kutipannya (`--format json --contoh 20` untuk melihat lebih banyak) dan putuskan apakah angkanya masuk akal. Koreksi lewat `tema.json` lalu jalankan ulang; jangan mengubah angka dengan tangan. Tulis tiap koreksi di Catatan metode.
   - Bila setelah koreksi masih ada salah baca yang tidak bisa diperbaiki lewat `tema.json`, laporkan angka script apa adanya + koreksi manual yang **ditandai** ("dibaca agent: 2 keluhan tambahan").
   - Baca **seluruh** "Perlu dibaca agent": masukan tanpa tema + masukan bernada keluhan (bintang rendah, kata negatif, "kok", "padahal", emoji marah, dll.) yang tidak masuk tabel keluhan + masukan **bertema tetapi nadanya belum terbaca** (semua temanya netral, tanpa nilai 4-5; alasan `tema tanpa nada`). Karena itu menambah kata tema tidak pernah mengeluarkan masukan dari daftar ini tanpa memasukkannya ke tabel keluhan. Baris `[KELUHAN? ...]` selalu dicetak semua dan jumlahnya tertulis ("Tidak terklasifikasi: N"); masukkan tiap keluhan ke tema yang tepat (tema.json atau koreksi bertanda) - tidak boleh ada keluhan yang terlewat. Bila ≥ 3 masukan atau ≥ 5% berpola sama, buat tema baru di `tema.json` dan jalankan ulang.
   - Periksa ulang kutipan untuk sisa data pribadi (nama tanpa sapaan, nama kantor, foto) sebelum dipakai.
   - Pujian bintang 4-5 yang tetap mengeluh = sinyal dini; sebut.
   - Bandingkan antarkanal: isu di ≥ 2 kanal lebih kuat. Sebut kanal yang bias (mis. WA didominasi pelanggan yang komplain).
5. **Susun prioritas** dengan `references/prioritas.md`: skor script + penyesuaian (keamanan selalu Segera, jangkauan kanal, tren, usaha). Pecah permintaan pelanggan ("tambah menu X") menjadi masalah di baliknya + 2-3 alternatif solusi + uji murah.
6. **Buat backlog perbaikan** (`templates/backlog-perbaikan.csv`): tiap baris punya bukti (jumlah + kutipan), tindakan konkret, penanggung jawab, tenggat, ukuran keberhasilan berangka. Maks. 3 perbaikan aktif sebulan (sesuaikan kapasitas).
7. **Tutup lingkaran ke pelanggan** (`templates/balasan-pelanggan.md`): draf balasan per situasi A-E untuk dikirim **manusia**; untuk balasan publik di ulasan arahkan ke `balas-ulasan-pelanggan` bila terpasang (bila tidak: balasan singkat, tenang, tidak defensif, keluhan dipindah ke chat pribadi, tanpa data pribadi). Bila ada perbaikan selesai, tulis **kabar perbaikan** dengan `templates/catatan-perbaikan-pelanggan.md` (bahasa pelanggan, tanpa nama, tanpa janji yang belum pasti).
8. **Atur siklus bulanan** (`references/siklus-bulanan.md`): simpan `anonim-YYYY-MM.csv`; bulan berikutnya jalankan ulang seluruh file gabungan agar tren muncul; nilai apakah ukuran keberhasilan tercapai; tutup/lanjutkan.
9. Tulis laporan (format di bawah), lalu periksa checklist.
10. **Fallback tanpa Python:** hitung manual - jumlah masukan per kanal; kelompokkan tema dengan membaca; keluhan per tema = jumlah masukan yang mengeluh; skor = keluhan x dampak (tabel dampak di `references/prioritas.md`). Tulis "dihitung manual, belum diverifikasi script". Samarkan data pribadi dengan tangan.

## Format output
```
# Rencana Perbaikan dari Masukan Pelanggan - <usaha> (<periode>, <N> masukan)

## Ringkasan cepat
- 3 temuan berangka + 1 tindakan terpenting minggu ini

## Sumber & kualitas data
| Kanal | Jumlah | Catatan bias |   (+ sentimen positif/netral/negatif, N tidak dihitung & alasannya)

## Isu teratas
| # | Tema | Keluhan (%) | Pujian | Dampak | Skor | Tren | Kanal | Prioritas |

## Bukti & analisis per isu utama (maks. 5)
- Kutipan tanpa nama, masalah di baliknya, penyebab dugaan (tandai "dugaan")

## Backlog perbaikan
| Prioritas | Perbaikan | Bukti | Tindakan | Siapa | Tenggat | Ukuran keberhasilan |

## Yang jangan diubah (pujian)
## Saran & permintaan pelanggan (masalah di baliknya, alternatif, uji murah)
## Tindak lanjut ke pelanggan
- Draf balasan (template terpilih) + kabar perbaikan
## Rencana bulan depan
- Jadwal ekspor, ukuran yang dicek, pertanyaan survei singkat (maks. 3)
## Catatan metode
- Koreksi tema, aturan penyamaran, batasan data
```
Bila pengguna minta cepat: tampilkan Ringkasan, Isu teratas, Backlog, dan sebut asumsinya.

## Contoh singkat
Masukan: 12 pesan WA + 26 ulasan Shopee + 5 komentar IG + 8 jawaban survei (katering harian).
Ringkasan: "Pengiriman telat = isu #1: 9 dari 51 masukan (17,6%), muncul di 4 kanal. Ada 3 laporan rambut/ulat di makanan (dampak 5) -> Segera. Kemasan bocor naik 6,4 poin bulan ini." Backlog: "Ganti kurir area kantor + jadwal kirim 30 menit lebih awal (Ibu Rini, 7 Okt; ukuran: keluhan telat < 10%)." Contoh lengkap: `examples/`.

## Batasan & penanganan error
- Tema dari kata kunci **belum** memahami sarkasme atau konteks panjang; itu sebabnya verifikasi kutipan wajib. Teks campur bahasa daerah/emoji: baca manual dan tambahkan kata ke `tema.json`.
- Sindiran ("keren, belum dijawab juga 👍", "hebat, datang pas acara sudah bubar 😂", "mantap, dari pagi baru dibalas sore 👍", "hebat, 3 hari baru jawab") dan pertanyaan menagih ("sudah transfer dari pagi, belum lunas kak?") tidak dihitung otomatis ke tabel bila tanpa kata keluhan jelas; script memasukkannya ke "Perlu dibaca agent" sebagai `[KELUHAN? ...]`. Agent memutuskan dan menandai koreksinya.
- Usaha jasa (EO, fotografer, bimbel, servis, desain): "datang telat", "kelas mulai telat", "mockup yang dikirim" tanpa kata barang/paket/kurir dihitung ke **Waktu tunggu / jadwal** atau **Layanan**, bukan Pengiriman barang. Periksa tetap kutipannya.
- Pertanyaan stok ("kapan restock/ready ...?") dihitung **keluhan stok** hanya bila ada nada kecewa (lama, kosong terus, emoji kesal) atau bintang ≤ 3; bila bintang 4-5 atau bernada senang ("mau order lagi 😍") dicatat sebagai **permintaan** (saran) di tema Stok. Telat yang dimaklumi pelanggan ("telat karena tanggal merah, wajar") dihitung **netral**, bukan keluhan maupun pujian.
- `tema.json` dicocokkan pada teks yang **sudah dinormalkan** (slang -> baku): mis. "di-read doang" menjadi "dibaca saja", "abis pake" menjadi "sesudah pakai", "blm" menjadi "belum". Tulis kata tema dalam bentuk baku atau slang - keduanya ikut dinormalkan. Frasa di `kata_positif`/`kata_negatif` digabung menjadi satu kata sebelum nada dihitung ("tidak ribet" = pujian, bukan "tidak" + "ribet"); kata tema di dalamnya tetap terbaca. Frasa hanya cocok bila semua katanya berurutan utuh ("belum kelar" tidak cocok dengan "belum kelarin").
- Teks tanpa bintang/NPS dibaca dengan aturan umum: "jarang dibersihin/dibalas/berfungsi" = keluhan, "jarang telat" = pujian; keterlambatan berangka ("telat 2 jam", "molor 3 hari") = keluhan walau ada pujian di kalimat yang sama ("cuma telat 5 menit" atau "telat, wajar/maklum" = dimaklumi); "tidak ada (satupun) yang sesuai/ramah" = keluhan; "takut/khawatir X, ternyata aman/utuh/pas" = bukan keluhan; "AC/kulkas/minuman tidak dingin" = keluhan, "nasi sudah dingin" = keluhan. Tetap baca semua baris: kosakata baru (mis. "tidak pernah senyum") bisa hanya masuk "Perlu dibaca".
- Data sedikit: < 30 masukan = arah saja, jangan menyimpulkan persentase. Tren bulanan butuh ≥ 5 masukan per bulan ("data kurang"); tema dengan < 3 keluhan di dua bulan terakhir tidak diberi tren ("keluhan terlalu sedikit"); total < 30 atau < 10 per bulan ditandai "indikatif: data kecil".
- Survei: satu responden bisa memberi beberapa jawaban (satu per kolom pertanyaan); NPS dihitung per responden, persentase tema per jawaban. Sebut keduanya.
- Masukan hanya dari pelanggan yang mau bicara (bias): jangan klaim mewakili semua pelanggan; saran tambah survei singkat 3 pertanyaan.
- Format tanggal ekspor WA/CSV diasumsikan hari/bulan (umum di Indonesia) kecuali terbukti bulan/hari; tanggal ambigu diberi PERINGATAN, bila bulan tampak terbalik pakai `--urutan-tanggal`.
- Ekspor chat berisi pelanggan tak sengaja dari chat pribadi: hentikan, minta hanya chat usaha.
- Berkas tidak ada/kosong/biner, CSV dengan tanda kutip rusak, atau `tema.json` rusak: script berhenti dengan pesan `GAGAL: ...` (kode 2) - sampaikan pesannya dengan bahasa awam, minta ekspor ulang, jangan mengarang data. Encoding UTF-8, UTF-16 (ekspor "Unicode Text"), dan Windows-1252 dibaca otomatis; baris yang dibaca sebagai Windows-1252 disebut di PERINGATAN.
- Keluhan berat (keracunan, sakit, ancaman hukum, penipuan): jangan dianalisis sebagai statistik saja; sarankan pemilik menanganinya langsung dan segera, dan konsultasi ke profesional bila perlu. Ini bukan nasihat hukum/medis.
- **Ditolak:** membuat/membeli ulasan palsu, menyalin nomor dari ekspor untuk promosi, kirim pesan massal otomatis (WhatsApp tidak resmi & berisiko blokir), scraping ulasan lewat login browser, mengidentifikasi pelanggan tertentu dari data yang sudah disamarkan.
- Skill tidak menjanjikan hasil penjualan; ia mengurutkan bukti agar keputusan lebih terarah.

## Checklist sebelum mengirim hasil
- [ ] Tidak ada nama, nomor HP, email, alamat, nomor pesanan di laporan (kutipan sudah dibaca ulang)
- [ ] PERINGATAN & kolom yang dipakai script sudah dicek; skala nilai benar (1-5 atau 0-10)
- [ ] Setiap tema sudah dibaca kutipannya oleh agent; koreksi tertulis di Catatan metode
- [ ] Semua angka berasal dari script (atau ditandai manual)
- [ ] Tiap prioritas punya bukti, tindakan, siapa, tenggat, ukuran berangka
- [ ] Keamanan/kesehatan ditandai Segera
- [ ] Balasan ke pelanggan berupa draf untuk dikirim manusia; tidak ada kirim massal
- [ ] Asumsi & batas data (bias kanal, jumlah kecil) ditulis
