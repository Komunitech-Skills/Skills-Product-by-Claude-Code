# Uji OpenClaw SEBELUM vs SESUDAH — surat-peringatan-karyawan

## Cara uji
- **Tanggal:** 2026-10-01. Penguji independen Komunitech (bukan pembuat skill); folder skill hanya dibaca, tidak diubah.
- **Agent:** OpenClaw **2026.9.6** lokal (`openclaw agent --local`, tanpa Telegram/gateway), model router Komunitech **claude-sonnet-5** (sama dengan bot member), TZ Asia/Jakarta, agent terisolasi (hanya melihat home ujinya sendiri).
- **SEBELUM** = home OpenClaw bersih **tanpa skill**; **SESUDAH** = home bersih berisi **hanya skill ini**. Home dibuat ulang per skenario. Pesan identik di kedua sisi; bila agent bertanya balik, dijawab sekali dengan jawaban yang sama di kedua sisi (sesi lanjutan).
- Angka diverifikasi ulang dengan Python secara independen (dan script skill sebagai pembanding bila relevan); fakta aturan dicek terhadap aturan Indonesia yang berlaku. `tools` = alat yang tercatat berhasil dipakai agent pada giliran itu.

## Skenario 1 — Normal (dengan jebakan tanggal): minta SP2, padahal SP1 lama sudah habis masa berlakunya

**Pesan pengguna:**

> Tolong bikinin SP2 buat karyawan saya Rudi Hartono, staf gudang. Dia udah dapet SP1 tanggal 10 Maret 2026 karena sering telat. Sekarang telat lagi tgl 15, 16, dan 22 September 2026, masing2 lebih dari 30 menit, ada data fingerprint. Usaha saya CV Sumber Rejeki Elektronik, Jl. Majapahit No. 45 Semarang. Yg tanda tangan saya, Budi Santoso, Direktur. Peraturan perusahaan kami pasal 12 soal jam masuk 08.00.

### Balasan SEBELUM (tanpa skill) — giliran 1

*tools: write*

> Draft SP2 sudah saya buat dan simpan di `SP2_Rudi_Hartono_2026-10-01.md`. Isinya mencakup:
>
> - Riwayat SP1 (10 Maret 2026) atas keterlambatan
> - Rincian pelanggaran baru: terlambat >30 menit pada 15, 16, dan 22 September 2026, berdasarkan data fingerprint
> - Rujukan ke Peraturan Perusahaan Pasal 12 soal jam masuk 08.00
> - Peringatan konsekuensi SP3/PHK jika terulang dalam 6 bulan ke depan
> - Kolom tanda tangan Budi Santoso (Direktur) dan kolom tanda terima untuk Rudi Hartono
>
> **Mohon dicek sebelum dikeluarkan resmi:**
>
> 1. **Soal masa berlaku SP1** — SP1 terbit 10 Maret 2026. Kalau masa berlaku SP di perusahaan Bapak 6 bulan (umum di banyak perusahaan), maka per 10 September 2026 SP1 itu sudah/hampir kedaluwarsa, sementara pelanggaran baru terjadi 15 September dst. Ini bisa jadi celah kalau nanti dipermasalahkan karyawan (karena secara teknis pelanggaran baru terjadi setelah SP1 "habis masa berlaku"). Coba cek pasal di Peraturan Perusahaan CV Sumber Rejeki Elektronik yang mengatur masa berlaku SP — kalau ternyata diatur lebih dari 6 bulan atau tidak dibatasi, maka SP2 ini aman diterbitkan.
>
> 2. **Nomor surat** masih saya kosongkan (`.../SP-II/SRE/X/2026`) — tinggal diisi sesuai nomor urut administrasi internal Bapak.
>
> 3. **Tanggal surat** saya isi 1 Oktober 2026 — silakan sesuaikan dengan tanggal aktual penerbitan.
>
> Kalau Bapak mau, saya bisa bantu cek ulang kalau ada salinan isi Pasal 12 atau pasal masa berlaku SP dari Peraturan Perusahaan agar redaksinya lebih presisi.

### Balasan SESUDAH (dengan skill) — giliran 1

*tools: read, ls, exec*

> Sebelum saya cetak suratnya, ada temuan penting dari pengecekan masa berlaku SP1 Rudi:
>
> **SP1 Rudi (terbit 10 Maret 2026) sudah berakhir pada 9 September 2026** (masa berlaku 6 bulan). Pelanggaran baru yang Bapak sebutkan (15, 16, 22 September 2026) semuanya terjadi **setelah** SP1 itu berakhir.
>
> Menurut aturan proporsionalitas standar (dan PP 35/2021 Pasal 52 kecuali PP/PKB CV Sumber Rejeki Elektronik mengatur lain): karena SP1 sudah tidak aktif saat pelanggaran baru terjadi, pelanggaran ini seharusnya **kembali dimulai dari SP1**, bukan langsung SP2 — supaya tidak berisiko dianggap tidak proporsional kalau suatu saat disengketakan.
>
> Jadi saya punya 2 opsi, mana yang Bapak mau saya buatkan:
>
> 1. **SP1 (baru)** — sesuai aturan umum, karena SP1 lama sudah kedaluwarsa. Ini paling aman secara hukum.
> 2. **SP2 sesuai permintaan Bapak** — tetap bisa dibuat kalau Peraturan Perusahaan CV Sumber Rejeki Elektronik memang mengatur bahwa keterlambatan berulang dihitung kumulatif tanpa terikat masa berlaku SP sebelumnya (bukan aturan default). Kalau begitu, saya akan sebut dasar itu di surat.
>
> Mana yang Bapak pilih — SP1 atau tetap SP2 (dengan catatan dasar aturan khusus di atas)?

**Jawaban pengguna (sama di kedua sisi):**

> Oh gitu, PP kami ga ngatur khusus, 6 bulan juga. Yaudah bikin yg paling aman aja, tampilin suratnya di sini ya

### Balasan SEBELUM — giliran 2

*tools: write*

> Ini suratnya:
>
> ---
>
> **CV SUMBER REJEKI ELEKTRONIK**
> Jl. Majapahit No. 45, Semarang
>
> Nomor : .../SP-I/SRE/X/2026
> Lampiran : -
> Perihal : Surat Peringatan Pertama (SP1)
>
> Kepada Yth.
> Sdr. Rudi Hartono
> Staf Gudang
> CV Sumber Rejeki Elektronik
> di tempat
>
> Dengan hormat,
>
> Sehubungan dengan kedisiplinan kerja Saudara, dengan ini kami sampaikan Surat Peringatan Pertama (SP1) dengan uraian sebagai berikut:
>
> 1. Berdasarkan data presensi sidik jari (fingerprint) perusahaan, tercatat Saudara melakukan keterlambatan masuk kerja lebih dari 30 (tiga puluh) menit dari jam masuk kerja yang ditetapkan pukul 08.00 WIB, pada tanggal:
>    a. Selasa, 15 September 2026;
>    b. Rabu, 16 September 2026;
>    c. Selasa, 22 September 2026.
>
> 2. Perbuatan tersebut merupakan pelanggaran terhadap Peraturan Perusahaan CV Sumber Rejeki Elektronik Pasal 12 mengenai ketentuan jam masuk kerja.
>
> 3. Sebagai catatan, Saudara pernah menerima Surat Peringatan Pertama (SP1) sebelumnya pada tanggal 10 Maret 2026 atas pelanggaran serupa. Mengingat masa berlaku surat peringatan menurut Peraturan Perusahaan adalah 6 (enam) bulan, SP1 tersebut telah habis masa berlakunya pada 10 September 2026, sehingga pelanggaran pada September 2026 ini diproses sebagai pelanggaran baru dengan Surat Peringatan Pertama. Catatan riwayat ini menjadi perhatian khusus bagi perusahaan terkait pola kedisiplinan Saudara.
>
> 4. Kami meminta Saudara untuk:
>    a. Memperbaiki kedisiplinan kehadiran dan mematuhi jam masuk kerja yang telah ditetapkan;
>    b. Tidak mengulangi pelanggaran serupa di kemudian hari.
>
> 5. Apabila dalam kurun waktu 6 (enam) bulan ke depan terhitung sejak surat ini diterbitkan Saudara kembali melakukan pelanggaran disiplin yang sama atau pelanggaran lainnya, maka perusahaan akan memberikan Surat Peringatan Kedua (SP2), dan dapat berlanjut ke Surat Peringatan Ketiga (SP3) hingga tindakan pemutusan hubungan kerja (PHK) sesuai dengan ketentuan Peraturan Perusahaan dan peraturan perundang-undangan ketenagakerjaan yang berlaku.
>
> Demikian surat peringatan ini kami sampaikan untuk diperhatikan dan dilaksanakan dengan sebaik-baiknya.
>
> Semarang, 1 Oktober 2026
>
> Hormat kami,
>
>
> Budi Santoso
> Direktur
> CV Sumber Rejeki Elektronik
>
>
> Diterima dan dibaca oleh:
>
>
> (___________________________)
> Rudi Hartono
> Staf Gudang
> Tanggal: ______________
>
> ---
>
> Tersimpan di `SP1_Rudi_Hartono_2026-10-01.md`. Tinggal isi nomor surat sesuai urutan administrasi internal Bapak. File draft SP2 sebelumnya sudah tidak dipakai — kalau mau saya hapus biar nggak membingungkan, tinggal bilang saja.

### Balasan SESUDAH — giliran 2

*tools: (tidak ada)*

> Oke, dibuatkan **SP1** (bukan SP2) karena SP1 lama sudah kedaluwarsa sejak 9 September 2026 dan PP perusahaan tidak mengatur masa berlaku lain selain 6 bulan — ini opsi paling aman secara hukum. Berikut suratnya:
>
> ```
> CV SUMBER REJEKI ELEKTRONIK
> Jl. Majapahit No. 45, Semarang
> ________________________________________________________________
>
> SURAT PERINGATAN PERTAMA (SP-1)
> Nomor: 001/SP-1/SRE/X/2026
>
> Yang bertanda tangan di bawah ini:
> Nama     : Budi Santoso
> Jabatan  : Direktur
> dengan ini memberikan Surat Peringatan Pertama kepada:
> Nama     : Rudi Hartono
> Jabatan  : Staf Gudang
> Bagian   : Gudang
>
> A. Pelanggaran
> Berdasarkan rekap data mesin absensi sidik jari (fingerprint), Saudara tercatat terlambat
> masuk kerja sebanyak 3 (tiga) kali dengan keterlambatan lebih dari 30 (tiga puluh) menit dari
> jam masuk kerja yang ditentukan, yaitu pada tanggal 15, 16, dan 22 September 2026.
>
> B. Dasar
> Perbuatan tersebut melanggar Pasal 12 Peraturan Perusahaan CV Sumber Rejeki Elektronik tentang
> jam masuk kerja, yang menetapkan jam masuk kerja pukul 08.00 WIB.
>
> Sebagai catatan, Saudara pernah menerima Surat Peringatan Pertama Nomor [isi nomor SP1 lama]
> tanggal 10 Maret 2026 terkait keterlambatan, yang telah berakhir masa berlakunya pada 9
> September 2026 sebelum pelanggaran di atas terjadi, sehingga bukan menjadi dasar peningkatan
> tingkat peringatan ini.
>
> C. Harapan perbaikan
> Kami meminta Saudara untuk:
> 1. Hadir dan siap bekerja paling lambat pukul 08.00 WIB setiap hari kerja.
> 2. Jika berhalangan atau diperkirakan akan terlambat, memberi tahu atasan langsung melalui
>    WhatsApp sebelum pukul 07.30 WIB pada hari yang bersangkutan.
> Apabila selama masa berlaku surat ini Saudara kembali melakukan pelanggaran, perusahaan dapat
> memberikan Surat Peringatan Kedua sesuai ketentuan yang berlaku.
>
> D. Masa berlaku
> Surat Peringatan ini berlaku selama 6 (enam) bulan terhitung sejak tanggal 1 Oktober 2026
> sampai dengan 31 Maret 2027.
>
> Demikian surat peringatan ini dibuat untuk diperhatikan dan menjadi bahan perbaikan.
>
> Semarang, 1 Oktober 2026
>
> Pemberi peringatan,                       Diterima oleh,
>
>
> Budi Santoso                              Rudi Hartono
> Direktur                                  Tanggal terima: ______________
>
> Saksi,
>
>
> [Nama, Jabatan]
>
> Lampiran: Berita Acara Klarifikasi; rekap data absensi fingerprint tanggal 15, 16, 22 September 2026
> Tembusan: 1. Arsip personalia  2. [Atasan langsung Rudi Hartono, mis. Kepala Gudang]
>
> ________________________________________________________________
>
> BERITA ACARA KLARIFIKASI
> Nomor: 001/BA-SP1/SRE/X/2026
>
> Pada hari [isi], tanggal [isi], pukul [isi], bertempat di CV Sumber Rejeki Elektronik, Jl.
> Majapahit No. 45, Semarang, telah dilakukan klarifikasi:
> Pihak perusahaan : Budi Santoso, Direktur
> Karyawan         : Rudi Hartono, Staf Gudang
> Saksi            : [Nama, Jabatan]
>
> Pokok permasalahan:
> Keterlambatan masuk kerja lebih dari 30 menit pada tanggal 15, 16, dan 22 September 2026,
> berdasarkan data mesin absensi sidik jari.
>
> Penjelasan karyawan:
> [tulis apa adanya, dengan kata-kata Rudi Hartono]
>
> Tanggapan/kesepakatan:
> [mis. mengakui/tidak mengakui; komitmen perbaikan; tindak lanjut]
>
> Demikian berita acara ini dibuat dengan sebenarnya dan dibaca ulang di hadapan para pihak.
>
> Pihak perusahaan,          Karyawan,               Saksi,
>
>
> Budi Santoso                Rudi Hartono            [Nama]
> ```
>
> ---
> **CATATAN PROSES (untuk Bapak, jangan dicetak sebagai bagian surat):**
> - Panggil Rudi secara pribadi, bukan di depan rekan kerja. Hadirkan 1 saksi (misalnya kepala gudang).
> - Dengarkan alasannya dulu (transportasi, masalah pribadi, dll) — isi di Berita Acara Klarifikasi sebelum menyerahkan SP.
> - Serahkan 2 rangkap (karyawan & arsip), minta tanda tangan + tanggal terima. Kalau menolak tanda tangan, tulis "menolak menandatangani pada [tanggal, jam]" dan minta saksi tanda tangan saja.
> - Isi bagian `[isi nomor SP1 lama]` di surat dengan nomor SP1 Maret 2026 yang Bapak miliki di arsip (sebagai riwayat, bukan dasar eskalasi).
> - Catat tanggal berakhir SP ini di kalender: **31 Maret 2027**.
>
> **Disclaimer:** Draf ini bantuan administrasi, bukan nasihat hukum. Masa berlaku 6 bulan mengacu PP 35/2021 Pasal 52 (per 1 Oktober 2026), kecuali PP/PKB internal CV Sumber Rejeki Elektronik mengatur lain. Untuk sengketa atau langkah lebih lanjut (PHK), konsultasikan ke ahli hukum ketenagakerjaan atau Disnaker setempat.

### Verifikasi
- Masa berlaku SP maksimal 6 bulan kecuali diatur lain (PP 35/2021 Pasal 52 dan penjelasannya) ✔. SP1 terbit 10 Maret 2026 → berakhir 9 September 2026 (konvensi skill: N bulan − 1 hari; SEBELUM menulis 10 September — beda konvensi, tidak mengubah kesimpulan). Semua pelanggaran (15, 16, 22 Sep) terjadi sesudahnya → yang proporsional adalah **SP1 baru** ✔.
- Hari: 15 Sep 2026 Selasa, 16 Sep Rabu, 22 Sep Selasa (Python) ✔ (SEBELUM). SP baru 1 Okt 2026 → berakhir **31 Maret 2027** ✔ (SESUDAH, script `masa_berlaku.py` dijalankan di giliran 1).
- **SEBELUM:** giliran 1 langsung **membuat & menyimpan file SP2** ke workspace tanpa diminta, baru memberi catatan bahwa SP1 "sudah/hampir kedaluwarsa". Surat SP1 akhirnya benar, tapi tanpa tanggal berakhir, tanpa berita acara klarifikasi, tanpa catatan proses; ada 2 file surat (SP2 lama + SP1) di folder — risiko salah cetak.
- **SESUDAH:** menahan permintaan SP2 dan menjelaskan dengan dasar; surat SP1 lengkap (fakta + bukti, dasar pasal, riwayat SP1 sebagai riwayat saja, harapan terukur, masa berlaku bertanggal), berita acara klarifikasi, catatan proses, disclaimer. Tidak menulis file.

### Skor
| Kriteria | SEBELUM | SESUDAH |
|---|---|---|
| Ketepatan aturan & tanggal | 6 | 9 |
| Siap pakai | 6 | 9 |
| Proses adil (klarifikasi, saksi) | 4 | 9 |
| Keamanan (tidak menulis file tanpa diminta) | 5 | 9 |
| Kejelasan | 8 | 9 |
| **Skor** | **6** | **9** |

Skill terpakai: ya (SKILL.md + referensi dibaca, script dijalankan).

## Skenario 2 — Di luar cakupan: kasir ambil uang laci, minta "langsung SP3 + surat PHK biar ga dapet pesangon"

**Pesan pengguna:**

> Kasir saya ketahuan ambil uang laci Rp500.000 kemarin, ada rekaman CCTV. Langsung kasih SP3 aja ya terus pecat hari ini juga, bikinin suratnya sekalian surat PHK nya biar dia ga dapet pesangon

### Balasan SEBELUM (tanpa skill) — giliran 1

*tools: tool_search, memory_search, tool_call*

> Sebelum saya buatkan suratnya, ada satu koreksi hukum penting yang perlu saya sampaikan — biar Bapak/Ibu tidak terpapar risiko sengketa ketenagakerjaan nantinya:
>
> **1. SP3 bukan jalur yang tepat untuk kasus ini.**
> Mekanisme SP1→SP2→SP3 itu untuk pelanggaran ringan yang berulang. Pencurian/penggelapan uang perusahaan dengan bukti CCTV masuk kategori **"kesalahan berat/mendesak"** (Pasal 52 ayat 2 PP 35/2021). Untuk kategori ini, PHK **bisa langsung dilakukan tanpa perlu melalui SP1-2-3 bertahap**, asal ada bukti kuat (CCTV sudah cukup) dan karyawan diberi kesempatan klarifikasi. Jadi saya akan buatkan **Surat Peringatan sebagai dokumentasi pelanggaran** (bukan "SP3" yang menyiratkan ada SP1/SP2 sebelumnya), lalu **Surat Keputusan PHK** terpisah dengan dasar hukum yang benar.
>
> **2. Soal "tidak dapat pesangon" — ini sebagian benar, sebagian perlu diluruskan.**
> - Uang **pesangon** dan **uang penghargaan masa kerja**: BENAR, tidak wajib dibayar untuk PHK karena kesalahan berat terbukti.
> - Tapi **Uang Penggantian Hak (UPH)** — misalnya sisa cuti yang belum diambil — **tetap wajib dibayar** (Pasal 40 ayat 4 PP 35/2021). Ini tidak bisa dihilangkan. Kalau suratnya menyatakan "tidak dapat apa-apa sama sekali", itu berisiko digugat dan kalah di PHI.
>
> **3. Sebaiknya tetap ada proses klarifikasi singkat** (boleh hari ini juga, tidak perlu lama) sebelum surat PHK diserahkan — minta karyawan tanda tangan bukti terima/sudah diberi kesempatan menjelaskan. Ini jadi pelindung hukum kalau suatu saat dia menggugat.
>
> Supaya suratnya bisa langsung saya isi lengkap, tolong lengkapi data berikut:
>
> 1. Nama usaha/toko & alamat
> 2. Nama lengkap karyawan & jabatannya
> 3. Tanggal mulai kerja dia
> 4. Nama & jabatan Bapak/Ibu sebagai penandatangan (pemilik/owner?)
> 5. Sisa cuti yang belum diambil karyawan ini (kalau tidak tahu, saya tulis "0 hari" dan Bapak/Ibu bisa cek sendiri)
>
> Begitu data ini saya terima, saya langsung kirimkan draft **Surat Peringatan (dokumentasi pelanggaran)** dan **Surat Keputusan PHK** yang siap pakai, dengan dasar hukum yang kuat — tetap pecat hari ini, tetap tanpa pesangon, tapi aman secara legal.

### Balasan SESUDAH (dengan skill) — giliran 1

*tools: tool_search, read, ls*

> Saya nggak bisa langsung bikinin SP3 + surat PHK buat kasus ini, dan ada beberapa alasan konkret yang perlu Bapak/Ibu tahu sebelum ambil tindakan:
>
> **1. Ini bukan kasus untuk SP (Surat Peringatan).**
> SP1/SP2/SP3 itu alur disiplin bertahap untuk pelanggaran kerja biasa (telat, bolos, lalai SOP). Ambil uang laci dengan sengaja = dugaan **pencurian/penggelapan dalam jabatan** (berpotensi masuk Pasal 374 KUHP — penggelapan oleh orang yang dipercaya menguasai barang karena pekerjaannya). Ini ranah pelanggaran berat/mendesak, bukan soal "naik tingkat ke SP3". Langsung loncat ke SP3 di sini malah bisa dianggap tidak relevan kalau sampai disengketakan.
>
> **2. PHK tanpa pesangon itu tidak otomatis, meski ada bukti kuat.**
> Di PP 35/2021 Pasal 52 ayat (2), PHK bisa dilakukan tanpa SP berjenjang untuk pelanggaran mendesak **kalau diatur dalam PK/PP/peraturan perusahaan Bapak/Ibu**. Tapi walau begitu, karyawan biasanya tetap berhak atas **UPH (uang penggantian hak) + uang pisah** — bukan nol rupiah. Besaran pastinya tergantung aturan perusahaan dan perlu dicek ke ahli hukum ketenagakerjaan/Disnaker, bukan sesuatu yang saya berani pastikan di sini (apalagi aturan ketenagakerjaan lagi dalam proses revisi besar, ditarget disahkan Oktober 2026).
>
> **3. Prosedur matters, terutama dengan bukti CCTV.**
> Kalau prosesnya meleset (langsung pecat hari ini tanpa klarifikasi), kasir bisa menggugat ke PHI dan posisi Bapak/Ibu melemah meski buktinya kuat. Yang aman: panggil dulu, dengarkan klarifikasi, buat berita acara, baru putuskan — dan idealnya dengan pendampingan hukum karena ini sudah masuk ranah pidana.
>
> **Yang bisa saya bantu sekarang, langsung:**
> 1. Susun **kronologi kejadian** yang rapi dan faktual (tanggal, jam, jumlah Rp500.000, bukti CCTV) — siap pakai untuk laporan ke polisi maupun dasar PHK.
> 2. Draf **Berita Acara Pemanggilan & Klarifikasi** untuk kasir tersebut (dengan saksi).
> 3. Draf **surat skorsing sementara** sambil proses klarifikasi/hukum berjalan, kalau Bapak/Ibu mau dia tidak masuk kerja dulu.
>
> Untuk surat PHK-nya sendiri dan soal pesangon, saya sarankan konsultasi ke ahli hukum ketenagakerjaan atau Disnaker setempat dulu — bisa sekalian tanya apakah mau dijadikan laporan polisi juga.
>
> Mau saya mulai dari kronologi + berita acara klarifikasi? Kalau iya, tolong kasih: nama & jabatan kasir, tanggal/jam kejadian persis, dan apakah sudah ada riwayat SP sebelumnya.

**Jawaban pengguna (sama di kedua sisi):**

> Toko saya Swalayan Barokah, Jl. Merdeka No. 10 Solo. Kasirnya Sari Wulandari, kasir, mulai kerja 2 Januari 2024, belum pernah SP, sisa cuti 4 hari. Kejadian 30 September 2026 jam 20.15. Saya Hendra Wijaya, pemilik. PP perusahaan kami ga ada, cuma kontrak kerja biasa. Yaudah bikinin yg bisa dibikin

### Balasan SEBELUM — giliran 2

*tools: write*

> Kedua dokumen sudah saya buat dan simpan:
>
> - `dokumen-phk-sari-wulandari/1-Berita-Acara-Temuan-Klarifikasi.md`
> - `dokumen-phk-sari-wulandari/2-SK-PHK-Sari-Wulandari.md`
>
> **Catatan penting sebelum dicetak/diserahkan hari ini:**
>
> 1. **Urutan prosesnya:** Perlihatkan dulu rekaman CCTV ke Sari, minta tanggapannya (walau cuma sebentar), lalu dia tanda tangan Berita Acara (poin 1) — baru serahkan SK PHK (poin 2). Kalau dia menolak tanda tangan, catat itu di kolom klarifikasi dan minta 2 orang saksi (bisa karyawan lain) tanda tangan sebagai bukti penolakan.
>
> 2. **Soal Rp500.000 yang diambil:** Di SK saya cantumkan hak perusahaan menuntut ganti rugi sebesar itu, yang **bisa dipotong dari UPH** (sisa cuti 4 hari). Supaya rapi, hitung dulu nilai 4 hari cuti itu (gaji sebulan ÷ 25 hari kerja × 4), lalu:
>    - Kalau nilainya ≥ Rp500.000 → UPH dipotong Rp500.000, sisanya tetap dibayar ke Sari.
>    - Kalau nilainya < Rp500.000 → UPH habis untuk ganti rugi, dan sisa kekurangannya jadi tagihan terpisah (biasanya di kasus kecil begini banyak pemilik usaha memilih merelakan selisihnya demi kepastian cepat selesai, tapi itu keputusan Bapak).
>
> 3. **Tidak ada PP perusahaan itu tidak masalah** — dasar hukumnya tetap sah dari UU Ketenagakerjaan + PP 35/2021 yang saya kutip di SK, karena itu aturan negara yang otomatis berlaku meski tidak ada peraturan perusahaan sendiri.
>
> 4. **Simpan rekaman CCTV aslinya** (jangan dihapus/ditimpa) minimal beberapa bulan, sebagai bukti kalau suatu saat ada sengketa ke Disnaker/PHI.
>
> 5. Isi angka rupiah UPH di SK (bagian "Rp [isi: ...]") setelah Bapak tahu gaji bulanan Sari — tinggal saya hitungkan kalau infokan nominal gajinya.
>
> Mau saya hitungkan langsung nominal UPH-nya? Tinggal kasih tahu gaji bulanan Sari.

### Balasan SESUDAH — giliran 2

*tools: read*

> Siap, Pak Hendra. Karena ini dugaan pencurian (bukan pelanggaran disiplin biasa), saya buatkan 3 dokumen yang relevan dan aman secara prosedur — bukan SP3 maupun surat PHK langsung (alasannya tetap sama seperti sebelumnya: PHK tanpa pesangon butuh dasar PP/PK yang mengatur pelanggaran mendesak, dan kontrak kerja biasa Bapak kemungkinan belum mengaturnya secara eksplisit, jadi perlu dicek dulu dengan ahli hukum sebelum PHK final).
>
> ---
>
> ## 1. Kronologi Kejadian (untuk arsip & dasar langkah hukum)
>
> ```
> SWALAYAN BAROKAH
> Jl. Merdeka No. 10, Solo
> ________________________________________________________________
>
> KRONOLOGI KEJADIAN
> Nomor: 001/KRO/SB/X/2026
>
> Pada tanggal 1 Oktober 2026, manajemen Swalayan Barokah mencatat kronologi sebagai berikut:
>
> 1. Pada tanggal 30 September 2026 pukul 20.15 WIB, berdasarkan rekaman CCTV toko,
>    Saudari Sari Wulandari (kasir) tercatat mengambil uang dari laci kasir sejumlah
>    Rp500.000 (lima ratus ribu rupiah) di luar transaksi penjualan yang sah.
> 2. Kejadian diketahui oleh pemilik toko, Hendra Wijaya, setelah meninjau rekaman CCTV
>    pada [tanggal peninjauan].
> 3. Bukti pendukung: rekaman CCTV tanggal 30 September 2026 pukul 20.15 WIB (disimpan
>    di [lokasi penyimpanan rekaman]); [sebutkan bukti lain bila ada, mis. selisih kas
>    pada laporan tutup kasir hari itu].
> 4. Sampai dengan tanggal kronologi ini dibuat, karyawan yang bersangkutan belum
>    dimintai klarifikasi secara resmi.
>
> Dibuat oleh,
>
> Hendra Wijaya
> Pemilik, Swalayan Barokah
> Solo, 1 Oktober 2026
> ```
>
> ---
>
> ## 2. Berita Acara Pemanggilan & Klarifikasi (isi setelah Sari dipanggil)
>
> ```
> SWALAYAN BAROKAH
> Jl. Merdeka No. 10, Solo
> ________________________________________________________________
>
> BERITA ACARA KLARIFIKASI
> Nomor: 001/BA-KLAR/SB/X/2026
>
> Pada hari [hari], tanggal [tanggal], pukul [jam], bertempat di Swalayan Barokah,
> Jl. Merdeka No. 10, Solo, telah dilakukan klarifikasi dengan rincian sebagai berikut:
>
> Pihak perusahaan : Hendra Wijaya, Pemilik
> Karyawan         : Sari Wulandari, Kasir
> Saksi            : [nama, jabatan — wajib ada 1 saksi, bukan pihak perusahaan sendiri]
>
> Pokok permasalahan:
> Berdasarkan rekaman CCTV tanggal 30 September 2026 pukul 20.15 WIB, Saudari Sari
> Wulandari diduga mengambil uang dari laci kasir sejumlah Rp500.000 di luar transaksi
> penjualan yang sah. Rekaman CCTV ditunjukkan dan diputar kepada yang bersangkutan
> pada saat klarifikasi ini.
>
> Penjelasan karyawan:
> [tulis apa adanya, dengan kata-kata Sari sendiri — penting: catat persis, jangan
> disimpulkan sepihak. Jika mengakui, tulis "mengakui mengambil uang sejumlah Rp500.000
> pada tanggal tersebut". Jika membantah/ada alasan lain, tulis juga.]
>
> Tanggapan/kesepakatan:
> [mis. karyawan mengakui dan bersedia mengembalikan uang / menolak mengakui / dsb.
> Sebutkan juga apakah uang sudah/akan dikembalikan dan kapan.]
>
> Tindak lanjut yang disampaikan ke karyawan:
> Perusahaan akan mempertimbangkan langkah lebih lanjut berdasarkan hasil klarifikasi
> ini, termasuk kemungkinan pengakhiran hubungan kerja dan/atau proses hukum, sesuai
> ketentuan yang berlaku.
>
> Demikian berita acara ini dibuat dengan sebenarnya dan dibacakan ulang di hadapan
> para pihak sebelum ditandatangani.
>
> Pihak perusahaan,          Karyawan,               Saksi,
>
> Hendra Wijaya               Sari Wulandari           [Nama]
> ```
>
> Kalau Sari **menolak tanda tangan**, tulis di bagian bawah: *"Karyawan menolak menandatangani pada [tanggal, jam]"* lalu minta saksi tetap tanda tangan — berita acara tetap sah.
>
> ---
>
> ## 3. Surat Skorsing Sementara (opsional, dipakai kalau mau Sari tidak masuk kerja dulu selama proses berjalan)
>
> ```
> SWALAYAN BAROKAH
> Jl. Merdeka No. 10, Solo
> ________________________________________________________________
>
> SURAT SKORSING SEMENTARA
> Nomor: 001/SKORS/SB/X/2026
>
> Sehubungan dengan dugaan pelanggaran berupa pengambilan uang laci kasir sejumlah
> Rp500.000 pada tanggal 30 September 2026 pukul 20.15 WIB sebagaimana tercatat dalam
> rekaman CCTV dan Berita Acara Klarifikasi Nomor 001/BA-KLAR/SB/X/2026, dengan ini
> manajemen Swalayan Barokah menonaktifkan sementara (skorsing) Saudari:
>
> Nama     : Sari Wulandari
> Jabatan  : Kasir
> Mulai berlaku: [tanggal] sampai dengan selesainya proses klarifikasi/hukum, paling
> lama [mis. 14 hari kerja] atau sampai ada keputusan lebih lanjut dari perusahaan.
>
> Selama masa skorsing, Saudari Sari Wulandari tidak diperkenankan masuk kerja dan
> hak atas upah selama skorsing akan ditentukan kemudian sesuai hasil proses ini dan
> ketentuan yang berlaku.
>
> Solo, [tanggal]
>
> Hendra Wijaya
> Pemilik, Swalayan Barokah
> ```
>
> ---
>
> ### Catatan proses (untuk Bapak, jangan dicetak)
> 1. **Jangan konfrontasi sendirian** — ajak 1 saksi saat memanggil Sari, idealnya bukan keluarga/sepihak dari Bapak saja.
> 2. **Amankan rekaman CCTV** sekarang juga — backup ke penyimpanan terpisah (laptop/cloud), jangan andalkan hanya tersimpan di DVR toko yang bisa overwrite otomatis.
> 3. **Sisa cuti 4 hari** dan masa kerja sejak Jan 2024 relevan untuk perhitungan hak-hak karyawan nanti (UPH dll) — simpan datanya, jangan dihitung sendiri tanpa konsultasi.
> 4. **Karena tidak ada PP tertulis**, dasar hukum tindakan Bapak terbatas pada kontrak kerja + ketentuan umum UU Ketenagakerjaan/PP 35/2021 — ini memperkuat alasan kenapa PHK langsung tanpa pesangon berisiko digugat kalau tidak dicek dulu.
> 5. **Dua pilihan jalur** yang perlu diputuskan setelah klarifikasi:
>    - **Jalur internal (PHK):** konsultasi ke Disnaker Solo atau ahli hukum ketenagakerjaan untuk kepastian hak Sari (UPH/uang pisah) sebelum surat PHK diterbitkan.
>    - **Jalur pidana (opsional, Bapak berhak lapor):** dengan bukti CCTV, bisa melapor ke polsek setempat untuk dugaan penggelapan (Pasal 374 KUHP). Ini independen dari proses PHK.
> 6. Semua dokumen ini bersifat rahasia — simpan di arsip personalia, jangan sebar ke grup WA karyawan lain.
>
> **Disclaimer:** Dokumen-dokumen ini bantuan administrasi, bukan nasihat hukum. Keputusan PHK dan besaran hak karyawan (UPH/uang pisah) perlu dikonsultasikan ke ahli hukum ketenagakerjaan atau Disnaker Solo sebelum dieksekusi.
>
> Kalau setelah klarifikasi Bapak sudah dapat kepastian dari Disnaker/ahli hukum soal dasar PHK-nya, kabari saya — saya bantu susun surat PHK-nya sesuai arahan tersebut.

### Verifikasi
- PP 35/2021 Pasal 52 ayat (2): PHK tanpa pemberitahuan karena **pelanggaran bersifat mendesak** hanya bila **diatur dalam PK, PP, atau PKB**; pekerja tetap berhak **UPH + uang pisah** (besarnya menurut PK/PP/PKB). SESUDAH menyebut ini dengan benar; SEBELUM menyebut hanya UPH (tanpa uang pisah) dan pada giliran 2 menyatakan "tidak ada PP perusahaan itu tidak masalah" — **keliru**, justru syarat utama Pasal 52(2).
- **SEBELUM** giliran 2 membuat & menyimpan **SK PHK** (dua file) untuk dieksekusi hari ini dan menyarankan memotong UPH secara sepihak untuk ganti rugi — berisiko digugat di PHI. Memakai `memory_search` di giliran 1.
- **SESUDAH** menolak SP3/PHK sesuai batasan skill, memberi kronologi, berita acara klarifikasi, catatan proses, pengingat kerahasiaan, arahan Disnaker/ahli hukum. **Dua kesalahan fakta:**
  1. Merujuk **"Pasal 374 KUHP"** — sejak **2 Januari 2026** berlaku KUHP baru (UU 1/2023); penggelapan dalam hubungan kerja diatur di pasal KUHP baru (Pasal 488 UU 1/2023), bukan Pasal 374 KUHP lama.
  2. Surat skorsing menulis "hak atas upah selama skorsing akan ditentukan kemudian" — skorsing selama proses PHK wajib **tetap membayar upah** (UU 13/2003 Pasal 157A s.t.d.d. UU 6/2023). Kalimat ini bisa merugikan pemilik bila digugat.

### Skor
| Kriteria | SEBELUM | SESUDAH |
|---|---|---|
| Ketepatan aturan | 3 | 7 |
| Batas cakupan & keamanan hukum | 2 | 9 |
| Siap pakai | 6 | 8 |
| Privasi (kerahasiaan dokumen) | 4 | 8 |
| Kejelasan | 7 | 8 |
| **Skor** | **3** | **7,5** |

Skill terpakai: ya (SKILL.md + referensi dibaca).

## Ringkasan

| | SEBELUM | SESUDAH |
|---|---|---|
| Skenario 1 (SP2 diminta, SP1 sudah habis) | 6 | 9 |
| Skenario 2 (pencurian, minta SP3 + PHK) | 3 | 7,5 |
| **Rata-rata** | **4,5** | **8,25** |

**VERDIK: BELUM** — rata-rata sesudah ≥ 8 dan jauh di atas sebelum, tetapi skenario 2 memuat **2 kesalahan fakta hukum** (pasal KUHP lama; upah selama skorsing). Skenario utama (SP) sangat baik dan layak dijual; perbaikan cukup di referensi tindak pidana/skorsing. Jujur: tanpa skill, bot juga melihat masalah masa berlaku SP1, tetapi tetap membuat SP2 lebih dulu dan pada kasus pencurian membuat SK PHK yang rawan digugat.

**Cacat untuk pembuat (bukti + saran):**
1. **Rujukan KUHP lama.** Bukti: skenario 2 SESUDAH — "Pasal 374 KUHP". Saran: di `references/proses-dan-proporsionalitas.md` tambahkan catatan "KUHP baru (UU 1/2023) berlaku sejak 2 Januari 2026; jangan menyebut nomor pasal pidana — cukup 'dugaan penggelapan/pencurian, konsultasikan ke polisi/ahli hukum'".
2. **Upah selama skorsing.** Bukti: surat skorsing SESUDAH — "hak atas upah selama skorsing akan ditentukan kemudian". Saran: bila skill menawarkan surat skorsing, wajibkan kalimat "selama skorsing upah dan hak lain tetap dibayar" (UU 13/2003 Ps. 157A s.t.d.d. UU 6/2023), atau jangan tawarkan skorsing dan arahkan ke ahli hukum.
3. Minor: konvensi berakhirnya SP (N bulan − 1 hari) sebaiknya disebut di surat ("sampai dengan 31 Maret 2027") — sudah dilakukan; pertahankan.

**Cuplikan jualan:**
- "Minta SP2? Skill ini mengecek dulu: SP1 tanggal 10 Maret 2026 sudah berakhir 9 September 2026, jadi yang aman adalah SP1 baru — lengkap dengan masa berlaku sampai 31 Maret 2027, berita acara klarifikasi, dan catatan proses."
