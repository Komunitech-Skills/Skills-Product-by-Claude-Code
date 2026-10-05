# Daftar perintah `scripts/piutang.py`

Format umum: `python3 scripts/piutang.py <perintah> [opsi] [--db PATH] [--json]` (Windows: `python`/`py`).
Perintah bertanda **(besar)** hanya pratinjau sampai ditambah `--ya` setelah pengguna setuju (cadangan dibuat
sebelum disimpan). Perintah bertanda **(tulis)** langsung tersimpan (cadangan harian otomatis). Lainnya hanya
membaca (database dibuka read-only).

Lokasi database: `--db` → ENV `KOMUNITECH_PIUTANG_DB` → ENV `KOMUNITECH_DATA` + `/piutang/piutang.db` →
`~/KomunitechData/piutang/piutang.db`. Cadangan: `backup-piutang/` di folder yang sama. Batas tunggu database
terkunci: ENV `KOMUNITECH_PIUTANG_TIMEOUT` (detik, default 15).

| Perintah | Kegunaan | Opsi penting |
|---|---|---|
| `init` (besar) | Buat buku piutang | `--nama-usaha`, `--pengirim`, `--rekening`, `--termin` (hari, default 30), `--zona WIB|WITA|WIT`, `--mulai-baru` (database rusak & tanpa cadangan) |
| `info` | Lokasi, jumlah data, pemeriksaan database, cadangan, beda jam komputer | — |
| `atur` (tulis) | Ubah pengaturan | `--nama-usaha`, `--pengirim`, `--rekening`, `--termin`, `--zona` |
| `tambah-pelanggan` (tulis) | Pelanggan baru tanpa nota | `--nama`, `--wa`, `--sapaan` (Bu/Pak/Kak/`-`), `--catatan`, `--izinkan-duplikat` |
| `ubah-pelanggan` (tulis) | Ubah nama/nomor/sapaan | `--pelanggan`, `--nama`, `--wa` (`-` hapus), `--sapaan`, `--catatan` |
| `hapus-pelanggan` (besar) | Hapus data pelanggan (hanya bila piutang & deposit nol) | `--pelanggan` |
| `catat` (tulis) | Catat nota/bon yang belum dibayar | `--pelanggan` (wajib), `--nominal` ATAU `--dpp` + `--ppn 11|12`, `--nota`, `--tanggal`, `--jatuh-tempo` (tanggal atau "30 hari") ATAU `--termin`, `--keterangan`, `--wa`, `--sapaan`, `--pelanggan-baru` |
| `ubah-nota` (tulis) | Koreksi nota | `--nota`, `--tanggal`, `--jatuh-tempo`/`--termin`, `--nominal`, `--keterangan`, `--no-baru`, `--pelanggan` (hanya bila belum ada pembayaran) |
| `bayar` (tulis) | Catat pembayaran | `--pelanggan` dan/atau `--nota`, `--jumlah` (nominal atau `lunas`), `--tanggal`, `--metode`, `--catatan`, `--kelebihan kredit|kembalikan|nota-lain`, `--izinkan-dobel` |
| `pakai-kredit` (tulis) | Pakai deposit untuk nota terbuka | `--pelanggan`, `--nota`, `--tanggal` |
| `kembalikan` (tulis) | Deposit dikembalikan ke pelanggan | `--pelanggan`, `--jumlah` (nominal atau `semua`), `--tanggal`, `--catatan` |
| `potong` (besar) | Kurangi tagihan: retur, diskon pelunasan, diikhlaskan | `--nota`, `--jumlah` (nominal atau `sisa`), `--alasan` (wajib), `--tanggal` |
| `batal-nota` (besar) | Nota salah catat/dobel/pesanan batal | `--nota`, `--alasan` (wajib). Pembayaran pada nota itu menjadi deposit |
| `batal-bayar` (besar) | Pembayaran salah catat/transfer gagal | `--bayar B0003`, `--alasan` (wajib) |
| `saldo` | Saldo semua pelanggan / rincian satu pelanggan | `--pelanggan`, `--per <tanggal>`, `--semua` (termasuk saldo nol), `--samarkan` |
| `umur` | Umur piutang (aging) + persen | `--per <tanggal>`, `--semua`, `--samarkan` |
| `jatuh-tempo` | TERLEWAT / HARI INI / MINGGU INI (7 hari ke depan) | `--semua` (default maks 20 baris per kelompok), `--samarkan` |
| `ringkasan` | Ringkasan harian untuk Telegram pemilik | `--samarkan`, `--semua` (default maks 10 baris per kelompok) |
| `rekap` | Rekap periode + JSON untuk laporan | `--periode hari-ini|kemarin|minggu-ini|minggu-lalu|bulan-ini|bulan-lalu|tahun-ini|semua`, `--dari/--sampai`, `--rumus`, `--samarkan` |
| `draf` | Draf pesan tagihan + tautan wa.me | `--pelanggan` atau `--nota`, `--pesan "<teks final>"` |
| `terkirim` (tulis) | Pemilik sudah mengirim pengingat | `--pelanggan` atau `--nota` (sekali per hari per nota) |
| `impor <file.csv>` (besar) | Impor dari CSV nota/kasir/Excel | `--termin`, `--gabung-baris`, `--format-tanggal hari-bulan|bulan-hari` |
| `ekspor` | CSV untuk Excel / tagih-piutang | `--format lengkap|tagih-piutang|pembayaran`, `--status terbuka|semua`, `--ke <file.csv>` (alias `--csv`), `--timpa`, `--samarkan` |
| `backup` | Cadangan manual / daftar | `--daftar`, `--label` |
| `restore` (besar) | Pulihkan dari cadangan (juga saat database rusak total) | `--dari <file>` |

`--pelanggan` menerima kode (`P0003`), nomor WA, atau nama ("Tini" cocok dengan "Warung Bu Tini"). Lebih dari
satu yang cocok → gagal dengan `ambigu: true` + `pilihan`. Saat `catat`, pencocokan lebih ketat: hanya nama sama
persis/kode/nomor; nama mirip → `mirip: true` (tanyakan: orang yang sama atau `--pelanggan-baru`).

## Aturan data
- **Uang** selalu integer rupiah. Diterima: `1.250.000`, `1,25 jt`, `750rb`, `2 jt 500 rb`, `Rp1.250.000,-`,
  `1.234.567,50` (sen dibulatkan ke rupiah terdekat, 0,5 ke atas, dan disebut). Ditolak: `4,5` tanpa satuan,
  `12.50`, `1.500 jt`, `5m`, negatif, nol, ≥ Rp 1 triliun.
- **PPN** (`--dpp` + `--ppn`): `11` = 12% × DPP nilai lain 11/12 (efektif 11%), `12` = 12% penuh (barang mewah).
  PPN = floor(DPP × tarif) sekali, pecahan dihitung persis; tidak pernah melebihi tarif. Pembulatan belum
  dicocokkan dengan Coretax. Harga yang sudah termasuk PPN → pakai `--nominal` (pemecahan DPP: skill `hitung-ppn`).
- **Tanggal** (hari/bulan/tahun): `26/09/2026`, `26-09-2026`, `26.09.2026`, `26/9/26` (tahun 2 angka disebut),
  `26 Sep 2026`, `26-Sep-2026`, `2026-09-26` (juga dengan jam), `hari ini`, `kemarin`, `3 hari lalu`. Tanpa tahun
  (`26/9`, `26 Sep`) hanya bila ≤ 180 hari dari acuan (nota/bayar: ke belakang; jatuh tempo: ke depan dari tanggal
  nota). Ditolak: tanggal tidak ada (`31/09/2026`), format Amerika (`10/25/2026`, diberi petunjuk), angka seri
  Excel (`46291`), tahun < 2000/> 2100, tanggal nota/bayar di masa depan, jatuh tempo sebelum tanggal nota,
  `--jatuh-tempo 30` (tanggal atau hari?).
- **Nomor nota** dibandingkan tanpa spasi/tanda baca (`INV-001` = `inv 001` = `INV/001`). Nomor otomatis `PB-0001`
  (catat) dan `IMP-0001` (impor tanpa kolom nota).
- **Nomor WA** → `62…`; tampil `0812-0000-1234`, disamarkan `0812-****-1234`.
- **Alokasi pembayaran** tanpa `--nota`: jatuh tempo paling awal dulu (lalu tanggal nota). Tanggal alokasi = yang
  lebih akhir antara tanggal bayar dan tanggal nota (DP sebelum nota tetap sah).
- **Invarian** (diperiksa setiap perubahan, sebelum disimpan): sisa nota ≥ 0 dan deposit pelanggan ≥ 0. Jika
  dilanggar → seluruh perubahan dibatalkan dengan `invarian: true`.

## Rumus
- Sisa nota = nominal − pembayaran yang dialokasikan ke nota itu − potongan.
- Total piutang = jumlah sisa semua nota aktif (nota batal tidak dihitung).
- Deposit/kelebihan bayar pelanggan = pembayaran − bagian yang dipakai untuk nota aktif − pengembalian.
- Saldo bersih = piutang − deposit (minus = deposit milik pelanggan, bukan utang pelanggan).
- Hari lewat = tanggal posisi − jatuh tempo. Umur: ≤ 0 belum jatuh tempo; 1–30; 31–60; 61–90; > 90 hari.
  Persen = nominal kelompok ÷ total piutang, 1 desimal (0,05 ke atas).
- Jatuh tempo: TERLEWAT = hari lewat > 0; HARI INI = 0; MINGGU INI = jatuh tempo 1–7 hari lagi.
- Posisi `--per` = hanya nota, pembayaran, alokasi, potongan, pengembalian bertanggal ≤ tanggal itu.

## Draf pesan tagihan
Nota yang ikut: terlewat + jatuh tempo ≤ 7 hari (atau `--nota`). Tidak ada? semua nota terbuka (pengingat awal).

| Jenis | Kondisi (keterlambatan terbesar) | Isi |
|---|---|---|
| `pengingat-awal` | belum jatuh tempo | "Izin mengingatkan ... akan jatuh tempo", abaikan bila sudah bayar |
| `hari-jatuh-tempo` | 0 hari | "... jatuh tempo hari ini", abaikan bila sudah bayar |
| `terlewat-ringan` | 1–6 hari | asumsi baik ("sepertinya terlewat"), minta bukti bila sudah bayar |
| `terlewat` | 7–29 hari | minta rencana tanggal bayar |
| `terlewat-lama` | ≥ 30 hari | + tawaran jadwal pembayaran bertahap |

Semua draf: sapaan (Bu/Pak dari nama, "Bapak/Ibu di <usaha>" untuk nama usaha), daftar nota + sisa + jatuh
tempo, total, rekening dari pengaturan, ucapan terima kasih. Tanpa denda, ancaman, atau kata hukum. `saran`
(untuk pemilik, bukan untuk pelanggan) muncul bila lewat ≥ 14 hari atau diingatkan ≥ 2 kali: pakai `tagih-piutang`.

## Impor CSV
Kolom wajib: pelanggan, tanggal, nominal (atau sisa). Pemisah `;` `,` tab `|` dikenali otomatis; UTF-8 atau
Windows-1252. Judul kolom yang dikenali (huruf besar/kecil, spasi/garis bawah bebas):

| Isi | Judul kolom |
|---|---|
| pelanggan | pelanggan, nama pelanggan, nama, customer, pembeli, konsumen, klien, debitur |
| nota | no nota, no invoice, invoice, no faktur, no transaksi, receipt number, order id, no pesanan, no bon, no struk |
| tanggal | tanggal, tgl, date, tanggal nota/transaksi/invoice, invoice date, waktu, created at |
| jatuh tempo | jatuh tempo, tgl jatuh tempo, jt, due date, tempo, batas bayar (tanggal, atau "30 hari") |
| nominal | nominal, total, jumlah, grand total, total tagihan, amount, nilai, total nota/bon |
| dibayar | dibayar, terbayar, sudah dibayar, paid, amount paid, dp, uang muka |
| sisa | sisa, sisa tagihan, outstanding, balance, balance due, kurang bayar |
| no wa | no wa, wa, whatsapp, no hp, hp, telepon, phone |
| keterangan | keterangan, catatan, note, deskripsi, item, produk, barang |
| status | status, status bayar, payment status, metode bayar, payment method |
| termin | termin, terms, top, payment terms |

- Status: `lunas/paid/selesai/tunai/cash/QRIS/transfer/debit/kartu kredit/e-wallet` → dilewati (sudah dibayar);
  `batal/void/cancel/refund/retur` → dilewati; `belum lunas/tempo/bon/utang/kasbon/unpaid/partial/DP/pending` →
  diimpor; lainnya → baris bermasalah.
- Dibayar di file → dicatat sebagai pembayaran bertanggal nota ("sebelum impor"). Dibayar = nominal → dilewati.
- Nomor nota sudah ada di buku dengan pelanggan & nominal sama → dilewati (impor ulang aman); berbeda → masalah.
- Tanpa kolom nota: baris sama persis (pelanggan, tanggal, nominal) di file → masalah; sudah ada di buku → dilewati.
- Deteksi format tanggal: ada nilai seperti `09/25/2026` (angka kedua > 12) → seluruh impor ditolak kecuali
  `--format-tanggal bulan-hari`; campur hari/bulan & bulan/hari → selalu ditolak.
- Nama pelanggan diawali `=`, `+`, `@` (rumus Excel), tanggal/nominal rusak, dibayar > nominal, jatuh tempo sebelum
  tanggal nota → baris bermasalah (nomor baris fisik di file disebut).

## Kontrak `rekap --json` (`skema_json` 1)
Untuk dibaca alat lain (mis. bagian TAGIHAN `laporan-harian-usaha` bila kelak mendukung buku-piutang). Semua
nominal integer rupiah; tanggal `YYYY-MM-DD`. Kunci berikut tidak akan diubah tanpa menaikkan `skema_json`.

```json
{
  "ok": true, "skema_json": 1, "aplikasi": "buku-piutang", "versi": "1.0.0",
  "hari_ini": "2026-09-30", "zona": "WIB",
  "periode": {"nama": "bulan September 2026", "dari": "2026-09-01", "sampai": "2026-09-30"},
  "arus_periode": {
    "nota_baru": {"jumlah": 4, "nominal": 15100000},
    "pembayaran_masuk": {"jumlah": 2, "nominal": 2300000},
    "potongan": {"jumlah": 0, "nominal": 0},
    "nota_dibatalkan": {"jumlah": 0, "nominal": 0},
    "kelebihan_dikembalikan": {"jumlah": 0, "nominal": 0}
  },
  "posisi": {
    "per": "2026-09-30", "total_piutang": 12850000, "jumlah_nota_terbuka": 3,
    "jumlah_pelanggan_berpiutang": 3, "kredit_pelanggan": 50000, "persen_terlewat": 13.6,
    "umur": {"belum_jatuh_tempo": {"jumlah_nota": 1, "nominal": 11100000}, "1_30": {"...": 0},
             "31_60": {"...": 0}, "61_90": {"...": 0}, "lebih_90": {"...": 0}}
  },
  "jatuh_tempo": {"terlewat": {"jumlah_nota": 2, "nominal": 1750000, "jumlah_pelanggan": 2},
                  "hari_ini": {"...": 0}, "tujuh_hari": {"...": 0}},
  "teratas_terlewat": [{"kode": "P0002", "pelanggan": "Kafe Senja", "sisa_terlewat": 1400000, "telat_maks_hari": 18}],
  "data_sensitif": true, "rumus": {"...": "..."}, "teks": "REKAP PIUTANG - ..."
}
```
- `posisi` dihitung per akhir periode (atau hari ini bila periode belum selesai); `jatuh_tempo` selalu terhadap
  **hari ini**.
- `teratas_terlewat` memuat nama pelanggan (maks. 5). Untuk laporan yang dikirim ke chat, panggil dengan
  `--samarkan` (nama jadi inisial, `data_sensitif: false`).
- Cara menghubungkan (tanpa mengubah skill lain): alat laporan menjalankan
  `python3 <folder>/buku-piutang/scripts/piutang.py rekap --dari <tgl> --sampai <tgl> --json --samarkan [--db PATH]`
  dan membaca kunci di atas apa adanya. Perintah ini hanya membaca (database dibuka read-only).
