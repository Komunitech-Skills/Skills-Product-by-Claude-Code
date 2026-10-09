# Uji 09 - Input tidak lengkap (permintaan + CSV setengah jadi)

Penguji independen, 2026-09-29, `claude-code (simulasi agent)`.

**Pengguna:** "Tolong bikin PRD buat produk kue kering lebaran saya. Ini ide-idenya, urutkan ya" + lampiran CSV:
```
nama,jangkauan,dampak,keyakinan,usaha
Varian cokelat,500,,60,3
Varian keju,banyak,1,70,2
Tas kertas,300,0.5,0.9,1
Box hampers,200,2,120,4
```

## Perilaku agen
1. Karena pembeli sasaran, harga, dan ukuran tidak ada, agen mengirim **satu pesan** berisi 5 pertanyaan singkat + opsi "pakai default" (sesuai SKILL.md; sama dengan contoh 04 pembuat). Baik.
2. Script dijalankan (keluaran asli, kode 1):
```
| 1 | Tas kertas | 1,35 | Sekarang |
TIDAK DIHITUNG baris 2 (Varian cokelat): kolom 'dampak' kosong
TIDAK DIHITUNG baris 3 (Varian keju): kolom 'jangkauan' bukan angka: 'banyak'
TIDAK DIHITUNG baris 5 (Box hampers): keyakinan harus 0-100 (persen)
```
Tiga baris rusak ditolak dengan alasan jelas, tidak ditebak. Baik.

## BUG ditemukan
"Tas kertas" keyakinan ditulis `0.9` (maksud pengguna 90%). Script menerimanya sebagai **0,9 persen**, skor 1,35 padahal seharusnya **135** (verifikasi: 300 x 0,5 x 0,9 / 1 = 135). Salah 100 kali lipat **tanpa peringatan**, dan ide ini justru jadi "Sekarang" hanya karena ide lain ditolak. Pengguna awam sering menulis keyakinan sebagai pecahan (0,8). Script sebaiknya menolak atau memperingatkan keyakinan 0 < k <= 1.

Uji tambahan data rusak (semua di scratchpad penguji):
- `"10,000"` (ribuan gaya Inggris) terbaca 10 (bukan 10.000) tanpa peringatan.
- Header Inggris (`name,reach,...`) hanya menghasilkan "kolom 'nama' kosong" - tidak menjelaskan bahwa nama kolom salah.
- `--kapasitas` dengan metode ICE diabaikan diam-diam.
- File non-UTF-8 (ekspor Excel lama), file kosong, folder sebagai path: ditolak dengan kode 2. Baik.

**Vonis: LULUS dengan bug** (alur tanya-sekali benar; validasi keyakinan pecahan bolong).
