# Skenario 3 (normal) — Rekap operasional: bersihkan CSV Rupiah campur format & impor

**Penguji:** Akun B (independen). CSV dibuat sendiri oleh penguji, sengaja mencampur format
Rupiah yang diminta diverifikasi: `Rp1.250.000,00`, `1,25jt`-style (lihat temuan), `1.250.000`,
`Rp 18.500`, `125000.50`, `13000` polos, plus 1 baris rusak (nilai bukan angka) untuk menguji
batas kemampuan pembersihan.

## CSV mentah (ringkas, 5 baris valid + 1 baris rusak)
```
Tanggal Transaksi,Nama Barang,Harga Satuan,Jumlah,Total Penjualan
2026-09-01,Minyak Goreng 1L,"Rp 18.500",10,"Rp1.250.000,00"
2026-09-01,Beras Premium 5kg,"62.500",2,"125000.50"
2026-09-02,Gula Pasir 1kg,13000,15,"195.000"
2026-09-02,Kecap Manis,"Rp. 12.500,00",8,"100.000"
2026-09-03,Telur Ayam (kg),"32,5",20,"1.250.000,75"
2026-09-03,Item Aneh (bukan angka),"tiga puluh ribu",5,"belum diisi"
```

## `bersihkan-csv` — hasil & verifikasi independen (dihitung ulang manual)
| Sel asli | Diharapkan (hitung manual) | Hasil script |
|---|---|---|
| `Rp 18.500` | 18500 | 18500 ✓ |
| `Rp1.250.000,00` | 1250000.00 | 1250000 ✓ |
| `62.500` | 62500 | 62500 ✓ |
| `125000.50` | 125000.50 | 125000.5 ✓ |
| `13000` | 13000 | 13000 ✓ |
| `195.000` | 195000 | 195000 ✓ |
| `Rp. 12.500,00` | 12500.00 | 12500 ✓ |
| `100.000` | 100000 | 100000 ✓ |
| `32,5` | 32.5 | 32.5 ✓ |
| `1.250.000,75` | 1250000.75 | 1250000.75 ✓ |

Semua **cocok 100%** dengan hitungan manual (dot-jadi-ribuan vs koma-jadi-desimal ditentukan
dengan benar berdasarkan posisi tanda baca terakhir).

**Header dirapikan benar:** `Tanggal Transaksi` → `TanggalTransaksi`, `Harga Satuan` →
`HargaSatuan`, dll. (aturan Grist: awali huruf, hanya huruf/angka/garis bawah).

## Temuan penting #1 — format "1,25jt"/"1,25 juta" TIDAK dikenali
pedoman kurasi Komunitech & README skill ini (bagian "3–5 manfaat", poin 3) menyebut contoh **"Rp 1,25jt"**
sebagai salah satu format yang "dirapikan otomatis". Diuji langsung:
```python
_bersihkan_angka("Rp 1,25jt")  -> None
_bersihkan_angka("1,25jt")     -> None
```
Regex `ANGKA_RP` tidak menerima huruf apa pun selain awalan "Rp"/"Rp.", jadi singkatan "jt"
(juta)/"rb"/"ribu" yang lazim dipakai UMKM Indonesia di WA/catatan tulisan tangan **tidak
dikonversi** — sel tetap apa adanya dan **seluruh kolom** ikut ditandai Text (lihat temuan #2).
Ini **overclaim** di README yang tidak cocok dengan kemampuan script sungguhan.

## Temuan penting #2 — satu sel gagal parse → SATU KOLOM PENUH batal dikonversi, tanpa menunjuk baris mana
Baris terakhir (`Item Aneh...` dengan `Harga Satuan="tiga puluh ribu"`, `Total
Penjualan="belum diisi"`) membuat **kolom `HargaSatuan` dan `TotalPenjualan` di SELURUH file**
kembali dicap "(Text)" dan nilainya **tidak dirapikan sama sekali** — termasuk baris 1–5 yang
tadinya berhasil dikonversi bila diuji sendirian (dibuktikan: menjalankan hanya 4 baris pertama
tanpa baris rusak → kolom yang sama menjadi "(Numeric)" dan semua nilai terkonversi bersih).
Perilaku "all-or-nothing per kolom" ini **benar secara desain** (mencegah kolom campur angka/
teks setengah-setengah) dan **tidak menyebabkan angka salah** (tidak ada silent-wrong-number),
tapi pesan keluarannya tidak menyebut **baris mana** yang menyebabkan kolom batal — pengguna
awam bisa bingung kenapa kolom Rupiahnya "kok jadi Text semua". Rekomendasi: sebutkan baris
pertama yang gagal parse per kolom di ringkasan `bersihkan-csv`.

## `impor-csv` (setelah dibersihkan, tanpa baris rusak) — REST API server tiruan independen
```bash
python3 scripts/grist.py buat-tabel pesanan --dokumen "Toko Berkah" --tabel RekapHarian --ya
python3 scripts/grist.py impor-csv rekap-bersih2.csv --dokumen "Toko Berkah" --tabel RekapHarian --ya
```
Hasil: `BERHASIL: 4 baris ditambahkan ke tabel 'RekapHarian'.` — dicek langsung ke penyimpanan
server tiruan (4 records tersimpan, field & nilai numerik sesuai file bersih).

**Uji negatif:** mengimpor CSV **mentah** (header masih `Tanggal Transaksi` berspasi) ditolak
**sebelum** ada request terkirim ke server: `GAGAL: Nama kolom 'Tanggal Transaksi' tidak sesuai
aturan Grist ... Jalankan 'bersihkan-csv' dulu.` — benar, tidak ada percobaan tulis parsial.

## Hasil
Fungsi inti (pembersihan angka & impor) **benar dan teruji ulang independen**. Satu overclaim
di README (format "jt"/"rb") harus diperbaiki sebelum rilis — lihat HASIL-UJI.md.
