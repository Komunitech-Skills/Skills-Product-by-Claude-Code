# 00 — Uji A/B: tanpa skill vs dengan skill (skenario S1)

**Input pengguna (sama persis):**
> Buatkan laporan penjualan otomatis tiap Senin jam 7 pagi, kirim ke Telegram saya. File kasirnya saya taruh di folder laporan/masuk/penjualan, chat id telegram saya 123456789

## A. Tanpa skill (agent OpenClaw umum)
Simulasi jujur: agent tahu OpenClaw punya cron, lalu langsung membuat jadwal.
```
Siap! Saya buatkan jadwalnya:

openclaw cron add --name "Laporan Penjualan Mingguan" --cron "0 7 * * 1" \
  --message "Baca file CSV di laporan/masuk/penjualan dan buat ringkasan penjualan minggu lalu" \
  --announce --channel telegram --to 123456789

Setiap Senin jam 7 pagi Anda akan menerima ringkasan penjualan di Telegram.
```
Masalah (diperiksa):
- Tanpa `--tz Asia/Jakarta` → cron memakai zona waktu komputer Gateway (`--help`: "cron default: Gateway host local timezone"); di VPS UTC laporan tiba 14:00 WIB.
- Tidak mengecek apakah folder berisi data → saat file belum diekspor, agent terjadwal bisa mengirim "omzet Rp 0"/karangan.
- Tidak ada contoh laporan pertama, tidak diuji, tidak ada `--session isolated`, tidak menyebut syarat komputer menyala, tidak ada aturan tanpa data pelanggan.
- Angka tiap minggu dihitung "dikira-kira" oleh model dari CSV (tanpa script) — status Batal, "Rp 30.000,-", dan tanggal rusak rawan salah.

## B. Dengan skill
(lengkap di `01-penjualan-mingguan-telegram.md`)
- Cek data (`cek_sumber_data.py`) → hitung lewat `rekap.py` (Batal dibuang, baris rusak dilaporkan) → pesan rapi 13 baris lewat `susun_pesan.py`:
```
*Laporan Penjualan Mingguan*
Senin 14 - Minggu 20 Sep 2026
Total omzet: Rp 2.778.000 | Jumlah baris/item terjual: 62 | Rata-rata omzet/hari: Rp 396.857
Hari terbaik: Minggu 20/09 (Rp 524.000) | Hari terendah: Rabu 16/09 (Rp 270.000)
Produk terlaris: Matcha Latte 39 pcs Rp 858.000; Roti Bakar Coklat 38 pcs Rp 570.000; Croissant 26 pcs Rp 520.000
⚠️ 7 transaksi Batal tidak dihitung. ⚠️ 1 baris dilewati (tanggal tidak terbaca).
```
- Konfirmasi → `automations add ... --tz "Asia/Jakarta" --session isolated --announce --channel telegram --to "123456789"` (dijalankan sungguhan pada Gateway uji: jalan berikutnya Senin 07:00 WIB) → uji run → cara kelola → syarat komputer menyala + opsi jasa setup.

## Penilaian
| Kriteria | Tanpa skill | Dengan skill |
|---|---|---|
| Zona waktu benar | Tidak | Ya (`--tz Asia/Jakarta`) |
| Data kosong → tidak kirim nol | Tidak dijaga | Dijaga (dua lapis: cek sebelum jadwal + instruksi di prompt) |
| Angka dihitung script & terverifikasi | Tidak | Ya (cocok dengan hitungan independen) |
| Contoh pertama & uji sebelum aktif | Tidak | Ya |
| Privasi & kanal aman | Tidak dibahas | Telegram default, tanpa data pelanggan |

**Kesimpulan:** dengan skill jelas lebih baik dan lebih aman.
