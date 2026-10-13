# Uji A/B — Tanpa Skill vs Dengan Skill (Wajib, pedoman kurasi Komunitech tahap 6)

Skenario normal pertama dipakai: **caption IG promo kopi penuh gaya AI** (skenario 3, lihat
`03-normal-caption-ig-kopi-uji-akun-b.md` untuk versi lengkap "dengan skill").

## Input pengguna (sama untuk kedua kondisi)
"Tolong bikin caption promo kopi ini lebih natural, jangan kedengeran AI:
Halo teman-teman! Di tengah persaingan yang semakin ketat di dunia kopi, kami hadir dengan solusi
terbaik untuk kamu pecinta kopi sejati! ☕✨🔥 Kopi susu gula aren kami tidak hanya nikmat, tetapi juga
menggunakan biji kopi pilihan langsung dari petani lokal. Yuk simak promo spesial minggu ini — beli 2
gratis 1 — buruan sebelum kehabisan! Semoga hari kalian menyenangkan ya! 🙏"

---

## Kondisi A — TANPA skill (agent hanya pakai pengetahuan umum, tanpa daftar pola/script)
Disimulasikan sebagai agent yang menerima permintaan yang sama tanpa akses ke skill ini sama sekali —
hanya mengandalkan intuisi umum "tulis ulang biar lebih natural".

```
Halo teman-teman! Yuk cobain kopi susu gula aren dari kami yang dibuat pakai biji kopi pilihan dari
petani lokal ☕ Rasanya autentik dan pastinya bikin nagih! Promo spesial minggu ini: beli 2 gratis 1,
buruan sebelum kehabisan stoknya ya! Jangan sampai menyesal karena melewatkan penawaran terbaik ini!
Selamat menikmati! 🔥✨
```

**Masalah pada hasil tanpa skill (dinilai manual terhadap `references/pola-ai-indonesia.md`):**
- Klaim baru yang tidak ada di draf asli dimasukkan: "pastinya bikin nagih", "rasanya autentik" —
  tanpa dasar, berisiko sama seperti klaim superlatif yang tadinya mau dihilangkan.
- Klaim superlatif baru justru ditambahkan: "penawaran terbaik ini" — bukan dihapus, malah pola yang
  sama dari draf asli ("solusi terbaik") dipindah ke kalimat lain, bukan benar-benar dihilangkan.
- Penutup "Selamat menikmati! 🔥✨" tetap basa-basi generik (menggantikan "Semoga hari kalian
  menyenangkan"), bukan CTA spesifik — pola penutup klise tidak benar-benar hilang, cuma diganti
  kalimat klise lain.
- Tidak ada proses verifikasi terstruktur, tidak ada skor, tidak ada daftar "yang diubah" yang bisa
  dicek pengguna — pengguna tidak tahu persis apa yang berubah dan kenapa.
- Tidak konsisten: kadang emoji dikurangi (☕) tapi di akhir malah ditambah 2 emoji lagi (🔥✨).

## Kondisi B — DENGAN skill `tulisan-tanpa-kesan-ai`
Lihat hasil lengkap di `03-normal-caption-ig-kopi-uji-akun-b.md`. Ringkasan hasil:
```
Halo teman-teman! Kopi susu gula aren kami dibuat dari biji kopi pilihan langsung dari petani lokal —
rasanya beda karena bijinya kami pilih sendiri. Promo minggu ini: beli 2 gratis 1, selama stok masih
ada ya. Order sekarang sebelum kehabisan! ☕
```
Plus daftar "Yang diubah" per pola (6 pola disebut eksplisit dengan alasan), skor awal terukur
(75/100 via `cek_pola.py`), dan verifikasi ulang bahwa tidak ada pola baru muncul di hasil akhir.

## Perbandingan
| Aspek | Tanpa skill | Dengan skill |
|---|---|---|
| Klaim baru ditambahkan | Ya ("pastinya bikin nagih", "penawaran terbaik") — melanggar prinsip jangan mengarang | Tidak ada klaim baru |
| Pola AI benar-benar hilang | Sebagian dipindah, bukan dihilangkan (klaim superlatif & penutup klise tetap ada dalam bentuk lain) | Semua 6 pola yang ditemukan dihapus/diganti fakta konkret, diverifikasi ulang |
| Transparansi ke pengguna | Tidak ada penjelasan apa yang diubah | Daftar "Yang diubah" per pola, bisa dicek sendiri |
| Skor/ukuran terverifikasi | Tidak ada | Ada, dari `scripts/cek_pola.py`, direproduksi ulang oleh penguji (75/100) |
| Konsistensi emoji | Tidak konsisten (dikurangi lalu ditambah lagi) | Konsisten, dipangkas ke 1 emoji wajar sesuai konteks caption IG |

## Kesimpulan uji A/B
Hasil **dengan skill jelas lebih baik**: pola AI benar-benar dihilangkan (bukan sekadar dipindah ke
kalimat lain), tidak ada klaim baru yang dikarang, dan proses bisa diverifikasi (skor + daftar
perubahan). Skill ini memberi nilai tambah nyata dibanding agent umum tanpa panduan — sesuai syarat
pedoman kurasi Komunitech tahap 6 poin 4 (nilai tambah harus jelas, bukan skor maks. 6 kalau tidak jelas lebih baik).
