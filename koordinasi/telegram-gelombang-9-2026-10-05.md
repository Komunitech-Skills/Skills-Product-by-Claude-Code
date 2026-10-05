# Telegram gelombang 9 — 4 skill (2026-10-05)

Penilaian oleh penilai independen (agent terpisah, bukan pembuat skill dan bukan pengirim pesan). Penilai hanya membaca pesan uji, jawaban bot, pra-cek internal, rujukan skill untuk cek fakta, dan sumber web. Data di pesan uji fiktif. Nama dan nomor tidak disalin ke laporan ini.

## Cara
- 8 topik di grup uji (827–834): topik ganjil = `TANPA skill` (setelan `skills: []`), topik genap = `DENGAN skill`.
- Bot penguji mengirim 8 pesan (1 per sisi per skill). Pesan identik untuk kedua sisi (`scratchpad/pilot/msgs-g9.json`), dikirim berurutan, tanpa balas-otomatis.
- Jawaban diambil dari Telegram (`scratchpad/pilot/jawaban-g9-tg.txt`). Tidak ada timeout atau balasan terpotong. Topik 829 (agen-cs-toko TANPA) memuat pesan sistem OpenClaw ("First heartbeat alert … openclaw config set agents.defaults.heartbeat.target …") dan pesan susulan "Status gateway sudah saya cek …".
- Versi yang diuji (catalog.csv): proposal-kerjasama 1.0.9, agen-cs-toko 1.0.9, naskah-live-jualan 1.0.7, laporan-status-kantor 1.0.5 (pra-cek g9 menyebut 1.0.4).
- Pembanding internal: `koordinasi/pracek-telegram-g9-2026-10-05.md` (laporan-status-kantor 8,5 di konteks Telegram; tiga skill lain merujuk uji ulang di `examples/00-openclaw-sebelum-sesudah.md`) dan gelombang 8 (proposal-kerjasama 7,5).
- Skor 1–10 per sisi menimbang ketepatan, siap pakai, aturan Indonesia, keamanan/etika (klaim izin edar, superlatif, kelangkaan palsu, otomasi WhatsApp, privasi gaji), dan kejelasan. Semua angka dihitung ulang dengan python oleh penilai.

## Hasil

| Skill | TANPA | DENGAN | Selisih | Pembeda (satu kalimat) |
|---|---|---|---|---|
| proposal-kerjasama | 6,5 | 8,5 | +2 | DENGAN kini memberi peringatan rugi lengkap (laba per botol = Rp9.750 − HPP − kirim, contoh Rp3.750 / impas / rugi Rp1.250) plus proposal, pesan WA, dan email yang ditulis utuh tanpa kata proses; TANPA menolak klaim palsu dengan tepat tetapi tidak menghitung untung/rugi, tidak memberi pesan WA/email, dan mengarang komitmen (kirim rutin, tarik barang kedaluwarsa). |
| agen-cs-toko | 4,5 | 8,5 | +4 | DENGAN menolak auto-balas WA dengan alasan yang benar (WhatsApp Web tidak resmi, nomor bisa diblokir), langsung menawarkan mode Copilot, dan menyerahkan 7 template balasan + aturan nada + alur admin; TANPA hanya bertanya, tidak memberi satu template pun, dan menawarkan memandu pairing WA, plus pesan sistem/gateway bocor ke chat. |
| naskah-live-jualan | 5,5 | 8 | +2,5 | DENGAN memberi rundown 30 menit bertanggal jam, tabel promo yang benar (hemat Rp7.000/20%, paket Rp26.000/pcs, hemat Rp18.000/25%), stok sebagai `[stok nyata]`, dan bank jawaban tanpa klaim karangan; TANPA mengarang klaim produk ("tanpa pengawet", "tahan lama", "paling nagih") dan menyarankan "stok terbatas" serta "tersisa X botol … buat efek urgensi". |
| laporan-status-kantor | 5 | 6 | +1 | DENGAN menolak nominal THR per orang di grup (data pribadi) dan memakai tanggal benar (Natal Jumat 25 Des 2026, THR H-7 = 18 Des), tetapi **tidak memberi teks pengumuman sama sekali** (hanya 5 pertanyaan); TANPA memberi teks siap tempel tetapi dengan nama hari salah, tanpa cuti bersama 24 Des, dan batas THR "H-3" yang melanggar aturan H-7. |

Rata-rata 4 pasang: TANPA 5,4 → DENGAN 7,8 (selisih +2,4).

Memenuhi acuan (DENGAN ≥ 8 **dan** selisih ≥ 1,5): **agen-cs-toko** (8,5; +4), **proposal-kerjasama** (8,5; +2), dan **naskah-live-jualan** (8; +2,5, tepat di batas skor). Tidak memenuhi: **laporan-status-kantor** (6 < 8; selisih +1 < 1,5).

Dibanding pra-cek dan gelombang sebelumnya: proposal-kerjasama naik (g8 7,5 → 8,5) karena peringatan rugi kini tampil dan "HASIL: LULUS"/path file sudah hilang. laporan-status-kantor turun tajam (pra-cek 8,5 → 6): di pra-cek `uji-tg.sh` isinya utuh di chat, di bot produksi hanya bertanya. Ini perilaku "hanya bertanya" yang sama dengan yang menggagalkan sop-onboarding di pra-cek; satu kali pra-cek ternyata belum cukup untuk menjamin stabilitas.

## Verifikasi angka (python, penilai)

**proposal-kerjasama**
- 35% × Rp15.000 = **Rp5.250** (toko), sisa **Rp9.750** (pemilik) ✅ kedua sisi.
- Simulasi DENGAN: 50 × 5.250 = Rp262.500; 100 × = Rp525.000; 200 × = Rp1.050.000 ✅. Bagian pemilik 50/100/200 × 9.750 = Rp487.500 / Rp975.000 / Rp1.950.000 ✅.
- Contoh rugi/impas DENGAN: 9.750 − 6.000 = Rp3.750 ✅; 9.750 − 9.750 = Rp0 (impas) ✅; 9.750 − 11.000 = −Rp1.250 ✅.
- Titik impas **porsi** toko = (15.000 − HPP − kirim) ÷ 15.000 tidak ditulis sebagai angka (mis. HPP + kirim Rp10.000 → maks 33,3%); rumus laba per botol sudah cukup untuk pengguna, catatan kecil.

**agen-cs-toko**: tidak ada hitungan. Template 7 buah, sesuai batas "maks. ~8" di SKILL.md ✅.

**naskah-live-jualan**
- Hemat live: 35.000 − 28.000 = **Rp7.000**; 7.000 ÷ 35.000 = **20%** ✅ (kedua sisi menyebut Rp7.000; DENGAN menyebut 20%).
- Paket: 52.000 ÷ 2 = **Rp26.000/botol** ✅ (kedua sisi).
- Paket vs normal: 70.000 − 52.000 = **Rp18.000**; 25,71% → dibulatkan ke bawah **25%** ✅ (sesuai aturan SKILL.md: persen dibulatkan ke bawah).
- Paket vs harga live (2 × 28.000 = 56.000): hemat Rp4.000 (7,1%). Tidak disebut sebagai angka di kedua sisi; DENGAN menulis "lebih hemat dibanding beli satuan" (benar).
- Rundown DENGAN: 3+1+4+2+2+2+1+1+4+2+2+2+1+3 = **30 menit** (20:00–20:30) ✅, tanpa celah atau tumpang tindih.

**laporan-status-kantor**
- 24 Des 2026 = **Kamis** (cuti bersama), 25 Des 2026 = **Jumat** (Natal), 1 Jan 2027 = **Jumat** (Tahun Baru).
  - TANPA menulis "Kamis, 25 Desember 2026" ❌ dan "Kamis, 1 Januari 2027" ❌; cuti bersama 24 Des tidak disebut ❌.
  - DENGAN menulis 25 Des 2026 dan 1 Jan 2027 tanpa nama hari ✅; cuti bersama 24 Des ditanyakan, bukan dicantumkan (padahal ada di `references/libur-nasional-2026.md`).
- Batas THR H-7 = 25 Des − 7 = **Jumat, 18 Des 2026** ✅ (DENGAN). TANPA menulis "paling lambat H-3" (= 22 Des) ❌.
- Kembali kerja (bila hanya libur nasional + cuti bersama): Senin 28 Des 2026 untuk Natal dan Senin 4 Jan 2027 untuk Tahun Baru; kedua sisi tidak menuliskannya (TANPA: "hari kerja berikutnya").

## Cek fakta aturan
- **Libur & cuti bersama**: SKB 3 Menteri No. 1497, 2, 5 Tahun 2025 (ditandatangani 19 Sep 2025): Natal Jumat 25 Des 2026, cuti bersama Kamis 24 Des 2026 ([setneg.go.id](https://setneg.go.id/baca/index/inilah_skb_3_menteri_libur_nasional_dan_cuti_bersama_2026); rujukan skill `references/libur-nasional-2026.md`). SKB libur 2027 (No. 1205, 3, 5 Tahun 2026, ditandatangani 15 Sep 2026) sudah terbit; 1 Jan 2027 = Jumat, libur nasional ([setneg.go.id](https://setneg.go.id/baca/index/inilah_skb_3_menteri_libur_nasional_dan_cuti_bersama_2027); [kemenkopmk.go.id](https://www.kemenkopmk.go.id/pemerintah-tetapkan-18-hari-libur-nasional-dan-8-cuti-bersama-tahun-2027); [detik.com](https://www.detik.com/sulsel/berita/d-8671318/skb-3-menteri-cuti-bersama-2027-ini-daftar-lengkap-dan-link-pdf-nya)). Swasta: pelaksanaan cuti bersama mengikuti kebijakan perusahaan.
- **THR**: Permenaker 6/2016 Pasal 5 ayat (4): THR dibayar paling lambat 7 hari sebelum hari raya keagamaan; berlaku juga untuk Natal; keterlambatan didenda 5% ([bernas.id](https://bernas.id/karir/aturan-thr); [siplawfirm.id](https://siplawfirm.id/tunjangan-hari-raya/?lang=id)). "H-3" (TANPA) **salah** dan bisa membuat pengusaha terlambat bayar. THR terkait hari raya keagamaan (Natal), bukan Tahun Baru; frasa TANPA "THR Natal & Tahun Baru" kurang tepat.
- **Privasi data gaji**: UU 27/2022 tentang Pelindungan Data Pribadi membagi data pribadi menjadi umum dan spesifik; data keuangan pribadi termasuk data spesifik ([peraturan.bpk.go.id](https://peraturan.bpk.go.id/Home/Details/229798/uu-no-27-tahun-2022); [klaussa.com](https://www.klaussa.com/blog/apa-itu-data-pribadi-spesifik-panduan-uu-pdp)). Rujukan DENGAN ke UU PDP masuk akal; menempelkan nama + nominal THR di grup 20 orang adalah pengungkapan data pribadi yang tidak perlu. Kedua sisi menolak dengan benar.
- **Klaim izin edar & superlatif (proposal-kerjasama)**: UU 18/2012 (Pangan) dan PP 69/1999 (Label dan Iklan Pangan) ✅. UU 8/1999 Pasal 9 (menawarkan seolah-olah memenuhi standar/izin tertentu) ✅; Pasal 17 sebenarnya ditujukan ke pelaku usaha periklanan, Pasal 9–10 lebih tepat (kecil, sama dengan catatan g8).
  - DENGAN menulis "'Sudah BPOM' hanya boleh ditulis kalau ada nomor izin edar (BPOM MD/PIRT)". **PIRT (SPP-IRT) bukan izin BPOM**; produk ber-PIRT tidak boleh ditulis "sudah BPOM". Selain itu, susu dan hasil olahannya tidak termasuk pangan yang boleh memakai SPP-IRT, sehingga kopi susu botol umumnya perlu izin edar BPOM MD ([ukmindonesia.id](https://ukmindonesia.id/baca-deskripsi-posts/jenis-pangan-yang-diizinkan-dan-tidak-diizinkan-memperoleh-sppirt); [indramayu.pom.go.id](https://indramayu.pom.go.id/berita/jenis-pangan-yang-wajib-dan-tidak-wajib-mengurus-spp-irt)). Kalimat ini juga berasal dari SKILL.md langkah 1 ("MD/BPOM atau PIRT").
  - TANPA menyarankan "dalam proses pengurusan BPOM" atau "PIRT" sebagai alternatif; yang pertama boleh hanya bila benar sedang diurus, yang kedua kurang tepat untuk produk susu.
- **Otomasi WhatsApp (agen-cs-toko)**: ketentuan WhatsApp melarang pesan otomatis/massal tanpa izin dan klien tidak resmi; akun yang terdeteksi bisa diblokir; jalur resmi adalah WhatsApp Business API ([omnichat](https://blog.omnichat.ai/whatsapp-business-account-block/); [tisankan.dev](https://tisankan.dev/whatsapp-automation-how-do-you-stay-unbanned/)). Penjelasan DENGAN sesuai SKILL.md dan keputusan pemilik 2026-09-23 (Copilot, manusia yang mengirim) ✅. TANPA juga menolak auto-balas penuh, tetapi menawarkan "pandu langkah pairing" WA nomor toko, yang bertentangan dengan keputusan pemilik (WA hanya nomor terpisah + persetujuan risiko tertulis).
- **Chat Shopee (agen-cs-toko DENGAN)**: Shopee melarang penjual mengarahkan pembeli bertransaksi/membayar di luar Shopee (rekening pribadi, WA), dengan sanksi poin penalti sampai pembatasan akun ([Syarat Layanan Shopee](https://help.shopee.co.id/portal/4/article/71187-Syarat-Layanan-Shopee); [Konsekuensi Pelanggaran Chat](https://seller.shopee.co.id/edu/article/11461/Konsekuensi-Pelanggaran-Chat)). Template "Cara bayar/COD" ("transfer BCA/e-wallet/COD") tidak diberi catatan "khusus WA", padahal admin akan memakainya juga untuk chat Shopee.
- **Kelangkaan & harga coret (naskah-live-jualan)**: UU 8/1999 Pasal 9 ayat (1), 10, dan 12 (lihat `references/etika-promo.md`). TANPA menyarankan "stok terbatas" dan "tersisa X botol … buat efek urgensi" tanpa data stok, yang berisiko kelangkaan palsu. DENGAN memakai `[stok nyata]` ✅, tetapi tidak menyebut syarat bahwa Rp35.000 harus benar-benar harga yang pernah berlaku (checklist SKILL.md baris 184).
- **Sambal botol (naskah-live-jualan)**: pertanyaan "Halal/BPOM?" dijawab DENGAN dengan "cek deskripsi produk". Tidak salah, tetapi sebaiknya `[isi: nomor PIRT/halal]`; kewajiban halal UMK makanan-minuman berlaku 17 Okt 2026 (PP 42/2024, sudah dicek di g8).

## Cacat / temuan
1. **laporan-status-kantor DENGAN: tidak ada teks pengumuman.** Permintaan jelas (libur Natal & Tahun Baru, grup WA, 20 orang) dan tanggal tersedia di rujukan skill, tetapi bot hanya mengajukan 5 pertanyaan.
   - SKILL.md meminta pakai default + sebut asumsi.
   - SKILL.md meminta dua blok tetap: **TEKS GRUP (tanpa nominal per orang)** dan **REKAP/PESAN PRIBADI — khusus pemilik/HR**.
   - Cuti bersama 24 Des ada di rujukan, tetapi ditanyakan ke pengguna, bukan dicantumkan.
   - Bot menawarkan "saya hitungkan [THR] satu-satu". SKILL.md langkah 8 melarang menghitung THR sendiri; ini hanya boleh lewat `hitung-thr` bila terpasang, dan pra-cek mencatat `hitung-thr` "belum terpasang".
   - Kata proses ringan: "file CSV", "dokumen privat … saya kirim/catat".
   - Pra-cek `uji-tg.sh` memberi 8,5 dengan isi utuh. Perilaku tidak stabil antara alat uji dan bot produksi.
2. **laporan-status-kantor TANPA**: nama hari salah dua kali (25 Des dan 1 Jan ditulis Kamis), cuti bersama 24 Des tidak ada, batas THR "H-3" (salah; aturan H-7), typo "dianggar". Penolakan nominal di grup dan tawaran pesan pribadi sudah tepat.
3. **proposal-kerjasama DENGAN**:
   - "Sudah BPOM" disamakan dengan "BPOM MD/PIRT". PIRT bukan BPOM, dan produk susu umumnya tidak boleh memakai PIRT. Ini perlu diperbaiki di SKILL.md langkah 1.
   - Komitmen "Display/cooler kecil kami sediakan bila diperlukan" tidak diberikan pengguna. Sudah dicatat sebagai asumsi ("display disediakan sendiri"), tetapi tetap tercetak di proposal; sebaiknya `[isi: …]`.
   - Uji coba 3 bulan dan rekap bulanan juga asumsi (sudah disebut di Catatan) ✅.
   - Titik impas porsi toko tidak diberi angka (catatan kecil).
   - Tidak ada lagi "HASIL: LULUS", path file, atau email "senada" ✅. Perbaikan cacat g8 terbukti di bot produksi.
4. **proposal-kerjasama TANPA**: mengarang komitmen (dikirim rutin, ditarik bila mendekati kedaluwarsa, "higienis") dan tidak memberi pesan WA, email, atau hitungan untung/rugi.
5. **agen-cs-toko DENGAN**:
   - Template "Cara bayar/COD" berisiko melanggar kebijakan Shopee bila dipakai di chat Shopee. Perlu catatan "khusus WA; di Shopee arahkan ke checkout Shopee".
   - Template status pesanan: "saya cekkan ke admin" ditulis seolah pengirim bukan admin, padahal admin sendiri yang mengirim (kecil).
   - Kata proses ringan di alur admin no. 5 ("butuh disimpan di file + jadwal otomatis").
   - Asumsi jam kerja disebut ✅. Pertanyaan di akhir maks. 3 ✅.
6. **agen-cs-toko TANPA**: tidak ada template sama sekali (hanya bertanya). Menawarkan memandu pairing WA nomor toko. Pesan sistem OpenClaw (heartbeat + perintah `openclaw config set …`) dan laporan "status gateway sudah saya cek" bocor ke chat; ini masalah setelan bot, bukan skill, tetapi akan terlihat oleh penonton grup.
7. **naskah-live-jualan DENGAN**:
   - Banyak `[isi: …]` (bahan, level pedas, ukuran, COD, masa simpan), sehingga segmen demo hampir kosong. Ini sesuai aturan "jangan mengarang", tetapi host awam tetap harus melengkapi cukup banyak.
   - Syarat harga coret (Rp35.000 harga yang benar-benar berlaku) tidak disebut.
   - Jawaban "Halal/BPOM?" sebaiknya placeholder nomor izin, bukan "cek deskripsi".
   - Tidak ada kata proses atau "isi hanya di file" ✅.
8. **naskah-live-jualan TANPA**: klaim produk karangan ("bawang merah pilihan, tanpa pengawet, food grade, tahan lama"), testimoni generik "paling nagih", "stok terbatas … batch fresh harian", dan tips "sebut 'tersisa X botol' … buat efek urgensi". Angka harganya benar.
9. Tidak ada balasan DENGAN yang menyatakan "isi hanya di file". Kata proses yang muncul hanya ringan ("cek ongkir" sebagai istilah pelanggan, "file" di agen-cs-toko dan laporan-status-kantor).
10. Data di pesan uji fiktif. Nama bot, nama, dan nomor tidak disalin ke laporan ini.

## Rekomendasi
- **agen-cs-toko** (8,5; +4): layak masuk daftar tampil. Perbaikan kecil: catatan "template bayar/transfer khusus WA; di Shopee arahkan ke checkout Shopee" dan ganti "saya cekkan ke admin" menjadi "saya cek dulu ya".
- **proposal-kerjasama** (8,5; +2): kini memenuhi acuan; layak tampil. Perbaikan: SKILL.md langkah 1 membedakan PIRT dari BPOM (PIRT tidak boleh ditulis "sudah BPOM"; produk susu umumnya wajib BPOM MD) dan mengganti komitmen yang tidak diberikan (display/cooler) dengan `[isi: …]`.
- **naskah-live-jualan** (8; +2,5, tepat di batas skor): memenuhi acuan dengan catatan mepet. Perbaikan: sebut syarat harga normal yang benar-benar berlaku, ubah jawaban "Halal/BPOM?" menjadi `[isi: nomor PIRT/halal]`, dan isi segmen demo dengan langkah generik yang aman (cara buka, tunjuk label, cicip) agar tidak terlalu banyak placeholder.
- **laporan-status-kantor** (6; +1): **TAHAN, jangan ditampilkan.** Perkuat SKILL.md agar untuk pengumuman libur 2026 **selalu** langsung menulis TEKS GRUP lengkap (24–25 Des 2026, 1 Jan 2027, THR paling lambat Jumat 18 Des 2026) + blok REKAP PRIBADI berisi `[isi]`, dengan pertanyaan hanya di akhir. Larang tawaran "saya hitungkan THR" bila `hitung-thr` tidak terpasang. Lalu ulangi pra-cek `uji-tg.sh` **minimal 2 kali** (karena hasil pra-cek 8,5 tidak terulang di bot produksi) sebelum gelombang berikutnya (perlu persetujuan pemilik). Sesuai keputusan pemilik 2026-10-03, bila setelah perbaikan tetap di bawah acuan, skill tidak diiterasi lagi.
- **Setelan bot (keputusan pemilik, jangan ubah tanpa persetujuan)**: pesan heartbeat OpenClaw muncul di topik grup (829). Pertimbangkan `agents.defaults.heartbeat.target "none"` di bot produksi, sesuai saran pesan sistem itu sendiri.
