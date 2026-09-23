# 03 — "bikinin dong" (usaha sablon kaos, kas diproyeksikan minus)

## Skenario
S3 — permintaan singkat/malas. Data wajib ada tapi seadanya, dan batas aman serta tanggal mulai tidak disebut, jadi dipakai default dengan asumsi disebutkan. Kasus ini menguji minggu NEGATIF, opsi yang mendorong kewajiban ke luar minggu 13, dan kejujuran simulasi. Tanggal hari ini: Rabu, 23 September 2026.

## Input pengguna
> bikinin dong proyeksi kas 13 minggu. kas 8jt, omzet seminggu 5jt, belanja stok kaos polos+tinta 3,5jt/minggu, gaji 2 org 5jt tiap tgl 1, sewa kios 2,5jt tiap tgl 10, iklan IG 1jt tiap 2 minggu, minggu ke 11 mau beli mesin press 7,5jt

## Langkah yang dijalankan agent
CSV (kolom `kritis` sengaja dikosongkan seperti agent yang malas mengisi, sehingga script menebak dari kata kunci):
```
minggu;jenis;kategori;nominal;keterangan;kritis
semua;masuk;Omzet penjualan;5.000.000;perkiraan per minggu;
semua;keluar;Belanja stok;3.500.000;;
tgl:1;keluar;Gaji 2 karyawan;5.000.000;;
tgl:10;keluar;Sewa kios;2.500.000;;
11;keluar;Mesin press kaos;7.500.000;;
setiap 2;keluar;Iklan Instagram;1.000.000;;
```
`python3 scripts/proyeksi_kas.py rencana-kas.csv --saldo-awal "8jt" --mulai 2026-09-28 --output-csv proyeksi-kas-13-minggu.csv`, lalu dijalankan ulang untuk opsi.

## Output

## Proyeksi Kas 13 Minggu (28 Sep – 27 Des 2026)
Saldo awal Rp 8.000.000 · Batas aman Rp 6.346.154 (asumsi: rata-rata pengeluaran 1 minggu)

| Mg | Periode | Masuk | Keluar | Saldo akhir | Status |
|---|---|---:|---:|---:|---|
| 1 | 28 Sep – 4 Okt | Rp 5.000.000 | Rp 9.500.000 | Rp 3.500.000 | 🟡 Di bawah batas |
| 2 | 5 – 11 Okt | Rp 5.000.000 | Rp 6.000.000 | Rp 2.500.000 | 🟡 Di bawah batas |
| 3 | 12 – 18 Okt | Rp 5.000.000 | Rp 4.500.000 | Rp 3.000.000 | 🟡 Di bawah batas |
| 4 | 19 – 25 Okt | Rp 5.000.000 | Rp 3.500.000 | Rp 4.500.000 | 🟡 Di bawah batas |
| 5 | 26 Okt – 1 Nov | Rp 5.000.000 | Rp 9.500.000 | Rp 0 | 🟡 Di bawah batas |
| 6 | 2 – 8 Nov | Rp 5.000.000 | Rp 3.500.000 | Rp 1.500.000 | 🟡 Di bawah batas |
| 7 | 9 – 15 Nov | Rp 5.000.000 | Rp 7.000.000 | -Rp 500.000 | 🔴 NEGATIF |
| 8 | 16 – 22 Nov | Rp 5.000.000 | Rp 3.500.000 | Rp 1.000.000 | 🟡 Di bawah batas |
| 9 | 23 – 29 Nov | Rp 5.000.000 | Rp 4.500.000 | Rp 1.500.000 | 🟡 Di bawah batas |
| 10 | 30 Nov – 6 Des | Rp 5.000.000 | Rp 8.500.000 | -Rp 2.000.000 | 🔴 NEGATIF |
| 11 | 7 – 13 Des | Rp 5.000.000 | Rp 14.500.000 | -Rp 11.500.000 | 🔴 NEGATIF |
| 12 | 14 – 20 Des | Rp 5.000.000 | Rp 3.500.000 | -Rp 10.000.000 | 🔴 NEGATIF |
| 13 | 21 – 27 Des | Rp 5.000.000 | Rp 4.500.000 | -Rp 9.500.000 | 🔴 NEGATIF |

### Kesimpulan
- **Titik paling kritis: minggu 11 (7–13 Des), saldo −Rp 11.500.000.** Penyebabnya mesin press Rp 7.500.000 dibeli saat kas sudah minus (setelah gajian 1 Des), bersamaan dengan sewa kios 10 Des, belanja stok, dan iklan.
- **Kas pertama kali minus di minggu 7 (9–15 Nov), −Rp 500.000**, karena sewa kios jatuh di minggu itu. Minggu 5 (gajian 1 Nov) kas tepat habis, Rp 0.
- Minggu negatif: 7, 10, 11, 12, 13 · Di bawah batas aman: 1, 2, 3, 4, 5, 6, 8, 9. **Tidak ada satu minggu pun yang aman.**
- Tambahan dana agar tidak minus: **Rp 11.500.000** (agar di atas batas aman: Rp 17.846.154).
- ⚠️ **Masalahnya bukan jadwal, tapi selisih rutin.** Dalam 13 minggu, uang masuk Rp 65.000.000 dan uang keluar Rp 82.500.000. Tanpa mesin pun kas tetap turun rata-rata sekitar Rp 770.000 per minggu. Menggeser jadwal bayar hanya memindahkan masalah.

### Opsi tindakan (urut dari dampak terbesar)
1. **Tunda mesin press Rp 7.500.000 sampai omzet naik, lalu naikkan omzet ke ±Rp 6.000.000/minggu (+20%)**, misalnya lewat pesanan kaos komunitas/kantor dengan DP. Hasil hitung ulang: **tidak ada minggu minus**, saldo terendah Rp 4.500.000 (minggu 1), saldo akhir minggu 13 Rp 11.000.000. Di bawah batas masih minggu 1, 2, 3, 5.
2. **Tunda mesin press dan potong iklan IG jadi Rp 500.000 per 2 minggu.** Hasil hitung ulang: saldo terendah −Rp 1.000.000 (minggu 11), tinggal 1 minggu minus. Kalau hanya mesin yang ditunda, saldo terendah masih −Rp 4.000.000 (minggu 11) dengan 5 minggu minus. **Menunda mesin saja tidak cukup.**
3. **Naikkan omzet ke Rp 6.000.000/minggu tapi tetap beli mesin di minggu 11.** Hasil hitung ulang: saldo terendah −Rp 500.000 (minggu 11), minus 1 minggu. Artinya mesin baru masuk akal kalau omzet naik lebih dari 20%.
4. **Minta termin 2 minggu ke supplier kaos polos/tinta.** Simulasi script: saldo terendah −Rp 4.500.000 (minggu 11), minggu minus 11–13. **PERHATIAN:** Rp 7.000.000 tagihan stok pindah ke setelah minggu 13. Utangnya tetap ada.
5. **Tambahan modal pemilik Rp 11.500.000** (pilihan terakhir). Ini hanya menutup minus. Kalau ingin selalu di atas batas aman, butuh Rp 17.846.154. Pinjaman bank/KUR butuh waktu proses beberapa minggu, jadi tidak cocok untuk minus di minggu 7. Simulasi cicilan bisa dibuat dengan skill `pengajuan-kur`. **Jangan pakai pinjol ilegal.**

**Yang tidak saya sarankan:** hasil simulasi otomatis "gabungan" (termin supplier + tunda mesin dan iklan) terlihat bagus, dengan saldo terendah Rp 5.000.000 dan tanpa minggu minus. Namun Rp 16.500.000 kewajiban hanya didorong ke setelah minggu 13. Setelah dibayar, saldo akhir Rp 7.000.000 menjadi sekitar **−Rp 9.500.000**, sama dengan tanpa tindakan.

### File Excel
`proyeksi-kas-13-minggu.csv` (pemisah `;`).

Asumsi: minggu 1 mulai Senin 28 Sep 2026 (Senin terdekat) · omzet rata Rp 5.000.000/minggu · iklan dibayar minggu 1, 3, 5, …, 13 · batas aman = rata-rata pengeluaran 1 minggu (Rp 6.346.154) · Pembulatan rupiah penuh.
Catatan dari script: pos "Belanja stok" belum jelas kritis/tidak (saya anggap wajib dibayar). Tidak ada piutang pelanggan yang tercatat. Kalau ada pelanggan yang masih berutang, kabari saya karena itu opsi tercepat.
Proyeksi berdasarkan perkiraan Anda, jadi perbarui tiap minggu. Bukan nasihat keuangan profesional.

## Catatan penguji
- **Diverifikasi independen**: tabel dasar dan 5 varian opsi cocok 13/13 minggu dengan hitungan terpisah. `setiap 2` → minggu 1, 3, 5, …, 13 benar. Rata-rata turun per minggu tanpa mesin = (8.000.000 − (−2.000.000))/13 ≈ Rp 769.231.
- **Temuan penting (sedang):** simulasi "Gabungan semua opsi" script melaporkan "minggu negatif: tidak ada, saldo terendah Rp 5.000.000". Script memang memberi PERHATIAN Rp 16.500.000 jatuh setelah minggu 13, tetapi **tidak menghitung saldo setelah kewajiban itu dibayar** (−Rp 9.500.000). Pembeli awam atau agent yang hanya menyalin angka bisa mengira masalahnya selesai. Saran: tambahkan `saldo_setelah_kewajiban_tertunda = saldo_akhir_minggu_n − jatuh_setelah_horizon` dan tandai opsi "hanya menunda" bila nilainya < 0 atau < batas.
- Kurang (sedang): SKILL.md tidak meminta agent menyebut masalah struktural (`arus_kas_bersih` negatif). Agent di sini menyimpulkannya sendiri.
- Bagus: aturan anti-pinjol, pinjaman sebagai pilihan terakhir, dan contoh kalimat semuanya sesuai `references/opsi-tindakan.md`.
