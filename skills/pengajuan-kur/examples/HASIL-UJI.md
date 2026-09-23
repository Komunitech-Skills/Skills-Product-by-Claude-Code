# HASIL UJI — pengajuan-kur

- **Tanggal:** 2026-09-23
- **Penguji:** agent penguji independen (simulasi, Claude Code)
- **Folder kerja uji:** `/tmp/uji-pengajuan-kur/`
- **Script dijalankan:** ya (5 skenario + data tepi: "Rp 1.500.000,50", plafon 0, tenor 0, laba 0/negatif, bunga "0,5%/bulan", "6 persen", "5 persen", plafon > Rp500 jt, akad ke-3 dagang, rincian salah format/tidak sama plafon, bunga 0, biaya rumah tangga, CSV jadwal)
- **Verifikasi angka independen:** ya — `verif.py` (rumus float terpisah, tanpa kode skill): anuitas, flat, total bunga, efektif setara flat (bisection sendiri), flat setara acuan, rasio, plafon maks — 6 kasus, semuanya cocok ke rupiah.
- **Cek fakta regulasi:** teks lengkap Permenko Perekonomian 1/2026 dibaca dari DDTC (Pasal 1, 13, 14, 19–21, 24, 27–45). Situs ekon.go.id (siaran pers) **diblokir proxy** saat pengujian — tidak diverifikasi.

## Hasil cek fakta `references/regulasi.md` vs teks Permenko 1/2026
| Klaim | Hasil |
|---|---|
| Plafon SM ≤10 jt / Mikro >10–100 jt / Kecil >100–500 jt (Ps 29, 36, 43) | ✅ Benar |
| Bunga SM 3%; Mikro produksi/ekspor 6%, dagang 6%/7% maks 2 akad; Kecil dagang 6/7/8/9% (Ps 30, 36(3), 37, 44(1)) | ✅ Benar |
| "flat/anuitas yang setara menyesuaikan" | ✅ Benar (kutipan tepat) |
| Tenor SM & Mikro 3 th MK / 5 th inv; Kecil 4/5; perpanjangan SM 4/7, Mikro & Kecil 5/7 (Ps 31, 38, 45) | ✅ Benar |
| Agunan tambahan dilarang s.d. Rp100 jt (Ps 20(1)), sanksi subsidi (Ps 21), KI sbg agunan (Ps 19) | ✅ Benar |
| Nilai cair = nilai akad (Ps 13(2)); SLIK & surat lunas/roya (Ps 14) | ✅ Benar |
| Syarat: ≥6 bln, NIB/SKU, NIK, NPWP Mikro >50 jt & Kecil wajib, belum pernah kredit komersial + pengecualian (Ps 27, 34, 41) | ✅ Benar |
| Sektor produksi = di luar perdagangan (Ps 1 angka 2) | ✅ Benar |
| "provisi" tidak ada di teks | ✅ Benar (dicari, 0 hasil) |
| Graduasi dari **KUR Mikro** ke Kecil (Ps 44(3)–(4): +1% dari bunga Mikro terakhir, naik 1%/akad, maks 9%) | ❌ **Tidak dimuat** (hanya graduasi dari Super Mikro) |
| Syarat "belum pernah menerima KUR dengan plafon di atas plafon jenis ini" (Ps 27(1)d, 34(1)e) | ➖ Tidak dimuat |

## Skor
| Kriteria | Skor (1–10) | Catatan |
|---|---:|---|
| Pemicu (description tepat) | 9 | Spesifik, sebut bank penyalur, EN/ID, batas pinjol & arus kas |
| Kemudahan awam | 9 | Penjelasan flat vs efektif dengan angka, emoji kategori, `[isi: …]` |
| Kualitas output | 9 | Paket lengkap (simulasi, rasio, rencana dana, profil, checklist, langkah) |
| Akurasi (angka/fakta) | 8 | Semua angka tepat; fakta regulasi benar; celah graduasi Mikro→Kecil & parsing "persen" |
| Penanganan input kurang | 9 | Bertanya sekali, 5 pertanyaan; mode "simulasi saja" |
| Penanganan di luar cakupan | 9 | Tolak pemalsuan/jaminan/calo; pinjol diarahkan ke OJK |
| Keamanan | 10 | Tanpa jaringan/subprocess; hanya tulis `--output-csv`; tidak minta data sensitif |
| **SKOR AKHIR** | **8** | |

**Status: LULUS** (dengan perbaikan sedang disarankan)

## Cacat
### Berat
- Tidak ada.

### Sedang
1. **Kata "persen" dianggap "per bulan"** (`scripts/simulasi_kur.py` baris 252: regex `(/|per|...)` cocok dengan "**per**sen"). `--bunga "5 persen"` → **60%/tahun** diterima dengan peringatan "diisi PER BULAN"; `"6 persen"` → 72% → error. Agent yang meneruskan teks pengguna apa adanya akan mendapat simulasi salah total. **Saran:** buang kata "persen/%" sebelum deteksi, dan gunakan `\bper\s*(bulan|bln)\b|/\s*(bulan|bln)|sebulan|tiap bulan`.
2. **Graduasi KUR Mikro → KUR Kecil sektor perdagangan tidak diatur** (`references/regulasi.md` "Catatan pasal" & `bunga_acuan_kur` baris 158–173). Pasal 44(3)(b)–(4): bunga KUR Kecil pertama = bunga Mikro terakhir + 1%, naik 1%/akad, maks 9%. Contoh: pernah 2× KUR Mikro dagang (6%, 7%) → KUR Kecil pertama seharusnya 8%, script `--akad-ke 1` memberi 6%. **Saran:** tambah butir di regulasi.md dan argumen `--bunga-mikro-terakhir` (atau pertanyaan "KUR sebelumnya jenis apa & bunganya berapa?") di SKILL.md bagian Input.
3. **Penggunaan campuran investasi + modal kerja** tidak didukung (`--penggunaan` satu nilai; S1: alat 70 jt + stok 30 jt, tenor 60 bulan lolos cek padahal porsi modal kerja maks 36 bulan). **Saran:** di `--rincian-dana` izinkan penanda `[inv]`/`[mk]` per pos dan beri `perhatian` bila tenor > batas modal kerja untuk porsi MK; minimal tambah kalimat di SKILL.md langkah 6.

### Ringan
4. Laba negatif `--laba-bersih -2jt` ditolak argparse (harus `--laba-bersih=-2jt`); tulis di SKILL.md atau terima "minus 2jt".
5. `plafon_maks = 0` (cicilan lain sudah ≥ 30% laba) tanpa penjelasan; tambahkan `catatan` "cicilan lain sudah menghabiskan batas aman" dan skenario "tanpa cicilan lain".
6. Saat bunga dari bank kemungkinan **flat**, kategori rasio yang menonjol tetap dari anuitas; tambahkan flag `--bunga-flat` agar rasio utama memakai metode yang ditawarkan.
7. regulasi.md belum memuat syarat Ps 27(1)d/34(1)e (belum pernah KUR di atas plafon jenis tsb) dan Ps 28(2)/35(2) (kredit program pemerintah lain yang sudah lunas tetap boleh).
8. KUR Kecil dagang akad ≥ 5: pesan "tidak diatur — tanyakan bank" (wajar), bisa ditambah bahwa Ps 44(4) membatasi maks 9%.
9. SKILL.md "Kapan TIDAK digunakan": tambahkan eksplisit "membuat/menggelembungkan laporan keuangan untuk pengajuan" (S5 ditangani baik, tetapi hanya tersirat).

## Yang sudah bagus
- Rumus anuitas/flat, pembulatan dengan selisih di cicilan terakhir, total pokok = plafon (`cek_total_pokok_sama_plafon`), efektif setara flat, flat setara acuan — semuanya tepat.
- Tidak pernah menjanjikan persetujuan: disclaimer di script & template, aturan di regulasi.md no. 4, checklist.
- Rasio & peringatan (🟢 ≤30 / 🟡 30–50 / 🔴 >50 / ⛔ ≥100) plus plafon maks aman; laba nol/negatif ditangani.
- Error input jelas (plafon 0, tenor 0, > Rp500 jt, akad ke-3 dagang, rincian salah format, bunga > 60%).
- Uji A/B: jauh lebih baik dari agent tanpa skill (yang memakai flat, klaim agunan > Rp50 jt, narasi karangan). Banding pesaing: menang atas `loan-comparison` (FerroxLabs, Apache-2.0).
