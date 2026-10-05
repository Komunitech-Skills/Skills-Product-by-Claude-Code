# Sumber `rapikan-data-berantakan`: OpenRefine (BSD-3) + Data Carpentry (CC BY 4.0)

Tanggal: 2026-10-05. Jalur: kurasi (ATM). Kandidat berasal dari `research/sources/kurasi-bsd-cc-2026-10-05.md` (#3 dan #4, skor 19, prioritas TINGGI).

## Sumber
| Sumber | URL | Pembuat | Bukti (dari riset kurasi) | Lisensi | Keputusan |
|---|---|---|---|---|---|
| OpenRefine | https://github.com/OpenRefine/OpenRefine | OpenRefine contributors (asal Google Refine) | 12.020 bintang / 2.174 fork, sejak 2012, aktif (Okt 2026); dipakai pustakawan/jurnalis/peneliti; 5 sinyal | BSD-3-Clause (LICENSE.txt) | Ambil **gagasan** (clustering nilai mirip, alur lihat-kelompokkan-putuskan-terapkan). Kode tidak dibaca/disalin. |
| Docs OpenRefine "Cell editing: cluster and edit" | https://openrefine.org/docs/manual/cellediting | OpenRefine | dokumentasi resmi | (docs tidak disalin) | Dibaca 2026-10-05 hanya untuk memahami metode. |
| Data Carpentry: Data Organization in Spreadsheets | https://datacarpentry.org/spreadsheet-ecology-lesson/ (dibaca via datacarpentry.github.io/spreadsheet-ecology-lesson/01-format-data.html) | The Carpentries | ratusan fork, 710 commit, aktif (Sep 2026); 3 sinyal | CC BY 4.0 (halaman: "licensed under CC-BY 4.0 by The Carpentries") | Adaptasi prinsip tabel rapi ke Bahasa Indonesia dengan atribusi dan pernyataan perubahan. |

## Yang dipelajari (ide, bukan kutipan)
- OpenRefine: (a) kunci tabrakan "sidik jari" (huruf kecil, buang tanda baca/aksen, urut kata unik) untuk menangkap beda urutan/spasi; (b) sidik jari n-gram untuk salah ketik/spasi; (c) kemiripan jarak (Levenshtein/PPM) lebih lambat, makin permisif makin perlu tinjauan manusia; (d) penggabungan hanya setelah disetujui pengguna.
- Data Carpentry: variabel di kolom, observasi di baris, satu informasi per sel, simpan data mentah, ekspor ke teks (CSV), struktur konsisten.

## Audit keamanan (Tahap 3)
Hanya halaman dokumentasi yang dibaca. Tidak ada clone, tidak ada kode sumber dijalankan. Diperiksa instruksi tersembunyi, perintah unduh-jalankan, kiriman data keluar, kredensial: nihil. **Lolos.**

## Nilai tambah Komunitech (wajib ATM)
Seluruhnya baru: script `rapikan.py` (Python standar; `difflib`, `decimal`) untuk nomor HP Indonesia (08/62/+62/0062/nol hilang/notasi ilmiah Excel/telepon rumah/nomor ganda), tanggal Indonesia (nama bulan ID/EN, 2 digit tahun, nomor seri Excel, deteksi hari/bulan vs bulan/hari dari bukti kolom, tanggal fiktif), rupiah (Rp, `,-`, rb/jt/juta, titik ribuan vs koma desimal, pembulatan setengah naik sesuai standar library), singkatan nama Indonesia (Muh./Muhammad, sapaan Bpk./Ibu/Mas/Hj., kota Jogja/Yogyakarta), duplikat sadar konteks (daftar vs transaksi), keputusan pengguna (`--gabung-kelompok`, `--nama-baku`, `--buang-duplikat-persis`), kolom `_catatan`, laporan JSON, 40 tes termasuk data rusak, contoh data fiktif, aturan privasi UU PDP dan penolakan scraping/penggabungan sumber lain, README penjualan.

## Lisensi turunan
- BSD-3: tidak ada kode/teks diturunkan, jadi tidak ada `LICENSE-BSD`; atribusi gagasan dicatat di `ATTRIBUTION.md`.
- CC BY 4.0: atribusi (pembuat, tautan, lisensi, "diubah/diadaptasi") di `ATTRIBUTION.md` dan `references/tabel-rapi.md`.
- Tidak ada klaim afiliasi/dukungan dari OpenRefine atau The Carpentries.

## PERLU REVIEW / catatan jujur untuk penguji
- Nama mirip adalah heuristik: ambang kemiripan 0,86 dan panjang minimal 5 karakter; "Ani/Anis" sengaja tidak dikelompokkan. Uji dengan data nama nyata beragam (nama Jawa/Sunda/Batak/Tionghoa) untuk melihat salah-gabung/terlewat.
- Pelipatan singkatan hanya daftar kecil (Muh/Moh/Mhd/Mohammad..., Jl, Jogja, Jkt, dst.). Variasi lain tidak terdeteksi.
- Nomor telepon tetap (021...) diterima apa adanya dengan catatan; tidak divalidasi per kode area.
- Tanggal dua digit tahun: 00-69 jadi 2000-an. Tanggal ambigu dibaca hari/bulan.
- Waktu proses 20.000 baris dengan ±4.000 nama unik sekitar 10 detik.
