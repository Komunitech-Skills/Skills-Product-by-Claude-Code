# Skenario 04 — Input tidak lengkap / keliru

**Penguji:** pembuat skill, 2026-09-30. Dijalankan sungguhan terhadap **Kanboard v1.2.54 asli** (kode sumber resmi tag git `v1.2.54`, PHP 8.4 + SQLite, `http://127.0.0.1:8080`, zona waktu aplikasi Asia/Jakarta). Akun AI: `ayu` (peran Manajer) dengan token pribadi yang disimpan lewat `simpan-kunci` (token tidak pernah tampil). Data fiktif. Baris `$` ditampilkan tanpa tanda kutip; saat mengetik sendiri, bungkus nilai yang berisi spasi dengan tanda kutip.

## Permintaan pengguna
> "Tambah kartu: kirim sampel kain ke Bu Wati, deadline akhir bulan, tugaskan ke Dedi."

## Bila dijalankan tanpa papan
```
$ python3 scripts/kanboard.py tambah-kartu --judul Kirim sampel kain ke Bu Wati
GAGAL: Sebutkan papannya: --papan "nama atau id" (lihat daftar-papan).
(kode keluar 2)
```

Agent melihat daftar papan:
```
$ python3 scripts/kanboard.py daftar-papan
DAFTAR PAPAN KANBOARD
- Produksi Konveksi Ayu (id 1)
- Order Batik Laras (id 2)
(kode keluar 0)
```

## Pertanyaan agent (sekali, satu pesan)
> Sebelum saya buat, mohon pastikan:
> 1. Masuk papan mana — **Produksi Konveksi Ayu** atau **Order Batik Laras**?
> 2. Dedi belum jadi anggota papan di Kanboard, jadi belum bisa ditugaskan. Mau tanpa PIC dulu, atau tambahkan Dedi di Kanboard (papan → ikon roda → Izin)?

Pengguna: "Batik Laras. Tanpa PIC dulu."

## Keluaran nyata untuk data yang keliru
```
$ python3 scripts/kanboard.py tambah-kartu --papan Batik Laras --judul Kirim sampel kain ke Bu Wati --tenggat 31/10 --ke dedi
GAGAL: Anggota 'dedi' tidak ditemukan di papan ini. Yang bisa ditugaskan: Ayu Lestari.
SARAN: Tambahkan orang itu sebagai anggota papan di Kanboard (ikon roda > Izin), atau buat kartu tanpa --ke.
(kode keluar 2)
```

Versi awal belum mengenal "akhir bulan":
```
$ python3 scripts/kanboard.py tambah-kartu --papan Batik Laras --judul Kirim sampel kain ke Bu Wati --tenggat akhir bulan
GAGAL: Tenggat tidak dikenali: 'akhir bulan'.
SARAN: Format yang didukung: 'hari ini', 'besok', 'lusa', 'N hari lagi', nama hari ('Jumat', 'Jumat depan'), 'minggu depan', '25/10' (tanggal/bulan), '25/10/2026', '25 Oktober 2026', '2026-10-25'; boleh ditambah 'jam 14:00'.
(kode keluar 2)
```

Setelah uji ini pembuat menambahkan `akhir bulan` dan `awal bulan depan` (+ uji regresi). Dijalankan ulang ke Kanboard asli:
```
$ python3 scripts/kanboard.py tambah-kartu --papan "Batik Laras" --judul "Kirim sampel kain ke Bu Wati" --tenggat "akhir bulan" --ya
KARTU DIBUAT: #9
Papan: Order Batik Laras (id 2)
Kolom: Pesanan Baru
Judul: Kirim sampel kain ke Bu Wati
Jatuh tempo: Rabu, 30 September 2026 jam 17:00 WIB
```
"Akhir bulan" = hari ini (30 September) dan jam 17:00 sudah lewat saat dicoba, sehingga versi akhir juga menampilkan **PERINGATAN: jatuh tempo ini SUDAH LEWAT** di pratinjau (ditambahkan setelah uji ini; tercakup uji regresi). Ungkapan samar "besok lusa"/"kapan-kapan" kini ditolak, tidak ditebak.

## Pelajaran
- Tanya **sekali**, dalam satu pesan, untuk semua kekurangan (papan, PIC).
- Tidak ada yang ditulis ke Kanboard sebelum data lengkap dan pengguna menjawab "ya".
