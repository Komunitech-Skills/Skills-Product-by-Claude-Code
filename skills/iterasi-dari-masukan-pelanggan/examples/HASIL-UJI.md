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

---
## Catatan revisi 1.0.1 (pembuat, 2026-09-29) - teks penguji di atas TIDAK diubah
Status tetap `uji`, skor tetap 6 sampai diuji ulang oleh penguji independen. Versi katalog 1.0.1.

### Tindak lanjut 15 permintaan
| # | Perbaikan | Tes regresi (`scripts/uji_olah_masukan.py`) |
|---|---|---|
| 1 | Kolom teks dipilih per kata judul (bukan substring): "Ulasan Pembeli", "Komentar User", "Isi Ulasan", "Review Content", "Ulasan" terbaca; "Waktu Ulasan", "Foto Ulasan", "No. Pesanan" (kata penghalang) dan "Balasan Penjual" (suara penjual) dilewati; kolom yang isinya > 50% tanggal/angka/kode tidak dipakai. Tanpa kolom teks -> `GAGAL` + daftar kolom, kode 2 | `UjiKolom` (Shopee, Tokopedia, TikTok Shop, Google Form, tanpa kolom teks, kolom paksa tidak ada) |
| 2 | Baris `Sumber` menyebut kolom teks/nilai/skala/tanggal per CSV; `PERINGATAN` bila kolom paksa berisi tanggal/angka atau > 30% baris terlalu pendek (menyebut kolom yang dipakai) | `test_kolom_paksa_berisi_tanggal...`, `test_banyak_baris_pendek...` |
| 3 | Nilai dibaca utuh (4,5; 8/10; ★★★). Skala 0-10 dari judul ("0-10", NPS, rekomendasi) atau isi (> 5 atau ada 0) -> promotor/pasif/detraktor + NPS per responden; skala ragu (judul "Nilai/Skor", isi 1-5) -> peringatan + `--skala 5/10` | `UjiSkala` (5 tes) |
| 4 | "kurang (begitu) + kata" = keluhan (bobot -2); "tidak/nggak/gak/ga/gk + positif" = keluhan; "pas" dihapus dari kata positif (hanya "pas banget/di badan/ukurannya pas"); "tidak + aksi" (datang, dibalas, berfungsi) = keluhan; kata_negatif kustom tetap keluhan walau dinegasi; kalimat tanya tidak dihitung pujian; negasi hanya berlaku untuk kata tepat sesudahnya | `UjiNegasi` (8 tes) |
| 5 | Duplikat hanya bila baris identik: pembeli/pesanan (atau seluruh baris bila tanpa kolom identitas) + nilai + teks; WA: pengirim + tanggal + teks. Teks tempelan tidak dibuang; teks sama dari orang berbeda dihitung + peringatan; `--buang-teks-sama` opsional | `UjiDuplikat` (4 tes) |
| 6 | Tema bawaan baru: Tempat/fasilitas, Waktu tunggu/antrean, Bau/aroma, Kebersihan (dampak 3) dipisah dari Keamanan produk (dampak 5). "rapi" keluar dari Kemasan, "dingin/hangat" keluar dari Pengiriman, "paket" keluar dari Varian, "komplain"/"kasar" keluar dari Layanan; "warna" masuk Kualitas; "kurang 1/satu" & "yg datang cuma 2" -> Ketepatan pesanan; "restock" -> Stok. Template baru `tema-fashion.json`, `tema-kafe.json`, `tema-laundry-jasa.json` | `UjiTema`, `test_semua_template_tema_valid` |
| 7 | `tambah_kata` (menambah kata ke tema bawaan), `hapus_tema`, penjelasan "id sama = mengganti" di SKILL.md & `_petunjuk` template; kata tema.json ikut dinormalkan ("dibales" = "dibalas"); peringatan otomatis bila dua tema menghitung keluhan yang sama (dobel) | `test_tambah_kata...`, `test_id_sama_mengganti...`, `test_peringatan_tema_dobel` |
| 8 | `GAGAL: ...` + kode 2 (tanpa traceback) untuk berkas/tema tidak ada, folder, biner, CSV rusak, tanda kutip tidak seimbang, JSON tema rusak/salah bentuk, gagal menulis `--simpan-anonim`. BOM UTF-8/UTF-16 LE/BE dan UTF-16 tanpa BOM dikenali; UTF-8 campur didekode per baris (emoji di baris lain utuh) + peringatan | `UjiBerkasRusak` (7 tes) |
| 9 | Tren: "keluhan terlalu sedikit" bila < 3 keluhan di dua bulan terakhir; "indikatif: data kecil" bila total < 30 atau < 10 per bulan; catatan "Data < 30" di output | `test_tren_indikatif_dan_keluhan_sedikit` |
| 10 | "Perlu dibaca agent" menampilkan hingga 20 + "+N lainnya"; JSON memuat semuanya | `test_perlu_dibaca_agent_tampil_semua` |
| 11 | Kolom survei judul bebas: diterima bila berupa pertanyaan ("?", apa/ingin/perlu...) walau jawabannya pendek; "-", "tidak ada" dihitung "jawaban kosong"; kolom permintaan ("ingin ditambah") = saran, tema dari judul kolom, 1 kata boleh; nilai baris tidak dipakai menebak keluhan di kolom permintaan | `test_google_form_jawaban_pendek_dan_strip` |
| 12 | Penyamaran: "makasih kak rina"/"kak rina," (huruf kecil di akhir frasa), nama dua kata, "a.n./atas nama", "Saya/nama saya Nama", telepon rumah (021/022), Perum/Griya/Komplek/Blok/RT/RW/Kav, plat nomor, "Pak RT Joko" | `UjiPenyamaranLanjut` |
| 13 | Token nama pengirim tanpa sapaan/gelar ("Kak Yanti" -> "Yanti"), kata umum tidak dijadikan nama | `test_nama_pengirim_bersapaan` |
| 14 | ATTRIBUTION.md: "Kedua lisensi" | - |
| 15 | Rujukan `analisis-ulasan`, `balas-ulasan-pelanggan`, `balas-chat-cs` diberi "bila terpasang; bila tidak, ..." (SKILL.md, description, template balasan) | - |

Tambahan SKILL.md: script = saringan pertama; agent wajib membaca setiap masukan di CSV anonim (≤ 150; lebih dari itu: semua keluhan 5 tema teratas + ≥ 30 acak + semua tanpa tema), membaca kutipan **setiap** tema, mengoreksi lewat tema.json, dan mencatat koreksi. Checklist ditambah cek PERINGATAN/kolom/skala.

### Recall keluhan (sebelum v1.0.0 -> sesudah v1.0.1)
Set berlabel di scratchpad `revisi-iterasi/label.py` & `label_baru.py`, pengukur `ukur.py`. "Recall item" = masukan keluhan yang ditandai keluhan;
"recall tema" = pasangan (masukan, tema benar) yang ditandai keluhan (label memakai id tema v1.0.1, jadi v1.0.0 juga dirugikan oleh tema
yang belum ada). Nilai bintang/0-10 dipakai seperti di berkas aslinya.

| Set | n (keluhan) | Recall item | Recall tema | Keluhan palsu |
|---|---|---|---|---|
| A. Data penguji s06+s07+s08, dilabel ulang per baris oleh pembuat (jumlah per tema sama dengan tabel penguji) | 75 (51) | 59% -> **100%** | 36% -> **98%** | 0/24 -> 0/24 |
| B. Set tahan buatan pembuat, ditulis SEBELUM kode diubah (tetapi pembuat yang sama menyusun kamus - bukan uji buta) | 60 (41) | 63% -> **100%** | 51% -> **100%** | 1/19 -> 0/19 |
| C. Set baru, ditulis SETELAH penyetelan selesai, diukur sekali, tidak dipakai menyetel | 40 (29) | 62% -> **83%** | 45% -> **79%** | 0/11 -> 1/11 |
| A+B tanpa bintang (teks saja) | 135 (92) | 41% -> **98%** | 29% -> **97%** | 1/43 -> 0/43 |

Angka A dan B **terlalu optimistis** (kamus disetel dengan melihat data itu). Angka jujur untuk data baru adalah set C (~80%). Karena itu
verifikasi agent tetap wajib. Kasus yang masih lolos: typo substitusi ("hamber", "ramh" - sengaja tidak dikoreksi karena di korpus repo
±18.100 kata unik, koreksi substitusi mengubah 328 kata, kebanyakan kata umum yang benar, mis. "tanggal"->"tanggap", "benar"->"besar"; kini hanya huruf berulang dan satu
huruf hilang pada kata >= 6 huruf; di korpus yang sama tinggal 8 perubahan, semuanya wajar mis. "paking"->"packing"), kalimat yang keluhannya tersirat ("pesan navy dateng hitam"),
dan satu keluhan yang tercatat di tema tetangga ("restock ... udh nunggu lama" -> Waktu tunggu, bukan Stok).

### Jalan ulang skenario penguji (perintah persis SKILL.md, tanpa --kolom-*)
- 06: kolom "Ulasan Pembeli"/"Rating"/"Waktu Ulasan" terpilih otomatis; 34 masukan (Shopee 20 - dua "Barang sesuai pesanan" dihitung +
  peringatan), tanpa tanggal di kutipan. `verifikasi.py` penguji: OK (n=34).
- 07: skala 0-10 dikenali, NPS 12 responden (promotor 4, pasif 3, detraktor 5 -> -8,3, indikatif); kolom menu terbaca sebagai saran
  (Varian 8 saran, 0 keluhan); Tempat/fasilitas = isu #1 (10 keluhan); "kurang bersih" = keluhan Kebersihan. `verifikasi.py`: OK (n=30;
  "perfect" nilai 10 kini dihitung karena ulasan 1 kata dengan nilai tidak dibuang).
- 08: "kurang ramah" = keluhan Layanan, "kurang 1 kaos kaki" = Ketepatan pesanan, "bau apek" hanya di Bau/aroma (tidak dobel dengan Keamanan);
  dengan tema.json penguji muncul peringatan dobel "Bau apek" vs "Bau / aroma". `verifikasi.py`: angka cocok; satu-satunya selisih
  "jenis pembayaran" = tema yang hanya disebut netral ("kirim invoice"), memang disengaja (tema disebut tanpa keluhan/pujian/saran).
- 09: semua kasus berkas rusak -> `GAGAL` kode 2; UTF-16 terbaca benar; 3x "roti enak" = pujian rasa 3; `wa-campur.txt` emoji/kutip aman.

### Lain-lain
- Contoh 01 & data `examples/data/anonim-2026-09.csv` dibuat ulang dengan v1.0.1 (Pengiriman 11 -> 9 keluhan: "salah kirim" dan "lauk dingin"
  tidak lagi dobel/salah tema); angka di SKILL.md, README, dan contoh 02 disesuaikan. Contoh 06-10 dan 00-* (milik penguji) tidak diubah.
- Tes: 21 -> 66 (lulus di Python 3.10, 3.11, 3.12, 3.13). `python3 scripts/validate.py --skill iterasi-dari-masukan-pelanggan`: valid.
  Kinerja: 5.000 baris CSV ~1,2 detik.
- Mohon uji ulang independen (disarankan dengan set berlabel baru yang tidak dilihat pembuat).
