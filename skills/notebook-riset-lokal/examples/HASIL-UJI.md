# HASIL UJI — notebook-riset-lokal v1.0.0 (penguji independen, Akun B)

Tanggal uji: 2026-09-26. Penguji tidak menulis kode skill ini; hanya membaca folder skill + `docs/panduan-open-notebook.md` dan menjalankannya dari luar.

## 1. Lingkungan uji — Open Notebook ASLI berhasil dijalankan tanpa Docker
Docker tidak tersedia di sandbox ini juga, tapi **berhasil dijalankan langsung dari kode sumber** (bukan server tiruan) di scratchpad `/tmp/.../rt-notebook/`:

1. `git clone https://github.com/lfnovo/open-notebook.git`, `git checkout 3127f14` → persis commit yang diklaim `ATTRIBUTION.md` (`version` di `pyproject.toml` = `1.14.0`). **Klaim commit/versi di ATTRIBUTION.md TERVERIFIKASI BENAR.**
2. SurrealDB: diunduh langsung dari URL rilis resmi GitHub (`github.com/surrealdb/surrealdb/releases/download/v2.0.0/surreal-v2.0.0.linux-amd64.tgz`, redirect ke `release-assets.githubusercontent.com` atas nama GitHub, diunduh lewat TLS terverifikasi). **Verifikasi checksum: SEBAGIAN.** SHA-256 file diunduh dihitung (`7f1aa547e4ea808f7781737766715ed6f4082788598b5260f39085777862c566`), tapi tidak ada aset `.sha256`/checksums resmi di rilis tsb., dan `install.surrealdb.com` (skrip pasang resmi SurrealDB) sendiri **tidak melakukan verifikasi checksum** — jadi tidak ada sumber independen kedua untuk dicocokkan di sandbox ini (API GitHub diblokir kebijakan sesi). Binari diuji jalan (`surreal version` → `2.0.0`) dan diunduh dari domain resmi GitHub releases via TLS, bukan dari mirror pihak ketiga — risiko dinilai rendah tapi **bukan verifikasi checksum penuh**; catat sebagai keterbatasan sesi ini, bukan alasan menolak skill.
3. `uv sync --no-dev` di clone tsb. → semua dependensi Python terpasang tanpa error.
4. Dijalankan (bukan Docker): `surreal start --bind 127.0.0.1:8000 ...` (DB), `run_api.py` dengan `API_HOST=127.0.0.1 API_PORT=5055` (API), dan `surreal-commands-worker` (pemroses sumber latar belakang — dibutuhkan agar `tambah-sumber`/`cari` benar-benar mengindeks; di Docker resmi ini jalan otomatis lewat `supervisord.conf`, di luar Docker harus dijalankan manual, hal ini **tidak disebut** di `docs/panduan-open-notebook.md` tapi tidak relevan untuk pembeli karena mereka memang memakai Docker/image resmi yang sudah menyertakan worker).
5. Migrasi database (25 migrasi) berjalan otomatis, `GET /health` → `{"status":"healthy"}`, semua koneksi diuji hanya ke `127.0.0.1`.

Semua server dimatikan (`kill -9`) di akhir sesi; diverifikasi `curl` ke `127.0.0.1:5055` dan `:8000` sudah gagal konek.

Tidak ada model AI (Ollama/API key) dipasang — sesuai instruksi tugas, ini dipakai untuk menguji perilaku "model AI belum diatur" apa adanya.

## 2. Temuan BUG (terhadap server asli — bukan asumsi)

### Bug #1 — KRITIS: `tambah-sumber` gagal 100% (tipe `link` maupun `teks`)
`scripts/notebook.py` fungsi `cmd_tambah_sumber` mengirim `POST /api/sources` dengan `Content-Type: application/json`. Endpoint asli versi 1.14.0 (`api/routers/sources.py`, dependency `parse_source_form_data`) mendeklarasikan semua field lewat `Form(...)` — artinya endpoint **hanya** menerima `multipart/form-data` (atau minimal `application/x-www-form-urlencoded`), bukan JSON. Akibatnya server selalu membalas:
```
422: [{'type': 'missing', 'loc': ['body', 'type'], 'msg': 'Field required', 'input': None}]
```
Dibuktikan dengan permintaan form-data manual (`curl -F ...`) yang **berhasil** ke server yang sama — jadi ini murni bug format request di skill, bukan masalah server/konfigurasi. Ini fitur paling inti ("kumpulkan dokumen ke satu tempat") dan **gagal total** untuk kedua tipe sumber yang didukung. Lihat `examples/03-...`, `04-...`, `05-...`.

**Kemungkinan penyebab bug lolos sebelumnya:** `tests/uji_regresi.py` (server tiruan) mengimplementasikan `/api/sources` untuk menerima JSON biasa (lihat `Handler.do_POST` di `tests/uji_regresi.py`), sehingga 30/30 uji regresi tetap LULUS (diverifikasi ulang di sesi ini) walau tidak mencerminkan perilaku server asli. Ini celah antara "verifikasi baca kode sumber" dan kenyataan endpoint FastAPI dengan `Depends(parse_source_form_data)`.

**Rekomendasi perbaikan:** ubah `panggil()`/`cmd_tambah_sumber` agar pada `tambah-sumber` mengirim `multipart/form-data` (encode manual dengan `urllib` — bisa pakai `email.mime.multipart` atau boundary manual karena tanpa paket luar), lalu perbarui `tests/uji_regresi.py` agar mock server ikut menuntut form-data (agar regresi ini tertangkap otomatis ke depannya).

### Bug #2 — SEDANG: `cari` kehilangan info tipe & cuplikan
`POST /api/search` (teks) versi 1.14.0 mengembalikan objek hasil dengan field `id`, `parent_id`, `relevance`, `title` saja — **tidak ada** `parent_type`, `type`, `matches`, `content`, atau `name`. `cmd_cari` membaca field-field yang tidak ada tsb., sehingga `tipe` selalu `"?"` dan `cuplikan` selalu `""`. Jumlah hasil & judul tetap benar (tidak fatal), tapi fitur "cepat verifikasi tanpa buka dokumen" jadi kurang berguna. Lihat `examples/04-...`.

**Rekomendasi perbaikan:** sesuaikan `cmd_cari` dengan field asli (`id`/`parent_id`/`relevance`/`title`); untuk cuplikan sebenarnya, mungkin perlu endpoint lain atau memang tidak tersedia di `text_search` — perlu dicek lagi ke pembuat Open Notebook / kode `open_notebook.domain.notebook.text_search`.

### Yang TERVERIFIKASI BENAR terhadap server asli (tidak ada bug)
- `cek`, `daftar-notebook`, `buat-notebook` (pratinjau & `--ya`), `daftar-sumber` — field & alur persis sesuai dokumentasi.
- `tanya`/`ringkasan` menolak dengan pesan "Belum ada model AI default..." (exit 8) persis seperti didokumentasikan, memanggil `GET /api/models/defaults` asli.
- Validasi `--url` hanya `127.0.0.1`/`localhost`/`::1` (exit 2) — diuji dengan alamat TEST-NET nyata (`192.0.2.10`), bukan cuma placeholder.
- Input tidak lengkap (`--tipe teks` tanpa `--teks`) & tipe `file` ditolak dengan pesan jelas (exit 2 / 8), tanpa pernah menghubungi server.
- Tidak ada perintah hapus di skill (diverifikasi: `DELETE /api/notebooks/{id}` memang ada di API asli, tapi skill sengaja tidak memanggilnya).
- Audit keamanan kode: tidak ada `eval`/`exec`/`subprocess`/`os.system`; satu-satunya titik panggilan HTTP (`panggil()`) selalu lewat `periksa_url()`; kata sandi tidak pernah dicetak utuh (`tampilkan_kunci_tersamar`); tidak ada pengiriman data ke domain selain `args.url`.

## 3. Verifikasi klaim `docs/panduan-open-notebook.md`
- **Port default & docker-compose resmi:** DIVERIFIKASI BENAR. `docker-compose.yml` resmi di commit `3127f14` memang menulis `ports: ["8502:8502", "5055:5055"]` **tanpa** `127.0.0.1:` untuk service `open_notebook` (dibaca langsung dari file repo asli) — artinya bawaan resmi membuka kedua port ke semua antarmuka jaringan, persis seperti diklaim panduan bagian 4. Koreksi panduan (menambahkan `127.0.0.1:`) untuk kedua port **valid dan perlu**. Menariknya, service `surrealdb` **sudah** dibatasi `127.0.0.1:8000:8000` di versi resmi ini (kemungkinan diperbaiki upstream setelah panduan Komunitech ditulis) — tidak mengubah kesimpulan, hanya catatan bahwa upstream sudah membenahi separuh masalah.
- **Nama variabel `OPEN_NOTEBOOK_PASSWORD` → header `Authorization: Bearer`:** DIVERIFIKASI BENAR dari `api/auth.py` (`PasswordAuthMiddleware`, `get_secret_from_env("OPEN_NOTEBOOK_PASSWORD")`, cek `Bearer <sandi>`).
- **`OPEN_NOTEBOOK_ENCRYPTION_KEY` wajib:** dikonfirmasi lewat run nyata — server berjalan normal dengan env ini diisi.
- **RAM (≥8 GB, ≥16 GB dengan model lokal):** TIDAK BISA diverifikasi presisi (di luar cakupan: butuh menjalankan Ollama + model lokal sungguhan, tidak dilakukan sesi ini). Sebagai data pendukung: SurrealDB+API+worker (tanpa Docker, tanpa LLM, tanpa frontend Next.js, tanpa Docling/Crawl4AI) memakai total ±520 MB RSS saat idle di uji ini — jauh di bawah 8 GB, jadi klaim minimal 8 GB (yang mencakup overhead Docker Desktop + frontend + image penuh) terdengar **jujur/konservatif**, bukan berlebihan. Klaim 16 GB untuk model lokal sejalan dengan pengetahuan umum kebutuhan RAM model bahasa 7–8B — masuk akal, tidak diverifikasi presisi.
- **Kebutuhan Docker jujur:** BENAR — Open Notebook memang **hanya** didistribusikan resmi lewat image Docker (`lfnovo/open_notebook`), tidak ada installer/`pip install` resmi untuk paket lengkap (frontend+API+worker) sesuai `Dockerfile`/`README.md` resminya. Panduan tidak melebih-lebihkan atau meremehkan langkah ini.

## 4. Lima skenario (lihat file terpisah)
| # | Skenario | File | Hasil |
|---|---|---|---|
| 1 | Klinik: simpan brosur/SOP lalu tanya | `03-klinik-brosur-sop-uji-akun-b.md` | Terhambat Bug #1; sisanya benar |
| 2 | Konsultan: ringkasan regulasi, tanpa nasihat hukum | `04-konsultan-regulasi-pdf-uji-akun-b.md` | Terhambat Bug #1; disclaimer hukum benar di kode; `cari` kena Bug #2 |
| 3 | Toko: bandingkan 3 katalog supplier | `05-toko-katalog-supplier-uji-akun-b.md` | Terhambat Bug #1 (tipe `link`) |
| 4 | Input tidak lengkap | `06-input-tidak-lengkap-uji-akun-b.md` | ✅ Benar |
| 5 | Luar cakupan (buka ke internet / hapus semua notebook) | `07-luar-cakupan-uji-akun-b.md` | ✅ Benar (keduanya ditolak sesuai desain) |

Uji A/B: `00-pembanding-tanpa-skill.md`. Uji banding pesaing: `00-banding-pesaing.md` (tidak ditemukan skill Open Notebook lokal publik; dibandingkan dengan skill konektor NotebookLM cloud + produk NotebookLM asli — konsep skill kita unggul di privasi, implementasi saat ini kalah karena Bug #1).

## 5. Tes bawaan
- `python3 tests/uji_regresi.py` → **30/30 LULUS** (server tiruan; tidak mendeteksi Bug #1/#2 karena mock tidak meniru persis kontrak form-data/field pencarian asli — lihat rekomendasi di atas).
- `python3 scripts/validate.py --skill notebook-riset-lokal` → **LULUS** (`✅ 1 skill valid, 90 baris katalog sesuai.`).
- `uji_openclaw.sh` **tidak dijalankan** sesuai instruksi tugas.

## 6. Skor kualitas: **3/10 — REVISI, JANGAN RILIS**

**Alasan:** pedoman kurasi Komunitech tahap 6.7: "Di bawah 7 → revisi, jangan rilis." Skor rendah murni karena **Bug #1** — fitur inti "kumpulkan PDF/artikel/notulen/katalog ke satu notebook" (alasan utama skill ini dibuat, disebutkan di kalimat pertama `description` SKILL.md) **gagal 100%** terhadap server Open Notebook 1.14.0 asli, untuk kedua tipe sumber yang didukung (`link` dan `teks`). Tanpa perbaikan, pembeli yang mengikuti alur di README/SKILL.md persis akan selalu mendapat galat `422` di langkah paling awal dan tidak bisa memakai skill sama sekali untuk kasus penggunaan utamanya.

**Yang sudah bagus (jangan dibuang saat revisi):** struktur pratinjau→`--ya`, penanganan galat awam (401/404/localhost-only/timeout/model-AI-kosong), audit keamanan bersih, dokumentasi jujur soal status "belum diverifikasi", dan `docs/panduan-open-notebook.md` yang klaimnya terbukti akurat terhadap kode sumber asli (port, env var, kebutuhan Docker). Setelah Bug #1 (dan idealnya Bug #2) diperbaiki serta diuji ulang terhadap server asli (bukan cuma server tiruan), skill ini punya dasar kuat untuk naik ke skor lulus.

## 7. PERLU REVIEW / tindak lanjut
- **WAJIB sebelum status naik ke `lulus`:** perbaiki `cmd_tambah_sumber` (kirim multipart/form-data), perbaiki `tests/uji_regresi.py` agar mock server menuntut form-data (supaya regresi ini terdeteksi otomatis ke depannya), lalu uji ulang oleh penguji independen terhadap server Open Notebook asli (bukan hanya server tiruan) — sesuai Tahap 6.7.
- **Disarankan:** perbaiki `cmd_cari` agar sesuai field asli (`id`/`parent_id`/`relevance`/`title`), atau dokumentasikan keterbatasan "tanpa cuplikan" bila memang tidak tersedia dari API.
- **Catatan kecil, tidak menghalangi:** verifikasi checksum SurrealDB di sesi ini hanya sebagian (lihat bagian 1) karena API GitHub diblokir kebijakan sesi — untuk rilis produksi, verifikasi checksum sebaiknya diulang di lingkungan dengan akses penuh, atau dicatat sebagai keterbatasan bawaan proyek upstream (SurrealDB sendiri tidak menerbitkan checksum resmi per rilis).

---

## Uji ulang independen v1.0.1 (Akun B, 2026-09-26)

Penguji independen kedua (bukan pembuat, bukan penguji v1.0.0). Lingkungan disiapkan dari nol di scratchpad terpisah (`rt-notebook2/`): clone `lfnovo/open-notebook` commit `3127f14` (versi `1.14.0`, sesuai klaim), SurrealDB v2.0.0 binary resmi, `uv sync`, API + worker latar belakang, semua hanya di `127.0.0.1`. Detail penuh: `08-uji-ulang-v101-akun-b.md`.

**Bug #1 (tambah-sumber 422) — DIPERBAIKI, TERVERIFIKASI.** `tambah-sumber --tipe link` dan `--tipe teks` (termasuk teks panjang 16.800 karakter dan teks berisi karakter Indonesia + emoji) berhasil `200`/`ditambahkan: true` terhadap server 1.14.0 asli, dan diproses sampai `status: completed`. Total 7 sumber ditambahkan lintas 3 skenario nyata (klinik, konsultan, toko) tanpa satu pun galat `422`.

**Bug #2 (cari kehilangan info) — DIPERBAIKI, TERVERIFIKASI.** `cari` mengembalikan `judul`/`id_dokumen`/`relevansi` yang benar dan akurat terhadap isi sumber; keterbatasan "tanpa cuplikan kalimat" didokumentasikan jujur lewat field `catatan`, sesuai API asli.

**Perintah lain dikonfirmasi ulang benar terhadap server asli:** `cek`, `buat-notebook`, `daftar-notebook`, `daftar-sumber`, `tanya`/`ringkasan` (pesan "model AI belum diatur" jelas, exit 8), tipe `file` ditolak (exit 8), tipe tak dikenal ditolak argparse (exit 2), URL non-localhost ditolak tanpa hubungi server (exit 2), server mati (exit 4), timeout (exit 4), **password salah → 401 Unauthorized (exit 5) baru diverifikasi kali ini** (uji v1.0.0 belum sempat menguji auth aktif), password benar → berhasil dengan sandi tersamar, peringatan `chmod 600` pada file kunci longgar. `podcast-mulai` dengan profil belum dibuat → galat 500 generik yang tetap tertangani (exit 4, tidak crash) tapi kurang informatif — dicatat sebagai perbaikan kecil, bukan penghalang kelulusan.

**Tidak ada data terhapus:** tidak ada subperintah hapus di skill; 3 notebook & 7 sumber yang dibuat sesi ini tetap utuh sampai akhir. Semua server dimatikan di akhir sesi; port `5055` dan `8000` dikonfirmasi bebas (`curl` gagal konek, kode `000`).

**Tes bawaan:** `python3 tests/uji_regresi.py` → 40/40 LULUS. `python3 scripts/validate.py --skill notebook-riset-lokal` → LULUS.

### Skor kualitas: **9/10 — LULUS**
Kedua bug yang menahan skor v1.0.0 di 3/10 terbukti diperbaiki dan diverifikasi ulang terhadap server Open Notebook 1.14.0 **asli** (bukan server tiruan), lintas 3 skenario nyata sekaligus uji auth (401) yang belum tercakup di uji sebelumnya. Tidak ada bug baru ditemukan pada permukaan yang diuji. Satu poin ditahan karena: (a) pesan galat `podcast-mulai` untuk profil belum dibuat masih generik ("500 internal"), (b) belum ada uji platform asli (OpenClaw/Codex/Cursor) — sesuai catatan `SKILL.md` sendiri, dan (c) verifikasi checksum SurrealDB tetap hanya sebagian (keterbatasan bawaan upstream, bukan skill). Direkomendasikan lanjut ke Tahap 6.10 (uji platform asli) sebelum naik ke `rilis`.

---

## Uji ulang v1.0.2 (2026-09-28)

Penguji independen, scratchpad terpisah, tidak mengubah `scripts/`/`SKILL.md`. Server Open Notebook
asli tidak dijalankan ulang kali ini; dipakai server HTTP tiruan minimal (Python `http.server` standar)
yang membalas `404`/`422` persis pada `POST /api/podcasts/generate`, untuk menguji jalur pesan galat
secara terisolasi dan berulang.

- **404** (`{"detail": "Episode profile not found"}`): `podcast-mulai --ya` menghasilkan pesan galat
  Indonesia spesifik — "Gagal mulai podcast: profil episode '...' atau profil pembicara '...'
  kemungkinan belum dibuat di server ini (...) — buka http://127.0.0.1:8502 ... Settings > Podcasts,
  buat dulu 'Episode Profile' dan 'Speaker Profile' ..." — **bukan lagi pesan 404 generik "cek id
  notebook/sumber"** yang membingungkan pengguna. Exit kode 2 (K_INPUT), sesuai dokumentasi.
- **422** (`detail` berisi list error validasi Pydantic): pesan yang sama muncul (jalur deteksi
  `e.kode == K_INPUT and ("profile" in pesan.lower() or "404" in pesan or "422" in pesan)` cocok
  lewat literal "422" di pesan). Sedikit catatan gaya bahasa (rendah): teks gabungan menyebut baik
  "profil kemungkinan belum dibuat" maupun "ini kemungkinan bug skill, laporkan ke Komunitech" dalam
  satu kalimat — sedikit membingungkan urutan sebab, tapi tidak salah secara faktual dan tetap
  mengarahkan pengguna ke langkah yang benar (buat profil dulu).
- `tests/uji_regresi.py`: **41/41 lulus**, tanpa regresi.

**Skor: 9/10.** Perbaikan pesan galat `podcast-mulai` di v1.0.2 terverifikasi berfungsi untuk kedua
kode status (404 & 422) yang dilaporkan sebagai generik di uji K8 sebelumnya. Satu poin ditahan untuk
catatan gaya bahasa minor pada kasus 422 di atas — kosmetik, tidak menghalangi status `lulus`.
