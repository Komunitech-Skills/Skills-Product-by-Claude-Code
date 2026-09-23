# 04 — Input tidak lengkap

**Skenario:** S4 — status PTKP tidak disebut, gaji ≤ Rp 10 juta di 2026 (perlu cek DTP).

**Input pengguna (persis):**
> Tolong hitung PPh 21 karyawan saya yang gajinya 9 juta ya

**Output (agent bertanya sekali, sesuai SKILL.md):**

> Siap, saya hitungkan. Supaya angkanya tepat, mohon jawab singkat:
> 1. Status PTKP karyawan per 1 Januari 2026: belum/sudah menikah, dan jumlah tanggungan (mis. TK/0, K/1, K/3)?
> 2. Yang dihitung satu bulan saja (Januari–November) atau setahun penuh sampai Desember?
> 3. Apakah ada potongan JHT 2% + JP 1% dari gajinya (ikut BPJS Ketenagakerjaan)? Dan apakah perusahaan membayar premi JKK/JKM/BPJS Kesehatan (ini ikut dihitung sebagai penghasilan bruto)?
> 4. Ada THR/bonus tahun ini? Bulan apa dan berapa?
> 5. Apakah usaha Anda di industri alas kaki, tekstil & pakaian jadi, furnitur, kulit & barang kulit, atau pariwisata (KLU utama tercantum di Lampiran A PMK 105/2025)? Kalau ya, PPh 21-nya bisa ditanggung pemerintah di 2026.
>
> Kalau mau cepat: sebutkan saja status PTKP-nya, sisanya saya pakai asumsi (tanpa iuran, tanpa THR, bukan sektor DTP) dan saya sebutkan asumsinya.

**Tindak lanjut (bila pengguna menjawab "K/1, sebulan aja, bukan industri itu"):**
`python3 scripts/pph21.py bulan --ptkp K/1 --bruto 9jt` → TER kategori B, baris di atas Rp 7.300.000 s.d. Rp 9.200.000 → tarif 1% → **PPh 21 Rp 90.000** (terverifikasi independen).

**Catatan penguji:**
- Pertanyaan satu kali, bernomor, maks. 5, dengan jalur cepat — sesuai prinsip produk.
- Pertanyaan DTP muncul tepat karena gaji ≤ Rp 10 juta dan tahun 2026, tanpa menganggap perusahaan berhak.
