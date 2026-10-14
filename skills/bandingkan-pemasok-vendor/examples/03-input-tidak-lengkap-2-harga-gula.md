# 03 - Input tidak lengkap: 2 harga gula pasir tanpa jumlah & lead time

- **Tanggal:** 2026-10-14 · **Penguji:** agent penguji independen (bukan pembuat) · OpenClaw 2026.10.2 lokal, model `claude-sonnet-5`, home berisi hanya skill ini. Hasil SEBELUM/SESUDAH utuh: `00-openclaw-sebelum-sesudah.md`.

## Input (pesan pengguna)
> Mau beli gula pasir. Toko Makmur 15.500/kg, Agen Sinar 16.200/kg tapi gratis ongkir. Mending yang mana?

## Output SESUDAH (skill aktif)
> **Perbandingan 2 penawaran gula pasir: 10 kg (asumsi, qty belum disebut), tenggat belum disebut**
> Toko Makmur termurah dan direkomendasikan; selisihnya tipis (hampir seri) dengan Agen Sinar meski Agen Sinar gratis ongkir — ongkir gratisnya belum cukup menutup selisih harga per kg.
>
> | Pemasok | Total bayar (per kg) | Selisih vs termurah | Skor (peringkat) |
> |---|---|---|---|
> | Toko Makmur | Rp155.000 (Rp15.500) | termurah | 76,5 (1) |
> | Agen Sinar | Rp162.000 (Rp16.200) | +Rp7.000 (+4,5%) | 74,8 (2) |
>
> **Rekomendasi: Toko Makmur**
> 1. Lebih murah Rp7.000 untuk 10 kg (Rp15.500 vs Rp16.200/kg), meski Agen Sinar gratis ongkir — ongkirnya tidak menutupi selisih harga.
> 2. Lead time dan termin kedua pemasok belum disebutkan, jadi dinilai netral/sama.
> 3. Skornya hampir seri (beda 1,7 poin) — kalau Toko Makmur ternyata kena ongkir yang lumayan besar, posisinya bisa berbalik ke Agen Sinar.
>
> **Rincian singkat:**
> - Toko Makmur: Rp15.500/kg x 10 = Rp155.000; ongkir belum disebut; PKP/PPN belum jelas; lead time & termin belum disebut.
> - Agen Sinar: Rp16.200/kg x 10 = Rp162.000; ongkir gratis (franco); PKP/PPN belum jelas; lead time & termin belum disebut.
>
> **Kalau kondisinya berubah:** beli 2x (20 kg) → Toko Makmur tetap termurah (Rp310.000 vs Rp324.000); bila Toko Makmur ternyata kena ongkir di atas Rp7.000, Agen Sinar jadi lebih hemat; bagi pesanan 70/30 → Rp157.100, tambahan Rp2.100 dibanding full ke Toko Makmur.
>
> **Risiko yang perlu dijaga:** ongkir Toko Makmur belum diketahui (bisa membalik keputusan); status PKP/PPN kedua pemasok belum jelas (potensi tambahan Rp17.050-17.820 kalau PKP dan harga belum termasuk PPN); harga bisa berubah sewaktu-waktu, pastikan masih berlaku saat pesan.
>
> **Data yang belum ada:**
> - [isian: ongkir Toko Makmur ke alamat Anda]
> - [isian: jumlah kg yang sebenarnya dibutuhkan — asumsi di atas pakai 10 kg]
> - [isian: status PKP & apakah harga sudah termasuk PPN, untuk kedua pemasok]
>
> **Asumsi:** pembeli bukan PKP; bobot skor default; jumlah 10 kg (contoh, belum dikonfirmasi).
> Catatan: alat bantu keputusan pembelian, bukan nasihat pajak/hukum; pastikan harga & PPN tertulis di penawaran/faktur.
>
> Berapa kg sebenarnya yang mau dibeli, dan tahu berapa ongkir dari Toko Makmur kalau beli segitu?

## Catatan penguji
- **Nilai SESUDAH 6,5** (SEBELUM 7). Skill **tidak** memberi nilai tambah di input sependek ini.
- Perilaku patuh: hitung dulu dengan asumsi yang disebut, `[isian]` untuk ongkir/jumlah/PKP, satu pertanyaan di akhir, disclaimer.
- Angka benar untuk asumsi 10 kg (155.000 vs 162.000; skor 76,5/74,8; 2x 310.000/324.000; bagi 70/30 Rp157.100; potensi PPN 17.050/17.820).
- **Cacat:** kalimat inti "Toko Makmur termurah... ongkir gratisnya belum cukup menutup selisih" menyimpulkan seolah ongkir Toko Makmur Rp0, padahal belum diketahui (contoh di SKILL.md sendiri memakai "termurah sementara"). Model dasar justru lebih berguna: aturan impas umum "ongkir Toko Makmur < Rp700 × jumlah kg". Jumlah 10 kg dipilih sendiri. "Potensi PPN" untuk gula pasir menyesatkan karena gula konsumsi termasuk barang kebutuhan pokok yang dibebaskan PPN (lihat PERLU REVIEW di HASIL-UJI).
