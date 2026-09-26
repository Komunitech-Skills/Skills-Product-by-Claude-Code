# Uji ulang v1.0.2 — Skenario 5: di luar cakupan (file bukan ekspor pesanan)

File fiktif `laporan-omzet.csv` (`Tanggal, Total Penjualan, Total Pesanan, Rata-rata Nilai
Pesanan`) — laporan rekap omzet harian, BUKAN ekspor daftar pesanan per baris. Sesuai SKILL.md
bagian "Kapan TIDAK digunakan", skill harus menolak dengan jelas, bukan mengarang daftar.

```
python3 scripts/resi.py laporan-omzet.csv --json
```

## Hasil
- `ok: false`, exit code 1, **tidak ada traceback**.
- `error`: "Judul kolom pesanan tidak dikenali. Pastikan ini file ekspor PESANAN marketplace
  (bukan laporan lain)... Kolom yang ada di file: Tanggal, Total Penjualan, Total Pesanan,
  Rata-rata Nilai Pesanan. ... sebutkan manual salah satu atau lebih flag berikut ... --kolom-no-
  pesanan "Nama Kolom", --kolom-sku "Nama Kolom", ..." — pesan **langsung menyebut kemungkinan
  penyebab (file bukan ekspor pesanan) dan menyediakan jalan keluar** (`--kolom-...`) meski di
  kasus ini jalan keluar itu memang tidak relevan (filenya bukan data pesanan sama sekali) —
  sesuai instruksi SKILL.md langkah 5, agent yang memakai skill ini masih harus menilai apakah
  override masuk akal atau memang harus bilang ke pengguna "ini bukan file pesanan".
- `kolom_ada` mencantumkan 4 kolom asli file — tidak ada yang disembunyikan/disalahartikan.
- Tidak ada file output ditulis (tidak ada `daftar-ambil.md`/`urutan-resi.md` di folder ini) —
  dikonfirmasi tidak mengarang daftar dari data yang tidak sesuai.

**Hasil: BENAR**, sesuai batasan cakupan yang didokumentasikan.
