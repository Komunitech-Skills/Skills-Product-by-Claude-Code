# QA baca pembeli awam - promosi Minggu 18 Okt 2026 20.00 WIB

Tugas A2 Akun A (papan-tugas "Pembagian 2026-10-16"). Dibaca sebagai pemilik UMKM awam teknologi. Sumber yang dibaca: `promosi/halaman-sebelum-sesudah.html` (isi kartu berasal dari `promosi/sebelum-sesudah.jsonl`, 118 skill `lolos_promosi: true`) dan, per skill, bagian "Contoh sebelum & sesudah" (atau "Sebelum / sesudah") + "Bukti uji di bot Telegram" di `skills/<nama>/README.md`. Dari 118 skill, 29 milik Akun B (gelombang Telegram, tidak disentuh), 89 diperiksa dan diperbaiki langsung kalimatnya.

Catatan penting: kartu di halaman menampilkan **apa adanya** kolom `angka_kunci` dan `catatan_jujur` (skrip `promosi_sebelum_sesudah.py` baris `"angka": ..., "catatan": ...`). Jadi masalah terbesar ada di jsonl, bukan di HTML.

## Ringkasan prioritas

**P1 - harus diputuskan/diperbaiki sebelum Minggu 20.00 (Akun B/pemilik, bukan saya):**

1. **Kartu dipromosikan, padahal bukti Telegram di README (dan di catatan kartu itu sendiri) menyatakan skill belum lulus atau malah kalah.** Pembeli yang membuka kartu lalu README akan melihat dua cerita. Terparah: `audit-akun-iklan` (Telegram 7,5 -> 6, "skill kalah"), `iterasi-dari-masukan-pelanggan` (6 -> 5, angka salah), `pph21-ter` (Telegram 8 -> 6 pada v1.0.4, skill kalah; perbaikan 1.0.5 belum diulang di bot), `ekstrak-nota-faktur` (4,5 -> 7,5 "belum lulus", file Excel tidak terkirim), `presentasi-instan` (6,9 -> 7,5), `cv-lamaran-ats` (7 -> 8), `arsip-nota` (7 -> 8), `laporan-status-kantor` (4,5 -> 5; keputusan 19a pemilik: tidak dipromosikan, tetapi `lolos_promosi` masih true). Daftar lengkap ada di bagian "Untuk Akun B".
2. **`checklist-keamanan-pangan-usaha`: `catatan_jujur` sendiri menulis "DITAHAN dari promosi ... memuat fakta keamanan pangan yang salah" tetapi `lolos_promosi` true dan kartu tampil.** Aturan kartu di halaman: "tidak ada angka atau fakta yang salah". Kontradiksi langsung.
3. **Kalimat aturan di halaman terlalu mutlak:** "Skill tampil di sini bila ... tidak ada angka atau fakta yang salah." Padahal catatan kartu mengakui sisa cacat (mis. `naskah-live-jualan` "frasa 'selalu ready' masih muncul", `landing-page-siap-tayang` "masih sesekali menambah frasa fitur kecil yang tidak disebut pengguna", `tagih-piutang` "Script keliru membaca kolom 'sdh bayar'", `proposal-kerjasama` "kadang menambah janji yang tidak diberikan pengguna", `hitung-thr` "nama usaha karangan"). Usulan kalimat ada di bagian Halaman.
4. **`perjanjian-sederhana`: `selisih` di jsonl 3,75 padahal 9,0 - 4,25 = 4,75.** Skrip menghitung ulang selisih saat menampilkan (jadi mungkin tidak tampil salah), tetapi jsonl perlu dibetulkan agar `SEBELUM-SESUDAH.md` konsisten. Juga `checklist-keamanan-pangan-usaha` 2,6 vs hitungan 2,65 (pembulatan).

**P2 - jargon dan kode internal yang tampil di kartu (perlu dibersihkan di jsonl oleh Akun B/lead, saya tidak boleh mengubah `promosi/*`):**

5. `catatan_jujur` di puluhan kartu berisi istilah proses yang tidak dimengerti pembeli: "gelombang 12/13/14/15", "BELUM", "LULUS", "uji ulang", "agent kurator", "mock", "router", "tool call", "find /", "gateway", "non-deterministik", "sampel 3 sesi", "pra-cek", "Pilot ulang bot Telegram (26, 2026-10-12)" (angka 26 = nomor keputusan internal), "tetap di bundle, tidak dipakai sebagai cuplikan pilot". Daftar skill per jenis istilah ada di bagian "Pola lintas skill".
6. `angka_kunci`/`tanpa_skill`/`dengan_skill` memuat nama berkas dan perintah: `openclaw.json` (pengingat-follow-up), `hitung_pl_jurnal.py`, `ambil_berita.py`, `cek_koin.py`, `kripto/JURNAL.csv` (pantau-pasar-kripto), `cek_balasan.py --faskes` (balas-ulasan-pelanggan), `cek_pola.py` (tulisan-tanpa-kesan-ai), "doctor --fix", "exec 'ask'", "token -> restart" (cek-privasi-openclaw), "endpoint", "regresi" (siyuan-sop), "47 endpoint".
7. Catatan yang menjelaskan **riwayat versi dan metode uji** (misalnya "1.0.0 BELUM 5,25->6,75; 1.0.1 BELUM 4,75->7,5; 1.0.2 LULUS tipis 8,19") membingungkan pembeli awam dan membuat skill terlihat rapuh. Cukup satu kalimat hasil terakhir dan batas uji.

**P3 - kalimat di README (sudah saya perbaiki untuk 89 skill di luar daftar 29, lihat bagian "Yang sudah diperbaiki"):** placeholder "(pesan di grup uji internal Komunitech)", "gelombang N", "Verdik ...", "versi repo", tautan pesan yang tidak tercatat, nama berkas skrip di cuplikan, istilah teknis `--ya`, singkatan JP tanpa penjelasan.

## Halaman `halaman-sebelum-sesudah.html`

| Lokasi | Kutipan | Masalah | Usulan pengganti |
|---|---|---|---|
| Judul `h1` | "Pertanyaan yang sama, bot yang sama. Bedanya hanya skill." | "skill" belum dijelaskan untuk pembeli yang baru kenal; "bot yang sama" oke. | "Pertanyaan yang sama, asisten AI yang sama. Bedanya hanya satu: ada atau tidaknya skill Komunitech." |
| Lede | "Setiap skill kami uji dengan pesan sehari-hari dan pesan jebakan, sekali tanpa skill dan sekali dengan skill." | "pesan jebakan" kurang jelas; tidak menyebut berapa kali diuji. | "Setiap skill kami uji dengan pesan sehari-hari dan satu pesan yang sengaja memancing kesalahan, sekali tanpa skill dan sekali dengan skill." |
| Statistik | "skill dengan bukti jelas" | "bukti jelas" terdengar sebagai klaim mutlak. | "skill yang bedanya terlihat jelas pada uji kami" |
| Langkah 1 | "Dua pesan gaya chat WA: pekerjaan biasa dan satu jebakan (data kurang, aturan baru, permintaan berisiko)." | "jebakan" ambigu. | "Dua pesan gaya chat WA: pekerjaan biasa dan satu pesan sulit (data kurang, aturan baru, atau permintaan berisiko)." |
| Langkah 2 | "Bot & model sama / Satu-satunya beda: skill dimatikan atau aktif." | "model" istilah teknis. | "Asisten AI yang sama / Satu-satunya beda: skill dimatikan atau dinyalakan." |
| Langkah 4 | "Angka dihitung ulang ... dengan kalkulator terpisah; aturan yang dikutip dicek." | Mutlak ("dicek") padahal beberapa kartu bilang "PERLU REVIEW". | "Angka kami hitung ulang dengan kalkulator terpisah; aturan yang dikutip kami cek ke sumbernya (beberapa masih ditandai perlu ditinjau ahli)." |
| Aturan | "Skill tampil di sini bila skor dengan skill >= 8, lebih tinggi >= 1,5 poin, dan tidak ada angka atau fakta yang salah." | Klaim mutlak, bertentangan dengan catatan kartu (lihat P1 no. 2-3). | "Skill tampil di sini bila skor dengan skill minimal 8, lebih tinggi minimal 1,5 poin, dan pada uji terakhir kami tidak menemukan angka atau fakta yang salah. Sisa kekurangan yang kami temukan ditulis di tiap kartu." |
| Aturan | "Penilainya AI, jadi selisih kecil tidak berarti banyak; hasil bisa berbeda di model AI lain." | Bagus dan jujur; "model AI lain" cukup dimengerti. | Pertahankan. |
| Header | "Hasil uji · OpenClaw · 2026-10-16" | Tanggal 16 Okt padahal promosi 18 Okt; "OpenClaw" sudah dikenal member VIP, tetapi non-member mungkin tidak. | "Hasil uji di OpenClaw (asisten AI yang dipakai member Komunitech) - diperbarui 16 Okt 2026" |
| Kartu (semua) | Label "skor tanpa skill/dengan skill" | Skor 1-10 dari AI penguji; belum ada penjelasan "10 itu apa" di kartu. | Tambah satu baris di bawah aturan: "10 = jawabannya bisa langsung dipakai tanpa diperbaiki." |
| Kartu medis | label "Belum direview tenaga medis" | Sudah jelas dan jujur. | Pertahankan. |

## Pola lintas skill (isi kartu/README)

| Pola | Contoh kutipan | Skill yang kena (tampil di kartu) | Usulan |
|---|---|---|---|
| Istilah proses "gelombang N" di `catatan_jujur` | "Terbukti di bot Telegram asli (gelombang 12, 2026-10-12, agent kurator)" | cek-privasi-openclaw, laporan-otomatis-terjadwal, rencana-pelajaran-guru, fider-masukan-pelanggan, notebook-riset-lokal, proposal-kerjasama, laporan-status-kantor, sop-onboarding, strategi-konten-iklan, sunting-tulisan-jelas, analisis-selisih-anggaran, seleksi-cv-pelamar, triase-email-masuk, rangkaian-pesan-pelanggan, rapor-mingguan-ai, landing-page-siap-tayang, proses-pesanan-wa, checklist-keamanan-pangan-usaha, simulasi-cicilan-pinjaman, cek-risiko-dan-asuransi-usaha, persiapan-jual-atau-wariskan-usaha, cari-prospek-web, satu-lawan-satu-dan-umpan-balik, pantau-cron-openclaw | "Diuji juga di bot Telegram sungguhan pada 12 Okt 2026: skor 7,5 menjadi 9." |
| "BELUM"/"LULUS" kapital | "Versi awal 1.0.4 sempat BELUM lulus." | siyuan-sop, cek-privasi-openclaw, surat-peringatan-karyawan, hledger-usaha, strategi-merek-usaha, atur-keuangan-pribadi, foto-produk-brief, kalkulator-klinis-nakes, pantau-pasar-kripto, cek-risiko-dan-asuransi-usaha, simulasi-cicilan-pinjaman, cari-prospek-web, bandingkan-pemasok-vendor, ubah-draf-ke-dokumen, kartu-belajar-anki, kalender-pajak (+ banyak lain) | Ganti "BELUM" dengan "belum lulus uji kami" atau hapus riwayat versi lama; "LULUS" dengan "lulus". |
| Riwayat versi uji | "1.0.0 BELUM 5,25->6,75; 1.0.1 BELUM 4,75->7,5; 1.0.2 LULUS tipis 8,19" | pantau-cron-openclaw, seleksi-cv-pelamar, bandingkan-pemasok-vendor, ubah-draf-ke-dokumen, kartu-belajar-anki, rencana-restok-barang, cari-prospek-web, tagih-piutang | Sisakan hasil terbaru saja: "Pada uji terakhir: 4 menjadi 8." |
| Nama berkas/perintah | "mengubah openclaw.json dua kali tanpa izin"; "script hitung_pl_jurnal.py dijalankan dua kali"; "cek_balasan.py --faskes" | pengingat-follow-up, pantau-pasar-kripto, balas-ulasan-pelanggan, tulisan-tanpa-kesan-ai, listing-marketplace, checklist-keamanan-pangan-usaha, tagih-piutang | "mengubah berkas pengaturan bot dua kali tanpa izin"; "alat hitung bawaan skill dijalankan dua kali"; hapus nama berkas. |
| Istilah teknis agent | "mengubah konfigurasi gateway dan menjalankan doctor --fix"; "exec 'ask' -> automation ditolak"; "token -> restart"; "6-14 tool call"; "agent sempat find /" | cek-privasi-openclaw, pantau-pasar-kripto, pengingat-pasien-klinik, rapor-mingguan-ai, karyawan-ai-mulai, pph-final-umkm, arus-kas-13minggu, harga-jual-marketplace, kalender-pajak | "mengubah pengaturan inti bot dan menjalankan perbaikan otomatis tanpa persetujuan"; "6-14 langkah kerja"; "sempat menelusuri seluruh isi komputer uji". |
| Server/uji tiruan jargon | "server SiYuan tiruan (8 endpoint)"; "mock API"; "kunci Fider mock tidak terbaca" | siyuan-sop, fider-masukan-pelanggan, notebook-riset-lokal | "Diuji dengan SiYuan tiruan di komputer uji, bukan aplikasi sungguhan." |
| Frasa internal pilot | "tetap di bundle, tidak dipakai sebagai cuplikan pilot" | notebook-riset-lokal, sunting-tulisan-jelas, analisis-selisih-anggaran, triase-email-masuk, rangkaian-pesan-pelanggan, proses-pesanan-wa, persiapan-jual-atau-wariskan-usaha | Hapus kalimat; diganti "Pada uji di Telegram selisihnya kecil (+0,5)." (angka sudah ada di kalimat sebelumnya). |
| Singkatan tak dijelaskan di kartu | "HPP", "DPP", "PKP", "TER", "NPV", "IRR", "FIFO", "P25", "opt-in", "SKU" | spesifikasi-produk-usaha, buku-stok, buat-invoice, surat-penawaran-harga, slip-gaji-bpjs, hitung-thr, pph21-ter, kelayakan-investasi-usaha, pantau-pasar-kripto, riset-harga-kompetitor, laporan-iklan-mingguan, listmonk-newsletter | Satu penjelasan dalam kurung pertama kali muncul: "HPP (modal pokok per barang)", "NPV (nilai untung dihitung ke uang hari ini)". |
| Skor yang berubah-ubah dalam satu catatan | "Skor 7 / 3 / 6" dan "Skor 9 / 8,67 / 8" tanpa penjelasan | pantau-pasar-kripto | "Tiga skenario diuji: rata-rata 5,3 menjadi 8,6." |
| Klaim mutlak pada hasil | "0 pelanggaran dari 4 sesi"; "Terbukti di bot Telegram asli"; "semua angka cocok" | laporan-otomatis-terjadwal, hampir semua "Terbukti ..." | "Terbukti" -> "Teruji"; sebut jumlah percobaan ("pada 4 percobaan, tidak ada pelanggaran"). |
| Uji dengan sampel sangat kecil dipakai sebagai angka utama | "Hanya satu skenario ... bukan 5 skenario per skill" | harga-jual-marketplace, listing-marketplace, balas-ulasan-pelanggan, pengingat-pasien-klinik, promo-kalender, rekap-penjualan-csv, kalender-pajak, pantau-pasar-kripto | Sudah jujur; ringkas jadi satu kalimat: "Diuji pada satu skenario." |

## Temuan per skill (89 skill di luar daftar 29; S = sudah saya perbaiki di README, A = kirim ke Akun B/lead karena menyangkut angka/verdik/jsonl)

Format: skill | kutipan | masalah | usulan | tindakan.

| Skill | Kutipan | Masalah | Usulan | Tindakan |
|---|---|---|---|---|
| siyuan-sop | "Diuji dengan server SiYuan tiruan (8 endpoint)"; "Uji regresi v1.0.10"; "mesin inti SiYuan resmi v3.8.5" | "endpoint", "regresi", "mesin inti" jargon | "Diuji dengan SiYuan tiruan di komputer uji"; "Uji ulang v1.0.10" | S (README: mesin inti dihapus); A (kartu) |
| kontrak-kerja-pkwt | "keluaran nyata skrip `hitung_pkwt.py`"; "bot Telegram asli, gelombang 4 (2026-10-03)" | nama berkas, "gelombang" | "hasil hitung nyata dari alat hitung bawaan skill"; "bot Telegram asli (2026-10-03)" | S |
| spt-tahunan-op | Kartu: "kurang bayar Rp14.400.000 (PKP Rp136.000.000)"; README contoh: kurang bayar Rp5.700.000 | Kartu dan README memakai kasus berbeda tanpa penjelasan; "PKP" tidak dijelaskan | Tambah di kartu: "(kasus konsultan IT omzet Rp380 juta)"; README sudah punya keterangan K/1 | A |
| cek-privasi-openclaw | Kartu: "mengubah konfigurasi gateway dan menjalankan doctor --fix"; "exec 'ask'"; "agent kurator" | istilah teknis berat | "mengubah pengaturan inti bot ... tanpa persetujuan" | S (README); A (kartu) |
| odoo-usaha | "sampel 3 sesi; model non-deterministik" | jargon | "Diuji 3 kali; hasil AI bisa sedikit berbeda tiap percobaan." | A |
| pengingat-follow-up | Kartu: "mengubah openclaw.json dua kali tanpa izin". README: "gelombang uji 4 (satu putaran uji di bot)"; "skor tidak dicatat di gelombang itu" | nama berkas; proses internal; skor Telegram tidak ada sama sekali | "mengubah berkas pengaturan bot dua kali tanpa izin"; README sudah diganti jadi "skor tidak dicatat" | S; A (kartu) |
| surat-peringatan-karyawan | "Putaran terakhir hanya sisi dengan skill (4 sesi)"; README Telegram: "(Gelombang ini tidak memberi skor angka.)" | jargon "sesi", "putaran" | "Uji terakhir hanya pada sisi dengan skill (4 percobaan)." | S (README); A (kartu) |
| katalog-reseller | "Reseller 20 bungkus untung sekitar Rp86.000 (dihitung script)" | angka Rp86.000 tidak ada di README (README: untung 10 pcs +-Rp143.000); "script" | "dihitung oleh alat hitung bawaan" | A (angka tak ditemukan di README) |
| karyawan-ai-mulai | README Telegram: "Verdik uji bot: LULUS - DENGAN memetakan 3 kebutuhan ke 3 skill nyata (rekap-penjualan-csv = ...)" | "Verdik"; nama skill dengan tanda hubung membingungkan | "Hasil: lulus - dengan skill, bot memetakan 3 kebutuhan ke 3 skill yang sudah ada ..." | S (hanya "Verdik" -> "Hasil") |
| riset-saham-berita | Kartu angka: "tanpa skill diberi target harga Rp550-575"; "PER 7,68x, PBV 1,07x" | "PER/PBV/ROE" tak dijelaskan; angka 575/1,07 tidak ada di README | Jelaskan dalam kurung atau hapus | A |
| laporan-otomatis-terjadwal | Kartu: "Gelombang 12 ... agent dengan skill mencari CSV di workspace sedangkan contoh ada di HOME bot uji (masalah lingkungan)"; "0 pelanggaran dari 4 sesi" | Sangat teknis, mengakui uji tidak sah di kartu promosi | Ringkas: "Uji di Telegram 12 Okt tidak dinilai karena masalah di komputer uji; diuji ulang kemudian." | A |
| kanboard-papan-kerja | Kartu: "kartu dipindah tanpa tanya -> tidak ada perubahan sebelum 'ya'"; skor sesudah 9 tidak muncul di README | tanda panah/"token" | - | A (skor tidak cocok README: cek) |
| edukasi-pasien-klinik | README: "Belum direview tenaga medis"; Catatan dosis; kartu: "Hanya 1 skenario regresi" | "regresi" jargon; selain itu bagus | "Diuji pada satu skenario ulang." | A |
| inventree-gudang | README: "ulangi perintah + --ya" dan "transkrip uji pembuat skill ... `examples/uji-pembuat/transkrip-inventree-1.5.6.txt`" | `--ya` tampil di contoh; path berkas | Penjelasan `--ya` ditambah; path diganti "folder `examples/`" | S |
| rencana-pelajaran-guru | README: "Contoh ini dibuat dengan versi awal yang menebak 3 JP ... bawaan sekarang 2 JP"; kartu: "Dasar CP: 032/H/KR/2024 (usang)" | "JP" tak dijelaskan; kalimat membingungkan (contoh dari versi lama) | "versi awal skill yang menebak 3 JP (jam pelajaran) ...; sekarang ... dipakai bawaan 2 JP" ; kartu: tulis nomor dasar CP lengkap | S (README); A (kartu: "timeout", "konteks Telegram") |
| fider-masukan-pelanggan | Kartu: "Gelombang 12 ... kunci Fider mock tidak terbaca" | jargon | Ringkas jadi "uji di Telegram 12 Okt gagal karena kunci uji tidak terbaca; perlu diulang" | A |
| kebijakan-privasi-pdp | Kartu: "tenggat tanpa skill ~34 jam vs seharusnya ~10 jam" | tidak jelas tenggat apa (notifikasi kebocoran data? 3x24 jam?) | "tenggat lapor kebocoran data" | A |
| slip-gaji-bpjs | README Telegram: "Diperbaiki di versi 1.0.7 ..., belum diuji ulang di bot Telegram. Versi 1.0.8 hanya memperbarui rujukan aturan JKK (PP 37/2021 dan perubahannya, PP 6/2025)" | Riwayat versi di bukti uji | Ringkas ke satu kalimat | S (hanya "versi repo" -> "versi skill") |
| lowongan-kerja | Kartu "UMK Sidoarjo 2026 Rp5.191.541" | README contoh memakai Semarang; kartu pakai Sidoarjo | - | A (konsistensi contoh) |
| dolibarr-usaha | Kartu: "API", "CSV" | Tidak dijelaskan | "sambungan data (API)" seperti di README | A |
| hledger-usaha | Kartu: "Laba bersih Rp7.865.500; neraca Rp21.515.500; sisa piutang Rp40.000"; README contoh: laba bersih Rp1.600.000, neraca Rp17.200.000 | **Angka kartu tidak sama dengan contoh di README** (kasus berbeda tanpa keterangan) | Tambahkan "(contoh uji lengkap)" di kartu atau samakan | A |
| perjanjian-sederhana | README Telegram: "Verdik gelombang: BELUM - ... file perjanjian lengkap gagal terkirim"; kartu 4,25 -> 9; selisih jsonl 3,75 | Telegram 6 -> 6,5 "belum lulus" bertentangan dengan kartu 4,25 -> 9; selisih salah | Beri keterangan "uji Telegram 3 Okt memakai versi lama, sudah diperbaiki"; betulkan selisih 4,75 | S (kata "gelombang"/"Verdik"); A (selisih/verdik) |
| program-referral-loyalitas | Kartu: "biaya/referral Rp42.500, laba pesanan pertama Rp25.000, kuota 23"; README contoh: biaya per referral Rp30.000, anggaran Rp600.000 maks 20 referral | **Angka kartu tidak ada di README** (kasus beda, hadiah Rp20.000 vs Rp15.000) | Samakan atau beri keterangan kasus | A |
| notebook-riset-lokal | README contoh berupa blok ```json``` (`"pertanyaan"`, `"jawaban"`, `"catatan"`) sebagai "Sesudah" | Pembeli awam melihat kode, bukan hasil; kalimat "AI akan menyampaikannya dalam kalimat biasa" sudah ada tapi di bawah blok | Pindahkan kalimat itu ke atas blok, atau tampilkan jawabannya sebagai kalimat | A (butuh edit isi contoh; tidak diubah) |
| tulisan-tanpa-kesan-ai | "skrip pemeriksa pola (`cek_pola.py`) 100/100"; "skor pola AI 100/100" | nama berkas; "100/100" terkesan mutlak | "pemeriksa pola AI bawaan memberi 100 dari 100; ini alat bantu, bukan jaminan lolos pendeteksi" | S (nama berkas); A (kartu) |
| frappe-books-usaha | Kartu "605.000" tidak ditemukan di README | angka tidak bisa ditelusuri | - | A |
| listmonk-newsletter | README: "opt-in double"; "Uji-kirim ke diri sendiri: BELUM / isi berubah sejak uji" | Istilah teknis di contoh | Tambah kurung: "opt-in double = pelanggan harus mengonfirmasi lewat email" | A (belum diubah; butuh keputusan penjelasan) |
| luncurkan-produk-baru | README Telegram: "Verdik uji bot: LULUS - DENGAN menutup semua jalur jual sebelum notifikasi BPOM terbit (termasuk pre-order/DP)" | Verdik/huruf kapital, kalimat panjang | - | S |
| umami-analitik | README: "klik dari WhatsApp tercatat sebagai 'Langsung'" | OK; "Bounce rate" dijelaskan | - | tidak ada temuan berat |
| proposal-kerjasama | Kartu: "Bot Telegram gelombang 9: 6,5 -> 8,5 (gelombang 8 dengan 1.0.8 masih 7,5)" | jargon "gelombang" | "Di Telegram: 6,5 menjadi 8,5" | A |
| laporan-harian-usaha | README OK ("Void = nota dibatalkan" dijelaskan) | - | - | bersih |
| pengajuan-kur | README Telegram: "gelombang 7"; "Verdik gelombang: LULUS"; "Pasal 20" | jargon proses | "Hasil: lulus" | S |
| spesifikasi-produk-usaha | Kartu "HPP maksimal Rp9.000 (jual Rp18.000, margin 50%)"; README contoh: jual Rp15.000, HPP maks Rp7.500 | Angka kartu beda kasus dengan README tanpa keterangan | Tambahkan kasus | A |
| uji-pasar-produk-cepat | README Telegram: "rentang Wilson 0-24%" | "Wilson" istilah statistik | "rentang wajar 0-24%" | S (Verdik/gelombang); A ("Wilson" tidak diubah: angka/istilah) |
| buku-piutang | README OK | - | - | bersih |
| kalkulator-klinis-nakes | Kartu: "aspirin 75-150 mg disebut" (tanpa skill); README: "(verdik uji LULUS)" | Kartu menyebut dosis obat dari jawaban tanpa skill, padahal ini skill medis; "verdik" | Hindari menyebut angka dosis di materi promosi; README "hasil uji: lulus" | S (README); A (kartu: dosis) |
| pph21-ter | README Telegram: "Jadi di uji ini skill kalah." dan "Dengan skill (versi 1.0.4): skor 6 dari 10" | **Kartu tampil 7,25 -> 8,9; README bilang skill kalah di bot Telegram** (sudah diperbaiki 1.0.5 tetapi belum diuji ulang di bot) | Putuskan tampil atau tidak; kalau tampil, kartu perlu catatan yang sama jelasnya | A (P1) |
| agen-cs-toko | README Telegram: "WhatsApp Web tidak resmi"; "mode Copilot" | "Copilot" tidak dijelaskan di bagian Telegram (dijelaskan di FAQ) | "mode Copilot (bot menyiapkan draf, Anda yang mengirim)" | A |
| grist-usaha | README: "--ya", "docId", "wa.me/" | Perintah teknis | Ditambah catatan `--ya` | S |
| laporan-iklan-mingguan | Kartu "Biaya per hasil Rp25.900 -> Rp36.842" tidak di README; "CPC/CPM/CTR" | angka tak ditemukan; singkatan | - | A |
| strategi-merek-usaha | README: "bot Telegram asli (gelombang 8, 2026-10-05) ..."; kartu "BELUM lulus (7,5)" | jargon | - | S (README); A (kartu) |
| actual-budget-usaha | "AI modern sudah menandai tarik tunai ..." | frasa aneh | "AI zaman sekarang sudah ..." | S |
| laporan-status-kantor | README Telegram: skor 4,5 -> 5, "Hasil: belum lulus"; kartu 6,3 -> 9 | **Keputusan 19a: tidak dipromosikan, tetapi `lolos_promosi` true** | Ubah `lolos_promosi` ke false atau minta pemilik | A (P1) |
| naskah-live-jualan | Kartu: "frasa 'oleh-oleh khas' dan 'selalu ready' masih muncul" | mengakui cacat di kartu padahal aturan halaman bilang tidak ada fakta salah | lihat P1 no. 3 | A; S (README Verdik) |
| atur-keuangan-pribadi | Kartu: "dana darurat 'kira-kira 15-18 juta' -> pokok sebenarnya Rp7.250.000"; README contoh memakai kasus Dimas & Rina (9 bulan Rp72.450.000) | kartu dan README beda kasus | beri keterangan | A |
| sop-onboarding | README: "keluaran nyata skrip `jadwal_onboarding.py`"; kartu: "pra-cek 1.0.4 hanya bertanya" | nama berkas, "pra-cek" | "hasil hitung nyata dari alat hitung bawaan" | S (README); A (kartu) |
| strategi-konten-iklan | README: "Bot Telegram asli (gelombang 10, 2026-10-05)"; kartu "43 pesanan", README contoh "84 pesanan" | jargon; beda kasus | - | S; A |
| buku-stok | Kartu "HPP" | - | - | A (kecil) |
| vikunja-tugas | README: "Ulangi perintah yang sama + --ya" | perintah teknis | catatan `--ya` | S |
| absensi-lokal | README contoh: "script, yaitu program kecil di dalam skill" | sudah dijelaskan | - | bersih |
| kasir-lokal | README: "PBJT" di kartu | singkatan | - | A (kecil) |
| tangani-keberatan-pelanggan | README Telegram: "gelombang 11", "verdik LULUS", "(tautan pesan uji ulang ini tidak tercatat)"; kartu "Pilot ulang bot Telegram (26, 2026-10-12)" | jargon | - | S (README); A (kartu) |
| aktifkan-kembali-pelanggan | README Telegram: "Verdik: BELUM" (7 -> 8); kartu 4,0 -> 8,6; angka kunci "15 pelanggan Rp15.252.000" vs README contoh "18 pelanggan Rp16.125.000" | Telegram "belum lulus" bertentangan dengan kartu; angka beda kasus | - | S (kata); A (verdik/angka) |
| kelayakan-investasi-usaha | Kartu "NPV 12% Rp109.237.735; balik modal 1 tahun 1 bulan"; README contoh "NPV Rp60.356.969; balik modal 1 tahun 7 bulan" | **Dua kasus berbeda** tanpa keterangan; "NPV/IRR" | Samakan dengan kasus yang diuji di Telegram (balik modal 1 tahun 1 bulan) | A |
| sunting-tulisan-jelas | README Telegram: 7 -> 7,5 "belum lulus"; kartu 6,25 -> 8,5 | Kartu dan Telegram bertentangan | - | S (kata); A |
| rapikan-data-berantakan | README Telegram: "Hasil: belum lulus" (7 -> 7,5/8); kartu 3,5 -> 9 | idem | - | S (kata); A |
| triase-keluhan-pelanggan | README Telegram: "BELUM DAPAT DINILAI ... pembanding tanpa skill hilang"; "Gelombang 11b" | jargon, verdik belum | "Hasil: belum dapat dinilai" | S (kata); A |
| analisis-selisih-anggaran | README Telegram: 7,5 -> 8 "belum lulus"; kartu 5,75 -> 8,5 | idem | - | S (kata ada di README); A |
| seleksi-cv-pelamar | README Status: "bot Telegram asli (gelombang 14, 2026-10-12)" | jargon | - | S (bagian Telegram), status uji dibersihkan juga |
| triase-email-masuk | README Telegram: 7,5 -> 8 "belum lulus"; kartu 5,5 -> 8 | idem | - | S (kata); A |
| rangkaian-pesan-pelanggan | README: "opt-out `stop`" | "opt-out" belum dijelaskan | "pesan berhenti (balas 'stop')" | S (kata gelombang/verdik); A |
| rapor-mingguan-ai | README Status: "gelombang 13" | jargon | - | S |
| landing-page-siap-tayang | README: "Verdik gelombang: LULUS"; "file `index.html`", "potongan dari `examples/data/hasil-sesudah-v101-s1.html`" | path berkas | path dihapus | S |
| proses-pesanan-wa | README: "tautan pesan tidak tercatat di log ini"; kartu 5,5 -> 8,4 vs Telegram +1,0 | di README sudah dijelaskan, bagus | - | S (kata) |
| checklist-keamanan-pangan-usaha | README: "Verdik uji bot: BELUM"; kartu: "DITAHAN dari promosi" | **lihat P1 no. 2** | - | S (kata); A (P1) |
| simulasi-cicilan-pinjaman | Kartu "4.823.129" tidak di README | angka tak ditemukan | - | A |
| cek-risiko-dan-asuransi-usaha | Kartu "39,4 jt / 15,8 jt" tidak di README (README: kurang Rp4.050.000) | beda kasus | - | A |
| persiapan-jual-atau-wariskan-usaha | README: "dalam konteks kanal Telegram", path `examples/data/pjs-tg-s1-01-sesudah.txt` | path, jargon | "lewat Telegram" | S |
| cari-prospek-web | README: "pencarian yang teliti bisa memakan beberapa menit (... sekitar 18 menit)" | Tidak instan; sudah jujur | - | bersih |
| satu-lawan-satu-dan-umpan-balik | README tabel Tanpa/Dengan | bagus | - | bersih |
| ubah-draf-ke-dokumen | README Telegram: "sebut nama skill ini bila Anda ingin alur 'rapikan draf'" | Meminta pembeli menyebut nama skill; ini mengakui kelemahan; kartu 5,63 -> 8,28 | - | A |
| kartu-belajar-anki | README: "21 kartu" di contoh vs "16 kartu utuh" di Telegram; "tab pemisah ... hilang" | **Angka kartu beda** (21 vs 16) dalam README yang sama | konfirmasi mana yang benar | A |
| panduan-wawancara-kerja | README: Telegram 6 -> 8,5, paragraf sangat panjang | kalimat panjang, "dasar hukumnya belum dicocokkan" | Pecah paragraf | A (isi bukti uji; tidak diubah) |
| rencana-restok-barang | README: tiga versi uji (1.0.2, 1.0.3, 1.0.4) | Riwayat versi di bukti uji; "lead time" | "lama kirim" | A |
| bandingkan-pemasok-vendor | README: "skor gabungan (86,5 vs 85,8, 'hampir seri') tampil tanpa penjelasan bobotnya" | Mengakui kelemahan; sudah jujur | - | bersih |
| hitung-thr | Kartu: "Lulus tipis (rata-rata tepat 8,0)"; "nama usaha karangan" | jargon | - | A |
| pph-final-umkm | Kartu: "agent sempat memindai disk (find /)" | jargon | "sempat menelusuri seluruh isi komputer uji" | A |
| buat-invoice | Kartu: "nama berkas HTML tidak sama dengan nomor invoice" | OK | - | A (kecil) |
| arus-kas-13minggu | Kartu: "S5 tanpa skill tidak menghasilkan jawaban"; "find /"; "/tmp" | kode skenario "S5", path | "pada satu skenario, AI tanpa skill tidak menjawab dalam 3 percobaan" | A |
| harga-jual-marketplace | Kartu: "argumen tool call tidak diperiksa"; README contoh Shopee margin | jargon | - | A |
| listing-marketplace | Kartu: "len", "505 padahal 515 karakter" | detail pengujian yang tidak perlu | hapus | A |
| balas-ulasan-pelanggan | Kartu: "924 karakter vs 469 karakter" dll.; "`cek_balasan.py --faskes`" | sangat teknis | ringkas | A |
| pengingat-pasien-klinik | README Telegram: "versi terkini 1.0.9, sedangkan versi yang tampil di bot saat uji itu bukan 1.0.9" ; kartu "exec", "kode 2" | kalimat membingungkan; kartu teknis | "Uji dilakukan pada versi lama; perbaikan sesudahnya belum diuji ulang di Telegram." | A (isi bukti uji) |
| promo-kalender | Kartu "Regresi" | jargon | - | A |
| rekap-penjualan-csv | Kartu "regresi", "1.2.2" | jargon | - | A |
| kalender-pajak | Kartu "KAP 411128/411125" disebut "mengarang"; "tool call" | jargon | - | A |
| pantau-pasar-kripto | Kartu: banyak nama berkas dan "Skor 7 / 3 / 6" | lihat pola | - | A |
| riset-harga-kompetitor | Kartu: "skor tanpa skill dibatasi 5 karena dua salah hitung"; "P25/P75" | aturan batas skor internal | "Tanpa skill ada dua salah hitung" | A |

## Yang sudah diperbaiki langsung (README di luar 29 skill)

Perubahan kalimat saja (tanpa angka/verdik baru), di bagian sebelum/sesudah, "Bukti uji di bot Telegram", beberapa kalimat lain yang menyebut "gelombang N", dan satu-dua kalimat spesifik:

- Ganti `: (pesan di grup uji internal Komunitech) - skor X` menjadi `: skor X`; bila skor memang tidak dicatat menjadi `skor tidak dicatat`.
- Hapus "gelombang N" / "gelombang uji N (satu putaran uji di bot)" dari baris "Diuji di bot OpenClaw asli ...".
- "Verdik ... : LULUS/BELUM" menjadi "Hasil: lulus/belum lulus" (nilai verdik tidak diubah).
- Hapus "(tautan pesan ... tidak tercatat ...)"; "versi repo saat itu/uji" menjadi "versi skill saat itu/uji"; hapus "di catatan uji/gelombang".
- Nama berkas skrip di cuplikan (`hitung_pkwt.py`, `jadwal_onboarding.py`, `cek_pola.py`) menjadi "alat hitung bawaan skill"/dihapus; path `examples/...` pada beberapa cuplikan diganti "folder `examples/`" atau dihapus.
- Satu kalimat penjelas `--ya` ditambahkan di `vikunja-tugas`, `grist-usaha`, `inventree-gudang`.
- `rencana-pelajaran-guru`: "JP (jam pelajaran)" dan kalimat contoh versi awal diperjelas. `actual-budget-usaha`: "AI modern" -> "AI zaman sekarang". `siyuan-sop`: "mesin inti" dihapus.

README yang diubah (43): actual-budget-usaha, aktifkan-kembali-pelanggan, analisis-selisih-anggaran, cek-privasi-openclaw, checklist-keamanan-pangan-usaha, edukasi-pasien-klinik, grist-usaha, inventree-gudang, kalkulator-klinis-nakes, karyawan-ai-mulai, katalog-reseller, kelayakan-investasi-usaha, kontrak-kerja-pkwt, landing-page-siap-tayang, laporan-status-kantor, lowongan-kerja, luncurkan-produk-baru, naskah-live-jualan, pengajuan-kur, pengingat-follow-up, pengingat-pasien-klinik, perjanjian-sederhana, persiapan-jual-atau-wariskan-usaha, proses-pesanan-wa, rangkaian-pesan-pelanggan, rapikan-data-berantakan, rapor-mingguan-ai, rencana-pelajaran-guru, seleksi-cv-pelamar, siyuan-sop, slip-gaji-bpjs, sop-onboarding, spesifikasi-produk-usaha, strategi-konten-iklan, strategi-merek-usaha, sunting-tulisan-jelas, surat-peringatan-karyawan, tangani-keberatan-pelanggan, triase-email-masuk, triase-keluhan-pelanggan, tulisan-tanpa-kesan-ai, uji-pasar-produk-cepat, vikunja-tugas. Satu commit per README (`git log --grep "QA promosi"`).

Yang sengaja TIDAK diubah di README karena menyangkut angka/verdik/isi contoh: kutipan hasil uji (skor, selisih), tulisan "belum lulus" (verdik asli tetap), blok JSON di `notebook-riset-lokal`, contoh `listmonk-newsletter`, paragraf panjang `panduan-wawancara-kerja`, riwayat versi di `rencana-restok-barang`.

## Untuk Akun B

### 1. Daftar 29 skill gelombang Telegram: temuan

Semua README di bawah **tidak saya sentuh**. Usulan kalimat diberikan; angka/verdik hanya untuk dicek.

| Skill | Kutipan | Masalah | Usulan |
|---|---|---|---|
| ekstrak-nota-faktur | README Telegram: "Tanpa skill skor 4,5 -> dengan skill skor 7,5 (selisih +3, belum lulus acuan kami: skor dengan skill di bawah 8)"; kartu 6,0 -> 9,0 | Verdik "belum lulus" di bukti uji vs kartu 9,0; paragraf Telegram sangat panjang dan mengulang diri; "Uji internal (lokal, berkas di folder kerja wajar): 5,5-6 -> 9" | Beri satu kalimat: "Di Telegram, file Excel belum terkirim ke chat; kami sedang memperbaiki"; hapus pengulangan "Catatan jujur ... Tanpa skill ..." |
| rencana-marketing-usaha | "Catatan jujur ... Satu label di jawaban dengan skill keliru: tertulis 'target laba Rp8.000/pelanggan'" | Mengaku label salah; "selisih +1,5, tepat di batas lulus acuan kami" | Pertahankan jujur, tetapi sederhanakan "acuan lulus kami" menjadi "batas minimal selisih 1,5 poin" |
| arsip-nota | "Perbandingan ini tidak bersih: kedua sisi memakai folder nota yang sama ... Akan diuji ulang dengan folder terpisah" | Pengakuan uji tidak adil dalam bukti uji untuk pembeli; kartu 5,75 -> 8,75 | Tahan sampai uji ulang, atau tulis ringkas "uji ulang menyusul" |
| iterasi-dari-masukan-pelanggan | "Tanpa skill skor 6 -> dengan skill skor 5 (selisih -1 ...)"; "meski angka salah (12 pesan, 38 masukan ...; yang benar 13, 39, 5 dari 7)" | **Skill kalah di bot dan angka salah** tetapi kartu 5,9 -> 8,5 tampil dan README contoh memakai angka "13 chat" | P1: tahan atau tunggu uji ulang v1.0.12 |
| audit-akun-iklan | "Tanpa skill skor 7,5 -> dengan skill skor 6 (selisih -1,5)" | **Skill kalah** di Telegram; kartu 6,0 -> 8,5 | P1: tahan atau beri catatan jelas |
| presentasi-instan | "Tanpa skill skor 6,9 -> dengan skill 7,5 ... berkas deck tidak sampai ke chat Telegram"; "masih memuat istilah teknis seperti 'cek otomatis'" | Belum lulus; kartu 6,0 -> 8,5 | P1 |
| cv-lamaran-ats | "Tanpa skill 7 -> 8 (selisih +1, belum lulus)"; "Skor kata kunci (mis. 45%) hanya hitungan kata sederhana" | belum lulus; kartu 6,0 -> 8,5 | P1 |
| balas-chat-cs | Kartu catatan "Uji pertama BELUM karena janji karangan; lulus setelah revisi" | jargon BELUM/Uji pertama | "Versi awal sempat memberi janji yang tidak ada; sudah diperbaiki." |
| foto-produk-brief | Kartu "Uji awal sempat BELUM" | jargon | idem |
| analisis-excel | Kartu "uji awal v1.0.x sempat BELUM (7,25->7,75)"; angka "Total gaji Rp29.550.000 (subtotal ikut terhitung = Rp51.000.000)" tidak ada di README | jargon; angka tak ditemukan | ringkas; samakan contoh |
| tagih-piutang | Kartu "Lolos tipis (selisih +1,6). Script keliru membaca kolom 'sdh bayar'... Kata proses ('script', 'skill ini') sesekali bocor." ; "examples/HASIL-UJI.md" | jargon, path, mengaku cacat | ringkas |
| pantau-cron-openclaw | Kartu "1.0.0 BELUM 5,25->6,75; 1.0.1 BELUM 4,75->7,5; 1.0.2 LULUS tipis 8,19"; "Gateway"; "token masih bocor di sebagian jawaban" | riwayat versi, jargon | hanya hasil terbaru |
| gaji-umkm | Kartu angka "Rp5.708.150 ... Rp6.526.950" tidak di README; "Sisi dengan skill belum menyebut lokasi file CSV/slip dan tenggat setor" | angka beda kasus | samakan |
| surat-penawaran-harga | Kartu "Satu kali router mengembalikan panggilan alat rusak dan diulang" | jargon berat | hapus |
| notulen-rapat | Kartu "'2,1M' dibaca Rp2.100.000.000" ; README Telegram "'2,1M' sebagai Rp2.100.000.000" | Angka mutlak bergantung konteks (sewa forklift); sudah ada "Catatan jujur" | Pertahankan |
| analisis-rasio-keuangan-usaha | Kartu "Rasio lancar 1,66" tidak ada di README (README: 1,30x dan 0,89x) | angka beda kasus | samakan |
| surat-resmi | Kartu "Hari acara: 'Jumat' -> Sabtu, 17 Oktober 2026"; README contoh RT 03 | beda kasus | samakan |
| resi-picking | Kartu `5,77E+17` | notasi ilmiah Excel tidak dimengerti | "nomor resi panjang tidak rusak jadi 5,77E+17" |
| audit-seo-toko-online | Kartu "Title 118 karakter -> 51 karakter; meta description kosong -> 132 karakter" tak ada di README (README: 36 karakter) | beda kasus | samakan |
| tender-checklist | Kartu angka (Rp234.487.500, Rp236.600.000) tidak ada di README (README: Rp39.750.000) | beda kasus | samakan |
| dasbor-lokal, copy-landing-page, studio-video-pendek-ai, strategi-harga-produk, follow-up-prospek, peringatan-dini-operasional, laporan-insiden-usaha, sop-writer | `angka_kunci` kosong atau berbeda kasus dari contoh README | Tidak ada masalah berat | - |
| positioning-persona-usaha | Kartu "Bio 159-219 karakter (terpotong) -> 142 dari 150"; README Telegram sangat panjang ("Rincian persona ... baru muncul bila Anda membalas 'lengkap'") | Paragraf Telegram panjang & detail | pecah |
| gaji-umkm, sop-writer | Kartu catatan "Skor sebelum dari uji pertama" | jargon "uji pertama" | - |

Pola yang sama di README 29 skill itu: "Verdik ..." / "Hasil" tanpa "gelombang" sudah tidak dipakai oleh banyak (tertulis "Diuji ... dengan pesan yang sama"), tetapi **semua** README bagian Telegram 16 Okt memuat paragraf satu blok 1.000+ karakter yang sulit dibaca; usulan: pecah menjadi 3 butir (Skor / Yang dilakukan dengan skill / Yang dilakukan tanpa skill / Catatan jujur).

### 2. Masalah angka dan verdik (lintas semua 118 skill)

| Item | Detail | Usulan |
|---|---|---|
| Verdik Telegram "belum lulus" atau skill kalah, padahal kartu tampil | audit-akun-iklan (7,5 -> 6), iterasi-dari-masukan-pelanggan (6 -> 5), pph21-ter (8 -> 6 pada 1.0.4), ekstrak-nota-faktur (4,5 -> 7,5), presentasi-instan (6,9 -> 7,5), cv-lamaran-ats (7 -> 8), arsip-nota (7 -> 8), laporan-status-kantor (4,5 -> 5), ubah-draf-ke-dokumen (7 -> 8), kartu-belajar-anki (7,5 -> 8), sunting-tulisan-jelas (7 -> 7,5), analisis-selisih-anggaran (7,5 -> 8), triase-email-masuk (7,5 -> 8), rangkaian-pesan-pelanggan (7,5 -> 8,75), rapikan-data-berantakan (7 -> 7,5), triase-keluhan-pelanggan (7,5 -> 8,5), aktifkan-kembali-pelanggan (7 -> 8), persiapan-jual-atau-wariskan-usaha (7 -> 7,5), proses-pesanan-wa (7,5 -> 8,5), checklist-keamanan-pangan-usaha (7 -> 7,5), notebook-riset-lokal (6,5 -> 7), perjanjian-sederhana (6 -> 6,5, gelombang 5) | Keputusan lead/pemilik: tahan kartu, atau tambah di kartu satu kalimat jujur ("Di bot Telegram sungguhan selisihnya lebih kecil: ...") |
| `lolos_promosi` true padahal keputusan menahan | laporan-status-kantor (keputusan 19a), checklist-keamanan-pangan-usaha (`catatan_jujur` sendiri "DITAHAN dari promosi") | set `lolos_promosi` false atau hapus kalimat "ditahan" setelah diperbaiki |
| Selisih jsonl tidak cocok dengan skor | perjanjian-sederhana selisih 3,75 (seharusnya 4,75); checklist-keamanan-pangan-usaha 2,6 (2,65) | betulkan di jsonl |
| `angka_kunci` memakai kasus berbeda dari contoh README | hledger-usaha (laba Rp7.865.500 vs Rp1.600.000), program-referral-loyalitas (biaya referral Rp42.500 vs Rp30.000), kelayakan-investasi-usaha (NPV Rp109.237.735 / 1 th 1 bln vs Rp60.356.969 / 1 th 7 bln), aktifkan-kembali-pelanggan (15 pelanggan Rp15.252.000 vs 18 pelanggan Rp16.125.000), spt-tahunan-op (Rp14.400.000 vs Rp5.700.000), strategi-konten-iklan (43 pesanan vs 84), spesifikasi-produk-usaha, atur-keuangan-pribadi, simulasi-cicilan-pinjaman, cek-risiko-dan-asuransi-usaha, laporan-iklan-mingguan, analisis-rasio-keuangan-usaha, audit-seo-toko-online, tender-checklist, gaji-umkm | Tambahkan keterangan kasus di kartu ("pada uji kasus toko X") atau pakai angka kasus yang sama dengan README |
| Angka kartu tidak ditemukan di README sama sekali | katalog-reseller (Rp86.000), frappe-books-usaha (605.000), riset-saham-berita (550-575, PBV 1,07), kalkulator-klinis-nakes (150 mg), pph21-ter (Rp220.000, Rp5.955.000), persiapan-jual-atau-wariskan-usaha (Rp96,9-251,9 jt), rekap-penjualan-csv (Rp3.038.000, 44,4%), promo-kalender (Rp36.070, Rp62.300, Rp12.574), riset-harga-kompetitor (Rp58.000, Rp15.038, Rp54.825), balas-ulasan-pelanggan (karakter), proses-pesanan-wa (Rp54.375, Rp255.625) | Angka berasal dari berkas uji; boleh, tetapi cek kebenaran dan satu kasus dengan README |
| Skor di kartu tidak ditemukan di README | kanboard-papan-kerja (9), strategi-konten-iklan (6,5 dan 9), cek-risiko-dan-asuransi-usaha (8,6), sop-writer (8,75) | cek apakah README harus menyebut skor yang sama |
| Versi diuji berbeda dari versi README | Hampir semua (jsonl `versi_teruji` < versi README); paling jauh: kelayakan-investasi-usaha (1.0.1 vs 1.0.6), agen-cs-toko (1.0.7 vs 1.0.11), slip-gaji-bpjs (1.0.5 vs 1.0.8), copy-landing-page (1.0.4 vs 1.0.7), panduan-wawancara-kerja (1.0.0 vs 1.0.3), simulasi-cicilan-pinjaman (1.0.1 vs 1.0.4) | wajar, tetapi untuk perubahan besar tulis "perubahan sesudahnya belum diuji ulang" di kartu |
| README tanpa bagian "Bukti uji di bot Telegram" | 64 dari 118 (mis. siyuan-sop, kontrak-kerja-pkwt, spt-tahunan-op, hitung-thr, buat-invoice, arus-kas-13minggu) | tidak wajib; hanya catatan |
| Angka di README vs jsonl (angka skor) | Tidak ada ketidakcocokan skor "tanpa/dengan" yang jelas selain di atas | - |

## Skill tanpa temuan berarti (hanya kata kecil)

umami-analitik, laporan-harian-usaha, buku-piutang, absensi-lokal, kasir-lokal, cari-prospek-web, satu-lawan-satu-dan-umpan-balik, bandingkan-pemasok-vendor.
