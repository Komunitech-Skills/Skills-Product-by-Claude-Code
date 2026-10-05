# Contoh alur Telegram: guru minta modul untuk supervisi besok

**Guru (Telegram):** buatkan modul ajar Bahasa Inggris kelas 7 descriptive text hewan peliharaan, buat supervisi besok

**Yang dilakukan agent (urutan):**
1. Mapel, topik, dan kelas sudah jelas, jadi tidak bertanya; asumsi 1 pertemuan x 2 JP dicatat di akhir.
2. Membaca SKILL.md sekali, tanpa web fetch, lalu menulis balasan RINGKAS tetapi utuh (±4.000-6.000 karakter) dalam satu pesan: modul ajar ringkas (info umum, CP rujukan + kolom tempel, 2-3 TP, tabel kegiatan 10+60+10 = 80 menit COCOK, asesmen singkat), LKPD maks. 6 soal tanpa jawaban, rubrik ringkas, "Kunci Jawaban (untuk guru)". Contoh bentuknya: `09-format-ringkas-telegram.md`.
3. Karena guru menyebut "supervisi", SETELAH isi chat selesai agent menjalankan `python3 scripts/buat_docx.py` sekali dari file .md sementara (dihapus setelahnya), tanpa bertanya "mau dibuatkan?".
4. Agent menulis HANYA: "File Word: <jalur persis dari output script>". Tidak ada kata "lampirkan/terkirim" kecuali alat kirim file benar-benar dipanggil dan berhasil. Bila script gagal, file tidak disebut.

**Yang TIDAK boleh muncul:** "isi lengkap ada di file .md di workspace", "mau saya buatkan .docx sekarang?", "sudah saya kirim/lampirkan" tanpa alat kirim file, "File tersimpan di jalur di atas" tanpa jalur, balasan belasan ribu karakter (4 bagian) yang membuat model macet, atau file .md modul yang dibiarkan di workspace.
