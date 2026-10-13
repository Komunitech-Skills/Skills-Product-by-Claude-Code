# Riwayat perubahan — validasi-ide-produk-baru

Catatan teknis per versi (dipindah dari README agar halaman pembeli ringkas).

## Catatan revisi 1.0.6 (2026-10-13)
- Batasan di SKILL.md: aturan eksplisit anti-karangan (jangan mengarang angka/kebijakan/tindakan yang tidak diberikan pengguna; tulis `[isian: ...]` atau tandai asumsi). Temuan audit contoh: angka hasil uji pasar di `examples/01` dan `examples/02` kini ditandai sebagai data fiktif yang dimasukkan pengguna (input lanjutan). Logika dan skrip tidak berubah.

## 1.0.5 (2026-10-13)
- Rujukan ke skill `brainstorming-ide-usaha` (status arsip, tidak dijual) dihapus dari description, bagian Kapan TIDAK digunakan, dan langkah GAGAL; diganti arahan netral. Logika & skrip tidak berubah.

## Catatan revisi 1.0.4 (2026-10-01)
Hasil uji sebelum/sesudah di OpenClaw (`examples/00-openclaw-sebelum-sesudah.md`) menemukan salah hitung: 52 vote polling IG dijumlahkan dengan 4 PO berbayar sehingga muncul klaim "balik modal +Rp416.000" (yang benar −Rp26.000). Perbaikan:
- **Aturan hitung baru di SKILL.md:** hanya pesanan berkomitmen (PO sudah transfer/DP/bayar, checkout, laku terjual) yang masuk konversi, pendapatan, margin, dan balik modal. Vote/like/komentar/"mau" = **minat**, dilaporkan terpisah dan tidak pernah dijumlahkan dengan pesanan. Instruksi lama "gabungkan metode jadi satu total" dihapus.
- `scripts/hitung_validasi.py`: argumen `--minat`, mode JSON `kanal` (pesanan & minat per kanal dipisah otomatis), status "BELUM BISA DINILAI" bila hanya ada minat, rumus ditampilkan di setiap baris uang, format rugi `-Rp26.000`.
- Untung/rugi wajib lewat script atau rumus eksplisit yang ditampilkan; satu set ambang ditetapkan di awal sesuai harga.
- `references/menu-uji-murah.md` dan `templates/form-pencatatan.md` memisahkan kolom pesanan vs minat.
- `tests/uji_regresi.py`: +17 cek regresi (kasus keripik: 4 pesanan, −Rp26.000, tidak boleh muncul 56/416).

## Riwayat versi

- **1.0.1** (2026-09-26) — Revisi hasil uji independen Tahap 6 (skor 7,5/10, lihat `examples/HASIL-UJI.md`):
  - **Bug diperbaiki:** `scripts/hitung_validasi.py` salah membaca harga format Indonesia bertitik ribuan (mis. `25.000` terbaca `25`, salah 1000x diam-diam). Fungsi `parse_uang` baru kini mendukung `Rp25.000`, `150.000`, `1.234.567`, singkatan `25rb`/`1jt`/`1,5jt`, dan **menolak** pola ambigu (`25.5`, `1.234,56`, `25,000` tanpa singkatan) dengan pesan jelas alih-alih menebak. Tes regresi baru: `tests/uji_regresi.py` (23 kasus, 14 diterima + 9 ditolak).
  - `templates/pesan-uji-murah.md`: template #1 (broadcast WA pre-order) dan #4 (listing PO marketplace) kini menyebutkan eksplisit kebijakan batal/refund (uang kembali 100% bila batch tidak jadi diproduksi atau pembeli batal sebelum masa produksi, dengan batas waktu pengembalian) — sebelumnya tidak disebut sama sekali.
  - `ATTRIBUTION.md`: commit hash sumber diverifikasi ulang (`1cef1a9eae10017389863d51e289e0ae41e17fcb`, 40 karakter SHA-1, sesuai `git rev-parse HEAD` repo sumber).
- **1.0.0** (2026-09-26) — Rilis awal (status `draft`, hasil ATM dari `product-on-purpose/pm-skills`, Apache-2.0).
