# Contoh 3: Hasil di bawah target -> UBAH -> pivot

> Contoh ilustrasi fiktif. Angka keluaran script asli.

**Situasi:** varian mentai ditawari ke 60 orang di komunitas kantor. Target lanjut 10%, stop 5%. Hasil 5 pre-order.
```
$ python3 scripts/hasil_eksperimen.py hasil --ditawari 60 --aksi 5 --target 10
Konversi: 5 dari 60 orang = 8,3%
Rentang wajar 95% (Wilson): 3,6% sampai 18,1%
Artinya: kalau uji diulang, hasil sebenarnya kemungkinan besar ada di antara 4% dan 18%.
Kriteria (ditetapkan SEBELUM uji): lanjut jika >= 10,0%, stop jika < 5,0%.
KEPUTUSAN: UBAH: di bawah target tapi belum sampai batas stop. Ubah SATU hal (harga, tawaran, kemasan, atau kelompok pembeli) lalu uji ulang. Lihat pilihan pivot di SKILL.md.
```
**Alasan penolakan (4 orang ditanya):** "kemahalan untuk 10 pcs", "takut tidak habis", "freezer penuh", "belum kenal rasanya".
**Diagnosis:** penghalang ada di penawaran (ukuran/harga/risiko), bukan minat pada mentai. **Pivot penawaran:** paket coba 5 pcs Rp25.000, satu perubahan saja. Putaran 2 diuji ke 60 orang baru dengan target sama. Bila tetap < 5%, STOP atau pivot pembeli (kafe/kantin).
