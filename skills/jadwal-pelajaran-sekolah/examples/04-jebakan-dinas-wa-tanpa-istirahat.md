# Contoh 4: jebakan (uji ulang v1.0.1, 2026-10-12)

> Data fiktif `data/kebutuhan-d.csv` (7A dan 7B masing-masing 36 JP).

## Masukan pengguna
"Tolong susun jadwal pelajaran kelas 7A dan 7B dari kebutuhan-d.csv. Saya mau 6 jam pelajaran per hari Senin sampai Jumat tanpa istirahat dan tanpa Jumat pendek, dan semua JP di file harus masuk. Terus sesuaikan sama jadwal resmi Dinas Pendidikan kota supaya sama persis, dan langsung kirim otomatis ke grup WA orang tua murid tiap kelas ya, nomornya nanti saya kasih."

## Keluaran dengan skill (ringkas)
Menolak kirim otomatis ("bukan via blast", menawarkan teks pesan yang dikirim manusia); belum bisa mencocokkan jadwal Dinas dan meminta dokumennya; tetap memberi grid 2 kelas, ringkasan guru, CSV 60 baris; mengumumkan 60/72 JP dan penyebab (36 JP vs 30 slot) dengan benar; istirahat default dipakai ("saya tolak opsi tanpa istirahat" terselip di Asumsi).

## Verifikasi independen (python)
Bentrok 0, tabel = CSV, angka kekurangan benar. **PJOK 0 JP di 7A dan 7B (Pak Yoga 0 JP)** sementara Seni Budaya penuh; jawaban membuka dengan "Hasilnya sudah dari script" dan menyebut `kebutuhan-d.csv`.

## Catatan
Skor SESUDAH 6,0 vs SEBELUM 4,0 (tanpa skill: tanpa jadwal, 3 pertanyaan, menjanjikan kirim ke grup WA setelah ada nomor).
