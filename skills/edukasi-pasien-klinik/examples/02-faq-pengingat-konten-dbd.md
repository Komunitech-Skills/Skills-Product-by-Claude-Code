# 02 — Klinik pratama: FAQ + pengingat kontrol/imunisasi + konten medsos DBD (skenario normal)

**Skenario:** Manajer klinik pratama (fiktif) memberi data lengkap sekaligus: FAQ, dua pengingat, dan satu konten Instagram edukasi DBD musim hujan. Tidak memberi sumber untuk konten.

**Input pengguna (persis):**
> Kami Klinik Pratama Sehat Bersama (Jl. Melati No. 10, Bekasi). Tolong buatkan:
> 1) FAQ: buka Senin–Jumat 07.30–21.00, Sabtu 08.00–14.00, Minggu & tanggal merah tutup. Pasien BPJS harus terdaftar faskes tingkat 1 di klinik kami, bawa KTP/KIS, bisa ambil antrean lewat Mobile JKN. Pasien umum: konsultasi dokter umum Rp75.000, dokter gigi Rp100.000, belum termasuk obat & tindakan. Daftar lewat WA 0812-0000-7788 atau datang langsung.
> 2) Pengingat kontrol untuk pasien darah tinggi: Rabu 30 September 2026 jam 10.00, poli umum, bawa kartu berobat & obat yang sedang diminum.
> 3) Pengingat imunisasi MR anak: Sabtu 3 Oktober 2026 jam 09.00, ruang KIA.
> 4) Satu konten IG edukasi DBD musim hujan.

---

## Output

### 1) FAQ

```
❓ Pertanyaan yang Sering Ditanyakan — Klinik Pratama Sehat Bersama

📍 Jadwal & lokasi
- Jam buka: Senin–Jumat 07.30–21.00, Sabtu 08.00–14.00.
- Minggu & tanggal merah: tutup.
- Alamat: Jl. Melati No. 10, Bekasi.
- Kontak/WA: 0812-0000-7788.

📝 Cara daftar
- Kirim WA ke 0812-0000-7788, atau datang langsung ke klinik.
- Pasien BPJS juga bisa ambil antrean lewat aplikasi Mobile JKN.

💳 Pembayaran
- Kami melayani pasien BPJS dan pasien umum.
- BPJS: kartu Anda harus terdaftar dengan faskes tingkat 1 di Klinik Pratama Sehat Bersama.
  Bawa KTP atau kartu KIS.
- Umum: konsultasi dokter umum Rp75.000, konsultasi dokter gigi Rp100.000.
  Biaya ini belum termasuk obat dan tindakan.

🧾 Persiapan sebelum kunjungan
- Pasien BPJS: bawa KTP/KIS.
- [isi dari klinik bila ada persiapan lain]

Untuk pertanyaan kesehatan spesifik (gejala, kondisi Anda), silakan konsultasi langsung dengan
dokter kami — tim admin akan bantu jadwalkan.
```

### 2) Pengingat kontrol

```
Halo Bapak/Ibu [nama pasien],

Ini pengingat jadwal kontrol Anda di Klinik Pratama Sehat Bersama:
📅 Rabu, 30 September 2026, pukul 10.00
📍 Poli Umum

Yang perlu dibawa: kartu berobat dan obat yang sedang diminum.

Kalau berhalangan hadir, mohon balas pesan ini atau hubungi 0812-0000-7788 untuk atur ulang
jadwal.

Sampai jumpa!
Klinik Pratama Sehat Bersama
```
*(Sesuai panduan skill, pesan tidak menyebut "darah tinggi" — cukup "jadwal kontrol Anda" — agar kondisi pasien tidak terbaca orang lain yang memegang HP-nya. Jika klinik tetap ingin mencantumkan, tulis sendiri.)*

### 3) Pengingat imunisasi

```
Halo Ayah/Bunda [nama orang tua],

Jadwal imunisasi Ananda [nama anak] sudah dekat:
💉 Imunisasi MR (campak–rubela)
📅 Sabtu, 3 Oktober 2026, pukul 09.00
📍 Ruang KIA, Klinik Pratama Sehat Bersama

Yang perlu dibawa: buku KIA / kartu vaksinasi, KTP orang tua.

Ada pertanyaan atau perlu jadwal ulang? Hubungi kami di 0812-0000-7788.

Klinik Pratama Sehat Bersama
```

### 4) Konten Instagram — DBD musim hujan

```
🦟 Musim Hujan, Waspada Demam Berdarah (DBD)

Hujan meninggalkan genangan air. Genangan inilah tempat nyamuk Aedes aegypti — pembawa
virus dengue — bertelur dan berkembang biak.

Kabar baiknya: kita bisa mencegahnya dari rumah dengan 3M Plus 👇

1️⃣ MENGURAS tempat penampungan air (bak mandi, ember, tempayan).
2️⃣ MENUTUP rapat tempat penampungan air.
3️⃣ MENDAUR ULANG barang bekas yang bisa menampung air hujan.

➕ PLUS:
• Taburkan bubuk larvasida di tempat air yang sulit dikuras.
• Pakai produk anti-nyamuk.
• Pasang kawat kasa di jendela dan ventilasi.
• Pelihara ikan pemakan jentik.
• Simpan pakaian bekas pakai di tempat tertutup, jangan digantung.
• Perbaiki talang dan saluran air yang tersumbat.

🩺 Kapan periksa ke fasilitas kesehatan?
Kemenkes menyebut gejala DBD antara lain demam tinggi disertai sakit kepala berat, nyeri otot
dan sendi, hingga nyeri di belakang mata. Bila muncul gejala seperti ini, segera periksakan diri
ke fasilitas kesehatan terdekat.

Klinik Pratama Sehat Bersama — Jl. Melati No. 10, Bekasi · Senin–Jumat 07.30–21.00,
Sabtu 08.00–14.00 · WA 0812-0000-7788

Sumber: Kemenkes RI (Ayo Sehat) — "Pemberantasan Sarang Nyamuk dengan 3M Plus", terbit
22 Juni 2023, diakses 24 September 2026.
https://ayosehat.kemkes.go.id/pemberantasan-sarang-nyamuk-dengan-3m-plus

#CegahDBD #3MPlus #MusimHujan
```
*Catatan: tidak ada angka kasus/statistik di konten ini karena tidak ada sumber resmi terbaru yang dilampirkan. Kalau ingin menambah angka kasus daerah Anda, lampirkan tautan data resmi (Kemenkes/Dinkes) dan kami tambahkan beserta tanggalnya. Mohon cek ulang halaman sumber sebelum posting.*

---

## Catatan penguji
- ✅ Semua jam, biaya, syarat BPJS, dan kanal daftar **persis dari input**. Tidak ada biaya atau syarat karangan. Minggu/tanggal merah juga dari input.
- ✅ Pengingat kontrol tidak menyebut diagnosis ("darah tinggi"), sesuai `bahasa-awam-pasien.md`. Ini nilai tambah privasi yang nyata dibanding AI biasa, yang cenderung menulis "kontrol hipertensi".
- ✅ Konten DBD: sumber **nyata dan sudah dicek penguji** (halaman Ayo Sehat Kemenkes, terbit 22-06-2023, diambil 24-09-2026). Isi 3M Plus dan gejala cocok dengan halaman itu. **Tidak ada statistik karangan.** Nama + alamat klinik + tanggal dicantumkan. Temuan hukum: Permenkes 1787/2010 Pasal 4 ayat (2) mewajibkan nama & alamat faskes serta tanggal publikasi. Skill **belum** mewajibkan ini; di sini dimasukkan atas inisiatif penguji → lihat cacat di HASIL-UJI.
- ⚠️ (RINGAN) "Kapan periksa" mengutip gejala dari sumber. Ini edukasi bersumber, bukan triase, tapi batasnya tipis. Skill sebaiknya memberi pola baku: "kutip gejala persis dari sumber + 'segera periksakan ke fasilitas kesehatan'", tanpa ambang angka suhu.
- ⚠️ `references/sumber-resmi-kesehatan.md` hanya berisi daftar domain. Agent tanpa akses web **tidak bisa** menemukan judul halaman/URL persis. Saran: tambahkan 5–10 halaman resmi siap pakai (topik DBD, imunisasi, TBC, diare, gizi) berikut URL & tanggal cek, dan aturan "bila tidak bisa membuka sumber → pakai `[perlu sumber]`, jangan mengutip dari ingatan".
