# Template draf pesan (bawaan skill)

Draf dibuat oleh `scripts/cek_jatuh_tempo.py` (fungsi `draf_pesan`). Halaman ini berguna saat Python tidak bisa
dijalankan, atau saat pemilik minta versi lain. Aturan tetap berlaku untuk semua draf:
- **Pemilik yang mengirim.** Bot tidak mengirim draf ke pelanggan.
- Kolom `catatan` bersifat pribadi dan **tidak pernah** dimasukkan ke draf. Yang boleh masuk hanya `nama`, `perihal`, nominal, dan tanggal.
- `{sapaan}` = nama di daftar. Jika nama berupa kode (ada angka, mis. `PLG-07`), pakai "Bapak/Ibu".
- `[rekening]` diisi pemilik sendiri (disarankan simpan di `USER.md`/memori agent, bukan di DAFTAR.csv).
- Tanpa ancaman, tanpa menyebut polisi/pidana, tanpa "disebar/viral", tanpa urgensi palsu.

## Piutang (nada bertahap, selaras skill `tagih-piutang`)
| Kapan | Nada | Draf |
|---|---|---|
| Sebelum jatuh tempo | Ramah | Selamat pagi {sapaan}, izin mengingatkan pembayaran {perihal} sebesar {nominal} yang jatuh tempo {besok/lusa/pada}, {tanggal} ("besok" hanya untuk H-1). Pembayaran bisa melalui [rekening]. Abaikan pesan ini jika sudah membayar. Terima kasih. |
| Hari H | Ramah | Selamat pagi {sapaan}, kami mengingatkan pembayaran {perihal} sebesar {nominal} jatuh tempo hari ini, {tanggal}. Jika sudah transfer, mohon kirimkan bukti transfernya agar bisa kami catat. Abaikan pesan ini jika sudah membayar. Terima kasih. |
| Lewat 1–6 hari | Asumsi baik | Selamat pagi {sapaan}, mohon maaf mengganggu. Menurut catatan kami, pembayaran {perihal} sebesar {nominal} yang jatuh tempo {tanggal} belum kami terima. Mungkin terlewat; jika sudah transfer, mohon kirimkan bukti transfernya. Jika belum, pembayaran bisa melalui [rekening]. Terima kasih. |
| Lewat 7–13 hari, atau 14–29 hari belum pernah diingatkan | Tegas-sopan | Selamat pagi {sapaan}. Kami menindaklanjuti pembayaran {perihal} sebesar {nominal} yang sudah lewat {N} hari dari jatuh tempo ({tanggal}). Mohon informasikan tanggal pasti pembayarannya, paling lambat {hari ini + 3}. Jika ada kendala, kami terbuka membicarakan jadwal pembayaran. Terima kasih. |
| Lewat 14–29 hari & sudah ≥ 1x diingatkan, atau ≥ 30 hari | Pemberitahuan tertulis | Yth. {sapaan}, bersama pesan ini kami sampaikan secara tertulis bahwa pembayaran {perihal} sebesar {nominal} yang jatuh tempo {tanggal} sudah lewat {N} hari dan belum kami terima. Mohon pembayaran diselesaikan paling lambat {hari ini + 7} melalui [rekening], atau hubungi kami sebelum tanggal tersebut bila ingin membahas jadwal cicilan secara tertulis. Terima kasih atas perhatiannya. |

Jumlah pengingat yang sudah dikirim diambil dari kolom `diingatkan` (naik lewat perintah `terkirim`).
Nada tertinggi di skill ini = "pemberitahuan tertulis". ≥ 30 hari dan ≥ 2x diingatkan → saran somasi lewat
`tagih-piutang`. Denda (hanya jika tertulis di kontrak) dan cicilan tertulis juga → `tagih-piutang`.

## Prospek (selaras skill `follow-up-prospek`)
Draf berubah sesuai kolom `diingatkan`:
- **0 (pertama), hari ini / H-1:** Halo {sapaan}, semoga harinya lancar. Saya ingin menindaklanjuti {perihal}. Apakah ada yang
  bisa saya bantu jelaskan lagi? Kalau belum jadi prioritas, cukup balas "nanti" saja, saya tidak akan mengganggu.
- **Terlambat:** Halo {sapaan}, mohon maaf baru menyapa lagi. Terkait {perihal}, apakah masih relevan untuk
  {sapaan} saat ini? Kalau ada yang ingin ditanyakan, saya siap bantu. Kalau belum jadi prioritas, cukup balas
  "nanti" saja, saya tidak akan mengganggu.
- **1x:** menawarkan info tambahan (harga, waktu, contoh hasil) + jalan keluar "nanti".
- **2x:** memudahkan keputusan (telepon 10 menit atau pilihan yang lebih sederhana) + jalan keluar "nanti".
- **≥ 3x:** pesan pamit yang sopan ("ini pesan terakhir saya ..."), lalu tandai `selesai`.
- Prospek menjawab "tidak"/"jangan hubungi lagi" → tandai `selesai`, jangan dijadwalkan ulang (UU PDP: berhenti bila diminta).

## Timesheet klien
Selamat sore {sapaan}, berikut rekap jam kerja {periode}: total {X jam Y menit} ({desimal} jam), nilai {Rp ...}.
Rincian:
- {tanggal}: {durasi} - {keterangan}

Mohon konfirmasinya sebelum kami terbitkan invoice. Terima kasih.

Angka **wajib** dari `timesheet --klien "<nama>"`. Draf di rekap harian sengaja memakai `[TOTAL JAM]`/`[NILAI]`
sampai angka itu dihitung.

## Janji
- **Sebelum/hari ini:** Halo {sapaan}, mengingatkan janji kita {hari ini/besok/lusa/pada}, {tanggal} untuk {perihal}.
  Apakah jadwalnya masih sesuai? Terima kasih.
- **Terlambat:** tanpa draf. Tanyakan ke pemilik apakah perlu ditandai selesai atau ditunda.

## Lainnya
Pengingat pribadi pemilik (mis. perpanjang izin usaha), tanpa draf ke orang lain.

## Contoh rekap lengkap (data fiktif `templates/DAFTAR.csv`, hari ini 2 Okt 2026)
```
PENGINGAT FOLLOW-UP - Jumat, 2 Oktober 2026

TERLAMBAT (1)
1. #2 Piutang - CV Contoh Maju | Rp 12.500.000 | INV-0788 | lewat 11 hari (jatuh tempo 21 Sep 2026) | sudah diingatkan 1x
   Catatan: bilang tunggu pencairan proyek

HARI INI (3)
1. #5 Janji - Bu Dewi | meeting jam 10.00 di kantor | hari ini
2. #3 Prospek - Pak Budi | penawaran paket katering kantor | hari ini
   Catatan: minta dihubungi setelah rapat direksi
3. #4 Timesheet - PT Kreatif Contoh | minggu ini | hari ini

BESOK / H-1 (1)
1. #1 Piutang - Bu Rina | Rp 4.500.000 | INV-012 seragam | besok, 3 Okt 2026
   Catatan: biasanya bayar akhir pekan

Total piutang tertunggak (terlambat + hari ini): Rp 12.500.000
Umur piutang terlambat: 1-30 hari: Rp 12.500.000 (1)
Piutang jatuh tempo besok: Rp 4.500.000
Menyusul 7 hari ke depan: #6 Perpanjang izin usaha (5 Okt 2026)

DRAF PESAN (cek dulu, lalu salin & kirim sendiri dari WA/email Anda)

#2 untuk CV Contoh Maju:
Selamat pagi CV Contoh Maju. Kami menindaklanjuti pembayaran INV-0788 sebesar Rp 12.500.000 yang sudah lewat 11 hari dari jatuh tempo (21 Sep 2026). Mohon informasikan tanggal pasti pembayarannya, paling lambat 5 Okt 2026. Jika ada kendala, kami terbuka membicarakan jadwal pembayaran. Terima kasih.
...
Balas misalnya: "selesai 3", "terkirim 3", "tunda 3 ke Senin", "hapus 3".
```
Catatan pribadi ("bilang tunggu pencairan proyek") hanya muncul di rekap untuk pemilik, tidak di draf.
