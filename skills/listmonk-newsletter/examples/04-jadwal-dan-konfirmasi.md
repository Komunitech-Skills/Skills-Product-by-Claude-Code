# 04 - Jadwal dan gerbang konfirmasi (hasil nyata)

**Pengguna:** "Kirim sekarang aja ke semua." (belum diuji kirim)
```
$ listmonk.py kirim 3 --ya --konfirmasi-penerima 2
  list 'Newsletter Toko Uji' (opt-in double): 2 penerima
  Uji-kirim ke diri sendiri: BELUM / isi berubah sejak uji
DITOLAK: lakukan 'uji-kirim' ke email Anda sendiri dulu (isi harus sama persis).
```
Setelah uji kirim:
```
$ listmonk.py kirim 3
BELUM DIKIRIM. WAJIB tanya pengguna: 'Kirim ke sekitar 2 orang di list tsb? (ya/tidak)'. Bila ya: ulangi dengan --ya --konfirmasi-penerima 2
$ listmonk.py kirim 3 --ya --konfirmasi-penerima 99
DITOLAK: jumlah konfirmasi (99) tidak sama dengan perkiraan sekarang (2). Tunjukkan angka terbaru ke pengguna.
```
**Agent ke pengguna:** "Email ini akan dikirim ke sekitar 2 orang (yang sudah konfirmasi) di list 'Newsletter Toko Uji'. Subjek: ... Contoh sudah Anda terima. Kirim sekarang? (ya/tidak)" -> pengguna "ya" -> `--ya --konfirmasi-penerima 2`.

Jadwal: `jadwal 3 --waktu "2026-10-05 09:00" --tz WIB --ya --konfirmasi-penerima 2` -> "dijadwalkan 2026-10-05 09:00 WIB untuk sekitar 2 penerima. listmonk harus tetap menyala pada jam itu." Waktu lampau ditolak (kode 2). `batalkan 3 --ya` mengembalikan kampanye terjadwal ke draf.
