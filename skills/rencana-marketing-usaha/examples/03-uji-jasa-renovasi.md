# Uji 03 — Skenario normal: jasa renovasi rumah (B2C, tiket besar)

> Uji simulasi oleh agent penguji independen, 2026-09-29. Usaha fiktif. Angka dari `scripts/alokasi_anggaran.py` (diverifikasi independen).

**Permintaan pengguna:**
"Saya kontraktor renovasi rumah di Depok (dapur, kamar mandi, tambah kamar). Rata-rata nilai proyek 35 juta, modal material + tukang ± 26,5 juta. Survei & bikin RAB keluar biaya sekitar 250 ribu per kunjungan, biasanya 1 dari 4 survei yang jadi. Sekarang dapat proyek 5 per bulan, hampir semua dari mulut ke mulut. Budget promosi 5 juta per bulan. Mau rencana marketing Okt-Des, target 20 proyek."

**Perilaku agent:** data wajib lengkap. Agent memasukkan biaya survei yang gagal ke biaya per proyek: 4 survei x Rp 250.000 = **Rp 1.000.000 per proyek jadi** (dijelaskan ke pengguna). Tanpa langkah ini margin akan terlihat lebih besar dari aslinya.

---

# Rencana Marketing Renovasi Rumah — Oktober-Desember 2026

Disusun: 29 Sep 2026 | **Asumsi:** nilai proyek rata-rata Rp 35 jt, biaya langsung Rp 26,5 jt, biaya survei per proyek jadi Rp 1 jt (1 dari 4 survei jadi), laba target setelah marketing Rp 3 jt/proyek (usulan agent, konfirmasi), tanpa pembelian ulang dalam kuartal. Tenaga marketing: pemilik 4 jam/minggu + admin.

## 0. Ringkasan
- Tujuan: 15 -> **20 proyek** tertandatangani (kontrak + DP) Okt-Des 2026 (omzet ± Rp 700 jt).
- Segmen: pemilik rumah 30-50 th di Depok & sekitar, rumah 5-20 tahun, ingin renovasi dapur/kamar mandi sebelum Lebaran 2027.
- Kanal utama (3): Google Ads penelusuran + Google Maps/ulasan, program referral pelanggan & mandor, konten foto/video sebelum-sesudah proyek asli.
- Anggaran Rp 15.000.000, cadangan eksperimen Rp 1.500.000.
- Batas biaya per proyek dari marketing: impas Rp 7,5 jt, target Rp 4,5 jt. **Ini batas atas, bukan perkiraan biaya.**
- Minggu ini: minta ulasan Google dari 10 klien lama, foto 5 proyek selesai, pasang formulir "tahu dari mana?" di RAB.

## 1. Kondisi sekarang
| Hal | Kondisi | Data |
|---|---|---|
| Proyek per bulan | 5 (hampir semua referensi) | Pemilik |
| Margin | Rp 7,5 jt/proyek (21,4%) setelah biaya survei | Script |
| Tingkat jadi survei | 25% | Pemilik |
| Kanal jalan | Mulut ke mulut; Google Maps belum dikelola | — |

## 2. Tujuan SMART
| Tujuan | Awal | Target | Tenggat | Ukur |
|---|---|---|---|---|
| Proyek kontrak + DP | 15/kuartal | 20 | 31 Des | Buku kontrak |
| Permintaan survei | ± 20/bulan | 27/bulan | Des | Catatan chat WA |
| Ulasan Google | cek | +25 ulasan asli | 31 Des | Google Business |

## 3. Target pasar
Pemilik rumah tapak 30-50 th di Depok, Cinere, Cibubur; masalah: takut kontraktor kabur/molor/biaya membengkak. Momen: bonus akhir tahun, persiapan Lebaran (renovasi harus selesai H-30), musim hujan (bocor). Tempat: Google ("renovasi kamar mandi Depok"), Maps, grup FB/WA perumahan, rekomendasi tetangga.

## 4. Pesan kunci
Janji: **"Renovasi dapur & kamar mandi dengan RAB tertulis, jadwal jelas, dan garansi pekerjaan."** Bukti: foto sebelum-sesudah proyek asli (izin pemilik, tanpa alamat), ulasan Google, contoh RAB, garansi tertulis (isi sesuai kebijakan nyata). Ajakan: "Chat WA untuk jadwal survei." Jangan klaim "termurah" atau "pasti selesai 7 hari".

## 5. Kanal
| Kanal | Peran | Alasan | Pemilik | Jam/minggu |
|---|---|---|---|---|
| Google Ads penelusuran + Maps | Kenal + Tertarik | Orang yang mencari "renovasi ... Depok" sedang butuh | Pemilik | 1,5 |
| Referral pelanggan & mandor | Rekomendasi | Kanal yang sudah terbukti (70% usaha datang dari sini); beri komisi tertulis, mis. Rp 500 rb per proyek jadi | Pemilik | 1 |
| Konten sebelum-sesudah (IG, FB grup perumahan) | Tertarik | Mengurangi takut; bahan iklan & RAB | Admin | 1,5 |
Follow-up calon klien setelah survei -> `pengingat-follow-up`; penawaran/RAB -> `surat-penawaran-harga`.

## 6. Kalender
| Minggu | Momen | Kegiatan | Kanal |
|---|---|---|---|
| 1-2 Okt | Persiapan | Lengkapi Maps, minta ulasan klien lama, siapkan kartu referral | Maps, WA |
| Okt | Musim hujan mulai | Konten "cek atap & talang sebelum hujan", iklan kata kunci bocor/atap | Google Ads |
| Nov | Bonus akhir tahun | Konten "renovasi dapur sebelum Natal/Lebaran" | Konten, Ads |
| Des | Persiapan Lebaran 2027 | "Pesan jadwal Jan-Feb sekarang"; kuota proyek | WA, Ads |
Lebaran 2027 diperkirakan sekitar Maret 2027 — **pastikan ke SKB libur nasional**.

## 7. Anggaran (keluaran script)
```
ANGGARAN Rp 15.000.000 untuk 3 bulan
- Google Ads (penelusuran): Rp 5.400.000 total (36.0% dari anggaran), ~Rp 1.800.000/bulan
- Google Maps & ulasan: Rp 2.025.000 total (13.5% dari anggaran), ~Rp 675.000/bulan
- Referral & mandor: Rp 3.375.000 total (22.5% dari anggaran), ~Rp 1.125.000/bulan
- Konten foto sebelum-sesudah: Rp 2.700.000 total (18.0% dari anggaran), ~Rp 900.000/bulan
- Cadangan eksperimen (10%): Rp 1.500.000
Cek: jumlah semua = anggaran (OK).
```

## 8. Target angka (keluaran script)
```
Harga jual Rp 35.000.000 | HPP Rp 26.500.000 | biaya platform Rp 0 | biaya/pesanan Rp 1.000.000
Margin kontribusi per pesanan: Rp 7.500.000 (21.4%)  STATUS: AMAN
- CAC titik impas (pesanan pertama): Rp 7.500.000
- ROAS titik impas: 4.67
- CAC target: Rp 4.500.000
- ROAS target: 7.78
- Pesanan dari iklan: 1
- Pesanan dibutuhkan untuk target omzet: 20
- Anggaran iklan maks (impas): Rp 150.000.000
```
Cara membaca (penting untuk jasa bernilai besar):
- "Pesanan dari iklan: 1" berarti Google Ads Rp 5,4 jt **cukup menghasilkan 1 proyek** untuk sesuai target laba. Itu syarat minimum, bukan perkiraan.
- "Anggaran iklan maks Rp 150 jt" adalah batas teoretis bila **semua** 20 proyek dari iklan; jangan dibaca sebagai saran belanja. Rencana ini tetap Rp 15 jt.
- Margin 21,4% tergolong tipis untuk iklan berbayar besar (referensi kanal menyarankan ≥ 25%): mulai kecil dan utamakan referral.

Corong (asumsi, ganti dengan data): untuk 20 proyek
```
Target 20 pesanan -> perlu 2000 di awal corong (Klik)
- Klik -> Chat: konversi 10% -> butuh 2000 untuk dapat 200
- Chat -> Survei: konversi 40% -> butuh 200 untuk dapat 80
- Survei -> Deal: konversi 25% -> butuh 80 untuk dapat 20
```
Karena 15 proyek biasanya datang dari referensi, iklan hanya perlu menutup ± 5 proyek -> ± 500 klik; cek biaya per klik di Google Ads.

## 9. KPI & aturan
| Tahap | KPI | Target | Aturan |
|---|---|---|---|
| Tertarik | Chat WA baru dari iklan | 50/kuartal | — |
| Beli | Survei -> kontrak | ≥ 25% | Bila < 15% 1 bulan: perbaiki RAB/penawaran |
| Beli | Biaya iklan per proyek | ≤ Rp 4,5 jt | Hentikan kata kunci bila 2 bulan biaya/proyek > Rp 7,5 jt |
| Rekomendasi | Proyek dari referral | 12 | Komisi dibayar setelah pelunasan |

## 10. Risiko
| Risiko | Tanda | Tindakan |
|---|---|---|
| Banyak survei tidak jadi | Tingkat jadi turun | Kualifikasi anggaran lewat chat sebelum survei |
| Kapasitas tukang penuh | Jadwal molor | Batasi kuota proyek; tawarkan jadwal Januari |

## 11. Keputusan terbuka
Konfirmasi laba target Rp 3 jt/proyek; besaran komisi referral; garansi yang benar-benar diberikan.

## 12. Langkah minggu ini
1. WA 10 klien lama minta ulasan Google + foto hasil. 2. Buat kartu/pesan referral dengan komisi tertulis. 3. Tambah pertanyaan "tahu dari mana?" di setiap chat baru.

*Bukan jaminan hasil.*

---

## Penilaian penguji
- Agent mengoreksi biaya survei gagal ke biaya per proyek — wawasan bernilai tinggi. ✔
- Keluaran script "Pesanan dari iklan: 1" dan "Anggaran iklan maks Rp 150 jt" **mudah menyesatkan pengguna awam** di usaha tiket besar; agent harus menafsirkan sendiri. SKILL.md belum memberi instruksi cara membaca. Temuan M1.
- Script menyatakan STATUS: AMAN pada margin 21,4%, sedangkan `references/kanal-umkm-indonesia.md` menyarankan iklan berbayar hanya bila margin ≥ 25% dan SKILL.md langkah 2 memakai ambang 15%. Tiga ambang berbeda (15/20/25). Temuan L2.
- Skill tidak punya contoh khusus jasa/lead (survei -> deal); corong fleksibel menutupinya. ✔
