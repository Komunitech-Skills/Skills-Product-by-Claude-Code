# Dapur Aman, Checklist Siap Tempel

**Ceritakan usaha kuliner Anda dalam satu kalimat; dapat checklist, catatan suhu, dan kartu staf yang tinggal ditempel.**

Diuji AI penguji independen: 5,6 → 8,25 dari 10 (batas suhu, alergen, dan halal dicek faktanya, dan paket lengkap tampil langsung di chat Telegram, bukan hanya nama berkas).

> **PERLU REVIEW perizinan/ahli:** bagian perizinan hanya petunjuk awal dan belum diverifikasi penuh oleh ahli; cek ke Dinas Kesehatan/BPOM/lembaga halal. Bukan pengganti pelatihan atau pemeriksaan resmi, dan bukan nasihat hukum.

> **Yang Anda butuhkan:** AI agent yang mendukung skill (OpenClaw, Claude Code, Codex, atau Cursor — langganan AI-nya ditanggung sendiri) di komputer Windows/Mac/Linux. Python 3 (bawaan Mac/Linux, unduh gratis di Windows) untuk menjalankan skrip pendukung skill ini; tanpa Python skill tetap berjalan, AI mengerjakannya langsung tetapi hasil angka sebaiknya Anda cek ulang. Tidak perlu API key atau akun tambahan dari Komunitech.

## Manfaat
- Checklist harian (datang, sebelum buka, jam sibuk, tutup) sesuai menu dan alat yang Anda punya.
- Catatan (log) suhu kulkas, freezer, masak, dan pemanasan ulang lengkap dengan batas Celsius dan "kalau melebihi, lakukan apa".
- Kartu 10 aturan dapur untuk staf, bahasa sehari-hari.
- Peta risiko menu: ayam, telur, santan, susu, nasi, seafood, alergen, dan kontaminasi silang.
- Ringkasan izin yang relevan (sertifikat laik higiene SLHS, izin pangan rumahan PIRT, izin edar BPOM kode MD, halal, label) sebagai petunjuk awal.

## Cocok untuk siapa
Pemilik kafe, warung, katering rumahan, toko kue, usaha minuman, dan frozen food yang ingin dapurnya lebih tertib dan lebih siap bila ada pemeriksaan (bukan jaminan lulus pemeriksaan), tanpa harus menulis prosedur kerja (SOP) dari nol.

## Cara pakai
Tulis misalnya: "Buatkan checklist keamanan pangan untuk katering rumahan, menu nasi box ayam bakar dan sayur santan, 2 staf, ada 1 kulkas." Hasil langsung muncul lengkap. Punya catatan suhu? Simpan sebagai file tabel CSV (kolom `waktu,alat,suhu`; di Excel: Simpan sebagai CSV) dan minta dicek; pelanggaran batas dan lama makanan berada di suhu rawan (5–60 °C) dihitung otomatis.

## Yang tidak dilakukan
Tidak membuat sertifikat higiene/halal, tidak menulis "bebas alergen" untuk dapur bersama, tidak membantu mengganti tanggal kadaluarsa, dan tidak mengisi catatan suhu palsu. Sebagai gantinya, Anda mendapat cara yang sah (mengurus izin resmi, label "diproses di dapur yang juga mengolah ...", membuang bahan lewat tanggal, mengisi catatan jujur dengan cepat).

## Contoh sebelum/sesudah
**Tanpa skill:** bot menyimpan checklist sebagai file di server, sehingga pengguna Telegram hanya menerima nama file.

**Dengan skill:** paket lengkap tampil langsung di chat: checklist harian, catatan suhu dengan tindakan bila melebihi batas, kartu 10 aturan staf, peta risiko menu, dan petunjuk perizinan. Cuplikan keluarannya untuk katering nasi box (contoh dengan data fiktif, dari `examples/01-katering-nasi-box.md`):

```
**Ayam 63 °C: tidak, jangan.** Ayam/unggas — digoreng utuh, potong, berapa pun bentuknya — wajib matang inti **≥ 74 °C** di bagian paling tebal. Salmonella dan Campylobacter di bagian dalam ayam baru mati di suhu itu; 63 °C hanya berlaku untuk ikan/seafood, telur langsung saji, atau daging sapi/kambing utuh — bukan ayam. Kalau mau lebih cepat: potong lebih kecil/pipih biar matang merata, bukan turunkan suhu. Termometer tusuk (bukan infrared) wajib untuk cek ini — infrared cuma baca permukaan.
…
**1. Checklist Harian**
…
Saat masak & kemas (titik paling kritis untuk kalian):
- [ ] Ayam goreng: ukur inti bagian paling tebal, wajib ≥ 74 °C sebelum diangkat
- [ ] Telur balado: masak sampai inti ≥ 71 °C (ini hidangan matang yang ditahan, bukan telur langsung saji)
- [ ] Sayur santan: didihkan sampai benar-benar mendidih, jangan campur santan baru dengan sisa lama
- [ ] Catat jam makanan selesai matang/mulai dikemas — ini jam mulai hitungan suhu ruang
- [ ] Nasi box dikemas secepat mungkin, jangan dibiarkan terbuka lama di meja
```

## Instalasi singkat
Salin folder ini ke folder skills AI agent Anda:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |

Panduan lengkap (termasuk Windows): lihat `docs/instalasi.md` (di dalam ZIP bernama `CARA-INSTAL.md`).

**Hasil uji (OpenClaw, uji otomatis agent, v1.0.2):** rata-rata nilai 5,6 tanpa skill menjadi 8,25 dengan skill (skala 10), dari empat skenario: katering nasi box dengan jebakan "ayam 63 °C cukup kan?" (di konteks Telegram), warung bakso dan es campur, permintaan kurang lengkap, serta jebakan label halal dan "bebas alergen". Tidak ditemukan kesalahan fakta keselamatan pada empat jawaban dengan skill. Pemeriksaan catatan suhu (kulkas 9 °C selama sekitar 3 jam dan freezer -17 °C tertangkap, cocok dengan hitungan independen) berasal dari uji sebelumnya pada v1.0.1 (`examples/02-cek-log-suhu-kafe-v1.0.1.md`) dan tidak termasuk dalam empat skenario ini. Rincian: `examples/00-openclaw-sebelum-sesudah.md`. Diuji langsung di OpenClaw saja; Claude Code, Codex, dan Cursor belum diuji langsung (format skill-nya sama). Angka di bagian "Bukti uji di bot Telegram" di bawah berasal dari uji tersendiri pada versi sebelum perbaikan 1.0.2 (satu skenario dengan topik lain), jadi tidak sama dengan angka ini.

## Bukti uji di bot Telegram

Diuji di bot OpenClaw asli (grup uji Komunitech, tautan hanya terbuka untuk anggota grup): gelombang 14, 2026-10-12.
- Tanpa skill: https://t.me/c/4407409583/1206/1233 — skor 7
- Dengan skill: https://t.me/c/4407409583/1207/1236 — skor 7,5
Verdik gelombang: BELUM — Dengan skill paketnya lebih lengkap (checklist bercentang, log suhu dengan tindakan bila di atas 5 °C, kartu aturan staf, peta risiko menu), tetapi memuat kesalahan fakta (ayam boleh 63 °C untuk potongan utuh, santan ditulis alergen susu, halal ditulis opsional); tanpa skill sudah menolak sertifikat/logo palsu dan klaim bebas alergen.

Kekurangan ini diperbaiki di versi 1.0.2.

## FAQ
**Apakah ini menggantikan pelatihan atau SLHS resmi?** Tidak. Ini alat bantu kebiasaan kerja; pelatihan dan pemeriksaan resmi tetap lewat Dinas Kesehatan/BPOM.
**Apakah angka suhunya sesuai aturan Indonesia?** Angka suhu dari WHO, FDA Food Code 2022, dan USDA (dicek 2026-10-12; ayam harus matang di bagian inti sampai 74 °C), daftar alergen mengikuti label BPOM, dan halal ditulis wajib sesuai UU 33/2014 & PP 42/2024. Tetap cocokkan dengan Dinkes setempat (PERLU REVIEW).
**Perlu instal apa-apa?** Tidak. Skill tetap berguna tanpa program kecil bawaannya (script); program itu hanya butuh Python standar.

> PERLU REVIEW perizinan/ahli: bagian perizinan (selain halal dan alergen yang dicek 2026-10-12) belum diverifikasi ulang ke sumber resmi. Bukan nasihat hukum.

Versi 1.0.2 (2026-10-12): perbaikan fakta suhu ayam, alergen santan, dan kewajiban halal setelah uji Telegram gelombang 14.

## Riwayat perubahan

Versi terkini: **1.0.2**. Rincian teknis tiap versi ada di `CHANGELOG.md` di folder skill ini.
