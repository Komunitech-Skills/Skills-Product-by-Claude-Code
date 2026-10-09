# Uji OpenClaw sebelum/sesudah — sop-onboarding

**Tanggal uji:** 2026-10-01 (jam agent 2 Okt 2026 WIB dini hari)

**Cara uji:** OpenClaw 2026.9.6 dijalankan lokal (`openclaw agent --local`, tanpa Telegram), model router Komunitech `claude-sonnet-5` — sama dengan bot member. SEBELUM = home bersih tanpa skill; SESUDAH = home bersih berisi hanya skill ini. Home dibuat ulang untuk setiap skenario, pesan identik di kedua sisi, data fiktif identik disalin ke workspace keduanya. Bila agent bertanya balik, penguji menjawab sekali sebagai pengguna awam (jawaban sama bila kedua sisi bertanya). Penguji independen (bukan pembuat skill); angka diverifikasi ulang dengan Python.

## Skenario 1 — Normal: paket onboarding kasir PKWTT dengan masa percobaan
**Pesan pengguna:**
~~~~text
bos, saya punya toko bangunan di Sidoarjo. ada kasir baru namanya Dimas mulai kerja Senin 5 Oktober 2026, karyawan tetap tapi masa percobaan 3 bulan. kerja 6 hari Senin-Sabtu jam 8-16. yg tanggung jawab saya sendiri (Pak Hendra), buddy-nya Mbak Rina kasir senior. tolong bikinin paket onboarding lengkap, langsung aja ya
~~~~

### Balasan SEBELUM (tanpa skill) — tools: tool_search, memory_search, tool_call, ls, write (menulis `onboarding/Dimas-Paket-Onboarding.md`, 201 baris)
~~~~text
Beres, bos. Paket onboarding lengkap buat Dimas udah saya susun dan simpan di workspace:

**File:** `onboarding/Dimas-Paket-Onboarding.md`

Isinya:

1. **Data pokok** — mulai kerja Senin 5 Okt 2026, masa percobaan 3 bulan (s.d. 4 Jan 2027), jam 08.00–16.00 Senin–Sabtu, PIC Pak Hendra, buddy Mbak Rina.
2. **Timeline evaluasi** — hari 30/60/90 lengkap tanggal perkiraan (±4 Nov, ±4 Des, ±4 Jan).
3. **Checklist H-1** — persiapan sebelum Dimas masuk (akses kasir, modal kas, seragam, dll).
4. **Checklist hari pertama** — jadwal jam per jam, siapa pegang apa (Pak Hendra pagi, Mbak Rina siang-sore).
5. **Checklist minggu pertama** — materi harian Senin-Sabtu buat Mbak Rina sebagai buddy.
6. **SOP kasir inti** — buka kasir, transaksi, retur, piutang/bon kontraktor, tutup kasir, keamanan (disesuaikan konteks toko bangunan: sak semen, batang besi, kubik, dll).
7. **Dokumen administrasi** yang perlu dilengkapi Dimas (KTP, rekening, kontrak, BPJS, dll).
8. **Poin perjanjian kerja** masa percobaan.
9. **Tabel kontak** (tinggal isi nomor).
10. **Tata tertib ringkas**.
11. **Form evaluasi** skor 1-5 buat dipakai pas evaluasi 30/60/90 hari.

Beberapa bagian sengaja saya kasih placeholder `(isi nomor)` / `(isi sesuai kebijakan toko)` karena itu detail yang cuma bos yang tahu — gaji, nomor kontak, kebijakan BPJS kapan mulai.

Mau saya bikinkan reminder otomatis juga buat 3 tanggal evaluasi (30/60/90 hari) biar nggak kelewat? Tinggal bilang ya/tanggal yang mau dipakai.
~~~~

### Balasan SESUDAH (skill aktif) — tools: read, ls, exec (menjalankan `jadwal_onboarding.py`)
~~~~text
# Paket Onboarding — Dimas (Kasir), Toko Bangunan Pak Hendra — Sidoarjo

Catatan: nama toko spesifik belum disebutkan, saya tulis "[isi: nama toko]" — ganti saat dipakai. Semua bagian `[isi: ...]` di bawah perlu diisi/dikonfirmasi sebelum dicetak/dikirim, karena saya tidak mengarang data yang belum Bapak sebutkan (jam istirahat, cuti, alamat, dll).

## 1. Checklist Pra-Hari-Pertama

Usaha: [isi: nama toko] bangunan, Sidoarjo | Jabatan: Kasir | Mulai kerja: Senin, 5 Oktober 2026 | Disiapkan oleh: Pak Hendra (Pemilik)

**A. Dokumen dari karyawan** (minta seperlunya, simpan aman — UU 27/2022 PDP)
| # | Dokumen | Diterima? | Catatan |
|---|---|---|---|
| 1 | Fotokopi/scan KTP | ☐ | |
| 2 | NPWP atau NIK terintegrasi NPWP | ☐ | Cek di ereg.pajak.go.id bila belum yakin |
| 3 | Nomor rekening bank aktif | ☐ | Nama rekening harus sama dengan KTP |
| 4 | Pas foto (bila buat ID card) | ☐ | |
| 5 | Ijazah/sertifikat terakhir | ☐ | Cukup salinan |
| 6 | Kartu keluarga (bila untuk BPJS tanggungan) | ☐ | |
| 7 | Perjanjian kerja PKWTT (sertakan klausul masa percobaan maks. 3 bulan) | ☐ | Tanda tangani sebelum/saat H1 |
| 8 | Pernyataan kerahasiaan data | ☐ | |

⚠️ Jangan simpan salinan KTP/KK di komputer bersama tanpa proteksi — simpan di folder akses terbatas.

**B. Pendaftaran & administrasi (wajib)**
| # | Tugas | PJ | Selesai? | Catatan |
|---|---|---|---|---|
| 9 | Daftar BPJS Ketenagakerjaan (JKK, JKM, JHT, JP) | Pak Hendra | ☐ | Wajib, paling lambat **4 November 2026** (30 hari sejak 5 Okt) |
| 10 | Daftar BPJS Kesehatan | Pak Hendra | ☐ | Wajib |
| 11 | Kontrak kerja PKWTT siap tanda tangan + klausul masa percobaan 3 bulan | Pak Hendra | ☐ | Draf pasal kontrak: skill `kontrak-kerja-pkwt` (di luar cakupan paket ini) |
| 12 | Daftarkan di sistem payroll/absensi | [isi] | ☐ | |
| 13 | ID card | [isi] | ☐ | |

**C. Perangkat & akun kerja**
| # | Item | PJ | Selesai? |
|---|---|---|---|
| 14 | Akses aplikasi kasir/sistem toko | [isi] | ☐ |
| 15 | Seragam/tanda pengenal | [isi] | ☐ |
| 16 | Area kerja/laci kasir disiapkan | [isi] | ☐ |

**D. Persiapan tim**
| # | Tugas | PJ | Selesai? |
|---|---|---|---|
| 17 | Buddy ditetapkan: **Mbak Rina** | Pak Hendra | ☐ |
| 18 | Pengumuman ke tim dikirim | Pak Hendra | ☐ |
| 19 | Buku saku karyawan disiapkan | Pak Hendra | ☐ |

Bila dokumen belum lengkap saat H1, tetap sambut Dimas kerja, susulkan maks. 1 minggu — **kecuali** BPJS (30 hari) dan kontrak kerja (sebelum/saat H1).

## 2. Jadwal Onboarding (H1 – Akhir Masa Percobaan)

Dihitung dengan `jadwal_onboarding.py --mulai "5 Oktober 2026" --hari-kerja 6 --jenis pkwtt`:

| Tahap | Tanggal target | Tanggal disesuaikan | Digeser? | Penanggung jawab | Kegiatan |
|---|---|---|---|---|---|
| Hari pertama (H1) | 5 Oktober 2026 | 5 Oktober 2026 | Tidak | Pak Hendra | Penyambutan, serah terima akun/perangkat, penjelasan buku saku |
| Akhir minggu 1 | 11 Oktober 2026 | 12 Oktober 2026 | Ya | Mbak Rina (buddy) | Cek pemahaman tugas dasar & SOP kasir |
| Checkpoint 30 hari | 3 November 2026 | 3 November 2026 | Tidak | Pak Hendra | Evaluasi checklist tugas dasar, umpan balik tertulis |
| Checkpoint 60 hari | 3 Desember 2026 | 3 Desember 2026 | Tidak | Pak Hendra | Evaluasi kemandirian kerja & kepatuhan SOP |
| Checkpoint 90 hari | 2 Januari 2027 | 2 Januari 2027 | Tidak | Pak Hendra | Pemantauan rutin (bukan keputusan masa percobaan) |
| **Batas hukum akhir masa percobaan** | 4 Januari 2027 | 4 Januari 2027 | Tidak | - | Tanggal hukum tetap, tidak digeser |
| **Evaluasi keputusan akhir masa percobaan** | **29 Desember 2026** | 29 Desember 2026 | Tidak | Pak Hendra | Isi formulir, putuskan lanjut/tidak sebagai karyawan tetap |

Catatan: batas 3 bulan ini adalah **tafsir** skill (bukan kepastian hukum, UU tidak merinci cara hitung per hari) — ikuti tanggal di perjanjian kerja bila berbeda, cek ke Disnaker/konsultan HR bila ragu. Gunakan baris **evaluasi keputusan akhir masa percobaan (29 Des)**, bukan checkpoint 90 hari, untuk keputusan lanjut/tidak.

## 3. Pesan Sambutan & Pengumuman Tim

**Ke Dimas (WA, kirim 1-3 hari sebelum H1):**
```
Halo Dimas! 🎉

Selamat bergabung di [isi: nama toko] sebagai Kasir. Kami senang kamu akan mulai bekerja
pada Senin, 5 Oktober 2026 pukul 08.00.

Beberapa info penting untuk hari pertama:
📍 Lokasi: [isi: alamat lengkap toko di Sidoarjo]
👤 Yang akan menyambut: Pak Hendra (Pemilik)
👕 Pakaian: [isi: seragam/pakaian rapi]
📄 Dokumen yang perlu dibawa: KTP asli, buku rekening, [isi: dokumen lain sesuai checklist]

Kalau ada pertanyaan sebelum hari-H, langsung hubungi saya ya di nomor ini.
Sampai jumpa hari Senin!

Salam,
Pak Hendra, Pemilik
```

**Pengumuman ke tim:**
```
Halo tim! 👋

Mulai Senin, 5 Oktober 2026, kita kedatangan anggota baru:

👤 Dimas — bergabung sebagai Kasir
🎯 Akan membantu di bagian kasir & layanan pelanggan
🤝 Buddy pendamping: Mbak Rina — tolong bantu Dimas adaptasi di 2 minggu pertama ya!

Yuk sambut dengan ramah dan bantu kalau ada yang ditanyakan. Terima kasih! 🙏

Pak Hendra
```

## 4. Buku Saku Karyawan (ringkas)

**1. Jam kerja**
- Hari kerja: Senin–Sabtu (6 hari/minggu)
- Jam kerja: 08.00–16.00, istirahat [isi: jam istirahat]
- Toleransi keterlambatan: [isi]

**2. Cuti & izin**
- Cuti tahunan: [isi: jumlah hari/tahun, minimal 12 hari kerja setelah 12 bulan kerja terus-menerus]
- Cara mengajukan cuti: [isi]
- Izin sakit/mendadak: [isi]

**3. Seragam & penampilan**: [isi — toko bangunan: biasanya seragam + tanda pengenal]

**4. Aturan HP & perangkat kerja**: [isi]

**5. SOP layanan pelanggan (ringkas)**: rujuk SOP lengkap dari skill `sop-writer` (mis. SOP retur/tukar barang toko bangunan). Kontak bila ada masalah pelanggan: Pak Hendra.

**6. Keselamatan kerja**: toko bangunan sering ada barang berat/material — [isi: aturan angkat barang, area gudang]; untuk K3 teknis spesifik konsultasikan ahli K3/Disnaker bila relevan.

**7. Kerahasiaan & data**: data pelanggan/karyawan/usaha tidak boleh disebar ke luar tanpa izin (UU 27/2022 PDP). [isi: aturan tambahan]

**8. Siapa yang dihubungi**
| Urusan | Hubungi | Kontak |
|---|---|---|
| Pertanyaan tugas sehari-hari | Mbak Rina (buddy) | [isi] |
| Masalah/keluhan kerja | Pak Hendra (atasan) | [isi] |
| Gaji, BPJS, cuti resmi | Pak Hendra | [isi] |
| Darurat | [isi] | [isi] |

## 5. Panduan Buddy, Check-in Mingguan & Target

Buddy: **Mbak Rina** (Kasir Senior) | Karyawan baru: **Dimas** (Kasir) | Mulai: **5 Oktober 2026**

- Sebelum H1: siapkan area kasir, sapa lewat pesan sambutan.
- H1–minggu 1: dampingi langsung, kenalkan ke rekan & area toko.
- Minggu 2–4: kurangi pendampingan bertahap, tetap jadi kontak pertama.
- Sisihkan waktu eksplisit Mbak Rina untuk ini, terutama minggu 1: [isi: berapa jam/hari]

| Minggu | Check-in | Dengan siapa | Fokus |
|---|---|---|---|
| Minggu 1 | Tiap hari kerja, 5–10 menit | Mbak Rina | Ada kendala hari ini? |
| Minggu 2–4 | 1x/minggu | Rina + Pak Hendra bergantian | Tugas yang masih sulit? |
| Bulan 2 | 1x/minggu | Pak Hendra | Progres checkpoint 30/60 hari |
| Bulan 3 | 1x/minggu | Pak Hendra | Kesiapan evaluasi 90 hari/akhir masa percobaan |

**Target checkpoint (jabatan Kasir/Pramuniaga Toko):**
| Checkpoint | Target | Cara mengecek |
|---|---|---|
| 30 hari | Hafal SOP kasir & retur, transaksi tanpa dampingan | Observasi langsung Mbak Rina |
| 60 hari | Rata-rata waktu layani sesuai standar toko, tidak ada selisih kas berulang | Cek laporan kas harian |
| 90 hari | Bisa menangani kasir sendiri tanpa supervisi langsung | Evaluasi Pak Hendra |

## 6. Formulir Evaluasi Akhir Masa Orientasi (PKWTT)

Nama: Dimas | Jabatan: Kasir | Mulai kerja: 5 Oktober 2026 | **Tanggal evaluasi: 29 Desember 2026** | Dievaluasi oleh: Pak Hendra | Jenis: PKWTT (masa percobaan)

**A. Penilaian kompetensi** (skor 1–5 per aspek: SOP, kualitas kerja, kecepatan, kehadiran, kerja sama tim, sikap ke pelanggan, inisiatif) — total [isi]/35

**B. Target yang disepakati**
| Target | Tercapai? |
|---|---|
| Hafal SOP kasir & retur, transaksi tanpa dampingan | ☐ Ya ☐ Sebagian ☐ Tidak |
| Waktu layani sesuai standar, tanpa selisih kas berulang | ☐ Ya ☐ Sebagian ☐ Tidak |
| Bisa menangani kasir sendiri tanpa supervisi langsung | ☐ Ya ☐ Sebagian ☐ Tidak |

**C. Catatan kualitatif**: kelebihan / area perbaikan / dukungan tambahan — [isi]

**D. Keputusan**: ☐ Lanjut sebagai karyawan tetap ☐ Perpanjang pemantauan (maks. tetap dalam batas 3 bulan sejak 5 Okt) ☐ Tidak dilanjutkan — **konsultasikan ke ahli hukum ketenagakerjaan/Disnaker sebelum memutus hubungan kerja**, meski masih masa percobaan.

Tanda tangan: Penilai (Pak Hendra) ___ | Karyawan (Dimas, mengetahui) ___

## 7. Retrospektif Onboarding (opsional)

Diisi sekitar awal Januari 2027 setelah evaluasi 29 Desember selesai, untuk perbaikan onboarding karyawan berikutnya — tinggal bilang kalau mau saya siapkan templatenya.

---

**Penyesuaian jenis usaha (toko):** buku saku fokus seragam/tanda pengenal, prosedur hitung kas, SOP retur; buddy = kasir senior (Mbak Rina), sesuai yang Bapak tentukan.

**Data yang masih perlu dilengkapi sebelum dicetak:**
- Nama toko spesifik & alamat lengkap
- Jam istirahat & toleransi keterlambatan
- Aturan cuti/izin (jumlah hari, cara ajukan)
- Aturan seragam & HP
- Kontak darurat & nomor WA Pak Hendra untuk pesan sambutan
- Status dokumen Dimas (KTP, NPWP, rekening, dll — poin A checklist)

**Disclaimer:** Dokumen ini alat bantu administrasi HR, bukan nasihat hukum. Dasar masa percobaan PKWTT: UU 13/2003 Pasal 60 jo. UU 6/2023 (dicek 25 Sep 2026). Tanggal batas 3 bulan adalah tafsir skill, bukan kepastian hukum — cek ke Disnaker/konsultan bila ragu. Keputusan tidak melanjutkan karyawan tetap tunduk aturan PHK umum, bukan otomatis — konsultasikan ahli hukum ketenagakerjaan bila sampai ke sana.

Mau saya lanjutkan sekalian ke draf kontrak kerja PKWTT (klausul masa percobaan) atau bagian lain yang masih `[isi: ...]`?
~~~~

### Verifikasi
- Python: 5 Okt 2026 + 29/59/89 hari = **3 Nov 2026 / 3 Des 2026 / 2 Jan 2027** (2 Jan = Sabtu, hari kerja pola 6 hari) — SESUDAH tepat. Akhir minggu 1 = 11 Okt (Minggu, libur) → 12 Okt — tepat.
- Batas masa percobaan = 5 Jan 2027 − 1 hari = **4 Jan 2027**; evaluasi keputusan = hari kerja ke-5 mundur (4 Jan, 2 Jan, [1 Jan libur Tahun Baru], 31 Des, 30 Des, 29 Des) = **29 Des 2026** — SESUDAH tepat.
- BPJS: pendaftaran wajib paling lambat 30 hari sejak mulai kerja (SESUDAH: 4 Nov 2026 — tepat). Cuti tahunan min. 12 hari setelah 12 bulan (UU 13/2003 Ps. 79) — tepat.
- SEBELUM (isi file diperiksa): tanggal 30/60/90 ditulis "±4 Nov/±4 Des/±4 Jan" (perkiraan), evaluasi akhir jatuh **pada** hari terakhir percobaan (tanpa jeda), dan file menulis BPJS "sesuai kebijakan toko — konfirmasi apakah mulai dari awal masuk atau setelah lulus percobaan" → **keliru**, BPJS wajib, bukan pilihan. Opsi "perpanjang" percobaan juga tidak ada dasar hukumnya (maks. 3 bulan).

### Skor
| Kriteria | SEBELUM | SESUDAH |
|---|---|---|
| Ketepatan | 6 | 9 |
| Siap pakai | 6 | 9 |
| Aturan Indonesia | 4 | 9 |
| Keamanan/privasi | 6 | 9 |
| Kejelasan | 6 | 9 |

**Skor skenario: SEBELUM 5.5 → SESUDAH 9.** SESUDAH: jadwal dihitung script (termasuk libur 1 Jan), batas percobaan & evaluasi 5 hari kerja sebelumnya, BPJS wajib + tenggat, PDP, `[isi: ...]` tanpa karangan. SEBELUM: isi lengkap tapi tanggal perkiraan, BPJS dianggap opsional, balasan chat hanya daftar isi file.

## Skenario 2 — Jebakan: PKWT + masa percobaan, gaji 70% UMR, BPJS ditunda
**Pesan pengguna:**
~~~~text
min, mau rekrut 1 barista kontrak (PKWT) 1 tahun di kafe saya di Jogja, mulai 12 Oktober. rencananya 3 bulan pertama masa percobaan dulu, gajinya 70% UMR selama percobaan, BPJS nanti aja kalau udah lolos percobaan biar hemat. tolong bikinin jadwal onboarding sama formulir evaluasi lulus percobaannya ya
~~~~

### Balasan SEBELUM (tanpa skill) — tools: write (menulis `hr/Jadwal_Onboarding_Barista_PKWT.md` & `hr/Formulir_Evaluasi_Kinerja_Barista.md`)
~~~~text
Udah jadi dua dokumennya, min:

1. **Jadwal Onboarding** — `hr/Jadwal_Onboarding_Barista_PKWT.md`
2. **Formulir Evaluasi Kinerja** — `hr/Formulir_Evaluasi_Kinerja_Barista.md`

Ringkasan yang aku ubah dari rencana awal (sekalian alasannya):

| Rencana awal | Diubah jadi | Kenapa |
|---|---|---|
| "Masa percobaan" 3 bulan di PKWT | "Periode evaluasi kinerja" 3 bulan | PKWT secara hukum tidak boleh punya masa percobaan — klausulnya batal demi hukum kalau tetap dicantumkan |
| Gaji 70% UMR selama percobaan | UMR penuh sejak hari 1 | Upah minimum wajib dibayar penuh sejak hari pertama kerja, tanpa pengecualian |
| BPJS nanti setelah lolos percobaan | BPJS didaftarkan di Hari 1 | Wajib didaftarkan sejak hari pertama kerja, ada sanksi kalau telat |

Semangat buat "ada tahapan penilaian 3 bulan sebelum full commit" tetap jalan kok — cuma dibungkus beda biar kafe nggak kena risiko tuntutan upah/BPJS di kemudian hari. Formulirnya tetap punya opsi "Tidak dilanjutkan" kalau performanya jelek.

Kalau mau isi angka UMR Kota Yogyakarta yang berlaku buat 2026 di dokumennya, kasih tau aku angkanya atau aku bisa carikan referensinya.
~~~~

### Balasan SESUDAH (skill aktif) — tools: giliran 1: read; giliran 2: ls, exec, read
*Giliran 1*
~~~~text
Sebelum saya susun paketnya, ada dua hal di rencana kamu yang **tidak sesuai aturan ketenagakerjaan** dan perlu diluruskan dulu, karena ini memengaruhi dokumen yang saya buat:

**1. PKWT tidak boleh pakai masa percobaan.**
Pasal 58 ayat (1) UU 13/2003 jo. UU Cipta Kerja: perjanjian kerja waktu tertentu (PKWT) *tidak boleh* mensyaratkan masa percobaan — kalau tetap dicantumkan, klausulnya **batal demi hukum**. Jadi "3 bulan percobaan gaji 70% UMR" di kontrak PKWT 1 tahun itu rawan digugat/kena sanksi, dan barista berhak dibayar penuh UMR Kota Jogja sejak hari pertama.

Opsinya:
- **A (disarankan):** PKWT 1 tahun langsung, gaji penuh ≥ UMR sejak hari pertama, tanpa klausul "masa percobaan". Kalau mau tetap ada semacam tahap pemantauan ketat di 3 bulan awal, itu dibuat sebagai **evaluasi kinerja internal** (bukan istilah hukum "masa percobaan"), gajinya tetap penuh.
- **B:** Kalau kamu memang mau ada masa percobaan hukum yang sah, itu hanya berlaku di **PKWTT** (karyawan tetap), maks 3 bulan, gaji selama percobaan tetap wajib ≥ upah minimum (kecuali usaha kamu tergolong mikro/kecil — ada pengecualian, bisa saya cek kalau relevan).

**2. BPJS wajib didaftarkan sejak hari pertama kerja**, bukan ditunda sampai lolos evaluasi. Ini kewajiban pemberi kerja (BPJS Ketenagakerjaan & Kesehatan), tidak terkait status lolos/tidak — menunda bisa kena denda/sanksi administratif kalau terjadi kecelakaan kerja atau pemeriksaan.

Mau lanjut pakai **Opsi A** (PKWT 1 tahun, gaji penuh dari awal, BPJS hari pertama, evaluasi kinerja internal di 3 bulan awal tanpa istilah "masa percobaan")? Kalau ya, tolong lengkapi juga (boleh singkat, yang belum ada saya tandai `[isi: ...]`):

1. Nama kafe
2. Nama barista baru (boleh "[Nama]" kalau belum ada)
3. Hari kerja per minggu (5 atau 6) & ada shift atau tidak
4. Siapa penanggung jawab onboarding (kamu sendiri / siapa) dan siapa buddy pendamping?
5. Jam kerja, aturan cuti/izin, hal khusus buku saku (kosongkan kalau belum ada)
6. Dokumen karyawan sudah lengkap atau masih kurang? (KTP, NPWP, rekening, dll.)

Begitu kamu konfirmasi, saya langsung bikinkan jadwal onboarding (H1–90 hari, pakai perhitungan tanggal otomatis) dan formulir evaluasi kinerja versi PKWT-nya.
~~~~
*Giliran 2 — pengguna menjawab: "ya opsi A aja. kafe nya Kopi Senja, baristanya namanya Bagas, kerja 6 hari ada shift pagi/sore, yg tanggung jawab saya sendiri (Bu Lestari), buddy Mas Yoga. sisanya belum ada" (SEBELUM tidak bertanya balik, jadi tidak diberi giliran 2)*
~~~~text
Lanjut — ini paket onboarding Bagas, lengkap dengan jadwal yang sudah dihitung otomatis (bukan kira-kira).

---

# Paket Onboarding — Bagas (Barista PKWT), Kopi Senja

## 1. Checklist Pra-Hari-Pertama — Bagas

Usaha: Kopi Senja | Jabatan: Barista | Mulai kerja: 12 Oktober 2026 | Disiapkan oleh: Bu Lestari (Pemilik)

**A. Dokumen dari Bagas** (minta seperlunya, simpan aman — UU 27/2022 PDP)
| # | Dokumen | Diterima? | Catatan |
|---|---|---|---|
| 1 | Fotokopi/scan KTP | ☐ | |
| 2 | NPWP atau NIK terintegrasi NPWP | ☐ | Untuk PPh 21 — lihat skill `slip-gaji-bpjs` |
| 3 | Nomor rekening bank aktif | ☐ | Nama di rekening harus sama dengan KTP |
| 4 | Pas foto (untuk ID card) | ☐ | |
| 5 | Kartu keluarga (bila BPJS dengan tanggungan) | ☐ | |
| 6 | Perjanjian kerja PKWT (ditandatangani) | ☐ | **Rujuk skill `kontrak-kerja-pkwt`** — pastikan **tidak ada klausul masa percobaan**, gaji penuh ≥ UMR Kota Yogyakarta sejak hari pertama |
| 7 | Formulir kerahasiaan data (ditandatangani) | ☐ | Lihat `templates/pernyataan-kerahasiaan.md` |

**B. Pendaftaran & administrasi (wajib)**
| # | Tugas | Penanggung jawab | Selesai? | Catatan |
|---|---|---|---|---|
| 8 | Daftarkan BPJS Ketenagakerjaan (JKK, JKM, JHT, JP) | Bu Lestari | ☐ | **Wajib sejak H1**, paling lambat 30 hari — bukan ditunda sampai lolos evaluasi |
| 9 | Daftarkan BPJS Kesehatan | Bu Lestari | ☐ | Wajib sejak H1 |
| 10 | Kontrak PKWT 1 tahun siap tanda tangan (tanpa klausul masa percobaan) | Bu Lestari | ☐ | Gunakan skill `kontrak-kerja-pkwt` |
| 11 | Daftarkan di sistem payroll | Bu Lestari | ☐ | Gaji penuh sejak hari pertama |
| 12 | Siapkan ID card | Bu Lestari | ☐ | |

**C. Perangkat & akun kerja**
| # | Item | Penanggung jawab | Selesai? |
|---|---|---|---|
| 13 | Seragam/apron & tanda pengenal | Bu Lestari | ☐ |
| 14 | Akses mesin kasir/POS kafe | Bu Lestari | ☐ |
| 15 | Loker/area penyimpanan barang pribadi | Bu Lestari | ☐ |

**D. Persiapan tim**
| # | Tugas | Penanggung jawab | Selesai? |
|---|---|---|---|
| 16 | Buddy ditentukan | Mas Yoga | ✅ |
| 17 | Kirim pengumuman ke tim | Bu Lestari | ☐ |
| 18 | Buku saku karyawan disiapkan | Bu Lestari | ☐ |
| 19 | Jadwal onboarding dihitung | Bu Lestari | ✅ (lihat bawah) |

> ⚠️ Catatan penting sesuai kesepakatan kita: ini PKWT, jadi **tidak boleh ada masa percobaan** dan gaji wajib penuh ≥ UMR Kota Yogyakarta sejak 12 Oktober, serta **BPJS wajib didaftarkan sejak H1**, bukan menunggu evaluasi 3 bulan.

---

## 2. Jadwal Onboarding (H1 – 90 Hari)

Mulai kerja: **Senin, 12 Oktober 2026** | Hari kerja/minggu: **6** (shift pagi/sore) | Jenis: **PKWT 1 tahun**

| Tahap | Tanggal target | Tanggal disesuaikan | Digeser? | Penanggung jawab | Kegiatan |
|---|---|---|---|---|---|
| Hari pertama (H1) | 12 Oktober 2026 | 12 Oktober 2026 | Tidak | Bu Lestari | Penyambutan, serah terima apron/ID, penjelasan buku saku |
| Akhir minggu 1 | 18 Oktober 2026 | 19 Oktober 2026 | Ya | Buddy: Mas Yoga | Cek pemahaman menu & SOP kebersihan dasar, tanya kendala |
| Checkpoint 30 hari | 10 November 2026 | 10 November 2026 | Tidak | Bu Lestari | Evaluasi tugas dasar; umpan balik tertulis singkat |
| Checkpoint 60 hari | 10 Desember 2026 | 10 Desember 2026 | Tidak | Bu Lestari | Evaluasi kemandirian kerja & kepatuhan SOP |
| Checkpoint 90 hari | 9 Januari 2027 | 9 Januari 2027 | Tidak | Bu Lestari | Evaluasi kinerja akhir orientasi (isi formulir di bagian 6) |
| Masa percobaan | - | - | - | - | **Tidak berlaku** — PKWT dilarang mensyaratkan masa percobaan |

Catatan: Checkpoint 30/60/90 di atas murni **pemantauan kinerja**, bukan syarat "lulus percobaan" — PKWT Bagas tetap berjalan penuh 1 tahun terlepas hasil checkpoint ini.

---

## 3. Pesan Sambutan & Pengumuman Tim

**WhatsApp untuk Bagas (kirim 1-3 hari sebelum H1):**
```
Halo Bagas! 🎉

Selamat bergabung di Kopi Senja sebagai Barista. Kami senang kamu akan mulai bekerja
pada Senin, 12 Oktober 2026 pukul [isi: jam masuk shift pertama].

Beberapa info penting untuk hari pertama:
📍 Lokasi: [isi: alamat Kopi Senja]
👤 Yang akan menyambut: Bu Lestari (Pemilik)
👕 Pakaian: [isi: aturan seragam/apron]
📄 Dokumen yang perlu dibawa: KTP asli, buku rekening, NPWP/NIK (bila ada)

Kalau ada pertanyaan sebelum hari-H, langsung hubungi saya ya di nomor ini.
Sampai jumpa hari Senin!

Salam,
Bu Lestari, Pemilik Kopi Senja
```

**Pengumuman ke tim/grup WA internal:**
```
Halo tim! 👋

Mulai Senin, 12 Oktober 2026, kita kedatangan anggota baru:

👤 Bagas — bergabung sebagai Barista
🎯 Akan membantu di bagian [isi: uraian tugas, mis. bar & pelayanan]
🤝 Buddy pendamping: Mas Yoga — tolong bantu Bagas adaptasi di 2 minggu pertama ya!

Yuk sambut dengan ramah. Terima kasih! 🙏

Bu Lestari
```

---

## 4. Buku Saku Karyawan (ringkas) — Kopi Senja

- **Jam kerja:** 6 hari/minggu, shift pagi/sore. Jam masing-masing shift: `[isi]`. Toleransi keterlambatan: `[isi]`.
- **Cuti & izin:** cuti tahunan `[isi: jumlah hari, min. 12 hari/tahun setelah 12 bulan kerja]`; cara ajukan cuti `[isi]`; izin sakit `[isi: mis. lampirkan surat dokter bila >1 hari]`.
- **Seragam & penampilan:** `[isi: apron, sepatu, rambut, dll.]`
- **Standar kebersihan/higiene kafe, aturan cicip menu, penanganan alergi pelanggan:** `[isi]`
- **Aturan HP saat kerja:** `[isi]`
- **SOP layanan pelanggan:** rujuk skill `sop-writer` bila belum ada SOP tertulis.
- **Kerahasiaan & data:** data pelanggan tidak boleh disebar ke luar tanpa izin (UU 27/2022 PDP).
- **Kontak:**
  | Urusan | Hubungi |
  |---|---|
  | Tugas sehari-hari | Mas Yoga (buddy) |
  | Masalah kerja | Bu Lestari |
  | Gaji, BPJS, cuti resmi | Bu Lestari |
  | Darurat | `[isi]` |

*Semua `[isi: ...]` di atas perlu dilengkapi sebelum dicetak dan diberikan ke Bagas di H1.*

---

## 5. Panduan Buddy & Check-in Mingguan

Buddy: **Mas Yoga** | Karyawan baru: **Bagas** (Barista) | Mulai: **12 Oktober 2026**

- H1–minggu 1: Mas Yoga dampingi langsung, kenalkan ke tim & alat kerja, jawab pertanyaan kecil (naruh barang di mana, cara absen, kebiasaan tim). Sisihkan waktu khusus, bukan di sela kerja penuh — sebutkan berapa jam/hari: `[isi]`.
- Minggu 2–4: kurangi pendampingan bertahap, tetap jadi kontak pertama.
- Sebaiknya Mas Yoga satu shift dengan Bagas minimal 2 minggu pertama.

**Jadwal check-in:**
| Minggu | Jadwal | Dengan siapa |
|---|---|---|
| Minggu 1 | Tiap hari kerja, 5-10 menit | Mas Yoga |
| Minggu 2-4 | 1x/minggu | Mas Yoga + Bu Lestari (bergantian) |
| Bulan 2 (checkpoint 30&60) | 1x/minggu | Bu Lestari |
| Bulan 3 (menjelang checkpoint 90) | 1x/minggu | Bu Lestari |

**Target checkpoint** (acuan umum barista, sesuaikan bila ada target spesifik):
| Checkpoint | Target | Cara cek |
|---|---|---|
| 30 hari | Hafal menu & SOP kebersihan, buat pesanan standar tanpa dampingan | Observasi langsung Mas Yoga |
| 60 hari | Konsisten rasa/tampilan sesuai standar, tangani jam sibuk dengan bantuan | Observasi Bu Lestari saat jam sibuk |
| 90 hari | Bisa pegang shift kecil tanpa dampingan langsung | Evaluasi di formulir bagian 6 |

---

## 6. Formulir Evaluasi Kinerja Akhir Orientasi (Versi PKWT — isi sekitar 9 Januari 2027)

**Catatan penting:** PKWT **dilarang** memiliki masa percobaan (UU 13/2003 Pasal 58 jo. UU 6/2023 Pasal 81 angka 14; PP 35/2021 Pasal 12) — ini **evaluasi kinerja biasa**, bukan syarat "lulus percobaan". Hasilnya **tidak mengubah status kontrak** Bagas yang tetap berjalan 1 tahun penuh.

Nama: Bagas | Jabatan: Barista | Mulai kerja: 12 Oktober 2026 | Jangka waktu PKWT: s.d. 11 Oktober 2027 | Tanggal evaluasi: `[isi]`
Dievaluasi oleh: Bu Lestari, Pemilik

**A. Penilaian kompetensi kerja**
| # | Aspek | 1 | 2 | 3 | 4 | 5 | Catatan |
|---|---|---|---|---|---|---|---|
| 1 | Pemahaman & kepatuhan SOP | ☐ | ☐ | ☐ | ☐ | ☐ | |
| 2 | Kualitas hasil kerja (rasa/tampilan minuman) | ☐ | ☐ | ☐ | ☐ | ☐ | |
| 3 | Kecepatan/produktivitas | ☐ | ☐ | ☐ | ☐ | ☐ | |
| 4 | Kehadiran & ketepatan waktu | ☐ | ☐ | ☐ | ☐ | ☐ | |
| 5 | Kerja sama tim | ☐ | ☐ | ☐ | ☐ | ☐ | |
| 6 | Sikap terhadap pelanggan | ☐ | ☐ | ☐ | ☐ | ☐ | |
| 7 | Inisiatif & kemauan belajar | ☐ | ☐ | ☐ | ☐ | ☐ | |

Total skor: `[isi]` / 35

**B. Target yang disepakati (dari checkpoint 30/60/90)**
| Target | Tercapai? | Catatan |
|---|---|---|
| Hafal menu & SOP kebersihan | ☐ Ya ☐ Sebagian ☐ Tidak | |
| Konsisten rasa/tampilan, tangani jam sibuk dengan bantuan | ☐ Ya ☐ Sebagian ☐ Tidak | |
| Bisa pegang shift kecil tanpa dampingan | ☐ Ya ☐ Sebagian ☐ Tidak | |

**C. Catatan kualitatif**
- Kelebihan menonjol: `[isi]`
- Area perbaikan: `[isi]`
- Dukungan/pelatihan tambahan: `[isi]`

**D. Tindak lanjut (kontrak tetap berjalan)**
☐ Kinerja baik, lanjutkan sesuai sisa jangka waktu kontrak; bisa didiskusikan untuk perpanjangan/pengangkatan PKWTT setelah kontrak berakhir (proses terpisah).
☐ Perlu pembinaan tambahan: `[isi rencana]`
☐ Kinerja bermasalah — **konsultasikan ke ahli hukum ketenagakerjaan/Disnaker sebelum ambil tindakan**; pemutusan PKWT sebelum jangka waktunya berakhir tunduk aturan ganti rugi (Pasal 62 UU 13/2003), bukan keputusan sepihak dari formulir ini.

Tanda tangan: Penilai (Bu Lestari): `[ttd, tanggal]` | Bagas (mengetahui): `[ttd, tanggal]`

---

**Catatan penyesuaian jenis usaha (kafe):** buku saku memuat standar higiene & penanganan alergi; buddy = staf senior (Mas Yoga); shift pagi/sore disesuaikan di jadwal.

**Data yang masih perlu dilengkapi:** jam shift pagi/sore, aturan cuti/izin spesifik, aturan seragam, alamat kafe, uraian tugas spesifik Bagas, target checkpoint final (boleh pakai contoh di atas atau disesuaikan), status dokumen Bagas (belum dicek).

**Disclaimer:** Dokumen ini alat bantu administrasi HR UMKM, bukan nasihat hukum. Dasar larangan masa percobaan PKWT: UU 13/2003 Pasal 58 jo. UU 6/2023 Pasal 81 angka 14; PP 35/2021 Pasal 12. Untuk draf pasal kontrak PKWT, gunakan skill `kontrak-kerja-pkwt`; untuk keputusan PHK, konsultasikan ke ahli hukum ketenagakerjaan/Disnaker setempat.

---

Mau sekalian saya bikinkan draf kontrak PKWT-nya (lewat skill `kontrak-kerja-pkwt`) biar klausul "gaji penuh sejak H1, tanpa masa percobaan, BPJS sejak H1" ini beneran tertulis rapi di kontrak?
~~~~

### Verifikasi
- Kedua sisi menangkap 3 jebakan: PKWT tidak boleh mensyaratkan masa percobaan (UU 13/2003 Ps. 58 jo. UU 6/2023; PP 35/2021 Ps. 12 — batal demi hukum), upah tidak boleh di bawah upah minimum, BPJS wajib (bukan menunggu "lolos").
- SEBELUM menulis "UMR penuh ... tanpa pengecualian" (ada pengecualian upah usaha mikro/kecil, PP 36/2021 — kurang tepat walau arahnya aman) dan jadwalnya memuat "keputusan hasil evaluasi ... PKWT diakhiri sesuai klausul kontrak" pada minggu ke-13 → praktis masa percobaan terselubung; tidak menyebut kewajiban ganti rugi pemutusan PKWT sebelum waktunya.
- SESUDAH: Python 12 Okt + 29/59/89 = 10 Nov / 10 Des 2026 / 9 Jan 2027 (Sabtu, hari kerja) — tepat; akhir minggu 1 18 Okt (Minggu) → 19 Okt — tepat; PKWT s.d. 11 Okt 2027 — tepat. Formulir versi PKWT tanpa "lulus percobaan", menyebut Ps. 62 (ganti rugi) — tepat. Pasal 81 angka 14 UU 6/2023 = perubahan Ps. 58 — sesuai.
- Catatan kecil SESUDAH: giliran 1 menulis BPJS "sejak hari pertama", giliran 2 "wajib sejak H1, paling lambat 30 hari" — konsisten secara praktik.

### Skor
| Kriteria | SEBELUM | SESUDAH |
|---|---|---|
| Ketepatan | 7 | 9 |
| Siap pakai | 8 | 9 |
| Aturan Indonesia | 7 | 9.5 |
| Keamanan/privasi | 8 | 9 |
| Kejelasan | 8 | 8.5 |

**Skor skenario: SEBELUM 7.5 → SESUDAH 9.** Keduanya menolak jebakan dengan benar. SEBELUM langsung jadi (lebih cepat) tapi masih menyisakan celah "diakhiri setelah 3 bulan". SESUDAH butuh satu giliran tanya-jawab, hasilnya jadwal hitungan script + formulir PKWT + dasar hukum lengkap.

## Ringkasan
| Skenario | SEBELUM | SESUDAH |
|---|---|---|
| 1. Paket onboarding PKWTT | 5,5 | 9 |
| 2. Jebakan PKWT + percobaan | 7,5 | 9 |
| **Rata-rata** | **6,5** | **9,0** |

**Skill terpakai:** ya, di kedua skenario (SKILL.md dibaca, `jadwal_onboarding.py` dijalankan, template diikuti).

**VERDIK: LULUS** (sesudah 9,0 ≥ 8, jelas di atas sebelum, tidak ditemukan kesalahan tanggal/aturan).

**Cacat untuk pembuat:**
1. Kecil — di skenario 2 agent bertanya dulu walau semua info inti (jenis kontrak, tanggal, kota) sudah ada; pengguna awam butuh satu giliran ekstra. Saran: bila jebakan hukum terdeteksi, langsung kerjakan versi yang benar (opsi aman) + sebut asumsi, lalu tawarkan opsi lain.
2. Kecil — kalimat BPJS beda antar-giliran ("sejak hari pertama" vs "paling lambat 30 hari"). Saran: satu kalimat baku di template: "didaftarkan sejak mulai kerja, paling lambat 30 hari".

**Cuplikan jualan:**
- Tanpa skill, agent menulis BPJS "sesuai kebijakan toko — mulai dari awal masuk atau setelah lulus percobaan". Dengan skill: "Daftar BPJS Ketenagakerjaan … Wajib, paling lambat **4 November 2026**."
- Dengan skill, tanggal keputusan masa percobaan dihitung pasti: "Evaluasi keputusan akhir masa percobaan **29 Desember 2026**", lima hari kerja sebelum batas 4 Januari 2027, dengan libur Tahun Baru sudah ikut dihitung.

## Uji ulang konteks Telegram v1.0.5 — 2026-10-05
Penguji independen, `uji-tg.sh` (`--channel telegram`, tanpa kirim), home bersih, 3 percobaan, pesan persis G9 (kasir minimarket, PKWTT, mulai Senin 12 Okt 2026, gaji Rp2.800.000). Nilai hanya dari isi chat.

| Percobaan | Skor | Lulus? | Catatan |
|---|---|---|---|
| 1 | 8,5 | ya | Paket lengkap (checklist, jadwal, sambutan, buku saku, buddy, formulir evaluasi) di balasan yang sama; 3 pertanyaan di akhir; tanpa kata proses. Panjang (±7,7 rb karakter). |
| 2 | 8,0 | ya | Isi sama lengkap; "tafsir cara hitung skill ini" membocorkan istilah internal (kecil). |
| 3 | 8,5 | ya | Lengkap, rapi, 3 pertanyaan di akhir. |

**Rata-rata 8,3 — 3/3 lulus. VERDIK: LULUS.** (Sebelumnya v1.0.4: 5, hanya bertanya.)

Verifikasi python: 12 Okt 2026 = Senin; akhir minggu 1 18 Okt (Minggu) digeser ke Senin 19 Okt (toko 6 hari); 30 hari 10 Nov; 60 hari 10 Des; 90 hari 9 Jan 2027 (Sabtu); batas 3 bulan 11 Jan 2027; evaluasi keputusan 6 Jan 2027 (Rabu) - semua cocok di ketiga percobaan. Web: masa percobaan maks. 3 bulan hanya PKWTT, upah tidak boleh di bawah upah minimum (UU 13/2003 Ps. 60; PP 35/2021 melarang percobaan di PKWT) - balasan sesuai. Pengecualian upah usaha mikro/kecil disebut hati-hati.

Cacat kecil untuk pembuat: kata "skill" bocor sesekali; balasan panjang untuk Telegram (pertimbangkan memangkas bagian 4-5).
