# Contoh 03, data rusak: ekspor Excel dengan pemisah titik koma

> Dibuat oleh pembuat skill. Data fiktif: `data-rusak.csv` (pemisah `;`, nama kolom "WhatsApp", "Terakhir Beli", "Total").

## Permintaan pengguna
> "Ini data pelanggan dari Excel saya, tolong lihat siapa yang perlu dihubungi lagi."

## Langkah agen
```bash
python3 scripts/segmentasi.py examples/data-rusak.csv --hari-ini 2026-10-05
```
Keluaran script (UNTUK AGENT SAJA):
```
UNTUK AGENT SAJA -- ringkasan hitungan. Jangan tempel mentah ke pengguna; sampaikan hasilnya dengan bahasa biasa.
Tanggal acuan: 2026-10-05 | Baris data dibaca: 7 | Pelanggan unik valid: 4 | Ditolak: 3
Dianggap pasif bila sudah >= 45 hari sejak beli terakhir. Masih aktif (tidak dihubungi): 1

SEGMEN (hari sejak beli terakhir)
  A Baru senyap : 45-90 hari | B Senyap : 91-180 | C Lama hilang : 181-365 | D Sangat lama : 366+
  kode | segmen       | jumlah | rata-rata belanja | nilai belanja (rata-rata x jumlah) | skenario 10% kembali
  A    | Baru senyap  |      0 |               Rp0 |                                Rp0 | Rp0
  B    | Senyap       |      1 |       Rp1.500.000 |                        Rp1.500.000 | Rp150.000
  C    | Lama hilang  |      1 |         Rp750.000 |                          Rp750.000 | Rp75.000
  D    | Sangat lama  |      1 |       Rp2.000.001 |                        Rp2.000.001 | Rp200.000
  TOTAL: 3 pelanggan pasif | nilai belanja historis Rp4.250.001 | skenario Rp425.000 (kira-kira 0.3 pelanggan kembali)
  Catatan: angka 'nilai belanja' = rata-rata belanja per pelanggan x jumlah (bukan ramalan). Skenario = ASUMSI persentase kembali yang bisa diubah (--target-balik), bukan janji hasil.

JADWAL (3 pelanggan x 3 pesan = 9 pesan; maks 10 pesan/hari; tanpa hari Minggu; mulai 2026-10-05, selesai paling lambat 2026-10-29)
  Urutan = nilai belanja terbesar dulu. Pesan 2 & 3 HANYA bila pelanggan belum membalas dan tidak komplain/minta berhenti.
  no | segmen | nama | no_wa | hari | total | tag | pesan1 | pesan2 | pesan3
  1 | D | Mbak Ina | 6281311112207 | 642 | Rp2.000.001 | - | 2026-10-05 | 2026-10-15 | 2026-10-29
  2 | B | Bu Citra | 6281311112201 | 146 | Rp1.500.000 | - | 2026-10-05 | 2026-10-15 | 2026-10-29
  3 | C | Pak Doni | 6281311112202 | 216 | Rp750.000 | - | 2026-10-05 | 2026-10-15 | 2026-10-29

PERLU DILENGKAPI / BARIS DITOLAK (3) -- tidak masuk jadwal:
  baris 4 | Mbak Eka | nomor rusak (format ilmiah Excel '8.13111E+11'); format kolom sebagai Teks lalu ekspor ulang
  baris 5 | Kak Fajar | tanggal tidak ada di kalender '2026/13/05' (dibaca dd/mm/yyyy)
  baris 6 | Bu Gina | total belanja negatif '-250000'
```

### Verifikasi independen
- Pak Doni: 03-03-2026 dibaca 3 Maret 2026 (hari-bulan-tahun), selisih ke 5 Okt = 216 hari: segmen C (181-365). Benar.
- Bu Citra: "12 Mei 2026" = 146 hari: segmen B. Mbak Ina: 01/01/2025 = 642 hari: segmen D; "2.000.000,50" = 2.000.000,5 dibulatkan Rp2.000.001.
- Pak Hadi: 07/09/2026 = 28 hari, masih aktif, tidak dihubungi.
- Ditolak 3 baris: nomor rusak format ilmiah Excel (8.13111E+11, digit terpotong dan tidak bisa dipulihkan), bulan ke-13 (2026/13/05), total negatif. Script tidak menebak.

## Balasan ke pengguna

Dari 7 baris data, 3 pelanggan pasif yang bisa langsung dihubungi, dengan total belanja dulu **Rp4.250.001**:

| Pelanggan | Lama diam | Segmen | Total belanja dulu |
|---|---|---|---|
| Mbak Ina | sekitar 1 tahun 9 bulan | D (sangat lama) | Rp2.000.001 |
| Bu Citra | sekitar 5 bulan | B (senyap) | Rp1.500.000 |
| Pak Doni | sekitar 7 bulan | C (lama hilang) | Rp750.000 |

Pak Hadi baru belanja September, jadi belum perlu dihubungi.

**Tiga baris tidak bisa dipakai, mohon dicek di file Anda:**
1. **Mbak Eka**: nomornya terubah Excel menjadi bentuk "8,13E+11" sehingga angkanya hilang. Perbaiki dengan memformat kolom nomor sebagai *Teks*, lalu isi ulang nomornya.
2. **Kak Fajar**: tanggal "2026/13/05" tidak ada di kalender (bulan ke-13). Mohon dicek tanggal sebenarnya.
3. **Bu Gina**: total belanja tertulis minus Rp250.000. Mungkin retur atau salah ketik.

Tiga pelanggan itu belum saya masukkan ke jadwal; kalau datanya sudah diperbaiki, kirim lagi dan saya hitung ulang. Saya tidak menebak isinya supaya Anda tidak mengirim pesan ke nomor yang salah.

**Jadwal:** Pesan 1 hari ini (Senin 5 Okt) untuk ketiganya, pesan 2 pada 15 Okt, pesan 3 pada 29 Okt, hanya bagi yang belum membalas. Teks pesan untuk segmen B, C, dan D ada di bawah.

**Pesan 1, segmen B (Bu Citra):**
```
Halo Bu Citra, ini [nama Anda] dari [nama usaha]. Sudah beberapa bulan sejak terakhir Ibu belanja di tempat kami, dan kami cuma ingin menyapa. Boleh tahu, ada yang kurang cocok atau memang sedang tidak butuh? Jujur saja tidak apa-apa, justru membantu kami berbenah. Kalau tidak ingin dihubungi lagi, balas "stop" ya.
```
**Pesan 1, segmen C (Pak Doni):**
```
Selamat siang Pak Doni. Saya [nama Anda] dari [nama usaha]. Dulu Bapak pernah langganan [yang dulu dibeli] di tempat kami, dan kami masih ingat. Apa kabar? Kalau ada waktu, boleh cerita apa yang membuat Bapak jarang mampir lagi? Tidak ada maksud memaksa. Kalau tidak berkenan dihubungi lagi, balas "stop" saja.
```
**Pesan 1, segmen D (Mbak Ina):**
```
Halo Mbak Ina, ini [nama Anda] dari [nama usaha]. Sudah lebih dari setahun sejak terakhir kita ketemu, semoga Mbak sehat selalu. Kalau nomor ini sudah bukan Mbak Ina, mohon maaf mengganggu. Kalau tidak ingin dihubungi lagi, balas "stop" ya.
```
Pesan 2 dan 3 sama dengan contoh sebelumnya (tanpa penawaran sampai Anda menentukan).

**Pertanyaan:**
1. Ada penawaran yang boleh disebut di pesan ketiga, atau tanpa penawaran saja?
2. Apa yang biasanya dibeli ketiga pelanggan ini, supaya `[yang dulu dibeli]` bisa diisi?

---
## Catatan pembuat
- Titik koma dan nama kolom bervariasi dikenali; 3 baris rusak dilaporkan dengan alasan, tidak ditebak; tidak ada traceback.
- Nomor yang rusak tidak ditebak (risiko mengirim ke orang yang salah).
