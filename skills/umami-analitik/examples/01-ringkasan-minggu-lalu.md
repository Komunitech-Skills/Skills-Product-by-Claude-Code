# 01 — Normal: "Pengunjung web saya minggu lalu berapa? Naik nggak?"

**Pembuat:** uji pembuat 29 Sep 2026 terhadap **Umami 3.4.0 asli** (Docker resmi, 127.0.0.1) dengan data fiktif landing page "Keripik Bu Sri" (`tests/isi_data_fiktif.py`). Akun AI `agen-baca` (view-only via tim), kunci API. Penguji independen menulis hasilnya sendiri di `HASIL-UJI.md`.

## Yang dijalankan agent
```
umami.py ringkasan --periode minggu-lalu
umami.py halaman --periode minggu-lalu
```

## Keluaran skill (apa adanya)
```
RINGKASAN WEBSITE: Keripik Bu Sri (landing) (keripikbusri.contoh.id)
Periode: minggu lalu, Senin 21 Sep 2026 - Minggu 27 Sep 2026
Pembanding: 14 Sep 2026 - 20 Sep 2026
- Pengunjung unik       : 11   (sebelumnya 4; naik 7 (+175%))
- Kunjungan             : 12   (sebelumnya 4; naik 8 (+200%))
- Tayangan halaman      : 23   (sebelumnya 6; naik 17 (+283%))
- Bounce rate           : 25% (3 dari 12 kunjungan hanya 1 halaman tanpa klik)   (sebelumnya 50%)
- Rata-rata lama        : 48 dtk per kunjungan   (sebelumnya 17 dtk)
- Halaman per kunjungan : 1,9
Catatan: pengunjung unik dihitung per perangkat+browser (tanpa cookie); satu orang dengan HP & laptop terhitung 2.

HALAMAN TERATAS: Keripik Bu Sri (landing) (keripikbusri.contoh.id)
Periode: minggu lalu, Senin 21 Sep 2026 - Minggu 27 Sep 2026
  Halaman                             Tayangan  Pengunjung  % pengunjung
  /                                         11          10           91%
  /produk/keripik-balado                     5           5           45%
  /cara-pesan                                3           3           27%
  /produk/keripik-original                   2           2           18%
  /terima-kasih                              2           2           18%
Total: 23 tayangan dari 11 pengunjung unik.
```

## Jawaban agent ke pengguna (ringkas)
Minggu lalu (Senin 21 – Minggu 27 Sep) website Ibu dikunjungi **11 pengunjung unik** (minggu sebelumnya 4, naik 175%), 23 halaman dibuka. Bounce rate turun dari 50% ke 25%. Halaman yang paling dilihat setelah beranda: **Keripik Balado** (5 pengunjung).

*Saran (bukan fakta):* 1) Taruh tombol WA di halaman Keripik Balado paling atas — halaman itu paling diminati. 2) Halaman Keripik Original baru dilihat 2 orang; coba tampilkan di beranda.

## Verifikasi independen
Hitung ulang dari daftar kunjungan fiktif (`isi_data_fiktif.py harapan --dari 2026-09-21 --sampai 2026-09-27`): 11 pengunjung, 12 kunjungan, 23 tayangan, 3 bounce, 580 detik → 580÷12 = 48 dtk; halaman `/` 10 pengunjung (11 tayangan). Pembanding 14–20 Sep: 4/4/6, bounce 2 dari 4 = 50%, 70÷4 = 17 dtk. **Semua cocok.**
