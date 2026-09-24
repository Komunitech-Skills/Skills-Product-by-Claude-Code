# Panduan Pasang Stirling-PDF untuk UMKM (bahasa awam)

Stirling-PDF adalah program **gratis dan open-source** (inti berlisensi MIT) untuk
mengolah PDF: gabung, pisah, kompres, OCR, watermark, kunci sandi, dan banyak lagi.
Program ini jalan **di komputer Anda sendiri**: file PDF tidak diunggah ke internet,
dan tidak ada biaya bulanan untuk fitur intinya. Panduan ini menyiapkan Stirling-PDF
agar bisa dipakai skill **PDF Lokal** (`pdf-lokal`).

> **Tidak ingin repot?** Komunitech menyediakan **jasa setup berbayar**: pemasangan
> Stirling-PDF (termasuk versi lengkap dengan OCR bahasa Indonesia), pengecekan
> keamanan, dan penyalaan otomatis setiap komputer dihidupkan. Hubungi admin
> komunitech.com.

**Status panduan (24 September 2026):** Komunitech menjalankan langsung **Stirling-PDF
v2.14.3 lewat Docker** (jalur "self-hosted" resmi, image `ghcr.io/stirling-tools/
stirling-pdf`) untuk menguji seluruh perintah skill `pdf-lokal` - semua berhasil.
**Aplikasi desktop resmi (.exe/.dmg/.deb) BELUM dicoba klik langsung oleh Komunitech**
(lingkungan pembuatan skill ini tidak bisa menjalankan aplikasi jendela/GUI); langkah
di bawah untuk aplikasi desktop disusun dari dokumentasi resmi docs.stirlingpdf.com
(diakses 2026-09-24). Bila tampilan di komputer Anda berbeda, ikuti tulisan di layar
dan hubungi kami.

**Temuan penting dari dokumentasi resmi yang perlu Anda tahu SEBELUM memilih jalur
pemasangan:** aplikasi desktop dalam mode bawaan ("Local-only") **tidak menyertakan
OCR** (menjadikan PDF hasil scan bisa dicari teksnya) maupun konversi dokumen kantor -
untuk itu aplikasi akan minta Anda masuk akun "Stirling Cloud" (layanan online, bukan
lokal) atau menyambung ke server sendiri. Kalau Anda **hanya butuh gabung/pisah/
kompres/putar/watermark/kunci-sandi**, aplikasi desktop (Jalur A) sudah cukup. Kalau
Anda **juga butuh OCR** (mis. untuk resi/nota hasil scan), langsung pakai **Jalur B
(Docker)** - tetap gratis & 100% di komputer Anda, ini yang dipakai Komunitech saat
menguji skill.

## Daftar isi
1. Sebelum mulai
2. Jalur A - Aplikasi Desktop (Windows/macOS/Linux) - mudah, tanpa OCR
3. Jalur B - Docker (semua OS) - disarankan bila butuh OCR
4. Menyalakan & mengecek Stirling-PDF setiap hari
5. Keamanan (login, API key, hanya localhost)
6. Menyambungkan aplikasi desktop ke server Docker (opsional, dapat keduanya)
7. Pembaruan
8. Masalah umum

---

## 1. Sebelum mulai
| Kebutuhan | Keterangan |
|---|---|
| Komputer | Windows 10/11, macOS, atau Linux. RAM ≥ 4 GB, ruang kosong ≥ 1-2 GB |
| Waktu | Jalur A: ±5 menit. Jalur B (Docker): ±15-20 menit bila Docker belum terpasang |
| Python 3.8+ | Untuk skill `pdf-lokal` (gratis di python.org; saat memasang di Windows centang **Add Python to PATH**) |
| Docker Desktop (hanya Jalur B) | Gratis untuk pemakaian pribadi/UMKM kecil, unduh di docker.com |

Istilah: **Stirling-PDF** = programnya. **Docker** = cara menjalankan program dalam
"kotak" terpisah yang rapi, dipakai banyak software open-source. **API/port 8080** =
"pintu" tempat skill `pdf-lokal` bicara dengan Stirling-PDF, alamatnya
`http://localhost:8080` (localhost = komputer sendiri, tidak bisa diakses dari luar).

---

## 2. Jalur A - Aplikasi Desktop (mudah, tanpa OCR)
Cukup untuk: gabung, pisah, kompres, putar, watermark, kunci/buka sandi PDF.
**Tidak** untuk: OCR, rapikan-resi mungkin ikut terbatas (lihat catatan tiap OS).

### Windows
1. Unduh installer resmi: https://files.stirlingpdf.com/win-installer.exe (link resmi
   dari docs.stirlingpdf.com). **Jangan** unduh dari situs lain.
2. Jalankan file `.exe`, ikuti langkah di layar. Terpasang ke
   `C:\Program Files\Stirling-PDF`.
3. Buka dari **Start Menu**, cari "Stirling PDF".
- ✅ **Cek berhasil:** aplikasi terbuka, tampil halaman utama dengan kartu-kartu tool
  (Merge, Split, Compress, dst.).
- ❌ **Kalau gagal:** Windows SmartScreen memblokir → klik **More info → Run anyway**
  (hanya karena file dari files.stirlingpdf.com, sumber resmi). Antivirus memblokir →
  izinkan folder instalasi, sumbernya resmi.

### macOS
1. Unduh: https://files.stirlingpdf.com/mac-installer.dmg (universal, jalan di
   Apple Silicon maupun Intel).
2. Buka file `.dmg`, seret ikon Stirling-PDF ke folder **Applications**.
3. Buka dari Launchpad/Applications.
- ✅ **Cek berhasil:** aplikasi terbuka normal.
- ❌ **Kalau gagal:** muncul peringatan "pengembang tidak dikenal" (Gatekeeper) →
  buka **System Settings → Privacy & Security**, cari pesan soal Stirling-PDF, klik
  **Open Anyway**, lalu buka aplikasinya lagi.

### Linux
Pilih salah satu sesuai distro:
```bash
# Debian/Ubuntu
wget https://files.stirlingpdf.com/linux-installer.deb
sudo apt install ./linux-installer.deb

# Fedora/RHEL
wget https://files.stirlingpdf.com/linux-installer.rpm
sudo dnf install ./linux-installer.rpm
```
- ✅ **Cek berhasil:** aplikasi "Stirling PDF" muncul di menu aplikasi & bisa dibuka.
- ❌ **Kalau gagal:** `dpkg`/`dnf` menolak karena dependensi → jalankan
  `sudo apt --fix-broken install` (Debian/Ubuntu) lalu ulangi. Kalau masih gagal,
  langsung pakai Jalur B (Docker) di bawah - untuk Linux justru sering lebih mudah.

### Setelah terpasang (semua OS)
- ✅ **Cek Stirling-PDF menyala:** buka browser, ketik `http://localhost:8080` →
  tampil halaman Stirling-PDF. Atau jalankan `python3 scripts/pdf.py cek` dari skill
  `pdf-lokal` → harus tertulis "Stirling-PDF HIDUP".
- ❌ **Kalau gagal terhubung:** pastikan aplikasi Stirling-PDF sedang dibuka (bukan
  ditutup ke tray). Coba tutup total lalu buka ulang aplikasinya.

---

## 3. Jalur B - Docker (disarankan bila butuh OCR)
Ini jalur yang dipakai Komunitech untuk menguji skill `pdf-lokal` secara langsung,
jadi paling terjamin cocok. Sedikit lebih teknis tapi hanya perlu disalin-tempel.

### 3.1 Pasang Docker Desktop (lewati bila sudah ada)
1. Unduh di https://www.docker.com/products/docker-desktop/ sesuai OS Anda, pasang
   seperti aplikasi biasa, lalu buka Docker Desktop sekali agar mesinnya menyala.
- ✅ **Cek berhasil:** ikon Docker Desktop menyala hijau/"Running" di system tray.
- ❌ **Kalau gagal:** Windows minta aktifkan **WSL2** → ikuti tautan yang muncul di
  installer Docker (proses otomatis, minta restart komputer sekali).

### 3.2 Jalankan Stirling-PDF
Buka Terminal (macOS/Linux) atau PowerShell (Windows), salin-tempel:
```bash
docker run -d --name stirling-pdf --restart unless-stopped \
  -p 8080:8080 \
  -v stirling-data:/configs \
  ghcr.io/stirling-tools/stirling-pdf:latest
```
`--restart unless-stopped` membuat Stirling-PDF otomatis menyala lagi setiap Docker
Desktop dinyalakan (mis. setelah komputer di-restart) - tidak perlu ketik ulang.

- ✅ **Cek berhasil:** buka `http://localhost:8080` di browser → tampil halaman
  Stirling-PDF. Atau jalankan `python3 scripts/pdf.py cek` → tertulis versi & "UP".
- ❌ **Kalau gagal:**
  - "port is already allocated" → sesuatu sudah memakai port 8080. Ganti perintah
    jadi `-p 8090:8080`, lalu set `STIRLING_URL=http://localhost:8090` sebelum
    memakai skill.
  - "Cannot connect to the Docker daemon" → Docker Desktop belum menyala, buka dulu.
  - Unduhan macet/lambat → ulangi perintah `docker run ...`, Docker melanjutkan
    unduhan yang belum selesai.

Perintah di atas **secara default TIDAK mengaktifkan login** (sesuai perilaku standar
image Docker resmi untuk pemakaian pribadi) - lihat bagian Keamanan di bawah untuk
opsi menyalakan login bila komputer dipakai bersama orang lain.

---

## 4. Menyalakan & mengecek Stirling-PDF setiap hari
- **Jalur A (Desktop):** cukup buka aplikasinya seperti aplikasi biasa.
- **Jalur B (Docker):** kalau memakai `--restart unless-stopped`, otomatis menyala
  begitu Docker Desktop menyala (dan Docker Desktop sendiri bisa diatur menyala
  otomatis saat komputer dihidupkan, lewat Settings Docker Desktop). Kalau tidak,
  jalankan `docker start stirling-pdf`.
- **Cek cepat kapan saja:** `python3 scripts/pdf.py cek` (dari folder skill
  `pdf-lokal`) atau buka `http://localhost:8080` di browser.

---

## 5. Keamanan (login, API key, hanya localhost)
- **Bawaan (default):** tanpa login, mendengarkan hanya untuk komputer sendiri lewat
  `localhost:8080`. Ini AMAN selama komputer Anda tidak dipakai bersama orang yang
  tidak dipercaya dan port 8080 tidak sengaja dibuka ke internet/jaringan kantor
  (jangan lakukan port forwarding router ke port ini).
- **Kalau komputer dipakai bersama (mis. komputer kasir bersama)** dan ingin
  menambah kunci: nyalakan login dengan menambah `-e SECURITY_ENABLELOGIN=true` di
  perintah `docker run` (Jalur B), lalu buka `http://localhost:8080`, login pertama
  kali dengan `admin`/`admin` (segera ganti sandinya di menu Account).
  Ambil **API key** lewat ikon gerigi (⚙️) kanan atas → **Account Settings** → salin
  "API Key", lalu sebelum memakai skill jalankan (contoh Windows PowerShell):
  ```powershell
  $env:STIRLING_API_KEY="tempel-api-key-di-sini"
  ```
  (macOS/Linux: `export STIRLING_API_KEY="..."`)
- ✅ **Cek berhasil (login aktif):** `python3 scripts/pdf.py cek` tetap berhasil
  setelah `STIRLING_API_KEY` diisi.
- ❌ **Kalau gagal:** pesan "butuh login/API key" → API key salah/belum di-set,
  ulangi salin dari Account Settings (pastikan tidak ada spasi tambahan).
- **Jangan** mengubah `-p 8080:8080` menjadi alamat yang bisa diakses dari internet
  (mis. lewat penerus port router) - Stirling-PDF dirancang untuk dipakai di
  komputer/jaringan lokal sendiri, bukan server publik.

---

## 6. Menyambungkan aplikasi desktop ke server Docker (opsional)
Ingin tampilan aplikasi desktop yang rapi TAPI juga bisa OCR? Pasang **Jalur A**
untuk tampilannya dan **Jalur B** untuk mesinnya, lalu sambungkan:
1. Buka aplikasi desktop Stirling-PDF → ikon gerigi (⚙️) → **Settings → Connection**.
2. Pilih **Self-hosted server**, isi alamat `http://localhost:8080` (atau port lain
   bila diubah di langkah 3.2), simpan.
- ✅ **Cek berhasil:** menu OCR di aplikasi desktop tidak lagi minta login Cloud.
- ❌ **Kalau gagal:** pastikan Jalur B (Docker) sedang menyala (`docker ps` harus
  menampilkan `stirling-pdf` berstatus `Up`).

---

## 7. Pembaruan
- **Jalur A:** aplikasi desktop biasanya memberi notifikasi update sendiri; atau
  unduh ulang installer terbaru dari tautan di bagian 2 dan pasang menimpa yang lama.
- **Jalur B:** 
  ```bash
  docker pull ghcr.io/stirling-tools/stirling-pdf:latest
  docker stop stirling-pdf && docker rm stirling-pdf
  # lalu jalankan ulang perintah "docker run ..." di bagian 3.2
  ```
- Setelah update, jalankan `python3 scripts/pdf.py cek` untuk pastikan versi baru
  terbaca dan skill tetap bisa terhubung.

---

## 8. Masalah umum
| Gejala | Kemungkinan sebab | Solusi |
|---|---|---|
| `python3 scripts/pdf.py cek` bilang "Tidak bisa menghubungi" | Stirling-PDF belum dibuka/mati | Buka aplikasinya (Jalur A) atau `docker start stirling-pdf` (Jalur B) |
| Perintah `ocr` gagal terus (404) | Pakai aplikasi desktop mode Local-only (tidak ada OCR) | Pindah ke Jalur B (Docker), atau sambungkan desktop ke Docker (bagian 6) |
| OCR jalan tapi hasil bahasa Indonesia kurang akurat | Paket bahasa `ind` belum terpasang di server (default hanya Inggris/Prancis/Jerman/dll.) | Di aplikasi/menu OCR Stirling-PDF, cari opsi unduh paket bahasa tambahan, pilih Indonesian/`ind` |
| "port is already allocated" saat `docker run` | Port 8080 dipakai program lain | Pakai `-p 8090:8080` lalu set `STIRLING_URL=http://localhost:8090` |
| Skill bilang butuh `STIRLING_API_KEY` | Login diaktifkan di server | Ikuti bagian 5 untuk ambil & set API key |
| File PDF "terkunci"/gagal diproses padahal yakin filenya benar | File memang berpassword, atau rusak | Buka dulu dengan perintah `buka-kunci` (kalau tahu sandinya) bila memang berpassword; kalau bukan, coba buka file itu di pembaca PDF biasa dulu untuk pastikan tidak rusak |

**Sumber resmi yang dirujuk panduan ini** (diakses 2026-09-24): docs.stirlingpdf.com
(halaman Installation/Windows, Installation/Mac, Installation/Unix, Configuration/
Security, FAQ), github.com/Stirling-Tools/Stirling-PDF, dan pengujian langsung
Komunitech terhadap Stirling-PDF v2.14.3 lewat Docker.
