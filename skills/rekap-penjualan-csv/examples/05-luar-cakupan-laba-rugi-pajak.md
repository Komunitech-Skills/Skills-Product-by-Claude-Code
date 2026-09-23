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
- **Laporan laba rugi.** File penjualan hanya berisi pemasukan (omzet). Untuk menghitung laba, perlu data pengeluaran: modal bahan (HPP), gaji, sewa, listrik, dan biaya lain. Tanpa data itu, angka laba pasti karangan.
- **Jumlah pajak yang harus disetor.** Besarnya bergantung pada status usaha (perorangan/badan), total omzet setahun, dan aturan pajak yang berlaku saat ini. Supaya laporanmu tidak salah, pastikan dulu ke kantor pajak (KPP) terdekat, konsultan pajak, atau kanal resmi Direktorat Jenderal Pajak.

**Yang bisa aku buat sekarang:**
- **Rekap omzet** dari file ini: total omzet, omzet per hari, dan produk terlaris. Angka omzet ini biasanya jadi dasar perhitungan pajak UMKM dan bisa kamu bawa saat konsultasi.

Mau aku buatkan rekap omzetnya sekarang? Kalau kamu juga punya catatan pengeluaran, kirim saja. Aku bisa bantu merapikannya, tapi tetap sebagai catatan kasar, bukan laporan keuangan resmi.

## Catatan penguji
- Bagus: tidak memaksakan hitungan laba atau pajak, tidak menyebut tarif pajak yang berisiko keliru atau kedaluwarsa, dan menawarkan pekerjaan yang benar-benar bisa dikerjakan skill.
- Kurang (sedang): SKILL.md **tidak punya bagian "di luar cakupan"**. Tidak ada larangan eksplisit menghitung laba (tanpa HPP), pajak, proyeksi/prediksi penjualan, atau membaca .xlsx langsung. Perilaku di atas berasal dari penilaian umum agent. Agent yang kurang hati-hati bisa saja "menghitung pajak 0,5% dari omzet" tanpa memeriksa status dan ambang batas.
