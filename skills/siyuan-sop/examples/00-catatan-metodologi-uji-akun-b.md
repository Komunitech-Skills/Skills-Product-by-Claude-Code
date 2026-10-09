# Catatan metodologi — uji independen Akun B (2026-09-26)

## Kernel SiYuan: tiruan, bukan asli — alasan
Dicoba menjalankan kernel SiYuan v3.8.5 asli (rilis resmi GitHub) sesuai instruksi. Akses ke
`github.com`/`api.github.com` dari sandbox sesi ini **ditolak oleh proxy jaringan sesi**
("GitHub access to this repository is not enabled for this session" / HTTP 403 untuk unduhan
biner rilis; `add_repo` hanya membuka `git clone` sumber, bukan unduhan aset rilis biner, dan
membangun SiYuan dari sumber — Go + frontend — tidak realistis dalam batas waktu 15 menit).
Karena itu dipakai **server kernel tiruan buatan sendiri** (`mock_kernel.py`, `http.server`
standar Python, ditulis independen — tidak menyalin `tests/test_siyuan.py` milik pembuat) yang
meniru bentuk endpoint `/api/notebook/*`, `/api/query/sql`, `/api/filetree/*`,
`/api/export/exportMdContent`, `/api/block/appendBlock` berdasar `references/api-endpoints.md` dan
`tests/fixtures/siyuan-3.8.5-respons.json` (dibaca sebagai referensi **bentuk** data, bukan disalin
logikanya).

**Keterbatasan yang jujur diakui:** mock ini tidak mereplikasi mesin FTS/indeks SiYuan asli (mis.
jeda pengindeksan yang dicatat pembuat di skenario 01 aslinya) dan pengurai SQL di dalamnya sengaja
sederhana (bukan SQLite sungguhan) — untuk kasus injeksi SQL, verifikasi utama dilakukan **langsung
terhadap kode `scripts/siyuan.py`** (fungsi `escape_sql_literal`/`escape_like`), bukan hanya
lewat balasan mock, agar kesimpulan tetap valid walau mock terbatas. Temuan pembuat soal kernel asli
(Skenario 01 pembuat: jeda indeks; audit: request tanpa Authorization diproses) **tidak dapat
direproduksi ulang terhadap kernel asli** oleh Akun B karena kendala jaringan ini — kedua temuan itu
diverifikasi lewat pembacaan kode + dokumentasi + replikasi perilaku yang relevan di mock (lihat
`05-di-luar-cakupan-uji-akun-b.md` Kasus D), bukan lewat kernel asli sendiri. Ini keterbatasan uji,
dicatat apa adanya sesuai instruksi.

## Yang dijalankan
- 42 uji unit bawaan (`python3 -m unittest discover -s tests`) — semua **OK**.
- `python3 scripts/validate.py --skill siyuan-sop` dari root — **lolos**.
- 5 skenario manual end-to-end terhadap mock kernel independen (lihat `01`-`05`).
- Perbandingan A/B tanpa-skill vs dengan-skill (`00-pembanding-tanpa-skill.md`).
- Perbandingan pesaing via pencarian web (`00-banding-pesaing.md`).
