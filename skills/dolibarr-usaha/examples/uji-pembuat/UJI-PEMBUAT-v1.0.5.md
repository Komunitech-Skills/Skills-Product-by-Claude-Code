# Catatan pembuat: dolibarr-usaha v1.0.5 (2026-09-25)

- **Penulis:** pembuat perbaikan (Claude Code, agent pembuat). Ini **bukan** uji independen dan tidak memberi skor kualitas. Status katalog: `uji`, menunggu uji ulang independen.
- **Lingkungan:** Linux, Python 3.11, server Dolibarr **tiruan** dari `tests/uji_regresi.py` (bentuk respons dari rekaman asli 24.0.1). Versi ini **tidak** diuji di Dolibarr asli.
- **Data uji (scratchpad sesi, di luar repo):** `d15/repro.py` (skrip reproduksi), `d15/repro-v1.0.4-keluaran.txt`, `d15/repro-v1.0.5-keluaran.txt`, `d15/tes-baru-pada-v1.0.4.txt`, serta salinan skrip v1.0.4 (`d15/v104/`) untuk membuktikan bahwa tes baru gagal pada versi lama.
- **Sumber temuan:** D1–D3 di `09-uji-ulang-v1.0.4.md` §4 dan bagian "Uji ulang v1.0.4 (Akun B)" di `HASIL-UJI.md`.

## Gangguan baru di server tiruan
| Mode | Arti |
|---|---|
| `galat:<kode>:<titik>` | Server **sudah memproses**, lalu membalas 5xx. Kode 500 dibalas JSON galat Dolibarr, sedangkan 502/503/504 dibalas halaman HTML proxy. |
| `tolak:<kode>:<titik>` | Kontrol negatif: server membalas 5xx **tanpa memproses** apa pun. |
| `sebagian:<titik>` | Sudah diproses, `Content-Length: 64` tetapi hanya 2 bita yang dikirim, sehingga klien mendapat `IncompleteRead`. |

Titik yang tersedia sama dengan v1.0.4: `post_invoice`, `baris<N>`, `get_invoice`, `post_pelanggan`.

## Reproduksi pada v1.0.4
Perintah A: pelanggan 2, `@KPI-250|3`, `Gula Aren 1kg|2|32.500`, `Ongkos kirim|1|12345`, `--tanggal 2026-09-24 --ya`. Percobaan 1 dijalankan dengan gangguan, lalu perintah yang sama diulang tanpa gangguan.

| Temuan | Gangguan | v1.0.4 percobaan 1 | Ulangan |
|---|---|---|---|
| D1 | `galat:500/502/504:post_invoice` (draf sudah terbuat) | kode **6** "Dolibarr mengembalikan galat 504: 504 Gateway Time-out504 Gateway Time-out", tanpa "mungkin tersimpan" | kode 7, draf tetap 1 |
| D1 | `galat:504:baris2` (baris sudah masuk) | kode 8, tetapi "Baris 2 ... **DITOLAK** Dolibarr ...; baris ini **tidak masuk**", padahal isi terbaca ulang 2 baris | kode 7 |
| D1 | `galat:504:post_pelanggan` | kode **6** generik | – |
| D2 | `sebagian:post_invoice`, `sebagian:baris2`, `sebagian:post_pelanggan` | kode **6** "Galat tak terduga (IncompleteRead) ... jalankan `cek`" | kode 7 |
| D3 | Perintah B (paku + kuas) terputus di `post_invoice`, lalu perintah A | kode **7**, "lengkapi barisnya sesuai pratinjau di atas" (pratinjau milik A, draf milik B) | – |
| D3 | Draf kosong tanpa kode perintah, lalu perintah A | kode 7 dengan kalimat yang sama | – |

Semua temuan penguji tereproduksi. Satu hal tambahan: judul halaman galat proxy tercetak dua kali ("504 Gateway Time-out504 Gateway Time-out") karena isi `<title>` dan `<h1>` digabung.

## Akar masalah
1. `Dolibarr.minta` hanya menganggap `URLError`/`OSError` pada permintaan tulis sebagai "mungkin terkirim". Balasan HTTP 5xx diteruskan ke `_olah` dan menjadi `Gagal` kode 6 dengan `mungkin_terkirim=False`. Akibatnya `_draf_tidak_lengkap` menyebut baris tersebut DITOLAK.
2. `http.client.IncompleteRead` muncul saat `r.read()`. Galat ini bukan turunan `OSError`, jadi tidak tertangkap dan jatuh ke `except Exception` di `main`.
3. `draf_tertinggal` menahan **semua** draf kosong milik pelanggan tanpa melihat kode perintahnya, dan pesannya memakai satu kalimat umum untuk semua jenis draf.

## Perbaikan (`scripts/dolibarr.py`)
- **D1:** pada permintaan **tulis** (`metode != "GET"`), balasan 500–599 masuk jalur `_gagal_tulis`: kode 8, "MUNGKIN SUDAH TERSIMPAN", `mungkin_terkirim=True`. Pengecualiannya 501 (modul mati) dan 503 "not allowed from your IP" (blokir IP). Keduanya ditolak sebelum diproses, jadi tetap diperlakukan sebagai pasti gagal. Galat 4xx tidak berubah: tetap "DITOLAK ... tidak masuk" atau kode 5 untuk 401/403. Permintaan **baca** yang menerima 5xx juga tidak berubah.
  - Pesan 5xx: "Dolibarr (atau server perantaranya) membalas galat 504: 504 Gateway Time-out SAAT MENGIRIM data. Galat server seperti ini bisa terjadi SETELAH data diproses. Data ini MUNGKIN SUDAH TERSIMPAN di Dolibarr."
  - `_teks_polos()` baru membuang `<head>`, `<script>`, dan `<style>`, lalu merapikan spasi, sehingga judul halaman tidak tercetak dua kali. Fungsi ini juga dipakai `_olah`.
- **D2:** `http.client.HTTPException` (`IncompleteRead`, `BadStatusLine`) kini ditangkap. Pada permintaan tulis hasilnya kode 8 "Jawaban Dolibarr terpotong/rusak SAAT MENGIRIM data (IncompleteRead). Data ini MUNGKIN SUDAH TERSIMPAN". Pada permintaan baca hasilnya kode 3 "Jawaban Dolibarr terpotong/rusak". Klausul ini sengaja diletakkan **setelah** `OSError`, karena `RemoteDisconnected` adalah turunan `OSError` sekaligus `HTTPException` dan harus tetap dilaporkan sebagai "Koneksi ... putus". Isi halaman galat yang ikut terpotong (`e.read()` pada `HTTPError`) juga ditangani.
- **Laporan per baris (D1/D2):** kalimat "Dolibarr tidak menjawab" diganti sebab yang sebenarnya ("Dolibarr membalas galat 504" atau "jawaban Dolibarr terpotong/rusak"). Setelah itu script menyimpulkan dari isi draf yang dibaca ulang: "Menurut isi draf yang dibaca ulang, baris 2 SUDAH masuk / BELUM masuk". Kesimpulan ini sah karena draf baru dibuat oleh script sendiri. JSON memuat `baris_masuk: true/false`.
- **`_kepala_tidak_pasti`:** bila draf tidak ditemukan saat dicek ulang, teksnya kini "belum ada draf baru dari perintah ini ... Bisa jadi permintaan tadi memang tidak diproses, atau Dolibarr masih memprosesnya". Kalimat ini jujur untuk 5xx yang memang menolak.
- **D3:** `draf_tertinggal` membedakan empat keadaan:

  | Keadaan | Contoh | Perilaku |
  |---|---|---|
  | `kosong` | Rp 0, kode perintah **sama** | Menahan. Tindakan: "Hapus draf kosong (PROV101) (ID 101), lalu jalankan ulang perintah ini." |
  | `sebagian` | sudah ada baris, kode perintah **sama** | Menahan. Tindakan: "Buka draf ..., cocokkan dengan pratinjau di atas lalu tambahkan baris yang kurang, ATAU hapus ..." |
  | `kosong_tanpa_kode` | Rp 0 tanpa kode perintah (sisa v1.0.3 atau dibuat manual) | Menahan. Tindakan: "Buka draf kosong (PROV95) (ID 95). Jika memang tidak dipakai, hapus, lalu jalankan ulang perintah ini." |
  | `kosong_lain` | Rp 0, kode perintah **lain** | **Tidak menahan.** Hanya `CATATAN: pelanggan ini juga punya draf KOSONG (Rp 0) sisa perintah LAIN ...: (PROV101) (ID 101) ... hapus di Dolibarr`. JSON memuat `draf_kosong_lain`. |

  Kalimat "lengkapi barisnya sesuai pratinjau di atas" dihapus. Setiap draf kini diberi tindakan sendiri sesuai jenisnya.

### Alasan pilihan D3 (risiko tagihan ganda)
- Draf **kosong** tidak bisa menagih siapa pun. Tagihan baru terjadi bila manusia mengisi barisnya dan menekan Validasi. Jadi membiarkan draf kosong milik perintah **lain** tidak menambah risiko dobel.
- Perintah pemilik draf kosong itu **tetap ditahan** olehnya, karena kode perintahnya sama. Contoh: B yang terputus lalu diulang tetap mendapat kode 7 dan tidak mendapat draf kedua.
- Bahaya justru ada pada perilaku lama. Pesan lama menyuruh "lengkapi sesuai pratinjau di atas", sehingga orang awam bisa mengisi draf milik B dengan barang milik A. Setelah itu, perintah A yang dijalankan lagi (atau `--tetap-buat`) bisa menghasilkan dua tagihan A.
- Draf kosong **tanpa** kode perintah tetap menahan, karena asalnya tidak bisa dipastikan. Draf itu bisa berasal dari perintah yang sama di v1.0.3, atau sedang diisi manual oleh pengguna untuk transaksi yang sama. Pilihan yang lebih aman di sini adalah bertanya dulu.
- Draf **sebagian** (sudah ada baris) milik perintah lain sudah tidak menahan sejak v1.0.4. Aturan ini tidak diubah.

## Hasil setelah perbaikan (repro yang sama, `repro-v1.0.5-keluaran.txt`)
| Gangguan | Percobaan 1 | Ulangan | POST pada ulangan | Draf pelanggan 2 |
|---|---|---|---|---|
| `galat:500/502/504:post_invoice` | **8** "MUNGKIN SUDAH TERSIMPAN", "(PROV101) (ID 101) SUDAH TERBUAT ... KOSONG", "JANGAN mengulang" | 7, tindakan "Hapus draf kosong (PROV101)" | 0 | 1 |
| `sebagian:post_invoice` | **8** "terpotong/rusak ... (IncompleteRead) ... MUNGKIN SUDAH TERSIMPAN" | 7 | 0 | 1 |
| `galat:504:baris2` | 8, "Dolibarr membalas galat 504. Baris ini MUNGKIN sudah masuk", "baris 2 **SUDAH** masuk", tanpa "DITOLAK" | 7 | 0 | 1 (2 baris) |
| `sebagian:baris2` | 8, "jawaban Dolibarr terpotong/rusak ... MUNGKIN sudah masuk", "baris 2 SUDAH masuk" | 7 | 0 | 1 |
| `tolak:504:baris2` (kontrol) | 8, "baris 2 **BELUM** masuk", "1 baris" | 7 | 0 | 1 (1 baris) |
| `tolak:500:post_invoice` (kontrol) | 8, "belum ada draf baru dari perintah ini" | **0** (dibuat) | 4 | 1 lengkap |
| `pelanggan tambah` 504 / terpotong | **8** "MUNGKIN SUDAH TERSIMPAN", tanpa "coba lagi" | – | – | – |
| D3: B terputus, lalu A | A: **0**, dibuat `(PROV102)` + CATATAN tentang `(PROV101)` | B diulang: **7** "Hapus draf kosong (PROV101)" | 0 | `(PROV101)` kosong + `(PROV102)` lengkap |
| D3b: draf kosong tanpa kode, lalu A | **7**, "tanpa kode perintah ..., asalnya tidak bisa dipastikan", "Buka draf kosong (PROV95)" | – | – | – |

## Tes regresi (`tests/uji_regresi.py`)
| Tes baru | Isi |
|---|---|
| `test_d1_5xx_saat_post_invoice_mungkin_tersimpan` | 500/502/503/504 setelah draf terbuat: kode 8, "MUNGKIN SUDAH TERSIMPAN", draf disebut. Ulangan kode 7, 0 POST, tetap 1 draf |
| `test_d1_5xx_saat_baris_tidak_disebut_ditolak` | 504 di baris 2 (sudah masuk): tanpa "DITOLAK"/"tidak masuk", ada "SUDAH masuk", JSON `baris_masuk: true`. Kontrol `tolak:504`: "BELUM masuk". Ulangan kode 7 |
| `test_d1_5xx_kontrol_negatif_tidak_tersimpan` | 500 tanpa diproses: kode 8 jujur, ulangan membuat draf (kode 0) |
| `test_d1_4xx_dan_bukan_tulis_tidak_berubah` | `_5xx_tidak_pasti`: 5xx benar, 4xx/501/503-blokir-IP salah. 403 saat tulis tetap kode 5. 502 pada baca ulang akhir tidak berlabel "MUNGKIN SUDAH TERSIMPAN" |
| `test_d1_pelanggan_tambah_504` | kode 8, judul tidak dobel, tanpa "coba lagi". Ulangan kode 7 (nama/HP sama) |
| `test_d2_jawaban_terpotong_saat_menulis` | IncompleteRead di `post_invoice`, `baris2`, `post_pelanggan`: kode 8, tanpa "Galat tak terduga"/Traceback. Terpotong saat baca ulang: pesan koneksi biasa. `RemoteDisconnected` tetap "Koneksi ... putus" |
| `test_d3_draf_kosong_perintah_lain_hanya_catatan` | Draf kosong B tidak menahan A (kode 0, `draf_kosong_lain`, CATATAN). B diulang tetap kode 7 dengan "Hapus draf kosong (PROV101)", tanpa "lengkapi barisnya sesuai pratinjau" |
| `test_d3_draf_kosong_tanpa_kode_tetap_menahan_dengan_pesan_jelas` | Draf kosong tanpa kode perintah: kode 7, pesan menyebut draf dan tindakannya, 0 tulis |

- Pada skrip **v1.0.4** (`tes-baru-pada-v1.0.4.txt`), **ke-8 tes baru gagal** (13 kegagalan subtes dan 1 error). Ke-85 tes lama tetap lolos dengan server tiruan yang diperluas.
- Pada **v1.0.5**, `python3 tests/uji_regresi.py` menghasilkan **93 tes OK** (85 lama + 8 baru). Tidak ada tes lama yang diubah.
- `python3 scripts/validate.py`: **68 skill valid, 68 baris katalog sesuai**.
- **Pembulatan tidak berubah:** `hitung_invoice`, `dpp_cara_dolibarr`, dan `draf_kembar` tidak disentuh. Tes angka B1 lama tetap lolos.

## Dokumentasi
- `SKILL.md`: versi 1.0.5, bagian C (draf tertinggal per jenis, CATATAN draf kosong perintah lain, kode 8 mencakup 5xx dan jawaban terpotong), tabel galat (baris 7, baris baru "0 + CATATAN", baris 8), dan catatan "gagal di tengah".
- `README.md`: status uji 1.0.5 ditulis jujur (baru diuji pembuat di server tiruan).
- `scripts/dolibarr.py`: `VERSI_SKRIP = "1.0.5"`, docstring kode keluar 8.

## Belum dilakukan / untuk penguji independen
- Belum diuji di **Dolibarr asli**. Perlu dipastikan bahwa DoliWamp/Apache asli benar-benar mengirim 500/502/504 pada kasus nyata (mis. PHP `max_execution_time`, proxy di VPS). Bentuk halaman galatnya juga perlu dicek, dan dipastikan tidak ada 5xx lain yang sebenarnya "pasti ditolak".
- Balasan 500 dari Dolibarr bisa berupa kegagalan yang sudah di-rollback (mis. "Error creating invoice"). Script kini menyebut balasan seperti ini "mungkin tersimpan". Pilihan ini sengaja konservatif: script mengecek ulang, lalu melaporkan "belum ada draf baru dari perintah ini", dan ulangan tidak tertahan.
- Balasan **200** yang isinya bukan JSON pada permintaan tulis (mis. peringatan PHP tercetak sebelum JSON) masih menjadi kode 6 "bukan data JSON". Kasus ini di luar D1–D3 dan belum ditangani.
- D4 (sidik memuat tanggal) dan kosmetik K-a s.d. K-d belum ditangani, karena di luar cakupan tugas ini.
