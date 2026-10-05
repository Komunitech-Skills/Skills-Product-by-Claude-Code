# Hasil Uji Independen — `laporan-status-kantor`

**Tanggal:** 2026-09-23
**Penguji:** agent penguji independen (simulasi, Claude Code) — bukan pembuat skill
**Metode:** membaca hanya folder `skills/laporan-status-kantor/`, menjalankan 5 skenario
dengan berperan sebagai agent yang memuat skill ini, uji A/B tanpa-vs-dengan skill, uji
banding vs skill sumber ATM (`internal-comms`, Anthropic, Apache-2.0), dan uji muat
OpenClaw otomatis.

## Ringkasan skenario
| # | Skenario | File | Hasil |
|---|---|---|---|
| S1 | 3P mingguan toko bangunan → pemilik (WA) | `01-3p-toko-bangunan.md` | Baik, 1 celah instruksi (privasi nama karyawan tidak eksplisit) |
| S2 | Update tim startup + versi klien | `02-startup-tim-dan-klien.md` | Baik, pagar anti-bocor info ke klien terbukti bekerja |
| S3 | HR: cuti bersama + jam kerja Ramadan + FAQ + THR | `03-hr-pengumuman-dan-faq.md` | Baik, tidak mengarang tanggal/nominal, benar rujuk `hitung-thr` |
| S4 | Input tidak lengkap ("bikinin laporan mingguan dong") | `04-input-tidak-lengkap.md` | Sangat baik, tanya sekali sesuai spesifikasi |
| S5 | Di luar cakupan/etika: tuduhan karyawan & PHK sepihak | `05-di-luar-cakupan.md` | Baik, menolak & mengarahkan dengan tepat, tapi tidak dijamin instruksi eksplisit |

## Tabel skor (1–10)

| Kriteria | Skor | Catatan |
|---|---|---|
| Pemicu (description tepat) | 9 | Kata kunci ID & EN lengkap (laporan mingguan, weekly update, 3P, newsletter, FAQ karyawan, incident report, standup, dll.), jelas kapan dipakai. |
| Kemudahan awam | 8 | Tanpa setup, langsung dari chat/teks; pertanyaan klarifikasi ringkas & bernomor; ada jalan pintas untuk pengguna terburu-buru. |
| Kualitas output | 9 | Format WA benar (`*tebal*`), siap tempel, terstruktur konsisten per jenis; bahasa Indonesia natural, bukan terjemahan kaku. |
| Akurasi (angka/fakta) | 9 | Tidak ada script berhitung (memang bukan skill kalkulasi) sehingga tidak ada risiko salah hitung; seluruh fakta diambil persis dari bahan mentah, info hilang ditandai `[isi: ...]`, tidak menebak tanggal SKB/nominal THR. |
| Penanganan input kurang | 10 | Tanya sekali, satu pesan, bernomor, maks. 5 — persis sesuai brief; ada opsi default untuk pengguna cepat. |
| Penanganan di luar cakupan | 7 | Berhasil menolak tuduhan tanpa bukti & PHK sepihak dengan tepat, TAPI ini bergantung pada penilaian agen karena SKILL.md tidak membahas skenario ini secara eksplisit (lihat cacat SEDANG di bawah). |
| Keamanan | 10 | Tidak ada script sama sekali (murni instruksi teks), tidak ada panggilan jaringan, tidak ada pembacaan kredensial, tidak ada pola prompt injection di SKILL.md/README/templates/references (diperiksa manual, dicek juga hasil audit ATTRIBUTION.md). Muat di OpenClaw: eligible=true, modelVisible=true, commandVisible=true, disabled/blocked/agentFiltered/notInjected=false (lihat `check-full.json` di scratchpad penguji). |

**SKOR AKHIR: 8/10 — LULUS (≥7)**

Alasan skor akhir (bukan rata-rata otomatis): skill ini kuat di hampir semua dimensi
kritis untuk pembeli awam (anti-karang data, format WA benar, pagar privasi karyawan,
pagar kebocoran info ke klien, penanganan input kurang yang matang, tidak ada risiko
keamanan). Skor ditahan dari kisaran 9–10 karena dua celah instruksi SEDANG (bukan cacat
berat — perilaku aktual tetap benar dalam uji ini) yang membuat hasil **bergantung pada
kehati-hatian agen tertentu**, bukan instruksi eksplisit di SKILL.md — risiko nyata untuk
produk berbayar yang akan dipakai berbagai agent/model berbeda-beda tingkat kehati-hatian.

## Uji A/B (wajib) — `00-pembanding-tanpa-skill.md`
**Hasil dengan skill JELAS lebih baik**, termasuk perbedaan fungsional nyata (tanpa skill
memakai `**bold**` yang TIDAK akan tebal di WhatsApp — cacat fungsional bila dipakai
langsung), bukan cuma kosmetik. Tidak memicu batas skor ≤6.

## Uji banding sumber/pesaing (wajib) — `00-banding-pesaing.md`
Dibandingkan dengan skill sumber ATM `internal-comms` (Anthropic, Apache-2.0) untuk S1 &
S2: skill kita **menang jelas** di semua kriteria rubrik (kegunaan langsung, lokalisasi,
akurasi/anti-karang, kesiapan WA, cakupan jenis, perlindungan data sensitif). Tidak
ditemukan pesaing publik lain yang sebanding (`manairalabs/bicara-skills` dan
`alvinindra/bahasa-skills` tidak relevan; `zayan-work/skill-weekly-report` terlalu personal
dan berbasis git, dicatat sebagai temuan tapi tidak sebanding). Tidak memicu batas skor ≤6.

## Cek atribusi & lisensi
- `ATTRIBUTION.md` memuat teks Apache-2.0 **utuh dan identik** dengan `LICENSE.txt` sumber
  (diff hanya newline penutup — nihil perbedaan substansi). Diverifikasi dengan `diff`
  langsung terhadap hasil `git clone --depth 1 https://github.com/anthropics/skills`.
- Atribusi (nama, URL, commit, tanggal), pernyataan "file telah diubah" (Bagian 4(b)), dan
  daftar 10 perubahan konkret — **lengkap dan akurat**; dicek satu per satu terhadap isi
  sumber asli (jumlah baris sumber 187, 4 jenis komunikasi, tanpa script, tanpa NOTICE —
  semua klaim di ATTRIBUTION.md cocok dengan yang saya baca langsung dari clone).
- **Tidak ditemukan teks sumber disalin mentah** ke file produk (SKILL.md/README/
  templates/references) — dicek dengan grep frasa khas sumber ("30-60sec",
  "matter-of-fact", "megaphone", "1000+ people", dst.); yang cocok hanya kutipan dalam
  konteks perbandingan/atribusi (`ATTRIBUTION.md`, `examples/00-banding-pesaing.md`), yang
  memang wajar dan bukan pelanggaran.
- `research/sources/kurasi-internal-comms-2026-09-24.md` **lengkap**: mencantumkan nama,
  URL, pembuat, commit, tanggal, lisensi, hasil audit keamanan, penilaian sinyal bukti, dan
  keputusan — sesuai format Tahap 2 CLAUDE.md.
- Catatan: skor sinyal bukti kurasi (Tahap 2) sendiri diakui pembuat "≈2-3 dari 5" (di
  ambang bawah), diterima karena pembuat kredibel (Anthropic resmi) dan bukan AI slop —
  penilaian ini masuk akal dan sudah didokumentasikan jujur, bukan disembunyikan.

## Uji muat OpenClaw
`skills check --json` (OpenClaw dari `/tmp/oc`, `HOME` sementara, skill diinstal ke
`~/.openclaw/skills/`): skill `laporan-status-kantor` tercatat
`eligible=true, modelVisible=true, commandVisible=true`, dan **tidak** muncul di daftar
`disabled/blocked/agentFiltered/notInjected/missingRequirements`. **LULUS uji muat
OpenClaw.**

## Daftar cacat

### SEDANG
1. **Privasi nama karyawan di 3P ke atasan tidak diatur eksplisit** (S1,
   `01-3p-toko-bangunan.md`). SKILL.md checklist menyebut larangan "alasan cuti pribadi ...
   tanpa izin eksplisit", tapi tidak menegaskan apakah nama karyawan boleh disebut ke
   pemilik/atasan (penerima berwenang) dalam laporan 3P biasa (bukan laporan insiden).
   **Saran perbaikan konkret**: tambahkan 1 baris di SKILL.md bagian "Batasan &
   penanganan error" atau di checklist, mis.: *"Nama karyawan + alasan sakit/izin pribadi:
   default JANGAN sebut nama, tulis sebagai 'staf/tim [bagian]', kecuali pengguna secara
   eksplisit minta nama disebutkan."*
2. **Skenario tuduhan tanpa bukti / PHK sepihak tidak dibahas eksplisit** (S5,
   `05-di-luar-cakupan.md`). Skill berhasil menolak dengan tepat dalam uji ini, tapi
   berdasarkan penalaran umum agen, bukan instruksi tertulis — berisiko tidak konsisten di
   agen/model lain yang kurang hati-hati. **Saran perbaikan konkret**: tambahkan baris baru
   di bagian "Batasan & penanganan error" SKILL.md (persis setelah baris "Di luar cakupan
   ..."), mis.: *"Tuduhan ke karyawan tertentu tanpa bukti/proses resmi, atau PHK sepihak
   tanpa dasar hukum: JANGAN susun teksnya. Jelaskan risiko hukum/etika secara singkat,
   arahkan ke `surat-peringatan-karyawan` dan/atau konsultan hukum ketenagakerjaan."*

### RINGAN
3. Template `faq-karyawan.md` tidak punya contoh konkret menjawab pertanyaan THR secara
   ringkas sambil merujuk skill `hitung-thr` (S3) — jawaban yang dihasilkan agak panjang
   untuk format FAQ yang seharusnya "1-2 kalimat". **Saran**: tambahkan 1 contoh baris FAQ
   THR di template, mis.: *"THR cair kapan? Sesuai aturan, paling lambat H-7 sebelum Hari
   Raya; nominal per karyawan silakan cek ke HR/skill `hitung-thr`."*
4. Checklist SKILL.md tidak punya butir eksplisit untuk kasus dual-audience (versi tim vs
   versi klien dari bahan yang sama) — pagar kebocoran info sudah ada di
   `templates/3p-ke-klien.md`, tapi tidak direfleksikan di checklist utama SKILL.md.
   **Saran**: tambahkan butir *"Jika membuat versi ganda (tim + klien) dari bahan yang
   sama: versi klien sudah disaring dari info SDM/keuangan internal sesuai
   `3p-ke-klien.md`."*

## Apakah angka script sudah diverifikasi independen?
**Tidak ada script** di skill ini (tidak ada folder `scripts/`) — skill murni instruksi
teks/template, tidak melakukan perhitungan apa pun (perhitungan uang secara eksplisit
diarahkan ke skill lain seperti `hitung-thr`). Tidak berlaku untuk verifikasi angka
independen.

## Catatan koordinator — v1.0.1 (setelah uji, skor 8 LULUS)
Dua cacat SEDANG diperbaiki dengan menuliskan aturannya secara eksplisit di SKILL.md bagian "Batasan & penanganan error": (1) default privasi nama karyawan di laporan ke atasan/pemilik/klien; (2) penolakan memo tuduhan tanpa bukti / PHK sepihak + rujukan ke `surat-peringatan-karyawan` dan konsultan. Perilaku yang diuji tidak berubah (sebelumnya sudah benar berkat penalaran agent; kini tertulis).

## Riwayat revisi — v1.0.6 (2026-10-05)
Temuan Telegram gelombang 9 (cacat no. 1): balasan hanya berisi 5 pertanyaan, tanpa teks pengumuman. Perbaikan: aturan "kerjakan dulu, tanya di akhir", kerangka pengumuman libur akhir tahun dua blok, 1 Jan 2027 ditambahkan ke referensi, butir checklist baru. Status: **menunggu uji ulang independen**.


## Uji ulang Telegram v1.0.6 (2026-10-05)
Uji ulang Telegram v1.0.6 (2026-10-05): 3 percobaan 8,0 / 8,3 / 6,0, rata-rata 7,43, 2/3 lulus. VERDIK TIDAK LULUS. Teks pengumuman dua blok kini selalu tampil; sisa: kata "skill" bocor & tahun ucapan salah (2026 bukan 2027) di 1 percobaan.

## Riwayat revisi - v1.0.7 (2026-10-05)
Dari uji ulang Telegram v1.0.6 (TIDAK LULUS). Perbaikan: aturan tahun ucapan + kata terlarang di SKILL.md, 2 butir checklist. Status: **menunggu uji ulang independen**.

## Uji ulang konteks Telegram — 2026-10-05
Lihat bagian "Uji ulang konteks Telegram" terakhir di `00-openclaw-sebelum-sesudah.md`: verdik LULUS (laporan-status-kantor 1.0.7 rata-rata 8,5, 3/3; agen-cs-toko 1.0.11 rata-rata 8,0, 2/3).
