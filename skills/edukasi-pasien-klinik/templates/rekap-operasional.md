# Template: Rekap Operasional Klinik (Non-Klinis)

Dipakai untuk merapikan hasil `scripts/rekap_kunjungan.py`, atau untuk rekap manual bila data
tidak dalam bentuk CSV. **Tidak pernah** memuat nama, NIK, atau diagnosis pasien.

```
📊 Rekap Operasional — [Nama Klinik]
Periode: [tanggal mulai] – [tanggal selesai]

Total kunjungan: [angka]

Per hari:
- [tanggal]: [jumlah]
- ...

Per poli/layanan:
- [nama poli]: [jumlah] ([persen]% dari total)
- ...

Per penjamin:
- BPJS: [jumlah]
- Umum: [jumlah]
- Asuransi lain: [jumlah]

Jam paling ramai: [jam 1], [jam 2], [jam 3]

Perkiraan pasien tidak datang/batal: [jumlah] ([persen]% dari total)

Catatan: rekap ini bersifat agregat (jumlah), tidak memuat nama/diagnosis pasien.
```

Cara menghasilkan angka di atas dari file CSV ekspor klinik:
```
python3 <folder-skill-ini>/scripts/rekap_kunjungan.py --file kunjungan.csv
```
(Windows: ganti `python3` dengan `python` atau `py`.)

Jika Python tidak bisa dijalankan, hitung manual: kelompokkan baris data per hari/poli/penjamin
dengan cara menghitung (tally) langsung di spreadsheet (mis. PivotTable / `COUNTIF`), lalu isi
angka ke template di atas. Jangan menampilkan kolom nama/NIK/diagnosis di hasil akhir mana pun.
