# Uji OpenClaw 03 — Hitung untung/rugi trading + pajak — INFO KURANG (tanpa data transaksi)

Tanggal: 2026-10-01 (Asia/Jakarta) · Agent: OpenClaw lokal (`openclaw agent --local`), model router Komunitech yang sama dengan bot member. SEBELUM = home `kosong-kripto-keuangan` (tanpa skill), SESUDAH = home `sol-kripto-keuangan` (6 skill paket). Kedua home dibuat ulang bersih sebelum skenario ini.

## Pesan member (identik di kedua sisi)

> min tolong hitungin untung rugi trading kripto saya bulan september dong, sekalian pajaknya berapa ya

Jawaban lanjutan member (sesi yang sama, identik di kedua sisi):

> ini kak catetan saya dari aplikasi indodax, semua di indodax. sebelum september saya belum punya koin apa2.
> 3 sep beli BTC 0,002 harga 1.700.000.000 fee 6.800
> 5 sep beli ETH 0,05 harga 62.000.000 fee 6.200
> 12 sep beli SOL 2 harga 3.100.000 fee 12.400
> 18 sep jual BTC 0,001 harga 1.820.000.000 fee 7.280
> 22 sep jual SOL 2 harga 2.850.000 fee 11.400
> 25 sep beli BTC 0,001 harga 1.760.000.000 fee 3.520
> 28 sep jual ETH 0,02 harga 66.500.000 fee 2.660

## Tool yang dipakai

- SEBELUM: giliran 1 `ls`, `memory_search`; giliran 2 **tanpa tool** (hitung di kepala).
- SESUDAH: giliran 1 membaca `pantau-pasar-kripto/SKILL.md`, cek `kripto/`; giliran 2 menulis `kripto/JURNAL.csv` (format template skill) dan menjalankan `scripts/hitung_pl_jurnal.py --dari 2026-09-01 --sampai 2026-09-30`.

## SEBELUM (tanpa skill) — balasan utuh

### Giliran 1

> Sudah saya cek memory dan workspace — belum ada catatan transaksi trading kripto kamu tersimpan di sana, jadi aku nggak bisa hitung untung/rugi bulan September tanpa data transaksinya dulu.
>
> Supaya bisa aku hitungin akurat, tolong kasih salah satu dari ini:
>
> 1. **Export CSV/Excel** riwayat transaksi September dari exchange kamu (Indodax, Tokocrypto, Reku, Binance, dll) — biasanya ada menu "Export Transaction History" atau "Riwayat Transaksi".
> 2. Atau kalau transaksinya nggak banyak, kirim manual aja per transaksi: tanggal, aset (misal BTC/ETH), beli/jual, harga saat itu, jumlah, dan fee (kalau ada).
>
> Juga tolong konfirmasi:
> - **Exchange mana** yang dipakai? (Ini penting buat tarif pajak — beda antara exchange yang **terdaftar PFAK/Bappebti-OJK** vs yang nggak)
> - Semua transaksi di exchange yang sama, atau ada beberapa platform?
>
> **Soal pajaknya** sekilas, di Indonesia pajak kripto itu sifatnya **final per transaksi jual**, bukan dari total untung/rugi:
> - Exchange **terdaftar** di Indonesia (Indodax, Tokocrypto, Reku, Pintu, dll): **PPh Final 0,1%** + **PPN 0,11%** dari nilai transaksi jual — biasanya udah **dipotong otomatis** sama exchange-nya dan ada bukti potongnya.
> - Exchange **luar negeri/tidak terdaftar** (Binance global, dll): tarifnya lebih tinggi, **PPh 0,2%** + **PPN 0,22%**, dan ini biasanya **belum dipotong** jadi harus kamu setor/lapor sendiri.
>
> Jadi untung/rugi (buat kamu pribadi) aku hitung dari selisih harga jual-beli, sementara pajaknya tergantung status exchange di atas. Kirim datanya ya, nanti langsung aku rekap lengkap sama estimasi pajaknya.

### Giliran 2

> Udah aku hitung lengkap pakai metode FIFO (yang dibeli duluan, dijual duluan). Ini hasilnya:
>
> **📊 Ringkasan Laba/Rugi per Aset (September 2026)**
>
> 🟠 **BTC**
> - Beli 3 Sep: 0,002 @ Rp1.700.000.000 (fee Rp6.800)
> - Jual 18 Sep: 0,001 @ Rp1.820.000.000 (fee Rp7.280)
> - Modal yang terjual: Rp1.703.400 | Hasil jual bersih: Rp1.812.720
> - **Untung: +Rp109.320**
> - Sisa: 0,001 BTC (dari lot pertama) + 0,001 BTC (beli 25 Sep @ Rp1.760.000.000, fee Rp3.520) → total sisa 0,002 BTC, modal Rp3.466.920 (belum dijual, belum masuk hitungan untung/rugi)
>
> 🔵 **ETH**
> - Beli 5 Sep: 0,05 @ Rp62.000.000 (fee Rp6.200)
> - Jual 28 Sep: 0,02 @ Rp66.500.000 (fee Rp2.660)
> - Modal yang terjual: Rp1.242.480 | Hasil jual bersih: Rp1.327.340
> - **Untung: +Rp84.860**
> - Sisa: 0,03 ETH, modal Rp1.863.720 (belum dijual)
>
> 🟣 **SOL**
> - Beli 12 Sep: 2 @ Rp3.100.000 (fee Rp12.400)
> - Jual 22 Sep: 2 @ Rp2.850.000 (fee Rp11.400) — semua terjual
> - Modal: Rp6.212.400 | Hasil jual bersih: Rp5.688.600
> - **Rugi: -Rp523.800**
>
> **💰 Total Realized P&L September: Rp(329.620) — rugi tipis**
> (Untung BTC + untung ETH − rugi SOL, fee exchange sudah termasuk)
>
> Total fee trading yang kebayar: Rp50.260
>
> ---
>
> **🧾 Estimasi Pajak Kripto**
>
> Indodax itu exchange terdaftar resmi di Bappebti/OJK (PFAK), jadi tarifnya yang rendah:
> - **PPN 0,11%** dari nilai transaksi — dikenakan di transaksi beli maupun jual
> - **PPh Final 0,1%** dari nilai transaksi — dikenakan khusus di transaksi jual
>
> Rincian per transaksi:
>
> | Transaksi | Nilai | PPN 0,11% | PPh 0,1% |
> |---|---|---|---|
> | Beli BTC 3 Sep | 3.400.000 | 3.740 | - |
> | Beli ETH 5 Sep | 3.100.000 | 3.410 | - |
> | Beli SOL 12 Sep | 6.200.000 | 6.820 | - |
> | Jual BTC 18 Sep | 1.820.000 | 2.002 | 1.820 |
> | Jual SOL 22 Sep | 5.700.000 | 6.270 | 5.700 |
> | Beli BTC 25 Sep | 1.760.000 | 1.936 | - |
> | Jual ETH 28 Sep | 1.330.000 | 1.463 | 1.330 |
>
> **Total PPN: Rp25.641**
> **Total PPh Final: Rp8.850**
> **Total Pajak: ± Rp34.491**
>
> Catatan penting: di Indodax, pajak ini **biasanya sudah otomatis dipotong** oleh sistem di setiap transaksi (lihat di "Riwayat Transaksi" atau "Mutasi" — kadang terpisah dari kolom "fee" yang kamu kirim). Jadi kemungkinan besar kamu **tidak perlu lapor/setor sendiri** lagi — tapi cek lagi detail breakdown di app Indodax (biasanya ada kolom "Pajak" terpisah) buat mastiin nilai fee yang kamu catat itu murni fee trading atau udah termasuk pajak, soalnya ratio fee BTC jual 18 Sep (0,4%) beda dari transaksi lain (0,2%) — kemungkinan itu udah termasuk pajak di dalamnya.
>
> **Kesimpulan:** Secara realized, trading kamu bulan September **rugi tipis Rp329.620** (dari fee+rugi SOL yang lebih besar dari untung BTC+ETH). Posisi kripto yang masih kamu pegang (0,002 BTC + 0,03 ETH) belum dihitung untung/ruginya karena belum dijual — kalau mau tau unrealized P&L-nya, kasih tau harga BTC/ETH sekarang ya.

## SESUDAH (dengan paket skill) — balasan utuh

### Giliran 1

> Belum ada jurnal trading kamu di sini (`kripto/JURNAL.csv` belum dibuat), jadi aku belum bisa hitung untung-rugi Septembernya — ngarang angka jelas nggak boleh.
>
> Supaya bisa dihitung otomatis (FIFO, sudah termasuk biaya), aku perlu data transaksi kripto kamu bulan September (atau lebih, biar cost basis-nya akurat kalau ada beli sebelum September). Formatnya gini, per baris:
>
> tanggal, koin, aksi (beli/jual), jumlah_koin, harga_satuan (Rp), biaya (fee, Rp), alasan_rencana (opsional), tinjau_ulang_pada (opsional), tinjau_ulang_syarat (opsional)
>
> Contoh:
> ```
> tanggal,koin,aksi,jumlah_koin,harga_satuan,biaya,alasan_rencana,tinjau_ulang_pada,tinjau_ulang_syarat
> 2026-09-05,BTC,beli,0.01,900000000,9000,,,
> 2026-09-20,BTC,jual,0.005,950000000,9500,,,
> ```
>
> Bisa kamu kirim datanya (boleh langsung di chat atau export CSV dari exchange), atau kalau sudah punya riwayat transaksi di aplikasi exchange, tinggal salin saja. Setelah itu aku jalankan skrip hitung P/L (FIFO) khusus untuk transaksi bulan September, dan sekalian jelasin soal pajak PPh final 0,21% yang biasanya sudah dipotong otomatis exchange.
>
> Info soal pajaknya duluan ya sambil nunggu datamu:
> - Kalau transaksi kamu lewat PAKD (Pedagang Aset Keuangan Digital) berizin OJK dalam negeri (exchange lokal resmi seperti Indodax, Pintu, Tokocrypto, dll.), dikenai **PPh final 0,21%** dari nilai transaksi jual — ini **biasanya sudah otomatis dipotong exchange** saat kamu jual, jadi kamu nggak perlu setor sendiri lagi untuk itu.
> - Potongan ini bisa aku masukkan ke kolom `biaya` di jurnal biar P/L yang dihitung sudah bersih setelah pajak.
> - Untuk kepastian kewajiban pajak kamu secara pribadi (misalnya kalau ada penghasilan lain, lapor SPT, dll.), tetap perlu cek ke konsultan pajak atau DJP langsung — aku nggak hitung SPT/pelaporan pajak.
>
> Kirim data transaksinya ya, nanti langsung aku hitungin.
>
> *Informasi, bukan nasihat investasi. Keputusan & risiko sepenuhnya milik Anda.*

### Giliran 2

> Udah aku hitung pakai script FIFO (biar akurat per lot), ini hasilnya untuk **September 2026** — semua transaksi kamu di Indodax:
>
> ## Ringkasan P/L (realized, dari yang sudah dijual)
>
> | Koin | Tgl Jual | Jual | Proceeds | Cost Basis (FIFO) | Fee | P/L | % |
> |---|---|---|---|---|---|---|---|
> | BTC | 18 Sep | 0,001 | Rp 1.812.720 | Rp 1.703.400 | Rp 7.280 | **+Rp 109.320** | +6,42% |
> | SOL | 22 Sep | 2 | Rp 5.688.600 | Rp 6.212.400 | Rp 11.400 | **-Rp 523.800** | -8,43% |
> | ETH | 28 Sep | 0,02 | Rp 1.327.340 | Rp 1.242.480 | Rp 2.660 | **+Rp 84.860** | +6,83% |
>
> **Total realized P/L September: -Rp 329.620 (rugi bersih)**
>
> SOL yang bikin minus — jual di harga lebih rendah dari beli.
>
> ## Posisi yang masih dipegang (belum direalisasi)
> - **BTC**: 0,002 (sisa dari 2 lot: beli 3 Sep + 25 Sep), harga rata-rata perolehan ≈ Rp 1.733.460.000/BTC
> - **ETH**: 0,03, harga rata-rata perolehan ≈ Rp 62.124.000/ETH
>
> (Ini belum untung/rugi karena belum dijual — nilainya tergantung harga pasar sekarang kalau mau dicek.)
>
> ## Soal pajak (info, bukan nasihat pajak)
> Transaksi di Indodax (PAKD berizin OJK) kena **PPh final 0,21%** dari nilai transaksi **jual**, biasanya **otomatis dipotong exchange** saat itu juga — bukan kamu setor manual belakangan.
>
> Total nilai jual September kamu: Rp 1.820.000 + Rp 5.700.000 + Rp 1.330.000 = **Rp 8.850.000**
> Estimasi PPh final 0,21%: **≈ Rp 18.585**
>
> Catatan: fee yang kamu catat (6.800, 6.200, dst.) kelihatannya fee trading Indodax (~0,2%), bukan PPh-nya — biasanya potongan PPh ini terpisah dan sudah otomatis di history transaksi Indodax kamu. Kalau mau cross-check angka pastinya, cek di riwayat transaksi/laporan pajak di app Indodax (biasanya ada menu khusus laporan pajak/PPh).
>
> Untuk kepastian kewajiban pajak kamu secara keseluruhan (misal kalau digabung penghasilan lain, perlu lapor di SPT atau tidak), tetap aku arahkan ke konsultan pajak atau DJP langsung ya — bukan ranah aku hitung SPT.
>
> Data transaksinya udah aku simpan rapi di `kripto/JURNAL.csv` biar gampang dilanjutin bulan depan — tinggal tambah baris baru aja.
>
> *Informasi, bukan nasihat investasi. Keputusan & risiko sepenuhnya milik Anda.*

## Verifikasi independen penguji

**Info kurang (giliran 1):** keduanya tidak mengarang angka dan meminta data sekali dalam satu pesan. SESUDAH memberi format CSV baku; SEBELUM menawarkan export CSV atau ketik manual + menanyakan exchange.

**P/L FIFO (hitung ulang penguji, pecahan eksak):**

| Jual | Hasil bersih | Modal FIFO | P/L | SEBELUM | SESUDAH |
|---|---:|---:|---:|---|---|
| BTC 0,001 (18 Sep) | 1.812.720 | 1.703.400 | +109.320 | ✅ | ✅ (+6,42%) |
| SOL 2 (22 Sep) | 5.688.600 | 6.212.400 | −523.800 | ✅ | ✅ (−8,43%) |
| ETH 0,02 (28 Sep) | 1.327.340 | 1.242.480 | +84.860 | ✅ | ✅ (+6,83%) |
| **Total** | | | **−329.620** | ✅ | ✅ |

Sisa: BTC 0,002 modal Rp3.466.920 (rata-rata Rp1.733.460.000) ✅ kedua sisi; ETH 0,03 modal Rp1.863.720 (rata-rata Rp62.124.000) ✅. Angka P/L **sama benarnya** di kedua sisi.

**Pajak — pembeda utama:**
- Aturan berlaku sejak **1 Agustus 2025: PMK 50/2025** — aset kripto tidak lagi dikenai PPN; PPh Pasal 22 final **0,21%** dari nilai transaksi lewat PAKD dalam negeri, **1%** lewat platform luar negeri ([pajak.go.id](https://www.pajak.go.id/en/node/117234), [Ortax](https://ortax.org/tarif-naik-penjualan-kripto-kini-dipungut-pph-pasal-22-0-21-persen)). Ketentuan kripto lama (PMK 68/2022, kemudian disesuaikan PMK 81/2024) tidak berlaku lagi untuk transaksi setelah tanggal itu.
- **SEBELUM: SALAH / usang.** Memakai tarif lama PPh final 0,1% + **PPN 0,11% atas beli dan jual** (luar negeri 0,2% + 0,22%), menyebut "PFAK/Bappebti". Estimasi "Total pajak ± Rp34.491" (PPN Rp25.641 + PPh Rp8.850) — aritmetikanya benar untuk tarif lama, tetapi tarifnya tidak berlaku lagi untuk September 2026.
- **SESUDAH: BENAR.** Nilai jual Rp8.850.000 × 0,21% = **Rp18.585** ✅, dipotong otomatis exchange, arahkan ke konsultan/DJP untuk SPT. Tidak menyebut tarif 1% luar negeri (tidak relevan di kasus ini).

**Catatan jujur:** fee jual BTC tanggal 18 Sep di data uji = 0,4% dari nilai (lainnya 0,2%). SEBELUM **menangkap kejanggalan ini** dan menyarankan cek apakah fee itu sudah termasuk pajak; SESUDAH menyebut semua fee "~0,2%" (terlewat).

## Nilai

| | Sebelum | Sesudah |
|---|---|---|
| Skor (1–10) | 5.5 | 9 |

- SEBELUM 5.5: P/L akurat walau tanpa script dan jeli soal fee, tetapi **informasi pajaknya usang** (PPN atas beli & jual, PPh 0,1%) — member diberi angka pajak yang salah hampir 2× lipat dan dasar aturan yang tidak berlaku.
- SESUDAH 9: P/L dihitung script (FIFO, terverifikasi), pajak sesuai PMK 50/2025, jurnal tersimpan rapi untuk bulan depan, disclaimer. Minus: melewatkan anomali fee.
- Skill terpakai: `pantau-pasar-kripto` (SKILL.md, template `JURNAL.csv`, `hitung_pl_jurnal.py`, aturan pajak di SKILL.md/`references/regulasi.md`).
