# HASIL UJI INDEPENDEN — odoo-usaha v1.0.0

- **Tanggal:** 30 September 2026
- **Penguji:** agent penguji independen (bukan pembuat); hanya membaca folder skill, `docs/panduan-odoo.md`, (riset internal kurator, tidak disertakan dalam paket). Server tiruan pembuat (`tests/`) **tidak dipakai**.
- **Lingkungan:** salinan skill di scratchpad. **Odoo Community ASLI** dijalankan lokal dari image Docker resmi `odoo:18.0` (18.0-20260926, XML-RPC) dan `odoo:19.0` (19.0-20260926, JSON-2) + `postgres:16`, modul Sales + Inventory + Invoicing, tanpa data demo. Data fiktif diisi penguji lewat API admin (7 SO termasuk kasus tepi zona waktu, 11 faktur/nota kredit termasuk bayar sebagian/lunas/draf, 3 aturan stok minimum, stok minus). Pengguna API: `bot-laporan` (Sales All Documents, Accounting Read-only, Inventory User), `bot-own` (Sales Own Documents), `bot-draf`, `admin`; kunci API asli dibuat di Odoo.
- **Belum diuji:** Odoo 16, 17, 20; Enterprise; Odoo Online (*.odoo.com, paket Custom); server via https/reverse proxy; multi-perusahaan; data besar (> 10.000 baris); OpenClaw/Telegram sungguhan (jadwal). Keluaran agent di skenario 10 adalah simulasi agent.

## Skenario
| # | Skenario | Berkas | Hasil |
|---|---|---|---|
| 1 | Normal: penjualan harian (WIB/WITA, kemarin, 18 & 19) | `06-…` | LULUS — semua angka cocok hitungan penguji |
| 2 | Normal: piutang + umur + laporan harian tersamar | `07-…` | LULUS (1 temuan sedang `--per-tanggal` lampau) |
| 3 | Normal: stok menipis + draf quotation + anti-dobel | `08-…` | LULUS (1 temuan sedang soal hak kunci) |
| 4 | Input tidak lengkap / kredensial belum diatur | `09-…` | LULUS — 13 kasus, pesan & kode keluar tepat |
| 5 | Di luar cakupan (hapus/posting/kirim tagihan) + keamanan | `10-…` | LULUS — 12 metode terlarang ditolak (kunci admin), redirect & host asing ditolak |
| A/B | Tanpa vs dengan skill | `00-pembanding-tanpa-skill.md` | Dengan skill jauh lebih baik (tanpa skill: penjualan −Rp 260.850, piutang +Rp 862.470) |
| Pesaing | erpipe mcp-odoo, ivnvxd mcp-server-odoo | `00-banding-pesaing.md` | odoo-usaha unggul untuk audiens target (analisis dokumentasi, pesaing tidak dijalankan) |

**Verifikasi nama field/metode di Odoo asli 18 & 19:** benar semua — `sale.order` (`state`, `date_order`, `amount_untaxed/tax/total`, `currency_id`, `origin`, `validity_date`), `sale.order.line` (`product_uom_qty`, `price_subtotal`), `account.move` (`move_type`, `state`, `payment_state` not_paid/partial/paid, `invoice_date`, `invoice_date_due`, `amount_*_signed`, `amount_residual_signed`), `stock.warehouse.orderpoint` (`product_min_qty`, `product_max_qty`, `qty_on_hand`, `qty_forecast`), `product.product` (`is_storable`, `qty_available`, `virtual_available`), `res.partner` (`mobile` hilang di 19, ditangani), JSON-2 `create(vals_list)`, `fields_get(attributes)`, `res.users/context_get` (uid terbaca). Kunci API tidak bocor di 22 berkas keluaran (0 kecocokan).

## Temuan
### TINGGI
1. **Hak "Own Documents" → penjualan Rp 0 diam-diam.** Dengan kunci `bot-own` (*Sales: User: Own Documents*, hak yang panduan §5 izinkan untuk Bot Penjualan, dan panduan juga membolehkan memakai akun sendiri), `penjualan` mencetak `Jumlah pesanan: 0 / Total Rp 0` (benar: 3 pesanan Rp 1.245.461,08), kode 0, tanpa peringatan; `laporan-harian` terjadwal akan melaporkan angka salah ke pemilik. `cek` hanya menulis "Penjualan (Sales): bisa dibaca (0 data)". Bukti: `06`, bagian Temuan. **Saran:** di `cek`/`penjualan`/`laporan-harian` periksa apakah pengguna API punya grup `sales_team.group_sale_salesman_all_leads` (baca grup pengguna + `ir.model.data`) atau bandingkan dengan `search_count` tanpa filter; bila hanya "Own Documents", beri CATATAN "angka hanya pesanan milik pengguna ini" / kode non-0 untuk laporan; perbaiki panduan §5.

### SEDANG
2. **`piutang --per-tanggal` masa lalu memasukkan faktur yang belum terbit.** Per 2026-06-15: skill "8 faktur Rp 3.407.200, semua belum jatuh tempo"; benar hanya 2 faktur yang sudah terbit per 15 Juni (INV/00005 terbit 01-06, INV/00006 terbit 01-05), keduanya belum jatuh tempo, total Rp 1.554.000. Bukti: `07`. **Saran:** tambah domain `invoice_date <= per_tanggal`, dan tulis jelas bahwa status bayar tetap kondisi saat ini (atau batasi `--per-tanggal` ke hari ini/masa depan).
3. **Pemisahan kunci "Bot Laporan (baca) vs Bot Penjualan" tidak nyata di Odoo.** Dengan hak yang disarankan panduan §5, `bot-laporan` berhasil membuat draf S00008 di 18 & 19. Baris tabel galat SKILL "Hak akses … kurang (mis. kunci baca dipakai membuat draf)" tidak terjadi; "Billing" untuk faktur juga memberi hak posting. **Saran:** perbaiki SKILL/panduan secara jujur: pengaman utama = daftar izin metode di script (terbukti), hak Odoo hanya membatasi kerusakan bila kunci dipakai di luar skill; sarankan *Accounting: Read-only* (bukan Billing).

### RENDAH
4. CATATAN tetap di `cek` "belum diuji ke server Odoo asli (hanya server tiruan)" dan paragraf status uji SKILL.md kini usang → perbarui: "diuji ke Odoo Community 18 & 19 lokal (penguji independen); belum ke Odoo Online/Enterprise/16/17/20".
5. ENV `ODOO_HOST_DIIZINKAN` menambah host ke daftar izin tanpa `atur --izinkan-host`/penegasan pemilik dan tidak didokumentasikan di SKILL.md. Dokumentasikan atau hapus.
6. `stok-menipis`: bila penerimaan sudah terjadwal (perkiraan ≥ maks), baris "stok -2 (MINUS) … saran pesan 0" benar tetapi membingungkan pembeli awam; tambahkan keterangan "sudah ada barang masuk terjadwal".
7. Pratinjau quotation membulatkan subtotal baris ke rupiah (Rp 18.519) sedangkan Odoo menyimpan 18.518,51; dilaporkan COCOK (< Rp 1). Sesuai standar pembulatan, cukup dicatat.

## Skor: **7/10**
Alasan: inti produk terbukti di **Odoo asli** 18 (XML-RPC) dan 19 (JSON-2) — semua angka penjualan, umur piutang (termasuk batas bucket), stok & saran pesan, serta pajak draf cocok hitungan independen; tebakan nama field/metode pembuat benar semua. Keamanan kuat dan teruji: daftar izin metode menolak 12 metode terlarang bahkan dengan kunci admin, redirect tidak membawa kunci, host asing/penyamaran URL ditolak, 0 kebocoran kunci, nama pelanggan tersamar di laporan, draf dobel diblokir. A/B menunjukkan nilai tambah besar. Dikurangi karena temuan TINGGI #1 (angka Rp 0 diam-diam dengan konfigurasi hak yang diizinkan panduan) dan SEDANG #2–#3. Memenuhi ambang ≥ 7, tetapi **#1–#4 sebaiknya diperbaiki dan diuji ulang sebelum status `lulus`/beta**.

## Batas kejujuran
Diuji ke Odoo Community **asli** yang dijalankan lokal oleh penguji (bukan tiruan), tetapi **belum** ke Odoo Online (*.odoo.com), Enterprise, versi 16/17/20, https nyata, maupun data usaha sungguhan. `platform_teruji` yang pantas: `claude-code (simulasi agent)`; tidak ada uji OpenClaw/Telegram asli di sesi ini.
