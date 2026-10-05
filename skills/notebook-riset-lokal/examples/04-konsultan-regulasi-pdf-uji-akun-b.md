# 04 — Skenario normal 2: konsultan menyusun ringkasan regulasi dari PDF (tanpa nasihat hukum)

**Diuji terhadap Open Notebook 1.14.0 asli** (server sama seperti `03-...`). Konsultan ingin mengumpulkan cuplikan regulasi (dari PDF yang sudah ia salin isinya, karena skill sengaja tidak mengunggah file — lihat SKILL.md "Kapan TIDAK digunakan") dan minta ringkasan, TANPA meminta nasihat hukum.

## Langkah 1 — buat notebook & tambah cuplikan regulasi (tipe teks, mewakili isi PDF yang ditempel)
```
$ python3 scripts/notebook.py buat-notebook --nama "Regulasi Ketenagakerjaan 2026" --ya
```
```
$ python3 scripts/notebook.py tambah-sumber --notebook "Regulasi Ketenagakerjaan 2026" --tipe teks \
  --teks "Pasal 12: Upah lembur dihitung 1,5x upah per jam untuk jam pertama..." \
  --judul "Cuplikan PP Pengupahan" --ya
GALAT: 422: [{'type': 'missing', 'loc': ['body', 'type'], 'msg': 'Field required', 'input': None}]
```
❌ **Bug sama seperti `03-...`** (lihat `HASIL-UJI.md` Bug #1) — `tambah-sumber` gagal untuk tipe `teks` maupun `link`, jadi konsultan **tidak bisa** memasukkan cuplikan regulasi lewat skill ini sampai diperbaiki. Sumber ditambahkan manual lewat form-data agar langkah berikut bisa diuji.

## Langkah 2 — minta ringkasan (tanpa nasihat hukum)
```
$ python3 scripts/notebook.py ringkasan --notebook "Regulasi Ketenagakerjaan 2026"
GALAT: Belum ada model AI default yang diatur di Open Notebook (...). Buka http://127.0.0.1:8502 > Settings > Models...
```
(exit code 8) ✅ Sama seperti `tanya`, ditolak jelas karena tidak ada model AI di sandbox uji — bukan menebak isi regulasi.

**Catatan kepatuhan diverifikasi dari kode:** bila model AI tersedia, `cmd_ringkasan` (di `scripts/notebook.py`) selalu menempelkan catatan *"Ringkasan otomatis dari model AI, bukan pengganti membaca dokumen aslinya untuk keputusan penting (hukum/pajak/kontrak)."* — sesuai instruksi "tanpa nasihat hukum" di SKILL.md, dan konsisten dengan yang diklaim di `examples/01-...`. Penguji tidak bisa memverifikasi teks ringkasan sungguhan (perlu model AI), tapi struktur kode & disclaimer sudah benar.

## Langkah 3 — cari cepat tanpa AI (bekerja, dengan cacat minor)
```
$ python3 scripts/notebook.py cari --kueri "lembur" --notebook "Regulasi Ketenagakerjaan 2026"
{"kueri": "lembur", "jumlah": 1, "hasil": [{"judul": "Cuplikan PP Pengupahan", "tipe": "?", "cuplikan": ""}]}
```
⚠️ **Bug #2 (minor, tidak fatal):** jumlah hasil benar, tapi `tipe` selalu `"?"` dan `cuplikan` selalu kosong. Dikonfirmasi dari kode: respons asli `POST /api/search` (versi 1.14.0) hanya berisi field `id`, `parent_id`, `relevance`, `title` — TIDAK ada `parent_type`/`type`/`matches`/`content`/`name` yang dibaca `cmd_cari`. Jadi hasil pencarian tetap berguna (tahu dokumen mana yang cocok) tapi kehilangan info tipe & cuplikan kalimat yang cocok, yang justru paling berguna untuk konsultan memverifikasi cepat tanpa buka dokumen.

## Ringkasan skenario
Sama seperti skenario 03: terhambat di `tambah-sumber`. Disclaimer "bukan nasihat hukum" sudah benar di kode. `cari` berfungsi tapi kurang informatif akibat Bug #2.
