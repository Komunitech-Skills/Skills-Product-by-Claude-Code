# Format Data untuk scripts/skor_ide.py

Dipakai di Langkah Kerja C.5 SKILL.md. Dua file dibutuhkan: daftar ide (CSV) dan bobot kriteria (JSON). Nama kolom kriteria di kedua file **harus sama persis**.

## File ide (CSV)

Baris pertama = header. Kolom pertama selalu `nama_ide`. Kolom berikutnya = satu kriteria per kolom, nilai **1–5** (1 = sangat rendah/buruk, 5 = sangat tinggi/baik untuk kriteria itu).

```csv
nama_ide,kesesuaian_modal,potensi_permintaan,kemudahan_eksekusi,kecocokan_keahlian,potensi_margin
Paket laundry kilat 3 jam,4,4,3,5,3
Laundry sepatu & tas,3,3,2,3,4
Member langganan bulanan,5,4,4,4,4
Laundry karpet/gorden,2,3,2,3,4
```

**Kriteria default yang disarankan** (boleh diganti/ditambah sesuai kesepakatan dengan pengguna):
- `kesesuaian_modal` — semakin sesuai dengan modal yang disebutkan pengguna, semakin tinggi.
- `potensi_permintaan` — perkiraan seberapa banyak calon pelanggan yang butuh/mau (berdasar cerita pengguna, bukan angka pasti).
- `kemudahan_eksekusi` — semakin mudah dikerjakan dengan SDM/waktu yang ada, semakin tinggi.
- `kecocokan_keahlian` — semakin cocok dengan keahlian/aset yang sudah dimiliki, semakin tinggi.
- `potensi_margin` — perkiraan margin/untung per unit atau per transaksi.

## File bobot (JSON)

Angka bobot **positif** (tidak harus 1–5, boleh mis. 1–5 atau 1–10) menunjukkan seberapa penting kriteria itu bagi pengguna. Nama kunci harus sama persis dengan nama kolom di file ide.

```json
{
  "kesesuaian_modal": 5,
  "potensi_permintaan": 4,
  "kemudahan_eksekusi": 3,
  "kecocokan_keahlian": 2,
  "potensi_margin": 4
}
```

## Menjalankan

```bash
python3 scripts/skor_ide.py skor --ide ide.csv --bobot bobot.json
```

Windows (kalau `python3` tidak dikenali, coba `python` atau `py`):
```bash
py scripts/skor_ide.py skor --ide ide.csv --bobot bobot.json
```

Keluaran: tabel ide terurut dari skor tertimbang tertinggi ke terendah, plus tanda kalau ada dua ide atau lebih yang skornya sama persis (seri) — dalam kasus itu, putuskan pemenang lewat diskusi untung-rugi kualitatif, jangan asal pilih baris pertama.

## Menghitung titik impas kasar (opsional)

```bash
python3 scripts/skor_ide.py impas --modal 5000000 --margin 15000
```

Menghitung jumlah unit yang harus terjual untuk menutup modal awal (`modal ÷ margin per unit`, dibulatkan ke atas). Ini **perkiraan kasar** untuk menimbang ide, bukan pengganti perhitungan HPP lengkap dari resep/BOM (pakai skill `hitung-hpp` untuk itu).
