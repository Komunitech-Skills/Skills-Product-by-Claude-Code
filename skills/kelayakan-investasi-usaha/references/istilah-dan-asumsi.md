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
| Penyusutan garis lurus | Nilai alat turun sama rata tiap tahun | (investasi − nilai sisa) ÷ masa pakai dalam proyek; tanpa perkiraan harga jual kembali: investasi ÷ umur ekonomis |
| Nilai sisa | Perkiraan nilai alat di akhir masa hitung (bisa dijual) | investasi − penyusutan × tahun terpakai, atau perkiraan pengguna |
| Batas aman | Seberapa jauh omzet boleh turun / biaya boleh naik sebelum NPV jadi negatif | dicari script |

Cara menyebut di chat: "NPV Rp60 juta artinya, setelah modal kembali **dan** Anda mendapat hasil minimal 12% per tahun, masih ada kelebihan setara Rp60 juta uang hari ini."

## 2. Tingkat diskonto default 12%
- Asal-usul: bunga KUR Mikro/Kecil sektor produksi **6% efektif per tahun** (Permenko Perekonomian No. 1 Tahun 2026 Pasal 37 & 44, berlaku 13 Januari 2026; konfirmasi ke bank penyalur; lihat juga skill `pengajuan-kur`) ditambah **tambahan risiko usaha 6%** karena omzet rencana baru belum pasti.
  - **Dasar aturan:** Peraturan Menteri Koordinator Bidang Perekonomian No. 1 Tahun 2026 tentang Pedoman Pelaksanaan Kredit Usaha Rakyat. Pasal 37 ayat (1) huruf a (KUR mikro) dan Pasal 44 ayat (1) huruf a (KUR kecil): untuk Sektor Produksi atau sektor perdagangan berorientasi ekspor "6% (enam persen) efektif per tahun". Ditetapkan 5 Januari 2026, diundangkan dan berlaku 13 Januari 2026 (Berita Negara RI Tahun 2026 No. 17); mencabut Permenko Perekonomian 1/2022 beserta perubahannya.
  - Sektor perdagangan yang tidak berorientasi ekspor: 6% untuk akad pertama, lalu naik per akad (KUR mikro 7% akad kedua; KUR kecil 7%/8%/9% akad kedua–keempat), Pasal 37 ayat (1) huruf b dan Pasal 44 ayat (1) huruf b. Patokan 12% tetap asumsi contoh.
  - **Sumber & tanggal cek (2026-10-13, penguji independen):** teks pasal dibaca dari salinan teks lengkap di basis data hukum DDTC (sumber sekunder): https://perpajakan.ddtc.co.id/sumber-hukum/peraturan-pusat/peraturan-menteri-koordinator-bidang-perekonomian-1-tahun-2026 . Tarif 6% efektif (KUR mikro & kecil sektor produksi/ekspor) dan tanggal berlaku 13 Januari 2026 sejalan dengan siaran pers resmi Kemenko Perekonomian (Januari 2026): https://www.ekon.go.id/publikasi/detail/6784/konsolidasi-kredit-program-pemerintah-2026-perkuat-pedoman-pelaksanaan-kredit-program-optimalkan-penyaluran-dan-wujudkan-pertumbuhan-ekonomi-inklusif-berbasis-usaha-mikro-dan-kecil (halaman sedang tidak dapat dibuka langsung saat pengecekan; isi dibaca dari indeks mesin pencari). Salinan resmi di jdih.ekon.go.id dan peraturan.go.id tidak dapat diakses saat pengecekan itu.
  - **Cek ulang ke salinan resmi (2026-10-15, penguji independen):** JDIH BPK — https://peraturan.bpk.go.id/Details/342969/permenko-perekonomian-no-1-tahun-2026 (PDF: https://peraturan.bpk.go.id/Download/406143/2026PemenkoEkon001.pdf). Pasal 37 & 44 ayat (1) huruf a («… dikenakan sebesar 6% (enam persen) efektif per tahun …»), pengecualian huruf b, dan tanggal berlaku 13 Januari 2026 cocok. Bunga 6% tidak berlaku untuk semua sektor/akad.
- **Uji ketat 20%:** NPV juga selalu dihitung pada 20%/tahun. Positif = rencana tetap menutup modal walau bunga lebih mahal atau risiko lebih besar; hanya informasi, kesimpulan tetap dari patokan 12% (atau patokan pengguna).
- Ini **asumsi pembanding**, bukan rekomendasi dan bukan bunga bank yang berlaku untuk pengguna.
- Ganti bila: modal dari pinjaman → pakai bunga efektif pinjaman itu (+ tambahan risiko bila mau); modal sendiri → pakai hasil minimal yang pengguna inginkan (mis. "kalau tidak lebih dari deposito/ usaha lain, buat apa").
- Bunga/cicilan pinjaman **jangan** dimasukkan lagi ke biaya: sudah diwakili diskonto (menghindari hitung dua kali).

## 3. Pajak (disebut, tidak dihitung rinci)
- **PPh final UMKM 0,5% dari omzet** (PP 55/2022 sebagaimana diubah PP 20/2026; PP 20/2026 diundangkan 22 April 2026): untuk peredaran bruto ≤ Rp4,8 miliar/tahun; orang pribadi tidak dikenai pajak atas omzet s.d. Rp500 juta/tahun dari seluruh usaha (PP 55/2022 Pasal 60). Opsi: `--pajak-persen 0,5` (dasar omzet). Penghematan biaya bukan omzet → tidak menambah PPh final.
  - **Jangka waktu setelah PP 20/2026:** untuk wajib pajak **orang pribadi**, tarif 0,5% kini berlaku tanpa batas jumlah tahun ("selamanya") **selama masih memenuhi syarat** — PP 20/2026 menghapus Pasal 59 PP 55/2022 yang dulu membatasi 7 tahun. PT perorangan juga tidak lagi dibatasi jumlah tahun, tetapi aturan peralihannya berbeda dari orang pribadi; koperasi dan badan lain mengikuti batas waktu & aturan peralihan sendiri. Rinciannya di skill `pph-final-umkm`, atau tanyakan ke DJP (Kring Pajak 1500200)/konsultan pajak. Script tetap opsi sederhana: 0,5% dari omzet, tanpa memeriksa jangka waktu atau syarat.
  - **Sumber & tanggal cek (2026-10-14 s.d. 2026-10-15, penguji independen):** artikel DJP tentang PP 20/2026 untuk UMKM orang pribadi — https://www.pajak.go.id/id/artikel/pp-202026-tarif-pph-05-bagi-umkm-orang-pribadi-berlaku-selamanya («… dapat menggunakan tarif PPh Final 0,5% selama masih memenuhi kriteria tanpa khawatir masa berlakunya berakhir»); penghapusan Pasal 59 dicek di salindia DJP PP 20/2026 (Pasal I angka 6); tarif 0,5% & batas Rp4,8 miliar: siaran pers DJP https://www.pajak.go.id/id/siaran-pers/wajib-pajak-umkm-kenali-hak-dan-kewajiban-perpajakannya .
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
