# Uji OpenClaw Asli — Solusi VIP Usaha Offline

- **Tanggal:** 2026-10-01 (Asia/Jakarta)
- **Penguji:** agent penguji independen Komunitech (bukan pembuat skill/solusi)
- **Rincian per skenario:** folder [`uji-openclaw/`](uji-openclaw/) (pesan, balasan SEBELUM & SESUDAH utuh, verifikasi, nilai)

## Cara uji

- OpenClaw terpasang lokal, dipanggil dengan `openclaw agent --local --session-id … -m "…" --json` (satu giliran per panggilan, tanpa Telegram/gateway). Model: router Komunitech `ninerouter/komunitech` — **sama dengan bot Telegram member**.
- **SEBELUM** = home OpenClaw tanpa skill apa pun. **SESUDAH** = home OpenClaw dengan paket skill usaha-offline terpasang di `~/.openclaw/skills/`. Workspace (AGENTS/SOUL/IDENTITY) identik.
- Pesan identik di kedua sisi, ditulis seperti member awam di Telegram (format "1,5jt", "38.000"). Bila agent bertanya balik, dijawab **sekali** sebagai member, jawaban sama di kedua sisi.
- Pemakaian skill dicek dari daftar alat di JSON hasil dan transkrip sesi (file SKILL.md yang dibaca, script yang dijalankan).
- Semua angka dihitung ulang dengan Python terpisah; aturan dicek terhadap PP 55/2022, PP 35/2021, Perpres 64/2020, PP 44/45/46/2015, PMK 168/2023, PMK 81/2024.
- Semua data (nama, rekening, omzet) **fiktif**.

## Skor

| # | Skenario | Skill yang terpakai (SESUDAH) | SEBELUM | SESUDAH | Pemenang |
|---|---|---|:-:|:-:|---|
| 01 | HPP & harga jual es kopi | `hitung-hpp` (script dijalankan) | 8 | 7 | SEBELUM |
| 02 | Gaji + BPJS + PPh 21, 2 karyawan | `gaji-umkm` (database dibuat, `hitung`) | 8 | 8 | Seri |
| 03 | PPh Final 0,5% OP, batas Rp500 jt | `pph-final-umkm` (script dijalankan) | 8 | 7 | SEBELUM |
| 04 | Rekap kas harian dari file + selisih laci | **tidak ada** (`kas-umkm` hanya ditawarkan) | 9 | 9 | Seri |
| 05 | Tagih piutang laundry (info awal kurang) | `tagih-piutang` (script hari telat) | 6 | 8 | SESUDAH |
| | **Rata-rata** | | **7,8** | **7,8** | |

**Skor keseluruhan solusi (SESUDAH): 7/10.**

Penilaian jujur: untuk **pertanyaan sekali-jawab**, model router Komunitech tanpa skill sudah kuat — angka gaji, BPJS, PPh final, dan kas di kedua sisi sama-sama benar. Paket skill **tidak** membuat jawaban satu-giliran lebih akurat; di 2 dari 5 skenario malah sedikit kalah karena model melewatkan catatan dari script atau mengira-ngira di luar tabel script. Keunggulan nyata paket ada di:
1. **Keamanan & kepatuhan kebijakan** — tanpa skill, agent menawarkan "langsung saya kirimkan ke WA Bu Rina" (melanggar mode Copilot dan mengklaim kemampuan yang tidak ada). Dengan skill, tidak.
2. **Data yang menetap** — gaji tersimpan di database lokal (bulan depan tinggal `hitung`), slip & CSV transfer, resep HPP tersimpan sebagai file yang bisa diubah.
3. **Kejujuran batas data** — dengan skill, agent tidak mengklaim "di atas UMK" tanpa angka; ada dasar aturan + catatan pembulatan.

Nilai jual paket sebaiknya ditekankan pada sistem kerja harian (pencatatan, jadwal laporan, data tersimpan, pagar keamanan), **bukan** "jawaban lebih pintar" — klaim itu tidak didukung uji ini.

## Cacat per skill (bukti + saran)

| Skill | Cacat | Bukti | Saran |
|---|---|---|---|
| `hitung-hpp` | Model menyarankan harga yang **tidak ada di tabel script** (Rp18.000) lalu mengira BEP-nya (~429–460, benar 501 gelas) dan menulis klaim salah "biaya terbesar bukan bahan (7.205) tapi gaji+sewa+listrik (4.327)". | `uji-openclaw/01-hpp-harga-jual.md` | Tambahkan aturan wajib di SKILL.md: "Setiap harga yang Anda sarankan harus dihitung script — bila di luar tabel, jalankan ulang dengan `harga_jual` (sudah didukung `references/format-input.md`). Jangan membandingkan komponen biaya tanpa angka dari output script." |
| `pph-final-umkm` | Catatan script "cek DJP bila batas setor jatuh di hari libur" tidak diteruskan (15 Nov 2026 = Minggu). Batas jangka waktu tarif 0,5% (7 tahun pajak untuk OP sejak terdaftar, PP 55/2022 Ps. 59) sama sekali tidak disinggung, padahal NPWP 2021 → batas 2027. | `uji-openclaw/03-pph-final-umkm.md` | Script menghitung hari dalam pekan dan menulis "15 Nov 2026 jatuh hari Minggu → setor hari kerja berikutnya". Bila pengguna menyebut tahun terdaftar, script/SKILL wajib mengeluarkan baris "jangka waktu tarif 0,5%: menurut PP 55/2022 s.d. tahun X — cek perubahan aturan terbaru". |
| `gaji-umkm` | Bertanya balik "tanggal masuk" sebelum menghitung (tambah 1 giliran), padahal hanya relevan untuk karyawan yang masuk/keluar di tahun berjalan. UMK tidak dicek (dengan jujur diminta). | `uji-openclaw/02-gaji-bpjs.md` | Izinkan default "masuk sebelum tahun berjalan" dengan asumsi disebut, lalu tanya di akhir. Sediakan tabel UMK/UMP referensi (dengan tahun & sumber) atau minta angka UMK dalam pertanyaan pertama yang sama. |
| `kas-umkm` | Tidak terpicu untuk "rekap catatan kas dari file teks"; agent menghitung sendiri, skill hanya ditawarkan di akhir. Hasil tetap benar, tetapi member tidak mendapat buku kas tersimpan. | `uji-openclaw/04-rekap-kas-harian.md` | Tambah kata pemicu di `description` ("rekap catatan kas", "uang di laci harusnya berapa", "kas kurang", "impor catatan kas") dan alur "impor catatan harian dari teks → buku kas + opname" dengan pratinjau. |
| `tagih-piutang` | Pesan tidak memuat rincian per bulan yang sudah diberikan member; saran eskalasi "tahap 4 ±3 Oktober" (2 hari) terlalu cepat untuk tetangga. | `uji-openclaw/05-tagih-piutang-info-kurang.md` | Selalu tampilkan rincian tagihan bila tersedia; jarak eskalasi minimal mengikuti tahapan (≥7 hari) kecuali pengguna minta lebih cepat. |
| (paket/umum) | Kedua sisi mencari file dengan `find /` ke seluruh disk walau file ada di workspace. | 04 (transkrip) | Di PANDUAN/AGENTS bawaan solusi: "cari file di workspace dulu". Bukan cacat skill. |

## Cuplikan jualan (hanya yang jujur lebih baik)

1. **Tidak asal kirim ke pelanggan.** Tanpa paket: *"Mau langsung saya kirimkan ke nomor WA Bu Rina?"* — Dengan paket: draf sopan + hitung telat (*"Janji bayar: 25 September 2026 → sudah lewat 6 hari"*), Anda yang mengirim. (uji 05)
2. **Gaji bulan depan tinggal satu kalimat.** Dengan paket, data Andi & Sari tersimpan di komputer Anda; hasil hitung sama persis dengan hitungan independen (transfer Rp3.164.150 & Rp2.544.000, setor BPJS Rp818.800), lalu *"bilang saja 'kunci' — saya buatkan slip gaji per orang dan file transfer CSV-nya."* (uji 02)

## Catatan teknis alat uji

- Home SESUDAH berisi 24 skill, termasuk `dasbor-lokal` (status `draft`, menurut PANDUAN belum termasuk paket) dan skill di luar daftar 17+4 PANDUAN (`pengingat-follow-up`, `rekap-penjualan-csv`). Tidak ada yang terpakai di uji ini, tetapi isi home uji tidak persis sama dengan paket yang dijual.
- SEBELUM mencoba web search (`tool_search`/`tool_call`) dan tidak tersedia — wajar untuk home kosong.
- Setiap panggilan 1–4 menit; tidak ada kegagalan/timeout. Transkrip dibaca read-only dari SQLite sesi untuk memastikan skill/script yang dipakai.

## Uji ulang 2026-10-01 (keuangan)

Penguji independen, OpenClaw lokal asli, model router Komunitech (`claude-sonnet-5`), home baru `sol2-usaha-offline` (direset sebelum tiap skenario). Hanya sisi SESUDAH; pesan, jawaban lanjutan, dan file data identik dengan uji pertama. Semua angka dihitung ulang dengan Python dan script skill dijalankan ulang oleh penguji. Tidak ada paket pip yang terpasang selama uji.

| # | Skill (versi) | Cacat lama hilang? | Regresi / temuan baru | Skor lama → baru | Status |
|---|---|---|---|:-:|---|
| [01](uji-openclaw/01-hpp-harga-jual-ulang.md) | `hitung-hpp` 1.0.3 | **Ya**: BEP Rp18.000 = 501 gelas (benar), "bahan baku Rp7.205 (54%) — komponen terbesar" (benar) | BEP Rp19.000/20.000 ditulis 450/409, script 451/410 (selisih 1 gelas, dibulatkan ke bawah oleh model); klaim harga pasar tanpa sumber | 7 → **8** | LULUS |
| [02](uji-openclaw/02-gaji-bpjs-ulang.md) | `gaji-umkm` 1.0.6 | **Ya**: angka lengkap di giliran 1 dengan asumsi tanggal masuk disebut; UMK/JKK/tanggal masuk dalam satu pesan | Tidak ada (kecil: "dua hal" lalu tiga butir) | 8 → **9** | LULUS |
| [03](uji-openclaw/03-pph-final-umkm-ulang.md) | `pph-final-umkm` 1.0.3 | **Ya, keduanya**: "16 Nov 2026 (15 Nov jatuh Minggu…)"; batas 7 tahun s.d. 2027 + PP 20/2026 belum diverifikasi | Tidak ada | 7 → **9** | LULUS |
| [04](uji-openclaw/04-rekap-kas-harian-ulang.md) | `kas-umkm` 1.0.11 | **Ya**: skill kini terpakai (rekap per baris, laba kas + asumsinya, selisih laci), tawaran simpan ke buku kas | Tidak ada | 9 → **9** | LULUS |

Semua angka (HPP 13.331,92; transfer 3.164.150/2.544.000 dan setor BPJS 818.800; PPh final Okt Rp260.000; laci 2.581.500, selisih −1.500) cocok dengan hitungan independen.

## Uji ulang 2026-10-01 (keuangan, putaran 2)

Penguji independen, OpenClaw lokal asli, model router Komunitech, home baru (direset sebelum skenario). Hanya sisi SESUDAH; pesan identik dengan uji pertama dan uji ulang 1. Angka dihitung ulang dengan Python dan script skill dijalankan ulang oleh penguji. Tidak ada paket pip yang terpasang selama uji.

| # | Skill (versi) | Cacat sisa hilang? | Regresi / temuan baru | Skor lama → baru | Status |
|---|---|---|---|:-:|---|
| [01](uji-openclaw/01-hpp-harga-jual-ulang2.md) | `hitung-hpp` 1.0.4 | **Ya**: semua BEP sama persis dengan script (Rp18.000 = 501, Rp20.000 = 410, Rp21.000 = 376, Rp22.000 = 347) | Tidak ada; sisa kecil: klaim "harga pasar umumnya 18-25rb" tanpa sumber | 8 → **8,5** | LULUS |
