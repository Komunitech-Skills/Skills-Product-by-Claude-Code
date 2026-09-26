# Uji pembuat hledger-usaha v1.0.1 (26 September 2026)

> Catatan **pembuat** atas revisi pemeliharaan berdasarkan temuan penguji independen Akun B
> (`examples/HASIL-UJI.md`, skor 9/10). Bukan uji independen.

## Perubahan
| Temuan | Perbaikan v1.0.1 |
|---|---|
| 1 TINGGI — larangan pembukuan ganda | SKILL.md: baris di tabel "Kapan TIDAK digunakan" + butir pertama "Keamanan & batasan" dengan jawaban penolakan baku (gaya sama dengan `kas-umkm`): dua file jurnal/dua versi laporan, omzet dikecilkan, tanggal dimundurkan, transaksi disembunyikan; dasar UU KUP Pasal 28 ayat (3) & Pasal 39 ayat (1) huruf d & f (UU 28/2007); alternatif sah (`pph-final-umkm`, omzet s.d. Rp 500 juta tidak dikenai pajak untuk orang pribadi, konsultan). Checklist ditambah. |
| 2 SEDANG — pembayaran dipotong PPh 23 | `catat --jenis terima-piutang|jasa|jual` menerima `--pph23` (nominal bukti potong, atau `2%`/`4%` × nominal dibulatkan ke bawah ke rupiah) dan/atau `--diterima` (potongan = nominal − diterima; dicek konsisten). Contoh tagihan Rp 10.000.000 diterima Rp 9.800.000 → `Aset:Bank` +9.800.000, `Aset:Pajak Dibayar Dimuka:PPh 23` +200.000 (akun dibuat otomatis; template `init` kini punya `Aset:Pajak Dibayar Dimuka`), `Aset:Piutang Usaha:<pihak>` −10.000.000; pendapatan tetap bruto. Catatan otomatis: minta bukti potong (Coretax: Bukti Pemotongan/Pemungutan Unifikasi), tarif 2%/4%, PP 55/2022 → konsultan, pembulatan belum dicocokkan dengan Coretax. Potongan bukan 2%/4% → PERHATIAN; potongan ≤0 atau ≥ tagihan, tarif selain 2/4%, `--pph23` pada jenis lain, dan `--pph23` pada tagihan tempo → ditolak (kode 2). `ekspor-emkm` memberi PERHATIAN bila ada saldo Pajak Dibayar Dimuka (tidak ikut buku kas). |
| 3 SEDANG — impor bank saja | `impor-bank` selalu menampilkan "INGAT: mutasi bank hanya berisi uang yang lewat rekening ... catat dengan `catat --via kas`". `laba-rugi`/`bulanan` menambah CATATAN "laba ini belum lengkap" bila pendapatan/biaya periode itu hanya dari mutasi bank tanpa satu pun transaksi `Aset:Kas`. SKILL.md langkah B.7 + checklist. |

Tarif PPh 23 dicek 26-09-2026: halaman DJP https://www.pajak.go.id/en/node/35004 ("2% x jumlah bruto" untuk jasa teknik, manajemen, konsultan, dan jasa lain; tanpa NPWP tarif 100% lebih tinggi), dasar UU 36/2008 Pasal 23 dan PMK 141/PMK.03/2015 (https://jdih.kemenkeu.go.id/dok/141-pmk-03-2015). UU KUP dibaca dari naskah UU 28/2007. Rincian di `references/sumber-resmi.md`.

## Otomatis: `tests/uji_regresi.py`
- Dengan hledger 1.52.4 asli (binary resmi Linux, SHA-256 `f76a2e40…9643a` cocok): **36/36 lulus** (32 lama + 4 baru).
- Tanpa hledger: 31 lulus, 5 dilewati.
- Tes baru `UjiV101`: pelunasan 10 jt diterima 9,8 jt (pratinjau tidak menulis; posting persis; piutang 0; pendapatan bruto 10 jt; neraca seimbang; ekspor EMKM mengingatkan Pajak Dibayar Dimuka); `--pph23 2%` pada 10.000.001 → 200.000 (ke bawah), tarif 15% ditolak, `--diterima` tidak konsisten ditolak, 250rb → PERHATIAN, potongan > tagihan ditolak, `--pph23` pada `beli` & pada jasa tempo ditolak, jasa langsung 4%; pengingat tunai di impor bank & CATATAN laba belum lengkap (hilang setelah ada transaksi kas); SKILL.md memuat penolakan pembukuan ganda dan `--pph23`.

## Manual (hledger 1.52.4 asli)
Buku "Rangga Konsultan": saldo awal BCA 12 jt, jasa tempo 10 jt, pelunasan `--diterima 9,8jt` → `hledger check accounts` lulus, neraca: Bank 21,8 jt + Pajak Dibayar Dimuka 200 rb = modal 12 jt + laba 10 jt (SEIMBANG).

## Belum dikerjakan
Temuan RENDAH 4–5 (nama akun mentah di arus kas, "LABA KOTOR 100%" usaha jasa, "kolom_5", galat argparse `--nominal -500rb`, panduan Mac/Windows) dan uji Windows/Mac sungguhan.
