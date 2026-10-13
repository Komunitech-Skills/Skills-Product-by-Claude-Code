# Riwayat perubahan — absensi-lokal

Catatan teknis per versi (dipindah dari README agar halaman pembeli ringkas).

## Catatan revisi 1.0.7 (2026-10-03)
- Jalur baru "upah pekerja harian lepas" tanpa database (SKILL.md bagian F, `scripts/upah_harian.py`): menghitung upah mingguan/periode dari hari kerja, setengah hari, lembur, tambahan, dan potongan/kasbon yang diketik di chat. Tidak menyimpan apa pun.
- Lembur dicek terhadap minimum PP 35/2021 (upah sebulan = tarif harian x 25 untuk pola 6 hari atau x 21 untuk pola 5 hari, dibagi 173 per jam). Bila pemilik memakai tarif lembur sendiri yang lebih rendah dari minimum, script memberi peringatan dan menampilkan total versi minimum. `gaji-umkm` tetap untuk gaji bulanan. Uji `tests/uji_upah_harian.py`.

## Catatan revisi 1.0.6 (2026-10-01)
- Dari uji OpenClaw sebelum/sesudah: kini data karyawan selalu ditampilkan sebagai pratinjau dan baru disimpan setelah Anda membalas "ya"; tanggal yang kosong untuk semua karyawan ditandai "kemungkinan libur — konfirmasi" (bukan dianggap bolong per orang).

## Catatan revisi 1.0.5 (2026-10-01)
- Petunjuk lokasi script ditambahkan di SKILL.md: script ada di subfolder `scripts/` di folder skill. Agent dilarang mencari script atau file pengguna ke seluruh disk (mis. `find /`).

## Catatan revisi 1.0.4 (2026-09-29)
- Pengaman: singkatan opsi baris perintah tidak lagi diterima (mis. `--y` tidak bisa dibaca sebagai `--ya`), sehingga konfirmasi tidak terpicu tanpa sengaja. Ditambah uji regresi.

## Catatan revisi 1.0.3 (2026-09-29)
- Baris "Aturan kerja" ditambahkan di SKILL.md: agent tidak boleh memasang paket/aplikasi sendiri, tidak membuka atau mencari file di luar yang diberikan pengguna, dan hasil yang ditulis ke file harus disebut lokasinya (folder kerja, bukan `/tmp`).

## Catatan revisi 1.0.2 (2026-09-29)
- Aturan kredensial & jadwal (SKILL.md dan `references/openclaw-jadwal.md`): agent tidak pernah mencari, membaca, atau menampilkan token/API key dari environment, file konfigurasi, atau riwayat. Jadwal hanya dibuat setelah pengguna membalas "ya" atas perintah dan jam yang ditunjukkan.

## Catatan revisi 1.0.1 (2026-09-24)
- Versi saat skill pertama masuk repo (lolos uji muat OpenClaw). Perbaikan kecil; rincian di riwayat git.

## Catatan revisi 1.0.0 (sebelum 2026-09-24)
- Rilis awal (uji internal).
