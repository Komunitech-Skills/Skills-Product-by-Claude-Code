# Contoh 1 — Kumpulkan regulasi & tanya-jawab (skenario normal)

Konteks: konsultan pajak mengumpulkan PP/PMK terkait UMKM ke satu notebook, lalu bertanya langsung alih-alih membaca satu-satu.

> ⚠️ **Status uji.** Output di bawah dihasilkan dengan menjalankan `scripts/notebook.py` v1.0.1 terhadap **server tiruan yang sudah diperbarui** (`tests/uji_regresi.py`, sekarang menuntut `multipart/form-data` & skema pencarian yang sama seperti server asli — lihat `ATTRIBUTION.md`), bukan langsung dari Open Notebook asli. Bentuk JSON dan alur pesan (termasuk perbaikan `tambah-sumber` & `cari`) **sudah dibuktikan sama persis terhadap Open Notebook 1.14.0 ASLI** oleh penguji independen — lihat `examples/HASIL-UJI.md` dan `examples/03-07-*-uji-akun-b.md` untuk log lengkap server sungguhan. Isi jawaban AI ("PPh final UMKM 0,5%...") tetap **contoh yang direkayasa untuk uji**, bukan jawaban model AI sungguhan (model AI di luar cakupan uji ini).

## 1. Cek koneksi
```
$ python3 scripts/notebook.py cek
```
```json
{
  "url": "http://127.0.0.1:5055",
  "auth_aktif": false,
  "jumlah_notebook": 1,
  "kata_sandi": "(tidak dipakai)",
  "pesan": "Open Notebook bisa dihubungi dan siap dipakai."
}
```

## 2. Daftar notebook yang ada
```
$ python3 scripts/notebook.py daftar-notebook
```
```json
{
  "jumlah": 1,
  "notebook": [
    {
      "id": "notebook:abc123",
      "nama": "Regulasi Pajak UMKM",
      "deskripsi": "kumpulan PP/PMK",
      "jumlah_sumber": 2,
      "jumlah_catatan": 0,
      "diarsip": false
    }
  ]
}
```

## 3. Tambah sumber (pratinjau dulu, lalu --ya)
```
$ python3 scripts/notebook.py tambah-sumber --notebook "Regulasi Pajak UMKM" --tipe link --sumber-url "https://jdih.kemenkeu.go.id/pp-55-2022"
```
```
[PRATINJAU - belum dikirim] Akan menambah sumber ke notebook
  notebook_id: notebook:abc123
  sumber: {'notebooks': ['notebook:abc123'], 'type': 'link', 'url': 'https://jdih.kemenkeu.go.id/pp-55-2022'}
  catatan: Tambahkan --ya untuk benar-benar menambah. Pemrosesan (baca isi, ringkas) berjalan di latar belakang; cek dengan 'daftar-sumber'.
```
```
$ python3 scripts/notebook.py tambah-sumber --notebook "Regulasi Pajak UMKM" --tipe link --sumber-url "https://jdih.kemenkeu.go.id/pp-55-2022" --ya
```
```json
{
  "ditambahkan": true,
  "id": "source:baru1",
  "judul": "Processing...",
  "status": "new",
  "catatan": "Sumber sedang diproses (dibaca & diindeks). Cek 'daftar-sumber' beberapa saat lagi bila judul/isi belum lengkap."
}
```
Permintaan ini dikirim sebagai `multipart/form-data` (bukan JSON — lihat `ATTRIBUTION.md` soal bug v1.0.0 yang diperbaiki). Judul awal untuk tipe `link` biasanya `"Processing..."` sampai worker Open Notebook selesai membaca halamannya; cek lagi dengan `daftar-sumber` beberapa saat kemudian untuk judul final.

## 4. Cek status pemrosesan sumber
```
$ python3 scripts/notebook.py daftar-sumber --notebook "Regulasi Pajak UMKM"
```
```json
{
  "notebook_id": "notebook:abc123",
  "jumlah": 2,
  "sumber": [
    {"id": "source:s1", "judul": "PP 55/2022", "status": "completed", "jumlah_bagian_terindeks": 12, "jumlah_insight": 1},
    {"id": "source:s2", "judul": "(belum ada judul, masih diproses)", "status": "processing", "jumlah_bagian_terindeks": 0, "jumlah_insight": 0}
  ]
}
```

## 5. Tanya-jawab dengan kutipan
```
$ python3 scripts/notebook.py tanya --notebook "Regulasi Pajak UMKM" --pertanyaan "Berapa tarif PPh final UMKM terbaru?"
```
```json
{
  "pertanyaan": "Berapa tarif PPh final UMKM terbaru?",
  "jawaban": "PPh final UMKM 0,5% dari omzet (PP 55/2022).",
  "catatan": "Jawaban disusun model AI dari sumber di notebook Anda. Selalu periksa ulang isi penting (regulasi, angka, kutipan) di sumber aslinya lewat 'daftar-sumber'/'cari' sebelum dipakai."
}
```
Agent menyampaikan jawaban **beserta catatan periksa-ulang** apa adanya — tidak dihilangkan sekalipun terkesan mengulang.

## 6. Cari cepat tanpa model AI
```
$ python3 scripts/notebook.py cari --kueri "PPh final"
```
```json
{
  "kueri": "PPh final",
  "jumlah": 1,
  "hasil": [
    {"judul": "PP 55/2022", "id_dokumen": "source:s1", "relevansi": 0.734}
  ],
  "catatan": "API pencarian Open Notebook tidak menyediakan cuplikan kalimat yang cocok — hanya judul & id dokumen. Buka dokumennya lewat 'daftar-sumber' atau http://127.0.0.1:8502 untuk melihat isinya."
}
```
API pencarian resmi Open Notebook **tidak** mengembalikan cuplikan kalimat yang cocok (dikonfirmasi terhadap server asli) — hasil hanya judul, id dokumen, dan skor relevansi. Agent menyampaikan keterbatasan ini apa adanya, tidak berpura-pura punya cuplikan.
