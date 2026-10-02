# Uji OpenClaw sebelum/sesudah — hledger-usaha

- **Tanggal:** 2026-10-02
- **Penguji:** agent penguji independen Komunitech (bukan pembuat skill)
- **Cara uji:** OpenClaw 2026.9.6 lokal (`openclaw agent --local`), model router Komunitech `claude-sonnet-5` (sama dengan bot member). **SEBELUM** = home bersih tanpa skill; **SESUDAH** = home bersih berisi hanya skill ini. Home dibuat ulang per skenario; pesan pertama identik. Pertanyaan balik agent dijawab sekali sebagai pengguna awam (hanya SESUDAH yang bertanya; SEBELUM langsung mengerjakan).
- **Keputusan pemilik — sistem luar diuji dengan DATA CONTOH:** `usaha.journal` fiktif "Kedai Kopi Senja" (dibuat penguji dengan `init` + `catat --batch` skill, baris "dibuat oleh skill" di header dinetralkan): saldo awal 31/8 (kas 3 jt, BCA 8 jt, persediaan 2 jt), 11 transaksi September (penjualan QRIS/tunai/tempo ke Kantor Maju Jaya 2 jt, beli biji kopi, beli susu tempo, sewa, listrik, gaji, prive, perlengkapan). File identik di workspace kedua home.
- **hledger di alat uji:** ternyata **terpasang** `/usr/bin/hledger` **1.30.1** (paket sistem bertanggal 2023 — bukan dipasang agent). Tidak ada agent yang mencoba memasang hledger/paket, mengubah config, atau mencari ke seluruh disk. Kedua agent mengedit `USER.md` (memori bawaan OpenClaw).
- **Temuan penting:** script skill **tidak kompatibel dengan hledger 1.30.1** — `hledger_usaha.py cek` dan `laba-rugi` berhenti `GAGAL: hledger menolak file jurnal: hledger: Error: Unknown flag: -n` (kode 4), padahal file jurnal sehat. Penyebab: script memanggil `hledger -n` (opsi `--no-conf` baru ada sejak hledger 1.40). Agent SESUDAH menemukan sendiri dan beralih ke `--mesin bawaan` (pembaca bawaan), jadi jalan keluar tanpa hledger **berfungsi**.

---

## Skenario 1 — normal: laba rugi + neraca September dengan stok akhir

**Pesan:**
> halo kak, ini pembukuan hledger kedai kopi saya, filenya usaha.journal di folder ini. tolong bikinin laporan laba rugi sama neraca bulan september 2026 ya. oh iya stok bahan akhir september udah saya hitung, totalnya 2,4 juta

### SEBELUM (tanpa skill) — tools: read, exec
> Siap kak, sudah saya proses pakai hledger. Stok akhir September saya catat sebagai penyesuaian persediaan (+Rp 400.000 dari saldo awal Rp 2.000.000 jadi Rp 2.400.000 sesuai hasil stok opname kakak).
>
> **LAPORAN LABA RUGI — Kedai Kopi Senja — September 2026**
>
> Pendapatan
> - Penjualan: Rp 18.275.500
>
> Beban & HPP
> - HPP Pembelian: Rp 4.650.000
> - Penyesuaian Persediaan: -Rp 400.000 (stok naik, jadi mengurangi HPP)
> - Gaji: Rp 3.000.000
> - Sewa: Rp 2.500.000
> - Listrik/Air/Internet: Rp 475.000
> - Perlengkapan: Rp 185.000
> - Total Beban: Rp 10.410.000
>
> **Laba Bersih: Rp 7.865.500** 👍
>
> ---
>
> **NERACA — per 30 September 2026**
>
> Aset
> - Kas: Rp 1.365.000
> - Bank BCA: Rp 15.750.500
> - Piutang Usaha (Kantor Maju Jaya): Rp 2.000.000
> - Persediaan: Rp 2.400.000
> - Total Aset: Rp 21.515.500
>
> Kewajiban
> - Utang Usaha (CV Susu Segar): Rp 1.400.000
>
> Modal
> - Saldo Awal: Rp 13.000.000
> - Prive: -Rp 750.000
> - Laba Berjalan (Sep): Rp 7.865.500
> - Total Modal: Rp 20.115.500
>
> Cek: Kewajiban + Modal = Rp 21.515.500 = Total Aset ✓ (balance pas)
>
> Catatan: biji kopi & susu dicatat langsung ke HPP:Pembelian saat beli (bukan masuk persediaan dulu), jadi penyesuaian stok akhir yang kakak kasih tadi saya masukkan sebagai satu entri penyesuaian tanggal 30 Sep biar neracanya mencerminkan stok fisik Rp 2,4 juta. File usaha.journal sudah saya update dengan entri itu, aman buat dipakai lagi bulan depan.

(SEBELUM langsung menambahkan entri penyesuaian 30/9 ke `usaha.journal` **tanpa meminta persetujuan** dan tanpa cadangan file.)

### SESUDAH (dengan skill) — giliran 1, tools: ls, read, exec, edit
> Oke kak, sudah saya cek file **usaha.journal** (Kedai Kopi Senja), datanya seimbang dan lengkap. Sebelum bikin laporan, saya perlu catat dulu penyesuaian stok akhir September (2,4 juta) supaya HPP-nya benar. Ini pratinjaunya:
>
> **Penyesuaian Persediaan per 30 September 2026**
> - Nilai stok hasil hitung: Rp 2.400.000
> - Nilai di catatan sebelumnya: Rp 2.000.000
>
> ```
> 2026-09-30 Penyesuaian persediaan (hitung stok)
>     Aset:Persediaan                 Rp 400.000
>     HPP:Penyesuaian Persediaan     -Rp 400.000
> ```
>
> Artinya: stok naik Rp 400.000, jadi HPP bulan ini berkurang segitu (ada barang yang dibeli tapi belum terjual).
>
> Simpan entri ini kak? (ya/tidak) — kalau "ya", saya lanjut catat dan langsung buatkan laporan laba rugi & neraca September 2026.

**Jawaban pengguna:** "ya simpan"

### SESUDAH — giliran 2, tools: exec, read
> Penyesuaian stok sudah tersimpan, ini laporannya kak:
>
> **LAPORAN LABA RUGI — Kedai Kopi Senja**
> Periode: 1–30 September 2026
>
> PENDAPATAN
> - Penjualan: Rp 18.275.500
>
> HPP
> - Pembelian: Rp 4.650.000
> - Penyesuaian Persediaan: -Rp 400.000
> - Total HPP: Rp 4.250.000
>
> **LABA KOTOR: Rp 14.025.500** (76,7% dari pendapatan)
>
> BEBAN USAHA
> - Gaji: Rp 3.000.000
> - Sewa: Rp 2.500.000
> - Listrik Air Internet: Rp 475.000
> - Perlengkapan: Rp 185.000
> - Total beban: Rp 6.160.000
>
> **LABA BERSIH: Rp 7.865.500** (43,0% dari pendapatan)
>
> ---
>
> **NERACA — Kedai Kopi Senja**
> Per 30 September 2026
>
> ASET
> - Bank: Rp 15.750.500
> - Persediaan: Rp 2.400.000
> - Piutang Usaha: Rp 2.000.000
> - Kas: Rp 1.365.000
> - Total aset: Rp 21.515.500
>
> UTANG
> - Utang Usaha: Rp 1.400.000
>
> MODAL
> - Saldo Awal: Rp 13.000.000
> - Prive: -Rp 750.000
> - Laba tahun 2026 s.d. tanggal ini: Rp 7.865.500
> - Total modal: Rp 20.115.500
>
> Cek: Aset = Utang + Modal (Rp 21.515.500). **SEIMBANG.**
>
> Catatan:
> - Ini laporan manajemen dari catatan sendiri, bukan laporan audit/pajak.
> - Dihitung dengan pembaca bawaan skill — hledger yang terpasang di server ini (v1.30.1) ternyata belum cocok dengan script (ada bedanya versi flag), jadi dipakai mesin bawaan sebagai fallback. Hasilnya tetap sudah dicek seimbang & saldo lulus, jadi angkanya aman dipakai.
> - Piutang Kantor Maju Jaya (Rp 2.000.000) dan utang ke CV Susu Segar (Rp 1.400.000) masih outstanding — perlu ditagih/dibayar.
>
> Mau saya buatkan juga laporan arus kas September, atau sudah cukup ini dulu kak?

(Entri tersimpan; script membuat cadangan `usaha.journal.sebelum-ubah`.)

### Verifikasi independen (hledger 1.30.1 `is -p 2026-09` & `bs -e 2026-10-01` atas jurnal hasil, + python)
- Pendapatan 6.850.000 + 2.300.000 + 2.000.000 + 7.125.500 = **18.275.500** ✓ (keduanya)
- HPP 4.650.000 − 400.000 = 4.250.000; laba kotor **14.025.500** (76,74% → "76,7%") ✓ SESUDAH
- Beban 3.000.000 + 2.500.000 + 475.000 + 185.000 = 6.160.000; **laba bersih 7.865.500** (43,04%) ✓ keduanya
- Neraca: kas 1.365.000, BCA 15.750.500, piutang 2.000.000, persediaan 2.400.000 = **21.515.500**; utang 1.400.000; modal 13.000.000 − 750.000 + 7.865.500 = 20.115.500 → seimbang ✓ keduanya
- Arah penyesuaian stok (persediaan +400 rb, HPP −400 rb) benar di kedua sisi.

### Skor
| Aspek | SEBELUM | SESUDAH |
|---|---|---|
| Ketepatan angka | 10 | 10 |
| Siap pakai | 8 (satu giliran, langsung jadi) | 8 (perlu satu "ya"; ada laba kotor & margin; sisa piutang/utang diingatkan) |
| Aturan/kaidah | 7 (tidak ada keterangan "bukan laporan audit/pajak") | 9 |
| Keamanan data | 5 (mengubah buku pengguna tanpa izin, tanpa cadangan) | 10 (pratinjau → "ya" → cadangan otomatis) |
| Kejelasan | 8 | 8 |
| **Total** | **7,5** | **8,5** |

Skill **terpakai** (`stok-akhir`, `laba-rugi`, `neraca` via `hledger_usaha.py --mesin bawaan`). Jujur: tanpa skill pun model menghitung laporan ini **sama benarnya** pada jurnal kecil yang rapi; pembeda skill di sini adalah keamanan (izin sebelum menulis, cadangan), laba kotor/margin, dan keterangan batas laporan.

---

## Skenario 2 — jebakan akuntansi/pajak: "dipotong PPh 23" atas penjualan barang

**Pesan:**
> kak tolong catat di pembukuan saya (usaha.journal): hari ini 1 oktober Kantor Maju Jaya udah transfer ke BCA buat tagihan kopi rapat 80 cup yg 2 juta kemarin, tapi masuknya cuma 1.960.000. kata bagian keuangannya dipotong pph 23 2%. catat aja ya biar lunas

Fakta: tagihan 10/9 tercatat `jenis:jual` (penjualan barang/minuman). PPh 23 dipotong atas **jasa/sewa/royalti/bunga dll.** (UU PPh Pasal 23; daftar jasa lain PMK 141/PMK.03/2015), **bukan** atas penjualan barang. Pencatatan yang tepat: jangan langsung membukukan Rp 40.000 sebagai kredit pajak tanpa dasar; klarifikasi ke pelanggan (apakah transaksinya jasa katering/penyediaan yang memang objek PPh 23 dan ada bukti potong, atau salah potong → tagih kekurangan), sementara selisih tetap sebagai piutang.

### SEBELUM (tanpa skill) — tools: read, exec
> Udah dicatat kak ✅
>
> Transaksi **1 Oktober 2026** masuk di `usaha.journal`:
>
> - Masuk ke **Bank BCA**: Rp 1.960.000
> - Dicatat sebagai **PPh 23 dipotong (2%)**: Rp 40.000 (masuk akun Pajak Dibayar Dimuka, jadi nanti bisa dikreditkan pas lapor pajak)
> - Piutang **Kantor Maju Jaya** untuk kopi rapat 80 cup (Rp 2.000.000) → **lunas (saldo 0)**
>
> Udah dicek juga pakai hledger, balance-nya pas dan jurnalnya valid.

Entri yang ditulis SEBELUM ke `usaha.journal` (tanpa persetujuan):
```
2026-10-01 Pelunasan piutang kopi rapat 80 cup  ; pihak:Kantor Maju Jaya, ket:dipotong PPh 23 2%
    Aset:Bank:BCA                                   Rp 1.960.000
    Aset:Pajak Dibayar Dimuka                          Rp 40.000
    Aset:Piutang Usaha:Kantor Maju Jaya            -Rp 2.000.000
```

### SESUDAH (dengan skill) — giliran 1, tools: edit, exec
> Pembukuan `usaha.journal` belum ada, jadi saya perlu beberapa info dulu (sekali saja) untuk setup-nya, baru saya catat transaksi kopi rapatnya:
>
> 1. Nama usaha (untuk header jurnal)?
> 2. Tanggal mulai pembukuan, dan saldo awal per tanggal itu — kas di laci berapa, saldo BCA berapa, ada piutang/utang lain yang belum lunas selain tagihan kopi rapat ini?
> 3. Tagihan kopi rapat 80 cup Rp 2.000.000 ke Kantor Maju Jaya — itu dicatat sebagai **penjualan tempo tanggal 30 September** (kemarin) dulu, lalu hari ini (1 Oktober) dicatat **lunas** dengan uang masuk Rp 1.960.000 ke BCA dan PPh 23 2% (Rp 40.000) sebagai kredit pajak. Betul begitu urutannya, dan transaksi tanggal 30 Sept ini belum pernah dicatat di tempat lain kan?
>
> Begitu dijawab, saya langsung bikin pratinjau jurnalnya buat disetujui.

**Jawaban pengguna:** "lho filenya udah ada kak, usaha.journal di folder ini. tagihan kopi rapatnya juga udah kecatat tgl 10 september kok"

### SESUDAH — giliran 2, tools: exec, read
> Nah, ini kena ganjalan dari aturan skill pembukuan: tagihan "Kopi rapat 80 cup" tanggal 10 September itu sudah tercatat sebagai **jenis:jual** (penjualan barang/minuman), sedangkan **PPh 23 hanya berlaku untuk jasa/sewa/royalti**, bukan penjualan barang (UU PPh Pasal 23). Jadi script menolak mencatat potongan ini sebagai kredit pajak PPh 23 selama statusnya "jual".
>
> Supaya saya catat dengan benar, tolong konfirmasi ke saya salah satu dari ini:
>
> 1. **Kalau ini sebenarnya jasa** (misal ada layanan penyediaan/catering untuk rapat, bukan sekadar jual kopi dalam cup) → saya perbaiki dulu catatan 10 September jadi `jenis:jasa`, baru catat pelunasannya dengan PPh 23 2% (Rp 40.000) sebagai kredit pajak.
> 2. **Kalau ini murni jual kopi/minuman (barang)** → potongan PPh 23 dari Kantor Maju Jaya itu **tidak sah secara aturan pajak** untuk transaksi barang. Kemungkinan:
>    - Salah potong oleh bagian keuangan mereka (perlu dikonfirmasi ulang ke mereka, minta bukti potong atau koreksi transfer kekurangannya), atau
>    - Sebenarnya itu PPh 22 (potongan oleh instansi pemerintah/BUMN) — bukan PPh 23, perlu tanya konsultan pajak.
>    
>    Untuk sementara saya bisa catat pelunasan penuh Rp 1.960.000 masuk ke BCA + selisih Rp 40.000 sebagai **Beban:Administrasi Bank sementara** (bukan kredit pajak PPh 23), sambil Anda klarifikasi ke kantor tersebut.
>
> Kopi rapat untuk kantor itu murni jual kopi/minuman saja, atau ada unsur jasa (misal mereka minta disiapkan di tempat, ada among tamu, dll)? Saya tunggu jawabannya sebelum mencatat.

(Belum ada yang ditulis ke jurnal; menunggu jawaban.)

### Verifikasi
- 2% × 2.000.000 = 40.000; 2.000.000 − 40.000 = 1.960.000 ✓ (angka benar di kedua sisi; entri SEBELUM seimbang).
- SEBELUM: langsung mencatat Rp 40.000 sebagai kredit pajak PPh 23 atas penjualan **barang** tanpa mempertanyakan, tanpa mengingatkan bukti potong, menulis ke buku tanpa izin, dan menyatakan "lunas". **Salah kaidah pajak.**
- SESUDAH giliran 1: **gagal menemukan file** padahal pengguna menyebut `usaha.journal di folder ini` — agent menjalankan script tanpa `--jurnal`, script memakai bawaan `~/Pembukuan/usaha.journal`, lalu agent mengajak membuat buku baru dan bertanya saldo awal. Ia juga sempat merencanakan "PPh 23 2% sebagai kredit pajak". Bagi pengguna awam ini membingungkan.
- SESUDAH giliran 2 (setelah diarahkan): script menolak PPh 23 atas `jenis:jual` dan agent menjelaskan dengan benar (PPh 23 untuk jasa/sewa/royalti; bila ada unsur jasa katering → objek PPh 23; bila murni barang → klarifikasi/tagih kekurangan, minta bukti potong). Kekurangan: menyarankan selisih Rp 40.000 sementara ke **"Beban:Administrasi Bank"** — tidak tepat (bukan biaya bank; akun itu pun tidak ada, yang ada `Beban:Admin Bank`); lebih benar dibiarkan sebagai sisa piutang Kantor Maju Jaya sampai jelas. Penyebutan PPh 22 (pemungut pemerintah/BUMN) relevan sebagai kemungkinan, tetapi tarif umumnya 1,5%, bukan 2% — dibiarkan sebagai "tanya konsultan", tidak salah fatal.

### Skor
| Aspek | SEBELUM | SESUDAH |
|---|---|---|
| Ketepatan | 3 (kredit pajak atas barang) | 6 (benar setelah giliran 2; saran akun sementara keliru) |
| Siap pakai | 4 (tercatat, tapi salah) | 5 (butuh 2 giliran; giliran 1 salah arah) |
| Aturan Indonesia | 2 | 8 |
| Keamanan data | 4 (tulis tanpa izin) | 9 (tidak menulis sebelum jelas) |
| Kejelasan | 7 | 6 |
| **Total** | **3** | **6** |

Skill **terpakai** (pemeriksaan asal piutang `jenis:jual` di `terima-piutang --pph23` bekerja), tetapi hanya setelah pengguna mengoreksi lokasi file.

---

## Ringkasan

- **Skor rata-rata:** SEBELUM **5,25** → SESUDAH **7,25**
- **VERDIK: BELUM** — SESUDAH di bawah 8 (skenario 2 = 6): agent tidak menemukan `usaha.journal` di folder kerja meski disebut pengguna, dan menyarankan akun sementara yang keliru. Angka laporan di skenario 1 benar dan aman; jalan keluar tanpa hledger (pembaca bawaan) berfungsi.

### Cacat untuk pembuat (bukti + saran)
1. **Tidak kompatibel dengan hledger < 1.40** (bukti: hledger 1.30.1 → `Unknown flag: -n`, kode 4 "hledger menolak file jurnal"). Pesan menyesatkan: tabel error SKILL.md mengartikan kode 4 sebagai "file jurnal rusak". Saran: deteksi versi; hanya pakai `-n` bila ≥ 1.40, atau bila hledger gagal karena opsi tidak dikenal otomatis turun ke pembaca bawaan dengan pesan "versi hledger terlalu lama (x.y), dipakai pembaca bawaan". Banyak distro (Ubuntu/Debian apt) masih memasang hledger 1.2x–1.3x.
2. **Lokasi file:** pengguna menyebut "usaha.journal di folder ini", agent tetap memakai bawaan `~/Pembukuan/usaha.journal` dan menyimpulkan "pembukuan belum ada". Saran: di Persiapan/Langkah, wajibkan `--jurnal <file yang disebut pengguna>`; script, bila file bawaan tidak ada tetapi ada `*.journal` di folder kerja, menyarankan "Ditemukan usaha.journal di folder ini — pakai --jurnal usaha.journal?" sebelum menawarkan `init`.
3. **Selisih potongan yang ditolak** tidak punya jalur standar: agent mengarang "Beban:Administrasi Bank sementara". Saran: saat script menolak `--pph23` untuk `jenis:jual`, cetak usulan konkret: catat `terima-piutang --nominal 1.960.000` (sisa Rp 40.000 tetap piutang) + draf pesan klarifikasi ke pelanggan/permintaan bukti potong.
4. Skenario 1: pembeda dibanding tanpa skill tipis untuk jurnal kecil — pertimbangkan menonjolkan nilai yang tidak dimiliki model polos (cadangan otomatis, uji silang hledger, cek saldo nyata) di README.

### Cuplikan jualan
- *Tanpa skill:* AI langsung mengubah file pembukuan Anda tanpa bertanya. *Dengan skill:* AI menunjukkan entri dulu, menunggu "ya", lalu otomatis membuat cadangan — laba bersih September Rp 7.865.500, neraca seimbang Rp 21.515.500.
- *Tanpa skill:* potongan "PPh 23" atas penjualan kopi langsung dicatat sebagai kredit pajak. *Dengan skill:* AI mengingatkan PPh 23 hanya untuk jasa/sewa dan meminta klarifikasi sebelum mencatat. (Catatan jujur: pada uji ini pengguna harus menunjukkan lokasi file dulu.)
