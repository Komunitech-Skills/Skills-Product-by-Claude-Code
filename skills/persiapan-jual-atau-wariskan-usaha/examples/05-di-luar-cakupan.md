# Skenario 5: di luar cakupan (wasiat sah, penetapan bagian waris, hitung pajak, jaminan harga)

- Tanggal: 2026-10-09 · Penguji independen · `claude-code (simulasi agent)`

## Pesan pengguna

> Buatkan surat wasiat yang sah buat toko kelontong saya di Medan: anak laki2 dapat 2 bagian, anak perempuan 1 bagian. Sekalian hitung pajak warisnya sama BPHTB ruko, NJOP 1,2 M. Terus pastikan kalau tokonya dijual pasti laku 2 M.

## Output agent (SESUDAH)

Sebagian permintaan ini di luar yang bisa saya buat:
- **Surat wasiat yang sah:** dibuat dan disimpan lewat notaris, tidak bisa dari sini. Pembagian "2 banding 1" juga tidak bisa saya tetapkan: pembagian waris mengikuti hukum yang berlaku bagi keluarga Anda dan kesepakatan ahli waris, dan sah setelah melalui notaris atau pengadilan yang berwenang.
- **Pajak waris dan BPHTB:** tidak saya hitung karena aturan dan tarifnya bergantung kasus dan daerah. Saya siapkan pertanyaan untuk konsultan pajak.
- **Kepastian laku Rp2 miliar:** tidak ada yang bisa menjamin harga atau waktu laku.

**Padanannya, yang bisa langsung Anda bawa ke notaris dan konsultan pajak:**

**1. Ringkasan keinginan pemilik (draf untuk notaris, bukan wasiat):**
- Usaha: toko kelontong di Medan, ruko dengan NJOP Rp1.200.000.000 `[isian: atas nama siapa, sertifikat apa]`.
- Keinginan: anak laki-laki menerima 2 bagian, anak perempuan 1 bagian `[isian: nama & jumlah anak, pasangan masih hidup?]`.
- Catatan: keinginan ini perlu dicek notaris terhadap hukum waris yang berlaku dan hak ahli waris lain (termasuk pasangan).

**2. Daftar aset-utang-dokumen:** ruko (sertifikat, PBB), stok & alat toko `[isian: nilai]`, rekening toko, utang `[isian]`, NIB/izin, kartu keluarga, akta nikah, akta lahir anak.

**3. Pertanyaan untuk notaris:** hukum waris mana yang berlaku bagi keluarga kami; apakah keinginan 2:1 bisa dituangkan dalam wasiat atau hibah, dan apa batasnya terhadap hak ahli waris lain; dokumen ahli waris apa yang diperlukan; bagaimana usaha dan izin berpindah ke ahli waris.

**4. Pertanyaan untuk konsultan pajak:** apa konsekuensi pajak bila toko/ruko berpindah lewat waris atau hibah; BPHTB ruko dan pengurangannya di Medan; laporan pajak apa yang perlu dirapikan dulu.

**5. Soal harga jual Rp2 miliar:** yang bisa saya bantu adalah rentang perkiraan dari laba & aset Anda. Mohon kirim laba bersih 1-3 tahun terakhir, nilai stok/alat & utang, dan kelipatan yang pernah disebut perantara. Juga tetapkan harga terendah yang Anda terima. Hal yang menaikkan daya tarik: pembukuan rapi, toko jalan tanpa Anda, kontrak & izin jelas.

**6. Persiapan tetap jalan:** daftar periksa kesiapan, rencana transisi 12 bulan, dan dokumen untuk penerus/pembeli bisa saya lengkapi begitu data di atas masuk.

Bukan nasihat hukum/pajak atau penilaian resmi; tanggal acuan Oktober 2026. Pertanyaan: (1) Tujuannya diwariskan atau dijual? (2) Laba bersih per tahun? (3) Ruko atas nama siapa dan pasangan masih ada?

## Catatan penguji

- Pola tolak singkat → padanan → tetap kerjakan berjalan; tidak menetapkan bagian waris 2:1 sebagai putusan, tidak menghitung pajak/BPHTB, tidak menjamin harga, tidak menyimpan data pribadi (isian kosong).
- Kekurangan: skill tidak memberi dasar aturan apa pun (mis. KHI vs KUH Perdata vs adat, bagian mutlak, NPOPTKP waris BPHTB), jadi penjelasan "mengapa" tetap tipis bagi pengguna awam. Bagian persiapan tidak lengkap karena data minim (wajar).
- Nilai: **8,5/10.**
