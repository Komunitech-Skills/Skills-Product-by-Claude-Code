# Uji A/B - tanpa skill vs dengan skill (skenario normal 1)

Penguji independen, 2026-09-29, `claude-code (simulasi agent)`. Prompt sama dengan `06-uji-normal-keripik-tempe.md`:
"Saya jual keripik tempe pedas di Semarang, kemasan plastik klip 100 g Rp15.000. Mau naik kelas: bikinin spesifikasi produknya, target margin kotor 40%. Ide: level pedas 1-5, standing pouch zip 150 g, varian rumput laut, paket reseller 20 pcs. Mana dulu?"

## A. Tanpa skill (jawaban agen umum, diringkas)
> **Spesifikasi Keripik Tempe Pedas**
> - Bahan: tempe, tepung, bumbu pedas. Kemasan: standing pouch agar lebih premium.
> - Harga: dengan margin 40%, modal sebaiknya sekitar Rp9.000.
> - Legalitas: urus PIRT dan halal, daftarkan merek.
> - Prioritas ide: 1) standing pouch (paling berdampak ke citra), 2) level pedas, 3) paket reseller, 4) rumput laut.
> - Saran: lakukan tes pasar, promosi di TikTok.

Ciri: tidak ada versi/tanggal, persyaratan tidak bisa dicek ("lebih premium"), urutan ide dari perasaan agen (reseller di atas rumput laut tanpa alasan angka), tidak ada standar mutu/uji terima, tidak ada tautan resmi, tidak ada "di luar cakupan", tidak ada catatan perubahan, tidak ada brief untuk pemasok kemasan. HPP benar secara angka tapi tanpa rumus.

## B. Dengan skill
Lihat `06-uji-normal-keripik-tempe.md`: dokumen 11 bagian bernomor versi; asumsi ditandai; takaran tidak dikarang; HPP maksimal Rp9.000 dengan rumus; standar mutu berisi angka + cara cek + toleransi; pengingat izin dengan tautan resmi + tanggal cek + disclaimer; skor RICE dihitung script (pouch 300, level pedas 240, rumput laut 66,67, reseller 42 - diverifikasi independen) dan roadmap ditulis sebagai hasil untuk pembeli; brief pemasok tanpa HPP; tabel perubahan.

## Perbandingan
| Aspek | Tanpa skill | Dengan skill |
|---|---|---|
| Siap dikirim ke produsen | tidak | ya (brief terpisah, tanpa data internal) |
| Persyaratan bisa dicek | tidak | ya (angka, cara uji, toleransi) |
| Prioritas | perasaan, urutan 3-4 berbeda dari hitungan | dihitung, bisa diaudit |
| Angka karangan | tidak ada, tapi tanpa rumus | rumus tertulis |
| Izin | 1 kalimat | per item + tautan + tanggal cek (belum ada tenggat halal 17-10-2026) |
| Versi & jejak perubahan | tidak ada | ada |

**Kesimpulan:** dengan skill **jelas lebih baik**. Kelemahan yang sama di kedua sisi: tidak ada yang menyebut tenggat wajib halal UMK 17 Oktober 2026.
