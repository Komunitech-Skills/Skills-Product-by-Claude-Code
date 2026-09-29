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

## Tindak lanjut Temuan #1 & #2 (v1.0.1, 2026-09-26)
Diagnosis ulang dengan Vikunja 2.6.0 ASLI (binary linux-amd64 baru diunduh dari `dl.vikunja.io`,
checksum SHA-256 di dalam zip dicocokkan OK, dijalankan sungguhan terikat `127.0.0.1`, dimatikan
setelah selesai) plus kode sumber frontend `go-vikunja/vikunja` tag `v2.6.0`
(`frontend/src/components/token/ApiTokenForm.vue`):

- **`--ke` DIDUKUNG token API.** Memanggil `PUT /api/v1/tokens` lewat sesi JWT pemilik dengan
  kelompok izin `tasks_assignees: [create, read_all]` (nama kelompok persis seperti yang dipakai
  server sendiri di `/api/v1/routes`) lalu memakai token itu untuk `PUT /api/v1/tasks/{id}/assignees`
  **berhasil** (dites 2x, task baru & task lama). Tanpa kelompok `tasks_assignees` sama sekali,
  panggilan yang sama gagal persis seperti temuan Akun B: `{"code":11,"message":"missing, malformed,
  expired or otherwise invalid token provided"}` (HTTP 401) — bukan 403. Kesimpulan: bukan skrip yang
  salah dan bukan fitur tak didukung; akar masalahnya kemungkinan besar Akun B tidak pernah mencoba
  ejaan kelompok yang benar (`tasks_assignees`, jamak+garis bawah) di antara >12 kombinasi yang
  dicoba (semua varian yang disebut di Temuan #1 pakai `task_assignees` tunggal atau tanpa garis
  bawah).
- **Nama di panduan §6 sudah benar untuk label yang tampil di layar** ("Tasks Assignees") —
  dikonfirmasi dari kode sumber `ApiTokenForm.vue`: nama kelompok/izin ditulis dengan garis bawah
  (`tasks_assignees`, `projectusers`, dst.) lalu tampilan menggantinya jadi spasi + huruf kapital tiap
  kata lewat CSS. **Yang SALAH** di §6 lama: baris "Projects: Project Users" — kotak yang sebenarnya
  dibutuhkan bernama **"Projectusers"** (satu kata, tanpa spasi, di DALAM kelompok "Projects"),
  BUKAN kelompok terpisah "Projects Users" (yang mengatur keanggotaan proyek, bukan lookup nama).
  §6 sudah diperbaiki dengan nama persis + penjelasan bahwa "Tasks Assignees" adalah kelompok
  TERPISAH yang mudah terlewat, dan pesan galat skrip (`cmd_tambah`) sekarang menyebut kemungkinan
  penyebab ini secara eksplisit saat 401 terjadi tepat di langkah penugasan.
- **Temuan #2 (tumpang tindih `hari-ini`/`terlambat`)**: dikonfirmasi sebagai perilaku disengaja.
  Ditambahkan catatan otomatis di output kedua perintah (`CATATAN_TUMPANG_TINDIH`) + penjelasan di
  `SKILL.md` bagian C.
- Dua uji regresi baru ditambahkan (total 64): (1) token tanpa `tasks_assignees` menghasilkan pesan
  galat yang menyebut kelompok "Tasks Assignees" secara eksplisit; (2) output `hari-ini`/`terlambat`
  memuat catatan tumpang tindih. 64/64 lulus, `scripts/validate.py --skill vikunja-tugas` lulus.
- Klaim "diuji ... penugasan (--ke) ... dengan Vikunja 2.6.0 ASLI" di `SKILL.md`/`README.md`
  **dipertahankan** (bukan dihapus) karena kini direproduksi ulang secara independen lewat REST API
  mentah terhadap server v2.6.0 sungguhan — lihat langkah di atas — bukan sekadar klaim pembuat asli.
  Server uji & token dibuat di scratchpad sekali pakai lalu dimatikan/dibuang setelah sesi ini,
  sesuai aturan keamanan pengujian (tidak ada token nyata yang bocor ke repo).

## Uji ulang independen v1.0.1 (Akun B, 2026-09-26)

**Penguji:** Akun B lain (independen dari sesi revisi v1.0.1 di atas), membaca hanya folder skill
+ `docs/panduan-vikunja.md`. Detail lengkap: `examples/06-uji-ulang-v101-akun-b.md`.

**Skor kualitas (revisi): 9/10.** Naik dari 8/10 karena Temuan #1 (TINGGI) dan #2 (SEDANG) dari
uji v1.0.0 di atas **terverifikasi telah diperbaiki dan direproduksi ulang dari nol** dengan
Vikunja 2.6.0 asli (binary baru diunduh, checksum SHA-256 dicocokkan OK, dijalankan terikat
`127.0.0.1:3456`, dimatikan setelah selesai) — bukan hanya membaca laporan sesi revisi
sebelumnya. Tidak 10/10 karena satu prasyarat tidak eksplisit di SKILL.md/README: `--ke` baru
berhasil setelah target user ditambahkan sebagai kolaborator proyek (langkah manusia di Vikunja,
konsisten dengan batasan skill "mengatur anggota tim dilakukan manusia", tapi tidak disebutkan
sebagai prasyarat langsung di bagian D SKILL.md).

**Temuan yang dikonfirmasi:**
- Token dibuat lewat `PUT /api/v1/tokens` persis mengikuti tabel izin panduan §6
  (`projects: read_all/read_one/projectusers`, `tasks: read_all/read_one/create/update`,
  `tasks_assignees: create/read_all`) — **diterima**. Dikonfirmasi lewat `GET /api/v1/routes`
  server sendiri bahwa nama kelompok persis `tasks_assignees` dan `projectusers` adalah kunci di
  DALAM kelompok `projects` (bukan kelompok terpisah `projects_users`) — koreksi §6 v1.0.1 akurat.
- `--ke budi2` **berhasil** menugaskan tugas baru setelah budi2 jadi kolaborator proyek; diverifikasi
  lewat `GET /api/v1/tasks/{id}/assignees`.
- Token API **tanpa** kelompok `tasks_assignees` → `--ke` gagal dengan pesan 401 yang **secara
  eksplisit menyebut "Tasks Assignees"** sebagai kemungkinan penyebab — sesuai klaim revisi v1.0.1.
- Tumpang tindih `hari-ini`/`terlambat`: direproduksi dengan tugas bertenggat "hari ini jam 06:00"
  (lewat) — muncul di kedua laporan, catatan peringatan tampil di keduanya.
- Regresi lain lulus: tanggal Indonesia (9 format dicek manual terhadap 26 Sep 2026, semua benar),
  gerbang konfirmasi (tanpa `--ya` tidak menulis), penolakan URL non-localhost (IP LAN & domain
  publik http, keduanya ditolak dengan pesan yang benar), mode `dari-teks` (PIC & tenggat terdeteksi
  benar, baris non-bullet diabaikan & dihitung).
- `tests/uji_regresi.py`: **64/64 lulus**. `scripts/validate.py --skill vikunja-tugas`: **lulus**
  (81 baris katalog sesuai). `scripts/uji_openclaw.sh` tidak dijalankan (di luar cakupan uji ulang
  ini).

**Tidak ada temuan baru berprioritas TINGGI/SEDANG.** Satu saran RENDAH: sebutkan eksplisit di
SKILL.md bagian D bahwa `--ke` mengasumsikan target sudah jadi anggota/kolaborator proyek di
Vikunja (bukan sekadar user terdaftar di sistem), agar ekspektasi pembeli sesuai sejak awal.

---

## Uji ulang v1.0.2 (2026-09-28)

Penguji independen, scratchpad terpisah (bukan `.claude/skills/`), tidak mengubah `scripts/`/`SKILL.md`.

- **Dokumentasi `--ke` butuh kolaborator proyek**: dikonfirmasi ADA dan jelas di `SKILL.md` bagian D.4
  ("**Syarat:** orang itu harus sudah jadi **kolaborator proyek** itu di Vikunja... kalau belum, `--ke`
  gagal dengan pesan..."), lengkap dengan cara menambahkan lewat Share/Bagikan → Add User, dan rujukan
  ke `docs/panduan-vikunja.md` §6. Ini menutup saran RENDAH dari uji sebelumnya.
- **`dari-teks` label `PIC: Nama` di mana pun dalam baris** — diuji 6 baris gaya WA manual (di luar
  `tests/uji_regresi.py`):
  1. `PIC: Andi kirim penawaran ke klien besok` → `ke="Andi"` benar.
  2. `Follow up vendor PIC: Budi Santoso sebelum Jumat` (label di tengah) → `ke="Budi Santoso"` benar.
  3. Jebakan negatif: `Deadline: kirim laporan sebelum PIC berubah` (kata "PIC" tanpa titik dua
     setelahnya) → tidak terdeteksi sebagai PIC (benar, tidak ada label eksplisit).
  4. Jebakan huruf kecil: `pic: rina follow up supplier` → **tidak terdeteksi** (regex label hanya
     cocok "PIC" huruf besar; pola umum `Nama:` juga menolak karena "pic" ada di daftar `_BUKAN_NAMA`).
     Perilaku konsisten & aman (tidak salah tangkap), tapi berarti PIC gaya WA huruf kecil terlewat.
  5. **TEMUAN (sedang, bukan regresi v1.0.2 — sudah ada sejak pola umum `Nama: tugas` dibuat):**
     `TOPIC: bahas rencana marketing minggu depan` → pola umum `_POLA_PIC` (bukan `_POLA_PIC_LABEL`)
     salah menangkap kata "TOPIC" sebagai **nama orang** (`ke="TOPIC"`) dan menghapusnya dari judul,
     karena "TOPIC" tidak ada di set `_BUKAN_NAMA` (yang hanya berisi kata Indonesia seperti
     "catatan"/"deadline") padahal berbentuk "Kata:" satu kata berhuruf besar di awal — persis pola
     yang dipakai untuk mendeteksi PIC. Kata header umum WA/email lain yang berpotensi sama:
     "INFO:", "UPDATE:", "STATUS:", "SUBJECT:". Saran perbaikan: tambahkan padanan Inggris umum ke
     `_BUKAN_NAMA` atau wajibkan nama PIC minimal 2 kata untuk pola umum (label eksplisit `PIC:` tetap
     boleh 1 kata).
  6. `Siapkan invoice PIC: Maya` (label di akhir baris) → `ke="Maya"`, judul `"Siapkan invoice"` benar.
- `tests/uji_regresi.py`: **67/67 lulus**, tanpa regresi.

**Skor: 9/10.** Dokumentasi `--ke` dan deteksi label `PIC:` di v1.0.2 bekerja sesuai klaim changelog,
tanpa regresi. Satu poin ditahan untuk temuan SEDANG di atas (pola umum `Nama:` bisa salah tangkap kata
non-nama berbahasa Inggris seperti "TOPIC:" sebagai PIC) — tidak menghalangi status `lulus` saat ini,
disarankan diperbaiki di revisi berikutnya.

## Uji ulang (2026-09-29) - v1.0.3 - penguji independen
Tes regresi 69/69 OK. 21 baris gaya WA (bullet) lewat `dari-teks`:
- `TOPIC:`, `INFO:`, `UPDATE:`, `NOTE:`, `AGENDA:`, `FYI:`, `Perihal:`, `Action:`, `Reminder:`, `Hasil rapat:`, `Catatan:`, `Urgent:`, `Deadline:` -> tanpa PIC, judul utuh (tanggal Jumat/besok/25/10 tetap terbaca benar). Nama asli `Budi:`, `ANDI:`, `Siti Aminah -`, `PIC: Rina/Andi` (awal & akhir) terbaca. `--anggota "Topic,Tono,Info"` menang atas daftar kata header (perilaku sesuai dokumen).
- Temuan RENDAH: kata pembuka umum yang tidak ada di daftar, mis. `Mohon: Bu Rina tolong kirim faktur`, masih jadi PIC "Mohon" (draf tetap wajib diperiksa pengguna, sudah diperingatkan `_dugaan`). Baris tanpa bullet tidak dibaca (sesuai aturan).
**Skor: 8,5/10. Lulus.**
