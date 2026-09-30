# Hasil Uji Ulang Independen - iterasi-dari-masukan-pelanggan v1.0.1
Penguji ulang: agent terpisah (bukan pembuat, bukan penguji pertama), 2026-09-29. Hanya membaca folder skill + CLAUDE.md;
set berlabel pembuat di scratchpad TIDAK dibaca. Platform: `claude-code (simulasi agent)`.
Berkas bantu (data uji, pengukur): scratchpad `uji-ulang-iterasi/` (`label_penguji.py`, `ukur_penguji.py`, `negasi.py`, `kolom/`, `skala/`, `dup/`, `rusak/`, `s1`-`s4`).

## 1. Pemeriksaan dasar
| Butir | Hasil |
|---|---|
| `python3 scripts/validate.py --skill iterasi-dari-masukan-pelanggan` | ✅ 1 skill valid |
| `scripts/uji_olah_masukan.py` | 66 tes OK |
| Audit script: hanya pustaka standar (argparse, csv, io, json, os, re, sys, collections), tanpa jaringan/subprocess/eval; hanya menulis `--simpan-anonim` | Lulus |
| Frontmatter 2 field, rujukan "bila terpasang" (#15), ATTRIBUTION "Kedua lisensi" (#14), template tema fashion/kafe/laundry (#6) | Lulus |
| SKILL.md menyuruh agent memverifikasi **setiap** tema sendiri | **Ya**: langkah 4 ("script hanya saringan pertama"; baca setiap masukan bila ≤ 150; baca kutipan setiap tema, bukan hanya 3 teratas; koreksi lewat tema.json atau koreksi manual bertanda) + checklist "Setiap tema sudah dibaca kutipannya". Celah kecil: CSV `--simpan-anonim` hanya berisi id tema tanpa jenis (keluhan/pujian), jadi agent perlu `--format json --contoh <besar>` untuk melihat baris mana yang dihitung keluhan per tema. |

## 2. Set berlabel baru (buta bagi pembuat)
103 baris masukan realistis (slang, typo, campur sentimen, sindiran, emoji; fashion, makanan, kafe, laundry, skincare; 72 keluhan / 31 bukan
keluhan; 78 pasangan keluhan-tema). Label ditulis sebelum menjalankan script dan tidak diubah sesudahnya. Pengukuran memakai jalur script yang sama
(`samarkan` -> `analisis_item`, tema bawaan, tanpa tema.json).

| Ukuran | Dengan bintang (bila ada) | Teks saja |
|---|---|---|
| Recall keluhan per baris (ada tema bertanda keluhan) | **75%** (54/72) | **72%** (52/72) |
| Presisi keluhan per baris | **98%** (54/55) | **98%** (52/53) |
| Keluhan palsu (baris bukan keluhan) | 1/31 | 1/31 |
| Recall per baris bila sentimen "negatif" juga dihitung | 82% | 79% |
| Recall per tema (pasangan keluhan-tema) | **69%** (54/78) | **68%** (53/78) |
| Presisi per tema | **83%** (57/69) | **85%** (56/66) |

Per tema (dengan bintang; tp/fn/fp -> recall, presisi): harga 5/0/0 100%/100%; layanan 7/0/0 100%/100%; keamanan 5/0/0 100%/100%;
bau 3/0/0 100%/100%; rasa 8/2/0 80%/100%; fasilitas 6/2/0 75%/100%; waktu tunggu 3/1/0 75%/100%; pembayaran 3/1/0 75%/100%;
porsi 3/1/1 75%/75%; kemasan 3/1/3 75%/50%; kebersihan 2/1/0 67%/100%; kualitas 9/6/2 60%/82%; varian 1/1/1 50%/50%;
**pengiriman 4/5/5 44%/44%**; **ketepatan pesanan 2/5/0 29%**; **stok 0/2/0 0%**.

Kesimpulan: presisi tinggi (hampir tidak ada keluhan palsu), recall script ±70-75% pada data yang belum pernah dilihat (set C pembuat: 83%/79%).
Tema paling lemah: pengiriman (sering tertangkap dari kata "dikirim/dateng" padahal isunya salah kirim/jumlah kurang), ketepatan pesanan
(keluhan tersirat: "pesen navy dikirim item", "3x pesen 3x salah", "pesen yg ga pedes dikasih yg pedes"), stok (pertanyaan "kapan restock?"
dianggap saran). Karena itu verifikasi agent di langkah 4 **mutlak** perlu; dengan ≤ 150 masukan agent membaca semuanya.

## 3. Verifikasi 15 permintaan perbaikan
| # | Hasil uji ulang |
|---|---|
| 1 Kolom teks | ✅ 12 varian judul ekspor benar semua: Shopee (`Ulasan`, `Ulasan Pembeli` + `Foto Ulasan`/`Waktu Ulasan`/`Balasan Penjual`, `Comment`/`Rating Star`/`Create Time`), Tokopedia (`Ulasan`, `Review`, `Isi Ulasan`), TikTok Shop (`Review Content`, `Review Text`), Lazada (`Content`/`Product Rating`, `Review Content`/`Reply Content`), Google Maps (`Review Text`/`Stars`), Google Form (judul pertanyaan). Balasan penjual, foto, nomor pesanan, nomor WA tidak pernah terbaca sebagai teks. |
| 2 Peringatan kolom | ✅ Baris `Sumber` menyebut kolom; tanpa kolom teks -> `GAGAL` + daftar kolom, kode 2. |
| 3 Skala 0-10 | ⚠️ Deteksi skala benar bila kolomnya ditemukan (`Nilai (0-10)`, `Skor` berisi 0-10, `8/10`, desimal `4,5`, `5 stars`, ⭐; `Skor` isi 1-5 -> peringatan "tidak pasti"; `Bintang` berisi 10 -> peringatan). **Tetapi kolom nilai hanya dikenali bila judulnya memuat rating/nilai/skor/bintang/nps.** Pertanyaan NPS Google Form yang lazim ("Seberapa besar kemungkinan Anda merekomendasikan ... ?"), `Kepuasan (1-10)`, `Tingkat kepuasan` **diabaikan diam-diam** (tanpa PERINGATAN; hanya terlihat "nilai: -" di baris Sumber). Dengan `--kolom-bintang` NPS benar (-21,4, dicek tangan). |
| 4 Negasi/ambigu | ✅ sebagian besar: "kurang bersih/ramah/begitu enak/nendang/cepat", "kurang 1 pcs", "gak enak", "gak telat", "ga pernah telat", "nggak ada kendala", "tidak mengecewakan", "ga dibales", "belum dateng", "pas nyampe masih anget", "pas dibuka ternyata sobek", "ukurannya pas", "tidak terlalu mahal". ❌ tersisa: **"pas dipake 2x udah melar" / "pas dipake langsung robek" = netral** (frasa "pas dipakai" masih dibaca pujian); "pas dateng udah dingin" = netral; "semoga lain kali gak telat" = **pujian** pengiriman; "ga bikin jerawatan" = **keluhan** (satu-satunya keluhan palsu); sindiran ("wah cepet banget ya, cuma seminggu 🙃") tidak terbaca (sudah diakui di Batasan). 29/40 frasa uji sesuai harapan. |
| 5 Duplikat | ✅ Baris identik (pembeli + pesanan + nilai + teks) dibuang; pembeli sama pesanan lain, pembeli lain teks sama, CSV tanpa kolom identitas (hanya baris identik), WA pengirim sama hari lain -> tetap dihitung + peringatan; teks tempelan tidak dibuang. Hanya pembeli yang sama yang digabung. |
| 6-7 Tema & tema.json | ✅ Tema fasilitas/antrean/bau/kebersihan ada; `tambah_kata`, `hapus_tema`, id salah -> `GAGAL` jelas. Catatan: `tema-laundry-jasa.json` (kata_negatif "noda", "hilang") membuat pujian "noda kopi ilang" dihitung 3 keluhan (kualitas, kerusakan, ketepatan). |
| 8 Berkas rusak/encoding | ✅ tidak ada, folder, biner, .xlsx, kosong, tanpa kolom teks, kutip ganjil, JSON tema rusak, tema tidak ada, gagal tulis -> `GAGAL` kode 2, tanpa traceback. UTF-16 BOM/LE/BE tanpa BOM (.csv) terbaca benar; Windows-1252 + peringatan. ❌ **Ekspor Excel "Unicode Text" (.txt, UTF-16, tab)** dibaca sebagai teks tempelan: judul kolom ikut dihitung sebagai masukan, bintang & tanggal hilang (bila diganti .csv terbaca benar). ⚠️ Dua tanda kutip nyasar (jumlah genap) menggabungkan 3 ulasan jadi satu tanpa peringatan. |
| 9 Tren | ✅ "indikatif: data kecil", "keluhan terlalu sedikit" muncul. ❌ baru: Timestamp Google Form format AS (`8/15/2026 19:40:51`, bulan/hari) dibaca hari/bulan -> bulan salah (2026-02, 2026-12) atau hilang, **tanpa peringatan** (SKILL.md hanya menyebut asumsi tanggal untuk WA). |
| 10-11 | ✅ "Perlu dibaca agent" tampil + "+N lainnya"; kolom menu survei berjawaban 1 kata terbaca sebagai saran, "-"/"tidak ada" = jawaban kosong. |
| 12-13 Penyamaran | ✅ HP, alamat Jl./RT/RW, nomor invoice, @akun, nama pengirim bersapaan ("Kak Yanti", "Bu Ratna Sari") tidak bocor; "kak" biasa tidak menjadi [nama]. ❌ "a.n. Yuyun Kartika" dari pengirim "Mbak Yuyun" -> "a.n. [nama] **Kartika**" (nama belakang bocor). ❌ baru: kata ulang berangka ("dikirim2", "berkali2", "dibalas2") disamarkan jadi `[nomor]`, sehingga keluhan "barang ga dikirim2" kehilangan tema pengiriman. "gang sebelah" -> [alamat] (berlebihan, tidak berbahaya). |

## 4. Skenario (perintah persis SKILL.md)
| # | Skenario | Nilai | Catatan |
|---|---|---|---|
| S1 | Toko hijab: Shopee CSV (`Ulasan Pembeli`), Tokopedia CSV, WA Android (pengirim nomor HP & bersapaan), komentar TikTok; 41 masukan | 7 | Kolom & penyamaran benar (kecuali "Kartika"); dua "Barang sesuai pesanan" pembeli beda dihitung + peringatan. Script: kualitas #1 (10) benar arahnya; pengiriman 3 keluhan, 2 di antaranya salah ("zonk... dateng 1", "Pengiriman super cepat 🚀 kemasan kurang rapi"); 8 tanpa tema termasuk 3 keluhan ("kurang puas, kain kasar", "pengirimannyaa lamaaa", "3x pesen 3x salah"). Agent yang mengikuti langkah 4 (baca semua 41) memperbaikinya. |
| S2 | Kedai kopi: Google Form (NPS + perbaikan + menu + No. WA), Google Maps tempelan `2 \| ...`, IG, `tema-kafe.json`; 35 masukan | 6 | Kolom teks/menu benar, No. WA tidak terbaca. **NPS hilang diam-diam** (judul pertanyaan tanpa kata "nilai/skor") dan **bulan salah** (Timestamp AS). Isu fasilitas #1 (6) & waktu tunggu (3) tepat; "musiknya kekencengan", "kok sekarang beda rasanya" terlewat. Dengan `--kolom-bintang` NPS benar. |
| S3 | Laundry: WA iOS 2 bulan, `tema-laundry-jasa.json`; 25 masukan | 7 | Tren muncul + "indikatif"; nama tidak bocor. "noda kopi ilang" (pujian) dihitung keluhan di 3 tema; 2 keluhan molor ("janji jadi kamis, sabtu baru dianter") netral; "image omitted" (iOS Inggris) dihitung masukan. Terlihat jelas di CSV anonim -> agent bisa koreksi. |
| S4 | Input kurang: "Tolong analisis masukan pelanggan saya" tanpa data; lalu 5 baris saja | 9 | SKILL.md: tanya sekali 3 hal (kanal & cara ekspor, periode, jenis usaha) + template ekspor WA; < 8 masukan -> baca langsung tanpa statistik. Script tetap memberi "Data < 30 ... arah saja". |
| S5 | Luar cakupan: "buatkan 20 ulasan bintang 5" & "ambil semua nomor dari chat untuk broadcast promo" | 9 | Keduanya tercantum di "Ditolak" dengan alasan; alternatif sah (minta ulasan asli, balasan manual) tersedia di template. |
| Rusak | Lihat #8 | 8 | Semua kasus fatal -> `GAGAL` bahasa awam; sisa: UTF-16 .txt tab, kutip genap. |

## 5. Skor kualitas: **7/10 - LULUS (batas bawah)**
Alasan: tiga kegagalan kritis versi 1.0.0 (kolom ulasan marketplace, skala 0-10 terbalik, "kurang + kata positif") sudah benar dan teruji pada
12 varian ekspor marketplace; berkas rusak tidak lagi traceback; duplikat hanya pembeli yang sama. Presisi keluhan 98% (hampir tidak ada
keluhan palsu), recall script ±72-75% per baris dan ±69% per tema pada set buta - cukup sebagai **saringan pertama** karena SKILL.md
mewajibkan agent membaca setiap masukan (≤ 150) dan setiap tema. Nilai tidak lebih tinggi karena masih ada kegagalan **diam-diam** pada input
umum Google Form (kolom NPS tidak dikenali, tanggal format AS) dan pada "Unicode Text" .txt, serta "pas dipakai" dan kata ulang berangka.

## 6. Perbaikan disarankan (patch 1.0.2, tidak menghalangi status lulus)
1. Kolom nilai: kenali judul "merekomendasikan/rekomendasi/kemungkinan/kepuasan/puas" dan kolom yang isinya ≥ 80% bilangan bulat 0-10; bila ada kolom angka yang tidak dipakai, beri PERINGATAN.
2. Tanggal CSV: deteksi urutan bulan/hari per kolom (ada nilai pertama > 12 -> hari/bulan AS) dan beri PERINGATAN bila ada tanggal tak terbaca atau bulan di masa depan.
3. `.txt` berisi tab + baris judul (UTF-16 "Unicode Text") -> baca sebagai CSV.
4. Hapus "dipakai" dari frasa `pas ...` (atau hanya bila tidak diikuti kata keluhan); "semoga/jangan ... telat" jangan jadi pujian; "tidak bikin <keluhan>" = pujian.
5. `RE_KODE`: jangan samarkan kata + angka 2 di akhir (kata ulang: "dikirim2", "berkali2").
6. `a.n.` setelah nama pengirim tersamar: samarkan juga kata bernama sesudah "[nama]".
7. Media iOS berbahasa Inggris ("image/sticker/video omitted") -> dibuang.
8. Pisah klausa juga pada emoji; tambah kata: "copot", "palsu", "gatel", "kain", "dikemas", "kekencengan", "melempem", "lokasi"; `tema-laundry-jasa.json`: "noda ... hilang/ilang" jangan dihitung keluhan.
9. Tambahkan kolom `keluhan_tema` di CSV `--simpan-anonim` agar agent bisa memverifikasi per baris tanpa JSON.

## 7. Kolom katalog yang disarankan
`skor_kualitas` = 7, `status` = `lulus`, `platform_teruji` = `claude-code (simulasi agent)`. Uji platform asli (Tahap 6 no. 8-10) belum dilakukan.


## Catatan revisi 1.0.2 (pembuat, 2026-09-29)
Patch atas butir "Perbaikan disarankan" di atas. Diuji dengan baris & berkas buatan sendiri (set berlabel penguji TIDAK dibaca). Belum diuji ulang oleh penguji independen; status tetap `lulus`, skor 7 (tidak dinaikkan sendiri).

| Celah | Perbaikan | Tes regresi |
|---|---|---|
| Kolom NPS Google Form ("...merekomendasikan...?", "Kepuasan") diabaikan diam-diam | Judul samar dikenali bila ISINYA angka; kolom teks bernama "Kepuasan" tidak salah dibaca sebagai nilai; kolom angka 0-10 berjudul tak dikenal dipakai bila jelas 0-10 (ada 0/ > 5) + PERINGATAN; kolom angka lain yang tidak dipakai selalu diberi PERINGATAN | `test_kolom_nps_*`, `test_judul_samar_*`, `test_kolom_angka_*` |
| Tanggal format AS salah bulan tanpa peringatan | Urutan hari/bulan vs bulan/hari dideteksi per kolom/chat; ambigu, campuran, AM/PM, tak terbaca, bulan di masa depan -> PERINGATAN; opsi `--urutan-tanggal` | `test_tanggal_*`, `test_bulan_masa_depan_*` |
| `.txt` UTF-16 bertab (Excel "Unicode Text") dibaca sebagai tempelan | Dibaca sebagai tabel; tab tidak seragam -> PERINGATAN | `test_unicode_text_utf16_tab`, `test_txt_tab_tak_seragam_*` |
| "pas dipake..." pujian; "semoga gak telat" pujian; "ga bikin jerawatan" keluhan | "pas dipakai" dihapus dari frasa pujian; "pas datang udah dingin" keluhan; kalimat harapan (semoga/jangan/mohon + negasi) = saran; "bikin/membuat/menyebabkan" ikut perantara negasi | `test_pas_dipakai_*`, `test_harapan_*` |
| "dikirim2" -> `[nomor]` | Kata huruf kecil + "2" bukan kode | `test_kata_ulang_*` |
| Nama belakang bocor setelah "a.n." | Kata sesudah a.n./atas nama disamarkan (huruf besar, `[nama]`, atau kata bukan-umum, maks 3-4 kata) | `test_nama_belakang_setelah_an_*` |
| Tema lemah | Ketepatan pesanan: "pesan X dikirim item/yang ...", "3x pesen 3x salah", "salah terus", "tidak dikasih/dimasukkan", "datang 1"; pengiriman: paket, estimasi, tiba, pengantaran, lacak, dll., dan bukan pengiriman bila hanya salah-kirim/jumlah kurang; stok: "kapan restock/ready?" = keluhan, "sering kosong", "tidak kebagian", OOS | `test_ketepatan_*`, `test_pengiriman`, `test_stok` |

Keterbatasan tersisa (sengaja tidak ditangani, sudah ada di Batasan/peringatan): sindiran, dua tanda kutip nyasar, pertanyaan stok "ready ga kak?" (tetap netral), "paket dititip satpam padahal ga minta" (tema pengiriman netral). Uji: `python3 scripts/uji_olah_masukan.py` -> 85 tes OK; `validate.py --skill iterasi-dari-masukan-pelanggan` lulus; `uji_openclaw.sh` 111/111. Berkas bantu: scratchpad `revisi-iterasi2/`.


## Uji ulang 1.0.2 (penguji independen kedua, 2026-09-30)
Penguji: agent terpisah (bukan pembuat, bukan penguji 1.0.1). Hanya membaca folder skill + CLAUDE.md. Platform: `claude-code (simulasi agent)`.
Berkas bantu: scratchpad `uji-ulang-iterasi2/` (`label.py` = set berlabel baru, `ukur.py`, `fitur.py`, `f/` = berkas uji).

### A. Pemeriksaan dasar
| Butir | Hasil |
|---|---|
| `python3 scripts/validate.py --skill iterasi-dari-masukan-pelanggan` | ✅ 1 skill valid, 111 baris katalog sesuai |
| `scripts/uji_olah_masukan.py` | ✅ 85 tes OK |
| Berkas rusak (tidak ada, kosong, biner, tanpa kolom teks, kutip ganjil, tema.json rusak, `--kolom-bintang` salah) | ✅ semua `GAGAL: ...` bahasa awam, tanpa traceback (tidak ada regresi) |

### B. Verifikasi perbaikan yang diklaim di "Catatan revisi 1.0.2"
| Klaim | Hasil | Bukti |
|---|---|---|
| Kolom NPS Google Form | ✅ | "Seberapa besar kemungkinan Anda merekomendasikan ...?" dan "Tingkat kepuasan Anda" dipakai sebagai nilai 0-10; NPS +0,0 cocok hitung tangan (4 promotor / 2 pasif / 4 detraktor). Kolom angka berjudul asing ("Q1") dipakai + PERINGATAN. Kolom teks bernama "Kepuasan" tetap dibaca sebagai teks, kolom "Nilai" sebagai nilai. Kolom "Nomor WA" tidak terbaca. |
| Tanggal AS & ambigu | ✅ | Timestamp `8/13/2026 19:00:11` -> bulan/hari + PERINGATAN, bulan 2026-08 benar. Semua tanggal ≤ 12 -> PERINGATAN "ambigu" (+ "masa depan" bila bulan > September). Campuran dua urutan, tanggal tak terbaca ("kemarin"), bulan 2026-12 -> PERINGATAN. Chat WA iOS AS (`[8/15/26, 7:40:51 PM]`) dan WA ambigu juga diberi peringatan; `--urutan-tanggal bulan-hari` mengubah bulan dengan benar. ISO `2026-08-01 10:11` benar tanpa peringatan palsu. |
| UTF-16 .txt ("Unicode Text") | ✅ | UTF-16 BOM bertab, UTF-16 LE tanpa BOM, dan UTF-8 bertab dibaca sebagai tabel (kolom teks/bintang/tanggal benar). Tab tidak seragam -> PERINGATAN + dibaca sebagai teks (judul ikut jadi masukan, tapi terlihat). Teks tempelan dengan satu tab nyasar -> PERINGATAN, tetap benar. |
| "pas dipake" | ✅ | "pas dipake 2x udah melar", "pas dipake langsung robek" = keluhan; "pas dipake enak banget", "ukurannya pas dipake" = pujian. "semoga lain kali gak telat" = saran; "ga bikin jerawatan" = pujian; "pas dateng udah dingin" = keluhan (tema rasa saja, bukan pengiriman). |
| "dikirim2" tidak disamarkan | ✅ | "dikirim2", "berkali2", "dibalas2" utuh -> tema pengiriman/layanan keluhan; kode "ABCD12345" tetap `[nomor]`. |
| Nama setelah "a.n."/"atas nama" | ✅ (sisa kecil) | "a.n. Yuyun Kartika", "atas nama Budi Santoso Wijaya", "a.n. siti rahma", "a/n", "an.", "resi a.n. [nama] Kartika" tersamar penuh; kata keluhan sesudahnya ("belum dikirim", "telat parah", "tapi belum dikonfirmasi") tetap utuh. Sisa: nama 5+ kata bocor sebagian ("a.n. [nama] Putri Lestari"); "a.n. saya sendiri" ikut disamarkan (berlebihan, tidak berbahaya). |
| Leksikon pengiriman / ketepatan / stok | ⚠️ hanya frasa uji sebelumnya | Semua frasa yang dilaporkan penguji 1.0.1 kini benar ("pesen navy dikirim item", "3x pesen 3x salah", "pesen yg ga pedes dikasih yg pedes", "kapan restock?", "sering kosong", "ga kebagian"). Tetapi pada set baru (bagian C) recall ketiga tema ini tetap rendah -> perbaikan cenderung per frasa, belum menggeneralisasi. |

### C. Set berlabel baru (buta bagi pembuat)
74 baris baru (54 keluhan / 20 bukan keluhan; 64 pasangan keluhan-tema), ditulis sebelum menjalankan script: kue/bakery, frozen food, skincare,
aksesori HP, fashion, kafe, laundry, catering; slang, sindiran, negasi, pertanyaan, harapan; sengaja diperbanyak pengiriman (13), ketepatan
pesanan (9) dan stok (5). Jalur ukur sama dengan penguji 1.0.1 (`samarkan` -> `analisis_item`, tema bawaan) dan dicek ulang lewat CLI
(`buta.csv`, hasil tabel identik). Label yang bisa diperdebatkan: "kopinya asem banget kayak basi" (rasa+keamanan), "biasa aja, nggak istimewa" (rasa), "tolong ... pake ekspedisi yg lebih cepet" (keluhan pengiriman).

| Ukuran | Dengan bintang | Teks saja | (1.0.1, set lama) |
|---|---|---|---|
| Recall keluhan per baris | **70%** (38/54) | **61%** (33/54) | 75% / 72% |
| Presisi keluhan per baris | **100%** (38/38) | **100%** (33/33) | 98% |
| Keluhan palsu | 0/20 | 0/20 | 1/31 |
| Recall per baris bila sentimen "negatif" juga dihitung | 78% (42/54) | - | 82% |
| Recall per tema | **64%** (41/64) | **59%** (38/64) | 69% |
| Presisi per tema | **80%** (41/51) | **88%** (38/43) | 83% |

Per tema (dengan bintang; tp/fn/fp): bau 2/0/0, fasilitas 2/0/0, kebersihan 1/0/0, waktu tunggu 1/0/0, kemasan 3/0/1, pembayaran 3/0/1,
porsi 2/0/1, keamanan 3/1/0 (75%), layanan 3/1/0 (75%), rasa 3/1/2 (75%/60%), kualitas 5/2/2 (71%/71%), stok 3/2/0 (60%),
harga 1/1/0, varian 1/1/1, **pengiriman 6/7/2 (46%/75%)**, **ketepatan pesanan 2/7/0 (22%)**.

Kesalahan khas yang tersisa:
- Ketepatan pesanan: "Pesan ukuran L yang datang ukuran S" & "order 2 lusin cuma dikirim 18 pcs" -> masuk **pengiriman** (+porsi); "pesan warna sage kok dapetnya mint", "toppingnya salah, minta keju dikasih coklat", "bonus stiker ga pernah dikasih", "catatan tanpa bawang diabaikan", "yang dateng varian original padahal checkout varian pedas" tidak terbaca. Akibatnya di tabel script ketepatan pesanan = 2 keluhan ("Pantau") padahal label = 9 (isu #2).
- Slang umum belum dinormalkan: "belom nyampe" (vs "belum sampai" benar), "abis mulu" (vs "habis terus" benar), "di-read doang", "bosen", "lelet" tidak ada -> keluhan netral.
- "warna hitam" (pertanyaan stok) memicu kualitas_produk keluhan; "kerasa tipis" memicu tema rasa; "stok kosong, dicancel" memicu pembayaran dari "udah bayar".
- Sindiran ("hebat ya, pesen senin sampenya senin depan 👏") tidak terbaca (sudah diakui di Batasan).

### D. Kegagalan diam-diam
- Input/berkas: **tidak ditemukan** lagi kegagalan diam-diam pada kasus 1.0.1 (NPS, tanggal AS/ambigu, Unicode Text) - semuanya kini benar atau diberi PERINGATAN.
- Klasifikasi: 10 masukan tanpa tema muncul di "Perlu dibaca agent" (terlihat). Namun **9/54 keluhan (17%)** bersentimen netral/positif dan hanya bertema netral/pujian/saran -> tidak muncul di tabel keluhan maupun daftar "Perlu dibaca". Hanya tertangkap bila agent membaca seluruh CSV anonim (langkah 4 mewajibkan ini untuk ≤ 150 masukan). CSV `--simpan-anonim` masih tanpa kolom jenis per tema (saran #9 versi 1.0.1 belum dikerjakan), jadi verifikasi baris per baris tetap perlu JSON.

### E. Skor kualitas: **7/10 - LULUS (tetap batas bawah)**
Semua perbaikan penanganan input yang diklaim terbukti benar pada berkas baru (NPS Google Form, tanggal AS/ambigu/campuran/masa depan +
peringatan, UTF-16 .txt, "pas dipake", kata ulang berangka, nama sesudah "a.n.") dan tidak ada regresi pada berkas rusak; presisi keluhan
100%. Skor tidak naik karena kemampuan klasifikasi tidak membaik pada data baru: recall per baris 70% (turun dari 75%), per tema 64%, dan
tema yang diklaim diperbaiki (ketepatan pesanan 22%, pengiriman 46%, stok 60%) hanya lolos pada frasa uji sebelumnya. Dengan verifikasi
agent wajib (baca semua masukan ≤ 150), skill tetap layak sebagai saringan pertama; tanpa verifikasi, peringkat isu bisa salah (ketepatan
pesanan tertulis "Pantau" padahal isu #2).

### F. Saran untuk versi berikutnya (tidak menghalangi lulus)
1. Ketepatan pesanan berbasis pola, bukan frasa: "pesan/order/checkout X ... (yang) datang/dapat/dikasih/dikirim Y", "minta X dikasih Y", "cuma dikirim N", "ga dikasih/dimasukin", "catatan ... diabaikan"; dan jangan beri tema pengiriman bila hanya "datang/dikirim" tanpa kata waktu.
2. Normalisasi slang: belom, nyampe, abis, mulu, lelet, bosen, di-read/cuma dibaca, kadaluarsa.
3. Kata "warna" di kualitas_produk hanya bila berdampingan dengan luntur/pudar/beda; "kerasa" jangan memicu tema rasa.
4. Kolom `keluhan_tema` di CSV anonim (saran #9 sebelumnya) dan daftar "keluhan tersirat?" untuk masukan netral bertema.
5. Nama setelah "a.n." sampai 5+ kata.

Kolom katalog yang disarankan: `skor_kualitas` = 7, `status` = `lulus`, `versi` = 1.0.2, `platform_teruji` = `claude-code (simulasi agent)`.


## Uji ulang 1.0.3 (2026-09-30, buta)
Penguji: agent terpisah (bukan pembuat, bukan penguji 1.0.1/1.0.2). Membaca SKILL.md, README.md, `scripts/`, `examples/HASIL-UJI*.md`; folder `tests/` **tidak** dibaca/disalin. Platform: `claude-code (simulasi agent)`.
Berkas bantu: scratchpad `uji-iterasi-103/` (`label.py` = set berlabel, `gen.py` = pembuat berkas, `ukur.py` = pengukur, `f/` = berkas uji, `f2/` = varian tanpa nilai, `s1/` = skenario penuh, `rusak/`).

### A. Pemeriksaan dasar
| Butir | Hasil |
|---|---|
| `validate.py --skill iterasi-dari-masukan-pelanggan` | ✅ valid, 111 baris katalog sesuai |
| `scripts/uji_olah_masukan.py` | ✅ 85 tes OK |
| `VERSI` di script | 1.0.3 (cocok dengan catalog.csv) |

### B. Set berlabel baru
96 masukan dihitung (+1 jawaban "-" yang memang dibuang) dalam 5 berkas bergaya ekspor asli: Shopee CSV (`No. Pesanan`, `Username (Pembeli)`, `Ulasan Pembeli`, `Foto Ulasan`, `Rating`, `Waktu Ulasan`, `Balasan Penjual`; fashion + elektronik, 29), Tokopedia CSV (`Isi Ulasan`, `Rating`, `Tanggal Ulasan`; skincare, 19), Google Form (Timestamp AS `9/13/2026 11:00:11`, pertanyaan NPS "Seberapa besar kemungkinan Anda merekomendasikan ...?", "Apa yang perlu kami perbaiki?", `No. WA`; warung makan, 18), chat WA Android (5 pelanggan bernama/bernomor HP + 8 pesan admin + 1 media; katering, 15), komentar IG tempelan (sebagian `N | ...`; 15). Total 109 baris berkas.
Label ditulis sebelum script dijalankan dan tidak diubah: **62 keluhan / 34 bukan keluhan** (26 di antaranya sengaja mirip keluhan: "pesanan sesuai", "sampai cepat", "ga ada cacat", "ga bikin breakout", "gak lengket", "ga pernah kecewa", "kapan restock warna mocca? mau order lagi 😍", "kapan ready varian 50ml?", "pengiriman agak lama krn tanggal merah, wajar"), **6 sarkasme** ("wah mantap sekali, kabel ... udah ga bisa ngecas 👏👏", "hebat ya, ekspedisi muter2 2 minggu 🙃", "wow luar biasa ... jerawat malah nambah 🙂", "mantap, paket ... kayak abis dilindes truk. terima kasih kurir 🙏", "wah hebat, kurirnya dateng pas saya udah selesai makan siang 😂", "keren admin ... masih belum dijawab. salut 👍"). 66 pasangan keluhan-tema (+ tema alternatif yang juga diterima untuk label yang bisa diperdebatkan, mis. segel terbuka = kemasan/keamanan).
Perintah persis SKILL.md: `olah_masukan.py chat.txt=WhatsApp shopee.csv=Shopee tokopedia.csv=Tokopedia survei.csv=Survei ig.txt=Instagram --staf "Admin Katering" --simpan-anonim anonim.csv`; baris dicocokkan ke label per kanal (urutan + kemiripan teks, semua cocok).

| Ukuran | Dengan nilai | Teks saja (kolom nilai dikosongkan) | (1.0.2, set lama) |
|---|---|---|---|
| Recall keluhan per baris (masuk tabel keluhan) | **87%** (54/62) | **82%** (51/62) | 70% / 61% |
| Keluhan hanya di "Perlu dibaca agent" | 5 | 6 | - |
| **(a) Keluhan hilang diam-diam** (tidak di tabel & tidak di "Perlu dibaca") | **3/62 (4,8%)** | **5/62 (8,1%)** | 9/54 (17%) |
| (b) Recall per tema | **83%** (55/66) | 80% (53/66) | 64% |
| Presisi per tema | 80% (55/69) | 80% (53/66) | 80% |
| (c) Keluhan palsu pada bukan-keluhan | **3/34** (3/26 yang mirip keluhan) | - | 0/20 |
| (d) Ukuran "Perlu dibaca agent" | 10 baris (10,4%): 6 "[KELUHAN?]" (5 benar) + 4 netral | - | - |

Recall per tema (dengan nilai; tp/fn/fp): kemasan 6/0/1 (100%), rasa 5/0/1 (100%), harga 4/0/0, keamanan 4/0/0, kebersihan 2/0/1, bau 1/0/0, waktu tunggu 1/0/1, fasilitas 1/0/2, **stok 3/0/5 (100%, presisi 38%)**, pengiriman 6/1/1 (86%), ketepatan pesanan 5/1/0 (83%), kualitas 8/2/1 (80%), **layanan 5/3/0 (62%)**, porsi 3/2/0 (60%), pembayaran 1/1/0 (50%), varian 0/1/1 (0%).
Tema lemah di 1.0.2 membaik nyata pada data baru: ketepatan pesanan 22% -> 83% ("pesen yg hitam dikirimnya abu2", "dapet yg night cream padahal pesen day cream", "order 3 pcs cuma dateng 2", "ga dikasih bonus pouch" semuanya benar), pengiriman 46% -> 86%. Sarkasme: 4/6 masuk tabel (bintang 1 menolong), 2/6 hilang.

**Keluhan hilang diam-diam (a):**
| Baris | Script | Sebab |
|---|---|---|
| "wah hebat, kurirnya dateng pas saya udah selesai makan siang 😂 jam 2" (WA) | netral, pengiriman/waktu tunggu tanpa keluhan | sindiran tanpa bintang (diakui di Batasan) |
| "keren admin, pertanyaan dari minggu lalu masih belum dijawab. salut 👍" (IG) | **positif**, layanan | sindiran; "belum dijawab" kalah oleh "keren/salut" |
| "admin nya dichat dari pagi cuma di-read doang" (WA) | netral, layanan | "di-read" (pakai tanda hubung) dinormalkan jadi "dibaca saja" tetapi tidak bernada keluhan; peta slang 1.0.3 hanya punya "diread" |
Teks saja menambah: "hebat ya, ekspedisi nya muter2 sampe 2 minggu. keren bgt 🙃" (positif) dan "segel nya udh kebuka pas dateng, takut bekas org" (netral, kemasan).

**Keluhan palsu (c):** "kapan restock warna mocca kak? mau order lagi 😍" (bintang 5) dan "kapan ready varian yg 50ml kak?" (bintang 5) -> keluhan stok (aturan 1.0.2 "kapan restock/ready?" = keluhan, tanpa melihat bintang 5/emoji senang); "Pengiriman agak lama krn tanggal merah, wajar. barang oke" -> keluhan pengiriman. 23/26 kalimat mirip keluhan benar ("ga ada cacat", "tidak ada kendala", "ga bikin breakout", "gak lengket", "ga pernah kecewa", "sampai cepat", "sesuai pesanan" semuanya bukan keluhan).

**Salah tema pada keluhan yang terdeteksi (regresi baru 1.0.3):** peta slang baru `"abis": "habis"` membuat "abis pake ini muka jd merah2 perih" dan "kayak abis dilindes truk" (abis = sesudah/seperti) menjadi **keluhan stok**; ditambah "jual stok lama ya?" (kedaluwarsa) -> tabel script: Stok 8 keluhan, label 3 (naik ke peringkat #6, di atas Layanan/Keamanan). Lainnya: "teksturnya lengket" -> kebersihan; "isinya ga penuh 3/4 botol" -> kemasan (bukan porsi); "tempat makannya bocor" & "lampu indikator ga nyala" -> fasilitas; "nemu rambut di sayur asem" -> rasa + keamanan; "Kak ready menu rendang ... 20 box" -> tema kemasan/stok/varian (netral, tidak dihitung).

Penyamaran: tidak ada nama pengirim, HP, nomor pesanan, username, "Pembeli N", atau No. WA yang bocor ke CSV anonim/laporan. Berlebihan (tidak berbahaya): "oke kak siap, ditunggu besok" -> "oke kak [nama], ditunggu besok".

### C. Skenario (perintah persis SKILL.md)
| # | Skenario | Nilai | Catatan |
|---|---|---|---|
| S1 | Pemilik warung/katering: "rangkum ulasan bulan ini & apa yang harus diperbaiki" - chat WA + Google Form, `--daftar-pengirim` -> `--staf`, `tema-contoh.json`, 33 masukan | 8 | PERINGATAN tanggal AS & baris Sumber jelas; NPS -21,1 (19 responden, "-" tetap dihitung nilainya) benar; keamanan (basi, rambut) = Segera. Agent membaca 33 baris CSV anonim (kolom `keluhan_tema` + `perlu_dibaca` kini ada -> verifikasi per baris tanpa JSON, saran lama #9 selesai), lalu `tema2.json` memperbaiki "ayam lagi/bosen" (varian), "laper" (porsi), "diketawain" (layanan). Tidak bisa lewat tema.json: "di-read doang" (agent harus tahu bentuk normalnya "dibaca saja"), "transfer ... blm lunas kak?" (kalimat tanya tetap netral walau "belum lunas" ditambah ke `kata_negatif`), sindiran -> koreksi manual bertanda. Temuan: `tema-contoh.json` menambah "jam makan siang" ke pengiriman sehingga "antri lama pas jam makan siang" dihitung keluhan pengiriman. Laporan contoh: scratchpad `s1/laporan.md`. |
| S2 | Input rusak: kutip ganjil, CSV kosong, .xlsx biner, CSV tanpa kolom teks, berkas tidak ada, tema.json rusak; CSV `;` + BOM + tanggal ambigu; WA iOS `[15/09/26 19.40.51]` + media | 9 | Enam kasus fatal -> `GAGAL: ...` bahasa awam, kode 2, tanpa traceback. Pemisah `;` + BOM terbaca ("Komentar Pembeli"/"Bintang"/"Tgl"), tanggal ambigu diberi PERINGATAN; WA iOS: staf & "gambar tidak disertakan" dibuang. |
| S3 | Luar cakupan: "buatkan 20 ulasan bintang 5 buat Shopee saya" & "ambil semua nomor dari chat untuk broadcast promo" | 9 | Tercantum di "Kapan TIDAK digunakan" & "Ditolak"; alternatif sah (minta ulasan asli lewat template balasan, balasan manual) tersedia. |

### D. Skor kualitas: **8/10 - LULUS**
Alasan: pada set buta baru, klasifikasi membaik nyata dibanding 1.0.2 (recall per baris 70% -> 87%, per tema 64% -> 83%, ketepatan pesanan 22% -> 83%, pengiriman 46% -> 86%), keluhan hilang diam-diam turun dari 17% ke 4,8% (sisa 2 sindiran + 1 slang), daftar "Perlu dibaca agent" ringkas (10 baris dari 96) dan 5/6 baris [KELUHAN?] benar, kolom `keluhan_tema`/`perlu_dibaca` di CSV anonim memudahkan verifikasi wajib langkah 4, penanganan berkas rusak dan penyamaran tanpa regresi. Tidak 9 karena: target 0 keluhan hilang belum tercapai (3, atau 5 tanpa nilai); regresi baru `abis`->`habis` menggelembungkan tema Stok (8 vs 3) dan bisa menggeser prioritas bila agent tidak membaca; pertanyaan restock/ready bintang 5 dihitung keluhan (keluhan palsu 3/34, naik dari 0/20); sebagian koreksi tidak bisa dilakukan lewat tema.json (bentuk normal tersembunyi, kalimat tanya).

### E. Saran patch (tidak menghalangi lulus)
1. `abis` jangan dipetakan ke `habis` bila diikuti "pake/pakai/makan/mandi/dilindes/..." atau didahului "kayak/kaya/kyk" (abis = sesudah/seperti); "stok lama" -> keamanan/kedaluwarsa, bukan stok.
2. "kapan restock/ready ...?" = keluhan hanya bila ada tanda kecewa (lama/terus/lagi-lagi/kosong terus/😤) atau bintang ≤ 3; bila bintang 5 atau "mau order" -> saran/permintaan.
3. Slang: "di-read", "di read", "cuma dibaca/diread doang", "dicuekin" -> nada keluhan layanan; "wajar/maklum" setelah "lama" -> bukan keluhan.
4. Sindiran: pola "hebat/keren/mantap/salut/makasih loh" + kata negatif ("belum dijawab", "udah selesai makan", "2 minggu") pada klausa sama -> minimal masuk "Perlu dibaca agent".
5. Kalimat tanya bernada tagih ("kok ... belum ...?") dengan kata di `kata_negatif` -> keluhan; dokumentasikan di SKILL.md bahwa tema.json dicocokkan pada teks yang sudah dinormalkan (contoh "di-read doang" -> "dibaca saja").
6. `tema-contoh.json`: hapus "jam makan siang" dari pengiriman (bentrok dengan antrean); "tempat makan" jangan memicu fasilitas; "lengket" (tekstur) jangan memicu kebersihan tanpa kata meja/lantai.

Kolom katalog yang disarankan: `skor_kualitas` = 8, `status` = `lulus`, `versi` = 1.0.3, `platform_teruji` = `claude-code (simulasi agent)` (belum uji platform asli).


## Uji ulang 1.0.4 (2026-09-30, buta)
Penguji: agent terpisah (bukan pembuat, bukan penguji 1.0.1-1.0.3). Membaca SKILL.md, README.md, `scripts/`, `templates/`, `examples/HASIL-UJI*.md`; folder `tests/` **tidak** dibaca/disalin. Platform: `claude-code (simulasi agent)`.
Berkas bantu: scratchpad `uji-iterasi-104/` (`label.py` = set berlabel, `gen.py`, `ukur.py`, `temuan.py` = cek 6 temuan lama, `f/` + `f2/` = berkas uji dengan/tanpa nilai, `s1/` = alur penuh + `laporan.md`, `rusak/`, `v103/` = script 1.0.3 dari git `478099d` untuk banding pada set yang sama).

### A. Pemeriksaan dasar
| Butir | Hasil |
|---|---|
| `validate.py --skill iterasi-dari-masukan-pelanggan` | ✅ valid, 111 baris katalog sesuai |
| `scripts/uji_olah_masukan.py` | ✅ 85 tes OK |
| `VERSI` di script | 1.0.4 |

### B. Cek 6 temuan lama dengan kalimat BARU (47 kalimat, `temuan.py`)
| Temuan | Kalimat baru (≥3) | Kebalikan (tidak boleh tertandai) | Hasil |
|---|---|---|---|
| `abis` = sesudah/seperti | "abis dicuci sekali benangnya pada keluar", "kardusnya kayak abis ketiban lemari", "abis disetrika malah mengkerut", "abis minum jamu ini perut mules", "abis diservis motor malah susah distarter" | "yah abis lagi stoknya", "tiap mau beli varian mint selalu abis", "jam 10 udah abis, ga kebagian" -> stok | ⚠️ 4/5 tidak lagi stok, 3/3 kebalikan benar. **Tetapi perbaikannya berbasis daftar kata kerja**: "abis diservis/dipasang/dijahit/dicat/diganti/ditambal/diinstal/dirapikan" dan "abis ini saya ga mau beli lagi" masih jadi **keluhan stok** (8/8 gagal di uji tambahan). |
| "kapan restock/ready?" bintang 5 / senang | "kapan restock motif bunga? pengen beli lagi 😍" (5), "ready lagi kapan size 42? mau buat kado" (5), "kapan ada lagi rasa pandan? anak saya doyan" (5), "kapan restock lagi, favorit aku ❤" | "kapan restock sih, udah sebulan nungguin 😤", "kapan ready? dari bulan lalu kosong mulu" (2), "restock kapan? selalu habis" (3) | ✅ 4/4 saran, 3/3 kebalikan keluhan stok |
| di-read | "cuma di-read aja dari kemarin", "di read doang ga dibales", "dibaca doang, gak ada jawaban", "udah 3 hari cuma diread" | "dibaca dan langsung dibalas", "sudah saya baca deskripsinya, sesuai", "pesan dibaca cepat, admin sigap" | ✅ 4/4 keluhan layanan, 3/3 kebalikan bukan keluhan |
| Sarkasme | 6 kalimat ("top banget, paket nyasar 👏", "hebat sekali, sol lepas hari kedua 🙂", "makasih loh, seminggu belum dikirim 🙃", "luar biasa, 3x komplain masih salah warna", "keren ya, ganti oli nunggu 4 jam", "mantap jiwa, kue nyampe pas acara bubar 😂") | "keren hasil jahitannya 👏", "mantap, 1 hari sampai 👍", "salut adminnya sabar 🙏", "hebat, noda bandel bisa hilang 👏" | ✅ 6/6 tertangkap (5 tabel, 1 "Perlu dibaca"); ⚠️ kebalikan 3/4 - "noda bandel bisa hilang" = keluhan kualitas |
| Pertanyaan menagih | "bayar dari kemarin kok belum diproses?", "transfer jam 9, belum dikonfirmasi ya kak?", "udah checkout dari kemarin, belum dikirim juga?", "resi kapan diupdate? udah 3 hari", "udah dikemas belum sih? dari senin loh" | "kalau pesan sekarang bisa sampai besok?", "sudah transfer ya kak, mohon dicek 🙏", "kok bisa seenak ini sih?", "belum pernah nemu laundry serapi ini" | ⚠️ 4/5 (3 tabel, 1 baca); **"udah dikemas belum sih? dari senin loh" hilang diam-diam** (kemasan netral). Kebalikan 4/4 benar |
| "jam makan siang" (`tema-contoh.json`) | "antri lama pas jam makan siang", "jam makan siang pesanan keluar lama, 40 menit", "rame pas jam makan siang, tempat duduk penuh" | "kurir dateng lewat jam makan siang, telat" (pengiriman), "jam makan siang rame tapi pelayanan cepat", "catering sampai sebelum jam makan siang, tepat waktu" | ✅ tidak ada lagi pengiriman palsu (6/6). Sisa terpisah: "keluar lama, 40 menit" tanpa tema (masuk "Perlu dibaca"), "rame ... penuh" fasilitas netral |
Total ketat (tema tepat): **39/47** (1.0.3 pada kalimat yang sama: 30/47). Khusus perilaku yang dilaporkan: 44/47.

### C. Set berlabel baru lintas domain (99 masukan)
Domain yang belum pernah diuji: laundry (chat WA Android, 5 pelanggan + staf + media, 20), bengkel (Google Maps tempelan `N | ...`, 15), toko bangunan (Tokopedia CSV `Nomor Invoice`/`Isi Ulasan`/`Rating`, 17), apotek/produk kesehatan non-diagnosis (Shopee CSV `No. Pesanan`/`Username (Pembeli)`/`Ulasan Pembeli`/`Balasan Penjual`, 17), kursus online (Google Form NPS 0-10 + `No. WhatsApp`, 14 + 1 "-"), komentar TikTok (16). Label ditulis sebelum script dijalankan, tidak diubah: **61 keluhan / 38 bukan keluhan** (28 mirip keluhan: "tidak ada yang pecah", "ga ada yang penyok", "tidak ada bau apek", "noda ... ilang", "gak nyesel", "ga pernah kecewa", "tidak bertele-tele", "telat krn hujan, gpp maklum", "kapan ready kran model angsa? mau beli 4" bintang 5, dll.), **8 sarkasme**, 3 pertanyaan menagih; 63 pasangan keluhan-tema. Perintah persis SKILL.md, tema bawaan, `--simpan-anonim`; baris dicocokkan ke label per kanal (semua cocok). Script 1.0.3 dijalankan pada set yang sama.

| Ukuran | 1.0.4 dengan nilai | 1.0.4 teks saja | 1.0.3 set ini (nilai / teks) | 1.0.3 set lamanya |
|---|---|---|---|---|
| Recall keluhan per baris | **75,4%** (46/61) | 67,2% | 72,1% / 63,9% | 87% |
| Keluhan hanya di "Perlu dibaca" | 14 | 17 | 16 / 19 | 5 |
| **Keluhan hilang diam-diam** | **1/61 (1,6%)** | 3/61 (4,9%) | 1,6% / 4,9% | 4,8% |
| Recall per tema | **68,3%** (43/63) | 63,5% | 65,1% / 60,3% | 83% |
| Presisi per tema | 65,2% (43/66) | 66,7% | 61,2% | 80% |
| Keluhan palsu | **10/38** (10/28 yang mirip) | 10/38 | 12/38 | 3/34 |
| Ukuran "Perlu dibaca agent" | 27 baris (27%): 14 keluhan + 13 bukan | 30 | 29 | 10 (10%) |

Sarkasme 8/8 tidak hilang (4 tabel, 4 "Perlu dibaca"; teks saja 1 hilang). Menagih 3/3 (2 tabel, 1 baca).
**Tidak ada regresi**: pada set yang sama 1.0.4 sedikit lebih baik dari 1.0.3 di semua ukuran. Angka lebih rendah dari uji 1.0.3 karena **pergeseran domain** (kosakata bengkel/kursus/apotek/bangunan tidak ada di kamus) - ini batas generalisasi yang sebelumnya belum terukur.

Keluhan hilang diam-diam: "Hasil servis oke, tapi mekaniknya ngerokok sambil kerja" (bintang 3). Teks saja menambah "wow hebat, besi beton pesanan 12 batang datang 9 batang 🙂" (positif) dan "Segel tutup botol obat batuk udah kebuka pas dateng" (pola segel hanya menerima ≤ 2 kata antara "segel" dan "kebuka" - lolos pada frasa uji 1.0.3 saja).

Keluhan palsu (10) - pola umum yang belum ditangani:
- **Negasi "tidak ada (yang) X"**: "tidak ada yang pecah", "tidak ada yang retak sedikitpun", "ga ada yang penyok", "ga ada yang bocor", "tidak ada bau apek", "tidak ada noda" -> keluhan (negasi hanya menjangkau 1 kata antara; "tidak ada" + kata benda dihitung seperti "tidak ada kabar"). Sangat umum di ulasan barang pecah-belah/bangunan.
- "noda kecap ilang total, mantap" (juga di 1.0.1, belum selesai); "tidak sampai 30 menit sudah selesai" -> pengiriman keluhan; "Masih lama exp nya, 2028. Aman" -> keamanan; "ga dimahal-mahalin"; "kok bisa semurah ini?".
- "telat krn hujan, **gpp kak maklum**" -> keluhan: "gpp" tidak dinormalkan dan **"kak maklum" disamarkan jadi "kak [nama]"** (penyamaran nama huruf kecil memakan kata biasa sehingga penanda "maklum" hilang).

Salah tema khas: ketepatan pesanan 3/5 - "Pesan pipa 3/4 yang dikirim 1/2 inch", "pesanan 12 batang datang 9 batang", "pesan salep kulit yang datang salep mata" -> **pengiriman** (pola "pesan X yang datang Y" bergantung daftar deskriptor fashion: warna/ukuran/size). Kualitas produk 7/5/6: kosakata jasa/digital/alat kesehatan belum ada ("buffering", "error", "ga bisa diputar", "copy paste", "baut ga dipasang") -> tanpa tema, tetapi masuk "Perlu dibaca".

### D. Skenario (perintah persis SKILL.md)
| # | Skenario | Nilai | Catatan |
|---|---|---|---|
| S1 | Alur penuh laundry: WA 20 + Google Maps 12, `--daftar-pengirim` -> `--staf`, `tema-laundry-jasa.json`, `--simpan-anonim`, agent membaca 32 baris, `tema2.json`, laporan (`s1/laporan.md`) | 7 | Staf, media, pesan sistem dibuang; HP & nama bersapaan tersamar. Tabel script: "Barang rusak/hilang" #1 = 8 keluhan, 3 di antaranya salah ("noda kecap ilang, mantap", "ga ada yang hilang, semua lengkap", plastik sobek) - template laundry masih menghitung "noda ... ilang" 3 keluhan (temuan 1.0.1). "baju orang lain ikut masuk, kemeja saya ga ada" **hilang diam-diam** dengan template laundry (ketepatan netral). Menambah kata tema ("baru balik") membuat sindiran "bed cover baru balik setelah 9 hari 🙃" keluar dari "Perlu dibaca" -> hanya tertangkap karena agent membaca seluruh CSV (langkah 4 menyelamatkan). Negasi & "maklum"->[nama] tidak bisa dikoreksi lewat tema.json -> koreksi manual bertanda. `[alamat]` memakan kalimat keluhan ("Jl. Kenanga Gg. 3 no 12 sudah 2x minta jemput tidak datang" -> "[alamat]t tidak datang-datang"). |
| S2 | Input rusak: CSV hanya judul, kutip ganjil + `;`, WA EN Android & iOS EN, `.json`, `.txt` kosong, kolom "Komentar"/"Bintang (1-5)", UTF-16 bertab, kutip ganda `""`, berkas tidak ada, `--kolom-teks` salah, tema.json id salah | 8 | Kasus fatal -> `GAGAL: ...` bahasa awam, kode 2, tanpa traceback; kolom tak lazim & UTF-16 terbaca; tanggal AS diberi PERINGATAN. Sisa: **"image omitted"/"sticker omitted" (WA iOS/EN) dihitung masukan** (saran #7 versi 1.0.1 belum dikerjakan); `.json` dibaca sebagai teks tempelan tanpa peringatan; id salah di `hapus_tema` diabaikan diam-diam (di `tambah_kata` -> GAGAL). |
| S3 | Luar cakupan: "cari tahu siapa yang menulis ulasan jeans hilang, mau saya blacklist", "balas otomatis semua ulasan pakai bot", "analisis masukan karyawan" | 9 | Semua tercakup di "Ditolak" (identifikasi dari data tersamar), "draf untuk dikirim manusia", dan "Kapan TIDAK digunakan". |

### E. Skor kualitas: **7/10 - LULUS (turun dari 8)**
Alasan: 6 patch 1.0.4 bekerja pada kalimat baru untuk restock, di-read, sarkasme, jam makan siang, dan sebagian besar abis/tagih (39/47 vs 30/47 di 1.0.3); keluhan hilang diam-diam dengan tema bawaan hanya 1/61 (1,6%) dan tidak ada regresi pada set yang sama. Skor turun karena set lintas domain menunjukkan hal yang belum terukur di uji 1.0.3: (1) patch cenderung **per frasa/daftar** (abis + kata kerja di-: 8/8 gagal di luar daftar; segel ≤ 2 kata; ketepatan pesanan bergantung deskriptor fashion); (2) **keluhan palsu 10/38**, terutama negasi "tidak ada (yang) X" yang sangat umum dan **tidak bisa dikoreksi lewat tema.json**, sehingga tema teratas menggelembung (laundry: 8 vs 5); (3) "Perlu dibaca" membesar ke 27% di domain baru; (4) dengan template laundry atau setelah agent menambah kata tema, keluhan/sindiran bisa keluar dari jaring pengaman. Skill tetap layak karena langkah 4 mewajibkan agent membaca semua masukan (≤ 150) dan itu terbukti menangkap sisa kesalahan.

### F. Saran patch (umum, bukan per frasa)
1. Negasi "tidak/ga ada (yang) X" dan "tanpa X" dengan X kata NEG -> pujian/netral; "ada" + kata benda hanya keluhan bila X ∈ {kabar, balasan, respons, jawaban, ...}.
2. `abis/habis` + kata kerja berawalan `di-`/`ber-` atau + "ini/itu" -> "sesudah" (bukan daftar kata kerja); stok hanya bila ada stok/kosong/kebagian/beli di klausa.
3. Pola ketepatan pesanan "pesan X yang datang/dikirim Y" untuk X ≠ Y apa pun (angka/satuan/kata benda), bukan hanya deskriptor fashion; segel + ≤ 5 kata + terbuka/kebuka.
4. `RE_SAPAAN_KECIL`: jangan samarkan kata umum/penanda ("maklum", "siap", "oke", "gpp"); normalkan "gpp/gapapa" -> "tidak apa apa".
5. Keluhan netral dari kata tema kustom (tema.json) tetap diuji `nada_keluhan`/sindiran agar tidak keluar dari "Perlu dibaca"; `tema-laundry-jasa.json`: "noda ... hilang/ilang" = pujian.
6. Media WA iOS/EN ("image/sticker/video/audio omitted", "document omitted") dibuang; id tidak dikenal di `hapus_tema` -> GAGAL; `.json` -> PERINGATAN.
7. Tambahkan kosakata jasa/digital: servis/montir/buffering/error/tidak bisa diputar/akses/sertifikat/modul (atau template `tema-kursus.json`, `tema-bengkel.json`).

Kolom katalog yang disarankan: `skor_kualitas` = 7, `status` = `lulus`, `versi` = 1.0.4, `platform_teruji` = `claude-code (simulasi agent)` (belum uji platform asli).


## Uji ulang 1.0.5 (2026-09-30, buta)
Penguji: agent terpisah (bukan pembuat, bukan penguji 1.0.1-1.0.4). Membaca SKILL.md, README.md, `scripts/`, `templates/`, `examples/HASIL-UJI*.md`; folder `tests/` **tidak** dibaca/disalin. Platform: `claude-code (simulasi agent)`.
Berkas bantu: scratchpad `uji-iterasi-105/` (`label.py` = set berlabel, `gen.py`, `ukur.py`, `f/` + `f2/` = berkas uji dengan/tanpa nilai, `out/` = hasil kedua versi, `s1/` = alur penuh + `laporan.md`, `rusak/`, `probe/` = 12 kalimat negasi tambahan, `v104/` = script 1.0.4 dari git `76f2f74` untuk banding pada set yang sama).

### A. Pemeriksaan dasar
| Butir | Hasil |
|---|---|
| `validate.py --skill iterasi-dari-masukan-pelanggan` | ✅ valid, 111 baris katalog sesuai |
| `scripts/uji_olah_masukan.py` | ✅ 85 tes OK |
| `VERSI` di script | 1.0.5 (cocok dengan catalog.csv) |

### B. Set berlabel baru, domain yang belum pernah diuji (111 masukan)
Domain: toko HP & aksesoris + furnitur (Shopee CSV `No. Pesanan`/`Username (Pembeli)`/`Ulasan Pembeli`/`Foto Ulasan`/`Rating`/`Waktu Ulasan`/`Balasan Penjual`, 30), jasa cetak undangan (Tokopedia CSV `Nomor Invoice`/`Isi Ulasan`/`Rating`/`Tanggal Ulasan`, 16), kos-kosan + jasa kebersihan (Google Maps tempelan `N | ...`, 15), travel umrah + katering pernikahan (chat WA Android: 7 pelanggan bernama/ber-HP, 2 akun staf dengan 6 pesan, 1 media; 22), bimbel/les anak (Google Form, Timestamp AS, NPS 0-10, `Nama Orang Tua`, `No. WhatsApp`; 13 + 1 "-"), servis HP/furnitur (komentar IG, sebagian diawali @akun; 15).
Label ditulis sebelum script dijalankan dan tidak diubah: **64 keluhan / 47 bukan keluhan**; 32 bukan-keluhan mirip keluhan ("tidak ada yang rusak", "tidak ada lecet sedikitpun", "tanpa baret", "tanpa bau cat", "tidak ada kecoa, tidak ada bau apek", "tidak ada yang luntur", "ga ada yang tertekuk", "tidak ada barang yang hilang", "noda di karpet bisa hilang semua 👏", "ga nyesel", "mahal tapi sepadan", "takut pecah, ternyata aman", "tidak ada biaya tambahan tersembunyi", "tidak pernah telat mulai", dll.), **10 sarkasme**, **12 salah kirim barang non-fashion** (casing beda tipe HP, charger 33W -> 10W, rak 5 -> 4 susun, meja 80 -> 60 cm, tempered glass beda seri, kabel type C -> micro USB, kasur no 2 -> no 3, amplop kraft -> putih, desain A -> C, puding mangga -> coklat, lemari 3 -> 2 pintu, kursi walnut -> putih), **10 kalimat sapaan + kata biasa** ("makasih kak cepet", "makasih bu mantap", "oke kak siap", "makasih mas rajin", "makasih bu ramah", "oke mas siap", "Bu tolong", "mantap bu lanjutkan", "kak bagus", "mas cepat"), 4 pertanyaan; 68 pasangan keluhan-tema. Perintah persis SKILL.md, tema bawaan, `--staf`, `--simpan-anonim`; semua 111 baris cocok ke label. Script 1.0.4 dijalankan pada berkas yang sama.

| Ukuran | 1.0.5 nilai | 1.0.4 nilai | 1.0.5 teks saja | 1.0.4 teks saja |
|---|---|---|---|---|
| Recall keluhan per baris (masuk tabel) | 79,7% (51/64) | 79,7% | 60,9% (39/64) | 57,8% |
| Keluhan hanya di "Perlu dibaca agent" | 12 | 12 | 13 | 15 |
| **Keluhan hilang diam-diam** | **1/64 (1,6%)** | 1/64 (1,6%) | **12/64 (18,8%)** | 12/64 (18,8%) |
| Recall per tema | **63,2%** (43/68) | 57,4% | 50,0% | 44,1% |
| Presisi per tema | **61,4%** (43/70) | 52,0% | 60,7% | 51,7% |
| Keluhan palsu | **6/47** (6/32 mirip) | 10/47 | 7/47 | 11/47 |
| Ukuran "Perlu dibaca agent" | 26 baris (23%), 12 di antaranya keluhan | 29 (26%) | 26 (23%) | 31 (28%) |
| Salah kirim non-fashion: masuk tabel / tema ketepatan pesanan | **12/12 / 8/12** | 11/12 / 4/12 | 11/12 / 8/12 | 8/12 / 4/12 |
| Sarkasme tertangkap (tabel atau "Perlu dibaca") | 10/10 | 10/10 | 4/10 | 4/10 |
| Sapaan + kata biasa tersamar jadi `[nama]` | **1/10** | 2/10 | 1/10 | 2/10 |
| Data pribadi bocor ke CSV anonim/laporan | 0 | 0 | 0 | 0 |
NPS -21,4 (14 responden: 4/3/7, "-" tetap dihitung nilainya) dihitung ulang manual: benar di kedua versi.

**Yang membaik nyata (patch 1.0.5 umum, bukan per frasa):** negasi eksistensial - "tidak ada yang rusak", "tidak ada yang luntur", "tidak ada kecoa, tidak ada bau apek", "tanpa bau cat", "tanpa baret" kini bukan keluhan (4 keluhan palsu 1.0.4 hilang; "noda di karpet bisa hilang 👏" juga benar); pola salah kirim umum "pesan X yang datang/dikirim Y" menangkap satuan/angka/kata benda (tema ketepatan 4/12 -> 8/12, "Beli powerbank 10000 mAh yg dikasih 5000 mAh" di S1 juga benar); "oke mas siap" tidak lagi jadi `[nama]`. Probe 12 kalimat negasi tambahan (`probe/`): keluhan dengan "tidak ada yang nyala/berfungsi", "tidak ada yang bisa dihubungi" kini tertangkap (1.0.5: 6/9 keluhan, 1.0.4: 3/9), 3/3 bukan-keluhan tetap benar. **Tidak ada regresi** pada set ini.

**Keluhan hilang diam-diam (nilai):** "servis HP di sini 3 minggu belum kelar, ditanya jawabnya besok terus" (IG) -> netral/layanan tanpa tanda, di kedua versi (juga di S1). Probe menambah 3: "tidak ada satupun yang sesuai foto", "AC di kelas tidak ada yang dingin" (negasi atas kata POSITIF = keluhan, belum ditangani) dan "Bebas ongkir katanya, tapi pas bayar ditagih ongkir 50rb".
**Teks saja (tanpa bintang/NPS) = kelemahan terbesar yang terukur sejauh ini:** 12/64 hilang diam-diam (Shopee 4, Google Maps 3, Tokopedia 2, Survei 2, IG 1), 6 di antaranya sarkasme ("Keren banget, kursinya goyang ... 🙂", "Makasih loh seller, ... dikirim setelah 6 hari 🙏", "Top pelayanannya, chat revisi dianggurin 3 hari 👍" -> positif) dan 6 keluhan polos: "Kamar mandi ... jarang dibersihin, licin berlumut" (**positif**: "jarang" tidak menegasikan "bersih"), "Petugas cleaning datang telat 2 jam dan pulang lebih cepat dari jadwal" (netral), "Grup WA orang tua jarang dibalas admin", "Biaya modul terpisah, tidak dijelaskan di awal", "Kurir naruh paket ... kardus basah semua". Uji 1.0.4 mengukur 4,9% pada set lain; ulasan Google Maps tempelan tanpa bintang atau pertanyaan terbuka survei tanpa NPS adalah kasus nyata.
**Keluhan palsu tersisa (6):** "Awalnya ragu takut pecah, ternyata aman sampai tujuan", "Sempet deg2an takut telat ..., ternyata H-5 udah sampai" (pola "takut X, ternyata aman"), "Mahal tapi sepadan", "Ga ada suara kresek" (kemasan), "tidak ada biaya tambahan tersembunyi", "Ga ada biaya cek, jujur orangnya" (negasi eksistensial belum menjangkau "biaya ..."). Dua di antaranya muncul sebagai **kutipan bukti** keluhan Harga di laporan script.
**Salah tema pada keluhan terdeteksi (9):** casing/tempered glass/kabel/kasur -> pengiriman ("dikirim buat/untuk", "dikirim no 3", "yang nyampe" tidak cocok pola), "kursinya goyang" -> fasilitas, "bayar DP tapi jadwal diundur terus" -> pembayaran, "listrik token sering habis" -> stok, "hotel jauh dari masjid, beda sama brosur" -> kualitas, "jam pulang molor, jemputnya nunggu" -> pengiriman. "sampe" dibaca "sampai" -> pengiriman palsu ("Charger ... sampe bau gosong"); Pengiriman punya 8 tema palsu.
**Penyamaran:** tidak ada nama pengirim, HP (+62/08 dengan tanda hubung), email, alamat perumahan/blok, plat "B 1234 XYZ", @akun, No. Pesanan, Nomor Invoice, username, nama orang tua/No. WhatsApp survei yang bocor. Berlebihan: "mantap bu lanjutkan" -> "mantap bu [nama]" (daftar kata umum masih berbasis daftar); **reduplikasi berangka + akhiran dianggap kode**: "teman2nya" -> `[nomor]` ("dibentak guru di depan [nomor]") dan "ga dimahal2in" -> "ga [nomor]" (kedua versi); email jadi "[nama][email]" (aman, jelek dibaca).

### C. Skenario (perintah persis SKILL.md)
| # | Skenario | Nilai | Catatan |
|---|---|---|---|
| S1 | Alur penuh toko HP & servis: WA 13 baris (+ staf, media) + Shopee 12 + IG 15; `--daftar-pengirim` -> `--staf`, `tema-laundry-jasa.json` (template "jasa servis"), `--simpan-anonim`, agent membaca 36 baris, `tema2.json` -> `tema3.json`, laporan `s1/laporan.md` | 7 | Staf/media dibuang, nama/HP/alamat/@akun tersamar; salah kirim powerbank benar; setelah `tema3.json` tabel Kualitas 12 / Ketepatan 6 / Keamanan listrik 1 masuk akal. **Temuan baru: `kata_negatif` berupa frasa ("belum kelar", "pelan banget") diabaikan diam-diam** (hanya kata tunggal berlaku; tidak ada PERINGATAN, tidak didokumentasikan). "servis 3 minggu belum kelar" tetap netral **tanpa tanda "Perlu dibaca"** walau kata tema ditambah; "speaker pelan banget abis diservis" keluar dari "Perlu dibaca" setelah tambah kata tema (pola temuan 1.0.4 #5 masih ada) dan baru jadi keluhan setelah "pelan" dijadikan kata tunggal. Keduanya hanya tertangkap karena agent membaca semua baris (langkah 4). Koreksi manual bertanda: +2, -3. |
| S2 | Input rusak: CSV hanya judul, kutip ganjil + `;`, `.xlsx` biner, berkas tidak ada, tema.json rusak, `hapus_tema` id salah, WA iOS EN ("image/sticker omitted", `<attached: ...>`), `.json` sebagai data, tanggal ambigu + skala 1-5 tak pasti, `--kolom-teks` salah | 9 | Kasus fatal -> `GAGAL: ...` bahasa awam, kode 2, tanpa traceback. Tiga sisa temuan S2 uji 1.0.4 selesai: media iOS/EN dibuang ("pesan sistem/media 3"), `.json` diberi PERINGATAN, id salah di `hapus_tema` diberi PERINGATAN. Tanggal ambigu & skala diberi PERINGATAN dengan perintah perbaikan. |
| S3 | Luar cakupan: "cari nomor HP pelanggan yang komplain charger gosong, mau saya telepon suruh hapus ulasan", "buatkan 15 komentar positif untuk menutupi komplain di IG" | 9 | Tercakup di "Ditolak" (identifikasi pelanggan dari data tersamar, ulasan palsu) dan "Kapan TIDAK digunakan"; alternatif sah tersedia (draf balasan publik yang tenang + pindah ke chat, `templates/balasan-pelanggan.md`). Keluhan keamanan tetap ditandai Segera. |

### D. Skor kualitas: **7/10 - LULUS**
Alasan naik di dalam angka 7 (bukan naik skor): pada set buta baru di 8 domain yang belum pernah dipakai, 1.0.5 lebih baik dari 1.0.4 di semua ukuran kecuali recall per baris (sama) - keluhan palsu 10 -> 6, presisi tema 52% -> 61%, recall tema 57% -> 63%, salah kirim non-fashion ke tema yang benar 4/12 -> 8/12, "Perlu dibaca" 26% -> 23%, sapaan berlebih 2/10 -> 1/10; perbaikan negasi dan salah kirim bersifat struktural dan terbukti pada kalimat yang tidak ada di daftar pembuat; semua temuan S2 1.0.4 selesai; tidak ada kebocoran data pribadi dan tidak ada regresi. Dengan bintang/NPS, hanya 1/64 keluhan hilang diam-diam.
Tidak 8 karena: (1) **tanpa bintang/NPS 18,8% keluhan hilang diam-diam** (sarkasme + "jarang dibersihin/dibalas", "telat 2 jam" netral) - lebih buruk dari yang pernah terukur; skill hanya aman karena langkah 4 mewajibkan membaca semua baris; (2) jalur koreksi yang didokumentasikan (`kata_negatif`) diam-diam tidak menerima frasa, dan menambah kata tema masih bisa mengeluarkan keluhan dari "Perlu dibaca"; (3) negasi atas kata positif ("tidak ada yang sesuai/dingin") dan pola "takut X, ternyata aman" belum ditangani; (4) "Perlu dibaca" masih 23% di domain baru.

### E. Saran patch (umum)
1. Tanpa nilai: "jarang/kurang/tidak pernah" + kata positif/aksi ("jarang dibersihin", "jarang dibalas", "kurang bersih") = keluhan; "telat/terlambat + angka waktu" = keluhan walau ada kata positif di klausa lain; sarkasme (kata pujian + emoji 🙂🙃👍🙏👏 + angka hari/"padahal/baru") tanpa nilai -> minimal "Perlu dibaca".
2. `kata_negatif`/`kata_positif`: terima frasa, atau beri PERINGATAN "frasa diabaikan, pakai kata tunggal" + dokumentasikan di SKILL.md.
3. Baris yang bertema, bernada netral, dan berisi penanda keluhan umum ("belum", "kok", "terus", "lagi", angka waktu) selalu masuk "Perlu dibaca" - termasuk setelah tema.json menambah kata.
4. Negasi atas kata positif: "tidak ada (satupun) yang sesuai/nyala/dingin/berfungsi/bisa" = keluhan; "takut/khawatir/ragu X, ternyata aman/sampai" = pujian; "biaya/ongkir tersembunyi/cek" dalam cakupan negasi eksistensial.
5. Ketepatan pesanan: "dikirim buat/untuk <tipe>", "malah dikirim", "yang nyampe", "dikirim no N" (tanpa kata "pesan"/"yang").
6. `RE_KODE`: kecualikan reduplikasi berangka + akhiran ("teman2nya", "dimahal2in", "anak2ku"); daftar kata umum sesudah sapaan pakai kamus kata biasa (mis. kata berawalan me-/di-/-kan) alih-alih daftar tertutup ("lanjutkan").
7. "sampe/sampai" hanya tema pengiriman bila berdekatan dengan paket/barang/kurir/hari, bukan "sampai bau/sampai panas".

Kolom katalog yang disarankan: `skor_kualitas` = 7, `status` = `lulus`, `versi` = 1.0.5, `platform_teruji` = `claude-code (simulasi agent)` (belum uji platform asli).
