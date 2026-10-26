# Hasil Uji — perjanjian-sederhana (kandidat VIP)

- **Tanggal:** 2026-09-23
- **Penguji:** agent penguji independen (simulasi, Claude Code)
- **Versi yang diuji:** SKILL.md, README.md, ATTRIBUTION.md, `references/` (batasan-rujukan, checklist-tanda-tangan, klausul-pilihan, regulasi), 7 template di `templates/`, `scripts/perjanjian.py`
- **Metode:** 5 skenario (01–05, dengan S5 berisi dua kasus: jual beli tanah & investasi) + uji A/B (00-pembanding) + uji banding pesaing (00-banding). Script dijalankan sungguhan di `/tmp/uji-perjanjian-sederhana/`. Angka diverifikasi dengan implementasi terbilang independen dan `date` sistem.

## Audit keamanan
- `perjanjian.py` hanya memakai `argparse, json, os, re, sys, datetime, decimal`. Tidak ada jaringan/subprocess/eval, tidak menulis/menghapus file, dan tidak membaca kredensial. `cek` hanya membaca file draf yang disebut.
- SKILL.md/README/references/template: tidak ada prompt injection. Blok PANDUAN AGENT berupa komentar HTML berisi instruksi yang wajar (dan diabaikan oleh `cek`). Ada instruksi menjaga data pribadi (NIK, alamat) sesuai UU PDP.
- **Aman.**

## Verifikasi angka & fakta (independen)
| Uji | Hasil |
|---|---|
| Terbilang: 20.048 angka (daftar tepi 0, 1, 10–19, 100, 101, 110, 1.000, 1.001, 1.100, 1.999, 1.001.000, 101.101.101, 10¹², 10¹²+1 + 20.000 acak s.d. 10¹³) dibandingkan dengan implementasi penguji | **0 perbedaan** ✔ |
| Nominal: `Rp 7.500.000`, `1.500.000,50` (→ "… rupiah lima puluh sen"), `1,5jt`, `2 miliar`, `15.000,-`, `0`; `-5000`, `5m` (ambigu), `abc` ditolak dengan pesan jelas | ✔ |
| Tanggal pembuka: Rabu 23-09-2026, Kamis 01-10-2026, Senin 05-10-2026 (cek `date`); `31/02/2026` ditolak | ✔ |
| Termin: 10.000.001 × 33/33/34 (sisa ke termin terakhir, total cocok); `33,3;33,3;33,4`; persen ≠ 100% ditolak | ✔ |
| Bagi hasil 60/40 dari Rp 12.345.679 → 7.407.407 + 4.938.272; peringatan dasar omzet | ✔ |
| Denda 0,1%/hari × 30 hari × 5 jt = 150.000, batas 5% = 250.000; tanpa batas → peringatan; > 10% → peringatan | ✔ |
| Meterai: perjanjian 2/3 rangkap; kuitansi 5.000.000 tidak wajib, 5.000.001 wajib (UU 10/2020) | ✔ |
| `cek`: terbilang salah ("lima juta ribu rupiah") terdeteksi; penomoran pasal loncat terdeteksi; nilai ≥ Rp500 jt → RUJUK; file kosong/.docx → GALAT | ✔ |
| `cek` pada draf berisiko: "PERJANJIAN INVESTASI … keuntungan 5% per bulan", "PENGIKATAN JUAL BELI KAVLING … SHM", "pinjam … bunga 3% … BPKB sebagai jaminan", klausul harga jual minimum + denda | **Tidak satu pun ditandai RUJUK PROFESIONAL** (lihat S1) |

## Pemeriksaan khusus (brief)
- **Pasal wajib lengkap** di semua template yang diuji (reseller, sewa tempat, jasa freelance): para pihak, latar belakang, ruang lingkup, hak & kewajiban dua pihak, harga & pembayaran, jangka waktu, wanprestasi, keadaan memaksa, sengketa, lain-lain, tanda tangan + meterai, lampiran ✔.
- **Syarat sah 1320 KUHPerdata** dijelaskan benar (subjektif = dapat dibatalkan, objektif = batal demi hukum) dan wajib ditampilkan per draf ✔.
- **Catatan meterai** benar: Rp10.000, berapa pun nilainya, per rangkap, bukan syarat sah, pemeteraian kemudian, kuitansi > Rp5 juta ✔.
- **Rujukan profesional** untuk tanah (PP 24/1997 Ps. 37/PPAT), investasi/imbal hasil pasti/banyak investor (OJK), pihak asing (UU 24/2009 Ps. 31), jaminan, perjanjian kerja, waralaba, pemerintah, sengketa berjalan ✔ (S5a, S5b).
- **Klausul MAP/harga jual kembali di template reseller:** template memakai "harga jual yang disarankan" dan memberi ⚠ dengan rujukan **UU 5/1999**; `references/regulasi.md` §5 menyebut Pasal 8. Saat pengguna meminta harga minimum wajib + denda, agent menolak memasukkannya dan memberi alternatif sah ✔ (S1).
- Klausul lain yang rawan sudah ditandai: pengesampingan Ps. 1266–1267 ("masih diperdebatkan"), arbitrase (PN tidak berwenang), non-compete, pengosongan tanpa putusan pengadilan, denda tanpa batas ✔. Tidak ditemukan klausul yang jelas melanggar hukum di ketujuh template.

## Skor
| Kriteria | Skor (1–10) | Alasan singkat |
|---|---|---|
| Pemicu (description tepat) | 9 | Jenis perjanjian, "kontrak/MoU/NDA", dan pengecualian (tanah, investasi, asing, karyawan) jelas di description. |
| Kemudahan awam | 9 | Satu kalimat cukup; `[[...]]` + daftar kekurangan; checklist bahasa awam; posisi pengguna disebut. |
| Kualitas output | 9 | Draf lengkap, seimbang, pasal ⚠ dirangkum, 1320, checklist, meterai, disclaimer. A/B dan pesaing jelas kalah. |
| Akurasi (angka/fakta) | 9 | Terbilang 0 salah dari 20.048 angka; dasar hukum tepat dan bertanggal. Tanggal berakhir masih dihitung manual. |
| Penanganan input kurang | 9 | Tanya sekali dengan pilihan (S4); jalur cepat dengan asumsi (S3). |
| Penanganan di luar cakupan | 8 | Penolakan & rujukan sangat baik (S5a/S5b), tetapi jaring pengaman otomatis `cek` bolong untuk investasi/kavling/jaminan/MAP. |
| Keamanan | 10 | Lokal, tanpa jaringan; perlindungan data pribadi diingatkan. |

## SKOR AKHIR: 8 / 10 → **LULUS**

Kualitas draf, keseimbangan klausul, dan penanganan kasus berisiko sudah setara standar VIP. Uji A/B menunjukkan nilai tambah paling besar justru di bagian yang paling penting: skill **mencegah** klausul harga jual kembali minimum yang diminta pengguna, sedangkan agent tanpa skill menuliskannya. Skill juga menang telak atas pesaing Indonesia (`spk-generator`). Nilai tidak 9 karena fungsi `cek` (yang di SKILL.md langkah 5 dipakai sebagai pemeriksa sebelum kirim, dan diiklankan untuk "cek draf buatan sendiri") tidak mendeteksi kasus rujuk yang paling umum.

## Daftar cacat & saran perbaikan

### Berat
- Tidak ada.

### Sedang
- **S1 — Deteksi risiko `cek` terlalu sempit** (`perjanjian.py` baris 325–337, `POLA_BAHAYA`). Lolos tanpa tanda: kata **"investasi"/"dana investasi"/"keuntungan 5% per bulan"** (pola hanya `investor`, `imbal hasil tetap|pasti`, `keuntungan tetap|pasti`); **"pengikatan jual beli"/PPJB/"kavling"/SHM dalam konteks jual beli** (pola mensyaratkan kata tanah/rumah/bangunan/apartemen/ruko ≤ 60 karakter setelah "jual beli"); **BPKB, "sebagai jaminan", "bunga x% per bulan"** (pola hanya "jaminan fidusia/sertifikat", "hak tanggungan", "gadai", "agunan"); **harga jual kembali minimum** ("harga minimum/minimal", "tidak boleh menjual di bawah", "banting harga"). Ini penting untuk use case README "Tolong cek draf perjanjian ini".
  *Saran:* perluas pola: investasi → `\binvestasi\b|keuntungan \d+([.,]\d+)? ?% ?(per|/) ?bulan|bagi hasil tetap|modal (kembali|balik) (utuh|penuh)`; tanah → `\bppjb\b|pengikatan jual beli|\bkavling\b|jual beli[^.\n]{0,80}\b(shm|sertifikat|kavling|lahan)\b`; jaminan/bunga → `\bbpkb\b|sebagai jaminan|\bbunga\b[^.\n]{0,20}\d+ ?%`; MAP (kategori baru "Tinjau: UU 5/1999 Ps. 8") → `harga (jual )?(minimum|minimal|terendah)|(dilarang|tidak boleh) menjual[^.\n]{0,30}(di bawah|lebih murah)|banting harga`. Tambahkan kasus uji dari `05-…` dan `01-…` ke tes internal.

### Ringan
- Tidak ada subperintah penghitung tanggal berakhir/jatuh tempo (mis. `perjanjian.py sampai 2026-10-01 --bulan 12` → 30 September 2027). Saat ini agent menghitung manual di tiap draf (S1, S2, S3).
- `jasa-freelance.md` PANDUAN AGENT: default "50% di muka, 50% setelah selesai" kurang cocok untuk kontrak berulang > 1 bulan. Sarankan termin bulanan.
- `sewa-tempat.md` PANDUAN AGENT: tambahkan peringatan untuk kios pasar/mal yang berstatus **hak pakai/sewa dari pengelola** (perlu izin pengelola untuk menyewakan ulang). Kasus ini sangat umum.
- `meterai --jenis kwitansi` memakai default `--rangkap 2`, jadi kuitansi wajib meterai tercetak "2 lembar". Kuitansi biasanya satu lembar asli. Default untuk kuitansi sebaiknya 1.
- `terbilang "2,5"` menghasilkan "Rp 2,50 (dua rupiah lima puluh sen)". Pengguna yang lupa satuan "jt" tidak diperingatkan. Beri peringatan bila nominal < Rp 1.000 atau mengandung sen.
- README menyebut `CARA-INSTAL.md` yang tidak ada di folder skill. Pastikan ikut di paket.

## Ringkasan uji tambahan
- **A/B (00-pembanding-tanpa-skill.md):** tanpa skill, agent menulis klausul harga jual minimum + denda Rp 5 juta + pemutusan sepihak, tanpa retur/kerahasiaan/checklist, dengan ejaan "materai". Skill **jelas lebih baik**.
- **Pesaing (00-banding-pesaing.md):** `adamriofc/spk-generator` (MIT) hanya 4 pasal inti, ikut menulis klausul MAP, dan menjadikan pengesampingan Ps. 1266 "wajib" tanpa catatan. Skill kita **menang** di semua kriteria. Ide yang bisa dipelajari: BAST sebagai syarat pelunasan, teguran bertahap, pertanyaan eksplisit status PPN/PPh 23.

## Uji ulang OpenClaw v1.0.6 (2026-10-03)
- Penguji independen, OpenClaw 2026.9.6 lokal, model router Komunitech claude-sonnet-5, home bersih per skenario; rincian di `00-openclaw-sebelum-sesudah.md` bagian "Uji ulang v1.0.6".
- Skor sebelum → sesudah: sewa kios 5,5 → 9; jebakan utang + BPKB 3 → 9; varian titip jual (sesudah saja) 9. Rata-rata berpasangan 4,25 → 9,0 (selisih +4,75).
- Tiga cacat tampilan Telegram gelombang 5 sudah teratasi: naskah utuh tampil di chat (dipecah Bagian 1/4–4/4), beban biaya (PBB pemilik; listrik/air/iuran pasar penyewa) konsisten antar pasal & asumsi, pengakhiran bertahap tanpa pengosongan sepihak. Disclaimer ada; angka sewa, jaminan, dan jadwal bayar terverifikasi Python.
- **VERDIK: LULUS** (acuan pemilik 2026-10-03: sesudah ≥ 8, selisih ≥ 1,5). Cacat tersisa minor: "pemilik sah" di latar belakang saat status hak kios belum diketahui, satu butir checklist meterai kurang jelas, satu bagian chat ±4.090 karakter.

## Catatan revisi 1.0.9 (2026-10-26)
- Pemicu: pra-cek konteks Telegram Akun A 21 Okt 2026 (v1.0.8) skor 7,5 TIDAK SIAP. Isi dan angka benar; yang gagal hanya cara kirim di chat: jalur berkas disebut, kata "script" muncul, naskah 13.664 karakter dalam satu blok kode, dua gaya isian.
- Perbaikan: larangan jalur berkas (kalimat baku "Balas 'kirim file'"), larangan kata script/skrip/tool/exec/python, naskah teks biasa per "Bagian 1/N" < 3.800 karakter dipotong antar-pasal (perintah `bagi`), pemeriksa balasan (`cek-balasan`), satu gaya isian `[isi: ...]`. Isi pasal/angka tidak berubah.
- Uji: `scripts/uji_regresi.py` lulus (termasuk uji baru untuk tiap aturan; `bagi` diuji pada ketujuh template: tiap bagian ≤ 3.800, label urut, potongan selalu di awal pasal/lampiran/penutup, jumlah pasal, ayat, dan nominal tetap sama). Skor 8 di atas tetap; belum diuji ulang di bot Telegram asli maupun `uji-tg.sh`.
