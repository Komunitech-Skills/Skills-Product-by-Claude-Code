# Skenario 02 — Toko TikTok Shop + Tokopedia digabung (normal, tapi ketemu batas nyata)

Data rekaan: 1 file ekspor gaya TikTok Shop (pemisah `;`, header bahasa Inggris seperti asli
TikTok Shop, 5 pesanan) + 1 file ekspor gaya Tokopedia (koma, header bahasa Indonesia umum,
4 pesanan). Skill hanya menerima satu file per jalan — pengguna dengan 2 kanal harus menjalankan
skrip **dua kali** (sekali per file) lalu gabung hasilnya sendiri. Ini wajar untuk skill "sekali
jalan tanpa database", tapi perlu disebut ke pembeli di jawaban chat, bukan cuma di dokumentasi.

## File TikTok Shop (pemisah `;`)
Header asli: `Order/adjustment ID;SKU Reference No.;Nama Produk;Nama Variasi;Quantity;
Shipping Provider Name;Tracking ID;Order Substatus;Buyer Message`

- **Auto-deteksi kolom pertama (tanpa override): GAGAL.** Kolom "No. pesanan" dan "SKU" tidak
  terdeteksi karena `Order/adjustment ID` dan `SKU Reference No.` tidak ada di daftar sinonim
  (`SINONIM_PESANAN`) — sesuai peringatan "PERLU REVIEW" yang sudah ditulis sendiri di SKILL.md.
  Error yang dikembalikan sudah jelas dan menyertakan `kolom_ada` + `pemetaan_terdeteksi` parsial,
  sehingga pengguna/agent bisa langsung tahu kolom mana yang perlu di-override.
- Dengan override manual:
  ```
  python3 scripts/resi.py in_tiktok_tokped.csv --pemisah ";" \
    --kolom-no-pesanan "Order/adjustment ID" --kolom-sku "SKU Reference No." \
    --kolom-status "Order Substatus" --kolom-catatan "Buyer Message" --json
  ```
  Hasil: `ok: true`, 5 pesanan total, 4 aktif (1 batal), total barang 7 pcs, kurir JNE 2 / J&T 1 /
  SPX Express 1. **Diverifikasi manual dari CSV: cocok persis** (TT-88004 berisi 2 baris/SKU dalam
  1 pesanan — dihitung sebagai 1 pesanan, qty digabung per SKU, sesuai perilaku yang diklaim).

## File Tokopedia (header umum, koma)
Header: `No. Invoice,Kode SKU,Nama Barang,Varian,Jumlah Produk Dibeli,Nama Kurir,No Resi,
Status Terakhir,Catatan Pembeli`

- Auto-deteksi juga **gagal sebagian**: "No. Invoice" tidak match sinonim (`invoice`/`nomor invoice`
  ada di daftar, tapi kolomnya "No. Invoice" — lihat akar masalah di bawah), begitu juga
  "Nama Barang" (bukan "nama produk") dan "Nama Kurir" (bukan "opsi pengiriman"/"kurir" polos).
- Dengan override manual (`--kolom-no-pesanan "No. Invoice" --kolom-nama "Nama Barang"
  --kolom-kurir "Nama Kurir"`): `ok: true`, 4 pesanan aktif, total 9 pcs, kurir sesuai file.
  Diverifikasi manual — cocok persis.

## Akar masalah teknis (untuk dicatat, BUKAN untuk diperbaiki oleh penguji)
Fungsi `deteksi_kolom` di `scripts/resi.py` mencocokkan **persis** dulu, baru mencocokkan
**sebagian** — tapi pencocokan sebagian hanya dipakai untuk kata kunci sinonim yang panjangnya
**≥ 8 huruf**. Sinonim seperti `"kurir"` (5 huruf) dan `"invoice"` (7 huruf) karena itu **tidak
pernah** dicocokkan sebagian, sehingga kolom "Nama Kurir" atau "No. Invoice" (varian umum di
ekspor Indonesia) gagal terdeteksi otomatis meski kelihatan jelas secara manusiawi. Ini bukan bug
yang membuat hasil salah (script menolak dengan jujur, tidak menerka), tapi mengurangi klaim
"instan tanpa setup" untuk 2 dari 2 file uji di skenario ini — keduanya perlu override manual.

## Kesimpulan skenario 02
Tidak ada data yang salah dihitung (semua kasus yang lolos, angkanya 100% cocok). Tapi tingkat
keberhasilan auto-deteksi kolom pada 2 contoh header TikTok Shop/Tokopedia yang realistis di uji
ini adalah **0 dari 2** tanpa override — jauh dari klaim "instan, cukup satu kalimat". Sudah ada
jalan keluar (pesan error jelas + flag `--kolom-...`), tapi agent yang memakai skill WAJIB
membaca `pemetaan_kolom`/error dan tahu cara menawarkan override, bukan hanya lapor gagal.

## Penyegaran v1.0.5 (2026-10-17)
> Hasil dan skor uji asli di atas **tidak diubah**. File input skenario ini tidak disimpan di repo, jadi skrip tidak dijalankan ulang. Sejak v1.0.5 setiap jalan (satu per file) wajib menampilkan "Pesanan di file", "Dilewati:" dengan nomor pesanan, dan "Stok setelah dikemas" (tanpa file stok: "Stok tidak dicek (tidak ada file stok)."); di kanal chat tanpa jalur berkas dan tanpa tabel lebar. Keterbatasan satu file per jalan (gabung dua kanal manual) tidak berubah dan tetap perlu disebut ke pengguna.
