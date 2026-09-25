# HASIL UJI — brainstorming-ide-usaha (Tahap 6, penguji independen)

- **Tanggal:** 2026-09-25
- **Penguji:** agent terpisah dari pembuat (Claude Code, simulasi agent) — hanya membaca folder skill ini.
- **Lokasi uji:** salinan di scratchpad `uji-biu/brainstorming-ide-usaha/` (bukan `.claude/skills/`).
- **Platform:** `claude-code (simulasi agent)` — belum diuji di OpenClaw/Codex/Cursor asli.

## Ringkasan skenario

| # | File | Skenario | Jalur | Hasil |
|---|---|---|---|---|
| 00 | `00-pembanding-tanpa-skill.md` | A/B skenario 01 | – | **Dengan skill menang jelas** (30 vs 17 dari 35) |
| 00 | `00-banding-pesaing.md` | vs obra/superpowers `brainstorming` & phuryn/pm-skills `brainstorm-ideas-existing` | – | **Skill kita menang** (30 vs 13 vs 20) |
| 01 | `01-warung-makan-sepi-siang.md` | Warung makan sepi siang, modal ≤ Rp5 jt | B | Lulus. Impas 125/500/143 unit diverifikasi independen. |
| 02 | `02-toko-hijab-harbolnas-1111.md` | Toko hijab online, ide promo 11.11 | B (+skor atas persetujuan) | Lulus. Skor 4,105…3,368 diverifikasi; serah-terima ke `promo-kalender` jelas. |
| 03 | `03-freelancer-desain-diversifikasi-cepat.md` | Freelancer desain, "cepat, jangan banyak tanya" | C (mode instan) | Lulus dengan catatan: gerbang persetujuan & bobot default harus ditafsirkan agent. Skor & impas (27) diverifikasi. |
| 04 | `04-input-tidak-lengkap.md` | "kasih ide usaha dong" | C | Lulus, tapi 5 giliran tanya sebelum ide pertama. |
| 05 | `05-di-luar-cakupan-kripto-arisan-berantai.md` | Kripto dijamin untung + arisan berantai | tolak | Lulus: ditolak sopan + alasan + alternatif legal, tanpa janji untung. |

## Script `scripts/skor_ide.py`

- Tes bawaan: `python3 test_skor_ide.py` → **32 tes OK**.
- Verifikasi angka independen (Python terpisah, Σ nilai×bobot ÷ Σ bobot; `ceil(modal/margin)`): semua skor skenario 02 & 03 dan contoh pembuat (4,278 … 2,778) **cocok**; impas 125/500/143/27/334/200 **cocok**. Bobot total bukan 100 (mis. 60+30=90) dinormalisasi dengan benar (Ide Y 3,667; Ide X 3,333). Skor seri terdeteksi (3 ide 3,400).
- Data rusak yang **ditangani baik** (pesan jelas, exit 1): CSV kosong, header saja, nilai 0/6/teks/`nan`, ide duplikat (huruf sama), file tidak ada, bobot nol semua/negatif/`"3,5"`, margin negatif/nol.

## Bug & temuan berprioritas

### TINGGI
1. **Koma desimal tanpa kutip menggeser kolom diam-diam → skor salah tanpa peringatan.** CSV `Ide Y,3,5,4` (maksud: 3,5 dan 4) pada baris selain baris data pertama dibaca sebagai a=3, b=5; nilai ke-4 dibuang `csv.DictReader` (kunci `None`) tanpa error. Hasil: 3,800 padahal seharusnya 3,700, exit 0. (Kalau terjadi di baris data pertama baru ditolak, dengan pesan membingungkan "kolom … tidak ada di file bobot: [None]".) Lokasi: `scripts/skor_ide.py` `baca_ide()` — header diambil dari `baris_list[0].keys()`, baris dengan kolom berlebih tidak dicek.
   **Perbaikan:** tolak setiap baris yang punya kunci `None` / jumlah kolom ≠ header, dengan pesan "baris N punya kolom berlebih — kalau pakai koma desimal (3,5), tulis 3.5 atau beri tanda kutip". Tambah tes.

### SEDANG
2. **CSV gaya Excel Indonesia ditolak dengan pesan menyesatkan.** File ber-BOM (Excel "CSV UTF-8") dan pemisah titik koma → "file ide wajib punya kolom 'nama_ide'" padahal kolomnya ada. Koma desimal berkutip `"3,5"` → "bukan angka". Lokasi `baca_ide()`. **Perbaikan:** baca dengan `encoding="utf-8-sig"`, deteksi pemisah (`csv.Sniffer` atau cek `;` di header), terima `3,5` → 3.5, strip spasi di header.
3. **Bobot `NaN`/`Infinity` di JSON diterima** → semua skor `nan`, exit 0 (Python `json` menerima literal ini). `true` diterima sebagai bobot 1. Lokasi `baca_bobot()`. **Perbaikan:** tolak `bool` dan nilai non-finite (`math.isfinite`).
4. **"Satu pertanyaan per pesan" bertentangan dengan prinsip instan CLAUDE.md §1** ("tanyakan sekali dalam satu pesan berisi daftar pertanyaan singkat"). Skenario 04 butuh 5 giliran sebelum ide pertama; A/B & pesaing juga menunjukkan ini satu-satunya kelemahan. Lokasi `SKILL.md` Jalur B.1 & C.2. **Perbaikan:** satu pesan berisi 3–5 pertanyaan pilihan ganda (modal, waktu/tenaga, lokasi, keahlian/aset, target), susulan hanya jika ambigu.
5. **Batas Jalur B vs C tidak konsisten, dan Jalur B tidak punya alat hitung.** Definisi SKILL.md: produk/jasa baru untuk usaha yang sudah jalan = B; tetapi contoh pembuat (laundry tambah layanan) dilabeli C. Jalur B.4 meminta "waktu balik modal kasar" tapi `impas` hanya disebut di C.8; skor tertimbang hanya di C.5 (penguji memakainya di 01/02 atas inisiatif sendiri). **Perbaikan:** izinkan/wajibkan `impas` di B.4 dan skor opsional di B bila ide ≥ 4; samakan label contoh pembuat atau perjelas kriteria.
6. **Tidak ada bobot default resmi.** SKILL.md: "kriteria & bobot wajib disepakati atau memakai default yang disebutkan", tapi hanya kriteria default yang disebut; bobot hanya contoh di template. Mode cepat (skenario 03) memaksa agent mengarang. **Perbaikan:** tetapkan bobot default eksplisit di SKILL.md Input (mis. contoh template 5/4/3/2/4 atau semua sama) dan wajib disebut sebagai asumsi.
7. **Mode "cepat" vs gerbang persetujuan wajib Jalur C tidak diatur.** Lokasi `SKILL.md` Prinsip instan + C.7. **Perbaikan:** tulis aturan: di mode cepat, sajikan ide + skor + rekomendasi dalam satu pesan, gerbang cukup satu kata ("ketik 1/2/3 atau 'lanjut'").

### RENDAH
8. **Traceback mentah (bukan pesan awam):** CSV encoding ANSI/cp1252 (`UnicodeDecodeError`), path berupa folder (`IsADirectoryError`), `impas --modal nan`/`inf` (`ValueError`/`OverflowError`). `--modal 5.000.000` (format Indonesia) → pesan argparse berbahasa Inggris. Lokasi `baca_ide()`, `baca_bobot()`, `hitung_impas()`, `buat_parser()`. **Perbaikan:** tangkap `OSError`/`UnicodeDecodeError`, cek `math.isfinite`, parser angka yang menerima `5.000.000`/`5000000`.
9. **Tampilan `impas` membulatkan margin** (`--margin 2500.5` tampil "Rp2.500", `0.1` tampil "Rp0") sementara hitungan memakai nilai asli — tampilan tidak cocok dengan hitungan. Label "Modal awal        :" kurang satu spasi (tidak sejajar). Istilah "unit" kurang pas untuk jasa/langganan.
10. **Ambang lanjut/berhenti di `templates/kerangka-uji-murah.md` bercelah:** "perbaiki 6–9 dari 10", "hentikan <30%" → 3–5 dari 10 tidak punya aturan (juga di contoh pembuat). **Perbaikan:** "perbaiki jika 30–99% target".
11. **`references/musim-dan-momentum.md`:** "Gajian / tanggal muda 1 & 25–30" tumpang tindih dengan "Tanggal tua 20–28"; 12.12 disebut dua kali di baris Harbolnas; "1.1" bukan umum disebut tanggal kembar Harbolnas. Tahun ajaran baru "pertengahan Juni–Juli" masuk akal (tahun ajaran mulai ±pertengahan Juli; belanja Juni–Juli). Ramadan/Lebaran **tidak diberi tanggal** dan ada peringatan wajib cek — baik (perkiraan 2027: awal Ramadan ±8 Feb, Idulfitri ±10 Mar, belum resmi).
12. **Kategori terlarang tanpa dasar aturan.** CLAUDE.md Tahap 4.5 meminta dasar aturan + tanggal untuk domain sensitif. **Perbaikan:** 2–3 baris rujukan (UU 7/2014 tentang Perdagangan — larangan skema piramida; perizinan OJK untuk penghimpunan dana/investasi; cek daftar entitas ilegal di OJK) + tanggal cek di `references/`.
13. Duplikat nama beda huruf/spasi (`Ide X` vs `ide x `) tidak terdeteksi; spasi di header (`nama_ide, a, b`) membuat kolom tidak cocok.
14. Emoji `❌`/`⚠️` pada `print` bisa memicu `UnicodeEncodeError` di Windows bila keluaran dialihkan (konsol non-UTF-8) — belum diuji di Windows asli.

## Pemeriksaan lain
- **Janji untung:** tidak ada. README FAQ tegas "tidak menjamin laku"; semua skenario menandai asumsi.
- **Bahasa awam:** baik; istilah SCAMPER/skor tertimbang/titik impas dijelaskan. Keluaran script "Peringkat/Skor Tertimbang/BEP" masih agak teknis tapi dijelaskan agent.
- **Perbedaan dengan skill lain:** jelas. `promo-kalender` (mekanisme & margin promo), `hitung-hpp` (HPP presisi), `riset-calon-pelanggan`, `proposal-kerjasama`, `kalender-konten-30hari`, `caption-sosmed-umkm` — semua ada di repo dan dirujuk dengan benar. Skenario 02 menunjukkan serah-terima yang mulus.
- **Keamanan script:** hanya membaca file lokal yang ditunjuk, tanpa jaringan/penulisan file. Aman.

## Skor kualitas: **7 / 10**

**Alasan:** Alur inti kuat dan terbukti menang — A/B jelas lebih baik (30 vs 17), mengalahkan dua pesaing (30 vs 13 / 20), domain & konteks Indonesia sangat baik, penolakan kategori terlarang tepat, semua angka yang dihasilkan cocok dengan verifikasi independen. Dikurangi karena: (1) bug TINGGI script yang bisa menghasilkan skor salah **diam-diam** saat pengguna memakai koma desimal — bertentangan dengan janji "angka dihitung, bukan dikira"; (2) CSV gaya Excel Indonesia (BOM, `;`, koma desimal) tidak didukung; (3) gaya tanya satu-per-satu membuat skill lambat bagi pengguna awam, berlawanan dengan prinsip instan; (4) aturan jalur/bobot default/mode cepat masih harus ditafsirkan agent.

**Rekomendasi:** perbaiki temuan #1–#3 (script + tes baru) dan #4–#7 (SKILL.md) sebelum naik status; setelah perbaikan, cukup uji ulang script dengan data rusak di atas + ulang skenario 03 & 04 oleh penguji independen. Target skor setelah revisi: 8–9.

---

## Uji ulang v1.0.1

- **Tanggal:** 2026-09-25
- **Penguji:** agent independen kedua (bukan pembuat, bukan perevisi), salinan di scratchpad `uji2-biu/`. Platform: `claude-code (simulasi agent)`.
- **Rincian lengkap:** [`06-uji-ulang-v1.0.1.md`](06-uji-ulang-v1.0.1.md).

**Ringkasan:**
- Tes bawaan: **60 tes OK**.
- Temuan lama #1–#14: **semua beres** (TINGGI #1 kini ditolak di baris mana pun dengan pesan jelas; CSV Excel ID ber-BOM/`;`/`3,5` terbaca benar; NaN/Infinity/true ditolak; cp1252, folder, `5.000.000`/`5jt`/`15rb`, margin < 1 ditangani dengan pesan Indonesia).
- Verifikasi independen (`fractions.Fraction`): 3.000 ide acak → 0 selisih skor; 8 kasus titik impas → semua cocok; skor skenario 04 mode cepat (4,167 … 3,278) cocok.
- Skenario 01 ulang: **1 giliran tanya** (sebelumnya 3). Skenario 04 ulang: 1 giliran tanya (sebelumnya 5); mode cepat jalan tanpa bertanya, bobot default resmi dipakai & disebut, gerbang persetujuan cukup satu balasan.
- Regresi: dasar aturan kategori terlarang benar (UU 7/2014 Pasal 9, UU 8/1995, UU 4/2023 P2SK), tidak ada janji untung, SKILL.md 110 baris.

**Bug baru (tidak ada yang tinggi):**
- B-5 (sedang-rendah): header dengan nama kolom kembar diterima diam-diam (kolom terakhir menimpa).
- B-2 (rendah-sedang): salah ketik/huruf besar di nama kolom default → diam-diam pindah ke bobot sama rata (sumber disebut di keluaran).
- B-1 nomor baris salah setelah baris kosong; B-3 header `Nama_Ide` huruf besar ditolak; B-4 koma ekor Excel → pesan `['']`; B-6 `--modal -5jt` pesan argparse Inggris; B-7 aturan gerbang singkat mode cepat hanya eksplisit di Jalur C; B-8 9.9/10.10/11.11 disebut "Harbolnas nasional" (resmi hanya 12.12).

## Skor kualitas uji ulang: **8 / 10**

**Alasan:** Semua temuan uji pertama diperbaiki dan terbukti lewat uji ulang, termasuk bug TINGGI yang bisa membuat skor salah diam-diam. Script kini tahan terhadap format Excel Indonesia dan angka rupiah gaya lokal, angka cocok 100% dengan hitungan independen (termasuk 3.000 ide), dan alur tanya sudah "instan" (satu pesan / mode cepat tanpa tanya) sesuai CLAUDE.md §1 tanpa kehilangan gerbang persetujuan. Belum 9 karena masih ada dua celah kecil yang bisa memberi hasil tidak sesuai maksud tanpa error (kolom header kembar, salah ketik nama kolom default → bobot sama rata) serta beberapa pesan error kecil yang kurang tepat.

**Rekomendasi:** **Lulus** (skor ≥ 7) — boleh naik ke status `lulus` menunggu uji platform asli. Perbaikan B-5 & B-2 disarankan pada revisi berikutnya (patch kecil + tes), tidak wajib uji ulang penuh.

## Uji ulang v1.0.2

- **Tanggal:** 2026-09-25.
- **Penguji:** agent independen ketiga (bukan pembuat/perevisi/penguji sebelumnya), salinan di scratchpad `uji3-biu/`. Platform: `claude-code (simulasi agent)`.

**Hasil:**
- `python3 scripts/test_skor_ide.py` → **72 tes OK** (sebelumnya 60).
- **B-1..B-8 semua beres**, diverifikasi dengan kasus baru: header kembar `nama_ide,a,a` → **ditolak** dengan pesan jelas (B-5); nama kolom default salah ketik/huruf besar (`Kesesuaian_Modal` dst.) → **dicocokkan via casefold** dan otomatis pakai bobot default resmi, bukan diam-diam sama rata lagi (B-2, kini lebih baik dari yang dilaporkan sebelumnya); baris kosong di tengah → nomor baris fisik benar (baris 4, bukan 3) (B-1); header `Nama_Ide` huruf besar diterima (B-3); koma ekor Excel (`nama_ide,a,b,`) dibuang otomatis (B-4); `--modal -5jt` → pesan Indonesia jelas "modal awal harus lebih besar dari 0" (B-6); gerbang persetujuan mode cepat kini eksplisit disebut di langkah B.5 & C.2 (B-7); `references/musim-dan-momentum.md` kini menulis "9.9, 10.10, 11.11 (kampanye diskon marketplace); 12.12 = Harbolnas nasional resmi" (B-8).
- **Cek Harbolnas via web search:** dikonfirmasi — Harbolnas resmi digagas 2012 dan dirayakan 12.12 oleh asosiasi e-commerce Indonesia (IdeA); 9.9/10.10/11.11 adalah promo tanggal kembar marketplace bulanan yang meniru pola Harbolnas, bukan Harbolnas resmi itu sendiri. Teks skill sekarang akurat.
- CSV Excel Indonesia baru (BOM + `;` + koma desimal + header UPPERCASE + baris kosong + koma ekor sekaligus): terbaca benar, skor 4,000 & 3,139 cocok dengan hitungan independen (`Fraction`).
- **250 ide acak** (nilai bulat & `,5`) dibanding hitungan independen `Fraction`: **selisih 0** untuk semua skor.
- Titik impas independen (`math.ceil` via `Fraction`) untuk 5 pasangan modal/margin dari contoh (125, 500, 143, 334, 27 unit): **semua cocok**. Data mentah contoh laundry (4,278…2,778) tidak disertakan sebagai CSV di repo sehingga tidak bisa dihitung ulang langsung dari file; formula (Σnilai×bobot/Σbobot) sudah diverifikasi identik lewat 250 kasus acak dan tidak berubah dari v1.0.1 yang sebelumnya mengonfirmasi angka itu.

**Bug baru:** tidak ditemukan yang baru pada rentang uji ini.

## Skor kualitas uji ulang v1.0.2: **9 / 10**

Semua temuan B-1..B-8 dari uji ulang v1.0.1 terbukti diperbaiki dengan benar, termasuk B-2 yang kini malah lebih ketat dari perbaikan minimum yang disarankan (bukan cuma catat sumber, tapi mencocokkan nama kolom secara toleran dan tetap pakai bobot resmi). Angka skor & titik impas 100% cocok independen pada 250 kasus acak + kasus format Excel Indonesia gabungan. Klaim Harbolnas terverifikasi via web search. Tidak naik ke 10 karena data mentah contoh laundry pembuat tidak tersedia sebagai file untuk verifikasi ulang persis, dan cakupan uji ini tidak mengulang skenario percakapan penuh (01-05) atau uji platform asli.
