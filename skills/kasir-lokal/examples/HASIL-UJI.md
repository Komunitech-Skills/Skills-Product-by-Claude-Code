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

---

# Uji ulang v1.1.0 — 2026-09-24

- **Penguji:** agent penguji independen (simulasi, Claude Code), bukan pembuat. Hanya membaca folder skill; DB uji di `/tmp/uji-kasir-lokal/{v11,kafe,reg,mig,tz}`.
- **Tes bawaan:** `tests/uji_regresi.py` → 64 tes OK.
- **OpenClaw 2026.9.5:** `skills install --global` + `skills check --json` → kasir-lokal **eligible, modelVisible, commandVisible**.

## 1. Verifikasi angka PBJT (script penguji sendiri, hanya memanggil CLI; `verif/verif_pbjt.py`)
Model independen (Fraction): baris & diskon seperti v1.0.0; service charge = rupiah terdekat dari SC% × total setelah diskon; `pbjt-belum`: dasar = total setelah diskon (+ SC bila `--sc-kena-pajak ya`), PBJT = ⌊tarif × dasar⌋, total = dasar + PBJT (+ SC bila tidak kena); `pbjt-termasuk`: dasar = rupiah bulat terbesar dengan dasar + ⌊tarif × dasar⌋ ≤ harga; retur/void = nilai(sisa sesudah) − nilai(sisa sebelum) untuk dasar, SC, PBJT, total.

| Sapuan | Isi | Hasil |
|---|---|---|
| 20 konfigurasi × 3 seed | tarif 2,5% / 5% / 7,125% / 10% × {termasuk; belum tanpa SC; SC 5% kena; SC 5% tidak kena; SC 10% kena} | — |
| 900 nota | 1–4 produk acak (harga ganjil 4.000–41.900, produk kg pecahan 0,25–10), diskon item %/bertingkat/nominal/7,5%, diskon nota %/nominal/bertingkat | **0 beda** (netto, SC, dasar, PBJT, total) |
| ±560 retur sebagian & void | retur separuh baris (termasuk kg pecahan), lalu sebagian di-void sisanya; void penuh | **0 beda** (koreksi dasar, SC, PBJT, uang kembali). 4 "beda" = void atas nota yang sudah diretur penuh → script menolak dengan benar (artefak skrip uji) |
| 60 rekap bulanan | Σ PBJT dipungut, uang diterima, omzet tanpa PBJT | **0 beda** |
| Contoh di SKILL.md | 45.900 @10% → 4.590 → 50.490; termasuk 53.000 → dasar 48.182, PBJT 4.818 | benar |
| Migrasi DB v1.0.0 | DB dibuat kode v1.0.0 (git `c8c079c`, mode PPN termasuk) → dibuka v1.1.0 → retur nota lama (PPN −2.029/−4.059, sama persis dgn v1.0.0) → `atur` ke PBJT 10% → nota baru PBJT 6.850; retur nota lama tetap memakai PPN (pengaturan per nota) → rekap: PPN 71.561, PBJT 6.850, omzet 719.064 | cocok hitungan manual |

**Kesesuaian dengan UU 1/2022:** Pasal 57 ayat (1) dasar = jumlah yang dibayar konsumen → dipakai total setelah diskon, **tanpa** 11/12 ✓. Pasal 58 ayat (1)/(4) tarif ≤ 10% via Perda → tarif wajib diisi pengguna, 0/negatif/10,5/11 ditolak, desimal (2,5; 7,125) diterima ✓. Pasal 59 ayat (1) pokok = dasar × tarif ✓. Penggabungan PPN+PBJT ditolak dengan rujukan Pasal 4A ayat (2) huruf c UU PPN ✓.

**Pembulatan & disclaimer — jujur:** UU tidak mengatur pembulatan per nota; pilihan ⌊…⌋ sekali (tidak pernah memungut melebihi tarif) konsisten dengan standar library, dinyatakan sebagai *keputusan desain* di `references/pajak.md`, dan disclaimer rekap/struk menyebut "Pembulatan belum dicocokkan dengan sistem pajak daerah/Bapenda … tanyakan Bapenda". Service charge tidak diputuskan skill (wajib `--sc-kena-pajak`) — konservatif dan jujur; saran: tambahkan catatan bahwa Pasal 57 memakai "jumlah yang dibayarkan konsumen", sehingga SC yang dibayar konsumen **lazim** ikut dasar — tetap ikuti Perda.

## 2. Skenario kafe end-to-end (PBJT 10% + SC 5% kena pajak, WIB) — `/tmp/uji-kasir-lokal/kafe`
**A.1 (pertanyaan agent sesuai SKILL.md):** "(1) nama, alamat, telp, kota (WIB/WITA/WIT); (2) daftar menu; (3) kafe dengan meja-kursi: sudah terdaftar PBJT/pajak restoran di Bapenda? tarif di Perda/SKPD? harga menu sudah termasuk pajak? ada service charge, dan menurut Bapenda ikut dikenai pajak? (4) stok; (5) printer 58/80." → Jawaban fiktif: terdaftar, 10%, belum termasuk, SC 5% ikut dikenai.
`init --pajak pbjt-belum --tarif-pbjt 10 --service-charge 5 --sc-kena-pajak ya --zona WIB` → "Pajak: PBJT makanan/minuman 10% (harga menu belum termasuk PBJT) | Service charge 5% (kena pajak) | Zona: Asia/Jakarta (WIB)". Tanpa tarif → ditolak ("Tarif tidak diisi otomatis…"); SC tanpa `--sc-kena-pajak` → ditolak.

| Jam | Pesan | Subtotal | SC 5% | Dasar | PBJT | Total | Bayar/kembalian |
|---|---|---:|---:|---:|---:|---:|---|
| 08:20 | dua kopi susu, satu roti bakar keju, catatan: meja 3, bayar tunai 100rb | 53.000 | 2.650 | 55.650 | 5.565 | 61.215 | T 100.000 / 38.785 |
| 09:05 | 3 es teh manis diskon 10%+5%, 2 indomie, bayar qris | 42.390 | 2.120 | 44.510 | 4.451 | 48.961 | QRIS |
| 11:30 | 1 americano, 2 cappuccino diskon 2rb, diskon 10%, bayar tunai 80rb | 55.800 | 2.790 | 58.590 | 5.859 | 64.449 | T 80.000 / 15.551 |
| 12:45 | lima indomie, 5 es teh lemon, bayar qris 50rb, tunai 80rb | 107.500 | 5.375 | 112.875 | 11.287 | 124.162 | QRIS 50.000 + T 80.000 / 5.838 |
| 15:10 | 2 kentang goreng, 1 coklat panas, bayar debit → **void 15:15** | 43.000 | 2.150 | 45.150 | 4.515 | 49.665 | Debit, dikembalikan Debit 49.665 |
| 19:40 | kopi susu 3, pisang goreng 2, bayar tunai 150rb | 78.000 | 3.900 | 81.900 | 8.190 | 90.090 | T 150.000 / 59.910 |
| 11:40 | retur 1 cappuccino (tumpah) dari nota 11:30 | −18.900 | −945 | −19.845 | −1.985 | −21.830 | Tunai |

(Pesan 12:45 awalnya "bayar qris 50rb, tunai 50rb" → "Pembayaran KURANG Rp 24.162" — pembayar kurang tertangkap.)

Struk 58 mm (Chromium → PDF 57,8 × 100,9 mm, 1 halaman, `scrollWidth = clientWidth`; `struk-58mm-kafe-pbjt.png`):
```
   KAFE TERAS SENJA (FIKTIF)
   Jl. Contoh No. 7, Jakarta
            Selatan
         0812-0000-2222
--------------------------------
No                 N-260924-0001
Tgl         24/09/2026 08:20 WIB
Kasir                      Dimas
--------------------------------
Kopi Susu Gula Aren
  2 cup x 18.000          36.000
Roti Bakar Keju
  1 porsi x 17.000        17.000
--------------------------------
Subtotal                  53.000
Service 5%                 2.650
Dasar PBJT                55.650
PBJT 10%                   5.565
TOTAL                  Rp 61.215
Tunai                    100.000
Kembalian                 38.785
Catatan: meja 3
--------------------------------
 Struk ini bukan faktur pajak.
          Terima kasih
```
Mode `pbjt-termasuk` (DB terpisah): 53.000 → "TOTAL Rp 53.000 (sudah termasuk PBJT 10%) | Dasar PBJT Rp 48.182 | PBJT Rp 4.818" ✓.

**Tutup kasir:** kas awal 300.000 + tunai bersih 268.086 − kas keluar 30.000 = **538.086** (dihitung ulang manual: 61.215 + 64.449 + 74.162 + 90.090 − 21.830 = 268.086 ✓); fisik 537.500 → "SELISIH KURANG Rp 586"; non-tunai QRIS 98.961 ✓.

**Rekap harian/bulanan:** kotor 390.500, diskon −10.810, retur/void −61.900, bersih 317.790, **Service charge 15.890, PBJT dipungut 33.367**, uang diterima 367.047, **omzet tanpa PBJT 333.680**, rata-rata 77.775 (tanpa nota void) — semua dicek manual ✓. Rekap bulanan menambah "PBJT yang dipungut … Rp 33.367: setor & laporkan ke Bapenda … (kasir tidak menyetor)" + disclaimer UU 1/2022 Pasal 50–58.
**→ pph-final-umkm:** `rekap --tahun 2026` memberi `pph_final.py --jenis op --tahun 2026 --bulan-awal 9 --omzet 333680`; dijalankan sungguhan → Rp 0 (masih dalam Rp 500 juta bebas) ✓. Omzet PPh = uang diterima − PBJT (termasuk SC) — wajar sebagai peredaran bruto.

## 3. Regresi skenario 01–03 (kode v1.1.0, input sama)
| Skenario | Hasil |
|---|---|
| 01 warung kopi | 12 nota vs model independen: **0 beda**; tutup kasir 425.990 / kurang 990 **sama**; rekap kotor/diskon/bersih/metode/produk **sama**. Berubah (disengaja): rata-rata 51.949 → **51.672** (tanpa void, cocok hitungan uji v1.0.0); baris "11.00–11.59 1 nota Rp 55.000" (nota yang di-void) tidak lagi muncul di "Per jam" — konsisten dengan aturan tanpa void, tetapi **tidak disebut** di klaim pembuat (catat di changelog). |
| 02 toko bangunan PKP | PPN kedua mode, retur, omzet & PPN bulanan: **0 beda** (1.600.795 / 176.086; 1.442.161 / 158.634). Retur `0,75 kg kawat bendrat` kini diterima. |
| 03 kelontong | Ekspor buku-stok **identik byte-per-byte** dengan v1.0.0; rekap bersih 160.525 sama; rekap-penjualan-csv 160.525; rata-rata 57.150 → **56.833** (disengaja). CSV kini menulis `-2,5` sebagai angka ✓. |

## 4. Uji perbaikan lain
| Butir | Hasil |
|---|---|
| Satuan | `2 sak semen`, `semen 2 sak`, `semen sak 2`, `2 pail cat`, `0,5 m3 pasir`, `pasir 1,5 m3`, `setengah m3 pasir`, `3 batang besi`, `besi 3 batang`, `2 lembar triplek`, `12,5 m2 keramik`, `0,75 ton batu split`, `2 dus aqua`, `5 m kabel`, `2 semen 50 kg` (varian berisi "kg") ✓. Ditolak benar: `1,5 sak semen` (pecahan), `2 kg semen` & `2 meter semen` (satuan tak cocok), `2 lusin paku` (dengan petunjuk 1 lusin = 12). Penyempitan: `3 kg gula pasir` → produk kg, `1 karung gula pasir` → produk karung ✓. Retur `2,5 meter pipa pvc` ✓. |
| Larangan manipulasi (aturan 7) | Ada, jelas, dengan alternatif sah; rujukan UU KUP Pasal 39 ayat (1) sesuai isi umum pasal (menyampaikan SPT/keterangan tidak benar, memperlihatkan pembukuan palsu) — teks pasal belum dibuka penguji. Checklist menambah butir ✓. |
| Multi-cabang | Alternatif satu DB per cabang + gabung CSV → rekap-penjualan-csv tertulis di SKILL.md ✓. |
| Zona waktu (komputer TZ=UTC, 01:06 UTC) | `--zona WITA` → nota "24/09/2026 09:06 WITA" sama untuk TZ=UTC/Asia/Jakarta/America/New_York ✓; tanpa tzdata (`PYTHONTZPATH=/nonexistent`) fallback offset tetap → 09:06 WITA ✓; `info` memperingatkan "Jam komputer UTC+0, toko WITA (UTC+8) … jadwal OpenClaw pakai --tz Asia/Makassar" ✓; zona luar Indonesia/`UTC+7` ditolak dengan pilihan jelas. Batas tengah malam dicek lewat kode (`sekarang()` memakai zona toko), tidak dengan jam palsu. |
| Emoji | Emoji dibuang dari struk; nama panjang dibungkus; render `scrollWidth = clientWidth` (tidak terpotong) — `struk-58mm-emoji-v110.png` ✓ |
| `struk --teks` | Tidak lagi menaikkan hitungan cetak: HTML pertama tanpa "SALINAN", kedua "SALINAN" ✓ |
| Pesan setelah tutup kasir | Nota **setelah** jam tutup (22:30) → "Kasir sudah DITUTUP pukul … buka sesi baru" ✓. Nota susulan **di dalam** jam sesi yang sudah ditutup (21:30, sesi 08:00–22:00) masih "Kasir belum dibuka…" ✗ (ringan) |
| CSV formula injection | **REGRESI:** lihat cacat B1 |

## 5. Cacat v1.1.0

### BERAT
**B1. Perlindungan formula injection CSV bocor untuk teks berawalan `-angka` (regresi keamanan).** `sel_aman()` baris 613 mengecualikan semua teks yang diawali `-` + digit. Produk bernama `-1+1+cmd|' /C calc'!A0` (payload DDE klasik) dan `-5 Diskon Palsu` diekspor **tanpa** tanda `'` (bukti: `/tmp/uji-kasir-lokal/r/inj4.csv`: `…;INJ;-1+1+cmd|' /C calc'!A0;…`). Excel mengevaluasi sel berawalan `-` sebagai rumus (mis. `-1+HYPERLINK("http://…")`). v1.0.0 menandai semua `-`. Klaim SKILL.md "CSV hasil ekspor aman dari formula injection" menjadi tidak benar. Nama produk bisa berasal dari CSV pemasok yang diimpor. **Perbaikan (1 baris):** hapus pengecualian `(s[0] == "-" and not s[1].isdigit())` → cukup `s[0] in "=+-@\t\r"`, karena baris 611 sudah meloloskan angka murni (`-2,5`, `-9975`). Tambah tes regresi untuk `-1+1+cmd|…` dan `-5 abc`.

### SEDANG
Tidak ada.

### RINGAN
1. Rekap bulanan toko PBJT juga mencetak disclaimer PPN ("UU HPP & PMK 131/2024 (PPN 12% …)") — membingungkan untuk kafe yang tidak memungut PPN; pisahkan disclaimer PPh final dari PPN.
2. `init --pajak tanpa --tarif-pbjt 10` diterima diam-diam (tarif diabaikan); beri peringatan.
3. Pesan tarif 0/negatif berbunyi "…membatasi paling tinggi 10%" — kurang tepat; tulis "harus lebih dari 0 dan paling tinggi 10%".
4. Nota susulan di dalam jam sesi yang sudah ditutup masih memberi pesan "Kasir belum dibuka" (lihat tabel 4).
5. `2 gula pasir` bila ada produk per kg dan per karung dengan nama sama → otomatis memilih produk tanpa varian (per kg) tanpa catatan "dibaca sebagai"; tambahkan catatan agar pengguna sadar.
6. Perubahan "Per jam tanpa nota void" belum tercatat di changelog/README.
7. Saran (bukan cacat): catatan di `references/pajak.md` bahwa Pasal 57 memakai "jumlah yang dibayarkan konsumen", sehingga service charge yang dibayar konsumen lazim ikut dasar — tetap ikuti Perda.

## 6. Skor v1.1.0
| Kriteria | Skor |
|---|:-:|
| Pemicu | 9 |
| Kemudahan awam | 9 |
| Kualitas output | 9 |
| Akurasi (angka/fakta) | 10 |
| Penanganan input kurang | 9 |
| Penanganan di luar cakupan | 9 |
| Keamanan | **5** (regresi formula injection B1) |

## SKOR AKHIR v1.1.0: **6 / 10 — REVISI**
Mode PBJT benar: 900 nota + ±560 retur/void + 60 rekap, 0 beda. Mode ini juga sesuai UU 1/2022 Pasal 57–59, dan pembulatan serta disclaimernya jujur. Perbaikan satuan, larangan manipulasi, zona waktu, dan cacat ringan v1.0.0 terbukti. Regresi skenario 01–03 bersih, kecuali perubahan rata-rata dan per jam yang disengaja. Namun B1 adalah regresi keamanan pada perlindungan yang diklaim di SKILL.md, sehingga menurut aturan quality gate skor dibatasi ≤ 6. Perbaikannya satu baris + tes. Setelah B1 diperbaiki dan dicek ulang (cukup tes CSV injection + `tests/uji_regresi.py`), perkiraan skor **9/10 — LULUS**.

## Catatan koordinator — v1.1.1
B1 (regresi formula injection) diperbaiki koordinator: `sel_aman()` kembali mengamankan SEMUA teks diawali `= + - @ tab CR`; angka murni (mis. `-2,5`) tetap lolos sebagai angka lewat pengecekan regex sebelumnya. Tes regresi ditambah untuk `-1+1+cmd|' /C calc'!A0`, `-5 Diskon Palsu`, `-2,5`, `-2.5`; 64/64 tes lulus. Cacat ringan dari uji ulang v1.1.0 dicatat untuk versi berikutnya. Menunggu cek ulang singkat penguji.

---

# Cek ulang v1.1.1 — 2026-09-24 (perbaikan B1)

Penguji: agent penguji independen (simulasi, Claude Code). Kode `VERSI = "1.1.1"`; `sel_aman()` baris 613 kini `s[0] in "=+-@\t\r"`, angka murni tetap diloloskan regex baris 611. `tests/uji_regresi.py` → OK.

| Uji | Hasil |
|---|---|
| Bukti injeksi B1 diulang (DB `/tmp/uji-kasir-lokal/r`, ekspor penjualan `inj5.csv` & buku-stok `inj5-bs.csv`) | `'-1+1+cmd\|' /C calc'!A0`, `'-5 Diskon Palsu`, `'-2+3 Kopi`, `'=HYPERLINK(…)`, `'@SUM(1+1)`, `'+62 Kopi` — **semua diberi tanda `'`** di kedua format ✓ |
| Angka minus tetap angka (ekspor penjualan skenario 03, pemisah `;`) | Qty `-2,5`, `-3`, `-1`; Diskon `-525`; Total `-9975`, `-38750` — tanpa `'` ✓. Pemisah `,`: `-2.5` tanpa `'` ✓ |
| Ekspor penjualan skenario 03 vs v1.1.0 | identik (`diff` kosong); rekap-penjualan-csv total_omzet 160.525 ✓ |
| Ekspor buku-stok skenario 03 vs v1.0.0/v1.1.0 | **identik byte-per-byte** ✓ |

B1 **tertutup**. Tidak ada regresi pada perbaikan CSV angka minus v1.1.0. Cacat ringan v1.1.0 (butir 1–6) masih terbuka; tidak menghalangi rilis.

## SKOR AKHIR v1.1.1: **9 / 10 — LULUS**
Alasannya:
- **Akurasi:** PPN dan PBJT terverifikasi independen (0 beda pada ribuan nota, retur, dan rekap).
- **Kesesuaian aturan:** mengikuti UU 1/2022 Pasal 57–59 dan PMK 131/2024, dengan disclaimer yang jujur.
- **Keamanan:** kembali utuh.
- **Keunggulan:** jauh lebih baik daripada agent tanpa skill, dan tidak ada pesaing skill yang sebanding.

Nilai tidak 10 karena masih ada cacat ringan dan pengiriman Telegram belum diuji dengan bot asli.
