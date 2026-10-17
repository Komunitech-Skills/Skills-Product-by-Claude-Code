# Pra-cek Telegram Akun A (A-cepat) — 2026-10-17

Penguji: sub-agent penguji. Cara: uji simulasi kanal Telegram (`uji-tg.sh`, OpenClaw 2026.10.2 lokal, `--channel telegram`, tanpa kirim apa pun), HOME uji berisi hanya skill terkait, satu giliran, pesan = skenario normal pertama dari `examples/00-openclaw-sebelum-sesudah.md`. Hanya sisi DENGAN skill; pembanding TANPA skill memakai uji internal yang ada. Skor 1-10 menurut `koordinasi/alat-uji/brief/tester-umum.md`; angka kunci dihitung ulang penguji dengan Python. Daftar siap kirim: `scratchpad/openclaw-real/pilot/kandidat-a-cepat.json`.

## Kelompok 1

| Skill | Versi | Skor | Verdik | Catatan |
|---|---|---:|---|---|
| laporan-otomatis-terjadwal | 1.1.9 | 8,0 | SIAP KIRIM | CSV fiktif 57 nota 5-11 Okt dibuat penguji (CSV asli uji 1 Okt tidak tersimpan; pesan sama persis). Omzet Rp1.861.000, 103 pcs, rata-rata/hari Rp265.857, hari terbaik 6 Okt Rp311.000, terendah 7 Okt Rp209.000, terlaris Roti Bakar Keju 29 pcs Rp580.000: benar. Kurang: nama berkas CSV disebut; di HOME uji kanal Telegram belum terpasang sehingga jawaban berisi langkah pasang bot (di bot asli kanal sudah ada). Perlu rekap-penjualan-csv terpasang |
| checklist-keamanan-pangan-usaha | 1.0.3 | 8,0 | SIAP KIRIM | Ayam inti >=74 C (63 C ditolak), alergen telur + kelapa, halal UMK wajib 18 Okt 2026, SPP-IRT tidak untuk nasi box: benar. Panjang 8.697 karakter, tanpa tabel (dikirim sebagai 3 pesan). Perizinan ditandai PERLU REVIEW |
| pph21-ter | 1.0.6 | 8,5 | SIAP KIRIM | Jan-Nov Rp2.040.000 (Maret 7% Rp1.190.000), setahun Rp1.945.750 (neto Rp101.915.000, PKP Rp38.915.000), Desember lebih potong Rp94.250: dihitung ulang, benar. Tabel 4 kolom, 2.939 karakter. Disclaimer ada |
| hitung-thr | 1.0.11 | 8,0 | SIAP KIRIM | Andi Rp4.200.000, Sari Rp2.933.333, Dodi Rp1.808.333, Yanto Rp3.500.000, total Rp12.441.666, batas Rabu 3 Maret 2027, masa kerja 74/11/7/13 bulan: benar. Tabel 6 kolom agak lebar; draf grup tanpa nominal. 2.512 karakter |
| pph-final-umkm | 1.0.5 | 7,5 | TIDAK SIAP | Semua angka benar (Rp107.500 / Rp330.000 / total Rp437.500; kurang setor Rp165.000; sisa batas Rp4.212.500.000). Cacat tampilan: tabel 10 kolom di blok kode selebar ~120 karakter, harus digeser di ponsel (uji 16 Okt memakai tabel Markdown). Bila dikirim, hasil kemungkinan tetap sama; saran: kurator mempersempit kolom (mis. gabung "Kena pajak" dan "Batas setor" ke baris catatan) |
