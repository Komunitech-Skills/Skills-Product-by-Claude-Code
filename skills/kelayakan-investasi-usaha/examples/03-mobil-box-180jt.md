# 03 — Beli mobil box Rp180 juta vs sewa ekspedisi (investasi penghematan)

> Contoh pembuat skill (v1.0.0, diperbarui v1.0.1: label penghematan, NPV uji ketat 20%). Angka dari script, diverifikasi ulang dengan Python terpisah (NPV 9.701.913, IRR 13,85% identik).

## Pesan pengguna
"Usaha frozen food saya sewa ekspedisi sekitar 6,5 juta sebulan. Kalau beli mobil box 180 juta, biaya BBM, servis, pajak kendaraan, asuransi sekitar 3 juta sebulan (sopir sudah ada). Lebih untung beli?"

## Pemetaan (catatan agent)
Penghematan sewa 6,5jt/bulan → `--omzet` + `--jenis penghematan` (label hasil "Penghematan", bukan "Omzet"); biaya operasional mobil 3jt/bulan → `--biaya`. Masa 5 tahun (default), umur ekonomis kendaraan 8 tahun (asumsi) → nilai sisa garis lurus 180jt × 3/8 = 67,5jt. Pajak tidak ditambahkan: penghematan bukan omzet, jadi PPh final 0,5% tidak bertambah (disebut sebagai asumsi).
```bash
python3 scripts/kelayakan.py --investasi 180jt --omzet 6,5jt/bulan --biaya 3jt/bulan --tahun 5 --umur-ekonomis 8 --jenis penghematan --format teks
```

## Verifikasi manual
Hemat bersih (78.000.000 − 36.000.000) = 42.000.000/tahun. NPV 12% = −180.000.000 + 42.000.000 × 3,604776 + 67.500.000 ÷ 1,762342 = **Rp9.701.913**. Balik modal = 180 ÷ 42 = 4,29 tahun. NPV 20% = −180.000.000 + 42.000.000 × 2,990612 + 67.500.000 ÷ 2,48832 = **−Rp27.267.554**. Penghematan impas = (36.000.000 + 22.500.000) ÷ 12 = Rp4.875.000/bulan.

## Contoh balasan chat
**Beli mobil box Rp180 juta: KURANG LAYAK (dengan asumsi di bawah)**
Beli mobil menghemat ±Rp42 juta per tahun (Rp3,5 juta/bulan), tetapi modalnya baru kembali dalam 4 tahun 3 bulan, dan hasilnya hanya sedikit di atas patokan.

| Ukuran | Hasil | Arti |
|---|---|---|
| Balik modal | 4 tahun 3 bulan | dari penghematan bersih |
| Balik modal (nilai waktu uang) | belum dalam 5 tahun | bergantung harga jual mobil |
| NPV | Rp9.701.913 | kelebihan tipis di atas patokan 12% |
| NPV uji ketat 20% | −Rp27.267.554 | rugi bila patokan 20%/tahun |
| IRR | 13,85%/tahun | sedikit di atas 12% |
| PI | 1,05 | tiap Rp1 kembali Rp1,05 |
| Penghematan impas | Rp4.875.000/bulan | di bawah ini rugi di pembukuan |

Uji ketat: Bila hasil minimal yang diminta dinaikkan ke 20%/tahun (bunga lebih mahal atau risiko lebih besar), membeli mobil tidak lagi menutup modal plus hasil itu.

**Kalau meleset (NPV):** penghematan −10% → −Rp18.415.341 · −20% → −Rp46.532.595 · biaya mobil +10% → −Rp3.275.281.
**Kenapa kurang layak:** penghematan hanya boleh turun 3,5% (mis. pengiriman berkurang) dan biaya mobil naik 7,5% sebelum rugi dibanding patokan. Hasil positif juga bergantung pada mobil masih bernilai ±Rp67,5 juta di tahun ke-5.
**Agar layak:** penghematan (sewa ekspedisi yang tergantikan) minimal ±Rp6.275.716/bulan (bila biaya mobil tetap 3 juta), atau pilih mobil bekas yang lebih murah, atau manfaatkan mobil untuk pendapatan tambahan (antar pesanan pelanggan).
**Asumsi:** patokan 12%/tahun (asumsi tingkat diskonto contoh; ganti dengan bunga pinjaman Anda + premi risiko yang Anda pilih), masa 5 tahun, nilai mobil turun rata selama 8 tahun, sopir sudah ada, pajak tidak bertambah karena penghematan bukan omzet (bila usaha memakai PPh badan, laba naik dan pajaknya ikut naik).
Catatan: bukan nasihat keuangan; hasil tergantung asumsi, tidak ada jaminan untung.

Supaya lebih tajam:
1. Berapa perkiraan harga jual mobil box ini setelah 5 tahun?
2. Apakah sewa 6,5 juta itu bisa hilang seluruhnya, atau sebagian pengiriman tetap lewat ekspedisi?
3. Beli tunai atau kredit? Bila kredit, berapa bunganya?
