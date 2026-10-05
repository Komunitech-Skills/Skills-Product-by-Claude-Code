# Istilah & Asumsi — Kelayakan Investasi Usaha

Dibaca agent saat menjelaskan hasil ke pengguna awam. Pakai kalimat di kolom "Bahasa awam".

## 1. Istilah
| Istilah | Bahasa awam | Rumus (konvensi: tahun 0 = investasi, bertanda minus) |
|---|---|---|
| Arus kas bersih (uang bersih) | Uang yang benar-benar masuk dari rencana ini setelah bahan baku, biaya rutin, dan pajak | omzet − biaya variabel − biaya tetap − pajak |
| Payback / balik modal | Berapa lama sampai uang yang kembali menutup modal | tahun sebelum kumulatif ≥ 0 + sisa ÷ arus kas tahun itu |
| Payback terdiskonto | Balik modal kalau uang masa depan "didiskon" ke nilai hari ini | sama, tetapi memakai arus kas ÷ (1 + r)^t |
| Tingkat diskonto (r) | Hasil minimal per tahun yang Anda minta dari uang Anda — patokan pembanding | asumsi, default 12%/tahun |
| NPV | Untung bersih setara uang hari ini **di atas** patokan. Positif = mengalahkan patokan | Σ arus kas_t ÷ (1 + r)^t, t = 0..n |
| IRR | Imbal hasil per tahun dari rencana ini. Layak bila lebih besar dari patokan | r yang membuat NPV = 0 |
| PI (profitability index) | Tiap Rp1 modal kembali berapa (nilai hari ini). > 1 = baik | nilai kini arus kas tahun 1..n ÷ investasi |
| Omzet impas (BEP akuntansi) | Omzet minimal agar tidak rugi di pembukuan (sudah termasuk penyusutan alat) | (biaya tetap + penyusutan) ÷ (1 − % biaya variabel − % pajak omzet) |
| Omzet minimal agar layak (BEP ekonomi) | Omzet minimal agar NPV = 0, bila omzet sama tiap tahun | dicari script; memakai "biaya modal tahunan setara" = −PMT(r, n, investasi − nilai kini nilai sisa) |
| Penyusutan garis lurus | Nilai alat turun sama rata tiap tahun | (investasi − nilai residu) ÷ umur ekonomis |
| Nilai sisa | Perkiraan nilai alat di akhir masa hitung (bisa dijual) | investasi − penyusutan × tahun terpakai, atau perkiraan pengguna |
| Batas aman | Seberapa jauh omzet boleh turun / biaya boleh naik sebelum NPV jadi negatif | dicari script |

Cara menyebut di chat: "NPV Rp60 juta artinya, setelah modal kembali **dan** Anda mendapat hasil minimal 12% per tahun, masih ada kelebihan setara Rp60 juta uang hari ini."

## 2. Tingkat diskonto default 12%
- Asal-usul: bunga KUR Mikro/Kecil sektor produksi **6% efektif per tahun** (Permenko Perekonomian 1/2026; lihat juga skill `pengajuan-kur`) ditambah **tambahan risiko usaha 6%** karena omzet rencana baru belum pasti.
- Ini **asumsi pembanding**, bukan rekomendasi dan bukan bunga bank yang berlaku untuk pengguna.
- Ganti bila: modal dari pinjaman → pakai bunga efektif pinjaman itu (+ tambahan risiko bila mau); modal sendiri → pakai hasil minimal yang pengguna inginkan (mis. "kalau tidak lebih dari deposito/ usaha lain, buat apa").
- Bunga/cicilan pinjaman **jangan** dimasukkan lagi ke biaya: sudah diwakili diskonto (menghindari hitung dua kali).

## 3. Pajak (disebut, tidak dihitung rinci)
- **PPh final UMKM 0,5% dari omzet** (PP 55/2022): untuk peredaran bruto ≤ Rp4,8 miliar/tahun, berbatas waktu sesuai jenis wajib pajak; orang pribadi tidak dikenai pajak atas omzet s.d. Rp500 juta/tahun dari seluruh usaha. Opsi: `--pajak-persen 0,5` (dasar omzet). Penghematan biaya bukan omzet → tidak menambah PPh final.
- **PPh badan** (tarif umum 22%, UU HPP; ada fasilitas pengurangan tarif untuk badan beromzet tertentu): opsi `--pajak-persen 22 --dasar-pajak laba` (laba setelah penyusutan). Fasilitas, kompensasi rugi, dan penyusutan fiskal per kelompok harta tidak dimodelkan.
- Pembulatan pajak ke bawah (tidak melebihi tarif); belum dicocokkan dengan Coretax. Aturan bisa berubah: sarankan cek DJP/konsultan pajak.

## 4. Penyederhanaan model (sebut bila relevan)
1. Arus kas dianggap masuk di akhir tiap tahun (lebih hati-hati dari kenyataan bulanan).
2. Omzet/biaya konstan kecuali diberi `--kenaikan-omzet`/`--kenaikan-biaya` atau daftar per tahun.
3. Modal kerja awal (stok, deposit sewa) dimasukkan ke investasi; bila kembali di akhir, tambahkan ke `--nilai-sisa`.
4. Laba/rugi penjualan alat bekas tidak dikenai pajak; rugi tidak dibawa ke tahun berikutnya.
5. IRR dicari di rentang −99% s.d. 1000% per tahun; di luar itu dilaporkan tidak ada.

## 5. Umur ekonomis (asumsi umum, bisa diubah pengguna)
Mesin/peralatan kafe & dapur: 4–5 tahun · Kendaraan niaga (pickup, mobil box): ±8 tahun · Renovasi ruko sewa: sepanjang masa sewa. Angka ini hanya titik awal hitungan, bukan ketentuan pajak.
