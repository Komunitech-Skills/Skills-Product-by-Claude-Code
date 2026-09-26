# 00 — Pembanding tanpa skill vs dengan skill (uji independen Akun B)

Skenario: "Pak Budi (Toko Sari) menjalankan buku-stok, kasir-lokal, crm-wa, absensi-lokal,
buku-piutang, dan kas-umkm di laptopnya sendiri. Ia bertanya: 'Coba lihatkan semua data
usaha saya dari satu tempat — stok, dagangan, piutang, kas, semuanya.'"

## Tanpa skill (agent umum, tanpa `dasbor-lokal`)
Agent tidak tahu lokasi database keenam alat, tidak tahu skema tabelnya, dan tidak tahu
konvensi lintas platform (Windows vs Linux/Mac) maupun aturan keamanan (localhost-only,
immutable). Perilaku yang realistis:
- Menebak-nebak lokasi file (`stok.db`? `data.db`? di folder proyek?), sering salah karena
  lokasi asli ada di `~/KomunitechData/...` per alat.
- Jika berhasil menemukan file, kemungkinan menjalankan `sqlite3` atau membuka koneksi
  **tanpa `mode=ro`** — berisiko menulis tidak sengaja bila agent salah ketik SQL.
- Tidak tahu skema tabel (`nota`, `akun`, `transaksi`, `kontak`, dst.) → butuh eksplorasi
  `.schema` dulu, rawan salah tafsir kolom (mis. lupa mengeluarkan nota `void` dari
  penjualan, atau lupa `sisa > 0 AND jatuh_tempo <= today` untuk piutang).
- Kalau diminta "buka di browser", tidak tahu ada Datasette; kalaupun tahu, tidak otomatis
  mengingatkan `--host 127.0.0.1` — berisiko saran `0.0.0.0` supaya "bisa dibuka dari HP".
- Hasil: butuh banyak percakapan bolak-balik, jawaban tidak konsisten formatnya (uang bisa
  tampil "1700000" bukan "Rp 1.700.000"), dan berisiko keamanan (host publik / tulis tidak
  sengaja).

## Dengan skill `dasbor-lokal`
Perintah tunggal per alat, hasil langsung, tanpa eksplorasi skema:
```
python3 scripts/dasbor.py cari
python3 scripts/dasbor.py query kas-umkm saldo-per-akun
python3 scripts/dasbor.py query buku-piutang piutang-jatuh-tempo
```
Hasil nyata dari data uji (lihat `01-...md`): 6/6 database ditemukan otomatis di lokasi
default, 6/6 canned query menjawab benar (diverifikasi manual — lihat bagian "Verifikasi
angka" di `HASIL-UJI.md`), format uang konsisten "Rp 1.700.000", dan setiap koneksi baca-
saja (`?mode=ro`) — dibuktikan hash file sebelum/sesudah identik meski dicoba `INSERT`.
Saat diminta buka di browser, skill **selalu** menyiapkan `--host 127.0.0.1` + `-i`
(immutable) per database, tidak pernah menyarankan expose ke jaringan.

## Kesimpulan
Skill memberi nilai tambah jelas: hasil benar tanpa tebak-tebakan lokasi/skema, format
konsisten, dan pagar keamanan (read-only + localhost) yang tidak bisa diandalkan dari agent
umum yang menjalankan SQL bebas. Bukan "skor maks. 6" — perbedaan nyata dan terukur.
