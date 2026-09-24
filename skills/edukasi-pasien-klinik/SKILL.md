---
name: edukasi-pasien-klinik
description: Merapikan materi edukasi pasien (leaflet pasca-tindakan, pengingat kontrol/vaksin, FAQ klinik, konten medsos kesehatan bersumber resmi), balasan chat non-diagnosis, dan rekap operasional klinik (kunjungan, jam ramai, agregat tanpa nama/diagnosis) untuk dokter praktik mandiri, klinik pratama/gigi/kecantikan/fisioterapi, bidan, apotek. Gunakan saat diminta buatkan leaflet perawatan setelah tindakan, pesan pengingat kontrol pasien, FAQ jam buka/biaya/BPJS, konten edukasi kesehatan untuk Instagram/WA klinik, balasan chat pasien soal jadwal/biaya, atau rekap kunjungan harian klinik. JANGAN gunakan untuk diagnosis, skrining, kalkulator medis (BMI/dosis), atau interpretasi hasil lab — patient education leaflet, appointment reminder, clinic FAQ, health content writing, non-diagnostic clinic chat replies, clinic visit report (aggregate, no diagnosis).
---

# Edukasi Pasien & Operasional Klinik

## Tujuan
Mengubah poin/instruksi yang **sudah ditentukan tenaga kesehatan** menjadi materi siap kirim
(leaflet, pengingat, FAQ, konten medsos) dalam bahasa awam yang sopan, menyusun balasan chat
umum non-diagnosis, dan merekap data operasional klinik (jumlah kunjungan) secara agregat —
tanpa pernah membuat diagnosis, skrining, kalkulator medis, atau rekomendasi obat.

## Kapan digunakan
- Membuat leaflet/pesan WA perawatan setelah tindakan (cabut gigi, operasi kecil, persalinan,
  dsb.) dari poin yang diberikan dokter.
- Membuat pesan pengingat kontrol, vaksin, atau imunisasi sesuai jadwal yang **diisi klinik**.
- Merapikan FAQ klinik: jam buka, cara daftar, BPJS/asuransi/umum, biaya yang **ditetapkan
  klinik**.
- Menulis konten edukasi kesehatan umum untuk media sosial klinik, dengan sumber resmi (Kemenkes,
  WHO, IDAI, PDGI, dll.) dan tanggal yang dicantumkan.
- Menyusun balasan chat untuk pertanyaan jadwal/biaya/daftar, atau menenangkan & mengarahkan
  keluhan gejala ke jadwal konsultasi dokter (tanpa menilai gejala).
- Merekap kunjungan/operasional klinik dari data yang diberikan (per hari/poli/penjamin, jam
  ramai, pasien tidak datang) — hasil selalu agregat, tanpa nama/NIK/diagnosis.

## Kapan TIDAK digunakan
- Diagnosis, menebak penyakit dari gejala, atau menilai kondisi pasien → arahkan ke dokter.
- Skrining medis apa pun (risiko penyakit, kuesioner skrining klinis).
- Kalkulator medis (BMI untuk keputusan klinis, dosis obat, skor risiko).
- Interpretasi hasil lab/rontgen/pemeriksaan penunjang.
- Rekomendasi dosis obat.
- Triase kegawatdaruratan (menilai gawat-tidaknya kondisi pasien).
- Menyimpan/memproses rekam medis lengkap atau data pasien individual di luar sistem klinik.

Lihat daftar lengkap contoh tolak & kalimat baku di `references/batasan-medis.md`.

## Input
| Info | Wajib? | Default jika tidak diberikan |
|---|---|---|
| Jenis materi (leaflet/pengingat/FAQ/konten medsos/balasan chat/rekap) | Ya | Tanyakan |
| Nama klinik & jenis praktik | Ya (untuk leaflet/FAQ/konten) | Tanyakan singkat |
| Poin instruksi dari dokter (untuk leaflet/pengingat obat) | Ya, untuk leaflet | Jika kosong: skill TIDAK mengarang instruksi medis — minta poin dari dokter |
| Jadwal (tanggal/jam kontrol, vaksin) | Ya, untuk pengingat | Tanyakan; skill tidak menghitung jadwal sendiri |
| Info FAQ (jam, biaya, BPJS) | Ya, untuk FAQ | Tanyakan; skill tidak mengarang biaya |
| Topik & sumber untuk konten medsos | Ya (topik); sumber boleh dicari skill dari daftar resmi | Jika pengguna tidak beri sumber, skill mengutip dari `references/sumber-resmi-kesehatan.md` dan mencantumkannya |
| File CSV kunjungan (untuk rekap) | Ya, untuk rekap | Tanyakan path file |

Jika info wajib kurang, tanyakan **sekali** dalam satu pesan berisi daftar pertanyaan bernomor
(maks. 5). Jangan berasumsi soal instruksi medis, jadwal, atau biaya — itu wajib dari klinik.

## Langkah kerja
1. **Kenali jenis permintaan** (leaflet, pengingat, FAQ, konten medsos, balasan chat, rekap).
2. **Cek batasan medis dulu** (`references/batasan-medis.md`). Kalau permintaan menyentuh
   diagnosis/skrining/kalkulator medis/dosis/interpretasi lab/triase → **tolak** dengan sopan,
   jelaskan alasan singkat, tawarkan alternatif aman (arahkan ke dokter, buatkan jadwal
   konsultasi, atau kalimat baku darurat).
3. **Kumpulkan input wajib** sesuai tabel di atas. Untuk leaflet/pengingat/FAQ: minta poin dari
   tenaga kesehatan/klinik bila belum diberikan — jangan menebak.
4. **Susun materi** memakai template yang sesuai (`templates/`) dan gaya bahasa
   `references/bahasa-awam-pasien.md`. Untuk konten medsos, cari/kutip sumber resmi dari
   `references/sumber-resmi-kesehatan.md` dan cantumkan sumber + tanggal.
5. **Untuk rekap operasional:** jalankan `scripts/rekap_kunjungan.py` pada file CSV yang
   diberikan (lihat Format Output). Jika Python tidak bisa dijalankan, ikuti panduan manual di
   `templates/rekap-operasional.md`.
6. **Periksa checklist** di bawah sebelum mengirim hasil.
7. Sertakan catatan singkat di akhir bila ada bagian yang butuh isian klinik (mis. "[isi dari
   dokter]" yang belum terisi) atau bagian hukum yang berstatus PERLU DICEK.

## Format output
Leaflet/pengingat/FAQ/rekap: teks siap tempel WA (heading, bullet, emoji secukupnya), mengikuti
struktur di `templates/`. Konten medsos: teks siap posting + baris "Sumber: ..." **dan** baris
nama & alamat klinik + tanggal publikasi (wajib, Permenkes 1787/2010 Pasal 4 ayat (2)) di akhir.
Rekap: total pendaftaran, hadir, tidak datang, persentase (dari script — lihat
`templates/rekap-operasional.md`). Balasan chat: 1 paragraf pendek atau beberapa kalimat, sopan,
tanpa jargon.

## Contoh
**Input pengguna:** "Buatkan leaflet WA untuk pasien habis cabut gigi geraham. Dokter bilang:
kompres es 15 menit tiap jam untuk hari pertama, jangan kumur keras 24 jam, jangan makan/minum
panas dulu, boleh makan lunak, kalau darah tidak berhenti setelah 2 jam atau bengkak makin besar
hubungi klinik. Obat: asam mefenamat 500mg 3x1 sesudah makan selama 3 hari (dari resep dr. Sari).
Kontrol lagi kalau ada keluhan. Nama klinik: Klinik Gigi Sehat Ceria."

**Output (ringkas):**
```
🏥 Klinik Gigi Sehat Ceria
Perawatan Setelah Cabut Gigi Geraham — [tanggal hari ini]

Terima kasih sudah datang hari ini. Berikut panduan perawatan di rumah:

✅ Boleh / dianjurkan
- Kompres es di pipi luar, 15 menit setiap jam, untuk hari pertama
- Makan makanan lunak dulu

🚫 Hindari dulu
- Jangan berkumur keras selama 24 jam
- Jangan makan/minum yang panas dulu

💊 Obat
- Asam mefenamat 500mg — 3x sehari setelah makan — selama 3 hari
  (sesuai resep dr. Sari)

⚠️ Segera hubungi klinik bila:
- Darah tidak berhenti setelah 2 jam, atau bengkak makin membesar

📅 Kontrol berikutnya
- Jika ada keluhan, silakan hubungi kami untuk jadwal kontrol

📞 Ada pertanyaan? Hubungi kami di [nomor klinik].

Catatan: pesan ini bukan pengganti konsultasi. Kalau kondisi memburuk atau terasa darurat,
segera ke IGD terdekat atau hubungi 119 — jangan menunggu balasan chat ini.
```
*(Asumsi: nomor kontak klinik belum diberikan, ditandai `[nomor klinik]` — mohon dilengkapi.)*

## Checklist sebelum mengirim hasil
- [ ] Tidak ada diagnosis/skrining/kalkulator medis/dosis rekaan/interpretasi lab.
- [ ] Semua instruksi medis (obat, pantangan, tanda bahaya) persis dari yang diberikan dokter —
      tidak ditambah/ditebak skill.
- [ ] Semua jadwal & biaya berasal dari isian klinik — tidak dikarang.
- [ ] Tidak ada nama/NIK/tanggal lahir/diagnosis pasien sungguhan di output (pakai contoh/anonim
      bila perlu ilustrasi).
- [ ] Konten medsos mencantumkan sumber resmi + tanggal, angka tidak dikarang.
- [ ] Konten medsos mencantumkan nama & alamat klinik + tanggal publikasi (Permenkes 1787/2010
      Pasal 4 ayat (2)).
- [ ] Tidak ada klaim menyembuhkan, testimoni pasien, foto before-after, promosi diskon
      tindakan medis, superlatif ("terbaik"/"satu-satunya"), atau perbandingan/celaan faskes
      lain di materi yang berbentuk iklan/publikasi (Permenkes 1787/2010 Pasal 5).
- [ ] Bahasa awam, sopan, tidak menakut-nakuti (lihat `references/bahasa-awam-pasien.md`).
- [ ] Untuk balasan chat: bila menyentuh gejala, pakai kalimat baku arahkan ke dokter (dan
      kalimat darurat bila relevan) — tidak menilai kegawatan.
- [ ] **Wajib untuk rekap:** baca rincian per hari/poli/penjamin/status sebelum mengirim — nama
      pasien yang salah diketik ≥3 kali di kolom kategori (mis. staf mengetik nama pasien di
      kolom "Status") **masih bisa tampil** sebagai nama panggilan + jumlah baris (lihat batasan
      di bawah). Script sudah menyaring & menyembunyikan nilai lain yang mencurigakan secara
      otomatis — **jangan** membuka file CSV asli untuk melengkapi nilai yang disembunyikan itu
      ke dalam rekap. Status yang "tidak dikenal" sudah dicek manual, bukan diasumsikan hadir.

## Batasan & penanganan error
- **Input medis kosong/tidak lengkap untuk leaflet/pengingat:** jangan mengarang instruksi.
  Tanyakan poin dari dokter/klinik.
- **Diminta menilai gejala atau membuat diagnosis:** tolak dengan kalimat baku di
  `references/batasan-medis.md`, tawarkan buatkan jadwal konsultasi.
- **Diminta kalkulator medis (BMI klinis, dosis, skor risiko):** tolak, jelaskan ini di luar
  cakupan, arahkan ke tenaga kesehatan/alat resmi yang berwenang.
- **File CSV rekap tidak ada kolom tanggal, atau file kosong/rusak:** script akan menampilkan
  pesan error jelas (exit code 1) dan tidak menghasilkan rekap — minta file yang benar.
- **File CSV berisi kolom sensitif (nama/NIK/diagnosis dan variasinya seperti Dx/ICD-10/Keluhan
  Utama/No. WA):** isi kolom tersebut **tidak pernah ditampilkan** di rekap, hanya nama
  kolomnya yang dilaporkan sebagai diabaikan, demi privasi (UU PDP 27/2022; UU 17/2023 Ps. 301;
  PP 28/2024 Ps. 788-789). Khusus kolom bertipe "Nama", kata-katanya dibaca secara internal
  HANYA untuk menyaring nilai status/poli/penjamin yang kebetulan sama dengan sepotong nama
  pasien (lihat poin berikut) — isi kolom Nama sendiri tetap tidak pernah masuk ke output.
- **Status kehadiran di rekap tidak dikenali script (bukan "hadir" maupun "tidak datang"):**
  dilaporkan terpisah sebagai "tidak dikenal" — **tidak** diam-diam dihitung hadir. Cek daftar
  rincian status di hasil rekap dan tanyakan ke klinik bila perlu diklasifikasikan ulang.
- **Format tanggal campur dalam satu file CSV** (sebagian gaya Indonesia hari/bulan, sebagian
  gaya Amerika bulan/hari): script memberi peringatan eksplisit + nomor baris yang perlu dicek,
  bukan diam-diam menebak. Bila file sama sekali tidak punya bukti (semua hari/bulan ≤ 12),
  script tetap mengasumsikan format Indonesia tapi memberi peringatan bahwa itu asumsi — jalankan
  ulang dengan `--urutan-tanggal mdy` untuk membandingkan bila filenya diduga dari sumber Amerika.
- **Nilai status/poli/penjamin yang berpotensi berisi nama/kontak/diagnosis** (banyak kata,
  mengandung angka/"@", pola inisial "S.A.", kode ICD "J06", pola sapaan+nama seperti "Bu Ani",
  atau sama dengan kata di kolom "Nama" file yang sama): script **tidak pernah** mencetak nilai
  itu apa adanya, hanya jumlah baris & jumlah nilai berbeda yang disembunyikan. Nilai yang
  muncul di **bawah 3 baris** juga disembunyikan meski polanya aman (k-anonimitas sederhana —
  nilai langka kemungkinan besar salah isi/data satu pasien). Jangan buka file CSV asli untuk
  "melengkapi" bagian yang disembunyikan ke dalam rekap.
- **Batasan yang jujur harus diketahui pengguna:** bila staf klinik salah mengetik **nama
  pasien** (bukan nomor/diagnosis) di kolom status/poli/penjamin **berulang ≥3 kali** (dan file
  itu **tidak** punya kolom bertipe "Nama" terpisah untuk disaring silang), nama panggilan itu
  bisa tetap tampil sebagai kategori + jumlah baris — bukan diam-diam disembunyikan. Ini kondisi
  langka (kesalahan sistematis, bukan salah ketik sekali), tapi harus dicek manual lewat
  checklist di atas sebelum rekap dikirim/dipublikasikan.
- **Kolom "poli/layanan" berisi nama diagnosis/penyakit, bukan nama layanan** (mis. klinik
  memakai kolom itu untuk mencatat "Hipertensi", "ISPA"): jika istilah itu muncul berulang
  (≥ 3 baris) dan bukan pola kode ICD, script tetap menampilkannya sebagai **jumlah agregat per
  istilah** (bukan identitas pasien — hanya kolom "poli" bukan tempat yang tepat untuk
  diagnosis). Sarankan klinik mengisi kolom poli dengan nama layanan saja (mis. "Gigi", "KIA").
- **Baris CSV yang jumlah kolomnya tidak cocok dengan header** (mis. koma tanpa tanda kutip di
  salah satu nilai menggeser semua kolom setelahnya): script mengeluarkan baris itu dari rincian
  per hari/poli/penjamin/status (tidak menebak kolom mana yang benar), tetap menghitungnya di
  total pendaftaran, dan memberi peringatan bernomor baris — minta klinik memperbaiki file
  aslinya.
- **Dasar hukum:** UU PDP 27/2022, kerahasiaan medis UU 17/2023 & PP 28/2024, dan isi pasal
  Permenkes 1787/2010 tentang iklan sudah diverifikasi dari naskah resmi (lihat
  `references/aturan-privasi-dan-iklan.md`). Yang **masih PERLU DICEK**: status berlaku
  Permenkes 1787/2010 saat ini (belum ditemukan pencabutannya, tapi belum dicek ulang di
  jdih.kemkes.go.id) — jangan menjadikan itu satu-satunya dasar keputusan hukum tanpa verifikasi
  ulang.
- **Kondisi darurat disebut pengguna/pasien:** selalu sertakan kalimat baku arahkan ke IGD/119 —
  skill tidak menilai tingkat kegawatan (bukan triase).
- **Di luar cakupan lain** (rekam medis terintegrasi, sistem antrian, audit kepatuhan penuh):
  arahkan ke sistem/konsultan khusus — skill ini tidak mencakupnya.
