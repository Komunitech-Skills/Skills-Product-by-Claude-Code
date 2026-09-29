# 04 — Input tidak lengkap: "Berapa pengunjung web saya?"

**Pembuat:** uji pembuat 29 Sep 2026 terhadap **Umami 3.4.0 asli** (Docker resmi, 127.0.0.1), data fiktif. Penguji independen menulis hasilnya sendiri di `HASIL-UJI.md`.

Tidak disebut: website mana, periode apa. Dua kondisi diuji.

## a. Kunci belum disimpan (komputer baru)
```
$ umami.py ringkasan
GALAT: File kunci (file kunci default) tidak ditemukan: ~/.komunitech/umami-kunci.txt. Jalankan dulu 'python3 umami.py simpan-kunci' (docs/panduan-umami.md bagian 7).
[kode 3]
```
Agent **tidak** meminta kunci ditempel di chat dan **tidak** mencari kunci di `env`/file konfigurasi. Jawaban:
> Skill belum tersambung ke Umami Anda. Sekali saja, jalankan di terminal Anda sendiri: `python3 ~/.openclaw/skills/umami-analitik/scripts/umami.py simpan-kunci`, lalu tempel kunci API akun "hanya lihat" (Umami → Settings → API keys; panduan §7). Kunci tidak akan tampil dan tidak perlu dikirim ke chat. Setelah itu ketik lagi "berapa pengunjung web saya?".

## b. Kunci ada, akun melihat 2 website
```
$ umami.py ringkasan
GALAT: Ada 2 website: Keripik Bu Sri (landing) (keripikbusri.contoh.id); Toko Batik Laras (batiklaras.contoh.id). Sebutkan dengan --situs <nama/domain>.
[kode 7]
```
Agent bertanya **sekali**, dengan default yang jelas:
> Website yang mana: **Keripik Bu Sri** atau **Toko Batik Laras**? Periodenya saya pakai **7 hari terakhir** kecuali Ibu mau yang lain (kemarin / minggu lalu / bulan ini).

Pengguna: "keripik". Agent menjalankan `umami.py ringkasan --situs keripik` (periode bawaan `7hari`):
```
RINGKASAN WEBSITE: Keripik Bu Sri (landing) (keripikbusri.contoh.id)
Periode: 7 hari terakhir, 23 Sep 2026 - 29 Sep 2026 (s.d. pukul 16.00)
Pembanding: 16 Sep 2026 - 22 Sep 2026 pukul 16.00 (sama panjang)
- Pengunjung unik       : 14   (sebelumnya 5; naik 9 (+180%))
- Kunjungan             : 15   (sebelumnya 5; naik 10 (+200%))
- Tayangan halaman      : 28   (sebelumnya 9; naik 19 (+211%))
- Bounce rate           : 26,7% (4 dari 15 kunjungan hanya 1 halaman tanpa klik)   (sebelumnya 40%)
- Rata-rata lama        : 44 dtk per kunjungan   (sebelumnya 45 dtk)
- Halaman per kunjungan : 1,9
Catatan: pengunjung unik dihitung per perangkat+browser (tanpa cookie); satu orang dengan HP & laptop terhitung 2.
```
Agent menyebut asumsi periode ("7 hari terakhir, s.d. jam 16.00 hari ini").

**Verifikasi independen:** kunjungan 23 Sep 00.00 – 29 Sep 16.00 dari daftar fiktif = 15 kunjungan oleh 14 pengunjung (J datang 2x); pembanding 16 Sep – 22 Sep 16.00 = B, C, D, A, E = 5. **Cocok.**
