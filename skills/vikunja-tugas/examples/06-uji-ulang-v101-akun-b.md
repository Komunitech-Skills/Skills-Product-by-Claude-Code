# Uji ulang independen — vikunja-tugas v1.0.1 (Akun B, 2026-09-26)

**Penguji:** Akun B (independen, membaca folder skill + `docs/panduan-vikunja.md` saja).
**Tujuan:** memverifikasi ulang perbaikan v1.0.1 atas Temuan #1 (TINGGI, `--ke` "invalid token")
dan Temuan #2 (SEDANG, tumpang tindih `hari-ini`/`terlambat`) dari `HASIL-UJI.md` v1.0.0, dengan
Vikunja **v2.6.0 ASLI**.

## Lingkungan
- Binary resmi `vikunja-v2.6.0-linux-amd64-full.zip` diunduh dari `https://dl.vikunja.io/vikunja/v2.6.0/`
  (di luar repo, scratchpad sesi).
- Checksum SHA-256 di dalam zip (`vikunja-v2.6.0-linux-amd64.sha256`) dicocokkan dengan `sha256sum -c` →
  **OK**.
- Dijalankan dengan `config.yml` `service.interface: 127.0.0.1:3456` (log server mengonfirmasi
  `HTTP server listening on 127.0.0.1:3456`, bukan `0.0.0.0`).
- Dua user dibuat (`pemilikuji2`, `budi2`), satu proyek ("Toko Uji Ulang", id 6).
- Server dimatikan (`kill`) setelah seluruh pengujian selesai; tidak ada proses Vikunja tersisa.
- Tidak ada token/kredensial yang disalin ke repo — hanya di file sementara di scratchpad (HOME
  tiruan), dihapus bersama server setelah sesi.

## 1. Token dibuat PERSIS mengikuti panduan §6 (tabel izin)
Dibuat lewat `PUT /api/v1/tokens` (setara isian checkbox UI) dengan payload permission:
- Token baca: `projects: [read_all, read_one]`, `tasks: [read_all, read_one]` → **diterima (201)**.
- Token tulis+tugaskan: `projects: [read_all, read_one, projectusers]`,
  `tasks: [read_all, read_one, create, update]`, `tasks_assignees: [create, read_all]` →
  **diterima (201)**.

Dikonfirmasi lewat `GET /api/v1/routes` (peta rute resmi server, bukan tebakan) bahwa nama kelompok
persis `tasks_assignees` (endpoint `PUT/GET /api/v1/tasks/:projecttask/assignees`), dan bahwa
`projectusers` adalah kunci **di dalam** kelompok `projects` (endpoint
`GET /api/v1/projects/:project/projectusers`) — terpisah dari kelompok top-level `projects_users`
(mengatur keanggotaan proyek). Ini cocok persis dengan koreksi panduan §6 v1.0.1.

## 2. Alur `--ke` (penugasan) end-to-end
1. `daftar-proyek` → menampilkan "Toko Uji Ulang (id 6)", benar.
2. `tambah --ke budi2` (budi2 BELUM anggota proyek) → tugas tersimpan, penugasan **gagal** dengan
   pesan yang menyebut kemungkinan penyebab (anggota belum ada di proyek) — sesuai dokumentasi
   ("bila gagal, tugas tetap tersimpan").
3. Setelah `budi2` ditambahkan sebagai kolaborator proyek (`PUT /api/v1/projects/6/users`,
   langkah manusiawi yang setara "Teams/Admin" di UI, sesuai batasan skill), `tambah --ke budi2 --ya`
   → **BERHASIL**. Diverifikasi lewat `GET /api/v1/tasks/4/assignees` → `budi2` tercantum sebagai
   assignee.
- **Kesimpulan: `--ke` didukung dan bekerja dengan Vikunja 2.6.0 asli**, direproduksi independen dari
  nol (bukan mengandalkan klaim pembuat), asal (a) token dibuat dengan kelompok `tasks_assignees`
  sesuai §6, dan (b) target user sudah jadi kolaborator proyek (bukan langkah skill — langkah manusia
  di Vikunja, sudah tersirat di batasan SKILL.md "mengatur anggota tim... dilakukan manusia").

## 3. Token TANPA izin `tasks_assignees` → pesan 401 menyebut "Tasks Assignees"
Token baru dibuat dengan `tasks: [read_all, read_one, create, update]` + `projects: [...,projectusers]`
tapi **tanpa** kelompok `tasks_assignees` sama sekali. `tambah --ke budi2 --ya` dengan token ini:
- Tugas tetap tersimpan (#6).
- Pesan galat: *"401 dari Vikunja: ... KEMUNGKINAN BESAR PENYEBAB: token belum dicentang izin grup
  'Tasks Assignees' (Create + Read All) ..."* — **persis menyebut "Tasks Assignees"** seperti
  disyaratkan. Dikonfirmasi sesuai.

## 4. Regresi
- **Tanggal Indonesia** (acuan hari ini Sabtu, 26 September 2026): `besok`→27 Sep (Minggu), `lusa`→28
  Sep (Senin), `3 hari lagi`→29 Sep (Selasa), `Jumat`→2 Okt, `Jumat depan`→9 Okt, `minggu depan`→3 Okt,
  `25/10`→25 Okt, `25 Oktober 2026`→25 Okt, `2026-10-25`→25 Okt. **Semua benar** dicocokkan manual.
- **Gerbang konfirmasi**: `tambah` tanpa `--ya` tidak menulis apa pun (dicek lewat `cari` sebelum/
  sesudah, hasil kosong di kedua sisi).
- **Tolak URL non-localhost**: `--url http://192.168.1.10:3456` dan `--url http://vikunja.example.com`
  keduanya ditolak dengan pesan yang menyebut "bukan komputer ini (127.0.0.1/localhost)" dan
  menyarankan `--izinkan-jarak-jauh` bila memang disengaja.
- **Mode `dari-teks`**: notulen 4 baris (3 bullet + 1 baris "Catatan:" non-bullet) → 3 tugas terdeteksi
  dengan PIC (`Budi`, `Siti`) dan tenggat benar, kata "mendesak" memicu catatan prioritas, baris ke-4
  diabaikan dan dihitung eksplisit ("1 baris lain diabaikan"). Draf ditulis ke file JSON, **belum**
  masuk Vikunja (sesuai janji dokumentasi).
- **Tumpang tindih `hari-ini`/`terlambat`**: tugas baru dibuat dengan tenggat "hari ini jam 06:00"
  (sudah lewat) muncul di **kedua** laporan sekaligus, dan kedua perintah menampilkan catatan
  peringatan eksplisit — dikonfirmasi berjalan seperti didokumentasikan (perbaikan v1.0.1 untuk
  Temuan #2).

## 5. Uji otomatis
- `python3 skills/vikunja-tugas/tests/uji_regresi.py` → **64/64 lulus** (termasuk 2 tes baru v1.0.1:
  pesan galat `tasks_assignees` eksplisit, catatan tumpang tindih di output).
- `python3 scripts/validate.py --skill vikunja-tugas` → **lulus** ("1 skill valid, 81 baris katalog
  sesuai").
- `scripts/uji_openclaw.sh` **tidak dijalankan** (di luar cakupan uji ulang ini, sesuai instruksi).

## Kesimpulan
Kedua temuan v1.0.0 (TINGGI #1, SEDANG #2) **terverifikasi telah diperbaiki dan direproduksi ulang
secara independen** dengan Vikunja 2.6.0 asli, dari nol (token, user, proyek baru), tanpa
bergantung pada data/klaim sesi pembuat sebelumnya. Tidak ditemukan temuan baru berprioritas
TINGGI/SEDANG pada cakupan yang diuji ulang. Lihat penambahan skor & ringkasan di
`examples/HASIL-UJI.md` bagian "Uji ulang independen v1.0.1 (Akun B, 2026-09-26)".
