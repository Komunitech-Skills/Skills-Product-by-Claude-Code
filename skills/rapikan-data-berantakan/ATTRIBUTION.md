# Atribusi

## Jalur produksi
**Kurasi (ATM = Amati, Tiru, Modifikasi).** Skill ini mengambil dua hal terbukti dari sumber publik, lalu menulis ulang seluruhnya dalam Bahasa Indonesia untuk usaha kecil Indonesia, dengan script Python standar yang ditulis sendiri.

## Sumber 1: konsep "cluster and edit" OpenRefine (BSD-3-Clause)
- **Proyek:** [OpenRefine](https://github.com/OpenRefine/OpenRefine) (OpenRefine contributors; semula dikembangkan Google sebagai Google Refine). 12.000+ bintang, aktif sejak 2012.
- **Lisensi:** BSD 3-Clause (berkas `LICENSE.txt` repo dibaca 2026-10-05).
- **Yang diambil:** *hanya gagasan/metode*: alur "lihat -> kelompokkan -> putuskan -> terapkan"; pengelompokan nilai mirip dengan kunci yang bertabrakan (sidik jari kata: huruf kecil, buang tanda baca & aksen, urutkan kata unik; sidik jari n-gram huruf) dan kemiripan teks antar nilai; prinsip bahwa penggabungan hanya dilakukan setelah disetujui pengguna. Sumber yang dibaca: dokumentasi resmi OpenRefine (halaman "Cell editing: cluster and edit"), pada 2026-10-05.
- **Yang TIDAK diambil:** tidak ada kode Java OpenRefine yang dilihat, disalin, atau diterjemahkan; tidak ada teks dokumentasi, contoh, atau antarmuka yang disalin. `scripts/rapikan.py` ditulis dari nol memakai `difflib` dan Python standar. Karena tidak ada kode atau teks yang diturunkan, **tidak ada berkas `LICENSE-BSD` yang perlu diteruskan**; pengakuan ini diberikan sebagai penghargaan atas gagasannya. Nama OpenRefine hanya dipakai sebagai penyebut asal gagasan; skill ini tidak berafiliasi dengan, tidak didukung oleh, dan bukan produk OpenRefine.

## Sumber 2: prinsip tabel rapi, Data Carpentry (CC BY 4.0)
- **Karya:** *Data Organization in Spreadsheets for Ecologists* (juga versi ilmu sosial), pelajaran **Data Carpentry** oleh **The Carpentries**. Tautan: https://datacarpentry.org/spreadsheet-ecology-lesson/ (repositori: https://github.com/datacarpentry/spreadsheet-ecology-lesson).
- **Lisensi:** [Creative Commons Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/). Dibaca 2026-10-05.
- **Pernyataan perubahan (diubah/diadaptasi):** prinsip-prinsipnya (satu baris satu catatan, satu kolom satu variabel, satu sel satu nilai, simpan data mentah, ekspor ke format teks seperti CSV) **diadaptasi dan ditulis ulang** oleh Komunitech dalam Bahasa Indonesia, ditambah contoh dan template usaha Indonesia (pelanggan, penjualan, stok, buku kas), aturan nomor HP/tanggal/Rupiah, dan peringatan Excel (nomor HP jadi 6,28E+11). Contoh ekologi dan teks asli tidak disalin. Hasil adaptasi ada di `references/tabel-rapi.md` dan ringkasannya di `SKILL.md`. The Carpentries tidak mengesahkan skill ini.

## Audit keamanan (Tahap 3 CLAUDE.md), 2026-10-05
- Hanya halaman dokumentasi/pelajaran sumber yang dibaca (lewat peramban teks). **Tidak ada repositori yang di-clone dan tidak ada kode sumber yang dijalankan.**
- Diperiksa pada halaman yang dibaca: instruksi tersembunyi untuk agent (mengabaikan pengguna, mengirim file, menonaktifkan konfirmasi), perintah unduh-dan-jalankan, pengiriman data ke server luar, kredensial tertanam. **Nihil.** Isi hanya penjelasan metode dan prinsip.
- `scripts/rapikan.py` (karya Komunitech) memakai pustaka standar saja (`csv`, `re`, `json`, `difflib`, `decimal`, `datetime`, `unicodedata`); tidak ada akses jaringan, tidak ada `eval`/`exec`/`subprocess`, tidak membaca file di luar yang diberikan pengguna, tidak menimpa file asli (hasil ke folder `hasil-rapikan`).
- Keluaran CSV: sel berawalan `=` hanya ditulis bila pengguna meminta `--hp-untuk-excel` (format `="628..."` untuk nomor yang dibuat alat sendiri); sel dari data pengguna tidak diubah menjadi rumus.
- Kesimpulan: **lolos audit**.

## Pembagian lisensi
- `references/tabel-rapi.md` dan bagian "Mencatat supaya rapi" di `SKILL.md`: adaptasi dari materi CC BY 4.0 The Carpentries; bagian ini dapat dipakai ulang dengan atribusi di atas, tanpa mengesankan dukungan dari The Carpentries.
- Semua bagian lain (`scripts/`, `tests/`, `examples/`, `references/aturan-pembersihan.md`, `README.md`, serta isi `SKILL.md` selebihnya): karya orisinal Komunitech. Data di `examples/data-contoh.csv` fiktif (nama dan nomor karangan; kemiripan dengan orang nyata kebetulan belaka).

Penggunaan keseluruhan tunduk pada `LISENSI.txt` yang disertakan dalam paket pembelian, kecuali bagian CC BY di atas.

## Riwayat versi
### v1.0.0 (2026-10-05), rilis awal (status `uji`), hasil kurasi ATM.
