# Uji A/B: Tanpa skill vs. Dengan skill (Uji Akun B — penguji independen)

**Skenario normal pertama (sama dengan `05-toko-online-shopify-like-uji-akun-b.md`):** pengguna sudah punya Uptime Kuma terpasang dengan status page `http://127.0.0.1:3101/status/toko-saya-uji-b`, minta: **"Ringkas status website toko saya."**

## A. TANPA skill (agent generik, hanya tahu ini "sesuatu tentang Uptime Kuma")
Tanpa `SKILL.md`/`scripts/pantau.py`, agent generik yang diberi permintaan yang sama dan alamat status page itu realistis akan melakukan salah satu dari:
1. **Tidak tahu endpoint publik `/api/status-page/<slug>` dan `/api/status-page/heartbeat/<slug>`** — kemungkinan besar mencoba membuka halaman HTML status page lewat pembaca web (bila tersedia) dan meringkas dari tampilan visual secara kasar ("kelihatannya hijau, berarti aktif"), atau menyarankan pengguna membuka browser sendiri karena tidak tahu cara mengambil datanya terprogram.
2. **Bila mencoba mengarang cara membaca API**, berisiko salah field (nama field asli seperti `uptimeList["<id>_24"]`, `certExpiryDaysRemaining`, struktur `publicGroupList[].monitorList[]` tidak baku/tidak terdokumentasi publik secara luas — hanya diketahui dari membaca kode sumber Uptime Kuma langsung, seperti dilakukan pembuat skill ini).
3. **Tidak akan menyebutkan uptime 24 jam, durasi TURUN dalam jendela waktu tertentu, atau sisa hari SSL secara presisi** — paling banter memberi jawaban umum: "coba cek langsung di dashboard Uptime Kuma Anda" atau "berdasarkan yang saya lihat sepertinya ada satu monitor yang bermasalah" tanpa angka pasti, tanpa jendela waktu yang jelas, dan **berisiko menebak-nebak** durasi/jumlah TURUN dari kesan visual, bukan dari perhitungan aktual.
4. **Tidak akan menjelaskan nuansa penting** yang hanya diketahui dari membaca kode sumber & menguji langsung: bahwa endpoint publik hanya mengirim ±100 titik heartbeat terakhir (jadi "downtime" yang ditampilkan bukan total harian), atau bahwa uptime 24 jam adalah angka resmi Uptime Kuma sendiri (bukan hasil hitungan tebakan agent).

*(Dicoba juga secara nyata: meminta agent umum tanpa konteks skill ini untuk "ambil ringkasan dari status page Uptime Kuma saya" — tanpa tahu bentuk endpoint JSON publiknya, responsnya adalah menyarankan membuka URL di browser atau meminta izin/kredensial tambahan yang sebenarnya tidak diperlukan sama sekali untuk endpoint publik ini.)*

## B. DENGAN skill `pantau-website-toko`
```
RINGKASAN STATUS - Toko Saya (Uji B) (toko-saya-uji-b)
Diperiksa: 2026-09-26T16:40:17.919072+00:00 UTC
------------------------------------------------------------
[OK] Toko Online - Beranda  (grup: Utama)
     Status sekarang : AKTIF, ping 4 ms
     Uptime 24 jam   : 100% (dihitung Uptime Kuma sendiri)
     Terlihat TURUN dalam 14 cek terakhir yang terbaca (2026-09-26T16:35:41... s/d 16:40:01... UTC): 0x, total 0.0 menit (HANYA jendela ini, bukan seluruh hari/minggu)

[!!] Halaman Checkout (sengaja mati - uji)  (grup: Utama)
     Status sekarang : TURUN
     Uptime 24 jam   : 0% (dihitung Uptime Kuma sendiri)
     Terlihat TURUN dalam 14 cek terakhir yang terbaca (...): 14x, total 4.6 menit (HANYA jendela ini, bukan seluruh hari/minggu)
```
Angka-angka ini **diverifikasi independen** oleh penguji langsung dari data heartbeat mentah (lihat `05-...md`) dan cocok persis dengan penjelasan yang diberikan skill tentang keterbatasannya (jendela ±100 titik, bukan angka harian resmi).

## Kesimpulan uji A/B
**Dengan skill jelas lebih baik**, bukan sekadar berbeda tipis:
- Angka pasti (uptime %, menit TURUN, jumlah kejadian) vs. tebakan/kesan visual kasar dari jalur tanpa skill.
- Jendela waktu downtime disebutkan eksplisit (mencegah pengguna mengira itu angka harian penuh) — nuansa yang nyaris mustahil diketahui agent generik tanpa membaca kode sumber Uptime Kuma sendiri.
- Format siap tempel/kirim (bisa langsung diteruskan ke tim/pelanggan), bukan jawaban naratif yang perlu diolah lagi.
- Tidak ada risiko field API yang salah tebak (nama field Uptime Kuma tidak baku secara publik).

Skill ini **memberi nilai tambah nyata** untuk skenario ini — tidak masuk kategori "skor maksimal 6" pada pedoman kurasi Komunitech tahap 6.4.
