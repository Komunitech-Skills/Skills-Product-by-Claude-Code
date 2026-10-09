# Uji ULANG 02 — Budget bulanan & dana darurat dari mutasi rekening

Tanggal: 2026-10-01 (Asia/Jakarta) · Penguji independen (bukan pembuat) · OpenClaw lokal (`openclaw agent --local`), model router Komunitech yang sama dengan bot member · home `sol2-kripto-keuangan` (6 skill paket; `atur-keuangan-pribadi` 1.0.5, `pantau-pasar-kripto` 1.0.5), **direset bersih sebelum skenario**. Pesan, jawaban lanjutan, dan data file identik dengan uji asal.

Pembanding: [02-budget-dana-darurat-mutasi.md](02-budget-dana-darurat-mutasi.md) (SESUDAH lama 8). Data: `mutasi-september.csv` yang sama (24 baris) disalin ke workspace.

## Pesan member

> kak ini mutasi rekening saya bulan september, filenya mutasi-september.csv. tolong bikinin budget bulanan yg masuk akal ya, sama dana darurat saya harusnya berapa. saya udah nikah anak 1, istri ga kerja. tabungan saya sekarang cuma 4 juta. jujur tiap akhir bulan suka mepet 😅

## Tool yang dipakai

read, ls, exec (daftar dari JSON hasil). Penguji tidak membaca database sesi (dilarang), jadi isi perintah `exec` tidak dilihat; tidak ada tanda pencarian `find /` di keluaran. Rincian pokok di balasan identik dengan keluaran `keuangan.py dana-darurat` yang dijalankan ulang penguji.

## Balasan utuh (4.846 karakter)

> Oke, saya sudah hitung dari mutasi CSV-nya pakai alat budgeting (bukan kira-kira). Ini hasilnya:
>
> ## Ringkasan
> Bulan September kamu defisit **Rp1.709.800** (pemasukan Rp10.758.200, keluar Rp12.468.000) — penyebab utamanya bukan kebutuhan pokok, tapi top-up Indodax 2× Rp2.500.000 (26% gaji) plus belanja kecil-kecil via e-wallet/QRIS yang nggak kerasa. Kebutuhan wajib kamu sendiri sudah 66% dari gaji (wajar untuk keluarga dengan 1 anak di kota, tapi artinya ruang geraknya sempit), jadi solusinya bukan potong makan/sewa, tapi rem top-up kripto dulu & rapikan jajan. Dana darurat idealmu (menikah + anak) itu **9–12× Rp6.282.500 = Rp56,5–75,4 juta** — dari saldo Rp4 juta sekarang, ini jalan panjang (6–8 tahun di setoran wajar), tapi target antara "1 bulan pokok" (~Rp6,3jt) bisa kamu capai dalam ~4-5 bulan kalau mulai sekarang.
>
> ## Realisasi September vs Usulan Anggaran (gaji Rp9.500.000/bln)
>
> | Pos | Realisasi Sep | Usulan (steady-state) | Catatan |
> |---|---:|---:|---:|
> | Kontrakan | Rp2.000.000 | Rp2.000.000 | tetap |
> | Cicilan motor Adira | Rp1.150.000 | Rp1.150.000 | tetap |
> | Cicilan Shopee Paylater | Rp650.000 | Rp650.000 | tetap, tapi jangan nambah paylater baru |
> | Token PLN + Pulsa/kuota | Rp500.000 | Rp500.000 | tetap |
> | SPP PAUD anak | Rp350.000 | Rp350.000 | tetap |
> | Belanja bulanan & dapur | Rp1.500.000 | Rp1.500.000 | tetap |
> | Bensin + admin bank | Rp132.500 | Rp132.500 | tetap |
> | **Subtotal Kebutuhan wajib** | **Rp6.282.500 (66%)** | **Rp6.282.500 (66%)** | sudah di atas pola 50/30/20 — wajar untuk keluarga, bukan masalahnya |
> | Kiriman ortu | Rp1.000.000 | Rp1.000.000 | tetap |
> | Arisan RT | Rp500.000 | Rp500.000 | tetap (ini tabungan berputar) |
> | **Jajan/e-wallet/QRIS/tarik tunai** | **Rp2.185.500 (23%)** | **Rp1.000.000 (10,5%)** | ⚠️ turun 54% — **bertahap 3 bulan**, lihat di bawah |
> | **Top-up Indodax (kripto)** | **Rp2.500.000 (26%)** | **Rp0** | ⚠️ setop dulu, dialihkan ke dana darurat sampai dana darurat 1 bulan pokok aman |
> | Dana darurat (setoran baru) | Rp0 | Rp717.500 | baru, diambil dari jatah kripto+jajan di atas |
> | **Total** | **Rp12.468.000 (defisit)** | **Rp9.500.000 (pas Rp0)** | |
>
> **Jembatan 3 bulan** (biar nggak kaget, potongannya besar jadi dicicil):
> | Bulan | Jajan/e-wallet | Dana darurat |
> |---|---:|---:|
> | Okt | Rp1.500.000 | Rp217.500 |
> | Nov | Rp1.250.000 | Rp467.500 |
> | Des dst | Rp1.000.000 | Rp717.500 |
> (Kripto top-up: langsung ke Rp0 bulan ini — itu akar defisitnya.)
>
> ## Dana Darurat
> Status: menikah + 1 anak, istri tidak kerja → target **9–12 bulan** pengeluaran pokok.
> Pengeluaran pokok (sewa + makan + listrik + cicilan motor + cicilan paylater + SPP + bensin, dll) = **Rp6.282.500/bulan**.
>
> | Target | Jumlah | Kekurangan dari Rp4jt | Lama (setoran Rp717.500/bln) |
> |---|---:|---:|---:|
> | 1 bulan (milestone awal) | Rp6.282.500 | Rp2.282.500 | **~4–5 bulan** (dengan ramp di atas) |
> | 9 bulan | Rp56.542.500 | Rp52.542.500 | ~6 tahun 2 bulan |
> | 12 bulan | Rp75.390.000 | Rp71.390.000 | ~8 tahun 4 bulan |
>
> Angka 6-8 tahun itu memang berat kalau cuma andalkan setoran rutin — kalau ada proyek desain freelance (kamu dapat Rp1.250.000 bulan lalu) atau THR/bonus nanti, arahkan **100%-nya** ke dana darurat dulu, itu bisa pangkas waktunya signifikan.
>
> ## Asumsi yang dipakai
> - Pemasukan dasar hanya gaji tetap Rp9.500.000; proyek desain freelance (Rp1.250.000 bulan lalu) dianggap bonus tidak rutin, bukan bagian anggaran tetap.
> - Paylater Shopee dihitung sebagai cicilan wajib (bukan "keinginan") karena itu kewajiban utang, bukan belanja baru.
> - Arisan dihitung sebagai tabungan (uangnya kembali saat giliran), bukan pengeluaran hangus.
> - Top-up e-wallet (Gopay/OVO) dan tarik tunai digabung ke kategori Keinginan karena polanya konsumtif di mutasi (QRIS Indomaret/KFC/Shopee order).
> - Dana darurat disimpan terpisah, instrumen yang cepat cair & stabil nilainya (bukan aset yang naik-turun harga) — ini bukan rekomendasi beli/jual produk tertentu.
>
> ## Langkah minggu ini
> 1. Setop auto top-up/transfer rutin ke Indodax bulan ini — redirect Rp2,5jt itu ke rekening/pos "Dana Darurat" terpisah.
> 2. Buat akun/pos terpisah khusus dana darurat (bukan tabungan utama), isi Rp217.500 minggu ini sebagai setoran pertama.
> 3. Cek 1 minggu pemakaian Gopay/OVO — biasanya topup "menguap" jadi jajan tanpa sadar; targetkan jajan+e-wallet turun jadi Rp1,5jt bulan ini dulu (bukan langsung Rp1jt).
> 4. Jangan tambah paylater/pinjol baru untuk nutup bulan mepet — itu justru bikin lubang baru.
> 5. Tandai di kalender: cek progres dana darurat tiap akhir bulan, target milestone pertama Rp6,3jt (1 bulan pokok) tercapai sekitar Februari 2027 kalau konsisten.
>
> ⚠️ Bukan nasihat keuangan/investasi. Angka adalah simulasi dari data mutasi & asumsi di atas. Untuk kasus yang lebih rumit (mis. strategi kripto, utang bertambah), konsultasikan ke perencana keuangan bersertifikat.
## Verifikasi independen penguji (python + `keuangan.py` dijalankan ulang di salinan)

- Total keluar Rp12.468.000, masuk Rp10.758.200, defisit Rp1.709.800 ✅.
- Kebutuhan wajib = 2.000.000 + 1.150.000 + 650.000 + 500.000 + 350.000 + 1.500.000 + 132.500 = **Rp6.282.500** (66,1% gaji) ✅. Jajan/e-wallet = GoPay 500rb + Indomaret 287,5rb + KFC 186rb + OVO 300rb + Shopee 412rb + ATM 500rb = **Rp2.185.500** ✅. Realisasi menjumlah Rp12.468.000 ✅. Usulan menjumlah tepat Rp9.500.000 ✅ (juga baris Okt: jajan 1,5 jt + DD 217,5rb).
- Potongan jajan 1 − 1.000.000/2.185.500 = 54,2% ✅ ("turun 54%").
- Dana darurat: 6.282.500 × 9 = Rp56.542.500, × 12 = Rp75.390.000 ✅; (56.542.500 − 4 jt)/717.500 = 73,2 → 74 bln (6 th 2 bln) ✅; 99,5 → 100 bln (8 th 4 bln) ✅. Milestone 1 bulan pokok dengan ramp 217,5rb → 467,5rb → 717,5rb: tercapai bulan ke-5 (Feb 2027) ✅.
- `keuangan.py dana-darurat --pos … --cicilan "Motor=1,15jt" --cicilan "PayLater=650rb" --status anak --saldo 4jt --setoran 717500` → angka identik dengan balasan.

## Cacat lama

| Cacat lama | Hilang? | Bukti |
|---|---|---|
| Pokok dana darurat tanpa cicilan PayLater | **ya** | *"Pengeluaran pokok (sewa + makan + listrik + cicilan motor + cicilan paylater + SPP + bensin, dll) = Rp6.282.500/bulan"* |
| Pos jajan dipotong tajam tanpa catatan | **ya** | tabel "Realisasi Sep vs Usulan" + *"⚠️ turun 54% — bertahap 3 bulan"* + tabel jembatan Okt/Nov/Des. Sangat baik. |
| `find /` ke seluruh disk | **kemungkinan ya** | tool hanya `read`, `ls`, `exec`; balasan tidak menyebut lokasi lain. Tidak dapat dipastikan 100% tanpa membaca database sesi. |

## Regresi / temuan baru

1. **Kiriman ortu Rp1.000.000 keluar dari pengeluaran pokok — diam-diam.** Uji lama memasukkannya; SKILL.md 1.0.5 langkah 5 sendiri menulis pokok mencakup *"kiriman keluarga yang tidak bisa ditunda"*, dan catatan `keuangan.py` juga. Agent tidak bertanya dan tidak menyebut bahwa kiriman ortu dikeluarkan. Belanja Indomaret Rp287.500 juga dipindah ke "jajan". Akibatnya dasar dana darurat **Rp6.282.500**, lebih kecil dari uji lama (Rp6.907.500) dan dari angka yang diharapkan penguji (±Rp7,3–7,6 jt). Target 9 bulan **Rp56,5 jt vs ±Rp66–68 jt** bila kiriman ortu masuk → kekecilan ±Rp9–11,6 jt, **lebih besar** dari cacat lama (±Rp5,85 jt). Arah cacat lama (target kekecilan) belum tuntas, hanya berpindah pos.
2. **Kontradiksi kecil:** Langkah 1 *"redirect Rp2,5jt itu ke … pos Dana Darurat"*, padahal tabel hanya menyetor Rp217.500 (Okt) – Rp717.500; sisa uang Indodax terpakai menutup defisit. Member bisa bingung.
3. Frasa *"top-up Indodax 2× Rp2.500.000"* ambigu (sebenarnya 2 kali, total Rp2,5 jt).
4. Panjang 4.846 karakter — panjang untuk chat, tetapi isi tabel memang padat dan relevan.

## Nilai

| | Sesudah lama | Ulang 1.0.5 |
|---|---|---|
| Skor (1–10) | 8 | **8** |

Perbaikan nyata (PayLater masuk, realisasi vs anggaran + jembatan bertahap sangat membantu awam), tetapi target dana darurat tetap kekecilan karena kiriman ortu dikeluarkan tanpa penjelasan — pelanggaran aturan skill sendiri. Saran: di `anggaran`, pos kelompok "Keluarga & sosial" (kiriman ortu) ikut "Dasar dana darurat" secara default dan dicetak; SKILL.md mewajibkan agent menyebut pos yang **dikeluarkan** dari pokok beserta alasannya, atau menanyakannya sekali.
