# Uji OpenClaw SEBELUM vs SESUDAH: arus-kas-13minggu

## Uji ulang 1.0.5 (2026-10-16, penguji independen)

**Cara uji:** OpenClaw 2026.10.2 lokal (`openclaw agent --local`, satu giliran per panggilan), model router Komunitech (`ninerouter/komunitech`), zona waktu Asia/Jakarta, minggu 1 = Senin 19 Okt 2026. Setiap sampel memakai home baru yang terisolasi. **SESUDAH** = home yang hanya berisi `arus-kas-13minggu` 1.0.5 (folder skill dari repo), **SEBELUM** = home tanpa skill. Yang dijalankan ulang hanya skenario yang terkena cacat 14 Okt:
- **05**, kedua sisi. Sisi SEBELUM dicoba 3 kali; percobaan 2–3 memakai batas waktu provider 600 detik.
- **02**, sisi SESUDAH, dengan CSV yang sengaja diberi `;` berlebih di akhir tiga baris.
- **01**, sisi SESUDAH, untuk mengecek narasi opsi piutang.

Skor lain dipakai ulang dari uji 14 Okt (1.0.4) dan ditandai ↺. Pesan member identik dengan uji 14 Okt dan datanya fiktif. Jejak alat (jumlah jalan script, path berkas, durasi) dibaca dari transkrip sqlite home uji. Angka diverifikasi penguji dengan Python sendiri (tidak mengimpor script skill).

<details><summary>CSV uji skenario 02 (rencana-kas-cv-mitra.csv, dengan <code>;;;</code> / <code>;;</code> berlebih)</summary>

```csv
tanggal;keterangan;masuk;keluar
tiap minggu;Penjualan proyek kecil (rata-rata);15.000.000;
tiap minggu;Belanja material;;8.750.000
tgl 25 tiap bulan;Gaji staf 7 orang;;32.500.000;;;
tgl 5 tiap bulan;Sewa kantor;;7.500.000
tgl 15 tiap bulan;Angsuran KUR;;6.250.000
tgl 10 tiap bulan;Setor PPh 21 + PPN;;4.800.000
09/11/2026;Termin 2 proyek RS Harapan Fiktif;48.000.000;;;;
20/11/2026;Bayar supplier panel listrik (tempo);;27.000.000
14/12/2026;Pelunasan PT Delta Fiktif;35.000.000;;
21/12/2026;Bonus akhir tahun staf;;20.000.000
08/01/2027;Perpanjangan izin & asuransi;;9.500.000
```
</details>

| Skenario | Skor tanpa skill | Skor dengan skill | Sumber | Alasan |
|---|:-:|:-:|---|---|
| 01 Usaha kue (lokal) | 6,5 ↺ | **8,5** | dengan: ulang 16 Okt | Tabel cocok 13/13. Opsi "percepat DP" kini dihitung sebagai opsi sendiri yang **hanya** menggeser DP minggu 5→3 (minggu 3 Rp10.300.000, terendah Rp4.700.000 minggu 11). Opsi gabungan menyebut **kedua** pelunasan (DP 5→3, sisa 13→11) → terendah Rp18.800.000, Rp4.500.000 bahan pindah ke setelah minggu 13 (setelah dibayar Rp22.600.000). Minus: "seminggu sebelum sisa pelunasan cair" (seharusnya 2 minggu), "sedikit di bawah batas" untuk Rp2,0 jt, urutan opsi, `/tmp/hasil.json`, 494 detik. |
| 01 konteks Telegram | 3 ↺ | 8,5 ↺ (1.0.4) | 14 Okt | Tidak diuji ulang. Tidak masuk rata-rata (sama dengan 14 Okt). |
| 02 CSV CV + batas aman 25 jt | 6,5 ↺ | **8,5** | dengan: ulang 16 Okt | Baris ber-`;;;`/`;;` ikut terhitung (gaji Rp32.500.000 minggu 1/6/10, termin Rp48.000.000 minggu 4, Delta Rp35.000.000 minggu 9). Tabel cocok 13/13. **Defisit struktural −Rp45.400.000** disebut tegas. Kelima opsi cocok, dan opsi termin ditulis jujur sebagai "bukan solusi tuntas" (setelah dibayar Rp18.850.000). 214 detik (14 Okt 628 detik). Minus: masih `find /` di detik ke-5, "termin 30→44 hari" dikarang. |
| 03 Bengkel ambil order? | 6,5 ↺ | 9 ↺ | 14 Okt | Tidak diuji ulang; rumus script tidak berubah di 1.0.5. |
| 04 Info kurang (laundry) | 7,5 ↺ | 8 ↺ | 14 Okt | Tidak diuji ulang. |
| 05 Tunda pajak/gaji atau pinjol? | **tidak ada jawaban** | **8** | ulang 16 Okt | SEBELUM: 3 percobaan gagal (idle timeout 260 detik; LLM timeout 414 dan 413 detik). SESUDAH: **236 detik, 2 jalan script** (14 Okt: ±10 jalan, timeout 800 detik). Tabel cocok 13/13. Agent tegas menolak menunda pajak/gaji dan pinjol. Penjelasannya tepat: tanpa DP kulkas operasional nyaris impas. Enam angka opsi cocok. Minus: syarat pinjaman (Rp7 jt, cicilan Rp700 rb × 3) dikarang tanpa label asumsi dan ditaruh di opsi 1–2 (SKILL.md: pilihan terakhir); 8 minggu di bawah batas pada opsi unggulan tidak disebut; sanksi tanpa dasar aturan + tahun; tidak ada opsi nego penjual kulkas. |
| **Rata-rata** | **6,75** (01–04) | **8,4** (01–05) · 8,5 (01–04) | | **Selisih +1,65** (konservatif: 8,4 − 6,75) · +1,75 (berpasangan 01–04) |

**Durasi dan jalan script (jejak alat):**

| Sampel | Durasi | Jalan `proyeksi_kas.py` | Panggilan alat | Catatan |
|---|--:|:-:|:-:|---|
| 05 SESUDAH | 236 detik | 2 | 8 | 14 Okt: ±10 jalan, habis waktu 800 detik |
| 02 SESUDAH | 214 detik | 2 | 12 | `find /` di detik ke-5 (sebelum SKILL.md terbaca); 14 Okt 628 detik |
| 01 SESUDAH | 494 detik | 2 | 11 | membaca seluruh script; keluaran jalan pertama dipotong `head -300`, jalan kedua ke `/tmp/hasil.json`; 14 Okt 92 detik |
| 05 SEBELUM | 260 / 414 / 413 detik | – | – | tidak ada jawaban di ketiga percobaan |

**Verifikasi angka independen (hitung ulang penguji):** saldo akhir per minggu cocok **13/13** di ketiga skenario.

| Mg | 01 Kue | 02 CV Mitra | 05 Sembako |
|--:|--:|--:|--:|
| 1 | Rp18.300.000 | Rp38.000.000 | Rp6.000.000 |
| 2 | Rp9.800.000 | Rp44.250.000 | Rp5.000.000 |
| 3 | **−Rp700.000** | Rp43.000.000 | −Rp5.000.000 |
| 4 | Rp1.700.000 | Rp86.200.000 | −Rp3.600.000 |
| 5 | Rp16.000.000 | Rp65.450.000 | −Rp1.600.000 |
| 6 | Rp11.500.000 | Rp39.200.000 | −Rp4.600.000 |
| 7 | Rp12.000.000 | Rp37.950.000 | −Rp5.600.000 |
| 8 | Rp14.400.000 | Rp39.400.000 | −Rp3.600.000 |
| 9 | Rp17.700.000 | Rp74.400.000 | −Rp2.200.000 |
| 10 | Rp13.200.000 | Rp28.150.000 | −Rp5.200.000 |
| 11 | Rp4.700.000 | Rp34.400.000 | **−Rp6.200.000** |
| 12 | Rp9.200.000 | **Rp18.850.000** | −Rp4.200.000 |
| 13 | Rp22.600.000 | Rp18.850.000 | −Rp2.800.000 |
| Batas aman | Rp10.107.692 (asumsi) | Rp25.000.000 (pengguna) | Rp6.907.692 (asumsi) |
| Negatif / di bawah batas | 3 / 2, 4, 11, 12 | – / 12, 13 | 3–13 / 1, 2 |
| Masuk − keluar | Rp139.000.000 − Rp131.400.000 = +Rp7.600.000 | Rp278.000.000 − Rp323.400.000 = **−Rp45.400.000** | Rp78.000.000 − Rp89.800.000 = −Rp11.800.000 |
| Tambahan dana (tidak minus / ≥ batas) | Rp700.000 / Rp10.807.692 | – / Rp6.150.000 | Rp6.200.000 / Rp13.107.692 |

Penempatan tanggal: 01 gaji tgl 28 → minggu 2, 6, 11; sewa tgl 1 → 2, 7, 11; oven tgl 12 → 4, 8, 13; listrik tgl 20 → 1, 5, 9 (20 Jan di luar horizon). 02 gaji tgl 25 → 1, 6, 10; sewa tgl 5 → 3, 7, 12; KUR tgl 15 → 4, 9, 13; pajak tgl 10 → 4, 8, 12; termin 9 Nov → 4; panel 20 Nov → 5; Delta 14 Des → 9; bonus 21 Des → 10; izin 8 Jan → 12. 05 gaji → 1, 6, 10; sewa → 2, 7, 11; pajak tgl 15 → 4, 9, 13; DP kulkas 2 Nov → 3.

| Opsi yang disebut agent | Angka agent | Hitung ulang | Hasil |
|---|---|---|:-:|
| 01 Tunda mixer minggu 3→7 | terendah Rp4.700.000 (mg 11); di bawah batas 2, 11, 12; akhir Rp22.600.000 | sama | cocok |
| 01 DP saja minggu 5→3 | mg 3 Rp10.300.000; terendah Rp4.700.000 (mg 11) | sama | cocok |
| 01 Gabungan (DP 5→3, sisa 13→11, bahan mundur 2 mg, mixer 3→7) | terendah Rp18.800.000; Rp4.500.000 setelah mg 13; setelah dibayar Rp22.600.000 | sama (bahan mg 1–12 digeser, sesuai deskripsi script) | cocok |
| 01 Jualan +10% | akhir Rp34.300.000; mg 3–4 di bawah batas | mg 3 Rp2.000.000, mg 4 Rp5.300.000; akhir Rp34.300.000 | cocok ("sedikit" kurang tepat) |
| 02 Jualan +10% | terendah Rp36.850.000; akhir Rp38.350.000 | sama | cocok |
| 02 Termin material mundur 2 mg + panel mg 5→7 | terendah Rp36.350.000; Rp17.500.000 tertunda; setelah dibayar Rp18.850.000 | sama | cocok |
| 02 Material −10% | terendah Rp29.350.000; akhir Rp30.225.000 | sama | cocok |
| 02 Jualan +10% + Delta mg 9→7 / Delta saja | Rp36.850.000 / tetap Rp18.850.000 | sama | cocok |
| 05 Pinjaman Rp7 jt mg 3 + cicilan Rp700 rb mg 4, 9, 13 | terendah −Rp600.000 (mg 11); akhir Rp2.100.000 | sama | cocok |
| 05 Jualan +10% | terendah −Rp3.200.000 (mg 3); akhir Rp5.000.000 | sama (mg 3, 4, 6, 7 masih minus; tidak disebut) | cocok |
| 05 Stok −Rp500 rb/minggu | terendah −Rp3.500.000 (mg 3); akhir Rp3.700.000 | sama | cocok |
| 05 Gabungan pinjaman + jualan +10% | tanpa minggu minus; terendah Rp3.800.000 (mg 3); akhir Rp9.900.000 | sama (8 minggu masih di bawah batas; tidak disebut) | cocok |
| 05 Geser DP kulkas mg 3→7 | tetap −Rp6.200.000 (mg 11) | sama | cocok |
| 05 Termin stok mundur 2 mg | terendah Rp1.800.000; Rp8.000.000 tertunda; setelah dibayar −Rp2.800.000 | sama | cocok |
| 05 Tanpa DP kulkas (narasi "nyaris impas") | — | bersih +Rp200.000 | cocok |

**Salah angka: tidak ada.** Satu ketidaktepatan narasi di S1 ("seminggu sebelum" seharusnya dua minggu) tidak dihitung salah angka, sesuai preseden 14 Okt, dan skornya dikurangi 0,5.

**Status 3 cacat uji 14 Okt:**

| Cacat 1.0.4 | Status 1.0.5 | Bukti |
|---|---|---|
| S5 habis waktu (±10 jalan script) | **Hilang** | 236 detik, 2 jalan (dasar + opsi). S1 dan S2 juga 2 jalan. Durasi S1 494 detik masih jauh di atas target < 3 menit. |
| Narasi "percepat piutang" hanya menyebut satu baris | **Hilang** | S1: DP saja dihitung sebagai `--opsi` sendiri (5→3); gabungan menyebut DP 5→3 **dan** sisa 13→11; `deskripsi` + catatan script memuat kedua baris. |
| Pemisah CSV (`;` berlebih → berkas ditolak) | **Hilang** | S2: baris `;;;`/`;;` ikut terhitung. Agent menyalin data ke CSV format skill sendiri, jadi deteksi script tidak teruji lewat agent. Uji terpisah penguji: CSV format skill dengan `;;;` di akhir baris terbaca penuh (pemisah "titik koma", tanpa baris dilewati, total cocok). |

**Verdik: LULUS.** Rata-rata DENGAN 8,4 ≥ 8 (01–05 lokal), selisih +1,65 (konservatif) / +1,75 (berpasangan 01–04) ≥ 1,5, dan tidak ada salah angka. Ketiga cacat 14 Okt hilang. Pra-cek konteks Telegram belum dijalankan dengan 1.0.5 dan tetap wajib sebelum gelombang Telegram.

**Pembeda (satu kalimat):** Tanpa skill, model tidak menghasilkan jawaban sama sekali untuk kasus toko sembako (3 percobaan habis waktu; di uji 14 Okt juga pernah menyimpulkan "kas aman" padahal minggu 3 minus), sedangkan dengan skill 1.0.5 jawaban selesai dalam 214–494 detik dengan tabel 13 minggu yang cocok 100% dengan hitungan independen, penolakan tegas menunda pajak/gaji, defisit struktural −Rp45,4 jt yang terdeteksi dari CSV berantakan, dan setiap opsi berangka (mis. pinjaman resmi + jualan +10% → tidak ada minggu minus, saldo akhir Rp9,9 jt).

**Catatan jujur (untuk pembuat skill, bukan diubah penguji):**
1. `find /` masih terjadi di S2 (detik ke-5, paralel dengan percobaan memuat skill yang gagal karena `skills_read` belum tersedia), jadi aturan "UNTUK AGENT SAJA" di badan SKILL.md belum terbaca saat itu. Berkas tetap ditemukan di folder kerja. Usul: taruh petunjuk "berkas pengguna ada di folder kerja" di tempat yang terbaca lebih awal (deskripsi), atau terima ini sebagai kebiasaan model (sisi tanpa skill 14 Okt juga melakukannya).
2. Berkas di `/tmp` masih terjadi di S1. Keluaran jalan pertama dipotong agent sendiri dengan `| head -300`, lalu agent menjalankan ulang ke `/tmp/hasil.json` + `/tmp/err.txt` dan memilah JSON dengan `python3 -c` dua kali. Usul: ringkasan teks pendek bawaan untuk menulis jawaban (atau `--ringkas` juga di jalan dasar), supaya agent tidak perlu memotong atau memilah JSON besar.
3. Durasi: S5 236 detik, S2 214 detik (sedikit di atas target < 3 menit), S1 494 detik (2,7× target; 14 Okt 92 detik). Di S1 agent membaca seluruh `proyeksi_kas.py` (±1.200 baris) dan ada jeda berpikir panjang setelah keluaran JSON besar. Jalan script: 2 per sampel (≤ 4). Tidak ada sampel yang habis waktu. Kecepatan router ikut berpengaruh dan tidak bisa dipisahkan dari 1 sampel.
4. S5: syarat pinjaman (Rp7.000.000 cair minggu 3, cicilan Rp700.000 × 3) dikarang tanpa label asumsi, padahal SKILL.md mewajibkan nilai yang tidak diberikan pengguna ditandai asumsi. Pinjaman ditaruh sebagai opsi 1–2, padahal SKILL.md menyebutnya pilihan terakhir. Opsi unggulan ditulis "tidak ada minggu negatif" tanpa menyebut bahwa 8 dari 13 minggu masih di bawah batas aman. Sanksi DJP dan masalah hukum ketenagakerjaan tidak diberi dasar aturan + tahun. Tidak ada opsi menego penjual kulkas (DP lebih kecil atau dicicil). Kalimat "pinjol … ilegal" menggeneralisasi semua pinjol.
5. S1: kalimat "seminggu sebelum sisa pelunasan PT Cahaya Fiktif cair" tidak tepat; seharusnya dua minggu (minggu 11 vs minggu 13). Ini dinilai ketidaktepatan narasi, bukan salah angka, sesuai preseden 14 Okt (kalimat urutan tanggal di sisi tanpa skill juga tidak dihitung salah angka), dan dikurangi 0,5. Selain itu, "sedikit di bawah batas" dipakai untuk Rp2.000.000 vs batas Rp10.107.692, dan opsi tidak diurutkan dari dampak terbesar (gabungan Rp18,8 jt di urutan 3).
6. S2: "minta termin 30→44 hari" dikarang karena termin saat ini tidak diberikan pengguna. Script tidak bisa membaca langsung CSV format bebas (`tanggal;keterangan;masuk;keluar`), jadi agent menyalinnya sendiri ke format skill. Hasilnya benar (5 tanggal → minggu 4/5/9/10/12 cocok), tetapi salinan itu tidak dicek script. Galat script untuk berkas seperti itu menyebut baris 3 (`tiap minggu;Belanja material;;8.750.000`) sebagai baris judul karena "tiap minggu" cocok dengan kolom `minggu`, dan ini membingungkan.
7. Pemisah CSV: di OpenClaw S2 agent menulis CSV format skill sendiri (tanpa `;` berlebih), jadi deteksi pemisah script tidak teruji lewat agent. Penguji memeriksanya terpisah: CSV format skill dengan `;;;`/`;;` di akhir baris terbaca penuh (pemisah "titik koma", tidak ada baris dilewati, total masuk Rp96.000.000 / keluar Rp67.000.000 cocok hitungan manual).
8. Sisi TANPA S5 tidak menghasilkan jawaban dalam 3 percobaan 16 Okt (model idle timeout 260 detik; "LLM request timed out / stream ended without finish_reason" 414 dan 413 detik; agent sempat memanggil `sessions_history`), ditambah 1 percobaan 14 Okt. Kemungkinan penyebabnya beban router atau jawaban panjang, jadi ini bukan bukti mutlak bahwa model dasar tidak mampu. S5 hanya masuk rata-rata DENGAN.
9. Skor TANPA 01–04 dan 01-Telegram, serta skor DENGAN 01-Telegram, 03 dan 04 dipakai ulang dari uji 14 Okt (versi 1.0.4). Setiap sisi hanya 1 sampel per skenario. Konteks Telegram belum diuji dengan 1.0.5; pra-cek `uji-tg.sh` tetap wajib sebelum skill ini masuk gelombang Telegram (perhatikan durasi S1 494 detik).

<details><summary>Jawaban SESUDAH utuh, skenario 05 (toko sembako, 236 detik)</summary>

> Sudah saya hitung pakai proyeksi arus kas 13 minggu (mulai Senin 19 Okt 2026). Jawaban langsung dulu soal pertanyaan Anda, baru detail angkanya.
>
> **Soal tunda pajak & telat gaji karyawan: saya sarankan JANGAN.**
> - Gaji adalah hak karyawan — telat bisa kena masalah hukum ketenagakerjaan dan merusak kepercayaan tim, apalagi cuma 2 orang.
> - PPh final yang telat disetor kena sanksi bunga/denda dari DJP.
> - Keduanya saya kunci sebagai pos kritis dan **tidak ikut** simulasi "tunda" di bawah.
>
> **Soal pinjol: juga jangan.** Bunga dan dendanya sering mencekik dan ilegal. Yang lebih aman: pinjaman modal resmi (KUR mikro/bank/koperasi) sebesar kebutuhan riil saja — saya hitungkan dampaknya di Opsi 2 & 1 di bawah. Kalau mau simulasi cicilan KUR lebih detail, bisa saya bantu lagi.
>
> ## Proyeksi Kas 13 Minggu (19 Okt 2026 – 17 Jan 2027)
> Saldo awal Rp 9.000.000 · Batas aman **asumsi** Rp 6.907.692 (rata-rata pengeluaran 1 minggu — belum Anda konfirmasi)
>
> | Mg | Periode | Masuk | Keluar | Saldo akhir | Status |
> |---|---|---:|---:|---:|---|
> | 1 | 19–25 Okt | Rp 6.000.000 | Rp 9.000.000 | Rp 6.000.000 | 🟡 Di bawah batas |
> | 2 | 26 Okt–1 Nov | Rp 6.000.000 | Rp 7.000.000 | Rp 5.000.000 | 🟡 Di bawah batas |
> | 3 | 2–8 Nov | Rp 6.000.000 | Rp 16.000.000 | **-Rp 5.000.000** | 🔴 NEGATIF |
> | 4 | 9–15 Nov | Rp 6.000.000 | Rp 4.600.000 | -Rp 3.600.000 | 🔴 NEGATIF |
> | 5 | 16–22 Nov | Rp 6.000.000 | Rp 4.000.000 | -Rp 1.600.000 | 🔴 NEGATIF |
> | 6 | 23–29 Nov | Rp 6.000.000 | Rp 9.000.000 | -Rp 4.600.000 | 🔴 NEGATIF |
> | 7 | 30 Nov–6 Des | Rp 6.000.000 | Rp 7.000.000 | -Rp 5.600.000 | 🔴 NEGATIF |
> | 8 | 7–13 Des | Rp 6.000.000 | Rp 4.000.000 | -Rp 3.600.000 | 🔴 NEGATIF |
> | 9 | 14–20 Des | Rp 6.000.000 | Rp 4.600.000 | -Rp 2.200.000 | 🔴 NEGATIF |
> | 10 | 21–27 Des | Rp 6.000.000 | Rp 9.000.000 | -Rp 5.200.000 | 🔴 NEGATIF |
> | 11 | 28 Des–3 Jan | Rp 6.000.000 | Rp 7.000.000 | **-Rp 6.200.000** | 🔴 NEGATIF |
> | 12 | 4–10 Jan | Rp 6.000.000 | Rp 4.000.000 | -Rp 4.200.000 | 🔴 NEGATIF |
> | 13 | 11–17 Jan | Rp 6.000.000 | Rp 4.600.000 | -Rp 2.800.000 | 🔴 NEGATIF |
>
> ### Kesimpulan
> - **Pemicunya**: minggu 3 (2–8 Nov) kas langsung minus karena DP kulkas showcase Rp 12.000.000 bertabrakan dengan belanja bahan baku Rp 4.000.000, sementara masuk cuma Rp 6.000.000.
> - **Titik terendah**: minggu 11 (28 Des–3 Jan), saldo -Rp 6.200.000 — akumulasi defisit yang tidak pernah tertutup lagi setelah minggu 3.
> - Minggu negatif: 3 sampai 13 (11 dari 13 minggu). Minggu di bawah batas aman: 1–2.
> - Tambahan dana agar tidak minus: **Rp 6.200.000**; agar di atas batas aman: Rp 13.107.692.
> - Arus kas 13 minggu: masuk Rp 78.000.000 vs keluar Rp 89.800.000 → turun Rp 11.800.000 (±Rp 907.692/minggu). Catatan jujur: hampir seluruh selisih ini berasal dari DP kulkas Rp 12.000.000 yang sekali bayar — tanpa itu, operasional mingguan Anda nyaris impas. Tapi karena kas sekarang cuma Rp 9 juta, satu pos besar ini cukup untuk menjebol bantalan kas sampai akhir proyeksi.
> - Tidak ada pelunasan piutang pelanggan yang saya masukkan (Anda tidak menyebutkan ada).
>
> ### Opsi tindakan (urut dari dampak terbesar)
> 1. **Gabungan: Pinjaman modal resmi + naikkan penjualan 10%** — Pemasukan baru: Pinjaman modal Rp 7.000.000 di minggu 3; Pengeluaran baru: Cicilan pinjaman Rp 700.000 di minggu 4, 9, 13 (3×, total Rp 2.100.000); Penjualan tunai naik Rp 6.000.000 → Rp 6.600.000 di minggu 1–13 (total pemasukan bertambah Rp 7.800.000). Hasil simulasi: **tidak ada minggu negatif sama sekali**, titik terendah minggu 3 jadi Rp 3.800.000, saldo akhir minggu 13 Rp 9.900.000. Cara: ajukan pinjaman modal resmi (KUR mikro/bank/koperasi, bukan pinjol) + dorong penjualan lewat promo kecil/bundling di produk fast-moving.
> 2. **Pinjaman modal resmi Rp 7.000.000** (KUR mikro/bank/koperasi) di minggu 3, cicilan Rp 700.000 jatuh tgl 15 (3×, total Rp 2.100.000). Hasil: titik terendah minggu 11 jadi -Rp 600.000 (nyaris aman, bukan nol), saldo akhir Rp 2.100.000. Ini jumlah pas sesuai kebutuhan, bukan pinjaman besar sembarangan.
> 3. **Naikkan penjualan tunai 10%** (Rp 6.000.000 → Rp 6.600.000/minggu, total tambahan Rp 7.800.000 selama 13 minggu) — tanpa utang. Hasil: titik terendah tetap -Rp 3.200.000 (minggu 3), tapi saldo akhir membaik jadi Rp 5.000.000. Cara: naikkan sedikit margin produk yang tidak terlalu sensitif harga, tambah penjualan item pelengkap (misal snack/rokok) di kasir.
> 4. **Kurangi belanja bahan baku Rp 500.000/minggu** (Rp 4.000.000 → Rp 3.500.000, total hemat Rp 6.500.000) — nego ke supplier atau kurangi stok yang lambat laku. Hasil: titik terendah -Rp 3.500.000 (minggu 3), saldo akhir Rp 3.700.000. Sendirian belum cukup, tapi bagus dikombinasikan dengan opsi 1–3.
>
> **Catatan — jangan dipakai sebagai solusi utama:**
> - Geser DP kulkas showcase ke minggu 7 **tidak memperbaiki apa-apa** — titik terendah tetap -Rp 6.200.000 (di minggu 11), karena masalahnya akumulasi mingguan, bukan cuma timing DP.
> - Negosiasi termin bahan baku mundur 2 minggu memang bikin saldo terlihat positif selama 13 minggu (terendah Rp 1.800.000), **tapi Rp 8.000.000 tagihan itu cuma pindah ke setelah minggu ke-13** — begitu dibayar, saldo riil tetap -Rp 2.800.000. Ini menunda, bukan menyelesaikan.
>
> ### File Excel
> proyeksi-kas-13-minggu.csv — sudah tersimpan di folder kerja, bisa dibuka di Excel/Google Sheets.
>
>
> **Asumsi**: batas aman = rata-rata pengeluaran 1 minggu (Rp 6.907.692, belum Anda konfirmasi — ganti kalau Anda punya angka batas aman sendiri). Tidak ada piutang/pelunasan pelanggan dimasukkan karena tidak disebutkan.
> Catatan: proyeksi berdasarkan perkiraan Anda; perbarui tiap minggu dengan angka aktual. Ini bukan nasihat keuangan profesional — untuk keputusan besar (pinjaman, restrukturisasi), sebaiknya tetap konsultasi ke akuntan/konsultan UMKM.
</details>

<details><summary>Jawaban SESUDAH utuh, skenario 02 (CSV CV Mitra dengan <code>;;;</code>, 214 detik)</summary>

> # Proyeksi Kas 13 Minggu — CV Mitra Elektrik Fiktif (19 Okt 2026 – 17 Jan 2027)
>
> Saldo awal **Rp 64.250.000** · Batas aman **Rp 25.000.000** (sesuai Anda)
>
> | Mg | Periode | Masuk | Keluar | Saldo akhir | Status |
> |---|---|---:|---:|---:|---|
> | 1 | 19–25 Okt | Rp 15.000.000 | Rp 41.250.000 | Rp 38.000.000 | 🟢 Aman |
> | 2 | 26 Okt–1 Nov | Rp 15.000.000 | Rp 8.750.000 | Rp 44.250.000 | 🟢 Aman |
> | 3 | 2–8 Nov | Rp 15.000.000 | Rp 16.250.000 | Rp 43.000.000 | 🟢 Aman |
> | 4 | 9–15 Nov | Rp 63.000.000 | Rp 19.800.000 | Rp 86.200.000 | 🟢 Aman |
> | 5 | 16–22 Nov | Rp 15.000.000 | Rp 35.750.000 | Rp 65.450.000 | 🟢 Aman |
> | 6 | 23–29 Nov | Rp 15.000.000 | Rp 41.250.000 | Rp 39.200.000 | 🟢 Aman |
> | 7 | 30 Nov–6 Des | Rp 15.000.000 | Rp 16.250.000 | Rp 37.950.000 | 🟢 Aman |
> | 8 | 7–13 Des | Rp 15.000.000 | Rp 13.550.000 | Rp 39.400.000 | 🟢 Aman |
> | 9 | 14–20 Des | Rp 50.000.000 | Rp 15.000.000 | Rp 74.400.000 | 🟢 Aman |
> | 10 | 21–27 Des | Rp 15.000.000 | Rp 61.250.000 | Rp 28.150.000 | 🟢 Aman (mepet) |
> | 11 | 28 Des–3 Jan | Rp 15.000.000 | Rp 8.750.000 | Rp 34.400.000 | 🟢 Aman |
> | **12** | **4–10 Jan** | Rp 15.000.000 | Rp 30.550.000 | **Rp 18.850.000** | 🟡 **Di bawah batas** |
> | 13 | 11–17 Jan | Rp 15.000.000 | Rp 15.000.000 | Rp 18.850.000 | 🟡 Di bawah batas |
>
> ### Kesimpulan
> - **Titik paling kritis: minggu 12 (4–10 Jan)**, saldo turun jadi **Rp 18.850.000** (di bawah batas aman Rp 25 juta) — bertabrakannya 4 pos sekaligus: Perpanjangan izin & asuransi Rp 9.500.000, Belanja material Rp 8.750.000, Sewa kantor Rp 7.500.000, Setor PPh 21+PPN Rp 4.800.000, sementara masuk hanya Rp 15.000.000. Minggu 13 masih di bawah batas dengan saldo sama (Rp 18.850.000).
> - Tidak ada minggu yang **negatif**, tapi minggu 12 & 13 di bawah batas aman. Minggu 10 (21–27 Des) juga mepet — saldo hanya Rp 28.150.000 karena gaji staf Rp 32.500.000 dan bonus akhir tahun Rp 20.000.000 jatuh di minggu yang sama.
> - Tambahan dana agar seluruh 13 minggu di atas batas aman: **Rp 6.150.000**.
> - **Arus kas 13 minggu: masuk Rp 278.000.000 vs keluar Rp 323.400.000 → turun Rp 45.400.000** (rata-rata −Rp 3.492.308/minggu). **Ini defisit struktural** — bukan cuma soal jadwal, biaya rutin lebih besar dari pemasukan rutin.
> - Angsuran KUR Rp 6.250.000 jatuh tempo 15 Jan 2027, masih dalam horizon 13 minggu (minggu 13).
>
> ### Opsi tindakan (urut dari dampak terbesar)
> 1. **Naikkan penjualan proyek kecil 10%** — dari Rp 15.000.000 jadi Rp 16.500.000/minggu di minggu 1–13 (pemasukan bertambah total Rp 19.500.000). Hasil simulasi: titik terendah minggu 12 jadi **Rp 36.850.000**, tidak ada minggu minus, tidak ada minggu di bawah batas aman, saldo akhir Rp 38.350.000. Ini opsi yang benar-benar menutup defisit struktural, bukan sekadar menggeser jadwal. Cara: naikkan harga/ambil 1–2 proyek kecil tambahan per minggu.
> 2. **Negosiasi termin bahan (Belanja material + supplier panel listrik) mundur 2 minggu** — Belanja material Rp 8.750.000/minggu digeser mundur 2 minggu (Rp 17.500.000 di antaranya jatuh setelah minggu 13), dan tagihan Bayar supplier panel listrik Rp 27.000.000 digeser dari minggu 5 ke minggu 7. Hasil simulasi: titik terendah minggu 12 jadi Rp 36.350.000, tidak ada minggu minus/di bawah batas selama 13 minggu. **Tapi** Rp 17.500.000 kewajiban tetap harus dibayar setelah minggu 13 — begitu dibayar, saldo riil kembali ke Rp 18.850.000 (di bawah batas). Jadi ini meringankan jangka pendek, bukan solusi tuntas. Cara: hubungi supplier, minta termin 30→44 hari untuk pembelian rutin.
> 3. **Kurangi belanja material 10%** — dari Rp 8.750.000 jadi Rp 7.875.000/minggu (hemat total Rp 11.375.000). Hasil simulasi: titik terendah minggu 12 jadi Rp 29.350.000, tidak ada minggu minus/di bawah batas, saldo akhir Rp 30.225.000. Cara: audit stok, kurangi pembelian berlebih atau cari supplier lebih murah.
> 4. **Gabungan: naikkan penjualan 10% + percepat pelunasan PT Delta Fiktif dari minggu 9 ke minggu 7** — menambah pemasukan Rp 19.500.000 (opsi 1) ditambah menggeser Rp 35.000.000 piutang Delta lebih awal. Hasil simulasi: titik terendah **tetap Rp 36.850.000** (sama dengan opsi 1 saja) — percepat Delta memperkuat saldo di minggu 7–11 tapi tidak menambah nilai di titik kritis minggu 12. Tidak perlu dikejar bila opsi 1 sudah dijalankan.
> 5. **Percepat pelunasan PT Delta Fiktif saja** (minggu 9 → minggu 7) — hasil simulasi: titik terendah **tidak berubah**, tetap Rp 18.850.000 di minggu 12, dan minggu 12–13 tetap di bawah batas aman. Ditagih lebih cepat memang membantu arus kas di pertengahan Desember, tapi **tidak cukup** untuk mengatasi minggu kritis sendirian — perlu digabung dengan opsi 1 atau 3.
>
> ### File Excel
> `proyeksi-kas-13-minggu.csv` — disimpan di folder kerja, tinggal buka di Excel/Google Sheets (termasuk baris simulasi 5 opsi di atas).
>
> **Asumsi:**
> - Batas aman Rp 25.000.000 sesuai yang Anda tentukan.
> - Penjualan proyek kecil diasumsikan rata Rp 15.000.000/minggu sepanjang 13 minggu (angka dari data Anda, bukan proyeksi musiman per minggu).
> - Belanja material belum ditandai kritis/tidak di data — diperlakukan sebagai pos yang bisa dinegosiasikan terminnya (bukan ditunda sepihak).
> - Gaji, sewa, angsuran KUR, dan setor PPh 21+PPN diperlakukan selalu kritis (tidak pernah disarankan ditunda), sesuai aturan.
>
> **Catatan:** ini bukan nasihat keuangan profesional. Untuk langkah besar (restrukturisasi utang, pengurangan biaya rutin signifikan) sebaiknya didiskusikan dengan akuntan/konsultan. Perbarui proyeksi ini tiap minggu dengan angka aktual agar tetap akurat.
</details>

---


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
