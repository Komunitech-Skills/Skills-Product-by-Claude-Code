# HASIL UJI — crm-wa v1.0.0

- **Tanggal:** 2026-09-24
- **Penguji:** agent penguji independen (simulasi, Claude Code), bukan pembuat skill. Hanya membaca folder `crm-wa/` (+ SKILL.md/script `pengingat-follow-up` dan `broadcast-wa` untuk uji jembatan).
- **Lingkungan:** Linux, Python 3.11. Skill disalin ke scratchpad (`<uji>/skill/`), DB lewat `--db` per skenario, `HOME` & `KOMUNITECH_DATA` palsu; tidak ada yang ditulis ke `~/KomunitechData`. Tanggal disimulasikan dengan opsi uji `--hari-ini`.
- **Data uji:** fiktif (nomor 0812/0813-0000-xxxx), dibuat sendiri lewat `crm.py` dan CSV buatan penguji.
- **Uji regresi bawaan:** `tests/uji_regresi.py` → 38 tes OK (dijalankan ulang; bukan dasar penilaian).
- **Uji muat OpenClaw:** `bash scripts/uji_openclaw.sh` → OpenClaw **2026.9.6**: `crm-wa` ada di `eligible`, `modelVisible`, `commandVisible` ✔. (Catatan untuk koordinator: skrip melaporkan 55/56 karena skill lain, `dolibarr-usaha`, tidak eligible.)
- **Uji jadwal OpenClaw (Gateway uji lokal 2026.9.6, `gateway run --dev --allow-unconfigured --bind loopback`, HOME sementara):**
  - `automations add` Pilihan 1 (follow-up harian 08.00, `--command-argv` path absolut, `--announce --channel telegram --to 123456789`) → **diterima**: `schedule {cron "0 8 * * *", tz Asia/Jakarta}`, `payload.kind command`, `nextRunAtMs` = 2026-09-25 01:00 UTC = **08.00 WIB** ✔.
  - Rekap mingguan (`30 7 * * 1`) dan Pilihan 2 (agent, `--session isolated --tools exec,read --message …`) → **diterima** ✔.
  - `automations run <id> --wait` → `command ok … exitCode 0`, `automations runs` memuat teks `FOLLOW-UP CRM - Kamis, 24 September 2026 (WIB)…` ✔; DB tidak berubah (sha256 sama).
  - `deliveryStatus: not-delivered` — "Telegram bot token missing" (diharapkan; tidak ada token). **Pengiriman ke Telegram tidak terverifikasi.** Perilaku agent Pilihan 2 tidak diuji (butuh API key model).
- **Platform teruji:** `claude-code (simulasi agent)`; `openclaw (uji muat otomatis + jadwal perintah di Gateway uji, tanpa Telegram)`.

## Audit keamanan singkat
Hanya library standar; impor jaringan satu-satunya `urllib.parse.quote` (untuk encode). Dijalankan di bawah *audit hook* Python di semua perintah baca/draf/rekap/samarkan: **0 peristiwa socket/subprocess/os.system**. SQL berparameter (nama kolom di `UPDATE` berasal dari kode, bukan input). Menulis hanya ke DB, `backup-crm/`, dan path `--csv` yang diberikan (menolak menimpa tanpa `--timpa`, menolak `.db`). Tidak membaca kredensial. Tidak ada prompt injection di SKILL.md/README/references. **Lulus.**

## Skenario
| No | Berkas | Isi | Hasil |
|---|---|---|---|
| 00 | `00-pembanding-tanpa-skill.md` | A/B skenario 01 | Skill **jelas lebih baik** (27/30 vs 10/30) |
| 00 | `00-banding-pesaing.md` | personal-crm (ClawHub), crm-automation, lead-gen-crm, pipeline-management | Tidak ada pesaing setara; terdekat 19/40 vs 35/40 |
| 01 | `01-toko-kue-15-prospek-dua-minggu.md` | 15 prospek IG/TikTok/referensi/walk-in, 10–24 Sep, terkirim, deal, batal, rekap, samarkan | **Lulus**; angka 100% cocok; S1, S2 |
| 02 | `02-jasa-renovasi-nilai-besar-dan-batal.md` | Nilai 37,5 jt–1,2 M, WITA, PT/CV, irama sampai pamit, deal→batal | **Lulus**; angka 100% cocok (3 periode); S1 parah (telat 38 hari) |
| 03 | `03-reseller-impor-csv-dan-follow-up-harian.md` | Impor Google Contacts baru/lama, ekspor kontak WA, 300 kontak, follow-up harian, ekspor & jembatan | **Lulus bersyarat**; S3, S4, S6, S7 |
| 04 | `04-input-buruk.md` | Nomor aneh, tanggal, nilai, nama ambigu, CSV rusak/formula, DB terkunci/rusak, restore | **Lulus bersyarat**; **T1**, S2, S5, R1, R2 |
| 05 | `05-di-luar-cakupan.md` | Blast promo, kirim otomatis ke pelanggan, laba rugi, scraping IG, kirim ke grup WA | **Lulus**; R6, R7 |

## Verifikasi angka independen
Query SQLite read-only sendiri (`verif.py`, tidak meng-import crm.py) dibandingkan dengan `rekap --json`:
| Diuji | Hasil |
|---|---|
| s01 bulan Sep: lead 15, deal 5 = Rp3.875.000, rata Rp775.000, closing 2,6 hr, batal 3, konversi 33,3%, win 62,5%, per sumber, sumber terbaik (seri nilai → konversi), posisi per tahap | **0 beda** |
| s01 minggu lalu 14–20 Sep | **0 beda** |
| s02 Agustus / September / semua waktu (termasuk deal→batal, rata Rp213.333.333, closing 12,3 hr) | **0 beda** |
| s03 minggu ini (impor + selesai + batal) | **0 beda** |
| "Nilai prospek yang perlu disapa" (Σ terlambat + hari ini) | cocok |
| 33 tautan wa.me di-decode: nomor = DB, `text` = draf persis, tanpa karakter mentah | **0 salah** |
| Nilai/harga & isi catatan di draf bawaan (kebutuhan tanpa harga) | **0 bocor** |
| `rekap --json`: nomor HP / nama kontak | **0 bocor** (lihat R-catatan alasan bebas) |
| `hari-ini --samarkan`, `daftar --samarkan`: nomor & tautan | **0 bocor**; nama → inisial |

## Temuan cacat (urut keparahan)
| ID | Keparahan | Lokasi | Temuan & reproduksi |
|---|---|---|---|
| **T1** | **Tinggi** | `scripts/crm.py:2170-2177` (`cmd_restore`) | **Pemulihan gagal justru saat DB rusak.** Header DB rusak (mis. sinkron Drive/Dropbox gagal) → semua perintah menyarankan `backup --daftar` + `restore`; `restore --dari <cadangan sehat> --ya` → "Database rusak (file is not a database)… Pulihkan dari cadangan: restore" (berputar). Penyebab: `sqlite3.backup()` ke file tujuan yang rusak. Restore berhasil hanya bila kerusakan di tengah file atau file 0 byte. Repro di `04-input-buruk.md`. Saran: salin mentah (sudah ada), lalu tulis cadangan ke file sementara dan `os.replace` ke path DB. |
| **S1** | Sedang | `crm.py:1343-1358` (`cmd_catat`) | Pindah ke **deal** tanpa `--followup` mempertahankan jadwal pra-deal (bahkan yang sudah lewat). s01: Pak Anton deal 12/9 → "follow-up 11 September"; s02: Bu Fitri deal 28/8 → 24/9 tampil "telat 38 hari" + draf menanyakan pembayaran; 5/10 "TERLAMBAT" di s01 adalah deal. "Nilai prospek yang perlu disapa" ikut menjumlah deal. Saran: saat masuk deal, set follow-up default (mis. +2 hari atau tanya tanggal kirim/ambil) dan beri label "order berjalan" terpisah dari prospek. |
| **S2** | Sedang | `crm.py:820-822` (`cari_kontak`) | Dua kontak bernama sama, satu **batal** → nama dipetakan **diam-diam** ke yang aktif. Pemilik: "Bu Sari yang kemarin batal ternyata jadi order 2 jt" → K0017 (aktif) dijadikan deal, K0018 tetap batal; rekap salah. Bertentangan dengan SKILL aturan 3 "Jangan menebak kontak". Saran: tetap kembalikan `pilihan` (boleh menandai yang aktif sebagai saran). |
| **S3** | Sedang | `crm.py:1021-1023` (alias kolom `wa`), `crm.py:1984` | Kolom **"Nomor"** (Indonesia) dan **"Number"** (ekspor kontak WA) tidak dikenali → pratinjau menampilkan kontak **tanpa nomor** ("-") dan hanya catatan kecil "Kolom diabaikan: Nomor"; bila disetujui, kontak masuk tanpa nomor (tanpa tautan, tanpa cek duplikat). Saran: tambah alias `nomor`, `number`, `no`, `no. telp`; bila tidak ada kolom nomor, beri peringatan tegas di baris pertama pratinjau. |
| **S4** | Sedang | `crm.py:453` (`normalisasi_wa`), `crm.py:560-566` (`norm_label`), `crm.py:1044-1057` | Impor **Google Contacts** (yang diklaim didukung, SKILL.md:96, README:79): nilai ganda "`a ::: b`" pada Phone ditolak "24 digit"; Labels "`* myContacts ::: Reseller`" jadi satu label → `daftar --label reseller` = 0; Phone 1 = nomor rumah & Phone 2 = HP → yang disimpan nomor rumah, HP diabaikan. Saran: pecah `:::`, buang `* myContacts`, pilih Phone berlabel Mobile/HP pertama. |
| **S5** | Sedang | `crm.py:894-936` (`susun_draf`); `references/perintah.md:65` | Klaim "Draf tidak pernah memuat nilai/harga dan catatan pribadi" tidak berlaku untuk kolom **kebutuhan**, yang masuk draf apa adanya: `--kebutuhan "kue ultah 450rb, suaminya pelit"` → "Soal kue ultah 450rb, suaminya pelit, boleh saya bantu…". SKILL tidak melarang agent menaruh harga/komentar di kebutuhan. Dimitigasi karena manusia memeriksa sebelum kirim. Saran: aturan tertulis "kebutuhan = nama produk saja" + script memperingatkan bila kebutuhan berisi angka rupiah. |
| **S6** | Sedang | `crm.py:2031/2051` (impor → FU hari ini), `crm.py:1638-1639` (blok TERLAMBAT/HARI INI tanpa batas) | Impor 300 kontak → semuanya dijadwalkan follow-up **hari ini**; `hari-ini` = 351 baris / 29 KB berisi 300 nama + nomor (samarkan+tanpa draf 22 KB). Tidak dapat dipakai sebagai pesan Telegram harian (dan menumpahkan data pribadi massal). Pratinjau impor tidak menyebut hal ini. Saran: impor default tanpa jadwal (atau disebar), batasi blok dengan "… dan N lainnya". |
| **S7** | Sedang | `crm.py:979,990` (`tulis_csv` tidak me-*resolve* path); `crm.py:2106-2108` (`perintah_pengingat` tanpa `--file`) | (a) `ekspor --csv kontak.csv` menulis ke **folder kerja saat itu** tanpa konfirmasi lokasi, dan pesan hanya "Ekspor 5 kontak ke kontak.csv" — **bukan path lengkap**; file berisi nomor HP bisa jatuh ke folder yang disinkron/di-commit. (b) Perintah jembatan `perintah_pengingat` tidak menyertakan `--file`, dan pengingat-follow-up memakai default `./pengingat/DAFTAR.csv` relatif folder kerja. **Kejadian nyata saat uji:** penguji menjalankan perintah jembatan dari root repo, sehingga `pengingat/DAFTAR.csv` (3 nama fiktif, tanggal, nominal) terbentuk di root repo `/home/user/Skills` (sudah dipindahkan koordinator; kelalaian cwd penguji, tetapi menunjukkan risikonya bagi agent pembeli). Saran: default ekspor ke folder data (`…/crm/ekspor/`), selalu cetak path absolut; `perintah_pengingat` sertakan `--file` ke lokasi data pengingat. |
| R1 | Rendah | `crm.py:1012` + `crm.py:2010` | Baris kosong di CSV dibuang sebelum penomoran → nomor baris sesudahnya salah (Bu Gina baris file 10 dilaporkan "baris 9"). |
| R2 | Rendah | `crm.py:2015` vs `crm.py:1165` | Impor hanya menolak nama yang seluruhnya angka; baris CSV berkutip rusak menjadi kontak "Bu Eka;0812-0000-4106;kue lapis" tanpa nomor (`tambah` akan menolak nama berisi nomor). |
| R3 | Rendah | `crm.py:1402-1452` | `terkirim` setelah pesan pamit tetap menambah `fu_ke` (4, 5, …) tanpa menolak; kontak itu menetap di "BELUM DIJADWALKAN". |
| R4 | Rendah | `crm.py:1908,1914` | `cek-duplikat --samarkan` hanya menyamarkan nomor; **nama lengkap** tetap tampil (teks & JSON `pilihan`). |
| R5 | Rendah | `crm.py:2168` | Nama salinan `crm-<detik>-sebelum-restore.db` tanpa penanganan tabrakan (dua restore di detik yang sama saling menimpa; terlihat saat uji dengan jam tetap). |
| R6 | Rendah | SKILL.md:22 ("Promo massal manual → broadcast-wa") | Jalur alternatif tidak mulus: `ekspor` crm-wa (kolom `no_wa`, tanpa kolom persetujuan/berhenti) langsung ditolak `siapkan_broadcast.py` ("Kolom nomor WA tidak ditemukan"). Tidak ada tempat baku untuk "setuju promo"/"minta berhenti" di CRM. |
| R7 | Rendah | `references/openclaw-jadwal.md:17`; SKILL.md "Kapan TIDAK" | Pemberitahuan privasi jadwal Telegram menyebut "nama, nomor, tautan" tetapi teks `hari-ini` juga memuat **catatan obrolan terakhir** dan **nilai rupiah**. Permintaan laba rugi tidak dirujuk ke skill keuangan (`laporan-keuangan-emkm`). Alasan batal bebas diteruskan ke `rekap --json` berlabel `data_sensitif: false`. |
| K1 | Kosmetik | `crm.py:490-498`, `508-517`, `1667` | Nomor rumah 021-0000-3005 tampil "0210-000-3005"; samaran "Bu R." untuk Bu Rina & Bu Ratna; teks contoh statis "Bu Rina deal 4,2 jt" ikut tercetak di mode samarkan; pesan impor file biner mencetak sampah biner; sapaan-awal untuk lead telat berhari-hari tidak mengandung "maaf baru membalas"; kontak lama hasil impor disapa "terima kasih sudah menghubungi". |

## Penilaian titik rawan yang diminta pembuat
- **Nama ambigu (dua "Bu Sari"):** ditangani baik bila keduanya aktif (ditolak + `pilihan`, "Sarinah" tidak ikut); **gagal** bila salah satu batal (S2).
- **Tebakan tanggal:** "besok", "Senin", "Senin depan", "25/9", "tgl 3", "minggu depan", "Kamis" (hari ini Kamis → minggu depan + catatan), "20/9" (lewat → ditolak), "31/9" (tidak ada) — semua benar dan disertai catatan asumsi.
- **Impor CSV Google Contacts & ekspor kontak WA:** format lama OK; format baru bermasalah (S4); ekspor kontak WA/daftar "Nomor" gagal membaca nomor (S3).
- **Privasi teks ke Telegram:** pantas untuk chat pribadi pemilik (bukan pelanggan/grup), tautan wa.me di Telegram justru berguna di HP; tetapi pemberitahuan kurang lengkap (R7) dan setelah impor besar isinya membengkak (S6). Saran: default jadwal `--samarkan` atau `--tanpa-draf` untuk usaha dengan banyak kontak, dan sebutkan catatan+nilai di pemberitahuan.
- **Nada draf:** sopan, tidak memaksa, bahasa natural (pilihan 1/2/3, pesan pamit). Kekurangan kecil di K1.

## Skor kualitas: **6 / 10 — REVISI (jangan rilis dulu)**
Alasan:
- (+) Inti harian sangat kuat: angka 100% cocok di 3 skenario dan 7 periode, rumus tertulis, tautan wa.me 33/33 benar, draf berjenjang sopan, tanpa jaringan, formula injection tertangani, DB terkunci/rusak tidak pernah ditimpa, pratinjau + `--ya` konsisten.
- (+) A/B jelas lebih baik (27 vs 10); tidak ada pesaing publik setara (35 vs 19); lolos uji muat OpenClaw dan jadwal Pilihan 1/2 diterima Gateway 2026.9.6.
- (−) **T1**: jalur pemulihan yang dijanjikan di SKILL.md/pesan error gagal pada jenis kerusakan paling umum — pembeli awam terjebak.
- (−) Impor (fitur yang dijual "tidak perlu ketik ulang") gagal pada kolom "Nomor"/"Number" (S3) dan format Google Contacts baru (S4), serta membanjiri daftar harian (S6).
- (−) S1 membuat daftar "TERLAMBAT" tercemar deal yang sudah menang — mengurangi kepercayaan pada fitur inti.
- Perkiraan setelah T1 + S1–S4 + S6 diperbaiki dan diuji ulang independen: **8/10**.

---

## Uji ulang v1.0.1 (2026-09-24)
- **Penguji:** agent penguji independen (bukan pembuat atau perevisi). Simulasi Claude Code. Semua perintah dijalankan dari scratchpad dengan DB, `HOME` dan `KOMUNITECH_DATA` palsu. Data fiktif. Detail & reproduksi: `06-uji-ulang-v1.0.1.md`.
- **Uji otomatis:** `tests/uji_regresi.py` 53 tes OK · `scripts/validate.py` lolos (57/57) · `scripts/uji_openclaw.sh` OpenClaw 2026.9.6 eligible/modelVisible/commandVisible 57/57.

### Status klaim
| Klaim | Status |
|---|---|
| T1 restore saat DB rusak | **Tuntas**: repro asli + 8 jenis kerusakan (0 byte, tengah, terpotong, acak, hot journal, journal sampah/asing) pulih. File rusak dipindah ke `rusak-crm-<waktu>.db`. DB aplikasi lain/terkunci tidak ditimpa. `init --mulai-baru` bekerja. Pesan error tidak lagi berputar. |
| S1 deal → konfirmasi order | **Tuntas**: deal selalu di ORDER BERJALAN (+2 hari), 0 deal di TERLAMBAT (24/9, 30/9, 5/10), nilai prospek tanpa deal. |
| S2 nama ambigu (termasuk batal) | **Tuntas** |
| S3/S4 impor Nomor/Number/No, Google Contacts | **Tuntas** (kolom nomor-urut tidak terpakai, ` ::: ` & label dipecah, HP diutamakan, tanpa nomor → `--ya` ditolak) |
| S5 draf hanya nama produk | **Sebagian**: kasus koma/kurung/" - "/Rp/harga beres. Titik & "sejuta" masih lolos (N1). |
| S6 impor tanpa jadwal, batas baris | **Tuntas**: `--sebar 25` tepat 25/hari. `hari-ini` 300 kontak: 12,5 KB (sebelumnya 29 KB), `--semua` lengkap. |
| S7 ekspor & jembatan | **Tuntas**: default `<data>/ekspor/`, path lengkap, peringatan repo git, `--file` di setiap perintah jembatan. |
| R1–R5, R7 | **Tuntas** |
| K1 | Sebagian (inisial sama, format telepon rumah) · R6 belum (sesuai pengakuan) |

### Regresi
Tidak ada. Tiga skenario baru mirip 01–03 (16 lead toko roti; renovasi WITA 37,5 jt–2,5 M; impor 300 reseller) dihitung ulang independen dari SQLite: **15 periode, 0 beda** (konversi, win rate, nilai per tahap, rata-rata, lama closing, sumber terbaik, terlambat/hari ini/besok/order). 128 tautan wa.me benar. 0 nilai/catatan di draf bawaan. `--samarkan` dan `rekap --json` tanpa nomor HP. 0 akses jaringan (audit hook). Definisi rekap setelah S1 konsisten dengan SKILL.md & `references/perintah.md` (pipeline terbuka tidak berubah, deal pindah ke `order_perlu_konfirmasi`, kunci JSON lama tetap).

### Cacat tersisa
| ID | Keparahan | Ringkas (reproduksi di `06-uji-ulang-v1.0.1.md` §4) |
|---|---|---|
| N1 | Rendah | `--kebutuhan "kue 450 ribu. orangnya pelit banget"` → draf "Soal kue . orangnya pelit banget". "sejuta" tidak dikenali. "1,5 juta" → "kue 1". Dimitigasi: aturan 5, peringatan `tambah`, manusia memeriksa. |
| N2 | Rendah | Kutip tak tertutup di CSV menelan baris berikutnya ("Pak Oman") tanpa disebut. |
| N3 | Rendah (lama) | Kontak impor tanpa `tgl masuk` dihitung "lead masuk" hari impor (s-C: 301 lead, konversi 0,0%) dan disapa "terima kasih sudah menghubungi". |
| K2 | Kosmetik | Deal berjadwal besok ikut blok/hitungan BESOK. Pesan "jadwal prospek lama diganti" pada kontak baru. |
| K1, R6 | Kosmetik / Rendah | Sisa yang sudah diakui pembuat. |

### Skor kualitas: **8 / 10 — LULUS** (siap uji platform asli, Tahap 6 langkah 10)
Alasan:
- (+) Cacat tinggi T1 tuntas dan tahan terhadap berbagai jenis kerusakan, termasuk journal tertinggal. Pemulihan tidak pernah menghapus atau menimpa data.
- (+) Semua cacat sedang (S1–S4, S6, S7) tuntas. Fitur inti harian kini bersih: deal tidak mencemari TERLAMBAT, dan impor dari WA/Google Contacts membaca nomor dengan benar.
- (+) Angka 100% cocok di 15 periode, dan tidak ada regresi.
- (−) S5 belum sepenuhnya: komentar setelah titik dan "sejuta" masih bisa masuk draf (N1). Risikonya rendah karena draf selalu diperiksa manusia.
- (−) Sisa cacat rendah pada impor (N2, N3) dan kosmetik. Tidak ada yang menghalangi rilis. Saran: perbaiki N1–N3 di v1.0.2.

---

## Uji ulang v1.0.2 (Akun B, 2026-09-25)
- **Penguji:** agent penguji independen lintas akun (Akun B), bukan pembuat/perevisi. Simulasi Claude Code.
  Dijalankan dari skill hasil salinan di scratchpad terpisah, `HOME`/`KOMUNITECH_DATA` palsu, data fiktif.
  Detail & reproduksi: `07-uji-ulang-v1.0.2.md`.
- **Uji otomatis:** `tests/uji_regresi.py` 57 tes OK · `scripts/validate.py --skill crm-wa` lolos (1 skill
  valid, 68 baris katalog sesuai).

### Status klaim perbaikan v1.0.2
| Klaim | Status |
|---|---|
| N1 titik/koma desimal & nominal kata di draf | **Tuntas**: 5 kasus baru (titik ribuan bertingkat, koma desimal 2 digit, "2.5jt", koma-komentar) benar; satuan non-uang ("2,5 kg") sengaja tidak terbuang |
| N2 kutip CSV tak tertutup → peringatan | **Tuntas**: kutip di baris pertama & di tengah file, keduanya memicu peringatan rentang baris yang benar sebelum `--ya`; tidak ada baris hilang diam-diam |
| N3 impor tanpa `tgl masuk` disebut di pratinjau | **Tuntas**: tanpa kolom sama sekali & kolom sebagian kosong, keduanya dihitung & disebut benar (1 dari 2 pada kasus sebagian) |
| K2 (sebagian) pesan "jadwal lama diganti" pada kontak baru | **Tuntas untuk kasus ini**: kontak baru langsung tahap deal (dengan/tanpa `--nilai`) tidak lagi menyebut "diganti"; kontak lama pindah tahap tetap menyebutnya (tanpa regresi) |

### Regresi
Tidak ada. Angka pipeline (jumlah & nilai per tahap) dihitung ulang independen dari kontak yang dibuat selama
sesi uji dan cocok 100% dengan `rekap --json` (5 "baru", 3 "deal" dengan total nilai Rp 5.000.000).

### Cacat tersisa (sudah diakui pembuat, tidak menghalangi rilis)
K2 sisa (deal berjadwal besok ikut blok BESOK), K1 (inisial ganda, format telepon rumah), R6 (jalur
broadcast-wa belum mulus).

### Skor kualitas: **9 / 10 — LULUS**
Perbaikan N1–N3 dan K2-sebagian di v1.0.2 diverifikasi tuntas dengan kasus uji baru (bukan sekadar mengulang
test milik pembuat), tanpa regresi pada 57 tes otomatis maupun angka pipeline. Sisa cacat kosmetik/rendah yang
sudah diketahui tidak menghalangi rilis.

## Verifikasi pengamanan (2026-09-29)
Penguji independen, crm-wa 1.0.3.
- `python3 tests/uji_regresi.py`: 61 tes OK.
- Folder kosong (HOME sementara), 20 subcommand dijalankan: `init` tanpa `--ya` hanya pratinjau (menampilkan path db), `init --mulai-baru` tanpa `--ya` idem; perintah lain (ubah/catat/tunda/terkirim/lihat/draf/atur/tambah/daftar/rekap/hari-ini/impor/restore/dst.) gagal "Database CRM belum ada" (rc 1) atau salah argumen (rc 2). **0 file/folder dibuat** di semua kasus. `init --ya` baru membuat `crm.db`.
- SKILL.md aturan 4 + Langkah A: tunjukkan path DB, tunggu "ya" di pesan berikutnya, dilarang pratinjau dan `--ya` dalam satu giliran.
**Verdict: LULUS** (perlindungan di script terbukti; kepatuhan agent atas gerbang "ya" perlu dikonfirmasi di uji OpenClaw nyata).


## Uji ulang OpenClaw v1.0.7 (2026-10-02) — "satu database = satu usaha"
Penguji independen, OpenClaw 2026.9.6 lokal (model router Komunitech claude-sonnet-5), SEBELUM vs SESUDAH; detail di 00-openclaw-sebelum-sesudah.md.
- Skenario 1 (pengguna baru Dapur Bu Ani di komputer yang sudah berisi database "Dapur Mama Tia"): SESUDAH berhenti sebelum mencatat, menawarkan database terpisah/ganti profil, patuh gerbang "ya"; database Tia terbukti tetap 3 kontak tanpa perubahan, draf atas nama Ani dengan wa.me benar (62...), tanggal benar. SEBELUM tidak mencampur (membuat CSV baru) tetapi tanpa normalisasi nomor/wa.me, tahap karangan, dan menawarkan kirim langsung. Skor 6 -> 9.
- Skenario 2 (promo otomatis ke semua kontak, ada kontak batal "jangan dihubungi"): SESUDAH menolak kirim otomatis dengan alasan benar + tawaran draf wa.me (belum menyebut kontak batal). SEBELUM membuka openclaw.json dan menawarkan sambung WA via QR tanpa peringatan risiko. Skor 4 -> 8.
- Rata-rata 5,0 -> 8,5. **VERDIK: LULUS.** Cacat minor: kecualikan kontak batal saat menyusun draf banyak kontak; tiga giliran sebelum tercatat.
