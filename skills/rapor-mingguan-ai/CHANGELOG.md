# Riwayat perubahan — rapor-mingguan-ai

Catatan teknis per versi (dipindah dari README agar halaman pembeli ringkas).

## Catatan revisi 1.0.3 (2026-10-27)
Perbaikan dari temuan pra-cek konteks Telegram sebelumnya (draf revisi awal hilang karena container direset; dibangun ulang dari 1.0.2):
- **Nama pelanggan tidak boleh muncul di mana pun**, termasuk bagian asumsi dan pertanyaan (sebelumnya model sempat menulis nama pelanggan di pertanyaan). Pelanggan disebut "pelanggan di P3". Nama setelah "a/n" / "atas nama" ikut disamarkan; nomor HP di contoh hitungan kini ditutup penuh `[nomor]` (sebelumnya masih menyisakan 4 digit akhir). Kode percakapan yang ditulis dengan nama (mis. "P3 (Sari)") dipotong jadi "P3".
- **Pemeriksaan draf sebelum kirim** (`--cek-balasan`, langkah 11 SKILL.md): panjang ≤ 3.800 karakter, baris terakhir "Balas 'rinci'", tabel maks. 3 kolom dengan satu baris pemisah yang benar, baris "Angka tren (tempel minggu depan)" ada dan sama dengan hitungan, tanpa nama/inisial/nomor pelanggan, tanpa nama berkas/skrip/skill, persen tiap kriteria dan jumlah percakapan bersih sama dengan hitungan.
- **Rapor minggu lalu cukup ditempel apa adanya** (`--lama-jawaban`): dibaca dari baris "Angka tren", tabel, butir, atau kalimat ("fakta 100%, ingat konteks 85%"). Setiap rapor kini selalu memuat baris "Angka tren (tempel minggu depan)".
- **Persen mengikuti data**: contoh format ringkas (`examples/06`) diganti ke data klinik dengan persen yang berbeda-beda (sebelumnya semua kriteria 90%, berisiko disalin model). SKILL.md menegaskan angka tidak boleh disalin dari contoh.
- Batas balasan pertama: target ±3.000, batas keras 3.800 karakter (sebelumnya 3.000).
- Kinerja: daftar "gagal di" dan dugaan diringkas pada data besar; 2.000 penilaian + 1.500 percakapan berkas + cek draf selesai jauh di bawah 10 detik (diuji).
- Putaran 2 (temuan pemeriksa independen):
  - Rapor lama yang menulis jumlah sebelum persen ("Fakta: 10 dari 12 (83,3%)", "Konteks: 11/12 (91,7%)") kini terbaca benar (sebelumnya terbaca 10% / 11%, tren keliru tanpa peringatan). "a dari b" tanpa persen dihitung jadi persen. Label yang artinya gagal ("fakta salah 16,7%", "tidak nyambung", "janji berlebihan") tidak dipakai sebagai persen lolos dan diberi peringatan.
  - Kode percakapan bernama panjang ("P2 (Ibu Sari Wulandari)=fakta") tidak lagi membuat percakapan itu terbuang dari hitungan; pesan peringatan tidak mengulang nama; nama/inisial dari kode P ikut diperiksa di draf.
  - Pemeriksaan draf: menandai nama tanpa sapaan di pola umum ("Apakah Hendra ...", "keluhan Hendra (P4)") dan inisial di depan kode P ("H. (P4)"). Ini heuristik: nama di luar pola itu tetap hanya tertangkap bila diberikan lewat daftar nama atau berkas percakapan, jadi disiplin langkah 1/11 tetap perlu.
  - Positif palsu dikurangi: nama usaha setelah a/n ("a/n Klinik ...") dan nomor rekening usaha setelah kata "rekening" (kecuali nomor itu muncul di pesan pelanggan) tidak ditandai; persen di kalimat ringkasan/tren ("naik dari 90% ke 100%") tidak lagi dibaca sebagai angka minggu ini; baris tabel/butir ganda yang berbeda tetap tertangkap. Langkah 11 dibatasi maks. 3 kali cek ulang.
  - "x dari n" percakapan bersih dicocokkan sebagai angka utuh ("17 dari 120" tidak lagi dianggap "7 dari 12").
  - Pembulatan persen kini setengah ke atas (13/16 = 81,25 → 81,3), sama dengan hitung manual; sebelumnya pembulatan bawaan Python bisa memberi 81,2 (masalah lama sejak 1.0.2).
  - Checklist "tren" diselaraskan: kalimat naik/turun hanya bila ada rapor lama, baris "Angka tren" tetap selalu ada.
- Putaran 3 (temuan pemeriksa independen; masih di versi 1.0.3 karena versi ini belum dirilis/di-commit, jadi tidak dinaikkan lagi):
  - **Sedang:** pemeriksaan draf keliru menandai "percakapan bersih 'x dari n' belum tertulis" bila angkanya diikuti titik/koma ("bersih 7 dari 12, nilai umum C."). Batas angka kini: titik/koma boleh, kecuali diikuti digit (desimal). Perbaikan yang sama untuk pembacaan rapor lama ("Fakta: 10 dari 12." dan "Fakta = 90." sebelumnya tidak terbaca). Pencocokan tetap angka utuh ("17 dari 120", "7 dari 120", "1,7 dari 12" tidak dianggap "7 dari 12"); tes contoh 06 juga memakai batas angka utuh, bukan pencarian potongan teks.
  - Nama marketplace/layanan (Shopee, Tokopedia, Lazada, Gojek, Grab, Bpjs, dll.) tidak lagi ditandai sebagai kemungkinan nama pelanggan dan tidak ikut terbaca sebagai nama dari percakapan.
  - Nama tanpa sapaan di percakapan tempelan ("Kak, ini Yuni", "dengan Dimas") kini terbaca otomatis untuk pemeriksaan draf (langkah 11 tetap mewajibkan agent mendaftar nama sendiri).
  - `--nilai -` (stdin) dan `--nilai @berkas.txt`: daftar penilaian sangat panjang tidak lagi gagal karena batas panjang baris perintah (±128 KB Linux, jauh lebih kecil di Windows).
  - Dokumen diselaraskan: referensi tidak lagi menyuruh menulis "pelanggan A" (kini "pelanggan di P3"); README tidak lagi menyebut v1.0.2 sebagai versi terkini; contoh 01 ditulis ulang ke format 1.0.3 (tabel 3 kolom, baris "Angka tren", penutup "Balas 'rinci'", kalimat penjelas bila semua kriteria sama persen, peringatan agar angka tidak disalin; lolos pemeriksaan draf); contoh 02-03 diberi tanda FORMAT LAMA dan nama skill bertanda hubung di hasil contoh 02 diganti bahasa awam.
- Tes: 25 → 61 (regresi per aturan dan per temuan di atas, termasuk tes yang membaca SKILL.md/referensi/README untuk aturan lama yang bertentangan). Jujur: belum dipra-cek ulang dengan konteks Telegram dan belum diuji di bot.

## Catatan revisi 1.0.2 (2026-10-16)
Perbaikan dari pra-cek dengan pengaturan kanal Telegram (penguji independen, versi 1.0.1):
- **Angka rapor selalu benar dan saling cocok.** Sebelumnya jumlah percakapan "bersih" bisa dikira (pada data contoh tertulis 5 dari 10, seharusnya 4). Sekarang AI menulis dulu penilaian tiap percakapan, lalu semua angka (persen tiap kriteria dan percakapan bersih) dihitung dari penilaian itu: lewat skrip bila komputer bisa menjalankan Python, atau dengan rumus tetap bila tidak. Sebelum menulis, AI wajib mencocokkan angka: percakapan bersih tidak boleh melebihi angka lolos terendah, dan angka di ringkasan, tabel, serta teks harus sama. Bila semua kriteria kebetulan sama persen, rapor memberi satu kalimat penjelas.
- **Rapor ringkas untuk chat.** Balasan pertama paling banyak 3.000 karakter (batas satu pesan Telegram 4.096): tabel 3 kolom pendek atau daftar berbutir, PR maksimal 3 kalimat per butir, keputusan maksimal 3 butir. Rincian per percakapan dan cara cek tiap PR dikirim bila pengguna membalas "rinci".
- **Tanpa nama skill teknis di hasil.** Skill lain disebut dengan bahasa awam (mis. "pemeriksaan privasi bot"), bukan nama bertanda hubung.
- Aturan privasi diseragamkan: nomor pelanggan tidak ditulis sama sekali di rapor, termasuk 4 digit akhir.
- Skrip: pilihan baru `--nilai "P1=lolos; P2=nyambung,panjang"` (tanpa perlu berkas), baris "cek konsistensi", daftar percakapan yang gagal per kriteria, persen bergaya Indonesia (83,3%); penilaian yang kosong atau salah ketik tidak lagi dihitung "lolos". Tes unit ditambah (25 tes). Contoh format ringkas baru: `examples/06-format-ringkas-chat.md`.

## Catatan revisi 1.0.1 (2026-10-06)
- Revisi dari uji OpenClaw (skor 4,75 naik ke 8,25): urutan tetap pada "3 kesalahan teratas" dan PR minggu ini: kriteria kritis (salah fakta, janji yang tidak bisa ditepati, bocor data pribadi) selalu didahulukan dan masing-masing jadi butir terpisah; nada atau panjang hanya mengisi sisa kuota. PR wajib menutup kesalahan kritis dulu.
- Privasi: nama, inisial, dan potongan nomor pelanggan (termasuk 4 digit terakhir) tidak ditulis di rapor, diganti "pelanggan A/B". PR berisi fakta usaha hanya dari info yang diberikan pengguna (selain itu `[isian]`); nama berkas internal tidak disebut ke pengguna.

## Catatan revisi 1.0.0 (2026-10-06)
- Rilis awal (status uji).
