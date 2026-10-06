# Keluaran saring_prospek.py pada data uji (dijalankan penguji independen, 2026-10-06)

## prospek.csv
```
$ python3 scripts/saring_prospek.py data/prospek.csv --icp "kafe,katering,kue,takeaway,ramah lingkungan" --kota Bandung
nama,kota,jenis,website,kontak,sumber,tanggal,catatan,skor,periksa
Kopi Senja Contoh,Bandung,kafe,https://kopisenja.example,(022) 555-0101,https://kopisenja.example/kontak,,kafe takeaway banyak cup,67,
"Roti, Kue & Kopi Contoh",Bandung,bakery,https://rkk.example,"sales@rkk.example, (022) 555-0202",https://rkk.example/hubungi,,"packaging, takeaway",67,
Katering Ibu Ani Contoh,Cimahi,katering,,0812-3456-7890,https://maps.example/ani,,katering harian box,31,"nomor HP: pastikan nomor bisnis yang dipublikasikan situs resmi, bukan pribadi"
Dapur Sehat Contoh,Bandung,katering,https://dapursehat.example,dapursehat@gmail.com,-,,katering sehat ramah lingkungan,30,TANPA SUMBER: [belum terverifikasi]; email gratisan: cek apakah email bisnis resmi
Toko Kue Manis Contoh,Bandung,toko kue,https://kuemanis.example,info@kuemanis.example,,,kemasan kue,30,TANPA SUMBER: [belum terverifikasi]
Warung Tanpa Bukti,Bandung,kafe,,,[belum terverifikasi],,,26,TANPA SUMBER: [belum terverifikasi]

RINGKASAN: 7 baris masuk, 6 unik, 1 duplikat dibuang, 3 tanpa sumber, 2 perlu dicek kontaknya
DUPLIKAT: 'Kopi Senja Contoh Dago' sama dengan 'Kopi Senja Contoh'
```

Verifikasi independen skor (rumus dihitung ulang tangan): Kopi Senja 2/5 kata x55=22 +15 kota +10 web +10 kontak +10 sumber = 67 (cocok); Katering Ibu Ani 1/5x55=11 +0 (Cimahi) +0 web +10 +10 = 31 (cocok); baris tanpa sumber dibatasi 30 (cocok).

## maps.csv
```
$ python3 scripts/saring_prospek.py data/maps.csv --icp kafe
nama,kota,jenis,website,kontak,sumber,tanggal,catatan,skor,periksa
Kafe Satu Contoh,Bandung,kafe,https://maps.app.goo.gl/AAAA1,,,,,30,TANPA SUMBER: [belum terverifikasi]
Bakery Empat Contoh,Bandung,bakery,https://www.instagram.com/empat.example,,,,,18,TANPA SUMBER: [belum terverifikasi]
Katering Tiga Contoh,Bandung,katering,https://www.google.com/maps/place/Katering+Tiga,,,,,18,TANPA SUMBER: [belum terverifikasi]

RINGKASAN: 5 baris masuk, 3 unik, 2 duplikat dibuang, 3 tanpa sumber, 0 perlu dicek kontaknya
DUPLIKAT: 'Toko Kue Dua Contoh' sama dengan 'Kafe Satu Contoh'
DUPLIKAT: 'Kafe Lima Contoh' sama dengan 'Bakery Empat Contoh'
```

## templ.csv
```
$ python3 scripts/saring_prospek.py data/templ.csv --icp kafe
nama,kota,jenis,website,kontak,sumber,tanggal,catatan,skor,periksa
Kafe Dua Contoh,Bandung,kafe,,,,,,30,TANPA SUMBER: [belum terverifikasi]
Kafe Satu Contoh,Bandung,kafe,,,,,,30,TANPA SUMBER: [belum terverifikasi]

RINGKASAN: 2 baris masuk, 2 unik, 0 duplikat dibuang, 2 tanpa sumber, 0 perlu dicek kontaknya
```

## Berkas rusak
```
$ ... hanyaheader.csv
GAGAL: tidak ada baris prospek
kode keluar=2
$ ... kutip.csv
GAGAL: kolom nama usaha tidak ditemukan (judul kolom: nama/usaha/perusahaan)
kode keluar=2
$ ... acak.csv
GAGAL: new-line character seen in unquoted field - do you need to open the file with newline=''?
kode keluar=2
$ ... pendek.csv
GAGAL: kolom nama usaha tidak ditemukan (judul kolom: nama/usaha/perusahaan)
kode keluar=2
$ ... spasi.csv
GAGAL: berkas kosong
kode keluar=2
```

## titikkoma-tidak-rata.csv (CSV titik koma ala Excel Indonesia, satu baris kurang satu sel)
```
$ python3 scripts/saring_prospek.py data/titikkoma-tidak-rata.csv
GAGAL: kolom nama usaha tidak ditemukan (judul kolom: nama/usaha/perusahaan)
kode keluar=2
```
Berkas yang sama tanpa baris tidak rata terbaca normal. Penyebab: deteksi pemisah gagal pada baris tidak rata lalu jatuh ke koma.

## Temuan
1. **Duplikat palsu lewat domain bersama (cacat sedang):** di `maps.csv`, tautan Google Maps pendek (`maps.app.goo.gl`) dan Instagram dianggap "situs sama" sehingga usaha berbeda dibuang sebagai duplikat (5 baris jadi 3; "Toko Kue Dua" dianggap sama dengan "Kafe Satu"). Perlu daftar domain platform yang dikecualikan dari pencocokan domain (maps.app.goo.gl, goo.gl, google.com, instagram.com, facebook.com, tokopedia.com, shopee.co.id, linktr.ee, wa.me, dll.).
2. **Kolom tautan dari template sendiri tidak dikenali (cacat sedang):** `templates/rencana-pencarian.md` meminta kolom "Tautan halaman (Maps/situs)", tetapi judul ini tidak ada di ALIAS, sehingga tautannya hilang dan semua baris ditandai TANPA SUMBER.
3. **CSV titik koma dengan baris tidak rata ditolak seluruhnya** (lihat di atas).
4. Pesan galat berkas biner acak masih teknis berbahasa Inggris ("new-line character seen in unquoted field...").
5. Yang benar: dedup nama mirip & domain situs sendiri, batas skor 30 untuk baris tanpa sumber, tanda nomor HP & email gratisan, `--maks`/`--keluar`, berkas kosong/tanpa kolom nama/tidak ada → kode 2. Skor dihitung ulang manual: cocok. `tests/uji_regresi.py`: 8 tes OK.

---

# Uji ulang 1.0.1 (2026-10-06, penguji independen baru)

`python3 tests/uji_regresi.py` → **13 tes OK**.

## maps.csv (`--icp kafe,katering,kue --kota Bandung`)
```
Kafe Lima Contoh ... instagram.com/lima.example ... 43
Kafe Satu Contoh ... maps.app.goo.gl/AAAA1 ... 43
Katering Tiga Contoh ... google.com/maps/place/Katering+Tiga ... 43
Toko Kue Dua Contoh ... maps.app.goo.gl/BBBB2 ... 43
Bakery Empat Contoh ... instagram.com/empat.example ... 25
RINGKASAN: 5 baris masuk, 5 unik, 0 duplikat dibuang, 0 tanpa sumber
```
**Diperbaiki:** domain platform bersama tidak lagi dipakai sebagai kunci duplikat (1.0.0: 5 → 3 baris). Kolom `URL` dipakai sebagai sumber. Skor dihitung ulang tangan: Kafe Lima 1/3×55=18,3 + kota 15 + web platform 0 + kontak 0 + sumber 10 = 43 ✓; Bakery 0+15+0+0+10 = 25 ✓.

## templ.csv (judul "Tautan halaman (Maps/situs)")
Tautan terbaca sebagai `sumber`, 0 tanpa sumber, skor 43 ✓. **Diperbaiki** (1.0.0: semua TANPA SUMBER).

## titikkoma-tidak-rata.csv
`PERINGATAN: baris 3 hanya punya 2 kolom dari 3; kolom yang kurang dianggap kosong` → Toko A skor 25, Toko B 15 + `TANPA SUMBER`. **Diperbaiki** (1.0.0: seluruh berkas ditolak).

## Penanda DUMMY? (data buatan penguji, 9 baris)
- Benar ditandai: ManA (+62 812 3456 7890, "No. 123"), Moro (info@domain.com), 0811 1111 111 → skor 0, `DUMMY? [contoh/dummy, bukan kontak nyata]`. prospek.csv: "Katering Ibu Ani Contoh 0812-3456-7890" kini DUMMY?.
- Benar tidak ditandai: (022) 4230352 "No. 22"; HP 0812-1396-0941 diberi peringatan "nomor HP: pastikan nomor bisnis".
- Dedup domain sendiri benar: "Toko Kue Asli Cabang" (kafeasli.id/cabang) = "Kafe Asli".
- **Positif palsu (cacat ringan):** alamat nyata "Jl. Merdeka **No. 1**" dan "Jl. Riau **No. 12**" ditandai DUMMY? dengan alasan "alamat 'No. 123'" dan skornya jadi 0; nomor "(022) 2012345" (memuat deret 012345) juga ditandai. Regex `RE_NO_DUMMY` sebaiknya hanya "No. 123"/"No. 1234", dan deret dicek hanya di 6–8 digit terakhir yang seluruhnya deret.

## Berkas rusak
kosong / hanya judul / tanpa kolom nama / tidak ada → pesan Indonesia, kode 2 ✓. Biner acak masih "GAGAL: new-line character seen in unquoted field - do you need to open the file with newline=''?" (teknis, Inggris; ringan).
