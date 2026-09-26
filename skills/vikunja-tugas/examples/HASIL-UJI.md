# HASIL UJI — vikunja-tugas v1.0.0

**Penguji:** Akun B (independen, hanya membaca folder `skills/vikunja-tugas/` + `docs/panduan-vikunja.md`).
**Tanggal:** 2026-09-26 (commit diuji: 3c31bac).
**Lingkungan:** Vikunja **v2.6.0 ASLI**, binary resmi `vikunja-v2.6.0-linux-amd64` diunduh dari
`https://dl.vikunja.io/vikunja/v2.6.0/`, **SHA-256 dicocokkan OK** terhadap file `.sha256` yang
tersedia dalam paket unduhan resmi (upstream tidak menerbitkan checksum terpisah di halaman indeks,
hanya `.sig` PGP dan `.sha256` per-file di dalam folder rilis — checksum itulah yang dipakai, verifikasi
PGP tidak dilakukan karena keterbatasan waktu). Dijalankan sungguhan terikat `127.0.0.1:3456`
(scratchpad, bukan repo), database SQLite baru, registrasi 3 user (`pemilikuji`, `budi`, `siti`),
3 proyek, token API dibuat lewat REST API dengan skenario permission bervariasi (lihat #1). Server
dimatikan (`kill`) setelah pengujian selesai.

## Skor kualitas: **8/10**

Skrip sendiri sangat solid (62/62 uji regresi lulus, semua jalur error nyata cocok dokumentasi,
validasi URL localhost/HTTPS bekerja persis seperti diklaim, gerbang konfirmasi tulis tidak pernah
bisa dilewati, tidak ada pola berbahaya di kode). Diturunkan dari 9-10 karena **Temuan #1** —
klaim "penugasan (--ke) diuji ... dengan Vikunja 2.6.0 ASLI" tidak dapat direproduksi penguji
independen dengan token API mana pun yang valid menurut aturan skema tokennya sendiri, dan panduan
§6 mereferensikan nama izin ("Tasks Assignees") yang tidak berhasil dipetakan ke skema JSON API asli
manapun yang saya coba.

## Temuan berprioritas

### 1. TINGGI — fitur `--ke` (penugasan) gagal via token API di Vikunja 2.6.0 asli; nama izin "Tasks Assignees" di panduan §6 tidak dapat direproduksi
Dengan token API (`tk_...`) berisi SEMUA kombinasi izin proyek/tugas yang valid menurut validator
Vikunja sendiri (`projects: read_all, read_one, projectusers` + `tasks: read_all, read_one, create,
update`), memanggil `PUT /api/v1/tasks/{id}/assignees` **selalu** ditolak dengan
`{"code":11,"message":"missing, malformed, expired or otherwise invalid token provided"}` — bukan
403 (kurang izin), tapi seolah token itu sendiri tidak valid untuk endpoint ini. Saya mencoba >12
kombinasi nama grup izin (`task_assignees`, `taskassignees`, `assignees`, `assignees_create`,
`assignees_readall`, dst.) lewat `PUT /api/v1/tokens` — semua ditolak "invalid" oleh validator Vikunja
sendiri KECUALI kombinasi yang sudah dipakai skill (`projects`+`tasks` seperti di atas), yang lolos
validasi token tapi tetap gagal saat dipakai. Saya konfirmasi endpoint itu SENDIRI berfungsi normal
memakai sesi JWT pemilik (login biasa) — jadi ini bukan galat skrip Komunitech, dan skrip menangani
kegagalannya dengan benar (tugas tetap tersimpan, pesan jujur, tidak mengulang otomatis). Tapi ini
berarti: (a) SKILL.md/README yang mengklaim `--ke` "diuji ... dengan Vikunja 2.6.0 ASLI" perlu
diklarifikasi ulang — kemungkinan pembuat mengujinya dengan token yang dibuat lewat UI browser (bukan
API mentah), yang mungkin memetakan nama izin secara berbeda; (b) panduan §6 tabel izin token
("Tasks Assignees") kemungkinan tidak sesuai skema API asli 2.6.0, berisiko membingungkan pembeli
yang mencoba membuat token via UI dan tidak menemukan nama itu persis. **Rekomendasi:** pembuat
menguji ulang `--ke` dari nol dengan token yang benar-benar baru dibuat lewat UI Vikunja (bukan warisan
sesi lama), screenshot nama izin persis yang dicentang, dan perbarui §6 bila berbeda dari yang tertulis.
Bukti lengkap & langkah reproduksi ada di `01-toko-bangunan-uji-akun-b.md` dan `02-kantor-konsultan-uji-akun-b.md`.

### 2. SEDANG — dua laporan bisa tampilkan tugas yang sama tanpa disebutkan eksplisit
Tugas yang jatuh tempo hari ini TAPI jamnya sudah lewat akan muncul di **`hari-ini` maupun
`terlambat` sekaligus** (perilaku disengaja & konsisten — `hari-ini` = rentang tanggal, `terlambat` =
instant sudah lewat — bukan bug). SKILL.md tidak menyebutkan ini secara eksplisit; agent/pembeli yang
menjumlahkan kedua daftar bisa salah hitung total tugas unik. Saran: tambahkan satu kalimat di bagian
C SKILL.md. Lihat `01-toko-bangunan-uji-akun-b.md`.

### 3. RENDAH — checksum SHA-256 upstream tidak dipublikasikan terpisah di halaman indeks
`docs/panduan-vikunja.md`/SKILL.md menyebut "checksum SHA-256 dicocokkan" tapi tidak menjelaskan bahwa
Vikunja hanya menerbitkan `.sha256` per-file di dalam folder rilis (bukan halaman checksum terpisah)
dan `.sig` untuk verifikasi PGP penuh. Tidak menghalangi verifikasi (saya berhasil memverifikasi
SHA-256-nya), tapi baik dicatat di panduan agar pembeli tahu ke mana harus mencari file `.sha256` itu
(nama filenya mengikuti nama binary, bukan `checksums.txt` generik).

### 4. RENDAH — pola "PIC: Nama - tugas" tidak menghasilkan PIC terdeteksi
Lihat `03-kafe-uji-akun-b.md` — bukan bug (sesuai aturan "PIC" dikecualikan sebagai nama), tapi notasi
ini umum dipakai orang Indonesia di notulen dan berpotensi membuat PIC tidak terdeteksi diam-diam.
Saran peningkatan versi mendatang (bukan blocker rilis).

## Cakupan uji (checklist tugas)
- [x] 5 skenario: 3 normal (`01`,`02`,`03` — termasuk `dari-teks` dua varian), 1 input tidak lengkap (`04`, 4 varian termasuk proyek ambigu), 1 di luar cakupan/berisiko (`05`, 4 varian)
- [x] Uji A/B tanpa vs dengan skill → `00-pembanding-tanpa-skill-uji-akun-b.md`
- [x] Uji banding pesaing (web search) → `00-banding-pesaing-uji-akun-b.md`
- [x] Token berizin minimal dicoba (lihat Temuan #1)
- [x] Penolakan URL non-localhost (IP publik & domain publik http) → `05a`/`05b`
- [x] Konfirmasi sebelum menambah/menyelesaikan tugas → `01`,`05c` (diverifikasi via `cari` bahwa data tidak masuk tanpa `--ya`)
- [x] Tanggal Indonesia ("besok","lusa","Jumat","N hari lagi","25/10") diverifikasi manual terhadap tanggal acuan 26 Sep 2026 — semua BENAR
- [x] 401 (token salah), 404 (id tidak ada), timeout/connection-refused → semua diuji dengan server nyata, pesan sesuai dokumentasi
- [x] Jadwal `automations add` 07.00 WIB ke Telegram: pola di `references/openclaw-jadwal.md` memakai cron `"0 7 * * *" --tz Asia/Jakarta`, hanya perintah baca, token tidak pernah masuk argv — sudah benar dan jujur menyatakan belum diuji di Gateway sungguhan untuk skill ini
- [x] `tests/uji_regresi.py`: **62/62 lulus**
- [x] `scripts/validate.py --skill vikunja-tugas`: **lulus** ("1 skill valid, 80 baris katalog sesuai")
- [x] Panduan (`docs/panduan-vikunja.md`) diikuti langkah demi langkah oleh penguji tanpa pengalaman Vikunja sebelumnya — bisa diikuti, hanya kendala di §6 (Temuan #1)
- Tidak dijalankan: `scripts/uji_openclaw.sh` (sesuai instruksi tugas)

## Catatan keamanan (Tahap 3)
Tidak ditemukan perintah destruktif, pengiriman data ke server luar di luar Vikunja tujuan, pembacaan
kredensial/SSH/browser data, unduh-lalu-jalankan-shell, kode ter-obfuscate, atau dependensi mencurigakan
(`import` hanya modul stdlib Python). Tidak ada API key/token tertanam di kode. Instruksi SKILL.md
tidak mengandung prompt injection tersembunyi.
