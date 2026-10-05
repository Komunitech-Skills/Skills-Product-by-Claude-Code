# Skenario 03 — Laporan pagi: terlambat, hari ini, macet (normal)

**Penguji:** pembuat skill, 2026-09-30. Dijalankan sungguhan terhadap **Kanboard v1.2.54 asli** (kode sumber resmi tag git `v1.2.54`, PHP 8.4 + SQLite, `http://127.0.0.1:8080`, zona waktu aplikasi Asia/Jakarta). Akun AI: `ayu` (peran Manajer) dengan token pribadi yang disimpan lewat `simpan-kunci` (token tidak pernah tampil). Data fiktif. Baris `$` ditampilkan tanpa tanda kutip; saat mengetik sendiri, bungkus nilai yang berisi spasi dengan tanda kutip.

**Penyiapan data uji (jujur):** agar ada kartu "macet" tanpa menunggu berhari-hari, kolom `date_moved` empat kartu di database SQLite uji dimundurkan 4–12 hari (langsung di database uji, bukan lewat skill). Kartu lain dibuat lewat `tambah-kartu --ya`. Kartu #8 "Topi event lari 100 pcs" sengaja berada di kolom terakhir (Selesai) dengan tenggat lampau dan diam 12 hari.

## Permintaan pengguna
> "Kasih laporan papan hari ini, yang telat dan yang macet. Terus yang macet lebih dari 5 hari saja apa?"

## Laporan lengkap
```
$ python3 scripts/kanboard.py laporan
LAPORAN PAPAN KERJA - Rabu, 30 September 2026 19:44 WIB
Papan: semua papan aktif | kartu terbuka: 8
Terlambat 3 | Jatuh tempo hari ini 2 | Macet >= 3 hari 3

TERLAMBAT (3)
- #6 Jaket himpunan 40 pcs (jatuh tempo 28 Sep 2026 17:00; papan: Produksi Konveksi Ayu; kolom: Siapkan Bahan)
- #3 INV-0922 Pak Joko - kemeja L (jatuh tempo 30 Sep 2026 15:00; papan: Order Batik Laras; kolom: Dikirim)
- #5 Kaos komunitas lari 60 pcs (jatuh tempo 30 Sep 2026 16:00; papan: Produksi Konveksi Ayu; kolom: Produksi)

HARI INI (2)
- #3 INV-0922 Pak Joko - kemeja L (jatuh tempo 30 Sep 2026 15:00; papan: Order Batik Laras; kolom: Dikirim)
- #5 Kaos komunitas lari 60 pcs (jatuh tempo 30 Sep 2026 16:00; papan: Produksi Konveksi Ayu; kolom: Produksi)

MACET >= 3 HARI (3)
- #6 Jaket himpunan 40 pcs (diam 6 hari; papan: Produksi Konveksi Ayu; kolom: Siapkan Bahan)
- #2 INV-0921 Bu Wati - 2 kain tulis (diam 5 hari; papan: Order Batik Laras; kolom: Menunggu Bayar)
- #7 Polo kantor PT Sinar 30 pcs (diam 4 hari; papan: Produksi Konveksi Ayu; kolom: Order Masuk)
(kode keluar 0)
```

## Macet ≥ 5 hari
```
$ python3 scripts/kanboard.py macet --hari 5
KARTU MACET (tidak pindah kolom >= 5 hari)
Papan: semua papan aktif
Jumlah: 2
Kartu di kolom TERAKHIR papan (mis. Selesai/Tayang/Diterima) dianggap beres dan tidak dihitung terlambat/macet.
- #6 Jaket himpunan 40 pcs (diam 6 hari; jatuh tempo 28 Sep 2026 17:00; papan: Produksi Konveksi Ayu; kolom: Siapkan Bahan)
- #2 INV-0921 Bu Wati - 2 kain tulis (diam 5 hari; jatuh tempo 1 Okt 2026 17:00; papan: Order Batik Laras; kolom: Menunggu Bayar)
(kode keluar 0)
```

## Verifikasi independen (dihitung ulang dari data API mentah)
- Terlambat = kartu terbuka, `date_due` < sekarang (19:44 WIB), bukan di kolom terakhir: #6 (28 Sep 17:00), #3 (hari ini 15:00), #5 (hari ini 16:00) → **3** ✔. #8 Topi tidak masuk karena di kolom Selesai ✔.
- Hari ini = `date_due` bertanggal 30 Sep 2026 WIB: #3, #5 → **2** ✔ (keduanya juga terlambat — catatan tumpang-tindih tampil di perintah `hari-ini`).
- Macet ≥ 3 hari: #6 (6 hari), #2 (5), #7 (4) → **3** ✔; ≥ 5 hari: #6, #2 ✔. #8 (12 hari) tidak masuk karena kolom terakhir ✔.
- Panjang pesan laporan 1.050-an karakter (< 3.500, aman untuk Telegram).

## Jawaban agent (ringkas)
Laporan ditempel apa adanya. Saran tindak lanjut (bukan tindakan otomatis): cek bahan Jaket himpunan (#6, macet 6 hari dan sudah telat), tagih pembayaran INV-0921 Bu Wati (#2, 5 hari di Menunggu Bayar). Untuk dikirim otomatis tiap pagi ke Telegram, lihat `references/openclaw-jadwal.md`.
