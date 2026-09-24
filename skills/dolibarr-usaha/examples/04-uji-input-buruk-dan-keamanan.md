# 04 (uji independen) — Input buruk, galat Dolibarr, dan uji keamanan kunci API

**Penguji:** agent independen, 2026-09-24. Dolibarr **24.0.1 asli** + server tiruan kecil buatan penguji (`tangkap.py`: redirect 302, penggema header, HTML 200, penangkap proxy) di 127.0.0.1. Kunci fiktif.

## A. Galat koneksi & konfigurasi
| Kasus | Perintah | Keluaran | Kode | Nilai |
|---|---|---|---|---|
| Kunci salah (401, Dolibarr asli) | `DOLIBARR_API_KEY=kunciSalah-… cek` | "Kunci API ditolak Dolibarr (401)…" + Saran buat ulang kunci | 5 | ✅ kunci tidak tampil (juga di `--json`) |
| Dolibarr mati | `stok --url http://127.0.0.1:8111/dolibarr` | "tidak bisa dihubungi ([Errno 111] …)" + Saran Start DoliWamp | 3 | ✅ |
| URL salah | `cek --url http://127.0.0.1:8098/salah` | "Alamat API tidak ditemukan (404)" | 2 | ✅ |
| Modul API mati (Dolibarr asli, `unActivateModule`) | `cek` | "Modul 'API / Web services (REST server)' … belum aktif" + menu | 4 | ✅ |
| User hanya-baca (121,262,11,31,1001) menulis | `invoice buat … --ya`, `pelanggan tambah … --ya` | "Ditolak Dolibarr (403 …)" + Saran | 5 | ✅ tidak ada yang tertulis |
| Tanpa kunci | `HOME=kosong cek` | "Kunci API Dolibarr belum diatur" + "Jangan tempel kunci di chat" | 5 | ✅ |
| File kunci 644 | `chmod 644 …; stok` | "bisa dibaca pengguna lain … chmod 600" | 5 | ✅ |
| URL publik http | `cek --url http://tokoku.example.com/dolibarr` | "bukan komputer ini" | 2 | ✅ |
| sama + `--izinkan-url-luar` | – | "Alamat internet wajib https://" | 2 | ✅ (juga `http://8.8.8.8`) |
| LAN `http://192.168.1.20` tanpa izin | – | ditolak | 2 | ✅; dengan izin → http + PERINGATAN, **tanpa proxy** |
| Sandi di URL / skema ftp | – | ditolak | 2 | ✅ |
| Zona `--tz PST` | – | "Pakai WIB, WITA, atau WIT" | 2 | ✅ |

## B. Item & argumen aneh (`invoice buat --pelanggan 6 --item …`)
| Item | Hasil | Nilai |
|---|---|---|
| `Semen|abc|62500`, `|0|`, `|-2|`, `|2|-5`, diskon 150, harga kosong, nama kosong | pesan jelas, kode 2 | ✅ |
| `Semen|2|62.500` / `Rp 62.500,50` / `10%` / qty `1.5` | 62.500 / 62.500,50 / 10% / 1,5 | ✅ |
| `Semen|2|62,500` (gaya Inggris) | dibaca **Rp 62,50**, total Rp 138 | ⚠️ terlihat di pratinjau, tapi rawan bagi awam (R2) |
| `Semen|1e3|62500` | diterima sebagai 1.000 sak | ⚠️ R1 |
| `Semen|NaN|62500`, `Semen|2|Infinity`, `Semen|2|1e30` | **Traceback** `decimal.InvalidOperation` (dolibarr.py:641, :109), kode 1 | ❌ R1 |
| `--jatuh-tempo 99999999` | **Traceback** `OverflowError` (dolibarr.py:718) | ❌ R1 |
| `--pelanggan 999` / `abc` / `@TIDAKADA` / `--jatuh-tempo -3` / `--tanggal 31/02/2026` / tanpa `--item` | pesan jelas, kode 2 | ✅ |
| `pelanggan cari "') or (1=1"` | dibersihkan jadi `or 1=1`, 0 hasil | ✅ tidak ada injeksi sqlfilters |
| Draf ganda (`--ya` diulang) | DIBATALKAN, sebut PROV11 | ✅ |
| Pelanggan ganda: nama mirip | ditolak tanpa `--tetap-buat` | ✅ |
| Pelanggan ganda: **nomor telepon sama, nama beda** ("Ibu Rina Wati" vs "Bu Rina Wati") | lolos tanpa peringatan | ❌ S4 |

## C. Tidak ada penulisan tanpa `--ya`
Log PHP server: POST oleh skill hanya `thirdparties` ×1 (UD Sinar, setelah `--ya`), `invoices` + `invoices/{id}/lines` untuk PROV11/14/15 (setelah `--ya`). Semua pratinjau (±25 kali) → 0 POST. Jumlah baris `llx_facture`/`llx_societe` tidak berubah oleh pratinjau. Grep statis: hanya `GET` dan 3 jalur `POST`; tidak ada PUT/DELETE/validate/payments. ✅

## D. Kebocoran kunci API
| Uji | Hasil |
|---|---|
| Semua keluaran uji (teks, `--json` cek/piutang/stok/laporan/cari, galat) di-grep untuk kunci penuh | 0 ditemukan ✅ |
| Server menggemakan header `DOLAPIKEY` di pesan galat 500 | tampil `****5Wf1` (teks & JSON) ✅; kunci < 12 karakter → `****` ✅ |
| Redirect 302 dari 127.0.0.1:8201 ke :8202 | "Dolibarr mengalihkan … Kunci API tidak dikirim ulang", kode 6; log :8202 **kosong** ✅ |
| `http_proxy=http://127.0.0.1:8203`, `no_proxy` kosong, alamat lokal | penangkap proxy **tidak menerima apa pun** dari skill; pembanding `urllib` biasa **terkirim** ke proxy (uji sah) ✅ |
| `simpan-kunci` | file 600, folder 700, keluaran `****5Wf1` ✅ |
| Kunci berisi baris baru (file kunci 2 baris lewat `--kunci-file`, atau `DOLIBARR_API_KEY=$'abc\nbaris2'`) | **Traceback** `ValueError: Invalid header value b'kunciDuaBaris-AAAABBBB\nbaris2'` → **isi kunci tercetak utuh, tidak tersamar** (dolibarr.py:218-230 tanpa validasi; :316-318 ValueError tidak ditangkap; traceback tidak lewat `samarkan`) | ❌ **S3** |
| `--kunci-file` menunjuk file 600 lain (mis. kunci SSH satu baris) | isinya dikirim sebagai header ke Dolibarr **lokal** saja | rendah (catatan) |

## E. Hak user API (pertahanan lapis kedua)
Dolibarr 24.0.1 `api_invoices.class.php:1206-1208` (`validate`) dan `:1262-1264` (`settopaid`) hanya memeriksa hak **`facture creer` (12)**. Dengan kunci `api_tulis` (hak persis panduan §6.3, tanpa "Validasi"/"pembayaran"), panggilan API langsung:
- `POST invoices/8/validate` → **berhasil**, PROV8 menjadi `IN2609-0010` (fk_user_valid = api_tulis)
- `POST invoices/8/settopaid` → **berhasil**, `paye=1`
- `DELETE invoices/11` dan `POST invoices/4/payments` → 403 ✅
Hak 14 "Validate invoices" berjenis `invoice_advance` dan disembunyikan di layar Izin bila `MAIN_USE_ADVANCED_PERMS` mati (`user/perms.php:496`). Jadi saran panduan §6.4 "Jangan berikan: Validasi faktur" tidak melindungi apa pun, dan `cek` tidak memperingatkan hal ini. Script sendiri tetap tidak punya perintah itu → risiko hanya bila agent melanggar SKILL.md (curl langsung/prompt injection). → **S2** (klaim dokumentasi).

**Hasil skenario: LULUS sebagian** — tidak crash pada galat umum, tidak menulis tanpa `--ya`, redirect/proxy/penyamaran terbukti; tetapi S3 (kunci tercetak), S4, R1, R2.
