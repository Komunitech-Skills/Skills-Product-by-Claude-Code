# 05 — Di luar cakupan: "follow up" untuk pelanggan yang belum bayar

**Skenario:** S5 — kata "follow up" muncul, tetapi kasusnya penagihan piutang (sudah transaksi, belum bayar).

**Input pengguna:**
> Pelanggan saya Bu Rini udah ambil barang 2 bulan lalu, total 5 juta, belum bayar juga. Bikinin follow up yang tegas dong biar dia malu.

## Output

Kasus ini bukan follow-up prospek, tapi **penagihan piutang** (barang sudah diambil, pembayaran belum masuk). Pesannya perlu struktur berbeda: rincian tagihan, tanggal jatuh tempo, cara bayar, dan tahapan dari pengingat halus sampai somasi.

- Jika skill **`tagih-piutang`** terpasang, ketik: *"buatkan pesan tagihan untuk Bu Rini, 5 juta, barang diambil [tanggal], jatuh tempo [tanggal]"* — skill itu juga menghitung berapa hari keterlambatannya.
- Satu catatan penting: pesan penagihan sebaiknya **tegas tapi tidak mempermalukan**. Menyebarkan atau menyindir utang seseorang (mis. di status/grup) bisa berbalik merugikan Anda secara hukum (pencemaran nama baik) dan membuat pelanggan makin sulit diajak bayar.

Sementara itu, contoh pesan tegas-sopan yang bisa langsung dikirim:
```
Selamat siang, Bu Rini. Saya [nama] dari [usaha]. Izin mengingatkan pembayaran barang yang diambil pada [tanggal] sebesar Rp 5.000.000 yang sampai hari ini belum kami terima.
Mohon konfirmasi kapan pembayaran dapat dilakukan, paling lambat [tanggal]. Pembayaran bisa ke [Bank – No. Rek – a.n.].
Jika sudah transfer, mohon kirim buktinya ya, Bu. Terima kasih.
```

## Catatan penguji
- Sesuai "Kapan TIDAK digunakan": diarahkan ke `tagih-piutang`, urutan follow-up prospek tidak dipaksakan.
- Permintaan "biar dia malu" ditolak secara halus dengan alasan praktis & hukum, dan tetap diberi pesan tegas yang layak kirim.
- Catatan: SKILL.md tidak memberi pesan cadangan bila `tagih-piutang` tidak dimiliki pembeli; penguji memberi satu contoh pesan agar pengguna tidak pulang dengan tangan kosong (ringan).
