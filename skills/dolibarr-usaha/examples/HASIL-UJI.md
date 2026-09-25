# HASIL UJI — dolibarr-usaha v1.0.0 (uji independen)

- **Tanggal:** 2026-09-24
- **Penguji:** agent penguji independen (Claude Code, simulasi agent), bukan pembuat. `UJI-PEMBUAT.md` dan `01`–`05` berawalan nama lama (`01-draf-invoice-…` dst.) adalah catatan **pembuat**, tidak dijadikan dasar penilaian. Berkas uji independen: `00-*`, `01-uji-*` … `05-uji-*`, dan berkas ini.
- **Lingkungan:** Dolibarr **24.0.1 asli** (tag git resmi `b795838`, bersih) **dipasang ulang dari nol oleh penguji** di scratchpad: installer web step1→step5, MariaDB 10.11.14 baru (port 3317), PHP 8.4.19 `php -S` (`date.timezone=Asia/Jakarta`; juga diuji UTC, Europe/Paris, America/New_York, Asia/Makassar, Asia/Tokyo). Negara Indonesia, IDR, kamus PPN 11/12/0. Tiga kunci: admin, `api_baca` (121,262,11,31,1001), `api_tulis` (+122,12). Data fiktif "Toko Bangunan Sumber Makmur" dibuat penguji lewat API. Skill disalin ke scratchpad, `HOME` palsu.
- **Tidak diuji penguji:** Dolibarr 22.0.4 (tidak diulang), DoliWamp Windows, macOS, perilaku model asli di OpenClaw/Codex/Cursor, pengiriman Telegram.
- **Otomatis:** `tests/uji_regresi.py` 46 tes OK (tidak dijadikan dasar); `scripts/validate.py` 57 skill valid; `bash scripts/uji_openclaw.sh` → OpenClaw **2026.9.6**: `dolibarr-usaha` ada di `eligible`, `modelVisible`, `commandVisible` (57/57), tidak ada di `missingRequirements/blocked/disabled/notInjected`.
- **Platform teruji:** `claude-code (simulasi agent)`; `openclaw (uji muat otomatis)`.

## Audit keamanan
Hanya pustaka standar; tanpa `subprocess/eval`; menulis file hanya `simpan-kunci` (600/700). HTTP: GET + POST ke `thirdparties`, `invoices`, `invoices/{id}/lines` setelah `--ya` (dibuktikan log server: 0 POST dari ±25 pratinjau). Redirect ditolak (server tujuan tidak menerima kunci), proxy env diabaikan untuk alamat lokal/LAN (penangkap proxy kosong, pembanding urllib biasa tertangkap), kunci tersamar di teks/JSON/galat walau server menggemakannya, file kunci 644 ditolak, URL publik http ditolak, `sqlfilters` dibersihkan. Tidak ada prompt injection di SKILL.md/README/references. Panduan memuat peringatan DoliWamp mendengar di semua jaringan (dicocokkan: `httpd.conf.install:72 Listen`, `dolibarr.conf.install:28 Require all granted`) dan sandi DB default `changeme` (`doliwamp.iss:237`). **Lulus dengan catatan S2, S3.**

## Skenario
| No | Berkas | Isi | Hasil |
|---|---|---|---|
| 00 | `00-pembanding-tanpa-skill.md` | A/B skenario 01 | Skill **jelas lebih baik** (tanpa skill: PPN 12% penuh → lebih pungut Rp 17.238, tempo hilang, kunci di chat) |
| 00 | `00-banding-pesaing.md` | latinogino/dolibarr-mcp (18★), digitalfactorysn/mcp-dolibarr, skills.sh | Pesaing terbaik 14/40 vs **34/40** (payload pesaing → PPN 0, tempo hilang) |
| 01 | `01-uji-toko-bangunan-pelanggan-dan-invoice.md` | cek → cari/tambah → draf 3 baris + diskon + PPN; mewah; jasa; draf ganda | **Lulus**; angka 0 beda; S4, R4 |
| 02 | `02-uji-piutang-lewat-jatuh-tempo.md` | 8 piutang, bayar sebagian, batas 30/90 hari, `--samarkan`, 5 zona PHP | **Lulus**; angka 0 beda; R3 |
| 03 | `03-uji-stok-menipis-dan-laporan-harian.md` | stok minus/habis/menipis/saran beli, laporan hari ini & kemarin, modul mati | **Lulus pada konfigurasi normal**; S1, R5 |
| 04 | `04-uji-input-buruk-dan-keamanan.md` | 401, mati, 404, API mati, 403, URL publik/LAN, 20+ item aneh, ganda, kebocoran kunci, hak API | **Lulus sebagian**; S2, S3, S4, R1, R2 |
| 05 | `05-uji-di-luar-cakupan.md` | validasi/kirim/hapus/bayar/Coretax/broadcast/injeksi | **Lulus** (script tidak punya aksinya) |

## Verifikasi angka independen (Decimal & SQL sendiri, bukan kode skill)
| Diuji | Hasil |
|---|---|
| Total baris (diskon, harga bersen), DPP, DPP 11/12, PPN tepat, PPN ke bawah sekali, total — 3 invoice (umum, mewah, jasa) | **0 beda** vs script |
| Angka Dolibarr per baris (2 desimal) vs rumus penguji | **0 beda**; selisih Komunitech–Dolibarr Rp 0,01–0,56 **dilaporkan** "BEDA" |
| Sisa piutang (total − pembayaran), umur `DATEDIFF`, 5 kelompok, total | **0 beda** (zona PHP UTC/WIB/barat) |
| Penjualan harian (statut 1+2, draf/batal dikecualikan), DPP/PPN, belum dibayar, % vs kemarin (666,012 → 666,0) | **0 beda** |
| Status stok & saran beli 7 produk | **0 beda** |
| Standar pembulatan library & kalimat "belum dicocokkan dengan Coretax" | dipatuhi; ada di SKILL.md:114 + pesan BEDA |

## Temuan cacat
| ID | Keparahan | Lokasi | Temuan & reproduksi |
|---|---|---|---|
| **T1** | **Tinggi** | `scripts/build.py:119-133`; rujukan di `SKILL.md:22,29`, `README.md` (Instalasi 1), pesan `Saran` di `dolibarr.py:343,357` | **`docs/panduan-dolibarr.md` tidak ikut paket pembeli.** Repro: salin repo mini ke scratchpad → `python3 scripts/build.py --pembeli "Pembeli Fiktif" --skill dolibarr-usaha --izinkan-draft` → isi ZIP 14 berkas, tanpa panduan. Pembeli awam tidak mendapat langkah pasang DoliWamp, aktifkan modul, user API, dan kunci — padahal semua pesan galat merujuk ke sana. Saran: pindahkan/salin ke `skills/dolibarr-usaha/references/panduan-dolibarr.md` (atau build menyertakan `docs/panduan-*.md` yang dirujuk). |
| **S1** | Sedang | `dolibarr.py:927-937` (`ambil_produk`), `:1067-1084` | Modul **Stok** mati → API produk tetap jawab, stok kosong dianggap 0 → `stok` dan laporan harian: "habis 7 dari 7", "SMN-40 stok 0 HABIS -> beli 120". Alarm palsu tiap malam + saran beli salah. Repro: `unActivateModule('modStock')` → `laporan-harian`. Saran: cek modul/`stock_reel` null → "Stok tidak dicatat di Dolibarr (modul Stok mati)". |
| **S2** | Sedang | `docs/panduan-dolibarr.md` §6 langkah 3-4; `dolibarr.py:408-418` (HAK_BERISIKO) | Hak **12 "Buat/ubah invoice"** sudah cukup untuk `POST invoices/{id}/validate` dan `settopaid` via API (Dolibarr 24.0.1 `api_invoices.class.php:1208,1264`); hak 14 "Validasi" disembunyikan bila izin lanjutan mati. Repro: kunci `api_tulis` → `POST invoices/8/validate` → PROV8 jadi IN2609-0010; `settopaid` → paye=1. Klaim "jangan berikan Validasi faktur" memberi rasa aman palsu; `cek` tidak memperingatkan. Saran: tulis jujur di panduan & README (hak menulis = bisa validasi/tutup lewat API; perlindungan utama = script tanpa perintah itu + aturan agent), `cek` beri catatan saat `facture creer` aktif. |
| **S3** | Sedang | `dolibarr.py:218-230` (`baca_kunci`), `:316-318` (`minta`) | Kunci berisi baris baru (file kunci 2 baris lewat `--kunci-file`/`DOLIBARR_API_KEY_FILE`, atau ENV berisi `\n`) → `ValueError: Invalid header value b'kunciDuaBaris-AAAABBBB\nbaris2'` → **kunci tercetak utuh** di traceback, melanggar klaim "tidak pernah dicetak". Repro: `DOLIBARR_API_KEY=$'kunciDuaBaris-AAAABBBB\nbaris2' dolibarr.py cek`. Saran: validasi kunci (satu baris, karakter aman) saat dibaca; tangkap semua pengecualian di `main` dan cetak lewat `samarkan`. |
| **S4** | Sedang | `dolibarr.py:534-541` (`cari_pelanggan`), `:581-588` | Cek ganda hanya berdasar nama: "Ibu Rina Wati" dengan nomor **sama** dengan "Bu Rina Wati" lolos tanpa peringatan; `pelanggan cari "0812-3456-0002"` tidak menemukan pelanggan bernomor `081234560002`. Saran: normalisasi nomor (hapus spasi/strip, 62→0) saat cari & cek ganda juga per telepon/email. |
| R1 | Rendah | `dolibarr.py:631-643`, `:109`, `:718` | `NaN`, `Infinity`, `1e30` → traceback `InvalidOperation`; `--jatuh-tempo 99999999` → `OverflowError`; `1e3` diterima sebagai 1.000. |
| R2 | Rendah | `dolibarr.py:633-636` | `62,500` (gaya Inggris) dibaca Rp 62,50 (total Rp 138). Terlihat di pratinjau, tapi sebaiknya ditolak/ditanyakan bila tepat 3 digit setelah koma. |
| R3 | Rendah | `dolibarr.py:168-176`; `SKILL.md` (tidak menyebut `--tz`) | Bila zona PHP server lebih timur dari `--tz` (mis. Dolibarr Linux di Bali dengan zona sistem Asia/Makassar, tanpa `--tz WITA`), semua tanggal mundur 1 hari: "jatuh tempo hari ini" → "lewat 1 hari", 30 → 31 hari. DoliWamp default UTC aman. Saran: pakai `timestamp_php_tz` dari `/status` atau bulatkan ke tanggal terdekat (+12 jam); sebut `--tz` di SKILL.md. |
| R4 | Rendah | `dolibarr.py:800-803` | Pesan BEDA hanya menjelaskan pembulatan PPN; selisih **DPP** (total baris rupiah vs 2 desimal, mis. 237.500 vs 237.499,99) tidak dijelaskan. |
| R5 | Rendah | `dolibarr.py:1012-1019` | Semua bagian laporan gagal (modul API mati) → kode keluar 0; jadwal OpenClaw tampil `status: ok`. |
| R6 | Rendah | `SKILL.md:142` | Merujuk `tests/uji_regresi.py`, padahal `build.py` membuang `tests/` dari paket. |
| K1 | Kosmetik | `dolibarr.py:936-937`, `:1047`, `:749` | "stok 6 (min 6) aman -> beli 4"; laporan tanggal lampau memakai piutang kondisi sekarang tanpa label; draf ganda DIBATALKAN berjudul "DRAF INVOICE" dengan kode 0; produk tidak dijual ikut dinilai stok; pesan argparse campur Inggris; berkas contoh pembuat & penguji sama-sama bernomor 01–05. |

## Panduan `docs/panduan-dolibarr.md` (untuk awam)
- (+) Tiap langkah punya ✅ cek berhasil / ❌ kalau gagal, istilah dijelaskan, jujur soal yang belum dicoba (installer DoliWamp Windows, klik layar Backup, nyala otomatis).
- (+) Diverifikasi penguji: DoliWamp terbaru 22.0.4 (SourceForge, 9 Jan 2026), port 80/3306, sandi `changeme`, Apache `Listen` semua antarmuka, menu Start "Tools > Start DoliWamp server", PHP DoliWamp `date.timezone = UTC`, hak id 11/12/14/16/19/121/122/262/31/1001/342, kamus PPN tanpa tarif Indonesia, 405 saat set `api_key` via API.
- (−) S2 (klaim hak validasi), T1 (tidak ikut paket).
- Tidak bisa diverifikasi penguji: tampilan installer DoliWamp & SmartScreen, ikon "putar/refresh" Token for API, halaman Backup/Restore di layar, perilaku layanan Windows setelah restart, `setx`.

## Skor kualitas: **6 / 10**
Alasan:
- (+) Diuji penguji terhadap **Dolibarr 24.0.1 asli yang dipasang sendiri**: semua angka (PPN 11/12, diskon, bersen, piutang, laporan, stok) **0 beda** dengan hitung ulang independen; selisih dengan Dolibarr dilaporkan jujur.
- (+) Keamanan inti terbukti: tidak menulis tanpa `--ya`, tanpa validasi/bayar/hapus, redirect & proxy aman, kunci tersamar, URL publik ditolak.
- (+) A/B jelas lebih baik; unggul telak atas pesaing publik terbaik (34 vs 14/40); lolos uji muat OpenClaw 2026.9.6.
- (−) **T1**: panduan pemasangan yang dirujuk semua pesan galat tidak sampai ke pembeli awam.
- (−) **S1**: laporan harian bisa berisi data stok palsu (semua HABIS) — bertentangan dengan prinsip "reliable".
- (−) **S3**: jalur kebocoran kunci melanggar klaim keamanan; **S2**: klaim perlindungan hak user tidak akurat; **S4**: pelanggan ganda per nomor HP lolos.

**Keputusan: TIDAK LULUS (< 7) — revisi.** Perbaikan kecil dan terarah: T1, S1, S3 wajib; S2 (teks panduan/README + catatan `cek`), S4, R1 disarankan. Setelah itu uji ulang oleh penguji independen (04-D kunci multi-baris, 03 modul Stok mati, 01 cek ganda telepon, isi ZIP build). Perkiraan setelah revisi: 8/10.

---

## Uji ulang v1.0.1 (2026-09-24)
- **Penguji:** agent penguji independen baru (Claude Code, simulasi agent), bukan pembuat skill/revisi. Rincian lengkap: `06-uji-ulang-v1.0.1.md`.
- **Lingkungan:** **Dolibarr 24.0.1 asli** (instalasi penguji v1.0.0 dihidupkan ulang: MariaDB 10.11.14, PHP 8.4.19) + 6 server PHP zona lain ke database yang sama; build diuji di **salinan repo** di scratchpad.
- **Otomatis:** `uji_regresi.py` 63 tes OK; `uji_openclaw.sh` OpenClaw 2026.9.6 57/57 eligible/modelVisible/commandVisible; `validate.py` gagal 1 masalah milik **pdf-lokal** (pola curl-pipe-sh di HASIL-UJI-nya, commit ff044ad), bukan dolibarr-usaha.
- **Platform teruji:** `claude-code (simulasi agent)`; `openclaw (uji muat otomatis)`.

### Status klaim
| Klaim | Status |
|---|---|
| T1 panduan ikut ZIP | ✅ dolibarr-usaha +`docs/panduan-dolibarr.md`, pdf-lokal +`docs/panduan-stirling-pdf.md`; bundle/VIP lain tidak berubah (isi identik selain watermark & LISENSI); watermark & `LISENSI.txt` tetap |
| S1 Stok mati tanpa HABIS palsu | ✅ alarm/saran beli palsu hilang (v1.0.0 masih "habis 7"). ⚠️ Admin/user ber-342 mendapat diagnosis **salah** "hak kurang" (N1); "Modul Stok belum aktif" tidak pernah muncul di 24.0.1 asli |
| S2 dua user + risiko hak 12 | ✅ panduan/README/SKILL.md akurat (dicocokkan ke kode Dolibarr); peringatan `cek` hanya muncul bila hak 342 diberikan (N3) |
| S3 kunci rusak | ✅ 16 variasi: ujung dibersihkan, tengah ditolak, 0 traceback, 0 kunci tercetak |
| S4 ganda HP/email, cari ternormalisasi | ✅ |
| R1 / R2 / R4 / R5 | ✅ |
| R3 zona PHP ≠ `--tz` | ✅ dalam batas ≤ 12 jam barat / ≤ 11 jam timur (Makassar/Tokyo/Auckland kini benar); di luar batas (server AS) masih mundur 1 hari (N4) |

### Regresi
Tidak ada. Skenario 01–03 diulang: 4 draf baru (umum, mewah bersen, jasa tanpa PPN, umum desimal) + pratinjau 2,5 × 62.500,50 — DPP, DPP 11/12, PPN ke bawah sekali, diskon, total **0 beda** dengan kalkulator `Decimal` penguji; angka Dolibarr dilaporkan BEDA apa adanya dan cocok dengan DB. Piutang (8 → 10 invoice, 5 kelompok umur), laporan 24 & 25 Sep (termasuk % vs kemarin), stok 7 produk: **0 beda** dengan SQL. 0 POST tanpa `--ya`; redirect, proxy, URL publik, server rusak: aman.

### Cacat tersisa
- **N2 (sedang, sejak v1.0.0):** opsi umum yang ditulis **sebelum** subperintah (`--kunci-file`, `--tz`, `--json`, `--url`) diabaikan diam-diam. `dolibarr.py --kunci-file …-draf.txt simpan-kunci` menimpa **kunci baca default** dengan kunci draf, sehingga jadwal bisa berjalan dengan kunci yang mampu memvalidasi. Contoh resmi di panduan memakai posisi yang benar.
- **N1 (sedang-rendah):** diagnosis modul Stok mati vs hak kurang salah untuk admin/342 (tanpa data palsu).
- N3, N4, kosmetik (draf ganda kode 0, "bertanggal hari ini" di laporan lampau, panduan di luar folder skill setelah dipasang, invoice ditandai lunas tanpa pembayaran dihitung belum dibayar).

### Skor kualitas: **8 / 10** — **LULUS** (≥ 7)
Alasan:
- (+) Semua cacat wajib v1.0.0 (T1, S1, S3) terbukti beres pada Dolibarr asli; S2 dan S4 serta R1–R5 juga beres. Repro asli v1.0.0 (kunci dua baris, "Ibu Rina Wati", `0812-3456-0002`, `62,500`, NaN/1e30, modul Stok mati, zona Makassar) kini benar.
- (+) Angka tetap 0 beda di semua hitung ulang independen; keamanan inti tetap utuh; lolos uji muat OpenClaw.
- (−) N2 dapat merusak pemisahan kunci baca/draf yang justru disarankan revisi S2 bila opsi diletakkan di depan; N1 memberi saran perbaikan yang keliru untuk admin/342.
- Rekomendasi v1.0.2 (perbaikan kecil, tidak menghalangi status `lulus`): perbaiki N2 (`default=argparse.SUPPRESS` di subparser) dan N1 (cek `setup/modules`/tidak adanya `rights.stock` lebih dulu), sesuaikan kalimat panduan §6 soal 342, lalu uji platform asli oleh pemilik (DoliWamp Windows).

---

## Uji ulang v1.0.2 (2026-09-25)
- **Penguji:** agent penguji independen baru (Claude Code, simulasi agent), bukan pembuat skill/revisi. Rincian lengkap: `07-uji-ulang-v1.0.2.md`.
- **Lingkungan:** **Dolibarr 24.0.1 asli** (instalasi penguji v1.0.0 dihidupkan ulang dengan salinan database: MariaDB 10.11.14, PHP 8.4.19) + server kedua di alamat LAN kontainer untuk `--izinkan-url-luar`; Python 3.11.15.
- **Otomatis:** `uji_regresi.py` **70 tes OK**; `validate.py` di salinan bersih HEAD "59 skill valid" (di repo kerja gagal 1 masalah milik folder `laporan-iklan-mingguan` yang belum di-commit agent lain); `uji_openclaw.sh` OpenClaw 2026.9.6: dolibarr-usaha eligible/modelVisible/commandVisible (59/60, satu-satunya gagal folder yang sama).
- **Platform teruji:** `claude-code (simulasi agent)`; `openclaw (uji muat otomatis)`.

### Status klaim
| Klaim | Status |
|---|---|
| N2 opsi umum depan/tengah/belakang | ✅ Repro asli (`--kunci-file …-draf.txt simpan-kunci`) kini menulis ke file draf, file default utuh. Matriks 7 subperintah × 5 opsi × semua posisi: **84/84 dihormati**; `--tz` terbukti mengubah tanggal di semua posisi; nilai beda di dua posisi → kode 2 |
| N2 `simpan-kunci` path lengkap & tak menimpa tanpa `--ya` | ✅ termasuk `--ya` + kunci rusak/kosong → file lama tetap utuh |
| N1 "Modul Stok belum aktif" | ✅ admin, user tanpa/dengan 342 → diagnosis benar (kode 4); modul aktif + hak kurang → "belum punya hak" (kode 5); Explorer dimatikan → admin tetap benar, non-admin pesan gabungan jujur; 0 HABIS palsu di 7 keadaan |
| Kosmetik kode 7 / tanggal draf / lunas tanpa bayar | ✅ ketiganya (dengan catatan B1 di bawah) |
| Panduan §6/§7, batas zona di SKILL.md | ✅ akurat terhadap perilaku yang diamati |

### Regresi
Tidak ada. Pelanggan baru → draf 3 baris (diskon 4% & 7,5%, ongkir bersen, PPN 12% × DPP 11/12) + draf 2 baris: DPP, DPP 11/12, PPN ke bawah sekali, total **0 beda** dengan kalkulator `Decimal` penguji; angka Dolibarr (per baris, 2 desimal) dilaporkan BEDA apa adanya dan cocok DB. Piutang (10 invoice, kelompok umur, terlambat), stok (4 perlu perhatian + saran beli), laporan 24 & 25 Sep (termasuk % vs kemarin): **0 beda** dengan SQL. 0 POST tanpa `--ya` (12 POST total, semuanya dari `--ya`); redirect, proxy, URL publik, server menggemakan kunci: aman; 0 kunci/potongan kunci di 352 baris keluaran; 0 traceback.

### Cacat tersisa
- **B1 (sedang-rendah, ada sejak v1.0.0):** penahan draf ganda gagal bila DPP Dolibarr bersen (mis. diskon menghasilkan ,50 atau harga produk Rp 83.333,33) karena membandingkan `total_ht` Dolibarr dengan DPP yang sudah dibulatkan (`dolibarr.py` baris 854). Repro: draf 3 baris di atas diulang `--ya` → draf kembar `(PROV21)` dibuat, kode 0. DPP bulat tetap tertahan (kode 7).
- **B2 (rendah):** ENV `DOLIBARR_API_KEY` mengalahkan `--kunci-file` eksplisit tanpa peringatan (hanya `cek` menampilkan sumber kunci).
- Kosmetik: opsi diulang di posisi yang sama → nilai terakhir; konflik membandingkan teks mentah (`~/x` vs path absolut, `wit` vs `WIT` ditolak); metavar `_T0_…` di `--help`; `cek` belum memakai deteksi modul Stok baru; `simpan-kunci` tidak membaca `DOLIBARR_API_KEY_FILE`; penyamaran berlebih kata dari masukan kunci rusak. N4 (server AS) tetap, sudah dicatat jujur.

### Skor kualitas: **8 / 10** — **LULUS** (≥ 7)
Alasan:
- (+) Kedua cacat v1.0.1 (N2 sedang, N1 sedang-rendah) dan tiga kosmetik terbukti beres di Dolibarr asli, termasuk repro asli N2; tidak ada opsi umum yang diabaikan di posisi berbeda, kunci tidak pernah tertimpa/bocor.
- (+) Angka tetap 0 beda di semua hitung ulang independen; keamanan inti utuh; 70 tes regresi; lolos uji muat OpenClaw.
- (−) B1 membuat jaring pengaman "draf dobel" tidak bekerja pada kasus umum (diskon/harga bersen) — bertentangan dengan tabel galat SKILL.md; B2 bisa diam-diam memakai kunci lain dari yang diminta.
- **Kesimpulan:** **siap uji platform asli** (pemilik/tim, DoliWamp Windows sesuai `docs/uji-platform.md`) lalu beta. Disarankan memperbaiki B1 (toleransi < Rp 1 atau bandingkan dengan total versi Dolibarr) dan B2 (utamakan `--kunci-file` atau beri CATATAN) di v1.0.3 sebelum/selama beta; keduanya tidak menghalangi status `lulus`.
