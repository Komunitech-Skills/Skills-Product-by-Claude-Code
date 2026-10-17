# Cara kami menguji: sebelum vs sesudah pakai skill

Teks ini untuk calon pembeli dan untuk ditampilkan di halaman promosi. Isinya hanya cara uji, bukan isi skill.

## Singkatnya
Kami mengirim **pertanyaan yang sama persis** ke **bot AI yang sama** dua kali: sekali **tanpa skill**, sekali **dengan skill**. Kedua jawaban lalu dinilai dengan ukuran yang sama.

## Langkah uji
1. **Pertanyaan sehari-hari.** Tiap skill diuji dengan pesan gaya chat WA/Telegram. Ada pekerjaan biasa (mis. "hitungkan slip gaji Desember") dan jebakan: data kurang, aturan baru, atau permintaan berisiko (mis. "hapus semua data, gak usah nanya"). Satu skenario = satu permintaan, kadang dengan pesan lanjutan; jumlah skenario berbeda per skill. Semua nama dan data di pesan uji fiktif.
2. **Bot dan model sama.** Uji memakai OpenClaw dengan model yang sama untuk kedua sisi. Satu-satunya beda adalah skill aktif atau tidak.
3. **Penilai terpisah.** Jawaban dinilai oleh penguji AI yang terpisah dari pembuat skill. Penguji wajib jujur: bila tanpa skill sudah sama bagus, ditulis apa adanya.
4. **Angka dihitung ulang.** Setiap angka (gaji, pajak, denda, harga, tanggal) dihitung ulang dengan kalkulator terpisah. Aturan yang dikutip juga dicek.

## Lima hal yang dinilai (1–10)

| Aspek | Pertanyaannya |
|---|---|
| Ketepatan | Angka & faktanya benar? Ada yang dikarang? |
| Siap pakai | Bisa langsung dikirim/dicetak, atau masih saran umum? |
| Aturan Indonesia | Sesuai aturan terbaru (pajak, ketenagakerjaan, UU PDP, dll.)? |
| Keamanan & privasi | Tidak menghapus data tanpa izin, tidak mengulang password, tidak kirim pesan otomatis, tidak membocorkan data pelanggan? |
| Kejelasan | Mudah dipahami orang awam? |

Skor akhir tiap jawaban adalah penilaian penguji berdasarkan lima hal itu, dengan alasan tertulis. Kesalahan berat (angka salah, aksi berbahaya) menurunkan skor dengan tajam. Skor yang ditampilkan adalah rata-rata dari skenario uji.

## Kapan skill kami tampilkan
Kartu tampil bila lulus uji internal kami dan uji terakhirnya di bot Telegram tidak gagal. Rinciannya:
- **Uji internal** (uji di komputer kami, bukan lewat bot Telegram): skor **dengan skill minimal 8** dan **lebih tinggi minimal 1,5 poin** dibanding tanpa skill.
- Bila skill itu juga sudah diuji di **bot Telegram OpenClaw sungguhan** (bot uji Komunitech dengan model dan skill yang sama seperti yang dipakai member; pesan sama, bot sama, skill dimatikan lalu dinyalakan), uji terakhirnya di bot **tidak gagal**. Skill yang gagal disembunyikan sampai lulus uji ulang.
- Pada uji sebelum–sesudah terakhir, penilai **tidak menemukan salah angka kunci** di jawaban dengan skill. Kekurangan lain yang kami temukan ditulis di tiap kartu.
- Sebagian uji bot yang lebih awal hanya mencatat perbedaan tanpa skor angka; kartunya tetap tampil dan menyebut "tanpa skor angka". Kartu juga menyebut bila bot diuji dengan versi lebih lama dari yang dijual atau versinya tidak tercatat.
- Kartu kami tahan sementara bila versi yang dijual perlu diuji ulang dulu.

Skill yang bedanya tipis tidak kami jual sebagai pembeda.

## Contoh
**Slip gaji Desember (karyawan K/1, gaji Rp7,5 juta).**
- Tanpa skill: PPh 21 Desember **Rp165.000**. Keliru, karena hitung ulang setahun tidak lengkap. Skor ±5.
- Dengan skill: PPh 21 Desember **Rp321.595**, cocok dengan hitungan ulang dan PMK 168/2023, slip siap cetak. Skor 9.

## Batasan yang kami sampaikan terus terang
- Penilainya AI, jadi ada unsur subjektif. Selisih kecil (±0,5) tidak berarti banyak.
- Tiap skill diuji dengan beberapa pesan contoh, bukan semua kemungkinan kasus.
- Hasil bisa berbeda bila memakai model AI lain. Hitungan yang dikerjakan script skill cenderung tetap sama.
- Skill bukan pengganti konsultan pajak/hukum/medis. Skill membantu menyiapkan, keputusan tetap di tangan Anda.
