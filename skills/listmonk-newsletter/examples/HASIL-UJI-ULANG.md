# HASIL UJI ULANG - listmonk-newsletter 1.0.1 (penguji independen, 29 Sep 2026)
Lingkungan: **listmonk v6.2.0 ASLI** (Docker, postgres:17, port 127.0.0.1:9100) + **mailpit** sebagai SMTP penampung; pengguna API berperan sesuai panduan §7; HOME sementara agar `~/.komunitech` bersih. Semua kontak/alamat fiktif (`*.test`). Penguji hanya membaca folder skill, `docs/panduan-listmonk.md`, CLAUDE.md. Token tidak dicetak. `python3 scripts/validate.py --skill listmonk-newsletter` lolos; `tests/uji_regresi.py` 53 tes OK. Kontainer dihentikan setelah uji.

## Gerbang yang dicoba dibobol
| Gerbang | Percobaan | Hasil (listmonk asli) |
|---|---|---|
| Wajib uji-kirim | kirim tanpa uji; `--tanpa-uji`; id kampanye lain; ubah isi (body, subjek, template_id, pengirim) setelah uji | DITOLAK semua. `--tanpa-uji` tidak dikenal. Catatan per id + sidik bekerja |
| Sama tetapi tidak dicakup sidik | ubah `altbody` (teks polos), `headers`, **daftar penerima (lists)**, **isi template** setelah uji | **LOLOS** (tetap "SUDAH (isi sama)"). Sidik hanya memuat subjek, isi, template_id, tipe, pengirim |
| Catatan lokal dipalsukan | tulis `listmonk-uji.json` lewat fungsi skrip | LOLOS untuk pihak dengan akses shell (JSON polos tanpa tanda tangan, izin 644). Belum diakui terang di SKILL untuk berkas ini (hanya untuk alamat uji) |
| Alamat uji | `--ke` alamat asing; tanpa alamat terdaftar | DITOLAK, tak membuat pelanggan. Tetapi `simpan-alamat-uji` ditolak tanpa tty, **lolos lewat pty palsu (`script`)** dan frasa konfirmasi tercetak di layar. Keterbatasan agen-berakses-shell diakui di catatan revisi |
| Tautan berhenti | tag di `<!-- -->` dan `{{/* */}}` (template tanpa tautan) | DITOLAK (benar). Salah ketik `UnsubscribeUrl` ditolak listmonk saat kompilasi. `{{UnsubscribeURL}}` tanpa spasi diterima |
| Tautan berhenti | tag di `<script>` lewat `buat-kampanye` | DITOLAK. Tetapi kampanye yang dibuat di layar/API listmonk dengan `<script>`+tag **lolos lint, uji-kirim, dan gerbang kirim**; email uji tidak punya tautan `<a>` berhenti |
| Tautan berhenti | tag di atribut `alt`, `<style>`, `display:none`, komentar tak tertutup | Lolos lint; email uji (kasus `alt`) hanya memuat URL di atribut, bukan tautan yang bisa diklik. Pemeriksaan statis menghitung kemunculan, bukan tautan |
| Sumber persetujuan | BELI, database, DATABASE, jual beli, "Grup W.A.", "G r u p WA", nama berkas `database-beli.csv`, kolom `sumber` berisi Grup WA | DITOLAK. Besar-kecil huruf, spasi, ejaan angka teratasi |
| Sumber persetujuan | "Hasil **pembelian** dari agensi", "Data **sewaan**", "pihak ketiga / third party", "mitra bisnis", "lead generation", "dapat dr temen", "hasil akuisisi" | Tidak dikenali terlarang -> masuk `tak_dikenal`: ditolak tanpa `--pengguna-konfirmasi-setuju`, tetapi **"pembelian" + jawaban karangan ("Ya, saya yakin setiap orang sudah setuju") diterima** (sampai ringkasan). Konfirmasi tak dapat dibedakan dari agen yang mengarangnya |
| Singkatan opsi | `--y` di `kirim`, `impor` | DITOLAK ("unrecognized arguments") |
| Jumlah penerima | N salah, 0, negatif, tanpa `--ya`, list ganti | DITOLAK; angka harus sama dengan hitungan terbaru. Kirim sungguhan (2 penerima) sampai ke mailpit dengan benar |

## Yang terbukti dari revisi 1.0.1
P1 nomor 1-4 pada dasarnya **berfungsi di listmonk asli**: opsi pintas hilang, singkatan ditolak, tautan berhenti di komentar ditolak, alamat uji dibatasi lewat perintah skill, saringan sumber jauh lebih rapat. Alur nyata (impor, kampanye, uji kirim, kirim, mailpit menerima) berjalan.

## Kelemahan tersisa (tidak menggagalkan, tetapi harus jujur di dokumen)
1. Sidik uji-kirim tidak mencakup `altbody`, `headers`, **lists**, isi template. Rekomendasi: masukkan semuanya (atau sidik hasil render).
2. Lint tautan berhenti: hapus/abaikan blok `<script>`/`<style>`, cari `href="...UnsubscribeURL..."` (atau `@` di atribut `href`), dan jalankan lint `<script>` juga di `uji-kirim`/gerbang, bukan hanya di `buat-kampanye`.
3. Saringan sumber: tambah "pembelian/pembelian", "sewaan", "pihak ketiga", "third party", "agensi/agency", "mitra", "lead"; catat bahwa konfirmasi pengguna dapat dikarang agen (sudah disebut "pengaman tambahan").
4. SKILL/README: nyatakan terang bahwa `listmonk-uji.json` dan alamat uji tidak kebal terhadap agen dengan akses shell (pty/menulis berkas), pengaman melawan kelalaian, bukan penyerang. `listmonk-uji.json` dibuat izin 644; sebaiknya 600.
5. Tidak diuji (tetap PERLU UJI NYATA): SMTP sungguhan, inbox Gmail/Yahoo, Windows/macOS, HTTPS.

## Skor kualitas: 7/10 - LULUS (dengan catatan P2 di atas)
Alasan: semua celah P1 yang ditemukan uji pertama tertutup dan terverifikasi di listmonk asli; klaim di SKILL/README (`tidak ada opsi untuk melewatinya`, `--y ditolak`, tag di komentar tidak dihitung) benar. Tidak naik ke 8 karena masih ada bypass nyata di jalur normal listmonk (sidik tak mencakup lists/altbody/template; tautan berhenti di `<script>`/atribut lolos; sinonim beli). Semuanya butuh niat/kelalaian di luar alur skill, dan dampak jumlah penerima tetap dijaga gerbang N. Status disarankan: `lulus` -> uji platform asli pemilik; kerjakan poin 1-4 sebelum `rilis`.
