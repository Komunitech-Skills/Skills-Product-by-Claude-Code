# Template: Rekap Operasional Klinik (Non-Klinis)

Dipakai untuk merapikan hasil `scripts/rekap_kunjungan.py`, atau untuk rekap manual bila data
tidak dalam bentuk CSV. **Tidak pernah** memuat nama, NIK, atau diagnosis pasien. Semua angka
di bawah **wajib berasal dari script** (atau tally manual eksplisit) — jangan ditaksir.

```
📊 Rekap Operasional — [Nama Klinik]
Periode: [tanggal mulai] – [tanggal selesai]

Total pendaftaran tercatat: [angka]
Hadir: [angka] ([persen]%)
Tidak datang: [angka] ([persen]%)
[bila ada] Status tidak dikenal (cek manual, belum dihitung hadir/tidak datang): [angka] ([persen]%)

Per hari:
- [tanggal]: [jumlah]
- ...

Per poli/layanan (pendaftaran):
- [nama poli]: [jumlah]
- ...

Per penjamin (pendaftaran):
- BPJS: [jumlah]
- Umum: [jumlah]
- Asuransi lain: [jumlah]

Jam paling ramai: [jam 1], [jam 2], [jam 3]

[bila script memberi peringatan format tanggal, atau baris "(nilai lain disembunyikan demi
privasi)" pada status/poli/penjamin, salin peringatannya apa adanya — JANGAN coba menampilkan
nilai yang disembunyikan itu, cukup sebut jumlahnya]

Catatan: rekap ini bersifat agregat (jumlah), tidak memuat nama/diagnosis pasien. Persentase
dibulatkan 1 desimal (round half up).
```

Cara menghasilkan angka di atas dari file CSV ekspor klinik:
```
python3 <folder-skill-ini>/scripts/rekap_kunjungan.py --file kunjungan.csv
```
(Windows: ganti `python3` dengan `python` atau `py`.)

**Sebelum menyalin hasil ke template:**
1. Baca bagian "Rincian nilai status" dari output script — pastikan setiap status yang tertulis
   "tidak dikenal" sudah dicek manual (tanyakan ke klinik itu status apa), jangan dihitung
   sebagai hadir begitu saja.
2. Kalau script memberi peringatan format tanggal campur, tangani dulu sebelum mengirim rekap —
   jangan diabaikan.
3. Script sudah otomatis menyembunyikan nilai status/poli/penjamin yang berpotensi berisi nama,
   nomor kontak, atau diagnosis (nilai panjang, mengandung angka, atau pola sapaan+nama) — hanya
   menyisakan jumlah baris & jumlah nilai berbeda yang disembunyikan. **Jangan pernah** membuka
   file CSV asli untuk "melengkapi" nilai yang disembunyikan itu ke dalam rekap.

Jika Python tidak bisa dijalankan, hitung manual: kelompokkan baris data per hari/poli/penjamin
dan status kehadiran dengan cara menghitung (tally) langsung di spreadsheet
(mis. PivotTable/`COUNTIF`), tentukan SATU format tanggal untuk seluruh data sebelum
mengelompokkan per hari, lalu isi angka ke template di atas. Jangan menampilkan kolom
nama/NIK/diagnosis di hasil akhir mana pun.
