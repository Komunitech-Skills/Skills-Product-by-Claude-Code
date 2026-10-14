# 03 - Input tidak lengkap: 2 harga gula pasir tanpa jumlah & lead time

- **Tanggal:** 2026-10-14 (putaran 2, versi 1.0.1) · **Penguji:** agent penguji independen (bukan pembuat) · OpenClaw 2026.10.2 lokal, model `claude-sonnet-5`, home bersih berisi hanya skill ini. Hasil SEBELUM/SESUDAH utuh: `00-openclaw-sebelum-sesudah.md`.

## Input (pesan pengguna)
> Mau beli gula pasir. Toko Makmur 15.500/kg, Agen Sinar 16.200/kg tapi gratis ongkir. Mending yang mana?

## Output SESUDAH (skill 1.0.1, uji lokal)
> **Perbandingan 2 penawaran gula pasir: 1 kg (asumsi, karena jumlah belum disebutkan)**
>
> | Pemasok | Total bayar (per kg) | Selisih vs termurah | Skor (peringkat) |
> |---|---|---|---|
> | Toko Makmur | Rp15.500 | termurah sementara | 76,5 (1) |
> | Agen Sinar | Rp16.200 | lebih mahal Rp700 (4,5%) | 74,8 (2) |
>
> **Rekomendasi: Toko Makmur**
> - Peringkat: 1. Toko Makmur (skor 76,5), 2. Agen Sinar (skor 74,8). Skornya hampir seri dengan Agen Sinar (beda 1,7 poin).
> - Toko Makmur adalah yang termurah (sementara: ongkir belum diketahui): Toko Makmur lebih murah Rp700 daripada Agen Sinar untuk 1 kg.
> - Bila jumlahnya 2x (2 kg): termurah tetap Toko Makmur (Rp31.000).
> - Ongkir Toko Makmur belum diketahui (total di atas belum termasuk ongkir): Toko Makmur tetap tidak lebih mahal daripada Agen Sinar selama ongkirnya maksimal Rp700 untuk 1 kg.
> - Gula pasir kemungkinan termasuk bahan pokok yang dibebaskan PPN (PP 49/2022), jadi PPN tidak ditambahkan untuk pemasok yang status PKP-nya belum jelas; cek status barang.
>
> **Rincian singkat:**
> - Toko Makmur: Rp15.500/kg, ongkir belum diketahui, status PPN belum jelas, lead time & termin tidak disebut.
> - Agen Sinar: Rp16.200/kg, ongkir gratis, status PPN belum jelas, lead time & termin tidak disebut.
>
> **Risiko:**
> - Ongkir Toko Makmur belum tahu nominalnya — kalau lebih dari Rp700/kg, Agen Sinar justru lebih hemat total.
> - Harga bisa berubah sewaktu-waktu, belum ada konfirmasi tertulis/struk dari kedua toko.
> - Belum jelas kualitas, lead time, dan cara bayar — jadi perbandingan baru lihat dari sisi harga.
>
> **Pesan WA (siap kirim):**
> - Ke Toko Makmur: "Halo, mau tanya kalau beli gula pasir, ongkir ke [alamat] berapa ya? Harga Rp15.500/kg masih berlaku sampai kapan?"
> - Ke Agen Sinar: "Halo, untuk gratis ongkir ke [alamat] apakah ada minimal pembelian? Harga Rp16.200/kg sudah termasuk PPN atau belum ya?"
>
> **Data yang belum ada:** [isian: jumlah kg yang mau dibeli], [isian: ongkir Toko Makmur ke alamat Anda], [isian: minimal pembelian untuk gratis ongkir Agen Sinar], [isian: status PPN kedua toko]
> **Asumsi:** Dihitung untuk 1 kg karena jumlah belum disebutkan; pembeli bukan PKP.
> Catatan: Perbandingan ini alat bantu keputusan, bukan nasihat pajak/hukum — cek harga & syarat resmi sebelum beli.
>
> Pertanyaan:
> 1. Mau beli berapa kg?
> 2. Ada minimal pembelian untuk gratis ongkir di Agen Sinar?
> 3. Kalau beli kecil (1-2 kg), kira-kira ongkir Toko Makmur berapa?

## Catatan penguji (1.0.1)
- **Nilai SESUDAH 8** (SEBELUM 7).
- Kini dihitung per 1 kg sehingga hasilnya menjadi aturan umum: "termurah sementara" + "Agen Sinar justru lebih hemat bila ongkir Toko Makmur lebih dari Rp700/kg". Ini sama kuatnya dengan aturan impas model dasar, ditambah struktur, WA, `[isian]`, dan disclaimer.
- Catatan PP 49/2022 (gula pasir kemungkinan bebas PPN) membuat potensi PPN tidak ditambahkan lagi. Ini memperbaiki temuan PERLU REVIEW putaran 1.
- Kerja dulu, 3 pertanyaan di akhir.
- Kekurangan kecil: baris "bila 2x (2 kg)" tidak berguna; status "hampir seri" disebut walau data lain kosong.

## Riwayat
- 1.0.0: SESUDAH 6,5. Asumsi 10 kg dipilih sendiri, kalimat utama menganggap ongkir yang belum diketahui = Rp0, dan potensi PPN ditambahkan untuk gula.
