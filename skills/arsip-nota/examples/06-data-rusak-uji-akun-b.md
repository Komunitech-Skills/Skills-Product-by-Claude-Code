# Contoh 6 (uji independen) — Data rusak / input ekstrem

Diuji oleh penguji independen, 26 September 2026, folder sementara. Semua data fiktif.

## 1. Nama file aneh (emoji + karakter terlarang Windows)
File sumber: `nota🧾_toko<bangunan>?.jpg`, vendor diketik pengguna: `Toko "Aneh"/Bangunan*`.
```bash
python3 scripts/arsip.py tambah --file "nota🧾_toko<bangunan>?.jpg" --tanggal 01/09/2026 \
  --vendor 'Toko "Aneh"/Bangunan*' --nominal 100000 --ya --json
```
Hasil: `file_tujuan` = `.../2026-09-01_Toko-AnehBangunan_100000.jpg` — berhasil, tanpa error. Nama file arsip dibentuk dari **tanggal + vendor (dibersihkan) + nominal**, bukan dari nama file asli, jadi karakter aneh/emoji di nama file sumber sama sekali tidak berpengaruh; karakter terlarang Windows (`< > : " / \ | ? *`) di nama vendor otomatis dibuang (`nama_bagian_aman`). **Lulus.**

## 2. File 0 byte
```bash
python3 scripts/arsip.py tambah --file "kosong.jpg" --tanggal 01/09/2026 --vendor "Toko X" --nominal 50000 --json
```
```json
{"ok": false, "error": "File 'in/kosong.jpg' kosong (0 byte), sepertinya rusak/gagal diunduh."}
```
Ditolak sebelum tahap apa pun (bahkan sebelum hitung hash). **Lulus.**

## 3. Duplikat isi sama persis, nama file beda
`nota-a.jpg` diarsipkan (id 2). Salinan persis `nota-a-copy.jpg` (hash SHA-256 identik) dicoba diarsipkan lagi dengan `--ya` (tanpa `--izinkan-duplikat`):
```json
{
  "ok": true, "mode": "tersimpan",
  "perlu_izin": ["izinkan_duplikat"],
  "duplikat": {"id": 2, "tanggal": "2026-09-02", "vendor": "Toko Duplikat", "nominal": 75000, "path_file": "..."}
}
```
Diverifikasi: `jumlah_nota` di indeks **tetap 2** sebelum dan sesudah percobaan ini, tidak ada file baru disalin ke `data/arsip/2026/09/` — jadi secara substansi permintaan **ditolak dengan benar** (deteksi dobel berbasis hash bekerja walau nama file beda).

**Temuan (sedang):** field `"mode"` pada respons di atas berbunyi **`"tersimpan"`** padahal tidak ada apa pun yang benar-benar tersimpan (tidak ada `id` baru, tidak ada file disalin, jumlah nota tidak berubah) — ini terjadi karena kode di `cmd_tambah` (arsip.py baris ±633) menulis `"mode": "pratinjau" if not args.ya else "tersimpan"` pada jalur `perlu_izin`, padahal jalur ini **selalu return sebelum menulis apa pun**, terlepas dari `--ya`. Nilai `mode` yang benar seharusnya tetap `"pratinjau"` (atau nilai lain yang bukan "tersimpan") di jalur ini. Risikonya: agent yang hanya membaca field `mode` (bukan `perlu_izin`) berpotensi salah melaporkan ke pengguna bahwa nota sudah tersimpan padahal belum. Mitigasi saat ini: SKILL.md sudah eksplisit menyuruh agent memeriksa `perlu_izin` dan bertanya dulu sebelum lanjut (Aturan keamanan data #4), jadi dampak praktis kecil selama instruksi itu diikuti — tetap direkomendasikan untuk diperbaiki di kode sebelum rilis.

## 4. Tanggal salah / tidak ada di kalender
`31/02/2026` → `{"ok": false, "error": "Tanggal '31/02/2026' tidak ada di kalender."}`. **Lulus.**

## 5. Tanggal masa depan
`01/01/2027` (hari ini 26/09/2026) → ditolak dengan pesan jelas menyebut tanggal hari ini. **Lulus.**

## 6. Nominal format Indonesia (diuji langsung lewat `parse_nominal()`, diverifikasi manual)
| Input | Hasil `parse_nominal` | Benar? |
|---|---|---|
| `1.250.000` | `1250000` | Ya |
| `Rp 45rb` | `45000` | Ya |
| `4,5jt` | `4500000` | Ya |
| `150.000,50` | `150001` (dibulatkan, flag `dibulatkan=True`) | Ya — 150000,50 dibulatkan ke atas sesuai `ROUND_HALF_UP`, dan diberi tahu lewat peringatan |

## 7. Folder tujuan (`--db`) belum ada
Pratinjau (`tambah` tanpa `--ya`) ke path `does/not/exist/arsip.db` berhasil menampilkan pratinjau dengan `file_tujuan` di folder yang belum ada — tidak error, karena pratinjau tidak butuh folder sudah ada; folder baru dibuat otomatis (`mkdir(parents=True)`) hanya saat benar-benar menulis (`--ya`). **Lulus** (sesuai desain: pratinjau tidak boleh mengubah apa pun di disk).

## 8. Indeks (DB) rusak
- File teks biasa (bukan SQLite) sebagai `--db`: `{"ok": false, "error": "... rusak atau bukan indeks arsip-nota ... Pulihkan: arsip.py backup --daftar ...", "rusak": true}` — pesan berisi langkah pemulihan, tidak crash/traceback. **Lulus.**
- File DB 0 byte: pesan serupa, spesifik menyebut "kosong (0 byte)". **Lulus.**

## Ringkasan
7 dari 8 kasus data rusak/ekstrem ditangani dengan benar dan aman (tidak pernah menulis data salah, tidak pernah crash, pesan error selalu actionable). Satu temuan **sedang** (label `mode: tersimpan` yang tidak akurat pada jalur `perlu_izin` duplikat) direkomendasikan untuk diperbaiki sebelum rilis, meski dampaknya dimitigasi oleh instruksi SKILL.md yang sudah benar.
