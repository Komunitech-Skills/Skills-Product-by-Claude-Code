# Hasil Uji Independen - iterasi-dari-masukan-pelanggan v1.0.0
Penguji: agent terpisah dari pembuat (hanya membaca folder skill + CLAUDE.md), 2026-09-29. Platform: `claude-code (simulasi agent)`.
Contoh 01-05 dari pembuat dipertahankan; uji penguji = 06-10, 00-pembanding-tanpa-skill, 00-banding-pesaing.

## 1. Audit keamanan & format
| Butir | Hasil |
|---|---|
| Frontmatter hanya `name` + `description`, name = folder, satu baris, < 1024 karakter | Lulus |
| Script: hanya pustaka standar (argparse, csv, io, json, re, sys, collections; uji: os, tempfile, unittest), tanpa jaringan/subprocess/eval, tidak menulis selain `--simpan-anonim` | Lulus |
| Prompt injection / perintah tersembunyi / kredensial tertanam | Tidak ditemukan |
| Lisensi MIT phuryn: teks identik dengan `LICENSE` upstream (diff) | Lulus |
| Lisensi Apache-2.0 product-on-purpose: teks identik dengan upstream (diff); upstream memang tanpa NOTICE (dicek di clone); NOTICE lokal + keterangan perubahan 4(b) ada | Lulus |
| ATTRIBUTION.md | Lulus, typo: "Ketiga lisensi di atas (MIT dan Apache-2.0)" -> seharusnya "Kedua" |
| `python3 scripts/validate.py --skill iterasi-dari-masukan-pelanggan` | ✅ 1 skill valid |
| `scripts/uji_olah_masukan.py` | 21 tes OK |
| Hitungan (total, kanal, sentimen, bulan, skor, persen, prioritas, tren, urutan) diverifikasi independen dari CSV anonim + JSON | Cocok di semua jalan (06, 07, 08, data contoh n=51) |

## 2. Skenario
| # | Skenario | Nilai | Catatan utama |
|---|---|---|---|
| 06 | Toko hijab: Shopee CSV + WA Android + IG | 5 | CSV berjudul `Ulasan Pembeli`/`Waktu Ulasan`/`No. Pesanan` -> kolom salah dipilih, 20 ulasan tidak terbaca, exit 0. Recall keluhan 52% |
| 07 | Kedai kopi: Google Form cp1252 `;` + Google Maps tempelan | 5 | Nilai 0-10 dibaca sebagai bintang (10 -> 1); "kurang bersih" = pujian; kolom permintaan menu hilang; tidak ada tema fasilitas/antrean |
| 08 | Laundry: WA iOS 2 bulan + tema.json | 7 | Baik dengan tema.json; bau apek dobel di "Keamanan pangan"; "kurang ramah" = pujian |
| 09 | Input kurang + data rusak/encoding | 6 | Alur tanya/`<8 masukan` baik; traceback (file hilang, biner, JSON rusak); UTF-16 jadi sampah diam-diam; duplikat asli terbuang |
| 10 | Di luar cakupan | 9 | Semua penolakan & rujukan tepat |
| A/B | Tanpa vs dengan skill | Dengan skill jelas lebih baik | Unggul di privasi, backlog, balasan, siklus; bukan di akurasi tema |
| Pesaing | phuryn sentiment-analysis | Skill kita menang (33 vs 15) | Pesaing lebih tahan slang karena LLM membaca langsung |

## 3. Skor kualitas: **6/10 - BELUM LULUS (revisi, lalu uji ulang independen)**
Alasan: alur SKILL.md, privasi, template, siklus bulanan, dan materi README sangat baik (A/B dan pesaing menang). Namun prinsip "reliable"
CLAUDE.md dilanggar oleh script: input paling umum (ekspor ulasan marketplace dengan kolom "Ulasan Pembeli") gagal **diam-diam**, skala nilai
survei 0-10 membalik sentimen, dan pola sangat umum "kurang + kata positif" serta "pas" (= ketika) mengubah keluhan menjadi pujian. Angka yang
dihitung benar tapi dari klasifikasi yang salah tetap menyesatkan pembeli awam.

## 4. Permintaan perbaikan (penguji tidak mengubah skill)
**Kritis**
1. `pilih_kolom`: jangan buang kolom teks hanya karena mengandung "pembeli/user/nama" bila juga mengandung ulasan/review/komentar
   (mis. "Ulasan Pembeli", "Komentar User"); utamakan kecocokan persis & kandidat teks sebelum substring; jangan pilih kolom yang nilainya
   mayoritas tanggal/angka/kode ("Waktu Ulasan", "No. Pesanan") sebagai teks. Tambah tes untuk header ekspor Shopee/Tokopedia/TikTok Shop/Google Form.
2. Peringatan wajib bila kolom teks yang dipilih berisi > 50% tanggal/angka/kode atau bila banyak baris jadi "terlalu pendek" (sebut kolom yang dipakai di output).
3. Kolom nilai: kenali skala 0-10 (ambil angka utuh, deteksi maks > 5), petakan ke promotor/pasif/detraktor atau skala 1-5; jangan `re.search("[1-5]")`.
4. Sentimen: perlakukan "kurang" (dan "kurang begitu", "kurang terlalu") sebagai penegasi bagi kata positif; hapus "pas" dari kata positif
   (atau hanya bila berdiri sebagai "pas banget/pas di badan"); negasi atas kata keluhan kustom ("ga dibales") jangan jadi positif.
**Penting**
5. Duplikat: hanya buang bila baris identik termasuk tanggal/bintang/pengirim, atau jadikan opsi `--buang-duplikat`; ulasan pendek sama dari pembeli berbeda harus dihitung.
6. Tema bawaan: tambah "Tempat / fasilitas" (wifi, AC, parkir, toilet, colokan, musik) dan "Waktu tunggu / antrean"; ganti label "Keamanan pangan / kebersihan"
   menjadi netral usaha atau pisahkan "bau" non-makanan; keluarkan "rapi" dari Kemasan, "dingin/hangat" dari Pengiriman, "paket" dari Varian;
   tambah "warna" & "size/ukuran" untuk fashion; "kurang \d+" ke Ketepatan pesanan; "restock" ke Stok. Sediakan contoh tema.json per jenis usaha
   (fashion, kafe, laundry/jasa) di `templates/`.
7. Jelaskan di SKILL.md/template bahwa `id` tema yang sama **mengganti** kata bawaan (dan cara menambah kata tanpa mengganti).
8. Pesan jelas + exit 2 untuk file tidak ada, file biner/CSV rusak, JSON tema rusak (bukan traceback). Deteksi BOM UTF-16 (FF FE / FE FF) dan decode benar;
   untuk UTF-8 campur, decode per baris atau `errors="replace"` sebelum jatuh ke latin-1.
9. Tren: tampilkan "indikatif (data kecil)" bila total < 30 atau per bulan < 10; jangan tampilkan tren untuk tema dengan keluhan sangat sedikit (mis. 0 -> 2).
10. "Perlu dibaca agent": tampilkan semua (atau sebut "+N lainnya, lihat --format json").
11. Survei: jangan buang kolom teks jawaban pendek (permintaan menu); ambang panjang rata-rata 8 terlalu ketat bila banyak "-".
**Kecil**
12. Penyamaran: "kak rina" huruf kecil, nama dua kata setelah sapaan, "a.n. Nama", "Saya <Nama>", telepon rumah (021...), "Perum/Blok/RT/RW", plat nomor.
13. Nama pengirim berawalan sapaan ("Kak Yanti") membuat semua "kak" jadi "[nama]"; abaikan token sapaan saat membuat daftar nama.
14. ATTRIBUTION.md: "Ketiga lisensi" -> "Kedua lisensi".
15. Rujukan `analisis-ulasan`/`balas-ulasan-pelanggan`/`balas-chat-cs`: tambahkan "bila terpasang; bila tidak, ..." untuk pembeli eceran.

## 5. Kolom katalog yang disarankan
`skor_kualitas` = 6, `status` tetap `uji` (jangan `lulus`), `platform_teruji` = `claude-code (simulasi agent)` setelah revisi diuji ulang.
