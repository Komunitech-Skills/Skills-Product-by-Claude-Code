# Contoh alur Telegram: guru minta modul untuk supervisi besok

**Guru (Telegram):** buatkan modul ajar Bahasa Inggris kelas 7 descriptive text hewan peliharaan, buat supervisi besok

**Yang dilakukan agent (urutan):**
1. Mapel, topik, dan kelas sudah jelas, jadi tidak bertanya; asumsi 1 pertemuan x 2 JP dicatat di akhir.
2. Membaca SKILL.md sekali, tanpa web fetch, lalu menulis balasan RINGKAS tetapi utuh (±4.000-6.000 karakter) dalam satu pesan: modul ajar ringkas (info umum, CP rujukan + kolom tempel, 2-3 TP, tabel kegiatan 10+60+10 = 80 menit COCOK, asesmen singkat), LKPD maks. 6 soal tanpa jawaban, rubrik ringkas, "Kunci Jawaban (untuk guru)". Contoh bentuknya: `09-format-ringkas-telegram.md`.
3. Walau guru menyebut "supervisi", agent TIDAK membuat .docx dan TIDAK melampirkan file otomatis di giliran pertama.
4. Balasan ditutup kalimat baku: "Isi lengkap sudah ada di atas. Kalau perlu file Word, balas 'kirim file' — saya coba lampirkan." Tidak ada kata "terlampir/di bawah/sudah dikirim" dan tidak ada jalur file.
5. Hanya setelah guru membalas "kirim file": agent menjalankan `python3 scripts/buat_docx.py` sekali (file .md sementara dihapus), lalu memanggil alat kirim file kanal. Tulis "File Word terlampir." HANYA bila alat itu mengembalikan sukses; bila gagal, katakan jujur file tidak bisa dikirim dari sini dan sarankan menempel isi chat ke Word. Di kanal CLI/IDE jalur file dari output script boleh disebut.

**Yang TIDAK boleh muncul:** "isi lengkap ada di file .md di workspace", "mau saya buatkan .docx sekarang?", "sudah saya kirim/lampirkan" tanpa alat kirim file, jalur file lokal seperti "File Word: /tmp/..." di Telegram, "File tersimpan di jalur di atas" tanpa jalur, balasan belasan ribu karakter (4 bagian) yang membuat model macet, atau file .md modul yang dibiarkan di workspace.
