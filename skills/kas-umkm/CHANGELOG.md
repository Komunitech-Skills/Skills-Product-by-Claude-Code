# Riwayat perubahan — kas-umkm

Catatan teknis per versi (dipindah dari README agar halaman pembeli ringkas).

## Catatan revisi 1.0.13 (2026-10-17)
- Contoh rekap harian di `SKILL.md` diganti keluaran asli dari `examples/contoh-01-warung-sehari.md` (angka sebelumnya tidak punya berkas sumber); cara kerja tidak berubah.

## Catatan revisi 1.0.12 (2026-10-02)
- Biaya operasional umum (operasional, bensin/BBM/solar, uang makan sopir, tol, parkir, transport, ongkir, uang jalan) kini dikenali sebagai pengeluaran usaha, sehingga untung tidak tampak terlalu besar.
- Bila masih ada baris yang belum jelas ("perlu dicek"), hasil usaha ditulis sebagai **sementara** beserta angka bila baris itu ternyata biaya usaha, agar tidak menyesatkan. 102 uji otomatis lulus.

## Catatan revisi 1.0.11 (2026-10-01)
- **Rekap catatan kas dari teks/file tanpa database** (perintah baru `cek-catatan`): kirim catatan kas hari ini (file atau ketikan), langsung dapat pemasukan, pengeluaran usaha, untung hari itu, uang laci seharusnya, dan selisih (kurang/lebih) dengan uang yang dihitung — tanpa menyimpan apa pun. Kasbon, prive, dan uang QRIS/transfer dipisah otomatis. Setelah itu Anda bisa memilih menyimpannya ke buku kas.
- Skill kini terpicu oleh kalimat seperti "rekap catatan kas dari file", "uang di laci harusnya berapa", "kok laci kurang" (temuan uji OpenClaw: sebelumnya skill tidak terpakai).
- Instruksi: script dijalankan dari subfolder `scripts/` di folder skill; file pengguna dicari di folder kerja saja (tidak mencari ke seluruh disk). 100 uji otomatis lulus (4 uji baru).
