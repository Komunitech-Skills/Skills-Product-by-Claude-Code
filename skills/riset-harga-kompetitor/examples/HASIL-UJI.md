# HASIL UJI - riset-harga-kompetitor v1.0.0

- **Penguji:** agent independen (bukan pembuat), hanya membaca folder skill + CLAUDE.md. Model: Opus.
- **Tanggal:** 2026-09-28. Lokasi uji: scratchpad (salinan folder skill), bukan `.claude/skills/`.
- **Platform:** `claude-code (simulasi agent)`. Uji muat OpenClaw (`scripts/uji_openclaw.sh`) **belum** dijalankan penguji (di luar folder skill) - wajib dijalankan kurator.

## Skor: **6 / 10 - REVISI dulu** (perkiraan 8 setelah T1-T3, T6-T7 diperbaiki)

Alasan singkat: inti hitungan **sempurna** (117 nilai diverifikasi ulang dengan Decimal independen, **0 selisih**; contoh pembuat terreproduksi identik; 22 uji regresi lulus), cakupan & etika web sangat baik, A/B dan banding pesaing menang jelas. Namun tugas utama skill - **menyetarakan ukuran** - salah **diam-diam** pada penulisan ukuran yang sangat umum di Indonesia (`1/2 kg`, `250 g x 2`), dan baris salah itu tetap ikut statistik. Untuk produk berbayar yang menjanjikan "reliable", ini harus diperbaiki sebelum `lulus`.

## Ringkasan skenario
| # | Skenario | Hasil | Catatan |
|---|---|---|---|
| 00 | A/B tanpa vs dengan skill | Dengan skill jelas lebih baik | Minimum, median/kuartil, tabel, duplikat, link gagal |
| 00 | Banding pesaing (phuryn/pm-skills pricing-strategy ±26,6k★; OneWave competitor-price-tracker ±309★) | Menang telak (8,7 vs 3,0 vs 2,3) | Pelajari: "asumsi + cara menguji harga" |
| 01 | Kopi 250 g vs 200/500 g/1/2 kg/1 kg, 1 data web nyata | Lulus setelah koreksi input | Bug T1 & T7 muncul |
| 02 | Hijab voal 8 pesaing, rentang & promo, premium | Lulus | T4 (premium), T11 |
| 03 | Dimsum frozen + HPP + biaya Shopee, murah | Lulus setelah koreksi input | Bug T2, T9; PERHATIAN bekerja baik |
| 04 | Tanpa HPP | Lulus (aman) | T5: pertanyaan "harga pasaran" tertunda |
| 05 | Bot auto-repricing + scraping login Shopee | Lulus (ditolak sopan + alternatif) | - |

## Jalur web (dicoba sungguhan, tanpa login, 3 halaman)
| Halaman | Hasil |
|---|---|
| infokopi.com/product/jual-kopi-aceh-gayo/ | Berhasil: Kopi Arabika Aceh Gayo 250gr, Rp 80.000 -> dipakai di uji 01 |
| shopee.co.id/BUBUK-KOPI-ARABIKA-GAYO-250-GRAM-i.450270972.28311393933 | Kosong (render JS/perlu login) -> fallback tempel teks |
| azakopigayo.co.id/product/kopi-arabika-gayo-super-premium/ | HTTP 503 -> fallback tempel teks |
Instruksi SKILL.md (jangan coba cara lain, minta teks/screenshot, laporkan link gagal) sesuai kenyataan dan mudah diikuti.

## Verifikasi angka independen
`verif.py` penguji: harga pesaing diketik manual dari data mentah (tidak memakai parser script), hitung ulang setara, persentil (PERCENTILE.INC), balik modal & minimum (ceil), rentang/titik per strategi dengan batas minimum, harga cantik (cari semua kandidat ...900), laba/margin, posisi harga kita.
| Kasus | Nilai dicek | Selisih |
|---|---|---|
| S1 mentah / S1 benar | 19 / 19 | 0 / 0 |
| S2 / S2 per pcs | 15 / 15 | 0 / 0 |
| S3 mentah / S3 benar | 17 / 17 | 0 / 0 |
| Data rusak (b1) | 15 | 0 |
| **Total** | **117** | **0** |
Per 100 g dicek manual (mis. 42.500/200x100 = 21.250 ✓). Contoh pembuat (`contoh-pembuat-kopi-gayo.md`) dijalankan ulang: output identik.

## Uji data rusak (script)
| Input | Hasil | Nilai |
|---|---|---|
| `Rp49.900`, `49,9rb`, `Rp 1,2 jt`, `Rp49.900,-`, `49 900`, `0,5jt`, `49.999,50` | Terbaca benar | ✓ |
| `49.900-59.900`, `45rb–55rb`, `49-59rb`, `49.900 - 59rb` | Rentang benar, dipakai terendah | ✓ |
| `49,9`, `49.9`, `49900.50` | Ditolak "ambigu", baris dilewati + alasan | ✓ |
| kosong, `-49.900`, `Rp 0`, `hubungi penjual`, `1.2.3` | Ditolak + alasan | ✓ (`Rp -49.900` pesannya "kosong", T10) |
| duplikat (URL sama www/tanpa www/parameter; isi sama) | Dibuang + dilaporkan | ✓ |
| satuan campur (ml vs g, sachet vs g, "1 pack") | Dikeluarkan + alasan | ✓ |
| `5 ons` = 500 g, `12x25g`, `2 x 250 gr`, `1,5 L`, `1.000 ml` | Benar | ✓ |
| **`1/2 kg` -> 2.000 g, `1/4 kg` -> 4.000 g** | **Salah, diam-diam** | T1 |
| **`250 g x 2`, `250gr x 2 pcs`, `isi 2 @250gr`, `250 g + 250 g` -> 250 g; `Paket 2 pcs @ 250 gr` -> 2 pcs** | **Salah** | T2 |
| file header saja (0 baris), file kosong, JSON rusak, file tidak ada, kolom harga tak dikenal | `ERROR:` + exit 2 | ✓ (pesan generik, T10) |
| CSV kutip tidak seimbang | `ERROR` tidak ada harga terpakai | ✓ aman |
| CSV `;` dan tab + BOM | Terbaca | ✓ |
| **CSV non-UTF-8 (Excel Windows/ANSI) atau biner** | **Traceback, exit 1** | T6 |
| **Nilai berkoma tanpa kutip (`1,2RB terjual`)** | Kolom bergeser tanpa peringatan | T7 |
| JSON `"harga": 49.9` (angka) | Diterima sebagai **Rp 50** | T8 |
| HPP 0/teks, biaya+margin ≥ 100%, biaya 120%, ukuran "sebungkus", `--tanggal kemarin` | `ERROR:` jelas, exit 2 | ✓ |

## Temuan menurut tingkat keparahan
**TINGGI**
- **T1 - Pecahan ukuran salah dibaca.** `1/2 kg` -> 2.000 g, `1/4 kg` -> 4.000 g (regex menangkap angka setelah `/`). "1/2 kg" dan "1/4 kg" sangat umum di teks marketplace Indonesia. Harga setara jadi 4-16x salah. Perbaikan: dukung `a/b` (dan "setengah"), atau tolak baris dengan pecahan + alasan. Tambah uji regresi.

**SEDANG**
- **T2 - Pengali di belakang / paket tidak dikenali.** `250 g x 2`, `250gr x 2 pcs`, `isi 2 @250gr`, `250 g + 250 g` dibaca 250 g; `Paket 2 pcs @ 250 gr` dibaca 2 pcs. Uji 03: setara Rp 88.000 (benar Rp 44.000), P75 dan tertinggi salah. Perbaikan: pola `N sat x K`, `K x @N sat`, `N sat + N sat`; bila ragu tolak baris dengan alasan.
- **T3 - Baris "jauh dari median" tetap ikut statistik.** Justru baris salah baca (T1, T2, T8) terdeteksi di sini tetapi tetap menggeser terendah/tertinggi dan, pada n kecil, P25/P75. Usul: keluarkan dari statistik (tetap tampil di tabel) atau wajibkan agent mengonfirmasi ke pengguna sebelum menyajikan hasil. Tambahkan ke checklist SKILL.md: "cek setiap baris bercatatan jauh dari median".
- **T4 - Desain strategi premium.** Premium = [median..P75] adalah **subset** dari tengah [P25..P75]; hasilnya bukan premium (uji 02: premium Rp 42.000-44.750, di bawah 2 pesaing). Murah [min..P25] dan tengah [P25..P75] bersinggungan di P25 (wajar). Usul: premium = [P75..P90 atau maks], titik P75 (atau nama diganti "tengah-atas").
- **T5 - HPP wajib walau pertanyaan hanya "harga pasaran berapa".** Script menolak jalan; statistik pasar tertunda. Usul: mode pasar-saja bila HPP kosong (bagian batas harga & rekomendasi diganti permintaan HPP).
- **T6 - CSV non-UTF-8 membuat traceback.** CSV dari Excel Windows sering ANSI/cp1252. Usul: coba `utf-8-sig`, lalu `cp1252`; tangkap `UnicodeDecodeError` jadi `ERROR:` exit 2.
- **T7 - Jumlah kolom tidak cocok tidak diperingatkan.** Nilai berkoma tanpa kutip menggeser kolom (terjual 1, lokasi "2RB terjual"). Usul: peringatan per baris bila `DictReader` menghasilkan kunci `None`/nilai `None`; di SKILL.md minta agent memberi tanda kutip pada nilai berkoma atau memakai JSON.

**RENDAH**
- **T8** - Harga JSON numerik `49.9` diterima sebagai Rp 50 (tidak konsisten dengan penolakan `"49,9"`). Usul: tolak harga < 100 (atau < 1.000 dengan konfirmasi).
- **T9** - `isi 10 pcs 250 gr` dibaca 10 pcs (pola pertama menang) sehingga dikeluarkan padahal berat tersedia. Usul: bila teks memuat beberapa dimensi, pilih dimensi yang sama dengan produk kita.
- **T10** - Pesan kurang tepat: `Rp -49.900` -> "kosong"; `--margin -5` -> "bukan angka"; kolom harga tidak ditemukan -> pesan generik; duplikat URL dengan harga berbeda dibuang tanpa menyebut beda harga; "x dari N pesaing memasang harga coret" memakai N termasuk baris yang dikeluarkan.
- **T11** - Produk tanpa berat/isi (hijab): bila hanya satu pesaing punya ukuran (`2 pcs`), tidak ada peringatan dan paket dibandingkan apa adanya. Usul: peringatan bila sebagian baris punya ukuran dan sebagian tidak; SKILL.md: "produk satuan -> tulis `1 pcs`".
- **T12** - Saran: tambahkan "cara menguji harga baru" (pelajaran dari pesaing pricing-strategy).

## Penilaian pilihan desain pembuat
| Pilihan | Penilaian penguji |
|---|---|
| murah = min..P25, tengah = P25..P75, premium = median..P75 | Murah & tengah OK. **Premium tumpang tindih penuh dengan tengah** -> perbaiki (T4). |
| `49,9` tanpa "rb" ditolak | **Setuju** (aman, minta klarifikasi). Samakan perilaku untuk angka JSON (T8). |
| Satuan campur dikeluarkan, tidak dikonversi | **Setuju** (konversi g<->ml<->pcs butuh densitas/berat per pcs, rawan salah). Perbaiki prioritas dimensi (T9). |
| Rentang harga memakai harga terendah | **Setuju sebagai default** (harga "mulai dari" yang dilihat pembeli, dan catatan per baris jujur). Tambah di SKILL.md: bila pengguna menempel daftar varian, catat harga varian yang sebanding, bukan rentangnya. |
| Minimum dibulatkan ke atas, nilai lain ke terdekat | **Setuju** (konsisten dengan standar pembulatan repo; menjamin target margin). |
| Pencilan hanya ditandai | **Kurang** - lihat T3. |

## Kekuatan
- Hitungan Decimal eksak, rumus tertulis & dapat diaudit, rekomendasi tidak pernah di bawah minimum, PERHATIAN jelas saat pasar di bawah batas untung.
- Parser harga Indonesia sangat kuat (rb/jt/k, `,-`, rentang, s/d, en-dash, spasi ribuan).
- Etika web tepat: tanpa login/bypass, tanpa jaringan di script (hanya `urllib.parse`), fallback tempel teks.
- Frontmatter hanya `name` + `description` (728 karakter). SKILL.md 115 baris. README lengkap sesuai Tahap 8.

## Rekomendasi sebelum `lulus`
1. Perbaiki T1, T2 (+ uji regresi `1/2 kg`, `1/4 kg`, `250 g x 2`, `isi 2 @250gr`, `Paket 2 pcs @ 250 gr`).
2. Perbaiki T3, T6, T7; putuskan T4 (desain premium).
3. Jalankan `bash scripts/uji_openclaw.sh`.
4. Uji ulang oleh penguji independen (fokus data ukuran & CSV).

Artefak uji penguji (CSV, output, `verif.py`) ada di scratchpad sesi: `uji-riset-harga/{data,out,verif.py}`.
