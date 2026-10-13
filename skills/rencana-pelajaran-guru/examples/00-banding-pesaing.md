# Uji banding pesaing — `rencana-pelajaran-guru` vs pesaing publik

Skenario yang dibandingkan: **"buatkan modul ajar IPA kelas 7 tentang ekosistem 2 pertemuan"**
(skenario normal 1). Materi pesaing hanya **dibaca untuk dinilai**, tidak disalin.

## Pesaing 1 — Sumber ATM: `anthropics/k12-teacher-skills` — skill `k12-lesson-plan-creation`
(dibaca langsung dari repo GitHub, commit `281eb8d4...`, Apache-2.0)

**Cara kerja:** Route (deteksi mapel AS: math/ela/science/social_studies) → baca file
referensi mapel → cek konektor "Learning Commons Knowledge Graph" (proprietary pihak
ketiga) → clarify maks. 2 pertanyaan + tawaran draft cepat vs paket penuh → susun
`lesson.json` (skema JSON ~800+ baris logic rendering) → jalankan
`bash scripts/render_all.sh lesson.json OUTPUT_DIR` → hasil 3 file **.docx** (lesson plan,
student materials, observation template) + `.html`.

**Kelebihan nyata (diakui, dan sudah ditiru polanya di skill kita — lihat ATTRIBUTION.md):**
- Alur route→clarify→ground→build→output rapi dan "instan tapi terstruktur".
- "Copyright guardrail" tegas: tidak pernah reproduksi teks kurikulum sumber verbatim,
  dan footer jujur "Generated without the Learning Commons Knowledge Graph" bila standar
  resmi tidak tersedia — pola kejujuran ini yang kita adopsi jadi "(cek CP resmi)".
- Output akhir berupa file .docx siap edit (bukan hanya teks).

**Kelemahan untuk pasar Indonesia (fatal untuk pembeli target kita):**
- **100% konteks & kurikulum Amerika Serikat**: CCSS-M, CCSS-ELA, NGSS, C3 — sama sekali
  tidak menyebut Kurikulum Merdeka, CP, ATP, Fase A-F, atau Profil Lulusan/Pelajar
  Pancasila. Tidak relevan tanpa ditulis ulang total.
- **Butuh instalasi/dependensi**: mewajibkan Python + script rendering `.docx` (via
  `render_lesson_docx.py`, `lesson_common.py`) dan idealnya konektor Learning Commons
  Knowledge Graph berbayar/proprietary pihak ketiga untuk standar resmi — bertentangan
  langsung dengan prinsip pedoman kurasi Komunitech §1 "tanpa setup, tanpa API key/akun/instalasi paket".
  Skill kita sengaja tidak mereplikasi pipeline ini (lihat ATTRIBUTION.md poin 4).
- Tidak ada perhitungan JP/menit ala Indonesia sama sekali — pesaing pakai "45-60 minute
  period" generik ala sekolah AS, tanpa satuan JP dan tanpa validasi total menit
  vs jadwal.
- Tidak ada RPP 1 lembar, tidak ada istilah guru les/bimbel/madrasah.

**Skor kasar (aspek relevan pembeli guru Indonesia, 0-2 tiap 10 aspek, maks 20):**
Bahasa & istilah lokal 0, kesesuaian regulasi ID 0, konteks lokal 0, tanpa
setup/dependensi 0, verifikasi waktu format ID 0, RPP 1 lembar 0, kejujuran CP 2 (pola
ditiru), struktur kerja 2 (pola ditiru), kelengkapan dokumen (LKPD±) 1, guru
les/madrasah 0 → **5/20**. *(Skor rendah semata-mata karena target pasarnya memang bukan
Indonesia — bukan berarti skill ini buruk untuk pasarnya sendiri.)*

## Pesaing 2 — Prompt publik Indonesia terbaik yang ditemukan
Sumber: kumpulan "30 Prompt AI Terbaik untuk Guru 2026" — Dea Learning Center
(https://www.dealearningcenter.id/prompt-ai-untuk-guru-2026/), dibaca via web (bukan
skill/agent-skill format, prompt teks biasa untuk ditempel ke chatbot apa pun).
Pencarian tambahan: ClawHub, skills.sh, GitHub ("skill RPP kurikulum merdeka",
"modul ajar AI generator") — tidak ditemukan skill berformat Agent Skills (SKILL.md)
publik untuk RPP/Modul Ajar Indonesia yang memenuhi ambang bukti pemakaian pedoman kurasi Komunitech
Tahap 2 (bintang/instal/riwayat commit); yang ada adalah web tools closed-source
(modulajarcerdas.my.id, digitaleducation.id, dsb. — tidak bisa "dibaca" isinya/dinilai
sebagai skill) dan prompt teks lepas seperti di atas.

**Isi prompt (dibaca via web, diringkas untuk penilaian):** meminta input mapel/kelas-
fase/topik/alokasi waktu/model pembelajaran/**Profil Pelajar Pancasila** (istilah versi
lama, belum memakai "Profil Lulusan" 8 dimensi terbaru sesuai Permendikdasmen 13/2025);
meminta output TP format "ABCD" + Pemahaman Bermakna + 3 pertanyaan pemantik + alur
Pendahuluan-Inti-Penutup gaya "Memahami-Mengaplikasikan-Merefleksikan" + Asesmen Formatif
sederhana.

**Kelemahan dibanding skill kita:**
- Memakai istilah **"Profil Pelajar Pancasila"** — sudah diganti resmi jadi "Profil
  Lulusan" (8 dimensi) sejak Permendikdasmen No. 13/2025 (diverifikasi independen, lihat
  laporan balik). Prompt ini belum mengikuti regulasi terbaru.
- **Tidak ada mekanisme verifikasi CP** — tidak memperingatkan risiko mengarang kode/teks
  CP resmi.
- **Tidak ada validasi alokasi waktu JP** apa pun — "alokasi waktu" hanya kolom isian,
  tidak dihitung/dicocokkan dengan menit/JP per jenjang.
- **Tidak ada rubrik skor eksplisit** — asesmen formatif disebut sebagai konsep, bukan
  instrumen dengan cara menghitung nilai.
- Hanya satu dokumen (modul ajar) — tidak ada varian RPP 1 lembar, tidak ada paket
  LKPD+soal+kunci+rubrik terpisah, tidak ada penanganan guru les/bimbel/madrasah.
- Tidak ada pernyataan lisensi/sumber sama sekali (konten prompt marketing situs,
  bukan produk berlisensi jelas) — tidak relevan untuk dikurasi ATM (bukan MIT/Apache/
  CC-BY), hanya dipakai sebagai bahan banding, tidak disalin.

**Skor kasar (10 aspek sama seperti di atas):** Bahasa & istilah lokal 2, kesesuaian
regulasi ID **1** (istilah lama), konteks lokal 1 (kolom isian, tanpa contoh konkret
Indonesia bawaan), tanpa setup/dependensi 2 (prompt teks biasa), verifikasi waktu format
ID 0, RPP 1 lembar 0, kejujuran/guardrail CP 0, struktur kerja 1, kelengkapan dokumen
(LKPD/soal/rubrik) 0, guru les/madrasah 0 → **7/20**.

## Skill kita — `rencana-pelajaran-guru` (skor kasar aspek sama)
Bahasa & istilah lokal 2, kesesuaian regulasi ID 2 (Permendikdasmen 13/2025 & BSKAP
046/H/KR/2025 terverifikasi, istilah terbaru "Profil Lulusan" + padanan lama), konteks
lokal 2 (sawah/pasar/UMKM per mapel di `panduan-mapel.md`), tanpa setup/dependensi 2
(murni teks Markdown, script Python standar opsional), verifikasi waktu format ID 2
(script + langkah wajib), RPP 1 lembar 2, kejujuran/guardrail CP 2 ("cek CP resmi",
menolak mengarang), struktur kerja 2 (route jenjang→panduan mapel→CP→TP→ATP→kegiatan→
asesmen→diferensiasi→verifikasi→LKPD→soal→checklist), kelengkapan dokumen 2 (Modul Ajar+
LKPD+soal+kunci+rubrik, atau salah satu sesuai permintaan), guru les/madrasah 2 (dibahas
eksplisit) → **20/20** pada rubrik aspek pasar Indonesia ini.

## Kesimpulan uji banding
Skill kita **menang telak** melawan kedua pesaing untuk target pasar guru Indonesia:
lebih unggul dari sumber ATM Anthropic pada SEMUA aspek lokal (yang memang bukan tujuan
sumbernya), dan lebih unggul dari prompt publik Indonesia terbaik yang ditemukan pada
kepatuhan regulasi terkini, verifikasi waktu, kejujuran soal CP, dan kelengkapan dokumen.
Tidak ditemukan skill Agent Skills (SKILL.md) publik Indonesia yang lolos ambang bukti
kurasi pedoman kurasi Komunitech tahap 2 untuk topik ini — kata kunci yang dicari: "skill RPP kurikulum
merdeka", "modul ajar generator SKILL.md", "lesson plan Indonesia agent skill" di GitHub,
ClawHub, skills.sh (tidak ada hasil relevan berformat skill).
