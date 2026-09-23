# Skenario 2 — Normal: Software Kasir Resto + skor dari CSV

## Input pengguna
```
Siapa target pasar ideal untuk software kasir buat resto? Saya juga sudah punya
daftar 5 calon klien yang sudah saya nilai sendiri (0-5) untuk kecocokan profil,
kebutuhan, kemampuan bayar, dan akses ke pemilik/manajernya. Ini datanya (CSV):

Nama Resto,Cocok ICP,Kebutuhan,Kemampuan Bayar,Akses PIC
Resto Sedap Rasa,5,5,4,4
Warung Nasi Padang Sederhana,2,3,1,2
Kafe Kopi Senja,4,4,3,5
Resto Steak House Premium,5,3,5,3
Angkringan Mas Joko,1,2,1,1

Tolong urutkan mana yang paling prioritas dihubungi.
```

## Output

```
## Profil Pelanggan Ideal (ICP)
Resto/kafe skala kecil-menengah dengan transaksi harian cukup ramai (bukan
sekadar 1-2 kasir manual), masih pakai nota manual/Excel atau software kasir
lama yang menyulitkan laporan penjualan. Pengambil keputusan: pemilik langsung
(usaha kecil) atau manajer operasional (resto dengan beberapa cabang).
Kemampuan bayar: sanggup biaya langganan bulanan software kasir.

## Skor Kualifikasi Prospek
(dihitung dengan scripts/skor_prospek.py dari data yang Anda kirim, bobot default
cocok ICP 30% / kebutuhan 30% / kemampuan bayar 20% / akses PIC 20%)

| Nama | Skor | Kategori |
|---|---|---|
| Resto Sedap Rasa | 92.0 | Panas |
| Kafe Kopi Senja | 80.0 | Panas |
| Resto Steak House Premium | 80.0 | Panas |
| Warung Nasi Padang Sederhana | 42.0 | Dingin |
| Angkringan Mas Joko | 26.0 | Dingin |

Semua 5 baris berhasil dihitung, tidak ada baris dilewati.

### Panas (segera hubungi)
1. **Resto Sedap Rasa** (92.0) — cocok ICP & kebutuhan sama-sama tinggi (5/5),
   kemampuan bayar dan akses PIC juga baik. Prioritas #1.
2. **Kafe Kopi Senja** (80.0) — akses ke PIC paling mudah (5/5) meski kemampuan
   bayar sedang; cocok untuk didekati lebih dulu karena mudah dijangkau.
3. **Resto Steak House Premium** (80.0) — kemampuan bayar tertinggi (5/5) tapi
   kebutuhan & akses PIC sedang; perlu pendekatan lebih personal ke pengambil
   keputusan.

### Hangat
- (tidak ada di daftar ini)

### Dingin (prioritas rendah/lewati dulu)
- Warung Nasi Padang Sederhana (42.0), Angkringan Mas Joko (26.0) — kemampuan
  bayar & kecocokan ICP rendah, kemungkinan skala usaha terlalu kecil untuk
  software berbayar bulanan. Bisa dicoba lagi nanti kalau ada paket harga lebih
  murah, tapi bukan prioritas sekarang.

## Pesan Pembuka (WA, untuk prospek Panas #1: Resto Sedap Rasa)
Selamat siang Pak/Bu, perkenalkan saya [Nama Anda] dari [Nama Usaha Software
Kasir]. Kami menyediakan software kasir untuk resto yang memudahkan pencatatan
transaksi dan laporan penjualan harian. Kalau Resto Sedap Rasa saat ini masih
pakai pencatatan manual/Excel dan tertarik lihat demo singkat, boleh saya
kirimkan infonya? Mohon maaf mengganggu, boleh diabaikan bila belum relevan.

## Catatan Kepatuhan UU PDP
Pastikan kontak PIC (pemilik/manajer resto) yang dipakai adalah kontak bisnis
yang memang dipublikasikan resto tersebut (nomor WA bisnis, telepon di Google
Maps/website), bukan nomor pribadi yang didapat tanpa konteks bisnis.
Sertakan identitas pengirim jelas dan opsi berhenti dihubungi di setiap pesan.

## Asumsi
- Skor dihitung dari nilai 0-5 yang sudah Anda berikan sendiri di CSV (bukan
  dinilai otomatis oleh skill) — bobot dipakai bobot default karena tidak
  disebutkan prioritas berbeda
```

## Catatan penguji
- Tabel skor & kategori (92.0/80.0/80.0/42.0/26.0, 3 Panas 0 Hangat 2 Dingin)
  cocok persis dengan output script `skor_prospek.py` dan perhitungan manual
  independen (lihat `HASIL-UJI.md`).
- **Baik:** dua prospek dengan skor sama persis (80.0, Kafe Kopi Senja & Steak
  House) tetap dibedakan penjelasan kualitatifnya (akses PIC vs kemampuan bayar)
  alih-alih hanya menampilkan angka kosong — nilai tambah dibanding sekadar
  cetak tabel mentah.
- Tidak ada cacat berat/sedang. Cacat ringan: SKILL.md tidak menjelaskan cara
  menangani skor yang sama persis (tie-breaking) — perilaku baik di atas murni
  inisiatif agent, bukan instruksi eksplisit. Saran: boleh ditambahkan satu
  baris di format output "jika skor sama, urutkan berdasarkan kemudahan akses
  PIC lebih dulu" agar konsisten antar sesi, tapi dampaknya kecil.
