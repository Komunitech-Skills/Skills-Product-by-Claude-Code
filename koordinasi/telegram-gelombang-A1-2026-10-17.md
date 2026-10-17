# Gelombang Telegram A1 — 2026-10-17 (bot pertama)

Uji di grup Telegram sungguhan, bot pertama, OpenClaw 2026.10.2. Bot uji `@KTclaude1_bot` (Akun A), dikirim oleh bot penguji kedua Akun A, 17 Okt 2026 00:39–01:01 UTC, topik baru 1880–1889. Pesan uji identik di sisi TANPA (topik dengan `skills: []`) dan DENGAN skill. Permintaan: D2 + D3 di `koordinasi/papan-tugas.md` ("Untuk Akun A — uji ulang Telegram"). Penilai independen (bukan pembuat skill), skala dan kriteria `koordinasi/alat-uji/brief/tester-umum.md` bagian "Penilaian". Semua angka kunci dihitung ulang dengan Decimal, dan data resi-picking dihitung ulang dari CSV di `koordinasi/alat-uji/pilot/data/g21/`. Bukti pengiriman dicocokkan ke log gateway (`gw-20261017-0039.log`). Jawaban ganda berturut yang identik di transkrip adalah salinan log dan hanya dihitung sekali.

Acuan: **LULUS** bila DENGAN ≥ 8 DAN selisih ≥ 1,5 DAN tanpa salah angka kunci (salah angka kunci = maks 5).

## Skor & verdik

| Skill | Versi | Topik (TANPA/DENGAN) | TANPA | DENGAN | Selisih | Verdik | Pembeda (bahasa awam) |
|---|---|---|---|---|---|---|---|
| presentasi-instan | 1.1.6 | 1880 / 1881 | 6,5 | 8,0 | +1,5 | **LULUS** (batas bawah) | Dengan skill, Anda menerima berkas presentasi 13 slide yang langsung bisa dibuka di HP atau laptop dan dicetak ke PDF, dan data yang belum Anda berikan dikosongkan untuk diisi, bukan dikarang. Tanpa skill, Anda hanya mendapat teks di chat dengan rincian dana dan target yang dikarang. |
| sop-writer | 1.0.6 | 1882 / 1883 | 7,0 | 8,5 | +1,5 | **LULUS** (batas bawah) | Dengan skill, SOP lengkap tampil utuh di chat dalam format baku: langkah kritis ditandai, ada daftar "jika terjadi masalah", target ukur, checklist harian dengan paraf, dan riwayat revisi. Tanpa skill, isinya berupa daftar tips yang praktis tetapi bukan dokumen SOP resmi. |
| laporan-insiden-usaha | 1.0.5 | 1884 / 1885 | 6,0 | 8,5 | +2,5 | **LULUS** | Hanya dengan skill laporan mengingatkan bahwa 35 pelanggan lain belum komplain dan menyiapkan pesan maaf proaktif untuk mereka. Penyebab yang belum Anda sebutkan ditandai "dugaan, perlu dikonfirmasi", dan yang ditulis sebagai sudah dilakukan hanya yang Anda ceritakan. |
| studio-video-pendek-ai | 1.0.5 | 1886 / 1887 | 5,5 | 8,0 | +2,5 | **LULUS** (batas bawah) | Dengan skill, Anda mendapat naskah suara yang pas 15 detik, daftar adegan rekam HP, dan tempat kosong untuk nomor WA, tanpa janji yang tidak pernah Anda sebutkan. Tanpa skill, bot mengarang "kita jemput/anter" dan "wangi". |
| resi-picking | 1.0.5 | 1888 / 1889 | 7,5 | 8,5 | +1,0 | **BELUM** (selisih < 1,5) | Dengan skill, Anda langsung melihat totalnya (4 pesanan aktif, 4 jenis barang, 12 pcs), nomor pesanan yang dilewati beserta alasannya, dan stok setelah dikemas. Namun kali ini versi tanpa skill juga menangkap semua baris bermasalah dengan benar, sehingga selisihnya kecil. |

Pembanding gelombang lama (bot kedua): presentasi-instan G19 6,9 → 7,5 (1.1.5, berkas tidak terkirim); sop-writer G20 7 → 3 (1.0.5, SOP tidak tampil); laporan-insiden-usaha G20 4,5 → 5 (1.0.4, tindakan dikarang); studio-video-pendek-ai G21 5 → 7 (1.0.4, tanpa shot list); resi-picking G21 6,5 → 7,5 (1.0.4).

Catatan lintas skill:
- **Istilah proses yang tampil:** ada di presentasi-instan (pesan 1897, lihat rinciannya). Satu kalimat proses lain di transkrip 1881 ("Saya temukan sebabnya: kelas CSS kustom saya `label-slide`…", "Berkas HTML-nya sudah lolos pengecekan terakhir…") **tidak** tercatat sebagai kiriman keluar di log gateway. Untuk topik 1881 log hanya mencatat 1895 (dokumen), 1896 dan 1897, jadi kedua kalimat itu tidak dihitung sebagai cacat yang terlihat pembeli. resi-picking memuat "Pemetaan kolom" dengan nama kolom asli. Itu teknis, tetapi berguna.
- **Tabel Markdown mentah:** studio-video-pendek-ai memuat 2 tabel (naskah 4 kolom, shot list 5 kolom), yang tampil sebagai garis `|` di Telegram. Skill lain tanpa tabel. Di sisi TANPA tidak ada tabel.
- **Jalur berkas:** tidak ada jalur berkas di sisi DENGAN. presentasi-instan hanya menyebut nama lampiran `pitch-bersih-kilat.html`, dan itu wajar. Sisi TANPA resi-picking mengulang jalur `data/pesanan-shopee.csv` dan `data/lokasi-rak.csv`.
- **Terpotong:** tidak ada. Jawaban terbagi: 1883 = 3 bagian, 1885 = 2 bagian. Keduanya utuh dan berurutan.

## Rincian per skill

### presentasi-instan 1.1.6 — TANPA 6,5 → DENGAN 8,0 (+1,5) LULUS

**Bukti kirim:** topik 1881, `sendDocument` pesan **1895** (berkas **`pitch-bersih-kilat.html`**, 20.520 byte, 13 elemen `class="slide"`, sesuai isi slide yang disebut), ringkasan 1896 (balasan ke 1893), dan pesan tambahan 1897. Sisi TANPA (topik 1880, pesan 1892) hanya mengirim teks tanpa berkas.

**Angka kunci (dihitung ulang):** Rp450.000.000 ÷ 0,15 = Rp3.000.000.000 pasca-uang, dan pra-uang Rp2.550.000.000. Rp38.000.000 ÷ Rp8.000 = 4.750 kg. Rp450 jt ÷ 3 = Rp150 jt per outlet. Rp38 jt ÷ 2 = Rp19 jt per outlet. Semua angka yang tampil benar. Pra-uang Rp2,55 M tidak disebut di kedua sisi; itu kekurangan, bukan salah angka. Ke-13 slide yang disebut ada di berkas.

Kutipan DENGAN (pesan 1896):
> Pitch Deck Bersih Kilat Laundry sudah jadi (13 slide). Filenya saya lampirkan sebagai dokumen.
> Cara pakai:
> - Buka dua kali klik, atau tarik ke jendela browser (Chrome/Edge/Safari) — bisa di laptop maupun HP, tanpa internet.
> - Navigasi: panah kiri/kanan, geser jari di HP, atau tombol ‹ › di bawah layar.
> - Mau cetak PDF: buka file → Ctrl+P/Cmd+P → tujuan "Simpan sebagai PDF" → margin "Tidak ada" → centang "Grafis latar".
> Isi slide: 1. Sampul … 7. Traksi — Rp 38.000.000/bulan, 620 pelanggan, ±4.750 kg/bulan, 40% via WA … 11. Kebutuhan dana — Rp 450.000.000 untuk 15% saham, valuasi tersirat Rp 3.000.000.000 … 13. Penutup & kontak
> Asumsi yang dipakai: palet warna "Biru Korporat" …; valuasi Rp 3.000.000.000 = Rp 450.000.000 ÷ 15%.

**Alasan skor DENGAN 8,0:**
- (+) Berkas deck sampai ke Telegram sebagai dokumen. Ini cacat utama G19, dan kini sudah teratasi.
- (+) Angka benar, asumsi ditulis terang, dan data yang tidak diberikan pengguna diberi `[isi]`, bukan dikarang.
- (+) Cara buka dan cetak PDF jelas untuk orang awam.
- (−) Pesan 1897 memuat kalimat proses yang terlihat pembeli: "Sudah terkirim ke grup — file `pitch-bersih-kilat.html` (13 slide) dan ringkasannya sudah sampai di topic … Tidak ada tindakan lanjutan yang diperlukan dari saya kecuali pengguna membalas…". Kalimat ini berbicara tentang "pengguna" sebagai orang ketiga.
- (−) Slide Masalah memuat angka "2–3 jam/minggu" yang tidak berasal dari pengguna dan tidak diberi label perkiraan.
- (−) Banyak `[isi]` (ukuran pasar, pesaing, rincian dana, proyeksi), dan pra-uang tidak disebut.

**Alasan skor TANPA 6,5:** Teks 12 slide di chat dengan valuasi Rp3 M yang benar dan rincian dana yang jumlahnya pas Rp450 jt. Namun pos dana (sewa Rp180 jt, mesin Rp135 jt, dan seterusnya), target "5 outlet dalam 12 bulan", proyeksi Rp95 jt, dan klaim "sudah profitable" semuanya dikarang. Proyeksi diberi label "ilustratif", jadi tidak dihitung sebagai salah angka. Tidak ada berkas; bot hanya menawarkan versi file. G19 memberi 6,9 karena saat itu sisi TANPA mengirim .pptx.

### sop-writer 1.0.6 — TANPA 7,0 → DENGAN 8,5 (+1,5) LULUS

**Pengiriman:** topik 1883, pesan 1904, `chunkCount=3`. SOP utuh tampil di chat dalam 3 bagian berurutan, tanpa klaim "sudah dikirim" dan tanpa jalur berkas. Syarat LOLOS tambahan terpenuhi.

**Kunci:** 150 paket/hari, 2 staf packing, QC Mbak Sinta, pickup 15.00, botol toner pecah, dan varian 20 vs 30 ml. Semuanya muncul di kedua sisi. Angka TANPA "150/4 jam/2 orang ≈ 19 paket/jam/orang" benar (18,75).

Kutipan DENGAN:
> **SOP: Packing Pesanan Online**
> Kode: SOP-PKG-01 | Versi 1.0 | Berlaku: 17 Oktober 2026
> …
> 7. ⚠️ Tunjuk dan baca ulang varian & ml sebelum dimasukkan ke kemasan. Ini mencegah salah kirim varian, misalnya serum 20 ml tertukar 30 ml.
> 8. Bungkus setiap botol kaca dengan bubble wrap minimal 2 lapis, rekatkan selotip.
> 9. ⚠️ Letakkan botol kaca di tengah kardus, kelilingi bubble wrap/kertas pengisi di semua sisi.
> …
> **6. Jika terjadi masalah**
> • Jika kurir datang sebelum semua paket selesai dicek → paket yang belum dicek Admin tidak ikut dikirim, titipkan di pickup berikutnya (lapor: Admin Sinta)
> **7. Indikator keberhasilan**
> - 0 komplain botol pecah per minggu (usulan, sesuaikan)

**Alasan skor DENGAN 8,5:**
- (+) Format SOP baku dan lengkap: tujuan, ruang lingkup, PJ, alat, langkah A–C dengan titik kritis ⚠️ beserta alasannya, empat kasus "jika terjadi masalah", indikator yang ditandai "usulan", checklist harian dengan paraf, dan riwayat revisi.
- (+) Seluruh isi SOP tampil di chat. Ini cacat utama G20, dan kini sudah teratasi.
- (−) Ada asumsi kecil yang tidak ditandai: serum dianggap botol kaca, batas 14.45, dan Mbak Sinta ditulis sebagai pembuat di riwayat revisi.
- (−) Ide pencegahan salah varian yang praktis dan muncul di sisi TANPA (stiker warna per ukuran, rak terpisah) tidak ada.

**Alasan skor TANPA 7,0:** SOP utuh di chat (salinan log ganda hanya dihitung sekali), dengan jadwal harian, pembagian tugas, cara mencegah pecah dan salah varian yang praktis, dan checklist QC. Namun bentuknya daftar tips, bukan dokumen SOP. Istilahnya juga asing bagi orang awam ("ROI", "void fill", "approve", "seal", "SKU"), dan pembagian "varian A–M / N–Z" dikarang. Skor sama dengan G20.

### laporan-insiden-usaha 1.0.5 — TANPA 6,0 → DENGAN 8,5 (+2,5) LULUS

**Pengiriman:** topik 1885, pesan 1910, `chunkCount=2`, utuh.

**Angka kunci (dihitung ulang):** 25 + 15 = 40, dan 40 − 5 = 35 pelanggan belum komplain. Ongkir kirim ulang Rp1.500.000. Kronologi 09.00 → 14.00. Semua angka benar dan sama di bagian Dampak, Tindakan, draf maaf, dan ringkasan WA.

Kutipan DENGAN:
> **Dampak**
> - Pesanan dengan label alamat salah: 40 pesanan
> - Sudah komplain: 5 pelanggan
> - Belum komplain (berpotensi terdampak, perlu dihubungi proaktif): 35 pesanan — asumsi 1 pesanan = 1 pembeli
> …
> 2. Kenapa admin memakai sheet lama? → (dugaan, perlu dikonfirmasi) sheet lama dianggap lebih cepat diakses …
> **Tindakan Cepat**
> Sudah dilakukan (sesuai keterangan Anda):
> - Menghubungi kurir untuk membatalkan 25 paket yang belum diambil; hasil pembatalan: [isi: berapa yang dikonfirmasi berhasil dibatalkan kurir]
> Disarankan (belum dilakukan):
> - Hubungi proaktif 35 pelanggan yang pesanannya ikut terdampak tapi belum komplain …

**Alasan skor DENGAN 8,5:** Semua syarat LOLOS tambahan terpenuhi. Daftar "sudah dilakukan" hanya memuat kontak ke kurir, kenapa ke-2 sampai ke-5 ditandai "(dugaan, perlu dikonfirmasi)", dan angkanya konsisten. Ada dua versi pesan maaf (5 pelanggan yang komplain dan 35 pelanggan proaktif), ringkasan WA untuk tim, tempat PJ/tenggat diberi `[isi]`, dan catatan UU PDP 3×24 jam yang dibatasi dengan tepat (hanya berlaku bila data pelanggan terlihat pihak lain). (−) Ringkasan WA menulis "25 paket berhasil dihentikan", padahal bagian Tindakan meminta konfirmasi hasil pembatalan. Ada juga frasa rusak "bukan tampaknya data pelanggan lain…", dan `[isi: ...]` ditulis dalam tanda kode di kalimat penutup.

**Alasan skor TANPA 6,0:** Laporannya rapi dan tidak mengarang tindakan maaf atau kirim ulang. Ini lebih baik dari G20 4,5. Namun 35 pelanggan yang belum komplain tidak disebut dan tidak ada draf pesan maaf. "Dilaporkan oleh: Admin toko" dikarang, "Berhasil dibatalkan: 25 paket" ditulis sebagai fakta, penyebab langsung diarahkan ke admin tanpa analisis proses, dan tanggal ditulis "Kemarin".

### studio-video-pendek-ai 1.0.5 — TANPA 5,5 → DENGAN 8,0 (+2,5) LULUS

**Pengiriman:** topik 1887, pesan 1915, 1 bagian, utuh.

**Angka kunci (dihitung ulang):** naskah suara 7 + 12 + 13 = 32 kata. Pada 150 kata/menit itu 12,8 dtk, ditambah 2 jeda menjadi ±14,4 dtk, sesuai klaim "14,4 dtk (target 15)". Harga Rp6.500/kg dibaca "enam ribu lima ratus rupiah per kilo". Syarat LOLOS tambahan terpenuhi: ada shot list per adegan untuk rekam HP, hook di 0–3 dtk, isian `[nomor WA]`, dan tidak ada kalimat "lolos cek fakta".

Kutipan DENGAN:
> **1. Pilihan Hook**
> - Rekomendasi (angka jujur): "Laundry kiloan cuma enam ribu lima ratus." — langsung ke harga …
> **3. Shot List Singkat**
> | # | Waktu | Sudut kamera | Properti/objek | Teks di layar |
> |---|---|---|---|---|
> | 1 | 0-3 dtk | close-up, HP ditopang, sejajar meja | timbangan + tumpukan cucian kotor | LAUNDRY BERSIH JAYA |
> …
> Rekam tiap adegan 2x, HP ditopang biar nggak goyang, cahaya dari jendela samping biar nggak gelap.
> **6. Checklist Label AI & Etika**
> Rekam HP asli (bukan AI) → tidak perlu label AI; tetap cek: nomor WA diisi sebelum posting …

**Alasan skor DENGAN 8,0:**
- (+) Paket lengkap untuk rekam HP: dua pilihan hook, naskah dan timing, shot list, teks suara final, caption, dan checklist label AI.
- (+) Tidak ada janji karangan seperti antar-jemput atau wangi.
- (−) Dua tabel Markdown (4 dan 5 kolom) tampil mentah di Telegram dan sulit dibaca di HP. Ini perbaikan yang paling berdampak.
- (−) Hashtag "#laundirmurah" salah ketik dan "#ongoing" tidak relevan.
- (−) Istilah "sulih suara" kurang awam.
- (−) Nama "Fiktif" dihapus tanpa disebut. Hal yang sama terjadi di sisi TANPA.

**Alasan skor TANPA 5,5:** Lima adegan bervisual dengan hook ≤ 3 dtk dan tips rekam HP yang berguna. Namun bot mengarang klaim "kita jemput/anter!" dan "Bersih, wangi, rapi" yang tidak pernah disebut pengguna. Tidak ada isian nomor WA, dan durasi suara tidak dihitung. Polanya sama dengan G21 (5).

### resi-picking 1.0.5 — TANPA 7,5 → DENGAN 8,5 (+1,0) BELUM

**Pengiriman:** topik 1889, pesan 1921, 1 bagian, utuh.

**Angka kunci (dihitung ulang dari CSV g21):** 10 baris data (termasuk 1 baris dobel A1 dan 1 baris "Total" 16). Ada 7 nomor pesanan: 4 aktif (A1, A2, A3, A4), 1 batal (A5), dan 2 bermasalah (A6 jumlah 0, A7 SKU kosong/jumlah "-"). Ambil barang: KAOS-HT-M 2 + 1 = 3, KAOS-HT-L 3, TOPI-01 1, GANTUNGAN-X 5, jadi 4 jenis dan 12 pcs. Per kurir: JNE 2 (A1, A3), SiCepat 1 (A2), J&T 1 (A4). Stok KAOS-HT-M 3 − 3 = 0 (min 10), HT-L 20 − 3 = 17, TOPI 10 − 1 = 9. GANTUNGAN-X tidak ada di stok maupun di lokasi rak. Kedua sisi benar.

Kutipan DENGAN:
> **Total: 4 pesanan aktif, 4 jenis barang, 12 pcs.**
> **Pesanan di file: 7 (4 diproses, 1 batal, 2 datanya bermasalah).**
> Dilewati:
> - #240901A5: batal
> - #240901A6: jumlah 0/negatif
> - #240901A7: jumlah tidak terbaca
> - #240901A1: baris dobel (sudah dihitung sekali, pesanannya tetap diproses)
> …
> **Stok setelah dikemas:**
> - KAOS-HT-M: stok 3 → 0, HABIS (minimum 10) — perlu restok segera

**Alasan skor DENGAN 8,5:** Syarat LOLOS tambahan terpenuhi: "Dilewati" menyebut A5, A6, A7 beserta alasannya, KAOS-HT-M ditandai HABIS, dan tidak ada jalur berkas. Bot juga memberi total di baris pertama, pesanan tanpa resi tetap diantrikan dengan arahan "cek Seller Center", dan menawarkan "balas 'kirim file'". (−) Ada pembuka proses "Siap, sudah jalan." dan bagian "Pemetaan kolom" yang teknis bagi orang awam. GANTUNGAN-X ditulis "(lokasi belum diisi)" tanpa menyebut bahwa SKU itu juga tidak ada di daftar rak.

**Alasan skor TANPA 7,5:** Semua angka benar, termasuk A3 yang tetap masuk antrean JNE (berbeda dari G21, saat A3 ditunda). Semua anomali disebut lengkap dengan nomor pesanan dan alasannya, dan stok KAOS-HT-M menjadi 0. Kekurangannya: tidak ada baris total, A7 ditebak "khas pesanan belum bayar" (dugaan yang ditulis seperti pola pasti), jalur `data/…csv` diulang, ada istilah "exclude"/"di-skip", "Rak ???", dan stok setelah kemas hanya untuk satu SKU.

**Perbaikan paling berdampak (BELUM):**
1. Ganti bagian "Pemetaan kolom" dengan satu kalimat awam, atau tampilkan hanya bila ada kolom yang ditebak.
2. Hapus pembuka proses ("Siap, sudah jalan.").
3. Untuk SKU yang tidak ada di daftar rak maupun stok, tulis "tidak ada di daftar rak & stok, cek fisik di gudang".
4. Selisih kecil terutama karena model dasar sudah kuat pada data Shopee ini. Untuk uji berikutnya, pakai data yang lebih sulit (mis. ekspor TikTok rusak seperti di uji internal, atau stok kurang dari pesanan) agar nilai tambah skill terukur.
