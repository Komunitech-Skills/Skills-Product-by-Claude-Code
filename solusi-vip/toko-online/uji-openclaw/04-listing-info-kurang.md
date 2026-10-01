# Uji OpenClaw — Toko Online · Deskripsi produk Shopee — info awal kurang (hijab voal)

Tanggal uji: 2026-10-01 (Asia/Jakarta) · Penguji independen · Skill yang diharapkan: `listing-marketplace`

OpenClaw lokal (`openclaw agent --local`), model router Komunitech (`ninerouter/komunitech`) yang sama dengan bot. SEBELUM = home `kosong-toko-online` (tanpa skill). SESUDAH = home `sol-toko-online` (paket skill solusi terpasang). Pesan identik.

## Pesan member (giliran 1)

> bikinin deskripsi produk buat hijab voal aku dong, mau upload di shopee

## Pesan member (giliran 2)

> 1. hijab voal motif nama tokonya Rumah Hijab Nia  2. 115x115 voal premium, tepi lasercut  3. motif bunga: dusty pink, sage, mocca, navy  4. adem, ga licin, gampang dibentuk, ga nerawang  5. isi 1 pcs, cuci tangan aja jgn dipemutih. ga ada sertifikat. harga 59rb

## Balasan SEBELUM (tanpa skill) — utuh

**Giliran 1 SEBELUM — tidak ditampilkan.** Balasan giliran pertama sisi tanpa skill (agent memakai alat
`tool_search, memory_search, tool_call, ls, read` — menjelajah workspace/memori) **tidak bisa dibaca penguji**: saat
membuka file keluarannya, pengaman sesi penguji (auto-mode classifier, alasan "Credential Exploration") memblokir
pembacaan. Penguji tidak mencoba jalan lain. Jawaban member (giliran 2) dikirim identik ke kedua sisi; balasan
giliran 2 SEBELUM di bawah memperlihatkan bahwa agent tanpa skill kemudian langsung menulis deskripsi final.
Konsekuensi: perilaku "tanya sekali" sisi SEBELUM tidak dinilai.

### Giliran 2

_Alat yang dipakai agent: `tidak ada` · model jawaban: `claude-sonnet-5` · durasi 13 detik_

> Siap, ini versi final deskripsi produknya — tinggal copy-paste ke Shopee:
>
> ---
>
> **🌸 HIJAB VOAL MOTIF BUNGA PREMIUM | Tepi Lasercut | Rumah Hijab Nia**
>
> Tampil cantik effortless dengan hijab voal motif bunga dari Rumah Hijab Nia! Bahan voal premium yang adem, nggak licin, dan gampang dibentuk — cocok jadi andalan harian kamu.
>
> **✨ Keunggulan produk:**
> ✅ Bahan voal premium, adem & nggak nerawang
> ✅ Nggak licin, gampang dibentuk berbagai gaya hijab
> ✅ Tepi lasercut rapi, nggak perlu obras ulang
> ✅ Motif bunga cantik, elegan & nggak pasaran
> ✅ Cocok dipakai harian, kerja, hangout, sampai acara formal
>
> **📋 Detail produk:**
> 📏 Ukuran: 115 x 115 cm
> 🧵 Bahan: Voal premium
> ✂️ Finishing: Tepi lasercut
> 🎨 Pilihan warna/motif: Dusty Pink, Sage, Mocca, Navy
> 📦 Isi: 1 pcs per pembelian
>
> **🧺 Perawatan:**
> Cuci tangan, jangan gunakan pemutih, agar warna & kualitas bahan awet.
>
> **🛍️ Kenapa belanja di Rumah Hijab Nia?**
> 🚚 Dikirim cepat & packing aman
> 💯 Barang sesuai foto & deskripsi
> ⭐ Banyak pelanggan repeat order!
>
> **📝 Catatan:**
> - Produk ini tidak disertai sertifikat
> - Warna dapat sedikit berbeda tergantung pencahayaan & pengaturan layar HP masing-masing perangkat
>
> 💰 **Harga: Rp59.000**
>
> ---
>
> Mau aku bikinin juga versi singkat buat judul produk Shopee (biar kena SEO pencarian), atau ini sudah cukup?

## Balasan SESUDAH (dengan paket skill) — utuh

### Giliran 1

_Alat yang dipakai agent: `read` · model jawaban: `claude-sonnet-5` · durasi 15 detik_

> Oke, siap bikinin listing hijab voal buat Shopee. Aku butuh info produknya dulu biar nggak ngarang spek — tolong jawab yang bisa dijawab aja:
>
> 1. **Nama/merek produk** (misal "Hijab Voal Premium [merek kamu]")?
> 2. **Ukuran** (cm, misal 110x110) dan **bahan** detailnya (voal polos/motif, double hycon, voal ceruty, dll)?
> 3. **Varian warna** yang tersedia — sebutin semua?
> 4. **Keunggulan/pembeda** dari hijab lain (misal: anti ribet, adem, nggak nerawang, jahitan rapi, ada list jahit, dll)?
> 5. **Isi paket, cara cuci/rawat, dan apakah ada sertifikat** (misal tersertifikasi halal/SNI) — kalau nggak ada, nggak apa-apa, biar aku skip aja daripada ngarang.
>
> Kirim aja apa yang kamu tahu, yang belum ada nanti aku tandain buat dilengkapi belakangan.

### Giliran 2

_Alat yang dipakai agent: `read, exec` · model jawaban: `claude-sonnet-5` · durasi 64 detik_

> Semua lulus cek (judul & deskripsi dalam batas aman, kata kunci utama terpenuhi). Fokus kamu minta Shopee, tapi aku sertakan juga Tokopedia & TikTok Shop sekalian biar bisa dipakai ulang.
>
> ## Listing: Hijab Voal Motif Bunga — Rumah Hijab Nia
>
> ### Kata kunci
> - Utama: hijab voal motif
> - Pendukung: hijab voal premium, hijab voal bunga, hijab voal lasercut
> - Ekor panjang: hijab voal motif bunga adem, hijab voal lasercut ga nerawang, hijab segiempat motif bunga
>
> ### Judul (cek batas terbaru di Seller Center)
> | Platform | Judul | Panjang / batas aman |
> |---|---|---|
> | Shopee | Hijab Voal Motif Bunga Premium 115x115 Tepi Lasercut Rumah Hijab Nia | 68/100 ✅ |
> | Tokopedia | Hijab Voal Motif Bunga Premium 115x115 Lasercut | 47/70 ✅ |
> | TikTok Shop | Hijab Voal Motif Bunga Premium Lasercut 115x115 Rumah Hijab Nia | 63/100 ✅ |
>
> ### Deskripsi — Shopee & Tokopedia (645 karakter)
> ```
> Hijab Voal Motif Bunga dari Rumah Hijab Nia. Nyaman dipakai harian, adem dan gampang dibentuk.
>
> ✅ Bahan voal premium, adem dan ga licin
> ✅ Ga nerawang, nyaman dipakai seharian
> ✅ Gampang dibentuk sesuai gaya hijab favorit
> ✅ Tepi lasercut, rapi dan ga gampang buyar
> ✅ Motif bunga, tampil manis dan effortless
>
> SPESIFIKASI
> • Ukuran: 115 x 115 cm
> • Bahan: Voal Premium
> • Motif: Bunga
> • Tepi: Lasercut
> • Varian warna: Dusty Pink, Sage, Mocca, Navy
>
> ISI PAKET
> • 1 pcs hijab voal motif bunga (pilih warna sesuai varian)
>
> CARA RAWAT
> • Cuci tangan, jangan pakai pemutih
>
> Yuk pilih warna favoritmu dan klik Beli Sekarang / Masukkan Keranjang sekarang juga!
> ```
>
> ### Deskripsi — TikTok Shop (273 karakter)
> ```
> Hijab Voal Motif Bunga - Rumah Hijab Nia
>
> ✅ Adem, ga licin, ga nerawang
> ✅ Gampang dibentuk
> ✅ Tepi lasercut rapi
> ✅ Ukuran 115x115 cm
> ✅ Motif bunga, 4 pilihan warna: Dusty Pink, Sage, Mocca, Navy
>
> Isi 1 pcs. Cuci tangan, jangan pakai pemutih.
>
> Klik keranjang kuning sekarang!
> ```
>
> ### Hasil cek
> Script `cek_listing.py` — LULUS semua (Shopee, Tokopedia, TikTok Shop). Tidak ada temuan pelanggaran (no kontak luar, no klaim berlebihan). Saran minor: deskripsi TikTok agak pendek (273 char), tapi masih aman karena TikTok memang perlu ringkas.
>
> 📝 Asumsi & catatan:
> - Harga (Rp59rb) nggak aku masukin ke deskripsi karena itu diatur lewat kolom harga, bukan teks — tinggal kamu isi di form Shopee.
> - Nggak ada sertifikat (halal/BPOM/SNI) → sengaja nggak ditulis, sesuai aturan.
> - "Cek batas terbaru di Seller Center" — batas karakter di atas pakai angka aman, bukan batas resmi final Shopee.
>
> Mau aku bikinin versi lain (lebih playful/kasual, atau fokus ke satu warna tertentu buat A/B testing)?

## Verifikasi angka & fakta (independen)

Cek panjang (Python `len`) dan batas di `references/batas-platform.md` skill (Shopee judul 100 / deskripsi 3.000; Tokopedia 70 / 2.000):

| Teks SESUDAH | Klaim | Hitung ulang |
|---|---|---|
| Judul Shopee | 68/100 | 68 ✅ |
| Judul Tokopedia | 47/70 | 47 ✅ |
| Judul TikTok Shop | 63/100 | 63 ✅ |
| Deskripsi Shopee & Tokopedia | 645 | 645 ✅ |
| Deskripsi TikTok | 273 | 273 ✅ |

Klaim yang **tidak diberikan pemilik** (berisiko melanggar UU Perlindungan Konsumen No. 8/1999 Pasal 8–9 bila tidak benar):
- **SEBELUM:** "🚚 Dikirim cepat & packing aman", "💯 Barang sesuai foto & deskripsi", "⭐ Banyak pelanggan repeat order!", "elegan & nggak pasaran", "cocok … sampai acara formal", "nggak perlu obras ulang"; juga menaruh "Harga: Rp59.000" di deskripsi (harga diatur di kolom harga; bila harga berubah, deskripsi jadi salah) dan kalimat canggung "Produk ini tidak disertai sertifikat". Tidak ada judul terpisah.
- **SESUDAH:** satu tambahan kecil "tepi lasercut … **ga gampang buyar**" (pemilik hanya menyebut "tepi lasercut"); `cek_listing.py` tidak menangkapnya. Selebihnya hanya fakta dari pemilik; sertifikat sengaja tidak ditulis.

## Nilai

| | SEBELUM | SESUDAH |
|---|---|---|
| Skor (1–10) | — / 5,5 | 8.5 |

- **SEBELUM (giliran 2) 5,5/10** — rapi dan menarik, tapi menambahkan 6 klaim promosi yang tidak pernah disebut pemilik (termasuk "barang sesuai foto" dan "banyak repeat order" — persis hal yang bisa dibantah pembeli dan memicu ulasan buruk seperti skenario 03). Tanpa judul SEO terpisah. Giliran 1 tidak dinilai (lihat catatan).
- **SESUDAH 8,5/10** — skill terpakai (giliran 1 `read` SKILL.md; giliran 2 `read` + `exec` `cek_listing.py`). Giliran 1 bertanya **sekali**, 5 pertanyaan bernomor, dengan pesan "biar nggak ngarang spek" — sesuai prinsip. Giliran 2: kata kunci, judul 3 platform dengan panjang tercek, deskripsi siap tempel, catatan asumsi. Minus: satu klaim kecil tambahan ("ga gampang buyar").

Kriteria: ketepatan, langsung siap pakai, kepatuhan aturan Indonesia, keamanan/privasi, kejelasan untuk awam.
