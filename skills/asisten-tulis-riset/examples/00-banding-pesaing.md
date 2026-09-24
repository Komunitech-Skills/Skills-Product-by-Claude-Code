# Uji Banding Pesaing — skill/prompt publik untuk "research writing with citations"

**Tanggal uji:** 2026-09-23
**Penguji:** agent penguji independen (simulasi, Claude Code)

## Pencarian yang dilakukan
- GitHub code search & web search: `"SKILL.md" research writing citations anti-hallucination sources`
- `github.com/VoltAgent/awesome-openclaw-skills` → kategori `search-and-research.md`
- `anthropics/skills` — tidak ditemukan skill riset+sitasi khusus di repo resmi ini (fokusnya berbeda:
  docx/pptx/xlsx/pdf/dsb).
- `manairalabs/bicara-skills`, `alvinindra/bahasa-skills` — dicoba dicari, tidak ditemukan repo/skill
  dengan nama tersebut yang aktif & relevan untuk riset+sitasi berbahasa Indonesia (kemungkinan sudah
  tidak ada / berganti nama / tidak publik). Dicatat sebagai "tidak ditemukan", bukan diasumsikan ada.
- `ComposioHQ/awesome-claude-skills` — **sengaja tidak dibuka** sesuai instruksi (repo tanpa lisensi
  terverifikasi); hanya dicatat keberadaannya dari hasil pencarian sebelumnya (lihat `ATTRIBUTION.md`
  skill ini, yang sudah mencatatnya sebagai kandidat kurasi yang ditolak untuk dibuka/disalin).

## Pesaing yang ditemukan & dinilai
**Nama:** `grounded-citations` (bagian dari `NousResearch/hermes-agent`)
**URL:** https://github.com/NousResearch/hermes-agent/blob/main/skills/research/grounded-citations/SKILL.md
**Lisensi:** MIT (frontmatter skill: `license: MIT`; juga ada file `LICENSE` MIT di root repo)
**Pembuat:** Hermes Agent (proyek NousResearch) + kontributor "Teknium" — organisasi AI dengan rekam
jejak publik (model Hermes), repo bukan koleksi AI-slop (struktur skill rapi, versi 1.2.0, terintegrasi
dengan skill lain seperti `arxiv`, `reddit-reading`, `rss-feeds`).
**Dibaca untuk dinilai saja — isinya TIDAK disalin ke skill kita.** Script `sources.py` milik pesaing
**tidak dijalankan** (sesuai instruksi), hanya dibaca teksnya.

### Ringkasan mekanisme pesaing
- Memakai **ledger mekanis** (`scripts/sources.py`, JSON) yang memetakan `url → [n]`. Model **tidak
  pernah mengetik ulang URL atau nomor** — nomor didapat langsung dari output perintah `sources.py add`.
  Ini **mencegah ID/URL karangan secara struktural**, bukan hanya lewat instruksi tertulis.
- Punya **mode evidence**: kutipan verbatim per sumber divalidasi otomatis oleh script — ditolak jika
  teks kutipan **tidak** ditemukan persis di halaman yang sudah diambil (`web_extract`).
- `verify --min-coverage` menghitung persentase kalimat berbasis fakta yang punya `[n]` atau
  `[unverified]`, dan gagal (exit code) jika di bawah ambang.
- Cakupan lintas platform (web, Reddit, RSS, YouTube, kode) untuk riset "apa kata orang", dengan aturan
  memisahkan opini komunitas vs fakta terverifikasi.
- Generik/lintas domain (Inggris), tidak spesifik Indonesia: tidak ada daftar sumber resmi per negara,
  tidak ada aturan SEO, tidak ada aturan integritas akademik untuk tugas kuliah, tidak ada gaya sitasi
  sederhana untuk pembaca awam (formatnya `[n]` + `Sources:` gaya akademik/Perplexity).

## Jalankan skenario S1 dengan instruksi pesaing (simulasi, tanpa eksekusi script)

Mengikuti prosedur `grounded-citations` secara manual (berperan sebagai agent yang memuat skill
tersebut, tanpa benar-benar menjalankan `sources.py`): reset ledger → untuk tiap sumber yang sama yang
sudah dibuka nyata di skenario S1 kita ([1] pajak.go.id/en/node/119081, [2] .../119105,
[3] .../106827) ledger akan mendaftarkan `[1]`, `[2]`, `[3]` dengan urutan sama seperti registrasi —
karena hanya 3 sumber dan urutan pemakaian sama, hasilnya **secara isi setara** dengan draf kita di
`01-draf.md`: klaim yang sama, kutipan `[n]` di kalimat yang sama. Perbedaan utama ada di **cara kerja**,
bukan isi akhirnya:

- Pesaing akan **menolak/menandai error** bila skema kutipan langsung ("...") pada frasa
  "paling lambat akhir bulan ketiga tahun pajak berikutnya" tidak ditemukan verbatim di teks halaman
  yang diambil — memaksa penulis mengetik ulang persis, bukan parafrase yang disamarkan sebagai kutipan.
  Draf kita menulis frasa itu **dalam tanda kutip** mengikuti isi asli [1]/[3] — konsisten, tapi
  verifikasinya di skill kita dilakukan manual oleh penguji (baca §Verifikasi di `HASIL-UJI.md`), bukan
  otomatis oleh script seperti pesaing.
- Sources block pesaing akan berbentuk daftar `Sources:` gaya Perplexity/akademik, bukan format
  "Judul. Lembaga. Tahun. URL. Diakses tanggal" yang lebih mudah dibaca pembeli UMKM awam.
- Pesaing tidak punya larangan menulis tugas kuliah untuk diserahkan sebagai karya sendiri (skenario S5
  kita) — di luar cakupannya sama sekali.
- Pesaing tidak punya panduan SEO (judul/meta description/H2-H3/kata kunci) yang dibutuhkan untuk
  skenario artikel blog SEO seperti S1.

## Tabel penilaian

| Kriteria | `asisten-tulis-riset` (kita) | `grounded-citations` (pesaing) |
|---|---|---|
| Kualitas mekanisme anti-halusinasi | Baik, tapi bergantung disiplin agent + cek heuristik pasca-tulis (`cek_sitasi.py`, regex per baris) | **Lebih kuat secara struktural** — ledger mencegah ID/URL dikarang dari sumbernya, bukan hanya dicek belakangan; mode evidence verifikasi kutipan verbatim otomatis |
| Kesesuaian konteks Indonesia | **Unggul** — daftar sumber resmi (BPS/OJK/BI/SINTA), gaya sitasi awam, aturan SEO ID, penolakan tugas kuliah, Bahasa Indonesia | Tidak ada sama sekali; generik lintas negara/domain |
| Akurasi (untuk hasil S1 yang sama) | Setara — sumber yang sama, dibuka & dicocokkan manual | Setara secara isi; lebih ketat secara mekanis untuk kutipan langsung |
| Siap pakai untuk pembeli awam (tanpa setup) | **Unggul** — 0 dependency, cukup Python standar opsional, tanpa perlu ledger/JSON, tanpa perlu paham CLI | Perlu menjalankan CLI Python multi-perintah (`reset`, `add`, `render`, `verify`) berkali-kali — lebih rumit untuk pembeli awam Indonesia yang jadi target Komunitech |
| Cakupan tugas | Artikel/blog/whitepaper/newsletter/materi presentasi, SEO, etika akademik | Riset umum lintas platform (Reddit/RSS/YouTube/kode), lebih luas tapi tidak spesifik tulisan panjang berstruktur SEO |

## Kesimpulan
Skill kita **tidak kalah secara keseluruhan** — untuk kebutuhan spesifik pembeli (UMKM/profesional
Indonesia, tanpa setup, konteks lokal, SEO, etika akademik) skill kita lebih siap pakai dan lebih
relevan. Namun pesaing **unggul secara teknis** di satu titik penting: pencegahan halusinasi sitasi
secara **struktural/mekanis** (ledger + verifikasi kutipan verbatim otomatis), bukan sekadar heuristik
pasca-tulis seperti `cek_sitasi.py` kita.

## Yang bisa dipelajari dari pesaing (ide, bukan salinan teks)
1. **Verifikasi kutipan langsung secara otomatis**: `cek_sitasi.py` kita saat ini tidak memeriksa apakah
   teks di antara tanda kutip `"..."` benar-benar muncul verbatim di sumber — itu masih 100% tanggung
   jawab manusia/agent. Ide: tambahkan mode opsional yang membandingkan teks kutipan dengan salinan
   halaman sumber yang ditempel pengguna (tanpa perlu akses jaringan dari script itu sendiri, tetap
   stdlib-only sesuai aturan CLAUDE.md).
2. **Pendaftaran sumber "sebelum menulis"**: pesaing memaksa urutan register-dulu-baru-tulis. Skill kita
   bisa memperkuat instruksi di §4 Langkah Kerja agar draf sementara `templates/daftar-pustaka.md` diisi
   dan dikonfirmasi **sebelum** draf ditulis (sudah ada di alur, tapi bisa ditegaskan lebih keras sebagai
   gerbang wajib, bukan sekadar urutan langkah).
3. **Ambang cakupan sitasi (`--min-coverage`)**: ide berguna untuk pengembangan lanjutan
   `cek_sitasi.py` — opsi tambahan yang menghitung rasio kalimat berangka/klaim yang punya `[n]` vs
   total, sebagai skor kasar (tetap sebagai peringatan, bukan gerbang keras, karena tidak semua kalimat
   perlu sitasi).
