# Uji 04 — Input tidak lengkap: "tolong analisis file saya"

> Uji independen Tahap 6, 2026-09-25. `claude-code (simulasi agent)`, mengikuti SKILL.md apa adanya.

## Skenario A — tanpa file, tanpa tujuan
**Pengguna:** "tolong analisis file saya"

Acuan SKILL.md: tabel *Input* (file wajib → "minta dikirim"; pertanyaan tidak wajib → default
`profil` + `ringkas` + 3 temuan) dan aturan "tanyakan **sekali** dalam satu pesan singkat".

**Jawaban agent (dengan skill):**
> Siap, saya bantu. Supaya hasilnya pas, mohon kirim sekaligus:
> 1. **File-nya** (Excel .xlsx atau CSV). File .xls lama: buka di Excel → *Save As* → .xlsx.
> 2. **Mau tahu apa?** mis. total per kategori, tren per bulan, 10 pelanggan terbesar, bandingkan dua bulan,
>    atau rapikan data. Kalau belum tahu, saya kenali isinya dulu lalu beri 3 temuan utama.
> 3. Bila ada beberapa sheet: sheet mana yang dipakai (bila tidak disebut, saya pakai sheet pertama yang terlihat dan saya sebutkan).
>
> File diproses di komputer ini saja, tidak diunggah ke mana pun.

Penilaian: ✔ satu pesan, pertanyaan singkat, ada default, tidak mengarang angka. Tidak ada script yang dijalankan.

## Skenario B — file dikirim, tujuan tetap tidak jelas ("langsung aja")
Agent menjalankan default `profil` lalu `ringkas` pada `Penjualan 2026.xlsx`:
```bash
python3 scripts/analisis.py profil "Penjualan 2026.xlsx"
python3 scripts/analisis.py ringkas "Penjualan 2026.xlsx"
```
Hasil nyata: script memilih sheet **Q1** (sheet pertama yang *terlihat*, melewati `Master Barang`
yang tersembunyi) dan memperingatkan "Workbook punya 4 sheet (...); yang dianalisis: 'Q1'". Agent
menyebut asumsi itu di awal jawaban: *"Asumsi: saya lihat sheet Q1 dulu (Jan–Mar, 147 transaksi,
total Rp 67.313.000). Ada juga sheet Q2 dan Q3 — mau saya lihat semuanya?"*

Penilaian: ✔ asumsi disebut, peringatan diteruskan. ⚠ Default "sheet pertama" untuk workbook berisi
sheet per periode membuat analisis hanya 1/3 data; dengan fitur gabung sheet (HASIL-UJI #1) default
yang lebih baik adalah menawarkan gabungan bila semua sheet punya judul kolom sama.

## Skenario C — kolom/sheet yang disebut tidak ada
```bash
$ python3 scripts/analisis.py profil "Penjualan 2026.xlsx" --sheet Q4
GAGAL: Sheet 'Q4' tidak ada. Sheet yang tersedia: 1. Master Barang, 2. Q1, 3. Q2, 4. Q3.      (kode keluar 2)
$ python3 scripts/analisis.py pivot "Penjualan 2026.xlsx" --sheet q2 --grup kat --nilai omzet
GAGAL: Kolom nilai 'omzet' tidak ada. Kolom yang tersedia: Tanggal, No Nota, Kategori, Barang, Qty, Harga Satuan, Total, Pelanggan.   (kode 2)
```
✔ Pesan awam, tanpa traceback; `--sheet q2` (huruf kecil) dan `--grup kat` (sebagian nama) diterima.
Agent menjawab: *"Di file tidak ada kolom 'omzet'. Yang mirip: 'Total'. Pakai kolom Total?"*
