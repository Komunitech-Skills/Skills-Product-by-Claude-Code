# Contoh 3: input tidak lengkap (stok dan kisaran laku saja, tanpa lead time)

> Hasil uji penguji independen di OpenClaw 2026.10.2 (model claude-sonnet-5), 14 Okt 2026. Data fiktif. Jawaban SEBELUM (tanpa skill) dan penilaian lengkap ada di `00-openclaw-sebelum-sesudah.md`.

## Masukan pengguna
> stok tepung tinggal 20, sehari laku 3-5, kapan harus pesan?

Tanpa riwayat penjualan dan tanpa lead time.

## Keluaran di chat (SESUDAH, skill aktif)

> **Tepung — PESAN SEKARANG** (stok sudah di bawah titik aman)
>
> - Stok sekarang: 20
> - Rata-rata laku: ±4/hari (kisaran 3–5)
> - Perkiraan habis: ±5 hari (bisa 4 hari kalau laku lagi tinggi di 5/hari)
> - Titik pesan ulang (ROP) dengan asumsi lead time 7 hari, tingkat layanan 95%: ±32
> - Stok sekarang (20) **sudah di bawah** titik pesan ulang (32) → artinya seharusnya sudah dipesan dari beberapa hari lalu, bukan nanti.
> - Stok target setelah barang datang (cukup 14 hari ke depan): ±88
> - Perkiraan jumlah pesan: ±68 (sebelum disesuaikan isi per sak/kemasan dari pemasok)
>
> ⚠️ **Risiko:** kalau lead time pemasok memang 7 hari, tepung bisa habis sekitar 2 hari sebelum stok baru datang. Kalau bisa, pesan hari ini juga atau cari pemasok yang bisa kirim lebih cepat untuk kali ini.
>
> **Asumsi** (karena belum disebutkan): lead time pesan 7 hari, tingkat layanan 95%, stok dihitung cukup untuk 14 hari setelah barang datang. Dihitung manual dari kisaran laku yang Anda sebutkan, mohon dicek ulang kalau ada data penjualan harian yang lebih pasti.
>
> Biar lebih akurat, boleh dijawab 3 ini:
> 1. Lead time pemasok tepung sebenarnya berapa hari?
> 2. Tepung dijual per kg atau per sak? Kalau beli per sak isi berapa kg?
> 3. Ada harga beli per satuan, biar saya hitung juga nilai pesanannya?
>
> Catatan: perkiraan dari pola penjualan yang Anda sebutkan, bukan jaminan; cocokkan dengan stok fisik sebelum memesan.

## Catatan penguji
- Tetap bekerja dulu dengan default yang disebut (lead time 7 hari, layanan 95 %, 14 hari), lalu 3 pertanyaan.
- Cek manual: habis 20 ÷ 4 = 5 hari (4 hari bila 5/hari); ROP ≈ 4 × 7 + ±4 = ±32; target ≈ 4 × 21 + 4 = ±88; pesan ±68: konsisten.
- Kekurangan: baris hitungan & asumsi simpangan tidak ditunjukkan (SKILL.md meminta untuk fallback manual); pembulatan "±" bukan "ke atas" (33/89).
- Nilai: SEBELUM 7 → SESUDAH 8.
