# Format mutasi bank yang dikenali

Skill **tidak** bergantung pada satu tata letak tetap. Script mencari baris judul kolom di 40 baris pertama, lalu
mengenali kolom dari namanya. Contoh di `tests/fixtures/mutasi/` adalah **data fiktif** yang disusun mengikuti pola
umum ekspor CSV bank; tata letak asli bisa berubah sewaktu-waktu. Bila kolom tidak terbaca, script menyebut kolom
yang ada supaya pengguna/agent bisa memeriksa.

| Bank (pola umum) | Ciri | Yang dilakukan script |
|---|---|---|
| BCA (KlikBCA CSV) | Beberapa baris info di atas; judul `Tanggal Transaksi,Keterangan,Cabang,Jumlah,,Saldo`; tanggal `'01/09` **tanpa tahun**; angka gaya Inggris `"1,500,000.00"`; kolom tanpa judul berisi `CR`/`DB`; baris `PEND`; baris ringkasan `Saldo Awal`, `Mutasi Kredit`, `Mutasi Debet`, `Saldo Akhir` di bawah | Wajib `--tahun`; kolom CR/DB ditemukan otomatis; `PEND` dan ringkasan dilewati dengan alasan; pergantian tahun Des→Jan ditangani |
| BRI (IBBIZ/BRImo) | `TGL_TRAN,DESK_TRAN,MUTASI_DEBET,MUTASI_KREDIT,SALDO_AKHIR_MUTASI`; tanggal berjam | Jam dibuang; baris saldo awal bernilai 0 dilewati |
| Mandiri (Livin/MCM) | Sering pemisah titik koma; `Tanggal;Keterangan;Debit;Kredit;Saldo`; angka gaya Indonesia `1.500.000,00`; tanggal `01 Sep 2026` | Pemisah & gaya angka dideteksi otomatis; nama bulan Indonesia/Inggris dikenali |
| BNI | `Tanggal Transaksi,Uraian Transaksi,Tipe,Nominal,Saldo`, `Tipe` = `Db.`/`Cr.` | Kolom Tipe dipakai sebagai penanda masuk/keluar |
| Lainnya | Judul mirip (Tanggal/Date, Keterangan/Uraian/Description, Debet/Kredit, Jumlah+DB/CR, Saldo) | Deteksi otomatis |

## Aturan angka
- Gaya angka ditentukan **per file** dari semua angka (termasuk saldo): `1.500.000,00` = gaya Indonesia (`koma`),
  `1,500,000.00` = gaya Inggris (`titik`). File campur → berhenti dan minta `--desimal`.
- Bila semua angka bulat tanpa desimal: `1.500` dan `1,500` dibaca **seribu lima ratus** (Rupiah hampir tidak pernah
  memakai pecahan).
- Koma diikuti 1–2 angka (mis. `12,5`) dianggap **koma desimal gaya Indonesia**, jadi file dibaca gaya `koma` dan
  `12,5` = Rp 12,50. Setiap nominal di bawah Rp 100 masuk daftar "perlu dicek" supaya salah format ketahuan.
  Angka yang tidak cocok dengan gaya file (mis. `1.50.000`, atau `10,123` di file gaya koma) → baris dilewati
  "angka tidak jelas".
- `Rp`, `IDR`, spasi, `,-` di akhir, kurung `(25.000)` dan minus di depan/belakang dikenali.
- Lebih dari 2 angka desimal, atau di atas Rp 1 triliun per baris → dilewati dengan alasan.

## Aturan tanggal
- Urutan hari/bulan (kebiasaan Indonesia). Bila di file ada angka kedua > 12 (mis. `09/25/2026`) dan tidak ada angka
  pertama > 12, file dibaca bulan/hari dan diberi catatan. Campur keduanya → berhenti.
- Format dikenali: `01/09/2026`, `01-09-26`, `2026-09-01`, `01 Sep 2026`, `17 Agustus 2026`, `5-Okt-26`, dengan/atau
  tanpa jam.

## Penanda masuk/keluar
Urutan: kolom Debet+Kredit terpisah → kolom penanda (`CR/DB`, `D/K`, `Tipe`) → akhiran di angka (`1.000 CR`) → minus =
keluar. Semua angka positif tanpa penanda → berhenti (pengguna bisa menyatakan `--tanpa-tanda-masuk` bila memang
semua uang masuk).

## PDF / Excel
PDF tidak bisa dibaca (minta CSV dari internet banking). Excel (.xlsx/.xls) → minta pengguna "Simpan Sebagai CSV".
