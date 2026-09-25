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
