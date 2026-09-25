# HASIL UJI — kebijakan-privasi-pdp (Tahap 6, penguji independen)

- **Tanggal:** 2026-09-25 · **Penguji:** agent terpisah dari pembuat, hanya membaca folder skill · **Platform:** `claude-code (simulasi agent)`
- **Lokasi uji:** salinan skill di scratchpad (`.../scratchpad/uji-pdp/kebijakan-privasi-pdp/`), script dijalankan dari salinan. Tidak ada perubahan pada file skill selain folder `examples/`.
- **Script:** `cek_kebijakan.py` v1.0.0, Python 3 (Linux). Tes bawaan `tests/uji_regresi.py`: **LULUS 53 uji**.

## 1. Ringkasan skenario
| # | Skenario | Mode | Hasil | Catatan |
|---|---|---|---|---|
| 01 | Toko fashion Kirana Wear (WooCommerce+WA, Midtrans, JNE/J&T, Meta Pixel, GA, hosting SG), ID+EN | SUSUN | ✅ Lulus | Skor 100/100 ID & EN, 0 frasa berisiko, tidak ada karangan, SG disebut di transfer LN |
| 02 | Klinik gigi: persetujuan pasien baru Google Form + WA | PERSETUJUAN | ✅ Lulus dengan catatan | Data spesifik dikenali, peringatan Google Form; template D bertentangan dengan aturan "bisa ditolak tanpa kehilangan layanan" & memakai tanda tangan (tak ada di GForm) |
| 03 | Cek kebijakan salinan template luar (jual data, persetujuan dianggap, GDPR, tanpa masa simpan) | CEK | ✅ Lulus dengan catatan | 3 frasa TINGGI terdeteksi; skor 47 diverifikasi manual (7,5/16); 1 salah-positif unsur (cara ajukan) |
| 04 | "buatin privacy policy dong" | tanya sekali | ✅ Lulus | 8 pertanyaan bernomor dalam 1 pesan + opsi cepat |
| 05 | Minta klausul jual database + sembunyikan kebocoran | di luar cakupan | ✅ Lulus | Menolak dengan dasar Ps. 65/67/46/57, alternatif opt-in, checklist darurat, rujuk konsultan/polisi |
| A/B | Skenario 01 tanpa vs dengan skill | — | ✅ **Dengan skill jauh lebih baik** (53 vs 21 dari 55; script 100 vs 67) | Metode: baseline ditulis penguji yang sama (bias diakui) |
| Pesaing | phuryn/pm-skills `privacy-policy` | — | ✅ **Skill kita menang** (44 vs 21 dari 45) | Pesaing generik GDPR/US: tenggat 30 hari & batas anak 13 th (COPPA) salah untuk UU PDP; tak ada skill khusus UU PDP di ClawHub/skills.sh |

## 2. Uji script
### 2a. Data rusak — semua ditangani ✅ (kecuali dua catatan)
| Input | Hasil |
|---|---|
| File kosong / hanya spasi | `GALAT: File kosong…` exit 2 ✅ (JSON: `{"galat": …}`) |
| File tidak ada / folder / tanpa argumen | GALAT jelas, exit 2 ✅ |
| .docx (PK), PDF, biner | GALAT dengan saran simpan ulang ✅ |
| UTF-8 BOM, cp1252, UTF-16 ber-BOM | Terbaca, skor sama dengan versi UTF-8 ✅ |
| UTF-16 **tanpa BOM** | Ditolak sebagai "biner" (R-3) |
| HTML mentah (berbaris & minified) | Skor sama 100/100 ✅; jumlah kata membengkak (922→1239) karena tag dihitung; `<b>dapat</b> menjual` dan `dapat&nbsp;menjual` **tidak terdeteksi** (R-2) |
| Bahasa Inggris saja | 100/100 ✅ pola EN berfungsi |
| File sangat besar | 20 MB tanpa frasa berisiko: 14 detik. Dengan banyak frasa berisiko waktu **kuadratik**: 137 KB 0,2 dtk → 548 KB 1,1 dtk → 2,2 MB 10 dtk → 27 MB > 2 menit (dihentikan). Daftar risiko tak dibatasi (14.400 entri) (R-1) |

### 2b. Akurasi deteksi frasa berisiko (45 kalimat uji, `neg/cases.py` di scratchpad)
**Benar 28/45 · salah-positif 4 · salah-negatif 13.**
- ✅ Negasi yang benar: "Kami tidak pernah menjual…", "tidak akan pernah menjual atau menyewakan", "We do not sell / will never sell / will not sell, rent or trade", "Data tidak disimpan selamanya", "Kami tidak membagikan… pihak ketiga mana pun tanpa persetujuan".
- ✅ Kalimat campuran "Kami tidak menjual data Anda, tetapi kami dapat menjual data agregat…" tetap ditandai.
- ❌ **Salah-positif TINGGI:** "Data Anda **tidak akan dijual**." dan "Data Anda tidak dapat dijual kepada siapa pun." → ditandai TINGGI "menjual data" (kata negasi berada **di dalam** kecocokan pola `data[^.\n]{0,40}(dapat|…|akan) dijual`, sedangkan cek negasi hanya melihat teks sebelum kecocokan / awal kecocokan). Kalimat ini **umum** di kebijakan Indonesia yang patuh.
- ❌ Salah-positif lain: "Persetujuan tidak dianggap diberikan…" (TINGGI), "Kami tidak akan mengubah kebijakan ini tanpa pemberitahuan terlebih dahulu" (SEDANG), "Tidak ada sistem/metode… yang 100% aman" (SEDANG — muncul di output A/B & pesaing; kalimat ini justru jujur).
- ❌ Salah-negatif: "We may **sell or rent** your personal information", "We may share and sell your data", "memperdagangkan / menukar / mengalihkan dengan imbalan / memonetisasi data", "disimpan secara permanen", "tidak bertanggung jawab **jika data bocor**", "dibebaskan dari tanggung jawab", "dapat berubah sewaktu-waktu" (tanpa kata "tanpa pemberitahuan").

### 2c. Akurasi deteksi unsur (13 kalimat uji, `neg/unsur.py`)
Benar 2/13. Contoh salah:
- **Negasi dihitung ADA:** "Kami **tidak akan** memberi tahu Anda bila terjadi kebocoran." → unsur *kebocoran* = ADA (kata "tidak akan" di luar kecocokan, TOLAK tidak melihatnya).
- "Server kami berada di Singapura" / "server Amerika Serikat milik Google" → *transfer LN* TIDAK ADA (juga di output A/B: "server hosting … di Singapura" tidak dikenali).
- "Kami menyimpan data Anda selama 2 tahun" → *masa simpan* TIDAK ADA; tetapi "disimpan selama diperlukan" (kabur) → ADA.
- "Hubungi kami di 0812…" → *cara mengajukan* ADA (salah-positif, juga di skenario 03).
- "Kebijakan ini berlaku untuk Toko Kue Mawar" / "usaha milik Ibu Rina" → *identitas* TIDAK ADA.
- "mencabut persetujuan" (sinonim) tidak dikenali; "Penggunaan Informasi" tidak dihitung sebagai *tujuan*; "Akses, penghapusan…" tidak dihitung sebagai hak akses.
- "di bawah 18 tahun" tidak memicu unsur data anak (hanya pola EN `under 1[3-8]`).

### 2d. Verifikasi rumus skor (manual)
Rumus dinyatakan: Σ bobot terpenuhi ÷ Σ bobot berlaku × 100 (hak subjek bobot 2, proporsional 4 sub-hak; unsur bersyarat +1 bila terpicu).
| Kasus | Hitung manual | Script |
|---|---|---|
| 03 salinan | (1+1+1+1+1,5+1+1) = 7,5 ÷ (15+1) = 46,875 → 47 | 47 ✅ |
| A/B tanpa skill | 10 ÷ 15 = 66,7 → 67 | 67 ✅ |
| Pesaing | kontak, identitas, jenis, dasar, penerima, LN, masa simpan, cara, keamanan, tanggal, perubahan = 11 + hak 1,5 = 12,5 ÷ (15+1 anak) = 78,1 → 78 | 78 ✅ |
| 02 form | kontak, tujuan, dasar, LN, keamanan, data spesifik = 6 + hak 2×2/4 = 1 → 7 ÷ 16 = 43,75 → 44 | 44 ✅ |
Rumus & pembulatan konsisten; status mengikuti ambang ≥85/60 sesuai `references/checklist-uu-pdp.md`.
- ⚠ **Template kosong** (`templates/kebijakan-privasi.md`, 46 isian) mendapat **100/100** (status PERLU DILENGKAPI). Skor mengukur struktur, bukan isi — angka "100/100" di header output (format SKILL.md) bisa menyesatkan pengguna awam.

## 3. Kebenaran hukum (dicek via web search 2026-09-25)
| Klaim skill | Hasil cek | Status |
|---|---|---|
| Ps. 4 ayat (2) data spesifik (kesehatan, biometrik, genetika, kejahatan, anak, keuangan) | Sesuai | ✅ |
| Ps. 20 ayat (2) 6 dasar pemrosesan | Sesuai | ✅ |
| Hak subjek Ps. 5–13; tarik persetujuan Ps. 9 → berhenti 3×24 jam (Ps. 40); akses Ps. 32; perbaikan Ps. 30 | Sesuai (sumber sekunder, pasal.id) | ✅ |
| Ps. 46: pemberitahuan tertulis ≤ 3×24 jam ke subjek data & lembaga; isi minimal | Sesuai (Kompas, Hukumonline) | ✅ |
| Ps. 53 DPO + Putusan MK 151/PUU-XXII/2024 ("dan" → "dan/atau", cukup satu syarat) | Sesuai (Hukumonline, MKRI, GRP Law) | ✅ |
| Ps. 56 transfer LN (setara → memadai & mengikat → persetujuan) | Ayat (1)–(3) sesuai; ayat persetujuan tidak saya baca langsung | ✅/⚠ |
| Ps. 57 sanksi administratif, denda maks 2% pendapatan tahunan | Sesuai | ✅ |
| Ps. 65 larangan, Ps. 67 (5 th/Rp5 M; 4 th/Rp4 M; 5 th/Rp5 M) | Sesuai | ✅ |
| Ps. 68 pemalsuan — references: "denda Rp5 M vs Rp6 M, PERLU REVIEW" | Tempo, IDN Times, Hukumonline: **6 tahun / Rp6 miliar** → bisa diselesaikan | ✅ (perbarui references) |
| Ps. 70 korporasi denda maks 10× | Sesuai (dari ingatan + references) | ✅ |
| PP 33/2026: ditetapkan & diundangkan 16 Juli 2026, berlaku 16 Jan 2027, 225 pasal | Sesuai (Hukumonline Pro, CBQA, KRES, Meridian, Katadata) | ✅ |
| PP 33/2026: LN 2026 No. 88, 12 bab | **Tidak terverifikasi** oleh penguji | ⚠ |
| Lembaga pengawas belum terbentuk; fungsi sementara Kemkomdigi (Ditjen Pengawasan Ruang Digital) | Sesuai (CNBC 16 Sep 2026, Bisnis 13 Sep 2026, Kompas 27 Jul 2026) | ✅ |
| Permenkes 24/2022 Ps. 39: RME disimpan ≥ 25 th sejak kunjungan terakhir | Sesuai (Kemkes PDF, FH UI) | ✅ |
| UU KUP Ps. 28 ayat (11): 10 tahun | Sesuai | ✅ |
| Script: identitas "UU 27/2022 Pasal 21 & **31**" | Ps. 31 = kewajiban merekam kegiatan pemrosesan, bukan identitas pengendali | ⚠ rujukan kurang tepat |
| Script: kontak "Pasal 46 ayat **(2)** (narahubung)" | Ps. 46 ayat (2) UU = isi pemberitahuan (data terungkap, kapan/bagaimana, penanganan); narahubung disebut sumber sekunder PP 33/2026 | ⚠ rujukan kurang tepat |
| PP 33/2026 soal data anak (identifikasi anak, verifikasi persetujuan orang tua, transisi saat dewasa) | Diberitakan Katadata; **belum ada di skill** | ℹ celah kecil |
| Disclaimer "bukan nasihat hukum" + tanggal cek + status PP & lembaga | Ada di SKILL.md, README, references, dan output | ✅ |

## 4. Bug/temuan berprioritas
### TINGGI
- **T-1 Salah-positif TINGGI pada kalimat patuh "Data Anda tidak akan dijual" / "tidak dapat dijual".** Lokasi: `scripts/cek_kebijakan.py` RISIKO pola `data[^.\n]{0,40}(dapat|boleh|akan|bisa) dijual` + `cari_risiko()` (cek negasi hanya sebelum `m.start()` & awal kecocokan). Dampak: mode CEK menyuruh pengguna "Hapus" kalimat yang benar dan menurunkan status ke PERLU PERBAIKAN. Perbaikan: cek juga negasi **di dalam** kecocokan (mis. `re.search(r"\b(tidak|tak|bukan|never|not)\b", m.group(0))` untuk pola bertanda `cek_negasi`), atau ubah pola menjadi `data[^.\n]{0,40}(?<!tidak )(?<!tak )(dapat|boleh|akan|bisa) dijual` dan tambahkan kasus uji regresi.
- **T-2 Negasi dihitung sebagai unsur terpenuhi** ("Kami tidak akan memberi tahu Anda bila terjadi kebocoran" → kebocoran ADA). Lokasi: `ada()` + `TOLAK` hanya memeriksa teks kecocokan. Perbaikan: periksa ±40 karakter sebelum kecocokan pada kalimat yang sama (seperti `cari_risiko`) untuk unsur `kebocoran`, `perubahan`, `transfer_ln`; tambah tes.
### SEDANG
- **S-1 Salah-negatif frasa jual data berbahasa Inggris yang sangat umum** ("may sell or rent your personal information", "share and sell"). Lokasi: pola `(may|can|will) (sell|rent|trade) (your )?…`. Perbaikan: izinkan konjungsi, mis. `(may|can|will)( \w+){0,3} (sell|rent|trade)[^.\n]{0,40}(data|information)` + cek negasi; tambah sinonim ID "memperdagangkan|menukar|memonetisasi|mengalihkan … imbalan".
- **S-2 Skor 100/100 untuk template yang belum diisi (46 isian).** Lokasi: `periksa()`; SKILL.md format output menaruh "Skor cek: 100/100" di baris pertama. Perbaikan: tampilkan "Skor struktur 100/100 · 15 isian kosong" atau kurangi nilai unsur yang buktinya berada pada baris ber-`[isi:]`; di SKILL.md jelaskan bahwa skor = kelengkapan struktur.
- **S-3 Deteksi unsur rapuh untuk kalimat Indonesia biasa**: "server … di Singapura" (transfer LN), "Kami menyimpan data Anda selama 2 tahun" (masa simpan), "mencabut persetujuan", "Penggunaan Informasi" (tujuan), "di bawah 18 tahun" (pemicu anak), identitas "berlaku untuk [nama]"/"milik". Salah-positif: "Hubungi kami di …" = cara mengajukan. Lokasi: pola `UNSUR`/`UNSUR_BERSYARAT`. Perbaikan: tambah pola (nama negara/kota umum: singapura, amerika, eropa, jepang; `menyimpan data[^.\n]{0,30}selama`; `mencabut`; `penggunaan (data|informasi)`; `di bawah (umur|\d{2} tahun)`), hapus `di` dari pola `hubungi kami (…)` atau syaratkan kata "permintaan/hak".
- **S-4 Template D (klinik) bertentangan dengan aturan Mode 2**: kotak persetujuan "*(wajib untuk pelayanan)*" menjadikan persetujuan syarat layanan, padahal SKILL.md meminta persetujuan "bisa ditolak tanpa kehilangan layanan inti"; dasar pelayanan & rekam medis lebih tepat "pelaksanaan perjanjian/kewajiban hukum". Juga memakai "Tanda tangan" yang tidak ada di Google Form. Lokasi: `templates/pemberitahuan-persetujuan.md` bagian D. Perbaikan: jelaskan dasar pemrosesan di teks, jadikan persetujuan eksplisit untuk data kesehatan sebagai pernyataan + opsi "isi langsung di klinik"; tambah varian "D-online (Google Form)".
- **S-5 "100% aman" ditandai walau dinegasikan** ("Tidak ada sistem yang 100% aman"). Lokasi: pola RISIKO "100 ?% aman" (`cek_negasi=False`). Perbaikan: set `cek_negasi=True` + cek negasi dalam kalimat.
### RENDAH
- **R-1 Kinerja kuadratik** pada file besar berisi banyak frasa berisiko (`t.count("\n", 0, m.start())` per kecocokan) dan daftar risiko tak terbatas. Perbaikan: hitung nomor baris dengan `bisect` atas indeks newline; batasi ukuran file (mis. > 2 MB → GALAT/peringatan) dan jumlah temuan per pola (mis. 20).
- **R-2 HTML mentah**: tag dan entitas (`<b>`, `&nbsp;`) memutus pola; jumlah kata membengkak. Perbaikan: di `normalisasi()` buang tag `<[^>]+>`, `<script>/<style>` dan `html.unescape()`.
- **R-3 UTF-16 tanpa BOM** ditolak sebagai biner, padahal SKILL.md menyebut UTF-16 "terbaca otomatis". Perbaikan: deteksi pola byte nol berselang, atau ubah kalimat SKILL.md menjadi "UTF-16 ber-BOM".
- **R-4 Rujukan pasal kurang tepat di script**: identitas "Pasal 21 & 31", kontak "Pasal 46 ayat (2) (narahubung)". Perbaikan: identitas → Ps. 21 (dan informasi pemrosesan); kontak → Ps. 21 (+ "narahubung menurut PP 33/2026, pasal belum diverifikasi").
- **R-5 references/dasar-hukum.md Ps. 68** masih "PERLU REVIEW Rp5 M vs Rp6 M" — sumber (Tempo, IDN Times, Hukumonline) konsisten **Rp6 miliar/6 tahun**.
- **R-6 Tingkat GDPR/CCPA tidak konsisten**: script SEDANG, checklist C bagian 2 menyebut TINGGI.
- **R-7 Alasan risiko berbahasa Inggris** tampil untuk pengguna Indonesia bila frasanya berbahasa Inggris (mis. "We may sell…"). Perbaikan: pakai alasan ID (sebut juga EN bila perlu).
- **R-8 SKILL.md**: tidak ada panduan bila tenggat 3×24 jam kebocoran **sudah lewat** (skenario 05); opsi "jawab 1–3 saja" untuk pengguna yang ingin cepat belum tertulis; pertanyaan data kesehatan/anak (wajib) hanya tersirat di pertanyaan no. 3.
- **R-9 README** menyebut `CARA-INSTAL.md`, sedangkan CLAUDE.md menyatakan paket berisi `docs/instalasi.md` — pastikan nama file sesuai hasil `build.py`.
- ℹ Saran dari banding pesaing: tambahkan ringkasan 3–5 baris di awal output mode SUSUN dan pengingat perjanjian pengendali–prosesor (Ps. 51); celah PP 33/2026 data anak (identifikasi & verifikasi persetujuan orang tua) untuk aplikasi/layanan anak.

## 5. Skor kualitas: **7/10** — lulus bersyarat (perbaiki T-1, T-2, S-1, S-4 sebelum beta)
Alasan:
- (+) Output utama (mode SUSUN, PERSETUJUAN, TANGGAPI, penolakan) sangat baik: siap tempel, tidak mengarang, dasar pemrosesan per data, 3×24 jam, transfer LN jujur, disclaimer dan status PP/lembaga akurat. Klaim hukum inti terverifikasi.
- (+) **Menang jelas** di uji A/B (53 vs 21) dan **menang telak** atas pesaing (44 vs 21) — batas maks 6 tidak berlaku.
- (+) Penanganan input rusak baik; rumus skor terbukti konsisten dengan hitung ulang manual.
- (−) Pemeriksa kata kunci (inti mode CEK) punya salah-positif pada kalimat patuh yang umum ("tidak akan dijual" → TINGGI) dan salah-negatif pada frasa jual data EN yang umum; akurasi uji negasi/sinonim 28/45 dan unsur 2/13. SKILL.md memang mewajibkan agent membaca manual (checklist C), sehingga risiko tertahan, tetapi pengguna yang menjalankan script langsung (README menawarkan ini) bisa tersesat.
- (−) Template D klinik tidak konsisten dengan aturan persetujuan skill sendiri.
Setelah revisi T-1/T-2/S-1..S-5 dan penambahan tes regresi untuk kasus di §2b–2c, perlu uji ulang oleh penguji independen (fokus mode CEK).

## Lampiran — sumber yang dicek
- Hukumonline, MK Ps. 53: https://www.hukumonline.com/berita/a/lindungi-maksimal-data-pribadi--mk-tegaskan-kata-dan-dalam-pasal-53-uu-pdp-inkonstitusional-lt688a2dc5c249f/
- MKRI Putusan 151/PUU-XXII/2024: https://s.mkri.id/public/content/persidangan/putusan/putusan_mkri_12970_1753859809.pdf
- Hukumonline Pro, PP 33/2026 berlaku 16 Jan 2027: https://pro.hukumonline.com/a/lt6a97c3fe4527c/pemerintah-akhirnya-terbitkan-kerangka-implementasi-pelindungan-data-pribadi--berlaku-mulai-16-januari-2027
- CBQA (16 Sep 2026): https://cbqaglobal.com/id/blog/2026/09/16/pp-33-tahun-2026-memahami-kewajiban-dan-prioritas-organisasi-dalam-pelindungan-data-pribadi/
- Katadata, PP 33/2026 data anak: https://katadata.co.id/finansial/makro/6a9979b7c5745/pp-pelindungan-data-pribadi-berlaku-januari-2027-ini-aturan-baru-data-anak
- CNBC Indonesia (16 Sep 2026): https://www.cnbcindonesia.com/tech/20260916115609-37-768328/lembaga-perlindungan-data-belum-ada-di-ri-padahal-aturannya-sudah-ada
- Bisnis.com (13 Sep 2026): https://teknologi.bisnis.com/read/20260913/84/2003698/pembentukan-badan-pdp-dipercepat-implementasi-uu-pdp-dinilai-belum-efektif
- Kompas, Ps. 46 3×24 jam: https://regional.kompas.com/read/2026/07/17/174858878/pemprov-wajib-beri-tahu-korban-kebocoran-data-pengamat-sesuai-uu-pdp
- Tempo, Ps. 68 Rp6 M: https://www.tempo.co/hukum/uu-pdp-disahkan-pemalsu-data-pribadi-diancam-denda-hingga-rp6-miliar-271543
- pasal.id Ps. 56: https://pasal.id/peraturan/uu/uu-no-27-tahun-2022/pasal-56 · Ps. 9: https://pasal.id/peraturan/uu/uu-no-27-tahun-2022/pasal-9
- Permenkes 24/2022 (Kemkes): https://keslan.kemkes.go.id/unduhan/fileunduhan_1662611251_882318.pdf
- Pesaing: https://github.com/phuryn/pm-skills/blob/main/pm-toolkit/skills/privacy-policy/SKILL.md · https://github.com/PGScully/privacy-skill

---

## Uji ulang v1.0.1 (penguji independen kedua, 2026-09-25)
- **Penguji:** agent terpisah (bukan pembuat/perevisi), salinan skill di scratchpad `.../uji2-pdp/`. Platform: `claude-code (simulasi agent)`. Rincian lengkap: `06-uji-ulang-v1.0.1.md`.
- **Anti-overfitting:** set uji baru ditulis penguji sebelum membuka `tests/`. Tes bawaan: **LULUS 133 uji**. SKILL.md 149 baris.
- **Akurasi set baru:** frasa **41/48 (85%)** — FP 1, FN 6; unsur **60/65 (92%)** — FP 3, FN 2 (22 kalimat + 3 dokumen utuh: lengkap-patuh 14/14 & 100/100 CUKUP LENGKAP; setengah jadi 12/14; template AS 14/15). Semua kalimat patuh bernegasi (termasuk negasi ganda & klausa majemuk) benar → T-1/T-2/S-5 beres dan tidak kambuh.
- **Temuan lama:** T-1 ✅, T-2 ✅, S-1 ⚠ sebagian, S-2 ✅ (template kosong 84/100 BELUM SIAP), S-3 ⚠ sebagian besar, S-4 ✅ (template D & D-online: layanan = perjanjian + kewajiban hukum, persetujuan hanya tujuan tambahan & bisa ditolak, tanpa tanda tangan di GForm), S-5 ✅, R-1 ✅ (2 MB 1,97 dtk; > 5 MB GALAT), R-2 ✅ HTML, R-3 ✅ UTF-16 tanpa BOM, R-4..R-9 ✅. Skenario 03 diulang: ✅ lulus, skor 47 → 41 (FP cara ajukan hilang, diverifikasi manual).
- **Klaim hukum:** Ps. 5/21 identitas, Ps. 68 (6 th/Rp6 M), Ps. 46 (3×24 jam ke subjek & lembaga), PP 33/2026 (16 Jul 2026 → berlaku 16 Jan 2027), lembaga belum terbentuk/Kemkomdigi — semua ✅ terverifikasi via web search.
- **Bug baru:** SEDANG **B-1** berbagi data ke mitra iklan/pemasaran berbahasa Indonesia tidak terdeteksi (contoh majemuk "tidak menjual…, tetapi dapat membagikannya ke mitra iklan" lolos); SEDANG **B-2** "sell or rent aggregated and personal information" & "share … with advertisers" lolos di template luar. RENDAH: B-3 FP unsur (identitas "berlaku untuk layanan kami", kontak dari kata "WhatsApp", keamanan "is important"), B-4 status KURANG LENGKAP vs "BELUM SIAP" di SKILL.md, B-5 temuan ganda browse-wrap, B-6 FP/FN kecil, B-7 usia 13 (COPPA) tidak dikoreksi ke < 18, B-8 kunci `bukti` hilang di JSON hak_subjek.

### Skor kualitas uji ulang: **8/10** — LULUS (rekomendasi: perbaiki B-1 & B-2 sebelum beta; tidak perlu uji ulang penuh, cukup tes regresi + cek set `06`)
Alasan:
- (+) Semua temuan TINGGI (T-1, T-2) dan S-2, S-4, S-5 serta seluruh RENDAH beres; perbaikan tidak overfit — negasi andal pada 17/17 kalimat patuh baru, unsur 92% pada set baru, dokumen patuh buatan sendiri 100/100 tanpa salah tanda.
- (+) Template klinik kini konsisten dengan aturan persetujuan; klaim hukum inti terverifikasi; penanganan HTML/UTF-16/file besar baik.
- (+) Keunggulan A/B & banding pesaing dari uji pertama tetap berlaku (keluaran mode SUSUN/PERSETUJUAN tidak memburuk).
- (−) Mode CEK masih melewatkan pola "berbagi data untuk iklan" berbahasa Indonesia dan "sell/share" EN dengan kata sisipan — tepat di skenario salinan template luar. Risiko tertahan karena SKILL.md mewajibkan pembacaan manual checklist C, sehingga bukan penghalang lulus, tetapi pengguna yang menjalankan script sendiri bisa tidak diberi tahu.
