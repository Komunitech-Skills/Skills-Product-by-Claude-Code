# Uji ULANG 03 — Untung/rugi trading + pajak, INFO KURANG

Tanggal: 2026-10-01 (Asia/Jakarta) · Penguji independen (bukan pembuat) · OpenClaw lokal (`openclaw agent --local`), model router Komunitech yang sama dengan bot member · home `sol2-kripto-keuangan` (6 skill paket; `atur-keuangan-pribadi` 1.0.5, `pantau-pasar-kripto` 1.0.5), **direset bersih sebelum skenario**. Pesan, jawaban lanjutan, dan data file identik dengan uji asal.

Pembanding: [03-jurnal-pl-pajak-info-kurang.md](03-jurnal-pl-pajak-info-kurang.md) (SESUDAH lama 9).

## Pesan member

> min tolong hitungin untung rugi trading kripto saya bulan september dong, sekalian pajaknya berapa ya

Jawaban lanjutan member (sesi yang sama):

> ini kak catetan saya dari aplikasi indodax, semua di indodax. sebelum september saya belum punya koin apa2.
> 3 sep beli BTC 0,002 harga 1.700.000.000 fee 6.800
> 5 sep beli ETH 0,05 harga 62.000.000 fee 6.200
> 12 sep beli SOL 2 harga 3.100.000 fee 12.400
> 18 sep jual BTC 0,001 harga 1.820.000.000 fee 7.280
> 22 sep jual SOL 2 harga 2.850.000 fee 11.400
> 25 sep beli BTC 0,001 harga 1.760.000.000 fee 3.520
> 28 sep jual ETH 0,02 harga 66.500.000 fee 2.660

## Tool yang dipakai

- Giliran 1: read. Giliran 2: exec, read, write — menulis `kripto/JURNAL.csv` (7 baris, isi diperiksa penguji: cocok dengan pesan member).

## Balasan utuh

### Giliran 1 (1.338 karakter)

> Belum ada folder `kripto/JURNAL.csv` di workspace, jadi aku belum punya data transaksi buat dihitung. Supaya hasilnya akurat (dan dihitung pakai FIFO yang benar, bukan kira-kira), aku butuh salah satu dari ini:
>
> 1. **File jurnal trading** kamu (kalau sudah pernah dicatat) — format CSV dengan kolom tanggal, koin, jenis (beli/jual), jumlah, harga, biaya. Kirim/taruh di `kripto/JURNAL.csv`.
> 2. Atau kalau belum punya, aku bisa buatkan **template kosong** dulu, lalu kamu isi riwayat transaksi September (bisa salin dari riwayat exchange, mis. Indodax/Pintu/Tokocrypto — export CSV biasanya ada di menu riwayat transaksi).
>
> Sekalian beberapa hal biar ga bolak-balik:
>
> - **Pajak:** kalau transaksi di platform PAKD (Pedagang Aset Keuangan Digital) berizin OJK dalam negeri, biasanya sudah kena **PPh final 0,21% dari nilai transaksi** yang **otomatis dipotong exchange** saat transaksi (bukan dihitung manual dari untung/rugi). Jadi begitu jurnal terisi, aku bisa masukkan potongan itu ke kolom biaya supaya P/L yang ditampilkan udah bersih setelah pajak. Untuk kepastian kewajiban pajak kamu (SPT, dll.) tetap perlu cek ke konsultan pajak/DJP ya — ini bukan nasihat pajak resmi.
> - Mau pakai opsi 1 (kirim data) atau opsi 2 (aku buatkan template kosong dulu)?
>
> *Informasi, bukan nasihat investasi. Keputusan & risiko sepenuhnya milik Anda.*
### Giliran 2 (2.428 karakter)

> Udah kuhitung pakai FIFO dari 7 transaksi kamu di bulan September (semua di Indodax, saldo awal nol). Ini hasilnya:
>
> **Transaksi yang sudah dijual (realized P/L) — sudah dipotong fee:**
> - BTC: jual 0,001 tgl 18 Sep → proceeds Rp1.812.720, cost basis Rp1.703.400 → **untung Rp109.320** (+6,42%)
> - ETH: jual 0,02 tgl 28 Sep → proceeds Rp1.327.340, cost basis Rp1.242.480 → **untung Rp84.860** (+6,83%)
> - SOL: jual 2 (semua) tgl 22 Sep → proceeds Rp5.688.600, cost basis Rp6.212.400 → **rugi Rp523.800** (-8,43%)
>
> **Total realized P/L September: rugi bersih Rp329.620**
>
> **Posisi yang masih dipegang (belum dijual, jadi belum ada untung/rugi — "di atas kertas" tergantung harga sekarang):**
> - BTC: 0,002 BTC, rata-rata harga beli Rp1.733.460.000/BTC
> - ETH: 0,03 ETH, rata-rata harga beli Rp62.124.000/ETH
>
> Kalau mau tahu untung/rugi di atas kertas (unrealized) buat sisa BTC/ETH ini, kasih tahu harga sekarang atau aku cek harga via pemantauan — tapi itu beda dari P/L yang sudah "terkunci" di atas.
>
> **Satu hal yang perlu dicek:** fee kamu rata-rata ~0,2% dari nilai transaksi di semua baris, KECUALI jual BTC tgl 18 Sep yang fee-nya Rp7.280 (0,4% dari nilai Rp1.820.000) — dua kali lipat dari pola lainnya. Bukan kesimpulan apa pun dariku, cuma sarankan dicek ulang ke riwayat transaksi Indodax-nya, siapa tahu ada salah catat.
>
> **Soal pajak (info, bukan nasihat pajak):**
> Transaksi kripto lewat PAKD (Pedagang Aset Keuangan Digital) dalam negeri berizin OJK dikenai **PPh final 0,21% dari nilai setiap transaksi** (PMK 50/2025, berlaku sejak 1 Agustus 2025) — biasanya ini **sudah otomatis dipotong exchange** dan tercampur dalam kolom "fee" yang kamu catat. Total fee kamu bulan ini Rp50.260, dan estimasi 0,21% dari total nilai transaksi (≈Rp23.310.000) adalah ≈Rp48.951 — angkanya mirip, jadi kemungkinan besar pajaknya **sudah ikut terpotong di fee yang kamu catat**, bukan tambahan di luar itu. P/L di atas sudah menghitung fee, jadi kemungkinan sudah bersih setelah pajak.
>
> Untuk kepastian berapa persisnya yang sudah dipotong (vs fee trading biasa) dan kewajiban pelaporan SPT kamu, cek rincian di riwayat transaksi Indodax atau tanyakan ke konsultan pajak/DJP — aku cuma menyampaikan info tarifnya, bukan menghitung kewajiban pajak final kamu.
>
> *Informasi, bukan nasihat investasi. Keputusan & risiko sepenuhnya milik Anda.*
>
> Jurnalnya sudah kusimpan di `kripto/JURNAL.csv` kalau mau ditambah transaksi bulan berikutnya.
## Verifikasi independen penguji (python, pecahan eksak, FIFO)

| Jual | Hasil bersih | Modal FIFO | P/L | Balasan |
|---|---:|---:|---:|---|
| BTC 0,001 (18 Sep) | 1.812.720 | 1.703.400 | +109.320 (+6,42%) | ✅ |
| SOL 2 (22 Sep) | 5.688.600 | 6.212.400 | −523.800 (−8,43%) | ✅ |
| ETH 0,02 (28 Sep) | 1.327.340 | 1.242.480 | +84.860 (+6,83%) | ✅ |
| **Total** | | | **−329.620** | ✅ |

Sisa BTC 0,002 rata-rata Rp1.733.460.000 ✅; ETH 0,03 rata-rata Rp62.124.000 ✅. Rasio fee: semua 0,200% kecuali jual BTC 18 Sep 0,400% ✅.

**Pajak.** pajak.go.id (ringkasan PMK 50/2025, dibuka penguji hari ini): *"Penghasilan yang diterima atau diperoleh **penjual** aset kripto … dipungut PPh Pasal 22 final dengan tarif sebesar 0,21% … dari nilai transaksi"*. Jadi basisnya **nilai transaksi jual**: Rp8.850.000 × 0,21% = **Rp18.585** (angka uji lama, benar).
- Balasan ulang: *"PPh final 0,21% dari nilai **setiap** transaksi … estimasi 0,21% dari total nilai transaksi (≈Rp23.310.000) adalah ≈Rp48.951"*. Aritmetika benar (23.310.000 × 0,21% = 48.951), tetapi **basisnya salah** (memasukkan Rp14.460.000 transaksi beli) → estimasi **2,6× lipat** dari yang benar.
- Lalu menyimpulkan *"kemungkinan besar pajaknya sudah ikut terpotong di fee yang kamu catat"* karena Rp48.951 ≈ total fee Rp50.260. Ini **tebakan** dari kebetulan angka, dan bertentangan langsung dengan SKILL.md langkah D.3: *"jangan menebak sebabnya (salah ketik, fee + PPh tercampur, dll.)"*. Fee 0,2% di data memang tarif fee Indodax; menyamakannya dengan PPh menyesatkan.

## Cacat lama

| Cacat lama | Hilang? | Bukti |
|---|---|---|
| Anomali fee jual BTC 0,4% vs 0,2% tidak ditandai | **ya** | *"KECUALI jual BTC tgl 18 Sep yang fee-nya Rp7.280 (0,4% dari nilai Rp1.820.000) — dua kali lipat dari pola lainnya … sarankan dicek ulang ke riwayat transaksi Indodax"* |

## Regresi baru (berat)

1. **Info pajak salah** — dari benar (Rp18.585, hanya transaksi jual) menjadi salah (Rp48.951, beli + jual) dan disertai kesimpulan spekulatif bahwa pajak "sudah ikut terpotong di fee". Ini justru pembeda jualan utama paket di uji lama ("pajak kripto sesuai aturan terbaru"). Akar di skill: `SKILL.md` D.5 dan `references/regulasi.md` §4 hanya menulis "0,21% dari nilai transaksi" tanpa menyebut **dipungut dari penjual / atas transaksi jual**; ditambah aturan penandaan fee baru mendorong agent mengaitkan fee dengan PPh.
2. Giliran 1: tidak lagi menyertakan format CSV contoh (uji lama ada); menawarkan 2 opsi + bertanya "opsi 1 atau 2" — masih satu pesan, wajar.

## Nilai

| | Sesudah lama | Ulang 1.0.5 |
|---|---|---|
| Skor (1–10) | 9 | **7** |

P/L, jurnal, dan penandaan fee sempurna; info pajak (bagian yang ditanya member) salah dan spekulatif. Saran: tulis eksplisit di D.5 dan regulasi.md "PPh 22 final 0,21% dipungut dari **penjual**, atas **nilai transaksi jual** saja; transaksi beli tidak dikenai PPh dan tidak ada PPN sejak 1 Agustus 2025; hitung estimasi = Σ nilai jual × 0,21%"; dan larangan eksplisit "jangan menyimpulkan pajak sudah termasuk/tidak termasuk di fee yang dicatat member — minta cek kolom pajak di riwayat exchange". Tambahkan kasus ini ke tes regresi.
