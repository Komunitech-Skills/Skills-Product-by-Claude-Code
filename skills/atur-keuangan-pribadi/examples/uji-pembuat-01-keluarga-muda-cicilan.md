# Contoh 1 — Keluarga muda, satu anak, empat utang

> Dibuat oleh pembuat skill sebagai contoh cara pakai dan pengecekan awal. **Ini bukan pengganti uji A/B, uji banding pesaing, atau pengujian independen Tahap 6** — itu dilakukan terpisah oleh penguji lain.
> Semua angka di bawah adalah keluaran asli `scripts/keuangan.py` (dijalankan 2026-09-26), bukan diketik ulang dari kepala.

## Permintaan pengguna
> "Tolong bantu atur keuangan keluarga saya. Saya (Dimas) gaji bersih 6,5 juta, istri 3 juta, THR kami berdua setahun total 9,5 juta. Anak satu umur 1 tahun. Kontrakan 1,6 juta, dapur 2,1 juta, listrik+air 450rb, bensin 600rb, kuota+wifi 350rb, susu popok 700rb, kirim ibu 500rb, sedekah 100rb, jajan 500rb, Netflix-an 80rb. Utang: kartu kredit 12 juta (bunga 1,75% sebulan, minimum 600rb), paylater 3 juta (2,5%/bulan, minimum 200rb), pinjam kakak 2 juta (tanpa bunga, nyicil 250rb), KTA 20 juta (11% setahun efektif, cicilan 700rb). Dana darurat baru 2 juta. Kami bingung, gaji selalu habis."

## Langkah 1 — cakupan
Keuangan keluarga (bukan usaha), tidak meminta rekomendasi produk investasi → lanjut. Semua data inti sudah ada; bunga sudah jelas periodenya dan KTA disebut efektif → **tidak perlu bertanya**. Asumsi disebut di hasil.

## Langkah 2 — perintah yang dijalankan
```
python3 scripts/keuangan.py anggaran --pemasukan "Gaji Dimas=6,5jt" --pemasukan "Gaji Rina=3jt" \
  --musiman "THR berdua=9,5jt" --pos "Kontrakan=1,6jt" --pos "Listrik token & air=450rb" \
  --pos "Belanja dapur=2,1jt" --pos "Transport & bensin=600rb" --pos "Kuota & wifi=350rb" \
  --pos "Susu & popok=700rb" --pos "Cicilan minimum semua utang=1,75jt:wajib" --pos "Kiriman ortu=500rb" \
  --pos "Sedekah=100rb" --pos "Jajan & nongkrong=500rb:keinginan" --pos "Langganan streaming=80rb" \
  --pos "Pelunasan utang ekstra=1jt:tabungan" --pos "Dana darurat=561.666" --pola 60/20/20

python3 scripts/keuangan.py utang --utang "Kartu kredit;12jt;1,75%/bln;600rb;kk" \
  --utang "Paylater;3jt;2,5%/bln;200rb;paylater" --utang "Pinjam kakak;2jt;0%;250rb;keluarga" \
  --utang "KTA;20jt;11%/th;700rb;kta" --ekstra 1jt --metode banding

python3 scripts/keuangan.py dana-darurat --pengeluaran-pokok 8,05jt --status anak --saldo 2jt --setoran 561.666
```
(Percobaan pertama tanpa pos "Dana darurat" menyisakan Rp261.666 belum bertugas; sesuai prinsip zero-based, sisa itu dimasukkan ke dana darurat → Rp300.000 + Rp261.666 = Rp561.666.)

## Hasil untuk pengguna

### Ringkasan
Pemasukan keluarga Rp10.291.666/bulan (termasuk THR dibagi 12). "Gaji selalu habis" karena belum semua rupiah punya tugas dan cicilan + bunga utang memakan Rp1,75 juta/bulan. Langkah terpenting: kunci Rp1 juta/bulan untuk pelunasan ekstra dengan metode Avalanche — semua utang lunas dalam 15 bulan, lalu uang cicilan dialihkan ke dana darurat.

### Anggaran (pola 60/20/20 karena punya anak & kirim ortu)
| Pos | Kelompok | Jumlah | % pemasukan |
|---|---|---:|---:|
| Kontrakan | Kebutuhan wajib | Rp1.600.000 | 15,5% |
| Listrik token & air | Kebutuhan wajib | Rp450.000 | 4,4% |
| Belanja dapur | Kebutuhan wajib | Rp2.100.000 | 20,4% |
| Transport & bensin | Kebutuhan wajib | Rp600.000 | 5,8% |
| Kuota & wifi | Kebutuhan wajib | Rp350.000 | 3,4% |
| Susu & popok | Kebutuhan wajib | Rp700.000 | 6,8% |
| Cicilan minimum semua utang | Kebutuhan wajib | Rp1.750.000 | 17,0% |
| Kiriman ortu | Keluarga & sosial/ibadah | Rp500.000 | 4,9% |
| Sedekah | Keluarga & sosial/ibadah | Rp100.000 | 1,0% |
| Jajan & nongkrong | Keinginan | Rp500.000 | 4,9% |
| Langganan streaming | Keinginan | Rp80.000 | 0,8% |
| Pelunasan utang ekstra | Tabungan & pelunasan ekstra | Rp1.000.000 | 9,7% |
| Dana darurat | Tabungan & pelunasan ekstra | Rp561.666 | 5,5% |
| **Total dialokasikan** | | **Rp10.291.666** | 100,0% |
| **Sisa** | | **Rp0** | zero-based tercapai |

| Kelompok | Pola | Batas pola | Rencana | Selisih |
|---|---:|---:|---:|---:|
| Kebutuhan (wajib + keluarga/sosial) | 60% | Rp6.175.000 | Rp8.150.000 | +Rp1.975.000 |
| Keinginan | 20% | Rp2.058.333 | Rp580.000 | -Rp1.478.333 |
| Tabungan & pelunasan ekstra | 20% | Rp2.058.333 | Rp1.561.666 | -Rp496.667 |

Kebutuhan tinggi terutama karena cicilan (17%). Setelah utang lunas, pos cicilan Rp1,75 juta + ekstra Rp1 juta bebas → porsi tabungan otomatis naik jauh di atas 20%.

### Rencana pelunasan
| Metode | Urutan | Semua lunas | Total bunga | Utang pertama lunas |
|---|---|---:|---:|---:|
| **Avalanche** | Paylater → Kartu kredit → KTA → Pinjam kakak | bulan ke-15 | **Rp3.345.301** | bulan ke-3 |
| Snowball | Pinjam kakak → Paylater → Kartu kredit → KTA | bulan ke-15 | Rp3.501.409 | bulan ke-2 |

Avalanche lebih hemat **Rp156.108**. Rincian Avalanche per utang: Paylater lunas bulan ke-3, Pinjam kakak ke-8, Kartu kredit ke-9, KTA ke-15.
Cuplikan jadwal bulan ke-1 (Avalanche): Kartu kredit bunga Rp210.000 (12.000.000 × 1,75%), Paylater bunga Rp75.000 dan dibayar Rp1.200.000 (minimum Rp200.000 + ekstra Rp1.000.000), KTA bunga Rp183.333 (20.000.000 × 11% ÷ 12 = 183.333,33).

Peringatan dari script: KTA → pastikan bunganya memang efektif; jika di kontrak tertulis flat, jalankan `konversi-flat` dulu.

### Dana darurat (status punya anak → 9–12 bulan pengeluaran pokok)
Pengeluaran pokok = semua kebutuhan wajib + kiriman ortu = Rp8.050.000 (tanpa sedekah, jajan, streaming).
| Target | Jumlah | Setoran Rp561.666 saja | Setelah utang lunas (setoran naik jadi Rp3.311.666) |
|---|---:|---:|---:|
| 9 bulan | Rp72.450.000 | 126 bulan | 19 bulan lagi (setelah bulan ke-15) |
| 12 bulan | Rp96.600.000 | 169 bulan | 27 bulan lagi |
Dana darurat awal 1 bulan (Rp8.050.000) tercapai di bulan ke-11 (ceil(6.050.000 ÷ 561.666) = 11). Saldo di bulan ke-15 = 2.000.000 + 15 × 561.666 = Rp10.424.990; lalu setoran = 561.666 + 1.750.000 + 1.000.000 = Rp3.311.666.

### Asumsi yang dipakai
- THR dibagi 12, dibulatkan ke bawah. Pola 60/20/20 (keluarga dengan anak).
- Bunga efektif dari sisa saldo, dibulatkan ke rupiah terdekat per bulan; tidak ada belanja baru di kartu kredit/paylater, denda, atau biaya admin.
- Cicilan minimum utang yang lunas dialihkan ke utang berikutnya (anggaran tetap Rp2.750.000/bulan).

### Langkah minggu ini
1. Tanggal gajian: pindahkan Rp1.561.666 (ekstra utang + dana darurat) ke rekening terpisah **sebelum** belanja lain.
2. Tutup/bekukan paylater di aplikasi e-wallet; jangan pakai kartu kredit untuk belanja baru sampai lunas.
3. Bayar ekstra Rp1 juta ke **Paylater** bulan ini (bunga tertinggi 2,5%/bulan).
4. Cek kontrak KTA: bunga flat atau efektif?
5. Sampaikan ke kakak jadwal cicilan Rp250.000/bulan (lunas bulan ke-8) supaya jelas.

⚠️ Bukan nasihat keuangan/investasi. Angka adalah simulasi dari data & asumsi di atas. Untuk kasus rumit, konsultasikan ke perencana keuangan bersertifikat.

## Catatan pembuat (cek awal)
- Angka bulan ke-1 dicek manual (lihat cuplikan) dan cocok dengan script; tes regresi membandingkan seluruh simulasi dengan implementasi Fraction independen (`tests/uji_regresi.py`).
- Tidak ada rekomendasi produk/instrumen. Sedekah diperlakukan opsional sesuai pilihan pengguna.
- Temuan saat membuat contoh ini: pesan "coba pola 60/20/20" muncul walau pola sudah 60/20/20 → diperbaiki (pesan kini menyesuaikan pola yang dipakai).
