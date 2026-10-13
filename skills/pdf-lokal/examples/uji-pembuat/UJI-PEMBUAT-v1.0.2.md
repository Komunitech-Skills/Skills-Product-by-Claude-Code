# Catatan pembuat — pdf-lokal v1.0.2 (2026-09-25)

**Ditulis oleh:** agent pembuat skill (bukan penguji independen). Catatan ini
**tidak** menggantikan uji independen di `examples/HASIL-UJI.md` — nilai/keputusan resmi
tetap yang ada di file itu (skor 8/10, lulus, per uji ulang v1.0.1 2026-09-24).
`HASIL-UJI.md` tidak diubah.

## Tugas
Perawatan rutin: cek apakah temuan rendah (R2, R3) dari `HASIL-UJI.md` masih terbuka,
perbaiki yang jelas & aman, tanpa menambah fitur baru. Data uji sesi ini disiapkan di
`<folder uji sementara>/pdf`
(tidak dipakai — lihat bagian "Verifikasi" di bawah, tidak perlu data uji baru karena
pengecekan ini murni membaca teks yang sudah ada + regresi otomatis yang sudah tersedia).

## Temuan R2 & R3: sudah diperbaiki di v1.0.1, diverifikasi ulang tuntas di sesi ini

Membaca `HASIL-UJI.md` sampai habis (termasuk bagian "Uji ulang v1.0.1" baris 108-183),
penguji independen ke-2 sudah mengonfirmasi:

| Temuan | Status di HASIL-UJI.md | Verifikasi ulang saya di file saat ini |
|---|---|---|
| R2 — fallback bila `ekstrak-nota-faktur` belum terpasang | "Sudah ada, benar" | **Dikonfirmasi.** `SKILL.md` bagian "Kapan TIDAK digunakan" (baris 30-34) memuat kalimat eksplisit: "Kalau skill itu belum terpasang/dibeli, jangan diam saja - katakan dengan jelas: ..." — sesuai instruksi. |
| R3 — bedakan dokumen sensitif dari upload PDF online | "Sudah ada, tegas" | **Dikonfirmasi.** `SKILL.md` bagian "Cara manual tanpa script" poin 4-5 (baris 126-136) memisahkan tegas **Dokumen BIASA** (boleh diarahkan ke situs resmi Stirling-PDF sebagai jalan terakhir, dengan peringatan file akan diunggah) vs **Dokumen SENSITIF** (slip gaji, KTP/data pribadi, kontrak rahasia, data keuangan) → **"JANGAN PERNAH" menawarkan upload online**, bahkan bila diminta pengguna sendiri. |

Saya juga menelusuri `README.md`, `docs/panduan-stirling-pdf.md`, dan
`skills/pdf-lokal/scripts/pdf.py` untuk memastikan tidak ada tempat lain yang masih
menyarankan upload online tanpa membedakan sensitivitas dokumen: **tidak ditemukan**
(script tidak pernah punya logika "arahkan ke situs online" — itu murni instruksi
agen di `SKILL.md`; `README.md` dan panduan Docker tidak menyebut alternatif online
sama sekali).

**Kesimpulan R2/R3:** tidak ada perbaikan kode/isi lagi yang diperlukan untuk kedua
temuan ini — sudah tuntas sejak commit `edb39bd` (revisi v1.0.1) dan sudah lulus
verifikasi independen di commit `c0ec9fb`. Saya **tidak** mengarang perubahan baru
untuk R2/R3 supaya tidak menambah risiko regresi pada teks yang sudah terbukti benar.

## Temuan lain yang saya temukan sendiri saat menelusuri ulang (bukan dari daftar R2/R3)

Saat memverifikasi R2/R3, saya menemukan 2 **inkonsistensi dokumentasi** peninggalan
revisi v1.0.1 yang belum ikut diperbarui — bukan cacat fungsional/keamanan, tapi
melanggar prinsip kejujuran klaim di pedoman kurasi Komunitech (prinsip kejujuran):

1. **`SKILL.md` bagian Batasan** masih menulis "Belum diuji dengan Stirling-PDF versi
   lain selain v2.14.3" — padahal `references/sumber-api-stirling.md` dan
   `docs/panduan-stirling-pdf.md` sudah mencatat bahwa v1.0.1 **juga** diuji tuntas ke
   v3.0.0 (dan itulah versi yang direkomendasikan di panduan Docker sekarang). Klaim
   lama ini **meremehkan** cakupan uji yang sebenarnya sudah dilakukan.
   → Diperbaiki: sekarang menyebut kedua versi (2.14.3 dan 3.0.0) sudah diuji, sisanya
   (belum diuji aplikasi desktop resmi) tetap apa adanya.
2. **`README.md` bagian "Status pengujian"** juga masih hanya menyebut v2.14.3, belum
   menyebut v3.0.0 maupun hasil verifikasi independen (`pdfinfo`/`pdftotext`/`qpdf`/
   `sha256sum`) dan jumlah tes regresi terbaru (15/15).
   → Diperbaiki: disamakan dengan fakta di `HASIL-UJI.md` dan
   `references/sumber-api-stirling.md`.
3. **`README.md` bagian Manfaat** mengklaim mutlak "file PDF ... tidak pernah diunggah
   ke situs PDF online pihak ketiga" — klaim ini generik untuk seluruh skill, padahal
   `SKILL.md` sendiri (poin R3 di atas) mengizinkan agen menyarankan situs online resmi
   Stirling-PDF untuk dokumen **biasa** kalau Stirling-PDF belum terpasang. Klaim lama
   berisiko dibaca pembeli sebagai jaminan mutlak yang sedikit meleset dari perilaku
   nyata skill, tepat di area yang sama dengan R3 (privasi).
   → Diperbaiki: kalimat sekarang menegaskan yang benar-benar mutlak (script sendiri
   tidak pernah mengunggah kemana pun) DAN menonjolkan jaminan R3 untuk dokumen
   sensitif secara eksplisit, alih-alih klaim generik yang terlalu luas.

Ketiganya adalah perbaikan teks murni (tidak ada fitur baru, tidak ada perubahan
perilaku script selain nomor versi).

## Perubahan pada `scripts/pdf.py`
Satu-satunya perubahan: konstanta `VERSI = "1.0.1"` → `"1.0.2"` (dipakai di teks
`--help`), disamakan dengan `catalog.csv`. Tidak ada perubahan logika/endpoint/pesan
error apa pun.

**Tes regresi baru ditambahkan** (karena ada perubahan script, sesuai aturan kerja):
skenario `versi-konsisten-di-bantuan` di `tests/uji_regresi.py` — membaca konstanta
`VERSI` langsung dari kode sumber `scripts/pdf.py` (regex `^VERSI = "X.Y.Z"$`) lalu
memastikan angka yang sama benar-benar tercetak di `python3 pdf.py --help`
(`pdf-lokal vX.Y.Z`). Ini jaring pengaman supaya versi di konstanta script, teks
bantuan CLI, dan `catalog.csv` tidak diam-diam menyimpang lagi di masa depan (persis
jenis inkonsistensi yang saya temukan pada dokumentasi Markdown di atas).

## Verifikasi
```
$ python3 skills/pdf-lokal/tests/uji_regresi.py
...
16/16 skenario lulus.   # naik dari 15/15 (v1.0.1) — tes baru versi-konsisten-di-bantuan

$ python3 scripts/validate.py
✅ 68 skill valid, 68 baris katalog sesuai.
```
Tidak menjalankan Stirling-PDF sungguhan di sesi ini — tidak ada perubahan pada
logika pemanggilan API, jadi cukup regresi server tiruan + pembacaan silang dokumen.
Tidak ada file data uji baru yang diperlukan di scratchpad; direktori scratchpad
yang diminta sudah disiapkan namun kosong karena pengecekan ini murni tekstual +
regresi otomatis yang sudah ada.

## Berkas yang diubah
- `skills/pdf-lokal/SKILL.md` — perbaiki klaim versi Stirling-PDF yang sudah diuji.
- `skills/pdf-lokal/README.md` — sinkronkan status pengujian & klaim privasi dengan
  perilaku nyata skill (terkait R3).
- `skills/pdf-lokal/scripts/pdf.py` — bump `VERSI` ke `1.0.2`.
- `skills/pdf-lokal/tests/uji_regresi.py` — tes regresi baru untuk konsistensi versi.
- `catalog.csv` — baris `pdf-lokal`: versi `1.0.2`, status `uji`, tanggal_update
  `2026-09-25`.
- `HASIL-UJI.md` — **tidak diubah** (sesuai instruksi; itu milik penguji independen).

## Status setelah revisi ini
R2 dan R3 sudah tuntas sejak v1.0.1 dan tetap tuntas di v1.0.2 (tidak ada regresi).
Perbaikan v1.0.2 murni housekeeping dokumentasi (akurasi klaim versi & privasi) +
1 baris konstanta versi script + 1 tes regresi baru. Karena tidak ada perubahan
fungsional pada mesin pengolahan PDF, saya **tidak** mengklaim ini perlu uji ulang
penuh oleh penguji independen dari nol — cukup verifikasi ringan bahwa teks yang
diubah akurat (sesuai pola yang dipakai untuk N1 di v1.0.1). Status katalog diset ke
`uji` sesuai instruksi kerja; keputusan naik ke `lulus`/`beta`/`rilis` tetap milik
pemilik/penguji independen berikutnya.
