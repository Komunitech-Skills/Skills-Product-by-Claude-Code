# 04 — Input tidak lengkap

> Penguji independen Akun B, 26-09-2026. Simulasi agent (claude-code) mengikuti SKILL.md; perintah script dijalankan nyata di database uji. Nama FIKTIF.

## Permintaan pemilik
"Tolong hitung gaji bulan ini buat 3 karyawan baru saya: Rudi 5 juta, Sinta 6 juta, sama Tono."

## Yang kurang (menurut tabel Input SKILL.md)
Status PTKP (wajib), tanggal masuk (wajib), gaji pokok Tono (wajib). BPJS/UMK/JKK punya default.

## Perilaku script bila agent nekat menjalankan
```
$ gaji.py karyawan tambah --nama "Rudi Fiktif" --gaji-pokok 5jt
GAGAL: Rudi Fiktif: ptkp wajib diisi (--ptkp TK/0..K/3).           (kode 1)
$ gaji.py karyawan tambah --nama "Rudi Fiktif" --gaji-pokok 5jt --ptkp TK/0
GAGAL: Rudi Fiktif: tanggal masuk wajib diisi (--masuk YYYY-MM-DD (dipakai untuk PPh 21 bulan pertama/akhir & THR)).
```
→ Script tidak menebak PTKP/tanggal masuk. ✅ (Kekurangan kecil: kesalahan ditampilkan satu per satu, bukan sekaligus.)

## Jawaban agent yang benar (satu pesan, ≤ 5 pertanyaan — sesuai aturan SKILL.md)
> Siap, saya bantu. Supaya gajinya benar, saya perlu 5 hal dulu:
> 1. Status pajak (PTKP) masing-masing: lajang/menikah dan jumlah tanggungan (mis. TK/0, K/1)?
> 2. Tanggal mulai kerja Rudi, Sinta, dan Tono?
> 3. Gaji pokok Tono berapa? Ada tunjangan tetap (mis. transport/jabatan) untuk mereka?
> 4. Mereka ikut BPJS Kesehatan, JHT/JKK/JKM, dan JP semua? (Kalau tidak dijawab, saya anggap ikut semua.)
> 5. UMK kota Anda dan kelas risiko JKK? (Kalau tidak tahu: JKK 0,24% dan UMK tidak dicek — saya sebutkan di hasil.)
> Kalau mereka masuk di tengah bulan, gaji bulan ini dibayar penuh atau prorata sesuai perjanjian kerja?

Bila pemilik menjawab "pakai default saja": agent tetap **tidak boleh** menebak PTKP/tanggal masuk (wajib, script menolak); default hanya untuk BPJS (semua), JKK 0,24%, UMK tidak dicek, pola 5 hari — dan asumsi itu disebut di jawaban.

## Penilaian
- Script: menolak data wajib yang kosong dengan pesan jelas ✅.
- SKILL.md: aturan "tanya sekali, maks. 5 pertanyaan" + tabel wajib/default jelas ✅.
- Catatan: pertanyaan prorata sebaiknya ikut ditanyakan di awal (SKILL.md menaruhnya di Langkah C; agent bisa lupa).
- Skor skenario: 9/10.
