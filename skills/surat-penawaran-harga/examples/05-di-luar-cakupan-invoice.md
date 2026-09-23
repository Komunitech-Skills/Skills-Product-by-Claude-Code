# 05 — Di luar cakupan: minta tagihan (invoice) setelah barang dikirim

**Skenario:** S5 — pengguna meminta dokumen tagihan, bukan penawaran.

**Input pengguna:**
> Barang udah aku kirim ke PT Fiktif Sentosa kemarin, total 12 juta belum PPN, aku PKP. Tolong bikinin surat tagihannya, jatuh tempo 30 hari.

## Output

Karena barangnya sudah dikirim, dokumen yang tepat adalah **invoice (tagihan)**, bukan surat penawaran harga. Surat penawaran dipakai *sebelum* pembeli memesan.

- Jika skill **`buat-invoice`** terpasang, ketik saja: *"buatkan invoice untuk PT Fiktif Sentosa, total 12 juta belum PPN, saya PKP, jatuh tempo 30 hari"* — skill itu yang mengatur nomor invoice, jatuh tempo, dan rekening.
- Sebagai gambaran angka (dihitung dengan kalkulator SPH, mode PKP non-mewah): DPP Rp 12.000.000 → PPN 12% × DPP nilai lain 11/12 = **Rp 1.320.000** → total **Rp 13.320.000**.
- Ingat: faktur pajak resminya tetap dibuat lewat **Coretax** oleh PKP; invoice/SPH bukan faktur pajak.

Kalau ternyata Anda memang ingin mengirim **penawaran baru** untuk pesanan berikutnya, kabari saja, saya buatkan SPH-nya.

## Catatan penguji
- Sesuai bagian "Kapan TIDAK digunakan": mengarahkan ke `buat-invoice`, tidak memaksakan format SPH.
- Nilai tambah: tetap memberi gambaran PPN yang benar (12.000.000 × 11% = 1.320.000, diverifikasi) tanpa berpura-pura membuat invoice.
- Catatan: skill merujuk `buat-invoice`/`hitung-ppn`; bila pembeli tidak memiliki skill tersebut, arahan hanya berupa saran. SKILL.md sebaiknya memberi kalimat cadangan untuk kasus itu (ringan).
