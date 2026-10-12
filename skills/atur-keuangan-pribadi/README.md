# Gaji Nggak Numpang Lewat Lagi

**Atur anggaran keluarga, dana darurat, pelunasan utang, dan tabungan untuk DP rumah, sekolah anak, haji, sampai pensiun — dalam Rupiah, dihitung pasti, dengan bahasa sehari-hari.**

## Manfaat
- ✅ **Anggaran bulanan yang pas untuk keluarga Indonesia** — kiriman orang tua, arisan, zakat/perpuluhan/sedekah (opsional), cicilan motor/KPR, THR dibagi 12, dan jebakan top-up e-wallet sudah dipikirkan. Setiap rupiah punya tugas sampai sisa Rp0.
- ✅ **Tahu persis kapan utang lunas** — metode Avalanche (paling hemat) vs Snowball (paling cepat terasa menang), lengkap dengan jadwal per bulan, total bunga, dan selisih biayanya.
- ✅ **Bongkar bunga flat** — leasing "cuma 12% flat" ternyata ±21,6% efektif. Bandingkan pinjaman dengan angka yang jujur.
- ✅ **Alarm bahaya** — cicilan minimum yang tidak menutup bunga, bunga di atas batas OJK/BI (tanda pinjol ilegal), dan larangan tegas gali lubang tutup lubang, plus kontak resmi OJK.
- ✅ **Target jelas per bulan** — "DP rumah 60 juta 5 tahun lagi" → berapa yang harus ditabung tiap bulan, dengan asumsi inflasi tertulis.

## Cocok untuk siapa
- Karyawan & PNS yang gajinya "habis sebelum tanggal tua"
- Pasangan muda yang baru menggabungkan keuangan dan punya anak
- Pekerja lepas, driver ojol, pedagang dengan penghasilan tidak tetap
- Siapa pun yang punya beberapa cicilan (kartu kredit, paylater, KTA, pinjol legal) dan ingin keluar dari utang
- **Bukan untuk:** keuangan usaha (pakai `arus-kas-13minggu` / `laporan-keuangan-emkm`), THR karyawan (`hitung-thr`), atau mencari saran saham/kripto/reksa dana tertentu.

## Contoh sebelum & sesudah
**Sebelum (tanpa skill):** "Coba terapkan 50/30/20 dan lunasi utang berbunga tertinggi dulu." — saran umum, tanpa angka, tanpa memperhitungkan kiriman ortu dan THR, tidak tahu kapan lunas.

**Sesudah:** Keluarga Dimas & Rina (pemasukan Rp10,29 juta termasuk THR ÷ 12, empat utang) mendapat:
- Anggaran lengkap per pos dengan sisa **Rp0**, dibandingkan pola 60/20/20.
- Avalanche: **semua utang lunas bulan ke-15, total bunga Rp3.345.301** — hemat Rp156.108 dibanding Snowball.
- Dana darurat 9 bulan (Rp72,45 juta) tercapai 19 bulan setelah utang lunas.
- 5 langkah konkret minggu ini.
Contoh lengkap: `examples/uji-pembuat-01-keluarga-muda-cicilan.md`.

## Cara pakai
Setelah terpasang, cukup cerita dengan kalimat biasa:
- "Gaji saya 7 juta, istri 3 juta, bantu atur anggaran bulanan."
- "Utang kartu kredit 12 juta dan paylater 3 juta, mana dulu yang dilunasi?"
- "Freelancer, pengeluaran pokok 5 juta, dana darurat berapa?"
- "Mau umrah berdua 4 tahun lagi, nabung berapa sebulan?"

Kalau data kurang, AI bertanya sekali saja. Angka dihitung oleh script Python bawaan (tanpa instalasi tambahan, tanpa internet); kalau script tidak bisa dijalankan, AI memakai rumus tertulis yang sama.

## Instalasi singkat
Salin folder `atur-keuangan-pribadi` ke folder skills AI agent kamu:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |

Panduan lengkap (termasuk Windows): lihat `docs/instalasi.md` yang disertakan dalam paket.

## Bukti uji di bot Telegram

Diuji di bot OpenClaw asli (grup uji Komunitech, tautan hanya terbuka untuk anggota grup): gelombang 2–3, 2026-10-02.
- Tanpa skill: https://t.me/c/4407409583/517/525 — skor: lihat catatan gelombang
- Dengan skill: https://t.me/c/4407409583/313/542 — skor: lihat catatan gelombang
Verdik gelombang: — — DENGAN menyusun anggaran zero-based dari script; TANPA hanya anggaran dan dana darurat 6–9x pengeluaran tanpa script. Catatan jujur: THR sempat dihitung ganda, diperbaiki di versi 1.0.7.

## FAQ
**Apakah skill ini menyarankan investasi tertentu?**
Tidak. Skill ini tidak pernah merekomendasikan beli/jual saham, kripto, reksa dana, emas, atau produk bank/fintech tertentu. Imbal hasil hanya dipakai sebagai asumsi yang kamu tentukan sendiri.

**Data keuangan saya dikirim ke mana?**
Tidak ke mana-mana oleh skill ini. Script berjalan di komputer kamu, tanpa internet, dan tidak menyimpan file.

**Apakah hasilnya pasti tepat?**
Hitungannya pasti (diuji dengan verifikasi independen), tetapi hasilnya simulasi: bunga bisa berubah, ada denda/biaya admin, dan hidup tidak selalu sesuai rencana. Ini **bukan nasihat keuangan**; untuk kasus rumit, konsultasikan ke perencana keuangan bersertifikat. Aturan OJK/BI dicek 26 September 2026.

**Bunga KTA saya "0,9% per bulan", apakah dihitung benar?**
Ya. Sebutkan satuannya (per bulan/per tahun). Kalau satuannya tidak jelas, AI akan menanyakan dulu — karena 0,9% per bulan flat ternyata setara ±19,5% per tahun efektif, sedangkan 0,9% per tahun hanya ±1,7%.

## Riwayat versi
- **Catatan revisi 1.0.11 (2026-10-02)** — dari uji regresi OpenClaw v1.0.10 (dua temuan rendah): (1) tebakan kelompok pos tanpa label diperbaiki — kata sekolah/SPP/pendidikan/les/anak kini mengalahkan "jajan" (Kebutuhan wajib, tidak dipangkas), kiriman ke ibu/bapak/ortu/orang tua/keluarga ("Kirim ibu") dikenali sebagai kiriman keluarga yang tidak dipangkas otomatis, pos campuran ("Jajan+Sekolah anak") tidak dipangkas dan ditandai "(perlu dipisah)" agar AI menanyakan pemisahannya, dan pos belum dikelompokkan tidak lagi dipangkas otomatis; pemangkasan otomatis hanya untuk pos Keinginan yang jelas. AI kini menyebutkan pos yang kelompoknya ditebak sebelum memakai rencana pemangkasan. (2) Script menyebut jumlah baris tabel jadwal defisit (sampai THR cair) dan AI wajib menyalin tabel itu utuh. Tes unit ditambah (99 tes).
- **Catatan revisi 1.0.10 (2026-10-02)** — dari uji ulang OpenClaw v1.0.9 (dua temuan rendah): (1) saat defisit, pos tabungan yang di-nol-kan script kini muncul sebagai tindakan eksplisit di RINGKASAN SIAP TEMPEL ("TINDAKAN: jeda Arisan RT Rp200.000/bulan — bicarakan dengan pengelola arisan"), disertai kekurangan bila arisan tetap dibayar; hanya ada satu angka defisit berlabel basis "pos tabungan dijeda" di ringkasan, tabel, catatan, dan arus kas; (2) skenario alternatif dana darurat kini mencetak perbandingan lama tercapai sekarang vs skenario per kolom (setoran saja / + THR, termasuk "tidak berubah") agar selisih waktu tidak dikarang; opsi baru `--sisih-lebaran` (anggaran & dana-darurat) menyisihkan kebutuhan Lebaran dari THR sebelum ke dana darurat — bila belum diisi, script mencetak pengingat. Tes unit ditambah (94 tes).
- **Catatan revisi 1.0.9 (2026-10-02)** — dari uji ulang OpenClaw v1.0.8: (1) script `anggaran` kini mencetak blok **RINGKASAN SIAP TEMPEL** di paling atas berisi kalimat lengkap yang sudah memuat angka & penilaian (sisa/defisit dari gaji rutin, rasio cicilan total mis. "34,4% — DI ATAS batas aman 30%", pemakaian THR, target & lama tercapai dana darurat); SKILL.md mewajibkan agent menyalinnya apa adanya dan melarang menyebut persen satu pos sebagai rasio cicilan; (2) selama defisit masih tersisa setelah pemangkasan, sisa THR dicadangkan untuk menambal defisit bulan-bulan berikutnya (disebut berapa bulan), baru kelebihannya ke dana darurat — script dan SKILL.md kini selaras; (3) kekurangan sebelum THR cair dicek terhadap saldo (`--saldo`): bila tidak cukup, script menampilkan pilihan tanpa utang (percepat pemangkasan, tambah pemasukan sementara, tunda pos tertentu); (4) defisit utama selalu dihitung dari gaji rutin; angka "THR dibagi 12" hanya catatan gambaran setahun. Tes unit ditambah (87 tes).
- **Catatan revisi 1.0.8 (2026-10-02)** — dari uji ulang OpenClaw v1.0.7: (1) angka "bagaimana jika kiriman ortu tidak dihitung" kini dicetak script (tabel **Skenario alternatif** + kalimat siap tempel) dan SKILL.md mewajibkan setiap skenario alternatif lewat script — tanpa script, angka tidak ditampilkan; (2) judul kolom persen menyebut basisnya ("% pemasukan rutin", dan "% termasuk THR/12" bila ada THR); banding pola kini berbasis gaji rutin, sama dengan rasio cicilan; (3) bila pengeluaran melebihi gaji, script menyusun **pemangkasan bertahap 3 bulan** (keinginan dulu, lalu kebutuhan fleksibel) agar anggaran pas tanpa THR, menampilkan kekurangan per bulan sampai THR cair (`--bulan-cair`), dan menempatkan THR hanya sebagai penambal sementara. Tes unit ditambah (79 tes).
- **Catatan revisi 1.0.7 (2026-10-02)** — dari uji tampilan Telegram: THR sempat dihitung dua kali (dibagi 12 sebagai pemasukan bulanan, lalu disuruh disimpan lagi saat cair) sehingga setoran Rp1,5 juta/bulan "dari sisa gaji" padahal sisa gaji hanya Rp830.000. Kini anggaran memisahkan **arus rutin** (gaji: batas setoran bulanan) dan **THR/bonus** (setoran sekaligus saat cair, nominal penuh); bila pos melebihi gaji, ditampilkan kekurangan per bulan dan berapa bulan THR menambalnya. Rasio cicilan dihitung terhadap gaji rutin (basis disebut). Dana darurat bisa menghitung lama tercapai dengan setoran THR tahunan.
- **Catatan revisi 1.0.6 (2026-10-01)** — dari uji ulang OpenClaw: kiriman rutin ke orang tua (Rp1 juta) sempat dikeluarkan dari pengeluaran pokok tanpa penjelasan sehingga target dana darurat 9 bulan kekecilan ±Rp9 juta. Kini dasar dana darurat dihitung script dari daftar pos yang dicetak: kebutuhan wajib + semua cicilan + **kewajiban rutin keluarga** (kiriman ortu/mertua/adik masuk secara bawaan), plus tabel pos yang **dikeluarkan beserta alasannya**. AI wajib mengutip angka script dan menyebut pos yang dimasukkan/dikeluarkan; kamu bisa mengubahnya ("kiriman ortu bisa berhenti") dan angka dihitung ulang. "Shopee PayLater" kini otomatis dikenali sebagai cicilan. Contoh uji: pokok Rp7.282.500 → target 9 bulan Rp65.542.500 (sebelumnya Rp56.542.500).
- **Catatan revisi 1.0.5 (2026-10-01)** — dari uji OpenClaw solusi VIP kripto-keuangan: semua cicilan (PayLater, kartu kredit, KPR, motor, KTA, pinjol) kini **wajib masuk pengeluaran pokok** untuk dasar dana darurat (sebelumnya cicilan PayLater bisa terlewat sehingga target dana darurat kekecilan ±Rp5,85 juta). `anggaran` mencetak rincian "Dasar dana darurat"; `dana-darurat` menerima `--cicilan`/`--pos` dan mengingatkan bila belum ada cicilan tercatat. AI juga menampilkan realisasi vs anggaran per pos (potongan besar ditandai bertahap) dan hanya mencari file kamu di folder kerja, bukan seluruh disk.
- **v1.0.3 (2026-09-26)** — peringatan pos anggaran kecil tidak lagi berisik: pos yang wajar bernilai kecil (parkir, jajan, sampah, iuran, pulsa, dll.) hanya diperingatkan bila < Rp1.000; pos lain tetap diperingatkan bila < Rp10.000; jumlah yang ditulis dengan "Rp" atau satuan (5rb) dianggap disengaja. Angka hitungan tidak berubah.
- **v1.0.2 (2026-09-26)** — perbaikan kecil (angka hitungan tidak berubah): satuan bunga bahasa sehari-hari diterima ("18% setahun", "1,5% sebulan", "1,5 persen per bulan"; kata "flat"/"efektif" dikenali); pos anggaran yang janggal kecil (< Rp10.000, mis. "Makan=1.500") kini diperingatkan; target: bila dana terkumpul sudah cukup untuk harga sekarang, pesan menyebutnya lebih dulu lalu menampilkan kebutuhan setelah inflasi (tidak lagi bertentangan); catatan "bila bunganya FLAT" tidak muncul untuk bunga bertanda efektif; label pos salah dan angka negatif (mis. `--saldo -500rb`) diberi pesan yang jelas dalam bahasa Indonesia.
- **v1.0.1 (2026-09-26)** — satuan bunga wajib jelas (per bulan/per tahun) agar bunga flat KTA tidak salah baca; peringatan angka yang terlalu kecil (mis. "1.500"); target menampilkan "tercapai bulan ke berapa"; catatan menilai tawaran take over/refinancing.
- **v1.0.0 (2026-09-26)** — rilis awal.
