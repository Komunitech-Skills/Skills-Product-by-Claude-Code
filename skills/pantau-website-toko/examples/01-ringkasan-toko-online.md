# Contoh 1: Ringkasan status toko online (dengan Uptime Kuma)

**Permintaan pengguna:** "Ringkas status website toko saya."

**Konteks:** pengguna sudah memasang Uptime Kuma, menambahkan monitor "Toko Online" (website utama)
dan "WA Katalog" (link WA), lalu mempublikasikan status page dengan slug `toko-scenario2` dan
mengaktifkan "Show Certificate Expiry". (Data uji: `tests/fixtures/skenario2-*.json`, dibuat tangan
Komunitech untuk menguji jalur kode status AKTIF/ping/SSL yang tidak muncul di rekaman Uptime Kuma
2.5.5 asli — lihat `ATTRIBUTION.md`.)

**Perintah yang dijalankan agent:**
```bash
python3 scripts/pantau.py ringkasan --status-url http://127.0.0.1:PORT/status/toko-scenario2 --tanpa-log
```

**Keluaran nyata (dijalankan sungguhan terhadap server tiruan berisi data di atas):**
```
RINGKASAN STATUS - Toko Scenario2 (toko-scenario2)
Diperiksa: 2026-09-26T16:29:10.942122+00:00 UTC
------------------------------------------------------------
[OK] Toko Online  (grup: Utama)
     Status sekarang : AKTIF, ping 240 ms
     Uptime 24 jam   : 95.0% (dihitung Uptime Kuma sendiri)
     Terlihat TURUN dalam 5 cek terakhir yang terbaca (2026-09-26T08:00:00+00:00 s/d 2026-09-26T08:20:00+00:00 UTC): 2x, total 10.0 menit (HANYA jendela ini, bukan seluruh hari/minggu)
     Sertifikat SSL  : 9 hari lagi  <-- SEGERA PERPANJANG

[OK] WA Katalog  (grup: Utama)
     Status sekarang : AKTIF, ping 82 ms
     Uptime 24 jam   : 100.0% (dihitung Uptime Kuma sendiri)
     Terlihat TURUN dalam 3 cek terakhir yang terbaca (2026-09-26T08:00:00+00:00 s/d 2026-09-26T08:10:00+00:00 UTC): 0x, total 0.0 menit (HANYA jendela ini, bukan seluruh hari/minggu)
     Sertifikat SSL  : 120 hari lagi

Catatan: 'Uptime 24 jam' & sertifikat SSL diambil apa adanya dari Uptime Kuma (sisa hari SSL hanya tampil bila 'Show Certificate Expiry' aktif di status page & monitornya https). Ringkasan mingguan lihat perintah 'mingguan' (baca log lokal skill ini).
```

**Jawaban agent ke pengguna (contoh):**
> Status website Anda hari ini AKTIF semua. Yang perlu diperhatikan: **sertifikat SSL "Toko Online" tinggal 9 hari lagi — segera perpanjang** sebelum kedaluwarsa (kalau habis, browser pengunjung akan menampilkan peringatan "Not Secure"). Dalam beberapa jam terakhir yang terekam, "Toko Online" sempat turun 2x total 10 menit; "WA Katalog" tidak ada masalah. (Catatan: ini hanya jendela beberapa jam terakhir yang terbaca, bukan rangkuman satu hari penuh — jalankan "ringkasan mingguan" setelah beberapa hari untuk gambaran lebih luas.)
