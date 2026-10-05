# Panduan SiYuan untuk Basis Pengetahuan Usaha

**Komunitech tidak berafiliasi dengan SiYuan/b3log.** SiYuan adalah aplikasi pihak ketiga (lisensi AGPL-3.0, gratis) yang dipasang sendiri oleh pembeli dari situs resminya. Panduan ini adalah karya orisinal Komunitech untuk memasang dan mengamankannya sebelum dipakai bersama skill `siyuan-sop`.

> Diverifikasi 2026-09-26 dari repo resmi (`github.com/siyuan-note/siyuan`) dan uji langsung dengan kernel resmi v3.8.5. Aplikasi bisa berubah; kalau ada langkah yang tidak cocok lagi, kabari Komunitech.

## 1. Apa itu SiYuan & untuk apa dipakai di sini
SiYuan adalah aplikasi catatan/wiki yang **jalan sepenuhnya di komputer sendiri** (data tidak wajib dikirim ke server siapa pun), mirip Notion tapi lokal. Di paket Komunitech, SiYuan dipakai sebagai **basis pengetahuan usaha**: SOP, notulen rapat, dan FAQ toko/klinik (produk, harga, jam buka, kebijakan retur) - yang lalu bisa **dibaca dan dicari oleh AI agent** (OpenClaw/Claude Code/Codex/Cursor) lewat skill `siyuan-sop`, dan dipakai sebagai sumber kebenaran untuk skill `agen-cs-toko`/`balas-chat-cs`.

## 2. Instal (Windows/macOS/Linux)
1. Buka **https://github.com/siyuan-note/siyuan/releases** (halaman rilis resmi - jangan unduh dari situs lain/mirror).
2. Ambil rilis **stabil terbaru** (bukan yang bertanda `alpha`/`beta`), pilih file sesuai OS:
   - **Windows:** `siyuan-x.y.z-win.exe` (installer biasa, ikuti wizard).
   - **macOS:** `siyuan-x.y.z-mac.dmg` (Apple Silicon) atau `siyuan-x.y.z-mac-x64.dmg` (Intel).
   - **Linux:** `siyuan-x.y.z-linux.tar.gz` (ekstrak, jalankan `siyuan` di dalamnya) atau paket `.AppImage`/repo distro bila tersedia.
3. Jalankan aplikasi. Saat pertama kali dibuka, SiYuan akan membuatkan **folder ruang kerja (workspace)** - lokasi defaultnya **`Documents/SiYuan`** di folder pengguna (bisa diganti saat itu juga, atau nanti lewat Settings - About). Semua data (dokumen, gambar) tersimpan di folder ini sebagai file biasa - **inilah yang perlu di-backup**.
4. Buat minimal satu **buku catatan (notebook)**, misalnya "SOP & FAQ Toko".

## 3. Amankan SEBELUM dipakai bersama AI agent (wajib, ±5 menit)
Kernel SiYuan (bagian yang melayani API) secara default **hanya mendengar di `127.0.0.1`** (komputer sendiri) - ini aman selama tidak diubah. Langkah berikut menambah lapis pengaman:

1. **Buka Settings (ikon gerigi) - About (atau menu serupa).** Pastikan opsi semacam **"Serve on network" / "Network serving"** (istilahnya bisa berbeda antar versi) dalam keadaan **MATI**. Kalau menu ini tidak terlihat, berarti secara default sudah tidak melayani jaringan luar - biarkan begitu.
2. **Set kata sandi kunci layar** (di beberapa versi disebut *access authorization code* / *lock screen password*): **Settings - About** atau **Settings - Authentication**. Isi dengan kata sandi yang mudah diingat pemilik tapi tidak ditebak orang lain. Ini lapis pertahanan tambahan.
3. **Ambil token API:** **Settings - Authentication - API token** (di versi lama bisa ada di **Settings - About**). Salin token ini - akan dipakai skill `siyuan-sop`, **BUKAN** kata sandi kunci layar di langkah 2 (dua hal berbeda).
4. **Simpan token dengan aman, JANGAN ditempel di chat AI.** Buka terminal sendiri lalu jalankan:
   ```bash
   python3 <folder-skill>/scripts/siyuan.py simpan-kunci
   ```
   (Windows: `python` atau `py`). Tempel token saat diminta - tersimpan di `~/.komunitech/siyuan-kunci.txt` berizin ketat, tidak tampil di layar/log.
5. **PENTING - baca ini:** menurut pengujian Komunitech (lihat `research/sources/siyuan-2026-09-26.md`), permintaan API dari **program lain di komputer yang sama** (bukan dari peramban web) bisa saja tidak selalu diminta token, tergantung versi. Jadi pembatas keamanan yang **sesungguhnya** bukan hanya token, melainkan: **kernel SiYuan hanya bisa dijangkau dari komputer ini sendiri**. Karena itu:
   - **JANGAN PERNAH** membuka port `6806` ke internet atau jaringan kantor (tidak ada alasan bisnis untuk ini).
   - **JANGAN PERNAH** melakukan **port-forwarding router** ke port 6806.
   - **JANGAN memasang software yang tidak dipercaya** di komputer yang sama dengan SiYuan.
   - **Jangan bagikan akun/login komputer** itu ke orang yang tidak berhak melihat SOP/FAQ usaha.
6. **Jangan memasang plugin pihak ketiga** dari Bazaar/marketplace SiYuan untuk workspace basis pengetahuan ini kecuali sudah ditinjau - per audit Komunitech, ada celah keamanan yang butuh plugin jahat/terkompromi sebagai jalan masuknya (status per 2026-09-26: menunggu rilis stabil perbaikan).
7. **Jangan mengaktifkan fitur "Publish"** (menerbitkan workspace ke web) untuk basis pengetahuan internal ini - fitur itu untuk berbagi catatan publik, bukan untuk data usaha, dan per audit Komunitech ada celah yang butuh fitur ini aktif.

## 4. Sinkronisasi cloud & telemetri (opsional, defaultnya MATI)
- SiYuan punya fitur sinkronisasi cloud berbayar (akun SiYuan) dan opsi S3 sendiri - **keduanya tidak aktif** kecuali pengguna login/mengisi kredensialnya sendiri. Untuk paket ini, **biarkan mati**; cukup pakai backup manual (§5).
- Tidak ditemukan pengiriman data pemakaian tersembunyi pada aplikasi **desktop** (lihat audit). Catatan: aplikasi **mobile** SiYuan (HP) diketahui menyertakan Google Analytics yang menyala secara default - panduan ini **tidak mencakup pemakaian di HP**; pakai SiYuan desktop saja untuk basis pengetahuan usaha.

## 5. Backup (wajib, lakukan rutin)
Cara termudah - **salin folder workspace** (lihat lokasinya di Settings - About) ke tempat lain (drive eksternal/Google Drive/dsb.) secara berkala, misalnya tiap minggu. Cara resmi lain: dari dalam SiYuan, klik kanan buku catatan - **Export** - **.sy.zip** untuk mengekspor satu buku catatan sebagai satu file terkompresi.

## 6. Update
**Settings - About - Check for updates** (atau opsi "Automatically download update installation package" bila ingin otomatis diunduh - tetap butuh konfirmasi pengguna untuk memasangnya). Selalu update ke versi stabil terbaru; per audit 2026-09-26 ada dua celah keamanan yang baru akan tertutup di versi v3.8.6 (masih beta) - pantau rilis stabilnya.

## 7. Uninstall
- **Windows:** Control Panel - Uninstall a program - SiYuan.
- **macOS:** seret aplikasi dari folder Applications ke Trash.
- **Linux:** hapus folder ekstrak/`.AppImage`.
- Folder workspace (data Anda) **tidak ikut terhapus otomatis** - hapus manual bila memang ingin membuang datanya juga (backup dulu bila ragu).

## 8. Kalau bermasalah
| Gejala | Kemungkinan sebab | Solusi |
|---|---|---|
| Skill bilang "tidak bisa terhubung" | Aplikasi SiYuan belum dibuka/masih loading | Buka SiYuan, tunggu sampai tampil, coba lagi |
| Skill bilang "Token API ditolak (401)" | Token salah/sudah diganti | Ambil token baru (§3.3), jalankan `simpan-kunci` lagi |
| Lupa kata sandi kunci layar | - | Ikuti panduan resmi SiYuan untuk reset (butuh akses ke folder workspace); token API tidak berubah karenanya |
| Ingin pindah komputer | - | Salin folder workspace ke komputer baru, pasang SiYuan di sana, buka folder itu sebagai workspace |

---
*Panduan ini karya orisinal Komunitech, ditulis ulang dari riset & pengujian sendiri terhadap kernel resmi SiYuan v3.8.5 (2026-09-26), bukan salinan dokumentasi SiYuan.*
