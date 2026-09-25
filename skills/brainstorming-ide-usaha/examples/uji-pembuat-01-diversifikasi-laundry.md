# Uji Pembuat 01 — Diversifikasi Usaha Laundry (Jalur B)

Dibuat oleh pembuat skill sebagai contoh alur lengkap. **Bukan pengganti** pengujian independen Tahap 6 CLAUDE.md (agent/sesi terpisah, 5 skenario, uji A/B, uji banding pesaing).

## Permintaan awal pengguna

> "Usaha laundry saya sepi, ada ide tambahan produk/jasa nggak?"

## 1. Klasifikasi

Agent: "Ini kedengarannya produk/jasa tambahan untuk usaha yang sudah jalan, dengan modal & risiko kecil-menengah yang bisa dites minggu ini tanpa nambah karyawan/lokasi — saya proses sebagai **Jalur B (Perlu Diuji)**: gali dulu konteks & batasan, munculkan beberapa ide, saring dengan skor, lalu susun rencana uji dan aksi 7 hari. Kalau menurutmu ini ternyata lebih besar dari itu (mis. butuh modal jauh lebih besar atau lini usaha baru), bilang saja, saya naikkan ke Jalur C."

Pengguna: "Oke lanjut."

## 2. Gali konteks & batasan (ringkas; pada sesi asli ditanyakan dalam satu pesan berisi beberapa pertanyaan singkat sekaligus, sesuai Langkah B.1 SKILL.md v1.0.1)

- Usaha: laundry kiloan rumahan, jalan 1,5 tahun, area perumahan kelas menengah.
- Masalah: omzet turun ~20% dalam 2 bulan terakhir, kompetitor baru buka di dekat lokasi.
- Modal tambahan yang siap dipakai untuk coba ide baru: **Rp3.000.000**.
- Waktu: dikerjakan bersama 1 karyawan, ada waktu longgar 2–3 jam/hari di luar jam sibuk.
- SDM: pemilik + 1 karyawan, belum berencana rekrut lagi dalam waktu dekat.
- Lokasi: rumahan dengan etalase kecil di depan, area padat perumahan.
- Momentum: tidak mengejar momen tertentu, ingin solusi sepanjang waktu.

## 3. Tulis ulang pemahaman (dikirim ke pengguna untuk dikoreksi)

> "Jadi intinya: laundry kiloan yang sudah jalan 1,5 tahun, omzet turun karena ada kompetitor baru. Kamu punya modal tambahan sekitar Rp3 juta, waktu longgar 2–3 jam/hari bersama 1 karyawan, dan mau solusi yang bisa dites cepat tanpa nambah orang dulu. Berhasil = ada tambahan pemasukan yang menutup penurunan omzet itu. Betul begitu?"

Pengguna: "Betul."

## 4. Ide (teknik: SCAMPER + Gabung-Kombinasi, lihat references/teknik-ide-terstruktur.md)

- **S (Ganti):** Laundry khusus bayi (deterjen hipoalergenik) — beda dari kompetitor generik.
- **C (Gabung):** Member langganan bulanan (gabung beberapa layanan jadi paket tetap, hemat vs kompetitor per-kiloan).
- **M (Ubah/Perbesar):** Paket laundry kilat 3 jam — untuk yang butuh cepat, kompetitor belum tentu punya.
- **P (Alihkan kegunaan):** Laundry sepatu & tas — pakai mesin yang sudah ada di jam sepi.
- **Gabung-Kombinasi (aset lain):** Laundry karpet/gorden — perlengkapan yang jarang dicuci sendiri di rumah.

Setelah disaring bersama pengguna (buang ide yang perlu alat besar di luar modal Rp3 juta), tersisa 5 ide realistis di atas — dimasukkan ke `scripts/skor_ide.py`.

## 5. Skor tertimbang (dihitung script, bukan feeling)

Kriteria & bobot disepakati bersama pengguna (modal paling ketat karena baru habis untuk operasional, jadi bobot tertinggi):

```json
{
  "kesesuaian_modal": 5,
  "potensi_permintaan": 4,
  "kemudahan_eksekusi": 3,
  "kecocokan_keahlian": 2,
  "potensi_margin": 4
}
```

Perintah: `python3 scripts/skor_ide.py skor --ide ide-laundry.csv --bobot bobot-laundry.json`

Keluaran sebenarnya dari script:
```
Peringkat Nama Ide                                       Skor Tertimbang
------------------------------------------------------------------------
1         Member langganan bulanan                                 4.278
2         Paket laundry kilat 3 jam                                3.722
3         Laundry khusus bayi (deterjen hipoalergenik)             3.556
4         Laundry sepatu & tas                                     3.056
5         Laundry karpet/gorden                                    2.778

Bobot kriteria dipakai (total bobot = 18):
   - kesesuaian_modal: 5
   - potensi_permintaan: 4
   - kemudahan_eksekusi: 3
   - kecocokan_keahlian: 2
   - potensi_margin: 4
```
(Tidak ada skor seri pada data ini.)

## 6. Presentasi 2 ide teratas dengan untung-rugi

| Ide | Untung | Rugi/risiko |
|---|---|---|
| **Member langganan bulanan** (skor 4,28, #1) | Pemasukan lebih pasti tiap bulan, tidak butuh alat baru, cocok dijalankan pemilik+1 karyawan yang ada | Butuh promosi awal supaya orang mau komit bulanan; margin per transaksi individual sedikit lebih tipis |
| **Paket laundry kilat 3 jam** (skor 3,72, #2) | Bisa langsung jadi pembeda vs kompetitor baru, tidak butuh alat tambahan (pakai slot mesin di jam sepi) | Butuh disiplin jadwal ketat; kalau ramai bersamaan bisa telat dan mengecewakan pelanggan |

**Rekomendasi agent:** mulai dari **Member langganan bulanan** (skor tertinggi & risiko paling kecil untuk modal & SDM yang ada), dengan **laundry kilat 3 jam** sebagai ide cadangan kalau member langganan kurang diminati.

Pengguna: "Oke, coba member langganan bulanan dulu."

## 7. Rencana uji murah (MVP)

- **Cara uji:** tawarkan paket member bulanan (mis. 3x cuci-kering-lipat/bulan, harga tetap) via status WA + selebaran kecil di etalase depan ke pelanggan yang sudah pernah datang.
- **Durasi:** 1 minggu.
- **Target berhasil:** minimal 10 pelanggan mendaftar member dalam 1 minggu.
- **Kapan lanjut/berhenti:** ≥10 pendaftar (100%) → lanjut & promosikan lebih luas; 3–9 (30–99%) → perbaiki harga/isi paket, uji ulang 1 minggu lagi; <3 (<30%) → hentikan, coba ide #2 (laundry kilat 3 jam).
- **Biaya uji maksimal:** Rp300.000 (cetak selebaran kecil + pulsa promosi WA), jauh di bawah modal Rp3 juta yang disiapkan.

## 8. Rencana Aksi 7 Hari

| Hari | Tugas |
|---|---|
| 1 | Susun rincian paket member (harga, jumlah cuci/bulan, S&K) + cetak 30 selebaran kecil |
| 2 | Posting story WA + pasang selebaran di etalase, mulai tawarkan ke pelanggan yang datang |
| 3 | Follow up 10 pelanggan tetap terbaik lewat chat personal, tawarkan jadi member pertama |
| 4 | Catat jumlah pendaftar sejauh ini di buku/spreadsheet sederhana |
| 5 | Ulangi promosi ke pelanggan yang belum merespons hari 3 |
| 6 | Rekap total pendaftar & catat keluhan/pertanyaan yang sering muncul |
| 7 | Evaluasi vs target (10 pendaftar): putuskan lanjut, perbaiki, atau ganti ke ide cadangan |

## 9. Asumsi yang dipakai
Tidak ada default yang dipakai pada sesi ini — semua batasan (modal, waktu, SDM, lokasi, target) disebutkan langsung oleh pengguna.
