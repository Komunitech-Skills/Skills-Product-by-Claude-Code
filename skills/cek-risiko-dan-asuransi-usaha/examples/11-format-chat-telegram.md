# 11 - Format chat Telegram/WhatsApp (v1.0.3)

Contoh bentuk jawaban mode chat. **Bukan hasil uji bot**: ini perakitan manual dari keluaran script `python3 scripts/cek_risiko.py risiko examples/data/01-kafe-bekasi.json --dana 47400000 --tampilan chat` (data fiktif, sama dengan skenario 01). Angka dan tingkat berasal dari script; kalimat "Langkah pencegahan", asumsi, perlindungan umum, dan pertanyaan adalah contoh tulisan agen. Uji ulang di bot Telegram asli menunggu penguji independen.

Tidak ada tabel, tiap pesan di bawah 3.500 karakter, istilah asuransi dijelaskan sekali dalam kurung.

## Pesan 1 (2350 karakter)

```
Asumsi: kafe kecil di ruko 2 lantai dekat kali, Bekasi; 3 karyawan; status BPJS belum diketahui.

Tiga prioritas teratas:
1. Banjir (dekat kali, pernah 2020) · TINGGI (skor 12)
2. Kebakaran dapur (kompor gas, korsleting) · TINGGI (skor 10)
3. Barista kunci keluar mendadak · SEDANG (skor 9)

Dana darurat (3 bulan biaya tetap):
- Biaya tetap per bulan: Rp15.800.000
- Target: Rp47.400.000
- Kas cadangan: Rp8.000.000 (cukup 0,5 bulan biaya tetap)
- Kekurangan: Rp39.400.000; bila dicicil 12 bulan: Rp3.283.334 per bulan

Rincian per risiko:
1. Banjir (dekat kali, pernah 2020) · TINGGI (skor 12 = kemungkinan 3 x dampak 4)
- Dampak kira-kira: lebih dari 3 bulan biaya tetap, bisa tutup berminggu-minggu (nilai 4 dari 5)
- Langkah pencegahan: stok dan kulkas dinaikkan ke rak/palet tinggi; simpan nota dan daftar aset di map plastik
- Perlindungan/asuransi: Ya, pertimbangkan
- Prioritas: 1 dari 9. Sikap: Kurangi + alihkan (asuransi/kontrak)

2. Kebakaran dapur (kompor gas, korsleting) · TINGGI (skor 10 = kemungkinan 2 x dampak 5)
- Dampak kira-kira: usaha bisa bangkrut / ada korban cedera berat (nilai 5 dari 5)
- Langkah pencegahan: pasang APAR (alat pemadam ringan) dan cek selang serta kompor gas; rapikan kabel colokan
- Perlindungan/asuransi: Ya, pertimbangkan
- Prioritas: 2 dari 9. Sikap: Kurangi + alihkan (asuransi/kontrak)

3. Barista kunci keluar mendadak · SEDANG (skor 9 = kemungkinan 3 x dampak 3)
- Dampak kira-kira: setara sekitar 1 bulan biaya tetap (nilai 3 dari 5)
- Langkah pencegahan: tulis resep dan SOP (prosedur kerja) ke buku; latih satu orang cadangan
- Perlindungan/asuransi: Tidak perlu
- Prioritas: 3 dari 9. Sikap: Kurangi + siapkan dana cadangan

4. Karyawan cedera kerja (luka bakar, terpeleset) · SEDANG (skor 9 = kemungkinan 3 x dampak 3)
- Dampak kira-kira: setara sekitar 1 bulan biaya tetap (nilai 3 dari 5)
- Langkah pencegahan: sarung tangan anti panas, lantai dapur dijaga kering; cek BPJS karyawan
- Perlindungan/asuransi: BPJS: kewajiban pemberi kerja, cek aturan terbaru (JKK/jaminan kecelakaan kerja untuk cedera di tempat kerja; BPJS Kesehatan untuk sakit)
- Prioritas: 4 dari 9. Sikap: Kurangi (K3/keselamatan kerja, perlengkapan kerja) + daftarkan BPJS karyawan

Ini pemetaan awam per 2026-10-17, bukan nasihat asuransi, keuangan, atau hukum.
Balas "lanjut" untuk sisa risiko dan jenis perlindungan.
```

## Pesan 2, setelah pengguna membalas "lanjut" (2778 karakter)

```
5. Mesin espresso rusak/listrik padam · SEDANG (skor 9 = kemungkinan 3 x dampak 3)
- Dampak kira-kira: setara sekitar 1 bulan biaya tetap (nilai 3 dari 5)
- Langkah pencegahan: servis mesin berkala; siapkan genset kecil atau power bank untuk kasir
- Perlindungan/asuransi: Tidak perlu
- Prioritas: 5 dari 9. Sikap: Kurangi + siapkan dana cadangan

6. Pelanggan sakit perut/keracunan · SEDANG (skor 8 = kemungkinan 2 x dampak 4)
- Dampak kira-kira: lebih dari 3 bulan biaya tetap, bisa tutup berminggu-minggu (nilai 4 dari 5)
- Langkah pencegahan: cek suhu dan tanggal bahan; catat pemasok; simpan sampel menu
- Perlindungan/asuransi: Ya, pertimbangkan
- Prioritas: 6 dari 9. Sikap: Kurangi + alihkan (asuransi/kontrak)

7. Pencurian kas/stok · SEDANG (skor 6 = kemungkinan 3 x dampak 2)
- Dampak kira-kira: setara beberapa hari omzet (nilai 2 dari 5)
- Langkah pencegahan: setor uang laci tiap sore; stok mahal dihitung mingguan
- Perlindungan/asuransi: Tidak perlu
- Prioritas: 7 dari 9. Sikap: Kurangi + siapkan dana cadangan

8. Gempa bumi · RENDAH (skor 4 = kemungkinan 1 x dampak 4)
- Dampak kira-kira: lebih dari 3 bulan biaya tetap, bisa tutup berminggu-minggu (nilai 4 dari 5)
- Langkah pencegahan: rak tinggi diikat ke dinding; jalur keluar tidak tertutup
- Perlindungan/asuransi: Ya, pertimbangkan
- Prioritas: 8 dari 9. Sikap: Kurangi + alihkan (asuransi/kontrak)

9. Bukti transfer palsu · RENDAH (skor 4 = kemungkinan 2 x dampak 2)
- Dampak kira-kira: setara beberapa hari omzet (nilai 2 dari 5)
- Langkah pencegahan: cek mutasi rekening sebelum barang diserahkan
- Perlindungan/asuransi: Tidak
- Prioritas: 9 dari 9. Sikap: Terima (cukup dana cadangan)

Jenis perlindungan umum yang layak ditanyakan ke agen asuransi terdaftar (nama umum, bukan merek):
- Asuransi kebakaran/properti: melindungi bangunan, isi, dan stok; cek apakah banjir dan gempa termasuk atau perlu tambahan.
- Tanggung gugat umum (tanggung jawab bila orang lain rugi atau cedera karena usaha Anda): untuk pelanggan sakit perut atau terpeleset.
- BPJS Ketenagakerjaan dan BPJS Kesehatan untuk karyawan: kewajiban pemberi kerja, cek aturan terbaru di sumber resmi.
Asuransi mengalihkan kerugian besar yang jarang terjadi; ia bukan pengganti langkah murah, dan ada premi (biaya asuransi), pengecualian (hal yang tidak dijamin), dan batas klaim (permintaan ganti rugi).

Disclaimer: bukan nasihat asuransi, keuangan, atau hukum. Polis (surat perjanjian asuransi) dibeli lewat perusahaan berizin OJK (Otoritas Jasa Keuangan) dan agen terdaftar; baca sendiri isinya. Aturan BPJS dan perluasan banjir/gempa berubah, cek sumber resmi per 2026-10-17.

Boleh dijawab (maks 3):
1. Berapa perkiraan nilai peralatan dan stok kafe?
2. Karyawan sudah terdaftar BPJS belum?
3. Ruko ini sewa atau milik sendiri?
```
