# Skenario 02 — Toko batik online: papan order & pengiriman, pindah kartu (normal)

**Penguji:** pembuat skill, 2026-09-30. Dijalankan sungguhan terhadap **Kanboard v1.2.54 asli** (kode sumber resmi tag git `v1.2.54`, PHP 8.4 + SQLite, `http://127.0.0.1:8080`, zona waktu aplikasi Asia/Jakarta). Akun AI: `ayu` (peran Manajer) dengan token pribadi yang disimpan lewat `simpan-kunci` (token tidak pernah tampil). Data fiktif. Baris `$` ditampilkan tanpa tanda kutip; saat mengetik sendiri, bungkus nilai yang berisi spasi dengan tanda kutip.

## Permintaan pengguna
> "Buatkan papan order & pengiriman untuk toko Batik Laras. Masukkan pesanan Mbak Sinta (selendang) deadline 3 hari lagi. Terus order Pak Joko sudah diserahkan ke kurir, pindahkan ke Dikirim ya."

Agent menunjukkan pratinjau papan dan kartu lebih dulu (seperti skenario 01); pengguna menjawab "ya". Dua kartu lain (INV-0921 di *Menunggu Bayar*, INV-0922 di *Dikemas*) dibuat dengan cara yang sama sebelumnya.

## Papan & kartu (setelah "ya")
```
$ python3 scripts/kanboard.py buat-papan --jenis order-pengiriman --nama Order Batik Laras --ya
PAPAN DIBUAT: Order Batik Laras (id 2)
Template: order-pengiriman - Order & Pengiriman (toko online, distributor)
Kolom:
  1. Pesanan Baru
  2. Menunggu Bayar
  3. Dikemas
  4. Dikirim
  5. Retur/Komplain
  6. Diterima
Buka: http://127.0.0.1:8080/?controller=BoardViewController&action=show&project_id=2
(kode keluar 0)
```

```
$ python3 scripts/kanboard.py tambah-kartu --papan Batik Laras --judul INV-0923 Mbak Sinta - selendang --tenggat 3 hari lagi --ya
KARTU DIBUAT: #4
Papan: Order Batik Laras (id 2)
Kolom: Pesanan Baru
Judul: INV-0923 Mbak Sinta - selendang
Jatuh tempo: Sabtu, 3 Oktober 2026 jam 17:00 WIB
(kode keluar 0)
```

## Pindah kartu: pratinjau → "ya" → simpan
```
$ python3 scripts/kanboard.py pindah-kartu --id 3 --ke-kolom dikirim
PRATINJAU PINDAH KARTU #3: INV-0922 Pak Joko - kemeja L
Dari: Dikemas
Ke: Dikirim
Belum dipindah. Lanjut? (ya/tidak)
(kode keluar 0)
```

```
$ python3 scripts/kanboard.py pindah-kartu --id 3 --ke-kolom dikirim --ya
KARTU DIPINDAH #3: INV-0922 Pak Joko - kemeja L
Dari: Dikemas
Ke: Dikirim
(kode keluar 0)
```

Pengguna tak sengaja meminta lagi — tidak ada perubahan ganda:
```
$ python3 scripts/kanboard.py pindah-kartu --id 3 --ke-kolom Dikirim --ya
KARTU #3 SUDAH di kolom Dikirim - tidak ada yang diubah.
(kode keluar 0)
```

## Isi kolom
```
$ python3 scripts/kanboard.py kolom --papan Batik Laras
KOLOM PAPAN: Order Batik Laras (id 2)
1. Pesanan Baru (id 7): 1 kartu
2. Menunggu Bayar (id 8): 1 kartu
3. Dikemas (id 9): 0 kartu
4. Dikirim (id 10): 1 kartu
5. Retur/Komplain (id 11): 0 kartu
6. Diterima (id 12): 0 kartu
(kode keluar 0)
```

## Nama kolom ambigu ditangani
```
$ python3 scripts/kanboard.py pindah-kartu --id 3 --ke-kolom Di
GAGAL: Nama kolom 'Di' cocok lebih dari satu: Dikemas, Dikirim, Diterima. Tulis nama lengkapnya.
(kode keluar 7)
```

Agent bertanya sekali: "Maksudnya Dikemas, Dikirim, atau Diterima?"

## Catatan
Template `order-pengiriman` menaruh **Diterima** di kolom paling kanan karena skill menganggap kolom terakhir = beres (tidak dihitung terlambat/macet). Kanboard mencatat `date_moved` baru saat kartu #3 dipindah (dicek lewat API).
