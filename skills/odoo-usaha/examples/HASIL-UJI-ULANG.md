# HASIL UJI ULANG — odoo-usaha

## Uji ulang 1.0.1 (2026-09-30)

- **Penguji:** agent penguji independen (bukan pembuat, bukan penguji 1.0.0). Membaca folder skill, `examples/HASIL-UJI.md`, `docs/panduan-odoo.md` §5.
- **Lingkungan:** salinan skill di scratchpad; `HOME` diarahkan ke scratchpad (tidak menyentuh `~/.komunitech` asli). **Odoo Community asli** dari image Docker resmi `odoo:18.0` (18.0-20260926, XML-RPC) dan `odoo:19.0` (19.0-20260926, JSON-2) + `postgres:16`, modul Sales + Inventory + Invoicing, tanpa data demo, mata uang perusahaan IDR, pajak jual 11%.
- **Data uji BARU (berbeda dari uji 1.0.0), dibuat penguji lewat `odoo shell`:** 4 pelanggan fiktif, 6 produk (5 barang stok + 1 non-stok), 4 aturan stok minimum, stok minus −3, 1 penerimaan terjadwal (25 + 10), 8 SO (5 terkonfirmasi dengan jam di tepi zona waktu, 1 draf, 1 batal, penjual berbeda: pengguna bot / admin / kosong), 6 faktur + 2 nota kredit (bayar sebagian 2 kali, lunas, nota kredit dicocokkan ke faktur 25-08, 1 faktur draf).
- **Pengguna API (kunci API asli Odoo):** `bot-own` (Sales Own Documents + Inventory User), `bot-own-akun` (Own Documents + Accounting Read-only), `bot-lengkap` (Sales All Documents + Accounting Read-only + Inventory User = rekomendasi panduan), `bot-all-tanpa-akun` (All Documents saja), `admin`.
- **Semua angka harapan dihitung penguji secara independen** dari buku besar fiktif penguji (`hitung_piutang.py`, hitungan tangan untuk penjualan/stok/pajak), lalu dibandingkan dengan keluaran skill.

### 1. Temuan TINGGI #1 (Own Documents → Rp 0 diam-diam) — **TERATASI**
| Kunci | Versi | Keluaran skill | Harapan penguji | Kode |
|---|---|---|---|---|
| bot-own | 18 & 19 | `cek`: "Pesanan penjualan: HANYA milik pengguna API ini", "Faktur pelanggan: HANYA …" + 2× PERINGATAN | sesuai (grup hanya `group_sale_salesman`) | 0 (cek) |
| bot-own | 18 | `penjualan --rinci`: PERINGATAN DATA SEBAGIAN (pesanan & faktur) di atas angka; 2 pesanan Rp 321.345 (S00001 milik bot + S00003 tanpa penjual) | 2 / Rp 321.345 (angka usaha sebenarnya 3 / Rp 732.045) | **9** |
| bot-own | 19 | sama, `--terima-sebagian` | peringatan tetap tampil | 0 |
| bot-own | 18 | `laporan-harian`: PERINGATAN di baris 3–4 | — | **9** |
| bot-own | 19 | `piutang`: PERINGATAN, 0 faktur (hanya INV/00003 miliknya, sudah lunas) | benar untuk cakupan itu | **9** |
| bot-own-akun | 19 | pesanan: PERINGATAN (1 pesanan Rp 191.475); faktur: SEMUA (Rp 222.000) — peringatan hanya untuk pesanan | tepat: Accounting Read-only membuka semua faktur | **9** |
| bot-lengkap | 18 & 19 | cakupan SEMUA, tanpa peringatan; 3 pesanan **Rp 732.045** (DPP 659.500, pajak 72.545), kemarin Rp 388.389 (**+88,5%**); faktur 1 + 1 nota kredit **Rp 222.000** | 129.870 + 410.700 + 191.475 = 732.045; (732.045−388.389)/388.389 = 88,48%; 277.500 − 55.500 = 222.000 | 0 |
| bot-all-tanpa-akun | 18 & 19 | cakupan SEMUA (pesanan & faktur) | benar: All Documents melihat semua faktur pelanggan | 0 |

### 2. Temuan SEDANG #2 (`piutang --per-tanggal` lampau) — **TERATASI**
11 tanggal × 2 versi (kunci `bot-lengkap`), semuanya **identik** dengan hitungan independen (jumlah faktur, total sisa, bucket umur, hari lewat per faktur):

| Per tanggal | Skill (18 = 19) | Harapan penguji | Kasus yang diuji |
|---|---|---|---|
| 2026-05-09 | 0 faktur, Rp 0 | 0 | sebelum faktur pertama terbit |
| 2026-06-15 | 1, Rp 1.110.000 (lewat 6) | 1.110.000 | INV/00001 lunas 10-09 ditambahkan kembali; faktur terbit sesudahnya dikecualikan |
| 2026-07-15 | 3, Rp 3.385.000 | 3.385.000 | bayar sebagian 500.000 **pada** tanggal acuan dianggap sudah terjadi |
| 2026-07-31 | 3, Rp 3.385.000 | 3.385.000 | INV/00003 lunas 01-08 ditambahkan kembali |
| 2026-08-01 | 2, Rp 2.830.000 | 2.830.000 | pelunasan di hari acuan |
| 2026-08-18 | 3, Rp 6.160.000 | 6.160.000 | INV/00004 terbit 15-08, bayar sebagian 20-08 ditambahkan kembali |
| 2026-08-24 | 3, Rp 5.160.000 | 5.160.000 | — |
| 2026-08-25 | 3, Rp 5.049.000 | 5.049.000 | nota kredit 111.000 dicocokkan ke INV/00002 |
| 2026-09-15 | 2, Rp 4.439.000 | 4.439.000 | INV/00001 lunas 10-09 |
| 2026-09-29 | 3, Rp 5.216.000 | 5.216.000 | — |
| hari ini | 4, Rp 5.493.500 + NK terbuka Rp 55.500 | 5.493.500; 55.500 | faktur draf 999.000 tidak dihitung |

**Pembanding milik Odoo:** laporan *Aged Receivable* hanya ada di Enterprise (`account_reports`), tidak tersedia di Community. Sebagai gantinya penguji menjumlah saldo akun piutang (`account.move.line`, `asset_receivable`, `date <= per`) langsung di Odoo 18 & 19: 1.110.000 / 3.385.000 / 3.385.000 / 2.830.000 / 6.160.000 / 5.160.000 / 5.049.000 / 4.439.000 / 5.216.000 / 5.438.000 — **cocok** dengan skill untuk semua tanggal (hari ini: 5.493.500 − nota kredit 55.500 = 5.438.000).
Jalur peringatan: setelah penguji mematikan izin baca `account.partial.reconcile` untuk grup Sales di Odoo 18, `piutang --per-tanggal 2026-08-18` → **PERINGATAN DATA SEBAGIAN** + **kode 9** (angka jatuh ke sisa saat ini Rp 4.439.000, bukan 6.160.000). Izin dipulihkan setelahnya.

### 3. Temuan SEDANG #3 (klaim hak akses) — **TERATASI, 1 sisa dokumentasi**
Uji langsung ke API (di luar skill) dengan kunci `bot-lengkap` (hak rekomendasi):
| Aksi | 18 | 19 |
|---|---|---|
| `sale.order.create` / `write` | BERHASIL | BERHASIL (create) |
| `sale.order.action_confirm` | **BERHASIL** | (tidak diuji) |
| `account.move.create` | DITOLAK | DITOLAK 403 |
| `account.move.action_post` | DITOLAK ("don't have the access rights to post") | — |
| `res.partner.write/unlink`, `product.template.write` | DITOLAK | DITOLAK 403 |

(SO uji hasil probe dihapus lagi.) Jadi klaim SKILL/panduan bahwa Odoo tidak punya peran Penjualan baca-saja dan *Read-only* menahan posting faktur **benar**. **Daftar izin metode di sisi klien:** 16 panggilan terlarang (`write`, `action_confirm`, `unlink`, `copy`, `action_quotation_send`, `message_post`, `name_create` di sale.order; `action_post`/`create` account.move; `create` res.partner, sale.order.line, account.payment.register; `write` res.users, ir.model.access; `has_group` di res.partner; `action_apply_inventory`) → **16/16 ditolak** di 18 dan 19 sebelum dikirim (kode 2). Nilai `vals` quotation disusun script (tanpa `state`), dibaca ulang status DRAF.

### 4. Regresi
- **Penjualan & zona waktu:** WIB: S00004 (17:05 UTC 30-09 = 00:05 WIB 1-10) dikecualikan, S00002 (23:45 WIB) masuk, S00005 (23:30 WIB 29-09) masuk "kemarin". `--tz WITA`: 3 pesanan **Rp 543.234** (S00005 pindah ke hari ini, S00002 keluar), kemarin Rp 166.500 (+226,3%) — cocok hitungan. Draf & batal tidak dihitung. `--samarkan` → inisial.
- **Stok menipis:** GP-1 stok −3 MINUS, perkiraan 7 → saran **5** (12−7) "(sudah ada barang masuk terjadwal 10)"; MG-2 HABIS, perkiraan 25 → saran **0** "(… terjadwal 25; tunggu penerimaan)"; BRS-5 MENIPIS 4 → saran **26**; KB-200 habis tanpa aturan; barang non-stok tidak muncul; TC-25 (Odoo membuat penerimaan otomatis 12) tidak muncul — benar. Kasus "PERKIRAAN DI BAWAH MINIMUM" tidak teruji (Odoo mengisi ulang otomatis).
- **Laporan harian Telegram:** angka sama dengan `penjualan`/`piutang`/`stok-menipis`; 0 nama pelanggan lengkap (hanya nomor faktur + inisial); < 3.500 karakter.
- **Draf quotation + dobel:** 18: S00010 DPP Rp 60.750 (diskon 10%), pajak Odoo 6.682,50 vs standar 6.682 → COCOK; ulangan → **kode 7** "DRAF TIDAK DIBUAT … S00010". 19: DPP Rp 338.300, pajak 37.213 = 338.300 × 11% dibulatkan ke bawah → COCOK; ulangan → kode 7. Item rusak `#x` → kode 2.
- **Host allowlist tanpa `ODOO_HOST_DIIZINKAN`:** dengan ENV itu diisi `erp.contoh.id,attacker.id,nip.io`, semua tetap ditolak kode 2 (`erp.contoh.id`, `evil.odoo.com.attacker.id`, `127.0.0.1.nip.io`, `…odoo.com@attacker.id`, `http://….odoo.com`). String ENV tidak ada lagi di `odoo.py`. `atur --izinkan-host` menolak http untuk internet dan menyimpan host https (izin berkas 600).
- **`tests/uji_regresi.py`:** 51 uji OK. **`validate.py --skill odoo-usaha`:** valid. **Kebocoran kunci:** 0 dari 81 berkas keluaran.
- Kasus data nyata yang tertangkap baik: sebelum penguji membetulkan data, pesanan memakai pricelist USD (sisa sebelum mata uang perusahaan diganti ke IDR) → skill **tidak** menjumlahkannya dan menulis CATATAN per pesanan.

### Temuan baru
**SEDANG**
1. **`docs/panduan-odoo.md` §5 berisi sisa blok lama** (setelah daftar poin baru): baris tabel yatim `---|---|---|` lalu rekomendasi versi 1.0.0 — "Faktur/Akuntansi: … selain itu *Billing*", "Bot Penjualan: *User: Own Documents* atau *All Documents*", dan poin duplikat. Ini bertentangan dengan rekomendasi baru (bukan Billing; jangan Own Documents) dan membingungkan pembeli awam. Hapus blok itu.

**RENDAH**
2. Klaim "Odoo masih mengizinkan membuat/mengubah penawaran" kurang lengkap: dengan hak rekomendasi, kunci yang dipakai di luar skill juga bisa **mengonfirmasi pesanan** (terbukti di 18). Tambahkan "dan mengonfirmasi pesanan" agar risiko kunci bocor tergambar jujur.
3. Teks peringatan jalur "pelunasan tidak bisa dibaca" hanya menyebut faktur yang *lunas*; faktur yang *dibayar sebagian* setelah tanggal acuan juga tampil dengan sisa saat ini (lebih kecil). Arah peringatan & kode 9 sudah benar; cukup perjelas kalimatnya.
4. Panduan menyebut piutang lampau "butuh hak Akuntansi baca"; di Odoo 18 & 19 hak *Sales All Documents* saja sudah bisa membaca tabel pelunasan (angka benar). Konservatif, tidak merugikan.
5. `laporan-harian` bagian STOK tidak membawa keterangan "barang masuk terjadwal" (MG-2 tampil "0 (HABIS)" dan ikut hitungan "3 barang habis/minus. Cek pembelian.") padahal `stok-menipis` sudah menyarankan tunggu penerimaan.

### Skor: **8/10**
Alasan: ketiga temuan tinggi/sedang 1.0.0 terbukti teratasi dengan data baru di Odoo 18 & 19 asli — peringatan data sebagian + kode 9 muncul di semua perintah dengan hak Own Documents dan hilang dengan hak rekomendasi; piutang per tanggal lampau cocok 22/22 perbandingan dan cocok dengan saldo buku besar Odoo; klaim hak akses kini jujur dan daftar izin klien menahan 16/16 metode tulis. Regresi (zona waktu, stok, laporan tersamar, draf + anti-dobel, host allowlist) lulus, 51 uji regresi OK, 0 kebocoran kunci. Dikurangi karena blok usang yang bertentangan di panduan §5 (SEDANG #1) dan beberapa kalimat yang perlu dipertajam (#2–#5). Layak `lulus` setelah #1 diperbaiki (perbaikan dokumen, tidak perlu uji ulang penuh).

### Batas kejujuran
Diuji ke Odoo Community 18 & 19 asli lokal dengan data fiktif; **belum** ke Odoo Online, Enterprise, 16/17/20, https nyata, multi-perusahaan, data besar, atau OpenClaw/Telegram sungguhan. `platform_teruji` yang pantas tetap `claude-code (simulasi agent)`.

### Catatan revisi 1.0.2 (2026-09-30, oleh kurator, bukan penguji)
- Temuan SEDANG uji ulang 1.0.1 diperbaiki: blok sisa saran 1.0.0 di `docs/panduan-odoo.md` §5 (tabel kedua yang menyebut *Billing* dan *Own Documents* untuk Bot Penjualan) dihapus. Kini hanya ada satu tabel hak akses, yaitu All Documents + Akuntansi Read-only. Perubahan hanya di dokumen, script tidak berubah.
- Skor katalog 8 (uji ulang 1.0.1). platform_teruji: Odoo Community 18 & 19 di Docker oleh agent penguji; belum Odoo Online/Enterprise/16/17/20.
