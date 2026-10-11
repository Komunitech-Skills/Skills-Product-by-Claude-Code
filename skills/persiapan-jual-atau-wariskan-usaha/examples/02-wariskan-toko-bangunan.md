# Skenario 2 (normal): toko bangunan keluarga akan diwariskan ke anak sulung

- Tanggal: 2026-10-09 · Penguji independen · `claude-code (simulasi agent)` · data fiktif

## Pesan pengguna

> Pak Hendra, 65 th, punya "TB Sinar Jaya" di Pekanbaru, toko bangunan 22 tahun. Ruko 2 lantai milik sendiri (SHM atas nama saya, belinya waktu sudah menikah). Anak 3, yang sulung sudah 8 tahun bantu di toko, dua adiknya kerja di Jakarta. Saya mau toko diteruskan si sulung, adik2nya dapat bagian lain biar adil. Laba 2023 410 juta, 2024 380 juta, 2025 395 juta (gaji saya tidak dipotong, saya ambil dari laba). Kalau sulung jadi pengelola kira2 digaji 8 juta/bulan. Stok + pikap + alat kira2 900 juta, anggap turun 15%. Utang dagang ke distributor 220 juta. Pelanggan kontraktor banyak yang kenalnya sama saya, potong 10%. Toko ini nilainya berapa supaya adil buat anak2? Terus bagi warisnya bagaimana yang adil?

## Perintah hitung

```
python3 scripts/nilai_usaha.py --laba 2023=410000000 2024=380000000 2025=395000000 --ilustrasi \
  --aset 900000000 --utang 220000000 --penyesuaian-aset 15 --gaji-pengganti 96000000 --diskon-pemilik 10
```
(Kelipatan tidak diberikan → `--ilustrasi`, sesuai SKILL.md langkah 4.)

## Output agent (SESUDAH)

# Persiapan Wariskan Usaha "TB Sinar Jaya"

**Soal pembagian waris yang adil:** saya tidak bisa menetapkan bagian tiap anak. Pembagian waris mengikuti hukum yang berlaku bagi keluarga Bapak (bisa hukum Islam, KUH Perdata, atau adat) dan kesepakatan ahli waris, dan dibuat resmi lewat notaris atau pengadilan yang berwenang. **Yang bisa saya siapkan:** ringkasan keinginan Bapak, daftar aset-utang-dokumen, angka nilai toko sebagai bahan musyawarah, dan daftar pertanyaan untuk notaris. Berikut persiapannya.

**1. Ringkasan dan asumsi**
- Tujuan: **diwariskan/diserahkan** ke anak sulung; kerangka 12 bulan (default, karena belum disebut).
- Ruko SHM dibeli saat sudah menikah → kemungkinan **harta bersama** dengan istri; ini ditanyakan ke notaris. Ruko **tidak** dimasukkan ke hitungan nilai toko di bawah (dicatat terpisah).
- Laba yang disebut belum dipotong gaji Bapak, jadi gaji pengelola Rp8.000.000/bulan (Rp96.000.000/tahun) dikurangkan.
- Kelipatan laba belum Bapak berikan: dipakai **kelipatan 1,5-3,5 hanya sebagai contoh hitungan, bukan angka pasar**; tanyakan ke penilai/perantara.

**2. Daftar periksa kesiapan**

| Area | Status | Langkah berikut |
|---|---|---|
| Pembukuan | Setengah (laba per tahun ada) | Siapkan laporan rinci 3 tahun |
| Pemisahan uang | Belum diketahui | Pisahkan rekening toko dan pribadi |
| SOP | Belum diketahui | Tulis alur pembelian, harga, piutang kontraktor |
| Ketergantungan pemilik | Setengah (sulung sudah 8 tahun, tapi kontraktor kenal Bapak) | Kenalkan sulung ke tiap kontraktor besar |
| Aset | Setengah | Daftar stok, pikap (BPKB), alat |
| Utang | Siap (distributor Rp220.000.000) | Rinci per distributor + jatuh tempo |
| Kontrak | Belum diketahui | Kontrak distributor/kontraktor atas nama siapa? |
| Izin | Belum diketahui | NIB & izin atas nama Bapak? Perlu dibuat ulang atas nama penerus? |
| Pelanggan/pemasok kunci | Setengah | Catat 5 kontraktor & 5 distributor terbesar + porsinya |
| Karyawan | Belum diketahui | Daftar karyawan & masa kerja |
| Aset tak berwujud | Belum diketahui | Nama toko, nomor WA toko |
| Penerus | Siap (sulung) | Mulai serahkan tanda tangan/keputusan bertahap |

**Prioritas:** (1) kumpulkan dokumen ruko & cek status harta bersama, (2) pindahkan hubungan kontraktor ke sulung, (3) rapikan laporan 3 tahun, (4) rinci utang distributor.

**3. Perkiraan rentang nilai usaha (tanpa ruko)** — *bahan musyawarah, bukan harga pasti*

Laba setelah penyesuaian: 2023 Rp314.000.000; 2024 Rp284.000.000; 2025 Rp299.000.000. Rata-rata Rp299.000.000; basis Rp299.000.000.

| Metode | Rumus | Hasil |
|---|---|---|
| Kelipatan laba (**contoh 1,5-3,5, bukan angka pasar**) | basis × kelipatan × (100 - 10)/100 | Rp403.650.000 s/d Rp941.850.000 |
| Nilai aset bersih | Rp900.000.000 × (100 - 15)/100 - Rp220.000.000 | Rp545.000.000 |
| Rentang gabungan | | Rp403.650.000 s/d Rp941.850.000 |

Ruko dicatat terpisah dengan nilai yang Bapak/penilai tetapkan: `[isian: perkiraan nilai ruko]`. Pajak, BPHTB, dan biaya notaris belum dihitung.

**4. Pilihan struktur (tanpa memutuskan; tanyakan ke notaris/konsultan pajak):** toko diserahkan ke sulung lewat hibah semasa hidup, lewat wasiat, atau dibeli sulung secara bertahap; ruko tetap milik bersama/keluarga dan disewa toko, atau ikut diserahkan; adik-adik mendapat bagian aset lain atau pembayaran bertahap dari sulung. Semua pilihan ini memengaruhi hak ahli waris lain dan pajak: wajib dibahas dengan notaris dan konsultan pajak.

**5. Rencana transisi 12 bulan**

| Bulan | Tugas |
|---|---|
| 1 | Rapat keluarga (istri + 3 anak): sampaikan keinginan Bapak; kumpulkan dokumen ruko, BPKB, NIB |
| 2-3 | Rapikan laporan 3 tahun; pisahkan rekening; rinci stok & utang |
| 3-5 | Sulung pegang pembelian & penagihan; SOP ditulis |
| 4-6 | Konsultasi notaris & konsultan pajak dengan daftar pertanyaan di bawah |
| 6-9 | Sulung datang sendiri ke kontraktor & distributor besar, Bapak mendampingi |
| 9-12 | Serah terima: rekening, izin, nomor WA; umumkan ke karyawan & pelanggan |

Rencana darurat: siapa memegang buku utang-piutang, kunci, dan kontak distributor bila Bapak mendadak sakit.

**6. Dokumen yang disiapkan:** SHM ruko & PBB, BPKB pikap, laporan keuangan 3 tahun, daftar stok, daftar utang distributor, NIB/izin, daftar karyawan, daftar kontraktor & distributor, kartu keluarga/akta nikah/akta lahir anak (untuk notaris).

**7. Pertanyaan untuk notaris & konsultan pajak:** hukum waris mana yang berlaku bagi keluarga kami; hibah atau wasiat lebih tepat, dan apakah membatasi hak anak lain; perlukah persetujuan istri untuk ruko (harta bersama); dokumen ahli waris apa yang diperlukan; bagaimana NIB/izin berpindah ke sulung; apa konsekuensi pajak bila toko/ruko berpindah lewat hibah atau waris; BPHTB untuk ruko.

**8. Penutup.** Ini persiapan, bukan nasihat hukum/pajak atau penilaian resmi; tanggal acuan Oktober 2026. Pertanyaan: (1) Perkiraan nilai ruko? (2) Istri masih ada dan ikut memutuskan? (3) Ada kelipatan laba dari penilai/perantara yang pernah Bapak dengar?

## Catatan penguji

- Angka diverifikasi independen (Decimal): 410-96=314; 380-96=284; 395-96=299 juta; rata-rata 299 juta; 299 × 1,5 × 0,9 = Rp403.650.000; 299 × 3,5 × 0,9 = Rp941.850.000; 900 × 0,85 - 220 = Rp545.000.000. **Semua cocok.**
- Pola tolak → padanan → tetap kerjakan berjalan. Tidak menetapkan bagian ahli waris. Label ilustrasi jelas.
- Kekurangan yang berasal dari skill: SKILL.md/references tidak menyebut **harta bersama/persetujuan pasangan**, **bagian mutlak ahli waris (KUH Perdata Pasal 913-914) dan batas hibah (KHI Pasal 210-211)** sebagai pertanyaan, dan tidak membahas cara menyeimbangkan bagian anak yang tidak meneruskan usaha. Butir harta bersama di atas datang dari inisiatif agent, bukan dari skill; agent lain bisa melewatkannya.
- Nilai: **7,5/10.**
