# 00 — Uji A/B: S1 dengan vs tanpa skill

**Input pengguna (sama persis dengan S1):**
> Tolong balasin ulasan Shopee bintang 1 ini buat toko aku Rumah Alya: "Pesen gamis ukuran L yang dateng M!! Udah gitu chat seller slow respon 2 hari. Nyesel belanja di sini." Kami mau tukar ke L, ongkir retur kami yang tanggung. Admin yang pegang chat namanya Nisa.

## Output TANPA skill (AI agent biasa, tanpa membaca skill apa pun)
```
Halo Kak, terima kasih atas ulasannya 🙏

Mohon maaf sekali atas ketidaknyamanannya. Kami sangat menyesal ukuran yang Kakak terima tidak sesuai dan respon chat kami lambat.
Hal ini terjadi karena lonjakan pesanan beberapa hari terakhir sehingga tim kami sedikit kewalahan 🙏

Tenang Kak, kami akan menukar gamisnya ke ukuran L dan ongkir retur kami tanggung sepenuhnya! Silakan hubungi admin kami, Nisa,
di WhatsApp 0812-xxxx-xxxx agar prosesnya lebih cepat ya Kak.

Semoga Kakak berkenan memberikan kesempatan kedua dan mengubah rating setelah masalahnya selesai 😊

Salam hangat,
Rumah Alya
```

## Output DENGAN skill
Lihat `01-shopee-bintang-1-salah-ukuran.md` (balasan publik 358 karakter + alternatif + pesan chat pribadi + hasil cek script + catatan pemilik).

## Berdampingan

| Aspek | TANPA skill | DENGAN skill |
|---|---|---|
| Ajakan ke luar platform | **"hubungi … di WhatsApp 0812-…"** — dilarang di marketplace (penalti) | Diarahkan ke chat toko Shopee |
| Permintaan ubah rating | **"mengubah rating setelah masalahnya selesai"** — melanggar kebijakan ulasan | Tidak ada; catatan pemilik mengingatkan larangannya |
| Alasan karangan | "lonjakan pesanan … tim kewalahan" — tidak diberikan pengguna | Tidak mengarang penyebab |
| Janji publik | "ongkir retur kami tanggung sepenuhnya" di publik → bisa diminta semua pembeli | Janji detail hanya di chat pribadi |
| Pesan chat pribadi | Tidak ada | Ada, siap kirim, meminta bukti foto label |
| Pengecekan | Tidak ada | Script: tanpa data pribadi, tanpa ajakan keluar platform, panjang 358/500 |
| Urutan kirim | Tidak dibahas | "Kirim chat pribadi dulu, baru posting balasan publik" |

## Penilaian
- **Lebih baik berkat skill:** versi tanpa skill melakukan dua pelanggaran kebijakan marketplace sekaligus (mengarahkan ke WA dengan nomor, dan meminta
  pembeli mengubah rating) plus mengarang alasan keterlambatan. Versi dengan skill aman, tetap empatik, dan dilengkapi pesan chat pribadi + urutan kerja.
- **Setara:** nada minta maaf sama-sama sopan.
- **Kesimpulan:** hasil dengan skill **jelas lebih baik**.
