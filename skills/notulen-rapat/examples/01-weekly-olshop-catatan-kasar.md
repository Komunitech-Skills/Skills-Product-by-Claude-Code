# Contoh 01 – Rapat mingguan online shop dari catatan kasar

## Skenario
S1, permintaan normal. Pemilik online shop menempel catatan rapat mingguan yang diketik cepat. Isinya campuran: keputusan tegas ("deal", "oke"), usulan yang belum final ("kayaknya", "nanti diitung dulu"), tugas dengan tenggat relatif ("besok", "jumat depan", "kamis"), dan tugas tanpa pelaksana ("nanti ada yang cek"). Skill harus memisahkan semuanya tanpa mengarang dan mengonversi tanggal dengan script. Semua nama fiktif.

## Input pengguna
```
tolong rapihin jadi notulen ya

weekly meeting olshop Rumah Rajut Nadia, selasa 22 sept 2026 jam 10-11 via gmeet.
hadir: nadia (owner), bima (admin), tari (cs), yoga (gudang). rini ga ikut, cuti.
1. evaluasi sept: omzet s/d 20 sept 38jt, target 50jt. bima bilang ads shopee boros, ROAS cuma 3.
2. promo 10.10: tari usul diskon 15% semua produk. nadia bilang kayaknya 10% aja biar margin aman, nanti diitung dulu.
3. retur bulan ini 12, kebanyakan salah ukuran. deal: tambah tabel ukuran (cm) di semua listing. bima yg update listing, paling lambat jumat depan.
4. yoga minta rak gudang tambahan, nadia oke, budget max 2jt. yoga cari vendor rak, kasih penawaran kamis.
5. tari bikin template balasan chat utk pertanyaan ukuran, besok.
6. ads perlu dicek ulang settingannya, nanti ada yg cek.
rapat berikutnya selasa depan jam 10.
```

## Proses (dijalankan agent)
```
$ python3 scripts/tanggal_relatif.py --rapat "22-09-2026" --ekspresi "besok" "jumat depan" "kamis" "selasa depan" --format teks
Tanggal rapat: Selasa, 22 September 2026
- "besok" -> Rabu, 23 September 2026 [pasti]
- "jumat depan" -> Jumat, 2 Oktober 2026 [ambigu] | alternatif: Jumat, 25 September 2026 | 'Depan' bisa berarti minggu berikutnya atau hari terdekat. Mohon dikonfirmasi.
- "kamis" -> Kamis, 24 September 2026 [pasti]
- "selasa depan" -> Selasa, 29 September 2026 [pasti]
```

## Output

# NOTULEN RAPAT
**Rapat Mingguan Tim Rumah Rajut Nadia**

| | |
|---|---|
| Hari, tanggal | Selasa, 22 September 2026 |
| Waktu | pukul 10.00–11.00 WIB |
| Tempat/platform | Google Meet |
| Pemimpin rapat | Nadia (Owner) (disimpulkan) |
| Notulis | [isi] |
| Peserta | Nadia (Owner), Bima (Admin), Tari (CS), Yoga (Gudang) (4 orang) |
| Tidak hadir | Rini (cuti) |

## Agenda
1. Evaluasi penjualan September
2. Promo 10.10
3. Retur karena salah ukuran
4. Rak gudang tambahan
5. Template balasan chat pertanyaan ukuran
6. Pengaturan iklan (ads) Shopee

## Pembahasan
### 1. Evaluasi penjualan September
- Omzet sampai 20 September 2026: Rp 38.000.000. Target bulan ini Rp 50.000.000.
- Bima: biaya iklan Shopee dinilai boros, ROAS hanya 3.

### 2. Promo 10.10
- Tari mengusulkan diskon 15% untuk semua produk.
- Nadia: "kayaknya 10% aja biar margin aman", tetapi akan dihitung dulu. ⚠️ belum jelas apakah disepakati.

### 3. Retur karena salah ukuran
- Retur bulan ini 12 pesanan, sebagian besar karena salah ukuran.
- Disepakati menambahkan tabel ukuran (cm) di semua listing.

### 4. Rak gudang tambahan
- Yoga meminta rak gudang tambahan. Nadia menyetujui dengan anggaran maksimal Rp 2.000.000.

### 5. Template balasan chat
- Tari akan membuat template balasan untuk pertanyaan ukuran.

### 6. Pengaturan iklan Shopee
- Pengaturan iklan perlu dicek ulang. Pelaksana belum ditentukan.

## Keputusan
1. Tabel ukuran (cm) ditambahkan di semua listing produk.
2. Pengadaan rak gudang tambahan disetujui, dengan anggaran maksimal Rp 2.000.000.

## Action Items
| No | Tugas | PIC | Tenggat | Status |
|---|---|---|---|---|
| 1 | Membuat template balasan chat untuk pertanyaan ukuran | Tari | Rabu, 23 September 2026 ("besok") | Belum mulai |
| 2 | Mencari vendor rak dan menyampaikan penawaran | Yoga | Kamis, 24 September 2026 ("kamis") | Belum mulai |
| 3 | Memperbarui semua listing dengan tabel ukuran (cm) | Bima | Jumat, 2 Oktober 2026 ("jumat depan") ⚠️ | Belum mulai |
| 4 | Menghitung besaran diskon promo 10.10 (10% vs 15%) | ⚠️ belum ditentukan | ⚠️ belum ada tenggat | Belum mulai |
| 5 | Mengecek ulang pengaturan iklan Shopee | ⚠️ belum ditentukan | ⚠️ belum ada tenggat | Belum mulai |

## Belum diputuskan / dibahas di rapat berikutnya
- Besaran diskon promo 10.10: usulan 15% (Tari) vs 10% (Nadia). Menunggu hitungan margin.

## Perlu dikonfirmasi
- **"Jumat depan"** untuk update listing diartikan **Jumat, 2 Oktober 2026**. Jika yang dimaksud Jumat terdekat, tenggatnya **Jumat, 25 September 2026**.
- Siapa yang menghitung diskon 10.10, dan kapan hasilnya dibutuhkan? Promo jatuh 10 Oktober, jadi keputusan perlu diambil sebelum itu.
- Siapa yang mengecek pengaturan iklan Shopee, dan kapan?
- Notulis rapat ini siapa?

Rapat berikutnya: Selasa, 29 September 2026, pukul 10.00 WIB ("selasa depan").

---
## Pesan untuk grup WhatsApp
```
*Ringkasan Rapat Mingguan — Selasa, 22 Sep 2026*
✅ Keputusan:
1. Tabel ukuran (cm) ditambahkan di semua listing
2. Rak gudang tambahan disetujui, budget maks *Rp 2.000.000*
📌 Tugas:
• @Tari: template balasan chat soal ukuran, *Rabu, 23 Sep*
• @Yoga: penawaran vendor rak, *Kamis, 24 Sep*
• @Bima: update tabel ukuran di listing, *Jumat, 2 Okt* (atau 25 Sep? mohon konfirmasi)
❓ Belum diputuskan: diskon 10.10 (10% atau 15%), dan siapa yang cek setting ads Shopee.
Rapat berikutnya: *Selasa, 29 Sep, pukul 10.00*. Terima kasih semua 🙏
```

Mau dibuatkan versi email, atau pengingat tenggat untuk tiap orang?

## Catatan penguji
- **Script dijalankan sungguhan.** "jumat depan" berstatus `ambigu` dan dimasukkan ke "Perlu dikonfirmasi" beserta alternatifnya, sesuai langkah 5. **Verifikasi independen:** 23/9 = Rabu, 24/9 = Kamis, 25/9 dan 2/10 = Jumat, 29/9 = Selasa (dicek `datetime`). Aturan script juga diuji dengan brute force untuk 14 hari rapat × 7 nama hari × 2 bentuk ("<hari>" dan "<hari> minggu depan") + besok/lusa/N hari/akhir bulan: 0 selisih dari aturan yang tertulis di docstring.
- **Bagus (inti skill):** usulan diskon **tidak** ditulis sebagai keputusan (penanda lemah "kayaknya", "nanti diitung dulu"). "Deal" dan "nadia oke" dijadikan keputusan (penanda kuat). "Nanti ada yg cek" menjadi `PIC: ⚠️ belum ditentukan`. Angka disalin persis (38 juta, 50 juta, ROAS 3, 12 retur, 2 juta).
- **Bagus:** action items diurutkan dari tenggat terdekat. Pesan WA 80 kata (≤ 120), tanpa tabel, dengan mention dan tenggat.
- **Catatan:** action item 4 ("menghitung diskon") disimpulkan dari "nanti diitung dulu", dengan PIC dan tenggat ⚠️. Ini masih setia pada catatan: tugasnya tersirat, tetapi PIC tidak ditebak (tidak menulis "Nadia" walau ia yang berkata "nanti diitung dulu").
- **Kurang (ringan):** SKILL.md meminta rupiah `Rp 150.000` (dengan spasi). Ini tidak konsisten dengan skill `surat-resmi` yang memakai `Rp1.500.000,00` (EYD V). Untuk notulen internal tidak masalah, tapi sebaiknya satu gaya di seluruh library, atau disebut alasannya.
