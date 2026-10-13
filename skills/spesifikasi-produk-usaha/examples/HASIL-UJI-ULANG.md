# HASIL UJI ULANG - spesifikasi-produk-usaha v1.0.1

Penguji: agent independen (bukan pembuat, bukan penguji v1.0.0), 2026-09-29. Hanya membaca folder skill + pedoman kurasi Komunitech. Platform: `claude-code (simulasi agent)`. Data uji & skrip bantu ada di scratchpad penguji (tidak di folder skill). Skill tidak diubah.

## 1. Pemeriksaan otomatis
| Cek | Hasil |
|---|---|
| `python3 scripts/validate.py --skill spesifikasi-produk-usaha` | "1 skill valid", kode 0 |
| `tests/uji_regresi.py` | 40/40 lulus |
| Frontmatter hanya `name` + `description`; SKILL.md 83 baris | OK |
| Script: hanya pustaka standar, tanpa jaringan/subprocess/eval | OK (dibaca penuh) |

## 2. Verifikasi perbaikan F1-F6
| # | Perbaikan | Cara uji | Hasil |
|---|---|---|---|
| F1 | Kapasitas tidak mengunci tahap | `Besar(15) Sedang(4) Kecil(2)`, `--kapasitas 10` | Nanti (+ catatan "pecah jadi langkah kecil"), Sekarang, Sekarang. Skor 200 / 120 / 40 cocok hitung manual. Kasus lewati-lalu-lanjut `6,6,3,4` kap 10 -> L3+L1 Sekarang (9), L2+L4 Berikutnya (10): benar. **LULUS** |
| F2 | Keyakinan pecahan ditolak | `0,9`, `0.8`, `1` tanpa `%` | Ketiganya ditolak dengan pesan "0,9 maksudnya 90%?"; `0,9%` eksplisit diterima (skor 1,35 = 300x1x0,009/2, benar); `90` -> 135. **LULUS** |
| F3 | Referensi izin akurat | 6 klaim dicek ke sumber resmi (lihat bagian 3) | Semua klaim yang dicek benar. **LULUS** (1 kekurangan minor: olahan susu tidak disebut) |
| F4 | Contoh 01 -> BPOM MD | baca `01-...md` | Bagian 7 menyatakan tegas "tidak bisa PIRT", BPOM MD, opsi ubah proses (dengan catatan kemasan kedap juga pengecualian), tenggat halal 17-10-2026, tabel dasar aturan + tanggal cek. Roadmap = keluaran default contoh 02 (dijalankan ulang: identik). Klaim `--kapasitas 10` di contoh 02 dicek manual: benar. **LULUS** |
| F5 | Ukuran keberhasilan | SKILL.md langkah 3, Format Output bagian 2, cek akhir (f), templat baris 13, contoh 01, README | Ada di semua tempat, terukur dengan batas waktu. **LULUS** |
| F6 | Bug minor | `10,000` -> ditolak ambigu dengan saran; `10,000,000` -> 10 juta; `1.500,5` -> 1500,5; judul `idea,reach,impact,conf,effort` -> "kolom wajib tidak ditemukan: nama, keyakinan" + judul terbaca; judul Inggris lengkap diterima; ICE + `--kapasitas` -> PERINGATAN (stdout, stderr, JSON); 4 ide -> 2/1/1; 4 ide dengan 3 skor seri -> 3/0/1 + catatan (sesuai dokumentasi); kapasitas 0/huruf -> GAGAL jelas; file kosong -> GAGAL. **LULUS** |

## 3. Cek fakta referensi izin (WebSearch/WebFetch, 2026-09-29)
| Klaim di `references/perizinan-produk.md` | Sumber | Vonis |
|---|---|---|
| PIRT = Perban BPOM 4/2024; dikecualikan: rantai dingin/beku, kemasan hermetis, SNI wajib (AMDK, garam), klaim kesehatan, pangan bayi/PKGK, BTP, alkohol, produksi mesin otomatis; daya simpan < 7 hari | indramayu.pom.go.id/berita/jenis-pangan-yang-wajib-dan-tidak-wajib-mengurus-spp-irt ; peraturan.bpk.go.id/Details/282151 | **Benar.** Kurang: sumber juga menyebut **olahan berbasis susu** umumnya tidak bisa SPP-IRT (minor) |
| Halal UMK makanan-minuman 17-10-2026; kosmetik, obat bahan alam, suplemen, barang gunaan **sandang & aksesori** mulai 18-10-2026 (UU 33/2014, PP 42/2024) | bpjph.halal.go.id/read/tak-hanya-makanan-minuman-ini-jenis-produk-yang-wajib-bersertifikat-halal-mulai-18-oktober-2026 ; bpjph.halal.go.id/detail/bpjph-produk-kosmetik-wajib-bersertifikat-halal-pada-oktober-2026/ | **Benar** |
| Pakaian bayi SNI wajib, Permenperin 7/M-IND/PER/2/2014 (azo, formaldehida, logam terekstraksi, s.d. 36 bulan) | bsn.go.id berita 5744; pasal.id Permenperin 07/2014 | **Benar** (SNI 7617:2013) |
| Jamu/obat bahan alam -> registrasi BPOM, Perban BPOM 25/2023 | peraturan.go.id/id/peraturan-bpom-no-25-tahun-2023 ; ditwasotsk.pom.go.id | **Benar** |
| NIB: PP 28/2025 pengganti PP 5/2021 | peraturan.bpk.go.id/Details/319773/pp-no-28-tahun-2025 | **Benar** |
| DJKI: https://merek.dgip.go.id | dibuka langsung | **Benar** (situs resmi pendaftaran merek) |

## 4. Lima skenario (dijalankan ulang, mengikuti SKILL.md apa adanya)
Semua skor diverifikasi ulang dengan `fractions.Fraction` di luar script: **semua cocok**.

| # | Skenario | Hasil utama | Vonis |
|---|---|---|---|
| 1 | **Normal - piyama bayi katun + brief konveksi**; CSV 5 ide (`;`, `1.200`, `0,5`, `80%`), satu keyakinan ditulis `0,6` | Jalur izin: **SNI wajib pakaian bayi (Permenperin 7/2014), SPPT-SNI + tanda SNI**, uji lab azo/formaldehida/logam; halal sandang mulai 18-10-2026 (titik kritis: pewarna, kancing/aksesori); merek. Brief konveksi memuat ukuran, bahan, toleransi, sampel, MOQ, pertanyaan "SPPT-SNI yang dimiliki", tanpa HPP/margin. Script: 192 / 112,5 / 70 / 42,86 (benar); baris `0,6` ditolak dengan pesan "60%?" - agen meminta konfirmasi, tidak menebak (bila 60: 240 dan jadi #1) | **LULUS** (v1.0.0 GAGAL sebagian) |
| 2 | **Normal - dimsum beku, reseller**; RICE + `--kapasitas 10`, ide "Pabrik mini" usaha 30, jangkauan `"1,000"` | Langkah 5 & cek akhir (g): **beku -> tidak bisa PIRT, BPOM MD**; halal UMK 17-10-2026. Script: Pabrik mini 250 -> Nanti + "pecah jadi langkah kecil" (tidak lagi mengunci roadmap); paket 106,67 + vakum 80 Sekarang (9 hari); keju 80 Berikutnya (seri skor 80 dengan vakum, dipisah karena kapasitas; masuk akal); `1,000` ditolak ambigu | **LULUS** |
| 3 | **Normal - jamu kunyit asam botol + klaim "melancarkan haid"**; ICE 4 ide; HPP jual Rp12.000 margin 40% | Klaim khasiat ditolak/dibuang (langkah Batasan); jalur: jamu/obat bahan alam -> **BPOM TR** (Perban BPOM 25/2023) atau, bila dijual sebagai minuman tanpa klaim, pangan yang disimpan dingin -> BPOM MD - agen menulis "perlu dipastikan ke instansi". HPP maks 12.000 x 0,6 = **Rp7.200** (benar). ICE 280/210/160/144 (benar), 2/1/1 | **LULUS** |
| 4 | **Input tidak lengkap** - "bikin spesifikasi produk buat usahaku dong" + CSV pengguna ber-koma dengan desimal koma tanpa tanda kutip (`Tas kertas,300,1,0,9,2`) | Agen bertanya sekali (jenis produk, pembeli, harga, pembaca). Script: baris `Pouch,200,0,5,80,1` ditolak (dampak 0). **Tetapi** `Tas kertas,300,1,0,9,2` (6 nilai untuk 5 kolom) dibaca keyakinan 0, usaha 9 -> **skor 0,00 diam-diam, tanpa peringatan**, masuk Berikutnya | **LULUS dengan bug B10** |
| 5 | **Di luar cakupan** - minta hitung PPh final, buat kontrak maklon, tulis "sudah halal & BPOM" dengan nomor karangan | Pajak -> skill/konsultan pajak; kontrak -> profesional hukum; nomor izin & klaim halal/BPOM ditolak (Batasan: jangan mengarang nomor izin; langkah 4 referensi) | **LULUS** |

## 5. Temuan baru
**B10 (sedang) - baris dengan jumlah nilai lebih banyak dari judul kolom diterima diam-diam.** `csv.DictReader` menaruh nilai berlebih di kunci `None` dan script mengabaikannya. Kasus nyata: pengguna menulis desimal koma di file berpemisah koma tanpa kutip (`0,9`) -> nilai bergeser, keyakinan 0 -> skor 0,00, tanpa pesan. Jalur yang didokumentasikan (agen sendiri yang membuat CSV, langkah 6) biasanya aman, dan angka 0,00 tetap terlihat; karena itu tidak memblokir kelulusan, tetapi melanggar janji Batasan "script menolak baris ... jangan menebak". Saran: tolak baris yang punya nilai di luar kolom judul ("baris punya 6 nilai, judul 5 kolom; desimal koma di file berpemisah koma harus diberi tanda kutip atau pakai `;`") + uji regresi.

**Minor:** referensi PIRT belum menyebut olahan berbasis susu (disebut di sumber BPOM Indramayu yang sama).

## 6. A/B & pesaing
Tidak diulang: `00-pembanding-tanpa-skill.md` dan `00-banding-pesaing.md` v1.0.0 masih berlaku (skill menang jelas). Perbaikan 1.0.1 menutup satu-satunya kelebihan pesaing (metrik keberhasilan).

## 7. Skor: **8 / 10 - LULUS**
- (+) Semua F1-F6 terbukti diperbaiki dan diuji ulang dengan data rusak; semua angka cocok verifikasi independen.
- (+) Referensi izin kini akurat, punya dasar aturan + tanggal cek; jalur PIRT/MD/TR/notifikasi/SNI dipilih benar di 3 skenario normal, termasuk pakaian bayi dan produk beku.
- (-) B10: satu jalur input rusak masih menghasilkan skor salah diam-diam (−1).
- (-) Kekurangan minor olahan susu di referensi (−0,5), dibulatkan.

Rekomendasi: perbaiki B10 (+ uji regresi) sebelum naik ke `beta`; `platform_teruji` = `claude-code (simulasi agent)`.

## Catatan revisi 1.0.2 (kurator)
- B10 diperbaiki: baris dengan nilai lebih banyak dari judul kolom kini ditolak dengan pesan jelas (tes regresi ditambah).
