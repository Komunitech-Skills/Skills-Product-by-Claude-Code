# Uji A/B: tanpa skill vs dengan skill (skenario normal 1)

- Tanggal: 2026-10-09
- Penguji: agent independen (bukan pembuat), hanya membaca salinan folder skill di scratchpad.
- Platform: `claude-code (simulasi agent)`. Router model OpenClaw sedang mati (HTTP 530), jadi uji OpenClaw sebelum/sesudah tidak dijalankan dan `00-openclaw-sebelum-sesudah.md` belum dibuat.
- Berkas ini **mengganti** berkas parsial dari uji sebelumnya yang terputus; isi lama tidak dipakai.
- **Bias jujur:** kedua sisi disimulasikan dan dinilai oleh penguji yang sama (model sama). Sisi tanpa skill ditulis lebih dulu tanpa menerapkan SKILL.md, sebagai jawaban wajar model dasar. Selisih skor perlu dikonfirmasi lewat uji OpenClaw.

## Pesan pengguna (identik)

Lihat `01-jual-warung-bakso.md` (Pak Darto, warung bakso Klaten; laba 2023-2025 Rp84/97/91 juta setelah ambilan Rp3 juta/bulan; penjaga Rp3,5 juta/bulan; renovasi 2024 Rp12 juta sekali; alat Rp65 juta turun 25%; utang koperasi Rp18 juta; kelipatan 2-3; potongan resep 20%; biaya 4%; kebutuhan Rp6 juta × 18 bulan).

## SEBELUM (tanpa skill)

> Pak Darto, berikut gambaran kasarnya.
>
> **Perkiraan harga.** Rata-rata laba 3 tahun = (84 + 97 + 91) / 3 ≈ Rp90,7 juta. Dengan 2-3 kali laba: Rp181 juta - Rp272 juta. Karena resep hanya Bapak yang tahu, dipotong 20%: sekitar **Rp145 juta - Rp218 juta**. Dikurangi biaya notaris/perantara 4%: sekitar **Rp139 juta - Rp209 juta**. Kalau hanya alatnya dijual: Rp65 juta × 75% = Rp48,75 juta, dikurangi utang Rp18 juta = sekitar Rp30,75 juta.
>
> Kebutuhan 18 bulan × Rp6 juta = Rp108 juta, jadi kalau laku di kisaran itu kebutuhan Bapak tertutup, masih sisa Rp31-101 juta. Umumnya warung makan kecil memang dijual sekitar 1-3 kali laba setahun, jadi tawaran tetangga 2 kali laba cukup wajar.
>
> **Yang perlu disiapkan:**
> 1. Catatan keuangan 3 tahun yang rapi.
> 2. Resep ditulis dan ada orang yang dilatih.
> 3. Tanya pemilik kios apakah sewa bisa dioper.
> 4. Lunasi utang koperasi atau sepakati dengan pembeli.
> 5. Siapkan surat-surat (NIB, BPKB motor).
> 6. Buat perjanjian jual beli di notaris supaya aman.
>
> Semoga lancar, Pak!

**Nilai: 6,0/10.** Angka aritmetikanya benar untuk pendekatan sederhana, tetapi tidak memakai informasi penting yang sudah diberikan (ambilan pemilik vs gaji penjaga, renovasi sekali jalan), sehingga laba tidak disesuaikan; menyebut "umumnya 1-3 kali laba" sebagai fakta pasar tanpa sumber; utang tidak dikurangkan dari hasil yang dibandingkan dengan kebutuhan; tidak ada rencana per bulan, daftar dokumen, perlindungan kerahasiaan, pilihan struktur, maupun daftar pertanyaan untuk notaris/konsultan pajak; tidak ada disclaimer.

## SESUDAH (dengan skill)

Output utuh ada di `01-jual-warung-bakso.md`.

**Nilai: 6,5/10.** Jauh lebih lengkap dan siap pakai: daftar periksa 12 area berstatus (tidak ditebak), 4 prioritas, tabel metode + rumus, rencana transisi 12 bulan, daftar dokumen dengan aturan kerahasiaan, pilihan struktur, pertanyaan untuk notaris/konsultan pajak, label "asumsi Bapak, bukan angka pasar", disclaimer + tanggal acuan, maks 3 pertanyaan. **Namun** ada kesalahan angka dari rumus skill: renovasi sekali jalan 2024 ditambahkan ke ketiga tahun, sehingga batas atas terlalu tinggi Rp28.000.000 dan tren laba turun tertutupi; perbandingan dengan kebutuhan pensiun juga tidak mengurangi utang Rp18 juta. Kesalahan angka diberi bobot berat.

## Kesimpulan A/B

Selisih **+0,5** (6,0 → 6,5). Tanpa cacat angka, sisi sesudah diperkirakan ±8,5 (selisih ±2,5): nilai tambah struktur skill nyata, tetapi tertutup oleh kesalahan hitung yang dibawa rumus `--biaya-sekali`.
