# Contoh 01 - Sambutan pelanggan baru (toko kue)

> Contoh keluaran yang disusun pembuat dari kerangka skill (jadwal dari `scripts/jadwal_rangkaian.py`). Belum diuji penguji independen; nama dan produk fiktif.

**Pengguna:** "Toko kue saya, Kue Bu Rina, mau bikin pesan sambutan buat pelanggan baru. Pelanggan pertama beli hari Rabu 7 Oktober."

**Balasan:**

### Rangkaian sambutan (4 pesan, WA)
| Pesan | Tanggal kirim | Tujuan |
|---|---|---|
| 1 | Rabu, 7 Oktober 2026 | Terima kasih + kabar pesanan |
| 2 | Sabtu, 10 Oktober 2026 | Tips menyimpan kue |
| 3 | Sabtu, 17 Oktober 2026 | Tanya kabar, buka pintu untuk kendala |
| 4 | Rabu, 28 Oktober 2026 | Kenalkan menu lain (hanya bila Anda mau) |

### Teks pesan (siap salin)
**Pesan 1**
Halo Kak [nama], terima kasih sudah pesan [nama kue] di Kue Bu Rina. Pesanan Kakak [sedang kami siapkan / akan diantar tanggal `[isian]`]. Kalau ada yang mau diubah atau ditanyakan, balas saja chat ini. Salam, Rina. Kalau tidak ingin dapat pesan seperti ini lagi, balas "stop" ya.

**Pesan 2**
Halo Kak [nama], semoga [nama kue] sudah sampai dengan baik. Satu tips: [cara simpan yang berlaku untuk kue ini, mis. suhu ruang/kulkas dan batas hari]. Kalau ada kendala, kabari kami ya. Kalau tidak ingin dapat pesan seperti ini lagi, balas "stop" ya.

**Pesan 3**
Halo Kak [nama], bagaimana kuenya? Kalau ada yang kurang pas, ceritakan saja apa adanya, kami senang mendengar. Kalau tidak ingin dapat pesan seperti ini lagi, balas "stop" ya.

**Pesan 4 (kirim hanya bila ada menu lain yang relevan)**
Halo Kak [nama], karena Kakak sudah coba [nama kue], kami kabari ada [menu lain] yang sering dipilih bersamaan. Kalau tertarik, kami kirimkan daftar dan harganya. Kalau tidak ingin dapat pesan seperti ini lagi, balas "stop" ya.

### Kapan berhenti
- Pelanggan membalas apa pun: hentikan rangkaian, balas seperti percakapan biasa.
- Ada komplain atau retur: hentikan, tangani dulu, tidak ada pesan 3-4.
- Pelanggan minta berhenti: hormati, catat, jangan hubungi lewat kanal lain.

### Cara kirim
Anda mengirim satu per satu dari WA Anda, jam 09.00-20.00 waktu pelanggan, tidak hari Minggu. Mau pengingat tiap tanggal kirim? OpenClaw bisa mengingatkan Anda di Telegram (bukan mengirim ke pelanggan).

### Asumsi
Tanpa diskon, kanal WA, tidak ada fakta tentang kue selain yang Anda sebut.

### Pertanyaan
1) Cara simpan kue yang benar (untuk pesan 2)? 2) Ada menu lain yang ingin dikenalkan di pesan 4? 3) Nama pengirim?
