# Riwayat perubahan — kanboard-papan-kerja

Catatan teknis per versi (dipindah dari README agar halaman pembeli ringkas).

## Riwayat versi
- **1.0.6 (2026-10-02):** templat balasan saat token tertempel di chat memakai path relatif resmi `scripts/kanboard.py` (dijalankan dari dalam folder skill); agent dilarang menebak path seperti `~/.openclaw/...`.
- **1.0.5 (2026-10-02):** revisi kecil pada aturan token yang tertempel: pekerjaan pengguna tidak ditahan. Bila permintaan bisa dijawab dengan kunci yang sudah tersimpan (mis. pratinjau), hasilnya ditampilkan dulu tanpa mengulang token, baru di akhir jawaban agent menyarankan mengganti token yang sempat ditempel.
- **1.0.4 (2026-10-02):** aturan baru di SKILL.md: bila pengguna menempel kunci/token/password di chat, agent tidak boleh menulis ulang satu karakter pun darinya (tidak utuh, tidak awalan, tidak disamarkan), memakai templat balasan baku, dan token dianggap sudah bocor. Ditambah uji regresi.
- **1.0.3 (2026-10-02):** "Aturan konfirmasi perubahan" yang tidak bisa dilewati: setiap perubahan (pindah/ubah/tutup/hapus kartu, tambah kartu, buat papan) selalu lewat pratinjau lalu "ya" di pesan terpisah, walau pengguna berkata "langsung kerjain" atau "gak usah nanya". Agent dilarang menambahkan `--ya` pada panggilan pertama; perintah ubah tanpa `--ya` hanya menampilkan pratinjau. Ditambah uji regresi.
- **1.0.2 (2026-10-01):** petunjuk lokasi script ditambahkan di SKILL.md: script ada di subfolder `scripts/` di folder skill; agent dilarang mencari script atau file pengguna ke seluruh disk (mis. `find /`). Sebelumnya (30 Sep, setelah uji ulang 8/10) ditambahkan catatan zona waktu: bila zona waktu profil pengguna API Kanboard berbeda dari zona waktu aplikasi, tenggat bisa bergeser beberapa jam, jadi samakan keduanya dan cocokkan satu kartu dengan layar Kanboard.
- **1.0.1 (2026-09-30):** pembacaan jam bahasa Indonesia diperbaiki ("jam 3 sore" = 15:00, "10.00" = 10:00; jam 1-6 tanpa keterangan ditanyakan); tanggal tanpa tahun yang sudah lewat kini diberi PERINGATAN (tidak diam-diam ke tahun depan); kartu di kolom Selesai tidak muncul di "hari ini"; pesan ramah (tanpa traceback) untuk data aneh dari server; "kemarin" dikenali; pencocokan PIC sebagian ditegaskan.
- **1.0.0:** rilis awal.
