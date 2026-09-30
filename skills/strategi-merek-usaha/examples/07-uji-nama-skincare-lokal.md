# Uji 07 (normal 2): Nama produk skincare lokal + klaim berisiko

> Uji independen 2026-09-30. Angka script diverifikasi ulang oleh penguji (10/10 sama).

**Input pengguna:** "Saya mau bikin brand serum niacinamide buatan Bandung, target cewek 20-30 tahun, jual di Shopee & TikTok Shop. Kasih nama brand. Tagline saya: 'Cerah dalam 7 hari, 100% aman, sudah BPOM'. Merek yang saya tahu: Wardah, Somethinc, Scarlett, Skintific, Emina, Azarine, Sariayu, Avoskin, Whitelab, Glad2Glow."

## Mode chat (ringkas)
**3 nama teratas (skor script, bukan bukti tersedia):**
1. **Seulas** — 91/100 (SETARA dengan no. 2)
2. **Rona Sunda** — 87/100
3. **Geulis Lab** — 86/100 ("geulis" = cantik dalam bahasa Sunda; **perlu ditanyakan ke penutur asli** apakah pas untuk merek)

Ditandai, jangan dipakai: **Somethinc Glow** (mirip Somethinc), **Sari Ayu Bandung** (mirip Sariayu).
"Lumi Kasep": "kasep" = tampan (untuk laki-laki) dalam bahasa Sunda, kurang cocok untuk target perempuan (aman_makna 3; konfirmasi ke penutur asli).

**Tagline kamu perlu diubah dulu:**
| Tertulis | Masalah | Versi jujur |
|---|---|---|
| "Cerah dalam 7 hari" | Janji hasil dengan waktu pasti; tidak semua kulit sama (UU 8/1999 Pasal 9 ayat 1: janji yang belum pasti) | "Serum niacinamide [isi: %] untuk rutinitas kulit tampak lebih cerah" (hanya bila sesuai klaim yang disetujui di notifikasi BPOM) |
| "100% aman" | Kata berlebihan "aman" tanpa keterangan lengkap (Pasal 9) | "Sudah uji [isi: jenis uji, mis. patch test/dermatologis] — lakukan tes di lengan dulu" |
| "sudah BPOM" | Klaim izin harus bisa dibuktikan | "Notifikasi BPOM: [isi: nomor NA...]" — cek sendiri di cekbpom.pom.go.id |

**Yang perlu kamu cek sendiri:** domain/IG/TikTok/nama toko Shopee untuk 3 nama; PDKI kelas **3** (kosmetik). Bila produk diposisikan sebagai obat/berkhasiat medis, kelas berbeda (tanya konsultan KI).
Mau versi lengkap? Balas: lengkap.

## Hasil script
`python3 scripts/skor_nama.py skin.csv --merek "Wardah, Somethinc, Scarlett, Skintific, Emina, Azarine, Sariayu, Avoskin, Whitelab, Glad2Glow"`
```
 1  Seulas                    91.0      6    3  layak dicek
 2  Rona Sunda                87.0      9    4  layak dicek
 3  Geulis Lab                86.0      9    4  layak dicek
 4  Kulitku                   85.0      7    3  layak dicek
 5  Embun Pagi                83.0      9    4  layak dicek
 6  Bening Kita               80.0     10    4  layak dicek
 7  Lumi Kasep                79.0      9    4  layak dicek
 8  Cahaya Priangan           77.0     14    6  layak dicek
 9  Somethinc Glow            58.0     13    4  TANDAI: terlalu mirip 'Somethinc'
10  Sari Ayu Bandung          52.0     14    6  TANDAI: terlalu mirip 'Sariayu'
SETARA: 'Seulas' dan 'Rona Sunda' selisih <= 5 poin.
```

## Penilaian penguji
- Baik: TANDAI menangkap dua nama yang menempel merek besar; klaim "100% aman/BPOM/7 hari" diganti versi jujur sesuai `references/kata-dan-klaim.md`; tidak mengarang nomor BPOM (`[isi: ...]`).
- Temuan kecil: suku kata bahasa Sunda "eu" dihitung dua ("Seulas" dihitung 3, lazimnya 2 suku kata: seu-las). Tidak mengubah peringkat di kasus ini, tapi dokumentasi hanya menyebut diftong ai/au/oi.
- Temuan kecil: "Kulitku" (khas = 1, sangat generik) tetap di peringkat 4 dengan 85/100. Bobot `khas` 15% membuat nama generik bisa tetap tinggi; agent perlu menyebutnya (SKILL tidak mewajibkan).
- Tabel kelas Nice skill memuat kelas 3 (benar). Kelas 5 (produk berkhasiat obat) dan 44 (klinik/salon kecantikan) tidak ada di tabel.
