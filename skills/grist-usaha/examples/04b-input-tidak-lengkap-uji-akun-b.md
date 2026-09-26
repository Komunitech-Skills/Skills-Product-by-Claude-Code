# Skenario 4 (input tidak lengkap) — 5 varian, diuji independen

1. **`buat-tabel pelanggan` tanpa `--dokumen`** (argparse wajib):
   ```
   grist.py buat-tabel: error: the following arguments are required: --dokumen
   ```
   rc=2. Ditolak sebelum menyentuh jaringan — benar.

2. **`pola tampilkan supplier`** (pola tidak ada dalam 4 pola siap pakai):
   ```
   error: argument nama: invalid choice: 'supplier' (choose from 'pelanggan', 'pesanan', 'stok', 'jadwal-konten')
   ```
   Pesan menyebutkan pilihan yang valid — pengguna awam langsung tahu harus pilih apa.

3. **`ringkasan toko-berkah-jaya.grist Karyawan`** (nama tabel salah/tidak ada):
   ```
   GAGAL: Tabel 'Karyawan' tidak ada. Tabel yang ada: StokOpname, RekapHarian
   ```
   Menyebutkan tabel yang benar-benar ada — tidak menebak, tidak menampilkan traceback teknis.

4. **`daftar-tabel tidak-ada.grist`** (path file salah):
   ```
   GAGAL: File 'ujiku/tidak-ada.grist' tidak ditemukan.
   ```

5. **Dokumen ambigu di REST API** — didaftarkan 2 dokumen bernama mirip di server tiruan
   independen ("Toko Berkah Jaya" & "Toko Berkah Cabang 2"), lalu `--dokumen "Toko Berkah"`:
   script (fungsi `cari_dokumen`) mencetak daftar kedua docId yang cocok dan minta pengguna
   menyebutkan salah satu docId — **tidak menebak**, konsisten dengan klaim SKILL.md.

## Hasil
Semua 5 varian ditangani dengan pesan yang jelas, dalam bahasa Indonesia, tanpa jargon Python,
tanpa menebak sembarangan. Sesuai harapan.
