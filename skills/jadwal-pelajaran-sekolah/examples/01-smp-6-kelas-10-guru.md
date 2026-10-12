# Contoh 1: SMP 6 kelas, 10 guru, Jumat pendek (uji OpenClaw 2026-10-12)

> Data fiktif (`data/kebutuhan-mengajar.csv`, `data/info-sekolah.txt`). Hasil uji sungguhan oleh penguji independen; rincian utuh di `00-openclaw-sebelum-sesudah.md`.

## Masukan pengguna
"Tolong buatkan jadwal pelajaran SMP kami dari file kebutuhan-mengajar.csv dan info-sekolah.txt. Saya mau jadwal per kelas dan per guru, dan jangan sampai ada guru atau kelas yang bentrok. Kalau bisa ada file yang bisa saya cetak."

## Keluaran dengan skill (ringkas)
- Ringkasan: 168/168 JP terjadwal, bentrok 0 (Senin-Kamis 6 jam, Jumat 5 jam, istirahat setelah jam ke-3).
- Tabel kelas 7A dan satu tabel guru (Bu Ani) tampil di chat; 5 kelas lain, 9 guru lain, dan CSV (dipotong "... 168 baris total") hanya di berkas.
- Berkas yang ditulis agent: HTML siap cetak, CSV 168 baris, tabel per kelas/guru (.md).

## Verifikasi independen (python)
168 baris CSV: bentrok guru 0, bentrok kelas 0, jumlah per kegiatan cocok semua (60 kegiatan), tidak ada slot di luar batas. Tabel 7A di chat cocok dengan CSV.

## Catatan
- Jadwal benar tetapi kurang sehat: Matematika 4 JP berturut-turut Senin jam 1-4, IPA 4 jam berturut-turut Jumat; 22 dari 60 kegiatan ditaruh sebagai blok >=3 jam sehari (algoritme greedy berurutan).
- Jadwal tidak utuh di chat; menyebut nama berkas dan "folder workspace" (melanggar larangan isi hasil).
- Konteks Telegram: sama, hanya 7A, 7B, dan Bu Siti di chat; merujuk "file terlampir" yang tidak bisa dikirim; tidak menawarkan "balas 'kirim file'".
