# 00 — Uji A/B: tanpa skill vs dengan skill

Diuji terhadap **server Open Notebook 1.14.0 asli** yang dijalankan langsung (bukan Docker; SurrealDB v2.0.0 biner resmi + `uv sync` dari `github.com/lfnovo/open-notebook` commit `3127f14`) di `127.0.0.1` oleh penguji independen. Lihat `HASIL-UJI.md` untuk detail lingkungan uji.

Skenario: pemilik klinik ingin menyimpan brosur edukasi pasien + SOP internal, lalu bertanya "apa langkah pendaftaran pasien baru?".

## Tanpa skill (agent umum, tanpa `notebook-riset-lokal`)
Prompt: *"Tolong simpan SOP ini ke notebook riset saya di Open Notebook lalu jawab: apa langkah pendaftaran pasien baru?"*

Tanpa skill, agent umum (tanpa pengetahuan REST API Open Notebook) biasanya akan:
- Menebak-nebak cara "menyimpan ke Open Notebook" — kemungkinan mencoba membuka `http://127.0.0.1:8502` dengan browser tool (bila ada) atau mengarang langkah manual, atau langsung menjawab dari pengetahuan umum tanpa benar-benar menyimpan apa pun ke notebook pengguna.
- Tidak tahu endpoint REST resmi (`/api/notebooks`, `/api/sources`, format multipart untuk `/api/sources`), sehingga kemungkinan besar gagal total atau memberi instruksi manual "buka browser, klik di sana" — bukan aksi otomatis.
- Tidak ada pemeriksaan bahwa alamat server memang `127.0.0.1` (risiko menyarankan alamat lain tanpa sadar).
- Tidak ada pratinjau + persetujuan eksplisit sebelum menulis data.

## Dengan skill `notebook-riset-lokal`
Perintah nyata yang dijalankan (server asli):
```
$ python3 scripts/notebook.py buat-notebook --nama "Brosur & SOP Klinik" --deskripsi "Materi edukasi pasien & SOP internal" --ya
{"dibuat": true, "id": "notebook:u88lrelmn9bt9escjshv", "nama": "Brosur & SOP Klinik"}

$ python3 scripts/notebook.py daftar-notebook
{"jumlah": 1, "notebook": [{"id": "notebook:u88lrelmn9bt9escjshv", "nama": "Brosur & SOP Klinik", ...}]}

$ python3 scripts/notebook.py tanya --notebook "Brosur & SOP Klinik" --pertanyaan "Apa langkah pendaftaran pasien baru?"
GALAT: Belum ada model AI default yang diatur di Open Notebook (...). Buka http://127.0.0.1:8502 > Settings > Models...
```
(exit code 8 — pesan jelas, bukan macet/menebak; lihat `03-...-uji-akun-b.md`)

## Kesimpulan uji A/B
- **Notebook berhasil dibuat lewat REST API resmi** dengan struktur pratinjau→`--ya` yang benar — ini nilai tambah nyata dibanding agent umum yang harus menebak endpoint.
- **TEMUAN KRITIS:** `tambah-sumber` (langkah "simpan brosur/SOP") ternyata **gagal 100%** terhadap server asli v1.14.0 — lihat `HASIL-UJI.md` bagian Bug #1. Endpoint `/api/sources` butuh `multipart/form-data`, skill mengirim `application/json`, selalu balas `422`. Jadi untuk skenario A/B ini, skill **belum** benar-benar bisa "menyimpan brosur/SOP" seperti diklaim — nilai tambah dibanding tanpa skill jadi **tidak lengkap** sampai bug ini diperbaiki.
- Pesan galat "model AI belum diatur" jauh lebih baik dari agent tanpa skill (yang akan mengarang jawaban atau diam saja) — ini nilai tambah yang jelas dan terverifikasi terhadap server asli.
- Keamanan (`127.0.0.1` saja) adalah nilai tambah nyata: agent umum tidak akan otomatis menolak alamat bukan localhost.

**Ringkasan:** skill unggul jelas untuk *cek koneksi, buat-notebook, daftar-notebook/sumber, cari, pesan galat awam, keamanan alamat* — tapi **kalah dari janji utamanya** ("kumpulkan dokumen") karena bug `tambah-sumber`. Skor A/B tidak bisa maksimal karena fitur inti belum berfungsi terhadap server asli.
