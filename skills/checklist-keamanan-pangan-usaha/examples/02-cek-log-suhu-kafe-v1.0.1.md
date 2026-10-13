> Catatan: berkas versi 1.0.1 (arsip); angka suhu diperbaiki di versi 1.0.2 — lihat 01 terbaru.

# Skenario 2: kafe kopi + kue + frozen food, cek log suhu 2 hari

**Input:** "Kafe saya jual kopi, kue (cheesecake, brownies, roti sobek) sama frozen food (dimsum, nugget) disimpan di freezer, staf 5 orang. Ini log suhu 2 hari terakhir: [isi data/log-suhu.csv ditempel] cek log ini aman nggak, apa yang harus dibuang"

## Catatan
Data: `data/log-suhu.csv`. Keluaran script pada data yang sama:

```
REKAP LOG SUHU (batas: acuan ilmiah umum; PERLU REVIEW terhadap acuan Kemenkes/BPOM)
Baris terbaca: 16; baris bermasalah: 0

- freezer frozen food [freezer, batas <= -18 C]: 7 pembacaan, -19.0 sampai -12.0 C, melanggar 3, zona bahaya 0 menit
- kulkas kue [kulkas, batas <= 5 C]: 9 pembacaan, 3.0 sampai 9.0 C, melanggar 2, zona bahaya 180 menit

PELANGGARAN:
- 2026-10-04 14:00 kulkas kue: terburuk 9.0 C (batas <= 5 C), sekitar 180 menit di luar batas (dari pembacaan pertama sampai pembacaan yang kembali normal) - LEBIH DARI 2 JAM: bahan berisiko tinggi sebaiknya dibuang
- 2026-10-04 17:00 freezer frozen food: -17.0 C (batas <= -18 C). Tindakan: cek pintu dan colokan, jangan sering dibuka; bahan yang sudah lunak jangan dibekukan ulang, masak segera atau buang.
- 2026-10-05 07:30 freezer frozen food: -12.0 C (batas <= -18 C). Tindakan: cek pintu dan colokan, jangan sering dibuka; bahan yang sudah lunak jangan dibekukan ulang, masak segera atau buang.
- 2026-10-05 12:00 freezer frozen food: -12.0 C (batas <= -18 C). Tindakan: cek pintu dan colokan, jangan sering dibuka; bahan yang sudah lunak jangan dibekukan ulang, masak segera atau buang.
```

Verifikasi independen (python penguji): kulkas 2 pembacaan melanggar, episode 14:00-17:00 = 180 menit; freezer 3 pembacaan melanggar (-17, -12, -12). Semua angka di jawaban agent cocok. Catatan: 180 menit adalah durasi dari pembacaan pertama yang melanggar sampai pembacaan normal; kenaikan bisa sudah mulai setelah 11:00, jadi angka ini sebaiknya disebut "setidaknya 1,5 jam terukur, sampai 3 jam" bukan durasi pasti. Nilai: sebelum 7,5, sesudah 8,0.

**Sumber acuan angka dan aturan pada output di bawah** (ditambahkan kurator 2026-10-13, sama dengan `references/` skill): kulkas ≤ 5 °C — FDA, *Food Code 2022* (+ Supplement 2024), bab 3 dan WHO, *Five Keys to Safer Food* (2006); freezer ≤ -18 °C — USDA FSIS, *Safe Minimum Internal Temperature Chart* (diperbarui 2024) (0 °F); batas 2 jam di suhu ruang untuk bahan berisiko tinggi — USDA FSIS, *Safe Minimum Internal Temperature Chart* (diperbarui 2024) dan WHO, *Five Keys to Safer Food* (2006); masak ≥ 74 °C (ayam/sisa panasan) — FDA, *Food Code 2022* (+ Supplement 2024), bab 3 dan USDA FSIS, *Safe Minimum Internal Temperature Chart* (diperbarui 2024). Batas ini adalah acuan minimum, bukan pengganti acuan Kemenkes/BPOM (PERLU REVIEW).

## Output SESUDAH (skill aktif)

Saya sudah cek log suhu 16 baris (semua kebaca, tidak ada yang rusak). Hasilnya: **tidak sepenuhnya aman** — ada 1 insiden yang mengharuskan barang dibuang, dan 1 pola yang perlu dicek fisik + alatnya.

## 1. Kulkas kue (cheesecake, brownies, roti sobek) — batas aman <= 5°C

| Waktu | Suhu |
|---|---|
| 04/10 07:30 | 4°C |
| 04/10 11:00 | 4,5°C |
| 04/10 **14:00** | **9°C** ⚠️ |
| 04/10 **15:30** | **9°C** ⚠️ |
| 04/10 17:00 | 4°C (sudah normal lagi) |
| 04/10 21:00 | 3°C |
| 05/10 07:30–17:00 | 4–5°C (aman semua) |

Dari pembacaan jam 14:00 sampai kembali normal jam 17:00, kulkas ini berada di **atas 5°C selama sekitar 180 menit (3 jam)**. Karena lebih dari 2 jam, ini sudah melewati batas aman zona bahaya bakteri.

**👉 Yang harus dibuang:** bahan berisiko tinggi di kulkas itu yang terkena rentang panas 14:00–17:00 tanggal 4 Okt — terutama **cheesecake** (basis keju/krim) dan isian krim/susu kalau ada di brownies/roti sobek. Roti sobek tawar sendiri lebih tahan, tapi kalau isiannya custard/krim, ikut buang. Cek fisik: kalau tekstur lembek, lembap berlebih, atau bau asam — buang, jangan tunggu dicium lama-lama.

## 2. Freezer frozen food (dimsum, nugget) — batas aman <= -18°C

| Waktu | Suhu |
|---|---|
| 04/10 07:30 | -19°C |
| 04/10 11:00 | -18°C |
| 04/10 **17:00** | **-17°C** ⚠️ |
| 04/10 21:00 | -18°C |
| 05/10 **07:30** | **-12°C** ⚠️ |
| 05/10 **12:00** | **-12°C** ⚠️ |
| 05/10 17:00 | -19°C (sudah normal lagi) |

Ada 3 pembacaan di atas -18°C, dan yang paling mengkhawatirkan: **-12°C tercatat dua kali berturutan** (07:30 dan 12:00 tanggal 5), lalu baru kembali -19°C jam 17:00. Artinya freezer kemungkinan di atas -18°C selama rentang beberapa jam di antara 07:30–17:00 itu (tidak bisa dipastikan persis karena tidak ada pembacaan di antaranya).

**Tindakan:** cek pintu dan colokan freezer, jangan terlalu sering dibuka. **Cek fisik dimsum/nugget sekarang** — kalau ada bagian yang sudah terasa lunak/berair (tanda sempat mencair sebagian), **jangan dibekukan ulang**: masak segera atau buang. Kalau fisiknya masih keras dan beku penuh, kemungkinan aman, tapi tetap waspada.

## Kemungkinan sebab
- Kulkas kue naik ke 9°C jam makan siang → mungkin sering dibuka-tutup saat jam sibuk, atau pintu tidak rapat.
- Freezer naik ke -12°C dua kali berturutan di hari yang sama → pola ini pantas dicurigai masalah alat (pintu/segel/kompresor), bukan cuma kebiasaan buka-tutup. Kalau berulang lagi besok, sebaiknya panggil teknisi.

**Asumsi:** saya anggap cheesecake dan isian krim adalah yang paling rawan di kulkas kue itu; kalau ternyata isinya cuma roti tawar kering tanpa krim, barang itu bisa dipertimbangkan lagi (tapi tetap cek fisik).

Pengingat: ini acuan ilmiah umum (Celsius), bukan pengganti pemeriksaan resmi Dinkes/BPOM — kalau ada standar lokal yang beda, ikuti itu.

Tiga hal yang mau saya tanyakan:
1. Isi kulkas kue saat jam 14:00–17:00 tanggal 4 itu apa saja — biar saya bisa pastikan item mana yang wajib dibuang?
2. Freezer-nya baru atau sudah lama dipakai? Kalau sering naik ke -12°C, perlu cek teknisi atau tidak?
3. Mau saya buatkan sekalian paket checklist harian + log suhu cetak untuk staf, biar kejadian kayak ini ketahuan lebih cepat ke depannya?

---

## Uji script dengan data rusak (`data/log-suhu-rusak.csv`, `--tanggal 2026-10-06`)

```
REKAP LOG SUHU (batas: acuan ilmiah umum; PERLU REVIEW terhadap acuan Kemenkes/BPOM)
Baris terbaca: 4; baris bermasalah: 4

- kulkas [kulkas, batas <= 5 C]: 2 pembacaan, 4.0 sampai 7.0 C, melanggar 1, zona bahaya 0 menit
- kulkas ayam [masak, batas >= 74 C]: 1 pembacaan, 3.0 sampai 3.0 C, melanggar 1, zona bahaya 0 menit
- kulkas matang [masak, batas >= 74 C]: 1 pembacaan, 4.0 sampai 4.0 C, melanggar 1, zona bahaya 0 menit

PELANGGARAN:
- 2026-10-06 08:00 kulkas: terburuk 7.0 C (batas <= 5 C), sekitar 0 menit di luar batas (dari pembacaan pertama sampai pembacaan yang kembali normal) (belum terlihat pulih sampai pembacaan terakhir; durasi minimal)
- 2026-10-06 09:00 kulkas ayam: 3.0 C (batas >= 74 C). Tindakan: lanjutkan masak/panaskan, ukur ulang di bagian paling tebal sampai mencapai batas.
- 2026-10-06 09:00 kulkas matang: 4.0 C (batas >= 74 C). Tindakan: lanjutkan masak/panaskan, ukur ulang di bagian paling tebal sampai mencapai batas.

BARIS BERMASALAH (dilewati):
- baris 1: waktu tak terbaca
- baris 5: suhu bukan angka wajar
- baris 8: kolom kurang dari 3
- baris 9: suhu bukan angka wajar
```

Temuan: (1) `kulkas ayam` dan `kulkas matang` salah dikenali sebagai **masak (≥ 74 °C)** sehingga kulkas 3-4 °C dilaporkan melanggar dan disuruh "lanjutkan masak" (urutan pola di `jenis_alat` memeriksa kata ayam/matang sebelum kulkas). (2) Baris `2026-10-06 08:00,kulkas,4,5` (koma desimal tanpa tanda kutip) dibaca 4 tanpa peringatan; nilai seperti `5,8` akan terbaca 5 dan pelanggaran hilang. (3) Header `tgl` dilaporkan sebagai baris rusak (kecil). (4) `40 F` ditolak dengan benar; berkas hilang/biner keluar dengan pesan jelas.
