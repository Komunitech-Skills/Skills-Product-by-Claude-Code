# Uji 02 — Klinik gigi kecil: persetujuan pasien baru via Google Form + WA (mode PERSETUJUAN, data spesifik)

> Penguji independen, 2026-09-25. `claude-code (simulasi agent)`. Mengikuti SKILL.md Mode 2 + `templates/pemberitahuan-persetujuan.md` varian C & D + `references/pilihan-per-jenis-usaha.md` §5.

## Input pengguna
> Halo, saya drg. pemilik Klinik Gigi Senyum Sehat (praktik kecil, ±15 pasien/hari). Pasien baru biasanya daftar lewat Google Form yang saya kirim via WA, isinya nama, tgl lahir, no WA, alamat, keluhan, riwayat alergi & penyakit, obat yang diminum. Tolong buatin kalimat persetujuan datanya yang benar sesuai UU PDP, buat di Google Form dan pesan WA-nya.

## Perilaku agent
- Mengenali **data kesehatan = data pribadi spesifik** (Ps. 4 ayat (2)) → template D, persetujuan eksplisit terpisah, akses terbatas.
- Menggabungkan varian C (Google Form: pertanyaan wajib pilihan ganda aktif, tanpa jawaban default) + D (klinik).
- Checklist C: "Data spesifik dikumpulkan lewat Google Form/WA tanpa perlindungan tambahan → TINGGI" → agent memberi peringatan dan langkah pengaman.
- Tidak membuat informed consent tindakan medis (di luar cakupan) — disebutkan.
- Skala ±15 pasien/hari → bukan "skala besar" yang jelas; tetap disebut kemungkinan DPO & saran konsultan hukum kesehatan.

## Output agent (lengkap)

⚠ Draf ini bukan nasihat hukum. Data kesehatan termasuk **data pribadi spesifik** — sebaiknya ditinjau konsultan hukum kesehatan.

### 1. Teks untuk Google Form (tempel di deskripsi + pertanyaan)
```markdown
# Formulir Pendaftaran Pasien Baru — Klinik Gigi Senyum Sehat

**Pemberitahuan privasi (baca sebelum mengisi).** Klinik Gigi Senyum Sehat memakai data di formulir ini (identitas, nomor WA, keluhan gigi, riwayat alergi & penyakit, obat yang sedang diminum) untuk pendaftaran, pemeriksaan, rekam medis, penagihan, dan kewajiban hukum. Data kesehatan termasuk data pribadi yang bersifat spesifik (UU 27/2022 Pasal 4 ayat (2)); akses dibatasi untuk dokter gigi dan staf pendaftaran. Formulir ini memakai Google Forms/Sheets (server Google dapat berada di luar Indonesia). Jawaban formulir dipindahkan ke rekam medis klinik lalu dihapus dari Google Sheets paling lambat [isi: 30] hari. Hubungi [isi: email] / WA [isi: nomor] untuk akses, perbaikan, atau penghapusan data. Kebijakan lengkap: [isi: tautan].

**Persetujuan pemrosesan data pasien** * (wajib, pilih satu)
○ Saya (atau orang tua/wali pasien) telah membaca pemberitahuan di atas dan **setuju** data identitas & kesehatan diproses untuk pelayanan kesehatan gigi di Klinik Gigi Senyum Sehat.
○ Saya tidak setuju mengisi data kesehatan di formulir online — saya akan mengisinya langsung di klinik.

Pertanyaan opsional terpisah:
☐ Saya setuju menerima pengingat jadwal kontrol lewat WhatsApp.
☐ Saya setuju foto gigi sebelum/sesudah perawatan dipakai untuk edukasi di media sosial klinik **tanpa wajah/identitas**.

Bila pasien berusia di bawah 18 tahun: Nama orang tua/wali * · Hubungan dengan pasien *
```

**Pengaturan Google Form yang disarankan:**
- Pertanyaan persetujuan = *Pilihan ganda*, **wajib**, tanpa jawaban terpilih otomatis. Kolom *Timestamp* di Sheets menjadi bukti persetujuan (UU PDP Ps. 24 — simpan, jangan dihapus sebelum dipindah ke rekam medis).
- Aktifkan *Settings → Responses → Restrict to users in…* tidak tersedia untuk akun gratis; minimal: **jangan** bagikan tautan edit/Sheets ke grup, matikan "View results summary", kunci akun Google dengan verifikasi dua langkah.
- Batasi siapa yang bisa membuka Sheets jawaban (hanya drg. & 1 staf).

### 2. Pesan WA saat mengirim tautan formulir
> Halo Kak [nama], terima kasih sudah membuat janji di Klinik Gigi Senyum Sehat 🙏
> Mohon isi formulir pasien baru di tautan ini: [isi: tautan Google Form]. Formulir berisi data kesehatan (keluhan, alergi, obat) yang hanya dipakai untuk pemeriksaan dan rekam medis, dan hanya dibuka oleh dokter gigi & staf pendaftaran. Kalau lebih nyaman, data kesehatan bisa diisi langsung di klinik.
> Ingin diingatkan jadwal kontrol lewat WA? Balas **SETUJU PENGINGAT**. Bisa berhenti kapan saja dengan membalas **STOP**.

*Catatan:* jangan minta pasien mengetik keluhan/riwayat penyakit langsung di chat WA; arahkan ke formulir atau klinik. Balasan "SETUJU PENGINGAT" adalah bukti persetujuan — jangan dihapus.

### 3. Peringatan penting
- **Risiko TINGGI (checklist C):** data kesehatan di Google Form/Sheets & WA = data spesifik di layanan asing. Kurangi: pindahkan ke rekam medis klinik lalu hapus dari Sheets secara berkala, akses dibatasi, 2FA aktif, jangan simpan di grup WA.
- **Rekam medis** wajib disimpan sesuai aturan kesehatan (Permenkes 24/2022 Ps. 39 menyebut ≥ 25 tahun untuk rekam medis elektronik — **cocokkan dengan aturan terbaru di bawah UU 17/2023**).
- Formulir ini **bukan** informed consent tindakan medis; tetap gunakan formulir persetujuan tindakan yang berlaku di klinik.
- Pasien anak (< 18 th): persetujuan orang tua/wali (Ps. 25).
- DPO: praktik kecil umumnya belum "skala besar", tetapi Ps. 53 (setelah Putusan MK 151/PUU-XXII/2024, cukup satu syarat) + PP 33/2026 perlu dicek bersama konsultan.
- Tawaran lanjutan: saya bisa menyusun Kebijakan Privasi klinik lengkap (mode SUSUN) yang ditautkan dari formulir.

_Disclaimer: Disusun otomatis dari informasi Anda, mengacu pada UU 27/2022 (dicek 25 September 2026). PP 33/2026 berlaku 16 Januari 2027; lembaga pengawas PDP belum terbentuk saat pengecekan. Bukan nasihat hukum. Usaha yang memproses data kesehatan, anak, atau keuangan dalam skala besar sebaiknya meminta peninjauan konsultan hukum._

## Uji tambahan penguji: script pada teks pemberitahuan singkat
Script dirancang untuk kebijakan lengkap; dijalankan di sini hanya untuk menguji deteksi.
```
PEMERIKSAAN KEBIJAKAN PRIVASI (UU 27/2022 PDP) — form.md
Skor kelengkapan: 44/100  |  Status: KURANG LENGKAP  |  202 kata

UNSUR:
  [ ] Identitas pengendali data (nama usaha/pemilik) — TIDAK ADA
  [v] Kontak yang bisa dihubungi (email/WA/alamat) — ADA
  [ ] Jenis data pribadi yang dikumpulkan — TIDAK ADA
  [v] Tujuan pemrosesan — ADA
  [v] Dasar pemrosesan (persetujuan, perjanjian, kewajiban hukum, dll.) — ADA
  [ ] Pihak yang menerima data (kurir, payment gateway, marketplace, cloud, iklan) — TIDAK ADA
  [v] Transfer/penyimpanan data di luar negeri — ADA
  [ ] Masa simpan (retensi) data — TIDAK ADA
  [~] Hak subjek data (akses, koreksi, hapus, tarik persetujuan) — SEBAGIAN (kurang: akses, tarik persetujuan)
  [ ] Cara mengajukan permintaan hak & batas waktu tanggapan — TIDAK ADA
  [v] Langkah keamanan data — ADA
  [ ] Pemberitahuan bila terjadi kebocoran (kegagalan pelindungan data) — TIDAK ADA
  [ ] Tanggal berlaku / terakhir diperbarui — TIDAK ADA
  [ ] Cara memberi tahu perubahan kebijakan — TIDAK ADA
  [v] Data spesifik (kesehatan, biometrik, keuangan, dll.): perlakuan khusus — ADA

YANG PERLU DITAMBAHKAN:
  1. Sebutkan nama usaha/badan usaha dan nama pemilik atau penanggung jawab sebagai pengendali data. [UU 27/2022 Pasal 21 & 31 (pengendali wajib jelas identitasnya)]
  2. Tulis daftar data yang dikumpulkan (mis. nama, nomor WA, alamat kirim, riwayat pesanan). [UU 27/2022 Pasal 21 ayat (1) huruf c & e]
  3. Sebutkan kepada siapa data diberikan dan untuk apa (kurir, payment gateway, marketplace, penyedia cloud, platform iklan). [UU 27/2022 Pasal 21 & Pasal 51 (prosesor)]
  4. Tulis berapa lama data disimpan per jenis (mis. data pesanan 10 tahun untuk pembukuan pajak, chat CS 1 tahun) lalu dihapus. [UU 27/2022 Pasal 21 ayat (1) huruf d & f, Pasal 43–44]
  5. Tuliskan hak-hak berikut dengan bahasa sederhana: mengakses & minta salinan, memperbaiki, menghapus, menarik persetujuan (juga: keberatan atas keputusan otomatis, membatasi pemrosesan, gugat ganti rugi). [UU 27/2022 Pasal 5–13 & Pasal 21 ayat (1) huruf g]
  6. Tulis cara mengajukan (email/WA mana, data apa yang perlu disertakan) dan janji tanggapan paling lambat 3×24 jam. [UU 27/2022 Pasal 30, 32, 40 (tanggapan paling lambat 3×24 jam)]
  7. Tulis bahwa bila terjadi kegagalan pelindungan data, Anda akan memberi tahu pelanggan secara tertulis paling lambat 3×24 jam. [UU 27/2022 Pasal 46]
  8. Tulis "Berlaku sejak: [tanggal]" dan "Terakhir diperbarui: [tanggal]" di bagian atas. [UU 27/2022 Pasal 21 ayat (2) (perubahan informasi)]
  9. Tulis bahwa perubahan akan diberitahukan SEBELUM berlaku (mis. lewat website/WA/email). [UU 27/2022 Pasal 21 ayat (2)]

FRASA BERISIKO: tidak ditemukan.

CATATAN:
  - Masih ada 4 isian kosong (mis. [isi: 30]). Lengkapi sebelum dipublikasikan.
  - Info: tidak ada kontak PPDP/DPO. Wajib hanya bila memenuhi Pasal 53 (layanan publik, pemantauan skala besar, atau data spesifik skala besar); UMKM biasa cukup narahubung.

⚠ Pemeriksa bantu berbasis kata kunci, bukan penilaian hukum. Kata kunci yang ditemukan belum tentu isinya memadai.
```

## Penilaian penguji
- ✅ Template C+D menghasilkan persetujuan aktif, per tujuan, dengan opsional terpisah; peringatan Google Form sesuai checklist C.
- ⚠ **Kontradiksi template D:** kotak "Saya setuju data saya diproses… *(wajib untuk pelayanan)*" membuat persetujuan menjadi syarat layanan, padahal SKILL.md Mode 2 menyatakan persetujuan harus "bisa ditolak tanpa kehilangan layanan inti". Untuk pelayanan & rekam medis, dasar yang lebih tepat adalah **pelaksanaan perjanjian (terapeutik) / kewajiban hukum**, sedangkan persetujuan eksplisit dipakai untuk bagian opsional (atau untuk data spesifik sesuai kebijakan konservatif). Agent penguji menambahkan opsi "isi di klinik" sebagai jalan keluar — template sebaiknya menjelaskan ini (temuan S-4).
- ⚠ Template D memakai "Tanda tangan" yang tidak ada di Google Form — agent harus mengadaptasi sendiri; perlu varian "D-online".
- ⚠ Script (bila dipakai pada teks ini): *identitas* & *jenis data* **tidak terdeteksi** walau ada ("Klinik Gigi Senyum Sehat memakai data … (identitas, nomor WA, keluhan…)"); pemicu data anak **tidak terpicu** oleh "di bawah 18 tahun" (hanya pola Inggris `under 1[3-8]`). Lihat HASIL-UJI S-3.
