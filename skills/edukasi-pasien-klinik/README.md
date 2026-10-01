# Materi Pasien Rapi, Konsisten, Tanpa Repot Nulis Sendiri

**Leaflet, pengingat kontrol, FAQ, dan konten edukasi klinik jadi dalam hitungan menit — bukan diagnosis, tetap aman.**

## Manfaat
- ✅ Leaflet perawatan pasca-tindakan siap kirim WA, tinggal beri poin dari dokter.
- ✅ Pengingat kontrol/vaksin/imunisasi rapi dan sopan, sesuai jadwal yang klinik tentukan.
- ✅ FAQ klinik (jam buka, BPJS/umum, cara daftar) konsisten setiap kali dijawab.
- ✅ Konten edukasi medsos dengan sumber resmi (Kemenkes/WHO/IDAI/PDGI) yang dicantumkan jelas.
- ✅ Rekap kunjungan otomatis dari CSV — agregat saja, **tanpa nama/NIK/diagnosis** di output.

## Cocok untuk siapa
Dokter praktik mandiri, klinik pratama/gigi/kecantikan/fisioterapi, bidan, dan apotek yang ingin
komunikasi pasien lebih rapi tanpa menambah beban admin — dan tetap menjaga batas: **bukan alat
diagnosis atau skrining medis**.

## Contoh sebelum & sesudah
**Sebelum:** Dokter mendiktekan poin perawatan lisan ke admin, admin mengetik ulang manual tiap
pasien, format berbeda-beda, kadang lupa poin penting (obat, tanda bahaya).

**Sesudah (cukup ketik):** "Buatkan leaflet WA pasca cabut gigi. Dokter bilang: kompres es 15
menit tiap jam hari pertama, jangan kumur keras 24 jam, obat asam mefenamat 500mg 3x1 sesudah
makan 3 hari, kalau darah tidak berhenti 2 jam hubungi klinik."
→ Leaflet WA rapi, lengkap, format konsisten, siap tempel — dalam hitungan detik.

## Cara pakai
Setelah terpasang, cukup ketik permintaan biasa ke AI agent kamu, misalnya:
- "Buatkan pesan pengingat kontrol untuk pasien tanggal 2 Oktober jam 10, bawa buku KIA."
- "Buatkan FAQ klinik: jam buka Senin-Sabtu 08.00-20.00, terima BPJS & umum, daftar via WA."
- "Tulis konten edukasi IG tentang pentingnya imunisasi rutin, pakai sumber Kemenkes/IDAI."
- "Rekap kunjungan minggu ini dari file kunjungan.csv, per poli dan jam ramai."

## Batasan yang jujur perlu kamu tahu
- Skill ini **tidak mendiagnosis, tidak skrining, tidak menghitung dosis/BMI klinis, tidak
  menafsirkan hasil lab**. Setiap permintaan seperti itu akan ditolak dan diarahkan ke dokter.
- Semua instruksi medis (obat, pantangan, tanda bahaya) **harus kamu berikan sendiri** dari
  tenaga kesehatan — skill tidak mengarang instruksi medis.
- Sebagian dasar hukum (kerahasiaan medis, aturan iklan layanan kesehatan) ditandai **PERLU
  DICEK** karena belum diverifikasi dari naskah resmi — lihat
  `references/aturan-privasi-dan-iklan.md` sebelum dipakai untuk keperluan legal/kontrak.
- Rekap kunjungan butuh file CSV berkolom tanggal (dan idealnya poli/penjamin/status); isi kolom
  nama/NIK/diagnosis **tidak pernah ditampilkan** di rekap (bukan dihapus dari file aslimu).
  Nilai kategori yang jarang muncul (di bawah 3 baris) atau berpola nama/inisial/email/kode
  diagnosis tidak pernah dicetak, hanya digabung jadi angka. **Isi kolom "poli/layanan"
  sebaiknya nama layanan saja** (mis. "Gigi", "KIA") — bila klinik memasukkan nama
  diagnosis/penyakit ke kolom itu dan diagnosis itu berulang di banyak baris, rekap akan
  menampilkan **jumlah per diagnosis** (agregat, bukan identitas pasien), yang bisa jadi bukan
  yang kamu maksudkan.
- **Batasan jujur soal nama yang salah diketik berulang:** bila staf klinik salah mengetik nama
  pasien (bukan diagnosis/nomor) ke kolom status/poli/penjamin **≥3 kali** dalam satu file (dan
  file itu tidak punya kolom "Nama" terpisah yang bisa dipakai script untuk menyaring silang),
  nama panggilan itu bisa tetap tampil sebagai kategori + jumlah baris. Ini kejadian langka
  (kesalahan berulang sistematis, bukan salah ketik sekali) — **selalu periksa rincian per
  hari/poli/penjamin/status sebelum mengirim/mempublikasikan rekap**, ini bagian dari langkah
  kerja skill (checklist di SKILL.md), bukan opsional.

## Instalasi singkat
Salin folder `edukasi-pasien-klinik` ke folder skills AI agent kamu:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |

Panduan lengkap (termasuk Windows): lihat `CARA-INSTAL.md` di dalam paket.

## FAQ
**Apakah skill ini bisa membantu menjawab keluhan gejala pasien?**
Tidak untuk menilai/menebak penyakit atau menyarankan obat. Skill akan menenangkan pasien dan
mengarahkan ke jadwal konsultasi dokter — itu batas amannya.

**Apakah data pasien saya aman?**
Skill dirancang agar output rekap tidak pernah memuat nama/NIK/diagnosis (otomatis diabaikan
oleh script). Tetap jangan menempelkan rekam medis lengkap ke chat AI — cukup salin poin
instruksi umum dari dokter.

**Bisa dipakai untuk klinik gigi/kecantikan/fisioterapi, bukan cuma dokter umum?**
Bisa — template leaflet, pengingat, dan FAQ bersifat umum untuk semua jenis praktik kesehatan;
kamu tinggal isi poin sesuai bidangmu.

## Catatan revisi 1.0.8 (2026-10-01)
- Temuan uji ulang OpenClaw: pembuka "boleh langsung dikirim ke pasien" masih berupa izin kirim dari AI.
- Kini pembuka wajib: draf perlu dicek tenaga kesehatan/staf sebelum dikirim.

## Catatan revisi 1.0.7 (2026-10-01)
- Temuan uji ulang OpenClaw: catatan admin menyebut "tidak menjawab soal amoxicillin sisa" padahal draf justru melarangnya.
- Kini ada aturan "Catatan untuk admin" di SKILL.md: catatan wajib konsisten dengan isi draf, tanpa klaim "aman dikirim tanpa dokter".

## Catatan revisi 1.0.6 (2026-10-01)
- Temuan uji OpenClaw (klinik 05 & 02): kalimat penolakan baku belum melarang memakai antibiotik/obat sisa atau milik orang lain; leaflet menambah kata "dengan kuat" yang tidak ditulis dokter.
- Ditambah kalimat baku "jangan memberikan obat resep milik orang lain atau obat sisa, termasuk antibiotik sisa, sebelum diperiksa dokter" (tanpa dosis) — **PERLU REVIEW tenaga medis** sebelum rilis. Template leaflet kini melarang kata penguat/promosi yang tidak ditulis dokter dan meminta agent menyebut baris IGD/119 sebagai tambahan template. Script tidak berubah.
