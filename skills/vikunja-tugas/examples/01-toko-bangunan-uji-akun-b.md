# Skenario 1 (uji Akun B) — Toko Bangunan, tim 5 orang

**Lingkungan uji:** Vikunja **v2.6.0 ASLI** (binary resmi `vikunja-v2.6.0-linux-amd64`, unduh dari
`https://dl.vikunja.io/vikunja/v2.6.0/`, SHA-256 **dicocokkan OK** terhadap file `.sha256` yang
disertakan di paket unduhan itu sendiri — lihat catatan verifikasi di `HASIL-UJI.md`), dijalankan
sungguhan terikat ke `127.0.0.1:3456`, database SQLite baru. Token API dibuat lewat REST API
(bukan lewat UI, karena UI browser tidak tersedia di lingkungan uji ini) dengan izin
`projects: read_all, read_one, projectusers` + `tasks: read_all, read_one, create, update`,
disimpan lewat `simpan-kunci` milik skill sendiri. Tanggal acuan sistem: **Sabtu, 26 September 2026**.

## Perintah pengguna 1: "tugas apa yang telat?"
```
$ python3 vikunja.py terlambat
TUGAS TERLAMBAT
Proyek: semua proyek
Jumlah: 2
- Tagih pelanggan telat (jatuh tempo 20 Sep 2026; proyek: Toko Bangunan Sinar Jaya)
- Stok opname harian (jatuh tempo 26 Sep 2026; proyek: Toko Bangunan Sinar Jaya)
```
**Verifikasi independen:** "Tagih pelanggan telat" due `2026-09-20T10:00:00Z` — jelas < sekarang, benar telat.
"Stok opname harian" due `2026-09-26T10:00:00Z` (17:00 WIB) — saat perintah dijalankan jam 18:21 WIB,
jadi sudah lewat jam jatuh tempo hari ini → **benar** masuk kategori "terlambat" (skrip membandingkan
instant penuh, bukan hanya tanggal). Tugas yang sama juga tetap muncul di `hari-ini` (lihat di bawah) —
ini konsisten dengan desain skrip (dua laporan punya definisi berbeda: "jatuh tempo hari ini" vs
"sudah lewat waktu jatuh tempo"), bukan bug, tapi sebaiknya SKILL.md menyebutkan eksplisit bahwa
tugas bisa tampil di kedua daftar sekaligus.

## Perintah pengguna 2: "tambahkan tugas untuk Toko Bangunan: cek stok cat tembok, jatuh tempo Jumat, prioritas tinggi, tugaskan ke budi"
```
$ python3 vikunja.py tambah --proyek "Toko Bangunan Sinar Jaya" \
    --judul "Cek stok cat tembok" --tenggat "Jumat" --prioritas 3 --ke budi
PRATINJAU TAMBAH TUGAS
1.
   Judul : Cek stok cat tembok
   Proyek: Toko Bangunan Sinar Jaya (id 4)
   Tenggat: Jumat, 2 Oktober 2026
   Prioritas: 3 (tinggi)
   Ditugaskan ke: budi

Belum disimpan. Ulangi perintah yang sama + --ya untuk menyimpan ke Vikunja.
```
**Verifikasi tanggal independen:** acuan Sabtu 26 Sep 2026 → Jumat berikutnya = 2 Oktober 2026. Benar (dihitung manual: 26→Jumat terdekat setelah Sabtu adalah +6 hari = 2 Okt).

Setelah "ya":
```
$ python3 vikunja.py tambah --proyek "Toko Bangunan Sinar Jaya" \
    --judul "Cek stok cat tembok" --tenggat "Jumat" --prioritas 3 --ke budi --ya
CATATAN: tugas #3 tersimpan, tapi GAGAL menugaskan ke 'budi': 401 dari Vikunja: token salah/kedaluwarsa/
dihapus, ATAU token tidak punya izin untuk aksi ini ... Pesan server: missing, malformed, expired or
otherwise invalid token provided.
TERSIMPAN 1 TUGAS DI VIKUNJA:
- #3 Cek stok cat tembok (proyek id 4)
```
**Temuan PENTING (lihat HASIL-UJI.md #1):** tugas tetap tersimpan (sesuai dokumentasi), tapi penugasan
`--ke` GAGAL walau token sudah punya semua izin yang disebut panduan §6 ("Tasks Assignees" tidak
ketemu padanan nama JSON API yang valid — lihat percobaan di HASIL-UJI.md). Dites ulang dengan sesi
JWT pemilik (bukan token API `tk_...`) untuk endpoint yang sama (`PUT /tasks/3/assignees`) — BERHASIL.
Jadi kegagalan ini konsisten & dapat direproduksi: endpoint assignee di Vikunja 2.6.0 menolak token API
`tk_...` sama sekali (kode error "invalid token provided", bukan soal kurang izin), bukan galat skrip.
Skrip menangani ini dengan benar (tugas tetap tersimpan, error disampaikan apa adanya, tidak mengulang
otomatis) — tapi SKILL.md/README mengklaim fitur `--ke` "diuji ... dengan Vikunja 2.6.0 ASLI ...
penugasan (--ke)" berhasil; pada pengujian independen ini TIDAK berhasil dengan token API mana pun
yang saya buat. Perlu klarifikasi dari pembuat (lihat prioritas #1 di HASIL-UJI.md).

## Perintah pengguna 3: "ringkasan tugas tim toko bangunan"
```
$ python3 vikunja.py ringkasan --proyek "Toko Bangunan Sinar Jaya"
RINGKASAN TUGAS TERBUKA

budi (1 tugas):
  - Cek stok cat tembok (tinggi; jatuh tempo 2 Okt 2026; PIC: budi)

BELUM ADA PIC (2 tugas):
  - Tagih pelanggan telat (jatuh tempo 20 Sep 2026)
  - Stok opname harian (jatuh tempo 26 Sep 2026)
```
Catatan: "budi" muncul sebagai PIC di sini karena penugasan itu saya lakukan langsung lewat sesi
JWT pemilik (untuk membuktikan endpoint itu sendiri berfungsi), BUKAN lewat `--ke` skrip (yang gagal
di atas). Pengelompokan per-nama dan daftar "BELUM ADA PIC" terpisah bekerja dengan benar.

## Perintah pengguna 4: tandai selesai
```
$ python3 vikunja.py selesai --id 2
PRATINJAU TANDAI SELESAI: #2 Stok opname harian
Belum disimpan. Ulangi perintah yang sama + --ya untuk menyimpan.
$ python3 vikunja.py selesai --id 2 --ya
SELESAI: #2 Stok opname harian ditandai selesai di Vikunja.
$ python3 vikunja.py selesai --id 2 --ya
Tugas #2 (Stok opname harian) memang sudah SELESAI sebelumnya.
```
Benar: pratinjau wajib, penyelesaian ulang tidak dianggap error (sesuai dokumentasi).
