# Riwayat perubahan — presentasi-data-ke-atasan

Catatan teknis per versi.

## Catatan revisi 1.0.5 (2026-10-13)
- Batasan di SKILL.md ditambah aturan eksplisit: angka hanya dari data pengguna atau keluaran script (nominal dimasukkan dalam Rupiah penuh atau `jt`/`rb`, bukan "dalam juta", agar rata-rata tidak terbulatkan); detail yang tidak ada di input (kanal/marketplace, PIC, nominal anggaran, jadwal/program) ditulis `[isian: ...]`.
- Contoh 02: rata-rata mingguan nilai stok diperbaiki Rp30.000.000 → Rp30.333.333 (182.000.000 ÷ 6, dihitung ulang lewat script). Contoh 01–03 dan cuplikan README: "Shopee", nominal penurunan budget, PIC, dan "alokasi stok & jadwal promo" yang tidak ada di input diganti `[isian: ...]`.
- Tes ditambah: rata-rata daftar ber-satuan `jt` contoh 02 = 30.333.333.

## Catatan revisi 1.0.4 (2026-10-01)
- Petunjuk lokasi script ditambahkan di SKILL.md: script ada di subfolder `scripts/` di folder skill. Agent dilarang mencari script atau file pengguna ke seluruh disk (mis. `find /`).

## Catatan revisi 1.0.3 (2026-09-30)
- Format angka Indonesia diperbaiki: `scripts/hitung_perubahan.py` kini membaca `38.000`, `Rp 1.250.000`, `2,5`, `38rb`, dan `1,5jt`. Bentuk ragu seperti "38.5" atau "1,500" ditolak dengan pesan jelas, tidak ditebak diam-diam; agent menanyakan maksudnya. Pemisah `--daftar` boleh titik-koma bila ada koma desimal atau rb/jt. Ditambah uji.

## Catatan revisi 1.0.2 (2026-09-29)
- Baris "Aturan kerja" ditambahkan di SKILL.md: agent tidak boleh memasang paket/aplikasi sendiri, tidak membuka atau mencari file di luar yang diberikan pengguna, dan hasil yang ditulis ke file harus disebut lokasinya (folder kerja, bukan `/tmp`).

## Catatan revisi 1.0.1 (2026-09-26)
- Perbaikan dari uji independen pertama (9/10): bila nilai lama negatif (mis. laba rugi dari -Rp5.000.000 ke Rp2.000.000), script tetap menghitung persen secara benar tetapi menyertakan catatan agar persennya tidak ditampilkan mentah-mentah; cukup sebut arah dan selisih rupiah.
- Permintaan memoles, membulatkan, atau membalik arah angka demi terlihat bagus ditolak dengan sopan, lalu agent menawarkan alternatif jujur (sorot sisi positif yang memang ada di data).
- Nama fungsi pembulat di script diganti `format_angka` karena dipakai juga untuk angka yang bukan rupiah.

## Catatan revisi 1.0.0 (2026-09-26)
- Rilis awal (uji internal): mengubah angka/tabel menjadi pesan untuk atasan, pemilik, investor, atau bank dalam empat format siap pakai (ringkasan WA 5 baris, email formal, satu halaman eksekutif, dan skrip bicara 2 menit), dengan `scripts/hitung_perubahan.py` untuk perhitungan perubahan. Gagasan struktur diadaptasi dari skill berlisensi MIT (lihat `ATTRIBUTION.md`).
