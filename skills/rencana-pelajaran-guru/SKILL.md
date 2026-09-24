---
name: rencana-pelajaran-guru
description: Membuat Modul Ajar/RPP lengkap, RPP 1 lembar, LKPD, serta soal+kunci+rubrik penilaian sesuai Kurikulum Merdeka (CP, ATP, Tujuan Pembelajaran, Profil Lulusan/Profil Pelajar Pancasila, asesmen diagnostik-formatif-sumatif, diferensiasi) untuk guru SD/MI/SMP/MTs/SMA/MA/SMK dan guru les/bimbel di Indonesia, siap disalin ke Word/Google Docs. Gunakan saat pengguna minta dibuatkan rencana pelajaran, RPP, modul ajar, lesson plan, LKPD/lembar kerja siswa, atau soal ulangan+rubrik untuk satu topik dan jenjang. Trigger EN: lesson plan, teaching module, worksheet, rubric. Bukan untuk menyalin CP resmi kata demi kata atau membuat soal ujian nasional/ANBK bocoran.
---

# Rencana Pelajaran Guru (Modul Ajar Kurikulum Merdeka)

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
| Jenis dokumen yang diminta (Modul Ajar lengkap / RPP 1 lembar / LKPD saja / soal saja) | Tidak | Modul Ajar lengkap + LKPD + soal & rubrik (paket penuh) |

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

1. **Tentukan jenjang, fase, dan menit per JP** dari `references/dasar-kurikulum.md` §2–3.
   Jika guru menyebut jumlah pertemuan & JP, hitung total menit; bila tidak, pakai default
   1×2 JP.
2. **Baca `references/panduan-mapel.md`** untuk gaya mengajar, contoh konteks lokal, dan
   catatan diferensiasi sesuai mapel & kelompok jenjang (Fase A–B/C/D/E–F).
3. **Tentukan CP.** Jika guru menempelkan CP resmi, pakai persis itu. Jika tidak dan kamu
   tidak yakin kode/bunyi CP resminya, **jangan mengarang** — tulis ringkasan umum yang
   ditandai jelas `(cek CP resmi — cocokkan dengan dokumen resmi mapel & fase ini)`, lalu
   lanjutkan menyusun Tujuan Pembelajaran dari ringkasan itu.
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
   istilah itu. Ambil 1–2 dimensi yang paling relevan, jangan menempel semuanya asal.
8. **Rancang asesmen** diagnostik (awal), formatif (selama kegiatan), dan sumatif (akhir) —
   masing-masing dengan instrumen konkret, bukan sekadar nama jenisnya.
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
12. **Buat soal evaluasi + kunci + rubrik** (`templates/kerangka-rubrik.md`) dengan skor
    eksplisit dan cara menghitung nilai akhir yang jelas.
13. **Periksa dengan checklist** di bawah sebelum menyampaikan hasil ke guru.
14. **Tutup dengan ringkasan asumsi** (jika ada default yang dipakai) dan **tawarkan 2–3
    opsi revisi spesifik** sesuai mapel/topik (mis. "mau saya tambah versi soal yang lebih
    sulit untuk anak yang sudah paham?", "mau saya buatkan versi Bahasa Inggris untuk kelas
    bilingual?") — jangan hanya menulis "ada revisi?" tanpa opsi konkret.

## Format Output

Sampaikan sebagai teks Markdown terstruktur (heading, tabel, daftar bernomor) mengikuti
`templates/kerangka-modul-ajar.md`, `kerangka-lkpd.md`, dan `kerangka-rubrik.md`, dengan
urutan: **(1) Modul Ajar** (atau RPP 1 lembar bila diminta) → **(2) LKPD** → **(3) Soal +
Kunci + Rubrik**. Tambahkan catatan singkat di akhir:

```
Asumsi yang dipakai: [daftar bila ada default yang dipakai, mis. "1 pertemuan × 2 JP karena jumlah pertemuan tidak disebutkan"]
Cek sebelum dipakai: [mis. "CP di atas ringkasan umum — cocokkan dengan dokumen CP resmi fase & mapel ini"]
Cara pindah ke Word/Google Docs: salin semua teks di atas, tempel ke dokumen baru — Google
Docs otomatis membaca tanda # sebagai judul; di Word gunakan "Tempel Khusus > Teks Tanpa
Format" lalu terapkan gaya Heading pada judul-judul di atas.
```

Bila guru minta *hanya* salah satu dokumen (mis. "LKPD saja"), keluarkan dokumen itu saja
tanpa embel-embel dokumen lain.

## Contoh

**Input pengguna:** "buatkan modul ajar IPA kelas 7 tentang ekosistem 2 pertemuan"

**Output (ringkas — lihat contoh lengkap di `examples/01-modul-ajar-ipa-kelas7-ekosistem.md`):**
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
- [ ] Kunci jawaban LKPD/soal sudah dihitung ulang, bukan ditulis kira-kira
- [ ] Rubrik punya skor eksplisit dan cara menghitung nilai akhir
- [ ] Tidak ada soal yang meniru/berbau ujian nasional-ANBK bocoran
- [ ] Ditutup dengan asumsi (bila ada) + 2–3 opsi revisi spesifik

## Batasan & penanganan error
- **CP resmi:** skill ini tidak menyimpan basis data teks CP resmi lengkap (kode dan
  bunyinya bisa direvisi BSKAP sewaktu-waktu). Jangan pernah menuliskan kode/teks CP
  seolah pasti sesuai dokumen resmi kalau tidak yakin — selalu tandai untuk dicek. Jika
  guru menempelkan CP resmi, pakai itu sebagai sumber kebenaran.
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
