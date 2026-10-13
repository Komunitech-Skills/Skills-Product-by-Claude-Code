# Riwayat perubahan — laporan-harian-usaha

Catatan teknis per versi.

## Catatan revisi 1.1.4 (2026-10-01)
- Petunjuk lokasi script ditambahkan di SKILL.md: script ada di subfolder `scripts/` di folder skill. Agent dilarang mencari script atau file pengguna ke seluruh disk (mis. `find /`).

## Catatan revisi 1.1.3 (2026-09-29)
- Gerbang konfirmasi jadwal dipertegas (hasil uji pengamanan): perintah persis, jam, zona waktu, dan tujuan harus ditunjukkan dulu, lalu agent berhenti menunggu jawaban "ya" di pesan berikutnya. Permintaan awal ("kirim tiap jam 9 malam") tidak dianggap persetujuan.
- Baris "Aturan kerja" ditambahkan: tidak memasang paket/aplikasi sendiri, tidak membuka file di luar yang diberikan, hasil disimpan di folder kerja (bukan `/tmp`).

## Catatan revisi 1.1.2 (2026-09-29)
- Aturan keras baru di SKILL.md dan `references/openclaw-jadwal.md`: agent tidak boleh mencari, membaca, atau menampilkan token/API key dari environment, file konfigurasi, atau riwayat. Kanal Telegram disiapkan sendiri oleh pengguna; bila kanal belum siap atau `automations add` ditolak, agent berhenti dan memberi langkah persiapan.
- Pembuatan jadwal wajib melalui gerbang konfirmasi ("Lanjut? ya/tidak"). Versi script naik ke 1.1.2.

## Catatan revisi 1.1.1 (2026-09-26)
- Perawatan temuan rendah/kosmetik dari uji sebelumnya. Tidak ada fitur baru dan tidak ada angka yang berubah (omzet, uang diterima, stok, kehadiran, tagihan, prospek).
- Peringatan "belum absen tanpa keterangan" tidak lagi muncul sebelum jam masuk shift paling awal walau sebagian karyawan sudah absen.
- Cek yang terlewati karena struktur tabel berubah kini ikut tampil di bagian PERLU PERHATIAN (sebelumnya diam).
- Nota kasir yang dibatalkan (void) setelah diimpor ke buku-stok kini diingatkan beserta langkah memperbaikinya.
- Catatan status di `references/openclaw-jadwal.md` diperbarui. Uji regresi menjadi 53 tes.

## Catatan revisi 1.1.0 (2026-09-25)
- Bagian PROSPEK dari `crm-wa` ditambahkan ke laporan (prospek baru, deal, konversi).
- Setelah uji independen (8/10), label diperjelas: "Deal periode ini (termasuk dari prospek lama)" dan "Konversi prospek baru periode ini", dengan penjelasan di Aturan hitung.

## Catatan revisi 1.0.1 (2026-09-24)
- Perbaikan dari uji independen: impor sebagian kasir ke buku-stok kini terdeteksi (mis. "3 dari 5 nota kasir belum diimpor ke buku-stok").
- Penerima laporan selain pemilik diperbolehkan hanya bila pemilik menunjuknya secara eksplisit, masing-masing di chat pribadi (bukan grup). Uji ulang 9/10.

## Catatan revisi 1.0.0 (2026-09-24)
- Rilis awal (uji internal): laporan harian/mingguan gabungan dari kasir, stok, absensi, dan pengingat; hanya membaca lewat salinan database.
