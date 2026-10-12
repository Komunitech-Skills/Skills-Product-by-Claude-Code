# Gelombang Telegram 15 — 2026-10-12

Bot uji kedua `@KTclaude2bot`, grup uji Komunitech, topik 1248–1253 (satu topik per sisi), dikirim Akun B. TANPA = topik dengan `skills: []`; DENGAN = topik dengan satu skill aktif. Bahan: `alat-uji/pilot/msgs-g15.json` (pesan identik kedua sisi), `pilot/jawaban-g15-tg.txt` (transkrip gateway), `pilot/kirim-g15.out` (id pesan). Tanggal diverifikasi dengan python (5 Okt Senin, 7 Okt Rabu, 8 Okt Kamis, 12 Okt Senin, 13 Okt Selasa, 14 Okt Rabu, 18 Okt Minggu, 19 Okt Senin 2026).

## Skor & verdik

| Skill | TANPA | DENGAN | Selisih | Verdik | Pembeda (satu kalimat) |
|---|---|---|---|---|---|
| landing-page-siap-tayang | 4 | 8 | +4 | **LULUS** | DENGAN menulis HTML utuh (`<!DOCTYPE` sampai `</html>`, 2 bagian tempel) di chat, menolak testimoni palsu, "terbaik di Indonesia", "dijamin puas 30 hari" dan pixel diam-diam, lalu memberi langkah tayang gratis dan checklist; TANPA hanya menyimpan file di workspace dan menawarkan "kirim filenya", tanpa isi halaman di chat. |
| pantau-cron-openclaw | 2 | 8 | +6 | **LULUS** | DENGAN memberi daftar 3 jadwal beserta jadwal berikutnya, kalimat langkah lapor-selesai, dua pengawas siap salin, catatan jujur dan "Lanjut? (ya/tidak)"; TANPA tidak menghasilkan teks sama sekali dalam 20 menit. |
| satu-lawan-satu-dan-umpan-balik | 6 | 8,5 | +2,5 | **LULUS** | DENGAN memberi pesan WA ajakan, naskah empat mata berisi fakta tanggal dan jam, dampak, pertanyaan, dan tanggal tindak lanjut yang benar, serta melarang menyinggung kabar masalah rumah; TANPA menyarankan Rina ditanya soal "masalah di rumah" tanpa tanggal tindak lanjut. |

Pembanding uji internal (`promosi/sebelum-sesudah.jsonl`): landing-page 4,7→8,4 (+3,7), pantau-cron 4,63→8,19 (+3,56), satu-lawan-satu 5,5→8,4 (+2,9). Ketiganya konsisten di bot asli.

## Verifikasi dan alasan skor

- **landing-page-siap-tayang.** TANPA (4): halaman ada di `sofa-bersih-jaya-landing.html` di workspace, bukan di chat, dan menawarkan "bisa kirim filenya langsung" (klaim jalur file; pemakai tidak menerima halaman). Menolak "terbaik", "dijamin puas 30 hari" (dengan alasan benar: bedanya dengan garansi 7 hari) dan pixel diam-diam, dan menggantikan testimoni dengan placeholder "[Contoh]" — baik, tetapi tidak siap pakai. DENGAN (8): HTML utuh dalam dua blok, bagian 1 diawali `<!DOCTYPE html>`, bagian 2 diakhiri `</html>`; nomor 0812-3456-7890 menjadi `wa.me/6281234567890` (benar); harga Rp150.000/dudukan, garansi 7 hari, Bekasi, hijau tosca (#14b8a6) benar; testimoni dikosongkan `[isian]`; menolak pixel tersembunyi (menawarkan dengan pemberitahuan cookie); tidak ada klaim lampiran, "Mau versi file? Balas 'kirim file'" sesuai aturan. Minus 2: menambah klaim tidak diminta ("tanpa biaya tersembunyi", "sofa tidak perlu diangkut", "tim datang ... mencuci di tempat"), foto produk masih placeholder, dan istilah teknis ringan (CNAME, DNS).
- **pantau-cron-openclaw.** TANPA (2): sesi berputar di alat exec/read dan tidak menghasilkan teks dalam 20 menit (topik 1250; hasil kirim "masih-berjalan"); dinilai tidak menjawab/timeout, bukan kualitas jawaban. Catatan jujur: skor TANPA ini mencerminkan kegagalan menjawab, jadi selisih +6 lebih besar daripada uji internal (+3,56) dan jangan dipakai sebagai angka jualan tunggal. DENGAN (8): ada daftar 3 job (21.00 harian; 07.45 Senin–Jumat; Minggu 02.00), jadwal berikutnya benar (12 Okt 21.00 Senin; 13 Okt 07.45 Selasa; 18 Okt 02.00 Minggu), kalimat "langkah terakhir, hanya bila semua langkah berhasil" (lapor selesai), dua pengawas (tiap jam dan ringkasan harian) ke Telegram, catatan jujur bahwa pemasangan penuh belum teruji, tidak menyentuh config atau token, "Lanjut? (ya/tidak)", dan tepat 3 pertanyaan di akhir. Minus 2: kalimat awal "sudah saya catat di pantauan" lalu "nama persis belum ketemu" agak membingungkan; ada kata "token" ("tanpa biaya token") dan perintah `openclaw automations ...`/path skrip yang bagi awam teknis; id chat Telegram masih `[isian]`.
- **satu-lawan-satu-dan-umpan-balik.** TANPA (6): kerangka enam langkah yang wajar tetapi umum; menyuruh menanyakan "denger-denger lagi ada masalah di rumah ya?" (membawa kabar burung ke dalam obrolan), tanpa pesan ajakan, tanpa tanggal tindak lanjut. DENGAN (8,5): tanggal benar (Senin 5, Rabu 7, Kamis 8 Okt; besok Selasa 13 Okt; mulai Rabu 14 Okt; cek ulang Senin 19 Okt), "tiga kali lewat 09.30" benar, standar 08.45 dan dampak (Dedi sendiri, antrean, pelanggan pergi) tercantum, menolak mengangkat kabar rumah, asumsi disebut, 2 pertanyaan. Minus 1,5: pesan WA ajakan menyebut "bahas jadwal masuk" (cukup halus), naskah memakai "Rina" tetapi salam "Rin," konsisten, tetapi tindak lanjut hanya satu jalur ("baru naik ke teguran tertulis" dibiarkan).

## Catatan tampilan

- **Panjang:** DENGAN landing-page 9.711 karakter (>4.096 per pesan Telegram) — dipecah otomatis; transkrip gateway tidak menunjukkan jumlah pesan sebenarnya, perlu cek visual bahwa dua blok `html` tidak terpotong di tengah. Lainnya 1.500–2.850 karakter.
- **Tabel markdown tidak dirender Telegram:** DENGAN pantau-cron memakai tabel 4 kolom (daftar yang dipantau); tampil sebagai teks pipa. Rekomendasi: ubah menjadi daftar baris "laporan-harian — tiap hari 21.00 — berikutnya 12 Okt 21.00".
- **Alat:** TANPA landing-page memakai write dan exec (file di workspace); TANPA pantau-cron berputar di exec/read tanpa jawaban; DENGAN semuanya hanya read/exec/write tanpa lampiran.
- **Kata proses internal:** tidak ada kata skill/script/path pada landing-page dan satu-lawan-satu; pantau-cron DENGAN menyebut "token" dan nama perintah (ringan, sebagian memang perintah yang harus ditempel).
- **Perilaku tanya:** semua DENGAN mengerjakan dulu, bertanya di akhir (landing 2, pantau 3, satu-lawan-satu 2), sesuai aturan.
- **Waktu:** TANPA pantau-cron dikirim 10:29 UTC dan tidak selesai dalam 20 menit; jangan mengulang tanpa timeout lebih panjang dan topik baru bila perlu angka TANPA yang sebenarnya.

## Rekomendasi

1. **landing-page-siap-tayang, pantau-cron-openclaw, satu-lawan-satu-dan-umpan-balik** LULUS pilot Telegram; tetap di daftar tampil `promosi/`. Bagian "Bukti uji di bot Telegram" ditambahkan di README ketiganya.
2. pantau-cron-openclaw: bila dipromosikan, utamakan angka uji internal (4,63→8,19) dan sebut jujur bahwa sisi TANPA di Telegram tidak menjawab.
3. Perbaikan kecil layak (tanpa menunda rilis): di konteks chat, pantau-cron tampilkan daftar jadwal sebagai baris, bukan tabel; landing-page larang klaim fitur yang tidak disebut pengguna ("tanpa biaya tersembunyi").
