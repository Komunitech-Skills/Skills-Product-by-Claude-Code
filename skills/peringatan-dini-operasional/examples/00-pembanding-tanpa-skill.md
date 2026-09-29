# Uji A/B — tanpa skill vs dengan skill (skenario 01, pabrik garmen 45 hari)

> Penguji independen, 2026-09-29, simulasi agent (`claude-code (simulasi agent)`). Input sama:
> `examples/uji-garmen-45hari.csv` + "Ini log produksi konveksi saya 45 hari terakhir, ada yang perlu
> diwaspadai? Pemasok kain butuh 3 hari."

## A. Tanpa skill (agent umum)
Agent umum biasanya membaca CSV dengan skrip cepat (`float()` / pandas default) lalu menulis ringkasan.
Penguji menjalankan pembacaan naif itu pada file yang sama:
- 14 dari 38 sel output bertitik ribuan (`1.271`, `1.225`) **terbaca 1,271** → rata-rata output
  "752 pcs" (aslinya ±1.200) dan output hari ini tampak "turun 99%".
- Stok kain `5.430` terbaca **5,43 m** → kesimpulan "stok kain habis hari ini".
- Tidak ada baris TARGET yang dipakai; Minggu "libur" dianggap baris kosong/nol di beberapa hitungan.

Jawaban khas (disusun penguji dari pola jawaban agent umum, dengan angka yang sudah dibaca benar
secara manual — yaitu kasus *terbaik* tanpa skill):
```
Beberapa hal yang perlu diwaspadai:
1. Reject naik dalam beberapa hari terakhir (31 → 52). Hari ini 52, melebihi target 40.
   Sebaiknya cek kualitas bahan dan kinerja operator.
2. Downtime hari ini 95 menit, jauh di atas biasanya (±25 menit). Cek mesin.
3. Stok kain tinggal 5.430 m, dengan pemakaian ±1.960 m/hari cukup sekitar 2-3 hari.
   Segera pesan karena pemasok butuh 3 hari.
4. Output relatif stabil di kisaran 1.150-1.290.
Saran: lakukan maintenance rutin, evaluasi operator, dan pantau terus datanya.
```

## B. Dengan skill
Lihat `01-uji-garmen-45-hari.md` (output lengkap siap kirim Telegram).

## Perbandingan
| Aspek | Tanpa skill | Dengan skill |
|---|---|---|
| Pembacaan angka Indonesia (`1.271`, `5.430`) | rawan salah baca 1000× (terbukti pada pembacaan naif) | benar, dicocokkan 84/84 dengan angka asli |
| Seberapa tidak normal | "jauh di atas biasanya" (kira-kira) | 6,4σ, +163% vs Selasa biasanya, +30% dari target — dihitung |
| Kapan mulai | "beberapa hari terakhir" | naik 4 hari beruntun; uji mundur: 🟠 sejak 25 Sep (3 hari sebelum lewat target) |
| Reject karena output naik? | tidak dicek | metrik % reject otomatis (4,24%, 4,6σ) |
| Stok | "2–3 hari" dari pemakaian 1 hari | 2,8 hari dari rata 7 hari, dibandingkan lead time → 🔴 "pesan HARI INI" |
| Pencilan lama (listrik padam 4 Sep) | ikut rata-rata / tidak disebut | dibuang dari garis dasar & disebut |
| Hari libur | kadang dihitung 0 | tidak diisi tebakan, disebut |
| Tindak lanjut | saran umum ("evaluasi operator") — condong menyalahkan orang | pertanyaan cek 4M + 5 kenapa, "bukan cari kambing hitam" |
| Siap kirim | paragraf panjang | ±30 baris, emoji warna, siap Telegram/jadwal harian |
| Kejujuran | tanpa disclaimer | "peringatan statistik, bukan kepastian" |

**Kesimpulan A/B:** dengan skill jelas lebih baik — terutama pada ketepatan membaca angka, ukuran
seberapa serius, deteksi *dini* (sebelum target dilanggar), dan format siap kirim. Pada kasus yang
sudah sangat jelas (reject lewat target) agent tanpa skill juga menangkap masalah utamanya; nilai
tambah terbesar skill ada pada deteksi lebih awal (uji 02: 🟠 pada 22 Sep ketika telat kirim baru 9
dan masih jauh di bawah target 15 — agent tanpa skill cenderung menyebut "masih aman, di bawah target").
