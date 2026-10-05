# Uji ULANG ke-2 — 02 Budget bulanan & dana darurat dari mutasi rekening (2 sesi)

Tanggal: 2026-10-01 (Asia/Jakarta) · Penguji independen putaran ke-2 (bukan pembuat, tidak mengubah skill) · OpenClaw lokal (`openclaw agent --local`), model router Komunitech yang sama dengan bot member · home `sol2-kripto-keuangan` (6 skill paket; `atur-keuangan-pribadi` **1.0.6**, `pantau-pasar-kripto` **1.0.6**, isi folder identik dengan repo), **direset bersih (`reset2-kripto.sh`) sebelum tiap sesi**. Pesan, jawaban lanjutan, dan data file identik dengan uji asal.

Pembanding: [02-budget-dana-darurat-mutasi.md](02-budget-dana-darurat-mutasi.md) (8), [02-budget-dana-darurat-mutasi-ulang.md](02-budget-dana-darurat-mutasi-ulang.md) (1.0.5: 8). Data: `mutasi-september.csv` yang sama (24 baris) disalin ke workspace setelah reset. Dijalankan **dua kali** (sesi A dan B, masing-masing setelah reset) untuk melihat konsistensi angka.

## Pesan member

> kak ini mutasi rekening saya bulan september, filenya mutasi-september.csv. tolong bikinin budget bulanan yg masuk akal ya, sama dana darurat saya harusnya berapa. saya udah nikah anak 1, istri ga kerja. tabungan saya sekarang cuma 4 juta. jujur tiap akhir bulan suka mepet 😅

Tool: A = ls, read, exec · B = ls, read, exec (tidak ada tanda pencarian ke luar workspace di balasan).

## Balasan utuh — sesi A (4.777 karakter)

> Udah aku cek mutasinya dan hitung pakai kalkulator keuangan (bukan kira-kira). Ringkasnya duluan ya:
>
> ## Ringkasan
> Gaji Rp9,5jt/bulan kamu sebenarnya **cukup** buat semua kebutuhan wajib + cicilan + kiriman ibu (total Rp7,6jt), tapi penyebab mepet di akhir bulan itu **bukan dari situ** — ada Rp4,4jt (46% gaji!) kebocoran di pos yang nggak punya budget: top-up Indodax Rp2,5jt, tarik tunai Rp500rb, top-up GoPay+OVO Rp800rb, Shopee order + KFC Rp600rb. Dana darurat kamu sekarang Rp4jt, idealnya Rp68–91jt (9–12 bulan pengeluaran pokok) karena udah berkeluarga + ada anak — jauh, tapi bisa dicicil kalau kebocoran di atas ditutup dulu.
>
> ## Anggaran Bulanan (zero-based, dari Rp9,5jt gaji)
>
> | Pos | Kelompok | Jumlah | % |
> |---|---|---:|---:|
> | Kontrakan | Wajib | Rp2.000.000 | 21,1% |
> | Cicilan Motor Adira | Wajib | Rp1.150.000 | 12,1% |
> | Cicilan Shopee PayLater | Wajib | Rp650.000 | 6,8% |
> | Belanja Dapur | Wajib | Rp1.800.000 | 18,9% |
> | Listrik (Token) | Wajib | Rp350.000 | 3,7% |
> | SPP PAUD Anak | Wajib | Rp350.000 | 3,7% |
> | Pulsa & Data | Wajib | Rp150.000 | 1,6% |
> | Transport/BBM | Wajib | Rp150.000 | 1,6% |
> | Admin Bank | Wajib | Rp15.000 | 0,2% |
> | Kiriman Ibu | Keluarga/sosial | Rp1.000.000 | 10,5% |
> | Arisan RT | Tabungan | Rp500.000 | 5,3% |
> | **Dana Darurat** | Tabungan | **Rp785.000** | 8,3% |
> | Jajan & Hiburan | Keinginan | Rp300.000 | 3,2% |
> | Jatah bebas (e-wallet dll, sesuai pemakaian) | Keinginan | Rp300.000 | 3,2% |
> | **Total** | | **Rp9.500.000** | 100% |
>
> Dibanding pola 50/30/20: Kebutuhan kamu 80% (normal buat keluarga dengan anak, kota dengan kontrakan+cicilan), Keinginan cuma 6,3%, Tabungan 13,5%. Total cicilan (motor+paylater) = 18,9% dari gaji — masih di bawah batas aman 30%, oke.
>
> ## Realisasi September vs rencana di atas (dari mutasi kamu)
> Pos wajib (kontrakan, motor, paylater, listrik, SPP, pulsa, dapur ~Rp1,79jt, SPBU) semuanya **sudah pas/sesuai budget**. Yang bikin jebol:
>
> | Pos realisasi September | Jumlah | Catatan |
> |---|---:|---|
> | Topup Indodax (crypto) x2 | Rp2.500.000 | **Tidak ada di budget sama sekali** — ini porsi terbesar penyebab mepet |
> | Tarik tunai ATM | Rp500.000 | Uang cash gampang hilang jejak, tidak jelas kepakai ke mana |
> | Topup GoPay + OVO | Rp800.000 | |
> | Shopee order + QRIS KFC | Rp598.000 | |
> | Dana darurat disisihkan | Rp0 | Budget-nya Rp785rb, realisasi nihil |
>
> Bukan soal kripto-nya bagus/jelek ya (itu di luar kapasitas aku buat kasih saran beli/jual) — tapi dari sisi anggaran, Rp2,5jt/bulan ke situ itu nggak punya "jatah", jadi otomatis makan jatah tabungan+dana darurat. Keputusan naik/turunin nominalnya di tangan kamu sepenuhnya.
>
> ## Dana Darurat — Target
> Status: menikah + anak → target **9–12 bulan** pengeluaran pokok (Rp7.615.000/bulan).
>
> | Target | Jumlah | Kekurangan | Lama (setoran Rp785rb/bln) |
> |---|---:|---:|---:|
> | 9 bulan | Rp68.535.000 | Rp64.535.000 | ~83 bulan (6 th 11 bln) |
> | 12 bulan | Rp91.380.000 | Rp87.380.000 | ~9 th 4 bln |
>
> Itu lama banget kalau langsung incar target penuh — jangan patah semangat dulu. Ambil **milestone awal 1 bulan pokok (Rp7.615.000)** dulu: kekurangan dari saldo Rp4jt kamu sekarang = Rp3.615.000, dengan setoran Rp785rb/bulan ≈ **5 bulan** udah kecapai. Itu bikin kamu punya bantalan kalau motor rewel/anak sakit, baru lanjut nyicil ke 9–12 bulan.
>
> ## Asumsi yang dipakai
> - Pemasukan budget pakai gaji tetap Rp9,5jt saja; proyek desain Rp1,25jt bulan ini dianggap bonus (nggak pasti tiap bulan) — kalau dapat lagi, arahkan ke dana darurat biar lebih cepat.
> - Pokok dana darurat = kebutuhan wajib + cicilan + kiriman ibu (tetap harus dibayar walau gajian berhenti). Arisan, dana darurat sendiri, jajan **tidak** dihitung pokok.
> - Kiriman ke Ibu dianggap wajib rutin (bukan opsional) — kalau sebenarnya fleksibel saat darurat, kabari aku, target bisa turun jadi Rp6,6jt pokok.
>
> ## Langkah minggu ini
> 1. Set autodebet/auto-transfer Rp785rb ke rekening/produk dana darurat terpisah di tanggal gajian — jangan nunggu "sisa", soalnya selama ini sisa = Rp0.
> 2. Putuskan nominal wajar buat topup Indodax (misal jauh di bawah Rp2,5jt) biar nggak makan jatah dana darurat — ini keputusan kamu, bukan saranku soal kripto.
> 3. Catat tarik tunai & topup e-wallet dipakai buat apa 1 minggu ini, biar nggak ada "uang hilang" tanpa jejak.
> 4. Kejar milestone 1 bulan dana darurat (Rp7,6jt) dulu, ~5 bulan dari sekarang — baru pikir 9-12 bulan.
> 5. Kalau dapat proyek sampingan lagi, langsung masukkan ke dana darurat, bukan ke pengeluaran rutin.
>
> ⚠️ Bukan nasihat keuangan/investasi. Angka di atas simulasi dari mutasi + asumsi yang disebut. Soal kripto aku cuma kasih gambaran dampaknya ke anggaran, bukan saran beli/jual — kalau mau pendapat soal itu, konsultasi ke perencana keuangan bersertifikat.

## Balasan utuh — sesi B (5.042 karakter)

> Udah aku cek mutasinya pakai kalkulator keuangan — jangan-jangan ini yang bikin mepet 😅
>
> ## Ringkasan
> Gaji kamu Rp9.500.000/bulan, tapi September kemarin pengeluaran rutin (di luar proyek desain tambahan) tembus Rp12.468.000 — defisit Rp2.968.000, ditambal sama proyek desain Rp1.250.000 dan bunga tabungan, jadi saldo "cuma" turun Rp1.709.800. Biang keroknya: top-up kripto Indodax Rp2.500.000 (26% gaji!) plus e-wallet & jajan lain-lain masuk kelompok "Keinginan" total Rp4.685.500 (49% gaji, idealnya ≤30%). Dengan anggaran baru di bawah, kamu bisa zero-based Rp9.500.000 sambil tetap nabung dana darurat tiap bulan.
>
> > Catatan kecil: kamu bilang tabungan sekarang Rp4.000.000, tapi saldo akhir di mutasi ini Rp2.440.200. Aku pakai angka Rp4.000.000 dari kamu buat hitungan dana darurat di bawah — kalau itu gabungan rekening lain nggak masalah, tapi kalau sama rekening ini, cek lagi ya.
>
> ## Realisasi September vs Anggaran Usulan
>
> | Pos | Kelompok | Realisasi Sept | Usulan baru |
> |---|---|---:|---:|
> | Kontrakan | Wajib | Rp2.000.000 | Rp2.000.000 |
> | Cicilan Motor Adira | Wajib | Rp1.150.000 | Rp1.150.000 |
> | Shopee PayLater (cicilan) | Wajib | Rp650.000 | Rp650.000 |
> | Token PLN | Wajib | Rp350.000 | Rp350.000 |
> | Belanja dapur bulanan | Wajib | Rp1.235.000 | Rp1.235.000 |
> | Pasar sayur | Wajib | Rp265.000 | Rp265.000 |
> | SPP PAUD anak | Wajib | Rp350.000 | Rp350.000 |
> | Pulsa & data | Wajib | Rp150.000 | Rp150.000 |
> | Adm bulanan | Wajib | Rp12.500 | Rp12.500 |
> | Bensin motor | Wajib | Rp120.000 | Rp120.000 |
> | Kiriman ortu | Sosial | Rp1.000.000 | Rp1.000.000 |
> | **Dana darurat (nabung)** | Tabungan | Rp0 | **Rp700.000** |
> | Arisan RT | Tabungan | Rp500.000 | Rp500.000 |
> | Jajan + e-wallet + kripto, dll | Keinginan | Rp4.685.500 | **Rp1.017.500** |
> | **Total** | | **Rp12.468.000** | **Rp9.500.000** |
> | **Selisih vs gaji** | | **-Rp2.968.000 (defisit)** | **Rp0 (pas)** |
>
> Pola yang kepake: **75/10/15** (bukan 50/30/20 standar) karena cicilan+kiriman ortu kamu memang berat — wajar untuk keluarga dengan anak, yang penting tabungan tetap jalan.
>
> Yang paling kerasa harus dipotong: **top-up Indodax (kripto) Rp2.500.000** itu sendirian udah lebih gede dari cicilan motor. Kalau mau tetap "investasi" kripto, ambil dari jatah Keinginan Rp1.017.500 itu aja, jangan dari pos lain — dan itu pun idealnya setelah dana darurat & utang aman dulu (skill ini nggak kasih rekomendasi beli/jual kripto ya, cuma soal porsi anggarannya).
>
> ## Dana Darurat
>
> Status: **menikah + anak** → target **9–12 bulan** pengeluaran pokok.
>
> | Target | Jumlah | Kekurangan (dari Rp4jt) | Lama tercapai @ setoran Rp700rb/bln |
> |---|---:|---:|---:|
> | 9 bulan | Rp65.542.500 | Rp61.542.500 | ~88 bulan (7 th 4 bln) |
> | 12 bulan | Rp87.390.000 | Rp83.390.000 | ~120 bulan (10 th) |
>
> Pengeluaran pokok (dasar hitungan) = Rp7.282.500/bulan:
>
> | Pos pokok | Jumlah |
> |---|---:|
> | Kontrakan | Rp2.000.000 |
> | Cicilan Motor Adira | Rp1.150.000 |
> | Shopee PayLater | Rp650.000 |
> | Token PLN | Rp350.000 |
> | Belanja dapur | Rp1.235.000 |
> | Pasar sayur | Rp265.000 |
> | SPP PAUD anak | Rp350.000 |
> | Pulsa & data | Rp150.000 |
> | Adm bulanan | Rp12.500 |
> | Bensin | Rp120.000 |
> | Kiriman ortu | Rp1.000.000 |
> | **Total** | **Rp7.282.500** |
>
> 7 tahun untuk target penuh itu kejauhan buat dijadiin patokan harian, jadi **fokus dulu ke milestone 1 bulan pokok (~Rp7.282.500)**: dengan saldo Rp4jt + setoran Rp700rb/bulan, itu tercapai dalam **~5 bulan**. Itu udah cukup jadi "bantalan" kalau ada kejadian darurat, sambil nyicil ke target 9 bulan pelan-pelan.
>
> ## Asumsi yang dipakai
> - Kiriman ke ibu Rp1jt/bulan dianggap wajib rutin (masuk pokok dana darurat) — kalau sebenarnya bisa disetop saat darurat, pokok turun jadi Rp6.282.500 dan target 9 bln jadi Rp56,5jt (lebih ringan).
> - Proyek desain Rp1,25jt dianggap pemasukan tidak tetap, **tidak** dimasukkan ke anggaran rutin — sebaiknya langsung ditabung/buat dana darurat kalau ada lagi bulan depan.
> - Top-up e-wallet (Gopay/OVO) & Indodax digabung jadi satu pos "Keinginan" karena cuma pindah dompet, bukan pengeluaran sendiri-sendiri.
> - Dana darurat disimpan terpisah, instrumen likuid (bukan kripto/saham).
>
> ## Langkah minggu ini
> 1. Begitu gajian, langsung pindahkan Rp700.000 ke rekening/dompet terpisah khusus dana darurat — sebelum uang "kelihatan" di saldo utama.
> 2. Setop dulu top-up Indodax rutin; kalau mau tetap jalan, batasi ketat dalam jatah Keinginan Rp1.017.500/bulan (gabung sama jajan & e-wallet).
> 3. Cek slip Shopee PayLater — ada bunga/denda telat atau nggak. Kalau ada, prioritaskan lunasi cepat, jangan dibiarkan jadi cicilan permanen.
> 4. Proyek desain berikutnya: masukkan ke dana darurat dulu, bukan belanja tambahan — ini bisa pangkas 5 bulan jadi lebih cepat.
> 5. Akhir Oktober, bandingkan realisasi vs tabel "Usulan baru" di atas, lihat pos mana yang masih jebol.
>
> ⚠️ Bukan nasihat keuangan/investasi. Angka adalah simulasi dari data mutasi & asumsi di atas. Untuk kripto, aku nggak kasih rekomendasi beli/jual/tahan — itu di luar cakupan skill ini.

## Verifikasi independen penguji (python + `keuangan.py` 1.0.6 dijalankan di salinan)

Dasar: total keluar Rp12.468.000, masuk Rp10.758.200, defisit Rp1.709.800 ✅ (kedua sesi).

**Sesi A**
- Anggaran menjumlah tepat Rp9.500.000 ✅. Pokok = 2.000.000 + 1.150.000 + 650.000 + 1.800.000 + 350.000 + 350.000 + 150.000 + 150.000 + 15.000 + **1.000.000 (kiriman ibu)** = **Rp7.615.000** ✅ (memakai angka anggaran yang dibulatkan: dapur 1,8 jt, bensin 150rb, admin 15rb).
- 9 bln Rp68.535.000 ✅, 12 bln Rp91.380.000 ✅; (68.535.000 − 4 jt)/785.000 = 82,2 → 83 bln (6 th 11 bln) ✅; 87.380.000/785.000 = 111,3 → 112 bln (9 th 4 bln) ✅; milestone 1 bulan 3.615.000/785.000 = 4,6 → 5 bln ✅. Alternatif tanpa kiriman Rp6.615.000 ✅. "Kebocoran" 2,5 jt + 500rb + 800rb + 598rb = Rp4.398.000 = 46,3% gaji ✅. Kebutuhan 80,2%, keinginan 6,3%, tabungan 13,5% ✅.

**Sesi B**
- Realisasi menjumlah Rp12.468.000 ✅, defisit terhadap gaji −Rp2.968.000 ✅, "Keinginan" realisasi Rp4.685.500 (termasuk Indodax 2,5 jt dan Indomaret 287,5rb) ✅; usulan menjumlah Rp9.500.000 ✅.
- Pokok **Rp7.282.500** (tabel pos dimasukkan: realisasi wajib + cicilan + kiriman ortu) ✅ — sama persis dengan contoh uji di catatan revisi 1.0.6. 9 bln Rp65.542.500 ✅, 12 bln Rp87.390.000 ✅; 61.542.500/700.000 = 87,9 → 88 bln (7 th 4 bln) ✅; 83.390.000/700.000 = 119,1 → 120 bln ✅; milestone 3.282.500/700.000 = 4,7 → 5 bln ✅; alternatif tanpa kiriman 6.282.500 → 9 bln Rp56,5 jt ✅.
- Penguji menjalankan `keuangan.py anggaran` dengan pos yang sama: script mencetak tabel "Pos DIMASUKKAN / DIKELUARKAN + alasan" dan menandai pos tanpa label ("Pasar sayur … tanyakan ke pengguna apakah wajib") — perilaku script sesuai catatan revisi.
- Bonus: menandai bahwa tabungan Rp4 jt ≠ saldo akhir mutasi Rp2.440.200 dan meminta cek.

**Konsistensi A vs B:** keduanya memasukkan cicilan PayLater **dan** kiriman ortu, keduanya menyebut alternatif bila kiriman bisa dihentikan. Pokok berbeda Rp332.500 (A 7.615.000 vs B 7.282.500; 4,6%) karena A memakai angka anggaran yang dibulatkan + Indomaret masuk dapur, B memakai realisasi. Target 9 bulan Rp68,5 jt vs Rp65,5 jt — keduanya dalam rentang wajar penguji (±Rp65–68 jt) dan asumsi tertulis. Setoran DD berbeda (785rb vs 700rb) — pilihan anggaran, bukan salah hitung.

## Cacat sisa putaran 1

| Cacat sisa | Hilang? | Bukti |
|---|---|---|
| Kiriman ortu Rp1 jt dikeluarkan dari pokok diam-diam (target kekecilan ±Rp9–11,6 jt) | **ya (2/2 sesi)** | A: *"Pokok dana darurat = kebutuhan wajib + cicilan + kiriman ibu … kalau sebenarnya fleksibel saat darurat, kabari aku, target bisa turun jadi Rp6,6jt pokok."* B: tabel pos pokok berisi *"Kiriman ortu Rp1.000.000"* + *"kalau sebenarnya bisa disetop saat darurat, pokok turun jadi Rp6.282.500"* |
| "Redirect Rp2,5 jt ke dana darurat" bertentangan dengan tabel | **ya** | A: *"Putuskan nominal wajar buat topup Indodax … ini keputusan kamu"*; B: *"batasi ketat dalam jatah Keinginan Rp1.017.500"* — konsisten dengan tabel |
| Frasa "2× Rp2.500.000" ambigu | **ya** | A: *"Topup Indodax (crypto) x2 \| Rp2.500.000"*; B: *"top-up kripto Indodax Rp2.500.000"* |
| Panjang ±4.800 karakter | **tidak** | A 4.777, B 5.042 karakter — masih panjang untuk chat (isi relevan) |

## Regresi

1. **Potongan besar tidak lagi ditandai bertahap (2/2 sesi)** — melanggar SKILL.md langkah 4 (*"potongan > 30% dari realisasi ditandai sebagai target bertahap"*). A: jajan/e-wallet/tunai/Shopee realisasi ±Rp1,9 jt → Rp600rb (−68%) tanpa jembatan bulanan; B: Rp2.185.500 (di luar kripto) → Rp1.017.500 (−53%), juga tanpa tahap. Uji ulang 1.0.5 justru punya tabel jembatan Okt/Nov/Des yang dipuji. Risiko: anggaran terasa mustahil bagi member, lalu ditinggalkan.
2. Sesi A tidak menampilkan tabel pos pokok (hanya kalimat), padahal SKILL.md meminta menyebut pos dimasukkan/dikeluarkan — kalimatnya cukup jelas, minor.

## Nilai

| | Asal | Ulang 1.0.5 | **Ulang ke-2 A** | **Ulang ke-2 B** |
|---|---|---|---|---|
| Skor | 8 | 8 | **8** | **8.5** |

Cacat inti (dasar dana darurat tidak lengkap) **tuntas dan konsisten** di dua sesi, semua angka terverifikasi, transparansi pos pokok baik. Dikurangi karena aturan "potongan bertahap" tidak dijalankan di kedua sesi dan balasan masih panjang.
