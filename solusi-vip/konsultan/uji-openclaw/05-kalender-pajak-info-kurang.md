# 05 — Kalender pajak Oktober — info kurang lengkap

Tanggal uji: 2026-10-01 (Asia/Jakarta). OpenClaw lokal (`openclaw agent --local`), model router Komunitech (`ninerouter/komunitech`, sama dengan bot). SEBELUM = home `kosong-konsultan` (tanpa skill). SESUDAH = home `sol-konsultan` (paket skill solusi konsultan terpasang). Pesan identik di kedua sisi.

## Pesan member (giliran 1)

```
kapan aja saya harus bayar sama lapor pajak bulan oktober ini? biar ga kena denda
```

## Pesan member (giliran 2)

```
saya freelancer konsultan, orang pribadi. pakai yang 0,5% itu, belum PKP, nggak punya karyawan. omzet setahun kira2 600 juta.
```

## SEBELUM (tanpa skill)

### Giliran 1 — tools: ['tool_search', 'memory_search', 'tool_call', 'read']; lampiran file ke chat: tidak; durasi 138 dtk

````markdown
Oke, ini kalender pajak buat masa pajak September 2026 yang jatuh tempo bulan Oktober 2026 ini (berlaku umum buat UMKM/Wajib Pajak OP/Badan). Saya belum tahu usaha kamu persisnya pakai skema PPh Final UMKM, PKP (kena PPN), atau punya karyawan — jadi saya kasih semua kemungkinan, nanti saring sesuai kondisi:

• **PPh Final UMKM (PP 23 – tarif 0,5%)**
 - Bayar paling lambat **15 Oktober 2026**
 - Kalau sudah bayar & dapat NTPN, otomatis dianggap sudah lapor. Tapi kalau NIHIL (gak ada omzet/pajak terutang bulan itu), tetap wajib lapor SPT Masa nihil lewat Coretax/DJP Online, biasanya deadline tanggal 20.

• **PPh 21 (kalau punya karyawan/bayar gaji)**
 - Bayar paling lambat tanggal 10 → karena 10 Okt 2026 jatuh di hari Sabtu, biasanya mundur ke hari kerja berikutnya (Senin, 12 Okt 2026)
 - Lapor SPT Masa paling lambat **20 Oktober 2026**

• **PPh 25 (angsuran bulanan, kalau ada)**
 - Bayar paling lambat **15 Oktober 2026**, otomatis dianggap lapor kalau sudah ada NTPN

• **PPN (kalau sudah PKP)**
 - Bayar & lapor SPT Masa PPN paling lambat akhir bulan berikutnya → 31 Okt 2026 jatuh Sabtu, jadi kemungkinan mundur ke awal November. Ini yang paling perlu dicek ulang di Coretax karena bisa kegeser lagi kalau ketemu tanggal merah.

**Soal denda kalau telat:**
- Telat bayar: kena bunga per bulan dari pokok pajak (tarifnya mengacu ke tarif bunga acuan DJP bulanan, bisa beda tiap bulan).
- Telat lapor SPT Masa: denda Rp100.000 (untuk PPh 21/25/Final), Rp500.000 khusus SPT Masa PPN.

Catatan jujur: saya lagi nggak bisa browsing web real-time buat verifikasi tanggal pasti kalau ada pergeseran karena libur nasional/cuti bersama Oktober-November 2026 — jadi untuk tanggal yang kena geser (10 Okt dan akhir Okt), sebaiknya double-check sekali lagi di aplikasi Coretax DJP sebelum H-1.

Biar bisa saya bikinin reminder otomatis tiap bulan, boleh kasih tahu: usaha kamu pakai PPh Final UMKM (PP23) aja, atau sudah PKP (bayar PPN), dan ada karyawan tetap/nggak?
````

### Giliran 2 — tools: []; lampiran file ke chat: tidak; durasi 36 dtk

````markdown
Oke, dengan profil itu (OP freelance, PP23 0,5%, belum PKP, tanpa karyawan), kewajiban bulanan kamu disederhanain jadi **cuma satu: PPh Final UMKM 0,5%**. Gak ada PPh 21 (karena gak ada karyawan), gak ada PPN (karena belum PKP), dan gak ada PPh 25 (pengguna PP23 dibebaskan dari angsuran PPh 25).

**Untuk Oktober 2026:**
- Yang jatuh tempo bulan ini adalah setoran atas omzet **September 2026**.
- Bayar paling lambat **15 Oktober 2026** (lewat Coretax/bank, nanti dapat NTPN).
- Kalau sudah bayar dan dapat NTPN → otomatis dianggap sudah lapor, gak perlu lapor SPT Masa terpisah.
- Kalau September kamu nihil (gak ada penghasilan usaha) → tetap wajib lapor SPT Masa nihil, biasanya deadline tanggal 20.

**Poin penting yang relevan banget buat kamu — ambang Rp500 juta/tahun:**
Untuk WP Orang Pribadi pengguna PP23, ada bagian peredaran bruto kumulatif setahun sampai **Rp500 juta yang dibebaskan (tidak kena pajak sama sekali)**. Baru di atas Rp500 juta itu kena tarif 0,5%.

Karena omzet kamu setahun ~Rp600 juta, ada kemungkinan kumulatif omzet kamu baru nembus Rp500 juta sekitar bulan-bulan ini (Sep/Okt/Nov), tergantung pola income kamu. Dari titik itu ke bawah, bulan-bulan sebelumnya gak perlu setor pajak sama sekali — pajak cuma dihitung dari bagian yang melebihi Rp500 juta kumulatif.

Biar saya bisa kasih angka pasti yang harus kamu setor bulan ini, boleh kasih tahu:
1. Kira-kira berapa total omzet kumulatif kamu dari Januari–September 2026?
2. Sejak kapan kamu mulai pakai skema PP23 0,5% ini (tahun berapa)? — ini karena tarif final cuma berlaku maks 7 tahun pajak buat OP, kalau sudah lewat, kamu wajib pindah ke tarif normal (Pasal 17) dan mulai bayar PPh 25.

Sambil nunggu itu, mau saya buatkan reminder otomatis tiap tanggal 12 (H-3 dari deadline 15) biar nggak kelewat tiap bulan?
````

**Jejak tool (sebelum):** memory_search, `web_search` + `web_fetch` pajak.go.id (giliran 1); giliran 2 tanpa tool.

## SESUDAH (dengan paket skill)

### Giliran 1 — tools: ['tool_search', 'read', 'memory_search', 'tool_call']; lampiran file ke chat: tidak; durasi 24 dtk

````markdown
Belum ada catatan profil pajak kamu di memori saya, jadi saya perlu tahu dulu biar kalender tenggatnya pas (bukan tebak-tebakan). Jawab singkat ya, boleh sekaligus:

1. Usahanya **orang pribadi** atau **badan** (PT/CV/koperasi)?
2. Pakai **PPh final 0,5%** (omzet, PP 55/2022) atau sudah **pembukuan/tarif umum**?
3. Sudah **PKP** (pungut PPN) atau belum?
4. Punya **karyawan** (potong PPh 21), atau sering bayar jasa/sewa yang kena potong **PPh 23/4(2)**?

Begitu saya tahu profilnya, saya langsung kasih tanggal pasti setor & lapor untuk Oktober 2026 ini — termasuk yang mana yang kalau telat kena denda.
````

### Giliran 2 — tools: ['exec']; lampiran file ke chat: tidak; durasi 34 dtk

````markdown
Oke, profilmu: **orang pribadi, freelancer konsultan, PPh Final 0,5% (PP 55/2022), belum PKP, tanpa karyawan**, omzet ~Rp600 juta/tahun.

**Jadwal pajak Oktober 2026 (periode ini):**

| Tanggal | Kegiatan | Keterangan |
|---|---|---|
| **Kamis, 15 Oktober 2026** | **SETOR** PPh Final UMKM 0,5% masa pajak **September 2026** | Tidak ada lapor SPT Masa terpisah — setoran yang tervalidasi otomatis dianggap sudah lapor |

Cuma **satu tenggat** bulan ini: setor PPh final 0,5% atas omzet September, paling lambat **15 Oktober 2026** (Kamis, tidak jatuh di akhir pekan/libur jadi tidak bergeser).

**Catatan penting buat kamu khusus omzet ~600 juta/tahun:**
- Orang pribadi **boleh tidak setor** PPh final selama **omzet kumulatif tahun berjalan masih ≤ Rp500 juta**. Begitu kumulatif tembus Rp500 juta, sisa omzet di atas itu baru kena 0,5% dan **wajib disetor**.
- Dengan omzet ~600 juta/tahun, kemungkinan besar kamu **sudah melewati ambang Rp500 juta** sebelum September — jadi omzet September kemungkinan **sudah kena setor**, bukan lagi bebas. Cek kumulatif omzetmu Januari–September dulu untuk pastikan.
- Saya nggak hitung besaran rupiahnya di sini (itu bukan cakupan skill jadwal ini) — kalau mau saya hitungkan berapa yang harus disetor dari omzet Septembermu, tinggal bilang.

**Biar nggak kena denda:**
- Setor lewat Coretax (kode billing KAP 411128/411125, KJS sesuai PPh final) 2–3 hari sebelum 15 Oktober — mepet ke tanggal batas sering antre/trouble sistem.
- Keterlambatan setor PPh final dikenai bunga sesuai tarif acuan DJP (bukan denda tetap) — makin lama makin nambah, jadi lebih aman setor lebih awal.

Mau sekalian saya hitungkan nominal setorannya, atau dibuatkan kalender setahun penuh (termasuk SPT Tahunan OP Maret 2027) biar nggak kelewat terus?
````

**Jejak tool (sesudah):** memory_search, baca `kalender-pajak/SKILL.md`, bertanya (giliran 1); giliran 2 jalankan `scripts/kalender_pajak.py --profil op-umkm --tahun 2026 --bulan-mulai 10 --jumlah-bulan 1`. **Skill terpakai.**

## Verifikasi independen

Dicek dengan script skill (dijalankan penguji) dan aturan: PMK 81/2024 — PPh final UMKM (PP 55/2022) setor paling lambat tanggal 15 bulan berikutnya; setoran tervalidasi dianggap lapor SPT Masa. 15 Okt 2026 = Kamis, bukan libur → tidak bergeser. Orang pribadi: omzet kumulatif ≤ Rp500 juta setahun tidak terutang (PP 55/2022). PPh 21 (bila ada karyawan): setor tgl 15, lapor tgl 20 (PMK 81/2024).

| Butir | SEBELUM | SESUDAH |
|---|---|---|
| Giliran 1 (profil belum diketahui) | Daftar semua kemungkinan; **PPh 21 "bayar paling lambat tgl 10" ✘** (sejak 2025 tgl 15); menyebut "PP 23" ✘ (sudah diganti PP 55/2022); denda telat lapor Rp100 rb/Rp500 rb ✔; PPN akhir bulan → geser ke awal Nov ✔ | Bertanya 4 hal sekaligus, tanpa tebakan ✔ |
| Tenggat Oktober (profil OP UMKM) | 15 Okt 2026 ✔ | Kamis, 15 Okt 2026 ✔ (dari script) |
| Setor = lapor | ✔ | ✔ |
| "Nihil tetap wajib lapor SPT Masa, tgl 20" | Diklaim — **tidak dapat diverifikasi/meragukan** untuk OP PP 55 | Tidak diklaim |
| Ambang Rp500 juta | ✔, perkiraan "tembus sekitar Sep/Okt/Nov" ✔ (600 jt/12 = 50 jt/bln → kumulatif Jan–Sep ≈ 450 jt) | ✔ aturan, **tetapi menyimpulkan "kemungkinan besar sudah melewati ambang sebelum September" ✘** (rata-rata baru tembus ±Oktober) |
| Batas 7 tahun tarif 0,5% untuk OP | Disebut ✔ (nilai tambah) | Tidak disebut |
| Kode setor | — | **"KAP 411128/411125" ✘** — 411125 adalah PPh 25/29 OP, bukan PPh final UMKM (411128-420); tidak berasal dari skill (halusinasi model) |
| Dasar hukum disebut | PP 23 (usang) | PP 55/2022, PMK 81/2024 ✔ |

## Nilai

| Aspek | SEBELUM | SESUDAH |
|---|---|---|
| Ketepatan | Tanggal Okt benar; aturan PPh 21 & nama PP salah; klaim SPT nihil meragukan | Tanggal benar dari script; inferensi ambang & KAP 411125 salah |
| Siap pakai | Jawaban langsung di giliran 1 (tapi bercampur salah) | Tabel tenggat pasti + tips setor H-2/3 |
| Kepatuhan aturan ID | Dasar usang | PMK 81/2024 & PP 55/2022 |
| Keamanan/privasi | Aman | Aman |
| Kejelasan | Panjang, menyaring sendiri | Bertanya sekali lalu ringkas |
| **Total (1–10)** | **5** | **7** |

SESUDAH benar pada inti pertanyaan (tanggal pasti dari script, dasar hukum mutakhir, tidak menebak sebelum profil diketahui). Namun dua kesalahan tambahan dari model — kesimpulan ambang Rp500 juta yang terlalu cepat dan KAP 411125 — menurunkan nilainya. SEBELUM memakai aturan lama (PPh 21 tgl 10, "PP 23") yang bisa menyesatkan, walau sempat memberi poin bagus (batas 7 tahun).
