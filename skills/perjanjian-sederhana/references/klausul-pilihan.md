# Bank Klausul Pilihan

Pakai untuk mengganti/menambah pasal di template. Ganti `[isi: ...]` dengan data pengguna.

## Penyelesaian sengketa
**Opsi A: Musyawarah, lalu Pengadilan Negeri (default)**
> (1) Apabila terjadi perselisihan mengenai pelaksanaan Perjanjian ini, Para Pihak sepakat menyelesaikannya secara musyawarah untuk mufakat dalam waktu paling lama [isi: 30] ([isi: tiga puluh]) hari kalender sejak salah satu Pihak menyampaikan pemberitahuan tertulis.
> (2) Apabila musyawarah tidak mencapai mufakat, Para Pihak sepakat memilih penyelesaian melalui Pengadilan Negeri [isi: KOTA].

**Opsi B: Musyawarah, mediasi, lalu Pengadilan Negeri**
> (2) Apabila musyawarah tidak berhasil, Para Pihak dapat menempuh mediasi dengan mediator yang disepakati bersama. Biaya mediator ditanggung Para Pihak secara sama besar.
> (3) Apabila mediasi tidak berhasil dalam waktu [isi: 30] hari, sengketa diselesaikan melalui Pengadilan Negeri [isi: KOTA].

**Opsi C: Musyawarah, lalu arbitrase**
> (2) Apabila musyawarah tidak mencapai mufakat, sengketa diselesaikan melalui arbitrase oleh [isi: NAMA LENGKAP LEMBAGA ARBITRASE, mis. Badan Arbitrase Nasional Indonesia (BANI)] yang berkedudukan di [isi: ALAMAT/KOTA], menurut peraturan prosedur lembaga tersebut. Putusan arbitrase bersifat final dan mengikat Para Pihak.
> ⚠ TINJAU PENGACARA: dengan klausul arbitrase, Pengadilan Negeri tidak berwenang mengadili sengketa ini (UU 30/1999 Ps. 3 & 11). Biaya arbitrase bisa melebihi nilai sengketa kecil. Pastikan nama lengkap dan alamat lembaganya benar.

Tip untuk nilai kecil (≤ Rp500 juta): Opsi A memungkinkan **gugatan sederhana** di PN (lebih cepat dan murah). Sebutkan ini ke pengguna.

## Wanprestasi (umum)
> (1) Suatu Pihak dianggap wanprestasi apabila tidak melaksanakan, terlambat melaksanakan, atau melaksanakan tidak sebagaimana mestinya kewajibannya dalam Perjanjian ini, dan tetap tidak memperbaikinya dalam waktu [isi: 7] ([isi: tujuh]) hari kalender setelah menerima teguran tertulis dari Pihak lainnya.
> (2) Pihak yang dirugikan berhak menuntut pemenuhan kewajiban, ganti rugi atas kerugian nyata yang dapat dibuktikan, dan/atau mengakhiri Perjanjian ini sesuai Pasal Pengakhiran.

## Denda keterlambatan pembayaran
> Keterlambatan pembayaran dikenakan denda sebesar [isi: 0,1]% ([isi: nol koma satu persen]) per hari dari jumlah yang terlambat, paling banyak [isi: 5]% ([isi: lima persen]) dari jumlah tersebut.
> ⚠ TINJAU PENGACARA bila denda besar, tanpa batas, atau hanya berlaku sepihak.
Hitung contoh dengan `scripts/perjanjian.py denda`.

## Pengakhiran lebih awal
> (1) Perjanjian ini dapat diakhiri lebih awal: a. atas kesepakatan tertulis Para Pihak; b. oleh salah satu Pihak dengan pemberitahuan tertulis paling lambat [isi: 30] hari sebelumnya; atau c. oleh Pihak yang dirugikan apabila Pihak lainnya wanprestasi sebagaimana diatur dalam Pasal Wanprestasi.
> (2) Pengakhiran tidak menghapus kewajiban yang telah jatuh tempo sebelum tanggal pengakhiran.
> (3) Untuk pengakhiran ini, Para Pihak sepakat mengesampingkan ketentuan Pasal 1266 dan Pasal 1267 Kitab Undang-Undang Hukum Perdata sepanjang mensyaratkan putusan hakim.
> ⚠ TINJAU PENGACARA: keberlakuan pengesampingan Pasal 1266–1267 masih diperdebatkan.

## Pengosongan sepihak (OPSI, hanya bila pengguna sendiri memintanya; bukan default)
Jangan sisipkan tanpa permintaan pengguna. Bila diminta, tetap pertahankan teguran tertulis + tenggat, dan tulis peringatan ini tepat di bawah ayatnya serta di "Pasal yang sebaiknya ditinjau pengacara":
> ⚠ TINJAU PENGACARA: Klausul ini membolehkan pemilik mengosongkan/mengambil alih objek sewa (mengunci, menyegel, memindahkan barang) tanpa putusan pengadilan. Walau disepakati, tindakan sepihak berisiko digugat sebagai perbuatan melawan hukum (Ps. 1365 KUHPerdata) dan dilaporkan pidana (mis. memasuki pekarangan tanpa izin, perusakan/penggelapan barang penyewa). Klausul "sisa sewa hangus" juga bisa dinilai tidak seimbang. Jalur aman: teguran tertulis → tenggat → musyawarah/mediasi → gugatan (bisa gugatan sederhana bila nilai ≤ Rp500 juta, PERMA 4/2019).
Teks opsi: "Apabila PIHAK KEDUA tidak menyerahkan kembali Objek Sewa dalam tenggat ..., PIHAK KEDUA menyetujui PIHAK PERTAMA [isi: mengunci Objek Sewa / memindahkan barang PIHAK KEDUA ke ... dengan berita acara disaksikan 2 (dua) orang saksi], dan barang tersebut tetap milik PIHAK KEDUA serta dapat diambil kembali."

## Keadaan memaksa (umum)
> (1) Keadaan memaksa adalah keadaan di luar kendali dan kesalahan Para Pihak yang tidak dapat diperkirakan sebelumnya dan secara langsung menghalangi pelaksanaan Perjanjian, antara lain bencana alam, kebakaran, banjir, wabah yang ditetapkan pemerintah, perang, huru-hara, atau kebijakan pemerintah yang secara langsung melarang pelaksanaan Perjanjian.
> (2) Pihak yang mengalami keadaan memaksa wajib memberitahukan secara tertulis kepada Pihak lainnya paling lambat [isi: 7] ([isi: tujuh]) hari kalender sejak kejadian, disertai bukti yang wajar.
> (3) Selama keadaan memaksa, pelaksanaan kewajiban yang terdampak ditangguhkan tanpa denda. Apabila keadaan memaksa berlangsung lebih dari [isi: 60] ([isi: enam puluh]) hari kalender, Para Pihak akan bermusyawarah untuk melanjutkan, mengubah, atau mengakhiri Perjanjian, dengan menyelesaikan hak dan kewajiban yang telah timbul secara proporsional.
> (4) Kesulitan keuangan, kenaikan harga, atau kelalaian sendiri bukan keadaan memaksa.

## Kerahasiaan (sisipan untuk perjanjian non-NDA)
> Para Pihak wajib merahasiakan isi Perjanjian ini serta informasi usaha Pihak lainnya yang diperoleh karena Perjanjian ini (antara lain harga, data pelanggan, resep/formula, dan strategi usaha), kecuali diwajibkan oleh peraturan perundang-undangan atau atas persetujuan tertulis Pihak pemilik informasi. Kewajiban ini tetap berlaku [isi: 2] ([isi: dua]) tahun setelah Perjanjian berakhir.

## Pemberitahuan
> Setiap pemberitahuan berdasarkan Perjanjian ini dilakukan secara tertulis dan dianggap diterima apabila dikirim ke alamat atau nomor WhatsApp/email Para Pihak yang tercantum dalam Perjanjian ini. Perubahan alamat wajib diberitahukan secara tertulis.

## Lain-lain (umum)
> (1) Hal-hal yang belum atau tidak cukup diatur dalam Perjanjian ini akan diatur kemudian dalam addendum tertulis yang ditandatangani Para Pihak dan merupakan bagian tidak terpisahkan dari Perjanjian ini.
> (2) Apabila salah satu ketentuan dalam Perjanjian ini dinyatakan tidak berlaku, ketentuan lainnya tetap berlaku.
> (3) Tidak satu Pihak pun boleh mengalihkan hak dan kewajibannya berdasarkan Perjanjian ini kepada pihak lain tanpa persetujuan tertulis Pihak lainnya.
> (4) Lampiran Perjanjian ini merupakan bagian yang tidak terpisahkan dari Perjanjian ini.

## Identitas pihak berbentuk badan usaha
> [isi: NAMA], [isi: JABATAN], dalam hal ini bertindak dalam jabatannya tersebut untuk dan atas nama [isi: PT/CV NAMA], berkedudukan di [isi: KOTA], NIB [isi: NIB], berdasarkan [isi: akta pendirian/anggaran dasar terakhir Nomor ... atau surat kuasa tanggal ...], selanjutnya disebut "PIHAK PERTAMA".
