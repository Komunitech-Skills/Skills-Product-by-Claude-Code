# 09 — Uji ulang independen v1.0.4 (Akun B)

- **Tanggal:** 2026-09-25
- **Penguji:** agent penguji independen lintas akun (Akun B, Claude Code, simulasi agent). Bukan pembuat skill maupun pembuat perbaikan C1. Catatan pembuat `uji-pembuat/UJI-PEMBUAT-v1.0.4.md` hanya dibaca sebagai klaim yang diuji.
- **Objek:** `skills/dolibarr-usaha` v1.0.4 (commit `c5ec9d9`), disalin ke scratchpad `uji-doli2/` dan dijalankan dari salinan itu. `HOME` palsu.
- **Lingkungan:** Linux, Python 3.11.15. **Tanpa Dolibarr asli.** Data dan bentuk respons diambil dari kelas `Tiruan` di `tests/uji_regresi.py` (rekaman 24.0.1). **Gangguan dibuat sendiri oleh penguji:** kelas turunan `Pengganggu` mencegat jawaban **setelah** server selesai memproses permintaan. Mode gangguan milik pembuat (`putus:`/`lambat:`) tidak dipakai. Untuk uji timeout, `BATAS_WAKTU` diturunkan ke 0,5 detik lewat pembungkus, tanpa mengubah kode script.
- **Jenis gangguan:** `putus` (koneksi ditutup tanpa jawaban), `rst` (TCP RST), `lambat` (jawaban 1,5 detik > batas waktu), `500`/`502`/`504` (balasan 5xx padahal data sudah tersimpan), `sebagian` (Content-Length penuh tetapi isi terpotong, memicu IncompleteRead), `tolak500` (balasan 500 tanpa memproses, kontrol negatif).
- **Alat penguji (di luar repo):** `scratchpad/uji-doli2/uji_c1.py` (hasil: `hasil-c1.json` / `hasil-c1.txt`) dan `uji_b1b2.py` (alat uji v1.0.3 yang dijalankan ulang terhadap v1.0.4; hasil: `hasil-b1b2.txt`).

## 1. C1: idempotensi saat timeout atau koneksi putus
Perintah A: pelanggan 2 dengan 3 baris (15 × 62.500 diskon 4%, 3 × 87.500 diskon 7,5%, ongkir 137.345), `--tanggal 2026-09-24 --ya`. Di setiap skenario, percobaan 1 dijalankan dengan gangguan. Sesudahnya perintah yang **sama** diulang **3×** tanpa gangguan. Terakhir dijalankan perintah **B** yang berbeda (paku + kuas) untuk pelanggan yang sama.

### 1a. Matriks titik putus (31 skenario, 124 eksekusi perintah A)
| Titik × gangguan | Kode percobaan 1 | Ulang 3× | POST pada ulangan | Draf pelanggan 2 di akhir | Perintah B |
|---|---|---|---|---|---|
| POST header: putus / rst / lambat | **8**, "BELUM PASTI TERBUAT", "(PROV101) SUDAH TERBUAT … KOSONG", "JANGAN mengulang" | 7,7,7 | 0,0,0 | 1 (Rp 0) | 7 (lihat D3) |
| POST header: 500 / 502 / 504 (data tersimpan) | **6** "Dolibarr mengembalikan galat 504…" | 7,7,7 | 0,0,0 | 1 (Rp 0) | 7 |
| POST header: sebagian (IncompleteRead) | **6** "Galat tak terduga (IncompleteRead)" | 7,7,7 | 0,0,0 | 1 (Rp 0) | 7 |
| POST header: tolak500 (tidak tersimpan) | 6 | **0**,7,7 | 4,0,0 | 1 (lengkap) | 0 ✅ |
| Baris 1/2/3: putus / rst / lambat | **8** "TIDAK LENGKAP", "MUNGKIN sudah masuk", isi terbaca ulang (1/2/3 baris) | 7,7,7 | 0,0,0 | 1 (sebagian) | **0** ✅ |
| Baris 1/2/3: 504 (baris tersimpan) | 8, tetapi teksnya "**DITOLAK** Dolibarr…; baris ini tidak masuk" (lihat D1) | 7,7,7 | 0,0,0 | 1 | 0 ✅ |
| Baris 1/2/3: sebagian | **6** "Galat tak terduga (IncompleteRead)" | 7,7,7 | 0,0,0 | 1 | 0 ✅ |
| Baris 1: tolak500 | 8 "DITOLAK" (benar) | 7,7,7 | 0 | 1 (Rp 0) | 7 |
| Baris 2/3: tolak500 | 8 "DITOLAK" (benar) | 7,7,7 | 0 | 1 (sebagian) | 0 ✅ |
| Baca ulang akhir (validasi): putus / lambat / 500 | 8 "Semua 3 baris sudah diterima… JANGAN mengulang" | 7,7,7 | 0 | 1 (lengkap) | 0 ✅ |
| Cek daftar draf **sebelum** POST: lambat | 3 "coba lagi" (benar, belum ada yang ditulis) | **0**,7,7 | 4,0,0 | 1 | 0 ✅ |
| POST header putus **dan** baca ulang daftar putus | 8 "belum bisa dihubungi untuk dicek ulang… JANGAN mengulang" | 7,7,7 | 0 | 1 (Rp 0) | 7 |

**Kesimpulan C1:** di **31/31** skenario, jumlah draf pelanggan 2 di akhir = **1**, dan `POST invoices` hanya terjadi sekali (dua kali pada dua kontrol negatif yang percobaan pertamanya memang tidak menyimpan apa pun). **Tidak ada draf ganda** dari 93 pengulangan. Semua 124 percobaan 1 dan ulangan bebas dari "> Validasi", "COCOK", dan traceback. Kata "coba lagi" hanya muncul pada kasus yang memang belum menulis apa pun. Sidik perintah (`Kode perintah: <10 heksa>`) ada di catatan privat semua draf. JSON (timeout baris 2): `ok:false`, `kode_keluar:8`, `lengkap:false`, `gagal_baris:[2,…]`, `baris_mungkin_masuk:true`.

### 1b. Perintah berbeda dan kasus tepi
| Uji | Hasil |
|---|---|
| Perintah B setelah draf **sebagian** dari perintah A (23 skenario) | ✅ kode 0, dibuat. Tidak salah diblokir |
| Perintah A setelah draf **kosong** sisa perintah **B** (sidik B tercatat di catatan) | ⚠️ kode 7, 0 POST. Pesannya menyuruh "lengkapi barisnya sesuai pratinjau di atas", padahal pratinjau itu milik perintah A (D3) |
| Perintah A untuk pelanggan **lain** saat ada draf kosong | ✅ kode 0 |
| Draf sebagian tanggal 24 Sep, perintah yang sama diulang dengan tanggal 25 Sep (setara "besoknya" dengan tanggal default) | ⚠️ kode 0 → 2 draf. Keterbatasan ini sudah diakui pembuat |
| Dua proses bersamaan (tanpa gangguan) | ℹ️ kode 0,0 → 2 draf. Tidak ada penguncian. Di luar cakupan C1 dan tidak realistis untuk satu agen |
| `pelanggan tambah`: putus / lambat | ✅ kode 8 "MUNGKIN SUDAH TERSIMPAN", tanpa "coba lagi". Ulangan kode 7, 1 pelanggan |
| `pelanggan tambah`: 504 (data tersimpan) | kode 6 generik. Ulangan kode 7 (nama/HP sama), 1 pelanggan ✅ |

## 2. Regresi B1 & B2 (`uji_b1b2.py` dari uji v1.0.3, dijalankan ulang): **62 OK, 0 GAGAL**
- **B1**, 6 pola bersen. Angka dihitung ulang dengan `Decimal`/`Fraction` milik penguji: total baris dibulatkan half-up ke rupiah, PPN = floor(DPP × 11%) **sekali** dari DPP persis, DPP 11/12 hanya informasi. Hasilnya **0 beda**: A 1.280.158 / 140.817 (persis 140.817,38) / 1.420.975; B 43.675 / 4.804 / 48.479; C (mewah) 406.251 / 48.750 / 455.001; D 1.010 / 111 / 1.121; E (tanpa PPN) 204.167 / 0; F 116.673 / 12.834 / 129.507. DPP cara Dolibarr juga sama dengan hitungan sen penguji (A = 1.280.157,50, angka Dolibarr asli di uji v1.0.2). Perintah identik yang diulang 3× → `[7,7,7]`, 0 POST. Urutan item dibalik → tertahan. Batas toleransi tidak longgar (±1,58 dibuat). Invoice tervalidasi tidak menghalangi.
- **B2:** `--kunci-file` menang atas ENV di depan/belakang, dengan PERINGATAN. File 644 / 2 baris / biner / folder / hilang → kode 5 dan 0 kontak ke server. ENV yang diabaikan tidak pernah dikirim. Kunci baca dari file + kunci tulis di ENV → 403, tidak diam-diam memakai kunci tulis. Kosmetik lama K-a (`--kunci-file ""` jatuh ke ENV) dan K-b (`peringatan_kunci` tidak ada di JSON galat) **masih ada**.
- **Kebocoran:** 0 kunci utuh dan 0 `Traceback` di 243 keluaran (169 C1 + 74 B1/B2).

## 3. Tes otomatis
- `python3 tests/uji_regresi.py` di salinan scratchpad: **85 tes OK** (1 dilewati, khusus repo). Di repo: 85 OK.
- `python3 scripts/validate.py --skill dolibarr-usaha` (root repo): **✅ 1 skill valid, 68 baris katalog sesuai.**

## 4. Temuan
| ID | Keparahan | Lokasi | Temuan & saran |
|---|---|---|---|
| **D1** | Rendah | `Dolibarr.minta`/`_olah`, `_draf_tidak_lengkap` | Balasan **502/504** (gateway/proxy timeout, umum di VPS atau reverse proxy) dan 500 pada permintaan tulis dianggap pasti gagal. Pada POST header hasilnya kode 6 tanpa "mungkin tersimpan / jangan ulangi". Pada baris, teksnya "**DITOLAK** Dolibarr…; baris ini **tidak masuk**", padahal di tiruan baris itu sudah masuk (isi terbaca ulang memperlihatkan 1 baris). Tidak ada draf ganda karena pengulangan tetap tertahan (kode 7). Saran: 502/503/504 (dan mungkin 500) pada tulis → `mungkin_terkirim=True`. |
| **D2** | Rendah | `Dolibarr.minta` | `http.client.IncompleteRead`/`HTTPException` (jawaban terpotong) tidak ditangkap. Akibatnya jatuh ke "Galat tak terduga (IncompleteRead)", kode 6, dengan saran "jalankan `cek`". Tidak ada pesan "mungkin tersimpan", dan draf sebagian tidak dilaporkan. Pengulangan tetap tertahan. Saran: tangkap `http.client.HTTPException` bersama `OSError`. |
| **D3** | Rendah | `draf_tertinggal` | Draf **kosong** milik perintah **lain** menahan perintah berbeda untuk pelanggan yang sama, walau sidik perintahnya tercatat dan berbeda. Teks "lengkapi barisnya sesuai pratinjau di atas" lalu mengarahkan pengguna mengisi draf B dengan item A. Perilaku ini didokumentasikan sebagai sengaja konservatif dan bisa dilewati dengan `--tetap-buat`. Saran: draf kosong bersidik lain → cukup CATATAN; atau ubah teks menjadi "hapus draf kosong itu". |
| D4 | Info | `kode_perintah` | Sidik memuat tanggal, sehingga draf **sebagian** dari hari sebelumnya tidak dikenali (draf kosong tetap dikenali). Sudah diakui pembuat. |
| K-a, K-b, K-c, K-d | Kosmetik | lihat `08-…` §5 | Belum ditangani, sesuai catatan pembuat. |

## 5. Batasan uji
Seluruh uji memakai server tiruan. Perilaku timeout, RST, dan 5xx DoliWamp/Apache asli, kolom `note_private` pada user API berhak terbatas, dan pengaturan desimal selain 2 **tidak** diuji. Server tiruan menghitung seperti Dolibarr (2 desimal per baris, half-up), dan cara hitung ini cocok dengan satu data asli (skenario A).
