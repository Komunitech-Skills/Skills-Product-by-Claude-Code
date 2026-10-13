# Cari Calon Pelanggan, Langsung dari Web

**Sebutkan jenis usaha dan kotanya; dapatkan daftar 10-20 prospek berbukti, 3 prioritas, dan CSV siap tempel.**

## Manfaat
- ✅ **Daftar prospek terisi sendiri.** Tidak perlu berjam-jam membuka Maps dan situs satu per satu.
- ✅ **Setiap baris ada sumbernya.** URL dan tanggal cek tercantum; yang belum bisa dipastikan ditulis `[belum terverifikasi]`, tidak pernah dikarang.
- ✅ **Kontak bisnis yang sah saja:** telepon kantor, email umum, WA bisnis yang dipublikasikan. Tanpa nomor pribadi, tanpa beli database.
- ✅ **3 prospek prioritas** dengan alasan dan satu kalimat pembuka yang menyebut hal spesifik dari usaha mereka.
- ✅ **CSV siap tempel** ke Excel/Google Sheets.

## Cocok untuk siapa
- Pemilik usaha dan sales B2B yang ingin menambah calon klien, distributor, atau reseller.
- Freelancer dan agensi yang mencari klien di kota tertentu.
- **Bukan untuk:** menskor daftar yang sudah Anda punya (`riset-calon-pelanggan`), menulis pesan pembuka lengkap (`pesan-prospek-wa`), scraping dengan akun LinkedIn/Instagram, mengambil nomor pribadi, atau kirim WA massal (semua ditolak, tetapi daftar tetap dibuat dari sumber yang sah).

## Contoh sebelum & sesudah
**Sebelum:** "Cari klien jasa kebersihan kantor di Surabaya" berarti satu sore membuka Maps, menyalin nomor, dan tidak yakin mana yang masih aktif.

**Sesudah:** daftar prospek dengan alasan cocok, kontak bisnis, dan tautan sumber, tiga prioritas, dan CSV. Contoh nyata (uji OpenClaw dengan pencarian web hidup, 2026-10-10): kemasan ramah lingkungan di Bandung menghasilkan 15 prospek kafe/katering/toko kue yang utuh di chat. Permintaan "scrape grup Facebook/LinkedIn lalu WA massal" ditolak, diganti 14 hotel dari direktori asosiasi (PHRI) dan tidak ada nomor pribadi di tabel. Skor rata-rata 6,7 tanpa skill menjadi 8,2 dengan skill. Rincian: `examples/HASIL-UJI-openclaw-websearch-2026-10-10.md`.

Catatan jujur: skill ini bekerja penuh hanya bila agent Anda punya alat pencarian web yang aktif, dan pencarian yang teliti bisa memakan beberapa menit (di uji bot Telegram sekitar 18 menit). Kontak tetap perlu dicek ulang sebelum dihubungi.

## Cara pakai
Tulis misalnya:
- "Carikan 15 calon klien kafe di Bandung untuk jasa kemasan saya."
- "Cari distributor alat kesehatan di Medan."
- Bila agent Anda tidak bisa mencari di web, Anda akan mendapat rencana pencarian dan tabel untuk ditempel balik, lalu daftarnya dirapikan dan diskor.

Hubungi prospek satu per satu lewat kontak bisnisnya, sebut asal kontak, dan hormati bila mereka menolak.

## Instalasi singkat
Salin folder `cari-prospek-web` ke folder skill platform Anda (OpenClaw, Codex, Claude Code, Cursor). Rincian per platform: `docs/instalasi.md` di paket.

## Bukti uji di bot Telegram

Diuji di bot OpenClaw asli (grup uji Komunitech, tautan hanya terbuka untuk anggota grup): gelombang 15, 2026-10-12, dengan pencarian web aktif.
- Skor: 7 tanpa skill, 8,5 dengan skill.
Verdik gelombang: LULUS. Dengan skill setiap usaha ada tautan situs/Google Maps dan catatan nomor bisnis resmi; tanpa skill sudah ada 15 nama dari direktori publik tetapi tanpa prioritas dan tanpa sumber per baris.

## FAQ
**Apakah daftarnya pasti benar?** Setiap baris ditautkan ke sumbernya dan diberi tanggal cek; tetap cek singkat sebelum menghubungi karena info bisa berubah.

**Kenapa tidak boleh scrape LinkedIn/Instagram atau ambil nomor dari grup?** Melanggar aturan platform, berisiko akun diblokir, dan nomor pribadi dilindungi UU PDP. Sumber publik cukup untuk daftar awal yang baik.

**Perlu API key atau instal sesuatu?** Tidak. Pencarian memakai alat web bawaan agent Anda; tanpa itu Anda dapat rencana pencarian. Skrip penyaring opsional hanya butuh Python.

## Catatan
Daftar prospek berisi kontak bisnis dari sumber publik; patuhi UU PDP (UU 27/2022) dan hormati bila prospek menolak. Skill ini tidak mengirim pesan apa pun.
