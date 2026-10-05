# Uji OpenClaw asli SEBELUM vs SESUDAH — pph21-ter

**Tanggal:** 2026-10-01 · **Penguji:** agent penguji independen (bukan pembuat skill)

> **KOREKSI 2026-10-05 (versi 1.0.5):** penilaian DTP di dokumen ini memakai acuan yang keliru. Menurut teks PMK 105/2025 (Pasal 2 ayat 1, Pasal 5, Lampiran B), PPh 21 tetap dipotong lalu DTP dibayar tunai, sehingga pegawai gaji Rp 6.000.000 menerima **Rp 6.000.000**, bukan Rp 6.045.000. Jawaban "Rp 6.000.000 (utuh)" yang di bawah dinilai SALAH sebenarnya benar angkanya; jawaban "Rp 6.045.000" yang dinilai benar sebenarnya keliru. Cuplikan jualan di akhir dokumen **tidak boleh dipakai**. Riwayat asli dibiarkan apa adanya. Lihat `references/dtp-pmk105.md`.

## Cara uji

- OpenClaw 2026.9.6 lokal (`openclaw agent --local`), model router Komunitech `komunitech` → `claude-sonnet-5` (sama dengan bot member).
- SEBELUM = home tanpa skill ini; SESUDAH = home berisi skill ini saja. Home dibuat ulang bersih per skenario; pesan identik di kedua sisi; balasan lanjutan (bila ada) juga identik.
- Angka diverifikasi independen dengan Python + aturan Indonesia.
- Home SESUDAH: `s-pph21-ter`; SEBELUM: `k-pph21-ter`.


## Skenario 1 — Normal: PPh 21 setahun K/1 + THR Maret, kenapa Desember beda

### Giliran 1 — pesan pengguna
~~~~text
Pak, karyawan saya status K/1, gaji tetap Rp 8.500.000 sebulan dari Januari 2026, ikut BPJS TK jadi dipotong JHT 2% + JP 1% tiap bulan. THR Rp 8.500.000 cair bulan Maret. Usaha saya bengkel motor. Tolong hitung PPh 21 dia setahun 2026 per bulan ya, sama kenapa Desember katanya beda sendiri
~~~~

**SEBELUM (tanpa skill)** — tools: tool_search, web_fetch (pajak.go.id), tool_call

~~~~text
Sudah saya hitung lengkap, Pak. Saya pakai aturan PPh 21 terbaru (skema TER – PP 58/2023 & PMK 168/2023) yang berlaku sejak 2024 dan masih jadi dasar perhitungan 2026.

**1. Tentukan kategori dulu**
- Status K/1 → PTKP setahun Rp63.000.000 → masuk **kategori TER B**.

**2. PPh 21 Januari–November (pakai tarif TER langsung dari gaji bruto bulan itu)**

| Bulan | Bruto | Bracket TER B | Tarif | PPh 21 |
|---|---|---|---|---|
| Jan | 8.500.000 | 7.300.001–9.200.000 | 1,00% | Rp85.000 |
| Feb | 8.500.000 | sda | 1,00% | Rp85.000 |
| **Mar** (+THR) | **17.000.000** | 16.400.001–18.450.000 | **7,00%** | **Rp1.190.000** |
| Apr–Nov (8 bulan) | 8.500.000/bln | 7.300.001–9.200.000 | 1,00% | Rp85.000/bln |

Total dipotong Jan–Nov = 10×85.000 + 1.190.000 = **Rp2.040.000**

**3. Desember = rekonsiliasi tahunan (wajib pakai tarif Pasal 17, bukan TER lagi)**

| Komponen | Nilai |
|---|---|
| Bruto setahun (gaji 12× + THR) | Rp110.500.000 |
| Biaya jabatan (5%, maks 6jt/thn) | −Rp5.525.000 |
| Iuran pensiun (JHT 2%+JP 1% = 3% × gaji, bukan dari THR) | −Rp3.060.000 |
| **Penghasilan neto setahun** | Rp101.915.000 |
| PTKP K/1 | −Rp63.000.000 |
| **PKP** | Rp38.915.000 |
| Tarif Pasal 17 (≤60 juta → 5%) | **PPh 21 setahun = Rp1.945.750** |

**PPh 21 Desember** = Setahun − Jan-Nov = 1.945.750 − 2.040.000 = **−Rp94.250**

Artinya di Desember karyawan **tidak dipotong lagi**, malah ada **kelebihan potong Rp94.250 yang harus dikembalikan/dikreditkan** ke dia.

**Kenapa Desember selalu "beda sendiri":**
Jan–Nov itu cuma potongan di muka pakai tarif flat sesuai bracket gaji bruto bulan itu (TER), nggak peduli PTKP atau biaya jabatan. Giliran Desember, kantor WAJIB hitung ulang pajak setahun penuh pakai tarif progresif Pasal 17 setelah dikurangi PTKP & biaya jabatan — baru selisihnya dipotong/dikembalikan di bulan itu.

Di kasus karyawan Bapak ini jadi ekstrem karena THR muncul sekaligus di Maret, bikin bruto bulan itu melompat ke bracket TER 7% — padahal tarif efektif tahunannya cuma sekitar 1,76%. Makanya bukan cuma "beda", tapi malah kelebihan bayar yang harus dikembalikan di Desember.

Catatan: perhitungan ini asumsi BPJS JHT/JP dihitung dari gaji pokok saja (bukan dari THR, sesuai praktik umum) dan belum ada perubahan tarif PTKP/TER di 2026. Kalau mau saya bikinkan rekap dalam bentuk Excel/sheet biar gampang dipakai tiap bulan, tinggal bilang saja Pak.
~~~~

**SESUDAH (dengan skill)** — tools: read, exec (scripts/pph21.py)

~~~~text
**PPh 21 2026 — Karyawan Bengkel, status K/1 (TER kategori B)**

| Bulan | Penghasilan Bruto | Tarif TER | PPh 21 Dipotong |
|---|---:|---:|---:|
| Januari | Rp 8.500.000 | 1% | Rp 85.000 |
| Februari | Rp 8.500.000 | 1% | Rp 85.000 |
| Maret (+ THR) | Rp 17.000.000 | 7% | Rp 1.190.000 |
| April | Rp 8.500.000 | 1% | Rp 85.000 |
| Mei | Rp 8.500.000 | 1% | Rp 85.000 |
| Juni | Rp 8.500.000 | 1% | Rp 85.000 |
| Juli | Rp 8.500.000 | 1% | Rp 85.000 |
| Agustus | Rp 8.500.000 | 1% | Rp 85.000 |
| September | Rp 8.500.000 | 1% | Rp 85.000 |
| Oktober | Rp 8.500.000 | 1% | Rp 85.000 |
| November | Rp 8.500.000 | 1% | Rp 85.000 |
| Desember | Rp 8.500.000 | Pasal 17 (hitung ulang) | **(Rp 94.250)** → lebih potong |
| **Total** | **Rp 110.500.000** | | **Rp 1.945.750** |

**Kenapa Desember beda sendiri?**
Di Jan–Nov, PPh 21 dihitung simpel: tarif TER × bruto bulan itu. Tapi Desember (atau bulan terakhir kerja) wajib dihitung ulang pakai tarif progresif Pasal 17 atas penghasilan SETAHUN penuh — ini aturan resmi (PP 58/2023), bukan kesalahan hitung.

Rinciannya:
- Bruto setahun: Rp 110.500.000
- Biaya jabatan 5% (maks Rp 6.000.000/tahun): Rp 5.525.000
- Iuran JHT 2% + JP 1% (karyawan) setahun: Rp 3.060.000
- Penghasilan neto: Rp 101.915.000
- PTKP K/1: Rp 63.000.000
- PKP (dibulatkan ke ribuan): Rp 38.915.000
- PPh 21 terutang setahun = 5% × Rp 38.915.000 = **Rp 1.945.750**
- Sudah dipotong Jan–Nov: Rp 2.040.000
- Selisih: **lebih potong Rp 94.250**

Karena total yang sudah dipotong selama setahun (Rp 2.040.000) ternyata lebih besar dari pajak yang sebenarnya terutang (Rp 1.945.750), di Desember bapak **tidak memotong lagi**, malah wajib **mengembalikan kelebihan Rp 94.250** ke karyawan — paling lambat akhir Januari 2027.

**Ringkasan Setahun**
- Total gaji + THR: Rp 110.500.000
- Total PPh 21 terutang (riil): Rp 1.945.750
- Kelebihan potong yang harus dikembalikan di Desember: Rp 94.250

**Asumsi yang dipakai:**
- Iuran JHT 2% + JP 1% = Rp 255.000/bulan (3% × Rp 8.500.000), dipotong tiap bulan termasuk Maret (basis JHT/JP biasanya gaji pokok tanpa THR — tolong konfirmasi kalau beda).
- THR Rp 8.500.000 digabung ke bruto Maret (sesuai bulan cair).
- Gaji tetap sama Jan–Des, tidak ada kenaikan/bonus lain.
- Bengkel motor bukan termasuk sektor penerima PPh 21 DTP 2026 (alas kaki/tekstil/furnitur/kulit/pariwisata), jadi tidak dihitung DTP.

⚠️ Kelebihan potong Rp 94.250 di Desember wajib dikembalikan ke karyawan, bukan disetor ke negara.

_Alat bantu hitung, bukan nasihat pajak. Dasar: PP 58/2023, PMK 168/2023, UU HPP, berlaku per 23 September 2026. Kasus khusus: Kring Pajak 1500200 atau konsultan pajak._
~~~~

### Verifikasi
Hitung independen (Python, tabel TER B PP 58/2023, Pasal 17 UU HPP):
- TER B: Rp 8.500.000 → baris >7,3 jt s.d. 9,2 jt = 1% → Rp 85.000; Maret Rp 17.000.000 → baris >16,4 jt s.d. 18,45 jt = 7% → Rp 1.190.000. Jan–Nov = 10 × 85.000 + 1.190.000 = **Rp 2.040.000**.
- Setahun: bruto 110.500.000 − biaya jabatan 5% 5.525.000 − iuran (255.000 × 12) 3.060.000 = neto 101.915.000; PTKP K/1 63.000.000 → PKP 38.915.000 → 5% = **Rp 1.945.750** → Desember **lebih potong Rp 94.250** (dikembalikan ke pegawai paling lambat akhir bulan berikutnya — PMK 168/2023).
- SEBELUM: semua angka **benar**. SESUDAH: semua angka **benar** dan identik dengan script.
- Bengkel motor bukan sektor DTP PMK 105/2025 → keduanya tidak memakai DTP (SESUDAH menyebut alasannya).

### Skor
| | Skor | Alasan |
|---|---:|---|
| SEBELUM | 8 | Angka & penjelasan Desember benar, mencari ke pajak.go.id. Kurang: tanpa disclaimer/dasar aturan, tanpa batas waktu pengembalian kelebihan, tidak menyinggung DTP 2026. |
| SESUDAH | 9 | Angka sama benarnya + dari script teruji; tabel lengkap 12 bulan, batas waktu pengembalian (akhir Januari 2027), cek DTP sektor, asumsi & disclaimer. Pembeda kecil dibanding SEBELUM. |

Skill terpakai: Ya (SKILL.md dibaca, `scripts/pph21.py setahun` dijalankan).

## Skenario 2 — Info kurang + jebakan aturan terbaru: PPh 21 DTP 2026 (konveksi)

### Giliran 1 — pesan pengguna
~~~~text
Karyawan konveksi saya gajinya Rp 6.000.000 sebulan. PPh 21 bulan Oktober 2026 dia berapa ya? Katanya tahun ini pajak karyawan ada yang ditanggung pemerintah, bener ga?
~~~~

**SEBELUM (tanpa skill)** — tools: tool_search, web_fetch, tool_call

~~~~text
**PPh 21 Oktober 2026 — gaji Rp 6.000.000**

Tergantung status PTKP karyawan (kawin/tanggungan), karena itu menentukan kategori TER:

- **TK/0, TK/1, atau K/0** (Kategori A) → tarif efektif 0,75% untuk gaji Rp5.950.001–Rp6.300.000 → PPh 21 = **Rp45.000/bulan**
- **TK/2, TK/3, K/1, atau K/2** (Kategori B) → ambang bebas potongan Rp6.200.000 → gaji 6 juta masih di bawahnya → PPh 21 = **Rp0**
- **K/3** (Kategori C) → ambang bebas potongan Rp6.600.000 → PPh 21 = **Rp0**

Jadi kalau karyawan belum kawin tanpa tanggungan (TK/0, paling umum), potongannya Rp45.000. Kalau sudah kawin/punya tanggungan, kemungkinan besar Rp0. Status PTKP-nya yang mana?

**Soal PPh 21 ditanggung pemerintah — benar, dan ini relevan untuk usaha Bapak/Ibu:**

Pemerintah resmi merilis **PMK Nomor 105 Tahun 2025** — PPh 21 DTP berlaku untuk **seluruh masa pajak Januari–Desember 2026**, menyasar 5 sektor padat karya: **industri tekstil & pakaian jadi (termasuk konveksi)**, alas kaki, furnitur, kulit, dan pariwisata.

- Syarat perusahaan: KLU Utama termasuk daftar lampiran PMK 105/2025 (konveksi masuk kategori ini)
- Syarat karyawan: penghasilan bruto tetap ≤ Rp10 juta/bulan (gaji Rp6 juta jelas memenuhi), NIK sudah tervalidasi NPWP
- Mekanismenya: PPh 21 tetap dihitung normal pakai TER seperti di atas, tapi **tidak dipotong dari gaji** — nilainya justru **dibayar tunai oleh perusahaan** ke karyawan bersamaan gaji (dananya ditanggung pemerintah, bukan dari kantong perusahaan)
- Jadi kalau usaha konveksi Bapak/Ibu masuk KLU yang sesuai, karyawan dengan gaji 6 juta itu praktis **tidak kena potongan PPh 21 sama sekali** — bahkan kalau PPh 21-nya Rp45.000 (status TK/0), itu tetap diterima penuh sebagai gaji + uang tunai DTP tambahan.

**Yang perlu dicek/dilakukan sebagai pemberi kerja:**
1. Pastikan KLU Utama usaha di Coretax/DJP Online sudah terdaftar sebagai industri tekstil/pakaian jadi (konveksi)
2. Validasi NIK-NPWP tiap karyawan
3. Hitung PPh 21 pakai TER seperti biasa, tandai sebagai PPh 21 DTP di e-Bupot 21, bayar tunai ke karyawan — bukan dipotong
4. Wajib lapor realisasi di SPT Masa PPh 21/26 tiap bulan (telat lapor bisa bikin insentif setahun gugur)

Mau saya bantu hitung juga untuk status PTKP spesifik karyawan Bapak/Ibu, atau cek apakah KLU usaha konveksinya sudah pasti masuk daftar?
~~~~

**SESUDAH (dengan skill)** — tools: read

~~~~text
Sebelum saya hitung pastinya, saya perlu 2 info:

1. Status PTKP karyawan per 1 Januari 2026 (TK/0, TK/1, K/0, K/1, dst — sesuai status kawin & jumlah tanggungan)?
2. Soal PPh 21 DTP 2026: usaha konveksi Anda itu industri **tekstil & pakaian jadi** (atau alas kaki/furnitur/kulit/pariwisata), dan KLU utamanya tercantum di Lampiran A PMK 105/2025? Ini relevan karena gajinya ≤ Rp10 juta — kalau cocok, PPh 21-nya bisa ditanggung pemerintah (tidak dipotong dari gaji karyawan).

Begitu dua hal ini saya tahu, saya hitung langsung angkanya.
~~~~

### Giliran 2 — pesan pengguna
~~~~text
Dia masih bujang, belum ada tanggungan. KLU usaha saya 14111 pakaian jadi, kata konsultan masuk lampiran. Gajinya dari Januari juga 6 juta, tidak ada BPJS. Jadi Oktober saya potong berapa dan dia terima bersih berapa?
~~~~

**SEBELUM (tanpa skill)** — tools: —

~~~~text
Dengan data itu (TK/0, gaji tetap Rp6.000.000 sejak Januari, KLU 14111 dikonfirmasi masuk lampiran PMK 105/2025):

**Hitung PPh 21 terutang Oktober**
- Kategori TER: **A** (status TK/0)
- Gaji Rp6.000.000 masuk lapisan "di atas Rp5.950.000 s.d. Rp6.300.000" → tarif **0,75%**
- PPh 21 terutang = 6.000.000 × 0,75% = **Rp45.000**

**Karena kena fasilitas DTP (PMK 105/2025) — mekanismenya dibalik:**
Normalnya Rp45.000 ini dipotong dari gaji. Tapi karena KLU usaha Bapak/Ibu masuk sektor yang disubsidi, aturannya: **jangan dipotong** — malah dibayar tunai ekstra ke karyawan dari dana pemerintah.

**Slip gaji Oktober 2026:**

| Komponen | Nominal |
|---|---|
| Gaji pokok | Rp6.000.000 |
| Potongan PPh 21 | **Rp0** (ditanggung pemerintah) |
| Tunai PPh 21 DTP (tambahan) | **+Rp45.000** |
| **Total diterima (take home)** | **Rp6.045.000** |

Jadi dia bukan dipotong, tapi malah terima lebih — Rp6.045.000, naik Rp45.000 dari gaji pokoknya. (Tidak ada potongan BPJS sesuai info Bapak/Ibu.)

**Yang wajib dilakukan sebagai pemberi kerja, biar fasilitasnya sah:**
1. Cantumkan di slip gaji keterangan: *"PPh Pasal 21 Ditanggung Pemerintah Eks PMK Nomor 105 Tahun 2025"*
2. Hitung & catat PPh 21 Rp45.000 itu di e-Bupot 21 (Coretax) dengan kode DTP, bukan dipotong
3. Lapor di SPT Masa PPh 21/26 paling lambat tanggal 20 bulan berikutnya (untuk Oktober → lapor paling lambat 20 November 2026)
4. Pastikan NIK karyawan sudah tervalidasi NPWP — kalau belum valid, fasilitas ini gagal diklaim untuk dia

Catatan: syarat gaji ≤Rp10 juta ini dinilai dari Januari 2026 — karena gajinya tetap 6 juta sejak Januari, status eligible-nya sudah terkunci untuk sepanjang 2026 meski nanti naik gaji di tengah tahun (selama di bulan berjalan tidak melebihi 10 juta).
~~~~

**SESUDAH (dengan skill)** — tools: exec (scripts/pph21.py)

~~~~text
**PPh 21 Oktober 2026 — Karyawan Konveksi, status TK/0 (TER kategori A)**

| Bulan | Penghasilan bruto | Tarif TER | PPh 21 terutang | PPh 21 DTP |
|---|---|---|---|---|
| Oktober | Rp 6.000.000 | 0,75% | Rp 45.000 | Rp 45.000 (ditanggung pemerintah) |

**Jadi:**
- PPh 21 terutang Oktober: **Rp 45.000**
- Karena usaha Anda (KLU 14111, pakaian jadi) masuk Lampiran A PMK 105/2025 dan gaji ≤ Rp 10 juta, PPh 21 ini **ditanggung pemerintah (DTP)** — **tidak dipotong dari gaji karyawan**.
- **Yang Anda potong dari gajinya: Rp 0**
- **Gaji bersih yang dia terima: Rp 6.000.000 (utuh)**

Jadi betul kata orang itu — untuk sektor konveksi/pakaian jadi dengan gaji segini, pajaknya ditanggung negara, bukan karyawan. Yang perlu Anda lakukan sebagai pemberi kerja: tetap **hitung dan lapor** PPh 21 Rp 45.000 ini di SPT Masa PPh 21 dengan kode fasilitas DTP (via e-Bupot/Coretax), meski uangnya tidak dipotong dari karyawan — ini syarat supaya fasilitasnya sah.

Asumsi: gaji Rp 6 juta sudah sama dari Januari–Oktober, tidak ada BPJS/tunjangan/lembur tambahan, tidak ada iuran pensiun dipotong, tidak ada bonus/THR bulan ini.

⚠️ Januari–November (termasuk Oktober) pakai tarif TER langsung dari tabel; hitung ulang pasti terjadi di Desember pakai tarif Pasal 17 — bisa saya hitungkan juga kalau mau diproyeksikan dari sekarang.

_Alat bantu hitung, bukan nasihat pajak. Dasar: PP 58/2023, PMK 168/2023, UU HPP, PMK 105/2025, berlaku per 23 September 2026. Kasus khusus: Kring Pajak 1500200 atau konsultan pajak._
~~~~

### Verifikasi
- TK/0 → TER A; Rp 6.000.000 → baris >5,95 jt s.d. 6,3 jt = 0,75% → PPh 21 terutang **Rp 45.000** (keduanya benar).
- PMK 105/2025 (dicatat juga di `references/regulasi.md` skill ini, baris 20): PPh 21 DTP **dibayarkan tunai** oleh pemberi kerja kepada pegawai saat pembayaran penghasilan. Jadi pegawai menerima gaji Rp 6.000.000 **+ DTP tunai Rp 45.000 = Rp 6.045.000**; script skill pun mencetak kolom "PPh 21 DTP (dibayar tunai)".
- SEBELUM giliran 2: take home **Rp 6.045.000 — benar**. (Catatan minor: di giliran 1 SEBELUM langsung menganggap konveksi pasti masuk KLU lampiran; kalimat "(selama di bulan berjalan tidak melebihi 10 juta)" tidak tepat—syarat dinilai dari bruto Januari.)
- SESUDAH giliran 1: bertanya PTKP + konfirmasi sektor/KLU sesuai aturan skill — **benar dan aman**. Giliran 2: "Gaji bersih yang dia terima: **Rp 6.000.000 (utuh)**" — **SALAH**; DTP tunai Rp 45.000 tidak disebut sebagai tambahan yang wajib dibayarkan ke pegawai. Pemilik yang mengikuti jawaban ini kurang membayar Rp 45.000/bulan ke pegawai dan fasilitas DTP-nya tidak dijalankan dengan benar.

### Skor
| | Skor | Alasan |
|---|---:|---|
| SEBELUM | 8 | Jawaban akhir benar (Rp 6.045.000) dan langkah administrasi DTP berguna. Minus: giliran 1 mengasumsikan konveksi pasti eligible, tanpa disclaimer, ada satu kalimat syarat yang keliru. |
| SESUDAH | 6 | Gerbang konfirmasi sektor/KLU sangat baik, angka PPh 21 benar, disclaimer ada. Tetapi kesalahan fakta pada uang yang diterima pegawai (DTP harus dibayar tunai) — justru pertanyaan inti pengguna. |

Skill terpakai: Ya (SKILL.md dibaca; giliran 2 `scripts/pph21.py` dijalankan).

## Ringkasan
| Skenario | SEBELUM | SESUDAH |
|---|---:|---:|
| 1. Setahun K/1 + THR | 8 | 9 |
| 2. DTP konveksi (info kurang) | 8 | 6 |
| **Rata-rata** | **8,0** | **7,5** |

**VERDIK: BELUM** — sesudah < 8 dan ada kesalahan fakta (take home pay pegawai penerima DTP).

**Cacat untuk pembuat:**
1. *Take home DTP salah.* Bukti: skenario 2 giliran 2 SESUDAH "Gaji bersih yang dia terima: Rp 6.000.000 (utuh)", padahal PMK 105/2025 (dan `references/regulasi.md` baris 20) mewajibkan DTP dibayar tunai → Rp 6.045.000. Saran: di Format output & Checklist SKILL.md tambahkan baris wajib "Diterima pegawai = bruto − potongan + PPh 21 DTP tunai (bila DTP)"; buat script mencetak baris "Uang yang diterima pegawai" saat `--dtp`, dan dukung `--dtp` di subperintah `bulan` (sekarang hanya `setahun`; `bulan --dtp` ditolak "unrecognized arguments").
2. *Nilai tambah tipis di kasus normal.* Bukti: skenario 1 SEBELUM sudah benar semua (model mencari tabel TER di pajak.go.id). Pembeda skill ada di konsistensi, disclaimer, gerbang DTP — jangan jual dengan klaim "AI biasa salah hitung" untuk kasus sederhana.

**Cuplikan jualan:** (tahan sampai cacat DTP diperbaiki) — kandidat setelah revisi: "Sebelum menghitung insentif PPh 21 DTP 2026, bot menanyakan dulu sektor & KLU usaha Anda — tidak asal menganggap Anda berhak."


## Uji ulang 2026-10-01

**Penguji:** agent penguji independen Komunitech (bukan pembuat; skill hanya dibaca). **Versi diuji:** pph21-ter 1.0.4.
**Cara:** OpenClaw lokal (`openclaw agent --local`), model router Komunitech `claude-sonnet-5`, TZ Asia/Jakarta. Home **terisolasi** per sisi (mount namespace: agent hanya melihat home-nya; `pip install` hanya bisa masuk ke home uji, pustaka Python sistem read-only). SEBELUM = home tanpa skill (`rk-pph21-ter`), SESUDAH = home berisi skill ini saja (`r-pph21-ter`); kedua sisi dijalankan **ulang** (sisi SEBELUM uji pertama bisa tercemar), dibuat ulang bersih per skenario; pesan **sama persis** dengan uji pertama, balasan lanjutan identik di kedua sisi. Angka diverifikasi independen dengan Python; fakta aturan dicek sendiri.

### Skenario 1 — Normal: PPh 21 setahun K/1 + THR Maret (pesan sama persis)

**SEBELUM (tanpa skill)** — tools: tool_search, web_fetch, tool_call

~~~~text
Oke Pak, saya hitung pakai skema **TER (Tarif Efektif Rata-rata)** sesuai PP 58/2023 & PMK 168/2023 — ini aturan yang berlaku sejak 2024 dan masih dipakai 2026.

**Data karyawan:**
- Status K/1 (kawin, 1 tanggungan) → PTKP setahun = Rp 63.000.000 → masuk kategori **TER B**
- Gaji tetap Rp 8.500.000/bulan (Jan–Des 2026)
- THR Rp 8.500.000 cair Maret
- Potongan BPJS TK: JHT 2% + JP 1% dari gaji pokok (ini pengurang penghasilan, bukan penambah)

## Cara kerja TER
Untuk Januari–November, PPh 21 dihitung simpel: **penghasilan bruto bulanan × tarif TER sesuai tabel kategori B** (tidak dikurangi biaya jabatan/iuran dulu). Di Desember baru dihitung ulang total setahun pakai tarif progresif Pasal 17, dikurangi apa yang sudah dipotong Jan–Nov.

## Rincian per bulan (2026)

| Bulan | Penghasilan Bruto | Tarif TER B | PPh 21 |
|---|---|---|---|
| Jan | 8.500.000 | 1% | 85.000 |
| Feb | 8.500.000 | 1% | 85.000 |
| Mar | 17.000.000 (gaji+THR) | 7% | 1.190.000 |
| Apr | 8.500.000 | 1% | 85.000 |
| Mei | 8.500.000 | 1% | 85.000 |
| Jun | 8.500.000 | 1% | 85.000 |
| Jul | 8.500.000 | 1% | 85.000 |
| Agu | 8.500.000 | 1% | 85.000 |
| Sep | 8.500.000 | 1% | 85.000 |
| Okt | 8.500.000 | 1% | 85.000 |
| Nov | 8.500.000 | 1% | 85.000 |
| **Total Jan–Nov** | | | **2.040.000** |
| **Des** | (rekonsiliasi tahunan) | — | **–94.250** |

## Desember: kenapa beda sendiri

Desember dihitung ulang penuh setahun, bukan pakai tarif TER lagi:

1. **Bruto setahun** = (8.500.000 × 12) + THR 8.500.000 = **Rp 110.500.000**
2. **Pengurang:**
   - Biaya jabatan 5% × bruto = 5.525.000 (di bawah plafon 6 juta/tahun, jadi dipakai segini)
   - Iuran JHT 2% × gaji pokok setahun (102 juta) = 2.040.000
   - Iuran JP 1% × gaji pokok setahun = 1.020.000
   - Total pengurang = **8.585.000**
3. **Penghasilan neto setahun** = 110.500.000 − 8.585.000 = **101.915.000**
4. **PKP** = 101.915.000 − PTKP 63.000.000 = **38.915.000**
5. **PPh 21 setahun (tarif Pasal 17)** = 5% × 38.915.000 = **Rp 1.945.750**
6. **PPh Desember** = PPh setahun − PPh yang sudah dipotong Jan–Nov = 1.945.750 − 2.040.000 = **−94.250**

Artinya di Desember **tidak ada potongan PPh 21** — malah ada **lebih bayar Rp 94.250** yang harus Bapak kembalikan ke karyawan (take-home Desember-nya jadi lebih gede dari biasanya).

**Kenapa bisa minus?** Karena selama Jan–Nov, TER langsung dikenakan ke gaji bruto tanpa memperhitungkan biaya jabatan dan iuran JHT/JP. Pengurang-pengurang ini baru "dicairkan" manfaatnya di rekonsiliasi Desember, jadi total pajak riil setahun (1.945.750) ternyata lebih kecil dari yang sudah ditarik tiap bulan (2.040.000) — selisihnya dikembalikan.

**Total PPh 21 karyawan ini untuk 2026: Rp 1.945.750** (sesuai bukti potong 1721-A1 nanti).

Catatan: ini asumsi JHT/JP dihitung dari gaji pokok 8,5 juta (bukan dari THR), dan tidak ada komponen lain (lembur, tunjangan tidak tetap, dll). Kalau ada komponen lain yang belum disebut, kabari saya biar dihitung ulang.
~~~~

**SESUDAH (dengan skill)** — tools: read, exec (`scripts/pph21.py`)

~~~~text
Berikut hitungan PPh 21 karyawan Bapak untuk tahun 2026 (status K/1, gaji tetap Rp 8.500.000/bulan, TER kategori B):

**PPh 21 2026 — status K/1 (TER kategori B)**

| Bulan | Penghasilan bruto | Tarif TER | PPh 21 dipotong |
|---|---:|---:|---:|
| Januari | Rp 8.500.000 | 1% | Rp 85.000 |
| Februari | Rp 8.500.000 | 1% | Rp 85.000 |
| Maret (+THR) | Rp 17.000.000 | 7% | Rp 1.190.000 |
| April | Rp 8.500.000 | 1% | Rp 85.000 |
| Mei | Rp 8.500.000 | 1% | Rp 85.000 |
| Juni | Rp 8.500.000 | 1% | Rp 85.000 |
| Juli | Rp 8.500.000 | 1% | Rp 85.000 |
| Agustus | Rp 8.500.000 | 1% | Rp 85.000 |
| September | Rp 8.500.000 | 1% | Rp 85.000 |
| Oktober | Rp 8.500.000 | 1% | Rp 85.000 |
| November | Rp 8.500.000 | 1% | Rp 85.000 |
| Desember | Rp 8.500.000 | Pasal 17 (hitung ulang) | **Rp 94.250 lebih potong** (dikembalikan) |
| **Total** | **Rp 110.500.000** | | **Rp 1.945.750** |

**Kenapa Desember beda sendiri?**
Januari–November pakai tarif TER langsung (persentase dari tabel resmi × gaji bulan itu). Tapi Desember (atau bulan terakhir kerja) wajib dihitung ulang pakai tarif progresif Pasal 17 atas penghasilan setahun penuh — ini aturan baku, bukan kesalahan:

- Bruto setahun: Rp 110.500.000 (termasuk THR Maret)
- Biaya jabatan 5%, maks Rp 6 juta/tahun: Rp 5.525.000
- Iuran JHT 2% + JP 1% karyawan (Rp 255.000/bulan × 12): Rp 3.060.000
- Penghasilan neto setahun: Rp 101.915.000
- PTKP K/1: Rp 63.000.000
- PKP: Rp 38.915.000
- PPh 21 setahun (5% × PKP, karena masih di lapisan pertama): **Rp 1.945.750**
- Sudah dipotong Jan–Nov: Rp 2.040.000
- Selisih: **lebih potong Rp 94.250** → ini wajib Bapak kembalikan ke karyawan paling lambat akhir Januari 2027 (bukan dipotong lagi)

Jadi logikanya: TER bulanan itu cuma perkiraan cepat; di akhir tahun (atau saat karyawan resign) dicocokkan ulang pakai tarif resmi UU PPh atas total setahun. Karena perkiraan Jan–Nov sedikit lebih besar dari yang seharusnya, di Desember jadi "minus" alias lebih bayar — itu sebabnya angkanya beda sendiri dan malah negatif, bukan tambah potong.

**Ringkasan setahun:**
- Total bruto: Rp 110.500.000
- Total PPh 21 terutang (kredit pajak di SPT Tahunan karyawan): Rp 1.945.750
- Kelebihan potong yang wajib dikembalikan: Rp 94.250

Asumsi yang saya pakai:
- JHT+JP karyawan = 3% × Rp 8.500.000 = Rp 255.000/bulan, konstan sepanjang tahun.
- THR Rp 8.500.000 masuk sebagai tambahan di bulan Maret.
- Tidak menghitung DTP (pajak ditanggung pemerintah) karena bengkel motor bukan termasuk sektor yang disebut di Lampiran A PMK 105/2025 (alas kaki, tekstil & pakaian jadi, furnitur, kulit, pariwisata) — kalau ternyata usaha Bapak punya KLU lain yang masuk daftar itu, kabari saya, nanti saya hitung ulang.

_Alat bantu hitung, bukan nasihat pajak resmi. Dasar: PP 58/2023, PMK 168/2023, UU HPP. Untuk kasus khusus, hubungi Kring Pajak 1500200 atau konsultan pajak._
~~~~

### Skenario 2 — DTP konveksi, info kurang (2 giliran, pesan sama persis)

**Giliran 1 — SEBELUM** — tools: tool_search, web_fetch, tool_call

~~~~text
Sudah saya cek aturan terbaru (PMK 105/2025) plus tabel TER PPh 21 resmi — ini ringkasannya:

**1. Berapa PPh 21-nya (tanpa insentif, hitungan normal)**
Gaji Rp6.000.000/bulan, metode TER (berlaku sejak 2024, masih sama di 2026):
- Kalau status karyawan TK/0, TK/1, atau K/0 (lajang tanpa tanggungan, lajang 1 tanggungan, atau kawin tanpa tanggungan) → masuk kategori TER A. Gaji Rp6 juta ada di bracket Rp5.950.001–Rp6.300.000 → tarif 0,75%.
  → PPh 21 = Rp6.000.000 × 0,75% = **Rp45.000/bulan**
- Kalau status TK/2, TK/3, K/1, atau K/2 → masuk kategori TER B. Bracket "s.d. Rp6.200.000" = tarif 0%.
  → PPh 21 = **Rp0** (gaji belum kena potong sama sekali)

Jadi tergantung status PTKP karyawan (kawin/belum, jumlah tanggungan). Kalau bisa kasih tahu statusnya, saya pastikan angka tepatnya.

**2. Soal pajak ditanggung pemerintah — bener!**
Ini namanya **PPh 21 DTP (Ditanggung Pemerintah)**, diperpanjang untuk sepanjang tahun 2026 (Januari–Desember) lewat **PMK 105/2025**. Jadi bukan cuma kabar angin.

Syaratnya (harus semua terpenuhi):
- Usaha konveksi Bapak/Ibu masuk kategori **tekstil dan pakaian jadi** (konveksi biasanya masuk sini) — tapi harus dicek **kode KLU** di NPWP perusahaan apakah memang terdaftar di lampiran PMK 105/2025. Ini wajib dicek, bukan otomatis semua usaha tekstil dapat.
- Gaji bruto tetap karyawan ≤ Rp10.000.000/bulan → karyawan Rp6 juta ini lolos.
- Karyawan punya NPWP atau NIK yang sudah terintegrasi sistem DJP.
- Karyawan tidak sedang dapat insentif PPh 21 DTP lain.

Kalau semua syarat terpenuhi: PPh 21 yang terutang (Rp45.000 atau Rp0 di atas) **dibayar tunai oleh negara**, bukan dipotong dari gaji karyawan. Artinya karyawan terima gaji full Rp6.000.000 tanpa potongan pajak.

Yang perlu Bapak/Ibu (sebagai pemberi kerja) lakukan:
- Cek KLU usaha di DJP Online, pastikan cocok dengan lampiran PMK 105/2025.
- Tetap buat bukti potong PPh 21 tiap bulan (meski nilainya "ditanggung pemerintah", bukan Rp0 begitu saja — harus dicatat insentifnya).
- Lapor pemanfaatan via SPT Masa PPh 21/26 di Coretax tiap bulan, karena kalau telat lapor, insentifnya bisa hangus dan Bapak/Ibu malah wajib setor sendiri.

Kalau mau, saya bisa bantu cek daftar KLU resmi di lampiran PMK 105/2025 untuk pastikan usaha konveksinya termasuk — tinggal kasih tahu KBLI/KLU usahanya atau saya carikan daftarnya.
~~~~

**Giliran 1 — SESUDAH** — tools: read, ls

~~~~text
Supaya PPh 21-nya pas, saya perlu 2 info dulu (soalnya mempengaruhi tarif dan kemungkinan dapat subsidi pajak):

1. Status PTKP karyawan per 1 Januari 2026 — lajang (TK/0), sudah kawin tanpa tanggungan (K/0), kawin + jumlah tanggungan (K/1, K/2, K/3), dst?
2. Soal kabar "pajak ditanggung pemerintah" itu benar ada — namanya **PPh 21 DTP** (PMK 105/2025), tapi **khusus** untuk pekerja di sektor padat karya tertentu (alas kaki, tekstil & pakaian jadi, furnitur, kulit & barang kulit, pariwisata) dengan gaji tetap ≤ Rp 10 juta/bulan, dan KLU usahanya tercantum di lampiran aturan itu. Konveksi Anda termasuk tekstil/pakaian jadi, dan gaji Rp 6 juta di bawah batas — jadi berpotensi dapat. Apakah KLU usaha konveksi Anda resmi terdaftar di salah satu sektor itu (alas kaki/tekstil & pakaian jadi/furnitur/kulit/pariwisata)?

Begitu dikonfirmasi, saya langsung hitung PPh 21 Oktober-nya (dengan atau tanpa DTP).
~~~~

**Giliran 2 — SEBELUM** — tools: —

~~~~text
Oke, dengan data ini perhitungannya jadi jelas:

**Status karyawan**
Bujang, belum ada tanggungan = **TK/0** → masuk **kategori TER A**.

**Hitung PPh 21 terutang Oktober 2026**
- Gaji bruto Rp6.000.000 (tidak ada BPJS, jadi dasar pemotongan = gaji bruto penuh)
- Masuk bracket TER A: **Rp5.950.001 – Rp6.300.000 → tarif 0,75%**
- PPh 21 terutang = Rp6.000.000 × 0,75% = **Rp45.000**

**Karena insentif PPh 21 DTP berlaku (KLU 14111 masuk lampiran PMK 105/2025, gaji ≤Rp10 juta sejak Januari):**
- PPh 21 Rp45.000 itu **ditanggung pemerintah**, bukan dipotong dari gaji karyawan.
- Jadi **Oktober ini Bapak/Ibu potong Rp0** dari gaji karyawan untuk PPh 21.
- **Karyawan terima bersih: Rp6.000.000 penuh** (karena tidak ada potongan BPJS atau lainnya).

**Yang tetap wajib Bapak/Ibu lakukan sebagai pemberi kerja:**
1. Tetap **buat bukti potong PPh 21** senilai Rp45.000 per bulan (dicatat sebagai PPh 21 DTP, bukan dihilangkan begitu saja).
2. **Lapor SPT Masa PPh 21/26 via Coretax** setiap bulan (Jan–Okt dst), tepat waktu. Kalau telat lapor, insentif bisa dianggap tidak dimanfaatkan dan Bapak/Ibu wajib setor sendiri PPh 21 yang seharusnya ditanggung negara.
3. Pastikan karyawan **punya NPWP atau NIK yang sudah terintegrasi DJP** — ini syarat kumulatif terakhir yang belum dikonfirmasi. Kalau belum terintegrasi, insentif DTP tidak berlaku dan Rp45.000 itu harus dipotong beneran dari gajinya.

Satu hal untuk dicek: karena gaji sudah Rp6 juta sejak Januari dan ini syaratnya "dilihat pada Masa Pajak Januari 2026", pastikan laporan SPT Masa dari Januari sampai sekarang sudah konsisten dilaporkan sebagai pemanfaatan DTP — supaya tidak ada bulan yang "lolos" tanpa pelaporan.
~~~~

**Giliran 2 — SESUDAH** — tools: exec (`scripts/pph21.py`)

~~~~text
**PPh 21 Oktober 2026 — Karyawan konveksi, status TK/0 (bujang, tanpa tanggungan), TER kategori A**

| Komponen | Nilai |
|---|---|
| Gaji bruto sebulan | Rp 6.000.000 |
| Tarif TER (kategori A, lapisan Rp 5.950.000–6.300.000) | 0,75% |
| PPh 21 terutang | Rp 45.000 |

**Karena KLU 14111 (pakaian jadi) masuk Lampiran A PMK 105/2025 dan gaji ≤ Rp 10 juta → kena PPh 21 DTP (ditanggung pemerintah):**

- **PPh 21 dipotong dari gaji: Rp 0** — jadi Anda TIDAK memotong apa pun dari gaji Rp 6 juta-nya.
- **PPh 21 DTP yang wajib Anda bayar tunai ke dia bersama gaji: Rp 45.000**
- **Uang yang diterima karyawan: Rp 6.045.000** (Rp 6.000.000 gaji + Rp 45.000 DTP tunai)

Jadi: betul, kabar yang dia dengar itu benar — tapi bukan berarti "tidak kena pajak", melainkan pajaknya dibayar pemerintah lewat Anda, dan nilainya (Rp 45.000) tetap wajib diserahkan tunai ke dia di luar gaji pokok, bukan masuk kantong perusahaan.

⚠️ Catatan penting:
1. Syarat batas gaji (≤Rp 10 juta) seharusnya dicek dari gaji + tunjangan tetap bulan **Januari 2026** (bulan pertama tahun ini), bukan Oktober. Karena Anda bilang gajinya Rp 6 juta sejak Januari dan tidak ada tunjangan/BPJS lain, syaratnya terpenuhi.
2. Wajib tetap dibuatkan bukti potong dan dilaporkan di SPT Masa PPh 21/26 meski Rp 0 yang dipotong.
3. Ini untuk masa Januari–November. Desember dihitung ulang pakai tarif Pasal 17 (beri tahu saya nanti kalau mau dihitungkan).

_Alat bantu hitung, bukan nasihat pajak final — dasar PP 58/2023, PMK 168/2023, PMK 105/2025. Kasus khusus hubungi Kring Pajak 1500200 atau konsultan pajak Anda._
~~~~

### Verifikasi (Python independen + aturan)
- S1: TER B 8,5 jt → 1% = 85.000; Maret 17 jt → 7% = 1.190.000; Jan–Nov 2.040.000. Setahun: bruto 110.500.000 − BJ 5.525.000 − iuran 3.060.000 = neto 101.915.000 − PTKP K/1 63.000.000 = PKP 38.915.000 × 5% = **1.945.750** → Desember **lebih potong 94.250**. Kedua sisi **benar**.
- S2: TK/0 → TER A, 6 jt → 0,75% = **45.000**. PMK 105/2025 Pasal 5 (dicek: pajak.go.id, ortax.org, ikpi.or.id): PPh 21 DTP **dibayarkan tunai** oleh pemberi kerja kepada pegawai saat pembayaran penghasilan dan tidak dihitung sebagai penghasilan kena pajak → pegawai menerima 6.000.000 + 45.000 = **Rp 6.045.000**.
  - SESUDAH giliran 2: "PPh 21 dipotong Rp 0 · DTP tunai Rp 45.000 · **diterima Rp 6.045.000**" — **benar**; syarat batas Rp 10 jt dinilai dari bruto Januari — benar.
  - SEBELUM (dijalankan ulang): giliran 1 "karyawan terima gaji full Rp6.000.000", "dibayar tunai oleh negara"; giliran 2 "**Karyawan terima bersih: Rp6.000.000 penuh**" — **SALAH** (kurang Rp 45.000/bulan). Uji pertama sisi SEBELUM yang benar (Rp 6.045.000) ternyata tidak stabil.

### Status cacat lama
1. Take home DTP salah → **TERATASI** (script `bulan --dtp` dipakai, tiga baris wajib muncul).
2. Nilai tambah tipis di kasus normal → **masih berlaku** untuk S1 (tanpa skill juga benar); pembeda nyata ada di DTP.
**Regresi:** tidak ditemukan (S1 identik benar, disclaimer & dasar aturan tetap ada, istilah DTP/TER dijelaskan).

### Skor
| Skenario | SEBELUM | SESUDAH | Alasan |
|---|---:|---:|---|
| 1. Setahun K/1 + THR | 8 | 9 | Angka sama benar; SESUDAH + batas waktu pengembalian, cek sektor DTP, disclaimer. |
| 2. DTP konveksi | 5 | 9,5 | SEBELUM salah di pertanyaan inti (uang diterima pegawai); SESUDAH bertanya dulu, lalu angka & kewajiban tunai benar. |
| **Rata-rata** | **6,5** | **9,25** | |

**VERDIK: LULUS** — sesudah ≥ 8, jelas lebih baik dari sebelum, tanpa kesalahan fakta/angka.

**Cuplikan jualan (jujur):** "Karyawan konveksi gaji Rp6 juta penerima PPh 21 DTP 2026: AI biasa bilang dia terima Rp6.000.000 'utuh'. Dengan skill: dipotong Rp0, DTP Rp45.000 wajib dibayar tunai, **diterima Rp6.045.000** — sesuai PMK 105/2025 Pasal 5." (Untuk kasus normal tanpa DTP, jangan klaim AI biasa salah hitung.)


---

## Uji ulang v1.0.5 (DTP) — 2026-10-05

Penguji independen baru (bukan pembuat, tidak mengubah skill). Tujuan: memastikan cacat no. 1 gelombang 7 (`koordinasi/telegram-gelombang-7-2026-10-05.md`: DENGAN menulis "diterima Rp6.045.000") sudah hilang di perilaku bot, bukan hanya di script.

**Cara uji:** OpenClaw 2026.9.8 lokal (`openclaw agent --local`), model router Komunitech (`komunitech`, sama dengan bot), home bersih per skenario/run. SEBELUM = home tanpa skill (`uji.sh`); SESUDAH = home hanya berisi `pph21-ter` 1.0.5. Skenario 1 SESUDAH dijalankan **2× dengan `uji-tg.sh`** (konteks kanal Telegram, tanpa kirim), run A dilanjutkan 1 giliran jawaban pengguna (KLU). Skenario 2 dengan `uji.sh` 1× per sisi. Verifikasi angka: Python `Decimal` milik penguji (`scratchpad/verif-pph21-v105.py`, tabel TER diketik dari PP 58/2023, tidak mengimpor script skill).

### Skenario 1 — pesan gelombang 7 persis (DTP konveksi)
Pesan: "Karyawan konveksi saya gajinya Rp6.000.000 sebulan, status TK/0. Apa dia dapat insentif PPh 21 DTP tahun 2026? Berapa PPh 21 bulan Oktober dan uang yang dia terima?"

**SEBELUM** (`uji.sh`, tools: tool_search, web_fetch; 223 dtk)
~~~~text
Saya coba cek aturan terbaru dulu, tapi mesin pencari yang saya pakai lagi bermasalah (hasilnya nggak relevan/rusak), jadi saya nggak bisa memastikan 100% status insentif PPh 21 DTP untuk tahun pajak 2026 secara live. Berikut yang saya tahu + hitungan pastinya:

**Soal insentif PPh 21 DTP:**
Program "PPh 21 Ditanggung Pemerintah" untuk sektor industri padat karya (tekstil, garmen/konveksi, kulit, alas kaki, furniture) pernah berlaku untuk **tahun pajak 2025** (lewat PMK 10/2025), dengan syarat utama:
- Gaji bruto karyawan ≤ Rp10.000.000/bulan
- Perusahaan masuk klasifikasi KLU industri padat karya tertentu
- Karyawan punya NPWP/NIK terintegrasi
- Perusahaan lapor via SPT Masa PPh 21 dengan kode objek pajak DTP (biasanya lewat Coretax)

Gaji karyawan Anda (Rp6.000.000, TK/0) **memenuhi syarat batas gaji** dan konveksi **termasuk sektor padat karya** yang biasanya masuk daftar. Tapi saya **belum bisa konfirmasi apakah program ini diperpanjang resmi untuk tahun pajak 2026** — ini perlu dicek langsung karena programnya biasanya diatur per-PMK dengan periode terbatas (misal Jan-Jun saja). Saran saya: cek ke kantor pajak/konsultan pajak Anda atau akun Coretax perusahaan, cari PMK terbaru soal "PPh 21 DTP industri padat karya 2026" — kalau statusnya aktif, biasanya ada pengumuman resmi dari DJP/Kemenkeu dan fitur khusus di Coretax untuk lapor DTP.

**Hitungan PPh 21 Oktober 2026 (tarif normal, metode TER sesuai PP 58/2023):**

Gaji Rp6.000.000, status TK/0 → masuk kategori **TER A**, bracket gaji >5.950.000 s.d. 6.300.000 → tarif efektif **0,75%**.

PPh 21 = 6.000.000 × 0,75% = **Rp45.000**

**Uang yang diterima karyawan bulan Oktober:**

| Skenario | PPh 21 | Take-home pay |
|---|---|---|
| **Tanpa insentif DTP** (dipotong normal) | Rp45.000 | Rp5.955.000 |
| **Dengan insentif DTP aktif** (pajak ditanggung negara) | Rp45.000 (dibayar pemerintah, tidak dipotong dari gaji) | **Rp6.000.000 full** |

Jadi bedanya cuma Rp45.000/bulan — kecil, tapi kalau DTP aktif, karyawan terima gaji full tanpa potongan pajak, dan perusahaan tetap wajib lapor SPT Masa PPh 21 (nihil dipotong, tapi dilaporkan DTP).

Kalau Anda mau, saya bisa bantu cek ulang begitu akses pencarian saya normal lagi, atau bantu susun pertanyaan untuk ditanyakan ke AR (Account Representative) pajak Anda soal status 2026 ini.
~~~~

**SESUDAH run A** (`uji-tg.sh`, tools: read, exec `scripts/pph21.py`; 100 dtk)
~~~~text
Perhitungan dasar sudah saya jalankan. Untuk PPh 21 Oktober 2026-nya begini:

**PPh 21 Oktober 2026 — status TK/0 (TER kategori A)**
- Penghasilan bruto: Rp 6.000.000
- Tarif TER: 0,75% (bruto di atas Rp 5.950.000 s.d. Rp 6.300.000)
- **PPh 21 dipotong: Rp 45.000**

Soal insentif **PPh 21 DTP 2026** (ditanggung pemerintah, PMK 105/2025), saya belum bisa pastikan karena ini tidak otomatis untuk semua UMKM — hanya berlaku untuk perusahaan di **sektor tertentu**: alas kaki, tekstil & pakaian jadi, furnitur, kulit & barang kulit, atau pariwisata, **dan** kode KLU utama usaha Anda harus tercantum di Lampiran A PMK 105/2025.

Pertanyaannya: **apakah usaha konveksi Anda terdaftar dengan KLU yang masuk kategori tekstil/pakaian jadi di Lampiran A PMK 105/2025?** (Konveksi biasanya cocok, tapi saya tidak mau menebak KLU resminya.)

Kalau jawabannya **ya**, hasilnya jadi:
- PPh 21 tetap dipotong Rp 45.000 dari slip
- DTP dibayar tunai Rp 45.000 (nilai sama) ke karyawan bareng gaji
- Setoran ke negara: Rp 0
- **Uang yang diterima karyawan: Rp 6.000.000 (gaji penuh)**

Kalau jawabannya **tidak/tidak tahu KLU-nya**, maka tidak dapat DTP, dan:
- **Uang yang diterima karyawan Oktober: Rp 5.955.000** (Rp 6.000.000 − Rp 45.000 PPh 21)

Catatan: ini perhitungan sebelum potongan lain (misalnya iuran BPJS bagian karyawan), dan belum dicocokkan dengan Coretax. Alat bantu hitung, bukan nasihat pajak — kasus khusus bisa cek Kring Pajak 1500200.

Konfirmasi KLU usahanya, saya hitung ulang pakai angka DTP-nya kalau memang masuk kategori.
~~~~

Lanjutan run A — pengguna: "Ya, KLU kami 14111 (pakaian jadi konveksi), ada di Lampiran A." (23 dtk)
~~~~text
**Ya, karyawan Anda dapat insentif PPh 21 DTP 2026** — KLU 14111 (industri pakaian jadi) termasuk sektor tekstil & pakaian jadi di Lampiran A PMK 105/2025.

**PPh 21 Oktober 2026 — status TK/0 (TER kategori A)**
- Penghasilan bruto: Rp 6.000.000
- Tarif TER: 0,75% (bruto di atas Rp 5.950.000 s.d. Rp 6.300.000)
- **PPh 21 dipotong dari gaji: Rp 45.000**
- **PPh 21 DTP dibayar tunai ke karyawan: Rp 45.000** (nilai sama, PMK 105/2025 Pasal 5)
- **Setoran ke negara: Rp 0** (tetap wajib dibuat bukti potong & dilaporkan di SPT Masa)
- **Uang yang diterima karyawan: Rp 6.000.000** (gaji penuh — bukan Rp 6.045.000)

Jadi secara praktis: karyawan tetap menerima gaji penuh Rp 6.000.000 tanpa potongan pajak, perusahaan Anda tidak perlu menyetor PPh 21-nya ke kas negara, tapi **wajib tetap membuat bukti potong dan melaporkannya di SPT Masa PPh 21/26** — paling lambat **31 Januari 2027**. Kalau lewat batas itu, insentif gugur dan PPh yang dipotong wajib disetor sendiri.

⚠️ Catatan penting: syarat batas gaji ≤ Rp 10 juta untuk DTP seharusnya dicek dari **gaji + tunjangan tetap bulan Januari 2026** (atau bulan pertama kerja tahun ini), bukan bulan Oktober. Kalau gaji karyawan ini sama tiap bulan (Rp 6 juta), aman — tapi kalau Januari berbeda, kabari saya angkanya biar saya pastikan ulang.

_Alat bantu hitung, bukan nasihat pajak resmi. Dasar: PP 58/2023, PMK 168/2023, PMK 105/2025. Kasus khusus: Kring Pajak 1500200 atau konsultan pajak._
~~~~

**SESUDAH run B** (`uji-tg.sh`, home baru, tools: read, exec; 38 dtk)
~~~~text
**PPh 21 Oktober 2026 — Karyawan Konveksi, status TK/0 (TER kategori A)**

Gaji bruto sebulan: Rp 6.000.000 → tarif TER 0,75% (bruto Rp5.950.000–Rp6.300.000)

**Soal insentif DTP — perlu dikonfirmasi dulu:**
Konveksi *mungkin* masuk kategori tekstil & pakaian jadi yang berhak PPh 21 DTP 2026 (PMK 105/2025), tapi syaratnya bukan sekadar "usaha konveksi" — harus **KLU (Klasifikasi Lapangan Usaha) utama perusahaan yang terdaftar di pajak** memang tercantum di Lampiran A PMK 105/2025 (kategori alas kaki, tekstil & pakaian jadi, furnitur, kulit & barang kulit, atau pariwisata). Mohon konfirmasi: apakah KLU usaha Anda sudah dicek dan cocok dengan lampiran itu?

Sambil menunggu konfirmasi, berikut dua skenario:

**① Jika TIDAK dapat DTP (skenario normal/default):**
- PPh 21 dipotong: **Rp 45.000** (0,75% × Rp6.000.000)
- Disetor ke negara: Rp 45.000
- **Uang diterima karyawan: Rp 5.955.000**

**② Jika DAPAT DTP (KLU cocok & terdaftar):**
- PPh 21 dipotong dari gaji: Rp 45.000
- PPh 21 DTP dibayar tunai kembali ke pegawai: Rp 45.000 (nilai sama)
- Setoran ke negara: Rp 0 (tapi tetap wajib dibuat bukti potong & dilapor di SPT Masa)
- **Uang diterima karyawan: Rp 6.000.000** (gaji penuh, bukan gaji + Rp45.000)

Asumsi: tidak ada potongan iuran BPJS TK/pensiun karyawan dan tidak ada premi perusahaan yang ditambahkan ke bruto — beri tahu saya jika ada, agar saya hitung ulang.

⚠️ Alat bantu hitung, bukan nasihat pajak resmi. Untuk memastikan status KLU, bisa cek di NPWP perusahaan/profil Coretax atau hubungi Kring Pajak 1500200.
~~~~

**Verifikasi:** TER A (TK/0), baris "di atas Rp5.950.000 s.d. Rp6.300.000" = 0,75% → 0,75% × 6.000.000 = **Rp45.000**. Tanpa DTP diterima 6.000.000 − 45.000 = **Rp5.955.000**. Dengan DTP (PMK 105/2025 Pasal 2 ayat 1, Pasal 5, Lampiran B): 6.000.000 − 45.000 + 45.000 = **Rp6.000.000**, setoran Rp0.
- SESUDAH A, A-lanjutan, B: semua angka **benar**; "Rp6.045.000" tidak muncul sebagai jawaban (A-lanjutan & B justru menegaskan "bukan gaji + DTP"). Keduanya meminta konfirmasi KLU dan memberi dua skenario. Syarat bruto Januari 2026 ≤ Rp10 jt disebut di A-lanjutan (tidak di jawaban pertama A/B), batas lapor 31 Januari 2027 di A-lanjutan.
- SEBELUM: angka benar (5.955.000 / 6.000.000), tetapi **tidak tahu dasar 2026** (menyebut PMK 10/2025 untuk 2025, "belum bisa konfirmasi diperpanjang 2026"), dan menulis DTP "tidak dipotong dari gaji" (mekanisme tidak persis PMK 105/2025: dipotong lalu dibayar tunai). Tidak minta konfirmasi KLU.

### Skenario 2 — Desember K/1 + THR Maret (jebakan lebih potong)
Pesan: "Pegawai saya status K/1, gajinya Rp9.500.000 per bulan dari Januari sampai Desember 2026, terus bulan Maret dapat THR Rp9.500.000. Tidak ada potongan BPJS. Berapa PPh 21 yang harus dipotong bulan Desember?"

**SEBELUM** (`uji.sh`, tools: process, exec, read + 12 panggilan web; **691 dtk ≈ 11,5 menit**)
~~~~text
Saya sudah dapat sumber resminya langsung dari JDIH Kemenkeu (PP 58/2023 dan PMK 168/2023), jadi perhitungan di bawah ini memakai tarif resmi, bukan perkiraan.

**Cara hitung PPh 21 Desember (skema TER, berlaku sejak 2024):**
Bulan Desember = Masa Pajak Terakhir → PPh 21 dihitung **ulang disetahunkan** memakai tarif Pasal 17 (progresif), lalu dikurangi total PPh 21 yang sudah dipotong Januari–November (dengan TER bulanan Kategori B, karena K/1).

**1. Penghasilan bruto setahun**
- Gaji 12 bulan × Rp9.500.000 = Rp114.000.000
- THR (Maret) = Rp9.500.000
- **Total = Rp123.500.000**

**2. Biaya jabatan**
5% × Rp123.500.000 = Rp6.175.000 → dibatasi maks Rp500.000/bulan × 12 = **Rp6.000.000**

**3. Penghasilan neto setahun**
Rp123.500.000 − Rp6.000.000 = **Rp117.500.000**

**4. PTKP K/1**
54.000.000 (WP sendiri) + 4.500.000 (kawin) + 4.500.000 (1 anak) = **Rp63.000.000**

**5. PKP setahun**
Rp117.500.000 − Rp63.000.000 = **Rp54.500.000**

**6. PPh 21 terutang setahun** (tarif Pasal 17: 5% utk lapisan 0–60jt)
5% × Rp54.500.000 = **Rp2.725.000**

**7. PPh 21 yang sudah dipotong Jan–Nov** (TER bulanan Kategori B, dari PP 58/2023):
- Rp9.500.000 masuk rentang "di atas Rp9.200.000 s.d. Rp10.750.000" → tarif **1,5%**
- Jan, Feb, Apr–Nov (10 bulan normal): 1,5% × 9.500.000 = Rp142.500/bulan × 10 = Rp1.425.000
- Maret (gaji + THR = Rp19.000.000) masuk rentang "di atas Rp18.450.000 s.d. Rp21.850.000" → tarif **8%**: 8% × 19.000.000 = Rp1.520.000

Total Jan–Nov = Rp1.425.000 + Rp1.520.000 = **Rp2.945.000**

**8. PPh 21 Desember = PPh setahun − PPh Jan-Nov**
Rp2.725.000 − Rp2.945.000 = **−Rp220.000**

## Hasil
PPh 21 yang harus **dipotong** bulan Desember = **Rp0** (nihil).

Justru terjadi **lebih potong Rp220.000** selama Jan–Nov (karena THR di bulan Maret kena TER 8% jauh lebih tinggi dari tarif efektif riilnya setahun). Sesuai PMK 168/2023, kelebihan ini **dikembalikan ke pegawai** oleh perusahaan pada Masa Pajak Desember, bukan dipotong lagi — jadi slip gaji Desember pegawai ini malah menerima pengembalian PPh 21 sebesar Rp220.000, bukan potongan.
~~~~

**SESUDAH** (`uji.sh`, tools: read, exec `scripts/pph21.py`; 38 dtk)
~~~~text
**PPh 21 Desember 2026 — status K/1, gaji Rp9.500.000/bulan + THR Rp9.500.000 di Maret (TER kategori B)**

Hasil: **PPh 21 bulan Desember = Rp 0, dan ada lebih potong Rp 220.000 yang wajib dikembalikan ke pegawai** (bukan dipotong lagi). Penjelasan:

| Bulan | Bruto | Tarif/Metode | PPh 21 |
|---|---:|---:|---:|
| Jan, Feb, Apr–Nov (10 bulan) | Rp 9.500.000 | TER 1,5% | Rp 142.500/bulan |
| Maret (+ THR) | Rp 19.000.000 | TER 8% | Rp 1.520.000 |
| **Total dipotong Jan–Nov** | | | **Rp 2.945.000** |

**Hitung ulang Masa Pajak Terakhir (Desember) — pakai Pasal 17, bukan TER:**
- Total bruto setahun: Rp 123.500.000 (12× gaji + THR)
- Biaya jabatan 5%, maks Rp 500.000 × 12 bulan: Rp 6.000.000
- Penghasilan neto setahun: Rp 117.500.000
- PTKP K/1: Rp 63.000.000
- PKP (dibulatkan ke bawah ke ribuan): Rp 54.500.000
- PPh 21 terutang setahun (5% × 54.500.000, masih di lapisan pertama): Rp 2.725.000
- Sudah dipotong Jan–Nov: Rp 2.945.000
- **PPh 21 Desember = Rp 2.725.000 − Rp 2.945.000 = −Rp 220.000** → kelebihan potong

Jadi di bulan Desember **tidak ada potongan** lagi, dan perusahaan wajib **mengembalikan Rp 220.000** ke pegawai tersebut, paling lambat akhir Januari 2027.

**Ringkasan setahun:**
- Total bruto: Rp 123.500.000
- Total PPh 21 terutang (jadi kredit pajak di SPT Tahunan pegawai): Rp 2.725.000
- Kelebihan potong yang dikembalikan: Rp 220.000

Asumsi yang dipakai: tidak ada iuran pensiun/BPJS karyawan yang dipotong (sesuai info Anda), tidak ada zakat lewat perusahaan, pegawai bekerja penuh 12 bulan.

_Alat bantu hitung, bukan nasihat pajak. Dasar: PP 58/2023, PMK 168/2023, UU HPP, berlaku per 23 September 2026. Kasus khusus → Kring Pajak 1500200 atau konsultan pajak._
~~~~

**Verifikasi (Decimal):** TER B 9.500.000 (di atas 9.200.000 s.d. 10.750.000) 1,5% = 142.500 × 10 = 1.425.000; Maret 19.000.000 (di atas 18.450.000 s.d. 21.850.000) 8% = 1.520.000; Jan–Nov **2.945.000**. Setahun: bruto 123.500.000 − biaya jabatan 6.000.000 (maks) = neto 117.500.000 − PTKP K/1 63.000.000 = PKP **54.500.000** × 5% = **2.725.000**. Desember = 2.725.000 − 2.945.000 = **−220.000** (lebih potong, dikembalikan; PMK 168/2023: paling lambat akhir bulan berikutnya). Kedua sisi **benar**. SEBELUM menulis pengembalian "pada Masa Pajak Desember" (kurang presisi) dan tanpa disclaimer; SESUDAH menyebut tenggat akhir Januari 2027, asumsi, dan disclaimer. SESUDAH tidak menyinggung DTP walau 2026 & gaji ≤ Rp10 jt (pengguna tidak bertanya; kekurangan kecil).

### Skor
| Skenario | SEBELUM | SESUDAH | Alasan |
|---|---:|---:|---|
| 1. DTP konveksi (Telegram) | 6 | 8,75 (A 8,5 · B 9) | SEBELUM angka benar tetapi tak tahu aturan 2026 & tak cek KLU; SESUDAH angka sesuai PMK 105/2025 di 2/2 run, cek KLU, 2 skenario, setoran Rp0 — A tanpa syarat bruto Januari di jawaban pertama. |
| 2. Desember K/1 + THR | 8,5 | 9 | Angka sama benar; SEBELUM 11,5 menit dengan 12 panggilan web (berisiko timeout di bot) & tenggat pengembalian kurang presisi; SESUDAH 38 dtk, tenggat & disclaimer. |
| **Rata-rata** | **7,25** | **8,9** | selisih **+1,6** |

Angka salah SESUDAH: **0** (dari 4 balasan). Angka salah SEBELUM: 0.

**VERDIK: LULUS** (sesudah 8,9 ≥ 8, selisih +1,6 ≥ 1,5, 0 angka salah). Catatan jujur: selisih tipis di atas batas. Di gelombang 7 Telegram sisi TANPA mendapat 8 untuk pesan yang sama (pencarian web berhasil), jadi pembeda skenario DTP bergantung pada apakah AI biasa berhasil mencari aturan 2026. Pembeda yang stabil: kecepatan, cek KLU, dan empat baris DTP yang konsisten.

**Cacat 1 gelombang 7: TERATASI** — bot dengan skill tidak lagi menulis Rp6.045.000; script & SKILL.md 1.0.5 dipatuhi di konteks Telegram.

**Cacat sisa (ringan, untuk pembuat):**
1. Jawaban pertama skenario 1 (A & B) belum menyebut syarat bruto tetap **Januari 2026** ≤ Rp10 jt; baru muncul setelah konfirmasi KLU. Saran: wajibkan satu baris syarat itu di blok "Jika DAPAT DTP".
2. Skenario 2 (tahun 2026, gaji ≤ Rp10 jt): tidak ada satu kalimat "bila usaha di sektor PMK 105/2025, PPh ini bisa DTP" — opsional, jangan sampai menambah pertanyaan.
3. Frasa "dipotong Rp45.000 dari slip" (run A) bisa dibaca pemilik awam seolah gaji berkurang; run B lebih jelas ("dibayar tunai kembali").

**Cuplikan jualan (jujur):**
- "Karyawan konveksi Rp6 juta, TK/0, 2026: skill langsung mengecek KLU, lalu memberi dua jawaban siap pakai — tanpa DTP diterima Rp5.955.000; dengan DTP PPh Rp45.000 tetap dipotong, dibayar tunai kembali, setoran Rp0, diterima Rp6.000.000 (PMK 105/2025)."
- "PPh 21 Desember dengan THR: AI biasa bisa benar, tapi butuh ±11 menit mencari aturan di internet; dengan skill jawabannya keluar ±40 detik, termasuk lebih potong Rp220.000 dan tenggat pengembaliannya."
(Jangan klaim AI biasa salah angka di dua skenario ini — di uji ini angkanya benar.)
