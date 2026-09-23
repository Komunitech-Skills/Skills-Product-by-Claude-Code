# 03 — Singkat/malas: karyawan toko online ingin otomasi resi Shopee

**Skenario:** S3 (normal, gaya malas). Persona: karyawan/staf retail online. Permintaannya
sebagian di luar cakupan: cetak resi lewat login Seller Centre = scraping marketplace via login
browser, yang **ditolak pemilik**.

**Input pengguna (persis):**
> bikinin dong asisten buat urus resi shopee, tiap hari cape cetak resi 200an paket + input no resi kurir

**Yang dijalankan agent:**
```bash
python3 ~/.openclaw/skills/karyawan-ai-mulai/scripts/peta_kebutuhan.py \
  --tugas "cetak resi shopee, input no resi kurir" --industri "toko online" --json
```
Hasil nyata script:
```json
{"rekomendasi": [{"tugas": "cetak resi shopee, input no resi kurir", "skill": "pengajuan-kur"}], ...}
```
Hasil ini **salah**: kata "kurir" mengandung "kur", sehingga script merekomendasikan skill
pengajuan KUR (pinjaman bank). Agent penguji mengabaikan hasil script dan mencocokkan manual ke
tabel `peta-skill.md` (fallback yang diizinkan SKILL.md). Pengguna ingin cepat, jadi dipakai
default + asumsi (tanpa wawancara).

---

## Output

## Ringkasan Anda
Anda staf toko online (retail) yang setiap hari mengurus sekitar 200 paket Shopee: cetak resi
dan input nomor resi kurir. Karena Anda ingin cepat, saya pakai pengaturan default (lihat asumsi
di bawah).

## Rekomendasi Paket Kerja Pertama
Jujur dulu: **cetak resi dan input nomor resi otomatis di Shopee belum bisa kami sediakan.**
Caranya harus membuat AI login ke Seller Centre dan mengklik-klik layar. Itu melanggar aturan
Shopee, akun toko bisa dibatasi, dan data login Anda harus dipegang AI. Cara resmi yang aman:
fitur **Cetak Massal / Atur Pengiriman Massal** di Shopee Seller Centre, atau aplikasi mitra resmi
Shopee (Shopee Open Platform) yang dipakai toko Anda.

Yang **bisa** langsung meringankan kerja harian Anda:
1. **rekap-penjualan-csv**: kirim file **Ekspor Pesanan** Shopee, langsung dapat rekap pesanan dan
   omzet harian. Pesanan batal/retur tidak ikut dihitung.
2. **balas-chat-cs**: draf balasan untuk chat "resi kok belum update?", "paket belum sampai", komplain salah kirim.
3. **listing-marketplace**: judul & deskripsi produk yang rapi saat ada barang baru.

Ide otomasi lanjutan (opsional): rekap pesanan kemarin dikirim otomatis tiap pagi. Syaratnya
komputer menyala terus dan file ekspor ditaruh di satu folder. Bisa dibahas setelah minggu pertama.

## Status Pemasangan
- Sudah terpasang: belum ada
- Perlu dipasang: rekap-penjualan-csv, balas-chat-cs, listing-marketplace → **boleh saya pasang
  sekarang ke folder skill OpenClaw (`~/.openclaw/skills`)? (ya/tidak)**

*[Pengguna: "ya"]*: terpasang.

## Hasil Tugas Pertama: 4 balasan chat soal resi (siap tempel)
1. **"Kak resi saya kok belum update?"**
   Halo Kak, mohon maaf menunggu 🙏 Paket Kakak sudah kami serahkan ke kurir hari ini. Nomor resi
   biasanya aktif 1×24 jam setelah kurir memindai paket. Kalau besok siang belum berubah, kabari
   kami ya Kak, kami bantu cek langsung ke kurir.
2. **"Paket belum sampai padahal estimasi kemarin"**
   Halo Kak, maaf atas keterlambatannya 🙏 Kami sudah cek, paket masih di hub kurir [kota]. Kami
   pantau terus dan kabari Kakak paling lambat besok. Terima kasih sudah sabar menunggu.
3. **"Barang yang datang salah"**
   Mohon maaf sekali Kak, ini kesalahan kami 🙏 Boleh kirim foto barang + label paketnya? Setelah
   kami cek, kami kirim barang yang benar dan ongkir retur kami tanggung.
4. **"Kapan dikirim?"**
   Halo Kak, pesanan yang masuk sebelum jam 15.00 kami kirim di hari yang sama. Setelah jam 15.00
   dikirim besok pagi. Nomor resi otomatis muncul di aplikasi Shopee.

## Rencana 7 Hari
| Hari | Kebiasaan baru | Skill |
|---|---|---|
| 1 | Simpan 4 balasan di atas ke Balasan Cepat Shopee Chat | balas-chat-cs |
| 2 | Coba Cetak Massal resi di Seller Centre (fitur resmi) | — |
| 3 | Ekspor pesanan kemarin, minta rekap | rekap-penjualan-csv |
| 4 | Tempel 5 chat komplain, minta draf balasan | balas-chat-cs |
| 5 | Rapikan judul 3 produk terlaris | listing-marketplace |
| 6 | Rekap pesanan 1 minggu: hari tersibuk, produk paling banyak dikirim | rekap-penjualan-csv |
| 7 | Evaluasi. Kalau komputer toko menyala terus, bahas rekap pagi otomatis | — |

## Privasi
Data Anda tetap di komputer Anda. File ekspor pesanan berisi nama dan alamat pembeli (data
pribadi), jadi simpan seperlunya saja. Mau saya jalankan cek privasi dasar (`cek-privasi-openclaw`)
sekarang, atau lain kali?

**Asumsi yang dipakai:** skala tim 2–5 orang; kanal: langsung di komputer toko; komputer tidak
selalu menyala; ada kekhawatiran privasi (default aman). Silakan koreksi kapan saja.

---

## Catatan penguji
- **Bagus (karena agent mengikuti fallback manual):** jujur soal batas, tidak menjanjikan
  otomasi login Shopee, tetap ada hasil siap pakai, dan asumsi disebut.
- **Cacat berat (script):** `peta_kebutuhan.py` mencocokkan dengan substring, sehingga
  **"kurir" → pengajuan-kur**. Persona retail yang menyebut "resi kurir" akan dapat rekomendasi
  pinjaman KUR bila agent mempercayai script. Uji tambahan menunjukkan salah cocok serupa: "gaji
  sopir" → sop-writer, "pendapatan harian" → perjanjian-sederhana ("nda"), "atur agenda" →
  katalog-reseller ("agen"), "urus notaris" → ekstrak-nota-faktur, industri "shrimp farm" → paket HR.
- **Sedang:** SKILL.md tidak menyebut larangan pemilik "scraping marketplace lewat login browser".
  Penolakan di atas berasal dari penilaian agent, bukan dari skill. Kebutuhan stok/inventori
  (kebutuhan #7) belum ada padanan di peta.
