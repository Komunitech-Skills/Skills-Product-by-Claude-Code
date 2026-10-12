# Contoh 3: Input tidak lengkap: kinerja karyawan turun

> Hasil uji OpenClaw asli (2026-10-12, model claude-sonnet-5, uji otomatis agent). Perbandingan lengkap sebelum/sesudah: `00-openclaw-sebelum-sesudah.md`.

## Masukan pengguna
"Karyawan saya kinerjanya turun, tolong bantu cara ngomongnya."

## Keluaran di chat (dengan skill)

> Pelan tapi jelas — ini kerangka yang bisa langsung dipakai, isi bagian `[isian: ...]` dengan kejadian konkret punyamu.
>
> **Kerangka: Konteks → Fakta → Dampak → Tanya → Sepakat**
>
> **(a) Naskah ucapan (empat mata, bukan di depan tim)**
>
> "[Nama], saya mau ngobrol soal kerjaan beberapa [isian: minggu/hari] terakhir, 10-15 menit ya.
>
> Saya lihat [isian: kejadian konkret yang bisa dilihat — contoh: 'minggu ini 3 laporan telat dikirim dari jadwal', 'ada 2 pesanan salah input', 'target harian meleset 2 hari berturut-turut']. Dari sisi [isian: toko/tim/pelanggan], ini bikin [isian: dampaknya apa — contoh: 'rekap kas jadi telat', 'pelanggan komplain', 'temen lain harus nutupin'].
>
> Dari sisi kamu sendiri, ada kendala apa akhir-akhir ini? ... (dengarkan sampai selesai, jangan motong)
>
> Oke, kalau begitu kita sepakat [isian: langkah konkret — contoh: 'mulai besok cek ulang sebelum kirim', 'kamu kabari saya kalau kewalahan di jam sibuk']. Kita cek lagi [isian: tanggal], gimana?"
>
> Hindari kata "selalu/sering/malas" — sebut tanggal dan jumlah. Jangan dibungkus pujian basa-basi di depan ("sandwich"); kalau memang ada hal bagus, puji itu terpisah dan spesifik di lain waktu.
>
> **(b) Pesan WA ajakan ngobrol (bukan buat negur lewat WA)**
>
> "[Nama], besok [isian: jam/waktu] bisa ngobrol sebentar ga? Ada yang mau saya omongin soal kerjaan, santai aja, bukan hal buruk kok."
>
> **(c) Tindak lanjut**
> - Catat kesepakatan: langkah apa, mulai kapan → `[isian]`
> - Cek ulang tanggal: `[isian]` (kalau jatuh libur, geser ke hari kerja berikutnya)
> - Kalau belum ada perubahan di cek ulang itu baru naik ke teguran tertulis — beda skill (surat teguran karyawan), bukan sekarang
>
> **(d) Asumsi + pertanyaan**
> Saya asumsikan ini baru percakapan pertama (bukan sudah berkali-kali ditegur), dan empat mata saja cukup — bukan lewat WA tertulis.
>
> 1. Kejadian konkretnya apa persis (telat, hasil kerja, sikap ke pelanggan, lainnya)?
> 2. Ini baru pertama kali ngobrolin, atau sudah pernah ditegur sebelumnya?
> 3. Karyawannya tipe gampang kebuka atau cenderung diam/defensif kalau ditegur?
>
> Kalau kamu kasih tahu detailnya, saya bisa isiin naskahnya jadi lebih pas dan siap langsung dipakai.

## Catatan penguji
Skor sebelum 6.5 / sesudah 8.0. SESUDAH (8,0): kerjakan dulu: naskah ucapan berbingkai `[isian]` lengkap, pesan WA ajakan siap kirim, tindak lanjut (geser bila tanggal jatuh libur), asumsi, 3 pertanyaan di akhir (sesuai aturan maks 3). Kurang: WA ajakan memakai "bukan hal buruk kok" (frasa yang dalam skill sendiri diwanti-wanti), kata "beda skill" bocor ke pengguna, dan kerangka masih umum karena memang tanpa data.
