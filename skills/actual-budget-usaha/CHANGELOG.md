# Riwayat perubahan — actual-budget-usaha

Catatan teknis per versi.

## Catatan revisi 1.0.8 (2026-10-17)
- Contoh keluaran ringkasan di SKILL.md (bagian Format output) disamakan dengan keluaran skrip: baris Pajak tertulis "bawaan bulan lalu minus Rp 600.000", bukan "-Rp 600.000". Cara kerja tidak berubah.

## Catatan revisi 1.0.7 (2026-10-02)
- Aturan baru di SKILL.md: bila pengguna menempel kunci/token/password di chat, agent tidak boleh menulis ulang satu karakter pun darinya dan cukup menyebut "kunci yang Anda tempel".

## Catatan revisi 1.0.6 (2026-10-02)
- Temuan uji OpenClaw: usulan kategori kini dicocokkan ke kategori yang sudah ada di budget (mis. "Iklan & Promosi" menjadi "Iklan"), memakai kategori dari riwayat transaksi lama untuk penerima yang sama, dan nama penerima dirapikan (tanpa kode atau nomor referensi).
- Baris yang perlu dicek ditanyakan dalam satu pesan lewat bagian "PERTANYAAN UNTUK PENGGUNA" dari keluaran script (dikelompokkan, maksimal 5 pertanyaan). Versi script naik ke 1.0.6.

## Catatan revisi 1.0.5 (2026-10-01)
- Petunjuk lokasi script ditambahkan di SKILL.md: script ada di subfolder `scripts/` di folder skill. Agent dilarang mencari script atau file pengguna ke seluruh disk (mis. `find /`).

## Catatan revisi 1.0.4 (2026-09-29)
- Pengaman: singkatan opsi baris perintah tidak lagi diterima (mis. `--timp` tidak bisa dibaca sebagai opsi menimpa), sehingga file tidak tertimpa atau ditulis tanpa sengaja. Ditambah uji regresi.

## Catatan revisi 1.0.3 (2026-09-29)
- Baris "Aturan kerja" ditambahkan di SKILL.md: agent tidak boleh memasang paket/aplikasi sendiri, tidak membuka atau mencari file di luar yang diberikan pengguna, dan hasil yang ditulis ke file harus disebut lokasinya (folder kerja, bukan `/tmp`).

## Catatan revisi 1.0.2 (2026-09-29)
- Aturan kredensial & jadwal (SKILL.md dan `references/openclaw-jadwal.md`): agent tidak pernah mencari, membaca, atau menampilkan token/API key dari environment, file konfigurasi, atau riwayat. Jadwal hanya dibuat setelah pengguna membalas "ya" atas perintah dan jam yang ditunjukkan.

## Catatan revisi 1.0.1 (2026-09-26)
- Lulus uji; diuji dengan budget Actual 26.9.0 asli (dibuat lewat API resmi, data fiktif).
- Pembeda dengan `kas-umkm` dijelaskan: skill ini untuk pengguna yang memakai aplikasi Actual dan ingin anggaran per kategori, sedangkan `kas-umkm` untuk buku kas harian tanpa aplikasi. Bila pengguna hanya bilang "impor mutasi ini", agent bertanya sekali tujuannya.
- Setor tunai kini ditanyakan asalnya (hasil jualan yang belum tercatat = pemasukan; pindah dana sendiri = transfer); nominal di bawah Rp100 ditandai agar format angkanya diperiksa.

## Catatan revisi 1.0.0 (2026-09-26)
- Rilis awal (uji internal): asisten Actual Budget (aplikasi anggaran amplop gratis, data lokal) untuk freelancer dan usaha kecil. Mengubah mutasi bank BCA/BRI/Mandiri/BNI (CSV, angka format Indonesia) menjadi CSV impor Actual yang valid dengan usulan kategori dan daftar baris ragu, serta ringkasan anggaran bulanan.
