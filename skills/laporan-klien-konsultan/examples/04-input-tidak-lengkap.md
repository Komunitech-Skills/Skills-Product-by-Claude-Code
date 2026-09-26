# Skenario 04 (input tidak lengkap / data rusak) — Penanganan error

## 4a. Mencatat tanpa `--proyek`
```bash
python3 scripts/laporan_klien.py --file run04/log.csv catat --klien "CV Sinar" \
  --pekerjaan "Bikin laporan keuangan"
```
```
laporan_klien.py catat: error: the following arguments are required: --proyek
exit=2
```
**Penilaian:** Ditolak dengan jelas, tidak menebak nama proyek. Sesuai `SKILL.md` (proyek wajib).
Menurut `SKILL.md` §Input, bila info wajib kurang, agent seharusnya **tanya sekali** ke pengguna
sebelum memanggil script — argparse di sini hanya jaring pengaman lapis kedua bila agent lupa.

## 4b. Mencatat tanpa `--klien`
```
laporan_klien.py catat: error: the following arguments are required: --klien
exit=2
```
Sama seperti 4a — ditolak jelas.

## 4c. Minta laporan untuk file yang belum pernah dibuat sama sekali
```bash
python3 scripts/laporan_klien.py --file run04/tidak-ada.csv laporan --klien "CV Sinar"
```
```
Error: File log 'run04/tidak-ada.csv' tidak ditemukan. Catat pekerjaan dulu dengan perintah
`catat`, atau jalankan `init` untuk membuat file kosong.
exit=1
```
**Penilaian:** Pesan jelas, tidak membuat laporan kosong seolah valid.

## 4d. Nama klien salah ketik (klien ada di file, tapi typo saat minta laporan)
```bash
python3 scripts/laporan_klien.py --file run04/log.csv catat --klien "CV Sinar Abadi" \
  --proyek "Audit" --pekerjaan "Cek neraca" --jam 2
python3 scripts/laporan_klien.py --file run04/log.csv laporan --klien "CV Sinarr"
```
```
Error: Tidak ada catatan untuk klien 'CV Sinarr' di 'run04/log.csv'. Klien yang tercatat:
CV Sinar Abadi.
exit=1
```
**Penilaian:** Bagus — menyebutkan nama klien yang benar-benar tercatat, membantu pengguna
menyadari typo tanpa harus membuka file CSV manual. Sesuai `SKILL.md` ("jangan membuat laporan
kosong yang seolah valid").

## 4e/4f. Format jam yang TIDAK didukung: `"1:30"` dan `"90 menit"`
```bash
python3 scripts/laporan_klien.py --file run04/log.csv catat --klien "CV Sinar Abadi" \
  --proyek "Audit" --pekerjaan "Rapat" --jam "1:30"
# Error: Jam '1:30' bukan angka. Contoh yang benar: 2 atau 2.5 (atau 2,5). exit=1

python3 scripts/laporan_klien.py --file run04/log.csv catat --klien "CV Sinar Abadi" \
  --proyek "Audit" --pekerjaan "Rapat" --jam "90 menit"
# Error: Jam '90 menit' bukan angka. Contoh yang benar: 2 atau 2.5 (atau 2,5). exit=1
```
**Temuan (lihat HASIL-UJI.md #2):** Script sengaja hanya menerima angka desimal (titik/koma),
sesuai dokumentasi. Pesan error sudah jelas dan memberi contoh format benar, jadi tidak
membingungkan pengguna teknis yang membaca stderr. Tapi `SKILL.md` **tidak secara eksplisit**
menyuruh agent mengonversi ucapan lisan umum ("1 jam 30 menit", "90 menit", "sejaman setengah")
ke angka desimal sebelum memanggil script — ini bergantung pada agent menyimpulkan sendiri.
Risiko rendah untuk model yang kuat, tapi sebaiknya ditambahkan satu kalimat eksplisit di SKILL.md
supaya konsisten di semua platform/model.

## Data rusak di file CSV (bukan lewat `catat`, disunting manual/rusak dari luar)

### File CSV kosong (hanya header)
Laporan tetap dibuat, kosong dan jujur (bukan mengarang isi), `catatan` menjelaskan tidak ada
data pada periode itu. **Sesuai desain.**

### File CSV benar-benar 0 byte (tanpa header)
Tidak error — dibaca sebagai 0 baris, laporan kosong dibuat seperti kasus di atas. Perilaku ini
**longgar** (tidak menolak file tanpa header sama sekali) tapi tetap aman: tidak pernah mengarang
isi, hanya melaporkan kosong. Tidak dianggap bug, tapi dicatat sebagai temuan minor.

### Kolom hilang (header tanpa kolom `jam`)
```
Error: File log 'run04/rusak-kolom.csv' tidak berkolom ['jam'] -- pastikan header persis:
tanggal,klien,proyek,pekerjaan,jam,status,kendala,butuh_dari_klien.
exit=1
```
**Bagus** — menyebutkan kolom persis yang hilang.

### Jam negatif yang disisipkan langsung ke CSV (melewati validasi `catat`)
```
Error: Baris 2 'jam-negatif.csv': Jam tidak boleh negatif.
exit=1
```
**Bagus** — validasi tetap berjalan saat membaca file, bukan hanya saat menulis lewat `catat`
(mengantisipasi file yang diedit manual di Excel/Sheets).

### Tanggal tidak valid (`31/13/2026`) & status tidak valid (`ngasal`) di CSV
Keduanya ditolak dengan pesan yang menyebut baris & file secara spesifik ("Baris 2
'tanggal-rusak.csv': ..."). **Sesuai desain** ("File log rusak/kolom tidak sesuai → script
menyebutkan baris & kolom yang bermasalah").

## Status
**Lulus dengan satu catatan perbaikan minor** (konversi format jam lisan → desimal sebaiknya
disebut eksplisit di `SKILL.md` sebagai tanggung jawab agent). Tidak ada crash/traceback pada
seluruh kasus input tidak lengkap/rusak yang diuji.
