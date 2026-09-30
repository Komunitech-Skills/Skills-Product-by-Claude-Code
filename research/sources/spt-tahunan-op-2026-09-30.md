# Riset regulasi — skill `spt-tahunan-op` (SPT Tahunan PPh Orang Pribadi)

Dicek: **2026-09-30** oleh agent pembuat. Jalur: **orisinal** (tidak ada materi pihak ketiga yang disalin).
Legenda status: ✅ = diverifikasi (naskah resmi / situs DJP, atau fakta yang sudah terverifikasi resmi di riset repo sebelumnya) · 🟡 = sekunder saja (≥1 sumber non-resmi, konsisten) · ⚠️ PERLU REVIEW = belum dicocokkan dengan naskah resmi / ada ketidakjelasan.

## A. Fakta yang dipakai script `scripts/spt_op.py`

| # | Fakta | Status | Sumber |
|---|---|---|---|
| 1 | Tarif Pasal 17 ayat (1) huruf a (UU 7/2021 HPP), berlaku sejak TP 2022: 5% s.d. Rp60 jt; 15% >60–250 jt; 25% >250–500 jt; 30% >500 jt–5 M; 35% >5 M | ✅ (sudah diverifikasi dari naskah UU di riset `pph21-ter`, 2026-09-23) | UU 7/2021 JDIH Kemenkeu https://jdih.kemenkeu.go.id/api/download/a9faab97-aca7-4f87-9fdc-faa8123d1454/7TAHUN2021UU.pdf ; konsisten https://artikel.pajakku.com/lapisan-pajak-penghasilan-pph-orang-pribadi-pasca-uu-hpp |
| 2 | PTKP setahun: diri Rp54.000.000; kawin +Rp4.500.000; istri yang penghasilannya digabung +Rp54.000.000; tiap tanggungan +Rp4.500.000, maks 3 | ✅ diri/kawin/tanggungan (riset `pph21-ter`, UU HPP Pasal 7 ayat (1)); tambahan istri digabung = UU PPh Pasal 7 ayat (1) huruf c → 🟡 (bunyi pasal tidak dibaca ulang hari ini) | UU 7/2021; PMK 101/PMK.010/2016; https://klikpajak.id/blog/pengertian-ptkp/ |
| 3 | PTKP **tidak berubah** sampai 2026 (terakhir naik lewat PMK 101/2016); wacana kenaikan (usulan Rp7,5 jt/bln, Agustus 2025) belum menjadi aturan | 🟡 (2 sumber sekunder 2025–2026; tidak ada PMK baru ditemukan) | https://pajakku.com/artikel/perkembangan-ptkp-dari-masa-ke-masa-bagaimana-proyeksi-ptkp-2026 ; https://hitunggaji.id/blog/ptkp-2026-tabel-lengkap/ |
| 4 | Status PTKP ditentukan keadaan **awal tahun pajak** | ✅ (PMK 168/2023 Pasal 9, riset `pph21-ter`) | idem |
| 5 | PKP dibulatkan **ke bawah hingga ribuan rupiah penuh** | ✅ (PMK 168/2023 Pasal 8 ayat (3)–(4), riset `pph21-ter`); untuk SPT Tahunan dipakai aturan yang sama → ⚠️ ringan: belum dicocokkan dengan hitungan otomatis Coretax | idem |
| 6 | Biaya jabatan 5% bruto, maks Rp6 jt/tahun (Rp500 rb × bulan) — dipakai hanya untuk helper `--a1-bruto` | ✅ (PMK 168/2023 Pasal 10 ayat (2)) | idem |
| 7 | NPPN: WP OP usaha/pekerjaan bebas dengan peredaran bruto **< Rp4,8 miliar** setahun boleh memakai norma, **wajib memberitahukan DJP paling lama 3 bulan pertama tahun pajak**; tidak memberitahukan → dianggap memilih pembukuan | ✅ situs DJP (6 Feb 2026) — dasar Pasal 463 PMK 81/2024 s.t.d.d. PMK 1/2026; sumber lain menyebut Pasal 450 ayat (2) → nomor pasal ⚠️ PERLU REVIEW | https://www.pajak.go.id/en/node/119175 ; https://muc.co.id/en/article/nppn-determines-the-tax-scheme-for-individual-taxpayers-do-not-miss-the-31-march-reporting-deadline |
| 8 | Klaim DJP: "sekali terlambat/tidak memberitahukan NPPN → **selamanya** wajib pembukuan" | ⚠️ PERLU REVIEW (hanya artikel DJP; belum dicocokkan dengan naskah PMK) — skill menulisnya sebagai peringatan, bukan kepastian | https://www.pajak.go.id/en/node/119175 |
| 9 | Pemberitahuan NPPN di Coretax: menu Layanan Administrasi, kode layanan **AS.04-01** | 🟡 (artikel DJP) | https://www.pajak.go.id/en/node/119175 ; https://www.online-pajak.com/tentang-efaktur-ppn/nppn-coretax |
| 10 | Persentase NPPN diatur **PER-17/PJ/2015** per KLU & wilayah (10 ibu kota provinsi / ibu kota provinsi lainnya / daerah lainnya). Script **tidak** menyimpan tabel; pengguna memasukkan persen dari lampiran. Contoh sekunder: jasa perancangan khusus 32%/31%/29%; dokter 50% | 🟡 contoh (sekunder); tabel penuh ⚠️ PERLU REVIEW → pengguna wajib cek lampiran | https://datacenter.ortax.org/ortax/aturan/show/15783 ; https://klikpajak.id/blog/nppn-pajak/ ; https://pajak.go.id/en/node/37752 |
| 11 | Zakat/sumbangan keagamaan wajib ke BAZNAS/LAZ/lembaga yang dibentuk/disahkan pemerintah = **pengurang penghasilan bruto** (menghitung neto); bukti setor memuat nama & NPWP/NIK, jumlah, tanggal, nama lembaga | 🟡 (DDTC, PP 60/2010, PER-08/PJ/2021 disebut sekunder); naskah PP tidak dibaca hari ini | https://news.ddtc.co.id/berita/nasional/38624/jadi-pengurang-penghasilan-bruto-zakat-perlu-dilaporkan-dalam-spt ; https://pajak.go.id/en/node/105487 |
| 12 | Zakat yang **sudah dipotong lewat pemberi kerja** sudah menjadi pengurang di bukti potong (PMK 168/2023 Pasal 10 ayat (1) huruf c) → jangan dikurangkan dua kali | ✅ (riset `pph21-ter`) | idem |
| 13 | Penghasilan usaha yang dikenai **PPh final 0,5% (PP 55/2022 jo. PP 20/2026)** tidak ikut tarif Pasal 17; dilaporkan di lampiran penghasilan final / rekap peredaran bruto (L-3B), PPh final yang sudah disetor dicantumkan | 🟡 (DJP & Ortax, 2026) | https://www.pajak.go.id/en/node/119105 ; https://www.ortax.org/panduan-mengisi-objek-pph-final-dalam-spt-tahunan-pph-orang-pribadi-coretax |
| 14 | Kredit pajak = PPh 21 (bukti potong A1 pegawai swasta / A2 ASN; bukti potong PPh 21 bukan pegawai), PPh 22, PPh 23, PPh 24, angsuran PPh 25 yang dibayar; PPh final **tidak** dikreditkan | 🟡 (struktur Bagian D Kredit Pajak — Ortax; UU PPh Pasal 28) | https://ortax.org/bentuk-spt-tahunan-pph-orang-pribadi-era-coretax |
| 15 | Angsuran PPh 25 tahun berikutnya = (PPh terutang − PPh 21/22/23/24 yang dipotong/dipungut/dikreditkan) ÷ 12 (UU PPh Pasal 25 ayat (1)); ada di Lampiran 4 Coretax | 🟡 rumus umum UU PPh; penerapan untuk karyawan-saja ⚠️ PERLU REVIEW → script hanya menampilkannya bila ada usaha/pekerjaan bebas | https://ortax.org/bentuk-spt-tahunan-pph-orang-pribadi-era-coretax |
| 16 | Kurang bayar (PPh 29) harus dilunasi **sebelum** SPT disampaikan; di Coretax SPT KB masuk "SPT menunggu pembayaran" dan kode billing dibuat otomatis | ✅ (Coretaxpedia DJP; kalender-pajak #15) | https://pajak.go.id/coretaxpedia/lapor-spt-tahunan-orang-pribadi |
| 17 | Lebih bayar: pilih restitusi atau kompensasi; OP **tanpa** usaha/pekerjaan bebas, dan OP usaha/pekerjaan bebas dengan LB ≤ **Rp100 juta**, termasuk WP persyaratan tertentu (pengembalian pendahuluan, Pasal 17D UU KUP; PMK 39/2018 s.t.d.t.d. PMK 209/2021 s.t.d.d. PMK 119/2024) | 🟡 (Kring Pajak & 2 sekunder) | https://x.com/kring_pajak/status/1915684630981992528 ; https://artikel.pajakku.com/syarat-dan-prosedur-pengembalian-pendahuluan-dalam-restitusi-pajak ; https://www.ortax.org/lapor-spt-tahunan-pph-lebih-bayar-apa-prosedur-selanjutnya |
| 18 | Batas lapor SPT Tahunan OP: 3 bulan setelah akhir tahun pajak (**31 Maret**), tidak bergeser meski hari libur | ✅ (PMK 81/2024 Pasal 169, dicek di riset `kalender-pajak` 2026-09-26) | https://www.pajak.go.id/en/node/113110 |
| 19 | TP 2025 (lapor 2026) diperpanjang sekali ke **30 April 2026** lewat KEP-55/PJ/2026 | 🟡 (1 sumber utama, riset `kalender-pajak`) | https://news.ddtc.co.id/berita/nasional/1818216/batas-waktu-pelaporan-spt-tahunan-wp-op-diperpanjang-hingga-april-2026 |
| 20 | Denda telat lapor SPT Tahunan OP **Rp100.000** (UU KUP Pasal 7 ayat (1)), ditagih lewat STP | 🟡 (DDTC, situs DJP lama); nilai tidak diubah UU HPP | https://news.ddtc.co.id/berita/nasional/1810050/telat-lapor-spt-tahunan-dendanya-tunggu-surat-tagihan-pajak-terbit ; https://pajak.go.id/en/node/66324 |
| 21 | Telat bayar kurang bayar → sanksi bunga per bulan (tarif acuan KMK bulanan, UU KUP Pasal 9 ayat (2b)). **Tidak dihitung script** | ⚠️ PERLU REVIEW (tarif berubah tiap bulan) | — |

## B. Formulir SPT di Coretax (tahun pajak 2025 dilaporkan 2026 dan seterusnya)

| # | Fakta | Status | Sumber |
|---|---|---|---|
| 22 | Formulir **1770, 1770 S, 1770 SS dihapus**; mulai TP 2025 hanya **satu SPT Tahunan PPh OP** dinamis (pertanyaan ya/tidak di induk menentukan lampiran) | ✅ situs DJP (30 Des 2025) | https://pajak.go.id/en/node/118848 ; https://www.pajak.go.id/index.php/en/node/118193 |
| 23 | Dasar bentuk SPT: **PER-11/PJ/2025** | 🟡 (Ortax; artikel DJP #22 tidak menyebut) | https://ortax.org/bentuk-spt-tahunan-pph-orang-pribadi-era-coretax ; https://ideatax.id/id/articles/perdirjen-pajak-nomor-11-tahun-2025 |
| 24 | Induk: A Identitas · B Ikhtisar Penghasilan Neto · C PPh Terutang · D Kredit Pajak · E PPh Kurang/Lebih Bayar · F Pembetulan · G Permohonan Pengembalian LB · H Angsuran PPh 25 Tahun Berikutnya · I Pernyataan Transaksi Lainnya · J Lampiran Tambahan · K Pernyataan | 🟡 (Ortax, 10 Sep 2025) | idem |
| 25 | Lampiran 1: harta, utang, tanggungan, penghasilan neto dari pekerjaan, daftar bukti potong · Lampiran 2: penghasilan final, bukan objek, luar negeri · Lampiran 3: L-3A-1…L-3A-4 (rekonsiliasi/neto usaha & pekerjaan bebas), L-3B rekap peredaran bruto, L-3C penyusutan, L-3D rincian biaya · Lampiran 4: angsuran PPh 25 & PPh terutang suami-istri PH/MT · Lampiran 5: kompensasi kerugian, pengurang penghasilan, pengurang pajak | 🟡 (Ortax) — kode persis ⚠️ PERLU REVIEW (bisa berubah di rilis Coretax) | idem |
| 26 | Bukti potong yang dibuat pemotong di Coretax (mis. A1 format baru) otomatis tersedia/terisi saat konsep SPT dibuat ("Posting") | 🟡 (Coretaxpedia) | https://pajak.go.id/coretaxpedia/lapor-spt-tahunan-orang-pribadi |
| 27 | Keluarga = satu kesatuan ekonomi; penghasilan istri digabung kecuali PH/MT (atau istri hanya dari 1 pemberi kerja yang sudah dipotong & tidak terkait usaha suami — UU PPh Pasal 8 ayat (1)) | 🟡 (situs DJP; Pasal 8 dari ingatan riset sebelumnya) → PH/MT **di luar cakupan** skill | https://pajak.go.id/en/node/118848 |

## C. Keputusan desain skill
- Script menghitung PPh Pasal 17 atas penghasilan **non-final** saja. Omzet PP 55 hanya dicatat (tidak mengubah PPh terutang) dan dipakai untuk cek batas NPPN Rp4,8 M.
- Neto karyawan diambil dari angka **"penghasilan neto" di bukti potong A1/A2** (paling akurat). Helper `--a1-bruto` hanya cadangan (biaya jabatan dihitung; iuran pensiun harus diisi manual).
- Rugi usaha/pekerjaan bebas (neto negatif), kompensasi kerugian, PH/MT, penghasilan luar negeri (PPh 24), WP baru di tengah tahun (disetahunkan) → **di luar cakupan** MVP, script menolak/menyarankan konsultan.
- Pembulatan: neto NPPN = bruto × persen dibulatkan ke rupiah terdekat; PKP dibulatkan ke bawah ribuan; PPh dibulatkan ke bawah rupiah (praktis selalu bulat). **Belum dicocokkan dengan Coretax.**

## D. PERLU REVIEW (ringkas)
1. Nomor pasal NPPN (Pasal 450 vs 463 PMK 81/2024 s.t.d.d. PMK 1/2026) & klaim "selamanya pembukuan" (#7–8).
2. Tabel persen NPPN (PER-17/PJ/2015) — skill tidak menyimpan; wajib cek lampiran (#10).
3. Kode lampiran Coretax (#25) dan penerapan PPh 25 untuk karyawan-saja (#15).
4. Tarif bunga keterlambatan (#21) tidak dihitung.
5. Pembulatan belum dicocokkan dengan hitungan otomatis Coretax.
