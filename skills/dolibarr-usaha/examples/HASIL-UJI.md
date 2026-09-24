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
