# Catatan uji pembuat — vikunja-tugas v1.0.0

**Penguji:** pembuat skill (agent sesi Komunitech Skills Factory), 2026-09-26.
**Catatan peran:** ini uji oleh **pembuat sendiri** (Akun A), bukan uji independen. Uji independen
(Akun B, `examples/HASIL-UJI.md`, `00-pembanding-tanpa-skill.md`, `00-banding-pesaing.md`) **belum**
dikerjakan — di luar cakupan tugas ini, sengaja tidak dibuat di sini.

## 1. Yang diuji & bagaimana

### 1.1 Uji regresi otomatis (`tests/uji_regresi.py`)
- **62 test** unittest, semua lulus (`python3 skills/vikunja-tugas/tests/uji_regresi.py` → `OK`).
- Cakupan: parser tanggal Indonesia (17 kasus, termasuk tanggal tidak valid seperti 31 Februari),
  `dari-teks` (8 kasus, termasuk deteksi nama, kata "PIC:" yang sengaja TIDAK dianggap nama, baris
  diabaikan), validasi URL/keamanan (6 kasus: localhost, domain publik dengan/tanpa HTTPS,
  jaringan kantor 192.168.x), `simpan-kunci`/token (6 kasus: tolak tanpa prefiks `tk_`, tolak
  timpa tanpa `--ya`, token tidak pernah tercetak di stdout/stderr, dsb.), dan **server Vikunja
  tiruan** (25 kasus ujung-ke-ujung lewat `subprocess`: cek, daftar-proyek, hari-ini, terlambat,
  tambah [pratinjau/--ya/token kurang izin/proyek tidak ada/dengan --ke berhasil & gagal], selesai
  [normal/sudah selesai/id tidak ada], ringkasan, cari, batch [normal/kosong], galat 500 saat
  menulis → kode 8, **timeout sungguhan** saat menulis (server tiruan ditunda 2 detik, `--timeout
  0.5`) → kode 8, keluaran `--json`, dan `dari-teks` yang dipastikan **tidak** memanggil jaringan
  sama sekali).
- Fixture (`tests/fixtures/vikunja-2.6.0.json`) berisi bentuk data (proyek, tugas, token, pesan
  galat 401/404, daftar grup izin) yang **direkam dari Vikunja 2.6.0 asli**, bukan dikarang.
- `python3 -m unittest discover -s skills/vikunja-tugas/tests` (tanpa argumen pola) menemukan
  **0 test** karena nama file `uji_regresi.py` tidak cocok pola bawaan `test*.py` — ini **konsisten
  dengan skill lain di repo ini** (`dolibarr-usaha`, `hledger-usaha` memakai nama file yang sama
  dan docstring yang sama, "Jalankan: python3 tests/uji_regresi.py"). Dijalankan langsung
  (`python3 skills/vikunja-tugas/tests/uji_regresi.py`), semua 62 lulus.

### 1.2 Uji integrasi terhadap Vikunja 2.6.0 ASLI (bukan simulasi)
Ini bagian yang **melampaui** uji regresi berserver-tiruan:
1. Binary resmi diunduh dari `https://dl.vikunja.io/vikunja/v2.6.0/vikunja-v2.6.0-linux-amd64-full.zip`
   (URL resmi dari `vikunja.io/docs/installing/`). Checksum SHA-256 dicocokkan dengan file
   `.sha256` bawaan paket → **COCOK**. Verifikasi tanda tangan GPG (`.sig`) **tidak selesai**
   (keyserver GPG tidak terjangkau lewat proxy sandbox, lihat `research/sources/vikunja-2026-09-26.md`
   §3) — dicatat sebagai **PERLU REVIEW**, bukan diklaim selesai.
2. Binary dijalankan sungguhan, diikat ke `127.0.0.1:3456` lewat `config.yml` (`service.interface:
   127.0.0.1:3456`), database SQLite baru.
3. Terhadap instance hidup ini, `scripts/vikunja.py` dijalankan (bukan `curl` manual) untuk:
   - `simpan-kunci` (lewat ENV untuk otomasi uji, jalur manusia interaktif diuji terpisah lewat
     `subprocess` + `getpass` di `tests/uji_regresi.py`).
   - `cek`, `daftar-proyek`.
   - `hari-ini`, `terlambat`, `minggu-ini`, `cari` — termasuk memverifikasi jendela waktu 7 hari
     TIDAK termasuk hari ke-7 (lihat `examples/03-kafe.md`).
   - `tambah` (pratinjau lalu `--ya`), termasuk dengan `--ke <username>` yang **berhasil**
     (username memang ada & token diberi izin `tasks_assignees`+`projects.projectusers`) dan yang
     **gagal dengan anggun** (username fiktif, tugas tetap tersimpan — `examples/02-kantor-konsultan.md`).
   - `tambah --batch` dari file hasil `dari-teks` (alur penuh: notulen teks → draf JSON → tugas
     sungguhan di Vikunja).
   - `selesai` (normal & "sudah selesai sebelumnya").
   - `ringkasan` (pengelompokan per `assignees` sungguhan dari Vikunja, termasuk "BELUM ADA PIC").
   - Kasus gagal: token acak/salah → `401` (kode 5); id tugas tidak ada → `404` (kode 4); proyek
     tidak ada/ambigu → kode 2 dengan daftar proyek nyata.
4. Semua transkrip di atas ada di `examples/01`–`05` (data asli, dipotong bila perlu, tidak dikarang).

**Yang TIDAK diuji** (jujur, sesuai batas sandbox ini):
- Windows/macOS sungguhan (tidak ada mesin itu di sandbox).
- Docker (daemon diblokir kebijakan sandbox).
- OpenClaw Gateway sungguhan untuk `references/openclaw-jadwal.md` (hanya `scripts/uji_openclaw.sh`,
  uji muat/eligibility CLI, bukan uji pengiriman jadwal beneran — catat di `platform_teruji`
  sebagai `claude-code (simulasi agent)` + hasil `uji_openclaw.sh` bila lulus, BUKAN "openclaw
  teruji penuh").
- OpenID/SSO, MySQL/PostgreSQL (hanya SQLite, sesuai rekomendasi untuk tim kecil).

## 2. Bug yang ditemukan & diperbaiki selama uji pembuat sendiri
Dicatat apa adanya untuk transparansi proses (bukan berarti masih ada di v1.0.0 — semua sudah diperbaiki
sebelum status ini):
1. **Field draf `dari-teks` tidak sinkron dengan pembaca `tambah --batch`.** Draf sempat memakai
   nama field `pic_terdeteksi`/`tenggat_terdeteksi`, sedangkan `tambah --batch` membaca `ke`/
   `tenggat` — akibatnya tenggat & PIC hasil `dari-teks` **diam-diam diabaikan** saat dimasukkan ke
   Vikunja (ketahuan karena diuji ujung-ke-ujung terhadap server asli, tugas yang dibuat tidak
   punya `due_date`). Diperbaiki dengan menyamakan nama field + menambah field `proyek` kosong
   yang wajib diisi pengguna.
2. **Server tiruan di uji regresi tidak benar-benar menerapkan filter `due_date`,** sehingga uji
   `terlambat` bisa lolos "kebetulan" walau logikanya salah. Diperbaiki dengan menulis penerjemah
   kecil untuk bahasa filter Vikunja (`_terapkan_filter`) di server tiruan, termasuk semantik NULL
   untuk tugas tanpa tenggat (meniru perilaku Vikunja asli yang sudah dikonfirmasi lewat uji
   langsung).
3. **Uji tanggal "besok"/"seminggu lalu" berbasis jarak 1 hari terlalu rapuh** terhadap lamanya
   proses berjalan (batas hari nyata bisa terlewati di tengah sesi). Diperbaiki dengan memberi
   margin lebar (+3/−10 hari) pada data uji.
4. **Argumen umum (`--tz`, dll.) harus ditulis SETELAH nama perintah**, bukan sebelumnya (beda
   dengan asumsi awal yang meniru dokumentasi `dolibarr-usaha`) — SKILL.md & README ditulis sesuai
   perilaku nyata ini, bukan diklaim lebih fleksibel dari implementasinya.

## 3. Skor kualitas (usulan pembuat, bukan keputusan akhir)
**Belum diberi skor** — Tahap 6 CLAUDE.md mensyaratkan uji A/B tanpa-skill vs dengan-skill dan uji
banding pesaing oleh **penguji independen**, keduanya di luar cakupan tugas ini. Skor kualitas
dikosongkan di `catalog.csv` (`status=draft`) sampai penguji independen menyelesaikan itu.

## 4. PERLU REVIEW untuk pemilik
- Verifikasi GPG signature biner resmi belum selesai (§1.2 poin 1).
- Belum diuji platform asli manusia (OpenClaw/Codex/Claude Code/Cursor) sesuai `docs/uji-platform.md`.
- Kuirk "401 untuk token kurang izin, bukan 403" (didokumentasikan di `references/api-vikunja.md`)
  perlu dipantau bila Vikunja mengubah perilaku ini di rilis mendatang.
