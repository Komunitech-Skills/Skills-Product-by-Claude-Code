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
