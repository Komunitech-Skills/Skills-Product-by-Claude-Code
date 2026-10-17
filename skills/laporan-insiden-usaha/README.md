# Laporan Insiden Rapi Segera Setelah Masalah Terjadi

**Dari kejadian panik — pesanan salah kirim, kasir error, komplain viral — jadi laporan lengkap + draf minta maaf, siap kirim.**

*Diuji AI penguji independen di OpenClaw: 6,5 → 8,75 dari 10 (akar masalah mengarah ke proses, bukan menyalahkan karyawan, dan batas waktu lapor kebocoran data dihitung tepat).*

> **Yang Anda butuhkan:** AI agent yang mendukung skill (OpenClaw, Claude Code, Codex, atau Cursor — langganan AI-nya ditanggung sendiri) di komputer Windows/Mac/Linux. Tidak perlu API key atau akun tambahan dari Komunitech.

## Manfaat
- ✅ Susun laporan insiden lengkap (kronologi, dampak berangka, akar masalah, pencegahan) dari cerita berantakan
- ✅ Akar masalah dicari pakai 5 Kenapa (bertanya "kenapa?" berulang sampai ketemu sebabnya) yang **mengarah ke proses**, bukan menyalahkan karyawan
- ✅ Angka dampak diambil dari cerita Anda; yang belum Anda sebutkan ditandai `[isi: ...]`, bukan dikarang
- ✅ Langsung dapat **draf permintaan maaf ke pelanggan** (sopan, tanpa janji berlebihan) + **ringkasan siap tempel ke WA tim/pemilik**
- ✅ Kalau data pribadi pelanggan bocor: tenggat pemberitahuan 3×24 jam (UU Pelindungan Data Pribadi / UU PDP Pasal 46) dihitung, plus draf pemberitahuan ke pelanggan terdampak & catatan untuk lembaga (ditandai "perlu review hukum" agar ditinjau ahli hukum sebelum dikirim)

## Cocok untuk siapa
- Pemilik toko online/offline yang baru kena masalah operasional (retur massal, stok habis promo, kasir/QRIS error)
- Admin/CS yang harus cepat menjawab pelanggan setelah kejadian dan melapor ke atasan
- Owner UMKM yang ingin insiden dicatat rapi supaya bisa dievaluasi, bukan cuma diributkan lalu dilupakan

**Di luar cakupan:** kecelakaan kerja berat, kebakaran, atau kejadian yang mengancam nyawa. Untuk kecelakaan kerja, pemberi kerja wajib melapor ke BPJS Ketenagakerjaan dan Dinas Provinsi/unit pengawasan ketenagakerjaan setempat paling lama 2×24 jam (Permenaker 5/2021 Pasal 8) serta ke pihak berwenang — bukan lewat laporan insiden toko dari skill ini. Skill hanya membantu kronologi & komunikasi dasar; ini bukan nasihat K3 atau hukum, jadi tanyakan langkah resminya ke BPJS Ketenagakerjaan atau pengawas ketenagakerjaan.

## Contoh sebelum & sesudah
**Sebelum:** "QRIS di toko error total dari jam 12 siang sampe jam 1, pas lagi rame jam makan siang. Kasir cuma bisa terima cash, ada sekitar 15 pelanggan yang batal beli karena cuma bawa uang digital. Internet toko emang sering putus-nyambung, cuma pake 1 provider."

**Sesudah (cukup ketik: "buatin laporan insiden dari cerita ini"):**
```
## Akar Masalah (5 Kenapa)
1. Kenapa QRIS error? → Karena koneksi internet toko terputus.
2. Kenapa koneksi terputus? → Karena internet toko sering putus-nyambung.
3. Kenapa hal ini bisa mengganggu operasional total? → Karena toko hanya mengandalkan satu provider internet tanpa cadangan.

**Akar masalah:** Tidak ada koneksi internet/pembayaran cadangan saat provider utama bermasalah, sehingga satu gangguan koneksi langsung menghentikan seluruh pembayaran non-tunai.

## Rencana Pencegahan
| Tindakan | Penanggung jawab | Tenggat |
|---|---|---|
| Siapkan internet cadangan (paket data/modem kedua) khusus untuk mesin QRIS | Pemilik/Supervisor | [isi: tenggat] |
| Siapkan QRIS statis cetak (dari bank/penyedia lain) sebagai cadangan manual saat sistem utama down | Kasir/Supervisor | [isi: tenggat] |
```
Bagian `[isi: ...]` adalah yang Anda lengkapi sendiri; skill meminta AI tidak menebaknya. Hasil aslinya juga memuat kronologi, dampak, draf minta maaf, dan ringkasan WA — lihat contoh lengkap di `examples/02-qris-error-jam-sibuk.md`.

## Cara pakai
Setelah terpasang, cukup ceritakan kejadiannya seperti chat biasa ke AI agent Anda, misalnya:
- "Buatin laporan insiden, kemarin 40 pesanan salah alamat pas promo 9.9..."
- "QRIS error 1 jam pas jam makan siang, tolong susun laporan + draf minta maaf"
- "Ada data pelanggan kekirim ke grup salah, gimana laporannya?"

Jika info penting (tanggal, jumlah terdampak) belum disebut, skill akan menanyakan sekali dalam satu pesan — bukan berulang-ulang.

## Instalasi singkat
Salin folder `laporan-insiden-usaha` ke folder skills AI agent Anda:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |

Panduan lengkap (termasuk Windows): lihat `CARA-INSTAL.md` di dalam paket.

**Hasil uji (angka nyata):**
- **Uji OpenClaw, uji ulang v1.0.2** (penguji AI independen; angka dari `examples/00-openclaw-sebelum-sesudah.md`): rata-rata nilai 6,5 tanpa skill menjadi 8,75 dengan skill (skala 10). Tanpa skill, laporan menyebut nama admin sebagai akar masalah dan menulis tindakan yang belum terjadi seolah sudah dilakukan. Dengan skill, akar masalah mengarah ke proses, pembeli terdampak yang belum komplain ikut dihubungi, dan tenggat pemberitahuan kebocoran data (3×24 jam) dihitung tepat.
- Uji pertama (sebelum perbaikan) belum lulus: 7 menjadi 7,5, karena skill belum menyebut batas 3×24 jam. Pada uji ulang masih ada hal kecil yang perlu Anda periksa: satu klaim "sudah dilakukan" yang tidak Anda sebutkan, dan satu salah hitung durasi pada contoh apotek. Bagian hukum tetap perlu ditinjau konsultan hukum Anda.

**Status uji (jujur):** diuji di OpenClaw (uji otomatis agent) dan Claude Code (simulasi agent); Codex dan Cursor belum diuji langsung (format skill-nya sama).

## Bukti uji di bot Telegram

Diuji di bot OpenClaw asli (grup uji internal Komunitech, 17 Okt 2026, versi 1.0.5) dengan pesan yang sama: "Buatin laporan insiden. Kemarin pas promo 9.9, 40 pesanan label alamatnya kesalahan gara-gara admin salin data dari sheet lama. Ketahuan jam 14.00 pas ada komplain masuk 5 pelanggan, packing mulai jam 09.00. Kita udah hubungin…". Tanpa skill skor **6** → dengan skill skor **8,5** (selisih +2,5, lulus acuan kami). Hanya dengan skill laporan mengingatkan bahwa 35 pelanggan lain belum komplain dan menyiapkan pesan maaf proaktif untuk mereka. Penyebab yang belum Anda sebutkan ditandai "dugaan, perlu dikonfirmasi", dan yang ditulis sebagai sudah dilakukan hanya yang Anda ceritakan. Catatan jujur: ringkasan WA untuk tim masih menulis "25 paket berhasil dihentikan" sebagai fakta padahal hasil pembatalan masih perlu Anda pastikan, ada satu frasa yang kurang rapi, dan laporan tampil dalam 2 pesan berurutan. Uji sebelumnya: 16 Okt 2026 (versi 1.0.4) tanpa skill 4,5 → dengan skill 5; saat itu dugaan dan tindakan yang belum Anda lakukan ditulis seolah fakta.

## FAQ
**1. Apakah skill ini bisa dipakai untuk kebocoran data pelanggan?**
Skill ini bisa dipakai untuk kasus itu, mis. data terkirim ke grup salah. Skill menyebut kewajiban UU 27/2022 Pasal 46 — pemberitahuan tertulis paling lambat 3×24 jam ke pelanggan terdampak dan lembaga — menghitung batas waktunya, dan menyiapkan drafnya. Kalau Anda ingin "diam saja", skill akan mengingatkan dengan sopan bahwa menurut pasal itu pemberitahuan wajib. Ini **bukan nasihat hukum**; untuk kepastian penerapan, konsultasikan ke konsultan hukum atau petugas pelindungan data (DPO) Anda.

**2. Apakah laporan ini bisa dipakai untuk memberi sanksi ke karyawan?**
Skill ini tidak dirancang untuk itu, karena sengaja mengarahkan akar masalah ke proses/sistem, bukan ke individu. Untuk tindak lanjut kedisiplinan, gunakan skill **Surat Peringatan Karyawan** (`surat-peringatan-karyawan`) yang terpisah.

**3. Bagaimana kalau saya belum tahu jumlah kerugian pasti?**
Anda tetap bisa memakai skill ini: skill akan menandai bagian itu `[isi: jumlah]` daripada menebak-nebak, supaya angka di laporan tidak dikarang.

---
*Terinspirasi dari struktur `incident-postmortem`, `customer-incident-update`, dan `apology-letter` (MIT, pm-claude-skills), ditulis ulang & diperluas untuk konteks UMKM Indonesia. Rincian di `ATTRIBUTION.md`.*

## Riwayat perubahan

Versi terkini: **1.0.5**. Rincian teknis tiap versi ada di `CHANGELOG.md` di folder skill ini.
