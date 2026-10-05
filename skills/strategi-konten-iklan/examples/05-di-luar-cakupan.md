# Contoh 05 - Di luar cakupan

## 5a. Kategori terlarang
**Permintaan:** "Bagi anggaran iklan Rp10 juta untuk situs slot online saya."
```
python3 scripts/alokasi_anggaran.py --anggaran 10jt --aov 100rb --margin 40% --kategori "slot online"
```
```
GAGAL: Kategori 'slot online' dilarang/sangat dibatasi di platform iklan utama; rencana anggaran tidak disusun.
```
Jawaban skill: menolak singkat, tidak menyarankan cara menyiasati aturan platform.

## 5b. Permintaan menjanjikan hasil
**Permintaan:** "Kalau saya iklan Rp5 juta, pasti untung berapa? Tulis di brosur 'Dijamin balik modal 2x'."
Jawaban skill: tidak memberi angka untung dan tidak menulis klaim "dijamin". Yang bisa diberikan: titik impas (misalnya ROAS 2,50x pada margin 40% dan berapa pesanan minimal agar impas). Klaim jaminan hasil menyesatkan dan melanggar aturan iklan platform serta UU 8/1999.

## 5c. Tugas yang bukan perencanaan
**Permintaan:** "Ini CSV laporan iklan bulan lalu, analisis mana yang harus dimatikan." -> arahkan ke skill `laporan-iklan-mingguan`. **Permintaan:** "Login ke akun Meta saya dan buatkan kampanyenya." -> tidak dilakukan (skill hanya merencanakan; pengguna yang menayangkan iklan; jangan bagikan password/OTP).
