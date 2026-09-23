# 01 — Toko online hijab: bangun basis pengetahuan + draf balasan Copilot

**Skenario:** S1 (normal). Persona: pemilik toko online hijab (fiktif "Hijab Sakinah"). Ia
mengirim daftar harga dan satu chat pelanggan. Chat itu menanyakan hal yang **sebagian tidak
ada** di daftar harga (stok warna, ongkir ke Bekasi).

**Input pengguna (persis):**
> bikinin CS buat toko hijab saya dong, namanya Hijab Sakinah. harga: pashmina ceruti 89rb (8 warna), bergo instan jersey 65rb (S/M/L), segiempat voal premium 125rb, paket 3 pashmina 240rb campur warna. kirim pake J&T sama SiCepat, gratis ongkir min belanja 300rb jabodetabek. bayar transfer BCA atau QRIS. tuker warna/ukuran maks 3 hari, ongkir retur pembeli. ini ada chat masuk: "kak pashmina ceruti ready warna dusty pink? kalo ambil 3 bisa lebih murah gak? ongkir ke bekasi berapa"

**Yang dijalankan agent:** menulis `cs/PENGETAHUAN.md` dan `cs/ATURAN.md` dari template (nilai
kosong ditandai `[isi ...]`), lalu memeriksa draf dengan script (nyata, di `/tmp/uji-agen-cs-toko/`):
```bash
python3 ~/.openclaw/skills/agen-cs-toko/scripts/periksa_draf.py --pengetahuan cs/PENGETAHUAN.md --draf draf.txt
# [PERIKSA] 1 nominal di draf TIDAK ditemukan di basis pengetahuan: Rp 27.000   (exit 1)
# [OK] Tidak ada pola data sensitif
```
Rp 27.000 adalah selisih hasil hitungan (3 × Rp 89.000 = Rp 267.000; Rp 267.000 − Rp 240.000 =
Rp 27.000, diverifikasi dengan python). Karena ini hitungan, bukan karangan, angka tersebut
dicantumkan di "Perlu dicek admin".

---

## Output

### Basis pengetahuan dibuat
`cs/PENGETAHUAN.md` (ringkas):
| Nama | Varian | Harga |
|---|---|---|
| Pashmina Ceruti | 8 warna | Rp 89.000 |
| Bergo Instan Jersey | S/M/L | Rp 65.000 |
| Segiempat Voal Premium | motif | Rp 125.000 |
| Paket 3 Pashmina | campur warna | Rp 240.000 |

- Pengiriman: J&T, SiCepat. Gratis ongkir min. belanja Rp 300.000 (Jabodetabek). Estimasi: `[isi ...]`
- Bayar: transfer BCA, QRIS. Nomor rekening toko: `[isi ...]`
- Retur: tukar warna/ukuran maks. 3 hari setelah diterima, ongkir retur ditanggung pembeli.
- **Masih kosong:** stok per warna, tarif ongkir per kota, jam kerja admin, nama 8 warna.

`cs/ATURAN.md`: jam kerja default Senin–Sabtu 09.00–17.00 WIB (silakan ubah). Isinya juga
pemicu eskalasi (komplain berat, refund, ancaman, data sensitif, pertanyaan di luar basis
pengetahuan), pesan penahan, dan pembuka "asisten virtual Hijab Sakinah".

Cek dulu ringkasan ini ya Kak. Kalau sudah benar, basis pengetahuan ini yang dipakai untuk semua draf.

### Draf balasan untuk chat masuk
**Keyakinan:** Sedang
**Eskalasi:** Tidak

**Draf 1:**
Halo Kak, terima kasih sudah mampir ke Hijab Sakinah 🤍
Pashmina Ceruti harganya Rp 89.000/pcs. Kalau ambil 3, ada Paket 3 Pashmina jadi Rp 240.000
(boleh campur warna), lebih hemat Rp 27.000 dibanding beli satuan 😊
Untuk warna dusty pink, saya cek dulu stoknya ya Kak.
Gratis ongkir berlaku untuk belanja minimal Rp 300.000 di Jabodetabek. Untuk paket 3 pashmina,
ongkir ke Bekasi saya hitungkan dulu ya Kak, boleh info kecamatannya?

**Draf 2 (alternatif, lebih singkat):**
Halo Kak 🤍 Pashmina Ceruti Rp 89.000/pcs, kalau ambil 3 jadi Rp 240.000 (Paket 3 Pashmina,
campur warna). Dusty pink saya cek stok dulu ya. Ongkir ke Bekasi boleh info kecamatannya, Kak?

**Perlu dicek admin sebelum kirim:**
- Stok warna **dusty pink** (belum ada di basis pengetahuan).
- Ongkir ke Bekasi untuk belanja Rp 240.000 (di bawah batas gratis ongkir Rp 300.000; tarif per kota belum ada).
- "Hemat Rp 27.000" adalah hasil hitungan (3 × Rp 89.000 − Rp 240.000), bukan harga di daftar.
  Script menandainya, jadi hapus bila tidak ingin menyebut.

*Draf ini untuk Anda tempel & kirim sendiri. Bot tidak mengirim apa pun ke pelanggan.*

### Kanal untuk menerima draf
Saran: **Telegram** (bot resmi, tanpa risiko blokir). Anda meneruskan chat pelanggan ke bot
Telegram, lalu bot membalas dengan draf. Setup (jalankan sendiri atau saya bantu, dengan izin):
`openclaw channels add --channel telegram --token <token dari @BotFather>`

---

## Catatan penguji
- **Bagus:** basis pengetahuan dari satu pesan, bagian kosong ditandai jujur, dan tidak ada stok
  atau ongkir yang dikarang. Tingkat keyakinan Sedang tepat. Script menangkap angka turunan.
  Mode Copilot jelas. `channels add --channel telegram --token` **terverifikasi jalan** di HOME
  uji (token fiktif → akun Telegram "default", `dmPolicy: pairing`). `--token` tidak tercantum
  di `--help` umum, tapi ada di contoh resmi dan berfungsi.
- **Kurang:** pengguna menulis harga "89rb". Bila draf juga memakai "Rp 89rb", script membacanya
  sebagai **Rp 89** dan menandainya sebagai nominal asing (lihat HASIL-UJI). Draf di atas sengaja
  memakai format lengkap.

## Uji ulang v1.0.1
- "Rp 89rb" dan "240 ribu" kini dibaca benar (Rp 89.000 / Rp 240.000; draf harga benar → exit 0).
  Draf di atas dijalankan ulang: tetap hanya menandai "hemat Rp 27.000" (angka turunan), sesuai harapan.
- Script kini selalu mencetak pengingat "Klaim STOK tidak diperiksa", jadi baris "stok dusty pink
  perlu dicek admin" di draf makin penting.
- Kanal: v1.0.1 menjelaskan persetujuan pairing Telegram (`openclaw pairing list telegram`,
  `openclaw pairing approve telegram <KODE>`). Keduanya terverifikasi ada di 2026.9.5.
