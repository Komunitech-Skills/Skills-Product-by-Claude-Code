# Laporan Insiden Rapi, 5 Menit Setelah Masalah Terjadi

**Dari kejadian panik — pesanan salah kirim, kasir error, komplain viral — jadi laporan lengkap + draf minta maaf, siap kirim.**

## Manfaat
- ✅ Susun laporan insiden lengkap (kronologi, dampak berangka, akar masalah, pencegahan) dari cerita berantakan, dalam hitungan menit
- ✅ Akar masalah dicari pakai 5 Kenapa yang **mengarah ke proses**, bukan menyalahkan karyawan
- ✅ Angka dampak selalu dari input Anda — tidak pernah dikarang
- ✅ Langsung dapat **draf permintaan maaf ke pelanggan** (sopan, tanpa janji berlebihan) + **ringkasan siap tempel ke WA tim/pemilik**
- ✅ Kalau menyangkut data pelanggan, otomatis diingatkan kewajiban UU PDP secara umum dan diarahkan ke skill kebijakan privasi

## Cocok untuk siapa
- Pemilik toko online/offline yang baru kena masalah operasional (retur massal, stok habis promo, kasir/QRIS error)
- Admin/CS yang harus cepat menjawab pelanggan setelah kejadian dan melapor ke atasan
- Owner UMKM yang ingin insiden dicatat rapi supaya bisa dievaluasi, bukan cuma diributkan lalu dilupakan

## Contoh sebelum & sesudah
**Sebelum:** "QRIS di toko error total dari jam 12 siang sampe jam 1, pas lagi rame jam makan siang. Kasir cuma bisa terima cash, ada sekitar 15 pelanggan yang batal beli karena cuma bawa uang digital. Internet toko emang sering putus-nyambung, cuma pake 1 provider."

**Sesudah (cukup ketik: "buatin laporan insiden dari cerita ini"):**
```
## Akar Masalah (5 Kenapa)
1. Kenapa QRIS error? → Koneksi internet toko terputus.
2. Kenapa koneksi terputus? → Internet toko sering putus-nyambung.
3. Kenapa ini menghentikan semua pembayaran? → Hanya 1 provider internet, tanpa cadangan.
Akar masalah: Tidak ada internet/pembayaran cadangan saat provider utama bermasalah.

## Rencana Pencegahan
| Tindakan | PJ | Tenggat |
| Siapkan internet cadangan | Pemilik/Supervisor | [isi] |
| Siapkan QRIS statis cadangan | Kasir/Supervisor | [isi] |
```
Plus draf minta maaf & ringkasan WA — lihat contoh lengkap di `examples/`.

## Cara pakai
Setelah terpasang, cukup ceritakan kejadiannya seperti chat biasa ke AI agent kamu, misalnya:
- "Buatin laporan insiden, kemarin 40 pesanan salah alamat pas promo 9.9..."
- "QRIS error 1 jam pas jam makan siang, tolong susun laporan + draf minta maaf"
- "Ada data pelanggan kekirim ke grup salah, gimana laporannya?"

Jika info penting (tanggal, jumlah terdampak) belum disebut, skill akan menanyakan sekali dalam satu pesan — bukan berulang-ulang.

### Instalasi
Ikuti panduan instalasi per platform (OpenClaw, Claude Code, Codex, Cursor) di `docs/instalasi.md` pada paket pembelian.

## FAQ
**1. Apakah skill ini bisa dipakai untuk kebocoran data pelanggan?**
Bisa untuk kebocoran ringan (mis. data terkirim ke grup salah). Skill akan menjelaskan secara umum kewajiban UU 27/2022 (UU PDP) dan mengarahkan ke skill `kebijakan-privasi-pdp` serta konsultan — ini **bukan nasihat hukum**.

**2. Apakah laporan ini bisa dipakai untuk memberi sanksi ke karyawan?**
Tidak dirancang untuk itu. Skill ini sengaja mengarahkan akar masalah ke proses/sistem, bukan ke individu. Untuk tindak lanjut kedisiplinan, gunakan skill `surat-peringatan-karyawan` terpisah.

**3. Bagaimana kalau saya belum tahu jumlah kerugian pasti?**
Tidak masalah — skill akan menandai bagian itu `[isi: jumlah]` daripada menebak-nebak, supaya angka di laporan tetap bisa dipercaya.

---
*Terinspirasi dari struktur `incident-postmortem`, `customer-incident-update`, dan `apology-letter` (MIT, pm-claude-skills), ditulis ulang & diperluas untuk konteks UMKM Indonesia. Rincian di `ATTRIBUTION.md`.*
