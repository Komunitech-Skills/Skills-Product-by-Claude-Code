# Contoh 2 — Jasa Laundry Sepatu

**Input pengguna:**
> "Saya mau buka jasa laundry sepatu di rumah, worth it enggak ya sebelum saya sewa tempat & beli alat lengkap? Saya punya IG dengan sekitar 400 follower (rata-rata story dilihat 120-an), dan ada warung fotokopi teman deket kampus yang mau dititipi flyer."

**Jawaban pengguna atas pertanyaan harga** *(data fiktif yang dimasukkan pengguna untuk contoh)*:
> "Rencana harga Rp35.000 per pasang."

**Input lanjutan pengguna setelah 7 hari** *(data fiktif yang dimasukkan pengguna untuk contoh)*:
> "Story dilihat 118 orang, 9 vote 'Ya, mau!' tapi hanya 6 yang lanjut DM serius. Warung fotokopi: ±35 orang lewat (estimasi pemilik warung), 2 DM masuk dari flyer. Yang jawab 'nanti dulu' bilang 'Rp35rb kemahalan buat cuci sepatu sendiri, biasanya cuma perlu sikat cepat' dan 'gak tahu berapa lama prosesnya'."

## 1. Hipotesis
> "Kami percaya **mahasiswa/anak kos di sekitar kampus yang sepatunya kotor tapi malas cuci sendiri** mau membayar **Rp35.000/pasang** untuk **jasa cuci sepatu (ambil-antar area kampus)** karena bisa **hemat waktu & sepatu jadi bersih tanpa ribet**. Kami akan tahu ini benar jika minimal 15% dari yang ditawari benar-benar order dalam 7 hari."

## 2. Metode uji terpilih
Gabungan **polling story Instagram** (400 follower, cukup di atas ambang 100) + **titip flyer di warung fotokopi** dekat kampus. Dihitung **gabung total** (disepakati dengan pengguna karena keduanya sama-sama menyasar audiens kampus).

## 3. Kriteria lulus/gagal
Harga Rp35rb tergolong menengah (bukan impulsif, bukan mahal) → pakai ambang default 15%/8%. Minimal ditawari 20 — target realistis karena rata-rata views story 120 + estimasi ~40 orang lewat warung fotokopi selama seminggu.

## 4. Pesan yang dipakai
Story IG:
```
Lagi mikir mau buka jasa laundry sepatu (ambil-antar area kampus) 🤔
Cuci bersih, sepatu wangi, gak perlu repot cuci sendiri
Harga rencana: Rp35.000/pasang

Kalau ada, kamu bakal pakai? [Ya, mau! / Nanti dulu]

(DM aku kalau mau coba duluan pas udah buka 😊)
```
Flyer di warung fotokopi memakai pitch titip warung yang disesuaikan jadi ajakan DM IG.

## 5. Hasil setelah 7 hari
*(Angka dari input lanjutan di atas: data fiktif untuk contoh.)* Story dilihat 118 orang, 9 vote "Ya, mau!", 6 di antaranya lanjut DM serius. Warung fotokopi: ~35 orang lewat (estimasi pemilik warung), 2 DM masuk dari flyer. **Belum ada satu pun yang transfer/DP** — story dan flyer hanya mengajak DM, tidak membuka PO berbayar.

Sesuai Aturan Hitung (Langkah 2), vote dan DM tanpa bayar = **minat**, bukan pesanan. Kedua kanal hanya menghasilkan minat, jadi dihitung dengan mode `kanal` (`data-uji.json`):

```json
{"harga": 35000,
 "kanal": [{"nama": "Polling story IG", "ditawari": 118, "minat": 9},
           {"nama": "Flyer warung fotokopi", "ditawari": 35, "minat": 2}]}
```

```
$ python3 scripts/hitung_validasi.py --file data-uji.json
=== HASIL VALIDASI IDE ===
Yang dihitung sebagai pesanan: HANYA pre-order yang sudah transfer/DP/bayar atau order masuk.

Per kanal:
  - Polling story IG: ditawari 118, minat 9 (7.6%, BUKAN pesanan)
  - Flyer warung fotokopi: ditawari 35, minat 2 (5.7%, BUKAN pesanan)

Pesanan berkomitmen : 0 (belum ada kanal dengan pre-order/DP/bayar)
Sinyal minat        : 11 (vote/like/komentar — TIDAK dihitung sebagai pesanan)
Klasifikasi         : BELUM BISA DINILAI
Saran               : Minat belum sama dengan membeli. Ubah minat jadi pesanan dulu: buka pre-order dengan DP/transfer ke yang vote/komentar, lalu hitung ulang.
```

Ringkas: pesanan (sudah DP) **0 dari 153** ditawari; minat 11 (9 vote IG — 6 di antaranya DM — + 2 DM dari flyer) dilaporkan terpisah dan tidak dihitung sebagai pesanan.

Alasan yang sempat ditanyakan ke beberapa yang menjawab "nanti dulu": mayoritas bilang "Rp35rb kemahalan buat cuci sepatu sendiri, biasanya cuma perlu sikat cepat" dan "gak tahu berapa lama prosesnya" (masalah kejelasan, bukan cuma harga).

> **Catatan penguji:** dihitung ulang 2026-10-13 sesuai aturan DP. Versi sebelumnya menghitung 6 + 2 "DM serius" sebagai pre-order (8/153 = 5,2% → GAGAL), padahal belum ada yang transfer/DP. Dengan hanya pesanan ber-DP: 0 pesanan, 11 minat → **BELUM BISA DINILAI**.

## 6. Keputusan
**BELUM BISA DINILAI** — jangan sewa tempat atau beli alat lengkap dulu, tapi juga jangan langsung hentikan: datanya baru minat. Langkah berikut: ubah minat jadi pesanan. Hubungi 8 orang yang sudah DM (6 dari IG + 2 dari flyer) dan unggah ulang story dengan tawaran **PO berbayar** (DP atau bayar di muka, kebijakan batal/refund ditulis jelas), sekaligus jawab alasan penolakan: tambahkan info "estimasi selesai 1x24 jam, ambil-antar area kampus". Setelah 7 hari, hitung ulang dengan `--preorder` = jumlah yang sudah DP saja.

> Ilustrasi (bukan hasil): andai setelah PO berbayar konversi pesanan = 10% → **LULUS BERSYARAT**. Karena alasan penolakan dominan soal harga, UBAH satu variabel dulu (mis. harga perkenalan Rp25.000), uji ulang 7 hari dengan hipotesis baru. Jangan ubah target pembeli sekaligus — supaya jelas variabel mana yang memperbaiki hasil.
