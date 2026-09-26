# HASIL UJI — buku-piutang v1.0.0 (commit 3e02391)

- **Penguji:** agent independen lintas akun (Akun B), 26 Sep 2026. Hanya membaca folder skill; verifikasi angka dengan skrip Decimal sendiri dari data mentah, **tanpa membaca kode** `piutang.py`.
- **Lingkungan:** Linux, Python 3.11; salinan skill + `tagih-piutang` di scratchpad (`uji-bp/`), DB terpisah per skenario, data rekaan. Jenis uji: `claude-code (simulasi agent)`.

## Ringkasan
| Uji | Hasil |
|---|---|
| `tests/uji_regresi.py` | 52 tes OK |
| `python3 scripts/validate.py --skill buku-piutang` | ✅ 1 skill valid, 72 baris katalog sesuai |
| `bash scripts/uji_openclaw.sh` (OpenClaw 2026.9.6) | buku-piutang eligible / modelVisible / commandVisible ✅ (skrip keluar 1 karena `gaji-umkm` & `resi-picking`, bukan skill ini) |
| 01 Distributor sembako 30 pelanggan (impor CSV 49 baris) | ✅ angka 100% cocok |
| 02 Jasa servis AC, DPP+PPN, `--per`, PPh 23 via `potong` | ✅ |
| 03 Toko bangunan: cicilan, dobel, kelebihan bayar, deposit, batal bayar, kembalikan | ✅ |
| 04 Input tidak lengkap, tanggal ambigu, nominal & CSV rusak, DB rusak | ✅ kecuali 1 jalur restore (P2) |
| 05 Kirim massal + denda sepihak + ancaman | ✅ perilaku agent; guard `--pesan` kurang (P2) |
| A/B tanpa skill | dengan skill jelas lebih baik |
| Banding pesaing (`Denymbird/accounts-receivable-skills`, Kledo, Frappe Books) | unggul untuk target pasar; pesaing unggul di DSO & statement |
| Ekspor → `tagih-piutang` (`hitung_telat.py --file`) | terbaca; total & bucket identik (Rp 110.811.250; Rp 6.781.979) |

## Verifikasi angka independen (inti)
- Saldo 26 pelanggan, total Rp 110.811.250, bucket belum JT / 1–30 / 31–60 / 61–90 / >90 dan persen 1 desimal: cocok semua; juga cocok dengan skrip pesaing.
- Batas bucket 0/1/30/31/60/61/90/91 hari dan jendela 7/8 hari: benar.
- PPN floor sekali (500.500; 135.802; 933.333), pembulatan sen ROUND_HALF_UP (4.333.333,50 → 4.333.334; 1.234.567,49 → 1.234.567), catatan Coretax selalu muncul.
- Bayar sebagian, alokasi JT paling awal, kelebihan 166.666 → deposit → pakai-kredit, batal bayar membuka kembali 450.500, posisi `--per` lampau, rekonsiliasi rekap (bayar 20.650.000 = nota 20.583.334 + dikembalikan 66.666): cocok.
- Tanggal: `03/04/2026` = 3 Apr (hari/bulan), `3 Apr 26` = 3 Apr 2026 + catatan tahun 2 angka; format Amerika, tanggal tak ada, seri Excel, masa depan, tanpa tahun > 180 hari ditolak dengan pesan jelas.
- Restore: header rusak, file terpotong, halaman data rusak → pulih, saldo identik sebelum/sesudah, file rusak dipindah bukan dihapus.

## Temuan berprioritas
**P2 (perbaiki sebelum rilis)**
1. **Restore buntu saat halaman indeks tabel `meta` rusak** (uji 04-E, halaman 3 SQLite). Pesan menjadi "bukan database buku-piutang ... periksa --db"; `restore --ya` dan `init --mulai-baru` sama-sama menolak. Bertentangan dengan janji SKILL.md ("bisa walau database rusak total") dan membuat pengguna harus memindahkan file sendiri, hal yang dilarang SKILL.md. Bedakan "SQLite malformed" dari "database aplikasi lain" (mis. ada tabel `nota`/`pelanggan` di `sqlite_master`) dan izinkan restore memindahkan file.
2. **`draf --pesan` tanpa pemeriksaan isi** (uji 05). Teks berisi ancaman lapor polisi, sebar ke grup RT, dan denda 5% dijadikan tautan wa.me tanpa `peringatan`. Tambahkan pemeriksaan kata kunci → `peringatan` + minta konfirmasi (tanpa memblokir teks sopan).

**P3 (perbaikan kecil)**
3. Deteksi nama mirip terlalu sensitif untuk awalan umum: "Toko Hana" ~ "Toko Candra", "Toko Joko" ~ "Toko Eko", "Pel 2" ~ "Pel 1". Aman, tetapi merepotkan distributor dengan puluhan "Toko/Warung ...". Pertimbangkan membandingkan bagian nama setelah awalan umum (Toko, Warung, Kios, CV, PT, Bu, Pak).
4. Impor: status `??` (hanya tanda baca) diimpor sebagai piutang; menurut dokumentasi seharusnya menjadi baris bermasalah.
5. PPh 23 untuk pelanggan B2B jasa belum dipandu; `potong` berhasil tetapi rekap melabelinya "retur/diskon/hapus". Tambah satu baris panduan + label terpisah.
6. `ringkasan`: DP dari kolom `dibayar` impor dihitung sebagai "Pembayaran masuk kemarin" (bertanggal nota) sehingga bisa terbaca sebagai uang masuk baru.
7. `catat` memeriksa nominal sebelum kemiripan nama, jadi agent yang mengandalkan pesan error bertanya dua kali. Error argparse (kode 2) tidak keluar sebagai JSON walau `--json`.
8. Kosmetik: `ekspor --samarkan` menulis `'-` untuk WA kosong; urutan daftar `umur` tidak dijelaskan (bukan menurut total).

## Skor kualitas: **8/10**
**Alasan:** inti uang dan tanggal sangat kuat. Semua angka terverifikasi independen dan cocok dengan pesaing. Input buruk ditangani paling teliti di antara skill sejenis yang diuji (format Amerika, seri Excel, nominal ambigu, CSV Windows-1252, formula injection, dobel nota/bayar, invarian saldo). Alur pratinjau → `--ya` dan cadangan konsisten. Nilai tambah dibanding tanpa skill dan dibanding pesaing jelas. Belum 9 karena ada dua celah P2 pada aspek "reliable" dan "aman": satu jalur pemulihan DB yang buntu dan tidak adanya guard script pada teks tagihan bebas. Setelah P2 diperbaiki dan diuji ulang, skor 9 wajar.

**Rekomendasi status:** `lulus` (≥ 7) boleh dicatat pemilik. Perbaiki P2 sebelum `beta`/uji platform asli, lalu minta uji ulang oleh penguji independen untuk kedua perbaikan. `platform_teruji` = `claude-code (simulasi agent)` + muat OpenClaw otomatis; jadwal Telegram (`openclaw automations add`) belum diuji di Gateway.
