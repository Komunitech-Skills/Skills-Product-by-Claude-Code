# 03 — "bikinin dong" ide konten dari 12 ulasan bintang 5 (S3, normal & malas)

## Skenario
Penjual keripik pedas rumahan menempel 12 ulasan bintang 5 dengan format emoji ⭐ dan meminta ide konten. Permintaannya singkat dan malas.

## Input pengguna
> bikinin dong ide konten dr review2 ini
> ⭐⭐⭐⭐⭐ keripiknya renyah bgt, pedesnya nagih
> ⭐⭐⭐⭐⭐ udah ke-4 kali order, anak2 suka
> ⭐⭐⭐⭐⭐ packing rapi pake kardus, ga ada yg remuk
> ⭐⭐⭐⭐⭐ enak, gurih, bumbunya berasa sampe dalem
> ⭐⭐⭐⭐⭐ pengiriman cepet, besoknya udah sampe Bekasi
> ⭐⭐⭐⭐⭐ level 5 beneran pedes, mantul
> ⭐⭐⭐⭐⭐ harga murah, isinya banyak
> ⭐⭐⭐⭐⭐ renyah & ga keras, cocok buat ngemil nonton
> ⭐⭐⭐⭐⭐ makasih bonus stikernya kak, lucu
> ⭐⭐⭐⭐⭐ enak bgt, bakal order lagi buat oleh2
> ⭐⭐⭐⭐⭐ bumbunya pas ga keasinan
> ⭐⭐⭐⭐⭐ kriuk kriuk, ketagihan

## Langkah agent
Tempelan disimpan ke `ulasan.txt`, lalu `python3 scripts/olah_ulasan.py ulasan.txt --format teks`. Format ⭐ dikenali (12 ulasan berbintang). Script memberi peringatan sampel kecil. Agent membaca 1 ulasan yang belum terklasifikasi ("bumbunya pas ga keasinan"), yang ternyata pujian rasa. Karena permintaannya fokus pada ide konten, laporan dipersingkat (SKILL.md: "Tujuan khusus").

## Output

# Ide Konten dari Ulasan — Keripik Pedas (12 ulasan, semuanya 5★)
*Hanya 12 ulasan dan semuanya bintang 5, jadi ini bahan konten, bukan gambaran kepuasan seluruh pembeli.*

**Pujian yang paling sering muncul** (dihitung script, dicek agent):
| Pujian | Ulasan | Contoh kutipan |
|---|---|---|
| Rasa: renyah, gurih, pedas nagih | 7 dari 12 | "keripiknya renyah bgt, pedesnya nagih" |
| Pembeli berulang | 2 | "udah ke-4 kali order, anak2 suka" |
| Kemasan aman | 1 | "packing rapi pake kardus, ga ada yg remuk" |
| Pengiriman cepat | 1 | "pengiriman cepet, besoknya udah sampe Bekasi" |
| Harga & isi | 1 | "harga murah, isinya banyak" |
| Bonus stiker | 1 | "makasih bonus stikernya kak, lucu" |

**Ide konten**
1. **TikTok/Reels 10–15 detik, "tes kriuk"**. Hook (3 detik pertama): suara "kriuk" keripik dipatahkan dekat mikrofon. Teks di layar menampilkan kutipan "renyah & ga keras, cocok buat ngemil nonton". CTA: "Cek keranjang kuning, pilih level pedasmu."
2. **Carousel IG "Kata yang udah langganan"**. Hook: "Kenapa ada yang order sampai 4 kali?" Kutipan: "udah ke-4 kali order, anak2 suka" dan "bakal order lagi buat oleh2". CTA: "[isi: info paket oleh-oleh, bila memang ada], DM untuk pesan."
3. **Video ASMR packing (TikTok/Story)**. Hook: "Keripik rapuh dikirim jauh, aman nggak?" Kutipan: "packing rapi pake kardus, ga ada yg remuk". CTA: "Pesan sekarang, [isi: jangkauan pengiriman Anda]." Jangan menulis "tidak pernah remuk", karena buktinya baru satu ulasan.
4. **Story tantangan "Level 5 beneran pedes?"**. Hook: seseorang mencoba level 5 (teman atau tim sendiri, dengan izin). Kutipan: "level 5 beneran pedes, mantul". CTA: polling "Kamu kuat level berapa?"
5. **WA Status "Bonus kecil"**. Tampilkan foto stiker bonus dengan kutipan "makasih bonus stikernya kak, lucu". Pakai ini hanya selama bonus stiker memang masih dikirim.

**Aturan pakai:** jangan tampilkan nama atau username pembeli. Screenshot ulasan harus diburamkan bagian identitasnya. Untuk iklan berbayar, minta izin pembeli dulu. Jangan menambah klaim yang tidak ada di ulasan (mis. "terlaris", "tanpa pengawet"). Untuk caption lengkap pakai skill `caption-sosmed-umkm`; untuk jadwal sebulan pakai `kalender-konten-30hari`.

**Catatan metode:** 12 ulasan diolah script (rata-rata 5,0★). "Rasa" dikoreksi agent dari 5 ke 7 ulasan dengan menambah "bumbunya pas ga keasinan" dan "level 5 beneran pedes". Tidak ada keluhan terdeteksi.

## Catatan penguji
- Bagus: format ⭐ terbaca, permintaan malas tetap dilayani tanpa bertanya ulang, dan ide konten patuh aturan `references/ide-konten.md` (tanpa klaim baru, ada izin, ada CTA).
- Kurang: "kriuk kriuk, ketagihan" dan "ga keasinan" tidak langsung masuk p_rasa. Kata "ketagihan" tidak ada di kamus (yang ada hanya "nagih"). Ini gap slang kecil.
