# Contoh alur Telegram: guru minta modul untuk supervisi besok

**Guru (Telegram):** buatkan modul ajar Bahasa Inggris kelas 7 descriptive text hewan peliharaan, buat supervisi besok

**Yang dilakukan agent (urutan):**
1. Mapel, topik, dan kelas sudah jelas, jadi tidak bertanya; asumsi 1 pertemuan x 2 JP dicatat di akhir.
2. Menyusun isi lengkap, lalu mengirimnya di chat berurutan, tanpa ringkasan:
   - "Bagian 1/4 — Modul Ajar" (informasi umum, CP bertanda "cek CP resmi", Tujuan, kegiatan 10+60+10 = 80 menit COCOK, asesmen, diferensiasi)
   - "Bagian 2/4 — LKPD (lembar siswa, tanpa jawaban)"
   - "Bagian 3/4 — Soal + Rubrik"
   - "Bagian 4/4 — Kunci Jawaban (untuk guru)"
3. Karena guru menyebut "supervisi", agent langsung menjalankan `python3 scripts/buat_docx.py` dari file .md sementara (dihapus setelahnya), tanpa bertanya "mau dibuatkan?".
4. Agent melampirkan .docx lewat fitur kirim file Telegram. Bila lampiran tidak bisa dikirim, agent menulis: "File Word tersimpan di <jalur dari output script>; isi lengkapnya sudah ada di pesan di atas."

**Yang TIDAK boleh muncul:** "isi lengkap ada di file .md di workspace", "mau saya buatkan .docx sekarang?", "sudah saya kirim" tanpa konfirmasi, atau file .md modul yang dibiarkan di workspace.
