# Dasbor KPI lokal (ekspor-db)

Tujuan: melihat skor KPI (perusahaan → divisi → orang, tren, KPI merah) di browser tanpa software
baru berbayar. Angka **dihitung `skor_kpi.py`** (aturan sama dengan perintah `skor`); dasbor hanya
menampilkan.

## Perintah
```bash
python3 scripts/skor_kpi.py ekspor-db --rencana KPI/rencana-kpi.csv --realisasi KPI/realisasi.csv \
  --keluar KPI/dasbor [--anonim] [--anonim-divisi] [--grist] [--timpa]
```
Opsi aturan skor sama seperti `skor`: `--cap`, `--hijau`, `--kuning`, `--data-kosong`, `--min-bobot`,
`--bobot-divisi`, `--duplikat`, `--periode-default`, `--izinkan-minus`.

## Isi folder hasil
| File | Isi |
|---|---|
| `kpi.db` | SQLite. Tabel: `skor_perusahaan`, `skor_divisi`, `skor_orang`, `skor_kpi` (rincian, `tingkat` orang/divisi), `rencana`, `meta` |
| `kpi-metadata.yml` | Query siap klik untuk Datasette (sama dengan blok `kpi` di `dasbor-lokal/templates/metadata.yml`) |
| `kunci-kode-RAHASIA.csv` | Hanya mode `--anonim`: daftar kode = nama. Simpan terpisah! |
| `grist/*.csv` + `PETUNJUK-IMPOR-GRIST.md` | Hanya `--grist`: satu CSV per tabel |

Kolom penting: `status` = hijau/kuning/merah/belum (⚪ belum lengkap); `tren` = selisih poin
vs periode sebelumnya (kosong = tidak ada pembanding); `lengkap` 1/0; `jumlah_kpi_merah`.
Angka dibulatkan seperti tampilan laporan (skor 1 desimal, nilai 2 desimal). Titik desimal (`93.6`).

## Query siap pakai (Datasette: klik nama di halaman `kpi`; tanpa Datasette: dasbor-lokal)
| Nama | Isi | `dasbor.py query kpi-tim ...` |
|---|---|---|
| `perusahaan_tren` | skor perusahaan tiap periode | `perusahaan-tren` |
| `divisi_terbaru` | skor tiap divisi, periode terbaru | `divisi-terbaru` |
| `orang_terbaru` | skor tiap orang per divisi, periode terbaru | `orang-terbaru` |
| `tren_orang` | skor tiap orang tiap periode | `tren-orang` |
| `kpi_merah` | KPI berstatus merah, periode terbaru | `kpi-merah` |

## Membuka di Datasette (baca-saja, komputer ini saja)
```bash
datasette -i KPI/dasbor/kpi.db -m KPI/dasbor/kpi-metadata.yml --host 127.0.0.1
```
Buka `http://127.0.0.1:8001`. `-i` = immutable (data tidak bisa berubah lewat dasbor). Pasang
Datasette sekali: `docs/panduan-datasette.md`. Bila sudah memakai `dasbor-lokal`: taruh `kpi.db`
di `~/KomunitechData/kpi/kpi.db` (atau `KOMUNITECH_KPI_DB`), lalu `dasbor.py datasette`
mencetak perintah gabungan semua database.

## Grist (untuk yang sudah memakai `grist-usaha`)
`ekspor-db ... --grist` → ikuti `grist/PETUNJUK-IMPOR-GRIST.md` (Add New → Import from file, satu
tabel per CSV; semaphore lewat Cell Style; grafik tren lewat widget Chart). Bulan berikutnya
ekspor ulang dengan `--timpa --grist` lalu impor ulang/Update existing table.

## Privasi
Lihat `references/privasi-etika.md` bagian "Dasbor lokal". Ringkas: hanya `127.0.0.1`, jangan
dibagikan, pakai `--anonim` untuk layar bersama, skor = bahan diskusi bukan dasar sanksi/PHK.

## Cara kerja tren & periode
Semua periode di file realisasi yang punya rencana berlaku dan minimal satu angka masuk. Periode
tanpa data dilewati (dicantumkan di keluaran). Tren dihitung sama dengan `skor`.
