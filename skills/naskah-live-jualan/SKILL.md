---
name: naskah-live-jualan
description: Membuat naskah live selling siap baca untuk TikTok Live, Shopee Live, atau live IG/FB — rundown per segmen waktu (pembukaan, hook, demo, harga & promo, urgensi jujur, CTA checkout, rekap penonton baru, penutup) plus bank jawaban pertanyaan penonton, dengan angka promo dihitung script. Gunakan saat pengguna minta naskah/script live, rundown live, atau kata-kata host saat jualan live (live selling script, livestream shopping, live commerce). Bukan untuk caption posting atau deskripsi produk marketplace.
---

# Naskah Live Jualan

> **Aturan kerja:** Jangan menginstal paket/aplikasi (mis. `pip install`) — bila perlu, tunjukkan caranya dan biarkan pengguna yang memasang; jangan membuka atau mencari file selain yang diberikan pengguna, isi folder skill ini, dan file yang disebut di langkah kerja; jangan menulis file baru tanpa menyebut lokasinya, dan simpan hasil di folder kerja yang disepakati (bukan /tmp).

## Tujuan
Memberi host (pemilik toko, admin, atau host sewaan) naskah live yang runtut per menit, sehingga semua
produk kebagian waktu, penonton baru selalu tahu promonya, pertanyaan dijawab cepat, dan tidak ada klaim
atau urgensi palsu.

## Kapan digunakan
- "Buatin script live TikTok 1 jam buat jualan hijab"
- Menyiapkan rundown Shopee Live saat tanggal kembar/payday, atau melatih host baru
- Menyiapkan jawaban cepat untuk pertanyaan penonton yang sering muncul

## Kapan TIDAK digunakan
- Caption posting/video pendek → `caption-sosmed-umkm`; judul & deskripsi produk → `listing-marketplace`
- Rencana konten sebulan → `kalender-konten-30hari`; menentukan harga jual & margin → `harga-jual-marketplace`
- Membalas chat pembeli setelah live → `balas-chat-cs`

## Input
| Info | Wajib? | Default jika tidak diberikan |
|---|---|---|
| Produk yang dijual (nama + keunggulan/spesifikasi utama) | Ya | — (tanyakan) |
| Harga normal & harga/promo live per produk | Ya | — (tanyakan; tanpa promo pun boleh) |
| Platform | Tidak | TikTok Live |
| Durasi & jam mulai | Tidak | 60 menit, jam mulai tidak ditulis |
| Nama toko & nama host | Tidak | `[nama toko]`, `[nama host]` |
| Stok/kuota promo yang nyata, bonus, voucher | Tidak | Tidak disebut; ditulis `[stok nyata]` bila perlu |
| Info toko: kota kirim, jadwal kirim, COD, retur, izin/sertifikat | Tidak | `[isi: ...]` — tidak dikarang |
| Gaya bahasa host | Tidak | Santai-sopan, sapaan "Kak" |

Jika info wajib kurang, tanyakan **sekali** (maks. 5 pertanyaan bernomor). Jika pengguna ingin cepat,
pakai default dan sebutkan asumsinya di akhir.

## Langkah kerja
1. **Baca `references/etika-promo.md`.** Urgensi hanya boleh dari fakta nyata (stok di sistem, batas
   waktu voucher yang benar). Tolak kelangkaan palsu dan tawarkan versi jujurnya.
2. **Hitung semua angka promo** per produk (path relatif terhadap folder SKILL.md ini; Windows: `python`/`py`):
   ```bash
   python3 <folder-skill-ini>/scripts/hitung_promo.py --nama "Hijab Voal" --harga-normal "Rp 89.000" \
     --harga-live "Rp 69.000" --bundling "3=Rp 189.000"
   ```
   Atau `--diskon-persen 10 --bulatkan 1000` bila promo berupa persen. Produk tanpa promo tidak perlu
   script: sebut harga normalnya saja. Pakai `kalimat_live` dan
   `persen_hemat_boleh_diucapkan` dari output. Script menolak harga live ≥ harga normal dan memberi
   peringatan untuk diskon ≥ 50% dan bundling yang per pcs-nya tidak lebih murah dari harga live
   (paket seperti itu hanya boleh disebut hemat dibanding harga normal) — sampaikan ke pengguna.
3. **Susun rundown**:
   ```bash
   python3 <folder-skill-ini>/scripts/susun_segmen.py --durasi 60 --produk "Hijab Voal,Pashmina Kaos" --mulai 19:00
   ```
   Urutkan produk dari yang paling diandalkan. Script otomatis memakai pola ringkas bila waktu sempit,
   menyisipkan rekap 1 menit kira-kira tiap 15 menit (bisa di tengah blok produk, tidak di antara Hook
   dan Demo) selama waktunya muat, dan menolak durasi yang terlalu pendek. Jika produk sedikit sehingga
   satu produk muncul beberapa putaran, beri sudut bahasan berbeda tiap putaran (cara pakai, ukuran,
   perbandingan varian, jawab komentar).
4. **Tulis naskah per segmen** mengikuti rundown: kalimat siap ucap (bukan poin), dengan arahan aksi
   dalam kurung siku, mis. `[angkat produk ke kamera]`, `[pin produk no. 1]`, `[baca komentar]`.
   - Hook: pertanyaan/masalah pembeli dalam 1–2 kalimat. Demo: tunjukkan bukti (tekstur, ukuran, dipakai).
   - Harga: sebut harga normal → harga live → hemat (dari script). CTA: langkah checkout yang konkret
     ("klik keranjang kuning, pilih nomor 1, pilih warna, checkout").
   - Rekap: 2–3 kalimat untuk penonton yang baru masuk. Tanya-jawab: ambil dari bank jawaban.
5. **Lampirkan bank jawaban** 6–10 pertanyaan paling relevan dari `references/bank-jawaban.md`,
   diisi data pengguna.
6. **Jika Python tidak bisa dijalankan:** hitung manual dan tulis rumusnya:
   potongan = normal − live; persen = potongan ÷ normal × 100, **dibulatkan ke bawah**; harga dari diskon
   persen = normal × (100 − persen) ÷ 100, **dibulatkan ke atas** ke kelipatan yang dipilih; harga per pcs
   bundling = harga paket ÷ isi, **dibulatkan ke atas**. Rundown manual: pembukaan 3, per produk 11 menit
   (Hook 1, Demo 4, Harga 2, CTA 2, Tanya-jawab 2), rekap 1 menit tiap ±15 menit, penutup 3.
   Beri tahu pengguna bahwa hitungan dilakukan manual.
7. Periksa dengan checklist, lalu tawarkan revisi (lebih santai, bahasa daerah, durasi lain).

## Format output
```
## Naskah Live <platform> — <nama toko>, <durasi> menit (<jam mulai>)

### Rundown
| Waktu | Segmen | Produk |
|---|---|---|

### Angka promo (dihitung script)
| Produk | Normal | Harga live | Hemat | Bundling |
|---|---|---|---|---|

### Naskah
**[19:00–19:03] Pembukaan**
"..." [arahan aksi]
...

### Jawaban cepat pertanyaan penonton
| Pertanyaan | Jawaban |
|---|---|

### Catatan untuk host
- Angka `[stok nyata]` dibaca dari layar, jangan dikarang.
- Hal yang perlu dilengkapi: <[isi: ...]>
- Asumsi: <...>
```

## Contoh
**Input pengguna:** "Bikinin script TikTok Live 1 jam, mulai jam 7 malam, toko Nura Hijab dari Bandung.
Produk: Hijab Voal normal 89 ribu, live 69 ribu, paket 3 jadi 189 ribu. Pashmina Kaos 65 ribu diskon
10%. Inner Ninja 25 ribu, gak ada promo. Kirim tiap hari dari Bandung, bisa COD."

**Output (cuplikan):**
```
### Angka promo (dihitung script)
| Produk | Normal | Harga live | Hemat | Bundling |
|---|---|---|---|---|
| Hijab Voal | Rp 89.000 | Rp 69.000 | Rp 20.000 (22%) | Isi 3 Rp 189.000 → Rp 63.000/pcs |
| Pashmina Kaos | Rp 65.000 | Rp 59.000 (10%, dibulatkan ke atas ke Rp 1.000) | Rp 6.000 (9%) | – |
| Inner Ninja | Rp 25.000 | – | – | – |

**[19:00–19:03] Pembukaan**
"Halo Kak, selamat malam! Selamat datang di live Nura Hijab dari Bandung. Yang baru masuk, tap love dulu
biar nggak ketinggalan ya. Malam ini Hijab Voal cuma Rp 69.000 khusus selama live, dan ada paket isi 3
yang jatuhnya Rp 63.000 per pcs." [sapa 3 nama pertama di komentar]

**[19:08–19:10] Harga & promo — Hijab Voal**
"Harga normalnya Rp 89.000, khusus live jadi Rp 69.000, hemat Rp 20.000. Mau lebih hemat? Ambil paket
isi 3, Rp 189.000 saja, jadi cuma Rp 63.000 per pcs. Stok harga live yang ada di keranjang sekarang
[stok nyata] ya Kak, angkanya kelihatan di layar." [pin produk no. 1]

**[19:10–19:12] CTA — Hijab Voal**
"Caranya gampang: klik keranjang kuning, pilih nomor 1, pilih warna, lalu checkout.
Mau COD bisa, pilih saat checkout. Semua pesanan dikirim tiap hari dari Bandung."
```
Catatan asumsi: host `[nama host]`; stok & voucher tidak disebut karena tidak diberikan.

## Checklist sebelum mengirim hasil
- [ ] Semua angka harga/potongan/persen/per pcs berasal dari script (atau hitung manual tertulis)
- [ ] Tidak ada kelangkaan palsu: stok/kuota hanya `[stok nyata]` atau angka dari pengguna
- [ ] Harga normal adalah harga jual yang benar-benar berlaku sebelumnya (tanya bila ragu), bukan harga yang dinaikkan untuk dicoret
- [ ] Tidak ada klaim yang tidak diberikan pengguna (halal, BPOM, original, terlaris, klaim kesehatan)
- [ ] Setiap produk punya hook, demo, harga, CTA; ada rekap untuk penonton baru
- [ ] CTA mengarah ke keranjang/checkout di aplikasi, bukan ke WA atau transfer di luar platform
- [ ] Naskah berupa kalimat siap ucap, dengan arahan aksi dalam kurung siku

## Batasan & penanganan error
- Fitur live (voucher live, pin produk, posisi keranjang) berbeda per platform dan sering berubah;
  arahan aksi bersifat umum — minta host menyesuaikan dengan tampilan aplikasinya.
- Skill tidak menentukan harga jual atau margin. Jika harga live terlihat di bawah modal, sarankan cek
  dengan `hitung-hpp` / `harga-jual-marketplace`.
- Script menolak input tidak masuk akal (harga live ≥ normal, diskon ≥ 100%, durasi terlalu pendek)
  dengan pesan bahasa Indonesia. Sampaikan ke pengguna dan minta angka yang benar.
- Produk terlarang atau klaim medis → jangan dibuatkan naskah promosinya.
