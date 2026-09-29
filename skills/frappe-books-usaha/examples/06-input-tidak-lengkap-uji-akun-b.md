# Skenario 6 — Input tidak lengkap — uji Akun B

Permintaan: *"Laporan penjualan dari Frappe Books dong."* (tanpa lokasi file, tanpa periode)

## Perilaku script
| Kondisi komputer | Hasil |
|---|---|
| Tidak ada folder Frappe Books | kode 3: "Lokasi file database Frappe Books belum diketahui." + saran cari `*.books.db` |
| `~/Documents/Frappe Books/Kopi Senja.books.db` (satu file) | ditemukan otomatis, periode bawaan bulan ini (Sep 2026), zona WIB |
| `~/Frappe Books/Kopi Senja.books.db` | **tidak ditemukan** (kode 3) |
| `--bulan september` | kode 2: minta `ini`/`lalu`/`2026-09` |
| `--dari` tanpa `--sampai` | kode 2 dengan contoh |
| `--tz WITA2` | kode 2: pakai WIB/WITA/WIT |

Catatan nyata dari aplikasi asli: di Linux tanpa folder XDG "Documents", Frappe Books v0.36.0 menyimpan file perusahaan baru di
`~/Frappe Books/<nama>.books.db` (`app.getPath('documents')` = folder rumah). Pencarian otomatis skill hanya melihat
`Documents/` dan `Dokumen/`, jadi kasus ini jatuh ke pertanyaan lokasi (aman, tapi tidak otomatis). Windows dengan Documents yang
dialihkan ke OneDrive juga belum dicakup. (rendah)

## Respons agent yang diharapkan (mengikuti SKILL.md, disimulasikan penguji)
> Siap. Saya perlu 2 hal dulu:
> 1) Di mana file Frappe Books-nya? (biasanya `Documents/Frappe Books/<nama usaha>.books.db`, juga terlihat di layar awal Frappe Books)
> 2) Periode yang mana? (mis. bulan ini / bulan lalu / September 2026)
> Kalau mau cepat, saya pakai bulan ini, zona WIB.

Sesuai prinsip "tanya sekali" dan menyebut asumsi. Script tidak menebak file bila ada lebih dari satu (diuji di regresi #29). **Lulus.**
