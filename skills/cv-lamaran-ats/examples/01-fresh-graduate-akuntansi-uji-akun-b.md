# Skenario 1 (Akun B) — Normal: Fresh Graduate Akuntansi, Lowongan JobStreet Ditempel

## Input pengguna
```
Halo, saya baru lulus S1 Akuntansi. Ada lowongan di JobStreet nih, tolong sesuaikan
CV saya:

Staff Keuangan (Finance Staff)
PT Sinar Abadi Makmur - Jakarta Selatan
Kualifikasi:
- Min. S1 Akuntansi/Manajemen Keuangan, fresh graduate dipersilakan melamar
- Menguasai Microsoft Excel (VLOOKUP, Pivot Table)
- Memahami dasar akuntansi dan perpajakan (PPN, PPh)
- Teliti, jujur, dan mampu bekerja dengan deadline
- Mengoperasikan software akuntansi jadi nilai tambah (Accurate/MYOB)
- Domisili Jakarta atau sekitarnya
Tanggung jawab: input transaksi harian, rekonsiliasi bank bulanan, bantu laporan
keuangan bulanan, arsip dokumen keuangan.

Data saya: Ayu Lestari, Jakarta, 0813xxxxxxx, ayu.lestari@email.com. S1 Akuntansi
Universitas Merdeka lulus 2025. Magang Finance di Koperasi Mahasiswa Universitas
Merdeka Jan-Jun 2025: input transaksi harian ke buku besar manual dan Excel, bantu
rekonsiliasi kas bulanan, arsip bukti transaksi. Ekspektasi gaji 4,5-5 juta. Belum
pernah pakai Accurate/MYOB.
```

## Output (ringkas, disimulasikan agent membaca hanya folder skill)
Karena belum ada profil induk sebelumnya, agent membuatnya dulu (Langkah 1), lalu:

```
## Evaluasi Kecocokan Lowongan: Staff Keuangan di PT Sinar Abadi Makmur
**Saringan wajib:** LULUS — pendidikan S1 Akuntansi sesuai; lokasi Jakarta sesuai;
gaji tidak dicantumkan lowongan → "belum diketahui, tanyakan saat proses".

| Dimensi | Skor | Catatan |
|---|---|---|
| Keahlian & alat kerja | 55/100 | Excel & dasar akuntansi ada; Accurate/MYOB belum dikuasai (disebut "nilai tambah", bukan wajib) |
| Pengalaman | 60/100 | Magang finance relevan fungsinya (input transaksi, rekonsiliasi), tapi bukan pengalaman kerja formal |
| Preferensi & arah karier | — | Belum cukup data, tidak dinilai |
| Syarat administratif | 100/100 | Fresh graduate dipersilakan, pendidikan sesuai |

**Skor akhir: 66/100 — Cocok, lamar sambil perkuat celah**
### Celah: belum pernah pakai Accurate/MYOB (bukan wajib, jadi tidak fatal); pengalaman masih magang bukan kerja formal.
### Rekomendasi: Lamar — kualifikasi wajib terpenuhi, celah software akuntansi wajar untuk fresh graduate.

## Skor Kecocokan Kata Kunci
48.0% kata kunci lowongan ditemukan di draf CV (12/25)
Sudah ada: akuntansi, bulanan, jakarta, bank, dasar, excel, finance, fresh, graduate,
harian, input, membantu
Belum terlihat (setelah disaring — beberapa hasil mentah script dibuang karena bukan
keahlian, lihat catatan verifikasi di bawah): keuangan, deadline, dokumen, domisili,
laporan, manajemen

## CV Versi ATS
Ayu Lestari
Jakarta · 0813xxxxxxx · ayu.lestari@email.com

RINGKASAN PROFIL
Fresh graduate S1 Akuntansi dengan pengalaman magang mengelola input transaksi
harian dan rekonsiliasi bank menggunakan Excel...

PENGALAMAN KERJA
Magang Finance — Koperasi Mahasiswa Universitas Merdeka (Jan 2025-Jun 2025)
- Input transaksi harian ke sistem pencatatan dan Excel
- Membantu rekonsiliasi bank/kas bulanan
- Mengarsipkan dokumen dan bukti transaksi keuangan

PENDIDIKAN
S1 Akuntansi — Universitas Merdeka (2025)

KEAHLIAN
Excel (VLOOKUP, Pivot Table), dasar akuntansi & perpajakan (PPN, PPh), teliti
[Accurate/MYOB TIDAK dicantumkan — pengguna belum pernah pakai]

## Surat Lamaran (Formal) / Email Singkat
(disusun, menyebut kesediaan belajar Accurate/MYOB, tidak mengklaim sudah bisa)

## Checklist Sebelum Kirim
- [x] Tidak ada pengalaman/gelar dikarang — magang & pendidikan sesuai input
- [x] Accurate/MYOB tidak dicantumkan sebagai keahlian yang dimiliki
- [x] Ekspektasi gaji 4,5-5 juta dari isian pengguna sendiri, bukan taksiran pasar
- [x] CV satu kolom, tanpa tabel/foto
```

## Verifikasi independen
- Skor kata kunci dihitung ulang dengan menjalankan `scripts/skor_kecocokan.py` langsung
  (bukan simulasi): **48.0% (12/25)** — persis sama dengan yang ditampilkan di atas.
- **Temuan:** daftar "kata kunci hilang" mentah dari script masih memuat noise —
  `abadi`, `makmur` (pecahan nama PT), `dipersilakan`, `jujur`, `melamar` — 5 dari 13
  kata hilang mentah adalah noise. SKILL.md Langkah 4 sudah mengharuskan menyaring
  sebelum tampil ke pengguna, dan simulasi di atas mematuhi instruksi itu (kata-kata
  noise tersebut dibuang). Namun ini berarti `STOPWORDS` di script (v1.1.0, sama
  persis dengan v1.0.1 setelah "diperluas" menurut catatan koordinator) **belum**
  benar-benar menambah kata seperti "dipersilakan", "jujur", "melamar" — pekerjaan
  penyaringan masih sepenuhnya bergantung kehati-hatian agent, bukan otomatis di script.
  Ini defect RINGAN berulang dari uji v1.0.1 yang belum tuntas diperbaiki di script itu
  sendiri (lihat detail di `08-pembanding-v101-vs-v110-uji-akun-b.md`).
- Ekspektasi gaji (4,5-5 juta) hanya dipakai untuk mencatat "belum diketahui dari
  lowongan" — tidak ada angka pasar yang dikarang. Sesuai `evaluasi-kecocokan.md`.
