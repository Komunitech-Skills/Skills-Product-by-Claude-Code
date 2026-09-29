# 04 — Input tidak lengkap / tidak masuk akal

> Contoh dari pembuat skill (data fiktif). Belum uji independen.

## a. MoCA tanpa lama pendidikan
**Input:** "Saya dokter. Skor MoCA pasien 24, normal nggak?"

Script menolak (kode keluar 1):
```
$ python3 scripts/klinis.py kognitif --instrumen moca --skor 24
Input tidak valid: MoCA butuh lama pendidikan (tahun) untuk koreksi +1 poin
```
**Jawaban agent:**
```
Untuk menafsirkan MoCA saya perlu satu data lagi:
1. Lama pendidikan formal pasien (tahun)? (MoCA menambah 1 poin bila ≤ 12 tahun.)
```
(Setelah dijawab "9 tahun": skor akhir 25 < 26 → di bawah batas skrining, pertimbangkan evaluasi
lanjut; sumber Nasreddine 2005 / Husein dkk. 2010; penafian.)

## b. Skrining preeklampsia hanya dengan sistolik
**Input:** "Bidan. G2P1, TD sistolik 120, sebelumnya hamil normal. Skrining ya."
```
$ python3 scripts/klinis.py preeklampsia --faktor nullipara --sistolik 120
Input tidak valid: isi sistolik DAN diastolik untuk menghitung MAP
```
**Jawaban agent (satu pesan, bernomor):**
```
Agar skrining lengkap, mohon dilengkapi sekaligus:
1. Tekanan diastolik (mmHg)?
2. Usia ibu dan IMT sebelum hamil?
3. Jarak dari kehamilan sebelumnya (> 10 tahun?) dan apakah dengan pasangan yang sama?
4. Ada riwayat hipertensi kronik, diabetes, penyakit ginjal, autoimun/APS, atau kehamilan kembar?
5. Riwayat preeklampsia pada ibu/saudara perempuan pasien?
```
(Catatan: G2P1 berarti **bukan** nullipara — agent tidak memakai kode `nullipara`.)

## c. Satuan salah
```
$ python3 scripts/klinis.py imt --tinggi 5.2 --berat 130
Input tidak valid: tinggi 5.2: di luar rentang wajar 50-250 cm (cek satuan: cm atau m)
```
**Jawaban agent:** "Tinggi 5,2 sepertinya dalam kaki (feet) dan berat 130 mungkin pon. Mohon
kirim tinggi dalam cm dan berat dalam kg agar saya tidak menebak konversinya."
