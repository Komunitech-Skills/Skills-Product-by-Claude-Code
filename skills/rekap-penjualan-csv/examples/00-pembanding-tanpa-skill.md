# Pembanding A/B – Permintaan S1 dengan dan tanpa skill (uji ulang v1.1.0)

**Permintaan yang sama (S1):**
```
Halo, ini file export kasir kedai kopi aku 2 minggu pertama September (kasir-kopi-sept.csv). Tolong direkap ya, mau tau menu mana yang paling laku sama hari apa yang paling rame.
```
File: 127 baris, `Tanggal,Produk,Qty,Total`, total berformat `Rp 60.000` (lihat contoh 01).

## A. Tanpa skill (AI agent biasa, tanpa membaca skill apa pun)
Simulasi agent umum: membaca CSV dengan script Python singkat buatan sendiri (mengambil digit dari kolom Total), lalu menulis laporan.

> **Rekap Penjualan Kedai Kopi (1–14 September 2026)**
>
> Total penjualan: **Rp 5.084.000** dari 127 transaksi.
> Rata-rata penjualan per hari: Rp 363.143.
>
> **Penjualan per menu:**
> | Menu | Terjual | Pendapatan |
> |---|---|---|
> | Matcha Latte | 60 | Rp 1.320.000 |
> | Es Kopi Susu Gula Aren | 63 | Rp 1.134.000 |
> | Roti Bakar Coklat | 53 | Rp 848.000 |
> | Americano | 43 | Rp 645.000 |
> | Pisang Goreng | 36 | Rp 432.000 |
> | Kopi Tubruk | 38 | Rp 380.000 |
> | Teh Tarik | 25 | Rp 325.000 |
>
> **Menu paling laku:** Es Kopi Susu Gula Aren (63 cup), sedangkan pendapatan terbesar dari Matcha Latte.
>
> **Hari paling ramai:** 7 September 2026 (Rp 549.000). Hari paling sepi: 14 September 2026 (Rp 214.000).
>
> **Saran:**
> 1. Pertahankan kualitas menu andalan seperti Es Kopi Susu Gula Aren dan Matcha Latte.
> 2. Lakukan promosi di media sosial untuk meningkatkan penjualan di hari-hari sepi.
> 3. Pertimbangkan program loyalitas pelanggan, seperti kartu stamp.
> 4. Evaluasi menu yang kurang laku seperti Teh Tarik.

## B. Dengan skill `rekap-penjualan-csv`
Output lengkap ada di `01-kasir-kedai-kopi-2-minggu.md`. Ringkasnya: angka yang sama (dihitung script dan diverifikasi independen), format baku (total, baris, rata-rata kalender vs hari berjualan, top-5 dengan %, hari terbaik/terendah beserta nama hari), plus 3 insight berbasis angka: Matcha juara omzet walau qty lebih sedikit, dua minuman teratas = 48,3% omzet dengan saran paket spesifik, dan Senin 14/9 anjlok dibanding Senin 7/9 (Rp 214.000 vs Rp 549.000) disertai langkah cek penyebab.

## Penilaian singkat
| Aspek | Tanpa skill | Dengan skill |
|---|---|---|
| Angka (data rapi S1) | Sama benarnya. | Sama benarnya, dari script yang teruji. |
| Keandalan pada format lain | Parser "ambil digit saja" **gagal pada data berformat desimal Indonesia**. Pada file contoh 02 (`68.500,00`), cara ini menghasilkan **Rp 1.389.910.000**, padahal yang benar Rp 13.899.100 (100× lipat), tanpa peringatan. Tanggal, encoding ANSI, dan status batal juga tidak ditangani. | Format `Rp. 25000`, `15.000,-`, `68.500,00`, `;`, ANSI, tanggal teks, dan status batal ditangani, dan baris rusak dilaporkan. |
| Nama hari | Tanpa nama hari ("7 September"). | "Senin, 7 September", sehingga pola hari terlihat. |
| Rata-rata | Satu angka tanpa penjelasan dasar pembaginya. | Dibedakan per hari kalender vs hari berjualan. |
| Insight | Generik ("promosi di media sosial", "program loyalitas", "evaluasi Teh Tarik"). | Berbasis angka dan spesifik (paket 2 menu teratas, cek penyebab Senin anjlok). |
| Konsistensi format | Bergantung pada gaya agent saat itu. | Format tetap setiap kali, sehingga mudah dibandingkan antar-periode. |

**Kesimpulan: hasil dengan skill lebih baik.** Pada file S1 yang rapi, angkanya sama. Di sini nilai tambah skill terletak pada insight yang tajam, nama hari, dan definisi rata-rata yang jelas. Nilai tambah terbesarnya adalah **keandalan angka pada format Indonesia yang berantakan**: cara umum yang dipakai agent tanpa skill bisa salah 100× lipat tanpa peringatan (dibuktikan pada file contoh 02). Karena itu skill ini jelas memberi nilai tambah. Catatan: pada ekspor marketplace berstatus "Pengembalian", skill v1.1.0 masih punya celah (lihat contoh 06 dan HASIL-UJI).

---
**Uji ulang v1.2.0 (2026-09-23):** pembanding ini tetap berlaku. Pada file S1, output skill v1.2.0 identik dengan v1.1.0 (Rp 5.084.000, 127 baris). Nilai tambah skill pada data marketplace makin jelas di v1.2.0: bila agent tanpa skill tidak menyaring status (tidak ada instruksi untuk itu), omzet file contoh 06 terhitung Rp 10.793.000 (semua status) padahal seharusnya Rp 9.006.000 (+19,8%).
