# Contoh 1 - Spesifikasi produk (fiktif: "Teh Serai Jahe Kita")

**Pengguna:** "Mau bikin teh serai jahe botol 250 ml, jual Rp15.000, target margin 50%. Bantu susun spesifikasinya. Resep belum fix."

# Spesifikasi Produk: Teh Serai Jahe Kita - v0.1 - 2026-09-29
**Asumsi:** dijual online (marketplace + status WA) dan titip di kafe; produksi rumahan awal 60 botol/minggu; belum ada resep tetap. Semua nama usaha dan angka contoh ini fiktif.

## 1. Ringkasan
Minuman teh serai jahe siap minum botol 250 ml, manis sedang, untuk pekerja kantoran yang ingin minuman hangat-segar tanpa pewarna. Dijual Rp15.000/botol.

## 2. Masalah & pembeli sasaran
- Pembeli: karyawan kantor 25-40 tahun di kota besar.
- Keinginan: "minuman sore yang enak tapi tidak terlalu manis."
- Alasan beli: rasa rempah alami, botol praktis, bisa dipesan paket.

**Ukuran keberhasilan (3 bulan pertama):**
1. Terjual >= 240 botol/bulan (rata-rata 60 botol/minggu) pada bulan ke-3.
2. Pembeli ulang >= 30% (dari catatan pesanan WA/marketplace).
3. Skor rasa rata-rata >= 4 dari 5 pencicip di tiap batch uji (lihat bagian 6).

## 3. Produk
| Bahan | Takaran/batch (10 botol) | Catatan |
|---|---|---|
| Air | [belum ditentukan] | |
| Serai, jahe, teh, gula | [belum ditentukan, isi setelah uji rasa] | |
Hasil per batch: 10 botol | Daya simpan: [diuji dulu, tulis hasilnya; jangan diklaim sebelum diuji] | Penyimpanan: dingin (kulkas) - **keputusan ini menentukan jalur izin, lihat bagian 7.**

## 4. Kemasan & label
Botol PET 250 ml + tutup segel + label stiker. Label: nama produk, komposisi, isi bersih, produsen, tanggal produksi/kedaluwarsa, nomor izin (bila sudah ada).

## 5. HPP & harga target
Harga jual Rp15.000, margin kotor 50% -> **HPP maksimal Rp7.500** (15.000 x (1 - 0,5)), sudah termasuk botol, label, tenaga, gas. Angka pasti: jalankan `hitung-hpp`. Setelah potongan marketplace: `harga-jual-marketplace`.

## 6. Standar mutu & uji terima
| Aspek | Standar | Cara cek | Toleransi |
|---|---|---|---|
| Isi bersih | 250 ml | gelas ukur, 3 sampel/batch | 245-255 ml |
| Rasa | manis sedang, jahe terasa hangat | 5 pencicip, skor 1-5 | rata-rata >= 4 |
| Tampilan | jernih kecokelatan, tanpa endapan besar | visual | - |
| Segel | tidak bocor dibalik 10 detik | uji balik | 0 bocor |

## 7. Pengingat izin & legalitas
**Penting - jalur izin:** karena teh ini **harus disimpan dan dikirim dingin**, produk ini **tidak bisa memakai PIRT** (SPP-IRT). Pangan yang butuh penyimpanan/distribusi dingin dikecualikan dari SPP-IRT dan harus memakai **izin edar BPOM MD** (Peraturan BPOM No. 4 Tahun 2024). Pilihan yang perlu dibahas dengan Dinas Kesehatan/Balai POM setempat:
- (a) Tetap dingin -> siapkan izin edar **BPOM MD** (syarat sarana produksi lebih berat; cek produk sejenis di https://cekbpom.pom.go.id).
- (b) Ubah proses agar produk **aman disimpan di suhu ruang**, lalu uji daya simpan; baru tanyakan apakah produk hasil ubahan boleh PIRT (botol yang ditutup kedap/steril juga termasuk pengecualian - pastikan dulu).
Jangan memproduksi untuk dijual luas sebelum jalur ini jelas.

| Perlu dicek | Dasar aturan | Tautan | Status |
|---|---|---|---|
| Jalur izin edar: BPOM MD (produk dingin), bukan PIRT | Peraturan BPOM 4/2024 | https://sppirt.pom.go.id ; https://cekbpom.pom.go.id | belum |
| **Sertifikat halal - tenggat 17 Oktober 2026** untuk makanan-minuman usaha mikro-kecil (tinggal 18 hari dari tanggal dokumen); jalur self declare dengan pendamping bila memenuhi syarat | UU 33/2014; PP 42/2024 | https://ptsp.halal.go.id | belum |
| NIB | PP 28/2025 | https://oss.go.id | belum |
| Merek "Teh Serai Jahe Kita" (cek kemiripan dulu) | UU 20/2016 | https://merek.dgip.go.id | belum |
| Label: nama, komposisi, isi bersih, produsen, kedaluwarsa, "simpan dingin", nomor izin & logo halal setelah terbit | aturan label pangan BPOM | - | belum |

Dicek terakhir 2026-09-29 lewat situs resmi (lihat `references/perizinan-produk.md`). Ini pengingat, bukan nasihat hukum; konfirmasi ke Dinas Kesehatan/Balai POM/pendamping halal.

## 8. Prioritas & roadmap
Skor RICE dari `scripts/prioritas.py` (keluaran default, tanpa `--kapasitas`; lihat contoh 2). **Sekarang:** paket 6 botol, botol mini 100 ml untuk sampel. **Berikutnya:** varian tanpa gula. **Nanti:** langganan mingguan (usaha besar, keyakinan rendah; uji pre-order dulu).

## 9. Risiko & hal belum diketahui
Daya simpan belum diuji; harga serai di musim hujan belum diketahui; **jalur izin (BPOM MD vs ubah proses) belum diputuskan** dan menentukan biaya serta waktu mulai jual; tenggat halal 17-10-2026.

## 10. Di luar cakupan versi ini
Klaim kesehatan; penjualan luar kota (ongkir dingin); langganan.

## 11. Catatan perubahan
| Versi | Tanggal | Perubahan | Alasan | Hasil uji | HPP/label terdampak? |
|---|---|---|---|---|---|
| v0.1 | 2026-09-29 | Dokumen pertama | - | belum diuji | belum dihitung |
