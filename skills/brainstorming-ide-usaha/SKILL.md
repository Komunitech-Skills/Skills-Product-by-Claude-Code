---
name: brainstorming-ide-usaha
description: Memandu sesi curah gagasan terstruktur untuk ide usaha baru, ide promo, nama usaha/produk, diversifikasi usaha, atau solusi masalah operasional — menggali tujuan & batasan nyata (modal, waktu, SDM, lokasi, musim), memakai teknik ide terstruktur (SCAMPER, gabung-kombinasi, pembalikan masalah), menyaring ide dengan skor tertimbang yang dihitung script, menghitung untung per unit & biaya uji dalam rupiah (termasuk potongan GoFood/Shopee dll.), dan paling lambat di balasan kedua menutup dengan rencana uji 7 hari berisi target angka & biaya. Gunakan saat pengguna minta brainstorming ide bisnis, cari ide jualan, ide nama usaha/produk, ide promo, ide diversifikasi usaha, atau solusi masalah operasional (business idea brainstorming, product naming, promo ideas, business diversification, structured ideation, SCAMPER, idea scoring).
---

# Brainstorming Ide Usaha

> **Aturan kerja:** Jangan menginstal paket/aplikasi (mis. `pip install`) — bila perlu, tunjukkan caranya dan biarkan pengguna yang memasang; jangan membuka atau mencari file selain yang diberikan pengguna, isi folder skill ini, dan file yang disebut di langkah kerja; jangan menulis file baru tanpa menyebut lokasinya, dan simpan hasil di folder kerja yang disepakati (bukan /tmp).

Mengubah "saya mau usaha X tapi bingung mulai dari mana" menjadi beberapa ide konkret yang sudah disaring, diuji murah, dan punya rencana aksi 7 hari — bukan sekadar daftar ide acak.

## Aturan tempo & file (WAJIB, berlaku di Jalur B & C)
1. **Rencana uji 7 hari paling lambat di balasan kedua.** Balasan 1 boleh berisi satu
   daftar pertanyaan (maks. 5). Balasan 2 — setelah pengguna menjawab, atau balasan 1
   bila info sudah cukup / pengguna minta cepat — WAJIB memuat sekaligus: ringkasan
   pemahaman + asumsi, ide & skor, rekomendasi, **hitungan rupiah** (`rencana`), dan
   **Rencana Uji 7 Hari** lengkap untuk ide rekomendasi. Gerbang persetujuan menjadi
   **konfirmasi di akhir** ("Mau pakai ide #2 saja? Ketik 2, rencananya aku sesuaikan"),
   bukan penghenti sebelum rencana.
2. **File hanya di folder kerja (workspace) pengguna, tidak pernah di folder skill.**
   Utamakan tanpa file: `python3 scripts/skor_ide.py skor --ide -` dengan CSV lewat
   stdin (heredoc/pipe). Bila perlu menyimpan CSV/JSON, tulis di folder kerja saat ini
   (bukan `scripts/`, bukan /tmp) dan **sebutkan path lengkapnya** di balasan.
3. **Angka uang dihitung, bukan dikira.** Untung per unit, laba uji, titik impas →
   `skor_ide.py rencana`/`impas`. Angka pasar (jumlah pembeli, omzet pesaing) yang tidak
   diberikan pengguna ditandai "asumsi". Pada kasus investasi/bagi hasil **jangan
   menyebut angka imbal hasil** (mis. "2–5%/bulan") — itu karangan; cukup "sesuai laba
   riil yang dilaporkan".
4. **Harga yang disarankan wajib dicek kewajarannya — lewat script, bukan perasaan.**
   Harga baru/paket dihitung dari **biaya + margin**: `rencana --modal-unit <biaya/unit>
   --margin-target <persen>` (harga minimal keluar dari script), lalu dibandingkan dengan
   acuan pasar dari pengguna: `--harga-lama <harga eceran sendiri per satuan>` dan
   `--harga-pesaing <harga pesaing per satuan>`. Untuk paket/langganan isi beberapa satuan,
   tambahkan `--isi-per-unit <mis. 15> --satuan kg` supaya harga per kg terlihat. Bila script
   menulis **CEK** (lebih mahal dari harga sendiri/pesaing): turunkan harga/isi paket, atau
   sebutkan nilai tambah konkret yang dibayar pelanggan — jangan menulis "asumsi dari pola
   harga Anda" bila angkanya tidak cocok. Bila belum ada acuan pasar, tulis
   `[isi: harga pesaing per satuan]` (status BELUM DICEK). Isi paket & frekuensi layanan
   (mis. antar-jemput 1×/minggu) harus **sama** di cara uji, hitungan, dan tabel 7 hari.
5. **Jangan mengutip nomor pasal pidana** (KUHP, UU Perbankan, dll.) kecuali pengguna
   memintanya. Bila diminta, pakai hanya [references/rujukan-kasus-terlarang.md](references/rujukan-kasus-terlarang.md)
   (KUHP baru UU 1/2023 berlaku sejak 2 Januari 2026; nomor pasal KUHP lama tidak dipakai).

## Tujuan

Membantu pemilik UMKM/profesional Indonesia curah gagasan secara **terarah**: menggali dulu tujuan & batasan nyata (modal, waktu, SDM, lokasi, musim), baru memunculkan ide dengan teknik terstruktur, menyaringnya dengan skor yang dihitung (bukan feeling), dan menutup dengan langkah uji murah yang jelas — sehingga ide yang keluar benar-benar bisa dieksekusi minggu ini, bukan wacana.

## Kapan digunakan
- "Saya mau usaha sampingan tapi belum tahu jualan apa."
- "Butuh ide nama untuk toko roti baru saya."
- "Usaha laundry saya sepi, ada ide promo atau ide tambahan produk?"
- "Mau diversifikasi dari jualan baju ke lini produk lain, ide apa yang cocok?"
- "Stok bahan sering sisa/basi, ada ide solusinya?" (masalah operasional, bukan cuma ide produk baru)
- Punya beberapa ide di kepala tapi bingung mana yang paling layak dikerjakan duluan.

## Kapan TIDAK digunakan
- Sudah punya SATU ide jelas dan hanya butuh dieksekusi (mis. tulis promo → `promo-kalender`, tulis konten → `kalender-konten-30hari`/`caption-sosmed-umkm`, hitung modal produk → `hitung-hpp`, cari calon pelanggan → `riset-calon-pelanggan`, susun proposal kemitraan → `proposal-kerjasama`) — arahkan ke skill terkait, jangan mulai sesi brainstorming baru.
- Butuh nama usaha sekadar generator cepat tanpa proses (mis. "kasih 20 nama toko, cepat") — boleh dipakai jalur cepat skill ini (lihat Langkah Kerja Jalur A), tapi kalau pengguna benar-benar hanya mau daftar nama tanpa konteks apa pun, cukup beri daftar dan tawarkan sesi lengkap sebagai opsi, jangan dipaksakan.
- Riset kelayakan pasar mendalam (survei, analisis kompetitor terinci, proyeksi keuangan multi-tahun) — skill ini hanya menyaring ide dengan cepat & murah, bukan pengganti riset pasar profesional atau studi kelayakan formal.
- Keputusan hukum/pajak/perizinan usaha (bentuk badan usaha, PKP, NIB, dll.) — arahkan ke profesional/instansi terkait; skill ini tidak membahas legalitas.
- Ide di kategori terlarang (skema piramida/money game, judi, produk ilegal, investasi tanpa izin OJK, klaim obat menyembuhkan tanpa izin edar) → tolak dengan sopan, jelaskan alasannya. Jelaskan dengan bahasa awam (skema piramida dilarang UU Perdagangan; menghimpun dana/menawarkan investasi tanpa izin diawasi OJK — cek daftar entitas berizin di situs OJK atau Kontak OJK 157), **tanpa nomor pasal pidana** kecuali diminta (Aturan tempo 5; rujukan terkini di [references/rujukan-kasus-terlarang.md](references/rujukan-kasus-terlarang.md), dicek 2026-10-01).

## Input
Gali (atau simpulkan dari cerita pengguna) sebelum mulai:
1. **Jenis kebutuhan:** ide produk/jasa baru, ide promo, ide nama usaha/produk, ide diversifikasi, atau solusi masalah operasional?
2. **Konteks usaha saat ini:** sudah punya usaha (apa, sudah berapa lama, target pelanggan sekarang) atau mulai dari nol?
3. **Tujuan & ukuran berhasil:** apa yang ingin dicapai (tambah omzet, isi waktu kosong, kurangi limbah/stok sisa, dll.) dan seperti apa hasilnya dianggap berhasil?
4. **Batasan nyata** — modal yang bisa dipakai (Rupiah kasar), waktu yang tersedia per minggu, jumlah SDM/tenaga bantu, lokasi/wilayah operasi, dan musim/momentum yang relevan (lihat [references/musim-dan-momentum.md](references/musim-dan-momentum.md)).
5. **Hal yang sudah dicoba/ditolak** (kalau ada) — supaya tidak mengulang ide yang sudah gagal tanpa alasan baru.

**Prinsip instan:** kalau pengguna minta cepat ("langsung kasih ide aja", "jangan tanya-tanya"), JANGAN paksa menggali satu-per-satu. Pakai default berikut dan sebutkan sebagai asumsi di akhir:
- Modal: menengah-kecil (di bawah Rp5 juta), waktu: paruh waktu (di luar kerja/aktivitas utama), SDM: sendiri/dibantu 1 orang, lokasi: rumahan/online.
- Ukuran berhasil default: minimal 10 pelanggan/pesanan uji dalam 1 minggu tanpa rugi.

## Langkah Kerja

> **Lokasi script:** semua script skill ini ada di subfolder `scripts/` di folder yang sama dengan SKILL.md ini (folder skill). Jalankan dari sana; jangan mencari script atau file pengguna ke seluruh disk (mis. `find /`) — itu lambat dan menyentuh data pribadi di luar folder kerja.

### 0. Klasifikasi dulu, sebutkan ke pengguna
Sebelum bertanya lebih jauh, kelompokkan permintaan dan katakan klasifikasinya ("ini sepertinya jalur cepat, jadi saya langsung kasih beberapa opsi" dsb.) supaya pengguna bisa mengoreksi:

- **Jalur A — Cepat:** hanya butuh beberapa opsi ringan (nama usaha/produk, judul promo, 1 ide kecil pelengkap) tanpa keputusan besar menyusul. → langsung ke Langkah A.
- **Jalur B — Perlu Diuji:** ide produk/promo/perbaikan operasional baru untuk usaha yang **sudah berjalan**, risikonya kecil-menengah (modal terbatas, bisa dites minggu ini). → Langkah B lengkap.
- **Jalur C — Perlu Rencana:** usaha baru dari nol, diversifikasi ke lini usaha berbeda, atau perubahan besar yang memengaruhi banyak hal (modal besar, SDM baru, lokasi baru). → Langkah C lengkap (paling dalam).

Kalau ragu antara dua jalur, pilih yang **lebih dalam** (lebih aman kelebihan proses daripada ide besar dieksekusi tanpa disaring). Kalau di tengah sesi ternyata skalanya lebih besar dari perkiraan awal (mis. jalur B ternyata butuh modal besar & SDM baru), naikkan ke jalur C dan katakan alasannya ke pengguna — jangan diam-diam tetap di jalur lama.

**Jalur B vs C secara ringkas (biar tidak salah pilih):** kalau usaha **sudah berjalan** dan idenya adalah **1 produk/jasa/promo tambahan** dengan modal & risiko kecil-menengah yang **bisa dites minggu ini tanpa menambah SDM atau lokasi baru** → Jalur B (skor tertimbang & titik impas boleh dipakai di sini juga, lihat B.4). Kalau usaha **baru dari nol**, mencakup **beberapa lini/usaha berbeda sekaligus**, atau butuh **modal besar/SDM baru/lokasi baru** → Jalur C. Contoh: laundry yang sudah jalan menambah 1 layanan baru dengan modal kecil = Jalur B (lihat [examples/uji-pembuat-01-diversifikasi-laundry.md](examples/uji-pembuat-01-diversifikasi-laundry.md)); membuka lini usaha benar-benar baru di samping laundri yang ada = Jalur C.

**Bobot skor default resmi** (dipakai otomatis oleh `scripts/skor_ide.py` kalau file bobot tidak diberikan): `kesesuaian_modal=5, potensi_permintaan=4, kemudahan_eksekusi=3, kecocokan_keahlian=2, potensi_margin=4` — hanya berlaku kalau nama kolom kriteria di file ide persis sama dengan lima nama itu (lihat [templates/format-data-skor.md](templates/format-data-skor.md)). Kalau kriteria pengguna berbeda, script otomatis memakai bobot sama rata (semua = 1) dan menyebutkannya di keluaran — tidak pernah diam-diam memakai angka lain.

**Jalur A — Cepat:**
1. Tanyakan singkat konteks inti (bidang usaha, kesan/nada yang diinginkan) dalam **satu pesan** berisi 2–3 poin sekaligus, bukan satu-per-satu (jalur ini memang untuk kecepatan).
2. Berikan langsung 8–15 opsi (nama/judul/ide kecil) dikelompokkan per pendekatan (mis. untuk nama: deskriptif, gabungan kata, bahasa daerah/lokal, playful). Tandai 2–3 favorit dengan alasan singkat.
3. Cek ketersediaan secara kasar: ingatkan pengguna mengecek nama di Instagram/marketplace/pengecekan merek (DJKI) sebelum dipakai resmi — skill ini tidak mengecek ketersediaan otomatis.
4. Tutup dengan tawaran: "Mau salah satu ini diuji lebih dalam (target pasar, cara jual, dsb.)? Saya bisa lanjut ke sesi lebih lengkap."

**Jalur B — Perlu Diuji (ide untuk usaha yang sudah jalan):**
1. **Gali tujuan & batasan** dari daftar Input di atas dalam **satu pesan** berisi maksimal 5 pertanyaan singkat (pilihan ganda bila masuk akal) — tanyakan hanya hal yang benar-benar belum jelas dari cerita pengguna, jangan ulangi yang sudah disebutkan. Susulan (giliran kedua) hanya kalau ada jawaban yang ambigu. Kalau pengguna minta cepat, langsung pakai default di bagian Input dan sebutkan sebagai asumsi tanpa bertanya sama sekali.
2. **Tulis ulang pemahaman** dalam catatan singkat di awal balasan: tujuan, batasan, ukuran berhasil — pisahkan mana yang disebutkan pengguna vs asumsi Anda. Koreksi pengguna boleh menyusul; jangan berhenti menunggu koreksi (Aturan tempo 1).
3. **Munculkan ide** dengan 1–2 teknik terstruktur yang relevan dari [references/teknik-ide-terstruktur.md](references/teknik-ide-terstruktur.md) (SCAMPER, gabung-kombinasi, atau pembalikan masalah).
4. **Ajukan 2–3 pendekatan** (bukan satu ide tunggal) dengan untung-rugi masing-masing (modal, **waktu balik modal kasar** — hitung dengan `python3 scripts/skor_ide.py impas --modal <rupiah> --margin <rupiah per unit>` bila ada perkiraan margin per unit, lihat C.8 untuk detail cara pakai/batasannya) dan rekomendasi Anda + alasan. Kalau pendekatan yang dipertimbangkan ≥4, boleh saring dulu dengan skor tertimbang seperti Langkah C.5 sebelum menyajikan 2–3 teratas.
5. **Langsung susun rencana untuk ide rekomendasi** di balasan yang sama (Aturan tempo 1); tutup dengan konfirmasi singkat: "Mau ganti ke ide #2/#3? Ketik nomornya, rencananya aku sesuaikan."
6. **Rancang uji murah (MVP)** untuk ide yang disepakati memakai [templates/kerangka-uji-murah.md](templates/kerangka-uji-murah.md): cara uji (pre-order via status WA/story, jual terbatas ke pelanggan tetap dulu, dsb.), durasi (default 1 minggu bila tidak disebutkan), target ukuran berhasil (default 10 pelanggan/pesanan), dan kapan berhenti/lanjut.
   Hitung rupiahnya: `python3 scripts/skor_ide.py rencana --harga <jual/unit> --modal-unit <bahan+kemasan/unit> --potongan-persen <komisi aplikasi, 0 bila via WA> --biaya-uji <total uang keluar 7 hari> --target <unit>` (tambahkan `--modal <alat>` bila ada beli alat; untuk harga baru pakai `--margin-target <persen>` sebagai ganti `--harga`; **selalu** tambahkan `--harga-lama`/`--harga-pesaing` per satuan dari pengguna dan `--isi-per-unit`/`--satuan` untuk paket — Aturan tempo 4). Kutip angka keluaran apa adanya. Contoh paket laundry: `rencana --modal-unit 48rb --margin-target 30 --isi-per-unit 15 --satuan kg --harga-lama 6rb --harga-pesaing 5rb --biaya-uji 200rb --target 10` → harga minimal Rp68.572 (Rp4.571/kg, WAJAR). Persen potongan GoFood/GrabFood/ShopeeFood/marketplace **tanyakan atau minta pengguna cek di aplikasi mitranya** — jangan mengarang; bila belum tahu, hitung dua skenario (jual langsung via WA = 0% dan via aplikasi dengan persen yang disebut pengguna).
7. Tutup dengan **Rencana Uji 7 Hari** (lihat Format Output).

**Jalur C — Perlu Rencana (usaha baru/diversifikasi/perubahan besar):**
1. **Cek skala dulu.** Kalau permintaan sebenarnya mencakup beberapa usaha/lini berbeda sekaligus (mis. "mau buka kafe sekaligus jasa katering sekaligus toko online"), sampaikan itu di awal dan usulkan memecah jadi satu lini per sesi — jangan habiskan pertanyaan untuk merinci proyek yang perlu dipecah dulu.
2. **Gali konteks & batasan** selengkap Input di atas dalam **satu pesan** berisi maksimal 5 pertanyaan singkat (pilihan ganda bila masuk akal), mencakup hal yang belum disebutkan pengguna. Susulan hanya untuk jawaban yang ambigu atau kalau di tengah sesi ternyata ada kerumitan tersembunyi. **Mode cepat:** kalau pengguna minta cepat ("langsung kasih ide aja", "jangan tanya-tanya"), lewati pertanyaan ini sepenuhnya — pakai default di bagian Input dan sebutkan sebagai asumsi. Gerbang di langkah 7 berupa konfirmasi di akhir balasan yang sudah memuat rencana (Aturan tempo 1).
3. **Tulis ulang pemahaman** (tujuan, batasan modal/waktu/SDM/lokasi/musim, ukuran berhasil) singkat di awal balasan yang sama dengan ide & rencana — koreksi pengguna boleh menyusul, tidak perlu giliran terpisah.
4. **Munculkan ide** dengan 2–3 teknik dari [references/teknik-ide-terstruktur.md](references/teknik-ide-terstruktur.md), sesuaikan dengan musim/momentum yang relevan dari [references/musim-dan-momentum.md](references/musim-dan-momentum.md).
5. **Saring ide dengan skor tertimbang.** (Data ide kirim lewat stdin: `python3 scripts/skor_ide.py skor --ide - <<'EOF' ... EOF`; bila memakai file, simpan di folder kerja pengguna dan sebut path-nya — Aturan tempo 2.) Susun daftar ide (idealnya 5–10) dan kriteria penyaringan yang disepakati bersama pengguna (default: kesesuaian_modal, potensi_permintaan, kemudahan_eksekusi, kecocokan_keahlian, potensi_margin — lihat bobot default resmi di atas). Kalau ada Python, jalankan `python3 scripts/skor_ide.py skor --ide <file.csv> --bobot <file.json>` untuk menghitung skor tertimbang, peringkat, dan mendeteksi skor seri (lihat format di [templates/format-data-skor.md](templates/format-data-skor.md)). Argumen `--bobot` boleh dilewatkan (mis. di mode cepat) — script otomatis memakai bobot default resmi bila nama kolom cocok, atau bobot sama rata bila tidak, dan menyebutkan sumbernya di keluaran. Kalau Python tidak ada, hitung manual dengan rumus yang sama (skor = jumlah(nilai kriteria × bobot) / jumlah bobot) dan tampilkan cara hitungnya.
6. **Presentasikan 2–3 ide teratas** dengan untung-rugi, bukan cuma angka skor mentah — jelaskan kenapa unggul/kalah.
7. **Konfirmasi, bukan penghenti.** Untuk usaha baru/modal besar, tetap susun rencana **uji murah** 7 hari untuk ide rekomendasi (uji kecil sebelum keluar modal besar), lalu tanyakan di akhir apakah ide itu yang dipilih. Jangan menyusun rencana investasi penuh (sewa tempat, rekrut, beli alat besar) sebelum pengguna memilih.
8. **Rancang uji murah (MVP)** seperti Langkah B.6. Untuk ide yang perlu modal awal cukup besar, tawarkan hitung titik impas kasar: `python3 scripts/skor_ide.py impas --modal <rupiah> --margin <rupiah per unit>` (jumlah unit terjual untuk balik modal, dibulatkan ke atas; menerima angka biasa, format ribuan "5.000.000", "Rp5.000.000", atau singkatan "5jt"/"15rb"). Ini perkiraan kasar, bukan pengganti perhitungan HPP lengkap — arahkan ke skill `hitung-hpp` untuk modal per unit yang presisi dari resep/BOM.
9. Tutup dengan **Rencana Uji 7 Hari** + hitungan `rencana` (seperti B.6).

**Kanal uji khas Indonesia (pilih yang paling murah dulu):** status WA & broadcast ke pelanggan tetap (manual, bukan blast massal), grup WA RT/kompleks/kos/kampus/alumni (izin admin), Instagram/TikTok lokal + tag lokasi, titip jual di warung/kantin (konsinyasi), pre-order (PO) dengan DP/QRIS supaya minat terukur, COD/ambil sendiri, kerja sama ojek/kurir lokal. Momen: tanggal gajian (25–tanggal 1), awal bulan, Jumat (Jumat berkah), tanggal kembar marketplace, awal semester/libur kampus, Ramadan/Lebaran — lihat [references/musim-dan-momentum.md](references/musim-dan-momentum.md).

**YAGNI di semua jalur:** buang fitur/varian ide yang tidak diminta dan tidak perlu untuk uji pertama. Uji ide paling sederhana dulu yang masih bisa menjawab pertanyaan "apakah ini laku", baru tambah variasi setelah terbukti.

## Format Output
Sesuaikan dengan jalur yang dipakai:

**Jalur A:** daftar 8–15 opsi terkelompok per pendekatan + 2–3 favorit bertanda + pengingat cek ketersediaan + tawaran lanjut ke sesi lengkap.

**Jalur B & C**, paling lambat di balasan kedua (Aturan tempo 1):
1. **Ringkasan pemahaman** — tujuan, batasan, ukuran berhasil yang disepakati.
2. **Ide yang dipertimbangkan** — tabel ringkas (nama ide, pendekatan/teknik sumbernya, skor bila dihitung).
3. **Ide terpilih** — 1 (atau 2 untuk diuji berdampingan) ide yang disepakati pengguna, dengan alasan.
4. **Rencana uji murah (MVP)** — cara uji, durasi, target ukuran berhasil, kapan berhenti/lanjut.
5. **Hitungan rupiah** — kutipan keluaran `skor_ide.py rencana`: harga (dari biaya + margin bila harga baru), harga per satuan, **cek kewajaran harga** vs harga sendiri & pesaing (WAJAR / CEK / BELUM DICEK), potongan aplikasi, modal/unit, untung/unit, biaya uji, laba uji, unit untuk menutup biaya uji.
6. **Rencana Uji 7 Hari** — tabel wajib dengan kolom `Hari | Tugas konkret | Target angka | Biaya (Rp)`, Hari 1 s/d 7 lengkap. Target kumulatif Hari 3/5/7 dari keluaran `rencana`; total kolom biaya = `--biaya-uji`. **Titik berhenti dini** dari script ditulis di baris Hari 3 dan Hari 5 (Hari 3 = 0 → ganti tawaran/kanal; Hari 5 di bawah ambang → hentikan dan hemat sisa biaya). Hari 7 = evaluasi dengan ambang lanjut/perbaiki/hentikan dari keluaran script.
   Tambahkan **2 tanda bahaya** (pre-mortem): dua alasan paling mungkin ide ini gagal + sinyal awal yang dipantau Hari 1–3 (mis. "banyak yang tanya harga lalu diam → harga terlalu tinggi"). Contoh baris: `1 | Kirim penawaran PO paket langganan ke 40 kontak pelanggan lama via WA (satu per satu) | 40 pesan terkirim, ≥5 balasan | Rp0`.
7. **Asumsi yang dipakai** (bila ada default karena input awal kurang lengkap) + lokasi file bila ada yang disimpan + konfirmasi ganti ide.

## Contoh
Lihat [examples/uji-pembuat-01-diversifikasi-laundry.md](examples/uji-pembuat-01-diversifikasi-laundry.md) untuk contoh Jalur B lengkap (skor tertimbang opsional dipakai di sini) dari "usaha laundry saya sepi, ada ide tambahan?" sampai skor ide dihitung script dan rencana aksi 7 hari (dibuat oleh pembuat skill, bukan pengganti pengujian independen Tahap 6).

## Batasan & Penanganan Error
- **Bukan riset pasar profesional** — hasil skill ini adalah penyaringan cepat & murah berbasis logika + input pengguna, bukan survei, analisis kompetitor mendalam, atau proyeksi keuangan multi-tahun. Sebutkan ini bila pengguna butuh keputusan bermodal sangat besar.
- **Bukan pengecekan legal** — tidak mengecek ketersediaan nama usaha/merek secara resmi (DJKI), izin usaha, PKP, atau kepatuhan pajak. Ingatkan pengguna mengecek sendiri sebelum dipakai resmi.
- **Tidak pernah mengarang data pasar** (angka permintaan, jumlah kompetitor, tren) yang tidak diberikan pengguna atau tidak bisa diverifikasi — tandai sebagai asumsi/perlu dicek, bukan fakta.
- **Skor tertimbang bukan keputusan final** — hanya alat bantu menyaring & mengurutkan; presentasikan bersama untung-rugi kualitatif, jangan sekadar angka.
- **Kriteria & bobot wajib disepakati atau memakai default yang disebutkan**, jangan diam-diam memakai bobot sendiri tanpa menyebutkannya ke pengguna.
- **Input skor rusak** (nilai di luar 1–5, bobot kosong/negatif/nol, jumlah kolom kriteria tidak cocok antara data ide dan bobot): script `skor_ide.py` akan menolak dengan pesan jelas menyebut baris/kolom yang salah — jangan lanjutkan perhitungan manual dengan data yang sama sebelum diperbaiki.
- **Perhitungan titik impas** (`impas`) hanya kasar (modal awal ÷ margin per unit, dibulatkan ke atas) — tidak memperhitungkan biaya tetap bulanan berulang, pajak, atau penyusutan; untuk modal per unit presisi dari resep/BOM, arahkan ke skill `hitung-hpp`.
- **Kategori terlarang** (skema piramida/money game, judi, produk ilegal, investasi tanpa izin OJK, klaim obat/kesehatan tanpa izin edar) → tolak dengan sopan dan jelaskan alasannya (dasar aturan di bagian "Kapan TIDAK digunakan"), jangan tetap membuatkan idenya "dengan catatan".
- **Di luar cakupan** (riset kelayakan formal, legalitas usaha, negosiasi investor, ide sudah tunggal dan tinggal dieksekusi) → arahkan ke skill terkait atau ke profesional, jangan dipaksakan lewat sesi brainstorming ini.
- **Kasus investasi/titip dana/bagi hasil** → jangan menyebut angka imbal hasil atau bunga; arahkan ke laporan laba riil dan profesional/OJK.
- **Tanpa server/companion visual** — skill ini murni teks (chat + file Markdown/CSV/JSON); tidak menjalankan server lokal atau membuka browser, sesuai prinsip "tanpa setup" untuk pembeli awam.
