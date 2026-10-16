# HASIL UJI — tender-checklist v1.0.0 (uji independen Tahap 6)

- Tanggal: 2026-09-25 · Penguji: agent terpisah dari pembuat (claude-code, simulasi agent) · Salinan uji: scratchpad `uji-tender/`
- Tes bawaan `tests/uji_regresi.py`: **23/23 OK**. `uji_openclaw.sh`: 68/68 eligible/visible (termasuk skill ini). `validate.py`: 1 masalah **di luar skill ini** (`analisis-excel` belum di catalog).

## Ringkasan skenario
| # | Skenario | Hasil |
|---|---|---|
| 01 | CV kecil PKP, ATK HPS Rp185 jt, 12 baris, PPN 11/12 | ✅ Angka benar semua (diverifikasi Decimal), jadwal benar, catatan ambang PL Rp200 jt |
| 02 | Konstruksi HPS Rp2,4 M, jadwal + SBU/SKK, libur 20/10 | ✅ Tanggal benar; SKP 5−3=2; ⚠ label "TERLEWAT - kerjakan segera" untuk acara pengumuman/penjelasan |
| 03 | 76% HPS + satu baris salah hitung | ⚠ Total & peringatan <80% benar, **tetapi script tidak menunjuk baris salah** (kolom Jumlah diabaikan) dan salah membaca baris TOTAL di kolom lain |
| 04 | "Mau ikut tender pemerintah gimana?" | ✅ Tanya sekali, 5 pertanyaan, peta jalur |
| 05 | Arisan tender, pinjam bendera, pengalaman fiktif | ✅ Ditolak sopan, UU 5/1999 Ps. 22 & Tipikor, jalur sah (KSO/subkon/SBU) |
| A/B | 00-pembanding-tanpa-skill.md | ✅ Dengan skill jelas lebih baik (16 vs 2) — catatan: baseline disimulasikan penguji |
| Pesaing | 00-banding-pesaing.md | ✅ Unggul vs rfp-responder (10 vs 3); tidak ada skill tender RI publik |

## Verifikasi angka independen (Decimal/manual, tanpa membaca kode)
Semua cocok: skenario 01 (subtotal 163.545.400; PPN 17.989.994; total 181.535.394; 98,13%), 03 (368.775.000; 40.565.250; 409.340.250; 76,09%; 80% = 430.400.000), volume "1,5" & "2,25", harga "Rp1.250.000,00" & "Rp 12.345,67", pembulatan setengah ke atas, sel kosong/negatif ditolak per baris, CSV `;` dan `,` (bertanda kutip), mode termasuk PPN non-mewah & mewah (DPP terbesar dengan DPP+PPN ≤ harga — diuji brute-force, termasuk kasus sisa Rp1), total > HPS (selisih −Rp1 → gugur), HPS 0/negatif ditolak. Terbilang cocok. Jadwal: 6 kasus (libur, batas di Minggu/libur, Sabtu kerja, batas lewat, penjelasan setelah batas) cocok dengan hitungan kalender manual.

## Bug / temuan (berprioritas)
1. **[TINGGI] Baris "Total" tanpa PPN dilaporkan "cocok".** `scripts/cek_penawaran.py` `hitung()` (blok `for label, nilai in total_tertempel`, ±baris 330–338) menerima kecocokan dengan subtotal/DPP/PPN/total apa pun. CSV PKP dengan `Total;;;5.000.000` (lupa PPN; seharusnya 5.550.000) → "Info: Baris 'Total' ... cocok". Ini persis kesalahan gugur #16. **Perbaikan:** cocokkan label ke nilai yang sesuai (total/grand total → total; jumlah/subtotal → subtotal/DPP; PPN → PPN); jika label "Total" = subtotal padahal PPN > 0 → PERINGATAN "total di file belum termasuk PPN".
2. **[TINGGI] Kolom "Jumlah" pengguna diabaikan** → baris yang salah hitung tidak ditunjuk (skenario 03). `KUNCI_KOLOM` (±baris 155–162) tidak punya kunci `jumlah`/`jumlah harga`/`total harga`. **Perbaikan:** petakan kolom jumlah; per baris bandingkan dengan volume × harga, tampilkan "baris 3: file Rp47.375.000 ≠ hitung Rp74.375.000 (selisih Rp27.000.000)". Tambah tes regresi. Sesuaikan klaim SKILL.md langkah 5.
3. **[SEDANG] Baris total yang labelnya di kolom selain Uraian/No** (mis. `;;;;TOTAL;Rp341.775.000`, layout Excel umum dengan sel gabung) → "uraian kosong" + **TOTAL BELUM FINAL** palsu. Lokasi: kondisi `POLA_TOTAL.match(uraian) or (not uraian and POLA_TOTAL.match(no))` (±baris 272). **Perbaikan:** bila uraian kosong, cek semua sel teks terhadap `POLA_TOTAL`.
4. **[SEDANG] HPS dalam miliar tidak terbaca**: `"2,4 M"`, `"Rp2,4 miliar"`, `"2.4M"` → GALAT, padahal `"185jt"` bisa. Lokasi `parse_angka()` daftar akhiran (±baris 58). **Perbaikan:** tambah `miliar/milyar/m` (hati-hati "m" = meter pada volume → hanya untuk argumen HPS/pagu).
5. **[RENDAH] Peringatan <80% selalu menyebut jaminan pelaksanaan 5% HPS**, juga untuk paket kecil. Jaminan pelaksanaan hanya untuk kontrak barang/konstruksi/jasa lainnya **> Rp200 jt** (Perpres 16/2018 jo. 12/2021 Ps. 33). Tambah syarat itu; SKILL.md/referensi juga sebaiknya menyebut jaminan pelaksanaan 5% nilai kontrak (80–100% HPS) untuk perencanaan kas.
6. **[RENDAH] Jadwal:** acara Pengumuman/Penjelasan yang sudah lewat berlabel "TERLEWAT - kerjakan segera" (tidak bisa dikerjakan ulang) → ganti "SUDAH LEWAT – baca BA penjelasan/adendum" (`jadwal()`, ±baris 518).
7. **[RENDAH] Pesan selisih baris PPN** tidak menampilkan PPN hitungan script; label kosong `''` di "Baris dilewati" bila label ada di kolom No. Exit code 0 walau TOTAL BELUM FINAL (pertimbangkan exit 2).
8. **[RENDAH, isi] Konstruksi:** tidak ada pengingat PPh final jasa konstruksi (PP 9/2022) — cukup satu kalimat + arahkan ke konsultan pajak (sudah ditandai di luar cakupan di referensi, belum di SKILL.md langkah 5).

## Pemeriksaan aturan (web search 2026-09-25; situs JDIH LKPP/BPK/pasal.id terblokir egress → hanya cuplikan)
| Klaim skill | Hasil |
|---|---|
| PL barang/jasa lainnya ≤ Rp200 jt, konstruksi ≤ Rp400 jt (Ps. 38 Perpres 46/2025) | ✅ Cuplikan RRI, Radar Bojonegoro, konsolidasi LKPP |
| PL konsultansi ≤ Rp100 jt | ✅ (cuplikan; di Perpres pasalnya terpisah dari Ps. 38 — Ps. 41) |
| Pagu ≤ Rp15 M untuk UMK & koperasi, kecuali kemampuan teknis (Ps. 65) | ✅ cuplikan teks pasal |
| PDN: TKDN+BMP ≥40% → TKDN >25% (Ps. 66) | ✅ substansi (Antara, Core Business); rumusan "≥/paling sedikit" vs "lebih dari" belum dicek naskah → PERLU REVIEW (sudah ditandai) |
| Jaminan penawaran HPS > Rp10 M, 1–3% HPS; terintegrasi 1–3% pagu | ✅ PKMS LKPP & bankgaransi.id; ⚠ referensi menulis "Perpres 12/2021 **Pasal 30**" — sumber menunjuk **Pasal 31** → koreksi di `references/dasar-aturan.md` |
| <80% HPS → klarifikasi kewajaran; wajar → jaminan pelaksanaan 5% HPS; tidak wajar → gugur | ✅ (Buleleng, KLC Kemenkeu, konsolidasi Ps. 33); tambah syarat kontrak > Rp200 jt |
| Peraturan LKPP 12/2021 jo. 4/2024 | ✅ Perlem 4/2024 ditetapkan 14 Okt 2024 (ubah Lampiran III & VI, rancang-bangun) |
| Peraturan LKPP 2/2026 Katalog Elektronik (pembelian langsung, negosiasi, mini-kompetisi) | ✅ ada di JDIH LKPP/peraturan.go.id; tanggal berlaku 1 Sep 2026 hanya dari berita → PERLU REVIEW (sudah ditandai) |
| PMK 131/2024: 12% × DPP 11/12 untuk non-mewah, berlaku 1 Jan 2025 | ✅ pajak.go.id, Ortax |
| UU 5/1999 Ps. 22 larangan persekongkolan tender | ✅ |
| Tidak bisa diverifikasi (tetap bertanda PERLU REVIEW): pengecualian pengalaman usaha kecil < 3 th untuk paket ≤ Rp2,5 M; SKP KP=5; SPSE 4.5; kriteria usaha kecil PP 7/2021 | ⚠ |
Disclaimer (bukan nasihat hukum, dokumen pemilihan mengikat, pembulatan belum dicocokkan Coretax) ✅ ada di SKILL.md, README, output script.

## Skor: **6 / 10 — REVISI sebelum `lulus`**
Alasan: inti perhitungan (PPN 11/12 bulat ke bawah, mode termasuk PPN, %HPS, 80%, terbilang, jadwal hari kerja) **100% benar** pada semua uji; A/B jelas unggul; unggul telak atas pesaing; etika & disclaimer baik. Namun fungsi utama "pemeriksa rincian" gagal pada dua pola kesalahan Excel yang paling sering (bug 1: **konfirmasi palsu** "cocok" untuk total tanpa PPN; bug 2: baris salah hitung tidak ditunjuk) dan bug 3 memberi alarm palsu pada layout umum. Ini melanggar prinsip *reliable* untuk skill ecer. Perbaiki bug 1–4 (+ tes regresi), koreksi Pasal 31, lalu uji ulang independen — perkiraan skor setelah revisi 8–9.

---

# Uji ulang v1.0.1 (penguji independen baru, 2026-09-25)

Rincian lengkap: `06-uji-ulang-v1.0.1.md`. Tes bawaan **38/38 OK**; `validate.py` lolos; SKILL.md 100 baris.

- **Bug 1–4 beres** (diulang dari skenario 01–03): total tanpa PPN kini PERINGATAN "BELUM TERMASUK PPN" + total yang benar; baris salah hitung ditunjuk dengan selisihnya; TOTAL di kolom lain dikenali (tak ada lagi BELUM FINAL palsu); HPS "2,4 M"/"Rp2,4 miliar"/"2.4M"/"2.400.000.000" terbaca. Temuan 5–8 dan koreksi Pasal 31 juga beres.
- **13 CSV baru buatan penguji** (pemisah `;`/`,`/TAB, "Rp 1.250.000,-", volume desimal, pembulatan per baris, label di kolom lain, mode termasuk PPN, mewah, tanpa judul kolom, harga tak terbaca): **semua angka cocok dengan kunci Decimal independen**; tidak ada "cocok" palsu untuk total salah basis; salah hitung yang ada di kolom yang dikenali selalu ditunjuk.
- **Temuan baru:** (1) [SEDANG] alarm palsu untuk "Total Harga Sebelum PPN" (dianggap total sesudah PPN); (2) [SEDANG] "DPP Nilai Lain (11/12)" dibandingkan dengan DPP → alarm palsu; (3) [SEDANG] layout `Jumlah` (banyaknya) + `Jumlah Harga`: kolom Jumlah Harga diabaikan → baris salah hitung tidak ditunjuk (total yang salah tetap ketahuan); (4–6) [RENDAH] label "Harga Total" dilewati diam-diam, "cocok" terhadap total sementara saat BELUM FINAL, exit 0 walau ada PERINGATAN.
- **Aturan (web search):** Pasal 31 jaminan penawaran, Pasal 33 jaminan pelaksanaan (> Rp200 jt; 5% kontrak / 5% HPS bila < 80%), klarifikasi < 80% HPS, PPh final konstruksi PP 9/2022 — ✅ semua.

## Skor uji ulang: **8 / 10 — LULUS** (layak naik ke `lulus`; perbaiki temuan 1–3 di v1.0.2 sebelum `rilis`)
Alasan: keempat bug penyebab skor 6 sudah tertutup dan dilindungi tes regresi; perhitungan 100% benar di 16 kasus (3 lama + 13 baru); tidak ada konfirmasi palsu, jadi tidak ada risiko pengguna mengunggah angka salah karena "cocok". Belum 9 karena masih ada dua alarm palsu pada layout Excel PKP yang umum sejak 2025 (label "sebelum PPN" dan baris DPP nilai lain) yang bisa membingungkan pengguna awam, serta satu layout tabel barang yang umum di mana baris salah hitung tidak ditunjuk.

---

# Uji ulang v1.0.2 (penguji independen ketiga, 2026-09-25)

Salinan uji: scratchpad `uji3-tender/` (CSV uji + `kunci.py` Decimal independen di sana, tidak disalin ke repo). Tes bawaan `tests/uji_regresi.py`: **46/46 OK**.

## Temuan v1.0.1 → status
| # | Temuan | Status v1.0.2 |
|---|---|---|
| 1 | "Total Harga Sebelum PPN" dianggap total sesudah PPN | ✅ Beres — dicocokkan ke sebelum PPN; "Total Harga Setelah PPN" ke sesudah PPN |
| 2 | "DPP Nilai Lain (11/12)" alarm palsu | ✅ Beres — dibanding 11/12 × DPP (juga "DPP NL (11/12)") |
| 3 | `Jumlah` + `Jumlah Harga`: baris salah tidak ditunjuk | ✅ Beres — Jumlah = volume, baris salah ditunjuk + Catatan |
| 4 | "Harga Total" dilewati diam-diam | ✅ Beres — Info "TIDAK diperiksa otomatis" + perbandingan nilai, exit 1 |
| 5 | "cocok" terhadap total sementara saat BELUM FINAL | ✅ Beres — "sama dengan ... SEMENTARA - belum bisa dinyatakan cocok" |
| 6 | Exit 0 walau PERINGATAN | ✅ Beres — 0 bersih, 1 peringatan, 2 GALAT (file rusak/tidak ada), 3 BELUM FINAL. Catatan kecil: `--hps 0`/`-5` → exit 1 (peringatan), bukan 2 |

## CSV baru (kunci Decimal independen: baris dibulatkan setengah-ke-atas, PPN = 11% × DPP bulat ke bawah, mode termasuk PPN = DPP bulat terbesar dengan DPP+PPN ≤ harga)
| File | Isi | Kunci (DPP / PPN / Total) | Hasil script |
|---|---|---|---|
| n1 benar-bersih | `Qty`, `Harga Satuan (Rp)`, `Jumlah (Rp)`, vol 2,5; "Sub Total", "ppn 11%", "GRAND TOTAL" | 48.923.000 / 5.381.530 / 54.304.530; 90,51% | ✅ cocok semua, tanpa peringatan, exit 0 |
| n2 benar | pemisah `,` bertanda kutip, `Vol`, vol 7.5; "Total Excl. PPN", "DPP NL (11/12)", "PPN 12% x DPP NL", "Total Incl. PPN" | 17.157.500 / 1.887.325 / 19.044.825; 90,69% | ✅ cocok semua, exit 0 |
| n3 benar | **`Banyaknya` + `Jumlah Harga`**, harga desimal (3.333,33; 27.777,50; 1.234,56), pembulatan per baris | 793.081 / 87.238 / 880.319; 88,03% | ❌ **BUG BARU** (lihat bawah): total Rp12.013.332.039. Dengan judul `Kuantitas` → ✅ cocok semua, exit 0 |
| n4 SALAH | 1 baris salah Rp100.000 + 1 baris salah Rp1, Sub Total/PPN/Grand Total salah, label "PPN 12% x DPP NL" | 30.230.999 / 3.325.409 / 33.556.408; 93,21% | ✅ kedua baris ditunjuk + selisih; Sub Total, PPN, Grand Total diberi PERINGATAN; exit 1 |
| n5 SALAH | "Total Excl. PPN" benar, "ToTaL" = sebelum PPN (lupa PPN) | 8.750.000 / 962.500 / 9.712.500 | ✅ "BELUM TERMASUK PPN" + total benar; Excl. PPN cocok; exit 1 |
| n6 benar-bersih | harga termasuk PPN, `Qty`, `Harga Satuan (Rp)` | harga 26.931.365 → DPP 24.262.491 / PPN 2.668.874 / sisa 0; 89,77% | ✅ cocok, exit 0 |
| n7 SALAH halus | `Banyaknya`; baris 7 × 2.142,50 ditulis 14.997 (Excel ROUND = 14.998); Jumlah −Rp1; PPN +Rp1 (dibulatkan ke atas) | 114.997 / 12.649 / 127.646 | ❌ bug baru yang sama. Dengan `Kuantitas`: Jumlah & PPN selisih Rp1 ditunjuk; baris 14.997 **tidak** ditunjuk (toleransi < Rp1 dari hasil kali persis — disengaja) |
Tidak ada alarm palsu pada file benar (n1, n2, n6, n3-Kuantitas); semua kesalahan pada n4/n5 tertunjuk; tidak ada regresi angka pada layout yang kolomnya dikenali. Skenario template (`contoh-rincian.csv`) tetap sama.

## Bug baru
1. **[TINGGI] Kolom uang dipakai sebagai VOLUME bila judul kolom banyaknya tidak dikenal.** `kenali_header()` + fallback di `baca_rincian` (`if "volume" not in peta and "jumlah" in peta: peta["volume"] = peta.pop("jumlah")`, ±baris 287). Judul **`Banyaknya`, `Jml`, `Qty.`, `Volume Pekerjaan`** tidak ada di sinonim `volume` (hanya `banyak`, `qty`, `vol.` ...), lalu kolom **`Jumlah Harga`/`Jumlah Harga (Rp.)`** diubah menjadi volume → volume 4.500.000 × Rp450.000 = **Rp2.025.000.000.000**. Tanpa baris total di file dan tanpa HPS, output hanya berisi Catatan kecil (tanpa PERINGATAN baris). **Perbaikan:** (a) tambah sinonim `banyaknya`, `jml`, `jml.`, `qty.`, `kuantitas`, `volume pekerjaan`, `jumlah satuan`; normalisasi titik di akhir judul; (b) fallback Jumlah→volume hanya untuk judul `jumlah`/`jml` polos, **jangan** untuk judul berisi harga/total/nilai/rp — jika begitu, GALAT exit 2 "kolom volume tidak ditemukan"; (c) tes regresi untuk tiap judul di atas.
2. **[RENDAH]** Selisih baris < Rp1 terhadap hasil kali persis (mis. 7 × 2.142,50 = 14.997,5 ditulis 14.997) tidak ditunjuk, padahal ikut membuat baris Jumlah file selisih Rp1 → pengguna melihat subtotal beda Rp1 tanpa tahu barisnya. Pertimbangkan Info "baris X: pembulatan berbeda (Rp1)" saat subtotal file ≠ hitung.
3. **[RENDAH]** `--hps 0`/negatif → exit 1 (peringatan) padahal SKILL.md menyebut 2 = input buruk; samakan.

## Skor uji ulang v1.0.2: **7 / 10 — tetap `lulus`, JANGAN `rilis` sebelum bug baru 1 diperbaiki (v1.0.3 + uji ulang singkat)**
Alasan: keenam temuan v1.0.1 beres dan dilindungi 46 tes; mesin hitung 100% cocok dengan kunci Decimal pada semua layout yang kolomnya dikenali (n1, n2, n4–n6, n3/n7 versi Kuantitas), tanpa alarm palsu dan tanpa konfirmasi palsu. Turun dari 8 karena ditemukan jalur kegagalan baru yang parah pada judul kolom yang sangat umum di tabel barang Indonesia (`Banyaknya`/`Jml` + `Jumlah Harga`): angka hasil salah kali lipat jutaan dan bisa tercetak hanya dengan catatan kecil — melanggar prinsip *reliable*. Perbaikannya kecil dan lokal (sinonim + pembatasan fallback); setelah itu perkiraan skor 9.

---

# Uji ulang v1.0.3 (penguji independen keempat, 2026-09-25)

Salinan uji: scratchpad `uji4-tender/` (script) + `uji4-csv/` (12 CSV baru, kunci Decimal dihitung terpisah di terminal, tidak disalin ke repo). Tes bawaan `tests/uji_regresi.py`: **49/49 OK**.

## 12 CSV baru — judul kolom banyaknya bervariasi (fokus bug baru v1.0.2)
| File | Judul banyaknya | Pemisah | Hasil |
|---|---|---|---|
| c1 | Banyaknya | `,` | ✅ subtotal 1.137.500 cocok kunci |
| c2 | Jml (+ "Total Harga (Rp)") | `,` | ✅ subtotal 12.435.000 cocok |
| c3 | Jml. (+ "Nilai (Rp)") | `,` | ✅ subtotal 3.130.000 cocok |
| c4 | Qty. | `;` | ✅ subtotal 15.200.000 cocok |
| c5 | QTY | `,` | ✅ subtotal 37.100.000 cocok |
| c6 | Kuantitas | `;` | ✅ subtotal 17.360.000 cocok |
| c7 | Vol | `,` | ✅ subtotal 10.086.000 cocok |
| c8 | Volume Pekerjaan (vol desimal 45,5) | `,` | ✅ subtotal 109.675.000 cocok |
| c9 | "Jumlah" polos, **tanpa** kolom Jumlah Harga | `,` | ✅ dibaca sebagai volume (fallback lama), subtotal 7.350.000 cocok |
| c10 | Banyaknya (3 baris) | `;` | ✅ subtotal 28.060.000 cocok |
| c11 | **tanpa kolom volume sama sekali** (hanya Jumlah Harga) | `,` | ✅ GALAT exit 2: "kolom volume/banyaknya tidak dikenali (kolom 'Jumlah Harga' berisi rupiah, bukan volume)" — tidak ada hasil salah tercetak |
| c12 | Jml (2 baris sengaja salah hitung) | `,` | ✅ kedua baris ditunjuk + selisih benar (2.125.000/2.137.500 dan 1.625.000/1.622.500), exit 1 |

Tidak ada satu pun subtotal yang memakai kolom rupiah sebagai volume (dulu bug v1.0.2 menghasilkan triliunan pada pola ini). Semua nilai `item.volume`/`item.harga_satuan`/`item.jumlah` di keluaran `--json` diverifikasi cocok dengan kunci Decimal independen (perkalian manual per baris + `ROUND_HALF_UP`).

## Kode keluar HPS
- `--hps 0` → **GALAT, exit 2** ✅ (sebelumnya v1.0.2: exit 1)
- `--hps -5` → **GALAT, exit 2** ✅ (sebelumnya v1.0.2: exit 1)

Kedua-duanya kini konsisten dengan SKILL.md (2 = input buruk) dan dengan c11 (kolom tak dikenali → GALAT exit 2), bukan lagi peringatan.

## Bug baru
Tidak ditemukan. Temuan v1.0.2 (bug baru #1 [TINGGI], #3 [RENDAH]) tertutup penuh. Temuan #2 v1.0.2 [RENDAH, selisih <Rp1 tak ditunjuk] belum diperbaiki (di luar cakupan perbaikan v1.0.3, tetap tercatat di riwayat v1.0.2 di atas untuk dipertimbangkan pemilik).

## Skor uji ulang v1.0.3: **9 / 10 — LULUS, layak `rilis`**
Alasan: bug TINGGI (kolom rupiah dipakai sebagai volume) tuntas pada seluruh variasi judul kolom banyaknya yang lazim di tabel barang Indonesia (Banyaknya/Jml/Jml./Qty./QTY/Kuantitas/Vol/Volume Pekerjaan), termasuk kasus tanpa kolom volume sama sekali (kini berhenti dengan pesan jelas, bukan angka salah) dan kasus "Jumlah" polos tanpa Jumlah Harga (tetap dibaca sebagai volume seperti sebelumnya, benar). `--hps 0/-5` kini konsisten exit 2. 49/49 tes regresi lulus. Tidak 10 karena temuan minor v1.0.2 (#2, selisih pembulatan <Rp1 tak ditunjuk per baris) masih terbuka — dampaknya kecil (selisih Rp1) dan tidak melanggar prinsip reliable secara material.

---

## Uji ulang v1.0.4 (sesuai naskah resmi Perpres 46/2025)

- **Penguji:** agent independen (bukan pembuat, perevisi, atau penguji sebelumnya); salinan di scratchpad `uji-resmi/tender-checklist/`. Tanggal: **26 September 2026**.
- **Pencocokan naskah** (konsolidasi LKPP https://jdih.lkpp.go.id/regulation/download/konsolidasi-nomor-46-tahun-2025/1, HTTP 200 PDF, teks diekstrak dengan Python standar):
  - Pasal 30 ayat (2) (*) ✅ "Jaminan penawaran … untuk pengadaan Pekerjaan Konstruksi dan pekerjaan terintegrasi"; ayat (2a) jaminan sanggah banding; Pasal 31 ✅ HPS paling sedikit di atas Rp10 M, 1%–3% HPS, terintegrasi 1%–3% pagu.
  - Pasal 33 ayat (2) ✅ huruf a (jasa lainnya, aset penyedia dikuasai pengguna) tetap; **huruf b "Dihapus" (\*\*\*)** → pengecualian e-purchasing hilang. Ayat (1) > Rp200 jt, ayat (3) 5% kontrak / 5% HPS, ayat (4) terintegrasi acuan pagu, ayat (5) masa berlaku ✅.
  - Pasal 66 ✅ "TKDN paling sedikit 25%" bila ada PDN TKDN+BMP paling sedikit 40% (≥ 25%, bukan > 25%).
  - Pasal 65 ✅ ayat (3) pagu s.d. Rp15 M untuk UMK & koperasi; ayat (4) pengecualian kemampuan teknis.
- **Pesan jaminan per `--jenis`** (CSV sendiri: `t2` 2 baris laptop/printer, total Rp2.601.307.200, HPS Rp11 M dan Rp3 M; `t1` 4 baris konstruksi, total Rp5.590.345.725, HPS Rp12 M dan Rp6,5 M; PPN non-mewah; plus `--pagu 14M`):
  - konstruksi → "WAJIB JAMINAN PENAWARAN 1%-3% dari HPS = Rp110.000.000 s.d. Rp330.000.000" ✅
  - terintegrasi → wajib, "dari pagu anggaran" ✅ (lihat bug 1)
  - barang / jasa-lainnya / konsultansi → "umumnya TIDAK diperlukan … sejak Perpres 46/2025" ✅
  - tanpa `--jenis` → "ASUMSI: jenis tidak disebut (tambahkan --jenis) … hanya wajib bila KONSTRUKSI atau TERINTEGRASI" ✅ (v1.0.3 lama: "barang/konstruksi/jasa lainnya umumnya mensyaratkan" — salah, kini benar)
  - Jaminan pelaksanaan kontrak > Rp200 jt: barang/konstruksi/jasa-lainnya/terintegrasi → 5% kontrak "berlaku juga untuk e-purchasing" ✅; tanpa jenis → + asumsi "bukan konsultansi" ✅; konsultansi → "tidak diatur Pasal 33, ikuti dokumen pemilihan" ✅; < 80% HPS → 5% HPS + Pasal 33 ayat (3) huruf b ✅.
  - Cadangan UMK Pasal 65 ayat (3)/(4) muncul untuk tanpa jenis/barang/konstruksi/jasa-lainnya, tidak untuk konsultansi/terintegrasi ✅.
- **Angka tidak berubah:** subtotal/DPP/PPN/total/%HPS identik antara script v1.0.4 dan versi sebelum commit `c608c3a` untuk keempat kombinasi; diverifikasi ulang dengan Decimal independen: t1 5.036.347.500 / 553.998.225 / 5.590.345.725 / 46,59% & 86,01% / batas 80% Rp9,6 M; t2 2.343.520.000 / 257.787.200 / 2.601.307.200 / 23,65% & 86,71% / Rp8,8 M; 5% kontrak Rp279.517.286 & Rp130.065.360; 5% HPS Rp600.000.000 & Rp550.000.000 ✅.
- **Konsistensi dokumen:** SKILL.md, README, checklist-dokumen, kesalahan-gugur, lembar-kerja-tender tidak lagi menyebut jaminan penawaran untuk barang/jasa lainnya maupun pengecualian e-purchasing ✅.
- **Tes bawaan:** `python3 tests/uji_regresi.py` → **53 tes OK**.
- **Bug baru:**
  1. [RENDAH] `--jenis terintegrasi` + `--pagu` diisi: rentang 1%–3% jaminan penawaran dan 5% jaminan pelaksanaan (< 80%) tetap dihitung dari **HPS**, bukan pagu (Pasal 31 ayat (3), Pasal 33 ayat (4)); ambang 80% juga masih terhadap HPS. Sudah diberi keterangan "acuan pagu", tetapi bila pagu tersedia sebaiknya dihitung dari pagu. Kalimatnya juga janggal ("di atas dihitung dari HPS" padahal angkanya muncul sesudahnya).
  2. [KOSMETIK] Teks memakai slug "pengadaan jasa-lainnya" (tanda hubung).

### Skor uji ulang v1.0.4: **9/10**
Alasan: keempat koreksi hukum cocok dengan naskah konsolidasi resmi; pesan jaminan benar untuk keenam varian jenis; angka hitungan tidak berubah dan cocok dengan Decimal independen; 53 tes lulus. Belum 10 karena bug rendah #1 (terintegrasi memakai HPS walau pagu ada). **Rekomendasi: LULUS.**

## Uji ulang v1.0.5 (penguji independen, cek singkat, 26 Sep 2026)
Disalin ke scratchpad `uji-kecil/`, dijalankan dari sana. Tes bawaan: **60/60 lulus**.

**Verifikasi naskah resmi** (naskah konsolidasi LKPP Perpres 16/2018 jo. 12/2021 jo. 46/2025, PDF jdih.lkpp.go.id, salinan teks di scratchpad):
- Pasal 31 ayat (3): "Pengadaan Barang/Jasa yang dilakukan secara terintegrasi, Jaminan Penawaran … 1% hingga 3% dari nilai **Pagu Anggaran**" → perubahan **didukung**.
- Pasal 33 ayat (4): terintegrasi — penawaran 80%–100% **Pagu Anggaran** → 5% nilai Kontrak; di bawah 80% Pagu Anggaran → 5% nilai **Pagu Anggaran** → perubahan **didukung**. Ambang HPS > Rp10 M (Ps. 31 ayat (1)) tetap dari HPS — script benar.
- Tidak ada TEMUAN TINGGI.

**Skenario (terintegrasi, penawaran Rp12 M):** HPS 15 M + pagu 16 M → penawaran 160–480 jt (1–3% pagu), < 80% pagu (12,8 M) → jaminan pelaksanaan Rp800 jt (5% pagu) ✓. Tepat 80% pagu (12,8 M) → 5% kontrak Rp640 jt ✓ (batas inklusif sesuai "antara 80% sampai dengan 100%"). Tanpa `--pagu` → dari HPS "sebagai gambaran" ✓. Subtotal/total/%HPS (80,00%)/batas 80% HPS tidak berubah ✓. `jasa lainnya` tanpa tanda hubung ✓. `--pagu 0` / `-5` → GALAT kode 2: **wajar** (pagu 0 tidak bermakna dan akan membuat ambang 80% = 0).

**Bug baru (RENDAH):**
1. Pagu < HPS atau total > pagu (mis. HPS 15 M, pagu 10 M, total 12 M): selain "melebihi pagu", muncul "5% dari nilai kontrak … (penawaran 80%-100% pagu anggaran)" padahal 120% pagu — teks keliru, angka tidak dipakai (penawaran di atas pagu tidak bisa menang). Sarankan pesan jaminan pelaksanaan dilewati bila total > pagu, dan peringatan bila pagu < HPS.

### Skor uji ulang v1.0.5: **9/10** — perubahan sesuai naskah resmi; satu temuan teks rendah.

## Uji bot Telegram asli v1.0.8 (16 Okt 2026) → revisi v1.0.9 (catatan pembuat revisi, belum diuji ulang)
- Hasil bot: tanpa skill 5 → dengan skill **7,5** (BELUM; ambang 8). Angka benar semua (DPP Rp39.768.000, PPN Rp4.374.480, total Rp44.142.480, 23,86% HPS), tetapi checklist dokumen yang ditanyakan tidak muncul (batas unggah sudah lewat), tanpa dasar aturan/penafian, tanpa pengingat PPN/PPh 22 bendahara, kalimat jaminan penawaran/pelaksanaan tergabung, dan ada kata proses "hitungan script".
- Perbaikan v1.0.9: urutan jawaban tetap + daftar cek sebelum kirim (SKILL.md Format Output), checklist dokumen wajib walau tenggat lewat + checklist minimal di SKILL.md, baris Dasar aturan baku, jaminan penawaran vs pelaksanaan dua butir terpisah, bagian "Pengingat" baru di hasil hitung (jaminan penawaran & potongan bendahara; tampilan saja), kata "script" dihapus dari teks hasil hitung/jadwal/rujukan.
- Angka & kode keluar identik dengan v1.0.8 pada 98 kombinasi (14 CSV × 7 pilihan, `--json`). Tes bawaan: **66/66 OK**. Perlu uji ulang di bot Telegram (pra-cek konteks Telegram) sebelum dinyatakan lulus.
