# 00 — Uji banding pesaing (Tahap 6.5)

> Penguji independen, 30 Sep 2026. Pesaing **hanya dibaca** (README/dokumentasi di GitHub), **tidak disalin dan kodenya tidak dijalankan** (aturan audit: kode luar tidak tepercaya). Karena itu perbandingan skenario normal 1 untuk pesaing adalah **analisis kemampuan terdokumentasi**, bukan eksekusi. Jujur: ini lebih lemah daripada uji jalan berdampingan.

## Pencarian
GitHub `odoo mcp in:name,description` urut bintang (458 repo), plus ClawHub/skills.sh (kata kunci: "odoo", "odoo skill", "odoo xmlrpc agent"). Dua teratas:

| Pesaing | Sinyal | Lisensi | Ringkasan terdokumentasi |
|---|---|---|---|
| [erpipe-org/mcp-odoo](https://github.com/erpipe-org/mcp-odoo) | 418★, 190 fork, aktif (update 28-09-2026) | MIT | 41 tool MCP; baca umum; tulis diblok dan lewat alur `preview_write` → `validate_write` → `execute_approved_write` + flag ENV; XML-RPC 16–18 & JSON-2 19+; tool `receivable_payable_aging`; pasang via `uvx` |
| [ivnvxd/mcp-server-odoo](https://github.com/ivnvxd/mcp-server-odoo) | 393★, 184 fork, aktif | MPL-2.0 | CRUD generik + `aggregate_records`; mode standar butuh **modul Odoo MCP** terpasang; mode "YOLO" tanpa modul (read-only atau akses penuh "EXTREMELY DANGEROUS"); XML-RPC |

## Skenario normal 1 ("penjualan hari ini + siapa belum bayar"), dinilai berdampingan
| Kriteria (bobot) | odoo-usaha | erpipe mcp-odoo | ivnvxd mcp-server-odoo |
|---|---|---|---|
| Angka penjualan harian benar (zona WIB, status, draf/batal/besok) (3) | 3 — terbukti di Odoo asli 18/19 | 1 — agent harus menyusun domain & zona sendiri (risiko sama dengan A/B tanpa skill) | 1–2 — `aggregate_records` membantu jumlah, zona tetap tugas agent |
| Umur piutang benar (2) | 2 — terbukti, batas 30/31/90/91 | 2 — ada tool aging khusus (belum diverifikasi penguji) | 1 — rakit sendiri |
| Tanpa instalasi untuk pembeli awam (2) | 2 — Python standar | 0 — butuh `uvx`/paket Python | 0 — butuh paket + modul Odoo (mode aman) |
| Keamanan tulis (2) | 2 — daftar izin metode + draf saja + anti-dobel (terbukti) | 2 — alur izin 3 langkah + flag ENV (lebih umum) | 1 — aman bila modul dipasang; YOLO penuh berbahaya |
| Bahasa Indonesia, Rupiah, laporan Telegram tersamar (1) | 1 | 0 | 0 |
| **Total (10)** | **10** | **5** | **3–4** |

## Kelebihan pesaing yang patut dipelajari (tulis ulang dengan cara sendiri, jangan salin)
- Cakupan model jauh lebih luas (CRM, pembelian, akuntansi umum); multi-instance.
- Agregasi di sisi server (`read_group`) — lebih cepat untuk data besar dibanding `search_read` berhalaman (odoo-usaha membatasi 10.000 baris).
- erpipe: token validasi berkedaluwarsa untuk penulisan — mirip ide "kode perintah" odoo-usaha, tetapi berlaku umum.

## Kesimpulan
Untuk tugas & audiens target (pemilik UMKM awam, Rupiah, WIB, laporan Telegram), **odoo-usaha unggul**. Pesaing unggul untuk integrator teknis yang butuh cakupan luas. Skill tidak kalah → tidak ada batas skor 6 dari kriteria ini.
