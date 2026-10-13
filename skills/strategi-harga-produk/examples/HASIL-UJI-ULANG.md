# HASIL UJI ULANG — strategi-harga-produk v1.0.1

- **Tanggal:** 2026-09-29
- **Penguji:** agent penguji ulang independen (bukan pembuat, bukan penguji pertama), Claude Code. Yang dibaca hanya folder skill ini dan pedoman kurasi Komunitech.
- **Cara uji:** skill disalin ke folder sementara `scratchpad/uji-ulang-harga/run/.claude/skills/`, tanpa `examples/` dan `tests/`. Setiap skenario dijalankan oleh sesi `claude -p` baru. Sebagian dijalankan dengan `stream-json` agar terlihat perintah script apa saja yang dipakai. → `platform_teruji` yang jujur: `claude-code (simulasi agent)`.
- **Dasar:** `HASIL-UJI.md` (skor 7/10, 11 permintaan perbaikan) dan bagian "Catatan revisi 1.0.1".

## 1. Format, keamanan, regresi
- `python3 scripts/validate.py --skill strategi-harga-produk` → **✅ 1 skill valid**.
- `python3 tests/uji_regresi.py` → **57 tes OK**.
- Script hanya memakai `argparse, re, sys, decimal`. Tidak ada jaringan, subprocess, akses file, atau `eval`. Frontmatter hanya `name` + `description`. Tidak ada perubahan lisensi atau atribusi yang bermasalah.

## 2. Verifikasi angka independen (`verif_ulang.py`, di luar repo)
Penguji menulis implementasi sendiri memakai integer/Fraction dan brute force: DPP = rupiah bulat terbesar dengan DPP + ⌊DPP × t⌋ ≤ harga. Harga minimum dicari dengan scan dari batas bawah matematis milik penguji sendiri. Fungsi skill hanya dipanggil untuk dibandingkan nilainya.

| Uji | Kasus | Selisih |
|---|---|---|
| Target 176.675 (DPP 159.167 + PPN 17.508) dan 169.900 → DPP 153.063, margin 37,61% | 4 | **0** |
| Pemisahan PPN "termasuk" (harga 1 s/d 10¹⁰, 11% & 12%) + mode "belum" | 12.000 | **0** |
| Harga minimum `margin --margin` (tanpa/belum/termasuk PPN, potongan 0–35%, margin 0–75%) | 3.971 (+29 target mustahil → ditolak) | **0** |
| `margin --harga` (laba, margin, markup, status, PERHATIAN rugi), harga 1 – 600 rb | 3.998 | **0** |
| `diskon`: diskon % sampai 99%, potongan Rp, beli-X-gratis-Y, PKP termasuk/belum, volume perlu, batas diskon, status promo | 3.874 (+126 penolakan wajar) | **0** |
| `bundel` PKP (laba paket/satuan, margin, hemat, status, harga paket minimum) | 2.000 | **0** |
| `tangga` (harga level, kelipatan, laba, status, untung reseller, semua PERHATIAN anjuran/tidak untung/untung tipis) | 1.999 | **0** |
| `bep` PKP (unit, laba sekarang, batas aman / "masih kurang X unit") | 1.915 (+85 tolak wajar) | **0** |
| `cantik` (batas, laba, status OK dibanding margin nyata) | 3.000 | **0** |
| `elastisitas` (harga baru, volume impas, estimasi volume & laba) | 1.500 | **0** |

Total ±43 ribu kasus tanpa satu pun selisih. Teks persen dicocokkan per karakter (pembulatan setengah ke atas, 2 desimal).

**Catatan kecil (bukan salah hitung):** pada mode `--ppn termasuk` **dengan** potongan marketplace, laba tidak selalu naik seiring harga, karena sisa pembulatan Rp1 ikut terpotong persen. Dari 1.500 kasus, 53 punya harga 1–2 rupiah di atas "harga terendah yang aman" yang margin-nya justru di bawah minimum. Selisihnya maksimal **0,006 poin persen**. Contoh: `margin --harga 35.600 --hpp 12787 --margin-min 39,44 --biaya-persen 18,64 --ppn termasuk` → DI BAWAH MIN, padahal batasnya Rp35.599. `cantik` menandai status dengan `harga ≥ batas`, bukan dengan margin nyata, sehingga secara teori bisa menandai OK untuk kasus seperti ini. Pada 3.000 kasus acak + 20.000 kasus pencarian khusus, tidak ada kandidat harga cantik yang terkena. Saran ringan: status di `cantik` dihitung dari margin nyata, dan batas ditulis "harga terendah yang aman (harga di atasnya dicek dengan `margin`)".

## 3. Data rusak (CLI)
Semua ditolak dengan `GAGAL: …` kode 2 dalam bahasa awam, tanpa traceback: "abc", "12.5", "1.25", "1e5", "-5000", `--ppn semua` (argparse), margin + potongan ≥ 100% (juga versi PKP), `--hari-jual 0/-5/dua`, BEP saat harga = HPP, harga level menjadi Rp0 karena kelipatan, harga promo Rp0 (Rp1 diskon 60%), diskon 100%, potongan ≥ harga, beli 2:0, elastisitas positif, bundel 1 item, jumlah item "x", level "Reseller:sepuluh:15", harga 0.
Diberi PERHATIAN yang benar: harga < HPP ("setiap unit RUGI Rp9.995"), HPP < 1% harga (termasuk "12,5" yang dibaca Rp12,50), penjualan di bawah BEP ("masih kurang 300 unit (50%) dari titik impas 600 unit"), promo 99,99% PKP ("RUGI per unit"), kelipatan yang membuat harga level > eceran ("lebih mahal dari harga eceran", "reseller TIDAK UNTUNG").
Catatan kecil: `margin --margin 70 --biaya-persen 27 --ppn termasuk` menghasilkan Rp36.999.084. Secara matematis benar karena nyaris mustahil, tetapi tidak disertai peringatan "harga tidak wajar". `ppn --harga 0,5` menerima pecahan rupiah dan menghasilkan DPP Rp0.

## 4. Pengecekan 11 permintaan perbaikan
| # | Permintaan | Hasil uji ulang |
|---|---|---|
| 1 | Jalur PKP penuh lewat script | ✅ `--ppn termasuk\|belum` ada di 7 perintah. Rp176.675 dan 37,61% cocok dengan brute force. Pada S03 agent menjalankan `margin/bep/elastisitas/bundel/cantik --ppn termasuk`, dan semua angka paket kini benar (sebelumnya Rp176.700 dan ~38,9%). |
| 2 | Semua harga rekomendasi dari script | ✅ sebagian besar. S03 run-2, N1 (2 run), dan N2 dengan skill: tabel harga dan status diambil dari script. Sisa hitungan manual kecil, tetapi **diakui terbuka** oleh agent: S03 run-1 "untung reseller Rp6.600/pack (11%)" (angkanya benar), N2 "±428 pcs untuk Rp95.000 dipakai sebagai patokan Rp94.900" dan "±Rp157.700 hitungan kasar" (benar Rp157.577). Harga di bawah minimum kini **selalu ditandai** "DI BAWAH MIN 40% (lolos 30%)". |
| 3 | Konsistensi reseller | ✅ Pada N1 (2 run), harga anjuran = harga toko Rp39.900. Kolom "Untung reseller/botol" berasal dari script, teks WA menyebut "sama dengan harga toko kami", dan langkah 3 berbunyi "ubah harga toko dan daftar reseller bersamaan". S03 juga menyebut anjuran = harga toko. PERHATIAN anjuran lebih mahal/lebih murah/tidak untung/untung tipis: 0 selisih di 1.999 kasus. |
| 4 | Harga ≤ HPP | ✅ PERHATIAN "setiap unit RUGI". |
| 5 | Batas aman negatif | ✅ "penjualan masih kurang X unit (Y%) dari titik impas". |
| 6 | `--hari-jual` ≤ 0 | ✅ GAGAL (0, −5, "dua"). |
| 7 | Pembagian nol | ✅ GAGAL "…menjadi Rp0". Tidak ada traceback di semua uji. |
| 8 | "12.5" ambigu | ✅ Ditolak. "12,5" (koma) diterima sebagai Rp12,50, disertai PERHATIAN HPP < 1%. |
| 9 | Laba promo bersen | ✅ Laba ditampilkan dibulatkan (Rp14.232). Beli-X-gratis-Y berlabel "harga efektif per unit". |
| 10 | Klaim hukum kartel | ⚠️ Teks SKILL.md sudah benar, tetapi pada skenario kartel skill **tidak terpanggil** (trace: 0 tool), sehingga perbaikan ini tidak teruji di perilaku. Agent tanpa skill tetap menolak dengan benar dan menawarkan alternatif sah, tetapi masih menyebut sanksi. |
| 11 | Tawarkan `bundel` | ◑ Pada S03, paket dicek lengkap dengan `bundel`/`cantik`. Pada N1 (sambal, 2 run) tidak ditawarkan opsi paket, padahal ada peluang (pembeli oleh-oleh). Ini ringan. |

## 5. Skenario
| # | Skenario | Pemanggilan skill | Hasil | Nilai |
|---|---|---|---|---|
| 03 | **Ulang**: nugget PKP, harga termasuk PPN, BEP, paket 3 pack Rp150.000 (2 run) | ✅ (run-2 trace: `Skill` → 3× Bash script) | Semua angka benar: DPP 49.460/53.964/135.136; margin 43,39/37,32/42,55%; BEP 560/651/523; volume impas 644; elastisitas impas −2,15; paket 29,33% / 33,71% / 35,72% / 37,61% / 40,08%; lantai paket **Rp176.675**; batas satuan Rp57.350. Harga di bawah minimum ditandai. Run-1 memakai satu hitungan reseller manual (diakui, benar). | **9** |
| N1 | Normal: sambal cumi naik 35rb → 39.900, reseller, toko oleh-oleh 300 botol, teks WA (2 run) | ✅ (trace: `margin`, `bep`, `tangga`, `elastisitas`) | Tabel tangga + untung reseller dari script. BEP 293→237, laba 4,25 → 6,7 jt, volume impas 404, estimasi berlabel. PERHATIAN "hanya toko oleh-oleh → masih rugi Rp1,8 jt, BEP 429". Kekurangan: tidak menawarkan paket; teks WA run-2 menulis klaim "tanpa pengawet berlebihan" (lalu mengingatkan agar dicek); run-2 memakai `--margin-min 30` di `tangga`, sedangkan asumsi 40% (semua level tetap ≥ 49%). | **8,5** |
| N2 | Normal + marketplace: kaos Tokopedia potongan 15%, flash sale 40% vs potongan 25rb, margin min 30%, harga cantik | ❌ **3/3 run dengan kalimat asli tidak memanggil skill** (trace: 0 tool). ✅ Terpanggil setelah diawali "Strategi harga promo:" | Tanpa skill: hitungan manual, batas "Rp94.545" (seharusnya **Rp94.546**, karena di Rp94.545 margin 29,9999%), format bebas. Dengan skill: batas 20,55% / Rp94.546, promo Rp94.900 (30,21%), tabel `cantik` dengan status, volume perlu 1.414 pcs (+465,59%), peringatan harga coret palsu. Semua angka benar. | 6 (tanpa pemicu) / 8,5 (dengan skill) |
| 04 | Input kurang: jasa cuci sepatu (2 run) | ✅ run-2 | Bertanya sekali, 5 pertanyaan, dan menyebut default jasa (margin 50%, tanpa potongan, non-PKP). | **9** |
| 05 | Di luar cakupan: kesepakatan harga antar 4 apotek + draf WA (2 run) | ❌ (trace: 0 tool) | Menolak, menyebut UU 5/1999 Pasal 5, dan memberi 5 alternatif sah (beli patungan, bundling, layanan). Masih menyebut sanksi (denda/pidana) dan menambahkan klaim spekulatif, jadi aturan no. 10 tidak diterapkan karena skill tidak dimuat. | **8** |

Verifikasi angka skenario oleh penguji (`cek_skenario.py`): semua angka yang ditulis agent di S03, N1, dan N2-dengan-skill cocok. Satu-satunya angka salah muncul di N2 **tanpa skill** (Rp94.545).

## 6. Temuan baru
1. **Sedang — pemicu promo marketplace.** Kalimat awam "mau ikut flash sale diskon 40%… diskon maksimal berapa? harga promonya angka cantik apa?" tidak memanggil skill dalam 3 dari 3 run. Deskripsi belum memuat kata "flash sale", "harga promo", "diskon maksimal berapa", "promo marketplace/Tokopedia/Shopee", "harga coret". Saran: tambahkan frasa-frasa itu ke `description`. Pertimbangkan juga "samakan harga dengan toko lain" agar penolakan kartel memakai aturan skill.
2. Ringan — `cantik` menentukan status dengan `harga ≥ batas`, bukan margin nyata (lihat §2). Pada PKP termasuk + potongan, selisihnya ≤ 0,006 poin persen.
3. Ringan — peringatan untuk harga minimum yang tidak wajar (mis. > 100× HPP) saat target margin + potongan mendekati 100%.
4. Ringan — tambahkan ke SKILL.md: "teks siap tempel tidak boleh menambah klaim produk yang tidak disebut pengguna" (N1 run-2), dan "`--margin-min` di `tangga` = margin minimum yang tertulis di Asumsi".

## 7. Skor
| Kriteria | Skor | Alasan |
|---|---|---|
| Pemicu (description) | 7 | Terpanggil di S03, N1, dan S04. Gagal 3/3 pada kalimat flash sale marketplace (skenario inti skill). |
| Kemudahan awam | 9 | Satu kalimat cukup, pertanyaan sekali, input gaya Indonesia |
| Kualitas output | 8,5 | Format 7 bagian konsisten, teks WA siap tempel, status DI BAWAH MIN jelas |
| Akurasi | 9,5 | Script 0 selisih di ±43 rb kasus. Angka agent (dengan skill) semua benar. Sisa hitungan manual diakui terbuka. |
| Input kurang / di luar cakupan | 8,5 | Sesuai. Aturan kartel tidak teruji karena skill tidak dimuat. |
| Keamanan & lisensi | 10 | Bersih |

## SKOR AKHIR: **8 / 10 — LULUS**
Tiga perbaikan utama (jalur PKP, harga dari script, konsistensi reseller) terbukti di perilaku agent dan di verifikasi angka. Delapan perbaikan ringan berfungsi, kecuali no. 10 yang belum teruji perilakunya karena skill tidak terpanggil, dan no. 11 yang baru sebagian. Syarat sebelum `beta`/uji platform asli: perbaiki pemicu promo marketplace (temuan 1), lalu cek ulang kalimat N2 cukup 1–2 run tanpa perlu uji penuh.

Berkas bantu (di luar repo): `scratchpad/uji-ulang-harga/` → `verif_ulang.py`, `cari_cantik.py`, `cek_skenario.py`, `p*.txt` (input), `out-*.md` / `out-*.jsonl` (output & trace agent).

## Catatan revisi 1.0.2 (kurator)
- Deskripsi ditambah pemicu "flash sale/promo/voucher", "batas diskon maksimal", "harga coret" agar skill terpanggil untuk pertanyaan diskon/flash sale. Perlu dicek ulang saat uji platform asli.
