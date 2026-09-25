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
