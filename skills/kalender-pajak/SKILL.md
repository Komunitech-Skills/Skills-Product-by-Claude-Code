---
name: kalender-pajak
description: Menyusun kalender tenggat SETOR dan LAPOR pajak Indonesia per bulan/tahun sesuai profil wajib pajak (UMKM PPh final 0,5% PP 55, badan PKP/PPN + batas unggah faktur pajak keluaran, pemberi kerja PPh 21, pemotong PPh 23/4(2) unifikasi, PPh 25, SPT Tahunan) dengan pergeseran otomatis ke hari kerja bila jatuh di Sabtu/Minggu/libur nasional/cuti bersama (PMK 81/2024), plus checklist bulanan, "apa yang jatuh tempo 14 hari ke depan", file .ics untuk Google Calendar/Outlook, dan pengingat terjadwal OpenClaw ke Telegram. Gunakan saat pengguna tanya "kapan batas setor/lapor pajak", "jadwal pajak bulanan", "tenggat SPT", "pengingat pajak", tax calendar, tax deadline Indonesia, due date reminder. Bukan untuk menghitung besaran pajak (pakai pph-final-umkm, pph21-ter, hitung-ppn).
---

# Kalender Pajak (Tenggat Setor & Lapor)

> **Aturan kerja:** Jangan menginstal paket/aplikasi (mis. `pip install`) — bila perlu, tunjukkan caranya dan biarkan pengguna yang memasang; jangan membuka atau mencari file selain yang diberikan pengguna, isi folder skill ini, dan file yang disebut di langkah kerja; jangan menulis file baru tanpa menyebut lokasinya, dan simpan hasil di folder kerja yang disepakati (bukan /tmp).

## Tujuan
Memberi pemilik usaha, admin, dan orang pribadi **daftar tanggal pasti** kapan harus setor dan lapor pajak — sudah digeser bila jatuh di hari libur — dalam bentuk tabel, checklist bulanan, file kalender (.ics), atau pengingat otomatis. Skill ini hanya soal **jadwal**, bukan besaran pajak.

## Kapan digunakan
- "Kapan batas setor PPh 21 bulan ini?" / "Tanggal berapa lapor SPT Masa PPN?"
- "Buatkan jadwal pajak setahun untuk PT saya yang PKP dan punya 5 karyawan."
- "Apa saja pajak yang jatuh tempo 2 minggu ke depan?"
- "Bikinin file kalender pengingat pajak buat Google Calendar."
- "Ingatkan saya tiap bulan lewat Telegram."

## Kapan TIDAK digunakan
- Menghitung **berapa** pajaknya → `pph-final-umkm` (PPh 0,5%), `pph21-ter` (gaji), `hitung-ppn` (PPN) **bila skill itu terpasang** (cek daftar skill yang tersedia; bila tidak ada, katakan bahwa besaran pajak di luar cakupan skill ini, jangan mengarang angka). Skill ini boleh merujuk hasilnya.
- Membuat kode billing, mengisi SPT, atau login Coretax atas nama pengguna → jelaskan langkah umum saja; skill tidak mengakses Coretax.
- Sanksi/denda keterlambatan, pembetulan SPT, pemeriksaan, keberatan → arahkan ke konsultan pajak/AR.
- Pajak daerah (PBB, BPHTB, pajak restoran/hotel, pajak kendaraan) → di luar cakupan; tenggatnya diatur Perda masing-masing.
- Tahun buku badan yang tidak Januari–Desember → hanya bisa hitung manual (akhir bulan ke-4 setelah tahun buku berakhir); sebutkan keterbatasannya.

## Input
| Info | Wajib? | Default |
|---|---|---|
| Profil: orang pribadi/badan, UMKM 0,5% atau tarif umum, PKP atau bukan, punya karyawan, memotong PPh 23/4(2) | Ya | tanyakan; bila pengguna ingin cepat: `op-umkm` + sebut asumsi |
| Tahun & bulan mulai | Tidak | tahun berjalan, Januari (12 bulan) |
| Orang pribadi PPh 0,5%: omzet per bulan sejak Januari, atau perkiraan omzet setahun | Tidak | Tidak dihitung — bila pengguna menyebutnya, **wajib** dipakai (`--omzet-bulanan` / `--omzet-setahun`) |
| Format: tabel / checklist / .ics / CSV / pengingat OpenClaw | Tidak | tabel |

Info kurang → tanyakan **sekali** dalam satu pesan bernomor (maks. 4 pertanyaan), mis.: (1) orang pribadi atau badan (PT/CV/koperasi)? (2) pakai PPh final 0,5% atau pembukuan/tarif umum? (3) sudah PKP (memungut PPN)? (4) punya karyawan / membayar jasa atau sewa yang dipotong PPh 23/4(2)?

**Pemetaan profil** (boleh digabung dengan koma):
| Kondisi pengguna | Profil |
|---|---|
| Orang pribadi jualan/usaha, PPh 0,5% | `op-umkm` |
| Karyawan saja | `op-karyawan` |
| Orang pribadi usaha/pekerjaan bebas tarif umum | `op-pembukuan` |
| PT perorangan/koperasi PPh 0,5% | `badan-umkm` |
| Badan tarif umum, bukan PKP | `badan-umum` |
| Badan PKP | `badan-pkp` |
| Tambahan: sudah PKP (OP/badan UMKM) | `pkp` |
| Tambahan: punya karyawan | `pemberi-kerja` |
| Tambahan: memotong PPh 23/4(2)/15/22/26 | `pemotong` |

Kewajiban tunggal juga boleh dipakai langsung sebagai profil: `ppn`, `pph21`, `unifikasi`, `pph25`, `pph-final-umkm`, `spt-op`, `spt-badan`, `bukti-a1` (mis. `--profil ppn` untuk pengingat PPN saja).

## Langkah kerja
1. Tentukan profil dari cerita pengguna (tabel di atas). Sebut asumsi yang dipakai.
2. Jalankan script. Script ada di subfolder `scripts/` di folder yang sama dengan SKILL.md ini (folder skill); jalankan dari sana, jangan mencari ke seluruh disk (`find /`). Windows: `python` atau `py`:
   ```bash
   python3 <folder-skill-ini>/scripts/kalender_pajak.py --profil badan-pkp,pemberi-kerja --tahun 2026
   ```
   - Mulai bulan tertentu: `--bulan-mulai 10` (atau `Okt`), panjang `--jumlah-bulan 1-24` (default 12).
   - Yang jatuh tempo dekat: `--hari-ini 2026-09-25` (atau `--hari-ini hari-ini`), `--rentang 14` (default).
   - Checklist per bulan: `--format checklist`. Kalender: `--format ics --keluar kalender-pajak.ics` (tambah `--acara-pengingat` untuk pengguna Google Calendar). Juga `csv`, `json`.
   - **Orang pribadi PPh 0,5% yang menyebut omzet** ("omzet setahun kira-kira 600 juta", "Jan 48jt, Feb 45jt, …"): tambahkan `--omzet-setahun 600jt` (dianggap merata) atau `--omzet-bulanan "48jt;45jt;…"` (mulai Januari). Script menghitung bulan pertama omzet kumulatif **melewati** Rp500 juta, porsi omzet yang kena di bulan itu, dan tanggal setoran pertamanya. **Jangan menyimpulkan sendiri** kapan batas Rp500 juta terlewati — kutip blok "Kapan omzet kumulatif melewati Rp500 juta" apa adanya; bila omzet tidak diketahui, katakan belum bisa dipastikan dan tanyakan omzetnya.
   - Daftar profil: `--daftar-profil`. Libur tahun yang belum ada datanya: `--libur libur-2028.csv` (kolom `tanggal,jenis,keterangan`) — dilabeli "data libur dari pengguna" dan PERINGATAN tahun itu tetap tampil.
3. Salin tabel/checklist dari script **apa adanya** (jangan ubah tanggal). Tambahkan 1–2 kalimat sederhana, mis. "Setor PPh 21 masa Juli bergeser ke Selasa 18 Agustus karena 15–17 Agustus libur."
4. Untuk .ics: berikan file + cara impor (Google Calendar: Setelan → Impor & ekspor → Impor; Outlook: File → Buka → Impor). Sampaikan apa adanya (jangan janji lebih):
   - File memuat pengingat H-3 & H-1 pukul 09.00. **Apple Calendar & Outlook** biasanya memakainya; **Google Calendar sering mengabaikan pengingat dari file impor** dan memakai notifikasi default kalender. Untuk Google: sarankan atur notifikasi default kalender tujuan (mis. 3 hari & 1 hari sebelumnya), atau buat file dengan `--acara-pengingat` (menambah acara "Pengingat H-3/H-1" terpisah yang pasti terlihat di kalender).
   - Impor ulang: setiap acara punya UID tetap, sehingga Apple/Outlook umumnya memperbarui acara yang sama; **Google Calendar bisa tetap membuat duplikat**. Sarankan impor ke kalender khusus "Pajak" agar mudah dihapus lalu diimpor ulang.
5. Untuk pengingat OpenClaw: ikuti `references/openclaw-jadwal.md` (Telegram default; tunjukkan perintah dan minta "Lanjut? (ya/tidak)").
6. Selalu sertakan peringatan (bila ada) dan disclaimer dari output script — salin apa adanya ke balasan chat (tanggal, alasan geser, dasar aturan), jangan diringkas jadi "sesuai aturan terbaru".
   **Kode setor (KAP-KJS):** skill ini hanya memuat satu kode, yaitu deposit pajak **KAP 411618, KJS 100**. Kode lain (mis. untuk PPh final UMKM, PPh 21, PPN) **jangan disebut sama sekali** — katakan "pilih jenis pajak yang sesuai di menu Pembayaran Coretax; kode billing dibuat otomatis". Menyebut KAP dari ingatan berisiko salah (mis. 411125 adalah PPh 25/29 orang pribadi, bukan PPh final UMKM).
7. **Fallback tanpa Python:** susun manual dengan tabel aturan di bawah + daftar libur di `references/libur-nasional-2026.csv` / `-2027.csv`; beri tahu bahwa disusun manual dan periksa ulang tiap pergeseran.

## Aturan tenggat (PMK 81/2024, berlaku 1 Jan 2025; dicocokkan dengan naskah resmi 2026-09-26)
| Kewajiban | Setor paling lambat | Lapor paling lambat |
|---|---|---|
| PPh Final UMKM 0,5% (PP 55/2022 jo. PP 20/2026) | tgl 15 bulan berikutnya | dianggap lapor saat setoran tervalidasi |
| PPh 21/26 (pemberi kerja) | tgl 15 bulan berikutnya | tgl 20 bulan berikutnya (SPT Masa PPh 21/26) |
| PPh Unifikasi: 4(2), 15, 22, 23, 26 | tgl 15 bulan berikutnya | tgl 20 bulan berikutnya (SPT Masa PPh Unifikasi) |
| PPh 25 angsuran | tgl 15 bulan berikutnya | tgl 20, tetapi setoran tervalidasi (NTPN) dianggap sudah lapor pada tanggal setor (Ps. 171 ayat 10) → tidak dibuat acara lapor terpisah |
| PPN (PKP) | akhir bulan berikutnya **dan** sebelum SPT dikirim | akhir bulan berikutnya (walau nihil) |
| Faktur pajak keluaran (PKP) | — | **unggah & dapat persetujuan DJP paling lambat tgl 20** bulan berikutnya setelah tanggal pembuatan faktur (PER-11/PJ/2025 Ps. 44 ayat 1, berlaku 22 Mei 2025); tidak disetujui = bukan faktur pajak sah |
| SPT Tahunan OP | PPh 29 lunas sebelum SPT dikirim | 31 Maret (3 bulan setelah tahun pajak; Ps. 169 ayat 1) |
| SPT Tahunan Badan | PPh 29 lunas sebelum SPT dikirim | akhir bulan ke-4 (30 April bila tahun buku = kalender; Ps. 169 ayat 2) |
| Bukti potong BPA1 (1721-A1) ke karyawan | — | 1 bulan setelah masa pajak terakhir (31 Jan) |

**Pergeseran:** tenggat setor dan lapor **bulanan** yang jatuh pada Sabtu, Minggu, libur nasional, hari libur pemilu, atau **cuti bersama** bergeser ke **hari kerja berikutnya** — setor: PMK 81/2024 **Ps. 100 ayat 1** (merujuk tenggat Ps. 94); lapor SPT Masa: **Ps. 173 ayat 1** (hanya untuk pelaporan Ps. 171 & 172 — SPT Masa, serta PPN membangun sendiri/pemanfaatan dari luar Daerah Pabean oleh bukan-PKP). Geser berulang sampai ketemu hari kerja.
**Tidak digeser (ditampilkan di tanggal aslinya, label "TIDAK bergeser"):**
- **SPT Tahunan** — batasnya diatur **Ps. 169** dan **tidak bergeser meski hari libur** (Ps. 173 ayat 1 tidak mencakup Ps. 169; dicocokkan dengan naskah resmi). Tampilkan **satu tanggal** saja; bila jatuh di hari libur, keterangan script menyebut hari kerja sebelumnya + "tidak bergeser meski hari libur (PMK 81/2024 Ps. 169); lapor lebih awal". DJP biasanya tidak memundurkan tanggal, melainkan **menghapus sanksi** keterlambatan lewat keputusan khusus (mis. KEP-79/PJ/2025: s.d. 11 Apr 2025). KEP-55/PJ/2026 juga **bukan** perpanjangan — jatuh tempo SPT OP tahun pajak 2025 tetap 31 Mar 2026; yang dihapus hanya sanksi denda/bunga bila lapor/bayar s.d. 30 Apr 2026 (khusus orang pribadi); untuk badan TP 2025 berlaku KEP-71/PJ/2026 (jatuh tempo tetap, sanksi dihapus s.d. 1 bulan setelah jatuh tempo).
- **Unggah faktur pajak keluaran tgl 20** — tidak mundur walau libur/cuti bersama: PER-11/PJ/2025 tidak memuat ketentuan pergeseran (kesimpulan dari ketiadaan ketentuan → PERLU REVIEW). Bila tgl 20 hari libur, keterangan menyebut hari kerja sebelumnya sebagai saran (mis. 20 Mei 2027 Waisak → unggah paling aman **Jumat 14 Mei 2027**); tanggal batas resmi tetap tgl 20.
- **Bukti potong BPA1** (PERLU REVIEW).
Contoh terkonfirmasi: lapor SPT Masa PPh 21 masa Februari 2026: 20 Mar (cuti Idulfitri) → **25 Mar 2026**; setor PPh masa April 2026: 15 Mei (cuti bersama) → **18 Mei 2026**.
Rincian, sumber, dan status verifikasi: `references/aturan-tenggat.md`.

## Format output
```
## Kalender Pajak <rentang> - <profil>
Kewajiban: ...
Cakupan: tenggat yang JATUH pada <awal> s.d. <akhir> ... (masa terakhir & SPT tahun itu jatuh sesudahnya)
Data libur: SKB 3 Menteri <tahun> (file ...)[; data libur dari pengguna, belum diverifikasi (file ...)]
> PERINGATAN (bila data libur tahun itu belum ada)
| Tanggal | Kegiatan | Keterangan |          ← alasan bergeser (mis. "21 Mar: Sabtu & Idulfitri 1447 H") atau, untuk tenggat tidak bergeser di hari libur, "selesaikan paling lambat hari kerja sebelumnya: <tanggal>"
**Catatan per kewajiban** ...
**Aturan pergeseran** ...
_Disclaimer_
```
Mode `--hari-ini`: tabel `| Sisa | Tanggal | Kegiatan | Keterangan |` dengan "HARI INI", "besok", "N hari lagi", lalu baris "Tenggat berikutnya sesudah rentang ini: <tanggal> (N hari lagi) - <kegiatan>" (juga bila rentang kosong).
Sampaikan kalimat "Cakupan" ke pengguna bila ia minta "kalender tahun X" (tenggat masa Desember X dan SPT Tahunan tahun X jatuh di tahun berikutnya).

## Contoh
**Pengguna:** "Saya punya CV kecil, sudah PKP, karyawan 3 orang, sering bayar jasa yang dipotong PPh 23. Tolong jadwal pajak Oktober–Desember 2026."

**Perintah:** `python3 <folder-skill-ini>/scripts/kalender_pajak.py --profil badan-pkp,pemberi-kerja,pemotong --tahun 2026 --bulan-mulai 10 --jumlah-bulan 3`

**Output (dipersingkat):**
```
| Kamis, 15 Oktober 2026 | SETOR PPh 21/26 (pemberi kerja) masa Sep 2026 | - |
| Kamis, 15 Oktober 2026 | SETOR PPh Unifikasi (PPh 4(2), 15, 22, 23, 26 non-pegawai) masa Sep 2026 | - |
| Kamis, 15 Oktober 2026 | SETOR PPh 25 (angsuran bulanan) masa Sep 2026 | - |
| Selasa, 20 Oktober 2026 | LAPOR SPT Masa PPh 21/26 masa Sep 2026 | - |
| Selasa, 20 Oktober 2026 | LAPOR SPT Masa PPh Unifikasi masa Sep 2026 | - |
| Selasa, 20 Oktober 2026 | UNGGAH faktur pajak keluaran bulan Sep 2026 (batas persetujuan DJP) | - |
| Senin, 2 November 2026 | SETOR & LAPOR PPN masa Sep 2026 | bergeser dari 31 Okt (31 Okt: Sabtu; 1 Nov: Minggu) |
| Senin, 16 November 2026 | SETOR PPh 21/26 (pemberi kerja) masa Okt 2026 | bergeser dari 15 Nov (15 Nov: Minggu) |
```
Lalu jelaskan: "PPN masa September boleh disetor & dilapor sampai Senin 2 November karena 31 Oktober hari Sabtu — tapi lebih aman selesaikan Jumat 30 Oktober."
Contoh lengkap: `examples/uji-pembuat-01-cv-pkp-okt-des.md`.

## Checklist sebelum mengirim hasil
- [ ] Profil & asumsi disebut (OP/badan, 0,5%/tarif umum, PKP, karyawan, pemotong).
- [ ] Tanggal disalin dari script tanpa diubah; pergeseran dijelaskan.
- [ ] Peringatan "data libur belum ada" disampaikan bila muncul.
- [ ] Tidak menyebut besaran pajak; rujuk skill hitung terkait (bila terpasang) bila ditanya.
- [ ] Tidak ada KAP/KJS selain 411618-100 (deposit); kapan omzet melewati Rp500 juta hanya dari blok script (atau tidak disimpulkan).
- [ ] Profil PKP: batas unggah faktur pajak keluaran (tgl 20) ikut disebut.
- [ ] .ics: tidak menjanjikan pengingat pasti muncul di Google Calendar atau impor ulang pasti tanpa duplikat.
- [ ] Butir PERLU REVIEW (BPA1 tanpa geser, unggah faktur tidak bergeser) tidak dinyatakan sebagai kepastian mutlak.
- [ ] Disclaimer + dasar aturan + tanggal cek ada.

## Batasan & penanganan error
- **Kredensial & jadwal (wajib):** JANGAN pernah mencari, membaca, atau menampilkan token/API key/kredensial dari environment (`env`, `printenv`), file konfigurasi (mis. `openclaw.json`, `.env`), atau riwayat; kanal Telegram diatur lewat pairing/konfigurasi OpenClaw oleh pengguna sendiri. Buat jadwal hanya setelah pengguna membalas "ya" atas perintah + jam yang ditunjukkan; kanal belum siap atau perintah ditolak → berhenti dan beri langkah persiapannya, jangan menyelidiki sendiri.
- Script keluar kode 2 + `ERROR: ...` (tanpa traceback) untuk profil tidak dikenal, bulan di luar 1–12, tahun di luar 2025–2100, tanggal salah, format salah, file libur rusak. Jelaskan dengan bahasa sederhana dan tawarkan pilihan yang benar.
- Data libur tersedia **2026 dan 2027** (SKB 3 Menteri). Tahun lain → script tetap jalan tetapi hanya menggeser Sabtu/Minggu dan menampilkan PERINGATAN; minta pengguna cek SKB tahun itu. File `--libur` buatan pengguna dipakai untuk menggeser, tetapi tidak dianggap data resmi (PERINGATAN tetap muncul).
- File `--libur` boleh berisi keterangan berkoma (sebaiknya diberi tanda kutip; tanpa kutip pun digabung utuh).
- Libur daerah/cuti bersama tambahan yang diumumkan belakangan, atau **perpanjangan tenggat khusus dari DJP** atau keringanan sanksi (mis. KEP-55/PJ/2026: jatuh tempo SPT Tahunan OP 2025 tetap 31 Mar 2026, sanksi denda/bunga dihapus bila lapor/bayar s.d. 30 Apr 2026, khusus orang pribadi — hanya diberi catatan, tanggal tidak diubah) tidak otomatis masuk → minta pengguna cek pengumuman DJP.
- Tanggal yang ditampilkan adalah **batas terakhir**; sarankan setor/lapor 2–3 hari kerja sebelumnya karena Coretax dan bank bisa padat menjelang tenggat.
- Kode billing dibuat di Coretax (menu Pembayaran) atau lewat saldo **deposit pajak** (KAP 411618, KJS 100 — satu-satunya kode yang boleh disebut); skill tidak membuat kode billing.

_Bukan nasihat pajak. Dasar: PMK 81/2024, PP 55/2022 jo. PP 20/2026, PER-2/PJ/2024, PER-11/PJ/2025, SKB 3 Menteri libur 2026 & 2027; pasal tenggat dicocokkan dengan naskah resmi di pajak.go.id 2026-09-26, sebagian butir lain dari sumber sekunder. Skill ini tidak menghitung/membulatkan pajak; angka dari skill lain belum dicocokkan dengan Coretax. Cek pengumuman DJP terbaru dan konsultasikan dengan konsultan pajak atau AR._
