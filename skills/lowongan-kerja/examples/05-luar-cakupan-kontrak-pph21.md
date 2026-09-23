# Contoh 05 – Di luar cakupan: kontrak PKWT dan hitung PPh 21

## Skenario
S5, di luar cakupan. Pengguna sudah menemukan karyawan dan meminta kontrak kerja PKWT serta perhitungan PPh 21. Keduanya tercantum di "Kapan TIDAK digunakan" SKILL.md. Skill harus mengarahkan, bukan memaksakan.

## Input pengguna
```
Admin yang kemarin udah aku terima nih. Tolong buatin kontrak kerja PKWT 1 tahun buat dia, sekalian hitungin PPh 21 dari gaji 5 juta per bulan ya.
```

## Output

Selamat, admin barunya sudah dapat! 🎉 Dua permintaan ini di luar tugas skill lowongan kerja, jadi aku arahkan dulu supaya hasilnya aman:

**1. Kontrak kerja PKWT 1 tahun**
Ini sebaiknya dibuat dengan skill **`perjanjian-sederhana`**, yang khusus menyusun perjanjian. Kontrak PKWT juga punya aturan yang perlu dipatuhi, misalnya jenis pekerjaan yang boleh dikontrak, batas jangka waktu, dan kompensasi saat kontrak berakhir. Aturan ketenagakerjaan juga sedang dalam proses perubahan (RUU Pelindungan Ketenagakerjaan). Karena itu, setelah drafnya jadi, **minta ahli hukum ketenagakerjaan atau Disnaker setempat mengeceknya** sebelum ditandatangani.

**2. Menghitung PPh 21**
Ini di luar cakupan skill ini. PPh 21 bergantung pada status PTKP (menikah/tanggungan), komponen gaji, dan aturan tarif yang berlaku. Supaya tidak salah potong, gunakan **kalkulator PPh 21 resmi dari DJP** atau konsultasikan ke konsultan pajak/akuntan.

**Yang masih bisa aku bantu dari skill ini:**
- Membuat loker untuk posisi lain yang masih kosong.
- Membuat pertanyaan screening atau tes kecil untuk rekrutmen berikutnya.

Mau lanjut ke salah satunya?

## Catatan penguji
- **Bagus:** sesuai "Kapan TIDAK digunakan": kontrak diarahkan ke `perjanjian-sederhana` dengan saran cek ahli hukum, dan PPh 21 disebut di luar cakupan dengan saran kalkulator resmi/konsultan. Tidak ada angka pajak yang dikarang.
- **Bagus:** nada ramah dan tetap menawarkan bantuan yang relevan.
- **Catatan:** saran "kalkulator PPh 21 resmi dari DJP" tidak disertai tautan, dan memang sebaiknya tidak ditebak. SKILL.md hanya menulis "kalkulator resmi atau konsultan". Cukup.
- **Catatan:** pengarahan ke skill lain (`perjanjian-sederhana`) hanya berguna bila pembeli juga memiliki skill itu. Saran ringan untuk SKILL.md: tambahkan kalimat "jika skill tersebut tidak terpasang, sarankan pengguna berkonsultasi ke ahli hukum" agar agent tidak menjanjikan skill yang tidak ada.
