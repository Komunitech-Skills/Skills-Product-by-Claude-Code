# HASIL UJI — kalender-pajak (penguji independen, Tahap 6)

- Tanggal uji: 2026-09-25 · Penguji: agent terpisah (bukan pembuat), hanya membaca folder skill · Lokasi uji: salinan di scratchpad, bukan `.claude/skills/`
- Lingkungan: Python 3 standar, Linux · Platform: `claude-code (simulasi agent)`
- Tes bawaan: `python3 tests/uji_regresi.py` → **33 tes OK**

## 1. Ringkasan skenario
| # | Skenario | Profil / perintah | Hasil |
|---|---|---|---|
| 01 | Warung OP UMKM 0,5% + 3 karyawan, Okt 2026–Mar 2027 + .ics | `op-umkm,pemberi-kerja`, 6 bulan, md + ics | LULUS — 20/20 tanggal benar, .ics valid |
| 02 | CV PKP (PPN, PPh 21, 23, 25): 14 hari ke depan per 25 Sep 2026 | `badan-pkp,pemberi-kerja,pemotong --hari-ini 2026-09-25` | LULUS (catatan P1) — PPN 30 Sep benar |
| 03 | PT PKP kalender 2027 + SPT Tahunan badan + checklist | `badan-pkp,pemberi-kerja,pemotong --tahun 2027` | LULUS (catatan P1) — 73/73 benar, SPT badan 30 Apr 2027 |
| 04 | "kapan bayar pajak?" | tanya sekali (4 butir) / default `op-umkm` | LULUS |
| 05 | Menunda setor tanpa denda + hitung PPN + kalender 2029 | tolak/rujuk + `--tahun 2029` dengan PERINGATAN | LULUS |
| A/B | Skenario 01 tanpa vs dengan skill | — | Dengan skill jelas lebih baik (20/20 vs 13/20 tanggal benar) |
| Pesaing | Kalender Pajakku/Ortax/Klikpajak/Metro TV 2026; tidak ada skill agent pesaing | — | Skill unggul untuk skenario 01; pesaing unggul di batas unggah faktur (PKP) |

## 2. Temuan berprioritas
| Prio | Temuan | Lokasi | Usulan perbaikan |
|---|---|---|---|
| **P1** | Profil PKP (`badan-pkp`, `pkp`, `ppn`) **tidak memuat batas unggah faktur pajak keluaran tgl 20 bulan berikutnya** (PER-11/PJ/2025 jo. PMK 81/2024 Ps. 387; dikonfirmasi Kring Pajak di X & DDTC/Ortax "Batas upload faktur pajak mundur jadi tanggal 20"). Terlambat unggah berisiko sanksi; kalender pesaing (Metro TV/Pajakku) mencantumkannya. Untuk skill yang menjual "semua tenggat", ini celah kelengkapan terbesar. | `scripts/kalender_pajak.py` (daftar kewajiban `ppn`), tabel aturan di `SKILL.md` & `references/aturan-tenggat.md`, `templates/checklist-bulanan.md` | Tambah kewajiban "UNGGAH faktur pajak keluaran masa X" tgl 20 bulan berikutnya untuk PPN. Status pergeseran hari libur untuk unggah faktur **belum jelas** (DDTC: "batas upload faktur pajak tak mundur meski Coretax terkendala") → tampilkan tanpa geser + label PERLU REVIEW, seperti BPA1. Tambah tes regresi. |
| P2 | Klaim "pengingat H-3 & H-1 ikut terpasang" saat impor ke Google Calendar kemungkinan besar tidak berlaku: Google Calendar sering mengabaikan VALARM pada impor .ics (terutama ke kalender non-utama; lihat thread Google Calendar Community). Juga klaim "impor ulang tidak membuat dobel ... acara diperbarui" belum diuji (tidak ada `SEQUENCE`). | `README.md` (Manfaat, FAQ), `SKILL.md` Langkah 4, `references/openclaw-jadwal.md` (Alternatif) | Ubah jadi "pengingat terpasang di Outlook/Apple Calendar; di Google Calendar atur notifikasi default kalender (mis. 3 hari & 1 hari sebelumnya)". Uji impor ulang nyata atau lunakkan klaim; pertimbangkan `SEQUENCE`/`LAST-MODIFIED`. |
| P3 | File `--libur` dengan keterangan berisi koma tanpa tanda kutip diterima diam-diam; keterangan terpotong ("Uji, dengan koma" → "Uji"). | parser CSV libur di script | Beri ERROR/peringatan bila baris punya >3 kolom, atau gabungkan sisa kolom ke keterangan. |
| P3 | Mode `--hari-ini`: bila rentang kosong/sedikit, tidak ada info tenggat berikutnya (agent harus inisiatif menjalankan ulang). | output mode hari-ini | Tambah baris "Tenggat berikutnya: <tanggal> <kegiatan>". |
| P3 | Label alasan geser memprioritaskan "Sabtu/Minggu" walau tanggal itu juga hari raya (21 Mar 2026 tertulis "Sabtu", bukan "Sabtu, Idulfitri"). Kosmetik. | fungsi alasan geser | Tampilkan keduanya. |
| P3 | "Kalender 2027" = tenggat yang **jatuh** di 2027 (masa Des 2026–Nov 2027); tenggat masa Des 2027 & SPT Tahunan 2027 (di 2028) tidak disebut. | output md | Tambah satu kalimat penjelasan cakupan. |
| P3 | Kalender 2026 menampilkan SPT Tahunan 2025 = 31 Mar/30 Apr 2026 tanpa menyebut KEP-55/PJ/2026 (sudah lewat, dampak kecil). | output md | Opsional: catatan khusus tahun pajak 2025. |
| P3 | `references/openclaw-jadwal.md` memakai `--profil ppn`, tidak tercantum di tabel pemetaan SKILL.md (tetap valid, ada di `--daftar-profil`). | SKILL.md tabel profil | Sebut "kewajiban tunggal juga boleh: ppn, pph21, ...". |

Tidak ditemukan bug perhitungan tanggal.

## 3. Verifikasi tanggal independen
Metode: penguji menulis penghitung sendiri (`verif.py`, di scratchpad; **tanpa membaca kode script**) dari aturan di SKILL.md: setor tgl 15 (PPh final, PPh 21, Unifikasi, PPh 25), lapor tgl 20 (PPh 21, Unifikasi), PPN akhir bulan berikutnya, geser berulang ke hari kerja (Sabtu, Minggu, libur, cuti bersama); SPT OP 31 Mar, SPT badan 30 Apr, BPA1 31 Jan tanpa geser. Daftar libur **diketik ulang sendiri** dari hasil pencarian SKB 3 Menteri (bukan dari CSV skill).

Data libur yang diverifikasi via web search:
- 2026 (17 libur + 8 cuti; SKB 19 Sep 2025): cuti 16 Feb, 18 Mar, 20/23/24 Mar, 15 Mei, 28 Mei, 24 Des — cocok dengan CSV skill. Sumber: setneg.go.id/baca/index/inilah_skb_3_menteri_libur_nasional_dan_cuti_bersama_2026 ; setneg Keppres 42/2025 ; kontan (Iduladha 27 Mei 2026).
- 2027 (18 libur + 8 cuti; SKB 15 Sep 2026): Isra Mikraj 5 Jan & 26 Des, cuti Imlek 5 Feb, Imlek 6 Feb, Nyepi 8 Mar, Idulfitri 10–11 Mar + cuti 9, 12, 15 Mar, cuti 25 Mar + Wafat 26 Mar, Kenaikan 6 Mei, Iduladha 17 Mei + cuti 18 Mei, cuti Waisak 19 Mei + Waisak 20 Mei, 1 Muharam 6 Jun, Maulid 15 Agu — cocok dengan CSV skill. Sumber: detik.com/jatim/berita/d-8667135 ; rri.co.id/nasional/2736371 ; cnnindonesia.com/edukasi/20260921093907-561-1406196 ; nu.or.id ; money.kompas.com/read/2026/09/25/123841826. (1 Jan, 1 Mei, 1 Jun, 17 Agu, 25 Des tetap; Paskah 28 Mar 2027 sesuai kalender gerejawi.) Catatan SKB: tanggal Idulfitri/Iduladha 2027 masih bisa diubah Keputusan Menag.

Hasil perbandingan (semua kewajiban sekaligus, `--format csv`):
| Rentang | Diharapkan | Script | Selisih |
|---|---|---|---|
| Okt 2026 – Des 2027 | 108 | 108 | **0** |
| Jan 2026 – Des 2028 (2028 hanya Sabtu/Minggu, sesuai aturan skill) | 250 (+10 butir Jan–Apr 2026 masa Des 2025/tahun pajak 2025 yang tidak dibangkitkan verifier) | 260 | **0** |

Cek khusus (semua cocok):
| Kasus | Hasil |
|---|---|
| Lapor SPT Masa PPh 21/Unifikasi masa Feb 2026: 20 Mar → 25 Mar 2026 (cuti 20, Sab-Min 21-22 Idulfitri, cuti 23-24) | 25 Mar ✔ (dikonfirmasi DDTC "Ada libur panjang, batas waktu pelaporan SPT Masa PPh dimundurkan") |
| Setor masa Apr 2026: 15 Mei (cuti Kenaikan) → 18 Mei 2026 | 18 Mei ✔ (DDTC) |
| PPN masa Apr 2026: 31 Mei (Minggu, Waisak) → 1 Jun (Pancasila) → 2 Jun 2026 | 2 Jun ✔ (DDTC "Ada tanggal merah, batas setor dan lapor PPN masa April mundur") |
| Desember → Januari: masa Des 2026 setor 15 Jan 2027 (Jumat), lapor 20 Jan; masa Des 2027 → 17 Jan 2028 (15 Sabtu) | ✔ |
| Feb non-kabisat: PPN masa Jan 2027: 28 Feb 2027 (Minggu) → 1 Mar | ✔ |
| Feb kabisat: PPN masa Jan 2028: 29 Feb 2028 (Selasa) | ✔ |
| Lebaran 2027: setor masa Feb 2027: 15 Mar (cuti) → 16 Mar | ✔ |
| Rantai Mei 2027: 15 Mei (Sab) → 16 Min → 17 Iduladha → 18/19 cuti → 20 Waisak → **21 Mei**; lapor 20 Mei → 21 Mei | ✔ |
| Natal–Tahun Baru: 24–26 Des 2026/2027 tidak mengenai tgl 15/20/akhir bulan; 31 Des 2026 (Kamis) & 31 Des 2027 (Jumat) tetap | ✔ |
| SPT Tahunan OP 31 Mar 2029 (Sabtu) tidak bergeser + peringatan | ✔ sesuai aturan skill |
| Rentang melewati tahun tanpa data (Des 2027 → Jan 2028; `--hari-ini 2027-12-25`) | PERINGATAN 2028 muncul ✔ |

## 4. Validasi .ics (parser penguji `icscheck.py`)
| Cek RFC 5545 | s01.ics (20 acara) | big.ics (174 acara, 24 bulan, 4 profil) |
|---|---|---|
| Semua baris CRLF, tanpa LF telanjang, CRLF di akhir | ✔ | ✔ |
| Panjang baris ≤ 75 oktet; lipatan tidak memotong karakter UTF-8 | ✔ | ✔ |
| BEGIN/END seimbang; VEVENT punya UID, DTSTAMP, DTSTART, DTEND, SUMMARY | ✔ | ✔ |
| UID unik; stabil antar-run & tetap sama saat tanggal bergeser (uji `--libur` tambahan) | ✔ | ✔ |
| `DTSTART;VALUE=DATE`, DTEND = +1 hari | ✔ | ✔ |
| 2 VALARM per acara: `-P2DT15H` (H-3 09.00), `-PT15H` (H-1 09.00) | ✔ | ✔ |
| Koma/titik koma di SUMMARY/DESCRIPTION/X-WR-CALNAME di-escape | ✔ | ✔ |
| `file` mengenali "iCalendar calendar file"; output stdout juga CRLF | ✔ | ✔ |
Catatan: tidak ada `SEQUENCE`/`VTIMEZONE` (acara seharian, tidak wajib). Lihat P2 soal perilaku Google Calendar.

## 5. Data rusak (detail di `05-di-luar-cakupan-2029.md`)
Profil tak dikenal/kosong, bulan 0/13, tahun 2024/"abc", `--hari-ini` 25-09-2026 & 2026-02-30, `--rentang` 0/91, `--jumlah-bulan` 25, format pdf, file libur (bulan 13, tanpa kolom tanggal, biner non-UTF-8, tidak ada), path keluaran tak bisa ditulis → semua `ERROR: ...` kode 2, tanpa traceback ✔. Profil berspasi/huruf besar/koma ganda ditoleransi ✔. File libur kosong untuk 2028 tetap memunculkan PERINGATAN ✔. Satu celah: koma tanpa kutip di keterangan (P3).

## 6. Pemeriksaan aturan (web search, 2026-09-25)
| Klaim skill | Status penguji | Sumber |
|---|---|---|
| Setor PPh tgl 15 bulan berikutnya (PMK 81/2024) | Terkonfirmasi | muc.co.id (DGT: tgl 15 seragam); Ortax jatuh-tempo PMK 81; KPMG TNF Jan 2025 |
| Lapor SPT Masa PPh 21/26 & Unifikasi tgl 20 | Terkonfirmasi | Kring Pajak X status/1970341259035492665 & /2089567954849730721 |
| PPN setor & lapor akhir bulan berikutnya | Terkonfirmasi | DDTC 1809652 & 1819761 |
| Pergeseran lapor SPT Masa ke hari kerja berikutnya (Ps. 173 ayat 1); hari libur termasuk cuti bersama | Terkonfirmasi | hasil pencarian mengutip Ps. 173(1); DDTC 1818124 |
| Pergeseran setor | Terkonfirmasi isinya; satu sumber menyebut **Ps. 100** PMK 81/2024 untuk pembayaran — skill menulis "Ps. 94 dst." (sudah PERLU REVIEW) | hasil pencarian diskusipajak/Kring Pajak |
| SPT Tahunan OP 31 Mar / badan akhir bulan ke-4; tidak bergeser saat libur | Tenggat terkonfirmasi; "tidak bergeser" berbasis penjelasan DJP era PMK 243/2014 & 2025 — wajar tetap PERLU REVIEW (sudah ditandai) | DDTC 1801611, 1809076 |
| PP 55/2022: setor tervalidasi = lapor | Konsisten dengan praktik & Ps. 171 PMK 81 (sumber sekunder) | DDTC kamus PPh final UMKM |
| PP 20/2026 (22 Apr 2026) mengubah PP 55/2022; CV/PT/Firma tidak lagi peserta baru 0,5%; OP & PT perorangan/koperasi tetap | Terkonfirmasi — pemetaan `badan-umkm` = PT perorangan/koperasi sudah sesuai | pajak.go.id/en/node/119950 ; IAPI ; Tax Center PKN STAN |
| PPh 25 dianggap lapor saat setor | Tidak menemukan kutipan pasal eksplisit; skill sudah menandai PERLU REVIEW (tepat) | — |
| Batas unggah faktur keluaran tgl 20 | **Tidak dimodelkan skill** → P1 | Kring Pajak X status/2079821664121229515 ; Ortax "batas-upload-fp-mundur-jadi-tanggal-20" ; DDTC 1811029 |

Disclaimer: ada di SKILL.md, README, setiap output script, dan setiap DESCRIPTION .ics; menyebut dasar aturan + tanggal cek + arahan ke konsultan/AR ✔. Rujukan skill hitung (`pph-final-umkm`, `pph21-ter`, `hitung-ppn`) konsisten di SKILL.md, catatan output, dan checklist ✔. Skill tidak menghitung/membulatkan pajak (standar pembulatan library tidak relevan; disebut di disclaimer) ✔.

## 7. Skor
**7 / 10 — LULUS (batas bawah).**
- Alasan naik: ketepatan tanggal sempurna (0 selisih dari 108 tenggat Okt 2026–Des 2027, semua kasus khusus benar), penanganan input rusak sangat baik, .ics valid RFC 5545, 33 tes regresi lulus, A/B jauh lebih baik, unggul atas kalender publik untuk personalisasi & 2027, butir tidak pasti ditandai PERLU REVIEW secara jujur.
- Alasan tertahan: untuk profil PKP satu kewajiban bulanan bersanksi (unggah faktur tgl 20) hilang padahal skill menjanjikan "semua tenggat" (P1); klaim pengingat Google Calendar kemungkinan berlebihan (P2).
- Rekomendasi: perbaiki P1 & P2 sebelum `uji` platform asli; setelah itu diperkirakan 8–9. Uji ulang oleh penguji independen setelah revisi (fokus profil PKP).

---

## Uji ulang v1.0.1 (penguji independen kedua, 2026-09-25)
Rincian: `06-uji-ulang-v1.0.1.md`. Penguji bukan pembuat/perevisi; kode script tidak dibaca; uji di salinan scratchpad.

| Temuan v1.0.0 | Status v1.0.1 |
|---|---|
| P1 unggah faktur keluaran tgl 20 | **Selesai** — acara "UNGGAH faktur..." untuk `ppn`/`pkp`/`badan-pkp`, tidak digeser + label hari libur, di SKILL.md/references/checklist/README; dasar PER-11/PJ/2025 Ps. 44(1) terkonfirmasi web search |
| P2 klaim Google Calendar & impor ulang | **Selesai** — klaim dilunakkan secara jujur; `--acara-pengingat` menghasilkan VEVENT H-3/H-1 terpisah yang valid RFC 5545 (321 VEVENT, 214/214 offset benar, UID stabil) |
| P3 (koma libur, tenggat berikutnya, label Sabtu & hari raya, cakupan, sumber data, profil tunggal, Ps. 100) | **Selesai** semua |

- Tes bawaan: **50 OK**. SKILL.md 140 baris; disclaimer ada.
- Verifikasi tanggal independen: **0 selisih** dari 123 tenggat Okt 2026–Des 2027 (semua kewajiban) dan 9 profil; tanggal lama tetap (25 Mar 2026, 18 Mei 2026, 2 Jun 2026).
- Data rusak baru (BOM, titik koma, tanggal mustahil, kutip tak tertutup, keluaran ke folder, dll.): tanpa traceback, ERROR kode 2 bila perlu.
- Klaim aturan: Ps. 100(1) terkonfirmasi; Ps. 171 PPh 25 & "SPT Tahunan/unggah faktur tidak bergeser" tetap PERLU REVIEW dan **dijelaskan ke pengguna**, bukan disembunyikan. Catatan baru: Ps. 173(1) merujuk Ps. 171 **dan 172** — perlu dicek pemilik/konsultan (tidak berdampak pada tanggal Okt 2026–Des 2027).
- Temuan baru: hanya P3 (tanggal hari kerja sebelum unggah faktur yang jatuh libur, mis. 20 Mei 2027 → praktis Jumat 14 Mei; label file libur pengguna; kosmetik catatan .ics).

### Skor uji ulang: **8 / 10 — LULUS**
- Naik dari 7: celah kelengkapan PKP (P1) tertutup dengan dasar aturan terkonfirmasi, klaim kalender kini jujur dan ada solusi teknis yang valid (P2), semua P3 diperbaiki, tes regresi bertambah 33→50, ketepatan tanggal tetap sempurna.
- Belum 9: seluruh verifikasi aturan masih dari sumber sekunder (naskah resmi PMK 81/2024 & PER-11/PJ/2025 belum dibaca langsung), tiga butir PERLU REVIEW (PPh 25 ayat, SPT Tahunan/Ps. 172, unggah faktur saat libur) belum diputus, dan beberapa P3 kecil.
- Rekomendasi: status boleh naik ke `lulus` lalu uji platform asli; P3 dapat dikerjakan di v1.0.2 tanpa uji ulang penuh.

---

## Uji ulang v1.0.2 (penguji independen ketiga, cek singkat, 2026-09-25)
Penguji bukan pembuat/perevisi/penguji sebelumnya; kode script tidak dibaca; dijalankan dari salinan scratchpad (`uji3-kp/`).

| Temuan P3 v1.0.1 | Status v1.0.2 |
|---|---|
| SPT Tahunan di hari libur vs Ps. 173 | **Selesai** — mis. SPT Badan 30 Apr 2028 (Minggu): tanggal kalender tetap, "selesaikan paling lambat Jumat 28 Apr 2028; kemungkinan lain (PERLU REVIEW) ... mundur ke Senin 1 Mei 2028 — pakai tanggal yang lebih awal". Jujur, tidak dinyatakan pasti. |
| Unggah faktur tgl 20 saat libur | **Selesai** — 20 Mei 2027 (Waisak) tetap tanggal batas resmi, label "TIDAK bergeser - selesaikan paling lambat hari kerja sebelumnya: Jumat, 14 Mei 2027" (benar: 15–16 akhir pekan, 17 Iduladha, 18–19 cuti). |
| Label file libur pengguna | **Selesai** — baris "Data libur: ...; data libur dari pengguna, belum diverifikasi (file: ...)" + PERINGATAN tahun 2028 tetap tampil; keterangan berkoma dalam kutip terbaca utuh. |

- **Ps. 172 PMK 81/2024 (web search sendiri):** hanya ditemukan kutipan Ps. 173(1) "…sebagaimana dimaksud dalam Pasal 171 dan Pasal 172 bertepatan dengan hari libur, pelaporan dapat dilakukan paling lambat pada hari kerja berikutnya" (ringkasan DDTC/Kring Pajak); isi Ps. 172 tidak ditemukan secara jelas (naskah BPK/JDIH tidak bisa dibuka). Tidak ada sumber tegas → tetap **PERLU REVIEW**; penanganan dua kemungkinan di skill sudah tepat.
- **Libur SKB 2027 diverifikasi ulang** (web search: SKB ditandatangani 15 Sep 2026, 18 libur + 8 cuti; CNN Indonesia, RRI, Kemenag, Setneg, detik): 26 tanggal di `libur-nasional-2027.csv` cocok semua.
- **Verifikasi tanggal independen** (penghitung sendiri, tanpa membaca kode, 9 profil, tenggat jatuh 1 Okt 2026–31 Des 2027): **202 tenggat, 0 selisih**. Tanggal lama tetap: 25 Mar 2026 (lapor PPh 21 masa Feb), 18 Mei 2026 (setor masa Apr), 2 Jun 2026 (PPN masa Apr).
- **.ics** (parser sendiri, CRLF dijaga): 46 VEVENT (badan-pkp) & 321 VEVENT (`--acara-pengingat`, 107 tenggat + 214 pengingat); BEGIN/END seimbang, tidak ada baris >75 oktet, UID unik, UID/DTSTAMP/DTSTART/SUMMARY lengkap, DTEND = +1 hari, 2 VALARM per tenggat, tanggal .ics = tanggal CSV, offset H-3/H-1 benar 214/214.
- **Tes regresi** `tests/uji_regresi.py`: **62 OK** (naik dari 50).
- **Bug baru:** tidak ada yang memengaruhi tanggal 2026–2027. Catatan kosmetik (P3): untuk tahun tanpa data resmi (2028), "kemungkinan lain" SPT Badan menyebut Senin 1 Mei 2028 padahal 1 Mei selalu Hari Buruh (seharusnya 2 Mei) — sudah tertutup PERINGATAN data libur; dengan `--libur` berisi 1 Mei hasilnya benar (Selasa 2 Mei).

### Skor uji ulang v1.0.2: **8 / 10 — LULUS**
Ketiga P3 selesai dengan penjelasan jujur, ketepatan tanggal tetap sempurna, tes bertambah. Belum 9 karena naskah resmi Ps. 172 PMK 81/2024 & PER-11/PJ/2025 belum dibaca langsung (tiga butir PERLU REVIEW masih menunggu pemilik/konsultan).

---

## Uji ulang v1.0.3 (penguji independen keempat, cek singkat, 2026-09-26)
Penguji bukan pembuat/perevisi/penguji sebelumnya; kode script tidak dibaca sebelum uji; dijalankan dari salinan scratchpad (`uji4-kp/`).

- **Verifikasi naskah resmi PMK 81/2024 (Ps. 169/171/172/173):** dicoba WebFetch ke `pajak.go.id` — **diblokir egress proxy** sesi ini (`EGRESS_BLOCKED`), sehingga tidak bisa membaca naskah langsung secara independen. Tinjauan dilakukan atas konsistensi internal `references/aturan-tenggat.md`: klaim "Ps. 173 ayat (1) hanya menggeser Ps. 171 & 172, tidak mencakup Ps. 169 (SPT Tahunan)" masuk akal dan sejalan dengan bukti sekunder yang sudah ada sejak v1.0.2 (DDTC: SPT Tahunan tak diundur meski libur/Lebaran) — tidak ada temuan yang bertentangan, tapi **status pembacaan naskah resmi tetap klaim sepihak dari sesi sebelumnya, belum diverifikasi ulang secara independen** di sesi ini.
- **Tahun dengan 31 Mar/30 Apr di akhir pekan (2029, 2030):** dijalankan `--profil op-karyawan`/`badan-pkp`. 2029: SPT OP 31 Mar (Sabtu) → satu tanggal `2029-03-31`, `libur_tidak_bergeser: Sabtu`, saran hari kerja sebelumnya Jumat 30 Mar 2029; tidak ada field `kemungkinan_tanggal_bergeser`. 2030: SPT OP 31 Mar (Minggu) → sama, saran Jumat 29 Mar 2030. SPT Badan 30 Apr jatuh Senin (2029)/Selasa (2030), tidak libur di kedua tahun itu — perilaku hari-kerja-biasa terverifikasi lewat kasus lain di uji_regresi.py. Benar sesuai klaim "satu tanggal, tanpa geser".
- **Tanggal lama tidak berubah (regresi manual):** dicek langsung dari output `--format json` profil bulanan 2026 — 20→**25 Mar 2026** (lapor PPh 21/unifikasi masa Feb), 15→**18 Mei 2026** (setor masa Apr), PPN 31 Mei→**2 Jun 2026** (masa Apr). Semua cocok, tidak berubah.
- **`tests/uji_regresi.py`:** **62/62 OK**, termasuk kasus baru `test_1_spt_op_hari_libur_satu_tanggal`, `test_1_tidak_ada_kemungkinan_geser_sama_sekali`, `test_1_spt_hari_kerja_tanpa_catatan`.
- **Bug baru:** tidak ditemukan. Grep memastikan tidak ada sisa field/istilah `kemungkinan_tanggal_bergeser` di kode maupun SKILL.md — penghapusan klaim Ps. 172/173 untuk SPT Tahunan bersih, tidak setengah jalan.

### Skor uji ulang v1.0.3: **8 / 10 — LULUS**
Perubahan konsisten, tes tambah 3 kasus baru dan semua lulus, tanggal lama tak berubah, tahun edge-case (2029/2030) benar. Tetap 8 (bukan 9): verifikasi naskah resmi PMK 81/2024 Ps. 169/171/172/173 **tidak bisa dilakukan ulang secara independen** sesi ini karena `pajak.go.id` diblokir egress proxy — klaim "dicocokkan dengan naskah resmi 2026-09-26" masih bertumpu pada sesi sebelumnya, belum ada verifikasi kedua yang benar-benar independen membaca naskah aslinya.
