# Actual Budget Usaha — anggaran amplop lokal yang dikerjakan AI

**Mutasi bank jadi anggaran rapi, tanpa ketik ulang.**
*Pakai Actual Budget (gratis, data di komputer sendiri); AI yang mengimpor mutasi dan melaporkan sisa anggaran.*

> **Skill ini membantu Anda memakai Actual Budget, bukan menggantikannya.** Actual Budget adalah aplikasi
> open-source (lisensi MIT) yang Anda unduh sendiri dari https://actualbudget.org/download. Komunitech **tidak
> berafiliasi dengan Actual Budget**; nama dipakai hanya untuk menjelaskan kompatibilitas.

> **Yang Anda butuhkan:** AI agent yang mendukung skill (OpenClaw, Claude Code, Codex, atau Cursor — langganan AI-nya ditanggung sendiri) di komputer Windows/Mac/Linux. Python 3 (bawaan Mac/Linux, unduh gratis di Windows) untuk skrip hitung; tanpa Python skill tetap berjalan dengan hitungan oleh AI. Tidak perlu API key atau akun tambahan dari Komunitech.

## Manfaat
1. **Tidak perlu ketik transaksi satu per satu.** Mutasi CSV BCA, BRI, Mandiri, atau BNI langsung jadi file siap
   impor ke Actual. Angka format Indonesia (`1.500.000,00`) dan format Inggris (`1,500,000.00`) sama-sama terbaca
   persis sampai sen.
2. **Kategori terisi otomatis, yang ragu ditanyakan.** PLN, Telkomsel, Pertamina, Meta Ads, dan biaya admin
   langsung dikelompokkan. Tarik tunai, top up GoPay, belanja Tokopedia, atau baris dobel **tidak ditebak**; semuanya
   ditanyakan sekaligus dalam satu pesan.
3. **Tahu kategori yang jebol dalam 5 detik.** Tanya "anggaran bulan ini gimana?" dan dapat sisa per kategori,
   kategori yang minus, uang yang siap dianggarkan, dan 5 pengeluaran terbesar. Angkanya sama dengan hitungan Actual.
4. **Aman untuk data Anda.** File budget hanya dibaca, tidak pernah diubah. Tidak ada internet, akun, atau API key.
5. **Laporan datang sendiri.** Bisa dijadwalkan tiap Senin pagi ke Telegram Anda lewat OpenClaw.

## Cocok untuk siapa
- **Freelancer & profesional** (desainer, konsultan, fotografer) yang penghasilannya naik turun dan butuh anggaran
  per kategori supaya uang proyek tidak "hilang".
- **Usaha kecil** yang ingin mengendalikan biaya (sewa, iklan, bahan, ongkir) tanpa aplikasi akuntansi berbayar.
- Pengguna YNAB atau aplikasi anggaran berbayar yang ingin pindah ke alat gratis tanpa biaya bulanan.

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
- **Kas UMKM**: Anda cukup ingin **buku kas harian** lewat chat (uang masuk/keluar, saldo laci, hitung uang laci,
  prive) tanpa memasang aplikasi apa pun.
Keduanya bisa membaca mutasi bank. Bila ragu, agent akan bertanya sekali.

## Cara pakai
Ketik kalimat biasa ke agent, misalnya:
- "Ini mutasi BCA September, masukkan ke Actual."
- "Sisa anggaran saya bulan ini berapa? Ada yang jebol?"
- "Kirim ringkasan anggaran ke Telegram saya tiap Senin pagi."

## Instalasi singkat
1. Pasang aplikasi **Actual Budget desktop** (gratis): https://actualbudget.org/download. Buat budget dan rekening Anda.
2. Salin folder `actual-budget-usaha` ke folder skills platform Anda (OpenClaw, Claude Code, Codex, Cursor). Lokasi
   persis per platform ada di `docs/instalasi.md`.
3. Butuh Python 3.8+ (umumnya sudah ada). Tidak ada paket tambahan yang perlu dipasang.

## FAQ
**1. Apakah data keuangan saya dikirim ke Komunitech atau internet?**
Tidak. Script bekerja di komputer Anda, tanpa koneksi internet. File budget Actual hanya dibaca (read-only).

**2. Bank saya mengirim mutasi PDF, bisa?**
Belum. Unduh versi CSV atau Excel dari internet banking. File Excel cukup disimpan ulang sebagai CSV.

**3. Saya pakai Actual di browser (server), bukan aplikasi desktop. Bisa?**
Konversi mutasi ke CSV tetap bisa. Ringkasan otomatis butuh aplikasi desktop, atau file Export (.zip) yang
diekstrak, karena versi browser tidak menyimpan file budget di komputer.

## Status & kejujuran
Versi 1.0.1, status **draft**. Diuji dengan budget **Actual 26.9.0 asli** yang dibuat lewat API resmi (data fiktif):
angka ringkasan sama persis dengan Actual. File CSV hasil sudah diurai parser CSV Actual dan diimpor lewat API.
**Belum diuji:** klik manual di aplikasi desktop, Windows/macOS, ekspor mutasi asli terbaru dari tiap bank (contoh
mutasi disusun dari pola umum), dan pengiriman nyata ke Telegram. Ringkasan adalah alat bantu mengatur uang, bukan
laporan akuntansi atau pajak.

---
*Komunitech tidak berafiliasi dengan Actual Budget. "Actual Budget" adalah nama proyek milik pemiliknya.*
