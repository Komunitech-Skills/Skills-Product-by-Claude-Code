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

**Skor akhir: 65,3/100 — Cocok, lamar sambil perkuat celah**
(Preferensi tidak dinilai → bobot 35/30/15 dinormalisasi ke total 0,80:
(55×0,35 + 60×0,30 + 100×0,15) / 0,80 = 52,25 / 0,80 = 65,3125 → 65,3)
### Celah: belum pernah pakai Accurate/MYOB (bukan wajib, jadi tidak fatal); pengalaman masih magang bukan kerja formal.
### Rekomendasi: Lamar — kualifikasi wajib terpenuhi, celah software akuntansi wajar untuk fresh graduate.

## Skor Kecocokan Kata Kunci
56.0% kata kunci lowongan ditemukan di draf CV (14/25)
Sudah ada: keuangan, akuntansi, bulanan, jakarta, arsip, bantu, dasar, dokumen,
excel, finance, fresh, graduate, harian, input
Belum terlihat (setelah disaring — staff, abadi, makmur, jadi, mengoperasikan dibuang
karena bukan keahlian/pecahan nama PT): accurate, bank, deadline, domisili, laporan,
manajemen
→ Ditanyakan ke pengguna: pernah rekonsiliasi BANK, atau hanya kas? Pernah pakai
VLOOKUP/Pivot Table dan mengurus PPN/PPh? (jawaban menentukan apakah ditambahkan)

## CV Versi ATS
Ayu Lestari
Jakarta · 0813xxxxxxx · ayu.lestari@email.com

RINGKASAN PROFIL
Fresh graduate S1 Akuntansi dengan pengalaman magang mengelola input transaksi
harian dan membantu rekonsiliasi kas bulanan menggunakan Excel...

PENGALAMAN KERJA
Magang Finance — Koperasi Mahasiswa Universitas Merdeka (Jan 2025-Jun 2025)
- Input transaksi harian ke buku besar manual dan Excel
- Membantu rekonsiliasi kas bulanan
- Mengarsipkan dokumen dan bukti transaksi keuangan

PENDIDIKAN
S1 Akuntansi — Universitas Merdeka (2025)

KEAHLIAN
Excel, dasar akuntansi, teliti
[isi hanya bila benar-benar Anda kuasai: VLOOKUP, Pivot Table, perpajakan (PPN, PPh)]
[Accurate/MYOB TIDAK dicantumkan — pengguna belum pernah pakai]

## Surat Lamaran (Formal) / Email Singkat
(disusun, menyebut kesediaan belajar Accurate/MYOB, tidak mengklaim sudah bisa)

## Checklist Sebelum Kirim
- [x] Tidak ada pengalaman/gelar dikarang — magang & pendidikan sesuai input
- [x] Accurate/MYOB tidak dicantumkan sebagai keahlian yang dimiliki
- [x] VLOOKUP, Pivot Table, PPN/PPh, dan rekonsiliasi bank tidak diklaim — tidak ada
      di data pelamar; ditanyakan dulu
- [x] Ekspektasi gaji 4,5-5 juta dari isian pengguna sendiri, bukan taksiran pasar
- [x] CV satu kolom, tanpa tabel/foto
```

## Catatan penguji (audit contoh 2026-10-13)
- **Skill tidak boleh memasukkan keahlian/pengalaman yang tidak dimiliki pelamar.**
  Versi awal contoh ini menulis "Excel (VLOOKUP, Pivot Table), dasar akuntansi &
  perpajakan (PPN, PPh)" di KEAHLIAN dan "rekonsiliasi bank" di pengalaman — semuanya
  diambil dari teks lowongan, padahal data pelamar hanya menyebut Excel, buku besar
  manual, dan rekonsiliasi **kas**. Kini diganti `[isi hanya bila benar-benar Anda
  kuasai: ...]` dan ditanyakan ke pengguna (SKILL.md Langkah 5 & checklist "tidak
  dikarang").
- Skor akhir evaluasi: versi awal menulis 66/100; dihitung ulang dengan rumus bobot
  `references/evaluasi-kecocokan.md` (dimensi tidak dinilai dikeluarkan, bobot
  dinormalisasi) = **65,3/100** — label tetap "Cocok". Skill ini tidak punya script
  untuk skor evaluasi; `scripts/skor_kecocokan.py` hanya menghitung kata kunci.
- Skor kata kunci dijalankan ulang 2026-10-13 dengan `scripts/skor_kecocokan.py`
  (v1.1.3) pada CV di atas setelah perbaikan (isian `[...]` tidak ikut dihitung karena
  belum dikonfirmasi): **56.0% (14/25)**. Versi awal menulis 48.0% (12/25) dari draf
  CV lain dengan script v1.1.0 (daftar kata kunci teratas berubah sejak STOPWORDS
  diperluas di v1.1.1).

## Verifikasi independen (uji awal Akun B)
- Skor kata kunci dihitung ulang dengan menjalankan `scripts/skor_kecocokan.py` langsung
  (bukan simulasi, script v1.1.0): **48.0% (12/25)** — persis sama dengan yang ditampilkan
  pada versi awal contoh (kini diganti hasil script v1.1.3, lihat catatan di atas).
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
- Status 2026-10-13: noise `dipersilakan`, `jujur`, `melamar` sudah masuk STOPWORDS
  sejak v1.1.1 dan tidak muncul lagi di hasil script.
