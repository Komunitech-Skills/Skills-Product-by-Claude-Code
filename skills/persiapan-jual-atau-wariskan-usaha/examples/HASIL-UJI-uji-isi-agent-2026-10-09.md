# HASIL UJI: persiapan-jual-atau-wariskan-usaha 1.0.0

- Tanggal: 2026-10-09
- Penguji: agent independen (bukan pembuat), hanya membaca salinan folder skill di scratchpad.
- Jenis uji: **uji isi oleh agent** (`claude-code (simulasi agent)`). Router model OpenClaw mati (HTTP 530), jadi **uji OpenClaw sebelum/sesudah belum dilakukan** dan `00-openclaw-sebelum-sesudah.md` belum ada.
- Berkas `examples/` dari uji sebelumnya yang terputus (`00-pembanding-tanpa-skill.md` parsial) **tidak dipakai sebagai hasil dan telah ditimpa**; uji dimulai dari nol.
- Uji banding pesaing (Tahap 6.5) tidak termasuk tugas uji ini; belum dilakukan.

## VERDIK: **BELUM** · Skor kualitas: **7/10**

Alasan utama: ada **kesalahan angka** yang dibawa rumus skill (biaya sekali jalan ditambahkan ke semua tahun), dan selisih A/B hanya +0,5 (syarat ≥ 1,5). Struktur, batasan, dan perilaku tolak sudah baik; bila cacat T1 dan S1 diperbaiki, skill ini realistis mencapai ≥ 8.

## Tabel skor

| # | Skenario | Tanpa skill | Dengan skill | Catatan |
|---|---|---|---|---|
| 1 | Jual warung bakso (Klaten) | 6,0 | 6,5 | Struktur jauh lebih baik, tetapi batas atas nilai terlalu tinggi Rp28 juta (cacat T1) |
| 2 | Wariskan toko bangunan ke sulung | – | 7,5 | Angka benar; menolak menetapkan bagian waris; harta bersama hanya dari inisiatif agent |
| 3 | Beli bagian sekutu CV 40% | – | 7,0 | Angka benar; tidak ada panduan porsi/utang badan usaha, improvisasi agent |
| 4 | Input tidak lengkap | – | 8,5 | Kerja dulu, tidak mengarang angka, 3 pertanyaan |
| 5 | Di luar cakupan (wasiat, 2:1, pajak, jaminan harga) | – | 8,5 | Tolak → padanan → tetap kerjakan |
| | **Rata-rata sesudah** | | **7,6** | Selisih A/B (skenario 1): **+0,5** |

## Uji script

- `tests/uji_regresi.py`: **9/9 lulus**.
- Data rusak ditolak rapi (kode 2, pesan "GAGAL"): `150.000.000`, `150jt`, `10%`, tahun 2 digit, `inf`, `nan`, bulan negatif, kelipatan 0/negatif, `--kebutuhan-bulanan` tanpa `--bulan`, tanpa laba & aset.
- Semua angka di skenario 1-3 dihitung ulang independen dengan `decimal.Decimal` dan **cocok dengan keluaran script**; cacatnya ada di rumus/desain, bukan di aritmetika.
- Audit keamanan: hanya pustaka standar, tanpa jaringan, tanpa baca/tulis file, tanpa eval/exec/subprocess. Aman.

## Cacat

### Tinggi
**T1. `--biaya-sekali` ditambahkan ke setiap tahun, bukan ke tahun kejadiannya → nilai usaha terlalu tinggi.**
SKILL.md menulis "laba normalisasi per tahun = laba + gaji diambil - gaji pengganti + biaya sekali jalan" dan opsi hanya menerima satu angka.
Reproduksi: `python3 scripts/nilai_usaha.py --laba 2023=84000000 2024=97000000 2025=91000000 --kelipatan 2 3 --gaji-diambil 36000000 --gaji-pengganti 42000000 --biaya-sekali 12000000 --diskon-pemilik 20` → laba disesuaikan 90/103/97 juta, basis Rp96.666.667, rentang s/d **Rp232.000.000**. Yang benar (renovasi hanya 2024): 78/103/85 juta, basis Rp85.000.000 (tahun terakhir lebih rendah), rentang s/d **Rp204.000.000**. Selisih Rp28.000.000 dan peringatan "laba tahun terakhir turun" hilang. Perbaikan: terima `--biaya-sekali 2024=12000000` (per tahun), dan ubah rumus di SKILL.md.

### Sedang
**S1. Utang diperlakukan tidak konsisten.** Metode aset bersih mengurangi utang, metode kelipatan laba tidak; lalu keduanya digabung jadi satu rentang, dan "selisih vs kebutuhan hidup" memakai nilai yang belum dikurangi utang yang masih harus dilunasi pemilik (skenario 1: tampil s/d Rp114.720.000, padahal bila utang koperasi Rp18 juta dilunasi dari hasil jual sisa Rp96.720.000). Perbaikan: beri peringatan/pilihan "utang dilunasi dari hasil jual" dan tampilkan hasil bersih ke pemilik setelah utang.
**S2. Tidak ada dasar aturan untuk domain hukum/pajak** (pedoman kurasi Komunitech tahap 4.5 mewajibkan dasar aturan + tanggal berlaku). Skill hanya menulis "tanggal acuan Oktober 2026" tanpa satu pun rujukan. Tidak perlu menghitung pajak, tetapi daftar pertanyaan sebaiknya menyebut dasar yang sudah dicek (lihat Cek fakta di bawah) agar pengguna tahu apa yang ditanyakan.
**S3. Daftar pertanyaan profesional kurang butir penting:** persetujuan pasangan untuk harta bersama; hukum waris yang berlaku (KUH Perdata/KHI/adat) dan bagian mutlak ahli waris/batas hibah; pekerja tidak otomatis berhenti saat usaha dijual/diwariskan (hak pekerja beralih); PPh final 2,5% penjualan tanah/bangunan & SKB untuk waris; PPN Pasal 16D bila pemilik PKP; akta perubahan CV/persetujuan pemegang saham PT.
**S4. Jalur "serahkan ke mitra/sekutu" tidak didukung** padahal disebut di description: tidak ada langkah untuk porsi kepemilikan, utang badan usaha, dan siapa menanggung biaya; script tidak punya opsi porsi.

### Rendah
**R1.** Biaya transaksi dikalikan ke nilai aset bersih negatif sehingga negatif "membaik": `--aset 10000000 --utang 30000000 --biaya-transaksi 10` → -Rp20.000.000 menjadi -Rp18.000.000.
**R2.** Laba normalisasi negatif tanpa aset → hanya "GAGAL: tidak ada metode yang bisa dihitung"; peringatan "laba nol/negatif" yang lebih jelas hilang (`--laba 2025=1000000 --kelipatan 2 --gaji-pengganti 5000000`).
**R3.** Angka sangat besar memicu traceback, bukan "GAGAL" (`--aset 1e400`, kode 1).
**R4.** "Rentang gabungan" mencampur nilai jual-alat-saja dengan nilai usaha berjalan sehingga sangat lebar (skenario 1: Rp30,75 juta s/d Rp232 juta); lebih jelas bila aset bersih ditampilkan sebagai "batas bawah" terpisah.
**R5.** Frasa "pengalihan NIB" di references bisa menyesatkan: NIB usaha perorangan terikat NIK pemilik; lebih aman "apakah pemilik baru perlu NIB sendiri?" (belum ada sumber resmi yang tegas; PERLU REVIEW).
**R6.** Tahun `0000` diterima sebagai tahun laba.

## Cek fakta hukum/pajak (dicek 2026-10-09)

Skill sengaja tidak menghitung pajak/waris dan tidak memberi pendapat hukum; klaim yang ada (akta oleh notaris/PPAT, pembagian waris mengikuti hukum yang berlaku bagi keluarga, BPHTB untuk tanah/bangunan, PPN "bila relevan") **tidak salah**. Tidak ditemukan klaim keliru; kekurangannya adalah rujukan yang hilang (S2/S3). Fakta yang bisa dipakai pembuat:
- PPh final pengalihan tanah/bangunan 2,5% (PP 34/2016, berlaku 7 Sep 2016); waris tetap objek tetapi bisa dibebaskan dengan SKB: https://setkab.go.id/pp-no-342016-pph-pengalihanjual-beli-tanahbangunan-25-di-bawah-rp-60-juta-dikecualikan/ ; https://news.ddtc.co.id/berita/nasional/1809947/ingat-tanah-dan-bangunan-warisan-tak-ber-skb-tetap-jadi-objek-pajak
- BPHTB: tarif maks 5%, NPOPTKP min Rp80 juta, waris/hibah wasiat keluarga garis lurus satu derajat min Rp300 juta, ditetapkan perda (UU 1/2022 HKPD Pasal 46-47): https://news.ddtc.co.id/berita/nasional/35545/uu-hkpd-revisi-aturan-npoptkp-tanah-danatau-bangunan-ini-rinciannya
- Warisan bukan objek PPh; hibah ke keluarga sedarah garis lurus satu derajat dikecualikan bersyarat (UU PPh Pasal 4 ayat 3): https://news.ddtc.co.id/berita/nasional/1795835/warisan-bebas-pajak-tak-terbatas-hubungan-keluarga-beda-dengan-hibah
- PPN atas penyerahan aktiva yang semula tidak untuk dijual oleh PKP (UU PPN Pasal 16D): https://www.pajak.go.id/id/artikel/jual-aktiva-tetap-tidak-ada-ppn-nya
- Pembatasan pemindahan saham PT menurut anggaran dasar (UU 40/2007 Pasal 57): https://pasal.id/peraturan/uu/uu-no-40-tahun-2007/pasal-57
- Hibah KHI maks 1/3 (Pasal 210), hibah orang tua ke anak dapat diperhitungkan sebagai warisan (Pasal 211); bagian mutlak KUH Perdata Pasal 913-914: https://www.hukumonline.com/klinik/a/perbedaan-hibah-dan-wasiat-menurut-hukum-islam-lt696ee8bb34712 ; https://www.hukumonline.com/klinik/a/wasiat-tertutup-melanggar-legitieme-portie-otomatis-batal-lt67d380451e3d8
- Perjanjian kerja tidak berakhir karena penjualan/pewarisan/hibah usaha; hak pekerja jadi tanggung jawab pengusaha baru (UU 13/2003 Pasal 61 ayat 2-3; pasal PHK terkait telah diubah UU Cipta Kerja, cek naskah terbaru): https://www.hukumonline.com/klinik/a/status-karyawan-kontrak-jika-terjadi-pengalihan-perusahaan-lt5bd0098910a88/
- Catatan: sebagian sumber di atas adalah media pajak/hukum, bukan naskah resmi; sebelum dipakai di skill, cocokkan dengan JDIH/peraturan.go.id.

## Kepatuhan
- Disclaimer "bukan nasihat hukum/pajak/penilaian resmi" + arahan ke notaris/konsultan pajak/penilai: **ada**.
- Tidak menetapkan bagian waris, tidak membuat akta/wasiat, tidak menjamin harga: **patuh** (skenario 2 & 5).
- Tidak menyimpan data pribadi; daftar pelanggan tanpa kontak sebelum calon serius: **patuh**.
- Frontmatter hanya `name` & `description`: **patuh**.
- README "Contoh sebelum/sesudah" masih "Akan diisi dari hasil uji" (wajar untuk draft).

## Saran perbaikan (urut dampak)
1. Perbaiki T1: biaya sekali jalan per tahun (`2024=12000000`), sesuaikan rumus di SKILL.md, tambah tes.
2. Perbaiki S1: tampilkan "hasil bersih ke pemilik setelah utang & biaya" dan pakai itu untuk perbandingan kebutuhan hidup.
3. Lengkapi `references/pertanyaan-profesional.md` dengan butir S3 + dasar aturan & tanggal (S2), tetap sebagai pertanyaan, bukan jawaban.
4. Tambah bagian singkat jalur "beli/keluar sekutu" (porsi, utang badan usaha, biaya) dan opsi `--porsi` di script (S4).
5. Rapikan R1-R3 (negatif × biaya, pesan laba negatif, angka ekstrem).

## PERLU REVIEW
- Dasar aturan waris/pajak yang akan ditambahkan perlu dicek ahli (notaris/konsultan pajak) sebelum rilis.
- Status pengalihan NIB usaha perorangan (R5): belum ada sumber resmi yang tegas.
- Uji OpenClaw sebelum/sesudah (+ konteks Telegram) wajib dijalankan setelah router pulih; skor di atas adalah simulasi satu penguji (bias: penulis & penilai sama).
