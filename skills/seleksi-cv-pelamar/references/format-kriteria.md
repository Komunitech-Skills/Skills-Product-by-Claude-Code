# Format kriteria.json (untuk pra-saring dengan script)

```json
{
  "posisi": "Admin Toko Online",
  "wajib": [
    {"nama": "Kelola toko marketplace", "kata": ["shopee", "tokopedia", "tiktok shop"], "bobot": 3, "min_tahun": 1},
    {"nama": "Spreadsheet", "kata": ["excel", "google sheet"], "bobot": 2}
  ],
  "nilai_tambah": [
    {"nama": "Iklan marketplace", "kata": ["shopee ads", "iklan"], "bobot": 2}
  ]
}
```

- `kata`: kata kunci (huruf besar/kecil tidak berpengaruh; cocok per kata utuh). Tulis variasi yang umum di CV Indonesia.
- `bobot`: bawaan 1. `min_tahun`: bawaan 0 (tidak menilai lama kerja). Lama dihitung dari rentang tahun di bagian pengalaman ("2019 - 2023" = 4, "sekarang" = tahun ini, tumpang tindih tidak dobel) atau "3 tahun" di kalimat yang sama dengan kata kunci. Usia ("umur 28 tahun") dan bagian pendidikan tidak dihitung.
- `gugur_bila_tidak_ada` (hanya di `wajib`): true bila syarat dasar sah; hasilnya "belum_memenuhi_syarat_dasar", bukan dibuang.
- `termasuk_pendidikan`: true bila kata kunci boleh dicari di bagian pendidikan (jarang dipakai).
- Kriteria yang menyangkut usia, jenis kelamin, agama, suku, status kawin, penampilan, dan sejenisnya **ditolak** script dengan pesan galat.

Perintah: `python3 scripts/nilai_cv.py kriteria.json folder_cv --top 5 [--format ringkas|json|csv]` (Windows: `python` atau `py`). Sumber CV: folder berisi `.txt`/`.md` satu berkas satu CV, atau CSV berkolom `id` dan `teks`. PDF/DOCX diubah ke teks dulu.

Skor script: `100 x (0,75 x wajib + 0,25 x nilai tambah)`; tanpa nilai tambah `100 x wajib`. Nilai per kriteria: 1 bila ada (dan lama cukup), 0,5 + 0,5 x (lama/min_tahun) bila ada tapi lama kurang, 0,5 bila min_tahun ada tapi lama tidak tertulis, 0 bila tidak ada. Hasil hanyalah pra-saring kata kunci; kutipan bukti wajib diambil agent dari CV.
