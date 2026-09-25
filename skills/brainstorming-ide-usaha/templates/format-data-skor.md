# Format Data untuk scripts/skor_ide.py

Dipakai di Langkah Kerja B.4/C.5 SKILL.md. Butuh file ide (CSV); file bobot (JSON) **opsional** — lihat "Bobot default resmi" di bawah. Kalau bobot diberikan, nama kolom kriteria di kedua file **harus sama persis**.

## File ide (CSV)

Baris pertama = header. Kolom pertama selalu `nama_ide`. Kolom berikutnya = satu kriteria per kolom, nilai **1–5** (1 = sangat rendah/buruk, 5 = sangat tinggi/baik untuk kriteria itu). Boleh format Excel Indonesia: file "CSV UTF-8" (dengan BOM), pemisah kolom `;`, dan nilai desimal pakai koma (mis. `3,5`) — script mendeteksi ini otomatis. Kalau memakai pemisah `,` biasa dan butuh koma desimal, beri tanda kutip (`"3,5"`) supaya tidak dianggap dua kolom terpisah.

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

## File bobot (JSON) — opsional

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

### Bobot default resmi (kalau `--bobot` tidak diberikan)

Untuk mode cepat atau saat pengguna belum sempat menyepakati bobot, `--bobot` boleh dilewatkan. Script otomatis memakai:
- **Bobot default resmi di atas** (`kesesuaian_modal=5, potensi_permintaan=4, kemudahan_eksekusi=3, kecocokan_keahlian=2, potensi_margin=4`) — kalau nama lima kolom kriteria di file ide **persis sama** dengan lima nama itu.
- **Bobot sama rata** (semua kriteria = 1) — kalau nama kolomnya berbeda (mis. pengguna pakai kriteria sendiri).

Sumber bobot yang dipakai selalu disebutkan di baris terakhir keluaran script — jangan sampaikan skor ke pengguna tanpa menyebut bobot mana yang dipakai.

## Menjalankan

```bash
python3 scripts/skor_ide.py skor --ide ide.csv --bobot bobot.json
python3 scripts/skor_ide.py skor --ide ide.csv               # tanpa bobot -> pakai default resmi/sama rata
```

Windows (kalau `python3` tidak dikenali, coba `python` atau `py`):
```bash
py scripts/skor_ide.py skor --ide ide.csv --bobot bobot.json
```

Keluaran: tabel ide terurut dari skor tertimbang tertinggi ke terendah, plus tanda kalau ada dua ide atau lebih yang skornya sama persis (seri) — dalam kasus itu, putuskan pemenang lewat diskusi untung-rugi kualitatif, jangan asal pilih baris pertama.

## Menghitung titik impas kasar (opsional)

```bash
python3 scripts/skor_ide.py impas --modal 5000000 --margin 15000
python3 scripts/skor_ide.py impas --modal Rp5.000.000 --margin 15rb
```

`--modal`/`--margin` menerima angka biasa (`5000000`), format ribuan Indonesia (`5.000.000`), dengan awalan `Rp` (`Rp5.000.000`), atau singkatan (`5jt` = 5 juta, `15rb` = 15 ribu). Menghitung jumlah unit yang harus terjual untuk menutup modal awal (`modal ÷ margin per unit`, dibulatkan ke atas). "Unit" bisa berarti transaksi, pelanggan, atau siklus langganan tergantung jenis usaha. Ini **perkiraan kasar** untuk menimbang ide, bukan pengganti perhitungan HPP lengkap dari resep/BOM (pakai skill `hitung-hpp` untuk itu).
