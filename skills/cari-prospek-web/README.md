# Cari Calon Pelanggan, Langsung dari Web

**Sebutkan jenis usaha dan kotanya; dapatkan daftar 10-20 calon pelanggan (prospek) berbukti, 3 prioritas, dan tabel CSV (file tabel) siap tempel.**

Diuji AI penguji independen di OpenClaw dengan pencarian web aktif: 6,7 → 8,2 dari 10 (tanpa skill nama usaha dari direktori publik tanpa prioritas dan sumber per baris; dengan skill tiap usaha ada tautan sumber, kontak bisnis, dan 3 prioritas).

> **Yang Anda butuhkan:** AI agent yang mendukung skill (OpenClaw, Claude Code, Codex, atau Cursor — langganan AI-nya ditanggung sendiri) di komputer Windows/Mac/Linux. Python 3 (bawaan Mac/Linux, unduh gratis di Windows) untuk skrip hitung; tanpa Python skill tetap berjalan dengan hitungan oleh AI. Tidak perlu API key atau akun tambahan dari Komunitech.

## Manfaat
- ✅ **Daftar calon pelanggan terisi sendiri** (butuh alat pencarian web yang aktif di agent Anda). Tidak perlu berjam-jam membuka Google Maps dan situs satu per satu.
- ✅ **Setiap baris ada sumbernya.** URL dan tanggal cek tercantum; yang belum bisa dipastikan ditulis `[belum terverifikasi]`, tidak dikarang (kontak tetap perlu dicek ulang sebelum dihubungi).
- ✅ **Hanya kontak bisnis yang dipublikasikan:** telepon kantor, email umum, WA bisnis yang dipublikasikan. Tanpa nomor pribadi, tanpa beli database.
- ✅ **3 calon pelanggan prioritas** dengan alasan dan satu kalimat pembuka yang menyebut hal spesifik dari usaha mereka.
- ✅ **Tabel CSV (file tabel) siap tempel** ke Excel/Google Sheets.

## Cocok untuk siapa
- Pemilik usaha dan tenaga penjual B2B (jualan ke perusahaan lain) yang ingin menambah calon klien, distributor, atau reseller.
- Freelancer dan agensi yang mencari klien di kota tertentu.
- **Bukan untuk:** menilai daftar yang sudah Anda punya (skill Riset Calon Pelanggan), menulis pesan pembuka lengkap (skill Pesan Prospek WA), scraping (menyedot data otomatis) dengan akun LinkedIn/Instagram, mengambil nomor pribadi, atau kirim WA massal (permintaan ini ditolak, tetapi daftar tetap dibuat dari sumber yang sah).

## Contoh sebelum & sesudah
**Sebelum:** "Cari klien jasa kebersihan kantor di Surabaya" berarti satu sore membuka Maps, menyalin nomor, dan tidak yakin mana yang masih aktif.

**Sesudah:** daftar calon pelanggan dengan alasan cocok, kontak bisnis, dan tautan sumber, tiga prioritas, dan tabel CSV. Contoh nyata (uji OpenClaw dengan pencarian web aktif, 10 Okt 2026): kemasan ramah lingkungan di Bandung menghasilkan 15 calon pelanggan kafe/katering/toko kue yang tampil utuh di chat. Permintaan "scrape grup Facebook/LinkedIn lalu WA massal" ditolak, diganti 14 hotel dari direktori asosiasi (PHRI) dan tidak ada nomor pribadi di tabel. Angka ujinya ada di bagian "Hasil uji" di bawah.

Cuplikan keluaran uji (6 Okt 2026, v1.0.2, dipotong; `examples/01-normal-kemasan-bandung-telegram.md`):

> Sudah saya carikan lewat halaman direktori publik (bukan membuka tiap situs usaha satu-satu). Berikut hasilnya.
>
> **Tabel 15 calon pelanggan** (nama usaha, jenis, alasan cocok, skor, kontak bisnis publik, sumber, tanggal cek) …
>
> **3 prospek prioritas**
> 1. …
> 2. **Cita Rasa Catering** — katering dengan kebutuhan kotak makan harian berulang, cocok untuk kontrak pasokan rutin. *Pembuka:* "Selamat siang, saya melihat Cita Rasa Catering di Komplek Taman Holis Indah — kami sediakan kemasan makanan ramah lingkungan untuk box katering, apakah boleh saya kirim info produknya?"
> 3. **Armor Kopi** — kafe konsep outdoor/alam yang citranya sudah selaras dengan isu ramah lingkungan, jadi pesan jualan lebih mudah diterima. *Pembuka:* "Halo, saya lihat Armor Kopi punya konsep kafe di alam terbuka — mungkin cocok juga pakai kemasan to-go yang ramah lingkungan, boleh saya kirim contohnya?"

Catatan jujur: skill ini bekerja penuh hanya bila agent Anda punya alat pencarian web yang aktif, dan pencarian yang teliti bisa memakan beberapa menit (di uji bot Telegram sekitar 18 menit). Kontak tetap perlu dicek ulang sebelum dihubungi.

## Cara pakai
Tulis misalnya:
- "Carikan 15 calon klien kafe di Bandung untuk jasa kemasan saya."
- "Cari distributor alat kesehatan di Medan."
- Bila agent Anda tidak bisa mencari di web, Anda akan mendapat rencana pencarian dan tabel untuk ditempel balik, lalu daftarnya dirapikan dan diskor.

Hubungi calon pelanggan satu per satu lewat kontak bisnisnya, sebut asal kontak, dan hormati bila mereka menolak.

## Instalasi singkat
Salin folder `cari-prospek-web` ke folder skill platform Anda (OpenClaw, Codex, Claude Code, Cursor). Rincian per platform: `docs/instalasi.md` di paket.

**Hasil uji (angka nyata):** uji OpenClaw 10 Okt 2026 (uji otomatis agent, v1.0.2, pencarian web DuckDuckGo aktif, 4 skenario), skor 1–10 penguji independen: tanpa skill **6,7** → dengan skill **8,2** (LULUS). Sumber: `examples/HASIL-UJI-openclaw-websearch-2026-10-10.md`. Hasil di bot Telegram asli ada di bagian berikutnya.

**Status uji (jujur):** diuji di OpenClaw (uji otomatis agent) dan bot Telegram uji, keduanya dengan alat pencarian web aktif. Tanpa alat pencarian web, skill hanya memberi rencana pencarian. Claude Code, Codex, dan Cursor belum diuji langsung (format skill-nya sama).

## Bukti uji di bot Telegram

Diuji di bot OpenClaw asli (grup uji Komunitech, tautan hanya terbuka untuk anggota grup): gelombang 15, 2026-10-12, dengan pencarian web aktif.
- Skor: 7 tanpa skill, 8,5 dengan skill.
Verdik gelombang: LULUS. Dengan skill setiap usaha ada tautan situs/Google Maps dan catatan nomor bisnis resmi; tanpa skill sudah ada 15 nama dari direktori publik tetapi tanpa prioritas dan tanpa sumber per baris.

## FAQ
**Apakah daftarnya pasti benar?** Setiap baris ditautkan ke sumbernya dan diberi tanggal cek; tetap cek singkat sebelum menghubungi karena info bisa berubah.

**Kenapa tidak boleh scrape LinkedIn/Instagram atau ambil nomor dari grup?** Melanggar aturan platform, berisiko akun diblokir, dan nomor pribadi dilindungi UU PDP. Sumber publik cukup untuk daftar awal yang baik.

**Perlu API key atau instal sesuatu?** Tidak. Pencarian memakai alat web bawaan agent Anda; tanpa itu Anda dapat rencana pencarian. Skrip penyaring opsional hanya butuh Python.

## Catatan
Daftar berisi kontak bisnis dari sumber publik; patuhi UU PDP (UU 27/2022 tentang perlindungan data pribadi) dan hormati bila calon pelanggan menolak. Skill ini tidak mengirim pesan apa pun.

## Riwayat perubahan

Versi terkini: **1.0.2**. Rincian teknis tiap versi ada di `CHANGELOG.md` di folder skill ini.
