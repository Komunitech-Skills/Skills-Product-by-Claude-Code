# HASIL UJI — kas-umkm v1.0.0 (commit 757b3ed)

- Penguji: agent independen Akun B (tidak ikut membuat skill; kode `kas.py` tidak dibaca, hanya dijalankan).
- Tanggal: 2026-09-26. Lokasi uji: salinan di scratchpad (`uji-kas/`), data rekaan, database terpisah per skenario. Salinan kasir-lokal 1.1.1, laporan-keuangan-emkm, arus-kas-13minggu dipakai tanpa diubah.
- Platform: `claude-code (simulasi agent)`. `scripts/uji_openclaw.sh` **tidak** dijalankan (sesuai instruksi).

## Pemeriksaan otomatis
| Cek | Hasil |
|---|---|
| `tests/uji_regresi.py` | 59 tes OK (±3 dtk); ada 1 `ResourceWarning` file tidak ditutup di tes (kosmetik) |
| `python3 scripts/validate.py --skill kas-umkm` (dari root) | ✅ 1 skill valid, 77 baris katalog sesuai |
| Audit ringan script | tidak ada impor jaringan (`urllib/socket/http`), `subprocess`, `eval/exec`; Python standar |

## Skenario
| # | Berkas | Jenis | Skor |
|---|---|---|---|
| 01 | `01-warung-makan-laci-qris-rekening.md` | normal: laci + QRIS→BRI + GoPay, pindah dana, opname | 9 |
| 02 | `02-toko-kelontong-prive.md` | normal: prive > hasil usaha, batas prive, duplikat, batal | 9 |
| 03 | `03-laundry-bulanan-impor-ekspor.md` | normal: 2 bulan, impor kasir-lokal (retur, `--ganti`), ekspor emkm & arus kas | 9 |
| 04 | `04-input-tidak-lengkap-dan-data-rusak.md` | input kurang, nominal/tanggal buruk, CSV rusak/ambigu, DB rusak | 8 |
| 05 | `05-di-luar-cakupan-catatan-ganda-pajak.md` | berisiko: buku ganda untuk pajak, hapus catatan | 7 |
| A/B | `00-pembanding-tanpa-skill.md` | dengan skill jelas lebih baik (akun, pindah dana, prive, opname, persistensi) | — |
| Pesaing | `00-banding-pesaing.md` | ClawHub expense tracker ×2, bookkeeping-basics, BukuWarung → kas-umkm unggul (9 vs ≤6) | — |

## Verifikasi angka independen (Decimal, dari input)
Semua cocok ke rupiah:
- Saldo per akun di 01 (Laci 1.578.500 / BRI 4.830.000 / GoPay 225.000), 02 (Laci 6.300.000 / BCA 1.350.000), 03 (Laci 10.002.000 / Mandiri 9.499.000, 143 transaksi), 04 impor (BRI 5.269.066).
- Pindah dana: total saldo tetap, hasil usaha tidak berubah (hanya biaya admin → lain-lain); 8 pindah di 03 bersih 0.
- Opname per pecahan 1.233.500, selisih kurang 345.000; `--sesuaikan` mencatat penyesuaian dan hasil usaha ikut turun.
- Rekap per kategori & hasil usaha Agustus 8.245.000 / September 7.856.000; prive % 9,7 / 10,2 / 106,4 (dengan kelebihan 150.000).
- Impor kasir-lokal: per metode 72.000/59.000/35.000; nilai minus (retur QRIS −35.000) jadi keluar retur; `--ganti` membatalkan impor lama.
- Ekspor emkm → `laporan_emkm.py` laba bersih = hasil usaha (8.245.000; 7.856.000), neraca seimbang, kas cocok `--kas-akhir-aktual`.
- Ekspor arus-kas → rata-rata 2.975.000 & 228.571 (pembulatan HALF_UP benar), `proyeksi_kas.py` berjalan, minggu 1 keluar 3.908.571 cocok.
- Pembulatan sen dari file bank 215.500,50 → 215.501 (0,5 ke atas), diberitahukan.

## Temuan (berprioritas)
1. **[SEDANG] `impor --ya` tetap menyimpan baris `perlu_dicek` sebagai "lain-lain".** Contoh "TARIK TUNAI ATM" 500.000 tersimpan sebagai beban → hasil usaha turun 500.000 dan laci tidak bertambah, bila agent tidak menanyakan dulu. `perlu_izin` kosong sehingga tidak ada pengaman. Saran: jadikan `perlu_dicek` bagian dari `perlu_izin` (wajib `--tetapkan` atau flag eksplisit mis. `--terima-tebakan`).
2. **[SEDANG] Tidak ada larangan eksplisit membuat catatan ganda / mengurangi omzet / menghapus catatan untuk pajak.** Penolakan saat ini bergantung pada etika model. Tambahkan satu baris di "Kapan TIDAK digunakan" + "Batasan" (arahkan ke rekap yang benar, `pph-final-umkm`, konsultan).
3. [RENDAH] Prive bulanan diratakan per minggu di ekspor arus-kas (228.571/minggu padahal 800.000 tiap tgl 15). Pertimbangkan perlakuan seperti pos bulanan bila frekuensinya < separuh minggu, atau sebut di teks.
4. [RENDAH] Tebakan kategori tidak konsisten ("SPP anak" → prive, "belanja bulanan rumah" → ditanya). Aman (gagal ke arah bertanya), tetapi kata "rumah"/"belanja rumah" layak masuk kamus prive.
5. [RENDAH] Pesan kurang ramah: `--keluar -20rb` (argparse), pecahan `100rb x lima` → "Nominal 'rb x lima' tidak dikenali"; teks ekspor emkm "Pindah dana (10 baris)" = 5 pindah × 2 sisi.
6. [KOSMETIK] `ResourceWarning` di `tests/uji_regresi.py` baris 599 (`open` tanpa `with`).
7. [CATATAN] Sintaks `openclaw automations add ...` di `references/openclaw-jadwal.md` tidak diverifikasi di uji ini (uji_openclaw.sh tidak dijalankan).

## Skor kualitas: **8/10**
Alasan: inti buku kas (saldo multi-akun, pindah dana, opname, prive, rekap) benar ke rupiah di semua uji independen; rantai integrasi kasir-lokal → kas-umkm → laporan-keuangan-emkm / arus-kas-13minggu berjalan tanpa modifikasi dan angkanya konsisten; penanganan input buruk sangat baik (nominal/tanggal ambigu, CSV rusak, DB rusak, formula injection, duplikat, minus). Unggul jelas atas A/B dan pesaing. Dikurangi karena celah pengaman `perlu_dicek` di impor dan belum adanya larangan eksplisit catatan ganda untuk pajak (keduanya perbaikan kecil). Setelah temuan 1–2 diperbaiki dan diuji ulang, layak 9.

Rekomendasi status: **lulus** (skor ≥ 7), dengan perbaikan temuan 1–2 sebelum uji platform asli/beta.

---

## Uji ulang v1.0.1 (Akun B)
- **Tanggal:** 2026-09-26 · **Penguji:** agent independen Akun B (bukan pembuat) · rincian: `examples/06-uji-ulang-v1.0.1-akun-b.md`
- **Lingkungan:** salinan skill + `laporan-keuangan-emkm` di scratchpad, Linux, Python 3.11, data fiktif; simulasi agent `claude-code`.

| Temuan lama | Status v1.0.1 |
|---|---|
| 1 impor `perlu_dicek` jadi lain-lain | **Tertutup.** 3 baris tak jelas disimpan "Perlu dicek": ikut saldo, tidak ikut hasil usaha (2.092.500), `ekspor --format emkm` ditolak (`perlu_dicek: [11,12,13]`) sampai `golongkan` → 4.942.500. Tarik tunai ATM / setor tunai / top up GoPay otomatis pindah dana; pindah buku tanpa nama akun → Perlu dicek; `catat` "tarik tunai" diarahkan ke `pindah`. Decimal independen: Laci 600.000 / BRI 9.042.500 (= saldo file) / GoPay 400.000, pindah dana 0 terhadap hasil usaha — cocok semua. |
| 2 larangan pembukuan ganda | **Tertutup** (instruksi): Kapan TIDAK + Aturan 7 (UU KUP Ps. 28 (3), Ps. 39 (1) d & f) + checklist; 4 kalimat penggelapan ditolak, 1 permintaan sah (batal salah ketik) tidak ditolak. |
| 6 ResourceWarning | Tertutup (0 peringatan). |

Temuan baru:
1. **[SEDANG]** Ekspor emkm mengosongkan kategori lain-lain; `laporan_emkm.py` membaca "BIAYA TARIK TUNAI ATM BERSAMA" sebagai pindah dana → laba emkm 4.950.000 vs hasil usaha 4.942.500, neraca **TIDAK SEIMBANG −7.500** dengan `--kas-akhir-aktual`. Isi kode `beban_lain` eksplisit + tes rantai.
2. **[RENDAH]** "Per minggu" mencampur 'Perlu dicek' di masuk/keluar tetapi tidak di hasil usaha.
3. **[RENDAH]** `golongkan` penjualan→modal tanpa peringatan (bergantung Aturan 7).
Tanpa regresi: 65 tes OK; DB v1.0.0 → Agustus 8.245.000, ekspor emkm Agustus identik byte-per-byte; bangun ulang laundry = angka lama; `validate.py --skill kas-umkm` ✅.

### Skor: **8/10**
Alasan: kedua temuan SEDANG lama tertutup dan angka inti benar ke rupiah; tetapi perbaikan pindah dana memunculkan ketidakcocokan baru di rantai kas-umkm → laporan-keuangan-emkm (laba & neraca meleset untuk baris biaya tarik tunai) — kecil nominalnya, tetapi merusak kepercayaan laporan untuk bank/KUR. Setelah temuan baru 1 diperbaiki + dites → layak 9.

## Uji ulang independen v1.0.2 (Akun B, 2026-09-26)
- **Penguji:** agent independen Akun B (bukan pembuat) · rincian: `examples/07-uji-ulang-v1.0.2-akun-b.md`
- **Lingkungan:** salinan skill + `laporan-keuangan-emkm` 1.3.0 di scratchpad, Linux, Python 3.11, data fiktif; simulasi agent `claude-code`.

| Temuan uji ulang v1.0.1 | Status v1.0.2 |
|---|---|
| 1 [SEDANG] biaya tarik tunai hilang dari laba emkm | **Tertutup.** Data uji 06 diulang: baris diekspor `beban_keuangan`; emkm laba **4.942.500 = hasil usaha**, neraca seimbang, selisih 0, selisih kas 0 (v1.0.1: 4.950.000, −7.500). Data baru penguji (Mandiri + OVO; biaya adm/tarik tunai/BI-FAST/adm OVO/tarik tunai agen, bunga, pajak bunga): laba **2.789.487 = hasil usaha**, seimbang, selisih 0 — ekspor v1.0.1 atas DB yang sama memberi laba 2.870.987 dan selisih −81.500. Saldo per akun cocok hitung Decimal penguji. |
| 2 [RENDAH] per minggu mencampur 'Perlu dicek' | **Tertutup.** Baris per minggu & per hari yang memuat 'Perlu dicek' diberi penanda "[termasuk 'Perlu dicek' … - belum dihitung di hasil usaha]"; baris lain tanpa penanda; hilang setelah `golongkan`. |
| 3 [RENDAH] `golongkan` penjualan → modal | Belum diubah (di luar cakupan v1.0.2). |

Temuan baru: **[RENDAH-SEDANG]** catatan `lain-lain` keluar berketerangan "bayar utang…", "belanja rumah", "uang muka karyawan…", "cicilan…" diekspor dengan kategori kosong → emkm menggolongkannya prive/piutang lain/bayar pinjaman → laba emkm ≠ hasil usaha (uji: selisih 410.000) dan emkm melaporkan utang pinjaman negatif. Tidak diam-diam (catat memberi catatan prive; emkm bertanya), tetapi perluas `POLA_RAWAN_EMKM` + tes rantai. **[RENDAH]** "BIAYA TRF BI-FAST" saat impor jatuh ke 'Perlu dicek'.
Tanpa regresi: 68 tes OK; `rekap` DB uji lama identik antara v1.0.1 dan v1.0.2 (0 baris beda), laundry Agustus 8.245.000, ekspor emkm Agustus identik byte-per-byte; `validate.py --skill kas-umkm` ✅.

### Skor: **9/10**
Alasan: temuan SEDANG tertutup dan terbukti pada data uji lama serta data baru (laba emkm = hasil usaha, neraca seimbang, selisih 0), penanda 'Perlu dicek' jelas, angka inti tepat ke rupiah, tanpa regresi. Dikurangi 1 karena golongan ketidakcocokan yang sama masih bisa muncul untuk kata non-beban lain di keterangan lain-lain (walau kini ditandai emkm) dan platform asli belum diuji.

## Uji ulang v1.0.3 (2026-09-28)
- **Penguji:** agent independen (bukan pembuat); hanya membaca folder skill, scratchpad `uji-keu-0928/kas`, data fiktif, Linux, Python 3.11; rantai ke `laporan-keuangan-emkm` (repo saat ini).
- **Tes regresi:** `tests/uji_regresi.py` **72/72 OK**; `laporan-keuangan-emkm/scripts/uji_regresi.py` **SEMUA UJI LULUS**.
- **Data:** warung fiktif Agustus 2026, **40 baris** (laci 3 jt + BRI 5 jt; penjualan, kulakan, gaji, sewa, listrik, PBJT, prive) dengan jebakan: bayar bunga pinjaman KUR, denda telat cicilan, belanja rumah, kasbon Andi (+ dikembalikan), kasbon Budi (+ potong gaji), bayar utang toko bangunan, ongkos pinjam troli, biaya parkir pinjam mobil, biaya provisi pinjaman, bunga pinjaman koperasi (tanpa kategori), uang saku anak (tanpa kategori), angsuran motor pribadi, pinjaman dari saudara, "Bu Ani bayar hutang belanja", "Rudi pinjam uang", denda pajak.

Penggolongan ulang `lain-lain` (baru v1.0.3) — benar untuk: belanja rumah/angsuran motor pribadi → prive; kasbon Andi/Andi kembalikan kasbon → kasbon (keluar/masuk); pinjaman dari saudara → pinjaman masuk; bunga pinjaman KUR, denda telat cicilan, biaya provisi pinjaman, bunga pinjaman koperasi → tetap lain-lain (biaya); "pinjam troli"/"pinjam mobil" → tetap biaya (tidak salah tangkap). Jalur `impor` CSV juga menggolongkan ulang dengan alasan tertulis. ✅

Angka (Decimal penguji): masuk 11.734.000, keluar 10.154.000, kas akhir 9.580.000, **hasil usaha 3.230.000**, prive 1.700.000, kasbon sisa 350.000 — semua cocok `rekap`. Ekspor emkm + `--utang-bank-awal 20jt`: neraca **seimbang** (aset 9.930.000), piutang lain 350.000 ✅, tetapi **laba emkm 3.255.000 ≠ hasil usaha 3.230.000 (selisih 25.000)** dan utang pinjaman 20.375.000 (seharusnya 20.400.000). **Mismatch: 1 baris / 2 angka.**

Temuan:
1. **[SEDANG] Invarian laba = hasil usaha pecah untuk denda/biaya cicilan.** `kode_emkm` mengekspor "denda telat cicilan" dengan kategori **kosong**; emkm membaca kata "cicilan" → `bayar_pinjaman`. Uji mini: "denda telat cicilan" 25rb, "denda keterlambatan angsuran" 30rb, "biaya admin cicilan" 5rb → ketiganya jadi pokok (60rb); hanya "bunga cicilan KUR" tetap beban. Saran: lain-lain keluar yang cocok `POLA_UTANG` + `POLA_BUNGA_BIAYA` diekspor eksplisit `beban_keuangan`; tambah tes rantai.
2. **[SEDANG] "bayar utang toko bangunan" (utang pemasok) → pinjaman → `bayar_pinjaman`.** Di buku kas, belanja bon pemasok biasanya belum pernah dicatat, jadi pembayarannya adalah biaya/pembelian; di data uji hasil usaha terlalu tinggi 750.000 (23%) dan utang bank terbaca turun padahal utang ke bank tidak berubah. Ada mitigasi (catatan pratinjau menyebut "bila melunasi bon belanja stok … beli-stok"; ekspor mengingatkan `--utang-bank-awal`), tetapi bila kategori kosong dan ditebak dari "hutang" hanya muncul "Asumsi … ditebak", tanpa petunjuk itu. Saran: kata toko/agen/supplier/grosir/bon + utang → tanyakan (beli-stok vs pinjaman), atau ekspor `bayar_utang_usaha`.
3. **[SEDANG-RENDAH] Uang masuk "Bu Ani bayar hutang belanja" → pinjaman diterima.** Pelanggan melunasi bon warung dibaca sebagai utang baru: pendapatan kurang 150.000, utang lebih 150.000. Saran: arah masuk + nama/pelanggan/bon → penjualan atau tanyakan.
4. **[RENDAH]** "Rudi pinjam uang" (karyawan pinjam, urutan kata terbalik) tetap biaya lain-lain, bukan kasbon.
5. **[RENDAH, emkm]** "denda pajak telat lapor" masuk "Beban pajak penghasilan" (sanksi, bukan PPh).

Hasil usaha menurut penggolongan penguji (utang pemasok = biaya, Bu Ani = penjualan, Rudi = kasbon): 2.590.000 vs script 3.230.000.

### Skor: **6,5/10** (revisi, uji ulang)
Alasan: fitur kasbon & penggolongan ulang prive/kasbon/bunga bekerja, angka buku kas tepat ke rupiah, neraca emkm seimbang, tanpa regresi. Tetapi syarat utama rilis ini (laba emkm = hasil usaha) gagal pada jebakan yang disebut di brief ("denda telat cicilan"), dan kata "utang/hutang" masih membelokkan transaksi pemasok & pelanggan ke pinjaman bank sehingga laba warung bisa melenceng ratusan ribu. Perbaikan kecil dan terarah (pola ekspor + pertanyaan untuk utang pemasok/pelanggan).

## Uji ulang v1.0.4 (2026-09-28)
- **Penguji:** agent independen (bukan pembuat, bukan penguji v1.0.3); hanya membaca folder skill; salinan skill + `laporan-keuangan-emkm` di scratchpad `uji-kas-104`, Linux, Python 3.11, data fiktif; simulasi agent `claude-code`.
- **Tes regresi:** `tests/uji_regresi.py` **76/76 OK**; `laporan-keuangan-emkm/scripts/uji_regresi.py` **SEMUA UJI LULUS**; `validate.py --skill kas-umkm` ✅.
- **Data baru:** bengkel motor fiktif Agustus 2026, **57 baris** (48 `catat` + 9 baris impor mutasi BRI) + 3 pindah dana (setor laci, tarik tunai BCA + biaya Rp 6.500, tarik tunai ATM dari impor). Akun: Laci 2 jt, BCA 12 jt (QRIS), BRI 2 jt; utang bank awal 20 jt. Jebakan: cicilan KUR bulan 3, bunga KUR, "angsuran motor + denda", denda telat cicilan, biaya admin cicilan, denda keterlambatan angsuran leasing, biaya provisi, lunasi bon ke Toko Sinar, bon grosir oli, utang supplier sparepart, bayar utang toko Pak Joko, pelanggan nyicil servis, Pak Dedi bayar hutang servis, Bu Ani bayar hutang belanja, (ongkos) pinjam kunci, kasbon mekanik, Rudi/mekanik Joni pinjam uang, pajak kendaraan usaha, denda pajak telat lapor, sanksi administrasi PPh, belanja dapur rumah, SPP anak, uang saku anak; impor: TRSF BYR UTANG SUPPLIER, TRSF LUNASI BON TOKO SINAR, DENDA TELAT ANGSURAN KUR, ANGSURAN KUR, TRSF DARI PELANGGAN BAYAR HUTANG SERVIS, BIAYA TARIK TUNAI, BUNGA/PAJAK BUNGA.

| Perbaikan v1.0.4 | Hasil |
|---|---|
| 1 bunga/denda/biaya admin cicilan tetap biaya | ✅ denda telat cicilan, biaya admin cicilan, denda keterlambatan angsuran leasing, bunga KUR, provisi, DENDA TELAT ANGSURAN KUR (impor) → `lain-lain` → ekspor `beban_keuangan`. |
| 2 utang pemasok ≠ pinjaman bank | ✅ tanpa kategori: lunasi bon ke Toko Sinar / bon grosir oli / utang supplier sparepart / bayar utang toko Pak Joko / pelunasan hutang dagang **ditolak** (`perlu_kategori`, `utang_pemasok`) dengan pilihan beli-stok/lain-lain; `lain-lain` → `bayar_utang_usaha` + peringatan; `pinjaman` (catat & golongkan) → peringatan. Impor → "Perlu dicek" dengan saran `--tetapkan`; ekspor emkm ditolak sampai digolongkan. |
| 3 pelanggan bayar hutang = penjualan | ✅ "Bu Ani bayar hutang belanja", "pelanggan nyicil servis", "pelunasan bon servis Pak Dedi", impor "…PELANGGAN BAYAR HUTANG SERVIS" → penjualan. ❌ lihat temuan 2. |
| 4 "X pinjam uang" → kasbon; denda pajak → beban_lain | ✅ Rudi/mekanik Joni pinjam uang → kasbon (juga dari lain-lain); "ongkos pinjam kunci torsi"/"pinjam kunci" tidak salah tangkap (ditanyakan). Denda pajak & sanksi administrasi PPh → `pajak` + catatan tidak boleh dikurangkan (Pasal 9 (1) k) → ekspor `beban_lain`; emkm beban PPh hanya PPh final Rp 120.000. |

**Angka (Decimal penguji, dihitung dari daftar transaksi penguji, bukan dari DB):** masuk 12.202.500, keluar 13.767.000, saldo Laci 4.710.000 / BCA 8.858.500 / BRI 867.000 = **14.435.500**, hasil usaha **−3.339.500**, prive 470.000, kasbon sisa 155.000, utang bank 21.400.000 — semua cocok `rekap`/ekspor. Emkm (`--utang-bank-awal 20000000`): **laba −3.339.500 = hasil usaha**, neraca **seimbang** (14.590.500), kas akhir aktual cocok, opname laci PAS. **Mismatch angka script vs hitungan independen: 0.**
Regresi: tarik tunai ATM dikenali pindah dana, BIAYA TARIK TUNAI & biaya pindah → `beban_keuangan`, 'Perlu dicek' memblokir ekspor, peringatan prive, Aturan 7 (pembukuan ganda) utuh + dites. Tanpa regresi.

Mismatch penggolongan (menurut penguji) — 3 baris: hasil usaha seharusnya **−1.754.500** (selisih 1.585.000):
1. **[SEDANG] "angsuran motor + denda" (840rb, satu baris gabungan) → seluruhnya biaya** (ditebak dari kata 'denda'); pokok ±800rb ikut jadi beban, utang tidak berkurang. Sama untuk "angsuran leasing mobil derek + denda 50rb". Saran: bila ada kata angsuran/cicilan **dan** denda/bunga dalam satu baris → tolak & minta dipisah (pokok = pinjaman, denda = lain-lain).
2. **[SEDANG-RENDAH] Uang masuk "Pak Dedi bayar hutang servis" → pinjaman diterima** (ditebak dari 'hutang'). Pola pelanggan hanya menangkap "belanja"/"bon"/"pelanggan"; kata usaha jasa (servis, cuci, jahit, laundry) + nama orang lolos. Pendapatan −400rb, utang +400rb (emkm utang bank 21,4 jt, seharusnya 21 jt).
3. **[RENDAH] "belanja dapur rumah" (kategori lain-lain) tetap biaya** (hanya "belanja rumah"/"rumah tangga" dipindah ke prive; "belanja dapur", "belanja sayur rumah" lolos). Tidak diam di emkm (masuk "belum terklasifikasi"), tetapi `rekap` menghitungnya sebagai biaya (385rb).

Temuan lain:
4. **[SEDANG-RENDAH] Risiko hitung ganda pembelian kredit.** `catat --keluar --kategori beli-stok --catatan "beli oli ngebon di Toko Sinar (bayar belakangan)"` / "tempo 30 hari" / "belum dibayar" diterima tanpa peringatan dan mengurangi laci padahal belum ada uang keluar; pelunasan berikutnya (beli-stok lagi) → biaya ganda. Tanpa kategori, pesan penolakannya menyebut "bayar utang/bon" (keliru: ini pembelian bon, bukan pembayaran). Saran: kata ngebon/tempo/belum dibayar/bayar belakangan pada uang keluar → tolak: "Belum ada uang keluar; catat saat dibayar."
5. **[RENDAH]** SKILL.md menyebut memilih `pinjaman` untuk kasus v1.0.4 "tetap ada peringatan", tetapi `--kategori pinjaman` untuk "denda telat cicilan" dan "Rudi pinjam uang" tidak memberi peringatan (utang pemasok & Bu Ani memberi).
6. **[RENDAH]** "denda pajak telat lapor" dengan `--kategori lain-lain` tanpa catatan non-deductible (ekspor tetap `beban_lain` ✓). Impor "PAJAK BUNGA" (PPh final atas bunga bank, bukan sanksi) ikut diekspor `beban_lain` alih-alih beban PPh (laba tidak berubah).
7. **[RENDAH]** "bayar utang ke Pak Joko" / "bayar hutang" (tanpa kata toko) masih ditebak `pinjaman` (disebut di Asumsi) — wajar karena ambigu, tetapi lebih aman ditanyakan.

**Penilaian keraguan pembuat ("bayar utang toko Pak Joko" = biaya):** **benar untuk buku kas berbasis kas.** kas-umkm hanya mencatat uang bergerak; saat ambil barang secara bon belum ada uang keluar, jadi pembayaran adalah kejadian kas pertama = belanja. Ekspor `bayar_utang_usaha` membuat emkm menghitungnya sebagai pembelian (laba = hasil usaha); bila bon memang sudah tercatat sebagai utang di awal periode, `--utang-usaha-awal` membuat emkm tidak membebankannya lagi (diuji: `--utang-usaha-awal 1000000` → laba −2.339.500, utang usaha 0, neraca seimbang) — benar secara akrual. Hitung ganda hanya terjadi bila pembelian bon ikut dicatat sebagai uang keluar saat barang diambil (temuan 4) atau bila bon periode lalu sudah dibebankan di laporan emkm sebelumnya tetapi `--utang-usaha-awal` tidak diisi. Keduanya perlu dicegah dengan pertanyaan, bukan dengan mengembalikan ke `pinjaman`.

### Skor: **7,5/10** (layak lanjut; perbaiki temuan 1, 2, 4 di v1.0.5)
Alasan: keempat perbaikan v1.0.4 terbukti pada data baru di jalur catat, impor, dan golongkan; invarian laba emkm = hasil usaha terjaga, neraca seimbang, semua angka tepat ke rupiah, tanpa regresi. Dikurangi karena frasa jebakan baru masih lolos: baris gabungan angsuran + denda, pelanggan jasa "bayar hutang servis", pembelian bon yang dicatat sebagai uang keluar, dan variasi belanja rumah — total menggeser hasil usaha Rp 1,585 jt pada data uji; platform asli belum diuji.

## Uji ulang v1.0.5 (2026-09-28)
- **Penguji:** agent independen (bukan pembuat, bukan penguji v1.0.3/v1.0.4); hanya membaca folder skill; salinan skill + `laporan-keuangan-emkm` di scratchpad `uji-kas-105`, Linux, Python 3.11, data fiktif; simulasi agent `claude-code`.
- **Tes regresi:** `tests/uji_regresi.py` **84/84 OK** (1 dilewati: kasir-lokal tidak ada di sebelahnya); `laporan-keuangan-emkm/scripts/uji_regresi.py` **SEMUA UJI LULUS**; `validate.py --skill kas-umkm` ✅.
- **Data baru:** "Laundry Wangi" fiktif, Agustus 2026, **58 baris** (49 frasa `catat` → 51 catatan setelah dipisah + 9 baris impor mutasi BCA) + 4 pindah dana (3 tarik tunai BCA→laci, 2 di antaranya dengan biaya Rp 6.500; 1 setor laci→BCA). Akun: Laci 1,5 jt, BCA 8 jt (QRIS); utang bank awal 15 jt. Setiap frasa dicatat dulu **tanpa kategori** (melihat tebakan/penolakan), lalu dengan kategori jawaban "pengguna" + `--ya`. Frasa jebakan baru: cicilan mesin cuci + bunga, nyicil mesin pengering bulan 4 plus denda, Mbak Rina lunasi laundry bulan lalu, ambil deterjen ngebon di toko kimia, bayar tempo toko kimia, uang jajan anak, belanja dapur, belanja sayur rumah, bayar hutang ke Koh Ahong, bayar hutang ke Bu Lastri, Pak Harun bayar hutang laundry, Bu Wati bayar bon cucian, Bu Ida bayar laundry yang kemarin ngebon, Dodi pinjam uang, denda telat bayar PDAM, biaya admin angsuran leasing, denda keterlambatan cicilan, DP beli rak jemuran sisanya tempo, bayar KUR BRI termasuk bunga; impor: TRSF CICILAN MESIN CUCI + BUNGA, TRSF BYR HUTANG KOH AHONG, TRSF DARI RINA LUNASI LAUNDRY, TARIK TUNAI ATM, BIAYA TARIK TUNAI, BUNGA, PAJAK BUNGA, BIAYA ADM.

| Perbaikan v1.0.5 (temuan v1.0.4) | Hasil |
|---|---|
| 1 pokok + denda/bunga satu baris → tolak | ✅ "cicilan mesin cuci + bunga", "nyicil … plus denda", "bayar leasing plus denda", impor "TRSF CICILAN MESIN CUCI + BUNGA" (Perlu dicek, saran dipisah). ❌ lolos: akhiran **-nya** ("angsuran motor plus dendanya", "cicilan … sama bunganya", "+ adminnya") → **seluruhnya `pinjaman`** tanpa peringatan, juga dengan `--kategori pinjaman`; tanpa kata cicilan/angsuran ("bayar KUR BRI termasuk bunga", "setoran KUR + bunga", impor "BYR KUR BRI TERMASUK BUNGA"/"SETORAN KREDIT + BUNGA"/"PEMBAYARAN PINJAMAN DAN BUNGA") → **seluruhnya `lain-lain`** (hanya "ditebak"); "bayar pinjaman koperasi dan bunganya" → seluruhnya `pinjaman`. |
| 2 pelanggan jasa bayar hutang = penjualan | ✅ "Pak Harun bayar hutang laundry", "Bu Wati bayar bon cucian" → penjualan; "Koh Ahong bayar hutang" (masuk) ditanyakan. "Mbak Rina lunasi laundry bulan lalu" & impor "…RINA LUNASI LAUNDRY" ditanyakan (aman). |
| 3 belanja dapur/sayur rumah = prive | ✅ "belanja dapur rumah", "belanja sayur rumah" → prive; "uang jajan anak" → prive (juga dari `lain-lain`). "belanja dapur" saja → ditanyakan (wajar: di katering itu bahan usaha), tetapi dengan `--kategori lain-lain` diterima diam-diam sebagai biaya. |
| 4 ngebon/tempo/belum dibayar → tolak | ✅ "ambil deterjen ngebon di toko kimia" ditolak (juga dengan `--kategori beli-stok`); tidak salah tolak: "lunasi deterjen yang ngebon minggu lalu", "bayar bon … yang kemarin belum dibayar", "pelunasan pembelian tempo 30 hari", "bayar tempo toko kimia" (beli-stok), "DP beli rak jemuran, sisanya tempo". ❌ **uang masuk** "Bu Ida bayar laundry yang kemarin ngebon", "pelanggan bayar laundry tempo minggu lalu", "terima pembayaran laundry hotel (tempo 14 hari)" ditolak `belum_ada_uang` **walau `--kategori penjualan`** (uang sudah diterima; hanya bisa lewat dengan mengubah catatan). |
| 5 peringatan kategori pilihan | ✅ `pinjaman` untuk "Dodi pinjam uang" & "bayar hutang toko kimia" → peringatan; `lain-lain` untuk "bayar hutang ke Koh Ahong" → peringatan "tetap biaya". |
| 6 denda pajak & PAJAK BUNGA | ✅ "denda pajak telat lapor SPT" + `lain-lain` → peringatan Pasal 9 (1) k; impor "PAJAK BUNGA" → `pajak` + penjelasan, ekspor `beban_pajak_penghasilan`; "BUNGA" masuk → `pendapatan_lain`. |
| 7 "bayar utang ke <nama>" ditanyakan | ✅ Koh Ahong, Bu Lastri → `utang_ambigu` (keluar), impor "TRSF BYR HUTANG KOH AHONG" → Perlu dicek dengan saran pinjaman/beli-stok/lain-lain. |

**Angka (Decimal penguji dari daftar transaksi penguji, 72 catatan termasuk sisi pindah dana):** masuk 11.077.345, keluar 14.332.969, saldo Laci 1.440.000 / BCA 4.804.376 = **6.244.376**, **hasil usaha −2.125.624**, prive 1.030.000, kasbon sisa 150.000, pokok dibayar 4.950.000, pinjaman diterima 3.000.000, utang akhir 13.050.000 — **semua cocok** `rekap`/ekspor/emkm; opname laci Rp 1.440.000 PAS. **Mismatch angka: 0.**
Emkm (`--utang-bank-awal 15000000`): neraca **seimbang** (Rp 6.694.376), utang bank 13.050.000 ✅, beban PPh = 175.000 + 2.469 ✅. **Laba emkm −1.825.624 ≠ hasil usaha −2.125.624 (selisih 300.000)**: baris "DP beli rak jemuran" diekspor kategori kosong dan emkm menggolongkannya **aset tetap** (benar menurut SAK EMKM, bukan salah hitung). Dengan baris itu ditetapkan `beban_lain`, laba emkm = **−2.125.624 = hasil usaha**, neraca seimbang (6.394.376). Invarian terjaga; teks ekspor kas-umkm belum mengingatkan bahwa pembelian alat/aset membuat laba ≠ hasil usaha.
**Regresi:** tarik tunai ATM (impor) → pindah dana ✅; `pindah --biaya` & BIAYA TARIK TUNAI/BIAYA ADM → `beban_keuangan` ✅; utang pemasok tanpa kategori ("lunasi bon ke Toko Sinar", "bayar utang supplier deterjen", "bayar hutang toko kimia") → `utang_pemasok` ✅, ekspor `pembelian_bahan`; kasbon keluar/kembali & sisa di neraca ✅; peringatan prive ✅; Aturan 7 pembukuan ganda utuh + dites ✅. **Tanpa regresi.**

**Penolakan salah (false refusal):** dari 41 frasa normal di data, kode penolakan baru v1.0.5 muncul pada **1** (Bu Ida … ngebon, uang masuk); di probe tambahan 4 lagi: 2 uang masuk bertempo (di atas) dan 2 negasi yang ditolak `gabungan_pokok_denda` walau `--kategori pinjaman` ("cicilan ke-4 lunas tanpa denda", "angsuran mesin cuci bebas bunga 0%"). Semua jebakan yang memang ambigu (7/8) ditanyakan. Terpisah: 16/41 frasa normal laundry tanpa kategori dijawab "kategori belum jelas" (cuci kiloan, laundry express, beli deterjen/pewangi/plastik, service mesin cuci, fotokopi nota) — bukan blokir (agent bisa langsung mengisi kategori), tetapi kosakata tebakan untuk usaha jasa masih sempit.
**Bahasa penolakan:** sopan dan jelas alasannya, tetapi ditujukan ke agent (berisi `--kategori`, `--baris "keluar;<pokok>;…"`, huruf KAPITAL, awalan "GAGAL:" di mode teks). Agent harus menerjemahkan; SKILL.md belum memberi contoh kalimat tanya untuk pengguna awam (mis. "Dari Rp 1.100.000 itu, berapa bunganya? Nanti saya catat pokok dan bunganya terpisah.").

Temuan (berprioritas):
1. **[SEDANG] Perbaikan 1 bisa dilewati** oleh akhiran -nya (dendanya/bunganya/adminnya → seluruhnya pokok, beban bunga hilang, utang turun terlalu banyak, tanpa peringatan) dan oleh baris pokok+bunga tanpa kata cicilan/angsuran (KUR/kredit/pinjaman + bunga → seluruhnya biaya, di catat maupun impor). Contoh "bayar KUR BRI termasuk bunga" 1,1 jt: hasil usaha kurang Rp 1 jt. Saran: normalisasi akhiran -nya; perlakukan KUR/kredit/pinjaman/leasing/setoran sebagai kata pokok bila disambung kata denda/bunga.
2. **[SEDANG-RENDAH] `belum_ada_uang` salah tolak uang masuk** yang menyebut bayar/terima/pembayaran + ngebon/tempo, dan tidak bisa dilewati dengan kategori eksplisit. Saran: arah masuk + bayar/terima/pembayaran/lunas → jangan tolak; atau izinkan kategori eksplisit dengan peringatan.
3. **[RENDAH]** Negasi ("tanpa denda", "bebas bunga") ditolak sebagai gabungan.
4. **[RENDAH]** Pesan penolakan berbahasa teknis (flag CLI, kapital); tambahkan contoh kalimat tanya awam di SKILL.md atau field `pertanyaan`.
5. **[RENDAH]** Ekspor emkm tidak mengingatkan bahwa pembelian alat/aset (rak, mesin) dapat dikapitalisasi emkm sehingga laba ≠ hasil usaha; "belanja dapur" + `lain-lain` tanpa peringatan; kosakata tebakan usaha laundry/jasa sempit.

### Skor: **7,5/10** (layak lanjut; perbaiki temuan 1–2 di v1.0.6)
Alasan: ketujuh perbaikan v1.0.4 bekerja pada frasa baru di jalur catat, impor, dan ekspor; semua angka tepat ke rupiah (0 mismatch), neraca seimbang, invarian laba = hasil usaha terjaga (selisih satu-satunya = kapitalisasi aset yang benar), tanpa regresi, dan penolakan jarang salah pada entri normal (1/41). Belum naik karena perbaikan prioritas utama (pokok + bunga satu baris) masih lolos diam-diam lewat bentuk bahasa sehari-hari yang sangat umum ("plus dendanya", "KUR termasuk bunga") dengan dampak Rp 1 jt pada data uji, dan uang masuk dari pelanggan "yang kemarin ngebon" tidak bisa dicatat tanpa mengubah keterangan; platform asli belum diuji.

## Uji ulang v1.0.6 (2026-09-29)
- **Penguji:** agent independen (bukan pembuat, bukan penguji v1.0.3–v1.0.5); hanya membaca folder skill; salinan skill + `laporan-keuangan-emkm` di scratchpad `uji-kas-106`, Linux, Python 3.11, data fiktif; simulasi agent `claude-code`.
- **Tes regresi:** `tests/uji_regresi.py` **90/90 OK** (1 dilewati: kasir-lokal tidak ada di sebelahnya); `laporan-keuangan-emkm/scripts/uji_regresi.py` **SEMUA UJI LULUS**; `validate.py --skill kas-umkm` ✅.
- **Data baru:** toko roti fiktif "Roti Mbak Tari", September 2026, **55 baris** (45 frasa `catat` → 50 catatan setelah dipisah + 10 baris impor mutasi BNI) + 3 `pindah` (tarik BNI→laci, setor laci→BNI, tarik ATM bersama + biaya Rp 6.500). Akun: Laci 1 jt, BNI 10 jt (QRIS); utang bank awal 25 jt. Setiap frasa dicatat dulu **tanpa kategori**, lalu dengan jawaban "pengguna" + `--ya`. Frasa jebakan: setor cicilan oven plus bunganya, bayar KUR Mandiri sudah termasuk bunga, angsuran koperasi + adminnya, cicilan ke-6 tanpa denda, bunga 0% cicilan mixer, Bu Sri bayar roti yang kemarin ngebon, terima pelunasan pesanan tempo 7 hari, belanja dapur, beli tepung, fotokopi nota, ambil ragi & cokelat ngebon di toko bahan kue, lunasi bon toko bahan kue, bayar hutang ke Bu Narti, Pak RT bayar hutang pesanan kue, Dewi pinjam uang, DP beli etalase; impor: SETORAN KREDIT + BUNGA, PEMBAYARAN KUR MANDIRI TERMASUK BUNGA, TRSF DARI SRI WAHYUNI BYR ROTI YG NGEBON, TRSF BYR BON TOKO BAHAN KUE, TARIK TUNAI ATM, BIAYA TARIK TUNAI, BUNGA, PAJAK BUNGA, BIAYA ADM. Probe tambahan 53 frasa (tidak disimpan).

| Perbaikan v1.0.6 (temuan v1.0.5) | Hasil |
|---|---|
| 1 pokok + bunga/denda (-nya, KUR/kredit/koperasi/leasing/utang bank) | ✅ semua frasa data + probe ditolak `gabungan_pokok_denda`, juga dengan `--kategori pinjaman`: "plus bunganya", "termasuk bunga", "+ adminnya", "plus dendanya", "sama bunganya", "setoran KUR + bunga", "bayar leasing termasuk denda", "bayar utang bank + bunganya", "berikut bunganya", "(pokok+bunga)", "plus biaya administrasinya", "tanpa denda tapi plus bunga". Impor "SETORAN KREDIT + BUNGA", "PEMBAYARAN KUR MANDIRI TERMASUK BUNGA", "TRSF ANGSURAN KUR PLUS DENDANYA" → Perlu dicek + saran lewati & dua baris. Negasi diterima: "tanpa denda", "tidak ada denda", "bebas bunga", "bunga 0%", "0 persen", "tidak kena denda", "tanpa bunga dan tanpa denda", "tanpa biaya admin"; impor "ANGSURAN KREDIT BEBAS BUNGA" → pinjaman. ❌ kecil: "(denda nihil)", "dendanya dihapus" masih ditolak (lihat temuan 1). |
| 2 uang masuk bayar/terima + ngebon/tempo | ✅ "Bu Sri bayar roti yang kemarin ngebon", "terima pelunasan pesanan tempo 7 hari", "Bu Sri lunasi bon roti", "bayaran pesanan yang ngebon minggu lalu" → penjualan (ditebak). Masuk tanpa kata bayar ("pesanan kue Bu Ani tempo 14 hari", "pelanggan ngebon roti") tanpa kategori → ditanya dengan kalimat awam; dengan `--kategori penjualan` → diterima + peringatan "pastikan uangnya BENAR-BENAR sudah diterima". Keluar ngebon/tempo/belum dibayar tetap ditolak walau `--kategori beli-stok`; pelunasan bon/tempo keluar dan "DP oven, sisanya tempo" tidak salah tolak. |
| 3 belanja dapur + lain-lain → peringatan | ✅ peringatan "untuk rumah atau untuk usaha?"; "belanja dapur rumah" → prive. |
| 4 `pertanyaan` bahasa awam | ✅ ada di setiap penolakan (catat, `--kategori`, impor `perlu_dicek`), tanpa flag/kode/huruf kapital, sopan, menyebut nominal & keterangan, menawarkan tindakan ("Nanti saya catat terpisah: cicilan pokoknya (mengurangi utang) dan bunganya (biaya usaha)."). Mode teks menampilkan "Pertanyaan untuk pengguna:". |
| 5 ekspor: catatan kapitalisasi aset | ✅ ekspor emkm menyebut "DP beli etalase kue baru Rp 700.000 … dapat digolongkan ASET TETAP … laba bisa lebih besar … paling banyak Rp 700.000. Itu benar menurut SAK EMKM"; tebakan jasa baru: fotokopi, parkir, ongkir, servis → lain-lain, plastik → beli-stok, pesanan → penjualan. |

**Angka (Decimal penguji dari daftar transaksi penguji, 59 catatan non-pindah):** masuk 19.258.210, keluar 16.147.142, saldo Laci 4.165.000 / BNI 9.946.068 = **14.111.068**, **hasil usaha 3.611.068**, penjualan 12.105.000, prive 800.000, kasbon sisa 300.000, pinjaman diterima 5.000.000, pokok dibayar 6.400.000, utang akhir 23.600.000 — **semua cocok** `rekap`/ekspor/emkm; opname laci Rp 4.165.000 **PAS**. **Mismatch angka: 0.**
**Emkm** (`--utang-bank-awal 25000000`): neraca **seimbang** (Rp 15.111.068), kas 14.111.068, utang bank 23.600.000, kasbon 300.000, beban PPh 180.000 + 642 ✅. **Laba emkm 4.311.068 = hasil usaha 3.611.068 + 700.000**: selisih tepat = "DP beli etalase" yang dikapitalisasi emkm sebagai aset tetap (benar menurut SAK EMKM, penyusutan belum diisi) dan sudah diperingatkan di teks ekspor. Dengan baris itu `beban_lain`: laba **3.611.068 = hasil usaha**, neraca seimbang (14.411.068). Invarian terjaga.
**Regresi:** tarik tunai ATM (impor) → pindah dana ✅; BIAYA TARIK TUNAI, BIAYA ADM, `pindah --biaya` → `beban_keuangan` ✅; utang pemasok ("lunasi bon toko bahan kue", impor "TRSF BYR BON TOKO BAHAN KUE") → `utang_pemasok`/Perlu dicek → `pembelian_bahan` ✅; "bayar hutang ke Bu Narti" / "Bu Narti bayar hutang" → `utang_ambigu` ✅; "Pak RT bayar hutang pesanan kue" → penjualan ✅; kasbon ("kasbon Dewi", "Dewi pinjam uang", kembali) & sisa di neraca ✅; peringatan prive ✅; 'Perlu dicek' memblokir ekspor emkm ✅; ngebon keluar ditolak ✅; Aturan 7 (pembukuan ganda) utuh + dites ✅. **Tanpa regresi.**

**Penolakan salah:** dari 39 frasa normal di data, kode penolakan baru (gabungan/belum_ada_uang/utang_ambigu/utang_pemasok) muncul pada **0**; keenam jebakan yang memang harus ditanya (3 gabungan, 1 ngebon keluar, 1 utang pemasok, 1 utang ambigu) semuanya ditolak dengan `pertanyaan` yang tepat. Di probe: 2 negasi jarang ("denda nihil", "dendanya dihapus") ditolak. Terpisah, **7/39** frasa normal tanpa kategori dijawab "kategori belum jelas" (bukan blokir; agent cukup bertanya sekali): beli tepung (×2), beli gula dan mentega, beli telur, beli tepung dan ragi, gas elpiji, DP beli etalase; probe: beli terigu/mentega/ragi, isi ulang gas elpiji.

Temuan (berprioritas):
1. **[RENDAH]** Negasi berbentuk "denda nihil" / "dendanya dihapus" masih ditolak `gabungan_pokok_denda` walau `--kategori pinjaman` (hanya bisa lewat dengan mengubah keterangan). Jarang; aman (tidak diam-diam salah).
2. **[RENDAH]** Kosakata tebakan bahan usaha makanan sempit: "beli tepung/terigu/gula/mentega/telur/ragi", "gas elpiji" tidak ditebak `beli-stok`, sehingga pemilik toko roti/warung ditanya berulang tiap hari. Saran: "beli <bahan pangan umum>" → `beli-stok` (tetap "ditebak").
3. **[RENDAH]** Catatan `lain-lain` yang sudah dikonfirmasi pengguna (mis. "belanja dapur" setelah peringatan, "gas elpiji") diekspor dengan kategori kosong; emkm memasukkan "belanja dapur" ke "BELUM TERKLASIFIKASI" dan menandai laporan SEMENTARA (laba tidak berubah). Saran: ekspor `beban_lain` bila kategori `lain-lain` dipilih eksplisit.
4. **[INFO]** Uang masuk impor "TRSF DARI … BYR ROTI YG NGEBON" ditanyakan (tidak ditebak penjualan) — aman.

### Skor: **8,5/10** (lulus; temuan 1–3 opsional untuk v1.0.7)
Alasan: kelima perbaikan v1.0.6 terbukti pada data baru di jalur catat, `--kategori`, impor, dan ekspor; semua angka tepat ke rupiah (0 mismatch), neraca emkm seimbang, invarian laba = hasil usaha terjaga (selisih satu-satunya = kapitalisasi aset yang kini diperingatkan), tanpa regresi, 0 penolakan salah dari aturan baru pada entri normal, dan pertanyaan penolakan kini siap kirim ke pengguna awam. Sisa temuan hanya kenyamanan (tebakan bahan makanan, negasi langka, ekspor lain-lain kosong); platform asli belum diuji.
