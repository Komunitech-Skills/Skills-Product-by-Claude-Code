# Uji 06 - Normal 1: keripik tempe pedas + 4 ide (RICE)

Penguji independen, 2026-09-29, `claude-code (simulasi agent)`. Agen mengikuti SKILL.md, templat, dan referensi apa adanya. Data fiktif.

**Pengguna:** "Saya jual keripik tempe pedas di Semarang, kemasan plastik klip 100 g Rp15.000. Mau naik kelas: bikinin spesifikasi produknya, target margin kotor 40%. Ide pengembangan: level pedas 1-5, kemasan standing pouch zip 150 g, varian rumput laut, paket reseller 20 pcs. Mana dulu?"

Agen menanyakan sekali jangkauan/dampak/keyakinan/usaha, pengguna menjawab, agen membuat CSV (pemisah `;`, format angka Indonesia):
```
nama;jangkauan;dampak;keyakinan;usaha
Level pedas 1-5;1.200;1;80%;4
Kemasan standing pouch zip 150 g;2.000;0,5;90%;3
Varian rumput laut;800;1;50%;6
Paket reseller 20 pcs;150;2;70%;5
```
`python3 scripts/prioritas.py --metode rice --csv n1-keripik.csv` (keluaran asli, kode keluar 0):
```
| # | Ide | Skor | Tahap |
|---|---|---|---|
| 1 | Kemasan standing pouch zip 150 g | 300,00 | Sekarang |
| 2 | Level pedas 1-5 | 240,00 | Sekarang |
| 3 | Varian rumput laut | 66,67 | Berikutnya |
| 4 | Paket reseller 20 pcs | 42,00 | Berikutnya |
```
Dengan `--kapasitas 8`: baris 4 berubah jadi **Nanti** (3+4 = 7 hari muat di Sekarang; 6 hari muat di Berikutnya; 5 hari tidak muat lagi).

**Verifikasi independen (Fraction, bukan fungsi script):** 2000 x 0,5 x 0,9 / 3 = 300; 1200 x 1 x 0,8 / 4 = 240; 800 x 1 x 0,5 / 6 = 66,666... -> 66,67; 150 x 2 x 0,7 / 5 = 42. Semua cocok. "1.200" dan "0,5" terbaca benar.

## Ringkasan dokumen yang dihasilkan agen
- Judul `Spesifikasi Produk: Keripik Tempe Pedas - v1.0 - 2026-09-29`, baris Asumsi (produksi rumahan, jual di Shopee + reseller) diberi tanda [ASUMSI].
- Bagian 3 resep: bahan disebut (tempe, tepung beras, cabai, bawang putih, minyak), takaran "[belum ditentukan - isi dari resep Anda]" (tidak dikarang).
- Bagian 4 label: nama, komposisi, berat bersih, produsen, kedaluwarsa, nomor P-IRT bila sudah ada.
- Bagian 5: **HPP maksimal Rp9.000** = 15.000 x (1 - 0,40); dicek independen: benar. Rujuk `hitung-hpp`.
- Bagian 6: berat bersih 100 g (toleransi ditulis), kerenyahan setelah 14 hari di suhu ruang, kadar minyak visual, segel klip.
- Bagian 7: PIRT (sppirt.pom.go.id), halal (bpjph.halal.go.id), NIB (oss.go.id), merek DJKI; "dicek terakhir" + "bukan nasihat hukum".
- Bagian 8: tabel script apa adanya + roadmap sebagai hasil untuk pembeli.
- Bagian 9-11: risiko (harga cabai musiman, minyak tengik), di luar cakupan, tabel perubahan v0.x -> v1.0.

## Penilaian
- Struktur 11 bagian, angka dihitung, tanpa angka karangan: **baik**.
- **Kekurangan:** referensi tidak memberi tahu bahwa kewajiban halal untuk **produk makanan-minuman usaha mikro-kecil berlaku 17 Oktober 2026** (18 hari dari tanggal uji). Agen hanya menulis "diberlakukan bertahap". Untuk keripik tempe ini informasi paling mendesak di dokumen dan tidak muncul.
- Agen juga tidak bisa menyebut dasar aturan PIRT terbaru (Peraturan BPOM No. 4 Tahun 2024) karena referensi tidak mencantumkannya.

**Vonis: LULUS dengan catatan** (isi inti kuat; pengingat halal kurang tanggal kritis).
