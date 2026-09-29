---
name: studio-video-pendek-ai
description: Ubah produk atau topik jadi paket produksi video pendek vertikal 15-60 detik (TikTok, Reels, Shorts) - pilihan hook, naskah per adegan dengan hitungan durasi, storyboard/shot list (rekam HP atau prompt generator video AI), teks di layar, teks sulih suara Bahasa Indonesia, caption + hashtag, dan checklist label konten AI. Netral alat, tanpa instalasi. Use for short video script, storyboard, AI video prompt, voice-over, TikTok/Reels/Shorts content plan, AI disclosure checklist, UMKM content.
---

# Studio Video Pendek AI

## Tujuan
Dari satu kalimat ("bikinin video 30 detik untuk kopi susu gula aren") menghasilkan **paket produksi siap pakai**: pemilik usaha tinggal merekam dengan HP atau menempel prompt ke alat video AI pilihannya, lalu unggah sendiri. Skill ini menulis rencana dan teks, **bukan** membuat file video, dan tidak memerlukan API key atau instalasi.

## Kapan Dipakai / Tidak
Pakai: naskah/storyboard/prompt video pendek untuk produk, jasa, edukasi ringan, atau promo; ide hook; caption + hashtag; cek label AI.
Jangan pakai (tolak dengan sopan, tawarkan alternatif aman):
- Meniru wajah/suara **orang lain** (artis, tokoh, pesaing, kenalan) tanpa izin tertulis. Klon diri sendiri boleh, dengan persetujuan: arahkan ke `references/checklist-klon-diri.md`.
- Testimoni palsu, "before-after" rekaan, ulasan pelanggan karangan.
- Klaim kesehatan menyesatkan (menyembuhkan, "turun 10 kg seminggu") atau keuangan (untung pasti, "modal kecil balik berlipat").
- Konten hukum/medis/investasi yang butuh profesional; konten SARA, penipuan, atau menyerang pihak lain.
- Mengunggah otomatis: skill ini **tidak** memposting apa pun. Semua unggahan manual oleh pemilik akun.

## Input
Minimal: (1) produk/topik, (2) tujuan (jualan, edukasi, branding, promo). Opsional: durasi (default 30 dtk), platform (default TikTok + Reels + Shorts), harga & promo, target pembeli, gaya (santai/lucu/elegan), cara produksi (rekam HP / alat video AI / campuran), ada/tidaknya orang di layar, nama merek.
Bila info kurang: **tanya sekali** dalam satu pesan berisi daftar pendek (maks. 5 pertanyaan). Bila pengguna ingin cepat, pakai default lalu sebutkan asumsi di baris pertama ("Asumsi: 30 dtk, jualan, rekam HP, gaya santai").

## Langkah Kerja
1. **Tangkap brief.** Rangkum dalam 3-4 baris: produk, sasaran, satu janji utama (bukan lebih), bukti nyata yang benar-benar dimiliki (bahan, proses, jumlah terjual yang benar, sertifikat yang ada). Jangan mengarang bukti; bila tak ada, pakai demonstrasi proses.
2. **Tentukan durasi & jumlah adegan** (tabel di bawah). Video 15 dtk: 3 adegan. 30 dtk: 5-6. 45-60 dtk: 7-9.
3. **Tulis 3 pilihan hook** (3 detik pertama), masing-masing beda gaya: pertanyaan/masalah, pernyataan berani yang jujur, visual mengejutkan. Beri rekomendasi satu, sertakan alasannya satu kalimat. Lihat pola hook di bawah.
4. **Tulis naskah per adegan** dengan struktur Hook - Masalah/Konteks - Solusi/Produk - Bukti - CTA. Tiap adegan: nomor, rentang waktu, sulih suara, teks di layar.
5. **Hitung durasi.** Simpan sulih suara per adegan ke berkas teks format `Label | teks` dan jalankan `python3 scripts/durasi_naskah.py naskah.txt --target 30` (Windows: `python` atau `py`). Jika script tidak bisa dijalankan, hitung manual: **kata / 150 x 60 = detik** (jeda +0,5 dtk per tanda [jeda], +0,3 dtk antar adegan). Jika melebihi target, ringkas dulu; jangan menyuruh pengguna bicara lebih cepat dari ±170 kata/menit.
6. **Buat storyboard + shot list** dalam tabel (format di bawah). Untuk tiap adegan berikan **jalur A (rekam HP)** dan/atau **jalur B (prompt alat video AI)** sesuai pilihan pengguna. Bila belum memilih, berikan keduanya singkat.
7. **Teks sulih suara final** dalam Bahasa Indonesia sehari-hari: kalimat pendek (maks. ±12 kata), tanda `[jeda]`, penekanan dengan HURUF BESAR seperlunya, angka ditulis cara diucapkan ("dua puluh dua ribu rupiah") supaya suara AI/pemilik tidak salah baca.
8. **Caption + hashtag** (format di bawah).
9. **Checklist label & etika** (bagian "Label Konten AI"). Selalu sertakan, sesuaikan dengan jalur produksi yang dipilih.
10. **Cek akhir sebelum menyerahkan:** durasi dalam target; tidak ada klaim yang tak bisa dibuktikan; tidak ada wajah/suara orang lain; musik dari perpustakaan platform; harga/promo sama dengan input; teks di layar terbaca (maks. 7 kata per layar).

## Pola Hook (3 detik pertama)
| Gaya | Contoh (kopi susu) |
|---|---|
| Masalah | "Jam tiga sore, mata udah setengah watt?" |
| Angka jujur | "Dua puluh dua ribu, sudah dapat kopi yang diseduh baru." |
| Larangan ringan | "Jangan beli kopi susu dulu sebelum lihat ini." (bukan clickbait bohong; isi harus relevan) |
| Visual | Tuang gula aren cair ke gelas, ASMR, tanpa bicara 2 detik. |
| Penonton spesifik | "Buat kamu yang kerja WFH dan bosan sama kopi sachet." |
Hindari hook yang berjanji sesuatu yang tidak dibuktikan di video.

## Format Output
Keluarkan urut dengan judul bagian tetap ini:

**0. Asumsi & Brief** (3-4 baris)
**1. Pilihan Hook** (3 opsi + rekomendasi)
**2. Naskah & Timing**
| # | Waktu | Sulih suara | Teks di layar |
|---|---|---|---|
| 1 | 0-3 dtk | ... | ... |

Lalu satu baris: "Perkiraan durasi sulih suara: NN dtk (target NN dtk, 150 kata/menit)".
**3. Storyboard & Shot List**
| # | Visual | Jalur A: rekam HP (sudut, jarak, cahaya, properti) | Jalur B: prompt video AI |
|---|---|---|---|
**4. Teks Sulih Suara Final** (utuh, satu blok, dengan [jeda] dan cara baca angka)
**5. Caption & Hashtag**
**6. Checklist Label AI & Etika** (centang sesuai jalur produksi)
**7. Langkah Produksi Cepat** (urutan kerja 4-6 langkah, tanpa menyebut merek alat kecuali diminta pengguna)

## Blok Prompt Generik untuk Alat Video/Gambar AI
Tempel di alat apa pun (teks-ke-video atau gambar-ke-video). Tulis **satu blok per adegan**, klip 3-8 detik, dalam bahasa Inggris (kebanyakan alat lebih akurat), tanpa nama orang/merek terkenal:

```
[Subject]   what is in frame, concrete (e.g. "iced palm-sugar milk coffee in a clear glass, condensation on glass")
[Action]    one simple movement (e.g. "dark palm sugar syrup slowly swirls into white milk")
[Setting]   place + light (e.g. "small Indonesian cafe counter, warm morning window light")
[Camera]    vertical 9:16, shot size, movement (e.g. "close-up, slow push-in, shallow depth of field")
[Style]     realistic product commercial, natural colors, no text in frame
[Duration]  4 seconds
[Avoid]     distorted hands, extra fingers, garbled text or logos, real people's faces, brand logos
```
Aturan prompt: satu aksi per klip; jangan minta teks/logo/harga dari AI (tambahkan sendiri di aplikasi edit karena huruf AI sering rusak); untuk produk asli pakai **gambar-ke-video dari foto produk sendiri** supaya wujud produk tidak melenceng dan pembeli tidak merasa tertipu; simpan "seed"/pengaturan yang berhasil untuk konsistensi antaradegan; beri tahu pengguna bahwa hasil bisa perlu beberapa kali coba.
Untuk sulih suara AI: tempel teks sulih suara final, pilih suara generik bawaan alat (bukan tiruan orang lain), lalu dengarkan seluruhnya untuk cek salah baca.

## Storyboard Rekam HP (jalur A) - panduan singkat
Vertikal 9:16, HP ditopang (tripod/tumpukan buku), cahaya jendela di samping (hindari bayangan wajah dari atas), lensa dibersihkan, satu klip 2-5 detik per adegan, rekam 2 kali. Sebutkan properti yang harus disiapkan per adegan. Jika pemilik tidak mau tampil, pakai tangan/produk saja (POV tangan) atau sulih suara di atas gambar.

## Caption & Hashtag
- Caption: 1 kalimat hook ulang + 1 kalimat manfaat + CTA jelas ("Pesan via WA di profil") + harga bila relevan. TikTok: ≤ 150 karakter ideal; Reels/Shorts boleh lebih panjang.
- Hashtag: 5-8 buah = 2 luas (#kopitiktok), 3 niche (#kopisusugularen), 1-2 lokal/kota, 1 merek. Jangan pakai hashtag yang tidak relevan demi jangkauan.
- **Kalimat pengungkapan** bila ada unsur AI: "Video ini dibuat dengan bantuan AI." Letakkan di baris pertama/terakhir caption, bukan disembunyikan di antara hashtag.
- Berikan 2 varian caption (santai dan singkat).

## Label Konten AI (ringkasan, per 2026-09-29)
Ringkasan berikut berasal dari sumber pihak ketiga yang dirangkum di riset Komunitech (`research/sources/video-ai-2026-09-29.md`); **aturan platform sering berubah**. Minta pengguna memeriksa halaman bantuan resmi platform sebelum unggah. Detail dan tautan ada di `references/label-ai.md`.
- **TikTok:** wajib beri label bila video memuat wajah/suara sintetis yang realistis. Ada tombol "AI-generated content" di layar unggah. TikTok juga dapat membaca metadata C2PA dan melabeli otomatis.
- **YouTube (Shorts):** centang pengungkapan "altered or synthetic content" untuk konten realistis yang bisa disangka nyata (orang, kejadian, tempat). Animasi jelas fiksi/efek produksi biasa umumnya tidak perlu.
- **Instagram/Facebook (Meta):** label "AI info" bisa terpasang otomatis; gunakan opsi pengungkapan AI saat unggah bila tersedia.
- **Kebiasaan aman (semua platform):** tambahkan kalimat "dibuat dengan bantuan AI" di caption bila ada visual/suara buatan AI yang tampak nyata; jangan menghapus watermark/penanda AI dari alat; pakai musik/suara dari perpustakaan resmi platform; unggah manual.
Checklist ringkas (cetak di bagian 6 output):
- [ ] Ada wajah/suara/kejadian buatan AI yang tampak nyata? Jika ya, label platform dicentang.
- [ ] Kalimat "dibuat dengan bantuan AI" ada di caption.
- [ ] Tidak ada wajah/suara orang lain tanpa izin tertulis (klon diri sendiri: sudah persetujuan).
- [ ] Tidak ada testimoni/ulasan/before-after rekaan; produk di video sama dengan barang yang dikirim.
- [ ] Klaim kesehatan/keuangan tidak menyesatkan; harga & promo benar.
- [ ] Musik dari perpustakaan platform (bukan lagu unduhan).
- [ ] Watermark/penanda AI alat tidak dihapus.
- [ ] Unggah manual; tidak ada janji "posting otomatis".

## Contoh Ringkas
Input: "Bikin video 30 detik kopi susu gula aren, Rp22.000, jualan lewat WA."
Output (potongan): Asumsi: 30 dtk, jualan, rekam HP, santai. Hook rekomendasi: "Jam tiga sore, mata udah setengah watt?" Naskah 6 adegan, perkiraan sulih suara 28,3 dtk. Contoh lengkap: `examples/contoh-pembuat-kopi-aren.md`.

## Batasan & Penanganan Error
- Tidak membuat/mengedit berkas video, tidak menjalankan alat pihak ketiga, tidak memposting. Skill ini tidak berafiliasi dengan alat atau platform mana pun; nama alat hanya disebut bila pengguna yang menyebutnya.
- Bahasa naskah: Indonesia sehari-hari; sesuaikan dialek/logat hanya bila diminta. Bahasa Inggris hanya untuk prompt generator.
- Produk diatur (obat, suplemen, kosmetik, makanan olahan, alkohol, rokok): jangan klaim khasiat; minta nomor izin edar (BPOM/PIRT/halal) hanya jika pengguna sudah memilikinya, dan jangan mengarang nomornya. Arahkan ke aturan platform untuk kategori terbatas.
- Durasi > 60 dtk: jelaskan bahwa skill ini untuk 15-60 dtk; tawarkan memecah jadi seri.
- Angka (harga, diskon, stok) hanya dari pengguna; jangan menebak. Hitung diskon/harga dengan aritmetika biasa dan bulatkan ke rupiah terdekat.
- Script gagal / Python tidak ada: hitung manual dengan rumus di Langkah 5 dan sebutkan bahwa itu perkiraan.
- Perkiraan durasi ±10-15%; sarankan pengguna merekam sulih suara lalu mengukur ulang.
- Info ini bukan nasihat hukum; aturan platform dan UU (mis. perlindungan data pribadi, hak cipta) bisa berubah.
