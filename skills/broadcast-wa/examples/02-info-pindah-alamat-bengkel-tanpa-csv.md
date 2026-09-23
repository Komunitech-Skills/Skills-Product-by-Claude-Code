# 02 — Info pindah alamat bengkel (tanpa file kontak, nada lebih formal)

## Skenario
S2 — permintaan normal, bukan promo diskon melainkan info penting (pindah alamat) + promo kecil pembukaan.
Pengguna tidak punya file CSV dan ingin kirim lewat daftar siaran WhatsApp Business. Nada diminta sopan-formal.

## Input pengguna
```
Mau kabarin pelanggan bengkel saya kalau mulai 1 Oktober Bengkel Motor Maju Jaya pindah dari Jl. Melati ke
Jl. Kenanga No. 12 Bekasi Timur (sebelah minimarket). Minggu pertama buka, ganti oli gratis cek rem.
Bahasanya yang sopan ya, pelanggan saya banyak bapak-bapak. Saya kirim lewat broadcast list WA Business aja.
```

## Output

## Broadcast WA — Info Pindah Alamat Bengkel Motor Maju Jaya

Karena dikirim lewat **daftar siaran WhatsApp Business**, `{nama}` tidak bisa terisi otomatis. Di bawah ini
versi utama **tanpa placeholder** (siap tempel), lalu versi personal `{sapaan} {nama}` bila nanti ingin
mengirim per kontak.

### Variasi 1 (tanpa placeholder — untuk daftar siaran)
```
Selamat pagi Bapak/Ibu,
Kami dari Bengkel Motor Maju Jaya ingin memberi kabar: mulai 1 Oktober 2026 bengkel kami pindah ke Jl. Kenanga No. 12, Bekasi Timur (sebelah minimarket).
Selama minggu pertama di tempat baru, setiap ganti oli gratis cek rem.
Terima kasih sudah menjadi pelanggan kami. Silakan balas pesan ini bila ingin menanyakan arah atau booking servis.
Tidak ingin menerima info dari kami lagi? Balas STOP.
```

### Variasi 2 (tanpa placeholder — untuk daftar siaran)
```
Bapak/Ibu pelanggan Bengkel Motor Maju Jaya yang kami hormati,
Per 1 Oktober 2026 kami tidak lagi di Jl. Melati. Alamat baru kami: Jl. Kenanga No. 12, Bekasi Timur, persis di sebelah minimarket 🔧
Sebagai ucapan terima kasih, minggu pertama di alamat baru: ganti oli, cek rem gratis.
Mau booking jam servis? Cukup balas pesan ini.
Balas BERHENTI bila tidak ingin menerima info lagi.
```

### Variasi 3 (versi personal — hanya bila dikirim per kontak dengan file CSV)
```
Selamat siang {sapaan} {nama},
Ini dari Bengkel Motor Maju Jaya. Kami mengabarkan bahwa mulai 1 Oktober 2026 bengkel pindah ke Jl. Kenanga No. 12, Bekasi Timur (sebelah minimarket).
Minggu pertama di tempat baru, ganti oli sudah termasuk cek rem gratis.
Silakan balas pesan ini untuk menanyakan arah atau membuat jadwal servis.
Pesan ini dikirim karena {sapaan} terdaftar sebagai pelanggan Bengkel Motor Maju Jaya. Balas STOP untuk berhenti.
```

### Jadwal kirim yang disarankan
- **Senin 28 September 2026, 09.00–11.00 WIB** (3 hari sebelum pindah, supaya pelanggan tidak datang ke alamat lama),
  lalu **pengingat singkat Kamis 1 Oktober ±16.00** hanya jika perlu.
- Daftar siaran: pesan hanya sampai ke kontak yang **menyimpan nomor bengkel**. Jumlah kontak per daftar
  siaran dibatasi (lama dikenal 256 — cek ketentuan terbaru). Bila pelanggan banyak, bagi menjadi beberapa daftar dan
  kirim bertahap dengan jeda ±30 menit.
- Hindari jam salat Jumat (±11.30–13.00) dan malam di atas ±20.30.

### Hasil pengolahan kontak
Tidak ada file kontak, jadi tidak ada daftar kirim. Jika nanti ingin kirim per kontak dengan nama, siapkan
spreadsheet `Nama | Nomor | Persetujuan (ya/tidak) | Berhenti`, simpan sebagai CSV UTF-8, lalu minta saya mengolahnya.

### Sebelum kirim (UU PDP)
- [ ] Anggota daftar siaran adalah pelanggan yang memang bersedia dihubungi bengkel (info servis/promo)
- [ ] Yang membalas STOP/BERHENTI dikeluarkan dari daftar siaran
- [ ] Tidak memasukkan nomor dari grup WA atau nomor yang hanya pernah bertanya harga

Belum punya catatan persetujuan? Saat pelanggan servis, tanyakan: "Boleh kami kirimi info servis & promo lewat WA
sesekali, Pak? Bisa berhenti kapan saja." Catat "ya" + tanggal.

📝 Asumsi: tahun 2026; sapaan "Bapak/Ibu"; "gratis cek rem" hanya untuk ganti oli selama minggu pertama
(1–7 Oktober) — mohon pastikan rentang tanggal promonya agar bisa ditulis jelas. Mau versi lebih singkat untuk WA Status?

## Catatan penguji
- **Bagus:** agent mengikuti catatan di SKILL.md bahwa `{nama}` tidak terisi di daftar siaran dan memberi versi
  tanpa placeholder sebagai versi utama. Semua variasi punya teks berhenti. Alamat & promo persis dari pengguna.
  Saran jadwal masuk akal (sebelum tanggal pindah) dan batas daftar siaran diberi label "cek ketentuan terbaru".
- Pengguna menulis "minggu pertama" tanpa tanggal; agent tidak mengarang tanggal akhir promo di dalam pesan, hanya
  menyebut asumsinya dan meminta konfirmasi — sesuai aturan "tidak mengarang".
- **Uji ulang v1.0.1:** kontradiksi lama (langkah 2 mewajibkan `{sapaan} {nama}` di setiap variasi) sudah diperbaiki —
  SKILL.md langkah 2 kini menulis "kecuali versi khusus daftar siaran WhatsApp Business". Output di atas tetap sesuai.
  Variasi 1–2 tidak memuat "alasan menerima pesan" secara eksplisit selain "pelanggan kami"; masih wajar.
- Pesan info (bukan promo murni) tetap diberi opt-out — sesuai referensi.
- **Uji ulang v1.0.2:** kalimat alasan menerima pesan diganti dari "Kamu menerima …" ke "Pesan ini dikirim karena {sapaan} …" agar
  satu sapaan per pesan (aturan baru SKILL.md langkah 2). Semua teks berhenti lolos cek instruksi tindakan v1.0.2.
