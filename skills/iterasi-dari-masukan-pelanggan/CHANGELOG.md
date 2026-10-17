# Riwayat perubahan — iterasi-dari-masukan-pelanggan

Catatan teknis per versi.

## Catatan revisi 1.0.14 (2026-10-17)
- Hanya dokumen, logika script tidak berubah (konstanta `VERSI` dinaikkan). "Contoh singkat" di SKILL.md masih memakai angka lama (51 masukan, Pengiriman 9 = 17,6%, Kemasan naik 6,4 poin, pelaksana "Ibu Rini"); kini disamakan dengan keluaran script pada data contoh dan `examples/01`-`02`: 52 masukan (WhatsApp 13), Pengiriman 10 = 19,2% di 4 kanal, Kemasan 6 keluhan = 11,5% dan naik 6,0 poin, backlog pengiriman "Pak Andi, 7 Okt".
- `examples/03-bulan-kedua-tren.md`: catatan yang menyebut angka September lama (23,5% dan 11,8%) sebagai "keluaran v1.0.1" dikoreksi. Angka itu ilustrasi tulisan tangan, bukan keluaran script; script v1.0.1 pada data yang sama menghasilkan Pengiriman 6 dari 34 = 17,6% dan Kemasan 5 dari 34 = 14,7%. Kolom Sept sekarang (20,0% dan 14,3%) dicek ulang dengan script v1.0.13.
- README: cuplikan uji OpenClaw diberi keterangan bahwa datanya (toko kue "Kue Nara", 31 masukan) berbeda dari data contoh katering (52 masukan).

## Catatan revisi 1.0.13 (2026-10-16)
- Perbaikan dari temuan penguji independen (Akun A): permintaan menu atau paket produk ("boleh tambah menu vegetarian? semoga ada paket tanpa daging", "semoga ada paket hemat untuk kantor") ikut dihitung sebagai saran **Pengiriman**. Penyebabnya bukan kata "kirim" atau "antar", melainkan kata "paket": script mengira semua "paket" adalah barang kiriman. Kata "instan" ("mie instan") punya masalah yang sama.
- Sekarang kata lemah itu hanya dihitung Pengiriman bila memang berarti barang kiriman. Bila konteksnya produk/menu ("paket hemat", "paket nasi box", "paket tanpa daging", "ada/tambah/bikin paket ...", "mie instan"), Pengiriman dilepas. Permintaan paket ikut tema **Varian / menu / pilihan** (saran), jadi tidak hilang dari laporan. Contoh: "semoga ada paket hemat untuk kantor" kini masuk Harga + Varian/menu.
- Tidak berubah: kata kuat tetap menang. "paketnya penyok", "paket belum sampai", "paket kantor telat 2 jam", "kurir antar paketnya telat", "bisa kirim ke luar kota?" tetap Pengiriman. Kata "kirim" dan "antar" sengaja tidak diubah karena memang menandakan pengiriman.
- Dampak pada data contoh: saran Pengiriman 2 menjadi 0, saran Varian / menu 3 menjadi 4, keluhan Pengiriman tetap 10 (19,2%). Hasil contoh lama di folder `examples/` ditulis sebelum perbaikan ini (lihat catatan di `examples/HASIL-UJI.md`).
- Uji baru di `scripts/uji_olah_masukan.py` (kelas `UjiPaketProdukBukanPengiriman`): kasus menu/paket, kasus regresi keluhan Pengiriman, dan hitungan pada data contoh.

## Catatan revisi 1.0.12 (2026-10-16)
- Perbaikan dari uji di bot Telegram asli (gelombang 18): baris ekspor WhatsApp tanpa tanggal yang isinya hanya teks sistem ("Pesan ini dihapus", "Pesan dihapus", "This message was deleted", "You deleted this message") tidak lagi digabung ke pesan di atasnya. Sebelumnya pesan pelanggan di atasnya ikut terbuang, sehingga satu keluhan hilang dan angka rekap meleset (data uji: 38 masukan, 12 pesan WhatsApp, 4 dari 6 keluhan tanpa balasan; yang benar 39, 13, 5 dari 7, dan keluhan pengiriman 8 = 20,5%).
- Teks sistem hanya dibuang bila SELURUH isi pesan adalah teks sistem. Pesan pelanggan yang kebetulan memuat kata seperti "pesan ini dihapus" atau "telah ditambahkan" di tengah kalimat tidak lagi ikut terbuang. Baris sistem bertanggal ("Budi: Pesan ini dihapus") dan pemberitahuan enkripsi tetap dibuang seperti dulu.
- Baris sistem yang disisipkan di antara pesan pelanggan dan balasan admin tidak lagi memutus hitungan "dibalas atau belum".
- Data contoh `examples/data/chat-wa.txt` memuat baris yang sama, jadi rekapnya ikut berubah: 52 masukan (sebelumnya 51), keluhan pengiriman 10 (sebelumnya 9), keluhan WhatsApp tanpa balasan 5 dari 7. Hasil contoh lama di folder `examples/` ditulis sebelum perbaikan ini.
- Contoh disegarkan (2026-10-16): `examples/01`–`05` disamakan dengan keluaran v1.0.12 (52 masukan, WhatsApp 13, Pengiriman 10 = 19,2%, keluhan WA tanpa balasan 5 dari 7) dan `examples/data/anonim-2026-09.csv` dibuat ulang dengan perintah contoh 01. Skor/verdik uji tidak berubah; rincian di `examples/HASIL-UJI.md` bagian "Contoh disegarkan ke v1.0.12". `00-*.md`, `06`–`10`, dan `HASIL-UJI-ULANG.md` dibiarkan sebagai catatan uji historis.
- Uji baru di `scripts/uji_olah_masukan.py` (kelas `UjiPesanSistemWA`); angka contoh di `tests/uji_regresi_106.py` dan `tests/uji_regresi_107.py` disesuaikan.

## Catatan revisi 1.0.11 (2026-10-02)
- Revisi dari uji ulang OpenClaw: pelanggan di laporan, ringkasan, dan draf balasan disebut dengan inisial atau nomor urut ("Pelanggan A", "pelanggan #3"), bukan nama. Balasan publik (ulasan marketplace, Google Maps, komentar) tidak boleh memuat nama, nomor pesanan, atau detail pengenal, dan tidak boleh ditawarkan versi "pakai nama asli"; placeholder `{panggilan}` hanya untuk balasan pribadi yang dikirim manusia.
- Tema keamanan ditulis per jenis (jamur, basi/kedaluwarsa, hewan/serangga, dst.), tidak digabung dalam satu label. Daftar periksa dan template balasan diperbarui.

## Catatan revisi 1.0.10 (2026-10-02)
- Script mencetak bagian "Kalimat ringkasan siap salin" (total masukan, keluhan vs pesan tanpa balasan, sentimen per kanal, tiap tema beserta rincian). Agent diminta menyalinnya apa adanya, tidak menghitung persentase sendiri.
- Tema Keamanan dirinci per jenis (jamur, hewan/serangga, basi/kedaluwarsa, benda asing, sakit).
- Koreksi `--koreksi` dengan jenis "bukan keluhan" kini berlaku untuk semua hitungan (tabel tema, respons staf, daftar "Perlu dibaca").
- Bila permintaan ditolak (mis. ulasan palsu), agent wajib langsung memberi alternatif aman dalam pesan yang sama, seperti draf permintaan ulasan jujur untuk pelanggan yang benar-benar membeli.

## Catatan revisi 1.0.9 (2026-10-02)
- Revisi dari uji OpenClaw (toko kue fiktif): kosakata tekstur kue/roti ("bantat", "tengahnya basah" = keluhan; "tidak bantat" = pujian); "bintik hijau", "jamuran" = Keamanan; "roti sobek" dikenali sebagai nama produk, bukan barang robek.
- Keterlambatan tanpa kata "telat" ("nyampe jam 4 padahal janjinya jam 10", "3 hari belum datang") dihitung sebagai keluhan Pengiriman.
- Baru: hitungan respons staf (keluhan WhatsApp/ulasan yang belum dibalas, opsi `--staf`), sentimen per kanal dihitung script, dan `--koreksi` untuk mencatat koreksi agent dan menghitung ulang. Aturan: angka disalin dari script. Ditambah `templates/koreksi-contoh.csv` dan uji regresi baru.

## Catatan revisi 1.0.8 (2026-10-01)
- SKILL.md kini menyebut bahwa script ada di subfolder `scripts/` di folder skill, dan agent tidak boleh mencari file ke seluruh disk (mis. `find /`). Logika tidak berubah.

## Catatan revisi 1.0.7 (2026-09-30)
- Perbaikan struktural dari uji buta: koreksi salah ketik tidak lagi mengubah kata yang sah ("krimnya", "kirinya" tetap utuh); "SMP/SMA" tidak dibaca sebagai slang.
- Kata samar (kirim, datang, telat, sampai) pada usaha jasa (EO, fotografer, bimbel, desain) dihitung ke "Waktu tunggu / jadwal" atau "Layanan", bukan Pengiriman barang.
- Sindiran tanpa kata negatif ("hebat, 3 hari baru jawab") masuk "Perlu dibaca agent" sebagai `[KELUHAN?]`.
- Daftar kata kustom di `tema.json` yang berisi koma/titik atau hanya angka diberi PERINGATAN; penyamaran: kata sifat sesudah sapaan ("Mas telaten") bukan nama, kode model produk ("Sony A7 III") bukan plat nomor.

## Catatan revisi 1.0.6 (2026-09-30)
- `kata_positif` dan `kata_negatif` kustom boleh berupa frasa ("belum kelar", "pelan banget"); entri yang tidak bisa dipakai diberi PERINGATAN, tidak diabaikan diam-diam.
- Aturan baru: masukan bertema yang semua temanya netral dan tanpa nilai tinggi masuk "Perlu dibaca", sehingga menambah kata tema tidak bisa membuat masukan negatif hilang dari daftar baca.
- "Jarang dibersihin" dibaca keluhan sedangkan "jarang telat" pujian; keterlambatan berangka ("telat 2 jam") keluhan kuat; "takut X, ternyata aman" dibaca lega. Ditambah baris "Aturan kerja" di SKILL.md.

## Catatan revisi 1.0.5 (2026-09-30)
- Perbaikan struktural: negasi eksistensial ("tidak ada yang rusak", "tanpa bau") dibaca positif, sedangkan "tidak ada yang balas" tetap keluhan; salah kirim umum ("pesan X, yang datang Y") dikenali; "abis" berarti "sesudah" dalam "abis dibanting".
- Penyamaran tidak lagi menghapus kata umum sesudah sapaan ("gpp kak maklum"); pesan media WhatsApp iOS/Inggris ("image omitted") dibuang; id `hapus_tema` yang salah dan berkas `.json` diberi peringatan.

## Catatan revisi 1.0.4 (2026-09-30)
- Enam perbaikan dari uji buta: "abis/habis" bermakna "sesudah" tidak lagi dibaca stok habis; pertanyaan restock bernada senang atau bintang 4-5 dianggap permintaan, bukan keluhan; "di read" dibaca chat diabaikan; sindiran dan pertanyaan menagih minimal masuk "Perlu dibaca agent"; `templates/tema-contoh.json` tidak lagi menghitung "jam makan siang" sebagai pengiriman. Uji regresi baru.

## Catatan revisi 1.0.3 (2026-09-30)
- Jaring pengaman keluhan: tidak ada keluhan berlabel yang hilang diam-diam; setiap keluhan masuk tabel tema atau daftar "Perlu dibaca agent". Kosakata tema diperluas (ketepatan pesanan, pengiriman, stok) dan normalisasi slang/singkatan/huruf berulang diperkuat. Uji regresi dengan set berlabel baru ditambah.

## Catatan revisi 1.0.2 (2026-09-29)
- Patch atas temuan uji ulang: kolom NPS Google Form ("...merekomendasikan...?", "Kepuasan") dikenali bila isinya angka; format tanggal AS dan tanggal ambigu diberi PERINGATAN, opsi `--urutan-tanggal`; berkas `.txt` UTF-16 bertab dibaca sebagai tabel.
- "pas dipakai" tidak lagi dibaca pujian, kalimat harapan ("semoga gak telat") dibaca saran, "dikirim2" bukan nomor; nama belakang sesudah "a.n." disamarkan; tema ketepatan pesanan, pengiriman, dan stok diperkuat. 85 uji otomatis lulus.

## Catatan revisi 1.0.1 (2026-09-29)
- Revisi setelah uji pertama (skor 6/10), 15 butir: kolom teks dipilih per kata judul (bukan potongan kata) sehingga "Ulasan Pembeli" terbaca dan "Waktu Ulasan" atau "Balasan Penjual" dilewati; baris `Sumber` dan `PERINGATAN` menyebut kolom yang dipakai.
- Nilai dibaca utuh (4,5; 8/10; ★★★) dan skala 0-10 dihitung sebagai NPS; negasi ("tidak", "kurang") diperbaiki; duplikat hanya baris identik; tema baru (tempat, waktu tunggu, bau, kebersihan) dan template tema fashion, kafe, laundry/jasa.
- Pesan galat jelas (`GAGAL`) untuk berkas rusak, penyamaran data pribadi diperluas (telepon rumah, perumahan/blok/RT-RW, plat nomor, "a.n."), tren menandai data kecil. Agent wajib membaca masukan di CSV anonim dan kutipan tiap tema. Recall keluhan pada set uji naik dari 59-63% menjadi 83-100%.

## Catatan revisi 1.0.0 (2026-09-29)
- Rilis awal (uji internal): mengubah masukan pelanggan dari semua kanal (chat WhatsApp, ulasan Shopee/Tokopedia/Google Maps, komentar, survei) menjadi rencana perbaikan berurutan, dengan penyamaran data pribadi otomatis, tema, sentimen, tren bulanan, template backlog dan balasan. Kerangka diadaptasi dari karya berlisensi MIT dan Apache-2.0 (lihat `ATTRIBUTION.md`).
