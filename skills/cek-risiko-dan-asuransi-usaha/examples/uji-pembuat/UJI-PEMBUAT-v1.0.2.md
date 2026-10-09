# Catatan pembuat v1.0.2 (2026-10-09)

Berdasarkan `HASIL-UJI-uji-ulang-v1.0.1.md`. Bukan uji independen; uji ulang oleh penguji terpisah.

| ID | Perbaikan | Bukti |
|---|---|---|
| R1 | `kategori: "bpjs"` (atau nama jelas soal karyawan cedera/sakit/kecelakaan kerja, dikenali otomatis; korban pelanggan, pemilik, dan orang kunci yang keluar dikecualikan; `"umum"` mematikan) membuat script mencetak label BPJS + respons K3. SKILL.md langkah 4 dan aturan agent menyuruh menyalin, tidak menimpa. | Data uji 01, 02, 06, 07, 08, 09 kini otomatis berlabel BPJS; "Pemilik sakit", "Mekanik senior keluar/sakit", "Pelanggan terpeleset" tidak. Tes baru. |
| R2 | Tanggung gugat profesi, kerusakan mesin/peralatan, barang titipan pelanggan ditambah di `references/jenis-perlindungan.md`, `peta-risiko.md`, template pertanyaan butir 9. Tanpa merek/premi/angka. | PERLU REVIEW tenaga asuransi (ditandai di rujukan). |
| R3 | "agen berizin OJK" diganti: perusahaan berizin usaha OJK; agen terdaftar (lewat AAJI/AAUI/AASI, bersertifikasi, POJK 23/2023). | Sumber berupa pemberitaan (pejabat OJK 26-2-2024; investortrust 13-8-2026). Naskah POJK di jdih.ojk.go.id belum dibuka: tercatat di rujukan. |
| R4 | JKP ditambah (SKILL.md langkah 7, rujukan, peta risiko). | PP 37/2021 Pasal 1 dan 4 dibaca langsung dari PDF; situs BPJS TK (17-12-2025) menyebut 5 program. |
| R5 | Urutan: keberatan tertulis ke perusahaan, Kontak OJK 157 (157, WA 081157157157, konsumen@ojk.go.id, kontak157.ojk.go.id), LAPS SJK (lapssjk.id); sebut `laporan-insiden-usaha`. | Siaran pers OJK 6-1-2023 dan lapssjk.id, diakses 2026-10-09. Nomor bisa berubah; ditulis "per 2026-10-09". Syarat pengajuan LAPS tidak dipastikan, jadi disuruh cek di situs. |
| R6 | (a) "cukup X bulan" setengah-ke-atas murni integer; (b) kas cukup: tidak ada baris "Rp0 per bulan"; (c) nama biaya kosong ditolak; (d) BOM diterima (`utf-8-sig`); (e) `|` dan baris baru di nama diganti; (f) `3.000.000,00` kini pesan "koma memisahkan biaya". | 7 tes baru. |
| R7 | README "Sebelum / sesudah" diisi dari A/B skenario 1 (6 ke 8,5), tanpa angka karangan. | |
| R8 | Dana darurat jadi langkah 3, hitung risiko langkah 4 (pakai `--dana`). | |

Tes: `python3 skills/cek-risiko-dan-asuransi-usaha/tests/uji_regresi.py` = 23 tes OK (16 lama + 7 baru). Contoh uji lama (`examples/01`-`10`) tidak diubah; keluarannya ditulis oleh penguji pada v1.0.0/1.0.1 dan kolom BPJS-nya sekarang akan berbeda bila dijalankan ulang.
