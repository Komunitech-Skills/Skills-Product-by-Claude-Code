# 00 — Banding pesaing: skill/MCP Dolibarr publik vs dolibarr-usaha (skenario 01)

Pesaing hanya **dibaca untuk dinilai** (clone ke scratchpad, tidak dijalankan, tidak disalin). Tanggal riset: 24 Sep 2026.

## Pencarian
Kata kunci: "dolibarr" di skills.sh (API pencarian), ClawHub (halaman cari: "No matches for 'dolibarr'"; API tidak bisa dijangkau dari container), GitHub ("dolibarr mcp", urut bintang), web ("Dolibarr skill clawhub / skills.sh / SKILL.md"). MCP registry resmi (`registry.modelcontextprotocol.io`) timeout.

| Kandidat | Sumber | Bukti pemakaian | Sifat | Relevan? |
|---|---|---|---|---|
| **latinogino/dolibarr-mcp** | GitHub, MIT, 18★, 11 fork, 6 issue, dibuat Jul 2025, commit terakhir Feb 2026 | paling mapan | MCP server Python (butuh `pip install` mcp/aiohttp/pydantic/uvicorn), CRUD penuh + `delete_*`, `validate_invoice`, `dolibarr_raw_api` | **Dipakai untuk uji banding** |
| digitalfactorysn/mcp-dolibarr | GitHub, MIT (package.json), 12★, 12 fork, Apr 2026 | ada | MCP TypeScript "55+ alat", Prancis, `validate_invoice`, `delete_invoice_line`, contoh TVA 18% (Senegal) | Mirip, cakupan lebih luas, lebih berisiko |
| jeffsenso/dolibarr-skills → dolibarr-development | skills.sh, 29 instal | rendah | Pengembangan **modul** Dolibarr (kode PHP) | Bukan untuk operasional usaha |
| sandeeprdy1729/skill_galaxy → dolibarr-mcp-connector | skills.sh, 1 instal | tidak ada | SKILL.md tidak dapat diunduh (404) | Gugur |
| momodemo333/emmcp, homeserverhq, marioser, dll. | GitHub 1–3★ | tidak ada | MCP server lain | Gugur (≤3★) |

URL: https://github.com/latinogino/dolibarr-mcp · https://github.com/digitalfactorysn/mcp-dolibarr · https://skills.sh/jeffsenso/dolibarr-skills/dolibarr-development · https://skills.sh/sandeeprdy1729/skill_galaxy/dolibarr-mcp-connector

Tidak ada skill/MCP Dolibarr berbahasa Indonesia atau yang memahami PPN 12% × DPP 11/12.

## Uji banding skenario 01
Pesaing tidak dipasang (dependensi PyPI + klien MCP). Penguji membaca `create_invoice` (skema alat `dolibarr_mcp_server.py:504-569`, klien `dolibarr_client.py:653-681`: `customer_id→socid`, `product_id→fk_product`, sisanya diteruskan apa adanya) lalu **mengirim payload yang sama persis** ke Dolibarr 24.0.1 asli. Skema baris hanya punya `desc, qty, subprice, total_ht, total_ttc, vat, product_id, product_type` (tidak ada diskon), jadi agent menurunkan harga cat ke 80.937,5.

```
POST invoices {"socid":6,"date":"2026-09-24","due_date":"2026-10-24","lines":[
  {"desc":"Semen Tiga Roda 40kg","qty":20,"subprice":62500,"vat":11,"fk_product":11,"product_type":0},
  {"desc":"Cat Tembok Putih 5kg (diskon 7,5%)","qty":4,"subprice":80937.5,"vat":11,"product_type":0},
  {"desc":"Ongkos kirim truk","qty":1,"subprice":150000,"vat":11,"product_type":1}]}
→ (PROV12): DPP 1.723.750 | PPN **0** (tva_tx 0 di semua baris) | total 1.723.750 | jatuh tempo **2026-09-24**
```
Field `vat` dan `due_date` tidak dikenal Dolibarr → **PPN hilang dan jatuh tempo diam-diam jadi tanggal invoice**, tanpa pesan galat. (Alat `add_invoice_line` pesaing memakai field `vat` yang sama.) Tidak ada pratinjau, cek ganda, atau pencocokan; tersedia `validate_invoice`, `delete_invoice`, dan raw API tanpa konfirmasi; kunci API di `.env`/konfigurasi Claude Desktop.

## Skor berdampingan (penguji, 1–5)
| Kriteria | latinogino/dolibarr-mcp | dolibarr-usaha |
|---|---|---|
| Angka invoice benar (PPN, diskon, tempo) | 1 | 5 |
| Konteks pajak Indonesia (11/12, Coretax, disclaimer) | 1 | 5 |
| Keamanan tindakan (draf saja, pratinjau, tanpa hapus/validasi) | 1 | 4 (S2) |
| Keamanan kunci (file 600, samaran, tanpa proxy/redirect) | 2 | 4 (S3) |
| Cakupan fitur (order, proyek, kontak, CRUD) | 5 | 2 |
| Piutang berumur / stok menipis / laporan harian | 1 | 4 (S1) |
| Tanpa instalasi paket | 2 | 5 |
| Bahasa Indonesia, pengguna awam | 1 | 5 |
| **Total** | **14/40** | **34/40** |

Kelebihan pesaing yang layak dipelajari (ditulis ulang sendiri, bukan disalin): alat pencarian produk per kode/label di sisi server; cakupan pesanan (order) dan kontak.

**Kesimpulan:** dolibarr-usaha **unggul jelas** untuk UMKM Indonesia; pesaing terbaik menghasilkan invoice tanpa PPN dan tanpa jatuh tempo pada skenario yang sama.
