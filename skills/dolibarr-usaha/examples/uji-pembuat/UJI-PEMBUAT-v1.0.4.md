# Catatan pembuat: dolibarr-usaha v1.0.4 (2026-09-25)

- **Penulis:** pembuat perbaikan (Claude Code, agent pembuat). Ini **bukan** uji independen dan tidak memberi skor kualitas. Status katalog: `uji`, menunggu uji ulang independen.
- **Lingkungan:** Linux, Python 3.11.15, server Dolibarr **tiruan** dari `tests/uji_regresi.py` (bentuk respons dari rekaman asli 24.0.1). Mode gangguan baru mensimulasikan putus dan timeout. Versi ini **tidak** diuji di Dolibarr asli.
- **Data uji (scratchpad sesi, di luar repo):** `c1/repro.py` (skrip reproduksi), `c1/repro-v1.0.3-keluaran.txt`, `c1/repro-v1.0.4-keluaran.txt`, `c1/tes-baru-pada-v1.0.3.txt`, serta salinan skrip v1.0.3 (`c1/v103/`) untuk membuktikan bahwa tes baru gagal pada versi lama.
- **Sumber temuan:** C1 di `08-uji-ulang-v1.0.3.md` §1c dan §5, serta bagian "Uji ulang v1.0.3 (Akun B)" di `HASIL-UJI.md`.

## C1: pembuatan draf belum idempoten saat timeout atau koneksi putus

### Reproduksi (v1.0.3, server tiruan)
Perintah yang dipakai: `invoice buat --pelanggan 2 --item "@KPI-250|3" --item "Gula Aren 1kg|2|32.500" --item "Ongkos kirim|1|12345" --ya`. Setiap skenario dijalankan dua kali: percobaan 1 dengan gangguan, percobaan 2 dengan koneksi normal dan perintah yang sama. Server tiruan **sudah memproses** permintaan sebelum koneksi putus atau jawabannya terlambat. Untuk skenario timeout, batas waktu script diturunkan ke 0,5 detik lewat pembungkus tanpa mengubah kode script.

| Gangguan | v1.0.3 percobaan 1 | v1.0.3 percobaan 2 | Draf pelanggan 2 setelahnya |
|---|---|---|---|
| Putus setelah `POST invoices` | kode 3, "tidak menjawab ... coba lagi" | kode 0 | `(PROV101)` Rp 0 (0 baris) **+** `(PROV102)` ❌ |
| Timeout `POST invoices` | kode 3 | kode 0 | yatim Rp 0 + draf kedua ❌ |
| Timeout baris 1 (baris sudah masuk) | **kode 0**, "baris 1 gagal ... berisi baris sebelumnya saja", penjelasan selisih sen, penutup "Validasi" | kode 0 | `(PROV101)` Rp 255.000 (1 baris) **+** `(PROV102)` ❌ |
| Putus saat baca ulang akhir | kode 3 "coba lagi" | kode 7 | 1 draf lengkap ✅ (sudah aman sejak v1.0.3) |

### Akar masalah
1. `Dolibarr.minta` memperlakukan timeout dan putus pada permintaan **tulis** sama seperti pada permintaan baca: kode 3 disertai saran "coba lagi". Padahal pada permintaan tulis, datanya mungkin sudah diproses Dolibarr.
2. Pencegah dobel (`draf_kembar`) hanya mengenali draf yang **jumlahnya sama**. Draf kosong Rp 0 atau draf sebagian dari percobaan yang terputus tidak cocok jumlahnya, sehingga pengulangan membuat draf baru.
3. `cmd_invoice_buat` menganggap setiap kegagalan baris sebagai "pasti tidak masuk". Draf sebagian tetap diberi kode 0 dan diproses dengan alur sukses: COCOK/BEDA, penjelasan selisih sen, dan ajakan "Validasi".

### Perbaikan (`scripts/dolibarr.py`)
- **Kode keluar baru 8 (`KELUAR_TIDAK_PASTI`):** koneksi putus atau timeout **saat menulis**, sehingga data mungkin sudah tersimpan (sebagian). Pada permintaan tulis, `minta` kini memunculkan `Gagal(..., mungkin_terkirim=True)` dengan pesan "Data ini MUNGKIN SUDAH TERSIMPAN" dan saran "JANGAN langsung mengulang ... periksa dulu". Koneksi ditolak dan nama host tidak dikenal berarti permintaan pasti belum terkirim, jadi tetap kode 3. Permintaan baca tidak berubah. Pesan ini juga berlaku untuk `pelanggan tambah`.
- **Kode perintah:** `kode_perintah()` menghasilkan sidik SHA-256 10 heksa dari isi perintah (pelanggan, tanggal, jatuh tempo, jenis PPN, catatan, item). Sidik ini disimpan di catatan privat draf: `... Periksa sebelum validasi. Kode perintah: xxxxxxxxxx`.
- **Cek sebelum membuat draf (`draf_tertinggal`):** selain draf kembar, draf pelanggan yang sama juga menahan pembuatan (kode 7) bila (a) **kosong** (`total_ht` 0, termasuk sisa v1.0.3 yang belum punya kode perintah), atau (b) berkode perintah **sama** tetapi jumlahnya belum sama (draf sebagian). Pesannya menyebut draf itu (ref, ID, isi Rp) beserta hal yang perlu dicek, dan `--tetap-buat` tetap tersedia.
- **`POST invoices` terputus (`_kepala_tidak_pasti`):** script membaca ulang daftar draf pelanggan dan mencari kode perintahnya. Bila ditemukan, keluarannya "draf (PROV101) SUDAH TERBUAT ..., tetapi masih KOSONG". Bila tidak ditemukan atau Dolibarr tidak bisa dihubungi, keluarannya menjelaskan bahwa status draf belum pasti. Kode 8, disertai langkah cek di menu Tagihan/Nota > Draf.
- **Baris gagal atau baca ulang gagal (`_draf_tidak_lengkap`):** kode 8. Judulnya "DRAF INVOICE TIDAK LENGKAP" atau "... TERSIMPAN, BELUM BISA DIPERIKSA". Pesan membedakan baris yang **DITOLAK** Dolibarr (pasti tidak masuk) dari baris yang **MUNGKIN sudah masuk** (timeout), menyebut baris yang belum dikirim, dan isi draf yang terbaca ulang (jumlah baris dan DPP dibanding yang seharusnya). Keluaran ini **tanpa** COCOK/BEDA, **tanpa** penjelasan selisih sen, **tanpa** "> Validasi", dan tanpa "coba lagi". Penutupnya: draf jangan disahkan sebelum dicek manusia. JSON memuat `lengkap: false`, `ok: false`, `kode_keluar: 8`, dan `draf_tertinggal`.
- Standar pembulatan **tidak berubah** (`hitung_invoice` tidak disentuh). Script tetap tidak punya perintah hapus, validasi, atau bayar. Draf yatim dihapus manusia di Dolibarr.

### Hasil setelah perbaikan (repro yang sama, `c1/repro-v1.0.4-keluaran.txt`)
| Gangguan | Percobaan 1 | Percobaan 2 | Draf pelanggan 2 setelahnya |
|---|---|---|---|
| Putus setelah `POST invoices` | kode **8**: "(PROV101) SUDAH TERBUAT ... masih KOSONG", "JANGAN mengulang" | kode **7** "draf belum lengkap ... kosong, Rp 0" | hanya `(PROV101)` ✅ |
| Timeout `POST invoices` | kode 8 | kode 7 | hanya `(PROV101)` ✅ |
| Timeout baris 1 | kode 8 "TIDAK LENGKAP", "Baris 1 ... MUNGKIN sudah masuk", "Baris 2 s.d. 3 belum dikirim", "1 baris, DPP Rp 255.000 (seharusnya 3 baris ...)" | kode 7 "dari perintah yang sama tetapi belum lengkap" | hanya `(PROV101)` ✅ |
| Putus saat baca ulang akhir | kode 8 "Semua 3 baris sudah diterima ... JANGAN mengulang" | kode 7 (kembar) | 1 draf ✅ |

## Tes regresi (`tests/uji_regresi.py`)
Server tiruan kini punya mode `putus:<titik>` (sudah diproses, koneksi ditutup tanpa jawaban) dan `lambat:<titik>` (sudah diproses, jawaban ditunda 1,5 detik). Titik yang tersedia: `post_invoice`, `baris<N>`, `get_invoice`, `post_pelanggan`. Helper `jalan(..., batas_waktu=0.5)` menurunkan `BATAS_WAKTU` lewat pembungkus.

| Tes baru | Isi |
|---|---|
| `test_c1_putus_setelah_draf_dibuat` | Repro C1-a: kode 8 "KOSONG"; ulangan kode 7 tanpa POST; `--tetap-buat` membuat `(PROV102)` |
| `test_c1_timeout_post_invoice_json` | Timeout asli (0,5 detik): JSON `ok:false`, `kode_keluar:8`, `lengkap:false`, `draf_tertinggal=[(PROV101)]`; ulangan kode 7 |
| `test_c1_timeout_baris_pertama_draf_sebagian` | Repro C1-b: kode 8, "MUNGKIN sudah masuk", "1 baris", tanpa "Validasi"/"COCOK"/selisih sen/"coba lagi"; ulangan kode 7; perintah dengan item lain tetap dibuat |
| `test_c1_putus_di_baris_terakhir_dan_baca_ulang` | Baca ulang akhir putus: kode 8 "Semua 3 baris sudah diterima"; ulangan kode 7. Baris terakhir putus: tanpa "belum dikirim" |
| `test_c1_draf_kosong_lama_tanpa_kode_perintah` | Draf kosong sisa v1.0.3 (tanpa kode perintah) menahan pelanggan yang sama dan tidak menahan pelanggan lain |
| `test_c1_kode_perintah_di_catatan` | Kode perintah ada di catatan privat, stabil untuk perintah sama, berbeda untuk item berbeda |
| `test_c1_pelanggan_tambah_putus_mungkin_tersimpan` | `pelanggan tambah` putus: kode 8 "MUNGKIN SUDAH TERSIMPAN", tanpa "coba lagi" |
| `test_c1_dolibarr_mati_saat_tulis_tetap_kode_3` | Penjaga: koneksi ditolak tetap kode 3, bukan 8 |

Tes lama yang diubah: `test_invoice_baris_gagal_dilaporkan_tanpa_hapus` (baris 2 ditolak HTTP 400). Harapannya kini kode **8** (sebelumnya 0), "Baris 2 (Gula Aren 1kg) DITOLAK Dolibarr", "Baris 3 belum dikirim", dan tanpa penutup sukses.

- Pada skrip **v1.0.3**: 8 dari 9 tes C1 gagal (`c1/tes-baru-pada-v1.0.3.txt`). Yang lolos hanya penjaga kode 3.
- Pada **v1.0.4**: `python3 tests/uji_regresi.py` menghasilkan **85 tes OK** (77 lama + 8 baru).
- `python3 scripts/validate.py` menghasilkan **68 skill valid, 68 baris katalog sesuai**.

## Dokumentasi
- `SKILL.md`: versi 1.0.4, dua penjelasan baru di bagian C (draf belum lengkap, kode 8), dua baris baru di tabel galat, dan pembaruan catatan "gagal di tengah".
- `README.md`: status uji 1.0.4 ditulis jujur (baru diuji pembuat di server tiruan).
- `scripts/dolibarr.py`: `VERSI_SKRIP = "1.0.4"`, docstring kode keluar 8.

## Belum dilakukan / untuk penguji independen
- Belum diuji di **Dolibarr asli**. Perlu dipastikan hal berikut:
  - `GET invoices?status=draft&properties=...,note_private` mengembalikan `note_private`. Rekaman 24.0.1 memuatnya, tetapi belum dicek pada user API berhak terbatas.
  - Perilaku timeout nyata DoliWamp sama dengan simulasinya.
- Draf kosong yang dibuat **manual** oleh pengguna untuk pelanggan yang sama juga menahan pembuatan (kode 7, bisa dilewati dengan `--tetap-buat`). Ini sengaja dibuat konservatif.
- Kode perintah memuat tanggal. Pengulangan pada hari lain dengan tanggal default (hari ini) tidak mengenali draf **sebagian**, tetapi draf **kosong** tetap dikenali.
- Kosmetik K-a s.d. K-d dari `08-uji-ulang-v1.0.3.md` belum ditangani (di luar cakupan tugas ini).
