# Contoh 5 (Uji Akun B — penguji independen): Toko online sendiri, ringkasan via Uptime Kuma

**Konteks pengujian.** Uptime Kuma **2.5.5 ASLI** (rilis resmi, `git checkout 2.5.5` + `npm run setup`, dijalankan sungguhan terikat `127.0.0.1:3101`) dipasang dari nol di scratchpad penguji (terpisah dari sesi pembuat skill). Dibuat: akun admin, monitor "Toko Online - Beranda" (mengarah ke server HTTP lokal buatan penguji, selalu 200) dan monitor "Halaman Checkout (sengaja mati - uji)" (mengarah ke port yang sengaja tidak dibuka, `ECONNREFUSED`), dikelompokkan ke status page `toko-saya-uji-b` dan **dipublikasikan**.

**Permintaan pengguna:** "Ringkas status website toko saya."

**Perintah:**
```bash
python3 scripts/pantau.py ringkasan --status-url http://127.0.0.1:3101/status/toko-saya-uji-b --log /tmp/uji-b-log.jsonl
```

**Keluaran nyata (disalin apa adanya):**
```
RINGKASAN STATUS - Toko Saya (Uji B) (toko-saya-uji-b)
Diperiksa: 2026-09-26T16:40:17.919072+00:00 UTC
------------------------------------------------------------
[OK] Toko Online - Beranda  (grup: Utama)
     Status sekarang : AKTIF, ping 4 ms
     Uptime 24 jam   : 100% (dihitung Uptime Kuma sendiri)
     Terlihat TURUN dalam 14 cek terakhir yang terbaca (2026-09-26T16:35:41.552000+00:00 s/d 2026-09-26T16:40:01.567000+00:00 UTC): 0x, total 0.0 menit (HANYA jendela ini, bukan seluruh hari/minggu)

[!!] Halaman Checkout (sengaja mati - uji)  (grup: Utama)
     Status sekarang : TURUN
     Uptime 24 jam   : 0% (dihitung Uptime Kuma sendiri)
     Terlihat TURUN dalam 14 cek terakhir yang terbaca (2026-09-26T16:35:41.589000+00:00 s/d 2026-09-26T16:40:01.597000+00:00 UTC): 14x, total 4.6 menit (HANYA jendela ini, bukan seluruh hari/minggu)
```
(baris monitor ke-3 "SSL Cek" dipotong di sini — dibahas di `09-...`; contoh SSL lengkap ada di `07-...`)

## Verifikasi independen (bukan dari script)
Penguji mengambil `GET /api/status-page/heartbeat/toko-saya-uji-b` mentah dan menghitung sendiri di Python terpisah (tanpa memanggil `pantau.py`):
- Monitor "Toko Online - Beranda": 14 titik heartbeat, semua `status=1` (UP) → downtime jendela = **0.0 menit**. Cocok dengan keluaran script.
- Monitor "Halaman Checkout": 14 titik, semua `status=0` (DOWN) → durasi dihitung manual `Σ (waktu_titik_berikutnya - waktu_titik_ini)` untuk tiap titik DOWN (titik terakhir pakai waktu "sekarang") = **4.74 menit** pada saat verifikasi (beberapa detik setelah script berjalan, sehingga sedikit lebih besar dari 4.6 menit yang dicatat script — wajar karena "sekarang" bergerak maju; bila dihitung ulang persis pada waktu yang sama dengan run script, angkanya identik).
- `uptimeList["1_24"] = 1` dan `["2_24"] = 0` dari field resmi Uptime Kuma sendiri — skill **tidak** menghitung ulang angka ini (sesuai klaim SKILL.md), hanya meneruskan apa adanya. Dikonfirmasi field ini benar sesuai data heartbeat (monitor 1 100% up, monitor 2 100% down dalam window yang direkam).

**Kesimpulan verifikasi:** perhitungan durasi TURUN, jumlah kejadian TURUN, dan uptime 24 jam **akurat** dan sesuai penjelasan di SKILL.md (jendela ±100 titik terakhir, bukan angka harian penuh). Tidak ditemukan angka yang dikarang/diperkirakan.

## Log mingguan
Setelah `ringkasan` dijalankan 3x berturut-turut (log terpisah `/tmp/uji-b-log.jsonl`, 9 baris = 3 monitor × 3 kali), `mingguan --hari 7` menghasilkan rata-rata 100.0% / 0.0% / 0.0% — cocok dengan rata-rata manual (semua observasi identik karena dijalankan dalam rentang beberapa detik, jadi rata-ratanya trivial sama dengan nilai tunggalnya; formula `sum/len` di kode sudah diperiksa benar).
