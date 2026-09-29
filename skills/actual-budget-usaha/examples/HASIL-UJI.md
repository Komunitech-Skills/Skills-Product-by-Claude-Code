# HASIL UJI — actual-budget-usaha v1.0.0 (penguji independen Akun B, 26 September 2026)

Penguji bukan pembuat; hanya membaca folder skill. Semua data uji dibuat sendiri (fixture pembuat **tidak** dipakai
kecuali oleh tes bawaan). Uji di scratchpad, bukan `.claude/skills/`. `uji_openclaw.sh` tidak dijalankan (di luar
tugas ini).

## Skor: **8 / 10** — lulus quality gate (≥ 7)

## Alasan
- **Angka benar dan terbukti independen.** Dua budget Actual ASLI dibuat penguji dengan `@actual-app/api` 26.9.0
  (npm lokal di scratchpad): "Desainer Dimas" (amplop; rollover minus, kategori dihapus & dialihkan beserta
  anggarannya, split GoPay/Tokopedia, transfer on-budget, transfer ke akun off-budget berkategori, transaksi terhapus
  Rp 9.999.999, transaksi tanpa kategori, sen .99/.49/.25) dan "Warung Kopi Pak Joko" (amplop; jebol berturut-turut,
  akun laci, sen .75/.10, **hold Rp 1 jt untuk bulan depan**). `ringkasan --json` Juni–September dibandingkan dengan
  `getBudgetMonth` resmi dan hitungan Decimal penguji sendiri: **76 dari 76 pos sama persis** (sisa per kategori,
  To Budget, total pemasukan/anggaran/terpakai). Baseline tanpa skill salah di 3/6 kategori.
- **Konversi mutasi andal.** 4 CSV fiktif gaya BCA (cp1252, `'01/08`, CR/DB tanpa judul, PEND, 4 baris ringkasan,
  baris kembar), BRI (UTF-8 BOM, jam, format Indonesia, saldo minus), Mandiri (`;`, cp1252, `01 Agu 2026`),
  BNI (`Cr.`/`Db.`): semua cek saldo COCOK; hasil diurai parser server Actual + `looselyParseAmount` **asli** paket
  dan diimpor ke akun kosong: 26/26 baris, 0 galat, semua jumlah persis sampai sen, saldo akun = hitungan penguji.
  Baris ragu ditandai: tarik tunai, top up, kartu kredit, setor tunai, marketplace, refund, pencairan KUR, dobel.
- **Aman.** Audit kode: hanya pustaka standar (tidak ada socket/urllib/subprocess/kredensial); db dibuka
  `file:...?mode=ro`, disalin ke memori; hash db sama sebelum/sesudah, tidak ada file baru, jalan di folder read-only.
  File mutasi asli tidak diubah. Tanda `=` di awal keterangan dibuang.
- **Data rusak ditangani:** db tidak ada (kode 3), 0 byte & teks (kode 4 "bukan database SQLite"), SQLite lain
  (kode 4, sebut tabel yang hilang), folder kosong (3), .zip Export (2, minta ekstrak), banyak budget (2, minta pilih),
  kunci EXCLUSIVE (kode 4 setelah 5,06 detik), kunci RESERVED (tetap membaca data ter-commit), bulan tidak valid (2).
  Mutasi: campur format angka, tanpa penanda CR/DB, Excel, PDF, kosong, tidak ada → berhenti dengan pesan jelas.
- **Tes bawaan:** `python3 tests/uji_regresi.py` → 32 tes OK. `python3 scripts/validate.py --skill actual-budget-usaha`
  → "✅ 1 skill valid, 83 baris katalog sesuai."

## Skenario
| # | File | Jenis | Hasil |
|---|---|---|---|
| 3 | `03-normal-bca-freelancer-uji-akun-b.md` | normal (A/B & pesaing memakai skenario ini) | Lulus |
| 4 | `04-normal-ringkasan-warung-uji-akun-b.md` | normal | Lulus (temuan 1) |
| 5 | `05-normal-multibank-uji-akun-b.md` | normal | Lulus (temuan 2, 4) |
| 6 | `06-input-kurang-uji-akun-b.md` | input tidak lengkap | Lulus |
| 7 | `07-luar-cakupan-uji-akun-b.md` | luar cakupan (tulis DB + saran investasi) | Lulus |
| A/B | `00-pembanding-tanpa-skill.md` | tanpa vs dengan skill | Dengan skill jelas lebih baik |
| Pesaing | `00-banding-pesaing.md` | ClawHub thisisjeron/actual-budget, s-stefanov/actual-mcp | Skill kita unggul untuk sasaran (berbasis dokumentasi; pesaing tidak dijalankan) |

## Temuan (tidak ada yang kritis; tidak ada angka salah)
1. **Sedang — dana ditahan tidak tampil di teks.** `holdBudgetForNextMonth` Rp 1 jt: To Budget benar, tetapi teks
   ringkasan tidak menyebut "Ditahan untuk bulan depan" (hanya `ditahan` di `--json`). Pemilik bisa bingung.
2. **Sedang — `SETORAN PENJUALAN QRIS` ditandai PINDAH DANA** (pola `SETORAN` terlalu luas). Aman (dikosongkan &
   ditanyakan) tapi pesannya salah untuk warung yang menyetor hasil jualan. Persempit ke `SETOR(AN)? TUNAI`.
3. **Kecil — payee transfer tampil "(tanpa payee)"** di PENGELUARAN TERBESAR (transfer ke akun off-budget "Reksa
   Dana" Rp 2 jt). Payee transfer di Actual bernama kosong; sebaiknya tampil "Transfer ke Reksa Dana".
4. **Kecil — dokumentasi `12,5`.** `references/format-bank.md` bilang `12,5` tanpa petunjuk → dilewati; nyatanya
   `,5` dianggap petunjuk gaya koma sehingga dibaca Rp 12,50 (wajar). Selaraskan teks; pertimbangkan peringatan
   untuk nominal < Rp 100.
5. **Kecil — usulan "Pendapatan Usaha"** tidak dipetakan otomatis walau budget hanya punya satu kategori pemasukan
   (Honor Klien) → semua uang masuk jadi "perlu dicek".
6. **Tumpang tindih cakupan (perlu dirapikan untuk pembeli):**
   - `kas-umkm` juga "impor mutasi bank" + ringkasan Telegram, dan pemicunya "Impor mutasi BRI ini" sama.
     `actual-budget-usaha` sudah membedakan di tabel "Pilih skill" (kas-umkm = buku kas tanpa aplikasi), tetapi
     **description** hanya menyebut hledger-usaha & atur-keuangan-pribadi, tidak `kas-umkm`; dan `kas-umkm` /
     `atur-keuangan-pribadi` belum menyebut `actual-budget-usaha` sama sekali. Sarankan: tambah "atau buku kas tanpa
     aplikasi (kas-umkm)" di description ini, dan rujukan balik "pakai Actual Budget? → actual-budget-usaha" di
     kedua skill itu.
   - Dengan `atur-keuangan-pribadi` tidak membingungkan: itu rencana di chat tanpa aplikasi; skill ini operator
     aplikasi Actual.
7. **Belum diuji penguji:** mode tracking (tidak dibuat ulang secara independen; hanya lewat tes bawaan pembuat),
   income carryover/auto-hold, Windows/macOS, layar Import desktop (klik manual), ekspor mutasi bank asli,
   jadwal OpenClaw/Telegram (`references/openclaw-jadwal.md` masih ⚠️ belum diverifikasi, sesuai pengakuan pembuat).

## platform_teruji yang jujur
`claude-code (simulasi agent)` — script dijalankan di Linux; perilaku agent disimulasikan penguji.

## Rekomendasi
Layak lanjut ke uji platform asli setelah perbaikan temuan 1–2 dan 6 (kecil, tanpa mengubah rumus). Skor 8, bukan
lebih tinggi, karena temuan 1–2 terlihat langsung oleh pengguna warung dan jalur jadwal Telegram belum terbukti.
