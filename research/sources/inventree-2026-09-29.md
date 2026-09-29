# Riset sumber — InvenTree (inventree/InvenTree)

**Tanggal riset:** 2026-09-29
**Peneliti:** sesi Komunitech Skills Factory (agent pembuat, Akun A) — diverifikasi terhadap kode sumber resmi dan **rilis resmi yang benar-benar dijalankan** (§3).
**Konteks:** jalur 2 (produk siap pakai pengganti SaaS) untuk member VIP manufaktur/distribusi/retail (`research/kebutuhan-member-vip-2026-09-29.md`: paket "Kantor & Manajemen", ±8 member manufaktur/distribusi/logistik) — kebutuhan stock opname, inventori multi-lokasi & batch, BOM/produksi, penerimaan PO. Kandidat sudah tercatat di `research/software-pengganti-saas-2026-09-23.md` §2.4.

## 1. Identitas & sumber resmi
| Item | Nilai |
|---|---|
| Nama produk | **InvenTree** — "Open Source Inventory Management System" |
| Pembuat / pemelihara | Organisasi GitHub `inventree` (pengembang inti: Oliver Walters dkk.), proyek sejak 2017 |
| Repo | https://github.com/inventree/InvenTree |
| Dokumentasi | https://docs.inventree.org |
| Lisensi | **MIT** — file `LICENSE`: "MIT License, Copyright (c) 2017 - InvenTree Developers" (dicek di tag 1.5.6) |
| Bintang / fork (29 Sep 2026, GitHub API) | **7.654★ / 1.565 fork**, 162 issue terbuka, push terakhir 29 Sep 2026 |
| Rilis stabil terbaru | **1.5.6** (26 Sep 2026; tag `1.5.6`, commit `284a670413cc`); sebelumnya 1.5.5 (17 Sep), 1.5.4 & 1.5.3 (8 Sep), 1.5.2 (25 Agu) — rilis patch rutin |
| API | REST (Django REST Framework), token `inv-...` (kedaluwarsa bawaan 365 hari), versi API 530 pada 1.5.6; klien Python resmi `inventree-python` (tidak dipakai — skill kita stdlib saja) |
| Instalasi resmi | Docker (disarankan), paket installer (Debian/Ubuntu), bare metal (Python ≥ 3.12). Windows via WSL/Docker |

## 2. Sinyal bukti (CLAUDE.md Tahap 2 — wajib ≥ 3)
1. **Popularitas:** 7.654★ (ambang repo satu produk ≥ 100★), 1.565 fork.
2. **Umur & perawatan:** sejak Maret 2017, rilis bertahap (1.5.2 → 1.5.6 dalam 5 minggu, patch rutin), commit harian.
3. **Dipakai komunitas:** issue/PR dari banyak kontributor luar, terjemahan komunitas ±40 bahasa termasuk `id` (Crowdin), ekosistem plugin & aplikasi Android resmi.
4. **Kualitas isi:** test suite besar (`src/backend/InvenTree/*/tests*.py`), dokumentasi API/skema lengkap, requirements ter-pin dengan hash SHA-256.
**Kesimpulan:** sumber **kuat** → prioritas kurasi (keputusan pemilik 2026-09-26).

**Alternatif yang ditimbang:** Dolibarr modul stok (sudah ada `dolibarr-usaha`, GPL, lebih ke ERP umum), Frappe Books (sudah ada, inventori sederhana), ERPNext/Odoo (terlalu besar), Grist (tanpa logika stok). InvenTree paling pas untuk kebutuhan **lokasi + batch + BOM + PO receiving + opname** dengan lisensi paling longgar (MIT).

## 3. Cara verifikasi (kejujuran metodologi)
1. Tag `1.5.6` di-*clone* ke scratchpad (di luar `Skills/`, tidak masuk git). Dibaca: `stock/api.py` & `stock/serializers.py` (endpoint `count/`, field item), `part/api.py` (filter `low_stock`, `search`, `active`), `order/api.py` & `order/serializers.py` (`po/<pk>/receive/`, field `line_item`, `batch_code`, `expiry_date`, status PO), `build/status_codes.py`, `users/ruleset.py` & `users/models.py` (role, token `inv-`, kedaluwarsa 365 hari), `contrib/container/*` (Docker resmi). **Tidak ada kode yang disalin** ke skill.
2. **Audit keamanan instalasi (Tahap 3):** `src/backend/requirements.txt` = paket PyPI ter-pin + hash (dipasang dengan `pip --require-hashes`). `tasks.py` (2.603 baris) **tidak dijalankan** — kami memanggil `manage.py migrate`/`createsuperuser` dan `gunicorn` langsung, sehingga tidak ada unduhan tambahan (fungsi `frontend-download` di `tasks.py` mengunduh build frontend dari GitHub Releases resmi; tidak dipakai). `docker-compose.yml` resmi: image resmi, hanya proxy Caddy yang mem-publish port (bawaan `0.0.0.0:80/443` → panduan mewajibkan `127.0.0.1:`).
3. **Dijalankan sungguhan:** Python 3.12 venv, SQLite, `INVENTREE_PLUGINS_ENABLED=False`, gunicorn terikat `127.0.0.1:8000`. `GET /api/` → `{"server":"InvenTree","version":"1.5.6","apiVersion":530}`.
4. Data fiktif "UD Sumber Rasa" (pabrik keripik): 3 kategori, 5 lokasi (Gudang Utama/Rak A/Rak B, Ruang Produksi, Toko Depan), 8 barang (bahan baku kg/L, kemasan, 2 produk rakitan), 11 item stok ber-batch, BOM 2 produk, 2 pemasok, 2 PO berstatus Placed, 1 perintah produksi. Grup `Agen Baca` (view) & `Agen Gudang` (+add/change Stock & PO) dengan token masing-masing.
5. **Temuan nyata saat uji** (masuk panduan/skill):
   - Mata uang bawaan tidak termasuk IDR → pemasok `currency: IDR` ditolak 400 "not a valid choice" sampai `CURRENCY_CODES`/`INVENTREE_DEFAULT_CURRENCY` diatur.
   - Hak grup diterapkan ke izin Django oleh **worker** latar belakang; tanpa worker, `/api/user/roles/` sudah menampilkan hak tetapi aksi tulis tetap 403.
   - Daftar tanpa `limit` dikembalikan sebagai list biasa; dengan `limit` sebagai `{count, results}` — script menangani keduanya.
   - PO yang semua barisnya diterima otomatis berstatus Complete; terima barang ke PO non-Placed ditolak 400.
   - Token salah → 401 `Invalid token.`; kurang hak → 403 — berbeda dari Vikunja (yang memakai 401 untuk keduanya).
6. Semua perintah skill dijalankan terhadap server ini (transkrip: `skills/inventree-gudang/examples/uji-pembuat/transkrip-inventree-1.5.6.txt`); jawaban server direkam jadi fixture uji regresi.
7. **Belum diuji:** Docker (daemon tidak tersedia di sandbox), Windows/macOS, tampilan web (frontend tidak dibangun), worker `invoke worker`, pengiriman Telegram.

## 4. Keputusan kurasi
- **Jalur:** kurasi software (jalur 2) + skill orisinal Komunitech `inventree-gudang` (klien REST stdlib). InvenTree **tidak didistribusikan**; pembeli memasang dari sumber resmi mengikuti `docs/panduan-inventree.md`.
- **Lisensi:** MIT → boleh dibundel pun, tapi tidak perlu; skill adalah karya terpisah via HTTP. Atribusi & "tidak berafiliasi" di `ATTRIBUTION.md`/README.
- **Nilai tambah:** opname via lembar CSV Excel-Indonesia + pengaman "stok berubah sejak draf", terima barang dengan validasi sisa PO/status/kemasan, kebutuhan bahan & maksimal produksi dihitung Decimal, laporan harian Telegram (pola OpenClaw terverifikasi dari `vikunja-tugas`), panduan pasang bahasa awam + setelan Indonesia (IDR, bahasa, satuan), pemisahan akun baca/gudang.
- Usulan tier: **ecer Rp149.000** (setara `frappe-books-usaha`; kandidat paket "Kantor & Manajemen" VIP).
