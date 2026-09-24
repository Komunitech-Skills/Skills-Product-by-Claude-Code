# Contoh 02 — Grup Reseller (iPhone, AM/PM, .zip, ada LRM tak terlihat)

## Skenario
S2 (normal, ditulis singkat/malas ala pengguna awam). Pengguna Bu Rina, admin brand skincare,
mengirim ekspor grup reseller sebagai `.zip` "Tanpa Media" dari iPhone (format
`[M/D/YY, H:MM:SS AM/PM] Nama: pesan`), berisi pesan multi-baris (rekap order), karakter LRM
(U+200E) tak terlihat di beberapa baris, stiker/media, 1 pesan dihapus, dan tanggal yang secara
obyektif ambigu (semua nilai hari & bulan ≤ 12 di seluruh file — kasus nyata yang bisa terjadi).
File: `input/WhatsApp Chat with Reseller Cantik Skincare.zip` (fiktif, dibuat untuk pengujian).

## Input pengguna (persis)
> bikinin ringkasan grup reseller ini dong, zip nya kepencet export td pagi

## Langkah yang dijalankan
```
python3 scripts/parse_ekspor_wa.py "WhatsApp Chat with Reseller Cantik Skincare.zip" --indent 0
```
Hasil: `format_terdeteksi: ios`, `urutan_tanggal: d/m`, **catatan**: *"Urutan tanggal ambigu (hari
& bulan sama-sama ≤ 12 di semua pesan). Default dipakai: d/m (Indonesia). Cek tanggal bila hasil
terasa janggal."* → skrip membaca "9/12/26" sebagai **9 Desember 2026**, padahal (dari konteks
percakapan yang membahas hal "hari ini") kemungkinan besar maksud aslinya adalah tanggal lain.
1 hari, 90 pesan (89 obrolan/media/dihapus + 1 sistem). Statistik: Bu Rina 25, Tari 17, Yuni 16,
Nita 16, Dedi 15; jam ramai 09.00–10.00; 6 media/stiker; 1 dihapus.

## Output

```
📋 RINGKASAN GRUP: Reseller Cantik Skincare
Rentang: 9 Des 2026 · 90 pesan (dari 5 orang)

⚠️ CATATAN FORMAT TANGGAL: tanggal di file ini ambigu — hari & bulan sama-sama ≤ 12 di semua
pesan, jadi tidak bisa dipastikan otomatis. Saya membacanya sebagai **9 Desember 2026** (format
Indonesia, hari/bulan). Kalau menurut kamu ini seharusnya tanggal lain (mis. 12 September, format
bulan/hari ala AS yang biasa dipakai iPhone berbahasa Inggris), cek ulang tanggal aslinya di
WhatsApp dan kabari saya — saya akan proses ulang.

🔴 PERLU PERHATIAN (10)
1. [08.20] Dedi: "Masker Charcoal kapan restock? dari minggu lalu kosong terus, customer saya
   udah nanyain mulu" → dijawab (09.00): restock tanggal 15
2. [09.30] Nita: "produk Body Lotion Mangga kemarin dikirim ke saya tapi botolnya bocor pas
   sampai, gimana ya kak? customer saya komplain" → dijawab (09.35): diganti gratis ongkir,
   dikirim besok pagi
3. [10.00] Yuni: "promo ongkir gratis buat reseller masih berlaku sampai kapan?" → dijawab
   (10.05): sampai akhir bulan, minimal order Rp 500.000
4. [10.20] Dedi: "kapan invoice bulan lalu saya dikirim? butuh buat laporan pajak toko" →
   dijawab (10.25): sore itu ke DM — lalu ditagih ulang jam 13.30 (belum diterima), baru benar-
   benar dikirim 13.35
5. [10.45] Nita: "kalau retur produk yang belum kebuka gimana caranya? ada customer minta
   refund" → dijawab (10.50): boleh, segel utuh, maks 7 hari, dikurangi ongkir
6. [11.45] Nita: "PO batch 2 Sabun Wajah kapan dibuka? banyak yang nanya ke aku" → dijawab
   (11.50): besok jam 9 pagi, minimal 30 pcs
7. [13.30] Dedi: "invoice bulan lalu saya masih ditunggu ya, deadline lapor pajak besok" →
   **urgent**, dijawab (13.35): dikirim saat itu juga
8. [14.30] Dedi: "customer aku komplain paket ga sampai udah 5 hari, ini resinya
   JX2209981123, tolong dicek ke kurir" → dijawab (14.35) & update (15.00): nyangkut di gudang
   transit, estimasi besok siang, dikasih voucher ongkir gratis sebagai kompensasi ke customer
9. [16.10] Dedi: "PO batch 2 ini saya mau ambil 40 pcs, deadline pembayaran kapan?" → dijawab
   (16.15): maks 2 hari setelah PO ditutup, lewat = slot hangus
10. [17.05] Yuni: "sblm off, izin nanya, stok Serum Glow yg 50ml ready ga? beda sama yg 30ml td"
    → dijawab (17.10): ready, Rp 68.000/pcs, tapi "nanti saya balas detail pas online lagi" —
    ⚠️ belum benar-benar tuntas, masih ada detail menyusul

📌 DAFTAR TINDAKAN
| Tugas | PIC | Tenggat |
|---|---|---|
| Kabari Dedi saat Masker Charcoal restock | Bu Rina | Tanggal 15 (Des, mengikuti asumsi format di atas) |
| Kirim katalog PDF ke Nita | Bu Rina | Selesai (dikirim 13.00) |
| Proses & kirim ganti Body Lotion Mangga ke Nita | Bu Rina | Besok pagi |
| Buka PO batch 2 Sabun Wajah (min. 30 pcs) | Bu Rina | Besok jam 9 pagi |
| Bayar PO batch 2 (40 pcs, Dedi) | Dedi | Maks 2 hari setelah PO ditutup |
| Balas detail stok & harga Serum Glow 50ml ke Yuni | Bu Rina | ⚠️ belum jelas — "nanti pas online lagi" |

🔵 INFO (5)
- [08.12] Tari order Serum Glow 30ml x25, total Rp 1.050.000, DP diterima 50%, sisa Rp 525.000
  saat barang siap kirim
- [09.15] Tari mengirim bukti transfer DP
- [10.30] Bu Rina mengirim media (video, sepertinya salah kirim — Yuni & Tari menanyakan isinya)
- [11.30] Yuni menghapus satu pesan (isi tidak diketahui)
- [15.00] Update status resi Dedi: nyangkut di gudang transit, sampai besok siang

💬 OBROLAN
Sekitar 30+ pesan obrolan/sapaan/candaan (mis. "mantap noted", "gaskeun", stiker, emoji 😂🔥)

📎 Lampiran/media: 6 (termasuk 2 stiker) · 🗑️ Pesan dihapus: 1
⏰ Jam paling ramai: 09.00–10.00

Asumsi: nama saya di grup tidak disebutkan pengguna, jadi deteksi "perlu perhatian" memakai
pola pertanyaan langsung/keputusan/uang/komplain secara umum (bukan hanya mention "@Bu Rina").
Tanggal file dibaca dengan asumsi format Indonesia (d/m) karena ambigu — lihat catatan di atas.
```

## Catatan penguji
- **Multi-baris:** pesan Tari jam 08.12 (5 baris: "Order baru:/Nama:/Produk:/Total:/Metode:")
  berhasil digabung jadi satu pesan oleh parser (dicek di `out/b.json`), dan skill menyajikannya
  dengan benar sebagai satu info order — bukan pecah 5 baris terpisah.
- **LRM:** karakter tak terlihat U+200E yang disisipkan di beberapa baris (termasuk baris sistem
  enkripsi paling awal) tidak merusak parsing — semua pesan tetap terbaca, dicek lewat
  `verifikasi_independen.py` yang hasilnya identik dengan skrip skill.
- **Ambiguitas tanggal — INI YANG PALING PENTING:** skill **benar** mengikuti SKILL.md langkah 3
  dengan menampilkan catatan ambiguitas ke pengguna secara eksplisit di awal ringkasan, bukan
  diam-diam menganggap tanggalnya "9 Desember". Ini teruji baik.
- **Cacat sedang:** karena seluruh 90 pesan jatuh ke satu tanggal versi parser ("9 Desember"),
  ringkasan tidak dipecah per hari — padahal dari isi percakapan (nada "hari ini", "besok",
  volume 90 pesan dalam rentang jam 08.00–17.32) jelas ini SATU hari kerja sungguhan, cuma
  salah baca tanggal. Ini bukan bug skill (tanggal memang ambigu di sumbernya), tapi **saran
  perbaikan konkret**: SKILL.md langkah 8 sebaiknya menambahkan bahwa jika `urutan_tanggal`
  disertai catatan ambigu DAN cuma menghasilkan 1 hari dengan volume tinggi dalam rentang jam
  singkat, sebutkan eksplisit ke pengguna "kemungkinan besar ini semua 1 hari yang sama,
  terlepas dari pembacaan tanggal" agar tidak membingungkan pembeli awam yang melihat tanggal
  "9 Desember" padahal hari ini baru September.
- **Akurasi:** seluruh nominal (Rp 45.000, 42.000, 39.500, 1.050.000, 525.000, 38.000, 68.000)
  dan nomor resi JX2209981123 dicek persis sama dengan sumber, tidak ada yang salah kutip.
