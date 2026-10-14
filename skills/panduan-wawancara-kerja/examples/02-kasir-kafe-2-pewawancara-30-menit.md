# 02 - Kasir kafe, 2 pewawancara, 30 menit

- **Jenis skenario:** normal kedua
- **Diuji:** 2026-10-14, OpenClaw 2026.10.2 lokal, model router Komunitech (claude-sonnet-5), home berisi hanya skill ini. Penguji independen.
- **Nilai:** 8,5. Perbandingan lengkap dengan sisi tanpa skill: `00-openclaw-sebelum-sesudah.md`.

## Input (pesan pengguna, fiktif)

> Buatkan panduan wawancara untuk kasir kafe. Kafe kami kecil di Malang, kasir juga bantu bikin minuman sederhana kalau lagi ramai, pembayaran tunai dan QRIS. Yang mewawancarai 2 orang: saya (pemilik) dan supervisor. Waktunya 30 menit per pelamar.

## Output dengan skill (apa adanya)

> Sudah saya susun paket wawancaranya. Ringkasan asumsi: posisi Kasir Kafe (kafe kecil di Malang, kasir juga membantu racik minuman sederhana saat ramai, pembayaran tunai & QRIS); pewawancara 2 orang — Anda (pemilik) dan supervisor, bergantian memimpin pertanyaan per kompetensi dan mengisi kartu skor masing-masing; durasi 30 menit; satu wawancara utama (tidak bertahap).
>
> ## Kompetensi Inti
>
> 1. **K1 — Ketelitian hitung uang, kas, dan pembayaran tunai/QRIS** (30%, **kritis**) — Menghitung dan menyerahkan uang tunai dengan benar, memverifikasi pembayaran QRIS sebelum menyerahkan pesanan, serta mencatat dan melaporkan selisih sekecil apa pun.
> 2. **K2 — Kecepatan dan multitugas saat ramai, termasuk membantu racik minuman sederhana** (25%) — Tetap akurat melayani transaksi sambil membantu menyiapkan minuman sederhana saat kafe ramai, tanpa menurunkan kualitas layanan atau keamanan kasir.
> 3. **K3 — Layanan pelanggan dan penanganan komplain** (20%) — Melayani dengan sopan, menenangkan, dan menyelesaikan keluhan sesuai kewenangan.
> 4. **K4 — Kejujuran dan tanggung jawab** (15%, **kritis**) — Jujur terhadap uang dan barang kafe, mengakui kesalahan, memegang tanggung jawab yang diberikan.
> 5. **K5 — Kedisiplinan dan kerja sama jadwal** (10%) — Hadir tepat waktu sesuai shift, serah terima kas/area kerja yang rapi, bekerja sama dengan rekan.
>
> ## Alur Wawancara (30 menit)
>
> | Bagian | Menit | Isi |
> |---|---|---|
> | Pembuka dan perkenalan | 3 | Perkenalan, jelaskan kafe dan posisi |
> | Tes praktik | 6 | Bagian A hitung uang + QRIS (3 menit), Bagian B racik minuman sederhana (3 menit) |
> | K1 | 4 | Ketelitian hitung uang & QRIS |
> | K2 | 3 | Kecepatan & multitugas saat ramai |
> | K3 | 3 | Layanan pelanggan |
> | K4 | 3 | Kejujuran & tanggung jawab |
> | K5 | 3 | Kedisiplinan & jadwal |
> | Pertanyaan dari kandidat | 3 | Kandidat bertanya balik |
> | Penutup | 2 | Info langkah berikutnya |
> | **Total** | **30** | |
>
> Saran pembagian peran: satu pewawancara memimpin pertanyaan, satu mencatat dan boleh menambah pertanyaan lanjutan; bergantian memimpin tiap kompetensi. Keduanya mengisi kartu skor **sendiri-sendiri** sebelum berdiskusi.
>
> ## Bank Pertanyaan
>
> **K1 — Ketelitian hitung uang, kas, dan pembayaran tunai/QRIS (30%, kritis)**
> - Perilaku: "Ceritakan satu kali uang atau stok yang Anda pegang tidak cocok dengan catatan, baik tunai maupun non-tunai. Apa kejadiannya, apa yang Anda lakukan, dan bagaimana akhirnya?"
>   Kuat: menyebut nominal selisih, langkah menelusuri (hitung ulang, cek struk/riwayat transaksi), melapor di hari yang sama, ada perubahan kebiasaan sesudahnya. Lemah: "tidak pernah salah", menyalahkan orang lain/sistem, menutup selisih dari uang sendiri tanpa lapor. Lanjut: "Berapa selisihnya, dan siapa yang Anda beri tahu?"
> - Situasional: "Pelanggan bayar QRIS dan menunjukkan bukti bayar di HP-nya, tapi notifikasi pembayaran belum masuk ke aplikasi kasir, sementara antrean mulai mengular. Apa yang Anda lakukan?"
>   Kuat: tetap tenang, minta pelanggan tunggu sebentar, cek ulang riwayat/mutasi, tidak menyerahkan pesanan sebelum pembayaran terkonfirmasi, melibatkan atasan bila berlarut, menjelaskan dengan sopan. Lemah: langsung percaya tanpa cek, menyerahkan pesanan begitu saja, atau marah ke pelanggan. Lanjut: "Kalau ternyata memang belum masuk, apa langkah Anda berikutnya?"
>
> **K2 — Kecepatan dan multitugas saat ramai, termasuk membantu racik minuman sederhana (25%)**
> - Perilaku: "Ceritakan satu kali Anda harus mengerjakan dua hal sekaligus (misalnya melayani kasir sambil diminta membantu pekerjaan lain). Bagaimana Anda mengaturnya, dan apa hasilnya?" (pelamar belum pernah bekerja boleh cerita dari magang/sekolah/usaha keluarga)
>   Kuat: menyebut cara mengatur prioritas, minta bantuan saat perlu, tetap selesai tepat waktu, hasil nyata. Lemah: "jadi berantakan semua" tanpa cara mengatasi, atau mengaku tidak pernah menghadapi situasi semacam itu sama sekali. Lanjut: "Mana yang Anda dahulukan, dan mengapa?"
> - Situasional: "Kafe sedang ramai, 4 pelanggan mengantre di kasir, dan barista sendirian kewalahan membuat 3 pesanan es kopi susu. Supervisor minta Anda bantu membuat satu pesanan sebentar. Apa yang Anda lakukan dengan antrean kasir?"
>   Kuat: memberi tahu antrean akan sebentar, menyelesaikan transaksi yang sedang berjalan dulu, cepat bantu racik lalu kembali ke kasir, tidak membiarkan laci kasir tanpa pengawasan. Lemah: meninggalkan kasir begitu saja tanpa bilang apa-apa, atau menolak membantu tanpa alasan. Lanjut: "Bagaimana Anda memastikan laci kasir tetap aman saat membantu di area minuman?"
>
> **K3 — Layanan pelanggan dan penanganan komplain (20%)**
> - Perilaku: "Ceritakan satu pelanggan yang kecewa atau komplain kepada Anda. Apa yang terjadi, dan apa yang Anda lakukan?"
>   Kuat: mendengarkan sampai selesai, minta maaf tanpa menyalahkan, solusi dalam kewenangan, meneruskan ke atasan bila di luar wewenang. Lemah: berdebat, menyalahkan pelanggan. Lanjut: "Kalimat pertama apa yang Anda ucapkan ke pelanggan itu?"
> - Situasional: "Pelanggan komplain minumannya 'kurang manis dari biasanya' padahal dibuat sesuai takaran standar oleh rekan Anda. Apa yang Anda lakukan?"
>   Kuat: minta maaf atas ketidaknyamanan, menawarkan solusi sesuai kebijakan `[isian: kebijakan komplain rasa minuman]`, tidak menyalahkan rekan di depan pelanggan, menyampaikan ke rekan/atasan setelahnya. Lemah: membantah pelanggan, mengabaikan. Lanjut: "Kalau pelanggan tetap tidak puas, apa langkah selanjutnya?"
>
> **K4 — Kejujuran dan tanggung jawab (15%, kritis)**
> - Perilaku: "Ceritakan satu kesalahan Anda di pekerjaan/kegiatan yang merugikan orang lain. Apa yang Anda lakukan setelah sadar?"
>   Kuat: mengaku sendiri, menyebut kerugian apa adanya, memperbaiki. Lemah: menyembunyikan, menyalahkan sistem, "saya tidak pernah salah". Lanjut: "Siapa yang pertama Anda beri tahu?"
> - Situasional: "Anda melihat rekan kerja beberapa kali mengambil kue/minuman tanpa membayar untuk dirinya sendiri. Apa yang Anda lakukan?"
>   Kuat: menegur langsung dengan sopan, bila berulang melapor ke atasan, tidak ikut-ikutan. Lemah: mengabaikan, ikut, atau bergosip tanpa melapor. Lanjut: "Kalau teguran Anda tidak digubris, apa langkah berikutnya?"
>
> **K5 — Kedisiplinan dan kerja sama jadwal (10%)**
> - Perilaku: "Ceritakan satu kali jadwal Anda berubah mendadak atau rekan tidak bisa hadir. Apa yang Anda lakukan?"
>   Kuat: mengabari lebih awal, menawarkan solusi, menepati. Lemah: menghindar, mengeluh tanpa tindakan. Lanjut: "Siapa yang Anda hubungi lebih dulu?"
> - Situasional: "Anda dijadwalkan shift sore tapi akan terlambat 20 menit karena kendala di jalan. Apa yang Anda lakukan?"
>   Kuat: mengabari atasan/rekan sedini mungkin, memberi perkiraan waktu tiba. Lemah: diam sampai tiba. Lanjut: "Apa yang Anda lakukan supaya kejadian ini tidak sering terulang?"
>
> **Tes praktik (6 menit, bahan contoh, diumumkan sebagai tes)**
> - Bagian A (3 menit, tanpa kalkulator, lisan+tulis): hitung kembalian 2 transaksi tunai, lalu jawab 1 skenario QRIS.
>   1. Belanja Rp23.500 (kopi susu Rp18.000 + roti Rp5.500), bayar tunai Rp50.000, kembali **Rp26.500**.
>   2. Belanja Rp41.000 (2x es teh @Rp12.500 = Rp25.000 + kopi hitam Rp16.000), bayar tunai Rp50.000, kembali **Rp9.000**.
>   3. (Lisan) "Pelanggan menunjukkan notifikasi pembayaran QRIS Rp35.000 di HP-nya, tapi aplikasi kasir belum menampilkan pembayaran masuk. Apa yang Anda lakukan sebelum menyerahkan pesanan?" Kunci: tidak menyerahkan sebelum konfirmasi, cek ulang, minta waktu ke pelanggan, melibatkan atasan bila lebih dari `[isian: X menit]`.
> - Bagian B (3 menit, praktik): minta pelamar menyiapkan satu minuman sederhana dari bahan contoh (mis. kopi sachet + es + gula sesuai takaran `[isian: resep standar kafe]`) sambil diajak ngobrol santai layaknya melayani pelanggan. Amati kebersihan tangan/alat, kesesuaian takaran, kecepatan wajar, tetap ramah sambil bekerja.
> - Penilaian: Bagian A menilai K1 (benar semua termasuk langkah QRIS yang tepat = 5; satu kurang tepat = 3; dua atau lebih kurang tepat/langsung menyerahkan tanpa cek = 1-2). Bagian B menilai K2.
>
> ## Rubrik Skor 1-5
>
> **K1 — Ketelitian hitung uang & QRIS**
> 1 = salah hitung kembalian tunai sederhana, atau langsung percaya bukti bayar QRIS tanpa mengecek. 2 = benar bila tidak buru-buru tapi tidak terbiasa cek ulang; mengecek QRIS hanya kadang-kadang. 3 = menghitung tunai benar dengan sedikit koreksi, selalu cek notifikasi QRIS sebelum menyerahkan pesanan, melapor selisih bila ditemukan. 4 = cepat dan akurat, konsisten mengecek QRIS tiap transaksi, melapor selisih tepat di hari yang sama. 5 = seperti 4, ditambah punya kebiasaan kerja sendiri yang terbukti mengurangi kesalahan.
>
> **K2 — Kecepatan & multitugas saat ramai**
> 1 = kewalahan, sering salah transaksi atau abai keamanan kasir saat diminta bantu hal lain. 2 = bisa membantu tapi perlu diarahkan terus, kadang lupa memberi tahu antrean. 3 = tetap bekerja benar saat ramai, bisa membantu racik minuman dengan arahan singkat. 4 = mengatur prioritas sendiri, memberi kabar ke antrean, menjaga kasir tetap aman sambil membantu. 5 = seperti 4, ditambah cara kerja rapi yang membuat area tetap teratur meski ramai, bisa menyebut hasil nyata.
>
> **K3 — Layanan pelanggan & komplain**
> 1 = defensif, membalas pelanggan, tidak ada solusi. 2 = merespons sopan tapi ragu bertindak tanpa diarahkan. 3 = sopan, menyelesaikan keluhan umum sesuai kebijakan, tahu kapan memanggil atasan. 4 = menenangkan lebih dulu, menawarkan solusi jelas, pelanggan puas. 5 = seperti 4, ditambah mencatat penyebab supaya tidak terulang.
>
> **K4 — Kejujuran & tanggung jawab**
> 1 = menyembunyikan kesalahan atau membenarkan tindakan mengambil barang tanpa bayar. 2 = jujur hanya bila ditanya langsung, enggan melapor hal yang melibatkan rekan. 3 = jujur bila ditanya, melapor kesalahan besar. 4 = melapor sendiri tanpa ditanya, memperbaiki kerugian. 5 = seperti 4, ditambah konsisten menjaga aturan walau tidak diawasi dan berani menegur rekan.
>
> **K5 — Kedisiplinan & jadwal**
> 1 = sering terlambat tanpa kabar. 2 = kadang terlambat, mengabari hanya sesekali. 3 = hadir sesuai jadwal, mengabari bila berhalangan. 4 = konsisten tepat waktu, serah terima kas/area tertulis dan rapi. 5 = seperti 4, ditambah membantu menutup jadwal rekan yang berhalangan.
>
> ## Kartu Skor (satu per kandidat per pewawancara, isi sendiri-sendiri sebelum diskusi)
>
> - Posisi: Kasir Kafe | Tanggal: `[isian]` | Kode & nama panggilan kandidat: `[isian: C1, ...]` | Pewawancara: `[isian: nama]`
>
> | Kompetensi (bobot) | Skor 1-5 | Bukti singkat |
> |---|---|---|
> | K1 Ketelitian uang & QRIS (30%, kritis) | ___ | |
> | K2 Kecepatan & multitugas (25%) | ___ | |
> | K3 Layanan pelanggan (20%) | ___ | |
> | K4 Kejujuran & tanggung jawab (15%, kritis) | ___ | |
> | K5 Kedisiplinan & jadwal (10%) | ___ | |
>
> Tes praktik: `[isian: hasil Bagian A & B]` | Syarat dasar (ya/tidak, tidak dinilai): bersedia shift/akhir pekan `[isian: jadwal kafe]`
>
> 5 aturan pakai: (1) pertanyaan sama untuk semua kandidat; (2) catat bukti/kata-kata nyata, bukan kesimpulan; (3) skor sendiri-sendiri dulu, baru dibandingkan dengan pewawancara lain; (4) skor 1 atau 5 wajib satu kalimat bukti; (5) hal pribadi yang disebut kandidat sendiri tidak dicatat dan tidak memengaruhi skor.
>
> ## Pertanyaan yang Tidak Boleh Ditanyakan
>
> | Jangan tanyakan | Ganti dengan |
> |---|---|
> | Status menikah, rencana menikah/hamil, punya anak | "Kafe kami butuh shift bergilir termasuk akhir pekan `[isian: jadwal]`. Apakah jadwal itu bisa Anda penuhi rutin?" |
> | Agama, suku, asal daerah | "Berapa lama perjalanan Anda ke lokasi kerja, dan bisa tiba tepat waktu?" |
> | Usia/tanggal lahir | "Apakah Anda sudah berusia minimal 18 tahun?" (boleh, sebatas memastikan batas usia kerja) |
> | Kesehatan/disabilitas yang tidak terkait tugas | "Pekerjaan ini mengharuskan berdiri cukup lama dan sesekali mengangkat beban ringan. Apakah Anda mampu, dengan atau tanpa penyesuaian?" |
> | Penampilan, tinggi/berat badan, media sosial pribadi | "Kafe kami memakai standar kerapian seragam `[isian: aturan]`. Apakah Anda bersedia mengikutinya?" |
>
> Dasar: berlaku per 14 Oktober 2026. UU 13/2003 jo. UU 6/2023 Pasal 5-6 (kesempatan & perlakuan sama tanpa diskriminasi) dan SE Menaker M/6/HK.04/V/2025 (larangan syarat diskriminatif dalam rekrutmen); UU 27/2022 PDP untuk data pelamar. Ringkasan umum, bukan nasihat hukum — **PERLU REVIEW**: nomor pasal belum dicocokkan ke naskah resmi.
>
> ## Setelah Wawancara
> Kirim skor tiap pewawancara (Anda dan supervisor) ke saya, nanti saya hitung rata-rata per kompetensi, total, selisih penilaian yang perlu dibahas, dan ringkasan saran per kandidat — keputusan akhir tetap di Anda.
>
> **Asumsi yang saya pakai:** 1 wawancara utama (tidak bertahap), 2 pewawancara bergantian memimpin per kompetensi, bahan tes praktik bukan untuk dijual.
>
> Tiga hal yang perlu Anda lengkapi:
> 1. Resep/takaran minuman sederhana yang biasa dipakai untuk Bagian B tes praktik (mis. kopi susu gula aren, teh, dll)?
> 2. Kebijakan komplain rasa minuman kafe Anda (ganti gratis / racik ulang) untuk jawaban kuat di K3?
> 3. Jadwal shift/akhir pekan yang berlaku, untuk ditulis di kartu skor sebagai syarat dasar?

## Catatan penguji
- Kompetensi disesuaikan ke kasir yang juga meracik minuman dan menerima QRIS (bukan salinan mentah bank kasir).
- Angka diverifikasi: alur 3+6+4+3+3+3+3+3+2 = 30 menit (sama dengan pembagian script); Rp18.000 + Rp5.500 = Rp23.500, kembali Rp26.500; 2 x Rp12.500 + Rp16.000 = Rp41.000, kembali Rp9.000. Benar.
- Fakta yang tidak diberikan (resep, kebijakan komplain rasa, jadwal shift) ditulis `[isian]` dan ditanyakan di akhir (3 pertanyaan).
- Kekurangan: 3 menit per kompetensi dan tes 6 menit sangat padat; aturan "perilaku dulu, situasional bila perlu" tidak disebut.
- Nilai 8,5 vs tanpa skill 6,0.
