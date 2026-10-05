# Lembar Kerja Tender — [Nama Paket]

## 1. Ringkasan paket (salin dari SPSE / dokumen pemilihan)
| Data | Isi |
|---|---|
| Nama paket / kode tender | |
| Instansi / LPSE | |
| Metode (tender / seleksi / pengadaan langsung / e-purchasing / tender cepat) | |
| Jenis (barang / konstruksi / jasa lainnya / konsultansi / terintegrasi) → `--jenis` | |
| Kualifikasi usaha (kecil / non-kecil) | |
| KBLI / SBU yang diminta | |
| Syarat TKDN (paling sedikit 25%?) | |
| Pagu (s.d. Rp15 M → cadangan UMK, Pasal 65 ayat (3)–(4)) | Rp |
| HPS | Rp |
| Jaminan penawaran? (hanya konstruksi/terintegrasi, HPS > Rp10 M: 1%–3%; nilai, masa berlaku) | |
| Masa berlaku penawaran | ... hari kalender |
| Jangka waktu pelaksanaan | ... hari kalender |
| Jadwal: pengumuman / penjelasan / batas unggah / pembukaan | |

## 2. Keputusan ikut
| Cek kelayakan | Hasil | Catatan |
|---|---|---|
| Kualifikasi usaha cocok | Ya / Tidak | |
| KBLI di NIB cocok | Ya / Tidak | |
| NPWP & status PKP | Ya / Tidak | |
| SBU/SKK (konstruksi) | Ya / Tidak / Tidak perlu | |
| Pengalaman | Ya / Tidak / Dikecualikan | |
| SKP (konstruksi) = 5 − paket berjalan | ... | |
| Modal kerja cukup (setelah potongan PPN/PPh bendahara) | Ya / Tidak | |
**Keputusan:** IKUT / TIDAK IKUT — alasan: ...

## 3. Tabel spesifikasi (diminta vs ditawarkan)
| No | Item | Spesifikasi diminta | Ditawarkan (merek/tipe) | Memenuhi? |
|---|---|---|---|---|
| 1 | | | | Ya / Tidak |

## 4. Rincian harga
Isi `contoh-rincian.csv` (kolom: No; Uraian; Volume; Satuan; Harga Satuan; Jumlah — kolom Jumlah opsional, dicek per baris) lalu jalankan:
`python3 scripts/cek_penawaran.py harga rincian.csv --ppn nonmewah --hps "Rp ..." --jenis barang`
(Windows: `py scripts\cek_penawaran.py ...`). Tanpa script: pakai rumus di SKILL.md.

## 5. Jadwal mundur
`python3 scripts/cek_penawaran.py jadwal --batas "YYYY-MM-DD HH:MM" --penjelasan YYYY-MM-DD --libur YYYY-MM-DD`
