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

## 3. Produk
| Bahan | Takaran/batch (10 botol) | Catatan |
|---|---|---|
| Air | [belum ditentukan] | |
| Serai, jahe, teh, gula | [belum ditentukan, isi setelah uji rasa] | |
Hasil per batch: 10 botol | Daya simpan: [diuji dulu, tulis hasilnya; jangan diklaim sebelum diuji] | Penyimpanan: dingin.

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
Perlu dicek: izin PIRT (https://sppirt.pom.go.id, Dinas Kesehatan setempat), sertifikasi halal (https://bpjph.halal.go.id), label, NIB (https://oss.go.id). Dicek terakhir 2026-09-29 (pengingat umum, belum diverifikasi ke dinas). Bukan nasihat hukum.

## 8. Prioritas & roadmap
Skor RICE dari `scripts/prioritas.py` (lihat contoh 2). **Sekarang:** paket 6 botol, botol mini 100 ml untuk sampel. **Berikutnya:** varian tanpa gula. **Nanti:** langganan mingguan (usaha besar, keyakinan rendah; uji pre-order dulu).

## 9. Risiko & hal belum diketahui
Daya simpan belum diuji; harga serai di musim hujan belum diketahui; belum ada izin.

## 10. Di luar cakupan versi ini
Klaim kesehatan; penjualan luar kota (ongkir dingin); langganan.

## 11. Catatan perubahan
| Versi | Tanggal | Perubahan | Alasan | Hasil uji | HPP/label terdampak? |
|---|---|---|---|---|---|
| v0.1 | 2026-09-29 | Dokumen pertama | - | belum diuji | belum dihitung |
