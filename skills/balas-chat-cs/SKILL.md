---
name: balas-chat-cs
description: Membuat balasan chat customer service (CS) untuk WhatsApp dan chat marketplace (Shopee, Tokopedia, TikTok Shop, dll.) berbahasa Indonesia sesuai nada brand, mulai dari FAQ (stok, ongkir, cara order, pembayaran, jam buka) sampai komplain (barang rusak, telat, salah kirim, kurang) dengan alur empati → solusi → tindak lanjut; juga bisa menyusun bank jawaban/template quick reply dari info toko. Gunakan saat pengguna minta balas chat pelanggan, template CS, auto reply, quick reply, atau customer service reply / complaint handling. Bukan untuk ulasan/rating publik (pakai balas-ulasan-pelanggan).
---

# Balas Chat CS

## Tujuan
Membuat admin toko bisa membalas chat pelanggan dengan cepat, ramah, konsisten, dan tidak salah janji — baik membalas satu chat yang sedang masuk maupun menyiapkan **bank jawaban** (quick reply) untuk dipakai berulang.

## Kapan digunakan
- Pengguna menempel chat pelanggan: "Kak, paketku kok belum sampai?" → minta balasan.
- "Buatin template balasan CS untuk toko skincare-ku" / "bikin quick reply Shopee".
- Pelanggan marah/komplain (barang rusak, salah warna, kurang item, telat, tidak sesuai foto).
- Menyusun auto reply / pesan sapaan / pesan di luar jam kerja.

## Kapan TIDAK digunakan
- Membalas **ulasan/rating publik** di marketplace/Google Maps → `balas-ulasan-pelanggan`.
- Menagih pembayaran yang sudah lewat tempo → `tagih-piutang`.
- Mengejar calon pembeli yang tidak membalas → `follow-up-prospek`.
- Kirim promo massal → `broadcast-wa`.
- Jika skill rujukan di atas tidak terpasang, beri satu draf netral singkat dan jelaskan perbedaannya.
- Sengketa hukum, ancaman lapor polisi/BPSK, atau klaim cedera/kesehatan akibat produk: tulis balasan penenang yang netral saja, lalu sarankan pemilik usaha menangani langsung / berkonsultasi dengan ahli hukum.

## Input
| Info | Wajib? | Default jika tidak diberikan |
|---|---|---|
| Chat pelanggan (teks/tangkapan layar) **atau** permintaan bank jawaban | Ya | — (tanyakan) |
| Saluran: WA / marketplace (sebutkan yang mana) | Tidak | WhatsApp |
| Info toko relevan: produk, harga, stok, jam operasional, ekspedisi, cara bayar, kebijakan retur/garansi | Tidak* | Tulis `[isi ...]`; **jangan** mengarang |
| Nada brand: santai-akrab / ramah-sopan / formal | Tidak | Ramah-sopan, sapaan "Kak" |
| Nama admin/brand untuk tanda tangan | Tidak | `Admin [Nama Toko]` |
| Jam operasional admin/gudang | Tidak | `[isi jam kerja]`; janji waktu tindak lanjut harus jatuh di jam kerja |
| Solusi yang boleh ditawarkan (retur, tukar, refund, voucher, kirim ulang) | Tidak* | Tanyakan untuk komplain; jika tidak ada jawaban, tawarkan "cek dulu" tanpa menjanjikan |

\*Wajib bila jawabannya bergantung pada fakta toko (stok, ongkir, kebijakan). Jika kurang, tanyakan **sekali** (maks. 5 pertanyaan bernomor), atau buat balasan dengan `[isi ...]` bila pengguna ingin cepat.

## Langkah kerja
1. **Kenali jenis chat**: pertanyaan (FAQ), pesanan/transaksi, komplain, atau di luar topik/iseng. Perhatikan emosi pelanggan (netral, bingung, kesal, sangat marah).
2. **Pertanyaan/FAQ** → jawab langsung di kalimat pertama, lalu beri langkah berikutnya (cara order, link/etalase, konfirmasi). Contoh pola & bank jawaban: `templates/bank-jawaban.md`.
3. **Komplain** → pakai alur **E-S-T** (detail & contoh per kasus di `references/alur-komplain.md`):
   - **Empati**: akui perasaan & minta maaf atas ketidaknyamanan (tanpa menyalahkan pelanggan/kurir secara berlebihan).
   - **Solusi**: minta data minimum yang dibutuhkan (nomor pesanan, foto/video unboxing), jelaskan pilihan solusi yang **diizinkan pengguna** dan batas waktunya.
   - **Tindak lanjut**: kapan admin akan mengabari lagi (dalam jam operasional toko), lalu tepati. Tawarkan ringkasan tindakan untuk pengguna (apa yang harus dicek di gudang/ekspedisi).
4. **Sesuaikan nada brand** (lihat tabel di `references/nada-brand.md`) dan saluran:
   - WA: boleh 1–2 emoji, paragraf pendek, bisa lebih personal.
   - Marketplace: lebih ringkas; arahkan proses (retur/komplain/pengembalian dana) lewat fitur resmi platform; **jangan** mengajak transaksi atau pindah chat ke luar platform (umumnya dilarang aturan marketplace — cek Seller Center).
5. **Mode bank jawaban**: dari info toko, buat 15–30 template bernomor per kategori (sapaan, stok, harga & promo, ongkir & pengiriman, cara order, pembayaran, lacak paket, retur/tukar, komplain, di luar jam kerja, penutup). Beri judul pendek tiap template agar mudah dijadikan quick reply, dan batasi ≤ 500 karakter per template.
6. **Periksa** dengan checklist; tawarkan versi lain (lebih santai/formal, lebih pendek).

## Format output
**Mode balas satu chat:**
```
**Balasan (siap kirim):**
[teks balasan]

**Alternatif lebih singkat:**            ← opsional, untuk marketplace
[teks]

**Catatan untuk admin:**
- [yang perlu dicek/diisi sebelum kirim, mis. cek resi, konfirmasi stok]
- [tindak lanjut + kapan]
```

**Mode bank jawaban:**
```
## Bank Jawaban CS – [Nama Toko]
Nada: [..] · Sapaan: [..] · Tanda tangan: [..]

### 1. Sapaan & pembuka
**[1.1] Salam pertama** — "..."
**[1.2] Di luar jam kerja** — "..."
### 2. Stok & varian
...
(Bagian [isi ...] wajib diganti sebelum dipakai)
```

## Contoh
**Input pengguna:** "Toko hijab 'Kerudung Amanah' (Shopee). Pembeli chat: 'Min, pesen pashmina warna dusty pink yang dateng malah warna mocca!! Gimana nih, mau dipake kondangan Sabtu.' Kita bisa tukar, ongkir retur kita tanggung."

**Output:**
```
**Balasan (siap kirim):**
Halo Kak, mohon maaf banget ya, Kak, pesanan yang datang tidak sesuai warna. Pasti bikin khawatir apalagi mau dipakai kondangan Sabtu ini 🙏

Kami siap tukar ke dusty pink dan ongkir retur kami tanggung. Boleh bantu kirim foto pashmina yang diterima beserta label/plastiknya di chat ini, Kak? Setelah itu kami bantu ajukan penukaran lewat fitur pengembalian di Shopee.

Supaya keburu untuk Sabtu, dusty pink pengganti bisa kami kirim lebih dulu hari ini setelah fotonya kami cek. Kami kabari nomor resinya paling lambat pukul 17.00 ya, Kak.

**Catatan untuk admin:**
- Cek stok dusty pink sebelum menjanjikan kirim hari ini; jika kosong, ganti kalimat terakhir dengan pilihan warna lain atau pengembalian dana.
- "Kirim duluan sebelum barang retur diterima" adalah usulan: konfirmasi ke pemilik toko dulu.
- Cek proses pengembalian/penukaran yang berlaku di Seller Center Shopee.
- Catat penyebab salah kirim (salah ambil rak/label) untuk perbaikan packing.
```

## Checklist sebelum mengirim hasil
- [ ] Pertanyaan pelanggan terjawab di kalimat pertama/kedua.
- [ ] Tidak meminta pelanggan mengulang info yang sudah ia berikan di chat (nomor pesanan, alamat, foto).
- [ ] Komplain memakai urutan empati → solusi → tindak lanjut dengan waktu yang jelas.
- [ ] Tidak ada fakta karangan: stok, harga, ongkir, estimasi tiba, kebijakan retur, biaya admin → dari pengguna atau `[isi ...]`.
- [ ] Tidak menjanjikan solusi yang belum diizinkan pengguna (refund, voucher, kirim ulang) — tandai "usulan" di catatan admin.
- [ ] Tidak menyalahkan pelanggan, tidak defensif, tidak menyindir.
- [ ] Hanya meminta data yang perlu (nomor pesanan, foto/video); tidak meminta KTP, PIN, OTP, atau password.
- [ ] Marketplace: tidak mengajak transaksi/kontak di luar platform.
- [ ] Nada & sapaan konsisten dengan brand.

## Batasan & penanganan error
- Chat berisi ancaman, pelecehan, atau penipuan (mis. minta refund tanpa bukti berulang): balas tetap sopan & tegas, minta bukti sesuai prosedur, sarankan pengguna menyimpan bukti chat dan memakai fitur laporan platform.
- Klaim kesehatan/keamanan produk (alergi, iritasi, keracunan): tunjukkan kepedulian, sarankan pelanggan menghentikan pemakaian dan memeriksakan diri ke tenaga kesehatan, minta detail pesanan; jangan memberi diagnosis atau mengakui kesalahan hukum. Sarankan pemilik usaha menangani langsung.
- Jika tangkapan layar tidak terbaca atau konteks tidak jelas, tanyakan isi chatnya.
- Skill tidak terhubung ke sistem toko; status pesanan/resi harus dicek pengguna sendiri.
- Data pelanggan (nama, alamat, nomor) hanya dipakai untuk membalas chat tersebut dan tidak disimpan ke bank jawaban (UU PDP 27/2022).
