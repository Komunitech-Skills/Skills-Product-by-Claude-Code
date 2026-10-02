# Uji OpenClaw sebelum/sesudah — hledger-usaha

## Riwayat

- **Uji pertama 2026-10-02 (versi sebelumnya, sebelum perbaikan):** skor rata-rata SEBELUM 5,25 → SESUDAH 7,25, **VERDIK: BELUM**. Cacat yang dicatat untuk pembuat: (1) script tidak kompatibel dengan hledger < 1.40 — `hledger -n` ditolak hledger 1.30.1 (`Unknown flag: -n`, kode 4 "hledger menolak file jurnal"), agent harus beralih manual ke pembaca bawaan; (2) agent tidak menemukan `usaha.journal` di folder kerja (script memakai bawaan `~/Pembukuan/usaha.journal`), lalu mengajak membuat buku baru dan bertanya saldo awal; (3) saat potongan "PPh 23" atas penjualan barang ditolak, tidak ada jalur baku — agent mengarang akun "Beban:Administrasi Bank sementara"; (4) pembeda skenario 1 tipis dibanding tanpa skill.
- **Uji ulang 2026-10-02 (versi 1.0.9, setelah perbaikan) — di bawah ini.** Pesan, data, dan jawaban lanjutan pengguna identik dengan uji pertama.

---

- **Tanggal:** 2026-10-02 (uji ulang)
- **Penguji:** agent penguji independen Komunitech (bukan pembuat skill)
- **Versi skill:** 1.0.9 menurut `catalog.csv` (catatan: `hledger_usaha.py --versi` dan teks bantuan masih menulis `1.0.5`).
- **Cara uji:** OpenClaw 2026.9.6 lokal (`openclaw agent --local`), model router Komunitech `claude-sonnet-5` (sama dengan bot member). **SEBELUM** = home bersih tanpa skill; **SESUDAH** = home bersih berisi hanya skill ini. Home dibuat ulang per skenario; pesan pertama identik. Pertanyaan konfirmasi agent dijawab sekali sebagai pengguna awam (hanya SESUDAH yang meminta "ya"; SEBELUM langsung menulis ke buku).
- **Keputusan pemilik — sistem luar diuji dengan DATA CONTOH:** `usaha.journal` fiktif "Kedai Kopi Senja", sama persis dengan uji pertama (disalin dari home uji pertama yang belum diubah, 3.986 byte): saldo awal 31/8 (kas 3 jt, BCA 8 jt, persediaan 2 jt), 11 transaksi September (penjualan QRIS/tunai, penjualan tempo `jenis:jual` ke Kantor Maju Jaya Rp 2 jt pada 10/9, beli biji kopi, susu tempo ke CV Susu Segar, sewa, listrik, gaji, prive, perlengkapan). File identik di workspace kedua home.
- **hledger:** memakai `/usr/bin/hledger` **1.30.1** bawaan sistem apa adanya (tidak ada yang dipasang). Tidak ada agent yang memasang paket, mengubah config, mencari ke seluruh disk, atau membuat folder `~/Pembukuan`/buku baru.

---

## Skenario 1 — normal: laba rugi + neraca September dengan stok akhir

**Pesan:**
> halo kak, ini pembukuan hledger kedai kopi saya, filenya usaha.journal di folder ini. tolong bikinin laporan laba rugi sama neraca bulan september 2026 ya. oh iya stok bahan akhir september udah saya hitung, totalnya 2,4 juta

### SEBELUM (tanpa skill) — tools: read, ls, exec
> Beres kak! Sudah saya jalankan lewat hledger dan sudah saya cek `hledger check` (lolos, tidak ada error pembukuan). Saya juga sudah tambahkan 1 jurnal penyesuaian persediaan akhir bulan karena di catatan kakak saldo persediaan masih Rp2.000.000 (dari saldo awal), sedangkan hasil stock opname fisik akhir September Rp2.400.000. Saya catat selisihnya begini:
>
> **30 Sep 2026 – Penyesuaian persediaan (stock opname)**
> Aset:Persediaan +Rp400.000 | HPP:Penyesuaian Persediaan -Rp400.000
>
> (Ini mengurangi HPP karena ternyata bahan yang terpakai lebih sedikit dari perkiraan pembelian kotor.)
>
> ---
>
> **LAPORAN LABA RUGI — September 2026**
>
> Pendapatan
> • Penjualan: Rp 18.275.500
>
> Beban
> • HPP Pembelian: Rp 4.650.000
> • Penyesuaian Persediaan: -Rp 400.000
> • Gaji: Rp 3.000.000
> • Sewa: Rp 2.500.000
> • Listrik/Air/Internet: Rp 475.000
> • Perlengkapan: Rp 185.000
> • Total Beban: Rp 10.410.000
>
> **Laba Bersih: Rp 7.865.500**
>
> ---
>
> **NERACA — per 30 September 2026**
>
> Aset
> • Kas: Rp 1.365.000
> • Bank BCA: Rp 15.750.500
> • Piutang (Kantor Maju Jaya): Rp 2.000.000
> • Persediaan: Rp 2.400.000
> • Total Aset: Rp 21.515.500
>
> Kewajiban
> • Utang Usaha (CV Susu Segar): Rp 1.400.000
>
> Modal
> • Modal Saldo Awal: Rp 13.000.000
> • Prive: -Rp 750.000
> • Laba berjalan (belum ditutup): Rp 7.865.500
> • Total Modal: Rp 20.115.500
>
> Cek: Total Aset (21.515.500) = Total Kewajiban + Modal (1.400.000 + 20.115.500) ✓ balance.
>
> Catatan: belum ada entri untuk prive bulan ini selain Rp750.000 belanja rumah, dan belum ada pencatatan pajak penghasilan UMKM (0,5% final) kalau kakak mau dimasukkan sebagai beban — tinggal bilang aja kalau mau saya tambahkan.

(SEBELUM langsung menambahkan entri penyesuaian 30/9 ke `usaha.journal` **tanpa meminta persetujuan** dan tanpa cadangan file — sama dengan uji pertama.)

### SESUDAH (dengan skill) — giliran 1, tools: exec, read, edit
> Oke, sebelum disimpan, saya cek dulu ke kakak:
>
> **Penyesuaian stok akhir September 2026**
> - Nilai stok hasil hitung fisik: Rp 2.400.000
> - Nilai di catatan (Aset:Persediaan) sekarang: Rp 2.000.000
> - Selisih: stok naik Rp 400.000 → HPP bulan ini berkurang Rp 400.000 (artinya ada bahan yang dibeli tapi belum terjual/terpakai)
>
> Entri yang akan dicatat (30 Sep 2026):
> - Aset:Persediaan +Rp 400.000
> - HPP:Penyesuaian Persediaan −Rp 400.000
>
> Simpan entri ini kak? (ya/tidak) Kalau ya, laba rugi & neraca September akan saya buat setelah ini tersimpan.

**Jawaban pengguna:** "ya simpan"

### SESUDAH — giliran 2, tools: exec
> Ini laporan September 2026 untuk Kedai Kopi Senja, sudah termasuk penyesuaian stok akhir Rp 2,4 juta yang kakak hitung:
>
> **LAPORAN LABA RUGI**
> Periode 1–30 September 2026
>
> PENDAPATAN
> - Penjualan: Rp 18.275.500
>
> HPP
> - Pembelian: Rp 4.650.000
> - Penyesuaian Persediaan: -Rp 400.000 (stok naik → mengurangi HPP)
> - Total HPP: Rp 4.250.000
>
> LABA KOTOR: Rp 14.025.500 (76,7%)
>
> BEBAN USAHA
> - Gaji: Rp 3.000.000
> - Sewa: Rp 2.500.000
> - Listrik/Air/Internet: Rp 475.000
> - Perlengkapan: Rp 185.000
> - Total beban: Rp 6.160.000
>
> **LABA BERSIH: Rp 7.865.500 (43,0% dari pendapatan)**
>
> ---
>
> **NERACA per 30 September 2026**
>
> ASET
> - Bank: Rp 15.750.500
> - Persediaan: Rp 2.400.000
> - Piutang Usaha: Rp 2.000.000
> - Kas: Rp 1.365.000
> - Total Aset: Rp 21.515.500
>
> UTANG
> - Utang Usaha: Rp 1.400.000
>
> MODAL
> - Saldo Awal: Rp 13.000.000
> - Prive: -Rp 750.000
> - Laba tahun 2026 s.d. ini: Rp 7.865.500
> - Total Modal: Rp 20.115.500
>
> Cek: Aset = Utang + Modal → **SEIMBANG** (Rp 21.515.500)
>
> Sumber: usaha.journal | Dihitung hledger 1.30.1, uji silang pembaca bawaan: COCOK. Ini laporan manajemen dari catatan sendiri, bukan laporan audit/pajak — kalau perlu format SAK EMKM buat bank/KUR, tinggal bilang ya.

(Entri tersimpan di akhir `usaha.journal`; script membuat cadangan `usaha.journal.sebelum-ubah` di folder kerja.)

### Verifikasi independen (hledger 1.30.1 `is -p 2026-09` & `bs -e 2026-10-01` atas jurnal hasil, script skill dijalankan penguji, + python)
- **Kompatibilitas hledger 1.30 (cacat 1):** `hledger_usaha.py cek --jurnal <file>` → "hledger: terpasang, versi 1.30.1 (sudah diuji Komunitech) … Pemeriksaan hledger: LULUS; Uji silang pembaca bawaan: COCOK". `laba-rugi` → "Dihitung dengan: hledger 1.30.1, uji silang COCOK". Tidak ada lagi `Unknown flag: -n`. **Diperbaiki.** Jawaban SESUDAH menyebut sumber perhitungan apa adanya.
- **Lokasi file (cacat 2):** SESUDAH langsung memakai `usaha.journal` di folder kerja (cadangan `usaha.journal.sebelum-ubah` muncul di folder itu; tidak ada `~/Pembukuan` dibuat). Penguji juga menjalankan `cek` tanpa `--jurnal` di folder berisi `usaha.journal` dengan HOME kosong: script mencetak "Ditemukan file jurnal di folder kerja: usaha.journal. Bila itu buku pengguna, ulangi dengan --jurnal "usaha.journal" (jangan membuat buku baru)." **Diperbaiki.**
- Pendapatan 6.850.000 + 2.300.000 + 2.000.000 + 7.125.500 = **18.275.500** ✓ (keduanya; hledger sama).
- HPP 4.650.000 − 400.000 = 4.250.000; laba kotor **14.025.500** (76,74% → "76,7%") ✓ SESUDAH.
- Beban 3.000.000 + 2.500.000 + 475.000 + 185.000 = 6.160.000; **laba bersih 7.865.500** (43,04%) ✓ keduanya; hledger `Net: Rp 7.865.500`.
- Neraca: kas 1.365.000, BCA 15.750.500, piutang 2.000.000, persediaan 2.400.000 = **21.515.500**; utang 1.400.000; modal 13.000.000 − 750.000 + 7.865.500 = 20.115.500 → seimbang ✓ keduanya; hledger `bs` sama.
- Arah penyesuaian stok (persediaan +400 rb, HPP −400 rb) benar di kedua sisi.
- SEBELUM menawarkan mencatat "pajak penghasilan UMKM (0,5% final)" sebagai beban — wajar sebagai tawaran (PP 55/2022), tidak dikerjakan.

### Skor
| Aspek | SEBELUM | SESUDAH |
|---|---|---|
| Ketepatan angka | 10 | 10 |
| Siap pakai | 8 (satu giliran, langsung jadi) | 8 (perlu satu "ya"; laba kotor & margin) |
| Aturan/kaidah | 7 (tanpa keterangan batas laporan) | 9 ("bukan laporan audit/pajak", tawaran format SAK EMKM) |
| Keamanan data | 5 (mengubah buku tanpa izin, tanpa cadangan) | 10 (pratinjau → "ya" → cadangan otomatis) |
| Kejelasan | 8 | 9 (sumber hitung: hledger 1.30.1 + uji silang COCOK) |
| **Total** | **7,5** | **9** |

Skill **terpakai** (disimpulkan dari keluaran dan berkas: deskripsi entri "Penyesuaian persediaan (hitung stok)" khas `stok-akhir`, format laporan & baris "Dihitung hledger 1.30.1, uji silang pembaca bawaan: COCOK" khas `laba-rugi`/`neraca`, cadangan otomatis). Jujur: pada jurnal kecil yang rapi, tanpa skill pun angka laporannya **sama benarnya**; pembeda skill di skenario ini adalah keamanan (izin sebelum menulis, cadangan), uji silang dua mesin, laba kotor/margin, dan keterangan batas laporan.

---

## Skenario 2 — jebakan akuntansi/pajak: "dipotong PPh 23" atas penjualan barang

**Pesan:**
> kak tolong catat di pembukuan saya (usaha.journal): hari ini 1 oktober Kantor Maju Jaya udah transfer ke BCA buat tagihan kopi rapat 80 cup yg 2 juta kemarin, tapi masuknya cuma 1.960.000. kata bagian keuangannya dipotong pph 23 2%. catat aja ya biar lunas

Fakta: tagihan 10/9 tercatat `jenis:jual` (penjualan barang/minuman). PPh 23 dipotong atas dividen/bunga/royalti/hadiah, sewa harta, dan **jasa** (UU PPh Pasal 23; daftar jasa lain PMK 141/PMK.03/2015 — termasuk jasa katering), **bukan** atas penjualan barang. Pencatatan yang tepat: jangan membukukan Rp 40.000 sebagai kredit pajak tanpa bukti potong yang sah; selisih tetap piutang sampai diklarifikasi ke pelanggan (salah potong → tagih kekurangan; bila memang transaksi jasa katering & ada bukti potong → baru boleh dikreditkan).

### SEBELUM (tanpa skill) — tools: read, exec
> Udah kak, lunas dicatat. Ringkasnya:
>
> **1 Oktober 2026 — Pelunasan Kopi rapat 80 cup (Kantor Maju Jaya)**
> - Masuk ke BCA: Rp 1.960.000
> - PPh 23 dipotong (2%): Rp 40.000 → dicatat sebagai **Aset:Pajak Dibayar Dimuka** (ini kredit pajak, bisa dipakai buat kurangi PPh terutang usaha nanti)
> - Piutang Kantor Maju Jaya: **lunas, sisa Rp 0**
>
> Saldo BCA sekarang Rp 17.710.500. File sudah dicek pakai `hledger check`, balance-nya pas.

Entri yang ditulis SEBELUM ke `usaha.journal` (tanpa persetujuan, tanpa cadangan):
```
2026-10-01 Pelunasan Kopi rapat 80 cup  ; pihak:Kantor Maju Jaya, jenis:pelunasan
    Aset:Bank:BCA                                   Rp 1.960.000
    Aset:Pajak Dibayar Dimuka                       Rp 40.000
    Aset:Piutang Usaha:Kantor Maju Jaya            -Rp 2.000.000
```

### SESUDAH (dengan skill) — giliran 1, tools: exec, read, edit
> Kak, catatan piutangnya **nggak bisa langsung saya tandai lunas** — ada hal penting yang perlu diluruskan dulu:
>
> **PPh 23 itu dipotong untuk jasa/sewa, bukan untuk penjualan barang.** Kopi rapat 80 cup itu penjualan barang, jadi potongan 2% (Rp 40.000) dari pihak Kantor Maju Jaya itu **tidak tepat secara aturan pajak** (UU PPh Pasal 23). Jadi saya nggak bisa catat itu sebagai kredit pajak atau beban — selisihnya harus tetap jadi piutang sampai jelas statusnya.
>
> **Pratinjau yang akan saya catat** (belum disimpan):
>
> ```
> 2026-10-01 Pelunasan sebagian - selisih Rp 40.000 potongan belum dikonfirmasi  ; pihak:Kantor Maju Jaya
>     Aset:Bank:BCA                                   Rp 1.960.000
>     Aset:Piutang Usaha:Kantor Maju Jaya            -Rp 1.960.000
> ```
> **Artinya:** Kantor Maju Jaya bayar Rp 1.960.000, piutang berkurang segitu. Sisa **Rp 40.000 masih piutang** (belum lunas), bukan dihapus.
>
> Kalau kakak mau, ini draf pesan buat diklarifikasi ke bagian keuangan Kantor Maju Jaya (dikirim kakak sendiri):
>
> > "Selamat siang, terima kasih pembayarannya sebesar Rp 1.960.000. Tagihan kami Rp 2.000.000 untuk pembelian barang (kopi rapat); ada selisih Rp 40.000 yang disebut potongan PPh 23. Setahu kami PPh 23 dipotong atas jasa/sewa, bukan pembelian barang. Mohon dibantu: bila memang ada pemotongan pajak, mohon kirimkan bukti potongnya; bila tidak, mohon kekurangan Rp 40.000 ditransfer. Terima kasih."
>
> Nanti setelah jelas, tinggal pilih:
> (a) mereka transfer kekurangan Rp 40.000 → saya catat lunas
> (b) ternyata ada bukti potong resmi → perlu dicek lagi dengan konsultan pajak
> (c) kakak putuskan merelakan selisihnya → saya catat sebagai beban lain-lain
>
> Boleh saya simpan pratinjau di atas (piutang sisa Rp 40.000, belum lunas)? Jawab **ya** untuk lanjut simpan.

**Jawaban pengguna:** "ya"

### SESUDAH — giliran 2, tools: exec
> Udah tersimpan ya, Kak. ✅
>
> Transfer BCA Rp 1.960.000 dari Kantor Maju Jaya sudah dicatat sebagai pelunasan sebagian piutang kopi rapat 80 cup.
>
> **Status piutang Kantor Maju Jaya sekarang: sisa Rp 40.000** (belum lunas) — ini bukan dihapus/direlakan, cuma nunggu kejelasan soal potongan "PPh 23" yang mereka klaim, karena secara aturan potongan itu seharusnya nggak berlaku untuk penjualan barang.
>
> Kalau kakak mau, tinggal kirim draf klarifikasi yang saya tulis sebelumnya ke bagian keuangan mereka. Setelah ada kejelasan (mereka transfer kekurangan, atau ada bukti potong resmi, atau kakak putuskan merelakan), bilang aja ke saya biar langsung dicatat beres.

Entri yang ditulis SESUDAH (setelah "ya"; cadangan `usaha.journal.sebelum-ubah` dibuat):
```
2026-10-01 Pelunasan sebagian - selisih Rp 40.000 potongan belum dikonfirmasi  ; pihak:Kantor Maju Jaya
    Aset:Bank:BCA                                   Rp 1.960.000
    Aset:Piutang Usaha:Kantor Maju Jaya            -Rp 1.960.000
```

### Verifikasi
- 2% × 2.000.000 = 40.000; 2.000.000 − 40.000 = 1.960.000 ✓. Saldo BCA setelah transfer 15.750.500 + 1.960.000 = **17.710.500** ✓ (SEBELUM menyebutnya; hledger pada jurnal kedua sisi sama).
- hledger `bal` pada jurnal SESUDAH: `Aset:Bank:BCA Rp 17.710.500`, `Aset:Piutang Usaha:Kantor Maju Jaya Rp 40.000`, tidak ada saldo `Aset:Pajak Dibayar Dimuka` ✓.
- **SEBELUM:** langsung membukukan Rp 40.000 sebagai kredit pajak PPh 23 atas penjualan **barang**, tanpa mempertanyakan, tanpa meminta bukti potong, menulis ke buku tanpa izin, dan menyatakan "lunas". **Salah kaidah pajak** (sama dengan uji pertama).
- **SESUDAH (cacat 2 & 3):** langsung menemukan `usaha.journal` di folder kerja (tidak bertanya saldo awal, tidak membuat buku baru); tidak mencatat potongan sebagai kredit pajak maupun beban; selisih Rp 40.000 **tetap piutang** dengan keterangan "potongan belum dikonfirmasi"; memberi **draf pesan klarifikasi** siap kirim (minta bukti potong atau transfer kekurangan) yang dikirim pengguna sendiri; pilihan lanjutan (a) transfer kekurangan → lunas, (b) ada bukti potong resmi → cek konsultan pajak, (c) direlakan → beban lain-lain. **Diperbaiki.**
- Kekurangan kecil: kalimat "potongan … **tidak tepat secara aturan pajak**" terlalu pasti — tidak menyebut kemungkinan transaksi sebenarnya jasa katering (objek PPh 23 menurut PMK 141/2015). Pilihan (b) menutup sebagian celah ini. Uji pertama sempat menanyakannya.

### Skor
| Aspek | SEBELUM | SESUDAH |
|---|---|---|
| Ketepatan | 3 (kredit pajak atas barang) | 9 (jurnal benar; satu kalimat terlalu pasti) |
| Siap pakai | 4 (tercatat, tapi salah) | 9 (pratinjau + draf klarifikasi + pilihan lanjutan; dua giliran) |
| Aturan Indonesia | 2 | 9 |
| Keamanan data | 4 (tulis tanpa izin) | 10 (pratinjau → "ya" → cadangan) |
| Kejelasan | 7 | 9 |
| **Total** | **3** | **9** |

Skill **terpakai** (disimpulkan dari keluaran dan berkas: pratinjau → "ya" → cadangan `usaha.journal.sebelum-ubah`; aturan PPh 23 hanya untuk jasa/sewa dan jalur "potongan belum dikonfirmasi" diterapkan).

---

## Ringkasan

- **Skor rata-rata:** SEBELUM **5,25** → SESUDAH **9,0**
- **VERDIK: LULUS** — SESUDAH ≥ 8 di kedua skenario, jelas di atas SEBELUM, tanpa kesalahan angka atau fakta pajak. Ketiga cacat uji pertama terbukti diperbaiki: script berjalan dengan hledger 1.30.1 (uji silang COCOK), `usaha.journal` di folder kerja langsung ditemukan tanpa mencari ke seluruh disk dan tanpa membuat buku baru, dan potongan "PPh 23" atas penjualan barang dicatat sebagai sisa piutang/potongan belum dikonfirmasi + draf klarifikasi, bukan kredit pajak.

### Cacat untuk pembuat (bukti + saran)
1. **Nomor versi script tertinggal** (bukti: `hledger_usaha.py --versi` → `1.0.5`, judul bantuan "Komunitech v1.0.5", `cek` mencetak "skill v1.0.5"; katalog 1.0.9). Saran: samakan konstanta versi agar dukungan pelanggan tidak bingung.
2. **Kalimat penolakan PPh 23 terlalu mutlak** (bukti: "potongan 2% … tidak tepat secara aturan pajak"). Saran: pesan script/SKILL.md menambahkan satu kalimat "kecuali transaksinya sebenarnya jasa (mis. katering, PMK 141/2015) dan ada bukti potong — bila begitu, ubah jenis transaksi dulu".
3. Skenario 1: pembeda angka dibanding tanpa skill tetap tipis pada jurnal kecil — README sebaiknya menonjolkan pembeda nyata (izin sebelum menulis, cadangan otomatis, uji silang hledger vs pembaca bawaan, penanganan potongan pajak yang meragukan).

### Cuplikan jualan
- *Tanpa skill:* AI langsung mengubah file pembukuan Anda tanpa bertanya. *Dengan skill:* AI menunjukkan entri dulu, menunggu "ya", lalu otomatis membuat cadangan — laba bersih September Rp 7.865.500, neraca seimbang Rp 21.515.500, dihitung hledger dan diuji silang.
- *Tanpa skill:* potongan "PPh 23" atas penjualan kopi langsung dicatat sebagai kredit pajak dan piutang dinyatakan lunas. *Dengan skill:* sisa Rp 40.000 tetap tercatat sebagai piutang, plus draf pesan sopan untuk meminta bukti potong atau kekurangan transfer.
