# Strategi Merek Usaha: Nama, Penawaran, dan Promo Jujur

**Dari "bingung namanya" ke nama yang sudah dinilai dan penawaran yang jujur, lengkap dengan hitungan labanya.**

Diuji AI penguji independen di OpenClaw: 6 → 8,75 dari 10 (nama yang bunyinya mirip pesaing ditandai, laba per botol dihitung, dan "stok tinggal 5" palsu diganti urgensi yang jujur).

> **Yang Anda butuhkan:** AI agent yang mendukung skill (OpenClaw, Claude Code, Codex, atau Cursor — langganan AI-nya ditanggung sendiri) di komputer Windows/Mac/Linux. Python 3 (bawaan Mac/Linux, unduh gratis di Windows) untuk menjalankan skrip pendukung skill ini; tanpa Python skill tetap berjalan, AI mengerjakannya langsung tetapi hasil angka sebaiknya Anda cek ulang. Tidak perlu API key atau akun tambahan dari Komunitech.

## Manfaat
- 10 opsi nama dengan skor 0-100 yang **dihitung skrip** (panjang, suku kata, ejaan, kemiripan dengan merek yang Anda sebut, arti, keunikan), bukan sekadar selera.
- Pengingat cek arti negatif di bahasa daerah dan slang, plus **daftar cek domain (alamat situs), username IG/TikTok, dan merek di PDKI** (Pangkalan Data Kekayaan Intelektual, tempat cek merek terdaftar), langkah demi langkah, termasuk kelas Nice (penggolongan jenis barang/jasa untuk pendaftaran merek).
- Penawaran lengkap: nilai, bonus, garansi, batas waktu/stok yang jujur, nama paket.
- **Laba per unit dihitung** sebelum promo ditulis, jadi tidak jual rugi tanpa sadar.
- Teks siap tempel untuk WhatsApp, Instagram, dan marketplace, dengan ceklis kepatuhan UU Perlindungan Konsumen.

## Cocok untuk siapa
- Pemilik usaha kecil-menengah yang baru mau menamai usaha atau produk.
- Penjual online yang promonya sepi atau labanya tipis.
- Admin/marketing yang butuh penawaran cepat dan jujur.
Tidak cocok: nasihat hukum merek (sengketa, boleh/tidak boleh daftar), desain logo/kemasan.

## Contoh sebelum & sesudah
**Sebelum:** "Sambal saya namanya belum ada. Promonya diskon 30% terus tapi untungnya tipis."

**Sesudah (cukup ketik):** "Bantu cari nama untuk sambal cobek rumahan saya, Malang, dijual lewat Shopee dan WA, pembeli ibu-ibu dan anak kos. Merek yang saya tahu: Sambal Bu Rudy, Sambal Nusantara, ABC Sambal." Lalu minta penawaran: "Sambal cobek 180 g Rp38.000, modal Rp17.000, jual di Shopee (potongan 8%)."

Cuplikan balasan (dipotong; contoh dengan data fiktif dari `examples/01-nama-sambal-malang.md` dan `examples/02-penawaran-sambal.md`):
```
 #  Nama                      Skor  Huruf Suku  Status / catatan
 1  Cabe Gendis               86.0     10    4  layak dicek
 2  Pedas Kuy                 84.0      8    3  layak dicek
 3  Sambalku                  80.0      8    3  layak dicek
…
10  Sambel Pedas Nusantara    60.0     20    8  layak dicek; mirip 'Sambal Nusantara' (80% ejaan)
SETARA: 'Cabe Gendis' dan 'Pedas Kuy' selisih <= 5 poin.
…
LABA per unit       : Rp15.900 (margin 41.8%)
Versi B, diskon 15% tanpa bonus lain: harga tayang Rp32.300, laba Rp10.770 (margin 33,3%). Versi A (bonus, harga penuh) lebih menguntungkan Rp5.130 per botol.
```
Hasil lengkapnya juga memuat tabel cek domain/username/PDKI (belum dicek; Anda yang mengisi) dan penawaran "Paket Sarapan Pedas" (sambal + kartu resep + stiker, garansi ganti rusak) serta teks siap tempel untuk WhatsApp.

## Cara pakai
Ketik permintaan biasa:
- "Bantu cari nama untuk usaha kue kering saya di Bandung."
- "Nama ini mirip merek lain nggak? Merek yang saya tahu: ..."
- "Bikin penawaran sambal Rp38.000, modal Rp17.000, potongan Shopee 8%."

## Penting
Skill ini **tidak** menjamin nama tersedia atau bisa didaftarkan, dan bukan nasihat hukum. Anda yang mengecek domain, username, dan PDKI; konsultan kekayaan intelektual yang menilai risiko merek.

## Instalasi singkat
Salin folder `strategi-merek-usaha` ke folder skills AI agent Anda (OpenClaw, Codex, Claude Code, Cursor). Lokasi lengkap: **`docs/instalasi.md`** (di dalam paket bernama `CARA-INSTAL.md`).

Skrip hitung (opsional; tanpa Python skill tetap berjalan dengan rumus manual): `python3 scripts/skor_nama.py nama.csv --merek "Merek A, Merek B"` dan `python3 scripts/hitung_penawaran.py --harga 38000 --hpp 17000 --platform 8` (Windows: `python` atau `py`).

## Skill pelengkap
`positioning-persona-usaha` (target pembeli & tagline), `luncurkan-produk-baru` (rencana peluncuran), `hitung-hpp` (modal per produk), `harga-jual-marketplace` (harga setelah potongan marketplace), `copy-landing-page` (teks halaman jualan), `promo-kalender` (kalender promo).

**Hasil uji (angka nyata):** uji OpenClaw sebelum/sesudah otomatis agent, 2026-10-01 (uji ulang v1.0.3), skor 1–10 penguji independen. Sumber: `examples/00-openclaw-sebelum-sesudah.md`.
- Rata-rata 2 skenario: tanpa skill **6** → dengan skill **8,75** (LULUS).
- Bot Telegram asli (5 Okt 2026): tanpa skill **6** → dengan skill **8**; rinciannya ada di bagian "Bukti uji di bot Telegram" di bawah.

**Status uji (jujur):** sudah diuji di OpenClaw (uji otomatis agent) dan Claude Code (simulasi agent); bot Telegram asli. Codex dan Cursor belum kami uji langsung. Cek domain/handle/PDKI tetap manual — bukan nasihat hukum merek.

Diadaptasi dari skill open-source (MIT); rincian di `ATTRIBUTION.md`. Tidak berafiliasi dengan pembuat sumber.

## Bukti uji di bot Telegram

Uji terakhir: 5 Okt 2026, di bot OpenClaw asli (grup uji internal Komunitech), dengan pesan yang sama di kedua sisi: promo diskon 20% yang ingin diberi tulisan "stok tinggal 5" dan harga coret. Tanpa skill skor **6** → dengan skill skor **8** (selisih +2): lulus acuan kami, tepat di batas nilai 8.

Pembedanya: dengan skill, bot membuang tulisan "stok tinggal 5" dari teks promosi siap tempel (dipakai hanya bila stoknya memang nyata), memberi 3 pilihan caption, dan menghitung bahwa margin turun dari 48,6% ke 35,7% setelah diskon (untung per unit turun Rp7.000, sekitar 41%). Tanpa skill, bot menaruh "stok tinggal 5, buruan" di teks siap tempel lalu baru bertanya apakah stoknya benar.

Catatan jujur: lulusnya mepet. Bot dengan skill masih menambahkan kata yang tidak Anda sebutkan ("pedas gurih") di caption, tidak menyebut bahwa harga coret hanya sah bila harga itu memang pernah berlaku, dan tidak memberi angka perkiraan biaya stiker. Sebelumnya, uji otomatis agent (1 Okt 2026) menghasilkan 6 → 8,75 untuk skill ini; angkanya ada di bagian Hasil uji di atas.

## FAQ
**Apakah nama pilihan skill ini dijamin tidak dipakai orang lain?**
Tidak. Skill hanya membandingkan dengan merek yang Anda sebutkan dan memberi langkah cek. Hasil akhir ada di pencarian domain, username, dan PDKI yang Anda lakukan.

**Boleh bikin "stok tinggal 3" supaya orang buru-buru beli?**
Hanya bila memang benar. Skill menolak kelangkaan palsu dan menawarkan versi jujur (kuota nyata, batas tanggal yang ditegakkan).

**Apakah harus bisa Python?**
Tidak. Agent yang menjalankan skrip; bila tidak bisa, hitungan manual dengan rumus di `references/`.

## Riwayat perubahan

Versi terkini: **1.0.5**. Rincian teknis tiap versi ada di `CHANGELOG.md` di folder skill ini.
