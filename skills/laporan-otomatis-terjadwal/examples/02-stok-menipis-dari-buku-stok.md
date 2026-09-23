# 02 — Pengingat stok menipis harian (sumber: buku-stok)

**Skenario:** S2 (normal). Seller sudah memakai skill `buku-stok` (database `~/KomunitechData/stok.db`). Dua produk di bawah stok minimum.

**Input pengguna (persis):**
> ingetin saya stok yang mau abis tiap hari jam 7 pagi ya ke telegram (chat id 123456789). saya udah pake buku stok

## Mengikuti resep apa adanya (`templates/RESEP-stok-menipis.md`)
Resep meminta CSV stok di folder + `cek_sumber_data.py`, lalu memfilter `stok <= ambang` sendiri ("Tidak ada script hitung khusus"). Agent perlu membuat CSV dulu dari buku-stok:
```bash
python3 ../buku-stok/scripts/stok.py laporan menipis --csv laporan/masuk/stok/stok-menipis.csv
python3 scripts/cek_sumber_data.py --folder laporan/masuk/stok --pola "stok*.csv" --label stok --maks-umur-hari 2
```
**Masalah (diuji):** pada hari tanpa produk menipis, CSV hanya berisi judul kolom → `cek_sumber_data.py` menjawab `"siap": false` — *"hanya berisi judul kolom... Laporan TIDAK dibuat"*. Padahal resep sendiri menyatakan "tidak ada yang menipis" adalah hasil valid yang harus dilaporkan. Selain itu, jadwal harus tetap menjalankan ekspor CSV setiap pagi (langkah yang tidak ada di resep).

## Alur yang dipakai penguji (disarankan untuk revisi resep)
```bash
python3 ../buku-stok/scripts/stok.py info --json              # DB ada? mutasi_terakhir untuk umur data
python3 ../buku-stok/scripts/stok.py laporan menipis --json   # hanya baca
python3 scripts/susun_pesan.py --data pesan-stok.json
```

## Output

**Balasan agent (contoh pertama + konfirmasi):**
````
Buku stok Anda terbaca (6 produk aktif, transaksi terakhir 23 Sep 2026 18:08).
Contoh pesan yang akan masuk ke Telegram Anda setiap jam 07:00:

*Stok Menipis*
Kamis, 24 Sep 2026, 07:00 WIB

Jumlah produk menipis: 2

*Produk menipis*
- Kaos Polos Cotton 30s - Hitam L -- sisa 8 -- ambang 10 -- habis +-20 hari
- Mug Keramik 350ml - Putih -- sisa 9 -- ambang 10 -- habis +-90 hari

⚠️ Data stok dari buku-stok, transaksi terakhir dicatat 23 Sep 2026 18:08.

Jadwal: setiap hari 07:00 WIB -> Telegram 123456789. Lanjut? (ya/tidak)
````
Setelah "ya":
```bash
openclaw automations add "0 7 * * *" \
  "Pakai skill buku-stok: jalankan 'stok.py laporan menipis --json' (HANYA BACA, jangan jalankan perintah tulis atau --ya). Susun pesan 'Stok Menipis' maksimal 15 baris: jumlah produk menipis, lalu daftar 'Nama -- sisa X -- ambang Y', paling kritis dulu, maksimal 10. Kalau tidak ada yang menipis, tulis 'Tidak ada produk menipis hari ini'. Kalau database stok tidak ditemukan, katakan itu -- JANGAN kirim angka nol." \
  --name "Stok menipis harian" --tz "Asia/Jakarta" --session isolated \
  --announce --channel telegram --to "123456789"
```

## Catatan penguji
- Angka dari `laporan menipis --json` diverifikasi: HT-L terjual 12 dalam 30 hari → 0,4/hari → 8/0,4 = 20 hari; MUG 3/30 = 0,1/hari → 9/0,1 = 90 hari. Benar.
- Resep **perlu diperbarui** untuk memakai `stok.py laporan menipis --json` langsung (sekaligus memberi rata-rata laku & perkiraan habis yang tidak ada di resep CSV), memakai `stok.py info --json` (`mutasi_terakhir`) sebagai pengganti `cek_sumber_data.py`, dan menyebut bahwa buku-stok **tidak** menyimpan CSV sendiri. Tabel Langkah 1 SKILL.md juga menyebut "Perhitungan sendiri (script skill ini)" padahal skill ini tidak punya script stok.
- Kanal Telegram default, penerima pemilik sendiri, tanpa data pelanggan — sesuai.
