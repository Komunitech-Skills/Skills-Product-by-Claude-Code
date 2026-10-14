# Uji banding pesaing: rencana-restok-barang

- **Tanggal:** 2026-10-14
- **Penguji:** agent penguji independen Komunitech (bukan pembuat)
- **Kata kunci & sumber dicari (riset gelombang 29):** inventory reorder, reorder point, safety stock, demand forecasting skill, restock planning, inventory planning agent skill; skills.sh (cermin Skillselion), ClawHub, Tessl, GitHub (raw). Pesaing hanya **dibaca untuk dinilai**, tidak disalin ke skill Komunitech.
- **Pesaing yang dijalankan:**
  - **A. `inventory-demand-planning`** dari affaan-m/everything-claude-code (pesaing terkuat menurut adopsi: repo ±279 ribu bintang, ±5.200 instal skill). LICENSE repo MIT; frontmatter skill menulis `license: Apache-2.0`. Isi: panduan perencana ritel multi-lokasi (SS = Z × σ × √(LT+RP), EOQ, Croston, ABC/XYZ, promosi, markdown), tanpa script, berbahasa Inggris, konteks ritel AS. SKILL.md (24 KB) diunduh dari raw.githubusercontent.com ke folder uji terpisah, dipindai (tanpa script, tanpa instruksi berbahaya).
  - **B. `inventory-planner`** dari anthropics/knowledge-work-plugins (small-business, Apache-2.0). Isi: laju 7 & 28 hari, stok target 60 hari + lead time, barang lambat/mati, draf PO menunggu persetujuan. Hanya SKILL.md yang dipasang (file `reference/` dan gaya artefak bersama tidak ikut), jadi hasilnya sedikit di bawah versi plugin lengkap.
- **Cara uji:** OpenClaw 2026.10.2 lokal, model router sama (`claude-sonnet-5`), home terpisah berisi hanya skill pesaing, data & pesan **identik** dengan skenario 1 (`penjualan-90hari.csv`, `stok-sekarang.csv`, CV Grosir Bunda 3 hari, PT Ceria Distribusi 10 hari kelipatan 12). Kedua skill pesaing terbaca agent (A: `read SKILL.md`; B: `skills_read`).

## Hasil berdampingan (skenario 1, lokal)

| Aspek | Komunitech `rencana-restok-barang` | A. inventory-demand-planning | B. inventory-planner (Anthropic) |
|---|---|---|---|
| Kebenaran angka | Semua cocok dengan hitungan independen (125 angka) | **Salah jumlah**: subtotal CV ditulis Rp2.888.962 (benar Rp2.900.000), total Rp6.446.962 (benar Rp6.458.000) | Aritmetika benar (Rp44.265.000) |
| Metode | Rata-rata harian + tren 4 minggu, stok pengaman z × sd × √LT, ROP, stok target 14 hari, kelipatan dus | Dihitung bebas oleh model; rumus tidak ditunjukkan | Laju 7/28 hari, cakupan 60 hari + lead time, tanpa stok pengaman numerik |
| Besar belanja minggu ini | Rp9.799.000 sekarang + Rp3.351.000 minggu depan, terjadwal | Rp6,45 juta, alasan per barang singkat | **Rp44,3 juta** sekaligus (Popok 329 pcs, Botol Susu 300 pcs): berat bagi modal UMKM |
| Lonjakan Sabun 20 Sep | Ditandai + ditanyakan; tidak dibuang | Dibuang sepihak sebagai "outlier" | Tidak terdeteksi; Sabun dijadwalkan 365 pcs (Rp7.117.500) |
| Barang baru (Teether) | Data belum cukup, laju sementara, tanpa jumlah karangan (tetapi risiko kosong tidak disorot) | Dipesan 1 dus | "Jangan dipesan dulu", dipantau |
| Barang mati / berlebih | Gendongan Rp2.775.000; Dot kelebihan 213 pcs Rp1.917.000 | Disebut tanpa Rupiah | Gendongan Rp2.775.000; Dot Rp1.170.000 (definisi 60+10 hari) |
| Siap kirim ke pemasok | 2 draf WA utuh + total per pemasok | Tidak ada draf | Ditawarkan, menunggu persetujuan |
| Tanggal pesan minggu depan | Ya (17, 18, 20 Okt) | Tidak | Tidak (hanya "siap-siap minggu depan") |
| Asumsi & pertanyaan | Asumsi tertulis + 3 pertanyaan | Tidak ada | Asumsi singkat, tanpa pertanyaan |
| Lokal Indonesia | Rupiah, WA, istilah awam, disclaimer | Bahasa Indonesia dari model, tanpa WA | Bahasa Indonesia dari model, tanpa WA |
| **Nilai** | **8,5** | **5** | **6,5** |

**Kesimpulan:** skill Komunitech **unggul** atas kedua pesaing pada skenario normal utama: angka teruji vs salah jumlah (A) atau belanja 4,5× lebih besar tanpa stok pengaman dan tanpa deteksi lonjakan (B), ditambah draf WA dan jadwal pesan. Kelebihan pesaing yang patut dipelajari (ditulis ulang dengan cara sendiri, bukan disalin): A menyorot penurunan Pelampung dengan saran mencari sebabnya (komplain/harga/musim); B menampilkan **dua laju (7 & 28 hari) berdampingan** sehingga barang yang sedang naik terlihat, dan menolak menghitung hari habis untuk barang tanpa laju. Butir B ini relevan untuk cacat tren skill (lihat HASIL-UJI).

<details><summary>Jawaban lengkap pesaing A (inventory-demand-planning)</summary>

> Sudah saya hitung lengkap pakai data 90 hari penjualan + stok sekarang, dengan mempertimbangkan lead time masing-masing pemasok (CV Grosir Bunda 3 hari, PT Ceria Distribusi 10 hari + kelipatan dus isi 12), plus buffer stok pengaman biar nggak kehabisan sebelum barang datang.
>
> ## 📦 Pesan ke CV Grosir Bunda (datang 3 hari)
>
> | Barang | Jumlah Pesan | Alasan singkat |
> |---|---|---|
> | Popok Celana Bayi M isi 34 | **40 pcs** | Stok cuma 22, laku ~5-6/hari → cuma cukup 4 hari |
> | Bedak Bayi 150g | **28 pcs** | Stok cuma 9, laku ~3/hari → cuma cukup ~3 hari |
> | Minyak Telon 60ml | **8 pcs** | Stok 40 masih ada, tapi dikit-dikit biar pas target stok aman |
>
> Subtotal: **Rp2.888.962**
>
> ## 📦 Pesan ke PT Ceria Distribusi (datang 10 hari, kelipatan dus 12)
>
> | Barang | Jumlah Pesan | Alasan singkat |
> |---|---|---|
> | Botol Susu Anti Kolik 250ml | **60 pcs (5 dus)** | ⚠️ Penjualan naik tajam (~70%) 4 minggu terakhir, rata-rata sekarang ~4,6/hari — kalau pesan jumlah lama bisa kurang |
> | Tisu Basah Bayi 50 lembar | **84 pcs (7 dus)** | Stok 110 tapi laku kencang (~10/hari), lead time 10 hari butuh buffer besar |
> | Teether Silikon Buah | **12 pcs (1 dus)** | Baru mulai laku rutin 10 hari terakhir, stok tipis relatif |
>
> Subtotal: **Rp3.558.000**
>
> ### 💰 Total belanja minggu ini: **Rp6.446.962**
>
> ## ⏸️ Jangan dipesan dulu minggu ini
> - **Kaos Kaki Bayi (isi 3)** — stok 60 cukup ±25 hari, masih aman
> - **Sabun Cair Bayi 200ml** — stok 70 cukup, ada lonjakan aneh 65pcs di 20 Sept (kemungkinan borongan reseller) yang saya anggap outlier biar order tidak kebesaran
> - **Dot Bayi Silikon isi 2** — stok 260, kebanyakan, cukup 5+ bulan ke depan
> - **Selimut Bayi Bulu** — jarang laku, stok masih cukup
>
> ## 🚩 Perlu dicek manual, bukan auto-pesan
> - **Pelampung Leher Bayi** — ini yang perlu perhatian: dulu laku ~4/hari, 5 minggu terakhir anjlok jadi ~0,4/hari (stok 55 sekarang cukup sampai 4+ bulan). Coba cek: ada komplain produk? kalah saing harga? atau memang lagi sepi musim? Kalau cuma musiman, oke diamkan. Kalau ada masalah kualitas/kompetitor, perlu tindakan sebelum stoknya mubazir.
> - **Gendongan Hipseat** — cuma laku 9 pcs dalam 90 hari, dan nihil sejak awal Agustus (~2,5 bulan tidak laku sama sekali). Stok 15 pcs ini kandidat barang mati — pertimbangkan promo/diskon atau stop restock ke depannya.
>
> Kalau mau, saya bisa bikinkan jadwal otomatis supaya setiap minggu saya hitung ulang rekomendasi ini dari data penjualan terbaru.
</details>

<details><summary>Jawaban lengkap pesaing B (inventory-planner, hanya SKILL.md)</summary>

> Sudah saya hitung dari kedua file itu (penjualan 16 Jul–13 Okt 2026, 777 transaksi; stok 12 jenis barang). Asumsi: stok per file dianggap kondisi hari ini (14 Okt), lead time CV Grosir Bunda = 3 hari, PT Ceria Distribusi = 10 hari & kelipatan dus isi 12.
>
> **Ringkasan: 5 barang harus dipesan MINGGU INI, total Rp44.265.000**
>
> ## 🔴 PESAN SEKARANG (stok akan habis sebelum barang baru datang)
>
> **Ke CV Grosir Bunda (datang 3 hari) — subtotal Rp25.971.000**
> | Barang | Stok | Jual/hari (7h / 28h) | Cukup utk | Pesan | Harga | Total |
> |---|---:|---|---:|---:|---:|---:|
> | Bedak Bayi 150g | 9 | 2.9 / 3.4 | **2,7 hari** | 205 pcs | Rp11.000 | Rp2.255.000 |
> | Popok Celana Bayi M isi 34 | 22 | 5.6 / 5.6 | **3,9 hari** | 329 pcs | Rp62.000 | Rp20.398.000 |
> | Minyak Telon 60ml | 40 | 4.3 / 4.4 | **9,1 hari** | 237 pcs | Rp14.000 | Rp3.318.000 |
>
> **Ke PT Ceria Distribusi (datang 10 hari, kelipatan 12) — subtotal Rp18.294.000**
> | Barang | Stok | Jual/hari (7h / 28h) | Cukup utk | Pesan | Dus (isi 12) | Harga/pcs | Total |
> |---|---:|---|---:|---:|---:|---:|---:|
> | Tisu Basah Bayi 50 lembar | 110 | 10.7 / 9.5 | **10,3 hari** | 564 pcs | 47 dus | Rp8.500 | Rp4.794.000 |
> | Botol Susu Anti Kolik 250ml | 38 | 4.1 / 4.7 | **8,1 hari** | 300 pcs | 25 dus | Rp45.000 | Rp13.500.000 |
>
> Popok dan Bedak paling kritis — stoknya cuma cukup 3 hari, sementara pesan ke CV Grosir Bunda saja butuh 3 hari. Kalau tidak pesan hari ini, kemungkinan sempat kosong sebentar.
>
> ## 🟡 Belum darurat, tapi siap-siap minggu depan
> | Barang | Cukup utk | Pesan nanti | Pemasok |
> |---|---:|---:|---|
> | Sabun Cair Bayi 200ml | 10,2 hari | 365 pcs (Rp7.117.500) | CV Grosir Bunda |
> | Selimut Bayi Bulu | 14 hari | 19 pcs (Rp1.045.000) | CV Grosir Bunda |
> | Kaos Kaki Bayi isi 3 | 20,5 hari | 156 pcs / 13 dus (Rp2.340.000) | PT Ceria |
>
> (Semua dihitung untuk target stok 60 hari + lead time, pakai rata-rata penjualan 28 hari sebagai dasar jumlah, bukan angka 7 hari yang bisa lebih fluktuatif.)
>
> ## ⚠️ Data belum cukup — jangan dipesan dulu
> **Teether Silikon Buah** baru mulai terjual 10 hari (4–13 Okt, laku 37 pcs, lonjakan di minggu terakhir). Terlalu baru untuk dipercaya sebagai pola — pantau 1-2 minggu lagi sebelum menentukan jumlah pesan.
>
> ## 💤 Barang "mati" / stok nganggur — uang yang tertahan
> - **Gendongan Hipseat**: 0 terjual 28 hari terakhir (terakhir laku 4 Agustus), stok masih 15 pcs → **Rp2.775.000** nganggur. Ini bukan kandidat pesan ulang — justru pertimbangkan diskon/bundling.
> - **Dot Bayi Silikon isi 2**: stok 260 pcs tapi cuma laku ~1,9 pcs/hari → cukup untuk **140 hari**, kelebihan sekitar 130 pcs atau **Rp1.170.000** modal nganggur. Jangan tambah stok ini lama.
>
> Total modal yang "tidur" di dua barang ini: **Rp3.945.000**.
>
> ---
> Mau saya langsung buatkan draf PO ke masing-masing pemasok (CV Grosir Bunda & PT Ceria Distribusi) untuk daftar "pesan sekarang" di atas? Saya tunggu konfirmasi sebelum ada apa pun yang dikirim.
</details>

Jawaban skill Komunitech untuk pesan yang sama: lihat `00-openclaw-sebelum-sesudah.md` skenario 1 (SESUDAH, lokal).
