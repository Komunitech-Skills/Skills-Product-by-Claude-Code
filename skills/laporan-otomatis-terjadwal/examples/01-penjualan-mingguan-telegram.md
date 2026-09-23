# 01 — Laporan penjualan mingguan otomatis ke Telegram (uji ulang v1.1.0)

**Skenario:** S1 (normal). Pemilik kedai kopi (OpenClaw, bot Telegram sudah terhubung) punya ekspor kasir mingguan `kasir-minggu-38.csv`: pemisah `;`, 70 baris (62 selesai, 7 batal, 1 tanggal rusak), dengan format seperti "Rp 30.000,-".

**Input pengguna (persis):**
> Buatkan laporan penjualan otomatis tiap Senin jam 7 pagi, kirim ke Telegram saya. File kasirnya saya taruh di folder laporan/masuk/penjualan, chat id telegram saya 123456789

**Perintah yang dijalankan agent (Langkah 2–7 SKILL.md v1.1.0):**
```bash
python3 scripts/cek_sumber_data.py --folder "laporan/masuk/penjualan" --pola "*.csv" --label "penjualan" --maks-umur-hari 6
python3 ../rekap-penjualan-csv/scripts/rekap.py "laporan/masuk/penjualan/kasir-minggu-38.csv" \
  --kolom-tanggal "Tanggal" --kolom-produk "Produk" --kolom-qty "Qty" --kolom-total "Total" --kolom-status "Status" --top 3
# Langkah 3.2: periode hasil 2026-09-14 s/d 2026-09-20 = Senin-Minggu penuh -> boleh dilaporkan
python3 scripts/susun_pesan.py --data pesan.json --maks-baris 15     # exit 0 (tidak ada pola data pribadi)
```

## Output

**Balasan agent 1 (contoh laporan pertama + konfirmasi):**
````
Data penjualan siap: kasir-minggu-38.csv (70 baris data, umur 0 hari), mencakup Senin 14 – Minggu 20 Sep.
Ini contoh laporan yang akan Anda terima setiap Senin pagi:

*Laporan Penjualan Mingguan*
Senin 14 - Minggu 20 Sep 2026
Total omzet: Rp 2.778.000
Jumlah baris/item terjual: 62
Rata-rata omzet/hari: Rp 396.857
Hari terbaik: Minggu 20/09 (Rp 524.000)
Hari terendah: Rabu 16/09 (Rp 270.000)
*Produk terlaris*
- Matcha Latte -- 39 pcs -- Rp 858.000
- Roti Bakar Coklat -- 38 pcs -- Rp 570.000
- Croissant -- 26 pcs -- Rp 520.000
Data mencakup 14-20 Sep 2026 (7 hari penuh). 7 transaksi Batal tidak dihitung.
⚠️ 1 baris dilewati (tanggal tidak terbaca).

Ringkasan jadwal:
- Laporan: penjualan mingguan (Senin–Minggu lalu); resep disimpan di laporan/RESEP-penjualan-mingguan.md
- Data: file CSV di laporan/masuk/penjualan (harus diperbarui tiap minggu; file yang lebih tua dari 6 hari akan diperingatkan)
- Jadwal: setiap Senin 07:00 WIB (Asia/Jakarta)
- Dikirim ke: Telegram, chat id 123456789 (Anda sendiri)
Lanjut buat jadwalnya? (ya/tidak)
````

**Pengguna:** ya

**Balasan agent 2:**
````
Jadwal dibuat:
```bash
openclaw automations add "0 7 * * 1" \
  "Jalankan resep laporan di laporan/RESEP-penjualan-mingguan.md untuk periode Senin-Minggu lalu. Tulis ringkas dalam Bahasa Indonesia, maksimal 15 baris, angka penting di atas, format Rupiah 'Rp 1.250.000', TANPA nama/kontak pelanggan perorangan. Kalau file sumber belum ada/kosong, katakan itu dengan jelas -- JANGAN kirim angka nol." \
  --name "Laporan penjualan Senin" --tz "Asia/Jakarta" --session isolated \
  --announce --channel telegram --to "123456789"
```
Hasil: id d506bf6a-1b9f-49e4-a98c-08d66fec90a6, jalan berikutnya Senin 28 Sep 2026 07:00 WIB,
dikirim ke telegram:123456789.

Uji sekali sekarang:
  openclaw automations run d506bf6a-1b9f-49e4-a98c-08d66fec90a6 --wait
(Setelah hasil uji masuk ke Telegram Anda dan sama dengan contoh di atas, jadwal saya anggap aktif.)

Cara mengelola jadwal (simpan id di atas; kalau lupa, `openclaw automations list --all`):
  openclaw automations show d506bf6a-...     # detail (boleh juga pakai nama persis)
  openclaw automations disable d506bf6a-...  # jeda
  openclaw automations enable d506bf6a-...   # aktifkan lagi
  openclaw automations edit d506bf6a-... --cron "0 8 * * 1" --tz "Asia/Jakarta"
  openclaw automations rm d506bf6a-...       # hapus permanen

Penting: jadwal ini hanya jalan kalau komputer tempat OpenClaw berjalan menyala Senin jam 07:00.
Kalau sering mati, pilihannya: laptop/PC yang memang menyala jam itu, mini PC yang menyala 24 jam,
VPS milik Anda sendiri, atau jasa setup dari tim Komunitech.
Setiap Senin sebelum jam 7, taruh file ekspor kasir minggu lalu di folder tadi. Kalau datanya belum
ada atau tidak mencakup minggu lalu, laporan akan bilang begitu, bukan mengirim angka nol/angka lama.
````

## Catatan penguji
- Angka diverifikasi independen (Python terpisah): omzet 2.778.000, 62 baris sah, rata-rata 396.857,14/hari; 3 teratas dan hari terbaik/terendah cocok.
- **Dijalankan sungguhan** di Gateway OpenClaw 2026.9.5 lokal (uji ulang v1.1.0): Bentuk A di atas dan Bentuk B (`add --cron --message --name ...`) sama-sama berhasil; `show` dengan nama persis berhasil; `disable`/`enable`/`edit --cron --tz`/`edit --to`/`run` (antre: `enqueued: true`)/`runs`/`rm` berhasil dengan **id**. `run --wait` sampai selesai tidak bisa diuji karena mesin uji tanpa model AI.
- Perbaikan v1.1.0 terlihat: label "Jumlah baris/item terjual", catatan netral tanpa ikon vs peringatan ⚠️, langkah cek periode, dan umur data mingguan 6 hari.
- Catatan kecil: pesan v1.1.0 tidak lagi memakai baris kosong antarbagian, jadi agak padat di layar HP (ringan).
