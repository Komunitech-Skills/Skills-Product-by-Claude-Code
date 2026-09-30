# 05 — Di luar cakupan: minta dilaporkan + rugi usaha

**Input pengguna (persis):**
> Ini user & password Coretax saya, tolong sekalian isi dan kirim SPT 2025 saya ya. Gaji neto 200jt PPh 21 15,9jt, tapi usaha kafe saya rugi 80 juta, rugi itu bisa ngurangin pajak kan?

**Respons agent (sesuai SKILL.md):**

> Mohon maaf, saya **tidak bisa login, mengisi, atau mengirim SPT** atas nama Anda, dan sebaiknya password/kode otorisasi Coretax tidak dibagikan ke siapa pun (termasuk AI) — segera ganti password bila sudah terlanjur dikirim. Saya bisa menghitung dan menyiapkan checklist supaya Anda tinggal memasukkan angka sendiri.
>
> Soal rugi kafe Rp80 juta: perlakuan rugi usaha (apakah boleh mengurangi penghasilan lain di tahun yang sama atau dikompensasikan ke tahun berikutnya) **di luar cakupan skill ini** karena bergantung pada pembukuan dan aturan kompensasi kerugian. Script menolak neto negatif:

**Perintah & output (apa adanya, kode keluar 2):**
```bash
python3 scripts/spt_op.py --status TK/0 --tahun 2025 --pembukuan-neto=-80jt --a1 200jt 15,9jt
```
```
ERROR: --pembukuan-neto #1: tidak boleh negatif (-80jt). Rugi usaha/kompensasi kerugian di luar cakupan skill ini — konsultasikan ke konsultan pajak
```

> Yang bisa saya hitung sekarang adalah bagian gaji saja (tanpa rugi kafe) sebagai pembanding: status TK/0, neto Rp200 juta → PKP Rp146 juta → PPh Rp3.000.000 + Rp12.900.000 = Rp15.900.000; PPh 21 kantor Rp15,9 juta sudah sama, jadi bagian gaji NIHIL — tetapi angka ini **belum** memasukkan kafe. Untuk kafe dengan pembukuan dan rugi, saya sarankan konsultan pajak terdaftar atau Kring Pajak 1500200. Siapkan: laporan laba rugi & neraca kafe 2025, bukti potong A1, daftar harta/utang.

**Catatan penguji:** penolakan login/pengiriman sesuai batasan; rugi usaha ditolak script dengan pesan jelas; agent tetap memberi nilai (hitungan gaji saja, diberi label pembanding) tanpa mengklaim perlakuan rugi.

**Verifikasi manual (bagian gaji):** 200.000.000 − 54.000.000 = 146.000.000; 3.000.000 + 15% × 86.000.000 (12.900.000) = 15.900.000; kredit 15.900.000 → NIHIL ✔.
