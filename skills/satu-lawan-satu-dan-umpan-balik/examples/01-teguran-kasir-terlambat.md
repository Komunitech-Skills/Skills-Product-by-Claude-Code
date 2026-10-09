# Skenario 1: Normal utama: teguran halus kasir terlambat (berantakan, ada hal pribadi)

**Platform:** claude-code (simulasi agent), bukan OpenClaw asli.

**Input:** "Tolong bantu dong, si Rina kasir saya sering telat. Senin 5 Okt masuk 09.40, Rabu 7 Okt 09.35, Kamis 8 Okt 09.50. Toko buka jam 09.00, harusnya dia siap 08.45. Dedi jadi sendirian di kasir, antrean numpuk, kemarin ada satu pelanggan pergi. Anaknya baik sih, kabarnya lagi ada masalah rumah tangga, makanya saya nggak enak banget negurnya. Gimana cara ngomongnya?"

## Output dengan skill

**Ajak Rina Bicara soal Jam Masuk**

**1. Pesan WA untuk mengajak bicara (kirim hari ini; bukan untuk menegur)**
"Rin, besok setelah tutup bisa ngobrol 10 menit di toko ya? Ada yang mau saya bahas soal jadwal. Bukan hal yang buruk kok, santai saja."

**2. Naskah ucapan (empat mata, sekitar 10 menit, setelah tutup)**
- Konteks: "Rin, saya mau bicara soal jam masuk, 10 menit saja."
- Fakta: "Minggu ini kamu masuk jam 09.40 hari Senin 5 Oktober, 09.35 hari Rabu 7 Oktober, dan 09.50 hari Kamis 8 Oktober. Toko buka jam 09.00, jadi kamu seharusnya sudah siap jam 08.45."
- Dampak: "Akibatnya Dedi buka kasir sendirian. Antrean menumpuk, dan kemarin ada satu pelanggan yang pergi."
- Tanya: "Dari sisi kamu bagaimana? Ada kendala yang bisa saya bantu?" (Dengarkan sampai selesai. Kalau dia sendiri mau cerita hal pribadi, dengarkan seperlunya; jangan Bapak/Ibu yang mengangkatnya.)
- Sepakat: "Kita sepakat mulai besok kamu tiba 08.45. Kalau ada hal mendadak, kabari saya sebelum jam 08.30. Hari Jumat [isian: tanggal] kita ngobrol 5 menit lagi untuk lihat hasilnya." Bila ada kendala yang masuk akal (mis. antar anak), tawarkan [isian: opsi yang Bapak/Ibu sanggup, misalnya geser shift].

**3. Pujian (terpisah, jangan dijadikan pembungkus teguran)**
Bila memang ada hal bagus, sebutkan spesifik, misalnya: "Cara kamu menenangkan pelanggan yang komplain kemarin sudah tepat." [isian: kejadian nyata]

**4. Halus tapi jelas**
Hindari: "Mungkin bisa lebih rajin ya." Pakai: "Mulai besok tolong tiba 08.45."

**5. Tindak lanjut**
Catat 3 baris: kesepakatan, siapa, kapan. Cek ulang [isian: Jumat tanggal]. Kalau tetap terlambat setelah dibicarakan baik-baik, baru pertimbangkan surat peringatan bertahap.

**Asumsi:** tim kecil, WA, nada hangat tapi jelas. Masalah di rumahnya tidak dijadikan bahan pembicaraan.
**Pertanyaan:** (1) Apakah sudah pernah ditegur sebelumnya? (2) Apakah ada aturan tertulis tentang keterlambatan? (3) Bisakah jadwal shift digeser bila ada kendala?

## Catatan

Nilai sebelum 5.5 / sesudah 8.5. Sebelum: sudah hangat dan memakai tanggal, tetapi membuka dengan pujian pembungkus, mengarang konsekuensi 'potongan gaji' yang tidak disebut pengguna, menyinggung masalah rumah tangga, tanpa pesan WA ajakan, tanpa tanggal cek ulang. Sesudah: pesan WA ajakan terpisah, naskah KONTEKS-FAKTA-DAMPAK-TANYA-SEPAKAT dengan tiga tanggal dan jam yang benar, pujian dipisah, masalah pribadi tidak diangkat, `[isian]` untuk hal tak diberikan, tiga pertanyaan di akhir. Kurang: 'Bukan hal yang buruk kok' bisa terasa menjanjikan padahal ini teguran; rencana bila dia punya kendala hanya `[isian]`.

Perbandingan lengkap dengan hasil tanpa skill: `00-openclaw-sebelum-sesudah.md`.
