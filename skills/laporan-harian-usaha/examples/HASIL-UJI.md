# HASIL UJI — laporan-harian-usaha v1.0.0

- **Tanggal:** 2026-09-24
- **Penguji:** agent penguji independen (simulasi, Claude Code), bukan pembuat skill. Hanya membaca folder skill + SKILL.md alat yang dibaca skill ini.
- **Lingkungan:** Linux, Python 3.11. Skill + 4 alat disalin ke scratchpad (`<uji>/skills/`), HOME palsu, `KOMUNITECH_DATA` sementara, `TZ=Asia/Jakarta` (dan `UTC` untuk uji zona). Tidak ada yang dipasang di `.claude/skills` repo, tidak ada yang ditulis ke `~/KomunitechData` asli.
- **Data uji:** dibuat sendiri dengan script resmi `kasir.py`, `stok.py`, `absensi.py`, `cek_jatuh_tempo.py` (kafe 4 alat 7–24 Sep; toko online hanya buku-stok). Semua nama fiktif.
- **Uji regresi bawaan:** `tests/uji_regresi.py` → 31 tes OK (dijalankan ulang di salinan; tidak dijadikan dasar penilaian).
- **Uji muat OpenClaw:** `bash scripts/uji_openclaw.sh` → OpenClaw **2026.9.6**: `laporan-harian-usaha` ada di `eligible`, `modelVisible`, `commandVisible` (seluruh 53/53 skill lulus).
- **Platform teruji:** `claude-code (simulasi agent)`; `openclaw (uji muat otomatis)`. Pengiriman Telegram & perilaku agent OpenClaw **tidak** diuji penguji ini.

## Audit keamanan singkat
Script hanya memakai library standar; tanpa jaringan. `subprocess` hanya menjalankan script alat Komunitech (`sys.executable` + path file yang ditemukan, tanpa shell) dengan ENV `KOMUNITECH_*` dibuang dan `--db` diarahkan ke salinan. DB dibuka `mode=ro` + `VACUUM INTO` ke folder sementara yang dihapus di `finally` (0 folder `laporan-usaha-*` tersisa). `rmtree` hanya pada folder sementara buatan sendiri. Tidak membaca kredensial. Tidak ada prompt injection di SKILL.md/README/references. Catatan: script alat juga dicari di `./skills`, `./.claude/skills` pada folder kerja; folder kerja milik pengguna, jadi risiko rendah. **Lulus.**

## Skenario
| No | Berkas | Isi | Hasil |
|---|---|---|---|
| 00 | `00-pembanding-tanpa-skill.md` | A/B skenario 01 | Skill **jelas lebih baik** (omzet benar vs +19,5%, selisih kas, privasi, lembur) |
| 00 | `00-banding-pesaing.md` | biz-reporter, daily-report, oc-daily-business-report, sellerclaw | Tidak ada pesaing setara; terdekat 11/35 vs 34/35 |
| 01 | `01-kafe-harian-empat-alat.md` | Kafe PBJT 10%, 4 alat, void+retur+selisih kas, `--samarkan`, tengah malam WIB | **Lulus**; angka 100% cocok |
| 02 | `02-mingguan-minggu-lalu.md` | Minggu lalu vs sebelumnya, jadwal Senin 07.00, minggu berjalan | **Lulus**; angka 100% cocok |
| 03 | `03-toko-online-hanya-buku-stok.md` | Tanpa kasir: omzet dari buku-stok (offline + Shopee, batal/rusak tidak dihitung) | **Lulus**; angka 100% cocok |
| 04 | `04-input-buruk.md` | Tanggal masa depan/tidak ada, tz salah, DB rusak/0 byte, alat hilang, DB terkunci, CSV rusak/nomor HP, impor sebagian | **Lulus** (tidak crash/menggantung/menulis); 3 temuan |
| 05 | `05-di-luar-cakupan.md` | Kirim ke grup WA pelanggan, laba rugi, ubah angka, tandai lunas | **Lulus**; 1 celah instruksi rendah |

## Verifikasi angka independen
Query SQLite read-only sendiri + hitung manual (tidak memakai kode skill):
| Diuji | Hasil |
|---|---|
| Omzet bersih, uang diterima/PBJT, nota sah, rata-rata, per metode, terlaris (harian 24/9) | **0 beda** |
| Pembanding kemarin & hari yang sama minggu lalu; mingguan 14–20/9 vs 7–13/9; minggu berjalan 21–24/9 vs 14–17/9 | **0 beda** |
| Omzet buku-stok (offline + marketplace; batal & rusak dikecualikan), 3 pembanding | **0 beda** |
| Selisih kas (tabel `sesi`), stok minus/habis/menipis + restock, belum dikemas | **0 beda** |
| Kehadiran harian (terlambat menit, sakit/alpa/belum absen, lembur perlu keputusan) & mingguan (36 hari, 35 hadir, 3× / 72 mnt) | **0 beda** |
| Tagihan: hari terlambat, hari ini/besok, total tertunggak, baris rusak | **0 beda** |
| Fungsi persen vs rumus acuan `Fraction` (0,05 menjauhi nol): 20.008 kasus acak + tepi (±0,05) | **0 beda** |
| File asli (9 file, sha256) sebelum = sesudah ±15 kali jalan, termasuk DB terkunci/rusak | **sama** |
| Nama/perihal/catatan pelanggan & nomor HP di teks + JSON | **0 bocor** |
| `--samarkan` harian & mingguan (termasuk `perlu_dicek`, `sering_terlambat`) | nama → inisial, 0 bocor |

## Temuan cacat
| ID | Keparahan | Lokasi | Temuan & reproduksi |
|---|---|---|---|
| **S1** | **Sedang** | `scripts/laporan.py:439-443` (`cek_impor_kasir_ke_stok`) | Cek "penjualan kasir belum diimpor ke buku-stok" hanya menguji **ada ≥ 1 nota** tanggal itu di tabel `pesanan`. Impor **sebagian** (mis. ekspor siang, nota sore belum) tidak terdeteksi; laporan diam padahal stok belum terpotong. Repro: data skenario 01 → `kasir.py ekspor --format buku-stok --tanggal 2026-09-24` → sisakan hanya baris N-260924-0001 → `stok.py impor-pesanan … --ya` → `laporan.py` : butir "belum diimpor" hilang (6 dari 7 nota belum memotong stok). Saran: bandingkan himpunan nomor nota jual kasir (nota non-void) dengan `pesanan.no_pesanan`, laporkan jumlah yang belum. |
| R1 | Rendah | `laporan.py:697`, `:817` | Laporan **hari ini** setelah jam pulang (jadwal default 21.00): karyawan tanpa tap & tanpa keterangan ditulis "Belum absen (1): Tari" dan **tidak** masuk PERLU PERHATIAN (`not hd.get("hari_ini")`). Jadwal harian berikutnya melaporkan tanggal lain, jadwal mingguan baru Senin, jadi ketidakhadiran tanpa kabar tidak pernah muncul sebagai butir perhatian di laporan harian. Repro: skenario 01 (`--sekarang 2026-09-24T21:30+07:00`). Saran: setelah jam pulang shift, perlakukan seperti "Tanpa keterangan". |
| R2 | Rendah | `laporan.py:694-696` | Laporan hari ini **sebelum jam masuk** memberi alarm palsu "Belum ada satu pun data absen hari itu. File mesin absen mungkin belum diimpor." Repro: `--sekarang 2026-09-25T00:30+07:00` (atau 07.30 dengan shift 08.00). Saran: lewati bila `hari_ini` dan jam < jadwal masuk paling awal. |
| R3 | Rendah | `laporan.py:667`; `SKILL.md:133` | Pesan "Kasir & absensi mencatat jam komputer" tidak akurat untuk kasir-lokal 1.1.1, yang mencatat menurut **zona toko** (`kasir.py:373-378`). Laporan juga tidak membaca zona toko dari kasir: toko WITA dengan `--tz` default WIB tidak diberi peringatan (hanya dijelaskan di referensi). |
| R4 | Rendah | `laporan.py:295-296` (pesan alat diteruskan apa adanya) | DB absensi 0 byte/rusak: pesan menyebut path **salinan sementara** yang sudah dihapus (`/tmp/laporan-usaha-…/absensi.db`), bukan file asli. Repro: `: > data/absensi/absensi.db` → jalankan laporan. Saran: ganti path snapshot dengan `a["data"]`. |
| R5 | Rendah | `SKILL.md` Langkah C / `references/openclaw-jadwal.md` §0 | Tidak ada panduan untuk penerima kedua yang sah (pemilik bersama / pengelola). Agent bisa menolak atau mengizinkan secara tidak konsisten. |
| K1 | Kosmetik | `laporan.py:682`, `:773` | "Retur 1 \| void 1 (-Rp 30.000)" tanda minus ganda; per metode bayar termasuk pajak (jumlah 381.040) tanpa label, padahal omzet tanpa pajak (346.400). `--tz` menerima zona non-Indonesia (Asia/Tokyo). `--samarkan` bisa bentrok bila dua nama berawalan sama. |

Tidak ada cacat tinggi. Tidak ada angka salah, tidak ada penulisan ke data asli, tidak ada kebocoran data pelanggan.

## Skor kualitas: **8 / 10**
Alasan:
- (+) Angka 100% cocok dengan hitung ulang independen di 3 skenario normal, termasuk PBJT, void/retur, diskon, minggu berjalan, dan sumber buku-stok. Rumus % tertulis dan terbukti di 20 ribu kasus.
- (+) Aman: hanya baca (hash sama), tahan DB terkunci/rusak/hilang, tidak menggantung, tanpa nama pelanggan, `--samarkan` bekerja, tengah malam WIB benar.
- (+) A/B jelas lebih baik; tidak ada pesaing publik yang setara; lolos uji muat OpenClaw 2026.9.6.
- (+) Jadwal "Pilihan 1" tanpa AI menghilangkan risiko agent mengubah angka.
- (−) S1: pemeriksaan utama "stok belum terpotong" bisa memberi rasa aman palsu saat impor sebagian.
- (−) R1/R2: sinyal kehadiran di laporan harian kurang tepat waktu (tidak muncul setelah jam pulang, alarm palsu sebelum jam masuk).
- (−) Bergantung pada 4 alat lain di folder yang sama; bila hanya satu alat, nilainya turun (jujur dijelaskan di README).

**Keputusan: LULUS (≥ 7)**, boleh naik ke status `lulus`. Disarankan memperbaiki S1 (dan idealnya R1/R2/R4) sebelum `beta`, lalu uji ulang skenario 04-G oleh penguji independen.

---

## Uji ulang v1.0.1 (2026-09-24)

- **Penguji:** agent penguji independen (simulasi, Claude Code), bukan pembuat maupun yang merevisi. Rincian reproduksi: `06-uji-ulang-v1.0.1.md`.
- **Lingkungan:** salinan skill + 4 alat di scratchpad, HOME palsu, `KOMUNITECH_DATA` sementara, `TZ=Asia/Jakarta`/`UTC`. Data dibuat ulang dengan script resmi alat (kafe 4 alat + toko hanya buku-stok) dan kasus tambahan di salinan. Data fiktif.
- **Otomatis:** `tests/uji_regresi.py` 39 tes OK; `scripts/validate.py` 53 skill valid; `scripts/uji_openclaw.sh` OpenClaw 2026.9.6 semua skill siap.

### Status klaim perbaikan
| ID | Klaim | Status | Bukti singkat |
|---|---|---|---|
| S1 | Cek impor per nomor nota sah | **Terbukti** | Nol 6/6, sebagian 5/6, penuh 0, void tidak dihitung, retur penuh konsisten; struktur tabel berubah (6 variasi) → dilewati tanpa crash |
| R1 | Tanpa keterangan masuk PERLU PERHATIAN | **Terbukti** | "Belum absen tanpa keterangan (1): Tari" (21.30), "Tidak absen & tanpa keterangan" (tanggal lampau), `--samarkan` → "T." |
| R2 | Sebelum jam masuk → "Belum waktunya absen" | **Terbukti sebagian** | Benar 00.30/07.30/07.59 bila belum ada yang tap; salah bila ada yang datang lebih awal (N1) |
| R3 | Pesan zona & peringatan zona toko | **Terbukti** | Toko WITA + `--tz` WIB → peringatan; `--tz Asia/Makassar` → hilang; pesan jam komputer hanya soal absensi |
| R4 | Path file asli di pesan error | **Terbukti** | absensi/kasir/stok 0 byte → path asli; 0 path salinan |
| R5 | Penerima tambahan | **Sebagian** | SKILL.md jelas; `references/openclaw-jadwal.md` §0 belum diselaraskan (N4) |
| K | Minus ganda, label pajak, `--tz` non-Indonesia | **Terbukti** | "(Rp 30.000)"; label "termasuk pajak/service"; Asia/Tokyo/UTC → exit 2 |

### Regresi
Skenario 01, 02 (+ minggu berjalan, jadwal Senin), 03 diulang: omzet, uang diterima, nota sah, rata-rata, persen, per metode, terlaris, stok & restock, kehadiran, tagihan → **0 beda** dengan hitung ulang independen. `persen()` vs `Fraction` 30.011 kasus → 0 beda. sha256 data asli sebelum = sesudah; DB terkunci selesai 1,3 detik; 0 nama/nomor pelanggan bocor; tengah malam WIB benar di komputer UTC. Satu regresi perilaku kecil: N1.

### Cacat tersisa
| ID | Keparahan | Ringkas | Reproduksi |
|---|---|---|---|
| N1 | Rendah | Alarm "Belum absen tanpa keterangan … catat izin/alpa" sebelum jam masuk bila satu karyawan sudah tap lebih awal (efek samping R1; `laporan.py:762-774`) | `absensi.py catat --karyawan Dimas --tanggal 2026-09-25 --masuk 07.45` → `laporan.py --sekarang 2026-09-25T07:50+07:00` |
| N2 | Rendah | Cek impor/selisih kas yang dilewati (struktur berubah) hanya dicatat di JSON `catatan`, tidak di teks Telegram | rename `pesanan.no_pesanan` di salinan stok.db → teks diam |
| N3 | Rendah | Nota di-void setelah diimpor (stok buku-stok belum dikembalikan) tidak diingatkan | `kasir.py void --nota N-260923-0002` setelah impor 23/9 → laporan tanpa butir |
| N4 | Rendah | `references/openclaw-jadwal.md:14-16` masih "`--to` selalu pemilik", "tidak ke karyawan"; tidak selaras dengan R5 | baca §0 vs SKILL.md Langkah C |
| N5 | Kosmetik | `--samarkan` → "T.. Tanyakan" | skenario 01 + `--samarkan` |
| N6 | Kosmetik (lama) | Void lintas hari: "Nota: 5 (+2 dibatalkan)" vs butir impor "6 dari 6 nota" di laporan yang sama | void N-260923-0002 pada 24/9 → laporan 24/9 |
| K1 | Kosmetik (diketahui) | `--samarkan` bentrok nama berawalan sama | — |

### Skor kualitas v1.0.1: **9 / 10**
Alasan:
- (+) Cacat sedang S1 hilang: impor sebagian kini terdeteksi dengan jumlah tepat, void dikecualikan, dan cek tahan perubahan struktur (tidak pernah crash).
- (+) R1–R4 dan perbaikan kosmetik terbukti; 39 tes regresi lulus; semua angka skenario 01–03 tetap 0 beda dengan hitung ulang independen; hanya-baca, privasi, DB terkunci, dan tengah malam WIB tetap benar.
- (−) N1: perbaikan R1 membuka alarm palsu baru pada laporan pagi (tidak memengaruhi jadwal 21.00).
- (−) N2–N4: cek yang dilewati tidak terlihat di teks; void setelah impor tidak diingatkan; referensi OpenClaw belum diselaraskan dengan aturan penerima.
- Tidak ada cacat tinggi/sedang; semua sisa berkeparahan rendah/kosmetik.

**Keputusan: LULUS (≥ 7).** Layak naik ke uji platform asli lalu `beta`. Disarankan memperbaiki N1 dan N4 (kecil, murah) sebelum dibagikan ke beta tester; N2/N3 boleh dijadwalkan di versi berikutnya.
