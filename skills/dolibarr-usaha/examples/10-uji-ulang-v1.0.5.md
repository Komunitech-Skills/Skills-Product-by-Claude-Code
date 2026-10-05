# 10 — Uji ulang independen v1.0.5 (Akun B)

- **Tanggal:** 2026-09-25
- **Penguji:** agent penguji independen lintas akun (Akun B, Claude Code, simulasi agent). Bukan pembuat skill dan bukan pembuat perbaikan D1–D3. `uji-pembuat/UJI-PEMBUAT-v1.0.5.md` hanya dibaca sebagai daftar klaim yang diuji.
- **Objek:** `skills/dolibarr-usaha` v1.0.5 (commit `a5d2dda`). Skill disalin ke scratchpad `uji-doli3/` dan dijalankan dari salinan itu dengan `HOME` palsu. Repo tidak diubah, kecuali dua file laporan di `examples/`.
- **Lingkungan:** Linux, Python 3.11. **Tanpa Dolibarr asli.** Data dan bentuk respons diambil dari kelas `Tiruan` di `tests/uji_regresi.py` (rekaman 24.0.1). **Gangguan dibuat sendiri oleh penguji** (kelas turunan `Pengganggu` yang mencegat jawaban). Mode `galat:`/`tolak:`/`sebagian:` milik pembuat **tidak** dipakai. Untuk uji timeout, `BATAS_WAKTU` diturunkan ke 0,5 detik lewat pembungkus. Kode script tidak diubah.
- **Alat penguji (scratchpad, di luar repo):** `uji_d.py` → `hasil-d.json`, `uji_d2.py` → `hasil-d2.json`/`hasil-d2.txt`, dan `uji_b1b2.py` (alat uji v1.0.3/v1.0.4 yang dijalankan ulang) → `hasil-b1b2.txt`.

## Jenis gangguan
Kelompok pertama terjadi **SETELAH** server memproses dan menyimpan data:

| Kode | Arti |
|---|---|
| `putus` | Koneksi ditutup tanpa jawaban |
| `rst` | Koneksi di-reset (TCP RST) |
| `lambat` | Jawaban datang 1,5 detik, melewati batas waktu |
| `500` | Halaman HTML 500 |
| `500json` | JSON galat gaya Dolibarr, 500 |
| `502` / `503` / `504` | Halaman HTML proxy |
| `504kosong` | 504 tanpa isi |
| `504terpotong` | Halaman galat 504 ikut terpotong |
| `sebagian` / `sebagian0` / `sebagianhampir` | `Content-Length` penuh, tetapi yang terkirim hanya 1 bita, 0 bita, atau semua kecuali 1 bita (`IncompleteRead`) |
| `sampah` | Baris status HTTP rusak (`BadStatusLine`) |

Kelompok kedua adalah **kontrol negatif**: server membalas **TANPA** memproses apa pun.

| Kode | Arti |
|---|---|
| `tolak500` / `tolak502` / `tolak503` / `tolak504` | Balasan 5xx tanpa memproses |
| `tolak501` | Modul mati |
| `tolak503ip` | Balasan `503`, isi `API not allowed from your IP …` |

## 1. D1 + D2 + C1: matriks titik putus (80 skenario)
Perintah A: pelanggan 2 dengan 3 baris (15 × 62.500 diskon 4%, 3 × 87.500 diskon 7,5%, ongkir 137.345), `--tanggal 2026-09-24 --ya`. Setiap skenario berjalan begini:
1. Percobaan 1 dengan gangguan.
2. Perintah yang **sama** diulang **3×** tanpa gangguan.
3. Perintah **B** yang berbeda (paku + kuas) dijalankan untuk pelanggan yang sama.

Total eksekusi: **320 perintah A dan 80 perintah B**.

| Titik × gangguan | Percobaan 1 | Ulang 3× | POST saat ulang | Draf A akhir | B |
|---|---|---|---|---|---|
| POST header: putus / rst / lambat | **8** "BELUM PASTI TERBUAT", "(PROV101) SUDAH TERBUAT … KOSONG" | 7,7,7 | 0 | 1 (Rp 0) | **0** + CATATAN ✅ |
| POST header: 500 / 500json / 502 / **503** / 504 / 504kosong / 504terpotong | **8** "membalas galat 504: 504 Gateway Timeout … SAAT MENGIRIM data … bisa terjadi SETELAH data diproses. Data ini MUNGKIN SUDAH TERSIMPAN", draf kosong disebut, "JANGAN mengulang" | 7,7,7 | 0 | 1 (Rp 0) | 0 + CATATAN ✅ |
| POST header: sebagian / sebagian0 / sebagianhampir / sampah | **8** "Jawaban Dolibarr terpotong/rusak SAAT MENGIRIM data (IncompleteRead / BadStatusLine) … MUNGKIN SUDAH TERSIMPAN" | 7,7,7 | 0 | 1 (Rp 0) | 0 + CATATAN ✅ |
| POST header: tolak500 / 502 / 503 / 504 (tidak tersimpan) | 8, "belum ada draf baru dari perintah ini … bisa jadi permintaan tadi memang tidak diproses" | **0**,7,7 | 4,0,0 | 1 (lengkap) | 0 ✅ |
| POST header: **tolak501** | **4** "Modul … belum aktif", tanpa "mungkin tersimpan" ✅ | 0,7,7 | 4,0,0 | 1 | 0 |
| POST header: **tolak503ip** | **5** "Dolibarr menolak alamat IP komputer ini", tanpa "mungkin tersimpan" ✅ | 0,7,7 | 4,0,0 | 1 | 0 |
| Baris 1/2/3: putus / rst / lambat / 500json / 502 / 503 / 504 / 504terpotong / sampah / sebagian0 / sebagianhampir (baris **tersimpan**) | 8, "Baris N: Dolibarr membalas galat 504 / jawaban … terpotong. Baris ini MUNGKIN sudah masuk", lalu "Menurut isi draf yang dibaca ulang, baris N **SUDAH** masuk". Tidak ada "DITOLAK" | 7,7,7 | 0 | 1 (N baris) | 0 ✅ |
| Baris 1/2/3: tolak500 / tolak504 | 8, "MUNGKIN sudah masuk", lalu "baris N **BELUM** masuk" (benar) | 7,7,7 | 0 | 1 (N−1 baris) | 0 ✅ (baris 1 → 0 + CATATAN) |
| Baris 1/2/3: tolak501 / tolak503ip | 8, "Baris N **DITOLAK** Dolibarr (…); baris ini tidak masuk" (benar, pasti ditolak) | 7,7,7 | 0 | 1 | 0 ✅ |
| Baca ulang akhir GET: putus / lambat / 500 / 502 / 504 / sebagian | 8 "Semua 3 baris sudah diterima … JANGAN mengulang" | 7,7,7 | 0 | 1 (lengkap) | 0 ✅ |
| Cek daftar draf **sebelum** POST: lambat / sebagian | 3 "coba lagi" (benar, belum ada yang ditulis) | 0,7,7 | 4,0,0 | 1 | 0 |
| Cek daftar draf **sebelum** POST: 502 / 504 | 6 galat biasa (benar, belum ada yang ditulis) | 0,7,7 | 4,0,0 | 1 | 0 |
| POST 504 + baca ulang daftar 502; POST sebagian + baca ulang daftar putus | 8 "belum bisa dihubungi untuk dicek ulang … JANGAN mengulang" | 7,7,7 | 0 | 1 (Rp 0) | 0 + CATATAN |

**Hasil keseluruhan:**
- **80/80 skenario** berakhir dengan tepat **1 draf A**. Dari 240 pengulangan: **0 draf ganda**, dan 0 POST, kecuali 10 kontrol yang percobaan pertamanya memang tidak menyimpan apa pun.
- **0** "Galat tak terduga", **0** Traceback, dan **0** "DITOLAK" untuk data yang ternyata tersimpan.
- Pada percobaan gagal (kode ≠ 0): **0** "COCOK" dan **0** "> Validasi".
- Sidik perintah ada di catatan privat semua draf.
- Judul halaman proxy tidak tercetak dua kali.
- JSON baris 2 dengan 504: `ok:false`, `kode_keluar:8`, `lengkap:false`, `baris_masuk:true`, `baris_mungkin_masuk:true`.
- JSON POST terpotong: `kode_keluar:8`.

Catatan alat: pada putaran pertama, mode `sebagian` di baris tidak memotong apa pun. Jawaban baris hanya berupa angka 1 bita, jadi jawabannya tetap utuh dan hasilnya kode 0 yang sah. Karena itu mode ini diganti `sebagian0`/`sebagianhampir` di `uji_d2.py`, dan hasilnya tercantum di tabel di atas.

### 1b. `pelanggan tambah` (20 gangguan)
- Semua gangguan "setelah diproses", termasuk 503, 504kosong, 504terpotong, terpotong, dan sampah, menghasilkan **kode 8** "MUNGKIN SUDAH TERSIMPAN" tanpa "coba lagi". Ulangan mendapat kode 7, dan pelanggan tetap **1**.
- Kontrol tolak 500/502/503/504: kode 8, lalu ulangan kode 0, pelanggan 1.
- **tolak501** menghasilkan kode **4**, dan **tolak503ip** menghasilkan kode **5**. Ulangan kode 0. Keduanya **tidak** memakai label "mungkin tersimpan", sesuai dokumentasi (`_5xx_tidak_pasti`, SKILL.md tabel galat).

### 1c. D1/D2 pada perintah BACA (5 perintah × 6 gangguan)
`cek`, `piutang`, `stok`, `pelanggan cari`, dan `laporan-harian` diuji dengan gangguan di semua GET:
- 500/502/503/504 menghasilkan **kode 6** "Dolibarr mengembalikan galat 50x: …" (galat biasa).
- Jawaban terpotong/rusak menghasilkan **kode 3** "Jawaban Dolibarr terpotong/rusak (IncompleteRead/BadStatusLine)" dengan saran "coba lagi". Saran ini benar karena perintahnya hanya membaca.
- **0** label "MUNGKIN SUDAH TERSIMPAN", 0 POST, 0 traceback.

## 2. D3: draf kosong dari perintah lain
| Uji | Hasil |
|---|---|
| B terputus di POST header (putus / 504 / terpotong), lalu A | A **kode 0**, 4 POST, dengan "CATATAN: pelanggan ini juga punya draf KOSONG (Rp 0) sisa perintah LAIN … (PROV101) … hapus di Dolibarr". A diulang → 7 (kembar). ✅ |
| Sesudahnya B diulang 2× | **7, 7**, 0 POST. Tindakan: "Hapus draf kosong (PROV101) (ID 101), lalu jalankan ulang perintah ini." Kalimat lama "lengkapi barisnya sesuai pratinjau" **tidak muncul lagi** ✅ |
| A terputus (draf kosong sidik A), lalu A lagi | **7** dengan "Hapus draf kosong". B untuk pelanggan sama → 0 + CATATAN ✅ |
| Draf kosong **tanpa kode sah**, dengan catatan: kosong / "dibuat manual oleh kasir" / "Kode perintah: XYZ" / "kode perintah: abcdef0123" (huruf kecil) | Semuanya **kode 7**, 0 POST, dengan tindakan "Buka draf kosong (PROV95) (ID 95). Jika memang tidak dipakai, hapus…" ✅ (kode palsu/salah bentuk tidak dianggap "perintah lain") |
| `--json` | `draf_kosong_lain: ["(PROV101)"]`, `ok:true` ✅ |

## 3. Regresi B1, B2, dan C1
- **B1 + B2** (`uji_b1b2.py`): **62 OK, 0 GAGAL**.
  - Angka B1 dihitung ulang dengan `Decimal` penguji: total baris dibulatkan half-up ke rupiah, PPN = floor(DPP × 11%) **sekali** dari DPP persis. Hasilnya **0 beda**: A 1.280.158 / 140.817 (persis 140.817,38) / 1.420.975; B 43.675 / 4.804 / 48.479; C 406.251 / 48.750 / 455.001; D 1.010 / 111 / 1.121; E (tanpa PPN); F.
  - DPP cara Dolibarr juga sama dengan hitungan sen penguji (A = 1.280.157,50). Perintah identik yang diulang 3× → `[7,7,7]`, 0 POST.
  - B2: `--kunci-file` menang atas ENV dengan PERINGATAN. File rusak → kode 5 dan 0 kontak. Kunci ENV yang diabaikan tidak pernah dikirim.
- **C1:** semua 31 titik putus dari uji v1.0.4 tercakup dan diperluas di matriks §1 (80 skenario). Hasilnya 0 draf ganda.
- **Kebocoran:** 0 kunci utuh, 0 Traceback, dan 0 "Galat tak terduga" di **580 keluaran** (466 + 40 + 74).

## 4. Tes otomatis
- `python3 tests/uji_regresi.py`: salinan scratchpad **93 tes OK** (1 dilewati, khusus repo). Di repo: **93 OK**.
- `python3 scripts/validate.py --skill dolibarr-usaha` (root repo): **✅ 1 skill valid, 68 baris katalog sesuai.**

## 5. Temuan tersisa
| ID | Keparahan | Temuan |
|---|---|---|
| D5 | Info | Dolibarr asli membalas **500** "Error creating invoice" juga untuk penolakan bisnis yang di-rollback. v1.0.5 menyebutnya "MUNGKIN SUDAH TERSIMPAN". Pesan ini aman karena script mengecek ulang, melaporkan "belum ada draf baru dari perintah ini", dan tidak menahan ulangan. Namun jika sebabnya tetap, pengguna awam bisa menerima kode 8 berulang kali. Pembuat sudah mengakui hal ini. |
| D4' | Info | Draf **kosong** sisa perintah A bertanggal 24 tidak menahan A yang diulang dengan tanggal 25 (sidik memuat tanggal). Hasilnya draf baru + CATATAN "sisa perintah **LAIN**". Tidak ada risiko tagihan ganda karena draf Rp 0 tidak menagih. Kata "LAIN" sedikit keliru untuk barang yang sama. Di v1.0.4 kasus ini tertahan. |
| – | Info | Kode 501 dan 503-blokir-IP dianggap pasti ditolak. Ini sesuai perilaku Dolibarr (dicek sebelum API dimuat), tetapi bentuk teks 503 asli belum dicocokkan dengan DoliWamp. Balasan 200 non-JSON saat menulis masih kode 6 (diakui pembuat). |
| K-a…K-d | Kosmetik | Belum ditangani, di luar cakupan. |

## 6. Batasan uji
Seluruh uji memakai server tiruan. Hal-hal berikut **tidak** diuji:
- Perilaku 5xx/putus dari Apache/DoliWamp/proxy asli.
- Kolom `note_private` untuk user API berhak terbatas.
- Balapan dua proses.
