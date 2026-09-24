# 04 — Input tidak lengkap: "catat penjualan tadi"

**Skenario:** Kedai Kopi Senja (DB skenario 01) sudah berjalan. Pemilik mengetik singkat tanpa barang, jumlah, cara bayar, maupun jam.

**Input pengguna (persis):**
> catat penjualan tadi

## Output

Agent **tidak** menjalankan `jual` dengan kalimat itu (script hanya akan menjawab *"'catat penjualan tadi': tidak dikenal. Tidak ada produk yang mirip"*, sudah dicoba penguji) dan tidak mengarang pesanan. Sesuai SKILL.md bagian Input ("tanyakan sekali dalam satu pesan bernomor") dan langkah B.4 (transaksi terlewat pakai `--waktu`):

```
Siap, saya catat. Tolong lengkapi sekaligus ya:
1. Apa saja yang dibeli dan berapa? (mis. "2 kopi susu, 1 roti bakar keju")
2. Ada diskon? (per barang atau seluruh nota)
3. Bayarnya pakai apa dan berapa? (tunai berapa / QRIS / transfer / campuran). Kalau tidak disebut, saya anggap tunai uang pas.
4. Kira-kira jam berapa transaksinya? (agar masuk rekap per jam & hitungan tutup kasir yang benar)

Contoh balasan cepat: "2 kopi susu, 1 roti bakar keju, qris, jam 10.15"
```

**Balasan pengguna:**
> 2 kopi susu, 1 roti bakar keju, qris, jam 10.15

Agent menjalankan `jual --pesan "2 kopi susu, 1 roti bakar keju, bayar qris" --waktu "2026-09-24 10:15"`:
```
Nota N-260924-0013 (belum disimpan) | 24/09/2026 10:15
1. Kopi Susu Gula Aren 2 x Rp 18.000 = Rp 36.000
2. Roti Bakar Keju 1 x Rp 17.000 = Rp 17.000
TOTAL Rp 53.000 | QRIS Rp 53.000 | Kembalian Rp 0
Catatan: "kopi susu" saya baca sebagai Kopi Susu Gula Aren (KSGA).
Catatan: kasir hari ini sudah ditutup jam 21.00; nota ini tidak masuk hitungan tutup kasir tadi (QRIS, jadi uang laci tidak terpengaruh).
Simpan? Balas "ya".
```

Variasi input kurang yang diuji dengan script:
| Input | Tanggapan (dari script, disampaikan agent) |
|---|---|
| `kopi, bayar` | "'kopi': cocok dengan beberapa produk. Pilih salah satu: Kopi Susu Gula Aren (KSGA) Rp 18.000; Kopi Hitam (KH) Rp 12.000; Kopi Tubruk (KT) Rp 10.000" |
| `es teh 2 sama roti bakar` | dua pilihan Es Teh (Manis/Lemon) + dua varian Roti Bakar (Coklat/Keju) dalam satu pesan |
| `1 NSG` (tanpa cara bayar) | tercatat sebagai tunai uang pas, dengan catatan "Cara bayar tidak disebut: dianggap TUNAI uang pas. Koreksi bila salah." |
| `1 NSG, bayar qris, transfer` | "Lebih dari satu metode bayar tanpa jumlah. Sebutkan jumlah per metode, mis. 'qris 50rb, tunai 50rb'." |

## Catatan penguji
- **Bagus:** satu pertanyaan bernomor, singkat, dengan contoh balasan; default (tunai uang pas) disebut sebagai asumsi; produk ambigu selalu ditanyakan, tidak ditebak.
- **Kurang (ringan):** SKILL.md tidak menulis eksplisit "jangan kirim kalimat tanpa barang ke script" dan tidak menyebut perilaku bila nota dicatat **setelah** kasir ditutup (script menaruh nota tanpa sesi dan memberi peringatan "Kasir belum dibuka", yang membingungkan pengguna awam karena kasir *sudah* ditutup, bukan belum dibuka). Saran: bedakan pesan "kasir sudah ditutup jam …; nota ini tidak masuk tutup kasir hari ini".
- Keterangan: di uji nyata, peringatan script berbunyi "Kasir belum dibuka (buka-kasir)…"; baris "kasir hari ini sudah ditutup" di atas adalah parafrase agent.
</content>
</invoke>
