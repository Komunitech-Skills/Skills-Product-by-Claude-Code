# Uji OpenClaw sebelum/sesudah — atur-keuangan-pribadi

> Catatan penguji: saat uji ulang v1.0.7, berkas ini belum ada di repo (dicek di semua branch), sehingga dibuat baru dan hanya berisi bagian uji ulang di bawah.

## Uji ulang v1.0.7 (2026-10-02)

**Cara uji:** OpenClaw 2026.9.6 lokal (`openclaw agent --local`), model router Komunitech `komunitech` → `claude-sonnet-5` (sama dengan bot member). SEBELUM = home tanpa skill; SESUDAH = home berisi hanya `atur-keuangan-pribadi` v1.0.7. Home bersih dibuat ulang per skenario, pesan identik di kedua sisi, satu giliran (agent tidak bertanya balik). Penguji independen (bukan pembuat); angka diverifikasi ulang dengan Python dan dengan menjalankan `scripts/keuangan.py` sendiri. Fokus uji ulang: THR tidak dihitung dua kali, setoran bulanan = sisa gaji rutin, rasio cicilan berbasis gaji rutin.

Perilaku agent: tidak memasang paket, tidak mengubah config, tidak menawarkan kirim/posting ke pihak lain, tidak mencari ke seluruh disk. SESUDAH memakai alat `read` + `exec` (membaca SKILL.md dan menjalankan script); SEBELUM tanpa alat.

### Skenario 1 — keluarga muda Bekasi (normal, wajib)

**Pesan:**
> Kami tinggal di Bekasi, anak 1 umur 2 tahun (dititip daycare). Gaji bersih suami 8,5 juta, istri 4 juta. THR masing-masing 1x gaji. Cicilan motor 1,2 juta, KPR 3,1 juta, kirim ke orang tua 1 juta. Listrik+PDAM+gas sekitar 650 ribu, belanja dapur 2,2 juta, susu & popok 750 ribu, daycare 1 juta, bensin+tol+parkir 600 ribu, pulsa & internet 350 ribu, sedekah 200 ribu, kondangan rata-rata 150 ribu, makan di luar 400 ribu, Netflix dkk 70 ribu. Dana darurat baru ada 8 juta. Tolong atur anggaran bulanan dan berapa dana darurat yang harus kami punya.

**Balasan SEBELUM (tanpa skill):**

````markdown
Oke, saya hitung dulu arus kasnya baru masuk ke dana darurat.

**Pemasukan bulanan:** Rp12.500.000 (suami 8,5jt + istri 4jt)

**Pengeluaran rutin:**
- KPR: 3.100.000
- Cicilan motor: 1.200.000
- Belanja dapur: 2.200.000
- Daycare: 1.000.000
- Kirim orang tua: 1.000.000
- Susu & popok: 750.000
- Listrik+PDAM+gas: 650.000
- Bensin+tol+parkir: 600.000
- Pulsa & internet: 350.000
- Makan di luar: 400.000
- Sedekah: 200.000
- Kondangan: 150.000
- Netflix dkk: 70.000
**Total: Rp11.670.000**

**Sisa/surplus: Rp830.000/bulan (hanya 6,6% dari income)** — ini yang perlu diperbesar.

**Cek rasio kesehatan keuangan:**
- Cicilan utang (KPR+motor) = 34,4% dari income → masih di batas aman, tapi sudah di ujung atas. Jangan tambah utang konsumtif baru dulu.
- Kebutuhan pokok (needs) = 78,8% → tinggi, wajar untuk keluarga muda ber-KPR + anak balita di Bekasi, tapi artinya ruang gerak tipis.
- Lifestyle (makan luar+netflix+kondangan) = 5%
- Memberi (ortu+sedekah) = 9,6%
- Nabung = 6,6%

**Saran alokasi THR (total gabungan ±Rp12,5jt/tahun):**
- 70% (≈8,75jt) → dana darurat
- 20% (≈2,5jt) → pos tahunan (lebaran, kondangan musiman, servis motor/rumah)
- 10% (≈1,25jt) → kebutuhan/kesenangan anak & diri sendiri

**Berapa dana darurat yang ideal?**
Kalian dua sumber income (risiko lebih kecil dari single income), tapi punya KPR+motor+anak kecil, jadi targetnya 6–9x pengeluaran bulanan:
- Minimum (6x): **±Rp70.000.000**
- Nyaman (9x): **±Rp105.000.000**

Sekarang baru Rp8.000.000 → kurang Rp62–97 juta.

**Proyeksi ngejar target:**
Surplus 830rb/bln + THR 8,75jt/thn ≈ nambah Rp18,7 juta/tahun. Dengan pace ini, target minimum 70jt bisa dicapai dalam ±3–3,5 tahun. Supaya lebih cepat:
- Pangkas makan di luar ke ±250rb → tambahan 150rb/bulan ke tabungan.
- Evaluasi belanja dapur 2,2jt (untuk 3 orang relatif besar) — coba meal plan/belanja mingguan, potensi hemat 200-300rb.
- Simpan dana darurat di reksadana pasar uang atau deposito, bukan tabungan biasa, biar tetap cair tapi dapat return kecil.

**Catatan penting lain:**
- Cek apakah suami sudah punya asuransi jiwa — krusial karena dia penopang cicilan KPR terbesar, kalau terjadi apa-apa cicilan rumah bisa jadi beban berat.
- Setelah dana darurat tembus minimum (70jt), baru alihkan surplus ke investasi jangka panjang (pendidikan anak/pensiun), jangan dicampur dulu sebelum dana darurat aman.
````

**Balasan SESUDAH (skill aktif):**

````markdown
## Ringkasan (3 kalimat)
Dengan pemasukan rutin Rp12,5 juta/bulan dan THR Rp12,5 juta/tahun, pos wajib (termasuk cicilan motor+KPR+kiriman ortu) menyedot Rp10,85 juta — masih ada Rp830.000/bulan dari gaji yang belum bertugas plus bagian THR yang harus dicadangkan sekaligus saat cair, bukan dicicil lagi. Dana darurat Rp8 juta baru ~6-8% dari target yang seharusnya (Rp97,65–130,2 juta untuk 9-12 bulan pengeluaran pokok, karena sudah punya anak); dengan setoran Rp830rb/bulan saja butuh 9-12 tahun, tapi kalau THR ikut disetor penuh saat cair, turun jadi 4-6 tahun. Rasio cicilan (motor+KPR) sudah 34,4% dari gaji rutin — di atas batas aman 30%, jadi jangan tambah utang baru apa pun alasannya.

## Anggaran Bulanan (zero-based)

**Pemasukan**

| Sumber | Jumlah |
|---|---:|
| Gaji suami | Rp8.500.000 |
| Gaji istri | Rp4.000.000 |
| **Pemasukan rutin/bulan** | **Rp12.500.000** |
| THR (suami+istri, setara 1x gaji masing²) | Rp12.500.000/tahun (sekali cair) |

**Pos pengeluaran**

| Pos | Kelompok | Jumlah | % gaji |
|---|---|---:|---:|
| KPR | Wajib | Rp3.100.000 | 22,9% |
| Cicilan motor | Wajib | Rp1.200.000 | 8,9% |
| Belanja dapur | Wajib | Rp2.200.000 | 16,2% |
| Daycare | Wajib | Rp1.000.000 | 7,4% |
| Susu & popok | Wajib | Rp750.000 | 5,5% |
| Listrik+PDAM+gas | Wajib | Rp650.000 | 4,8% |
| Bensin+tol+parkir | Wajib | Rp600.000 | 4,4% |
| Pulsa & internet | Wajib | Rp350.000 | 2,6% |
| Kiriman ortu | Keluarga/sosial | Rp1.000.000 | 7,4% |
| Sedekah | Keluarga/sosial | Rp200.000 | 1,5% |
| Kondangan | Keluarga/sosial | Rp150.000 | 1,1% |
| Makan di luar | Keinginan | Rp400.000 | 3,0% |
| Netflix dkk | Keinginan | Rp70.000 | 0,5% |
| **Total dialokasikan** | | **Rp11.670.000** | 86,2% |
| **Sisa gaji belum bertugas → dana darurat** | | **Rp830.000** | 6,1% |

**Banding pola (pakai 60/20/20, bukan 50/30/20, karena kamu sudah punya anak+KPR di kota penyangga)**

| Kelompok | Batas pola | Rencana kamu | Selisih |
|---|---:|---:|---:|
| Kebutuhan (wajib+keluarga) | Rp8.125.000 | Rp11.200.000 | +Rp3.075.000 (di atas pola) |
| Keinginan | Rp2.708.333 | Rp470.000 | -Rp2.238.333 (jauh di bawah — bagus) |
| Tabungan | Rp2.708.333 | Rp830.000 | -Rp1.878.333 (perlu naik) |

**Arus kas THR (jangan dicicil dua kali)**

| Arus | Jumlah | Kapan |
|---|---:|---|
| Setoran bulanan ke dana darurat (dari gaji) | Rp830.000 | tiap bulan |
| THR suami+istri (total) | Rp12.500.000 | sekali, saat cair → langsung masuk dana darurat |

## Dana Darurat

| Target | Jumlah | Kekurangan dari Rp8jt | Lama (setoran Rp830rb/bln saja) | Lama (+ THR saat cair) |
|---|---:|---:|---:|---:|
| 9 bulan (minimum, sudah punya anak) | Rp97.650.000 | Rp89.650.000 | ~9 th 1 bln | ~4 tahun |
| 12 bulan (lebih aman) | Rp130.200.000 | Rp122.200.000 | ~12 th 4 bln | ~6 tahun |

**Pos yang dihitung sebagai pokok (Rp10.850.000/bulan):** KPR, cicilan motor, dapur, susu/popok, daycare, listrik/air/gas, bensin/tol, pulsa/internet, kiriman ortu (dianggap wajib ditunda tidak bisa). **Dikeluarkan dari pokok:** sedekah, kondangan, makan di luar, Netflix — ini pos yang bisa dihentikan dulu kalau gaji berhenti.

> Catatan: dengan setoran Rp830rb/bulan saja, waktu tercapainya terasa sangat lama (9-12 tahun). Ini sinyal nyata bahwa ruang gerak keuangan kalian sempit — bukan karena boros (pos keinginan sudah sangat kecil, cuma Rp470rb), tapi karena pos wajib (KPR+motor+dapur+daycare) memang berat untuk pendapatan Rp12,5jt/bulan.

## Asumsi yang dipakai
- Pola pembanding 60/20/20 (bukan 50/30/20) karena ada anak balita, KPR, dan kota penyangga — kebutuhan wajar lebih besar dari 50%.
- THR 1x gaji masing-masing = Rp12,5 juta/tahun, diasumsikan cair bulan ke-12 dari sekarang (paling konservatif); kalau biasanya cair lebih cepat (mis. bulan Ramadan), lama tercapai dana darurat sedikit lebih singkat — sebutkan kalau mau dihitung ulang.
- Status "menikah + anak" → target dana darurat 9-12 bulan pengeluaran pokok (bukan 3-6 bulan seperti lajang).
- Kiriman orang tua dimasukkan sebagai pokok wajib (dianggap tak bisa dihentikan). Kalau sebenarnya bisa ditunda saat darurat, target turun ke sekitar Rp9,45jt pokok (9 bln = Rp85,05jt) — beri tahu saya kalau ingin dihitung ulang dengan asumsi ini.
- Tidak ada asumsi imbal hasil investasi (0%) — dana darurat hanya di tabungan/rekening terpisah yang likuid, bukan instrumen yang nilainya naik-turun.

## Langkah minggu ini
1. Buka rekening terpisah (bisa sub-saving di bank yang sama) khusus dana darurat, jangan dicampur rekening harian.
2. Setiap gajian, langsung pindahkan Rp830.000 ke rekening itu dulu (bayar diri sendiri di awal, bukan sisa akhir bulan).
3. Saat THR cair nanti (total Rp12,5 juta), masukkan **seluruhnya** ke dana darurat — jangan dipakai belanja lain dulu sampai dana darurat tembus minimum 9 bulan (Rp97,65jt).
4. Jangan ambil cicilan/utang baru apa pun (kartu kredit, paylater, KTA) — rasio cicilan sudah 34,4% dari gaji, di atas batas aman 30%.
5. Review 3 bulan lagi: kalau ada kenaikan gaji/bonus/proyek sampingan, prioritaskan menambah setoran bulanan dana darurat dulu sebelum menambah pos keinginan.

⚠️ Bukan nasihat keuangan/investasi. Angka adalah simulasi dari data & asumsi di atas. Untuk kasus rumit, konsultasikan ke perencana keuangan bersertifikat.
````

**Verifikasi (Python + `keuangan.py anggaran`/`dana-darurat` dijalankan penguji):**

| Angka | Balasan SESUDAH | Hitungan penguji | Status |
|---|---:|---:|---|
| Total pos | Rp11.670.000 | Rp11.670.000 | ✓ |
| Sisa gaji rutin (12,5 jt − 11,67 jt) | Rp830.000 | Rp830.000 | ✓ |
| Pokok dana darurat (wajib + KPR + motor + kiriman ortu) | Rp10.850.000 | Rp10.850.000 | ✓ |
| Target 9 / 12 bulan | Rp97.650.000 / Rp130.200.000 | sama | ✓ |
| Lama tercapai setoran rutin saja | ~9 th 1 bln / ~12 th 4 bln | 109 / 148 bln | ✓ |
| Lama tercapai + THR Rp12,5 jt cair bulan ke-12 | ~4 th / ~6 th | 48 / 72 bln | ✓ |
| Rasio cicilan (4,3 jt ÷ gaji rutin 12,5 jt) | 34,4% | 34,4% | ✓ basis gaji rutin |
| Langkah aksi: setor Rp830.000/bulan + THR Rp12.500.000 sekaligus saat cair | — | sama dengan tabel "Arus kas rutin vs musiman" script | ✓ **THR tidak dihitung dua kali** |
| Alternatif "kiriman ortu tidak dihitung": pokok | **Rp9,45 jt** (9 bln Rp85,05 jt) | **Rp9.850.000** (9 bln Rp88.650.000) | ✗ salah Rp400.000/bln — dihitung sendiri, bukan dari script `--bukan-pokok` |
| Kolom "% gaji" (KPR 22,9%) | basis Rp13.541.666 (gaji + THR/12) | KPR ÷ gaji rutin = 24,8% | ✗ label menyesatkan (basis termasuk THR/12) |
| Banding 60/20/20: batas Rp8.125.000 / Rp2.708.333 | basis gaji + THR/12 | — | ⚠ basis campur: batas pakai THR/12, tapi "rencana tabungan" hanya Rp830.000 (THR tidak ikut) |

SEBELUM: total Rp11.670.000, surplus Rp830.000, rasio cicilan 34,4%, target 6×/9× total belanja (±Rp70 jt/±Rp105 jt), proyeksi Rp18,7 jt/th — semua aritmetika benar; THR dipakai 70% untuk dana darurat (tidak dobel). Kelemahan: basis dana darurat = seluruh belanja (bukan pokok), tanpa tabel zero-based, menyebut reksa dana pasar uang/deposito (arah produk), target 6–9 bln untuk keluarga beranak.

**Skor:** SEBELUM **6,5/10** — benar & berguna (bonus: ingat asuransi jiwa pencari nafkah), tapi tidak terstruktur dan dasar dana darurat kasar. SESUDAH **8/10** — tabel lengkap, pokok dengan pos masuk/keluar + alasan, THR dipisah rapi dan langkah aksi konsisten dengan script, rasio cicilan berbasis gaji rutin; dikurangi karena satu angka alternatif salah (Rp9,45 jt) dan label "% gaji" yang basisnya termasuk THR/12. Skill terpakai (read + exec).

### Skenario 2 — defisit bulanan tapi ada THR (jebakan)

Angka pilihan penguji: gaji Rp6 jt, pos Rp6,6 jt (defisit Rp600.000/bln), THR Rp6 jt, ingin menabung dana darurat Rp500.000/bln.

**Pesan:**
> Gaji bersih saya 6 juta, istri ibu rumah tangga, anak 1 SD. THR 1x gaji. Kontrakan 1,5 juta, cicilan motor 900 ribu, belanja dapur 2 juta, listrik+air 400 ribu, bensin 400 ribu, pulsa 200 ribu, kirim ortu 500 ribu, jajan & uang saku anak 300 ribu, ngopi+rokok 400 ribu. Dana darurat belum ada sama sekali. Tiap bulan kok selalu kurang ya, kata teman THR kan bisa nutup. Saya juga mau mulai nabung dana darurat 500 ribu per bulan. Tolong diatur.

**Balasan SEBELUM (tanpa skill):**

````markdown
Oke, saya hitung dulu kondisi real-nya biar jelas kenapa "selalu kurang" — dan kenapa saran teman soal THR itu agak keliru.

**1. Akar masalahnya: pengeluaran rutin SUDAH lebih besar dari gaji**

Total pengeluaran bulanan Anda saat ini:
- Kontrakan 1.500.000
- Cicilan motor 900.000
- Dapur 2.000.000
- Listrik+air 400.000
- Bensin 400.000
- Pulsa 200.000
- Kirim ortu 500.000
- Jajan/uang saku anak 300.000
- Ngopi+rokok 400.000
= **Rp 6.600.000**

Gaji Rp 6.000.000 → **defisit Rp 600.000/bulan**, dan ini belum termasuk nabung dana darurat sama sekali. Jadi bocornya bukan karena kurang hemat sesekali, tapi struktural: tiap bulan memang minus 600rb.

**2. Kenapa THR tidak bisa "menutup" ini**

THR itu kejadian 1x setahun (Rp 6.000.000), tapi defisitnya terjadi TIAP bulan. Kalau setahun defisitnya 600rb x 12 = Rp 7.200.000, sedangkan THR cuma Rp 6.000.000 — tetap kurang Rp 1.200.000 meski semua THR dipakai nombok defisit bulanan. Itu belum untuk dana darurat. Jadi strategi "THR nutup kekurangan" itu jebakan — tahun depan Anda balik lagi ke titik minus, siklus berulang terus. Yang harus dibenahi adalah pengeluaran bulanannya, bukan ngandelin bonus tahunan.

**3. Rencana pemangkasan bulanan (realistis, bertahap)**

Fokus di pos yang paling fleksibel, bukan yang wajib (kontrakan & cicilan motor tidak bisa diganggu):
- Ngopi+rokok: 400rb → 50rb (stop rokok total — selain hemat ~350rb, ini investasi kesehatan)
- Dapur: 2.000.000 → 1.600.000 (masak sendiri, belanja mingguan pakai list/pasar bukan minimarket, kurangi makan siap saji)
- Jajan anak: 300rb → 150rb (bekal dari rumah)
- Pulsa: 200rb → 100rb (pindah paket/provider lebih murah, manfaatkan WiFi)
- Listrik+air: 400rb → 350rb (hemat lampu/standby)
- Bensin: 400rb → 350rb (servis rutin motor, irit rute)

Total hemat: Rp 1.100.000. Ini pas menutup defisit 600rb + menyisakan 500rb buat dana darurat.

Budget baru (total = Rp 6.000.000, pas gaji):
- Kontrakan 1.500.000
- Motor 900.000
- Dapur 1.600.000
- Listrik+air 350.000
- Bensin 350.000
- Pulsa 100.000
- Kirim ortu 500.000 (tidak diotak-atik, ini kewajiban)
- Jajan anak 150.000
- Ngopi/rokok 50.000
- **Dana darurat 500.000** ✅

**Catatan jujur:** pemangkasan dapur dari 2jt ke 1,6jt itu cukup berat (20%) untuk keluarga 3 orang. Kalau ternyata tidak kuat jalan full sejak bulan pertama, lebih realistis mulai dari nabung 200-300rb dulu di bulan 1-2, sambil membiasakan diri hemat dapur & stop rokok, baru naik ke 500rb di bulan 3 setelah kebiasaan belanja stabil. Jangan dipaksa sempurna dari awal, nanti malah gagal total dan balik ke kebiasaan lama.

**4. Soal THR — pakai untuk dana darurat, bukan untuk nutup bulanan**

Karena dana darurat Anda nol, pakai seluruh THR (Rp 6.000.000) sebagai modal awal dana darurat. Itu langsung setara ~1 bulan pengeluaran — buffer penting kalau motor rusak, anak sakit, atau ada pengeluaran mendadak. Target ideal dana darurat untuk keluarga: 3-6x pengeluaran bulanan (≈ Rp 18-36 juta), jadi THR + tabungan rutin 500rb/bulan adalah langkah awal yang benar menuju sana, bukan solusi sekali jalan.

**Langkah konkret bulan ini:**
1. Setorkan THR ke rekening/tempat terpisah khusus dana darurat — jangan dicampur rekening harian.
2. Coba jalankan budget baru di atas selama 1 bulan, catat realisasinya.
3. Review akhir bulan: kalau dapur/rokok ternyata sulit ditekan segitu, sesuaikan nominal nabung (boleh turun ke 300rb), yang penting jangan sampai defisit lagi.
````

**Balasan SESUDAH (skill aktif):**

````markdown
## Ringkasan

Masalahnya bukan di THR, tapi di struktur bulanan: kebutuhan wajib + kiriman ortu kamu saja (Rp6.200.000) **sudah lebih besar dari gaji bulanan** (Rp6.000.000) — belum dihitung ngopi+rokok dan rencana dana darurat. THR 1x gaji itu cair **sekali setahun**, bukan tiap bulan, jadi kalau dipakai menambal bolong bulanan *dan* dianggap bisa untuk hal lain juga, itu menghitung uang yang sama dua kali — makanya tetap kurang. Supaya tidak kurang lagi dan dana darurat tetap jalan, ngopi+rokok harus dipangkas dulu dan setoran dana darurat dimulai dari Rp200.000 (bukan Rp500.000) sambil THR dipakai khusus menambal gaji sepanjang tahun.

## Anggaran Bulanan (versi yang pas, zero-based)

| Pos | Kelompok | Jumlah |
|---|---|---:|
| Kontrakan | Wajib | Rp1.500.000 |
| Cicilan motor | Wajib | Rp900.000 |
| Belanja dapur | Wajib | Rp2.000.000 |
| Listrik+air | Wajib | Rp400.000 |
| Bensin | Wajib | Rp400.000 |
| Pulsa | Wajib | Rp200.000 |
| Kiriman ortu | Sosial | Rp500.000 |
| Jajan & uang saku anak | Wajib | Rp300.000 |
| Ngopi+rokok | Keinginan | **Rp100.000** (dari Rp400.000) |
| Dana darurat | Tabungan | **Rp200.000** (dari rencana Rp500.000) |
| **Total** | | **Rp6.500.000** |

- Pemasukan rutin (gaji): Rp6.000.000/bulan → pos di atas minus gaji = **-Rp500.000/bulan**. Ini kekurangan yang HARUS ditambal THR, bukan dicari dari pos lain.
- THR Rp6.000.000 ÷ Rp500.000/bulan = **cukup menambal 12 bulan penuh, sisa Rp0**. Artinya THR tahun ini habis dipakai menambal gaji — jangan dipakai lagi buat beli barang/liburan, karena memang sudah "terpakai" di atas kertas.
- Cara pakainya: begitu THR cair, taruh di rekening terpisah (jangan campur rekening harian), lalu tarik Rp500.000 setiap bulan ke rekening belanja.
- Rasio cicilan motor: 15% dari gaji rutin — masih aman (batas wajar 30%).

## Dana Darurat

| Target | Jumlah | Lama tercapai (setoran Rp200.000/bln) |
|---|---:|---:|
| Milestone 1 bulan pokok (langkah awal) | Rp6.200.000 | ~31 bulan |
| 9 bulan (target akhir, keluarga dengan anak) | Rp55.800.000 | ~23 tahun |
| 12 bulan | Rp74.400.000 | ~31 tahun |

Pokok Rp6.200.000/bulan ini dihitung dari: kontrakan, dapur, listrik+air, bensin, pulsa, jajan anak, cicilan motor, dan kiriman ortu (kewajiban rutin keluarga) — jajan/ngopi tidak dihitung karena bisa dihentikan saat darurat.

Angka 23–31 tahun di setoran Rp200.000 memang terasa lama — itu kenapa milestone pertama yang realistis adalah **1 bulan pokok (Rp6,2 juta)**, bukan langsung 9-12 bulan. Begitu cicilan motor lunas atau ada tambahan income, setoran bisa dinaikkan dan waktunya memendek jauh.

## Asumsi yang dipakai

- THR dihitung terpisah dari gaji rutin (tidak digabung dua kali), sesuai arus kas musiman.
- Target dana darurat 9-12 bulan karena status menikah + 1 anak.
- Pembulatan ke bawah untuk pemasukan musiman per bulan.
- Tidak ada info utang berbunga tinggi (kartu kredit/pinjol) — kalau ada, dana darurat awal 1 bulan harus diprioritaskan sebelum hal lain.

## Langkah minggu ini

1. Mulai gajian berikutnya, turunkan pos ngopi+rokok dari Rp400.000 → Rp100.000 (hemat Rp300.000) — potong bertahap kalau berat, misalnya Rp250.000 bulan ini, Rp100.000 bulan depan.
2. Buka rekening/dompet terpisah khusus "Dana Darurat", auto-debet Rp200.000 setiap gajian — jangan tunggu "ada sisa".
3. Saat THR cair, langsung pindahkan seluruh Rp6.000.000 ke rekening buffer terpisah, lalu tarik Rp500.000/bulan ke rekening harian untuk menambal gaji — jangan dipakai belanja lain dulu.
4. Review ulang anggaran 3 bulan sekali; begitu ada kelonggaran (cicilan motor lunas, income naik), naikkan setoran dana darurat menuju Rp500.000.
5. Jangan tutup kekurangan bulan ke bulan dengan paylater/pinjol — itu memperparah, bukan solusi.

⚠️ Bukan nasihat keuangan/investasi. Angka adalah simulasi dari data & asumsi di atas. Untuk kasus rumit, konsultasikan ke perencana keuangan bersertifikat.
````

**Verifikasi:**

| Angka | SEBELUM | SESUDAH | Hitungan penguji |
|---|---|---|---|
| Total pos awal / defisit | Rp6,6 jt / −Rp600.000 ✓ | (pokok Rp6,2 jt > gaji) ✓ | Rp6.600.000 / −Rp600.000 |
| THR vs defisit setahun | 7,2 jt > 6 jt ✓ | — | Rp7.200.000 |
| Anggaran baru | Rp6.000.000, hemat Rp1,1 jt, DD Rp500.000 ✓ | Rp6.500.000, defisit Rp500.000 ✓ | 6,0 jt ✓ / 6,5 jt ✓ |
| THR menambal | — | 6 jt ÷ 500 rb = 12 bln ✓ | 12 bln |
| Pokok, target 9/12 bln | 3–6× ≈ 18–36 jt (basis 6 jt) | 6,2 jt; 55,8 jt / 74,4 jt ✓ | 6.200.000; 55.800.000 / 74.400.000 |
| Lama (setor Rp200.000) | — | 31 bln / ~23 th / ~31 th ✓ | 31 / 279 / 372 bln |
| Rasio cicilan | — | 15% dari gaji rutin ✓ | 900 rb ÷ 6 jt = 15% |
| THR dobel? | Tidak (THR seluruhnya ke DD, defisit ditutup pemangkasan) | Tidak (THR seluruhnya untuk menambal, DD hanya Rp200.000 dari gaji) | — |

Catatan SESUDAH: (a) setoran bulanan **turun ke Rp200.000** dan THR dipakai menambal defisit — sesuai aturan revisi, tidak dobel; (b) tidak membahas **bulan-bulan sebelum THR cair** — kekurangan Rp500.000/bln belum ada penambalnya sampai THR cair (dan menyetor Rp200.000 ke DD sambil defisit artinya bulan itu tetap minus); (c) defisit struktural dibiarkan bergantung pada THR tiap tahun ("bukan dicari dari pos lain") — hanya ngopi+rokok yang dipotong, padahal SEBELUM menunjukkan pemangkasan bertahap pos lain bisa menutup defisit tanpa THR; (d) kontradiksi kecil: pokok memasukkan jajan anak, lalu menulis "jajan/ngopi tidak dihitung"; asumsi "pembulatan THR/12" tidak relevan.

SEBELUM: aritmetika benar semua, menjelaskan jebakan THR dengan jelas, menutup defisit lewat pemangkasan bertahap (dengan catatan jujur bahwa dapur −20% berat), THR jadi modal awal dana darurat. Kelemahan: target dana darurat 3–6× (rendah untuk keluarga beranak), tanpa tabel/rasio cicilan.

**Skor:** SEBELUM **7,5/10**. SESUDAH **7,5/10** — logika THR benar dan angka tepat, tapi celah waktu sebelum THR cair dan ketergantungan permanen pada THR membuatnya tidak lebih baik dari tanpa skill. Skill terpakai (read + exec).

### Ringkasan uji ulang v1.0.7

- **Skor rata-rata:** SEBELUM 7,0 → SESUDAH 7,75.
- **Fokus revisi:** ✓ THR tidak dihitung dua kali di kedua skenario; ✓ setoran bulanan = sisa gaji rutin (S1 Rp830.000; S2 diturunkan karena defisit); ✓ rasio cicilan berbasis gaji rutin (34,4%; 15%).
- **VERDIK: BELUM** — rata-rata sesudah < 8, S2 tidak lebih baik dari tanpa skill, dan ada satu kesalahan angka di S1.

**Cacat untuk pembuat:**
1. **Angka alternatif dihitung sendiri (SEDANG).** S1: "kiriman ortu tidak dihitung → pokok Rp9,45 jt, 9 bln Rp85,05 jt"; benar Rp9.850.000 / Rp88.650.000. Saran: di SKILL.md langkah 5 wajibkan menjalankan ulang `--bukan-pokok` untuk angka "bila … target turun menjadi Rp…", atau biarkan script mencetak baris alternatif tanpa kiriman keluarga.
2. **Basis persentase campur (RENDAH).** Kolom `% pemasukan` dan banding pola di `anggaran` memakai gaji + THR/12; agent melabelinya "% gaji" dan membandingkan batas tabungan (basis dengan THR) dengan setoran rutin saja. Saran: script menampilkan % terhadap gaji rutin (atau dua kolom), dan banding pola menghitung "Tabungan" termasuk setoran THR/12 bila basis memakai THR/12.
3. **Defisit + THR: celah waktu (SEDANG).** S2: tidak ada penanganan bulan sebelum THR cair dan defisit dibiarkan bergantung THR permanen. Saran: bagian "Arus kas rutin vs musiman" saat sisa rutin < 0 mencetak "THR cair bulan ke-N; sebelum itu kekurangan Rp… × N belum tertutup", dan SKILL.md menyuruh menutup defisit dengan pemangkasan bertahap (Keinginan → pos fleksibel) dulu, THR hanya penambal sementara; setoran dana darurat dari gaji = Rp0 selama sisa rutin ≤ 0.

**Cuplikan jualan:**
- Tanpa skill: "Dana darurat ideal ±Rp70–105 juta" (perkiraan dari total belanja). Dengan skill: "Pokok Rp10.850.000 (KPR, motor, kiriman ortu masuk; sedekah, kondangan, makan di luar, Netflix dikeluarkan) → target Rp97.650.000; setor Rp830.000/bulan dari gaji + THR Rp12.500.000 sekaligus saat cair → tercapai ±4 tahun."
