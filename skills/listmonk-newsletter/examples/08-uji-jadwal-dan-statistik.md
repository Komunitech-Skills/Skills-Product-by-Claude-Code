# 08 - Normal 3: jadwal + statistik (listmonk 6.2.0 asli)
- `jadwal --waktu "besok pagi"` -> kode 2; waktu lampau -> kode 2; "2026-13-45 25:99" -> kode 2.
- `jadwal 3 --waktu "2026-10-05 09:00" --tz WIB` tanpa `--ya` ditahan; dengan `--ya --konfirmasi-penerima 3` -> status `scheduled`, send_at `2026-10-05T02:00:00Z` (WIB benar). `batalkan` jadwal -> kembali draf. `jeda` tanpa `--ya` ditahan.
- Setelah kampanye #4 terkirim, satu piksel + satu klik disimulasikan: `statistik 4 --tautan` -> Terkirim 3 dari 3; Dibuka 1 = 33,3%; Klik 1 = 33,3%; klik/buka 100,0%; tautan wa.me terdaftar. Cocok hitungan manual. Catatan "dibuka = perkiraan" tampil.
