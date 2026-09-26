# Dasar Aturan Tenggat Setor & Lapor Pajak — dicek 25 September 2026 (revisi v1.0.1 dicek ulang 25 September 2026)

> Ringkasan untuk alat bantu jadwal, bukan nasihat pajak. Situs resmi (pajak.go.id, jdih.kemenkeu.go.id, peraturan.go.id, setneg.go.id) **tidak bisa dibuka langsung** dari lingkungan kerja saat riset; semua butir di bawah diverifikasi dari **hasil pencarian & sumber sekunder tepercaya** (DDTC News, Ortax, akun resmi Kring Pajak di X, portal berita nasional). Karena itu seluruh tabel berstatus minimal **PERLU REVIEW terhadap naskah resmi** sebelum rilis.
> Status: **Konsisten** = dua sumber sekunder atau lebih + kutipan pasal cocok; **PERLU REVIEW** = satu sumber / belum ada kutipan pasal / penafsiran skill.

## 1. Tenggat bulanan (PMK 81/2024, berlaku 1 Januari 2025 bersamaan dengan Coretax)
| # | Butir | Ketentuan dipakai skill | Status | Sumber |
|---|---|---|---|---|
| 1 | Setor PPh 4(2), 15, 21, 22, 23, 25, 26 | Paling lambat **tgl 15 bulan berikutnya** (penyeragaman; dulu tgl 10/15) | Konsisten (Ps. 94 ayat 2) | [1][2][3][4] |
| 2 | Lapor SPT Masa PPh 21/26 & SPT Masa PPh Unifikasi | **Tgl 20 bulan berikutnya** | Konsisten (Ps. 171) | [2][5][6] |
| 3 | Setor PPN/PPnBM | **Akhir bulan berikutnya** dan sebelum SPT Masa PPN disampaikan | Konsisten | [7][8] |
| 4 | Lapor SPT Masa PPN | **Akhir bulan berikutnya** (Ps. 171 ayat 13) | Konsisten | [9][8] |
| 5 | Pengecualian PPN: kegiatan membangun sendiri & pemanfaatan BKP tidak berwujud/JKP dari luar daerah pabean | Setor tgl 15 bulan berikutnya | Konsisten; **tidak dimodelkan** skill (kasus khusus → konsultan) | [7] |
| 6 | PPh Final UMKM (PP 55/2022) | Setor tgl 15; setoran tervalidasi **dianggap** menyampaikan SPT Masa (Ps. 171 ayat 4) | Konsisten | [10][3] |
| 7 | PPh 25 | Setor tgl 15; batas lapor SPT Masa PPh 25 **tgl 20**, tetapi WP yang sudah setor dan mendapat validasi (NTPN) **dianggap telah lapor pada tanggal setor** (Ps. 171 PMK 81/2024) → skill tidak membuat acara lapor terpisah | Isi konsisten (Kring Pajak menyebut batas lapor Ps. 171 tgl 20; ringkasan pencarian mengutip Ps. 171 **ayat 10** untuk "dianggap lapor"); nomor ayat **PERLU REVIEW** terhadap naskah resmi | [25][26] |
| 8 | Setor/bayar jatuh pada hari libur | Boleh **hari kerja berikutnya** — **Ps. 100 ayat 1** PMK 81/2024 ("dalam hal tanggal jatuh tempo pembayaran atau penyetoran pajak sebagaimana dimaksud dalam Pasal 94 bertepatan dengan hari libur, ... dapat dilakukan paling lambat pada hari kerja berikutnya"). Hari libur = Sabtu, Minggu, libur nasional, hari libur pemilu, **cuti bersama nasional**. (v1.0.0 menulis "Ps. 94 dst." — Ps. 94 adalah pasal tenggatnya, pergeseran ada di Ps. 100.) | Konsisten (isi, 3+ sumber); kutipan Ps. 100 dari sumber sekunder (hasil pencarian diskusipajak.com/Kring Pajak) — PERLU REVIEW naskah resmi | [1][11][12][27] |
| 9 | Lapor SPT **Masa** jatuh pada hari libur | Boleh hari kerja berikutnya (Ps. 173 ayat 1) | Konsisten | [9][13] |
| 10 | Contoh penerapan: SPT Masa PPh 21/Unifikasi masa Feb 2026 | 20 Mar 2026 (cuti Idulfitri) → **25 Mar 2026** | Konsisten (dipakai sebagai tes regresi) | [13] |
| 11 | Contoh penerapan: setor PPh masa April 2026 | 15 Mei 2026 (cuti bersama) → **18 Mei 2026** | Konsisten (tes regresi) | [14] |
| 12 | Geser berulang bila hari kerja berikutnya juga libur | Skill menggeser terus sampai hari kerja | Penafsiran wajar dari "hari kerja berikutnya"; cocok dengan contoh #10 | — |

## 2. Tenggat tahunan
| # | Butir | Ketentuan dipakai skill | Status | Sumber |
|---|---|---|---|---|
| 13 | SPT Tahunan PPh OP | Paling lambat 3 bulan setelah akhir tahun pajak (**31 Maret**) | Konsisten | [15][16] |
| 14 | SPT Tahunan PPh Badan | Paling lambat akhir bulan ke-4 setelah akhir tahun pajak (**30 April** untuk tahun buku kalender) | Konsisten | [15] |
| 15 | PPh 29 (kurang bayar tahunan) | Dilunasi sebelum SPT Tahunan disampaikan | Konsisten (ketentuan UU KUP) — tanggal setor PPh 29 tidak dibuat acara terpisah | [16] |
| 16 | SPT Tahunan jatuh di hari libur | **Tidak** bergeser otomatis; DJP memundurkan hanya lewat kebijakan khusus (2025: 31 Mar → 11 Apr; 2026: KEP-55/PJ/2026 → 30 Apr) | Dicek ulang 2026-09-25: DJP menegaskan pada Maret 2025 (sudah era PMK 81/2024, Ps. 169 ayat 1-2) bahwa batas 31 Mar 2025 tidak berubah walau Idulfitri, lalu memberi perpanjangan khusus; sumber sekunder menyebut perpanjangan hari libur hanya untuk SPT Masa. Belum ada kutipan naskah Ps. 173 yang membatasi ke SPT Masa → tetap **PERLU REVIEW**. Dua kemungkinan dijelaskan ke pengguna: (a) tidak bergeser — tanggal skill tepat; (b) ternyata ikut bergeser — tanggal skill lebih awal sehingga tetap aman. **v1.0.2 (dicek 2026-09-25):** kutipan Ps. 173 ayat 1 berbunyi "batas akhir pelaporan sebagaimana dimaksud dalam Pasal 171 dan Pasal 172" — bila Ps. 172 memuat batas SPT Tahunan, pembacaan harfiah berarti SPT Tahunan ikut bergeser. Web search 2026-09-25: naskah Ps. 172 tidak bisa dibuka (BPK, JDIH, Ortax datacenter, DDTC terblokir dari lingkungan kerja); ringkasan sekunder saling bertentangan (DDTC 1801611 "hanya SPT Masa" — artikel era PMK lama 2024; ringkasan lain "berlaku semua jenis SPT" tanpa kutipan pasal). Kring Pajak menyebut batas SPT Masa PPN ada di Ps. 171 ayat 13, jadi isi Ps. 172 tetap belum diketahui → **PERLU REVIEW** (pemilik/konsultan: baca naskah Ps. 172). Sejak v1.0.2 script menampilkan kedua tanggal bila SPT Tahunan jatuh di hari libur (`kemungkinan_tanggal_bergeser` di JSON); tanggal kalender tidak berubah. | [17][18][28][36] |
| 17 | Perpanjangan khusus | SPT Tahunan tahun pajak 2025 (OP & badan) diseragamkan sampai **30 April 2026** lewat **KEP-55/PJ/2026** (sekali saja) — tidak dimodelkan | Konsisten (1 sumber utama) | [19] |
| 18 | Perpanjangan atas permohonan WP | Bisa sampai 2 bulan dengan pemberitahuan — tidak dimodelkan | Konsisten | [16] |
| 19 | Bukti potong BPA1 (dulu 1721-A1) ke karyawan | Paling lama 1 bulan setelah masa pajak terakhir (PER-2/PJ/2024); skill menampilkan 31 Januari **tanpa geser** | **PERLU REVIEW** (pergeseran hari libur untuk bukti potong belum diverifikasi) | [20] |

## 2a. Faktur pajak keluaran (ditambahkan v1.0.1)
| # | Butir | Ketentuan dipakai skill | Status | Sumber |
|---|---|---|---|---|
| 20 | Batas unggah e-Faktur (termasuk di Coretax) | Diunggah & **mendapat persetujuan DJP paling lambat tgl 20 bulan berikutnya setelah tanggal pembuatan faktur** (PER-11/PJ/2025 Ps. 44 ayat 1, ditetapkan & berlaku 22 Mei 2025; sebelumnya tgl 15 menurut PER-03/PJ/2022). Faktur yang tidak disetujui bukan faktur pajak yang sah. Skill membuat acara "UNGGAH faktur pajak keluaran bulan X" tgl 20 untuk profil `ppn`/`pkp`/`badan-pkp` | **Konsisten** (akun resmi Kring Pajak di X + DDTC + Ortax + beberapa konsultan) | [29][30][31][32] |
| 21 | Unggah faktur jatuh di hari libur | **Tidak** bergeser — ditampilkan di tgl 20 dengan label "TIDAK bergeser" + saran hari kerja sebelumnya (v1.0.2; mis. 20 Mei 2027 → Jumat 14 Mei 2027) | **PERLU REVIEW** — hanya sumber sekunder: DDTC (era batas tgl 15: "upload e-Faktur paling telat tanggal 15, tak terpengaruh tanggal merah"), Pajakku & Bisa Pajak (Lebaran: batas unggah tidak diperpanjang). Pergeseran Ps. 100/173 PMK 81/2024 hanya menyebut pembayaran & pelaporan. | [33][34][35] |

## 3. Pembayaran di Coretax (info untuk pengguna, tidak dihitung skill)
- Kode billing dibuat di Coretax menu Pembayaran; bisa juga dari saldo **deposit pajak** (KAP 411618, KJS 100) yang dipakai untuk kewajiban apa pun. [21]
- Pemindahbukuan (Pbk) diajukan lewat Coretax menu Pembayaran → Permohonan Pemindahbukuan. [21]
- Masa berlaku kode billing di Coretax **belum diverifikasi** — jangan sebut angka hari.

## 4. Perubahan 2025–2026 yang relevan
- **PMK 81/2024** (berlaku 1 Jan 2025) — penyeragaman tgl 15/20 dan pergeseran hari libur di atas.
- **PP 20/2026** (ditetapkan 22 April 2026) mengubah PP 55/2022 (subjek PPh final 0,5%); tenggat setor tetap mengikuti PMK 81/2024. Rincian subjek: skill `pph-final-umkm`.
- **PMK 49/2026**: batas waktu khusus setor PPN atas pemanfaatan dari luar daerah pabean (PPN TDLN) — **tidak dimodelkan**, PERLU REVIEW bila pengguna punya transaksi impor jasa digital. [22]
- **KEP-55/PJ/2026**: perpanjangan SPT Tahunan 2025 ke 30 April 2026 (lihat #17).
- Tidak ditemukan (per 25 Sep 2026) PMK yang mengubah tgl 15/20/akhir bulan untuk 2027. Tetap cek pengumuman DJP.

## 5. Hari libur nasional & cuti bersama
| Tahun | Dasar | Jumlah | File | Status |
|---|---|---|---|---|
| 2026 | SKB Menag, Menaker, MenPANRB No. 1497/2025, 2/2025, 5/2025 (19 Sep 2025) | 17 libur + 8 cuti bersama | `libur-nasional-2026.csv` | Konsisten dari beberapa sumber sekunder; hari dalam seminggu dicocokkan dengan kalender |
| 2027 | SKB No. 1205/2026, 3/2026, 2/2026 (15 Sep 2026) | 18 libur (Isra Mikraj muncul dua kali: 5 Jan & 26 Des 2027) + 8 cuti bersama | `libur-nasional-2027.csv` | Konsisten dari beberapa sumber sekunder; PERLU REVIEW terhadap lampiran SKB resmi |
| 2028+ | Belum terbit | — | — | Script memberi PERINGATAN dan hanya menggeser Sabtu/Minggu |

Pemerintah bisa mengubah SKB (mis. menggeser cuti bersama). Bila berubah, perbarui CSV dan jalankan ulang tes.

## Sumber (dicek 2026-09-25)
1. Kring Pajak (X) — Ps. 94 PMK 81/2024, tgl 15: https://x.com/kring_pajak/status/2021876742596837857
2. Ortax — Batas waktu setor & lapor PPh Unifikasi: https://ortax.org/batas-waktu-setor-dan-lapor-pph-unifikasi
3. Ortax — PMK 81/2024 ubah tanggal jatuh tempo: https://ortax.org/jatuh-tempo-pembayaran-pajak-masa-menurut-pmk-81-2024
4. DDTC — PMK 81/2024 terbit, Coretax seragamkan tanggal setor: https://news.ddtc.co.id/berita/nasional/1806640/pmk-812024-terbit-coretax-seragamkan-tanggal-setor-pajak
5. Kring Pajak (X) — PPh 21 setor 15, lapor 20: https://x.com/kring_pajak/status/1970341259035492665
6. Ortax — Batas waktu setor & lapor PPh 21: https://ortax.org/ketentuan-batas-waktu-setor-dan-lapor-pph-pasal-21
7. Klikpajak — Batas waktu setor pajak terbaru mulai 2025: https://klikpajak.id/blog/surat-setoran-pajak-dan-batas-waktu-penyetoran-pajak/
8. OnlinePajak — Pengaruh PMK 81/2024 terhadap SPT Masa PPN: https://www.online-pajak.com/seputar-efaktur-ppn/pengaruh-pmk-81-tahun-2024-terhadap-pelaporan-spt-masa-ppn/
9. Kring Pajak (X) — SPT Masa PPN Ps. 171 ayat 13: https://x.com/kring_pajak/status/1939863389330973025
10. DDTC — Apa itu PPh Final UMKM: https://news.ddtc.co.id/literasi/kamus/1811984/apa-itu-pph-final-umkm
11. Kring Pajak (X) — PPh 21/26 hari libur: https://x.com/kring_pajak/status/2089567954849730721
12. Pajakku — Batas waktu bayar & setor sesuai PMK 81/2024: https://artikel.pajakku.com/batas-waktu-bayar-dan-setor-pajak-terbaru-mulai-tahun-2025-sesuai-pmk-812024/
13. DDTC — Ada libur panjang, batas lapor SPT Masa PPh dimundurkan (25 Mar 2026): https://news.ddtc.co.id/berita/nasional/1818124/ada-libur-panjang-batas-waktu-pelaporan-spt-masa-pph-dimundurkan
14. DDTC — Ada libur panjang, batas akhir setor PPh masa April diundur: https://news.ddtc.co.id/berita/nasional/1819436/ada-libur-panjang-batas-akhir-setor-pph-masa-april-diundur
15. Klikpajak — Batas waktu pembayaran & pelaporan SPT: https://klikpajak.id/blog/batas-waktu-pembayaran-pajak-badan/
16. Pajak.com — PMK 81/2024 perpanjangan lapor SPT Tahunan: https://www.pajak.com/pajak/pmk-81-2024-ini-ketentuan-perpanjangan-lapor-spt-tahunan-pph/
17. DDTC — Jatuh pada hari libur, batas lapor SPT Tahunan tidak diundur: https://news.ddtc.co.id/berita/nasional/1801611/jatuh-pada-hari-libur-batas-waktu-pelaporan-spt-tahunan-tidak-diundur
18. DDTC — Ada libur Lebaran, DJP: batas SPT Tahunan tak berubah: https://news.ddtc.co.id/berita/nasional/1809076/ada-libur-lebaran-djp-batas-waktu-pelaporan-spt-tahunan-tak-berubah
19. DDTC — Batas lapor SPT Tahunan OP diperpanjang hingga April 2026: https://news.ddtc.co.id/berita/nasional/1818216/batas-waktu-pelaporan-spt-tahunan-wp-op-diperpanjang-hingga-april-2026
20. Klikpajak — Bukti potong BPA1/BPA2: https://klikpajak.id/blog/bukti-potong-pph-21-formulir-1721-a1-dan-1721-a2/
21. Pajakku — Panduan deposit pajak di Coretax: https://pajakku.com/artikel/panduan-lengkap-deposit-pajak-di-coretax-djp ; Ortax — Ketentuan deposit: https://ortax.org/ketentuan-pembayaran-pajak-dengan-deposit-pajak
22. DDTC — PMK 49/2026 batas waktu khusus setor PPN TDLN: https://news.ddtc.co.id/berita/nasional/1821207/pmk-492026-atur-batas-waktu-khusus-setor-ppn-tdln
23. Libur 2026: Kemenko PMK https://www.kemenkopmk.go.id/pemerintah-tetapkan-17-hari-libur-nasional-dan-8-cuti-bersama-tahun-2026 ; RRI (16 Jan Isra Mikraj) https://rri.co.id/lain-lain/2086667/16-januari-2026-libur-nasional-peringati-isra-mikraj ; Liputan6 (Mei 2026) https://www.liputan6.com/cek-fakta/read/6370908/skb-3-menteri-libur-mei-2026-simak-jadwal-lengkapnya ; UMJ https://umj.ac.id/just_info/catat-sekarang-daftar-lengkap-hari-libur-nasional-dan-cuti-bersama-2026/
24. Libur 2027: CNN Indonesia https://www.cnnindonesia.com/nasional/20260915115826-20-1404106/daftar-lengkap-18-hari-libur-nasional-dan-8-cuti-bersama-2027 ; MenPANRB https://www.menpan.go.id/site/berita-terkini/pemerintah-tetapkan-18-hari-libur-nasional-dan-8-hari-cuti-bersama-tahun-2027 ; Hukumonline https://www.hukumonline.com/berita/a/Daftar-libur-nasional-2027%20-lt6aaa6070150ec/ ; Kemenag https://kemenag.go.id/en/nasional/terbit-skb-3-menteri-berikut-daftar-libur-nasional-dan-cuti-bersama-2027-xjNBM
25. Kring Pajak (X) — PPh 25: setor tgl 15 (Ps. 94), lapor tgl 20 (Ps. 171): https://x.com/kring_pajak/status/2054114604213825871 (dicek 2026-09-25, via hasil pencarian)
26. DDTC — Sudah setor PPh PHTB & divalidasi NTPN, tak perlu lapor SPT (Ps. 171 ayat 3): https://news.ddtc.co.id/berita/nasional/1808853/sudah-setor-pph-phtb-dan-divalidasi-dengan-ntpn-tak-perlu-lapor-spt
27. Diskusi Pajak — Jatuh tempo bayar & lapor PPh 21 pada hari libur (mengutip Ps. 100 ayat 1): https://www.diskusipajak.com/bagaimana-jika-jatuh-tempo-bayar-dan-lapor-spt-pph-21-jatuh-pada-hari-libur/ ; Supriyanto Rekan — PMK 81/2024 pembayaran jatuh hari Sabtu: https://www.supriyantorekan.com/2025/02/pmk-81tahun-2024-pembayaran-dan.html (keduanya dibaca lewat hasil pencarian 2026-09-25; situs tidak bisa dibuka langsung)
28. Kompas — DJP perpanjang batas lapor SPT Tahunan 2024 sampai 11 April 2025: https://www.kompas.com/jawa-barat/read/2025/03/26/125800488/ditjen-pajak-perpanjang-batas-waktu-lapor-spt-tahunan-2024-sampai-11 ; DDTC — DJP beri relaksasi batas SPT Tahunan OP: https://news.ddtc.co.id/berita/nasional/1809699/djp-beri-relaksasi-terkait-batas-waktu-pelaporan-spt-tahunan-op
29. Kring Pajak (X) — Ps. 44 ayat 1 PER-11/PJ/2025, faktur masa September batas unggah 20 Oktober: https://x.com/kring_pajak/status/1978331690327253221 ; juga https://x.com/kring_pajak/status/1957661569468494169 dan https://x.com/kring_pajak/status/1944593617815060758 (tgl 20 = batas unggah faktur, beda dengan lapor SPT Masa PPN)
30. DDTC — PER-11/PJ/2025 terbit, batas upload e-Faktur diundur jadi tanggal 20: https://news.ddtc.co.id/berita/nasional/1811050/per-11pj2025-terbit-batas-upload-e-faktur-diundur-jadi-tanggal-20 ; https://news.ddtc.co.id/berita/nasional/1811029/batas-upload-faktur-pajak-mundur-jadi-tanggal-20
31. Ortax — Batas upload faktur pajak mundur jadi tanggal 20: https://ortax.org/batas-upload-fp-mundur-jadi-tanggal-20
32. Pajak.com — PER-11/2025 ubah batas waktu unggah e-Faktur jadi tanggal 20: https://www.pajak.com/pajak/wajib-pajak-perlu-ketahui-per-11-2025-ubah-batas-waktu-unggah-e-faktur-jadi-tanggal-20/
33. DDTC — Upload e-Faktur paling telat tanggal 15, tak terpengaruh tanggal merah (aturan lama): https://news.ddtc.co.id/berita/nasional/1803236/upload-e-faktur-paling-telat-tanggal-15-tak-terpengaruh-tanggal-merah
34. Pajakku — Libur Lebaran, batas upload faktur pajak diperpanjang?: https://pajakku.com/artikel/libur-lebaran-batas-upload-faktur-pajak-diperpanjang ; https://artikel.pajakku.com/ada-cuti-bersama-lebaran-apakah-batas-waktu-upload-faktur-pajak-diperpanjang
35. Bisa Pajak — Batas upload faktur pajak tak mundur meski cuti bersama: https://bisapajak.id/batas-upload-faktur-pajak-lebaran/
36. Pencarian 2026-09-25 soal Ps. 172/173 PMK 81/2024 (hanya ringkasan hasil pencarian, naskah tidak terbuka): JDIH Kemenkeu https://jdih.kemenkeu.go.id/dok/pmk-81-tahun-2024 ; BPK https://peraturan.bpk.go.id/Details/306614/pmk-no-81-tahun-2024 ; DDTC 1801611 (lihat [17]); Kring Pajak Ps. 171 ayat 13 (lihat [9])
