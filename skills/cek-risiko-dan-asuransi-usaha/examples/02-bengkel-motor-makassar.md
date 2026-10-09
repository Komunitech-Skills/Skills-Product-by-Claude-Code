# 02 — Normal: bengkel motor, Makassar

**Pesan:**
> bengkel motor sy di depan rumah, makassar. mekanik 2, yg senior udh 8 thn sm sy, kl dia ga masuk bengkel ampir lumpuh. motor pelanggan kdg nginep. biaya tetap: gaji 7jt total, listrik 900rb, cicilan kompresor 650rb, lain2 500rb. tabungan usaha 20jt. perlu asuransi ga sih?

**Data risiko:** `data/02-bengkel-makassar.json`. Dana: `dana --biaya "Gaji=7000000,Listrik=900000,Cicilan kompresor=650000,Lain=500000" --bulan 3 --kas 20000000`.

**Output SESUDAH (ringkas):**
> Asumsi: bengkel di rumah sendiri, Makassar; 2 mekanik.
>
> | No | Risiko | K | D | Skor/Tingkat | Langkah murah | Perlu asuransi? |
> |---|---|---|---|---|---|---|
> | 1 | Mekanik senior keluar/sakit | 3 | 4 | 12 TINGGI | Catat SOP servis & langganan pelanggan, latih mekanik kedua | Ya, pertimbangkan |
> | 2 | Kebakaran (bensin, oli, korsleting) | 2 | 5 | 10 TINGGI | APAR, bensin di jeriken tertutup jauh dari las/gerinda, ganti kabel tua | Ya, pertimbangkan |
> | 3 | Mekanik cedera kerja | 3 | 3 | 9 SEDANG | Sarung tangan, kacamata gerinda; BPJS Ketenagakerjaan | Tidak perlu |
> | 4 | Gempa bumi | 2 | 4 | 8 SEDANG | Rak sparepart diikat ke dinding | Ya, pertimbangkan |
> | 5 | Motor pelanggan hilang/rusak saat dititip | 2 | 4 | 8 SEDANG | Kunci ganda, CCTV, tanda terima titipan | Ya, pertimbangkan |
> | 6 | Pencurian alat/sparepart | 3 | 2 | 6 SEDANG | Lemari alat terkunci, hitung stok mingguan | Tidak perlu |
> | 7 | Pemasok sparepart tunggal berhenti | 2 | 2 | 4 RENDAH | Simpan 1 kontak pemasok kedua | Tidak |
>
> Dana darurat 3 bulan: biaya tetap Rp9.050.000/bln → target **Rp27.150.000**; kas Rp20.000.000 (cukup ±2,2 bln); kekurangan **Rp7.150.000** → 6 bulan Rp1.191.667/bln.
> Perlindungan umum: kebakaran/properti (isi & bangunan; perluasan gempa dicek per polis), tanggung gugat/titipan kendaraan pihak ketiga (tanyakan ke agen apakah motor titipan bisa dijamin), BPJS. Disclaimer + 3 pertanyaan (nilai alat & stok, rumah milik sendiri?, zona gempa).

**Verifikasi:** skor 12,10,9,8,8,6,4 cocok; 7.000.000+900.000+650.000+500.000 = 9.050.000; ×3 = 27.150.000; −20.000.000 = 7.150.000; /6 = 1.191.666,7 → 1.191.667. Cocok.

**Catatan:** baris 1 "Perlu asuransi: Ya, pertimbangkan" untuk mekanik keluar diwarisi dari aturan angka script. Untuk mekanik **sakit/meninggal** ada padanan (asuransi jiwa/kecelakaan orang kunci), tetapi **keluar kerja** tidak bisa diasuransikan → menyesatkan bila disalin apa adanya (cacat B2). "Makassar rawan gempa 2" adalah penilaian penguji; skill benar menyuruh cek peta BMKG/BNPB.

**Skor: SEBELUM 6,5 · SESUDAH 7,5.**
