# Panduan Beta Tester Komunitech Skills

Versi 13 Oktober 2026

Terima kasih sudah bersedia menjadi beta tester. Panduan ini ditulis untuk Anda yang bukan orang teknis: ikuti hari demi hari, satu langkah sekali waktu. Setiap langkah punya **tanda berhasil** supaya Anda yakin sudah di jalur yang benar.

## Daftar periksa singkat

- [ ] Terima file ZIP paket beta (gratis, khusus Anda, jangan dibagikan).
- [ ] Ekstrak ZIP, pasang skill ke folder "skills" AI agent Anda (bagian 3).
- [ ] Pilih **minimal 3 skill** dari 10 skill beta yang cocok dengan usaha Anda (bagian 5).
- [ ] Pakai tiap skill pilihan untuk **pekerjaan nyata minimal 3 kali** selama 7 hari.
- [ ] Catat setiap pemakaian: tanggal, skill, kalimat perintah, hasil bisa langsung dipakai atau tidak, hal yang salah/aneh.
- [ ] Hari ke-7 (19 Oktober): isi formulir masukan untuk **tiap skill** yang dicoba (bagian 7), kirim paling lambat 20 Oktober di topik Telegram tempat Anda menerima paket ini atau lewat pesan pribadi ke pemilik Komunitech (cara menemukannya ada di bagian 7).

## 1. Apa itu Program Beta dan berapa lama?

Program Beta Tester Komunitech bertujuan menguji skill di tangan pengguna sungguhan (pengusaha dan profesional awam) sebelum skill dijual. Untuk Program Beta VIP ini dipilih **10 skill** yang sudah lulus pengujian tim Komunitech, termasuk dicoba langsung lewat bot Telegram OpenClaw. Yang kami butuhkan sekarang: skill itu dipakai untuk **pekerjaan nyata** Anda.

- **Masa uji:** 7 hari, **13–19 Oktober 2026**. Tenggat kirim masukan: **20 Oktober 2026**.
- **Target:** pilih **minimal 3 skill** yang cocok dengan usaha Anda (tidak harus semua 10), pakai masing-masing **minimal 3 kali** untuk pekerjaan nyata.
- **Hari ke-7 (19 Oktober):** isi formulir 5 menit untuk tiap skill yang dicoba; kirim paling lambat 20 Oktober.
- **Imbalan:** 10 skill yang diuji **gratis selamanya** + **1 skill lain** pilihan Anda (diberikan setelah formulir masukan Anda diterima).

Masukan Anda dirangkum tanpa nama (Beta 1, Beta 2, dst.) dan menentukan apakah skill direvisi lagi atau langsung dirilis.

> ### Yang kami butuhkan dari Anda
> 1. **Instal sendiri** tanpa bantuan, dan catat di langkah mana (jika) tersendat.
> 2. **Minimal 3 skill, masing-masing minimal 3 kali** untuk pekerjaan nyata Anda.
> 3. **Catatan tiap pemakaian:** tanggal, skill, kalimat perintah, hasil bisa langsung dipakai atau tidak, hal yang salah/aneh (tempel contohnya, hapus data pribadi/pelanggan).
> 4. **Formulir masukan per skill** di hari ke-7 (19 Oktober); kirim paling lambat 20 Oktober.
> 5. **Laporan** bila bot menjawab aneh, salah hitung, atau menolak permintaan wajar.

## 2. Apa yang Anda terima?

Satu file ZIP paket VIP beta, **gratis**, dengan nama seperti `komunitech-vip-beta-budi-a1b2c3d4e5f6.zip` (berisi nama Anda dan kode lisensi Anda; ukuran sekitar 9,8 MB). Isinya:

- **Satu folder per skill** (di dalamnya langsung ada `SKILL.md`), termasuk 10 skill beta.
- **`CARA-INSTAL.md`** — panduan pasang lengkap per platform.
- **`LISENSI.txt`** — kode lisensi, nama pemegang, daftar skill beserta versinya, dan teks lisensi.
- Folder `docs`, `solusi-vip` (panduan OpenClaw per profesi), dan `templates` (contoh teks aturan kerja bot OpenClaw) bukan skill dan tidak perlu dipasang; boleh dibaca bila Anda ingin memakai panduan per profesi. **Jangan** disalin ke folder skills; yang dipasang ke folder skills hanya folder skill.

Paket ini **khusus untuk Anda**: diberi tanda (watermark) berupa nama dan kode lisensi Anda, dan tiap `SKILL.md` berisi keterangan "Dilarang menyebarluaskan". Mohon tidak dibagikan ke siapa pun.

## 3. Cara pasang singkat

Skill adalah folder berisi `SKILL.md`. Memasangnya = menyalin folder skill ke folder "skills" milik AI agent Anda, lalu minta tolong seperti biasa; AI memakai skill otomatis bila relevan. Platform = aplikasi AI yang Anda pakai: OpenClaw (umumnya member VIP), Claude Code, OpenAI Codex, atau Cursor.

**Buka ZIP dulu:** Windows klik kanan ZIP → Extract All; Mac klik dua kali ZIP. Yang disalin nanti adalah **folder skill-nya** (yang langsung berisi `SKILL.md`), bukan folder pembungkus hasil ekstrak. Biarkan `LISENSI.txt` dan `CARA-INSTAL.md` tetap di folder hasil ekstrak; keduanya tidak perlu disalin ke folder skills.

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

Folder tujuan Mac/Linux: `~/.openclaw/skills/` (bisa diisi dengan cara seret folder di atas). Windows: bila OpenClaw Anda berjalan lewat WSL (fitur Windows untuk menjalankan Linux), pakai cara Terminal di bawah. Windows tanpa WSL belum kami uji; tulis "Perlu bantuan" di formulir dan tanyakan di topik Telegram tempat Anda menerima paket ini. Cara paling andal adalah lewat Terminal:

1. Buka Terminal. Mac: tekan Cmd + Spasi, ketik Terminal, lalu Enter. Windows: bila OpenClaw Anda berjalan lewat WSL (fitur Windows untuk menjalankan Linux), buka jendela WSL yang Anda pakai untuk OpenClaw.
2. Masuk ke folder hasil ekstrak: ketik `cd ` (dengan spasi) lalu seret folder hasil ekstrak ke jendela Terminal, lalu tekan Enter. Di WSL, folder Windows ditulis dengan awalan `/mnt/c/`, mis. `cd /mnt/c/Users/NamaAnda/Downloads/nama-folder-hasil-ekstrak` (huruf c kecil, pakai garis miring biasa). Sebaiknya ekstrak ZIP ke folder Downloads agar alamatnya mudah ditebak; ketik `ls` untuk melihat nama folder yang ada.
3. Jalankan `openclaw skills install ./kelayakan-investasi-usaha --global` (ganti dengan nama skill yang dipasang; ulangi per skill). `--global` memasang skill ke folder `~/.openclaw/skills/` Anda, sama seperti menyalin folder secara manual.
4. Cek dengan `openclaw skills list` (diketik di Terminal/jendela WSL di komputer tempat OpenClaw berjalan — bukan di chat Telegram). Skill terbaca pada pesan berikutnya.

Bila Terminal terasa sulit, tulis "Perlu bantuan" di formulir dan tanyakan di topik Telegram tempat Anda menerima paket ini — tim akan memandu.

### Claude Code

- Folder tujuan Mac/Linux: `~/.claude/skills/`; Windows: `%USERPROFILE%\.claude\skills\`
- Salin folder skill ke sana dengan cara seret folder di atas. Jangan ekstrak seluruh ZIP langsung ke folder skills: itu memasang lebih dari 100 skill sekaligus beserta folder `docs`, `solusi-vip`, dan `templates`, padahal untuk uji ini cukup skill yang Anda pilih.
- Jika folder skills baru dibuat, tutup dan buka lagi Claude Code. Cek: ketik `/skills`.

### OpenAI Codex

- Folder tujuan Mac/Linux: `~/.agents/skills/`; Windows: `%USERPROFILE%\.agents\skills\`
- Salin folder skill ke sana. Skill terbaca pada pesan berikutnya; bisa juga dipanggil langsung dengan mengetik tanda dolar diikuti nama skill, mis. `$kelayakan-investasi-usaha`. Cek: ketik `/skills`.

### Cursor

- Folder tujuan Mac/Linux: `~/.cursor/skills/`; Windows: `%USERPROFILE%\.cursor\skills\`
- Setelah memasang, buka chat baru (atau restart Cursor). Cursor juga membaca `~/.claude/skills` dan `~/.agents/skills`, jadi jangan pasang skill yang sama di beberapa folder itu sekaligus agar tidak dobel. Cek: ketik `/` di chat, cari nama skill.

**Python (hanya untuk skill yang memakai script):** Mac dan Linux umumnya sudah punya Python. Di Windows, pasang gratis dari python.org dan centang "Add Python to PATH" saat instalasi. Anda tidak perlu mengetik perintah apa pun; bot yang menjalankan script. Bila bot bertanya nama perintah Python di Windows, jawab `python`. Tanpa Python, skill hitungan tetap berjalan tetapi angkanya dihitung AI secara manual — sebaiknya Anda cek ulang; khusus `pantau-cron-openclaw` wajib Python 3 (tanpa Python pengawas tidak bisa dipasang).

**Masalah umum:** skill tidak muncul → pastikan `SKILL.md` ada langsung di dalam folder skill (bukan di dalam folder pembungkus) dan mulai percakapan baru (OpenClaw lewat Telegram: cukup kirim pesan baru ke bot Anda; Claude Code, Codex, atau Cursor: buka sesi/chat baru). Skill tidak dipakai otomatis → sebut kebutuhan lebih jelas atau panggil namanya (mis. "pakai skill kelayakan-investasi-usaha").

## 4. Alur 7 hari

### Hari 1 — Pasang dan coba 1 skill

1. Unduh ZIP dan buka (ekstrak). **Tanda berhasil:** Anda melihat banyak folder (lebih dari 100 — itu seluruh paket VIP Anda), file `CARA-INSTAL.md`, dan `LISENSI.txt`. Cari sepuluh folder skill beta berdasarkan nama di bagian 5 (mis. `kelayakan-investasi-usaha`); folder lainnya adalah skill VIP Anda yang lain dan boleh diabaikan selama uji. Folder `docs`, `solusi-vip` (panduan OpenClaw per profesi), dan `templates` (contoh teks aturan kerja bot OpenClaw) bukan skill dan tidak perlu dipasang; boleh dibaca bila Anda ingin memakai panduan per profesi.
2. Pasang **satu** skill dulu, misalnya `kelayakan-investasi-usaha`, dengan cara di bagian 3. **Tanda berhasil:** nama skill muncul saat dicek — OpenClaw: `openclaw skills list` (diketik di Terminal/jendela WSL di komputer tempat OpenClaw berjalan — bukan di chat Telegram); Claude Code atau Codex: ketik `/skills`; Cursor: ketik `/` di chat lalu cari nama skill.
3. Mulai percakapan baru (OpenClaw lewat Telegram: cukup kirim pesan baru ke bot Anda; Claude Code, Codex, atau Cursor: buka sesi/chat baru) dan tempel: `Hitung kelayakan beli mesin kopi Rp25 juta, omzet tambahan Rp4 juta per bulan`. **Tanda berhasil:** bot menjawab tegas layak / kurang layak / tidak layak lengkap dengan balik modal. (Bila muncul "dihitung manual, mohon dicek", berarti Python belum terpasang; lihat catatan Python di bagian 3.) Kalimat uji ini hanya untuk memastikan skill terpasang; yang dinilai adalah pemakaian untuk pekerjaan nyata Anda.
4. Catat di buku atau catatan HP: tanggal, nama skill, kalimat perintah, hasil bisa langsung dipakai atau tidak, dan hal yang salah/aneh. **Tanda berhasil:** catatan pertama Anda sudah ada.

### Hari 2–6 — Pakai untuk pekerjaan nyata

5. Pilih **minimal 3 skill** dari daftar di bagian 5 yang cocok dengan usaha Anda, lalu pasang semuanya. **Tanda berhasil:** ketiganya muncul di daftar skill.
6. Setiap hari, kerjakan 1–2 pekerjaan sungguhan dengan skill itu. Cukup kalimat biasa di chat; kalau bot mengajukan beberapa pertanyaan, jawab semuanya dalam satu pesan balasan. **Tanda berhasil:** hasilnya benar-benar Anda pakai (dikirim, dicetak, atau jadi dasar keputusan).
7. Catat tiap pemakaian seperti langkah 4. **Tanda berhasil:** di akhir Hari 6, tiap skill pilihan punya minimal 3 catatan.
8. Bila bot menjawab aneh atau salah hitung, tempel contohnya di catatan (hapus nama/nomor pelanggan). Pertanyaan teknis boleh langsung ditulis di topik Telegram tempat Anda menerima paket ini dengan menandai pemilik Komunitech (lihat bagian 7). **Tanda berhasil:** contoh masalah tersimpan di catatan Anda tanpa data pribadi.

### Hari 7 (19 Oktober) — Kirim masukan, paling lambat 20 Oktober

9. Isi formulir di bagian 7 **untuk tiap skill yang dicoba** (±5 menit per skill), lalu kirim di topik Telegram tempat Anda menerima paket ini atau lewat pesan pribadi ke pemilik Komunitech (lihat bagian 7). **Tanda berhasil:** satu formulir terkirim untuk tiap skill yang Anda coba.

## 5. Sepuluh skill fokus

Tempel kalimat di bawah apa adanya ke chat bot Anda, lalu ganti angka dan nama sesuai keadaan usaha Anda. Catatan: `pantau-cron-openclaw` dan `cek-privasi-openclaw` **hanya untuk OpenClaw**; delapan skill lain berformat sama sehingga bisa dipasang di Claude Code, Codex, atau Cursor, tetapi baru diuji di OpenClaw; laporan Anda dari platform lain sangat berharga.

**1. `pantau-cron-openclaw` — Laporan Terjadwal Gagal? Langsung Ketahuan.** Jadwal/laporan otomatis OpenClaw yang terlambat atau hilang ketahuan dan Anda dikabari lewat Telegram. Tugas 7 hari: periksa jadwal otomatis bot Anda, pasang pengawas (bot menampilkan rencana dan meminta "ya" sebelum mengubah jadwal). Perlu: hanya OpenClaw, Telegram terhubung, Python 3 (wajib). Catatan jujur: pemasangan penuh sampai kabar benar-benar masuk ke Telegram belum kami uji; bot akan menjalankan satu uji peringatan dulu — laporkan apakah pesan uji itu sampai ke Telegram Anda (ini masukan paling berharga untuk skill ini).
- `Pantau laporan harian 21.00 dan piutang 07.45 Senin-Jumat saya. Kabari ke Telegram kalau gagal.`
- `Job mana yang terlambat hari ini?` (job = jadwal otomatis bot Anda)

**2. `rapor-mingguan-ai` — Rapor Mingguan untuk Karyawan AI Anda.** Rapor satu layar atas percakapan bot dengan pelanggan: nilai A–D, kesalahan tersering, tren, dan teks perbaikan siap tempel. Tugas 7 hari: minta rapor mingguan pekerjaan bot. Perlu: salin sendiri 10–20 percakapan bot–pelanggan sebagai teks biasa (hapus nomor kartu dan data sensitif); Python tidak wajib.
- `Tolong buatkan rapor bot saya minggu ini. Ini percakapannya. Bot saya baru dua minggu.` (tempel percakapannya)
- `Ini rapor minggu lalu dan percakapan minggu ini. Naik atau turun?`

**3. `cek-privasi-openclaw` — Cek Privasi OpenClaw dalam Bahasa Awam.** Laporan merah/kuning/hijau atas pengaturan keamanan dan privasi OpenClaw; perbaikan ditawarkan satu per satu dengan izin Anda. Tugas 7 hari: audit privasi setelan bot sendiri. Perlu: hanya OpenClaw. Bila bot menjawab tidak bisa menjalankan perintah, itu normal: bot akan menuliskan perintahnya, lalu Anda salin dan jalankan di Terminal komputer tempat OpenClaw berjalan (atau tulis "Perlu bantuan" di formulir). Tanpa Python.
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

**8. `satu-lawan-satu-dan-umpan-balik` — Ngomong ke Tim Tanpa Tidak Enak Hati.** Naskah ucapan dan pesan WA untuk obrolan empat mata, teguran halus, rencana 30 hari karyawan baru, dan pengumuman ke tim. Tugas 7 hari: siapkan 1 sesi empat mata dengan karyawan. Perlu: tidak ada (tanpa Python, akun, atau program tambahan).
- `Saya nggak enak negur kasir yang sering telat.`
- `Buatkan agenda obrolan empat mata 30 menit dengan staf gudang saya.`

**9. `tangani-keberatan-pelanggan` — Jawab "Mahal" dan "Mikir Dulu" Tanpa Memaksa.** 2–3 balasan WA siap kirim untuk keberatan "mahal", "mikir dulu", "tanya suami/bos", "takut tipu", "pesaing lebih murah", plus satu pertanyaan lanjutan. Tugas 7 hari: balas 3 keberatan harga/pesaing sungguhan; Anda yang mengirim balasan satu per satu. Bila Anda belum menyebut data produk, bot menulis tanda `[isian: ...]` di balasannya; ganti tanda itu dengan data Anda sebelum dikirim ke pelanggan. Perlu: Python opsional (untuk hitungan harga per hari dan cicilan).
- `Pelanggan bilang 'kemahalan kak'. Aku jual [produk] Rp[harga].`
- `Klien jawab 'saya pikir-pikir dulu'. Gimana balasnya?`

**10. `landing-page-siap-tayang` — Landing Page Jadi dan Tayang Hari Ini.** Satu file web `index.html` utuh (tampil rapi di HP, tombol WhatsApp dengan pesan terisi, FAQ). Plus panduan langkah demi langkah menayangkannya gratis lewat layanan seperti Netlify Drop, GitHub Pages, atau Cloudflare Pages (hosting = tempat menyimpan halaman agar bisa dibuka orang lewat internet) dan cara memasang nama domain (alamat web Anda, mis. tokoanda.com). Tugas 7 hari: buat 1 halaman promo produk, lalu tayangkan. Ganti bagian bertanda `[isian: ...]` (mis. `[isian: harga]`) sebelum tayang; versi file bisa diminta dengan membalas "kirim file". Perlu: Anda sendiri yang mengunggah file ke hosting; Python tidak wajib.
- `Buatkan landing page jasa servis AC saya, WA 0812-3456-7890.`
- `Bagaimana pasang domain ke landing page ini?`

## 6. Aturan main

- **Yang dinilai adalah pekerjaan nyata.** Kalimat contoh di panduan ini hanya untuk memastikan skill terpasang; untuk penilaian, pakai skill pada pekerjaan sungguhan minimal 3 kali per skill.
- **Data Anda sendiri, tanggung jawab Anda sendiri.** Simpan di komputer sendiri, hapus nomor kartu dan data sensitif sebelum menempel, dan periksa hasil sebelum dipakai untuk keputusan uang, karyawan, atau pelanggan. Hasil skill bukan nasihat keuangan, hukum, asuransi, atau medis; keputusan akhir tetap di tangan Anda.
- **Jangan sebar paket.** ZIP diberi tanda (watermark) berupa nama dan kode lisensi Anda; `SKILL.md` di dalamnya memuat keterangan "Dilarang menyebarluaskan".
- **Laporkan bila bot menjawab aneh**, salah hitung, atau menolak permintaan wajar: tempel contohnya, hapus data pribadi/pelanggan dulu. Itu justru masukan paling berharga.
- **Tidak harus 10 skill.** Minimal 3 yang cocok; skill lain di dalam ZIP boleh dicoba, tetapi fokus penilaian pada 10 skill beta.
- **Privasi.** Hasil audit privasi tidak dikirim ke Komunitech, CV tidak dikirim ke mana pun oleh skill, dan hitungan berjalan di komputer Anda sendiri; yang kami terima hanya jawaban formulir Anda. Seperti pemakaian bot biasa, isi chat (termasuk CV atau percakapan yang Anda tempel) tetap diproses oleh penyedia model AI yang Anda pilih sendiri (mis. Anthropic/OpenAI), bukan oleh Komunitech; karena itu hapus data sensitif sebelum menempel. Masukan dirangkum anonim (Beta 1, Beta 2, dst.), dan testimoni hanya dikutip dengan izin tertulis Anda.

## 7. Cara dan tenggat mengirim masukan

**Tenggat: Hari ke-7 (19 Oktober 2026); kirim paling lambat 20 Oktober 2026.**

**Di mana mengirim:** di topik Telegram tempat Anda menerima paket ini, yaitu topik yang namanya diawali **"Beta VIP — panduan tester"** di grup Telegram Komunitech tempat Anda diundang (tempat pesan pembuka dan file ZIP Anda dikirim). Untuk menandai pemilik Komunitech, balas pesan pembuka di topik itu, atau ketik `@` lalu pilih nama yang disebut di pesan pembuka. Bila lebih nyaman, kirim lewat pesan pribadi (japri) ke pemilik Komunitech: ketuk nama pengirim pesan pembuka di topik itu, lalu pilih "Kirim Pesan".

- **Selama uji:** pertanyaan teknis ditulis di topik itu dengan menandai pemilik Komunitech.
- **Hari ke-7 (19 Oktober):** isi formulir di bawah untuk **tiap skill yang dicoba** (satu formulir per skill), kirim paling lambat 20 Oktober di topik yang sama atau lewat pesan pribadi ke pemilik Komunitech. Bila tim membagikan Google Form atau jalur WA, boleh lewat itu.
- Jawaban diteruskan ke tim tanpa nama/kontak Anda dan dirangkum anonim (Beta 1, Beta 2, dst.).

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
```

## 8. FAQ

**Harus mencoba semua 10 skill?**
Tidak. Pilih minimal 3 yang cocok dengan usaha Anda, masing-masing dipakai minimal 3 kali untuk pekerjaan nyata.

**Skill tidak muncul atau tidak dipakai otomatis?**
Pastikan `SKILL.md` ada langsung di dalam folder skill (bukan di dalam folder pembungkus), mulai percakapan baru (OpenClaw lewat Telegram: cukup kirim pesan baru ke bot Anda; Claude Code, Codex, atau Cursor: buka sesi/chat baru), lalu sebut kebutuhan lebih jelas atau panggil nama skill-nya, misalnya "pakai skill kelayakan-investasi-usaha". Di OpenClaw, cek dengan `openclaw skills list` (diketik di Terminal/jendela WSL di komputer tempat OpenClaw berjalan — bukan di chat Telegram).

**Saya pakai Windows, perlu apa?**
Untuk OpenClaw: bila OpenClaw Anda berjalan lewat WSL (fitur Windows untuk menjalankan Linux), jalankan perintah pasang di jendela WSL seperti langkah di bagian 3. Windows tanpa WSL belum kami uji; bila ragu atau Terminal terasa sulit, tulis "Perlu bantuan" di formulir dan tanyakan di topik Telegram tempat Anda menerima paket ini. Untuk skill hitungan: pasang Python dari python.org dan centang "Add Python to PATH"; tanpa Python skill hitungan tetap jalan, tetapi angka sebaiknya dicek ulang; khusus `pantau-cron-openclaw` wajib Python 3 (tanpa Python pengawas tidak bisa dipasang).

**Muncul "python not found"?**
Pasang Python (Windows dari python.org, centang "Add Python to PATH"), lalu tutup dan buka lagi aplikasi AI Anda (Claude Code, Codex, atau Cursor). Untuk OpenClaw: jalankan ulang OpenClaw di komputer tempat ia berjalan; bila tidak tahu caranya, tulis "Perlu bantuan" di formulir.

**Saya pakai Claude Code, Codex, atau Cursor, bukan OpenClaw. Masih berguna ikut?**
Sangat berguna. Ke-10 skill ini kami uji di OpenClaw (termasuk lewat bot Telegram); format skill sama di platform lain, tetapi pengalaman nyata di sana belum kami miliki. Ingat, `pantau-cron-openclaw` dan `cek-privasi-openclaw` hanya untuk OpenClaw.

**Apakah hasil audit privasi atau data saya dikirim ke Komunitech?**
Tidak. Hasil audit privasi tidak dikirim ke Komunitech, CV tidak dikirim ke mana pun oleh skill, dan hitungan berjalan di komputer Anda sendiri; yang kami terima hanya jawaban formulir yang Anda kirim. Seperti pemakaian bot biasa, isi chat (termasuk CV atau percakapan yang Anda tempel) tetap diproses oleh penyedia model AI yang Anda pilih sendiri (mis. Anthropic/OpenAI), bukan oleh Komunitech; karena itu hapus data sensitif sebelum menempel.

**Apa yang saya dapat setelah program selesai?**
10 skill yang diuji gratis selamanya + 1 skill lain pilihan Anda, diberikan setelah formulir masukan Anda diterima.

## 9. Terima kasih

Tujuh hari Anda sangat berarti: dari catatan kecil Anda, skill ini diperbaiki sebelum sampai ke pengusaha dan profesional lain di Indonesia. Selamat mencoba, dan sampai bertemu di topik Telegram tempat Anda menerima paket ini.
