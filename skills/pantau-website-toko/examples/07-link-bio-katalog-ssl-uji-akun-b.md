# Contoh 7 (Uji Akun B): Link bio + katalog, `cek-cepat` dengan SSL bermasalah

**Permintaan pengguna:** "SSL link bio + katalog saya kapan habis ya, kok HP pelanggan sempat nunjukin peringatan?"

## Kasus A — sertifikat self-signed (masih berlaku, tapi tidak terpercaya)
Server HTTPS lokal buatan penguji dengan sertifikat **self-signed sungguhan** (dibuat `openssl req -x509`, masa berlaku 30 hari).
```bash
python3 scripts/pantau.py cek-cepat https://127.0.0.1:9301
```
```
CEK CEPAT: https://127.0.0.1:9301
HTTP    : 200 (OK)
Respons : 36.5 ms
SSL     : 29 hari lagi (kedaluwarsa 2026-10-26)  [PERINGATAN: sertifikat tidak terpercaya]
```
Verifikasi independen: `openssl x509 -in ss.crt -noout -enddate` → `notAfter=Oct 26 ... 2026 GMT`, selisih ke tanggal uji (26 Sep 2026) = 30 hari kalender, script menampilkan 29 (pembulatan `.days` ke bawah karena ada sisa jam) — **wajar dan benar**, bukan kesalahan hitung.

## Kasus B — sertifikat kedaluwarsa sungguhan
Server HTTPS lokal dengan sertifikat yang sengaja dibuat **sudah kedaluwarsa** (`notAfter` dipaksa ke 2 Januari 2020 lewat `openssl ca -startdate/-enddate`, bukan hanya sertifikat baru yang "dianggap" kedaluwarsa).
```bash
python3 scripts/pantau.py cek-cepat https://127.0.0.1:9302
```
```
CEK CEPAT: https://127.0.0.1:9302
HTTP    : 200 (OK)
Respons : 40.9 ms
SSL     : -2460 hari lagi (kedaluwarsa 2020-01-02)  <-- SEGERA PERPANJANG  [PERINGATAN: sertifikat tidak terpercaya]
```
Verifikasi independen: `openssl x509 -in exp.crt -noout -enddate` → `notAfter=Jan 2 00:00:00 2020 GMT`. Selisih hari dari 26 Sep 2026 ke 2 Jan 2020 ≈ 2460 hari — **cocok** dengan angka `-2460` yang ditampilkan (skill menampilkan angka negatif untuk sertifikat yang sudah lama kedaluwarsa, bukan menyembunyikannya).

**Catatan kualitas (minor, bukan bug):** pesan "SEGERA PERPANJANG" (dipicu saat `sisa_hari <= 14`) terasa terlalu halus untuk sertifikat yang sudah kedaluwarsa **2.460 hari** yang lalu — kalimatnya lebih cocok untuk kasus "akan habis 9 hari lagi". Tetap ditandai jelas lewat `[PERINGATAN: sertifikat tidak terpercaya]` di baris yang sama, jadi tidak menyesatkan, hanya kurang tegas nadanya untuk kasus ekstrem ini.

## Kasus C — dibandingkan dengan `ringkasan` via Uptime Kuma untuk sertifikat self-signed
Monitor HTTPS yang sama (self-signed, Kasus A) juga didaftarkan ke Uptime Kuma sungguhan dan dimasukkan ke status page. Hasilnya: monitor berstatus **TURUN** (karena Uptime Kuma sendiri menolak sertifikat tidak terpercaya secara default — `rejectUnauthorized: true` pada `httpsAgent`-nya) dan `certExpiryDaysRemaining` di endpoint publik **kosong** (kode sumber `server/model/monitor.js` baris ~290 hanya mengisi `certExpiryDaysRemaining` bila `tlsInfo.valid` bernilai true). **Temuan:** untuk sertifikat self-signed, mode `ringkasan` (lewat Uptime Kuma) **tidak akan pernah menampilkan sisa hari SSL** — berbeda dengan `cek-cepat` yang tetap menampilkannya (dengan tanda tidak terpercaya). Ini konsisten dengan desain Uptime Kuma sendiri, bukan bug skill, tapi **layak ditambahkan sebagai catatan** di SKILL.md/README bagian `ringkasan`, supaya pengguna yang websitenya masih pakai sertifikat self-signed tidak bingung kenapa sisa hari SSL tidak pernah muncul di ringkasan meski sudah mengaktifkan "Show Certificate Expiry".
