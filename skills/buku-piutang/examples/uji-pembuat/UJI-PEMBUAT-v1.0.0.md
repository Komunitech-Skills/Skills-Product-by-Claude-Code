# Uji pembuat — buku-piutang v1.0.0 (bukan penilaian)

- **Tanggal:** 2026-09-26. **Oleh:** agent pembuat skill (bukan penguji independen). Skor kualitas sengaja **tidak**
  diberikan; penilaian, uji A/B, dan uji banding pesaing menunggu penguji terpisah (CLAUDE.md Tahap 6).
- **Lingkungan:** Linux, Python 3.10 & 3.12 (sintaks juga diperiksa untuk 3.8). Data fiktif di folder sementara /
  scratchpad, `--db` per skenario, tanggal disimulasikan dengan opsi uji `--hari-ini`.

## Yang sudah dijalankan
| Uji | Hasil |
|---|---|
| `tests/uji_regresi.py` | 52 tes OK (uang & PPN, tanggal ngawur, catat, bayar/kelebihan/deposit, invarian, batal, potong, umur & batasnya, jatuh tempo, posisi `--per`, rekap JSON, samarkan, draf & tautan, terkirim, impor CSV rusak/format Amerika/campur/per barang/tanpa nomor nota/ulang, ekspor + formula injection, restore DB rusak, `--mulai-baru`, DB 0 byte, DB milik aplikasi lain, DB terkunci, cadangan harian, tanpa jaringan) |
| Jembatan `tagih-piutang` | `ekspor --format tagih-piutang` dibaca `hitung_telat.py --file` tanpa error; sisa & total cocok (tes otomatis) |
| Audit hook Python (baca, draf, rekap, ekspor, backup) | 0 peristiwa socket/subprocess/os.system |
| Contoh sesi | `examples/contoh-sesi-toko-sembako.md` = keluaran asli script; angka dicek manual di bagian akhir file |
| `openclaw automations add` | **Belum** diuji di Gateway untuk skill ini; bentuk perintah disalin dari pola `crm-wa` yang sudah diuji |

## Catatan untuk penguji independen
- Skenario yang disarankan: toko grosir dengan bon ke warung (cicilan + kelebihan bayar), jasa B2B dengan invoice
  DPP+PPN termin 30 hari, impor ekspor kasir/Excel yang berantakan, input tidak lengkap, dan permintaan di luar
  cakupan (kirim tagihan otomatis ke semua pelanggan, surat somasi dengan denda, sebar nama penunggak ke grup).
- Kandidat pesaing untuk uji banding: skill/prompt "accounts receivable", "invoice tracker", "AR aging" di ClawHub,
  skills.sh, GitHub; fitur piutang aplikasi akuntansi berlangganan sebagai pembanding fitur.
