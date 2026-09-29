# 02 — Normal: "Promo gajian di IG, TikTok, WA — mana yang paling bawa pembeli?"

**Pembuat:** uji pembuat 29 Sep 2026 terhadap **Umami 3.4.0 asli** (Docker resmi, 127.0.0.1) dengan data fiktif landing page "Keripik Bu Sri" (`tests/isi_data_fiktif.py`). Akun AI `agen-baca` (view-only via tim), kunci API. Penguji independen menulis hasilnya sendiri di `HASIL-UJI.md`.

## Yang dijalankan agent
```
umami.py sumber --periode minggu-lalu
umami.py utm --periode 30hari
umami.py konversi --periode minggu-lalu
```

## Keluaran skill (apa adanya)
```
SUMBER TRAFIK: Keripik Bu Sri (landing) (keripikbusri.contoh.id)
Periode: minggu lalu, Senin 21 Sep 2026 - Minggu 27 Sep 2026
Kanal (per kunjungan):
  Kanal                                           Kunjungan    %  Pengunjung
  Media sosial (organik)                                  6  50%           6
  Langsung (termasuk WA/aplikasi tanpa UTM)               4  33%           4
  Pencarian Google dll (organik)                          2  17%           2
Situs perujuk (referrer):
  Situs                               Pengunjung  Kunjungan
  l.instagram.com                              3          3
  google.com                                   2          2
  tiktok.com                                   2          2
  l.facebook.com                               1          1
Catatan: klik dari WhatsApp, Telegram, aplikasi, atau QR biasanya TIDAK membawa alamat asal, jadi masuk 'Langsung'. Pakai tautan ber-UTM (perintah utm) agar terlihat jelas.

KAMPANYE UTM: Keripik Bu Sri (landing) (keripikbusri.contoh.id)
Periode: 30 hari terakhir, 31 Agu 2026 - 29 Sep 2026 (s.d. pukul 16.00)
Kampanye (utm_campaign):
  Nilai                               Pengunjung  Kunjungan  Tayangan
  promo-gajian-sep                            10         12        12
  reseller-okt                                 2          2         2
Sumber (utm_source):
  Nilai                               Pengunjung  Kunjungan  Tayangan
  instagram                                    4          5         5
  whatsapp                                     4          5         5
  tiktok                                       3          4         4
Medium (utm_medium):
  Nilai                               Pengunjung  Kunjungan  Tayangan
  social                                       4          5         5
  video                                        3          4         4
  status                                       3          3         3
  grup                                         2          2         2
Catatan: angka UTM dihitung dari halaman yang dibuka lewat tautan ber-UTM. Umami tidak menempelkan UTM ke event (klik WA/beli), jadi konversi per kampanye tidak dihitung di sini.

KONVERSI (EVENT): Keripik Bu Sri (landing) (keripikbusri.contoh.id)
Periode: minggu lalu, Senin 21 Sep 2026 - Minggu 27 Sep 2026
Pembanding: 14 Sep 2026 - 20 Sep 2026
  Event                     Jumlah  Pengunjung  Tingkat konversi  Sebelumnya
  klik-wa                        3           3             27,3%           1
  beli                           2           2             18,2%           0
Tingkat konversi = pengunjung yang melakukan event / 11 pengunjung unik periode ini.
- beli / nilai: total Rp47.000 dari 2 event (dari data tombol, BUKAN omzet resmi - cocokkan dengan catatan penjualan)
- beli / produk: Keripik Balado 250 g (1); Keripik Original 250 g (1)
- klik-wa / tombol: pesan-balado (2); hero (1)
```

## Jawaban agent ke pengguna (ringkas)
Dalam 30 hari, kampanye **promo-gajian-sep** membawa 10 pengunjung: Instagram 4, WhatsApp 4, TikTok 3 (satu orang bisa datang dari lebih dari satu sumber, jadi tidak dijumlah). Minggu lalu **3 dari 11 pengunjung (27,3%) klik tombol WA** dan 2 klik Beli (total nilai tombol Rp47.000 — ini dari klik tombol, bukan omzet resmi).

Catatan jujur: Umami tidak mencatat kampanye pada klik tombol, jadi **tidak bisa dipastikan** klik WA berasal dari IG atau TikTok. *Saran:* pakai tautan WA/tautan pelacak berbeda per kanal (panduan §5c & §8).

## Verifikasi independen
Referrer & UTM per pengunjung unik dihitung ulang dari daftar kunjungan: cocok (IG 3, google 2, tiktok 2, facebook 1; 30 hari: instagram 4, whatsapp 4, tiktok 3; promo-gajian-sep 10, reseller-okt 2). Kanal: 6+4+2 = 12 kunjungan = total kunjungan. Konversi 3÷11 = 27,27% → 27,3%; 2÷11 = 18,2%. **Cocok.**
