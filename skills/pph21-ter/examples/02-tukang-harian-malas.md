# 02 — Pekerja harian (permintaan singkat)

**Skenario:** S2 — permintaan singkat/malas.

**Input pengguna (persis):**
> bikinin dong itungan pph tukang harian 300rb sehari kerja 20 hari

**Perintah:** `python3 scripts/pph21.py harian --upah 300rb --hari 20`

**Output:**

**PPh 21 pegawai tidak tetap (harian/borongan)**
- Upah: Rp 6.000.000 untuk 20 hari → dasar upah harian: Rp 300.000
- Metode: TER harian 0% × Rp 300.000 = Rp 0 per hari
- **Total PPh 21 20 hari: Rp 0**

Catatan:
- Untuk pegawai tidak tetap yang TIDAK dibayar bulanan. Yang dibayar bulanan memakai TER bulanan (subperintah 'bulan').
- Sampai Rp 2.500.000 sehari: TER harian (0% s.d. Rp 450.000; 0,5% di atasnya). Di atas Rp 2.500.000 sehari: tarif Pasal 17 × 50% bruto sehari.
- Pemotong membuat bukti potong per hari kerja (PMK 168/2023, contoh Lampiran).
- PPh 21 dibulatkan ke bawah ke rupiah penuh; PKP dibulatkan ke bawah hingga ribuan rupiah (PMK 168/2023 Pasal 8 ayat 4). Pembulatan belum dicocokkan dengan Coretax; bila Coretax menampilkan angka berbeda, ikuti Coretax.

_Alat bantu hitung, bukan nasihat pajak. Dasar: PP 58/2023 (tarif TER), PMK 168/2023 (tata cara PPh 21), UU 7/2021 HPP (PTKP & tarif Pasal 17), PMK 105/2025 (PPh 21 DTP 2026), berlaku per 23 September 2026. Untuk kasus khusus (ekspatriat, pesangon, pensiun, natura, gross-up) hubungi Kring Pajak 1500200 atau konsultan pajak._

Jadi untuk tukang dengan upah Rp 300.000/hari **tidak ada PPh 21 yang dipotong** (upah harian masih di bawah Rp 450.000). Tetap buat bukti potong (nihil) per hari kerja bila diminta sistem Coretax.

**Catatan penguji:**
- Benar: batas TER harian 0% s.d. Rp 450.000 (Lampiran D PP 58/2023) dan contoh resmi Tuan L (Rp 450.000 → Rp 0).
- Permintaan singkat langsung dijawab tanpa bertanya ulang (tidak perlu PTKP untuk TER harian) — sesuai prinsip "instan".
- Uji tepi tambahan oleh penguji: Rp 450.000 → 0; Rp 450.001 → Rp 2.250; Rp 500.000 → Rp 2.500 (Tuan K); Rp 3.000.000/hari → Rp 75.000 (Tuan M & Z). Semua cocok.
