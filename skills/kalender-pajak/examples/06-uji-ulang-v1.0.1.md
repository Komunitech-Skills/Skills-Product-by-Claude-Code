# 06 — Uji ulang v1.0.1 (penguji independen kedua)

- Tanggal: 2026-09-25 · Penguji: agent terpisah (bukan pembuat/perevisi), hanya membaca folder skill; kode `scripts/kalender_pajak.py` **tidak dibaca**.
- Lokasi: salinan di scratchpad (`uji2-kp/`), bukan `.claude/skills/`. Python 3 standar, Linux. Platform: `claude-code (simulasi agent)`.
- Tes bawaan: `python3 tests/uji_regresi.py` → **50 tes OK** (v1.0.0: 33).
- SKILL.md: **140 baris** (< 300) ✔. Disclaimer ada di SKILL.md, setiap output md/hari-ini, README ✔.

## 1. Verifikasi tanggal independen (ulang)
Metode: penghitung baru `verif2.py` ditulis dari tabel aturan SKILL.md + `references/aturan-tenggat.md`: setor tgl 15 (PPh final, 21, Unifikasi, 25), lapor tgl 20 (PPh 21, Unifikasi), PPN setor+lapor akhir bulan berikutnya, geser berulang lewat Sabtu/Minggu/libur/cuti bersama; **unggah faktur keluaran tgl 20 tanpa geser**; SPT OP 31 Mar, SPT badan 30 Apr, BPA1 31 Jan tanpa geser. Daftar libur diketik ulang dari hasil web search (SKB 2026: cuti 16 Feb, 18 Mar, 20/23/24 Mar, 15 Mei, 28 Mei, 24 Des; SKB 2027 15 Sep 2026: Isra Mikraj 5 Jan & 26 Des, Nyepi 8 Mar, Idulfitri 10–11 Mar + cuti 9/12/15 Mar, Waisak 20 Mei + cuti 19 Mei, Maulid 15 Agu, dst.) — cocok dengan CSV skill.

| Uji | Diharapkan | Script | Selisih |
|---|---|---|---|
| Semua kewajiban, Okt 2026 – Des 2027 (termasuk 15 acara unggah faktur) | 123 | 123 | **0** |
| Per profil (op-umkm 16, op-karyawan 1, op-pembukuan 16, badan-umkm 16, badan-umum 16, badan-pkp 46, pkp 30, pemberi-kerja 31, pemotong 30) = subset kewajiban yang benar | cocok | cocok | **0** |

Tanggal lama tidak berubah: lapor PPh 21/Unifikasi masa Feb 2026 **20→25 Mar 2026** ✔; setor masa Apr 2026 **15→18 Mei 2026** ✔; PPN masa Apr 2026 **31 Mei→2 Jun 2026** ✔; PPN masa Jan 2026 28 Feb→2 Mar ✔.

Unggah faktur tgl 20 (tidak digeser, diberi label): 6 kali jatuh di hari libur pada rentang uji — 20 Des 2026 (Min), 20 Feb 2027 (Sab), 20 Mar 2027 (Sab), **20 Mei 2027 (Waisak)**, 20 Jun 2027 (Min), 20 Nov 2027 (Sab); juga 20 Mar 2026 (cuti Idulfitri) & 20 Jun 2026 (Sab). Semua berlabel "jatuh pada hari libur (...) dan TIDAK bergeser - selesaikan hari kerja sebelumnya" ✔.

## 2. P2 — `--acara-pengingat` & klaim Google Calendar
Parser penguji (`icscheck2.py`, dengan unfolding) pada 15 bulan `badan-pkp,pemberi-kerja,pemotong`:
| Cek | Hasil |
|---|---|
| CRLF semua baris, CRLF akhir, baris ≤ 75 oktet, tidak memotong UTF-8 | ✔ |
| BEGIN/END seimbang; VCALENDAR punya VERSION:2.0 & PRODID | ✔ |
| 321 VEVENT = 107 tenggat (masing-masing 2 VALARM) + 214 acara pengingat (0 VALARM, `TRANSP:TRANSPARENT`) | ✔ |
| Semua VEVENT punya UID, DTSTAMP, DTSTART;VALUE=DATE, SUMMARY; DTEND = +1 hari; UID unik | ✔ |
| Tanggal acara pengingat = tenggat −3 dan −1 hari (214/214 benar, dicek dari tanggal di SUMMARY) | ✔ |
| Koma/titik koma di SUMMARY di-escape | ✔ |
| UID acara tenggat identik dengan file tanpa `--acara-pengingat`; file stabil antar-run (kecuali DTSTAMP) | ✔ |
| `--acara-pengingat` tanpa `--format ics` → ERROR kode 2 | ✔ |
Teks klaim (SKILL.md Langkah 4, README Manfaat & FAQ, openclaw-jadwal.md, catatan output script): kini **jujur** — "Google Calendar sering mengabaikan pengingat dari file impor", saran notifikasi default kalender / acara pengingat terpisah, impor ulang ke Google "bisa tetap membuat duplikat". ✔ Checklist SKILL.md memuat larangan menjanjikan pengingat/impor ulang pasti.
Kosmetik: saat `--acara-pengingat` sudah dipakai, catatan output masih menyarankan "buat ulang file dengan --acara-pengingat".

## 3. P3 — pemeriksaan
| Temuan lama | Status |
|---|---|
| Keterangan libur berkoma tanpa kutip terpotong | **Diperbaiki**: "Uji, dengan koma, dua" utuh; berkutip juga utuh |
| `--hari-ini` tanpa tenggat berikutnya | **Diperbaiki**: "Tenggat berikutnya sesudah rentang ini: ... (N hari lagi)" muncul, juga saat rentang kosong (`spt-op` per 25 Sep 2026 → 31 Mar 2027, 187 hari) |
| Label "Sabtu" menutupi hari raya | **Diperbaiki**: "21 Mar: Sabtu & Idulfitri 1447 H" |
| Cakupan kalender tahun X | **Diperbaiki**: baris "Cakupan: tenggat yang jatuh pada ..." + kalimat masa terakhir |
| Sumber data libur | **Diperbaiki**: baris "Data libur: SKB 3 Menteri ... (file: ...)" |
| Profil kewajiban tunggal (`ppn`) di tabel | **Diperbaiki** (SKILL.md baris 47) |

## 4. Data rusak baru
| Input | Hasil |
|---|---|
| Libur `2028-02-30` / `17/01/2028` | ERROR kode 2, tanpa traceback ✔ |
| Pemisah titik koma (`tanggal;jenis;...`) | ERROR "harus punya kolom 'tanggal'" ✔ |
| CSV ber-BOM UTF-8 (ekspor Excel) | diterima, geser benar ✔ |
| Tanggal dobel | diterima tanpa efek ganda ✔ |
| Kutip tak tertutup | diterima, keterangan utuh, tanggal benar ✔ |
| Jenis tak dikenal (`liburan`) | diterima diam-diam sebagai libur (aman; P3 kosmetik) |
| File libur hanya header (2028) | PERINGATAN 2028 tetap muncul ✔ |
| `--keluar` ke folder | ERROR kode 2 ✔ |
| `--hari-ini 2026-13-01`, `--rentang -5` | ERROR kode 2 ✔ |
| Profil `ppn,,PPN , pemberi-kerja`; `--bulan-mulai Okt` | ditoleransi ✔ |
| 24 bulan mulai Des 2027 | satu PERINGATAN "2028, 2029 belum ada" ✔ |

## 5. Klaim aturan (web search 2026-09-25)
| Klaim | Hasil penguji |
|---|---|
| Ps. 100 ayat 1 PMK 81/2024: setor yang jatuh pada hari libur → hari kerja berikutnya (merujuk Ps. 94); hari libur termasuk Sabtu, Minggu, libur nasional, libur pemilu, cuti bersama (Ps. 100 ayat 2) | **Terkonfirmasi** dari kutipan di hasil pencarian (diskusipajak, supriyantorekan, DDTC 1819436). Koreksi dari "Ps. 94 dst." tepat |
| Ps. 171: PPh 25 lapor tgl 20, setoran tervalidasi NTPN dianggap lapor | Isi terkonfirmasi (DJP sipp.menpan KPP Karanganyar: SPT Masa PPh 25 dianggap disampaikan sesuai tanggal validasi NTPN; DDTC untuk PHTB Ps. 171 ayat 3). Nomor ayat tetap belum ditemukan → label PERLU REVIEW **tepat** |
| SPT Tahunan tidak bergeser | Sumber sekunder (DDTC 1801611 dan ringkasan pencarian) menyatakan pergeseran hanya untuk SPT Masa. **Catatan baru:** kutipan Ps. 173 ayat 1 berbunyi "batas akhir pelaporan sebagaimana dimaksud dalam **Pasal 171 dan Pasal 172**" — bila Ps. 172 memuat batas SPT Tahunan, pembacaan harfiah bisa berarti SPT Tahunan ikut bergeser. Isi Ps. 172 belum terverifikasi. Skill sudah menyajikan kedua kemungkinan ke pengguna ("bila ternyata boleh bergeser, tanggal di kalender tetap aman karena lebih awal") — ketidakpastian **tidak disembunyikan**. Dalam rentang Okt 2026–Des 2027 tidak ada dampak: 31 Mar 2027 (Rabu) & 30 Apr 2027 (Jumat) hari kerja |
| Unggah faktur keluaran tgl 20 (PER-11/PJ/2025 Ps. 44 ayat 1) | **Terkonfirmasi** (Kring Pajak X status/1978014760097779873 & /1957661569468494169; Ortax; DDTC 1811029; beberapa konsultan). Tidak bergeser saat libur: beberapa sumber sekunder ("PER-11/PJ/2025 tidak memberikan kelonggaran untuk hari libur"; DDTC 1808811 "tak mundur meski Coretax terkendala") — tidak ada kutipan pasal; label PERLU REVIEW **tepat** dan pilihan "tidak digeser" adalah pilihan aman |

## 6. Skenario 02 diulang (SKILL.md v1.0.1)
**Pengguna:** "CV saya sudah PKP, ada karyawan, potong PPh 23. Pajak apa yang jatuh tempo 14 hari ke depan?" (hari ini Jumat, 25 Sep 2026)
**Asumsi:** badan tarif umum, PKP, pemberi kerja, pemotong → `--profil badan-pkp,pemberi-kerja,pemotong --hari-ini 2026-09-25`.
**Output script (disalin apa adanya):**
| Sisa | Tanggal | Kegiatan | Keterangan |
|---|---|---|---|
| 5 hari lagi | Rabu, 30 September 2026 | SETOR & LAPOR PPN masa Agu 2026 | - |

Tenggat berikutnya sesudah rentang ini: **Kamis, 15 Oktober 2026** (20 hari lagi) - SETOR PPh 21/26, SETOR PPh Unifikasi, SETOR PPh 25 masa Sep 2026.
**Tambahan agent (sesuai checklist PKP):** "Batas unggah faktur pajak keluaran bulan September: Selasa 20 Oktober 2026 (tidak mundur walau libur). Faktur Agustus seharusnya sudah diunggah paling lambat 20 September." + data libur + disclaimer.
Penilaian: tanggal benar (30 Sep Rabu, 15 Okt Kamis, 20 Okt Selasa), tidak menyebut besaran pajak, asumsi disebut ✔. Catatan: mode `--hari-ini` tidak menampilkan acara unggah berikutnya bila di luar rentang dan tidak memuat catatan PERLU REVIEW; agent bergantung pada butir checklist SKILL.md untuk menyebut tgl 20.

## 7. Temuan baru
| Prio | Temuan | Usulan |
|---|---|---|
| P3 | Unggah faktur di hari libur hanya berkata "selesaikan hari kerja sebelumnya" tanpa tanggalnya; untuk 20 Mei 2027 hari kerja sebelumnya adalah **Jumat 14 Mei 2027** (15–19 Mei libur/cuti) — mudah terlewat | Tampilkan tanggal hari kerja sebelumnya di keterangan |
| P3 | Ps. 173(1) merujuk "Pasal 171 dan Pasal 172"; perlu dicek isi Ps. 172 terhadap klaim "SPT Tahunan tidak bergeser" | Tambah catatan ini di `references/aturan-tenggat.md` #16 untuk pemilik/konsultan |
| P3 | File `--libur` buatan pengguna dilabeli "SKB 3 Menteri ... 2028" dan mematikan PERINGATAN 2028 walau hanya 1–2 tanggal | Label "file tambahan pengguna"; opsional peringatan bila jumlah tanggal sedikit |
| P3 | Catatan `.ics` menyarankan `--acara-pengingat` padahal opsi itu sudah dipakai; jenis libur tak dikenal diterima diam-diam | Kosmetik |
