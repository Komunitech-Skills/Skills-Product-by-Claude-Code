# Skenario 4: Input tidak lengkap: kinerja karyawan turun

**Platform:** claude-code (simulasi agent), bukan OpenClaw asli.

**Input:** "Karyawan saya kinerjanya turun, tolong bantu cara ngomongnya."

## Output dengan skill

**Kerangka Percakapan Saat Kinerja Karyawan Turun (siap diisi)**

**Pesan WA ajakan (bisa dikirim sekarang)**
"[isian: nama], besok [isian: hari/jam] bisa ngobrol 15 menit ya? Ada yang mau saya bahas soal pekerjaan dan juga ingin dengar dari kamu. Santai saja."

**Naskah ucapan (kerangka KONTEKS-FAKTA-DAMPAK-TANYA-SEPAKAT)**
- Konteks: "Saya mau bicara soal [isian: hal, mis. hasil kerja bulan ini], 15 menit saja."
- Fakta: "[isian: kejadian yang bisa dilihat, dengan tanggal/angka, mis. 'Bulan lalu 3 laporan terlambat, tanggal ...']." Hindari kata "malas" atau "menurun terus".
- Dampak: "Akibatnya [isian: siapa terkena dan apa akibatnya]."
- Tanya: "Dari sisi kamu bagaimana? Ada yang menghambat atau yang bisa saya bantu?" Dengarkan sampai selesai.
- Sepakat: "Mulai [isian: tanggal] kita sepakat [isian: langkah konkret]. Kita cek lagi [isian: tanggal]."

**Pertanyaan pembuka yang aman:** "Pekerjaan apa yang paling menguras minggu ini?" "Ada yang menghambat kerjamu?"
**Langkah:** catat kejadian secara faktual dan adil; sampaikan secepatnya; empat mata; jangan di grup.

**Asumsi:** tim kecil, WA, nada hangat tapi jelas. Satu sisi cerita saja, jadi dengar dulu sisi karyawan.
**Tiga pertanyaan agar naskah tepat:** (1) Turunnya dalam hal apa dan sejak kapan (tanggal/angka)? (2) Peran karyawannya apa? (3) Hasil yang diharapkan sebulan ke depan apa?

## Catatan

Nilai sebelum 6.5 / sesudah 8.5. Sebelum: bertanya 5 hal lebih dulu, tidak menghasilkan apa pun. Sesudah: langsung memberi pesan WA dan naskah berbingkai `[isian]`, lalu 3 pertanyaan di akhir (sesuai aturan 'kerjakan dulu'). Kurang: naskah masih kerangka umum karena memang tanpa data; wajar.

Perbandingan lengkap dengan hasil tanpa skill: `00-openclaw-sebelum-sesudah.md`.
