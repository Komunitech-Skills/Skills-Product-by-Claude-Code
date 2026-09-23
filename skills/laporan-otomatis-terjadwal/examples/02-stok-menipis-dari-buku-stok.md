# 02 — Pengingat stok menipis harian dari buku-stok (uji ulang v1.1.0)

**Skenario:** S2 (normal). Seller sudah memakai skill `buku-stok` (database `~/KomunitechData/stok.db`), dan dua produk di bawah stok minimum.

**Input pengguna (persis):**
> ingetin saya stok yang mau abis tiap hari jam 7 pagi ya ke telegram (chat id 123456789). saya udah pake buku stok

**Perintah yang dijalankan agent (jalur utama `templates/RESEP-stok-menipis.md` v1.1.0, hanya baca):**
```bash
python3 ../buku-stok/scripts/stok.py info --json              # ok: true, mutasi_terakhir 2026-09-23 18:13
python3 ../buku-stok/scripts/stok.py laporan menipis --json   # jumlah: 2
python3 scripts/susun_pesan.py --data pesan-stok.json         # exit 0
```

## Output

**Balasan agent (contoh pertama + konfirmasi):**
````
Buku stok Anda terbaca (transaksi terakhir 23 Sep 2026 18:13).
Contoh pesan yang akan masuk ke Telegram Anda setiap jam 07:00:

*Stok Menipis*
Kamis, 24 Sep 2026, 07:00 WIB
Jumlah produk menipis: 2
*Produk menipis*
- Kaos Polos Cotton 30s - Hitam L -- sisa 8 -- ambang 10 -- habis ~20 hari
- Mug Keramik 350ml - Putih -- sisa 9 -- ambang 10 -- habis ~90 hari
Data stok dari buku-stok, transaksi terakhir dicatat 23 Sep 2026 18:13.

Kalau suatu hari tidak ada yang menipis, Anda tetap menerima "Jumlah produk menipis: 0 —
Tidak ada produk menipis hari ini" (kabar baik, bukan error).
Jadwal: setiap hari 07:00 WIB -> Telegram 123456789. Jadwal ini hanya boleh MEMBACA buku stok. Lanjut? (ya/tidak)
````
Setelah "ya":
```bash
openclaw automations add "0 7 * * *" \
  "Pakai skill buku-stok: jalankan 'stok.py info --json' lalu 'stok.py laporan menipis --json' (HANYA BACA, jangan jalankan --ya atau perintah tulis). Susun pesan 'Stok Menipis' maksimal 15 baris: jumlah produk menipis, lalu daftar 'Nama -- sisa X -- ambang Y -- habis ~Z hari', paling kritis dulu, maksimal 10. Kalau jumlah 0, tulis 'Tidak ada produk menipis hari ini'. Kalau database stok tidak ditemukan, katakan itu -- JANGAN kirim angka nol." \
  --name "Stok menipis harian" --tz "Asia/Jakarta" --session isolated --tools exec,read \
  --announce --channel telegram --to "123456789"
```

**Kasus "tidak ada yang menipis" (diuji pada database lain):** `laporan menipis --json` → `"jumlah": 0`; pesan:
```
*Stok Menipis*
Kamis, 24 Sep 2026, 07:00 WIB
Jumlah produk menipis: 0
Tidak ada produk menipis hari ini.
Data stok dari buku-stok, transaksi terakhir dicatat 23 Sep 2026 18:31.
```

## Catatan penguji
- v1.1.0 memperbaiki cacat S-3 uji pertama: resep kini memakai `stok.py info` + `laporan menipis --json` langsung, `jumlah: 0` diperlakukan sebagai kabar baik (tidak lagi berhenti di "hanya berisi judul kolom"), dan jalur CSV cadangan mewajibkan ekspor **semua** produk.
- Database belum ada → `stok.py info` memberi `ok: false` + exit 1; resep menyuruh berhenti (tidak ada laporan kosong palsu). Diuji.
- `--tools exec,read` **dijalankan sungguhan** di Gateway uji: job tersimpan dengan `toolsAllow: ["exec","read"]`.
- Angka diverifikasi: HT-L terjual 12 dalam 30 hari → 0,4/hari → 8/0,4 = 20 hari; MUG 3/30 → 9/0,1 = 90 hari.
