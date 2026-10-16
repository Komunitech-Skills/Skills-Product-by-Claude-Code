# Uji OpenClaw sebelum/sesudah: riset-harga-kompetitor

- **Tanggal:** 2026-10-16
- **Penguji:** agent penguji independen Komunitech (bukan pembuat skill)
- **Versi skill:** 1.0.5
- **Cara uji:** OpenClaw 2026.10.2 lokal (`openclaw agent --local`, satu giliran per panggilan), model router Komunitech `ninerouter/komunitech` (dilayani `claude-sonnet-5`, sama dengan bot member), TZ Asia/Jakarta. SEBELUM = home tanpa skill; SESUDAH = home berisi hanya `riset-harga-kompetitor` dari repo. Home dibuat ulang bersih per sampel dan pesan identik di semua sampel. Sisi SESUDAH dijalankan dua kali: lokal dan konteks kanal Telegram (`--channel telegram`, tanpa `--deliver`, tidak ada yang dikirim). Ini uji sebelum/sesudah per skill **pertama** untuk skill ini (uji internal lama: `examples/HASIL-UJI.md`; uji muat & platform otomatis: `examples/UJI-PLATFORM.md`).
- **Sampel & durasi:** SEBELUM lokal 101 detik; SESUDAH lokal 120 detik; SESUDAH konteks Telegram 71 detik.
- **Alat yang dipanggil agent:** SEBELUM tidak memanggil alat apa pun (menjawab langsung). SESUDAH lokal `read/ls/write/exec`: membaca SKILL.md dan template, menulis `pesaing-kopi-gayo.csv` di folder kerja, menjalankan `scripts/banding_harga.py`, lalu menghapus CSV itu. SESUDAH Telegram `skills_read/exec/read/write`: `find` dibatasi ke folder skill (bukan `find /`), CSV ditinggal di folder kerja. Tidak ada alat web/browser, tidak ada pencarian ke seluruh disk.
- **Data:** teks 8 produk pesaing yang ditempel member (fiktif): 250 gr, 200 gr, rentang harga, 500 gr, "1/2 kg", 1 kg, harga coret, dan 1 baris duplikat (baris 8 = baris 2). Modal Rp30.000 (sudah dengan kemasan), Shopee: admin 8% + gratis ongkir xtra 4% + PPh 0,5% + biaya proses Rp1.250, target untung minimal 20%, harga sekarang Rp58.000.

<details><summary>Data uji (pesan member, utuh)</summary>

````text
Tolong cek harga kopi gayo bubuk 250 gr saya dibanding pesaing. Ini teks produk pesaing yang saya salin:

1) Toko Kopi Sidikalang Jaya — Kopi Arabika Aceh Gayo 250gr, varian Medium Grind. Rp80.000. (website toko, belum ada ulasan)
2) Gayo Roastery — Kopi Gayo Bubuk Arabika 200 gr. Rp42.500 (coret Rp55.000). ⭐4,8 | 1,2RB terjual | Kab. Aceh Tengah
3) Kopi Pak Darmo — Arabika Gayo Bubuk Halus 250 gr. Rp54.900 - Rp62.900. ⭐4,9 | 850 terjual | Kota Medan
4) Bean Station ID — Arabika Gayo Wine 500gr. Rp109.500 (coret Rp125.000). ⭐4,9 | 500 terjual | Jakarta Selatan
5) Kedai Seduh — Kopi Gayo Bubuk 1/2 kg. Rp96.000. ⭐4,7 | 300 terjual | Bandung
6) Aroma Gayo — Kopi Arabika Gayo 1kg. Rp199.000. ⭐5,0 | 1RB terjual | Takengon
7) Kopi Rakyat — Kopi Gayo Bubuk 250g. Rp49.000 (coret Rp59.000). ⭐4,6 | 3RB+ terjual | Jakarta Timur
8) Gayo Roastery — Kopi Gayo Bubuk Arabika 200 gr. Rp42.500 (coret Rp55.000). ⭐4,8 | 1,2RB terjual | Kab. Aceh Tengah

Modal saya 30 ribu sudah sama kemasan. Jual di Shopee: admin 8%, gratis ongkir xtra 4%, PPh 0,5%, biaya proses 1.250. Target untung minimal 20%. Sekarang saya jual 58 ribu.
````
</details>

---

## Skenario 1 (normal): kopi gayo bubuk 250 gr vs 8 baris pesaing

### SEBELUM (skill mati)
> Sudah saya hitung. Ringkasnya: **harga kamu (Rp58.000) sudah di atas rata-rata pasar, tapi margin tetap sehat jauh di atas target 20%.** Detailnya:
>
> **1. Normalisasi harga pesaing ke basis 250 gr** (biar apple-to-apple, karena gramasi beda-beda)
>
> | Pesaing | Harga asli | Setara/250gr | Rating | Terjual |
> |---|---|---|---|---|
> | Kedai Seduh | Rp96.000/500gr | Rp48.000 | 4,7 | 300 |
> | Kopi Rakyat | Rp49.000/250gr | Rp49.000 | 4,6 | 3rb+ |
> | Aroma Gayo | Rp199.000/1kg | Rp49.750 | 5,0 | 1rb |
> | Gayo Roastery (2 listing sama) | Rp42.500/200gr | Rp53.125 | 4,8 | 1,2rb |
> | Bean Station (varian Wine) | Rp109.500/500gr | Rp54.750 | 4,9 | 500 |
> | Pak Darmo | Rp54.900–62.900/250gr | ~Rp58.900 | 4,9 | 850 |
> | Sidikalang Jaya | Rp80.000/250gr | Rp80.000 | — belum ada ulasan | — |
>
> **→ Band harga "normal" (buang outlier Sidikalang yang belum ada ulasan): Rp48.000–58.900**, rata-ratanya ~Rp52.000–53.000. Harga kamu Rp58.000 duduk di **papan atas**, hampir nempel Pak Darmo yang sudah rating 4,9 & 850 terjual — artinya kamu pasang harga setara toko paling established, padahal (asumsi) toko kamu belum punya histori penjualan sebanyak itu. Sidikalang yang pasang Rp80.000 tanpa ulasan itu berisiko, jangan dicontoh polanya.
>
> **2. Hitung biaya & margin di harga Rp58.000**
>
> - Potongan Shopee: 8% + 4% + 0,5% = 12,5% → Rp7.250
> - Biaya proses: Rp1.250
> - Total potongan: Rp8.500
> - Uang masuk bersih: Rp58.000 − 8.500 = Rp49.500
> - Modal: Rp30.000
> - **Laba bersih: Rp19.500**
> - = **33,6% dari harga jual**, atau **65% dari modal**
>
> Target minimal kamu 20% — baik dihitung dari modal maupun dari harga jual, harga sekarang jauh melampauinya.
>
> **3. Harga minimum biar tetap kena target 20%**
>
> - Kalau "untung 20%" = 20% dari modal → minimum **Rp42.600**
> - Kalau "untung 20%" = 20% dari harga jual → minimum **Rp46.300**
>
> Jadi kamu punya ruang gerak besar antara Rp46.300 (batas bawah margin aman) sampai Rp80.000 (batas atas pasar, berisiko).
>
> **Rekomendasi:**
>
> 1. **Kalau prioritasnya jualan cepat/bangun review & omset** (karena band harga pemenang pasar — Kopi Rakyat, Aroma Gayo, Kedai Seduh — justru di Rp48.000–50.000 dengan penjualan ratusan-ribuan): turunkan ke **Rp52.000–55.000**. Masih untung 45–53% dari modal (27–30% dari harga jual), jauh di atas target, tapi jadi lebih kompetitif untuk menarik pembeli baru.
> 2. **Kalau mau pertahankan posisi premium** di Rp58.000: perlu diferensiasi nyata (single origin, tanggal roasting, sertifikat, dll) biar sebanding dengan Pak Darmo yang sudah punya 850 terjual + rating 4,9 — tanpa itu, calon pembeli lebih pilih yang rating/jumlah terjualnya terbukti tapi lebih murah.
> 3. Pertimbangkan tambah **harga coret** (misal tampilkan Rp68.000 dicoret → Rp58.000) — pola ini dipakai 4 dari 7 pesaing (Gayo Roastery, Bean Station, Kopi Rakyat) dan terbukti menaikkan perceived discount tanpa mengorbankan margin riil kamu.
>
> Intinya: margin kamu aman di harga manapun antara 46rb–80rb, jadi ini murni soal strategi (volume vs premium), bukan soal untung-rugi.

### SESUDAH (skill aktif, konteks lokal)
> Sudah saya hitung pakai 7 dari 8 data (1 duplikat Gayo Roastery otomatis dibuang). Semua harga disetarakan ke 250 gr biar adil dibanding produk kamu.
>
> ## Riset Harga Pesaing: Kopi Gayo Bubuk (250 gr)
> Tanggal cek: 2026-10-16 | 7 pesaing dipakai dari 8 baris (1 duplikat dibuang) | Dasar: harga setara 250 gr
>
> | # | Toko | Ukuran asli | Harga tayang | Harga coret | Setara 250 gr | Per 100 g | Rating | Terjual |
> |---|---|---|---|---|---|---|---|---|
> | 1 | Sidikalang Jaya | 250 gr | Rp 80.000 | - | Rp 80.000 | Rp 32.000 | - | - |
> | 2 | Gayo Roastery | 200 gr | Rp 42.500 | Rp 55.000 | Rp 53.125 | Rp 21.250 | 4,8 | 1.200 |
> | 3 | Pak Darmo | 250 gr | Rp 54.900 (dipakai, dari rentang 54.900-62.900) | - | Rp 54.900 | Rp 21.960 | 4,9 | 850 |
> | 4 | Bean Station ID | 500 gr | Rp 109.500 | Rp 125.000 | Rp 54.750 | Rp 21.900 | 4,9 | 500 |
> | 5 | Kedai Seduh | 1/2 kg | Rp 96.000 | - | Rp 48.000 | Rp 19.200 | 4,7 | 300 |
> | 6 | Aroma Gayo | 1 kg | Rp 199.000 | - | Rp 49.750 | Rp 19.900 | 5,0 | 1.000 |
> | 7 | Kopi Rakyat | 250 g | Rp 49.000 | Rp 59.000 | Rp 49.000 | Rp 19.600 | 4,6 | 3.000 |
>
> ### Ringkasan harga pasar
> Terendah Rp 48.000 | P25 Rp 49.375 | **Median Rp 53.125** | P75 Rp 54.825 | Tertinggi Rp 80.000
>
> Harga kamu sekarang **Rp 58.000**: lebih mahal dari 6 pesaing, lebih murah dari 1 (Sidikalang Jaya) → posisi sekitar persentil ke-86 (di atas mayoritas pasar). Laba kamu saat ini **Rp 19.500/barang, margin 33,6%** — lebih tinggi dari target 20%, tapi harganya di atas kebanyakan pesaing.
>
> Pesaing paling laris: **Kopi Rakyat**, 3.000+ terjual, di harga setara Rp 49.000 (rating 4,6).
>
> ### Batas harga kamu (modal Rp 30.000 + Shopee 8% admin + 4% gratis ongkir xtra + 0,5% PPh + Rp1.250 proses, margin 20%)
> - Harga balik modal (laba 0): **Rp 35.715**
> - **Harga minimum (margin 20%): Rp 46.297**
>
> ### Rekomendasi harga (strategi tengah pasar)
> - Rentang: **Rp 49.375 - Rp 54.825**
> - Titik tengah: **Rp 53.125** → laba Rp 15.234/barang, margin 28,7%
> - Harga cantik terdekat: **Rp 52.900** → laba Rp 15.038/barang, margin 28,4%
>
> ### Promo pesaing
> 3 dari 7 pakai harga coret (diskon rata-rata 17,4%). Tidak ada yang eksplisit pasang promo ongkir di teks yang kamu kirim.
>
> ### Perlu dicek
> - Baris "Gayo Roastery" muncul 2x (data sama), yang kedua saya buang dari perhitungan.
>
> 💡 **Saran:**
> 1. Harga kamu Rp 58.000 sudah di atas 6 dari 7 pesaing padahal margin kamu (33,6%) sudah jauh di atas target 20%. Kalau mau lebih kompetitif tanpa mengorbankan target untung, turun ke kisaran **Rp 52.900 - Rp 54.900** masih memberi margin ~28%, jauh di atas batas minimum Rp 46.297.
> 2. Pesaing terlaris (Kopi Rakyat, 3rb+ terjual) justru di harga lebih murah (Rp 49.000) dengan harga coret. Kalau kamu mau bersaing di volume, harga coret + titik ~Rp 52.900-53.900 bisa jadi strategi, karena masih untung jauh di atas minimum.
> 3. Satu-satunya pesaing yang lebih mahal dari kamu (Sidikalang Jaya, Rp 80.000) belum punya ulasan — jadi posisi "premium tanpa bukti sosial" itu berisiko; produkmu lebih aman di tengah pasar yang sudah terbukti laku.
>
> **Catatan asumsi:** Rentang harga Pak Darmo pakai angka terendah (Rp 54.900) sesuai rentang yang ditampilkan. Belum ada data < Rp 100 per 100 gr pencilan, jadi semua 7 pesaing masuk statistik tanpa perlu konfirmasi tambahan.

### SESUDAH (skill aktif, konteks kanal Telegram, tanpa mengirim)
> Berikut hasil ricek harga Kopi Gayo Bubuk 250 gr kamu vs 7 pesaing (dari 8 baris yang ditempel, 1 duplikat Gayo Roastery dibuang):
>
> ## Riset Harga Pesaing: Kopi Gayo Bubuk (250 g)
> Tanggal analisis: 2026-10-16 | Dasar banding: harga disetarakan ke 250 g
>
> | # | Toko | Ukuran asli | Harga tayang | Harga coret | Harga setara 250g | Per 100g | Rating | Terjual |
> |---|---|---|---|---|---|---|---|---|
> | 1 | Sidikalang Jaya | 250gr | Rp 80.000 | - | Rp 80.000 | Rp 32.000 | - | - |
> | 2 | Gayo Roastery | 200 gr | Rp 42.500 | Rp 55.000 | Rp 53.125 | Rp 21.250 | 4,8 | 1.200 |
> | 3 | Kopi Pak Darmo | 250 gr | Rp 54.900 | - | Rp 54.900 | Rp 21.960 | 4,9 | 850 |
> | 4 | Bean Station ID | 500gr | Rp 109.500 | Rp 125.000 | Rp 54.750 | Rp 21.900 | 4,9 | 500 |
> | 5 | Kedai Seduh | 1/2 kg | Rp 96.000 | - | Rp 48.000 | Rp 19.200 | 4,7 | 300 |
> | 6 | Aroma Gayo | 1kg | Rp 199.000 | - | Rp 49.750 | Rp 19.900 | 5,0 | 1.000 |
> | 7 | Kopi Rakyat | 250g | Rp 49.000 | Rp 59.000 | Rp 49.000 | Rp 19.600 | 4,6 | 3.000+ |
>
> ### Ringkasan harga pasar
> Terendah Rp 48.000 — P25 Rp 49.375 — **Median Rp 53.125** — P75 Rp 54.825 — Tertinggi Rp 80.000
>
> Harga kamu sekarang **Rp 58.000** = lebih mahal dari 6 dari 7 pesaing (posisi ~persentil 86, cuma lebih murah dari Sidikalang Jaya). Pesaing terlaris (Kopi Rakyat, 3rb+ terjual) justru di harga paling murah: Rp 49.000.
>
> ### Batas harga kamu (modal Rp 30.000 + kemasan, Shopee: admin 8% + ongkir 4% + PPh 0,5% + proses Rp1.250, target margin 20%)
> - Harga balik modal: Rp 35.715
> - **Harga minimum (margin 20%): Rp 46.297**
> - Di harga sekarang Rp 58.000, labamu sebenarnya sudah Rp 19.500/pcs (margin 33,6%) — jauh di atas target 20%.
>
> ### Rekomendasi harga
> - Rentang wajar: **Rp 49.375 - Rp 54.825**
> - Titik rekomendasi: **Rp 53.125**
> - Harga cantik: **Rp 52.900** (laba Rp 15.038, margin 28,4%) — masih jauh di atas batas minimum 20%
>
> ### Promo pesaing
> 3 dari 7 pakai harga coret (diskon rata-rata 17,4%), tidak ada yang pasang promo ongkir eksplisit di teks.
>
> 💡 Saran:
> 1. Harga kamu (Rp 58.000) sekitar 9-18% lebih mahal dari harga pasar wajar — kemungkinan ini salah satu alasan kalah bersaing dari toko ber-rating tinggi seperti Kopi Rakyat dan Kedai Seduh.
> 2. Turun ke **Rp 52.900** tetap kasih margin sehat 28% (lebih dari target 20%), sekaligus lebih kompetitif — bisa tambah harga coret dari Rp 58.000 jadi Rp 52.900 biar kelihatan diskon (asal memang pernah dijual Rp58.000).
> 3. Pesaing terlaris pakai harga rendah + sudah banyak terjual/rating tinggi untuk dongkrak kepercayaan pembeli baru. Kalau rating/jumlah terjual kamu masih sedikit, strategi harga di bagian bawah rentang (≈Rp 49.900-52.900) + harga coret bisa bantu menarik pembeli pertama.
> 4. Sidikalang Jaya di Rp 80.000 tanpa ulasan — bukan patokan bagus karena posisinya outlier mahal tanpa bukti sosial.
>
> Catatan: harga pesaing hanya potret saat ditempel, belum termasuk ongkir/voucher, bisa berubah sewaktu-waktu. Tidak ada link yang perlu dicek ulang karena semua data dari teks yang kamu salin.

### Verifikasi angka

Dihitung ulang penguji dengan Python `Fraction` (tanpa mengimpor script skill). Harga setara 250 gr = harga ÷ isi × 250 (200 gr → ×1,25; 500 gr dan "1/2 kg" → ×0,5; 1 kg → ×0,25). Persentil = interpolasi linear (PERCENTILE.INC). Biaya marketplace = 12,5% dari harga jual + Rp1.250. Laba = harga − 12,5% × harga − Rp1.250 − Rp30.000. Rentang harga Pak Darmo (Rp54.900–Rp62.900) memakai angka terendah, sesuai aturan skill. Batas pencilan skill (di bawah separuh atau di atas dua kali median, yaitu < Rp26.562,5 atau > Rp106.250) tidak mengeluarkan siapa pun, termasuk Rp80.000.

| Cek | Acuan independen | SEBELUM | SESUDAH lokal / Telegram |
|---|---|---|---|
| Duplikat | Baris 8 = baris 2 (Gayo Roastery) | Dicatat "2 listing sama" ✓ | Dibuang dan disebut ✓ / ✓ (di kalimat pembuka) |
| Setara 250 gr | 80.000; 53.125; 54.900; 54.750; 48.000; 49.750; 49.000 | Benar untuk 6 pesaing; Pak Darmo dipakai titik tengah "~Rp58.900" tanpa penjelasan | Semua cocok ✓; per 100 g cocok ✓ / sama, tetapi Pak Darmo ditulis "Rp 54.900" tanpa menyebut rentang aslinya |
| Statistik | Median Rp53.125, P25 Rp49.375, P75 Rp54.825, terendah Rp48.000, tertinggi Rp80.000, rata-rata Rp55.646 | Tidak ada median/kuartil; "rata-rata ~Rp52.000–53.000" tanpa Sidikalang (acuan Rp52.254 dengan Pak Darmo Rp58.900) ✓ kira-kira | Cocok ✓ / ✓ |
| Posisi Rp58.000 | Lebih mahal dari 6 dari 7 (persentil ±86) | "Papan atas" ✓ | ✓ / ✓ |
| Laba di Rp58.000 | Potongan Rp7.250 + Rp1.250 = Rp8.500; laba **Rp19.500** = 33,6% dari harga = 65% dari modal | ✓ (keduanya disebut) | ✓ / ✓ |
| Harga balik modal | (30.000 + 1.250) ÷ 0,875 = 35.714,29 → **Rp35.715** | Tidak ada | ✓ / ✓ |
| Harga minimum untung 20% | Dari harga jual: 31.250 ÷ 0,675 = 46.296,30 → **Rp46.297**. Dari modal (laba ≥ Rp6.000): 37.250 ÷ 0,875 = 42.571,43 → **Rp42.572** | Dua tafsir disebut: Rp46.300 dan Rp42.600 (dibulatkan ke atas ke ratusan, aman) ✓ | Rp46.297 ✓ / ✓, tetapi **tidak dijelaskan** bahwa 20% itu dari harga jual (tafsir dari modal tidak disebut) |
| Rekomendasi | Rentang P25–P75 Rp49.375–Rp54.825, titik Rp53.125 (laba Rp15.234, 28,7%), harga cantik Rp52.900 (laba Rp15.038, 28,4%) | "Rp52.000–55.000": **"untung 45–53% dari modal" salah**, seharusnya 47,5–56,3% (27–30% dari harga jual: kira-kira benar, acuan 27,4–30,7%) | Cocok ✓ / ✓ |
| Harga coret | 3 dari 7 pesaing (Gayo Roastery 22,7%, Bean Station 12,4%, Kopi Rakyat 16,9%; rata-rata 17,4%) | **"4 dari 7 pesaing"** padahal yang disebut 3 dan memang 3 | ✓ / ✓ |
| Angka turunan lain | Rp58.000 vs median +9,2%, vs P25 +17,5%, vs P75 +5,8%; margin di Rp52.900–Rp54.900 = 28,4–30,6% | "aman di harga manapun antara 46rb–80rb" (Rp46.000 → margin 19,6%, sedikit di bawah 20%) | Lokal "Rp52.900–Rp54.900 masih memberi margin ~28%" (ujung bawah; ujung atas 30,6%) / Telegram "9–18% lebih mahal dari harga pasar wajar" (dasar tidak disebut; terhadap rentang wajar yang ditulis sendiri seharusnya 5,8–17,5%) |

**Tafsir "untung minimal 20%".** Kalimat member ambigu. Skill memakai **margin dari harga jual** (laba ÷ harga), sehingga minimum Rp46.297. Bila yang dimaksud 20% dari modal, minimum Rp42.572. Tafsir skill lebih ketat sehingga aman, dan harga sekarang maupun rekomendasi jauh di atas keduanya. Namun hanya jawaban SEBELUM yang menjelaskan kedua tafsir. Kedua jawaban SESUDAH hanya menulis "margin 20%", padahal keluaran script menulis "Target margin (laba / harga jual)". Keterangan itu terbuang saat disalin.

**Skor:**
- **SEBELUM: 5/10** (dibatasi maks. 5 karena salah angka; tanpa batas itu ±7). Normalisasi benar, duplikat dan varian "Wine" dicatat, dua tafsir 20% dihitung, laba di harga sekarang benar, dan saran strategi masuk akal. Kekurangannya: dua salah angka ("45–53% dari modal" dan "harga coret 4 dari 7"). Pak Darmo diam-diam dipakai titik tengah. Tidak ada median/kuartil, harga balik modal, per 100 g, atau kolom harga coret, dan rentang rekomendasinya kasar. Jawaban juga **menyarankan harga coret fiktif Rp68.000** ("tampilkan Rp68.000 dicoret → Rp58.000"), padahal harga itu tidak pernah dipakai. Cara ini berisiko dianggap diskon menyesatkan menurut UU 8/1999 Perlindungan Konsumen Pasal 9.
- **SESUDAH lokal: 8,5/10.** Tabel 7 pesaing lengkap (harga tayang, harga coret, setara 250 gr, per 100 g, rating, terjual) dan duplikat dibuang di bagian "Perlu dicek". Asumsi rentang Pak Darmo disebut. Statistik, posisi persentil 86, harga balik modal, harga minimum, rentang, titik, dan harga cantik dengan laba/margin semuanya cocok 100%. Promo diberi rata-rata diskon 17,4%, dan tiga saran berbasis data. Tidak ada kata proses. Dikurangi karena definisi 20% tidak dijelaskan, kalimat penutup rancu ("Belum ada data < Rp 100 per 100 gr pencilan…"), "~28%" untuk kisaran yang sebenarnya 28,4–30,6%, kolom lokasi hilang, dan varian "Wine" serta 1 kg (bubuk atau biji?) tidak ditanyakan.
- **SESUDAH konteks Telegram: 7,5/10.** Angka inti sama benarnya, jawaban utuh di chat, dan ada pengaman harga coret jujur ("asal memang pernah dijual Rp58.000"). Dikurangi karena rentang Pak Darmo tidak disebut (catatan script terbuang, jadi harga tayang tampil Rp54.900 saja). Saran 1 juga mengarang "kemungkinan ini salah satu alasan kalah bersaing" (member tidak bilang kalah) dan menyebut Kopi Rakyat dan Kedai Seduh "ber-rating tinggi", padahal rating 4,6 dan 4,7 itu dua terendah di daftar. Kekurangan lain: "9–18%" tanpa dasar yang jelas, definisi 20% tidak dijelaskan, bagian "Perlu dicek" hilang, salah ketik "ricek", dan CSV ditinggal di folder kerja tanpa disebut.

---

## Ringkasan

| Sampel | SEBELUM | SESUDAH |
|---|:-:|:-:|
| 1 lokal | 5 (±7 tanpa batas salah angka) | 8,5 |
| 1 konteks Telegram | (SEBELUM yang sama) | 7,5 |
| **Rata-rata** | **5** | **8,0** |

Selisih **+3,0**. **VERDIK: LULUS** (SESUDAH 8,0 ≥ 8, selisih 3,0 ≥ 1,5, tidak ada salah angka di sisi SESUDAH). **Pra-cek konteks Telegram: LOLOS dengan catatan.** Jawaban utuh di chat dan angkanya benar, tetapi mutu narasinya di bawah sampel lokal.

### Pembeda (satu kalimat)
Tanpa skill, bot memberi kisaran kasar dengan dua salah hitung ("untung 45–53% dari modal" di Rp52–55 rb, seharusnya 47,5–56,3%; "harga coret 4 dari 7", padahal 3) dan menyarankan harga coret fiktif Rp68.000. Dengan skill, semua harga disetarakan ke 250 gr, duplikat dibuang, median pasar Rp53.125 (P25 Rp49.375–P75 Rp54.825), harga minimum Rp46.297, dan harga cantik Rp52.900 (laba Rp15.038, margin 28,4%), semuanya cocok 100% dengan hitungan independen.

### Catatan jujur
- **Kelulusan bergantung pada aturan batas salah angka.** Tanpa batas maks. 5, SEBELUM bernilai ±7 dan selisihnya hanya ±1,0 (di bawah acuan 1,5). Salah angka SEBELUM tergolong ringan (persen untung dari modal dikecilkan 2,5–3,3 poin, hitungan harga coret meleset satu) dan tidak mengubah keputusan harga. Model dasar sudah menyetarakan ukuran dengan benar dan malah lebih baik dalam menjelaskan tafsir "untung 20%".
- Rata-rata SESUDAH tepat di ambang 8,0. Sampel konteks Telegram (7,5) lebih lemah daripada lokal (8,5) karena agent merangkum keluaran script dengan bebas dan membuang catatan asumsi.
- Satu skenario normal saja, dengan satu sampel per sisi (SESUDAH dua konteks). Skenario info kurang, data rusak, dan di luar cakupan tidak diulang di putaran ini (lihat `examples/04`, `05`, `HASIL-UJI.md`).
- Yang dinilai adalah teks jawaban OpenClaw (`--channel telegram` tanpa `--deliver`), bukan tampilan tabel di aplikasi Telegram sungguhan. Tabel 9 kolom kemungkinan sulit dibaca di layar ponsel.
- Varian "Arabika Gayo Wine" (proses wine) dan dua produk tanpa kata "bubuk" (500 gr Bean Station, 1 kg Aroma Gayo) mungkin tidak sebanding. Tidak ada sisi yang menanyakannya. Bila keduanya dikeluarkan, median berubah.

### Cacat untuk pembuat
1. **Catatan asumsi dari script terbuang saat dirangkum** (terutama di konteks Telegram): "rentang Rp54.900–Rp62.900, dipakai terendah" dan "Target margin (laba / harga jual)". Wajibkan kolom Catatan dan baris definisi margin disalin apa adanya, juga di versi ringkas untuk chat.
2. **Tafsir "untung X%" ambigu.** Bila member menulis "untung minimal 20%" tanpa "dari harga jual", sebut satu kalimat: "20% saya hitung dari harga jual (minimum Rp46.297); bila maksudnya 20% dari modal, minimumnya Rp42.572". Opsi baru script `--markup` (laba ÷ modal; belum ada di 1.0.5) akan membuat angka kedua dihitung, bukan dikira.
3. **Saran tidak boleh mengarang kondisi member** ("kalah bersaing") atau melabeli data secara keliru ("ber-rating tinggi" untuk rating terendah). Tambahkan aturan: saran hanya dari angka di tabel, dan perbandingan persen harus menyebut dasarnya (median atau P25/P75).
4. **Keterbandingan varian:** minta agent menanyakan sekali bila nama produk pesaing menyebut varian/proses berbeda ("Wine", "Honey", "Peaberry") atau tidak menyebut bentuk (bubuk/biji).
5. (Ringan) CSV kerja ditulis/dihapus tanpa disebut ke member (aturan kerja: sebut lokasi file baru), dan kalimat rancu "data < Rp 100 per 100 gr pencilan".

### Cuplikan jualan
> **Tanpa skill**, bot memberi kisaran harga kasar, salah menghitung persen untung, dan bahkan menyarankan memasang harga coret fiktif Rp68.000. **Dengan skill**, cukup tempel teks produk pesaing: semua ukuran disetarakan ke 250 gr, duplikat dibuang, median pasar Rp53.125, harga minimum agar tetap untung Rp46.297, dan harga cantik Rp52.900 (untung Rp15.038 per bungkus), semuanya dihitung, bukan dikira.
