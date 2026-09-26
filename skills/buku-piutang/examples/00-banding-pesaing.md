# Uji banding pesaing — buku-piutang v1.0.0

- **Penguji:** agent independen Akun B, 26 Sep 2026. Skill pesaing hanya dibaca & dijalankan untuk dinilai (tidak disalin).
- **Pencarian:** "accounts receivable aging SKILL.md agent skill", "AR aging clawhub/skills.sh", "Kledo fitur piutang umur piutang pengingat WhatsApp", "Frappe Books accounts receivable aging offline".

## Pesaing yang dinilai
### 1. Skill agent: `Denymbird/accounts-receivable-skills` (MIT)
- URL: https://github.com/Denymbird/accounts-receivable-skills — skill `accounts-receivable` (SKILL.md + `scripts/ar.py`, Python standar, ada tes). Dibuat 13 Agu 2026 (±1,5 bulan, 2 commit); jumlah bintang tidak terbaca dari API saat uji. Isi berkualitas (aturan "never compute a figure yourself", workings/control total, tone ladder), tetapi terhubung ke promosi layanan berbayar Paidnice.
- Audit singkat: `ar.py` hanya mengimpor argparse/csv/json/os/re/sys/datetime/decimal; tidak ada jaringan/subprocess. Dijalankan di folder terpisah.
- **Dijalankan pada data skenario 01** (CSV diubah ke format kolom Xero, `snapshot --as-of 2026-09-26` → `aging`):
```
open balance 110,811,250.00 | exceptions 49
TOTAL  Current 14,951,875.00 | 1-30 15,588,500.00 | 31-60 16,140,125.00 | 61-90 48,505,000.00 | 90+ 15,625,750.00
Overdue 95,859,375.00 of 110,811,250.00 open (86.5%)
RM Padang Sederhana   0.006,200,000.00   0.005,300,500.00   0.0011,500,500.00   ← kolom menempel untuk nominal Rupiah
```
  Angka identik dengan buku-piutang (validasi silang yang baik).

### 2. Aplikasi SaaS: Kledo (pembanding fitur)
- https://kledo.com/laporan-umur-piutang/ , https://kledo.com/laporan-hutang-piutang-per-kontak/ , https://kledo.com/detail-faq/apa-itu-fitur-pengingat-jatuh-tempo/
- Laporan umur piutang & piutang per kontak, ekspor, bagikan via email/WA; pengingat jatuh tempo otomatis ke pelanggan (SMS/WA) di paket Elite ke atas. Data di cloud, berlangganan.

### 3. Aplikasi open-source lokal: Frappe Books
- https://github.com/frappe/books — desktop offline, SQLite lokal, akuntansi double-entry lengkap (faktur, pembayaran, laporan). Perlu input lewat GUI, bukan chat; kurva belajar akuntansi.

## Penilaian berdampingan (skenario 01)
| Kriteria | buku-piutang | accounts-receivable (skill) | Kledo | Frappe Books |
|---|---|---|---|---|
| Angka umur/saldo benar | ✅ (terverifikasi) | ✅ identik | ✅ (asumsi) | ✅ (asumsi) |
| Buku tersimpan & diperbarui lewat chat (bayar, cicil, deposit, batal) | ✅ | ❌ snapshot baca saja | ✅ GUI | ✅ GUI |
| Kelebihan bayar / deposit / invarian saldo | ✅ | ❌ | ✅ | ✅ |
| Bahasa & format Indonesia (Rp, tanggal, "2,5 jt", "30 hari") | ✅ | ❌ Inggris, kolom rusak untuk Rupiah | ✅ | sebagian |
| Draf tagihan bertahap + wa.me, dikirim manusia | ✅ | brief → email Inggris | kirim otomatis (berbayar) | ❌ |
| Impor CSV berantakan dari kasir/Excel lokal | ✅ (Win-1252, format Amerika ditolak) | CSV Xero/QBO | impor terbatas | impor terbatas |
| Tanpa internet/langganan, data lokal | ✅ | ✅ (tapi butuh ekspor Xero/QBO) | ❌ | ✅ |
| DSO, surat pernyataan pelanggan (statement), denda | ❌ (denda sengaja → tagih-piutang) | ✅ | ✅ | sebagian |
| Ringkasan terjadwal ke Telegram (OpenClaw) | ✅ | ❌ | notifikasi aplikasi | ❌ |

## Kesimpulan
Untuk UMKM Indonesia yang mencatat bon lewat chat, **buku-piutang unggul jelas**: satu-satunya yang menggabungkan buku piutang persisten, bahasa & format lokal, penanganan cicilan/kelebihan bayar, dan draf WA yang dikirim sendiri. Pesaing skill unggul pada **DSO dan customer statement** (rekening koran pelanggan yang bisa dicetak/dikirim) serta blok "workings/control total" di setiap output. Kedua fitur itu layak dipertimbangkan (ditulis dengan cara sendiri) untuk versi berikut: `saldo --pelanggan` sudah dekat dengan statement, tinggal versi siap cetak/kirim.
