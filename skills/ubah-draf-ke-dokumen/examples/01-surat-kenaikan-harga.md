# Skenario 1: draf WA/ChatGPT jadi surat kenaikan harga (normal utama; juga konteks Telegram)

- **Tanggal uji:** 2026-10-12 (versi 1.0.1; OpenClaw 2026.9.6 lokal, model claude-sonnet-5; detail sebelum/sesudah lengkap di `00-openclaw-sebelum-sesudah.md`)
- **Data pesan:** `data/pesan-1-surat-kenaikan-harga.txt`
- **Data fiktif:** nama "Bayu" (nama fiktif), usaha, alamat, email `.example`, dan nomor telepon `08xx-xxxx-xxxx` (nomor fiktif, disamarkan 2026-10-13) hanya contoh.

## Input (pesan pengguna)

```
Tolong rapikan draf ini jadi surat resmi siap kirim ke pelanggan, pakai kop usaha saya. Kop: Kopi Seduh Nusantara, Jl. Dago Asri No. 12, Bandung 40135, Telp 08xx-xxxx-xxxx (nomor fiktif), email halo@kopiseduh-nusantara.example. Ini drafnya dari chat WA saya sama ChatGPT:

Tentu! Berikut ini draf suratnya ya kak 😊
yth. pelanggan setia kami
mulai 1 nov 2026 harga biji kopi kami naik ya soalnya harga bahan baku naik juga
- arabika gayo 250gr dari 68000 jadi 75000
- robusta lampung 250 gr dari 45rb jadi 49rb
- house blend 500gr dari 120.000 jadi 129.000
pesanan yg masuk sebelum 31 okt masih pake harga lama
kalau mau tanya wa aja ke 08xx-xxxx-xxxx
makasih banyak ya kak 🙏
-bayu pemilik
```

## Output SESUDAH (skill aktif) - biasa

> **Dokumen lengkap:**
>
> ```
> KOPI SEDUH NUSANTARA
> Jl. Dago Asri No. 12, Bandung 40135
> Telp 08xx-xxxx-xxxx · Email halo@kopiseduh-nusantara.example
> ────────────────────────────────────────────────
>
> Bandung, 12 Oktober 2026
>
> Perihal: Pemberitahuan Penyesuaian Harga Biji Kopi
>
> Yth. Pelanggan Setia Kopi Seduh Nusantara
> di tempat
>
> Dengan hormat,
>
> Bersama surat ini kami sampaikan bahwa mulai tanggal **1 November 2026**, Kopi Seduh Nusantara akan menyesuaikan harga sejumlah produk biji kopi. Penyesuaian ini dilakukan karena adanya kenaikan harga bahan baku.
>
> Rincian penyesuaian harga adalah sebagai berikut:
>
> | Produk | Harga Lama | Harga Baru |
> |---|---|---|
> | Arabika Gayo 250 gr | Rp68.000 | Rp75.000 |
> | Robusta Lampung 250 gr | Rp45.000 | Rp49.000 |
> | House Blend 500 gr | Rp120.000 | Rp129.000 |
>
> Untuk pesanan yang masuk **sebelum tanggal 31 Oktober 2026**, harga lama masih berlaku sepenuhnya.
>
> Apabila Bapak/Ibu memiliki pertanyaan, silakan menghubungi kami melalui WhatsApp di nomor 08xx-xxxx-xxxx.
>
> Kami mengucapkan terima kasih atas kepercayaan dan dukungan Bapak/Ibu selama ini.
>
> Hormat kami,
>
>
> Bayu
> Pemilik, Kopi Seduh Nusantara
> ```
>
> **Perubahan yang dirapikan:**
> - Dibuang basa-basi AI ("Tentu! Berikut ini draf suratnya ya kak 😊") dan emoji.
> - Ditambah kop usaha sesuai yang Anda berikan.
> - Ditambah tanggal surat, perihal, dan struktur pembuka-isi-penutup surat resmi.
> - Daftar harga diubah jadi tabel dengan format Rupiah baku (Rp68.000, bukan "68000"/"45rb"/"120.000").
> - Nada disesuaikan jadi formal-sopan ("kak" → "Bapak/Ibu"), tanpa mengubah angka atau fakta dari draf asli.
> - Tanda tangan dirapikan: nama, jabatan, nama usaha.
>
> **Asumsi & pertanyaan:**
> - Tidak memakai nomor surat (mis. 001/KSN/X/2026) karena draf tidak menyebutkannya — beri tahu jika Anda ingin ditambahkan.
> - Nama lengkap "Bayu" dipakai apa adanya dari draf; sebutkan jika perlu nama lengkap/gelar untuk tanda tangan.
> - Surat ini ditujukan umum ke "Pelanggan Setia" — beri tahu jika perlu versi dengan nama pelanggan personal.
>
> Isi lengkap sudah ada di atas. Kalau perlu file Word, balas 'kirim file' — saya coba lampirkan.

## Output SESUDAH (skill aktif) - konteks Telegram

> **KOPI SEDUH NUSANTARA**
> Jl. Dago Asri No. 12, Bandung 40135 · Telp 08xx-xxxx-xxxx · Email halo@kopiseduh-nusantara.example
> ────────────────────────────────────────
>
> Bandung, 12 Oktober 2026
>
> Perihal: Pemberitahuan Penyesuaian Harga Biji Kopi
>
> Yth. Pelanggan Setia Kami
> di Tempat
>
> Dengan hormat,
>
> Sehubungan dengan kenaikan harga bahan baku, kami informasikan bahwa mulai **1 November 2026** akan berlaku penyesuaian harga untuk produk biji kopi kami sebagai berikut:
>
> - Arabika Gayo 250 gr: dari Rp68.000 menjadi Rp75.000
> - Robusta Lampung 250 gr: dari Rp45.000 menjadi Rp49.000
> - House Blend 500 gr: dari Rp120.000 menjadi Rp129.000
>
> Pesanan yang masuk sebelum tanggal 31 Oktober 2026 masih akan dikenakan harga lama.
>
> Apabila ada pertanyaan, Bapak/Ibu dapat menghubungi kami melalui WhatsApp di nomor 08xx-xxxx-xxxx.
>
> Kami mengucapkan terima kasih atas kepercayaan dan dukungan Bapak/Ibu selama ini.
>
> Hormat kami,
>
> Bayu
> Pemilik, Kopi Seduh Nusantara
>
> ---
>
> Perubahan yang dirapikan:
> - Diberi kop usaha, tanggal surat, dan perihal (sebelumnya langsung masuk isi).
> - Sapaan dan penutup dirapikan jadi format surat resmi ("Yth.", "Dengan hormat,", "Hormat kami,").
> - Daftar harga diformat rapi dengan format Rupiah konsisten (Rp68.000 dst, bukan "68000"/"45rb").
> - Emoji dan gaya chat ("Tentu! ... ya kak 😊", "🙏") dihapus, bahasa dibuat formal-sopan.
> - Tanda tangan diberi nama lengkap jabatan "Pemilik, Kopi Seduh Nusantara" dari "-bayu pemilik".
>
> Asumsi: tanggal surat saya pakai tanggal hari ini (12 Oktober 2026) — ganti kalau mau tanggal lain. Kalau nama "Bayu" perlu nama lengkap, kasih tahu saya.
>
> Isi lengkap sudah ada di atas. Kalau perlu file Word, balas "kirim file" — saya coba lampirkan.

## Output SESUDAH (skill aktif) - balasan "kirim file" (Telegram)

> File Word-nya sudah jadi, saya lampirkan.

## Catatan penguji
- Skor: SEBELUM 7,0 -> SESUDAH 8,8.
- Angka dan tanggal benar; tanpa nomor surat/karangan (SEBELUM mode biasa menambah nomor surat `001/KSN/X/2026`).
- Telegram: isi utuh, tanpa path, tidak menulis "terlampir" pada giliran penawaran, tawaran "balas 'kirim file'" ada. Setelah "kirim file", file dibuat dan dilampirkan lewat payload media, **tetapi file .docx tidak valid XML** (`xmlns:r` hilang): `data/hasil-kirim-file-skenario1-v1.0.1.docx`.

