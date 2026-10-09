# Uji ulang independen — notebook-riset-lokal v1.0.1 (Akun B, penguji independen kedua, 2026-09-26)

Penguji ini **bukan** pembuat skill dan **bukan** penguji v1.0.0. Hanya membaca folder skill (`SKILL.md`, `scripts/notebook.py`, `docs/panduan-open-notebook.md`) lalu menjalankannya dari luar terhadap Open Notebook 1.14.0 **asli** (bukan server tiruan).

## 1. Lingkungan
Dijalankan tanpa Docker di scratchpad `rt-notebook2/`:
- `git clone` lfnovo/open-notebook, `git checkout 3127f14` → `pyproject.toml` version `1.14.0`. Persis klaim `SKILL.md`/`ATTRIBUTION.md`.
- SurrealDB v2.0.0 binary resmi diunduh dari rilis GitHub resmi, `surreal start --bind 127.0.0.1:8000 ... rocksdb:./surrealdata/data.db`.
- `uv sync --no-dev` → semua dependensi terpasang tanpa error.
- API (`run_api.py`, `API_HOST=127.0.0.1 API_PORT=5055`, `OPEN_NOTEBOOK_ENCRYPTION_KEY` diisi) → `GET /health` → `{"status":"healthy"}`.
- Worker latar belakang (`surreal-commands-worker --import-modules commands --max-tasks 5`) dijalankan terpisah, wajib agar `tambah-sumber` benar-benar diindeks (sama seperti temuan penguji v1.0.0).
- Semua koneksi hanya ke `127.0.0.1`. Semua proses dimatikan di akhir sesi (`kill -9` pada PID surreal/worker/API); diverifikasi `curl --max-time 2` ke port `5055` dan `8000` sama-sama gagal konek (kode `000`) setelahnya — port bebas.

## 2. Verifikasi perbaikan Bug #1 (tambah-sumber multipart) — **BENAR, LULUS**
Dites terhadap server asli:
- `tambah-sumber --tipe link` (artikel Wikipedia) → `200`, `ditambahkan: true`, diproses latar belakang sampai `status: completed` (dikonfirmasi lewat `daftar-sumber`).
- `tambah-sumber --tipe teks` berisi bahasa Indonesia + emoji (`🏥`, `🙏`) dan referensi UU No. 27/2022 PDP → berhasil, judul & isi tersimpan benar (tidak ada masalah encoding UTF-8).
- Teks panjang (16.800 karakter, ~200 pengulangan kalimat regulasi UMKM) → berhasil, `status: completed`.
- Total 3 skenario nyata (klinik: SOP+brosur, konsultan: regulasi ketenagakerjaan, toko: 3 katalog supplier dengan emoji `🚚`) — **7 sumber**, semua `ditambahkan: true` lalu `status: completed`. Tidak ada satupun galat `422`. Bug #1 **terbukti diperbaiki**.

## 3. Verifikasi perbaikan Bug #2 (cari) — **BENAR, LULUS**
`cari --kueri "pasien"` dan `--kueri "katun"` terhadap sumber yang sudah ditambahkan → hasil berisi `judul`, `id_dokumen`, `relevansi` yang benar dan sesuai isi sumber (mis. 3 supplier "katun" ditemukan dengan relevansi 0.425). Field `catatan` menjelaskan jujur bahwa API tidak menyediakan cuplikan kalimat — sesuai keterbatasan asli `POST /api/search`. Kata kunci tidak cocok → `jumlah: 0`, tanpa galat. Bug #2 **terbukti diperbaiki**.

## 4. Perintah lain (diverifikasi ulang terhadap server asli)
| Perintah | Hasil |
|---|---|
| `cek` | Benar: status server, `auth_aktif`, jumlah notebook |
| `buat-notebook` (3x, tanpa & dengan auth) | Benar |
| `daftar-notebook` | Benar, 3 notebook & jumlah sumber akurat setelah semua skenario |
| `daftar-sumber` | Benar, `status: completed` untuk semua 7 sumber |
| `tambah-sumber --tipe file` | Ditolak dengan pesan jelas (exit 8), tanpa hubungi server — sesuai desain |
| `tambah-sumber --tipe` tidak dikenal (`youtube`) | Ditolak oleh argparse sebelum kirim (exit 2) — luar cakupan ditangani benar |
| `tanya` / `ringkasan` tanpa model AI | "GALAT: Belum ada model AI default..." (exit 8) — sesuai dokumentasi, dikonfirmasi lewat `GET /api/models/defaults` asli |
| `podcast-mulai` (profil/pembicara tak ada) | `GALAT: 500 ...Failed to submit podcast generation job` (exit 4) — server menolak wajar karena profil belum dibuat di layar Open Notebook, sesuai Batasan yang didokumentasikan |
| URL non-localhost (`192.0.2.10`) | Ditolak (exit 2), **tanpa** menghubungi server |
| Server mati (port tak dipakai) | "Connection refused", saran jelas (exit 4) |
| Timeout sangat kecil (`--timeout 0.0001`) | Pesan timeout jelas (exit 4) |
| Password salah (`--kunci-file` isi salah, `OPEN_NOTEBOOK_PASSWORD` diaktifkan di server) | **401 Unauthorized**, pesan jelas (exit 5) |
| Password benar | Berhasil, `kata_sandi` ditampilkan tersamar (`sa****23`) |
| File kunci bisa dibaca user lain | PERINGATAN `chmod 600` muncul — sesuai desain keamanan |

## 5. Tidak ada penghapusan data
`--help` mengonfirmasi tidak ada subperintah hapus (`simpan-kunci, cek, daftar-notebook, buat-notebook, tambah-sumber, daftar-sumber, tanya, ringkasan, cari, podcast-mulai, podcast-status`). Setelah seluruh sesi uji: 3 notebook, 7 sumber, semuanya utuh (dikonfirmasi `daftar-notebook` terakhir) — tidak ada perintah yang menghapus apa pun.

## 6. Tes bawaan & validasi
- `python3 tests/uji_regresi.py` → **LULUS: 40 GAGAL: 0** (mock kini menuntut multipart & skema pencarian asli, sesuai klaim `SKILL.md`).
- `python3 scripts/validate.py --skill notebook-riset-lokal` → **LULUS** (`✅ 1 skill valid, 91 baris katalog sesuai.`).
- `uji_openclaw.sh` **tidak dijalankan**, sesuai instruksi tugas.

## 7. Kesimpulan
Kedua bug kritis/sedang dari uji v1.0.0 (skor 3/10) **terbukti diperbaiki dan diverifikasi ulang terhadap server Open Notebook 1.14.0 asli**, bukan hanya server tiruan. Ketiga skenario nyata (klinik, konsultan, toko) berjalan mulus dari `buat-notebook` sampai `daftar-sumber`/`cari`. Penanganan galat (401, non-localhost, timeout, server mati, model AI belum diatur, tipe file, input tidak lengkap) semuanya benar dan pesan awam jelas. Tidak ditemukan bug baru pada permukaan yang diuji sesi ini. Skor & alasan lengkap: lihat bagian baru di `HASIL-UJI.md`.

**Catatan (bukan bug, untuk revisi berikutnya):** `podcast-mulai` dengan profil/pembicara yang belum dibuat mengembalikan galat generik "500 ...internal" alih-alih pesan yang menyebut "profil podcast belum dibuat di Settings" — masih ditangani (exit 4, tidak crash), tapi pesan bisa lebih membantu pembeli awam. Ini sesuai Batasan yang sudah didokumentasikan (profil harus dibuat manual di layar Open Notebook), jadi tidak mengubah skor kelulusan.
