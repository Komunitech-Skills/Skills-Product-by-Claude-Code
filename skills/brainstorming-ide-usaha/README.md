# Sesi Brainstorming Ide Usaha yang Beneran Bisa Dieksekusi

**Ceritakan kebuntuanmu — ide produk baru, promo, nama usaha, diversifikasi, atau masalah operasional — dapat beberapa ide tersaring dengan skor terhitung, rencana uji murah, dan langkah aksi 7 hari, bukan sekadar daftar ide acak.**

## Manfaat
- ✅ Menggali tujuan & batasan nyata (modal, waktu, SDM, lokasi, musim) dulu sebelum melempar ide — supaya ide yang keluar memang bisa kamu kerjakan, bukan wacana
- ✅ Teknik ide terstruktur (SCAMPER, gabung-kombinasi, pembalikan masalah) dijelaskan bahasa sehari-hari dengan contoh usahamu sendiri
- ✅ Ide disaring pakai **skor tertimbang yang dihitung script**, bukan feeling — kamu tentukan kriteria & bobotnya, hasilnya angka + peringkat
- ✅ Setiap ide terpilih dilengkapi rencana uji murah (pre-order WA, tes 1 minggu, target jelas) plus titik impas kasar bila perlu modal awal
- ✅ Ditutup dengan **Rencana Aksi 7 Hari** — tabel harian siap dikerjakan, bukan cuma ide di kepala
- ✅ Ada jalur cepat kalau kamu cuma butuh beberapa opsi nama/judul tanpa proses panjang

## Cocok untuk siapa
- Pemilik UMKM yang usahanya sepi/stagnan dan butuh ide tambahan produk, promo, atau perbaikan operasional
- Yang mau mulai usaha sampingan tapi bingung mau jualan apa
- Pemilik usaha yang mau diversifikasi/buka lini baru dan butuh cara menyaring beberapa opsi secara adil
- Siapa pun yang butuh ide nama usaha/produk dengan beberapa pendekatan sekaligus
- **Bukan untuk:** kalau idemu sudah satu dan tinggal dieksekusi — pakai skill spesifiknya (`promo-kalender` untuk promo, `hitung-hpp` untuk modal produk, `riset-calon-pelanggan` untuk cari pelanggan, `proposal-kerjasama` untuk kemitraan)

## Contoh sebelum & sesudah
**Sebelum:** "Usaha laundry saya sepi, ada ide tambahan nggak?" → dijawab asal seperti "coba buka cabang baru" atau "kasih diskon aja" — tanpa mempertimbangkan modal, waktu, atau kenapa omzet turun.

**Sesudah (cukup ketik permintaan yang sama):** skill menggali dulu modal/waktu/SDM yang tersedia, memunculkan 5 ide pakai SCAMPER, menyaringnya dengan skor tertimbang terhitung (skor 4,28 untuk ide terbaik vs 2,78 untuk yang terlemah), lalu menutup dengan rencana uji 1 minggu (target 10 pendaftar) dan tabel Rencana Aksi 7 Hari. Lihat contoh penuh di `examples/uji-pembuat-01-diversifikasi-laundry.md`.

## Cara pakai
Setelah terpasang, cukup ketik permintaan biasa ke AI agent kamu, misalnya:
- "Usaha saya sepi, ada ide tambahan produk/jasa?"
- "Butuh ide nama untuk toko roti baru saya."
- "Mau diversifikasi dari jualan baju ke lini produk lain, ide apa yang cocok?"
- "Stok bahan sering sisa/basi, ada ide solusinya?"

AI akan mengelompokkan permintaanmu (cepat / perlu diuji / perlu rencana) dan bilang ke kamu supaya bisa dikoreksi. Kalau info usahamu belum lengkap, AI tanya secukupnya — biasanya cukup **satu pesan berisi maksimal 5 pertanyaan singkat**, bukan bertanya satu-satu. Kalau kamu buru-buru, bilang saja "langsung kasih ide aja" — nanti dipakai asumsi wajar (disebutkan di akhir) tanpa perlu ditanya sama sekali.

## Instalasi singkat
Salin folder `brainstorming-ide-usaha` ke folder skills AI agent kamu:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |

Panduan lengkap (termasuk Windows): lihat `docs/instalasi.md` yang disertakan dalam paket.

## FAQ
**Apakah skor idenya dikira-kira AI atau benar-benar dihitung?**
Benar-benar dihitung lewat script Python (`scripts/skor_ide.py`) dari nilai 1–5 per kriteria dan bobot yang kamu sepakati — bukan tebakan. Kalau Python tidak tersedia di perangkatmu, AI tetap menghitung manual dengan rumus yang sama dan menunjukkan cara hitungnya.

**Skill ini menjamin idenya pasti laku?**
Tidak. Ini alat bantu menyaring & menyusun rencana uji **murah** supaya kamu bisa tahu cepat apakah ide itu layak dilanjutkan atau tidak — bukan riset pasar profesional atau jaminan hasil. Setiap ide tetap perlu diuji nyata ke pelanggan.

**Harus tahu istilah bisnis rumit dulu?**
Tidak. SCAMPER, skor tertimbang, titik impas — semuanya dijelaskan dengan bahasa sehari-hari dan contoh dari usahamu sendiri, bukan jargon konsultan.

## Riwayat versi

- **1.0.2** (2026-09-25) — Perbaikan kecil hasil uji ulang independen Tahap 6 (lihat `examples/06-uji-ulang-v1.0.1.md`), 60 → 72 tes:
  - **Header kolom kembar** (mis. `nama_ide,a,a`) kini **ditolak** dengan galat jelas — sebelumnya diterima diam-diam dan nilai kolom terakhir menimpa yang lain sehingga skor salah tanpa peringatan.
  - **Nama kolom dicocokkan tanpa peduli huruf besar/kecil, spasi, atau garis bawah** (termasuk kolom `nama_ide` sendiri, mis. header `Nama_Ide`/`NAMA IDE` kini diterima). Kalau kolom kriteria memang tidak cocok dengan bobot default resmi sama sekali, `scripts/skor_ide.py` kini mencetak **PERINGATAN eksplisit di bagian ATAS keluaran** — sebelumnya diam-diam jatuh ke bobot sama rata dan sumbernya mudah terlewat di baris terakhir.
  - **Nomor baris di pesan galat kini mengikuti baris fisik file** (sebelumnya bergeser kalau ada baris kosong di tengah file).
  - Kolom tanpa nama di ujung akibat koma ekor gaya Excel kini dibuang otomatis kalau kosong (atau ditolak dengan pesan jelas kalau ternyata berisi data) — sebelumnya memunculkan pesan membingungkan `['']`.
  - `--modal -5jt`/`--margin -1000` (angka negatif lewat CLI) kini menampilkan pesan Bahasa Indonesia yang jelas, bukan pesan argparse bawaan Bahasa Inggris.
  - `SKILL.md` Jalur B.5: aturan gerbang persetujuan singkat di mode cepat kini disebut eksplisit (sebelumnya hanya ada di Jalur C.2).
  - `references/musim-dan-momentum.md`: label "Harbolnas nasional" kini hanya untuk 12.12 sesuai fakta; 9.9/10.10/11.11 dilabel "kampanye diskon marketplace".
- **1.0.1** (2026-09-25) — Revisi hasil uji independen Tahap 6 (skor 7/10, lihat `examples/HASIL-UJI.md`):
  - **Bug TINGGI diperbaiki:** `scripts/skor_ide.py` sekarang menolak baris CSV yang jumlah kolomnya tidak sama dengan header (mis. koma desimal tanpa kutip seperti `Ide Y,3,5,4`) dengan pesan jelas — sebelumnya kolom bisa bergeser diam-diam dan menghasilkan skor salah tanpa peringatan.
  - CSV gaya Excel Indonesia kini didukung: file ber-BOM ("CSV UTF-8"), pemisah `;` terdeteksi otomatis, dan nilai desimal berkutip seperti `"3,5"` diterima sebagai 3,5.
  - Bobot `NaN`/`Infinity`/`true`-`false` di file JSON kini ditolak.
  - Script `skor_ide.py skor` bisa dijalankan **tanpa** `--bobot` — otomatis memakai bobot default resmi (bila nama kolom kriteria cocok) atau bobot sama rata, disebutkan di keluaran.
  - `impas` kini menerima format rupiah Indonesia (`5.000.000`, `Rp5.000.000`, `5jt`, `15rb`), menolak nilai di bawah Rp1 dan nan/infinity dengan pesan jelas, serta tampilan modal/margin/BEP kini sejajar dan tidak lagi membulatkan nilai desimal menjadi "Rp0".
  - Pesan galat kini ramah (tanpa traceback Python) untuk file berenkoding non-UTF-8 (dicoba UTF-8 lalu CP1252) dan path yang ternyata folder.
  - Duplikat `nama_ide` yang hanya beda huruf besar/kecil atau spasi kini terdeteksi.
  - `SKILL.md`: satu pesan berisi maksimal 5 pertanyaan singkat menggantikan aturan "satu pertanyaan per pesan" (selaras prinsip "instan" Komunitech); batas Jalur B vs C diperjelas dan contoh laundry dilabel ulang jadi Jalur B; bobot default resmi ditetapkan; aturan mode cepat vs gerbang persetujuan Jalur C ditulis eksplisit.
  - `references/musim-dan-momentum.md`: tumpang-tindih rentang tanggal gajian/tanggal tua dan duplikasi 12.12 diperbaiki.
  - `templates/kerangka-uji-murah.md`: celah ambang 3–5 dari 10 di aturan lanjut/perbaiki/berhenti ditutup.
  - Dasar aturan (UU No. 7/2014 Pasal 9, UU No. 8/1995, UU No. 4/2023 P2SK) ditambahkan untuk kategori terlarang.
  - 28 tes regresi baru ditambahkan di `scripts/test_skor_ide.py` (total 60 tes, semua lulus).
- **1.0.0** (2026-09-25) — Rilis draft pertama (lihat `ATTRIBUTION.md` untuk sumber & proses ATM).

## Catatan revisi 1.0.5 (2026-10-01)
Dari uji sebelum/sesudah OpenClaw: setelah 2 giliran AI masih menunggu persetujuan dan
belum memberi rencana, serta menyimpan CSV di folder skill tanpa bilang. Kini **paling
lambat di balasan kedua** kamu sudah menerima ide terpilih + **Rencana Uji 7 Hari**
(Hari 1–7, target angka, biaya rupiah); ganti ide cukup ketik nomornya. Baru: perintah
`skor_ide.py rencana` menghitung **untung bersih per unit setelah potongan
GoFood/ShopeeFood/marketplace**, laba uji, unit untuk menutup biaya uji, dan target
kumulatif Hari 3/5/7 — dengan rumus tertulis. File kerja hanya disimpan di folder kerjamu
(lokasinya disebut), atau tidak sama sekali (data skor lewat stdin). Saran kanal uji khas
Indonesia (status/grup WA, PO + QRIS, titip warung, tanggal gajian). AI tidak lagi
menyebut angka imbal hasil karangan pada kasus investasi/bagi hasil.

## Catatan revisi 1.0.7 (2026-10-03)
Dari uji ulang OpenClaw: saran paket dibilang "bukan turun harga" padahal harganya sama dengan pesaing, target uji tidak nyambung ke kekurangan omzet, dan file sempat ditulis ke /tmp. Perbaikan:
- "Aturan wajib" di awal SKILL.md: fakta hanya dari kamu, angka & skor dari script, tanpa file di /tmp, plus daftar nilai tambah (skor berbobot, rencana uji 7 hari berangka, tanda risiko/legal).
- `rencana` kini mencetak **KONSISTENSI**: bila harga per satuan sama/lebih murah dari harga lama atau pesaing, ditandai turun harga (sebut dampak ke pelanggan lama); dengan `--gap-omzet`, target uji dihubungkan ke kekurangan omzet per bulan.

## Catatan revisi 1.0.6 (2026-10-01)
Dari uji ulang OpenClaw: saran paket laundry keluar Rp8.000–9.000/kg padahal harga
sendiri Rp6.000/kg dan pesaing Rp5.000/kg, dan pada kasus money game AI mengutip pasal
KUHP lama (378/372) yang sudah tidak berlaku sejak KUHP baru (UU 1/2023) berlaku
2 Januari 2026. Perbaikan:
- **Cek kewajaran harga otomatis.** `skor_ide.py rencana` kini bisa menghitung harga dari
  **biaya + margin** (`--margin-target`), menampilkan **harga per kg/porsi** untuk paket
  (`--isi-per-unit`, `--satuan`), lalu membandingkannya dengan harga kamu sendiri
  (`--harga-lama`) dan harga pesaing (`--harga-pesaing`): hasilnya WAJAR / CEK / BELUM
  DICEK. Harga yang lebih mahal dari acuan diberi peringatan dan harus disertai nilai tambah
  nyata atau diturunkan.
- **Titik berhenti dini** di rencana 7 hari: Hari 3 masih 0 → ganti tawaran/kanal; Hari 5
  di bawah ambang → hentikan uji dan hemat sisa biaya. Ditambah 2 tanda bahaya (pre-mortem)
  yang dipantau Hari 1–3.
- **Tanpa pasal pidana kecuali diminta.** Untuk ide terlarang AI menjelaskan bahayanya
  dengan bahasa awam; bila kamu minta dasar hukumnya, rujukan terkini (KUHP baru Pasal
  492 penipuan & Pasal 486 penggelapan, Kontak OJK 157, Satgas PASTI) ada di
  `references/rujukan-kasus-terlarang.md` (dicek 1 Oktober 2026).
- 8 tes baru (total 87 tes, semua lulus).
