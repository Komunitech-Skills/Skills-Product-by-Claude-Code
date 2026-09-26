# Uji 01 — Keluarga muda Bekasi: anggaran bulanan + dana darurat

> Penguji independen (Tahap 6), 2026-09-26. Skill dijalankan dari salinan di scratchpad; semua angka di bawah keluaran asli `scripts/keuangan.py`, lalu dicek ulang dengan simulasi independen penguji (lihat HASIL-UJI.md).

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
  --pos "Dana darurat=1.371.666:tabungan" --pos "Dana pendidikan anak=500rb:tabungan" --pola 60/20/20
python3 scripts/keuangan.py dana-darurat --pengeluaran-pokok 10.850.000 --status anak --saldo 8jt --setoran "1.371.666"
```
Catatan proses: percobaan pertama (tanpa label dan dengan pos dana darurat Rp1.000.000) menyisakan **Rp371.666 belum bertugas** dan beberapa pos ditandai "(tebakan)"; agent memindahkan sisa itu ke dana darurat dan memberi label eksplisit → sisa Rp0. Pengeluaran pokok untuk dana darurat = Kebutuhan wajib + kiriman orang tua (Rp11.200.000 − sedekah Rp200.000 − kondangan Rp150.000 = Rp10.850.000).

## Keluaran script (asli)
```
# Anggaran Bulanan (zero-based)

## Pemasukan per bulan

| Sumber | Jumlah |
|---|---:|
| Gaji suami | Rp8.500.000 |
| Gaji istri | Rp4.000.000 |
| Musiman dibagi 12 (THR suami Rp8.500.000, THR istri Rp4.000.000; total Rp12.500.000/th) | Rp1.041.666 |
| **Total pemasukan** | **Rp13.541.666** |

## Pos pengeluaran & alokasi

| Pos | Kelompok | Jumlah | % pemasukan |
|---|---|---:|---:|
| Cicilan KPR | Kebutuhan wajib | Rp3.100.000 | 22,9% |
| Cicilan motor | Kebutuhan wajib | Rp1.200.000 | 8,9% |
| Listrik token+PDAM+gas | Kebutuhan wajib | Rp650.000 | 4,8% |
| Belanja dapur | Kebutuhan wajib | Rp2.200.000 | 16,2% |
| Susu & popok anak | Kebutuhan wajib | Rp750.000 | 5,5% |
| Daycare | Kebutuhan wajib | Rp1.000.000 | 7,4% |
| Bensin+tol+parkir | Kebutuhan wajib | Rp600.000 | 4,4% |
| Pulsa & internet rumah | Kebutuhan wajib | Rp350.000 | 2,6% |
| Kiriman orang tua | Keluarga & sosial/ibadah | Rp1.000.000 | 7,4% |
| Sedekah/infak | Keluarga & sosial/ibadah | Rp200.000 | 1,5% |
| Kondangan | Keluarga & sosial/ibadah | Rp150.000 | 1,1% |
| Makan di luar | Keinginan | Rp400.000 | 3,0% |
| Langganan streaming | Keinginan | Rp70.000 | 0,5% |
| Dana darurat | Tabungan, dana darurat & pelunasan ekstra | Rp1.371.666 | 10,1% |
| Dana pendidikan anak | Tabungan, dana darurat & pelunasan ekstra | Rp500.000 | 3,7% |
| **Total dialokasikan** | | **Rp13.541.666** | 100,0% |
| **Sisa** | | **Rp0** | zero-based tercapai |

## Banding pola 60/20/20

| Kelompok | Pola | Batas pola | Rencana kamu | Selisih |
|---|---:|---:|---:|---:|
| Kebutuhan (wajib + keluarga/sosial) | 60% | Rp8.125.000 | Rp11.200.000 | +Rp3.075.000 |
| Keinginan | 20% | Rp2.708.333 | Rp470.000 | -Rp2.238.333 |
| Tabungan & pelunasan ekstra | 20% | Rp2.708.333 | Rp1.871.666 | -Rp836.667 |

## Catatan

- Kebutuhan tetap melebihi batas pola 60%. Cek pos terbesar (tempat tinggal, cicilan, dapur) dan jangan menambah cicilan baru; tabungan sekecil apa pun tetap jalan.
- Tabungan di bawah pola. Mulai dari jumlah kecil yang rutin (bayar diri sendiri dulu di hari gajian).
- Total cicilan Rp4.300.000 = 31,8% dari pemasukan. DI ATAS patokan umum 30% - jangan menambah utang baru; pertimbangkan subperintah utang.
- Pemasukan musiman (THR/bonus) dibagi 12 dan dibulatkan ke bawah. Simpan saat cair, lalu 'gaji'-kan ke anggaran tiap bulan; jangan dianggap uang bebas.

Bukan nasihat keuangan/investasi. Kasus rumit: konsultasikan ke perencana keuangan bersertifikat.

# Dana Darurat

- Status: Menikah/orang tua tunggal dengan anak atau tanggungan -> target 9-12 bulan pengeluaran pokok
- Pengeluaran pokok per bulan: Rp10.850.000
- Saldo sekarang: Rp8.000.000 | Setoran rutin: Rp1.371.666/bulan

| Target | Jumlah | Kekurangan | Lama tercapai | Progres |
|---|---:|---:|---:|---:|
| 9 bulan | Rp97.650.000 | Rp89.650.000 | 66 bulan (~5 th 6 bln) | #................... 8% |
| 12 bulan | Rp130.200.000 | Rp122.200.000 | 90 bulan (~7 th 6 bln) | #................... 6% |

Catatan:
- Pengeluaran pokok = yang tetap harus dibayar walau penghasilan berhenti (makan, tempat tinggal, listrik/air, transport, cicilan minimum, sekolah, BPJS, kiriman keluarga yang wajib). Bukan nongkrong/hiburan.
- Simpan di tempat terpisah yang aman dan cepat dicairkan (bukan instrumen yang nilainya naik-turun).
- Punya utang berbunga tinggi (kartu kredit/paylater/pinjol)? Kumpulkan dana darurat awal ~1 bulan pengeluaran pokok dulu, lalu fokus lunasi utang, baru lengkapi dana darurat.

Bukan nasihat keuangan/investasi. Kasus rumit: konsultasikan ke perencana keuangan bersertifikat.
```

## Jawaban akhir agent (sesuai format SKILL.md)

## Ringkasan
Pemasukan keluarga Rp13.541.666/bulan (gaji + THR dibagi 12) sudah dibagi habis sampai sisa Rp0. Masalah utamanya: cicilan KPR + motor Rp4,3 juta = 31,8% pemasukan (sedikit di atas patokan 30%) sehingga pos kebutuhan jauh di atas pola 60%. Langkah terpenting: jangan ambil cicilan baru, sisihkan dana darurat Rp1.371.666 di hari gajian, dan simpan THR di rekening terpisah untuk "digaji"-kan tiap bulan.

## Anggaran
| Kelompok | Jumlah | % pemasukan |
|---|---:|---:|
| Kebutuhan wajib (KPR, motor, dapur, listrik, anak, daycare, transport, internet) | Rp9.850.000 | 72,7% |
| Keluarga & sosial (kiriman ortu, sedekah, kondangan) | Rp1.350.000 | 10,0% |
| Keinginan (makan di luar, streaming) | Rp470.000 | 3,5% |
| Tabungan (dana darurat Rp1.371.666 + pendidikan anak Rp500.000) | Rp1.871.666 | 13,8% |
| **Total** | **Rp13.541.666** | **100%** — sisa **Rp0** |

Banding pola 60/20/20: kebutuhan +Rp3.075.000 di atas batas, keinginan sudah sangat hemat (Rp470.000 vs batas Rp2.708.333), tabungan kurang Rp836.667 dari 20%. Artinya ruang potong keinginan hampir habis — perbaikan harus datang dari tambah pemasukan atau (nanti) cicilan motor lunas.

## Dana Darurat
Status: menikah + 1 anak → target 9–12 bulan pengeluaran pokok (Rp10.850.000).
| Target | Jumlah | Kekurangan | Lama dengan setoran Rp1.371.666 |
|---|---:|---:|---:|
| 9 bulan | Rp97.650.000 | Rp89.650.000 | 66 bulan (±5 th 6 bln) |
| 12 bulan | Rp130.200.000 | Rp122.200.000 | 90 bulan (±7 th 6 bln) |

Angka 5,5 tahun memang lama. Percepat dengan: (1) begitu cicilan motor lunas, alihkan Rp1,2 juta ke dana darurat (setoran jadi ±Rp2,57 juta); (2) sebagian THR/bonus di luar kebutuhan Lebaran langsung masuk dana darurat; (3) tahap pertama cukup kejar 3 bulan (Rp32,55 juta) dulu.

## Asumsi yang dipakai
- THR 1x gaji masing-masing, dibagi 12 dan dibulatkan ke bawah (Rp1.041.666).
- Pola pembanding 60/20/20 (keluarga dengan anak & kiriman ortu).
- Pengeluaran pokok tidak termasuk sedekah & kondangan (bisa ditunda saat darurat); kiriman ortu tetap dihitung.
- BPJS Kesehatan dianggap dipotong kantor (tidak ada di pos). Bila mandiri, tambahkan.

## Langkah minggu ini
1. Buka rekening/kantong terpisah khusus dana darurat; atur autodebet Rp1.371.666 tanggal gajian.
2. Pisahkan Rp500.000 dana pendidikan anak di kantong lain.
3. Catat pengeluaran e-wallet sebulan ini menurut pemakaian (top-up bukan pengeluaran).
4. Sepakati suami-istri: tidak ada cicilan/paylater baru sampai cicilan < 30%.
5. Saat THR cair, simpan di rekening terpisah; ambil Rp1.041.666 per bulan.

⚠️ Bukan nasihat keuangan/investasi. Angka adalah simulasi dari data & asumsi di atas. Untuk kasus rumit, konsultasikan ke perencana keuangan bersertifikat.

## Penilaian penguji
- Angka dicek manual: 12.500.000 ÷ 12 = 1.041.666,67 → 1.041.666 ✓; rasio cicilan 4.300.000 ÷ 13.541.666 = 31,75% ✓; 89.650.000 ÷ 1.371.666 = 65,36 → 66 bulan ✓; 122.200.000 ÷ 1.371.666 = 89,09 → 90 ✓.
- Kategori khas Indonesia (kiriman ortu, kondangan, sedekah opsional, THR ÷ 12) tertangani. Pos tanpa label ditebak dan **ditandai "(tebakan)"** — baik.
- Catatan kecil: pada pola 60/20/20 script menampilkan catatan "Kebutuhan tetap melebihi batas pola 60%" — tepat. Script tidak menghitung simulasi "setelah motor lunas", agent menyimpulkannya sendiri (wajar).
- **Hasil: LULUS.**
