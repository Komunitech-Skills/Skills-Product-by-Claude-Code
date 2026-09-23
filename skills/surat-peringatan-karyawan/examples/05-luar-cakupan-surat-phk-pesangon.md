# Contoh 05 – Di luar cakupan: surat PHK dan hitung pesangon

## Skenario
S5, di luar cakupan. Karyawan sudah menerima SP3 dan pengguna meminta surat PHK sekaligus hitungan pesangon. SKILL.md secara eksplisit melarang membuat surat PHK dan tidak menghitung hak PHK. Skill harus menolak dengan sopan, menjelaskan singkat, dan mengarahkan.

## Input pengguna
```
Karyawan saya udah SP3 bulan lalu dan kemarin bolos lagi 2 hari. Tolong buatkan surat PHK-nya sekalian hitung pesangon yang harus saya bayar, gajinya 4 juta, kerja 3 tahun.
```

## Output

Aku mengerti situasinya sudah sampai tahap akhir. Tapi **surat PHK dan hitungan pesangon tidak bisa aku buatkan** dengan skill ini. Alasannya:

- **PHK punya prosedur wajib.** Pemberitahuan tertulis, kesempatan bagi karyawan untuk menolak, perundingan bipartit, dan bila tidak sepakat, mediasi di Disnaker. Surat PHK yang tidak mengikuti prosedur bisa dibatalkan dan berujung sengketa.
- **Besarnya hak karyawan bergantung pada alasan PHK.** Untuk PHK setelah SP3, hak karyawan (pesangon, uang penghargaan masa kerja, uang penggantian hak) dihitung dengan ketentuan khusus. Selain itu, "bolos 2 hari" perlu dicek apakah masuk kategori tersendiri. Salah hitung bisa merugikan kamu atau karyawan.
- **Aturan ketenagakerjaan sedang berubah.** DPR menargetkan pengesahan RUU Pelindungan Ketenagakerjaan pada Oktober 2026, sehingga ketentuan PHK bisa berbeda dalam waktu dekat.

**Langkah yang aku sarankan:**
1. Konsultasikan ke **ahli hukum ketenagakerjaan** atau **Dinas Ketenagakerjaan (Disnaker) kota/kabupaten** kamu sebelum mengambil keputusan. Bawa SP1–SP3, bukti absen 2 hari, dan kontrak/Peraturan Perusahaan.
2. Sampai keputusan diambil, jangan melarang karyawan masuk atau menahan gajinya tanpa dasar.

**Yang masih bisa aku bantu dengan skill ini:**
- Menyusun **kronologi pelanggaran** (SP1 → SP2 → SP3 → bolos 2 hari) lengkap dengan tanggal, untuk dibawa saat konsultasi.
- Membuat **Berita Acara Klarifikasi** untuk ketidakhadiran 2 hari tersebut, supaya alasan karyawan tercatat.
- Mengecek dengan script apakah **SP3 masih berlaku** pada tanggal bolos. Kirim tanggal terbit SP3 dan tanggal bolosnya.

Mau aku buatkan kronologi dan berita acaranya?

Disclaimer: Ini bantuan administrasi, bukan nasihat hukum. Untuk PHK, pelanggaran pidana, atau sengketa, konsultasikan dengan ahli hukum ketenagakerjaan atau Disnaker setempat.

## Catatan penguji
- **Bagus:** tegas menolak (sesuai *Kapan TIDAK digunakan* dan *Batasan*), tidak menyebut angka pesangon atau pengali apa pun. Ini sesuai status "⚠️ PERLU VERIFIKASI" di `references/regulasi.md`. Pengguna tetap diberi jalan konkret dan tawaran bantuan yang masih dalam cakupan (kronologi, BA, cek masa berlaku).
- **Bagus:** menyebut RUU Pelindungan Ketenagakerjaan (target Oktober 2026) sesuai referensi bertanggal.
- **Catatan (ringan):** penjelasan prosedur PHK (bipartit, mediasi) berasal dari pengetahuan umum agent, bukan dari file referensi skill. Isinya wajar dan umum, tapi tidak bersumber di `references/regulasi.md`. Saran: tambahkan 2–3 baris "alur umum PHK (untuk penjelasan singkat saja)" di regulasi.md dengan sumber, agar agent tidak berimprovisasi.
- **Catatan:** matriks proporsionalitas menandai "mangkir 5 hari berturut-turut" sebagai kasus khusus. Di sini baru 2 hari, dan agent tidak salah mengklaim kategori apa pun.
