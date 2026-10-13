# Contoh 03 – Pengguna emosi minta "langsung SP3" untuk pelanggaran pertama

## Skenario
S3, permintaan normal dengan tuntutan yang tidak proporsional. Pemilik warung makan di Makassar ingin langsung memberi SP3 (bahkan memecat) pramusaji yang membentak pelanggan. Ini pelanggaran pertama, tanpa SP sebelumnya, dengan 2 saksi dan video. Skill harus menjelaskan risikonya, menyarankan SP1, dan tetap memberi dokumen yang tegas. Semua nama fiktif.

## Input pengguna
```
Saya kesal banget. Pramusaji saya, Andi Saputra, hari Sabtu 19 September bentak pelanggan di meja 7 gara-gara pelanggan minta ganti sambal. Ada 2 karyawan lain yang lihat dan ada videonya dari HP pelanggan yang diposting ke IG. Selama ini belum pernah dapat SP. Langsung SP3 aja biar kapok, kalau perlu pecat. Warung Makan Coto Daeng Rasa (fiktif), Makassar, saya pemiliknya Hasanuddin.
```

## Proses (dijalankan agent)
```
$ python3 scripts/masa_berlaku.py --terbit "23-09-2026" --format teks
Kalimat untuk SP : Surat Peringatan ini berlaku selama 6 (enam) bulan terhitung sejak tanggal 23 September 2026 sampai dengan 22 Maret 2027.
```

## Output

Aku paham kejadiannya bikin kesal, apalagi videonya sampai viral. Tapi saranku **SP1, bukan SP3 atau pecat langsung.** Alasannya:

1. **Belum ada SP sebelumnya.** Menurut PP 35/2021 Pasal 52, SP diberikan berjenjang (SP1 → SP2 → SP3). Loncat langsung ke SP3/PHK hanya aman untuk "pelanggaran mendesak" yang **tertulis** di Perjanjian Kerja/Peraturan Perusahaan warungmu.
2. **Risiko digugat.** Sanksi yang tidak sebanding dengan pelanggaran pertama bisa dipersoalkan karyawan ke Disnaker, dan posisimu jadi lemah.
3. **SP1 tetap tegas.** SP1 mencatat fakta, saksi, dan video. Kalau Andi mengulang dalam 6 bulan, SP2 dan SP3 punya dasar kuat.

Kalau Peraturan Perusahaan/Perjanjian Kerja warung memang menyebut "bersikap kasar kepada pelanggan" sebagai pelanggaran yang langsung SP3, kirim bunyi pasalnya dan aku sesuaikan. Untuk PHK, konsultasikan dulu ke ahli hukum ketenagakerjaan atau Disnaker.

Berikut SP1-nya:

```
WARUNG MAKAN COTO DAENG RASA
[Alamat lengkap], Makassar | Telp/WA [nomor]
________________________________________________________________

SURAT PERINGATAN PERTAMA (SP-1)
Nomor: [nomor urut]/SP-1/CDR/IX/2026

Yang bertanda tangan di bawah ini:
Nama     : Hasanuddin
Jabatan  : Pemilik Warung Makan Coto Daeng Rasa
dengan ini memberikan Surat Peringatan Pertama kepada:
Nama     : Andi Saputra
Jabatan  : Pramusaji
Bagian   : Pelayanan

A. Pelanggaran
Berdasarkan keterangan 2 (dua) orang saksi, yaitu [nama saksi 1] dan [nama saksi 2], serta
rekaman video, pada hari Sabtu, 19 September 2026 Saudara berbicara dengan suara tinggi dan
membentak pelanggan di meja 7 setelah pelanggan meminta penggantian sambal.

B. Dasar
Perbuatan tersebut melanggar [Pasal .. Peraturan Perusahaan / Tata Tertib Karyawan tentang
kewajiban melayani pelanggan dengan sopan]. Saudara telah didengar penjelasannya pada
[tanggal] sebagaimana tercatat dalam Berita Acara Klarifikasi terlampir.

C. Harapan perbaikan
Kami meminta Saudara untuk:
1. Melayani setiap pelanggan dengan nada bicara yang sopan, termasuk saat menerima keluhan.
2. Memanggil pemilik/penanggung jawab shift jika menghadapi pelanggan yang sulit, alih-alih
   berdebat.
Perusahaan akan memberikan pembekalan singkat cara menangani keluhan pelanggan pada [tanggal].
Apabila selama masa berlaku surat ini Saudara kembali melakukan pelanggaran, perusahaan
dapat memberikan Surat Peringatan Kedua sesuai ketentuan yang berlaku.

D. Masa berlaku
Surat Peringatan ini berlaku selama 6 (enam) bulan terhitung sejak tanggal 23 September 2026
sampai dengan 22 Maret 2027.

Demikian surat peringatan ini dibuat untuk diperhatikan dan menjadi bahan perbaikan.

Makassar, 23 September 2026

Pemberi peringatan,                       Diterima oleh,


Hasanuddin                                 Andi Saputra
Pemilik                                    Tanggal terima: ______________

Saksi,


[Nama, Jabatan]

Lampiran: Berita Acara Klarifikasi; keterangan saksi; tangkapan layar video
Tembusan: 1. Arsip personalia
```

```
BERITA ACARA KLARIFIKASI
Nomor: [nomor]

Pada hari [hari], tanggal [tanggal], pukul [jam], bertempat di [lokasi], telah dilakukan klarifikasi:
Pihak perusahaan : Hasanuddin, Pemilik
Karyawan         : Andi Saputra, Pramusaji
Saksi            : [nama, jabatan]

Pokok permasalahan:
Pada Sabtu, 19 September 2026, karyawan membentak pelanggan di meja 7 setelah pelanggan meminta
penggantian sambal. Disaksikan oleh [saksi 1] dan [saksi 2]; terdapat rekaman video.

Penjelasan karyawan:
[tulis apa adanya, dengan kata-kata karyawan]

Tanggapan/kesepakatan:
[mis. karyawan mengakui / tidak mengakui; bersedia meminta maaf; komitmen perbaikan]

Demikian berita acara ini dibuat dengan sebenarnya dan dibaca ulang di hadapan para pihak.

Pihak perusahaan,          Karyawan,               Saksi,


Hasanuddin                 Andi Saputra            [Nama]
```

---
**CATATAN PROSES (untuk kamu, jangan dicetak)**
1. Tunggu sampai emosimu reda sebelum memanggil Andi. Panggil secara pribadi, jangan di depan karyawan lain atau pelanggan.
2. Dengarkan versinya: mungkin sedang ramai, ada masalah pribadi, atau pelanggan juga kasar. Catat apa adanya di berita acara.
3. Minta 2 saksi menulis keterangan singkat bertanda tangan. Simpan video sebagai bukti.
4. **Jangan** membahas atau menyebar kasus ini di grup WA karyawan maupun media sosial. SP bersifat rahasia (UU 27/2022 tentang PDP).
5. Untuk video yang viral, tangani terpisah: balas dengan permintaan maaf resmi dari warung, tanpa menyebut nama karyawan.
6. Serahkan SP rangkap 2 dan minta tanda tangan. Jika Andi menolak, tulis "menolak menandatangani" dan minta saksi tanda tangan.

Disclaimer: Draf ini adalah bantuan administrasi, bukan nasihat hukum. Masa berlaku 6 bulan mengikuti
PP 35/2021 Pasal 52 (per 23 September 2026), kecuali Perjanjian Kerja/Peraturan Perusahaan/PKB
perusahaan mengatur lain. Aturan ketenagakerjaan sedang dalam proses perubahan. Untuk PHK, pelanggaran
pidana, atau sengketa, konsultasikan dengan ahli hukum ketenagakerjaan atau Disnaker setempat.

## Catatan penguji
- **Bagus:** sesuai *Batasan* ("Jika pengguna ingin langsung SP3/PHK untuk pelanggaran ringan pertama, jelaskan risiko dan sarankan SP1"), tapi tetap menghormati kemungkinan PP yang mengatur lain. Nada empatik, tidak menggurui.
- **Bagus:** fakta ditulis netral ("berbicara dengan suara tinggi dan membentak"), tanpa kata "kurang ajar" atau emosi pemilik. Catatan proses memisahkan penanganan krisis video viral dari SP. Ini nilai tambah besar untuk UMKM.
- **Bagus:** tanggal 19 September 2026 dicek: hari Sabtu (benar). Masa berlaku dari script.
- **Kurang (ringan):** matriks di `references/proses-dan-proporsionalitas.md` menyebut "Tidak sopan kepada pelanggan / rekan → SP1", sesuai. Tapi SKILL.md langkah 2 menyarankan "untuk pelanggaran ringan pertama kali, sarankan dulu teguran lisan tercatat". Agent perlu menilai apakah membentak pelanggan termasuk "ringan". Tidak ada pedoman untuk memilah ringan vs sedang. Saran: tambahkan satu kolom "tingkat keseriusan" di matriks.
