# 00 — Uji A/B: tanpa skill vs dengan skill (skenario normal 1)

> Penguji independen, 30 Sep 2026, Odoo Community ASLI 18.0 lokal (data fiktif, lihat `06`). "Tanpa skill" = agent yang sama diberi alamat, database, login, dan kunci API, lalu menulis kueri XML-RPC sendiri seperti umumnya (simulasi oleh penguji; kueri naif yang lazim ditulis LLM tanpa panduan).

**Permintaan:** "Penjualan hari ini berapa, dan siapa yang belum bayar?"

## Tanpa skill
Kueri yang ditulis agent:
```python
sale.order search_read [date_order >= '2026-09-30 00:00:00', date_order <= '2026-09-30 23:59:59', state in (sale, done)]
account.move search_read [move_type = out_invoice, payment_state != paid]   # jumlahkan amount_residual
```
Hasil nyata dari Odoo 18:
```
Penjualan hari ini: 3 pesanan (S00007, S00003, S00002), total 984611.0800000001
Belum dibayar: 9 faktur, total 4269670.0
```
Masalah:
- **Zona waktu salah**: Odoo menyimpan jam dalam UTC. S00001 (00:30 WIB hari ini) hilang, S00007 (00:00 WIB **besok**) ikut. Total salah **Rp 260.850** (benar: Rp 1.245.461,08).
- **Piutang salah Rp 862.470**: faktur **draf** ikut dihitung (benar: 8 faktur Rp 3.407.200). Tidak ada umur piutang, nota kredit tidak dicatat.
- Format float mentah (`984611.0800000001`), tanpa pemisah ribuan Rupiah, tanpa nama disamarkan, tanpa pembanding kemarin/produk terlaris.
- Tidak ada pengaman: agent yang sama bisa memanggil `unlink`/`action_post` bila diminta; kunci API ditempel di chat/kode.

## Dengan skill
```
Pesanan terkonfirmasi: 3, total Rp 1.245.461,08 (+164,0% vs kemarin)
Sebelum pajak Rp 1.122.037,01 | Pajak Rp 123.424,07
Faktur diposting: 1 (+1 nota kredit), total Rp 299.700
PIUTANG: Belum lunas 8 faktur, Rp 3.407.200; lewat jatuh tempo 5 faktur, Rp 2.497.000
UMUR: belum JT 910.200 | 1-30 832.000 | 31-60 111.000 | 61-90 555.000 | >90 999.000
```
(Lengkap di `06` dan `07`.) Semua angka cocok dengan hitungan independen penguji; kunci disimpan di file 600, tidak pernah tampil; metode tulis selain draf quotation ditolak.

## Kesimpulan
Dengan skill **jelas lebih baik**: dua angka utama tanpa skill salah (penjualan −21%, piutang +25%) dengan cara yang tidak terlihat oleh pemilik awam. Bahan "sebelum/sesudah" README: "Tanpa skill: Rp 984.611 (salah zona waktu) → Dengan skill: Rp 1.245.461,08 (cocok layar Odoo)".
