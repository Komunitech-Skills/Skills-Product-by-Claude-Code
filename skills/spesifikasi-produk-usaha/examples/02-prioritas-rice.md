# Contoh 2 - Urutan ide dengan skor (script asli, data fiktif)

**Pengguna:** "Ada 4 ide tambahan untuk teh serai: tanpa gula, paket 6 botol, langganan mingguan, botol mini 100 ml. Mana dulu?"
Agen menanyakan sekali jangkauan/dampak/keyakinan/usaha, lalu membuat `ide-teh-serai.csv` dan menjalankan:
`python3 scripts/prioritas.py --metode rice --csv examples/ide-teh-serai.csv`

```
Metode RICE - 4 ide dihitung, 0 bermasalah

| # | Ide | Skor | Tahap |
|---|---|---|---|
| 1 | Paket 6 botol (hemat) | 80,00 | Sekarang |
| 2 | Botol 100 ml (mini/sampel) | 67,50 | Sekarang |
| 3 | Varian tanpa gula | 46,67 | Berikutnya |
| 4 | Langganan mingguan | 12,50 | Nanti |
```
(4 ide dibagi 2/1/1 supaya tiap tahap terisi.)
Cek manual: paket = 600 x 0,5 x 0,8 / 3 = 80; mini = 300 x 0,5 x 0,9 / 2 = 67,5; tanpa gula = 400 x 1 x 0,7 / 6 = 46,67; langganan = 150 x 2 x 0,5 / 12 = 12,5.

**Penjelasan awam:** skor tinggi = banyak pembeli tersentuh, dampak besar, yakin, dan usahanya kecil. Paket 6 botol paling cepat menghasilkan. Langganan berdampak besar per orang tapi keyakinan hanya 50% dan usaha 12 hari: uji dulu lewat pre-order 10 orang sebelum dibangun.

Dengan kapasitas 10 orang-hari (`--kapasitas 10`) hasilnya sama: Sekarang = paket + mini (5 hari), Berikutnya = tanpa gula (6 hari), Nanti = langganan, dengan catatan script: "usaha lebih besar dari kapasitas per tahap; pecah jadi langkah kecil" (12 hari > 10). Agen menyarankan memecah langganan: mulai dari pre-order 10 orang (usaha kecil) dulu.

**Roadmap (hasil untuk pembeli):** Sekarang: pembeli bisa beli paket hemat dan mencoba ukuran mini. Berikutnya: pilihan tanpa gula. Nanti: langganan mingguan.
