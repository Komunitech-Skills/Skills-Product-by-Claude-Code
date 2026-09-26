# 03 — Skenario normal 1: pemilik klinik menyimpan brosur & SOP lalu bertanya

**Diuji oleh penguji independen (Akun B) terhadap Open Notebook 1.14.0 ASLI**, dijalankan tanpa Docker di scratchpad (SurrealDB v2.0.0 biner resmi + `uv sync` repo `lfnovo/open-notebook` commit `3127f14`), hanya di `127.0.0.1`. Bukan server tiruan. Lihat `HASIL-UJI.md` untuk cara menjalankan.

## Langkah 1 — cek koneksi
```
$ python3 scripts/notebook.py cek
{
  "url": "http://127.0.0.1:5055",
  "auth_aktif": false,
  "jumlah_notebook": 0,
  "kata_sandi": "(tidak dipakai)",
  "pesan": "Open Notebook bisa dihubungi dan siap dipakai."
}
```
✅ Sesuai SKILL.md.

## Langkah 2 — buat notebook
```
$ python3 scripts/notebook.py buat-notebook --nama "Brosur & SOP Klinik" --deskripsi "Materi edukasi pasien & SOP internal" --ya
{"dibuat": true, "id": "notebook:u88lrelmn9bt9escjshv", "nama": "Brosur & SOP Klinik"}
```
✅ Berhasil, field `dibuat`/`id`/`nama` sesuai dokumentasi.

## Langkah 3 — tambah SOP (tipe teks) — ❌ GAGAL (bug nyata)
```
$ python3 scripts/notebook.py tambah-sumber --notebook "Brosur & SOP Klinik" --tipe teks \
  --teks "SOP Pendaftaran Pasien Baru: 1) Isi formulir data diri. 2) Tunjukkan KTP/BPJS. 3) Ambil nomor antrian." \
  --judul "SOP Pendaftaran" --ya
GALAT: 422: [{'type': 'missing', 'loc': ['body', 'type'], 'msg': 'Field required', 'input': None}]
```
**Penyebab (dikonfirmasi dengan membaca `api/routers/sources.py` versi 1.14.0):** endpoint `POST /api/sources` memakai dependency `parse_source_form_data`, yang mendeklarasikan semua field dengan `Form(...)` (FastAPI multipart/form-data), **bukan** model Pydantic biasa lewat body JSON. Skill mengirim `Content-Type: application/json`, sehingga FastAPI tidak menemukan field `type` sama sekali dan selalu membalas `422`.

**Dibuktikan dengan permintaan form-data manual (bukan lewat skill):**
```
$ curl -X POST http://127.0.0.1:5055/api/sources \
  -F "type=text" -F "content=..." -F "title=SOP Pendaftaran" \
  -F 'notebooks=["notebook:u88lrelmn9bt9escjshv"]' -F "async_processing=true"
{"id":"source:rsxfiw4zr37x3r9bxam3","title":"SOP Pendaftaran", ..., "status":"new", ...}
```
→ 200 OK. Ini membuktikan bug ada di `cmd_tambah_sumber` (mengirim JSON, seharusnya multipart form), bukan di pemahaman endpoint secara umum.

**Dampak:** pemilik klinik di skenario ini **tidak bisa** menyimpan brosur/SOP lewat perintah `tambah-sumber` sama sekali (tipe `teks` maupun `link`, lihat contoh `05-...`) sampai bug ini diperbaiki. Ini fitur inti skill — harus direvisi sebelum rilis.

## Langkah 4 — daftar sumber (setelah ditambah manual lewat form-data, agar pengujian berikutnya bisa lanjut)
```
$ python3 scripts/notebook.py daftar-sumber --notebook "Brosur & SOP Klinik"
{"notebook_id": "notebook:u88lrelmn9bt9escjshv", "jumlah": 1,
 "sumber": [{"id": "source:rsxfiw4zr37x3r9bxam3", "judul": "SOP Pendaftaran", "status": "completed", "jumlah_bagian_terindeks": 0, "jumlah_insight": 0}]}
```
✅ `daftar-sumber` sendiri bekerja benar terhadap server asli (field id/judul/status sesuai).

## Langkah 5 — bertanya (model AI belum diatur — sesuai batasan sandbox uji, TIDAK ADA model AI terpasang)
```
$ python3 scripts/notebook.py tanya --notebook "Brosur & SOP Klinik" --pertanyaan "Apa langkah pendaftaran pasien baru?"
GALAT: Belum ada model AI default yang diatur di Open Notebook (mis. Ollama lokal atau kunci API OpenAI/Anthropic). Buka http://127.0.0.1:8502 > Settings > Models, tambah minimal satu model bahasa, lalu jadikan default sebelum memakai 'tanya'/'ringkasan'.
```
(exit code 8) ✅ **Pesan galat jelas dan tepat** — dikonfirmasi memanggil `GET /api/models/defaults` asli, yang memang mengembalikan `default_chat_model: null` karena sandbox uji tidak memasang Ollama/API key (di luar cakupan uji ini). Agent tidak menebak jawaban, tidak macet, langsung mengarahkan ke Settings sesuai `docs/panduan-open-notebook.md` §5.

## Ringkasan skenario
- Alur "cek → buat notebook → tambah sumber → tanya" **terputus di langkah 3** karena bug `tambah-sumber`. Setelah dilewati manual, langkah 4–5 berjalan benar dan pesan error untuk model AI kosong sudah tepat.
