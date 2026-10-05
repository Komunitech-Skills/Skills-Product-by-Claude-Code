---
name: rencana-pelajaran-guru
description: Membuat Modul Ajar/RPP, RPP 1 lembar, LKPD, serta soal+kunci+rubrik sesuai Kurikulum Merdeka (CP, Tujuan Pembelajaran, Profil Lulusan, asesmen, diferensiasi) untuk guru SD/MI/SMP/MTs/SMA/MA/SMK dan guru les/bimbel di Indonesia. Format default RINGKAS ala modul ajar 1 lembar (balasan chat sekitar 4.000-6.000 karakter, utuh: modul, LKPD tanpa jawaban, rubrik, kunci guru terpisah); versi lengkap hanya bila diminta. Bila guru menyebut cetak/supervisi/Word/file: isi utuh di chat, buat .docx sekali, coba lampirkan lewat alat kirim file kanal chat (berhasil: 'File Word terlampir.'; gagal/tidak ada: jangan sebut jalur file, tawarkan balas 'kirim file'). CP tidak dikarang dan tidak diambil lewat web (rujuk BSKAP 046/H/KR/2025, kolom tempel bunyi CP resmi). Gunakan saat guru minta RPP, modul ajar, lesson plan, LKPD, soal+rubrik. EN: lesson plan, worksheet, answer key, rubric.
---

# Rencana Pelajaran Guru (Modul Ajar Kurikulum Merdeka)

> **Aturan kerja:** Jangan menginstal paket/aplikasi (mis. `pip install`) — bila perlu, tunjukkan caranya dan biarkan pengguna yang memasang; jangan membuka atau mencari file selain yang diberikan pengguna, isi folder skill ini, dan file yang disebut di langkah kerja; jangan menulis file baru tanpa menyebut lokasinya, dan simpan hasil di folder kerja yang disepakati (bukan /tmp).

> **ATURAN PALING ATAS (kanal chat: Telegram/WhatsApp/web):**
> 1. **Format default RINGKAS** (ala "modul ajar 1 lembar"), target balasan chat **sekitar 4.000-6.000 karakter** dan tetap **utuh**, bukan ringkasan isi: Modul Ajar ringkas, LKPD (maks. 6 soal, tanpa jawaban), rubrik ringkas, lalu "Kunci Jawaban (untuk guru)" terpisah. Versi lengkap/panjang (modul penuh, soal banyak) **hanya bila guru memintanya**. Balasan terlalu panjang pernah membuat model macet tanpa balasan di Telegram; jangan menulis lebih dari yang diminta.
> 2. **Isi utuh WAJIB ditulis di chat**; dilarang menulis "isi lengkap ada di file/workspace/folder" sebagai pengganti isi. Bila terpaksa panjang (versi lengkap diminta), pecah "Bagian 1/n ...".
> 3. **File Word:** bila guru menyebut cetak, print, supervisi, Word, docx, atau file, **setelah isi chat selesai ditulis** jalankan `scripts/buat_docx.py` **sekali** (tanpa bertanya). File di komputer bot (mis. /tmp/...) tidak bisa diambil guru di Telegram, jadi **coba lampirkan** file itu lewat kemampuan kirim file kanal chat (mis. alat message/attachment OpenClaw) bila tersedia. Berhasil: tulis singkat `File Word terlampir.` Tidak tersedia atau gagal: **JANGAN menyebut jalur file** (tidak ada "File Word: /tmp/...") dan tulis kalimat baku: `Isi lengkap sudah ada di atas. Kalau perlu file Word, balas 'kirim file' — saya coba lampirkan.` Dilarang menulis "terlampir/terkirim/saya kirim" kecuali alat kirim file benar-benar dipanggil dan berhasil. Di kanal non-chat (CLI/IDE) jalur file dari output script boleh disebut. Script gagal: jangan menyebut file sama sekali.
> 4. **Batasi tool call:** baca SKILL.md sekali; **JANGAN pernah web_fetch/web_search dokumen CP** (lampiran BSKAP ±1.700 halaman; pernah membuat timeout). Bila diminta bunyi/kode CP persis: beri rujukan + langkah mencari + kolom tempel, lalu langsung lanjut menyusun modul. Di kanal chat jangan menulis file .md hasil modul di workspace (berkas .md sementara untuk script .docx ditaruh di folder sementara dan dihapus setelahnya).

## Tujuan
Mengubah satu kalimat permintaan guru (mis. "buatkan modul ajar IPA kelas 7 tentang
ekosistem 2 pertemuan") menjadi Modul Ajar lengkap + LKPD + soal & rubrik yang siap
dicetak/ditempel ke Word atau Google Docs — sesuai struktur Kurikulum Merdeka, tanpa guru
perlu tahu istilah CP/ATP/Profil Lulusan.

## Kapan digunakan
- Guru minta dibuatkan Modul Ajar, RPP, RPP 1 lembar, lesson plan, rencana pembelajaran,
  atau rencana sesi les/bimbel untuk satu topik + jenjang tertentu.
- Guru minta LKPD/lembar kerja siswa, soal ulangan/kuis beserta kunci jawaban dan rubrik,
  untuk topik yang sudah/akan diajarkan.
- Guru minta memperbarui/merevisi Modul Ajar yang sudah ada (tambah pertemuan, ubah
  diferensiasi, sesuaikan ke template sekolah).

## Kapan TIDAK digunakan
- **Menilai/mengoreksi jawaban siswa tertentu** atau memberi umpan balik individual —
  di luar cakupan; skill ini membuat rencana & instrumen, bukan mengoreksi hasil kerja.
- **Soal ujian nasional, ANBK, atau ujian sekolah "bocoran"** — tolak dan jelaskan bahwa
  ini melanggar integritas akademik; tawarkan dibuatkan soal latihan setara sebagai
  gantinya.
- **Menuliskan kode/teks CP resmi dari ingatan seolah pasti benar** — lihat Batasan.
- **Kalkulator/skrining kebutuhan khusus, kesehatan, atau psikologi siswa** — di luar
  cakupan; skill hanya memberi catatan akomodasi umum, arahkan ke guru pendamping
  khusus (GPK)/psikolog sekolah untuk asesmen sesungguhnya.
- **Kurikulum negara lain / standar internasional (CCSS, IB, Cambridge)** tanpa diminta
  eksplisit — defaultnya selalu Kurikulum Merdeka Indonesia.

## Input
| Info | Wajib? | Default jika tidak diberikan |
|---|---|---|
| Mata pelajaran & topik | Ya | — (tanyakan) |
| Jenjang & kelas (mis. SMP kelas 7) | Ya | — (tanyakan; menentukan fase & menit/JP) |
| Jumlah pertemuan & JP per pertemuan | Tidak | 1 pertemuan × 2 JP |
| Teks/kode CP resmi dari guru | Tidak | Ringkasan umum, ditandai "(cek CP resmi)" — lihat Batasan |
| Dokumen/format Modul Ajar sekolah sendiri | Tidak | Format `templates/kerangka-modul-ajar.md` |
| Kondisi kelas (siswa berkebutuhan khusus, kelas besar/kecil, dll.) | Tidak | Tidak ada catatan khusus |
| Jenis dokumen yang diminta (versi lengkap / RPP 1 lembar / LKPD saja / soal saja) | Tidak | Paket RINGKAS: modul ajar ringkas + LKPD (maks. 6 soal) + rubrik ringkas + kunci guru. Versi lengkap hanya bila diminta |

Jika **mapel/topik** atau **jenjang** tidak disebut, tanyakan **sekali** dalam satu pesan
bernomor, sekaligus tawarkan opsi cepat, misalnya:
1. Mapel & topiknya apa?
2. Untuk kelas/jenjang berapa?
3. Berapa pertemuan (boleh dijawab "1 saja" atau "langsung buatkan default 1 pertemuan 2 JP")?

Jika guru ingin cepat ("buatkan saja", "terserah", tidak menjawab detail), pakai default
di atas dan sebutkan asumsinya di akhir hasil (lihat Format Output). Default JP **selalu**
2 JP per pertemuan untuk semua mapel & jenjang (jangan menebak alokasi per mapel).
Jika guru hanya menjawab sebagian pertanyaan, **jangan bertanya lagi**: pakai jawabannya,
isi sisanya dengan default, dan sebutkan asumsinya — kecuali jenjang/kelas masih kosong
(itu wajib; tanyakan satu kali itu saja).

## Langkah kerja

> **Lokasi script:** semua script skill ini ada di subfolder `scripts/` di folder yang sama dengan SKILL.md ini (folder skill). Jalankan dari sana; jangan mencari script atau file pengguna ke seluruh disk (mis. `find /`) — itu lambat dan menyentuh data pribadi di luar folder kerja.

1. **Tentukan jenjang, fase, dan menit per JP** dari `references/dasar-kurikulum.md` §2–3.
   Jika guru menyebut jumlah pertemuan & JP, hitung total menit; bila tidak, pakai default
   1×2 JP.
2. **Baca `references/panduan-mapel.md`** untuk gaya mengajar, contoh konteks lokal, dan
   catatan diferensiasi sesuai mapel & kelompok jenjang (Fase A–B/C/D/E–F).
3. **Tentukan CP.** Jika guru menempelkan CP resmi, pakai persis itu. Jika tidak dan kamu
   tidak yakin kode/bunyi CP resminya, **jangan mengarang** — tulis ringkasan umum yang
   ditandai jelas `(cek CP resmi — cocokkan dengan dokumen resmi mapel & fase ini)`, lalu
   lanjutkan menyusun Tujuan Pembelajaran dari ringkasan itu. Bila guru **meminta kode & bunyi
   CP resmi persis**, ikuti "Permintaan kode/bunyi CP resmi" di bagian Batasan (jangan mengarang).
4. **Susun Tujuan Pembelajaran** dengan kata kerja operasional yang terukur (mis.
   "menjelaskan", "menghitung", "membandingkan" — bukan "memahami" tanpa kelanjutan yang
   bisa diamati).
5. **Susun Alur Tujuan Pembelajaran** bila lebih dari 1 pertemuan — urutan logis dari yang
   paling dasar.
6. **Rancang kegiatan pembukaan–inti–penutup per pertemuan** dengan konteks lokal Indonesia
   yang sesuai topik (pasar tradisional, sawah/kebun, UMKM sekitar, budaya daerah, dll. —
   lihat `references/panduan-mapel.md`). Menit tiap bagian **harus dijumlahkan** hingga
   sama dengan total menit pertemuan itu (lihat Langkah 10 untuk verifikasinya).
7. **Tentukan Profil Lulusan** (istilah terbaru, 8 dimensi) yang relevan — sebutkan juga
   padanan Profil Pelajar Pancasila (6 dimensi lama) bila guru/sekolah masih memakai
   istilah itu. Tulis nama dimensi **persis** seperti daftar di `references/dasar-kurikulum.md` (mis. "Penalaran Kritis", bukan "Bernalar Kritis"; "Bernalar Kritis" hanya sebagai padanan lama). Ambil 1–2 dimensi yang paling relevan, jangan menempel semuanya asal.
8. **Rancang asesmen** diagnostik (awal), formatif (selama kegiatan), dan sumatif (akhir) —
   masing-masing dengan instrumen konkret, bukan sekadar nama jenisnya. **Slot waktu sumatif harus konsisten:** bila sumatif dikerjakan di dalam pertemuan, sisakan menitnya di rincian kegiatan (ikut dijumlahkan); bila tidak muat, tulis jelas "sumatif dilaksanakan di pertemuan/jam terpisah (di luar alokasi ini)".
9. **Rancang diferensiasi** (pengayaan & remedial, konten/proses/produk) mengikuti
   `references/panduan-mapel.md` §Diferensiasi.
10. **Verifikasi alokasi waktu.** Bila Python 3 tersedia, jalankan:
    ```bash
    python3 scripts/hitung_alokasi_waktu.py --jenjang <sd|smp|sma|...> --jp <n> --pertemuan "<pembukaan,inti,penutup;...>"
    ```
    Bila statusnya bukan `COCOK`, sesuaikan menit kegiatan sampai cocok sebelum
    menuliskan hasil akhir. Bila Python tidak tersedia, jumlahkan manual — jangan
    lewati langkah ini.
11. **Buat LKPD** (`templates/kerangka-lkpd.md`) yang soal-soalnya berasal langsung dari
    Tujuan Pembelajaran pertemuan itu, dengan kunci jawaban yang **dihitung ulang**
    (khusus Matematika/IPA — jangan menulis angka yang belum dipastikan benar).
    **LKPD adalah lembar siswa: tidak boleh ada jawaban, kata "Jawaban:", contoh isian
    benar, atau kunci di dalamnya** (hanya garis/kotak kosong "Jawab: ____"). Semua kunci
    ditulis utuh di bagian "Kunci Jawaban (untuk guru)" (lihat Format Output).
12. **Buat rubrik + kunci** (`templates/kerangka-rubrik.md`) dengan skor eksplisit dan cara
    menghitung nilai akhir yang jelas. Default ringkas: LKPD sekaligus menjadi soal sumatif (maks. 6 soal); soal terpisah hanya bila diminta.
13. **Periksa dengan checklist** di bawah sebelum menyampaikan hasil ke guru.
14. **Tutup dengan ringkasan asumsi** (jika ada default yang dipakai) dan **tawarkan 2–3
    opsi revisi spesifik** sesuai mapel/topik (mis. "mau saya tambah versi soal yang lebih
    sulit untuk anak yang sudah paham?", "mau saya buatkan versi Bahasa Inggris untuk kelas
    bilingual?") — jangan hanya menulis "ada revisi?" tanpa opsi konkret.

## Format Output

**Satu format baku** (selalu sama): teks Markdown dengan judul `#`/`##`/`###`, daftar `-`
atau `1.`, dan tabel `| a | b |`. **Jangan** memakai garis pemisah hiasan (`───`, `***`, `---`
berulang) dan jangan menumpuk baris kosong. Urutan: **(1) Modul Ajar ringkas** (atau RPP 1
lembar) → **(2) LKPD (lembar siswa, tanpa jawaban)** → **(3) Rubrik ringkas** → **(4) Kunci
Jawaban (untuk guru)**. Template: `templates/kerangka-rpp-1-lembar.md` (default),
`kerangka-modul-ajar.md` (hanya bila versi lengkap diminta), `kerangka-lkpd.md`, `kerangka-rubrik.md`.

**Isi default RINGKAS (target 4.000-6.000 karakter total):**
- **Informasi umum** singkat: mapel, kelas/fase, topik, alokasi (n pertemuan x JP = menit), model/metode satu baris.
- **CP:** rujukan (BSKAP 046/H/KR/2025) + kolom tempel "CP (salin dari dokumen resmi): [tempel]"; ringkasan umum bertanda "(cek CP resmi)".
- **2-3 Tujuan Pembelajaran** terukur; 1-2 dimensi Profil Lulusan.
- **Langkah kegiatan bertabel** (kolom: Tahap, Menit, Kegiatan guru dan siswa), jumlah menit = alokasi (diverifikasi).
- **Asesmen singkat:** diagnostik 1 baris, formatif 1 baris, sumatif = LKPD/soal; diferensiasi 1 baris pengayaan + 1 baris remedial.
- **LKPD:** judul, petunjuk, maks. 6 soal/tugas, tanpa jawaban ("Jawab: ____").
- **Rubrik ringkas:** tabel skor + cara menghitung nilai akhir.
- **Kunci Jawaban (untuk guru):** jawaban singkat per nomor + skor.
Versi lengkap (kegiatan rinci per pertemuan, soal banyak, pengayaan/remedial panjang) hanya bila guru minta "lengkap/detail".

**Aturan kunci jawaban (wajib):**
- Lembar siswa (LKPD & soal) bersih dari jawaban; guru bisa langsung menggandakannya.
- Semua kunci berkumpul di satu bagian terpisah berjudul persis `# Kunci Jawaban (untuk guru)`,
  di **akhir** dokumen, ditulis per nomor (jawaban, skor). Dilarang menulis "lihat jawaban di atas/di LKPD".
- Soal uraian: kunci berisi poin jawaban yang diharapkan + pedoman skor, bukan sekadar "bervariasi".

Tutup dengan catatan (maks. 4 baris):

```
Asumsi yang dipakai: [daftar bila ada default yang dipakai, mis. "1 pertemuan × 2 JP karena jumlah pertemuan tidak disebutkan"]
Cek sebelum dipakai: [mis. "CP di atas ringkasan umum — cocokkan dengan dokumen CP resmi fase & mapel ini"]
Cara pindah ke Word/Google Docs: tempel teks ke dokumen baru; tanda # di awal baris adalah
penanda judul — jadikan baris itu Heading lalu hapus tandanya (Cari & Ganti), atau minta
file .docx (lihat di bawah) yang judul & tabelnya sudah rapi.
```

**File Word (.docx) untuk cetak/supervisi.** Bila guru menyebut dicetak, print, supervisi,
Word/docx/file, atau akan dikumpulkan ke kepala sekolah/pengawas, dan Python 3 serta izin
menulis file tersedia, **setelah isi chat selesai ditulis**, kerjakan tanpa bertanya:
1. Tulis hasil (format baku di atas) ke satu file `.md` **sementara** (folder sementara, bukan workspace guru).
2. Pisahkan lembar siswa dan kunci dengan baris `<<HALAMAN BARU>>` di atas judul Kunci Jawaban.
3. Jalankan **sekali** `python3 scripts/buat_docx.py hasil.md hasil.docx` (Windows: `python` atau `py`);
   script mencetak "OK: file ditulis di <jalur>". Hapus file .md sementara setelahnya.
4. Kanal chat (Telegram/WhatsApp/web): coba lampirkan file lewat alat kirim file kanal. Berhasil: tulis `File Word terlampir.` Tidak tersedia/gagal: jangan sebut jalur file; tulis `Isi lengkap sudah ada di atas. Kalau perlu file Word, balas 'kirim file' — saya coba lampirkan.` Kanal non-chat (CLI/IDE): tulis `File Word: <jalur persis dari output script>`. Dilarang menulis
   "terlampir", "terkirim", "saya kirim" kecuali alat kirim file benar-benar dipanggil dan berhasil. Bila script gagal atau jalurnya tidak ada, jangan menyebut file sama sekali.
5. Isi utuh tetap ditulis di chat; file hanya salinan.
Bila Python/izin menulis file tidak ada, jangan membuat file palsu: tampilkan teks di chat
dan jelaskan cara menempel ke Word. Jangan menyalin pesan proses internal ke guru.

Bila guru minta *hanya* salah satu dokumen (mis. "LKPD saja"), keluarkan dokumen itu saja;
untuk LKPD, tetap sertakan "Kunci Jawaban (untuk guru)" sebagai bagian terpisah di akhir
(guru boleh menghapusnya sebelum menggandakan).

## Contoh

**Input pengguna:** "buatkan modul ajar IPA kelas 7 tentang ekosistem 2 pertemuan"

**Output (ringkas — contoh versi lengkap di `examples/01-modul-ajar-ipa-kelas7-ekosistem.md`; contoh format default ringkas di `examples/09-format-ringkas-telegram.md`):**
```
MODUL AJAR — IPA
A. Informasi Umum: Fase D, SMP kelas VII, 2 pertemuan × 2 JP (80 menit/pertemuan)...
B. Komponen Inti: CP (cek CP resmi — ringkasan: interaksi makhluk hidup & lingkungan)...
   Tujuan Pembelajaran: 1) Menjelaskan komponen biotik & abiotik ekosistem sawah...
   Kegiatan: Pertemuan 1 (pembukaan 10’ + inti 60’ + penutup 10’ = 80’, status COCOK)...
   Asesmen: diagnostik (kuis lisan 3 pertanyaan), formatif (lembar pengamatan kelompok),
   sumatif (5 soal uraian, lihat lampiran)...
C. Lampiran: LKPD "Ekosistem Sawah di Sekitar Kita", Soal + Kunci + Rubrik...

Asumsi yang dipakai: 2 JP per pertemuan (default) karena JP tidak disebutkan guru — sesuaikan dengan jadwal sekolah.
```

## Checklist sebelum mengirim hasil
- [ ] Jenjang, fase, dan menit/JP benar (§2–3 `references/dasar-kurikulum.md`)
- [ ] CP ditandai "(cek CP resmi)" bila bukan dari teks resmi yang diberikan guru
- [ ] Total menit kegiatan tiap pertemuan = total JP × menit/JP (diverifikasi, lihat Langkah 10)
- [ ] Setiap alat/bahan di Sarana-Prasarana benar-benar dipakai di suatu kegiatan
- [ ] Ada minimal 1 konteks lokal Indonesia yang konkret (bukan generik)
- [ ] Asesmen diagnostik, formatif, sumatif masing-masing ada instrumennya
- [ ] Slot waktu sumatif konsisten (menitnya ada di rincian kegiatan, atau ditulis "di pertemuan terpisah")
- [ ] Nama dimensi Profil Lulusan persis sesuai `references/dasar-kurikulum.md` (Penalaran Kritis, dst.)
- [ ] Kunci jawaban LKPD/soal sudah dihitung ulang, bukan ditulis kira-kira
- [ ] **Lembar siswa/LKPD tidak memuat jawaban**; kunci utuh ada di "Kunci Jawaban (untuk guru)" di akhir (bukan "lihat di atas")
- [ ] **Format default RINGKAS** (balasan sekitar 4.000-6.000 karakter, LKPD maks. 6 soal, 2-3 TP, kegiatan bertabel menit); versi panjang hanya bila diminta
- [ ] Isi chat **utuh** (modul ringkas, LKPD, rubrik, kunci guru), bukan ringkasan isi, tanpa kalimat "isi ada di file"
- [ ] Bila guru menyebut cetak/supervisi/Word/file: `buat_docx.py` dijalankan sekali SETELAH isi chat selesai; di kanal chat file dicoba dilampirkan: berhasil = "File Word terlampir."; gagal/tidak ada alat = TANPA jalur file, kalimat baku "Isi lengkap sudah ada di atas. Kalau perlu file Word, balas 'kirim file' — saya coba lampirkan."; jalur file hanya di kanal CLI/IDE
- [ ] Tidak ada kata "terlampir/terkirim" tanpa alat kirim file yang berhasil; script gagal = file tidak disebut; tidak ada .md modul tertinggal di workspace
- [ ] Tool call minimal: SKILL.md dibaca sekali; **tidak ada web_fetch dokumen CP** (CP resmi tidak diambil lewat web)
- [ ] Format baku: tanpa garis pemisah hiasan/baris kosong berulang; catatan Word/Docs sesuai format (tanda #)
- [ ] Rubrik punya skor eksplisit dan cara menghitung nilai akhir
- [ ] Tidak ada soal yang meniru/berbau ujian nasional-ANBK bocoran
- [ ] Ditutup dengan asumsi (bila ada) + 2–3 opsi revisi spesifik

## Batasan & penanganan error
- **CP resmi:** skill ini tidak menyimpan basis data teks CP resmi lengkap (kode dan
  bunyinya bisa direvisi BSKAP sewaktu-waktu). Jangan pernah menuliskan kode/teks CP
  seolah pasti sesuai dokumen resmi kalau tidak yakin — selalu tandai untuk dicek. Jika
  guru menempelkan CP resmi, pakai itu sebagai sumber kebenaran.
- **Permintaan kode/bunyi CP resmi "persis":** JANGAN mengambil dokumen CP lewat web (tanpa web_fetch/web_search; dokumen ±1.700 halaman) dan jangan mengarang atau mengutip dari ingatan (CP lama mis. Kepmen 033/H/KR/2022 sudah dicabut). Jawab singkat: (1) bunyi resmi harus disalin dari Keputusan Kepala BSKAP No. 046/H/KR/2025 (ditetapkan 18 Juli 2025; lampiran per fase & mapel); (2) langkah 3-4 baris: buka https://guru.kemendikdasmen.go.id, cari "Capaian Pembelajaran 046/H/KR/2025" dan unduh PDF-nya; pilih jenjang lalu mata pelajaran; temukan Fase (A-F) kelas itu; salin paragraf CP dan nama elemen apa adanya beserta nomor halaman; (3) sediakan kolom di modul: `Tempel bunyi CP resmi di sini: [tempel]  Sumber: BSKAP 046/H/KR/2025, hlm. __`; (4) tetap tulis TP yang selaras dengan elemen yang benar (nama/penomoran elemen boleh dari `references/panduan-mapel.md` bila sudah ada dan bersumber; bila tidak yakin, tandai "(cek CP resmi)"); bila guru menempelkan CP, pakai persis itu.
- **Format sekolah berbeda-beda:** bila guru melampirkan/menyebut template sekolahnya,
  ikuti template itu — isi dengan hasil Langkah Kerja skill ini, jangan memaksakan format
  Komunitech.
- **Soal ujian resmi/bocoran:** tolak permintaan yang meminta menyalin/menebak soal ujian
  nasional, ANBK, atau ujian sekolah yang sedang berlangsung; tawarkan soal latihan setara
  sebagai gantinya.
- **Perhitungan waktu & nilai** selalu lewat penjumlahan eksplisit / `scripts/hitung_alokasi_waktu.py`
  — jangan menuliskan total menit atau nilai akhir yang belum dihitung ulang.
- **Regulasi bisa berubah:** ringkasan aturan mengacu Permendikdasmen No. 13 Tahun 2025 dan
  Keputusan Kepala BSKAP No. 046/H/KR/2025 per tanggal akses di `references/dasar-kurikulum.md`.
  Sarankan guru mengecek update terbaru bila ada kebijakan baru dari sekolah/dinas.
- **Bukan pengganti profesional:** untuk akreditasi, supervisi dinas, atau kebutuhan siswa
  berkebutuhan khusus, hasil skill ini adalah draf kerja — verifikasi tetap oleh guru,
  kepala sekolah, atau tenaga ahli terkait.
