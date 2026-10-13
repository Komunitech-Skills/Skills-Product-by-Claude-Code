# Atribusi

Skill `rencana-pelajaran-guru` dibuat lewat proses **ATM (Amati, Tiru, Modifikasi)** dari:

- **Sumber:** https://github.com/anthropics/k12-teacher-skills — khususnya skill
  `plugin/skills/k12-lesson-plan-creation` (dan, sebagai bahan banding pola/alur saja,
  `k12-lesson-differentiation` & `k12-check-for-understanding`).
- **Pembuat:** Anthropic, PBC & Learning Commons.
- **Lisensi sumber:** Apache License 2.0 (teks lengkap di `LICENSE-APACHE.txt`), dengan
  `NOTICE` asli disalin di `NOTICE-UPSTREAM.txt`. Diverifikasi langsung dari file `LICENSE`
  repo (`git show HEAD:LICENSE`) — bukan dari klaim README — dan dari header SPDX
  `Apache-2.0` di setiap `SKILL.md`/`LICENSE` per-skill di dalam repo tersebut.
- **Commit yang diambil:** `281eb8d41fe2837d911541c9bbb870b58add804c` (2026-08-28), di-clone
  `--depth 1` (read-only) ke folder kerja sementara pada 2026-09-24. Tidak ada script dari
  repo sumber yang dijalankan.

## Pembagian lisensi (penting)

Sesuai Tahap 2 `pedoman kurasi Komunitech`: bagian yang **diadaptasi/diturunkan langsung** dari struktur
skill sumber tunduk pada Apache-2.0 (atribusi + keterangan perubahan, lihat di bawah).
Konten baru yang **ditulis dari nol** oleh Komunitech (contoh lokal Indonesia, aturan
kurikulum Indonesia, script hitung, dsb.) adalah karya Komunitech dan dapat dijual sebagai
bagian produk berbayar, dengan tetap menyertakan atribusi Apache-2.0 di atas untuk bagian
yang berasal dari sumber. Tidak ada teks kurikulum resmi Indonesia (CP/ATP) yang disalin
dari sumber mana pun — sumber ini adalah untuk kurikulum AS (CCSS/NGSS), sama sekali tidak
relevan dan **tidak dipakai** sebagai isi.

## Yang diamati & ditiru (pola struktural, bukan teks)

1. **Alur kerja bertahap**: tentukan mapel/jenjang → baca panduan khusus mapel → cek
   ketersediaan standar resmi sebelum menulis → susun rencana → tawarkan draf cepat vs
   paket lengkap → hasilkan dokumen lengkap dalam satu giliran → tutup dengan tawaran
   revisi konkret. Pola lima langkah ini (route → clarify → ground → build → output) yang
   membuat skill sumber terasa "instan tapi rapi" kami tiru strukturnya.
2. **"Copyright guardrail"** — instruksi eksplisit di sumber agar tidak pernah
   mereproduksi teks kurikulum sumber (KG/CCSS/NGSS) secara verbatim, dan menandai footer
   "Generated without the Learning Commons Knowledge Graph" bila data standar tidak
   tersedia. Kami tiru **prinsipnya** untuk konteks Indonesia: jangan mengarang teks CP
   resmi, tandai `(cek CP resmi)` bila tidak yakin — lihat `SKILL.md` §Batasan dan
   `references/dasar-kurikulum.md` §2.
3. **Aturan kualitas dokumen** (`references/output.md` sumber): menit tiap fase kegiatan
   harus dijumlahkan persis sama dengan total durasi pelajaran; setiap alat/bahan yang
   disebut harus benar-benar dipakai; jawaban/hitungan harus diverifikasi, bukan ditulis
   kira-kira; rubrik/instrumen asesmen harus konkret. Prinsip-prinsip ini kami tiru dan
   tuangkan ke checklist `SKILL.md` serta script verifikasi baru
   (`scripts/hitung_alokasi_waktu.py`).
4. **Struktur tiga dokumen terpisah** untuk satu pelajaran (dokumen guru / dokumen siswa /
   lembar observasi-evaluasi) — kami tiru sebagai Modul Ajar (guru) + LKPD (siswa) + Soal &
   Rubrik (evaluasi), disesuaikan dengan istilah dan komponen Kurikulum Merdeka.
5. **Penutup setiap giliran** yang menanyakan kepuasan guru dan menawarkan 2–4 opsi revisi
   spesifik sesuai topik (bukan "ada revisi?" generik) — pola ini ditiru di Langkah 14
   `SKILL.md`.

## Yang diubah/ditambahkan besar oleh Komunitech (nilai tambah)

1. **100% Bahasa Indonesia** untuk seluruh instruksi, template, dan contoh — sumber
   sepenuhnya berbahasa Inggris untuk guru K-12 Amerika Serikat.
2. **Kurikulum Merdeka Indonesia menggantikan CCSS/NGSS/C3 Amerika Serikat sepenuhnya**:
   komponen Modul Ajar (Informasi Umum, Komponen Inti, Lampiran), CP 6 fase (A–F), ATP,
   Tujuan Pembelajaran, Profil Lulusan 8 dimensi (dan padanan Profil Pelajar Pancasila 6
   dimensi versi lama) — ditulis dari nol berdasarkan riset regulasi terkini (Permendikdasmen
   No. 13 Tahun 2025, Keputusan Kepala BSKAP No. 046/H/KR/2025), lihat
   `references/dasar-kurikulum.md` untuk sumber & tanggal verifikasi. Sumber sama sekali
   tidak menyebut Kurikulum Merdeka, CP, ATP, atau Profil Pelajar Pancasila/Profil Lulusan.
3. **Alokasi waktu JP dihitung eksplisit per jenjang Indonesia** (SD/MI 35 menit, SMP/MTs
   40 menit, SMA/MA/SMK 45 menit) lewat script baru `scripts/hitung_alokasi_waktu.py`
   (Python standar, tanpa dependensi) — konsep "menit fase harus pas" ditiru dari sumber,
   tapi angka JP dan implementasi script ditulis sendiri dari nol; sumber memakai periode
   45–60 menit generik ala sekolah AS tanpa satuan JP.
4. **Tanpa dependensi/instalasi apa pun.** Sumber merender dokumen `.docx`/`.html` lewat
   pipeline JSON (`lesson.json`) + script rendering ~800+ baris per skill
   (`scripts/lesson_common.py`, `render_lesson_docx.py`, dst., walau seluruhnya Python
   standar tanpa `python-docx`). Versi ini **sengaja tidak mereplikasi pipeline rendering
   tersebut** — sesuai prinsip "instan/tanpa setup" `pedoman kurasi Komunitech` §1, output berupa teks
   Markdown terstruktur yang tinggal disalin-tempel ke Word/Google Docs (`SKILL.md` §Format
   Output), sehingga skill tetap 100% berguna meski Python tidak tersedia sama sekali —
   sumber mewajibkan Python + script rendering untuk menghasilkan dokumen apa pun.
5. **Konteks lokal Indonesia ditulis dari nol** (`references/panduan-mapel.md`): pasar
   tradisional, sawah/kebun, UMKM, budaya daerah, ojek online, dan contoh miskonsepsi umum
   siswa Indonesia per mapel — sumber memakai konteks AS (context generik/curriculum AS).
6. **Guru les/bimbel & madrasah** ditangani eksplisit (rencana sesi ringkas, istilah mapel
   madrasah, nilai keislaman opsional pada Profil Lulusan) — tidak ada padanannya di sumber.
7. **RPP 1 lembar** (`templates/kerangka-rpp-1-lembar.md`) sebagai format ringkas terpisah
   dari Modul Ajar lengkap, sesuai kebutuhan administrasi guru Indonesia — konsep ini tidak
   ada di sumber (sistem AS tidak mengenal RPP 1 lembar).
8. **Rubrik dengan rumus nilai eksplisit** (skor total ÷ skor maksimum × 100, dengan
   kategori nilai) ditulis dari nol di `templates/kerangka-rubrik.md` — sumber
   mendeskripsikan rubrik sebagai bagian skema JSON render, tanpa rumus nilai akhir
   berbasis skor.
9. **Batasan eksplisit menolak soal ujian nasional/ANBK bocoran** dan kalkulator/skrining
   kebutuhan khusus — kebijakan baru Komunitech, tidak ada di sumber.
10. **Dihapus sepenuhnya:** seluruh pipeline `lesson.json`/render `.docx`/`.html`, integrasi
    Learning Commons Knowledge Graph (`find_standard_statement` dkk. — konektor proprietary
    pihak ketiga), istilah dan kode standar AS (CCSS-M, CCSS-ELA, NGSS PE, C3, TEKS, SOL,
    OAS), referensi kurikulum bermerek AS (Illustrative Mathematics, OpenSciEd), dan seluruh
    frontmatter/field `license` bergaya sumber (frontmatter kami hanya `name` dan
    `description` sesuai `pedoman kurasi Komunitech` §2).

Seluruh teks `SKILL.md`, `README.md`, `references/`, `templates/`, `examples/`, dan
`scripts/hitung_alokasi_waktu.py` ditulis ulang dari nol dalam Bahasa Indonesia; tidak ada
kalimat sumber yang disalin verbatim — hanya pola struktural dan prinsip kualitas (poin
"Yang diamati & ditiru" di atas) yang dipelajari lalu diimplementasikan sendiri untuk
konteks Kurikulum Merdeka Indonesia.

## Berkas terkait
- `LICENSE-APACHE.txt` — teks lengkap Apache License 2.0 (identik dengan `LICENSE` sumber).
- `NOTICE-UPSTREAM.txt` — salinan persis file `NOTICE` di root repo sumber.
- File `references/dasar-kurikulum.md` internal `k12-lesson-plan-creation/references/NOTICE`
  (tentang Common Core State Standards © NGA/CCSSO) **tidak disalin** karena kami tidak
  mengambil konten CCSS apa pun — tidak relevan untuk Kurikulum Merdeka Indonesia.

Penggunaan paket ini oleh pembeli tunduk pada `LISENSI.txt` yang disertakan dalam paket
pembelian, tanpa mengurangi ketentuan Apache License 2.0 di atas untuk bagian yang berasal
dari karya asli.
