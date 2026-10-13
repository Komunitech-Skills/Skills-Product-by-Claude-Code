# Uji OpenClaw SEBELUM vs SESUDAH: gaji-umkm

## Uji ulang v1.0.11 (2026-10-13, penguji independen)

**Cara uji:** OpenClaw 2026.10.2 lokal (`openclaw agent --local`, satu giliran per panggilan, tanpa Telegram/gateway), model router Komunitech (`ninerouter/komunitech`), home baru yang terisolasi untuk setiap sampel. **SEBELUM** = home tanpa skill. **SESUDAH** = home berisi `gaji-umkm` 1.0.11 saja (isi paket pembeli, tanpa `tests/`). Ini berbeda dari uji 2026-10-01 yang memakai paket 24 skill usaha-offline. Pesan member identik di kedua sisi, yaitu pesan skenario 02 di bawah (data fiktif). **Kedua sisi dijalankan ulang**, masing-masing 2 sampel. Tidak ada sisi yang bertanya balik, jadi giliran 2 tidak dipakai. Rubrik sama dengan uji pertama: ketepatan, siap pakai, aturan Indonesia, keamanan, kejelasan.

**Verifikasi angka independen** (Python `Decimal`, tidak mengimpor script skill). Lembur: PP 35/2021 Pasal 31 (upah/jam = 1/173 upah sebulan; jam ke-1 1,5×, jam berikutnya 2×; rumus sama dengan Kepmenaker 102/2004 yang sudah diganti). BPJS Kesehatan: 4% + 1%, dasar gaji pokok + tunjangan tetap, maks. Rp12 jt (Perpres 82/2018 jo. 64/2020). JHT 3,7% + 2% (PP 46/2015). JKK 0,24% (asumsi risiko sangat rendah, PP 44/2015). JKM 0,3% (PP 44/2015). JP 2% + 1%, batas upah Rp11.086.300 sejak Maret 2026 (PP 45/2015). PPh 21 TER (PP 58/2023, PMK 168/2023): bruto pajak = gaji + lembur + iuran BPJS Kesehatan, JKK, dan JKM yang dibayar perusahaan; TER A 0% s.d. Rp5.400.000, TER B 0% s.d. Rp6.200.000. UMK Surakarta 2026 = Rp2.570.000 (Kepgub Jateng 100.3.3.1/505, menurut media; naskah resmi tidak dibaca), jadi kedua upah di atas UMK.

| | Andi (K/1) | Sari (TK/0) | Total |
|---|---:|---:|---:|
| Lembur (10,5 jam × 3.100.000/173) | 188.150 | 0 | |
| Pendapatan | 3.288.150 | 2.650.000 | 5.938.150 |
| Potongan karyawan (Kes 1% + JHT 2% + JP 1%) | 124.000 | 106.000 | 230.000 |
| Bruto pajak TER | 3.428.890 | 2.770.310 | |
| PPh 21 | 0 | 0 | 0 |
| **Transfer** | **3.164.150** | **2.544.000** | **5.708.150** |
| Setor BPJS Kesehatan | 155.000 | 132.500 | 287.500 |
| Setor BPJS Ketenagakerjaan | 286.440 | 244.860 | 531.300 |
| **Total setor BPJS** | | | **818.800** |
| Biaya perusahaan | 3.605.590 | 2.921.360 | 6.526.950 |

- **SEBELUM (2 sampel):** transfer, total setor BPJS, dan PPh 21 benar. Kedua sampel menulis lembur per hari 62.717 × 3 lalu totalnya 188.150 (seharusnya 188.151 bila dibulatkan per hari; selisih Rp1, tidak konsisten). Ambang TER dibandingkan dengan gaji kotor tanpa iuran yang dibayar perusahaan; hasilnya tetap 0.
- **SESUDAH (2 sampel):** angka diambil dari mesin skill (`payroll.py`, hitungan sementara tanpa database). Setiap kolom keluaran (termasuk bruto pajak dan biaya perusahaan) **cocok 100%** dengan tabel di atas.

| Sampel | Skor tanpa skill | Skor dengan skill | Alasan |
|---|:-:|:-:|---|
| 1 | 7 | 9 | Tanpa skill: angka benar dan rapi, tetapi tidak menyebut dasar aturan maupun disclaimer. Setoran digabung jadi "Total setor BPJS ke rekening BPJS Rp818.800", padahal BPJS Kesehatan dan Ketenagakerjaan disetor ke tempat berbeda. Dengan skill: setoran dipisah (Rp287.500 / Rp531.300), ada biaya perusahaan Rp6.526.950, 4 asumsi bernomor (tanggal masuk, JKK, UMK belum dicek, pola 5 hari), dasar aturan + catatan pembulatan, dan tawaran database setelah persetujuan. |
| 2 | 7 | 9 | Tanpa skill: angka benar, tabel per program, dan tawaran slip, tetapi mengklaim "Gaji pokok kalian berdua di atas UMK Solo, jadi aman" tanpa angka/sumber. Klaim ini kebetulan benar untuk 2026, padahal selisih Sari hanya Rp80.000. Tidak ada dasar aturan maupun disclaimer. Dengan skill: tabel per karyawan + biaya perusahaan, setoran dipisah, UMK diminta dari SK Gubernur, dan disclaimer lengkap (dasar aturan, Coretax, Kring Pajak). |
| **Rata-rata** | **7** | **9** | **Selisih +2,0** |

**Verdik: LULUS** (sesudah 9 ≥ 8, selisih 2,0 ≥ 1,5).

**Pembeda (satu kalimat):** Angka pokok sama-sama benar, tetapi dengan skill angka berasal dari mesin hitung yang cocok 100% dengan hitungan independen, setoran dipisah BPJS Kesehatan Rp287.500 / Ketenagakerjaan Rp531.300 lengkap dengan biaya perusahaan, asumsi bernomor, dan dasar aturan + disclaimer, tanpa klaim UMK; tanpa skill tidak ada dasar aturan atau disclaimer, setoran digabung ke satu "rekening BPJS", dan satu dari dua sampel mengklaim "di atas UMK, aman" tanpa angka.

**Catatan jujur:**
- Skor SEBELUM 8 pada uji 2026-10-01 **tidak terulang**. Kedua sampel baru mendapat 7 karena tidak menyebut dasar aturan, tidak memberi disclaimer, dan tidak memisahkan setoran per lembaga. Selisih ini datang dari kelengkapan dan kepatuhan, **bukan** dari ketepatan angka utama: transfer dan total setor sama-sama benar.
- Sisa kecil SESUDAH: (1) agent menulis CSV sementara dan slip (Markdown/HTML) di folder kerja **tanpa menyebut lokasinya** di balasan (SKILL.md meminta lokasi disebut); (2) tenggat setor (BPJS Kesehatan tgl 10, BPJS TK tgl 15) belum disebut di balasan pertama. Cacat lama "dua hal lalu tiga butir" sudah hilang.
- Disclaimer SESUDAH menulis "berlaku per 23 Sep 2026". Tanggal itu adalah tanggal status aturan di `references/dasar-aturan.md`, bukan tanggal karangan agent.
- Hanya satu skenario (2 karyawan tetap, tanpa karyawan masuk/keluar, tanpa DTP); 2 sampel per sisi.

---

**Sumber (ada di paket VIP):** `solusi-vip/usaha-offline/UJI-OPENCLAW.md` (tabel skor skenario 02, bagian "Cacat per skill", "Cuplikan jualan" dan "Uji ulang 2026-10-01 (keuangan)") dengan rincian per skenario di `solusi-vip/usaha-offline/uji-openclaw/02-gaji-bpjs.md` dan `02-gaji-bpjs-ulang.md`.
**Tanggal uji:** 2026-10-01 (Asia/Jakarta).
**Versi skill saat uji:** uji pertama kira-kira 1.0.5 (disimpulkan dari riwayat `catalog.csv` sebelum perbaikan pasca-uji; berkas sumber tidak menyebut versi), uji ulang = 1.0.6. Versi di katalog saat ini: 1.0.11.
**Penguji (agent):** agent penguji independen (bukan pembuat skill); uji ulang oleh penguji independen lain.

> Berkas ini ringkasan yang disalin dari catatan uji solusi VIP Usaha Offline (uji dilakukan per solusi, bukan per skill). Angka disalin apa adanya dari sumber.

## Cara uji
- OpenClaw lokal (`openclaw agent --local`, satu giliran per panggilan, tanpa Telegram/gateway). Model: router Komunitech `ninerouter/komunitech` (dilayani `claude-sonnet-5`), sama dengan bot member.
- **SEBELUM** = home OpenClaw tanpa skill. **SESUDAH** = home berisi paket skill usaha-offline (24 skill, termasuk `gaji-umkm`). Pesan identik. Agent SESUDAH bertanya balik sekali pada uji pertama; jawaban member ("Andi masuk 1 Maret 2022, Sari 1 Januari 2024. Belum pernah pakai, bikinin aja.") sama pada kedua putaran.
- Uji ulang hanya mengulang sisi SESUDAH; skor SEBELUM dipakai ulang dari uji pertama. Angka dihitung ulang penguji dengan Python (BPJS Kesehatan 4%/1%, JHT 3,7%/2%, JKK 0,24%, JKM 0,3%, JP 2%/1%, lembur PP 35/2021, PPh 21 TER PMK 168/2023).

**Pesan member (skenario 02):** "Tolong hitungin gaji september 2 karyawan warung makan saya di Solo. Andi: gapok 2,8jt + uang makan tetap 300rb, status nikah anak 1, lembur 3 hari masing2 2 jam (hari kerja biasa). Sari: gapok 2,65jt, belum nikah, ga lembur. Dua2nya ikut BPJS Kesehatan & BPJS TK (JHT, JKK, JKM, JP). Yg ditransfer ke masing2 berapa, saya nyetor BPJS berapa total, PPh 21 nya ada ga?"

## Skor

| Skenario | Versi skill | Skor tanpa skill | Skor dengan skill | Pembeda (satu kalimat) |
|---|---|:-:|:-:|---|
| 02 Gaji September + BPJS + PPh 21, 2 karyawan warung, uji pertama | ±1.0.5 | 8 | 8 | Angka kedua sisi sama persis dan benar (transfer Andi Rp3.164.150, Sari Rp2.544.000, setor BPJS Rp818.800, PPh 21 Rp0); dengan skill data tersimpan di database lokal dengan tawaran slip dan CSV transfer, serta jujur bahwa UMK belum dicek, tetapi butuh satu giliran tambahan (menanyakan tanggal masuk) sedangkan tanpa skill langsung tuntas dan menulis "di atas UMK Solo" tanpa angka. |
| 02, uji ulang (hanya sisi SESUDAH) | 1.0.6 | 8 (dari uji pertama) | 9 | Angka lengkap keluar di giliran 1 dengan asumsi tanggal masuk disebut, UMK/JKK/tanggal masuk dalam satu pesan, database dibuat hanya setelah member setuju. |
| **Rata-rata skenario ini** (skenario tunggal) | | **8** | **8** (uji pertama, seri) → **9** (1.0.6) | Selisih 0 pada uji pertama, +1 pada uji ulang. |

Rata-rata seluruh solusi usaha-offline (5 skenario, skill berbeda) di uji pertama: 7,8 → 7,8. Itu skor solusi, bukan skor skill ini.

## Verdik
**LULUS uji ulang (skor 9, 1.0.6).** Pada uji pertama hasilnya seri (8 vs 8).

## Catatan jujur
- Angka sama-sama benar di kedua sisi, jadi pembeda bukan ketepatan satu jawaban. Sumber menilai keunggulan ada pada hal yang tidak terlihat dalam satu jawaban: data tersimpan lokal untuk bulan depan, slip dan file transfer, dasar aturan, dan tidak mengklaim UMK tanpa data.
- Skor 9 adalah skor sisi SESUDAH setelah skill diperbaiki dari temuan uji pertama; sisi SEBELUM tidak dijalankan ulang.
- Sisa kecil pada uji ulang: kalimat "dua hal" lalu tiga butir. UMK Solo 2026 belum diisi sehingga cek batas upah dilewati (agent meminta angkanya).
- Versi 1.0.7 sampai 1.0.11 (antara lain mesin hitung disinkronkan, rujukan upah harian lepas, PPh 21 DTP PMK 105/2025) tidak diuji ulang di skenario ini.
- Satu skenario saja (dua karyawan tetap, tanpa karyawan masuk/keluar tahun berjalan).

## Cuplikan dari sumber (uji pertama)
Dengan skill, data Andi dan Sari tersimpan di komputer pemilik; hasil hitung sama persis dengan hitungan independen (transfer Rp3.164.150 dan Rp2.544.000, setor BPJS Rp818.800), lalu skill menawarkan: "bilang saja 'kunci' — saya buatkan slip gaji per orang dan file transfer CSV-nya."
