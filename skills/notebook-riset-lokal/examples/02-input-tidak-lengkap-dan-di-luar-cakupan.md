# Contoh 2 — Input tidak lengkap & di luar cakupan

> ⚠️ Sama seperti `examples/01-...`, dijalankan terhadap **server tiruan v1.0.1** (mock diperbarui menuntut `multipart/form-data`). Perilaku setara sudah dibuktikan terhadap Open Notebook 1.14.0 ASLI oleh penguji independen — lihat `ATTRIBUTION.md` dan `examples/HASIL-UJI.md`.

## A. Input tidak lengkap: tipe `teks` tanpa isi
```
$ python3 scripts/notebook.py tambah-sumber --notebook "Regulasi Pajak UMKM" --tipe teks --ya
```
```
GALAT: Tipe 'teks' butuh --teks (atau --file - untuk baca dari input).
```
(kode keluar 2). Agent menanyakan isi teks yang ingin ditambahkan sebelum mencoba lagi — tidak menebak isi.

## B. Di luar cakupan: mengunggah file PDF langsung dari komputer pengguna
```
$ python3 scripts/notebook.py tambah-sumber --notebook "Regulasi Pajak UMKM" --tipe file --ya
```
```
GALAT: Unggah file (PDF/Word/dll.) lewat perintah ini belum didukung skill ini — server membutuhkan alamat file di KOMPUTER SERVER (bukan komputer Anda bila beda mesin), dan validasi path itu rumit untuk dijamin aman lewat sekadar argumen baris perintah. Seret file itu ke tampilan web Open Notebook (http://127.0.0.1:8502) untuk sekarang.
```
(kode keluar 8). Skill sengaja menolak, bukan mencoba jalan pintas (mis. menebak path lokal) — agent mengarahkan pengguna ke tampilan web Open Notebook sesuai `SKILL.md` bagian "Kapan TIDAK digunakan".

## C. Di luar cakupan: alamat server bukan komputer sendiri
```
$ python3 scripts/notebook.py cek --url http://192.0.2.10:5055
```
```
GALAT: Alamat Open Notebook 'http://192.0.2.10:5055' bukan komputer ini (127.0.0.1/localhost). Open Notebook TIDAK dirancang untuk dibuka ke internet/jaringan kantor — semua dokumen dan isi tanya-jawab Anda bisa terbaca orang lain. Jalankan skill ini hanya terhadap Open Notebook di komputer sendiri (lihat docs/panduan-open-notebook.md).
```
(kode keluar 2). Tidak ada opsi `--izinkan-jarak-jauh` di skill ini (beda dengan `vikunja-tugas`) — Open Notebook memang tidak dirancang dibuka ke jaringan lain, jadi penolakan bersifat mutlak.

## D. Server tidak merespons dalam waktu wajar
```
$ python3 scripts/notebook.py cek --timeout 1
```
```
GALAT: Tidak ada balasan dari http://127.0.0.1:<port> dalam 1.0 detik (server sibuk/model AI lambat). Coba lagi, atau naikkan --timeout.
```
(kode keluar 4). Agent tidak mengulang otomatis berkali-kali; menyarankan menaikkan `--timeout` (model AI lokal seperti Ollama bisa lambat) atau mencoba lagi nanti.

## E. Model AI belum diatur (kondisi umum bagi pengguna baru)
Bila `GET /models/defaults` belum punya `default_chat_model` (server sungguhan, belum diuji langsung — lihat `ATTRIBUTION.md`), perintah `tanya`/`ringkasan` berhenti dengan pesan:
```
GALAT: Belum ada model AI default yang diatur di Open Notebook (mis. Ollama lokal atau kunci API OpenAI/Anthropic). Buka http://127.0.0.1:8502 > Settings > Models, tambah minimal satu model bahasa, lalu jadikan default sebelum memakai 'tanya'/'ringkasan'.
```
Agent mengarahkan ke `docs/panduan-open-notebook.md` bagian 5, bukan mencoba menebak model mana yang dipakai.
