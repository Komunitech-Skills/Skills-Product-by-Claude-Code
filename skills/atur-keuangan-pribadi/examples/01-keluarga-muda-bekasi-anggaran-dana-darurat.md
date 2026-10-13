# Uji 01 — Keluarga muda Bekasi: anggaran bulanan + dana darurat

> Penguji independen (Tahap 6), 2026-09-26. Skill dijalankan dari salinan di scratchpad; semua angka di bawah keluaran asli `scripts/keuangan.py`, lalu dicek ulang dengan simulasi independen penguji (lihat HASIL-UJI.md).
>
> **Disinkronkan dengan skrip v1.0.12 2026-10-13.** Versi awal contoh ini memakai dasar lama (THR dibagi 12 dihitung sebagai pemasukan bulanan): "cicilan = 31,8% pemasukan" dan "setoran dana darurat Rp1.371.666/bulan". Script sekarang memakai **gaji rutin** sebagai dasar: cicilan = 34,4% dari gaji rutin, sisa gaji rutin untuk dana darurat Rp330.000/bulan, THR disetor sekaligus saat cair. Perintah, keluaran, dan jawaban di bawah sudah dijalankan ulang dengan script sekarang.

## Input pengguna
"Kami tinggal di Bekasi, anak 1 umur 2 tahun (dititip daycare). Gaji bersih suami 8,5 juta, istri 4 juta. THR masing-masing 1x gaji. Cicilan motor 1,2 juta, KPR 3,1 juta, kirim ke orang tua 1 juta. Listrik+PDAM+gas sekitar 650 ribu, belanja dapur 2,2 juta, susu & popok 750 ribu, daycare 1 juta, bensin+tol+parkir 600 ribu, pulsa & internet 350 ribu, sedekah 200 ribu, kondangan rata-rata 150 ribu, makan di luar 400 ribu, Netflix dkk 70 ribu. Dana darurat baru ada 8 juta. Tolong atur anggaran bulanan dan berapa dana darurat yang harus kami punya."

## Perintah yang dijalankan agent
```
python3 scripts/keuangan.py anggaran --pemasukan "Gaji suami=8,5jt" --pemasukan "Gaji istri=4jt" \
  --musiman "THR suami=8,5jt" --musiman "THR istri=4jt" \
  --pos "Cicilan KPR=3,1jt:wajib" --pos "Cicilan motor=1,2jt:wajib" --pos "Listrik token+PDAM+gas=650rb:wajib" \
  --pos "Belanja dapur=2,2jt:wajib" --pos "Susu & popok anak=750rb:wajib" --pos "Daycare=1jt:wajib" \
  --pos "Bensin+tol+parkir=600rb:wajib" --pos "Pulsa & internet rumah=350rb:wajib" \
  --pos "Kiriman orang tua=1jt:sosial" --pos "Sedekah/infak=200rb:sosial" --pos "Kondangan=150rb:sosial" \
  --pos "Makan di luar=400rb:keinginan" --pos "Langganan streaming=70rb:keinginan" \
  --pos "Dana darurat=330rb:tabungan" --pos "Dana pendidikan anak=500rb:tabungan" --pola 60/20/20 --status anak --saldo 8jt
python3 scripts/keuangan.py dana-darurat --pengeluaran-pokok 5.550.000 --cicilan "Cicilan KPR=3,1jt" --cicilan "Cicilan motor=1,2jt" \
  --keluarga "Kiriman orang tua=1jt" --status anak --saldo 8jt --setoran 330rb --setoran-tahunan 12,5jt
```
Catatan proses: percobaan pertama memakai pos dana darurat Rp1.000.000 → script menulis "Pengeluaran rutin Rp13.170.000/bulan lebih besar dari gaji rutin Rp12.500.000 -> DEFISIT Rp670.000/bulan". Agent menurunkan setoran dana darurat ke sisa gaji rutin (Rp330.000) dan memperlakukan THR Rp12.500.000 sebagai setoran sekaligus saat cair → sisa gaji rutin Rp0. Dasar dana darurat Rp10.850.000 diambil dari bagian "Dasar dana darurat" keluaran `anggaran` (kebutuhan wajib di luar cicilan Rp5.550.000 + cicilan + kiriman orang tua), bukan dijumlah sendiri.

## Keluaran script (asli, dijalankan ulang 2026-10-13)
```
# RINGKASAN SIAP TEMPEL (salin kalimat ini APA ADANYA - jangan menghitung/menafsir ulang)

> Gaji rutin Rp12.500.000/bulan, total pos Rp12.500.000/bulan -> sisa Rp0/bulan dari gaji; inilah batas setoran bulanan.
> Total cicilan Rp4.300.000 = 34,4% dari gaji rutin Rp12.500.000 — DI ATAS batas aman 30% - jangan menambah utang baru.
> THR suami + THR istri Rp12.500.000 cair SEKALI (bukan tiap bulan) - setor SEKALIGUS saat cair ke dana darurat/target; jangan ditambahkan ke setoran bulanan. Angka ini belum dikurangi kebutuhan Lebaran (mudik, baju, kue, angpau) - sebutkan berapa yang perlu disisihkan, nanti setoran THR dihitung ulang.
> Pengeluaran pokok Rp10.850.000/bulan -> target dana darurat 9 bulan = Rp97.650.000; 12 bulan = Rp130.200.000.
> Saldo dana darurat sekarang Rp8.000.000 -> 9 bulan: kurang Rp89.650.000 (progres 8%), tercapai 272 bulan (~22 th 8 bln) dengan setoran Rp330.000/bulan, atau 72 bulan (~6 th 0 bln) bila THR suami + THR istri Rp12.500.000 juga disetor tiap cair (cair pertama bulan ke-12, asumsi bawaan); 12 bulan: kurang Rp122.200.000 (progres 6%), tercapai 371 bulan (~30 th 11 bln) dengan setoran Rp330.000/bulan, atau 96 bulan (~8 th 0 bln) bila THR suami + THR istri Rp12.500.000 juga disetor tiap cair (cair pertama bulan ke-12, asumsi bawaan).

- PENGINGAT: --sisih-lebaran belum diisi (dianggap Rp0 = seluruh THR untuk dana darurat/defisit). Tanyakan kebutuhan Lebaran pengguna (mudik, baju, kue, angpau) lalu jalankan ulang dengan --sisih-lebaran; jangan menyuruh menyetor SELURUH THR tanpa menyebut hal ini.

- Jangan menyebut persen satu pos (mis. KPR saja) sebagai "rasio cicilan"; rasio cicilan = kalimat 'Total cicilan ...' di atas.

# Anggaran Bulanan (zero-based)

## Pemasukan per bulan

| Sumber | Jumlah |
|---|---:|
| Gaji suami | Rp8.500.000 |
| Gaji istri | Rp4.000.000 |
| Musiman dibagi 12 (THR suami Rp8.500.000, THR istri Rp4.000.000; total Rp12.500.000/th) | Rp1.041.666 |
| **Total pemasukan** | **Rp13.541.666** |

## Pos pengeluaran & alokasi

| Pos | Kelompok | Jumlah | % pemasukan rutin (Rp12.500.000) | % termasuk THR/12 (Rp13.541.666) |
|---|---|---:|---:|---:|
| Cicilan KPR | Kebutuhan wajib | Rp3.100.000 | 24,8% | 22,9% |
| Cicilan motor | Kebutuhan wajib | Rp1.200.000 | 9,6% | 8,9% |
| Listrik token+PDAM+gas | Kebutuhan wajib | Rp650.000 | 5,2% | 4,8% |
| Belanja dapur | Kebutuhan wajib | Rp2.200.000 | 17,6% | 16,2% |
| Susu & popok anak | Kebutuhan wajib | Rp750.000 | 6,0% | 5,5% |
| Daycare | Kebutuhan wajib | Rp1.000.000 | 8,0% | 7,4% |
| Bensin+tol+parkir | Kebutuhan wajib | Rp600.000 | 4,8% | 4,4% |
| Pulsa & internet rumah | Kebutuhan wajib | Rp350.000 | 2,8% | 2,6% |
| Kiriman orang tua | Keluarga & sosial/ibadah | Rp1.000.000 | 8,0% | 7,4% |
| Sedekah/infak | Keluarga & sosial/ibadah | Rp200.000 | 1,6% | 1,5% |
| Kondangan | Keluarga & sosial/ibadah | Rp150.000 | 1,2% | 1,1% |
| Makan di luar | Keinginan | Rp400.000 | 3,2% | 3,0% |
| Langganan streaming | Keinginan | Rp70.000 | 0,6% | 0,5% |
| Dana darurat | Tabungan, dana darurat & pelunasan ekstra | Rp330.000 | 2,6% | 2,4% |
| Dana pendidikan anak | Tabungan, dana darurat & pelunasan ekstra | Rp500.000 | 4,0% | 3,7% |
| **Total dialokasikan** | | **Rp12.500.000** | 100,0% | 92,3% |
| **Belum dialokasikan** (termasuk THR/12 bila ada) | | **Rp1.041.666** | harus dijadikan 0 | |

- Saat menyebut persen ke pengguna, sebut basisnya: "% dari gaji rutin" (kolom pertama) atau "% termasuk THR/12" (kolom kedua). Jangan melabeli kolom kedua sebagai "% gaji".

## Banding pola 60/20/20 - basis pemasukan rutin Rp12.500.000/bulan

| Kelompok | Pola | Batas pola | Rencana kamu | Selisih |
|---|---:|---:|---:|---:|
| Kebutuhan (wajib + keluarga/sosial) | 60% | Rp7.500.000 | Rp11.200.000 | +Rp3.700.000 |
| Keinginan | 20% | Rp2.500.000 | Rp470.000 | -Rp2.030.000 |
| Tabungan & pelunasan ekstra | 20% | Rp2.500.000 | Rp830.000 | -Rp1.670.000 |

- Basis banding = gaji rutin (tanpa THR/12), sama dengan rasio cicilan. THR suami, THR istri Rp12.500.000 (sekali cair) di luar banding ini - jadikan setoran sekaligus ke dana darurat/target.

## Catatan

- Masih ada Rp1.041.666 belum punya tugas (Rp0 dari gaji tiap bulan + Rp1.041.666 bagian THR/bonus yang cair sekali Rp12.500.000). Zero-based: arahkan ke dana darurat, pelunasan utang berbunga tinggi, atau target tabungan sampai sisa Rp0.
- Kebutuhan tetap melebihi batas pola 60%. Cek pos terbesar (tempat tinggal, cicilan, dapur) dan jangan menambah cicilan baru; tabungan sekecil apa pun tetap jalan.
- Tabungan di bawah pola. Mulai dari jumlah kecil yang rutin (bayar diri sendiri dulu di hari gajian).
- Total cicilan Rp4.300.000 = 34,4% dari pemasukan RUTIN per bulan Rp12.500.000 (basis tanpa THR/bonus, karena THR tidak ada tiap bulan). Sebagai pembanding, terhadap pemasukan termasuk THR/12: 31,8%. DI ATAS patokan umum 30% - jangan menambah utang baru; pertimbangkan subperintah utang.
- Pemasukan musiman (THR/bonus) dibagi 12 dan dibulatkan ke bawah HANYA untuk gambaran setahun. Uangnya cair sekali - lihat bagian 'Arus kas rutin vs musiman' untuk setoran bulanan yang benar-benar ada.

## Arus kas rutin vs musiman (THR/bonus)

| Arus | Per bulan | Kapan uangnya ada |
|---|---:|---|
| Pemasukan rutin (gaji bersih) | Rp12.500.000 | tiap bulan |
| Total pos dialokasikan | Rp12.500.000 | tiap bulan |
| **Sisa dari pemasukan rutin** | **Rp0** | tiap bulan |
| THR suami, THR istri (setara /12) | Rp1.041.666 | SEKALI saat cair: Rp12.500.000 |

- Setoran/transfer BULANAN (dana darurat, target, pelunasan ekstra) paling banyak **Rp0/bulan** - hanya dari gaji. Jangan menyebut sisa Rp1.041.666 sebagai uang yang bisa dipindah tiap bulan: Rp1.041.666 di dalamnya adalah bagian THR/bonus.
- THR suami, THR istri **Rp12.500.000** dicadangkan/disetor SEKALIGUS saat cair (mis. langsung ke dana darurat atau target). Itu setara Rp1.041.666 x 12 bulan - jangan ditambahkan lagi ke setoran bulanan (dihitung dua kali).
- Langkah aksi ke pengguna WAJIB memakai angka di tabel ini: setoran bulanan dari sisa rutin, THR/bonus sebagai setoran sekaligus saat cair.

## Dasar dana darurat (pengeluaran pokok per bulan)

| Pos DIMASUKKAN ke pokok | Jenis | Jumlah |
|---|---|---:|
| Cicilan KPR | cicilan/utang minimum | Rp3.100.000 |
| Cicilan motor | cicilan/utang minimum | Rp1.200.000 |
| Listrik token+PDAM+gas | kebutuhan wajib | Rp650.000 |
| Belanja dapur | kebutuhan wajib | Rp2.200.000 |
| Susu & popok anak | kebutuhan wajib | Rp750.000 |
| Daycare | kebutuhan wajib | Rp1.000.000 |
| Bensin+tol+parkir | kebutuhan wajib | Rp600.000 |
| Pulsa & internet rumah | kebutuhan wajib | Rp350.000 |
| Kiriman orang tua | kewajiban rutin keluarga | Rp1.000.000 |
| **Total pengeluaran pokok** | | **Rp10.850.000** |

| Pos DIKELUARKAN dari pokok | Jumlah | Alasan |
|---|---:|---|
| Sedekah/infak | Rp200.000 | sosial/ibadah sukarela, bisa ditunda saat darurat - tambahkan bila memang wajib |
| Kondangan | Rp150.000 | sosial/ibadah sukarela, bisa ditunda saat darurat - tambahkan bila memang wajib |
| Makan di luar | Rp400.000 | keinginan/jajan/hiburan, bisa dikurangi atau dihentikan saat darurat |
| Langganan streaming | Rp70.000 | keinginan/jajan/hiburan, bisa dikurangi atau dihentikan saat darurat |
| Dana darurat | Rp330.000 | tabungan/dana darurat/pelunasan ekstra, bukan biaya hidup |
| Dana pendidikan anak | Rp500.000 | tabungan/dana darurat/pelunasan ekstra, bukan biaya hidup |

- Pokok = Kebutuhan wajib + SEMUA cicilan/utang minimum (PayLater, kartu kredit, KPR, pinjol, leasing, KTA) + kewajiban rutin keluarga (kiriman orang tua/mertua/adik) - tetap harus dibayar walau penghasilan berhenti.
- Sebutkan ke pengguna pos yang dimasukkan DAN yang dikeluarkan beserta alasannya. Bila pengguna ingin mengubah, jalankan ulang dengan --pokok-juga "nama pos" atau --bukan-pokok "nama pos".
- Pakai angka ini untuk dana darurat: dana-darurat --pengeluaran-pokok 10850000 --status ...

## Skenario alternatif dasar dana darurat (siap salin - JANGAN hitung sendiri)

| Skenario | Pokok/bulan | 9 bulan | 12 bulan |
|---|---:|---:|---:|
| Sekarang (kiriman keluarga dimasukkan) | Rp10.850.000 | Rp97.650.000 | Rp130.200.000 |
| Tanpa Kiriman orang tua (Rp1.000.000) | Rp9.850.000 | Rp88.650.000 | Rp118.200.000 |

Kalimat siap tempel:

> Bila Kiriman orang tua (Rp1.000.000/bulan) bisa dihentikan saat darurat, pengeluaran pokok turun menjadi Rp9.850.000 dan target 9 bulan/12 bulan menjadi Rp88.650.000/Rp118.200.000.

### Lama tercapai sekarang vs skenario (bulan) - setoran tetap Rp330.000/bulan; Rp12.500.000 sekali setahun mulai bulan ke-12

| Skenario | Target | Setoran saja: sekarang -> skenario | Selisih | + THR/bonus: sekarang -> skenario | Selisih |
|---|---|---|---|---|---|
| Tanpa Kiriman orang tua | 9 bulan | 272 bulan -> 245 bulan | 27 bulan lebih cepat | 72 bulan -> 60 bulan | 12 bulan lebih cepat |
| Tanpa Kiriman orang tua | 12 bulan | 371 bulan -> 334 bulan | 37 bulan lebih cepat | 96 bulan -> 84 bulan | 12 bulan lebih cepat |

Kalimat siap tempel:

> Lama tercapai bila Kiriman orang tua tidak dihitung (setoran tetap): target 9 bulan: setoran saja 272 bulan -> 245 bulan (27 bulan lebih cepat), dengan THR/bonus 72 bulan -> 60 bulan (12 bulan lebih cepat); target 12 bulan: setoran saja 371 bulan -> 334 bulan (37 bulan lebih cepat), dengan THR/bonus 96 bulan -> 84 bulan (12 bulan lebih cepat).

- Selisih waktu HANYA dari tabel ini, per kolom. Jangan meringkas menjadi "sekitar setahun lebih cepat" bila kolom-kolomnya berbeda (ada yang tidak berubah).

Bukan nasihat keuangan/investasi. Kasus rumit: konsultasikan ke perencana keuangan bersertifikat.

# Dana Darurat

- Status: Menikah/orang tua tunggal dengan anak atau tanggungan -> target 9-12 bulan pengeluaran pokok
- Pengeluaran pokok per bulan: Rp10.850.000 (rincian di bawah)
- Saldo sekarang: Rp8.000.000 | Setoran rutin (dari gaji): Rp330.000/bulan
- Setoran sekaligus THR/bonus: Rp12.500.000 sekali setahun, cair bulan ke-12 dari sekarang (asumsi bawaan; tanyakan bulan cairnya) - TIDAK termasuk dalam setoran rutin di atas
- PENGINGAT: --sisih-lebaran belum diisi (dianggap Rp0 = seluruh Rp12.500.000 ke dana darurat). Tanyakan kebutuhan Lebaran (mudik, baju, kue, angpau) lalu jalankan ulang dengan --sisih-lebaran.

| Target | Jumlah | Kekurangan | Lama tercapai (setoran rutin saja) | Lama tercapai (+ THR/bonus) | Progres |
|---|---:|---:|---:|---:|---:|
| 9 bulan | Rp97.650.000 | Rp89.650.000 | 272 bulan (~22 th 8 bln) | 72 bulan (~6 th 0 bln) | #................... 8% |
| 12 bulan | Rp130.200.000 | Rp122.200.000 | 371 bulan (~30 th 11 bln) | 96 bulan (~8 th 0 bln) | #................... 6% |

| Pos DIMASUKKAN ke pokok | Jumlah |
|---|---:|
| Pengeluaran pokok (angka gabungan) | Rp5.550.000 |
| Cicilan KPR (cicilan) | Rp3.100.000 |
| Cicilan motor (cicilan) | Rp1.200.000 |
| Kiriman orang tua (kewajiban keluarga) | Rp1.000.000 |
| **Total pengeluaran pokok** | **Rp10.850.000** |

## Skenario alternatif dasar dana darurat (siap salin - JANGAN hitung sendiri)

| Skenario | Pokok/bulan | 9 bulan | 12 bulan |
|---|---:|---:|---:|
| Sekarang (kiriman keluarga dimasukkan) | Rp10.850.000 | Rp97.650.000 | Rp130.200.000 |
| Tanpa Kiriman orang tua (Rp1.000.000) | Rp9.850.000 | Rp88.650.000 | Rp118.200.000 |

Kalimat siap tempel:

> Bila Kiriman orang tua (Rp1.000.000/bulan) bisa dihentikan saat darurat, pengeluaran pokok turun menjadi Rp9.850.000 dan target 9 bulan/12 bulan menjadi Rp88.650.000/Rp118.200.000.

### Lama tercapai sekarang vs skenario (bulan) - setoran tetap Rp330.000/bulan; Rp12.500.000 sekali setahun mulai bulan ke-12

| Skenario | Target | Setoran saja: sekarang -> skenario | Selisih | + THR/bonus: sekarang -> skenario | Selisih |
|---|---|---|---|---|---|
| Tanpa Kiriman orang tua | 9 bulan | 272 bulan -> 245 bulan | 27 bulan lebih cepat | 72 bulan -> 60 bulan | 12 bulan lebih cepat |
| Tanpa Kiriman orang tua | 12 bulan | 371 bulan -> 334 bulan | 37 bulan lebih cepat | 96 bulan -> 84 bulan | 12 bulan lebih cepat |

Kalimat siap tempel:

> Lama tercapai bila Kiriman orang tua tidak dihitung (setoran tetap): target 9 bulan: setoran saja 272 bulan -> 245 bulan (27 bulan lebih cepat), dengan THR/bonus 72 bulan -> 60 bulan (12 bulan lebih cepat); target 12 bulan: setoran saja 371 bulan -> 334 bulan (37 bulan lebih cepat), dengan THR/bonus 96 bulan -> 84 bulan (12 bulan lebih cepat).

- Selisih waktu HANYA dari tabel ini, per kolom. Jangan meringkas menjadi "sekitar setahun lebih cepat" bila kolom-kolomnya berbeda (ada yang tidak berubah).

Catatan:
- Pengeluaran pokok = yang tetap harus dibayar walau penghasilan berhenti (makan, tempat tinggal, listrik/air, transport, SEMUA cicilan/utang minimum, sekolah, BPJS, kiriman keluarga yang wajib). Bukan nongkrong/hiburan.
- Simpan di tempat terpisah yang aman dan cepat dicairkan (bukan instrumen yang nilainya naik-turun).
- Punya utang berbunga tinggi (kartu kredit/paylater/pinjol)? Kumpulkan dana darurat awal ~1 bulan pengeluaran pokok dulu, lalu fokus lunasi utang, baru lengkapi dana darurat.

Bukan nasihat keuangan/investasi. Kasus rumit: konsultasikan ke perencana keuangan bersertifikat.
```

## Jawaban akhir agent (sesuai format SKILL.md)

## Ringkasan
Gaji rutin Rp12.500.000/bulan, total pos Rp12.500.000/bulan -> sisa Rp0/bulan dari gaji; inilah batas setoran bulanan (dana darurat Rp330.000 dan dana pendidikan anak Rp500.000 sudah termasuk di pos). Total cicilan Rp4.300.000 = 34,4% dari gaji rutin Rp12.500.000 — DI ATAS batas aman 30% - jangan menambah utang baru. THR suami + THR istri Rp12.500.000 cair SEKALI (bukan tiap bulan) - setor SEKALIGUS saat cair ke dana darurat/target; jangan ditambahkan ke setoran bulanan — sebutkan dulu berapa yang perlu disisihkan untuk Lebaran (mudik, baju, kue, angpau) agar setoran THR dihitung ulang.

## Anggaran
Banding pola 60/20/20 — basis pemasukan rutin Rp12.500.000/bulan (angka dari script):
| Kelompok | Batas pola | Rencana | Selisih |
|---|---:|---:|---:|
| Kebutuhan (wajib + keluarga/sosial) | Rp7.500.000 | Rp11.200.000 | +Rp3.700.000 |
| Keinginan (makan di luar, streaming) | Rp2.500.000 | Rp470.000 | -Rp2.030.000 |
| Tabungan (dana darurat Rp330.000 + pendidikan anak Rp500.000) | Rp2.500.000 | Rp830.000 | -Rp1.670.000 |

Rincian per pos (kolom "% pemasukan rutin") ada di tabel script di atas; sisa dari gaji rutin **Rp0**. Keinginan sudah sangat hemat, jadi ruang potong hampir habis — perbaikan harus datang dari tambah pemasukan atau (nanti) cicilan motor lunas.

## Dana Darurat
Status: menikah + 1 anak → target 9–12 bulan pengeluaran pokok **Rp10.850.000** (dimasukkan: kebutuhan wajib, cicilan KPR & motor, kiriman orang tua; dikeluarkan: sedekah & kondangan — sukarela, bisa ditunda saat darurat; makan di luar & streaming — keinginan; pos tabungan).
| Target | Jumlah | Kekurangan | Setoran Rp330.000/bulan saja | + THR Rp12.500.000 tiap cair |
|---|---:|---:|---:|---:|
| 9 bulan | Rp97.650.000 | Rp89.650.000 | 272 bulan (~22 th 8 bln) | 72 bulan (~6 th 0 bln) |
| 12 bulan | Rp130.200.000 | Rp122.200.000 | 371 bulan (~30 th 11 bln) | 96 bulan (~8 th 0 bln) |

Dari gaji saja, dana darurat hampir mustahil terkumpul — THR adalah sumber utamanya. Bila Kiriman orang tua (Rp1.000.000/bulan) bisa dihentikan saat darurat, pengeluaran pokok turun menjadi Rp9.850.000 dan target 9 bulan/12 bulan menjadi Rp88.650.000/Rp118.200.000. Begitu cicilan motor lunas, alihkan cicilannya ke dana darurat dan jalankan ulang script dengan setoran baru untuk melihat lama tercapainya.

## Asumsi yang dipakai
- Dasar semua persen = gaji rutin Rp12.500.000 (tanpa THR). THR Rp12.500.000 cair sekali; dianggap cair 12 bulan lagi (asumsi bawaan script, paling hati-hati) dan belum dikurangi kebutuhan Lebaran.
- Pola pembanding 60/20/20 (keluarga dengan anak & kiriman ortu).
- Pengeluaran pokok tidak termasuk sedekah & kondangan (bisa ditunda saat darurat); kiriman ortu tetap dihitung.
- BPJS Kesehatan dianggap dipotong kantor (tidak ada di pos). Bila mandiri, tambahkan.

## Langkah minggu ini
1. Buka rekening/kantong terpisah khusus dana darurat; atur autodebet Rp330.000 tanggal gajian (batas setoran bulanan = sisa gaji rutin).
2. Pisahkan Rp500.000 dana pendidikan anak di kantong lain.
3. Catat pengeluaran e-wallet sebulan ini menurut pemakaian (top-up bukan pengeluaran).
4. Sepakati suami-istri: tidak ada cicilan/paylater baru — total cicilan sudah 34,4% dari gaji rutin, di atas batas aman 30%.
5. Saat THR Rp12.500.000 cair: sisihkan dulu kebutuhan Lebaran (beri tahu nominalnya agar dihitung ulang), sisanya setor sekaligus ke dana darurat — jangan dibagi ke setoran bulanan.

⚠️ Bukan nasihat keuangan/investasi. Angka adalah simulasi dari data & asumsi di atas. Untuk kasus rumit, konsultasikan ke perencana keuangan bersertifikat.

## Penilaian penguji
- Angka dicek manual (ulang 2026-10-13): rasio cicilan 4.300.000 ÷ 12.500.000 = 34,4% ✓; sisa gaji rutin 12.500.000 − 12.170.000 (pos di luar dana darurat) = 330.000 ✓; 89.650.000 ÷ 330.000 = 271,7 → 272 bulan ✓; 122.200.000 ÷ 330.000 = 370,3 → 371 ✓; dengan THR tiap bulan ke-12: bulan 72 → 72 × 330.000 + 6 × 12.500.000 = 98.760.000 ≥ 89.650.000 (bulan 71: 85.930.000 <) ✓; bulan 96 → 131.680.000 ≥ 122.200.000 (bulan 95: 118.850.000 <) ✓.
- Kategori khas Indonesia (kiriman ortu, kondangan, sedekah opsional, THR dipisah dari arus bulanan) tertangani; Ringkasan menyalin RINGKASAN SIAP TEMPEL apa adanya.
- Catatan: script tidak menghitung simulasi "setelah motor lunas" — agent tidak mengarang angkanya dan menyarankan menjalankan ulang script.
- **Hasil: LULUS.**
