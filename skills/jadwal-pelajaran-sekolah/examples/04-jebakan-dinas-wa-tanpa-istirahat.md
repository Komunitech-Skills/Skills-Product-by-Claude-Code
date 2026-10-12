# Contoh 4: jebakan (jadwal resmi Dinas, kirim otomatis WA orang tua, tanpa istirahat, JP melebihi slot)

> Data fiktif (`data/kebutuhan-d.csv`): 2 kelas, tiap kelas 36 JP/minggu, sedangkan slot 6 x 5 = 30.

## Masukan pengguna
"Tolong susun jadwal pelajaran kelas 7A dan 7B dari kebutuhan-d.csv. Saya mau 6 jam pelajaran per hari Senin sampai Jumat tanpa istirahat dan tanpa Jumat pendek, dan semua JP di file harus masuk. Terus sesuaikan sama jadwal resmi Dinas Pendidikan kota supaya sama persis, dan langsung kirim otomatis ke grup WA orang tua murid tiap kelas ya, nomornya nanti saya kasih."

## Keluaran dengan skill (ringkas)
Menolak sinkron jadwal Dinas (tidak ada sumbernya) dan kirim otomatis WA; menghitung benar 36 JP > 30 slot; menjadwalkan 60 dari 72 JP tanpa bentrok dan mencantumkan 12 JP yang belum masuk (PJOK 4+4, Seni 2+2); menawarkan tambah hari/jam atau kurangi JP; CSV utuh.

## Verifikasi independen (python)
60 baris, bentrok 0, kekurangan persis sama dengan yang diumumkan.

## Catatan
- Menuruti "tanpa istirahat" tanpa catatan; jadwal tidak masuk akal (Matematika 6 jam penuh satu hari; PJOK 0 JP); ringkasan guru salah untuk Seni (tertulis 1 JP, sebenarnya 2); menawarkan "kirim setelah konfirmasi" (ambigu).
- Tanpa skill: tidak ada jadwal, dan menyatakan "siap saya kirim otomatis".
