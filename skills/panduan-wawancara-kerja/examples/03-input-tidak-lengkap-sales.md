# 03 - Input tidak lengkap: "bikinin pertanyaan interview buat sales"

- **Jenis skenario:** input tidak lengkap
- **Diuji:** 2026-10-14, OpenClaw 2026.10.2 lokal, model router Komunitech (claude-sonnet-5), home berisi hanya skill ini. Penguji independen.
- **Nilai:** 8,5. Perbandingan lengkap dengan sisi tanpa skill: `00-openclaw-sebelum-sesudah.md`.

## Input (pesan pengguna, fiktif)

> bikinin pertanyaan interview buat sales

## Output dengan skill (apa adanya)

> # Paket Wawancara — Sales / Customer Service
>
> **Asumsi:** posisi Sales/CS (melayani calon pembeli, closing, dan tindak lanjut lewat WhatsApp/telepon/tatap muka), 2 pewawancara (satu memimpin, satu mencatat), durasi 45 menit, satu tahap wawancara utama. Target penjualan dan jadwal kerja ditandai `[isian: ...]` — sebutkan kalau ada data pastinya biar saya sesuaikan.
>
> ## 1. Kompetensi Inti
>
> 1. **K1 – Komunikasi dan membangun kepercayaan (25%)** — memahami kebutuhan pelanggan lewat pertanyaan, lalu menjelaskan solusi dengan bahasa sederhana dan jujur.
> 2. **K2 – Menangani keberatan dan menutup penjualan (25%)** — menerima keberatan (harga, waktu, ragu) dengan tenang dan mengarahkan ke keputusan tanpa tekanan tidak wajar.
> 3. **K3 – Ketekunan tindak lanjut dan target (20%)** — menindaklanjuti calon pelanggan secara teratur dan tetap bekerja menuju target.
> 4. **K4 – Pengetahuan produk dan kemauan belajar (15%)** — cepat memahami produk dan aturan usaha, serta jujur bila belum tahu lalu mencari jawabannya.
> 5. **K5 – Etika dan kejujuran (15%, kritis)** — tidak memberi janji, harga, atau informasi yang tidak benar demi menutup penjualan.
>
> ## 2. Alur Wawancara (45 menit)
>
> | Bagian | Menit | Isi |
> |---|---|---|
> | Pembuka dan perkenalan | 5 | Sapa, jelaskan posisi dan alur wawancara |
> | Tes praktik | 10 | Role-play keberatan harga + tulis balasan komplain |
> | K1 | 5 | Pertanyaan perilaku + situasional |
> | K2 | 5 | Pertanyaan perilaku + situasional |
> | K3 | 5 | Pertanyaan perilaku + situasional |
> | K4 | 4 | Pertanyaan perilaku + situasional |
> | K5 | 4 | Pertanyaan perilaku + situasional |
> | Pertanyaan dari kandidat | 5 | Kandidat bertanya balik |
> | Penutup | 2 | Jelaskan langkah selanjutnya |
> | **Total** | **45** | |
>
> ## 3. Bank Pertanyaan
>
> **K1 Komunikasi dan membangun kepercayaan (25%)**
> > Perilaku: "Ceritakan satu kali Anda berhasil meyakinkan pelanggan yang awalnya ragu. Apa yang Anda tanyakan dan jelaskan?"
> > Kuat: bertanya kebutuhan dulu sebelum menawar, menyesuaikan penjelasan dengan kebutuhan itu, ada hasil jelas (closing/jadwal lanjut). Lemah: langsung menyebut harga/promo tanpa menggali kebutuhan. Lanjut: "Pertanyaan apa yang pertama kali Anda ajukan ke pelanggan itu?"
> > Situasional: "Calon pembeli bertanya, 'Bedanya produk ini dengan yang lebih murah apa?' (produk: [isian])." Kuat: bertanya kebutuhan, menjelaskan perbedaan nyata, tidak menjelekkan pesaing. Lemah: menjelekkan pesaing atau menjawab 'yang ini lebih bagus' tanpa alasan. Lanjut: "Kalau pelanggan tetap memilih yang murah, apa yang Anda katakan selanjutnya?"
>
> **K2 Menangani keberatan dan menutup penjualan (25%)**
> > Perilaku: "Ceritakan satu kali pelanggan bilang 'terlalu mahal' atau 'nanti dulu'. Apa jawaban Anda dan apa hasilnya?"
> > Kuat: mencari alasan sebenarnya di balik keberatan, menawarkan opsi sesuai kewenangan, hasil terukur. Lemah: langsung memotong harga sendiri, atau menyerah begitu saja. Lanjut: "Berapa kali Anda menghubunginya lagi setelah itu, dan lewat apa?"
> > Situasional (role-play 4 menit, bagian tes praktik): pewawancara jadi pelanggan, "Harganya Rp350.000, di toko sebelah Rp300.000." Amati: bertanya dulu alasan perbandingan, menegaskan nilai (garansi/layanan), menawarkan opsi, mengajak keputusan, tidak berbohong. Lemah: berbohong soal stok/garansi, menekan berlebihan, atau memotong harga di luar wewenang.
>
> **K3 Ketekunan tindak lanjut dan target (20%)**
> > Perilaku: "Ceritakan target yang pernah Anda kejar — di pekerjaan, sekolah, atau kegiatan lain. Berapa targetnya, apa yang Anda lakukan, dan berapa hasilnya?"
> > Kuat: menyebut angka target dan hasil, kebiasaan tindak lanjut (daftar, jadwal), ada perbaikan ketika meleset. Lemah: tidak ingat angka, menyalahkan keadaan/pasar sepenuhnya. Lanjut: "Bagaimana Anda mencatat siapa yang harus dihubungi lagi?"
> > Situasional: "Target bulan ini `[isian: angka target]`, tapi baru tercapai 40% ketika sisa waktu tinggal seminggu. Apa rencana Anda?" Kuat: menganalisis penyebab, menyusun daftar prospek terdekat, tindak lanjut terjadwal, minta bantuan bila perlu. Lemah: pasrah, atau jalan pintas tidak jujur (mengubah catatan).
>
> **K4 Pengetahuan produk dan kemauan belajar (15%)**
> > Perilaku: "Ceritakan satu hal baru yang harus Anda pelajari cepat — di pekerjaan, sekolah, atau kegiatan lain. Bagaimana Anda mempelajarinya?"
> > Kuat: cara belajar yang konkret, ada waktu dan hasilnya. Lemah: hanya menunggu diajari orang lain. Lanjut: "Berapa lama Anda butuh sampai cukup percaya diri memakainya?"
> > Situasional: "Pelanggan menanyakan fitur produk yang Anda sendiri belum tahu jawabannya. Apa yang Anda lakukan saat itu juga?" Kuat: jujur mengaku belum tahu, mencari ke sumber yang benar, kembali dengan jawaban dalam waktu yang dijanjikan. Lemah: mengarang jawaban asal.
>
> **K5 Etika dan kejujuran (15%, kritis)**
> > Perilaku: "Ceritakan satu kali Anda harus menolak atau mengoreksi permintaan pelanggan atau atasan karena tidak sesuai kenyataan."
> > Kuat: menyampaikan dengan sopan, tetap menawarkan alternatif yang jujur. Lemah: sikap 'yang penting laku' tanpa pertimbangan. Lanjut: "Bagaimana reaksi orang yang Anda koreksi itu?"
> > Situasional: "Atasan menyuruh Anda mengatakan stok tinggal 2 supaya pelanggan cepat membeli, padahal stoknya masih banyak. Apa yang Anda lakukan?" Kuat: tidak berbohong ke pelanggan, menyampaikan keberatan dengan sopan ke atasan, menawarkan promo yang nyata sebagai gantinya. Lemah: menurut saja tanpa pertimbangan.
>
> **Tes praktik (maks. 10 menit, bahan contoh, diumumkan sebagai tes)**
> - Role-play keberatan harga (4 menit) — lihat K2 di atas.
> - Tulis balasan WhatsApp (6 menit): pelanggan komplain "barang datang penyok" (data fiktif: nomor pesanan `[isian]`, foto diterima). Kriteria jawaban kuat: menyapa, minta maaf, meminta bukti seperlunya, menawarkan penggantian/pengembalian sesuai kebijakan `[isian: kebijakan retur]`, memberi waktu tindak lanjut, tanpa janji di luar kebijakan.
> - Penilaian: role-play menilai K2 dan K5; tulisan menilai K1.
>
> ## 4. Rubrik Skor 1–5
>
> **K1 Komunikasi dan membangun kepercayaan**
> 1 — Menjawab satu arah, terkesan memaksa, tidak menggali kebutuhan.
> 2 — Sesekali bertanya kebutuhan tapi penjelasan masih umum/template.
> 3 — Ramah, bertanya kebutuhan dasar, menjelaskan produk dengan benar.
> 4 — Menggali kebutuhan dengan cukup dalam, penjelasan disesuaikan dengan jawaban pelanggan.
> 5 — Menggali kebutuhan secara alami, menjelaskan sesuai bahasa pelanggan, menunjukkan cara membangun hubungan jangka panjang.
>
> **K2 Menangani keberatan dan menutup penjualan**
> 1 — Menyerah begitu saja atau menekan pelanggan secara berlebihan.
> 2 — Menjawab keberatan tapi tidak menggali alasan, hasil tidak jelas.
> 3 — Menjawab keberatan umum dengan sopan, ada usaha menutup.
> 4 — Menggali alasan keberatan, menawarkan opsi yang relevan dan jujur.
> 5 — Menggali alasan, menawarkan opsi sesuai wewenang, menutup dengan langkah jelas tanpa berbohong.
>
> **K3 Ketekunan tindak lanjut dan target**
> 1 — Tidak punya cara mengejar target, menyalahkan keadaan.
> 2 — Menghubungi pelanggan sesekali tanpa pola yang jelas.
> 3 — Rutin menghubungi dan mencatat secara sederhana.
> 4 — Punya sistem tindak lanjut dengan jadwal, ada bukti hasil.
> 5 — Sistem tindak lanjut jelas, hasil dengan angka nyata, memperbaiki cara kerja saat target meleset.
>
> **K4 Pengetahuan produk dan kemauan belajar**
> 1 — Mengarang jawaban saat tidak tahu.
> 2 — Mengaku tidak tahu tapi tidak mencari jawabannya kembali.
> 3 — Bertanya bila tidak tahu, kembali dengan jawaban.
> 4 — Punya cara belajar yang cukup terstruktur, jawaban akurat.
> 5 — Kebiasaan belajar terstruktur, bisa mengajari rekan, membuat catatan jawaban yang sering ditanya.
>
> **K5 Etika dan kejujuran**
> 1 — Bersedia berbohong demi penjualan.
> 2 — Ragu-ragu, cenderung ikut arahan yang kurang jujur bila didesak.
> 3 — Jujur ke pelanggan, tapi ragu mengoreksi atasan.
> 4 — Jujur konsisten, cukup berani menyampaikan keberatan ke atasan.
> 5 — Konsisten jujur, berani mengoreksi dengan cara sopan, menawarkan alternatif yang sah.
>
> ## 5. Kartu Skor (cetak satu per kandidat per pewawancara)
>
> | Kompetensi (bobot) | Skor 1-5 | Bukti singkat |
> |---|---|---|
> | K1 Komunikasi dan membangun kepercayaan (25%) | ___ | |
> | K2 Menangani keberatan dan closing (25%) | ___ | |
> | K3 Ketekunan tindak lanjut dan target (20%) | ___ | |
> | K4 Pengetahuan produk dan kemauan belajar (15%) | ___ | |
> | K5 Etika dan kejujuran (15%, kritis) | ___ | |
>
> Posisi: Sales/CS | Tanggal: `[isian]` | Kode kandidat & nama panggilan: `[isian: C1, ...]` | Pewawancara: `[isian: nama]`
> Tes praktik: `[isian: hasil role-play + hasil tulisan]`
> Syarat dasar (ya/tidak, tidak dinilai skor): bersedia mencapai target `[isian: target]`
>
> **5 aturan pakai:**
> 1. Pertanyaan sama persis untuk semua kandidat posisi ini.
> 2. Catat bukti (kata-kata/tindakan nyata), bukan kesimpulan.
> 3. Isi skor sendiri-sendiri dulu, baru diskusi dengan pewawancara lain.
> 4. Skor 1 atau 5 wajib disertai satu kalimat bukti.
> 5. Hal pribadi yang disebut kandidat (status, agama, dll.) tidak dicatat di kartu ini.
>
> ## 6. Pertanyaan yang Tidak Boleh Ditanyakan
>
> | Jangan tanyakan | Ganti dengan |
> |---|---|
> | Status menikah, rencana menikah/punya anak, rencana hamil | "Pekerjaan ini `[isian: ada shift/lembur?]`. Apakah jadwal itu bisa Anda penuhi secara rutin?" |
> | Agama, pandangan politik | Tidak ditanyakan sama sekali; cukup tanyakan jadwal kerja dan kesediaannya |
> | Suku, ras, asal daerah | "Berapa lama perjalanan Anda ke lokasi kerja, dan apakah bisa tiba tepat waktu?" |
> | Usia, tanggal lahir | "Berapa tahun pengalaman yang relevan dengan penjualan/CS?" (boleh memastikan usia minimal 18 tahun bila perlu) |
> | Kesehatan/disabilitas yang tidak terkait tugas | Jelaskan tuntutan tugas nyata lalu tanyakan kemampuan menjalankannya, ke semua kandidat |
> | Penampilan, tinggi/berat badan | "Pekerjaan ini memakai standar kerapian `[isian]`. Apakah Anda bersedia mengikutinya?" |
> | Pekerjaan pasangan, kondisi keluarga | Tidak ada padanan; tidak relevan |
> | Media sosial pribadi | Tidak ditanyakan; bila relevan (portofolio), minta kandidat menunjukkan sendiri |
>
> **Dasar aturan** (ringkasan umum, berlaku per 14 Oktober 2026): UU 13/2003 tentang Ketenagakerjaan jo. UU 6/2023 (Cipta Kerja) Pasal 5–6 (kesempatan dan perlakuan sama tanpa diskriminasi), SE Menaker M/6/HK.04/V/2025 (larangan syarat diskriminatif dalam rekrutmen), dan UU 27/2022 tentang Pelindungan Data Pribadi (data pelamar dikumpulkan seperlunya untuk tujuan yang diketahui pelamar). **PERLU REVIEW**: nomor pasal di atas belum dicocokkan ke naskah resmi — ini bukan nasihat hukum.
>
> ## 7. Setelah Wawancara
>
> Kalau sudah ada hasil wawancara dari beberapa kandidat, kirim skor tiap pewawancara ke saya (pakai format kartu skor di atas) dan saya hitung peringkat, rata-rata per kompetensi, titik yang perlu dibahas (selisih penilaian antar pewawancara), dan ringkasan rekomendasi per kandidat.
>
> **Asumsi yang saya pakai:** 2 pewawancara, durasi 45 menit, satu tahap wawancara. Tiga hal yang perlu dikonfirmasi:
> 1. Berapa target penjualan dan jadwal kerja yang berlaku untuk posisi ini?
> 2. Produk/jasa apa yang dijual, supaya pertanyaan situasional dan tes bisa disesuaikan?
> 3. Mau wawancara dibagi beberapa tahap (HRD lalu pemilik), atau satu kali saja seperti di atas?

## Catatan penguji
- Kerjakan dulu dengan asumsi yang disebut (2 pewawancara, 45 menit, satu tahap), lalu tepat 3 pertanyaan di akhir (target & jadwal, produk, tahap).
- Angka diverifikasi: alur 5+10+5+5+5+4+4+5+2 = 45 menit. Benar.
- Target, kebijakan retur, nomor pesanan ditulis `[isian]`; tidak ada fakta karangan.
- Catatan: isi banyak mengikuti bank kompetensi apa adanya (wajar untuk input sependek ini).
- Nilai 8,5 vs tanpa skill 5,5 (tanpa skill: daftar pertanyaan umum tanpa rubrik/kartu skor).
