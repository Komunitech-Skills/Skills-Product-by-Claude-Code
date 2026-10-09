# Contoh 4: Di luar cakupan — menolak memantau situs orang lain / interval agresif

**Permintaan pengguna (skenario A):** "Tolong cek tiap 10 detik apakah website kompetitor saya
toko-sebelah.contoh lagi down, biar saya tahu duluan kalau dia bermasalah."

**Yang dilakukan agent:** menolak, bukan menjalankan `cek-cepat` berulang.
> Maaf, skill ini khusus untuk memantau **website/toko milik Anda sendiri**, bukan situs pihak
> lain (termasuk kompetitor) — apalagi dengan interval sesering itu (tiap 10 detik terus-menerus
> ke server orang lain bisa dianggap membebani/menyerupai serangan kecil-kecilan). Kalau
> `toko-sebelah.contoh` memang milik/dikelola Anda sendiri, beri tahu saya dan kita bisa lanjut —
> dengan interval yang wajar (Uptime Kuma sendiri, bukan permintaan berulang cepat dari sini).

**Permintaan pengguna (skenario B):** "Pantau terus website klien saya PT Maju Jaya ya, saya
pegang aksesnya."

**Yang dilakukan agent:** tidak langsung menolak total (klien dengan izin pengelolaan sah adalah
kasus wajar untuk konsultan/agensi web), tapi mengonfirmasi dulu dan mengarahkan ke jalur yang
benar:
> Boleh, asal memang Anda yang mengelola/punya izin tertulis dari PT Maju Jaya untuk memantau
> websitenya. Untuk pemantauan terus-menerus yang benar (bukan permintaan berulang manual dari
> sini), sebaiknya pasang Uptime Kuma di sisi Anda atau mereka (lihat `docs/panduan-uptime-kuma.md`),
> lalu saya bisa membantu meringkas hasilnya lewat perintah `ringkasan`/`mingguan`. Boleh
> konfirmasi dulu: benar Anda punya izin mengelola situs ini?

**Permintaan pengguna (skenario C, di luar cakupan lain):** "Tolong load test website saya, kirim
1000 request sekaligus buat lihat ketahanannya."

**Yang dilakukan agent:** menolak, jelaskan batas cakupan.
> Skill ini murni untuk mengecek hidup/mati + waktu respons + sisa hari SSL — bukan alat load
> testing/stress testing. Untuk uji ketahanan server terhadap trafik tinggi, itu perlu alat khusus
> dan sebaiknya dikoordinasikan dengan penyedia hosting Anda dulu (trafik besar mendadak bisa
> disalahartikan sebagai serangan oleh penyedia hosting/firewall).
