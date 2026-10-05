# 06 — Uji ulang independen v1.0.1 (setelah revisi)

- **Tanggal:** 2026-09-24 (jam server WIB sudah 25 Sep dini hari; laporan "hari ini" = 25 Sep)
- **Penguji:** agent penguji independen (Claude Code, simulasi agent). Bukan pembuat skill dan bukan pembuat revisi. Tidak mengubah kode.
- **Lingkungan:** **Dolibarr 24.0.1 asli** — instalasi penguji v1.0.0 (tag resmi, MariaDB 10.11.14 port 3317, PHP 8.4.19 `php -S`) dihidupkan ulang dari scratchpad. Data fiktif "Toko Bangunan Sumber Makmur" + data baru penguji ("Toko Baru Tiga", 4 draf). Server PHP tambahan dengan zona Asia/Makassar, Asia/Tokyo, UTC, America/New_York, Pacific/Auckland, America/Los_Angeles (mengarah ke database yang sama). Skill disalin ke scratchpad, `HOME` palsu. Kunci: `api_baca` (121,262,11,31,1001), `api_tulis` (+122,12), admin — ditampilkan tersamar (`****Ls4K`, `****5Wf1`, `****8Rt6`).
- **Tidak diuji:** Dolibarr 22.0.4, DoliWamp Windows, macOS, model asli di OpenClaw/Codex/Cursor, Telegram.

## A. Klaim revisi — status

| Klaim | Reproduksi penguji | Hasil |
|---|---|---|
| **T1** panduan ikut ZIP | Salinan repo di scratchpad; `build.py` lama (f7b3f1c) vs baru, 7 paket (`--skill dolibarr-usaha`, `--skill pdf-lokal`, keduanya, `--vip`, 3 bundle), semua `--izinkan-draft` | ✅ ZIP dolibarr-usaha: 22 → 23 berkas (+`docs/panduan-dolibarr.md`, isi identik dengan repo). ZIP pdf-lokal: +`docs/panduan-stirling-pdf.md`. VIP: 927 → 929 (hanya 2 panduan itu). 3 bundle: daftar berkas **identik**. Isi semua berkas sama kecuali `LISENSI.txt` dan baris watermark `SKILL.md` (dibuktikan dengan membuang baris watermark → 0 beda di 57 SKILL.md). Watermark ada di semua SKILL.md; `LISENSI.txt` berisi kode, pemegang, jenis, versi 1.0.1; `tests/` tidak ikut; `instalasi/program-beta/uji-platform` tidak ikut ke `docs/`. |
| **S1** Stok mati → tanpa HABIS palsu | `unActivateModule('modStock')` (sama seperti tombol di layar Modul) → `stok`, `stok --menipis`, `stok semen`, `laporan-harian`, `--json` | ✅ **Tidak ada lagi "habis 7 dari 7"/saran beli palsu** (v1.0.0 di keadaan sama masih "habis 7 … BSI-10 HABIS -> beli 20" — repro asli terkonfirmasi). Bagian STOK laporan: "Tidak bisa dibaca …", bagian lain tetap terkirim. ⚠️ **Pesan "Modul Stok belum aktif" tidak pernah muncul di Dolibarr asli:** kunci `api_baca` (tanpa 342) → pesan ambigu "modul belum aktif, atau … hak" (sesuai pengakuan "Belum"); tetapi kunci **admin** atau user **dengan hak 342** → **"User API belum punya hak 'Baca gudang dan stok'"** + saran buka Izin user — **diagnosis salah** (lihat N1). |
| **S2** panduan dua user + risiko hak 12, `cek` memberi peringatan | Baca panduan §6/§11, README FAQ, SKILL.md Keamanan; cocokkan `api_invoices.class.php` 24.0.1; `cek` dengan `api_tulis` dengan & tanpa hak 342 | ✅ Teks jujur dan akurat: `validate`/`settodraft`/`settopaid`/`settounpaid`/`putLine`/`deleteLine` memeriksa `facture creer` (baris 1158/1208/1264/1316/569/855), pembayaran `paiement` (1752), hapus `supprimer` (960). `cek` `api_tulis`+342 → CATATAN "Hak 'Buat/ubah invoice' … juga mengizinkan MEMVALIDASI dan MENANDAI LUNAS". ⚠️ `api_tulis` **tanpa** 342 (342 opsional di panduan) → **tidak ada peringatan** (daftar hak tak terbaca). Panduan §6 "✅ Untuk `api_draf` muncul catatan" hanya benar bila 342 diberikan. |
| **S3** kunci dibersihkan/ditolak, tanpa traceback | 16 variasi: ENV `\n` di ujung, spasi+`\r\n`, baris baru di tengah (repro v1.0.0 `kunciDuaBaris-…\nbaris2`), spasi/tab di tengah, non-ASCII, < 8 karakter, file 2 baris (repro v1.0.0 via `--kunci-file` & `DOLIBARR_API_KEY_FILE`), file BOM+CRLF (Notepad), file UTF-16, `simpan-kunci` stdin, 401 dengan spasi di ujung | ✅ Ujung dibersihkan (cek/piutang/stok jalan), tengah ditolak kode 5 dengan saran salin ulang, BOM+CRLF diterima, UTF-16 → "tidak bisa dibaca (UnicodeDecodeError)". **0 traceback; 0 kunci/potongan kunci utuh** di semua keluaran (grep). Server yang menggemakan kunci di galat 500 → `****5Wf1` (teks & JSON). |
| **S4** ganda per HP & email; `cari` normalisasi | Repro v1.0.0 "Ibu Rina Wati" 081234560004; `+62 812-3456-0002`, `6281234560003`, `812 3456 0005`; email beda huruf/spasi; HP tersimpan `+62 813-2222-1111`, `(0271) 123456` + `phone_mobile` `0896 7777 8888`; `cari "0812-3456-0002"`, `"+62 812 3456 0004"`, `"(0812) 3456.0001"`, potongan | ✅ Semua ganda tertangkap dengan alasan ("nomor HP sama", "email sama", gabungan), tidak dibuat tanpa `--tetap-buat`; HP beda → pratinjau biasa; `cari` menemukan semua format. 0 POST dari pratinjau. (Kosmetik: baris ganda menampilkan `phone`, bukan `phone_mobile` yang cocok.) |
| **R1** NaN/Infinity/1e30/tempo raksasa | 23 variasi item + `--jatuh-tempo` 99999999/3651/-1/3650/0 | ✅ Semua ditolak jelas kode 2 (NaN, Infinity, -Infinity, 1e30, 1e3, 0x10, 62_500, > 1.000.000 unit, > Rp 100 M, negatif, diskon > 100/negatif/NaN, jumlah 0); tempo di luar 0–3650 ditolak; 0 traceback. (Angka lebar-penuh `１` diterima = 1, tidak berbahaya.) |
| **R2** `62,500` ambigu | `62,500`, `1,250,000` | ✅ ditolak "ambigu … Tulis 62500 atau 62.500". `62.500`, `2,5|62.500,50`, `Rp. 62.500` tetap benar. |
| **R3** tanggal benar walau zona PHP ≠ `--tz` | `piutang` + `laporan-harian --tanggal 2026-09-24` pada 7 server × `--tz` WIB/WITA/WIT, dibandingkan dengan server WIB | ✅ Makassar, Tokyo, Auckland (timur), UTC, New York → **identik** untuk WIB/WITA (v1.0.0: Makassar/Tokyo/Auckland **beda**). Di luar batas yang ditulis di kode (≤ 12 jam barat): Los Angeles vs WIB (14 jam) dan New York/LA vs WIT → mundur 1 hari. Wajar untuk Dolibarr lokal; dicatat. |
| **R4** pesan selisih DPP | Draf mewah & umum dengan harga bersen | ✅ "Selisih DPP: Dolibarr menyimpan total baris dengan sen…" muncul hanya bila DPP beda. |
| **R5** semua bagian gagal → kode ≠ 0 | Cabut hak 11+1001; modul API mati; server JSON rusak/HTML | ✅ kode 5 / 4 / 6 dengan "Laporan tidak bisa dibuat: semua bagian gagal dibaca". Satu bagian gagal → kode 0, bagian lain tetap. |

## B. Regresi (skenario 01–03 diulang, hitung ulang independen)
Kalkulator penguji `Decimal` terpisah (tidak memakai kode skill) + SQL langsung ke `llx_facture`/`llx_facturedet`/`llx_product`.

| Kasus | Script | Penguji | Dolibarr (DB) |
|---|---|---|---|
| A umum: `@SMN-40|20`, Cat 4×87.500 disk 7,5%, ongkir 150.000 | DPP 1.723.750; 11/12 1.580.104,17; PPN 189.612 (dari 189.612,50 ke bawah); total 1.913.362 | sama | 1.723.750 / 189.612,50 → "BEDA PPN +0,50" ✅ |
| B mewah: `@BSI-10|7` (83.333,33), keramik 3×68.000 disk 12,5%, lem 2,5×12.345,67 | 583.333 + 178.500 + 30.864 = 792.697; PPN 95.123 (95.123,64); total 887.820 | sama | 792.697,49 / 95.123,70 → BEDA DPP +0,49 (dijelaskan) ✅; catatan tarif produk 11% vs 12% ✅ |
| C jasa tanpa PPN 12×45.000 disk 2,5%, tempo 0 | 526.500; PPN 0; COCOK | sama | `product_type=1`, tva 0 ✅ |
| D umum desimal | 250.000 + 10.000 + 8.382 = 268.382; PPN 29.522 (29.522,02) | sama | 268.382,24 / 29.522,04 ✅ |
| E pratinjau 2,5 × 62.500,50 | 156.251; PPN 17.187 (17.187,61) | sama | – |
| Draf ganda (A diulang `--ya`) | "DRAF INVOICE TIDAK DIBUAT (kemungkinan dobel)" | – | tidak ada invoice baru ✅ |
| Piutang per 25 Sep (8 invoice) | Rp 18.968.192,16; 1.855.892,25 / 4.802.970 / 7.261.975 / 5.047.354,91 | `DATEDIFF` SQL: sama | ✅ 0 beda |
| Laporan 24 Sep | 1.775.417,25; DPP 1.599.475; PPN 175.942,25; 3 invoice; naik 670,8% | sama | ✅ |
| Laporan 25 Sep setelah 2 draf divalidasi manusia (admin) | 2.439.862,50; DPP 2.250.250; PPN 189.612,50; naik 37,4%; piutang 10 inv Rp 21.408.054,66; terlambat 6 | sama | ✅ |
| Stok 7 produk | KRM-40 MINUS beli 12, PKU-7 HABIS beli 30, CAT-5 beli 9, SMN-40 beli 95; PSR-1 6/min 6 aman **tanpa** saran beli (K1 v1.0.0 beres) | sama | ✅ |

Tanpa `--ya`: 0 POST (log server PHP). Seluruh sesi: tepat 15 POST = 1 pelanggan + 4 invoice + 10 baris, semuanya dari perintah `--ya`. Tidak ada PUT/DELETE.

## C. Keamanan (diulang)
Redirect 302 → "Kunci API tidak dikirim ulang", server tujuan menerima 0 permintaan ✅. `HTTP_PROXY/ALL_PROXY` untuk alamat lokal diabaikan (penangkap proxy 0 permintaan) ✅. URL publik http/https tanpa izin, 192.168.x tanpa izin, `0.0.0.0`, `localhost.example.com`, `user@host`, `file://` → ditolak; http publik dengan izin → "wajib https" ✅. Server JSON rusak / HTML / struktur aneh → pesan GAGAL kode 6, tanpa traceback ✅. Perintah validasi/bayar/hapus tidak ada ✅. Pola penyamaran: 0 kunci utuh di semua keluaran.

## D. Temuan baru / tersisa
| ID | Keparahan | Temuan & reproduksi |
|---|---|---|
| **N1** | Sedang-rendah | `pastikan_stok_aktif` (dolibarr.py ±1007-1043) mengandalkan "hak stok tetap tercantum di /users/info saat modul mati". Di Dolibarr 24.0.1 asli **tidak**: `unActivateModule` menghapus `llx_rights_def` stok, jadi `users/info` tidak memuat `stock` sama sekali → admin/user ber-342 mendapat **"User API belum punya hak 'Baca gudang dan stok'"** dan diarahkan ke layar Izin (yang tidak menampilkan hak stok karena modul mati). `setup/modules` (yang memang menunjukkan `stock` hilang untuk admin) hanya dicoba bila `users/info` 403. Panduan §6.1 langkah 3 ("342 … membedakan modul Stok mati dari hak stok kurang") tidak terbukti. Tidak ada data palsu; hanya diagnosis salah. Saran: cek `setup/modules` lebih dulu bila bisa, dan bila `stock` tidak ada di `rights` sama sekali anggap modul mati. |
| **N2** | Sedang | Opsi umum **sebelum** subperintah diabaikan diam-diam (argparse `parents=[umum]` di parser utama **dan** subparser; default subparser menimpa). Ada sejak v1.0.0. Dampak: `dolibarr.py --kunci-file ~/…-draf.txt simpan-kunci` menyimpan kunci **draf ke file default** (menimpa kunci baca yang dipakai jadwal) — bertentangan dengan saran S2 (terbukti: file default berubah ke `****5Wf1`); `--tz WITA laporan-harian` tetap WIB; `--json cek` keluar teks; `--kunci-file X invoice buat --ya` memakai kunci default. `--help` justru menampilkan opsi ini di posisi depan. Panduan & SKILL.md memberi contoh posisi yang benar (setelah subperintah), jadi jalur resmi aman. Saran: `default=argparse.SUPPRESS` di subparser atau hapus `parents` dari parser utama. |
| N3 | Rendah | `cek` tanpa hak 342 tidak memberi peringatan hak 12 (lihat S2) — wajar secara teknis, tetapi panduan perlu menyebut "hanya bila hak 342 diberikan". |
| N4 | Rendah | Zona PHP server > 12 jam di barat zona toko (mis. hosting AS) → tanggal mundur 1 hari. Di luar pemakaian lokal; sebut di SKILL.md bagian `--tz`. |
| K | Kosmetik | Draf ganda "TIDAK DIBUAT" keluar kode 0; laporan tanggal lampau menulis "draf invoice bertanggal **hari ini**"; `docs/panduan-dolibarr.md` di ZIP ada di luar folder skill (setelah dipasang, agent tidak bisa membukanya — cukup untuk pembeli manusia); invoice yang ditandai lunas tanpa pembayaran (`paye=1`, `IN2609-0010`) masih dihitung "belum dibayar dari penjualan ini" Rp 11.100 di laporan 24 Sep. |

## E. Otomatis
- `python3 skills/dolibarr-usaha/tests/uji_regresi.py` → **63 tes OK** (27,9 d).
- `python3 scripts/validate.py` → **gagal 1 masalah, bukan dari skill ini**: `pdf-lokal: examples/HASIL-UJI.md berisi pola curl-pipe-sh` (commit ff044ad agent lain, masuk saat uji ini berjalan). Di salinan repo dengan baris itu dinetralkan: "57 skill valid". `dolibarr-usaha` sendiri valid.
- `bash scripts/uji_openclaw.sh` → OpenClaw **2026.9.6**: eligible 57/57, modelVisible 57/57, commandVisible 57/57.
- `git status` repo setelah uji: bersih selain berkas `examples/` ini (tidak ada `dist/`).
