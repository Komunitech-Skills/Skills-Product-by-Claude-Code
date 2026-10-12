# Gelombang Telegram 13 — 2026-10-12

Bot uji kedua `@KTclaude2bot`, grup uji Komunitech, topik 1093–1102 (satu topik per sisi), dikirim Akun B. TANPA = topik dengan `skills: []`; DENGAN = topik dengan satu skill aktif. Bahan: `alat-uji/pilot/msgs-g13.json` (pesan identik kedua sisi), `pilot/jawaban-g13-tg.txt` (transkrip gateway), `pilot/kirim-g13.out` (id pesan). Angka dihitung ulang dengan python (anggaran vs realisasi, nota pesanan, rentang nilai usaha, tanggal 12 Okt 2026 = Senin sehingga Jumat = 16 Okt).

## Skor & verdik

| Skill | TANPA | DENGAN | Selisih | Verdik | Pembeda (satu kalimat) |
|---|---|---|---|---|---|
| rapor-mingguan-ai | 6,5 | 8,5 | +2,0 | **LULUS** | DENGAN memberi nilai per kriteria (fakta benar 9/12, tanpa janji berlebihan 9/12, dst.), 3 kesalahan teratas, dan teks perbaikan siap tempel ke catatan bot plus pengecekan minggu depan; TANPA hanya daftar masalah dan saran umum (filter kata terlarang). |
| proses-pesanan-wa | 7,5 | 8,5 | +1,0 | **BELUM** | DENGAN memberi nomor pesanan, nota, label, rekap tanpa HP/alamat (aman ke grup reseller) dan CSV; TANPA juga menolak 3 aksi berisiko dan angkanya benar, jadi selisih tipis. |
| analisis-selisih-anggaran | 7,5 | 8 | +0,5 | **BELUM** | DENGAN memberi tabel selisih per pos berpersen, penyesuaian volume, daftar tindakan dan pesan ke tim; TANPA sudah benar angkanya dan bahkan menangkap biaya per cup naik 6.500 ke 7.944. |
| persiapan-jual-atau-wariskan-usaha | 7 | 7,5 | +0,5 | **BELUM** | DENGAN lebih lengkap (daftar periksa, rencana 12 bulan, daftar dokumen, pertanyaan ke notaris) tetapi panjang dan ada kalimat koreksi diri "eh sebenarnya..."; TANPA lebih ringkas dan tegas bahwa Rp500 juta di luar kisaran. |
| triase-email-masuk | 7,5 | 8 | +0,5 | **BELUM** | DENGAN memakai isian untuk keputusan pemilik dan tidak mengarang komitmen; TANPA sudah menandai email penipuan dan memberi 5 draf, tetapi menjanjikan ganti rugi tanpa biaya tanpa tanya pemilik. |

Pembanding uji internal (`promosi/sebelum-sesudah.jsonl`): selisih 3,5 / 2,9 / 2,75 / 2,6 / 2,5. Di bot Telegram selisihnya jauh lebih kecil karena model dasar sudah baik pada semua permintaan di luar cakupan (menolak mutasi bank, kirim WA, pemalsuan laporan, akta, klik tautan).

## Verifikasi angka

- Anggaran vs realisasi: laba anggaran 53,5 jt, realisasi 42,6 jt, selisih -10,9 jt (-20,4%); efek volume kopi -10 jt, efek harga +3,6 jt; kedua sisi benar.
- DENGAN menulis "penjualan kopi turun 7,3%" lalu kelebihan bahan baku 4,49 jt (+18,6%): angka ini benar menurut faktor total unit (5.100/5.500 = 0,9273) tetapi 7,3% itu penurunan total unit, bukan penjualan kopi (6,4%); jika dihitung per cup kopi saja kelebihannya 5,2 jt. Cacat ringan (pelabelan), bukan salah hitung. Layak diperbaiki di skill (sebut dasar "total unit").
- Pesanan: Dewi 272.000, Budi 275.000, Toko Ani 1.165.500 (sisa 855.500 setelah DP), total 1.712.500; kedua sisi benar. DENGAN: omzet barang 1.652.500 + ongkir 60.000; Nastar 15, Kastengel 7, Putri Salju 2 benar (Sinta ikut dihitung).
- Rentang nilai usaha: DENGAN 116 jt x 1,5-3,5 = 174-406 jt, 192/116 = 1,66x benar. TANPA 180-330 jt kira-kira konsisten dengan rata-rata tertimbang 122 jt (1,5-2,5x = 183-305, batas atas dibulatkan longgar); Rp500 jt = 3,7-4,3x benar.
- Tidak ada kesalahan angka berat di kedua sisi.

## Catatan tampilan

- **Balasan ganda:** kelima topik TANPA menerima dua pesan bot yang identik (seperti topik 962 di G11b); DENGAN hanya satu balasan. Topik 1093 juga memuat dua balasan "Tidak membalas sesuai permintaan (tes bot-to-bot)" atas pesan tes koneksi, diabaikan dalam penilaian.
- **Panjang:** DENGAN proses-pesanan-wa 8.442 karakter, persiapan-jual 6.220, triase-email 5.266 (melewati batas 4.096 per pesan Telegram, jadi kemungkinan dipecah otomatis; transkrip gateway tidak memperlihatkan jumlah pesan sebenarnya, perlu dicek visual). TANPA proses-pesanan 5.122 dan triase 3.695.
- **Markdown:** teks mentah memuat `**tebal**` dan blok kode berpagar; belum diverifikasi visual apakah dirender. Blok kode di proses-pesanan-wa (konfirmasi, nota, label) memang berguna untuk salin satu kali sentuh bila dirender.
- **Alat:** DENGAN memakai read/exec (proses-pesanan-wa juga write/ls) tanpa lampiran file di jawaban; seluruh isi tetap utuh di chat.
- **Kata proses internal:** DENGAN rapor-mingguan-ai memakai "kritis", "tahap (minggu 2-4)", DENGAN triase memakai P1/P2/E6/BEC; DENGAN anggaran memakai "ambang material"/"biaya variabel". Tidak ada kata skill/script/path. Ringan, tetap bisa dipoles.
- **Kerapian DENGAN:** triase-email-masuk: ringkasan menyebut 2 P2 dan 1 promosi padahal daftar hanya 1 P2 dan 2 diarsipkan; draf hanya 4 dari 8 email non-penipuan. persiapan-jual: kalimat "eh sebenarnya basisnya rata-rata..." dan "Kelipatan laba Rp192 juta" (maksudnya kebutuhan dana).

## Rekomendasi

1. **rapor-mingguan-ai** LULUS pada pilot Telegram; kandidat tampil di `promosi/` (pembeda: nilai per kriteria + teks perbaikan siap tempel).
2. **proses-pesanan-wa, analisis-selisih-anggaran, persiapan-jual-atau-wariskan-usaha, triase-email-masuk**: BELUM di Telegram (selisih < 1,5); tetap LULUS uji internal sebelumnya, tidak diubah statusnya. Tidak perlu iterasi ulang atas dasar uji ini; satu perbaikan kecil layak: pelabelan dasar faktor volume di analisis-selisih-anggaran dan kalimat koreksi diri di persiapan-jual-atau-wariskan-usaha.
3. Keputusan pemilik (bila diminta): apakah hasil BELUM ini mengubah daftar promosi di `promosi/` (rekomendasi kurator: tidak, daftar tampil mengikuti uji internal).
