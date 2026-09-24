# Sumber resmi & hasil verifikasi (diakses 24 September 2026)

Semua fakta tentang Dolibarr di skill ini diambil dari sumber resmi **dan** dicoba langsung pada Dolibarr asli yang dijalankan di container uji Komunitech.

## Sumber
| Fakta | Sumber (diakses 2026-09-24) |
|---|---|
| Versi stabil terbaru **24.0.1** (rilis 7 Sep 2026; 24.0.0 rilis 20 Agu 2026) | https://github.com/Dolibarr/dolibarr/releases/tag/24.0.1 · tag git `24.0.1` di https://github.com/Dolibarr/dolibarr |
| DoliWamp terbaru di SourceForge **22.0.4** (diubah 9 Jan 2026) | https://sourceforge.net/projects/dolibarr/files/Dolibarr%20installer%20for%20Windows%20(DoliWamp)/ |
| DoliWamp = Dolibarr + Apache + MariaDB + PHP sekali instal untuk Windows; upgrade harus dengan DoliWamp versi baru | https://wiki.dolibarr.org/index.php/Dolibarr_for_Windows_(DoliWamp) · `dev/build/exe/doliwamp/README.md` di repo |
| Default DoliWamp: folder `c:\dolibarr`, Apache port 80, MariaDB port 3306, sandi awal database `changeme` (bisa diganti saat instal), data di `c:\dolibarr\dolibarr_documents`, menu Start "Start/Stop DoliWamp server" | `dev/build/exe/doliwamp/doliwamp.iss`, `install.forced.php.install` (tag 22.0.4 & 24.0.1) |
| Apache DoliWamp `Listen <port>` (semua antarmuka) dan alias `/dolibarr` `Require all granted` → **bisa diakses dari jaringan** bila firewall mengizinkan | `dev/build/exe/doliwamp/httpd.conf.install`, `dolibarr.conf.install` |
| Modul REST: "API / Web services (REST server)", endpoint `/api/index.php/...`, header `DOLAPIKEY`, explorer `/api/index.php/explorer` | https://wiki.dolibarr.org/index.php?title=Module_Web_Services_API_REST_(developer) · `htdocs/api/class/api_access.class.php` |
| Batas PHP installer: min 7.1, peringatan di atas 8.5 | `htdocs/install/check.php` (24.0.1) |
| Kamus tarif PPN bawaan **tidak** berisi tarif Indonesia (negara 118) → harus ditambah manual | `htdocs/install/mysql/data/llx_c_tva.sql`, `llx_00_c_country.sql` (118 = ID Indonesia) |
| Mata uang IDR tersedia; bahasa `id_ID` tersedia (terjemahan sebagian) | `llx_c_currencies.sql`, `htdocs/langs/id_ID/` |
| Hak akses (id): 11 baca invoice, 12 buat/ubah invoice, 14 validasi, 16 pembayaran, 19 hapus; 121 baca pihak ketiga, 122 buat/ubah, 262 lihat semua pihak ketiga; 31 baca produk; 1001 baca stok; 342 ubah user sendiri | tabel `llx_rights_def` Dolibarr 24.0.1 |

## Perilaku API yang diamati langsung (Dolibarr 24.0.1 & 22.0.4, PHP 8.4, MariaDB 10.11)
| Situasi | Respons asli |
|---|---|
| `GET /status` | `{"success":{"code":200,"dolibarr_version":"24.0.1","access_locked":"0",...}}` (butuh kunci) |
| Modul API mati | HTTP **200** berisi HTML "Module **Api** must be enabled" / "Modul **Api** harus diaktifkan" |
| Tanpa kunci / kunci salah | **401** JSON `{"error":{"code":401,"message":"Unauthorized: ..."}}` |
| Modul Invoice dimatikan | **403** "Forbidden" (bukan 501) karena hak ikut modul |
| Endpoint tak dikenal | **501** teks "API not found (failed to include API file)" |
| Daftar pihak ketiga kosong | **404** "Not Found: No third parties found"; daftar invoice/produk kosong = `[]` |
| `GET /users/info` | 403 bila user tidak punya hak 342 (ubah user sendiri) atau 251; admin/hak 342 → berisi `rights` |
| `GET /setup/modules` | hanya admin (403 untuk user biasa) |
| `POST /users` dengan `api_key` | **405** "api_key can't be set/modified using the APIs" → kunci dibuat lewat layar Dolibarr |
| Angka | string 8 desimal, mis. `"total_tva":"36557.95000000"`; `remaintopay` dihitung server; tanggal = timestamp detik |
| Kode pelanggan | `code_client:"auto"` → dibuat otomatis (mis. `CU2609-00001`) |
| `POST /invoices` dengan `lines` sekaligus | berhasil tetapi memunculkan PHP Warning; script memakai `POST /invoices` lalu `POST /invoices/{id}/lines` per baris (tanpa warning) |
| PPN per baris | 12.345 × 11% = 1.357,95 disimpan apa adanya (2 desimal); dengan "Maks. desimal harga total" = 0 → 1.358 |
| `status=unpaid` | berisi juga invoice yang sudah dibayar penuh tapi belum ditutup (`remaintopay` = 0) |
| Filter `sqlfilters` | `(t.nom:like:'%x%')`, `(t.rowid:in:1,2)`, `(t.datef:=:'2026-09-24')` berfungsi di 22.0.4 & 24.0.1 |

## Belum diverifikasi
- DoliWamp Windows sungguhan (instal, layanan otomatis saat boot, firewall).
- Dolibarr di bawah 22 atau 25+.
- Modul multicompany, multi-mata-uang.
