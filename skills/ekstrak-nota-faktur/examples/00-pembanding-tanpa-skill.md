# 00 — Uji A/B: S1 tanpa skill vs dengan skill

**Input (sama dengan S1):** "Tolong masukin 4 nota ini ke Excel ya, sekalian dicek angkanya bener nggak." Dokumennya: struk minimarket (termasuk PPN), nota tulisan tangan yang totalnya salah jumlah Rp 10.000, invoice servis AC ber-PPN 12% × 11/12, dan kuitansi sewa tenda Rp 7.500.000 tanpa meterai terlihat. Transkripsi lengkap ada di `01-rekap-4-nota-toko-kue.md`.

## A. Tanpa skill (jawaban AI agent biasa, tanpa membaca skill apa pun)

> Berikut data dari 4 nota Anda:
>
> | No | Tanggal | Toko | Keterangan | Jumlah |
> |---|---|---|---|---|
> | 1 | 03/09/2026 | Minimarket Sumber Rejeki Fiktif | Gula, tepung, margarin | Rp 119.200 |
> | 2 | 05/09/2026 | Toko Bahan Kue Aneka Fiktif | Coklat, keju, mentega | Rp 730.500 |
> | 3 | 10/09/2026 | CV Sejuk Teknik Fiktif | Servis AC + freon (termasuk PPN 12%) | Rp 1.443.000 |
> | 4 | 12/09/2026 | Persewaan Tenda Pak Budi | Sewa tenda & kursi | Rp 7.500.000 |
> | | | | **Total** | **Rp 9.792.700** |
>
> Pengecekan:
> - Nota 2: jika dijumlah, 310.000 + 196.000 + 214.500 = Rp 720.500, sedangkan di nota tertulis Rp 730.500. Ada selisih Rp 10.000.
> - Invoice 3: PPN 12% dari Rp 1.300.000 seharusnya Rp 156.000, tetapi tertulis Rp 143.000. Sebaiknya dikonfirmasi ke penjual.
> - Lainnya sudah sesuai.
>
> Anda bisa menyalin tabel di atas ke Excel.

## B. Dengan skill `ekstrak-nota-faktur`
Lihat `01-rekap-4-nota-toko-kue.md`: status per dokumen, selisih N2 Rp 10.000, pengingat **meterai** kuitansi > Rp 5 juta, PPN struk dan invoice **dinyatakan benar** (12% × 11/12 = efektif 11%), terbilang dicek, rekap per kategori/penjual/bulan, PPN tercantum vs PPN dari faktur pajak, dan CSV `;` siap buka di Excel (UTF-8 BOM, NPWP ber-nol di depan aman).

## Penilaian

| Aspek | Tanpa skill | Dengan skill |
|---|---|---|
| Aturan PPN 2025+ | ❌ **Salah menuduh** invoice 3 kurang PPN (memakai 12% × DPP penuh). Pengguna bisa menagih vendor secara keliru. | ✅ 12% × DPP nilai lain 11/12, disertai rumus |
| Selisih nota tulisan tangan | ✅ Ditemukan | ✅ Ditemukan, status "Ada selisih" |
| Meterai / terbilang | ❌ Tidak dicek | ✅ Dicek (UU 10/2020, terbilang dibaca menjadi angka) |
| Konsistensi & ketelitian | Hitung manual, tanpa jejak | Script deterministik, terverifikasi independen |
| Siap pakai Excel | Tabel markdown (disalin manual) | CSV `;` + BOM, angka tanpa titik ribuan |
| Rekap | Total saja | Per kategori, penjual, bulan, dan PPN |

**Kesimpulan A/B:** skill **jelas lebih baik**. Tanpa skill, agent membuat kesalahan pajak yang penting: PPN yang sebenarnya benar dianggap kurang, karena memakai tarif 12% × DPP penuh. Agent tanpa skill juga melewatkan meterai dan terbilang, dan tidak menghasilkan file siap Excel.
