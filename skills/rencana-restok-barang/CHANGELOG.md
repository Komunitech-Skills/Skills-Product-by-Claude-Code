# Riwayat perubahan — rencana-restok-barang

Catatan teknis per versi (ringkasan pembeli ada di README).

## 1.0.2 (2026-10-14)
Perbaikan kecil dari uji ulang 1.0.1 (6,1 → 8,7, LULUS; skenario 1: 180 dari 182 angka cocok). Alur tidak berubah.
- **Presisi hari habis:** laju yang tidak kena batas kini dipakai langsung (laju 4 minggu terakhir), bukan rata-rata × (laju baru ÷ rata-rata); semua pembulatan ke atas/bawah dirapikan dulu ke 12 desimal. Contoh: stok 260 dengan laju 52/28 kini tepat 140 hari (sebelumnya 139,999… → 139).
- **Kalimat batas tren:** `kalimat_tren` menyebut "dibatasi" hanya bila batas 0,5–2× benar-benar terpakai; selain itu "(tidak kena batas)". SKILL.md: batas disebut hanya bila `tren_dibatasi` benar; contoh yang menyesatkan diganti.
- **Hari habis dengan laju dibatasi:** bila laju dibatasi, hasil menyertakan `habis_dalam_hari_laju_terbaru` dan teks "(laju dibatasi; dengan laju 4 minggu terakhir …: ±X hari)"; penanda akan kosong memakai yang lebih cepat habis.
- **SKILL.md:** lokasi script ditulis di aturan kerja (folder yang sama dengan SKILL.md + jalur umum per platform); larangan mencari file di luar folder skill/data pengguna, membaca kode script, dan membuka `examples/`; simbol "μ" diganti kata biasa.
- Script: opsi `--contoh` (ringkasan cara pakai); ringkasan tidak lagi menulis "modal tertahan Rp0" bila tidak ada barang mati.
- Uji regresi: 149 cek (10 cek baru, termasuk kasus tepat kelipatan 260 ÷ 52/28 = 140 yang gagal di cara lama).

## 1.0.1 (2026-10-14)
Revisi dari uji OpenClaw penguji independen (versi 1.0.0: 6,1 → 8,3, LULUS); lima temuan diperbaiki:
- **Akan kosong sebelum barang datang:** script menghitung `akan_kosong_hari` = ⌈lead time − stok ÷ laku/hari⌉ untuk semua barang yang stoknya diketahui, termasuk barang "data belum cukup" (memakai laju sementara). Daftar `akan_kosong_sebelum_barang_datang` + jumlahnya di ringkasan, dengan saran (pesan hari ini / pesanan kecil untuk barang data pendek, pemasok lebih cepat, atau terima kosong ±X hari). Ditulis paling atas di balasan.
- **Tren:** dideteksi dari laju 4 minggu terakhir vs sampai 8 minggu sebelumnya (bukan vs rata-rata seluruh data yang ikut memuat minggu terakhir), ambang ±20 % tetap. Laju yang dipakai = laju 4 minggu terakhir, dibatasi 0,5–2,0× rata-rata seluruh data (sebelumnya 0,5–1,5×); batas yang terpakai disebut terbuka. `kalimat_tren` per barang + catatan tren per barang; SKILL.md melarang menulis "stabil/tidak tajam" untuk barang naik/turun. Contoh: minyak goreng 130 → 165 per 4 minggu kini "naik 27 %" (sebelumnya "stabil").
- **Pencocokan nama:** huruf besar/kecil, tanda kurung, tanda baca, dan spasi diabaikan ("(isi 3)" = "isi 3"); SKU tanpa tanda baca/spasi. Nama yang hanya mirip masuk kelompok baru MUNGKIN BARANG YANG SAMA dan ditanyakan, tidak lagi dicatat sebagai barang mati.
- **Lonjakan:** aturan baru (> rata-rata + 3 simpangan, ≥ 4× dan ≥ 8 di atas median hari laku); hasil tanpa lonjakan dihitung sebagai pembanding (`tanpa_lonjakan`), catatan menyebut bila tren naik terjadi karena lonjakan, pertanyaan "promo atau borongan sekali?" dengan dua hasil.
- **Hitungan manual (tanpa Python):** wajib menampilkan baris rumus dengan angka terisi untuk maksimal 5 barang, asumsi simpangan disebut, pembulatan ke atas.
- Lain-lain: `--lead-time` dari pengguna dilabeli "lead time umum dari pengguna" (tidak ditanya ulang); satuan diambil dari nama bila tertulis dalam kurung, mis. "(karung)"; tabel lebar baris = minggu/tanggal dan kolom = barang terbaca langsung; ringkasan tanpa harga menampilkan `[isian]`, bukan Rp0; catatan "7 hari terakhir lebih ramai" bila ≥ 20 % dan ≥ 5 unit di atas rata-rata.
- Uji regresi: 139 cek (26 cek baru untuk butir di atas).

## 1.0.0 (2026-10-14)
- Rilis awal. Script `rencana_restok.py` (Decimal, pustaka standar): membaca CSV/TSV/tabel markdown/XLSX/JSON, ekspor marketplace (baris judul dicari, status batal/belum bayar/retur dilewati, baris dobel per nomor pesanan), ekspor mutasi dan laporan stok buku-stok, tabel lebar per tanggal, data per minggu/bulan; tanggal campur format termasuk nomor seri Excel dan file bergaya bulan/tanggal.
- Hitungan: rata-rata dan simpangan harian, tren 4 minggu (dibatasi 0,5–1,5×), faktor musim dari pengguna, stok pengaman z × sd × √lead time, titik pesan ulang, stok target (lead time + horizon), kelompok PESAN SEKARANG / MINGGU DEPAN / AMAN, pembulatan ke minimal order dan isi per dus, nilai pesanan, pesanan per pemasok + draf WA, minimal belanja pemasok, catatan stok minus dan barang di daftar yang tidak ada di data penjualan, barang mati (≥ 60 hari), stok berlebih (> 90 hari), data belum cukup (< 14 hari), lonjakan (ditandai, bisa diabaikan atas persetujuan pengguna), pertanyaan usulan maksimal 3.
- 113 cek uji regresi dengan angka pembanding dihitung terpisah.
