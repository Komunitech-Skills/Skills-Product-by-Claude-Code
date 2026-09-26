# Uji A/B — Skenario 01 tanpa skill vs dengan skill

- **Penguji:** agent independen Akun B, 26 Sep 2026. Permintaan & data sama dengan `01-distributor-sembako-30-pelanggan.md` (CSV 49 baris, 30 pelanggan).
- **Catatan jujur:** jawaban "tanpa skill" disimulasikan oleh penguji yang sama sebagai agent umum (tanpa folder skill, tanpa script), jadi ada bias pengetahuan. Perbedaan yang dicatat di bawah bersifat struktural, bukan soal gaya.

## Tanpa skill (agent umum)
Perilaku khas agent umum yang bisa menjalankan kode: membaca CSV, menulis skrip Python sekali pakai, lalu menampilkan tabel.
```
Rekap piutang UD Sumber Pangan (per 26/09/2026)
Total piutang: Rp 110.811.250 dari 38 nota
Umur: Current Rp 14.951.875 | 1-30 Rp 15.588.500 | 31-60 Rp 16.140.125 | 61-90 Rp 48.505.000 | >90 Rp 15.625.750
10 pelanggan terbesar: RM Padang Sederhana Rp 11.500.500, Toko Makmur Rp 9.750.000, ...

Contoh pesan tagihan:
"Yth. Bapak/Ibu Toko Makmur, kami mengingatkan tagihan sebesar Rp 9.750.000 yang telah jatuh tempo.
Mohon segera melakukan pembayaran. Terima kasih."
```
Hasil ini bisa benar angkanya **jika** agent kebetulan menulis kode (agent tanpa alat eksekusi akan menjumlah 38 baris di kepala — rawan salah). Yang tidak ada:
- **Tidak ada buku yang tersimpan.** Besok, saat "Kafe Senja transfer 1 juta", pengguna harus mengirim ulang seluruh file dan agent menghitung ulang dari nol; cicilan, deposit, dan pembatalan tidak punya tempat.
- Tidak ada aturan kelebihan bayar (saldo bisa minus diam-diam), tidak ada cegah nota/bayar dobel, tidak ada cadangan.
- Tanggal: "30 hari" dan format Amerika tidak diperiksa; baris lunas/void tergantung kejelian agent.
- Pesan tagihan satu gaya untuk semua (tidak membedakan belum jatuh tempo vs lewat 104 hari), tanpa rincian nota, tanpa rekening, tanpa tautan wa.me.
- Tidak ada samaran untuk ringkasan yang dibagikan, tidak ada jadwal ringkasan harian.

## Dengan skill
- Impor dengan pratinjau → persetujuan → cadangan otomatis → simpan; 11 baris lunas dilewati dengan alasan, baris bermasalah ditunjukkan nomornya.
- Angka umur, saldo 26 pelanggan, jatuh tempo 7 hari: **100% cocok** dengan verifikasi Decimal independen (lihat uji 01).
- Buku tetap tersimpan di komputer pemilik: pembayaran berikutnya cukup satu kalimat (`bayar`), alokasi otomatis ke JT paling awal, kelebihan bayar ditanyakan.
- Draf per pelanggan menyesuaikan tingkat keterlambatan (pengingat awal Bu Siti vs "terlewat-lama" + tawaran bertahap Toko Makmur), lengkap dengan rincian nota, rekening, dan tautan wa.me yang dikirim sendiri oleh pemilik.
- `ringkasan --samarkan` siap dijadwalkan ke Telegram pemilik.

## Kesimpulan
Dengan skill **jelas lebih baik**: bukan hanya laporan sekali jalan, tetapi buku piutang yang berkelanjutan, aman dari salah hitung/dobel/saldo minus, dengan draf tagihan yang langsung bisa dikirim. Bahan "sebelum/sesudah" README valid.
