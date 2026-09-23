# Contoh 05 – Di luar cakupan: laporan laba rugi dan hitung pajak

## Skenario
S5, di luar cakupan. Pengguna meminta laporan laba rugi dan jumlah pajak yang harus disetor dari file penjualan. Skill hanya bisa menghitung omzet. Laba butuh data modal/biaya, dan pajak bergantung pada status wajib pajak serta aturan yang berlaku. Skill harus menolak bagian itu dan menawarkan yang bisa dikerjakan.

## Input pengguna
```
Ini file penjualan kedai aku. Tolong sekalian bikinin laporan laba rugi sama hitungin pajak yang harus aku setor ya, biar langsung aku laporin.
```

## Output

Aku bisa bantu sebagian, tapi ada yang di luar kemampuan skill ini:

**Yang belum bisa aku buat dari file ini:**
- **Laporan laba rugi.** File penjualan hanya berisi pemasukan (omzet). Untuk menghitung laba, perlu data pengeluaran: modal bahan (HPP), gaji, sewa, listrik, dan biaya lain. Tanpa data itu, angka laba pasti karangan. Untuk ini, gunakan skill **`laporan-keuangan-emkm`** bersama catatan kas/pengeluaranmu.
- **Jumlah pajak yang harus disetor.** Besarnya bergantung pada status usaha (perorangan/badan), total omzet setahun, dan aturan pajak yang berlaku saat ini. Gunakan skill **`pph-final-umkm`**, lalu pastikan ke kantor pajak (KPP) terdekat, konsultan pajak, atau kanal resmi Direktorat Jenderal Pajak sebelum melapor.

**Yang bisa aku buat sekarang:**
- **Rekap omzet** dari file ini: total omzet, omzet per hari, dan produk terlaris. Angka omzet ini biasanya jadi dasar perhitungan pajak UMKM dan bisa kamu bawa saat konsultasi.

Mau aku buatkan rekap omzetnya sekarang? Kalau kamu juga punya catatan pengeluaran, kirim saja. Aku bisa bantu merapikannya, tapi tetap sebagai catatan kasar, bukan laporan keuangan resmi.

## Catatan penguji
- Bagus: tidak memaksakan hitungan laba atau pajak, tidak menyebut tarif pajak yang berisiko keliru atau kedaluwarsa, dan menawarkan pekerjaan yang benar-benar bisa dikerjakan skill.
- [v1.0.0, sudah diperbaiki] Kurang (sedang): SKILL.md **tidak punya bagian "di luar cakupan"**. Tidak ada larangan eksplisit menghitung laba (tanpa HPP), pajak, proyeksi/prediksi penjualan, atau membaca .xlsx langsung. Perilaku di atas berasal dari penilaian umum agent. Agent yang kurang hati-hati bisa saja "menghitung pajak 0,5% dari omzet" tanpa memeriksa status dan ambang batas.
- **Uji ulang v1.1.0 (2026-09-23):** SKILL.md sekarang punya bagian **"Kapan TIDAK digunakan"** (laba rugi → `laporan-keuangan-emkm`, pajak → `pph-final-umkm`, prediksi → dijelaskan, .xlsx → simpan sebagai CSV). Output di atas diperbarui agar mengarahkan ke skill tersebut. Catatan "Kurang (sedang)" sebelumnya **sudah diperbaiki**. Sisa catatan ringan: pengarahan ke skill lain belum punya fallback bila skill itu tidak terpasang.
