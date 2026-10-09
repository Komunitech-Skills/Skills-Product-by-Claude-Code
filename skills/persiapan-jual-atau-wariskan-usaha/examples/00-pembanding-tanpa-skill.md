# Uji A/B: tanpa skill vs dengan skill (skenario normal 1)

- Tanggal: 2026-10-09
- Penguji: agent independen (bukan pembuat), hanya membaca folder skill.
- Platform: `claude-code (simulasi agent)`. **Tidak ada akses OpenClaw/kunci model di sesi ini**, jadi uji `uji.sh`/`uji-tg.sh` dari brief tidak dijalankan dan file `00-openclaw-sebelum-sesudah.md` tidak dibuat.
- **Bias jujur:** tidak tersedia agent/penilai terpisah untuk sisi tanpa-skill. Kedua sisi disimulasikan oleh penguji yang sama (model yang sama), sisi tanpa-skill ditulis lebih dulu sebelum menerapkan SKILL.md. Penilai juga sama. Selisih skor bisa terlalu besar atau terlalu kecil; perlu dikonfirmasi lewat uji OpenClaw sebelum/sesudah.
- Semua angka sisi SESUDAH berasal dari `scripts/nilai_usaha.py` dan diverifikasi ulang secara independen (pecahan Python `fractions`, lihat `HASIL-UJI.md`).

## Pesan pengguna (identik di kedua sisi)

> Bu Sri di sini, punya warung makan "Dapur Bu Sri" di Semarang sudah 9 tahun, tempatnya sewa. Saya mau pensiun, rencananya dioper ke orang lain tahun depan. Laba bersih kira2: 2023 96 juta, 2024 118 juta, 2025 134 juta. Itu sudah dipotong gaji saya sendiri 4 juta/bulan. Kalau nanti ada manajer pengganti kira-kira digaji 5 juta/bulan. Alat masak, freezer, etalase, motor kira2 210 juta tapi sudah tua, anggap saja turun 30%. Masih ada sisa KUR 45 juta. Pernah ada perantara bilang warung begini biasanya 2 sampai 3 kali laba. Resep semua di kepala saya, jadi potong saja 15%. Biaya notaris/perantara anggap 5%. Setelah pensiun saya butuh 8 juta/bulan untuk 2 tahun. Kira2 warung saya laku berapa dan apa yang harus saya siapkan?

## SEBELUM (tanpa skill)

> Bu Sri, selamat atas 9 tahun usahanya! Berikut gambaran kasar nilai warung Ibu dan hal yang perlu disiapkan.
>
> **1. Perkiraan nilai**
> Rata-rata laba 3 tahun: (96 + 118 + 134) / 3 = Rp116 juta. Dengan kelipatan 2–3 kali dari perantara: **Rp232 juta – Rp348 juta**.
> Karena resep masih di kepala Ibu, dipotong 15%: **sekitar Rp197 juta – Rp296 juta**.
> Aset Rp210 juta turun 30% = Rp147 juta, dikurangi KUR Rp45 juta = Rp102 juta. Jadi kalau dijual hanya asetnya, sekitar Rp102 juta.
> Setelah biaya notaris/perantara 5%, kira-kira Ibu terima **Rp187 juta – Rp281 juta**.
> Kebutuhan 2 tahun: 8 juta × 24 = Rp192 juta. Jadi kalau harga di batas bawah, pas-pasan; di batas atas ada sisa sekitar Rp89 juta.
>
> **2. Yang perlu disiapkan**
> - Rapikan pembukuan 3 tahun terakhir.
> - Tulis resep dan SOP dapur supaya pembeli yakin warung bisa jalan tanpa Ibu.
> - Cek kontrak sewa: sisa berapa lama, boleh dialihkan atau tidak.
> - Lunasi atau jelaskan sisa KUR.
> - Siapkan NIB/izin, daftar karyawan, daftar pemasok.
> - Latih orang kepercayaan selama beberapa bulan sebelum dijual.
>
> **3. Tips**
> Umumnya warung makan di Indonesia dijual 1–3 kali laba tahunan, tergantung lokasi dan pelanggan tetap. Sebaiknya konsultasi dengan notaris untuk akta jual belinya, dan konsultan pajak untuk pajak penjualan.
>
> Semoga lancar pensiunnya, Bu!

## SESUDAH (dengan skill)

> # Persiapan Jual Usaha "Dapur Bu Sri"
>
> **(1) Ringkasan situasi & asumsi**
> Warung makan, 9 tahun, Semarang, tempat sewa. Tujuan: **dijual/dioper ke pihak lain**, kerangka **12 bulan**. Mulai sekarang ada untungnya: warung yang rapi dan tidak bergantung pada Ibu lebih mudah dinilai tinggi, dan serah terima lebih tenang.
> Asumsi dari Ibu: kelipatan 2–3 kali laba (dari perantara), potongan karena bergantung pada Ibu 15%, penyusutan aset 30%, biaya notaris/perantara 5%.
>
> **(2) Daftar periksa kesiapan**
>
> | Area | Status | Langkah berikut |
> |---|---|---|
> | Pembukuan 2–3 tahun | Setengah (angka laba ada, "kira-kira") | Cocokkan dengan mutasi rekening/nota |
> | Pemisahan uang pribadi–usaha | Belum diketahui | Pisahkan rekening usaha |
> | SOP / resep | Belum (resep di kepala Ibu) | Tulis resep & takaran baku |
> | Ketergantungan pada pemilik | Belum | Apa yang berhenti bila Ibu tidak masuk 1 bulan? |
> | Aset | Setengah (nilai kasar Rp210 juta) | Daftar alat + kondisi + bukti milik (BPKB motor) |
> | Utang | Siap (KUR sisa Rp45 juta tercatat) | Tanya bank: dilunasi atau dialihkan |
> | Kontrak sewa | Belum diketahui | Sisa masa sewa & boleh dialihkan? |
> | Izin (NIB, dll.) | Belum diketahui | Cek atas nama siapa |
> | Pelanggan & pemasok kunci | Belum diketahui | Catat 5 pemasok utama, pelanggan langganan/katering |
> | Karyawan | Belum diketahui | Daftar karyawan, masa kerja, hak tertunda |
> | Merek, akun online, nomor WA | Belum diketahui | Pindahkan ke nama usaha |
>
> **Prioritas pembenahan:** 1) tulis resep & SOP dapur; 2) pastikan sewa tempat bisa dialihkan (tanpa tempat, nilai warung turun tajam); 3) rapikan pembukuan 3 tahun dengan bukti; 4) pisahkan uang pribadi–usaha; 5) putuskan nasib KUR.
>
> **(3) Perkiraan rentang nilai** (bahan diskusi, bukan harga pasti)
> Laba disesuaikan: laba + gaji Ibu Rp48 juta/tahun − gaji manajer pengganti Rp60 juta/tahun = laba − Rp12 juta.
>
> | Tahun | Laba | Setelah penyesuaian |
> |---|---|---|
> | 2023 | Rp96.000.000 | Rp84.000.000 |
> | 2024 | Rp118.000.000 | Rp106.000.000 |
> | 2025 | Rp134.000.000 | Rp122.000.000 |
>
> Rata-rata Rp104.000.000; tahun terakhir Rp122.000.000 (lebih tinggi), jadi dasar = **Rp104.000.000**.
>
> | Metode | Rumus | Hasil |
> |---|---|---|
> | Kelipatan laba | Rp104.000.000 × 2–3 × 85% | Rp176.800.000 – Rp265.200.000 |
> | Nilai aset bersih | Rp210.000.000 × 70% − Rp45.000.000 | Rp102.000.000 |
> | Rentang gabungan | terendah–tertinggi | Rp102.000.000 – Rp265.200.000 |
> | Setelah biaya 5% | × 95% | **Rp96.900.000 – Rp251.940.000** |
>
> Dibanding kebutuhan pensiun Rp8.000.000 × 24 = **Rp192.000.000**: selisih **−Rp95.100.000 s/d Rp59.940.000**. Artinya di harga rendah hasil bersih belum cukup; batas harga terendah yang Ibu terima perlu ditentukan sekarang.
> Catatan: kelipatan dan persentase adalah asumsi Ibu/perantara, bukan angka pasar. Pajak dan biaya lain belum dihitung. Laba Ibu "kira-kira"; pembeli akan minta bukti.
>
> **(4) Pilihan struktur** (tanyakan ke notaris/konsultan pajak): jual seluruh warung vs hanya alat + resep; bayar sekaligus vs bertahap; Ibu mendampingi 1–3 bulan setelah serah terima; KUR dilunasi dari hasil jual atau diambil alih pembeli.
>
> **(5) Rencana 12 bulan**
> | Bulan | Tugas |
> |---|---|
> | 1 | Isi daftar periksa; kumpulkan catatan 3 tahun; tetapkan harga terendah |
> | 2–3 | Pisahkan rekening; daftar aset & utang; cek sewa dan NIB |
> | 3–5 | Tulis resep & SOP; satu juru masak dilatih memegang dapur |
> | 4–6 | Bawa daftar pertanyaan ke notaris & konsultan pajak; hubungi perantara |
> | 6–9 | Kenalkan calon pembeli; bagi data setelah ada perjanjian kerahasiaan |
> | 9–12 | Serah terima, pendampingan, ganti nama izin/akun; umumkan ke karyawan & langganan |
> Rencana darurat: siapa memegang kunci, rekening, kontak pemasok bila Ibu mendadak sakit.
>
> **(6) Dokumen untuk calon pembeli:** rekap keuangan 3 tahun + mutasi rekening; daftar alat & kondisi; surat KUR; kontrak sewa; NIB; daftar karyawan; resep/SOP; daftar pemasok (tanpa kontak sebelum calon serius); akun online & nomor WA usaha; perjanjian kerahasiaan (disiapkan notaris).
>
> **(7) Pertanyaan untuk profesional**
> - Notaris: bagaimana mengalihkan sewa tempat dan NIB? Dokumen bukti peralihan alat & motor? Perjanjian kerahasiaan & pendampingan?
> - Konsultan pajak: kewajiban pajak atas penjualan warung/alat? Perlu rapikan laporan pajak tahun lalu? Pajak masuk perhitungan harga terendah?
> - Perantara: kelipatan apa yang lazim untuk warung makan di Semarang? Biaya jasa & lama proses?
>
> **(8) Penutup** — Ini bahan diskusi, bukan harga pasti; tidak ada yang bisa menjamin harga laku.
> Pertanyaan: 1) Sisa masa sewa tempat dan boleh dialihkan? 2) Apa yang berhenti bila Ibu tidak masuk 1 bulan? 3) Berapa harga terendah yang Ibu mau terima?

## Penilaian

| Kriteria | Tanpa skill | Dengan skill |
|---|---|---|
| Kebenaran angka | Aritmetika benar, **tetapi** laba tidak disesuaikan gaji pemilik/pengganti (lebih tinggi Rp12 juta/tahun), tidak membandingkan gabungan dengan aset bersih, angka dibulatkan ("sekitar Rp197 juta") | Semua angka dari hitungan, cocok verifikasi independen; penyesuaian gaji dipakai |
| Fakta karangan | "Umumnya warung makan dijual 1–3 kali laba" disebut sebagai fakta (tidak bersumber) | Kelipatan selalu disebut asumsi pengguna |
| Siap pakai | Daftar periksa generik, tanpa status, tanpa rencana per bulan, tanpa daftar dokumen | Daftar periksa berstatus, prioritas, rencana 12 bulan, dokumen, pertanyaan notaris/pajak |
| Perilaku | Tidak bertanya apa pun; menyebut "akta jual beli" ke notaris (wajar) | Kerja dulu, 3 pertanyaan di akhir |
| Bahasa awam | Baik | Baik, sedikit lebih panjang |
| **Skor** | **6,5** | **8,5** |

Pembeda terkuat: tanpa skill, laba tidak disesuaikan gaji manajer pengganti sehingga perkiraan Rp187–281 juta bersih; dengan skill Rp96,9–251,9 juta dan terlihat bahwa di harga rendah kebutuhan pensiun Rp192 juta **kurang Rp95,1 juta**.
