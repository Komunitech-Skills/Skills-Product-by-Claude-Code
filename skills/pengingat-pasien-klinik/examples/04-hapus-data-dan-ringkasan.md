# Contoh 4 — Hapus data (hak pasien / UU PDP) dan ringkasan pemilik (data fiktif)

## Pasien minta datanya dihapus
> "Bu Wati minta datanya dihapus semua."
```bash
python3 scripts/pengingat_pasien.py --file pasien/DAFTAR.csv hapus --id 4
```
Pratinjau dulu (belum menghapus apa pun):
```
Akan dihapus PERMANEN:
- #4 Bu Wati (Kontrol, 2026-09-27)
Ulangi perintah yang sama + --ya untuk menghapus sungguhan.
```
Setelah pengguna konfirmasi "ya, hapus":
```bash
python3 scripts/pengingat_pasien.py --file pasien/DAFTAR.csv hapus --id 4 --ya
```
```
Dihapus permanen:
- #4 Bu Wati (Kontrol, 2026-09-27)
```
Menghapus lewat nomor WA (mis. pasien tidak ingat kode) juga bisa: `hapus --wa 0812-4444-5555 --ya`.

## Ringkasan harian untuk pemilik (dikirim ke Telegram lewat OpenClaw)
> "Ringkasan hari ini buat saya, yang aman dikirim ke Telegram."
```bash
python3 scripts/pengingat_pasien.py --file pasien/DAFTAR.csv --hari-ini 2026-09-26 \
  ringkasan --samarkan
```
```
Ringkasan pengingat pasien — Sabtu, 26 September 2026
Terlambat: 0 | Hari ini: 0 | Besok (H-1): 1 | H-3: 0 | Total aktif dijadwalkan: 3
Besok: Pak B. (Vaksin)
(Ringkasan ini TIDAK memuat nomor WA. Draf pesan ada di 'daftar' atau 'draf --id'.)
```
Nama pasien tampil sebagai inisial ("Pak B."), dan nomor WA tidak muncul sama sekali — aman
dikirim ke Telegram lewat jadwal OpenClaw (lihat `references/openclaw-jadwal.md`).

Ringkasan tanpa daftar nama sama sekali (hanya angka):
```bash
python3 scripts/pengingat_pasien.py --file pasien/DAFTAR.csv --hari-ini 2026-09-26 \
  ringkasan --tanpa-nama
```
```
Ringkasan pengingat pasien — Sabtu, 26 September 2026
Terlambat: 0 | Hari ini: 0 | Besok (H-1): 1 | H-3: 0 | Total aktif dijadwalkan: 3
(Ringkasan ini TIDAK memuat nomor WA. Draf pesan ada di 'daftar' atau 'draf --id'.)
```
