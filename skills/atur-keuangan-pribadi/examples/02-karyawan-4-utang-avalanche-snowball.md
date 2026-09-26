# Uji 02 — Karyawan dengan 4 utang: Avalanche vs Snowball

> Penguji independen, 2026-09-26. Keluaran asli `scripts/keuangan.py`; semua angka dicocokkan dengan simulasi Fraction independen penguji (HASIL-UJI.md §4).

## Input pengguna
"Saya karyawan, utang saya: kartu kredit 12 juta (bunga 1,75%/bulan, minimum 5%), KTA 30 juta bunga flat 0,9% per bulan 24 bulan (baru mulai), paylater 3 juta, pinjol legal 2 juta. Tiap bulan saya bisa sisihkan 2,5 juta lebih di luar cicilan. Mana dulu yang harus dilunasi, avalanche atau snowball? Kapan lunas?"

## Data yang dilengkapi agent (ditanyakan sekali, dijawab pengguna)
- Paylater: bunga 2,5%/bulan, cicilan minimum Rp300.000.
- Pinjol legal: bunga 0,1%/hari (batas OJK 2026), cicilan Rp500.000.
- KTA: pokok awal Rp30 jt, belum ada cicilan yang dibayar.
- Minimum kartu kredit 5% × Rp12 jt = Rp600.000 (script memakai minimum tetap; lihat catatan penguji).

## Langkah 1 — KTA flat → efektif
```
python3 scripts/keuangan.py konversi-flat --pokok 30jt --bunga-flat 10,8 --tenor 24
```
(agent mengubah 0,9%/bulan flat → 10,8%/tahun karena `--bunga-flat` hanya menerima persen per tahun; lihat temuan T-1)
```
# Konversi Bunga Flat -> Efektif

- Pokok Rp30.000.000, bunga flat 10,8%/tahun, tenor 24 bulan
- Rumus flat: cicilan = pokok/tenor + pokok x bunga_flat/12 = Rp1.250.000 + Rp270.000 = **Rp1.520.000**
- Total dibayar Rp36.480.000 | total bunga Rp6.480.000
- **Bunga efektif setara: 1,628%/bulan = 19,53%/tahun**

Artinya: pinjaman ini sama mahalnya dengan pinjaman berbunga efektif 19,53%/tahun (bunga dihitung dari sisa pokok). Bandingkan penawaran selalu dengan bunga EFEKTIF, bukan flat.

Bukan nasihat keuangan/investasi. Kasus rumit: konsultasikan ke perencana keuangan bersertifikat.
```

## Langkah 2 — simulasi pelunasan
```
python3 scripts/keuangan.py utang --utang "Kartu kredit;12jt;1,75%/bln;600rb;kk" \
  --utang "KTA;30jt;1,628%/bln;1.520.000;kta" --utang "Paylater;3jt;2,5%/bln;300rb;paylater" \
  --utang "Pinjol legal;2jt;0,1%/hari;500rb;pinjol" --ekstra 2,5jt --metode banding
```
(Pada percobaan pertama nama utang ditulis "KTA (flat 0,9%/bln -> efektif)"; hasil identik.)
```
# Rencana Pelunasan Utang

- Total cicilan minimum: Rp2.920.000 | Anggaran pelunasan: Rp5.420.000/bulan (ekstra Rp2.500.000)
- Asumsi: bunga dihitung dari sisa saldo tiap bulan (efektif), dibulatkan ke rupiah terdekat; bunga per tahun dibagi 12, per hari dikali 30; tidak ada utang/belanja baru, denda, atau biaya lain; anggaran tetap dan cicilan minimum utang yang lunas dialihkan ke utang berikutnya.

## PERINGATAN

- 'KTA': bila bunganya FLAT, ubah dulu ke bunga efektif dengan subperintah konversi-flat; simulasi ini menghitung bunga dari SISA saldo (efektif).

## AVALANCHE (bunga tertinggi dulu)

Urutan serangan: Pinjol legal -> Paylater -> Kartu kredit -> KTA

| Utang | Saldo awal | Bunga | Lunas bulan ke- | Total bunga |
|---|---:|---|---:|---:|
| Kartu kredit | Rp12.000.000 | 1,75% per bulan | 5 | Rp730.469 |
| KTA | Rp30.000.000 | 1,628% per bulan | 10 | Rp3.315.551 |
| Paylater | Rp3.000.000 | 2,5% per bulan | 2 | Rp120.875 |
| Pinjol legal | Rp2.000.000 | 0,1% per hari (dihitung 30 hari/bulan) | 1 | Rp60.000 |

**Semua lunas dalam 10 bulan (~0 th 10 bln). Total bunga Rp4.226.895. Total dibayar Rp51.226.895.**

## SNOWBALL (saldo terkecil dulu)

Urutan serangan: Pinjol legal -> Paylater -> Kartu kredit -> KTA

| Utang | Saldo awal | Bunga | Lunas bulan ke- | Total bunga |
|---|---:|---|---:|---:|
| Kartu kredit | Rp12.000.000 | 1,75% per bulan | 5 | Rp730.469 |
| KTA | Rp30.000.000 | 1,628% per bulan | 10 | Rp3.315.551 |
| Paylater | Rp3.000.000 | 2,5% per bulan | 2 | Rp120.875 |
| Pinjol legal | Rp2.000.000 | 0,1% per hari (dihitung 30 hari/bulan) | 1 | Rp60.000 |

**Semua lunas dalam 10 bulan (~0 th 10 bln). Total bunga Rp4.226.895. Total dibayar Rp51.226.895.**

## Banding

- Avalanche menghemat bunga Rp0 dibanding Snowball; lama lunas 10 vs 10 bulan.
- Utang pertama lunas: bulan ke-1 (Avalanche) vs bulan ke-1 (Snowball).
- Kedua metode sama biayanya untuk kasus ini; pilih yang paling mudah dijalani.

Jangan menutup utang dengan utang baru (gali lubang tutup lubang). Kesulitan bayar? Hubungi kreditur untuk restrukturisasi secara resmi; pengaduan: Kontak OJK 157.

Bukan nasihat keuangan/investasi. Kasus rumit: konsultasikan ke perencana keuangan bersertifikat.
```

Jadwal lengkap (`--jadwal`, Avalanche) — dipakai penguji untuk cek per baris:
```
### Jadwal bulanan (avalanche)

| Bulan | Utang | Bayar | Bunga | Pokok | Sisa saldo |
|---:|---|---:|---:|---:|---:|
| 1 | Kartu kredit | Rp600.000 | Rp210.000 | Rp390.000 | Rp11.610.000 |
| 1 | KTA | Rp1.520.000 | Rp488.400 | Rp1.031.600 | Rp28.968.400 |
| 1 | Paylater | Rp1.240.000 | Rp75.000 | Rp1.165.000 | Rp1.835.000 |
| 1 | Pinjol legal | Rp2.060.000 | Rp60.000 | Rp2.000.000 | Rp0 |
| 2 | Kartu kredit | Rp2.019.125 | Rp203.175 | Rp1.815.950 | Rp9.794.050 |
| 2 | KTA | Rp1.520.000 | Rp471.606 | Rp1.048.394 | Rp27.920.006 |
| 2 | Paylater | Rp1.880.875 | Rp45.875 | Rp1.835.000 | Rp0 |
| 3 | Kartu kredit | Rp3.900.000 | Rp171.396 | Rp3.728.604 | Rp6.065.446 |
| 3 | KTA | Rp1.520.000 | Rp454.538 | Rp1.065.462 | Rp26.854.544 |
| 4 | Kartu kredit | Rp3.900.000 | Rp106.145 | Rp3.793.855 | Rp2.271.591 |
| 4 | KTA | Rp1.520.000 | Rp437.192 | Rp1.082.808 | Rp25.771.736 |
| 5 | Kartu kredit | Rp2.311.344 | Rp39.753 | Rp2.271.591 | Rp0 |
| 5 | KTA | Rp3.108.656 | Rp419.564 | Rp2.689.092 | Rp23.082.644 |
| 6 | KTA | Rp5.420.000 | Rp375.785 | Rp5.044.215 | Rp18.038.429 |
| 7 | KTA | Rp5.420.000 | Rp293.666 | Rp5.126.334 | Rp12.912.095 |
| 8 | KTA | Rp5.420.000 | Rp210.209 | Rp5.209.791 | Rp7.702.304 |
| 9 | KTA | Rp5.420.000 | Rp125.394 | Rp5.294.606 | Rp2.407.698 |
| 10 | KTA | Rp2.446.895 | Rp39.197 | Rp2.407.698 | Rp0 |
```

## Jawaban akhir agent

## Ringkasan
Total utang Rp47 juta dengan anggaran pelunasan Rp5.420.000/bulan (minimum Rp2.920.000 + ekstra Rp2.500.000). Kabar baiknya: kalau disiplin dan **tidak menambah utang baru**, semuanya lunas dalam **10 bulan** dengan total bunga **Rp4.226.895**. Langkah terpenting: lunasi pinjol bulan ini juga, lalu paylater, kartu kredit, dan terakhir KTA.

## Rencana Pelunasan
KTA "flat 0,9%/bulan" sebenarnya setara **bunga efektif 1,628%/bulan (19,53%/tahun)** — hampir dua kali angka flatnya per tahun (10,8%).

| Urutan | Utang | Bunga efektif/bulan | Lunas bulan ke- | Total bunga |
|---:|---|---:|---:|---:|
| 1 | Pinjol legal Rp2.000.000 | 3,00% | 1 | Rp60.000 |
| 2 | Paylater Rp3.000.000 | 2,50% | 2 | Rp120.875 |
| 3 | Kartu kredit Rp12.000.000 | 1,75% | 5 | Rp730.469 |
| 4 | KTA Rp30.000.000 | 1,628% | 10 | Rp3.315.551 |
| | **Total** | | **10** | **Rp4.226.895** |

**Avalanche vs Snowball:** untuk utang Anda, urutannya **kebetulan sama** (utang terkecil juga yang bunganya tertinggi), jadi dua metode menghasilkan angka identik — tidak perlu bingung memilih. Kemenangan pertama: pinjol lunas bulan pertama.

## Asumsi yang dipakai
- Bunga dihitung dari sisa saldo tiap bulan, dibulatkan ke rupiah; 0,1%/hari × 30 = 3%/bulan.
- Minimum kartu kredit dianggap tetap Rp600.000 (aslinya 5% dari tagihan, makin kecil saat saldo turun — karena total anggaran tetap Rp5,42 jt, hasilnya praktis sama: selisih penguji Rp90).
- KTA dilunasi lebih cepat mulai bulan ke-5; **nilai pelunasan dipercepat resmi dari bank bisa berbeda** (ada yang memakai sisa pokok flat + penalti). Tanyakan dulu ke bank sebelum bulan ke-5.
- Tidak ada belanja baru di kartu kredit/paylater, denda, atau biaya admin.

## Cek bahaya
- Tidak ada cicilan minimum yang lebih kecil dari bunganya ✓.
- Pinjol 0,1%/hari tepat di batas OJK 2026 untuk pinjaman konsumtif — pastikan aplikasinya terdaftar di ojk.go.id / Kontak OJK 157 / WA 081-157-157-157.
- Kartu kredit 1,75%/bulan = batas maksimum BI ✓.

## Langkah minggu ini
1. Bayar pinjol Rp2.060.000 sekaligus bulan ini (sisa ekstra Rp940.000 ke paylater).
2. Nonaktifkan/hapus limit paylater dan jangan pakai kartu kredit untuk belanja baru.
3. Pasang pengingat tanggal jatuh tempo keempat utang (hindari denda).
4. Telepon bank KTA: tanyakan syarat & biaya pelunasan dipercepat/sebagian.
5. Sisihkan dana darurat awal kecil (mis. Rp500.000–1 juta) agar tidak lari ke paylater saat ada keperluan mendadak.

Jangan menutup utang dengan utang baru (gali lubang tutup lubang). Kesulitan bayar? Hubungi kreditur untuk restrukturisasi secara resmi; pengaduan Kontak OJK 157.

⚠️ Bukan nasihat keuangan/investasi. Angka adalah simulasi dari data & asumsi di atas. Untuk kasus rumit, konsultasikan ke perencana keuangan bersertifikat.

## Penilaian penguji
- Simulasi independen (Fraction): Avalanche & Snowball = 10 bulan, bunga Rp4.226.895, per utang 730.469 / 3.315.551 / 120.875 / 60.000, bulan lunas 5/10/2/1 — **identik** dengan script.
- Konversi flat: cicilan Rp1.520.000, r = 1,62753%/bln = 19,53%/th (bisection penguji) ✓. Memakai 1,628% (dibulatkan) vs r persis: selisih total bunga Rp1.052 — tidak material, tapi sebaiknya script bisa menerima bunga flat langsung (temuan T-3).
- Peringatan "bila bunganya FLAT, ubah dulu..." muncul untuk KTA walau sudah dikonversi — benar sebagai pengingat, sedikit berisik (temuan T-4).
- **Hasil: LULUS.**
