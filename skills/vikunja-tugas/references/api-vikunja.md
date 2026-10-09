# Referensi API Vikunja yang dipakai skill ini

Diverifikasi terhadap **Vikunja 2.6.0** (rilis 31 Agustus 2026) — kode sumber resmi
(`go-vikunja/vikunja`, commit `dfcae65b355fde612f546796ed722fa1742c305e`, dibaca 2026-09-26) DAN
dengan benar-benar **menjalankan binary resmi** (checksum SHA-256 cocok) di 127.0.0.1, membuat
proyek/tugas/token sungguhan, dan mencoba semua endpoint di bawah. Dokumentasi resmi ada di
`https://vikunja.io/docs/api-documentation/` dan Swagger interaktif di `/api/v1/docs` instance
Anda sendiri; halaman ini hanya bagian yang benar-benar dipakai `scripts/vikunja.py`, ditulis
ulang dengan kata-kata sendiri (bukan kutipan dari dokumentasi Vikunja).

## Autentikasi
- Header: `Authorization: Bearer tk_xxxxxxxxxxxxxxxxxxxxxxxx` (token API, awalan `tk_`, dibuat manual di Settings > API Tokens Vikunja — lihat `references/panduan-vikunja.md` §6).
- Vikunja juga mendukung login user/sandi (`POST /api/v1/login` → JWT) — **tidak dipakai** skill ini; skill hanya memakai token API berskop, tidak pernah menyimpan sandi akun.
- **Kuirk penting (diuji langsung, tidak didokumentasikan resmi):** token yang salah/kedaluwarsa DAN token yang sah tapi **kurang izin** untuk aksi tertentu **sama-sama membalas `401`** dengan pesan generik `"missing, malformed, expired or otherwise invalid token provided"` — bukan `403` untuk kasus kedua. `scripts/vikunja.py` menyebut kedua kemungkinan di setiap pesan galat 401.

## Skema izin token (dari `GET /api/v1/routes`, sumber kebenaran resmi)
Body `PUT /api/v1/tokens`: `{"title": "...", "expires_at": "2027-...Z", "permissions": {"<grup>": ["<izin>", ...]}}`.

| Grup | Izin yang dipakai skill | Dipakai untuk perintah |
|---|---|---|
| `projects` | `read_all`, `read_one` | `daftar-proyek`, `hari-ini`, `terlambat`, `minggu-ini`, `cari`, `ringkasan`, `tambah` (cari proyek), `cek` |
| `projects` | `projectusers` | `tambah --ke <username>` (cari id pengguna dari nama) |
| `tasks` | `read_all`, `read_one` | semua perintah baca |
| `tasks` | `create` | `tambah` |
| `tasks` | `update` | `selesai` |
| `tasks_assignees` | `create`, `read_all` | `tambah --ke <username>` |

Token respons: `{"id":1,"title":"...","token":"tk_...","permissions":{...},"expires_at":"...","owner_id":1}` — field `token` (teks asli) hanya muncul **sekali**, saat dibuat.

## Endpoint

| Aksi | Method & path | Catatan |
|---|---|---|
| Info server | `GET /api/v1/info` | Publik, tanpa token; dipakai `cek` untuk versi server |
| Daftar proyek | `GET /api/v1/projects?page=&per_page=` | Proyek dengan `id <= 0` (mis. `-2 "My Open Tasks"`) adalah proyek **semu**, dilewati skill |
| Tugas 1 proyek | `GET /api/v1/projects/{id}/tasks?filter=&s=&page=&per_page=` | |
| Tugas SEMUA proyek | `GET /api/v1/tasks?filter=&s=&page=&per_page=` | Dipakai bila `--proyek` tidak disebut. **Bukan** `/tasks/all` — endpoint itu tidak ada di v1 |
| 1 tugas | `GET /api/v1/tasks/{id}` | 404 bila tidak ada/tidak berhak |
| Buat tugas | `PUT /api/v1/projects/{id}/tasks` | Body: `{"title":..., "due_date":"RFC3339 UTC 'Z'", "priority":0-5, "description":...}` |
| Ubah tugas (tandai selesai) | `POST /api/v1/tasks/{id}` | Body `{"done":true}`; v1 memakai **POST untuk update**, bukan PATCH/PUT |
| Cari pengguna di proyek | `GET /api/v1/projects/{id}/projectusers?s=<kata>` | Perlu izin `projects: projectusers`, bukan `read_all` |
| Tugaskan ke anggota | `PUT /api/v1/tasks/{id}/assignees` | Body `{"user_id": <angka>}` — **wajib id angka**, bukan username |
| Daftar izin token | `GET /api/v1/routes` | Sumber kebenaran nama grup/izin (dipakai untuk menyusun tabel di atas, bukan dipanggil skill saat jalan) |

## Bahasa filter (`filter=`)
Ekspresi bebas mirip SQL, digabung `&&`/`||`, field umum: `due_date`, `done`, `priority`,
`project_id`. Skill ini **selalu mengirim tanggal absolut** yang sudah dihitung sendiri di Python
(bukan `now` milik server) supaya tidak tergantung zona waktu server, contoh:
```
due_date >= 2026-09-26T00:00:00Z && due_date < 2026-09-27T00:00:00Z && done = false
```
Tugas dengan `due_date` kosong **tidak pernah muncul** pada perbandingan `due_date` (diperlakukan seperti NULL di SQL) — diuji langsung terhadap server asli.

## Pagination
Header respons `X-Pagination-Total-Pages` menyebut jumlah halaman; skill mengambil semua halaman (`per_page=50`, maksimal 20 halaman/1000 baris per perintah, cukup untuk tim kecil).

## Format tanggal
Semua field tanggal (`due_date`, `expires_at`, dll.) adalah RFC3339 UTC berakhiran `Z`
(`2026-09-26T10:00:00Z`). Skill mengonversi dari/ke waktu lokal (`--tz`, default WIB) di sisi
Python; Vikunja sendiri menyimpan dan membalas selalu dalam UTC.

## Yang TIDAK dipakai skill ini (di luar cakupan v1.0.0)
Sub-tugas (`related_tasks`), tugas berulang (`repeat_after`/`repeat_mode`), label, lampiran,
tampilan Kanban/bucket, komentar, reaksi, tim (teams), berbagi proyek, webhook, API v2
(`/api/v2`, dipakai untuk fitur baru seperti OAuth/MCP — belum stabil untuk semua operasi tugas
saat riset ditulis). Semua ini bisa dikerjakan langsung di layar Vikunja.
