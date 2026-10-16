---
name: studio-video-pendek-ai
description: Ubah produk atau topik jadi paket produksi video pendek vertikal 15-60 detik (TikTok, Reels, Shorts) - pilihan hook, naskah per adegan dengan hitungan durasi, storyboard/shot list (rekam HP atau prompt generator video AI), teks di layar, teks sulih suara Bahasa Indonesia, caption + hashtag, dan checklist label konten AI. Netral alat, tanpa instalasi. Use for short video script, storyboard, AI video prompt, voice-over, TikTok/Reels/Shorts content plan, AI disclosure checklist, UMKM content.
---

# Studio Video Pendek AI

> **Aturan kerja:** Jangan menginstal paket/aplikasi (mis. `pip install`) — bila perlu, tunjukkan caranya dan biarkan pengguna yang memasang; jangan membuka atau mencari file selain yang diberikan pengguna, isi folder skill ini, dan file yang disebut di langkah kerja; jangan menulis file baru tanpa menyebut lokasinya, dan simpan hasil di folder kerja yang disepakati (bukan /tmp).

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

## Aturan Fakta (WAJIB)
- Sulih suara, teks layar, caption, dan prompt hanya boleh memuat **fakta produk yang disebut pengguna** (bahan, rasa, asal, ukuran, harga, promo, bukti). Jangan menambah sifat/keunggulan ("pilihan", "melimpah", "wangi", "segar", "asli dari ...").
- Fakta kurang: pakai placeholder `[isi: bahan/proses]` (atau `[NAMA PRODUK]`, `[HARGA]`), atau tanyakan sekali. Jangan menebak lalu menulisnya sebagai fakta.
- **Dilarang** menulis bahwa pengguna menyebut/meminta sesuatu bila tidak (mis. "sesuai yang Kakak sebut"). Hapus kalimat seperti itu.
- Catat fakta pengguna (kata-kata pengguna apa adanya) untuk argumen `--fakta`, lalu cek: `python3 <folder-skill-ini>/scripts/cek_fakta.py --teks-file naskah.txt --fakta "<fakta pengguna>"` (Windows: `python`/`py`). GAGAL = hapus klaim atau ganti `[isi: ...]`, jalankan ulang sampai LULUS. Bila script tak bisa dijalankan, periksa manual tiap kalimat terhadap daftar fakta.
- **Cek fakta adalah kerja internal.** Jangan menulis label "Fakta dari pengguna" atau kalimat proses seperti "lolos cek fakta" / "sudah dicek" di balasan; tulis hasilnya saja (naskah bersih + placeholder `[isi: ...]` yang perlu diisi). Fakta yang dipakai cukup muncul wajar di baris Asumsi & Brief.

## Langkah Kerja
1. **Tangkap brief.** Rangkum dalam 3-4 baris: produk, sasaran, satu janji utama (bukan lebih), bukti nyata yang benar-benar dimiliki (bahan, proses, jumlah terjual yang benar, sertifikat yang ada). Jangan mengarang bukti; bila tak ada, pakai demonstrasi proses.
2. **Tentukan durasi & jumlah adegan** (tabel di bawah). Video 15 dtk: **3 adegan** (hook, inti/harga, CTA). 30 dtk: 5-6. 45-60 dtk: 7-9.
3. **Tulis 3 pilihan hook**, masing-masing beda gaya: pertanyaan/masalah, pernyataan berani yang jujur, visual mengejutkan. Beri rekomendasi satu, sertakan alasannya satu kalimat. Lihat pola hook di bawah. **Hook wajib ≤ 3 detik untuk SEMUA durasi: ±6-7 kata tanpa `[jeda]` (7 kata = 2,8 dtk).** Hook jadi adegan 1 dengan rentang 0-3 dtk; hook lebih panjang → potong.
4. **Tulis naskah per adegan** dengan struktur Hook - Masalah/Konteks - Solusi/Produk - Bukti - CTA. Tiap adegan: nomor, rentang waktu, sulih suara, teks di layar. **Teks di layar adegan CTA selalu menyediakan isian `[nomor WA]`** (mis. "Pesan via WA: [nomor WA]"); bila pengguna sudah menyebut nomornya, pakai persis; jangan mengarang nomor. Bukan jualan lewat WA: ganti dengan `[akun/link]`.
5. **Hitung durasi.** Simpan sulih suara per adegan ke berkas teks format `Label | teks` dan jalankan `python3 <folder-skill-ini>/scripts/durasi_naskah.py naskah.txt --target 30` (Windows: `python` atau `py`). `<folder-skill-ini>` = folder tempat SKILL.md ini dibaca (mis. `~/.openclaw/skills/studio-video-pendek-ai`); jangan mencari script ke seluruh komputer (`find /` dsb.) dan jangan memakai salinan script dari folder lain. Jika script tidak bisa dijalankan, hitung manual: **kata / 150 x 60 = detik** (jeda +0,5 dtk per tanda [jeda], +0,3 dtk antar adegan). **Durasi sulih suara harus mendekati target: dalam ±10% (30 dtk -> 27-33 dtk).** Status MELEBIHI: ringkas. Status KEPENDEKAN (di bawah 90% target): tambah adegan/kalimat dari fakta pengguna (bukan klaim baru) atau ubah target video, lalu jalankan script lagi sampai PAS; tulis durasi akhir dari keluaran script. Jika melebihi target, ringkas dulu; jangan menyuruh pengguna bicara lebih cepat dari ±170 kata/menit.
6. **Buat storyboard + shot list** dalam tabel (format di bawah). Untuk tiap adegan berikan **jalur A (rekam HP)** dan/atau **jalur B (prompt alat video AI)** sesuai pilihan pengguna. Bila belum memilih, berikan keduanya singkat. **Pengguna menyebut akan merekam sendiri (HP/kamera) → shot list jalur A WAJIB ada di hasil pertama, termasuk video 15 dtk** (bentuk singkat di Mode Ringkas); jangan ditawarkan belakangan.
7. **Teks sulih suara final** dalam Bahasa Indonesia sehari-hari: kalimat pendek (maks. ±12 kata), tanda `[jeda]`, penekanan dengan HURUF BESAR seperlunya, angka ditulis cara diucapkan ("dua puluh dua ribu rupiah") supaya suara AI/pemilik tidak salah baca.
8. **Caption + hashtag** (format di bawah).
9. **Checklist label & etika** (bagian "Label Konten AI"). Selalu sertakan, sesuaikan dengan jalur produksi yang dipilih.
10. **Cek akhir sebelum menyerahkan:** durasi dalam target; hook ≤ 3 dtk; teks layar CTA memuat `[nomor WA]` (atau nomor dari pengguna); nomor bagian berurutan; tidak ada klaim yang tak bisa dibuktikan atau keunggulan produk yang tidak disebut pengguna (mis. "wangi", "tercepat"); tidak ada wajah/suara orang lain; semua kalimat lolos `cek_fakta.py` dan tidak ada "sesuai yang Kakak sebut" yang tak benar; musik dari perpustakaan platform; harga/promo sama dengan input; teks di layar terbaca (maks. 7 kata per layar).

## Pola Hook (≤ 3 detik, ±6-7 kata)
| Gaya | Contoh (kopi susu) |
|---|---|
| Masalah | "Jam tiga sore, mata udah setengah watt?" |
| Angka jujur | "Kopi susu cuma dua puluh dua ribu." |
| Larangan ringan | "Jangan beli kopi susu sebelum lihat ini." (bukan clickbait bohong; isi harus relevan) |
| Visual | Tuang gula aren cair ke gelas, ASMR, tanpa bicara 2 detik. |
| Penonton spesifik | "Kerja WFH, bosan kopi sachet?" |
Hindari hook yang berjanji sesuatu yang tidak dibuktikan di video.

## Format Output
Keluarkan urut dengan judul bagian tetap ini:

**0. Asumsi & Brief** (2-4 baris kalimat biasa: produk, harga/promo, sasaran, asumsi; tanpa label "Fakta dari pengguna" dan tanpa kalimat "lolos cek fakta")
**1. Pilihan Hook** (3 opsi ≤ 3 dtk + rekomendasi)
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
**7. Langkah Produksi Cepat** (urutan kerja 4-6 langkah; aplikasi edit seperti CapCut/InShot boleh disebut sebagai contoh pilihan, bukan kewajiban, dan pengguna bebas memakai aplikasi lain)

Nomor bagian selalu berurutan tanpa lompat.

**Mode Ringkas (video 15 dtk atau kurang, atau bila pengguna minta cepat):** keluarkan bagian 0 (2 baris), 1 (satu hook terbaik ≤ 3 dtk + satu cadangan), 2 (naskah & timing; 15 dtk = 3 adegan), **3 (Shot List Singkat)**, 4 (sulih suara final), 5 (caption & 3-5 hashtag), dan 6 (checklist label satu baris). Nomor 0-6 berurutan. Hanya bagian 7 dan storyboard lengkap dua jalur yang menunggu permintaan "lengkap"; tawarkan sekali: "Mau versi lengkap dengan storyboard dua jalur dan langkah produksi?"

**Shot List Singkat (bagian 3 Mode Ringkas)** WAJIB di hasil pertama bila pengguna menyebut akan merekam sendiri (HP/kamera) atau tidak menyebut cara produksi (asumsi rekam HP). Bila pengguna memilih alat video AI: satu baris prompt Inggris singkat per adegan. Satu baris per adegan, isi konkret dari fakta pengguna; properti hanya benda yang wajar ada di usaha itu atau diberi `[siapkan: ...]`, bukan klaim produk:

| # | Waktu | Sudut kamera | Properti/objek | Teks di layar |
|---|---|---|---|---|
| 1 | 0-3 dtk | close-up, HP ditopang | (benda yang direkam) | teks hook ≤ 7 kata |

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

## Label Konten AI (ringkasan, dicek ke halaman resmi 2026-09-29)
Ringkasan berikut dicocokkan dengan halaman resmi platform pada 2026-09-29 (rincian, tautan, dan bagian yang belum bisa diverifikasi ada di `references/label-ai.md`); **aturan platform sering berubah**. Tetap minta pengguna memeriksa halaman bantuan resmi sebelum unggah.
- **TikTok:** beri label pada konten realistis yang dibuat/diubah AI (alat label di layar unggah, atau stiker/keterangan). TikTok juga melabeli otomatis lewat metadata C2PA dan efek AI bawaannya. Halaman bantuan TikTok tidak bisa dibaca otomatis; rinciannya dari newsroom resmi.
- **YouTube (Shorts):** aktifkan pengaturan "AI use" di YouTube Studio untuk konten realistis yang bisa disangka nyata. Konten jelas fiksi/tidak realistis dan bantuan naskah/judul tidak perlu; musik buatan AI tercantum sebagai contoh yang perlu diungkap.
- **Instagram/Facebook (Meta):** label "AI info" bisa terpasang otomatis lewat penanda C2PA/IPTC; untuk video/audio realistis buatan AI, pengungkapan mandiri diwajibkan. Nama opsi persisnya di aplikasi belum terverifikasi.
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
- Tidak membuat/mengedit berkas video, tidak menjalankan alat pihak ketiga, tidak memposting. Skill ini tidak berafiliasi dengan alat atau platform mana pun; nama aplikasi/alat hanya sebagai contoh pilihan, bukan kewajiban.
- Bahasa naskah: Indonesia sehari-hari; sesuaikan dialek/logat hanya bila diminta. Bahasa Inggris hanya untuk prompt generator.
- Produk diatur (obat, suplemen, kosmetik, makanan olahan, alkohol, rokok): jangan klaim khasiat; minta nomor izin edar (BPOM/PIRT/halal) hanya jika pengguna sudah memilikinya, dan jangan mengarang nomornya. Arahkan ke aturan platform untuk kategori terbatas.
- Durasi > 60 dtk: jelaskan bahwa skill ini untuk 15-60 dtk; tawarkan memecah jadi seri.
- Angka (harga, diskon, stok) hanya dari pengguna; jangan menebak. Hitung diskon/harga dengan aritmetika biasa dan bulatkan ke rupiah terdekat.
- Produk tidak disebut sama sekali dan pengguna menjawab "lanjut": jangan mengarang produk. Buat naskah dengan penanda [NAMA PRODUK] dan [HARGA] untuk diisi pengguna, dan tulis itu di Asumsi.
- Script memberi PERINGATAN (adegan tanpa kata/hanya emoji, `[jeda abc]`, `--wpm` di luar 80-220): sampaikan ke pengguna dan perbaiki naskahnya; `--wpm` di luar 40-400 ditolak.
- Script gagal / Python tidak ada: hitung manual dengan rumus di Langkah 5 dan sebutkan bahwa itu perkiraan.
- Perkiraan durasi ±10-15%; sarankan pengguna merekam sulih suara lalu mengukur ulang.
- Info ini bukan nasihat hukum; aturan platform dan UU (mis. perlindungan data pribadi, hak cipta) bisa berubah.

## Riwayat versi
- **1.0.5** (2026-10-16): hasil uji bot Telegram asli (sesudah 7,0): Mode Ringkas 15 dtk kini memuat Shot List Singkat (sudut, properti, teks layar) bila pengguna merekam sendiri; hook ≤ 3 dtk (±6-7 kata) semua durasi; 15 dtk = 3 adegan; teks layar CTA berisi `[nomor WA]`; kalimat proses "lolos cek fakta"/label "Fakta dari pengguna" tidak ditulis di balasan; penomoran bagian berurutan.
- **1.0.4** (2026-10-13): rujukan ke skill arsip dihapus dari catatan asal `scripts/cek_fakta.py` (hanya komentar).
- **1.0.3** (2026-10-02): Aturan Fakta (hanya fakta dari pengguna, placeholder, dilarang "sesuai yang Kakak sebut"), `scripts/cek_fakta.py`, durasi sulih suara wajib dalam ±10% target, aplikasi edit hanya contoh pilihan.
- **1.0.2** (2026-09-29): path script `<folder-skill-ini>/scripts/durasi_naskah.py` (tanpa mencari ke seluruh komputer); tidak menambah keunggulan produk yang tidak disebut pengguna; aturan kerja standar (hasil uji OpenClaw 2026.9.6).
- **1.0.1** (2026-09-29): script memperingatkan adegan tanpa kata/hanya emoji dan `[jeda abc]` (bukan angka), memperingatkan `--wpm` di luar 80-220 dan menolak di luar 40-400, kolom tabel tidak melebur untuk angka besar, pesan "KEPENDEKAN" lebih ramah; Mode Ringkas untuk video 15 dtk; `references/label-ai.md` dicocokkan ke halaman resmi (TikTok newsroom, YouTube Help, Meta) per 2026-09-29. Uji regresi 17.
- **1.0.0** (2026-09-29): rilis awal.
