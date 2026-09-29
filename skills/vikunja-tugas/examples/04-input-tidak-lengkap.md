# Skenario 04 — Input tidak lengkap

**Penguji:** pembuat skill, 2026-09-26. Dijalankan sungguhan terhadap **Vikunja 2.6.0 asli**.

## Kasus A — proyek tidak disebutkan
> "Tambahin tugas beli galon air"

Agent tidak boleh menebak proyek. Menjalankan pratinjau tanpa `--proyek`:
```bash
python3 scripts/vikunja.py tambah --judul "Beli galon air"
```
```
GALAT: Tugas 'Beli galon air': proyek tidak disebutkan (--proyek, atau isi field 'proyek' di --batch).
```
(kode keluar 2). Agent bertanya balik **sekali**: "Ini masuk proyek yang mana? Proyek yang ada:
Toko Bangunan Sinar Jaya, Kantor Konsultan Mitra Prima, Kafe Senja, Kafe Senja Cabang 2." (daftar
diambil dari `daftar-proyek`, bukan dikarang).

## Kasus B — nama proyek ambigu
> "Tambahin tugas beli galon air ke kafe"

Ada dua proyek yang mengandung kata "Kafe":
```bash
python3 scripts/vikunja.py tambah --proyek "Kafe" --judul "Beli galon air"
```
```
GALAT: Nama proyek 'Kafe' cocok lebih dari satu: Kafe Senja (id 4); Kafe Senja Cabang 2 (id 5). Sebutkan id-nya.
```
Agent menanyakan mana yang dimaksud, menyebut kedua pilihan apa adanya.

## Kasus C — tanggal tidak jelas
> "Tugas beli galon, kerjain nanti deh"

"Nanti deh" bukan frasa tanggal yang dikenali:
```bash
python3 scripts/vikunja.py tambah --proyek 4 --judul "Beli galon air" --tenggat "nanti deh"
```
```
GALAT: Tenggat tidak dikenali: 'nanti deh'. Format yang didukung: 'hari ini', 'besok', 'lusa', 'N hari lagi', nama hari ('Jumat', 'Jumat depan'), 'minggu depan', '25/10', '25/10/2026', '25 Oktober 2026', '2026-10-25' — boleh diakhiri 'jam 14:00'.
```
Agent menawarkan: buat tugas **tanpa** tenggat dulu (hapus `--tenggat`), atau tanyakan tanggal
konkret ke pengguna. Tidak menebak tanggal secara diam-diam.

**Kesimpulan:** untuk ketiga kekurangan input yang paling umum (proyek tidak disebut, nama
proyek ambigu, tanggal tidak jelas), skill menolak dengan pesan jelas dan daftar pilihan nyata
dari Vikunja — bukan menebak atau membuat data yang salah.
