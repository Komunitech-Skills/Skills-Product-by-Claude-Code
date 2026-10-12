# Skenario 1: draf WA/ChatGPT jadi surat kenaikan harga (normal utama, juga konteks Telegram)

- **Tanggal uji:** 2026-10-12 (OpenClaw 2026.9.6 lokal, model claude-sonnet-5; detail sebelum/sesudah lengkap di `00-openclaw-sebelum-sesudah.md`)
- **Data pesan:** `data/pesan-1-surat-kenaikan-harga.txt`

## Input (pesan pengguna)

```
Tolong rapikan draf ini jadi surat resmi siap kirim ke pelanggan, pakai kop usaha saya. Kop: Kopi Seduh Nusantara, Jl. Dago Asri No. 12, Bandung 40135, Telp 0812-3456-7890, email halo@kopiseduh-nusantara.example. Ini drafnya dari chat WA saya sama ChatGPT:

Tentu! Berikut ini draf suratnya ya kak 😊
yth. pelanggan setia kami
mulai 1 nov 2026 harga biji kopi kami naik ya soalnya harga bahan baku naik juga
- arabika gayo 250gr dari 68000 jadi 75000
- robusta lampung 250 gr dari 45rb jadi 49rb
- house blend 500gr dari 120.000 jadi 129.000
pesanan yg masuk sebelum 31 okt masih pake harga lama
kalau mau tanya wa aja ke 0812-3456-7890
makasih banyak ya kak 🙏
-bayu pemilik
```

## Output SESUDAH (skill aktif)

> Berikut surat resmi yang sudah dirapikan dengan kop usaha Anda — tinggal salin dan kirim:
>
> ---
>
> **KOPI SEDUH NUSANTARA**
> Jl. Dago Asri No. 12, Bandung 40135
> Telp. 0812-3456-7890 · Email: halo@kopiseduh-nusantara.example
> ────────────────────────────────────────
>
> Bandung, 12 Oktober 2026
>
> Perihal: Pemberitahuan Penyesuaian Harga Biji Kopi
>
> Yth. Pelanggan Setia Kopi Seduh Nusantara
> di Tempat
>
> Dengan hormat,
>
> Bersama surat ini, kami sampaikan bahwa mulai **1 November 2026**, Kopi Seduh Nusantara akan melakukan penyesuaian harga pada beberapa produk biji kopi kami. Penyesuaian ini kami lakukan menyusul kenaikan harga bahan baku.
>
> Rincian harga baru adalah sebagai berikut:
>
> | Produk | Harga Lama | Harga Baru |
> |---|---|---|
> | Arabika Gayo 250 gr | Rp68.000 | Rp75.000 |
> | Robusta Lampung 250 gr | Rp45.000 | Rp49.000 |
> | House Blend 500 gr | Rp120.000 | Rp129.000 |
>
> Bagi Bapak/Ibu yang melakukan pemesanan **sebelum tanggal 31 Oktober 2026**, harga yang berlaku masih mengikuti harga lama.
>
> Apabila terdapat pertanyaan lebih lanjut, Bapak/Ibu dapat menghubungi kami melalui WhatsApp di nomor 0812-3456-7890.
>
> Kami mengucapkan terima kasih atas kepercayaan dan dukungan Bapak/Ibu selama ini kepada Kopi Seduh Nusantara.
>
> Hormat kami,
>
> Bayu
> Pemilik — Kopi Seduh Nusantara
>
> ---
>
> **Perubahan yang dirapikan:**
> - Dihapus basa-basi chat ("Tentu!", emoji, sapaan "kak") dan diganti sapaan surat formal.
> - Ditambahkan kop usaha, tanggal, dan perihal surat.
> - Daftar harga diubah jadi tabel dengan format Rupiah standar (Rp68.000, dst).
> - Kalimat disusun jadi paragraf resmi tapi tetap ramah, ditutup dengan tanda tangan "Bayu, Pemilik".
> - Tanggal ditulis lengkap format Indonesia (1 November 2026, 31 Oktober 2026).
>
> **Asumsi/pertanyaan:**
> 1. Tanggal surat saya isi hari ini (12 Oktober 2026) — kalau mau tanggal lain, beri tahu saya.
> 2. Nama penanda tangan saya tulis "Bayu, Pemilik" — kalau nama lengkap/jabatan beda, beri tahu.
> 3. Tidak saya beri nomor surat resmi (misal 001/KSN/X/2026) — kalau perlu, saya tambahkan.
>
> Isi lengkap sudah ada di atas. Kalau perlu file Word, balas 'kirim file' — saya coba lampirkan.

## Catatan

- Skor SEBELUM 6,5 -> SESUDAH 8,8. Semua harga (Rp68.000->75.000, Rp45.000->49.000, Rp120.000->129.000), tanggal 1 November 2026 dan batas 31 Oktober 2026 benar.
- Konteks Telegram: surat utuh tampil di chat, ada daftar perubahan, asumsi, 3 pertanyaan, dan kalimat baku "balas 'kirim file'" (path tidak disebut), sesuai keputusan pemilik.
- Tanpa skill di mode biasa, agent hanya menulis ke file workspace dan isi surat tidak muncul di chat.
- Balasan "kirim file" membuat .docx valid (`data/hasil-kirim-file-skenario1.docx`) tetapi agent menulis "File Word terlampir." padahal tidak ada alat kirim file: klaim keliru.
