---
name: sunting-tulisan-jelas
description: Menyunting tulisan kerja apa pun agar jelas, ringkas, dan mudah dipahami pembaca awam, yaitu email ke klien, pengumuman karyawan, deskripsi produk, panduan kerja, pesan WhatsApp ke pelanggan, dan laporan ke atasan. Memecah kalimat panjang, membuang kata pengisi dan jargon, mengubah langkah jadi daftar, menaruh inti di awal, tanpa mengubah fakta, angka, atau janji. Hasil berupa versi suntingan utuh, ringkasan perubahan, dan angka keterbacaan sebelum/sesudah. Gunakan saat pengguna minta sunting, perjelas, ringkas, rapikan tulisan, "kalimatnya kepanjangan", "bahasanya bikin pusing", jargon, edit for clarity, plain language, clear writing, simplify this email.
---

# Sunting Tulisan Jelas

> **Aturan kerja:** Jangan menginstal paket/aplikasi (mis. `pip install`) — bila perlu, tunjukkan caranya dan biarkan pengguna yang memasang; jangan membuka atau mencari file selain yang diberikan pengguna, isi folder skill ini, dan file yang disebut di langkah kerja; jangan menulis file baru tanpa menyebut lokasinya, dan simpan hasil di folder kerja yang disepakati (bukan /tmp).

## Tujuan
Mengubah tulisan kerja yang bertele-tele atau penuh istilah rumit menjadi tulisan yang dipahami pembaca awam dalam sekali baca. Isi tidak berubah; yang berubah cara menyampaikannya. Hasilnya langsung bisa ditempel atau dikirim.

## Kapan digunakan
- "Tolong rapikan email ini ke klien, kepanjangan."
- "Karyawan saya nggak ngerti pengumuman ini, tolong sederhanakan."
- Menyunting deskripsi produk, panduan untuk karyawan, pesan WA ke pelanggan, laporan ke atasan, proposal singkat, postingan pengumuman.
- Pengguna menempel tulisan lalu menulis "sunting", "perjelas", "ringkas", "buat lebih gampang dipahami", atau versi Inggrisnya.

## Kapan TIDAK digunakan
- Membuat surat resmi lengkap dengan format kop/nomor → pakai `surat-resmi`. Skill ini hanya menyunting isinya bila sudah ada draf.
- Menyusun SOP dari nol → `sop-writer`.
- Menghilangkan ciri tulisan buatan AI (pembuka klise, penutup "semoga bermanfaat") → `tulisan-tanpa-kesan-ai`. Dua skill ini boleh dipakai berurutan.
- Kontrak, perjanjian, dan teks hukum: kata-katanya sengaja baku; jangan disunting selain menandai bagian yang sulit dipahami.
- Menambah klaim, angka, testimoni, atau janji yang tidak ada di tulisan asli (lihat Batasan).
- Menulis dari nol tanpa draf, tulisan kreatif (puisi, cerita), dan menerjemahkan.

## Input
| Info | Wajib? | Bila tidak diberikan |
|---|---|---|
| Tulisan yang mau disunting | Ya | Minta ditempel (satu kalimat). Jangan mengarang isinya. |
| Pembaca | Tidak | Anggap pelanggan atau karyawan awam |
| Tujuan (minta persetujuan, memberi tahu, menjual, mengajari) | Tidak | Simpulkan dari isi tulisan |
| Nada | Tidak | Sopan sehari-hari, mengikuti nada tulisan asli |
| Batas panjang | Tidak | Sependek mungkin tanpa menghilangkan fakta |

**Kerjakan dulu, tanya di akhir.** Jangan menahan hasil demi bertanya. Sunting dengan asumsi di atas, sebutkan asumsinya satu kalimat, lalu tutup dengan maksimal 3 pertanyaan singkat dalam satu pesan. Satu-satunya alasan menunda adalah bila tulisannya belum ada.

## Langkah kerja
1. **Tetapkan pembaca dan tujuan.** Tulis di kepala: siapa yang membaca, apa yang harus mereka ketahui atau lakukan setelah membaca. Ini menentukan apa yang paling penting dan harus berada di depan.
2. **Ukur tulisan asli.** Simpan tulisan ke berkas teks sementara bila perlu, lalu jalankan:
   ```bash
   python3 <folder-skill-ini>/scripts/ukur_keterbacaan.py --file asli.txt
   ```
   (Windows: `python` atau `py`.) Bila Python tidak bisa dijalankan, hitung kira-kira sendiri: jumlah kalimat, kalimat lebih dari 25 kata, dan kata pengisi. Hasil ukuran hanya penanda kasar, bukan nilai mutu. Jangan menyebut angka yang tidak Anda ukur atau hitung.
3. **Catat fakta yang tidak boleh berubah**: semua angka, tanggal, jam, harga, nama orang/usaha, nomor, janji, syarat, dan tenggat. Bila ragu apakah sesuatu fakta, anggap fakta.
4. **Sunting dengan daftar periksa berikut** (rinciannya, termasuk pasangan sebelum/sesudah, ada di `references/prinsip-sunting.md`):
   - **Inti di depan.** Kalimat pertama berisi kabar atau permintaan utama. Sapaan dan konteks menyusul seperlunya.
   - **Satu kalimat, satu gagasan.** Sasaran rata-rata 18 kata atau kurang; pecah kalimat di atas 25 kata. Pecahan tidak boleh kehilangan hubungan sebab-akibat.
   - **Pelaku jelas.** Tulis "siapa melakukan apa". Pakai bentuk pasif ("di-") hanya bila pelakunya memang tidak penting atau tidak diketahui.
   - **Kata konkret.** Ganti "segera", "dalam waktu dekat", "berbagai macam" dengan tanggal, jam, atau contoh yang SUDAH ada di tulisan. Bila datanya tidak ada, jangan menebak: tandai `[cek: ...]`.
   - **Buang kata pengisi dan jargon** memakai `references/kata-pengisi-jargon.txt` sebagai penanda. Kata yang memang dibutuhkan pembaca boleh tetap ada.
   - **Satu istilah untuk satu benda**, jangan bergantian ("aplikasi", "sistem", "platform" untuk hal yang sama). Singkatan atau istilah yang tidak dikenal pembaca awam dijelaskan sekali di tempat pertama muncul. Ganti "hal tersebut"/"itu" dengan nama bendanya bila bisa salah tafsir.
   - **Langkah jadi daftar bernomor** (urutan penting). **Kumpulan hal setara jadi daftar butir.** Daftar didahului satu kalimat pengantar, butirnya sejajar bentuknya.
   - **Paragraf pendek** (maksimal 3-5 kalimat), satu topik, kalimat pertama merangkum isi paragraf. Untuk WhatsApp: baris pendek, satu pokok per baris, tanpa dinding teks.
   - **Permintaan harus terlihat**: siapa diminta melakukan apa, sampai kapan.
5. **Periksa fakta.** Bandingkan daftar fakta langkah 3 dengan hasil suntingan. Tidak boleh ada yang hilang, bertambah, atau bergeser maknanya (mis. "diharapkan" jadi "wajib", "sekitar" jadi pasti). Klaim yang mencurigakan (mutu terbaik, "tanpa pengawet", khasiat, garansi, sertifikat) tetap dipertahankan jika ada di tulisan asli, tetapi diberi `[cek: ...]` bila tampak belum terbukti. Jangan menghapus klaim diam-diam; sebutkan di ringkasan bila dibuang karena hanya kata muluk.
6. **Ukur hasil dan banding** dengan:
   ```bash
   python3 <folder-skill-ini>/scripts/ukur_keterbacaan.py --sebelum asli.txt --sesudah suntingan.txt
   ```
   Keluaran ini juga mencantumkan angka/tanggal yang hilang atau baru. Bila ada yang hilang tanpa alasan, perbaiki suntingan. Bila angka kalimat >25 kata masih ada, sunting lagi.
7. **Tulis balasan** sesuai format di bawah.

## Format output
Balasan memakai bahasa sehari-hari. Jangan menyebut kata proses seperti script, file, path, berkas, dijalankan, atau LULUS di balasan.

```
**Versi suntingan**
<tulisan LENGKAP, siap tempel atau kirim>

**Yang saya ubah**
- <3 sampai 5 poin, yang paling berdampak saja>

**Ukuran keterbacaan**
| | Sebelum | Sesudah |
|---|---|---|
| Jumlah kata | .. | .. |
| Rata-rata kata per kalimat | .. | .. |
| Kalimat lebih dari 25 kata | .. | .. |
| Kata pengisi/jargon/kabur | .. | .. |

Asumsi saya: <pembaca, nada>. <Hapus tanda [cek: ...] sebelum dikirim, bila ada.>
Pertanyaan (maks. 3): 1) ... 2) ...
```
- Versi suntingan SELALU utuh di balasan, bukan "ada di berkas".
- Tabel hanya memuat angka yang benar-benar terukur atau dihitung. Bila tidak bisa diukur, tulis "perkiraan" atau hilangkan tabelnya; jangan mengarang.
- Tulisan yang sudah jelas: katakan terus terang dan ubah seminimal mungkin. Jangan mengutak-atik demi terlihat bekerja.
- Pertanyaan dibuang jika memang tidak ada yang perlu ditanyakan.

## Contoh
Contoh lengkap dengan angka ada di `examples/` (email ke klien, pengumuman karyawan, deskripsi produk, tulisan kurang konteks, permintaan di luar cakupan). Satu cuplikan:

Sebelum: "Sehubungan dengan adanya keterlambatan bahan dari supplier, dengan ini kami sampaikan bahwa pengiriman akan dilakukan pada 17 Oktober 2026."
Sesudah: "Pengiriman mundur ke 17 Oktober 2026 karena bahan dari pemasok terlambat."

## Batasan & penanganan error
- **Isi tidak boleh hilang diam-diam:** alasan, syarat, cara kontak (mis. "lewat telepon"), dan konteks jadwal dipertahankan; bila ada yang dipangkas, sebutkan di ringkasan perubahan. Ringkasan perubahan hanya menyebut yang benar-benar diubah (jangan klaim kata diganti bila masih ada).
- **Tidak mengubah fakta, angka, nama, harga, tanggal, dan janji.** Bila tulisan asli saling bertentangan (mis. dua tanggal berbeda untuk hal yang sama), jangan memilih salah satu: tandai `[cek: ...]` dan tanyakan.
- **Tidak mengarang klaim.** Permintaan "bikin lebih meyakinkan" dilayani dengan memperjelas fakta yang ada, bukan menambah angka pelanggan, sertifikat, testimoni, kelangkaan, atau urgensi baru. Tolak bagian yang mengarang dengan sopan, jelaskan alasannya (merugikan pembeli dan nama usaha), lalu tawarkan memasukkannya bila pengguna punya buktinya. Tetap kerjakan sisa suntingan.
- **Tidak menjanjikan hasil bisnis** (mis. "pasti lebih laku", "pasti dibalas").
- **Teks kosong, hanya emoji, atau hanya angka**: minta pengguna menempelkan tulisannya.
- **Berkas Word/PDF/gambar**: skill ini bekerja pada teks; minta isinya ditempel, atau salin sendiri teksnya bila berkasnya terbaca sebagai teks biasa.
- **Tulisan sangat panjang (di atas sekitar 1.500 kata)**: sunting per bagian dalam beberapa balasan, mulai dari bagian yang paling penting, dan katakan bagian mana yang sudah selesai. Ukur per bagian.
- **Tulisan sangat pendek (di bawah 15 kata)**: tetap sunting; sebutkan bahwa angka keterbacaannya kurang berarti.
- **Tulisan berbahasa Inggris atau campuran**: prinsipnya sama; sunting dalam bahasa aslinya. Daftar kata pengisi hanya untuk Bahasa Indonesia, jadi penilaian kata pengisi Inggris cukup manual.
- **Bahasa daerah, slang, dan nada akrab yang disengaja** (mis. pesan ke pelanggan setia) dipertahankan; yang diperbaiki hanya yang membuat bingung.
- **Domain sensitif** (kesehatan, hukum, pajak, keuangan): sunting kejelasannya saja, jangan menyederhanakan sampai maknanya bergeser; bila istilah teknis tidak boleh dihapus, jelaskan dalam kurung.
- Ukuran dari script adalah **penanda kasar** (sasaran: rata-rata 18 kata atau kurang; tidak ada kalimat di atas 25 kata kecuali yang memang harus utuh). Daftar kata hanya penanda, bukan larangan. Penilaian akhir tetap pada pembaca.
- Menyunting tulisan akademik atau tugas agar lolos detektor AI **bukan** fungsi skill ini.
- Skill ini tidak mengirim apa pun ke luar komputer pengguna dan tidak menyimpan tulisan.
