# Rumus Grist (Python) untuk kebutuhan umum UMKM

Grist menghitung kolom rumus dengan **Python sungguhan** (bukan bahasa rumus khusus seperti
Excel) — kolom lain diakses lewat `$NamaKolom`, fungsi bawaan Excel-style seperti `TODAY()`,
`IF()`, `ROUND()` tersedia tanpa `import`. Kalau rumus ditulis lebih dari satu baris, baris
**terakhir** adalah nilai yang dikembalikan (mirip menjalankan beberapa baris di konsol Python).

**Kejujuran soal pengujian:** rumus di bawah ditulis mengikuti daftar fungsi resmi Grist yang
dikonfirmasi langsung dari kode sumber `grist-core` (`sandbox/grist/functions/*.py`), **bukan** hasil menjalankan langsung di dokumen Grist
sungguhan (lingkungan pembuatan skill ini tidak bisa menjalankan Grist). Grist menampilkan
galat rumus secara langsung di kotak formula (kotak berubah merah + pesan error) — kalau ada
rumus di bawah yang tidak persis cocok dengan versi Grist Anda, perbaiki sedikit mengikuti
pesan galat itu, atau laporkan ke Komunitech agar diperbarui.

Cara pakai: klik kolom di Grist → panel kanan **Column** → **Formula** → tempel isi kode di
bawah (tanpa baris `def ...`, itu hanya nama rujukan) → Grist otomatis menyimpan & menghitung.

## 1. Rapikan nomor WhatsApp jadi format `62...` (`rumus_wa_rapi`)
Dipakai di: pola **Daftar Pelanggan**, kolom `TeleponRapi` (rumus), sumber `$Telepon` (teks bebas).
```python
angka = "".join(c for c in str($Telepon) if c.isdigit())
if angka.startswith("62"):
    hasil = angka
elif angka.startswith("0"):
    hasil = "62" + angka[1:]
elif angka:
    hasil = "62" + angka
else:
    hasil = ""
hasil
```
Menerima `0812...`, `+62812...`, `62812...`, atau dengan spasi/strip — hasilnya selalu
`62812...` (tanpa `+`), siap dipakai di tautan `wa.me/62812...`.

## 2. Total baris pesanan setelah diskon (`rumus_total_baris`)
Dipakai di: pola **Pesanan**, kolom `Total`, sumber `$Jumlah`, `$HargaSatuan`, `$Diskon` (%).
```python
kotor = $Jumlah * $HargaSatuan
bersih = kotor * (1 - ($Diskon or 0) / 100)
round(bersih)
```
**Catatan pembulatan:** `round()` bawaan Python membulatkan ke **genap terdekat** pada angka
persis `,5` (mis. `round(2.5)` = `2`, `round(3.5)` = `4`) — berbeda dari standar Komunitech
"bulat ke atas pada ,5" yang dipakai di skill pajak/gaji (`hitung-ppn`, dll.). Untuk total
pesanan biasa selisihnya paling Rp 1 dan tidak material; **untuk perhitungan pajak/PPN resmi,
jangan pakai tabel Grist** — pakai skill `hitung-ppn` atau `dolibarr-usaha` yang pembulatannya
eksplisit dan sudah diuji.

## 3. Sisa stok (`rumus_sisa_stok`)
Dipakai di: pola **Stok Sederhana**, kolom `StokSaatIni`, sumber `$StokMasuk`, `$StokKeluar`.
```python
($StokMasuk or 0) - ($StokKeluar or 0)
```

## 4. Status stok: HABIS/MENIPIS/AMAN (`rumus_status_stok`)
Dipakai di: pola **Stok Sederhana**, kolom `Status`, sumber `$StokSaatIni`, `$BatasMinimum`.
```python
sisa = $StokSaatIni
batas = $BatasMinimum or 0
if sisa <= 0:
    hasil = "HABIS"
elif batas > 0 and sisa < batas:
    hasil = "MENIPIS"
else:
    hasil = "AMAN"
hasil
```
Aturan sama dengan skill `dolibarr-usaha`/`buku-stok`: MENIPIS hanya berlaku bila
`BatasMinimum` diisi (> 0) dan stok **kurang dari** batas itu.

## 5. Hitung mundur hari ke tanggal tayang (`rumus_hari_menuju`)
Dipakai di: pola **Jadwal Konten**, kolom `HariMenuju`, sumber `$Tanggal`, fungsi bawaan
`TODAY()`.
```python
selisih = $Tanggal - TODAY()
selisih.days
```
Hasil negatif berarti tanggal sudah lewat (belum tayang tepat waktu) — bisa dipakai untuk
menyorot baris yang terlambat di tampilan Grist (Conditional Formatting: kondisi
`$HariMenuju < 0`).

## Fungsi bawaan Grist lain yang berguna (sudah dikonfirmasi ada di kode sumber)
Tanggal: `TODAY()`, `NOW()`, `DATEADD(tanggal, days=..., months=...)`, `DATEDIF(mulai, akhir, "D")`.
Teks: `UPPER()`, `LOWER()`, `TRIM()`, `LEFT()`, `RIGHT()`, `SUBSTITUTE()`, `REGEXREPLACE()`.
Logika: `IF(kondisi, jika_benar, jika_salah)`, `AND()`, `OR()`, `IFERROR(nilai, default)`.
Angka: `ROUND()`, `ROUNDUP()`, `ROUNDDOWN()`, `ABS()`, `SUM()` (dalam rumus ringkasan/summary).

Rumus lain di luar daftar ini boleh diminta pengguna — tulis dengan Python biasa mengikuti pola
di atas (`$Kolom` untuk membaca kolom lain, baris terakhir = hasil), lalu sampaikan **jujur**
bahwa itu belum diuji langsung di Grist sungguhan dan minta pengguna mengetesnya (Grist
langsung menunjukkan galat bila ada yang salah, mudah diperbaiki).
