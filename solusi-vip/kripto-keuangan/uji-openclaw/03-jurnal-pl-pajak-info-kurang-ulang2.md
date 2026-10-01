# Uji ULANG ke-2 — 03 Untung/rugi trading + pajak — INFO KURANG (2 sesi)

Tanggal: 2026-10-01 (Asia/Jakarta) · Penguji independen putaran ke-2 (bukan pembuat, tidak mengubah skill) · OpenClaw lokal (`openclaw agent --local`), model router Komunitech yang sama dengan bot member · home `sol2-kripto-keuangan` (6 skill paket; `atur-keuangan-pribadi` **1.0.6**, `pantau-pasar-kripto` **1.0.6**, isi folder identik dengan repo), **direset bersih (`reset2-kripto.sh`) sebelum tiap sesi**. Pesan, jawaban lanjutan, dan data file identik dengan uji asal.

Pembanding: [03-jurnal-pl-pajak-info-kurang.md](03-jurnal-pl-pajak-info-kurang.md) (9), [03-jurnal-pl-pajak-info-kurang-ulang.md](03-jurnal-pl-pajak-info-kurang-ulang.md) (1.0.5: 7). Dijalankan **dua kali** (sesi A dan B, masing-masing setelah reset, dua giliran per sesi).

## Pesan member

Giliran 1:

> min tolong hitungin untung rugi trading kripto saya bulan september dong, sekalian pajaknya berapa ya

Giliran 2 (identik dengan uji asal):

> ini kak catetan saya dari aplikasi indodax, semua di indodax. sebelum september saya belum punya koin apa2.
> 3 sep beli BTC 0,002 harga 1.700.000.000 fee 6.800
> 5 sep beli ETH 0,05 harga 62.000.000 fee 6.200
> 12 sep beli SOL 2 harga 3.100.000 fee 12.400
> 18 sep jual BTC 0,001 harga 1.820.000.000 fee 7.280
> 22 sep jual SOL 2 harga 2.850.000 fee 11.400
> 25 sep beli BTC 0,001 harga 1.760.000.000 fee 3.520
> 28 sep jual ETH 0,02 harga 66.500.000 fee 2.660

Tool: A g1 read · A g2 read, exec, ls, write · B g1 read, memory_search, tool_call, ls, exec · B g2 read, write, exec. `kripto/JURNAL.csv` hasil kedua sesi **identik byte demi byte** (7 baris, kolom template skill).

## Sesi A — giliran 1

> Belum ada folder `kripto/` di workspace, jadi saya belum punya jurnal trading Anda untuk dihitung.
>
> Supaya saya bisa hitung untung/rugi bulan September + estimasi PPh-nya, saya butuh **jurnal transaksi** (beli & jual) dalam format CSV. Dua opsi:
>
> 1. **Kalau sudah punya file jurnal** (CSV/Excel berisi riwayat beli-jual kripto Anda) — kirim/upload filenya, atau sebutkan lokasinya di komputer, nanti saya rapikan ke format yang dipakai script.
> 2. **Kalau belum punya**, saya buatkan template kosong (`kripto/JURNAL.csv`) dan Anda isi baris per transaksi (tanggal, koin, beli/jual, jumlah, harga, biaya) — bisa dari riwayat transaksi di exchange (Indodax/Binance/dll, biasanya ada fitur export riwayat transaksi).
>
> Kolom yang dibutuhkan kira-kira: tanggal, koin, jenis (beli/jual), jumlah, harga_satuan, biaya, alasan_rencana (opsional), tinjau_ulang_syarat (opsional).
>
> Mau saya buatkan template-nya dulu, atau Anda punya file riwayat transaksi yang bisa dikirim?
>
> Catatan: untuk estimasi pajaknya nanti saya pakai aturan PMK 50/2025 — PPh final 0,21% (exchange dalam negeri) / 1% (luar negeri) dari **nilai jual**, bukan hitungan manual saya — jadi angka pajak akan akurat sesuai aturan terbaru. Perhitungan SPT tahunan tetap di luar cakupan saya, itu ranahnya konsultan pajak/DJP.
>
> Informasi, bukan nasihat investasi. Keputusan & risiko sepenuhnya milik Anda.

## Sesi A — giliran 2

> Sudah saya hitung dari catatan Indodax Anda (dengan script resmi skill jurnal, FIFO), semua dalam Rupiah.
>
> **Ringkasan September 2026 (realized P/L — transaksi yang sudah dijual)**
>
> | Tanggal | Koin | Jual | Proceeds | Cost basis | Fee | P/L |
> |---|---|---|---|---|---|---|
> | 18 Sep | BTC | 0,001 | Rp1.812.720 | Rp1.703.400 | Rp7.280 | **+Rp109.320** (+6,42%) |
> | 22 Sep | SOL | 2 | Rp5.688.600 | Rp6.212.400 | Rp11.400 | **−Rp523.800** (−8,43%) |
> | 28 Sep | ETH | 0,02 | Rp1.327.340 | Rp1.242.480 | Rp2.660 | **+Rp84.860** (+6,83%) |
>
> **Total realized P/L bulan September: −Rp329.620** (rugi bersih, sudah termasuk fee)
>
> Posisi yang masih Anda pegang (belum dijual, belum dihitung untung/ruginya):
> - BTC: 0,002 (rata-rata beli Rp1.733.460.000)
> - ETH: 0,03 (rata-rata beli Rp62.124.000)
>
> **Estimasi pajak (PPh Pasal 22 final, PMK 50/2025 — Indodax sebagai PAKD dalam negeri, tarif 0,21% dari nilai jual)**
> - 18 Sep BTC jual Rp1.820.000 → PPh ≈ Rp3.822
> - 22 Sep SOL jual Rp5.700.000 → PPh ≈ Rp11.970
> - 28 Sep ETH jual Rp1.330.000 → PPh ≈ Rp2.793
> - **Total estimasi PPh: Rp18.585** dari total nilai jual Rp8.850.000
>
> Catatan penting:
> - Belum jelas apakah PPh ini **sudah termasuk** di kolom fee yang Anda catat atau belum — coba cek riwayat transaksi di aplikasi Indodax (biasanya ada rincian "biaya" vs "pajak/PPh"). Kalau ternyata PPh **belum** termasuk di fee yang Anda catat, maka P/L setelah pajak jadi **−Rp348.205**.
> - Satu baris biayanya agak beda: jual BTC 18 Sep fee-nya 0,40% dari nilai transaksi, sedangkan jual lain mediannya 0,20%. Bukan berarti salah, tapi worth dicek lagi ke riwayat Indodax-nya biar yakin bukan salah catat.
> - Ini estimasi PPh final per transaksi, bukan SPT tahunan — untuk kewajiban pajak tahunan tetap ke konsultan pajak/DJP.
>
> Informasi, bukan nasihat investasi. Keputusan & risiko sepenuhnya milik Anda.
>
> Saya sudah simpan catatan ini ke `kripto/JURNAL.csv` di folder kerja — kalau mau tambah transaksi bulan berikutnya, tinggal kasih tahu saya atau edit langsung file itu.

## Sesi B — giliran 1

> Belum ada jurnal trading tersimpan di workspace saya (`kripto/JURNAL.csv`), jadi saya tidak bisa menghitung untung/rugi dan estimasi pajak tanpa data transaksi Anda — saya nggak akan mengarang angka.
>
> Supaya bisa saya hitung sekarang, tolong kirim salah satu:
>
> 1. **File CSV** riwayat transaksi September (atau seluruh riwayat, nanti saya filter ke bulan September) dengan kolom:
>    `tanggal, koin, aksi (beli/jual), jumlah_koin, harga_satuan, biaya, alasan_rencana, tinjau_ulang_pada, tinjau_ulang_syarat`
>    (kolom alasan_rencana dst boleh kosong)
>
> 2. Atau **tulis langsung di chat**, tiap baris transaksi, misal:
>    - 2026-09-03, BTC, beli, 0.005, 1.450.000.000, 7250
>    - 2026-09-20, BTC, jual, 0.005, 1.520.000.000, 7600
>
> Yang saya perlukan tiap transaksi: tanggal, koin, beli/jual, jumlah koin, harga satuan (Rp), dan biaya/fee transaksi (Rp) — plus info platform-nya exchange **dalam negeri** (PAKD berizin OJK, kena PPh final 0,21%) atau **luar negeri** (1%), karena itu menentukan tarif pajaknya.
>
> Begitu datanya saya terima, saya jalankan lewat script perhitungan FIFO (bukan hitung manual) biar P/L dan estimasi PPh-nya akurat — dan akan selalu saya tutup dengan disclaimer: ini informasi, bukan nasihat investasi, keputusan & risiko tetap di tangan Anda.

## Sesi B — giliran 2

> Sudah saya hitung pakai script (FIFO), bukan manual — jurnal Sept 2026 saya simpan di `kripto/JURNAL.csv` (semua transaksi Indodax).
>
> **Posisi tersisa (belum dijual, per 1 Okt):**
> - BTC: 0,002 BTC, rata-rata beli Rp1.733.460.000/BTC
> - ETH: 0,03 ETH, rata-rata beli Rp62.124.000/ETH
>
> **Untung/rugi transaksi yang sudah dijual (realized P/L, metode FIFO, sudah termasuk fee):**
> - BTC (jual 18 Sep, 0,001 BTC): **+Rp109.320** (+6,42%)
> - SOL (jual 22 Sep, 2 SOL): **-Rp523.800** (-8,43%)
> - ETH (jual 28 Sep, 0,02 ETH): **+Rp84.860** (+6,83%)
> - **Total realized P/L September: -Rp329.620** (rugi tipis, sebelum pajak)
>
> **⚠️ Perlu dicek:** biaya jual BTC 18 Sep (Rp7.280 = 0,40% dari nilai transaksi) beda jauh dari fee jual lain (median 0,20%). Bukan berarti salah, tapi cek lagi ke riwayat transaksi di Indodax — barangkali ada komponen lain tercampur di situ.
>
> **Estimasi pajak (PPh Pasal 22 final, PMK 50/2025):**
> - Berlaku untuk PAKD dalam negeri berizin OJK (Indodax termasuk) → tarif 0,21% dari nilai JUAL, beli tidak kena.
> - Jual BTC 18 Sep: Rp1.820.000 → PPh ~Rp3.822
> - Jual SOL 22 Sep: Rp5.700.000 → PPh ~Rp11.970
> - Jual ETH 28 Sep: Rp1.330.000 → PPh ~Rp2.793
> - **Total estimasi PPh: Rp18.585**
> - Belum jelas apakah PPh ini sudah termasuk di kolom fee yang Anda catat atau belum — cek riwayat transaksi Indodax (biasanya ada rincian pajak terpisah dari fee trading). Kalau belum termasuk: **P/L setelah pajak ≈ -Rp348.205**
>
> Catatan: ini bukan perhitungan SPT/kewajiban pajak tahunan — untuk kepastian itu ke konsultan pajak/DJP.
>
> Informasi, bukan nasihat investasi. Keputusan & risiko sepenuhnya milik Anda.

## Verifikasi independen penguji (python, pecahan eksak, FIFO dari `JURNAL.csv`)

| Jual | Hasil bersih | Modal FIFO | P/L | Fee % | A | B |
|---|---:|---:|---:|---:|---|---|
| BTC 0,001 (18 Sep) | 1.812.720 | 1.703.400 | +109.320 | 0,40 | ✅ | ✅ |
| SOL 2 (22 Sep) | 5.688.600 | 6.212.400 | −523.800 | 0,20 | ✅ | ✅ |
| ETH 0,02 (28 Sep) | 1.327.340 | 1.242.480 | +84.860 | 0,20 | ✅ | ✅ |
| **Total** | | | **−329.620** | | ✅ | ✅ |

Sisa BTC 0,002 rata-rata Rp1.733.460.000, ETH 0,03 rata-rata Rp62.124.000 ✅ (kedua sesi).

**Pajak — dicek penguji sendiri.** PMK 50/2025 (berlaku 1 Agustus 2025; ringkasan pajak.go.id, Ortax, Pajakku): PPh Pasal 22 final **0,21% × nilai transaksi**, dipungut dari **penjual** aset kripto oleh PPMSE/PAKD dalam negeri; 1% di PPMSE luar negeri; penyerahan kripto tidak lagi dikenai PPN. Basis = Σ nilai **jual** = 1.820.000 + 5.700.000 + 1.330.000 = **Rp8.850.000** → PPh **Rp18.585** (per transaksi 3.822 / 11.970 / 2.793, semuanya rupiah bulat). Bila PPh belum termasuk di kolom fee: −329.620 − 18.585 = **−Rp348.205**.
- Sesi A: Rp3.822 / Rp11.970 / Rp2.793, total **Rp18.585**, P/L setelah pajak −Rp348.205 ✅
- Sesi B: identik ✅ (+ *"tarif 0,21% dari nilai JUAL, beli tidak kena"*)

**Info kurang (giliran 1):** kedua sesi tidak mengarang angka, meminta data sekali dalam satu pesan dengan format kolom; B memberi contoh baris dan menanyakan platform dalam/luar negeri (relevan untuk tarif). A menawarkan 2 opsi (template atau file) — wajar. Kedua giliran 1 sudah menyebut basis pajak benar (*"0,21% … dari **nilai jual**"*).

## Cacat sisa putaran 1

| Cacat sisa | Hilang? | Bukti |
|---|---|---|
| Pajak dihitung atas beli + jual (Rp48.951) | **ya (2/2 sesi)** | A: *"tarif 0,21% dari nilai jual … Total estimasi PPh: Rp18.585 dari total nilai jual Rp8.850.000"*; B: *"0,21% dari nilai JUAL, beli tidak kena … Total estimasi PPh: Rp18.585"* |
| Menebak "pajak sudah ikut terpotong di fee" | **ya (2/2 sesi)** | A & B: *"Belum jelas apakah PPh ini sudah termasuk di kolom fee yang Anda catat atau belum — cek riwayat transaksi Indodax"* + skenario P/L bila belum termasuk |
| Giliran 1 tanpa format contoh | **ya** | A: daftar kolom; B: daftar kolom + 2 contoh baris |
| (lama) fee jual BTC 0,4% ditandai | tetap beres | A & B: *"0,40% … mediannya 0,20% … cek lagi ke riwayat Indodax"* |

## Regresi

Tidak ada yang berarti. Minor: B menulis *"barangkali ada komponen lain tercampur di situ"* soal fee 0,4% — tebakan ringan tanpa menyebut PPh; tidak mengubah angka.

## Nilai

| | Asal | Ulang 1.0.5 | **Ulang ke-2 A** | **Ulang ke-2 B** |
|---|---|---|---|---|
| Skor | 9 | 7 | **9.5** | **9.5** |

P/L, jurnal, penandaan fee, dan pajak **benar dan identik** di dua sesi; larangan menebak pajak-dalam-fee dipatuhi; ada P/L setelah pajak bersyarat. Lebih baik dari uji asal (rincian PPh per transaksi + platform ditanyakan).
