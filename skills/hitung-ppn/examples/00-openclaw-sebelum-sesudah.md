# Uji OpenClaw SEBELUM vs SESUDAH — hitung-ppn

## Cara uji
- **Tanggal:** 2026-10-01. Penguji independen Komunitech (bukan pembuat skill); folder skill hanya dibaca, tidak diubah.
- **Agent:** OpenClaw **2026.9.6** lokal (`openclaw agent --local`, tanpa Telegram/gateway), model router Komunitech **claude-sonnet-5** (sama dengan bot member), TZ Asia/Jakarta.
- **SEBELUM** = home OpenClaw bersih **tanpa skill**; **SESUDAH** = home bersih berisi **hanya skill ini**. Home dibuat ulang per skenario. Pesan identik di kedua sisi.
- Angka diverifikasi ulang dengan Python; aturan dicek terhadap UU HPP & PMK 131/2024 (tarif 12%; DPP nilai lain 11/12 untuk non-mewah → efektif 11%; 12% × harga hanya untuk barang mewah kena PPnBM).
- Perilaku agent: tidak ada yang memasang paket, mengubah config, atau mencari ke seluruh disk. SEBELUM skenario 2 memakai `web_fetch` (mencari aturan di internet).

## Skenario 1 — Normal: penawaran jasa, harga belum PPN, per unit

**Pesan pengguna:**
> Kak aku PKP, mau kirim penawaran jasa servis AC ke kantor klien, 15 unit @ Rp 350.000 belum termasuk PPN. PPN-nya berapa & total yang aku tagih jadi berapa? Biar bisa langsung aku tempel ke penawaran

**SEBELUM (tanpa skill)** — tools: (tidak ada)
~~~~text
Oke, ini hitungannya (asumsi tarif PPN umum 11%, karena kenaikan ke 12% cuma berlaku untuk barang mewah tertentu):

**Rincian:**
- DPP (Dasar Pengenaan Pajak): 15 unit × Rp 350.000 = **Rp 5.250.000**
- PPN 11% = **Rp 577.500**
- **Total tagihan: Rp 5.827.500**

Format siap tempel ke penawaran:

```
Jasa Servis AC          : 15 unit x Rp 350.000  = Rp 5.250.000
PPN 11%                                          = Rp   577.500
-----------------------------------------------------------------
TOTAL TAGIHAN                                    = Rp 5.827.500
```

Kalau klienmu minta harga sudah termasuk PPN (DPP include), tinggal bilang aja ya, hitungannya beda dikit (dibagi 1,11 dulu baru dipisah DPP & PPN-nya).
~~~~

**SESUDAH (dengan skill)** — tools: read, exec (skill terpakai: `scripts/hitung_ppn.py`)
~~~~text
**Perhitungan PPN** (jasa servis AC, 15 unit @ Rp 350.000 — belum termasuk PPN)

- Harga sebelum PPN (DPP): 15 × Rp 350.000 = **Rp 5.250.000**
- DPP nilai lain (11/12): Rp 4.812.500
- PPN 12%: **Rp 577.500** (setara 11% dari harga)
- **Total yang ditagih: Rp 5.827.500**

Cara hitung: DPP = 15 × 350.000 = 5.250.000 → DPP nilai lain = 11/12 × 5.250.000 = 4.812.500 → PPN = 12% × 4.812.500 = 577.500 → Total = 5.250.000 + 577.500 = 5.827.500.
Pembulatan: PPN dibulatkan ke bawah sekali ke rupiah penuh (belum dicocokkan dengan Coretax).

Tinggal ditempel ke penawaran:
> Jasa servis AC 15 unit @ Rp 350.000 = Rp 5.250.000
> PPN 12% = Rp 577.500
> **Total tagihan = Rp 5.827.500**

_Dasar: UU HPP & PMK 131/2024, berlaku per 23 September 2026. Alat bantu hitung, bukan nasihat pajak; untuk kasus khusus hubungi DJP (Kring Pajak 1500200) atau konsultan pajak._
~~~~

### Verifikasi (Python independen)
- H = 15 × 350.000 = 5.250.000; DPP nilai lain = 11/12 × H = 4.812.500; PPN = 12% × 4.812.500 = **577.500** (= 11% × H); total **5.827.500** ✔ kedua sisi.
- **SEBELUM** angka benar, tetapi menulis **"PPN 11%"** di teks penawaran dan menyatakan "kenaikan ke 12% cuma berlaku untuk barang mewah tertentu". Sejak 2025 tarif resmi **12%** untuk semua; non-mewah memakai DPP nilai lain 11/12 (PMK 131/2024). Label "PPN 11%" di dokumen PKP sudah tidak sesuai aturan yang berlaku. Tidak ada disclaimer/dasar aturan.
- **SESUDAH** label tarif & DPP nilai lain benar, cara hitung ditulis, pembulatan disebut, dasar + tanggal berlaku + disclaimer ada. Kekurangan kecil: blok "tinggal ditempel" hanya menulis "PPN 12% = Rp 577.500" tanpa baris DPP nilai lain, sehingga klien bisa mengira 12% × 5.250.000 = 630.000.

### Skor
| | SEBELUM | SESUDAH |
|---|---:|---:|
| Skenario 1 | 7 | 9 |

## Skenario 2 — Jebakan aturan terbaru: tagihan supplier "PPN 12% penuh"

**Pesan pengguna:**
> Supplier kertas HVS kirim tagihan: harga Rp 2.000.000 + PPN 12% Rp 240.000, total Rp 2.240.000. Bener ga sih hitungannya? Katanya sekarang PPN udah 12% semua

**SEBELUM (tanpa skill)** — tools: tool_search, web_fetch, tool_call (mencari aturan di internet)
~~~~text
Cek hitungan tagihannya dulu secara matematis, terus soal tarifnya:

**Matematikanya betul** — Rp2.000.000 + 12% × Rp2.000.000 = Rp2.240.000, penjumlahannya pas.

**Tapi tarif 12%-nya salah kaprah.** Info "PPN sekarang 12% semua" itu nggak akurat. Faktanya:

- Tarif PPN memang resmi naik ke 12% mulai 1 Jan 2025 (UU HPP), **tapi** pemerintah pakai mekanisme DPP Nilai Lain (PMK 131/2024): untuk barang/jasa **non-mewah**, DPP-nya dihitung 11/12 × harga jual.
- Hasilnya: PPN efektif yang dibayar = 12% × (11/12 × harga) = **11% dari harga jual**, sama kayak tarif lama.
- Tarif 12% penuh cuma kena ke **barang mewah** (yang kena PPnBM) — mobil mewah, apartemen mewah, dll.

Kertas HVS itu barang umum, bukan barang mewah. Jadi harusnya:

| | Supplier hitung | Seharusnya |
|---|---|---|
| Harga | 2.000.000 | 2.000.000 |
| PPN | 12% = 240.000 | 11% = 220.000 |
| **Total** | **2.240.000** | **2.220.000** |

Selisih Rp20.000. Worth ditanyain ke suppliernya — kemungkinan mereka salah paham soal "PPN naik jadi 12%" dan nggak tahu soal mekanisme DPP Nilai Lain ini. Kalau mau aman, minta mereka cek ulang atau tunjukkin PMK 131/2024 Pasal 2.
~~~~

**SESUDAH (dengan skill)** — tools: read, exec (skill terpakai: `scripts/hitung_ppn.py`)
~~~~text
Gak pas, tagihannya salah hitung. Supplier kena denger "PPN 12%" terus main kaliin 12% × harga, padahal buat barang biasa (non-mewah, kertas HVS termasuk ini) tarifnya **efektif 11%** pakai mekanisme DPP nilai lain 11/12.

**Perhitungan yang benar:**
- Harga sebelum PPN (DPP): Rp 2.000.000
- DPP nilai lain (11/12 × DPP): Rp 1.833.333,33
- PPN 12%: Rp 220.000 (efektif 11% dari harga)
- **Total yang seharusnya: Rp 2.220.000**

Cara hitung: DPP nilai lain = 11/12 × 2.000.000 = Rp 1.833.333,33 → PPN = 12% × 1.833.333,33 = Rp 220.000.

Tagihan supplier pakai Rp 240.000 (12% penuh dari harga) — itu kelebihan Rp 20.000 dari yang seharusnya, kecuali kertas HVS itu dianggap "barang mewah" (kena PPnBM), yang jelas bukan.

Jadi: "PPN sekarang 12%" itu benar sebagai *tarif nominal*, tapi berkat skema DPP nilai lain, untuk barang/jasa biasa efeknya tetap 11% dari harga — sama kayak era sebelumnya. 12% penuh cuma buat barang mewah.

Saran: minta supplier revisi tagihan jadi Rp 220.000 PPN / total Rp 2.220.000, atau tanyakan apa mereka salah paham soal aturan barunya.

Pembulatan: PPN dibulatkan ke bawah ke rupiah penuh (belum dicocokkan dengan Coretax).

_Dasar: UU HPP & PMK 131/2024, berlaku per 23 September 2026. Alat bantu hitung, bukan nasihat pajak; untuk kasus khusus hubungi DJP (Kring Pajak 1500200) atau konsultan pajak._
~~~~

### Verifikasi
- Kertas HVS non-mewah: PPN = 12% × 11/12 × 2.000.000 = **220.000**, total **2.220.000**, selisih tagihan supplier **Rp 20.000** ✔ kedua sisi.
- SEBELUM benar setelah mencari di web; rujukan "PMK 131/2024 **Pasal 2**" kurang tepat (Pasal 2 mengatur barang mewah 12% × harga; DPP nilai lain 11/12 ada di Pasal 3) — minor. Tidak ada disclaimer.
- SESUDAH benar tanpa akses internet, menampilkan DPP nilai lain 1.833.333,33, pembulatan, dasar aturan + tanggal, disclaimer.

### Skor
| | SEBELUM | SESUDAH |
|---|---:|---:|
| Skenario 2 | 8,5 | 9 |

## Ringkasan
| Skenario | SEBELUM | SESUDAH |
|---|---:|---:|
| 1. Penawaran jasa 15 unit | 7 | 9 |
| 2. Tagihan "12% penuh" (jebakan) | 8,5 | 9 |
| **Rata-rata** | **7,75** | **9,0** |

**VERDIK: LULUS** — sesudah ≥ 8, jelas ≥ sebelum, tanpa kesalahan fakta/angka.

Catatan jujur: untuk hitungan PPN sederhana, model dasar sudah menghasilkan angka yang benar. Pembeda skill ada di **label tarif yang sesuai aturan 2025–2026** (12% dengan DPP nilai lain, bukan "PPN 11%"), dasar aturan + disclaimer, dan tidak bergantung pada pencarian internet.

### Cacat untuk pembuat (bukti + saran)
1. (Minor) Blok siap tempel di S1 hanya "PPN 12% = Rp 577.500" → pembaca awam bisa mengira hitungan salah (12% × 5.250.000 = 630.000). Saran: di Format output, versi siap tempel wajib memuat baris "DPP nilai lain (11/12)" atau keterangan "12% × 11/12 × harga".

### Cuplikan jualan (jujur)
- "AI biasa menulis 'PPN 11%' di penawaran — label lama yang sudah tidak berlaku sejak 2025. Dengan skill: 'PPN 12% × DPP nilai lain 11/12 = Rp 577.500', lengkap dasar PMK 131/2024."
- "Tagihan supplier 'PPN 12% penuh' untuk kertas HVS? Skill langsung menunjukkan kelebihan Rp 20.000 — tanpa perlu cari di internet."
