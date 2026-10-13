# Actual Budget Usaha — anggaran amplop lokal yang dikerjakan AI

**Mutasi bank jadi anggaran rapi, tanpa ketik ulang.**
*Pakai Actual Budget (gratis, data di komputer sendiri); AI yang menyiapkan impor mutasi dan melaporkan sisa anggaran tiap "amplop" (pos per kategori, seperti amplop uang).*

*Diuji AI penguji independen di OpenClaw: 5,5 → 8,25 dari 10 (pembeda terbesar: menolak mengedit file budget langsung dan menahan laporan keuangan dari grup karyawan; di konversi mutasi sendiri unggulnya tipis; memakai data contoh).*

> **Skill ini membantu Anda memakai Actual Budget, bukan menggantikannya.** Actual Budget adalah aplikasi
> open-source (kode sumbernya terbuka, lisensi MIT) yang Anda unduh sendiri dari https://actualbudget.org/download. Komunitech **tidak
> berafiliasi dengan Actual Budget**; nama dipakai hanya untuk menjelaskan kompatibilitas.

> **Yang Anda butuhkan:** AI agent yang mendukung skill (OpenClaw, Claude Code, Codex, atau Cursor — langganan AI-nya ditanggung sendiri) di komputer Windows/Mac/Linux. Python 3 (bawaan Mac/Linux, unduh gratis di Windows) untuk menjalankan skrip pendukung skill ini; tanpa Python skill tetap berjalan, AI mengerjakannya langsung tetapi hasil angka sebaiknya Anda cek ulang. Tidak perlu API key atau akun tambahan dari Komunitech.

## Manfaat
1. **Tidak perlu ketik transaksi satu per satu.** Mutasi bank BCA, BRI, Mandiri, atau BNI (file CSV, yaitu tabel
   yang diunduh dari internet banking) diubah jadi file siap impor ke Actual. Angka format Indonesia
   (`1.500.000,00`) dan format Inggris (`1,500,000.00`) sama-sama terbaca sampai sen. Langkah impor di layar
   Actual sendiri belum diuji langsung.
2. **Kategori diusulkan otomatis, yang ragu ditanyakan.** PLN, Telkomsel, Pertamina, Meta Ads, dan biaya admin
   langsung dikelompokkan. Tarik tunai, top up GoPay, belanja Tokopedia, atau baris dobel **tidak ditebak**; semuanya
   ditanyakan sekaligus dalam satu pesan. Pada uji, cukup banyak baris tetap perlu Anda pilih karena nama kategori
   di budget Anda bisa berbeda dari usulan.
3. **Tahu kategori yang jebol dalam hitungan detik.** Tanya "anggaran bulan ini gimana?" dan dapat sisa per kategori,
   kategori yang minus, uang yang siap dianggarkan (To Budget), dan 5 pengeluaran terbesar. Pada data contoh, angkanya
   sama dengan hitungan Actual sendiri.
4. **Hati-hati dengan data Anda.** Skill hanya membaca file budget dan tidak menulis ke dalamnya (pada uji, isi file
   tidak berubah). Tidak memakai internet, akun, atau kunci akses (API key).
5. **Laporan datang sendiri.** Bisa dijadwalkan tiap Senin pagi ke Telegram Anda lewat OpenClaw (jadwal otomatis ini
   belum diuji langsung).

## Cocok untuk siapa
- **Freelancer & profesional** (desainer, konsultan, fotografer) yang penghasilannya naik turun dan butuh anggaran
  per kategori supaya uang proyek tidak "hilang".
- **Usaha kecil** yang ingin mengendalikan biaya (sewa, iklan, bahan, ongkir) tanpa aplikasi akuntansi berbayar.
- Pengguna YNAB (aplikasi anggaran amplop berbayar) atau aplikasi sejenis yang ingin pindah ke alat gratis tanpa
  biaya bulanan.

## Sebelum / sesudah
**Tanpa skill:** mutasi BCA dibuka di Excel, kolom disusun ulang manual, angka `"1,500,000.00"` dan tanggal `'01/09`
dibetulkan satu per satu. Tarik tunai ikut terhitung pengeluaran sehingga anggaran terlihat jebol padahal tidak.
Sisa anggaran hanya bisa dilihat dengan membuka aplikasi.

**Dengan skill** (hasil nyata, data fiktif; lengkapnya di `examples/`):
```
Terbaca: 13 transaksi | Dilewati: 5 | Perlu dicek: 5
Cek saldo bank: COCOK (saldo awal Rp 5.000.000 -> saldo akhir Rp 7.242.376,54)
...
KATEGORI JEBOL (2):
- Iklan: minus Rp 1.100.000 (anggaran Rp 1.000.000, terpakai Rp 3.200.000, bawaan bulan lalu Rp 1.100.000)
```

## Actual Budget Usaha atau Kas UMKM?
- **Actual Budget Usaha** (skill ini): Anda memakai aplikasi Actual dan ingin **anggaran per kategori**: jatah iklan
  berapa, sisa berapa, mana yang jebol, uang yang belum diberi tugas.
- **Kas UMKM** (skill Komunitech terpisah): Anda cukup ingin **buku kas harian** lewat chat (uang masuk/keluar, saldo laci, hitung uang laci,
  prive) tanpa memasang aplikasi apa pun.
Keduanya bisa membaca mutasi bank. Bila ragu, agent akan bertanya sekali.

## Cara pakai
Ketik kalimat biasa ke agent, misalnya:
- "Ini mutasi BCA September, masukkan ke Actual."
- "Sisa anggaran saya bulan ini berapa? Ada yang jebol?"
- "Kirim ringkasan anggaran ke Telegram saya tiap Senin pagi." (jadwal otomatis ini belum diuji langsung)

## Instalasi singkat
1. Pasang aplikasi **Actual Budget desktop** (gratis): https://actualbudget.org/download. Buat budget dan rekening Anda.
2. Salin folder `actual-budget-usaha` ke folder skills AI agent Anda:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |

Panduan lengkap (termasuk Windows): lihat `docs/instalasi.md` yang disertakan dalam paket. Butuh Python 3.8+ (umumnya sudah ada). Tidak ada paket tambahan yang perlu dipasang.

**Hasil uji (angka nyata):** uji OpenClaw otomatis agent, Okt 2026 (v1.0.7), skor 1–10: tanpa skill **5,5** → dengan skill **8,25** (LULUS). Contoh: menolak mengedit file budget (`db.sqlite`) langsung dan menahan pengiriman ringkasan ke grup WA; konversi mutasi BCA dengan **Cek saldo bank: COCOK** (saldo akhir Rp9.708.250,32); ringkasan September To Budget Rp1.010.000, 2 kategori jebol. Catatan jujur: pada konversi mutasi sendiri unggulnya tipis (7 → 7,5); keunggulan besar ada di keamanan data (4 → 9). Sumber skor: `examples/00-openclaw-sebelum-sesudah.md`. Cuplikan "Dengan skill" di atas berasal dari `examples/01-konversi-mutasi-bca.md` dan `examples/02-ringkasan-bulanan.md` (hasil skrip pada data fiktif), bukan dari uji OpenClaw.

**Status uji (jujur):** sudah diuji OpenClaw (sebelum/sesudah otomatis 2026-10-02; muat CLI). Aplikasi Actual desktop tidak dijalankan saat uji; yang dipakai hanya file budget fiktif yang dibuat lewat API resmi Actual versi 26.9.0, jadi impor ke layar Actual dan jadwal Telegram belum diuji langsung. Claude Code (simulasi agent). Codex dan Cursor belum uji platform asli. Ringkasan alat bantu anggaran, bukan laporan akuntansi/pajak.

## FAQ
**1. Apakah data keuangan saya dikirim ke Komunitech atau internet?**
Tidak. Script bekerja di komputer Anda, tanpa koneksi internet. File budget Actual hanya dibaca, tidak diubah.

**2. Bank saya mengirim mutasi PDF, bisa?**
Belum. Unduh versi CSV atau Excel dari internet banking. File Excel cukup disimpan ulang sebagai CSV.

**3. Saya pakai Actual di browser (server), bukan aplikasi desktop. Bisa?**
Konversi mutasi ke CSV tetap bisa. Ringkasan otomatis butuh aplikasi desktop, atau file Export (.zip) yang
diekstrak, karena versi browser tidak menyimpan file budget di komputer.

---
*Komunitech tidak berafiliasi dengan Actual Budget. "Actual Budget" adalah nama proyek milik pemiliknya.*

## Riwayat perubahan

Versi terkini: **1.0.7**. Rincian teknis tiap versi ada di `CHANGELOG.md` di folder skill ini.
