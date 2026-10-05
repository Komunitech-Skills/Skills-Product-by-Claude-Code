# Catatan pembuat — resi-picking v1.0.0 → v1.0.1 (revisi atas temuan Akun B)

Ini catatan AGENT PEMBUAT (bukan penguji independen) untuk menindaklanjuti
`examples/HASIL-UJI.md` dan `examples/02-tiktok-tokopedia-gabung.md`. File tersebut TIDAK diubah.

## Akar masalah (dikonfirmasi ulang dari kode v1.0.0)
`deteksi_kolom` mencocokkan persis dulu (string ternormalisasi utuh, spasi/huruf besar-kecil saja
yang diabaikan), baru mencocokkan sebagian — tapi cocok sebagian hanya berlaku untuk kata sinonim
sepanjang **>= 8 huruf** dan dites dengan substring biasa (`k in h`). Sinonim seperti `"kurir"` (5
huruf) dan `"invoice"` (7 huruf) karena itu tidak pernah dicoba di jalur cocok-sebagian, sehingga
kolom seperti "Nama Kurir" atau "No. Invoice" gagal terdeteksi walau jelas secara manusiawi.

## Perbaikan
1. **Deteksi berbasis token kata, bukan potongan huruf, dan tanpa ambang panjang kata.**
   Fungsi baru `_token(s)` memecah nama kolom & sinonim jadi tuple token (huruf/angka saja, lower,
   diakritik dihapus via `unicodedata.normalize("NFKD", ...)` + buang combining marks, underscore
   dan tanda baca lain jadi pemisah token). `_token_sublist(kecil, besar)` mengecek token sinonim
   muncul UTUH & berurutan di token kolom. Tahap 1 (cocok persis = seluruh token sama) selalu
   dicoba lebih dulu untuk semua sinonim suatu field; tahap 2 (sublist) baru dicoba kalau tahap 1
   gagal. Ini menghilangkan aturan lama ">= 8 huruf" sekaligus membuat pencocokan
   case/diakritik/underscore/spasi-insensitive, TANPA membuka celah "potongan kata" (mis. "kurir"
   tidak akan salah cocok ke "kurirnya" karena token harus utuh, bukan substring).
2. **Sinonim diperluas** (lihat `references/sumber-kolom-marketplace.md` untuk status verifikasi
   tiap entri — resmi vs best-effort + sumber & tanggal cek):
   - TERVERIFIKASI (TikTok Shop, halaman resmi, dicek 2026-09-26): `SKU ID` → sku, `Order
     Substatus` → status.
   - BEST-EFFORT (ditandai jelas, belum ada konfirmasi halaman resmi): varian invoice/order id
     (`no. invoice`, `invoice number`, `order/adjustment id`), `nama barang`/`item name` → nama,
     `nama kurir`/`kurir pengiriman`/`logistik`/`shipping provider` → kurir, `buyer message`/`buyer
     remark` → catatan, `sku id`/`sku reference no` → sku (redundan dgn perbaikan #1 tapi menambah
     kejelasan), `substatus` tunggal → status.
   - Sengaja TIDAK ditambahkan: `Delivery Option` (TikTok resmi) ke field kurir — di dokumentasi
     resmi artinya opsi pengiriman (reguler/instan), bukan nama kurir; memetakannya berisiko
     menampilkan label salah di urutan resi walau secara teknis "match".
3. **Pesan error lebih actionable.** Saat kolom wajib tidak lengkap atau header sama sekali tidak
   dikenali, pesan sekarang SELALU menyebutkan (a) kolom yang SUDAH terdeteksi otomatis
   (`pemetaan_terdeteksi`), (b) semua nama kolom yang ada di file, dan (c) flag `--kolom-...` yang
   PERSIS perlu ditambahkan (bukan cuma satu contoh generik seperti di v1.0.0). SKILL.md langkah 5
   diperbarui: agent WAJIB menawarkan perintah `--kolom-...` dari pesan error, bukan cuma melapor
   gagal — menindaklanjuti rekomendasi eksplisit Akun B di `HASIL-UJI.md`.

## Verifikasi hasil terhadap fixture asli tester
Dijalankan ulang PERSIS fixture di `examples/02-tiktok-tokopedia-gabung.md`:
- File gaya TikTok Shop (9 kolom, header seperti temuan Akun B): **9/9 kolom terdeteksi otomatis**,
  tanpa satupun `--kolom-...` (sebelumnya 0 kolom wajib terdeteksi, perlu override no_pesanan+sku).
- File gaya Tokopedia (9 kolom): **9/9 kolom terdeteksi otomatis** (sebelumnya no_pesanan, nama,
  kurir gagal → 3 dari 9 perlu override).
- Angka hasil (qty per SKU, jumlah pesanan aktif) dicek manual, cocok dengan yang diharapkan dari
  data fixture — lihat assertion di `tests/uji_regresi.py::UjiHeaderMarketplaceAsli`.

## Pengujian
- `tests/uji_regresi.py`: 19 → **27 test** (+8: header Shopee resmi, Shopee
  underscore/kapital/diakritik, TikTok Shop realistis, Tokopedia realistis, Lazada best-effort,
  Blibli best-effort, 2 test pesan error actionable). Semua 27 lulus (`python3 -m unittest discover
  -s skills/resi-picking/tests -p '*.py'`).
- `python3 scripts/validate.py --skill resi-picking` ✅.
- `bash scripts/uji_openclaw.sh` ✅ eligible/modelVisible/commandVisible untuk resi-picking (skill
  lain yang gagal di uji ini — `vikunja-tugas` — dikerjakan agent lain secara paralel, di luar
  cakupan revisi ini).

## Belum diperbaiki / masih terbuka
- Temuan #2 (tanpa kemampuan gabung lintas marketplace) dan #3 (baris "Total" tanpa SKU aman) dari
  `HASIL-UJI.md` sengaja TIDAK diubah di v1.0.1 (di luar cakupan revisi ini per instruksi kerja);
  masih tercatat sebagai keterbatasan yang wajar untuk alat "sekali jalan" di SKILL.md.
- Nama kolom Shopee/Tokopedia/Lazada/Blibli TETAP berstatus "best-effort" walau sudah dicoba dicek
  ke beberapa halaman resmi (lihat `references/sumber-kolom-marketplace.md`) — halaman resmi yang
  ditemukan menjelaskan CARA ekspor tapi tidak mencantumkan nama kolom Excel/CSV persis. Rekomendasi
  tetap sama seperti v1.0.0: kirim contoh file ekspor asli (data pembeli disamarkan) untuk
  memastikan daftar sinonim, terutama sebelum naik ke status `lulus`.
- Status tetap `uji` (belum dinaikkan ke `lulus`) — perlu penguji independen (Akun B) menguji ulang
  v1.0.1 dan memberi skor baru, sesuai Tahap 6 alur kerja.
