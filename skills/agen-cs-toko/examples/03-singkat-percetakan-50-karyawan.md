# 03 — Singkat/malas: percetakan 50+ karyawan, admin kewalahan

**Skenario:** S3 (normal, gaya malas). Persona: pemilik percetakan (skala 50+ karyawan, 5
admin CS). Input minim, tanpa daftar harga.

**Input pengguna (persis):**
> bikinin dong CS AI buat percetakan saya, admin 5 orang kewalahan chat masuk ratusan sehari. tiap malem kirim rekapnya ke telegram saya

---

## Output

Siap, Pak/Bu. Supaya draf CS **tidak mengarang harga**, saya butuh isi dasar percetakan dulu.
Jawab singkat saja. Yang belum ada boleh dikosongkan, nanti saya tandai `[isi ...]`:

1. **Daftar produk & harga** (boleh kirim file/foto price list): mis. kartu nama, brosur A5, spanduk per m², stiker, undangan.
2. **Minimal order & waktu pengerjaan** per produk (mis. "brosur min. 500 lbr, 2–3 hari kerja").
3. **Cara kirim desain & revisi** (format file, berapa kali revisi gratis).
4. **Pembayaran** (DP berapa %, transfer/QRIS) dan **kebijakan cetak ulang** bila salah cetak.
5. **Jam kerja admin** dan **siapa penerima eskalasi** (komplain/refund).

Sambil menunggu, ini yang sudah saya siapkan:
- `cs/PENGETAHUAN.md` dan `cs/ATURAN.md` dari template. Semua harga masih `[isi ...]`, jadi
  **belum dipakai** untuk menjawab harga.
- Pemicu eskalasi standar: komplain berat, refund, pembatalan pesanan besar, ancaman, data
  sensitif, dan pertanyaan yang tidak ada di basis pengetahuan.
- Untuk 5 admin: **satu basis pengetahuan dipakai bersama**, jadi jawaban semua admin sama.
  Tiap admin meneruskan chat ke bot Telegram yang sama dan menerima draf. Pelanggan tetap dibalas
  admin dari WA/marketplace masing-masing.

**Rekap harian ke Telegram (usulan, belum dijalankan):**
```bash
openclaw automations create \
  --cron "0 20 * * *" --tz "Asia/Jakarta" \
  --name "Rekap CS harian" \
  --message "Ringkas draf CS hari ini dari cs/log/<tanggal>.md: jumlah chat, 5 pertanyaan terbanyak, yang dieskalasi, dan pertanyaan yang belum ada di cs/PENGETAHUAN.md. Maks 15 baris." \
  --session isolated --announce --channel telegram --to "<chat id Telegram Anda>"
```
- Jalan tiap hari jam 20.00 WIB, **hanya bila komputer yang menjalankan OpenClaw menyala**.
- Setelah dibuat, uji sekali dengan `openclaw automations run <id>` (id muncul setelah create).
- Lanjut buat jadwal ini? (ya/tidak)

---

## Catatan penguji
- **Bagus:** satu pesan berisi 5 pertanyaan, tidak mengarang harga, dan saran basis pengetahuan
  bersama untuk 5 admin. Perintah `automations create --cron --tz --name --message --session
  isolated --announce --channel telegram --to` **diterima parser** di OpenClaw 2026.9.5 (berhenti
  di tahap Gateway tanpa kredensial, wajar di mesin uji). `automations run` **wajib id**,
  terverifikasi ("Missing required argument id").
- **Cacat (sedang):** prompt rekap di skill (`references/eskalasi-dan-kanal.md` §3) menyuruh
  automation "Baca **log draf balasan CS** hari ini", tetapi skill **tidak pernah menulis log
  apa pun**. Tidak ada langkah menyimpan ringkasan draf/eskalasi ke file. Automation dengan
  `--session isolated` tidak melihat percakapan admin, sehingga rekap akan kosong atau
  **dikarang** (jumlah chat, pertanyaan terbanyak). Di contoh ini penguji menambahkan
  `cs/log/<tanggal>.md` pada prompt, tetapi skill tetap perlu langkah "setiap draf, tambahkan
  satu baris ke cs/log/<tanggal>.md (tanpa nama/nomor pelanggan)".
- Skala 50+ dengan ratusan chat/hari: skill tidak membahas beban (satu bot untuk 5 admin) atau
  pemisahan sesi per admin (`session.dmScope`). Hanya disebut untuk Level 2.
