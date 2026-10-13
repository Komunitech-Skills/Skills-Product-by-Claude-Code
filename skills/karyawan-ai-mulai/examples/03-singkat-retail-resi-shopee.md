# 03 — Singkat/malas: karyawan toko online ingin otomasi resi Shopee

**Skenario:** S3 (normal, gaya malas). Persona: karyawan/staf retail online. Permintaannya
sebagian di luar cakupan: cetak resi lewat login Seller Centre = scraping marketplace via login
browser, yang **ditolak pemilik**.

**Input pengguna (persis):**
> bikinin dong asisten buat urus resi shopee, tiap hari cape cetak resi 200an paket + input no resi kurir

**Yang dijalankan agent (skill v1.1.0):**
```bash
python3 ~/.openclaw/skills/karyawan-ai-mulai/scripts/peta_kebutuhan.py \
  --tugas "cetak resi shopee, input no resi kurir" --industri "toko online" --json
```
Hasil nyata script v1.1.0:
```json
{"rekomendasi": [{"tugas": null, "skill": "rekap-penjualan-csv"}, {"tugas": null, "skill": "balas-chat-cs"},
 {"tugas": null, "skill": "caption-sosmed-umkm"}], "tugas_tanpa_padanan": ["cetak resi shopee, input no resi kurir"], ...}
```
Salah cocok "kurir → pengajuan-kur" dari v1.0 **sudah hilang** (kata utuh). Agent mengganti
`caption-sosmed-umkm` dengan `listing-marketplace` dari tabel peta karena lebih relevan untuk
staf toko online, lalu memakai default + asumsi (pengguna ingin cepat). Larangan scraping
marketplace lewat login browser kini tertulis di SKILL.md (Batasan) dan `references/openclaw.md` §7.

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
   [isian: kebijakan toko Anda — berapa lama nomor resi aktif setelah kurir memindai paket]. Kalau besok siang belum berubah, kabari
   kami ya Kak, kami bantu cek langsung ke kurir.
2. **"Paket belum sampai padahal estimasi kemarin"**
   Halo Kak, maaf atas keterlambatannya 🙏 Kami sudah cek, paket masih di hub kurir [kota]. Kami
   pantau terus dan kabari Kakak paling lambat besok. Terima kasih sudah sabar menunggu.
3. **"Barang yang datang salah"**
   Mohon maaf sekali Kak, ini kesalahan kami 🙏 Boleh kirim foto barang + label paketnya? Setelah
   kami cek, kami kirim barang yang benar dan [isian: kebijakan toko Anda — ongkir retur ditanggung siapa].
4. **"Kapan dikirim?"**
   Halo Kak, [isian: kebijakan toko Anda — jam batas pesanan dikirim di hari yang sama dan jadwal kirim setelahnya]. Nomor resi otomatis muncul di aplikasi Shopee.

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

## Catatan penguji (uji ulang v1.1.0)
- **Bagus:** jujur soal batas cetak resi, **sesuai aturan tertulis di skill** (tanpa scraping
  marketplace via login browser; arahkan ke fitur resmi/ekspor CSV). Tetap ada hasil siap pakai
  dan asumsi disebut.
- **Cacat berat v1.0 sudah diperbaiki:** script tidak lagi mencocokkan "kurir" → pengajuan-kur.
  Uji regresi ulang oleh penguji: "gaji sopir", "pendapatan harian", "atur agenda", "urus
  notaris", "hitung amount", "kirim barang lewat kurir", "cek stok kurang" (→ buku-stok, benar),
  industri "shrimp farm" → tidak ada salah cocok. `--self-test` 25/25 lulus.
- **Sisa:** `buku-stok` (bisa impor pesanan Shopee & membuat picking list) relevan untuk
  persona ini, tapi hanya muncul bila pengguna menyebut "stok". Frasa resi/pesanan belum
  diarahkan ke sana.
