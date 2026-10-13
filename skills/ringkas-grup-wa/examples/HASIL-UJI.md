# Hasil Uji Independen — ringkas-grup-wa

**Tanggal:** 2026-09-23 (simulasi tanggal jalan uji; dieksekusi pada sesi tanggal sistem 2026-09-24)
**Penguji:** agent penguji independen (simulasi, Claude Code) — tidak terlibat pembuatan skill,
hanya membaca folder `skills/ringkas-grup-wa/` dan brief uji.

## Ringkasan metodologi
- 3 ekspor chat fiktif dibuat sendiri (≥80 pesan tiap file, format berbeda sesuai penugasan) di
  `/tmp/uji-ringkas-grup-wa/input/`, dengan **kunci jawaban dibuat SEBELUM** menjalankan skill
  (`/tmp/uji-ringkas-grup-wa/kunci/kunci-{a,b,c}.md`).
- Parser dijalankan sungguhan (`scripts/parse_ekspor_wa.py`) untuk ketiga file, hasil JSON dicek
  satu per satu terhadap file sumber.
- Statistik (jumlah pesan per pengirim, jam ramai, media, dihapus) **diverifikasi independen**
  dengan skrip Python terpisah yang TIDAK memakai kode skill sama sekali
  (`/tmp/uji-ringkas-grup-wa/verifikasi_independen.py`, pendekatan regex sendiri dari nol) — hasil
  **cocok 100%** dengan output skrip skill untuk ketiga skenario (per-pengirim, jam ramai, jumlah
  media, jumlah dihapus, dan jumlah pesan dalam rentang filter untuk skenario c).
- Ringkasan (peran agent yang memuat SKILL.md) ditulis manual mengikuti format & langkah kerja
  SKILL.md persis, lalu recall/presisi dihitung terhadap kunci jawaban.
- Data rusak/tepi diuji: file kosong, biner, ZIP tanpa .txt, encoding latin-1 & UTF-16, format
  tanggal ambigu & tidak konsisten, baris sangat panjang (~26.000 karakter), nama pengirim berisi
  ":", pesan sistem bahasa Inggris, dan `--samarkan`.
- `references/openclaw-grup.md` diverifikasi ulang terhadap CLI OpenClaw **2026.9.5 (ec9c1a1)**
  sungguhan (`node openclaw.mjs`, HOME sementara): `config set` untuk `groupPolicy`,
  `groupAllowFrom`, `groups["<id>@g.us"].tools.deny` (notasi bracket), dan `historyLimit` semua
  **berhasil divalidasi** persis seperti diklaim dokumen (status **T**). `config validate` gagal
  hanya karena belum ada file config di lingkungan uji terisolasi (bukan kesalahan dokumentasi).
- `bash scripts/uji_openclaw.sh` disimulasikan manual dengan OpenClaw 2026.9.5 sungguhan: skill
  **muncul di `eligible`, `modelVisible`, dan `commandVisible`**, tidak ada di `blocked`/`disabled`.

## Tabel skor (1–10)
| Kriteria | Skor | Catatan |
|---|---|---|
| Pemicu (description tepat) | 8 | Kata kunci ID & EN lengkap (rekap grup, catch me up, chat digest), jelas kapan dipakai. Tidak menyebut kata "ekspor" secara eksplisit di description sehingga permintaan "ringkas grup X" tanpa lampiran perlu deteksi konteks tambahan (teruji baik di S4). |
| Kemudahan awam | 8 | Alur ekspor dijelaskan di README dengan langkah persis per platform; SKILL.md sendiri hanya merujuk README (lihat cacat di S4). |
| Kualitas output | 9 | Format konsisten, per-hari saat perlu, tabel tindakan, kutipan+jam nyata — sangat siap pakai. |
| Akurasi (angka/fakta) | 7 | Statistik & nominal 100% akurat (diverifikasi independen); TAPI ditemukan 1 kegagalan recall (item terlewat, skenario b) dan 1 **cacat berat pada `--samarkan`** (lihat di bawah) yang menurunkan skor kategori ini. |
| Penanganan input kurang | 9 | S4 bertanya sekali, jelas, dengan langkah ekspor lengkap; tidak melanggar aturan "jangan tanya dua kali". |
| Penanganan di luar cakupan | 9 | S5 menolak tegas + alasan UU PDP + alternatif etis, konsisten dengan keputusan pemilik. |
| Keamanan | 5 | Script sendiri aman (tidak ada jaringan/eksekusi berbahaya/pembacaan kredensial) — **tapi fitur privasi andalan (`--samarkan`) BOCOR**, ini menyangkut keamanan data pihak ketiga yang dijanjikan produk (lihat cacat berat). |

## SKOR AKHIR: 5 / 10 — **REVISI** (bukan LULUS)

**Alasan skor tidak dirata-rata otomatis:** kualitas ringkasan, ketaatan format, dan penanganan
S4/S5 semuanya sangat baik (8–9). Tapi ditemukan **cacat berat** pada fitur `--samarkan` yang
justru merupakan janji jualan utama skill ini ("Bisa menyamarkan nama & nomor anggota kalau isinya
sensitif" — README.md baris 10; checklist SKILL.md baris 132: "Kalau `--samarkan` dipakai, tidak
ada nama/nomor asli tersisa di output"). Karena ini **produk berbayar** yang secara eksplisit
menjual fitur anonimisasi untuk grup sensitif (keluarga/pelanggan/pasien — SKILL.md baris 137),
cacat privasi yang gagal total ini **membatasi skor ke ≤ 6** sesuai aturan brief, dan saya
menurunkannya lagi ke 5 karena dampaknya nyata (kebocoran identitas pihak ketiga) dan mudah
dieksploitasi pembeli tanpa sadar (mereka percaya `--samarkan` = aman).

## Cacat

### BERAT
1. **`--samarkan` TIDAK menyamarkan nama yang disebut di ISI pesan orang lain, hanya
   menyamarkan field `pengirim`.** Dibuktikan dengan `input/renovasi-toko.txt --samarkan`: field
   `pengirim` semua berubah jadi "Anggota 1".."Anggota 6" (benar), TAPI teks pesan seperti
   `"@Pak Nanda kalau atap galvalum..."`, `"sabar ya Budi, pak Nanda biasanya online siang"`,
   `"Sari menambahkan Ridho"` (pesan sistem) masih memuat **nama asli** — ditemukan **19 kemunculan
   nama asli** tersebar di **16 pesan berbeda** dari total 99 pesan (dicek dengan skrip Python
   independen, lihat detail di transkrip uji). Fungsi `samarkan_pengirim()` di
   `scripts/parse_ekspor_wa.py` baris 377-392 hanya memanggil `samarkan_nomor_dalam_teks()` untuk
   isi pesan (regex nomor telepon saja), **tidak pernah mengganti nama pengirim lain yang disebut
   di teks**, dan **tidak menyentuh pesan sistem** (`jenis: "sistem"`, `pengirim: None`) sama
   sekali meski isinya eksplisit menyebut nama (mis. "Sari menambahkan Ridho").
   **Saran perbaikan konkret:** di `samarkan_pengirim()` (baris ~377-392), setelah membangun
   `pemetaan` nama→"Anggota N", lakukan substring-replace nama asli (urutkan dari yang terpanjang
   dulu supaya nama yang jadi awalan nama lain tidak salah potong) pada `p["teks"]` untuk SEMUA
   pesan termasuk yang `jenis == "sistem"` sebelum atau sesudah `samarkan_nomor_dalam_teks`;
   tambahkan juga unit test baru di `tests/uji_regresi.py` (kelas `Samarkan` sudah ada tapi belum
   punya test untuk kasus ini — test yang ada baru menguji nomor telepon & pemetaan pengirim,
   bukan nama-di-isi-pesan) yang memasukkan mention nama di teks pesan lain dan memastikan hasil
   `--samarkan` tidak mengandung nama asli sama sekali.
   **Dampak nyata:** untuk grup sensitif (keluarga/pasien/pelanggan) yang justru direkomendasikan
   SKILL.md memakai `--samarkan`, identitas pihak ketiga tetap bisa terbaca lewat mention/isi
   pesan — bertentangan langsung dengan janji produk dan berisiko UU PDP bagi pembeli.

### SEDANG
2. **Recall tidak sempurna pada grup padat (skenario b):** dari 11 item Perlu Perhatian di kunci
   jawaban, 1 item terlewat (pertanyaan harga Toner Rose, lihat `examples/02-reseller-ios-zip.md`
   catatan penguji). Recall = 10/11 (91%). Ini murni kelalaian langkah kerja agent saat menyisir
   90 pesan manual, bukan bug skrip — tapi SKILL.md tidak punya mekanisme yang memaksa penyisiran
   sistematis (mis. checklist per pesan) untuk grup padat. **Saran:** tambahkan instruksi di
   SKILL.md langkah 4 untuk menandai dulu SEMUA pesan yang mengandung "?" sebagai kandidat Perlu
   Perhatian sebelum menyaring, khususnya untuk grup > 50 pesan/hari.
3. **Ambiguitas tanggal m/d vs d/m pada 1 hari volume tinggi tidak diberi peringatan tambahan:**
   pada skenario b, seluruh 90 pesan format "9/12/26" (ambigu) dibaca sebagai 1 tanggal ("9
   Desember"). Catatan ambiguitas dari script sudah disampaikan (baik), tapi SKILL.md tidak
   mengarahkan agent untuk menyadari & menyebutkan bahwa pola ini "kemungkinan besar 1 hari kerja
   yang sama terlepas dari pembacaan tanggal yang mungkin salah" — berpotensi membingungkan
   pembeli awam yang melihat tanggal jauh dari hari sebenarnya. Lihat saran di
   `examples/02-reseller-ios-zip.md`.
4. **Encoding UTF-16 tidak didukung** (`ENCODING_DICOBA` di `scripts/parse_ekspor_wa.py` baris 48
   hanya `utf-8-sig, utf-8, cp1252, latin-1`): file UTF-16 gagal total-dibaca-sebagai-mojibake dan
   berakhir dengan pesan "Tidak ada baris pesan yang dikenali" — bukan crash (baik), tapi pesan
   errornya tidak spesifik menyebut kemungkinan encoding salah. WhatsApp sendiri selalu mengekspor
   UTF-8 jadi risiko rendah, tapi pesan error generik ini bisa membingungkan pengguna yang filenya
   memang UTF-16 dari sumber lain (mis. hasil convert manual). **Saran:** tambahkan `utf-16` ke
   `ENCODING_DICOBA`, atau minimal sebutkan di pesan catatan "jika file berasal dari convert/edit
   manual, coba simpan ulang sebagai UTF-8".

### RINGAN
5. SKILL.md tidak menjelaskan cara menangani pesan yang statusnya "sudah dijawab di file yang
   sama" untuk kategori Perlu Perhatian (dianalisis di `examples/01`) — agent terpaksa menafsirkan
   sendiri. Saran: tambahkan sub-kategori "✅ sudah dijawab" vs "❗ masih menunggu".
6. Tidak ada aturan eksplisit soal pesan dari pengguna sendiri (bila diketahui namanya) di
   SKILL.md langkah 4 — lihat catatan di `examples/03`.
7. Nama pengirim yang (secara tidak wajar) mengandung ":" hanya menangkap sebagian sebelum tanda
   ":" pertama sebagai nama (diuji dengan `rusak/nama_titik_dua.txt`) — perilaku wajar untuk kasus
   yang sangat jarang terjadi di ekspor WA asli (nama kontak tidak boleh mengandung ":"), tidak
   perlu diperbaiki segera, cukup dicatat sebagai batasan yang diketahui.
8. `--samarkan` tidak menyamarkan nomor telepon berformat non-standar Indonesia (mis. nomor luar
   negeri) — di luar cakupan uji ini karena data uji semuanya nomor Indonesia, tapi layak dicatat
   sebagai batasan pola regex `POLA_NOMOR_TELEPON` (hanya menangkap awalan `62`/`0` + `8`).

## Verifikasi angka independen: **YA**
Statistik ketiga skenario (per-pengirim, jam ramai, jumlah media/stiker, jumlah dihapus, dan
jumlah pesan dalam rentang filter `--sejak`) dihitung ulang dengan skrip Python terpisah dari nol
(`verifikasi_independen.py`, regex sendiri, tidak memanggil `parse_ekspor_wa.py` sama sekali) —
hasil identik 100% dengan output skrip skill untuk skenario a, b, dan c.

## Uji A/B & banding pesaing
- `examples/00-pembanding-tanpa-skill.md`: hasil dengan skill jelas lebih baik — versi tanpa
  skill bahkan **salah faktual** (mengklaim keputusan pembayaran sudah final padahal file tidak
  menunjukkan itu).
- `examples/00-banding-pesaing.md`: pesaing yang ditemukan (`mocasus/whatsapp-group-summary`, 14
  ⭐) di bawah ambang kurasi pedoman kurasi Komunitech dan justru memakai pendekatan perekaman diam-diam yang
  bertentangan dengan kebijakan Komunitech — skill kita unggul dari sisi etika, kesiapan pakai,
  dan struktur output (kutipan+jam, daftar tindakan).

## Uji OpenClaw & pemuatan
`bash scripts/uji_openclaw.sh` (disimulasikan manual dengan OpenClaw 2026.9.5 sungguhan,
HOME terisolasi): skill `ringkas-grup-wa` muncul di `eligible` (24/58 total skill repo),
`modelVisible`, dan `commandVisible`; tidak ada di `blocked`/`disabled`/`missingRequirements`.
**Lulus uji muat OpenClaw.**

## Rekomendasi sebelum rilis
1. **Wajib perbaiki cacat berat #1 (`--samarkan` bocor nama di isi pesan & pesan sistem)** sebelum
   status naik dari `beta`/`lulus` — ini janji privasi inti produk. Setelah diperbaiki, uji ulang
   khusus kasus ini oleh penguji independen (bukan cukup baca kode, jalankan ulang skenario nyata
   dengan mention nama di isi pesan + pesan sistem yang menyebut nama).
2. Pertimbangkan perbaikan sedang #2–#4 (checklist penyisiran sistematis, catatan ambiguitas
   tanggal untuk kasus 1-hari-padat, dukungan UTF-16) pada revisi berikutnya — tidak menghalangi
   rilis sendirian, tapi meningkatkan reliabilitas.
3. Setelah revisi, `platform_teruji` untuk baris `catalog.csv` skill ini sebaiknya dicatat sebagai
   `openclaw (uji muat otomatis, simulasi agent)` — belum ada uji manusia sungguhan di platform
   manapun pada sesi ini.

---

## Uji ulang v1.0.1 (2026-09-24)

**Penguji:** agent penguji independen (simulasi, Claude Code) — sesi terpisah dari uji pertama,
tetap tidak terlibat pembuatan skill. Skor sebelumnya: **5/10 (REVISI)**, disebabkan cacat berat
`--samarkan` yang bocor nama di isi pesan/@mention/pesan sistem.

### Klaim pembuat yang diuji
1. `--samarkan` kini menyamarkan nama di isi pesan, @mention, pesan sistem, dan sapaan+nama pihak
   luar (mis. "Pak Budi" → "Orang N"), dengan field `kemungkinan_nama_tersisa` sebagai jaring
   pengaman transparan (best-effort, bukan jaminan mutlak).
2. `kandidat_perlu_perhatian[]` sebagai checklist wajib berbasis pola (tanda tanya, mention,
   uang, tenggat, kata keputusan/komplain) untuk mengurangi risiko item terlewat di grup padat.
3. Peringatan tambahan saat tanggal hanya punya satu kombinasi d/m-m/d (kemungkinan besar 1 hari
   yang sama meski terbaca ambigu).
4. Dukungan encoding UTF-16 (BOM & tanpa BOM, LE/BE, dipilih via heuristik baris yang cocok pola
   pesan).
5. `--nama-saya` untuk menandai pesan sendiri (`dari_saya`) & mention langsung.
6. Nomor telepon non-Indonesia (format `+<kode negara>...`) ikut disamarkan.
7. 68 unit test (naik dari 46).

### Metodologi uji ulang
- **Regresi:** `python3 tests/uji_regresi.py` → **68/68 lulus**, sesuai klaim.
- **Regresi statistik pada 3 fixture LAMA** (`renovasi-toko.txt`, zip reseller iOS, `alumni.txt`
  dengan filter `--sejak`): dibandingkan field `statistik` & jumlah pesan per hari hasil v1.0.0
  vs v1.0.1 — **identik 100%**, tidak ada regresi angka.
- **Fixture BARU yang belum pernah dilihat pembuat** (dibuat setelah menerima instruksi uji
  ulang, disimpan di `/tmp/uji-ringkas-grup-wa/input/kantor_baru.txt`, 92 pesan, Android, grup
  kantor kecil fiktif) memuat sengaja:
  - nama huruf kecil sebagai *pengirim* asli: `budi`, `kak rina` (bukan cuma di isi pesan)
  - panggilan "Mas Andi" (yang juga jadi nama pengirim literal, bukan sekadar sapaan) dan
    "kak rina" / "Bu Wati" / "Pak Herman" (pihak luar, disebut di isi pesan)
  - nama = kata umum Indonesia: "Indah", "Bayu", "Restu", "Fajar"
  - **ejaan ganda**: pengirim terdaftar "Muhammad Iqbal", tapi di pesan lain disapa "Ikbal"
    (varian fonetik, sengaja TIDAK sama persis agar diuji apakah tertangkap)
  - pesan sistem EN: `"Andi added Citra Lestari"`, `"Indah left"`, `"Fajar removed Bayu"`
  - nomor +65 (Singapura) dan +1 (AS), plus nomor Indonesia biasa
  - @mention (`@Restu`, `@Bayu`, `@Wati`, `@Andi`)
  - Kunci jawaban leak dibuat manual sebelum menjalankan `--samarkan` (daftar 17 identitas asli
    yang wajib hilang, lihat `/tmp/uji-ringkas-grup-wa/verifikasi_bocor_d.py`).
- **Deteksi kebocoran dihitung independen** dengan skrip Python baru
  (`verifikasi_bocor_d.py`) yang **tidak memanggil kode skill sama sekali** — mencocokkan daftar
  nama asli & pola nomor telepon umum terhadap `teks`/`pengirim` di hasil `--samarkan`.
- **Recall grup padat:** dihitung ulang untuk skenario b (reseller, 90 pesan) dengan memeriksa
  apakah `kandidat_perlu_perhatian[]` memuat seluruh 11 item di `kunci/kunci-b.md`.

### Hasil: kebocoran `--samarkan`
| Fixture | Identitas asli diuji | Bocor (independen) | Ditandai di `kemungkinan_nama_tersisa`? |
|---|---|---|---|
| `renovasi-toko.txt` (fixture lama, pernah bocor 19x/16 pesan di v1.0.0) | Budi, Dimas, Sari, Fajar, Pak Nanda, Ridho | **0** | field muncul, isinya hanya kata umum/akronim (Jaya Makmur, MCB, PLN, PVC, RAB) — bukan nama asli |
| `kantor_baru.txt` (fixture BARU) | 17 identitas (nama biasa, huruf kecil, panggilan, ejaan ganda, EN sistem, +65/+1) | **2** kemunculan — keduanya kata "Ikbal" (varian ejaan "Muhammad Iqbal" yang sengaja tidak identik) | **Ya** — "Ikbal" muncul persis di `kemungkinan_nama_tersisa` |
| Nomor telepon (+62, +65, +1) di kedua fixture | — | **0** bocor | — |

**Kesimpulan kebocoran:** cacat berat v1.0.0 **sudah diperbaiki**. Satu-satunya kebocoran yang
ditemukan di fixture baru (varian ejaan fonetik "Ikbal") adalah kasus yang secara eksplisit
**diberi tahu ke pengguna lewat `kemungkinan_nama_tersisa`** — bukan kebocoran diam-diam. Ini
sesuai dengan cara SKILL.md sekarang mendeskripsikan `--samarkan` (baris ~141: "upaya terbaik,
BUKAN jaminan mutlak... ejaan nama yang berbeda-beda... Selalu sampaikan isi
`kemungkinan_nama_tersisa`"). Karena skill sudah jujur soal keterbatasan ini DAN memberi jaring
pengaman yang benar-benar berfungsi (bukan janji kosong), ini **tidak lagi dihitung sebagai cacat
berat** — diturunkan jadi catatan RINGAN (lihat di bawah), asalkan agent benar-benar
menyampaikan isi `kemungkinan_nama_tersisa` ke pengguna seperti diinstruksikan (perlu diuji di
uji platform asli/beta, tidak bisa dipastikan 100% dari sisi skrip saja).

### Hasil: recall grup padat (skenario b, 90 pesan)
`kandidat_perlu_perhatian[]` memuat **37 pesan kandidat**, dan **11/11 item di kunci jawaban
`kunci/kunci-b.md` (termasuk item yang terlewat di uji v1.0.0: pertanyaan harga Toner Rose 14.00)
tercakup semua** → **recall 100%** bila agent memakai checklist ini sesuai instruksi SKILL.md
langkah 4 ("Setiap item di daftar ini harus dipertimbangkan"). Presisi checklist itu sendiri
wajar (37 kandidat dari 90 pesan grup jualan yang memang padat tanya-jawab harga/tenggat) — bukan
daftar Perlu Perhatian final (agent tetap harus menyaring), tapi jaring pengaman recall yang
efektif.

### Hasil: peringatan tanggal & UTF-16
- Skenario b (semua tanggal "9/12/26", 1 kombinasi) sekarang memunculkan catatan tambahan:
  *"PERINGATAN: hanya ada SATU kombinasi tanggal... besar kemungkinan semuanya terjadi dalam SATU
  hari yang sama..."* — persis mengatasi cacat sedang #3 di uji v1.0.0.
- File UTF-16 (dengan BOM maupun **tanpa BOM**, LE) yang sebelumnya gagal total dibaca kini
  terbaca benar (`Wïndy`, `Böbby` terdeteksi sebagai pengirim) — diuji ulang dengan file baru
  UTF-16-LE tanpa BOM, hasil benar. Cacat sedang #4 (UTF-16) **teratasi**.

### Regresi data rusak/tepi (ulang semua kasus uji v1.0.0)
File kosong, biner, ZIP tanpa .txt, tanggal tidak konsisten, nama berisi ":", pesan sistem EN,
baris sangat panjang — semua tetap berperilaku sama (tidak crash, exit code benar, pesan error
jelas). **Tidak ada regresi.**

### Uji muat OpenClaw (regresi)
`ringkas-grup-wa` tetap muncul di `eligible`/`modelVisible`/`commandVisible` OpenClaw 2026.9.5
setelah update file skrip — **tidak ada regresi pemuatan**.

### Tabel skor v1.0.1
| Kriteria | Skor v1.0.0 | Skor v1.0.1 | Catatan |
|---|---|---|---|
| Pemicu | 8 | 8 | Tidak berubah. |
| Kemudahan awam | 8 | 8 | Tidak berubah (cacat ringan S4 lama belum disentuh, di luar cakupan uji ulang ini). |
| Kualitas output | 9 | 9 | Tidak berubah. |
| Akurasi (angka/fakta) | 7 | 9 | `--samarkan` tidak lagi bocor diam-diam; checklist `kandidat_perlu_perhatian` menutup celah recall yang sebelumnya menurunkan skor. |
| Penanganan input kurang | 9 | 9 | Tidak berubah. |
| Penanganan di luar cakupan | 9 | 9 | Tidak berubah. |
| Keamanan | 5 | 9 | Fitur privasi inti kini benar-benar berfungsi & jujur soal batasannya (bukan janji palsu). Tidak diberi 10 karena "upaya terbaik" tetap punya celah residual (ejaan ganda) — wajar selama selalu diberitahukan, tapi tetap berarti pengguna harus baca `kemungkinan_nama_tersisa`, bukan sepenuhnya "pasang lupa". |

### SKOR AKHIR v1.0.1: **8 / 10 — LULUS**
Cacat berat v1.0.0 sudah tuntas diperbaiki dan diverifikasi independen (bukan hanya membaca
kode, tapi menjalankan fixture lama + fixture baru yang sengaja dirancang untuk mencari celah).
Recall grup padat naik ke 100% lewat mekanisme checklist baru. Tidak ditemukan cacat berat baru.

**Cacat SEDANG yang masih tersisa (bukan lagi berat):**
1. `--samarkan` masih bisa melewatkan varian ejaan fonetik yang jauh dari nama terdaftar (mis.
   "Ikbal" untuk "Iqbal") — **tapi selalu ditandai** di `kemungkinan_nama_tersisa`, jadi risikonya
   bergeser dari "kebocoran diam-diam" (berat) menjadi "agent lalai menyampaikan peringatan ke
   pengguna" (sedang, tergantung kepatuhan agent pada SKILL.md). **Saran:** karena ini kritikal
   untuk kepercayaan pembeli, pertimbangkan menambahkan ke checklist SKILL.md ("Checklist sebelum
   mengirim hasil") sebuah baris tegas: *"Jika `--samarkan` dipakai dan `kemungkinan_nama_tersisa`
   tidak kosong, WAJIB tampilkan daftar itu ke pengguna di awal atau akhir ringkasan — jangan
   hanya di catatan internal."* (SKILL.md sudah menyebutkan ini di beberapa tempat, tapi belum
   ada di checklist final baris-per-baris yang paling mudah diikuti agent tergesa-gesa.)
2. Cacat sedang lama #1 (skor "Kemudahan awam" S4 belum menyalin langkah ekspor ke SKILL.md
   sendiri) belum disentuh pembuat — di luar cakupan klaim v1.0.1, tetap tercatat sebagai
   perbaikan yang disarankan untuk revisi berikutnya.

**Verifikasi angka independen: YA** (statistik regresi 3 fixture lama + kebocoran nama/nomor di
fixture baru, keduanya dengan skrip terpisah dari kode skill).

**Rekomendasi:** skill ini **LULUS** dan layak naik status dari `draft`/`uji` ke tahap berikutnya
(uji platform asli oleh manusia sesuai panduan uji platform internal (tidak disertakan dalam paket), lalu program beta) — cacat berat
yang menahan rilis sebelumnya sudah tuntas. Catatan sedang #1 di atas sebaiknya tetap
ditindaklanjuti sebelum rilis penuh, tapi tidak menghalangi kelanjutan ke tahap uji platform.

## Catatan koordinator — setelah uji ulang v1.0.1 (8/10 LULUS)
Sedang #1: checklist akhir SKILL.md sudah memuat baris wajib menyampaikan `kemungkinan_nama_tersisa` bila tidak kosong (baris "Kalau `--samarkan` dipakai…") — tidak ada perubahan tambahan. Sedang #2 (S4): langkah ekspor chat Android & iPhone kini ditulis langsung di SKILL.md bagian Input.
