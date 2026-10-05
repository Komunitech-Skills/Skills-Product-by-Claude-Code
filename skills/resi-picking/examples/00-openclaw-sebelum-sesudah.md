# Uji SEBELUM/SESUDAH di OpenClaw asli — resi-picking

**Tanggal:** 2026-10-01 · **Penguji:** agent penguji independen (bukan pembuat skill)

## Cara uji
- OpenClaw **2026.9.6** dijalankan lokal (`openclaw agent --local`, tanpa gateway/Telegram), model router Komunitech **claude-sonnet-5** — sama dengan bot member.
- **SEBELUM** = home OpenClaw bersih tanpa skill ini (`k-resi-picking`); **SESUDAH** = home bersih berisi hanya skill ini (`s-resi-picking`). Home dibuat ulang sebelum setiap skenario.
- Pesan pengguna identik di kedua sisi, gaya awam WA/Telegram. File data fiktif identik disalin ke kedua home.
- Angka diverifikasi independen dengan Python oleh penguji; aturan Indonesia dicek terhadap teks aturan.
- **Catatan kontaminasi:** percobaan SEBELUM skenario 1 yang pertama (dijalankan bersamaan dengan SESUDAH) **tidak sah**: agent tanpa skill menelusuri folder lain di disk, menemukan `scripts/resi.py` milik skill ini, lalu menjalankannya (file hasilnya identik byte-per-byte dengan SESUDAH, ada jejak `encoding utf-8-sig` khas script). SEBELUM diulang sendirian dengan home bersih; yang dicatat di bawah adalah ulangan yang bersih (agent menyusun sendiri, tidak memakai script).

## Skenario 1 — Normal: picking list + urutan resi dari ekspor Shopee + lokasi rak

**Data uji:** `pesanan-shopee.csv` fiktif (12 baris, 9 pesanan, 1 berstatus Batal, 2 catatan pembeli, dua kolom mirip SKU: `SKU Induk` & `Nomor Referensi SKU`) + `lokasi-rak.csv` (6 SKU di rak A1/A2/B1/C3).

**Pesan pengguna (identik):**

````text
Kak, ini file pesanan shopee hari ini pesanan-shopee.csv sama lokasi rak lokasi-rak.csv. Tolong bikinin daftar ambil barang buat anak gudang sama urutan tempel resi per kurir ya, biar ga ketuker
````

### Balasan SEBELUM (tanpa skill) — tools: ls, read

````text
Siap kak, udah aku susun dari kedua file. Catatan: pesanan **2409301ABC03 aku skip** karena statusnya "Batal" — jangan ikut dipicking/ditempel resi.

## 📦 Daftar Ambil Barang (urut rak biar ga bolak-balik)

**Rak A1**
- Kaos Hitam M (KAOS-HTM-M) — 3 pcs
- Kaos Hitam L (KAOS-HTM-L) — 4 pcs

**Rak A2**
- Kaos Putih L (KAOS-PTH-L) — 6 pcs

**Rak B1**
- Topi Navy (TOPI-NVY) — 3 pcs
- Topi Hitam (TOPI-HTM) — 1 pcs

**Rak C3**
- Hoodie Abu XL (HOOD-ABU-XL) — 2 pcs

Total 19 pcs buat 8 pesanan aktif.

## 🧾 Checklist per Pesanan (buat cross-check pas packing)
- **ABC01** (SPX): Kaos Hitam M x2 [A1] + Topi Navy x1 [B1]
- **ABC02** (J&T): Kaos Putih L x3 [A2] — ⚠️ *bungkus kado*
- **ABC04** (JNE): Hoodie Abu XL x1 [C3]
- **ABC05** (SPX): Kaos Hitam M x1 [A1] + Kaos Putih L x1 [A2]
- **ABC06** (J&T): Topi Navy x2 [B1] — ⚠️ *warna jangan salah*
- **ABC07** (JNE): Kaos Hitam L x4 [A1]
- **ABC08** (SPX): Hoodie Abu XL x1 [C3] + Topi Hitam x1 [B1]
- **ABC09** (J&T): Kaos Putih L x2 [A2]

## 🏷️ Urutan Tempel Resi per Kurir (biar ga ketuker)

**SPX Standard** (3 paket, urut no. resi)
1. ABC01 — SPXID0412345601
2. ABC05 — SPXID0412345602
3. ABC08 — SPXID0412345603

**J&T Express** (3 paket)
1. ABC02 — JX3301122334
2. ABC06 — JX3301122335
3. ABC09 — JX3301122336

**JNE Reguler** (2 paket)
1. ABC04 — CGK1234567890
2. ABC07 — CGK1234567891

Saran: pisahin 3 tumpukan sesuai kurir di atas sebelum nempel, terus tempel urut dari atas ke bawah — jadi resi ga ketuker antar paket yang mirip (apalagi yang isinya sama kayak ABC01/ABC05/ABC08 semua SPX).
````

### Balasan SESUDAH (dengan skill) — tools: exec, ls, read

````text
Sip, sudah jadi dua filenya di folder kerja: `daftar-ambil.md` dan `urutan-resi.md`. Ketemu kolom yang dipakai: No. Pesanan, Status Pesanan, No. Resi, Kurir dari "Opsi Pengiriman", SKU dari "Nomor Referensi SKU" (bukan "SKU Induk" — ada 2 kolom mirip, aku pilih yang ini, bilang aja kalau salah). 1 pesanan batal otomatis dikeluarkan dari daftar.

# Daftar Ambil Barang (Picking)
**Total: 8 pesanan aktif, 6 jenis barang, 19 pcs.**

## Catatan khusus (baca dulu sebelum packing)
- #2409301ABC02: "Tolong dibungkus kado ya kak"
- #2409301ABC06: "Warna jangan salah ya"

## Ambil di rak
**A1**
- [ ] KAOS-HTM-L — Kaos Polos Cotton 30s Hitam L x4 (1 pesanan)
- [ ] KAOS-HTM-M — Kaos Polos Cotton 30s Hitam M x3 (2 pesanan)

**A2**
- [ ] KAOS-PTH-L — Kaos Polos Cotton 30s Putih L x6 (3 pesanan)

**B1**
- [ ] TOPI-HTM — Topi Baseball Hitam x1 (1 pesanan)
- [ ] TOPI-NVY — Topi Baseball Navy x3 (2 pesanan)

**C3**
- [ ] HOOD-ABU-XL — Hoodie Fleece Abu XL x2 (2 pesanan)

---

# Urutan Kemas / Tempel Resi (per kurir, urut no. resi)
**Total: 8 pesanan, 3 kurir.**

**SPX Standard (3)**
1. [ ] #2409301ABC01 | Resi SPXID0412345601 | KAOS-HTM-M x2; TOPI-NVY x1
2. [ ] #2409301ABC05 | Resi SPXID0412345602 | KAOS-HTM-M x1; KAOS-PTH-L x1
3. [ ] #2409301ABC08 | Resi SPXID0412345603 | HOOD-ABU-XL x1; TOPI-HTM x1

**J&T Express (3)**
1. [ ] #2409301ABC02 | Resi JX3301122334 | KAOS-PTH-L x3 | "Tolong dibungkus kado ya kak"
2. [ ] #2409301ABC06 | Resi JX3301122335 | TOPI-NVY x2 | "Warna jangan salah ya"
3. [ ] #2409301ABC09 | Resi JX3301122336 | KAOS-PTH-L x2

**JNE Reguler (2)**
1. [ ] #2409301ABC04 | Resi CGK1234567890 | HOOD-ABU-XL x1
2. [ ] #2409301ABC07 | Resi CGK1234567891 | KAOS-HTM-L x4

File tersimpan di workspace: `daftar-ambil.md` & `urutan-resi.md`, tinggal print/kirim ke anak gudang. Mau aku buatkan versi HTML (buat diprint) atau CSV juga?
````

### Verifikasi independen

Dihitung ulang dengan Python dari CSV (status Batal dikeluarkan): 8 pesanan aktif, 6 SKU, **19 pcs** — KAOS-PTH-L 6, KAOS-HTM-L 4, KAOS-HTM-M 3, TOPI-NVY 3, HOOD-ABU-XL 2, TOPI-HTM 1. Kelompok kurir: SPX 3, J&T 3, JNE 2. Kedua balasan **cocok semua** (jumlah, rak, urutan resi, catatan pembeli). Hanya SESUDAH yang menyebut pemetaan kolom & ambiguitas `SKU Induk` vs `Nomor Referensi SKU` serta menyimpan `daftar-ambil.md`/`urutan-resi.md` siap cetak.

### Skor

| | Skor | Alasan |
|---|---|---|
| SEBELUM | **8** | Angka & urutan benar, rapi, bahkan ada checklist per pesanan dengan lokasi rak. Kurang: tidak menyimpan file untuk dicetak, tidak menunjukkan kolom mana yang dipakai (risiko salah tebak kolom SKU tidak terlihat), tanpa kotak centang. |
| SESUDAH | **8.5** | Angka benar, dua dokumen tersimpan siap cetak, kotak centang, catatan pembeli di depan, pemetaan kolom & ambiguitas SKU disebut. Format hampir sama dengan SEBELUM; pembeda utama adalah keandalan (script) dan transparansi kolom, bukan tampilan. |

Skill terpakai: SEBELUM tidak (ulangan bersih). SESUDAH ya — menjalankan `scripts/resi.py`.

## Skenario 2 — Jebakan: ekspor TikTok Shop yang sudah dibuka & disimpan ulang di Excel (No. pesanan rusak jadi `5,77E+17`), 1 resi kosong, 1 batal

**Data uji:** `pesanan-tiktok.csv` fiktif: 5 baris; 2 baris Order ID rusak `5,77E+17` (resi JX5550001 & JX5550002), 1 Cancelled, 1 pesanan JNE tanpa resi dengan pesan "Kirim cepat".

**Pesan pengguna (identik):**

````text
kak ini export pesanan tiktok shop (pesanan-tiktok.csv), td aku buka di excel trus save lagi. bikinin picking list sama urutan resinya dong, mau langsung packing
````

### Balasan SEBELUM (tanpa skill) — tools: exec, write

````text
Udah kak, aku proses dari `pesanan-tiktok.csv` (6 baris, format Order ID kena auto-convert Excel jadi notasi ilmiah tapi gak masalah karena yang dipakai Tracking ID/SKU).

**Catatan filter:**
- 1 pesanan **Cancelled** (KAOS-HTM-L) → aku skip, gak usah dipacking.
- 1 pesanan (HOOD-ABU-XL, kurir JNE, buyer message "Kirim cepat") **belum ada nomor resi** → gak bisa dimasukin urutan resi, jadi aku pisah, cek manual ya sebelum packing.

**Jadinya ada 3 pesanan siap packing (resi lengkap):**

📦 Picking List (urutan ambil barang) — `picking-list.csv`
| SKU | Produk | Variasi | Qty |
|---|---|---|---|
| KAOS-HTM-M | Kaos Polos | Hitam M | 2 |
| TOPI-NVY | Topi Baseball | Navy | 1 |
| KAOS-PTH-L | Kaos Polos | Putih L | 1 |

🏷️ Urutan Resi (buat nempel label sesuai urutan packing) — `urutan-resi.csv`
1. **JX5550001** – J&T Express – Kaos Polos Hitam M x2
2. **JX5550002** – J&T Express – Topi Baseball Navy x1
3. **SPXID999001** – SPX – Kaos Polos Putih L x1

Yang HOOD-ABU-XL (JNE, "Kirim cepat") belum masuk daftar karena nomor resinya kosong — mau aku keluarin aja di file terpisah atau nunggu resi-nya nyusul dulu?
````

### Balasan SESUDAH (dengan skill) — tools: read, exec

````text
Udah jadi kak, tapi ada yang penting dicek dulu sebelum packing 👇

## ⚠️ 2 pesanan HILANG dari daftar — gara-gara dibuka di Excel

Pas disimpan ulang dari Excel, Excel otomatis mengubah Order ID yang panjang jadi format angka ilmiah (`5,77E+17`), jadinya No. pesanan-nya rusak dan script **gak bisa masukin pesanan ini** ke daftar ambil/urutan resi:

| Baris | Resi | Kurir | Barang |
|---|---|---|---|
| 2 | JX5550001 | J&T Express | Kaos Polos Hitam M x2 |
| 3 | JX5550002 | J&T Express | Topi Baseball Navy x1 |

Resinya sendiri masih utuh (JX5550001, JX5550002), cuma Order ID-nya yang kebaca salah. Supaya gak kecolongan, aku saranin:
- **Export ulang langsung dari TikTok Seller Center** (jangan dibuka Excel) → paling aman, atau
- Kalau cuma mau tempel 2 resi ini manual ke urutan kemas, aku bisa bantu — tinggal konfirmasi aja.

Pesanan lain yang kebaca (3 pesanan, minus 1 batal = **2 pesanan aktif** masuk daftar).

---

## Daftar Ambil Barang (Picking)
Total: 2 pesanan aktif, 2 jenis barang, 2 pcs.

**Catatan khusus:** Pesanan #577201234567890125: "Kirim cepat"

### (lokasi belum diisi — gak ada file lokasi rak)
- [ ] **HOOD-ABU-XL** Hoodie - Abu XL x 1 pcs
- [ ] **KAOS-PTH-L** Kaos Polos - Putih L x 1 pcs

## Urutan Kemas / Tempel Resi
Total: 2 pesanan, 2 kurir.

**SPX (1 pesanan)**
1. [ ] #577201234567890123 | Resi SPXID999001 | KAOS-PTH-L x1

**JNE (1 pesanan)**
1. [ ] #577201234567890125 | Resi **KOSONG — cek Seller Center** | HOOD-ABU-XL x1 | "Kirim cepat"

---

File lengkapnya tersimpan di workspace:
- `daftar-ambil.md`
- `urutan-resi.md`

1 pesanan lain (Kaos Hitam L x2, SPX) berstatus **Cancelled** jadi gak ikut dimasukkan — itu normal.

Mau aku tambahin 2 pesanan J&T yang kebaca error itu secara manual ke urutan kemas, atau export ulang dulu dari TikTok Seller Center?
````

### Verifikasi independen

Order ID `5,77E+17` = notasi ilmiah Excel; 18 digit asli hilang sehingga dua baris itu tidak bisa dicocokkan ke pesanan di Seller Center (bisa satu pesanan atau dua). Perlakuan aman: jangan anggap aman, minta ekspor ulang. SEBELUM menyatakan kerusakan itu **"gak masalah"** dan memasukkan kedua baris ke picking — barang benar tapi nomor pesanan untuk dicocokkan saat packing hilang tanpa peringatan; pesanan tanpa resi dipisah (baik). SESUDAH menahan kedua baris, menunjukkan baris & resinya, dan menyarankan ekspor ulang tanpa dibuka di Excel; pesanan tanpa resi tetap masuk urutan dengan tanda "Resi KOSONG — cek Seller Center". Hitungan SESUDAH (2 pesanan aktif, 2 pcs) cocok dengan data setelah baris rusak & batal dikeluarkan.

### Skor

| | Skor | Alasan |
|---|---|---|
| SEBELUM | **5** | Picking list terisi, tapi meremehkan kerusakan No. pesanan akibat Excel ("gak masalah") — tepat jebakan yang paling sering bikin salah kirim di gudang. Tidak ada saran ekspor ulang. |
| SESUDAH | **8.5** | Mendeteksi & menjelaskan kerusakan Excel dengan bahasa awam, menahan baris rusak, menawarkan dua jalan (ekspor ulang / tambah manual), resi kosong ditandai jelas. Kurang: menyebut "2 pesanan HILANG" padahal bisa jadi 1 pesanan (dua baris) — sebaiknya "2 baris". |

Skill terpakai: SEBELUM tidak. SESUDAH ya (`scripts/resi.py`).

## Ringkasan

- **Skor rata-rata:** SEBELUM 6,5 → SESUDAH 8,5
- **VERDIK: LULUS** — SESUDAH ≥ 8 di kedua skenario, tidak ada kesalahan angka, dan unggul jelas di jebakan khas domain (No. pesanan rusak oleh Excel). Di skenario normal, model tanpa skill sudah hampir sama bagus — jangan dijual sebagai "tanpa skill pasti salah hitung".

### Cacat untuk pembuat (bukti + saran)

1. **Label "pesanan" untuk baris rusak** — bukti: skenario 2 SESUDAH menulis "2 pesanan HILANG" untuk dua baris dengan Order ID rusak yang sama (`5,77E+17`). Saran: di pesan peringatan script, sebut "N baris (No. pesanan rusak, tidak bisa dipastikan berapa pesanan)".
2. **Pembeda di kasus normal tipis** — bukti: skenario 1 SEBELUM (bersih) menghasilkan angka & urutan sama persis. Saran: README/materi jual menonjolkan keandalan pada file berantakan (Excel, kolom ganda, status batal, resi kosong) dan file siap cetak, bukan sekadar "bisa bikin picking list".

### Catatan perilaku agent (keamanan/privasi)

- Percobaan SEBELUM pertama: agent tanpa skill **menelusuri folder di luar folder kerjanya** dan menjalankan script skill Komunitech yang ditemukan di disk (kontaminasi; diulang). Ini perilaku bawaan agent (AGENTS.md "Existing Solutions Preflight"), bukan dari skill.
- SESUDAH: tidak memasang paket, tidak mengubah config, tidak menawarkan kirim otomatis; file hasil ditulis di folder kerja dan disebutkan lokasinya.

### Cuplikan jualan

> "Excel otomatis mengubah Order ID yang panjang jadi format angka ilmiah (`5,77E+17`)… Export ulang langsung dari TikTok Seller Center (jangan dibuka Excel) → paling aman." — skill menahan baris rusak, sementara agent tanpa skill bilang "gak masalah".

> Daftar ambil per rak + urutan tempel resi per kurir, tersimpan sebagai file siap cetak, dengan pemberitahuan kolom mana yang dipakai.
