# HASIL UJI — resi-picking v1.0.0 (penguji independen, Akun B)

**Skor kualitas: 7/10**

## Temuan (berprioritas)

1. **[Sedang] Auto-deteksi kolom gagal pada header realistis TikTok Shop & Tokopedia (skenario
   02) — 0 dari 2 file lolos tanpa override.** Akar sebab: kata sinonim < 8 huruf ("kurir",
   "invoice") tidak pernah dicocokkan sebagian di `deteksi_kolom`, hanya cocok persis. Ini
   memang sudah ditandai "PERLU REVIEW" di SKILL.md dan ada jalan keluar (`--kolom-...` +
   `pemetaan_kolom`/error jelas), tapi mengurangi janji "instan, cukup satu kalimat" — agent
   WAJIB tahu menawarkan override, bukan cuma melaporkan gagal.
2. **[Rendah] Tanpa kemampuan gabung lintas marketplace** — toko dengan 2+ kanal harus
   menjalankan skrip berkali-kali dan menggabung hasil sendiri; wajar untuk alat "sekali jalan",
   tapi perlu disebut eksplisit ke pengguna di jawaban chat.
3. **[Info, tidak kritikal] Baris ringkasan "Total" tanpa SKU/nama tetap aman** (dites, tetap
   terbuang lewat cek "tanpa identitas barang"); risiko teoritis hanya jika suatu saat ekspor
   mengisi SKU pada baris total — belum ditemukan pada data nyata mana pun.

## Yang berjalan benar (diverifikasi independen, tanpa membaca kode)
- Total qty per SKU/varian, pengelompokan & urutan per kurir, jumlah pesanan aktif vs total,
  cross-check stok kurang, deteksi SKU tak dikenal — **100% cocok** pada ketiga skenario normal.
- Penanganan file rusak (BOM, qty rusak/negatif, duplikat, baris kosong, baris ringkasan) —
  tidak crash, semua dilaporkan dengan alasan + nomor baris.
- Di luar cakupan (minta login otomatis Seller Center): kode diaudit, **tidak ada** jaringan,
  scraping, subprocess, atau kredensial tertanam — batasan dijaga lewat instruksi SKILL.md,
  dan secara teknis skrip memang tidak mampu melakukan itu.
- `python3 scripts/validate.py --skill resi-picking` ✅ lulus; 19/19 test bawaan (`tests/uji_regresi.py`) ✅ lulus.
- Uji A/B: nilai tambah signifikan untuk tugas hitungan pasti (lihat `00-pembanding-tanpa-skill.md`).
- Uji banding pesaing: tidak ada skill agent pesaing langsung; dibanding SaaS berbayar, unggul di
  privasi & tanpa biaya bulanan, kalah di integrasi lintas-marketplace otomatis (`00-banding-pesaing.md`).

## Rekomendasi
Perluas `SINONIM_PESANAN` dengan variasi header TikTok Shop/Tokopedia yang lebih realistis
(`order/adjustment id`, `sku reference no.`, `no. invoice`, `nama barang`, `nama kurir`), dan
turunkan ambang panjang kata untuk pencocokan sebagian atau tambahkan daftar sinonim pendek yang
dicek persis dengan variasi umum ("no kurir", "nama kurir", dst.) sebelum naik ke `lulus`.
Skor di bawah 7 tidak tercapai karena inti perhitungan benar dan batasan keamanan terjaga; namun
skor ditahan di 7 (bukan lebih tinggi) karena tingkat sukses auto-deteksi kolom pada data
"marketplace asli" masih rendah pada uji ini.

`platform_teruji` belum diisi oleh penguji ini (hanya uji skrip/logika, bukan uji platform asli
OpenClaw/Codex/Claude Code/Cursor sesuai Tahap 6 poin 9–10).

---

## Uji ulang independen v1.0.2 (Akun B, 2026-09-26)

**Skor kualitas: 9/10**

Pengujian dilakukan sebagai sesi terpisah dari pembuat skill, hanya membaca folder `skills/resi-picking/`.
Data uji fiktif dibuat baru khusus untuk sesi ini di scratchpad terpisah dari repo (bukan file yang
sudah ada di `examples/uji-pembuat`). Detail lengkap tiap skenario: lihat file `0X-...-uji-ulang-v102-akun-b.md`
di folder ini.

### (a) Verifikasi temuan U12 — status: **BERES**
- Header realistis ekspor TikTok Shop (`Order/Adjustment ID, Tracking ID, Shipping Provider Name,
  Seller SKU, ...`) dan Tokopedia (`No. Invoice, No Resi, Jasa Kirim, SKU Penjual, ...`) kini
  terpetakan **otomatis 2 dari 2, tanpa override** — naik dari 0/2 di v1.0.0. Lihat `02-tiktok-
  tokopedia-header-realistis-uji-ulang-v102-akun-b.md`.
- Sinonim pendek ("kurir", "invoice") dicocokkan berbasis **token kata utuh**, bukan potongan
  substring: kolom uji "Kurirnya" dan "Investory Notes" (sengaja dibuat mirip tapi bukan kata utuh
  "kurir"/"invoice") **tidak** salah tertangkap sebagai kolom Kurir — dikonfirmasi dengan file
  `falsepos/test.csv` di scratchpad (tidak disertakan sebagai file `examples/` karena hanya cek
  negatif singkat, dicatat di sini).
- Pesan error saat ambigu/tidak ditemukan (skenario kolom hilang & di luar cakupan) jelas, menyebut
  kolom yang ada di file dan flag `--kolom-...` yang persis, **tanpa traceback** pada semua kasus
  yang diuji (file kosong, kolom wajib hilang, header tak dikenali, override kolom tidak ada).
- Peringatan `kolom_ambigu` baru **bekerja sesuai spesifikasi**: diuji dengan file yang sengaja
  punya 2 kolom kandidat SKU ("SKU Induk" & "Nomor SKU") — field ditandai ambigu dengan pesan
  jelas + saran `--kolom-sku`, dan override manual berhasil menghilangkan tanda ambigu itu. Lihat
  `03-blibli-lazada-kolom-ambigu-uji-ulang-v102-akun-b.md`.

### (b) 5 skenario Tahap 6 + data rusak — semua lulus, tidak ada crash/traceback
1. **Normal — Shopee** (header resmi ID + lokasi rak + stok): lulus, lihat file `01-...`.
2. **Normal — TikTok Shop & Tokopedia** (header realistis, fokus U12): lulus, lihat file `02-...`.
3. **Normal — Blibli/Lazada-style** (multi-kurir + kolom SKU ambigu yang disengaja): lulus, lihat
   file `03-...`.
4. **Input tidak lengkap** (hanya 4 kolom wajib, tanpa lokasi/stok/kurir/resi/status/catatan):
   lulus, peringatan akurat & tidak menebak-nebak. Lihat file `04-...`.
5. **Di luar cakupan** (file laporan omzet harian, bukan ekspor pesanan per baris): ditolak dengan
   pesan jelas, `ok:false`, tanpa traceback, tidak menulis file output. Lihat file `05-...`.
6. **Data rusak** (di scratchpad, bukan di `examples/`): file kosong → error jelas; kolom wajib
   hilang (`Jumlah`) → error jelas + saran flag; encoding **cp1252** dengan karakter non-ASCII
   ("Café Spécial", en dash "–") → terdeteksi otomatis sebagai `cp1252`, output Markdown UTF-8
   tetap terbaca benar; **BOM UTF-8** → terdeteksi `utf-8-sig`, jalan normal; **baris duplikat
   persis** → 1 baris dobel dihitung sekali (`baris_dilewati.baris_duplikat: 1`), tidak
   menggandakan qty. Semua kasus: exit code sesuai (`0` sukses / `1` gagal-jujur), tanpa Python
   traceback di stderr.

### (c) Verifikasi jumlah picking/rekap secara independen
Dihitung manual dari tiap CSV uji (lihat tabel di masing-masing file `0X-...md`) dan **cocok
persis** dengan output skrip pada semua 3 skenario normal + skenario input tidak lengkap: total
pesanan aktif, jumlah jenis barang, total pcs, pengelompokan rak, pengelompokan kurir, dan
peringatan stok kurang/SKU tak dikenal semuanya benar tanpa selisih.

### Uji tambahan
- `python3 scripts/validate.py --skill resi-picking` → ✅ lulus (1 skill valid, 80 baris katalog sesuai).
- `python3 tests/uji_regresi.py` → ✅ **29/29 lulus** (naik dari 19/19 di v1.0.0 — pembuat menambah
  10 tes baru untuk header marketplace asli & kolom ambigu, sejalan dengan rekomendasi uji sebelumnya).
- `uji_openclaw.sh` **tidak dijalankan** di sesi ini (di luar cakupan penugasan uji ulang ini).

### Temuan
1. **[Rendah] Dokumentasi uji vs kode: baik.** Komentar di `deteksi_kolom()` menjelaskan alasan
   perubahan (dari ambang 8-huruf ke pencocokan token) secara akurat dan cocok dengan perilaku
   yang teramati — memudahkan audit berikutnya.
2. **[Rendah, sama seperti v1.0.0] Tanpa kemampuan gabung lintas marketplace** — masih berlaku,
   tetap wajar untuk alat "sekali jalan"; agent tetap perlu diingatkan menyebutkan ini ke pengguna
   saat file dari 2+ kanal diberikan.
3. **[Info] Kolom bernama sangat mirip kata sinonim tapi bukan kata utuh** (mis. "Kurirnya",
   "Investory Notes") **dikonfirmasi tidak salah tertangkap** — tidak ada risiko regresi ke arah
   over-matching yang mengorbankan akurasi demi cakupan.

### Kesimpulan
Temuan U12 (Sedang) v1.0.0 **terverifikasi beres** dengan data baru yang sengaja realistis dan
berbeda dari fixture pembuat. Tidak ditemukan temuan baru bertingkat Tinggi atau Sedang. Skor naik
dari 7/10 menjadi **9/10** (bukan 10/10 karena keterbatasan gabung lintas-marketplace di poin (b.1)
tetap ada by design dan `uji_openclaw.sh`/uji platform asli belum dijalankan ulang di sesi ini —
`platform_teruji` yang sudah tercatat di `catalog.csv` berasal dari uji sebelumnya, bukan sesi ini).
Layak lanjut ke tahap uji platform asli (Tahap 6 poin 10) sebelum naik status ke `beta`.

