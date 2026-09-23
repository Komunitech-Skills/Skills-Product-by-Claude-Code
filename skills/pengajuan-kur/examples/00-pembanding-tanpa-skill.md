# 00 — Uji A/B: S1 dengan skill vs tanpa skill

**Input (sama dengan S1):**
> Saya punya bengkel las "Las Contoh Jaya" di Bekasi, udah jalan 4 tahun, punya NIB, karyawan 3 orang. Laba bersih sekitar 6 juta sebulan. Mau ajukan KUR BRI 100 juta 5 tahun buat beli mesin las & mesin bending 70 juta sama stok besi 30 juta. Tolong siapin semua yang perlu, sama cicilannya berapa, kuat nggak saya?

## A. Tanpa skill (agent umum, tanpa membaca skill/aturan)

> **Simulasi cicilan KUR BRI**
> Bunga KUR saat ini 6% per tahun. Dengan pinjaman Rp 100.000.000 selama 60 bulan:
> - Pokok per bulan: Rp 100.000.000 / 60 = Rp 1.666.667
> - Bunga per bulan: Rp 100.000.000 × 6% / 12 = Rp 500.000
> - **Cicilan per bulan: Rp 2.166.667**
>
> **Kemampuan bayar:** cicilan Rp 2.166.667 dari laba Rp 6.000.000 = 36%. Umumnya bank menoleransi cicilan hingga 30–40% dari penghasilan, jadi **masih cukup aman**.
>
> **Syarat & dokumen KUR BRI:** KTP, KK, NPWP, surat keterangan usaha / NIB, pas foto, usaha minimal 6 bulan, tidak sedang punya kredit lain, **agunan tambahan (BPKB/sertifikat) biasanya diminta untuk pinjaman di atas Rp 50 juta**.
>
> **Profil usaha (contoh):** Las Contoh Jaya adalah bengkel las yang telah berdiri 4 tahun dengan 3 karyawan dan pelanggan tetap dari kontraktor di Bekasi. Dengan mesin baru, kapasitas produksi diperkirakan naik 50%…
>
> **Tips:** siapkan dokumen lengkap agar pengajuan cepat disetujui.

## B. Dengan skill
Lihat `01-bengkel-las-100jt.md`: anuitas Rp 1.933.280 (yang berlaku untuk KUR, Pasal 37) vs ilustrasi flat Rp 2.166.667, rasio 32,2% 🟡 BERAT + plafon aman ± Rp 93,1 jt, rencana dana 70/30 ✔ + peringatan batas tenor modal kerja 36 bulan, profil usaha dengan `[isi: …]`, checklist Permenko (NPWP wajib > Rp50 jt) vs "cek ke bank", hak **tanpa agunan tambahan s.d. Rp100 jt**, disclaimer.

## Penilaian
| Aspek | Tanpa skill | Dengan skill |
|---|---|---|
| Metode cicilan | Flat — keliru untuk KUR (bunga KUR ditetapkan **efektif**; flat 6% setara ±10,85%) → cicilan dilebih-lebihkan Rp 233.387/bulan | Anuitas + penjelasan flat vs efektif dengan angka |
| Penilaian kemampuan bayar | "Masih cukup aman" pada 36% (ambang longgar tanpa dasar) | 32,2% → 🟡 BERAT + alternatif konkret |
| Fakta aturan | **Salah**: agunan tambahan > Rp50 jt (Permenko 1/2026 Pasal 20: dilarang s.d. Rp100 jt); "tidak sedang punya kredit lain" terlalu sempit/keliru (KPR, kartu kredit dll. boleh, Pasal 35) | Sesuai teks Permenko, dengan pasal |
| Narasi | Mengarang "pelanggan tetap dari kontraktor", "kapasitas naik 50%" | Hanya fakta pengguna + `[isi: …]` |
| Tenor campuran | Tidak dibahas | Peringatan modal kerja maks 36 bulan |
| Janji | "agar cepat disetujui" (nada menjanjikan) | Disclaimer tegas, tidak menjanjikan |

**Kesimpulan:** skill **jelas lebih baik** — lebih akurat (angka & aturan), lebih jujur, dan lebih siap pakai. (Output "tanpa skill" adalah simulasi penguji yang mencerminkan kesalahan umum: metode flat, agunan > Rp50 jt, narasi karangan.)
