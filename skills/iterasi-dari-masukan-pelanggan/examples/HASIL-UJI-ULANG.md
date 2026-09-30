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
