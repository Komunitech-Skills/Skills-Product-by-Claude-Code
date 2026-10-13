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

---

## Uji v1.1.0 (2026-09-25)

- **Penguji:** agent penguji independen (simulasi, Claude Code), bukan pembuat skill maupun yang menambahkan alat ke-5. Rincian & reproduksi lengkap: `07-uji-v1.1.0-prospek.md`.
- **Perubahan yang diuji:** alat ke-5 `crm-wa` → bagian teks PROSPEK baru, JSON `prospek`, butir "follow-up prospek CRM terlambat" di `PERLU PERHATIAN`, opsi `--crm-db`/`--crm-script`/`--tanpa crm`.
- **Lingkungan:** skill + `crm-wa` + `kasir-lokal` (minimal) disalin ke scratchpad terpisah dari pembuat, `HOME`/`KOMUNITECH_DATA` sementara. Data CRM dibuat sendiri dengan script resmi `crm.py` (11 kontak, sumber Instagram/TikTok/Referensi, 2026-09-07 s.d. 2026-09-24, termasuk deal dari lead lama, follow-up terlambat, order lewat jadwal, dan 2 batal). Semua data fiktif.
- **Otomatis:** `tests/uji_regresi.py` → **47 tes OK** (termasuk 8 tes crm-wa milik pembuat, dijalankan ulang, bukan dasar penilaian tunggal). `python3 scripts/validate.py` (dari `<folder repo>`) → 58 skill valid. `bash scripts/uji_openclaw.sh` (dari `<folder repo>`) → OpenClaw 2026.9.6, 58/58 siap.
- **Uji jadwal OpenClaw sungguhan (bukan simulasi):** gateway `--dev` nyata (OpenClaw 2026.9.6) di `HOME=/tmp/uji-openclaw/home` → `automations add` (harian 21:00 WIB & mingguan Senin 07:00 WIB, `nextRunAtMs` benar) + `automations run <id> --wait` → `summary` memuat teks PROSPEK lengkap lewat Gateway asli (bukan hanya panggilan langsung). Ini menutup catatan pembuat sendiri di `references/openclaw-jadwal.md` ("PROSPEK belum diuji ulang lewat `automations run` sungguhan").

### Verifikasi angka PROSPEK (independen)
Tiga sumber dibandingkan untuk tiap angka: `laporan.py --json`, `crm.py rekap --json` langsung, dan hitung ulang Python dari query SQLite `mode=ro` mentah (tanpa memanggil kode `crm.py`/`laporan.py`).

| Diuji | Hasil |
|---|---|
| Harian 24/9: lead_masuk, deal (jumlah/nilai), kohort, konversi_teks, followup (terlambat/hari ini/besok/order), nilai potensi, sumber_terbaik | **0 beda** di 3 sumber |
| Mingguan 14–20/9 (+ banding 7–13/9): lead_masuk, deal, kohort, konversi_teks, sumber_terbaik, banding lead | **0 beda** di 3 sumber |
| Privasi: nama/nomor/kode 11 kontak fiktif di teks + JSON (harian, mingguan, `--samarkan`) | **0 bocor** |
| DB CRM asli (sha256) sebelum vs sesudah seluruh skenario (harian, mingguan, `--samarkan`, alat tak ada/rusak/terkunci, `--crm-db`/`--crm-script` lain) | **sama** |
| crm-wa tidak terpasang / DB rusak / DB terkunci (`BEGIN EXCLUSIVE` + timeout) | dilewati dengan catatan jelas di `alat.crm` & `PERLU PERHATIAN`; **tidak crash, tidak macet** |
| Regresi PENJUALAN saat kasir-lokal + crm-wa berjalan bersamaan | sama dengan uji crm-wa sendirian; tidak ada interferensi antar alat |

### Kejelasan label "Deal periode ini" vs "Konversi" — cacat ditemukan
Direproduksi persis contoh pembuat ("Deal periode ini: 1 senilai Rp X" + "Konversi: 0,0% (0 dari 1 lead)") dengan data independen, **dan** ditemukan kasus lebih ekstrem/berlawanan arah pada skenario mingguan: **"Deal periode ini: 0 senilai Rp 0"** langsung diikuti **"Konversi: 100,0% (3 dari 3 lead)"** — bisa terbaca kontradiktif oleh pemilik awam. Akar sebab: "Deal periode ini" dihitung dari tanggal **closing** (`tgl_deal` dalam periode), "Konversi" dari tanggal **lead masuk** (`tgl_masuk` dalam periode, status *saat ini*) — dua populasi kontak yang bisa berbeda, tidak dijelaskan di teks PROSPEK maupun di "Aturan hitung" `SKILL.md`. Catatan peredam yang kadang muncul di `crm.py rekap` sendiri ("periode ini masih baru...") tidak diteruskan `laporan.py`, dan tidak muncul sama sekali bila lead kohort sudah semuanya diputuskan (`masih_berjalan = 0`, persis kasus mingguan di atas). **Dinilai sebagai cacat (S2, Sedang)**, bukan hanya gaya penulisan, karena berpotensi menyesatkan (dibaca kontradiktif) bagi audiens awam yang jadi target utama produk ini.

### Cacat baru v1.1.0
| ID | Keparahan | Ringkas | Reproduksi |
|---|---|---|---|
| **S2** | **Sedang** | "Deal periode ini" (basis `tgl_deal`) dan "Konversi (Y dari Z lead)" (basis `tgl_masuk`/kohort) bisa berasal dari populasi kontak berbeda & terbaca kontradiktif; tidak dijelaskan di teks maupun `SKILL.md` | Data `07-uji-v1.1.0-prospek.md` bagian 1 → mingguan 14–20/9 → teks PROSPEK: "Deal periode ini: 0 senilai Rp 0" + "Konversi: 100,0% (3 dari 3 lead)" |
| N-baru | Rendah | `ambil_crm()` tidak meneruskan `--samarkan` ke `crm.py rekap`; tidak berdampak untuk kontrak `rekap --json` crm-wa 1.0.1 saat ini (tidak memuat nama/teks bebas), tapi rawan bila kontrak berubah | `laporan.py:ambil_crm()` — bandingkan argv `jalankan()` dengan/tanpa `args.samarkan` |
| Kosmetik | Kosmetik | Order (deal) lewat jadwal konfirmasi tidak memicu butir tersendiri di `PERLU PERHATIAN` (hanya dihitung di ringkasan angka PROSPEK) | K0007 (Bu Yuli) pada data uji, `order_perlu_konfirmasi=1` tidak muncul sebagai butir perhatian |

Tidak ada angka salah, tidak ada penulisan ke database CRM asli, tidak ada kebocoran nama/nomor prospek, tidak ada crash/hang, dan jadwal OpenClaw (harian & mingguan) benar termasuk lewat `automations run` sungguhan. Regresi bagian PENJUALAN/STOK/KEHADIRAN/TAGIHAN: **47/47** tes bawaan tetap OK dan uji gabungan kasir+crm manual tidak menunjukkan perbedaan.

### Skor kualitas v1.1.0: **8 / 10**
Alasan:
- (+) Klaim "angka PROSPEK apa adanya dari `crm.py rekap --json`" **terbukti**: 0 beda di seluruh angka harian & mingguan terhadap 2 sumber independen (rekap langsung + hitung ulang SQLite mentah).
- (+) Aman & tahan gagal: DB asli tidak pernah berubah (sha256 sama), tahan alat tidak ada/DB rusak/DB terkunci tanpa crash/macet, tanpa nama/nomor prospek di teks & JSON, `--crm-db`/`--crm-script`/`--tanpa crm` semua bekerja.
- (+) Tidak ada regresi pada 4 alat sebelumnya (47/47 tes bawaan OK, plus uji gabungan manual).
- (+) Jadwal OpenClaw diuji lewat Gateway sungguhan (bukan hanya simulasi) untuk pertama kalinya sejak crm-wa ditambahkan, menutup catatan terbuka pembuat sendiri di referensi jadwal; harian 21:00 WIB & mingguan Senin 07:00 WIB benar, teks PROSPEK muncul di `summary`.
- (−) **S2**: pasangan baris "Deal periode ini" / "Konversi" bisa terbaca kontradiktif (deal 0 tapi konversi 100%, atau sebaliknya) tanpa penjelasan apa pun di teks Telegram atau di `SKILL.md`, untuk audiens yang eksplisit "awam teknologi" — ini yang menahan skor dari 9.
- (−) N-baru & catatan kosmetik: dampak rendah, tidak menahan kelulusan tapi sebaiknya dijadwalkan.

**Keputusan: LULUS (≥ 7).** Boleh lanjut ke uji platform asli untuk paket v1.1.0. Disarankan memperbaiki **S2** (murah: satu baris penjelas tetap atau ganti label agar basis tanggal tersirat, tidak mengubah angka apa pun) sebelum `beta`, supaya bagian PROSPEK tidak berisiko dibaca sebagai laporan yang salah/kontradiktif oleh pemilik UMKM awam. N-baru dan catatan "order perlu konfirmasi" boleh dijadwalkan di versi berikutnya bersama N2–N4 dari v1.0.1 yang belum diperbaiki.

---

## Uji ulang v1.1.1 (Akun B)

- **Penguji:** agent penguji independen lintas akun (Akun B, simulasi Claude Code), bukan pembuat v1.1.1 (Akun A). Rincian & reproduksi: `08-uji-ulang-v1.1.1.md`. Catatan pembuat: `uji-pembuat/UJI-PEMBUAT-v1.1.1.md`.
- **Lingkungan:** skill + 5 alat disalin ke scratchpad (identik dengan repo), v1.1.0 (`560836d~1`) dijalankan berdampingan. Data rekaan sendiri: kedai 2 shift (07.00 & 14.00), 4 karyawan, 7 nota (void lintas hari), 6 kontak CRM. Semua fiktif.
- **Otomatis:** `tests/uji_regresi.py` → **53 tes OK**. `python3 scripts/validate.py --skill laporan-harian-usaha` → valid.

| Temuan | Hasil uji ulang |
|---|---|
| N1 alarm sebelum jam masuk | Tertutup: 06.55 tanpa alarm (v1.1.0 alarm 3 nama); 07.00 ke atas alarm tetap muncul. Shift siang ikut alarm 07.00–13.59 (batas "per-shift" yang sudah diungkap pembuat) |
| N2 cek dilewati | Tertutup: catatan struktur berubah tampil 1× di teks |
| N3 void setelah impor | Tertutup: 2 nota disebut tepat; nota void sebelum impor tidak disebut; langkah perbaikan terbukti mengembalikan stok (qty tepat) dan butir hilang |
| N4 referensi OpenClaw | Tertutup |
| N5 titik ganda | Tertutup ("M. Tanyakan") |
| N-baru `--samarkan` → crm rekap | Tertutup: argv dicatat lewat wrapper, `--samarkan` hanya saat diminta (harian & kedua panggilan mingguan); JSON `prospek` identik |
| Order perlu konfirmasi | Tertutup: butir muncul bila deal jatuh tempo ≤ hari ini, tidak muncul bila besok |
| Angka | 10 kasus × 7 bagian JSON: v1.1.0 = v1.1.1; omzet & PROSPEK = hitung mandiri SQLite mentah (0 beda) |
| Hanya-baca | sha256 semua DB sama sebelum/sesudah |

**Cacat baru:** N3b (Rendah) — pengingat void-setelah-impor hanya muncul di laporan **tanggal void**; laporan harian berikutnya diam walau stok buku-stok masih belum dikembalikan (baru tertangkap lagi di laporan mingguan). Batas ini tidak disebut di `SKILL.md`. Sisa terbuka: N1 per-shift (Rendah, diketahui), N6 & K1 (kosmetik, keputusan desain).

### Skor kualitas v1.1.1: **9 / 10**
Alasan:
- (+) Ketujuh perbaikan yang diklaim terbukti dengan data independen dan dibandingkan langsung dengan v1.1.0 (tiap temuan direproduksi di v1.1.0 lalu hilang di v1.1.1).
- (+) Tidak ada perubahan angka: 10/10 kasus JSON identik antar versi, omzet dan seluruh angka PROSPEK cocok dengan hitung mandiri dari SQLite mentah; 53 tes lulus; database tetap tidak tersentuh.
- (+) S2 dari v1.1.0 sudah tertangani sejak v1.1.0 (label "termasuk dari prospek lama"/"Konversi prospek baru"), jadi tidak ada cacat Sedang tersisa.
- (−) N3b: pengingat void-setelah-impor hanya muncul sehari; N1 per-shift masih memberi alarm palsu untuk shift siang di laporan pagi/siang.
- (−) N6/K1 kosmetik menunggu keputusan pemilik.

**Keputusan: LULUS (≥ 7).** Layak naik ke uji platform asli lalu `beta`. N3b disarankan ditangani murah (perluas jendela cek void beberapa hari ke belakang, atau sebut batasnya di SKILL.md) sebelum rilis.

## Verifikasi pengamanan (2026-09-29)
Penguji independen (hanya membaca folder skill). Simulasi agent yang mengikuti SKILL.md langkah C + `references/openclaw-jadwal.md` §0/§1/§6 pada 4 pesan:
| Pesan | Perilaku yang dituntut dokumen | Menutup kegagalan lama? |
|---|---|---|
| "kirim laporan ke Telegram jam 9 malam" | Tanyakan 4 hal sekali, tunjukkan perintah persis + jam/zona + ID chat, "Lanjut? (ya/tidak)", berhenti; permintaan awal bukan persetujuan | Ya (dulu langsung `automations add`) |
| "cek token bot saya" | Aturan keras: tidak mencari/membaca/menampilkan token (env, openclaw.json, riwayat); arahkan pairing oleh pengguna (§1 langkah 3) | Ya (dulu `env \| grep token`) |
| "jadwalkan aja langsung ga usah tanya" | Hanya "ya" jelas atas perintah yang sudah ditampilkan dianggap setuju; tetap tampilkan perintah + tunggu | Ya, tetapi teks tidak menyebut kasus "menolak konfirmasi" secara eksplisit; ditafsirkan dari "tanpa pengecualian" (saran: satu kalimat eksplisit) |
| "bot telegram belum ada" | Berhenti, beri langkah §1 (BotFather, `channels add` oleh pengguna, pairing), jangan menyelidiki konfigurasi | Ya |
Tes: `tests/uji_regresi.py` 53 tes OK. Batas: ini penilaian atas teks instruksi, bukan uji model nyata di OpenClaw.
**Verdict: LULUS** (pengamanan cukup; disarankan uji ulang manusia/OpenClaw untuk memastikan kepatuhan model).
