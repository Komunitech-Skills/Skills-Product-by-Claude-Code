---
name: surat-peringatan-karyawan
description: Menyusun Surat Peringatan karyawan (SP1, SP2, SP3) yang proporsional dan terdokumentasi, berisi fakta pelanggaran, dasar perjanjian kerja/peraturan perusahaan, masa berlaku 6 bulan yang dihitung script, harapan perbaikan, kolom tanda tangan, plus berita acara klarifikasi dan catatan proses. Gunakan saat pengguna minta buat SP, surat teguran, surat peringatan pertama/kedua/ketiga, menindak karyawan telat/bolos, atau employee warning letter, disciplinary letter. Bukan untuk surat PHK.
---

# Surat Peringatan Karyawan (SP1/SP2/SP3)

> **Aturan kerja:** Jangan menginstal paket/aplikasi (mis. `pip install`) — bila perlu, tunjukkan caranya dan biarkan pengguna yang memasang; jangan membuka atau mencari file selain yang diberikan pengguna, isi folder skill ini, dan file yang disebut di langkah kerja; jangan menulis file baru tanpa menyebut lokasinya, dan simpan hasil di folder kerja yang disepakati (bukan /tmp).

## Tujuan
Membantu pemilik usaha dan staf HR memberi sanksi yang **adil, proporsional, dan tercatat rapi**: tingkat SP tepat, fakta jelas (bukan emosi), dasar aturan disebut, masa berlaku benar, dan karyawan diberi kesempatan memperbaiki diri.

## Kapan digunakan
- Pengguna minta dibuatkan SP1, SP2, SP3, surat teguran tertulis, atau surat peringatan.
- Pengguna bertanya "karyawan saya sering telat / bolos / melanggar, harus SP berapa?".
- Pengguna ingin mengecek apakah SP sebelumnya masih berlaku sebelum memberi SP berikutnya.

## Kapan TIDAK digunakan
- **Surat PHK / pemecatan / pesangon** → jangan buat. Jelaskan singkat bahwa PHK punya prosedur dan hak pekerja yang wajib dipenuhi, lalu arahkan ke ahli hukum ketenagakerjaan atau Disnaker setempat.
- Dugaan tindak pidana (pencurian, penggelapan, kekerasan, pelecehan) → boleh bantu kronologi & berita acara, tapi sarankan konsultasi ahli hukum sebelum mengambil tindakan. **Jangan mengutip nomor pasal pidana (KUHP)** di surat maupun penjelasan, kecuali pengguna memintanya; cukup tulis "dugaan pencurian/penggelapan — konsultasikan ke ahli hukum/kepolisian". Bila diminta: KUHP baru (UU 1/2023) berlaku sejak **2 Januari 2026**; Pasal 374 KUHP lama tidak dipakai lagi (padanannya Pasal 488 UU 1/2023, penggelapan karena hubungan kerja) — tetap minta dicek ahli hukum.
- **Surat skorsing** hanya bila pengguna meminta, dan **wajib** memuat kalimat: "Selama masa skorsing, upah beserta hak lain yang biasa diterima tetap dibayar penuh." Jangan pernah menulis upah "ditentukan kemudian", dipotong, atau tidak dibayar (UU 13/2003 Pasal 157A ayat (2) s.t.d.d. UU 6/2023; Putusan MK 168/PUU-XXI/2023: kewajiban berjalan sampai proses perselisihan berkekuatan hukum tetap). Lihat `references/regulasi.md` bagian 3.
- Kontrak kerja → `perjanjian-sederhana`. Lowongan → `lowongan-kerja`. Surat resmi lain → `surat-resmi`. SOP → `sop-writer`.

## Input
| Info | Wajib? | Default jika tidak diberikan |
|---|---|---|
| Nama karyawan, jabatan/bagian | Ya | — (tanyakan; boleh pakai `[Nama]` bila pengguna ingin template) |
| Kronologi pelanggaran: apa, kapan, berapa kali, bukti | Ya | — (tanyakan) |
| Riwayat SP sebelumnya (jenis & tanggal terbit) | Ya | Dianggap belum pernah SP → SP1 (sebutkan asumsi) |
| Aturan yang dilanggar (pasal PK/PP/PKB atau tata tertib) | Tidak | `[Pasal ... Peraturan Perusahaan/Perjanjian Kerja]` + saran untuk mengisinya |
| Nama usaha, alamat, nama & jabatan penanda tangan | Tidak | `[isi]` |
| Tanggal terbit | Tidak | Hari ini |
| Masa berlaku | Tidak | 6 bulan (cek PK/PP/PKB perusahaan) |
| Sudah dipanggil & didengar penjelasannya? | Tidak | Dianggap belum → sertakan draf berita acara klarifikasi |

Jika info wajib kurang, tanyakan **sekali** (maks 5 pertanyaan bernomor). Jika pengguna ingin cepat, buat dengan placeholder dan sebutkan asumsinya.

## Langkah kerja

> **Lokasi script:** semua script skill ini ada di subfolder `scripts/` di folder yang sama dengan SKILL.md ini (folder skill). Jalankan dari sana; jangan mencari script atau file pengguna ke seluruh disk (mis. `find /`) — itu lambat dan menyentuh data pribadi di luar folder kerja.
1. **Susun fakta, bukan kesan.** Ubah keluhan ("dia malas") menjadi fakta terukur: tanggal, jam, jumlah kejadian, bukti (absensi fingerprint, CCTV, chat, laporan pelanggan, saksi). Jika tidak ada fakta terukur, minta dulu; jangan menulis tuduhan umum.
2. **Tentukan tingkat SP secara proporsional** dengan matriks di `references/proses-dan-proporsionalitas.md`:
   - Belum ada SP aktif → umumnya **SP1** (untuk pelanggaran ringan pertama kali, sarankan dulu teguran lisan tercatat).
   - Ada SP aktif dan terjadi pelanggaran baru → naik satu tingkat (SP1 → SP2 → SP3).
   - Langsung SP2/SP3 hanya jika **PK/PP/PKB perusahaan mengaturnya** untuk pelanggaran tertentu; jika pengguna tidak bisa menunjukkan aturannya, sarankan SP1 dan jelaskan risikonya.
   - Setelah SP3 masih melanggar → berhenti di sini: arahkan ke ahli hukum (masuk wilayah PHK).
3. **Cek masa berlaku SP sebelumnya dan hitung masa berlaku SP baru dengan script** (jangan dihitung kira-kira). Path relatif terhadap folder SKILL.md ini; Windows: ganti `python3` dengan `python` atau `py`:
   ```bash
   python3 <folder-skill-ini>/scripts/masa_berlaku.py --terbit "<tanggal SP baru>" --format teks
   python3 <folder-skill-ini>/scripts/masa_berlaku.py --terbit "<tanggal SP lama>" --cek "<tanggal pelanggaran baru PERTAMA>" --format teks
   ```
   Jika pelanggaran baru terjadi berulang kali, `--cek` memakai tanggal kejadian **pertama** setelah SP lama terbit. Jika sebagian kejadian terjadi setelah SP lama berakhir, jelaskan ke pengguna kejadian mana yang masuk masa berlaku dan mana yang tidak. SP yang sudah berakhir boleh disebut sebagai riwayat, tetapi tidak menjadi dasar menaikkan tingkat.
   Pakai `--bulan N` jika PK/PP/PKB menetapkan masa berlaku lain. Salin `kalimat_surat` dari output ke surat.
   **Fallback jika Python tidak bisa dijalankan:** tanggal berakhir = tanggal yang sama N bulan kemudian, dikurangi 1 hari (contoh: terbit 23 September 2026 → berakhir 22 Maret 2027). Jika tanggal itu tidak ada (mis. 31 Februari), pakai hari terakhir bulan tersebut. Beri tahu pengguna bahwa tanggal dihitung manual.
4. **Tulis surat** dengan format output di bawah: nada tegas tapi sopan, tanpa menghina, tanpa menyebut hal pribadi di luar pelanggaran.
5. **Tambahkan harapan perbaikan yang terukur** (mis. "hadir paling lambat pukul 08.00 setiap hari kerja") dan pembinaan yang ditawarkan (bila ada).
6. **Sertakan draf Berita Acara Klarifikasi** jika karyawan belum dipanggil, dan **Catatan Proses** untuk pengguna (bukan untuk dicetak).
7. Periksa checklist, lalu tambahkan disclaimer.

## Format output
```
[KOP: Nama Usaha — Alamat — Telepon]

SURAT PERINGATAN [PERTAMA/KEDUA/KETIGA] (SP-[1/2/3])
Nomor: [nomor]

Yang bertanda tangan di bawah ini, [nama], [jabatan] [nama usaha], memberikan Surat Peringatan [..] kepada:
Nama        : ...
Jabatan     : ...
Bagian      : ...

A. Pelanggaran
Berdasarkan [bukti], Saudara/Saudari telah [fakta pelanggaran + tanggal/jumlah].
[Jika SP2/SP3: Pelanggaran ini terjadi saat SP-[x] Nomor [..] tanggal [..] masih berlaku.]

B. Dasar
Perbuatan tersebut melanggar [Pasal .. Peraturan Perusahaan/Perjanjian Kerja/tata tertib].
Saudara/Saudari telah didengar penjelasannya pada [tanggal] (Berita Acara terlampir).

C. Harapan perbaikan
1. ...
[Konsekuensi: pelanggaran berikutnya selama masa berlaku dapat dikenai SP-[berikutnya] sesuai ketentuan perusahaan.]

D. Masa berlaku
[kalimat_surat dari script]

[Kota], [tanggal]
Pemberi peringatan,                     Diterima oleh,
[ttd]                                    [ttd]
[Nama, Jabatan]                          [Nama karyawan]
                                         Tanggal terima: ....
Saksi: [Nama, Jabatan] [ttd]
Tembusan: 1. Arsip personalia  2. ...

---
CATATAN PROSES (untuk pengguna, jangan dicetak)
DISCLAIMER
```
Template lengkap tiap tingkat + berita acara klarifikasi: `references/template-sp.md`.

## Contoh
**Input pengguna:** "Tolong buatin SP buat Rina, kasir di toko bangunan saya di Sidoarjo. Bulan ini telat 6 kali, lebih dari 30 menit, sudah ditegur lisan 2x. Belum pernah SP."

**Output (ringkas):**
```
SURAT PERINGATAN PERTAMA (SP-1)
Nomor: 001/SP-1/TB-MAJU/IX/2026
...
A. Pelanggaran
Berdasarkan rekap absensi mesin sidik jari periode 1–22 September 2026, Saudari tercatat
terlambat masuk kerja sebanyak 6 (enam) kali dengan keterlambatan lebih dari 30 menit,
yaitu pada tanggal 2, 5, 9, 12, 16, dan 19 September 2026. Saudari telah ditegur secara
lisan pada 9 dan 16 September 2026.

B. Dasar
Perbuatan tersebut melanggar [Pasal .. Peraturan Perusahaan tentang jam kerja]...

C. Harapan perbaikan
1. Hadir dan siap bekerja paling lambat pukul 08.00 WIB setiap hari kerja.
2. Jika berhalangan atau akan terlambat, memberi tahu atasan lewat WhatsApp sebelum pukul 07.30.

D. Masa berlaku
Surat Peringatan ini berlaku selama 6 (enam) bulan terhitung sejak tanggal 23 September 2026
sampai dengan 22 Maret 2027.
...
CATATAN PROSES: Panggil Rina dulu, dengar alasannya (mis. masalah transportasi/keluarga),
catat di berita acara, baru serahkan SP. Minta tanda tangan penerimaan; jika menolak,
tulis "menolak menandatangani" dan minta saksi tanda tangan.

Disclaimer: Draf ini bantuan administrasi, bukan nasihat hukum. Masa berlaku 6 bulan mengikuti
PP 35/2021 Pasal 52 (per 23 September 2026) kecuali PK/PP/PKB perusahaan mengatur lain.
Untuk PHK atau sengketa, konsultasikan ke ahli hukum ketenagakerjaan atau Disnaker setempat.
```

## Checklist sebelum mengirim hasil
- [ ] Tingkat SP sesuai riwayat & matriks proporsionalitas; alasan pemilihan tingkat dijelaskan ke pengguna.
- [ ] Fakta berisi tanggal/jumlah/bukti; tidak ada kata merendahkan ("malas", "bodoh") atau hal pribadi.
- [ ] Dasar aturan disebut, atau placeholder `[Pasal ...]` + saran untuk mengisinya.
- [ ] Tanggal berakhir berasal dari script (atau diberi label "dihitung manual").
- [ ] Ada harapan perbaikan yang terukur, kolom tanda tangan pemberi, penerima, saksi, dan tanggal terima.
- [ ] Catatan proses (panggil dulu, dengar penjelasan, dokumentasi) dan disclaimer ada.
- [ ] Tidak ada kalimat PHK/pemecatan otomatis ("jika mengulangi akan langsung dipecat").

## Batasan & penanganan error
- Jangan menulis ancaman PHK langsung. Tulis konsekuensi bertahap sesuai ketentuan perusahaan.
- Jika pengguna ingin langsung SP3/PHK untuk pelanggaran ringan pertama, jelaskan risiko (tidak proporsional, dapat digugat) dan sarankan SP1.
- Jika SP sebelumnya sudah berakhir (cek script), pelanggaran baru umumnya kembali ke SP1 kecuali PK/PP/PKB mengatur lain.
- Jika script error (format tanggal salah), baca pesan error, perbaiki input (mis. `23-09-2026`), jalankan ulang.
- Aturan ketenagakerjaan sedang dalam proses perubahan (RUU Pelindungan Ketenagakerjaan ditargetkan Oktober 2026). Dasar aturan, tanggal berlaku, dan hal yang perlu verifikasi ada di `references/regulasi.md`.
- Jangan menyimpan atau menyebarkan data karyawan di luar percakapan; SP bersifat rahasia (hanya karyawan, atasan, dan arsip personalia).
