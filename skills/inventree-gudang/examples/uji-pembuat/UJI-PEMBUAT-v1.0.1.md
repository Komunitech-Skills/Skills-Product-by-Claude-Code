# Catatan uji pembuat — inventree-gudang v1.0.1

**Penguji:** pembuat (Akun A), 2026-09-29. Menindaklanjuti `examples/HASIL-UJI.md` (uji independen v1.0.0, 8/10). Bukan uji independen — uji ulang skenario 03 & redirect oleh penguji independen masih diperlukan.

## Perbaikan
| Temuan | Perbaikan v1.0.1 | Bukti |
|---|---|---|
| M1 IPN persis dianggap ambigu (`PK-05` vs `PK-05B`) | `pilih_baris_po`: `#id` barang → IPN persis → nama persis → SKU persis → baru potongan kata; ambigu hanya di tahap potongan; pesan pilihan menampilkan IPN, #id, SKU; baris PO yang sama disebut dua kali ditolak | 5 uji regresi baru (`TesV101`) |
| S1 redirect membawa token | Opener khusus `_TolakPengalihan`: redirect apa pun → berhenti (kode 4), tidak ada permintaan ke alamat tujuan | `test_redirect_tidak_diikuti_token_tidak_bocor` (302 GET & 307 POST; server tujuan menerima 0 permintaan). Uji ini **gagal** pada kode v1.0.0 (dicoba dengan mengembalikan `urlopen`) |
| S2 proxy ENV dipakai | `ProxyHandler({})` untuk localhost/127.0.0.1/::1/*.localhost/LAN; alamat internet (HTTPS + `--izinkan-jarak-jauh`) tetap memakai proxy sistem | `test_proxy_env_diabaikan_untuk_localhost` (proxy penangkap menerima 0 permintaan; juga **gagal** pada v1.0.0) + `test_opener_lokal_tanpa_proxy_internet_pakai_proxy`. Server asli: `HTTP_PROXY=http://127.0.0.1:9` (proxy mati) + `NO_PROXY` kosong → semua perintah tetap jalan (`transkrip-v1.0.1-inventree-1.5.6.txt`) |
| D1 urutan mata uang | Panduan §5.1: Supported Currencies dulu, baru Default Currency | — |
| D2 sandi & token akun AI | Panduan §6b/c langkah demi langkah (Add User tanpa sandi → ⋮ Change Password [superuser] → Groups → login sebagai akun AI → Access Tokens), dicocokkan dengan kode frontend 1.5.6 (`UserTable.tsx`, `ApiTokenTable.tsx`) | — |
| L1 kemasan pemasok | `po-terbuka`, pratinjau & TERSIMPAN menampilkan setara stok (`+1 kemasan pemasok = +6 stok`) | `test_kemasan_pemasok_ditampilkan` |
| L2 BO Pending | `stok-menipis` memakai max(`building`, `scheduled_to_build`) | `test_produksi_menunggu_ikut_dihitung` |
| L3 catatan per baris | Tampil di pratinjau, ditempel ke catatan transaksi (dipotong ≤ 500 karakter; batas kolom InvenTree 512) | 2 uji |
| L4 batch per baris | SKILL.md: pecah per batch | — |
| L5 stocktake_date | SKILL.md & pesan pratinjau diperjelas | — |
| L6 | Folder `~/.komunitech` dibuat 700; peringatan http-LAN sekali; 502/503/504 menyarankan `docker compose ps` | 2 uji |
| L7/L8 | Panduan §2: `nano`/Notepad, `invoke update` butuh internet 5–15 menit, sandi tidak terlihat; status Docker diuji penguji independen | — |

## Hasil
- `python3 tests/uji_regresi.py` → **75 test OK** (61 lama + 14 baru).
- Server asli InvenTree 1.5.6 (instalasi manual pembuat): `cek`, `po-terbuka`, `terima-barang` (IPN persis & nama persis, `--ya`), `stok-menipis` dengan proxy mati di ENV → semua benar; PO-0001 sisa 50 → 40 kg.
- `python3 scripts/validate.py` lolos.
