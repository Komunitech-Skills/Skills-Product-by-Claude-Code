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

## Uji ulang v1.0.8 (2026-10-02)

**Cara uji:** tanggal 2026-10-02. OpenClaw 2026.9.6 lokal (`openclaw agent --local`), model router Komunitech `komunitech` → `claude-sonnet-5` (sama dengan bot member). SEBELUM = home tanpa skill; SESUDAH = home berisi hanya `atur-keuangan-pribadi` v1.0.8 (salinan repo). Home bersih dibuat ulang per skenario, pesan identik di kedua sisi; lanjutan memakai id sesi yang sama. Penguji independen (bukan pembuat); semua angka diverifikasi dengan Python dan dengan menjalankan `scripts/keuangan.py` sendiri. Fokus: tiga temuan v1.0.7 — (1) angka skenario alternatif dihitung sendiri, (2) basis persen tercampur, (3) defisit + THR tidak menangani bulan sebelum THR cair.

Perilaku agent: tidak memasang paket, tidak mengubah config, tidak menawarkan kirim/posting ke pihak lain, tidak mencari ke seluruh disk. SESUDAH memakai `read` + `exec` (lanjutan S1: `exec` saja); SEBELUM tanpa alat.

### Skenario 1 — keluarga muda Bekasi (normal, wajib) + lanjutan

**Pesan:**
> Kami tinggal di Bekasi, anak 1 umur 2 tahun (dititip daycare). Gaji bersih suami 8,5 juta, istri 4 juta. THR masing-masing 1x gaji. Cicilan motor 1,2 juta, KPR 3,1 juta, kirim ke orang tua 1 juta. Listrik+PDAM+gas sekitar 650 ribu, belanja dapur 2,2 juta, susu & popok 750 ribu, daycare 1 juta, bensin+tol+parkir 600 ribu, pulsa & internet 350 ribu, sedekah 200 ribu, kondangan rata-rata 150 ribu, makan di luar 400 ribu, Netflix dkk 70 ribu. Dana darurat baru ada 8 juta. Tolong atur anggaran bulanan dan berapa dana darurat yang harus kami punya.

**Balasan SEBELUM (tanpa skill):**

````markdown
Saya sudah hitung semua angkanya. Ringkasan dan rencananya di bawah.

## 1. Total pemasukan & pengeluaran bulanan

**Pemasukan bersih:** Rp12.500.000 (suami 8,5jt + istri 4jt)

**Pengeluaran rutin:**
- KPR: Rp3.100.000
- Cicilan motor: Rp1.200.000
- Belanja dapur: Rp2.200.000
- Susu & popok: Rp750.000
- Daycare: Rp1.000.000
- Listrik+PDAM+gas: Rp650.000
- Bensin+tol+parkir: Rp600.000
- Kirim orang tua: Rp1.000.000
- Pulsa & internet: Rp350.000
- Sedekah: Rp200.000
- Kondangan: Rp150.000
- Makan di luar: Rp400.000
- Netflix dkk: Rp70.000

**Total pengeluaran: Rp11.670.000**
**Sisa (surplus): Rp830.000/bulan (≈6,6% dari gaji)**

## 2. Analisis cepat

- **Rasio cicilan utang (KPR+motor) = 34,4% dari pendapatan.** Ini sudah mendekati batas aman (idealnya di bawah 30-35%). Saran: **jangan ambil utang baru** (kartu kredit, paylater, motor kedua) sampai rasio ini turun atau income naik.
- **Tabungan hanya 6,6%** — di bawah standar sehat (10-20%). Ini wajar untuk keluarga muda dengan KPR+anak kecil, tapi perlu diperbesar pelan-pelan.
- Pos terbesar setelah utang: dapur + makan luar (Rp2,6jt, 21%) dan anak (susu/popok+daycare Rp1,75jt, 14%) — keduanya memang kebutuhan, sulit dipotong banyak.
- Pos "lentur" yang bisa jadi buffer kalau darurat: makan di luar (400rb), kondangan (150rb), Netflix (70rb) — total Rp620rb bisa ditekan sementara kalau perlu.

## 3. Rencana anggaran bulanan (pakai alokasi surplus + THR)

Karena surplus bulanan kecil, cara realistis membesarkan tabungan:
1. **Sisa Rp830.000/bulan → masuk dana darurat dulu**, jangan untuk investasi apa pun sebelum dana darurat aman.
2. **THR (total Rp12.500.000/tahun, suami+istri)** dibagi dua:
   - ~70% (Rp8.750.000) → dana darurat (percepat)
   - ~30% (Rp3.750.000) → "sinking fund" tahunan: servis motor, pajak kendaraan, kebutuhan sekolah/daycare mendadak, dll. Ini penting supaya pos bulanan tidak jebol kalau ada biaya tahunan tiba-tiba.
3. Kalau ada rezeki tambahan (bonus, THR naik, kerja sampingan), prioritas tetap ke dana darurat sampai target tercapai.

## 4. Berapa dana darurat yang harus dimiliki?

Rumus standar: **dana darurat = pengeluaran bulanan × jumlah bulan buffer**, jumlah bulan tergantung profil risiko.

Kondisi keluarga Anda: **dual income** (risiko lebih rendah dibanding 1 income), tapi punya **anak kecil + KPR** (fixed obligation besar) → disarankan **6-9 bulan pengeluaran**, bukan standar minimal 3-6 bulan.

Dengan pengeluaran bulanan Rp11.670.000:
- **Minimal (6 bulan): ≈ Rp70.000.000**
- **Ideal/aman (9 bulan): ≈ Rp105.000.000**

**Posisi sekarang: Rp8.000.000** — ini baru ~0,7 bulan pengeluaran, jadi memang masih sangat kurang.

**Simulasi mengejar target (pakai surplus Rp830rb/bulan + 70% THR Rp8,75jt/tahun):**
- Tambahan per tahun ≈ (830rb×12) + 8.750.000 = **Rp18.710.000/tahun**
- Dari Rp8jt sekarang → target Rp70jt (6 bulan) tercapai **sekitar 3,3 tahun**
- Target Rp105jt (9 bulan) tercapai **sekitar 5,2 tahun**

Itu lumayan lama karena surplus bulanan memang kecil. Kalau mau lebih cepat, opsi yang paling realistis:
- Tekan makan di luar + kondangan jadi lebih hemat ±Rp200-300rb/bulan → bisa pangkas waktu ~20-25%.
- Cari tambahan income kecil (freelance, jualan sampingan) — karena sisi pengeluaran sudah cukup "ramping" untuk kebutuhan keluarga dengan anak dan KPR.

**Catatan penting:** sampai dana darurat minimal 6 bulan (Rp70jt) tercapai, sebaiknya jangan mulai investasi saham/reksadana agresif — amankan buffer ini dulu di tempat likuid (tabungan terpisah/reksadana pasar uang), baru alokasikan dana baru ke investasi jangka panjang untuk pendidikan anak.
````

**Balasan SESUDAH (skill aktif):**

````markdown
## Ringkasan
Pemasukan rutin keluarga Rp12.500.000/bulan (gaji suami+istri), ditambah THR Rp12.500.000 sekali setahun. Masalah utama: kebutuhan wajib + cicilan + kiriman ortu sudah Rp11.200.000/bulan (89,6% dari gaji rutin), jauh di atas pola 50% — wajar untuk keluarga dengan anak kecil dan KPR, tapi artinya sisa untuk ditabung cuma **Rp830.000/bulan** dari gaji. Langkah terpenting: alirkan Rp830.000/bulan itu khusus ke dana darurat, dan setor THR (Rp12.500.000) sekaligus saat cair — jangan dipakai menambah gaya hidup dulu, karena dana darurat kalian baru 8% dari target minimal.

## Anggaran Bulanan (zero-based)

**Pemasukan**

| Sumber | Jumlah |
|---|---:|
| Gaji suami | Rp8.500.000 |
| Gaji istri | Rp4.000.000 |
| THR (suami+istri Rp12.500.000/th, dibagi 12 — hanya gambaran) | Rp1.041.666 |
| **Total pemasukan (gambaran tahunan)** | **Rp13.541.666** |

**Pos pengeluaran**

| Pos | Kelompok | Jumlah | % gaji rutin (Rp12.500.000) |
|---|---|---:|---:|
| KPR | Kebutuhan wajib | Rp3.100.000 | 24,8% |
| Belanja dapur | Kebutuhan wajib | Rp2.200.000 | 17,6% |
| Motor | Kebutuhan wajib | Rp1.200.000 | 9,6% |
| Daycare | Kebutuhan wajib | Rp1.000.000 | 8,0% |
| Kiriman ortu | Keluarga/sosial | Rp1.000.000 | 8,0% |
| Susu & popok | Kebutuhan wajib | Rp750.000 | 6,0% |
| Listrik+PDAM+gas | Kebutuhan wajib | Rp650.000 | 5,2% |
| Bensin+tol+parkir | Kebutuhan wajib | Rp600.000 | 4,8% |
| Makan di luar | Keinginan | Rp400.000 | 3,2% |
| Pulsa & internet | Kebutuhan wajib | Rp350.000 | 2,8% |
| Sedekah | Keluarga/sosial | Rp200.000 | 1,6% |
| Kondangan | Keluarga/sosial | Rp150.000 | 1,2% |
| Netflix dkk | Keinginan | Rp70.000 | 0,6% |
| **Total dialokasikan** | | **Rp11.670.000** | 93,4% |
| **Belum punya tugas** | | **Rp1.871.666*** | — |

\*Dari jumlah ini, hanya **Rp830.000** yang benar-benar uang bulanan (sisa gaji rutin). Sisanya Rp1.041.666 cuma "bagian THR/12" — bukan uang yang ada tiap bulan.

**Arus kas: rutin vs musiman (THR)**

| Arus | Per bulan | Kapan uangnya ada |
|---|---:|---|
| Pemasukan rutin (gaji bersih) | Rp12.500.000 | tiap bulan |
| Total pos wajib+sosial+keinginan | Rp11.670.000 | tiap bulan |
| **Sisa rutin → ini yang boleh ditransfer tiap bulan** | **Rp830.000** | tiap bulan |
| THR suami+istri | **Rp12.500.000** | SEKALI saat cair |

**Banding 50/30/20 (basis gaji rutin Rp12.500.000)**

| Kelompok | Batas pola | Rencana kamu | Selisih |
|---|---:|---:|---:|
| Kebutuhan (wajib+sosial) | Rp6.250.000 (50%) | Rp11.200.000 | +Rp4.950.000 |
| Keinginan | Rp3.750.000 (30%) | Rp470.000 | -Rp3.280.000 |
| Tabungan | Rp2.500.000 (20%) | Rp0 (sebelum dialokasikan) | -Rp2.500.000 |

Kebutuhan jauh di atas 50% — normal untuk keluarga dengan KPR+anak kecil di kota penyangga Jakarta. Rasio cicilan (Motor+KPR) = **24,8%** dari gaji rutin, masih di bawah batas aman 30%, jadi belum perlu buru-buru melunasi lebih cepat/refinancing. Karena Keinginan kalian sudah hemat (hanya 3,8%), alokasikan sisa Rp830.000/bulan sepenuhnya ke tabungan/dana darurat (bukan dipotong dari pos lain).

## Dana Darurat

Status: menikah + punya anak → target **9–12 bulan** pengeluaran pokok.

**Pokok yang dihitung (bukan kira-kira):**

| Pos dimasukkan | Jumlah |
|---|---:|
| Belanja dapur, listrik/air/gas, susu-popok, daycare, bensin+tol+parkir, pulsa internet | Rp5.550.000 |
| Motor (cicilan) | Rp1.200.000 |
| KPR (cicilan) | Rp3.100.000 |
| Kiriman ortu (kewajiban keluarga) | Rp1.000.000 |
| **Total pengeluaran pokok** | **Rp10.850.000** |

Dikeluarkan dari pokok (boleh ditunda saat darurat): Sedekah Rp200rb, Kondangan Rp150rb, Makan di luar Rp400rb, Netflix Rp70rb.

**Target & progres**

| Target | Nominal | Kekurangan dari saldo Rp8jt | Lama tercapai (hanya setoran Rp830rb/bln) | Lama tercapai (+THR tahunan) | Progres |
|---|---:|---:|---:|---:|---:|
| 9 bulan | Rp97.650.000 | Rp89.650.000 | ~9 th 1 bln | ~4 tahun | 8% |
| 12 bulan | Rp130.200.000 | Rp122.200.000 | ~12 th 4 bln | ~6 tahun | 6% |

**Skenario alternatif (siap pakai, kalau kiriman ortu sewaktu-waktu bisa dihentikan saat darurat):**
Pokok turun ke Rp9.850.000 → target 9 bulan Rp88.650.000, 12 bulan Rp118.200.000. Ini bukan anjuran menghentikan kiriman — hanya opsi bila benar-benar darurat.

**Rekomendasi realistis:** Dengan setoran bulanan sekecil ini, target 9 bulan penuh baru tercapai ~4 tahun (dibantu THR). Fokus dulu capai **1 bulan pokok (~Rp10.850.000)** dalam waktu dekat sebagai bantalan minimum, baru naikkan ke 9–12 bulan begitu ada kenaikan gaji atau pos bisa dipangkas.

## Asumsi yang dipakai
- Pola 50/30/20 sebagai pembanding; kebutuhan di atas batas wajar untuk keluarga ber-KPR+anak.
- THR diasumsikan cair 12 bulan dari sekarang (paling konservatif) — sebutkan bulan sebenarnya kalau mau dihitung ulang lebih presisi.
- Kiriman ortu dihitung sebagai kewajiban rutin pokok (karena belum dikonfirmasi bisa dihentikan).
- Tidak ada imbal hasil pada dana darurat (disimpan di rekening/tabungan terpisah yang likuid, bukan instrumen naik-turun).
- Tidak ada utang berbunga tinggi (KK/paylater/pinjol) selain Motor & KPR, jadi tidak perlu strategi Avalanche/Snowball.

## Langkah minggu ini
1. Buka rekening/tabungan terpisah khusus dana darurat (bukan dicampur rekening harian), auto-transfer **Rp830.000** setiap tanggal gajian.
2. Saat THR cair nanti, setor **penuh Rp12.500.000** ke rekening dana darurat itu — jangan dipotong-potong ke pos lain.
3. Target antara: kumpulkan dulu 1 bulan pokok (~Rp10.850.000) sebagai bantalan minimum sebelum mengejar 9–12 bulan.
4. Jangan tambah cicilan/utang baru — rasio cicilan sudah 24,8% dari gaji rutin, cukup dekat batas aman 30%.
5. Evaluasi ulang anggaran begitu ada kenaikan gaji/bonus — setiap kenaikan sebaiknya langsung dialokasikan ke dana darurat dulu sebelum gaya hidup naik.

⚠️ Bukan nasihat keuangan/investasi. Angka adalah simulasi dari data & asumsi di atas. Untuk kasus rumit, konsultasikan ke perencana keuangan bersertifikat.
````

**Pesan lanjutan (id sesi sama):**
> Kalau kiriman ke orang tua nggak dihitung, targetnya jadi berapa?

**Balasan lanjutan SEBELUM:**

````markdown
Kalau kiriman ke orang tua (Rp1.000.000) dikeluarkan dari hitungan pengeluaran wajib — misalnya dengan asumsi saat kondisi darurat, kiriman itu bisa ditunda sementara — maka basis hitungannya begini:

## Pengeluaran bulanan (tanpa kiriman ortu)

Rp11.670.000 − Rp1.000.000 = **Rp10.670.000/bulan**

## Target dana darurat baru

- **Minimal (6 bulan):** Rp10.670.000 × 6 = **Rp64.020.000**
- **Ideal (9 bulan):** Rp10.670.000 × 9 = **Rp96.030.000**

Turun sekitar Rp6 juta dari target sebelumnya (Rp70jt → Rp64jt, dan Rp105jt → Rp96jt).

## Catatan penting

- Ini **hanya mengubah target**, bukan tabungan aktual Anda. Kalau kiriman ke orang tua tetap jalan tiap bulan di dunia nyata (bukan cuma asumsi di atas kertas), **surplus Anda tetap Rp830.000/bulan**, jadi waktu mengejar target tidak berubah — cuma garis finishnya lebih dekat:
  - Dari Rp8jt sekarang → **Rp64jt** (6 bulan): ≈ **3 tahun**
  - → **Rp96jt** (9 bulan): ≈ **4,7 tahun**
  (sedikit lebih cepat dari skenario sebelumnya, karena target lebih rendah)

- Tapi kalau maksudnya kiriman ke orang tua **benar-benar dihentikan/dikurangi** secara permanen, surplus bulanan naik jadi **Rp1.830.000/bulan**, dan itu mempercepat jauh lebih signifikan:
  - → Rp64jt: ≈ **1,9 tahun**
  - → Rp96jt: ≈ **3 tahun**

Kalau yang dimaksud skenario kedua (kiriman ortu memang mau dikurangi/dihentikan), kasih tahu saya nominalnya biar saya hitung ulang anggaran bulanannya juga — bukan cuma target dana daruratnya.
````

**Balasan lanjutan SESUDAH:**

````markdown
Kalau kiriman ke orang tua (Rp1.000.000/bulan) tidak dihitung sebagai pokok (misalnya karena bisa dihentikan sementara saat darurat), pengeluaran pokok turun jadi **Rp9.850.000/bulan**, dan targetnya:

| Target | Nominal | Kekurangan dari saldo Rp8jt | Lama tercapai (setoran Rp830rb/bln saja) | Lama tercapai (+THR tahunan) |
|---|---:|---:|---:|---:|
| 9 bulan | Rp88.650.000 | Rp80.650.000 | ~8 th 2 bln | ~4 tahun |
| 12 bulan | Rp118.200.000 | Rp110.200.000 | ~11 th 1 bln | ~5 tahun |

Dibanding sebelumnya (kiriman ortu dihitung): turun sekitar **Rp9 juta** (9 bulan) dan **Rp12 juta** (12 bulan) — lumayan, tapi waktu tercapainya tidak berubah drastis karena setoran bulanan tetap kecil (Rp830rb).

Catatan penting: ini cuma skenario "kalau". Kalau kenyataannya kiriman ke orang tua itu wajib dan tidak bisa dihentikan walau kalian sendiri lagi kesulitan (penghasilan berhenti), lebih aman tetap pakai angka yang **memasukkan** kiriman ortu (target Rp97,65jt/Rp130,2jt dari perhitungan sebelumnya) — supaya dana darurat benar-benar cukup menutup semua kewajiban, bukan cuma kebutuhan sendiri.
````

**Verifikasi (Python independen + `keuangan.py anggaran --status anak` dan `dana-darurat --setoran 830rb --setoran-tahunan 12,5jt --bulan-cair 12` dijalankan penguji):**

| Angka | SEBELUM | SESUDAH | Hitungan penguji |
|---|---|---|---|
| Total pos / sisa rutin | Rp11.670.000 / Rp830.000 ✓ | Rp11.670.000 / Rp830.000 ✓ | Rp11.670.000 / Rp830.000 |
| Kolom persen | "6,6% dari gaji" ✓ | "% gaji rutin": KPR 24,8%, dapur 17,6% … ✓ (basis kolom = judul) | 24,8% (basis Rp12.500.000) |
| **Rasio cicilan (KPR+motor)** | 34,4% ✓ | **24,8% "masih di bawah batas aman 30%" ✗** (itu persen KPR saja; diulang di Langkah 4) | Rp4.300.000 ÷ Rp12.500.000 = **34,4%** — script: "DI ATAS patokan umum 30%" |
| Banding 50/30/20 | — | Rp6.250.000/3.750.000/2.500.000 vs Rp11.200.000/470.000/0 ✓ | sama |
| Pokok dana darurat | basis total belanja Rp11.670.000 (termasuk keinginan) | Rp10.850.000 + pos dikeluarkan disebut ✓ | Rp10.850.000 |
| Target 9 / 12 bln | 6× ≈ Rp70 jt / 9× ≈ Rp105 jt (aritmetika ✓, basis & kelipatan lebih longgar) | Rp97.650.000 / Rp130.200.000 ✓ | sama |
| Lama tercapai | 3,3 th / 5,2 th (pakai 70% THR) ✓ | 9 th 1 bln & ~4 th; 12 th 4 bln & ~6 th ✓ | 109/48 bln; 148/72 bln |
| Progres | — | 8% / 6% ✓ | 8,2% / 6,1% |
| Alternatif tanpa kiriman ortu (jawaban awal) | — | Rp9.850.000 → Rp88.650.000 / Rp118.200.000 ✓ (disalin dari script) | sama |
| Lanjutan "tanpa kiriman ortu" | Rp10.670.000 → 6× Rp64.020.000 / 9× Rp96.030.000 ✓; 3 th / 4,7 th ✓; surplus 1,83 jt → 1,9 th (≈1,8) / 3 th | Rp9.850.000; Rp88.650.000 / Rp118.200.000; 8 th 2 bln & ~4 th; 11 th 1 bln & ~5 th ✓ (agent menjalankan script lagi: `exec`) | 98/48 bln; 133/60 bln |
| THR dobel? | Tidak (70% THR ke DD) | Tidak (Rp830.000/bln + Rp12.500.000 sekali) ✓ | — |

Catatan SESUDAH: temuan v1.0.7 #1 (angka alternatif dihitung sendiri) **sudah beres** — di jawaban awal maupun lanjutan angkanya sama persis dengan script. Temuan #2 (basis persen) **beres** untuk kolom tabel dan banding pola. **Kesalahan baru:** rasio cicilan ditulis 24,8% (persen KPR saja) dengan label "Motor+KPR" dan disimpulkan "di bawah batas aman 30%, belum perlu…", padahal script mencetak 34,4% DI ATAS 30%. Ini mengubah pesan penting (peringatan jangan tambah utang jadi lebih lunak), meski Langkah 4 tetap menyarankan tidak menambah utang.

SEBELUM: aritmetika benar, rasio cicilan benar, alur THR wajar (70% ke DD, 30% sinking fund). Kelemahan: dasar dana darurat memakai total belanja termasuk makan di luar/Netflix, kelipatan 6–9 bulan untuk keluarga beranak balita, menyarankan reksa dana pasar uang (produk), tanpa tabel; lanjutan menjawab dengan baik dan bahkan membedakan "target turun" vs "kiriman benar-benar dihentikan".

**Skor:** SEBELUM **6,5/10**. SESUDAH **7,5/10** — paling lengkap & hampir semua angka dari script, tetapi satu angka kunci (rasio cicilan) salah dan kesimpulannya terbalik. Skill terpakai (read + exec; lanjutan exec).

### Skenario 2 — defisit bulanan, THR baru cair 4 bulan lagi, sudah pakai paylater (jebakan)

Angka pilihan penguji: gaji Rp7.000.000, pos Rp8.100.000 (defisit Rp1.100.000/bln), THR Rp7.000.000 cair bulan ke-4, dana darurat Rp0.

**Pesan:**
> Pak, gaji bersih saya 7 juta, istri nggak kerja, anak 2 (SD sama TK). Kontrakan 1,8 juta, cicilan motor 850 ribu, belanja dapur 2,3 juta, listrik+air 450 ribu, bensin 450 ribu, SPP & uang saku anak 700 ribu, pulsa+wifi 300 ribu, kirim ortu 500 ribu, rokok+ngopi 450 ribu, jajan & makan di luar 300 ribu. Tiap bulan nombok terus, kemarin sampai gesek paylater. THR 1x gaji baru cair 4 bulan lagi. Dana darurat nol. Gimana ngaturnya biar nggak minus terus?

**Balasan SEBELUM (tanpa skill):**

````markdown
Pak, saya hitung dulu total pengeluarannya ya — ini yang bikin nombok:

**Total pengeluaran saat ini: Rp 8.100.000**
(kontrakan 1,8jt + motor 850rb + dapur 2,3jt + listrik/air 450rb + bensin 450rb + SPP&saku anak 700rb + pulsa/wifi 300rb + kirim ortu 500rb + rokok/ngopi 450rb + jajan luar 300rb)

**Gaji: Rp 7.000.000**
**Defisit: Rp 1.100.000/bulan** — ini angka pasti yang selama ini ditutup pakai paylater.

Kalau dipisah kebutuhan wajib vs keinginan:
- Kebutuhan pokok (kontrakan, motor, dapur, listrik, bensin, SPP, pulsa/wifi) = **Rp 6.850.000** — ini aja udah makan hampir semua gaji
- Sisa cuma Rp 150.000, padahal kirim ortu + rokok/ngopi + jajan luar = Rp 1.250.000

Jadi sumber defisitnya jelas: bukan kebutuhan pokok yang kemahalan, tapi pos "keinginan" yang kegedean dibanding sisa uangnya.

**Langkah 1 — Stop dulu paylater.** Jangan dipakai lagi mulai sekarang, bunga/dendanya bisa nambahin masalah. Catat total yang udah kepake biar tau beban pastinya.

**Langkah 2 — Pangkas pos keinginan (target hemat ~700rb):**
- Rokok+ngopi 450rb → tekan ke 150rb (hemat 300rb). Ini pos paling bisa dikontrol penuh dan dampaknya paling besar.
- Jajan/makan luar 300rb → 100rb (hemat 200rb)
- Kirim ortu 500rb → sementara 300rb (hemat 200rb). Bukan berhenti, tapi jujur aja ke ortu kalau lagi berat, naikin lagi kalau sudah stabil.

**Langkah 3 — Trim sedikit di dapur (target hemat 200-300rb):**
- Belanja mingguan pakai daftar, bukan harian/dadakan
- Kurangi jajanan kemasan, masak dari bahan mentah
- Dapur 2,3jt → coba tekan ke 2,1jt

Total penghematan: ±900rb–1,1jt → **cukup buat nutup defisit**, bahkan bisa mulai sisa dikit buat nabung.

**Setelah breakeven (1-2 bulan stabil), urutan prioritas:**
1. Lunasi utang paylater dulu — jangan ditunda, ini prioritas utama
2. Mulai nabung dana darurat, meski cuma 100-200rb/bulan. Target awal realistis: 2-3jt dulu, bukan langsung 1x gaji
3. THR 4 bulan lagi (±7jt) — **jangan dipakai konsumtif**. Pakai urutan: lunasin sisa paylater → isi dana darurat → baru kalau ada sisa, buat kebutuhan besar anak

**Yang perlu dicek lebih lanjut:**
- Cicilan motor 850rb — berapa sisa tenornya? Kalau masih panjang dan bunganya tinggi, worth dicek apakah bisa dipercepat pelunasan pakai THR nanti.
- Kalau memungkinkan, istri bisa coba usaha kecil dari rumah (jualan online, katering kecil-kecilan) — dengan 1 sumber penghasilan buat 4 orang, memang mepet banget, jadi tambahan penghasilan kecil pun ngaruh.

Mau saya bikinkan rincian alokasi bulanan baru (versi lengkap per pos) biar Bapak tinggal pakai sebagai pegangan tiap bulan?
````

**Balasan SESUDAH (skill aktif):**

````markdown
Oke, saya hitung pakai angka pasti (bukan kira-kira) — ini hasilnya.

## Ringkasan
Pengeluaran rutin Bapak **Rp8.100.000/bulan**, padahal gaji **Rp7.000.000** → defisit **Rp1.100.000/bulan**, itu sebab kenapa selalu nombok sampai kena paylater. Masalah utamanya bukan satu pos besar, tapi kombinasi: dapur, kontrakan, cicilan motor sudah pas-pasan, dan belum ada dana darurat sama sekali jadi tiap kejutan kecil langsung lari ke utang. THR 4 bulan lagi bisa bantu, tapi cuma penambal sementara — yang wajib dibenahi dulu adalah pos Keinginan & kebutuhan fleksibel, bertahap 3 bulan.

## Anggaran bulanan (zero-based)

| Pos | Kelompok | Sekarang | % gaji rutin |
|---|---|---:|---:|
| Kontrakan | Wajib | Rp1.800.000 | 25,7% |
| Cicilan motor | Wajib | Rp850.000 | 12,1% |
| Belanja dapur | Wajib | Rp2.300.000 | 32,9% |
| Listrik & air | Wajib | Rp450.000 | 6,4% |
| Bensin | Wajib | Rp450.000 | 6,4% |
| SPP & uang saku anak | Wajib | Rp700.000 | 10,0% |
| Pulsa & wifi | Wajib | Rp300.000 | 4,3% |
| Kirim ortu | Keluarga/sosial | Rp500.000 | 7,1% |
| Rokok & ngopi | Keinginan | Rp450.000 | 6,4% |
| Jajan & makan luar | Keinginan | Rp300.000 | 4,3% |
| **Total** | | **Rp8.100.000** | **115,7%** |
| **DEFISIT** | | **-Rp516.667** (vs gaji+THR/12) | |

Banding pola 50/30/20 (basis gaji rutin Rp7.000.000): Kebutuhan kamu **Rp7.350.000** (pola maks Rp3.500.000), Keinginan **Rp750.000** (pola maks Rp2.100.000, justru di bawah — bukan boros di sini), Tabungan **Rp0** (pola minimal Rp1.400.000). Jadi sebenarnya bukan kebanyakan jajan, tapi kebutuhan wajib memang berat untuk gaji segini — wajar untuk keluarga dengan 2 anak, tapi harus dipangkas sampai pas.

## Menutup defisit TANPA mengandalkan THR (pemangkasan bertahap 3 bulan)

| Pos | Sekarang | Potong | Jadi |
|---|---:|---:|---:|
| Rokok & ngopi | Rp450.000 | -Rp220.000 | Rp230.000 |
| Jajan & makan luar | Rp300.000 | -Rp150.000 | Rp150.000 |
| Belanja dapur | Rp2.300.000 | -Rp230.000 | Rp2.070.000 |
| Listrik & air | Rp450.000 | -Rp40.000 | Rp410.000 |
| Bensin | Rp450.000 | -Rp40.000 | Rp410.000 |
| Pulsa & wifi | Rp300.000 | -Rp30.000 | Rp270.000 |
| **Total potongan** | | **-Rp710.000** | |

Dengan pemangkasan maksimal yang wajar ini, defisit turun dari Rp1.100.000 jadi **Rp390.000/bulan** — belum tertutup 100%. Sisa Rp390.000 ini perlu ditutup dari: tambahan penghasilan kecil (ojol/jualan sampingan), atau tinjau ulang pos besar (kontrakan/cicilan motor) — **jangan ditutup paylater/pinjol lagi**.

Jadwal transisi sampai THR cair (bulan ke-4):

| Bulan | Kekurangan bulan itu | Kumulatif | Sumber |
|---:|---:|---:|---|
| 1 | Rp840.000 | Rp840.000 | belum ada — talangi dari saldo kalau ada, **bukan** paylater |
| 2 | Rp610.000 | Rp1.450.000 | sda |
| 3 | Rp390.000 | Rp1.840.000 | sda |
| 4 | Rp390.000 | Rp2.230.000 | **THR cair bulan ini** |

Begitu THR Rp7.000.000 cair: **Rp2.230.000** dipakai menutup/mengganti kekurangan 4 bulan transisi tadi, sisanya **Rp4.770.000** jadi modal awal dana darurat.

## Dana darurat
Pengeluaran pokok (kontrakan+dapur+listrik+bensin+SPP+pulsa+cicilan motor+kirim ortu) = **Rp7.350.000/bulan**. Status menikah+anak → target **9–12 bulan pokok = Rp66.150.000–Rp88.200.000**. Kalau kirim ortu suatu saat bisa dihentikan sementara saat darurat, pokok turun ke Rp6.850.000 → target Rp61.650.000–Rp82.200.000. Sekarang saldo darurat masih Rp0 — wajar, fokus dulu tutup defisit bulan 1-4, baru mulai setor rutin setelah itu.

## Soal paylater
Saya belum punya saldo & bunga paylater-nya — kalau Bapak kirim (sisa tagihan, bunga per bulan, cicilan minimumnya), saya hitungkan jadwal pelunasan paylater sambil tetap jalan anggaran di atas, biar nggak nambah gali lubang tutup lubang.

## Asumsi yang dipakai
- THR 1x gaji = Rp7.000.000, cair 4 bulan lagi
- Status keluarga: menikah + anak → target dana darurat 9-12 bulan
- Tidak ada data imbal hasil investasi, tidak dihitung

## Langkah minggu ini
1. Mulai bulan ini: rokok/ngopi Rp450rb→Rp230rb, jajan luar Rp300rb→Rp150rb (langsung hemat Rp370rb)
2. Bulan depan tambah pangkas: dapur Rp2,3jt→Rp2,07jt, listrik Rp450rb→Rp410rb, bensin Rp450rb→Rp410rb, pulsa/wifi Rp300rb→Rp270rb
3. Kekurangan Rp390-840rb/bulan selama masa transisi ini jangan pakai paylater baru — cari talangan dari saldo yang ada atau tahan dulu
4. Kirim saya data paylater yang sudah kepakai (saldo, bunga, cicilan min) biar dihitungkan rencana lunasnya
5. Pas THR cair bulan ke-4: Rp2.230.000 tutup kekurangan transisi, sisa Rp4.770.000 langsung jadi setoran pertama dana darurat (target Rp66-88 juta)

⚠️ Bukan nasihat keuangan/investasi. Angka adalah simulasi dari data & asumsi di atas. Untuk kasus rumit, konsultasikan ke perencana keuangan bersertifikat.
````

**Verifikasi (Python independen + `keuangan.py anggaran --musiman "THR=7jt" --status anak --bulan-cair 4` dijalankan penguji):**

| Angka | SEBELUM | SESUDAH | Hitungan penguji / script |
|---|---|---|---|
| Total pos / defisit rutin | Rp8.100.000 / Rp1.100.000 ✓ | Rp8.100.000 / Rp1.100.000 ✓; 115,7% gaji rutin ✓ | Rp8.100.000 / Rp1.100.000 / 115,7% |
| Baris "DEFISIT −Rp516.667 (vs gaji+THR/12)" | — | angka sama dengan script, tetapi muncul di bawah tabel yang judul ringkasannya defisit Rp1,1 jt — membingungkan | script "Catatan: DEFISIT Rp516.667" (basis THR/12) |
| Banding 50/30/20 | — | Rp7.350.000 / Rp750.000 / Rp0 vs batas Rp3.500.000 / Rp2.100.000 / Rp1.400.000 ✓ | sama |
| Pemangkasan | rokok −300 rb, jajan −200 rb, ortu −200 rb, dapur −200–300 rb → "±900 rb–1,1 jt, **cukup buat nutup defisit**" ✗ | 6 pos, total −Rp710.000, sisa defisit Rp390.000 ✓ (jujur: belum cukup) | SEBELUM maks. Rp1.000.000 < Rp1.100.000 → **tidak** cukup; SESUDAH = script |
| Bulan sebelum THR cair | tidak dibahas (dianggap langsung impas) | kekurangan Rp840.000 / 610.000 / 390.000 / 390.000; kumulatif Rp1.840.000 sebelum THR, Rp2.230.000 s.d. bulan ke-4 ✓ | sama dengan script |
| THR Rp7.000.000 | lunasi paylater → DD | Rp2.230.000 tutup transisi, sisa Rp4.770.000 → "setoran pertama dana darurat" | Rp4.770.000 ✓, tetapi script: sisa itu "hanya cukup menambal sisa defisit Rp390.000/bulan selama 12 bulan berikutnya" (4.770.000 ÷ 390.000 = 12,2) |
| Setoran DD dari gaji selama defisit | "100–200 rb setelah impas" | Rp0 sampai defisit tertutup ✓ | Rp0 |
| Pokok, target 9/12 bln | tidak ada target | Rp7.350.000; Rp66.150.000 / Rp88.200.000 ✓ | sama |
| Alternatif tanpa kirim ortu | — | Rp6.850.000; Rp61.650.000 / Rp82.200.000 ✓ (disalin dari script) | sama |
| Rasio cicilan | — | tidak disebut (12,1%, aman) | 12,1% |
| Paylater | stop, lunasi dulu | stop, minta saldo/bunga/minimum untuk dihitung ✓ | — |

Catatan SESUDAH: temuan v1.0.7 #3 **beres** — bulan sebelum THR cair ditangani dengan tabel per bulan, setoran DD dari gaji Rp0, defisit ditutup pemangkasan bertahap (Keinginan dulu), THR hanya penambal transisi. Semua nominal berasal dari script. Sisa cacat: (a) sisa THR Rp4.770.000 disarankan masuk dana darurat padahal sisa defisit Rp390.000/bln masih berjalan setelah bulan ke-4 tanpa sumber pasti (script sendiri menulis sisa THR itu untuk menambal 12 bulan berikutnya; SKILL.md langkah 4(d) menyuruh "sisanya disetor sekaligus ke dana darurat" — instruksi dan script tidak selaras); (b) kekurangan Rp1.840.000 sebelum THR disuruh "talangi dari saldo kalau ada" padahal dana darurat nol — tidak ada sumber konkret selain "jangan paylater"; (c) baris −Rp516.667 di tabel membingungkan pembaca awam.

SEBELUM: ramah, jelas, langsung melarang paylater, ide tambah penghasilan. Tetapi klaim angka salah ("±900 rb–1,1 jt cukup nutup defisit" — maksimal Rp1.000.000), menyebut defisit bersumber dari "keinginan" padahal pokok saja sudah Rp6.850.000 + kiriman ortu, tidak membahas 4 bulan sebelum THR, tanpa target dana darurat.

**Skor:** SEBELUM **6/10**. SESUDAH **8/10** — tepat, siap pakai, jujur bahwa pemangkasan belum cukup; dikurangi karena alokasi sisa THR bertentangan dengan sisa defisit dan talangan pra-THR tanpa sumber. Skill terpakai (read + exec).

### Ringkasan uji ulang v1.0.8

- **Skor rata-rata:** SEBELUM 6,25 → SESUDAH 7,75 (S1 6,5 → 7,5; S2 6 → 8).
- **Temuan v1.0.7:** ✓ #1 angka alternatif "tanpa kiriman ortu" kini disalin dari script (S1 awal & lanjutan, S2) dan tepat; ✓ #2 kolom persen berbasis gaji rutin dengan judul yang benar, banding pola basis gaji rutin; ✓ #3 bulan sebelum THR cair ditangani (tabel kekurangan per bulan, setoran DD Rp0, pemangkasan bertahap, THR penambal sementara).
- **VERDIK: BELUM** — ada satu kesalahan angka di S1 (rasio cicilan 24,8% bukan 34,4%, kesimpulan terbalik), dan rata-rata sesudah < 8.

**Cacat untuk pembuat:**
1. **Rasio cicilan salah baca (SEDANG).** S1: "Rasio cicilan (Motor+KPR) = 24,8% … masih di bawah batas aman 30%" dan Langkah 4 "24,8% … cukup dekat batas aman"; script: "Total cicilan Rp4.300.000 = 34,4% … DI ATAS patokan umum 30%". 24,8% adalah persen KPR di tabel. Saran: script mencetak rasio cicilan sebagai baris/kalimat siap tempel yang menonjol (mis. di bagian ringkasan atas: "Rasio cicilan 34,4% dari gaji rutin — DI ATAS 30%"), dan SKILL.md langkah 9 menambahkan rasio cicilan ke daftar angka yang wajib disalin dari script.
2. **Sisa THR vs sisa defisit (SEDANG-RENDAH).** S2: sisa THR Rp4.770.000 disuruh jadi setoran pertama dana darurat, padahal defisit Rp390.000/bln masih berjalan setelah bulan ke-4; script sendiri menulis sisa itu "hanya cukup menambal sisa defisit … 12 bulan berikutnya". Akar: SKILL.md langkah 4(d) "sisanya disetor sekaligus ke dana darurat" tidak membedakan kasus pemangkasan cukup vs belum cukup. Saran: selaraskan — bila script menulis "BELUM cukup", sisa THR dicadangkan di rekening terpisah sebagai penambal sisa defisit (dan disebut berapa bulan), DD baru diisi setelah defisit tertutup; wajibkan menyalin kalimat siap tempel ketiga apa adanya.
3. **Talangan pra-THR tanpa sumber (RENDAH).** Kekurangan Rp1.840.000 sebelum THR → "talangi dari saldo bila ada" padahal saldo Rp0. Saran: bila saldo DD/tabungan 0, script/SKILL.md memberi opsi konkret tanpa utang berbunga (tambahan pemasukan sementara, jual barang tak terpakai, minta keringanan jadwal ke pemilik kontrakan/keluarga, percepat pemangkasan bulan 1) atau menyatakan terang bahwa bulan 1–3 tetap minus.
4. **Baris defisit basis THR/12 membingungkan (RENDAH).** S2 tabel: "DEFISIT −Rp516.667 (vs gaji+THR/12)" di bawah ringkasan defisit Rp1.100.000. Saran: saat defisit rutin, script melabeli catatan itu "gambaran setahun bila THR dibagi 12" atau tidak mencetaknya, agar agent tidak menaruhnya di tabel utama.

**Cuplikan jualan:**
- Tanpa skill: "Pangkas rokok, jajan, kiriman ortu, dapur — total ±900 rb–1,1 jt, cukup buat nutup defisit" (padahal maksimal Rp1.000.000 < defisit Rp1.100.000). Dengan skill: "Pemangkasan bertahap 3 bulan −Rp710.000, sisa defisit Rp390.000 dijelaskan terus terang; kekurangan per bulan sampai THR cair dihitung (Rp840.000 → Rp610.000 → Rp390.000), THR Rp7.000.000 menutup Rp2.230.000 masa transisi — tanpa paylater."
- Tanya "kalau kiriman ortu nggak dihitung?" → dengan skill langsung dihitung ulang oleh script: target 9 bulan Rp88.650.000, tercapai ±4 tahun dengan THR.


## Uji ulang v1.0.9 (2026-10-02)

**Cara uji:** tanggal 2026-10-02, putaran 3 (terakhir). OpenClaw 2026.9.6 lokal (`openclaw agent --local`), model router Komunitech `komunitech` → `claude-sonnet-5` (sama dengan bot member). SEBELUM = home tanpa skill; SESUDAH = home berisi hanya `atur-keuangan-pribadi` v1.0.9 (salinan repo). Home bersih dibuat ulang per skenario, pesan identik di kedua sisi; lanjutan memakai id sesi yang sama. Penguji independen (bukan pembuat); setiap nominal & persen diverifikasi dengan Python independen dan dengan menjalankan `scripts/keuangan.py` sendiri. Fokus: temuan v1.0.8 — (1) rasio cicilan 24,8% (benar 34,4%), (2) sisa THR vs sisa defisit, (3) talangan pra-THR dari saldo Rp0, (4) baris defisit basis THR/12.

Perilaku agent: tidak memasang paket, tidak mengubah config, tidak menawarkan kirim/posting ke pihak lain, tidak mencari ke seluruh disk. SESUDAH memakai `read` + `exec` (lanjutan S1: `exec` saja); SEBELUM tanpa alat.

### Skenario 1 — keluarga muda Bekasi (normal, wajib) + lanjutan

**Pesan:**
> Kami tinggal di Bekasi, anak 1 umur 2 tahun (dititip daycare). Gaji bersih suami 8,5 juta, istri 4 juta. THR masing-masing 1x gaji. Cicilan motor 1,2 juta, KPR 3,1 juta, kirim ke orang tua 1 juta. Listrik+PDAM+gas sekitar 650 ribu, belanja dapur 2,2 juta, susu & popok 750 ribu, daycare 1 juta, bensin+tol+parkir 600 ribu, pulsa & internet 350 ribu, sedekah 200 ribu, kondangan rata-rata 150 ribu, makan di luar 400 ribu, Netflix dkk 70 ribu. Dana darurat baru ada 8 juta. Tolong atur anggaran bulanan dan berapa dana darurat yang harus kami punya.

**Balasan SEBELUM (tanpa skill):**

````markdown
Oke, saya hitung berdasarkan data yang dikasih. Total pemasukan bulanan kalian (gabungan bersih): **Rp 12.500.000** (suami 8,5jt + istri 4jt).

**1. Rincian pengeluaran bulanan (totalnya Rp 11.670.000)**

Cicilan/komitmen tetap – Rp 4.300.000 (34,4% dari income)
- Cicilan motor: Rp 1.200.000
- KPR: Rp 3.100.000

Kebutuhan pokok – Rp 6.550.000 (52,4%)
- Listrik+PDAM+gas: Rp 650.000
- Belanja dapur: Rp 2.200.000
- Susu & popok: Rp 750.000
- Daycare: Rp 1.000.000
- Bensin+tol+parkir: Rp 600.000
- Pulsa & internet: Rp 350.000
- Kirim orang tua: Rp 1.000.000

Sosial/ibadah – Rp 350.000 (2,8%)
- Sedekah: Rp 200.000
- Kondangan: Rp 150.000

Gaya hidup – Rp 470.000 (3,8%)
- Makan di luar: Rp 400.000
- Netflix dkk: Rp 70.000

**Sisa/tabungan: Rp 830.000 (6,6%)**

**2. Titik perhatian**

Rasio cicilan kalian (motor+KPR) sudah 34,4% dari income — ini di batas atas rule of thumb umum (maksimal 30-35%). Artinya: *jangan dulu ambil utang baru* (cicilan HP, kartu kredit, dsb) sampai rasio ini turun atau income naik.

Tabungan rutin cuma 6,6% dari income, jauh di bawah ideal 20%. Ini bukan karena boros — pos kebutuhan & cicilan memang berat — tapi artinya progres ke dana darurat/investasi akan lambat kalau hanya mengandalkan sisa bulanan.

**3. Berapa dana darurat yang harus kalian punya**

Karena kalian dual income (dua sumber gaji, jadi risiko lebih rendah dibanding satu penghasil) tapi sudah punya anak dan cicilan besar, target yang realistis:
- Minimum: **6x pengeluaran bulanan** = 6 × Rp 11.670.000 ≈ **Rp 70.000.000**
- Target aman/ideal: **9x pengeluaran bulanan** ≈ **Rp 105.000.000**

Dana darurat kalian sekarang Rp 8 juta — baru sekitar 0,7x. Masih jauh, tapi bukan hal buruk, ini memang tahap awal buat banyak keluarga muda.

**4. Cara ngejar dana darurat lebih cepat**

Kalau cuma mengandalkan sisa Rp 830.000/bulan, buat nambah Rp 62 juta (menuju target 70jt) butuh ±6 tahun. Terlalu lambat. Manfaatkan THR:

- THR tahunan kalian total ±Rp 12.500.000/tahun (1x gaji masing-masing).
- Saran split: 70% (±Rp 8,75jt) langsung masuk dana darurat, 30% (±Rp 3,75jt) buat kebutuhan Lebaran/kondangan/baju yang memang musiman — jangan dipotong dari budget bulanan.
- Dengan tambahan THR + sisa bulanan (830rb×12 = 9,96jt), total nabung per tahun ≈ Rp 18,7 juta → target 70jt bisa tercapai dalam ±3,3 tahun.

**5. Saran tambahan**
- Taruh dana darurat di tempat likuid & aman: rekening terpisah atau reksadana pasar uang — jangan deposito jangka panjang atau saham.
- Begitu gajian masuk, langsung autodebet sisa Rp 830.000 ke rekening dana darurat ("bayar diri sendiri duluan") biar nggak kepake.
- Kalau mau genjot lebih cepat, pos yang paling elastis buat dipangkas sementara: makan di luar (Rp 400rb) — turunin ke Rp 250-300rb bisa nambah Rp 100-150rb/bulan ke tabungan, tanpa mengorbankan kebutuhan anak atau cicilan.
- Setelah dana darurat capai minimal 6x (±70jt), baru mulai alokasikan ke investasi jangka panjang (pendidikan anak, pensiun) — jangan dibalik urutannya.

Singkatnya: budget kalian sudah cukup rapi dan tidak defisit, tapi marginnya tipis karena cicilan besar. Prioritas sekarang: disiplin nabung sisa bulanan + manfaatkan THR maksimal buat ngejar dana darurat 70-105 juta sebelum mikirin investasi lain.
````

**Balasan SESUDAH (skill aktif):**

````markdown
# Atur Keuangan Bulanan Keluarga — Bekasi

## Ringkasan (3 kalimat)
Gaji rutin Rp12.500.000/bulan, total pos Rp11.670.000/bulan -> sisa Rp830.000/bulan dari gaji; inilah batas setoran bulanan. Total cicilan Rp4.300.000 = 34,4% dari gaji rutin Rp12.500.000 — DI ATAS batas aman 30% - jangan menambah utang baru. Pengeluaran pokok Rp10.850.000/bulan -> target dana darurat 9 bulan = Rp97.650.000; 12 bulan = Rp130.200.000.

## Anggaran (zero-based)

**Pemasukan per bulan**

| Sumber | Jumlah |
|---|---:|
| Gaji suami | Rp8.500.000 |
| Gaji istri | Rp4.000.000 |
| Musiman dibagi 12 (THR suami Rp8,5jt, THR istri Rp4jt; total Rp12.500.000/th) | Rp1.041.666 |
| **Total pemasukan (gambaran setahun)** | **Rp13.541.666** |

**Pos pengeluaran & alokasi**

| Pos | Kelompok | Jumlah | % pemasukan rutin (Rp12.500.000) | % termasuk THR/12 |
|---|---|---:|---:|---:|
| Cicilan motor | Kebutuhan wajib | Rp1.200.000 | 9,6% | 8,9% |
| KPR | Kebutuhan wajib | Rp3.100.000 | 24,8% | 22,9% |
| Kiriman orang tua | Keluarga & sosial | Rp1.000.000 | 8,0% | 7,4% |
| Listrik/PDAM/gas | Kebutuhan wajib | Rp650.000 | 5,2% | 4,8% |
| Belanja dapur | Kebutuhan wajib | Rp2.200.000 | 17,6% | 16,2% |
| Susu & popok | Kebutuhan wajib | Rp750.000 | 6,0% | 5,5% |
| Daycare | Kebutuhan wajib | Rp1.000.000 | 8,0% | 7,4% |
| Bensin/tol/parkir | Kebutuhan wajib | Rp600.000 | 4,8% | 4,4% |
| Pulsa & internet | Kebutuhan wajib | Rp350.000 | 2,8% | 2,6% |
| Sedekah | Keluarga & sosial | Rp200.000 | 1,6% | 1,5% |
| Kondangan | Keluarga & sosial | Rp150.000 | 1,2% | 1,1% |
| Makan di luar | Keinginan | Rp400.000 | 3,2% | 3,0% |
| Netflix dkk | Keinginan | Rp70.000 | 0,6% | 0,5% |
| **Total dialokasikan** | | **Rp11.670.000** | 93,4% | 86,2% |

**Sisa dari gaji rutin yang belum punya tugas: Rp830.000/bulan** → ini jatah setoran bulanan ke tabungan/dana darurat.

**Banding pola 50/30/20 (basis gaji rutin Rp12.500.000)**

| Kelompok | Pola | Batas pola | Rencana kamu | Selisih |
|---|---:|---:|---:|---:|
| Kebutuhan (wajib + keluarga/sosial) | 50% | Rp6.250.000 | Rp11.200.000 | +Rp4.950.000 |
| Keinginan | 30% | Rp3.750.000 | Rp470.000 | -Rp3.280.000 |
| Tabungan & pelunasan ekstra | 20% | Rp2.500.000 | Rp0 | -Rp2.500.000 |

Kebutuhan jauh di atas pola 50/30/20 — wajar untuk keluarga dengan cicilan KPR+motor dan anak balita; pola 60/20/20 lebih realistis di kondisi kalian, selama tabungan tetap jalan.

**Arus kas rutin vs musiman (THR)**

| Arus | Per bulan | Kapan uangnya ada |
|---|---:|---|
| Pemasukan rutin (gaji bersih) | Rp12.500.000 | tiap bulan |
| Total pos dialokasikan | Rp11.670.000 | tiap bulan |
| **Sisa dari gaji rutin** | **Rp830.000** | tiap bulan |
| THR suami+istri (setara/12) | Rp1.041.666 | SEKALI saat cair: **Rp12.500.000** |

Setoran bulanan ke dana darurat/tabungan paling banyak **Rp830.000/bulan** (hanya dari gaji). THR Rp12.500.000 disetor **sekaligus** saat cair — jangan ditambahkan lagi ke setoran bulanan (dihitung dua kali kalau begitu).

## Dana Darurat

**Dasar perhitungan (pengeluaran pokok)**

| Pos dimasukkan ke pokok | Jumlah |
|---|---:|
| Cicilan motor | Rp1.200.000 |
| KPR | Rp3.100.000 |
| Kiriman orang tua | Rp1.000.000 |
| Listrik/PDAM/gas | Rp650.000 |
| Belanja dapur | Rp2.200.000 |
| Susu & popok | Rp750.000 |
| Daycare | Rp1.000.000 |
| Bensin/tol/parkir | Rp600.000 |
| Pulsa & internet | Rp350.000 |
| **Total pokok** | **Rp10.850.000** |

Dikeluarkan dari pokok (karena sifatnya opsional/bisa dihentikan saat darurat): Sedekah Rp200.000, Kondangan Rp150.000, Makan di luar Rp400.000, Netflix Rp70.000.

**Target & progres** (status: menikah + anak → 9–12 bulan pengeluaran pokok)

| Target | Jumlah dibutuhkan | Saldo sekarang | Kurang | Progres | Lama tercapai (setoran Rp830rb/bln saja) | Lama tercapai (+THR tiap cair) |
|---|---:|---:|---:|---:|---|---|
| 9 bulan | Rp97.650.000 | Rp8.000.000 | Rp89.650.000 | 8% | ~9 th 1 bln (109 bulan) | ~4 th 0 bln (48 bulan) |
| 12 bulan | Rp130.200.000 | Rp8.000.000 | Rp122.200.000 | 6% | ~12 th 4 bln (148 bulan) | ~6 th 0 bln (72 bulan) |

**Skenario alternatif:** bila Kiriman orang tua (Rp1.000.000/bulan) bisa dihentikan saat darurat, pengeluaran pokok turun menjadi Rp9.850.000 dan target 9 bulan/12 bulan menjadi Rp88.650.000/Rp118.200.000.

## Asumsi yang dipakai
- THR masing-masing 1× gaji (suami Rp8,5jt + istri Rp4jt = Rp12,5jt/tahun), diasumsikan cair bulan ke-12 (belum disebutkan bulan pastinya — kalau sudah tahu, hitungan "lama tercapai" bisa dipercepat).
- Status keluarga: menikah + punya anak → target dana darurat 9–12 bulan pengeluaran pokok.
- Kiriman orang tua dihitung sebagai kewajiban rutin pokok (bukan opsional), karena belum ada info kalau itu bisa dihentikan saat darurat.
- Tidak ada e-wallet top-up terpisah disebut; semua angka dianggap nominal pengeluaran riil.

## Langkah minggu ini
1. Hari gajian: langsung pindahkan **Rp830.000** ke rekening terpisah khusus dana darurat (bayar diri sendiri dulu) — ini sisa maksimal dari gaji rutin, jangan dipakai dulu untuk pos lain.
2. Saat THR cair (total **Rp12.500.000** gabungan suami+istri), setor **sekaligus** semuanya ke dana darurat — ini mempercepat target 9 bulan dari ~9 tahun menjadi ~4 tahun.
3. Rasio cicilan kalian **34,4%** (di atas batas aman 30%) — tunda dulu rencana utang baru (refinancing, cicilan lain, dsb.) sampai rasio ini turun.
4. Diskusikan dengan pasangan: apakah kiriman orang tua Rp1 juta bisa dihentikan sementara kalau ada kondisi darurat beneran — kalau bisa, target dana darurat turun jadi Rp88,65 juta (9 bulan), lebih ringan dicapai.
5. Tinjau ulang anggaran tiap 3 bulan, terutama setelah daycare/kebutuhan anak berubah; kalau mau coba pola 60/20/20, saya bisa hitungkan ulang.

⚠️ Bukan nasihat keuangan/investasi. Angka adalah simulasi dari data & asumsi di atas. Untuk kasus rumit, konsultasikan ke perencana keuangan bersertifikat.
````

**Lanjutan (pesan identik):**
> Kalau kiriman ke orang tua nggak dihitung, targetnya jadi berapa?

**Balasan SEBELUM:**

````markdown
Kalau pos kirim ke orang tua (Rp 1.000.000) dikeluarkan dari hitungan dana darurat, berarti basisnya jadi pengeluaran wajib bulanan yang lain saja:

**Pengeluaran bulanan (tanpa kirim ortu): Rp 10.670.000**

Target dana darurat baru:
- Minimum (6x): 6 × Rp 10.670.000 = **Rp 64.020.000**
- Ideal (9x): 9 × Rp 10.670.000 = **Rp 96.030.000**

Jadi turun dari 70jt/105jt menjadi ±64jt/96jt — selisihnya sekitar Rp 6-9 juta, lumayan membantu.

Tapi perlu dipikirkan: apakah kiriman ke orang tua itu realistis untuk dihentikan kalau salah satu dari kalian kena PHK atau sakit? Kalau orang tua kalian memang bergantung pada kiriman itu untuk kebutuhan hidup sehari-hari (bukan sekadar bonus), kemungkinan besar kalian akan tetap memaksakan kirim meski dalam kondisi darurat — jadi secara praktik, dana darurat yang lebih aman tetap pakai basis Rp 11.670.000 (termasuk kirim ortu).

Kalau kiriman itu sifatnya lebih fleksibel (bisa dikurangi/dihentikan sementara saat kondisi sulit tanpa dampak besar ke orang tua), maka target Rp 64-96 juta ini masuk akal dipakai.
````

**Balasan SESUDAH:**

````markdown
Kalau kiriman ke orang tua (Rp1.000.000/bulan) tidak dihitung sebagai pos pokok:

## Dana Darurat — Skenario Tanpa Kiriman Orang Tua

Pengeluaran pokok Rp9.850.000/bulan -> target dana darurat 9 bulan = Rp88.650.000; 12 bulan = Rp118.200.000.

**Perbandingan:**

| | Dengan kiriman ortu | Tanpa kiriman ortu |
|---|---:|---:|
| Pokok/bulan | Rp10.850.000 | Rp9.850.000 |
| Target 9 bulan | Rp97.650.000 | Rp88.650.000 |
| Target 12 bulan | Rp130.200.000 | Rp118.200.000 |

**Progres dengan saldo sekarang Rp8.000.000:**

| Target | Kurang | Progres | Lama tercapai (Rp830rb/bln saja) | Lama tercapai (+THR tiap cair) |
|---|---:|---:|---|---|
| 9 bulan | Rp80.650.000 | 9% | ~8 th 2 bln (98 bulan) | ~4 th 0 bln (48 bulan) |
| 12 bulan | Rp110.200.000 | 7% | ~11 th 1 bln (133 bulan) | ~5 th 0 bln (60 bulan) |

Jadi selisihnya Rp9 juta (9 bulan) hingga Rp12 juta (12 bulan) lebih ringan dibanding kalau kiriman ortu dihitung pokok — tapi target tercapainya hanya maju sekitar 1 tahun lebih cepat. Catatan: ini dihitung dengan asumsi kiriman ortu memang bisa dihentikan sementara kalau benar-benar darurat (bukan kewajiban yang tak tergoyahkan) — kalau kenyataannya tidak bisa dihentikan, pakai angka Rp97,65 juta / Rp130,2 juta dari perhitungan awal.

Sisa setoran bulanan dari gaji tetap sama: **Rp830.000/bulan** (angka ini tidak berubah oleh keputusan pokok/bukan-pokok, karena pos kiriman ortu tetap dibayar tiap bulan — yang berubah hanya seberapa besar target dana darurat yang perlu dicapai).

⚠️ Bukan nasihat keuangan/investasi. Angka adalah simulasi dari data & asumsi di atas.
````

**Verifikasi (Python independen + `keuangan.py` dijalankan penguji):**

| Angka | SEBELUM | SESUDAH | Hitungan penguji | Status |
|---|---|---|---|---|
| Total pos / sisa gaji rutin | Rp11.670.000 / Rp830.000 | sama | 11.670.000 / 830.000 | ✓ keduanya |
| Rasio cicilan (motor+KPR) | 34,4% | **34,4% DI ATAS 30%** (Ringkasan & Langkah 3) | 4.300.000 ÷ 12.500.000 = 34,4% | ✓ keduanya (temuan v1.0.8 #1 beres) |
| KPR di tabel | – | 24,8% (hanya di kolom pos) | 24,8% | ✓ tidak lagi disebut "rasio cicilan" |
| THR/12; % total dialokasikan | – | Rp1.041.666; 93,4% / 86,2% | 1.041.666; 93,36% / 86,18% | ✓ |
| Pokok dana darurat | 6×/9× total belanja Rp11.670.000 (termasuk Netflix/makan di luar) ≈ Rp70 jt / Rp105 jt | Rp10.850.000 → 9 bln Rp97.650.000; 12 bln Rp130.200.000 | 10.850.000; 97.650.000; 130.200.000 (70.020.000 / 105.030.000 untuk versi SEBELUM) | ✓ aritmetika keduanya; dasar SEBELUM memasukkan pos keinginan |
| Lama tercapai 9 / 12 bln | ±6 th ke 70 jt tanpa THR; ±3,3 th dengan 70% THR | 109 / 148 bln tanpa THR; 48 / 72 bln dengan THR (cair bulan ke-12) | 109 / 148; 48 / 72; 6,2 th; 3,31 th | ✓ |
| Progres | 0,7× | 8% / 6% | 8,2% / 6,1% | ✓ |
| Lanjutan tanpa kiriman ortu | Rp10.670.000 → 6× Rp64.020.000, 9× Rp96.030.000 | Rp9.850.000 → Rp88.650.000 / Rp118.200.000; kurang 80.650.000 / 110.200.000; 98 / 133 bln; 48 / 60 bln dengan THR; progres 9% / 7% | sama persis | ✓ keduanya |

Catatan kecil SESUDAH (bukan angka salah): (a) lanjutan menulis "target tercapainya hanya maju sekitar 1 tahun lebih cepat" — benar untuk 3 dari 4 kolom (109→98, 148→133, 72→60 bln), tetapi target 9 bulan **dengan THR tetap 48 bulan** (tidak maju); (b) Langkah 2 menyetor THR Rp12.500.000 seluruhnya ke dana darurat tanpa menyisakan pos Lebaran (mudik/baju/angpau) — SEBELUM justru menyisakan 30%; (c) banding pola menampilkan "Tabungan Rp0" padahal Langkah 1 menyetor Rp830.000 (sisa belum dijadikan pos tabungan di tabel, jadi zero-based belum benar-benar Rp0).

**Skor:** SEBELUM **6,5/10** — aritmetika benar, rasio cicilan benar, alur THR 70/30 realistis; tetapi dasar dana darurat memasukkan pos keinginan, kelipatan 6–9 bulan untuk keluarga beranak balita, menyebut reksa dana pasar uang (jenis produk), tanpa tabel. SESUDAH **8,5/10** — semua angka cocok dengan script & hitungan penguji, rasio cicilan kini benar dan kesimpulannya tegas, pos dimasukkan/dikeluarkan dijelaskan, lanjutan dihitung ulang script; dikurangi untuk tiga catatan kecil di atas. Skill terpakai (read + exec; lanjutan exec).

### Skenario 2 — defisit bulanan, THR cair 6 bulan lagi, tabungan kecil Rp1,5 juta (jebakan)

Angka pilihan penguji (berbeda dari putaran sebelumnya): gaji Rp6.200.000, pos Rp7.580.000 (termasuk arisan RT Rp200.000), THR Rp6.200.000 cair bulan ke-6, saldo tabungan Rp1.500.000 (bukan nol — menguji cabang "saldo ada tapi tidak cukup").

**Pesan:**
> Mas, gaji bersih saya 6,2 juta (karyawan pabrik di Karawang), istri di rumah, anak 1 SMP. Kontrakan 1,5 juta, cicilan motor 780 ribu, cicilan HP 450 ribu, belanja dapur 2,1 juta, listrik+air+gas 400 ribu, bensin 350 ribu, sekolah + uang saku anak 600 ribu, pulsa & wifi 250 ribu, kirim mertua 300 ribu, arisan RT 200 ribu, rokok 400 ribu, nongkrong & jajan 250 ribu. Tiap bulan kurang terus. THR 1x gaji baru cair 6 bulan lagi. Tabungan cuma sisa 1,5 juta. Gimana biar nggak minus tiap bulan?

**Balasan SEBELUM (tanpa skill):**

````markdown
Oke, saya hitung dulu angkanya. Total pengeluaran yang Mas sebutkan = **Rp7.580.000**, sementara gaji **Rp6.200.000**. Jadi defisitnya **Rp1.380.000/bulan** — itu sebabnya tabungan kemakan terus.

**Yang paling bisa dipotong (dari yang paling "nggak sakit" ke yang paling berat):**

1. **Rokok – 400rb** → ini pos terbesar yang 100% bisa dihilangkan/dikurangi tanpa korbankan kebutuhan anak-istri. Kalau bisa setop atau minimal setengahnya, langsung hemat 200–400rb.
2. **Nongkrong & jajan – 250rb** → pangkas ke 100rb, hemat 150rb.
3. **Bensin – 350rb** → kalau ada rekan kerja searah, coba nebeng/gantian bawa motor (carpool informal), lumayan ke pabrik Karawang biasanya rame yang searah. Bisa hemat 100–150rb.
4. **Pulsa & wifi – 250rb** → cek ulang paketnya, sering ada paket lebih murah atau gabung Wifi+pulsa jadi satu provider. Potensi hemat 30–50rb.

Kalau 4 ini digarap serius, bisa hemat sekitar **600–900rb/bulan** — belum nutup penuh defisit 1,38 juta, tapi sudah separuh jalan.

**Yang perlu dicek, bukan langsung dipotong:**

- **Cicilan HP – 450rb**: ini porsinya lumayan besar (±7% gaji). Tinggal berapa bulan lagi? Kalau itu dari pinjol/paylater (Kredivo, Akulaku, dll) dengan bunga tinggi, prioritaskan dilunasi duluan begitu ada dana lebih — jangan sampai nambah utang baru selama masih nyicil ini.
- **Arisan RT – 200rb**: ini sebenarnya "nabung paksa", bukan murni pengeluaran, tapi kalau lagi ketat, nggak masalah izin ke pengurus untuk cuti sementara atau ambil slot nanti belakangan.

**Yang jangan diotak-atik:** kontrakan, belanja dapur, sekolah anak, kirim mertua — ini kebutuhan pokok dan tanggung jawab, risikonya lebih besar kalau dipangkas.

**Soal belanja dapur (2,1 juta, pos terbesar):** bukan dipotong, tapi dioptimalkan — belanja mingguan di pasar/grosir bukan harian di warung/minimarket biasanya bisa hemat 10–15%, plus kurangi beli makan jadi/jajan di luar kalau ada.

**Untuk nutup sisa defisitnya, dua opsi realistis:**

- **Lembur di pabrik** kalau tersedia — biasanya ini jalan tercepat nambah penghasilan buat buruh pabrik, tanya ke atasan/HRD soal kuota lembur bulan ini.
- **Istri usaha kecil-kecilan dari rumah** — jualan jajanan, terima pesanan masakan, reseller online, apapun yang modalnya kecil. Nggak perlu besar, yang penting nambah arus kas bulanan.

**Soal tabungan Rp1,5 juta:** itu jangan disentuh dulu kecuali darurat beneran (sakit, motor rusak berat). Itu bantalan Mas satu-satunya sebelum THR cair 6 bulan lagi.

**Rencana simpel bulan depan:**
1. Potong rokok + nongkrong + bensin + pulsa → target hemat 700–900rb.
2. Cari lembur atau usaha sampingan istri → target tambahan 500rb+.
3. Kalau masih kurang, itu artinya cicilan HP yang jadi beban — percepat pelunasannya begitu ada rejeki lebih, baru napas.

Kalau mau, saya bisa bantu bikin breakdown bulanan lebih detail atau simulasi kalau sebagian pos dipangkas — tinggal bilang.
````

**Balasan SESUDAH (skill aktif):**

````markdown
Oke, saya hitungkan pakai angka beneran (bukan kira-kira), berdasarkan data yang Mas kasih.

## Ringkasan

Total pengeluaran Mas Rp7.580.000/bulan (termasuk arisan Rp200rb) lebih besar dari gaji rutin Rp6.200.000; tanpa pos tabungan pun pengeluaran Rp7.380.000/bulan → **DEFISIT Rp1.180.000/bulan** (dihitung dari gaji saja, karena THR cair sekali, bukan tiap bulan). Setelah semua pos yang masih bisa dipangkas dipotong habis, masih kurang **Rp560.000/bulan** — perlu tambahan pemasukan rutin atau meninjau pos besar (kontrakan/cicilan), **bukan** utang baru. Kabar baiknya: total cicilan Mas (motor+HP) cuma 19,8% dari gaji — masih di bawah batas aman 30%, jadi bukan cicilan yang jadi biang masalah, tapi memang gaji vs pengeluaran dapur+wajib yang terlalu mepet.

## Pos mana yang dipangkas (bertahap 3 bulan, bukan langsung)

- Rokok: Rp400.000 → Rp200.000 (potong 50%)
- Nongkrong & jajan: Rp250.000 → Rp130.000 (potong 48%)
- Belanja dapur: Rp2.100.000 → Rp1.890.000 (potong 10%)
- Listrik/air/gas: Rp400.000 → Rp360.000 (potong 10%)
- Bensin: Rp350.000 → Rp320.000 (potong ~9%)
- Pulsa & wifi: Rp250.000 → Rp230.000 (potong 8%)
- **Total hemat: Rp620.000/bulan** (setelah bulan ke-3)

Tempat tinggal, cicilan, sekolah anak, dan kiriman mertua **tidak dipotong** (itu kewajiban pokok, bukan sumber masalah).

Setelah dipotong penuh pun masih kurang **Rp560.000/bulan** — ini yang perlu ditutup dari sumber lain, bukan dikorbankan dari pos wajib.

## Jadwal kekurangan sampai THR cair (6 bulan lagi)

| Bulan | Kekurangan bulan itu | Kumulatif |
|---|---:|---:|
| 1 | Rp960.000 | Rp960.000 |
| 2 | Rp750.000 | Rp1.710.000 |
| 3 | Rp560.000 | Rp2.270.000 |
| 4 | Rp560.000 | Rp2.830.000 |
| 5 | Rp560.000 | Rp3.390.000 |
| 6 | THR cair bulan ini | — |

Saldo Mas sekarang Rp1.500.000 **tidak cukup** buat nutup kekurangan masa transisi ini (kurang Rp1.890.000 kalau mepet sampai bulan ke-5). Tiga pilihan tanpa utang:
1. **Percepat pemangkasan** — semua potongan langsung penuh mulai bulan ini juga (bukan bertahap 3 bulan), kekurangan sebelum THR cair turun dari Rp3.390.000 jadi Rp2.800.000.
2. **Tambah pemasukan sementara ~Rp380.000/bulan selama 5 bulan** — lembur, jualan kecil, jasa, jual barang nganggur.
3. **Tunda/kurangi sementara** pos yang masih bisa: kiriman mertua, rokok, nongkrong (kiriman mertua hanya kalau sudah dibicarakan baik-baik dulu).

**Jangan ditutup pakai paylater/pinjol/kartu kredit** — itu gali lubang tutup lubang, HP Mas sudah cicilan, jangan ditambah lagi.

## Saat THR cair (6 bulan lagi), Rp6.200.000

- Rp3.950.000 → otomatis menutup kekurangan masa transisi bulan 1–6
- Sisa Rp2.250.000 → Rp2.240.000 **dicadangkan** (jangan dipakai dulu) untuk menambal sisa defisit Rp560rb/bulan selama 4 bulan berikutnya (bulan 7–10)
- Mulai bulan ke-11, kalau sisa defisit masih ada, butuh sumber baru (bukan THR lagi) — makanya opsi tambah pemasukan rutin di atas penting, bukan cuma andalkan THR
- **Setoran dana darurat dari gaji = Rp0 dulu** sampai defisit ini beneran tertutup

## Dana darurat (gambaran, belum jalan dulu)

Pengeluaran pokok (sewa+cicilan+dapur+listrik+sekolah+kiriman mertua) = Rp6.730.000/bulan. Untuk status berkeluarga+anak, target 9–12 bulan = **Rp60.570.000 – Rp80.760.000**. Saldo sekarang Rp1.500.000 baru 2% dari target. Kalau kiriman mertua suatu saat bisa dihentikan sementara saat darurat, pokok turun ke Rp6.430.000 dan target turun ke Rp57.870.000/Rp77.160.000.

## Asumsi yang dipakai

- THR 1x gaji (Rp6.200.000), cair 6 bulan lagi (sesuai info Mas)
- Status: menikah + anak → target dana darurat 9–12 bulan pengeluaran pokok
- Saldo tabungan sekarang: Rp1.500.000
- Arisan RT dihitung sebagai tabungan (bukan pokok darurat), kiriman mertua dihitung sebagai kewajiban keluarga rutin

## Langkah minggu ini

1. Mulai pangkas 6 pos di atas — kalau sanggup, langsung penuh (bukan nunggu 3 bulan) biar kekurangan sebelum THR lebih kecil.
2. Cari tambahan ±Rp380.000/bulan selama 5 bulan ke depan (lembur pabrik, atau istri jualan kecil-kecilan di rumah — anak sudah SMP, biasanya ada waktu luang).
3. JANGAN setor ke dana darurat/arisan tambahan dulu sampai defisit bulanan ini tertutup — fokus bertahan dulu.
4. Begitu THR cair nanti, sisihkan Rp2.240.000-nya di rekening terpisah (jangan tercampur rekening harian) untuk nutup bulan 7–10, baru sisanya untuk dana darurat.
5. Ngobrol baik-baik sama istri soal kemungkinan kiriman ke mertua disesuaikan sementara kalau memang situasi makin berat — bukan dihentikan paksa, tapi dibicarakan.

⚠️ Bukan nasihat keuangan/investasi. Angka adalah simulasi dari data & asumsi di atas. Untuk situasi yang makin berat, boleh konsultasi ke perencana keuangan bersertifikat atau lembaga keuangan komunitas setempat.
````

**Verifikasi (Python independen + `keuangan.py` dijalankan penguji dengan `--status anak --saldo 1,5jt --bulan-cair 6`):**

| Angka | SEBELUM | SESUDAH | Hitungan penguji | Status |
|---|---|---|---|---|
| Total pos / defisit | Rp7.580.000 / Rp1.380.000 | Rp7.580.000; defisit Rp1.180.000 (arisan Rp200.000 diperlakukan sebagai tabungan) | 7.580.000; 1.380.000 (semua pos) / 1.180.000 (tanpa arisan) | ✓ keduanya, beda basis (lihat catatan arisan) |
| Rasio cicilan | – (cicilan HP "±7% gaji") | 19,8% di bawah 30% | 1.230.000 ÷ 6.200.000 = 19,84%; HP 7,26% | ✓ |
| Potensi pemangkasan | "600–900rb/bulan" | Rp620.000 (rincian 6 pos) | rincian SEBELUM sendiri: 200–400 + 150 + 100–150 + 30–50 = **Rp480.000–750.000** | ✗ SEBELUM melebih-lebihkan; ✓ SESUDAH |
| Sisa defisit setelah pangkas | "belum nutup penuh … separuh jalan" | Rp560.000/bulan | 1.180.000 − 620.000 = 560.000 | ✓ |
| Kekurangan bulan 1–6 | tidak dibahas | 960.000 / 750.000 / 560.000 ×4; kumulatif s.d. bulan 5 Rp3.390.000 | 960.000; 1.710.000; 2.270.000; 2.830.000; 3.390.000; 3.950.000 | ✓ |
| Saldo vs kekurangan pra-THR | "jangan disentuh kecuali darurat" | saldo Rp1.500.000 TIDAK cukup, kurang Rp1.890.000; percepat → Rp2.800.000; tambah ±Rp380.000/bln × 5 | 1.890.000; 5 × 560.000 = 2.800.000; 1.890.000 ÷ 5 = 378.000 | ✓ (temuan v1.0.8 #3 beres — tidak lagi "talangi dari saldo" tanpa sumber) |
| Pemakaian THR | – | Rp3.950.000 tutup bulan 1–6; sisa Rp2.250.000, Rp2.240.000 dicadangkan untuk 4 bulan (bulan 7–10); DD Rp0 sampai defisit tertutup | 6.200.000 − 3.950.000 = 2.250.000; ⌊2.250.000 ÷ 560.000⌋ = 4; 4 × 560.000 = 2.240.000 | ✓ (temuan v1.0.8 #2 beres) |
| Dana darurat | tidak dibahas | pokok Rp6.730.000; 9/12 bln Rp60.570.000 / Rp80.760.000; tanpa mertua Rp6.430.000 → Rp57.870.000 / Rp77.160.000; progres 2% | sama persis; progres 2,48% / 1,86% | ✓ |
| Baris "defisit vs gaji+THR/12" | – | tidak muncul | – | ✓ (temuan v1.0.8 #4 beres) |

Catatan SESUDAH: (a) **arisan RT diam-diam berhenti dibayar.** Script/agent mengklasifikasikan arisan Rp200.000 sebagai "tabungan" lalu menyetel setoran tabungan Rp0 selama defisit, sehingga defisit menjadi Rp1.180.000 — tetapi balasan tidak pernah berkata terang "izin cuti/berhenti sementara dari arisan RT" (Langkah 3 hanya "JANGAN setor ke dana darurat/arisan tambahan", yang bisa dibaca arisan yang sudah berjalan tetap dibayar). Bila arisan tetap dibayar, kekurangan riil bulan 1–5 = Rp4.390.000 (bukan Rp3.390.000) dan sisa defisit setelah pangkas Rp760.000/bulan (bukan Rp560.000). Script sendiri juga mencetak dua angka defisit (Rp1.180.000 di ringkasan, Rp1.380.000 di catatan pemasukan). SEBELUM justru menyarankan izin ke pengurus arisan. (b) Label "pokok (sewa+cicilan+dapur+listrik+sekolah+kiriman mertua)" tidak menyebut bensin & pulsa, meski angkanya sudah memasukkan keduanya. (c) Tabel jadwal baris bulan 6 tertulis "—" padahal kekurangan Rp560.000 bulan itu ikut ditutup THR (angka Rp3.950.000 tetap benar).

**Skor:** SEBELUM **6/10** — ramah, defisit Rp1.380.000 benar, ide lembur/usaha istri dan izin arisan bagus; tetapi klaim hemat "600–900rb" melebihi rinciannya sendiri (maks. Rp750.000), tidak ada rencana 5 bulan sebelum THR, tidak ada target dana darurat. SESUDAH **8/10** — semua nominal cocok dengan script & hitungan penguji, ketiga temuan v1.0.8 terkait S2 beres (saldo tidak cukup → pilihan konkret tanpa utang; sisa THR dicadangkan untuk bulan 7–10; dana darurat ditunda; baris THR/12 hilang); dikurangi karena perlakuan arisan tidak dijelaskan ke pengguna. Skill terpakai (read + exec).

### Ringkasan uji ulang v1.0.9

- **Skor rata-rata:** SEBELUM 6,25 → SESUDAH 8,25 (S1 6,5 → 8,5; S2 6 → 8).
- **Temuan v1.0.8:** ✓ #1 rasio cicilan 34,4% DI ATAS 30% disalin benar (Ringkasan & Langkah), 24,8% hanya di kolom KPR; ✓ #2 sisa THR dicadangkan untuk sisa defisit (bulan 7–10), dana darurat baru diisi setelah defisit tertutup; ✓ #3 saldo kecil tidak cukup → disebut terang + tiga pilihan tanpa utang dengan nominal; ✓ #4 baris defisit basis THR/12 tidak lagi muncul.
- **Kesalahan angka:** tidak ada di SESUDAH (semua nominal & persen cocok dengan Python independen). SEBELUM: satu (klaim hemat 600–900rb vs rincian maks. Rp750.000).
- **VERDIK: LULUS** — sesudah 8,25 ≥ 8, jelas di atas sebelum, tanpa kesalahan fakta/angka. Dua catatan RENDAH di bawah untuk revisi ringan (tidak perlu uji ulang penuh).

**Cacat untuk pembuat (RENDAH):**
1. **Arisan sebagai "tabungan" saat defisit.** Bukti: S2 defisit Rp1.180.000 (arisan dikeluarkan), setoran tabungan Rp0, tetapi balasan tidak menyuruh pengguna menghentikan/izin cuti arisan; bila tetap dibayar, kekurangan pra-THR Rp4.390.000 bukan Rp3.390.000. Script juga mencetak Rp1.380.000 di catatan pemasukan. Saran: saat defisit dan ada pos tabungan berjenis arisan, script mencetak kalimat siap tempel "Rencana ini menganggap arisan Rp… DIHENTIKAN/ditunda sementara (bicarakan dengan pengurus); bila tetap dibayar, kekurangan menjadi Rp…/bulan" — atau perlakukan arisan berjalan sebagai kewajiban (bukan setoran yang bisa di-nol-kan) secara bawaan.
2. **Narasi "maju sekitar 1 tahun".** S1 lanjutan: target 9 bulan dengan THR tetap 48 bulan (tidak maju). Saran: script mencetak selisih lama tercapai per kolom di skenario alternatif, atau SKILL.md melarang meringkas selisih waktu tanpa angka script. Pertimbangkan juga pengingat menyisakan pos Lebaran saat menyarankan THR "disetor seluruhnya".

**Cuplikan jualan:**
- Tanpa skill: "Potong rokok, nongkrong, bensin, pulsa — bisa hemat 600–900rb" (rinciannya sendiri maks. Rp750.000) dan 6 bulan sebelum THR tidak direncanakan. Dengan skill: "Pemangkasan bertahap −Rp620.000, sisa defisit Rp560.000/bulan dijelaskan terus terang; kekurangan sampai THR cair Rp3.390.000, tabungan Rp1,5 juta tidak cukup → kurang Rp1.890.000: tambah pemasukan ±Rp380.000/bulan atau percepat pemangkasan — tanpa paylater. Saat THR cair, Rp2.240.000 dicadangkan untuk bulan 7–10."
- Keluarga muda Bekasi: dengan skill, rasio cicilan 34,4% langsung ditandai DI ATAS batas aman 30%, dan dana darurat dihitung dari pengeluaran pokok (Rp10.850.000 → target 9 bulan Rp97.650.000), bukan dari total belanja termasuk Netflix.
