# Hasil uji: sunting-tulisan-jelas

- **Tanggal:** 2026-10-05
- **Penguji:** agent penguji independen Komunitech (bukan pembuat), hanya membaca folder skill
- **Cara uji:** OpenClaw 2026.9.6 lokal, model router Komunitech `claude-sonnet-5` (sama dengan bot member), skill dimatikan vs aktif, home bersih per skenario, ditambah 1 jalan konteks kanal Telegram (tanpa kirim). Rincian dan balasan utuh ada di `00-openclaw-sebelum-sesudah.md`.
- **platform_teruji yang boleh ditulis:** `openclaw (uji otomatis agent)`

## Skor kualitas: 8/10

Alasan:
- **Kekuatan:** skill benar-benar terpakai (`read` + `exec`), dan angka keterbacaan di balasan sama persis dengan script yang dijalankan ulang penguji. Di skenario normal, semua angka, tanggal, alasan, dan nada permintaan utuh. Ada ringkasan perubahan, tabel ukuran nyata, asumsi pembaca, dan tanpa kata proses. Di skenario jebakan, klaim BPOM, 10.000 pelanggan, dan garansi 2 tahun ditolak dengan alasan dan tawaran memakai bukti. Tulisan tetap disunting tanpa satu klaim pun ditambahkan. Tanpa skill, model menambah khasiat kosmetik karangan ("samarkan tampilan pori", "menenangkan kulit").
- **Kekurangan:** pembeda di tugas inti (merapikan email) tipis. Tanpa skill pun model menghasilkan email yang jelas dan lebih ringkas. Di konteks Telegram, rincian isi ("lewat telepon", alasan jadwal) hilang padahal diklaim maksudnya tidak berubah. Ringkasan perubahan skenario 2 menyebut satu perubahan yang tidak terjadi ("berkualitas" masih ada).
- **Uji sebelum/sesudah OpenClaw:** rata-rata 6,25 → 8,5 (selisih +2,25). **VERDIK: LULUS** (sesudah ≥ 8, selisih ≥ 1,5, tanpa kesalahan fakta di SESUDAH). Catatan: selisih di skenario normal hanya +1,5. Nilai jualnya adalah menjaga isi dan menolak klaim karangan, bukan kalimat yang jauh lebih bagus.

## Cacat (untuk pembuat)
1. Langkah catat fakta (3) dan periksa fakta (5) perlu memasukkan alasan/sebab dan saluran komunikasi. Bila dibuang, wajib disebut di "Yang saya ubah" (terlihat di konteks Telegram).
2. Tulis eksplisit bahwa angka yang tersirat dari daftar (mis. "3 item" menjadi 3 butir) boleh hilang hanya bila disebut.
3. Cocokkan setiap poin "Yang saya ubah" dengan hasil akhir.
4. Klaim kabur yang tersisa ("bahan pilihan berkualitas") diberi `[cek: ...]` atau disebut.
