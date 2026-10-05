# Panduan Pasang hledger untuk UMKM (bahasa awam)

hledger adalah program pembukuan **gratis dan open-source** (lisensi GPL-3.0). Semua catatan keuangan disimpan di **satu file teks** di komputer Anda sendiri: tidak ada biaya bulanan, tidak perlu internet, tidak dititipkan ke perusahaan lain. Panduan ini menyiapkan hledger agar bisa dipakai skill **hledger Usaha** (`hledger-usaha`).

> **Kabar baik:** skill `hledger-usaha` **tetap bisa mencatat dan membuat laporan walau hledger belum dipasang** (memakai pembaca bawaan). Memasang hledger menambah pemeriksaan resmi, tampilan web lokal (hledger-web), dan kemampuan membaca file jurnal yang lebih rumit.

> **Tidak ingin repot?** Komunitech menyediakan **jasa setup berbayar**: pemasangan hledger, buku awal dengan saldo usaha Anda, aturan mutasi bank Anda, jadwal laporan bulanan ke Telegram, dan backup otomatis. Hubungi admin komunitech.com.

> Komunitech tidak berafiliasi dengan proyek hledger. hledger adalah karya Simon Michael dan kontributornya. Komunitech **tidak** mendistribusikan hledger; Anda mengunduhnya sendiri dari sumber resmi.

**Status panduan (26 September 2026):** versi yang diuji **hledger 1.52.4**. Komunitech mengunduh berkas Linux resmi dari halaman rilis GitHub, mencocokkan checksum SHA-256 dengan yang tertera di halaman rilis (cocok), lalu menjalankan hledger, hledger-web, dan seluruh perintah skill dengan file jurnal bertemplate Indonesia. **Langkah Windows dan Mac belum dicoba langsung** di komputer Windows/Mac (disusun dari halaman resmi hledger.org dan isi berkas rilis). Bila tampilan Anda berbeda, ikuti tulisan di layar dan hubungi kami.

## Daftar isi
1. Sebelum mulai
2. Pasang di Windows
3. Pasang di Mac
4. Pasang di Linux
5. Membuat buku (file jurnal) pertama
6. Memberi tahu hledger letak buku (LEDGER_FILE)
7. Backup & pemulihan
8. Opsional: hledger-web (tampilan di browser, hanya komputer ini)
9. Memperbarui hledger
10. Masalah umum

---

## 1. Sebelum mulai
| Kebutuhan | Keterangan |
|---|---|
| Komputer | Windows 10/11 64-bit, Mac (chip Apple atau Intel), atau Linux 64-bit. Ruang kosong ±300 MB |
| Waktu | ±15–30 menit |
| Python 3.8+ | Untuk skill (gratis di python.org; saat memasang di Windows centang **Add Python to PATH**) |
| Internet | Hanya untuk mengunduh. Setelah itu hledger jalan tanpa internet |

Istilah: **jurnal** = file buku Anda (`usaha.journal`). **Akun** = pos keuangan (Kas, Bank, Piutang, dst.). **Terminal** = jendela perintah (Windows: *Command Prompt*; Mac: *Terminal*).

### Checksum resmi 1.52.4 (untuk memastikan file asli)
Halaman rilis menampilkan "sha256" di samping tiap berkas. Untuk versi 1.52.4:

| Berkas | SHA-256 |
|---|---|
| `hledger-windows-x64.zip` | `2921b1c61b4d8ff32622b5eff01de4d5e7e166cb456e89002d42640f474b6fde` |
| `hledger-mac-arm64.tar.gz` (Mac chip Apple M1/M2/M3/M4) | `c90a0fe4537439e958ce530f7175d937749f5f126759c94c1212774abe9eb971` |
| `hledger-mac-x64.tar.gz` (Mac Intel) | `1e4d4114ca065f6f0f6e45453ec30571eb00989bf34d439c80042368ae22c49c` |
| `hledger-linux-x64.tar.gz` | `f76a2e4088e162b7658e43077502569d5a6fdacd219b19bfb9aab6588b69643a` (dicek Komunitech: cocok) |

Versi lebih baru → pakai angka yang tertera di halaman rilisnya sendiri. Angka tidak sama = **jangan dipakai**, hapus file dan unduh ulang.

---

## 2. Pasang di Windows
Tingkat kesulitan: **mudah**.

### 2.1 Unduh dari sumber resmi
1. Buka **https://hledger.org/install.html** → bagian binary resmi, atau langsung **https://github.com/hledgerorg/hledger/releases**.
2. Di rilis teratas bertanda *Latest* (saat panduan ditulis: **1.52.4**), bagian **Assets**, klik `hledger-windows-x64.zip`.
3. **Jangan** mengunduh dari situs lain.

### 2.2 Cek keaslian (checksum)
1. Buka **Command Prompt** (tekan tombol Windows, ketik `cmd`, Enter).
2. Ketik (sesuaikan bila folder unduhan Anda berbeda):
   ```
   certutil -hashfile "%USERPROFILE%\Downloads\hledger-windows-x64.zip" SHA256
   ```
3. Bandingkan deretan angka-huruf yang muncul dengan tabel di bagian 1 (huruf besar/kecil tidak masalah).
- ✅ **Berhasil:** sama persis.
- ❌ **Beda:** hapus file, unduh ulang dari halaman resmi.

### 2.3 Ekstrak & taruh di folder tetap
1. Klik kanan file zip → **Extract All** → isi tujuan `C:\hledger` → **Extract**.
2. Pastikan di dalam `C:\hledger` ada `hledger.exe` (dan `hledger-web.exe`). Bila ada folder di dalam folder, pindahkan file `.exe` ke `C:\hledger` langsung.

### 2.4 Daftarkan ke PATH (agar bisa dipanggil dari mana saja)
1. Tekan tombol Windows, ketik **"environment"**, pilih **Edit environment variables for your account** (Edit variabel lingkungan untuk akun Anda).
2. Di bagian atas (*User variables*), pilih **Path** → **Edit** → **New** → ketik `C:\hledger` → **OK** → **OK**.
3. **Tutup** semua Command Prompt, buka yang baru, ketik:
   ```
   hledger --version
   ```
- ✅ **Berhasil:** muncul `hledger 1.52.4, windows-x86_64` (atau versi lebih baru).
- ❌ **"'hledger' is not recognized"** → langkah 2.4 belum tersimpan atau Command Prompt belum dibuka ulang.
- ❌ **Windows SmartScreen / antivirus memblokir** → hanya izinkan bila checksum di 2.2 cocok.

> Alternatif yang juga tercantum di hledger.org: `winget install -e --id simonmichael.hledger` (satu perintah, butuh winget/App Installer). Belum dicoba Komunitech.

---

## 3. Pasang di Mac
Tingkat kesulitan: **sedang** (ada satu langkah izin keamanan Mac).

### 3.1 Pilih berkas yang sesuai
Menu Apple (logo apel di kiri atas) → **About This Mac / Tentang Mac Ini**:
- Tertulis **Chip Apple M1/M2/M3/M4** → unduh `hledger-mac-arm64.tar.gz`
- Tertulis **Processor Intel** → unduh `hledger-mac-x64.tar.gz`

Dari **https://github.com/hledgerorg/hledger/releases** (rilis teratas, bagian **Assets**).

### 3.2 Cek keaslian
Buka **Terminal** (Cmd + Spasi, ketik "Terminal"), lalu:
```bash
shasum -a 256 ~/Downloads/hledger-mac-arm64.tar.gz
```
(ganti nama file bila Intel). Bandingkan dengan tabel bagian 1.

### 3.3 Ekstrak & pasang
```bash
mkdir -p ~/hledger
tar xzf ~/Downloads/hledger-mac-arm64.tar.gz -C ~/hledger
echo 'export PATH="$HOME/hledger:$PATH"' >> ~/.zshrc
```
Tutup Terminal, buka lagi, lalu `hledger --version`.

- ❌ **"cannot be opened because the developer cannot be verified" / "tidak dapat dibuka"** → buka **System Settings → Privacy & Security**, gulir ke bawah, klik **Open Anyway / Tetap Buka** untuk `hledger`, lalu jalankan lagi. Lakukan hanya bila checksum di 3.2 cocok. Ulangi untuk `hledger-web` bila dipakai.
- ❌ **"command not found"** → Terminal belum dibuka ulang, atau baris PATH belum masuk ke `~/.zshrc`.

> Alternatif bila Anda sudah memakai Homebrew: `brew install hledger` (tercantum di hledger.org). Belum dicoba Komunitech.

---

## 4. Pasang di Linux
```bash
cd ~/Downloads
sha256sum hledger-linux-x64.tar.gz        # bandingkan dengan tabel bagian 1
mkdir -p ~/.local/bin
tar xzf hledger-linux-x64.tar.gz -C ~/.local/bin hledger hledger-web
hledger --version
```
Berkas diunduh dari **https://github.com/hledgerorg/hledger/releases**. Bila `hledger` tidak ditemukan, tambahkan `export PATH="$HOME/.local/bin:$PATH"` ke `~/.bashrc` lalu buka terminal baru. (Langkah ini yang dicoba Komunitech: berhasil, `hledger 1.52.4, linux-x86_64`.)

---

## 5. Membuat buku (file jurnal) pertama

### 5.1 Cara termudah: minta AI
Setelah skill `hledger-usaha` terpasang, ketik ke AI agent Anda:
> "Mulai pembukuan hledger untuk usaha saya, nama Kopi Sari, rekening BCA. Mulai 1 September 2026. Saldo per 31 Agustus: kas di laci 2 juta, BCA 10 juta, stok 3 juta, utang KUR 5 juta."

AI akan membuat folder **`Pembukuan`** di folder pengguna Anda (`C:\Users\NAMA\Pembukuan` / `/Users/NAMA/Pembukuan`) berisi:

| Isi | Fungsi |
|---|---|
| `usaha.journal` | Buku Anda (file teks) |
| `aturan-bank.rules` | Kata kunci untuk mengelompokkan mutasi bank (boleh diubah) |
| `impor/` | Salinan rapi mutasi bank yang sudah dimasukkan |
| `ekspor/` | Buku kas untuk laporan SAK EMKM |
| `backup/` | Cadangan |

### 5.2 Akun bawaan (berbahasa Indonesia)
| Akun | Artinya |
|---|---|
| **Aset:Kas** | Uang tunai di laci/brankas |
| **Aset:Bank:BCA** (dst.) | Saldo rekening usaha |
| **Aset:Piutang Usaha** | Uang pelanggan yang belum dibayar |
| **Aset:Persediaan** | Nilai stok barang/bahan |
| **Aset:Peralatan** | Mesin, etalase, laptop, kendaraan usaha |
| **Utang:Usaha** / **Utang:Bank** | Utang ke pemasok / pinjaman bank-KUR |
| **Modal:Saldo Awal / Setoran / Prive** | Modal pemilik; prive = uang usaha yang dipakai pribadi |
| **Pendapatan:Penjualan / Jasa / Lain-lain** | Uang dari jualan, jasa, bunga/cashback |
| **HPP:Pembelian** | Harga pokok: beli barang dagang/bahan baku |
| **Beban:Gaji / Sewa / Listrik Air Internet / ...** | Biaya operasional |

### 5.3 Seperti apa isi file-nya?
Anda **tidak perlu** menyentuh file ini (AI yang menulis), tetapi bentuknya sederhana:
```
2026-09-01 Penjualan harian kopi
    Aset:Kas                                        Rp 1.250.000
    Pendapatan:Penjualan                           -Rp 1.250.000
```
Artinya: kas bertambah Rp 1.250.000 dari penjualan. Setiap transaksi harus berjumlah nol (itulah "pembukuan berpasangan"), jadi salah hitung langsung ketahuan.

### 5.4 Melihat laporan sendiri (opsional)
Di Command Prompt/Terminal (setelah bagian 6):
```
hledger is -p 2026-09          (laba rugi September)
hledger bs                     (neraca)
hledger bal Aset:Kas           (saldo kas)
hledger check accounts         (periksa buku)
```
Tampilan hledger membulatkan ke rupiah; angka yang disimpan tetap persis sampai sen.

---

## 6. Memberi tahu hledger letak buku (LEDGER_FILE)
Skill sudah otomatis memakai `Pembukuan/usaha.journal`. Langkah ini hanya agar **hledger dan hledger-web** yang Anda jalankan sendiri langsung membuka buku yang sama.
- **Windows** (Command Prompt): `setx LEDGER_FILE "%USERPROFILE%\Pembukuan\usaha.journal"` lalu buka Command Prompt baru.
- **Mac**: `echo 'export LEDGER_FILE="$HOME/Pembukuan/usaha.journal"' >> ~/.zshrc`
- **Linux**: `echo 'export LEDGER_FILE="$HOME/Pembukuan/usaha.journal"' >> ~/.bashrc`

⚠️ Bila Anda sudah memakai LEDGER_FILE untuk buku lain (mis. keuangan pribadi), jangan diganti; skill akan memakai LEDGER_FILE itu. Minta AI selalu memakai `--jurnal` ke buku usaha.

---

## 7. Backup & pemulihan
Buku Anda hanyalah file kecil, jadi backup sangat mudah.
1. **Otomatis per perubahan:** setiap kali AI menyimpan transaksi, versi sebelumnya disimpan sebagai `usaha.journal.sebelum-ubah`.
2. **Backup bertanggal:** ketik ke AI "backup pembukuan saya" → salinan bertanggal-jam, mis. `backup/usaha-20260926-160500.journal`, + aturan bank, dicek sama persis dengan aslinya.
3. **Di luar komputer (wajib, seminggu sekali):** salin **seluruh folder `Pembukuan`** ke flashdisk atau penyimpanan cloud pilihan Anda. Laptop hilang/rusak = buku tetap selamat.
4. **Memulihkan:** tutup hledger-web bila menyala, ganti `usaha.journal` dengan file backup (ganti namanya menjadi `usaha.journal`), lalu minta AI "cek pembukuan saya" (atau `hledger check`).

Jangan menyimpan buku di folder yang disinkronkan dua komputer sekaligus sambil dua-duanya mencatat: perubahan bisa saling menimpa.

---

## 8. Opsional: hledger-web (tampilan di browser, hanya komputer ini)
hledger-web menampilkan buku Anda di browser: daftar transaksi, saldo, grafik sederhana.
```
hledger-web -f "%USERPROFILE%\Pembukuan\usaha.journal" --serve --allow=view      (Windows)
hledger-web -f ~/Pembukuan/usaha.journal --serve --allow=view                     (Mac/Linux)
```
Lalu buka **http://127.0.0.1:5000** di browser. Hentikan dengan **Ctrl + C** di jendela perintah.

Aturan keamanan (penting):
- hledger-web **tidak punya kata sandi**. Bawaannya hanya bisa dibuka dari komputer ini (`127.0.0.1`), dan itu harus tetap begitu. **Jangan** menambah `--host 0.0.0.0`, jangan membuka port di router, dan jangan memakai layanan "tunnel" untuk mengaksesnya dari internet.
- Pakai `--allow=view` (hanya lihat). Pencatatan tetap lewat AI/skill agar setiap transaksi diperiksa dan dicadangkan.
- Jika Windows Firewall bertanya izin jaringan untuk `hledger-web.exe`, pilih **Cancel/Batal**; browser di komputer ini tetap bisa membuka.

(Dicoba Komunitech di Linux: hledger-web 1.52.4 hanya mendengarkan `127.0.0.1`, halaman & data akun terbuka di browser lokal.)

---

## 9. Memperbarui hledger
Unduh rilis baru dengan langkah yang sama (cek checksum dari halaman rilisnya), timpa file lama. Skill akan memberi tanda "belum diuji Komunitech" untuk versi selain 1.52.4, tetapi tetap berjalan; cocokkan satu-dua angka dengan `hledger bal` setelah memperbarui. File jurnal Anda tidak berubah.

---

## 10. Masalah umum
| Gejala | Penyebab | Solusi |
|---|---|---|
| `'hledger' is not recognized` / `command not found` | PATH belum diatur atau terminal belum dibuka ulang | Ulangi 2.4 / 3.3 / 4, buka terminal baru |
| Mac: "developer cannot be verified" | Pengaman Gatekeeper | Privacy & Security → Open Anyway (setelah checksum cocok) |
| `Strict account checking ... has not been declared` | Akun dipakai tanpa didaftarkan (biasanya karena file diedit manual) | Minta AI "cek pembukuan"; tambahkan baris `account Nama:Akun` atau perbaiki salah ketik |
| `could not balance this transaction` | Transaksi tidak berjumlah nol (diedit manual) | Perbaiki baris yang disebut, atau pulihkan dari `.sebelum-ubah`/backup |
| `balance assertion failed` | Pengecekan saldo (`= Rp ...`) tidak cocok | Ada transaksi terlewat/dobel sebelum tanggal itu |
| Galat tentang encoding/karakter | File bukan UTF-8 (mis. disimpan ulang dengan aplikasi lain) | Simpan ulang sebagai UTF-8, atau pulihkan dari backup |
| hledger-web: port 5000 dipakai | Program lain memakai port itu | Tambah `--port 5055` |
| Angka di hledger bulat, di skill ada sen | Tampilan hledger dibulatkan (`commodity Rp 1.000,`) | Normal; angka tersimpan tetap persis |

---
Lisensi hledger: GPL-3.0-or-later (kode sumber: https://github.com/hledgerorg/hledger). Panduan dan skill ini adalah karya Komunitech, terpisah dari hledger.
