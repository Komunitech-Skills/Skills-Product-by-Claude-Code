# Contoh pembuat: distributor fiktif, 8 orang, 3 divisi

> Contoh dari pembuat skill (bukan hasil uji independen). Semua nama & angka **fiktif**.
> Output di bawah adalah hasil nyata `scripts/skor_kpi.py` versi 1.0.0 (dijalankan 2026-09-29)
> dengan file di `templates/`. Angka kunci diverifikasi tangan di `tests/uji_regresi.py`.

**Usaha:** CV Sumber Makmur Distribusi (fiktif), distributor sembako ke toko kelontong di Sidoarjo.
Pemilik: Pak Hendra. Data selama ini: target di buku tulis, laporan harian di grup WA "Tim SMD",
beberapa file Excel.

| Divisi | Orang | Peran |
|---|---|---|
| Sales | Andi Pratama, Rina Wulandari | sales |
| Sales | Dewi Lestari | cs |
| Gudang & Pengiriman | Budi Santoso, Joko Susilo | gudang |
| Gudang & Pengiriman | Eko Saputra | kurir |
| Keuangan & Admin | Sari Indah | keuangan |
| Keuangan & Admin | Tono Wijaya | admin |

---

## Langkah 1 — "KPI apa yang cocok untuk gudang?"

```
$ python3 scripts/skor_kpi.py katalog --peran gudang
*gudang*
- Akurasi stok (%, makin tinggi makin baik) bobot 35%, contoh target 99% — sumber: buku-stok (stock opname)
- Pesanan dikemas hari yang sama (%, makin tinggi makin baik) bobot 30%, contoh target 95% — sumber: buku-stok impor-pesanan / resi-picking
- Salah kirim (pesanan, makin rendah makin baik) bobot 20%, contoh target 3 pesanan — sumber: log komplain / retur
- Item stok habis (SKU, makin rendah makin baik) bobot 15%, contoh target 5 SKU — sumber: buku-stok laporan menipis
```

## Langkah 2 — Template rencana KPI

```
$ python3 scripts/skor_kpi.py template --tim templates/tim-contoh.csv --periode 2026-10 --keluar KPI/
Dibuat:
- KPI/rencana-kpi.csv
- KPI/rencana-kpi.xlsx
- KPI/realisasi-2026-10.csv
32 baris KPI.
```
Target lalu disesuaikan dengan data Pak Hendra (omzet Andi 150 jt, Rina 120 jt, ambang omzet,
ambang akurasi stok 97%, dst.) → `templates/rencana-kpi-contoh.csv`.

```
$ python3 scripts/skor_kpi.py cek --rencana templates/rencana-kpi-contoh.csv
✅ Rencana KPI valid: 32 KPI, 8 orang, 3 divisi.
```
Bila salah isi (contoh lain: bobot 60 + 30, target omzet 0):
```
❌ Rencana KPI belum bisa dipakai:
- Rencana baris 2 (Ani / Omzet): target 0 untuk KPI arah 'naik' tidak bisa dihitung (pembagian dengan nol). Isi target lebih dari 0.
- Bobot KPI Ani berjumlah 90, harus tepat 100. Ubah bobot lalu cek lagi.
```

## Langkah 3 — Rekap grup WA jadi draf realisasi

Isi `templates/pesan-wa-contoh.txt` (ekspor chat grup, 30 Sep 2026):
```
[30/09/26 17.06] Pak Hendra: Andi closing 14 deal, target 15, omzet 162 jt
[30/09/26 17.07] Rina: omzet saya 96jt, closing 9
[30/09/26 17.08] Pak Hendra: Joko salah kirim 6 dan akurasi opname 96%
[30/09/26 17.09] Pak Hendra: Eko antar 640 paket, gagal kirim 4%
[30/09/26 17.10] Pak Hendra: Sari mantap, tutup buku 6 hari
```
```
$ python3 scripts/skor_kpi.py baca-teks --rencana templates/rencana-kpi-contoh.csv --teks templates/pesan-wa-contoh.txt --periode 2026-09 --keluar KPI/draf.csv
DRAF realisasi dari teks — WAJIB dicek sebelum dipakai:
- Andi Pratama | Jumlah closing = 14 deal
- Andi Pratama | Omzet penjualan = Rp 162.000.000
- Rina Wulandari | Omzet penjualan = Rp 96.000.000
- Rina Wulandari | Jumlah closing = 9 deal
- Joko Susilo | Salah kirim = 6 pesanan
- Joko Susilo | Akurasi stok = 96%
- Eko Saputra | Jumlah pengiriman = 640 paket
- Eko Saputra | Paket gagal kirim = 4%
- Sari Indah | Hari tutup buku = 6 hari
```
"Rina: omzet saya ..." dibaca sebagai Rina karena pengirimnya Rina. "target 15" dibandingkan
dengan rencana (sama, jadi tidak ada catatan). Agent menunjukkan tabel ini, Pak Hendra membalas
"ok", status draf diubah ke `dikonfirmasi`, lalu digabung ke `realisasi.csv` bersama angka
lain dari Excel (hasil akhirnya = `templates/realisasi-contoh.csv`). Data "Nota diarsip" milik
Tono belum masuk.

Log komplain & pengiriman harian (`templates/log-operasional-contoh.csv`):
```
$ python3 scripts/skor_kpi.py rekap-log --log templates/log-operasional-contoh.csv
Rekap log → realisasi:
- 2026-09 | Eko Saputra | Pengiriman tepat waktu = 75 (dari log: 4 catatan (persen))
- 2026-09 | Joko Susilo | Salah kirim = 3 (dari log: 2 catatan (jumlah))
- 2026-09 | Dewi Lestari | Komplain selesai <=2 hari = 75 (dari log: 4 catatan (persen))
- 2026-09 | Dewi Lestari | Waktu respons pertama = 8 (dari log: 3 catatan (rata-rata))
```
(Log contoh ini hanya potongan beberapa hari, jadi angkanya berbeda dari realisasi bulanan penuh.)

## Langkah 4 — Skor September (ringkasan untuk Telegram pemilik)

```
$ python3 scripts/skor_kpi.py skor --rencana templates/rencana-kpi-contoh.csv --realisasi templates/realisasi-contoh.csv --periode 2026-09 --judul "KPI CV Sumber Makmur Distribusi"
📊 *KPI CV Sumber Makmur Distribusi — 2026-09*
Perusahaan: 🟡 93,6 (▲6,3 vs 2026-08) — sebagian

*Divisi*
🟡 Gudang & Pengiriman: 91,7 ▼4,2
🟡 Keuangan & Admin: 93,1 ▲17,6 (tanpa Tono Wijaya)
🟡 Sales: 96,1 ▲5,6

*Per orang* (urut divisi & nama, bukan peringkat)
🟢 Budi Santoso (Gudang & Pengiriman): 107,1 ▲10,8
🟡 Eko Saputra (Gudang & Pengiriman): 91,3 ▼8,2 — perlu perhatian: Paket gagal kirim 66,7%
🔴 Joko Susilo (Gudang & Pengiriman): 76,7 ▼15,1 — perlu perhatian: Salah kirim 0,0%
🟡 Sari Indah (Keuangan & Admin): 93,1 ▲27,1 — perlu perhatian: Hari tutup buku 80,0%
⚪ Tono Wijaya (Keuangan & Admin): belum lengkap — belum ada data: Nota diarsip lengkap
🟢 Andi Pratama (Sales): 102,4 ▲9,0
🟢 Dewi Lestari (Sales): 107,5 ▲15,0
🔴 Rina Wulandari (Sales): 78,3 ▼7,3 — perlu perhatian: Jumlah closing 60,0%

⚠️ Tono Wijaya belum lengkap (tidak ikut rata-rata divisi): belum ada data Nota diarsip lengkap.

Skor 100 = rata-rata target tercapai (maks 120% per KPI). 🟢 ≥100 🟡 ≥80 🔴 <80. Bahan diskusi, bukan dasar sanksi otomatis.
```
Saran tindak lanjut dari agent (berbasis angka):
1. Joko: salah kirim 6 dari target 3 dan akurasi stok 96% (di bawah batas 97%) → bahas di 1:1, cek apakah ada lonjakan pesanan/ SKU mirip.
2. Rina: closing 9 dari 15, omzet 96 jt (di bawah batas 100 jt) → lihat pipeline `crm-wa` bersama.
3. Tono: lengkapi data "Nota diarsip lengkap" supaya skor Keuangan & Admin utuh.

Cek hitung (Joko): akurasi 96 ÷ 99 = 97,0% × 35 = 33,94; dikemas 88 ÷ 95 = 92,6% × 30 = 27,79;
salah kirim (2 − 6 ÷ 3) = 0% × 20 = 0; stok habis (2 − 5 ÷ 5) = 100% × 15 = 15 → 76,73 → **76,7**.

Versi untuk grup kantor (tanpa nama, Tono dihitung dari KPI yang ada):
```
$ ... --tanpa-nama --data-kosong bobot-ulang
📊 *Laporan KPI Tim — 2026-09*
Perusahaan: 🟡 95,7 (▲8,4 vs 2026-08)

*Divisi*
🟡 Gudang & Pengiriman: 91,7 ▼4,2
🟡 Keuangan & Admin: 99,2 ▲23,8
🟡 Sales: 96,1 ▲5,6

⚠️ 1 orang dihitung dari sebagian KPI (--data-kosong bobot-ulang).

Skor 100 = rata-rata target tercapai (maks 120% per KPI). 🟢 ≥100 🟡 ≥80 🔴 <80. Bahan diskusi, bukan dasar sanksi otomatis.
```

## Langkah 5 — Bahan 1:1 untuk Joko

```
$ python3 scripts/skor_kpi.py skor ... --periode 2026-09 --orang "Joko Susilo"
*Rincian KPI Joko Susilo (Gudang & Pengiriman) — 2026-09*
Skor: 🔴 76,7 (▼15,1 vs 2026-08)

🔴 Akurasi stok ↑: 96% dari target 99% → capaian 97,0%, bobot 35%, nilai 33,9 ▼1,5
🟡 Pesanan dikemas hari yang sama ↑: 88% dari target 95% → capaian 92,6%, bobot 30%, nilai 27,8 ▼4,2
🔴 Salah kirim ↓: 6 pesanan dari target 3 pesanan → capaian 0,0%, bobot 20%, nilai 0,0 ▼66,7
🟢 Item stok habis ↓: 5 SKU dari target 5 SKU → capaian 100,0%, bobot 15%, nilai 15,0 ＝0,0
```
Draf catatan (dari `templates/catatan-1on1.md`):
- **Apresiasi:** stok habis tepat di target (5 SKU) walau pesanan ramai.
- **Pertanyaan pembuka:** "Salah kirim naik dari 4 ke 6 bulan ini. Menurut kamu apa penyebabnya?"
  · "Ada hambatan di luar kendalimu, misalnya label rak, SKU yang mirip, atau jumlah pesanan?"
- **Kemungkinan penyebab (hipotesis, dicek bersama):** varian kemasan mirip (1 kg vs 900 g);
  pesanan hari Senin menumpuk.
- **Kesepakatan:** (diisi saat 1:1).

## Langkah 6 — OKR kuartal 4 (check-in minggu ke-6 dari 13, `--jalan 0,5`)

```
$ python3 scripts/skor_kpi.py okr --okr templates/okr-contoh.csv --periode 2026-Q4 --jalan 0,5
🎯 *OKR — 2026-Q4* (waktu berjalan 0,50)
🟢 Divisi Sales — Jadi distributor pilihan toko kelontong di Sidoarjo: 0,52
   🟢 Toko aktif order bulanan: 0,50
   🔴 Repeat order toko baru dalam 30 hari (%): 0,25
   🟢 Katalog digital dikirim ke semua toko aktif: 0,80
🟢 Gudang & Pengiriman — Pengiriman yang bisa diandalkan: 0,53
   🟢 Pengiriman tepat waktu (%): 0,56
   🟢 Salah kirim per bulan (turun): 0,50
Progres 0-1,0. 🟢 ≥ waktu berjalan, 🟡 ≥ 70% dari itu, 🔴 di bawahnya.
```
Cek: toko aktif (150 − 120) ÷ (180 − 120) = 0,50; repeat order (45 − 40) ÷ (60 − 40) = 0,25
< 0,35 (70% × 0,5) → 🔴; salah kirim menurun (5 − 8) ÷ (2 − 8) = 0,50.

## Langkah 7 — Jadwal (OpenClaw)

Setelah Pak Hendra setuju dengan contoh laporan di Langkah 4:
```
openclaw automations add "0 7 2 * *" "Jalankan resep di KPI/RESEP-laporan-kpi.md untuk bulan lalu ..." \
  --name "Laporan KPI bulanan" --tz "Asia/Jakarta" --session isolated \
  --announce --channel telegram --to "<ID chat Telegram Pak Hendra>"
```
→ catat `id` → `openclaw automations run <id> --wait` → tunjukkan hasil → jelaskan
`disable/enable/rm <id>` dan syarat komputer menyala. (Belum diuji di Gateway untuk skill ini;
pola dari `laporan-otomatis-terjadwal`.)
