# 01 — Promo gajian toko roti, dengan file kontak CSV

## Skenario
S1 — permintaan normal dan lengkap. Pengguna memberi isi promo, nama toko, cara order, dan file kontak
CSV (40 baris fiktif, berisi kontak yang belum setuju, nomor dobel, nomor rusak, dan yang minta berhenti).
Script `siapkan_broadcast.py` dijalankan sungguhan di `/tmp/uji-broadcast-wa/`.

## Input pengguna
```
Tolong bikinin broadcast WA buat pelanggan toko roti saya, Roti Hangat Mbak Sri di Solo. Promo gajian
25-30 September: roti sobek cokelat 25rb jadi 20rb, terus roti manis beli 2 gratis 1. Order tinggal
bales chat, bisa diantar buat area Laweyan. Aku ada file pelanggan.csv, mulai kirim Jumat 25 Sept jam 10 pagi ya.
Yang udah bilang stop aku taruh di stop.txt.
```

## Output

## Broadcast WA — Promo Gajian Roti Hangat Mbak Sri (25–30 September)

### Variasi 1
```
Halo {sapaan} {nama} 👋
Ini dari Roti Hangat Mbak Sri, Solo. Karena {sapaan} pelanggan kami, ada kabar gajian nih: 25–30 September, Roti Sobek Cokelat cuma Rp 20.000 (biasanya Rp 25.000). Plus beli 2 roti manis gratis 1.
Mau dipesankan? Balas chat ini ya, area Laweyan bisa kami antar.
Tidak ingin menerima info promo lagi? Balas STOP.
```

### Variasi 2
```
Selamat gajian, {sapaan} {nama}! 🎉
Roti Hangat Mbak Sri lagi ada promo sampai 30 September: Roti Sobek Cokelat Rp 20.000 dari Rp 25.000, dan roti manis beli 2 gratis 1. Pas buat sarapan keluarga.
Balas "PESAN" + jumlahnya, nanti kami catat. Untuk area Laweyan bisa kami antar.
Kamu menerima pesan ini karena bersedia dikirimi info dari Roti Hangat Mbak Sri. Balas STOP untuk berhenti.
```

### Variasi 3
```
{sapaan} {nama}, stok roti buat minggu ini sudah aman? 🍞
Khusus 25–30 September di Roti Hangat Mbak Sri: Roti Sobek Cokelat Rp 20.000 (normal Rp 25.000) dan promo roti manis beli 2 gratis 1.
Cukup balas chat ini untuk pesan. Pengantaran tersedia untuk area Laweyan.
Balas BERHENTI kalau tidak mau dapat info lagi ya, {sapaan}.
```

**Versi untuk daftar siaran WhatsApp Business** (nama tidak terisi otomatis di daftar siaran):
```
Halo Kak 👋 Ini dari Roti Hangat Mbak Sri, Solo. Promo gajian 25–30 September: Roti Sobek Cokelat Rp 20.000 (biasanya Rp 25.000) dan roti manis beli 2 gratis 1. Balas chat ini untuk pesan, area Laweyan bisa kami antar.
Tidak ingin menerima info promo lagi? Balas STOP.
```

### Jadwal kirim yang disarankan
- Jumat, 25 September 2026, mulai 10.00 WIB, 20 pesan per batch, jeda ±1 menit antarpesan, 30 menit antarbatch.
- Hari Jumat: selesaikan sebelum ±11.30 dan jangan kirim selama jam salat Jumat (±11.30–13.00). Dengan 25 kontak, pengiriman selesai ±10.54, jadi aman.
- Pengingat kedua (opsional, hanya untuk yang belum membalas): Minggu 27 September ±16.00. Jangan lebih dari 1–2 kali per minggu.

### Hasil pengolahan kontak
Siap kirim: **25** dari 40 baris | Dilewati: **10** belum/tidak setuju, **2** minta berhenti (kolom Berhenti), **1** ada di stop.txt, **1** nomor tidak valid, **1** nomor duplikat
Sebaran variasi: V1 = 9, V2 = 8, V3 = 8 | Jadwal: 25 Sep 2026 10.00 → 10.54 WIB
File: `broadcast_siap.csv` (berisi jadwal, pesan yang sudah terisi nama, dan link wa.me per kontak. Buka link satu per satu, cek pesannya, lalu tekan kirim. **Simpan di komputer sendiri, jangan dibagikan.**)

Cara pakai file: buka di Excel/Google Sheets → urutkan menurut `jadwal_kirim` → klik `link_wa` → WhatsApp terbuka dengan pesan sudah terisi → tekan kirim.

### Sebelum kirim (UU PDP)
- [ ] Semua penerima sudah setuju menerima info promo (kolom Persetujuan = ya)
- [ ] Yang membalas STOP/BERHENTI dicatat di kolom Berhenti atau stop.txt dan tidak dikirimi lagi
- [ ] File kontak & `broadcast_siap.csv` disimpan aman, tidak dibagikan ke grup/orang lain
- [ ] Balas yang minta berhenti: "Baik Kak, nomor Kakak sudah kami hapus dari daftar info promo. Terima kasih."

📝 Asumsi: sapaan default "Kak" untuk nama tanpa Bu/Pak/Mbak/Mas; nama depan saja; zona WIB; pengantaran
Laweyan **tidak** disebut gratis karena tidak disebutkan. Mau versi lebih formal, bahasa Jawa halus, atau lebih pendek?

## Catatan penguji
- **Bagus:** setiap variasi punya `{sapaan} {nama}`, nama toko + alasan menerima pesan, angka persis dari
  pengguna (tidak ada "hemat 20%" hasil hitung sendiri), 1 CTA, dan teks berhenti. Panjang 334/384/326 karakter
  (dalam rentang 300–600). Emoji 1 per variasi.
- **Angka script diverifikasi independen** (python terpisah): 40 − 10 (tidak setuju/kosong) − 2 (kolom berhenti)
  − 1 (stop.txt) − 1 (nomor "0812-00") − 1 (duplikat "+62 812 0000 1000" = "0812-0000-1000") = **25**, dan daftar
  nomor yang lolos identik dengan hasil script. Jadwal 10.00–10.19 (batch 1, 20 pesan), 10.19 + 1 menit + 30 menit = 10.50 (batch 2) — benar.
- Normalisasi nomor benar: `0812-0000-1000`, `+62 812 0000 1000`, `(0812) ...`, `81200000004`, `+62 (0)812...` → `62812...`.
- Script hanya memakai `urllib.parse.quote` untuk membuat link; **tidak ada pengiriman pesan dan tidak ada akses jaringan**.
- **Kurang:** script tidak mengenal jam salat Jumat, padahal `references/aturan-pdp-wa.md` menyarankan menghindarinya.
  Di sini aman karena hanya 25 kontak; dengan 100 kontak mulai Jumat 10.00, pesan ke-41 dst. jatuh di 11.30–13.00.
  Agent harus mengingatkan sendiri.
- **Cacat yang ditemukan di uji data tepi (tidak muncul di contoh ini, lihat HASIL-UJI.md):** kolom Berhenti yang
  berisi "STOP" atau tanggal **tidak** dianggap berhenti, dan nomor yang punya baris "berhenti" tetap dikirimi bila ada baris duplikat tanpa tanda berhenti.
