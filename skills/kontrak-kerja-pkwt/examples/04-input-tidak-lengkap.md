# Uji 04 — Input tidak lengkap: "bikinin kontrak karyawan dong"

> Penguji independen, 25 September 2026.

## Input pengguna
> "bikinin kontrak karyawan dong"

## Proses agent
- Pemicu cocok (mode Susun), tetapi tidak jelas **kontrak (PKWT) atau tetap (PKWTT)** dan tidak ada data sama sekali.
- SKILL.md: "Tanyakan **sekali** dalam satu pesan bernomor, maksimal 8 butir". Tidak ada angka → script belum dijalankan (tidak mengarang tanggal/upah).
- Ditambah satu pertanyaan penentu cakupan (kontrak atau tetap) digabung ke butir 4 agar tetap ≤ 8 butir.

## Output agent

Siap, saya bantu buatkan. Skill ini untuk **karyawan kontrak (PKWT)**. Kalau yang dimaksud karyawan **tetap**, beri tahu saja; untuk itu saya jelaskan bedanya dan sarankan dicek ke konsultan/Disnaker.

Supaya kontraknya tepat, mohon isi yang Anda tahu (yang kosong akan saya beri tanda [isi: ...]):
1. Nama usaha, jenis usaha, alamat, dan nama + jabatan penanda tangan
2. Nama pekerja (NIK/alamat boleh diisi sendiri nanti)
3. Jabatan & tugas utamanya
4. Kenapa pekerjaan ini kontrak, bukan tetap? (proyek, musiman, produk baru, pengganti sementara, dll.)
5. Tanggal mulai & lama kontrak (atau "sampai proyek X selesai"); apakah ini perpanjangan? sejak kapan kontrak pertama?
6. Gaji pokok + tunjangan tetap per bulan (atau upah harian), tanggal gajian
7. Hari & jam kerja
8. Kota/kabupaten tempat kerja dan UMK-nya tahun ini (bila tahu)

Kalau ingin cepat, jawab saja yang Anda tahu (mis. "barista, 1 tahun mulai 1 November, gaji 4 juta, di Depok"), sisanya saya tandai untuk diisi. Satu hal perlu diketahui dari awal: kontrak PKWT **tidak boleh memakai masa percobaan**.

## Uji lanjutan: pengguna menjawab minim
> "kasir, 1 tahun, gaji 3,5jt, langsung buatin aja"

Agent: membuat draf dengan `[isi: ...]` untuk nama usaha, pekerja, tanggal mulai, kota/UMK, jam kerja; menjalankan script **hanya setelah** ada tanggal mulai. Karena tanggal mulai tidak ada, agent **tidak** mengarang tanggal: menulis "Perkiraan kompensasi 12 bulan = 1 × upah = Rp3.500.000" (rumus 12 bulan tidak bergantung tanggal) dan menandai tanggal `[isi]`. Agent juga memberi peringatan 🔴 bahwa **kasir** umumnya pekerjaan tetap (checklist A2) dan meminta alasan sementara sebelum draf final.

Verifikasi: 12/12 × 3.500.000 = 3.500.000 ✅ (script: `--periode "1 Januari 2027 s.d. 31 Desember 2027" --upah 3,5jt` → Rp3.500.000, dijalankan penguji hanya untuk cek rumus).

## Penilaian
Lulus. Pertanyaan sekali, bernomor, ≤ 8 butir, bahasa awam, ada jalur cepat, tidak mengarang data. Catatan kecil: SKILL.md tidak menyebut apa yang dilakukan bila **tanggal mulai** tidak diketahui padahal script mewajibkan `--periode` — agent menanganinya sendiri; sebaiknya dieksplisitkan.
