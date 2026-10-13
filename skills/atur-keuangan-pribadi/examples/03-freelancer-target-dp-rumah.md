# Uji 03 — Freelancer penghasilan naik-turun, target DP rumah Rp150 jt dalam 4 tahun

> Penguji independen, 2026-09-26. Keluaran asli script; target & dana darurat dicek ulang dengan rumus FV independen penguji.
>
> **Disinkronkan dengan skrip v1.0.12 2026-10-13.** Versi awal contoh ini memakai dasar lama (bonus ÷ 12 dihitung sebagai pemasukan bulanan): pemasukan Rp6.333.333 dan setoran DP **Rp1.383.333/bulan**, padahal sisa penghasilan rutin (bulan terendah Rp5.500.000) hanya cukup untuk setoran DP **Rp550.000/bulan**; bonus Rp10.000.000 kini disetor sekaligus saat cair. Pengeluaran pokok dana darurat kini diambil dari script (Rp4.450.000, termasuk langganan software kerja), bukan Rp4.300.000 hitungan agent. Perintah, keluaran, dan jawaban di bawah sudah dijalankan ulang dengan script sekarang.

## Input pengguna
"Saya desainer freelance, lajang, ngekos di Jogja. Penghasilan 6 bulan terakhir: 9 jt, 6,5 jt, 12 jt, 7 jt, 5,5 jt, 10 jt. Biasanya ada bonus proyek akhir tahun sekitar 10 jt (anggap 'THR' saya). Pengeluaran: kos 1,5 jt, makan 1,5 jt, transport 400 rb, internet+pulsa 300 rb, BPJS mandiri 100 rb, software 150 rb, kirim ibu 500 rb, nongkrong 300 rb. Dana darurat sudah 12 jt, DP rumah sudah ada 20 jt. Pengen DP rumah 150 jt dalam 4 tahun. Uang tabungan saya di deposito, bunganya kira-kira 4,5% setahun."

## Perintah yang dijalankan agent
```
python3 scripts/keuangan.py anggaran --pemasukan "Penghasilan freelance (bulan terendah 6 bln)=5,5jt" \
  --musiman "Bonus proyek akhir tahun=10jt" --pos "Kos=1,5jt:wajib" --pos "Makan & dapur=1,5jt:wajib" \
  --pos "Transport ojol/bensin=400rb:wajib" --pos "Internet & pulsa=300rb:wajib" \
  --pos "BPJS Kesehatan mandiri kelas 2=100rb:wajib" --pos "Kiriman ibu=500rb:sosial" \
  --pos "Langganan software kerja=150rb:wajib" --pos "Nongkrong & hiburan=300rb:keinginan" \
  --pos "Dana darurat=200rb:tabungan" --pos "DP rumah=550rb:tabungan" --status lepas --saldo 12jt
python3 scripts/keuangan.py dana-darurat --pengeluaran-pokok 3,95jt --keluarga "Kiriman ibu=500rb" --status lepas --saldo 12jt --setoran 200rb --setoran-tahunan 10jt
python3 scripts/keuangan.py target --nama "DP rumah" --jenis rumah --biaya-sekarang 150jt --tahun 4 --terkumpul 20jt --kemampuan 550rb
python3 scripts/keuangan.py target --nama "DP rumah (skenario imbal 4,5%)" --jenis rumah --biaya-sekarang 150jt --tahun 4 --imbal 4,5 --terkumpul 20jt --kemampuan 550rb
python3 scripts/keuangan.py target --nama "DP" --biaya-sekarang 150jt --tahun {6,7,8} --terkumpul 20jt --kemampuan 550rb   # tuas "perpanjang waktu"
```
(Imbal 4,5% dipakai hanya sebagai skenario karena pengguna sendiri menyebut angkanya — sesuai SKILL.md.)

Catatan proses: perintah versi awal (`--pos "DP rumah=1.383.333:tabungan"`) kini membuat script menulis "Pengeluaran rutin Rp6.333.333/bulan lebih besar dari gaji rutin Rp5.500.000 -> DEFISIT Rp833.333/bulan". Agent menurunkan setoran DP ke sisa penghasilan rutin (Rp550.000) dan memperlakukan bonus Rp10.000.000 sebagai setoran sekaligus saat cair → sisa rutin Rp0. Dasar dana darurat Rp4.450.000 diambil dari bagian "Dasar dana darurat" keluaran `anggaran` (Rp3.950.000 kebutuhan wajib + kiriman ibu Rp500.000). Tidak ada cicilan (baris "CEK CICILAN" sudah dicek ke pengguna).

## Keluaran script (asli, dijalankan ulang 2026-10-13)
```
# RINGKASAN SIAP TEMPEL (salin kalimat ini APA ADANYA - jangan menghitung/menafsir ulang)

> Gaji rutin Rp5.500.000/bulan, total pos Rp5.500.000/bulan -> sisa Rp0/bulan dari gaji; inilah batas setoran bulanan.
> Bonus proyek akhir tahun Rp10.000.000 cair SEKALI (bukan tiap bulan) - setor SEKALIGUS saat cair ke dana darurat/target; jangan ditambahkan ke setoran bulanan. Angka ini belum dikurangi kebutuhan Lebaran (mudik, baju, kue, angpau) - sebutkan berapa yang perlu disisihkan, nanti setoran THR dihitung ulang.
> Pengeluaran pokok Rp4.450.000/bulan -> target dana darurat 12 bulan = Rp53.400.000.
> Saldo dana darurat sekarang Rp12.000.000 -> 12 bulan: kurang Rp41.400.000 (progres 22%), tercapai 207 bulan (~17 th 3 bln) dengan setoran Rp200.000/bulan, atau 48 bulan (~4 th 0 bln) bila Bonus proyek akhir tahun Rp10.000.000 juga disetor tiap cair (cair pertama bulan ke-12, asumsi bawaan).

- PENGINGAT: --sisih-lebaran belum diisi (dianggap Rp0 = seluruh THR untuk dana darurat/defisit). Tanyakan kebutuhan Lebaran pengguna (mudik, baju, kue, angpau) lalu jalankan ulang dengan --sisih-lebaran; jangan menyuruh menyetor SELURUH THR tanpa menyebut hal ini.

# Anggaran Bulanan (zero-based)

## Pemasukan per bulan

| Sumber | Jumlah |
|---|---:|
| Penghasilan freelance (bulan terendah 6 bln) | Rp5.500.000 |
| Musiman dibagi 12 (Bonus proyek akhir tahun Rp10.000.000; total Rp10.000.000/th) | Rp833.333 |
| **Total pemasukan** | **Rp6.333.333** |

## Pos pengeluaran & alokasi

| Pos | Kelompok | Jumlah | % pemasukan rutin (Rp5.500.000) | % termasuk THR/12 (Rp6.333.333) |
|---|---|---:|---:|---:|
| Kos | Kebutuhan wajib | Rp1.500.000 | 27,3% | 23,7% |
| Makan & dapur | Kebutuhan wajib | Rp1.500.000 | 27,3% | 23,7% |
| Transport ojol/bensin | Kebutuhan wajib | Rp400.000 | 7,3% | 6,3% |
| Internet & pulsa | Kebutuhan wajib | Rp300.000 | 5,5% | 4,7% |
| BPJS Kesehatan mandiri kelas 2 | Kebutuhan wajib | Rp100.000 | 1,8% | 1,6% |
| Kiriman ibu | Keluarga & sosial/ibadah | Rp500.000 | 9,1% | 7,9% |
| Langganan software kerja | Kebutuhan wajib | Rp150.000 | 2,7% | 2,4% |
| Nongkrong & hiburan | Keinginan | Rp300.000 | 5,5% | 4,7% |
| Dana darurat | Tabungan, dana darurat & pelunasan ekstra | Rp200.000 | 3,6% | 3,2% |
| DP rumah | Tabungan, dana darurat & pelunasan ekstra | Rp550.000 | 10,0% | 8,7% |
| **Total dialokasikan** | | **Rp5.500.000** | 100,0% | 86,8% |
| **Belum dialokasikan** (termasuk THR/12 bila ada) | | **Rp833.333** | harus dijadikan 0 | |

- Saat menyebut persen ke pengguna, sebut basisnya: "% dari gaji rutin" (kolom pertama) atau "% termasuk THR/12" (kolom kedua). Jangan melabeli kolom kedua sebagai "% gaji".

## Banding pola 50/30/20 - basis pemasukan rutin Rp5.500.000/bulan

| Kelompok | Pola | Batas pola | Rencana kamu | Selisih |
|---|---:|---:|---:|---:|
| Kebutuhan (wajib + keluarga/sosial) | 50% | Rp2.750.000 | Rp4.450.000 | +Rp1.700.000 |
| Keinginan | 30% | Rp1.650.000 | Rp300.000 | -Rp1.350.000 |
| Tabungan & pelunasan ekstra | 20% | Rp1.100.000 | Rp750.000 | -Rp350.000 |

- Basis banding = gaji rutin (tanpa THR/12), sama dengan rasio cicilan. Bonus proyek akhir tahun Rp10.000.000 (sekali cair) di luar banding ini - jadikan setoran sekaligus ke dana darurat/target.

## Catatan

- Masih ada Rp833.333 belum punya tugas (Rp0 dari gaji tiap bulan + Rp833.333 bagian THR/bonus yang cair sekali Rp10.000.000). Zero-based: arahkan ke dana darurat, pelunasan utang berbunga tinggi, atau target tabungan sampai sisa Rp0.
- Kebutuhan melebihi batas pola. Wajar untuk keluarga dengan tanggungan atau kota mahal; coba pola 60/20/20 dan pastikan tabungan tetap ada.
- Tabungan di bawah pola. Mulai dari jumlah kecil yang rutin (bayar diri sendiri dulu di hari gajian).
- Pemasukan musiman (THR/bonus) dibagi 12 dan dibulatkan ke bawah HANYA untuk gambaran setahun. Uangnya cair sekali - lihat bagian 'Arus kas rutin vs musiman' untuk setoran bulanan yang benar-benar ada.

## Arus kas rutin vs musiman (THR/bonus)

| Arus | Per bulan | Kapan uangnya ada |
|---|---:|---|
| Pemasukan rutin (gaji bersih) | Rp5.500.000 | tiap bulan |
| Total pos dialokasikan | Rp5.500.000 | tiap bulan |
| **Sisa dari pemasukan rutin** | **Rp0** | tiap bulan |
| Bonus proyek akhir tahun (setara /12) | Rp833.333 | SEKALI saat cair: Rp10.000.000 |

- Setoran/transfer BULANAN (dana darurat, target, pelunasan ekstra) paling banyak **Rp0/bulan** - hanya dari gaji. Jangan menyebut sisa Rp833.333 sebagai uang yang bisa dipindah tiap bulan: Rp833.333 di dalamnya adalah bagian THR/bonus.
- Bonus proyek akhir tahun **Rp10.000.000** dicadangkan/disetor SEKALIGUS saat cair (mis. langsung ke dana darurat atau target). Itu setara Rp833.333 x 12 bulan - jangan ditambahkan lagi ke setoran bulanan (dihitung dua kali).
- Langkah aksi ke pengguna WAJIB memakai angka di tabel ini: setoran bulanan dari sisa rutin, THR/bonus sebagai setoran sekaligus saat cair.

## Dasar dana darurat (pengeluaran pokok per bulan)

| Pos DIMASUKKAN ke pokok | Jenis | Jumlah |
|---|---|---:|
| Kos | kebutuhan wajib | Rp1.500.000 |
| Makan & dapur | kebutuhan wajib | Rp1.500.000 |
| Transport ojol/bensin | kebutuhan wajib | Rp400.000 |
| Internet & pulsa | kebutuhan wajib | Rp300.000 |
| BPJS Kesehatan mandiri kelas 2 | kebutuhan wajib | Rp100.000 |
| Kiriman ibu | kewajiban rutin keluarga | Rp500.000 |
| Langganan software kerja | kebutuhan wajib | Rp150.000 |
| **Total pengeluaran pokok** | | **Rp4.450.000** |

| Pos DIKELUARKAN dari pokok | Jumlah | Alasan |
|---|---:|---|
| Nongkrong & hiburan | Rp300.000 | keinginan/jajan/hiburan, bisa dikurangi atau dihentikan saat darurat |
| Dana darurat | Rp200.000 | tabungan/dana darurat/pelunasan ekstra, bukan biaya hidup |
| DP rumah | Rp550.000 | tabungan/dana darurat/pelunasan ekstra, bukan biaya hidup |

- Pokok = Kebutuhan wajib + SEMUA cicilan/utang minimum (PayLater, kartu kredit, KPR, pinjol, leasing, KTA) + kewajiban rutin keluarga (kiriman orang tua/mertua/adik) - tetap harus dibayar walau penghasilan berhenti.
- Sebutkan ke pengguna pos yang dimasukkan DAN yang dikeluarkan beserta alasannya. Bila pengguna ingin mengubah, jalankan ulang dengan --pokok-juga "nama pos" atau --bukan-pokok "nama pos".
- Pakai angka ini untuk dana darurat: dana-darurat --pengeluaran-pokok 4450000 --status ...

## Skenario alternatif dasar dana darurat (siap salin - JANGAN hitung sendiri)

| Skenario | Pokok/bulan | 12 bulan |
|---|---:|---:|
| Sekarang (kiriman keluarga dimasukkan) | Rp4.450.000 | Rp53.400.000 |
| Tanpa Kiriman ibu (Rp500.000) | Rp3.950.000 | Rp47.400.000 |

Kalimat siap tempel:

> Bila Kiriman ibu (Rp500.000/bulan) bisa dihentikan saat darurat, pengeluaran pokok turun menjadi Rp3.950.000 dan target 12 bulan menjadi Rp47.400.000.

### Lama tercapai sekarang vs skenario (bulan) - setoran tetap Rp200.000/bulan; Rp10.000.000 sekali setahun mulai bulan ke-12

| Skenario | Target | Setoran saja: sekarang -> skenario | Selisih | + THR/bonus: sekarang -> skenario | Selisih |
|---|---|---|---|---|---|
| Tanpa Kiriman ibu | 12 bulan | 207 bulan -> 177 bulan | 30 bulan lebih cepat | 48 bulan -> 36 bulan | 12 bulan lebih cepat |

Kalimat siap tempel:

> Lama tercapai bila Kiriman ibu tidak dihitung (setoran tetap): target 12 bulan: setoran saja 207 bulan -> 177 bulan (30 bulan lebih cepat), dengan THR/bonus 48 bulan -> 36 bulan (12 bulan lebih cepat).

- Selisih waktu HANYA dari tabel ini, per kolom. Jangan meringkas menjadi "sekitar setahun lebih cepat" bila kolom-kolomnya berbeda (ada yang tidak berubah).

Bukan nasihat keuangan/investasi. Kasus rumit: konsultasikan ke perencana keuangan bersertifikat.

# Dana Darurat

- Status: Pekerja lepas/freelancer/pemilik usaha, penghasilan tidak tetap -> target 12 bulan pengeluaran pokok
- Pengeluaran pokok per bulan: Rp4.450.000 (rincian di bawah)
- Saldo sekarang: Rp12.000.000 | Setoran rutin (dari gaji): Rp200.000/bulan
- Setoran sekaligus THR/bonus: Rp10.000.000 sekali setahun, cair bulan ke-12 dari sekarang (asumsi bawaan; tanyakan bulan cairnya) - TIDAK termasuk dalam setoran rutin di atas
- PENGINGAT: --sisih-lebaran belum diisi (dianggap Rp0 = seluruh Rp10.000.000 ke dana darurat). Tanyakan kebutuhan Lebaran (mudik, baju, kue, angpau) lalu jalankan ulang dengan --sisih-lebaran.

| Target | Jumlah | Kekurangan | Lama tercapai (setoran rutin saja) | Lama tercapai (+ THR/bonus) | Progres |
|---|---:|---:|---:|---:|---:|
| 12 bulan | Rp53.400.000 | Rp41.400.000 | 207 bulan (~17 th 3 bln) | 48 bulan (~4 th 0 bln) | ####................ 22% |

| Pos DIMASUKKAN ke pokok | Jumlah |
|---|---:|
| Pengeluaran pokok (angka gabungan) | Rp3.950.000 |
| Kiriman ibu (kewajiban keluarga) | Rp500.000 |
| **Total pengeluaran pokok** | **Rp4.450.000** |

## Skenario alternatif dasar dana darurat (siap salin - JANGAN hitung sendiri)

| Skenario | Pokok/bulan | 12 bulan |
|---|---:|---:|
| Sekarang (kiriman keluarga dimasukkan) | Rp4.450.000 | Rp53.400.000 |
| Tanpa Kiriman ibu (Rp500.000) | Rp3.950.000 | Rp47.400.000 |

Kalimat siap tempel:

> Bila Kiriman ibu (Rp500.000/bulan) bisa dihentikan saat darurat, pengeluaran pokok turun menjadi Rp3.950.000 dan target 12 bulan menjadi Rp47.400.000.

### Lama tercapai sekarang vs skenario (bulan) - setoran tetap Rp200.000/bulan; Rp10.000.000 sekali setahun mulai bulan ke-12

| Skenario | Target | Setoran saja: sekarang -> skenario | Selisih | + THR/bonus: sekarang -> skenario | Selisih |
|---|---|---|---|---|---|
| Tanpa Kiriman ibu | 12 bulan | 207 bulan -> 177 bulan | 30 bulan lebih cepat | 48 bulan -> 36 bulan | 12 bulan lebih cepat |

Kalimat siap tempel:

> Lama tercapai bila Kiriman ibu tidak dihitung (setoran tetap): target 12 bulan: setoran saja 207 bulan -> 177 bulan (30 bulan lebih cepat), dengan THR/bonus 48 bulan -> 36 bulan (12 bulan lebih cepat).

- Selisih waktu HANYA dari tabel ini, per kolom. Jangan meringkas menjadi "sekitar setahun lebih cepat" bila kolom-kolomnya berbeda (ada yang tidak berubah).

Catatan:
- Pengeluaran pokok = yang tetap harus dibayar walau penghasilan berhenti (makan, tempat tinggal, listrik/air, transport, SEMUA cicilan/utang minimum, sekolah, BPJS, kiriman keluarga yang wajib). Bukan nongkrong/hiburan.
- CEK CICILAN: belum ada cicilan yang tercatat. Bila ada cicilan PayLater, kartu kredit, KPR, motor/leasing, KTA, atau pinjol, tambahkan (--cicilan "PayLater=650rb") - cicilan tetap wajib dibayar saat penghasilan berhenti, jadi masuk dasar dana darurat.
- Simpan di tempat terpisah yang aman dan cepat dicairkan (bukan instrumen yang nilainya naik-turun).
- Punya utang berbunga tinggi (kartu kredit/paylater/pinjol)? Kumpulkan dana darurat awal ~1 bulan pengeluaran pokok dulu, lalu fokus lunasi utang, baru lengkapi dana darurat.

Bukan nasihat keuangan/investasi. Kasus rumit: konsultasikan ke perencana keuangan bersertifikat.

# Target: DP rumah

| Asumsi | Nilai |
|---|---:|
| Biaya bila dibeli hari ini | Rp150.000.000 |
| Jangka waktu | 48 bulan (~4 th 0 bln) |
| Inflasi (asumsi, per tahun) | 4% |
| Imbal hasil tabungan (asumsi, per tahun) | 0% |
| Dana sudah terkumpul | Rp20.000.000 |

| Hasil | Nilai |
|---|---:|
| Perkiraan biaya saat dibutuhkan | **Rp175.979.800** |
| Dana terkumpul pada saat itu | Rp20.000.000 |
| **Tabungan yang dibutuhkan per bulan** | **Rp3.249.580** |

**Kurang Rp2.699.580 per bulan** dari kemampuan Rp550.000. Pilihan: perpanjang waktu, turunkan target, atau tambah pemasukan.
Dengan menabung Rp550.000/bulan, target TIDAK tercapai dalam 60 tahun (kenaikan biaya karena inflasi lebih cepat dari tabungan). Naikkan setoran atau turunkan target.

Rumus: biaya_nanti = biaya x (1 + inflasi/12)^bulan; tabungan/bulan = (biaya_nanti - terkumpul x (1+r)^bulan) x r / ((1+r)^bulan - 1), r = imbal/12 (jika r = 0: dibagi jumlah bulan). Setoran di akhir bulan, dibulatkan ke atas. Angka inflasi & imbal hasil adalah ASUMSI, bukan janji; tidak ada rekomendasi produk investasi.

Bukan nasihat keuangan/investasi. Kasus rumit: konsultasikan ke perencana keuangan bersertifikat.

# Target: DP rumah (skenario imbal 4,5%)

| Asumsi | Nilai |
|---|---:|
| Biaya bila dibeli hari ini | Rp150.000.000 |
| Jangka waktu | 48 bulan (~4 th 0 bln) |
| Inflasi (asumsi, per tahun) | 4% |
| Imbal hasil tabungan (asumsi, per tahun) | 4,5% |
| Dana sudah terkumpul | Rp20.000.000 |

| Hasil | Nilai |
|---|---:|
| Perkiraan biaya saat dibutuhkan | **Rp175.979.800** |
| Dana terkumpul pada saat itu | Rp23.936.288 |
| **Tabungan yang dibutuhkan per bulan** | **Rp2.896.959** |

**Kurang Rp2.346.959 per bulan** dari kemampuan Rp550.000. Pilihan: perpanjang waktu, turunkan target, atau tambah pemasukan.
**Dengan menabung Rp550.000/bulan, target tercapai di bulan ke-364 (~30 th 4 bln)**, saat biayanya diperkirakan Rp503.684.907 (asumsi inflasi & imbal hasil yang sama).

Rumus: biaya_nanti = biaya x (1 + inflasi/12)^bulan; tabungan/bulan = (biaya_nanti - terkumpul x (1+r)^bulan) x r / ((1+r)^bulan - 1), r = imbal/12 (jika r = 0: dibagi jumlah bulan). Setoran di akhir bulan, dibulatkan ke atas. Angka inflasi & imbal hasil adalah ASUMSI, bukan janji; tidak ada rekomendasi produk investasi.

Bukan nasihat keuangan/investasi. Kasus rumit: konsultasikan ke perencana keuangan bersertifikat.
```
Tuas perpanjang waktu (imbal 0%, inflasi 4%, terkumpul Rp20 jt; untuk ketiganya script juga menulis "Dengan menabung Rp550.000/bulan, target TIDAK tercapai dalam 60 tahun"):
| Jangka | Biaya nanti | Tabungan/bulan | Kurang dari kemampuan Rp550.000 |
|---|---:|---:|---:|
| 6 th | Rp190.611.282 | Rp2.369.602 | Rp1.819.602 |
| 7 th | Rp198.377.080 | Rp2.123.537 | Rp1.573.537 |
| 8 th | Rp206.459.268 | Rp1.942.285 | Rp1.392.285 |

## Jawaban akhir agent

## Ringkasan
Gaji rutin Rp5.500.000/bulan, total pos Rp5.500.000/bulan -> sisa Rp0/bulan dari gaji; inilah batas setoran bulanan (anggaran memakai bulan terendah 6 bulan terakhir; setoran DP dari penghasilan rutin Rp550.000/bulan). Masalahnya, DP Rp150 jt hari ini diperkirakan jadi **Rp175.979.800** dalam 4 tahun (inflasi 4%), sehingga butuh **Rp3.249.580/bulan** (atau Rp2.896.959 bila tabungan tumbuh 4,5%/th) — kurang Rp2.699.580 per bulan dari kemampuan Rp550.000, dan dengan Rp550.000/bulan saja target TIDAK tercapai dalam 60 tahun. Bonus proyek akhir tahun Rp10.000.000 cair SEKALI (bukan tiap bulan) - setor SEKALIGUS saat cair ke dana darurat/target; jangan ditambahkan ke setoran bulanan — langkah terpentingnya: kelebihan di bulan ramai dan bonus dipakai untuk dana darurat dan DP, bukan dibelanjakan.

## Anggaran (bulan sepi)
Banding pola 50/30/20 — basis penghasilan rutin Rp5.500.000/bulan (angka dari script):
| Kelompok | Batas pola | Rencana | Selisih |
|---|---:|---:|---:|
| Kebutuhan wajib + kiriman ibu | Rp2.750.000 | Rp4.450.000 | +Rp1.700.000 |
| Keinginan | Rp1.650.000 | Rp300.000 | -Rp1.350.000 |
| Tabungan (dana darurat Rp200.000 + DP Rp550.000) | Rp1.100.000 | Rp750.000 | -Rp350.000 |

## Dana Darurat (pekerja lepas → 12 bulan)
Pengeluaran pokok **Rp4.450.000** (dimasukkan: kos, makan, transport, internet & pulsa, BPJS, software kerja, kiriman ibu; dikeluarkan: nongkrong & hiburan, pos tabungan). Target 12 bulan **Rp53.400.000**; ada Rp12.000.000 (22%); dengan setoran Rp200.000/bulan saja butuh 207 bulan (~17 th 3 bln) — terlalu lama; bila bonus Rp10.000.000 juga disetor tiap cair, 48 bulan (~4 th 0 bln). Bila Kiriman ibu (Rp500.000/bulan) bisa dihentikan saat darurat, pengeluaran pokok turun menjadi Rp3.950.000 dan target 12 bulan menjadi Rp47.400.000. Karena penghasilan tidak tetap, dana darurat didahulukan: alokasikan **seluruh kelebihan bulan ramai ke dana darurat sampai minimal 6 bulan pengeluaran pokok**, lalu bagi 50:50 dengan DP.

## Target DP Rumah
| Skenario | Biaya nanti | Tabungan Rp20 jt jadi | Butuh/bulan | Dengan Rp550.000/bulan |
|---|---:|---:|---:|---|
| 4 th, imbal 0% | Rp175.979.800 | Rp20.000.000 | Rp3.249.580 | tidak tercapai dalam 60 tahun |
| 4 th, imbal 4,5% (asumsi Anda) | Rp175.979.800 | Rp23.936.288 | Rp2.896.959 | bulan ke-364 (~30 th 4 bln) |
| 6 th, imbal 0% | Rp190.611.282 | Rp20.000.000 | Rp2.369.602 | tidak tercapai dalam 60 tahun |
| 8 th, imbal 0% | Rp206.459.268 | Rp20.000.000 | Rp1.942.285 | tidak tercapai dalam 60 tahun |

Tiga tuas: (1) **tambah setoran dari bulan ramai dan bonus** — angka di atas belum memasukkan bonus Rp10.000.000/tahun (script target belum menghitung setoran tahunan); jalankan ulang script dengan setoran baru untuk melihat bulan tercapainya; (2) perpanjang waktu — dengan setoran Rp550.000 saja tidak cukup, tetap perlu tambahan setoran; (3) turunkan target (rumah lebih kecil / DP 10%). Catatan: dengan imbal 0% dan inflasi 4%, memperpanjang waktu hanya membantu pelan karena harga ikut naik.

## Asumsi yang dipakai
- Penghasilan rutin = bulan terendah 6 bulan terakhir (Rp5.500.000); bonus Rp10.000.000 cair sekali setahun, dianggap cair 12 bulan lagi (asumsi bawaan script, paling hati-hati) dan disetor sekaligus — tidak dibagi ke setoran bulanan.
- Inflasi harga rumah 4%/th (bisa lebih tinggi di lokasi tertentu); imbal 4,5% hanya skenario dari angka Anda, bukan janji atau rekomendasi produk.
- Setoran di akhir bulan, dibulatkan ke atas.

## Langkah minggu ini
1. Buat 3 kantong: operasional (Kebutuhan Rp4.450.000 + Keinginan Rp300.000), dana darurat (Rp200.000/bulan), DP rumah (Rp550.000/bulan).
2. Aturan bulan ramai: setiap rupiah di atas Rp5.500.000 (anggaran bulan sepi) → 100% dana darurat sampai minimal 6 bulan pengeluaran pokok.
3. Saat bonus akhir tahun Rp10.000.000 cair: sisihkan dulu kebutuhan akhir tahun/Lebaran bila ada, sisanya setor sekaligus ke dana darurat/DP — jangan "digaji"-kan ke setoran bulanan.
4. Cek harga rumah incaran & syarat DP (bisa 10–20%) agar angka target realistis.
5. Tinjau ulang rencana tiap 3 bulan.

⚠️ Bukan nasihat keuangan/investasi. Angka adalah simulasi dari data & asumsi di atas. Untuk kasus rumit, konsultasikan ke perencana keuangan bersertifikat.

## Penilaian penguji
- Verifikasi independen: biaya nanti 150.000.000 × (1+0,04/12)^48 = 175.979.800 ✓; PMT 0% = ceil(155.979.800/48) = 3.249.580 ✓; imbal 4,5%: FV terkumpul 23.936.287,5 → tampil 23.936.288 ✓, PMT 2.896.959 ✓; 6/7/8 tahun cocok semua.
- Ulang 2026-10-13 (dasar penghasilan rutin): sisa rutin 5.500.000 − 4.750.000 − 200.000 = 550.000 ✓; kurang 3.249.580 − 550.000 = 2.699.580 ✓, 2.896.959 − 550.000 = 2.346.959 ✓, tuas 6/7/8 th 1.819.602 / 1.573.537 / 1.392.285 ✓; dana darurat 41.400.000 ÷ 200.000 = 207 bulan ✓; dengan bonus tiap bulan ke-12: bulan 48 → 48 × 200.000 + 4 × 10.000.000 = 49.600.000 ≥ 41.400.000 (bulan 47: 39.400.000 <) ✓.
- Penghasilan tidak tetap memakai bulan terendah sesuai SKILL.md ✓; tidak ada rekomendasi produk (deposito hanya disebut pengguna) ✓.
- Temuan T-5 (versi awal: script tidak menghitung bulan tercapai) sudah diperbaiki sejak v1.0.1 — script kini mencetak bulan tercapai/tidak tercapai. Catatan pola 50/30/20 menyebut "wajar untuk keluarga dengan tanggungan" untuk pengguna lajang — teks generik (minor).
- **Hasil: LULUS.**
