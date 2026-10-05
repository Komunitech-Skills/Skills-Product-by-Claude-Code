# 06 — Input tidak lengkap (server asli)

**Diuji terhadap Open Notebook 1.14.0 asli.**

```
$ python3 scripts/notebook.py tambah-sumber --notebook "Brosur & SOP Klinik" --tipe teks --ya
GALAT: Tipe 'teks' butuh --teks (atau --file - untuk baca dari input).
```
(exit code 2) ✅ Validasi input dilakukan **di skill sendiri sebelum memanggil server** (tidak butuh server untuk mendeteksi ini) — pesan jelas, agent akan menanyakan isi teks yang ingin ditambahkan, bukan menebak. Perilaku ini identik dengan hasil uji server tiruan sebelumnya (`examples/02-...`), konsisten.
