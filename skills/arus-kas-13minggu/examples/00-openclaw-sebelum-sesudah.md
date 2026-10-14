# Uji OpenClaw SEBELUM vs SESUDAH: arus-kas-13minggu

## Uji ulang per skill v1.0.4 (2026-10-14, penguji independen)

**Cara uji:** OpenClaw 2026.10.2 lokal (`openclaw agent --local`, satu giliran per panggilan), model router Komunitech (`ninerouter/komunitech`). Setiap sampel memakai home baru yang terisolasi. **SEBELUM** = home tanpa skill. **SESUDAH** = home berisi `arus-kas-13minggu` 1.0.4 saja (folder skill dari repo). Ini **uji per skill**, bukan paket solusi 17 skill seperti uji 2026-10-01. Ada 5 skenario, masing-masing 1 sampel per sisi, dan **kedua sisi dijalankan ulang**. Skenario 01 juga dijalankan dalam konteks kanal Telegram (`--channel telegram`, tanpa `--deliver`, tidak ada yang dikirim). Pesan member identik di kedua sisi dan datanya fiktif. Semua sampel memakai mulai minggu 1 = Senin 19 Okt 2026.

**Verifikasi angka independen** dilakukan dengan Python (tidak mengimpor script skill): saldo mingguan, minggu negatif/di bawah batas, arus kas bersih, dan setiap opsi yang disebut dihitung ulang. Batas aman default = rata-rata pengeluaran 1 minggu, sesuai SKILL.md.

| # | Skenario (pesan member, ringkas) | Angka acuan |
|---|---|---|
| 01 | Usaha kue: kas 15 jt, jual 9 jt/mg, bahan 4,5 jt/mg, gaji 9 jt tgl 28, sewa, cicilan oven, listrik, hampers DP 11 jt 20 Nov + 11 jt 15 Jan, mixer 15 jt 3 Nov, bonus 9 jt 23 Des. "Aman nggak?" | **Minggu 3 negatif −Rp700.000**, di bawah batas minggu 2, 4, 11, 12; bersih +Rp7.600.000 |
| 02 | File CSV CV (format bebas: tanggal;keterangan;masuk;keluar), saldo 64,25 jt, batas aman 25 jt | Terendah minggu 12 Rp18.850.000, minggu 12–13 di bawah batas, **defisit struktural −Rp45.400.000** |
| 03 | Bengkel: kas 12 jt, tawaran armada (beli oli 9 jt 10 Nov, dibayar 18 jt 21 Des). "Aman gak kalau saya ambil?" | Dengan order: **minggu 7–9 negatif**, terendah −Rp1.250.000; tanpa order tidak negatif |
| 04 | Laundry: gaji karyawan tanpa angka, omzet berupa rentang. "Cukup ga sampe tahun baru?" | Harus bertanya (gaji), bukan mengarang |
| 05 | Toko sembako: DP kulkas 12 jt; "mending tunda setor pajak & telat gaji seminggu, atau ambil pinjol?" | Negatif minggu 3–13 (terendah −Rp6.200.000); tidak boleh menyarankan menunda pajak/gaji |

| Skenario | Skor tanpa skill | Skor dengan skill | Alasan |
|---|:-:|:-:|---|
| 01 Usaha kue (lokal) | 6,5 | 8,5 | Tanpa skill: model harian (bukan mingguan), kesimpulan benar "tidak aman, minus 3 Nov" dan saran tunda mixer, tetapi tanpa tabel per minggu, tanpa batas aman, angka "~", dan satu kalimat urutan tanggal kacau ("28 Des (gajian) → 23 Des (bonus)"). Dengan skill: tabel 13 minggu **cocok 100%**, penyebab minggu 3 tepat, surplus +Rp7.600.000 (bukan defisit struktural), dan listrik 20 Jan setelah minggu 13 disebut. Opsi "tunda mixer ke minggu 7" benar (terendah Rp4.700.000). **Cacat:** opsi "percepat DP" ditulis hanya untuk DP 20 Nov, padahal hasil Rp9.800.000 dari script juga memajukan pelunasan 15 Jan ke minggu 11 (`rincian_digeser` memuat dua pos). Bila hanya DP yang dimajukan, terendah Rp4.700.000. |
| 01 konteks Telegram | **3** | 8,5 | Tanpa skill: **"kas kakak aman untuk 3 bulan ke depan, saldo nggak pernah minus"**, titik terendah "5,6 jt". Ini salah karena gaji 9 jt tgl 28 Okt dan listrik 20 Okt terlewat; yang benar, minggu 3 minus. Dengan skill: angka sama dengan sampel lokal, tabel ditulis sebagai daftar per minggu (cocok untuk Telegram), dengan rekomendasi tegas "cukup Opsi 1 (tunda mixer)" dan disclaimer. Cacat opsi "percepat DP" sama dengan sampel lokal. |
| 02 CSV CV + batas aman | 6,5 | 8,5 | Kedua sisi menghasilkan tabel yang benar dan menandai minggu 12–13. Tanpa skill: **defisit struktural −Rp45,4 jt tidak disebut**, enam saran tanpa angka, dan dua di antaranya (bonus dimajukan ke awal Des, nego supplier panel 20 Nov) tidak menyentuh saldo minggu 12. Dengan skill: defisit struktural dijelaskan, opsi berangka **semuanya cocok** (naik pemasukan +1 jt/mg → terendah Rp30.850.000; material 7 jt/mg → Rp39.750.000; cicil izin → minggu 12 Rp23.600.000; nego panel tidak berpengaruh), dan opsi "geser semua belanja material" dari script ditolak dengan alasan. **Cacat:** agent menjalankan `find /` untuk mencari CSV (melanggar aturan kerja SKILL.md; sisi tanpa skill juga), memakai `/tmp/hasil.json`, dan **waktu proses 628 detik**. |
| 03 Bengkel ambil order? | 6,5 | 9 | Tanpa skill: arah benar (minus awal Des, minta DP), tetapi **listrik 22 Okt terlewat** sehingga semua saldo meleset Rp850.000 (terendah −Rp400.000 vs −Rp1.250.000), saran tanpa simulasi, dan ada komentar "PT Kurir Fiktif berarti perusahaan palsu, red flag". Dengan skill: tabel **cocok 100%**. Penyebab dijelaskan (oli 9 jt minggu 4 menguras cadangan, sewa minggu 7) dan dibandingkan dengan kondisi tanpa order (−Rp380 rb/mg). Opsi berangka **cocok**: DP 50% → terendah Rp7.750.000; termin toko oli ke minggu 10 → Rp7.750.000; gabungan → Rp10.050.000 tanpa minggu di bawah batas; saldo akhir Rp16.050.000. Catatan: 382 detik, sebagian untuk men-debug bug CSV script (lihat Catatan jujur). |
| 04 Info kurang (laundry) | 7,5 | 8 | Tanpa skill: menanyakan gaji sambil memberi kerangka hitung dan jawaban bersyarat ("cukup selama gaji total ≤ ~12–13 jt/bulan"). Ini berguna, meski kasar. Dengan skill: satu pesan, 4 pertanyaan bernomor, hanya no. 1 (gaji) wajib dan sisanya diberi default (batas aman, tanpa piutang). Sesuai SKILL.md, tetapi tanpa gambaran awal. Ada satu salah ketik ("sekali-lagi"). |
| 05 Tunda pajak/gaji atau pinjol? | — | — | **Tidak dapat dinilai.** SEBELUM: router *model idle timeout* (513 detik, tanpa jawaban). SESUDAH: agent membaca SKILL.md dan `opsi-tindakan.md`, menyusun CSV dengan benar (gaji/pajak kritis, DP kulkas tidak kritis), lalu menjalankan ±10 simulasi terpisah (DP dicicil, DP separuh, tambah omzet, pangkas belanja, gabungan) dan **kehabisan batas waktu 800 detik sebelum menulis jawaban**. Uji ulang tidak bisa dijalankan karena instalasi alat uji OpenClaw di VM sudah terhapus. |
| **Rata-rata skenario 01–04 (lokal)** | **6,75** | **8,5** | **Selisih +1,75** |

**Verdik: LULUS** pada 4 skenario yang dapat dinilai (sesudah 8,5 ≥ 8, selisih 1,75 ≥ 1,5). **Pra-cek konteks Telegram skenario 01: LOLOS**, karena tabel lengkap ditulis di chat dalam bentuk daftar yang aman untuk Telegram, dan CSV hanya tambahan. Lulus ini **dengan catatan wajib**: risiko waktu proses (lihat butir 1 di bawah) harus ditangani sebelum skill ditampilkan di bot asli. Skenario 05 perlu dijalankan ulang setelah perbaikan.

**Pembeda (satu kalimat):** Tanpa skill, model bisa salah menyimpulkan "kas aman, tidak pernah minus" (konteks Telegram, gaji 28 Okt terlewat), melewatkan pos rutin, dan memberi saran tanpa angka yang kadang tidak menyentuh minggu kritis. Dengan skill, tabel 13 minggu cocok 100% dengan hitungan independen di semua skenario yang dinilai, defisit struktural (−Rp45,4 jt) terdeteksi, dan setiap opsi disimulasikan dengan angka (mis. DP 50% + termin oli → saldo terendah Rp10.050.000).

**Catatan jujur (untuk pembuat skill, bukan diubah penguji):**
1. **Waktu proses panjang.** SESUDAH: S1 92 detik, S1 Telegram 163 detik, S2 628 detik, S3 382 detik, dan S5 **timeout pada 800 detik** setelah ±10 run script. Penyebabnya, agent membuat satu CSV + satu run per opsi (langkah 5–6 SKILL.md) tanpa batas jumlah run. Usul: batasi 1 run dasar + simulasi bawaan script + maksimal 2 run tambahan, lalu tulis jawaban. Usul lain, script menerima beberapa skenario dalam satu panggilan.
2. **Opsi "percepat piutang" menggeser semua baris piutang**, tetapi narasi agent hanya menyebut satu (S1 lokal & Telegram). Usul: SKILL.md mewajibkan menyebut setiap baris di `rincian_digeser`, atau script memberi opsi per pos.
3. **Bug script (direproduksi pada `scripts/proyeksi_kas.py` 1.0.4):** jika satu baris memiliki pemisah `;` berlebih di akhir (mis. `10;masuk;Pelunasan piutang;18.000.000;;;`), `csv.Sniffer` gagal dan script jatuh ke pemisah koma. Akibatnya seluruh file ditolak dengan "Kolom wajib tidak ditemukan: kategori, nominal". `--pemisah` hanya berlaku untuk output, jadi tidak bisa menolong. Di S3 agent menghabiskan beberapa giliran untuk men-debug ini. Usul: bila kolom wajib tidak ditemukan, coba ulang dengan `;`, `,`, tab, dan `|` berdasarkan baris judul.
4. Aturan kerja yang masih dilanggar: `find /` untuk mencari file member (S2; model tanpa skill juga melakukannya), serta file sementara di `/tmp` (S1 Telegram, S3).
5. Satu sampel per sisi per skenario. Skor SEBELUM 7,5 di uji 2026-10-01 tidak terulang (kini 6,5–7,5, dan 3 di konteks Telegram). Lampiran CSV tidak dinilai sebagai file Telegram, hanya namanya di chat.

---

**Sumber (ada di paket VIP):** `solusi-vip/kantor-manajemen/UJI-OPENCLAW.md` (tabel skor skenario 05, bagian "Cacat per skill", "Cuplikan jualan" dan "Uji ulang ke-3 2026-10-01") dengan rincian per skenario di `solusi-vip/kantor-manajemen/uji-openclaw/05-arus-kas-13-minggu-info-kurang.md` dan `05-arus-kas-13-minggu-ulang3.md`.
**Tanggal uji:** 2026-10-01 (Asia/Jakarta).
**Versi skill saat uji:** uji pertama kira-kira 1.0.2 (disimpulkan dari riwayat `catalog.csv` sebelum perbaikan pasca-uji; berkas sumber tidak menyebut versi), uji ulang = 1.0.3. Versi di katalog saat ini: 1.0.3.
**Penguji (agent):** agent penguji independen (bukan pembuat skill); uji ulang oleh penguji independen ke-3 untuk paket kantor-manajemen (satu-satunya uji ulang skill ini).

> Berkas ini ringkasan yang disalin dari catatan uji solusi VIP Kantor & Manajemen (uji dilakukan per solusi, bukan per skill). Angka disalin apa adanya dari sumber.

## Cara uji
- OpenClaw lokal (`openclaw agent --local`, tanpa Telegram/gateway). Model: router Komunitech `ninerouter/komunitech` (dilayani `claude-sonnet-5`), sama dengan bot member.
- **SEBELUM** = home `kosong-kantor-manajemen` (tanpa skill). **SESUDAH** = home `sol-kantor-manajemen` (17 skill paket terpasang); uji ulang di home `sol3-kantor-manajemen` dari skill terbaru repo. Kedua home dibuat ulang bersih sebelum skenario; pesan dan jawaban lanjutan identik.
- Skenario "info kurang lalu dilengkapi": member hanya memberi saldo awal, agent bertanya sekali, member menjawab satu kali (sama di kedua sisi).
- Uji ulang hanya mengulang sisi SESUDAH; skor SEBELUM dipakai ulang dari uji pertama. Saldo mingguan, total, dan simulasi dihitung ulang penguji dengan Python.

**Pesan member (skenario 05, giliran 1):** "bikinin proyeksi arus kas 13 minggu dong. saya takut kas ga cukup buat gaji akhir bulan. saldo kas sekarang sekitar 380 juta" (giliran 2: data pemasukan Rp210 jt per minggu (minggu 1-2 hanya Rp150 jt), gaji Rp420 jt tiap tanggal 25, supplier Rp130 jt per minggu, sewa Rp75 jt tanggal 5, cicilan Rp62 jt tanggal 15, batas aman Rp100 jt, mulai Senin 5 Oktober).

## Skor

| Skenario | Versi skill | Skor tanpa skill | Skor dengan skill | Pembeda (satu kalimat) |
|---|---|:-:|:-:|---|
| 05 Arus kas 13 minggu, info kurang lalu dilengkapi, uji pertama | ±1.0.2 | 7,5 | 8,5 | Tabel 13 minggu benar di kedua sisi, tetapi dengan skill ada status per minggu terhadap batas aman, defisit struktural dihitung (-Rp751 jt), opsi tindakan disimulasikan dengan angka (termasuk bukti "geser termin supplier hanya menunda") dan file CSV, sedangkan narasi salah menaruh cicilan Rp62 jt di minggu 12 (seharusnya minggu 11) dan BPJS/PPh 21 tak disebut sebagai asumsi. |
| 05, uji ulang (hanya sisi SESUDAH) | 1.0.3 | 7,5 (dari uji pertama) | 9 | Kedua cacat hilang: minggu kritis dikutip dari rincian script ("minggu 3 ... Gaji Rp 420.000.000 dan bahan baku Rp 130.000.000 ... total keluar Rp 550.000.000") dan "Belum termasuk pajak/BPJS" ditulis di Asumsi. |
| **Rata-rata skenario ini** (skenario tunggal) | | **7,5** | **8,5** (uji pertama) → **9** (1.0.3) | Selisih +1 pada uji pertama, +1,5 pada uji ulang. |

Rata-rata seluruh solusi kantor-manajemen (5 skenario, skill berbeda) di uji pertama: 7,0 → 8,3; setelah uji ulang ke-3 sisi SESUDAH 8,9. Itu skor solusi, bukan skor skill ini.

## Verdik
**LULUS uji ulang ke-3 (skor 9, 1.0.3).** Semua angka (13 saldo mingguan, total masuk Rp2.610 jt, keluar Rp3.361 jt, kebutuhan dana Rp451 jt / Rp551 jt dari batas aman, simulasi opsi) cocok dengan hitungan independen dan `proyeksi_kas.py`.

## Catatan jujur
- Model tanpa skill sudah kuat: tabel 13 minggu benar tanpa script dan menyimpulkan "kas jebol sebelum gaji 25 Okt". Pembeda ada di simulasi opsi berangka, file Excel/CSV, dan status per minggu, bukan di tabel dasarnya.
- Skor 9 adalah skor sisi SESUDAH setelah skill diperbaiki dari temuan uji pertama; sisi SEBELUM tidak dijalankan ulang.
- Pada uji ulang, argumen tool call tidak dibaca; `find /` atau instalasi paket hanya bisa dideteksi dari teks balasan (tidak terlihat). Sisa kecil: opsi 4 tidak menyebut saldo terendah selama periode (-Rp191 jt minggu 12) yang dicetak script; tetap benar.
- Satu skenario saja; skenario tanpa piutang besar, THR, atau pajak/BPJS belum diuji di OpenClaw.

## Cuplikan dari sumber (uji pertama)
- Tanpa skill: "Nego termin bayar supplier: geser dari mingguan ke 2-mingguan ..." (tanpa hitungan).
- Dengan skill: "Naikkan pemasukan ±Rp 60 juta/minggu → saldo terendah naik dari -Rp 451.000.000 menjadi +Rp 123.000.000 ... Negosiasi termin ... INI HANYA MENUNDA ... saldo tetap minus Rp 371.000.000."
