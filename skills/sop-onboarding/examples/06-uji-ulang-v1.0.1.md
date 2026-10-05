# Uji 06 — Uji ulang independen v1.0.1 (Tahap 6 butir 7)

Tanggal uji: 25 September 2026 · Penguji: agent terpisah (bukan pembuat, perevisi, atau penguji v1.0.0) ·
Skill disalin ke scratchpad (`uji2-onb/sop-onboarding/`) dan dijalankan dari sana · Versi diuji: 1.0.1.

## 1. Verifikasi tanggal independen

### Metode
Penguji menulis penghitung sendiri (`verif2.py`, di scratchpad) **tanpa membaca kode script**, hanya dari
aturan SKILL.md langkah 3:
- Minggu 1 = mulai + 6; checkpoint 30/60/90 = mulai + 29/59/89; semuanya digeser **maju** ke hari kerja.
- Batas hukum PKWTT = tanggal sama 3 bulan kemudian − 1 hari; bila tanggal itu tidak ada → hari terakhir
  bulan itu (tanpa −1). Tidak pernah digeser.
- Evaluasi keputusan = hari kerja ke-5 dihitung mundur, **termasuk** hari kerja terakhir ≤ batas.
  (Teks "5 hari kerja sebelum batas" bisa dibaca dua cara; tafsir "termasuk" dipilih karena hanya itu
  yang cocok dengan contoh Sinta 19 Des 2026. Lihat temuan B-3.)
- Hari kerja 5 = Sen–Jum, 6 = Sen–Sab; libur nasional **dan** cuti bersama dianggap bukan hari kerja.
- Peringatan H1 bila tanggal mulai bukan hari kerja; peringatan checkpoint 90 bila checkpoint 90 setelah
  digeser > batas hukum.

Daftar libur disusun penguji sendiri dari web search (lalu baru dicocokkan dengan CSV skill):
- **2026** (SKB 3 Menteri No. 1497/2/5 Tahun 2025; 17 libur + 8 cuti bersama): cocok 25/25 tanggal dengan
  `references/libur-nasional-2026.csv`.
- **2027** (SKB 3 Menteri ditandatangani 15 Sep 2026; 18 libur + 8 cuti bersama): cocok 26/26 tanggal dengan
  `references/libur-nasional-2027.csv`, termasuk Nyepi 8 Mar, cuti bersama Idulfitri 9/12/15 Mar, Idulfitri
  10–11 Mar, Isra Mikraj 26 Des 2027.
- Sumber: antaranews.com/berita/5741357 ; news.detik.com/berita/d-8664635 ; hukumonline.com (daftar libur 2027
  lt6aaa6070150ec dan cuti bersama 2026 lt68d137f7bd314) ; kemenag.go.id (SKB 2027) ; setneg.go.id (SKB 2026 &
  2027, hanya lewat hasil pencarian — situs diblokir proxy).

### Hasil perbandingan dengan script (`--format json`)
| Uji | Jumlah | Beda |
|---|---|---|
| Acak 2026–2027 (seed 20260925), 5 & 6 hari, PKWTT & PKWT | 320 | **0** |
| Kasus khusus × (5, 6 hari) | 36 | **0** |
| Hampir menyeluruh: tiap 3 hari 1 Jan 2026–31 Des 2027, 5 & 6 hari, PKWTT | 488 | **0** |
| Properti (penghitung mandiri, semua 730 tanggal × 2): evaluasi > batas | 1.460 | **0** kasus |
| Properti: evaluasi/minggu1/checkpoint jatuh di libur/akhir pekan | 1.460 | **0** kasus |

Dari 356 kasus pertama: peringatan checkpoint 90 muncul 39×, peringatan H1 98×, semuanya sama persis
dengan penghitung mandiri. Satu-satunya perbedaan struktural: PKWT punya baris informasi
`percobaan_pkwt` dengan tanggal `null` (disengaja, bukan tanggal).

### Kasus khusus (nilai dari penghitung mandiri = script)
| Mulai | HK | Batas hukum | Evaluasi keputusan | Checkpoint 90 | Peringatan |
|---|---|---|---|---|---|
| Sen 14 Des 2026 | 5 | Sab 13 Mar 2027 | **Sen 1 Mar 2027** (melewati 8–12 Mar: Nyepi + Lebaran) | 16 Mar 2027 | ✅ ⚠️ checkpoint 90 > batas |
| Sen 14 Des 2026 | 6 | 13 Mar 2027 | Rab 3 Mar 2027 | 13 Mar 2027 | — (90 = batas, tidak lewat) |
| Sen 28 Sep 2026 | 6 | Min 27 Des 2026 | **Sab 19 Des 2026** (melewati 24–25 Des) | 26 Des 2026 | — |
| Sen 28 Sep 2026 | 5 | 27 Des 2026 | Kam 17 Des 2026 | 28 Des 2026 | ✅ ⚠️ checkpoint 90 |
| Min 31 Jan 2027 | 5/6 | 30 Apr 2027 | Sen 26 Apr 2027 | 30 Apr 2027 | ✅ ⚠️ H1 (saran 1 Feb) |
| Sab 31 Jan 2026 | 5 | 30 Apr 2026 | 24 Apr 2026 | 30 Apr 2026 | ✅ ⚠️ H1 |
| Sen 30 Nov 2026 | 5 | 28 Feb 2027 | 22 Feb 2027 | 1 Mar 2027 | ✅ ⚠️ checkpoint 90 |
| Sel 30 Nov 2027 | 5 | 29 Feb 2028 | 23 Feb 2028 | 28 Feb 2028 | — |
| Sel 29 Feb 2028 | 5 | 28 Mei 2028 | 22 Mei 2028 | 29 Mei 2028 | ✅ ⚠️ checkpoint 90 |
| Min 4 Okt 2026 | 5 | 3 Jan 2027 | Rab 23 Des 2026 | 4 Jan 2027 | ✅ ⚠️ H1 + ⚠️ checkpoint 90 |
| Jum 25 Des 2026 (Natal) | 5/6 | 24 Mar 2027 | 18 / 19 Mar 2027 | — | ✅ ⚠️ H1 (saran 28 / 26 Des) |
| Rab 10 Mar 2027 (Lebaran) | 5/6 | 9 Jun 2027 | 3 / 4 Jun 2027 | — | ✅ ⚠️ H1 (saran 16 Mar / Sab 13 Mar) |

Semua cocok. **P1-1 (evaluasi melewati batas) tuntas**: evaluasi keputusan kini baris terpisah, selalu ≤ batas
dan selalu hari kerja; checkpoint 90 yang melewati batas diberi peringatan ⚠️ di atas tabel dan di catatan.

### Penilaian definisi "3 bulan"
(mulai + 3 bulan kalender) − 1 hari, dengan klip akhir bulan (31 Jan → 30 Apr; 29/30 Nov → 28 Feb) **wajar**:
tidak pernah melebihi 3 bulan kalender dan sesuai cara umum menghitung jangka waktu. Karena evaluasi
dijadwalkan 5 hari kerja sebelumnya, selisih 1–2 hari antar-tafsir di akhir bulan tidak berisiko.
**Namun** SKILL.md, script, dan referensi menyajikannya sebagai "Definisi batas" yang pasti — tidak ada
kalimat bahwa ini **tafsir** (UU tidak merinci cara menghitung "3 bulan"), dan tidak ada saran mengikuti
tanggal yang tertulis di perjanjian kerja bila berbeda (temuan B-1).

## 2. Verifikasi contoh & perbaikan P2
| Item | Status | Bukti |
|---|---|---|
| P1-2 contoh SKILL.md | ✅ tanggal cocok persis dengan `--mulai "28 September 2026" --hari-kerja 6 --jenis pkwtt` (26 Des / 27 Des / 19 Des) | output script |
| P1-2 README | ✅ "checkpoint 90 26 Des, batas hukum 27 Des, evaluasi 19 Des" cocok; tidak lagi menyebut 25 Des | README |
| Klaim di contoh SKILL.md "tidak ada [libur] yang jatuh di rentang ini" | ❌ salah: 24–25 Des 2026 ada di rentang dan **menggeser** evaluasi (tanpa libur = 22 Des; dengan libur = 19 Des) | B-2 |
| Kolom kegiatan/penanggung jawab contoh | ⚠️ diringkas ("Buddy: Rina", "Pemantauan rutin") ≠ teks script; ditandai "ringkas", bisa diterima | — |
| P2-1 H1 di libur | ✅ peringatan ⚠️ + saran tanggal kerja berikutnya, tidak digeser otomatis (sesuai SKILL.md) | 98 kasus |
| P2-2 libur bawaan | ✅ 2026 & 2027 dimuat otomatis dan benar; `--libur` digabung, bukan mengganti (uji `extra.csv` 28 Des 2026 → ⚠️ H1) | — |
| P2-3 aturan geser & definisi | ✅ tertulis di SKILL.md langkah 3, identik dengan script | 844 kasus 0 beda |
| P2-4 upah usaha mikro/kecil | ✅ ada di checklist mutu SKILL.md, catatan script, `references/dasar-hukum-onboarding.md` poin 5b bertanda PERLU REVIEW. Isi cocok dengan web search: Ps. 90B dikecualikan; kesepakatan min. 50% rata-rata konsumsi provinsi & 25% di atas garis kemiskinan (PP 36/2021 Ps. 36) | hukumonline.com/klinik/a/upah-minimum-usaha-kecil-lt50c7d16e6ea32 ; literasihukum.com/upah-minimum-umkm ; katadata.co.id |
| P2-5 formulir PKWT | ✅ `formulir-evaluasi-orientasi-pkwt.md` tanpa opsi "lulus masa percobaan"; ada catatan Ps. 62 (ganti rugi) & konsultasi Disnaker | — |
| Panduan buddy + check-in mingguan | ✅ `templates/panduan-buddy.md` (harian minggu 1, mingguan bulan 1–3, alokasi waktu buddy) | — |
| Target per jabatan | ✅ tabel 6 jabatan di `references/varian-jenis-usaha.md`, dengan larangan mengarang angka | — |
| Retrospektif | ✅ `templates/retrospektif-onboarding.md`, opsional | — |
| Tes bawaan | ✅ `python3 tests/uji_regresi.py` → **LULUS 136 cek** (termasuk 14 Des 2026, 4 Okt 2026, 28 Sep 2026) | — |
| SKILL.md | ✅ 204 baris (< 300); frontmatter hanya `name` & `description` | — |

## 3. Uji data rusak (baru)
| Input | Hasil |
|---|---|
| `28-9-26`, `besok`, `Senin 28 September 2026` (tanpa koma), `30 Februari 2027`, kosong | ✅ ERROR ramah, exit 2 |
| `28/09/2026`, `2026/09/28`, `28 Sep 2026`, `28 Sept 2026`, `Senin, 28 September 2026` | ✅ terbaca benar |
| `--libur` dengan BOM UTF-8, baris kosong/spasi/komentar `#`, header `Tanggal,Keterangan` + tanggal teks | ✅ terbaca |
| `--libur` tanggal tak ada (`2026-02-30`), path berupa folder | ✅ ERROR ramah dengan nomor baris |
| `--libur` CSV titik-koma (`tanggal;keterangan`) | ❌ masih gagal di baris 1 (P3 lama) |
| `--mulai 9999-12-31` | ❌ masih `Traceback OverflowError` (P3 lama) |
| `--mulai 0001-01-01`, `1900-01-01`, `2100-01-01` | ⚠️ diterima tanpa peringatan tahun tak wajar (P3 lama); hanya catatan "tidak ada data libur" |
| `--jenis PKWT` (huruf besar), `--hari-kerja 4` | ✅ ditolak argparse (pesan bahasa Inggris; agent bisa ulang) |
| Mulai 1 Des 2027 (evaluasi di Feb 2028, dekat Idulfitri 1449 H) | ⚠️ libur 2028 belum ada (SKB belum terbit); hanya poin catatan di bawah tabel, **bukan** baris ⚠️ di atas tabel (B-5) |

## 4. Ulang skenario 02 — Klinik gigi, perawat PKWT 1 tahun, mulai 1 Des 2026

**Input:** "Klinik gigi saya di Bandung terima perawat gigi baru, kontrak PKWT 1 tahun mulai 1 Desember 2026.
Klinik buka Senin–Sabtu, 2 shift. Buatkan paket onboarding, tolong tekankan soal kerahasiaan data pasien."

Mengikuti SKILL.md v1.0.1: info cukup untuk mulai (nama & buddy belum ada → `[isi: ...]`, disebut sebagai
asumsi). Perintah (libur bawaan dimuat otomatis, tidak perlu menyusun file libur seperti di uji 02 lama):
```bash
python3 scripts/jadwal_onboarding.py --mulai "1 Desember 2026" --hari-kerja 6 --jenis pkwt \
  --nama "[Nama], Perawat Gigi" --format markdown
```

### Output agent (ringkas tapi lengkap per format)

# Paket Onboarding — [Nama], Perawat Gigi, [Nama Klinik Gigi], Bandung

Asumsi: nama karyawan, nama klinik, penanggung jawab, dan buddy belum disebut → ditandai `[isi: ...]`.
Status **PKWT 1 tahun** → **tanpa masa percobaan** (dilarang; bila dicantumkan batal demi hukum — UU 13/2003
Ps. 58 jo. UU 6/2023 Ps. 81 angka 14; PP 35/2021 Ps. 12).

## 1. Checklist Pra-Hari-Pertama
| # | Item | Catatan |
|---|---|---|
| 1 | Salinan KTP, NPWP/NIK, rekening gaji, pas foto | Minta seperlunya, simpan di folder berakses terbatas (UU 27/2022 PDP) |
| 2 | **STR & SIP perawat gigi** | Wajib untuk tenaga kesehatan; verifikasi keabsahan **di luar cakupan skill ini** → bagian legal/Dinkes |
| 3 | Perjanjian kerja PKWT 1 tahun (1 Des 2026 s.d. [isi: tanggal akhir sesuai kontrak]) | Susun/cek lewat skill `kontrak-kerja-pkwt`; **tanpa** klausul masa percobaan |
| 4 | BPJS Ketenagakerjaan & BPJS Kesehatan | **Wajib**, paling lambat 30 hari sejak mulai kerja — targetkan selesai sebelum checkpoint 30 hari (30 Des 2026) |
| 5 | Pernyataan kerahasiaan + poin rekam medis pasien | `templates/pernyataan-kerahasiaan.md`; ketentuan medis khusus → konsultasi legal/Dinkes |
| 6 | Seragam klinik, APD (masker, sarung tangan), loker, akun sistem pendaftaran/jadwal | [isi: penanggung jawab] |
| 7 | Jadwal shift minggu 1 (selalu bersama buddy) | [isi: shift pagi/sore] |

## 2. Jadwal Onboarding (H1 – 90 Hari)
| Tahap | Tanggal target | Tanggal disesuaikan | Digeser? | Penanggung jawab | Kegiatan |
|---|---|---|---|---|---|
| Hari pertama (H1) | 1 Desember 2026 | 1 Desember 2026 | Tidak | Pemilik/Atasan langsung | Penyambutan, serah terima perangkat & akun, penjelasan buku saku karyawan |
| Akhir minggu 1 | 7 Desember 2026 | 7 Desember 2026 | Tidak | Buddy/rekan pendamping | Cek pemahaman tugas dasar & SOP harian, tanya kendala |
| Checkpoint 30 hari | 30 Desember 2026 | 30 Desember 2026 | Tidak | Atasan langsung | Evaluasi checklist tugas dasar; beri umpan balik tertulis singkat |
| Checkpoint 60 hari | 29 Januari 2027 | 29 Januari 2027 | Tidak | Atasan langsung | Evaluasi kemandirian kerja & kepatuhan SOP |
| Checkpoint 90 hari | 28 Februari 2027 | 1 Maret 2027 | Ya | Pemilik/Atasan | Evaluasi checkpoint orientasi |
| Masa percobaan | - | - | Tidak | - | Tidak berlaku untuk PKWT |

- Checkpoint 90 hari: evaluasi akhir orientasi (formulir evaluasi kinerja versi PKWT).
- Masa percobaan: PKWT DILARANG mensyaratkan masa percobaan; bila ada, batal demi hukum. Checkpoint 30/60/90
  hanya pemantauan kinerja biasa.
- Libur 24–25 Des 2026 & 1 Jan 2027 tidak mengenai tanggal kegiatan; bila klinik tetap buka di hari itu,
  jangan jadwalkan perawat baru tanpa buddy.

## 3. Pesan Sambutan & Pengumuman Tim
WA (santai-sopan, varian klinik): "Halo [Nama]! Selamat bergabung di [Nama Klinik] sebagai perawat gigi.
Kamu mulai Selasa, 1 Desember 2026 pukul [isi: jam shift]. Yang menyambut: [isi: kepala klinik/dokter
penanggung jawab]. Mohon bawa KTP asli, STR/SIP asli (untuk dicek, bukan ditahan), dan buku rekening. Sampai
jumpa!" — plus pengumuman ke grup tim dengan nama buddy [isi].

## 4. Buku Saku Karyawan (ringkas)
Jam kerja & shift: Senin–Sabtu, 2 shift [isi: jam]. Cuti/izin: [isi] (min. 12 hari kerja setelah 12 bulan).
Seragam & APD: [isi]. HP: [isi]. **Kerahasiaan data pasien:** jangan memfoto rekam medis/wajah/rontgen
pasien, jangan membahas pasien di grup WA pribadi, akses data pasien hanya lewat akun sendiri, laporkan
kebocoran ke [isi]. Materi diagnosis/klinis **tidak** dibuat di sini. Kontak: buddy [isi], atasan [isi].

## 5. Panduan Buddy, Check-in Mingguan & Target
Buddy: [isi: perawat senior]. Check-in harian 5–10 menit minggu 1 (1–7 Des 2026), mingguan bulan 1–3.
Jabatan "perawat gigi" tidak ada di tabel target → 3 target non-klinis dari tugas utama, tanpa angka karangan:
| Checkpoint | Target | Cara cek |
|---|---|---|
| 30 hari (30 Des 2026) | Paham alur pasien, SOP sterilisasi alat & kerahasiaan rekam medis klinik ini | Observasi buddy + checklist SOP |
| 60 hari (29 Jan 2027) | Menyiapkan ruang & alat tindakan mandiri sesuai SOP klinik | Observasi atasan |
| 90 hari (1 Mar 2027) | Menjalankan shift dengan supervisi minimal | Umpan balik dokter/atasan |
Kompetensi klinis & kewenangan praktik dinilai sesuai STR/SIP dan aturan profesi, bukan oleh skill ini.

## 6. Formulir Evaluasi Akhir Orientasi
Pakai `templates/formulir-evaluasi-orientasi-pkwt.md` (tanpa istilah "lulus masa percobaan"), isi sekitar
1 Mar 2027. Hasil tidak mengubah status PKWT; kinerja bermasalah → konsultasi ahli hukum/Disnaker, pemutusan
sebelum kontrak berakhir tunduk Ps. 62 (ganti rugi).

## 7. Retrospektif (opsional, setelah 1 Mar 2027)
`templates/retrospektif-onboarding.md`.

Catatan penyesuaian: varian klinik (STR/SIP, rekam medis, APD, buddy perawat senior, 2 shift).
Data yang perlu dilengkapi: nama, klinik, jam shift, cuti, buddy, penanggung jawab, tanggal akhir kontrak.
Disclaimer: alat bantu administrasi, bukan nasihat hukum; dasar hukum per 25 Sep 2026 di
`references/dasar-hukum-onboarding.md`.

### Penilaian skenario 02
✅ Tanpa baris/klausul masa percobaan, dasar larangan disebut; formulir PKWT dipakai; libur dimuat otomatis
(perbaikan dari uji lama yang butuh file libur buatan penguji); target tidak mengarang angka dan tidak masuk
ranah klinis; kerahasiaan pasien ditekankan tanpa mengarang ketentuan medis. ⚠️ Skill tidak mengingatkan
bahwa PKWT hanya boleh untuk pekerjaan yang **tidak bersifat tetap** (Ps. 59) — perawat klinik lazimnya
pekerjaan tetap; cukup satu kalimat rujukan ke `kontrak-kerja-pkwt` (B-6).

## 5. Temuan baru
**P2**
- **B-1 Definisi "3 bulan" tidak dinyatakan sebagai tafsir.** SKILL.md langkah 3, catatan script, dan
  referensi menyebutnya "Definisi batas" seolah kepastian hukum. *Usul:* tambah "tafsir perhitungan yang umum
  dipakai; UU tidak merinci — ikuti tanggal di perjanjian kerja bila berbeda dan konsultasikan bila ragu".

**P3**
- **B-2** Contoh SKILL.md menulis "tidak ada [libur] yang jatuh di rentang ini" — keliru; Natal 24–25 Des 2026
  ada di rentang dan justru menggeser evaluasi dari 22 ke 19 Des. Ganti kalimatnya (sekaligus contoh bagus
  manfaat libur bawaan).
- **B-3** "5 hari kerja sebelum batas (dihitung mundur dari hari kerja terakhir ≤ batas)" ambigu (termasuk/
  tidak termasuk hari kerja terakhir); fallback manual bisa beda 1 hari kerja. Tulis "hari kerja ke-5 dihitung
  mundur, hari kerja terakhir ≤ batas dihitung sebagai ke-1".
- **B-4** Cuti bersama diperlakukan sebagai libur tanpa menyebut bahwa bagi swasta cuti bersama mengikuti
  kebijakan perusahaan (SKB). Aman (evaluasi jadi lebih awal), tetapi layak satu kalimat.
- **B-5** Data libur tahun berikutnya (2028) tidak ada → hanya catatan di bawah tabel; jadikan baris ⚠️ di atas
  tabel bila rentang jadwal melewati tahun tanpa data libur.
- **B-6** Pengingat PKWT hanya untuk pekerjaan tidak tetap (Ps. 59) belum ada (rujuk `kontrak-kerja-pkwt`).
- **B-7** SKILL.md menyebut contoh "varian bengkel … tanggal mulai di hari libur" di `examples/` — belum ada
  (P3 lama).
- **B-8** P3 lama belum diperbaiki: overflow `9999-12-31` (Traceback), tahun tak wajar diterima, CSV
  titik-koma gagal. Urutan tabel: baris batas hukum ditaruh sebelum evaluasi yang lebih awal (tidak kronologis).
- **B-9** Pasal 62 disebut di formulir PKWT tetapi tidak ada di tabel `references/dasar-hukum-onboarding.md`.

## 6. Skor
**8 / 10 — LULUS quality gate.** Lihat `HASIL-UJI.md` bagian "Uji ulang v1.0.1".
