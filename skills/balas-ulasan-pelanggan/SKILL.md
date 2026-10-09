---
name: balas-ulasan-pelanggan
description: Menulis balasan publik untuk ulasan pelanggan di Shopee, Tokopedia, TikTok Shop, dan Google Maps (positif, netral, negatif) yang tenang, tidak defensif, tidak membocorkan data pembeli, dan mengarahkan keluhan ke chat pribadi — plus pesan chat pribadinya dan cek otomatis. Gunakan saat pengguna minta balas ulasan/review, bintang 1, komplain di kolom ulasan, atau rating jelek (reply to review, respond to negative review, Google review reply). Bukan untuk membalas chat pribadi pelanggan (pakai balas-chat-cs).
---

# Balas Ulasan Pelanggan

> **Aturan kerja:** Jangan menginstal paket/aplikasi (mis. `pip install`) — bila perlu, tunjukkan caranya dan biarkan pengguna yang memasang; jangan membuka atau mencari file selain yang diberikan pengguna, isi folder skill ini, dan file yang disebut di langkah kerja; jangan menulis file baru tanpa menyebut lokasinya, dan simpan hasil di folder kerja yang disepakati (bukan /tmp).

## Tujuan
Mengubah ulasan — terutama bintang 1–2 — menjadi kesempatan menunjukkan ke calon pembeli bahwa toko
bertanggung jawab, tanpa emosi, tanpa membocorkan data, dan dengan penyelesaian yang dipindah ke chat pribadi.

## Kapan digunakan
- "Bantu balas ulasan bintang 1 ini: <tempel ulasan>"
- Membalas banyak ulasan sekaligus (positif, netral, negatif) di marketplace atau Google Maps
- Menyusun template balasan toko agar admin konsisten

## Kapan TIDAK digunakan
- Membalas chat/DM pribadi pembeli → `balas-chat-cs` (skill ini hanya menyertakan pesan pembuka eskalasi)
- Membuat judul/deskripsi produk → `listing-marketplace`
- Tuduhan hukum serius (keracunan, penipuan, ancaman tuntutan): tetap bantu balasan singkat yang aman,
  tapi sarankan pemilik berkonsultasi dengan pengacara sebelum memposting

## Input
| Info | Wajib? | Default jika tidak diberikan |
|---|---|---|
| Teks ulasan (+ bintang bila ada) | Ya | — (minta ditempel) |
| Platform | Tidak | Ditebak dari konteks; jika tidak jelas, anggap marketplace (aturan paling ketat) |
| Nama toko/usaha & nama penanda tangan | Tidak | Tanpa tanda tangan |
| Fakta dari sisi toko (mis. sudah dikirim ulang, stok habis, kebijakan retur) | Tidak | Tidak diasumsikan; solusi ditulis umum |
| Solusi yang disetujui pemilik (ganti, refund, voucher) | Tidak | Tidak dijanjikan; ditulis "kami bantu penyelesaiannya" |
| Gaya bahasa | Tidak | Sopan-hangat, sapaan "Kak" (Google Maps: "Kak"/"Bapak/Ibu" sesuai nada ulasan) |

Jika ulasan belum ditempel, minta **sekali** bersama pertanyaan lain yang perlu (maks. 5, bernomor).
Jika pengguna ingin cepat, tulis balasan dengan asumsi aman dan sebutkan asumsinya.

## Langkah kerja
1. **Baca `references/pola-balasan.md`.** Tentukan jenis (positif 4–5★, netral 3★ atau campuran,
   negatif 1–2★ atau keluhan) dan jenis masalah (rusak, salah kirim, telat, rasa, pelayanan, harga,
   diduga palsu, kasar, tuduhan serius). Jika bintang dan isi bertentangan, ikuti isinya.
2. **Tulis balasan publik** sesuai kerangka jenisnya:
   - Positif: terima kasih + sebut hal spesifik + ajakan kembali.
   - Netral: terima kasih + akui masukan + tindak lanjut/tips.
   - Negatif: terima kasih/akui → maaf atas pengalaman → langkah singkat tanpa menyalahkan → ajak ke
     chat pribadi → penutup. Jangan membantah fakta di depan umum; klarifikasi seperlunya dengan netral.
   Sebut hanya detail yang ditulis pengulas sendiri. Jangan tulis nomor pesanan/resi, alamat, nomor HP,
   isi chat. Jangan menawarkan imbalan untuk ubah/hapus ulasan. Jangan menjanjikan kompensasi yang
   belum disetujui pemilik. **Klaim tindakan yang belum dikonfirmasi pemilik** ("sudah kami bahas bersama tim", "sudah kami tegur", "sudah kami perbaiki", "sudah kami kirim ulang") **dilarang** ditulis sebagai fakta; jadikan isian `[konfirmasi pemilik: sudah dibahas bersama tim?]` atau beri dua pilihan kalimat (versi bila sudah / versi netral "masukan Kakak kami catat dan teruskan") dan tanyakan ke pemilik. Tanpa konfirmasi, pakai versi netral.
   **Khusus fasilitas/layanan kesehatan** (klinik, praktik dokter/dokter gigi, bidan, apotek, laboratorium,
   RS, fisioterapi, psikolog) — **PERLU REVIEW** tenaga medis/kepatuhan sebelum dipakai sebagai aturan final:
   - Jangan menyebut atau mengonfirmasi bahwa pengulas/keluarganya **pasien**, kapan berkunjung, atau
     **tindakan, kondisi, keluhan, obat, hasil** apa pun — walaupun pengulas sendiri menulisnya
     (❌ "saat periksa gigi putra/putri Bapak", ❌ "saat berkunjung ke klinik kami", "saat datang/berobat" — semuanya membenarkan kunjungan; ✅ "mohon maaf bila pengalaman di klinik kami tidak sesuai harapan").
   - Boleh menanggapi hal operasional secara umum (waktu tunggu, keramahan, kejelasan informasi) tanpa
     merinci kunjungan pengulas, lalu alihkan ke **kanal pribadi** (nomor/email resmi di profil, atau chat).
   - Dasar: kewajiban menjaga rahasia kesehatan pasien (UU 17/2023 tentang Kesehatan Pasal 301; PP 28/2024
     Pasal 788–789 juga berlaku untuk staf admin) dan data kesehatan termasuk data pribadi bersifat spesifik
     (UU 27/2022 tentang PDP Pasal 4 ayat (2) huruf a). Bukan nasihat hukum.
   - Jalankan script dengan `--faskes`.
3. **Untuk ulasan negatif/netral dengan masalah**, tulis juga **pesan chat pribadi** (eskalasi) yang boleh
   meminta bukti & nomor pesanan secara pribadi.
4. **Cek otomatis** setiap balasan publik. Script ada di subfolder `scripts/` di folder yang sama dengan
   SKILL.md ini (folder skill); jangan mencarinya ke seluruh disk (`find /`). Windows: `python`/`py`.
   ```bash
   python3 <folder-skill-ini>/scripts/cek_balasan.py --platform shopee --jenis negatif --teks "<balasan>"
   # klinik/faskes: tambahkan --faskes
   ```
   Platform: `shopee`, `tokopedia`, `tiktok`, `google`, `lainnya`. Perbaiki semua **GAGAL** (data pribadi,
   ajakan keluar platform di marketplace, permintaan ubah ulasan, terlalu panjang); tinjau **CEK** & **SARAN**.
   Status **PERLU DICEK (privasi)** berarti ada kemungkinan nama lengkap pembeli (sapaan + 2 kata kapital),
   kutipan isi chat pribadi ("Kakak bilang '...'"), atau nama jalan — hapus kecuali itu memang nama toko/
   alamat usaha sendiri atau kalimat yang ditulis pengulas di ulasannya.
   **Jika Python tidak bisa dijalankan:** periksa manual dengan checklist di bawah dan hitung panjang teks;
   beri tahu pengguna bahwa pengecekan dilakukan manual.
5. Berikan 1 balasan utama + 1 alternatif (lebih singkat atau lebih formal), lalu tawarkan revisi.
   Untuk 3 ulasan atau lebih sekaligus, alternatif boleh dilewati agar hasil tetap ringkas.

## Format output
```
## Balasan ulasan — <platform>, <★ bila ada> (<positif/netral/negatif>: <jenis masalah>)

### Balasan publik (utama) — <panjang> karakter
<teks siap tempel>

### Alternatif (lebih singkat/formal)
<teks>

### Pesan chat pribadi (jika perlu eskalasi)
<teks>

### Hasil cek
<ringkasan script atau "dicek manual">

📝 Catatan untuk pemilik: <hal yang perlu diputuskan, mis. setuju ganti barang?; saran lapor ulasan bila melanggar>
```
Untuk banyak ulasan sekaligus: ulangi blok per ulasan, beri nomor, dan jangan memakai kalimat pembuka
yang sama persis untuk semua.

## Contoh
**Input pengguna:** "Balasin ulasan Shopee bintang 1 ini, toko saya Dapur Bu Ratmi: 'Paket nyampe 6 hari,
botol sambalnya bocor, kardus basah semua. Kecewa, gak lagi-lagi.' Kami mau ganti botol baru kalau ada
video unboxing."

**Output:**
```
### Balasan publik (utama) — 316 karakter
Kak, terima kasih sudah memberi tahu, dan mohon maaf paketnya lama sampai dan botol sambalnya bocor.
Kami paham ini mengecewakan. Kami sudah menghubungi Kakak lewat chat toko untuk membantu penggantian
botol baru — mohon dicek ya Kak. Masukan ini juga kami pakai untuk memperkuat kemasan pengiriman.
— Dapur Bu Ratmi

### Alternatif (lebih singkat)
Mohon maaf atas pengiriman yang lama dan botol yang bocor, Kak. Kami sudah kirim pesan lewat chat toko
untuk membantu penggantiannya. Terima kasih masukannya.

### Pesan chat pribadi
Halo Kak, ini Rina dari Dapur Bu Ratmi. Kami sudah membaca ulasan Kakak dan mohon maaf botolnya sampai
bocor. Boleh kirimkan video unboxing atau foto kondisi paket saat diterima? Setelah kami cek, kami kirim
botol pengganti ya Kak. Terima kasih sudah sabar.

### Hasil cek
Lulus (shopee, negatif): tidak ada data pribadi, tidak ada ajakan keluar platform.
📝 Catatan untuk pemilik: kirim pesan chat pribadi dulu, baru posting balasan publik (karena balasan menyebut "sudah menghubungi"). Jangan menjanjikan pengganti dengan syarat ulasan diubah. "Rina" = contoh nama admin.
```

**Contoh Google Maps (ringkas):** ulasan 2★ "Bakso enak tapi nunggu 40 menit, pelayannya jutek" untuk
Bakso Pak Kumis Bekasi → balasan: terima kasih atas pujian baksonya, maaf atas waktu tunggu & sikap tim,
"sudah kami bahas bersama tim" (hanya jika pemilik memang melakukannya), undangan menghubungi nomor
resmi yang tercantum di profil usaha.

## Checklist sebelum mengirim hasil
- [ ] Tidak ada nomor pesanan/invoice/resi, alamat, nomor HP/email pembeli, atau isi chat pribadi
- [ ] Tidak defensif: tidak membantah, tidak menyalahkan pembeli/kurir di depan umum
- [ ] Tidak meminta ubah/hapus ulasan dan tidak menawarkan imbalan untuk itu
- [ ] Ulasan negatif: ada maaf + arahan ke chat pribadi (marketplace: fitur chat toko, bukan WA)
- [ ] Janji/kompensasi hanya yang disetujui pemilik; fakta toko tidak dikarang
- [ ] Spesifik terhadap isi ulasan; panjang dalam batas aman (cek batas terbaru)
- [ ] Faskes/klinik: tidak menyebut/mengonfirmasi status pasien, kunjungan, tindakan, atau kondisi; dialihkan ke kanal pribadi; script dengan `--faskes` lulus
- [ ] Hasil cek script dilaporkan (atau "dicek manual")

## Batasan & penanganan error
- Skill tidak memposting balasan dan tidak membaca ulasan langsung dari platform; pengguna menempelkannya.
- Batas panjang balasan per platform tidak dipastikan; skill memakai batas aman dan meminta pengguna cek.
- Ulasan berisi ujaran kebencian, SARA, atau data pribadi orang lain: sarankan fitur "laporkan ulasan"
  di platform; balasan (jika tetap dibuat) singkat dan netral.
- Ringkasan aturan (UU PDP, kebijakan ulasan) bukan nasihat hukum; untuk tuduhan serius atau ancaman
  tuntutan, arahkan ke pengacara.
- Script error (platform tidak dikenal, teks kosong, file tidak ada) → pesan bahasa Indonesia; perbaiki argumen atau cek manual.
