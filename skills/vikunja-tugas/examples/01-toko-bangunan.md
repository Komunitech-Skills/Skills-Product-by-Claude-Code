# Skenario 01 — Toko bangunan (normal)

**Penguji:** pembuat skill, 2026-09-26. Dijalankan sungguhan terhadap **Vikunja 2.6.0 asli**
(binary resmi, checksum SHA-256 cocok) di `127.0.0.1:3456`, proyek "Toko Bangunan Sinar Jaya" (id 2).

## Permintaan pengguna
> "Buatkan tugas untuk toko bangunan: cek stok cat tembok, jatuh tempo besok, prioritas tinggi, tugaskan ke komunitech_test"

## Perintah agent
```bash
python3 scripts/vikunja.py tambah --proyek "Toko Bangunan" --judul "Cek stok cat tembok" \
  --tenggat "besok" --prioritas 3 --ke komunitech_test
```

## Keluaran (pratinjau)
```
PRATINJAU TAMBAH TUGAS
1.
   Judul : Cek stok cat tembok
   Proyek: Toko Bangunan Sinar Jaya (id 2)
   Tenggat: Minggu, 27 September 2026
   Prioritas: 3 (tinggi)
   Ditugaskan ke: komunitech_test

Belum disimpan. Ulangi perintah yang sama + --ya untuk menyimpan ke Vikunja.
```
Agent menunjukkan pratinjau ini ke pengguna dan menanyakan "Simpan ke Vikunja? (ya/tidak)".

## Setelah pengguna menjawab "ya"
```bash
python3 scripts/vikunja.py tambah --proyek "Toko Bangunan" --judul "Cek stok cat tembok" \
  --tenggat "besok" --prioritas 3 --ke komunitech_test --ya
```
```
TERSIMPAN 1 TUGAS DI VIKUNJA:
- #3 Cek stok cat tembok (proyek id 2)
```

## Permintaan lanjutan
> "Ada tugas yang telat gak?"
```bash
python3 scripts/vikunja.py terlambat
```
```
TUGAS TERLAMBAT
Proyek: semua proyek
Jumlah: 1
- Tagih pelanggan telat (jatuh tempo 20 Sep 2026; proyek: Toko Bangunan Sinar Jaya; PIC: komunitech_test)
```

> "Cari tugas yang ada kata stok"
```bash
python3 scripts/vikunja.py cari "stok"
```
```
HASIL CARI: 'stok'
Jumlah: 1
- Cek stok cat tembok (tinggi; jatuh tempo 27 Sep 2026; proyek: Toko Bangunan Sinar Jaya; PIC: komunitech_test)
```

**Kesimpulan:** tambah tugas dengan tenggat bahasa Indonesia, prioritas, dan penugasan berjalan
benar dalam satu kali pratinjau + konfirmasi; pencarian & filter terlambat lintas proyek akurat.
