# Contoh 5 (Uji Independen — Akun B) — Kursus Bahasa Inggris Anak Online

**Input pengguna:**
> "Saya mau buka kursus bahasa Inggris online buat anak SD, 2x seminggu, harga rencana Rp300.000/bulan. Saya ada grup WA orang tua murid les privat saya sebelumnya (~50 orang), belum pernah nawarin kursus online sebelumnya."

## 1. Hipotesis
> "Kami percaya **orang tua murid les privat sebelumnya yang anaknya usia SD** mau membayar **Rp300.000/bulan** untuk **kursus bahasa Inggris anak online 2x seminggu** karena bisa **belajar terjadwal tanpa harus antar-jemput ke tempat les**. Kami akan tahu ini benar jika minimal 15% dari yang ditawari benar-benar daftar dalam 7 hari."

## 2. Metode uji terpilih
Pre-order via broadcast WA ke grup orang tua murid (50 kontak, di atas ambang 30).

## 3. Kriteria lulus/gagal
- Minimal ditawari: 20 (dikirim ke 50 kontak sekaligus, di atas minimal).
- Harga Rp300rb/bulan termasuk kategori harga tinggi/pertimbangan lama (mendekati ambang ">Rp300rb" di SKILL.md) — SKILL.md menyebutkan ambang **boleh** diturunkan ke 10%/5% untuk kasus ini. Akun B menandai ini sebagai opsi yang **seharusnya ditawarkan** oleh agent ke pengguna sebelum uji, bukan otomatis diterapkan diam-diam (sesuai instruksi "jelaskan penyesuaian ini ke pengguna, jangan diam-diam ubah tanpa bilang"). Untuk skenario ini diasumsikan pengguna memilih tetap pakai ambang default (15%/8%) karena ingin standar yang sama dengan produk lain miliknya.

## 4. Hasil setelah 7 hari
50 ditawari, 3 daftar.

```
$ python3 scripts/hitung_validasi.py --ditawari 50 --preorder 3 --harga 300000
=== HASIL VALIDASI IDE ===
Ditawari       : 50 orang/tampilan
Pre-order/beli : 3
Konversi       : 6.0%
Klasifikasi    : GAGAL
Saran          : Data belum mendukung ide ini dalam bentuk sekarang — pertimbangkan HENTIKAN atau pivot besar. ...
```
Verifikasi independen: 3/50 = 0,06 → 6,0% ✅, di bawah ambang bersyarat 8% → GAGAL, konsisten.

## 5. Keputusan
**HENTIKAN (dalam bentuk sekarang) — dengan catatan penting yang wajib disampaikan agent:** SKILL.md Batasan menyebut ambang adalah heuristik, bukan hukum pasti, dan untuk produk harga tinggi boleh diturunkan ke 10%/5%. Kalau ambang itu dipakai (bukan default), 6,0% **masih di bawah 10%** tapi **di atas 5%** → hasilnya jadi LULUS BERSYARAT, bukan GAGAL. Ini penting: agent wajib menjelaskan kedua kemungkinan ke pengguna dan bertanya ambang mana yang ingin dipakai **sebelum** memvonis GAGAL, bukan cuma melaporkan hasil default begitu saja — sesuai instruksi "jelaskan ke pengguna, jangan diam-diam ubah". Rekomendasi ke pengguna: sampaikan hasil default (GAGAL) + opsi ambang harga-tinggi (LULUS BERSYARAT) berdampingan, minta pengguna pilih dasar penyesuaian yang jujur, jangan otomatis pilih salah satu demi hasil yang "enak didengar".

## Catatan penguji
- Ini bukan bug skrip (perhitungan konversi benar), tapi celah **ambiguitas keputusan** di alur SKILL.md: ambang mana yang final untuk produk harga tinggi tidak dikunci di awal Langkah 3 kalau pengguna tidak diberi pilihan eksplisit lebih dulu — berisiko agent yang kurang hati-hati diam-diam memilih ambang yang menguntungkan narasi. SKILL.md sudah cukup jelas melarang ini secara tekstual ("jangan diam-diam ubah tanpa bilang"), jadi ini catatan kejelasan proses, bukan pelanggaran skill.
