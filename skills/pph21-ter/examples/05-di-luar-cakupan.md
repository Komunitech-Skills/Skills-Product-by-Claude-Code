# 05 — Di luar cakupan: PPh 21 pesangon

**Skenario:** S5 — permintaan di luar cakupan.

**Input pengguna (persis):**
> Karyawan saya kena PHK, dapat pesangon 150 juta. Pajaknya berapa? Pakai TER juga kan?

**Output:**

> Pesangon **tidak** dihitung dengan TER. Pesangon dikenai PPh 21 **final** dengan tarif berlapis khusus (diatur tersendiri dalam PP 68/2009), terpisah dari gaji bulanan — dan itu di luar cakupan skill ini, jadi saya tidak akan menebak angkanya.
>
> Yang bisa saya bantu dengan skill ini:
> - PPh 21 **gaji terakhir** karyawan tersebut (bulan dia berhenti dihitung ulang dengan tarif Pasal 17, termasuk kelebihan potong yang harus dikembalikan).
> - THR bila PHK terjadi ≤ 30 hari sebelum hari raya (pakai skill `hitung-thr`).
>
> Untuk pajak pesangon, silakan konfirmasi ke Kring Pajak 1500200 atau konsultan pajak; besaran pesangonnya sendiri sebaiknya dicek ke Disnaker (PP 35/2021).

**Catatan penguji:**
- Sesuai bagian "Kapan TIDAK digunakan" SKILL.md: pesangon diarahkan keluar, tidak dipaksakan ke TER.
- Agent tetap menawarkan bagian yang masih dalam cakupan (Masa Pajak Terakhir). Baik.
- Catatan ringan: SKILL.md tidak menyebut dasar aturan pesangon, sehingga agent bergantung pada pengetahuannya sendiri untuk kalimat pengarahan. Saran: tambahkan satu baris di "Kapan TIDAK digunakan" — "pesangon/uang pensiun sekaligus = PPh 21 final PP 68/2009, bukan TER".
