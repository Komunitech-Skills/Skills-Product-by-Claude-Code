# Catatan pembuat v1.0.1 (2026-10-10)

Berdasarkan `examples/HASIL-UJI-uji-isi-agent-2026-10-09.md`. Ini catatan pembuat, **bukan uji independen**; v1.0.1 perlu diuji ulang oleh penguji terpisah (termasuk OpenClaw sebelum/sesudah + konteks Telegram). Berkas uji milik penguji (`HASIL-UJI*.md`, `00-*`, `01`-`05`) tidak diubah; angka di contoh lama ditulis dengan v1.0.0 dan bisa berbeda bila dijalankan ulang.

## T1 (TINGGI): biaya sekali jalan ditambahkan ke semua tahun

**Reproduksi di v1.0.0** (salinan script lama, data warung bakso penguji, `--biaya-sekali 12000000`):
laba disesuaikan 90/103/97 juta, basis Rp96.666.667, nilai s/d **Rp232.000.000**, selisih vs kebutuhan s/d Rp114.720.000, tanpa peringatan "laba tahun terakhir lebih rendah".

**Desain baru:** `--biaya-sekali TAHUN=JUMLAH`, boleh beberapa dan boleh mengulang opsi (tahun yang sama dijumlahkan). Hanya ditambahkan ke tahun itu. Angka **tanpa tahun** hanya diterima bila `--laba` berisi tepat satu tahun (tidak ada ambiguitas); bila lebih dari satu tahun, ditolak dengan pesan "harus disertai tahun kejadiannya, mis. --biaya-sekali 2024=12000000". Pilihan ini dianggap paling tidak mengejutkan: menebak tahun (mis. tahun terakhir) atau menyebar ke semua tahun sama-sama bisa salah diam-diam. Tahun yang tidak ada di `--laba` ditolak; tahun di luar 3 tahun terakhir diberi peringatan "tidak dipakai".

**Hasil v1.0.1** (`--biaya-sekali 2024=12000000`): 78/103/85 juta, rata-rata Rp88.666.667, basis Rp85.000.000 (tahun terakhir lebih rendah, peringatan muncul), nilai usaha Rp136.000.000 s/d Rp204.000.000. Batas atas turun Rp28.000.000, sama dengan temuan penguji.

**Verifikasi independen** (skrip `decimal` terpisah di scratchpad, tidak mengimpor `nilai_usaha.py`): norm 78.000.000/103.000.000/85.000.000; basis 85.000.000; 136.000.000-204.000.000; setelah biaya 4% 130.560.000-195.840.000; dikurangi utang Rp18.000.000 = 112.560.000-177.840.000; vs kebutuhan Rp108.000.000 = 4.560.000-69.840.000. Selisih batas atas lama vs baru = 28.000.000. Semua cocok dengan keluaran script. Perhitungan yang sama juga ditulis di tes `test_t1_biaya_sekali_hanya_tahunnya`.

## SEDANG

| ID | Perbaikan | Bukti |
|---|---|---|
| S1 utang | Kedua metode kini **sebelum utang** (kelipatan laba = nilai usaha berjalan; aset = nilai aset setelah penyesuaian, ditampilkan sebagai batas bawah bila hanya aset dijual, menjawab R4). Utang dikurangkan **sekali**: bawaan "dilunasi pemilik dari hasil jual" (harga tetap, hasil bersih berkurang) atau `--utang-ikut` (utang ikut pembeli/tetap di badan usaha: harga = (nilai - utang) x porsi). Baris baru "Hasil bersih ke pemilik (setelah biaya dan utang yang dilunasi)" dan perbandingan kebutuhan hidup memakai angka ini. "Aset dikurangi utang" tetap ditampilkan sebagai gambaran tutup usaha. | Warung bakso: hasil bersih Rp112.560.000-177.840.000 (bukan s/d Rp222.720.000 tanpa utang). Bu Sri (data OpenClaw penguji): v1.0.0 selisih vs kebutuhan -Rp95.100.000 s/d Rp59.940.000; v1.0.1 -Rp69.040.000 s/d Rp14.940.000 (batas atas kini sudah dikurangi KUR Rp45.000.000; batas bawah tidak lagi memakai aset-minus-utang). Dicek ulang dengan `decimal`. Tes `test_s1_utang_sekali_di_kedua_metode`. |
| S2 dasar aturan | `references/dasar-aturan.md` baru: 12 baris, tiap baris berisi dasar aturan, tanggal/versi, isi singkat, URL, dan **status cek** (Resmi / Sekunder / Belum terverifikasi). SKILL.md menyuruh agent hanya memakai aturan dari berkas ini sebagai bahan bertanya. | Resmi (dibuka 10-10-2026): Setkab tentang PP 34/2016; Keterangan Tertulis DJP KT-16/2025 (PMK 81/2024 Pasal 200, SKB waris, PER-8/PJ/2025 Pasal 101(5)c, BPHTB tetap berlaku, UU 1/2022); artikel pajak.go.id tentang Pasal 16D (opini pegawai DJP). Sekunder: UU PPh Pasal 4(1)d, UU 1/1974 Pasal 36, KUH Perdata 913-914, KHI 210-211, UU 13/2003 Pasal 61, UU 40/2007 Pasal 57. Belum terverifikasi: Permenkumham 17/2018 & status layanan CV 2024; NIB perorangan. peraturan.bpk.go.id menolak akses (403), peraturan.go.id 503, PDF JDIH Kemenkeu berupa pindaian. |
| S3 pertanyaan | `references/pertanyaan-profesional.md` ditambah: persetujuan pasangan (harta bersama), bagian mutlak/hak ahli waris lain (legitieme portie, batas hibah KHI), karyawan PKWT/PKWTT dan hak yang beralih, SKB PPh untuk tanah/bangunan warisan, PPN Pasal 16D bila PKP, akta perubahan CV/firma, anggaran dasar PT, jaminan pribadi atas utang. Tiap butir merujuk nomor di `dasar-aturan.md`. | Tetap berupa pertanyaan, bukan jawaban; tanpa tarif/angka pajak. |
| S4 sekutu | SKILL.md langkah 5a (porsi dari akta, utang badan usaha tetap di usaha, siapa menanggung biaya, cara bayar, jaminan pribadi, bagian minoritas, akta notaris, anggaran dasar PT); script `--porsi`. Bila porsi < 100 dan ada utang, script otomatis memakai mode utang-ikut dan memberi peringatan. | Data CV penguji (contoh 03) + `--porsi 40`: nilai 100% Rp534.000.000-667.500.000; harga bagian 40% Rp189.600.000-243.000.000; setelah biaya 3% Rp183.912.000-235.710.000. Dicek ulang dengan `decimal`. Tes `test_s4_porsi_sekutu`. |

## RENDAH
| ID | Perbaikan |
|---|---|
| R1 | Biaya transaksi dihitung dari `max(harga, 0)`; harga negatif tidak lagi "membaik" (tes `test_r1_biaya_tidak_dari_negatif`). Aset dikurangi utang tidak lagi dikalikan biaya transaksi. |
| R2 | Laba setelah penyesuaian nol/negatif tanpa aset: pesan "laba setelah penyesuaian nol/negatif (basis -Rp4.000.000) dan aset tidak diisi ... isi --aset atau benahi laba dulu". |
| R3 | Angka di atas Rp1.000 triliun ditolak dengan "GAGAL ... cek salah ketik"; galat aritmetika lain juga ditangkap (kode 2, bukan traceback). |
| R4 | Lihat S1: nilai aset ditampilkan terpisah sebagai batas bawah; rentang nilai usaha tidak lagi mencampur aset-minus-utang dengan kelipatan laba. Peringatan bila nilai aset di atas batas bawah kelipatan. |
| R5 | "Pengalihan NIB" diganti "apakah penerus/pembeli perlu NIB sendiri" (SKILL.md, pertanyaan notaris); ditandai Belum terverifikasi/PERLU REVIEW. |
| R6 | Tahun harus 1900-2100. |

## Tes
`python3 tests/uji_regresi.py`: **15 tes OK** (9 lama + 6 baru). Dua tes lama menyandi perilaku yang justru cacat dan disesuaikan seminimal mungkin:
- `test_kelipatan_manual`: argumen `--biaya-sekali 10000000` (tanpa tahun, 3 tahun laba) kini ditolak; diganti `2023=10000000 2024=10000000 2025=10000000` sehingga angka harapan (basis Rp136.000.000, rentang Rp272.000.000-408.000.000) **tidak berubah**.
- `test_aset_dan_gabungan`: `selisih_vs_kebutuhan` [-34.500.000, 51.000.000] mengabaikan utang Rp80.000.000 (cacat S1); kini [-114.500.000, -29.000.000] dan ditambah cek `hasil_bersih_pemilik` [5.500.000, 91.000.000]. Asersi lain (aset bersih, metode, rentang bruto/bersih) tetap sama.

`python3 scripts/validate.py --skill persiapan-jual-atau-wariskan-usaha`: valid (description 1.023 karakter, mendekati batas 1.024).

## PERLU REVIEW
- Semua baris "Sekunder"/"Belum terverifikasi" di `references/dasar-aturan.md` dicocokkan ke naskah resmi oleh notaris/konsultan pajak.
- Uji independen v1.0.1 + uji OpenClaw/Telegram.
