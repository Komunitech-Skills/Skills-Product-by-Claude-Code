# Contoh 5 (uji independen) — Input tidak lengkap & permintaan luar cakupan

Diuji oleh penguji independen, 26 September 2026.

## A. Input tidak lengkap

### A1. Tanggal & nominal kosong
```bash
python3 scripts/arsip.py tambah --file "struk-spbu-1.jpg" --tanggal "" --vendor "SPBU Pertamina" --nominal "" --ya --json
```
```json
{"ok": false, "error": "Tanggal kosong."}
```
Exit code 1. Tidak ada file yang disalin, tidak ada baris yang tersimpan (dicek: script gagal sebelum tahap tulis). Sesuai SKILL.md: agent wajib menanyakan info wajib (tanggal/vendor/nominal) dalam **satu pesan**, bukan menjalankan dengan nilai kosong — perilaku script (gagal cepat dengan pesan jelas) mendukung pola itu.

### A2. `--nominal` tidak disertakan sama sekali
```bash
python3 scripts/arsip.py tambah --file "struk-spbu-1.jpg" --tanggal 05/09/2026 --vendor "SPBU" --json
```
```
arsip.py tambah: error: the following arguments are required: --nominal
```
Exit code 2 (perintah salah tulis, sesuai dokumentasi kode keluar di SKILL.md). Pesan argparse standar, jelas menyebut field yang kurang.

### A3. `--file` tidak disertakan
Sama polanya: exit code 2, pesan menyebut `--file` wajib.

**Kesimpulan A:** penanganan input kurang sudah baik — selalu gagal (tidak pernah menulis apa pun) dengan pesan yang bisa langsung dipakai agent untuk bertanya balik ke pengguna, kode keluar konsisten (1 = gagal validasi isi, 2 = salah tulis perintah).

## B. Luar cakupan

### B1. "Tolong OCR otomatis semua nota di folder ini, baca sendiri nominalnya"
Tidak ada perintah OCR di script (`python3 scripts/arsip.py --help` hanya menampilkan: init, info, tambah, cari, rekap, duplikat, ekspor, backup, restore). SKILL.md bagian "Kapan TIDAK digunakan" secara eksplisit mengarahkan ke skill `ekstrak-nota-faktur` untuk membaca isi nota. Perilaku benar: agent yang memakai skill ini **tidak bisa** dan **tidak seharusnya** mencoba OCR sendiri dari arsip-nota.

### B2. "Hapus saja nota-nota lama yang sudah lebih dari setahun"
```bash
python3 scripts/arsip.py hapus --db data/arsip.db --json
```
```
arsip.py: error: argument perintah: invalid choice: 'hapus' (choose from 'init', 'info', 'tambah', 'cari', 'rekap', 'duplikat', 'ekspor', 'backup', 'restore')
```
Tidak ada perintah hapus sama sekali di parser — sesuai Aturan keamanan data #1 di SKILL.md ("File nota TIDAK PERNAH dihapus"). Permintaan ini secara struktural tidak bisa dijalankan lewat script, memaksa agent menolak/menjelaskan batasan alih-alih mengarang cara menghapus (mis. lewat `os.remove` manual) — desain yang aman.

**Kesimpulan B:** dua permintaan luar cakupan (OCR otomatis, hapus nota) keduanya **tidak bisa dijalankan** oleh script (tidak ada perintah untuk itu), memaksa agent mengikuti batasan SKILL.md alih-alih berimprovisasi dengan cara yang berisiko.
