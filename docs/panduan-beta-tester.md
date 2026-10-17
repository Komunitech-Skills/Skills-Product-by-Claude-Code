# Panduan Beta Tester Komunitech Skills

Versi 17 Oktober 2026 (revisi setelah pemeriksaan ulang oleh tim)

Terima kasih sudah bersedia menjadi beta tester. Panduan ini ditulis untuk Anda yang bukan orang teknis: ikuti hari demi hari, satu langkah sekali waktu. Setiap langkah punya **tanda berhasil** supaya Anda yakin sudah di jalur yang benar.

## Daftar periksa singkat

- [ ] Terima file ZIP paket beta (khusus Anda, jangan dibagikan).
- [ ] Ekstrak ZIP, pasang skill ke folder "skills" AI agent Anda (bagian 3).
- [ ] Pilih **minimal 3 skill** dari 10 skill beta yang cocok dengan usaha Anda (bagian 5).
- [ ] Pakai tiap skill pilihan untuk **pekerjaan nyata minimal 3 kali** selama 7 hari.
- [ ] Catat setiap pemakaian: tanggal, skill, kalimat perintah, hasil bisa langsung dipakai atau tidak, hal yang salah/aneh.
- [ ] Hari ke-7: isi formulir masukan untuk **tiap skill** yang dicoba (bagian 7), kirim paling lambat 1 hari sesudah hari ke-7 lewat jalur masukan di bagian 7 (topik Telegram beta, atau kontak admin Komunitech bila Anda tidak memakai Telegram).

## 1. Apa itu Program Beta dan berapa lama?

Program Beta Tester Komunitech bertujuan menguji skill di tangan pengguna sungguhan (pengusaha dan profesional awam) sebelum skill dijual. Untuk Program Beta VIP ini dipilih **10 skill** yang sudah lulus pengujian tim Komunitech dan sudah dicoba langsung lewat bot Telegram OpenClaw (tiga skill tambahan di bagian 5 belum dicoba di bot Telegram). Di panduan ini, **bot Anda** berarti agen OpenClaw yang Anda ajak bicara lewat Telegram. Yang kami butuhkan sekarang: skill itu dipakai untuk **pekerjaan nyata** Anda.

- **Masa uji:** **7 hari sejak Anda menerima ZIP**. Kirim masukan paling lambat **1 hari sesudah hari ke-7**. (Khusus penerima paket 13 Oktober 2026: masa uji 13–19 Oktober, kirim paling lambat 20 Oktober.)
- **Target:** pilih **minimal 3 skill** yang cocok dengan usaha Anda (tidak harus semua 10), pakai masing-masing **minimal 3 kali** untuk pekerjaan nyata.
- **Hari ke-7:** isi formulir (±5 menit per skill) untuk tiap skill yang dicoba; kirim paling lambat 1 hari sesudahnya.
- **Imbalan (bukan uang):** akses lebih awal ke skill-skill berikutnya sebelum dirilis; prioritas untuk permintaan skill dari Anda; dan, hanya bila Anda setuju, nama atau nama usaha Anda dicantumkan di daftar terima kasih. Diberikan setelah formulir masukan Anda diterima. Tidak ada imbalan uang atau potongan harga, dan kami tidak menjanjikan hasil tertentu dari pemakaian skill.

Di laporan tim, masukan Anda ditulis sebagai ringkasan tanpa nama (Beta 1, Beta 2, dst.) dan menentukan apakah skill direvisi lagi atau langsung dirilis. Catatan: saat Anda mengirimnya di Telegram, nama akun Anda terlihat (lihat bagian 7).

> ### Yang kami butuhkan dari Anda
> 1. **Instal sendiri** tanpa bantuan, dan catat di langkah mana (jika) tersendat.
> 2. **Minimal 3 skill, masing-masing minimal 3 kali** untuk pekerjaan nyata Anda.
> 3. **Catatan tiap pemakaian:** tanggal, skill, kalimat perintah, hasil bisa langsung dipakai atau tidak, hal yang salah/aneh (tempel contohnya, hapus data pribadi/pelanggan).
> 4. **Formulir masukan per skill** di hari ke-7; kirim paling lambat 1 hari sesudahnya.
> 5. **Laporan** bila bot menjawab aneh, salah hitung, atau menolak permintaan wajar.

## 2. Apa yang Anda terima?

Satu file ZIP paket VIP beta, khusus Anda, dengan nama seperti `komunitech-vip-beta-budi-a1b2c3d4e5f6.zip` (berisi nama Anda dan kode lisensi Anda; ukuran sekitar 10 MB, bisa sedikit berubah). Unduh dan ekstrak ZIP ini di komputer, bukan di HP: isinya lebih dari 100 folder yang sulit dibuka di ponsel. Isinya:

- **Satu folder per skill** (di dalamnya langsung ada `SKILL.md`), termasuk 10 skill beta.
- **`PANDUAN-BETA-TESTER.html`** (dan `PANDUAN-BETA-TESTER.md`, isinya sama) — panduan ini, supaya selalu ada di tangan Anda. Buka yang `.html` dengan klik dua kali (terbuka di browser).
- **`CARA-INSTAL.md`** — panduan umum untuk semua paket Komunitech, bukan khusus beta. **Untuk uji ini, abaikan bagian "Cara cepat: satu perintah" di dalamnya** (juga saran menyalin seluruh folder skill sekaligus): itu memasang semua skill sekaligus. Ikuti bagian 3 panduan ini (salin hanya folder skill yang Anda pilih). Catatan: README beberapa skill menyebut `docs/instalasi.md`; di paket Anda berkas itu bernama `CARA-INSTAL.md`.
- **`LISENSI.txt`** — kode lisensi, nama pemegang, daftar skill beserta versinya, dan teks lisensi.
- Folder `docs`, `solusi-vip` (panduan OpenClaw per profesi), dan `templates` (contoh teks aturan kerja bot OpenClaw) bukan skill dan tidak perlu dipasang; boleh dibaca bila Anda ingin memakai panduan per profesi. **Jangan** disalin ke folder skills; yang dipasang ke folder skills hanya folder skill.

Paket ini **khusus untuk Anda**: diberi tanda pengenal tersembunyi (watermark) berisi nama dan kode lisensi Anda, dan tiap `SKILL.md` berisi keterangan "Dilarang menyebarluaskan". Mohon tidak dibagikan ke siapa pun.

## 3. Cara pasang singkat

Skill adalah folder berisi `SKILL.md`. Memasangnya = menyalin folder skill ke folder "skills" milik AI agent Anda, lalu minta tolong seperti biasa; AI memakai skill otomatis bila relevan. Platform = aplikasi AI yang Anda pakai: OpenClaw (umumnya member VIP), Claude Code, OpenAI Codex, atau Cursor. **Terminal** = jendela tempat Anda mengetik perintah di komputer; cara seret folder di bawah tidak memerlukannya.

**Buka ZIP dulu:** Windows klik kanan ZIP → Extract All; Mac klik dua kali ZIP. Yang disalin nanti adalah **folder skill-nya** (yang langsung berisi `SKILL.md`), bukan folder pembungkus hasil ekstrak. Di dalam hasil ekstrak juga ada folder `docs`, `solusi-vip`, dan `templates` yang letaknya sejajar dengan folder skill: **jangan diseret ke folder skills**, cukup dibaca bila perlu. Biarkan `LISENSI.txt`, `CARA-INSTAL.md`, dan `PANDUAN-BETA-TESTER.*` tetap di folder hasil ekstrak; semuanya tidak perlu disalin ke folder skills. Jangan memakai "Cara cepat: satu perintah" di `CARA-INSTAL.md`: itu menyalin seluruh isi ZIP ke folder skills.

**Cara termudah menyalin folder** (tanpa Terminal):

Windows:
1. Tekan tombol Windows + R.
2. Tempel alamat folder tujuan persis seperti di bagian aplikasi Anda di bawah (OpenClaw / Claude Code / Codex / Cursor), mis. `%USERPROFILE%\.claude\skills\` (`%USERPROFILE%` adalah alamat folder pengguna Anda, biasanya `C:\Users\NamaAnda`; ketik apa adanya, Windows yang menerjemahkan).
3. Tekan Enter.
4. Seret folder skill ke jendela yang terbuka.

Bila muncul pesan folder tidak ada: tekan Windows + R, ketik `%USERPROFILE%`, Enter. Di jendela yang terbuka klik kanan → New → Folder, beri nama sesuai aplikasi Anda, mis. `.claude` (dengan titik di depan), buka folder itu, lalu buat folder `skills` di dalamnya. Ulangi langkah Windows + R dengan alamat lengkap.

Mac:
1. Di Finder tekan Cmd + Shift + G.
2. Tempel alamat folder tujuan, mis. `~/.claude/skills`.
3. Tekan Enter.
4. Seret folder skill ke sana.

Catatan: folder yang namanya diawali titik (`.claude`, `.openclaw`) disembunyikan Mac; tekan Cmd + Shift + . (titik) agar tampak.

Memakai lebih dari satu platform: salin ke masing-masing folder tujuan.

### OpenClaw (utama — semua member VIP memakai ini)

Folder tujuan Mac/Linux: `~/.openclaw/skills/` (bisa diisi dengan cara seret folder di atas). Windows: bila OpenClaw Anda berjalan lewat WSL (fitur Windows untuk menjalankan Linux; bila Anda tidak tahu apa itu WSL, anggap Anda tidak memakainya), pakai cara Terminal di bawah. Windows tanpa WSL belum kami uji: tulis "Perlu bantuan" lewat jalur masukan di bagian 7 dan tanyakan folder skills yang dipakai OpenClaw Anda; tim akan memberi alamatnya. Cara paling andal adalah lewat Terminal:

1. Buka Terminal. Mac: tekan Cmd + Spasi, ketik Terminal, lalu Enter. Windows: bila OpenClaw Anda berjalan lewat WSL (fitur Windows untuk menjalankan Linux), buka jendela WSL yang Anda pakai untuk OpenClaw.
2. Masuk ke folder hasil ekstrak (`cd` artinya pindah ke folder): ketik `cd ` (dengan spasi) lalu seret folder hasil ekstrak ke jendela Terminal, lalu tekan Enter. Di WSL, folder Windows ditulis dengan awalan `/mnt/c/`, mis. `cd /mnt/c/Users/NamaAnda/Downloads/nama-folder-hasil-ekstrak` (huruf c kecil, pakai garis miring biasa). Sebaiknya ekstrak ZIP ke folder Downloads agar alamatnya mudah ditebak; ketik `ls` (artinya: tampilkan isi folder) untuk melihat nama folder yang ada.
3. Jalankan `openclaw skills install ./kelayakan-investasi-usaha --global` (ganti dengan nama skill yang dipasang; ulangi per skill). `--global` memasang skill ke folder `~/.openclaw/skills/` Anda, sama seperti menyalin folder secara manual.
4. Cek dengan `openclaw skills list` (diketik di Terminal/jendela WSL di komputer tempat OpenClaw berjalan — bukan di chat Telegram). Skill terbaca pada pesan berikutnya.

**OpenClaw Anda berjalan di komputer lain (VPS atau mini PC)?** Kirim folder skill yang Anda pilih ke komputer itu (dengan cara yang biasa Anda pakai untuk memindah berkas), lalu jalankan langkah 3–4 di komputer itu. Tidak tahu caranya? Tulis "Perlu bantuan" lewat jalur masukan di bagian 7; tim akan memandu.

Bila Terminal terasa sulit, tulis "Perlu bantuan" lewat jalur masukan di bagian 7 — tim akan memandu.

### Claude Code

- Folder tujuan Mac/Linux: `~/.claude/skills/`; Windows: `%USERPROFILE%\.claude\skills\`
- Salin folder skill ke sana dengan cara seret folder di atas. Jangan ekstrak seluruh ZIP langsung ke folder skills: itu memasang lebih dari 100 skill sekaligus beserta folder `docs`, `solusi-vip`, dan `templates`, padahal untuk uji ini cukup skill yang Anda pilih.
- Jika folder skills baru dibuat, buka sesi baru (atau ketik `/reload-skills`). Cek: ketik `/skills`.

### OpenAI Codex

- Folder tujuan Mac/Linux: `~/.agents/skills/`; Windows: `%USERPROFILE%\.agents\skills\`
- Salin folder skill ke sana. Skill terbaca pada pesan berikutnya; bisa juga dipanggil langsung dengan mengetik tanda dolar diikuti nama skill, mis. `$kelayakan-investasi-usaha`. Cek: ketik `/skills`.

### Cursor

- Folder tujuan Mac/Linux: `~/.cursor/skills/`; Windows: `%USERPROFILE%\.cursor\skills\`
- Pakai chat Agent di aplikasi Cursor di komputer Anda, bukan Cloud Agent atau jadwal otomatis (Automation) Cursor: di sana skill dari folder pribadi tidak otomatis terbaca.
- Setelah memasang, buka chat Agent baru (atau restart Cursor). Cursor juga membaca folder skill Claude Code dan Codex (`~/.claude/skills`, `~/.agents/skills`), jadi jangan pasang skill yang sama di beberapa folder itu sekaligus agar tidak dobel. Cek: ketik `/` diikuti nama skill di chat Agent, atau lihat di sidebar Customize → Skills.

**Python (program pembantu hitung; hanya untuk skill yang memakainya):** Mac dan Linux umumnya sudah punya Python. Di Windows, pasang gratis dari python.org (pilih versi 3 terbaru) dan centang kotak "Add Python to PATH" di jendela instalasi. Anda tidak perlu mengetik perintah apa pun; bot yang menjalankan programnya. Bila bot bertanya nama perintah Python di Windows, jawab `python`. Tanpa Python, skill hitungan tetap berjalan tetapi angkanya dihitung AI secara manual — sebaiknya Anda cek ulang; khusus `pantau-cron-openclaw` wajib Python 3 (tanpa Python pengawas tidak bisa dipasang).

**Masalah umum:** skill tidak muncul → pastikan `SKILL.md` ada langsung di dalam folder skill (bukan di dalam folder pembungkus) dan mulai percakapan baru (OpenClaw lewat Telegram: cukup kirim pesan baru ke bot Anda; Claude Code, Codex, atau Cursor: buka sesi/chat baru). Skill tidak dipakai otomatis → sebut kebutuhan lebih jelas atau panggil namanya (mis. "pakai skill kelayakan-investasi-usaha").

## 4. Alur 7 hari

### Hari 1 — Pasang dan coba 1 skill

1. Unduh ZIP ke komputer (bukan ke HP) dan buka (ekstrak). **Tanda berhasil:** Anda melihat banyak folder (lebih dari 100 — itu seluruh paket VIP Anda), file `PANDUAN-BETA-TESTER.html`, `CARA-INSTAL.md`, dan `LISENSI.txt`. Cari sepuluh folder skill beta berdasarkan nama di bagian 5 (mis. `kelayakan-investasi-usaha`); folder lainnya adalah skill VIP Anda yang lain dan boleh diabaikan selama uji. Folder `docs`, `solusi-vip` (panduan OpenClaw per profesi), dan `templates` (contoh teks aturan kerja bot OpenClaw) bukan skill dan tidak perlu dipasang; boleh dibaca bila Anda ingin memakai panduan per profesi.
2. Pasang **satu** skill dulu, misalnya `kelayakan-investasi-usaha`, dengan cara di bagian 3. **Tanda berhasil:** nama skill muncul saat dicek — OpenClaw: `openclaw skills list` (diketik di Terminal/jendela WSL di komputer tempat OpenClaw berjalan — bukan di chat Telegram); Claude Code atau Codex: ketik `/skills`; Cursor: ketik `/` diikuti nama skill di chat Agent.
3. Mulai percakapan baru (OpenClaw lewat Telegram: cukup kirim pesan baru ke bot Anda; Claude Code, Codex, atau Cursor: buka sesi/chat baru) dan tempel: `Hitung kelayakan beli mesin kopi Rp25 juta, omzet tambahan Rp4 juta per bulan`. **Tanda berhasil:** bot menjawab tegas layak / kurang layak / tidak layak lengkap dengan balik modal. Bila bot bertanya balik (mis. biaya bulanan), jawab semuanya dalam satu pesan; tanda berhasilnya tetap sama. Bila bot hanya menjawab umum tanpa kata "balik modal" (artinya skill tidak dipakai), tulis "skill tidak terpanggil" di catatan Anda, lalu minta dengan menyebut namanya: "pakai skill kelayakan-investasi-usaha". (Bila muncul "dihitung manual, mohon dicek", berarti Python belum terpasang; lihat catatan Python di bagian 3.) Kalimat uji ini hanya untuk memastikan skill terpasang; yang dinilai adalah pemakaian untuk pekerjaan nyata Anda.
4. Catat di buku atau catatan HP: tanggal, nama skill, kalimat perintah, hasil bisa langsung dipakai atau tidak, dan hal yang salah/aneh. **Tanda berhasil:** catatan pertama Anda sudah ada.

### Hari 2–6 — Pakai untuk pekerjaan nyata

5. Pilih **minimal 3 skill** dari daftar di bagian 5 yang cocok dengan usaha Anda, lalu pasang semuanya. **Tanda berhasil:** ketiganya muncul di daftar skill.
6. Setiap hari, kerjakan 1–2 pekerjaan sungguhan dengan skill itu. Cukup kalimat biasa di chat; kalau bot mengajukan beberapa pertanyaan, jawab semuanya dalam satu pesan balasan. **Tanda berhasil:** hasilnya benar-benar Anda pakai (dikirim, dicetak, atau jadi dasar keputusan).
7. Catat tiap pemakaian seperti langkah 4. **Tanda berhasil:** di akhir Hari 6, tiap skill pilihan punya minimal 3 catatan.
8. Bila bot menjawab aneh atau salah hitung, tempel contohnya di catatan (hapus nama/nomor pelanggan). Pertanyaan teknis boleh langsung ditulis lewat jalur masukan di bagian 7 (topik Telegram beta dengan menandai pemilik Komunitech, atau kontak admin Komunitech). **Tanda berhasil:** contoh masalah tersimpan di catatan Anda tanpa data pribadi.

### Hari 7 — Kirim masukan, paling lambat 1 hari sesudahnya

9. Isi formulir di bagian 7 **untuk tiap skill yang dicoba** (±5 menit per skill), lalu kirim lewat jalur masukan di bagian 7. **Tanda berhasil:** satu formulir terkirim untuk tiap skill yang Anda coba.

## 5. Sepuluh skill fokus

Tempel kalimat di bawah apa adanya ke chat bot Anda, lalu ganti angka dan nama sesuai keadaan usaha Anda. **Bagian dalam [kurung siku] adalah isian: ganti seluruhnya, termasuk tanda kurungnya, dengan data Anda** (mis. `[produk]` diganti `kopi susu`). Catatan: `pantau-cron-openclaw` dan `cek-privasi-openclaw` **hanya untuk OpenClaw**; delapan skill lain berformat sama sehingga seharusnya bisa dipasang di Claude Code, Codex, atau Cursor, tetapi kami baru menguji di OpenClaw; laporan Anda dari platform lain sangat berharga.

**1. `pantau-cron-openclaw` — Laporan Terjadwal Gagal? Kabar Masuk ke Telegram.** Jadwal/laporan otomatis OpenClaw yang terlambat atau hilang ketahuan dan Anda dikabari lewat Telegram. Tugas 7 hari: periksa jadwal otomatis bot Anda, pasang pengawas, yaitu pencatat yang memberi kabar ke Telegram bila jadwal otomatis bot terlambat (bot menampilkan rencana dan meminta "ya" sebelum mengubah jadwal). Perlu: hanya OpenClaw, Telegram terhubung, Python 3 (wajib). Catatan jujur: kabar HILANG sudah terbukti tiba di Telegram pada uji kami 13 Okt 2026, dan alur pemasangan lewat chat (bot menampilkan rencana → Anda balas "ya") berhasil di bot uji kami pada 16 Okt 2026 dengan versi sebelumnya; versi yang Anda terima belum tuntas kami uji di bot. Bot akan menjalankan satu uji peringatan dulu — laporkan apakah pesan uji itu sampai ke Telegram Anda (ini masukan paling berharga untuk skill ini).
- `Pantau laporan harian 21.00 dan piutang 07.45 Senin-Jumat saya. Kabari ke Telegram kalau gagal.`
- `Job mana yang terlambat hari ini?` (job = jadwal otomatis bot Anda)

**2. `rapor-mingguan-ai` — Rapor Mingguan untuk Karyawan AI Anda.** Rapor satu layar atas percakapan bot dengan pelanggan: nilai A–D, kesalahan tersering, tren, dan teks perbaikan siap tempel. Tugas 7 hari: minta rapor mingguan pekerjaan bot. Perlu: salin sendiri 10–20 percakapan bot–pelanggan sebagai teks biasa (hapus nomor kartu dan data sensitif); Python tidak wajib.
- `Tolong buatkan rapor bot saya minggu ini. Ini percakapannya. Bot saya baru dua minggu.` (tempel percakapannya)
- `Ini rapor minggu lalu dan percakapan minggu ini. Naik atau turun?`

**3. `cek-privasi-openclaw` — Cek Privasi OpenClaw dalam Bahasa Awam.** Laporan merah/kuning/hijau atas pengaturan keamanan dan privasi OpenClaw; perbaikan ditawarkan satu per satu dengan izin Anda. Tugas 7 hari: audit privasi setelan bot sendiri. Perlu: hanya OpenClaw. Bila bot menjawab tidak bisa menjalankan perintah, itu normal: bot akan menuliskan perintahnya, lalu Anda salin dan jalankan di Terminal komputer tempat OpenClaw berjalan (atau tulis "Perlu bantuan" lewat jalur masukan di bagian 7). Tanpa Python.
- `cek privasi saya`
- `amankah OpenClaw saya?`

**4. `kelayakan-investasi-usaha` — Cek Layak Investasi Sebelum Keluar Uang.** Jawaban tegas layak / kurang layak / tidak layak untuk beli mesin, buka cabang, atau beli kendaraan usaha, lengkap balik modal, omzet minimal, uji "kalau meleset", dan batas aman. Tugas 7 hari: hitung kelayakan 1 rencana beli alat/cabang. Tidak untuk saham, kripto, reksa dana, atau deposito. Perlu: Python 3 disarankan. Tanpa Python, bot menghitung manual (mohon dicek ulang) dan tidak menampilkan IRR, yaitu persentase keuntungan tahunan investasi.
- `Buka cabang modal 250 juta, omzet tahun pertama 380 juta, kapan balik modal?`
- `Lebih untung beli mobil box 180 juta atau tetap sewa 6,5 juta sebulan?`

**5. `simulasi-cicilan-pinjaman` — Tahu Harga Asli Cicilan Sebelum Tanda Tangan.** Dari angka penawaran kredit: cicilan per bulan, total bunga, bunga efektif setara per tahun (termasuk admin/provisi/asuransi), jadwal angsuran, dan batas cicilan aman dari gaji. Tugas 7 hari: bandingkan 2 tawaran kredit. Perlu: Python 3 disarankan (tanpa Python: dihitung manual, mohon dicek).
- `Motor 25 juta, DP 20%, 3 tahun, bunga 0,8% per bulan. Cicilannya berapa? Mahal nggak?`
- `Pinjam 30 juta, cicilannya 1,5 juta selama 24 bulan. Bunganya sebenarnya berapa persen?`

**6. `cek-risiko-dan-asuransi-usaha` — Cek Risiko Usaha, Tahu Perlu Asuransi atau Tidak.** Tabel risiko usaha, langkah murah minggu ini, keputusan perlu asuransi atau tidak per risiko, dan target dana darurat. Tugas 7 hari: peta risiko + target dana darurat usaha. Perlu: Python opsional (tanpa Python dihitung manual dengan rumus yang sama); tidak masuk ke akun bank/asuransi/BPJS.
- `Kafe saya di ruko dekat sungai, 3 karyawan, apa risikonya dan perlu asuransi apa?`
- `Berapa dana darurat usaha yang ideal?` (sebutkan biaya tetap bulanan: sewa, gaji, listrik, cicilan, dan kas cadangan sekarang)

**7. `seleksi-cv-pelamar` — Seleksi Puluhan CV dalam Hitungan Menit.** Peringkat CV per kriteria dengan kutipan bukti, shortlist, pertanyaan wawancara, dan draf pesan untuk pelamar. Tugas 7 hari: saring 3–10 CV lowongan nyata. Simpan CV di komputer sendiri dan hapus setelah proses. Perlu: CV harus berupa teks yang ditempel ke chat. Bila pelamar mengirim PDF yang tulisannya bisa disalin, buka PDF-nya, salin seluruh teksnya, lalu tempel ke chat; jangan mengirim file PDF ke bot. CV berupa foto/scan tidak terbaca — minta pelamar mengirim versi teks. Python tidak wajib.
- `Ini 12 CV untuk admin toko online. Pilih 5 terbaik dan siapkan pertanyaan wawancaranya.` (tempel CV-nya)
- `Bikinin pesan untuk yang lolos dan yang belum cocok.`

**8. `satu-lawan-satu-dan-umpan-balik` — Siapkan Obrolan Empat Mata dengan Karyawan.** Naskah ucapan dan pesan WA untuk obrolan empat mata, teguran halus, rencana 30 hari karyawan baru, dan pengumuman ke tim. Tugas 7 hari: siapkan 1 sesi empat mata dengan karyawan. Perlu: tidak ada (tanpa Python, akun, atau program tambahan).
- `Saya nggak enak negur kasir yang sering telat.`
- `Buatkan agenda obrolan empat mata 30 menit dengan staf gudang saya.`

**9. `tangani-keberatan-pelanggan` — Jawab "Mahal" dan "Mikir Dulu" Tanpa Memaksa.** 2–3 balasan WA siap kirim untuk keberatan "mahal", "mikir dulu", "tanya suami/bos", "takut tipu", "pesaing lebih murah", plus satu pertanyaan lanjutan. Tugas 7 hari: balas 3 keberatan harga/pesaing sungguhan; Anda yang mengirim balasan satu per satu. Bila Anda belum menyebut data produk, bot menulis tanda `[isian: ...]` di balasannya; ganti seluruh tanda itu (termasuk kurungnya) dengan data Anda sebelum dikirim ke pelanggan. Perlu: Python opsional (untuk hitungan harga per hari dan cicilan).
- `Pelanggan bilang 'kemahalan kak'. Aku jual [produk] Rp[harga].` (ganti isinya, contoh lengkap: `Pelanggan bilang 'kemahalan kak'. Aku jual kopi susu Rp35.000.`)
- `Klien jawab 'saya pikir-pikir dulu'. Gimana balasnya?`

**10. `landing-page-siap-tayang` — Landing Page Jadi dan Tayang Hari Ini.** Satu file web `index.html` utuh (tampil rapi di HP, tombol WhatsApp dengan pesan terisi, FAQ). Plus panduan langkah demi langkah menayangkannya gratis lewat layanan seperti Netlify Drop, GitHub Pages, atau Cloudflare Pages (hosting = tempat menyimpan halaman agar bisa dibuka orang lewat internet) dan cara memasang nama domain (alamat web Anda, mis. tokoanda.com). Tugas 7 hari: buat 1 halaman promo produk, lalu tayangkan. Ganti bagian bertanda `[isian: ...]` (mis. `[isian: harga]`) sebelum tayang; versi file bisa diminta dengan membalas "kirim file". Perlu: Anda sendiri yang mengunggah file ke hosting; Python tidak wajib.
- `Buatkan landing page jasa servis AC saya, WA 0812-3456-7890.`
- `Bagaimana pasang domain ke landing page ini?`

**Tambahan (opsional): tiga skill baru di ZIP Anda.** Tidak wajib diuji, tetapi bila sempat, masukan Anda sangat membantu. Formatnya sama dengan 10 skill di atas, jadi seharusnya bisa dipasang di platform lain; tetapi kami baru menguji di OpenClaw dan belum lewat bot Telegram.

- `bandingkan-pemasok-vendor` — Pilih Pemasok Paling Untung, Bukan Paling Murah. Kalimat: `Tolong bandingin 3 balasan WA supplier [bahan] ini, butuh [jumlah] paling lambat [N] hari lagi:` lalu tempel chat pemasoknya.
- `rencana-restok-barang` — Rencana kulakan dari data penjualan. Kalimat: `Ini penjualan 90 hari plus stok sekarang toko [jenis toko], minggu ini harus kulakan apa dan berapa?` lalu tempel tabel penjualan, atau letakkan berkas tabel (CSV; dari Excel: Save As → CSV) di folder kerja bot.
- `panduan-wawancara-kerja` — Pertanyaan dan rubrik wawancara siap pakai. Kalimat: `Buatkan pertanyaan wawancara dan rubrik skor untuk [posisi], wawancara [durasi] menit, [N] pewawancara.`

## 6. Aturan main

- **Yang dinilai adalah pekerjaan nyata.** Kalimat contoh di panduan ini hanya untuk memastikan skill terpasang; untuk penilaian, pakai skill pada pekerjaan sungguhan minimal 3 kali per skill.
- **Data Anda sendiri, tanggung jawab Anda sendiri.** Simpan di komputer sendiri, hapus nomor kartu dan data sensitif sebelum menempel, dan periksa hasil sebelum dipakai untuk keputusan uang, karyawan, atau pelanggan. Hasil skill bukan nasihat keuangan, hukum, asuransi, atau medis; keputusan akhir tetap di tangan Anda.
- **Jangan sebar paket.** ZIP diberi tanda pengenal tersembunyi (watermark) berisi nama dan kode lisensi Anda; `SKILL.md` di dalamnya memuat keterangan "Dilarang menyebarluaskan".
- **Laporkan bila bot menjawab aneh**, salah hitung, atau menolak permintaan wajar: tempel contohnya, hapus data pribadi/pelanggan dulu. Itu justru masukan paling berharga.
- **Tidak harus 10 skill.** Minimal 3 yang cocok; skill lain di dalam ZIP boleh dicoba, tetapi fokus penilaian pada 10 skill beta.
- **Privasi.** Hasil audit privasi tidak dikirim ke Komunitech, CV tidak dikirim ke mana pun oleh skill, dan hitungan berjalan di komputer Anda sendiri; yang kami terima hanya jawaban yang Anda kirim lewat jalur masukan di bagian 7. Seperti pemakaian bot biasa, isi chat (termasuk CV atau percakapan yang Anda tempel) tetap diproses oleh penyedia model AI yang Anda pilih sendiri (mis. Anthropic/OpenAI), bukan oleh Komunitech; karena itu hapus data sensitif sebelum menempel. Di laporan tim, masukan hanya ditulis sebagai ringkasan tanpa nama (Beta 1, Beta 2, dst.), dan testimoni hanya dikutip dengan izin tertulis Anda. Ingat: saat Anda mengirim di Telegram, nama akun Anda terlihat (lihat bagian 7).

## 7. Cara dan tenggat mengirim masukan

**Tenggat: hari ke-7 masa uji Anda; kirim masukan paling lambat 1 hari sesudahnya.** (Penerima paket 13 Oktober 2026: hari ke-7 = 19 Oktober, kirim paling lambat 20 Oktober.)

**Di mana mengirim (pilih salah satu):**

- **Telegram (jalur utama):** topik yang namanya diawali **"Beta VIP — panduan tester"** di grup Telegram Komunitech tempat Anda diundang. Untuk menandai pemilik Komunitech, balas pesan pembuka di topik itu, atau ketik `@` lalu pilih nama yang disebut di pesan pembuka. Bila lebih nyaman, kirim lewat pesan pribadi (japri) ke pemilik Komunitech: ketuk nama pengirim pesan pembuka di topik itu, lalu pilih "Kirim Pesan".
- **Bila Anda tidak memakai Telegram:** kirim lewat kontak admin Komunitech yang biasa Anda hubungi: [KONTAK ADMIN]. Tulisan dalam kurung siku itu diisi oleh pengirim paket; bila masih tertulis apa adanya, tanyakan kontaknya ke orang yang mengirim paket ini.

**Siapa yang bisa melihat jawaban Anda:** jawaban di topik Telegram terlihat oleh pemilik Komunitech dan anggota lain di grup itu, lengkap dengan nama akun Telegram Anda; jawaban lewat pesan pribadi (japri) atau kontak admin hanya terlihat oleh penerimanya. Jadi jawaban Anda **tidak anonim saat dikirim**. Di laporan tim, kami hanya menulis ringkasan tanpa nama (Beta 1, Beta 2, dst.). Mohon tidak menempel data pribadi atau data pelanggan di jawaban.

- **Selama uji:** pertanyaan teknis ditulis lewat jalur yang sama dengan menandai pemilik Komunitech.
- **Hari ke-7:** isi formulir di bawah untuk **tiap skill yang dicoba** (satu formulir per skill), kirim paling lambat 1 hari sesudahnya lewat jalur di atas. Bila tim membagikan Google Form, boleh lewat itu.

**Formulir masukan (salin, isi per skill).** Tulis nama skill di baris pertama jawaban Anda.

```
1. Platform & OS yang dipakai?
2. Instalasi berhasil tanpa bantuan? (Ya / Perlu bantuan / Gagal — di langkah mana?)
3. Berapa kali dipakai untuk pekerjaan nyata minggu ini?
4. Seberapa berguna hasilnya? (1–5)
5. Seberapa sering hasil bisa langsung dipakai tanpa diedit? (Selalu / Sering / Kadang / Jarang)
6. Lama pekerjaan ini tanpa skill? Dengan skill?
7. Pernah dapat hasil salah/aneh? Ceritakan.
8. Yang paling disukai?
9. Satu hal yang harus diperbaiki?
10. Harga wajar menurut Anda? (Rp0 / Rp29rb / Rp49rb / Rp99rb / Rp149rb+)
11. Boleh dikutip sebagai testimoni? (Ya dengan nama / Ya anonim / Tidak)
12. Boleh nama atau nama usaha Anda dicantumkan di daftar terima kasih program beta? (Ya, nama saja / Ya, nama dan usaha / Tidak) — cukup dijawab di formulir pertama.
```

## 8. FAQ

**Harus mencoba semua 10 skill?**
Tidak. Pilih minimal 3 yang cocok dengan usaha Anda, masing-masing dipakai minimal 3 kali untuk pekerjaan nyata.

**Skill tidak muncul atau tidak dipakai otomatis?**
Pastikan `SKILL.md` ada langsung di dalam folder skill (bukan di dalam folder pembungkus), mulai percakapan baru (OpenClaw lewat Telegram: cukup kirim pesan baru ke bot Anda; Claude Code, Codex, atau Cursor: buka sesi/chat baru), lalu sebut kebutuhan lebih jelas atau panggil nama skill-nya, misalnya "pakai skill kelayakan-investasi-usaha". Di OpenClaw, cek dengan `openclaw skills list` (diketik di Terminal/jendela WSL di komputer tempat OpenClaw berjalan — bukan di chat Telegram).

**Saya pakai Windows, perlu apa?**
Untuk OpenClaw: bila OpenClaw Anda berjalan lewat WSL (fitur Windows untuk menjalankan Linux; bila Anda tidak tahu apa itu WSL, anggap Anda tidak memakainya), jalankan perintah pasang di jendela WSL seperti langkah di bagian 3. Windows tanpa WSL belum kami uji; bila ragu atau Terminal terasa sulit, tulis "Perlu bantuan" lewat jalur masukan di bagian 7, dan tim akan memberi tahu folder skills yang dipakai OpenClaw Anda. Untuk skill hitungan: pasang Python dari python.org dan centang "Add Python to PATH"; tanpa Python skill hitungan tetap jalan, tetapi angka sebaiknya dicek ulang; khusus `pantau-cron-openclaw` wajib Python 3 (tanpa Python pengawas tidak bisa dipasang).

**Muncul "python not found"?**
Pasang Python (Windows dari python.org, centang "Add Python to PATH"), lalu tutup dan buka lagi aplikasi AI Anda (Claude Code, Codex, atau Cursor). Untuk OpenClaw: jalankan ulang OpenClaw di komputer tempat ia berjalan; bila tidak tahu caranya, tulis "Perlu bantuan" lewat jalur masukan di bagian 7.

**Saya pakai Claude Code, Codex, atau Cursor, bukan OpenClaw. Masih berguna ikut?**
Sangat berguna. Ke-10 skill ini kami uji di OpenClaw (termasuk lewat bot Telegram); format skill sama di platform lain, tetapi pengalaman nyata di sana belum kami miliki. Ingat, `pantau-cron-openclaw` dan `cek-privasi-openclaw` hanya untuk OpenClaw.

**Saya hanya punya HP, bisa ikut?**
Pemasangan dilakukan di komputer tempat OpenClaw Anda berjalan, dan ZIP-nya tidak cocok dibuka di ponsel. Bila Anda hanya memakai HP, tulis "Perlu bantuan" lewat jalur masukan di bagian 7; tim akan memandu.

**Apakah hasil audit privasi atau data saya dikirim ke Komunitech?**
Tidak. Hasil audit privasi tidak dikirim ke Komunitech, CV tidak dikirim ke mana pun oleh skill, dan hitungan berjalan di komputer Anda sendiri; yang kami terima hanya jawaban yang Anda kirim lewat jalur masukan di bagian 7 (nama akun Telegram Anda terlihat saat mengirim; di laporan tim kami menuliskannya tanpa nama). Seperti pemakaian bot biasa, isi chat (termasuk CV atau percakapan yang Anda tempel) tetap diproses oleh penyedia model AI yang Anda pilih sendiri (mis. Anthropic/OpenAI), bukan oleh Komunitech; karena itu hapus data sensitif sebelum menempel.

**Apa yang saya dapat setelah program selesai?**
Imbalannya bukan uang: akses lebih awal ke skill-skill berikutnya sebelum dirilis, prioritas untuk permintaan skill dari Anda, dan (hanya bila Anda setuju) nama atau nama usaha Anda di daftar terima kasih. Diberikan setelah formulir masukan Anda diterima. Tidak ada potongan harga, dan kami tidak menjanjikan hasil tertentu dari pemakaian skill.

## 9. Terima kasih

Tujuh hari Anda sangat berarti: dari catatan kecil Anda, skill ini diperbaiki sebelum sampai ke pengusaha dan profesional lain di Indonesia. Selamat mencoba, dan sampai bertemu di jalur masukan (topik Telegram beta).
