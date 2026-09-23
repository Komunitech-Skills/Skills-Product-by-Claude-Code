# 05 — Di luar cakupan: laporan laba rugi bulanan

**Skenario:** S5 — di luar cakupan (tugas milik skill `laporan-keuangan-emkm`).

**Input pengguna (persis):**
> Tolong buatin laporan laba rugi usaha kue saya bulan Agustus, penjualan 18 juta, belanja bahan 7 juta, gaji karyawan 3 juta, sewa 1,5 juta

## Output

Laporan laba rugi adalah tugas skill **`laporan-keuangan-emkm`** — skill ini (hitung-hpp) khusus menghitung **modal per produk (HPP)**, harga jual, dan titik impas.

- Kalau skill `laporan-keuangan-emkm` sudah terpasang, cukup kirim ulang permintaan yang sama; data Anda (penjualan Rp18 juta, bahan Rp7 juta, gaji Rp3 juta, sewa Rp1,5 juta) sudah cukup untuk memulai.
- Kalau belum punya skill itu, saya tetap bisa membantu menyusun ringkasan sederhana secara umum, tetapi tanpa format laporan EMKM.

Yang bisa saya bantu di sini: menghitung **HPP per kue** dari resep Anda supaya tahu produk mana yang paling untung, atau mengecek apakah harga jual sekarang sudah menutup semua biaya.

## Catatan penguji
- Diarahkan dengan benar ke `laporan-keuangan-emkm` sesuai "Kapan TIDAK digunakan".
- Agent tidak memaksakan script HPP untuk laporan periode. Bagus.
- SKILL.md tidak memberi kalimat cadangan bila skill rujukan tidak dimiliki; agent menyusunnya sendiri.
