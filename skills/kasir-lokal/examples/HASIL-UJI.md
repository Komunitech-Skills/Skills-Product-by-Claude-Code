# HASIL UJI — kasir-lokal v1.0.0

- **Tanggal:** 2026-09-23 (uji dijalankan hingga 2026-09-24 dini hari)
- **Penguji:** agent penguji independen (simulasi, Claude Code) — bukan pembuat skill; hanya membaca folder `skills/kasir-lokal/`.
- **Lingkungan:** Linux, Python 3.11, DB uji di `/tmp/uji-kasir-lokal/*` (ENV `KOMUNITECH_KASIR_DB` / `--db`), Chromium 1194 headless, OpenClaw 2026.9.5 (HOME sementara).
- **Uji regresi bawaan:** `tests/uji_regresi.py` → 44 tes OK.
- **Platform teruji:** `claude-code (simulasi agent)`; OpenClaw: `skills install --global` + `skills check --json` → kasir-lokal **eligible, modelVisible, commandVisible**; sintaks `automations add/list/run/runs/enable/disable/rm` cocok dengan CLI asli (Gateway tidak dijalankan, Telegram tidak diuji).

## Audit keamanan singkat
Tidak ada impor jaringan (`socket/urllib/http/subprocess` tidak ada); satu `unlink()` hanya menghapus file DB yang **baru gagal dibuat** oleh `init`; tidak membaca kredensial; tidak ada prompt injection di SKILL.md/README/references; data contoh fiktif. CSV ekspor dilindungi formula injection (`= + - @` diberi `'`), HTML struk di-escape (`html.escape`). Aturan "`--ya` hanya setelah pengguna setuju, tidak dari jadwal/instruksi file" tertulis jelas. **Lulus.**

## Skenario
| No | Berkas | Isi | Hasil |
|---|---|---|---|
| 00 | `00-pembanding-tanpa-skill.md` | Uji A/B skenario 01 | Skill **jelas lebih baik** |
| 00 | `00-banding-pesaing.md` | Skill agent sejenis: tidak ada; banding OSPOS/Frappe Books/NexoPOS + celah vs Moka/Majoo | Tidak kalah untuk target |
| 01 | `01-warung-kopi-sehari-penuh.md` | Impor 15 produk (CSV `;`/BOM), 12 nota kalimat campur, void, retur, kas keluar, tutup kasir selisih, rekap + jadwal Telegram, struk 58/80 | Lulus; angka 100% cocok |
| 02 | `02-toko-bangunan-pkp-ppn.md` | PKP: PPN belum/termasuk, kg/meter pecahan, retur pecahan + koreksi PPN, rekap bulanan/tahunan → pph-final-umkm | Lulus angka; cacat parser satuan |
| 03 | `03-kelontong-ekspor-buku-stok-rekap.md` | Ekspor → buku-stok (2× impor + impor ulang), void setelah impor, retur sebagian; ekspor → rekap-penjualan-csv | Lulus; tidak dobel; cacat qty `'-2,5` |
| 04 | `04-input-tidak-lengkap.md` | "catat penjualan tadi" | Tanya sekali, bernomor |
| 05 | `05-di-luar-cakupan.md` | QRIS otomatis / hapus nota untuk pajak / 5 cabang | Ditolak/dibatasi; 2 celah instruksi |
| — | `struk-*.png` | Render Chromium (58/80 mm, PPN, nama emoji) | 58 → PDF 57,8 mm; 80 → 80,1 mm; 1 halaman; emoji terpotong |

## Verifikasi angka independen (script penguji sendiri, tidak mengimpor kode skill)
Rumus ditulis ulang dengan `fractions.Fraction`: baris = qty × harga (rupiah terdekat, .5 ke atas); diskon bertingkat per langkah dari sisa; diskon nota dibagi proporsional (sisa terbesar); PPN belum = ⌊11% × DPP⌋; PPN termasuk = DPP bulat terbesar dengan DPP + ⌊11% × DPP⌋ ≤ harga; retur = nilai sisa sebelum − sesudah; kas seharusnya = kas awal + tunai − kembalian − refund tunai + kas masuk − kas keluar.

| Diuji | Hasil |
|---|---|
| Skenario 01: 12 nota (bruto, total, kembalian, netto per baris vs DB) | **0 beda** |
| Void (alokasi diskon nota 2.667/2.333), retur CAP 18.900 | cocok |
| Tutup kasir: tunai bersih 250.990, seharusnya 425.990, selisih −990; non-tunai QRIS 130.000 / Transfer 97.500 / Debit 37.000 / E-wallet 34.000 | cocok |
| Rekap: kotor 648.000, diskon 24.610, bersih 549.490, rata-rata 51.949, per jam (10 slot), per produk (15) | cocok |
| Skenario 02: 6 nota × 2 mode (netto/DPP/PPN/total vs DB), 2 retur × 2 mode (total/PPN/DPP), omzet & PPN bulanan | **0 beda** |
| PPN vs `skills/hitung-ppn/scripts/hitung_ppn.py` (dijalankan) — 48 nilai × 2 mode | **0 beda** |
| Identitas 12% × 11/12 × DPP = 11% × DPP (tanpa pembulatan berantai) | benar |
| Skenario 03: stok buku-stok setelah 2 impor + void + retur; omzet rekap-penjualan-csv 160.525 = rekap kasir | cocok |

## Verifikasi hukum independen
**(i) PPN 12% × DPP nilai lain 11/12 — TERVERIFIKASI.** DJP (https://www.pajak.go.id/en/node/113453): PMK 131/2024 berlaku 1 Januari 2025; tarif tetap 12%, barang non-mewah memakai nilai lain 11/12 → efektif 11%; barang mewah 12% penuh; dasar Pasal 8A & 16G UU PPN s.t.d.t.d. UU 7/2021 (HPP). Rumus & disclaimer skill sesuai.

**(ii) PBJT makanan/minuman — kini TERVERIFIKASI dari teks resmi** (salinan UU 1/2022 dari DJPK Kemenkeu: https://djpk.kemenkeu.go.id/wp-content/uploads/2022/01/Salinan-UU-Nomor-1-Tahun-2022.pdf ; halaman resmi: https://djpk.kemenkeu.go.id/?p=22499 ; JDIH BPK https://peraturan.bpk.go.id/Details/195660/uu-no-1-tahun-2022 diblokir Cloudflare saat uji, perlu dicek manual oleh pembuat):
| Pasal UU 1/2022 (HKPD) | Isi (ringkas, dari salinan resmi) |
|---|---|
| Pasal 1 angka 42 | PBJT = pajak yang dibayar **konsumen akhir** atas konsumsi barang dan/atau jasa tertentu |
| Pasal 1 angka 44–45 | Makanan dan/atau Minuman = yang disediakan/dijual/diserahkan, langsung/tidak langsung/lewat pesanan **oleh restoran**; Restoran = fasilitas penyediaan layanan makanan/minuman dengan dipungut bayaran |
| Pasal 4 ayat (2) huruf c | PBJT = pajak **kabupaten/kota** |
| Pasal 50 huruf a | Objek PBJT meliputi Makanan dan/atau Minuman |
| Pasal 51 ayat (1) | Yang disediakan oleh (a) **restoran** yang paling sedikit menyediakan meja, kursi, dan/atau peralatan makan-minum; (b) jasa boga/katering |
| Pasal 51 ayat (2) | Dikecualikan: (a) **peredaran usaha tidak melebihi batas yang ditetapkan Perda**; (b) toko swalayan & sejenisnya yang tidak semata-mata menjual makanan/minuman; (c) pabrik makanan/minuman; (d) lounge bandara |
| Pasal 56 | Subjek = konsumen; **Wajib Pajak = orang pribadi/badan yang menjual/menyerahkan** (pemilik usaha memungut) |
| Pasal 57 ayat (1) | Dasar pengenaan = **jumlah yang dibayarkan konsumen** (tidak ada DPP 11/12) |
| Pasal 58 ayat (1), (4) | Tarif **paling tinggi 10%**, ditetapkan dengan Perda |
| Pasal 59 ayat (1) | Pokok PBJT = dasar pengenaan × tarif Perda |
| Pasal 94 | Seluruh jenis pajak & tarif daerah ditetapkan dalam **1 Perda** |
| Pasal 187 huruf b | Perda lama (UU 28/2009, "pajak restoran") berlaku paling lama 2 tahun sejak UU diundangkan (5 Januari 2022) |

**Hubungan dengan PPN:** Pasal 4A ayat (2) huruf c UU PPN s.t.d.t.d. UU HPP — makanan & minuman yang disajikan di hotel, restoran, rumah makan, warung, dan sejenisnya (dikonsumsi di tempat maupun dibawa pulang, termasuk jasa boga/katering) yang merupakan objek pajak daerah **tidak dikenai PPN** (DJP: https://www.pajak.go.id/en/node/81110 ; DDTC: https://news.ddtc.co.id/makanan-dan-minuman-bisa-kena-ppn-bagaimana-ketentuannya-39340). Sebaliknya, makanan/minuman oleh toko swalayan yang tidak semata-mata menjual makanan, pabrik, dan lounge bandara bisa kena PPN (PMK 70/2020 Pasal 4 ayat (4), menurut DDTC — belum dicek teks PMK-nya).

**Penilaian risiko:** pernyataan di `references/pajak.md` & README ("umumnya bukan objek PPN, melainkan PBJT, tarif Perda paling tinggi 10%") **benar**; label BELUM TERVERIFIKASI bisa diganti dengan pasal di atas. Karena README dan SKILL.md jujur menyebut "belum menghitung PBJT" dan mengarahkan ke Bapenda, produk **tidak menyesatkan secara aktif**. Tetapi untuk target utama (kedai kopi/kafe/warung makan dengan meja-kursi), pemilik yang sudah terdaftar wajib PBJT/PB1 **tidak bisa** memungut dan mencetak PBJT di struk, tidak bisa memisahkan PBJT dari omzet, dan rekap tidak menyiapkan setoran PBJT bulanan — gap fungsional besar (lihat cacat S1). Risiko salah pakai: pengguna kafe yang ingin "pajak 10%" bisa mencoba mode PPN (diblok bila tidak `--pkp ya`, tapi bisa lolos bila ia menjawab "ya PKP") → PPN 11% efektif padahal objeknya bukan PPN.

## Data rusak & tepi
| Uji | Hasil |
|---|---|
| Nama produk sangat panjang + emoji, nama toko panjang + em dash | Dibungkus rapi; **emoji dihitung 1 kolom padahal tampil 2 → tepi kanan terpotong** ("(FIKTIF" kehilangan ")", "Sri 😊" terpotong) — `struk-58mm-emoji-terpotong.png` |
| Harga 0 / negatif / ilmiah `1,5E+04` / sen `15.000,50` / format Inggris `1,250.00` / kode ganda / stok pecahan utk pcs / kode kosong | Semua ditolak per baris dengan alasan jelas; kode kosong diberi `P001` |
| CSV kosong / tanpa kolom wajib / `.xlsx` / Windows-1252 | Pesan jelas; cp1252 terbaca (Café) dengan peringatan. Kode non-ASCII (`CAFé`) ditolak — teks non-JSON hanya "Tidak ada produk yang bisa diimpor" tanpa alasan baris (alasan ada di JSON) |
| qty 0, qty negatif, pecahan untuk porsi, diskon 110%, diskon > harga, harga di pesanan `@20rb`, bon/utang | Semua ditolak dengan pesan jelas |
| Bayar kurang / non-tunai melebihi total / dua metode tanpa jumlah / `15.000.00` | Ditolak, menyebut kekurangan |
| Nota duplikat < 10 menit | Pratinjau bertanya; `--ya` ditolak tanpa `--izinkan-duplikat` |
| DB terkunci (proses kedua `BEGIN EXCLUSIVE`/`IMMEDIATE`) | Tulis & baca menunggu lalu gagal dengan pesan ramah; data tidak rusak |
| Formula injection ekspor (`=HYPERLINK`, `@SUM`, `+62`) | Diberi `'` — aman. **Efek samping:** qty pecahan negatif `-2,5` juga jadi `'-2,5` |
| Stok mode `kasir` + ekspor buku-stok | Peringatan "stok terpotong DOBEL" muncul |
| Zona waktu | Waktu naif jam komputer: TZ=UTC mencatat 00:37, WIB 07:37, WIT 09:37 untuk transaksi yang sama; tidak ada pengaturan zona waktu toko |

## Skor per kriteria
| Kriteria | Skor | Alasan |
|---|:-:|---|
| Pemicu (description) | 9 | Spesifik, ID+EN, 477 karakter; mencakup kata "catat penjualan/struk/tutup kasir/rekap kasir/cashier/POS" |
| Kemudahan awam | 8 | Kalimat biasa, pratinjau → "ya"; hambatan: satuan milik produk ("2 sak semen") ditolak, dan setiap nota perlu konfirmasi |
| Kualitas output | 9 | Struk rapi 58/80 mm (PDF lebar pas), tutup kasir & rekap siap kirim, jejak void/retur |
| Akurasi (angka/fakta) | 10 | Semua angka cocok independen & dengan hitung-ppn; dasar hukum PPN/PBJT benar |
| Penanganan input kurang | 9 | Tanya sekali bernomor, default tunai pas disebut, ambigu tidak ditebak |
| Penanganan di luar cakupan | 7 | QRIS & multi-cabang jelas; tidak ada larangan eksplisit void untuk mengecilkan omzet; tidak ada alternatif multi-cabang |
| Keamanan | 9 | Tanpa jaringan, pratinjau wajib, backup otomatis, anti-injection, penanganan lock |

## Cacat & saran perbaikan

### BERAT
Tidak ada.

### SEDANG
1. **Tidak ada mode PBJT/PB1 untuk usaha makanan-minuman** (target utama README). Saran: tambah `--pajak pbjt-belum|pbjt-termasuk --tarif-pbjt N` (N ≤ 10, wajib diisi pengguna dari Perda/SKPD; tolak > 10), dasar = jumlah dibayar konsumen setelah diskon (Pasal 57), tanpa DPP 11/12, larang kombinasi dengan PPN untuk item yang sama; rekap bulanan menampilkan "PBJT dipungut" + omzet tanpa PBJT; langkah A.1 SKILL.md menambah pertanyaan "Usaha makanan/minuman dengan meja-kursi? Sudah terdaftar pajak restoran/PBJT di Bapenda? Tarifnya?". Ganti label BELUM TERVERIFIKASI di `references/pajak.md` §PBJT dengan pasal & URL di atas. Pembulatan PBJT: sebutkan belum dicocokkan dengan aplikasi pajak daerah setempat.
2. **Parser satuan** (`buang_satuan`, `SATUAN_PECAHAN`): `2 sak semen`, `2 pail cat`, `semen 2 sak`, `2 dus aqua`, `3 lembar triplek` ditolak "tidak dikenal"; m3/m2/ton tidak boleh pecahan (`0,5 m3 pasir` ditolak). Saran: di `cmd_jual` panggil `buang_satuan(nama, p_satuan)` dengan **semua satuan yang ada di tabel produk** (bukan hanya "pcs") + daftar umum (sak, zak, dus, pak, lembar, batang, rol, pail, ikat); tambah `m2, m3, kubik, ton, cc` ke `SATUAN_PECAHAN`; terapkan pembuangan satuan juga di `cmd_retur` (sekarang `0,75 kg kawat bendrat` gagal).
3. **Tidak ada larangan eksplisit manipulasi omzet.** SKILL.md "Aturan keamanan data" perlu butir: "Jangan void/retur penjualan yang benar-benar terjadi untuk mengecilkan omzet/pajak atau atas permintaan 'hapus nota'; tolak dan tawarkan cek batas Rp 500 juta PPh final." (lihat 05b).
4. **Zona waktu toko**: waktu memakai jam komputer tanpa zona; di VPS (pilihan "mesin 24 jam") yang default UTC, nota tercatat 7 jam lebih awal dan rekap per jam/tanggal salah. Saran: pengaturan `--zona Asia/Jakarta` di `init/atur` (pakai `zoneinfo`, Python ≥ 3.9, fallback offset tetap +7/+8/+9), dan `info` memperingatkan bila zona komputer ≠ zona toko.

### RINGAN
5. CSV penjualan: qty pecahan negatif ditulis `'-2,5` (sel teks di Excel; SUM Qty salah). Di `baris_csv_penjualan`/`qty_csv`, jangan lewatkan angka ke `sel_aman`, atau kembalikan float lalu format di writer.
6. Struk: lebar emoji/karakter lebar dihitung 1 kolom → terpotong di kanan (`_kiri_kanan`, `_bungkus`). Pakai `unicodedata.east_asian_width` (W/F = 2) atau buang emoji dari struk (printer thermal umumnya tidak bisa mencetak emoji).
7. `struk --teks` menaikkan penghitung cetak → cetak kertas pertama berlabel "SALINAN". Hitung hanya untuk file HTML/cetak.
8. "Rata-rata/nota" ikut menghitung nota yang di-void (`hitung_rekap`); kecualikan nota berstatus void.
9. Nota yang diretur sebagian tidak diberi tanda "ada retur R-…" saat struknya dicetak ulang; nama kasir sesi tidak otomatis ke struk.
10. Nota susulan setelah tutup kasir memberi peringatan "Kasir belum dibuka", padahal kasir *sudah ditutup*, dan saran "buka kasir dengan --waktu sebelum jam nota" tidak bisa dijalankan (ditolak karena sebelum tutup terakhir). Bedakan pesannya.
11. `produk impor` tanpa `--json`: bila semua baris rusak, teks hanya "Tidak ada produk yang bisa diimpor." tanpa alasan per baris — sertakan daftar baris rusak di teks.
12. SKILL.md 5c: tambahkan alternatif multi-cabang (satu DB per cabang + gabung CSV di rekap-penjualan-csv).

## SKOR AKHIR: **8 / 10 — LULUS**
Alasan: inti kasir (hitung, pajak PPN, void/retur, tutup kasir, rekap, ekspor ke skill lain) terbukti **akurat 100%** lewat verifikasi independen, aman, dan jauh lebih baik daripada agent tanpa skill; tidak ada pesaing agent skill yang sebanding. Nilai tidak lebih tinggi karena (a) belum ada mode PBJT untuk segmen kuliner yang justru disasar, (b) parser satuan gagal pada kalimat lazim toko bangunan/grosir, (c) celah instruksi manipulasi omzet, dan (d) zona waktu. Perbaiki cacat SEDANG 1–4 sebelum beta untuk member F&B; setelah revisi, uji ulang oleh penguji independen (terutama mode PBJT bila ditambahkan).

## Catatan koordinator — v1.1.0
Mode PBJT (pajak daerah makanan/minuman restoran), satuan, larangan manipulasi nota, zona waktu, dan cacat ringan ditambahkan pembuat; 64/64 tes lulus (dicek ulang koordinator). Karena PBJT adalah perhitungan pajak BARU yang belum diuji independen, status diturunkan sementara ke `uji` sampai uji ulang independen v1.1.0 selesai.
