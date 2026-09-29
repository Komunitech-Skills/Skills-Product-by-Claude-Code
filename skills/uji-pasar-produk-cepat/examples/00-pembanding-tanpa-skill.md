# Uji A/B: tanpa skill vs dengan skill (skenario normal 1)

> Dibuat oleh penguji independen (2026-09-29). Contoh fiktif. Angka "dengan skill" = keluaran asli `scripts/hasil_eksperimen.py`; semua angka diverifikasi ulang dengan hitungan penguji sendiri (lihat HASIL-UJI.md).

**Input pengguna (sama untuk keduanya):**
"Saya jual nastar premium toples 500 g Rp95.000, HPP sekitar Rp58.000. Mau tes pre-order Lebaran. Sudah kirim penawaran ke 120 kontak WA pelanggan (sebagian keluarga), 21 orang transfer DP Rp30.000. Target saya 15%. Lanjut produksi 300 toples?"

---

## A. Tanpa skill (jawaban agent umum)

> Selamat, hasilnya bagus! 21 dari 120 = **17,5%**, di atas target 15%. Artinya minat pasar cukup tinggi.
> Margin Anda (95.000 - 58.000) / 95.000 = 39%, sehat.
> Saran:
> 1. Lanjutkan produksi, tapi mulai bertahap, misalnya 150 toples dulu lalu tambah jika laris.
> 2. Promosikan lewat Instagram dan marketplace untuk menjangkau lebih banyak pembeli.
> 3. Kumpulkan testimoni dari pembeli pertama.
> 4. Perhatikan kemasan agar tidak rusak saat dikirim.
> Semoga sukses!

Catatan penguji: angka konversi & margin benar, tetapi (1) tidak ada rentang ketidakpastian, (2) tidak menyadari bahwa 300 toples butuh sekitar 1.700 kontak dengan konversi 17,5%, (3) angka "150 toples" dikira-kira tanpa dasar, (4) bias kontak keluarga tidak dibahas, (5) tidak ada kriteria/log untuk putaran berikutnya.

## B. Dengan skill `uji-pasar-produk-cepat`

```
$ python3 scripts/hasil_eksperimen.py hasil --ditawari 120 --aksi 21 --target 15
Konversi: 21 dari 120 orang = 17,5%
Rentang wajar 95% (Wilson): 11,7% sampai 25,3%
Artinya: dengan data ini, angka sebenarnya kemungkinan besar ada di antara 12% dan 25%.
Kriteria (ditetapkan SEBELUM uji): lanjut jika >= 15,0%, stop jika < 7,5%.
KEPUTUSAN: LANJUT BERTAHAP: angka mencapai target, tapi batas bawah rentang (11,7%) masih di bawah target. Lanjut bertahap kecil (mis. produksi batch kecil) atau tambah sampel dulu.
```

**Hasil & keputusan (bahasa awam):** 21 dari 120 kontak (17,5%) sudah bayar DP, melewati target 15%. Tapi dengan 120 orang, angka sebenarnya bisa di mana saja antara sekitar 12% dan 25%, jadi keputusannya **LANJUT BERTAHAP**: produksi bertahap, belum 300 toples.

**Kenapa belum 300:** untuk 300 toples dengan konversi 17,5% Anda perlu menawari sekitar 300 ÷ 0,175 = **1.715 orang**; kalau konversi sebenarnya di batas bawah (11,7%), sekitar **2.565 orang**. Kontak Anda baru 120.

**Margin:** (95.000 - 58.000) ÷ 95.000 = 38,9% per toples (belum termasuk ongkir/kemasan kirim; cek dengan `hitung-hpp`).

**Catatan bias:** sebagian yang ditawari keluarga. Pisahkan hitungan keluarga vs pelanggan biasa; kalau DP keluarga dikeluarkan, hitung ulang dengan script.

**Langkah berikutnya:**
1. Produksi sesuai 21 pesanan + cadangan kecil.
2. Putaran 2: tawarkan ke 100 kontak/pelanggan baru (bukan keluarga), kriteria dikunci sama (lanjut >= 15%, stop < 7,5%, tenggat 5 hari).
3. Asumsi berikutnya: nastar tetap utuh saat dikirim (kirim 5 paket uji ke luar kota).

**Baris log:** `#1 | 2026-09-29 | minat+harga | PO WA | 120 | 21 | 17,5% | LANJUT BERTAHAP`

Asumsi: target 15% ditetapkan sebelum uji; batas stop default 7,5% (setengah target).

---

## Penilaian
| Aspek | Tanpa skill | Dengan skill |
|---|---|---|
| Angka konversi & margin | Benar | Benar |
| Ketidakpastian (rentang wajar) | Tidak ada | Wilson 11,7%-25,3% (terverifikasi) |
| Jawaban atas "300 toples?" | Dikira "150 dulu" | Dihitung: butuh ±1.715-2.565 kontak |
| Bias kontak keluarga | Tidak dibahas | Dibahas + cara koreksi |
| Kriteria & log putaran berikut | Tidak ada | Ada, siap salin |

**Kesimpulan: dengan skill jelas lebih baik.** Catatan: perhitungan "butuh 1.715 kontak" dilakukan agent (penguji) dari hasil script; SKILL.md belum secara eksplisit menyuruh menerjemahkan konversi ke jumlah kontak yang dibutuhkan (lihat permintaan perbaikan).
