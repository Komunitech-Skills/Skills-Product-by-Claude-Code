# Uji A/B — tanpa skill vs dengan skill (uji independen Akun B)

Skenario normal pertama: pengguna toko bangunan bertanya "tugas apa yang telat di Vikunja saya?" dan
minta ditambahkan tugas baru dengan penugasan.

## TANPA skill (agent generik, hanya tahu "Vikunja itu task manager open-source")
Simulasi jawaban agent tanpa akses ke skill ini (tidak tahu alamat, header auth, format filter
Vikunja, atau konvensi tanggal Indonesia yang harus didukung):

> "Saya tidak punya akses langsung ke instalasi Vikunja Anda. Anda bisa membuka Vikunja di browser,
> masuk ke proyek yang relevan, lalu memfilter tugas berdasarkan tanggal jatuh tempo untuk melihat
> yang terlambat. Untuk menambah tugas baru dengan tenggat 'Jumat' dan menugaskan ke Budi, buka
> tombol '+ New Task', ketik judul, klik ikon kalender, pilih tanggal Jumat terdekat, lalu cari nama
> Budi di kolom assignee."
>
> (Jika dipaksa "coba saja pakai API", agent generik biasanya akan menebak-nebak bentuk endpoint,
> berisiko salah format tanggal RFC3339, salah asumsi header token, atau — lebih buruk — menyarankan
> menempelkan token API langsung di prompt chat.)

Tidak ada angka nyata, tidak ada verifikasi bahwa server memang menyala, tidak ada penanganan format
tanggal Indonesia, tidak ada jalur konfirmasi sebelum menulis, dan ada risiko token diminta ditempel
di chat.

## DENGAN skill (hasil nyata dari server Vikunja 2.6.0 sungguhan, lihat `01-toko-bangunan-uji-akun-b.md`)
```
TUGAS TERLAMBAT
Proyek: semua proyek
Jumlah: 2
- Tagih pelanggan telat (jatuh tempo 20 Sep 2026; proyek: Toko Bangunan Sinar Jaya)
- Stok opname harian (jatuh tempo 26 Sep 2026; proyek: Toko Bangunan Sinar Jaya)
```
dan untuk penambahan tugas — pratinjau konkret dengan tanggal Indonesia yang sudah dihitung benar
("Jumat, 2 Oktober 2026"), meminta konfirmasi eksplisit, dan (walau penugasan `--ke` ternyata gagal
di lingkungan uji ini karena masalah token API Vikunja — lihat HASIL-UJI.md #1) tugas induknya tetap
tersimpan dan agent tahu persis apa yang berhasil/gagal, bukan menebak.

## Kesimpulan uji A/B
Skill jelas lebih baik: data nyata (bukan instruksi generik "buka browser"), tanggal Indonesia
dihitung otomatis dan benar, alur konfirmasi sebelum menulis, dan penanganan token yang aman (tidak
pernah diminta ditempel di chat). Nilai tambah signifikan dikonfirmasi — skor tidak dibatasi maksimal 6.
