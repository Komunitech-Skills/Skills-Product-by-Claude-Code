# Analisis Excel Tanpa Rumus, Tinggal Tanya

**Kirim file Excel/CSV, tanya pakai bahasa biasa, dapat tabel + temuan + saran grafik — angkanya
dihitung komputer, bukan dikira-kira AI.**

## Manfaat
- ✅ **Jawaban langsung dari file Anda:** "total per kategori", "bulan mana paling tinggi",
  "September naik berapa dibanding Agustus", "10 pelanggan terbesar" — tanpa bikin PivotTable
  atau rumus SUMIFS sendiri.
- ✅ **Angka bisa dipercaya:** semua dihitung script (presisi penuh untuk rupiah), baris "TOTAL"
  di bawah tabel otomatis tidak dihitung dua kali, nilai yang aneh dilaporkan lengkap dengan nomor
  barisnya — bukan ditebak diam-diam.
- ✅ **Tahan file berantakan:** judul laporan di atas tabel, sel gabungan (merge), angka
  "Rp 1.234.567,89", tanggal campur "25/09/2026" / "25 Sep 2026" / "2026-09-25", "kopi susu" vs
  "Kopi Susu ", file CSV dari Excel Windows lama — semua ditangani.
- ✅ **Siap pakai:** tabel siap tempel ke WA/laporan, file CSV hasil yang bisa dibuka di Excel,
  narasi temuan bahasa awam, dan saran grafik yang cocok.
- ✅ **Merapikan data:** satu perintah menghasilkan salinan data yang bersih (file asli tidak
  diubah).

## Cocok untuk siapa
- Pemilik usaha & admin kantor yang punya data di Excel (biaya operasional, stok, pelanggan,
  piutang, absensi) tapi tidak sempat/tidak bisa bikin PivotTable
- Profesional (HR, keuangan, guru, pengurus koperasi/yayasan) yang butuh ringkasan cepat untuk
  rapat atau laporan ke atasan
- Siapa pun yang sering ditanya "totalnya berapa?" dan harus menghitung manual

## Contoh sebelum & sesudah
**Sebelum (AI tanpa skill):** AI membaca sebagian isi file lalu *mengira-ngira* total; baris
"TOTAL" di bawah tabel ikut terjumlah (hasilnya jadi dobel), "LISTRIK & AIR" dan "listrik & air"
dihitung sebagai dua kategori, dan sel yang isinya rumus kosong tidak disadari.

**Sesudah (dengan skill):** "Ini file biaya operasional, pengeluaran paling besar di mana dan
September naik berapa dari Agustus?"
```
| Kategori      | Baris | Jumlah Nominal | % dari total |
| Sewa          | 3     | Rp 13.500.000  | 48,9%        |
| Transport     | 5     | Rp 8.995.000   | 32,6%        |
| Listrik & Air | 3     | Rp 4.140.000   | 15,0%        |
...
Jumlah Nominal: naik 73,5% (Rp 7.555.000 → Rp 13.110.000).
Naik paling besar: Transport — naik 310,7% (Rp 1.595.000 → Rp 6.550.000).
⚠️ 1 sel berisi rumus tanpa nilai tersimpan (E16) sehingga dianggap kosong ...
⚠️ 1 baris Total/Jumlah dilewati agar tidak terhitung dua kali (baris 18: TOTAL | … ).
```
(Contoh lengkap: `examples/uji-pembuat-01-biaya-operasional-xlsx.md`.)

## Cara pakai
Kirim/sebutkan lokasi file ke AI agent Anda, lalu tanya seperti biasa:
- "Tolong analisis file Excel ini, ada yang aneh nggak?"
- "Total pengeluaran per divisi berapa? Simpan tabelnya jadi file."
- "Bandingkan omzet cabang bulan Agustus dan September."
- "Rapikan data ini supaya bisa dipakai di Excel."

Tips: skill ini **paling andal untuk tabel rapi** — **satu baris judul kolom** dan **satu baris per
kejadian/transaksi** (lihat `templates/contoh-tabel-rapi.csv`). File berantakan tetap dicoba, tetapi untuk
**laporan berformat** (ada subtotal per kelompok, baris Total/rekap di tengah, rincian Tunai/QRIS di bawah
total, dua tabel dalam satu sheet, cetakan bank multi-halaman) AI akan **selalu meminta konfirmasi Anda**
sebelum memberi angka final — tata letak laporan sangat beragam, jadi pengecekan singkat oleh Anda tetap perlu.

## Syarat
- File `.xlsx` atau `.csv` (≤ 50 MB). File `.xls` lama: buka di Excel lalu *Save As → .xlsx*.
- Python 3 di komputer (biasanya sudah ada di Mac/Linux; Windows: pasang gratis dari python.org).
  Tidak perlu paket tambahan, akun, atau API key. Tanpa Python pun skill tetap memandu langkah
  manual dengan rumus Excel yang setara.

## Instalasi singkat
Salin folder `analisis-excel` ke folder skills AI agent Anda:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |

Panduan lengkap (termasuk Windows): lihat `CARA-INSTAL.md` di dalam paket.

## FAQ
**Apakah data saya dikirim ke internet?**
Tidak oleh skill ini. Perhitungan berjalan di komputer Anda lewat script Python. Bila file berisi
data pribadi (NIK, No HP, gaji), skill akan mengingatkan dan hanya menampilkan ringkasan.

**Bisa membaca file Excel dengan banyak sheet?**
Bisa. Skill menyebutkan sheet apa saja yang ada dan sheet mana yang dianalisis; Anda tinggal
bilang "pakai sheet Rekap". Bila datanya dipecah satu sheet per bulan/kuartal, bilang saja
"gabungkan semua sheet" — total Januari–September dihitung sekaligus, baris TOTAL tiap sheet dibuang.

**Kenapa file CSV saya ditolak "Jumlah kolom tidak cocok"?**
Aturannya sederhana: setiap baris harus punya kolom sebanyak judul kolom. Bila satu baris kolomnya
kurang (ada sel terlewat) atau lebih (ada koma di dalam teks tanpa tanda kutip), angkanya bisa masuk
ke kolom yang salah dan totalnya keliru. Daripada memberi angka salah diam-diam, skill menyebut nomor
baris dan isinya agar Anda bisa membetulkannya. Kolom kosong di ujung kanan dan alamat/catatan yang
ditulis beberapa baris dalam satu sel tetap boleh, begitu juga kolom paling kanan yang sering
dikosongkan (mis. "Catatan") walau komanya tidak diketik — selama isi baris tidak bergeser. Pesan
galat menyebut kemungkinan penyebab (sel terlewat di tengah, koma tanpa tanda kutip, tanda kutip
nyasar, catatan di tengah tabel) dan langkah memperbaikinya.

**File ekspor Shopee/Tokopedia/mutasi bank saya ada baris Total, saldo, dan "Dicetak oleh…" di bawahnya. Aman?**
Aman. Baris yang **pasti** bukan data — Total/Grand Total/Rata-rata/Saldo Akhir dan catatan di bawah
tabel, Saldo Awal di atas tabel, sel berumus SUM/AVERAGE di Excel — tidak dihitung, dan skill menyebutkan
baris mana saja beserta isinya. Baris yang **mungkin** total (mis. angka tanpa keterangan yang kebetulan
sama dengan jumlah di atasnya) tidak dibuang diam-diam: skill tetap menghitungnya, memberi peringatan
tegas, menunjukkan total DENGAN dan TANPA baris itu, lalu menanyakannya kepada Anda. Sejak v1.0.7 ini
juga berlaku untuk baris "Jakarta Total" hasil Excel *Data › Subtotal* yang disimpan sebagai CSV dan
rincian pembayaran (Tunai/QRIS) di bawah "Total Penjualan". Judul kolom yang berulang tiap halaman dan
"Halaman 1 dari 2" dilewati; bila ada **tabel kedua** dengan judul kolom berbeda, skill berhenti dan
menyebut baris awalnya agar kedua tabel tidak tercampur. Sejak v1.0.8 juga baris subtotal/total yang
**terisi lengkap** (mis. "Subtotal Cabang Bekasi" dengan tanggal, qty, dan omzet), pivot yang disalin
sebagai nilai, dan tabel **tanpa baris judul kolom** (baris pertama tidak lagi hilang diam-diam).
Sejak v1.0.9 ada **pengaman silang**: bila file Anda punya baris Total/Grand Total, skill mencocokkan
angkanya dengan hasil hitungan. Cocok → disebutkan (lebih yakin). Beda (mis. hasil tepat 2× Grand Total
karena subtotal ikut terhitung) → peringatan tegas di atas hasil beserta kedua angkanya. Sejak v1.0.10,
bila justru **Total di file Anda yang keliru** (mis. angka yang tersimpan sebagai teks tidak ikut dijumlah
Excel), skill memberi tahu baris mana penyebabnya dan tidak menyodorkan angka file yang salah.

**Apakah bisa memprediksi penjualan bulan depan atau analisis statistik rumit?**
Tidak. Skill ini fokus menjawab pertanyaan dari data yang sudah terjadi (total, rata-rata, tren,
perbandingan). Untuk prediksi/statistik lanjut, gunakan jasa analis data.

## Riwayat versi
| Versi | Tanggal | Perubahan |
|---|---|---|
| 1.0.10 | 2026-09-25 | Revisi uji ulang v1.0.9: **B33** pengaman silang membedakan dua situasi — (1) hitungan tepat 2×/3× Total file → "Kemungkinan DOBEL HITUNG", total tanpa subtotal = angka file (satu-satunya kasus angka file ditawarkan); (2) selisih lain → "Total di file (Y) tidak sama dengan jumlah baris data (X) … Periksa rumus Total di file Anda" + "Angka Total di file BUKAN jawaban alternatif", dengan penyebab bila ditemukan: sel angka bertipe teks yang dilewati SUM Excel (X2: baris 4, 7) atau 1–3 baris tepi di luar rentang rumus (X9: baris 7) → turun menjadi PERINGATAN (hitungan script benar); field JSON `penjelasan`. **B34** nama produk berawalan "Total"/"Jumlah" ("Total Care Shampoo", "Jumlah Besar Hemat") pada baris terisi penuh tanpa angka = jumlah baris di atasnya bukan lagi kandidat ringkasan (label persis "Total", berakhiran ":", "Grand Total/Subtotal …" tetap). Semua fixture v1.0.0–v1.0.9 (139 file): 136 identik, 3 beda = perbaikan yang dituju (K2, X2, X9); 0 c; 133 tes. |
| 1.0.9 | 2026-09-25 | Revisi uji ulang v1.0.8: **B29** pivot bentuk ringkas dengan kelompok beranak TUNGGAL (baris kelompok = baris tepat di bawahnya) tidak lagi membatalkan deteksi seluruh file — dievaluasi per kelompok (syarat: ≥ 1 kelompok beranak ≥ 2 bila judul khas PivotTable, ≥ 2 bila bukan) — W8 c → b (TANPA = 6.140.000 / qty 51 = kunci). **B31 pengaman silang Grand Total** (lapis kedua untuk tata letak yang belum dikenal): angka baris Total/Grand Total/Jumlah di ekor tabel (dikeluarkan, rumus SUM, atau kandidat di baris terakhir) dibandingkan dengan total hitungan per kolom → cocok = catatan "COCOK dengan baris 'Total' di file"; = total TANPA kandidat = ditambahkan ke peringatan kandidat; beda = PERINGATAN TEGAS paling atas "Total hitungan X ≠ Grand Total di file Y" + "tepat 2×/3×" + total alternatif (subtotal kelompok terakhir & angka = rata-rata/min/maks tidak dipakai untuk peringatan beda; field JSON `cek_silang_total`). **B30** judul kolom angka bulat tampil apa adanya ("2023"). **B32** kolom nomor urut (#/No urut, atau Kolom1 tabel tanpa judul berisi 1..n) tidak dijumlah. Semua fixture v1.0.0–v1.0.8: 0 c; 127 tes; 50 ribu baris + 5.000 subtotal ±6 dtk. |
| 1.0.8 | 2026-09-25 | Revisi uji ulang v1.0.7: **B24** subtotal/total TERISI LENGKAP jadi kandidat (PERINGATAN TEGAS + total alternatif, tidak dibuang): angka kolom utama + ≥ 1 kolom angka lain = jumlah blok ≥ 2 baris di atasnya atau jumlah semua baris di atasnya (grand total), dengan pengaman kebetulan (kolom No/ID/nomor urut & kolom kembar diabaikan, ≥ 2 kolom bernilai > 100 atau kata ringkasan di sel teks unik, blok 2 baris di awal tabel wajib cocok semua kolom); kata ringkasan di kolom tanggal/angka ("Jumlah Hadir"); label = judul kelompok sebelumnya ("SEMEN" … "Subtotal Semen") — V1, V4, V5, V6 c → b (alternatif = kunci). **B25** tabel tanpa judul kolom: header bertanggal/berangka sejenis isi kolom → baris ikut dihitung, Kolom1..N, PERINGATAN TEGAS; opsi `--tanpa-header`, `--header-baris` (alias), `--baris-header 0`; tahun/nomor urut sebagai judul tetap judul — V13 c → a+peringatan (1.015.000). **B26** pivot bentuk ringkas: subtotal di atas anak-anaknya (tabel terbagi habis) dan "Jawa Total" di bawah → kandidat; info PivotTable — V3 c → b (7.500.000). P3: judul kelompok satu sel dilewati + disebut (**B28**, V1 n=10 bukan 13); CSV e-Faktur FK/LT/OF → GAGAL khusus + `--paksa --filter "FK=FK"` (V7 = DPP 17.500.000); kolom Tahun/Masa Pajak/Bulan = periode (V8 tidak lagi menjumlah Tahun); urut kode angka 1, 2, …, 10. Kinerja: jalur cepat rapikan teks & regex terkompilasi, pencarian rincian dengan bisect (50 ribu baris ±8 dtk, termasuk 5.000 subtotal). Semua fixture v1.0.0–v1.0.7: 0 c; 119 tes. |
| 1.0.7 | 2026-09-25 | Revisi uji ulang v1.0.6 — **pengaman umum**, bukan tambalan per tata letak: (1) detektor umum kandidat baris ringkasan (tidak membuang; PERINGATAN TEGAS + total alternatif TANPA SEMUA kandidat + per kandidat, pesan dibatasi 8 baris/30 nomor): (i) kata ringkasan utuh (Total/Subtotal/Jumlah/Grand/Rekap/Rata-rata/Saldo) di sel teks mana pun pada baris yang lebih jarang terisi daripada baris data — termasuk "Jakarta Total" dari *Data › Subtotal* (**B19**, S12); (ii) baris jarang yang angkanya = jumlah ≥ 2 baris tepat di atasnya; (iii) ≥ 2 baris jarang berurutan di bawah/atas baris ringkasan yang jumlahnya = baris itu (rincian Tunai/QRIS/Transfer, **B20**, S3: alternatif 159.000). (2) Judul kolom berulang (≥ 50% nama kolom di posisi sama) dilewati + info; judul laporan berulang & "Halaman x dari y" dilewati (**B23**, S4: 7 baris); judul kolom BERBEDA di tengah = tabel kedua → GAGAL "mulai baris N" (`--paksa` = PERINGATAN TEGAS) + opsi baru `--mulai-baris`/`--sampai-baris` (**B21**, S5). (3) `=SUM(C5,C9,C12)` dan `=C5+C9+C12` = rumus agregat → dikeluarkan (**B22**, S1b/S1c). (4) `profil` menampilkan 5 baris pertama & 5 terakhir yang DIPAKAI + tabel baris dikeluarkan + kandidat; SKILL.md: `profil` wajib sebelum angka apa pun + cek sekilas; README & SKILL.md jujur: paling andal untuk tabel rapi, laporan berformat selalu dikonfirmasi. Semua fixture v1.0.0–v1.0.6: tidak ada c (S3, S12 → b dengan alternatif = kunci; S5 → GAGAL jelas; S1b, S1c, S4 → a). 107 tes; 50 ribu baris < 8 dtk. |
| 1.0.6 | 2026-09-25 | Revisi uji ulang v1.0.5 — **ganti prinsip, bukan tambah aturan**: baris hanya dikeluarkan otomatis bila TIDAK ambigu: (a) XLSX sel berumus agregat SUM/SUBTOTAL/AVERAGE/COUNT/MIN/MAX/AGGREGATE atas baris lain (teks rumus `<f>`, termasuk rumus bersama; rumus per baris & saldo berjalan bukan ringkasan; nilai polos tanpa rumus tidak pernah dianggap ringkasan); (b) blok ekor berlabel ringkasan (label hanya di sel teks pertama) / catatan kaki (Catatan/NB/Sumber…, walau berangka) / teks yang dipisah baris kosong; (c) kepala (judul, Saldo Awal). Selain itu (Subtotal/label di tengah, angka tanpa label = jumlah/rata-rata di atasnya, termasuk subtotal kelompok 1 baris & SUM lalu AVERAGE di CSV) **tetap dihitung** + "PERINGATAN TEGAS — Kemungkinan baris ringkasan ikut terhitung: baris N (isi…)" di paling atas keluaran + total alternatif DENGAN/TANPA (per baris bila ≤ 4) + saran `--buang-baris N[,M]`. Opsi baru `--buang-baris` & `--pertahankan-baris` (gabungan sheet: `"TW1:7"`); JSON `baris_dikeluarkan`/`kemungkinan_ringkasan`/`total_alternatif`; isi baris ditulis "Kolom=nilai" dengan format rupiah (B18). SKILL.md: agent wajib menyebut baris dikeluarkan & kandidat, dan bertanya sekali/menampilkan kedua total sebelum angka final. Hasil fixture v1.0.5: R6/R6b/R7 (kategori), R8/R8c/R8d (catatan berangka), R11 (SUM/AVERAGE xlsx), R11b → a; R3, R3c, R5, R10, R16, R9, N11, N13 → b (kunci penguji = total default atau total alternatif); tidak ada c. Tes regresi per fixture (94 tes). |
| 1.0.5 | 2026-09-25 | Revisi uji ulang v1.0.4 (0 angka salah diam-diam, ekspor nyata terbaca tanpa `--paksa`): **B10** baris angka tanpa label yang isinya = jumlah/rata-rata kolom di atasnya (rumus SUM/AVERAGE; di tengah file = subtotal per kelompok, di ekor juga min/maks; toleransi Rp1) dilewati + peringatan "totalnya DOBEL"; label ringkasan dikenali di kolom mana pun (Rata-rata/Average/Saldo Awal/Saldo Akhir/Mutasi Kredit/Debet/Grand Total, "Jumlah pesanan:"; Min/Maks hanya bila satu-satunya teks). **B11/B12** blok catatan di bawah tabel ("Dicetak oleh…", "Sumber: …", catatan ber-padding) tidak dihitung sebagai data + info berisi isinya (jumlah baris, rentang tanggal, pivot bersih); kolom paling kanan yang opsional (mis. Catatan tanpa koma di ujung) boleh tidak ada bila isi baris tidak bergeser (tipe per kolom dicek) → N1, N2, N4 (mutasi BCA), N8 terbaca tanpa `--paksa`; sel terlewat di tengah (C8, N9) & kutip nyasar (C4) tetap GAGAL. Pesan GAGAL jumlah kolom berbahasa awam: sebut sel yang bergeser ("angka '18000' masuk kolom 'Barang'"), kemungkinan penyebab & langkah perbaikan. **B13** kolom berakhiran Code/ID/No/Ref = kode (tidak dijumlah); "Credit"/"Debet" dikenali sebagai uang. Tes regresi per file fixture v1.0.4 (+ varian XLSX SUM, subtotal tanpa label, kasus negatif). |
| 1.0.4 | 2026-09-25 | Revisi uji ulang v1.0.3 — **aturan jumlah kolom** menggantikan tebakan "baris di dalam sel tampak seperti data": setiap baris data CSV wajib punya jumlah kolom = judul kolom (sel kosong berlebih di ujung kanan boleh); baris kurang/lebih kolom → GAGAL dengan nomor baris + isi ringkas, atau `--paksa` + PERINGATAN TEGAS "N baris … MUNGKIN SALAH" (menutup B5/C8 & C4: angka salah diam-diam). Heuristik lama dihapus; cek "baris tertelan kutip nyasar" kini hanya untuk kolom yang biasanya satu baris (F3b tetap GAGAL; C5 alamat 3 baris + "50%⏎sisa" terbaca tanpa `--paksa`, B6). Info sel multi-baris jadi catatan ringan. B8: "≈ … (selisih Rp X)" bila rekap tidak persis sama; B9: periode tanpa data tidak lagi disebut "penurunan -100%". Tes regresi per file untuk semua fixture penguji + pengunci angka lama. |
| 1.0.3 | 2026-09-25 | Cegah angka salah diam-diam (uji ulang v1.0.2): kutip nyasar yang menelan satu baris data kini GAGAL dengan nomor baris — jumlah baris di Notepad dicocokkan dengan baris terbaca + baris lanjutan sel, dan baris lanjutan yang tampak seperti baris data utuh disebut sebagai "kemungkinan N baris data HILANG" (dengan `--paksa`: PERINGATAN TEGAS); sel multi-baris jarang di kolom yang biasanya satu baris diperingatkan "mungkin tanda kutip nyasar"; `--sheet semua` melewati sheet rekap/ringkasan (nama Ringkasan/Rekap/Total/Summary/Resume, isinya = jumlah sheet lain, atau sedikit baris berlabel bulan/triwulan) + opsi `--sertakan`; peringatan "kemungkinan DOBEL HITUNG" bila total gabungan ≈ 2 × total tanpa satu sheet; peringatan menyebut "N baris berisi sel multi-baris (M sel)"; "Kolom kolom" → "Kolom". Angka skenario 01–03 & file uji ulang v1.0.1/v1.0.2 yang benar tidak berubah (dikunci tes). |
| 1.0.2 | 2026-09-25 | Revisi uji ulang: CSV sah berisi alamat multi-baris berkoma tidak lagi ditolak (deteksi "kemungkinan rusak" kini memakai parser CSV + cek baris-mirip-data & jumlah kolom; kutip tak tertutup tetap GAGAL) + opsi `--paksa` untuk membaca apa adanya; `--sheet semua` memilih acuan struktur dari sheet yang paling banyak cocok (sheet Ringkasan di depan dilewati) + opsi `--acuan`; peringatan sel multi-baris digabung jadi satu dengan nomor baris Notepad ↔ Excel; judul "Total kolom Jumlah" (bukan "Jumlah Jumlah"); email tersamar menyertakan 2 karakter akhir (`a•••01@…`); "Uang Lembur"/tunjangan/THR/bonus ditandai sensitif, "Simpanan"/iuran/setoran dikenali sebagai uang; saran nomor sheet untuk nama sheet berkoma; "baris 4 s.d. 4" → "baris 4". Angka skenario 01–03 & 3 file uji ulang tidak berubah (dikunci tes). |
| 1.0.1 | 2026-09-25 | Revisi hasil uji independen: gabung beberapa sheet (`--sheet semua` / `"Q1,Q2,Q3"`, kolom `Sheet`, TOTAL per sheet dibuang, beda kolom diperingatkan); CSV bertanda kutip tak tertutup kini GAGAL dengan nomor baris (sebelumnya diam-diam menelan baris); kolom "Nilai terisi" + peringatan sel kosong di `pivot`/`top`; NIK/No HP/email/rekening disamarkan di tabel (opsi `--tampilkan-pribadi`) + peringatan gaji per orang; kategori "4 A" = "4A" digabung & dilaporkan; peringatan duplikat di semua subperintah; nama bulan diurut kronologis; label `banding` dua sheet = nama sheet; pesan-pesan kecil diperhalus. Angka skenario uji 01–03 tidak berubah (dikunci tes). |
| 1.0.0 | 2026-09-25 | Rilis draft pertama. |
