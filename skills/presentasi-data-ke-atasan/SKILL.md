---
name: presentasi-data-ke-atasan
description: Mengubah angka/tabel/hasil analisis (omzet, biaya iklan, stok, kinerja tim) menjadi pesan untuk atasan/pemilik usaha/investor/bank - satu kalimat inti ("so what"), 3 angka pendukung, grafik yang tepat, risiko, dan rekomendasi - dalam 4 format siap pakai: ringkasan WA 5 baris, email formal, 1 halaman eksekutif, dan skrip bicara 2 menit. Gunakan saat pengguna sudah punya angka/hasil analisis dan bertanya "tolong buatkan ringkasan untuk bos/owner/atasan", "gimana cara sampaikan ini ke investor/bank", "bikin executive summary", "laporan ke atasan dari data ini", present data to boss, executive summary, data storytelling. Bukan untuk menghitung/mengolah data mentah dari nol (analisis-excel, rekap-penjualan-csv) atau membuat slide presentasi lengkap (presentasi-instan).
---

# Presentasi Data ke Atasan

> **Aturan kerja:** Jangan menginstal paket/aplikasi (mis. `pip install`) — bila perlu, tunjukkan caranya dan biarkan pengguna yang memasang; jangan membuka atau mencari file selain yang diberikan pengguna, isi folder skill ini, dan file yang disebut di langkah kerja; jangan menulis file baru tanpa menyebut lokasinya, dan simpan hasil di folder kerja yang disepakati (bukan /tmp).

## Tujuan
Pengguna sudah punya **angka atau hasil analisis** (dari `analisis-excel`,
`rekap-penjualan-csv`, laporan kasir, atau disebutkan langsung di chat) dan butuh
mengubahnya jadi pesan yang bisa dibaca/dipahami atasan, pemilik usaha, investor, atau
bank **dalam hitungan detik** — bukan tabel mentah yang harus ditafsirkan sendiri.

Prinsip inti: **kesimpulan dulu, baru bukti** (kebalikan cara berpikir analis yang
biasa menulis proses dulu baru kesimpulan di akhir). Atasan yang sibuk membaca baris
pertama saja — baris itu harus sudah menjawab "jadi bagaimana?" ("so what").

## Kapan digunakan
- "Tolong buatkan ringkasan untuk bos/owner dari data ini"
- "Gimana cara sampaikan penurunan omzet ini ke investor/bank?"
- "Bikinkan executive summary dari hasil analisis ini"
- "Saya mau lapor ke atasan tapi bingung mulai dari mana"
- Sudah ada hasil dari `analisis-excel`/`rekap-penjualan-csv` dan pengguna minta itu
  "dijadikan laporan buat atasan" atau "dikirim ke owner"

## Kapan TIDAK digunakan
- Data mentah belum diolah (file Excel/CSV belum dianalisis) → jalankan dulu
  `analisis-excel` (data campuran/keuangan/stok) atau `rekap-penjualan-csv` (ekspor
  kasir/Shopee/Tokopedia), **baru** hasilnya dibawa ke skill ini.
- Pengguna minta **slide/deck presentasi lengkap** (banyak halaman, untuk ditampilkan di
  layar/proyektor) → `presentasi-instan`. Skill ini fokus ke **1 pesan inti** dalam
  format pendek (WA/email/1 halaman/skrip bicara), bukan deck bertahap.
- Laporan status kerja rutin (3P: Progres-Rencana-Kendala, tanpa fokus ke satu angka
  kunci) → `laporan-status-kantor`.
- Menghitung angka dari nol (PPN, HPP, gaji, THR) → skill hitung yang sesuai; hasilnya
  baru dibawa ke sini sebagai bahan.
- Data yang disebutkan pengguna tidak jelas asalnya atau kelihatan mengarang-arang →
  tanyakan dulu sumbernya; skill ini **tidak boleh mengarang angka**.

## Input
| Info | Wajib? | Default bila tidak disebut |
|---|---|---|
| Angka/tabel/hasil analisis (data mentah, atau hasil dari skill analisis lain) | Ya | — (tanyakan; jangan mengarang) |
| Untuk siapa (atasan/pemilik, investor, bank, klien) | Ya | Tebak dari konteks; sebutkan asumsi |
| Konteks/tujuan (lapor rutin, minta keputusan, minta dana, jelaskan masalah) | Tidak | Tebak dari data; sebutkan asumsi |
| Format yang diinginkan (WA/email/1 halaman/skrip bicara) | Tidak | Buat **keempatnya** sekaligus (lihat Format Output) |
| Periode pembanding (bulan ini vs lalu, dsb.) | Tidak, jika data sudah berupa perbandingan | Tanyakan bila perlu hitung selisih/persen dan belum jelas dua titik datanya |
| Nada (formal/santai) | Tidak | Sopan-langsung ala kantor Indonesia |

Jika data mentah (bukan hasil analisis) dan info wajib kurang, tanyakan **sekali** dalam
satu pesan singkat, contoh gabungan:
1. Angka/datanya yang mana saja yang mau disampaikan? (boleh kirim file atau ketik angkanya)
2. Ini untuk siapa — atasan/owner, investor, bank, atau klien?
3. Tujuannya lapor rutin, minta keputusan/persetujuan, atau minta dana/pinjaman?

Bila pengguna terburu-buru dan hanya memberi angka mentah, buat asumsi wajar (penerima =
atasan langsung, tujuan = lapor kondisi terkini) dan sebutkan di akhir hasil.

## Langkah kerja

1. **Kumpulkan angka dari sumber yang jelas.** Angka **hanya boleh** berasal dari data
   yang diberikan pengguna atau hasil skill analisis lain (`analisis-excel`,
   `rekap-penjualan-csv`). Jangan pernah mengisi angka yang tidak disebutkan/tidak ada
   di data, sekalipun terdengar masuk akal.
2. **Hitung selisih/persen perubahan lewat script**, jangan dikira-kira. Path relatif
   terhadap folder skill ini; di Windows ganti `python3` dengan `python`/`py`:
   ```bash
   python3 <folder-skill-ini>/scripts/hitung_perubahan.py \
     --pasangan "Omzet:32000000:24500000" \
     --pasangan "Biaya iklan:4000000:5600000"
   ```
   Angka boleh ditulis seperti pengguna mengetiknya (`38.000`, `Rp 1.250.000`, `2,5`, `38rb`,
   `1,5jt`); bentuk ragu (`38.5`, `1,500`) ditolak script, jadi tanyakan maksudnya ke pengguna.
   Untuk total/rata-rata dari daftar angka (mis. omzet harian), pakai `--daftar
   "Label=angka1,angka2,..."` (pakai `;` sebagai pemisah bila ada koma desimal/rb/jt). Jika Python tidak tersedia, hitung manual langkah demi
   langkah (selisih = baru − lama; persen = selisih ÷ lama × 100, bulatkan 1 desimal)
   dan beri tahu pengguna hasil belum diverifikasi script.
3. **Rumuskan satu kalimat inti ("so what").** Bukan topik ("Laporan omzet September"),
   tapi kesimpulan yang bisa berdiri sendiri: apa yang terjadi + dampaknya, dalam satu
   kalimat. Contoh: "Omzet Agustus turun 23% karena bulan puasa, tapi margin tetap aman
   berkat efisiensi biaya iklan." Tes: kalau atasan cuma baca kalimat ini saja, apa dia
   sudah tahu apa yang harus dipikirkan/dilakukan?
4. **Pilih 3 angka pendukung** (bukan 5, bukan 1) yang paling menjelaskan kalimat inti —
   tiap angka harus punya satuan jelas (Rp, %, unit) dan berasal dari langkah 1–2. Buang
   angka menarik tapi tidak mendukung kalimat inti.
5. **Pilih grafik yang tepat** (lihat `references/pilih-grafik.md`) — hanya bila format
   output yang dipakai bisa menampilkan gambar (email/1 halaman); untuk WA/skrip bicara,
   gambarkan tren dengan kata ("naik 3 bulan berturut-turut") tanpa memaksakan grafik.
6. **Rumuskan risiko & rekomendasi.** Risiko = apa yang bisa terjadi bila dibiarkan
   (dengan angka bila memungkinkan). Rekomendasi = tindakan spesifik + siapa +
   kapan, bukan saran umum ("tingkatkan penjualan" ❌ vs "naikkan budget iklan Shopee
   Rp2 juta/bulan mulai minggu depan, PIC: Admin Toko" ✅). Bila data tidak cukup untuk
   rekomendasi spesifik, katakan itu dan sarankan data tambahan yang dibutuhkan —
   jangan mengarang rekomendasi.
7. **Susun ke format yang diminta** (lihat Format Output). Semua format memakai kalimat
   inti dan angka yang **sama** — hanya panjang & gaya penyampaian yang berbeda per
   kanal, sesuai `references/gaya-komunikasi.md`.
8. **Sebutkan asumsi** (penerima, periode, sumber data) di baris terakhir bila ada yang
   ditebak.

## Format Output

Bila pengguna tidak menyebut format, buat keempatnya. Bila hanya minta satu, buat itu
saja tapi sebut bahwa format lain tersedia.

### 1. Ringkasan WA (5 baris)
```
📊 *<Topik singkat>*
<Kalimat inti/so what>
• <angka 1>
• <angka 2>
• <angka 3>
👉 <rekomendasi/tindak lanjut singkat>
```

### 2. Email formal
Subjek + salam pembuka singkat + 1 paragraf kalimat inti & konteks + 3 angka pendukung
(poin) + risiko singkat + rekomendasi dengan PIC/tenggat + penutup. Lihat
`templates/email-formal.md`.

### 3. Satu halaman eksekutif
Struktur piramida: **Kesimpulan** di paling atas (tebal, 1 kalimat) → **3 angka
pendukung** (kartu/tabel ringkas, bukan tabel mentah) → **Grafik** (bila relevan) →
**Risiko** → **Rekomendasi** (aksi + PIC + tenggat) → catatan sumber data & periode di
bawah. Lihat `templates/satu-halaman-eksekutif.md`.

### 4. Skrip bicara 2 menit
Naskah lisan siap dibaca: kalimat pembuka (inti langsung, bukan basa-basi panjang) → 3
angka disampaikan dengan jeda alami → risiko singkat → rekomendasi/ajakan keputusan →
kalimat penutup yang membuka sesi tanya jawab. ±280–320 kata (≈2 menit bicara normal).
Lihat `templates/skrip-bicara.md`.

## Gaya komunikasi
Sopan-langsung ala kantor Indonesia: tidak berbelit, tidak menyalahkan pihak lain secara
langsung, tapi juga tidak menutup-nutupi masalah. Hindari jargon ("leverage",
"synergize", "low-hanging fruit"). Angka Rupiah selalu ditulis `Rp1.250.000` (bukan
`1250000` atau `Rp 1.250.000,-`), persen dengan tanda `%` menempel tanpa spasi ganda
(`23%`, bukan `23.0 %`). Detail lengkap di `references/gaya-komunikasi.md`.

## Batasan & Penanganan Error
- **Tidak menghitung angka baru dari nol** (PPN, HPP, payroll) — hanya mengolah angka
  yang sudah ada/dihitung skill lain menjadi pesan. Arahkan ke skill hitung yang sesuai
  bila pengguna minta perhitungan dari nol.
- **Tidak membuat slide/deck bergambar banyak halaman** → arahkan ke `presentasi-instan`
  bila itu yang diminta (skill ini bisa jadi bahan slide pertama/ringkasan pembuka deck
  tersebut).
- **Tidak boleh mengarang angka, tren, atau kutipan** yang tidak ada di data pengguna.
  Bila data tidak cukup untuk salah satu dari "3 angka pendukung", tanyakan datanya atau
  sebutkan eksplisit "data ini belum tersedia" — jangan isi dengan perkiraan tanpa label.
- **Data kualitatif saja (tanpa angka sama sekali):** tetap bisa dipakai, tapi kalimat
  inti & "angka pendukung" diganti fakta konkret (mis. jumlah keluhan, tanggal kejadian)
  dan skill menyebutkan bahwa ini bukan data kuantitatif.
- **Angka mencurigakan** (mis. persentase > 1000%, selisih negatif tapi dilabeli "naik")
  → tunjukkan hasil hitungan script apa adanya dan tanyakan ke pengguna, jangan diam-diam
  diperbaiki sendiri.
- **Nilai lama negatif** (mis. laba rugi dari -Rp5.000.000 ke Rp2.000.000): script tetap
  menghitung persennya secara matematis benar, tapi keluarannya menyertakan `catatan`
  yang menjelaskan persen dari basis negatif membingungkan dibaca sekilas (bisa
  berlawanan arah dengan label "naik/turun"). Ikuti catatan itu: sampaikan **arah dan
  selisih Rupiah saja** ke pengguna, jangan tampilkan angka persennya mentah-mentah.
- **Tolak permintaan memoles/memalsukan/membulatkan angka demi terlihat bagus** —
  misalnya pengguna minta persen penurunan "dikecilkan sedikit biar tidak terlalu
  buruk di depan atasan", angka dibulatkan ke arah yang menguntungkan tanpa dasar, atau
  arah tren "naik/turun" dibalik dari kenyataan data. Tolak dengan sopan dan jelaskan
  alasannya (angka yang dipoles merusak kepercayaan bila ketahuan, dan keputusan atasan
  jadi salah arah), lalu tawarkan **alternatif jujur**: sorot sisi positif yang benar
  ada di data (mis. margin tetap aman, tren membaik dibanding 2 bulan sebelumnya,
  rencana perbaikan yang sudah disiapkan) alih-alih mengubah angkanya.
- Bukan nasihat keuangan/investasi — untuk keputusan bernilai besar (pengajuan dana,
  laporan ke bank), sarankan tetap ditinjau oleh pemilik usaha/akuntan sebelum dikirim.
