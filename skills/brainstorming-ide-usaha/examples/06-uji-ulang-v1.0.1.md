# Uji 06 — Uji ulang v1.0.1 (Tahap 6 butir 7, penguji independen)

- **Tanggal:** 2026-09-25
- **Penguji:** agent terpisah (bukan pembuat, bukan perevisi v1.0.1) — hanya membaca folder skill ini + `examples/HASIL-UJI.md` uji pertama.
- **Lokasi uji:** salinan di scratchpad `uji2-biu/brainstorming-ide-usaha/` (bukan `.claude/skills/`).
- **Platform:** `claude-code (simulasi agent)`.
- **Yang diuji:** `SKILL.md` (110 baris), `scripts/skor_ide.py`, `scripts/test_skor_ide.py`, `templates/`, `references/`.

## 1. Tes bawaan

`python3 scripts/test_skor_ide.py` → **Ran 60 tests … OK** (sebelumnya 32).

## 2. Temuan uji pertama → status

| # | Prioritas | Temuan lama | Uji ulang (perintah/data) | Status |
|---|---|---|---|---|
| 1 | TINGGI | Koma desimal tanpa kutip di baris ke-2+ menggeser kolom diam-diam | `nama_ide,a,b` / `Ide X,4,3` / `Ide Y,3,5,4` → "baris 3: jumlah kolom (4) tidak sama dengan jumlah kolom header (3 …). Kalau ini karena koma desimal tanpa kutip (mis. 3,5), tulis pakai titik (3.5) atau beri tanda kutip", exit 1 | **Beres** |
| 2 | SEDANG | CSV Excel ID (BOM, `;`, `"3,5"`) ditolak | File ber-BOM, pemisah `;`, `"3,5"` berkutip dan `3,5` tanpa kutip → X 3,667, Y 3,667 (seri terdeteksi), Z 3,000. Independen: (4·60+3·30)/90 = 330/90; (3,5·60+4·30)/90 = 330/90; (3,5·60+2·30)/90 = 270/90 — cocok. `;` + nama berisi koma berkutip juga benar | **Beres** |
| 3 | SEDANG | Bobot `NaN`/`Infinity`/`true` diterima | Ketiganya ditolak dengan pesan jelas, exit 1 | **Beres** |
| 4 | SEDANG | Satu pertanyaan per pesan | SKILL.md B.1 & C.2: satu pesan, maks. 5 pertanyaan, susulan hanya bila ambigu; mode cepat tanpa tanya. Diuji ulang di skenario 01 & 04 di bawah (1 giliran tanya) | **Beres** |
| 5 | SEDANG | Batas Jalur B/C & alat hitung B | Ringkasan B vs C eksplisit; B.4 memakai `impas`, skor opsional bila ≥ 4 ide; contoh laundry dilabel ulang Jalur B | **Beres** |
| 6 | SEDANG | Tidak ada bobot default resmi | Bobot 5/4/3/2/4 di SKILL.md + template + script (`--bobot` opsional, sumber bobot selalu dicetak; nama kolom lain → sama rata dan disebut) | **Beres** |
| 7 | SEDANG | Mode cepat vs gerbang persetujuan | C.2 & C.7: gerbang tetap wajib, cukup satu balasan ("ketik 1/2/3 atau 'lanjut'") | **Beres** (lihat catatan B-4 di bawah untuk Jalur B) |
| 8 | RENDAH | Traceback mentah / format rupiah Indonesia | cp1252 (`Caf\xe9`) terbaca; byte tak terbaca → "encoding tidak dikenali. Simpan ulang sebagai CSV UTF-8"; folder sebagai `--ide`/`--bobot` → "path … adalah folder"; `--modal nan`/`inf`/`1e309` → pesan Indonesia (lewat argparse, exit 2); `5.000.000`, `Rp15.000`, `5jt`, `15rb`, `1,5jt` → benar (334 / 75 unit) | **Beres** |
| 9 | RENDAH | Tampilan margin dibulatkan; label tak sejajar; istilah "unit" | `--margin 2500.5` tampil `Rp2.500,50`, BEP 2.000 (5.000.000/2.500,5 = 1.999,6 → 2.000 ✓); `--margin 0.5` ditolak ("kurang dari Rp1"); label sejajar; catatan istilah unit ditambahkan | **Beres** |
| 10 | RENDAH | Ambang uji murah bercelah | "0–29% berhenti, 30–99% perbaiki, 100%+ lanjut" | **Beres** |
| 11 | RENDAH | Tabel musim tumpang tindih | Tanggal muda 1/25 + beberapa hari; tanggal tua 20–24; 1.1 dihapus; Ramadan tanpa tanggal + peringatan | **Beres** (sisa kecil: 9.9/10.10/11.11 disebut "Harbolnas nasional" padahal Harbolnas resmi hanya 12.12 — lihat B-8) |
| 12 | RENDAH | Kategori terlarang tanpa dasar aturan | UU 7/2014 Pasal 9 (larangan skema piramida; sanksi pidana di Pasal 105), UU 8/1995 Pasar Modal, UU 4/2023 P2SK + cek daftar OJK, tanggal cek 2026-09-25 | **Beres** — rujukan benar |
| 13 | RENDAH | Duplikat beda huruf/spasi; spasi di header | `Ide X` vs `ide  x ` terdeteksi; header `nama_ide , a , b ` dirapikan | **Beres** (header huruf besar belum — B-3) |
| 14 | RENDAH | Emoji di Windows | Emoji dihapus dari keluaran + `reconfigure(errors="replace")` | **Beres** (belum diuji di Windows asli) |

## 3. Data rusak BARU (belum dicoba di uji pertama)

| Kasus | Hasil | Penilaian |
|---|---|---|
| Baris kosong di tengah (2 baris kosong, lalu `Ide Y,3,9`) | Ditolak "baris **3** ('Ide Y'), kolom 'b': nilai 9 di luar rentang" — padahal Ide Y ada di baris fisik **5** | Bug B-1 (rendah) |
| Baris berisi koma saja `,,` | "baris 3: 'nama_ide' kosong" | OK |
| Header `Nama_Ide , A ,B` (huruf besar) | Ditolak "wajib punya kolom 'nama_ide' (header terbaca: ['Nama_Ide', …])" | B-3 (rendah) — pesan cukup jelas, tapi bisa diterima otomatis |
| Kolom default salah huruf (`Kesesuaian_Modal`) tanpa `--bobot` | Jalan dengan bobot **sama rata** (3,800), sumber disebut di keluaran | B-2 (rendah–sedang) |
| Kolom kriteria ekstra (`c`) tidak ada di bobot | "kolom kriteria di file ide tidak ada di file bobot: ['c']" | OK |
| Koma di akhir tiap baris (kolom kosong ekor ala Excel) | Dengan bobot: "…tidak ada di file bobot: ['']"; tanpa bobot: "kolom '': nilai kosong" | B-4 (rendah) — pesan membingungkan |
| Header kolom kembar `nama_ide,a,a` / `Ide X,1,5` | **Diterima diam-diam**, nilai kolom terakhir dipakai → skor 5,000, exit 0 | B-5 (sedang-rendah) — skor salah tanpa peringatan |
| JSON bobot rusak (`{"a":60, "b":30,`) | "file bobot bukan JSON valid: Expecting property name … line 1 column 17" | OK (pesan teknis Inggris dari `json`, tapi berlabel jelas) |
| JSON berupa list | "harus berupa objek JSON tidak kosong" | OK |
| Bobot string `"3,5"` | "bukan angka: '3,5'" | OK (konsisten dengan uji pertama; bisa diterima seperti nilai CSV) |
| JSON ber-BOM | Terbaca benar | OK |
| JSON kunci kembar (`"a":60 … "a":1`) | Diam-diam memakai nilai terakhir | Rendah (perilaku standar JSON) |
| Nilai negatif `-4` | "nilai -4 di luar rentang 1-5" | OK |
| `--modal -5jt` | argparse: "expected one argument" (Inggris, tidak menyebut negatif) | B-6 (rendah) |
| `--margin=-1000` | "margin per unit harus lebih besar dari 0" | OK |
| `4.5.1`, `1e0`, spasi di sekitar angka | Ditolak / diterima wajar | OK |
| Pemisah tab | Ditolak "wajib punya kolom 'nama_ide' (header terbaca: ['nama_ide\tA'] …)" | Rendah — pesan menunjukkan penyebabnya |
| CRLF (Windows) | Benar | OK |
| **3.000 ide**, `;`, desimal koma campur, tanpa `--bobot` | 0,47 detik; **0 selisih** dari 3.000 skor dibanding hitungan independen dengan `fractions.Fraction` (Σnilai×bobot/18, format 3 desimal); urutan turun benar; bobot default resmi dipakai & disebut | OK |
| Titik impas independen (`-(-modal // margin)` dengan Fraction) | 125, 500, 143, 334, 1.000.000, 3, 2.000, 142.857.143 — semua **cocok** | OK |

## 4. Bug baru berprioritas

- **B-5 (sedang-rendah)** — Header dengan nama kolom kembar diterima diam-diam (nilai kolom terakhir menimpa). Lokasi `skor_ide.py` `baca_ide()` (`dict(zip(header, …))`). Perbaikan: tolak header yang punya nama kolom sama (setelah strip).
- **B-2 (rendah-sedang)** — Salah ketik/huruf besar di nama kolom default membuat script diam-diam pindah ke bobot sama rata. Sumber disebut di keluaran, tapi pengguna awam mudah melewatkannya. Perbaikan: bandingkan nama kolom secara `casefold()`, atau cetak peringatan eksplisit "kolom mirip bobot default tapi tidak persis sama".
- **B-1 (rendah)** — Nomor baris di pesan error salah setelah ada baris kosong (baris kosong dibuang sebelum penomoran). Perbaikan: simpan nomor baris fisik.
- **B-3 (rendah)** — Header `Nama_Ide`/`NAMA_IDE` ditolak; bisa dinormalisasi huruf kecil.
- **B-4 (rendah)** — Kolom kosong di ujung (koma ekor dari Excel) memberi pesan `['']` yang membingungkan; sebaiknya dibuang otomatis bila seluruh kolom kosong, atau pesan "ada kolom tanpa nama".
- **B-6 (rendah)** — `--modal -5jt` memunculkan pesan argparse Inggris; tidak kritis (nilai negatif memang tidak sah).
- **B-7 (rendah, SKILL.md)** — Aturan "mode cepat tetap lewat gerbang persetujuan, dipersingkat satu balasan" ditulis eksplisit hanya di Jalur C.2; Jalur B.1 menyebut mode cepat tapi B.5 tidak merujuk aturan gerbang singkat itu. Agent di skenario 01 menafsirkannya dengan benar, tapi sebaiknya satu kalimat di B.5.
- **B-8 (rendah, references)** — `musim-dan-momentum.md`: "9.9, 10.10, 11.11, 12.12 (Harbolnas nasional …)" — Harbolnas resmi adalah 12.12; tanggal kembar lain adalah kampanye marketplace. Ubah kata jadi "tanggal kembar marketplace; Harbolnas nasional = 12.12".

Tidak ada bug baru yang membuat angka salah pada input wajar; B-5 hanya terjadi bila header memang cacat.

## 5. Skenario ulang

### Skenario 01 — Warung makan sepi siang, modal ≤ Rp5 juta (Jalur B)

> **Pengguna:** "Warung makan saya ramai pagi sama malam, tapi jam 1 sampai jam 4 sore sepi banget. Ada ide produk baru buat naikin omzet? Modal paling 5 juta lah."

**Agent (Langkah 0 + B.1, SATU pesan):**
"Ini ide tambahan untuk usaha yang sudah jalan, modal terbatas dan bisa dites minggu ini — saya proses sebagai **Jalur B (Perlu Diuji)**. Kalau ternyata mau renovasi/tambah karyawan, bilang saja, saya naikkan ke jalur yang lebih lengkap.
Supaya idenya pas, jawab singkat 4 hal ini sekaligus (boleh pakai huruf):
1. Warung dekat apa? (a) kantor/ruko/bengkel (b) sekolah/kampus (c) perumahan (d) jalan raya — boleh lebih dari satu.
2. Siapa yang jaga jam 13–16?
3. Menu andalan + harga jual + perkiraan modal bahan per porsi?
4. Sudah pernah coba apa untuk jam sepi (diskon, dll.)? Ada momen yang dikejar (gajian, Lebaran) atau sepanjang waktu?"

**Pengguna (satu balasan):** "a dan c, ada ruko, bengkel, kantor kelurahan, belakangnya perumahan. Saya sama istri. Nasi campur 15 ribu, bahan sekitar 9 ribu. Pernah diskon 10% jam siang, nggak ngaruh. Sepanjang waktu aja."

**Agent (B.2):** ringkasan "yang Anda sebutkan" vs "asumsi saya" (tujuan: isi jam 13–16 tanpa tambah karyawan; berhasil = ≥ 10 transaksi tambahan/hari setelah 1 minggu tanpa rugi) + minta koreksi. → Pengguna: "Betul."

**Agent (B.3):** Pembalikan masalah (orang tak sempat keluar → antar; yang datang sore cari minum/camilan; masalah bukan harga → jangan ulangi diskon) + SCAMPER P (dapur menganggur untuk nasi kotak) & C (paket ngopi sore).

**Agent (B.4, titik impas lewat script, bukan dikira):**
```
python3 scripts/skor_ide.py impas --modal 750000 --margin 6000        → 125 unit
python3 scripts/skor_ide.py impas --modal 1.500.000 --margin 3rb      → 500 unit
python3 scripts/skor_ide.py impas --modal 1jt --margin 7000           → 143 unit
```
(Format Indonesia `1.500.000`, `3rb`, `1jt` kini diterima. Independen: ⌈750.000/6.000⌉ = 125; ⌈1.500.000/3.000⌉ = 500; ⌈1.000.000/7.000⌉ = ⌈142,86⌉ = 143 — cocok.)

| # | Pendekatan | Modal awal | Margin/unit (asumsi) | Balik modal kasar | Risiko utama |
|---|---|---|---|---|---|
| 1 | Pre-order makan siang antar ke ruko/bengkel/kelurahan | Rp750.000 | Rp6.000 | 125 porsi (± 3 minggu bila 8/hari) | Antar bentrok jam ramai |
| 2 | Paket "ngopi sore" (minuman + 2 gorengan) | Rp1.500.000 | Rp3.000 | 500 paket (± 2 bulan) | Margin tipis |
| 3 | Nasi kotak pesanan (rapat, arisan, pengajian) | Rp1.000.000 | Rp7.000 | 143 kotak | Pesanan tidak rutin |

Rekomendasi: #1 (modal terkecil, menu sudah terbukti, menjawab alasan utama sepi). Margin & volume ditandai **asumsi**, bukan data pasar; tidak ada janji laku.

**Agent (B.5 gerbang):** "Lanjut #1 saja, atau #1 + #3 berdampingan? Ketik 1 atau 1+3." → Pengguna: "1."

**Agent (B.6–B.7):** MVP 1 minggu (pre-order via WA ke 20 kontak ruko/bengkel, batas pesan jam 11, target 10 pesanan/hari; ambang 0–29% berhenti, 30–99% perbaiki, 100% lanjut) + tabel Rencana Aksi 7 Hari + daftar asumsi.

**Hasil:** Lulus. **Satu giliran tanya** (sebelumnya 3), total 4 giliran pengguna sampai rencana (sebelumnya 6). Angka cocok independen.

### Skenario 04 — Input tidak lengkap: "kasih ide usaha dong" (Jalur C)

**Varian a — pengguna mau menjawab:**

**Agent (Langkah 0 + C.1–C.2, SATU pesan):**
"Karena ini mulai usaha dari nol, saya pakai **Jalur C (Perlu Rencana)**. Jawab singkat 5 hal ini sekaligus — atau ketik 'langsung aja' kalau mau saya pakai asumsi umum:
1. Dijalankan: (a) sambilan (b) full waktu (c) belum tahu
2. Modal siap pakai: (a) < Rp1 jt (b) Rp1–5 jt (c) Rp5–20 jt (d) > Rp20 jt
3. Kota & cara jual: online / dari rumah / titip / lapak
4. Keahlian, hobi, atau aset (masak, jahit, motor, desain, mengajar …)
5. Hasil yang dianggap berhasil dalam 1–2 bulan pertama?"

**Pengguna:** "a, b sekitar 2 juta, Bekasi perumahan, online/rumah, saya masak lumayan istri jago bikin kue, nambah 1–2 juta sebulan udah seneng."

→ Agent menulis ulang pemahaman (disebut vs asumsi) dan lanjut ke ide. **1 giliran tanya** (uji pertama: 5 giliran).

**Varian b — mode cepat ("langsung kasih ide aja, jangan tanya-tanya"):**

Agent tidak bertanya; sekaligus dalam satu pesan menyajikan asumsi default SKILL.md (modal < Rp5 jt, paruh waktu, sendiri/dibantu 1 orang, rumahan/online, berhasil = 10 pesanan uji/1 minggu tanpa rugi), 5 ide, skor, rekomendasi, dan gerbang singkat.

Script dijalankan **tanpa `--bobot`**:
```
python3 scripts/skor_ide.py skor --ide ide.csv
Peringkat Nama Ide                                      Skor Tertimbang
1         Kue kering pre-order via WA                             4.167
2         Frozen food rumahan (dimsum/risol)                      3.722
3         Les privat online SD                                    3.667
4         Jasa titip belanja pasar induk                          3.500
5         Jual ulang (reseller) produk skincare lokal             3.278
Bobot kriteria dipakai (total bobot = 18; sumber: default resmi skill (--bobot tidak diberikan …))
```
Independen (bobot 5/4/3/2/4, Σ = 18): Kue 75/18 = 4,167; Frozen 67/18 = 3,722; Les 66/18 = 3,667; Jastip 63/18 = 3,500; Reseller 59/18 = 3,278 — **cocok**.

Penutup agent: "Rekomendasi saya #1 kue kering pre-order (modal kecil, bisa uji lewat status WA minggu ini). Bobot yang saya pakai = default skill (modal 5, permintaan 4, kemudahan 3, keahlian 2, margin 4). **Ketik 1/2/3, atau 'lanjut' untuk rekomendasi saya** — setelah itu saya susun rencana uji 7 hari." (Untuk ide reseller skincare agent menambahkan: pastikan produk sudah ber-izin edar BPOM.)

**Hasil:** Lulus. Mode cepat jalan dengan default + asumsi disebut, bobot tidak dikarang, gerbang tetap ada tapi hanya satu balasan.

## 6. Regresi

- Kategori terlarang & dasar aturan: UU No. 7/2014 Pasal 9 (skema piramida) benar; UU 8/1995 & UU 4/2023 (P2SK) + cek daftar OJK benar; tanggal cek & peringatan "aturan bisa berubah" ada. Batasan menolak tanpa "dengan catatan" tetap ada.
- Janji untung: tidak ada (grep "dijamin/pasti untung/pasti laku" hanya muncul di FAQ README yang menjawab "Tidak").
- SKILL.md: **110 baris** (< 300). Frontmatter hanya `name` & `description`.
- Keamanan script: hanya membaca file lokal yang ditunjuk; tanpa jaringan, tanpa menulis file, tanpa `subprocess`/`eval`. Aman.
