# 06 — Uji ulang independen crm-wa v1.0.1 (2026-09-24)

- **Penguji:** agent penguji independen (simulasi, Claude Code). Bukan pembuat skill dan bukan yang merevisinya. Hanya membaca folder `crm-wa/`.
- **Lingkungan:** Linux, Python 3.11. Skill disalin ke scratchpad (`<uji>/skill/`). Semua perintah dijalankan dari `<uji>`, DB lewat `--db` per skenario, dan `HOME` serta `KOMUNITECH_DATA` palsu. Tanggal disimulasikan dengan `--hari-ini`.
- **Data:** fiktif semua (nomor 0811/0812/0813-0000-xxxx, "Reseller Fiktif 001–300", usaha fiktif).
- **Verifikasi angka:** `verif.py` buatan penguji membaca SQLite read-only dan menghitung ulang dengan rumus di SKILL.md, **tanpa meng-import crm.py**. Hasilnya dibandingkan dengan `rekap --json` / `hari-ini --json`.

## 1. Status klaim revisi
| Klaim | Reproduksi penguji | Status |
|---|---|---|
| **T1** restore saat DB rusak | Repro asli v1.0.0 (header ditimpa `b'X'*100` → `restore --dari <harian> --ya`) → **TERSIMPAN**, 2 kontak kembali, file rusak dipindah ke `backup-crm/rusak-crm-20260924-090000.db`. Diulang untuk 8 jenis kerusakan: file 0 byte, 8 KB sampah di tengah, file terpotong 1/3, 50 KB acak, hot journal asli, hot journal + header ditimpa, journal sampah + header ditimpa, journal milik DB lain + kerusakan tengah. **Semua pulih** (`info`: pemeriksaan ok). Journal lama ikut dipindah. DB sqlite milik aplikasi lain → restore **menolak** (tidak ditimpa). DB terkunci `BEGIN EXCLUSIVE` → "sedang dipakai…", tidak ditimpa. Cadangan yang rusak → ditolak dengan saran memilih cadangan lain. Tanpa DB → dipasang. `init` pada DB rusak → menunjuk restore/`--mulai-baru`. `init --mulai-baru` (pratinjau → `--ya`) → DB baru, file rusak dipindah dengan sha256 sama. `--mulai-baru` pada DB sehat → ditolak. Semua pesan error menunjuk langkah yang berhasil (tidak ada lagi saran yang berputar). | **Tuntas** |
| **S1** deal → konfirmasi order +2 | s-A: Rahma (FU prospek 5/9) deal 6/9 → 8/9; Bambang (FU 7/9 lewat) deal 8/9 → 10/9; s-B: Fitri deal 28/8 → 30/8; `--followup 26/9` dihormati; `tambah --tahap deal` → +2. `hari-ini` 24/9, 30/9, 5/10: deal **hanya** di "ORDER BERJALAN" ("sejak N hari lalu"), **0 deal di TERLAMBAT**. "Nilai prospek yang perlu disapa" = Σ prospek terbuka saja (Rp 7.520.000, cocok independen). `terkirim` pada deal → +2 hari, tidak pernah pamit. | **Tuntas** (lihat K2) |
| **S2** nama ambigu termasuk batal | Dua "Bu Sari" (satu batal) + "Sarinah": `catat/draf/terkirim --kontak "Bu Sari"`/`"sari"` → GAGAL `ambigu: true`, `pilihan` berisi kode, nama, `akhir_wa`, tahap (termasuk batal). Sarinah tidak ikut. Dengan kode → K0002 batal→deal + catatan "diaktifkan kembali". | **Tuntas** |
| **S3** kolom Nomor/Number/No | `Name,Number` (ekspor kontak WA, awalan `~` dibuang), `No;Nama;Nomor` (No = nomor urut → tidak dipakai, Nomor dipakai), `Nama;No` berisi HP → dipakai. `No;Nama;Produk` (hanya nomor urut) → PERHATIAN "kolom nomor WA tidak ditemukan". | **Tuntas** |
| **S4** Google Contacts | Baru: First/Last Name, `Labels "* myContacts ::: Reseller ::: VIP"` → label `reseller, vip` (`daftar --label reseller` = 2). Phone 1 Home + Phone 2 Mobile → yang dipakai HP, nomor rumah dicatat di riwayat. `a ::: b` dalam satu sel → HP pertama dipakai. Lama (Name, Group Membership, Phone N - Type) → OK. | **Tuntas** |
| **S3/S4** tanpa kolom nomor | Pratinjau diawali PERHATIAN, `--ya` → GAGAL kecuali `--tanpa-nomor`. | **Tuntas** |
| **S5** draf hanya nama produk | `"kue ultah 450rb, suaminya pelit"` → draf "Soal **kue ultah**". `"tumpeng 30 box harga Rp1.500.000 nego"` → "tumpeng 30 box". `"hampers (budget 2jt) - buat bos…"` → "hampers". Ada peringatan saat `tambah`. Catatan (`--catatan`) tidak masuk draf (0 bocor pada 128 draf). **Tetapi** titik dan "sejuta" tidak ditangani: lihat N1. | **Sebagian** |
| **S6** impor tanpa jadwal, batas baris | Impor 3–300 kontak: `followup` NULL, pratinjau menyebut "tanpa jadwal… ulangi dengan --sebar 10". `--sebar 25` → 25 per hari (21/9–2/10, dicek di SQLite). `hari-ini` 300 kontak: blok 20/20/10 + "... dan N lainnya", 10 draf, 12,5 KB (v1.0.0: 29 KB). `--samarkan --tanpa-draf` 5,5 KB. `--semua` → semua 137 baris. JSON `terpotong` benar. | **Tuntas** |
| **S7** ekspor & jembatan | `ekspor` → `<uji>/sC/ekspor/crm-lengkap-20260924-090000.csv` (path lengkap). `--ke hasil.csv` → path absolut disebut. Tujuan di repo git → "Catatan: Folder tujuan berada di dalam repositori git…". File sudah ada → ditolak tanpa `--timpa`. `.db` → ditolak. `--format pengingat`: setiap perintah membawa `--file <path lengkap>`, default `$KOMUNITECH_DATA/pengingat/DAFTAR.csv` (bukan folder kerja); `--file-pengingat` dihormati. | **Tuntas** |
| R1 nomor baris fisik | `rusak.csv` dengan baris `;;` dan baris kosong → baris bermasalah disebut "baris 6" = nomor baris fisik. | Tuntas |
| R2 nama berisi nomor | Kutip tak tertutup → "! baris 6: kolom nama berisi nomor telepon…" ditolak. | Tuntas (lihat N2) |
| R3 terkirim setelah pamit | Terkirim ke-5 → GAGAL "sudah dikirimi pesan pamit"; `hari-ini` → "SUDAH DIKIRIMI PESAN PAMIT: 1 kontak". | Tuntas |
| R4 cek-duplikat --samarkan | Teks & JSON: "Bu S.", nomor `0812-****-4017`, kebutuhan kosong. | Tuntas |
| R5 tabrakan nama restore | Dua restore di detik yang sama → `…-sebelum-restore.db` dan `…-sebelum-restore-2.db`. | Tuntas |
| R7 privasi/rujukan | `openclaw-jadwal.md` menyebut catatan & nilai rupiah. Laba rugi → `laporan-keuangan-emkm`. Alasan bebas → `data_sensitif: true`; `--samarkan` → "lainnya", `data_sensitif: false`. | Tuntas |
| K1 kosmetik | Sapaan-ulang untuk kontak masuk > 14 hari lalu ✔, "Mohon maaf baru sempat membalas" ✔, contoh balasan memakai kode ✔, file biner → pesan bersih ✔. Tersisa: inisial sama ("Bu R." untuk Ratna & Rina), telepon rumah `02100003005` tampil tanpa format / samaran `0210-****-3005`. | Sebagian (sesuai pengakuan) |
| R6 broadcast-wa | Tidak diubah (hanya dicatat di SKILL.md). | Belum (sesuai pengakuan) |

## 2. Uji regresi skenario 01–03 (data baru, dihitung ulang independen)
| Skenario | Isi | Hasil verif.py |
|---|---|---|
| s-A "Roti Bu Wati" (mirip 01) | 16 lead IG/TikTok/referensi/walk-in, 1–24 Sep, terkirim, nego, deal, lunas, batal (3 alasan), `--masuk 20/9`, `tambah --tahap deal`, 2 "Bu Sari" | 7 periode (bulan ini, minggu lalu, minggu ini, `--tanggal`, `--dari/--sampai`, semua, bulan lalu dari 5/10): **0 beda**. Contoh: lead 16, deal 6 = Rp4.775.000, rata Rp795.833, closing 5,2 hari, konversi 37,5%, win 66,7%, sumber terbaik Instagram (Rp2.600.000). Minggu lalu: Referensi, `sampel_kecil`. Kelompok follow-up (terlambat 6 / hari ini 1 / besok 1 / order 3) cocok. |
| s-B "CV Bangun Karya Fiktif" (mirip 02) | WITA, 37,5 jt–2,5 M, PT/Toko (sapaan "Bapak/Ibu di …"), telepon kantor, irama sampai pamit, deal→batal, deal→ditawar→deal (tgl deal diganti), `tambah --tahap selesai --masuk 1/9`, tawaran ulang +30 hari | 5 periode **0 beda** (mis. semua waktu: deal 3 = Rp3.680.000.000, rata Rp1.226.666.667, closing 23,3 hari, win 75,0%). |
| s-C "Grosir Fiktif" (mirip 03) | Impor 300 kontak `--sebar 25`, impor ulang (300 duplikat dilewati), `hari-ini`, ekspor, jembatan | Rekap & follow-up **0 beda** (terlambat 76, hari ini 25, besok 25, nilai Rp39.500.000). |

- **Tautan wa.me:** 128 draf di-decode (s-A 22, s-B 5, s-C 101). Nomor = DB, `text` = draf persis, tanpa karakter mentah: **0 salah**.
- **Privasi draf:** 0 nilai/Rp, 0 isi catatan di draf bawaan (dengan kebutuhan normal).
- **`--samarkan`** (`hari-ini`, `daftar`, `cek-duplikat`): 0 nomor utuh, 0 tautan, nama → inisial, tanpa catatan.
- **`rekap --json`:** 0 nomor HP, 0 nama kontak (dicek per string `wa` & nama dari DB, 15 keluaran).
- **Tanpa jaringan:** 15 perintah (baca, tulis, impor, ekspor, backup) di bawah audit hook Python → **0 peristiwa socket/subprocess/exec**. Hanya library standar (`urllib.parse.quote` untuk encode).
- **Konsistensi definisi rekap setelah S1:** posisi & pipeline terbuka (baru+dihubungi+ditawar) tidak berubah. `followup.terlambat/hari_ini` kini hanya prospek + tawaran ulang, deal di `order_perlu_konfirmasi`, dan `nilai_terlambat_dan_hari_ini` hanya prospek terbuka. Ini sesuai "Catatan v1.0.1" di `references/perintah.md` dan SKILL.md Langkah D. Kunci JSON lama tetap ada (`skema_json` 1). Inkonsistensi kecil: `besok` masih mencampur deal (K2).

## 3. Uji otomatis
- `python3 skills/crm-wa/tests/uji_regresi.py` → **53 tes OK** (v1.0.0: 38).
- `python3 scripts/validate.py` → "57 skill valid, 57 baris katalog sesuai".
- `bash scripts/uji_openclaw.sh` → OpenClaw 2026.9.6: eligible / modelVisible / commandVisible **57/57** (termasuk crm-wa).

## 4. Cacat tersisa / baru
| ID | Keparahan | Temuan & reproduksi |
|---|---|---|
| **N1** | Rendah | `hal_untuk_draf` tidak memotong di titik, tidak mengenali "sejuta", dan memotong di koma desimal sebelum membuang nominal. `tambah --kebutuhan "kue 450 ribu. orangnya pelit banget"` → draf "Soal **kue . orangnya pelit banget**, boleh saya bantu…". `"kue sejuta untuk mantan pacar"` → masuk utuh. `"kue 1,5 juta untuk ultah mertua yang cerewet"` → "kue 1". `"brownies 4.500.000 rupiah dp 50%…"` → "brownies rupiah". Dampaknya dimitigasi: aturan wajib 5 melarang isian seperti ini, peringatan `tambah` menampilkan teks yang akan dipakai, dan manusia memeriksa sebelum kirim. Saran: potong juga di `. `, tambahkan `sejuta/seratus ribu/rupiah/ribu`, buang nominal sebelum memotong di koma. |
| **N2** | Rendah | Kutip tak tertutup di CSV menelan baris-baris berikutnya tanpa disebut. `rusak.csv` berisi 5 baris data; baris 6 `"Bu Eka;…` ditolak, tetapi baris 7 "Pak Oman" ikut hilang ("3 baris data dibaca", tidak disebut). Saran: bila jumlah baris fisik ≠ baris terbaca, beri peringatan. |
| **N3** | Rendah (sudah ada sejak v1.0.0, tidak diklaim) | Kontak lama hasil impor tanpa kolom `tgl masuk` mendapat tanggal masuk = hari impor, sehingga dihitung sebagai "Lead masuk". s-C: lead masuk 301, konversi 0,0%. Rekap bulan itu jadi menyesatkan, dan pratinjau impor tidak menyebutnya. Kontak itu juga disapa "terima kasih sudah menghubungi" karena dianggap baru. Saran: opsi `--masuk-default` / peringatan di pratinjau. |
| K2 | Kosmetik | Deal dengan jadwal besok masuk blok & hitungan **BESOK** (`followup.besok`), sementara terlambat/hari ini dipisah. Pesan `tambah --tahap deal` berbunyi "jadwal prospek lama diganti" padahal kontak baru. |
| K1 | Kosmetik (sisa) | Inisial bisa sama ("Bu R."), telepon rumah tanpa format (`02100003005`, samaran `0210-****-3005`). Nomor kedua hasil impor tampil sebagai "Catatan terakhir" di `hari-ini`. |
| R6 | Rendah (sisa) | Jalur `broadcast-wa` belum mulus (tidak diubah). |

**Uji ulang v1.0.1 selesai, skor 8/10 (lulus), rincian di `HASIL-UJI.md`.**
