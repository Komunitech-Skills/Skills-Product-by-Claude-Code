# Panduan Pasang Datasette untuk UMKM (bahasa awam)

Datasette adalah program **gratis dan open-source** (lisensi Apache-2.0, dibuat Simon Willison) untuk membuka database SQLite di browser: lihat tabel, sortir, klik-klik, jalankan pertanyaan (SQL) — seperti dasbor BI berbayar, tapi jalan **di komputer Anda sendiri**. Panduan ini menyiapkan Datasette agar bisa dipakai skill **Dasbor Lokal** (`dasbor-lokal`) untuk membuka data alat lokal Komunitech: `buku-stok`, `kasir-lokal`, `crm-wa`, `absensi-lokal`, `buku-piutang`, `kas-umkm`.

> **Kabar baik:** skill `dasbor-lokal` **tetap bisa menjawab pertanyaan walau Datasette belum dipasang** (memakai `sqlite3` bawaan Python). Memasang Datasette menambah tampilan browser yang bisa diklik-klik dan tanya SQL bebas.

> Komunitech tidak berafiliasi dengan proyek Datasette atau Simon Willison. Komunitech **tidak** mendistribusikan Datasette; Anda memasangnya sendiri dari **PyPI resmi**.

**Status panduan (26 September 2026):** dicoba dengan **Datasette 0.65.5** dari PyPI resmi, dipasang ke virtualenv terpisah (bukan sistem) di Linux, dengan enam database contoh hasil menjalankan langsung skill `buku-stok`/`kasir-lokal`/`crm-wa`/`absensi-lokal`/`buku-piutang`/`kas-umkm` berisi data fiktif. Semua canned query di `skills/dasbor-lokal/templates/metadata.yml` diuji dan hasilnya dicocokkan manual — cocok, dan database **terbukti tidak berubah** (hash sebelum/sesudah sama persis). **Langkah instalasi Windows/Mac di bawah belum dicoba langsung** oleh Komunitech di komputer Windows/Mac sungguhan (disusun dari dokumentasi resmi `docs.datasette.io`); bila tampilan Anda berbeda, ikuti tulisan di layar.

## Daftar isi
1. Sebelum mulai
2. Pasang Datasette (Windows/Mac/Linux, satu cara untuk ketiganya)
3. Pengamanan wajib: localhost saja + selalu read-only/immutable
4. Menjalankan Datasette untuk alat lokal Komunitech
5. Query siap pakai (canned query)
6. Memperbarui & mencopot Datasette
7. Masalah umum

---

## 1. Sebelum mulai
| Kebutuhan | Keterangan |
|---|---|
| Komputer | Windows 10/11, macOS, atau Linux. Ruang kosong ±100 MB |
| Python 3.8+ | Wajib. Gratis di python.org; saat memasang di Windows centang **Add Python to PATH** |
| Waktu | ±5–10 menit |
| Setidaknya satu alat lokal Komunitech sudah dipakai | Datasette hanya menampilkan data yang sudah ada; alat yang belum pernah dipakai belum punya database |

Istilah: **PyPI** = toko resmi paket Python (pypi.org), tempat Datasette diunduh. **pipx** = cara resmi memasang program Python supaya terpisah rapi dari proyek lain (disarankan Datasette sendiri). **localhost / 127.0.0.1** = "komputer ini sendiri"; alamat yang tidak bisa dijangkau dari komputer/HP lain.

---

## 2. Pasang Datasette
Tingkat kesulitan: **mudah**, sama untuk Windows/Mac/Linux (semua lewat Terminal/Command Prompt, bukan installer klik-klik).

### 2.1 Cara yang disarankan: `pipx`
`pipx` adalah cara resmi yang disarankan dokumentasi Datasette (https://docs.datasette.io/en/stable/installation.html) untuk memasang program Python sebagai aplikasi command-line, terpisah dari Python proyek lain.

**Windows** (buka **Command Prompt**: tombol Windows → ketik `cmd`):
```
py -m pip install --user pipx
py -m pipx ensurepath
```
Tutup dan buka lagi Command Prompt, lalu:
```
pipx install datasette
```

**Mac / Linux** (buka **Terminal**):
```
python3 -m pip install --user pipx
python3 -m pipx ensurepath
```
Tutup dan buka lagi Terminal, lalu:
```
pipx install datasette
```
(Mac dengan Homebrew juga bisa `brew install pipx` lebih dulu, sesuai dokumentasi pipx resmi.)

- ✅ **Cek berhasil:**
  ```
  datasette --version
  ```
  Muncul `datasette, version 0.65.5` (atau lebih baru).
- ❌ **"'datasette'/'pipx' is not recognized" / "command not found"** → `ensurepath` belum tersimpan atau terminal belum dibuka ulang. Coba tutup total Terminal/Command Prompt, buka yang baru.
- ❌ **"pip is not recognized"** → Python belum di-PATH-kan; pasang ulang Python dari python.org dan centang **Add Python to PATH** (Windows), lalu ulangi.

### 2.2 Alternatif: `pip` biasa (bila `pipx` bermasalah)
```
python3 -m pip install --user datasette
```
(Windows: `py -m pip install --user datasette`.) Sedikit lebih sederhana, tapi Datasette tercampur dengan paket Python lain di akun Anda — `pipx` lebih rapi untuk jangka panjang.

**Jangan** memasang lewat cara lain (mis. skrip "tempel-dan-jalankan" dari situs yang bukan `pypi.org`/`pip`/`pipx`, atau perintah yang mengunduh lalu langsung menjalankan skrip dari internet). Kedua cara di atas satu-satunya yang direkomendasikan Komunitech.

---

## 3. Pengamanan wajib (±2 menit, sebelum dipakai tiap hari)
**Kenapa wajib?** Datasette menyalakan "server" kecil di komputer Anda yang bisa menampilkan **semua isi database** yang Anda buka lewatnya — transaksi kasir, nomor WA pelanggan, gaji karyawan, dsb. Dua aturan ini **tidak boleh dilewati**:

**Aturan 1 — Selalu localhost, jangan buka ke jaringan.**
- Jalankan Datasette **tanpa** `--host 0.0.0.0`. Skill `dasbor-lokal` selalu menyiapkan perintah dengan `--host 127.0.0.1` (bawaan Datasette sebenarnya juga sudah `127.0.0.1` bila `--host` tidak ditulis sama sekali — tetap tulis eksplisit agar jelas).
- Jangan atur *port forwarding* di router, jangan pakai *tunnel* (ngrok, Cloudflare Tunnel, dsb.), jangan pasang di hosting/VPS yang punya alamat publik tanpa HTTPS+password. Ingin dibuka dari HP/cabang lain? Itu butuh pengamanan tambahan (HTTPS, autentikasi) — konsultasikan ke **jasa setup Komunitech**, jangan dikerjakan sendiri.
- ✅ **Cek berhasil (uji dari HP, 2 menit):** sambungkan HP ke Wi-Fi yang sama, cari IP komputer (Windows: `ipconfig`; Mac: System Settings → Wi-Fi → Details; Linux: `hostname -I`), lalu di HP buka `http://<IP itu>:8001`. **Benar bila HP TIDAK bisa membuka.**
- ❌ **Kalau HP bisa membuka:** Datasette dijalankan dengan `--host 0.0.0.0` atau firewall komputer mengizinkan akses masuk untuk Python. Hentikan Datasette (Ctrl+C di terminal), jalankan ulang tanpa `0.0.0.0`, dan periksa firewall (izinkan Python hanya untuk jaringan yang benar-benar perlu, atau blokir sepenuhnya bila tak perlu diakses dari luar).

**Aturan 2 — Selalu buka database dengan `--immutable` (read-only).**
- Perintah yang disiapkan `dasbor-lokal` selalu memakai `-i PATH` (singkatan `--immutable`) untuk **setiap** database, bukan menuliskan path database begitu saja sebagai argumen biasa. Ini memastikan Datasette **tidak bisa mengubah** data asli apa pun yang diklik/diketik di browser — bahkan Datasette sendiri menolak perintah SQL selain `SELECT`.
- Jangan menambahkan flag `-a`/`--allow-download-non-immutable`, `--edit`, atau plugin pihak ketiga yang mengizinkan tulis, kecuali Anda benar-benar paham risikonya.
- ✅ **Cek berhasil:** buka salah satu tabel di browser Datasette, coba jalankan SQL `DELETE FROM ...` atau `INSERT INTO ...` di kotak "Custom SQL query" → Datasette menjawab galat "Statement must be a SELECT" dan **tidak** mengubah apa pun.

---

## 4. Menjalankan Datasette untuk alat lokal Komunitech
Cara termudah: minta skill `dasbor-lokal` menyiapkan perintahnya (menemukan sendiri database mana saja yang sudah ada):
```
python3 <folder-skill>/scripts/dasbor.py datasette
```
Salin perintah yang dicetak, tempel di Terminal/Command Prompt, Enter. Buka browser ke **http://127.0.0.1:8001**.

Lokasi database default tiap alat (skill `dasbor-lokal` sudah tahu ini; hanya untuk referensi bila Anda menjalankan Datasette manual):

| Alat | Lokasi database default |
|---|---|
| `buku-stok` | `~/KomunitechData/stok.db` |
| `kasir-lokal` | `~/KomunitechData/kasir/kasir.db` |
| `crm-wa` | `~/KomunitechData/crm/crm.db` |
| `absensi-lokal` | `~/KomunitechData/absensi/absensi.db` |
| `buku-piutang` | `~/KomunitechData/piutang/piutang.db` |
| `kas-umkm` | `~/KomunitechData/kas/kas.db` |

(`~` = folder home Anda, mis. `C:\Users\NamaAnda` di Windows. Bila Anda memindahkan database ke lokasi lain lewat `--db`/ENV saat memakai alat itu, cek lokasinya di `SKILL.md` alat tersebut.)

Perintah manual setara (bila tidak lewat script), contoh untuk `buku-stok` dan `kasir-lokal` saja:
```
datasette -i ~/KomunitechData/stok.db -i ~/KomunitechData/kasir/kasir.db --host 127.0.0.1
```
- ✅ **Cek berhasil:** terminal menampilkan "INFO: Uvicorn running on http://127.0.0.1:8001", dan browser menampilkan tabel-tabel dari database Anda.
- ❌ **"Port 8001 sudah dipakai"** → tambahkan `-p 8002` (atau port lain) di akhir perintah, lalu buka `http://127.0.0.1:8002`.
- Tutup Datasette dengan **Ctrl+C** di jendela terminal saat sudah selesai memakainya (tidak perlu dibiarkan menyala terus-menerus kecuali Anda memang mau).

---

## 5. Query siap pakai (canned query)
`skills/dasbor-lokal/templates/metadata.yml` sudah berisi pertanyaan yang paling sering dibutuhkan, muncul otomatis sebagai tautan yang bisa diklik di halaman tiap database Datasette:

| Alat | Canned query | Isi |
|---|---|---|
| `buku-stok` | `stok_menipis` | Barang yang stoknya ≤ stok minimum, paling parah di atas |
| `kasir-lokal` | `penjualan_per_hari` | Total & jumlah nota per hari (nota void dikeluarkan), 30 hari terakhir |
| `buku-piutang` | `piutang_jatuh_tempo` | Piutang yang sisa tagihannya > 0 dan sudah lewat jatuh tempo |
| `absensi-lokal` | `kehadiran_harian` | Jam masuk/pulang tiap karyawan hari ini |
| `crm-wa` | `prospek_per_tahap` | Jumlah & nilai prospek per tahap pipeline |
| `kas-umkm` | `saldo_per_akun` | Saldo tiap akun kas (laci, bank, e-wallet, dst.) |

Tidak mau/tidak sempat pasang Datasette? Semua query yang sama bisa dijalankan lewat perintah teks biasa (lihat `skills/dasbor-lokal/SKILL.md`):
```
python3 <folder-skill>/scripts/dasbor.py query buku-stok stok-menipis
```

---

## 6. Memperbarui & mencopot Datasette
- Perbarui: `pipx upgrade datasette` (atau `pip install --user --upgrade datasette`).
- Copot: `pipx uninstall datasette` (atau `pip uninstall datasette`). Database Anda **tidak ikut terhapus** — Datasette hanya membacanya, tidak menyimpan salinan.

---

## 7. Masalah umum
| Gejala | Penyebab | Solusi |
|---|---|---|
| "'datasette' is not recognized" / "command not found" | PATH belum termuat | Tutup-buka ulang terminal setelah `pipx ensurepath`; pastikan Python terpasang dengan benar |
| Browser: "This site can't be reached" di `127.0.0.1:8001` | Datasette belum/berhenti jalan | Jalankan ulang perintah dari `dasbor.py datasette`; pastikan jendela terminal tidak ditutup |
| HP bisa membuka dasbor lewat Wi-Fi | Dijalankan dengan `--host 0.0.0.0` atau firewall longgar | Ulangi tanpa `0.0.0.0` (bagian 3, Aturan 1); periksa firewall |
| Tabel kosong padahal alat sudah dipakai | Path database salah/beda dari yang Anda kira | Jalankan `python3 dasbor.py cari` untuk melihat lokasi yang terdeteksi |
| SQL `INSERT`/`DELETE` ditolak Datasette | Ini **disengaja** (immutable + Datasette hanya izinkan `SELECT`) | Bukan galat; ubah data lewat skill alat aslinya (`kasir-lokal`, `buku-stok`, dst.), bukan lewat Datasette |
| "database is locked" | Alat lain (mis. jadwal OpenClaw) sedang menulis ke database itu | Tunggu sebentar lalu coba lagi; data aman |

Butuh bantuan? **Jasa setup Komunitech** dapat memasangkan Datasette, menyiapkan dasbor untuk semua alat lokal Anda sekaligus, dan mengajari cara memakainya. Hubungi admin komunitech.com.

Komunitech tidak berafiliasi dengan proyek Datasette; Datasette adalah perangkat lunak terpisah (Apache-2.0) milik pembuatnya, Simon Willison.
