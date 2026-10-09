# 09 - Data rusak & galat (listmonk 6.2.0 asli)
| Kasus | Hasil |
|---|---|
| CSV kosong / acak biner / tanpa kolom email | GALAT jelas, kode 3 |
| CSV `;` dengan email `z@@x`, kutip tak tertutup, spasi | valid 2, buang 3 (benar) |
| Latin-1 | terbaca |
| `.xlsx` palsu / `.xls` / berkas tak ada | pesan jelas kode 3 |
| `.xlsx` bom-entitas XML | terhenti aman (batas amplifikasi Python) TAPI keluar Traceback mentah, bukan pesan ramah |
| Token salah / pengguna salah | kode 5 "Ditolak 403", token tidak tercetak (grep 0) |
| Tanpa akun | kode 3 |
| Server mati (port salah) | kode 4 pesan awam |
| `http://example.com` / `https://example.com` tanpa izin | kode 2 |
| Server web lain bukan listmonk | kode 7 "Tidak ditemukan" (pesan kurang jelas) |
| Duplikat, email tidak valid | dibuang & dihitung |
| hapus-pelanggan tanpa/ dengan `--ya`, dua kali, `%` | ditahan / terhapus / "tidak ada" / "tidak ada" |
| nama list ambigu | kode 7 minta ID |
