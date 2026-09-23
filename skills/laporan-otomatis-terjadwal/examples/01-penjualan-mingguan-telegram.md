# 01 — Laporan penjualan mingguan otomatis ke Telegram

**Skenario:** S1 (normal). Pemilik kedai kopi (OpenClaw, Telegram bot sudah terhubung) punya ekspor kasir mingguan `kasir-minggu-38.csv` (pemisah `;`, 70 baris: 62 selesai, 7 batal, 1 tanggal rusak, format "Rp 30.000,-").

**Input pengguna (persis):**
> Buatkan laporan penjualan otomatis tiap Senin jam 7 pagi, kirim ke Telegram saya. File kasirnya saya taruh di folder laporan/masuk/penjualan, chat id telegram saya 123456789

**Perintah yang dijalankan agent (Langkah 2–7 SKILL.md):**
```bash
python3 scripts/cek_sumber_data.py --folder "laporan/masuk/penjualan" --pola "*.csv" --label "penjualan" --maks-umur-hari 10
python3 ../rekap-penjualan-csv/scripts/rekap.py "laporan/masuk/penjualan/kasir-minggu-38.csv" \
  --kolom-tanggal "Tanggal" --kolom-produk "Produk" --kolom-qty "Qty" --kolom-total "Total" --kolom-status "Status" --top 3
python3 scripts/susun_pesan.py --data pesan.json --maks-baris 15
```

## Output

**Balasan agent 1 (contoh laporan pertama + konfirmasi):**
````
Data penjualan siap: kasir-minggu-38.csv (70 baris data, umur 0 hari).
Ini contoh laporan yang akan Anda terima setiap Senin pagi:

*Laporan Penjualan Mingguan*
Senin 14 - Minggu 20 Sep 2026

Total omzet: Rp 2.778.000
Jumlah transaksi: 62
Rata-rata omzet/hari: Rp 396.857
Hari terbaik: Minggu 20/09 (Rp 524.000)
Hari terendah: Rabu 16/09 (Rp 270.000)

*Produk terlaris*
- Matcha Latte -- 39 pcs -- Rp 858.000
- Roti Bakar Coklat -- 38 pcs -- Rp 570.000
- Croissant -- 26 pcs -- Rp 520.000

⚠️ 7 transaksi berstatus Batal tidak dihitung.
⚠️ 1 baris dilewati (tanggal tidak terbaca).

Ringkasan jadwal:
- Laporan: penjualan mingguan (Senin–Minggu lalu), resep disimpan di laporan/RESEP-penjualan-mingguan.md
- Data: file CSV terbaru di laporan/masuk/penjualan
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
Hasil: id 1307d905-fe39-4490-9b62-2468ee9e1b94, jalan berikutnya Senin 28 Sep 2026 07:00 WIB,
pengiriman: telegram:123456789.

Uji sekali sekarang:
  openclaw automations run 1307d905-fe39-4490-9b62-2468ee9e1b94 --wait
(Setelah hasil uji masuk ke Telegram Anda dan sama dengan contoh di atas, jadwal saya anggap aktif.)

Cara mengelola jadwal:
  openclaw automations list --all                 # lihat semua jadwal
  openclaw automations disable 1307d905-...       # jeda
  openclaw automations enable 1307d905-...        # aktifkan lagi
  openclaw automations edit 1307d905-... --cron "0 8 * * 1" --tz "Asia/Jakarta"
  openclaw automations rm 1307d905-...            # hapus permanen

Penting: jadwal ini hanya jalan kalau komputer tempat OpenClaw berjalan menyala Senin
jam 07:00. Kalau sering mati, pilihannya: laptop/PC yang memang menyala jam itu, mini PC
yang menyala 24 jam, VPS milik Anda sendiri, atau jasa setup dari tim Komunitech.
Setiap Senin sebelum jam 7, taruh file ekspor kasir minggu lalu di folder tadi — kalau
belum ada, laporan akan bilang "belum ada data", bukan mengirim angka nol.
````

## Catatan penguji
- Angka diverifikasi independen (Python terpisah): omzet 2.778.000, 62 baris sah, rata-rata 396.857,14/hari, 3 teratas & hari terbaik/terendah cocok persis.
- Perintah `automations add` di atas **dijalankan sungguhan** pada Gateway OpenClaw 2026.9.5 lokal (HOME uji, tanpa model/kanal): job tercipta, `nextRunAtMs` = Senin 2026-09-28 07:00 WIB, `deliveryPreview: announce -> telegram:123456789`. `edit --cron/--tz/--to`, `disable`, `enable`, `rm` berhasil dengan **id**.
- `run --wait` hanya bisa diuji sampai antre (tidak ada model AI di mesin uji → timeout); ini batas lingkungan uji.
- Contoh di atas **sengaja memakai id**: bila agent mengikuti SKILL.md Langkah 6 (`run <id-atau-nama>`) dan memakai nama, OpenClaw menjawab "Automation not found: Laporan penjualan Senin" (diuji). Lihat HASIL-UJI.md cacat S-1.
- Label "Jumlah transaksi: 62" di sini tepat karena satu baris = satu transaksi; untuk ekspor marketplace (satu pesanan banyak baris) label ini menyesatkan.
