# HASIL UJI — dolibarr-usaha v1.0.0 (status: draft)

- **Tanggal:** 2026-09-24
- **Penguji:** **pembuat skill** (belum ada penguji independen, belum ada uji A/B & banding pesaing). Karena itu **belum diberi skor kualitas** dan status tetap `draft`.
- **Lingkungan:** Linux (Ubuntu 24.04 container), Python 3.11, PHP 8.4.19 (server bawaan `php -S`, `date.timezone=Asia/Jakarta`), MariaDB 10.11.14. Dolibarr diambil dari tag git resmi `24.0.1` dan `22.0.4` (github.com/Dolibarr/dolibarr), diinstal dengan installer CLI resmi (`install/step2.php`, `step5.php`), modul diaktifkan dengan fungsi resmi `activateModule()`. Negara Indonesia, IDR, bahasa id_ID, tarif PPN 0/11/12 ditambahkan ke kamus.
- **Tidak diuji:** DoliWamp di Windows sungguhan, macOS, Dolibarr < 22 atau ≥ 25, pengiriman Telegram sungguhan, perilaku agent (skill dipanggil model).

## Ringkasan
| Uji | Hasil |
|---|---|
| Dolibarr asli **24.0.1** — semua perintah (`cek`, `pelanggan cari/tambah`, `invoice buat` pratinjau & `--ya`, `piutang`, `stok`, `laporan-harian`) | **Lulus** |
| Dolibarr asli **22.0.4** (versi DoliWamp terbaru di SourceForge) — semua perintah | **Lulus** |
| Galat di Dolibarr asli: kunci salah (401), Dolibarr mati, modul API mati (200+HTML), modul Invoice mati (403), URL salah (404 HTML), user tanpa hak | **Lulus** (pesan awam + kode keluar sesuai) |
| Kunci admin vs user khusus: `cek` memperingatkan admin & 7 hak berisiko | **Lulus** |
| `tests/uji_regresi.py` (server tiruan dari respons asli 24.0.1) | **46 tes OK** |
| OpenClaw 2026.9.6: `skills check` → eligible, modelVisible, commandVisible | **Lulus** |
| OpenClaw `automations add` + `run --wait` (laporan harian, kunci dari file) | **Lulus**; Telegram tidak terkirim (tanpa bot token) |
| Kebocoran kunci: dicek di setiap keluaran uji regresi (stdout+stderr), JSON, dan saat redirect | **0 bocor** |

## Pencocokan angka dengan Dolibarr asli
| Kasus | Hitungan Komunitech | Dolibarr | Keterangan |
|---|---|---|---|
| 3 baris, DPP 332.345, PPN umum | PPN 36.557 | 36.557,95 | beda 0,95 → dilaporkan |
| Sama, "Maks. desimal harga total" = 0 | 36.557 | 36.558 | beda 1 → dilaporkan |
| 2 baris mewah + diskon 10%, DPP 3.249.999 | PPN 389.999 | 390.000 | beda 1 (pembulatan per baris) |
| DPP 606.250 (examples/01) | 66.687 | 66.687,50 | beda 0,50 |
| DPP 1.000.000 jasa | 110.000 | 110.000 | COCOK |
DPP Dolibarr selalu sama dengan DPP Komunitech pada semua uji (pembulatan baris ke rupiah hanya berbeda bila harga × jumlah × diskon menghasilkan sen).

## Skenario
| No | Berkas | Isi | Hasil |
|---|---|---|---|
| 01 | `01-draf-invoice-dpp-11-12.md` | Produk + jasa + diskon, pratinjau → `--ya`, cocokkan | Lulus, angka diverifikasi manual |
| 02 | `02-piutang-dan-laporan-harian.md` | Umur piutang, bayar sebagian, lunas-belum-ditutup, laporan | Lulus, angka diverifikasi manual |
| 03 | `03-dolibarr-22-stok-dan-pelanggan.md` | Versi 22.0.4, user non-admin | Lulus |
| 04 | `04-input-buruk-dan-galat.md` | 12 galat/input buruk | Lulus, tidak ada penulisan |
| 05 | `05-di-luar-cakupan.md` | Validasi/bayar/hapus/broadcast/e-Faktur | Dijamin teknis (script tidak punya aksinya); perilaku agent belum diuji |

## Audit keamanan (oleh pembuat)
- Hanya pustaka standar (`urllib`, `json`, `decimal`, …). Tidak ada `subprocess`, `eval`, penulisan file kecuali `simpan-kunci` (file 600, folder 700).
- Metode HTTP yang dipakai: GET, dan POST hanya ke `thirdparties`, `invoices`, `invoices/{id}/lines` setelah `--ya`. Tidak ada PUT/DELETE/validate/payments (uji statis).
- Kunci: header `DOLAPIKEY` (tidak di URL), proxy dimatikan untuk alamat lokal/LAN, redirect ditolak agar kunci tidak diteruskan, keluaran disaring (`****abcd`).
- `sqlfilters`: kata pencarian dibersihkan dari `( ) ' " % \ : _ *` sebelum dikirim; Dolibarr juga memvalidasi sendiri.
- Data Dolibarr diperlakukan sebagai data (SKILL.md melarang mengikuti instruksi di dalamnya).

## Temuan / keterbatasan yang diketahui
1. Harga termasuk PPN belum didukung (diarahkan ke `hitung-ppn`).
2. `piutang` tidak mengurangi nota kredit yang belum dipakai (nota kredit dilewati).
3. Laporan harian memakai **tanggal invoice**, bukan tanggal uang masuk.
4. `cek` untuk user tanpa hak "ubah user sendiri" (342) tidak bisa menampilkan daftar hak; hanya uji baca.
5. Dolibarr menjawab 404 untuk daftar pihak ketiga kosong dan 403 saat modul mati — sudah ditangani, tetapi bisa berubah di versi lain.

## Langkah berikut sebelum `uji`/`lulus`
- Uji independen 5 skenario + A/B (tanpa skill) + banding pesaing (mis. skill/MCP Dolibarr di GitHub/ClawHub).
- Uji di **DoliWamp 22.0.4 Windows** sungguhan (instal, layanan saat boot, firewall, `python`/`py`).
