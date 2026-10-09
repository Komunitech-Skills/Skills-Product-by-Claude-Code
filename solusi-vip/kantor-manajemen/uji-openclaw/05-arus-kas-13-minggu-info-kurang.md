# Uji OpenClaw 05 — Proyeksi arus kas 13 minggu — INFO KURANG (hanya saldo awal), lalu dilengkapi

Tanggal: 2026-10-01 · Agent: OpenClaw lokal (`openclaw agent --local`), model router Komunitech (`ninerouter/komunitech`, sama dengan bot member), sesi baru per sisi, kedua home direset sebelum skenario. SEBELUM = home `kosong-kantor-manajemen` (tanpa skill), SESUDAH = home `sol-kantor-manajemen` (17 skill paket kantor-manajemen). Semua data fiktif.

## Pesan member (identik di kedua sisi)

> bikinin proyeksi arus kas 13 minggu dong. saya takut kas ga cukup buat gaji akhir bulan. saldo kas sekarang sekitar 380 juta

Jawaban lanjutan member (sesi yang sama, identik di kedua sisi):

> oke ini datanya. minggu pertama mulai senin 5 oktober.
> - pemasukan dari pelanggan rata2 210jt per minggu, tapi minggu 1 dan 2 cuma 150jt karena ada yg telat bayar
> - gaji 48 karyawan total 420jt, dibayar tiap tanggal 25
> - bayar supplier 130jt per minggu
> - sewa gudang 75jt tiap tanggal 5
> - cicilan bank 62jt tiap tanggal 15
> - ga ada THR atau bonus di periode ini
> - saldo minimal yg saya mau aman 100jt

## SEBELUM (tanpa skill) — balasan utuh

> Oke, saldo awal 380 juta. Biar proyeksi 13 minggunya akurat (bukan karangan), saya butuh beberapa angka dulu:
>
> 1. **Pemasukan** — rata-rata kas masuk per minggu (omzet/penjualan tunai + piutang yang cair), atau kalau fluktuatif, kasih kisaran per bulan nanti saya bagi per minggu.
> 2. **Gaji** — total gaji karyawan per bulan + tanggal pastinya (misal tgl 25 atau akhir bulan tanggal berapa).
> 3. **Biaya rutin lain** — sewa, bahan baku/stok, listrik, cicilan, dll — per minggu atau per bulan.
> 4. **Ada tagihan besar** dalam 13 minggu ke depan? (pajak, cicilan utang, bayar supplier besar, dll)
> 5. **Ada piutang besar** yang diharapkan cair di periode ini?
>
> Kalau belum ada catatan detail, kasih estimasi kasar aja dari ingatan — nanti saya susun tabel mingguannya dan tandain minggu mana yang berisiko kas minus sebelum gajian.

### SEBELUM — giliran 2

> Sudah saya hitung berdasarkan data itu. Kabar buruknya: **kas memang akan jebol sebelum gajian pertama (25 Oktober)**, dan masalahnya terus berulang di dua gajian berikutnya.
>
> ## Proyeksi Arus Kas 13 Minggu (saldo awal: Rp380jt)
>
> | # | Periode | Masuk | Keluar | Rincian Keluar | Net | Saldo Akhir |
> |---|---------|------:|-------:|----------------|----:|-------------:|
> | 1 | 5–11 Okt | 150 | 205 | Supplier 130 + Sewa 75 | -55 | 325 |
> | 2 | 12–18 Okt | 150 | 192 | Supplier 130 + Cicilan 62 | -42 | 283 |
> | 3 | 19–25 Okt | 210 | 550 | Supplier 130 + **Gaji 420** | -340 | **-57** ⚠️ |
> | 4 | 26 Okt–1 Nov | 210 | 130 | Supplier 130 | +80 | 23 |
> | 5 | 2–8 Nov | 210 | 205 | Supplier 130 + Sewa 75 | +5 | 28 |
> | 6 | 9–15 Nov | 210 | 192 | Supplier 130 + Cicilan 62 | +18 | 46 |
> | 7 | 16–22 Nov | 210 | 130 | Supplier 130 | +80 | 126 |
> | 8 | 23–29 Nov | 210 | 550 | Supplier 130 + **Gaji 420** | -340 | **-214** ⚠️ |
> | 9 | 30 Nov–6 Des | 210 | 205 | Supplier 130 + Sewa 75 | +5 | -209 |
> | 10 | 7–13 Des | 210 | 130 | Supplier 130 | +80 | -129 |
> | 11 | 14–20 Des | 210 | 192 | Supplier 130 + Cicilan 62 | +18 | -111 |
> | 12 | 21–27 Des | 210 | 550 | Supplier 130 + **Gaji 420** | -340 | **-451** ⚠️ |
> | 13 | 28 Des–3 Jan | 210 | 130 | Supplier 130 | +80 | -371 |
>
> *(angka dalam juta rupiah)*
>
> ## Kesimpulan — ini serius
>
> Kekhawatiran Anda benar, bahkan lebih parah dari sekadar "ga cukup":
>
> 1. **Gajian pertama (25 Okt) sudah tidak tertutup.** Saldo tembus **-57jt** — defisit ~157jt dari target minimum 100jt. Ini cuma 3 minggu dari sekarang.
> 2. Sempat pulih ke +126jt di minggu 7 (karena belum ada potongan besar), tapi **gajian 25 Nov langsung menjebloskan ke -214jt**.
> 3. Setelah itu saldo **tidak pernah positif lagi** sampai akhir periode, dan makin dalam di gajian 25 Des (-451jt), berakhir di **-371jt** di minggu ke-13.
> 4. Akar masalah struktural: pemasukan mingguan (~210jt) hanya cukup nutup supplier (130jt) + sisa kecil untuk sewa/cicilan. Begitu ada gaji (420jt) nongol dalam minggu yang sama, defisitnya 340jt — dan ini terjadi **3 kali** dalam 13 minggu.
>
> ## Berapa yang dibutuhkan
>
> Supaya saldo **tidak pernah di bawah 100jt** sepanjang 13 minggu, titik terlemah ada di minggu 12 (-451jt). Anda butuh tambahan dana sekitar **Rp551 juta** masuk sejak awal periode (baik dari percepatan penagihan, suntikan modal, atau pinjaman modal kerja) — dan itu **harus sudah tersedia sebelum 25 Oktober**, karena krisis pertama muncul di minggu 3, bukan di minggu 12.
>
> ## Yang bisa dilakukan sekarang
>
> - **Tagih piutang yang telat** (minggu 1–2) lebih agresif — ini langsung menambah kas sebelum gajian pertama.
> - **Nego termin bayar supplier** — geser dari mingguan ke 2-mingguan, atau mundur beberapa hari supaya tidak bentrok dengan tanggal gajian.
> - **Siapkan fasilitas kredit modal kerja (working capital)** minimal ~550–600jt sebagai jaring pengaman, bukan untuk dipakai semua, tapi supaya tidak gagal bayar gaji.
> - **Cek apakah cicilan bank bisa direstruktur** atau sewa gudang bisa dinego jadi bulanan di tanggal lain yang tidak numpuk dengan gaji.
> - Kalau ada pelanggan besar dengan piutang jatuh tempo di sekitar tgl 20-25 tiap bulan, prioritaskan penagihan tepat sebelum gajian.
>
> Mau saya buatkan juga versi spreadsheet (CSV/Excel) biar bisa diotak-atik sendiri, atau dicoba skenario kalau supplier dinego jadi 2-mingguan?

## SESUDAH (paket skill kantor-manajemen) — balasan utuh

> Oke, siap bantu bikin proyeksi kas 13 minggunya. Saldo awal Rp 380 juta sudah dicatat. Supaya akurat, tolong jawab beberapa hal ini ya:
>
> 1. **Penjualan tunai/transfer langsung** — kira-kira berapa per minggu?
> 2. **Piutang pelanggan** yang akan masuk (kalau ada) — siapa, berapa, perkiraan kapan?
> 3. **Pengeluaran rutin**:
>    - Belanja bahan/supplier per minggu — berapa?
>    - **Gaji** — tanggal berapa dan totalnya berapa? (ini yang paling bikin khawatir ya)
>    - Sewa — berapa & tanggal berapa?
>    - Cicilan/angsuran (kalau ada) — berapa & tanggal berapa?
>    - Pajak/BPJS/operasional lain — berapa & kapan?
> 4. **Pengeluaran besar sekali saja** dalam 3 bulan ke depan (THR, renovasi, beli alat)? Kalau tidak ada, bilang saja tidak ada.
> 5. **Batas aman** yang Anda mau (saldo minimum biar tenang)? Kalau belum ada angka, saya pakai asumsi rata-rata pengeluaran 1 minggu.
>
> Boleh jawab singkat/list saja, tidak perlu format khusus.

### SESUDAH — giliran 2

> ## Proyeksi Kas 13 Minggu (5 Okt 2026 – 3 Jan 2027)
> Saldo awal **Rp 380.000.000** · Batas aman **Rp 100.000.000** (sesuai permintaan Anda)
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
> - **Titik paling kritis: minggu 12** (21–27 Des), saldo tembus **-Rp 451.000.000** — minggu itu gaji Rp 420 juta, bahan Rp 130 juta, dan cicilan Rp 62 juta jatuh bersamaan (total keluar Rp 550 juta vs masuk Rp 210 juta).
> - **Minggu 3** (19–25 Okt) sudah negatif duluan karena gaji 25 Okt jatuh bareng bahan baku, sementara minggu 1–2 pemasukan masih turun (Rp 150 juta).
> - Minggu negatif: **3, 8, 9, 10, 11, 12, 13** (7 dari 13 minggu). Di bawah batas aman: 4, 5, 6.
> - Tambahan dana agar tidak minus: **Rp 451.000.000** (agar di atas batas aman Rp 100 juta: **Rp 551.000.000**).
> - Arus kas 13 minggu: masuk **Rp 2.610.000.000** vs keluar **Rp 3.361.000.000** → **turun Rp 751.000.000** (rata-rata **-Rp 57.769.231/minggu**). **Ini bukan sekadar soal jadwal — pengeluaran rutin Anda memang lebih besar dari pemasukan rutin (defisit struktural).** Geser-geser tanggal saja tidak akan menyelesaikan masalah.
> - Catatan tambahan: sewa gudang Rp 75 juta berikutnya jatuh 5 Jan 2027, 2 hari setelah minggu 13 — siapkan itu juga.
>
> ### Mengapa gaji akhir bulan jadi masalah
> Gaji Rp 420 juta setiap tanggal 25 selalu jatuh di minggu yang juga ada bahan baku Rp 130 juta → total keluar Rp 550 juta sekali dalam ~4 minggu, sementara pemasukan rutin cuma ~Rp 210 juta/minggu. Minggu-minggu "gajian" (3, 8, 12) adalah yang paling berbahaya.
>
> ### Opsi tindakan (urut dampak)
>
> **1. Naikkan pemasukan ±Rp 60 juta/minggu** (harga, volume penjualan, atau pelanggan baru) — paling efektif karena ini masalah struktural.
>    → Simulasi: saldo terendah naik dari **-Rp 451.000.000 menjadi +Rp 123.000.000** (minggu 3), dan **semua 13 minggu jadi AMAN** (saldo akhir Rp 409.000.000).
>    Cara: evaluasi harga jual, dorong repeat order, atau buka 1 kanal penjualan tambahan.
>
> **2. Pangkas belanja bahan baku dari Rp 130 juta → Rp 70 juta/minggu** (hemat Rp 60 juta/minggu) — alternatif kalau menaikkan penjualan sulit.
>    → Simulasi: hasil sama — saldo terendah **+Rp 123.000.000**, **semua minggu AMAN**.
>    ⚠️ Pastikan stok tetap cukup; cek dengan supplier apakah ada diskon volume yang hilang kalau order dikurangi.
>
>    *Realistisnya kombinasi keduanya lebih aman buat dicoba dulu — misalnya tambah penjualan Rp 30 juta/minggu + hemat bahan Rp 30 juta/minggu, baru kejar lebih besar kalau belum cukup.*
>
> **3. Negosiasi termin bayar supplier mundur 2 minggu** — bisa membantu jangka pendek, **tapi INI HANYA MENUNDA, bukan solusi**: setelah termin digeser, saldo terendah membaik jadi -Rp 191.000.000 (minggu 12), namun ada **Rp 260.000.000** utang bahan yang jatuh *setelah* minggu 13 — begitu dibayar, saldo tetap minus Rp 371.000.000. Jangan andalkan ini sendirian.
>
> **4. Suntikan modal / pinjaman sebagai jalan terakhir**: jumlah minimal **Rp 551.000.000** agar saldo tetap di atas batas aman sepanjang 13 minggu. Proses pinjaman butuh waktu, jadi kurang cocok untuk menutup minggu 3 yang sudah dekat (19 Okt) — kalau mau jalur ini, segera ajukan. Saya bisa bantu simulasi cicilan KUR kalau diperlukan.
>
> ### File Excel
> `proyeksi-kas-13-minggu.csv` — buka di Excel/Google Sheets. Juga tersimpan simulasi opsi 1 (`proyeksi-opsi-tambah-penjualan.csv`) dan opsi 2 (`proyeksi-opsi-pangkas-bahan.csv`) untuk perbandingan langsung.
>
> **Asumsi:** tidak ada pos piutang pelanggan yang saya masukkan (Anda sebut pemasukan sudah rata-rata dari pelanggan); batas aman Rp 100 juta sesuai permintaan Anda; pembulatan ke rupiah penuh.
> **Catatan:** ini proyeksi dari perkiraan Anda — perbarui tiap minggu dengan angka aktual biar makin akurat. Gaji, cicilan bank, dan sewa selalu diperlakukan sebagai kewajiban kritis yang **tidak** disarankan untuk ditunda.
>
> Mau saya coba skenario gabungan (tambah penjualan sedikit + pangkas bahan sedikit) biar lebih realistis, atau langsung bantu susun pesan negosiasi ke supplier?

## Verifikasi & pemakaian skill

- **Giliran 1 (info kurang):** kedua sisi bertanya **sekali** dalam satu daftar singkat, tidak mengarang angka. SESUDAH (setelah membaca `arus-kas-13minggu/SKILL.md`) juga menanyakan batas aman saldo dan pajak/BPJS — lebih lengkap. Setara, SESUDAH sedikit lebih baik.
- **Pemakaian skill (giliran 2):** SESUDAH menulis `rencana-kas.csv` dari template, menjalankan `scripts/proyeksi_kas.py --saldo-awal … --mulai 2026-10-05 --batas-aman …`, lalu 2–3 simulasi opsi (tambah penjualan, pangkas bahan, mundurkan termin supplier) dan menyimpan CSV. SEBELUM tanpa tool.
- **Angka (dihitung ulang penguji, Python, minggu Senin–Minggu mulai 5 Okt):** saldo akhir mg1–13 = 325, 283, −57, 23, 28, 46, 126, −214, −209, −129, −111, −451, −371 (juta). **Tabel kedua sisi benar semua.** Total masuk 2.610 jt, keluar 3.361 jt, turun 751 jt ✓ (SESUDAH). Dana agar ≥ batas aman 551 jt ✓ (kedua sisi). Simulasi opsi 1 (+60 jt/minggu): saldo terendah +123 jt di mg3, akhir 409 jt ✓.
- **Kesalahan SESUDAH:** "minggu 12 … gaji Rp 420 juta, bahan Rp 130 juta, **dan cicilan Rp 62 juta** jatuh bersamaan" — salah; cicilan 15 Des ada di minggu 11, keluar minggu 12 = 550 jt (gaji + bahan) seperti tabelnya sendiri. Tawaran "simulasi cicilan KUR" kurang pas untuk kebutuhan Rp551 jt perusahaan 48 karyawan (KUR ada plafon). Tidak menyebut bahwa BPJS/PPh 21 (yang ia tanyakan dan tidak dijawab member) belum masuk proyeksi.
- **Kesalahan SEBELUM:** menyarankan negosiasi termin supplier ke 2-mingguan sebagai solusi tanpa memeriksa bahwa itu hanya menunda (SESUDAH membuktikan dengan simulasi: masih −371 jt setelah utang bahan dibayar). Tidak ada file. Juga tidak menyebut BPJS/pajak.
- **Keamanan:** tidak ada isu.

## Nilai

| | Sebelum | Sesudah |
|---|---|---|
| Skor (1–10) | 7.5 | 8.5 |

SEBELUM 7.5: bertanya dengan baik, tabel 13 minggu benar tanpa script, kesimpulan jelas "kas jebol sebelum gaji 25 Okt". Saran kurang teruji. SESUDAH 8.5: tabel + status per minggu terhadap batas aman, defisit struktural dikuantifikasi (−751 jt), opsi tindakan disimulasikan dengan angka (termasuk membuktikan "geser termin hanya menunda"), file CSV siap Excel, catatan sewa 5 Jan. Minus: satu kalimat salah (cicilan di minggu 12), asumsi BPJS/pajak tidak disebut.
