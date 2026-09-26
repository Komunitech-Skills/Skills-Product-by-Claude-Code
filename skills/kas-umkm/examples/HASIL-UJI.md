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
