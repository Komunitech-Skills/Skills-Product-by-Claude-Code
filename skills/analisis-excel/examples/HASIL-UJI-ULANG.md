# Hasil Uji Ulang — analisis-excel

## Uji ulang 1.0.14 (2026-09-30)

**Penguji:** agent independen (bukan pembuat). Yang dibaca hanya folder skill ini, ditambah bagian 4 catatan internal kurator (tidak disertakan dalam paket) sebagai konteks temuan.
**Lingkungan:** salinan skill di scratchpad (`uji-ae-1014/skill`), dijalankan di Linux dengan Python 3 standar (tanpa openpyxl). Semua data uji fiktif dan dibuat penguji.
**Fokus:** perbaikan temuan "menimpa file `--keluar` diam-diam" (script dan SKILL.md langkah 6).

### Skor: 9/10

Alasan: pengaman timpa bekerja di semua subperintah yang menulis. Tanpa `--timpa`, script keluar dengan kode 2, isi lama tetap utuh, dan pesan `GAGAL` berbahasa awam menyebut `--timpa`. Dengan `--timpa`, penulisan berhasil. File input tidak bisa ditimpa lewat variasi path biasa (relatif, `./`, absolut, `..`, `//./`, symlink). Singkatan opsi ditolak. Regresi 142 tes lulus. Angka di 3 skenario normal cocok dengan hitungan independen. Instruksi SKILL.md sudah tegas. Nilai dikurangi 1 karena satu celah tepi: file input masih bisa ditimpa lewat hard link, dan kemungkinan juga lewat beda huruf besar/kecil di macOS (temuan T1).

### 1. Pengaman timpa file

Setiap perintah dijalankan dengan `ada.csv` yang berisi "KEEP", pertama tanpa lalu dengan `--timpa`:

| Subperintah | Tanpa `--timpa` | Dengan `--timpa` |
|---|---|---|
| `bersihkan --keluar ada.csv` | kode 2, isi "KEEP" utuh | kode 0, tertulis |
| `bersihkan` (nama bawaan `data-bersih.csv` sudah ada) | kode 2, isi "KEEP" utuh | kode 0, tertulis |
| `pivot` | kode 2, utuh | kode 0 |
| `top` | kode 2, utuh | kode 0 |
| `tren` | kode 2, utuh | kode 0 |
| `ringkas` | kode 2, utuh | kode 0 |
| `banding` (dua periode) | kode 2, utuh | kode 0 |
| `banding --file-b` | kode 2, utuh | kode 0 |
| `profil` | kode 2, utuh | kode 0 |

Pesan yang muncul: `GAGAL: File keluaran sudah ada: ada.csv. Pakai nama lain atau tambahkan --timpa bila pengguna sudah setuju menimpa.`

**File input tidak bisa ditimpa walau memakai `--timpa`.** Semua percobaan di bawah keluar dengan kode 2 dan pesan "File keluaran tidak boleh menimpa file asli". md5 `data.csv` tidak berubah.
- `bersihkan`/`pivot` dengan `--keluar` berupa `data.csv`, `./data.csv`, path absolut, `../w/data.csv`, `<abs>//./data.csv`, dan symlink `link.csv → data.csv`.
- `banding --file-b data2.csv` dengan `--keluar` berupa `data2.csv`, `./data2.csv`, dan path absolut.
- `banding link.csv ... --keluar data.csv`: input berupa symlink, keluaran menunjuk file target symlink itu.

**Kasus lain:**
- `--tim`, `--timp`, dan `--t` ditolak (`unrecognized arguments`, kode 2). Isi file tetap utuh.
- Symlink menggantung (`dang.csv → nowhere.csv`) dianggap sudah ada dan ditolak tanpa `--timpa`. Ini perilaku aman.
- `--keluar` berupa folder dengan `--timpa`: `GAGAL: Gagal menulis 'dirx' ... Is a directory`, kode 2, tanpa traceback.

### 2. Regresi

- `python3 -B tests/uji_regresi.py`: **Ran 142 tests, OK** (64,5 dtk). Sudah termasuk `UjiTimpaFileKeluaran`.
- **Normal 1, CSV** (`data.csv`, 6 transaksi toko bangunan):
  - `pivot --grup Kategori`: Cat 585.000 (40,5%), Besi 500.000 (34,6%), Semen 360.000 (24,9%), total 1.445.000.
  - `tren`: Agu 515.000, Sep 930.000 (+80,6%), rata-rata 722.500.
  - Hitungan penguji: 275+310=585; 150+90+120=360; 585/1445=40,48%; 930/515−1=80,58%. Semua cocok.
  - Peringatan "periode tidak penuh" untuk Agu (mulai tgl 3) dan Sep (akhir tgl 28) tepat.
- **Normal 2, XLSX** (`cabang.xlsx`, dibuat dengan zipfile, sheet 'Rekap'):
  - `pivot`: Surabaya Rp 30.250.000 (39,0%), Bandung 26.250.000 (33,9%), Medan 21.000.500 (27,1%), total 77.500.500.
  - `ringkas`: rata-rata Omzet 12.916.750, median 13.125.000; Biaya jumlah 52.250.000, rata-rata 8.708.333, median 8.700.000.
  - Hitungan penguji cocok. Median Omzet = (12,5 jt + 13,75 jt)/2. Median Biaya = (8,3 jt + 9,1 jt)/2.
- **Normal 3, CSV format Excel Indonesia** (`;`, `1.250.000,50`):
  - `top --n 3`: Toko Maju 2.310.750, Bu Rina 1.250.001, Bu Ani 1.005.000.
  - `ringkas`: jumlah Rp 5.890.751 (nilai sebenarnya 5.890.750,75), rata-rata 1.178.150.
  - Hitungan penguji cocok, dengan pembulatan ke rupiah terdekat sesuai standar library.
- **Input rusak:** XLSX terpotong, CSV 0 byte, file tidak ada, CSV dengan kutip tidak ditutup, dan kolom grup yang salah. Semuanya menghasilkan `GAGAL: ...` berbahasa awam dengan saran (Save As, perbaiki kutip, daftar kolom tersedia), kode 2, tanpa traceback.

### 3. Perilaku SKILL.md

Simulasi: pengguna berkata "langsung aja simpan ke laporan.csv", padahal `laporan.csv` sudah ada.
- Langkah 6 menyuruh agent mengecek dulu apakah file `--keluar` sudah ada. Bila ada, agent bertanya "File X sudah ada, timpa atau simpan sebagai X-2?".
- Langkah 6 juga menyatakan "Jangan menimpa tanpa jawaban tegas; 'langsung aja' bukan izin menimpa", dan `--timpa` hanya dipakai setelah pengguna setuju.
- Kalimat "langsung aja" sudah diubah menjadi "...dan file yang sudah ada tidak pernah ditimpa tanpa izin".
- Walau agent lupa mengecek, script tetap menolak tanpa `--timpa`. Pesan GAGAL-nya ("tambahkan --timpa bila pengguna sudah setuju") mengarahkan agent untuk bertanya.
- **Hasil: jelas.** Agent yang patuh akan bertanya dulu. Permintaan perbaikan 1–3 di dokumen koordinasi sudah terpenuhi.

### Temuan

**T1 (sedang–rendah): file input bisa ditimpa lewat hard link, dan kemungkinan lewat beda kapital di macOS.**
- Penyebab: `periksa_keluaran` membandingkan `os.path.realpath`, yang tidak mengenali dua path berbeda yang menunjuk inode yang sama.
- Bukti: `ln data2.csv hard2.csv`, lalu `banding data.csv --file-b data2.csv --nilai Jumlah --keluar hard2.csv --timpa` menghasilkan kode 0. Setelah itu `md5sum -c` melaporkan `data2.csv: FAILED`, artinya file input kedua tertimpa.
- Beda kapital: di Linux (case-sensitive) `--keluar DATA.csv` membuat file baru, dan itu benar. Di macOS (APFS/HFS+ case-insensitive), `realpath` tidak menyeragamkan kapital. Akibatnya `DATA.csv` kemungkinan besar lolos pemeriksaan "file asli", ditolak hanya sebagai "sudah ada", dan dengan `--timpa` menimpa `data.csv`. Kasus ini **tidak diuji** karena tidak ada sistem file case-insensitive di lingkungan uji.
- Syaratnya tetap `--timpa`, yang hanya dipakai setelah pengguna setuju, jadi risiko nyata kecil.
- Saran: tambahkan `os.path.exists(path) and os.path.exists(a) and os.path.samefile(path, a)` di samping pembandingan realpath. Tambahkan satu tes regresi hard link.

**T2 (kecil): `daftar --keluar baru.csv` diterima tetapi tidak menulis apa pun** (kode 0, tanpa pesan).
- `tulis_csv_hasil` juga diam-diam tidak menulis bila tabel hasil kosong.
- Akibatnya agent bisa mengira file sudah dibuat.
- Saran: beri catatan "tidak ada tabel untuk disimpan; --keluar diabaikan", atau tolak `--keluar` untuk `daftar`.

### Kesimpulan

Perbaikan 1.0.14 **lulus**. Temuan GAGAL di verifikasi perilaku (bagian 4) sudah tertutup, baik di script maupun di SKILL.md. T1 dan T2 disarankan untuk patch berikutnya dan tidak menghalangi rilis.

### Catatan revisi 1.0.15 (2026-09-30, oleh kurator, bukan penguji)
- T1: `periksa_keluaran` kini juga memakai `os.path.samefile`, jadi hard link ke file asli ditolak walau `--timpa`. Kasus beda huruf besar-kecil di macOS/Windows ikut tertutup lewat cara yang sama, tetapi belum diuji di sistem itu.
- T2: `--keluar` tanpa tabel hasil menambahkan peringatan "file ... TIDAK dibuat".
- Tes regresi baru `UjiHardLinkDanTabelKosong` (2 tes); seluruh `tests/uji_regresi.py` lolos (144 tes).
- Skor tidak diubah (9/10 dari penguji). Perubahan ini kecil dan tidak mengubah perilaku lain.
