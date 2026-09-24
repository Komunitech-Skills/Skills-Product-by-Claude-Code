# Checklist riset proyek kripto (due diligence) -- FAKTA SAJA, TANPA KESIMPULAN BELI/JUAL

Isi setiap baris dengan fakta + sumber (tautan). Kolom yang tidak ditemukan sumbernya:
tulis **"tidak ditemukan / perlu dicek"** -- jangan diisi perkiraan atau opini.
Tutup selalu dengan disclaimer di `SKILL.md`. Format ini dipakai agent untuk menyusun
hasil riset di Langkah C `SKILL.md`, bukan diserahkan mentah-mentah ke member sebagai
formulir kosong.

## 1. Tim & organisasi
- Nama tim/pendiri, identitas terverifikasi (LinkedIn/rekam jejak publik) atau anonim?
- Ada perusahaan/yayasan resmi di baliknya? Terdaftar di mana?
- Riwayat proyek sebelumnya dari tim yang sama (kalau ada)?

## 2. Tokenomics (ekonomi token)
- Total suplai, suplai beredar saat ini, jadwal *unlock*/vesting ke depan (sumber:
  whitepaper/dokumentasi resmi + explorer blockchain).
- Alokasi token: berapa persen ke tim, investor, komunitas, treasury?
- Ada mekanisme *burn*/deflasi, atau justru inflasi berkelanjutan?

## 3. Audit kontrak & keamanan
- Sudah diaudit firma keamanan mana? Tautan laporan audit resminya?
- Kalau belum ada audit publik, tulis itu apa adanya -- ini fakta penting, bukan opini.
- Ada riwayat *exploit*/peretasan sebelumnya? Bagaimana ditangani?

## 4. Likuiditas & perdagangan
- Terdaftar di exchange mana saja? Berizin resmi Indonesia (PAKD OJK) atau hanya
  exchange luar negeri?
- Volume perdagangan 24 jam & kedalaman *order book* (dari data publik CoinGecko/
  exchange, sebutkan sumbernya & jam datanya -- jangan dari ingatan).

## 5. Status legal di Indonesia
Lihat `references/regulasi.md` untuk dasar hukum yang sudah diverifikasi (per tanggal di
file itu, DIKOREKSI setelah uji independen menemukan beberapa kesalahan di draf pertama).
Poin yang perlu dicek per proyek:
- Ada **DUA** bursa aset keuangan digital di Indonesia, masing-masing dengan Daftar Aset
  Keuangan Digital (DAKD) SENDIRI: **CFX (PT Central Finansial X)** dan **ICEX (PT Fortuna
  Integritas Mandiri)**. Koin ini perlu dicek di **kedua** daftar itu, bukan cuma satu --
  status "tidak ada di DAKD CFX" TIDAK berarti "tidak ada di DAKD manapun".
- **PAKD = Pedagang Aset Keuangan Digital** (exchange berizin OJK yang menjual/
  memfasilitasi jual-beli aset kripto) -- istilah ini BUKAN "Penyelenggara Perdagangan"
  (istilah payung yang juga mencakup bursa, lembaga kliring, dan kustodian). Pakai istilah
  yang tepat saat menulis hasil riset.
- Cara cek konkret: buka daftar aset resmi di situs bursa (mis. cfx.co.id -> halaman
  Daftar Aset Kripto) atau ICEX, atau tanya langsung ke PAKD berizin yang dipakai member.
  Kalau tidak bisa diakses/dipastikan saat riset, tulis **"perlu dicek ke ojk.go.id / DAKD
  bursa berizin"**, jangan menebak status legalnya. **Jangan mengutip nomor pasal spesifik**
  kecuali sudah diverifikasi ulang dari teks resmi peraturan (lihat catatan di
  `references/regulasi.md` §2).
- Apakah proyek ini menawarkan skema investasi (mis. *staking* dengan imbal hasil tetap,
  program referral berjenjang) yang berpotensi masuk kategori investasi ilegal/skema
  Ponzi di luar cakupan aset kripto biasa? Ini butuh kehati-hatian ekstra (lihat §6).
  Dugaan skema ilegal bisa dilaporkan member ke OJK (kontak 157) atau Satgas PASTI.

## 6. Perhatian (tanda skema penipuan/pump -- edukasi netral, BUKAN sinyal jual)
Tandai kalau ditemukan (jelaskan sebagai fakta yang perlu diketahui, tanpa menyimpulkan
"karena itu jangan beli" -- itu tetap keputusan member):
- Janji imbal hasil tetap/pasti besar (mis. "%X per bulan dijamin") -- ciri klasik skema
  Ponzi, aset kripto asli tidak bisa menjamin imbal hasil tetap.
- Tekanan waktu berlebihan ("buru-buru sebelum kehabisan", "harga naik 10x minggu depan").
- Program referral berjenjang sebagai sumber utama "keuntungan" (bukan dari produk/layanan
  nyata).
- Token baru tanpa audit, tim anonim total, dan komunitas yang melarang pertanyaan kritis
  (dihapus/di-*ban* kalau bertanya soal risiko).
- Klaim kemitraan/dukungan tokoh/lembaga besar tanpa konfirmasi resmi dari pihak yang
  diklaim.

## Format penutup wajib
```
Sumber yang dipakai: <daftar tautan>
Kolom yang belum bisa diverifikasi: <daftar, kalau ada>
Informasi, bukan nasihat investasi. Keputusan & risiko sepenuhnya milik Anda.
```
