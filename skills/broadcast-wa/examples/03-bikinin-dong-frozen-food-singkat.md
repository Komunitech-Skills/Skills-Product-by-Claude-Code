# 03 — "bikinin dong" broadcast frozen food (permintaan singkat/malas)

## Skenario
S3 — pengguna mengetik singkat dan santai. Info wajib (isi promo, nama toko, cara order) sebenarnya sudah ada,
jadi skill harus langsung mengerjakan dengan default dan menyebut asumsi, bukan bertanya.

## Input pengguna
```
bikinin dong pesen wa buat pelanggan frozen mama nisa, nugget ayam 1kg diskon jd 55rb sampe minggu. order bales chat aja
```

## Output

## Broadcast WA — Promo Nugget Ayam 1 kg Frozen Mama Nisa

### Variasi 1
```
Halo {sapaan} {nama} 👋
Frozen Mama Nisa di sini. Buat pelanggan setia kami, Nugget Ayam 1 kg lagi diskon jadi Rp 55.000, berlaku sampai hari Minggu.
Mau dipisahkan satu? Balas chat ini aja ya.
Tidak ingin menerima info promo lagi? Balas STOP.
```

### Variasi 2
```
{sapaan} {nama}, stok lauk anak di freezer masih ada? 🍗
Minggu ini Nugget Ayam 1 kg di Frozen Mama Nisa cuma Rp 55.000, sampai hari Minggu saja.
Tinggal balas "NUGGET" + jumlahnya, nanti kami siapkan.
Pesan ini dikirim karena {sapaan} pelanggan Frozen Mama Nisa. Balas STOP untuk berhenti.
```

### Variasi 3
```
Selamat pagi {sapaan} {nama}!
Info singkat dari Frozen Mama Nisa: Nugget Ayam kemasan 1 kg sedang diskon, jadi Rp 55.000 sampai Minggu ini.
Pesan cukup lewat balas chat ini ya.
Balas BERHENTI kalau tidak mau dapat info promo lagi.
```

### Jadwal kirim yang disarankan
- Kamis 24 atau Jumat 25 September 2026, **±09.00–11.00 WIB** (ibu rumah tangga biasanya pegang HP setelah urusan pagi),
  bertahap 20 pesan per batch, jeda ±1 menit antarpesan, 30 menit antarbatch. Jumat: hindari ±11.30–13.00.
- Tidak perlu pengingat kedua kecuali banyak yang bertanya; maksimal 1–2 promo per minggu per kontak.

### Hasil pengolahan kontak
Belum ada file kontak. Kalau punya daftar pelanggan (Nama, Nomor, Persetujuan), kirim file CSV-nya, nanti saya buatkan
daftar kirim + link WA per kontak.

### Sebelum kirim (UU PDP)
- [ ] Hanya kirim ke pelanggan yang sudah setuju dikirimi info promo
- [ ] Yang balas STOP/BERHENTI dicatat dan tidak dikirimi lagi
- [ ] Daftar nomor pelanggan disimpan aman, tidak dibagikan

📝 Asumsi: "sampai Minggu" = Minggu 27 September 2026 (tanggal tidak ditulis di pesan supaya tidak salah — sebutkan
tanggalnya kalau mau dicantumkan); harga normal tidak disebut karena tidak diberikan (jadi tidak ada "hemat X%");
target pelanggan ibu rumah tangga; sapaan default "Kak". Mau versi lebih pendek untuk WA Status?

## Catatan penguji
- **Bagus:** tidak bertanya ulang karena info wajib sudah lengkap; asumsi disebut di akhir. Tidak ada angka hasil
  hitungan sendiri — harga normal tidak ada, sehingga tidak menulis "hemat …" (sesuai langkah 2).
  Tiga variasi berbeda pembuka, susunan, dan CTA ("balas chat", "balas NUGGET", "balas chat ini").
- Teks berhenti ada di tiap variasi; emoji ≤ 1 per variasi.
- **Kurang (ringan):** Variasi 2 menebak target "lauk anak" dari asumsi — wajar, sudah disebut di asumsi, tetapi
  SKILL.md tidak mengatur boleh/tidaknya menambah sudut pandang pembeli yang tidak diberikan.
- **Uji ulang v1.0.2:** kalimat alasan menerima pesan diganti dari "Kamu menerima …" ke "Pesan ini dikirim karena {sapaan} …" agar
  satu sapaan per pesan (aturan baru SKILL.md langkah 2). Semua teks berhenti lolos cek instruksi tindakan v1.0.2.
