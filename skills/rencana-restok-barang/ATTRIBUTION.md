# Atribusi

## Jalur produksi
**Kreasi orisinal Komunitech.** Alur kerja, rumus dan aturan pengelompokan, script `scripts/rencana_restok.py`, uji regresi `tests/uji_regresi.py`, template, referensi, dan README ditulis sendiri oleh Komunitech untuk pasar Indonesia (Rupiah, ekspor kasir dan marketplace lokal, ekspor skill Buku Stok, pemasok via WhatsApp, isi per dus dan minimal order, musim belanja Indonesia).

## Asal ide
Ide kebutuhan "perencana restok" tercatat dalam kurasi Komunitech atas repositori publik [anthropics/knowledge-work-plugins](https://github.com/anthropics/knowledge-work-plugins) (pembuat: Anthropic, lisensi Apache-2.0), yang memuat skill bertema perencanaan persediaan untuk usaha kecil. Catatan kurasi itu hanya berisi ringkasan fitur. **Pembuat skill ini tidak membaca dan tidak menyalin teks, contoh, template, atau kode skill sumber**; seluruh isi ditulis dari pengetahuan umum manajemen persediaan (rata-rata permintaan, stok pengaman, titik pesan ulang) dan riset repo Komunitech sendiri. Karena tidak ada materi Apache-2.0 yang disalin, tidak ada berkas lisensi pihak ketiga yang perlu disertakan; asal ide dicatat demi keterbukaan. Anthropic tidak berafiliasi dengan dan tidak mengesahkan produk Komunitech ini.

## Audit keamanan (pedoman kurasi Komunitech)
`scripts/rencana_restok.py` hanya memakai pustaka standar Python (`argparse`, `csv`, `io`, `json`, `re`, `sys`, `calendar`, `datetime`, `decimal`, dan `zipfile` + `xml.etree.ElementTree` untuk membaca .xlsx). Hanya membaca file yang diberikan pengguna; tidak menulis file apa pun; tidak ada akses jaringan, `eval`/`exec`/`subprocess`, atau pembacaan kredensial. Tes memakai folder sementara sistem.

## Data contoh
Semua nama barang, pemasok, toko, kode, angka, dan tanggal di `templates/`, `references/`, dan `tests/` fiktif. Nama marketplace dan aplikasi hanya disebut sebagai contoh sumber data, tidak berafiliasi.

## Lisensi
Penggunaan tunduk pada `LISENSI.txt` yang disertakan dalam paket pembelian.

## Riwayat versi
- 1.0.0 (2026-10-14): rilis awal; diuji penguji independen di OpenClaw (6,1 → 8,3).
- 1.0.1 (2026-10-14): perbaikan lima temuan uji; uji ulang terbatas 6,1 → 8,7.
- 1.0.2 (2026-10-14): perbaikan presisi hari habis dan kalimat batas tren (lihat `CHANGELOG.md`).
- 1.0.3 (2026-10-14): judul kelompok waktu nyata, rumus per barang, draf WA wajib (lihat `CHANGELOG.md`).
- 1.0.4 (2026-10-14): deteksi otomatis data per hari/minggu/bulan (lihat `CHANGELOG.md`).
