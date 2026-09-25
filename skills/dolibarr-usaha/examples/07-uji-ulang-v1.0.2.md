# 07 — Uji ulang independen v1.0.2 (setelah revisi N1/N2/kosmetik)

- **Tanggal:** 2026-09-25 (jam server 13.34–13.45 WIB)
- **Penguji:** agent penguji independen (Claude Code, simulasi agent). Bukan pembuat skill dan bukan pembuat revisi v1.0.2. Tidak mengubah kode.
- **Lingkungan:** **Dolibarr 24.0.1 asli** — instalasi penguji v1.0.0 (tag resmi, `src24`) dihidupkan ulang dari scratchpad dengan **salinan database** sendiri (`uji3-dolibarr/db`, MariaDB 10.11.14 port 3317) + PHP 8.4.19 `php -S` (`Asia/Jakarta`) di 127.0.0.1:8098, dan server kedua di alamat LAN kontainer `172.17.0.1:8097` (untuk `--izinkan-url-luar`). Python 3.11.15. Skill disalin ke scratchpad, `HOME` palsu. Kunci baru dibuat penguji untuk `api_baca` (`****4Qd8`) dan `api_tulis`/draf (`****1Ny5`) + kunci admin (`****8Rt6`). Data fiktif "Toko Bangunan Sumber Makmur" + pelanggan baru penguji "Warung Bu Sari Rejeki".
- **Tidak diuji:** Dolibarr 22.0.4, DoliWamp Windows, macOS, Python < 3.11, model asli di OpenClaw/Codex/Cursor, Telegram.

## A. Klaim revisi — status

| Klaim | Reproduksi penguji | Hasil |
|---|---|---|
| **N2** opsi umum di depan maupun di belakang | **Repro asli v1.0.1:** `--kunci-file ~/.komunitech/dolibarr-kunci-draf.txt simpan-kunci` → kini "Kunci akan disimpan di: …/dolibarr-kunci-draf.txt", file default **tidak berubah** (md5 sama, tetap `****4Qd8`). **Matriks 7 subperintah × 5 opsi × semua posisi** (depan / tengah untuk `pelanggan cari`, `pelanggan tambah`, `invoice buat` / belakang) = 84 kombinasi + 7 kontrol: `--url` port mati → kode 3, `--kunci-file` kunci salah → 401 kode 5, `--tz XYZ` → kode 2, `--json` → JSON, `--url` LAN + `--izinkan-url-luar` → tersambung + PERINGATAN http. **84/84 dihormati**, 0 diabaikan. `--url` depan + `--izinkan-url-luar` belakang (dan sebaliknya) → digabung benar. `--tz` benar-benar mengubah tanggal: dengan jam dipatok 25 Sep 16.30 UTC, `piutang`/`laporan-harian`/`invoice buat` WIB = 25 Sep, WIT/WITA = 26 Sep di posisi depan, tengah, dan belakang. Nilai beda di dua posisi (`--url`, `--tz WIT`/`WITA`, `--kunci-file a`/`b`) → kode 2 "ditulis lebih dari sekali dengan nilai berbeda", tidak ada yang dijalankan/dibuat | ✅ **TERBUKTI** |
| **N2** `simpan-kunci` menyebut path & tidak menimpa | Default ada → "sudah ada (berisi kunci ****4Qd8). Tidak ditimpa." kode 2 + saran `--kunci-file`/`--ya`; sama untuk file draf (opsi di belakang). `--ya` + kunci berspasi → ditolak kode 5 **sebelum** file dibuka; `--ya` + masukan kosong → "Kunci kosong. Tidak ada yang disimpan" kode 2; file tetap utuh. `--ya` di depan subperintah → ditolak (argumen tidak dikenal), bukan diam-diam | ✅ **TERBUKTI** |
| **N1** "Modul Stok belum aktif" lewat swagger.json | `unActivateModule('modStock')` (seperti tombol di layar Modul): admin, `api_baca` tanpa 342, `api_baca` + 342 → semua **"Modul Stok belum aktif … Status habis/menipis tidak dinilai"** kode 4 (v1.0.1: admin/342 mendapat diagnosis salah "hak kurang"). Modul aktif + `api_baca` tanpa hak 1001 → "User API belum punya hak 'Baca gudang dan stok' (modul Stok aktif)" kode 5 — benar. **Fallback** dengan `API_EXPLORER_DISABLED=1` (swagger membalas teks 200, bukan JSON): admin → `setup/modules` → "Modul Stok belum aktif" ✅; user non-admin (dengan/tanpa 342, modul mati atau hak kurang) → pesan gabungan jujur "modul belum aktif, atau … hak (Dolibarr tidak memberi tahu yang mana)". Laporan harian: bagian STOK "Tidak bisa dibaca: …", bagian lain tetap, kode 0. Tidak ada HABIS palsu di semua 7 keadaan | ✅ **TERBUKTI** (kosmetik: `cek` sendiri masih menulis "TIDAK BISA DIBACA (modul belum aktif, atau … hak)" tanpa memakai deteksi baru) |
| Kosmetik: pelanggan/draf ganda kode 7 | Pelanggan `+62 813 5555 7777` (tersimpan `081355557777`) → "nomor HP sama" kode 7, `--json` `ok:false, kode_keluar:7`. Draf ganda DPP bulat (Rp 152.400) → "TIDAK DIBUAT (kemungkinan dobel)" kode 7 (teks & JSON) | ✅ untuk kode keluar — ⚠️ lihat **B1**: draf ganda **tidak tertahan** bila DPP Dolibarr bersen |
| Kosmetik: laporan lampau menyebut tanggal draf | `laporan-harian --tanggal 2026-09-24` → "5 draf invoice bertanggal 2026-09-24 belum divalidasi"; hari ini → "bertanggal hari ini" (5 draf, cocok SQL) | ✅ |
| Kosmetik: lunas tanpa pembayaran | `IN2609-0010` (`paye=1`, 0 pembayaran) — laporan 24 Sep: "Belum dibayar dari penjualan ini: Rp 1.625.567,25" (v1.0.1: +Rp 11.100). SQL: hanya IN2609-0005 yang belum dibayar | ✅ |
| Panduan §6/§7, batas zona di SKILL.md | §6.1 langkah 3: peringatan hak invoice hanya bila 342 diberikan; "modul mati vs hak kurang dibedakan lewat daftar API, kecuali Explorer API dimatikan" — **cocok** dengan perilaku di atas. §6 ✅ "Untuk `api_draf` (bila diberi hak 342)". §7 langkah 2 menyebut path & penolakan menimpa. SKILL.md "Tanggal": batas 12 jam barat / 11 jam timur + server Amerika bisa bergeser 1 hari | ✅ |

## B. Regresi (skenario normal diulang, hitung ulang independen)
Kalkulator `Decimal` penguji terpisah (`hitung_independen.py`, tidak memakai kode skill) + SQL langsung.

| Kasus | Script | Penguji | Dolibarr (DB) |
|---|---|---|---|
| Pelanggan baru "Warung Bu Sari Rejeki" 0813-5555-7777 (pratinjau → `--ya`, kunci draf di **tengah**) | pratinjau 0 POST; TERSIMPAN ID 8 `CU2609-00008` | – | 1 POST thirdparties ✅ |
| Draf A (kunci draf di **depan**): `@SMN-40|15||4`, `@CAT-5|3|87.500|7,5`, `Ongkos kirim truk|1|137.345`, tempo 21 | baris 900.000 / 242.813 / 137.345; DPP 1.280.158; 11/12 1.173.478,17; PPN 140.817 (dari 140.817,38 ke bawah); total 1.420.975 | **sama** | 1.280.157,50 / 140.817,33 / 1.420.974,83 → "BEDA DPP −0,50; PPN +0,33; TOTAL −0,17" + penjelasan; per baris cocok DB (242.812,50 / 26.709,38 …) ✅ |
| Draf B `@PKU-7|5`, `Kawat bendrat|2|18.000|10` | 152.400; PPN 16.764; COCOK | sama | 152.400 / 16.764 ✅ |
| Piutang per 25 Sep | 10 invoice Rp 21.408.054,66; belum jatuh tempo 4 / Rp 4.295.754,75; 1–30: 2 / 4.802.970; 31–60: 2 / 7.261.975; > 90: 2 / 5.047.354,91; terlambat 6 / 17.112.299,91 | `DATEDIFF` + `llx_paiement_facture`: sama | ✅ 0 beda |
| Stok `--menipis` | KRM-40 MINUS beli 12; PKU-7 HABIS beli 30; CAT-5 beli 9; SMN-40 beli 95; PSR-1 6/6 aman | SQL sama | ✅ |
| Laporan 25 Sep | Rp 2.439.862,50; DPP 2.250.250; PPN 189.612,50; 2 invoice; naik 37,4% | SQL sama; 37,42% | ✅ |
| Laporan 24 Sep | Rp 1.775.417,25; 3 invoice; naik 670,8%; belum dibayar 1.625.567,25 | SQL sama; 670,83% | ✅ |

Seluruh sesi: **12 POST berhasil** = 1 pelanggan + 3 invoice + 8 baris, semuanya dari perintah `--ya` + 1 POST 403 (kunci baca mencoba `tambah --ya`, ditolak Dolibarr). 0 PUT/DELETE. Pratinjau: 0 POST.

## C. Keamanan (diulang)
- Redirect 302 → "Kunci API tidak dikirim ulang"; server tujuan 0 permintaan ✅.
- `HTTP_PROXY`/`http_proxy`/`ALL_PROXY` ke penangkap untuk alamat lokal → penangkap 0 permintaan ✅.
- Server 500 yang menggemakan kunci → `****4Qd8` (teks & JSON) ✅.
- `https://dolibarr.contoh-toko.id` tanpa izin → ditolak; http publik dengan izin (opsi di depan) → "wajib https"; `file://`, `user:pass@`, `0.0.0.0`, `localhost.example.com` → ditolak ✅.
- Grep 352 baris keluaran (matriks ×2 + semua skenario) untuk 4 kunci uji, potongan 8 dan 12 karakter: **0 temuan**; 0 traceback.

## D. Temuan baru / tersisa
| ID | Keparahan | Temuan & reproduksi |
|---|---|---|
| **B1** | Sedang-rendah (ada sejak v1.0.0, bukan regresi) | Penahan draf ganda membandingkan `total_ht` Dolibarr dengan DPP hitungan sendiri yang **dibulatkan ke rupiah** (`dolibarr.py` ±854: `desimal(d.get("total_ht")) == hit["dpp"]`). Bila DPP Dolibarr bersen (diskon menghasilkan ,50, atau harga produk bersen seperti BSI-10 Rp 83.333,33), keduanya tidak pernah sama → **draf kembar tetap dibuat**. Repro: draf A di atas dijalankan ulang dengan `--ya` → `(PROV21)` identik dengan `(PROV20)`, kode 0. Draf ber-DPP bulat tetap tertahan (kode 7). Dampak: dua draf (belum sah) bila agent/pengguna mengulang `--ya`; manusia masih memeriksa sebelum validasi. Saran: bandingkan dengan toleransi < Rp 1 atau dengan total baris versi Dolibarr. |
| B2 | Rendah | ENV `DOLIBARR_API_KEY` **mengalahkan** `--kunci-file` yang ditulis eksplisit, di posisi mana pun, tanpa peringatan (`piutang --kunci-file kunci-salah` tetap sukses dengan kunci ENV). `cek` menampilkan sumber kunci ("dari ENV"), perintah lain tidak. Tidak dijelaskan di SKILL.md/panduan. Saran: `--kunci-file` diutamakan, atau beri CATATAN bila keduanya ada. |
| K | Kosmetik | (1) Opsi yang sama diulang di **posisi yang sama** (`--tz WIT --tz WIB piutang`) → nilai terakhir dipakai diam-diam (perilaku argparse biasa; klaim hanya soal dua posisi). (2) Perbandingan konflik memakai teks mentah: `~/x` vs path absolut yang sama, `wit` vs `WIT` → ditolak (aman, sedikit kaku; `--tz wita` huruf kecil juga ditolak). (3) `--help` menampilkan metavar `_T0_URL`, `_T0_KUNCI_FILE`, `_T0_TZ`. (4) Kata dari masukan kunci rusak ikut disamarkan di pesan ("baris ****" bila masukan memuat kata "baru") — terlalu hati-hati, tidak bocor. (5) `cek` belum memakai deteksi modul Stok baru. (6) `simpan-kunci` tidak membaca ENV `DOLIBARR_API_KEY_FILE` (hanya `--kunci-file`/default), sedangkan perintah lain membacanya. (7) `--kunci-file ""`/`--url ""` jatuh ke default/ENV. |
| N4 | Rendah (tetap, sudah dicatat jujur) | Server > 12 jam di barat zona toko → tanggal mundur 1 hari. |

## E. Otomatis
- `python3 skills/dolibarr-usaha/tests/uji_regresi.py` → **70 tes OK** (72 d; naik dari 63).
- `python3 scripts/validate.py` (repo kerja) → **gagal 1 masalah, bukan dari skill ini**: `laporan-iklan-mingguan: ada di skills/ tapi tidak ada di catalog.csv` (folder belum di-commit milik agent lain, muncul saat uji berjalan). Pada salinan bersih `git archive HEAD`: **"59 skill valid, 59 baris katalog sesuai"**.
- `bash scripts/uji_openclaw.sh` → OpenClaw **2026.9.6 (eb377ac)**: eligible/modelVisible/commandVisible **59/60** — satu-satunya yang gagal `laporan-iklan-mingguan` (folder yang sama, belum lengkap); `dolibarr-usaha` lolos ketiganya.
- `git status` repo setelah uji: hanya berkas `examples/` ini + folder `skills/laporan-iklan-mingguan/` milik agent lain (tidak disentuh penguji).
