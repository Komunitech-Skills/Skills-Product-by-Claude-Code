# Uji OpenClaw sebelum/sesudah: listing-marketplace (skenario 04 dalam uji solusi VIP Toko Online; terakhir versi 1.0.4)

Berkas ini merangkum hasil uji yang **sudah tercatat** di `solusi-vip/toko-online/UJI-OPENCLAW.md` (tabel skenario 04 dan tabel uji ulang) serta tiga berkas rincinya di `solusi-vip/toko-online/uji-openclaw/`: `04-listing-info-kurang.md`, `04-listing-info-kurang-ulang.md`, `04-listing-ulang3.md`. Tidak ada uji baru untuk berkas ini; semua kutipan TANPA/DENGAN disalin dari berkas-berkas itu (dipotong seperlunya dengan tanda […]).

## Kepala

- **Tanggal uji:** 2026-10-01 (Asia/Jakarta). Tiga putaran pada hari yang sama: uji pertama, uji ulang, dan uji ulang ke-3.
- **Penguji:** agent penguji independen Komunitech (bukan pembuat skill). Sumber menyebut uji pertama "agent penguji independen", uji ulang "penguji independen", dan uji ulang ke-3 "penguji independen ke-3"; ketiganya bukan pembuat skill.
- **Versi skill yang diuji:**
  - Uji pertama: versi tidak dicatat di berkas uji. `CHANGELOG.md` skill mencatat bahwa versi 1.0.3 dibuat sebagai tanggapan atas temuan uji ini, jadi uji pertama memakai versi sebelum 1.0.3.
  - Uji ulang: **1.0.3**.
  - Uji ulang ke-3: **1.0.4** (versi uji terakhir).
- **Cara uji (dari sumber):** OpenClaw lokal (`openclaw agent --local`, tanpa Telegram/gateway), memakai model router Komunitech yang sama dengan bot member (`ninerouter/komunitech`; jawaban dilayani `claude-sonnet-5` di kedua sisi). SEBELUM = home `kosong-toko-online` (skill dimatikan: folder `~/.openclaw/skills` kosong). SESUDAH = home `sol-toko-online` (paket skill Toko Online + skill tambahan VIP terpasang di `~/.openclaw/skills`); pada uji ulang ke-3 home `sol3-toko-online` direset dari skill terbaru di repo sebelum skenario, sesi baru, hanya sisi SESUDAH. Workspace awal identik. Pesan ditulis seperti pemilik toko online awam mengetik di WA/Telegram (singkat, santai, salah ketik); skenario 04 sengaja info kurang, dua giliran, jawaban member dikirim sekali dan identik di kedua sisi.
- **Versi OpenClaw:** tidak disebut di berkas sumber. `catalog.csv` mencatat uji ini sebagai "openclaw 2026.9.6–9.7 (uji sebelum/sesudah otomatis 2026-10-01)".
- **Pemakaian skill dicek dari:** daftar tool di JSON keluaran (`successfulToolNames`) + format keluaran yang identik dengan keluaran script skill. Argumen tool call **tidak** diperiksa (lihat "Batasan uji").
- **Verifikasi angka:** panjang karakter dihitung ulang penguji dengan Python (`len`) terhadap batas di `references/batas-platform.md` skill (Shopee judul 100 / deskripsi 3.000; Tokopedia 70 / 2.000). Pada uji ulang dan uji ulang ke-3, `cek_listing.py` versi repo juga dijalankan penguji untuk cek balik.
- **Catatan jujur tentang cakupan:** uji ini dijalankan sebagai **satu skenario** (nomor 04, "info kurang") di dalam uji solusi VIP Toko Online (5 skenario untuk 5 skill berbeda), **bukan** uji 5 skenario per skill. Pembanding TANPA skill (5,5) hanya dari giliran 2 uji pertama dan **tidak diulang** di uji ulang. Versi katalog sekarang (1.0.5) lebih baru dari versi yang diuji (lihat "Catatan jujur").

## Ringkasan skor

| Putaran | Versi skill | Tanpa skill | Dengan skill | Selisih |
|---|---|:-:|:-:|:-:|
| Uji pertama | tidak dicatat (sebelum 1.0.3) | 5,5* | 8,5 | +3,0 |
| Uji ulang | 1.0.3 | 5,5 (dari uji pertama, tidak diulang) | **9** | +3,5 |
| Uji ulang ke-3 | 1.0.4 | 5,5 (dari uji pertama, tidak diulang) | **9** | +3,5 |

\* Skenario 04 SEBELUM hanya dinilai dari giliran 2; balasan giliran 1 tidak terbaca penguji (lihat "Batasan uji").

- **Skor akhir yang dipakai (uji terakhir, 1.0.4):** 5,5 → 9 dari 10.
- **Kesalahan angka di sisi DENGAN skill pada uji terakhir:** tidak ada. Panjang yang dilaporkan (673 dan 294 karakter) sama dengan hitung ulang penguji.
- **Verdik: LULUS.** Uji ulang (1.0.3) dan uji ulang ke-3 (1.0.4) sama-sama dinyatakan LULUS oleh penguji.

**Kalimat pembeda:** Tanpa skill, AI langsung menulis deskripsi hijab dengan enam klaim yang tidak pernah disebut pemilik toko (mis. "Dikirim cepat & packing aman", "Banyak pelanggan repeat order!"); dengan skill, AI bertanya sekali dulu, lalu menulis judul untuk tiga marketplace dan deskripsi terutama dari fakta pemilik, dengan panjang karakter yang cocok dengan hitung ulang penguji.

## Tugas (pesan pengguna)

Pesan identik di kedua sisi dan di semua putaran, dikirim dalam dua giliran.

**Giliran 1:**

> bikinin deskripsi produk buat hijab voal aku dong, mau upload di shopee

**Giliran 2 (jawaban member):**

> 1. hijab voal motif nama tokonya Rumah Hijab Nia  2. 115x115 voal premium, tepi lasercut  3. motif bunga: dusty pink, sage, mocca, navy  4. adem, ga licin, gampang dibentuk, ga nerawang  5. isi 1 pcs, cuci tangan aja jgn dipemutih. ga ada sertifikat. harga 59rb

## Hasil TANPA skill (uji pertama, giliran 2)

Giliran 1 sisi TANPA skill tidak dapat dibaca penguji (agent memakai alat `tool_search, memory_search, tool_call, ls, read` untuk menjelajah workspace/memori). Giliran 2: alat yang dipakai agent `tidak ada`, durasi 13 detik. Kutipan (dipotong):

> Siap, ini versi final deskripsi produknya — tinggal copy-paste ke Shopee:
>
> **🌸 HIJAB VOAL MOTIF BUNGA PREMIUM | Tepi Lasercut | Rumah Hijab Nia**
>
> […]
>
> **✨ Keunggulan produk:**
> ✅ Bahan voal premium, adem & nggak nerawang
> ✅ Nggak licin, gampang dibentuk berbagai gaya hijab
> ✅ Tepi lasercut rapi, nggak perlu obras ulang
> ✅ Motif bunga cantik, elegan & nggak pasaran
> ✅ Cocok dipakai harian, kerja, hangout, sampai acara formal
>
> […]
>
> **🛍️ Kenapa belanja di Rumah Hijab Nia?**
> 🚚 Dikirim cepat & packing aman
> 💯 Barang sesuai foto & deskripsi
> ⭐ Banyak pelanggan repeat order!
>
> **📝 Catatan:**
> - Produk ini tidak disertai sertifikat
>
> […]
>
> 💰 **Harga: Rp59.000**
>
> Mau aku bikinin juga versi singkat buat judul produk Shopee (biar kena SEO pencarian), atau ini sudah cukup?

**Kelemahan (temuan penguji):**
- Menambah enam klaim yang tidak pernah diberikan pemilik: "Dikirim cepat & packing aman", "Barang sesuai foto & deskripsi", "Banyak pelanggan repeat order!", "elegan & nggak pasaran", "cocok … sampai acara formal", "nggak perlu obras ulang". Penguji mencatat klaim seperti ini berisiko melanggar UU Perlindungan Konsumen No. 8/1999 Pasal 8–9 bila tidak benar, dan persis hal yang bisa dibantah pembeli lalu memicu ulasan buruk (seperti skenario 03 di uji yang sama).
- Menaruh "Harga: Rp59.000" di deskripsi (harga diatur di kolom harga; bila harga berubah, deskripsi jadi salah) dan kalimat canggung "Produk ini tidak disertai sertifikat".
- Tidak ada judul terpisah.
- Nilai: **5,5/10** ("rapi dan menarik, tapi menambahkan 6 klaim promosi yang tidak pernah disebut pemilik").

## Hasil DENGAN skill

### Uji pertama (versi sebelum 1.0.3): 8,5

Giliran 1 (alat `read`, 15 detik) bertanya sekali dengan lima pertanyaan bernomor, dibuka dengan:

> Oke, siap bikinin listing hijab voal buat Shopee. Aku butuh info produknya dulu biar nggak ngarang spek — tolong jawab yang bisa dijawab aja:

Giliran 2 (alat `read, exec`, 64 detik) memberi kata kunci, judul tiga platform, dan dua deskripsi. Kutipan (dipotong):

> | Platform | Judul | Panjang / batas aman |
> |---|---|---|
> | Shopee | Hijab Voal Motif Bunga Premium 115x115 Tepi Lasercut Rumah Hijab Nia | 68/100 ✅ |
> | Tokopedia | Hijab Voal Motif Bunga Premium 115x115 Lasercut | 47/70 ✅ |
> | TikTok Shop | Hijab Voal Motif Bunga Premium Lasercut 115x115 Rumah Hijab Nia | 63/100 ✅ |
>
> […]
>
> ✅ Tepi lasercut, rapi dan ga gampang buyar
>
> […]
>
> - Nggak ada sertifikat (halal/BPOM/SNI) → sengaja nggak ditulis, sesuai aturan.

Kelebihan: bertanya sekali ("biar nggak ngarang spek"), panjang judul dan deskripsi cocok dengan hitung ulang penguji (68, 47, 63; deskripsi Shopee/Tokopedia 645, TikTok 273), harga tidak dimasukkan ke deskripsi, sertifikat tidak ditulis. Kekurangan: satu klaim tambahan kecil "tepi lasercut … ga gampang buyar" (pemilik hanya menyebut "tepi lasercut") dan `cek_listing.py` tetap LULUS. Nilai: **8,5/10**.

### Uji ulang (1.0.3): 9

Giliran 1 (alat `read`, 19 detik) bertanya sekali. Giliran 2 (alat `ls, read, exec`, 90 detik). Kutipan catatan agent:

> - Aku sempat kasih kata "rapi" di deskripsi tapi dihapus karena kamu gak bilang itu — kalau tepi lasercutnya memang halus/rapi menurutmu, kasih tahu aja nanti aku tambahkan.
> - Harga 59rb gak aku taruh di deskripsi (itu diisi langsung di kolom harga Shopee, bukan teks deskripsi) — biar gak dobel info.

Kelebihan: frasa "ga gampang buyar" tidak muncul lagi; deskripsi hanya memakai fakta pemilik; penguji menjalankan `cek_listing.py --fakta` pada teks final (LULUS, "Tidak ada temuan") dan pada teks lama (GAGAL untuk 'ga gampang buyar' dan 'rapi'), jadi script kini menangkap cacat lama. Kekurangan: panjang deskripsi yang dilaporkan (505) berbeda dari teks yang tampil (515). Nilai: **9/10**.

### Uji ulang ke-3 (1.0.4, uji terakhir): 9

Giliran 1 (alat `read`, 1 panggilan, 15 detik) dan giliran 2 (alat `read, exec`, 5 panggilan, 0 gagal, 89 detik). Giliran 1 dibuka dengan:

> Oke, aku bantu bikinin listing hijab voal buat Shopee. Biar deskripsinya pas dan nggak ngarang spesifikasi, boleh dilengkapi dulu:

Giliran 2, kutipan (dipotong):

> Semua lulus cek (Shopee & Tokopedia LULUS, TikTok Shop LULUS dengan saran minor). Ini hasilnya, tinggal copy-paste ke Shopee:
>
> ## Listing: Hijab Voal Motif Bunga — Rumah Hijab Nia
>
> […]
>
> ### Judul (cek batas terbaru di Seller Center)
> | Platform | Judul | Panjang/batas aman |
> |---|---|---|
> | Shopee | Hijab Voal Motif Bunga Premium 115x115 Tepi Lasercut Rumah Hijab Nia | 68/100 |
> | Tokopedia | Hijab Voal Motif Bunga Premium 115x115 Lasercut | 47/70 |
> | TikTok Shop | Hijab Voal Motif Bunga Premium 115x115 Tepi Lasercut Rumah Hijab Nia | 68/100 |
>
> ### Deskripsi — Shopee & Tokopedia (673 karakter)
> ```
> Hijab voal motif bunga dari Rumah Hijab Nia. Bahan voal premium dengan tepi lasercut, cocok dipakai sehari-hari untuk kerja, kuliah, atau jalan santai.
>
> ✅ Bahan voal premium, adem dipakai sehari-hari
> ✅ Tidak licin, gampang dibentuk sesuai gaya
> ✅ Tepi lasercut
> ✅ Tidak nerawang
> ✅ Motif bunga, tersedia 4 pilihan warna kalem
>
> […]
> ```
>
> […]
>
> 📝 Catatan:
> - Harga 59rb nggak aku masukin ke teks deskripsi — itu kamu isi langsung di kolom harga Shopee ya.
> - "Halal/sertifikat" nggak ditulis karena kamu bilang belum ada sertifikat.
> - Batas karakter di atas adalah batas aman, cek lagi batas terbaru di Seller Center kamu.

Kelebihan: panjang yang dilaporkan sama dengan hitung ulang penguji; file di workspace identik dengan teks di chat; `cek_listing.py --fakta` versi repo (dijalankan penguji) LULUS tanpa temuan; klaim ketahanan tidak ada. Kekurangan (kecil, lolos script): "cocok … untuk kerja, kuliah, atau jalan santai" dan "warna kalem" tidak dari pemilik. Nilai: **9/10**.

## Kebenaran angka yang dicek penguji

| Putaran | Hal yang dicek | Klaim balasan | Hitung ulang penguji |
|---|---|---|---|
| Uji pertama | Judul Shopee / Tokopedia / TikTok Shop | 68/100, 47/70, 63/100 | 68, 47, 63 (cocok) |
| Uji pertama | Deskripsi Shopee & Tokopedia / TikTok | 645 / 273 | 645 / 273 (cocok) |
| Uji ulang (1.0.3) | Judul (sama di 3 platform) | 63 | 63 (cocok; Tokopedia 63/70) |
| Uji ulang (1.0.3) | Deskripsi Shopee & Tokopedia | 505 karakter | **515** (selisih 10; jauh di bawah batas 3.000/2.000) |
| Uji ulang (1.0.3) | Deskripsi TikTok | tidak dilaporkan | 256 |
| Uji ulang ke-3 (1.0.4) | Deskripsi Shopee & Tokopedia / TikTok | 673 / 294 | 673 / 294 (persis sama; file di workspace identik) |
| Uji ulang ke-3 (1.0.4) | Judul Shopee / Tokopedia | 68 / 47 | 68 / 47 (cocok) |
| Uji ulang ke-3 (1.0.4) | `cek_listing.py --fakta` (repo, dijalankan penguji) | LULUS | LULUS, 673/3000, tidak ada temuan |

Harga Rp59.000 sengaja tidak dimasukkan ke deskripsi dan sertifikat tidak diklaim di semua putaran DENGAN skill.

## Batasan uji (dari sumber)

- Argumen tool call tidak bisa diperiksa: bukti pemakaian script disimpulkan dari format keluaran yang identik dengan keluaran script. Pada uji ulang ke-3, database sesi tidak dibuka sehingga tidak terlihat instalasi paket atau `find /` dari teks/berkas, "tetapi tidak bisa dipastikan 100%".
- Balasan giliran 1 skenario 04 SEBELUM tidak terbaca (pembacaan file keluarannya diblokir pengaman sesi penguji; penguji tidak mencoba jalan lain). Perilaku "tanya sekali" sisi SEBELUM tidak dinilai; file mentahnya tetap ada di `hasil/toko-04-sebelum.txt` untuk diperiksa pemilik.
- Log `.err` berisi peringatan `SQLite reclamation Worker failed … database owner is no longer current` setelah setiap giliran, tidak memengaruhi balasan.

## Catatan jujur

- Ini satu skenario dalam uji solusi VIP Toko Online, bukan 5 skenario per skill. Skenario normal (tiga platform sekaligus, tolak klaim halal/diet, tolak barang KW) diuji di Claude Code (simulasi agent), bukan di OpenClaw: lihat `HASIL-UJI.md`.
- Versi yang diuji terakhir adalah 1.0.4 (2026-10-01); versi di `catalog.csv` sekarang 1.0.5. Menurut `CHANGELOG.md` skill, 1.0.5 (2026-10-13) mengganti rujukan ke skill yang diarsipkan dengan `konten-mingguan`; versi 1.0.5 belum diuji ulang di berkas ini.
- Nilai TANPA skill (5,5) berasal dari uji pertama dan tidak diulang pada uji ulang; selisih +3,5 membandingkan nilai TANPA uji pertama dengan nilai DENGAN uji terakhir.
- Dua tambahan kecil di uji terakhir ("warna kalem", contoh pemakaian) lolos dari `cek_listing.py`, jadi frasa "hanya dari fakta pemilik" belum berlaku mutlak.

## Rujukan

- `solusi-vip/toko-online/UJI-OPENCLAW.md` (tabel skenario 04, tabel "Uji ulang 2026-10-01", tabel "Uji ulang ke-3 2026-10-01")
- `solusi-vip/toko-online/uji-openclaw/04-listing-info-kurang.md` (uji pertama)
- `solusi-vip/toko-online/uji-openclaw/04-listing-info-kurang-ulang.md` (uji ulang, 1.0.3)
- `solusi-vip/toko-online/uji-openclaw/04-listing-ulang3.md` (uji ulang ke-3, 1.0.4)
