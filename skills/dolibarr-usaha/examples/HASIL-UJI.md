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

---

## Uji ulang v1.0.3 (Akun B)
- **Tanggal:** 2026-09-25
- **Penguji:** agent penguji independen lintas akun (Akun B, Claude Code, simulasi agent), bukan pembuat skill/perbaikan. Rincian: `08-uji-ulang-v1.0.3.md`.
- **Lingkungan:** salinan skill di scratchpad; **server Dolibarr tiruan** (turunan `tests/uji_regresi.py`, respons dari rekaman 24.0.1) + mode putus/timeout buatan penguji. **Tidak** diuji di Dolibarr asli pada versi ini. Python 3.11.15.
- **Otomatis:** `uji_regresi.py` **77 tes OK** (1 dilewati, khusus repo); `validate.py --skill dolibarr-usaha` ✅ valid; `uji_openclaw.sh` tidak dijalankan di sini (oleh penguji pimpinan).
- **Platform teruji:** `claude-code (simulasi agent)`.

### Status klaim
| Klaim | Status |
|---|---|
| B1 draf ganda saat DPP bersen | ✅ 6 pola (repro asli v1.0.2 diskon 4%/7,5% + ongkir, repro pembuat, harga 83.333,33 PPN mewah, 10 × 100,50, jasa tanpa PPN, qty desimal + diskon 33,33%): perintah identik diulang 3× → kode 7, **0 POST tambahan**; urutan item dibalik juga tertahan; jumlah beda ≥ ± Rp 1,5 tetap dibuat; invoice tervalidasi tidak menghalangi |
| Angka (DPP, DPP 11/12, PPN floor sekali, total) | ✅ **0 beda** dengan kalkulator `Fraction`/`Decimal` penguji di 6 skenario; DPP cara Dolibarr = angka Dolibarr asli 1.280.157,50 (skenario A) |
| B1 idempoten saat timeout/putus | ⚠️ baru diuji: timeout baca ulang akhir aman (kode 7); putus/timeout **setelah** draf dibuat atau saat menambah baris → draf kosong/sebagian tertinggal dan pengulangan membuat draf kedua (**C1**) |
| B2 `--kunci-file` vs ENV | ✅ `--kunci-file` menang di depan/belakang, PERINGATAN di stderr (+`peringatan_kunci` di JSON sukses); file hilang/kosong/644/2 baris/biner/folder → kode 5, 0 permintaan ke Dolibarr; ENV diabaikan tidak pernah dikirim/tercetak; 0 kunci & 0 traceback di 72 keluaran |
| Panduan §2.4 vs script | ✅ konsisten (lokal saja kecuali opt-in, https wajib untuk internet, kunci via `simpan-kunci` tanpa argumen/riwayat shell, file 600 di luar folder skill, izin minimum di §6) |

### Cacat tersisa
- **C1 (sedang-rendah, baru):** pembuatan draf belum idempoten terhadap timeout/koneksi putus: draf kosong Rp 0 yatim + saran "coba lagi" → draf kedua; draf sebagian berakhir kode 0 dengan teks "Validasi" dan penjelasan selisih sen yang tidak cocok. Saran di `08-…` §5.
- Kosmetik: `--kunci-file ""` jatuh ke ENV tanpa peringatan; `peringatan_kunci` tidak ada di JSON galat; toleransi efektif ± Rp 1,49 (dokumen: < Rp 1); panduan §7 `api_komunitech` vs §6 `api_baca`/`api_draf`.

### Skor kualitas: **8 / 10** — **LULUS** (≥ 7)
Alasan:
- (+) B1 dan B2 terbukti beres terhadap reproduksi aslinya dan variasi data rusak; tidak ada regresi (77 tes, angka 0 beda, 0 kebocoran kunci, 0 POST tanpa `--ya`).
- (+) B2 menutup celah pemisahan kunci baca/draf yang dijanjikan panduan §6/§10; §2.4 jujur dan sesuai perilaku script.
- (−) C1: jaring pengaman draf dobel masih bisa ditembus pada skenario timeout yang realistis di komputer toko yang lambat (pesan justru menyarankan mengulang). Draf tidak sah dan diperiksa manusia, jadi tidak menghalangi `lulus`.
- (−) Tidak diuji ulang di Dolibarr asli pada versi ini (hanya tiruan + satu angka asli dari uji v1.0.2).
- **Kesimpulan:** v1.0.3 layak lanjut ke uji platform asli/beta; perbaiki C1 (pesan galat koneksi pada perintah tulis + deteksi draf kosong/sebagian) di v1.0.4.

---

## Uji ulang v1.0.4 (Akun B)
- **Tanggal:** 2026-09-25
- **Penguji:** agent penguji independen lintas akun (Akun B, Claude Code, simulasi agent). Bukan pembuat skill maupun pembuat perbaikan C1. Rincian lengkap ada di `09-uji-ulang-v1.0.4.md`.
- **Lingkungan:** salinan skill di scratchpad. Server Dolibarr **tiruan** (data dari rekaman 24.0.1) dengan **pengganggu buatan penguji**: putus, RST, timeout, 500/502/504, dan jawaban terpotong. Semua gangguan terjadi **setelah** data diproses. **Tidak** diuji di Dolibarr asli. Python 3.11.15.
- **Otomatis:** `uji_regresi.py` **85 tes OK** (1 dilewati di salinan, khusus repo). `validate.py --skill dolibarr-usaha` ✅ valid.
- **Platform teruji:** `claude-code (simulasi agent)`.

### Status klaim
| Klaim | Status |
|---|---|
| C1: putus/timeout saat menulis → kode 8 "mungkin sudah tersimpan", bukan "coba lagi" | ✅ Terbukti untuk putus, RST, dan timeout di POST header, baris 1/2/3, dan baca ulang akhir. ⚠️ Balasan 5xx atau jawaban terpotong menghasilkan kode 6 atau teks "DITOLAK", tanpa draf ganda (D1, D2) |
| C1: draf kosong/sebagian menahan perintah yang sama (kode 7) | ✅ 31 skenario × ulang 3×: **0 draf ganda**, 0 POST pada ulangan. Setiap skenario berakhir dengan tepat 1 draf |
| C1: sidik perintah di catatan privat | ✅ Ada di semua draf. Draf sebagian dikenali lewat sidik |
| Perintah berbeda untuk pelanggan sama tidak salah diblokir | ✅ Dengan draf **sebagian**: 23/23 dibuat. ⚠️ Dengan draf **kosong** milik perintah lain: tertahan, dan teks mengarahkan ke item yang keliru (D3, rendah, bisa `--tetap-buat`) |
| B1 regresi (DPP bersen, PPN floor sekali, `Decimal` penguji) | ✅ 6 pola, **0 beda**, ulang 3× → `[7,7,7]`, 0 POST |
| B2 regresi (`--kunci-file` vs ENV, kunci tak tercetak) | ✅ 0 kunci dan 0 traceback di 243 keluaran |

### Cacat tersisa
- **D1 (rendah):** 502/504/500 pada permintaan tulis diperlakukan sebagai pasti gagal. Akibatnya muncul kode 6 atau "baris ini tidak masuk", padahal data mungkin tersimpan. Pengulangan tetap tertahan.
- **D2 (rendah):** `IncompleteRead` (jawaban terpotong) menghasilkan "Galat tak terduga", kode 6, tanpa panduan cek draf.
- **D3 (rendah):** draf kosong bersidik perintah lain tetap menahan perintah berbeda, dan saran "lengkapi sesuai pratinjau" menyesatkan.
- D4 (info): pengulangan draf sebagian pada tanggal lain tidak dikenali. Balapan dua proses tidak dicegah. Kosmetik K-a s.d. K-d masih ada.

### Skor kualitas: **8 / 10** (**LULUS**, ≥ 7)
Alasan:
- (+) C1 beres untuk semua gangguan yang disebut dalam temuan: tidak ada draf ganda di 31 titik putus × 3 pengulangan. Pesan kode 8 jujur dan melarang mengulang. Draf sebagian tidak lagi berakhir dengan "COCOK" atau "Validasi". Perintah lain tidak terhalang oleh draf sebagian.
- (+) Tidak ada regresi: 85 tes, angka B1 0 beda dengan `Decimal` penguji, B2 utuh, 0 kebocoran kunci.
- (−) Galat 5xx dan jawaban terpotong saat menulis belum masuk jalur "mungkin tersimpan" (D1, D2). D3 bisa membingungkan pengguna awam. Belum diuji di Dolibarr asli.
- **Kesimpulan:** v1.0.4 layak lanjut ke uji platform asli dan beta. D1–D3 disarankan diperbaiki di versi berikutnya, tetapi tidak menghalangi status `lulus`.

## Uji ulang v1.0.5 (Akun B)
- **Tanggal:** 2026-09-25
- **Penguji:** agent penguji independen lintas akun (Akun B, Claude Code, simulasi agent). Bukan pembuat skill dan bukan pembuat perbaikan D1–D3. Rincian lengkap ada di `10-uji-ulang-v1.0.5.md`.
- **Lingkungan:** salinan skill di scratchpad. Server Dolibarr **tiruan** (data rekaman 24.0.1) dengan **pengganggu buatan penguji**: putus, RST, lambat, 500/502/503/504 (HTML/JSON/kosong/terpotong), jawaban terpotong 0/1/n−1 bita, baris status rusak, serta kontrol tanpa diproses (5xx, 501, 503-blokir-IP). **Tidak** diuji di Dolibarr asli. Python 3.11.
- **Otomatis:** `uji_regresi.py` **93 tes OK**. `validate.py --skill dolibarr-usaha` ✅ valid.
- **Platform teruji:** `claude-code (simulasi agent)`.

### Status klaim
| Klaim | Status |
|---|---|
| D1: 5xx saat MENULIS → kode 8 "MUNGKIN SUDAH TERSIMPAN" | ✅ POST header, baris 1–3, `pelanggan tambah`, untuk 500/500json/502/503/504/504kosong/504terpotong. Baris yang tersimpan tidak lagi disebut "DITOLAK". Baca ulang menyimpulkan "SUDAH/BELUM masuk" dengan benar (kontrol tolak → BELUM) |
| D1: 501 dan 503-blokir-IP tetap pasti gagal | ✅ POST: kode 4 / kode 5, tanpa "mungkin tersimpan". Baris: "DITOLAK … tidak masuk". Ulangan boleh membuat draf |
| D1/D2: 5xx atau jawaban terpotong saat MEMBACA tetap galat biasa | ✅ 5 perintah baca × 6 gangguan: kode 6 (5xx) / kode 3 "terpotong/rusak", 0 "mungkin tersimpan" |
| D2: jawaban terpotong → pesan jelas, bukan "Galat tak terduga" | ✅ IncompleteRead (0/1/n−1 bita) dan BadStatusLine saat menulis → kode 8. **0** "Galat tak terduga" di 580 keluaran |
| D3: draf kosong dari perintah LAIN hanya CATATAN | ✅ A dibuat (kode 0) dengan CATATAN dan JSON `draf_kosong_lain`. B yang diulang tetap 7 dengan tindakan "Hapus draf kosong". Kalimat menyesatkan sudah hilang |
| D3: perintah SAMA, atau draf kosong tanpa kode sah, tetap menahan | ✅ kode 7, 0 POST (termasuk kode palsu/huruf kecil) |
| C1: banyak titik putus, ulang 3× | ✅ 80 skenario, 240 pengulangan → **0 draf ganda**. Setiap skenario berakhir dengan tepat 1 draf |
| B1 regresi (DPP bersen, PPN floor sekali, `Decimal` penguji) | ✅ 6 pola, 0 beda, `[7,7,7]` |
| B2 regresi (`--kunci-file` vs ENV, kunci tak tercetak) | ✅ 62/62 OK. 0 kunci di 580 keluaran |

### Cacat tersisa
- **D5 (info):** Dolibarr memakai 500 "Error creating invoice" juga untuk penolakan bisnis. Kasus ini kini berlabel "mungkin tersimpan". Tetap aman karena ada cek ulang dan ulangan tidak ditahan, tetapi bisa membingungkan bila terus berulang.
- **D4' (info):** draf kosong sisa perintah yang sama tetapi bertanggal lain kini hanya menghasilkan CATATAN "perintah LAIN". Tidak ada risiko tagihan ganda.
- Balasan 200 non-JSON saat menulis, balapan dua proses, dan kosmetik K-a s.d. K-d masih ada.

### Skor kualitas: **9 / 10** (**LULUS**, ≥ 7)
Alasan:
- (+) D1, D2, dan D3 terbukti beres dengan gangguan buatan penguji sendiri. Cakupannya lebih luas dari tes pembuat: 503, 504 kosong/terpotong, BadStatusLine, dan terpotong 0/n−1 bita.
- (+) Pembedaan tulis vs baca serta 501/503-IP berjalan sesuai dokumentasi. Pesan kode 8 jujur, dan kesimpulan "baris N SUDAH/BELUM masuk" benar di semua kontrol.
- (+) Tidak ada regresi: 0 draf ganda di 80 titik × 3 ulangan, angka B1 0 beda, B2 utuh, 93 tes OK, dan 0 kebocoran kunci.
- (−) Belum diuji di Dolibarr/DoliWamp asli. Masih ada D5/D4' (info) dan kosmetik lama.
- **Kesimpulan:** v1.0.5 layak lanjut ke uji platform asli dan beta.
