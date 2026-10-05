# Uji 03 — Freelancer penghasilan naik-turun, target DP rumah Rp150 jt dalam 4 tahun

> Penguji independen, 2026-09-26. Keluaran asli script; target & dana darurat dicek ulang dengan rumus FV independen penguji.

## Input pengguna
"Saya desainer freelance, lajang, ngekos di Jogja. Penghasilan 6 bulan terakhir: 9 jt, 6,5 jt, 12 jt, 7 jt, 5,5 jt, 10 jt. Biasanya ada bonus proyek akhir tahun sekitar 10 jt (anggap 'THR' saya). Pengeluaran: kos 1,5 jt, makan 1,5 jt, transport 400 rb, internet+pulsa 300 rb, BPJS mandiri 100 rb, software 150 rb, kirim ibu 500 rb, nongkrong 300 rb. Dana darurat sudah 12 jt, DP rumah sudah ada 20 jt. Pengen DP rumah 150 jt dalam 4 tahun. Uang tabungan saya di deposito, bunganya kira-kira 4,5% setahun."

## Perintah yang dijalankan agent
```
python3 scripts/keuangan.py anggaran --pemasukan "Penghasilan freelance (bulan terendah 6 bln)=5,5jt" \
  --musiman "Bonus proyek akhir tahun=10jt" --pos "Kos=1,5jt:wajib" --pos "Makan & dapur=1,5jt:wajib" \
  --pos "Transport ojol/bensin=400rb:wajib" --pos "Internet & pulsa=300rb:wajib" \
  --pos "BPJS Kesehatan mandiri kelas 2=100rb:wajib" --pos "Kiriman ibu=500rb:sosial" \
  --pos "Langganan software kerja=150rb:wajib" --pos "Nongkrong & hiburan=300rb:keinginan" \
  --pos "Dana darurat=200rb:tabungan" --pos "DP rumah=1.383.333:tabungan"
python3 scripts/keuangan.py dana-darurat --pengeluaran-pokok 4,3jt --status lepas --saldo 12jt --setoran 200rb
python3 scripts/keuangan.py target --nama "DP rumah" --jenis rumah --biaya-sekarang 150jt --tahun 4 --terkumpul 20jt --kemampuan 1.383.333
python3 scripts/keuangan.py target --nama "DP rumah (skenario imbal 4,5%)" --jenis rumah --biaya-sekarang 150jt --tahun 4 --imbal 4,5 --terkumpul 20jt --kemampuan 1.383.333
python3 scripts/keuangan.py target --nama "DP" --biaya-sekarang 150jt --tahun {6,7,8} --terkumpul 20jt --kemampuan 1.383.333   # tuas "perpanjang waktu"
```
(Imbal 4,5% dipakai hanya sebagai skenario karena pengguna sendiri menyebut angkanya — sesuai SKILL.md.)

## Keluaran script (asli)
```
# Anggaran Bulanan (zero-based)

## Pemasukan per bulan

| Sumber | Jumlah |
|---|---:|
| Penghasilan freelance (bulan terendah 6 bln) | Rp5.500.000 |
| Musiman dibagi 12 (Bonus proyek akhir tahun Rp10.000.000; total Rp10.000.000/th) | Rp833.333 |
| **Total pemasukan** | **Rp6.333.333** |

## Pos pengeluaran & alokasi

| Pos | Kelompok | Jumlah | % pemasukan |
|---|---|---:|---:|
| Kos | Kebutuhan wajib | Rp1.500.000 | 23,7% |
| Makan & dapur | Kebutuhan wajib | Rp1.500.000 | 23,7% |
| Transport ojol/bensin | Kebutuhan wajib | Rp400.000 | 6,3% |
| Internet & pulsa | Kebutuhan wajib | Rp300.000 | 4,7% |
| BPJS Kesehatan mandiri kelas 2 | Kebutuhan wajib | Rp100.000 | 1,6% |
| Kiriman ibu | Keluarga & sosial/ibadah | Rp500.000 | 7,9% |
| Langganan software kerja | Kebutuhan wajib | Rp150.000 | 2,4% |
| Nongkrong & hiburan | Keinginan | Rp300.000 | 4,7% |
| Dana darurat | Tabungan, dana darurat & pelunasan ekstra | Rp200.000 | 3,2% |
| DP rumah | Tabungan, dana darurat & pelunasan ekstra | Rp1.383.333 | 21,8% |
| **Total dialokasikan** | | **Rp6.333.333** | 100,0% |
| **Sisa** | | **Rp0** | zero-based tercapai |

## Banding pola 50/30/20

| Kelompok | Pola | Batas pola | Rencana kamu | Selisih |
|---|---:|---:|---:|---:|
| Kebutuhan (wajib + keluarga/sosial) | 50% | Rp3.166.667 | Rp4.450.000 | +Rp1.283.333 |
| Keinginan | 30% | Rp1.900.000 | Rp300.000 | -Rp1.600.000 |
| Tabungan & pelunasan ekstra | 20% | Rp1.266.667 | Rp1.583.333 | +Rp316.666 |

## Catatan

- Kebutuhan melebihi batas pola. Wajar untuk keluarga dengan tanggungan atau kota mahal; coba pola 60/20/20 dan pastikan tabungan tetap ada.
- Pemasukan musiman (THR/bonus) dibagi 12 dan dibulatkan ke bawah. Simpan saat cair, lalu 'gaji'-kan ke anggaran tiap bulan; jangan dianggap uang bebas.

Bukan nasihat keuangan/investasi. Kasus rumit: konsultasikan ke perencana keuangan bersertifikat.

# Dana Darurat

- Status: Pekerja lepas/freelancer/pemilik usaha, penghasilan tidak tetap -> target 12 bulan pengeluaran pokok
- Pengeluaran pokok per bulan: Rp4.300.000
- Saldo sekarang: Rp12.000.000 | Setoran rutin: Rp200.000/bulan

| Target | Jumlah | Kekurangan | Lama tercapai | Progres |
|---|---:|---:|---:|---:|
| 12 bulan | Rp51.600.000 | Rp39.600.000 | 198 bulan (~16 th 6 bln) | ####................ 23% |

Catatan:
- Pengeluaran pokok = yang tetap harus dibayar walau penghasilan berhenti (makan, tempat tinggal, listrik/air, transport, cicilan minimum, sekolah, BPJS, kiriman keluarga yang wajib). Bukan nongkrong/hiburan.
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

**Kurang Rp1.866.247 per bulan** dari kemampuan Rp1.383.333. Pilihan: perpanjang waktu, turunkan target, atau tambah pemasukan.

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

**Kurang Rp1.513.626 per bulan** dari kemampuan Rp1.383.333. Pilihan: perpanjang waktu, turunkan target, atau tambah pemasukan.

Rumus: biaya_nanti = biaya x (1 + inflasi/12)^bulan; tabungan/bulan = (biaya_nanti - terkumpul x (1+r)^bulan) x r / ((1+r)^bulan - 1), r = imbal/12 (jika r = 0: dibagi jumlah bulan). Setoran di akhir bulan, dibulatkan ke atas. Angka inflasi & imbal hasil adalah ASUMSI, bukan janji; tidak ada rekomendasi produk investasi.

Bukan nasihat keuangan/investasi. Kasus rumit: konsultasikan ke perencana keuangan bersertifikat.
```
Tuas perpanjang waktu (imbal 0%, inflasi 4%, terkumpul Rp20 jt):
| Jangka | Biaya nanti | Tabungan/bulan | Kurang dari kemampuan Rp1.383.333 |
|---|---:|---:|---:|
| 6 th | Rp190.611.282 | Rp2.369.602 | Rp986.269 |
| 7 th | Rp198.377.080 | Rp2.123.537 | Rp740.204 |
| 8 th | Rp206.459.268 | Rp1.942.285 | Rp558.952 |

## Jawaban akhir agent

## Ringkasan
Anggaran disusun dari bulan terendah Rp5,5 jt + bonus ÷ 12 = Rp6.333.333, dan sudah habis dibagi (sisa Rp0) dengan Rp1.383.333 untuk DP rumah. Masalahnya, DP Rp150 jt hari ini diperkirakan jadi **Rp175.979.800** dalam 4 tahun (inflasi 4%), sehingga butuh **Rp3.249.580/bulan** (atau Rp2.896.959 bila tabungan tumbuh 4,5%/th) — kurang ±Rp1,5–1,9 jt dari kemampuan bulan sepi. Langkah terpenting: kelebihan di bulan ramai (rata-rata 6 bulan terakhir Rp8,33 jt, ±Rp2 jt di atas bulan terendah) dibagi untuk dana darurat dan DP, bukan dibelanjakan.

## Anggaran (bulan sepi)
| Kelompok | Jumlah | Pola 50/30/20 |
|---|---:|---:|
| Kebutuhan wajib + kiriman ibu | Rp4.450.000 (70%) | batas Rp3.166.667 |
| Keinginan | Rp300.000 (5%) | batas Rp1.900.000 |
| Tabungan (dana darurat Rp200.000 + DP Rp1.383.333) | Rp1.583.333 (25%) | min Rp1.266.667 |

## Dana Darurat (pekerja lepas → 12 bulan)
Target 12 × Rp4.300.000 = **Rp51.600.000**; ada Rp12 jt (23%); dengan setoran Rp200.000 butuh 198 bulan — terlalu lama. Karena penghasilan tidak tetap, dana darurat didahulukan: alokasikan **seluruh kelebihan bulan ramai ke dana darurat sampai minimal 6 bulan (Rp25,8 jt)**, lalu bagi 50:50 dengan DP.

## Target DP Rumah
| Skenario | Biaya nanti | Tabungan Rp20 jt jadi | Butuh/bulan |
|---|---:|---:|---:|
| 4 th, imbal 0% | Rp175.979.800 | Rp20.000.000 | Rp3.249.580 |
| 4 th, imbal 4,5% (asumsi Anda) | Rp175.979.800 | Rp23.936.288 | Rp2.896.959 |
| 6 th, imbal 0% | Rp190.611.282 | Rp20.000.000 | Rp2.369.602 |
| 8 th, imbal 0% | Rp206.459.268 | Rp20.000.000 | Rp1.942.285 |

Tiga tuas: (1) **tambah setoran dari bulan ramai** — bila rata-rata Rp1,5 jt/bulan ekstra masuk DP, target 4 tahun hampir tercapai; (2) perpanjang ke 6–7 tahun; (3) turunkan target (rumah lebih kecil / DP 10%). Catatan: dengan imbal 0% dan inflasi 4%, memperpanjang waktu hanya membantu pelan karena harga ikut naik.

## Asumsi yang dipakai
- Pemasukan = bulan terendah 6 bulan (Rp5,5 jt) + bonus Rp10 jt ÷ 12 (dibulatkan ke bawah).
- Inflasi harga rumah 4%/th (bisa lebih tinggi di lokasi tertentu); imbal 4,5% hanya skenario dari angka Anda, bukan janji atau rekomendasi produk.
- Setoran di akhir bulan, dibulatkan ke atas.

## Langkah minggu ini
1. Buat 3 kantong: operasional (Rp4,75 jt), dana darurat, DP rumah.
2. Aturan bulan ramai: setiap rupiah di atas Rp6,33 jt → 100% dana darurat sampai Rp25,8 jt.
3. Simpan bonus akhir tahun di rekening terpisah, "gaji"-kan Rp833.333/bulan.
4. Cek harga rumah incaran & syarat DP (bisa 10–20%) agar angka target realistis.
5. Tinjau ulang rencana tiap 3 bulan.

⚠️ Bukan nasihat keuangan/investasi. Angka adalah simulasi dari data & asumsi di atas. Untuk kasus rumit, konsultasikan ke perencana keuangan bersertifikat.

## Penilaian penguji
- Verifikasi independen: biaya nanti 150.000.000 × (1+0,04/12)^48 = 175.979.800 ✓; PMT 0% = ceil(155.979.800/48) = 3.249.580 ✓; imbal 4,5%: FV terkumpul 23.936.287,5 → tampil 23.936.288 ✓, PMT 2.896.959 ✓; 6/7/8 tahun cocok semua; dana darurat 39.600.000 ÷ 200.000 = 198 ✓.
- Penghasilan tidak tetap memakai bulan terendah sesuai SKILL.md ✓; tidak ada rekomendasi produk (deposito hanya disebut pengguna) ✓.
- Kekurangan: script tidak menghitung "berapa bulan tercapai dengan kemampuan X" — agent harus coba-coba `--tahun` (temuan T-5). Catatan pola 50/30/20 menyebut "wajar untuk keluarga dengan tanggungan" untuk pengguna lajang — teks generik (minor).
- **Hasil: LULUS.**
