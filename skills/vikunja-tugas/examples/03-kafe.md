# Skenario 03 — Kafe (normal): tugas harian & tandai selesai

**Penguji:** pembuat skill, 2026-09-26. Dijalankan sungguhan terhadap **Vikunja 2.6.0 asli**,
proyek "Kafe Senja" (id 4).

## Permintaan pengguna
> "Tambahin 3 tugas buat kafe: belanja susu & biji kopi hari ini prioritas tinggi, servis mesin espresso minggu depan, sama bayar sewa 3 hari lagi prioritas mendesak tugaskan ke komunitech_test"

## Perintah agent (tiga kali `tambah --ya`, tiap kali dipratinjaukan dulu)
```bash
python3 scripts/vikunja.py tambah --proyek "Kafe Senja" --judul "Belanja susu & biji kopi" --tenggat "hari ini" --prioritas 3 --ya
python3 scripts/vikunja.py tambah --proyek "Kafe Senja" --judul "Servis mesin espresso" --tenggat "minggu depan" --ya
python3 scripts/vikunja.py tambah --proyek "Kafe Senja" --judul "Bayar sewa bulan ini" --tenggat "3 hari lagi" --prioritas 4 --ke komunitech_test --ya
```
```
TERSIMPAN 1 TUGAS DI VIKUNJA:
- #8 Belanja susu & biji kopi (proyek id 4)
TERSIMPAN 1 TUGAS DI VIKUNJA:
- #9 Servis mesin espresso (proyek id 4)
TERSIMPAN 1 TUGAS DI VIKUNJA:
- #10 Bayar sewa bulan ini (proyek id 4)
```

## "Tugas hari ini di kafe apa aja?"
```bash
python3 scripts/vikunja.py hari-ini --proyek "Kafe Senja"
```
```
TUGAS HARI INI (Sabtu, 26 September 2026)
Proyek: Kafe Senja
Jumlah: 1
- Belanja susu & biji kopi (tinggi; jatuh tempo 26 Sep 2026)
```

## "Minggu ini ada apa?"
```bash
python3 scripts/vikunja.py minggu-ini --proyek "Kafe Senja"
```
```
TUGAS 7 HARI KE DEPAN
Proyek: Kafe Senja
Jumlah: 2
- Belanja susu & biji kopi (tinggi; jatuh tempo 26 Sep 2026)
- Bayar sewa bulan ini (mendesak; jatuh tempo 29 Sep 2026; PIC: komunitech_test)
```
("Servis mesin espresso", jatuh tempo 7 hari lagi persis, secara sengaja **tidak** dihitung
"minggu ini" — jendela yang dipakai adalah hari ini sampai +7 hari, TIDAK termasuk hari ke-7
itu sendiri. Ini konsisten & terdokumentasi, bukan bug.)

## "Belanja susunya sudah, tandai selesai"
```bash
python3 scripts/vikunja.py selesai --id 8
```
```
PRATINJAU TANDAI SELESAI: #8 Belanja susu & biji kopi
Belum disimpan. Ulangi perintah yang sama + --ya untuk menyimpan.
```
Setelah "ya":
```bash
python3 scripts/vikunja.py selesai --id 8 --ya
```
```
SELESAI: #8 Belanja susu & biji kopi ditandai selesai di Vikunja.
```

**Kesimpulan:** parser tanggal Indonesia ("hari ini", "minggu depan", "N hari lagi") dan batas
jendela `minggu-ini` bekerja tepat sesuai dokumentasi; `selesai` selalu meminta konfirmasi.
