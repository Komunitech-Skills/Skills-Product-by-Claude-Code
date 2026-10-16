# Gelombang Telegram 18 — 2026-10-16 (bot kedua)

Keputusan otomatis **90** (2026-10-16). Bot uji kedua `@KTclaude2bot` (OpenClaw, config 2026.10.2, model router Komunitech `ninerouter/komunitech`), grup uji internal Komunitech, topik baru 1590–1599 buatan bot penguji (genap = TANPA, topik dengan `skills: []`; ganjil = DENGAN). Pesan: `alat-uji/pilot/msgs-g18b.json` (identik di kedua sisi kecuali topik; arsip-nota punya giliran ke-2 "ya" di topik DENGAN, sesuai alur pratinjau di SKILL.md); topik: `pilot/topik-g18b.json`; balasan: `pilot/updates-g2.jsonl` (getUpdates, thread 1590–1599, balasan terpecah digabung berurutan, pesan "Working" diabaikan); id kirim: `alat-uji/sent-g2.jsonl`. 11 pesan terkirim (10 pesan uji + "ya", message_id 1600–1641), semua dibalas. Pesan rencana-marketing-usaha diganti skenario normal warung bakso (`examples/01`, periode Nov–Jan), karena pesan jebakan dari prep G18 membuat pra-cek lebih dari 10 menit. SKILL.md dan script di home bot identik dengan repo (diff penilai, tanpa folder `examples/`): rencana-marketing-usaha 1.0.6, notulen-rapat 1.0.4, ekstrak-nota-faktur 1.0.4, arsip-nota 1.0.7, iterasi-dari-masukan-pelanggan 1.0.11. Pra-cek `uji-tg.sh`: notulen, ekstrak, arsip selesai pada putaran pertama; rencana-marketing (pesan jebakan) dan iterasi kena batas 600 detik, lalu putaran ulang selesai (rencana-marketing bakso 263 detik, iterasi 547 detik). Penilai: agent penilai independen (bukan pembuat), memakai bagian "Penilaian" di `alat-uji/brief/tester-umum.md`; satu salah angka/fakta = sisi itu maks. 5. Tanggal dicek dengan python: 1 Okt 2026 Kamis, 2 Okt Jumat, 5 Okt Senin, 7 Okt Rabu, 8 Okt Kamis, 9 Okt Jumat.

## Skor & verdik

| Skill (versi) | TANPA | DENGAN | Selisih | Verdik | Pembeda (satu kalimat) |
|---|---|---|---|---|---|
| notulen-rapat (1.0.4) | 5 | 8,5 | +3,5 | **LOLOS** | Hanya DENGAN yang membaca "2,1M" sebagai Rp2.100.000.000 (TANPA menulis Rp2,1 juta), mengubah semua tanggal relatif ke tanggal pasti (besok = Jumat 2 Okt, sebelum Rabu 7 Okt, rapat berikutnya Kamis 8 Okt), menandai "Jumat depan" ambigu (2 atau 9 Okt), dan menambah pesan siap kirim ke grup WA. |
| rencana-marketing-usaha (1.0.6) | 6,5 | 8 | +1,5 | **LOLOS** (tepat di ambang) | DENGAN memberi target terukur (+10 porsi malam/hari), anggaran per kanal yang jumlahnya pas Rp9.000.000, batas biaya iklan per pelanggan (Rp10.000 makan di tempat, Rp6.000 GoFood) dengan aturan berhenti, dan menyimpulkan GoFood jangan jadi andalan iklan. TANPA justru menaruh pos terbesar (Rp1.000.000/bulan) di promo GoFood yang marginnya paling tipis, tanpa target angka. |
| ekstrak-nota-faktur (1.0.4) | 4,5 | 7,5 | +3,0 | **BELUM** (DENGAN < 8) | Hanya DENGAN yang menangkap PPN invoice dihitung 12% penuh (untuk jasa biasa seharusnya Rp165.000, kelebihan tagih Rp15.000) dan menyarankan bertanya ke penjual. TANPA menyatakan invoice "sudah cocok semua" dan berkas Excel-nya berisi rumus salah, tetapi DENGAN tidak melampirkan berkas Excel yang diminta. |
| arsip-nota (1.0.7) | 7 | 8 | +1,0 | **BELUM** (perbandingan tidak bersih) | DENGAN menyalin 3 nota ke arsip setelah konfirmasi dan membiarkan file asli utuh, sedangkan TANPA langsung mengganti nama file asli. Nota dobel terdeteksi lewat isi file di kedua sisi, dan rekapnya sama (Rp1.887.500). |
| iterasi-dari-masukan-pelanggan (1.0.11) | 6 | 5 | −1,0 | **BELUM** (salah angka) | DENGAN memberi backlog berpenanggung jawab dan bertenggat, draf balasan, dan temuan keluhan WA yang tidak dibalas tanpa menyebut nama pelanggan. Namun satu keluhan WA ("Kurir telat lagi, nunggu lama. Tolong dibenahi") terlewat, sehingga beberapa angkanya salah. TANPA menghitung keluhan per isu dengan benar, tetapi tanpa rencana kerja. |

Pembanding uji internal (skor promosi / `examples/`):
- Notulen, pesan sama: 6 → 9 (1.0.4).
- Rencana marketing, skenario warung bakso (periode Okt–Des): 6,0 → 9,0 (1.0.4).
- Ekstrak nota, pesan sama: 6,0 → 9,0 (skenario 1 di `00-openclaw-sebelum-sesudah.md`: 5,5 → 9).
- Arsip nota: rata-rata dua skenario 5,75 → 8,75; skenario yang sama dengan pesan ini 7 → 9.
- Iterasi masukan: 5,9 → 8,5 (1.0.11), **dengan data lain** (31 masukan, kasus jamur). Data gelombang ini terdiri dari 18 baris chat dan 26 ulasan.

Beda terhadap uji internal:
- **Notulen:** TANPA turun dari 6 ke 5 hanya karena aturan "salah angka = maks. 5" diterapkan. Sisi TANPA lokal juga menulis Rp2,1 juta.
- **Rencana marketing:** TANPA di bot sedikit lebih baik. DENGAN kehilangan poin karena kata proses, label "target laba", dan istilah yang tidak dijelaskan.
- **Ekstrak nota:** hitungan DENGAN tetap sempurna. Skornya turun karena di kanal Telegram berkas yang diminta tidak terlampir, sedangkan di uji lokal berkas di folder kerja memang bisa dibuka.
- **Arsip nota:** DENGAN butuh satu giliran tambahan karena workspace dipakai bersama (lihat catatan jujur).
- **Iterasi:** data uji baru memuat baris "Pesan ini dihapus" yang membuka cacat script.

## Kutipan balasan (dipendekkan, `…` = dipotong)

### notulen-rapat

TANPA (topik 1592, 796 karakter, 1 pesan, msg 1601):
> Notulen Rapat Mingguan 📅 1 Oktober, pukul 09.00 …
> 1. Sales • Realisasi Sept: Rp2,1 juta dari target Rp2,5 juta • Penyebab: 2 customer besar mundur ke Oktober • Keputusan: target Okt tetap Rp2,5 juta • Aksi: Tono kirim daftar prospek, deadline Jumat depan
> 2. Gudang • 2 unit forklift rusak, teknisi datang Senin …
> • Aksi: Bu Sari buat daftar piutang & draft tagihan, selesai sebelum Rabu … Rapat berikutnya: Kamis depan, jam sama

DENGAN (topik 1593, 2.854 karakter, 1 pesan setelah pesan "Working", msg 1604):
> • Hari, tanggal: Kamis, 1 Oktober 2026 … • Tempat/platform: [isi] • Pemimpin rapat: [isi] • Notulis: [isi]
> • Sales September tercapai Rp 2.100.000.000 dari target Rp 2.500.000.000. …
> • Forklift 2 rusak; teknisi datang Senin, 5 Oktober 2026.
> Keputusan 1. Target penjualan Oktober tetap Rp 2.500.000.000. 2. Sewa forklift sementara disetujui Pak Budi: 3 hari, Rp 450.000/hari.
> Action Items (urut tenggat terdekat) 1. Rina — Order 60 palet, maks Rp 85.000/pcs — Jumat, 2 Oktober 2026 ("besok") — Belum mulai 2. Bu Sari — … — Sebelum Rabu, 7 Oktober 2026 ("sebelum rabu") 3. Tono — Kirim daftar prospek pengganti 2 customer yang mundur — ⚠️ "Jumat depan": Jumat, 2 Oktober 2026 atau Jumat, 9 Oktober 2026 (ambigu, mohon dipastikan)
> Rapat berikutnya: Kamis, 8 Oktober 2026, jam yang sama (09.00 WIB).
> Pesan untuk grup WhatsApp … • @Tono: kirim daftar prospek, tenggat Jumat depan ⚠️ (2 atau 9 Okt, mohon dipastikan) ❓ Kenaikan gaji driver dibahas lagi rapat berikutnya

### rencana-marketing-usaha

TANPA (topik 1590, 3.493 karakter, 1 pesan, msg 1632):
> • Dine-in: harga 20rb − bahan 9rb − bungkus 1rb = untung kotor 10rb/porsi (50%) • Via GoFood: … warung terima 16rb, dikurangi bahan+bungkus 10rb = untung kotor 6rb/porsi (30%)
> Budget 3jt/bulan, dibagi 6 pos: • Promo GoFood (diskon ongkir/voucher via aplikasi GoBiz…): 1.000.000 • Promo "Jam Sepi" dine-in (diskon 18.00–21.00): 800.000 • Cetak materi …: 400.000 (bulan 1), turun ke ±100rb bulan 2-3 …
> Bulan 2 (Desember) — … Paket "Nonton Bareng/Keluarga Malam" …
> Cara pantau gampang … Catat di buku/notes HP: jumlah porsi siang, jumlah porsi malam, jumlah dari GoFood

DENGAN (topik 1591, 6.065 karakter, 3 pesan: 3.881 + 101 + 2.083, setelah pesan "Working", msg 1635–1637):
> @KTpenguji_bot Oke, ini rencana marketing 3 bulan … Beberapa asumsi saya pakai karena belum disebutkan — tolong dikoreksi kalau meleset.
> • Tujuan: tambah ±10 porsi malam (17.00-21.00)/hari, total ±900 porsi tambahan selama 3 bulan, per 31 Jan 2027 … • Margin GoFood: Rp6.000 (30%) — AMAN tapi lebih tipis, GoFood jangan jadi andalan iklan
> 7. Anggaran (dihitung script, bukan kira-kira) Total Rp9.000.000 untuk 3 bulan: • Iklan Meta/IG radius 3km: Rp3.240.000 (36%), ~Rp1.080.000/bulan … • Cadangan eksperimen (10%): Rp900.000 Cek jumlah = anggaran: OK.
> • CAC titik impas: Rp10.000 | ROAS titik impas: 2,00 • CAC target: Rp8.000 | ROAS target: 2,50 … GoFood: • CAC titik impas: Rp6.000 | ROAS titik impas: 3,34
> … minimal harus menghasilkan 405 pelanggan baru (bukan perkiraan, ini syarat balik modal sesuai target laba Rp8.000/pelanggan) = minimal omzet dari iklan Rp8.100.000 … • Jangkauan 386.000 → Klik 5.790 (1,5%) → Chat/kunjungan 1.158 (20%) → Pesanan 405 (35%)
> … hentikan iklan kalau CAC > Rp10.000 selama 4 minggu berturut … Catatan: ini alat bantu perencanaan, target adalah tujuan bukan jaminan hasil …

### ekstrak-nota-faktur

TANPA (topik 1594, 292 karakter dalam 2 pesan: keterangan berkas 172 + teks 120, ditambah berkas `Rekap_Nota_Toko_Kue_Sep2026.xlsx`, setelah pesan "Working", msg 1607–1608):
> [berkas Rekap_Nota_Toko_Kue_Sep2026.xlsx] Rekap nota belanja toko kue — Sep 2026 ⚠️ Nota 1 (Toko Bahan Kue Sari) ada selisih Rp10.000 — cek lagi fisik notanya ya ✅ Nota 2 & Invoice CV Cetak Kilat sudah cocok semua
> Sudah terkirim, Kak — file Excel rekapnya nongol di grup ya. Ada yang mau ditambahin atau dicek lagi dari nota-nota itu?
> (isi berkas, sheet "Faktur Pajak (CV Cetak Kilat)") PPN hasil hitung ulang (= DPP x 12%) … STATUS PEMERIKSAAN: ✓ SEMUA HITUNGAN COCOK (PPN & Total sesuai dengan invoice)

DENGAN (topik 1595, 2.786 karakter, 1 pesan setelah pesan "Working", msg 1611):
> | N1 | 03-09-2026 | Toko Bahan Kue Sari | Nota | Rp 334.000 | ⚠️ Ada selisih | … | I1 | 08-09-2026 | CV Cetak Kilat | Invoice | Rp 1.680.000 | ⚠️ Perlu dicek |
> • I1 (CV Cetak Kilat): PPN ditulis Rp 180.000 = 12% dari DPP penuh … aturan sejak 2025 seharusnya 12% × 11/12 × DPP = Rp 165.000 (efektif 11%). Kalau pakai PPN yang benar, totalnya jadi Rp 1.665.000, beda Rp 15.000 … tanyakan ke CV Cetak Kilat sebelum bayar, jangan asumsi itu penipuan.
> • Total: Rp 2.051.500 • PPN tercantum: Rp 180.000 • Per kategori: Bahan baku Rp 334.000 · Bahan kemasan Rp 1.717.500
> CSV (siap tempel ke Excel, pemisah ;) No;ID;Tanggal;…;Subtotal Dihitung Script;DPP Dihitung Script;PPN Seharusnya;… (28 kolom)
> Sudah saya simpan juga jadi file rekap-nota-kue.csv di folder kerja — tinggal buka langsung di Excel.
> Dasar PPN: UU HPP & PMK 131/2024, per 23 September 2026. Ini alat bantu hitung, bukan nasihat pajak resmi — … Kring Pajak 1500200 …

### arsip-nota

TANPA (topik 1596, 787 karakter, 1 pesan setelah pesan "Working", msg 1614):
> Selesai dirapiin! 📁 File yang direname (format: Tanggal_Penjual_Keterangan_Nominal): • 2026-09-20_Toko-Bangunan-Sinar-Jaya_Semen_Rp1.250.000.jpg • 2026-09-22_SPBU-Pertamina_Bensin_Rp150.000.jpg • 2026-09-25_PLN_Tagihan-Listrik_Rp487.500.pdf
> File IMG_20260920_101 (1).jpg saya cek hash-nya — memang identik 100% sama nota Sinar Jaya yang pertama, jadi saya pindah ke nota/duplikat/ biar nggak dobel kehitung.
> | Material/Bangunan | Rp 1.250.000 | … | TOTAL | Rp 1.887.500 |
> Rekap lengkap + rincian per nota saya simpan di rekap-pengeluaran-sept2026-nota.csv di root workspace.

DENGAN (topik 1597, 2.752 karakter dalam 2 giliran: 1.599 + 1.153, masing-masing setelah pesan "Working", msg 1617 dan 1630):
> [giliran 1] File yang disebutkan nggak ada — IMG_20260920_101.jpg, … tidak ketemu di nota/. Yang justru ada di sana (sudah dalam format nama baku, seperti hasil arsip): … • folder duplikat/ berisi 2026-09-20_Toko-Bangunan-Sinar-Jaya_Semen_DUPLIKAT.jpg
> Saya cek isi filenya (hash SHA-256): file di folder duplikat/ itu identik persis …
> Sebelum saya jalankan tambah ke indeks, tolong konfirmasi dulu (saya sudah siapkan indeksnya di ~/KomunitechData/arsip-nota/): 1. … 2. … 3. File asli IMG_*/faktur_listrik_sept.pdf-nya ada di mana? …
> [giliran 2, setelah "ya"] Arsip tersimpan (3 nota, file asli tetap ada di nota/, disalin ke arsip): 1. 2026-09-20_Toko-Bangunan-Sinar-Jaya_1250000.jpg — … Rp 1.250.000, kategori Bahan baku (tebakan dari nama vendor) …
> … saya tidak memasukkannya ke indeks lagi supaya pengeluaran tidak terhitung dobel. REKAP PENGELUARAN SEPTEMBER 2026 Jumlah nota: 3 | Total: Rp 1.887.500 …
> Semua angka di atas langsung dari hasil script arsip, bukan dihitung manual. Mau sekalian diekspor ke CSV buat kas-umkm?

### iterasi-dari-masukan-pelanggan

TANPA (topik 1598, 1.580 karakter, 1 pesan setelah pesan "Working", msg 1640):
> Udah saya baca semua — 18 chat WA + 26 ulasan Shopee bulan September. …
> 1. Higiene dapur & packing — paling urgent walau kejadiannya cuma 3x Ada rambut di topping (WA - Sari, Shopee - Pembeli 7) dan ulat di sayur (Shopee - Pembeli 24). Semua jadi bintang 1 …
> 2. Kurir/pengiriman telat — paling sering muncul 5 dari 11 ulasan bintang rendah di Shopee soal telat (sampe 90 menit–2 jam), ditambah 2 keluhan serupa di WA dari Budi. …
> Sisi baiknya: … Dewi Lestari minta varian tanpa telur — ini bisa jadi ide produk baru. Saran urutan eksekusi: benerin higiene dulu …

DENGAN (topik 1599, 6.620 karakter, 3 pesan: 3.895 + 27 + 2.698, setelah pesan "Working", msg 1673–1675):
> Sudah saya baca semua datanya: 12 pesan pelanggan di chat WA September (3 pesan dari "Admin Kue Nara" saya kecualikan sebagai tim) + 26 ulasan Shopee September — total 38 masukan. Saya olah pakai script tema/sentimen, lalu saya cek ulang satu-satu kutipannya …
> • Pengiriman telat = isu #1: 7 dari 38 masukan (18,4%) … • 4 dari 6 keluhan via WA (66,7%) belum pernah dibalas Admin …
> • Respons staf (WA) — yang TIDAK pernah dibalas: "Kemarin krimnya kurang…", "Kotak kuenya bocor…", "Ada rambut di toppingnya…", "Harga naik ya?…"
> 1. [Segera] Keamanan pangan — bukti: 3 laporan (2 rambut, 1 ulat) — tindakan: wajib hairnet + cek visual akhir sebelum packing — PJ: Pemilik — tenggat 23 Okt — ukuran berhasil: 0 laporan benda asing bulan depan
> Draf balasan siap kirim (manusia yang kirim, isi {panggilan} sesuai pelanggannya) • Keluhan WA pengiriman yang belum dibalas: "Halo Kak {panggilan}, mohon maaf atas keterlambatan pengiriman kemarin. …"

## Verifikasi angka

**notulen-rapat.** Hasil `tanggal_relatif.py --rapat 2026-10-01` cocok dengan cek kalender python:
- besok = Jumat 2 Okt;
- Senin = 5 Okt;
- sebelum Rabu = sebelum 7 Okt (bila diartikan ketat, paling lambat Selasa 6 Okt);
- Kamis depan = 8 Okt;
- Jumat depan = 9 Okt, ambigu dengan alternatif 2 Okt.

Semua tanggal dan nama hari di DENGAN benar, dan pesan WA DENGAN berisi 97 kata (≤ 120). TANPA tidak mengubah satu pun tanggal relatif. Satuan "2,1M"/"2,5M" berarti miliar. Konteksnya jelas: sewa forklift Rp450.000/hari dan 60 palet × Rp85.000 = Rp5.100.000, jadi omzet Rp2,1 juta sebulan mustahil. **TANPA salah angka** (Rp2,1 juta / Rp2,5 juta); DENGAN benar (Rp2.100.000.000 / Rp2.500.000.000).

**rencana-marketing-usaha.** `alokasi_anggaran.py` dijalankan dengan data pesan (`target --harga-jual 20000 --hpp 9000 --biaya-per-pesanan 1000 --laba-target-per-pesanan 2000 --anggaran-iklan 3240000`; GoFood `--biaya-platform 20 --laba-target-per-pesanan 1000`; `alokasi --anggaran 9000000 --bulan 3 --kanal "…=40,…=25,…=20,…=15"`; `funnel 405` dengan 1,5/20/35%). Keluarannya sama persis dengan DENGAN. Angka kunci juga dihitung ulang sendiri:

| Angka | Hitung ulang | DENGAN | TANPA |
|---|---|---|---|
| Margin makan di tempat | 20.000 − 9.000 − 1.000 = 10.000 (50%) | sama | sama |
| Margin GoFood | 20.000 × 0,8 − 10.000 = 6.000 (30%) | sama | sama |
| CAC / ROAS impas, makan di tempat | 10.000 / 20.000 ÷ 10.000 = 2,00 | sama | — |
| CAC / ROAS target (laba 2.000) | 8.000 / 2,50 | sama | — |
| CAC / ROAS GoFood impas & target | 6.000 / 3,333 → dibulatkan ke atas 3,34; 5.000 / 4,00 | sama | — |
| Alokasi 9 jt | cadangan 900.000; 8.100.000 × 40/25/20/15% = 3.240.000 / 2.025.000 / 1.620.000 / 1.215.000; per bulan 1.080.000 / 675.000 / 540.000 / 405.000 | sama | 6 pos = 3.000.000/bulan ✓ |
| Pelanggan & omzet dari iklan | 3.240.000 ÷ 8.000 = 405; 405 × 20.000 = 8.100.000 | sama | — |
| Corong | 405 ÷ 35% = 1.157,1 → 1.158; ÷ 20% = 5.790; ÷ 1,5% = 386.000 | sama | — |
| Target porsi malam | 10/hari × 92 hari (Nov–Jan) = 920 ≈ "±900" | sama | — |

Klaim TANPA juga benar:
- diskon malam 20% → 16.000 − 10.000 = 6.000, masih untung;
- diskon 10% lewat GoFood → 18.000 × 0,8 − 10.000 = 4.400, masih untung.

**Tidak ada salah hitung di kedua sisi.** Ada satu label keliru di DENGAN: "syarat balik modal sesuai target laba Rp8.000/pelanggan".
- Rp8.000 adalah batas biaya iklan per pelanggan; laba targetnya Rp2.000.
- 405 pelanggan adalah syarat mencapai target laba. Titik impas iklan sebenarnya 3.240.000 ÷ 10.000 = **324 pelanggan**.
- Kalimat ini berasal dari label script "Minimal pesanan agar balik modal iklan", yang memakai CAC target, dan muncul juga di contoh uji internal (`examples/01-uji-warung-bakso.md`).

**ekstrak-nota-faktur.** `cek_nota.py` dijalankan dengan data pesan. Hasilnya (status, selisih, PPN seharusnya, rekap, CSV) **sama persis** dengan DENGAN. Hitung ulang sendiri:

| Dokumen | Hitung ulang | DENGAN | TANPA (chat + berkas) |
|---|---|---|---|
| N1 Toko Bahan Kue Sari | 135.000 + 85.000 + 124.000 = 344.000 ≠ 334.000 → selisih 10.000 | sama | sama |
| N2 Minimarket Berkah | 3 × 12.500 = 37.500 = total | cocok | chat: cocok. Berkas: sel Selisih = `I11 − I12` merujuk baris kosong → **−37.500** di samping "✓ COCOK" |
| I1 CV Cetak Kilat | PMK 131/2024, jasa biasa: DPP nilai lain 11/12 × 1.500.000 = 1.375.000; PPN 12% = **165.000**; total 1.665.000; lebih tagih 15.000. Terbilang = 1.680.000 ✓; NPWP 16 digit | sama | "sudah cocok semua"; berkas: PPN = DPP × 12%, "✓ SEMUA HITUNGAN COCOK" |
| Rekap | 334.000 + 37.500 + 1.680.000 = 2.051.500; kemasan 37.500 + 1.680.000 = 1.717.500 | sama | chat: tidak ada. Berkas: total tertulis 2.051.500 ✓, tetapi "Total Hasil Cek" = 344.000 + **0** + 1.680.000 = **2.024.000** (seharusnya 2.061.500) |

Total invoice = DPP + PPN (1.500.000 + 180.000). Artinya angka 1.500.000 adalah harga jual, sehingga tafsir DENGAN konsisten dengan aturan. Rumus dalam berkas TANPA tidak punya nilai tersimpan; nilainya dihitung penilai seperti Excel menghitungnya. **TANPA: dua salah angka/fakta. DENGAN: tidak ada.**

**arsip-nota.** 1.250.000 + 150.000 + 487.500 = **1.887.500**, benar di kedua sisi. Workspace bot diperiksa baca-saja:
- sidik SHA-256 file Sinar Jaya, file dobel, dan file asli data uji sama;
- `nota/` berisi 3 file bernama baru hasil TANPA, ditambah `duplikat/…_DUPLIKAT.jpg`;
- arsip DENGAN memuat 3 salinan di `arsip/2026/09/`, dan file di `nota/` tetap ada.

Klaim "file asli tetap ada, disalin ke arsip" benar. **Tidak ada salah angka.**

**iterasi-dari-masukan-pelanggan.** Data di workspace bot identik dengan salinan di scratchpad. Isinya: 18 baris chat (17 pesan bertanggal, yaitu 14 dari pelanggan dan 3 dari Admin Kue Nara, ditambah 1 baris tanpa tanggal "Pesan ini dihapus"; satu pesan pelanggan berupa media) dan 26 ulasan (bintang 1: 6, 2: 5, 3: 2, 4: 4, 5: 9).

| Klaim | Dihitung penilai dari data | DENGAN | TANPA |
|---|---|---|---|
| Pesan WA pelanggan | 13 pesan teks (14 − 1 media) | **12** ✗ | "18 chat WA" (= jumlah baris) |
| Total masukan | 13 + 26 = 39 | **38** ✗ | — |
| Keluhan pengiriman | Shopee 5 (bintang 1–2) + 1 (bintang 4 "telat sedikit") + WA 2 (2/9 dan 22/9) = 8 (20,5%) | **7 (18,4%)** ✗ | "5 dari 11 ulasan bintang rendah + 2 di WA" ✓ |
| Sentimen WA | positif 4, netral 2, negatif 7 | negatif **6** ✗ | — |
| Keluhan WA tak dibalas | 7 keluhan; Admin membalas 2/9 (telat) dan 18/9 (kurang kotak) → 5 dari 7 (71,4%); pesan tanpa balasan 10 dari 13 (76,9%) | **4 dari 6 (66,7%); 9 dari 12 (75%)** ✗; daftar melewatkan 22/9 "Kurir telat lagi…" | tidak dibahas |
| Keamanan pangan | rambut 2 (WA 11/9, Shopee), ulat 1 = 3 | 3 ✓ | 3 ✓ |
| Kemasan / porsi / harga / ketepatan / rasa | 3 / 3 / 3 / 2 / 2 (sesudah koreksi tema yang dijelaskan bot) | sama ✓ | sesuai (kemasan "2 Shopee + 1 WA") |
| Data pribadi | HP 0812-… dan alamat Jl. Melati … | tidak disalin, tanpa nama ✓ | tidak disalin; 4 nama pelanggan disebut |

Penyebabnya ada di script `olah_masukan.py`:
1. Baris tanpa tanggal "Pesan ini dihapus" diperlakukan sebagai lanjutan pesan Budi 22/9.
2. Pola pesan sistem `pesan ini dihapus` lalu membuang **seluruh** pesan itu, tercatat sebagai "pesan sistem/media 2".

Penilai menjalankan script dengan data yang sama dan `koreksi.csv` milik bot. Hasilnya persis angka bot: 38; 12; 4 dari 6; 9 dari 12; pengiriman 7. Setelah baris itu dihapus, hasilnya 39; 13; 5 dari 7 (71,4%); 10 dari 13 (76,9%); pengiriman 8 (20,5%), dan keluhan 22/9 muncul di daftar "belum dibalas". Daftar `--daftar-pengirim` pun menunjukkan Budi 4 pesan, sedangkan rekap WA hanya memuat 3 pesan Budi. **DENGAN: salah angka (maks. 5).** Urutan prioritasnya tidak berubah: pengiriman tetap nomor 1 dan keamanan pangan tetap segera.

## Alasan skor & cacat

- **notulen-rapat**
  - **TANPA (5):** ringkas, peserta lengkap, persetujuan sewa forklift dan hal yang belum diputus tercatat. Kekurangannya:
    - "2,1M" dibaca juta (salah angka, maks. 5);
    - "forklift 2 rusak" menjadi "2 unit forklift" tanpa tanda ragu;
    - tidak ada tanggal relatif yang diubah, dan tanggal rapat ditulis tanpa tahun/hari;
    - tidak ada bagian keputusan terpisah, daftar konfirmasi, maupun pesan WA.
  - **DENGAN (8,5):**
    - Plus:
      - tanggal pasti dan benar, dengan "Jumat depan" ditandai ambigu di notulen dan pesan WA;
      - miliar benar;
      - keputusan dipisah dari tugas, tanpa tugas karangan untuk Hendra;
      - "Forklift 2" disalin apa adanya, dan isian `[isi]` dipakai untuk data yang tidak ada;
      - tugas diurutkan menurut tenggat dan diberi status, ditambah pesan WA 97 kata;
      - tanpa kata proses, satu pesan.
    - Minus:
      1. Tugas Tono ditambah "pengganti 2 customer yang mundur", yang tidak ada di catatan.
      2. Meminta konfirmasi "jam 9 pagi" padahal pengguna menulis "tadi pagi".
      3. Ada 5 butir "perlu dikonfirmasi" ditambah 1 tawaran.
- **rencana-marketing-usaha**
  - **TANPA (6,5):**
    - Plus: margin dua jalur benar, anggaran per bulan pas, wawasan biaya tambahan jualan malam benar, rencana per bulan praktis, cara pantau 2 menit/hari.
    - Minus:
      - tanpa target terukur, batas biaya iklan, maupun aturan berhenti;
      - pos terbesar ada di promo GoFood, kanal dengan margin paling tipis;
      - sisa dana cetak bulan 2–3 tidak dialokasikan ulang;
      - tanpa catatan bahwa ini bukan jaminan hasil.
  - **DENGAN (8):**
    - Plus: semua angka cocok dengan script dan hitung ulang; 12 bagian lengkap; asumsi dan "DATA BELUM ADA" ditulis terbuka; tujuan bertanda usulan; kalender "dicek per 16 Okt 2026"; aturan hentikan iklan; rencana B; 3 langkah minggu ini; catatan bukan jaminan hasil.
    - Minus:
      1. Label keliru "target laba Rp8.000/pelanggan … syarat balik modal". Lihat verifikasi: titik impasnya 324 pelanggan.
      2. Kata proses "dihitung script" muncul dua kali, ditambah "bisa pakai skill promo-kalender".
      3. Ringkasan menulis "Rp9.000.000 + cadangan Rp900.000", padahal cadangan sudah termasuk di 9 juta.
      4. CAC/ROAS/corong tanpa penjelasan awam.
      5. Dipecah 3 pesan, salah satunya hanya 101 karakter (dua baris angka), dan diawali "@KTpenguji_bot".
- **ekstrak-nota-faktur**
  - **TANPA (4,5):**
    - Plus: berkas .xlsx sungguhan (3 sheet) terkirim di chat, dan selisih Nota 1 benar.
    - Minus:
      - PPN 12% penuh atas jasa biasa dinyatakan cocok (salah fakta);
      - berkas berisi rumus yang salah rujuk (Nota 2 −37.500 bertanda cocok; total hasil cek 2.024.000);
      - di chat tidak ada rekap, dasar aturan, maupun disclaimer.
  - **DENGAN (7,5):**
    - Plus: hitungan dan cek PPN sempurna, peringatan disampaikan "bukan tuduhan", rekap per kategori dan per penjual, dasar aturan + Kring Pajak.
    - Minus untuk kanal Telegram:
      1. Pengguna minta "ke Excel", tetapi tidak ada berkas terlampir. Bot malah menulis "sudah saya simpan … di folder kerja — tinggal buka langsung di Excel", padahal pengguna tidak bisa membuka folder itu. Ini bertentangan dengan keputusan pemilik no. 14/15: lampirkan berkas, atau jangan sebut jalurnya dan tawarkan "balas 'kirim file'".
      2. CSV 28 kolom (sebagian besar kosong) ditempel di chat, judul kolomnya memuat kata "Script", dan pemisah ";" tidak terbagi otomatis bila ditempel langsung.
      3. Tabel markdown tampil sebagai teks mentah.
- **arsip-nota**
  - **TANPA (7):**
    - Plus: satu giliran, nama baku, nota dobel dicek lewat isi file lalu dipindah (tidak dihapus), rekap dan kategori tepat.
    - Minus:
      - nama file asli diganti di tempat tanpa pratinjau;
      - file dobel ikut diganti nama tanpa disebut;
      - istilah "hash" dan "root workspace";
      - CSV disimpan di tempat yang tidak bisa dibuka dari Telegram;
      - tanpa indeks untuk dicari ulang.
  - **DENGAN (8):**
    - Plus: tidak menebak saat nama file tidak cocok; mencocokkan isi file dobel; 3 pertanyaan bernomor; setelah "ya" menyalin (bukan memindah) ke arsip; nota dobel tidak masuk indeks; rekap benar; kategori ditandai tebakan.
    - Minus:
      1. Jalur dan kata proses muncul di chat: "~/KomunitechData/arsip-nota/", "tambah ke indeks", "hasil script arsip", dan nama skill lain "kas-umkm".
      2. Istilah teknis "hash SHA-256" dan "byte-for-byte".
      3. Semen dikategorikan "Bahan baku".
      4. Giliran 1 makan waktu ±5,5 menit.
- **iterasi-dari-masukan-pelanggan**
  - **TANPA (6):**
    - Plus: hitungan per isu benar, urutan prioritas masuk akal, ide varian tanpa telur dicatat, HP dan alamat tidak disalin.
    - Minus:
      - 4 nama pelanggan disebut;
      - "Semua jadi bintang 1", padahal laporan WA tidak berbintang;
      - "18 chat WA" adalah jumlah baris, termasuk 3 pesan admin;
      - tidak melihat bahwa 5 dari 7 keluhan WA tidak dibalas;
      - tanpa penanggung jawab, tenggat, ukuran berhasil, maupun draf balasan.
  - **DENGAN (5):** kerangka dan isi kualitatif setara ±8,5. Cakupannya: admin dikecualikan, tanpa data pribadi, tema dengan kutipan, koreksi tema dijelaskan, temuan keluhan tak dibalas, sinyal dini bintang 4, backlog maks. 3 dengan penanggung jawab/tenggat/ukuran, draf balasan, dan rencana bulan depan. Skornya dibatasi 5 karena:
    1. Satu keluhan WA hilang, sehingga 5 angka salah (12, 38, 6 negatif, 4 dari 6 / 9 dari 12, pengiriman 7 / 18,4%), padahal balasan menulis "sudah saya baca semua … cek ulang satu-satu".
    2. Draf "Keluhan WA pengiriman yang belum dibalas" tidak cocok dengan daftar tak dibalas yang ditulis bot sendiri.
    3. Kata proses muncul: "script tema/sentimen", "berkas koreksi", "keluaran script".
    4. Panjang 6.620 karakter dalam 3 pesan, salah satunya 27 karakter.
    5. Waktu balas ±13 menit.

## Perilaku bot asli vs uji lokal

- **Pemicu:** kelima skill terpicu di sisi DENGAN; format dan angkanya sama dengan keluaran script masing-masing. Sisi TANPA tidak menunjukkan jejak skill (topik `skills: []`).
- **Kata proses:** muncul di 4 dari 5 jawaban DENGAN (rencana marketing, ekstrak nota, arsip nota, iterasi), berupa "script", "skill", jalur folder, "indeks", atau nama skill lain. Hanya notulen yang bersih.
- **Panjang dan pemecahan:**
  - notulen 2.854 karakter dan ekstrak 2.786 karakter, masing-masing satu pesan;
  - rencana marketing 6.065 dan iterasi 6.620 karakter dipecah 3 pesan, dengan potongan 101 dan 27 karakter sebagai pesan tersendiri (pola yang sama dengan G17);
  - arsip 2 giliran.
- **File:** satu-satunya berkas terkirim adalah `.xlsx` di TANPA ekstrak nota. DENGAN ekstrak nota dan TANPA arsip menyebut berkas CSV di folder bot yang tidak bisa dibuka pengguna. DENGAN arsip menyebut jalur arsip. DENGAN iterasi hanya menawarkan CSV.
- **Pesan "Working":** ada sebelum balasan di 8 topik (9 pesan), termasuk tiga topik TANPA (ekstrak, arsip, iterasi). Tidak ada di topik 1590 dan 1592. Ini perilaku platform, bukan skill.
- **Waktu balas** (kirim → balasan terakhir):

  | Skill | TANPA | DENGAN |
  |---|---|---|
  | notulen | ±20 detik | ±1 menit 40 detik |
  | rencana marketing | ±67 detik | ±6 menit 15 detik |
  | ekstrak nota | ±5 menit 33 detik | ±1 menit 35 detik |
  | arsip nota | ±1 menit 50 detik | ±5 menit 35 detik + ±80 detik (2 giliran) |
  | iterasi | ±60 detik | **±13 menit 18 detik** |

- **Tanya di akhir:**
  - rencana marketing: TANPA menawarkan template, DENGAN memberi 3 keputusan terbuka;
  - notulen: TANPA tidak bertanya, DENGAN memberi 5 butir konfirmasi + 1 tawaran;
  - ekstrak: TANPA 1 pertanyaan, DENGAN tidak bertanya;
  - arsip: DENGAN memberi 3 pertanyaan sebelum menyalin (sesuai aturan pratinjau);
  - iterasi: DENGAN 1 tawaran CSV.

## Catatan jujur

- **arsip-nota, workspace bersama:** semua topik bot kedua memakai satu workspace.
  - Sisi TANPA (09:07–09:09 UTC) mengganti nama file asli di `nota/` lebih dulu. Akibatnya sisi DENGAN (mulai 09:09) bertemu nama yang tidak cocok, menjelaskan ketidakcocokan, lalu baru mengarsipkan setelah "ya".
  - Penanganan DENGAN atas keadaan itu aman dan tepat, dan nilainya diberikan atas gabungan kedua giliran.
  - Selisih +1,0 sebagian dipengaruhi urutan ini, jadi perbandingannya tidak bersih. Pada uji internal, skenario yang sama menghasilkan 7 → 9.
  - Kekurangan DENGAN yang tidak terkait urutan (jalur, kata proses, nama skill lain) tetap dikurangi.
- **ekstrak-nota, berkas Excel TANPA:**
  - Brief menyebut isi berkas tidak bisa dibuka dari getUpdates. Penilai menemukan salinan identik di folder `media/outbound` bot uji (8.422 byte, sama dengan `document.file_size`; sama juga dengan `workspace/output`) dan membukanya baca-saja.
  - Kalau berkas itu tidak dinilai, TANPA tetap maks. 5 karena kesimpulan "cocok semua" pada PPN.
  - Catatan konteks menyebut msg 1607 "tanpa teks", padahal ada keterangan berkas 172 karakter.
- **rencana-marketing, label "target laba Rp8.000":** tidak dihitung salah angka. Alasannya:
  - semua angkanya benar;
  - kelirunya ke arah hati-hati (405 > 324);
  - frasa yang sama ada di contoh uji internal yang diberi 9;
  - asalnya dari label script.

  Bila pemilik menganggapnya salah fakta, DENGAN menjadi maks. 5 dan verdik BELUM.
- **notulen, aturan maks. 5:** diterapkan konsisten di gelombang ini. Uji internal memberi 6 untuk kesalahan "Rp2,1 juta" yang sama.
- **iterasi:**
  - Data gelombang ini berbeda dari data uji internal, jadi skor 5,9 → 8,5 tidak bisa dibandingkan langsung.
  - Kesalahan berasal dari script, bukan dari agent yang mengarang. Namun SKILL.md mewajibkan agent membaca setiap masukan (≤ 150), dan balasan mengklaim sudah melakukannya.
  - Saat sesi DENGAN berjalan, data gelombang lain ikut disalin ke workspace yang sama (09:35 UTC). Tidak terlihat pengaruhnya pada hasil.
- **"18 chat WA" di TANPA iterasi:** tidak dihitung salah angka, karena cocok dengan jumlah baris berkas (acuan brief) dan tidak dipakai untuk kesimpulan apa pun. Uji internal sebelumnya menilai pola serupa ("16 chat WA") sebagai salah; di sini dicatat sebagai cacat kecil.

## Rekomendasi

1. **notulen-rapat: LOLOS (+3,5).** Masuk daftar tampil `promosi/`, dengan pembeda "2,1M → miliar, tanggal pasti, 'Jumat depan' ambigu ditandai, pesan WA". Usulan perbaikan kecil yang tidak menunda:
   - jangan meminta konfirmasi waktu yang sudah tersirat ("tadi pagi");
   - deskripsi tugas disalin tanpa tambahan tafsir ("pengganti 2 customer").
2. **rencana-marketing-usaha: LOLOS, tepat di ambang (+1,5).** Sebelum ditampilkan sebagai promosi:
   - ganti label script/SKILL "Minimal pesanan agar balik modal iklan" (bila ada laba target) menjadi "Minimal pelanggan agar sesuai target (biaya iklan maks. Rp8.000/pelanggan, laba Rp2.000)" dan tampilkan juga titik impas (324);
   - larang "script/skill/nama skill lain" di jawaban kanal chat;
   - tulis "Rp9.000.000, sudah termasuk cadangan Rp900.000".

   Bila dipromosikan, sebut jujur bahwa AI biasa pun menghitung margin dengan benar; pembedanya ada di target, batas biaya iklan per kanal, dan aturan berhenti.
3. **ekstrak-nota-faktur: BELUM (DENGAN 7,5, selisih +3,0).** Sesuai aturan 2026-10-03, skill ini tetap di bundle/`beta` (uji internal LULUS) dan tidak dipromosikan. Pembedanya kuat (PPN 11/12, kelebihan tagih Rp15.000), dan cacatnya terbatas pada cara penyerahan berkas di kanal chat. Bila kurator memutuskan satu revisi (mode keputusan otomatis), tiga perbaikan paling berdampak:
   1. di kanal chat, lampirkan berkas CSV/XLSX (bot terbukti bisa mengirim dokumen). Bila tidak bisa, jangan sebut folder kerja dan tawarkan "balas 'kirim file'";
   2. ganti judul kolom "… Dihitung Script" menjadi "… Hitung Ulang", dan di chat tampilkan CSV ringkas (kolom kosong disembunyikan) atau pemisah tab;
   3. hindari tabel markdown di Telegram.

   Sesudahnya cukup kirim ulang DENGAN saja (pesan sama).
4. **arsip-nota: BELUM (+1,0), perbandingan tidak bersih.** Jangan disimpulkan "tanpa beda" sebelum uji ulang dengan **workspace terpisah per topik**: salin `nota/` baru untuk tiap sisi, atau kirim DENGAN lebih dulu di folder lain. Perbaikan skill yang tetap relevan: di kanal chat jangan tampilkan jalur `~/KomunitechData/…`, kata "indeks/script", istilah "hash SHA-256", dan nama skill lain ("kas-umkm"). Sampai diuji ulang, skill tetap di bundle/`beta` dan tidak dipromosikan.
5. **iterasi-dari-masukan-pelanggan: BELUM (salah angka).** Ini cacat nyata di script dan bisa terjadi di ekspor WA asli. Perbaikan yang disarankan, sebagai 1.0.12:
   - baris tanpa tanggal yang **seluruhnya** berupa teks sistem ("Pesan ini dihapus", "This message was deleted") jangan digabung ke pesan sebelumnya; perlakukan sebagai baris sistem tersendiri. Pola sistem hanya dicocokkan bila **seluruh** isi pesan adalah teks sistem;
   - tambahkan tes regresi untuk kasus ini;
   - script mencetak peringatan bila jumlah pesan per pengirim di `--daftar-pengirim` tidak sama dengan jumlah masukan WA yang dihitung.

   Waktu balas 13 menit di bot juga perlu dicatat (pra-cek lokal 547 detik). Sesudah perbaikan, kirim ulang DENGAN saja dengan pesan dan data yang sama. Angka yang diharapkan: 39 masukan, 13 pesan WA, 5 dari 7 keluhan tak dibalas, pengiriman 8 (20,5%).
6. **Catatan alat uji:** untuk skill yang mengubah file (arsip-nota, dan skill lain yang menulis ke workspace), sisi TANPA dan DENGAN harus memakai salinan data terpisah. Ini perlu dicatat di `alat-uji/README.md` agar gelombang berikutnya tidak mengulang kerancuan ini.
