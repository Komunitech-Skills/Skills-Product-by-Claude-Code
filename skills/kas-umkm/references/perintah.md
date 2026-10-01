# Daftar perintah kas.py

Format umum: `python3 scripts/kas.py <perintah> [opsi] [--db PATH] [--json]` (Windows: `py` atau `python`).
Semua perintah tulis hanya **pratinjau** sampai diberi `--ya`.

| Perintah | Fungsi | Opsi penting |
|---|---|---|
| `init` | Buat buku kas baru + akun "Laci kas" | `--nama-usaha` (wajib), `--kas-awal`, `--mulai DD/MM/YYYY`, `--batas-prive`, `--zona WIB\|WITA\|WIT`, `--mulai-baru` (database rusak tanpa cadangan) |
| `info` | Lokasi database, akun & saldo, cadangan | — |
| `atur` | Ubah pengaturan | `--nama-usaha`, `--zona`, `--batas-prive 3jt\|hapus` |
| `akun daftar` | Saldo per akun | — |
| `akun tambah` | Tambah rekening/e-wallet/brankas | `--nama`, `--jenis tunai\|bank\|e-wallet`, `--saldo-awal`, `--tanggal-awal`, `--terima-qris`, `--kode` |
| `akun ubah` | Ubah akun | `--akun`, `--nama`, `--saldo-awal`, `--tanggal-awal`, `--terima-qris` |
| `catat` | Uang masuk/keluar | `--masuk N` / `--keluar N`, `--kategori`, `--metode`, `--akun`, `--catatan`, `--tanggal`; atau `--baris` diulang; `--izinkan-duplikat`, `--izinkan-minus` |
| `pindah` | Pindah dana antar akun | `--dari`, `--ke`, `--jumlah`, `--biaya`, `--tanggal`, `--catatan` |
| `batal` | Batalkan catatan (tidak dihapus) | `--id 12` atau `#12`, `--alasan` (wajib). Pindah dana: kedua sisi ikut batal |
| `opname` | Hitung uang fisik vs buku | `--fisik N` atau `--pecahan "..."`, `--akun`, `--tanggal`, `--sesuaikan`, `--daftar` |
| `cek-catatan` (v1.0.11) | Rekap sekali jalan dari catatan kas teks/file **tanpa database** (tidak menyimpan, tanpa `--ya`): pemasukan & beban usaha, hasil usaha (laba kas), kasbon/prive/modal terpisah, uang laci seharusnya, selisih dengan hitungan fisik | `--baris "arah;jumlah;kategori;metode;catatan"` diulang atau `--file catatan.txt` (baris `#` diabaikan), `--laci-awal`, `--fisik N` atau `--pecahan "..."`. Kategori kosong = ditebak; tidak tertebak = "PERLU DICEK" (ikut laci, tidak ikut hasil usaha); metode kosong = tunai (disebut sebagai asumsi) |
| `rekap` | Rekap teks siap Telegram | `--tanggal`, `--minggu ini\|lalu\|tgl`, `--bulan ini\|lalu\|09/2026`, `--dari --sampai` (default hari ini) |
| `saldo` | Saldo per akun per tanggal | `--tanggal` |
| `daftar` | Catatan beserta ID | periode, `--kategori`, `--akun`, `--cari`, `--semua` (termasuk batal), `--maks` |
| `impor` | CSV buku kas / mutasi bank | `FILE`, `--akun`, `--jenis-file mutasi-bank\|buku-kas`, `--format-tanggal hari-bulan\|bulan-hari`, `--tahun`, `--kategori-default`, `--tetapkan N=kategori\|pindah:akun\|lewati`, `--sertakan-mirip` |
| `golongkan` (v1.0.1) | Tetapkan kategori catatan "Perlu dicek" (atau catatan biasa lain) | `--id 12` / `--id 12,15`, `--kategori prive\|lain-lain\|...\|pindah:<akun>` (pindah: sisi pasangan dicatat di akun itu), `--izinkan-minus` |
| `impor-kasir` | Rekap harian kasir-lokal (JSON) | `FILE`, `--akun-untuk qris=BRI`, `--ganti` |
| `ekspor` | CSV | `--format lengkap\|emkm\|arus-kas`, `--csv FILE`, periode, `--minggu-riwayat 8`, `--semua`, `--pemisah` |
| `backup` | Cadangan manual / daftar | `--daftar`, `--label` |
| `restore` | Pulihkan dari cadangan | `--dari FILE` |

## Format `--baris`
`arah;jumlah;kategori;metode;catatan;akun;tanggal` — minimal `arah;jumlah`. Kolom kosong = default/tebakan.
Arah: `masuk` / `keluar`. Contoh:
```
--baris "masuk;1,2jt;penjualan;tunai;jualan hari ini"
--baris "keluar;200rb;listrik-air;transfer;token PLN;BRI"
--baris "keluar;50rb;;;es batu;;kemarin"
```

## Nominal yang diterima
`25rb`, `25 ribu`, `100k`, `1,2jt`, `1,25 juta`, `1 jt 250 rb`, `1.250.000`, `Rp1.250.000,-`. Ditolak: `5m` (juta atau miliar?), `1.500 jt`, `4,5` (tanpa satuan), minus, sen (`12,50`), angka ilmiah Excel (`1.5E+06`), 0.
Dari file bank juga diterima format Inggris `1,500,000.00`, akhiran `CR`/`DB`, `(200.000)`; sen dibulatkan ke rupiah terdekat.

## Tanggal
Ketik: `hari ini`, `kemarin`, `3 hari lalu`, `26/09/2026`, `26-09-2026`, `2026-09-26`, `26 Sep 2026`. **Ditolak**: tanpa tahun (`26/09`), tahun 2 angka (`26/09/26`), urutan bulan/hari (`09/26/2026`), tanggal masa depan, nomor seri Excel.
Kategori impor (v1.0.1): (1) `--tetapkan` pengguna; (2) kolom kategori di file; (3) **aturan pindah dana**: tarik tunai ATM (rekening keluar → akun tunai), setor tunai (akun tunai → rekening), pindah buku/antar rekening sendiri/top up yang menyebut nama akun pasangan → `pindah` (`pindah_dikenali`); baris berawalan biaya tetap pengeluaran; (4) tebakan dari keterangan; (5) `--kategori-default`; (6) selain itu **`perlu-dicek`**: ikut saldo, tidak ikut hasil usaha, ditampilkan "BELUM DIGOLONGKAN" di `rekap`, `ekspor --format emkm` ditolak (`perlu_dicek`: daftar ID) sampai `golongkan`; `ekspor --format arus-kas` melewatinya dengan catatan. `daftar --kategori "perlu dicek"` menampilkan semuanya. Baris "Per hari"/"Per minggu" di `rekap` yang memuat catatan 'Perlu dicek' diberi penanda `[termasuk 'Perlu dicek' ... - belum dihitung di hasil usaha]` (v1.0.2).

File impor: urutan hari/bulan diperiksa untuk **seluruh file**. Jika ada baris yang jelas hari/bulan (mis. 26/09), semua dibaca hari/bulan. Jika semua tanggal bisa dibaca dua arah, script meminta `--format-tanggal`. Campuran jelas hari/bulan dan jelas bulan/hari → file ditolak.

## Kolom CSV yang dikenali (impor)
- Tanggal: `Tanggal`, `Tgl`, `Date`, `Tanggal Transaksi`, `Posting Date`
- Keterangan: `Keterangan`, `Uraian`, `Deskripsi`, `Catatan`, `Description`, `Berita`
- Nominal: `Masuk`/`Keluar` (atau `Pemasukan`/`Pengeluaran`), `Debit`/`Kredit` (wajib `--jenis-file`), `Jumlah`/`Nominal`/`Amount`/`Mutasi` (+ kolom `Jenis` berisi masuk/keluar/CR/DB, atau akhiran CR/DB, atau tanda minus)
- Opsional: `Kategori`, `Metode`, `Akun`/`Rekening`
- Baris judul boleh didahului baris informasi rekening (dicari di 15 baris pertama). Baris `Saldo awal/akhir`, `Total`, dan tanggal `PEND` dilewati.

## Kode keluar & JSON
`0` berhasil (termasuk pratinjau), `1` gagal (`error`, plus penanda seperti `perlu_kategori`, `perlu_akun`, `perlu_jenis_file`, `perlu_format_tanggal`, `sudah_diimpor`, `rusak`), `2` perintah salah tulis.
Perintah tulis mengembalikan `mode`, `perlu_konfirmasi`, `perlu_izin` (daftar flag yang harus diputuskan pengguna), `peringatan`, `teks`, dan `backup` (bila cadangan dibuat).

## Struktur data (pengguna mahir)
Satu file SQLite: `akun` (saldo awal + tanggal mulai, penampung QRIS), `transaksi` (tanggal ISO, arah, jumlah integer rupiah, kategori, metode, akun, catatan, jenis `biasa|pindah|penyesuaian|kasir`, grup pindah dana, sumber `manual|impor:<file>|kasir`, sidik impor, status `aktif|batal` + alasan), `opname`, `log`, `meta`. Boleh dibuka read-only dengan DB Browser for SQLite; jangan diedit manual.
