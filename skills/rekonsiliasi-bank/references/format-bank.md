# Petunjuk Format Ekspor Mutasi Bank

> **Status: BELUM TERVERIFIKASI dengan file ekspor asli terbaru.** Ringkasan di bawah adalah pola umum yang sering dijumpai; nama kolom, urutan, dan format angka dapat berbeda per kanal (internet banking pribadi vs bisnis, aplikasi mobile, CMS korporat) dan dapat berubah sewaktu-waktu. Karena itu skill ini **selalu** menjalankan `deteksi` lalu meminta konfirmasi pengguna. Diperbarui: 2026-09-23.

## Pola yang ditangani script
| Pola | Contoh | Argumen `cocokkan` |
|---|---|---|
| Baris info rekening di atas tabel | "No. rekening : …", "Periode : 01/09/2026 - 30/09/2026" | Otomatis dilewati (atau `--baris-judul-bank N`) |
| Satu kolom nominal + kolom CR/DB tanpa judul | `Jumlah` = `1,500,000.00`, kolom berikutnya `CR` | `--bank-nominal Jumlah --bank-dk kolom_5` |
| Akhiran CR/DB di angka | `1,500,000.00 CR` | `--bank-nominal Jumlah` |
| Kolom debet & kredit terpisah | `Debit` / `Credit`, `Mutasi Debet` / `Mutasi Kredit` | `--bank-debet … --bank-kredit …` |
| Nominal bertanda | `-200000` = keluar | `--bank-nominal … --bank-tanpa-penanda negatif-keluar` |
| Tanggal tanpa tahun | `'02/09` (dengan apostrof) | Tahun dari baris "Periode", atau `--tahun 2026` |
| Transaksi tertunda | `PEND` di kolom tanggal | Dilewati & dilaporkan |
| Baris ringkasan di bawah | "Saldo Awal", "Mutasi Kredit", "Saldo Akhir" | Dilewati (tanggal tak terbaca) |
| Angka format Inggris / Indonesia | `1,500,000.00` / `1.500.000,00` | Otomatis |
| Tanggal | `01/09/2026`, `2026-09-01 10:11:12`, `01 Sep 2026`, `01-SEP-26`, `20260901` | Otomatis (`--urutan-tanggal mdy` bila format AS) |

## Tebakan per bank (hanya petunjuk — BELUM TERVERIFIKASI)
| Tebakan script | Ciri judul kolom yang dicari |
|---|---|
| mirip BCA | "Tanggal Transaksi" + "Cabang"; nominal + kolom CR/DB; tanggal sering tanpa tahun |
| mirip Mandiri | "Val. Date"/"Value Date" + "Reference"/"Transaction Code"; kolom Debit & Credit |
| mirip BRI | "TGL_TRAN", "DESK_TRAN", "MUTASI_DEBET", "MUTASI_KREDIT" |
| mirip BNI | "Post Date" + "Journal" |
| format umum | Selain itu — tetap bisa diproses setelah kolom dikonfirmasi |

## Jika pengguna hanya punya PDF / foto
1. Sarankan unduh ulang mutasi dalam format CSV/Excel dari internet banking (menu mutasi rekening / rekening koran).
2. Jika tidak bisa: salin tabel dari PDF ke Excel/Google Sheets, rapikan kolom tanggal–keterangan–nominal–CR/DB, simpan sebagai CSV.
3. Jangan pernah meminta kredensial internet banking untuk "mengambilkan" mutasi.

## Privasi (sampaikan singkat ke pengguna)
- File mutasi berisi nama, nomor rekening, dan pola keuangan — data pribadi (UU PDP 27/2022).
- Proses di komputer sendiri; jangan unggah ke grup/chat umum.
- Hapus baris info rekening di bagian atas file dan kolom saldo bila hasil akan dibagikan ke pihak lain (mis. admin/akuntan eksternal) — cukup kolom tanggal, keterangan, nominal.
- Hapus `hasil-rekonsiliasi.csv` dari folder bersama setelah selesai.
