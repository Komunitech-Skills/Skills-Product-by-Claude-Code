# 09 (uji ulang v1.0.1) — Input tidak lengkap: toko bangunan, tanpa angka

- Tanggal: 2026-10-09 · Penguji independen · `claude-code (simulasi agent)`
- Data risiko: `data/09-toko-bangunan-uji-ulang.json`

## Pesan
> toko bangunan sy perlu asuransi apa? dana darurat brp?

## Perilaku yang diharapkan (SKILL.md)
Kerjakan dulu dengan asumsi default (ruko di kota besar, 2 karyawan, status BPJS tidak diketahui), nilai aset `[isian]`, dana darurat `[isian]` karena biaya tetap tidak ada; maksimal 3 pertanyaan di akhir. Script `dana` **tidak** dijalankan (tidak ada angka); tidak boleh mengarang biaya.

## Output SESUDAH (ringkas)
> **Asumsi:** toko bangunan di ruko, kota besar, 2 karyawan, status BPJS belum diketahui, ada 1 pick-up antar; nilai stok `[isian: nilai aset]`.
>
> | No | Risiko | K | D | Skor/Tingkat | Langkah murah | Perlu asuransi? |
> |---|---|---|---|---|---|---|
> | 1 | Piutang tukang/kontraktor macet | 4 | 3 | 12 TINGGI | Batas utang per pelanggan, DP untuk pesanan besar, nota ditandatangani | Tidak ada asuransi umum; pakai mitigasi lain |
> | 2 | Kebakaran (cat, thinner, kabel) | 2 | 5 | 10 TINGGI | Cat & thinner dipisah dari sumber panas, APAR, larangan merokok | Ya, pertimbangkan |
> | 3 | Karyawan cedera angkat semen/besi | 3 | 3 | 9 SEDANG | Troli, sarung tangan, angkat berdua | BPJS (wajib bagi pemberi kerja, cek aturan terbaru) |
> | 4 | Pencurian stok/uang | 3 | 3 | 9 SEDANG | Stok opname mingguan, setor kas harian | Tidak perlu |
> | 5 | Barang jatuh menimpa pelanggan | 2 | 4 | 8 SEDANG | Rak besi diikat, besi beton tidak disandarkan di jalur pelanggan | Ya, pertimbangkan (tanggung gugat umum) |
> | 6 | Pick-up antar kecelakaan | 2 | 4 | 8 SEDANG | Sopir istirahat cukup, muatan diikat, servis rutin | Ya, pertimbangkan (asuransi kendaraan) |
> | 7 | Banjir merusak semen/gypsum | 2 | 3 | 6 SEDANG | Semen di palet, gypsum di rak | Tidak perlu |
>
> **Dana darurat:** target = biaya tetap per bulan × 3 = **[isian: biaya tetap per bulan] × 3**. Begitu Bapak/Ibu kirim angkanya (sewa, gaji, listrik, cicilan), saya hitung pasti beserta kekurangan dan cicilan menabungnya.
> Perlindungan umum tanpa merek; disclaimer.
> Pertanyaan: 1) Biaya tetap per bulan (sewa, gaji, listrik, cicilan)? 2) Kas cadangan sekarang? 3) Berapa karyawan dan sudah ikut BPJS?

## Verifikasi
Skor 12, 10, 9, 9, 8, 8, 6 cocok (Decimal). Tidak ada angka rupiah yang dikarang.

## Catatan penguji
Perilaku sesuai aturan "kerjakan dulu, tanya di akhir" (3 pertanyaan). Baris 3 kembali butuh penimpaan label BPJS oleh agent (R1).

**Skor: SESUDAH 8,5.**
