# Uji ulang ke-3 — Kantor 05 · Arus kas 13 minggu, info kurang lalu dilengkapi (arus-kas-13minggu 1.0.3)

Tanggal: 2026-10-01 (Asia/Jakarta) · Penguji independen ke-3 (bukan pembuat skill). OpenClaw asli lokal (`openclaw agent --local`), model router Komunitech (`ninerouter/komunitech`, jawaban `claude-sonnet-5`), sama dengan bot member. Home `sol3-kantor-manajemen` direset (`reset3-*.sh`, skill terbaru dari repo) sebelum skenario, sesi baru, hanya sisi SESUDAH. Pesan member (dan jawaban lanjutan) **sama persis** dengan uji pertama. Argumen tool call tidak dibaca (database sesi tidak dibuka), jadi `find /` atau instalasi paket hanya bisa dideteksi dari teks balasan dan jumlah/jenis alat: **tidak ada tanda instalasi paket atau `find /`** di skenario ini (tidak ada balasan/berkas yang menyinggungnya).

## Pesan member giliran 1 (sama persis)

> bikinin proyeksi arus kas 13 minggu dong. saya takut kas ga cukup buat gaji akhir bulan. saldo kas sekarang sekitar 380 juta

## Pesan member giliran 2 (sama persis)

> oke ini datanya. minggu pertama mulai senin 5 oktober.
> - pemasukan dari pelanggan rata2 210jt per minggu, tapi minggu 1 dan 2 cuma 150jt karena ada yg telat bayar
> - gaji 48 karyawan total 420jt, dibayar tiap tanggal 25
> - bayar supplier 130jt per minggu
> - sewa gudang 75jt tiap tanggal 5
> - cicilan bank 62jt tiap tanggal 15
> - ga ada THR atau bonus di periode ini
> - saldo minimal yg saya mau aman 100jt

## Balasan SESUDAH (ulang ke-3) — giliran 1 (utuh)

_alat: `read` · 1 panggilan, 0 gagal · durasi 11 dtk_

> Oke, saya siapkan proyeksi kas 13 minggunya. Saldo awal Rp 380.000.000 sudah saya catat. Supaya akurat, saya perlu beberapa angka lagi (jawab sebisanya, boleh perkiraan):
>
> 1. Perkiraan penjualan tunai/transfer masuk per minggu berapa?
> 2. Ada piutang pelanggan yang akan cair dalam 3 bulan ke depan? (nama, nominal, kira-kira kapan)
> 3. Pengeluaran rutin: belanja bahan/stok per minggu berapa? Gaji karyawan tanggal berapa & totalnya (ini yang kamu khawatirkan)? Sewa, cicilan, pajak/BPJS kalau ada — berapa & tanggal berapa?
> 4. Ada pengeluaran besar sekali-sekali dalam 3 bulan ke depan (THR, alat, renovasi, dll)?
> 5. Mau pakai batas aman saldo minimum tertentu, atau saya pakai default (rata-rata pengeluaran 1 minggu)?

## Balasan SESUDAH (ulang ke-3) — giliran 2 (utuh)

_alat: `exec, write, read` · 10 panggilan, 0 gagal · durasi 312 dtk_

> Sudah selesai dihitung. Ini hasilnya pakai script, bukan kira-kira:
>
> ## Proyeksi Kas 13 Minggu (5 Okt 2026 – 3 Jan 2027)
> Saldo awal Rp 380.000.000 · Batas aman Rp 100.000.000 (sesuai Anda)
>
> | Mg | Periode | Masuk | Keluar | Saldo akhir | Status |
> |---|---|---:|---:|---:|---|
> | 1 | 5–11 Okt | Rp 150.000.000 | Rp 205.000.000 | Rp 325.000.000 | 🟢 Aman |
> | 2 | 12–18 Okt | Rp 150.000.000 | Rp 192.000.000 | Rp 283.000.000 | 🟢 Aman |
> | 3 | 19–25 Okt | Rp 210.000.000 | Rp 550.000.000 | **-Rp 57.000.000** | 🔴 NEGATIF |
> | 4 | 26 Okt–1 Nov | Rp 210.000.000 | Rp 130.000.000 | Rp 23.000.000 | 🟡 Di bawah batas |
> | 5 | 2–8 Nov | Rp 210.000.000 | Rp 205.000.000 | Rp 28.000.000 | 🟡 Di bawah batas |
> | 6 | 9–15 Nov | Rp 210.000.000 | Rp 192.000.000 | Rp 46.000.000 | 🟡 Di bawah batas |
> | 7 | 16–22 Nov | Rp 210.000.000 | Rp 130.000.000 | Rp 126.000.000 | 🟢 Aman |
> | 8 | 23–29 Nov | Rp 210.000.000 | Rp 550.000.000 | **-Rp 214.000.000** | 🔴 NEGATIF |
> | 9 | 30 Nov–6 Des | Rp 210.000.000 | Rp 205.000.000 | -Rp 209.000.000 | 🔴 NEGATIF |
> | 10 | 7–13 Des | Rp 210.000.000 | Rp 130.000.000 | -Rp 129.000.000 | 🔴 NEGATIF |
> | 11 | 14–20 Des | Rp 210.000.000 | Rp 192.000.000 | -Rp 111.000.000 | 🔴 NEGATIF |
> | 12 | 21–27 Des | Rp 210.000.000 | Rp 550.000.000 | **-Rp 451.000.000** | 🔴 NEGATIF (terendah) |
> | 13 | 28 Des–3 Jan | Rp 210.000.000 | Rp 130.000.000 | -Rp 371.000.000 | 🔴 NEGATIF |
>
> ### Kesimpulan
> - **Titik paling kritis bukan di akhir bulan ini, tapi minggu 3 (19–25 Okt) — hanya 3 minggu dari sekarang.** Gaji Rp 420.000.000 dan bahan baku Rp 130.000.000 jatuh bersamaan di minggu itu (total keluar Rp 550.000.000), sementara masuk hanya Rp 210.000.000. Saldo tembus **-Rp 57.000.000**.
> - Pola ini berulang setiap bulan: minggu bergaji (3, 8, 12) selalu minus besar karena gaji+bahan baku bertabrakan.
> - Minggu negatif: 3, 8, 9, 10, 11, 12, 13 (7 dari 13 minggu). Di bawah batas aman: 4, 5, 6.
> - Tambahan dana agar tidak minus sepanjang periode: **Rp 451.000.000**. Agar selalu di atas batas aman Rp 100 juta: **Rp 551.000.000**.
> - **Arus kas 13 minggu: masuk Rp 2.610.000.000 vs keluar Rp 3.361.000.000 → turun Rp 751.000.000 (rata-rata -Rp 57.769.231/minggu). Ini defisit struktural** — bukan cuma soal jadwal, uang yang masuk memang lebih kecil dari yang keluar secara rutin.
> - Pos tambahan: sewa gudang Rp 75.000.000 jatuh 5 Jan 2027, 2 hari setelah minggu 13 — pastikan saldo saat itu cukup.
>
> ### Opsi tindakan (urut dampak)
> 1. **Tagih tuntas pelanggan yang telat bayar di minggu 1 & 2** (dari Rp 150 jt/minggu kembali ke Rp 210 jt penuh). Hasil simulasi: saldo terendah (minggu 12) naik dari -Rp 451.000.000 jadi -Rp 331.000.000 — membantu Rp 120.000.000, tapi belum cukup sendirian.
> 2. **Naikkan penjualan/harga rata-rata ~Rp 70.000.000/minggu** (dari Rp 210 jt jadi Rp 280 jt) mulai minggu 3 — ini wajib karena defisitnya struktural, bukan cuma geser jadwal. Hasil simulasi: semua minggu negatif hilang, saldo terendah jadi **+Rp 13.000.000** (minggu 3, masih sedikit di bawah batas aman).
> 3. **Gabungan opsi 2 + negosiasi termin bahan baku mundur 2 minggu ke supplier** ("Pak/Bu, bisa termin 14 hari untuk bulan ini?") → saldo terendah naik jadi **Rp 206.000.000** (minggu 8), **tidak ada lagi minggu negatif maupun di bawah batas aman** sepanjang 13 minggu. Ini kombinasi paling kuat dari data Anda.
> 4. Negosiasi termin bahan baku saja (tanpa naikkan penjualan) **hanya menunda, bukan solusi**: Rp 1.690.000.000 digeser, tapi Rp 260.000.000 tetap jatuh setelah minggu 13 dan saldo akhirnya tetap -Rp 371.000.000. Jangan dijadikan andalan.
> 5. **Pinjaman/suntikan modal** sebagai jalan terakhir jika opsi 1–3 belum cukup cepat dijalankan: kebutuhan Rp 551.000.000 agar selalu di atas batas aman. Proses pinjaman butuh waktu minggu — tidak akan cair sebelum minggu 3 (19 Okt), jadi tidak bisa jadi andalan untuk gajian bulan ini kecuali Anda sudah punya pinjaman standby.
>
> ### File Excel
> `proyeksi-kas-13-minggu.csv` — sudah tersimpan di folder kerja, siap dibuka di Excel/Google Sheets.
>
> **Asumsi:** Belum termasuk pajak/BPJS karena belum Anda sebutkan — jika ada, saldo riil bisa lebih rendah dari tabel di atas. Tidak ada THR/bonus di periode ini (sesuai info Anda). Semua nominal dibulatkan ke rupiah penuh.
>
> **Intinya:** kekhawatiran Anda soal gaji akhir bulan benar, tapi masalah sebenarnya sudah mulai di minggu 3 (19–25 Okt) dan berulang setiap bulan — bukan cuma akhir bulan ini. Paling realistis dikerjakan sekarang: percepat tagihan ke pelanggan yang telat (opsi 1) sambil mulai negosiasi termin supplier (bagian dari opsi 3) — dua hal ini bisa langsung Anda mulai minggu ini.

## Cacat lama — hilang?

Uji pertama: [05-arus-kas-13-minggu-info-kurang.md](05-arus-kas-13-minggu-info-kurang.md).

| Cacat dilaporkan | Hilang? | Bukti (kutipan) |
|---|---|---|
| Narasi "minggu 12 … dan cicilan Rp62 juta jatuh bersamaan" (cicilan di minggu 11) | **Ya** | *"minggu 3 (19–25 Okt) … Gaji Rp 420.000.000 dan bahan baku Rp 130.000.000 jatuh bersamaan … total keluar Rp 550.000.000"*; *"minggu bergaji (3, 8, 12) selalu minus besar karena gaji+bahan baku bertabrakan"*. Tidak ada lagi cicilan yang salah minggu. CSV hasil: cicilan di minggu 2, 6, 11 ✓. |
| BPJS/PPh 21 yang ditanyakan tetapi tidak dijawab tidak disebut | **Ya** | Giliran 1 menanyakan *"Sewa, cicilan, pajak/BPJS kalau ada"*; giliran 2: *"Asumsi: Belum termasuk pajak/BPJS karena belum Anda sebutkan — jika ada, saldo riil bisa lebih rendah"*. |
| `find /` | Tidak terdeteksi | Argumen alat tidak dibaca. |

## Verifikasi angka (Python penguji)

Python independen (minggu Senin–Minggu mulai 5 Okt): saldo akhir mg1–13 = 325, 283, −57, 23, 28, 46, 126, −214, −209, −129, −111, −451, −371 (juta) — **tabel benar semua** ✓. Masuk 2.610 jt, keluar 3.361 jt, turun 751 jt (−57.769.231/mg) ✓. Butuh 451 jt agar tak minus, 551 jt agar ≥ batas aman ✓. Minggu negatif 3, 8–13 (7) ✓; di bawah batas 4–6 ✓. Sewa 5 Jan 2027 = 2 hari setelah mg13 ✓. Simulasi: opsi 1 (mg1–2 jadi 210 jt) terendah −331 jt mg12 ✓; opsi 2 (+70 jt/mg mulai mg3) terendah +13 jt mg3 ✓; opsi 3 (opsi 2 + geser supplier) terendah 206 jt mg8 — cocok dengan `proyeksi_kas.py --geser-supplier 2` versi repo yang dijalankan penguji (script hanya menggeser pembayaran sampai minggu bermasalah terakhir) ✓; opsi 4 Rp260 jt jatuh setelah mg13, saldo setelah dibayar −371 jt ✓ (sesuai keluaran script).

## Regresi / temuan baru

- Tidak ada regresi berarti. Kecil: opsi 4 tidak menyebut saldo terendah selama periode (−191 jt mg12) yang dicetak script, langsung ke "−371 jt setelah dibayar"; tetap benar.
- Opsi 5 menyebut pinjaman "tidak akan cair sebelum minggu 3" — wajar sebagai kehati-hatian, bukan fakta yang dihitung.
- File `proyeksi-kas-13-minggu.csv` dibuat di workspace dan isinya cocok dengan tabel di chat.

## Nilai

| | Sesudah lama (uji pertama) | Sesudah baru (ulang ke-3) |
|---|---|---|
| Skor | 8.5 | **9** |

Kedua cacat hilang; semua angka dan simulasi cocok dengan hitungan penguji dan script; narasi minggu kritis kini dikutip dari rincian per minggu. **LULUS uji ulang ke-3.**
