# Siapkan Usaha Anda Siap Dijual atau Diwariskan

**Dari "usaha ini kira-kira dihargai berapa?" sampai rencana serah terima 12 bulan, tanpa janji laku dan tanpa angka pasar karangan.**

Diuji AI penguji independen di OpenClaw: 6,1 → 8,7 dari 10 (uji penuh, 5 skenario; tanpa skill umumnya tidak ada daftar periksa berstatus, rencana serah terima per bulan, dan daftar pertanyaan untuk notaris/konsultan pajak; dengan skill ketiganya ada, dan nilai usaha dihitung skrip sebagai rentang dari angka dan asumsi Anda, bukan harga pasti).

> **Yang Anda butuhkan:** AI agent yang mendukung skill (OpenClaw, Claude Code, Codex, atau Cursor — langganan AI-nya ditanggung sendiri) di komputer Windows/Mac/Linux. Python 3 (bawaan Mac/Linux, unduh gratis di Windows) untuk menjalankan skrip pendukung skill ini; tanpa Python skill tetap berjalan, AI mengerjakannya langsung tetapi hasil angka sebaiknya Anda cek ulang. Tidak perlu API key atau akun tambahan dari Komunitech.

## Manfaat
- Daftar periksa kesiapan: pembukuan, prosedur kerja tertulis (SOP), ketergantungan pada Anda, aset, utang, kontrak, izin, pelanggan dan pemasok kunci.
- Rentang nilai usaha yang dihitung dari angka dan asumsi Anda sendiri, lengkap dengan rumus dan peringatan (bukan harga pasti).
- Rencana transisi 3-12 bulan per bulan, bisa langsung dikerjakan.
- Daftar dokumen untuk calon pembeli/penerus dan daftar pertanyaan siap bawa ke notaris dan konsultan pajak.
- Jujur soal batas: tidak membuat akta, wasiat, atau pembagian waris, dan tidak menghitung pajak.

## Cocok untuk siapa
Pemilik warung, toko, kafe, bengkel, jasa, atau toko online yang ingin menjual, mewariskan ke anak, atau menyerahkan ke karyawan; pemilik yang mendekati pensiun.

## Contoh sebelum/sesudah
Kasus warung makan Bu Sri (laba 2023-2025 Rp96 juta/Rp118 juta/Rp134 juta, sisa KUR (kredit usaha rakyat) Rp45 juta, kebutuhan pensiun Rp8 juta/bulan selama 2 tahun):
- **Tanpa skill:** AI juga menyesuaikan gaji manajer dan potongan resep, tetapi dengan rumus rata-rata tertimbang buatan sendiri, lalu menyimpulkan "realistis laku di kisaran 190-280 jt" (walau disebut bukan penilaian resmi); ada 8 saran persiapan, tetapi tanpa daftar periksa berstatus, rencana transisi per bulan, atau daftar pertanyaan khusus untuk notaris/konsultan pajak.
- **Dengan skill (v1.0.1):** laba disesuaikan dengan gaji manajer pengganti dan potongan karena resep masih di kepala pemilik, lalu nilai usaha, biaya 5%, pelunasan KUR, dan hasil bersih dipisah jelas serta dibandingkan dengan kebutuhan pensiun (bisa kurang Rp69.040.000 di harga rendah). Plus daftar periksa, rencana transisi, dan pertanyaan untuk notaris/konsultan pajak. Cuplikan keluarannya (keluaran asli uji OpenClaw otomatis lewat Telegram, v1.0.1, 10 Okt 2026, data fiktif). Istilah: kelipatan laba = berapa kali laba setahun dipakai sebagai patokan harga (di sini 2-3 kali, kata perantara); laba normalisasi = laba setelah disesuaikan:

```
## 4) Perkiraan rentang nilai
| Metode | Rentang | Rumus/catatan |
|---|---|---|
| Kelipatan laba normalisasi (nilai usaha berjalan, sebelum utang) | Rp176.800.000 s/d Rp265.200.000 | basis laba Rp104.000.000 x kelipatan 2-3 x (100-15)/100 |
…
- **Nilai usaha 100% (sebelum utang): Rp176.800.000 s/d Rp265.200.000**
- Utang KUR Rp45.000.000: diasumsikan dilunasi Bu Sri dari hasil jual (harga tidak berubah, tapi hasil bersih berkurang).
- Setelah biaya notaris/perantara 5%: Rp167.960.000 s/d Rp251.940.000
- **Hasil bersih ke Bu Sri (setelah biaya dan pelunasan KUR): Rp122.960.000 s/d Rp206.940.000**
- Kebutuhan hidup 24 bulan x Rp8 juta = Rp192.000.000. **Selisih hasil bersih vs kebutuhan: -Rp69.040.000 (batas bawah) s/d +Rp14.940.000 (batas atas).**
```

## Instalasi singkat
Salin folder ini ke folder skills AI agent Anda:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |

Panduan lengkap (termasuk Windows): `docs/instalasi.md` (di dalam ZIP bernama `CARA-INSTAL.md`).

**Cara pakai:** cukup ketik, misalnya: "Saya mau oper kafe saya tahun depan, bantu siapkan." Data yang kurang ditanyakan sekali, dan angka yang belum Anda berikan tidak dikarang.

**Hasil uji (OpenClaw, uji otomatis agent):** uji penuh v1.0.0 (5 skenario, 10 Okt 2026): rata-rata nilai 6,1 tanpa skill menjadi 8,7 dengan skill (skala 10); rincian di `examples/HASIL-UJI.md`. Uji ulang setelah perbaikan v1.0.1 (6 skenario, 10-11 Oktober 2026): 5,92 menjadi 8,83; rincian di `examples/HASIL-UJI-v1.0.1-openclaw-2026-10-10.md`. Skenario: jual warung makan Bu Sri, wariskan bengkel cat, jual laundry tanpa angka, jebakan akta dan "pasti laku Rp500 juta", dan jual 30% saham bengkel las; uji ulang menambah warung bakso dengan renovasi dan beli bagian sekutu 40%. Contoh Bu Sri di atas berasal dari v1.0.1. Diuji langsung di OpenClaw saja; Claude Code, Codex, dan Cursor belum diuji langsung (format skill-nya sama). Angka di bagian "Bukti uji di bot Telegram" di bawah berasal dari uji tersendiri (satu skenario dengan topik lain), jadi tidak sama dengan angka ini.

## Bukti uji di bot Telegram

Diuji di bot Telegram uji (bot OpenClaw asli di grup uji Komunitech), 12 Okt 2026, satu skenario yang menyangkut harga jual Rp500 juta, tanpa dan dengan skill:
- Tanpa skill: skor 7 dari 10.
- Dengan skill: skor 7,5 dari 10.
Selisihnya tipis. Tanpa skill, jawabannya ringkas dan tegas bahwa Rp500 juta di atas kisaran wajar. Dengan skill, jawabannya lebih lengkap (daftar periksa, rencana 12 bulan, dokumen untuk pembeli, pertanyaan ke notaris) tetapi panjang dan ada kalimat koreksi diri. Jadi di skenario ini, keunggulan skill ada di kelengkapan, bukan di jawabannya yang lebih benar.

## FAQ
**Apakah ini menggantikan notaris?** Tidak. Skill menyiapkan bahan dan pertanyaan; akta dan keputusan hukum tetap lewat notaris.
**Angka nilai usaha dari mana?** Dari laba, aset, dan kelipatan yang Anda berikan. Tanpa kelipatan dari Anda, hasil diberi label contoh hitungan, bukan angka pasar.
**Datanya ke mana?** Skill ini sendiri tidak mengirim apa pun ke pihak lain; namun isi percakapan diproses oleh model AI di aplikasi agent Anda, jadi ikuti kebijakan privasi aplikasi itu.

> **Catatan penting:** hasil berupa rentang hitungan dari angka dan asumsi Anda, bukan penilaian (appraisal) resmi, bukan nasihat hukum, pajak, atau keuangan. Akta, wasiat, pembagian waris, dan pajak tetap lewat notaris, konsultan pajak, atau penilai berizin.

## Riwayat perubahan

Versi terkini: **1.0.1**. Rincian teknis tiap versi ada di `CHANGELOG.md` di folder skill ini.
